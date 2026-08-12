"""a1 -- are the note's claims TRUE?  Exact rational arithmetic, no float anywhere.

The novelty question this ticket asks cannot be answered without knowing what is being
compared, so the note's four structural claims are re-derived here from their own
definitions before any comparison is drawn.  Every arm is scored, including three that
are designed to go RED and must.

  A1  section 1: C_o^{-1}(F) is EXACTLY a cube Q^{d(F)}, edges tau_1, tau_3, ...
                 and C_e^{-1}(F) likewise with tau_2, tau_4, ...
  A2  section 2: Var(f | C_o) = (1/4) sum_{j free} c_{B_j}^2 -- no covariance terms.
  A3  section 3, identity (*): E_BK(f) = (2/(n-1)) (E Var(f|C_o) + E Var(f|C_e)).
  A4  section 4, identity (***): (I - P_BK) f = (2/(n-1)) (2I - Pi_o - Pi_e) f.
  A5  CONTROL, MUST GO RED: A3 and A4 on a function that is NOT a pair-orientation
      linear statistic.  If they held there too, the note's degree-one hypothesis
      would be carrying nothing and the identity would be a triviality about the
      chain rather than about linear statistics.
  A6  CONTROL, MUST GO RED: is the space of pair-orientation statistics invariant
      under P_BK?  If it were, (**) would bound the gap from below by itself.  It is
      not, and that is exactly why the note has to assume something in section 5.
  A7  NAMED CONTROL: V_k, the family this tree already knows has AT graph = Q_k
      (docs/OneThird-Hodge-Side-Leverage.md:132).  C_o must collapse to ONE fiber and
      C_e to singletons.
"""

import sys
from fractions import Fraction
from itertools import combinations

from lib623a import (C_even, C_odd, all_posets, bk_apply, bk_energy,
                     bk_neighbours, conditional_expectation, fibers,
                     free_blocks, incomparable_pairs, linear_extensions,
                     mean_conditional_variance, pair_orientation, v_family,
                     variance)


# A deterministic, reproducible coefficient generator.  No Date/random seeding from
# the clock: the same run gives the same coefficients forever.
def coeffs_for(ip, salt):
    """Assign each incomparable pair a distinct nonzero rational coefficient.
    Distinct values matter: equal coefficients could hide a sign or an index error."""
    out = {}
    for k, p in enumerate(ip):
        num = ((k * 7 + salt * 13) % 11) - 5
        if num == 0:
            num = 3
        out[p] = Fraction(num, (k % 4) + 1)
    return out


def check_poset(rel, n, salts=(0, 1, 2)):
    """Returns a dict of per-arm (checked, failed) counts for one poset."""
    les = linear_extensions(rel, n)
    ip = incomparable_pairs(rel, n)
    res = {k: [0, 0] for k in ("A1", "A2", "A3", "A4", "A5a", "A5b", "A6")}
    if n < 2 or not les:
        return res, les, ip

    # ---- A1: fibers are exactly cubes, with the stated edges.
    for C, parity, want_odd in ((C_odd, 'odd', True), (C_even, 'even', False)):
        for _key, members in fibers(les, C).items():
            res["A1"][0] += 1
            L0 = members[0]
            fb = free_blocks(L0, rel, parity)
            ok = (len(members) == 2 ** len(fb))
            # every member must have the SAME free-block set (same positions, same
            # element pairs as unordered sets) -- otherwise "the blocks are fixed"
            # is false and the cube identification is an accident of counting.
            blocks0 = sorted((i, frozenset((x, y))) for (i, x, y) in fb)
            for L in members:
                b = sorted((i, frozenset((x, y)))
                           for (i, x, y) in free_blocks(L, rel, parity))
                if b != blocks0:
                    ok = False
            # the edges inside the fiber are exactly the tau_i of the right parity
            for L in members:
                for (i, M) in bk_neighbours(L, rel):
                    inside = (C(M) == C(L))
                    right_parity = (i % 2 == 1) if want_odd else (i % 2 == 0)
                    if inside != right_parity:
                        ok = False
            if not ok:
                res["A1"][1] += 1

    for salt in salts:
        c = coeffs_for(ip, salt)
        f = {L: pair_orientation(L, c) for L in les}

        # ---- A2: within-fiber variance is the diagonal sum, no covariance terms.
        for C, parity in ((C_odd, 'odd'), (C_even, 'even')):
            for _key, members in fibers(les, C).items():
                res["A2"][0] += 1
                fb = free_blocks(members[0], rel, parity)
                want = sum(c[tuple(sorted((x, y)))] ** 2
                           for (_i, x, y) in fb) / 4
                got = variance([f[L] for L in members])
                if want != got:
                    res["A2"][1] += 1

        # ---- A3: identity (*).
        res["A3"][0] += 1
        lhs = bk_energy(les, rel, f)
        rhs = (Fraction(2, n - 1) *
               (mean_conditional_variance(les, C_odd, f) +
                mean_conditional_variance(les, C_even, f)))
        if lhs != rhs:
            res["A3"][1] += 1

        # ---- A4: identity (***), pointwise.
        res["A4"][0] += 1
        Pf = bk_apply(les, rel, f)
        po = conditional_expectation(les, C_odd, f)
        pe = conditional_expectation(les, C_even, f)
        for L in les:
            l = f[L] - Pf[L]
            r = Fraction(2, n - 1) * (2 * f[L] - po[L] - pe[L])
            if l != r:
                res["A4"][1] += 1
                break

        # ---- A5: the same two identities on a NON-linear statistic.  These are
        # scored INVERTED: a "failure" here is the control working.
        g = {}
        for k, L in enumerate(sorted(les)):
            g[L] = Fraction(((k * k * 5 + salt * 3) % 17) - 8, (k % 3) + 1)
        res["A5a"][0] += 1
        lhs = bk_energy(les, rel, g)
        rhs = (Fraction(2, n - 1) *
               (mean_conditional_variance(les, C_odd, g) +
                mean_conditional_variance(les, C_even, g)))
        if lhs != rhs:
            res["A5a"][1] += 1
        res["A5b"][0] += 1
        Pg = bk_apply(les, rel, g)
        go = conditional_expectation(les, C_odd, g)
        ge = conditional_expectation(les, C_even, g)
        for L in les:
            if g[L] - Pg[L] != Fraction(2, n - 1) * (2 * g[L] - go[L] - ge[L]):
                res["A5b"][1] += 1
                break

        # ---- A6: is P_BK f again a pair-orientation statistic?  Decide by solving
        # for coefficients exactly: a pair-orientation statistic is determined on
        # L(P) by (a, {c_p}), so fit by exact linear algebra over the incomparable
        # pairs and check the fit is exact.
        res["A6"][0] += 1
        if not is_pair_orientation(Pf, les, ip):
            res["A6"][1] += 1

    return res, les, ip


def is_pair_orientation(h, les, ip):
    """Exact: is h in span{1} + span{1{x <_L y} : {x,y} in I(P)} as a function on L(P)?
    Gaussian elimination over Fraction on the design matrix."""
    cols = [None] + list(ip)
    rows = []
    for L in les:
        pos = {x: k for k, x in enumerate(L)}
        r = [Fraction(1)]
        for (x, y) in ip:
            r.append(Fraction(1) if pos[x] < pos[y] else Fraction(0))
        r.append(h[L])
        rows.append(r)
    ncol = len(cols)
    piv = 0
    for col in range(ncol):
        sel = None
        for r in range(piv, len(rows)):
            if rows[r][col] != 0:
                sel = r
                break
        if sel is None:
            continue
        rows[piv], rows[sel] = rows[sel], rows[piv]
        pv = rows[piv][col]
        rows[piv] = [v / pv for v in rows[piv]]
        for r in range(len(rows)):
            if r != piv and rows[r][col] != 0:
                fac = rows[r][col]
                rows[r] = [a - fac * b for a, b in zip(rows[r], rows[piv])]
        piv += 1
    # inconsistent iff some row is all-zero in the coefficient columns with a
    # nonzero right-hand side
    for r in rows:
        if all(v == 0 for v in r[:ncol]) and r[ncol] != 0:
            return False
    return True


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print("a1 -- the note's four structural claims, re-derived exactly")
    print("     source: docs/imports/compression.tex (44d08ea)")
    print("     ALL ARITHMETIC EXACT (Fraction).  No float on any line below.")
    print()
    print("  A1  fibers are cubes with the stated edges          [must be 0 failures]")
    print("  A2  Var(f|C) = (1/4) sum c^2, no covariances        [must be 0 failures]")
    print("  A3  identity (*)  E_BK = (2/(n-1))(EVar_o + EVar_e) [must be 0 failures]")
    print("  A4  identity (***) (I-P)f = (2/(n-1))(2I-Pi_o-Pi_e)f[must be 0 failures]")
    print("  A5a CONTROL (*)  on a NON-linear statistic          [MUST FAIL]")
    print("  A5b CONTROL (***) on a NON-linear statistic         [MUST FAIL]")
    print("  A6  CONTROL: is P_BK f again a pair-orientation f?  [MUST FAIL]")
    print()
    hdr = ("  n   posets    A1 f/c        A2 f/c        A3 f/c    "
           "A4 f/c    A5a f/c   A5b f/c   A6 f/c")
    print(hdr)
    print("  " + "-" * (len(hdr) - 2))
    grand = {k: [0, 0] for k in ("A1", "A2", "A3", "A4", "A5a", "A5b", "A6")}
    for n in range(2, nmax + 1):
        tot = {k: [0, 0] for k in grand}
        np_ = 0
        for rel in all_posets(n):
            np_ += 1
            res, _les, _ip = check_poset(rel, n)
            for k in tot:
                tot[k][0] += res[k][0]
                tot[k][1] += res[k][1]
        for k in grand:
            grand[k][0] += tot[k][0]
            grand[k][1] += tot[k][1]
        print("  %-3d %-8d  %-13s %-13s %-9s %-9s %-9s %-9s %-9s" % (
            n, np_,
            "%d/%d" % (tot["A1"][1], tot["A1"][0]),
            "%d/%d" % (tot["A2"][1], tot["A2"][0]),
            "%d/%d" % (tot["A3"][1], tot["A3"][0]),
            "%d/%d" % (tot["A4"][1], tot["A4"][0]),
            "%d/%d" % (tot["A5a"][1], tot["A5a"][0]),
            "%d/%d" % (tot["A5b"][1], tot["A5b"][0]),
            "%d/%d" % (tot["A6"][1], tot["A6"][0])))
    print()
    print("  POOLED, n = 2..%d, all labelled posets, 3 coefficient vectors each:" % nmax)
    for k in ("A1", "A2", "A3", "A4"):
        v = grand[k]
        print("    %-4s %6d checked, %6d FAILED   %s"
              % (k, v[0], v[1], "OK" if v[1] == 0 else "*** BROKEN ***"))
    for k in ("A5a", "A5b", "A6"):
        v = grand[k]
        print("    %-4s %6d checked, %6d failed   %s   [control: failure is the pass]"
              % (k, v[0], v[1],
                 "FIRES" if v[1] > 0 else "*** CONTROL DID NOT FIRE ***"))

    # ---------------------------------------------------------------- A7
    print()
    print("  A7 -- NAMED CONTROL on V_k, the family docs/OneThird-Hodge-Side-Leverage.md")
    print("        :132 records as having AT graph = the hypercube Q_k.  The note's odd")
    print("        compression must collapse V_k to ONE fiber (the whole space, a cube)")
    print("        and its even compression to singletons.")
    print()
    print("    k   n   |L(P)|   C_o fibers   max |fiber|   C_e fibers   max |fiber|   verdict")
    a7_ok = True
    for k in (1, 2, 3, 4):
        rel, n = v_family(k)
        les = linear_extensions(rel, n)
        fo = fibers(les, C_odd)
        fe = fibers(les, C_even)
        ok = (len(fo) == 1 and max(len(v) for v in fo.values()) == 2 ** k
              and len(fe) == len(les) and max(len(v) for v in fe.values()) == 1)
        a7_ok = a7_ok and ok
        print("    %-3d %-3d %-8d %-13d %-13d %-13d %-13d %s"
              % (k, n, len(les), len(fo), max(len(v) for v in fo.values()),
                 len(fe), max(len(v) for v in fe.values()),
                 "as predicted" if ok else "*** NOT AS PREDICTED ***"))
    print()
    print("    A7: %s" % ("OK -- on V_k the odd compression IS the whole cube, so the"
                          " note's foliation\n        degenerates to the single"
                          " already-known cube there and adds nothing on that family."
                          if a7_ok else "*** BROKEN ***"))


if __name__ == "__main__":
    main()
