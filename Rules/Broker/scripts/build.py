#!/usr/bin/env python3
"""Collect HK/US internet broker domains / IP ranges and render Clash + Surge + Shadowrocket rulesets.

Stdlib only. Run from anywhere:  python3 scripts/build.py
"""

import datetime
import functools
import ipaddress
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config" / "brokers.jsonc"
CLASH_DIR = ROOT / "Clash"
SURGE_DIR = ROOT / "Surge"
SHADOWROCKET_DIR = ROOT / "Shadowrocket"
README = ROOT / "README.md"
CATEGORY = ROOT.name

# Shared Rules/Reject/<Platform>/Reject.* lists, one section per category
sys.path.insert(0, str(ROOT.parent / "Reject" / "scripts"))
import reject as shared_reject  # noqa: E402

V2FLY_RAW = "https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/{}"
BM7_RAW = "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/{platform}/{name}/{name}.{ext}"
RIPE_PREFIXES = "https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS{}"
FORECHO_RAW = "https://raw.githubusercontent.com/forecho/broker-rules/main/rule/{platform}/{name}.{ext}"
FORECHO_CONF = "https://raw.githubusercontent.com/forecho/broker-rules/main/Source/{dir}/{conf}.conf"
PLATFORMS = ("Surge", "Shadowrocket", "Clash")
PLATFORM_EXT = {"Surge": "list", "Shadowrocket": "list", "Clash": "yaml"}
ENTRIES = "brokers"
USER_AGENT = "Broker-Rules/1.0 (+https://github.com)"

# A rule set must not shrink below this fraction of its previous size in one run.
MIN_KEEP_RATIO = 0.5

DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)(?!-)[a-z0-9-]{1,63}(?<!-)(\.(?!-)[a-z0-9-]{1,63}(?<!-))+$"
)
KEYWORD_RE = re.compile(r"^[a-z0-9.-]+$")


class SourceError(Exception):
    pass


def log(msg):
    print(msg, flush=True)


def warn(msg):
    # Rendered as an annotation when running in GitHub Actions.
    print(f"::warning::{msg}", flush=True)


def fetch(url, retries=3, timeout=30):
    last = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8")
        except Exception as exc:  # noqa: BLE001 - any network failure is retried
            last = exc
            if attempt < retries:
                time.sleep(2 * attempt)
    raise SourceError(f"GET {url} failed: {last}")


class RuleSet:
    def __init__(self):
        self.suffix = set()
        self.full = set()
        self.keyword = set()
        self.nets = set()
        # (kind, value) entries an upstream itself marks as ads / telemetry
        self.tracked = set()

    def update(self, other):
        self.suffix |= other.suffix
        self.full |= other.full
        self.keyword |= other.keyword
        self.nets |= other.nets
        self.tracked |= other.tracked

    def add_cidr(self, value):
        try:
            self.nets.add(ipaddress.ip_network(value.strip(), strict=False))
        except ValueError:
            warn(f"invalid CIDR skipped: {value!r}")

    def normalize(self, deny_suffix=(), exclude=()):
        exclude = {e.lower() for e in exclude}
        deny_suffix = {d.lower() for d in deny_suffix}

        def clean(values, kind):
            out = set()
            for v in values:
                v = v.strip().lower().rstrip(".")
                if not v or v in exclude:
                    continue
                if kind == "keyword":
                    ok = KEYWORD_RE.match(v)
                else:
                    ok = DOMAIN_RE.match(v)
                if not ok:
                    warn(f"invalid {kind} skipped: {v!r}")
                    continue
                if kind == "suffix" and v in deny_suffix:
                    warn(f"overly broad suffix skipped: {v!r}")
                    continue
                out.add(v)
            return out

        suffix = clean(self.suffix, "suffix")
        full = clean(self.full, "domain")
        keyword = clean(self.keyword, "keyword")

        def covered(domain, include_self):
            parts = domain.split(".")
            start = 0 if include_self else 1
            return any(".".join(parts[i:]) in suffix for i in range(start, len(parts) - 1))

        self.suffix = {s for s in suffix if not covered(s, include_self=False)}
        suffix = self.suffix
        self.full = {f for f in full if not covered(f, include_self=True)}
        self.keyword = keyword

        v4 = [n for n in self.nets if n.version == 4]
        v6 = [n for n in self.nets if n.version == 6]
        self.nets = set(ipaddress.collapse_addresses(v4)) | set(ipaddress.collapse_addresses(v6))
        return self

    def subtract(self, seen):
        """Copy without entries already covered by `seen` (used for aggregate sections)."""

        def covered(domain):
            parts = domain.split(".")
            return any(".".join(parts[i:]) in seen.suffix for i in range(len(parts) - 1))

        out = RuleSet()
        out.suffix = {d for d in self.suffix if not covered(d)}
        out.full = {d for d in self.full if d not in seen.full and not covered(d)}
        out.keyword = self.keyword - seen.keyword
        out.nets = {
            n for n in self.nets
            if not any(n.version == m.version and n.subnet_of(m) for m in seen.nets)
        }
        return out

    def sorted_domains(self):
        def key(d):
            return list(reversed(d.split(".")))

        return sorted(self.suffix, key=key), sorted(self.full, key=key), sorted(self.keyword)

    def sorted_nets(self):
        return sorted(self.nets, key=lambda n: (n.version, n.network_address, n.prefixlen))

    def count(self):
        return len(self.suffix) + len(self.full) + len(self.keyword) + len(self.nets)


# ---------------------------------------------------------------- sources


def load_v2fly(name, exclude_attrs, seen=None, reject_attrs=()):
    seen = seen if seen is not None else set()
    if name in seen:
        return RuleSet()
    seen.add(name)
    rs = RuleSet()
    text = fetch(V2FLY_RAW.format(name))
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        tokens = line.split()
        entry = tokens[0]
        attrs = {t[1:] for t in tokens[1:] if t.startswith("@")}
        if attrs & set(exclude_attrs):
            continue
        if ":" in entry:
            kind, value = entry.split(":", 1)
        else:
            kind, value = "domain", entry
        field = {"domain": "suffix", "full": "full", "keyword": "keyword"}.get(kind)
        if field:
            getattr(rs, field).add(value)
            if attrs & set(reject_attrs):
                rs.tracked.add((field, value.lower()))
        elif kind == "include":
            rs.update(load_v2fly(value, exclude_attrs, seen, reject_attrs))
        elif kind == "regexp":
            log(f"  v2fly/{name}: regexp not portable to Clash+Surge, skipped: {value}")
        else:
            warn(f"v2fly/{name}: unknown entry type {kind!r}")
    return rs


def load_asn(asn):
    rs = RuleSet()
    data = json.loads(fetch(RIPE_PREFIXES.format(asn)))
    if data.get("status") != "ok":
        raise SourceError(f"RIPEstat AS{asn}: status {data.get('status')}")
    for p in data["data"]["prefixes"]:
        rs.add_cidr(p["prefix"])
    return rs


# ---------------------------------------------------------------- per-platform upstreams
#
# blackmatrix7 and forecho publish one file per client. Each of our platforms is built
# from the upstream file for the same platform (Surge <- Surge, Shadowrocket <- Shadowrocket,
# Clash <- Clash); v2fly, RIPEstat and the manual entries are platform-neutral.


def parse_classical(text):
    """(TYPE, value) pairs from a Surge list or a Clash classical payload."""
    out = []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or line == "payload:":
            continue
        line = line.removeprefix("- ").strip().strip("'\"")
        kind, _, rest = line.partition(",")
        if rest:
            out.append((kind.strip().upper(), rest.split(",", 1)[0].strip().lower()))
    return out


def to_ruleset(pairs, label):
    rs = RuleSet()
    for kind, value in pairs:
        if kind == "DOMAIN-SUFFIX":
            rs.suffix.add(value)
        elif kind == "DOMAIN":
            rs.full.add(value)
        elif kind == "DOMAIN-KEYWORD":
            rs.keyword.add(value)
        elif kind in ("IP-CIDR", "IP-CIDR6"):
            rs.add_cidr(value)
        else:
            log(f"  {label}: unsupported rule skipped: {kind},{value}")
    return rs


_platform_cache = {}


def platform_rules(url_fmt, label, **fmt):
    """{platform: [(TYPE, value)]} fetched from each platform's own upstream file."""
    key = (url_fmt, tuple(sorted(fmt.items())))
    if key not in _platform_cache:
        out = {}
        for platform in PLATFORMS:
            url = url_fmt.format(platform=platform, ext=PLATFORM_EXT[platform], **fmt)
            pairs = parse_classical(fetch(url))
            if not pairs:
                raise SourceError(f"{label} ({platform}): no rules parsed")
            out[platform] = pairs
        _platform_cache[key] = out
    return _platform_cache[key]


@functools.lru_cache(maxsize=None)
def forecho_conf(name, conf):
    """Rules of one forecho Source/<name>/<conf>.conf, used only to split the list per entry."""
    url = FORECHO_CONF.format(dir=name.lower(), conf=conf)
    return set(parse_classical(fetch(url)))


def forecho_claimed(cfg, name):
    """Rules of every forecho conf that some entry in the config maps."""
    claimed = set()
    for entry in cfg[ENTRIES]:
        for src in entry.get("sources", []):
            if src["type"] == "forecho" and src["list"] == name and "conf" in src:
                claimed |= forecho_conf(name, src["conf"])
    return claimed


def load_forecho(src, cfg):
    name = src["list"]
    rules = platform_rules(FORECHO_RAW, f"forecho/{name}", name=name)
    if src.get("rest"):
        # Whatever no mapped conf claims (shared SDKs, IPs, confs added upstream later).
        claimed = forecho_claimed(cfg, name)
        keep = lambda r: r not in claimed  # noqa: E731
        label = f"forecho/{name} (unmapped)"
        extra = {r for r in rules["Surge"] if keep(r)}
        if extra:
            log(f"  {label}: {len(extra)} rules not in any mapped conf")
    else:
        members = forecho_conf(name, src["conf"])
        keep = lambda r: r in members  # noqa: E731
        label = f"forecho/{name}:{src['conf']}"
    return {p: to_ruleset([r for r in pairs if keep(r)], label) for p, pairs in rules.items()}


def forecho_unmapped_warnings(cfg):
    """Warn about forecho rules no entry publishes (a list without a "rest" holder)."""
    lists = {}
    for entry in cfg[ENTRIES]:
        for src in entry.get("sources", []):
            if src["type"] == "forecho":
                lists[src["list"]] = lists.get(src["list"], False) or bool(src.get("rest"))
    for name, has_rest in lists.items():
        if has_rest:
            continue
        claimed = forecho_claimed(cfg, name)
        rules = platform_rules(FORECHO_RAW, f"forecho/{name}", name=name)
        for kind, value in sorted({r for r in rules["Surge"] if r not in claimed}):
            warn(f"forecho/{name}: {kind},{value} is not in any mapped conf, not published")


def load_blackmatrix7(name):
    return {
        p: to_ruleset(pairs, f"blackmatrix7/{name}")
        for p, pairs in platform_rules(BM7_RAW, f"blackmatrix7/{name}", name=name).items()
    }


def build_broker(broker, cfg):
    """({platform: kept}, {platform: rejected}): neutral sources shared by all platforms,
    per-platform sources by platform."""
    neutral = RuleSet()
    neutral.suffix |= set(broker.get("domain_suffix", []))
    neutral.full |= set(broker.get("domain", []))
    neutral.keyword |= set(broker.get("domain_keyword", []))
    for c in broker.get("ip_cidr", []):
        neutral.add_cidr(c)
    own = {p: RuleSet() for p in PLATFORMS}

    def per_platform(parts, label):
        log(f"  {label}: {parts['Surge'].count()} entries")
        for p in PLATFORMS:
            own[p].update(parts[p])

    for src in broker.get("sources", []):
        kind = src["type"]
        if kind == "v2fly":
            part = load_v2fly(src["list"], cfg.get("v2fly_exclude_attrs", []), reject_attrs=cfg.get("v2fly_reject_attrs", []))
            log(f"  v2fly/{src['list']}: {part.count()} entries")
            neutral.update(part)
        elif kind == "asn":
            part = load_asn(src["asn"])
            log(f"  AS{src['asn']}: {part.count()} entries")
            neutral.update(part)
        elif kind == "blackmatrix7":
            per_platform(load_blackmatrix7(src["list"]), f"blackmatrix7/{src['list']}")
        elif kind == "forecho":
            per_platform(load_forecho(src, cfg), f"forecho/{src['list']}:{src.get('conf', 'unmapped')}")
        else:
            raise SourceError(f"unknown source type {kind!r}")

    out, rejected = {}, {}
    for p in PLATFORMS:
        rs = RuleSet()
        rs.update(neutral)
        rs.update(own[p])
        kept, rej = split_reject(rs, cfg.get("reject", {}))
        out[p] = kept.normalize(cfg.get("global_deny_suffix", []), broker.get("exclude", []))
        rejected[p] = rej.normalize((), broker.get("exclude", []))
    return out, rejected


def load_mainland_brokers(cfg):
    """Domains of mainland securities firms, which must never end up in a broker ruleset."""
    deny = RuleSet()
    for name in cfg.get("mainland_deny_v2fly", []):
        deny.update(load_v2fly(name, []))
    return deny.suffix | deny.full


def drop_mainland(name, rs, mainland, quiet=False):
    def hit(domain):
        parts = domain.split(".")
        return any(".".join(parts[i:]) in mainland for i in range(len(parts) - 1))

    for kind in ("suffix", "full"):
        values = getattr(rs, kind)
        bad = {d for d in values if hit(d)}
        for d in sorted(bad if not quiet else ()):
            warn(f"{name}: {d} belongs to a mainland securities firm, dropped")
        setattr(rs, kind, values - bad)
    return rs


def split_reject(rs, reject_cfg):
    """(kept, rejected): ads / tracking / telemetry entries go to the category's Reject list.

    An entry is rejected when its upstream marks it (v2fly @ads / @telemetry) or it is at or
    under one of the config's reject domains. Runs before normalize(), so a tracker host under
    a vendor's own suffix is moved out instead of being folded into that suffix."""
    suffixes = {d.lower() for d in reject_cfg.get("domain_suffix", [])}
    hosts = {d.lower() for d in reject_cfg.get("domain", [])}

    def hit(field, value):
        value = value.strip().lower().rstrip(".")
        if (field, value) in rs.tracked or value in hosts:
            return True
        if field == "keyword":
            return False
        parts = value.split(".")
        return any(".".join(parts[i:]) in suffixes for i in range(len(parts)))

    kept, rejected = RuleSet(), RuleSet()
    for field in ("suffix", "full", "keyword"):
        for value in getattr(rs, field):
            getattr(rejected if hit(field, value) else kept, field).add(value)
    kept.nets = set(rs.nets)
    return kept, rejected


def combine(entries):
    """Merge [(name, desc, {platform: RuleSet})] into one ruleset, one commented section per entry."""
    rs = {p: RuleSet() for p in PLATFORMS}
    sections = {p: [] for p in PLATFORMS}
    for name, desc, parts in entries:
        for p in PLATFORMS:
            part = parts[p].subtract(rs[p])
            rs[p].update(part)
            sections[p].append((name, desc, part))
    return rs, sections


# ---------------------------------------------------------------- renderers


def surge_rules(rs):
    suffix, full, keyword = rs.sorted_domains()
    lines = [f"DOMAIN-SUFFIX,{d}" for d in suffix]
    lines += [f"DOMAIN,{d}" for d in full]
    lines += [f"DOMAIN-KEYWORD,{k}" for k in keyword]
    for n in rs.sorted_nets():
        kind = "IP-CIDR" if n.version == 4 else "IP-CIDR6"
        lines.append(f"{kind},{n},no-resolve")
    return lines


def surge_domain_set(rs):
    suffix, full, _ = rs.sorted_domains()
    return [f".{d}" for d in suffix] + full


def clash_payload(lines):
    out = ["payload:"]
    for line in lines:
        if not line:
            out.append("")
        elif line.startswith("#"):
            out.append(f"  {line}")
        else:
            out.append(f"  - '{line}'")
    return out


def clash_domain(rs):
    suffix, full, _ = rs.sorted_domains()
    return [f"+.{d}" for d in suffix] + full


def clash_ipcidr(rs):
    return [str(n) for n in rs.sorted_nets()]


def header(name, description, fmt, rs, comment):
    suffix, full, keyword = rs.sorted_domains()
    nets = rs.sorted_nets()
    v4 = sum(1 for n in nets if n.version == 4)
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    return [
        f"{comment} NAME: {name}",
        f"{comment} DESC: {description}",
        f"{comment} FORMAT: {fmt}",
        f"{comment} UPDATED: {now}",
        f"{comment} DOMAIN-SUFFIX: {len(suffix)}",
        f"{comment} DOMAIN: {len(full)}",
        f"{comment} DOMAIN-KEYWORD: {len(keyword)}",
        f"{comment} IP-CIDR: {v4}",
        f"{comment} IP-CIDR6: {len(nets) - v4}",
        f"{comment} SOURCE: https://github.com/v2fly/domain-list-community, https://github.com/forecho/broker-rules, https://github.com/blackmatrix7/ios_rule_script, RIPEstat",
    ]


HEADER_RE = re.compile(
    r"^# (NAME|DESC|FORMAT|UPDATED|DOMAIN-SUFFIX|DOMAIN|DOMAIN-KEYWORD|IP-CIDR|IP-CIDR6|SOURCE): "
)


def body_of(path):
    """Existing file content without the metadata header (for change detection)."""
    if not path.exists():
        return None
    return [l for l in path.read_text().splitlines() if not HEADER_RE.match(l)]


def is_rule(line):
    stripped = line.strip()
    return bool(stripped) and not stripped.startswith("#") and stripped != "payload:"


def sectioned(fn, sections):
    """Render each (name, description, ruleset) section under a comment banner."""
    if len(sections) == 1 and sections[0][0] is None:
        return fn(sections[0][2])
    out = []
    for name, description, part in sections:
        lines = fn(part)
        if not lines:
            continue
        if out:
            out.append("")
        out += [
            "# " + "=" * 60,
            f"# {name}",
            f"# {description}",
            "# " + "=" * 60,
        ]
        out += lines
    return out


def write_if_changed(path, head, body):
    """Rewrite only when rules changed, so the UPDATED stamp means something."""
    if not any(is_rule(l) for l in body):
        if path.exists():
            path.unlink()
            log(f"  removed {path.relative_to(ROOT)} (empty)")
        return
    if body_of(path) == body:
        return
    path.write_text("\n".join(head + body) + "\n")
    log(f"  wrote {path.relative_to(ROOT)} ({len(body)} lines)")


def render(name, description, rs_by, sections_by=None):
    """Write all seven formats, each platform from its own {platform: RuleSet}.

    `sections_by` ({platform: sections}) splits the body into commented blocks."""
    sections_by = sections_by or {p: [(None, None, rs_by[p])] for p in PLATFORMS}
    outputs = [
        ("Surge", SURGE_DIR / f"{name}.list", "Surge RULE-SET", surge_rules, False),
        ("Surge", SURGE_DIR / f"{name}_Domain.list", "Surge DOMAIN-SET", surge_domain_set, False),
        ("Shadowrocket", SHADOWROCKET_DIR / f"{name}.list", "Shadowrocket RULE-SET", surge_rules, False),
        ("Shadowrocket", SHADOWROCKET_DIR / f"{name}_Domain.list", "Shadowrocket DOMAIN-SET", surge_domain_set, False),
        ("Clash", CLASH_DIR / f"{name}.yaml", "Clash rule-provider, behavior: classical", surge_rules, True),
        ("Clash", CLASH_DIR / f"{name}_Domain.yaml", "Clash rule-provider, behavior: domain", clash_domain, True),
        ("Clash", CLASH_DIR / f"{name}_IP.yaml", "Clash rule-provider, behavior: ipcidr", clash_ipcidr, True),
    ]
    for platform, path, fmt, fn, is_clash in outputs:
        body = sectioned(fn, sections_by[platform])
        if is_clash:
            body = clash_payload(body)
        write_if_changed(path, header(name, description, fmt, rs_by[platform], "#"), body)


def previous_count(agg_name, name):
    """Rules under `name`'s section banner in the existing aggregate Surge list (0 if absent)."""
    body = body_of(SURGE_DIR / f"{agg_name}.list") or []
    banner = "# " + "=" * 60
    count, current = 0, None
    for prev, line in zip([""] + body, body):
        if prev == banner and line.startswith("# "):
            current = line[2:]
        elif current == name and is_rule(line):
            count += 1
    return count


# ---------------------------------------------------------------- README


README_LABEL = "券商"


# Any raw ruleset link, whatever repo/subdir it currently points at.
RAW_LINK = re.compile(
    r"https://raw\.githubusercontent\.com/[^/\s)]+/[^/\s)]+/main/(?!Rules/Reject/)(?:[^\s)]*?/)?(?=(?:Surge|Shadowrocket|Clash)/)"
)


def repo_slug():
    slug = os.environ.get("GITHUB_REPOSITORY")
    if slug:
        return slug
    try:
        url = subprocess.run(
            ["git", "-C", str(ROOT), "remote", "get-url", "origin"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        m = re.search(r"github\.com[:/](.+?)(?:\.git)?$", url)
        if m:
            return m.group(1)
    except Exception:  # noqa: BLE001
        pass
    return "<USER>/<REPO>"


def repo_subdir():
    """Path of ROOT inside its git repo, e.g. "Rules/AI" in the Net monorepo."""
    try:
        return subprocess.run(
            ["git", "-C", str(ROOT), "rev-parse", "--show-prefix"],
            capture_output=True, text=True, check=True,
        ).stdout.strip().rstrip("/")
    except Exception:  # noqa: BLE001
        return ""


def update_readme(entries):
    if not README.exists():
        return
    slug = repo_slug()
    subdir = repo_subdir()
    base = f"https://raw.githubusercontent.com/{slug}/main" + (f"/{subdir}" if subdir else "")
    p = f"{base}/" if base else ""

    def surge_of(rs):
        return rs["Surge"] if isinstance(rs, dict) else rs

    def counts(rs):
        rs = surge_of(rs)
        return len(rs.suffix) + len(rs.full) + len(rs.keyword), len(rs.nets)

    # entries = every member, then the aggregate last; only the aggregate has files.
    n, _, agg = entries[-1]
    members = [e for e in entries[:-1] if surge_rules(surge_of(e[2]))]
    clash = f"[classical]({p}Clash/{n}.yaml) · [domain]({p}Clash/{n}_Domain.yaml)"
    if (agg["Clash"] if isinstance(agg, dict) else agg).nets:
        clash += f" · [ipcidr]({p}Clash/{n}_IP.yaml)"
    domains, nets = counts(agg)
    rows = [
        "| 平台 | 规则文件 |",
        "| --- | --- |",
        f"| Surge | [RULE-SET]({p}Surge/{n}.list) · [DOMAIN-SET]({p}Surge/{n}_Domain.list) |",
        f"| Shadowrocket | [RULE-SET]({p}Shadowrocket/{n}.list) · [DOMAIN-SET]({p}Shadowrocket/{n}_Domain.list) |",
        f"| Clash / mihomo | {clash} |",
        "",
        f"`{n}` 共 {domains} 条域名规则、{nets} 个 IP 段，收录以下 {len(members)} 个{README_LABEL}：",
        "",
        f"| {README_LABEL} | 说明 | 域名 | IP |",
        "| --- | --- | ---: | ---: |",
    ]
    for name, desc, rs in members:
        d, i = counts(rs)
        rows.append(f"| {name} | {desc} | {d} | {i} |")
    block = "<!-- RULES:START -->\n" + "\n".join(rows) + "\n<!-- RULES:END -->"
    text = README.read_text()
    new = re.sub(r"<!-- RULES:START -->.*?<!-- RULES:END -->", block, text, flags=re.S)
    if slug != "<USER>/<REPO>":
        # Re-point every ruleset link (usage examples too) at this repo/subdir.
        new = RAW_LINK.sub(base + "/", new)
    if new != text:
        README.write_text(new)
        log("  updated README.md")


# ---------------------------------------------------------------- main


def load_config():
    """brokers.jsonc is JSON plus full-line // comments."""
    lines = [l for l in CONFIG.read_text().splitlines() if not l.lstrip().startswith("//")]
    return json.loads("\n".join(lines))


def main():
    cfg = load_config()
    try:
        mainland = load_mainland_brokers(cfg)
    except SourceError as exc:
        # Without the deny list we cannot prove the output is clean, so publish nothing.
        sys.exit(f"mainland deny list unavailable: {exc}")
    log(f"mainland deny list: {len(mainland)} domains")
    CLASH_DIR.mkdir(exist_ok=True)
    SURGE_DIR.mkdir(exist_ok=True)
    SHADOWROCKET_DIR.mkdir(exist_ok=True)

    built = []
    rejects = []
    failed = []
    for broker in cfg["brokers"]:
        name = broker["name"]
        log(f"[{name}]")
        try:
            kept, rej = build_broker(broker, cfg)
            rs = {
                p: drop_mainland(name, part, mainland, quiet=p != "Surge")
                for p, part in kept.items()
            }
        except SourceError as exc:
            warn(f"{name}: {exc}; keeping previous aggregate")
            failed.append(name)
            continue
        prev = previous_count(cfg["aggregate"]["name"], name)
        new = len(surge_rules(rs["Surge"]))
        if prev and new < prev * MIN_KEEP_RATIO:
            warn(f"{name}: shrank from {prev} to {new} rules; keeping previous aggregate")
            failed.append(name)
            continue
        log(f"  total: {new} rules")
        built.append((name, broker["description"], rs))
        rejects.append((name, broker["description"], rej))

    agg = cfg.get("aggregate")
    if agg and not failed:
        log(f"[{agg['name']}]")
        rs, sections = combine(built)
        log(f"  total: {len(surge_rules(rs['Surge']))} rules")
        render(agg["name"], agg["description"], rs, sections)
        built.append((agg["name"], agg["description"], rs))
    elif agg:
        warn(f"{agg['name']}: skipped because {', '.join(failed)} failed")

    # Ads / tracking / telemetry pulled out of every entry go to the shared Rules/Reject lists,
    # as this category's section; the other categories' sections are left alone.
    if cfg.get("reject") is not None and not failed:
        log(f"[Reject: {CATEGORY}]")
        _, sections = combine(rejects)
        shared_reject.update(CATEGORY, {p: [(n, d, surge_rules(part)) for n, d, part in sections[p]] for p in PLATFORMS}, log)
    elif cfg.get("reject") is not None:
        warn(f"Reject: {CATEGORY} section kept because {', '.join(failed)} failed")

    if not failed:
        update_readme(built)
        try:
            forecho_unmapped_warnings(cfg)
        except SourceError as exc:
            warn(f"forecho unmapped check skipped: {exc}")

    if len(failed) == len(cfg["brokers"]):
        sys.exit("all brokers failed")


if __name__ == "__main__":
    main()
