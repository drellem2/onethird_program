"""b2 — THE TIERED TABLE, with a verdict per row and the reason beside it.

The ticket asks for completeness, and names the axis that decides it: **what the candidate READS**.
That axis is the right one and it settles the table almost entirely, because of b1:

    reads the pair marginals `pi`                -> FACTORS by definition
    reads the poset `P`, or anything built on it -> FACTORS, because `P = {pi = 1}` (b1, C1)
    reads `supp(mu)`                             -> DOES NOT factor; testable at b3's witness
    reads the weights of `mu`                    -> DOES NOT factor; testable at `a2.3`'s witness

So the tiering the ticket proposed — measure / support / order relation / derived objects — has its
middle TWO tiers on the SAME side of the line and its top two on opposite sides.  `L(P)` and
`supp(mu)` are not the same object and only the second is surplus.  Rows below say which.

WHAT IS COMPUTED AND WHAT IS ARGUED.  Every row marked `computed` is evaluated on `a2.3`'s witness
shape (b1.3) or b3's support witness, and its verdict is the measured one.  Rows marked `by C1` are
not evaluated one by one — C1 is a proof, and evaluating a consequence of a proof on one witness
adds nothing.  The computed rows exist as a VACUITY GUARD on C1: if C1 were mis-stated, at least
one of them would separate.  A dozen do not.
"""

from fractions import Fraction
from itertools import combinations, permutations

import lib8b32 as L

# ------------------------------------------------------------------ witnesses

n = 6
prs = list(combinations(range(n), 2))
ident = tuple(range(n))
witness = None
for mask in range(1 << len(prs)):
    lt = [[False] * n for _ in range(n)]
    for i, (x, y) in enumerate(prs):
        if mask >> i & 1:
            lt[x][y] = True
    if not L.is_strict_order(n, lt):
        continue
    S = L.linexts(n, lt)
    if len(S) < 2:
        continue
    pi = L.marg_set(S, n)
    if L.lstar(pi, n) != ident or L.max_flip(pi, ident) > Fraction(1, 3):
        continue
    cols, basis = L.kernel_basis(S, n)
    if basis and (witness is None or len(S) < len(witness[1])):
        witness = (tuple(tuple(r) for r in lt), S, cols, basis)
PW, SW, colsW, basisW = witness
MU1 = L.unif(SW)
_d = basisW[0]
_s = min(abs(Fraction(1, len(SW)) / v) for v in _d if v != 0) / 2
MU2 = {sig: MU1[sig] + _s * _d[i] for i, sig in enumerate(colsW)}   # a2.3's shape: weights differ
# b3.2's SET witness: a proper subset of L(P) with L(P)'s exact marginals.  Among the twelve, the
# one used here is chosen to OMIT L* — because one of the rows below is `L* is a member of the
# support`, and a witness that happens to keep L* would score that row BLIND for a reason that is
# an artefact of enumeration order rather than a fact about the candidate.  Four of the six
# 3-element witnesses omit it (b3.1), so this is a choice among witnesses, not a search for one.
SETWIT = None
_STAR = L.lstar(L.marg_set(SW, n), n)
for m in range(1, len(SW)):
    cands = [T for T in combinations(SW, m) if L.marg_set(T, n) == L.marg_set(SW, n)]
    drop = [T for T in cands if _STAR not in T]
    if drop:
        SETWIT = L.unif(drop[0])
        break
    if cands:
        SETWIT = L.unif(cands[0])
        break

# ------------------------------------------------------------------ poset invariants


def relmat(mu):
    return L.forced_poset(L.marg(mu, n), n)


def height(lt):
    best = 0
    memo = {}

    def down(x):
        if x in memo:
            return memo[x]
        memo[x] = 1 + max([down(y) for y in range(n) if lt[y][x]] or [0])
        return memo[x]
    for x in range(n):
        best = max(best, down(x))
    return best


def width(lt):
    best = 0
    for k in range(1, n + 1):
        for A in combinations(range(n), k):
            if all(not lt[x][y] and not lt[y][x] for x, y in combinations(A, 2)):
                best = max(best, k)
    return best


def n_antichains(lt):
    c = 0
    for k in range(n + 1):
        for A in combinations(range(n), k):
            if all(not lt[x][y] and not lt[y][x] for x, y in combinations(A, 2)):
                c += 1
    return c


def jump_number(lt):
    best = None
    for Lx in L.linexts(n, lt):
        j = sum(1 for i in range(n - 1) if not lt[Lx[i]][Lx[i + 1]])
        best = j if best is None else min(best, j)
    return best


def mobius_hat(lt):
    """`mu(0-hat, 1-hat)` of `P` with a bottom and a top adjoined — the reduced Euler
    characteristic of the order complex of `P`, up to sign."""
    elts = ["0"] + list(range(n)) + ["1"]

    def leq(a, b):
        if a == b:
            return True
        if a == "0" or b == "1":
            return True
        if a == "1" or b == "0":
            return False
        return lt[a][b]
    mob = {}

    def m(a, b):
        if (a, b) in mob:
            return mob[(a, b)]
        if a == b:
            mob[(a, b)] = 1
        else:
            mob[(a, b)] = -sum(m(a, c) for c in elts if leq(a, c) and leq(c, b) and c != b)
        return mob[(a, b)]
    return m("0", "1")


def dimension(lt):
    """Order dimension: the least number of linear extensions whose intersection is `P`."""
    ext = L.linexts(n, lt)
    comp = [(x, y) for x in range(n) for y in range(n) if x != y and not lt[x][y] and not lt[y][x]]
    if not comp:
        return 1
    for k in range(2, len(ext) + 1):
        for R in combinations(ext, k):
            posl = []
            for e in R:
                p = [0] * n
                for t, v in enumerate(e):
                    p[v] = t
                posl.append(p)
            if all(any(p[x] > p[y] for p in posl) for x, y in comp):
                return k
    return None


def bk_graph(S):
    """The BK graph on a SET of orders: an edge for each adjacent transposition inside the set.
    Daniel's original object.  Called on `L(P)` it is a function of `P`; called on `supp(mu)` it
    is not — and the two rows below are exactly that distinction."""
    Sx = set(S)
    E = set()
    for u in Sx:
        for i in range(len(u) - 1):
            v = list(u)
            v[i], v[i + 1] = v[i + 1], v[i]
            v = tuple(v)
            if v in Sx:
                E.add(frozenset((u, v)))
    return frozenset(E), len(Sx)


def f17_three_mutually_adjacent(S):
    Sl = list(S)
    Sx = set(S)

    def adj(u, v):
        d = [i for i in range(len(u)) if u[i] != v[i]]
        return len(d) == 2 and d[1] == d[0] + 1
    for i in range(len(Sl)):
        for j in range(i + 1, len(Sl)):
            if not adj(Sl[i], Sl[j]):
                continue
            for k in range(j + 1, len(Sl)):
                if adj(Sl[i], Sl[k]) and adj(Sl[j], Sl[k]):
                    return True
    return False


def f22_no_three_antichain(lt):
    for A in combinations(range(n), 3):
        if all(not lt[x][y] and not lt[y][x] for x, y in combinations(A, 2)):
            return False
    return True


def weak_ideal(S, star):
    def inv(w):
        pos = {x: i for i, x in enumerate(w)}
        return frozenset((a, b) for a, b in combinations(star, 2) if pos[a] > pos[b])
    invs = {inv(w) for w in S}
    for w in permutations(star):
        iw = inv(w)
        if iw not in invs and any(iw < j for j in invs):
            return False
    return True


# ------------------------------------------------------------------ TIER 0 and TIER 1

L.banner("b2.1  TIER 0 — reads the pair marginals.  FACTORS BY DEFINITION.")
pi1, pi2 = L.marg(MU1, n), L.marg(MU2, n)
star1, star2 = L.lstar(pi1, n), L.lstar(pi2, n)
rows0 = [
    ("compression2 hypothesis (1) — max flip against L*",
     L.max_flip(pi1, star1), L.max_flip(pi2, star2), "mg-0fc6 a2.2"),
    ("the distinguished extension L*  [Daniel's candidate 1]", star1, star2, "mg-0fc6 a2.3"),
    ("delta(P) — the balance constant",
     min(min(pi1[(x, y)], 1 - pi1[(x, y)]) for x, y in combinations(range(n), 2)
         if 0 < pi1[(x, y)] < 1),
     min(min(pi2[(x, y)], 1 - pi2[(x, y)]) for x, y in combinations(range(n), 2)
         if 0 < pi2[(x, y)] < 1), "STATE.md glossary"),
    ("the pair-bias multiset  [F8's key]",
     " ".join(str(v) for v in
              sorted(min(pi1[(x, y)], 1 - pi1[(x, y)]) for x, y in combinations(range(n), 2))),
     " ".join(str(v) for v in
              sorted(min(pi2[(x, y)], 1 - pi2[(x, y)]) for x, y in combinations(range(n), 2))),
     "docs/FACTS.md F8"),
]
for label, a, b, src in rows0:
    L.verdict(a == b, f"FACTORS (computed): {label}", f"both {a}   [{src}]")
L.note("F19 ('at delta = 1/3 every incomparable pair is adjacent in e') and the dyadic merge tree")
L.note("are in this tier too and are not separately evaluated: both are functions of delta and L*.")

L.banner("b2.2  TIER 1 — reads the POSET P, or anything built from it.  FACTORS BY C1.")
P1, P2 = relmat(MU1), relmat(MU2)
L.verdict(P1 == P2, "the two witnesses recover the SAME order relation",
          "this row is C1 itself; every row below is a consequence of it")
LE1, LE2 = L.linexts(n, P1), L.linexts(n, P2)
rows1 = [
    ("e(P) — the number of linear extensions", len(LE1), len(LE2)),
    ("L(P) as a SET  [NOT supp(mu) — see b2.3]", LE1, LE2),
    ("the BK graph of L(P)  [DANIEL'S ORIGINAL QUESTION]", bk_graph(LE1), bk_graph(LE2)),
    ("height of P", height(P1), height(P2)),
    ("width of P", width(P1), width(P2)),
    ("order dimension of P", dimension(P1), dimension(P2)),
    ("jump number of P", jump_number(P1), jump_number(P2)),
    ("number of antichains of P", n_antichains(P1), n_antichains(P2)),
    ("Mobius function mu(0-hat, 1-hat) — the order complex's reduced Euler characteristic",
     mobius_hat(P1), mobius_hat(P2)),
    ("F17: three mutually adjacent linear extensions of P",
     f17_three_mutually_adjacent(LE1), f17_three_mutually_adjacent(LE2)),
    ("F22: P has no 3-element antichain", f22_no_three_antichain(P1), f22_no_three_antichain(P2)),
    ("L(P) is a weak-order ideal under L*  [Daniel's Bruhat candidate]",
     weak_ideal(LE1, star1), weak_ideal(LE2, star2)),
]
for label, a, b in rows1:
    shown = a if not isinstance(a, (tuple, frozenset)) else f"<{len(a)} items>"
    L.verdict(a == b, f"FACTORS (computed): {label}", f"both {shown}")
L.note("NOT EVALUATED ONE BY ONE, AND NOT NEEDED: the order polytope, the chain polytope, the")
L.note("order complex's homotopy type, alpha (F8), F13's reversal symmetry, F15's equality set,")
L.note("and the cohomology of the category of posets evaluated at P.  Each has P — or a functor")
L.note("of P — as its ONLY input, so each is a function of pi by C1 and takes one value here.")
L.note("The twelve computed rows above are the vacuity guard on that claim, not a sample of it.")

L.banner("b2.3  TIER 2 — reads supp(mu).  DOES NOT FACTOR.  Testable only at b3's witness.")
star = star1
rows2 = [
    ("L* is a member of the support", star in L.support(MU1), star in L.support(SETWIT)),
    ("|supp| equals e(P(pi))",
     len(L.support(MU1)) == len(LE1), len(L.support(SETWIT)) == len(LE1)),
    ("supp is a weak-order ideal under L*",
     weak_ideal(L.support(MU1), star), weak_ideal(L.support(SETWIT), star)),
    ("the BK graph of supp(mu)  [the SAME construction on the OTHER object]",
     bk_graph(L.support(MU1)), bk_graph(L.support(SETWIT))),
]
for label, a, b in rows2:
    shown = (a, b) if not isinstance(a, tuple) else (f"<{len(a[0])} edges>", f"<{len(b[0])} edges>")
    L.verdict(a != b, f"DOES NOT FACTOR (computed): {label}", f"realizable {shown[0]} / not {shown[1]}")
L.verdict(L.marg(MU1, n) == L.marg(SETWIT, n),
          "and the witness really is marginal-equivalent", "b3.2's set witness, inside hypothesis (1)")
L.note("THE BK GRAPH APPEARS IN BOTH TIERS AND THAT IS THE ANSWER TO DANIEL'S OPENING QUESTION:")
L.note("read on L(P) it is a function of the pair marginals and injects nothing; read on supp(mu)")
L.note("it is not.  The object was never the issue — which set it is taken on is.")
L.note("F17 IS ALSO A TIER-2 CANDIDATE when read on supp rather than on L(P), and it is BLIND on")
L.note("both witnesses this directory has (b3.4).  Blind is not the same verdict as factors.")

L.banner("b2.4  TIER 3 — reads the WEIGHTS.  DOES NOT FACTOR.  a2.3 is the witness.")
rows3 = [
    ("H(mu)", round(L.entropy_bits(MU1), 6), round(L.entropy_bits(MU2), 6)),
    ("mu is uniform on its support", L.realizable(MU1, n)[0], L.realizable(MU2, n)[0]),
    ("max weight / min positive weight",
     max(MU1.values()) / min(w for w in MU1.values() if w > 0),
     max(MU2.values()) / min(w for w in MU2.values() if w > 0)),
]
for label, a, b in rows3:
    L.verdict(a != b, f"DOES NOT FACTOR (computed): {label}", f"realizable {a} / not {b}")
L.note("b4 shows the sharpest member of this tier — gap(mu) = log2 e(P(pi)) - H(mu), zero EXACTLY")
L.note("on the realizable measures — and why it cannot be turned into a bound.")

L.banner("b2.5  WHAT THIS ENUMERATION DOES NOT COVER — stated, because completeness was the ask")
for s in [
    "1. Functions of pi, P, supp and the weights are ALL of mu, so the tiering is exhaustive OVER",
    "   FUNCTIONS OF A SINGLE MEASURE.  It says nothing about maps whose input is a FAMILY of",
    "   measures, a poset TOGETHER with extra combinatorial data not determined by it, or an",
    "   object outside this category altogether.",
    "2. 'Does not factor' is established by exhibiting disagreement, so it is exact.  'Factors' is",
    "   established for tiers 0 and 1 by PROOF (C1), not by agreement on a witness — but a row",
    "   whose tier is misassigned inherits the wrong verdict, and tier assignment is a reading of",
    "   the definition, not a measurement.",
    "3. BLIND rows (F17 on supp) are neither: one evaluation, no proof either way.",
    "4. n = 6 is ONE poset and n <= 4 is exhaustive.  Every count in this directory names its",
    "   population; no count here is asserted for general n.",
]:
    L.note(s)

L.finish()
