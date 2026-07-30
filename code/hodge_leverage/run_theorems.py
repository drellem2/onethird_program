"""Verification of the four new structural statements, and of the two negatives.

Committed output: `theorems_output.txt`.

  D. The down-up walk on the facets of F(P) is the lazy adjacent-transposition
     walk:  I - P_du = Delta_AT / (2(n-1)).  Exact rational check.
  L. Localisation: link_{F(P)}(sigma) is the simplicial join of the F(Q_i) over
     the blocks Q_i of sigma.  Checked as a simplicial isomorphism, face by face.
  H. Codimension-2 links: the complete list is P_2, P_3, P_4, C_4, C_6, with
     lambda_2 = -1, 0, 1/2, 0, 1/2.  C_4 is a commuting pair of moves, C_6 the
     braid hexagon, and P_4/P_3/P_2 are their boundary truncations.
  G. gamma_i = 1/2 at every level for the antichain: the explicit eigenfunction
     f(S) = sum_{i in S} a_i, sum a_i = 0, has eigenvalue exactly 1/2.
  N1 (negative). Twisted, the top relative boundary map IS the signed
     vertex-edge incidence matrix of the adjacent-transposition graph:
     Delta_AT = N^T N.  So the top-degree Hodge structure is the classical
     incidence factorisation and carries nothing new.
  N2 (negative). Representation theory does not descend: for every non-antichain
     the span of the shape-alpha faces is not an S_n-submodule of
     Ind_{S_alpha}^{S_n} 1; and even for the antichain, sum_i s_i is not central,
     so characters do not diagonalise Delta_AT.
"""

import math
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "face_geometry"))

from face_complex import (Poset, proper_ideals, linear_extensions, le_to_facet,
                          adjacent_transposition_graph, perm_sign, top_laplacians,
                          twist)
from posets import all_posets, cover_string
from links import (faces_of, facets_of, blocks_of_face, induced_subposet,
                   link_skeleton, canon_key)
from linalg import lambda2_weighted_graph
from lrb import all_faces


# --------------------------------------------------------------------------
# D. the down-up walk
# --------------------------------------------------------------------------

def down_up_exact(P):
    """P_du as a sparse dict-of-dicts of Fractions, from ridge incidence only."""
    facets = facets_of(P)
    fidx = {f: i for i, f in enumerate(facets)}
    nr = P.n - 1
    ridge_facets = {}
    for f in facets:
        for i in range(len(f)):
            r = f[:i] + f[i + 1:]
            ridge_facets.setdefault(r, []).append(f)
    M = {}
    for f in facets:
        i = fidx[f]
        row = M.setdefault(i, {})
        for k in range(len(f)):
            r = f[:k] + f[k + 1:]
            cof = ridge_facets[r]
            for g in cof:
                j = fidx[g]
                row[j] = row.get(j, Fraction(0)) + Fraction(1, nr * len(cof))
    return facets, fidx, M


def check_D(P):
    """I - P_du == Delta_AT/(2(n-1))?  Returns (ok, applicable).

    Compared on the union of the two supports (both matrices are sparse), so the
    check is over every position where either side is nonzero.
    """
    if P.n < 2:
        return True, False
    facets, fidx, Pdu = down_up_exact(P)
    les, A, deg = adjacent_transposition_graph(P)
    order = [fidx[le_to_facet(w)] for w in les]
    inv = {order[a]: a for a in range(len(les))}
    m = len(les)
    c = Fraction(1, 2 * (P.n - 1))
    for a in range(m):
        i = order[a]
        row = Pdu.get(i, {})
        support = set(row) | {i} | {order[b] for b in range(m) if A[a][b]}
        for j in support:
            b = inv[j]
            lhs = (1 if a == b else 0) - row.get(j, Fraction(0))
            rhs = c * ((deg[a] if a == b else 0) - A[a][b])
            if lhs != rhs:
                return False, True
    return True, (m >= 2)


# --------------------------------------------------------------------------
# L. localisation
# --------------------------------------------------------------------------

def check_L(P):
    """For every face sigma: link(sigma) is the join of F(Q_i) over the blocks.

    The claimed isomorphism sends a link vertex K (a proper ideal of P with
    sigma + {K} a chain) to the pair (i, K \\ I_i) where i is the unique index
    with I_i subset K subset I_{i+1}.  Verified to be (a) a bijection onto
    the disjoint union of the proper nonempty ideals of the blocks and (b) a
    simplicial isomorphism: a set of link vertices is a face of the link iff the
    image sets form a chain of ideals inside each block.
    """
    faces = faces_of(P)
    facets = facets_of(P)
    full = (1 << P.n) - 1
    bad = 0
    checked = 0
    for d in sorted(faces):
        for sigma in faces[d]:
            bounds = [0] + list(sigma) + [full]
            blocks = blocks_of_face(P, sigma)
            Qs = [induced_subposet(P, b) for b in blocks]
            # (a) target vertex set
            target = set()
            for i, Q in enumerate(Qs):
                elts = [x for x in range(P.n) if (blocks[i] >> x) & 1]
                for pid in proper_ideals(Q):
                    m = 0
                    for j, x in enumerate(elts):
                        if (pid >> j) & 1:
                            m |= 1 << x
                    target.add((i, m))
            verts, _ = link_skeleton(P, sigma, facets)
            img = {}
            for K in verts:
                i = None
                for t in range(len(bounds) - 1):
                    if (bounds[t] & K) == bounds[t] and (K & bounds[t + 1]) == K \
                            and K != bounds[t] and K != bounds[t + 1]:
                        i = t
                        break
                if i is None:
                    bad += 1
                    continue
                img[K] = (i, K & ~bounds[i])
            if set(img.values()) != target or len(set(img.values())) != len(verts):
                bad += 1
                continue
            # (b) simplicial isomorphism, on every subset of link vertices that
            # the link's own face list contains, and every subset the join
            # predicts -- so both directions.
            link_faces = set()
            for f in facets:
                if set(sigma) <= set(f):
                    rest = tuple(sorted(set(f) - set(sigma)))
                    for mask in range(1 << len(rest)):
                        sub = tuple(rest[j] for j in range(len(rest))
                                    if (mask >> j) & 1)
                        link_faces.add(sub)
            for sub in link_faces:
                per_block = {}
                for K in sub:
                    i, mm = img[K]
                    per_block.setdefault(i, []).append(mm)
                ok = True
                for i, ms in per_block.items():
                    ms = sorted(ms)
                    for a in range(len(ms) - 1):
                        if (ms[a] & ms[a + 1]) != ms[a] or ms[a] == ms[a + 1]:
                            ok = False
                if not ok:
                    bad += 1
            # reverse direction, without enumerating subsets: the forward map is
            # injective and lands in the join's face set, so equality of the two
            # face sets follows from equality of their cardinalities.  The join's
            # f-vector is the convolution of the factors' f-vectors.
            conv = [1]
            for Q in Qs:
                fq = faces_of(Q)
                fv = [0] * (Q.n + 1)
                fv[0] = 1                      # the empty face
                for dd in sorted(fq):
                    if dd >= 0:
                        fv[dd + 1] = len(fq[dd])
                new = [0] * (len(conv) + len(fv) - 1)
                for a, ca in enumerate(conv):
                    if not ca:
                        continue
                    for b, cb in enumerate(fv):
                        if cb:
                            new[a + b] += ca * cb
                conv = new
            if sum(conv) != len(link_faces):
                bad += 1
            checked += 1
    return checked, bad


# --------------------------------------------------------------------------
# H. codimension-2 links
# --------------------------------------------------------------------------

def graph_type(nv, edges):
    """Name the 1-dimensional link: P_m (path) or C_m (cycle), else 'other'."""
    deg = [0] * nv
    for (u, v, w) in edges:
        deg[u] += 1
        deg[v] += 1
    if nv == 0:
        return "empty"
    if max(deg) > 2:
        return "other(maxdeg=%d)" % max(deg)
    ends = sum(1 for d in deg if d == 1)
    if len(edges) == nv and ends == 0:
        return "C_%d" % nv
    if len(edges) == nv - 1 and ends == 2:
        return "P_%d" % nv
    if nv == 2 and len(edges) == 1:
        return "P_2"
    return "other(nv=%d,ne=%d,ends=%d)" % (nv, len(edges), ends)


def check_H(P):
    """Classify the codimension-2 links of F(P).  Returns dict type -> (count,
    lambda2, block-signature examples)."""
    n = P.n
    d = n - 2
    if d < 2:
        return {}
    faces = faces_of(P)
    facets = facets_of(P)
    out = {}
    for sigma in faces.get(d - 2, []):
        verts, edges = link_skeleton(P, sigma, facets)
        t = graph_type(len(verts), edges)
        lam, conn = lambda2_weighted_graph(len(verts), edges)
        sig = tuple(sorted(canon_key(induced_subposet(P, b))
                           for b in blocks_of_face(P, sigma) if bin(b).count("1") > 1))
        rec = out.setdefault(t, {"count": 0, "lam": set(), "sigs": set()})
        rec["count"] += 1
        rec["lam"].add(None if lam is None else round(lam, 12))
        rec["sigs"].add(sig)
    return out


# --------------------------------------------------------------------------
# G. the 1/2 eigenfunction on the antichain
# --------------------------------------------------------------------------

def check_G(n):
    """The 1-skeleton of F(A_n): the walk from a proper nonempty S subset [n]
    picks a uniform maximal chain through S and then a uniform other vertex of
    it.  Claim: f(S) = sum_{i in S} a_i with sum_i a_i = 0 satisfies Pf = f/2.

    Checked here by building the weighted 1-skeleton and applying the walk to
    such an f, exactly (Fractions).
    """
    P = Poset(n, [])
    facets = facets_of(P)
    verts, edges = link_skeleton(P, (), facets)
    nv = len(verts)
    dd = [0] * nv
    adj = [[] for _ in range(nv)]
    for (u, v, w) in edges:
        dd[u] += w
        dd[v] += w
        adj[u].append((v, w))
        adj[v].append((u, w))
    # a with sum zero: a_i = i - (n-1)/2, scaled to integers
    a = [Fraction(2 * i - (n - 1), 1) for i in range(n)]
    assert sum(a) == 0
    f = []
    for S in verts:
        f.append(sum(a[i] for i in range(n) if (S >> i) & 1))
    worst = Fraction(0)
    for u in range(nv):
        s = sum(Fraction(int(w)) * f[v] for (v, w) in adj[u])
        lhs = s / Fraction(int(dd[u]))
        diff = abs(lhs - f[u] / 2)
        if diff > worst:
            worst = diff
    # the full spectrum is only needed to confirm that 1/2 is the SECOND
    # eigenvalue and not merely an eigenvalue; the dense solver is capped.
    lam = None
    if nv <= 130:
        lam, _ = lambda2_weighted_graph(nv, edges)
    return nv, worst, lam


# --------------------------------------------------------------------------
# N1. Delta_AT = N^T N with N the signed incidence matrix
# --------------------------------------------------------------------------

def check_N1(P):
    """Twisted, the relative top boundary map is the signed vertex-edge
    incidence matrix of the adjacent-transposition graph, up to row signs.

    Concretely: build N (rows = edges of the AT graph, entries +1/-1 at the two
    endpoints) and check E L^rel E == N^T N.
    """
    if P.n < 2:
        return True, False
    T = top_laplacians(P)
    les = T["les"]
    Lrel_tw = twist(T["L_rel"], les)
    idx = {w: i for i, w in enumerate(les)}
    _, A, _ = adjacent_transposition_graph(P)
    m = len(les)
    rows = []
    for i in range(m):
        for j in range(i + 1, m):
            if A[i][j]:
                rows.append((i, j))
    NtN = [[0] * m for _ in range(m)]
    for (i, j) in rows:
        NtN[i][i] += 1
        NtN[j][j] += 1
        NtN[i][j] -= 1
        NtN[j][i] -= 1
    ok = all(Lrel_tw[i][j] == NtN[i][j] for i in range(m) for j in range(m))
    return ok, len(rows) > 0


# --------------------------------------------------------------------------
# N2. representation theory does not descend
# --------------------------------------------------------------------------

def check_N2(P):
    """For each shape alpha with >= 2 parts, is the set of P-compatible ordered
    partitions of shape alpha equal to ALL ordered partitions of that shape?

    S_n acts transitively on the ordered partitions of a fixed shape, so the
    span of the compatible ones is an S_n-submodule of Ind_{S_alpha}^{S_n} 1 iff
    it is everything (it is never zero -- cutting a linear extension into
    consecutive blocks always gives a compatible face).  Returns
    (n_shapes, n_stable, n_nonempty).
    """
    from itertools import permutations
    n = P.n
    faces = all_faces(P)
    shapes = {}
    for x in faces:
        if len(x) < 2:
            continue
        shapes.setdefault(tuple(bin(b).count("1") for b in x), set()).add(x)
    n_stable = 0
    for alpha, compat in shapes.items():
        # total number of ordered partitions of shape alpha
        tot = math.factorial(n)
        for a in alpha:
            tot //= math.factorial(a)
        if len(compat) == tot:
            n_stable += 1
    return len(shapes), n_stable, len(shapes)


def sum_si_central(n):
    """Is sum_i s_i central in C[S_n]?  It is iff {s_1..s_{n-1}} is closed under
    conjugation, i.e. iff it is the whole class of transpositions."""
    return (n - 1) == n * (n - 1) // 2


# --------------------------------------------------------------------------

def main():
    print("=" * 78)
    print("D. THE DOWN-UP WALK IS THE LAZY ADJACENT-TRANSPOSITION WALK")
    print("   I - P_du  ==  Delta_AT / (2(n-1)),  exact rational check")
    print("=" * 78)
    for n in range(1, 7):
        ok = tot = nontriv = 0
        for P in all_posets(n):
            tot += 1
            good, appl = check_D(P)
            ok += 1 if good else 0
            nontriv += 1 if appl else 0
        print("n=%d  posets=%3d  identity holds on %3d  (non-degenerate,"
              " |L(P)|>=2: %3d)" % (n, tot, ok, nontriv))

    print()
    print("=" * 78)
    print("L. LOCALISATION: link(sigma) = join of F(Q_i) over the blocks of sigma")
    print("   verified as a simplicial isomorphism, every face of every poset")
    print("=" * 78)
    for n in range(1, 6):
        tot = faces_checked = bad = 0
        for P in all_posets(n):
            tot += 1
            c, b = check_L(P)
            faces_checked += c
            bad += b
        print("n=%d  posets=%3d   faces checked=%6d   isomorphism failures=%d"
              % (n, tot, faces_checked, bad))

    print()
    print("=" * 78)
    print("H. CODIMENSION-2 LINKS: the complete list")
    print("=" * 78)
    agg = {}
    for n in range(4, 7):
        for P in all_posets(n):
            for t, rec in check_H(P).items():
                a = agg.setdefault(t, {"count": 0, "lam": set(), "sigs": set()})
                a["count"] += rec["count"]
                a["lam"] |= rec["lam"]
                a["sigs"] |= rec["sigs"]
    print("  over all posets with 4 <= n <= 6:")
    print("  %-8s %8s  %-18s  %s" % ("link", "count", "lambda_2", "block types"
                                     " (non-singleton blocks, canonical)"))
    for t in sorted(agg):
        a = agg[t]
        sig_names = sorted({fmt_sig(s) for s in a["sigs"]})
        print("  %-8s %8d  %-18s  %s"
              % (t, a["count"], ",".join(str(x) for x in sorted(a["lam"])),
                 "; ".join(sig_names)))
    print()
    print("  reading: C_4 = two commuting moves s_t s_u = s_u s_t (|t-u|>=2);")
    print("           C_6 = the braid hexagon s_t s_{t+1} s_t = s_{t+1} s_t s_{t+1};")
    print("           P_4, P_3, P_2 = the same two pictures truncated by the")
    print("           boundary (free ridges deleted).  lambda_2 <= 1/2 always,")
    print("           attained exactly at C_6 and P_4.")

    print()
    print("=" * 78)
    print("G. gamma = 1/2 IS ATTAINED BY AN EXPLICIT EIGENFUNCTION (antichain)")
    print("   f(S) = sum_{i in S} a_i with sum a_i = 0;  claim P f = f/2")
    print("=" * 78)
    for n in range(3, 9):
        nv, worst, lam = check_G(n)
        print("  A_%d: 1-skeleton has %4d vertices;  max_u |(Pf)(u) - f(u)/2| ="
              " %s (exact);  lambda_2 = %s"
              % (n, nv, worst,
                 ("%.12f" % lam) if lam is not None else "(dense solver capped)"))

    print()
    print("=" * 78)
    print("N1. TWISTED, THE TOP RELATIVE BOUNDARY IS THE SIGNED INCIDENCE MATRIX")
    print("    E L^rel E == N^T N   (so the top-degree Hodge structure is the")
    print("    classical incidence factorisation of the graph Laplacian)")
    print("=" * 78)
    for n in range(1, 7):
        ok = tot = nontriv = 0
        for P in all_posets(n):
            tot += 1
            good, appl = check_N1(P)
            ok += 1 if good else 0
            nontriv += 1 if appl else 0
        print("n=%d  posets=%3d   identity holds on %3d   (with >=1 edge: %3d)"
              % (n, tot, ok, nontriv))

    print()
    print("=" * 78)
    print("N2. REPRESENTATION THEORY DOES NOT DESCEND")
    print("=" * 78)
    for n in range(2, 6):
        tot = 0
        allstable = 0
        anti = 0
        for P in all_posets(n):
            tot += 1
            ns, nstab, _ = check_N2(P)
            if ns == nstab:
                allstable += 1
                if P.is_antichain():
                    anti += 1
        print("n=%d  posets=%3d   posets on which EVERY shape-alpha face span is"
              " an S_n-submodule: %d  (of which antichains: %d)"
              % (n, tot, allstable, anti))
    print()
    print("  and even where the S_n symmetry is present (the antichain),")
    print("  sum_i s_i is central in C[S_n] iff n-1 = C(n,2):")
    for n in range(2, 8):
        print("    n=%d: %s" % (n, sum_si_central(n)))


def fmt_sig(sig):
    if not sig:
        return "(all blocks singletons)"
    names = []
    for (k, rel) in sig:
        if k == 2:
            names.append("A_2" if not rel else "C_2")
        elif k == 3:
            if not rel:
                names.append("A_3")
            elif len(rel) == 3:
                names.append("C_3")
            elif len(rel) == 1:
                names.append("A_1+C_2")
            else:
                mins = {a for (a, b) in rel}
                names.append("V" if len(mins) == 1 else "Lambda")
        else:
            names.append("size%d" % k)
    return "+".join(names)


if __name__ == "__main__":
    main()
