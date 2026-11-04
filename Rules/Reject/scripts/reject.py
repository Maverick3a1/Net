"""Shared ads / tracking / telemetry list for every category under Rules/.

Each category's scripts/build.py calls update() with its own sections. The
category's sections in Rules/Reject/<Platform>/Reject.* are replaced and the
other categories' sections are kept as they are, so a category can be rebuilt
on its own. The files themselves are the only state: nothing else is stored.

Rules are passed in Surge classical syntax (DOMAIN-SUFFIX,x / DOMAIN,x /
DOMAIN-KEYWORD,x / IP-CIDR,x,no-resolve); Clash classical uses the same lines.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUTS = {
    "Surge": (ROOT / "Surge" / "Reject.list", "Surge RULE-SET", False),
    "Shadowrocket": (ROOT / "Shadowrocket" / "Reject.list", "Shadowrocket RULE-SET", False),
    "Clash": (ROOT / "Clash" / "Reject.yaml", "Clash rule-provider, behavior: classical", True),
}
BANNER = "# " + "=" * 60
SEP = " / "


def _plain(line):
    """A file line as Surge syntax: Clash payload items and comments unwrapped."""
    s = line.strip()
    if s == "payload:":
        return None
    if s.startswith("- "):
        s = s[2:].strip()
        if len(s) >= 2 and s[0] == s[-1] and s[0] in "'\"":
            s = s[1:-1]
    return s


def _read(path):
    """[(category, title, description, [rules])] in file order."""
    if not path.exists():
        return []
    lines = [l for l in (_plain(x) for x in path.read_text().splitlines()) if l is not None]
    sections = []
    i = 0
    while i < len(lines):
        if lines[i] == BANNER and i + 3 < len(lines) and lines[i + 3] == BANNER:
            title = lines[i + 1][2:]
            desc = lines[i + 2][2:]
            category, _, name = title.partition(SEP)
            sections.append((category, name, desc, []))
            i += 4
            continue
        if sections and lines[i] and not lines[i].startswith("#"):
            sections[-1][3].append(lines[i])
        i += 1
    return sections


def _body(sections, is_clash):
    out = []
    for category, name, desc, rules in sections:
        if not rules:
            continue
        if out:
            out.append("")
        out += [BANNER, f"# {category}{SEP}{name}", f"# {desc}", BANNER] + rules
    if is_clash:
        out = ["payload:"] + [
            "" if not l else f"  {l}" if l.startswith("#") else f"  - '{l}'" for l in out
        ]
    return out


def _header(fmt):
    # No UPDATED stamp or counts: every category's PR touches this file, and lines that
    # change on every write would make two such PRs conflict.
    return [
        "# NAME: Reject",
        "# DESC: Ads, tracking and telemetry pulled out of every category under Rules/",
        f"# FORMAT: {fmt}",
        "# SOURCE: Rules/<category>/scripts/build.py (see each category's README)",
    ]


def update(category, sections_by_platform, log=print):
    """Replace `category`'s sections; sections_by_platform = {platform: [(name, desc, [rules])]}."""
    for platform, (path, fmt, is_clash) in OUTPUTS.items():
        old = _read(path)
        others = [s for s in old if s[0] != category]
        mine = [(category, n, d, list(r)) for n, d, r in sections_by_platform[platform] if r]
        sections = sorted(others + mine, key=lambda s: s[0])  # stable: keeps each category's order
        body = _body(sections, is_clash)
        rel = path.relative_to(ROOT.parent.parent)
        if not body:
            if path.exists():
                path.unlink()
                log(f"  removed {rel} (empty)")
            continue
        text = "\n".join(_header(fmt) + body) + "\n"
        if path.exists() and path.read_text() == text:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        log(f"  wrote {rel} ({sum(len(s[3]) for s in sections)} rules)")
