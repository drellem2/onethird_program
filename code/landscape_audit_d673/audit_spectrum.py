#!/usr/bin/env python3
"""
mg-d673 INDEPENDENT AUDIT of mg-ebd8 / 714aceb -- instrument 2 of 3.

THE CLOSED FORM, TESTED AGAINST THE ACTUAL MATRIX, IN EXACT RATIONALS.

The target checked its Brown-Theorem-2 closed form
    m_X = prod_{B in X} (|B|-1)!   if every block of X is an antichain of P
    m_X = 0                        otherwise
against "the repo's own triangular solve".  Both sides of that comparison are
solutions of the SAME counting identity, so a shared misreading of what the
identity indexes cannot be caught from inside it -- which is exactly how a
canonicalisation bug returned labelled counts for isomorphism classes earlier
in this arc.

This instrument does not use the counting identity at all.  It builds the
|L(P)| x |L(P)| transition matrix of the walk for explicit rational weights,
and computes dim ker(M - lambda I) by exact Gaussian elimination over
Fraction.  If the predicted spectrum is right, the dimensions sum to |L(P)|
(which also proves M diagonalisable) and each matches the predicted
multiplicity.

It also re-derives numbers the EXISTING pipeline already carries, so that a
disagreement can surface:
  * the note's sec 5a level->multiplicity table for P = {a<b, c<d} (14 levels,
    six carrying multiplicity, sum 6);
  * the note's sec 5b eigenvalues under its three published weightings w1, w2,
    w3, including the w2 collision at 11/32 with dim ker 2.

Pure Python 3, no third-party imports.  Shares no code with
code/landscape_ebd8/, code/semigroup_note/, code/face_geometry/ or
code/hodge_leverage/.
"""

import sys
from fractions import Fraction
from math import factorial

from audit_populations import (iso_classes, F_of_P, AC_by_acyclicity,
                               linear_extensions, leq_matrix, refines)


# --------------------------------------------------------------------------
# the walk
# --------------------------------------------------------------------------


def act(move, word):
    """move . word in F(P): blocks of the product are the non-empty
    B_p n C_q in lexicographic (p,q) order.  With `word` an ordering (all
    singleton blocks) this is: list the blocks of `move` in order, each block's
    elements in the order they appear in `word`."""
    out = []
    for B in move:
        out.extend([x for x in word if x in B])
    return tuple(out)


def support(move):
    return tuple(sorted(move, key=lambda s: sorted(s)))


def transition_matrix(moves, weights, words):
    idx = {w: i for i, w in enumerate(words)}
    e = len(words)
    M = [[Fraction(0) for _ in range(e)] for _ in range(e)]
    for mv, w in zip(moves, weights):
        if w == 0:
            continue
        for c in words:
            M[idx[act(mv, c)]][idx[c]] += w
    return M


def predicted_spectrum(rel, n, moves, weights):
    """eigenvalue at level X = total weight of the moves whose support is
    COARSER THAN OR EQUAL TO X; multiplicity from the closed form."""
    le = leq_matrix(rel, n)
    ac = sorted(AC_by_acyclicity(rel, n), key=lambda p: (len(p), sorted(sorted(b) for b in p)))
    supp = [support(m) for m in moves]
    out = []
    for X in ac:
        lam = sum(w for s, w in zip(supp, weights) if refines(X, s))
        anti = all(not (le[i][j] or le[j][i])
                   for B in X for i in B for j in B if i != j)
        m = 1
        if anti:
            for B in X:
                m *= factorial(len(B) - 1)
        else:
            m = 0
        out.append((X, lam, m))
    return out


# --------------------------------------------------------------------------
# exact linear algebra
# --------------------------------------------------------------------------


def nullity(M, lam):
    """dim ker(M - lam I) by exact Gaussian elimination over Fraction."""
    e = len(M)
    A = [[M[i][j] - (lam if i == j else 0) for j in range(e)] for i in range(e)]
    rank = 0
    row = 0
    for col in range(e):
        piv = None
        for r in range(row, e):
            if A[r][col] != 0:
                piv = r
                break
        if piv is None:
            continue
        A[row], A[piv] = A[piv], A[row]
        pv = A[row][col]
        A[row] = [x / pv for x in A[row]]
        for r in range(e):
            if r != row and A[r][col] != 0:
                f = A[r][col]
                A[r] = [a - f * b for a, b in zip(A[r], A[row])]
        row += 1
        rank += 1
        if row == e:
            break
    return e - rank


# --------------------------------------------------------------------------
# generic weights
# --------------------------------------------------------------------------

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
          67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]


def generic_weights(k):
    """distinct, deterministic, summing to 1"""
    raw = []
    p = 0
    for i in range(k):
        raw.append(PRIMES[i % len(PRIMES)] + 1000 * (i // len(PRIMES)) + i)
    tot = sum(raw)
    return [Fraction(r, tot) for r in raw]


# --------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------


def check_poset(rel, n, verbose=False):
    moves = F_of_P(rel, n)
    words = linear_extensions(rel, n)
    weights = generic_weights(len(moves))
    spec = predicted_spectrum(rel, n, moves, weights)

    # (a) the closed form's multiplicities sum to |L(P)|
    tot = sum(m for (_, _, m) in spec)
    ok_sum = (tot == len(words))

    # (b) actual dim ker per DISTINCT predicted eigenvalue
    M = transition_matrix(moves, weights, words)
    groups = {}
    for (X, lam, m) in spec:
        groups.setdefault(lam, 0)
        groups[lam] += m
    ok_dims = True
    dimsum = 0
    detail = []
    for lam in sorted(groups, reverse=True):
        d = nullity(M, lam)
        dimsum += d
        detail.append((lam, groups[lam], d))
        if d != groups[lam]:
            ok_dims = False
    ok_diag = (dimsum == len(words))
    return ok_sum, ok_dims, ok_diag, tot, len(words), detail, len(moves), len(spec)


# --------------------------------------------------------------------------
# the worked example, against the NOTE's own published tables
# --------------------------------------------------------------------------

NAMES = "abcd"


def fmt(part):
    return "|".join("".join(NAMES[x] for x in sorted(B))
                    for B in sorted(part, key=lambda s: sorted(s)))


def worked_example():
    n = 4
    rel = frozenset({(0, 1), (2, 3)})           # a<b, c<d
    moves = F_of_P(rel, n)
    words = linear_extensions(rel, n)
    print("  |F(P)| = %d moves, |L(P)| = %d linear extensions, |AC(P)| = %d levels"
          % (len(moves), len(words), len(AC_by_acyclicity(rel, n))))
    print()

    # --- the note's sec 5a table, re-derived from the closed form ---
    NOTE_5A = {                     # docs/OneThird-Semigroup-Walk-Family-Note.md sec 5a
        "a|b|c|d": 1, "ac|b|d": 1, "ad|b|c": 1, "a|bc|d": 1, "a|bd|c": 1,
        "ab|c|d": 0, "a|b|cd": 0, "ac|bd": 1, "ab|cd": 0, "abc|d": 0,
        "abd|c": 0, "acd|b": 0, "a|bcd": 0, "abcd": 0,
    }
    w = generic_weights(len(moves))
    spec = predicted_spectrum(rel, n, moves, w)
    print("  sec 5a: level -> multiplicity, closed form vs the note's published table")
    bad = 0
    for (X, lam, m) in spec:
        key = fmt(X)
        exp = NOTE_5A.get(key)
        ok = "OK" if exp == m else "*** MISMATCH ***"
        if exp != m:
            bad += 1
        print("     %-10s closed form %d   note %s   %s" % (key, m, exp, ok))
    print("     sum of multiplicities = %d, |L(P)| = %d  -> %s"
          % (sum(m for _, _, m in spec), len(words),
             "OK" if sum(m for _, _, m in spec) == len(words) else "MISMATCH"))
    print("     levels covered: %d of %d in the note's table; disagreements: %d"
          % (len(spec), len(NOTE_5A), bad))
    print()

    # --- the note's sec 5b eigenvalues, three published weightings ---
    W = {
        "abcd":     (4, 8, 2),
        "a|bcd":    (6, 4, 3),
        "ac|bd":    (2, 3, 5),
        "ac|b|d":   (3, 2, 1),
        "a|bc|d":   (5, 6, 6),
        "c|ad|b":   (7, 3, 7),
        "a|c|bd":   (1, 2, 4),
        "a|b|c|d":  (4, 4, 4),
    }

    def ordered_name(mv):
        return "|".join("".join(NAMES[x] for x in sorted(B)) for B in mv)

    NOTE_5B = {   # level -> (w1, w2, w3) as thirty-secondths
        "ac|bd":   (6, 11, 7),
        "ac|b|d":  (9, 13, 8),
        "ad|b|c":  (11, 11, 9),
        "a|bd|c":  (13, 17, 14),
        "a|bc|d":  (15, 18, 11),
        "a|b|c|d": (32, 32, 32),
    }
    NOTE_DIMKER = {"w1": [1, 1, 1, 1, 1, 1], "w2": [1, 1, 1, 1, 2],
                   "w3": [1, 1, 1, 1, 1, 1]}

    bad2 = 0
    for wi, label in enumerate(("w1", "w2", "w3")):
        weights = []
        for mv in moves:
            nm = ordered_name(mv)
            weights.append(Fraction(W[nm][wi], 32) if nm in W else Fraction(0))
        assert sum(weights) == 1, sum(weights)
        spec = predicted_spectrum(rel, n, moves, weights)
        M = transition_matrix(moves, weights, words)
        print("  sec 5b under %s (the note's own published column):" % label)
        groups = {}
        for (X, lam, m) in spec:
            if m:
                exp = NOTE_5B.get(fmt(X))
                e_lam = Fraction(exp[wi], 32) if exp else None
                ok = "OK" if e_lam == lam else "*** MISMATCH ***"
                if e_lam != lam:
                    bad2 += 1
                print("     %-10s lambda = %-8s note says %-8s  %s"
                      % (fmt(X), lam, e_lam, ok))
            groups[lam] = groups.get(lam, 0) + m
        dims = []
        for lam in sorted(groups, reverse=True):
            if groups[lam] == 0:
                continue
            d = nullity(M, lam)
            dims.append(d)
            if d != groups[lam]:
                bad2 += 1
                print("     *** dim ker(M - %s I) = %d, predicted %d ***"
                      % (lam, d, groups[lam]))
        got = sorted(dims, reverse=True)
        exp = sorted(NOTE_DIMKER[label], reverse=True)
        ok = "OK" if got == exp else "*** MISMATCH ***"
        if got != exp:
            bad2 += 1
        print("     dim ker multiset %s, note says %s  %s ; sum %d of %d %s"
              % (got, exp, ok, sum(dims), len(words),
                 "(M is diagonalisable)" if sum(dims) == len(words) else "*** NOT ***"))
        print()
    return bad + bad2


def main():
    print("=" * 78)
    print("mg-d673 AUDIT INSTRUMENT 2 -- THE CLOSED FORM AGAINST THE ACTUAL")
    print("MATRIX SPECTRUM, IN EXACT RATIONAL ARITHMETIC.")
    print("The counting identity is not used anywhere in this file.")
    print("=" * 78)
    print()
    print("-" * 78)
    print("2.1  THE WORKED EXAMPLE P = {a<b, c<d}, against the note's OWN")
    print("     published sec 5a and sec 5b tables")
    print("-" * 78)
    bad = worked_example()

    print("-" * 78)
    print("2.2  EXHAUSTIVE SWEEP: closed form vs dim ker(M - lambda I), generic")
    print("     weights, exact rationals")
    print("-" * 78)
    emax = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    print("     (posets with |L(P)| <= %d; the exact nullity is O(e^3) per"
          " eigenvalue)" % emax)
    print()
    print("%3s %8s %8s %10s %10s %10s %10s"
          % ("n", "classes", "checked", "skipped", "sum m = e", "dims match",
             "diagonalisable"))
    for n in range(1, 6):
        classes = iso_classes(n)
        checked = skipped = 0
        b_sum = b_dim = b_diag = 0
        for rel in classes:
            e = len(linear_extensions(rel, n))
            if e > emax:
                skipped += 1
                continue
            ok_sum, ok_dims, ok_diag, tot, ee, detail, nm, nl = check_poset(rel, n)
            checked += 1
            b_sum += not ok_sum
            b_dim += not ok_dims
            b_diag += not ok_diag
            if not (ok_sum and ok_dims and ok_diag):
                bad += 1
                print("   *** FAIL n=%d rel=%s sum=%d e=%d" % (n, sorted(rel), tot, ee))
        print("%3d %8d %8d %10d %10s %10s %10s"
              % (n, len(classes), checked, skipped,
                 "%d bad" % b_sum, "%d bad" % b_dim, "%d bad" % b_diag))
    print()
    print("=" * 78)
    print("INSTRUMENT 2 TOTAL DISAGREEMENTS: %d" % bad)
    print("=" * 78)


if __name__ == "__main__":
    main()
