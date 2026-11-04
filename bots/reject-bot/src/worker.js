// Telegram bot for adding domains to this repo's rule lists. You send text or a screenshot;
// the "Reject 待办判断" Claude routine (fired through its API trigger) suggests which lists
// each domain belongs in; you pick one per domain with the buttons.
//
//   Reject target        -> the Worker commits it to Rules/Reject (Manual section) right away.
//   <Category>/<Entry>   -> e.g. AI/OpenAI, Bank/HSBC: queued as "approved" and the routine is
//                           fired again; it edits that category's config, runs build.py and
//                           pushes to main, then reports back through /api/applied.
//
// Routes
//   POST /telegram              Telegram webhook (checked with WEBHOOK_SECRET)
//   GET  /api/pending           items waiting for suggestions          (Bearer ROUTINE_TOKEN)
//   GET  /api/photo/:id         an item's screenshot                   (Bearer ROUTINE_TOKEN)
//   POST /api/verdict/:id       the routine's suggestions for an item  (Bearer ROUTINE_TOKEN)
//   GET  /api/approved          category additions you confirmed       (Bearer ROUTINE_TOKEN)
//   POST /api/applied/:id/:i    the routine's result for one of those  (Bearer ROUTINE_TOKEN)
//   POST /api/setup             register the webhook and commands      (Bearer ROUTINE_TOKEN)

import { MANUAL_PATH, REJECT_FILES, applyEntries, cleanCandidate, ruleOf } from "./manual.js";

const TTL = 60 * 60 * 24 * 30; // items expire after 30 days
const CATEGORIES = ["AI", "Bank", "Broker", "Crypto"];
const TARGET_RE = new RegExp(`^(Reject|(${CATEGORIES.join("|")})/[A-Za-z0-9_]{1,40})$`);
const MAX_SUGGESTIONS = 3;
const STATUS_TEXT = {
  added: (d) => `→ 已加入 Reject${d.commit ? `（${d.commit.slice(0, 7)}）` : ""}`,
  existing: () => "→ Reject 里已有，未重复添加",
  approved: (d) => `→ 已确认加入 ${d.target}，等 Claude 写入`,
  applied: (d) => `→ 已加入 ${d.target}${d.commit ? `（${d.commit.slice(0, 7)}）` : ""}${d.note ? `：${d.note}` : ""}`,
  failed: (d) => `→ 加入 ${d.target} 失败：${d.note || "原因未知"}`,
  skipped: () => "→ 已跳过",
};
const FINAL = new Set(["added", "existing", "applied", "failed", "skipped"]);

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const path = url.pathname;
    try {
      if (req.method === "POST" && path === "/telegram") return await telegramWebhook(req, env);
      if (path.startsWith("/api/")) {
        if (!authorized(req, env)) return json({ error: "unauthorized" }, 401);
        if (req.method === "GET" && (path === "/api/pending" || path === "/api/approved")) {
          await env.QUEUE.put("state:fire_read", "1"); // a run has started reading the queues
          return json(path === "/api/pending" ? await pending(env) : await approved(env));
        }
        let m = path.match(/^\/api\/photo\/([a-z0-9]+)$/);
        if (req.method === "GET" && m) return await photo(env, m[1]);
        m = path.match(/^\/api\/verdict\/([a-z0-9]+)$/);
        if (req.method === "POST" && m) return json(await verdict(env, m[1], await req.json()));
        m = path.match(/^\/api\/applied\/([a-z0-9]+)\/(\d+)$/);
        if (req.method === "POST" && m) return json(await applied(env, m[1], Number(m[2]), await req.json()));
        if (req.method === "POST" && path === "/api/setup") return json(await setup(env, url.origin));
      }
      return new Response("not found", { status: 404 });
    } catch (err) {
      console.error(err && err.stack ? err.stack : err);
      return json({ error: String(err && err.message ? err.message : err) }, 500);
    }
  },
};

// ------------------------------------------------------------------ helpers

function json(body, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json" } });
}

function authorized(req, env) {
  const h = req.headers.get("authorization") || "";
  return Boolean(env.ROUTINE_TOKEN) && h === `Bearer ${env.ROUTINE_TOKEN}`;
}

async function tg(env, method, body) {
  const r = await fetch(`https://api.telegram.org/bot${env.TELEGRAM_TOKEN}/${method}`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await r.json();
  if (!data.ok) throw new Error(`telegram ${method}: ${data.description}`);
  return data.result;
}

const isOwner = (env, from) => from && String(from.id) === String(env.TELEGRAM_USER_ID);
const getItem = async (env, id) => upgrade(JSON.parse((await env.QUEUE.get(`item:${id}`)) || "null"));

// Items judged by the first version (verdict: reject|unsure|keep, decision: "added"...) still
// sit in KV for up to 30 days; read them in the current shape.
function upgrade(item) {
  if (!item || !item.verdict) return item;
  for (const c of item.verdict.candidates) {
    if (!c.suggestions) c.suggestions = c.verdict === "keep" ? [] : [{ target: "Reject", note: "" }];
    if (typeof c.decision === "string") c.decision = { target: "Reject", status: c.decision };
    if (!c.decision && !c.suggestions.length) c.decision = { status: "skipped", auto: true };
    delete c.verdict;
  }
  return item;
}
const putItem = (env, item) => env.QUEUE.put(`item:${item.id}`, JSON.stringify(item), { expirationTtl: TTL });

async function allItems(env) {
  const out = [];
  let cursor;
  do {
    const page = await env.QUEUE.list({ prefix: "item:", cursor });
    for (const k of page.keys) {
      const item = await getItem(env, k.name.slice(5));
      if (item) out.push(item);
    }
    cursor = page.list_complete ? undefined : page.cursor;
  } while (cursor);
  return out.sort((a, b) => a.created.localeCompare(b.created));
}

function finish(item) {
  if (item.verdict && item.verdict.candidates.every((c) => c.decision && FINAL.has(c.decision.status))) {
    item.status = "done";
  }
}

async function refreshVerdictMessage(env, item) {
  await tg(env, "editMessageText", {
    chat_id: item.chat_id,
    message_id: item.verdict_message_id,
    text: verdictText(item),
    reply_markup: keyboard(item),
  });
}

// ------------------------------------------------------------------ Telegram webhook

async function telegramWebhook(req, env) {
  if (req.headers.get("x-telegram-bot-api-secret-token") !== env.WEBHOOK_SECRET) {
    return new Response("forbidden", { status: 403 });
  }
  const update = await req.json();
  if (update.message && isOwner(env, update.message.from)) await onMessage(env, update.message);
  if (update.callback_query && isOwner(env, update.callback_query.from)) await onButton(env, update.callback_query);
  return new Response("ok"); // anyone else is ignored silently
}

async function onMessage(env, msg) {
  const reply = (text) => tg(env, "sendMessage", { chat_id: msg.chat.id, text, reply_to_message_id: msg.message_id });
  const text = msg.text || msg.caption || "";

  if (/^\/(start|help)\b/.test(text)) {
    return reply(
      "把域名的文字或截图发给我。Claude 会判断每个域名适合加到哪个列表：" +
        "Rules/Reject（广告 / 跟踪 / 遥测），或者 AI / Bank / Broker / Crypto 里的某一家（例如 AI/OpenAI）。" +
        "你点按钮选定后才会写入：Reject 立即提交；分类厂商由 Claude 改配置、重新生成规则后推送到 main。" +
        `通知 Claude 失败的消息会在兜底时间处理：${env.JUDGE_SCHEDULE || "按计划"}。\n\n/pending 查看还在排队的条数`,
    );
  }
  if (/^\/pending\b/.test(text)) {
    const n = (await pending(env)).length;
    const a = (await approved(env)).length;
    if (!n && !a) return reply("没有排队中的消息。");
    return reply(`等 Claude 判断：${n} 条；已确认、等 Claude 写入分类：${a} 条。`);
  }

  const photoId = msg.photo
    ? msg.photo[msg.photo.length - 1].file_id
    : msg.document && /^image\//.test(msg.document.mime_type || "")
      ? msg.document.file_id
      : null;
  if (!text.trim() && !photoId) return reply("只支持文字或图片。");

  const id = Date.now().toString(36) + Math.random().toString(36).slice(2, 5);
  await putItem(env, {
    id,
    status: "pending",
    created: new Date().toISOString(),
    chat_id: msg.chat.id,
    message_id: msg.message_id,
    text,
    photo_file_id: photoId,
  });
  const fired = await maybeFire(env);
  return reply(
    fired === "failed" || fired === "unconfigured"
      ? `已收到（编号 ${id}）。没能立即通知 Claude，会在兜底时间处理：${env.JUDGE_SCHEDULE || "按计划"}。`
      : `已收到（编号 ${id}），已通知 Claude 判断，通常几分钟内回复。`,
  );
}

// callback_data: p:<id>:<i>:<j> pick suggestion j for candidate i · s:<id>:<i> skip one
//                F:<id> pick every open candidate's first suggestion · S:<id> skip all
async function onButton(env, cq) {
  const [op, id, a, b] = (cq.data || "").split(":");
  const item = await getItem(env, id);
  const answer = (text) => tg(env, "answerCallbackQuery", { callback_query_id: cq.id, text });
  if (!item || !item.verdict) return answer("这条记录已过期或不存在。");

  const cands = item.verdict.candidates;
  const open = (c) => !c.decision;
  let picks = []; // [candidate, target]
  if (op === "p") {
    const c = cands[Number(a)];
    const s = c && c.suggestions[Number(b)];
    if (c && s && open(c)) picks = [[c, s.target]];
  } else if (op === "F") {
    // only confirmed first choices; suspected ones always need their own tap
    picks = cands
      .filter((c) => open(c) && c.suggestions.length && !c.suggestions[0].suspected)
      .map((c) => [c, c.suggestions[0].target]);
  } else if (op === "s" || op === "S") {
    const skip = op === "s" ? [cands[Number(a)]].filter((c) => c && open(c)) : cands.filter(open);
    if (!skip.length) return answer("没有需要处理的条目。");
    for (const c of skip) c.decision = { status: "skipped" };
    finish(item);
    await putItem(env, item);
    await refreshVerdictMessage(env, item);
    return answer("已跳过");
  }
  if (!picks.length) return answer("没有需要处理的条目。");

  const notes = [];
  const toReject = picks.filter(([, t]) => t === "Reject").map(([c]) => c);
  if (toReject.length) {
    const entries = toReject.map((c) => ({
      type: c.type,
      value: c.value,
      reason: c.reason,
      added: new Date().toISOString().slice(0, 10),
      source: `telegram:${item.id}`,
    }));
    const res = await commitEntries(env, entries);
    const addedRules = new Set(res.added.map(ruleOf));
    for (const c of toReject) {
      c.decision = addedRules.has(ruleOf(c))
        ? { target: "Reject", status: "added", commit: res.commit }
        : { target: "Reject", status: "existing" };
    }
    notes.push(res.added.length ? `Reject +${res.added.length}` : "Reject 里都已存在");
  }
  const toCategory = picks.filter(([, t]) => t !== "Reject");
  for (const [c, target] of toCategory) c.decision = { target, status: "approved", at: new Date().toISOString() };
  finish(item);
  await putItem(env, item);
  if (toCategory.length) {
    const fired = await maybeFire(env);
    notes.push(
      fired === "failed" || fired === "unconfigured"
        ? `分类 ${toCategory.length} 条已记下，兜底时间写入`
        : `分类 ${toCategory.length} 条交给 Claude 写入`,
    );
  }
  await refreshVerdictMessage(env, item);
  return answer(notes.join("；"));
}

// Start the "Reject 待办判断" routine through its API trigger. Requests that arrive while a
// fired run has not started reading the queues yet ride along with it instead of firing again
// (each routine allows 30 fires an hour); once that run has read them, fire a new one.
const FIRE_WINDOW_MS = 10 * 60 * 1000;

async function maybeFire(env) {
  if (!env.CLAUDE_ROUTINE_ID || !env.CLAUDE_ROUTINE_TOKEN) return "unconfigured";
  const now = Date.now();
  const lastFire = Number((await env.QUEUE.get("state:last_fire")) || 0);
  const read = (await env.QUEUE.get("state:fire_read")) !== "0";
  if (now - lastFire < FIRE_WINDOW_MS && !read) return "batched";
  const r = await fetch(`https://api.anthropic.com/v1/claude_code/routines/${env.CLAUDE_ROUTINE_ID}/fire`, {
    method: "POST",
    headers: {
      authorization: `Bearer ${env.CLAUDE_ROUTINE_TOKEN}`,
      "anthropic-beta": "experimental-cc-routine-2026-04-01",
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
    },
    body: "{}",
  });
  if (!r.ok) {
    console.error(`routine fire failed: ${r.status} ${await r.text()}`);
    return "failed";
  }
  await env.QUEUE.put("state:last_fire", String(now));
  await env.QUEUE.put("state:fire_read", "0");
  return "fired";
}

// ------------------------------------------------------------------ routine API

async function pending(env) {
  return (await allItems(env))
    .filter((i) => i.status === "pending")
    .map((i) => ({ id: i.id, created: i.created, text: i.text, has_photo: Boolean(i.photo_file_id) }));
}

async function approved(env) {
  const out = [];
  for (const item of await allItems(env)) {
    if (!item.verdict) continue;
    item.verdict.candidates.forEach((c, index) => {
      if (c.decision && c.decision.status === "approved") {
        const [category, entry] = c.decision.target.split("/");
        out.push({ item_id: item.id, index, type: c.type, value: c.value, category, entry, reason: c.reason });
      }
    });
  }
  return out;
}

async function photo(env, id) {
  const item = await getItem(env, id);
  if (!item || !item.photo_file_id) return json({ error: "no photo" }, 404);
  const file = await tg(env, "getFile", { file_id: item.photo_file_id });
  const r = await fetch(`https://api.telegram.org/file/bot${env.TELEGRAM_TOKEN}/${file.file_path}`);
  const type = /\.png$/i.test(file.file_path) ? "image/png" : "image/jpeg";
  return new Response(r.body, { status: r.status, headers: { "content-type": type } });
}

// body: {summary, candidates: [{type, value, reason, suggestions: [{target, note, suspected}]}]}
// target is "Reject" or "<Category>/<Entry>" (AI/OpenAI, Bank/HSBC, ...). suspected: true marks
// a plausible but unproven suggestion; it is offered with a 疑似 label and left out of
// "全部按首选", so you decide. Confirmed suggestions are listed first. No suggestions means
// "does not belong in any list".
async function verdict(env, id, body) {
  const item = await getItem(env, id);
  if (!item) return { error: "unknown item" };
  if (item.status !== "pending") return { error: `item is ${item.status}` };
  const seen = new Set();
  const candidates = [];
  for (const c of body.candidates || []) {
    const clean = cleanCandidate(c.type, c.value);
    if (!clean || seen.has(ruleOf(clean))) continue;
    seen.add(ruleOf(clean));
    const targets = new Set();
    const suggestions = [];
    for (const s of c.suggestions || []) {
      const target = String((s && s.target) || "").trim();
      if (!TARGET_RE.test(target) || targets.has(target) || suggestions.length >= MAX_SUGGESTIONS) continue;
      targets.add(target);
      suggestions.push({ target, note: String(s.note || "").slice(0, 120), suspected: s.suspected === true });
    }
    suggestions.sort((x, y) => Number(x.suspected) - Number(y.suspected)); // stable: confirmed first
    candidates.push({ ...clean, reason: String(c.reason || "").slice(0, 300), suggestions });
  }
  for (const c of candidates) if (!c.suggestions.length) c.decision = { status: "skipped", auto: true };
  item.verdict = { summary: String(body.summary || "").slice(0, 800), candidates, at: new Date().toISOString() };
  item.status = "judged";
  finish(item);
  const sent = await tg(env, "sendMessage", {
    chat_id: item.chat_id,
    reply_to_message_id: item.message_id,
    text: verdictText(item),
    reply_markup: keyboard(item),
  });
  item.verdict_message_id = sent.message_id;
  await putItem(env, item);
  return { ok: true, candidates: candidates.length };
}

// body: {ok: bool, commit?: sha, note?: string}
async function applied(env, id, index, body) {
  const item = await getItem(env, id);
  const c = item && item.verdict && item.verdict.candidates[index];
  if (!c || !c.decision || c.decision.status !== "approved") return { error: "not waiting to be applied" };
  c.decision = {
    target: c.decision.target,
    status: body.ok ? "applied" : "failed",
    commit: body.commit ? String(body.commit).slice(0, 40) : undefined,
    note: String(body.note || "").slice(0, 200),
  };
  finish(item);
  await putItem(env, item);
  await refreshVerdictMessage(env, item);
  return { ok: true };
}

async function setup(env, origin) {
  await tg(env, "setWebhook", {
    url: `${origin}/telegram`,
    secret_token: env.WEBHOOK_SECRET,
    allowed_updates: ["message", "callback_query"],
  });
  await tg(env, "setMyCommands", {
    commands: [
      { command: "pending", description: "查看排队中的消息" },
      { command: "help", description: "使用说明" },
    ],
  });
  return { ok: true, webhook: `${origin}/telegram` };
}

// ------------------------------------------------------------------ rendering

function verdictText(item) {
  const v = item.verdict;
  const lines = [`判断结果（编号 ${item.id}）`];
  if (v.summary) lines.push(v.summary);
  if (!v.candidates.length) lines.push("", "没有找到域名。");
  v.candidates.forEach((c, i) => {
    lines.push("", `${i + 1}. ${c.type},${c.value}`);
    if (c.reason) lines.push(`   ${c.reason}`);
    if (!c.suggestions.length) lines.push("   建议：不加入任何列表");
    c.suggestions.forEach((s, j) => {
      const label = s.suspected ? "疑似（未证实，由你决定）" : j === 0 ? "建议" : "也可";
      lines.push(`   ${label}：${s.target}${s.note ? `（${s.note}）` : ""}`);
    });
    if (c.decision && !c.decision.auto) lines.push(`   ${STATUS_TEXT[c.decision.status](c.decision)}`);
  });
  return lines.join("\n").slice(0, 4000);
}

function keyboard(item) {
  const rows = [];
  const open = item.verdict.candidates.map((c, i) => [c, i]).filter(([c]) => !c.decision);
  for (const [c, i] of open.slice(0, 30)) {
    rows.push([
      ...c.suggestions.map((s, j) => ({
        text: `${i + 1} → ${s.target}${s.suspected ? "（疑似）" : ""}`,
        callback_data: `p:${item.id}:${i}:${j}`,
      })),
      { text: `跳过 ${i + 1}`, callback_data: `s:${item.id}:${i}` },
    ]);
  }
  if (open.length > 1) {
    const row = [];
    if (open.some(([c]) => c.suggestions.length && !c.suggestions[0].suspected)) {
      row.push({ text: "全部按首选（不含疑似）", callback_data: `F:${item.id}` });
    }
    row.push({ text: "全部跳过", callback_data: `S:${item.id}` });
    rows.push(row);
  }
  return { inline_keyboard: rows };
}

// ------------------------------------------------------------------ GitHub

async function gh(env, path, init = {}) {
  const r = await fetch(`https://api.github.com/repos/${env.GITHUB_REPO}${path}`, {
    ...init,
    headers: {
      authorization: `Bearer ${env.GITHUB_TOKEN}`,
      accept: "application/vnd.github+json",
      "x-github-api-version": "2022-11-28",
      "user-agent": "reject-bot",
      ...(init.body ? { "content-type": "application/json" } : {}),
    },
  });
  const data = r.status === 204 ? null : await r.json();
  return { status: r.status, data };
}

function decodeBase64(b64) {
  const bin = atob(b64.replace(/\n/g, ""));
  return new TextDecoder().decode(Uint8Array.from(bin, (ch) => ch.charCodeAt(0)));
}

/** One commit on the branch with manual.json and the three Reject files; retries on a moved ref. */
async function commitEntries(env, entries) {
  const branch = env.GITHUB_BRANCH || "main";
  for (let attempt = 0; attempt < 4; attempt++) {
    const ref = await gh(env, `/git/ref/heads/${branch}`);
    if (ref.status !== 200) throw new Error(`github ref: ${ref.status}`);
    const head = ref.data.object.sha;
    const commit = await gh(env, `/git/commits/${head}`);

    const files = {};
    for (const path of [MANUAL_PATH, ...REJECT_FILES.map((f) => f.path)]) {
      const r = await gh(env, `/contents/${path}?ref=${head}`);
      if (r.status !== 200) throw new Error(`github read ${path}: ${r.status}`);
      files[path] = decodeBase64(r.data.content);
    }
    const res = applyEntries(files, entries);
    if (!res.added.length) return { ...res, commit: null };

    const tree = await gh(env, "/git/trees", {
      method: "POST",
      body: JSON.stringify({
        base_tree: commit.data.tree.sha,
        tree: Object.entries(res.files).map(([path, content]) => ({ path, mode: "100644", type: "blob", content })),
      }),
    });
    const n = res.added.length;
    const message =
      `Reject: add ${n} manual ${n === 1 ? "entry" : "entries"}\n\n` +
      res.added.map((e) => `- ${e.type},${e.value}: ${e.reason || ""}`.trimEnd()).join("\n") +
      "\n\nConfirmed via the Telegram reject bot; judged by the Reject 待办判断 routine.";
    const created = await gh(env, "/git/commits", {
      method: "POST",
      body: JSON.stringify({ message, tree: tree.data.sha, parents: [head] }),
    });
    const moved = await gh(env, `/git/refs/heads/${branch}`, {
      method: "PATCH",
      body: JSON.stringify({ sha: created.data.sha, force: false }),
    });
    if (moved.status === 200) return { ...res, commit: created.data.sha };
    if (moved.status !== 422) throw new Error(`github update ref: ${moved.status}`);
    // 422: the branch moved (e.g. a merged PR) between read and write; start over.
  }
  throw new Error("github: branch kept moving, gave up");
}
