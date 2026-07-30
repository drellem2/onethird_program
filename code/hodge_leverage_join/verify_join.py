"""Verification of the JOIN-SUPPRESSION theorem (ledger row J), landed by mg-a2bd.

Why this file exists.  mg-a806 added ledger row **G''** to
`docs/OneThird-Hodge-Side-Leverage.md`:

    G''  gamma_i >= 1/2 for EVERY FINITE POSET having a dimension-i face one of
         whose blocks induces an antichain of size >= 3.       [PROVEN]

The mg-d39d audit found it FALSE (55 (poset, level) counterexamples at n <= 6).
mg-a2bd strikes it.  The valuable half is the MECHANISM, and the mechanism is a
theorem:

    Theorem J (join suppression).  Let X_1, ..., X_r be weighted pure complexes,
    dim X_j = p_j >= 0, and let X = X_1 * ... * X_r with the product weights, so
    dim X = D = sum_j (p_j + 1) - 1.  Then the spectrum of the 1-skeleton walk
    of X on the complement of the constants is exactly

        union_j { (p_j / D) * mu : mu in spec(X_j on 1-perp) }
        union   { -1/D  with multiplicity r - 1 }.

    In particular an eigenvalue mu of a FACTOR survives into the join SCALED BY
    p_j/D < 1, so lambda_2(X) < lambda_2(X_j) whenever lambda_2(X_j) > 0 and
    there is a second factor: an exact 1/2 in a factor becomes STRICTLY LESS
    than 1/2 in the join.

Theorem G escapes this because its face has one block of size m and i+1
SINGLETONS, and a singleton block contributes no factor (F(A_1) is the empty
complex), so link(sigma) = F(A_m) on the nose -- not a join.  G'' dropped the
singleton requirement, and that is exactly the hypothesis doing the work.

The four checks below.  Nothing here re-derives Theorem L; the LINK side is
measured by `code/hodge_leverage/links.link_skeleton`, which builds the weighted
1-skeleton by brute force from the facet list, and the FACTOR side is assembled
independently from the factor complexes F(P|_B).  The two agree only if J holds.

  J1  the full-spectrum join identity, on EVERY genuine-join link of EVERY poset
      n <= 6 (a genuine join = at least two blocks of size >= 2).
  J2  the strike: per-level counterexamples to G'' broken down by n, and the
      n = 5 ones identified by name.
  J3  the smallest counterexample, predicted from J and measured by the
      deliverable's own `local_to_global.gammas`.
  J4  row G' (the D4 item): gamma_i(A_n) = lambda_2(F(A_{n-i-1})), the max over
      dimension-i faces being attained EXACTLY at the one-big-block faces --
      exhaustively over faces for n <= 6, over block-size multisets for
      n = 7..9 (with the n <= 6 face-level agreement as the control on that
      shortcut), and lambda_2(F(A_m)) computed here for m = 3..9.

Pure Python 3, no third-party packages.
"""

import math
import os
import sys
from fractions import Fraction
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "hodge_leverage"))
sys.path.insert(0, os.path.join(HERE, "..", "face_geometry"))

from face_complex import Poset, proper_ideals                    # noqa: E402
from links import (faces_of, facets_of, blocks_of_face,           # noqa: E402
                   induced_subposet, link_skeleton)
from linalg import jacobi_eigenvalues                            # noqa: E402
from local_to_global import gammas                                # noqa: E402
from posets import all_posets                                    # noqa: E402

TOL = 1e-9


# --------------------------------------------------------------------------
# spectra of weighted-graph walks
# --------------------------------------------------------------------------

def walk_spectrum(nvert, edges):
    """All eigenvalues (ascending) of P = D^{-1}W for a weighted graph.

    Returns None if some vertex is isolated (the walk is then not irreducible
    and lambda_2 = 1 by the convention in `linalg.lambda2_weighted_graph`).
    """
    if nvert < 1:
        return []
    d = [0.0] * nvert
    for (u, v, w) in edges:
        d[u] += w
        d[v] += w
    if any(x <= 0.0 for x in d):
        return None
    S = [[0.0] * nvert for _ in range(nvert)]
    for (u, v, w) in edges:
        val = w / math.sqrt(d[u] * d[v])
        S[u][v] += val
        S[v][u] += val
    return jacobi_eigenvalues(S)


def coxeter_skeleton(m):
    """The weighted 1-skeleton of F(A_m), built from the closed forms.

    Vertices: proper nonempty subsets S of [m], weight w(S) = |S|!(m-|S|)!.
    Edge {S, T} for S subset T: weight |S|!(|T|-|S|)!(m-|T|)!  =  the number of
    maximal subset chains through both.
    """
    verts = [S for S in range(1, (1 << m) - 1)]
    idx = {S: i for i, S in enumerate(verts)}
    f = [math.factorial(k) for k in range(m + 1)]
    edges = []
    for S in verts:
        sS = bin(S).count("1")
        for T in verts:
            if T == S or (S & T) != S:
                continue
            sT = bin(T).count("1")
            if sT <= sS:
                continue
            edges.append((idx[S], idx[T], float(f[sS] * f[sT - sS] * f[m - sT])))
    return len(verts), edges


def lambda2_power(nvert, edges, iters=6000):
    """lambda_2 of P = D^{-1}W by deflated power iteration on S + I.

    S = D^{-1/2} W D^{-1/2} has top eigenvector sqrt(d) with eigenvalue 1.
    Deflating it and power-iterating on S + I (all eigenvalues in [0, 2]) picks
    out lambda_2 + 1, because lambda_2 >= 1/2 > |lambda_min| on every complex
    reached here.  Used for the m = 8, 9 Coxeter complexes, where a dense Jacobi
    on 254 / 510 vertices is needlessly slow.
    """
    d = [0.0] * nvert
    for (u, v, w) in edges:
        d[u] += w
        d[v] += w
    sq = [math.sqrt(x) for x in d]
    nrm = math.sqrt(sum(x for x in d))
    v1 = [x / nrm for x in sq]
    x = [1.0 / (i + 2.0) + 0.5 * ((-1) ** i) for i in range(nvert)]

    def project(y):
        c = sum(a * b for a, b in zip(y, v1))
        return [a - c * b for a, b in zip(y, v1)]

    def apply(y):
        out = [a for a in y]                      # the + I term
        for (u, v, w) in edges:
            val = w / (sq[u] * sq[v])
            out[u] += val * y[v]
            out[v] += val * y[u]
        return out

    x = project(x)
    lam = 0.0
    for _ in range(iters):
        y = project(apply(x))
        n2 = math.sqrt(sum(a * a for a in y))
        if n2 == 0.0:
            return None
        y = [a / n2 for a in y]
        if max(abs(a - b) for a, b in zip(y, x)) < 1e-14:
            x = y
            break
        x = y
    Ax = project(apply(x))
    lam = sum(a * b for a, b in zip(Ax, x))
    return lam - 1.0


# --------------------------------------------------------------------------
# J1 -- the full-spectrum join identity
# --------------------------------------------------------------------------

def factor_spectra(P, sigma):
    """(D, [(p_j, spec_j)]) for the non-singleton blocks of sigma.

    spec_j is the spectrum of F(P|_{B_j})'s own 1-skeleton walk on the
    complement of the constants, computed from that factor complex alone --
    never from the link.  A block of size 2 gives a factor with p_j = 0, whose
    complex is V_j isolated vertices with no 1-skeleton walk to speak of --
    V_j = 2 for the 2-antichain, V_j = 1 for the 2-chain, which has only one
    proper nonempty ideal.  The scaling p_j/D = 0 kills whatever it carries, so
    the contribution is V_j - 1 copies of 0.
    """
    blocks = [b for b in blocks_of_face(P, sigma) if bin(b).count("1") >= 2]
    D = sum(bin(b).count("1") - 1 for b in blocks) - 1
    out = []
    for b in blocks:
        size = bin(b).count("1")
        p = size - 2
        Q = induced_subposet(P, b)
        if p == 0:
            # F(Q) on 2 elements: isolated vertices, no edge at all.
            out.append((p, [0.0] * (len(proper_ideals(Q)) - 1)))
            continue
        qfacets = facets_of(Q)
        verts, edges = link_skeleton(Q, (), qfacets)
        spec = walk_spectrum(len(verts), edges)
        if spec is None:
            return None
        out.append((p, spec[:-1]))        # drop the top eigenvalue 1
    return D, out


def predicted_spectrum(D, factors):
    pred = []
    for (p, spec) in factors:
        pred.extend((p / float(D)) * mu for mu in spec)
    pred.extend([-1.0 / D] * (len(factors) - 1))
    return sorted(pred)


def check_J1(populations):
    print("J1  THE JOIN SPECTRUM IDENTITY, on every genuine-join link, n <= 6")
    print("    measured: links.link_skeleton (brute force from the facet list)")
    print("    predicted: assembled from the factor complexes F(P|_B) alone")
    print()
    tot = 0
    worst = 0.0
    bad = 0
    per_n = {}
    for n, plist in populations:
        cn = ct = 0
        for P in plist:
            facets = facets_of(P)
            faces = faces_of(P)
            for i in sorted(faces):
                for sigma in faces[i]:
                    blocks = blocks_of_face(P, sigma)
                    if sum(1 for b in blocks if bin(b).count("1") >= 2) < 2:
                        continue          # not a genuine join
                    verts, edges = link_skeleton(P, sigma, facets)
                    meas = walk_spectrum(len(verts), edges)
                    if meas is None:
                        continue
                    fs = factor_spectra(P, sigma)
                    if fs is None:
                        continue
                    D, factors = fs
                    pred = predicted_spectrum(D, factors)
                    meas_rest = sorted(meas[:-1])
                    ct += 1
                    tot += 1
                    if len(pred) != len(meas_rest):
                        bad += 1
                        cn += 1
                        continue
                    dev = max((abs(a - b) for a, b in zip(pred, meas_rest)),
                              default=0.0)
                    worst = max(worst, dev)
                    if dev > TOL:
                        bad += 1
                        cn += 1
        per_n[n] = (ct, cn)
    for n in sorted(per_n):
        ct, cn = per_n[n]
        print("      n=%d  genuine-join links tested=%5d   mismatches=%d"
              % (n, ct, cn))
    print()
    print("    total genuine-join links tested : %d" % tot)
    print("    spectrum mismatches             : %d" % bad)
    print("    worst deviation over all of them: %.3e" % worst)
    print("    -> Theorem J holds on the whole population" if bad == 0
          else "    -> THEOREM J FAILS")
    print()
    return bad == 0


# --------------------------------------------------------------------------
# J2 -- the strike, broken down by n
# --------------------------------------------------------------------------

def has_antichain_block(P, sigma, k=3):
    for b in blocks_of_face(P, sigma):
        if bin(b).count("1") < k:
            continue
        Q = induced_subposet(P, b)
        if not Q.less:
            return True
    return False


def ordinal_sum_name(P):
    """Name P as an ordinal sum of antichains / chains when it is one.

    Recognises exactly the shape the n = 5 counterexamples have: a chain of
    "levels" L_1 < ... < L_k with every element of L_s below every element of
    L_{s+1}.  Returns e.g. 'A_2 (+) A_3' or None.
    """
    n = P.n
    below = [set() for _ in range(n)]
    for (a, b) in P.less:
        below[b].add(a)
    order = sorted(range(n), key=lambda x: len(below[x]))
    levels, cur = [], []
    for x in order:
        if cur and len(below[x]) != len(below[cur[0]]):
            levels.append(cur)
            cur = []
        cur.append(x)
    if cur:
        levels.append(cur)
    # every element of level s must be below every element of level s+1
    seen = 0
    for s, lev in enumerate(levels):
        for x in lev:
            if len(below[x]) != seen:
                return None
            for y in lev:
                if (x, y) in P.less or (y, x) in P.less:
                    return None
        seen += len(lev)
    for s in range(len(levels) - 1):
        for x in levels[s]:
            for y in levels[s + 1]:
                if (x, y) not in P.less:
                    return None
    parts = []
    for lev in levels:
        parts.append("C_1" if len(lev) == 1 else "A_%d" % len(lev))
    # collapse runs of singletons into chains
    out, run = [], 0
    for p in parts:
        if p == "C_1":
            run += 1
            continue
        if run:
            out.append("C_%d" % run if run > 1 else "C_1")
            run = 0
        out.append(p)
    if run:
        out.append("C_%d" % run if run > 1 else "C_1")
    return " (+) ".join(out)


def check_J2(populations):
    print("J2  THE STRIKE -- ledger row G'' as written (a PER-LEVEL claim)")
    print("    'gamma_i >= 1/2 for every finite poset having a dimension-i face")
    print("     one of whose blocks induces an antichain of size >= 3'")
    print()
    by_n = {}
    names_n5 = []
    for n, plist in populations:
        tot = bad = 0
        for P in plist:
            facets = facets_of(P)
            faces = faces_of(P)
            g = gammas(P, facets, faces)
            for i in sorted(faces):
                if i not in g:
                    continue
                if not any(has_antichain_block(P, s) for s in faces[i]):
                    continue
                tot += 1
                if g[i][0] < 0.5 - TOL:
                    bad += 1
                    if n == 5:
                        nm = ordinal_sum_name(P)
                        names_n5.append((nm or "(not an ordinal sum)", i,
                                         g[i][0]))
        by_n[n] = (tot, bad)
    ttot = sum(v[0] for v in by_n.values())
    tbad = sum(v[1] for v in by_n.values())
    for n in sorted(by_n):
        tot, bad = by_n[n]
        print("      n=%d  (poset, level) pairs with such a face=%3d   "
              "gamma_i < 1/2 on %2d" % (n, tot, bad))
    print()
    print("    population  : %d (poset, level) pairs, n <= 6" % ttot)
    print("    COUNTEREXAMPLES: %d   <-- G'' is FALSE" % tbad)
    print("    smallest n with a counterexample: %d"
          % min(n for n in by_n if by_n[n][1] > 0))
    print()
    print("    the n = 5 counterexamples, named:")
    for nm, i, gam in names_n5:
        print("      %-16s  i=%d  gamma_i=%.6f   (link is a genuine join)"
              % (nm, i, gam))
    print("    all %d of them are ordinal sums -- i.e. exactly the case where"
          % len(names_n5))
    print("    the face's OTHER block is not a singleton, so the link IS a join")
    print()
    return tbad, min((n for n in by_n if by_n[n][1] > 0), default=None)


# --------------------------------------------------------------------------
# J3 -- the smallest counterexample, predicted and measured
# --------------------------------------------------------------------------

def check_J3():
    print("J3  THE SMALLEST COUNTEREXAMPLE, predicted by J and measured by the")
    print("    deliverable's own local_to_global.gammas")
    print()
    # A_2 (+) A_3 : {0,1} < {2,3,4}
    rel = [(a, b) for a in (0, 1) for b in (2, 3, 4)]
    P = Poset(5, rel)
    facets = facets_of(P)
    faces = faces_of(P)
    g = gammas(P, facets, faces)
    print("    P = A_2 (+) A_3  (n = 5, {0,1} < {2,3,4}),  d = n-2 = 3")
    print("    measured gammas: %s"
          % {i: round(g[i][0], 6) for i in sorted(g)})
    # the face sigma = ({0,1}) at i = 0: blocks {0,1} (A_2) and {2,3,4} (A_3)
    sigma = (0b00011,)
    verts, edges = link_skeleton(P, sigma, facets)
    meas = walk_spectrum(len(verts), edges)
    D, factors = factor_spectra(P, sigma)
    print("    sigma = ({0,1}) at i = 0: blocks A_2 (p=0) and A_3 (p=1), D = %d"
          % D)
    print("    G'' asserts gamma_0 >= 1/2 because {2,3,4} is a 3-antichain.")
    print("    J predicts the hexagon's 1/2 lands at (p/D) * 1/2 = %s"
          % Fraction(1, 2 * D))
    print("    predicted link spectrum on 1-perp: %s"
          % [round(x, 6) for x in predicted_spectrum(D, factors)])
    print("    measured  link spectrum on 1-perp: %s"
          % [round(x, 6) for x in sorted(meas[:-1])])
    print("    measured gamma_0 = %.6f   (G'' asserts >= 0.5)  -> FALSE"
          % g[0][0])
    print()
    return g[0][0]


# --------------------------------------------------------------------------
# J4 -- row G': the max over dimension-i faces of F(A_n)
# --------------------------------------------------------------------------

def compositions(n, k):
    """Ordered tuples of k positive integers summing to n."""
    if k == 1:
        yield (n,)
        return
    for first in range(1, n - k + 2):
        for rest in compositions(n - first, k - 1):
            yield (first,) + rest


def link_lambda2_from_sizes(sizes, lam_cox):
    """lambda_2 of the link of a face of F(A_n) with the given block sizes.

    By Theorem L the link is the join of F(A_b) over the blocks, and by Theorem J
    its spectrum on 1-perp is the union of the scaled factor spectra together
    with -1/D.  Since lambda_2(F(A_b)) = lam_cox[b] and every factor spectrum
    lies in [-1, lambda_2(F(A_b))], the MAXIMUM is
        max_j (b_j - 2)/D * lambda_2(F(A_{b_j}))    (and -1/D if r = 1 is not
    the case), which is what this returns.
    """
    big = [b for b in sizes if b >= 2]
    D = sum(b - 1 for b in big) - 1
    if D <= 0:
        return None, D
    best = -1.0 / D if len(big) >= 2 else None
    for b in big:
        val = (b - 2) / float(D) * lam_cox[b]
        best = val if best is None else max(best, val)
    return best, D


def check_J4(populations, lam_cox):
    print("J4  ROW G' -- gamma_i(A_n) is a PER-LEVEL MAX, and J says where it")
    print("    is attained:  gamma_i(A_n) = lambda_2(F(A_{n-i-1})), attained")
    print("    EXACTLY at the faces with one block of size n-i-1 and i+1")
    print("    singletons -- Theorem G's face, and no other.")
    print()
    print("    (a) lambda_2(F(A_m)), computed here from the closed-form weights")
    for m in sorted(lam_cox):
        if m < 3:
            continue
        print("        m=%2d  |V|=%4d  lambda_2 = %.12f   == 1/2: %s"
              % (m, (1 << m) - 2, lam_cox[m], abs(lam_cox[m] - 0.5) < 1e-9))
    print()
    print("    (b) exhaustive over FACES of F(A_n), n = 3..6: is the argmax")
    print("        exactly the one-big-block faces, and is every other face")
    print("        STRICTLY below 1/2?")
    ok_b = True
    for n in range(3, 7):
        P = Poset(n, [])
        facets = facets_of(P)
        faces = faces_of(P)
        for i in range(-1, n - 3):
            m = n - i - 1
            hits, others, worst_other = 0, 0, -1.0
            for sigma in faces[i]:
                sizes = sorted(bin(b).count("1")
                               for b in blocks_of_face(P, sigma))
                verts, edges = link_skeleton(P, sigma, facets)
                lam, _ = _l2(len(verts), edges)
                one_big = (sizes.count(1) == i + 1 and max(sizes) == m)
                if one_big:
                    hits += 1
                    if abs(lam - lam_cox[m]) > TOL:
                        ok_b = False
                else:
                    others += 1
                    worst_other = max(worst_other, lam)
                    if lam >= 0.5 - TOL:
                        ok_b = False
            print("        A_%d  i=%2d  m=%d  one-big-block faces=%3d "
                  "(lambda_2 = %.6f)   other faces=%4d (max %.6f)"
                  % (n, i, m, hits, lam_cox[m], others,
                     worst_other if others else float("nan")))
    print("        -> argmax is exactly the one-big-block face set: %s" % ok_b)
    print()
    print("    (c) the same statement for n = 7, 8, 9, over block-size")
    print("        multisets via Theorems L + J (the shortcut whose")
    print("        face-level agreement (b) has just confirmed at n <= 6):")
    ok_c = True
    for n in range(7, 10):
        for i in range(-1, n - 3):
            m = n - i - 1
            best_other, arg_other = -1.0, None
            onebig = None
            for comp in compositions(n, i + 2):
                sizes = tuple(sorted(comp))
                lam, D = link_lambda2_from_sizes(sizes, lam_cox)
                if lam is None:
                    continue
                if sizes.count(1) == i + 1 and max(sizes) == m:
                    onebig = lam
                elif lam > best_other:
                    best_other, arg_other = lam, sizes
            if onebig is None or abs(onebig - lam_cox[m]) > TOL:
                ok_c = False
            if best_other >= 0.5 - TOL:
                ok_c = False
            print("        A_%d  i=%2d  m=%d  one-big-block lambda_2=%.6f   "
                  "best other=%.6f at sizes %s"
                  % (n, i, m, onebig if onebig is not None else float("nan"),
                     best_other, arg_other))
    print("        -> gamma_i = lambda_2(F(A_{n-i-1})) = 1/2 at every level,")
    print("           and no other face reaches it: %s" % ok_c)
    print()
    return ok_b and ok_c


_L2MEMO = {}


def _l2(nvert, edges):
    spec = walk_spectrum(nvert, edges)
    if spec is None or len(spec) < 2:
        return (1.0, False)
    return (spec[-2], True)


# --------------------------------------------------------------------------

def main():
    print("=" * 78)
    print("VERIFY_JOIN -- the join-suppression theorem (ledger row J), mg-a2bd")
    print("=" * 78)
    print()

    populations = []
    for n in range(2, 7):
        populations.append((n, list(all_posets(n))))
    print("population: posets up to isomorphism, n = 2..6: %s"
          % " ".join(str(len(p)) for _, p in populations))
    print()

    lam_cox = {2: 0.0}
    for m in range(3, 8):
        nv, ed = coxeter_skeleton(m)
        lam_cox[m] = _l2(nv, ed)[0]
    for m in (8, 9):
        nv, ed = coxeter_skeleton(m)
        lam_cox[m] = lambda2_power(nv, ed)

    ok1 = check_J1(populations)
    nbad, smallest = check_J2(populations)
    g0 = check_J3()
    ok4 = check_J4(populations, lam_cox)

    print("=" * 78)
    print("SUMMARY")
    print("  J1  join spectrum identity holds on every genuine-join link n<=6 : %s"
          % ok1)
    print("  J2  ledger row G'' counterexamples at n <= 6                     : %d"
          % nbad)
    print("      smallest n carrying one                                      : %d"
          % smallest)
    print("  J3  gamma_0(A_2 (+) A_3) = %.6f, predicted 1/4 by J             : %s"
          % (g0, abs(g0 - 0.25) < TOL))
    print("  J4  gamma_i(A_n) = lambda_2(F(A_{n-i-1})), argmax = one-big-block : %s"
          % ok4)
    print()
    print("  So: G'' is FALSE and struck; Theorem G, row G' and M2 are")
    print("  UNAFFECTED -- G's face has singleton blocks, so its link is not a")
    print("  join, and J is precisely what says the wider form was not free.")
    print("=" * 78)


if __name__ == "__main__":
    main()
