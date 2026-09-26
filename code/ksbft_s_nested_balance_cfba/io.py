"""io.py (mg-cfba): which named witnesses are interval orders (no induced 2+2)?  And a positive control."""
from fam import parse, grow, dual, glue, lib7, lt_to_dn, upmasks

def has_2p2(dn):
    n = len(dn); up = upmasks(dn)
    lt = lambda a, b: dn[b] >> a & 1
    inc = lambda a, b: a != b and not lt(a, b) and not lt(b, a)
    for a in range(n):
        for x in range(n):
            if not lt(a, x): continue
            for c in range(n):
                if c in (a, x) or not inc(c, x) or not inc(c, a): continue
                for y in range(n):
                    if y in (a, x, c) or not lt(c, y): continue
                    if inc(a, y) and inc(x, y): return True
    return False

P9 = parse("9 0 0 2 2 3 b 2b 2f 7f")
fams = {"2+2 (control, must be True)": [0, 1, 0, 4], "P9": P9, "rec11": parse("11 0 0 2 2 3 b 2b 2f af bf 1ff"),
        "W8": parse("8 0 0 0 4 4 6 16 2f"), "T8": parse("8 0 0 2 6 3 e 17 5f")}
for m in (0, 4):
    lo = grow(P9, m, 1); fams[f"Q_m m={m}"] = glue(lo, dual(lo), 1)
fams["F_12"] = lt_to_dn(lib7.fib(12)); fams["attach_both(F_20,8)"] = lt_to_dn(lib7.attach_both(20, 8))
fams["attach_low(F_16,5)"] = lt_to_dn(lib7.attach_low(lib7.fib(16), 5))
for k, d in fams.items():
    print(f"{k:30s} contains induced 2+2: {has_2p2(d)}")
