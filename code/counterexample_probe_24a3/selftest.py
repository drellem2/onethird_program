"""Controls for the mg-24a3 probe.  Every derived route is checked against a
brute-force route that shares no code with it.  Run before the probe; the probe
refuses to report if any control fails.
"""

from fractions import Fraction

import core
from core import (Poset, PartitionLattice, all_posets_bruteforce,
                  all_posets_by_extension, linear_extensions, restriction_counts,
                  pair_before_counts, delta_of, levels_of, multiplicities,
                  moves_of, act, support_index, uniform_move_spectrum,
                  move_pair_stats, order_ideals)

# A000112: number of posets on n unlabelled points.
POSET_COUNTS = {1: 1, 2: 2, 3: 5, 4: 16, 5: 63, 6: 318, 7: 2045}

FAILURES = []


def check(name, ok, detail=""):
    status = "ok  " if ok else "FAIL"
    print("  [%s] %s%s" % (status, name, ("  -- " + detail) if detail else ""))
    if not ok:
        FAILURES.append(name)
    return ok


# --------------------------------------------------------------------------

def control_enumeration():
    print("C1  poset enumeration against A000112, and the two routes against each other")
    small = {0: [Poset(0, [])]}
    prev = [Poset(1, [])]
    small[1] = prev
    ok_all = True
    for n in range(2, 8):
        by_ext = all_posets_by_extension(n, prev)
        ok_all &= check("n=%d  extension route gives %d classes" % (n, len(by_ext)),
                        len(by_ext) == POSET_COUNTS[n],
                        "expected %d" % POSET_COUNTS[n])
        if n <= 6:
            bf = all_posets_bruteforce(n)
            k1 = set(P.canonical_key() for P in by_ext)
            k2 = set(P.canonical_key() for P in bf)
            ok_all &= check("n=%d  brute-force route agrees set-for-set" % n, k1 == k2,
                            "%d vs %d" % (len(k1), len(k2)))
        prev = by_ext
    return ok_all


def control_canonical_key():
    """The refined-invariant key minimises over a SUBSET of S_n (the relabellings
    that respect the refined vertex invariant), so it need not equal the global
    lexicographic minimum -- and it does not.  What has to be true is that it is
    a complete isomorphism invariant: constant on isomorphism classes, and
    distinct on distinct ones.  Both are checked directly."""
    print("C2  canonical key is a COMPLETE isomorphism invariant")
    from itertools import permutations as _perms
    bad_const = bad_sep = 0
    tot_rel = 0
    ncls = 0
    for n in (3, 4, 5):
        posets = all_posets_bruteforce(n)
        # (i) constant on isomorphism classes: relabel each poset every which way
        for P in posets:
            k = P.canonical_key()
            for g in _perms(range(n)):
                tot_rel += 1
                Q = Poset(n, [(g[a], g[b]) for (a, b) in P.less])
                if Q.canonical_key() != k:
                    bad_const += 1
        # (ii) separates: as many keys as brute-force classes
        keys = set(P.canonical_key() for P in posets)
        bfk = set(P.canonical_key_bruteforce() for P in posets)
        ncls += len(bfk)
        if len(keys) != len(bfk):
            bad_sep += 1
    ok = check("constant under relabelling: 0 bad of %d relabellings" % tot_rel,
               bad_const == 0, "%d bad" % bad_const)
    ok &= check("separates non-isomorphic posets (%d classes at n=3,4,5)" % ncls,
                bad_sep == 0, "%d n bad" % bad_sep)
    # the key deliberately differs from the global lex minimum; record how often
    diff = sum(1 for n in (3, 4, 5) for P in all_posets_bruteforce(n)
               if P.canonical_key() != P.canonical_key_bruteforce())
    print("       (for the record: differs from the global lex minimum on %d of %d "
          "posets -- expected, and harmless)" % (diff, ncls))
    return ok


def control_restriction_and_pairs():
    print("C3  restriction counts and pair marginals against direct enumeration of L(P)")
    bad_e = bad_p = 0
    tot_e = tot_p = 0
    for n in (2, 3, 4, 5):
        for P in all_posets_bruteforce(n):
            e = restriction_counts(P)
            # e[S] against enumerating L(P|_S) directly
            for S in range(1 << n):
                elems = [i for i in range(n) if (S >> i) & 1]
                idx = {x: k for k, x in enumerate(elems)}
                rel = [(idx[a], idx[b]) for (a, b) in P.less if a in idx and b in idx]
                tot_e += 1
                if e[S] != len(linear_extensions(Poset(len(elems), rel))):
                    bad_e += 1
            les = linear_extensions(P)
            before = pair_before_counts(P, e)
            for x in range(n):
                for y in range(n):
                    if x == y:
                        continue
                    tot_p += 1
                    direct = sum(1 for w in les if w.index(x) < w.index(y))
                    if before[(x, y)] != direct:
                        bad_p += 1
    ok = check("e(P|_S) for every subset: 0 bad of %d" % tot_e, bad_e == 0, "%d bad" % bad_e)
    ok &= check("pair before-counts: 0 bad of %d" % tot_p, bad_p == 0, "%d bad" % bad_p)
    return ok


def control_levels_are_move_supports():
    print("C4  levels (acyclic quotients) == supports of P-compatible moves")
    bad = 0
    tot = 0
    for n in (2, 3, 4, 5):
        lat = PartitionLattice(n)
        for P in all_posets_bruteforce(n):
            byacyc = set(levels_of(P, lat))
            bysupp = set(support_index(mv, lat) for mv in moves_of(P))
            tot += 1
            if byacyc != bysupp:
                bad += 1
    return check("0 disagreements of %d posets" % tot, bad == 0, "%d bad" % bad)


def control_action_wellposed():
    print("C5  the action lands in L(P), and composition of moves matches")
    badA = badC = 0
    totA = totC = 0
    for n in (3, 4):
        for P in all_posets_bruteforce(n):
            les = set(linear_extensions(P))
            mvs = moves_of(P)
            for mv in mvs:
                for w in les:
                    totA += 1
                    if act(mv, w) not in les:
                        badA += 1
            # x.(y.c) == (x.y).c  with x.y the lexicographic intersection product
            for x in mvs:
                for y in mvs:
                    prod = tuple(B for Bx in x for B in
                                 [Bx & By for By in y] if B)
                    for w in les:
                        totC += 1
                        if act(x, act(y, w)) != act(prod, w):
                            badC += 1
    ok = check("action closed in L(P): 0 bad of %d" % totA, badA == 0, "%d bad" % badA)
    ok &= check("x.(y.c) == (x.y).c: 0 bad of %d" % totC, badC == 0, "%d bad" % badC)
    return ok


def _rank_exact(rows, ncols):
    """Exact rank of a matrix given as a list of lists of Fractions."""
    rows = [list(r) for r in rows]
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, len(rows)):
            if rows[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        pv = rows[r][c]
        for i in range(r + 1, len(rows)):
            if rows[i][c] != 0:
                f = rows[i][c] / pv
                for j in range(c, ncols):
                    rows[i][j] -= f * rows[r][j]
        r += 1
        if r == len(rows):
            break
    return r


def control_spectrum_against_matrix():
    print("C6  predicted spectrum against dim ker(M - lambda I) on the actual matrix")
    bad = 0
    tot = 0
    detail = []
    for n in (2, 3, 4):
        lat = PartitionLattice(n)
        for P in all_posets_bruteforce(n):
            les = linear_extensions(P)
            if len(les) > 24:
                continue
            pos = {w: k for k, w in enumerate(les)}
            N = len(les)
            mvs = moves_of(P)
            nm = len(mvs)
            M = [[Fraction(0) for _ in range(N)] for _ in range(N)]
            for mv in mvs:
                for w in les:
                    M[pos[act(mv, w)]][pos[w]] += Fraction(1, nm)
            e = restriction_counts(P)
            lidx = levels_of(P, lat)
            mult = multiplicities(P, lat, lidx, e)
            lam, lam2, _, _ = uniform_move_spectrum(P, lat, lidx, mult)
            # predicted multiplicity of each distinct NUMBER
            pred = {}
            for X in lidx:
                if mult[X]:
                    pred[lam[X]] = pred.get(lam[X], 0) + mult[X]
            tot += 1
            total_dim = 0
            okhere = True
            for val, mu in pred.items():
                A = [[M[i][j] - (val if i == j else 0) for j in range(N)] for i in range(N)]
                dimker = N - _rank_exact(A, N)
                total_dim += dimker
                if dimker != mu:
                    okhere = False
            if total_dim != N or not okhere:
                bad += 1
                detail.append("n=%d %s" % (n, P.cover_string()))
    return check("0 bad of %d posets (multiplicities matched AND dims sum to |L(P)|)" % tot,
                 bad == 0, ";".join(detail[:3]))


def control_multiplicity_identities():
    print("C7  sum of multiplicities == e(P), all multiplicities >= 0")
    bad_sum = bad_neg = 0
    tot = 0
    for n in (2, 3, 4, 5, 6):
        lat = PartitionLattice(n)
        posets = all_posets_bruteforce(n) if n <= 6 else []
        for P in posets:
            e = restriction_counts(P)
            lidx = levels_of(P, lat)
            mult = multiplicities(P, lat, lidx, e)
            tot += 1
            if sum(mult.values()) != e[(1 << n) - 1]:
                bad_sum += 1
            if any(v < 0 for v in mult.values()):
                bad_neg += 1
    ok = check("sum m_X == e(P): 0 bad of %d" % tot, bad_sum == 0, "%d bad" % bad_sum)
    ok &= check("all m_X >= 0: 0 bad of %d" % tot, bad_neg == 0, "%d bad" % bad_neg)
    return ok


def control_stationary_pair_marginal():
    print("C8  pi(x<y) = q(x<y)/(q(x<y)+q(y<x)) against the stationary vector of M")
    bad = 0
    tot = 0
    for n in (2, 3, 4):
        for P in all_posets_bruteforce(n):
            les = linear_extensions(P)
            if len(les) > 24 or not P.incomparable_pairs():
                continue
            pos = {w: k for k, w in enumerate(les)}
            N = len(les)
            mvs = moves_of(P)
            nm = len(mvs)
            M = [[Fraction(0) for _ in range(N)] for _ in range(N)]
            for mv in mvs:
                for w in les:
                    M[pos[act(mv, w)]][pos[w]] += Fraction(1, nm)
            # stationary vector: solve (M - I) v = 0, sum v = 1
            rows = [[M[i][j] - (1 if i == j else 0) for j in range(N)] + [Fraction(0)]
                    for i in range(N)]
            rows.append([Fraction(1)] * N + [Fraction(1)])
            v = _solve(rows, N)
            stats = move_pair_stats(P, mvs)
            for (x, y), (s, qx, qy, pi_pred) in stats.items():
                tot += 1
                actual = sum(v[pos[w]] for w in les if w.index(x) < w.index(y))
                if pi_pred is None or actual != pi_pred:
                    bad += 1
    return check("0 bad of %d incomparable pairs" % tot, bad == 0, "%d bad" % bad)


def _solve(rows, ncols):
    """Exact solve of an overdetermined consistent system; returns the unique
    solution (the systems here have a one-dimensional kernel pinned by the
    normalisation row)."""
    rows = [list(r) for r in rows]
    piv_of = []
    r = 0
    for c in range(ncols):
        p = None
        for i in range(r, len(rows)):
            if rows[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        pv = rows[r][c]
        rows[r] = [x / pv for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        piv_of.append(c)
        r += 1
        if r == len(rows):
            break
    v = [Fraction(0)] * ncols
    for i, c in enumerate(piv_of):
        v[c] = rows[i][ncols]
    return v


def control_delta_known_values():
    print("C9  delta against hand-known values")
    ok = True
    # antichain on 2: single pair, p = 1/2
    P = Poset(2, [])
    e = restriction_counts(P); b = pair_before_counts(P, e)
    d, _, _ = delta_of(P, e, b)
    ok &= check("antichain n=2: delta = 1/2", d == Fraction(1, 2), str(d))
    # 2-chain plus an isolated point: the tight 3-element poset, delta = 1/3
    P = Poset(3, [(0, 1)])
    e = restriction_counts(P); b = pair_before_counts(P, e)
    d, _, _ = delta_of(P, e, b)
    ok &= check("2-chain + point: delta = 1/3", d == Fraction(1, 3), str(d))
    # chain: no incomparable pair
    P = Poset(3, [(0, 1), (1, 2)])
    e = restriction_counts(P); b = pair_before_counts(P, e)
    d, _, _ = delta_of(P, e, b)
    ok &= check("3-chain: delta undefined", d is None, str(d))
    # antichain on 3: every pair p = 1/2
    P = Poset(3, [])
    e = restriction_counts(P); b = pair_before_counts(P, e)
    d, dmin, _ = delta_of(P, e, b)
    ok &= check("antichain n=3: delta = min-pair = 1/2",
                d == Fraction(1, 2) and dmin == Fraction(1, 2), "%s %s" % (d, dmin))
    return ok


def control_note_worked_example():
    print("C10 the worked example of docs/OneThird-Semigroup-Walk-Family-Note.md")
    #   P = {a<b, c<d} on a,b,c,d = 0,1,2,3
    P = Poset(4, [(0, 1), (2, 3)])
    lat = PartitionLattice(4)
    e = restriction_counts(P)
    lidx = levels_of(P, lat)
    mult = multiplicities(P, lat, lidx, e)
    ok = check("6 linear extensions", e[15] == 6, str(e[15]))
    ok &= check("26 P-compatible moves", len(moves_of(P)) == 26, str(len(moves_of(P))))
    ok &= check("14 of the 15 partitions are levels", len(lidx) == 14, str(len(lidx)))
    missing = [lat.parts[i] for i in range(len(lat.parts)) if i not in set(lidx)]
    ok &= check("the missing one is {a,d}|{b,c}",
                len(missing) == 1 and sorted(missing[0]) == sorted((0b1001, 0b0110)),
                str(missing))
    nz = sorted(lat.nblocks[i] for i in lidx if mult[i] > 0)
    ok &= check("six levels carry m>0, block counts 2,3,3,3,3,4", nz == [2, 3, 3, 3, 3, 4], str(nz))
    ok &= check("all nonzero multiplicities are 1",
                all(mult[i] == 1 for i in lidx if mult[i] > 0), "")
    return ok


def main():
    print("=" * 78)
    print("CONTROLS for the mg-24a3 counterexample-detection probe")
    print("=" * 78)
    for fn in (control_enumeration, control_canonical_key, control_restriction_and_pairs,
               control_levels_are_move_supports, control_action_wellposed,
               control_spectrum_against_matrix, control_multiplicity_identities,
               control_stationary_pair_marginal, control_delta_known_values,
               control_note_worked_example):
        fn()
        print()
    print("=" * 78)
    if FAILURES:
        print("CONTROLS FAILED: %s" % ", ".join(FAILURES))
        return 1
    print("ALL CONTROLS PASS")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
