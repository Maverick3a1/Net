// Telegram bot that queues domains (text or screenshots), fires the "Reject 待办判断" Claude
// routine through its API trigger, shows its verdicts with buttons, and commits confirmed
// ones to Rules/Reject.
//
// Routes
//   POST /telegram              Telegram webhook (checked with WEBHOOK_SECRET)
//   GET  /api/pending           queued items          (Bearer ROUTINE_TOKEN)
//   GET  /api/photo/:id         an item's screenshot  (Bearer ROUTINE_TOKEN)
//   POST /api/verdict/:id       the routine's verdict (Bearer ROUTINE_TOKEN)
//   POST /api/setup             register the webhook and commands (Bearer ROUTINE_TOKEN)

import { MANUAL_PATH, REJECT_FILES, applyEntries, cleanCandidate, ruleOf } from "./manual.js";

const TTL = 60 * 60 * 24 * 30; // queued items expire after 30 days
const VERDICT_ICON = { reject: "✅ 建议拒绝", unsure: "⚠️ 不确定", keep: "⛔ 不建议拒绝" };
const DECISION_TEXT = { added: "→ 已添加", skipped: "→ 已跳过", existing: "→ 已存在，未重复添加" };

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const path = url.pathname;
    try {
      if (req.method === "POST" && path === "/telegram") return await telegramWebhook(req, env);
      if (path.startsWith("/api/")) {
        if (!authorized(req, env)) return json({ error: "unauthorized" }, 401);
        if (req.method === "GET" && path === "/api/pending") {
          await env.QUEUE.put("state:last_poll", String(Date.now())); // a run has started reading
          return json(await pending(env));
        }
        let m = path.match(/^\/api\/photo\/([a-z0-9]+)$/);
        if (req.method === "GET" && m) return await photo(env, m[1]);
        m = path.match(/^\/api\/verdict\/([a-z0-9]+)$/);
        if (req.method === "POST" && m) return json(await verdict(env, m[1], await req.json()));
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
const getItem = async (env, id) => JSON.parse((await env.QUEUE.get(`item:${id}`)) || "null");
const putItem = (env, item) => env.QUEUE.put(`item:${item.id}`, JSON.stringify(item), { expirationTtl: TTL });

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
      "把域名的文字或截图发给我。我会马上通知 Claude 判断是不是广告 / 跟踪 / 遥测，" +
        "通常几分钟内把结论发给你；你点「添加」后才会写进 Rules/Reject。" +
        `通知失败的消息会在兜底时间处理：${env.JUDGE_SCHEDULE || "按计划"}。\n\n/pending 查看还在排队的条数`,
    );
  }
  if (/^\/pending\b/.test(text)) {
    const n = (await pending(env)).length;
    return reply(n ? `还有 ${n} 条在排队，Claude 正在处理或等兜底时间处理。` : "没有排队中的消息。");
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

// Start the "Reject 待办判断" routine through its API trigger. Messages that arrive while a
// fired run has not started reading the queue yet ride along with it instead of firing again
// (each routine allows 30 fires an hour); once that run has read the queue, fire a new one.
const FIRE_WINDOW_MS = 10 * 60 * 1000;

async function maybeFire(env) {
  if (!env.CLAUDE_ROUTINE_ID || !env.CLAUDE_ROUTINE_TOKEN) return "unconfigured";
  const now = Date.now();
  const lastFire = Number((await env.QUEUE.get("state:last_fire")) || 0);
  const lastPoll = Number((await env.QUEUE.get("state:last_poll")) || 0);
  if (now - lastFire < FIRE_WINDOW_MS && lastPoll < lastFire) return "batched";
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
  return "fired";
}

// callback_data: a:<id>:<i> add one · s:<id>:<i> skip one · A:<id> add all suggested · S:<id> skip all
async function onButton(env, cq) {
  const [op, id, idx] = (cq.data || "").split(":");
  const item = await getItem(env, id);
  const answer = (text) => tg(env, "answerCallbackQuery", { callback_query_id: cq.id, text });
  if (!item || !item.verdict) return answer("这条记录已过期或不存在。");

  const cands = item.verdict.candidates;
  const open = (c) => !c.decision;
  let picked = [];
  if (op === "a" || op === "s") picked = [cands[Number(idx)]].filter((c) => c && open(c));
  if (op === "A") picked = cands.filter((c) => open(c) && c.verdict === "reject");
  if (op === "S") picked = cands.filter(open);
  if (!picked.length) return answer("没有需要处理的条目。");

  let note = "已跳过";
  if (op === "a" || op === "A") {
    const entries = picked.map((c) => ({
      type: c.type,
      value: c.value,
      reason: c.reason,
      added: new Date().toISOString().slice(0, 10),
      source: `telegram:${item.id}`,
    }));
    const res = await commitEntries(env, entries);
    const addedRules = new Set(res.added.map(ruleOf));
    for (const c of picked) c.decision = addedRules.has(ruleOf(c)) ? "added" : "existing";
    note = res.added.length ? `已提交 ${res.added.length} 条到 main` : "都已存在，没有提交";
    if (res.commit) note += `（${res.commit.slice(0, 7)}）`;
  } else {
    for (const c of picked) c.decision = "skipped";
  }
  if (cands.every((c) => c.decision)) item.status = "done";
  await putItem(env, item);
  await tg(env, "editMessageText", {
    chat_id: item.chat_id,
    message_id: item.verdict_message_id,
    text: verdictText(item),
    reply_markup: keyboard(item),
  });
  return answer(note);
}

// ------------------------------------------------------------------ routine API

async function pending(env) {
  const out = [];
  let cursor;
  do {
    const page = await env.QUEUE.list({ prefix: "item:", cursor });
    for (const k of page.keys) {
      const item = await getItem(env, k.name.slice(5));
      if (item && item.status === "pending") {
        out.push({ id: item.id, created: item.created, text: item.text, has_photo: Boolean(item.photo_file_id) });
      }
    }
    cursor = page.list_complete ? undefined : page.cursor;
  } while (cursor);
  return out.sort((a, b) => a.created.localeCompare(b.created));
}

async function photo(env, id) {
  const item = await getItem(env, id);
  if (!item || !item.photo_file_id) return json({ error: "no photo" }, 404);
  const file = await tg(env, "getFile", { file_id: item.photo_file_id });
  const r = await fetch(`https://api.telegram.org/file/bot${env.TELEGRAM_TOKEN}/${file.file_path}`);
  const type = /\.png$/i.test(file.file_path) ? "image/png" : "image/jpeg";
  return new Response(r.body, { status: r.status, headers: { "content-type": type } });
}

// body: {summary, candidates: [{type, value, verdict: reject|unsure|keep, reason}]}
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
    const v = VERDICT_ICON[c.verdict] ? c.verdict : "unsure";
    candidates.push({ ...clean, verdict: v, reason: String(c.reason || "").slice(0, 300) });
  }
  item.verdict = { summary: String(body.summary || "").slice(0, 800), candidates, at: new Date().toISOString() };
  item.status = candidates.length ? "judged" : "done";
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
  if (!v.candidates.length) lines.push("", "没有找到可以加入拒绝列表的域名。");
  v.candidates.forEach((c, i) => {
    lines.push("", `${i + 1}. ${VERDICT_ICON[c.verdict]}  ${c.type},${c.value}`);
    if (c.reason) lines.push(`   ${c.reason}`);
    if (c.decision) lines.push(`   ${DECISION_TEXT[c.decision]}`);
  });
  return lines.join("\n").slice(0, 4000);
}

function keyboard(item) {
  const rows = [];
  const open = item.verdict.candidates.map((c, i) => [c, i]).filter(([c]) => !c.decision);
  for (const [c, i] of open.slice(0, 40)) {
    rows.push([
      { text: `添加 ${i + 1}${c.verdict === "keep" ? "（不建议）" : ""}`, callback_data: `a:${item.id}:${i}` },
      { text: `跳过 ${i + 1}`, callback_data: `s:${item.id}:${i}` },
    ]);
  }
  if (open.length > 1) {
    const row = [];
    if (open.some(([c]) => c.verdict === "reject")) row.push({ text: "添加全部 ✅", callback_data: `A:${item.id}` });
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
