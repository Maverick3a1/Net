#!/usr/bin/env python3
"""Offline test for dnscheck.py and its use in build.py.

All queries go to a fake DNS server on 127.0.0.1; nothing is sent to real resolvers.
Run: python3 BlackMatrix7Rules/scripts/test_dnscheck.py
"""

import asyncio
import os
import struct
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dnscheck  # noqa: E402

asked = []


class FakeDNS(asyncio.DatagramProtocol):
    """dead* -> NXDOMAIN, flaky* -> no answer, anything else -> NOERROR."""

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        txid = struct.unpack(">H", data[:2])[0]
        labels, i = [], 12
        while data[i]:
            labels.append(data[i + 1 : i + 1 + data[i]].decode())
            i += data[i] + 1
        name = ".".join(labels)
        asked.append(name)
        if name.startswith("flaky"):
            return
        rcode = 3 if name.startswith("dead") else 0
        self.transport.sendto(struct.pack(">HHHHHH", txid, 0x8180 | rcode, 1, 0, 0, 0) + data[12:], addr)


async def run_checks(port):
    loop = asyncio.get_running_loop()
    transport, _ = await loop.create_datagram_endpoint(FakeDNS, local_addr=("127.0.0.1", port))
    try:
        servers = {"a": ["127.0.0.1"], "b": ["127.0.0.1"]}
        resolver = dnscheck.Resolver(servers=servers, port=port, timeout=0.2, qps=5000)
        names = ["ok.example", "dead.example", "flaky.example"] + [f"x{i}.example" for i in range(300)]
        return await dnscheck.check(names, resolver)
    finally:
        transport.close()


def main():
    port = 53000 + os.getpid() % 1000
    res = asyncio.run(run_checks(port))
    assert res["ok.example"] == "ok"
    assert res["dead.example"] == "nx"
    assert res["flaky.example"] == "err"
    assert all(res[f"x{i}.example"] == "ok" for i in range(300))
    assert asked.count("dead.example") == 2, "NXDOMAIN is confirmed with the second provider"
    assert asked.count("flaky.example") == dnscheck.ATTEMPTS, "unanswered names are retried, then left unknown"
    print(f"ok: fake resolver answered {len(asked)} queries (all to 127.0.0.1:{port})")

    # removal only after two NXDOMAIN runs; unknown results never change anything
    names = {"ok.example", "dead.example", "flaky.example"}
    state = {}
    dnscheck.update(state, names, {"ok.example": "ok", "dead.example": "nx", "flaky.example": "err"})
    assert dnscheck.dead(state) == set() and "flaky.example" not in state
    dnscheck.update(state, names, {"dead.example": "nx", "flaky.example": "err"})
    assert dnscheck.dead(state) == {"dead.example"}
    dnscheck.update(state, names, {"dead.example": "ok"})
    assert dnscheck.dead(state) == set(), "a domain that comes back is restored"
    dnscheck.update(state, {"ok.example"}, {})
    assert set(state) == {"ok.example"}, "domains that left the list are forgotten"

    # a run where most answers are NXDOMAIN is ignored
    s = {}
    many = {f"n{i}.x": ("nx" if i < 250 else "ok") for i in range(300)}
    summary = dnscheck.update(s, set(many), many)
    assert summary["applied"] is False and s == {}
    few = {"a.x": "nx", "b.x": "nx", "c.x": "ok"}
    assert dnscheck.update({}, set(few), few)["applied"] is True, "small samples are not judged by ratio"

    # each day checks new + NXDOMAIN + one seventh of the rest; a week covers everyone
    all_names = {f"d{i}.example" for i in range(7000)}
    st = {n: ("ok", 0) for n in all_names}
    st["d1.example"] = ("nx", 1)
    days = [set(dnscheck.due(all_names | {"new.example"}, st, d)) for d in range(7)]
    assert all("new.example" in d and "d1.example" in d for d in days)
    assert set().union(*days) >= all_names
    assert 800 < len(days[0]) < 1250, len(days[0])

    # state file round trip
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "dns.tsv"
        dnscheck.save_state(p, {"b.example": ("nx", 2), "a.example": ("ok", 0)})
        assert dnscheck.load_state(p) == {"a.example": ("ok", 0), "b.example": ("nx", 2)}
        assert dnscheck.save_state(p, dnscheck.load_state(p)) is False, "unchanged state is not rewritten"

        # build.py: without BM7_DNS / GITHUB_ACTIONS it never queries, only applies saved results
        os.environ.pop("GITHUB_ACTIONS", None)
        os.environ["BM7_DNS"] = "0"
        import build  # noqa: E402

        build.STATE_DIR = Path(tmp)
        dnscheck.save_state(Path(tmp) / "dns-Ad.tsv", {"gone.example": ("nx", 2), "maybe.example": ("nx", 1)})

        async def no_queries(*_a, **_k):
            raise AssertionError("must not query DNS here")

        build.dnscheck.check = no_queries
        rules = {("DOMAIN-SUFFIX", "gone.example"), ("DOMAIN", "maybe.example"), ("DOMAIN", "keep.example"),
                 ("DOMAIN-KEYWORD", "gone"), ("IP-CIDR", "1.2.3.0/24")}
        kept, summary = build.drop_unresolvable("Ad", rules)
        assert kept == rules - {("DOMAIN-SUFFIX", "gone.example")}, kept
        assert summary == {"queried": 0, "removed": 1}
    print("ok: state, rotation, guard and build integration")


if __name__ == "__main__":
    main()
