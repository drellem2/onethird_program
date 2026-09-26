"""canon_check.py (audit mg-f4f0): control for eng.canonical and the reason xclimb canonicalises.
(1) fixes every Fishburn representation n<=8; (2) on random representations it preserves the order element by
element and is idempotent; (3) the n=18 'X-local failure' found by an early, non-canonicalising version of
xclimb.py is an ARTIFACT: in canonical form its best slack is -0.288."""
import random
from fractions import Fraction as F
from eng import *
bad = sum(1 for n in range(1, 9) for iv in fishburn(n) if canonical(iv) != sorted(iv))
print('(1) Fishburn reps n<=8 not fixed by canonical():', bad)
rng = random.Random(1); ok = 0
for _ in range(300):
    iv = rand_io(9, 8, 3, rng); c = canonical(iv, keep_order=True)
    ok += rel_from_iv(iv) == rel_from_iv(c) and canonical(c) == sorted(c)
print('(2) random reps: order preserved and idempotent:', ok, '/ 300')
from xclimb import score, TH
import xclimb
P = [(1,1),(1,1),(1,1),(1,1),(1,3),(1,3),(1,4),(1,5),(2,3),(2,8),(3,4),(3,5),(3,6),(4,5),(4,9),(5,6),(6,6),(7,8)]
print('(3) artifact: canonical score =', float(score(P)[0]), score(P)[2])
