#!/usr/bin/env python3
"""merge.py (mg-eedd): merge the AGG lines of several `onept scan` transcripts (one per stride
class) into one table.  Exact: margins are compared as Fractions."""
import sys
from fractions import Fraction
tot, fails, wm, hist, names, eps = {}, {}, {}, {}, {}, None
R = [0, 0, 0]; md = {}; mc = {}
fail_lines = []
for fn in sys.argv[1:]:
    for line in open(fn):
        if line.startswith('FAIL['):
            fail_lines.append(line.rstrip())
        if not line.startswith('AGG '):
            continue
        t = line.split()
        if t[1] == 'TOT':
            tot[int(t[2])] = tot.get(int(t[2]), 0) + int(t[3])
        elif t[1] == 'FAIL':
            k = (int(t[2]), int(t[3])); fails[k] = fails.get(k, 0) + int(t[4])
        elif t[1] == 'WM':
            p = int(t[2]); f = Fraction(int(t[3]), int(t[4]))
            if p not in wm or f < wm[p][0]:
                wm[p] = (f, ' '.join(t[5:]))
        elif t[1] == 'HIST':
            hist[int(t[2])] = hist.get(int(t[2]), 0) + int(t[3])
        elif t[1] == 'R':
            R = [R[i] + int(t[2 + i]) for i in range(3)]
        elif t[1] == 'MC':
            p = int(t[2]); f = Fraction(int(t[3]), int(t[4])); mc[p] = min(mc.get(p, f), f)
        elif t[1] == 'MD':
            p = int(t[2]); f = Fraction(int(t[3]), int(t[4])); md[p] = max(md.get(p, f), f)
        elif t[1] == 'NAME':
            names[int(t[2])] = ' '.join(t[3:])
        elif t[1] == 'EPS':
            f = Fraction(int(t[2]), int(t[3])); eps = f if eps is None or f > eps else eps
C = sorted(names)
print('non-chains analysed, by range pi:', ' '.join(f'pi={p}:{tot[p]}' for p in sorted(tot)), ' total', sum(tot.values()))
print('%-64s %s' % ('failures of', ' '.join(f'pi={p:<5d}' for p in sorted(tot)) + '  TOTAL'))
for c in C:
    row = [fails.get((p, c), 0) for p in sorted(tot)]
    print('%-64s %s  %d' % (names[c], ' '.join(f'{x:<8d}' for x in row), sum(row)))
print('worst margin by pi (min over P of max over v,pair of min(dist_P, dist_P-v)), exact:')
for p in sorted(wm):
    print(f'  pi={p}: {wm[p][0]} = {float(wm[p][0]):.6f}   at P = {wm[p][1]}')
print('worst margin of the canonical rule, by pi (min over P, over EVERY v of minimal range pi(v), of that v\'s best pair margin):')
for p in sorted(mc):
    print(f'  pi={p}: {mc[p]} = {float(mc[p]):.6f}' + ('   <-- NEGATIVE: some minimal-range v fails' if mc[p] < 0 else ''))
print('number of working v, histogram:', ' '.join(f'{k}:{hist[k]}' for k in sorted(hist)))
print('eps-transport (max over P of min over v, pair balanced in P-v, of dist(p_P, interval)):', eps)
import math
print(f'reweighting lemma R: checks={R[0]} violations={R[1]} (expected 0); control with r=pi(v): violations={R[2]} ' + ('FIRES' if R[2] else 'DOES NOT FIRE'))
for p in sorted(md):
    r = p + 1; b = (math.sqrt(r) - 1) / (math.sqrt(r) + 1)
    print(f'  max |p_P - p_(P-v)| over v with pi(v)={p}: {md[p]} = {float(md[p]):.6f}   bound (sqrt(r)-1)/(sqrt(r)+1) = {b:.6f}')
seen = set()
for l in fail_lines:
    key = l.split(']')[0]
    if sum(1 for s in seen if s[0] == key) < 3 and (key, l) not in seen:
        seen.add((key, l)); print(l)
