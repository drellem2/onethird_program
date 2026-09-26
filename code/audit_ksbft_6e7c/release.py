"""release.py (audit mg-6e7c): Lemma 1.3 of mg-ce69 by explicit enumeration: for every element u, the law of
f(u) - rho(u), rho(u) = max_{w<u} f(w) (0 if u minimal), is non-increasing.  Control: measured from
min_{w<u} f(w) instead (must produce violations).  Every connected poset in the files."""
import sys
from aud import close, conn, brute
viol = ctrl = elems = 0
for f in sys.argv[1:]:
    for line in open(f):
        a = line.split(); n = int(a[0])
        if n < 2: continue
        dn = close([int(t, 16) for t in a[1:1 + n]])
        if not conn(dn): continue
        L = brute(dn)
        for u in range(n):
            elems += 1
            h1 = [0] * (n + 1); h2 = [0] * (n + 1)
            for l in L:
                p = {x: i + 1 for i, x in enumerate(l)}
                below = [p[w] for w in range(n) if dn[u] >> w & 1]
                h1[p[u] - (max(below) if below else 0)] += 1
                h2[p[u] - (min(below) if below else 0)] += 1
            if any(h1[j + 1] > h1[j] for j in range(1, n)): viol += 1
            if any(h2[j + 1] > h2[j] for j in range(1, n)): ctrl += 1
print(f"elements={elems} violations={viol} control_violations={ctrl}", "OK" if viol == 0 and ctrl > 0 else "BAD")
