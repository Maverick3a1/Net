// Pure helpers shared by the Worker and its tests. They must render the Manual section
// exactly like Rules/Reject/scripts/reject.py does, so either side can rewrite it.

export const MANUAL_PATH = "Rules/Reject/config/manual.json";
export const REJECT_FILES = [
  { path: "Rules/Reject/Surge/Reject.list", clash: false },
  { path: "Rules/Reject/Shadowrocket/Reject.list", clash: false },
  { path: "Rules/Reject/Clash/Reject.yaml", clash: true },
];
export const TYPES = ["DOMAIN-SUFFIX", "DOMAIN", "DOMAIN-KEYWORD"];

const BANNER = "# " + "=".repeat(60);
const TITLE = "# Manual / Telegram";
const DESC = "# Added by hand after confirmation (Rules/Reject/config/manual.json)";
const DOMAIN_RE = /^(?=.{1,253}$)([a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z][a-z0-9-]{0,61}[a-z0-9]$/;
const KEYWORD_RE = /^[a-z0-9.-]{3,}$/;

/** Normalised {type, value} or null when it is not a rule we accept. */
export function cleanCandidate(type, value) {
  type = String(type || "").trim().toUpperCase();
  value = String(value || "").trim().toLowerCase().replace(/^\*?\./, "").replace(/\.$/, "");
  if (!TYPES.includes(type)) return null;
  if (type === "DOMAIN-KEYWORD" ? !KEYWORD_RE.test(value) : !DOMAIN_RE.test(value)) return null;
  return { type, value };
}

export const ruleOf = (e) => `${e.type},${e.value.trim().toLowerCase()}`;

/** Unique rules from manual.json entries, in file order (mirrors reject.manual_rules). */
export function manualRules(manual) {
  const out = [];
  for (const e of manual.entries) {
    const r = ruleOf(e);
    if (!out.includes(r)) out.push(r);
  }
  return out;
}

/** Replace (or add, or drop) the Manual section at the end of one Reject file. */
export function replaceManual(text, rules, clash) {
  const ind = clash ? "  " : "";
  const lines = text.replace(/\n$/, "").split("\n");
  const t = lines.indexOf(ind + TITLE);
  let keep = lines;
  if (t !== -1) {
    let start = t - 1; // the banner above the title
    if (start > 0 && lines[start - 1] === "") start -= 1;
    keep = lines.slice(0, start);
  }
  while (keep.length && keep[keep.length - 1] === "") keep.pop();
  if (rules.length) {
    const last = keep[keep.length - 1];
    const hasSections = last !== undefined && last !== "payload:" && !/^# (NAME|DESC|FORMAT|SOURCE): /.test(last);
    if (hasSections) keep.push("");
    keep.push(ind + BANNER, ind + TITLE, ind + DESC, ind + BANNER);
    for (const r of rules) keep.push(clash ? `  - '${r}'` : r);
  }
  return keep.join("\n") + "\n";
}

/** All rule lines in a Reject file (Surge syntax), for "already covered" checks. */
export function rulesIn(text) {
  const out = new Set();
  for (let l of text.split("\n")) {
    l = l.trim();
    if (l.startsWith("- ")) l = l.slice(2).trim().replace(/^'(.*)'$/, "$1");
    if (l && !l.startsWith("#") && l !== "payload:") out.add(l.toLowerCase());
  }
  return out;
}

/** True when `rule` is already in `covered`, or its domain sits under a DOMAIN-SUFFIX there. */
export function isCovered(covered, e) {
  if (covered.has(ruleOf(e).toLowerCase())) return true;
  if (e.type === "DOMAIN-KEYWORD") return false;
  const labels = e.value.split(".");
  for (let i = 0; i < labels.length - 1; i++) {
    if (covered.has("domain-suffix," + labels.slice(i).join("."))) return true;
  }
  return false;
}

/**
 * Apply new entries to the current files.
 * files: {path: text}. Returns {files: {path: newText}, added: [entry], existing: [entry]}.
 */
export function applyEntries(files, entries) {
  const manual = JSON.parse(files[MANUAL_PATH]);
  const covered = rulesIn(files[REJECT_FILES[0].path]);
  const added = [];
  const existing = [];
  for (const e of entries) {
    const r = ruleOf(e);
    if (isCovered(covered, e) || manual.entries.some((m) => ruleOf(m) === r)) existing.push(e);
    else {
      manual.entries.push(e);
      covered.add(r.toLowerCase());
      added.push(e);
    }
  }
  const out = {};
  if (added.length) {
    out[MANUAL_PATH] = JSON.stringify(manual, null, 2) + "\n";
    const rules = manualRules(manual);
    for (const f of REJECT_FILES) out[f.path] = replaceManual(files[f.path], rules, f.clash);
  }
  return { files: out, added, existing };
}
