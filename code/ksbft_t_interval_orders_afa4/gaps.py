"""gaps.py (mg-afa4): are the up-gaps G_up(i) = (r_i, min(r_{i+1}, rho(r_i))] of distinct L-consecutive
incomparable pairs pairwise disjoint when L respects interval dominance?  (and down-gaps dually)
Also verify |S_i| = sum_{p in G_up} alpha(p) + sum_{q in G_dn} beta(q) against the direct separator count."""
import sys
from collections import Counter
from iolib import *
from brightwell import covers, linexts, seps, dominance_ok
def gapdata(iv, L):
    n = len(iv); h = max(r for _, r in iv)
    rho = lambda p: min((r for l, r in iv if l > p), default=h + 1)
    lam = lambda q: max((l for l, r in iv if r < q), default=0)
    out = []
    for i in range(n - 1):
        a, b = L[i], L[i + 1]
        if not inc(iv, a, b): continue
        (la, ra), (lb, rb) = iv[a], iv[b]
        up = set(range(ra + 1, min(rb, rho(ra)) + 1)); dn = set(range(max(la, lam(lb)), lb))
        out.append((i, up, dn))
    return out
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
for n in range(3, NMAX + 1):
    c = Counter(); ex = {}
    for iv in gen(n):
        if all(not inc(iv, a, b) for a in range(n) for b in range(n)): continue
        C = covers(iv); alpha = Counter(l for l, _ in iv); beta = Counter(r for _, r in iv)
        tf_ind = not decomposable(iv) and len(set(iv)) == n
        for L in linexts(iv):
            G = gapdata(iv, L); dom = dominance_ok(iv, L)
            for i, up, dn in G:
                if sum(alpha[p] for p in up) + sum(beta[q] for q in dn) != len(seps(iv, C, L[i], L[i + 1])): c['formula_mismatch'] += 1
            ups = [u for _, u, _ in G]; dns = [d for _, _, d in G]
            disj = lambda S: all(not (S[x] & S[y]) for x in range(len(S)) for y in range(x))
            key = 'dom' if dom else 'nondom'
            c[key] += 1
            if not disj(ups): c[key + '_up_overlap'] += 1; ex.setdefault(key + '_up', (iv, L))
            if not disj(dns): c[key + '_dn_overlap'] += 1; ex.setdefault(key + '_dn', (iv, L))
            if dom and tf_ind:
                c['dom_tf_ind'] += 1
                if not disj(ups) or not disj(dns): c['dom_tf_ind_overlap'] += 1
    print(f"n={n}: {dict(c)}")
    for k, v in ex.items():
        if k.startswith('dom'): print("   ", k, v)
