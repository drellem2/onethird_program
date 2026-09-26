"""report.py -- collate probe summaries into the KSBFT-A tables (mg-2912).

  python3 report.py out/summary_*.txt

Reads only the per-(n, pi) bucket lines probe.cpp prints (exact fractions for
min delta and min M) and merges runs: a bucket (n, pi) that appears in several
runs must agree exactly (it is the same finite set of posets), and the script
REFUSES if two runs disagree.  Buckets are over posets with CONNECTED
incomparability graph; see README for why that loses nothing.
"""
import re
import sys
from fractions import Fraction
from math import sqrt

C = (5 - sqrt(5)) / 10
LINE = re.compile(
    r"^  pi=(\d+) count=(\d+) min_delta=(\d+)/(\d+) \S+ n_delta=1/3:(\d+) min_M=(\d+)/(\d+) \S+ "
    r"min_c=(\S+) min_trip_c=(\S+) viol441=(\d+) trip_viol441=(\d+) not_bft=(\d+) "
    r"with_struct=(\d+) min_struct_c=(\S+)$")
HEAD = re.compile(r"^n=(\d+) posets\(pi<=(\d+)\)=(\d+)")

buckets = {}   # (n, pi) -> dict
complete = {}  # n -> max D such that all pi <= D buckets at n are enumerated
for f in sys.argv[1:]:
    n = D = None
    for line in open(f):
        m = HEAD.match(line)
        if m:
            n, D = int(m.group(1)), int(m.group(2))
            complete[n] = max(complete.get(n, -1), min(D, n))
            continue
        m = LINE.match(line)
        if not m:
            continue
        g = m.groups()
        b = dict(count=int(g[1]), delta=Fraction(int(g[2]), int(g[3])), third=int(g[4]),
                 M=Fraction(int(g[5]), int(g[6])), c=float(g[7]), trip_c=float(g[8]) if g[8] != "NA" else None,
                 viol=int(g[9]), tviol=int(g[10]), notbft=int(g[11]), nstruct=int(g[12]),
                 struct_c=float(g[13]) if g[13] != "NA" else None, src=f)
        key = (n, int(g[0]))
        if key in buckets:
            a = buckets[key]
            same = all(a[k] == b[k] for k in ("count", "delta", "M", "third", "viol", "tviol", "notbft", "nstruct"))
            if not same:
                sys.exit(f"REFUSE: bucket {key} disagrees between {a['src']} and {f}")
        else:
            buckets[key] = b

ns = sorted(complete)
Ds = sorted({pi for (_, pi) in buckets})
print("coverage: n -> largest D with every pi<=D bucket enumerated:",
      ", ".join(f"{n}:{'all' if complete[n] >= n - 1 else complete[n]}" for n in ns))

print("\nTABLE 1  min delta over connected-G posets with pi = D exactly, per n  (EMPIRICAL)")
print("  D \\ n " + "".join(f"{n:>10d}" for n in ns))
for D in Ds:
    row = []
    for n in ns:
        b = buckets.get((n, D))
        row.append(f"{float(b['delta']):10.6f}" if b else (" " * 9 + "." if complete[n] >= D else " " * 9 + "-"))
    print(f"  {D:5d} " + "".join(row))
print("  ('.' = enumerated, no connected-G poset with that range; '-' = not enumerated)")

print("\nTABLE 1b  min delta over pi = D, cumulative over n <= N (exact), and margin above 1/3")
for D in Ds:
    best = None
    for n in ns:
        b = buckets.get((n, D))
        if b and (best is None or b["delta"] < best[0]):
            best = (b["delta"], n)
    maxn = max(n for n in ns if complete[n] >= D)
    print(f"  D={D:2d}: min delta = {best[0]} = {float(best[0]):.6f} at n={best[1]}  "
          f"margin over 1/3 = {float(best[0]) - 1/3:+.6f}  over C_BFT = {float(best[0]) - C:+.6f}  (n <= {maxn})")

print("\nTABLE 2  min M over connected-G posets with pi <= D, per n  (EMPIRICAL)")
print("  D \\ n " + "".join(f"{n:>10d}" for n in ns))
for D in Ds:
    row = []
    for n in ns:
        if complete[n] < min(D, n - 1):
            row.append(" " * 9 + "-")
            continue
        vals = [buckets[(n, p)]["M"] for p in range(D + 1) if (n, p) in buckets]
        row.append(f"{float(min(vals)):10.6f}" if vals else " " * 9 + ".")
    print(f"  {D:5d} " + "".join(row))
allmin = min((b["M"], n, p) for (n, p), b in buckets.items())
print(f"  global min M in the data: {allmin[0]} = {float(allmin[0]):.6f} at n={allmin[1]}, pi={allmin[2]}")

print("\nTABLE 3  Lemma 4.2 numerics  (EMPIRICAL; see README for why the lemma's hypothesis is never met)")
tot = sum(b["count"] for b in buckets.values())
viol = sum(b["viol"] for b in buckets.values())
tviol = sum(b["tviol"] for b in buckets.values())
notbft = sum(b["notbft"] for b in buckets.values())
print(f"  (bucket, poset) records: {tot}   [a poset in two runs is counted twice only if its bucket is]")
print(f"  delta < C_BFT + M^2/441           : {viol}")
print(f"  Lemma-4.1 triple a < C + M^2/441  : {tviol}")
print(f"  posets with a Lemma-4.1 candidate that is NOT a BFT triple (or none): {notbft}")
for D in Ds:
    cs = [(b["c"], n) for (n, p), b in buckets.items() if p == D]
    ts = [(b["trip_c"], n) for (n, p), b in buckets.items() if p == D and b["trip_c"] is not None]
    ss = [(b["struct_c"], n) for (n, p), b in buckets.items() if p == D and b["struct_c"] is not None]
    ns_ = sum(b["nstruct"] for (n, p), b in buckets.items() if p == D)
    print(f"  pi={D:2d}: best c in delta>=C+cM^2: {min(cs)[0]:.6f} (n={min(cs)[1]}); "
          f"Lemma-4.1 triple: {min(ts)[0] if ts else float('nan'):.6f}; "
          f"structured (Lemma 3.2 shape) triples: posets={ns_}, best c={min(ss)[0] if ss else float('nan'):.6f}")
