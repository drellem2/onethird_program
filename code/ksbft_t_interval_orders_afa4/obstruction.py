"""obstruction.py (mg-afa4): the two n=9 Brightwell obstructions -- per L-step: pair, separators, exact law in P;
and where the poset's balanced pairs actually are."""
from fractions import Fraction as F
from iolib import *
from brightwell import covers, seps
for iv, Lint in [([(1, 1), (1, 2), (1, 5), (2, 3), (2, 6), (3, 4), (4, 5), (5, 6), (6, 6)],
                  [(1, 1), (1, 2), (2, 3), (1, 5), (3, 4), (2, 6), (4, 5), (5, 6), (6, 6)]),
                 ([(1, 1), (1, 2), (2, 3), (2, 6), (3, 4), (4, 5), (5, 6), (6, 7), (7, 7)],
                  [(1, 1), (1, 2), (2, 3), (3, 4), (2, 6), (4, 5), (5, 6), (6, 7), (7, 7)])]:
    L = [iv.index(t) for t in Lint]; C = covers(iv); P, e = prob(iv)
    print(f"P = {iv}   e(P) = {e}   delta = {delta(P)} = {float(delta(P)):.4f}")
    for i in range(len(L) - 1):
        a, b = L[i], L[i + 1]
        if not inc(iv, a, b): print(f"   {iv[a]} < {iv[b]}"); continue
        S = seps(iv, C, a, b)
        print(f"   {iv[a]} || {iv[b]}   separators {[iv[z] for z in S]}   P[a<a'] = {P[(a, b)]} = {float(P[(a, b)]):.4f}")
    bal_ = sorted({(iv[a], iv[b], float(p)) for (a, b), p in P.items() if bal(p) and a < b})
    print("   balanced pairs:", [(x, y, round(p, 4)) for x, y, p in bal_])
