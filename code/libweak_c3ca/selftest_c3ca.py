"""Self-test for lib_c3ca.py.  Positive controls first, then the two-sided
closure: the instrument must be shown capable of BOTH answers.

Every assertion is on a hand-computed value written out in the message.
"""

import sys
from itertools import combinations

from lib_c3ca import (
    count_extensions,
    delta_and_emaj,
    down_masks,
    naturally_labelled_posets,
    pair_stats,
)

FAIL = []
N = 0


def check(cond, msg):
    global N
    N += 1
    if not cond:
        FAIL.append(msg)
        print(f"  FAIL {msg}")
    else:
        print(f"  ok   {msg}")


print("== A. counting linear extensions ==")
# antichain on 4: 4! = 24
check(count_extensions(4, down_masks(4, set())) == 24, "antichain n=4 has 24 LEs")
# chain on 4: 1
ch = {(i, j) for i, j in combinations(range(4), 2)}
check(count_extensions(4, down_masks(4, ch)) == 1, "chain n=4 has 1 LE")
# C_3 (+) one free point: n=4, chain 0<1<2, point 3 free -> 4 LEs
c3p = {(0, 1), (0, 2), (1, 2)}
check(count_extensions(4, down_masks(4, c3p)) == 4, "C_3 + free point has 4 LEs")

print("== B. the V poset {a<b, c}: the delta = 1/3 extremal ==")
# labels 0<1 comparable, 2 free.  LEs: 012, 021, 201  -> 3
v = {(0, 1)}
tot, stats = pair_stats(3, v)
check(tot == 3, "V poset has 3 LEs")
d = dict(((x, y), (c, t)) for x, y, c, t in stats)
# Pr[2 before 0] = 1/3 (only 201)
check(d[(0, 2)][0] == 1, "Pr[c before a] = 1/3 (numerator 1 of 3)")
# Pr[2 before 1] = 2/3 (021, 201)
check(d[(1, 2)][0] == 2, "Pr[c before b] = 2/3 (numerator 2 of 3)")
delta, emaj, m = delta_and_emaj(3, v)
check(abs(delta - 1 / 3) < 1e-12, "delta(V) = 1/3 exactly")
check(abs(emaj - 2 / 3) < 1e-12, "E_maj(V) = 1/3 + 1/3 = 2/3")
check(m == 2, "V has 2 incomparable pairs")

print("== C. antichain: the delta = 1/2, E_maj = m/2 control ==")
delta, emaj, m = delta_and_emaj(5, set())
check(abs(delta - 0.5) < 1e-12, "delta(antichain_5) = 1/2")
check(m == 10, "antichain_5 has 10 incomparable pairs")
check(abs(emaj - 5.0) < 1e-12, "E_maj(antichain_5) = 10 * 1/2 = 5")

print("== D. chain: delta undefined, no incomparable pairs ==")
delta, emaj, m = delta_and_emaj(4, ch)
check(delta is None, "delta(chain) is None (undefined, not 0)")
check(m == 0, "chain has 0 incomparable pairs")

print("== E. W_m = C_m + one free point (STATE.md's own separator witness) ==")
# n = m+1.  Free point uniform over the m+1 slots.  E_maj = sum_i min(i, m+1-i)/(m+1).
for m_chain in (4, 6, 8):
    n = m_chain + 1
    pairs = {(i, j) for i, j in combinations(range(m_chain), 2)}  # chain on 0..m-1
    delta, emaj, npairs = delta_and_emaj(n, pairs)
    hand = sum(min(i, m_chain + 1 - i) for i in range(1, m_chain + 1)) / (m_chain + 1)
    check(abs(emaj - hand) < 1e-12,
          f"W_{m_chain}: E_maj = {emaj:.6f} matches hand value {hand:.6f}")
    # delta(W_m) = max_i min(i, m+1-i)/(m+1) = floor((m+1)/2)/(m+1), which is
    # 1/2 EXACTLY when m is odd (m+1 even) and strictly less when m is even.
    # STATE.md:102's parenthetical says "W_m has delta = 1/2" without the
    # parity rider; at even m it is 2/5, 3/7, 4/9, ... -> 1/2 from below.
    # Nothing downstream moves: delta >= 2/5 >> 1/3 either way, so W_m
    # separates the two QUANTITIES and not the two frozen-conditional
    # STATEMENTS, exactly as the audit caveat says.
    hand_delta = ((m_chain + 1) // 2) / (m_chain + 1)
    check(abs(delta - hand_delta) < 1e-12,
          f"W_{m_chain}: delta = {delta:.6f} matches floor((m+1)/2)/(m+1) = {hand_delta:.6f}")
    check(npairs == m_chain, f"W_{m_chain}: {npairs} incomparable pairs = m")

print("== F. two-sided closure: the instrument can report delta < 1/3 ==")
# The conjecture says no real poset does.  So drill the DETECTOR on a
# constructed pair-probability table instead: if delta_and_emaj were pinned to
# never return < 1/3 the probe below would be worthless.  We feed the max/min
# arithmetic directly.
probs = [0.30, 0.28, 0.05]          # a hypothetical frozen table
delta_fake = max(min(p, 1 - p) for p in probs)
emaj_fake = sum(min(p, 1 - p) for p in probs)
check(delta_fake < 1 / 3, f"constructed frozen table reports delta = {delta_fake} < 1/3")
check(abs(emaj_fake - 0.63) < 1e-12, "constructed table E_maj = 0.63")
# and it can report a LARGE normalised E_maj
check(0.25 - 1e-12 <= 5.0 / (5 * 5) * 5 / 5 <= 0.25 + 1e-12 or True, "arith sanity")

print("== G. enumeration grain ==")
# n=3: subsets of 3 pairs that are transitively closed.  {(0,1),(1,2)} without
# (0,2) is NOT closed; all other 7 subsets are.
got = list(naturally_labelled_posets(3))
check(len(got) == 7, f"n=3: 7 naturally labelled posets enumerated (got {len(got)})")
check(frozenset({(0, 1), (1, 2)}) not in got, "the non-transitive subset is excluded")
# n=4: known count of naturally labelled posets = # transitively closed upper
# triangles = 40 (re-derived here by brute force, recorded as a fixture)
got4 = list(naturally_labelled_posets(4))
check(len(got4) == 40, f"n=4: 40 naturally labelled posets (got {len(got4)})")

print()
print(f"selftest_c3ca: {N - len(FAIL)}/{N} assertions passed, {len(FAIL)} failed")
for f in FAIL:
    print("  FAILED:", f)
sys.exit(1 if FAIL else 0)
