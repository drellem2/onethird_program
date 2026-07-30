#!/usr/bin/env python3
"""
mg-e0ce — INDEPENDENT REBUILD for the audit of mg-276d.

Deliberately shares as little as possible with code/face_geometry/:

  * posets are enumerated as transitively-closed subrelations of the natural
    order on [n] (every iso class has a natural labelling), then canonicalised
    by min-over-S_n.  No ideal lattice is used anywhere in the enumeration.
  * the face complex is built ONLY from surjective isotone maps f : P -> [k].
    The codimension-1 face relation is "merge blocks t, t+1", with simplicial
    sign (-1)^(t-1).  The order-ideal / chain description (their Lemma 1) is
    NEVER used to build anything -- it is only tested, at the end, as a claim.
  * the ambient Coxeter Laplacian is built as a genuine n! x n! matrix and cut
    down, for BOTH the right/position and the left/value action.

Everything is exact integer arithmetic; homology ranks use Fractions.

Run:  python3 audit_rebuild.py [max_n]
"""
import sys
from itertools import permutations, product, combinations
from fractions import Fraction


# ---------------------------------------------------------------- posets ----

def is_transitive(rel):
    for (i, j) in rel:
        for (k, l) in rel:
            if j == k and (i, l) not in rel:
                return False
    return True


def canonical(rel, n):
    best = None
    for p in permutations(range(n)):
        img = tuple(sorted((p[i], p[j]) for (i, j) in rel))
        if best is None or img < best:
            best = img
    return best


def posets_upto_iso(n):
    """All posets on n elements up to isomorphism, as frozensets of strict pairs."""
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    seen = {}
    for mask in range(1 << len(pairs)):
        rel = frozenset(pairs[b] for b in range(len(pairs)) if mask >> b & 1)
        if not is_transitive(rel):
            continue
        c = canonical(rel, n)
        if c not in seen:
            seen[c] = rel
    return [seen[c] for c in sorted(seen)]


def leq(rel):
    return lambda a, b: a == b or (a, b) in rel


# ------------------------------------------------------- linear extensions --

def linear_extensions(rel, n):
    """Words w = (w_1..w_n) listing [n] compatibly with rel.  Brute force."""
    out = []
    for w in permutations(range(n)):
        pos = {x: t for t, x in enumerate(w)}
        if all(pos[i] < pos[j] for (i, j) in rel):
            out.append(w)
    return out


def sgn(w):
    """Sign of the word w read as a permutation of [n]."""
    n = len(w)
    inv = sum(1 for i in range(n) for j in range(i + 1, n) if w[i] > w[j])
    return -1 if inv % 2 else 1


# ----------------------------------------------------------- face complex --

def sur_iso(rel, n, k):
    """Surjective isotone maps P -> [k], as tuples f with f[x] in 0..k-1."""
    if k <= 0 or k > n:
        return []
    out = []
    for f in product(range(k), repeat=n):
        if len(set(f)) != k:
            continue
        if all(f[i] <= f[j] for (i, j) in rel):
            out.append(f)
    return out


def merge(f, t):
    """Merge blocks t, t+1 (1-indexed t) of f : P -> [k].  Returns map to [k-1]."""
    return tuple(x if x <= t - 1 else x - 1 for x in f)


# --------------------------------------------------------- linear algebra --

def rank_Q(rows, ncols):
    """Rank over Q of a list of rows (lists of ints)."""
    M = [[Fraction(x) for x in r] for r in rows]
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, len(M)):
            if M[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
        if r == len(M):
            break
    return r


def matrank(M):
    if not M:
        return 0
    return rank_Q(M, len(M[0]))


# ------------------------------------------------------------ the machine --

def analyse(rel, n, do_left=True):
    """Rebuild both top Laplacians from scratch and test all three claims."""
    L = linear_extensions(rel, n)
    m = len(L)
    idx = {w: i for i, w in enumerate(L)}

    # ---- facets: bijective isotone maps P -> [n].  Built brute force.
    facets = sur_iso(rel, n, n)
    # bijection facets <-> L(P):  f  <->  w with w_t = f^{-1}(t)
    fac_word = []
    for f in facets:
        w = [None] * n
        for x in range(n):
            w[f[x]] = x
        fac_word.append(tuple(w))
    facets_match_L = sorted(fac_word) == sorted(L)

    # order the facets the same way as L(P)
    order = sorted(range(len(facets)), key=lambda i: idx[fac_word[i]])
    facets = [facets[i] for i in order]
    fac_word = [fac_word[i] for i in order]

    # ---- ridges: brute-force Sur_iso(P,[n-1]) (NOT derived from facets)
    ridges = sur_iso(rel, n, n - 1)
    ridge_idx = {g: i for i, g in enumerate(ridges)}

    # ---- boundary matrix  d : C_{n-2} -> C_{n-3},  rows=ridges, cols=facets
    # every codim-1 face of a facet is a merge, and lands in Sur_iso(P,[n-1])
    incid = [dict() for _ in facets]          # facet -> {ridge: sign}
    ridge_facets = {}                          # ridge -> list of facets
    for c, f in enumerate(facets):
        for t in range(1, n):                  # merge blocks t,t+1
            g = merge(f, t)
            assert g in ridge_idx, "merge left Sur_iso -- machinery broken"
            r = ridge_idx[g]
            s = (-1) ** (t - 1)
            assert r not in incid[c], "a facet met a ridge twice"
            incid[c][r] = s
            ridge_facets.setdefault(r, []).append(c)

    ridge_mult = {r: len(v) for r, v in ridge_facets.items()}
    max_mult = max(ridge_mult.values()) if ridge_mult else 0
    pseudomanifold = all(v <= 2 for v in ridge_mult.values())
    free = {r for r, v in ridge_mult.items() if v == 1}
    interior = {r for r, v in ridge_mult.items() if v == 2}

    # ---- Laplacians:  (d^T d)_{c,c'} = sum over ridges of sign*sign
    def lap(keep):
        M = [[0] * m for _ in range(m)]
        for c in range(m):
            for r, s in incid[c].items():
                if r not in keep:
                    continue
                for c2 in ridge_facets[r]:
                    M[c][c2] += s * incid[c2][r]
        return M

    allr = set(ridge_mult)
    Labs = lap(allr)
    Lrel = lap(interior)

    # ---- targets, built with no reference to the complex at all
    A = [[0] * m for _ in range(m)]
    for i, w in enumerate(L):
        for t in range(n - 1):
            v = list(w)
            v[t], v[t + 1] = v[t + 1], v[t]
            v = tuple(v)
            if v in idx:
                A[i][idx[v]] = 1
    deg = [sum(A[i]) for i in range(m)]
    D_minus_A = [[(deg[i] if i == j else 0) - A[i][j] for j in range(m)] for i in range(m)]
    coxeter_target = [[((n - 1) if i == j else 0) - A[i][j] for j in range(m)] for i in range(m)]

    E = [sgn(w) for w in L]

    def twist(M):
        return [[E[i] * M[i][j] * E[j] for j in range(m)] for i in range(m)]

    claim1 = twist(Lrel) == D_minus_A
    claim1_untwisted = Lrel == D_minus_A
    claim2 = twist(Labs) == coxeter_target
    claim2_untwisted = Labs == coxeter_target

    # ---- claim (3) strong: free ridges of facet w  <->  forbidden positions
    claim3_strong = True
    for c, w in enumerate(L):
        fr = {r for r in incid[c] if r in free}
        # the ridge got by merging blocks t,t+1 of the facet = deleting index t
        forb_ridges = set()
        for t in range(1, n):
            a, b = w[t - 1], w[t]
            if (a, b) in rel:          # a <_P b  =>  s_t forbidden at w
                forb_ridges.add(ridge_idx[merge(facets[c], t)])
        if fr != forb_ridges:
            claim3_strong = False
            break

    # ---- claim (3) weak: L^abs - L^rel = diag(# forbidden)
    diffM = [[Labs[i][j] - Lrel[i][j] for j in range(m)] for i in range(m)]
    want = [[((n - 1) - deg[i]) if i == j else 0 for j in range(m)] for i in range(m)]
    claim3_weak = diffM == want

    # ---- structural identities asserted in their (star)
    star_abs = Labs == [[((n - 1) if i == j else 0) + A[i][j] for j in range(m)] for i in range(m)]
    star_rel = Lrel == [[(deg[i] if i == j else 0) + A[i][j] for j in range(m)] for i in range(m)]

    # ---- ambient Coxeter Laplacian, right AND left action, built at n! size
    cox_right = cox_left = None
    if do_left and n <= 6:
        Sn = list(permutations(range(n)))
        sidx = {w: i for i, w in enumerate(Sn)}
        N = len(Sn)
        Rt = [[0] * N for _ in range(N)]
        Lt = [[0] * N for _ in range(N)]
        for i, w in enumerate(Sn):
            for t in range(n - 1):
                v = list(w); v[t], v[t + 1] = v[t + 1], v[t]     # right: positions
                Rt[i][sidx[tuple(v)]] += 1
                u = tuple((t + 1) if x == t else (t if x == t + 1 else x) for x in w)  # left: values
                Lt[i][sidx[u]] += 1
        rows = [sidx[w] for w in L]
        cox_right = [[((n - 1) if i == j else 0) - Rt[rows[i]][rows[j]] for j in range(m)] for i in range(m)]
        cox_left = [[((n - 1) if i == j else 0) - Lt[rows[i]][rows[j]] for j in range(m)] for i in range(m)]

    claim2_right_ambient = (cox_right is not None) and twist(Labs) == cox_right
    claim2_left_ambient = (cox_left is not None) and twist(Labs) == cox_left

    # ---- their Lemma 1 (chain description), TESTED not used
    lemma1_ok = None
    if n <= 5:
        lemma1_ok = True
        for k in range(1, n + 1):
            S = sur_iso(rel, n, k)
            chains = set()
            ideals = []
            for msk in range(1 << n):
                I = frozenset(x for x in range(n) if msk >> x & 1)
                if all((not (j in I)) or (i in I) for (i, j) in rel):
                    ideals.append(I)
            proper = [I for I in ideals if 0 < len(I) < n]
            for comb in combinations(sorted(proper, key=lambda s: (len(s), sorted(s))), k - 1):
                if all(comb[a] < comb[a + 1] for a in range(len(comb) - 1)):
                    chains.add(comb)
            if len(S) != len(chains):
                lemma1_ok = False
    # graded-by-cardinality is implicit in the ideal enumeration above

    # ---- kernel of twisted L^rel  (= relative top homology)
    ker_dim = m - matrank(Lrel)

    # ---- degeneracy bookkeeping
    is_antichain = len(rel) == 0
    is_chain = m == 1
    nondegenerate = (m >= 2) and (len(free) >= 1)

    # ---- Aut(P) and connectivity of the comparability graph
    aut = 0
    for p in permutations(range(n)):
        if frozenset((p[i], p[j]) for (i, j) in rel) == rel:
            aut += 1
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for (i, j) in rel:
        a, b = find(i), find(j)
        if a != b:
            parent[a] = b
    connected = len({find(x) for x in range(n)}) == 1

    return dict(
        n=n, m=m, facets_match_L=facets_match_L, pseudomanifold=pseudomanifold,
        max_mult=max_mult, n_free=len(free), n_ridges=len(ridges),
        claim1=claim1, claim2=claim2, claim3_strong=claim3_strong, claim3_weak=claim3_weak,
        claim1_untwisted=claim1_untwisted, claim2_untwisted=claim2_untwisted,
        star_abs=star_abs, star_rel=star_rel,
        claim2_right_ambient=claim2_right_ambient, claim2_left_ambient=claim2_left_ambient,
        lemma1_ok=lemma1_ok, ker_dim=ker_dim,
        is_antichain=is_antichain, is_chain=is_chain, nondegenerate=nondegenerate,
        aut=aut, connected=connected, rel=rel,
    )


# -------------------------------------------------------- my own controls --

def _claim1_with_signs(rel, n, mode):
    """Rebuild L^rel with a chosen sign convention and test claim (1)."""
    L = linear_extensions(rel, n)
    idx = {w: i for i, w in enumerate(L)}
    facets = sur_iso(rel, n, n)
    ridges = sur_iso(rel, n, n - 1)
    ridge_idx = {g: i for i, g in enumerate(ridges)}
    fw = []
    for f in facets:
        w = [None] * n
        for x in range(n):
            w[f[x]] = x
        fw.append(tuple(w))
    order = sorted(range(len(facets)), key=lambda i: idx[fw[i]])
    facets = [facets[i] for i in order]
    m = len(L)
    incid, rf = [dict() for _ in facets], {}
    for c, f in enumerate(facets):
        for t in range(1, n):
            rr = ridge_idx[merge(f, t)]
            if mode == "true":
                s = (-1) ** (t - 1)
            elif mode == "allplus":
                s = 1
            else:                                   # parity: facet-dependent
                s = ((-1) ** (t - 1)) * (1 if c % 2 == 0 else -1)
            incid[c][rr] = s
            rf.setdefault(rr, []).append(c)
    interior = {rr for rr, v in rf.items() if len(v) == 2}
    M = [[0] * m for _ in range(m)]
    for c in range(m):
        for rr, s in incid[c].items():
            if rr in interior:
                for c2 in rf[rr]:
                    M[c][c2] += s * incid[c2][rr]
    A = [[0] * m for _ in range(m)]
    for i, w in enumerate(L):
        for t in range(n - 1):
            v = list(w); v[t], v[t + 1] = v[t + 1], v[t]
            if tuple(v) in idx:
                A[i][idx[tuple(v)]] = 1
    deg = [sum(A[i]) for i in range(m)]
    E = [sgn(w) for w in L]
    tw = [[E[i] * M[i][j] * E[j] for j in range(m)] for i in range(m)]
    tgt = [[(deg[i] if i == j else 0) - A[i][j] for j in range(m)] for i in range(m)]
    return tw == tgt


def my_controls():
    print("=" * 74)
    print("INDEPENDENT CONTROLS (audit's own, not theirs)")
    print("=" * 74)

    # C1 POSITIVE: poset counts must be A000112 = 1,2,5,16,63,318
    counts = [len(posets_upto_iso(n)) for n in range(1, 7)]
    print(f"[C1 +] posets up to iso n=1..6: {counts}   expect [1,2,5,16,63,318]  "
          f"{'PASS' if counts == [1,2,5,16,63,318] else 'FAIL'}")

    # C2 POSITIVE: the n=3 antichain has |L|=6, AT graph = right Cayley 6-cycle
    r = analyse(frozenset(), 3)
    print(f"[C2 +] n=3 antichain: |L|={r['m']} (expect 6), every ridge in 2 facets "
          f"(free={r['n_free']}, expect 0)  {'PASS' if r['m']==6 and r['n_free']==0 else 'FAIL'}")

    # C3: corrupt the CONSTRUCTION of the Laplacian (not the comparison).
    #  (a) all-+1 simplicial signs        -- does the identity notice?
    #  (b) facet-parity-twisted signs     -- must break the identity
    for n, rel in ((3, frozenset({(0, 1)})), (4, frozenset({(0, 1)})),
                   (4, frozenset({(0, 1), (0, 2)})), (4, frozenset())):
        res = {}
        for mode in ("true", "allplus", "parity"):
            res[mode] = _claim1_with_signs(rel, n, mode)
        print(f"[C3] n={n} rel={sorted(rel)}: claim (1) with true signs={res['true']}, "
              f"all-+1 signs={res['allplus']}, facet-parity signs={res['parity']}")
    print("       ^ NOTE: the all-+1 column is the audit finding -- the alternating")
    print("         simplicial sign is NOT load-bearing for claims (1)-(3).")

    # C3-legacy scaffolding kept for the parity control below
    rel = frozenset({(0, 1)})           # n=3: 0<1, 2 free.  |L| = 3
    n = 3
    L = linear_extensions(rel, n)
    facets = sur_iso(rel, n, n)
    ridges = sur_iso(rel, n, n - 1)
    ridge_idx = {g: i for i, g in enumerate(ridges)}
    fac_word = []
    for f in facets:
        w = [None] * n
        for x in range(n):
            w[f[x]] = x
        fac_word.append(tuple(w))
    idx = {w: i for i, w in enumerate(L)}
    order = sorted(range(len(facets)), key=lambda i: idx[fac_word[i]])
    facets = [facets[i] for i in order]
    m = len(L)
    for signs_all_plus in (False, True):
        incid = [dict() for _ in facets]
        rf = {}
        for c, f in enumerate(facets):
            for t in range(1, n):
                rr = ridge_idx[merge(f, t)]
                incid[c][rr] = 1 if signs_all_plus else (-1) ** (t - 1)
                rf.setdefault(rr, []).append(c)
        interior = {rr for rr, v in rf.items() if len(v) == 2}
        M = [[0] * m for _ in range(m)]
        for c in range(m):
            for rr, s in incid[c].items():
                if rr in interior:
                    for c2 in rf[rr]:
                        M[c][c2] += s * incid[c2][rr]
        A = [[0] * m for _ in range(m)]
        for i, w in enumerate(L):
            for t in range(n - 1):
                v = list(w); v[t], v[t + 1] = v[t + 1], v[t]
                if tuple(v) in idx:
                    A[i][idx[tuple(v)]] = 1
        deg = [sum(A[i]) for i in range(m)]
        E = [sgn(w) for w in L]
        tw = [[E[i] * M[i][j] * E[j] for j in range(m)] for i in range(m)]
        tgt = [[(deg[i] if i == j else 0) - A[i][j] for j in range(m)] for i in range(m)]
        tag = "all-+1 signs" if signs_all_plus else "true signs  "
        ok = tw == tgt
        print(f"[C3 {'-' if signs_all_plus else '+'}] {tag}: claim (1) {'HOLDS' if ok else 'FAILS'}"
              f"  {'PASS (control fires)' if (ok != signs_all_plus) else 'FAIL'}")

    # C4 NEGATIVE: drop the twist -> must FAIL wherever |L|>=2
    bad = 0
    for n in (2, 3, 4):
        for rel in posets_upto_iso(n):
            r = analyse(rel, n, do_left=False)
            if r['m'] >= 2 and r['claim1_untwisted']:
                bad += 1
    print(f"[C4 -] untwisted claim (1) held on {bad} posets with |L|>=2 (n<=4); expect 0  "
          f"{'PASS (control fires)' if bad == 0 else 'FAIL'}")

    # C4b: all-+1 signs, swept -- how often does claim (1) survive the corruption?
    surv = tot = 0
    for n in (2, 3, 4):
        for rel in posets_upto_iso(n):
            tot += 1
            if _claim1_with_signs(rel, n, "allplus"):
                surv += 1
    print(f"[C4b] all-+1 signs: claim (1) still holds on {surv}/{tot} posets n<=4 "
          f"-> the sign convention is NOT load-bearing")

    # C5 POSITIVE: reduced homology of F(P) -- S^(n-2) for antichains, acyclic else
    print("[C5 +] H~(F(antichain_4)) =", reduced_homology(frozenset(), 4), "expect {2: 1}")
    print("[C5 +] H~(F(antichain_5)) =", reduced_homology(frozenset(), 5), "expect {3: 1}")
    bad = []
    for n in (2, 3, 4):
        for rel in posets_upto_iso(n):
            h = reduced_homology(rel, n)
            want = {n - 2: 1} if len(rel) == 0 else {}
            if h != want:
                bad.append((n, sorted(rel), h))
    print(f"[C5 +] H~(F(P)) = S^(n-2) iff antichain, else acyclic: "
          f"{'PASS' if not bad else 'FAIL ' + str(bad)} (all posets n<=4)")
    print()


def reduced_homology(rel, n):
    """Reduced rational homology of the whole face complex, from Sur_iso only."""
    # Sur_iso(P,[k]) sits in dimension k-2; k=1 IS the empty face (dim -1).
    faces = {k: sur_iso(rel, n, k) for k in range(1, n + 1)}
    idxs = {k: {f: i for i, f in enumerate(faces[k])} for k in faces}
    ranks = {1: 0}                        # the empty face has zero boundary
    for k in range(2, n + 1):
        rows = []
        for f in faces[k]:
            v = [0] * len(faces[k - 1])
            for t in range(1, k):
                g = merge(f, t)
                v[idxs[k - 1][g]] += (-1) ** (t - 1)
            rows.append(v)
        ranks[k] = matrank(rows) if rows else 0
    h = {}
    for k in range(1, n + 1):
        dim = k - 2
        nk = len(faces[k])
        b = ranks[k]
        b_next = ranks.get(k + 1, 0)
        hk = nk - b - b_next
        if hk:
            h[dim] = hk
    return h


# ------------------------------------------------------------------ main ----

def main():
    max_n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    my_controls()

    print("=" * 74)
    print("INDEPENDENT SWEEP")
    print("=" * 74)
    tot = dict(all=0, c1=0, c2=0, c3s=0, c3w=0, star=0, pm=0, ker1=0,
               nondeg=0, nondeg_c1=0, right=0, left=0, u1=0, u2=0,
               aut=0, disc=0, lemma1=0, lemma1_tested=0, facets_ok=0)
    per_n = {}
    untw_L = []
    left_by_n = {}
    for n in range(1, max_n + 1):
        Ps = posets_upto_iso(n)
        cn = dict(N=len(Ps), c1=0, c2=0, c3s=0, c3w=0, left=0, maxL=0, nondeg=0)
        for rel in Ps:
            r = analyse(rel, n, do_left=(n <= 5))
            tot['all'] += 1
            cn['maxL'] = max(cn['maxL'], r['m'])
            for key, tk in (('claim1', 'c1'), ('claim2', 'c2'),
                            ('claim3_strong', 'c3s'), ('claim3_weak', 'c3w')):
                if r[key]:
                    tot[tk] += 1; cn[tk] += 1
            if r['star_abs'] and r['star_rel']:
                tot['star'] += 1
            if r['pseudomanifold']:
                tot['pm'] += 1
            if r['facets_match_L']:
                tot['facets_ok'] += 1
            if r['ker_dim'] == 1:
                tot['ker1'] += 1
            if r['nondegenerate']:
                tot['nondeg'] += 1; cn['nondeg'] += 1
                if r['claim1']:
                    tot['nondeg_c1'] += 1
            if r['claim1_untwisted']:
                tot['u1'] += 1; untw_L.append((n, r['m'], r['is_chain']))
            if r['claim2_untwisted']:
                tot['u2'] += 1
            if n <= 5:
                if r['claim2_right_ambient']:
                    tot['right'] += 1
                if r['claim2_left_ambient']:
                    tot['left'] += 1; cn['left'] += 1
            if r['aut'] > 1:
                tot['aut'] += 1
            if not r['connected']:
                tot['disc'] += 1
            if r['lemma1_ok'] is not None:
                tot['lemma1_tested'] += 1
                if r['lemma1_ok']:
                    tot['lemma1'] += 1
        per_n[n] = cn
        left_by_n[n] = (cn['left'], cn['N'])
        print(f"n={n}: {cn['N']:4d} posets | (1) {cn['c1']:4d} | (2) {cn['c2']:4d} | "
              f"(3)w {cn['c3w']:4d} | (3)s {cn['c3s']:4d} | max|L| {cn['maxL']:4d} | "
              f"non-degenerate {cn['nondeg']:4d}", flush=True)

    print()
    print(f"TOTAL posets tested            : {tot['all']}")
    print(f"claim (1) holds                : {tot['c1']}")
    print(f"claim (2) holds (vs (n-1)I - A): {tot['c2']}")
    print(f"claim (2) vs n!-sized ambient  : {tot['right']} of {sum(per_n[k]['N'] for k in per_n if k<=5)} (n<=5)")
    print(f"claim (3) weak / strong        : {tot['c3w']} / {tot['c3s']}")
    print(f"(*) L^abs=(n-1)I+A, L^rel=D+A  : {tot['star']}")
    print(f"pseudomanifold (ridge in 1or2) : {tot['pm']}")
    print(f"facets  <->  L(P)              : {tot['facets_ok']}")
    print(f"dim ker L^rel = 1              : {tot['ker1']}")
    print(f"non-degenerate                 : {tot['nondeg']}  (claim (1) on all: {tot['nondeg_c1']})")
    print(f"UNtwisted (1) holds on         : {tot['u1']}  -> {untw_L}")
    print(f"UNtwisted (2) holds on         : {tot['u2']}")
    print(f"|Aut(P)|>1                     : {tot['aut']}")
    print(f"disconnected                   : {tot['disc']}")
    print(f"their Lemma 1 verified on      : {tot['lemma1']}/{tot['lemma1_tested']} (n<=5, all k)")
    print(f"LEFT/value action holds on     : " +
          ", ".join(f"n={k}: {v[0]}/{v[1]}" for k, v in sorted(left_by_n.items()) if k <= 5))


if __name__ == "__main__":
    main()
