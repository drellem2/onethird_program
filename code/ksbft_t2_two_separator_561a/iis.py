"""iis.py (mg-561a): extract an irreducible infeasible subsystem (deletion filter) from lpcheck's model for
(O9a, bad L) with tools T1 only and eps fixed to a tiny positive value, and print it in words.
usage: python3 iis.py [O9a|O9b|S10] [T1[,T2,T3]]"""
import sys
from fractions import Fraction as F
from lpcheck import build
import xlp

O = {'O9a': ([(1, 1), (1, 2), (1, 5), (2, 3), (2, 6), (3, 4), (4, 5), (5, 6), (6, 6)],
             [(1, 1), (1, 2), (2, 3), (1, 5), (3, 4), (2, 6), (4, 5), (5, 6), (6, 6)]),
     'O9b': ([(1, 1), (1, 2), (2, 3), (2, 6), (3, 4), (4, 5), (5, 6), (6, 7), (7, 7)],
             [(1, 1), (1, 2), (2, 3), (3, 4), (2, 6), (4, 5), (5, 6), (6, 7), (7, 7)]),
     'S10': ([(1, 1), (1, 2), (1, 6), (2, 3), (2, 7), (3, 4), (4, 5), (5, 6), (6, 7), (7, 7)],   # the n=10 TS-survivor
             [(1, 1), (1, 2), (2, 3), (3, 4), (1, 6), (2, 7), (4, 5), (5, 6), (6, 7), (7, 7)])}
name = sys.argv[1] if len(sys.argv) > 1 else 'O9a'
tools = tuple(sys.argv[2].split(',')) if len(sys.argv) > 2 else ('T1',)
iv, Lint = O[name]; L = [iv.index(t) for t in Lint]
M, eps = build(iv, L, tools)
delta = F(1, 10 ** 6)
rows = M.rows + [({eps: 1}, '>=', delta)]
feas = lambda rs: xlp.solve(M.nv, rs, {})[0] != 'infeasible'
assert not feas(rows), "feasible: nothing to extract"
keep = list(rows)
i = 0
while i < len(keep):
    trial = keep[:i] + keep[i + 1:]
    if not feas(trial): keep = trial
    else: i += 1
print(f"{name}, tools {tools}: irreducible infeasible subsystem of {len(keep)} rows (of {len(rows)}):")
for lin, sense, rhs in keep:
    print("   " + " + ".join(f"{v}*{M.names[k]}" for k, v in lin.items()) + f" {sense} {rhs}")
