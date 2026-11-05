"""Find domains that no longer exist, for rule sets marked 移除无法解析的域名 (Advertising).

Only NXDOMAIN counts as "does not exist": timeouts, SERVFAIL and refusals are treated as
unknown and never lead to removal. An NXDOMAIN answer is confirmed with a second resolver
from a different provider, and a domain is only dropped after two runs in a row found it
missing.

To keep a run to tens of thousands of queries instead of 300k, the state file
(state/dns.tsv: domain, ok|nx, consecutive NXDOMAIN runs) remembers results. Each run checks:
domains not seen before, domains currently NXDOMAIN, and the seventh of the rest whose hash
falls on today (so every domain is rechecked once a week). The file only changes when a
domain's status changes, so the daily git diff stays small.

Standard library only: a minimal DNS client over UDP with asyncio, rate limited.
"""

import asyncio
import hashlib
import random
import struct

# Non-filtering public resolvers, two providers. (Filtering ones like Quad9 answer NXDOMAIN for
# blocked domains, which ad domains often are.)
RESOLVERS = {"google": ["8.8.8.8", "8.8.4.4"], "cloudflare": ["1.1.1.1", "1.0.0.1"]}
QPS = 1200           # total queries per second across all resolvers
IN_FLIGHT = 600      # max outstanding queries
TIMEOUT = 2.5        # seconds per attempt
ATTEMPTS = 3         # tries per domain before giving up as "unknown"
REMOVE_AFTER = 2     # consecutive NXDOMAIN runs before a domain is removed
MAX_NX_RATIO = 0.6   # more NXDOMAIN than this among checked domains = something is wrong; apply nothing
GUARD_MIN = 200      # ...but only judge that ratio when at least this many domains answered


def build_query(txid, name):
    header = struct.pack(">HHHHHH", txid, 0x0100, 1, 0, 0, 0)  # RD set, one question
    qname = b"".join(bytes([len(p)]) + p.encode("ascii") for p in name.split(".")) + b"\x00"
    return header + qname + struct.pack(">HH", 1, 1)  # A, IN


def parse_rcode(data):
    if len(data) < 12:
        return None, None
    txid, flags = struct.unpack(">HH", data[:4])
    return txid, flags & 0x000F  # 0 NOERROR, 2 SERVFAIL, 3 NXDOMAIN, 5 REFUSED


class _Client(asyncio.DatagramProtocol):
    def __init__(self):
        self.waiting = {}
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        txid, rcode = parse_rcode(data)
        fut = self.waiting.pop(txid, None)
        if fut and not fut.done():
            fut.set_result(rcode)

    def error_received(self, exc):  # noqa: D401 - asyncio callback
        pass


class Resolver:
    """Sends A queries to the given servers; resolve(name, provider) -> 'ok' | 'nx' | 'err'."""

    def __init__(self, servers=None, qps=QPS, in_flight=IN_FLIGHT, timeout=TIMEOUT, port=53):
        self.servers = servers or RESOLVERS
        self.qps, self.timeout, self.port = qps, timeout, port
        self.sem = asyncio.Semaphore(in_flight)
        self.clients = {}
        self.next_slot = 0.0
        self.lock = asyncio.Lock()

    async def _client(self, ip):
        if ip not in self.clients:
            loop = asyncio.get_running_loop()
            _, proto = await loop.create_datagram_endpoint(_Client, remote_addr=(ip, self.port))
            self.clients[ip] = proto
        return self.clients[ip]

    async def _pace(self):
        loop = asyncio.get_running_loop()
        async with self.lock:
            now = loop.time()
            slot = max(self.next_slot, now)
            self.next_slot = slot + 1.0 / self.qps
            wait = slot - now
        if wait > 0:
            await asyncio.sleep(wait)

    async def query(self, ip, name):
        client = await self._client(ip)
        loop = asyncio.get_running_loop()
        txid = random.randrange(65536)
        while txid in client.waiting:
            txid = random.randrange(65536)
        fut = loop.create_future()
        client.waiting[txid] = fut
        await self._pace()
        client.transport.sendto(build_query(txid, name))
        try:
            return await asyncio.wait_for(fut, self.timeout)
        except asyncio.TimeoutError:
            client.waiting.pop(txid, None)
            return None

    async def resolve(self, name, provider):
        ips = self.servers[provider]
        async with self.sem:
            for attempt in range(ATTEMPTS):
                rcode = await self.query(ips[attempt % len(ips)], name)
                if rcode == 0:
                    return "ok"
                if rcode == 3:
                    return "nx"
            return "err"

    def close(self):
        for c in self.clients.values():
            c.transport.close()


async def check(names, resolver=None):
    """{name: 'ok' | 'nx' | 'err'}. NXDOMAIN must be confirmed by the other provider."""
    resolver = resolver or Resolver()
    providers = list(resolver.servers)

    async def one(i, name):
        first = providers[i % len(providers)]
        r = await resolver.resolve(name, first)
        if r != "nx":
            return name, r
        second = providers[(i + 1) % len(providers)]
        r2 = await resolver.resolve(name, second)
        return name, ("nx" if r2 == "nx" else "ok" if r2 == "ok" else "err")

    try:
        results = await asyncio.gather(*(one(i, n) for i, n in enumerate(names)))
    finally:
        resolver.close()
    return dict(results)


# ------------------------------------------------------------------ state


def load_state(path):
    state = {}
    if path.exists():
        for line in path.read_text().splitlines():
            if line and not line.startswith("#"):
                name, status, streak = line.split("\t")
                state[name] = (status, int(streak))
    return state


def save_state(path, state):
    lines = ["# domain\tstatus (ok|nx)\tconsecutive NXDOMAIN runs — written by BlackMatrix7Rules/scripts/build.py"]
    lines += [f"{n}\t{s}\t{k}" for n, (s, k) in sorted(state.items())]
    text = "\n".join(lines) + "\n"
    if not path.exists() or path.read_text() != text:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return True
    return False


def bucket(name, buckets=7):
    return int(hashlib.sha1(name.encode()).hexdigest()[:8], 16) % buckets


def due(names, state, day_index):
    """Which names to query this run: new ones, NXDOMAIN ones, and today's seventh of the rest."""
    return sorted(n for n in names if n not in state or state[n][0] == "nx" or bucket(n) == day_index % 7)


def update(state, names, results):
    """Apply query results; returns a summary. Unknown ('err') results leave a domain as it was."""
    checked = [n for n in results if results[n] != "err"]
    nx = [n for n in checked if results[n] == "nx"]
    summary = {"queried": len(results), "answered": len(checked), "nx": len(nx),
               "errors": len(results) - len(checked), "applied": True}
    if len(checked) >= GUARD_MIN and len(nx) / len(checked) > MAX_NX_RATIO:
        summary["applied"] = False  # resolvers misbehaving (or blocked); trust nothing from this run
        return summary
    for n, r in results.items():
        if r == "ok":
            state[n] = ("ok", 0)
        elif r == "nx":
            prev = state.get(n, ("ok", 0))
            state[n] = ("nx", prev[1] + 1 if prev[0] == "nx" else 1)
    for n in list(state):  # forget domains that left the list
        if n not in names:
            del state[n]
    return summary


def dead(state):
    return {n for n, (s, k) in state.items() if s == "nx" and k >= REMOVE_AFTER}
