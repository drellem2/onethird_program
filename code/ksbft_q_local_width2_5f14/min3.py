"""min3.py (mg-5f14): the candidate 'three minimal elements => a balanced pair among the minimal
elements' (EMPIRICAL probe).  For every indecomposable P with >= 3 minimal elements and NO balanced
pair among its minimal elements, print a histogram by (range, n - range, has an element comparable
to nothing).  n - range small means some element is incomparable to almost everything."""
import sys
from fractions import Fraction
from probe import analyse, dual, inc, connected, balanced

for f in sys.argv[1:]:
    hist = {}
    wit = {}
    tot = 0
    for line in open(f):
        a = line.split()
        n, dn = int(a[0]), [int(t, 16) for t in a[1:]]
        up = dual(dn)
        mins = [x for x in range(n) if dn[x] == 0]
        if len(mins) < 3 or not connected(n, dn, up):
            continue
        tot += 1
        e, B, pos, _ = analyse(dn)
        if any(balanced(Fraction(B[x][y], e)) for x in mins for y in mins if x < y):
            continue
        rng = max(sum(inc(dn, up, x, y) for y in range(n)) for x in range(n))
        iso = any(dn[x] == 0 and up[x] == 0 for x in range(n))
        k = (rng, n - rng, iso)
        hist[k] = hist.get(k, 0) + 1
        wit.setdefault(k, " ".join(a))
    print("== file", f.split("/")[-1], "indecomposable with >=3 minimal:", tot)
    for k in sorted(hist):
        print("AGG no-balanced-minimal-pair range %d n-range %d isolated %s : %d   e.g. %s" % (k[0], k[1], k[2], hist[k], wit[k]))
