"""lcc12.py (audit mg-f4f0): is the X-local failure X12 locally counterexample-compatible (LCC, mg-561a sec 2.1)
on X = {a,a',s,t}, on X u Y (Y = common incomparables of a, a'), and on X u Y u Inc(S)?
LCC on a set U: every incomparable pair in U has law outside [1/3, 2/3]; the >2/3 relation on U is transitive
(a linear order); P[a<a'] > 2/3; and no element of U sits between a and a' in it."""
from fractions import Fraction as F
from itertools import permutations
from eng import *
from xfail import X12, X14

def lcc(iv, cnt, e, U, a, a2):
    U = sorted(set(U)); th = F(1, 3)
    for x in U:
        for y in U:
            if x < y and inc(iv, x, y):
                p = F(cnt[x][y], e)
                if th <= p <= 1 - th: return False, f'balanced pair {iv[x]} {iv[y]} P={p}'
    beats = lambda x, y: lt(iv, x, y) or (inc(iv, x, y) and F(cnt[x][y], e) > F(2, 3))
    # the order: sort by number of elements beaten (tournament) and check transitivity
    order = sorted(U, key=lambda x: -sum(beats(x, y) for y in U))
    for i in range(len(order)):
        for j in range(i + 1, len(order)):
            if not beats(order[i], order[j]): return False, f'not transitive at {iv[order[i]]},{iv[order[j]]}'
    pa, pb = order.index(a), order.index(a2)
    if pb != pa + 1: return False, 'something between a and a\''
    return True, [iv[x] for x in order]

for name, P in (('X12', X12), ('X14', X14)):
    R = rel_from_iv(P); C = covers_rel(R); cnt, e = pair_counts(R); n = len(P)
    for a, a2, s, t in cont_twosep(P, R, C):
        X = [a, a2, s, t]
        Y = [y for y in range(n) if inc(P, y, a) and inc(P, y, a2)]
        IS = [y for y in range(n) if inc(P, y, s) or inc(P, y, t)]
        for lab, U in (('X', X), ('X u Y', X + Y), ('X u Y u Inc(S)', X + Y + IS), ('all of P', range(n))):
            ok, info = lcc(P, cnt, e, U, a, a2)
            print(f'{name}: LCC on {lab:15s} (|U|={len(set(U))}): {ok}  {info}')
