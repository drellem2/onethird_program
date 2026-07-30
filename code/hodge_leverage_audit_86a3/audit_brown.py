"""Independent rebuild of §9: the face semigroup, Brown's theorem, and -- the
part the deliverable leaves open -- an EXACT DECISION for the cases §9.4 calls
"undecided".

§9.4 uses a sufficient condition only (an unreachable AT edge).  Where it does
not bite, the deliverable stops.  Here the question is decided outright by exact
rational linear programming: the lazy AT walk is a Brown walk iff the system

    sum_x w(x) T_x = P_lazy ,   w >= 0 ,   sum_x w(x) = 1

is feasible, where T_x[c,d] = [x.c = d].  That is a finite LP with rational
data, so "undecided" is not a resting place -- it is a question nobody asked.
"""

import sys
from fractions import Fraction

from audit_core import (posets_upto_iso, linexts, facet_of, all_faces, blocks,
                        induced, at_graph, proper_ideals_of)
from exact_lp import feasible


# --------------------------------------------------------------------------
# the band
# --------------------------------------------------------------------------

def faces_as_partitions(P):
    fs = all_faces(P)
    out = []
    for d in sorted(fs):
        for s in fs[d]:
            out.append(blocks(P, s))
    return out


def prod(x, y):
    out = []
    for B in x:
        for C in y:
            m = B & C
            if m:
                out.append(m)
    return tuple(out)


def acyclic_partitions(P):
    """Every set partition pi of P with P/pi acyclic, as frozensets of masks.
    Enumerated over ALL set partitions and filtered -- the deliverable's route
    is the same test, but this enumeration is independent."""
    n = P.n
    parts = []

    def rec(i, blks):
        if i == n:
            parts.append(tuple(blks))
            return
        for j in range(len(blks)):
            nb = list(blks)
            nb[j] |= (1 << i)
            rec(i + 1, nb)
        rec(i + 1, blks + [1 << i])

    rec(0, [])
    out = set()
    for pi in parts:
        bof = {}
        for j, B in enumerate(pi):
            for x in range(n):
                if (B >> x) & 1:
                    bof[x] = j
        adj = {j: set() for j in range(len(pi))}
        for (a, b) in P.lt:
            if bof[a] != bof[b]:
                adj[bof[a]].add(bof[b])
        colour = {}

        def dfs(u):
            colour[u] = 1
            for v in adj[u]:
                if colour.get(v, 0) == 1:
                    return True
                if colour.get(v, 0) == 0 and dfs(v):
                    return True
            colour[u] = 2
            return False

        if not any(colour.get(u, 0) == 0 and dfs(u) for u in adj):
            out.add(frozenset(pi))
    return out


def refines(Y, X):
    return all(any((b & a) == b for a in X) for b in Y)


def chambers_refining(P, X):
    t = 1
    for B in X:
        t *= len(linexts(induced(P, B)))
    return t


def multiplicities(P, L):
    order = sorted(L, key=lambda X: -len(X))
    m = {}
    for X in order:
        s = 0
        for Y in L:
            if Y != X and refines(Y, X):
                s += m.get(Y, 0)
        m[X] = chambers_refining(P, X) - s
    return m


# --------------------------------------------------------------------------
# exact rank over Q
# --------------------------------------------------------------------------

def rank_q(M):
    M = [row[:] for row in M]
    rows, cols = len(M), len(M[0]) if M else 0
    r = 0
    for c in range(cols):
        p = None
        for i in range(r, rows):
            if M[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        pv = M[r][c]
        M[r] = [v / pv for v in M[r]]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [M[i][j] - f * M[r][j] for j in range(cols)]
        r += 1
        if r == rows:
            break
    return r


# --------------------------------------------------------------------------
# the checks
# --------------------------------------------------------------------------

def check_band(n):
    bad_axiom = bad_assoc = bad_supp = 0
    for P in posets_upto_iso(n):
        F = faces_as_partitions(P)
        S = set(F)
        ident = ((1 << P.n) - 1,)
        for x in F:
            if prod(x, x) != x:
                bad_axiom += 1
                break
            if prod(ident, x) != x or prod(x, ident) != x:
                bad_axiom += 1
                break
        else:
            for x in F:
                for y in F:
                    xy = prod(x, y)
                    if xy not in S or prod(prod(x, y), x) != xy:
                        bad_axiom += 1
                        break
                else:
                    continue
                break
        if n <= 4:
            for x in F:
                for y in F:
                    for z in F:
                        if prod(prod(x, y), z) != prod(x, prod(y, z)):
                            bad_assoc += 1
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break
        sup = {frozenset(x) for x in F}
        if sup != acyclic_partitions(P):
            bad_supp += 1
    return bad_axiom, bad_assoc, bad_supp


def weight_families(P, F):
    """Several deliberately different weightings, to test that the predicted
    MULTIPLICITIES really are w-free."""
    out = {}
    st = 7
    w = {}
    for x in F:
        st = (1103515245 * st + 12345) % 100003
        w[x] = 1 + st % 97
    out["generic all faces"] = w
    st = 11
    w = {}
    for x in F:
        if len(x) == 2:
            st = (1103515245 * st + 12345) % 100003
            w[x] = 1 + st % 61
    out["two-block faces"] = w
    st = 13
    w = {}
    for x in F:
        if len(x) == 2 and bin(x[0]).count("1") == 1:
            st = (1103515245 * st + 12345) % 100003
            w[x] = 1 + st % 53
    out["({i},rest) faces"] = w
    # two extra families the deliverable did not use
    w = {x: 1 for x in F}
    out["uniform all faces"] = w
    w = {x: 1 for x in F if len(x) == P.n}
    out["chambers only"] = w
    w = {x: (3 ** len(x)) for x in F if len(x) >= 2}
    out["3^k on k-block faces"] = w
    return out


def check_spectrum(n, verbose=False):
    """Predicted (lambda_X, m_X) vs the actual matrix, by exact rational rank."""
    tally = {}
    mult_sets = {}
    for P in posets_upto_iso(n):
        F = faces_as_partitions(P)
        chambers = [x for x in F if len(x) == P.n]
        cidx = {c: i for i, c in enumerate(chambers)}
        L = sorted({frozenset(x) for x in F}, key=lambda X: (len(X), sorted(X)))
        mX = multiplicities(P, L)
        key = P.tag()
        mult_sets.setdefault(key, mX)
        for name, w in weight_families(P, F).items():
            tot = sum(w.values())
            if tot == 0:
                continue
            m = len(chambers)
            M = [[Fraction(0)] * m for _ in range(m)]
            for x, wt in w.items():
                if not wt:
                    continue
                for c in chambers:
                    M[cidx[c]][cidx[prod(x, c)]] += Fraction(wt, tot)
            lam = {}
            for X in L:
                s = 0
                for x, wt in w.items():
                    if wt and refines(X, frozenset(x)):
                        s += wt
                lam[X] = Fraction(s, tot)
            pred = {}
            for X in L:
                pred[lam[X]] = pred.get(lam[X], 0) + mX[X]
            ok = True
            tot_dim = 0
            for Lam, mult in pred.items():
                A = [[M[i][j] - (Lam if i == j else 0) for j in range(m)]
                     for i in range(m)]
                dim = m - rank_q(A)
                tot_dim += dim
                if dim != mult:
                    ok = False
            if tot_dim != m:
                ok = False
            t = tally.setdefault(name, [0, 0])
            t[0] += 1
            t[1] += bool(ok)
            if verbose and not ok:
                print("      FAIL", name, P.tag())
    return tally


# --------------------------------------------------------------------------
# §9.4 decided exactly
# --------------------------------------------------------------------------

def decide_brown(P):
    """Returns (verdict, witness) with verdict in
    {'vacuous', 'IS a Brown walk', 'NOT a Brown walk'}."""
    les, adj = at_graph(P)
    m = len(les)
    if m < 2:
        return "vacuous", None
    nr = P.n - 1
    # the lazy AT walk
    Pl = [[Fraction(0)] * m for _ in range(m)]
    for i in range(m):
        Pl[i][i] = Fraction(1) - Fraction(len(adj[i]), 2 * nr)
        for j in adj[i]:
            Pl[i][j] = Fraction(1, 2 * nr)
    # faces, as maps on chambers; keep only those whose map stays inside the
    # support of the target
    F = faces_as_partitions(P)
    chambers = [x for x in F if len(x) == P.n]
    cidx = {c: i for i, c in enumerate(chambers)}
    # chambers of the band are exactly L(P), matched through the prefix chain
    assert len(chambers) == m
    maps = set()
    for x in F:
        f = tuple(cidx[prod(x, c)] for c in chambers)
        if all(Pl[i][f[i]] != 0 for i in range(m)):
            maps.add(f)
    maps = sorted(maps)
    if not maps:
        return "NOT a Brown walk", None
    rows = []
    rhs = []
    for i in range(m):
        for j in range(m):
            rows.append([1 if f[i] == j else 0 for f in maps])
            rhs.append(Pl[i][j])
    rows.append([1] * len(maps))
    rhs.append(Fraction(1))
    ok, x = feasible(rows, rhs)
    if not ok:
        return "NOT a Brown walk", None
    wit = [(maps[k], x[k]) for k in range(len(maps)) if x[k] != 0]
    return "IS a Brown walk", wit


def unreachable_edge_test(P):
    """The deliverable's own sufficient test, rebuilt: is some AT edge
    unreachable from the candidate faces?"""
    les, adj = at_graph(P)
    m = len(les)
    if m < 2:
        return "vacuous"
    F = faces_as_partitions(P)
    chambers = [x for x in F if len(x) == P.n]
    cidx = {c: i for i, c in enumerate(chambers)}
    cand = []
    for x in F:
        f = tuple(cidx[prod(x, c)] for c in chambers)
        if all(f[i] == i or f[i] in adj[i] for i in range(m)):
            cand.append(f)
    reach = set()
    for f in cand:
        for i in range(m):
            reach.add((i, f[i]))
    for i in range(m):
        for j in adj[i]:
            if (i, j) not in reach:
                return "NOT a Brown walk"
    return "undecided by this test"


def main():
    hi = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print("=" * 78)
    print("AUDIT §9: the face semigroup, independently rebuilt")
    print("=" * 78)
    print("\n1-2. band axioms and supports == acyclic partitions")
    for n in range(1, min(hi, 5) + 1):
        a, b, c = check_band(n)
        print("    n=%d  axiom violations=%d  associativity violations=%s  "
              "support mismatches=%d" % (n, a, b if n <= 4 else "(skipped)", c))

    print("\n3. Brown multiplicities: nonnegative integers summing to |L(P)|")
    for n in range(1, hi + 1):
        neg = wrong = tot = 0
        for P in posets_upto_iso(n):
            F = faces_as_partitions(P)
            L = sorted({frozenset(x) for x in F},
                       key=lambda X: (len(X), sorted(X)))
            mX = multiplicities(P, L)
            tot += 1
            if any(v < 0 for v in mX.values()):
                neg += 1
            if sum(mX.values()) != len(linexts(P)):
                wrong += 1
        print("    n=%d  posets=%3d  negative m_X: %d   sum != |L(P)|: %d"
              % (n, tot, neg, wrong))

    print("\n4. predicted spectrum vs the actual matrix (exact rational ranks)")
    print("   SIX weight families -- the deliverable used three.  Identical")
    print("   multiplicities m_X are reused across all six, which is what")
    print("   'independent of w' has to mean operationally.")
    for n in range(2, min(hi, 4) + 1):
        tally = check_spectrum(n, verbose=True)
        for name in sorted(tally):
            t = tally[name]
            print("    n=%d  %-22s  correct on %2d of %2d" % (n, name, t[1], t[0]))

    print("\n5. §9.4 DECIDED, not left undecided: exact rational LP")
    for n in range(2, hi + 1):
        notb = isb = vac = 0
        details = []
        for P in posets_upto_iso(n):
            v, wit = decide_brown(P)
            t = unreachable_edge_test(P)
            if v == "vacuous":
                vac += 1
            elif v == "NOT a Brown walk":
                notb += 1
            else:
                isb += 1
            if t == "undecided by this test":
                details.append((P, v, wit))
        print("    n=%d  NOT a Brown walk: %2d   IS a Brown walk: %2d   "
              "vacuous: %d" % (n, notb, isb, vac))
        for P, v, wit in details:
            print("        [test said UNDECIDED]  %-34s |L(P)|=%2d  ->  %s"
                  % (P.tag(), len(linexts(P)), v))
            if wit is not None and n <= 5:
                print("            witness w:", ", ".join(
                    "%s on %s" % (val, list(f)) for f, val in wit))


if __name__ == "__main__":
    main()
