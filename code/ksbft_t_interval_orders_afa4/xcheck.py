"""xcheck.py (mg-afa4): iolib.laws vs explicit enumeration of linear extensions; T8/T13/T14 interval-order status."""
import random, itertools, sys
from fractions import Fraction as F
from iolib import *
sys.path.insert(0, '../ksbft_s_nested_balance_cfba')
from io import StringIO

def brute(iv):
    n = len(iv); cnt = {}; e = 0
    for perm in itertools.permutations(range(n)):
        pos = {v: i for i, v in enumerate(perm)}
        if any(lt(iv, a, b) and pos[a] > pos[b] for a in range(n) for b in range(n)): continue
        e += 1
        for a in range(n):
            for b in range(n):
                if inc(iv, a, b) and pos[a] < pos[b]: cnt[(a, b)] = cnt.get((a, b), 0) + 1
    return {k: F(cnt.get(k, 0), e) for k in [(a, b) for a in range(n) for b in range(n) if inc(iv, a, b)]}, e

random.seed(1); bad = 0; tot = 0
for n in range(2, 8):
    L = list(gen(n)); random.shuffle(L)
    for iv in L[:60]:
        P, e = prob(iv); Q, e2 = brute(iv); tot += 1
        if P != Q or e != e2: bad += 1
print(f"xcheck laws vs brute force: {tot} interval orders n=2..7, mismatches = {bad}")
# control: a perturbed engine (drop one ideal term) must mismatch
iv = [(1,1),(1,2),(2,3),(3,3),(1,3)]
P, e = prob(iv); Q, _ = brute(iv)
k = next(iter(P)); P2 = dict(P); P2[k] += F(1, e)
print("CONTROL perturbed law detected:", P2 != Q)

def parse(s):
    t = s.split(); n = int(t[0]); return [int(x, 16) for x in t[1:1 + n]]
def has2p2(dn):
    n = len(dn); L = lambda a, b: dn[b] >> a & 1
    I = lambda a, b: a != b and not L(a, b) and not L(b, a)
    return any(L(a, x) and L(c, y) and I(a, y) and I(c, x) and I(a, c) and I(x, y)
               for a in range(n) for x in range(n) for c in range(n) for y in range(n))
for name, s in [("T8", "8 0 0 2 6 3 e 17 5f"), ("T13", "13 0 1 0 3 5 17 3f b bf 1ff 7f 7ff 47f"),
                ("T14", "14 0 0 153 12 2 1b 3 3b 53 15f 11ff 33ff bb 3ff"), ("N12", "12 0 4 0 6 f 885 6 805 aff 5f 8af 5"),
                ("P9 (control: interval order)", "9 0 0 2 2 3 b 2b 2f 7f")]:
    print(f"{name}: contains induced 2+2 = {has2p2(parse(s))}")
