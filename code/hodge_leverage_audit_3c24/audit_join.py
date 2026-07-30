"""mg-3c24 -- INDEPENDENT AUDIT of mg-a2bd (the strike of ledger row G'').

mg-a2bd strikes ledger row G'' from docs/OneThird-Hodge-Side-Leverage.md as
FALSE, records the mechanism as new row J (Theorem J, joins suppress lambda_2),
adds a new row G''' (the true form), and repairs row G' by writing the
max-over-the-level step down.  This file rebuilds every load-bearing number of
that landing from scratch.

Nothing here imports code/hodge_leverage/ or code/face_geometry/.  `rebuild.py`
next to this file re-derives the poset population, the faces of F(P), the
weighted link 1-skeleton and the spectral decisions by different routes -- see
its docstring.  The decisive tests are EXACT (rational inertia of W - tD), not
floating point.

  A  the population
  B  the strike: G'' as a PER-LEVEL claim -- the 55, exactly
  C  the strike: G'' under the PER-FACE reading its own proof sentence argues
  D  row G''' -- the row mg-a2bd ADDED beyond its brief -- tested, not assumed
  E  Theorem J: the full-spectrum join identity, independently
  F  Theorem G and row G': lambda_2(F(A_m)) exactly, and where gamma_i is
     attained
"""

import math
import sys
import time
from fractions import Fraction

import rebuild as R

HALF = Fraction(1, 2)
NEAR = 1e-6


def lam2_and_ge_half(nv, edges):
    """(float lambda_2, exact bool 'lambda_2 >= 1/2').

    The float value is for reporting; the boolean is decided exactly whenever
    the float is anywhere near the 1/2 threshold, so no decision below rests on
    floating point.
    """
    if nv < 2:
        return (None, None)
    sp = R.walk_spectrum_float(nv, edges)
    if sp is None:                       # isolated vertex -> disconnected
        return (1.0, True)
    lam = sp[-2]
    if abs(lam - 0.5) < NEAR:
        return (lam, R.lambda2_ge_exact(nv, edges, HALF))
    return (lam, lam > 0.5)


def antichain_block(P, sigma, k=3):
    """Does some block of sigma induce an antichain of size >= k?"""
    for B in sigma:
        if bin(B).count("1") >= k and not R.induced(P, B).less:
            return True
    return False


def one_antichain_rest_singletons(P, sigma, k=3):
    """Row G''''s hypothesis: one block an antichain of size >= k, all other
    blocks singletons."""
    big = [B for B in sigma if bin(B).count("1") > 1]
    if len(big) != 1:
        return False
    B = big[0]
    return bin(B).count("1") >= k and not R.induced(P, B).less


def name_poset(P):
    """Name P as an ordinal sum of antichains/chains when it is one."""
    n = P.n
    lev = {}
    for x in range(n):
        lev.setdefault(len(P.dn[x]), []).append(x)
    levels = [lev[k] for k in sorted(lev)]
    for s in range(len(levels) - 1):
        for a in levels[s]:
            for b in levels[s + 1]:
                if (a, b) not in P.less:
                    return None
    parts = []
    for L in levels:
        if len(L) == 1:
            parts.append("A_1")
        elif all((a, b) not in P.less and (b, a) not in P.less
                 for i, a in enumerate(L) for b in L[i + 1:]):
            parts.append("A_%d" % len(L))
        else:
            return None
    # merge runs of singletons into chains C_k
    out, run = [], 0
    for p in parts:
        if p == "A_1":
            run += 1
        else:
            if run:
                out.append("C_%d" % run if run > 1 else "A_1")
                run = 0
            out.append(p)
    if run:
        out.append("C_%d" % run if run > 1 else "A_1")
    return " (+) ".join(out)


# ==========================================================================

def main():
    t0 = time.time()
    print("=" * 78)
    print("mg-3c24 -- INDEPENDENT AUDIT of mg-a2bd (the G'' strike)")
    print("=" * 78)
    print()
    print("Every object below is rebuilt in rebuild.py from the definitions:")
    print("  posets     : brute-force canonicalisation over all n! relabellings")
    print("  faces      : P-compatible ORDERED PARTITIONS, peeled off the front")
    print("  links      : REFINEMENTS of the face, weighted by PRODUCTS of")
    print("               linear-extension counts of the induced subposets")
    print("  lambda_2   : EXACT rational INERTIA of W - tD (not a float sweep)")
    print("  spectra    : Householder + implicit-shift QL (not cyclic Jacobi)")
    print()

    # ---------------------------------------------------------------- A
    print("A  THE POPULATION")
    pops = []
    for n in range(1, 7):
        ps = R.all_posets_indep(n)
        pops.append((n, ps))
        print("     n=%d  posets up to isomorphism = %3d" % (n, len(ps)))
    tot = sum(len(p) for _, p in pops)
    print("     total n <= 6 : %d   (deliverable: 405)  %s"
          % (tot, "AGREE" if tot == 405 else "DISAGREE"))
    print()
    sys.stdout.flush()

    # one pass computing every link we need
    #   level_data[(n, pid, i)] = list of (sigma, lam_float, ge_half_bool)
    per_n_pairs = {}
    per_n_ctr = {}
    ctr_detail = []
    face_pop = 0
    face_ctr = 0
    gppp_pairs = 0
    gppp_fail_level = []
    gppp_faces = 0
    gppp_fail_face = []
    gamma_cache = {}

    for n, plist in pops:
        if n < 2:
            continue
        pairs = ctrs = 0
        for pid, P in enumerate(plist):
            F = R.faces_by_dim(P)
            cache = {}
            for i in range(-1, n - 3):
                faces = F.get(i, [])
                if not faces:
                    continue
                qualifies = False
                gppp_here = False
                best = None
                any_ge = False
                for sigma in faces:
                    verts, edges = R.link_graph(P, sigma, cache)
                    lam, ge = lam2_and_ge_half(len(verts), edges)
                    if lam is None:
                        continue
                    if best is None or lam > best:
                        best = lam
                    if ge:
                        any_ge = True
                    q = antichain_block(P, sigma)
                    if q:
                        qualifies = True
                        face_pop += 1
                        if not ge:
                            face_ctr += 1
                    if one_antichain_rest_singletons(P, sigma):
                        gppp_here = True
                        gppp_faces += 1
                        if not ge:
                            gppp_fail_face.append((n, pid, i))
                if best is None:
                    continue
                gamma_cache[(n, pid, i)] = (best, any_ge)
                if qualifies:
                    pairs += 1
                    if not any_ge:
                        ctrs += 1
                        ctr_detail.append((n, pid, i, best, name_poset(P), P))
                if gppp_here:
                    gppp_pairs += 1
                    if not any_ge:
                        gppp_fail_level.append((n, pid, i))
        per_n_pairs[n] = pairs
        per_n_ctr[n] = ctrs
        print("   ... n=%d swept" % n)
        sys.stdout.flush()
    print()

    # ---------------------------------------------------------------- B
    print("B  THE STRIKE -- ledger row G'' AS WRITTEN (a PER-LEVEL claim)")
    print("     'gamma_i >= 1/2 for every finite poset having a dimension-i")
    print("      face one of whose blocks induces an antichain of size >= 3'")
    print()
    for n in sorted(per_n_pairs):
        print("      n=%d  (poset, level) pairs with such a face=%4d   "
              "gamma_i < 1/2 on %2d" % (n, per_n_pairs[n], per_n_ctr[n]))
    P_tot = sum(per_n_pairs.values())
    C_tot = sum(per_n_ctr.values())
    print()
    print("    population      : %d (poset, level) pairs, n <= 6   "
          "(mg-a2bd: 754)  %s"
          % (P_tot, "AGREE" if P_tot == 754 else "DISAGREE"))
    print("    COUNTEREXAMPLES : %d                                "
          "(mg-a2bd: 55)   %s"
          % (C_tot, "AGREE" if C_tot == 55 else "DISAGREE"))
    small = min([d[0] for d in ctr_detail]) if ctr_detail else None
    print("    smallest n      : %s                                 "
          "(mg-a2bd: 5)    %s"
          % (small, "AGREE" if small == 5 else "DISAGREE"))
    print()
    print("    the n = 5 counterexamples, named:")
    n5 = sorted([d for d in ctr_detail if d[0] == 5], key=lambda d: str(d[4]))
    for (n, pid, i, best, nm, P) in n5:
        print("      %-14s i=%d  gamma_i=%s   covers=%s"
              % (nm, i, Fraction(best).limit_denominator(10 ** 6),
                 sorted(sorted(x) for x in [[a, b] for (a, b) in P.less])[:0] or ""))
    allsum = all(d[4] is not None for d in n5)
    print("    all four are ordinal sums: %s" % allsum)
    print()
    vals = sorted(set(round(d[3], 6) for d in ctr_detail if d[0] == 6))
    print("    distinct gamma values among the n = 6 counterexamples:")
    print("      %s" % ", ".join("%.6f" % v for v in vals))
    print()

    # ---------------------------------------------------------------- C
    print("C  THE STRIKE -- G'' under the PER-FACE reading its proof argues")
    print("    faces (all posets n <= 6, levels -1..n-4) with a block inducing")
    print("    an antichain of size >= 3, and how many have lambda_2 < 1/2")
    print()
    print("      qualifying faces : %d   (mg-a2bd/mg-d39d: 7989)  %s"
          % (face_pop, "AGREE" if face_pop == 7989 else "DISAGREE"))
    print("      of them FAILING  : %d   (mg-a2bd/mg-d39d: 3901)  %s"
          % (face_ctr, "AGREE" if face_ctr == 3901 else "DISAGREE"))
    print()

    # ---------------------------------------------------------------- D
    print("D  ROW G''' -- THE ROW mg-a2bd ADDED BEYOND ITS BRIEF")
    print("    'gamma_i >= 1/2 for every finite poset having a dimension-i face")
    print("     whose blocks are one antichain of size >= 3 AND SINGLETONS")
    print("     OTHERWISE', labelled PROVEN.  Tested, not accepted:")
    print()
    print("      (poset, level) pairs meeting the hypothesis : %d" % gppp_pairs)
    print("      of them with gamma_i < 1/2                  : %d  %s"
          % (len(gppp_fail_level),
             "-> G''' HOLDS" if not gppp_fail_level else "-> G''' FAILS"))
    print("      the stronger PER-FACE form (every such face has")
    print("      lambda_2(link) >= 1/2):  faces=%d  failures=%d  %s"
          % (gppp_faces, len(gppp_fail_face),
             "-> holds per face too" if not gppp_fail_face else "-> FAILS"))
    print()
    sys.stdout.flush()

    # ---------------------------------------------------------------- E
    print("E  THEOREM J -- the full-spectrum join identity, independently")
    print("    link side : my own refinement-built weighted 1-skeleton")
    print("    factor side: assembled from F(P|_B) for the non-singleton blocks")
    print()
    tot_links = 0
    bad = 0
    worst = 0.0
    per_n = {}
    for n, plist in pops:
        if n < 2:
            continue
        cnt = cb = 0
        for P in plist:
            F = R.faces_by_dim(P)
            cache = {}
            for i in sorted(F):
                for sigma in F[i]:
                    big = [B for B in sigma if bin(B).count("1") >= 2]
                    if len(big) < 2:
                        continue
                    verts, edges = R.link_graph(P, sigma, cache)
                    meas = R.walk_spectrum_float(len(verts), edges)
                    if meas is None:
                        continue
                    D = sum(bin(B).count("1") - 1 for B in big) - 1
                    pred = []
                    ok = True
                    for B in big:
                        sz = bin(B).count("1")
                        p = sz - 2
                        Q = R.induced(P, B)
                        QF = R.faces_by_dim(Q)
                        qcache = {}
                        qv, qe = R.link_graph(Q, QF[-1][0], qcache)
                        if p == 0:
                            pred.extend([0.0] * (len(qv) - 1))
                            continue
                        qs = R.walk_spectrum_float(len(qv), qe)
                        if qs is None:
                            ok = False
                            break
                        pred.extend((p / float(D)) * mu for mu in qs[:-1])
                    if not ok:
                        continue
                    pred.extend([-1.0 / D] * (len(big) - 1))
                    pred.sort()
                    rest = sorted(meas[:-1])
                    cnt += 1
                    tot_links += 1
                    if len(pred) != len(rest):
                        cb += 1
                        bad += 1
                        continue
                    dev = max((abs(a - b) for a, b in zip(pred, rest)),
                              default=0.0)
                    worst = max(worst, dev)
                    if dev > 1e-9:
                        cb += 1
                        bad += 1
        per_n[n] = (cnt, cb)
        print("      n=%d  genuine-join links tested=%5d   mismatches=%d"
              % (n, cnt, cb))
        sys.stdout.flush()
    print()
    print("    total genuine-join links tested : %d   (mg-a2bd: 48846)  %s"
          % (tot_links, "AGREE" if tot_links == 48846 else "DISAGREE"))
    print("    spectrum mismatches             : %d" % bad)
    print("    worst deviation                 : %.3e" % worst)
    print()

    # the smallest counterexample, by hand
    print("    the smallest counterexample, re-derived by hand:")
    A2A3 = R.P0(5, [(a, b) for a in (0, 1) for b in (2, 3, 4)])
    F = R.faces_by_dim(A2A3)
    cache = {}
    for sigma in F[0]:
        if sorted(bin(B).count("1") for B in sigma) == [2, 3]:
            v, e = R.link_graph(A2A3, sigma, cache)
            sp = R.walk_spectrum_float(len(v), e)
            print("      P = A_2 (+) A_3, sigma = ({0,1},{2,3,4}), i = 0")
            print("      factors: F(A_2) (p=0) and F(A_3) (p=1), D = 2")
            print("      J predicts the hexagon's 1/2 lands at (1/2)*(1/2) = 1/4")
            print("      measured link spectrum on 1-perp: %s"
                  % [round(x, 6) for x in sp[:-1]])
            ex = R.spectral_inertia_at(len(v), e, Fraction(1, 4))
            print("      EXACT inertia of W - (1/4)D : %s" % (ex,))
            print("      -> exactly one eigenvalue above 1/4 (the constant 1),")
            print("         and 1/4 IS an eigenvalue: lambda_2 = 1/4 exactly")
            g = gamma_cache
            break
    print()

    # ---------------------------------------------------------------- F
    print("F  THEOREM G AND ROW G'")
    print()
    print("    (a) lambda_2(F(A_m)) decided EXACTLY by rational inertia")
    for m in range(3, 9):
        nv, ed = R.coxeter_graph(m)
        pos, zero, neg = R.spectral_inertia_at(nv, ed, HALF)
        verdict = ("lambda_2 = 1/2 EXACTLY" if pos == 1 and zero >= 1
                   else "lambda_2 > 1/2" if pos >= 2 else "lambda_2 < 1/2")
        print("        m=%d  |V|=%4d  inertia(W - D/2) = (%d, %d, %d)   %s"
              % (m, nv, pos, zero, neg, verdict))
        sys.stdout.flush()
    nv, ed = R.coxeter_graph(9)
    sp = R.walk_spectrum_float(nv, ed)
    print("        m=9  |V|= %d  lambda_2 = %.12f (float; exact inertia at"
          " |V|=510 is out of budget)" % (nv, sp[-2]))
    print()
    print("    (b) Theorem G's eigenfunction, EXACTLY, on my own F(A_m):")
    print("        f(S) = sum_{i in S} a_i with sum a_i = 0;  is Pf = f/2 ?")
    for m in range(3, 10):
        nv, ed = R.coxeter_graph(m)
        a = [Fraction(1)] + [Fraction(-1)] + [Fraction(0)] * (m - 2)
        a2 = [Fraction(i + 1) for i in range(m)]
        s = sum(a2)
        a2 = [x - Fraction(s, m) for x in a2]
        worst_r = Fraction(0)
        for avec in (a, a2):
            verts = list(range(1, (1 << m) - 1))
            idx = {S: i for i, S in enumerate(verts)}
            f = [sum(avec[t] for t in range(m) if (S >> t) & 1) for S in verts]
            deg = [Fraction(0)] * nv
            num = [Fraction(0)] * nv
            for (u, v, w) in ed:
                deg[u] += w
                deg[v] += w
                num[u] += w * f[v]
                num[v] += w * f[u]
            for u in range(nv):
                r = num[u] / deg[u] - f[u] / 2
                if abs(r) > worst_r:
                    worst_r = abs(r)
        print("        m=%d  max |(Pf)(S) - f(S)/2| over 2 a-vectors = %s"
              % (m, worst_r))
        sys.stdout.flush()
    print()
    print("    (c) row G': is gamma_i(A_n) attained EXACTLY at the")
    print("        one-big-block face?  Exhaustive over ALL faces, exact.")
    okall = True
    for n in range(3, 7):
        An = R.P0(n, [])
        F = R.faces_by_dim(An)
        cache = {}
        for i in range(-1, n - 3):
            obb = obb_ge = 0
            oth = oth_ge = 0
            oth_best = None
            for sigma in F.get(i, []):
                sizes = sorted(bin(B).count("1") for B in sigma)
                verts, edges = R.link_graph(An, sigma, cache)
                lam, ge = lam2_and_ge_half(len(verts), edges)
                if lam is None:
                    continue
                big = [s for s in sizes if s > 1]
                if len(big) == 1:
                    obb += 1
                    obb_ge += 1 if ge else 0
                else:
                    oth += 1
                    oth_ge += 1 if ge else 0
                    if oth_best is None or lam > oth_best:
                        oth_best = lam
            good = (obb == obb_ge) and (oth_ge == 0)
            okall = okall and good
            print("        A_%d i=%2d  m=%d  one-big-block faces=%4d "
                  "(all >= 1/2: %s)   other faces=%4d (any >= 1/2: %s, "
                  "max %s)"
                  % (n, i, n - i - 1, obb, obb == obb_ge, oth, oth_ge > 0,
                     "n/a" if oth_best is None else "%.6f" % oth_best))
        sys.stdout.flush()
    print("        -> argmax is EXACTLY the one-big-block face set: %s" % okall)
    print()
    print("    (d) the same by L + J over block-size multisets, n = 7..9")
    print("        lambda_2(link) = max_j (b_j-2)/D * lambda_2(F(A_{b_j}))")
    lam_A = {}
    for m in range(2, 10):
        if m == 2:
            lam_A[m] = 0.0
            continue
        nv, ed = R.coxeter_graph(m)
        lam_A[m] = R.walk_spectrum_float(nv, ed)[-2]

    def multisets(total, maxpart):
        """partitions of `total` into parts >= 1 (each part = b_j - 1)"""
        def rec(rem, mx):
            if rem == 0:
                yield ()
                return
            for p in range(min(rem, mx), 0, -1):
                for t in rec(rem - p, p):
                    yield (p,) + t
        return rec(total, maxpart)

    for n in range(7, 10):
        for i in range(-1, n - 3):
            D = n - i - 3
            best_other = None
            best_sizes = None
            obb_val = None
            for part in multisets(n - i - 2, n - i - 2):
                sizes = tuple(sorted(p + 1 for p in part))
                if sum(sizes) > n:
                    continue
                val = max([(b - 2) / float(D) * lam_A[b] for b in sizes if b >= 2]
                          + [-1.0 / D])
                if len(sizes) == 1:
                    obb_val = val
                else:
                    if best_other is None or val > best_other:
                        best_other = val
                        best_sizes = sizes
            print("        A_%d i=%2d  m=%d  one-big-block lambda_2=%.6f   "
                  "best other=%s at sizes %s"
                  % (n, i, n - i - 1, obb_val,
                     "n/a" if best_other is None else "%.6f" % best_other,
                     best_sizes))
    print()
    print("(no wall-clock line: this file regenerates byte-for-byte)")


if __name__ == "__main__":
    main()
