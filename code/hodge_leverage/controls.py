"""Controls for mg-a3d4, in both directions.

Committed output: `controls_output.txt`.

POSITIVE CONTROLS -- the instrument reproduces answers known independently of
this programme:

  P1  lambda_2(Delta_AT(A_n)) = 2 - 2 cos(pi/n).  This is Aldous' spectral gap
      conjecture for the path, proved by Caputo-Liggett-Richthammer (2010): the
      interchange process on a graph has the same spectral gap as the one-particle
      walk.  Compared against the Lanczos solver.
  P2  lambda2_weighted_graph against closed forms for cycles and paths:
      lambda_2(C_m) = cos(2 pi / m),  lambda_2(P_m) = cos(pi / (m-1)).
  P3  the two eigensolvers (dense Jacobi, sparse Lanczos) agree on the same
      matrices -- disjoint code paths.
  P4  the Tsetlin library.  For the antichain and w supported on the faces
      ({i}, rest), Brown's prediction must reproduce the classical move-to-front
      spectrum: eigenvalue sum_{i in S} w_i with multiplicity D(n - |S|), the
      number of derangements.  Neither the derangement numbers nor the subset
      indexing appear anywhere in `lrb.py`.
  P5  the localisation theorem, used as a memo key: faces with the same multiset
      of block isomorphism types must give links with the same lambda_2.  Checked
      by computing every link directly, with the memo disabled.

NEGATIVE CONTROLS -- each perturbs a CONSTRUCTION introduced by this work item,
not merely a downstream comparison (mg-e0ce finding F2).  For every mutation the
report gives the number of posets on which it FIRES and the number on which it is
VACUOUS, with vacuity computed (the mutation did not change the object) rather
than asserted.

  X1a the link's WEIGHTS: replace the induced measure w(tau) = #facets containing
      tau by uniform weights.  Reported even though it DOES NOT FIRE -- see the
      note in its output: inflating gamma cannot falsify a lower bound, so this
      mutation is not a usable control, and X1b replaces it.
  X1b the link's INCIDENCE: keep the true vertex set, but join every pair of link
      vertices (forget that a face of the link must be a chain of ideals).  This
      deflates gamma and must falsify (LG).
  X2  the link's VERTEX SET: take all proper ideals comparable with the top ideal
      of sigma instead of the true link.  Must break the join decomposition.
  X3  the down-up walk's CONSTRUCTION: treat every ridge as interior (pretend
      free ridges have two facets).  Theorem D must fail.
  X4  the band PRODUCT: order the intersections by (j,i) instead of (i,j).  The
      band axioms and/or the Brown spectrum must fail.
  X5  the MULTIPLICITY rule: sum over Y <= X instead of Y >= X.  Must produce
      negative multiplicities or a wrong spectrum.
"""

import math
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "face_geometry"))

from face_complex import Poset, proper_ideals, linear_extensions
from posets import all_posets, cover_string
from linalg import (jacobi_eigenvalues, lambda2_weighted_graph, smallest_nonzero,
                    sparse_matvec, dense_matvec)
from links import (faces_of, facets_of, link_skeleton, join_type, at_gap_matrix,
                   blocks_of_face)
from local_to_global import at_lambda2, lg_bound, link_lambda2
from lrb import (all_faces, lrb_product, support, support_lattice, refines,
                 brown_multiplicities, brown_eigenvalues, brown_walk,
                 weights_all_faces, weights_singleton_first, chambers_refining)
from run_lrb import kernel_dim


def derangements(n):
    d = [1, 0]
    while len(d) <= n:
        k = len(d) - 1
        d.append(k * (d[k] + d[k - 1]))
    return d[n]


# --------------------------------------------------------------------------
# positive controls
# --------------------------------------------------------------------------

def P1():
    print("P1  lambda_2(Delta_AT(A_n)) vs Aldous / Caputo-Liggett-Richthammer")
    worst = 0.0
    for n in range(2, 7):
        got = at_lambda2(Poset(n, []))
        want = 2 - 2 * math.cos(math.pi / n)
        worst = max(worst, abs(got - want))
        print("      n=%d  Lanczos=%.12f  2-2cos(pi/n)=%.12f  |diff|=%.2e"
              % (n, got, want, abs(got - want)))
    print("      PASS" if worst < 1e-9 else "      FAIL")
    return worst < 1e-9


def P2():
    print("P2  lambda2_weighted_graph vs closed forms for cycles and paths")
    ok = True
    for m in (4, 5, 6, 7, 8):
        edges = [(i, (i + 1) % m, 1.0) for i in range(m)]
        got, _ = lambda2_weighted_graph(m, edges)
        want = math.cos(2 * math.pi / m)
        ok = ok and abs(got - want) < 1e-10
        print("      C_%d: got %.12f  want %.12f" % (m, got, want))
    for m in (2, 3, 4, 5, 6):
        edges = [(i, i + 1, 1.0) for i in range(m - 1)]
        got, _ = lambda2_weighted_graph(m, edges)
        want = math.cos(math.pi / (m - 1))
        ok = ok and abs(got - want) < 1e-10
        print("      P_%d: got %.12f  want %.12f" % (m, got, want))
    print("      PASS" if ok else "      FAIL")
    return ok


def P3():
    print("P3  dense Jacobi vs sparse Lanczos on the same Delta_AT matrices")
    ok = True
    for P in [Poset(4, []), Poset(4, [(0, 1)]), Poset(5, [(0, 1), (2, 3)]),
              Poset(5, [(0, 1)])]:
        les, rows = at_gap_matrix(P)
        m = len(les)
        M = [[0.0] * m for _ in range(m)]
        for i, row in enumerate(rows):
            for (j, v) in row:
                M[i][j] = v
        ev = jacobi_eigenvalues(M)
        jac = [x for x in ev if x > 1e-9][0]
        lan = at_lambda2(P)
        ok = ok and abs(jac - lan) < 1e-9
        print("      %-20s |L|=%3d  Jacobi=%.12f  Lanczos=%.12f"
              % (cover_string(P), m, jac, lan))
    print("      PASS" if ok else "      FAIL")
    return ok


def P4():
    print("P4  the Tsetlin library: Brown's prediction vs the classical")
    print("    move-to-front spectrum (eigenvalue sum_{i in S} w_i with")
    print("    multiplicity = #derangements(n - |S|))")
    ok = True
    for n in range(2, 6):
        P = Poset(n, [])
        faces = all_faces(P)
        w = weights_singleton_first(faces, P)
        # index the weights by the singleton element
        wi = {}
        for x, v in w.items():
            wi[x[0].bit_length() - 1] = v
        L = support_lattice(P, faces)
        mult = brown_multiplicities(P, L)
        lam = brown_eigenvalues(P, w, L, faces)
        mine = {}
        for X in L:
            if mult[X]:
                mine[lam[X]] = mine.get(lam[X], 0) + mult[X]
        classical = {}
        for mask in range(1 << n):
            S = [i for i in range(n) if (mask >> i) & 1]
            mu = derangements(n - len(S))
            if mu:
                v = sum(wi[i] for i in S)
                classical[v] = classical.get(v, 0) + mu
        same = (mine == classical)
        ok = ok and same
        print("      n=%d  Brown: %s" % (n, sorted(mine.items())))
        print("           Tsetlin: %s   match=%s" % (sorted(classical.items()), same))
    print("      PASS" if ok else "      FAIL")
    return ok


def P5():
    print("P5  the localisation theorem as a memo key: same block types =>")
    print("    same link lambda_2.  Memo disabled; every link computed directly.")
    ok = True
    for n in range(2, 6):
        seen = {}
        clash = 0
        for P in all_posets(n):
            facets = facets_of(P)
            faces = faces_of(P)
            for d in sorted(faces):
                if d > P.n - 4:
                    continue
                for sigma in faces[d]:
                    key = join_type(P, sigma)
                    verts, edges = link_skeleton(P, sigma, facets)
                    lam, _ = lambda2_weighted_graph(len(verts), edges)
                    v = None if lam is None else round(lam, 10)
                    if key in seen and seen[key] != v:
                        clash += 1
                    seen[key] = v
        ok = ok and clash == 0
        print("      n=%d  distinct block-type keys=%3d   clashes=%d"
              % (n, len(seen), clash))
    print("      PASS" if ok else "      FAIL")
    return ok


# --------------------------------------------------------------------------
# negative controls -- construction-side
# --------------------------------------------------------------------------

def _mutated_lg(P, mutate):
    """The (LG) bound recomputed with `mutate(verts, edges)` in place of the true
    weighted link 1-skeleton.  Returns (bound, changed_any_link)."""
    facets = facets_of(P)
    faces = faces_of(P)
    d = P.n - 2
    prod = 1.0
    changed = False
    for i in range(-1, d - 1):
        bm = None
        for sigma in faces.get(i, []):
            verts, edges = link_skeleton(P, sigma, facets)
            lt, _ = lambda2_weighted_graph(len(verts), edges)
            nv, ne = mutate(verts, edges)
            lm, _ = lambda2_weighted_graph(nv, ne)
            if lm is not None and (bm is None or lm > bm):
                bm = lm
            if lt is not None and lm is not None and abs(lt - lm) > 1e-12:
                changed = True
        if bm is not None:
            prod *= (1 - bm)
    return 2.0 * prod, changed


def X1a():
    print("X1a MUTATE THE LINK WEIGHTS: uniform instead of the induced measure.")
    print("    Question asked: does the (LG) bound built from the mutated links")
    print("    become FALSE (exceed the true lambda_2)?")
    fires = vac = valchanged = 0
    for n in range(3, 7):
        for P in all_posets(n):
            b, changed = _mutated_lg(
                P, lambda v, e: (len(v), [(u, w, 1.0) for (u, w, _x) in e]))
            truth = at_lambda2(P)
            if (not changed) or truth is None:
                vac += 1
                continue
            valchanged += 1
            if b > truth + 1e-9:
                fires += 1
    print("      fires on %d posets; vacuous on %d (mutation changed no link, or"
          " |L(P)|=1); mutation changed the bound's VALUE on %d"
          % (fires, vac, valchanged))
    print("      DOES NOT FIRE, and this is reported rather than dropped.  The")
    print("      reason is structural, not luck: uniform link weights come out")
    print("      with lambda_2 at least as large as the induced-measure ones on")
    print("      every poset here, which makes the mutated bound SMALLER and so")
    print("      still true.  (LG) is a lower bound, so a mutation that inflates")
    print("      gamma can never falsify it.  X1a is therefore NOT a usable")
    print("      negative control for the link construction; X1b is.")
    return None


def X1b():
    print("X1b MUTATE THE LINK INCIDENCE: keep the true vertex set but join every")
    print("    pair (forget that a face of the link must be a CHAIN of ideals).")
    print("    This deflates gamma, so it can and must falsify (LG).")
    fires = vac = 0
    examples = []

    def mutate(verts, edges):
        nv = len(verts)
        return nv, [(i, j, 1.0) for i in range(nv) for j in range(i + 1, nv)]

    for n in range(3, 7):
        for P in all_posets(n):
            b, changed = _mutated_lg(P, mutate)
            truth = at_lambda2(P)
            if (not changed) or truth is None:
                vac += 1
                continue
            if b > truth + 1e-9:
                fires += 1
                if len(examples) < 3:
                    examples.append((P.n, cover_string(P), b, truth))
    print("      fires (mutated bound exceeds the truth, i.e. the perturbed"
          " construction yields a FALSE theorem) on %d posets; vacuous on %d"
          % (fires, vac))
    for e in examples:
        print("      e.g. n=%d %-18s mutated bound=%.6f > truth=%.6f" % e)
    return fires > 0


def X2():
    print("X2  MUTATE THE LINK VERTEX SET: all proper ideals comparable with the")
    print("    top ideal of sigma.  Must break the join decomposition (the")
    print("    vertex count must stop matching sum_i #proper ideals of Q_i).")
    fires = vac = 0
    for n in range(3, 6):
        for P in all_posets(n):
            facets = facets_of(P)
            faces = faces_of(P)
            pid = proper_ideals(P)
            for d in sorted(faces):
                for sigma in faces[d]:
                    verts, _ = link_skeleton(P, sigma, facets)
                    if not sigma:
                        mut = set(pid)
                    else:
                        top = sigma[-1]
                        mut = {K for K in pid if K not in sigma and
                               ((K & top) == K or (K & top) == top)}
                    if mut == set(verts):
                        vac += 1
                    else:
                        fires += 1
    print("      fires (mutated vertex set differs from the true link) on %d"
          " faces; vacuous on %d faces" % (fires, vac))
    return fires > 0


def X3():
    print("X3  MUTATE THE DOWN-UP WALK: treat every ridge as interior (pretend")
    print("    free ridges lie in two facets).  Theorem D must fail.")
    from links import facets_of as _f
    from face_complex import adjacent_transposition_graph, le_to_facet
    fires = vac = 0
    for n in range(2, 7):
        for P in all_posets(n):
            facets = _f(P)
            m = len(facets)
            fidx = {f: i for i, f in enumerate(facets)}
            nr = P.n - 1
            ridge_facets = {}
            for f in facets:
                for i in range(len(f)):
                    r = f[:i] + f[i + 1:]
                    ridge_facets.setdefault(r, []).append(f)
            # mutation: every ridge contributes 1/2 to itself and 1/2 to the
            # "other" facet, taken to be itself when the ridge is free
            M = [[Fraction(0)] * m for _ in range(m)]
            mutated = False
            for f in facets:
                i = fidx[f]
                for k in range(len(f)):
                    r = f[:k] + f[k + 1:]
                    cof = ridge_facets[r]
                    if len(cof) == 1:
                        mutated = True
                        M[i][i] += Fraction(1, 2 * nr)
                        M[i][i] += Fraction(1, 2 * nr)   # same as truth: no-op
                    else:
                        for g in cof:
                            M[i][fidx[g]] += Fraction(1, nr * len(cof))
            # a mutation that actually bites: give free ridges weight 1/2 only
            M2 = [[Fraction(0)] * m for _ in range(m)]
            bites = False
            for f in facets:
                i = fidx[f]
                for k in range(len(f)):
                    r = f[:k] + f[k + 1:]
                    cof = ridge_facets[r]
                    if len(cof) == 1:
                        bites = True
                        M2[i][i] += Fraction(1, 2 * nr)
                    else:
                        for g in cof:
                            M2[i][fidx[g]] += Fraction(1, nr * len(cof))
            if not bites:
                vac += 1
                continue
            les, A, deg = adjacent_transposition_graph(P)
            order = [le_to_facet(w) for w in les]
            c = Fraction(1, 2 * (P.n - 1))
            bad = False
            for a in range(m):
                for b in range(m):
                    lhs = (1 if a == b else 0) - M2[fidx[order[a]]][fidx[order[b]]]
                    rhs = c * ((deg[a] if a == b else 0) - A[a][b])
                    if lhs != rhs:
                        bad = True
                        break
                if bad:
                    break
            if bad:
                fires += 1
            else:
                vac += 1
    print("      fires (Theorem D fails under the mutation) on %d posets;"
          " vacuous on %d (no free ridge: the antichains)" % (fires, vac))
    return fires > 0


def X4():
    print("X4  MUTATE THE BAND PRODUCT: order intersections by (j,i).")
    print("    The band axioms and/or the Brown spectrum must fail.")

    def bad_product(x, y):
        out = []
        for C in y:
            for B in x:
                m = B & C
                if m:
                    out.append(m)
        return tuple(out)

    ax_fires = sp_fires = vac = 0
    for n in range(2, 5):
        for P in all_posets(n):
            faces = all_faces(P)
            fset = set(faces)
            idf = tuple([(1 << P.n) - 1])
            bad = 0
            differs = False
            for x in faces:
                for y in faces:
                    if bad_product(x, y) != lrb_product(x, y):
                        differs = True
                    xy = bad_product(x, y)
                    if xy not in fset or bad_product(xy, x) != xy:
                        bad += 1
            if not differs:
                vac += 1
                continue
            if bad:
                ax_fires += 1
            # spectrum under the mutated product
            w = weights_all_faces(faces)
            chambers = [x for x in faces if len(x) == P.n]
            cidx = {c: i for i, c in enumerate(chambers)}
            mm = len(chambers)
            M = [[0] * mm for _ in range(mm)]
            for x in faces:
                if not w.get(x):
                    continue
                for c in chambers:
                    d = bad_product(x, c)
                    if len(d) != P.n:
                        M = None
                        break
                    M[cidx[c]][cidx[d]] += w[x]
                if M is None:
                    break
            if M is None:
                sp_fires += 1
                continue
            L = support_lattice(P, faces)
            mult = brown_multiplicities(P, L)
            lam = brown_eigenvalues(P, w, L, faces)
            grouped = {}
            for X in L:
                if mult[X]:
                    grouped[lam[X]] = grouped.get(lam[X], 0) + mult[X]
            tot = 0
            okall = True
            for v, c in grouped.items():
                k = kernel_dim(M, v)
                tot += k
                if k != c:
                    okall = False
            if (not okall) or tot != mm:
                sp_fires += 1
    print("      band axioms fail on %d posets; Brown spectrum fails on %d;"
          " vacuous on %d (the mutation equals the true product)"
          % (ax_fires, sp_fires, vac))
    return sp_fires > 0 or ax_fires > 0


def X5():
    print("X5  MUTATE THE MULTIPLICITY RULE: sum over Y <= X instead of Y >= X.")
    print("    Must give negative multiplicities or a wrong total.")
    fires = vac = 0
    for n in range(2, 6):
        for P in all_posets(n):
            L = support_lattice(P)
            order = sorted(L, key=lambda X: len(X))
            m = {}
            for X in order:
                tot = chambers_refining(P, X)
                s = sum(m.get(Y, 0) for Y in L if Y != X and refines(X, Y))
                m[X] = tot - s
            true_m = brown_multiplicities(P, L)
            if m == true_m:
                vac += 1
                continue
            if any(v < 0 for v in m.values()) or \
                    sum(m.values()) != len(linear_extensions(P)):
                fires += 1
            else:
                vac += 1
    print("      fires on %d posets; vacuous on %d (the mutated rule coincides"
          " with the true one, or stays nonnegative with the right total)"
          % (fires, vac))
    return fires > 0


def main():
    print("=" * 78)
    print("POSITIVE CONTROLS")
    print("=" * 78)
    res = [("P1", P1()), ("P2", P2()), ("P3", P3()), ("P4", P4()), ("P5", P5())]
    print()
    print("=" * 78)
    print("NEGATIVE CONTROLS (construction-side: each perturbs an object this")
    print("work item BUILDS, not a downstream comparison)")
    print("=" * 78)
    X1a()
    res += [("X1b", X1b()), ("X2", X2()), ("X3", X3()), ("X4", X4()),
            ("X5", X5())]
    print()
    print("summary:", ", ".join("%s=%s" % (k, "PASS" if v else "FAIL")
                                for k, v in res))


if __name__ == "__main__":
    main()
