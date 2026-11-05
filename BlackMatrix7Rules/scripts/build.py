#!/usr/bin/env python3
"""Generate Surge / Shadowrocket / Clash rule sets the way blackmatrix7/ios_rule_script does.

This does not copy blackmatrix7's generated files. It reads config/rulesets.json (each rule
set's upstream sources, the sub-rule sets it includes and the rule sets it excludes, taken
from blackmatrix7's READMEs), downloads every upstream source itself and applies the same
processing its READMEs describe:

  remove duplicates · DOMAIN merged into DOMAIN-SUFFIX · DOMAIN-SUFFIX merged into a parent
  suffix · DOMAIN merged into DOMAIN-KEYWORD · IP-CIDR(6) collapsed · MITM hostnames
  derived from URL-REGEX and merged

Which merges apply comes from each rule set's README badges (config "merge"). Known gaps:
it does not remove domains that fail to resolve (blackmatrix7 does; that needs hundreds of
thousands of DNS lookups a day), it does not rewrite URL-REGEX patterns, and blackmatrix7's
closed generator drops some upstream DOMAIN-KEYWORD rules by criteria it does not publish.

Output: BlackMatrix7Rules/<Name>/<Surge|Shadowrocket|Clash>/<files>, same file variants as
blackmatrix7. config/overrides.json adds or removes rules by hand (the Telegram bot's
"编辑广告"). Python 3.9+ standard library only.
"""

import concurrent.futures
import datetime
import ipaddress
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config" / "rulesets.json"
OVERRIDES = ROOT / "config" / "overrides.json"
README = ROOT / "README.md"
REPO = "https://github.com/Maverick3a1/Net"
RAW = "https://raw.githubusercontent.com/Maverick3a1/Net/main/BlackMatrix7Rules"
USER_AGENT = "Net-BlackMatrix7Rules/1.0 (+https://github.com/Maverick3a1/Net)"
MIN_KEEP_RATIO = 0.5  # a rule set may not shrink below half its previous size in one run
WORKERS = 24

TYPE_ORDER = [
    "DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "DOMAIN-WILDCARD", "IP-CIDR", "IP-CIDR6", "IP-ASN",
    "GEOIP", "PROCESS-NAME", "DEST-PORT", "USER-AGENT", "URL-REGEX", "AND", "OR", "NOT",
]
ALIASES = {
    "HOST": "DOMAIN", "HOST-SUFFIX": "DOMAIN-SUFFIX", "HOST-KEYWORD": "DOMAIN-KEYWORD",
    "HOST-WILDCARD": "DOMAIN-WILDCARD", "IP6-CIDR": "IP-CIDR6", "DST-PORT": "DEST-PORT",
}
LOGICAL = {"AND", "OR", "NOT"}
FREE_TEXT = {"URL-REGEX", "USER-AGENT"}
POLICIES = {
    "reject", "reject-tinygif", "reject-img", "reject-dict", "reject-array", "reject-200",
    "reject-drop", "reject-no-drop", "reject-video", "direct", "proxy", "block",
}
DOMAIN_RE = re.compile(r"^(?=.{1,253}$)[a-z0-9_]([a-z0-9_-]*[a-z0-9_])?(\.[a-z0-9_]([a-z0-9_-]*[a-z0-9_])?)+$")
HOSTS_RE = re.compile(r"^(?:0\.0\.0\.0|127\.0\.0\.1|::1?|::)\s+(\S+)")
SKIP_HOSTS = {"localhost", "localhost.localdomain", "local", "broadcasthost", "ip6-localhost", "0.0.0.0"}

# Rule types each platform keeps (blackmatrix7 drops URL-REGEX and logical rules for Clash and
# logical rules for Shadowrocket, and writes IPv6 ranges as IP-CIDR for Shadowrocket).
PLATFORM_TYPES = {
    "Surge": set(TYPE_ORDER),
    "Shadowrocket": set(TYPE_ORDER) - LOGICAL,
    "Clash": {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "IP-CIDR", "IP-CIDR6", "IP-ASN", "GEOIP",
              "PROCESS-NAME", "DEST-PORT"},
}
IP_TYPES = {"IP-CIDR", "IP-CIDR6", "IP-ASN", "GEOIP"}


def log(msg):
    print(msg, flush=True)


def warn(msg):
    print(f"::warning::{msg}", flush=True)


# ------------------------------------------------------------------ fetching


def fetch(url):
    last = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"{url}: {last}")


V2FLY_RAW = "https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/{}"


def fetch_v2fly(name, seen=None):
    """A v2fly domain-list-community list as Surge rule lines, following include: lines.

    Plain / domain: lines are suffixes, full: is an exact host, keyword: a keyword; regexp: is
    skipped (not portable). Attributes (@cn, @ads ...) are ignored: the whole list is used."""
    seen = seen if seen is not None else set()
    if name in seen:
        return []
    seen.add(name)
    out = []
    for raw in fetch(V2FLY_RAW.format(name)).splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        value = line.split()[0]
        kind, _, rest = value.partition(":")
        if not rest:
            kind, rest = "domain", value
        if kind == "include":
            out += fetch_v2fly(rest, seen)
        elif kind == "domain":
            out.append(f"DOMAIN-SUFFIX,{rest}")
        elif kind == "full":
            out.append(f"DOMAIN,{rest}")
        elif kind == "keyword":
            out.append(f"DOMAIN-KEYWORD,{rest}")
    return out


def fetch_source(url):
    """A source is a URL, or "v2fly:<list>" for a v2fly domain-list-community list."""
    if url.startswith("v2fly:"):
        return "\n".join(fetch_v2fly(url[6:]))
    return fetch(url)


def fetch_all(urls):
    texts, failed = {}, []
    with concurrent.futures.ThreadPoolExecutor(WORKERS) as pool:
        futures = {pool.submit(fetch_source, u): u for u in urls}
        for f in concurrent.futures.as_completed(futures):
            u = futures[f]
            try:
                texts[u] = f.result()
            except Exception as exc:  # noqa: BLE001
                failed.append(u)
                warn(f"source failed, skipped this run: {exc}")
    return texts, failed


# ------------------------------------------------------------------ parsing


def norm_domain(value):
    v = value.strip().strip("'\"").lower().rstrip(".")
    if v.startswith("*."):
        v = v[2:]
    return v if DOMAIN_RE.match(v) else None


def as_net(value):
    try:
        return ipaddress.ip_network(value.strip().strip("'\""), strict=False)
    except ValueError:
        return None


def ip_rule(net):
    return ("IP-CIDR6" if net.version == 6 else "IP-CIDR", str(net))


def strip_logical(rest):
    """'((A,b),(C,d)),REJECT' -> '((A,b),(C,d))'"""
    depth = 0
    for i, ch in enumerate(rest):
        depth += ch == "("
        depth -= ch == ")"
        if depth == 0 and i > 0:
            return rest[: i + 1]
    return None


def parse_typed(line):
    kind, _, rest = line.partition(",")
    kind = ALIASES.get(kind.strip().upper(), kind.strip().upper())
    rest = rest.strip()
    if kind in LOGICAL:
        body = strip_logical(rest)
        return (kind, body) if body else None
    if kind == "USER-AGENT":
        value = rest.split(",")[0].strip()  # never contains a comma; the rest is a policy (group)
        return (kind, value) if value else None
    if kind in FREE_TEXT:
        parts = rest.split(",")
        while len(parts) > 1 and parts[-1].strip().lower() in POLICIES | {"no-resolve"}:
            parts.pop()
        value = ",".join(parts).strip()
        return (kind, value) if value else None
    parts = [p.strip() for p in rest.split(",")]
    value = parts[0] if parts else ""
    if kind in ("DOMAIN", "DOMAIN-SUFFIX"):
        d = norm_domain(value)
        if d is None and kind == "DOMAIN" and as_net(value) and "/" not in value:
            d = value.strip()  # blackmatrix7 keeps DOMAIN,<ip literal>
        return (kind, d) if d else None
    if kind == "DOMAIN-KEYWORD":
        v = value.strip().lower()
        return (kind, v) if v and " " not in v else None
    if kind == "DOMAIN-WILDCARD":
        v = value.strip().lower()
        return (kind, v) if re.match(r"^[a-z0-9_.*?-]+$", v) else None
    if kind in ("IP-CIDR", "IP-CIDR6"):
        net = as_net(value)
        return ip_rule(net) if net else None
    if kind in ("IP-ASN", "GEOIP", "PROCESS-NAME", "DEST-PORT"):
        return (kind, value) if value else None
    return None  # unknown type


def parse_source(text):
    """Every supported syntax: Surge / QX / Clash classical, Clash payload (domain / ipcidr
    behaviour), Surge DOMAIN-SET, plain domain lists, hosts files, AdBlock `||domain^`,
    sgmodule [Rule] sections, and m3u / URL lists (hostnames)."""
    rules = set()
    section = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith(("#", "//", "!", ";")) or line == "payload:":
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip().lower()
            continue
        if section not in (None, "rule", "filter_local", "filter"):
            continue
        if line.startswith("- "):
            line = line[2:].strip().strip("'\"")
        if line.startswith("||"):  # AdBlock
            m = re.match(r"^\|\|([a-z0-9_.-]+)\^(\$.*)?$", line.lower())
            if m and (not m.group(2) or "important" in m.group(2) or m.group(2) in ("$third-party",)):
                d = norm_domain(m.group(1))
                if d:
                    rules.add(("DOMAIN-SUFFIX", d))
            continue
        if line.startswith("@@") or line.startswith("|"):
            continue
        m = HOSTS_RE.match(line)
        if m:
            d = norm_domain(m.group(1))
            if d and d not in SKIP_HOSTS:
                rules.add(("DOMAIN", d))
            continue
        if re.match(r"^https?://", line, re.I):  # m3u / URL lists
            host = urllib.parse.urlsplit(line.split()[0]).hostname or ""
            net = as_net(host)
            if net:
                rules.add(ip_rule(net))
            elif norm_domain(host):
                rules.add(("DOMAIN", norm_domain(host)))
            continue
        if "," in line:
            r = parse_typed(line)
            if r:
                rules.add(r)
            continue
        token = line.split()[0]
        if token.startswith("+.") or token.startswith("."):
            d = norm_domain(token.lstrip("+").lstrip("."))
            if d:
                rules.add(("DOMAIN-SUFFIX", d))
            continue
        net = as_net(token)
        if net and ("/" in token or ":" in token or token.count(".") == 3):
            rules.add(ip_rule(net))
            continue
        d = norm_domain(token)
        if d:
            rules.add(("DOMAIN", d))
    return rules


# ------------------------------------------------------------------ set logic


def parents(domain):
    labels = domain.split(".")
    return [".".join(labels[i:]) for i in range(1, len(labels) - 1)]


class Matcher:
    """Answers "is this rule equal to, or inside, one of these rules?" (for excludes / removes)."""

    def __init__(self, rules, keywords=False):
        self.exact = set(rules)
        # keywords=True (comparison only): a DOMAIN-KEYWORD contained in a domain also matches it
        kws = [v for t, v in rules if t == "DOMAIN-KEYWORD"] if keywords else []
        self.kw_re = re.compile("|".join(re.escape(k) for k in kws)) if kws else None
        self.suffixes = {v for t, v in rules if t == "DOMAIN-SUFFIX"}
        self.nets = [ipaddress.ip_network(v) for t, v in rules if t in ("IP-CIDR", "IP-CIDR6")]

    def covers(self, rule):
        t, v = rule
        if rule in self.exact:
            return True
        if t in ("DOMAIN", "DOMAIN-SUFFIX"):
            if self.kw_re and self.kw_re.search(v):
                return True
            return v in self.suffixes or any(p in self.suffixes for p in parents(v))
        if t in ("IP-CIDR", "IP-CIDR6") and self.nets:
            net = ipaddress.ip_network(v)
            return any(net.version == n.version and net.subnet_of(n) for n in self.nets)
        return False


def optimize(rules, merge):
    """Merge the way the rule set's README badges say. blackmatrix7 keeps DOMAIN-SUFFIX rules
    that contain a keyword (YouTube keeps 170 *youtube* suffixes next to DOMAIN-KEYWORD,youtube),
    so only plain DOMAIN rules are folded into keywords, and only where the badge says so."""
    suffixes = {v for t, v in rules if t == "DOMAIN-SUFFIX"}
    keywords = [v for t, v in rules if t == "DOMAIN-KEYWORD"] if merge.get("domain_into_keyword") else []
    kw_re = re.compile("|".join(re.escape(k) for k in sorted(keywords, key=len))) if keywords else None
    out = set()
    nets = {4: [], 6: []}
    for t, v in rules:
        if t in ("DOMAIN", "DOMAIN-SUFFIX"):
            covered = any(p in suffixes for p in parents(v))
            if t == "DOMAIN-SUFFIX" and covered and merge.get("suffix_into_suffix", True):
                continue  # DOMAIN-SUFFIX inside a parent DOMAIN-SUFFIX
            if t == "DOMAIN":
                if merge.get("domain_into_suffix", True) and (covered or v in suffixes):
                    continue  # DOMAIN covered by a DOMAIN-SUFFIX
                if kw_re and kw_re.search(v):
                    continue  # DOMAIN covered by a DOMAIN-KEYWORD
            out.add((t, v))
        elif t in ("IP-CIDR", "IP-CIDR6") and merge.get("ip", True):
            net = ipaddress.ip_network(v)
            nets[net.version].append(net)
        else:
            out.add((t, v))
    for version in (4, 6):
        for net in ipaddress.collapse_addresses(nets[version]):
            out.add(ip_rule(net))
    return out


class Graph:
    def __init__(self, cfg, texts, overrides):
        self.cfg = cfg["rulesets"]
        self.texts = texts
        self.overrides = overrides
        self.done = {}
        self.stack = []

    def rules(self, name):
        if name in self.done:
            return self.done[name]
        if name in self.stack:
            raise RuntimeError("include / exclude cycle: " + " -> ".join(self.stack + [name]))
        self.stack.append(name)
        spec = self.cfg[name]
        rules = set()
        for url in spec["sources"]:
            if url in self.texts:
                rules |= parse_source(self.texts[url])
        for sub in spec["include"]:
            rules |= self.rules(sub)
        for ex in spec["exclude"]:
            m = Matcher(self.rules(ex))
            rules = {r for r in rules if not m.covers(r)}
        ov = self.overrides.get(name) or {}
        for line in ov.get("add", []):
            r = parse_typed(line)
            if r:
                rules.add(r)
            else:
                warn(f"{name}: override add {line!r} is not a rule")
        if ov.get("remove"):
            removes = [r for r in (parse_typed(l) for l in ov["remove"]) if r]
            m = Matcher(removes)
            rules = {r for r in rules if not m.covers(r)}
        result = optimize(rules, spec.get("merge", {}))
        self.stack.pop()
        self.done[name] = result
        return result


# ------------------------------------------------------------------ MITM


def mitm_hosts(regexes):
    hosts = set()
    for rx in regexes:
        s = rx.lstrip("^").replace("\\/", "/")
        m = re.match(r"^(?:https\??|http\??|https\?)?(?:s\?)?:?//(.+)$", s) or re.match(r"^https?\??://(.+)$", s)
        if not m:
            continue
        host = re.split(r"/|\$|:\d", m.group(1), maxsplit=1)[0]
        for pat in (r"\[\^/\]\+", r"\[\^/\]\*", r"\.\+\??", r"\.\*\??", r"\\w\+", r"\\d\+", r"\[[a-z0-9-]+\]\+",
                    r"\[\\w-\]\+", r"\\d\{?\d*,?\d*\}?", r"\\w", r"\[0-9\]\+?"):
            host = re.sub(pat, "*", host)
        host = host.replace("\\.", ".").replace("\\-", "-")
        if re.search(r"[()|?\[\]{}+^$\\]", host) or not host or "." not in host:
            continue
        host = re.sub(r"\*+", "*", host)
        hosts.add(host)
    wild = [h for h in hosts if "*" in h]
    pats = [re.compile("^" + re.escape(w).replace("\\*", ".*") + "$") for w in wild]
    return sorted(h for h in hosts if "*" in h or not any(p.match(h) for p in pats))


# ------------------------------------------------------------------ rendering


def sort_key(rule):
    t, v = rule
    return (TYPE_ORDER.index(t) if t in TYPE_ORDER else 99, v)


def line_of(rule, no_resolve, platform):
    t, v = rule
    if platform == "Shadowrocket" and t == "IP-CIDR6":
        t = "IP-CIDR"
    if platform == "Clash" and t == "DEST-PORT":
        t = "DST-PORT"
    s = f"{t},{v}"
    if no_resolve and t in IP_TYPES:
        s += ",no-resolve"
    return s


def counts(rules, platform):
    out = {}
    for t, _ in rules:
        if platform == "Shadowrocket" and t == "IP-CIDR6":
            t = "IP-CIDR"
        out[t] = out.get(t, 0) + 1
    return out


def header(name, title, platform, rules, note):
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"# NAME: {name}",
        f"# DESC: {title}",
        "# AUTHOR: generated by Maverick3a1/Net following blackmatrix7/ios_rule_script's method",
        f"# REPO: {REPO}",
        f"# UPDATED: {now}",
    ]
    if note:
        lines.append(f"# NOTE: {note}")
    c = counts(rules, platform)
    for t in sorted(c):
        lines.append(f"# {t}: {c[t]}")
    lines.append(f"# TOTAL: {sum(c.values())}")
    return lines


def is_header(line):
    return line.startswith("# ")


def write_if_changed(path, head, body):
    """Rewrite only when the rules changed, so UPDATED means something and git stays quiet."""
    old = None
    if path.exists():
        old = [l for l in path.read_text().splitlines() if not is_header(l)]
    if old == body:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(head + body) + "\n")
    return True


def payload(lines, quote=False):
    return ["payload:"] + [f"  - '{l}'" if quote else f"  - {l}" for l in lines]


def render(name, title, rules):
    """Write every file variant blackmatrix7 publishes for the three platforms."""
    written = 0
    regexes = sorted(v for t, v in rules if t == "URL-REGEX")
    note = "contains URL-REGEX rules; use with MITM (see the _MITM module)" if regexes else ""
    for platform in ("Surge", "Shadowrocket", "Clash"):
        kept = sorted((r for r in rules if r[0] in PLATFORM_TYPES[platform]), key=sort_key)
        domains = [v for t, v in kept if t == "DOMAIN"]
        suffixes = [v for t, v in kept if t == "DOMAIN-SUFFIX"]
        rest = [r for r in kept if r[0] not in ("DOMAIN", "DOMAIN-SUFFIX")]
        d = ROOT / name / platform
        head = header(name, title, platform, kept, note if platform != "Clash" else "")
        files = {}
        if platform in ("Surge", "Shadowrocket"):
            files[f"{name}.list"] = [line_of(r, True, platform) for r in rest]
            files[f"{name}_Resolve.list"] = [line_of(r, False, platform) for r in rest]
            files[f"{name}_Domain.list"] = domains + ["." + s for s in suffixes]
            if platform == "Surge":
                files[f"{name}_All.list"] = [line_of(r, False, platform) for r in kept]
                files[f"{name}_All_No_Resolve.list"] = [line_of(r, True, platform) for r in kept]
        else:
            files[f"{name}.yaml"] = payload([line_of(r, False, platform) for r in rest])
            files[f"{name}_No_Resolve.yaml"] = payload([line_of(r, True, platform) for r in rest])
            files[f"{name}_Classical.yaml"] = payload([line_of(r, False, platform) for r in kept])
            files[f"{name}_Classical_No_Resolve.yaml"] = payload([line_of(r, True, platform) for r in kept])
            files[f"{name}_Domain.yaml"] = payload(domains + ["+." + s for s in suffixes], quote=True)
            files[f"{name}_Domain.txt"] = domains + ["." + s for s in suffixes]
            files[f"{name}_Domain_For_Clash.txt"] = domains + ["+." + s for s in suffixes]
            files[f"{name}.list"] = [line_of(r, True, platform) for r in kept]
        for fname, body in files.items():
            if not any(l.strip() and l != "payload:" for l in body):
                stale = d / fname
                if stale.exists():
                    stale.unlink()
                    written += 1
                continue
            written += write_if_changed(d / fname, head, body)
        if platform != "Clash":
            hosts = mitm_hosts(r[1] for r in kept if r[0] == "URL-REGEX")
            mods = [f"{name}_MITM.sgmodule"] + ([f"{name}_MITM.conf"] if platform == "Shadowrocket" else [])
            for fname in mods:
                path = d / fname
                if not hosts:
                    if path.exists():
                        path.unlink()
                        written += 1
                    continue
                text = (f"#!name={name} MITM ({len(hosts)})\n#!desc=Derived from the URL-REGEX rules of {name}\n"
                        f"#!author=Maverick3a1/Net\n\n[MITM]\nhostname = %APPEND% {','.join(hosts)}\n")
                if not path.exists() or path.read_text().split("\n[MITM]")[1:] != text.split("\n[MITM]")[1:]:
                    path.write_text(text)
                    written += 1
    return written


def previous_total(name):
    path = ROOT / name / "Surge" / f"{name}_All.list"
    if not path.exists():
        return 0
    m = re.search(r"^# TOTAL: (\d+)$", path.read_text()[:2000], re.M)
    return int(m.group(1)) if m else 0


def update_readme(stats):
    if not README.exists():
        return
    rows = ["| Rule set | 内容 | 规则数 | Surge | Shadowrocket | Clash |", "| --- | --- | ---: | --- | --- | --- |"]
    for name, title, total in stats:
        if not total:
            continue  # nothing generated yet (e.g. every source unreachable): no files to link
        base = f"{RAW}/{name}"
        rows.append(
            f"| **{name}** | {title} | {total} "
            f"| [All]({base}/Surge/{name}_All.list) · [RULE-SET]({base}/Surge/{name}.list) · [DOMAIN-SET]({base}/Surge/{name}_Domain.list) "
            f"| [RULE-SET]({base}/Shadowrocket/{name}.list) · [DOMAIN-SET]({base}/Shadowrocket/{name}_Domain.list) "
            f"| [classical]({base}/Clash/{name}_Classical.yaml) · [domain]({base}/Clash/{name}_Domain.yaml) |"
        )
    block = "<!-- RULES:START -->\n" + "\n".join(rows) + "\n<!-- RULES:END -->"
    text = README.read_text()
    new = re.sub(r"<!-- RULES:START -->.*?<!-- RULES:END -->", block, text, flags=re.S)
    if new != text:
        README.write_text(new)
        log("updated README.md")


# ------------------------------------------------------------------ comparison with blackmatrix7

BM7_RULE = "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/{0}/{1}"
LOG_DIR = ROOT / "logs"
LOG_KEEP_DAYS = 30
SAMPLE = 30


def fetch_bm7(name):
    """blackmatrix7's published Surge rules for a rule set: (rules, updated) or (None, error)."""
    last = None
    for fname in (f"{name}_All.list", f"{name}.list"):  # small sets only have <name>.list (complete)
        try:
            text = fetch(BM7_RULE.format(name, fname))
        except Exception as exc:  # noqa: BLE001
            last = exc
            continue
        m = re.search(r"^# UPDATED: (.+)$", text, re.M)
        rules = set()
        for line in text.splitlines():
            if line.strip() and not line.startswith("#"):
                r = parse_typed(line.strip())
                if r:
                    rules.add(r)
        return rules, (m.group(1).strip() if m else "?")
    return None, str(last)


def type_counts(rules):
    out = {}
    for t, _ in rules:
        out[t] = out.get(t, 0) + 1
    return out


def compare_one(name, ours, theirs):
    common = ours & theirs
    only_theirs = theirs - ours
    only_ours = ours - theirs
    # A rule missing on one side may still be matched there by a broader rule (DOMAIN under a
    # DOMAIN-SUFFIX, a subnet inside a bigger range); count those separately.
    m_ours, m_theirs = Matcher(ours, keywords=True), Matcher(theirs, keywords=True)
    theirs_uncovered = sorted((r for r in only_theirs if not m_ours.covers(r)), key=sort_key)
    ours_uncovered = sorted((r for r in only_ours if not m_theirs.covers(r)), key=sort_key)
    return {
        "name": name,
        "ours": len(ours),
        "theirs": len(theirs),
        "common": len(common),
        "only_theirs": len(only_theirs),
        "only_ours": len(only_ours),
        "theirs_uncovered": theirs_uncovered,
        "ours_uncovered": ours_uncovered,
        "types": (type_counts(ours), type_counts(theirs)),
    }


def write_compare_log(results, failed_sources):
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    day = now.strftime("%Y-%m-%d")
    lines = [
        f"# 与 blackmatrix7 的差异 · {day}",
        "",
        f"生成时间：{now.strftime('%Y-%m-%d %H:%M:%S')}（北京时间）。比较对象：blackmatrix7 当前发布的 Surge 规则"
        "（有 `_All.list` 用它，否则用 `<名称>.list`），按规则逐条比较（忽略 no-resolve 和顺序）。",
        "",
        "- **只有我们有 / 只有它有**：对方文件里没有这一条完全相同的规则。",
        "- **其中未被覆盖**：对方也没有能匹配它的更宽的规则（上级 DOMAIN-SUFFIX、包含在域名里的 DOMAIN-KEYWORD、包含它的 IP 段），也就是真正的行为差异。",
        "",
        "| 规则集 | 我们 | blackmatrix7 | 相同 | 只有我们有 | 其中未被覆盖 | 只有它有 | 其中未被覆盖 | 它的更新时间 |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    details = []
    for r in results:
        if "error" in r:
            lines.append(f"| {r['name']} | {r['ours']} | 读取失败 | | | | | | {r['error'][:60]} |")
            continue
        lines.append(
            f"| [{r['name']}](#{r['name'].lower()}) | {r['ours']} | {r['theirs']} | {r['common']} "
            f"| {r['only_ours']} | {len(r['ours_uncovered'])} | {r['only_theirs']} | {len(r['theirs_uncovered'])} | {r['updated']} |"
        )
        ours_t, theirs_t = r["types"]
        types = sorted(set(ours_t) | set(theirs_t), key=lambda t: TYPE_ORDER.index(t) if t in TYPE_ORDER else 99)
        details += ["", f"## {r['name']}", ""]
        details.append("按类型（我们 / blackmatrix7）：" + "，".join(f"{t} {ours_t.get(t, 0)} / {theirs_t.get(t, 0)}" for t in types))
        for label, items in (("只有 blackmatrix7 有、我们也没覆盖到的", r["theirs_uncovered"]),
                             ("只有我们有、blackmatrix7 也没覆盖到的", r["ours_uncovered"])):
            if not items:
                continue
            shown = items[:SAMPLE]
            more = f"（共 {len(items)} 条，列出前 {len(shown)} 条）" if len(items) > len(shown) else f"（共 {len(items)} 条）"
            details += ["", f"**{label}**{more}：", "", "```"] + [f"{t},{v}" for t, v in shown] + ["```"]
    if failed_sources:
        details += ["", "## 本次没能下载的上游", "", "这些来源缺了，是差异的原因之一：", ""]
        details += [f"- {u}" for u in sorted(failed_sources)]
    LOG_DIR.mkdir(exist_ok=True)
    path = LOG_DIR / f"{day}.md"
    path.write_text("\n".join(lines + details) + "\n")
    log(f"wrote {path.relative_to(ROOT)}")
    cutoff = (now - datetime.timedelta(days=LOG_KEEP_DAYS)).strftime("%Y-%m-%d")
    for old in LOG_DIR.glob("????-??-??.md"):
        if old.stem < cutoff:
            old.unlink()
            log(f"removed {old.relative_to(ROOT)} (older than {LOG_KEEP_DAYS} days)")


def compare_all(names, graph, failed_sources):
    with concurrent.futures.ThreadPoolExecutor(WORKERS) as pool:
        fetched = dict(zip(names, pool.map(fetch_bm7, names)))
    results = []
    for name in names:
        ours = graph.rules(name)
        theirs, info = fetched[name]
        if theirs is None:
            results.append({"name": name, "ours": len(ours), "error": info})
            warn(f"compare: could not read blackmatrix7's {name}: {info}")
            continue
        r = compare_one(name, ours, theirs)
        r["updated"] = info
        results.append(r)
    write_compare_log(results, failed_sources)


# ------------------------------------------------------------------ main


def needed(cfg, names):
    seen, todo = set(), list(names)
    while todo:
        n = todo.pop()
        if n in seen or n not in cfg["rulesets"]:
            continue
        seen.add(n)
        todo += cfg["rulesets"][n]["include"] + cfg["rulesets"][n]["exclude"]
    return seen


def main(argv):
    cfg = json.loads(CONFIG.read_text())
    overrides = json.loads(OVERRIDES.read_text()) if OVERRIDES.exists() else {}
    outputs = [n for n in cfg["outputs"] if not argv or n in argv]
    names = needed(cfg, outputs)
    urls = sorted({u for n in names for u in cfg["rulesets"][n]["sources"]})
    log(f"{len(outputs)} outputs need {len(names)} rule sets and {len(urls)} sources")
    texts, failed = fetch_all(urls)
    log(f"fetched {len(texts)}/{len(urls)} sources")

    graph = Graph(cfg, texts, overrides)
    stats, problems = [], 0
    for name in outputs:
        rules = graph.rules(name)
        total = len(rules)
        prev = previous_total(name)
        title = cfg["rulesets"][name]["title"]
        if prev and total < prev * MIN_KEEP_RATIO:
            warn(f"{name}: shrank from {prev} to {total} rules; keeping previous files")
            problems += 1
            stats.append((name, title, prev))
            continue
        written = render(name, title, rules)
        log(f"[{name}] {total} rules, {written} files changed")
        stats.append((name, title, total))
    if not argv:
        update_readme(stats)  # a partial run would drop the other rule sets' rows
        compare_all(outputs, graph, failed)  # logs/<date>.md: differences from blackmatrix7
    if failed and len(failed) == len(urls):
        sys.exit("every source failed")


if __name__ == "__main__":
    main(sys.argv[1:])
