#!/usr/bin/env python3
"""table_base.py (mg-6b81): the delta-1/3 minima table of docs/KSBFT-M-margin-induction.md §1,
read from out_base.txt's '## D=4 n=k' sections (which contain every indecomposable member of Pi_4,
hence of Pi_2 and Pi_3, by Lemma 2.5(c)).  Exact reduced fractions."""
import sys
from fractions import Fraction
sec = None; rows = {}; counts = {}
for line in open(sys.argv[1] if len(sys.argv) > 1 else 'out_base.txt'):
    if line.startswith('## '):
        sec = line.strip()
        continue
    f = line.split()
    if sec and sec.startswith('## D=4 n=') and f[:2] == ['AGG', 'LT']:
        n = int(sec.split('n=')[1]); pi = int(f[2])
        rows[(n, pi)] = Fraction(int(f[5]), int(f[6])); counts[(n, pi)] = int(f[3])
ns = sorted({k[0] for k in rows})
print('| n | #indec (pi=2/3/4) | pi=2 | pi=3 | pi=4 |')
print('|---|---|---|---|---|')
for n in ns:
    c = '/'.join(str(counts.get((n, p), 0)) for p in (2, 3, 4))
    cells = []
    for p in (2, 3, 4):
        v = rows.get((n, p))
        cells.append('–' if v is None else ('%s = %.5f' % (v, float(v))))
    print('| %d | %s | %s |' % (n, c, ' | '.join(cells)))
allv = [(v, k) for k, v in rows.items() if v > 0]
m = min(allv)
print('\nmin over n, pi of the positive entries: %s = %.5f at (n, pi) = %s' % (m[0], float(m[0]), m[1]))
print('zero entries (delta = 1/3 exactly):', [k for k, v in rows.items() if v == 0])
print('negative entries (counterexamples):', [k for k, v in rows.items() if v < 0])
tot = {n: sum(counts.get((n, p), 0) for p in (2, 3, 4)) for n in ns}
print('indecomposable non-chains per n (range <= 4):', tot)
