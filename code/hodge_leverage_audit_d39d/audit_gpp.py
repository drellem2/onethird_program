"""mg-d39d, independent audit of mg-a806.

Target: the NEW ledger row **G''** added by mg-a806 to
`docs/OneThird-Hodge-Side-Leverage.md` §11 and asserted in §6:

    G''  gamma_i >= 1/2 for EVERY FINITE POSET having a dimension-i face one of
         whose blocks induces an antichain of size >= 3.
         label: PROVEN (§6; "free from G + Theorem L")

Nothing in `code/hodge_leverage/` is imported.  The poset enumeration, the
compatible face complex, the links, the induced weights and the eigenvalue
routine are all rebuilt here from their definitions.

Two things are measured, separately, because they are different statements:

  (a) the PER-FACE reading the §6 sentence actually argues for --
      lambda_2(link(sigma)) >= 1/2 whenever one block of sigma induces an
      antichain of size >= 3;
  (b) the PER-LEVEL reading the ledger row states --
      gamma_i = max over dim-i faces >= 1/2 whenever SOME dim-i face has such a
      block.

Run:  python3 audit_gpp.py
"""

import itertools
import math
import sys

# --------------------------------------------------------------------------
# posets on n elements, up to isomorphism -- built by adding one maximal
# element at a time, deduplicated by brute-force canonical form.
# --------------------------------------------------------------------------


def closure(n, rel):
    """transitive closure of a set of strict pairs"""
    r = set(rel)
    changed = True
    while changed:
        changed = False
        for (a, b) in list(r):
            for (c, d) in list(r):
                if b == c and (a, d) not in r:
                    r.add((a, d))
                    changed = True
    return frozenset(r)


def canon(n, rel):
    best = None
    for p in itertools.permutations(range(n)):
        t = tuple(sorted((p[a], p[b]) for (a, b) in rel))
        if best is None or t < best:
            best = t
    return (n, best)


def down_sets(n, rel):
    """order ideals (down-closed subsets) as bitmasks"""
    below = [0] * n
    for (a, b) in rel:
        below[b] |= 1 << a
    out = []
    for m in range(1 << n):
        ok = True
        for x in range(n):
            if (m >> x) & 1 and (below[x] & ~m):
                ok = False
                break
        if ok:
            out.append(m)
    return out


def all_posets(nmax):
    """dict n -> list of frozenset-of-pairs, one per isomorphism class"""
    res = {0: [frozenset()]}
    for n in range(1, nmax + 1):
        seen = {}
        for rel in res[n - 1]:
            for I in down_sets(n - 1, rel):
                new = set(rel)
                for x in range(n - 1):
                    if (I >> x) & 1:
                        new.add((x, n - 1))
                r2 = closure(n, new)
                k = canon(n, r2)
                if k not in seen:
                    seen[k] = r2
        res[n] = list(seen.values())
    return res


# --------------------------------------------------------------------------
# F(P): the order complex of the proper part of J(P)
# --------------------------------------------------------------------------


def proper_ideals(n, rel):
    full = (1 << n) - 1
    return [m for m in down_sets(n, rel) if m != 0 and m != full]


def maximal_chains(n, rel):
    """facets of F(P): chains of proper nonempty ideals of length n-1,
    i.e. one ideal of each cardinality 1..n-1"""
    ids = proper_ideals(n, rel)
    by_size = {}
    for m in ids:
        by_size.setdefault(bin(m).count("1"), []).append(m)
    facets = []

    def rec(k, cur, prev):
        if k == n:
            facets.append(tuple(cur))
            return
        for m in by_size.get(k, []):
            if (prev & m) == prev:
                cur.append(m)
                rec(k + 1, cur, m)
                cur.pop()

    rec(1, [], 0)
    return facets


def all_chains(n, rel):
    """every face of F(P) as a tuple of ideals in increasing order,
    grouped by dimension (= len - 1); dimension -1 is the empty face"""
    ids = sorted(proper_ideals(n, rel), key=lambda m: (bin(m).count("1"), m))
    out = {-1: [()]}
    cur = [(m,) for m in ids]
    d = 0
    while cur:
        out[d] = cur
        nxt = []
        for c in cur:
            top = c[-1]
            for m in ids:
                if m != top and (top & m) == top:
                    nxt.append(c + (m,))
        cur = nxt
        d += 1
    return out


def blocks(n, sigma):
    full = (1 << n) - 1
    prev = 0
    bs = []
    for I in sigma:
        bs.append(I & ~prev)
        prev = I
    bs.append(full & ~prev)
    return bs


def induces_antichain(rel, mask, size):
    elts = [x for x in range(64) if (mask >> x) & 1]
    if len(elts) < size:
        return False
    s = set(elts)
    for (a, b) in rel:
        if a in s and b in s:
            return False
    return True


def link_weighted_skeleton(n, sigma, facets):
    """vertices and weighted edges of the 1-skeleton of link(sigma),
    weights induced from the uniform measure on facets"""
    ss = set(sigma)
    cont = [set(f) for f in facets if ss <= set(f)]
    verts = set()
    for f in cont:
        verts |= (f - ss)
    verts = sorted(verts)
    idx = {v: i for i, v in enumerate(verts)}
    ew = {}
    for f in cont:
        rest = sorted(f - ss)
        for a in range(len(rest)):
            for b in range(a + 1, len(rest)):
                key = (idx[rest[a]], idx[rest[b]])
                ew[key] = ew.get(key, 0) + 1
    return verts, [(i, j, float(w)) for (i, j), w in sorted(ew.items())]


# --------------------------------------------------------------------------
# lambda_2 = second largest eigenvalue of the walk D^{-1} W  (own Jacobi)
# --------------------------------------------------------------------------


def jacobi_eigs(A):
    m = len(A)
    a = [row[:] for row in A]
    for _ in range(100):
        off = 0.0
        for i in range(m):
            for j in range(i + 1, m):
                off += a[i][j] * a[i][j]
        if off < 1e-24:
            break
        for p in range(m):
            for q in range(p + 1, m):
                if abs(a[p][q]) < 1e-18:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(m):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p] = c * akp - s * akq
                    a[k][q] = s * akp + c * akq
                for k in range(m):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k] = c * apk - s * aqk
                    a[q][k] = s * apk + c * aqk
    return sorted(a[i][i] for i in range(m))


def lambda2(nvert, edges):
    if nvert < 2:
        return None
    d = [0.0] * nvert
    for (u, v, w) in edges:
        d[u] += w
        d[v] += w
    if any(x <= 0 for x in d):
        return 1.0                      # isolated vertex => disconnected
    S = [[0.0] * nvert for _ in range(nvert)]
    for (u, v, w) in edges:
        val = w / math.sqrt(d[u] * d[v])
        S[u][v] += val
        S[v][u] += val
    ev = jacobi_eigs(S)
    return ev[-2]


# --------------------------------------------------------------------------


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    P = all_posets(nmax)
    print("posets up to isomorphism, n = 0..%d: %s   (A000112: 1 1 2 5 16 63 318)"
          % (nmax, " ".join(str(len(P[k])) for k in range(nmax + 1))))
    print()

    per_face_bad = []
    per_level_bad = []
    per_face_tot = 0
    per_level_tot = 0

    for n in range(2, nmax + 1):
        for rel in P[n]:
            facets = maximal_chains(n, rel)
            faces = all_chains(n, rel)
            d = n - 2
            for i in range(-1, d - 1):          # -1 <= i <= d-2
                gam = None
                has_a3 = False
                a3_faces = []
                for sigma in faces.get(i, []):
                    verts, edges = link_weighted_skeleton(n, sigma, facets)
                    lam = lambda2(len(verts), edges)
                    if lam is None:
                        continue
                    if gam is None or lam > gam:
                        gam = lam
                    bl = blocks(n, sigma)
                    if any(induces_antichain(rel, b, 3) for b in bl):
                        has_a3 = True
                        a3_faces.append((sigma, lam, bl))
                for (sigma, lam, bl) in a3_faces:
                    per_face_tot += 1
                    if lam < 0.5 - 1e-9:
                        per_face_bad.append((n, sorted(rel), i, sigma, lam,
                                             [bin(b) for b in bl]))
                if has_a3:
                    per_level_tot += 1
                    if gam is not None and gam < 0.5 - 1e-9:
                        per_level_bad.append((n, sorted(rel), i, gam))
        print("n=%d done" % n)

    print()
    print("=" * 78)
    print("(a) PER-FACE reading -- 'one block induces an antichain of size >= 3")
    print("    therefore lambda_2(link sigma) >= 1/2', which is what §6's")
    print("    sentence argues:")
    print("    faces with such a block: %d" % per_face_tot)
    print("    faces where lambda_2(link) < 1/2: %d   <-- COUNTEREXAMPLES"
          % len(per_face_bad))
    for row in per_face_bad[:8]:
        print("      n=%d rel=%s  i=%d  lambda_2=%.6f  blocks=%s"
              % (row[0], row[1], row[2], row[4], row[5]))
    print()
    print("(b) PER-LEVEL reading -- ledger row G'' as written:")
    print("    (poset, level) pairs having such a face: %d" % per_level_tot)
    print("    of those with gamma_i < 1/2: %d" % len(per_level_bad))
    for row in per_level_bad[:8]:
        print("      n=%d rel=%s  i=%d  gamma=%.6f" % row)
    print("=" * 78)


if __name__ == "__main__":
    main()
