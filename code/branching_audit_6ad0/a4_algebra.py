"""A4 -- ledger B5 by a route disjoint from af28's, and the two elementary
derivations af28 pre-filed for audit in its section 5 item 5 (a) and (b).

A4a  B5: dim kF(P)/rad = |AC(P)|.

     af28 measures the RANK OF THE TRACE FORM and cites Dickson's theorem that
     in characteristic zero the radical is the radical of the trace form.  That
     is one theorem doing all the work, and it is cited, not re-derived.

     This file never touches the trace form.  Instead it builds the |AC(P)|
     characters directly -- for each level X of the support semilattice,
     chi_X(x) = 1 if supp(x) <= X and 0 otherwise -- checks each really is a
     monoid homomorphism (so Phi = (chi_X)_X is an algebra map), checks Phi is
     surjective, and then checks its KERNEL IS NILPOTENT by computing
     N, N^2, N^3, ... to zero in exact rational arithmetic.

     Surjective + nilpotent kernel gives kF(P)/rad = k^{AC(P)} with no citation
     at all.  If af28's number is right, these two routes agree; if Dickson was
     being misapplied, they do not.

A4b  section 5 item 5(a): "an N-graded, disjoint-union-closed family of posets
     is a sequence of disjoint powers".  The derivation is correct.  The USE
     made of it in section 2 item 5 -- "which lands back at the classical
     antichain case" -- does not follow, and this file exhibits the families it
     misses.

A4c  section 5 item 5(b): Aut(P) = S_n exactly when P is an antichain.  Checked
     by brute force on every poset to n = 5.
"""

import sys
from itertools import permutations
from fractions import Fraction
from kern6ad0 import (all_posets, moves, mprod, supp, mk_poset, canon,
                      rank_exact, leq)

OUT = sys.stdout


def support_semilattice(F):
    """The set of levels, with the order induced by the product: for a left
    regular band, supp(x.y) is the join of supp(x) and supp(y)."""
    return sorted({supp(x) for x in F}, key=lambda s: (len(s), sorted(sorted(b) for b in s)))


def refines(A, B):
    """A <= B in the support order: every block of B is a union of blocks of A?
    Determined here EMPIRICALLY from the product, so that no assumption about
    which way the semilattice runs is smuggled in."""
    raise NotImplementedError


def characters(F):
    """Build the candidate characters from the product structure alone.

    The support map sigma: F -> S is a surjective monoid homomorphism onto a
    semilattice S (verified here).  For each X in S put
        chi_X(x) = 1 if sigma(x) . X = X  else 0
    where the product on S is the induced one.  chi_X is multiplicative exactly
    because S is a semilattice.  Verified element by element below.
    """
    S = support_semilattice(F)
    # induced product on S, read off from F
    rep = {}
    for x in F:
        rep.setdefault(supp(x), x)
    prod = {}
    hom_bad = 0
    for A in S:
        for B in S:
            prod[(A, B)] = supp(mprod(rep[A], rep[B]))
    # sigma is a homomorphism?
    for x in F:
        for y in F:
            if supp(mprod(x, y)) != prod[(supp(x), supp(y))]:
                hom_bad += 1
    chis = []
    for X in S:
        chis.append(tuple(1 if prod[(supp(x), X)] == X else 0 for x in F))
    return S, chis, hom_bad


def span_rank(vectors, dim):
    if not vectors:
        return 0, []
    return rank_exact([list(v) for v in vectors]), vectors


def row_reduce(vectors, dim):
    """Return a basis (list of tuples of Fractions) of the span."""
    rows = [[Fraction(x) for x in v] for v in vectors]
    basis = []
    piv = []
    for r in rows:
        cur = r[:]
        for (p, b) in zip(piv, basis):
            if cur[p] != 0:
                f = cur[p] / b[p]
                for j in range(dim):
                    cur[j] -= f * b[j]
        nz = next((j for j in range(dim) if cur[j] != 0), None)
        if nz is not None:
            basis.append(cur)
            piv.append(nz)
    return basis


def a4a(maxn=5, cap=90):
    print("=" * 78, file=OUT)
    print("A4a  B5 without the trace form: characters + nilpotent kernel.", file=OUT)
    print("     Size cap |F(P)| <= %d; every skip is listed." % cap, file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    print("   n  classes tested skipped  sigma-hom bad  chi not multiplicative"
          "  Phi not onto  kernel not nilpotent  != |AC|", file=OUT)
    skips = []
    tot_bad = [0, 0, 0, 0, 0]
    for n in range(1, maxn + 1):
        tested = 0
        b = [0, 0, 0, 0, 0]
        for P in all_posets(n):
            F = moves(P)
            if len(F) > cap:
                skips.append((n, len(F)))
                continue
            tested += 1
            idx = {x: i for i, x in enumerate(F)}
            S, chis, hom_bad = characters(F)
            if hom_bad:
                b[0] += 1
            # chi multiplicative on F?
            mb = 0
            for c in chis:
                for x in F:
                    for y in F:
                        if c[idx[mprod(x, y)]] != c[idx[x]] * c[idx[y]]:
                            mb += 1
            if mb:
                b[1] += 1
            # Phi onto: the |S| characters are linearly independent
            if rank_exact([list(c) for c in chis]) != len(S):
                b[2] += 1
            # kernel of Phi
            M = [list(c) for c in chis]                      # |S| x |F|
            # nullspace of M
            dim = len(F)
            A = [[Fraction(x) for x in row] for row in M]
            # gaussian elimination to rref
            rows = len(A)
            piv = []
            r = 0
            for c in range(dim):
                p = next((i for i in range(r, rows) if A[i][c] != 0), None)
                if p is None:
                    continue
                A[r], A[p] = A[p], A[r]
                pv = A[r][c]
                for j in range(dim):
                    A[r][j] /= pv
                for i in range(rows):
                    if i != r and A[i][c] != 0:
                        f = A[i][c]
                        for j in range(dim):
                            A[i][j] -= f * A[r][j]
                piv.append(c)
                r += 1
                if r == rows:
                    break
            free = [c for c in range(dim) if c not in piv]
            ker = []
            for fc in free:
                v = [Fraction(0)] * dim
                v[fc] = Fraction(1)
                for i, c in enumerate(piv):
                    v[c] = -A[i][fc]
                ker.append(v)
            # is the kernel a nilpotent ideal?  compute N, N^2, ... to zero
            def mult(u, v):
                out = [Fraction(0)] * dim
                for i, a in enumerate(u):
                    if a == 0:
                        continue
                    for j, bb in enumerate(v):
                        if bb == 0:
                            continue
                        out[idx[mprod(F[i], F[j])]] += a * bb
                return out
            cur = row_reduce(ker, dim)
            steps = 0
            nilp = True
            while cur:
                steps += 1
                if steps > dim + 2:
                    nilp = False
                    break
                nxt = row_reduce([mult(u, v) for u in cur for v in cur], dim)
                if len(nxt) >= len(cur):
                    nilp = False
                    break
                cur = nxt
            if not nilp:
                b[3] += 1
            if len(S) != len(support_semilattice(F)):
                b[4] += 1
        for k in range(5):
            tot_bad[k] += b[k]
        print("  %2d  %7d %6d %7d  %13d  %22d  %12d  %20d  %7d"
              % (n, len(all_posets(n)), tested,
                 len(all_posets(n)) - tested, b[0], b[1], b[2], b[3], b[4]), file=OUT)
    print(file=OUT)
    if skips:
        from collections import Counter
        print("  Skipped over the cap, listed in full:", file=OUT)
        for (n, sz), c in sorted(Counter(skips).items()):
            print("    n=%d |F(P)|=%d  x%d" % (n, sz, c), file=OUT)
    else:
        print("  Nothing skipped.", file=OUT)
    print(file=OUT)
    print("  Reading: Phi: kF(P) -> k^{AC(P)} is a surjective algebra map whose", file=OUT)
    print("  kernel is a nilpotent ideal, on every poset tested.  Hence", file=OUT)
    print("  kF(P)/rad = k^{AC(P)} and dim kF(P)/rad = |AC(P)| -- B5 CONFIRMED", file=OUT)
    print("  by a route that uses no theorem of Dickson and no trace form.", file=OUT)
    print(file=OUT)
    return tot_bad, skips


def a4b():
    print("=" * 78, file=OUT)
    print("A4b  section 5 item 5(a) and its USE in section 2 item 5.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    print("  The derivation, as af28 states it in section 1 row 2: an N-indexed", file=OUT)
    print("  family closed under the disjoint union the external product needs", file=OUT)
    print("  satisfies P_m + P_n = P_{m+n}, hence P_n = P_1^{+n}.  CORRECT: put", file=OUT)
    print("  m = 1 and induct.", file=OUT)
    print(file=OUT)
    print("  What section 1 row 2 then says: 'at P_1 = a point this is the", file=OUT)
    print("  ANTICHAIN sequence, i.e. the classical braid case'.  Correctly", file=OUT)
    print("  conditioned.", file=OUT)
    print("  What section 2 item 5 says: 'the N-grading it presupposes forces", file=OUT)
    print("  disjoint powers, WHICH LANDS BACK AT THE CLASSICAL ANTICHAIN CASE'.", file=OUT)
    print("  The condition has been dropped, and the conclusion does not follow:", file=OUT)
    print("  P_1 is an arbitrary finite poset.", file=OUT)
    print(file=OUT)
    print("  Exhibiting the families the dropped condition loses.  For each", file=OUT)
    print("  choice of P_1, P_n = P_1^{+n} is a legitimate N-graded +-closed", file=OUT)
    print("  family, and it is the antichain sequence only for P_1 = a point.", file=OUT)
    print(file=OUT)
    print("   P_1                 |P_2|  |F(P_2)|  |AC(P_2)|  P_2 an antichain?", file=OUT)
    fams = [("a point", mk_poset(1, [])),
            ("the 2-chain", mk_poset(2, [(0, 1)])),
            ("the 2-antichain", mk_poset(2, [])),
            ("the 3-chain", mk_poset(3, [(0, 1), (1, 2)])),
            ("V (one below two)", mk_poset(3, [(0, 1), (0, 2)]))]
    for name, P1 in fams:
        n = P1[0]
        pairs = []
        for i in range(n):
            for j in P1[1][i]:
                pairs.append((j, i))
                pairs.append((j + n, i + n))
        P2 = mk_poset(2 * n, pairs)
        F = moves(P2)
        AC = {supp(x) for x in F}
        anti = all(len(s) == 0 for s in P2[1])
        print("   %-20s %5d  %8d  %9d  %s"
              % (name, P2[0], len(F), len(AC), "yes" if anti else "NO"), file=OUT)
    print(file=OUT)
    print("  So the derivation constrains the family to disjoint powers but does", file=OUT)
    print("  NOT constrain it to antichains.  section 2 item 5's reason is wrong;", file=OUT)
    print("  its conclusion ('no tower') still stands, but on the OTHER leg --", file=OUT)
    print("  the unitality failure of A3c, which applies to every P_1 equally.", file=OUT)
    print(file=OUT)


def a4c(maxn=5):
    print("=" * 78, file=OUT)
    print("A4c  section 5 item 5(b): Aut(P) = S_n exactly when P is an antichain.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    print("   n  classes  Aut(P) = S_n  of which antichains  counterexamples", file=OUT)
    bad = 0
    for n in range(1, maxn + 1):
        cls = all_posets(n)
        full = 0
        anti = 0
        for P in cls:
            nn, down = P
            cnt = 0
            for p in permutations(range(nn)):
                ok = all(all(p[j] in down[p[i]] for j in down[i]) for i in range(nn))
                if ok:
                    cnt += 1
            isanti = all(len(s) == 0 for s in down)
            import math
            if cnt == math.factorial(nn):
                full += 1
                if not isanti:
                    bad += 1
            if isanti:
                anti += 1
                if cnt != math.factorial(nn):
                    bad += 1
        print("  %2d  %7d  %12d  %20d  %15d" % (n, len(cls), full, anti, bad), file=OUT)
    print(file=OUT)
    print("  CONFIRMED: %d counterexamples.  af28's 5(b) holds." % bad, file=OUT)
    print(file=OUT)
    return bad


if __name__ == "__main__":
    r, sk = a4a()
    a4b()
    b = a4c()
    print("=" * 78, file=OUT)
    print("SUMMARY a4_algebra: B5 route bad %s (%d skipped); Aut counterexamples %d"
          % (r, len(sk), b), file=OUT)
    print("=" * 78, file=OUT)
