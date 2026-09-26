"""show.py (mg-5f14): human-readable dump of one poset (hex down-masks as in pcert files):
covers, minimal/maximal elements with position laws, every incomparable pair's P[x before y]."""
import sys
from fractions import Fraction
from probe import analyse, dual, inc


def show(tokens):
    n, dn = int(tokens[0]), [int(t, 16) for t in tokens[1:]]
    up = dual(dn)
    e, B, pos, _ = analyse(dn)
    cov = [(u, v) for v in range(n) for u in range(n) if dn[v] >> u & 1 and not any(dn[v] >> w & 1 and dn[w] >> u & 1 for w in range(n))]
    print("P =", " ".join(tokens), " e =", e)
    print("  covers:", " ".join(f"{u}<{v}" for u, v in cov))
    for x in range(n):
        if dn[x] == 0:
            print(f"  min {x}: Inc={[y for y in range(n) if inc(dn, up, x, y)]} pos law", [str(Fraction(c, e)) for c in pos[x] if True][:6])
    for x in range(n):
        if up[x] == 0:
            print(f"  max {x}: Inc={[y for y in range(n) if inc(dn, up, x, y)]} pos-from-top law", [str(Fraction(pos[x][n - 1 - j], e)) for j in range(6)])
    for x in range(n):
        for y in range(x + 1, n):
            if inc(dn, up, x, y):
                p = Fraction(B[x][y], e)
                print(f"  P[{x}<{y}] = {p} {'BAL' if Fraction(1,3) <= p <= Fraction(2,3) else ''}")


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        show(arg.split())
