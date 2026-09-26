"""kc_ctl.py (audit mg-f4f0): pipeline-level positive control for kc.py's K_C search: the SAME generator and DFS,
with pattern (iii) NOT forbidden, must find dominance-respecting L that avoid (i) and (ii) (the mg-561a staircase
survivor phenomenon); each found L is then checked to contain (iii), i.e. K_C still holds on it."""
import random, time, sys
from eng import *
from kc import search_bad, K
rng = random.Random(99); T = float(sys.argv[1]); t0 = time.time(); seen = set(); found = 0; with_iii = 0; ex = None
while time.time() - t0 < T:
    n = rng.randint(11, 14); m = rng.randint(n - 5, n - 2); iv = [(i, i + 1) for i in range(1, m)] + [(1, 1), (m, m)]
    while len(iv) < n:
        l = rng.randint(1, m); r = min(m, l + rng.choice([0, 1, 2, 3, 4, 5])); iv.append((l, r))
    iv = canonical(iv); key = tuple(iv)
    if key in seen: continue
    seen.add(key)
    nl, bad, tr = search_bad(iv, use_iii=False)
    for L in bad:
        found += 1; pt = K(iv).pat(list(L)); with_iii += 'iii' in pt; ex = ex or (iv, [iv[x] for x in L], pt)
print(f'{len(seen)} distinct posets, {T:.0f}s: L avoiding (i),(ii) found with (iii) allowed: {found} -> control {"FIRES" if found else "DOES NOT FIRE"}; '
      f'of them containing (iii): {with_iii} (K_C holds on each: {with_iii == found})')
if ex: print('   example:', ex)
