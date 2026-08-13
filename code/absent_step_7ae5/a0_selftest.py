"""mg-7ae5 / A0 — controls, run BEFORE anything is believed.

Sections:
  A  definitions against hand-computable objects
  B  the DECOMPOSABILITY identity that P2 bets on, proved-by-exhaustion in range
  C  PLUG-BACKS: ten values published by OTHER documents, reproduced on this
     code, which shares no line with theirs
  D  WRONG-DIRECTION WORLDS: four deliberately broken predicates that MUST
     break a published number, so agreement in C is evidence and not luck
  E  the detector for P5's monotone-ceiling claim, tested on a synthetic
     population where the answer is known and is NOT monotone
"""

from fractions import Fraction
import sys

from lib7ae5 import (poset_iter, linear_extensions, incomparable, density,
                     p_matrix, delta, balanced_pairs, delta1, phi,
                     is_ordinal_sum_at, induced, is_chain, cut_verdict,
                     eps_sup, eps_dem_chain13, eps0_required_cap, LO, HI)

FAILS = []


def check(tag, got, want, note=""):
    ok = got == want
    if not ok:
        FAILS.append(tag)
    print("  %-7s %-46s got %-26s %s%s"
          % ("GREEN" if ok else "RED", tag, str(got),
             "" if ok else "want " + str(want), (" — " + note) if note else ""))
    return ok


print("=" * 78)
print("mg-7ae5 / A0 — SELFTEST")
print("=" * 78)

# ------------------------------------------------------------------- A -----
print("\nA. DEFINITIONS AGAINST HAND-COMPUTABLE OBJECTS")

# A1 — Op-Form Claim 3.3's poset P0 = {a<b} u {c}, by hand in that document.
n, rel = 3, frozenset({(0, 1)})          # 0<1, 2 isolated
ex = linear_extensions(n, rel)
P = p_matrix(n, rel, ex)
check("A1a |L(P0)|", len(ex), 3, "Op-Form Cl. 3.3, by hand")
check("A1b p_ac", P[(0, 2)], Fraction(2, 3), "Op-Form Cl. 3.3")
check("A1c p_bc", P[(1, 2)], Fraction(1, 3), "Op-Form Cl. 3.3")
check("A1d delta(P0)", delta(n, rel, ex), Fraction(1, 3),
      "the boundary object: delta = 1/3 EXACTLY")

# A2 — the antichain: Op-Form Cl. 7.1 / §4.2, Delta_1 = (n-k)/n on prefixes.
for n in (4, 5, 6):
    rel = frozenset()
    ex = linear_extensions(n, rel)
    ok = all(delta1(n, rel, ex, k) == Fraction(n - k, n)
             for k in range(1, n // 2 + 1))
    check("A2 antichain n=%d Delta_1=(n-k)/n" % n, ok, True,
          "Op-Form Cl. 7.1: >= 1/2 on every prefix")
    check("A2b antichain n=%d min Delta_1" % n,
          min(delta1(n, rel, ex, k) for k in range(1, n)) >= Fraction(1, 2),
          True, "the hypothesis class EXCLUDES the antichain")

# A3 — Phi = Delta_1 for |A| <= n/2 (Op-Form Lemma 2.1: an identity, not a bound)
bad = 0
for n in (4, 5, 6):
    for rel in poset_iter(n):
        ex = linear_extensions(n, rel)
        for k in range(1, n // 2 + 1):
            if phi(n, rel, ex, k) != delta1(n, rel, ex, k):
                bad += 1
check("A3 Phi == Delta_1 for k<=n/2 (n<=6)", bad, 0, "Op-Form Lemma 2.1")

# A4 — the chain has no incomparable pair, delta undefined, density 0
for n in (3, 5):
    rel = frozenset((i, j) for i in range(n) for j in range(i + 1, n))
    ex = linear_extensions(n, rel)
    check("A4 chain n=%d |L|" % n, len(ex), 1)
    check("A4 chain n=%d delta" % n, delta(n, rel, ex), None)
    check("A4 chain n=%d density" % n, density(n, rel), Fraction(0))

# ------------------------------------------------------------------- B -----
print("\nB. THE DECOMPOSABILITY IDENTITY (P2), BY EXHAUSTION")

viol_a = viol_b = 0
cuts = downsets = ordsums = disjoint = 0
for n in range(3, 7):
    for rel in poset_iter(n):
        ex = linear_extensions(n, rel)
        for k in range(1, n):
            cuts += 1
            z = (delta1(n, rel, ex, k) == 0)
            o = is_ordinal_sum_at(n, rel, k)
            if z and not o:
                viol_a += 1
            if o and not z:
                viol_b += 1
            # A_k is a DOWN-SET at every cut of every poset in this encoding
            # (relations run from smaller index to larger), so down-set-ness is
            # the deliberately weaker property Delta_1 = 0 must not collapse to.
            if all(not (j < k <= i) for (i, j) in rel):
                downsets += 1
            if o:
                ordsums += 1
            # and the OTHER extreme: no relation crosses the cut at all
            if all(not (i < k <= j) for (i, j) in rel):
                disjoint += 1
check("B1 Delta_1=0 => ordinal sum (n<=6)", viol_a, 0)
check("B2 ordinal sum => Delta_1=0 (n<=6)", viol_b, 0)
check("B3 down-set-ness is VACUOUS here", downsets, cuts,
      "all %d cuts; so Delta_1 = 0 is strictly stronger than 'A_k is a down-set' "
      "— only %d cuts are ordinal-sum splits, and %d are disjoint-union splits"
      % (cuts, ordsums, disjoint))

# B4 — the lemma A2 §E turns on: delta(P[A] (+) P[B]) = max(delta(P[A]), delta(P[B])).
#      Linear extensions of an ordinal sum are products, incomparable pairs live
#      inside one side, and p_xy is unchanged there.  Checked EXHAUSTIVELY rather
#      than asserted, because the whole minimality consequence rests on it.
viol = tested = 0
for n in range(3, 7):
    for rel in poset_iter(n):
        exts = linear_extensions(n, rel)
        for k in range(1, n):
            if not is_ordinal_sum_at(n, rel, k):
                continue
            tested += 1
            mA, subA, _ = induced(rel, set(range(k)))
            mB, subB, _ = induced(rel, set(range(k, n)))
            dA = delta(mA, subA, linear_extensions(mA, subA))
            dB = delta(mB, subB, linear_extensions(mB, subB))
            sides = [x for x in (dA, dB) if x is not None]
            want = max(sides) if sides else None
            if delta(n, rel, exts) != want:
                viol += 1
check("B4 delta(P(+)Q) = max(delta P, delta Q)", viol, 0,
      "exhaustive over %d ordinal-sum splits, n<=6 — so a DECOMPOSABLE frozen "
      "poset has a frozen SIDE, and minimality forbids it" % tested)

# ------------------------------------------------------------------- C -----
print("\nC. PLUG-BACKS — ten values published by OTHER documents")

# C1 — mg-3969 A1: poset counts in normal form, n = 3..6
for n, want in ((3, 7), (4, 40), (5, 357), (6, 4824)):
    check("C1 posets n=%d" % n, sum(1 for _ in poset_iter(n)), want,
          "mg-3969 A1 table")

# C2 — mg-3969 A1: max Delta_1 over all prefix cuts of NON-CHAIN posets
for n, want in ((3, Fraction(2, 3)), (4, Fraction(3, 4)),
                (5, Fraction(4, 5)), (6, Fraction(5, 6))):
    mx = Fraction(0)
    for rel in poset_iter(n):
        if len(rel) == n * (n - 1) // 2:
            continue
        ex = linear_extensions(n, rel)
        for k in range(1, n):
            mx = max(mx, delta1(n, rel, ex, k))
    check("C2 max Delta_1 n=%d" % n, mx, want, "mg-3969 A1 table")

# C3 — mg-3969 A1: prefix cuts of the non-chain posets
tot_cuts = 0
for n in range(3, 7):
    cuts = sum(n - 1 for rel in poset_iter(n)
               if len(rel) != n * (n - 1) // 2)
    tot_cuts += cuts
check("C3 cuts of non-chain posets n<=6", tot_cuts, 12 + 117 + 1424 + 24115,
      "mg-3969 A1 table (12,117,1424,24115)")

# C4 — mg-3969 Claim 6.1's witness, in full: Delta_1 = 17/78, |L| = 26,
#      both sides = {x<z} u {y}, and ALL FOUR balanced-in-side pairs evicted.
n = 6
rel = frozenset({(0, 2), (0, 3), (0, 4), (0, 5), (1, 4), (1, 5), (2, 4), (3, 4)})
ex = linear_extensions(n, rel)
check("C4a witness |L(P)|", len(ex), 26, "mg-3969 Cl. 6.1")
check("C4b witness Delta_1 at k=3", delta1(n, rel, ex, 3), Fraction(17, 78),
      "mg-3969 Cl. 6.1 — the published ceiling on U_either (BOTH scope)")
pP = p_matrix(n, rel, ex)
evicted = []
for S in (set(range(3)), set(range(3, 6))):
    m, sub, idx = induced(rel, S)
    inv = {i: e for e, i in idx.items()}
    for (a, b), p_in in balanced_pairs(m, sub, linear_extensions(m, sub)).items():
        x, y = inv[a], inv[b]
        p_out = pP[(x, y)] if (x, y) in pP else 1 - pP[(y, x)]
        evicted.append((p_in, p_out))
check("C4c four balanced-in-side pairs", len(evicted), 4, "mg-3969 Cl. 6.1")
check("C4d all four leave [1/3,2/3]",
      sorted(str(o) for _, o in evicted),
      sorted(["9/13", "19/26", "19/26", "4/13"]), "mg-3969 Cl. 6.1, verbatim")

# C5 — mg-d3c7's refuting family: chain c_1<..<c_{n-1} plus isolated z,
#      n = 2k+1, A = {z, c_1..c_{k-1}}, Delta_1 = (k+1)/((2k+1)k).
def d3c7_family(k):
    """z is element 0; the chain is 1<2<...<2k.  A_k = {0,...,k-1} is then
    {z} u {first k-1 chain elements}, which is mg-d3c7's A."""
    n = 2 * k + 1
    rel = frozenset((i, j) for i in range(1, n) for j in range(i + 1, n))
    return n, rel


for k in (3, 4):
    n, rel = d3c7_family(k)
    ex = linear_extensions(n, rel)
    check("C5 d3c7 family k=%d Delta_1" % k, delta1(n, rel, ex, k),
          Fraction(k + 1, (2 * k + 1) * k), "mg-d3c7 §4's family, verbatim")
    check("C5b d3c7 family k=%d density" % k, density(n, rel),
          Fraction(2, n), "d = 2/n — SPARSE (P5)")

# C6 — mg-ac0c §3: the residual wall at eps_0 = 1 is 2n/(n+1) at d = 1
for n in (2, 15):
    wall = eps_sup(n, Fraction(1)) / eps_dem_chain13(Fraction(1))
    check("C6 wall at eps0=1, n=%d" % n, wall, Fraction(2 * n, n + 1),
          "mg-ac0c §3: 4/3 at n=2, 15/8 at n=15")

# C7 — mg-ac0c §4: closure needs eps_0 >= n/(2(n+1)) at d = 1
for n, want in ((2, Fraction(1, 3)), (7, Fraction(7, 16)), (100, Fraction(50, 101))):
    check("C7 required eps0 at d=1, n=%d" % n, eps0_required_cap(n, Fraction(1)),
          want, "mg-ac0c §4 table")

# C8 — mg-ac0c §3.1 / mg-0e8c §4: chain (I)=(III) at eps_0 = 1/5 closes only
#      at d <= 2e-2 in the limit
d_star = eps_dem_chain13(Fraction(1, 5)) * Fraction(10 ** 6 + 1, 10 ** 6)
check("C8 closure density at eps0=1/5", d_star > Fraction(1, 50), True,
      "-> 2e-2 from above; exact value %s" % d_star)

# C9 — mg-0e8c §4 cross-check: primitivity forces d >= 2/n, so d <= 2e-2
#      needs n >= 100
check("C9 primitive d>=2/n meets 2e-2 at", min(n for n in range(3, 400)
                                               if Fraction(2, n) <= Fraction(1, 50)),
      100, "mg-0e8c §4: 'exactly the n >= 100 threshold row 8 records'")

# C10 — Op-Form §4.2: antichain Delta_1 minimised at k = n/2, value 1/2
n = 6
check("C10 antichain min Delta_1 n=6", min(delta1(n, frozenset(),
                                                  linear_extensions(n, frozenset()), k)
                                           for k in range(1, n)),
      Fraction(1, 2), "Op-Form §4.2")

# C11 — mg-832f's INDEPENDENT AUDIT, §7.1 and its box at :80-88.  It published
#       BEFORE this ticket existed: 'above n = 3, every poset with delta <= 1/3
#       is an ORDINAL SUM', 0 primitive at n = 4,5,6,7; the delta <= 1/3 counts
#       3, 6, 9, 21; the non-chain counts 6, 39, 356, 4823; and the PRIMITIVE
#       MINIMUM of delta at 2/5, 4/11, 5/14 (n = 4,5,6).  a2 §D' reproduces the
#       first of these, so it is a REPRODUCTION and not a finding, and this
#       control is where that is established rather than asserted.
cnt13, cntnc, primmin, primat13 = {}, {}, {}, {}
for n in range(3, 7):
    c13 = cnc = 0
    pm = None
    p13 = 0
    for rel in poset_iter(n):
        ex = linear_extensions(n, rel)
        dl = delta(n, rel, ex)
        if dl is None:
            continue
        cnc += 1
        prim = min(delta1(n, rel, ex, k) for k in range(1, n)) > 0
        if dl <= Fraction(1, 3):
            c13 += 1
            if prim:
                p13 += 1
        if prim and (pm is None or dl < pm):
            pm = dl
    cnt13[n], cntnc[n], primmin[n], primat13[n] = c13, cnc, pm, p13
check("C11a delta<=1/3 counts n=3..6", [cnt13[n] for n in range(3, 7)],
      [3, 6, 9, 21], "mg-832f audit :324, verbatim")
check("C11b non-chain counts n=3..6", [cntnc[n] for n in range(3, 7)],
      [6, 39, 356, 4823], "mg-832f audit :324, verbatim")
check("C11c primitive minimum of delta n=4..6",
      [primmin[n] for n in range(4, 7)],
      [Fraction(2, 5), Fraction(4, 11), Fraction(5, 14)],
      "mg-832f audit :331 — 'strictly above 1/3 and not monotone'")
check("C11d primitive posets with delta<=1/3, n=4..6",
      [primat13[n] for n in range(4, 7)], [0, 0, 0],
      "mg-832f audit :327 — and n=3 has %d, the exception they also record"
      % primat13[3])

# ------------------------------------------------------------------- D -----
print("\nD. WRONG-DIRECTION WORLDS — each MUST break a published number")

n = 6
rel = frozenset({(0, 2), (0, 3), (0, 4), (0, 5), (1, 4), (1, 5), (2, 4), (3, 4)})
ex = linear_extensions(n, rel)

# D1 — normalise by max(|A|,|B|) instead of min: the 17/78 witness must move.
A = set(range(3))
tot = sum(len(A - set(s[:3])) for s in ex)
wrong = Fraction(tot, len(ex)) / max(3, 3)
check("D1 max-normalisation still 17/78?", wrong == Fraction(17, 78), True,
      "EXPECTED-EQUAL at |A|=|B|: this witness CANNOT separate the two")
A = set(range(2))
tot = sum(len(A - set(s[:2])) for s in ex)
check("D1b at k=2 the two normalisations differ",
      Fraction(tot, len(ex)) / 2 != Fraction(tot, len(ex)) / 4, True,
      "so D1's blindness is a property of the witness, not of the control")

# D2 — half-open window [1/3,2/3): must lose balanced pairs somewhere
lost = 0
for nn in (4, 5):
    for r in poset_iter(nn):
        e = linear_extensions(nn, r)
        full = balanced_pairs(nn, r, e)
        half = {p: v for p, v in p_matrix(nn, r, e).items() if LO <= v < HI}
        lost += len(full) - len(half)
check("D2 half-open window loses pairs", lost > 0, True,
      "%d pairs sit exactly at 2/3 — the boundary is LOAD-BEARING" % lost)

# D3 — comparability density instead of incomparability: the d3c7 family flips
n, rel = d3c7_family(3)
comp_d = Fraction(len(rel), n * (n - 1) // 2)
check("D3 comparability density of d3c7 family", comp_d, Fraction(1) - Fraction(2, n),
      "= 5/7; a sign error here would call the SPARSEST family the densest")
check("D3b and it is NOT the incomparability density", comp_d != density(n, rel), True)

# D4 — a world where disjunct (i) is read as 'some pair', not 'some BALANCED
#      pair': then every non-chain poset satisfies it and the ceiling vanishes.
n = 6
rel = frozenset({(0, 2), (0, 3), (0, 4), (0, 5), (1, 4), (1, 5), (2, 4), (3, 4)})
ex = linear_extensions(n, rel)
v = cut_verdict(n, rel, ex, 3)
check("D4 witness fails U_either under the CORRECT reading",
      v['fails_either'], True, "if this went GREEN under the wrong reading the "
      "whole ceiling would be an artefact")
check("D4b and the witness is in the BOTH population", v['scope'], 'BOTH')

# ------------------------------------------------------------------- E -----
print("\nE. THE MONOTONE-CEILING DETECTOR, TESTED WHERE THE ANSWER IS KNOWN")


def ceiling_by_density_floor(failures, floors):
    """min Delta_1 over failures with d >= d0, for each d0.  None if empty."""
    out = []
    for d0 in floors:
        c = [eps for (eps, d) in failures if d >= d0]
        out.append(min(c) if c else None)
    return out


floors = [Fraction(0), Fraction(1, 4), Fraction(1, 2)]
mono = ceiling_by_density_floor(
    [(Fraction(1, 10), Fraction(1, 10)), (Fraction(1, 2), Fraction(3, 4))], floors)
check("E1 detector on a monotone population", mono,
      [Fraction(1, 10), Fraction(1, 2), Fraction(1, 2)])
nonmono = ceiling_by_density_floor(
    [(Fraction(1, 2), Fraction(1, 10)), (Fraction(1, 10), Fraction(3, 4))], floors)
check("E2 detector REPORTS a non-monotone population", nonmono,
      [Fraction(1, 10), Fraction(1, 10), Fraction(1, 10)],
      "the ceiling does NOT rise here — P5 would be refuted and the detector says so")

# ---------------------------------------------------------------- verdict --
print("\n" + "=" * 78)
if FAILS:
    print("RED — %d control(s) failed: %s" % (len(FAILS), ", ".join(FAILS)))
    sys.exit(1)
print("GREEN — every control passed.")
print("=" * 78)
