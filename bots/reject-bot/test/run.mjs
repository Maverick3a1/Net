// End-to-end test with Telegram, GitHub and KV mocked: message -> pending -> verdict ->
// "add" button -> one commit. Then checks the committed files against reject.py's own
// rendering of the same manual.json. Run: node bots/reject-bot/test/run.mjs
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { cpSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import worker from "../src/worker.js";
import { MANUAL_PATH, REJECT_FILES, replaceManual, manualRules } from "../src/manual.js";

const REPO = join(dirname(fileURLToPath(import.meta.url)), "../../..");
const OWNER = 4242;

// ---- mocks
const kv = new Map();
const QUEUE = {
  get: async (k) => kv.get(k) ?? null,
  put: async (k, v) => void kv.set(k, v),
  list: async ({ prefix }) => ({ keys: [...kv.keys()].filter((k) => k.startsWith(prefix)).map((name) => ({ name })), list_complete: true }),
};
const repo = {};
for (const p of [MANUAL_PATH, ...REJECT_FILES.map((f) => f.path)]) repo[p] = readFileSync(join(REPO, p), "utf8");
let head = "c0";
const commits = [];
const sent = [];
let msgId = 100;
const fires = [];
let fireStatus = 200;

globalThis.fetch = async (url, init = {}) => {
  url = String(url);
  const body = init.body ? JSON.parse(init.body) : null;
  const ok = (result) => new Response(JSON.stringify({ ok: true, result }));
  if (url.startsWith("https://api.anthropic.com/")) {
    fires.push({ url, headers: init.headers });
    return new Response(JSON.stringify({ type: "routine_fire" }), { status: fireStatus });
  }
  if (url.startsWith("https://api.telegram.org/")) {
    const method = url.split("/").pop();
    sent.push({ method, body });
    if (method === "sendMessage") return ok({ message_id: ++msgId });
    return ok(true);
  }
  const m = url.match(/^https:\/\/api\.github\.com\/repos\/[^/]+\/[^/]+(\/.*)$/);
  assert(m, `unexpected fetch ${url}`);
  const path = m[1];
  const res = (data, status = 200) => new Response(JSON.stringify(data), { status });
  if (path === "/git/ref/heads/main") return res({ object: { sha: head } });
  if (path.startsWith("/git/commits/")) return res({ tree: { sha: "t-" + head } });
  if (path.startsWith("/contents/")) {
    const p = decodeURIComponent(path.slice(10).split("?")[0]);
    return res({ content: Buffer.from(repo[p]).toString("base64") });
  }
  if (path === "/git/trees") return res({ sha: "tree1", _files: body.tree });
  if (path === "/git/commits") {
    commits.push(body);
    return res({ sha: "c" + commits.length, _tree: body.tree });
  }
  if (path === "/git/refs/heads/main") {
    head = body.sha;
    return res({});
  }
  throw new Error("unhandled " + path);
};
// capture tree contents (the mock trees endpoint does not store them)
const realFetch = globalThis.fetch;
globalThis.fetch = async (url, init = {}) => {
  if (String(url).endsWith("/git/trees")) for (const t of JSON.parse(init.body).tree) repo[t.path] = t.content;
  return realFetch(url, init);
};

const env = {
  QUEUE,
  TELEGRAM_TOKEN: "tg",
  TELEGRAM_USER_ID: String(OWNER),
  WEBHOOK_SECRET: "hook",
  ROUTINE_TOKEN: "rt",
  GITHUB_TOKEN: "gh",
  GITHUB_REPO: "Maverick3a1/Net",
  GITHUB_BRANCH: "main",
  JUDGE_SCHEDULE: "每天 23:00",
  CLAUDE_ROUTINE_ID: "trig_test",
  CLAUDE_ROUTINE_TOKEN: "sk-test",
};
const call = (method, path, body, headers = {}) =>
  worker.fetch(new Request("https://bot.example" + path, { method, headers, body: body && JSON.stringify(body) }), env);
const hook = (update) => call("POST", "/telegram", update, { "x-telegram-bot-api-secret-token": "hook" });
const api = (method, path, body) => call(method, path, body, { authorization: "Bearer rt" });

// ---- auth
assert.equal((await call("POST", "/telegram", {}, {})).status, 403);
assert.equal((await call("GET", "/api/pending")).status, 401);
await hook({ message: { message_id: 1, chat: { id: 9 }, from: { id: 1 }, text: "stranger.example.com" } });
assert.equal((await (await api("GET", "/api/pending")).json()).length, 0, "strangers are ignored");

assert.equal(fires.length, 0, "strangers do not fire the routine");

// ---- message -> fire -> pending
const lastReply = () => sent.filter((s) => s.method === "sendMessage").at(-1).body.text;
await hook({ message: { message_id: 2, chat: { id: 9 }, from: { id: OWNER }, text: "ads.example-track.com 和 t.example.net" } });
assert.equal(fires.length, 1);
assert.equal(fires[0].url, "https://api.anthropic.com/v1/claude_code/routines/trig_test/fire");
assert.equal(fires[0].headers.authorization, "Bearer sk-test");
assert.equal(fires[0].headers["anthropic-beta"], "experimental-cc-routine-2026-04-01");
assert.match(lastReply(), /已通知 Claude/);
// a second message before the run reads the queue rides along with it
await hook({ message: { message_id: 3, chat: { id: 9 }, from: { id: OWNER }, text: "second.example.org" } });
assert.equal(fires.length, 1, "batched into the pending run");
const queue = await (await api("GET", "/api/pending")).json();
assert.equal(queue.length, 2);
const id = queue[0].id;
const id2 = queue[1].id;
// once the run has read the queue, a new message fires a new run; a failed fire falls back
fireStatus = 429;
await hook({ message: { message_id: 4, chat: { id: 9 }, from: { id: OWNER }, text: "third.example.org" } });
assert.equal(fires.length, 2);
assert.match(lastReply(), /兜底时间处理：每天 23:00/);
fireStatus = 200;
await hook({ message: { message_id: 5, chat: { id: 9 }, from: { id: OWNER }, text: "fourth.example.org" } });
assert.equal(fires.length, 3, "a failed fire does not block the next one");

// ---- verdict: per-domain suggestions; bad values and bad targets are dropped
const v = await (
  await api("POST", `/api/verdict/${id}`, {
    summary: "四个域名",
    candidates: [
      { type: "DOMAIN-SUFFIX", value: "Example-Track.com", reason: "跟踪", suggestions: [{ target: "Reject", note: "埋点" }] },
      {
        type: "DOMAIN",
        value: "t.example.net",
        reason: "OpenAI 的 API 主机",
        suggestions: [{ target: "AI/OpenAI", note: "证书 O=OpenAI" }, { target: "Personal/Direct" }, { target: "Reject" }],
      },
      { type: "DOMAIN-SUFFIX", value: "appsflyersdk.com", reason: "已在 Bank 段", suggestions: [{ target: "Reject" }] },
      { type: "DOMAIN", value: "nothing.example.org", reason: "普通网站", suggestions: [] },
      { type: "DOMAIN", value: "not a domain", reason: "x", suggestions: [{ target: "Reject" }] },
    ],
  })
).json();
assert.deepEqual(v, { ok: true, candidates: 4 });
let item = JSON.parse(kv.get(`item:${id}`));
assert.deepEqual(item.verdict.candidates[1].suggestions.map((x) => x.target), ["AI/OpenAI", "Reject"]);
assert.equal(item.verdict.candidates[3].decision.status, "skipped", "no suggestion -> nothing to pick");
const kb = sent.filter((x) => x.method === "sendMessage").at(-1).body.reply_markup.inline_keyboard;
assert(kb.every((row) => row.length === 1), "one button per row");
assert.deepEqual(kb.map((row) => row[0].text), [
  "1 → Reject", "跳过 1",
  "2 → AI/OpenAI", "2 → Reject", "跳过 2",
  "3 → Reject", "跳过 3",
  "全部按首选（不含疑似）", "全部跳过",
]);
assert.deepEqual((await (await api("GET", "/api/pending")).json()).map((q) => q.id).includes(id), false, "judged items leave the queue");
assert.equal((await (await api("POST", `/api/verdict/${id}`, { candidates: [] })).json()).error, "item is judged");

// ---- "all first choices": Reject ones commit at once (existing one reported); category ones are queued + fire
const firesBefore = fires.length;
await hook({ callback_query: { id: "q1", from: { id: OWNER }, data: `F:${id}` } });
assert.equal(commits.length, 1);
const manual = JSON.parse(repo[MANUAL_PATH]);
assert.deepEqual(manual.entries.map((e) => `${e.type},${e.value}`), ["DOMAIN-SUFFIX,example-track.com"]);
assert.match(repo[REJECT_FILES[0].path], /# Manual \/ Telegram\n.*\n# =+\nDOMAIN-SUFFIX,example-track\.com\n$/);
assert.equal(fires.length, firesBefore + 1, "category picks fire the routine");
const queued = await (await api("GET", "/api/approved")).json();
assert.deepEqual(queued.map((q) => [q.item_id, q.index, q.category, q.entry, q.value]), [[id, 1, "AI", "OpenAI", "t.example.net"]]);

// ---- the routine reports the category write back
assert.deepEqual(await (await api("POST", `/api/applied/${id}/1`, { ok: true, commit: "abc1234def", note: "已重新生成" })).json(), { ok: true });
assert.equal((await (await api("POST", `/api/applied/${id}/1`, { ok: true })).json()).error, "not waiting to be applied");
assert.equal((await (await api("GET", "/api/approved")).json()).length, 0);
item = JSON.parse(kv.get(`item:${id}`));
assert.deepEqual(item.verdict.candidates.map((c) => c.decision.status), ["added", "applied", "existing", "skipped"]);
assert.equal(item.status, "done");
const edited = sent.filter((x) => x.method === "editMessageText").at(-1).body.text;
assert.match(edited, /→ 已加入 AI\/OpenAI（abc1234）：已重新生成/);
assert.match(edited, /→ Reject 里已有/);

// ---- skipping a single domain
await api("POST", `/api/verdict/${id2}`, { candidates: [{ type: "DOMAIN", value: "second.example.org", suggestions: [{ target: "Crypto/Binance" }] }] });
await hook({ callback_query: { id: "q2", from: { id: OWNER }, data: `s:${id2}:0` } });
assert.equal(JSON.parse(kv.get(`item:${id2}`)).status, "done");
assert.equal(commits.length, 1, "skips never commit");

// ---- the Worker's files must equal what reject.py renders from the same manual.json
const tmp = mkdtempSync(join(tmpdir(), "rejectbot-"));
cpSync(join(REPO, "Rules/Reject"), join(tmp, "Rules/Reject"), { recursive: true });
writeFileSync(join(tmp, MANUAL_PATH), repo[MANUAL_PATH]);
execFileSync("python3", ["-I", join(tmp, "Rules/Reject/scripts/reject.py")], { stdio: "ignore" });
for (const f of REJECT_FILES) assert.equal(repo[f.path], readFileSync(join(tmp, f.path), "utf8"), f.path);

// ---- removing every manual rule restores the original files byte for byte
for (const f of REJECT_FILES) {
  const original = readFileSync(join(REPO, f.path), "utf8");
  assert.equal(replaceManual(repo[f.path], [], f.clash), original, f.path);
  assert.equal(replaceManual(original, manualRules(manual), f.clash).includes("Manual / Telegram"), true);
}

console.log(`ok: ${commits.length} commits, ${fires.length} fires, ${sent.length} Telegram calls`);

// ---- suspected suggestions: labeled, confirmed ones first, never picked by "全部按首选"
await hook({ message: { message_id: 20, chat: { id: 9 }, from: { id: OWNER }, text: "bochk01.etdsinfo.com" } });
const sid = (await (await api("GET", "/api/pending")).json()).at(-1).id;
await api("POST", `/api/verdict/${sid}`, {
  summary: "疑似中银香港",
  candidates: [
    { type: "DOMAIN", value: "bochk01.etdsinfo.com", reason: "名称疑似中银香港", suggestions: [{ target: "Bank/BOCHK", note: "证书无法获取", suspected: true }] },
    {
      type: "DOMAIN",
      value: "bochk02.etdsinfo.com",
      reason: "同上",
      suggestions: [{ target: "Bank/BOCHK", note: "未证实", suspected: true }, { target: "Reject", note: "埋点" }],
    },
  ],
});
const sItem = JSON.parse(kv.get(`item:${sid}`));
assert.deepEqual(sItem.verdict.candidates[1].suggestions.map((x) => [x.target, x.suspected]), [["Reject", false], ["Bank/BOCHK", true]]);
const sMsg = sent.filter((x) => x.method === "sendMessage").at(-1).body;
assert.match(sMsg.text, /疑似（未证实，由你决定）：Bank\/BOCHK（证书无法获取）/);
assert.deepEqual(sMsg.reply_markup.inline_keyboard.slice(0, 2).map((row) => row.map((b) => b.text)), [["1 → Bank/BOCHK（疑似）"], ["跳过 1"]]);
const commitsBefore = commits.length;
await hook({ callback_query: { id: "q9", from: { id: OWNER }, data: `F:${sid}` } });
let after = JSON.parse(kv.get(`item:${sid}`));
assert.equal(after.verdict.candidates[0].decision, undefined, "suspected first choice is left for you");
assert.equal(after.verdict.candidates[1].decision.target, "Reject");
assert.equal(commits.length, commitsBefore + 1);
await hook({ callback_query: { id: "q10", from: { id: OWNER }, data: `p:${sid}:0:0` } });
after = JSON.parse(kv.get(`item:${sid}`));
assert.deepEqual(after.verdict.candidates[0].decision.status, "approved");
assert.deepEqual((await (await api("GET", "/api/approved")).json()).map((q) => [q.entry, q.value]), [["BOCHK", "bochk01.etdsinfo.com"]]);
console.log("ok: suspected suggestions");

// ---- items stored by the first version still render and accept buttons
kv.set("item:old1", JSON.stringify({
  id: "old1", status: "judged", created: new Date().toISOString(), chat_id: 9, message_id: 7, verdict_message_id: 8,
  verdict: { summary: "", candidates: [
    { type: "DOMAIN", value: "old.example-ads.com", verdict: "reject", reason: "旧格式" },
    { type: "DOMAIN", value: "keep.example.com", verdict: "keep", reason: "旧格式" },
    { type: "DOMAIN", value: "done.example.com", verdict: "reject", reason: "旧格式", decision: "skipped" },
  ] },
}));
await hook({ callback_query: { id: "q3", from: { id: OWNER }, data: "p:old1:0:0" } });
const old = JSON.parse(kv.get("item:old1"));
assert.deepEqual(old.verdict.candidates.map((c) => c.decision.status), ["added", "skipped", "skipped"]);
assert.equal(old.status, "done");
console.log("ok: old items upgraded");
