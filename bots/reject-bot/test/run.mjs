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
await new Promise((r) => setTimeout(r, 5));
// once the run has read the queue, a new message fires a new run; a failed fire falls back
fireStatus = 429;
await hook({ message: { message_id: 4, chat: { id: 9 }, from: { id: OWNER }, text: "third.example.org" } });
assert.equal(fires.length, 2);
assert.match(lastReply(), /兜底时间处理：每天 23:00/);
fireStatus = 200;
await hook({ message: { message_id: 5, chat: { id: 9 }, from: { id: OWNER }, text: "fourth.example.org" } });
assert.equal(fires.length, 3, "a failed fire does not block the next one");

// ---- verdict (one duplicate of an existing Crypto rule, one invalid value dropped)
const v = await (
  await api("POST", `/api/verdict/${id}`, {
    summary: "两个域名",
    candidates: [
      { type: "DOMAIN-SUFFIX", value: "Example-Track.com", verdict: "reject", reason: "跟踪" },
      { type: "DOMAIN", value: "t.example.net", verdict: "unsure", reason: "可能是统计" },
      { type: "DOMAIN-SUFFIX", value: "appsflyersdk.com", verdict: "reject", reason: "已在 Bank 段" },
      { type: "DOMAIN", value: "not a domain", verdict: "reject", reason: "x" },
    ],
  })
).json();
assert.deepEqual(v, { ok: true, candidates: 3 });
assert.deepEqual((await (await api("GET", "/api/pending")).json()).map((q) => q.id).includes(id), false, "judged items leave the queue");
assert.equal((await (await api("POST", `/api/verdict/${id}`, { candidates: [] })).json()).error, "item is judged");

// ---- "add all suggested" -> one commit with the new rule; the existing one is reported
await hook({ callback_query: { id: "q1", from: { id: OWNER }, data: `A:${id}` } });
assert.equal(commits.length, 1);
const manual = JSON.parse(repo[MANUAL_PATH]);
assert.deepEqual(manual.entries.map((e) => `${e.type},${e.value}`), ["DOMAIN-SUFFIX,example-track.com"]);
assert.match(repo[REJECT_FILES[0].path], /# Manual \/ Telegram\n.*\n# =+\nDOMAIN-SUFFIX,example-track\.com\n$/);

// ---- add the remaining one by itself
await hook({ callback_query: { id: "q2", from: { id: OWNER }, data: `a:${id}:1` } });
assert.equal(commits.length, 2);
const item = JSON.parse(kv.get(`item:${id}`));
assert.deepEqual(item.verdict.candidates.map((c) => c.decision), ["added", "added", "existing"]);
assert.equal(item.status, "done");

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

void id2;
console.log(`ok: ${commits.length} commits, ${fires.length} fires, ${sent.length} Telegram calls`);
