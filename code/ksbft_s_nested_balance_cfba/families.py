"""families.py (mg-cfba): Nested Balance on the structured extremal families (doc sec. 2).
For each poset: n, range, delta (best pair), deltaN (best NESTED pair), #balanced, #balanced nested,
#non-nested incomparable pairs, flag (NB / NB_FAILS / CEX_1323).  Exact balance tests (nb.c)."""
import random
from fam import parse, fmt, grow, dual, glue, lib7, lt_to_dn, run, rng, connected, is_prime, closure

rows = []
P9 = parse("9 0 0 2 2 3 b 2b 2f 7f")
rows.append(("P9", P9))
rows.append(("rec11 (mg-2912 range-6 record)", parse("11 0 0 2 2 3 b 2b 2f af bf 1ff")))
rows.append(("W8 (Q sec3.5)", parse("8 0 0 0 4 4 6 16 2f")))
for m in (0, 2, 4, 6, 10, 14):
    lo = grow(P9, m, 1)
    rows.append((f"Q_m m={m}", glue(lo, dual(lo), 1)))
B7 = parse("7 0 0 2 2 3 b 2b")
for r in (1, 2, 3):
    rows.append((f"B7+tail(12) r={r}", grow(B7, 12, r)))
for N in (5, 8, 12, 20, 30):
    rows.append((f"Fibonacci F_{N}", lt_to_dn(lib7.fib(N))))
for N, R in ((20, 8), (16, 6), (24, 8)):
    rows.append((f"attach_both(F_{N},{R})", lt_to_dn(lib7.attach_both(N, R))))
for N, R in ((12, 3), (16, 5), (20, 8)):
    rows.append((f"attach_low(F_{N},{R})", lt_to_dn(lib7.attach_low(lib7.fib(N), R))))
two2 = lib7.disjoint_union(lib7.chain(2), lib7.chain(2))
rows.append(("hub(2+2,{0,1,2},8)", lt_to_dn(lib7.hub(two2, [0, 2, 1], 8))))

res = run([d for _, d in rows])
print(f"{'family':34s} {'n':>3s} {'rng':>3s} {'conn':>4s} {'prime':>5s} {'delta':>8s} {'deltaN':>8s} {'#bal':>4s} {'#balN':>5s} {'#nonN':>5s} flag")
bad = 0
for (name, d), r in zip(rows, res):
    pr = is_prime(d) if len(d) <= 30 else None
    print(f"{name:34s} {r['n']:3d} {rng(d):3d} {str(connected(d))[0]:>4s} {str(pr)[0]:>5s} {r['delta']:8.5f} {r['deltaN']:8.5f} {r['nbal']:4d} {r['nbalN']:5d} {r['nnon']:5d} {r['flag']}")
    bad += r["flag"] != "NB"
print(f"named families: {len(rows)} posets, NB failures {bad}")
