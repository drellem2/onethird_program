#!/usr/bin/env python3
"""mg-5630 INDEPENDENT audit of mg-78c0 / c0cf104.

Everything below is built from scratch (own poset enumeration, own ideal
lattice, own boundary matrix, own Laplacians).  It does NOT import the
deliverable's code or the mg-e0ce audit code -- the point is to check the
NEGATIVE CONTROL 3 numbers and the structural claims about it by a disjoint
route.
"""
from itertools import permutations, combinations
import sys

# ---------------------------------------------------------------- posets
def transitive_closure(n, rel):
    R = set(rel)
    changed = True
    while changed:
        changed = False
        for (a, b) in list(R):
            for (c, d) in list(R):
                if b == c and (a, d) not in R and a != d:
                    R.add((a, d)); changed = True
    return frozenset(R)

def all_posets_raw(n):
    """All strict partial orders on [n] (as frozensets of (a<b) pairs)."""
    pairs = [(a, b) for a in range(n) for b in range(n) if a != b]
    out = set()
    # enumerate by DAG-on-a-linear-order trick: every poset has a linear ext,
    # so wlog a<b in the numbering implies not b<a.  Enumerate subsets of the
    # upper triangle, keep the transitively closed ones, then take closure.
    up = [(a, b) for a in range(n) for b in range(a + 1, n)]
    for mask in range(1 << len(up)):
        rel = frozenset(up[i] for i in range(len(up)) if mask >> i & 1)
        cl = transitive_closure(n, rel)
        if cl == rel:
            out.add(rel)
    return out

def iso_classes(n):
    """One representative per isomorphism class."""
    raw = all_posets_raw(n)
    seen = set(); reps = []
    for rel in sorted(raw, key=lambda r: (len(r), sorted(r))):
        if rel in seen:
            continue
        orb = set()
        for p in permutations(range(n)):
            orb.add(frozenset((p[a], p[b]) for (a, b) in rel))
        # only orbit members that are themselves "upper triangular" are in raw
        seen |= orb
        reps.append(rel)
    return reps

def linear_extensions(n, rel):
    les = []
    for w in permutations(range(n)):
        pos = {v: i for i, v in enumerate(w)}
        if all(pos[a] < pos[b] for (a, b) in rel):
            les.append(w)
    return les

def perm_sign(w):
    s = 1
    w = list(w)
    for i in range(len(w)):
        for j in range(i + 1, len(w)):
            if w[i] > w[j]:
                s = -s
    return s

# ------------------------------------------------- complex + Laplacians
def facet_of(w):
    """Chain of proper non-empty order ideals, as frozensets, in size order."""
    return tuple(frozenset(w[:t]) for t in range(1, len(w)))

def build(n, rel, sign_mode="true", ridge_drop=None, facet_perm=None):
    les = linear_extensions(n, rel)
    facets = [facet_of(w) for w in les]
    if facet_perm is not None:
        facets = [facets[facet_perm(i, len(facets))] for i in range(len(facets))]
    ridges = set()
    for f in facets:
        for i in range(len(f)):
            ridges.add(f[:i] + f[i + 1:])
    ridges = sorted(ridges, key=lambda r: sorted(sorted(x) for x in r))
    if ridge_drop is not None and len(ridges) > ridge_drop:
        del ridges[ridge_drop]          # deliberate construction corruption
    ridx = {r: i for i, r in enumerate(ridges)}
    nr, nc = len(ridges), len(facets)
    # boundary matrix
    d = [[0] * nc for _ in range(nr)]
    for j, f in enumerate(facets):
        if sign_mode == "parity":
            col = 1 if j % 2 == 0 else -1
        else:
            col = 1
        for i in range(len(f)):
            g = f[:i] + f[i + 1:]
            if g not in ridx:
                continue
            s = 1 if sign_mode == "allplus" else (-1) ** i * col
            d[ridx[g]][j] += s
    occ = [sum(1 for j in range(nc) if d[r][j] != 0) for r in range(nr)]
    interior = [r for r in range(nr) if occ[r] == 2]
    def dtd(rows):
        L = [[0] * nc for _ in range(nc)]
        for r in rows:
            for a in range(nc):
                if d[r][a] == 0: continue
                for b in range(nc):
                    if d[r][b] == 0: continue
                    L[a][b] += d[r][a] * d[r][b]
        return L
    return {"les": les, "facets": facets, "d": d, "nr": nr, "nc": nc,
            "L_abs": dtd(range(nr)), "L_rel": dtd(interior)}

def at_target(n, rel, les):
    idx = {w: i for i, w in enumerate(les)}
    m = len(les)
    A = [[0] * m for _ in range(m)]
    for w in les:
        for t in range(n - 1):
            v = list(w); v[t], v[t + 1] = v[t + 1], v[t]; v = tuple(v)
            if v in idx:
                A[idx[w]][idx[v]] = 1
    return [[(sum(A[i]) if i == j else 0) - A[i][j] for j in range(m)] for i in range(m)]

def twist(L, les, extra=None):
    s = [perm_sign(w) for w in les]
    if extra is not None:
        s = [s[i] * extra(i) for i in range(len(s))]
    return [[s[i] * L[i][j] * s[j] for j in range(len(les))] for i in range(len(les))]

def claim1(n, rel, sign_mode="true", extra_twist=None, **kw):
    B = build(n, rel, sign_mode=sign_mode, **kw)
    lhs = twist(B["L_rel"], B["les"], extra_twist)
    return lhs == at_target(n, rel, B["les"]), B

# ---------------------------------------------------------------- checks
def pop(nmax):
    out = []
    for n in range(2, nmax + 1):
        for rel in iso_classes(n):
            out.append((n, rel))
    return out

def main():
    P5 = pop(5)
    print("population: %d iso classes for 2<=n<=5 (expect 86 = 2+5+16+63)" % len(P5))
    per = {}
    for n, rel in P5: per[n] = per.get(n, 0) + 1
    print("  per n:", per)

    bites = [(n, r) for (n, r) in P5 if len(linear_extensions(n, r)) >= 2]
    print("  |L(P)|>=2 on %d of %d  (expect 82)" % (len(bites), len(P5)))

    # --- A. NC3 line 1: true signs pass
    ok = sum(1 for n, r in P5 if claim1(n, r)[0])
    print("A  true signs: claim (1) holds on %d/%d   [doc says 86/86]" % (ok, len(P5)))

    # --- B. NC3 line 2: allplus.  Check BOTH Laplacians, untwisted.
    same_rel = same_abs = same_lhs = 0
    for n, r in P5:
        Bt = build(n, r, "true"); Bp = build(n, r, "allplus")
        same_rel += (Bt["L_rel"] == Bp["L_rel"])
        same_abs += (Bt["L_abs"] == Bp["L_abs"])
        same_lhs += (twist(Bt["L_rel"], Bt["les"]) == twist(Bp["L_rel"], Bp["les"]))
    print("B  allplus: L_rel unchanged %d/%d ; L_abs unchanged %d/%d ; twisted LHS %d/%d"
          % (same_rel, len(P5), same_abs, len(P5), same_lhs, len(P5)))
    okp = sum(1 for n, r in P5 if claim1(n, r, "allplus")[0])
    print("   allplus: claim (1) still holds on %d/%d   [doc: 86/86]" % (okp, len(P5)))
    # WHY: is the true boundary matrix = D_row * allplus matrix?
    factors = 0
    for n, r in P5:
        Bt = build(n, r, "true"); Bp = build(n, r, "allplus")
        good = True
        for i in range(Bt["nr"]):
            sgn = None
            for j in range(Bt["nc"]):
                if Bp["d"][i][j] == 0: continue
                q = Bt["d"][i][j] * Bp["d"][i][j]
                if sgn is None: sgn = q
                elif sgn != q: good = False
        factors += good
    print("   TRUE boundary = diag(row signs) * ALLPLUS boundary on %d/%d posets"
          % (factors, len(P5)))

    # --- C. NC3 line 3: facet-parity
    par_app, par_rej = 0, 0
    conj_ok = 0
    for n, r in bites:
        Bt = build(n, r, "true"); Bq = build(n, r, "parity")
        Lt = twist(Bt["L_rel"], Bt["les"]); Lq = twist(Bq["L_rel"], Bq["les"])
        if Lt != Lq:
            par_app += 1
            if Lq != at_target(n, r, Bt["les"]): par_rej += 1
        # is parity exactly diagonal conjugation of L_rel by diag((-1)^j)?
        m = Bt["nc"]
        D = [1 if j % 2 == 0 else -1 for j in range(m)]
        conj = [[D[i] * Bt["L_rel"][i][j] * D[j] for j in range(m)] for i in range(m)]
        conj_ok += (conj == Bq["L_rel"])
    print("C  facet-parity: bites on %d/%d of the |L|>=2 posets, rejected on %d"
          "   [doc: rejected 82/82, bites on all 82]" % (par_app, len(bites), par_rej))
    print("   parity L_rel == diag((-1)^j) . true L_rel . diag((-1)^j) on %d/%d"
          % (conj_ok, len(bites)))

    # --- D. IS THE PARITY CORRUPTION ABSORBABLE INTO THE TWIST?
    absorb = 0
    for n, r in P5:
        ok2, _ = claim1(n, r, "parity", extra_twist=lambda i: 1 if i % 2 == 0 else -1)
        absorb += ok2
    print("D  parity + twist E.D  => claim (1) holds again on %d/%d posets"
          "   (if 86: the corruption is a re-orientation absorbable into E,"
          " i.e. the same class as M1/M3)" % (absorb, len(P5)))

    # --- E. spectra preserved?
    print("E  parity preserves the spectrum of L_rel by construction (conjugation"
          " by an involution) -- see C.")

    # --- F. POSITIVE CONTROL ON THE CONTROL: corrupt the CONSTRUCTION in a
    #        way that is NOT a sign convention, and see what NC3's three lines say.
    for name, kw in [("drop ridge #0 from the complex", dict(ridge_drop=0)),
                     ("swap facets 0 and 1 (mis-indexed facet enumeration)",
                      dict(facet_perm=lambda i, m: (1 if i == 0 else 0 if i == 1 else i) if m >= 2 else i))]:
        l1 = sum(1 for n, r in P5 if claim1(n, r, "true", **kw)[0])
        # line 2: allplus leaves L_rel unchanged?
        s2 = 0
        for n, r in P5:
            Bt = build(n, r, "true", **kw); Bp = build(n, r, "allplus", **kw)
            s2 += (twist(Bt["L_rel"], Bt["les"]) == twist(Bp["L_rel"], Bp["les"]))
        # line 3: parity rejected where it bites?
        app = rej = 0
        for n, r in bites:
            Bt = build(n, r, "true", **kw); Bq = build(n, r, "parity", **kw)
            Lt = twist(Bt["L_rel"], Bt["les"]); Lq = twist(Bq["L_rel"], Bq["les"])
            if Lt != Lq:
                app += 1
                if Lq != at_target(n, r, Bt["les"]): rej += 1
        print("F  CORRUPTED PIPELINE (%s):" % name)
        print("     NC3 line1 true-signs pass  : %d/%d  %s"
              % (l1, len(P5), "FIRES (line 1 catches it)" if l1 != len(P5) else "SILENT"))
        print("     NC3 line2 allplus-unchanged: %d/%d  %s"
              % (s2, len(P5), "FIRES" if s2 != len(P5) else "SILENT"))
        print("     NC3 line3 parity-rejected  : %d of %d biting  %s"
              % (rej, app, "SILENT (still rejects)" if rej == app and app == len(bites)
                 else "FIRES (bite-count or rejection changed)"))

    # --- G. Corollary B' recomputed from scratch, n=2..8
    print("G  Corollary B' -- left/value vs right/position on the ANTICHAIN:")
    for n in range(2, 9):
        Sn = list(permutations(range(n)))
        w0 = tuple([1, 0] + list(range(2, n)))     # s_1 (0-indexed positions 0,1)
        R, Lf = set(), set()
        for t in range(n - 1):
            v = list(w0); v[t], v[t + 1] = v[t + 1], v[t]; R.add(tuple(v))
            Lf.add(tuple((t + 1) if x == t else (t if x == t + 1 else x) for x in w0))
        diff_at_s1 = (R != Lf)
        anyw = any((lambda w: (set(tuple(v) for v in [ (lambda l: (l.__setitem__(t, w[t+1]), l.__setitem__(t+1, w[t]), l)[2])(list(w)) for t in range(n-1)]) !=
                               set(tuple((t+1) if x==t else (t if x==t+1 else x) for x in w) for t in range(n-1))))(w)
                    for w in Sn)
        # the specific witness s_1 s_2 (right) not left
        s1s2 = None
        if n >= 3:
            v = list(w0); v[1], v[2] = v[2], v[1]; s1s2 = tuple(v)
        print("     n=%d: neighbourhoods differ at w=s_1? %-3s ; some w differs? %-3s ; "
              "s_1s_2=%s in R\\L? %s"
              % (n, "YES" if diff_at_s1 else "NO", "YES" if anyw else "NO",
                 s1s2, (s1s2 in R and s1s2 not in Lf) if s1s2 else "-"))

    # --- H. left-reading claim (2) on the antichain, full matrix check n=3,4,5
    print("H  claim (2) LEFT reading on the antichain (full matrix test):")
    for n in range(2, 7):
        rel = frozenset()
        B = build(n, rel, "true")
        les = B["les"]; idx = {w: i for i, w in enumerate(les)}; m = len(les)
        lhs = twist(B["L_abs"], les)
        for side in ("right", "left"):
            A = [[0] * m for _ in range(m)]
            for w in les:
                for t in range(n - 1):
                    if side == "right":
                        v = list(w); v[t], v[t + 1] = v[t + 1], v[t]; v = tuple(v)
                    else:
                        v = tuple((t + 1) if x == t else (t if x == t + 1 else x) for x in w)
                    if v in idx: A[idx[w]][idx[v]] = 1
            tgt = [[((n - 1) if i == j else 0) - A[i][j] for j in range(m)] for i in range(m)]
            print("     n=%d %-5s : claim (2) %s" % (n, side, "HOLDS" if lhs == tgt else "FAILS"))

if __name__ == "__main__":
    main()
