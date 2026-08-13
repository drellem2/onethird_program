"""b3 — THE SUPPORT-LEVEL WITNESS THE TICKET SAYS IS MISSING.  It is not missing.

`a2.3`'s two measures SHARE A SUPPORT, so every predicate that reads only the support takes the
same value on both for a reason that has nothing to do with factoring.  The ticket asks for a
second witness — "two SETS of permutations with identical pair marginals, one of which is `L(P)`
for some poset and one of which is not" — and says to build it before evaluating any support-level
candidate.

A WEAK VERSION OF IT ALREADY SITS IN `mg-0fc6`'s OWN CONTROL LIST, unrecognised as a witness:
`a2.1`'s third control is the two-atom measure, and `Unif({sigma, sigma^rev})` has EVERY pair
marginal at 1/2, which is exactly `Unif(S_n) = Unif(L(antichain))`'s marginal vector.  Two sets,
identical marginals, one a poset's and one not.  b1.5 measures it.  Its defect is `mg-0fc6`'s own
D4: the antichain's max flip is 1/2, so that pair sits OUTSIDE compression2's hypothesis (1).

b3.2 BUILDS THE WITNESS INSIDE THE HYPOTHESIS POPULATION, which is the version that binds: at the
same n = 6, e(P) = 9 poset `a2.3` used, six 3-element and six 6-element PROPER SUBSETS of `L(P)`
carry `L(P)`'s pair marginals exactly, and none of them is any poset's linear-extension set.

THIS ARM DOES THE THREE THINGS THAT ARE ACTUALLY OPEN:

  b3.1  Enumerate the WHOLE marginal fiber at the n=6 hypothesis-population witness — every vertex,
        exactly — so "which supports occur at this marginal vector" is answered rather than sampled.
  b3.2  Ask whether a SET-level witness exists INSIDE the hypothesis population, exhaustively:
        is there `S` strictly inside `L(P)` with the same normalised pair counts?
  b3.3  Evaluate the support-level candidates on the witnesses that exist, and say for each
        whether it is shown NOT to factor, or merely blind here.

AND ONE LOGICAL CORRECTION THE TICKET'S OWN PROCEDURE NEEDS.  The ticket says "same value on both
-> it factors -> dead".  That is too strong: agreement at ONE point of a fiber is not a proof of
factoring, it is one evaluation.  What agreement DOES prove is the thing the ticket cares about —
that the candidate cannot separate THIS realizable measure from THIS non-realizable one, so it
cannot inject realizability on its own.  Both readings are printed below and they are labelled
differently, because a table that records "factors" where it measured "blind here" is a table that
has stopped being falsifiable.
"""

from fractions import Fraction
from itertools import combinations

import lib8b32 as L

# ------------------------------------------------------------------ the n=6 witness, rebuilt

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
PI_W = L.marg_set(SW, n)
STAR_W = L.lstar(PI_W, n)


def fiber_vertices(S, n):
    """EVERY vertex of `{nu >= 0 : sum nu = 1, pair marginals = pi(Unif(S))}`, exactly.

    Basic feasible solutions: choose `rank` columns, solve, keep the ones that are non-negative.
    `C(9,5) = 126` systems here, so this is an enumeration and not a search.
    """
    S = list(S)
    rows = [[Fraction(1)] * len(S)]
    tgt = [Fraction(1)]
    for x, y in combinations(range(n), 2):
        row = []
        for sig in S:
            pos = [0] * n
            for t, e in enumerate(sig):
                pos[e] = t
            row.append(Fraction(1) if pos[x] < pos[y] else Fraction(0))
        rows.append(row)
        tgt.append(sum(r * Fraction(1, len(S)) for r in row))
    red, piv = L._rref([r + [t] for r, t in zip(rows, tgt)], len(S))
    rank = len(piv)
    out = {}
    for B in combinations(range(len(S)), rank):
        sub = [[rows[i][c] for c in B] + [tgt[i]] for i in range(len(rows))]
        rr, pp = L._rref(sub, rank)
        if len(pp) != rank:
            continue
        sol = [Fraction(0)] * rank
        good = True
        for i, c in enumerate(pp):
            sol[c] = rr[i][rank]
        # verify the solution really satisfies every row (the system is overdetermined)
        for i in range(len(rows)):
            if sum(rows[i][c] * sol[j] for j, c in enumerate(B)) != tgt[i]:
                good = False
                break
        if not good or any(v < 0 for v in sol):
            continue
        nu = {sig: Fraction(0) for sig in S}
        for j, c in enumerate(B):
            nu[S[c]] += sol[j]
        out[tuple(sorted(nu.items()))] = nu
    return list(out.values())


L.banner("b3.1  THE WHOLE MARGINAL FIBER AT THE n = 6 HYPOTHESIS-POPULATION WITNESS")
L.note(f"P has e(P) = {len(SW)}; the fiber has dimension {len(basisW)}; L* = {STAR_W}")
verts = fiber_vertices(SW, n)
L.verdict(len(verts) > 1, "the fiber is a polytope with more than one vertex",
          f"{len(verts)} vertices, enumerated exactly")
real_v = [v for v in verts if L.realizable(v, n)[0]]
L.verdict(len(real_v) == 0,
          "NOT ONE VERTEX IS REALIZABLE",
          "the only realizable point of this fiber is Unif(L(P)), which is interior")
smaller = [v for v in verts if len(L.support(v)) < len(SW)]
L.verdict(len(smaller) == len(verts),
          "every vertex has a SUPPORT STRICTLY SMALLER than L(P)",
          f"support sizes {sorted(set(len(L.support(v)) for v in verts))} against e(P) = {len(SW)}")
L.note("So a support-level witness INSIDE the hypothesis population exists and there are many:")
L.note("same marginals as Unif(L(P)), different support, not realizable.")

drops_star = [v for v in verts if STAR_W not in L.support(v)]
L.verdict(len(drops_star) > 0,
          "and at least one of them DOES NOT CONTAIN L*",
          f"{len(drops_star)} of {len(verts)} vertices drop the majority order")

L.banner("b3.2  IS THERE A SET-LEVEL WITNESS INSIDE THE HYPOTHESIS POPULATION?")
# A *set* witness is stronger than a *measure* witness: it needs a proper subset of L(P) whose
# NORMALISED pair counts are unchanged, i.e. a second uniform measure in the same fiber.


def proper_subsets_with_same_marginals(S, n, cap=1 << 24):
    """Every non-empty `T` strictly inside `S` with `pi(Unif(T)) = pi(Unif(S))`.

    Exhaustive by meet-in-the-middle on the pair-count vector: `2^(k/2)` per half, so `|S| <= 24`
    is comfortable and larger sets are declined rather than sampled (the caller states the cap).
    """
    S = list(S)
    k = len(S)
    if (1 << k) > cap:
        return None
    inc = [(x, y) for x, y in combinations(range(n), 2)]
    vecs = []
    for sig in S:
        pos = [0] * n
        for t, e in enumerate(sig):
            pos[e] = t
        vecs.append(tuple(1 if pos[x] < pos[y] else 0 for x, y in inc))
    total = tuple(sum(v[i] for v in vecs) for i in range(len(inc)))
    h = k // 2
    left, right = list(range(h)), list(range(h, k))

    def enum(idxs):
        acc = {}
        for m in range(1 << len(idxs)):
            sz = 0
            vec = [0] * len(inc)
            for b, i in enumerate(idxs):
                if m >> b & 1:
                    sz += 1
                    for j in range(len(inc)):
                        vec[j] += vecs[i][j]
            acc.setdefault((sz, tuple(vec)), []).append(m)
        return acc

    A, B = enum(left), enum(right)
    found = []
    for m in range(1, k):
        # target counts must be integral
        tgt = []
        okint = True
        for j in range(len(inc)):
            num = total[j] * m
            if num % k:
                okint = False
                break
            tgt.append(num // k)
        if not okint:
            continue
        for (sa, va), masksA in A.items():
            if sa > m:
                continue
            need = (m - sa, tuple(t - v for t, v in zip(tgt, va)))
            if any(c < 0 for c in need[1]) or need not in B:
                continue
            for ma in masksA:
                for mb in B[need]:
                    T = [S[i] for b, i in enumerate(left) if ma >> b & 1]
                    T += [S[i] for b, i in enumerate(right) if mb >> b & 1]
                    found.append(tuple(sorted(T)))
    return sorted(set(found))


# CONTROL ON THE WITNESS-FINDER ITSELF, before its answer is used for anything.  This function is
# new code and it decides this ticket's headline EXISTENCE claim, so it is checked against naive
# enumeration over every subset — the route it exists to replace — on subjects small enough for
# both to run.  A finder that is the only thing that can see its own findings is the defect this
# whole directory is about, arriving inside the remedy.
naive_ok = True
naive_cases = 0
for m in (3, 4):
    for lt in L.all_posets(m):
        Sx = L.linexts(m, lt)
        if len(Sx) < 2 or len(Sx) > 12:
            continue
        tot = L.marg_set(Sx, m)
        naive = sorted({tuple(sorted(T)) for k in range(1, len(Sx))
                        for T in combinations(Sx, k) if L.marg_set(T, m) == tot})
        if proper_subsets_with_same_marginals(Sx, m) != naive:
            naive_ok = False
        naive_cases += 1
L.verdict(naive_ok, "the meet-in-the-middle finder agrees with NAIVE subset enumeration",
          f"{naive_cases} posets at n = 3 and 4 with |L(P)| <= 12, every subset compared")
naive6 = sorted({tuple(sorted(T)) for k in range(1, len(SW))
                 for T in combinations(SW, k) if L.marg_set(T, n) == L.marg_set(SW, n)})
L.verdict(proper_subsets_with_same_marginals(SW, n) == naive6,
          "and it agrees on the n = 6 witness too, against all 2^9 subsets naively",
          f"{len(naive6)} subsets found by both routes")

sub = proper_subsets_with_same_marginals(SW, n)
sizes = sorted({len(T) for T in sub}) if sub else []
L.verdict(bool(sub),
          "A SET-LEVEL WITNESS EXISTS, AND IT IS INSIDE THE HYPOTHESIS POPULATION",
          f"{len(sub)} proper subsets of L(P) share its marginals exactly; sizes {sizes}"
          f" against e(P) = {len(SW)}; all {2 ** len(SW)} subsets tested")
L.verdict(all(not L.realizable(L.unif(T), n)[0] for T in sub),
          "and NOT ONE of them is a linear-extension set",
          "forced: same marginals give the same P, and a proper subset of L(P) is not L(P)")
L.note("This is exactly the object the ticket asked for and expected might not exist — two SETS")
L.note("of permutations with identical pair marginals, one a poset's L(P) and one not — and it")
L.note("sits inside compression2's own hypothesis (1), which the two-atom witness does not.")
L.note("SO EVERY SUPPORT-LEVEL CANDIDATE IS NOW TESTABLE, at a witness the note's own standing")
L.note("assumption admits.")

# How common this is, measured rather than asserted.
hits = {}
for m in (3, 4):
    tot = wit = 0
    example = None
    for lt in L.all_posets(m):
        S = L.linexts(m, lt)
        if len(S) < 2:
            continue
        tot += 1
        s = proper_subsets_with_same_marginals(S, m)
        if s:
            wit += 1
            if example is None:
                example = (lt, S, s[0])
    hits[m] = (tot, wit, example)
    L.verdict(True, f"n = {m}: posets admitting a proper same-marginal subset",
              f"{wit} of {tot} (exhaustive over all labelled posets and ALL their subsets)")
ex = hits[3][2]
L.note(f"n = 3 example: L(P) = {ex[1]}   proper subset with identical marginals = {ex[2]}")
inside = []
for m in (3, 4):
    for lt in L.all_posets(m):
        S = L.linexts(m, lt)
        if len(S) < 2:
            continue
        pi = L.marg_set(S, m)
        st = L.lstar(pi, m)
        if st is None or L.max_flip(pi, st) > Fraction(1, 3):
            continue
        if proper_subsets_with_same_marginals(S, m):
            inside.append((m, lt))
L.verdict(len(inside) == 0,
          "and at n = 3 and 4 NONE of the carriers is in the hypothesis population",
          "so the n = 6 witness above is the first one inside it, not a typical member")
L.note("SCOPE, stated because these counts are the weakest claims in the directory: exhaustive at")
L.note("n = 3 and n = 4 over all labelled posets and ALL their subsets, and exhaustive at the")
L.note("single n = 6 witness poset.  n = 5 is NOT swept and n = 6 is ONE poset — the subset")
L.note("enumeration is 2^|L(P)| and |L(P)| reaches 120 at n = 5.  The EXISTENCE claim above needs")
L.note("only the one poset; the FREQUENCY counts say nothing above n = 4.")

L.banner("b3.3  THE SUPPORT-LEVEL CANDIDATES, EVALUATED")


def weak_ideal(S, n, star):
    """Is `S` an order ideal of the weak order, relabelled so that `star` is the identity?

    `Inv(w)` = the set of pairs appearing out of `star`-order in `w`.  `L(P)` with a natural
    labelling is exactly `{w : Inv(w) misses the comparable pairs}`, which is downward closed —
    so this is a NECESSARY condition for a set to be some poset's `L(P)` under that labelling.
    """
    rank = {x: i for i, x in enumerate(star)}

    def inv(w):
        pos = {x: i for i, x in enumerate(w)}
        return frozenset((a, b) for a, b in combinations(star, 2) if pos[a] > pos[b])

    invs = {inv(w) for w in S}
    from itertools import permutations as P
    for w in P(star):
        iw = inv(w)
        if iw in invs:
            continue
        if any(iw < j for j in invs):        # strictly below a member and not a member
            return False
    return True


star6 = STAR_W
mu1 = L.unif(SW)
nu_small = min(smaller, key=lambda v: len(L.support(v)))
nu_nostar = drops_star[0]

anti = L.antichain(4)
S4 = L.linexts(4, anti)
two_atom4 = {(0, 1, 2, 3): Fraction(1, 2), (3, 2, 1, 0): Fraction(1, 2)}

rows = []
# (candidate, value on the realizable side, value on the non-realizable side, witness used)
rows.append(("L* is a member of the support",
             star6 in L.support(mu1), star6 in L.support(nu_nostar), "b3.1 fiber vertex, n = 6"))
rows.append(("the support is a weak-order ideal under L*",
             weak_ideal(L.support(mu1), 6, star6),
             weak_ideal(L.support(nu_small), 6, star6), "b3.1 fiber vertex, n = 6"))
rows.append(("the support is a weak-order ideal under L*  [two-atom]",
             weak_ideal(S4, 4, (0, 1, 2, 3)),
             weak_ideal(tuple(sorted(two_atom4)), 4, (0, 1, 2, 3)), "two-atom, n = 4"))
rows.append(("|support| equals e(P(pi))",
             len(L.support(mu1)) == len(SW),
             len(L.support(nu_small)) == len(SW), "b3.1 fiber vertex, n = 6"))
for label, a, b, w in rows:
    L.verdict(a != b, f"SEPARATES: {label}", f"realizable {a} / non-realizable {b}   [{w}]")

L.banner("b3.4  AND THE CANDIDATES THAT ARE BLIND HERE — reported, not omitted")
# F17: "three mutually adjacent linear extensions do not exist" — adjacency = one adjacent
# transposition apart.  A property of the SET, so it is a tier-2 candidate by the ticket's tiering.


def has_three_mutually_adjacent(S):
    Sx = set(S)

    def adj(u, v):
        d = [i for i in range(len(u)) if u[i] != v[i]]
        return len(d) == 2 and d[1] == d[0] + 1 and u[d[0]] == v[d[1]] and u[d[1]] == v[d[0]]

    Sl = list(Sx)
    for i in range(len(Sl)):
        for j in range(i + 1, len(Sl)):
            if not adj(Sl[i], Sl[j]):
                continue
            for k in range(j + 1, len(Sl)):
                if adj(Sl[i], Sl[k]) and adj(Sl[j], Sl[k]):
                    return True
    return False


blind = []
blind.append(("F17: three mutually adjacent members exist",
              has_three_mutually_adjacent(L.support(mu1)),
              has_three_mutually_adjacent(L.support(nu_small))))
blind.append(("F17, on the two-atom witness",
              has_three_mutually_adjacent(S4),
              has_three_mutually_adjacent(tuple(sorted(two_atom4)))))
for label, a, b in blind:
    L.verdict(a == b, f"BLIND HERE (does not separate): {label}",
              f"both {a} — this is ONE evaluation, not a proof that it factors")
L.note("F17 is TRUE of every linear-extension set (that is what makes it a fact) and is also true")
L.note("of both non-realizable witnesses here, so it excludes nothing they contain.  That is a")
L.note("statement about these witnesses, not a theorem about F17.")

L.finish()
