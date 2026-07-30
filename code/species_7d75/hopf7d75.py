"""Shared constructions for mg-7d75's Hopf-monoid checks.

Everything here is a construction taken from Aguiar-Mahajan, "Monoidal
Functors, Species and Hopf Algebras", instantiated on our objects:

  * the Hopf monoid of POSETS P (Section 13.1.1), product disjoint union,
    coproduct p |-> p|_S (x) p|_T when S is a lower set of p and 0 otherwise
    (Section 13.4.2: "e_{S,T}(p) = 0 <=> S is a lower set of p", and "the Hopf
    monoid of posets of Section 13.1.1 is P_0");
  * the Hopf monoids of SET COMPOSITIONS (faces) and SET PARTITIONS (flats)
    of Chapter 12, product concatenation / disjoint union, coproduct
    restriction;
  * the HADAMARD product (Section 8.13): "the Hadamard product h1 x h2 of two
    Hopf monoids h1 and h2 is again a Hopf monoid."

The two subspecies under test are

    F[I]  = { (p, F) : p a poset on I, F a face in the braid cone of p }
    AC[I] = { (p, X) : p a poset on I, X in AC(p) }

sitting inside P x Sigma and P x Pi respectively.  No claim is made here; the
claims are the measurements in t5_hopf_monoid.py and t6_fock_and_record.py.
"""

from itertools import combinations
from kern7d75 import sc_product

GROUND = 4

# ---- posets on an arbitrary finite ground set -------------------------------

def posets_on(I):
    I = tuple(sorted(I))
    pairs = [(a, b) for a in I for b in I if a != b]
    out = set()
    for k in range(len(pairs) + 1):
        for sub in combinations(pairs, k):
            rel = set(sub)
            if any((b, a) in rel for (a, b) in rel):
                continue
            ok = True
            changed = True
            while changed and ok:
                changed = False
                for (a, b) in list(rel):
                    for (c, d) in list(rel):
                        if b == c:
                            if a == d:
                                ok = False
                            elif (a, d) not in rel:
                                rel.add((a, d))
                                changed = True
                if any((b, a) in rel for (a, b) in rel):
                    ok = False
            if ok:
                out.add(frozenset(rel))
    return sorted(out, key=lambda r: (len(r), sorted(r)))


def restrict_poset(rel, S):
    return frozenset((a, b) for (a, b) in rel if a in S and b in S)


def is_lower_set(rel, S):
    return all(a in S for (a, b) in rel if b in S)


def faces_on(I, rel):
    """Faces of the braid arrangement on I lying in the braid cone of rel."""
    I = frozenset(I)
    out = []
    for F in _all_compositions(I):
        idx = {}
        for t, B in enumerate(F):
            for v in B:
                idx[v] = t
        if all(idx[a] <= idx[b] for (a, b) in rel):
            out.append(F)
    return out


def _all_compositions(I):
    I = sorted(I)
    if not I:
        return [()]
    out = []

    def rec(rem, acc):
        if not rem:
            out.append(tuple(acc))
            return
        rem = sorted(rem)
        for k in range(1, len(rem) + 1):
            for B in combinations(rem, k):
                rec([x for x in rem if x not in B],
                    acc + [frozenset(B)])
    rec(I, [])
    return out


def restrict_face(F, S):
    return tuple(B & S for B in F if B & S)


def concat(F, G):
    return tuple(F) + tuple(G)


def supp_of(F):
    return frozenset(F)


def restrict_part(X, S):
    return frozenset(B & S for B in X if B & S)


def part_union(X, Y):
    return frozenset(X) | frozenset(Y)


def acyclic(rel, X):
    blocks = sorted(X, key=lambda b: sorted(b))
    where = {}
    for t, B in enumerate(blocks):
        for v in B:
            where[v] = t
    m = len(blocks)
    succ = [set() for _ in range(m)]
    for (a, b) in rel:
        if where[a] != where[b]:
            succ[where[a]].add(where[b])
    col = [0] * m

    def dfs(v):
        col[v] = 1
        for w in succ[v]:
            if col[w] == 1:
                return False
            if col[w] == 0 and not dfs(w):
                return False
        col[v] = 2
        return True
    return all(col[v] != 0 or dfs(v) for v in range(m))


# ---- the two candidate species ----------------------------------------------

def elems_F(I):
    return [(rel, F) for rel in posets_on(I) for F in faces_on(I, rel)]


def elems_AC(I):
    out = []
    for rel in posets_on(I):
        for X in {supp_of(F) for F in faces_on(I, rel)}:
            out.append((rel, X))
    return sorted(out, key=repr)


def mu_F(x, y):
    return (x[0] | y[0], concat(x[1], y[1]))


def _cond(rel, S, mode):
    if mode is True or mode == "lower":
        return is_lower_set(rel, S)
    if mode is False or mode == "none":
        return True
    if mode == "antichain":
        return not any(a in S and b in S for (a, b) in rel)
    raise ValueError(mode)


def de_F(x, S, T, lowerset=True):
    rel, F = x
    if not _cond(rel, S, lowerset):
        return None
    return ((restrict_poset(rel, S), restrict_face(F, S)),
            (restrict_poset(rel, T), restrict_face(F, T)))


def mu_AC(x, y):
    return (x[0] | y[0], part_union(x[1], y[1]))


def de_AC(x, S, T, lowerset=True):
    rel, X = x
    if not _cond(rel, S, lowerset):
        return None
    return ((restrict_poset(rel, S), restrict_part(X, S)),
            (restrict_poset(rel, T), restrict_part(X, T)))


def decompositions(I):
    I = sorted(I)
    out = []
    for m in range(1 << len(I)):
        S = frozenset(I[i] for i in range(len(I)) if m >> i & 1)
        out.append((S, frozenset(I) - S))
    return out


def run(name, elems, mu, de, lowerset=True):
    """Returns a dict of failure counts for each axiom."""
    f = dict(prod_closure=0, coprod_closure=0, assoc=0, coassoc=0, compat=0,
             tested=0)
    universe = {}
    for k in range(GROUND + 1):
        for I in combinations(range(GROUND), k):
            universe[frozenset(I)] = set(elems(frozenset(I)))
    for I, els in universe.items():
        for (S, T) in decompositions(I):
            # product closure
            for x in universe[S]:
                for y in universe[T]:
                    z = mu(x, y)
                    f["tested"] += 1
                    if z not in els:
                        f["prod_closure"] += 1
            # coproduct closure
            for x in els:
                d = de(x, S, T, lowerset)
                if d is None:
                    continue
                if d[0] not in universe[S] or d[1] not in universe[T]:
                    f["coprod_closure"] += 1
    # associativity / coassociativity on the top ground set
    I = frozenset(range(GROUND))
    for (S, R) in decompositions(I):
        for (S1, S2) in decompositions(S):
            for x in universe[S1]:
                for y in universe[S2]:
                    for z in universe[R]:
                        if mu(mu(x, y), z) != mu(x, mu(y, z)):
                            f["assoc"] += 1
    for (A, rest) in decompositions(I):
        for (B, C) in decompositions(rest):
            for x in universe[I]:
                d1 = de(x, A, B | C, lowerset)
                l = None if d1 is None else de(d1[1], B, C, lowerset)
                d2 = de(x, A | B, C, lowerset)
                r = None if d2 is None else de(d2[0], A, B, lowerset)
                lv = None if l is None else (d1[0], l[0], l[1])
                rv = None if r is None else (r[0], r[1], d2[1])
                if lv != rv:
                    f["coassoc"] += 1
    # compatibility
    for (S1, T1) in decompositions(I):
        for (S2, T2) in decompositions(I):
            A, B = S1 & S2, S1 & T2
            C, D = T1 & S2, T1 & T2
            for x in universe[S1]:
                for y in universe[T1]:
                    lhs = de(mu(x, y), S2, T2, lowerset)
                    dx = de(x, A, B, lowerset)
                    dy = de(y, C, D, lowerset)
                    if dx is None or dy is None:
                        rhs = None
                    else:
                        rhs = (mu(dx[0], dy[0]), mu(dx[1], dy[1]))
                    if lhs != rhs:
                        f["compat"] += 1
    return f


