"""a2 -- does (**) bound the BK gap, or only touch it?

The note's section 5 is explicit that its payoff rests on an assumption it does not
prove: "assuming your agents' claim that the relevant standard eigenfunction is linear
is correct".  a1 shows the identities are exact.  This arm measures what they buy
WITHOUT that assumption, and how much the assumption is actually asking for.

  gap_BK   = smallest nonzero eigenvalue of I - P_BK          [FLOAT]
  gap_lin  = min over CENTERED pair-orientation statistics of E_BK(f)/Var(f)   [FLOAT]

By the variational principle gap_lin >= gap_BK always, so (**) is unconditionally an
UPPER bound on the gap and is a lower bound only where the two coincide.

  B1  gap_lin >= gap_BK at every poset                        [must hold]
  B2  how often is gap_lin > gap_BK?  -- i.e. how often is the bottom eigenfunction
      NOT a pair-orientation statistic, so that (**) does not reach the gap
  B3  SELF-CHECK: the energy matrix built from the CHAIN and the energy matrix built
      from the note's conditional variances must agree.  This is a1's A3 again, on a
      different instrument and in float; if it disagreed, a2 would be measuring
      something other than the note.
"""

import math
import sys
from fractions import Fraction

from lib623a import (C_even, C_odd, all_posets, bk_neighbours, fibers,
                     incomparable_pairs, linear_extensions)

TOL = 1e-9


def jacobi(A):
    """Eigenvalues of a symmetric matrix by cyclic Jacobi.  Returns sorted list and
    the final off-diagonal norm, which is printed so the reader can see the residual
    rather than trust it."""
    n = len(A)
    A = [row[:] for row in A]
    for _sweep in range(60):
        off = math.sqrt(sum(A[i][j] ** 2 for i in range(n) for j in range(n) if i != j))
        if off < 1e-12:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(A[p][q]) < 1e-15:
                    continue
                theta = (A[q][q] - A[p][p]) / (2 * A[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(n):
                    akp, akq = A[k][p], A[k][q]
                    A[k][p] = c * akp - s * akq
                    A[k][q] = s * akp + c * akq
                for k in range(n):
                    apk, aqk = A[p][k], A[q][k]
                    A[p][k] = c * apk - s * aqk
                    A[q][k] = s * apk + c * aqk
    off = math.sqrt(sum(A[i][j] ** 2 for i in range(n) for j in range(n) if i != j))
    return sorted(A[i][i] for i in range(n)), off


def gap_bk(les, rel):
    """Smallest nonzero eigenvalue of I - P_BK, plus the Jacobi residual."""
    m = len(les)
    n = len(les[0])
    idx = {L: k for k, L in enumerate(les)}
    A = [[0.0] * m for _ in range(m)]
    for L in les:
        i = idx[L]
        nb = bk_neighbours(L, rel)
        A[i][i] = len(nb) / (n - 1)
        for (_p, M) in nb:
            A[i][idx[M]] -= 1.0 / (n - 1)
    ev, off = jacobi(A)
    # the constant vector is an exact 0 eigenvector; drop the smallest one
    return (ev[1] if len(ev) > 1 else 0.0), off


def centered_basis(les, ip):
    """Orthonormal basis (uniform inner product) of the centered pair-orientation
    statistics, as a list of vectors over les.  Gram-Schmidt with a rank drop."""
    m = len(les)
    cols = []
    for (x, y) in ip:
        v = []
        for L in les:
            pos = {a: k for k, a in enumerate(L)}
            v.append(1.0 if pos[x] < pos[y] else 0.0)
        mu = sum(v) / m
        cols.append([a - mu for a in v])
    onb = []
    for v in cols:
        w = v[:]
        for u in onb:
            d = sum(w[i] * u[i] for i in range(m)) / m
            w = [w[i] - d * u[i] for i in range(m)]
        nr = math.sqrt(sum(a * a for a in w) / m)
        if nr > 1e-9:
            onb.append([a / nr for a in w])
    return onb


def energy_matrix_chain(les, rel, onb):
    """M_ab = E_BK(u_a, u_b) from the chain itself."""
    n = len(les[0])
    m = len(les)
    idx = {L: k for k, L in enumerate(les)}
    d = len(onb)
    M = [[0.0] * d for _ in range(d)]
    for L in les:
        i = idx[L]
        for (_p, N) in bk_neighbours(L, rel):
            j = idx[N]
            for a in range(d):
                da = onb[a][j] - onb[a][i]
                for b in range(d):
                    M[a][b] += da * (onb[b][j] - onb[b][i])
    sc = 1.0 / (2 * m * (n - 1))
    return [[M[a][b] * sc for b in range(d)] for a in range(d)]


def energy_matrix_note(les, onb):
    """M_ab from the note's (*): (2/(n-1)) (E Cov(.|C_o) + E Cov(.|C_e))."""
    n = len(les[0])
    m = len(les)
    idx = {L: k for k, L in enumerate(les)}
    d = len(onb)
    M = [[0.0] * d for _ in range(d)]
    for C in (C_odd, C_even):
        for _key, members in fibers(les, C).items():
            ks = [idx[L] for L in members]
            mus = [sum(onb[a][k] for k in ks) / len(ks) for a in range(d)]
            for a in range(d):
                for b in range(d):
                    M[a][b] += sum((onb[a][k] - mus[a]) * (onb[b][k] - mus[b])
                                   for k in ks)
    sc = 2.0 / ((n - 1) * m)
    return [[M[a][b] * sc for b in range(d)] for a in range(d)]


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    cap = int(sys.argv[2]) if len(sys.argv) > 2 else 24
    print("a2 -- what (**) buys WITHOUT the note's section-5 assumption")
    print("     gap_lin >= gap_BK always.  Where it is STRICT, the BK bottom")
    print("     eigenfunction is not a pair-orientation statistic and (**) is an")
    print("     UPPER bound on the gap only.")
    print()
    print("     [FLOAT] -- gap_BK and gap_lin are eigenvalues, computed by cyclic")
    print("     Jacobi; the worst off-diagonal residual over the whole run is printed.")
    print("     POPULATION CAP: posets with |L(P)| > %d are SKIPPED and counted."
          % cap)
    print()
    print("  n   posets  in-pop  skipped(|L|>%d)  B2: gap_lin > gap_BK   B1 viol   worst ratio    argmax" % cap)
    worst_off = 0.0
    b3_worst = 0.0
    for n in range(3, nmax + 1):
        npos = inpop = skipped = strict = viol = 0
        wr = 1.0
        wr_at = None
        for rel in all_posets(n):
            npos += 1
            les = linear_extensions(rel, n)
            if len(les) > cap:
                skipped += 1
                continue
            ip = incomparable_pairs(rel, n)
            if len(les) < 2 or not ip:
                continue
            inpop += 1
            g, off = gap_bk(les, rel)
            worst_off = max(worst_off, off)
            onb = centered_basis(les, ip)
            if not onb:
                continue
            Mc = energy_matrix_chain(les, rel, onb)
            Mn = energy_matrix_note(les, onb)
            b3_worst = max(b3_worst,
                           max(abs(Mc[a][b] - Mn[a][b])
                               for a in range(len(onb)) for b in range(len(onb))))
            ev, off2 = jacobi(Mc)
            worst_off = max(worst_off, off2)
            gl = ev[0]
            if gl < g - 1e-7:
                viol += 1
            if gl > g + 1e-7:
                strict += 1
                if g > TOL and gl / g > wr:
                    wr = gl / g
                    wr_at = sorted(rel)
        print("  %-3d %-7d %-7d %-16d %-22s %-9d %-14.6f %s"
              % (n, npos, inpop, skipped, "%d of %d" % (strict, inpop), viol, wr,
                 wr_at if wr_at else "-"))
    print()
    print("  B1  gap_lin >= gap_BK violations: see column above (must be 0)")
    print("  B3  SELF-CHECK max |chain-energy - note-energy| over all posets, all")
    print("      basis pairs: %.3e   (a1's A3 on a second instrument, in float)"
          % b3_worst)
    print("      worst Jacobi off-diagonal residual: %.3e" % worst_off)


if __name__ == "__main__":
    main()
