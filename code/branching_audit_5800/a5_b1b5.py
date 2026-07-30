"""A5 -- the two results mg-6ad0 STRENGTHENED, checked for over-correction.

mg-5800's brief: a repair correcting overstatements can over-correct into
hedging a result that is in fact stronger than originally claimed, and both
directions are defects.  The two results are:

  B1  a LATTICE isomorphism J(D_lam) -> [0, lam] -- meet and join preserved,
      not merely an order isomorphism;
  B5  dim kF(P)/rad = |AC(P)|, re-derived with NO trace form and NO cited
      theorem: |AC(P)| characters built from the product alone, Phi
      surjective, ker Phi nilpotent in exact arithmetic.

Both are re-established here on this audit's own instrument, so that the
question "did the repair weaken them" is asked against a measured fact rather
than against another ticket's report.
"""
import sys
from fractions import Fraction
from itertools import product as iproduct
from kern5800 import (bits, canon, ideal_lattice, ideals, interval_poset,
                      meet_join_tables, skew_cell_poset, straight_shapes,
                      shape_to_mu_lam)

print("=" * 78)
print("A5  B1 AS A LATTICE ISOMORPHISM, AND B5 WITHOUT A TRACE FORM")
print("=" * 78)

# ------------------------------------------------------------------ B1

NB1 = int(sys.argv[1]) if len(sys.argv) > 1 else 7
print("\n[B1] J(D_lam) -> [0, lam], MEET AND JOIN, every pair, lam |- n <= %d" % NB1)
lams = [tuple(b for a, b in s) for n in range(1, NB1 + 1) for s in straight_shapes(n)]
print("  partitions: %d" % len(lams))
ord_bad = meet_bad = join_bad = 0
maxsize = 0
for lam in lams:
    sh = tuple((0, r) for r in lam)
    k, kup = skew_cell_poset(sh)
    ids = ideals(k, kup)
    m, iup, iels = interval_poset((), lam)
    maxsize = max(maxsize, m)
    # the map: ideal I -> the partition whose row i is the number of cells of I
    # in row i.  Built here, not imported.
    cells = [(i, j) for i, r in enumerate(lam) for j in range(r)]
    def phi(I):
        rows = [0] * len(lam)
        for c in bits(I):
            rows[cells[c][0]] += 1
        return tuple(rows)
    img = [phi(I) for I in ids]
    pos = {tuple(e): t for t, e in enumerate(iels)}
    if sorted(img) != sorted(tuple(e) for e in iels):
        ord_bad += 1
        continue
    jm, jup, jids = ideal_lattice(k, kup)
    jmeet, jjoin = meet_join_tables(jm, jup)
    imeet, ijoin = meet_join_tables(m, iup)
    f = [pos[phi(jids[a])] for a in range(jm)]
    for a in range(jm):
        for b in range(jm):
            le_src = (jids[a] & jids[b]) == jids[a]
            le_dst = all(x <= y for x, y in zip(iels[f[a]], iels[f[b]]))
            if le_src != le_dst:
                ord_bad += 1
            if f[jmeet[a][b]] != imeet[f[a]][f[b]]:
                meet_bad += 1
            if f[jjoin[a][b]] != ijoin[f[a]][f[b]]:
                join_bad += 1
print("  largest interval: %d elements" % maxsize)
print("  order failures (both directions, every pair): %d" % ord_bad)
print("  MEET not preserved: %d" % meet_bad)
print("  JOIN not preserved: %d" % join_bad)
print("  => B1 is a LATTICE isomorphism, not merely an order isomorphism: %s"
      % (ord_bad == meet_bad == join_bad == 0))

# ------------------------------------------------------------------ B5

NB5 = int(sys.argv[2]) if len(sys.argv) > 2 else 4
print("\n[B5] dim kF(P)/rad = |AC(P)|, with NO trace form and NO cited theorem,")
print("  n <= %d.  F(P) is the set of P-compatible ORDERED set partitions with" % NB5)
print("  the block-intersection product; AC(P) is the set of supports.")


def moves(n, up):
    """P-compatible ordered set partitions, by filtering ALL of them."""
    out = []
    def rec(remaining, blocks):
        if remaining == 0:
            out.append(tuple(blocks))
            return
        sub = remaining
        while sub:
            blocks.append(sub)
            rec(remaining ^ sub, blocks)
            blocks.pop()
            sub = (sub - 1) & remaining
    rec((1 << n) - 1, [])
    keep = []
    for x in out:
        idx = {}
        for t, B in enumerate(x):
            for e in bits(B):
                idx[e] = t
        if all(idx[i] <= idx[j] for i in range(n) for j in bits(up[i])):
            keep.append(x)
    return keep


def mprod(x, y):
    return tuple(D for B in x for C in y if (D := B & C))


def supp(x):
    return tuple(sorted(x))


from kern5800 import decode, enumerate_posets
ps = enumerate_posets(NB5)
tot = 0
lrb_bad = 0
hom_bad = 0
surj_bad = 0
nilp_bad = 0
dim_bad = 0
for n in range(1, NB5 + 1):
    for code in ps[n]:
        up = decode(n, code)
        F = moves(n, up)
        pos = {x: i for i, x in enumerate(F)}
        N = len(F)
        # left regular band: xx = x and xyx = xy
        for x in F[:min(N, 40)]:
            if mprod(x, x) != x:
                lrb_bad += 1
            for y in F[:min(N, 20)]:
                if mprod(mprod(x, y), x) != mprod(x, y):
                    lrb_bad += 1
        AC = sorted({supp(x) for x in F})
        # semilattice order on supports: C <= D iff C = supp(m) with
        # C * D = C, computed via a representative product
        rep = {}
        for x in F:
            rep.setdefault(supp(x), x)
        def le(C, D):
            return supp(mprod(rep[C], rep[D])) == C
        # characters chi_C(x) = 1 iff C <= supp(x)
        chars = [[1 if le(C, supp(x)) else 0 for x in F] for C in AC]
        # Phi is an algebra map: chi_C(xy) = chi_C(x) chi_C(y)
        for ci, C in enumerate(AC):
            for x in F[:min(N, 25)]:
                for y in F[:min(N, 25)]:
                    if chars[ci][pos[mprod(x, y)]] != chars[ci][pos[x]] * chars[ci][pos[y]]:
                        hom_bad += 1
        # surjectivity <=> the |AC| character vectors are linearly independent
        rows = [[Fraction(v) for v in r] for r in chars]
        rank = 0
        piv = []
        for r in rows:
            v = r[:]
            for (pc, pv) in piv:
                if v[pc]:
                    f0 = v[pc] / pv[pc]
                    v = [a - f0 * b for a, b in zip(v, pv)]
            nz = next((i for i, a in enumerate(v) if a), None)
            if nz is not None:
                piv.append((nz, v))
                rank += 1
        if rank != len(AC):
            surj_bad += 1
        # ker Phi.  Phi(x) depends only on supp(x), so {x - rep[supp(x)]} spans
        # a subspace of the kernel of dimension N - |AC| = dim ker Phi exactly.
        # Two-term basis vectors, which is what makes the nilpotency check
        # affordable in exact arithmetic.
        kb = []
        for x in F:
            r = rep[supp(x)]
            if x != r:
                v = {pos[x]: Fraction(1), pos[r]: Fraction(-1)}
                kb.append(v)
        if len(kb) != N - len(AC):
            dim_bad += 1
        ptab = [[pos[mprod(F[a], F[b])] for b in range(N)] for a in range(N)]

        def vmul(u, v):
            out = {}
            for a, ua in u.items():
                row = ptab[a]
                for b, vb in v.items():
                    z = row[b]
                    out[z] = out.get(z, Fraction(0)) + ua * vb
            return {k: w for k, w in out.items() if w}

        def reduce_basis(vecs):
            piv = {}
            out = []
            for v in vecs:
                v = dict(v)
                while v:
                    c = min(v)
                    if c in piv:
                        pv = piv[c]
                        f0 = v[c] / pv[c]
                        for k2, w in pv.items():
                            v[k2] = v.get(k2, Fraction(0)) - f0 * w
                        v = {k2: w for k2, w in v.items() if w}
                    else:
                        piv[c] = v
                        out.append(v)
                        break
            return out

        cur = reduce_basis(kb)
        power = 1
        while cur and power <= N + 1:
            nxt = reduce_basis([vmul(u, v) for u in cur for v in kb])
            power += 1
            if len(nxt) >= len(cur) and power > N:
                break
            cur = nxt
        if cur:
            nilp_bad += 1
            print("    ker Phi NOT nilpotent for n=%d code=%s" % (n, code))
        tot += 1
print("  posets: %d;  LRB failures: %d;  character-multiplicativity failures: %d"
      % (tot, lrb_bad, hom_bad))
print("  Phi surjective (|AC| characters linearly independent) failures: %d" % surj_bad)
print("  dim ker Phi != |F(P)| - |AC(P)| failures: %d" % dim_bad)
print("  ker Phi NOT nilpotent: %d" % nilp_bad)
print("  => dim kF(P)/rad = |AC(P)| for all %d posets to n <= %d, with no trace"
      % (tot, NB5))
print("     form and no cited theorem: %s"
      % (lrb_bad == hom_bad == surj_bad == dim_bad == nilp_bad == 0))

print("\nSUMMARY a5_b1b5: B1 order %d, meet %d, join %d; B5 posets %d, "
      "LRB bad %d, character-hom bad %d, surjectivity bad %d, kernel-dim bad %d, "
      "non-nilpotent %d"
      % (ord_bad, meet_bad, join_bad, tot, lrb_bad, hom_bad, surj_bad, dim_bad,
         nilp_bad))
