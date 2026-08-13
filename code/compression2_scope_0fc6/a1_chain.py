"""a1 — IS THE NOTE'S CHAIN CORRECT?  Every boxed claim of compression2.tex, on real posets.

Checked here, in the note's own order:

  (losslessness, line 32)   L  <->  (W_B)                        — a BIJECTION, forgets nothing
  (2, line 49)              inv_{L*}(L) = sum_B K_B
  (3, line 62)              K_B = sum_t d_t(W_B)
  (4, line 78)              E K_B <= m^2/3   under hypothesis (1)
  (5, line 100)             the entropy lemma, against the exact per-node entropy
  (6, line 153)             log2 e(P) <= (1 - 1/(24 ln2)) n log2 n

Hypothesis (1) — `Pr[v_j <_L v_i] <= 1/3 for every i<j` against a coherent distinguished
extension `L*` — is the note's standing assumption.  It is NOT satisfied by most posets, so the
population is split: the identities are checked EVERYWHERE (they are unconditional), and the
inequalities are checked on the subpopulation where (1) actually holds.
"""
import sys
from fractions import Fraction

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import lib0fc6 as L  # noqa: E402

# --------------------------------------------------------------- (losslessness), (2), (3)

L.banner("a1.1  the merge encoding is a BIJECTION, and (2) and (3) are identities")
tot_le = 0
tot_nodes = 0
for n in (2, 3, 4, 5):
    posets = L.all_posets(n)
    nodes = L.dyadic_nodes(n)
    ok_bij = ok_2 = ok_3 = True
    seen_words_collision = 0
    cnt = 0
    for lt in posets:
        LEs = L.linear_extensions(n, lt)
        star = LEs[0]  # ANY linear extension serves as L* for the identities (they are
        # unconditional in L*); the coherent one is used for the inequalities below.
        seen = {}
        for Lx in LEs:
            W = L.merge_words(Lx, star, nodes)
            if W in seen:
                seen_words_collision += 1
            seen[W] = Lx
            if L.decode_merge_words(W, star, nodes) != Lx:
                ok_bij = False
            if L.inv_against(Lx, star) != sum(L.word_inv(w) for w in W):
                ok_2 = False
            for w in W:
                if L.word_inv(w) != L.word_prefix_area(w):
                    ok_3 = False
            cnt += 1
            tot_nodes += len(W)
    tot_le += cnt
    L.verdict(ok_bij and seen_words_collision == 0,
              f"n={n}: L <-> (W_B) is a bijection on every L(P)",
              f"{len(posets)} posets, {cnt} extensions, {seen_words_collision} collisions")
    L.verdict(ok_2, f"n={n}: (2)  inv_L*(L) = sum_B K_B", f"{cnt} extensions")
    L.verdict(ok_3, f"n={n}: (3)  K_B = sum_t d_t(W_B)", f"{tot_nodes} node-words so far")

# the ANTICHAIN at n = 6, 7, 8 carries EVERY merge-word structure at those sizes (all n!
# orders), which is what the identities are about; exhaustive posets at n >= 6 buy nothing
# extra for an unconditional identity and cost minutes.
for n in (6, 7, 8):
    nodes = L.dyadic_nodes(n)
    lt = L.antichain(n)
    LEs = L.linear_extensions(n, lt)
    star = tuple(range(n))
    ok_bij = ok_2 = ok_3 = True
    seen = set()
    for Lx in LEs:
        W = L.merge_words(Lx, star, nodes)
        if W in seen:
            ok_bij = False
        seen.add(W)
        if L.decode_merge_words(W, star, nodes) != Lx:
            ok_bij = False
        if L.inv_against(Lx, star) != sum(L.word_inv(w) for w in W):
            ok_2 = False
        for w in W:
            if L.word_inv(w) != L.word_prefix_area(w):
                ok_3 = False
        tot_nodes += len(W)
    tot_le += len(LEs)
    L.verdict(ok_bij, f"n={n} (antichain, all {len(LEs)} orders): bijection")
    L.verdict(ok_2, f"n={n} (antichain, all {len(LEs)} orders): (2)")
    L.verdict(ok_3, f"n={n} (antichain, all {len(LEs)} orders): (3)")

print()
print(f"       [scope] {tot_le} linear extensions (all labelled posets n <= 5, plus every "
      f"order at n = 6,7,8); {tot_nodes} node-words.")
print("       [note] BIJECTION, not compression: (W_B) determines L and L determines (W_B).")
print("              compression2's 'compression' FORGETS NOTHING.  It is a re-coordinatisation")
print("              (merge sort's recording tape) plus an entropy estimate — a different KIND")
print("              of object from compression.tex's C_o, which is a genuine quotient map.")

# --------------------------------------------------------------- the hypothesis population

L.banner("a1.2  WHICH POSETS SATISFY HYPOTHESIS (1)?")
pop = {}
for n in (3, 4, 5):
    posets = L.all_posets(n)
    good = []
    for lt in posets:
        LEs = L.linear_extensions(n, lt)
        if len(LEs) == 1:
            continue  # a chain: (1) holds vacuously, and the note is about counterexamples
        star = L.coherent_order(LEs, n)
        if star is None:
            continue
        pp = L.pair_probs(LEs, n)
        if L.max_flip_against(pp, star) <= Fraction(1, 3):
            good.append((lt, LEs, star))
    pop[n] = good
    dmin = None
    for lt, LEs, star in good:
        d = L.delta(LEs, n, lt)
        if d is not None:
            dmin = d if dmin is None else min(dmin, d)
    print(f"  n={n}: {len(good):5d} of {len(posets):5d} non-chain posets satisfy (1)"
          f"   (min delta over them: {dmin})")
print()
print("       [note] every member has delta(P) <= 1/3, i.e. every member is AT OR BELOW the")
print("              1/3-2/3 boundary.  A poset with delta > 1/3 cannot satisfy (1), so the")
print("              hypothesis population IS the boundary-and-below class this corpus already")
print("              studies (docs/FACTS.md F19, mg-6ff4).")

# --------------------------------------------------------------- (4)

L.banner("a1.3  (4)  E K_B <= m^2/3 on the hypothesis population")
for n in (3, 4, 5):
    nodes = L.dyadic_nodes(n)
    bad = 0
    checked = 0
    worst_ratio = 0.0
    for lt, LEs, star in pop[n]:
        N = len(LEs)
        for (lo, mid, hi) in nodes:
            m = mid - lo
            mm = hi - mid
            tot = 0
            for Lx in LEs:
                W = L.merge_words(Lx, star, [(lo, mid, hi)])
                tot += L.word_inv(W[0])
            EK = Fraction(tot, N)
            cap = Fraction(m * mm, 3)
            checked += 1
            if EK > cap:
                bad += 1
            if cap > 0:
                worst_ratio = max(worst_ratio, float(EK / cap))
    L.verdict(bad == 0, f"n={n}: E K_B <= |A||C|/3 at every node of every member",
              f"{checked} node-instances, {bad} violations, worst E K_B / cap = {worst_ratio:.4f}")

# --------------------------------------------------------------- (5)

L.banner("a1.4  (5)  the entropy lemma, against the EXACT per-node entropy")
for n in (3, 4, 5):
    nodes = L.dyadic_nodes(n)
    bad = 0
    checked = 0
    for lt, LEs, star in pop[n]:
        N = len(LEs)
        for nd in nodes:
            (lo, mid, hi) = nd
            m = mid - lo
            if m != hi - mid:
                continue  # (5) is stated for BALANCED nodes
            dist = {}
            for Lx in LEs:
                w = L.merge_words(Lx, star, [nd])[0]
                dist[w] = dist.get(w, 0) + 1
            H = L.entropy_bits([Fraction(v, N) for v in dist.values()])
            checked += 1
            if H > L.note_word_bound(m) + 1e-12:
                bad += 1
    L.verdict(bad == 0, f"n={n}: H(W_B) <= 2m - m^3/(3 ln2 (4m^2-1)) at every balanced node",
              f"{checked} balanced-node instances, {bad} violations")

print()
print("       [scope] the lemma is TRUE here but is NOT TIGHT at these block sizes: a0.7")
print("               measures that the note's per-node bound is WEAKER than the free bound")
print("               log2 C(2m,m) for every m < 27, i.e. for every block of fewer than 54")
print("               elements it says less than 'the word is a word'.")

# --------------------------------------------------------------- (6)

L.banner("a1.5  (6)  log2 e(P) <= 0.9399 n log2 n on the hypothesis population")
for n in (3, 4, 5):
    bad = 0
    slack = None
    for lt, LEs, star in pop[n]:
        lhs = __import__("math").log2(len(LEs))
        rhs = L.note_headline_bound(n)
        if lhs > rhs + 1e-12:
            bad += 1
        s = rhs - lhs
        slack = s if slack is None else min(slack, s)
    L.verdict(bad == 0, f"n={n}: (6) holds on every member", f"{len(pop[n])} members, "
              f"{bad} violations, min slack {slack:.3f} bits")

L.banner("a1.6  BUT WHERE DOES (6) FIRST BEAT THE FREE BOUND e(P) <= n! ?")
import math  # noqa: E402
def bites(n):
    return L.note_headline_bound(n) < L.log2_factorial(n)


lo, hi = 2, 2
while not bites(hi):
    hi *= 2
    if hi > 10 ** 12:
        break
while lo + 1 < hi:
    mid = (lo + hi) // 2
    if bites(mid):
        hi = mid
    else:
        lo = mid
cross = hi
print(f"  first n with 0.9399 n log2 n  <  log2 n!  :  n = {cross}   (binary search; "
      f"bites({cross}) = {bites(cross)}, bites({cross-1}) = {bites(cross-1)})")
for n in (10, 100, 1000, 10 ** 4, 10 ** 6, 10 ** 7, 10 ** 8):
    b = L.note_headline_bound(n)
    f = L.log2_factorial(n)
    print(f"    n = {n:>10}:  note bound {b:>16.1f}   log2 n! {f:>16.1f}   "
          f"{'BOUND BITES' if b < f else 'weaker than n!'}")
L.verdict(cross is not None and cross > 10 ** 6,
          "(6) is NUMERICALLY VACUOUS below a crossover above 10^6",
          f"crossover n = {cross}")

sys.exit(L.finish())
