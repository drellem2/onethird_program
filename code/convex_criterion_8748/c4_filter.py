#!/usr/bin/env python3
"""c4 — THE FAST FILTER ON COMPRESSION PROPOSALS.  Two questions, both cheap, both answerable
before anyone writes a lemma.

`mg-0fc6`'s scope document recommends two first-checks for any new compression, and this ticket
exists so that they are findable and runnable rather than archived inside a `SCOPE: low` verdict:

    Q1  IS THE FAMILY NESTED?     If yes, its increments exist and a convex combination of THEM
                                  is a Littlewood–Paley multiplier — canonical (c2).  If no, the
                                  increments are not projections (Theorem C) and the intuition
                                  does not transfer.  ⚠️ Q1 is about the INCREMENTS: combining
                                  the COMPRESSIONS is never a compression either way (c1).

    Q2  CAN IT SEE REALIZABILITY? Feed it `mg-0fc6` `a2.3`'s two measures — identical pair
                                  marginals, one a linear-extension measure and one not.  If the
                                  construction returns the same answer on both, it reads the
                                  poset only through its pair marginals and CANNOT supply a
                                  realizability fact (`STATE.md:21`).

Neither question is a verdict on anything.  Q1 says whether one particular step is available;
Q2 says whether the construction is in the information set the wall already sits at equality on.
A construction can pass both and still be worthless, and `compression2` passes Q1 and fails Q2.

Both routines below take a CALLABLE, so the next design can be handed to them without editing
this file.  That is the point of the arm.
"""
import os
import sys
from fractions import Fraction
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib8748 as L  # noqa: E402


# ================================================================= Q1

def classify_family(parts):
    """Q1, in one call.  `parts` is a list of partitions of the same space, coarsest first.

    Returns `(verdict, detail)`.  Cost is one pass per consecutive pair — no matrix is formed.
    """
    if len(parts) < 2:
        return ("degenerate", "fewer than two distinct compressions")
    if L.is_filtration(parts):
        return ("NESTED", "increments exist; Σ λ_l D_l is a Littlewood–Paley multiplier")
    bad = [(k, L.nestedness(parts[k], parts[k + 1])) for k in range(len(parts) - 1)
           if not L.refines(parts[k], parts[k + 1])]
    return ("NOT NESTED", f"first failure at level {bad[0][0]}→{bad[0][1 - 1] + 1}: "
                          f"{bad[0][1]}")


# ================================================================= Q2

def two_measure_exhibit(n_max=6):
    """`a2.3`'s exhibit, re-derived here rather than imported.

    Returns `(n, mu1, mu2)` with IDENTICAL pair marginals, `mu1` a linear-extension measure and
    `mu2` not.  The construction is a COMMUTING SQUARE: `L`, `L·s`, `L·t`, `L·s·t` for two
    disjoint legal adjacent swaps, so `flag(L) + flag(L·s·t) = flag(L·s) + flag(L·t)` coordinate
    by coordinate — an exact kernel direction of the pair-marginal map with all four orders
    inside `L(P)`.  Moving mass `+ε, +ε, −ε, −ε` around it leaves every pair marginal fixed and
    destroys uniformity-on-support, which is what realizability requires.

    ⚠️ `mg-0fc6`'s D4, CARRIED OVER RATHER THAN REDISCOVERED: the base poset must satisfy the
    hypothesis `δ(P) ≤ 1/3`.  Their first version used the antichain, whose maximum flip is
    `1/2`, and so demonstrated the point on a measure the note's own standing assumption
    EXCLUDES.  The filter is worth nothing if it runs outside the hypothesis it is filtering.
    """
    for n in range(4, n_max + 1):
        # ONE REPRESENTATIVE PER ISOMORPHISM CLASS.  The exhibit is a WITNESS — one suffices —
        # and realizability, the pair marginals and the hypothesis are all isomorphism
        # invariants, so nothing is lost and `n = 6` becomes reachable (4 824 representatives
        # against 3^15 labelled masks).
        for lt in L.posets_upto_iso(n):
            LEs = L.linear_extensions(n, lt)
            if len(LEs) < 4:
                continue
            pp = L.pair_probs(LEs, n)
            if not pp or max(min(p, 1 - p) for p in pp.values()) > Fraction(1, 3):
                continue
            sq = _square(LEs, n, lt)
            if sq is None:
                continue
            mu1 = {Lx: Fraction(1, len(LEs)) for Lx in LEs}
            eps = Fraction(1, 4 * len(LEs))
            mu2 = dict(mu1)
            a, b, c, d = sq
            mu2[a] += eps
            mu2[b] += eps
            mu2[c] -= eps
            mu2[d] -= eps
            if L.pair_probs_measure(mu1, n) == L.pair_probs_measure(mu2, n):
                return (n, lt, LEs, mu1, mu2)
    return None


def _square(LEs, n, lt):
    S = set(LEs)
    for Lx in LEs:
        ps = L.bk_edges(Lx, n, lt)
        for p in ps:
            for q in ps:
                if q < p + 2:
                    continue
                A, C, D = Lx, L.swap(Lx, p), L.swap(Lx, q)
                B = L.swap(L.swap(Lx, p), q)
                if len({A, B, C, D}) == 4 and all(x in S for x in (A, B, C, D)):
                    return (A, B, C, D)
    return None


def is_realizable(mu, n):
    """Uniform on the linear extensions of SOME poset?  The oracle, with its reason."""
    supp = [Lx for Lx, w in mu.items() if w != 0]
    ws = {mu[Lx] for Lx in supp}
    if len(ws) != 1:
        return (False, "not uniform on its support")
    # the only candidate poset is the intersection order of the support
    rel = [(i, j) for (i, j) in combinations(range(n), 2)]
    lt_pairs = []
    for (i, j) in rel:
        if all(Lx.index(i) < Lx.index(j) for Lx in supp):
            lt_pairs.append((i, j))
        elif all(Lx.index(j) < Lx.index(i) for Lx in supp):
            lt_pairs.append((j, i))
    lt = L.tclose(n, lt_pairs)
    LEs = L.linear_extensions(n, lt)
    if set(LEs) != set(supp):
        return (False, f"support is not L(P): |L(P)|={len(LEs)} vs |supp|={len(supp)}")
    return (True, "uniform on the linear extensions of the intersection order")


def marginal_blind(construction, n, mu1, mu2):
    """Q2, in one call.  `construction` maps a measure to whatever it reads out of it."""
    a, b = construction(mu1, n), construction(mu2, n)
    return (a == b, a, b)


# ================================================================= the arm

L.banner("c4.1  THE EXHIBIT, re-derived on an implementation sharing no code with mg-0fc6")
ex = two_measure_exhibit()
L.verdict(ex is not None, "a two-measure exhibit exists")
n, lt, LEs, mu1, mu2 = ex
r1, why1 = is_realizable(mu1, n)
r2, why2 = is_realizable(mu2, n)
L.verdict(L.pair_probs_measure(mu1, n) == L.pair_probs_measure(mu2, n),
          "mu1 and mu2 have IDENTICAL pair marginals", f"n = {n}, e(P) = {len(LEs)}")
L.verdict(r1, "mu1 IS a linear-extension measure", why1)
L.verdict(not r2, "mu2 is NOT a linear-extension measure", why2)
# the corpus's own two-atom law — an order and its REVERSE — which is the standard non-example.
# ⚠️ D2, KEPT: this row first used the two lexicographically-first extensions, which differ by
# one adjacent transposition and ARE the linear extensions of their intersection order.  The
# oracle correctly accepted them and the row went RED against a control that was wrong.
two_atom = {LEs[0]: Fraction(1, 2), tuple(reversed(LEs[0])): Fraction(1, 2)}
ok2, why_atom = is_realizable(two_atom, n)
L.verdict(not ok2, "and the oracle REFUSES the corpus's two-atom law — it is not a constant True",
          why_atom)

L.banner("c4.2  Q2 APPLIED — what compression2's chain reads, and what it cannot")


def reads_pair_marginals(mu, nn):
    """`compression2`'s ONLY input: hypothesis (1), the maximum flip probability."""
    pp = L.pair_probs_measure(mu, nn)
    return max(min(p, 1 - p) for p in pp.values())


def reads_the_support(mu, nn):
    """A PLANTED construction that is NOT blind — the entropy of the measure itself."""
    return tuple(sorted(str(w) for w in mu.values()))


blind1, v1a, v1b = marginal_blind(reads_pair_marginals, n, mu1, mu2)
blind2, v2a, v2b = marginal_blind(reads_the_support, n, mu1, mu2)
L.verdict(blind1, "compression2's input (1) is MARGINAL-BLIND — same value on both",
          f"max flip = {v1a} on both")
L.verdict(not blind2,
          "WRONG-DIRECTION CONTROL: a support-reading construction is NOT blind",
          "so the filter does not answer 'blind' to everything")

L.banner("c4.3  Q1 APPLIED — four families, two of each kind")
CASES = []

# (a) compression2's scales
for nn, rel in ((4, []), (6, [(0, 1), (1, 2), (3, 4), (4, 5)])):
    lt2 = L.tclose(nn, rel)
    LE2 = L.linear_extensions(nn, lt2)
    CASES.append((f"compression2 scales, n={nn}", L.scale_filtration(LE2, LE2[0], nn), "NESTED"))

# (b) compression.tex's parity pair, at a poset measured TRANSVERSE in c3
lt3 = L.antichain(4)
LE3 = L.linear_extensions(4, lt3)
CASES.append(("compression.tex (C_o, C_e), n=4 antichain",
              [L.parity_foliation(LE3, 4, lt3, 0), L.parity_foliation(LE3, 4, lt3, 1)],
              "NOT NESTED"))

# (c) a PLANTED nested family that is NOT compression2's — prefix-length σ-algebras.  Its job is
#     to show 'NESTED' is not a property only compression2 has, so the filter is not a detector
#     for one construction wearing the language of a criterion.
CASES.append(("planted: prefixes of increasing length, n=4 antichain",
              [L.partition_of(LE3, lambda Lx, k=k: Lx[:k]) for k in range(5)],
              "NESTED"))

for label, parts, want in CASES:
    got, detail = classify_family(parts)
    L.verdict(got == want, f"{label}", f"{got} — {detail}")

L.note("THE FILTER, IN THE FORM THE NEXT PROPOSAL SHOULD MEET IT:",
       "",
       "  Q1  nested?            classify_family(parts)      one pass, no matrix",
       "  Q2  marginal-blind?    marginal_blind(f, n, mu1, mu2)",
       "",
       "Q1 = NESTED licenses ONE step: a convex combination of the INCREMENTS is canonical.",
       "It licenses nothing else, and in particular it is NOT evidence the construction is",
       "going anywhere.  Q2 = blind is the expensive answer: a construction that cannot tell",
       "mu1 from mu2 reads the poset only through its pair marginals, and STATE.md:21 says",
       "every route below 1 must add a REALIZABILITY fact, which such a construction cannot.",
       "compression2 is NESTED and BLIND — mg-0fc6 §2 — which is exactly why the criterion is",
       "worth keeping and the route it arrived in is not.")

sys.exit(L.finish())
