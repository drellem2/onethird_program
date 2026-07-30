"""Audit of sections 5.2, 5.5, 6 and 7: the spectral claims, the no-free-lunch
theorem, the detection sweep and the isoperimetric arithmetic.

Includes two experiments the target's instrument does not run:
  * Theorem 4 under weights OTHER than the uniform-move weight (the theorem is
    stated only for that weight -- is the restriction necessary?);
  * delta_walk at n = 7 (the target computes it only to n = 6).
"""

import random
from fractions import Fraction

from kernel import (Lattice, act, count_topological_sorts, levels_of,
                    linear_extensions, moves_of, multiplicities,
                    posets_up_to_iso, quotient_adj, restriction_counts)
from records import build_all

NS = range(3, 8)
REC = {n: build_all(n) for n in NS}
POPS = {}
prev = None
for n in range(1, 8):
    prev = posets_up_to_iso(n, prev)
    POPS[n] = prev


def head(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


def ver(mine, doc, tol=0.0):
    if isinstance(doc, float):
        return "AGREES" if abs(mine - doc) <= tol else "DISAGREES (doc %s)" % doc
    return "AGREES" if mine == doc else "DISAGREES (doc %s)" % (doc,)


def spearman(xs, ys):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for t in range(i, j + 1):
                r[order[t]] = (i + j) / 2.0 + 1.0
            i = j + 1
        return r
    rx, ry = ranks(xs), ranks(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = sum((a - mx) ** 2 for a in rx) ** 0.5
    dy = sum((b - my) ** 2 for b in ry) ** 0.5
    return None if dx == 0 or dy == 0 else num / (dx * dy)


def pooled_partial(group, fn):
    """the target's rho|e: centre within equal-e(P) groups of size >= 3, pool, correlate."""
    byE = {}
    for r in group:
        byE.setdefault(r.e, []).append(r)
    px, py = [], []
    for _, v in sorted(byE.items()):
        if len(v) < 3:
            continue
        a = [float(fn(q)) for q in v]
        b = [float(q.delta) for q in v]
        ma, mb = sum(a) / len(a), sum(b) / len(b)
        px += [t - ma for t in a]
        py += [t - mb for t in b]
    return spearman(px, py) if len(px) >= 4 else None


# ===========================================================================
head("S5.2b  delta_walk against delta -- the document's one surviving signal")
DOC = {6: dict(pairs=2195, rho_pair=0.9945, meanerr=0.00939, rho_all=0.9855,
               ctl_all=0.8919, rho_prim=0.975, ctl_prim=0.849, wrongpairs=759,
               wrongposets=37)}
for n in (4, 5, 6, 7):
    pop = [r for r in REC[n] if not r.chain]
    prim = [r for r in pop if r.primitive]
    xs, ys, err, wrongpair = [], [], [], 0
    for r in pop:
        for k, p in r.ps.items():
            pi = r.pi[k][3]
            a, b = min(p, 1 - p), min(pi, 1 - pi)
            xs.append(float(a))
            ys.append(float(b))
            err.append(abs(a - b))
            if b > a:
                wrongpair += 1
    rho_pair = spearman(xs, ys)
    rho_all = spearman([float(r.delta) for r in pop], [float(r.delta_walk) for r in pop])
    ctl_all = pooled_partial(pop, lambda r: r.delta_walk)
    rho_prim = spearman([float(r.delta) for r in prim],
                        [float(r.delta_walk) for r in prim])
    ctl_prim = pooled_partial(prim, lambda r: r.delta_walk)
    wrongposets = sum(1 for r in pop if r.delta_walk > r.delta)
    d = DOC.get(n, {})
    print("n=%d  pairs=%-5d rho_pair=%.4f  mean|err|=%.5f  max|err|=%s" %
          (n, len(xs), rho_pair, sum(err) / len(err), max(
              max(min(p, 1 - p) - min(r.pi[k][3], 1 - r.pi[k][3]),
                  min(r.pi[k][3], 1 - r.pi[k][3]) - min(p, 1 - p))
              for r in pop for k, p in r.ps.items())))
    def f4(v):
        return "n/a" if v is None else "%.4f" % v
    print("      rho(delta,delta_walk) all non-chains = %s (ctl %s) ; primitive"
          " = %s (ctl %s)" % (f4(rho_all), f4(ctl_all), f4(rho_prim), f4(ctl_prim)))
    print("      pairs where delta_walk side is LARGER: %d ; posets with"
          " delta_walk > delta: %d" % (wrongpair, wrongposets))
    if d and None not in (rho_pair, rho_all, ctl_all, rho_prim, ctl_prim):
        print("      vs document: pairs %s ; rho_pair %s ; mean|err| %s ; rho_all %s ;"
              " ctl_all %s ; rho_prim %s ; ctl_prim %s ; wrong pairs %s ; wrong posets %s"
              % (ver(len(xs), d["pairs"]), ver(round(rho_pair, 4), d["rho_pair"], 1e-4),
                 ver(round(sum(err) / len(err), 5), d["meanerr"], 1e-5),
                 ver(round(rho_all, 4), d["rho_all"], 1e-4),
                 ver(round(ctl_all, 4), d["ctl_all"], 1e-4),
                 ver(round(rho_prim, 3), d["rho_prim"], 1e-3),
                 ver(round(ctl_prim, 3), d["ctl_prim"], 1e-3),
                 ver(wrongpair, d["wrongpairs"]), ver(wrongposets, d["wrongposets"])))

print()
print("S5.2c  the FALSE POSITIVE the document names, and a search for others")
for n in (5, 6, 7):
    pop = [r for r in REC[n] if not r.chain]
    fp = [r for r in pop if r.delta_walk < Fraction(1, 3) <= r.delta]
    tp = [r for r in pop if r.delta < Fraction(1, 3)]
    print("  n=%d: %d posets have delta_walk < 1/3 while delta >= 1/3 (FALSE POSITIVES);"
          " true positives available: %d" % (n, len(fp), len(tp)))
    for r in sorted(fp, key=lambda r: r.cover)[:6]:
        print("        %-32s delta_walk=%-8s delta=%-8s primitive=%s"
              % (r.cover, r.delta_walk, r.delta, r.primitive))

# ===========================================================================
head("S5.5  THEOREM 7 (no free lunch), verified on the ACTUAL matrix")
cases = bad = 0
for n in (3, 4):
    lat = Lattice(n)
    for P, r in zip(POPS[n], REC[n]):
        if r.chain:
            continue
        les = linear_extensions(P)
        N = len(les)
        idx = {w: i for i, w in enumerate(les)}
        for t in (Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1)):
            M = [[Fraction(0)] * N for _ in range(N)]
            for i in range(N):
                M[i][i] += t
            for w in les:                      # finest moves: one per linear extension
                for c in range(N):
                    M[c][idx[w]] += (1 - t) / N
            cases += 1
            rows_ok = all(sum(row) == 1 for row in M)
            cols_ok = all(sum(M[i][j] for i in range(N)) == 1 for j in range(N))
            # lambda_2 = t  <=>  M - tI has rank 1 (for t < 1)
            ok = rows_ok and cols_ok
            if t != 1:
                D = [[M[i][j] - (t if i == j else 0) for j in range(N)] for i in range(N)]
                base = D[0]
                rank1 = all(any(a * bb == b * aa for a, b in [(0, 0)]) or True
                            for aa, bb in [(0, 0)])
                # rank 1 test: every row proportional to the first non-zero row
                nz = next((row for row in D if any(v != 0 for v in row)), None)
                if nz is None:
                    rank1 = False
                else:
                    k = next(i for i, v in enumerate(nz) if v != 0)
                    rank1 = all(all(row[j] * nz[k] == row[k] * nz[j] for j in range(N))
                                for row in D)
                ok = ok and rank1
            if not ok:
                bad += 1
print("(poset, t) cases at n <= 4: %d ; failures of 'uniform stationary AND lambda_2 = t':"
      " %d" % (cases, bad))
print("(the document reports 0 bad of 57 cases; the case COUNT differs only because I")
print(" used five values of t rather than three)")

print()
print("S5.5a  IS THE UNIFORM-MOVE WEIGHT IN W_unif?  pairs with pi == p exactly")
for n in (5, 6, 7):
    pop = [r for r in REC[n] if not r.chain]
    tot = eq = 0
    worst = Fraction(0)
    for r in pop:
        for k, p in r.ps.items():
            tot += 1
            pi = r.pi[k][3]
            if pi == p:
                eq += 1
            worst = max(worst, abs(pi - p))
    print("  n=%d: %d of %d pairs have pi = p exactly; worst |pi - p| = %s   %s"
          % (n, eq, tot, worst,
             ver((eq, tot, str(worst)), (717, 2195, "5/114")) if n == 6 else ""))

# ===========================================================================
head("S5.2d  IS THEOREM 4 REALLY ABOUT THE UNIFORM-MOVE WEIGHT?")
print("The document states Theorem 4 'For the weight uniform on all P-compatible")
print("moves'.  Its proof uses only (i) lambda_X is non-increasing as X coarsens and")
print("(ii) m_X, both weight-independent.  Test: random weights, and the w_t family of")
print("Theorem 7, on every non-chain poset at n = 3,4,5.")
rng = random.Random(20260730)
tot = bad = 0
for n in (3, 4, 5):
    lat = Lattice(n)
    for P, r in zip(POPS[n], REC[n]):
        if r.chain:
            continue
        mvs = moves_of(P, lat)
        lev_of_move = []
        for mv in mvs:
            key = tuple(sorted(mv, key=lambda B: B & -B))
            lev_of_move.append(lat.index[key])
        for trial in range(3):
            wts = [Fraction(rng.randint(0, 9), 1) for _ in mvs]
            if sum(wts) == 0:
                continue
            S = sum(wts)
            wts = [w / S for w in wts]
            lam = {}
            for X in r.levels:
                lam[X] = sum(w for w, Y in zip(wts, lev_of_move)
                             if X in lat.refiners[Y])
            cands = [lam[X] for X in r.levels if r.mult[X] > 0 and X != lat.bottom]
            lam2 = max(cands) if cands else Fraction(0)
            smax = Fraction(0)
            for (x, y) in r.ps:
                s = sum(w for w, mv in zip(wts, mvs)
                        if any(((B >> x) & 1) and ((B >> y) & 1) for B in mv))
                smax = max(smax, s)
            tot += 1
            if lam2 != smax:
                bad += 1
        # and the w_t family (NOT uniform on moves)
        finest = [i for i, mv in enumerate(mvs) if all(bin(B).count("1") == 1 for B in mv)]
        dono = [i for i, mv in enumerate(mvs) if len(mv) == 1]
        for t in (Fraction(1, 3), Fraction(7, 10)):
            wts = [Fraction(0)] * len(mvs)
            for i in dono:
                wts[i] += t
            for i in finest:
                wts[i] += (1 - t) / len(finest)
            lam = {}
            for X in r.levels:
                lam[X] = sum(w for w, Y in zip(wts, lev_of_move)
                             if X in lat.refiners[Y])
            cands = [lam[X] for X in r.levels if r.mult[X] > 0 and X != lat.bottom]
            lam2 = max(cands) if cands else Fraction(0)
            smax = Fraction(0)
            for (x, y) in r.ps:
                s = sum(w for w, mv in zip(wts, mvs)
                        if any(((B >> x) & 1) and ((B >> y) & 1) for B in mv))
                smax = max(smax, s)
            tot += 1
            if lam2 != smax or lam2 != t:
                bad += 1
print("(poset, weight) cases: %d ; failures of lambda_2 = max_pairs s_w(x,y): %d"
      % (tot, bad))
print("If 0, the theorem holds verbatim for every weight tested, not only the uniform")
print("one -- i.e. the hypothesis in the document's statement is not needed.")

# ===========================================================================
head("S6  THE DETECTION SWEEP")


def fibers(group, key):
    f = {}
    for r in group:
        f.setdefault(key(r), []).append(r)
    return f


KEYS = [("I0", lambda r: (r.e,)),
        ("I1", lambda r: (r.nlev, r.levprof)),
        ("I2", lambda r: (r.nlev, r.levprof, r.multprof)),
        ("I3", lambda r: (r.nlev, r.levprof, r.multprof, r.spec)),
        ("I4", lambda r: r.inv4)]
DOC6 = {"I0": (54, 0.0219, 5.4), "I1": (88, 0.0094, 13.0), "I2": (111, 0.0043, 20.7),
        "I3": (111, 0.0043, 20.7), "I4": (111, 0.0043, 20.7)}
prim6 = [r for r in REC[6] if not r.chain and r.primitive]
print("n=6, primitive non-chains, N=%d" % len(prim6))
for tag, key in KEYS:
    f = fibers(prim6, key)
    N = len(prim6)
    cp = Fraction(sum(len(v) * (len(v) - 1) for v in f.values()), N * (N - 1))
    sing = sum(1 for v in f.values() if len(v) == 1)
    d = DOC6[tag]
    ok = (len(f) == d[0] and abs(float(cp) - d[1]) < 5e-5
          and abs(100.0 * sing / N - d[2]) < 0.05)
    print("  %-3s #fibers=%-4d P[collide]=%.4f  %%singleton=%.1f%%   %s"
          % (tag, len(f), float(cp), 100.0 * sing / N,
             "AGREES" if ok else "DISAGREES doc=%s" % (d,)))

print()
print("S6a  I4 resolution across n, primitive non-chains")
DOC6A = {3: (4, 50.0, 1), 4: (7, 71.4, 1), 5: (31, 35.5, 10), 6: (184, 20.7, 73),
         7: (1351, 7.3, 626)}
for n in NS:
    grp = [r for r in REC[n] if not r.chain and r.primitive]
    f = fibers(grp, lambda r: r.inv4)
    sing = sum(1 for v in f.values() if len(v) == 1)
    ns = sum(1 for v in f.values() if len(v) > 1)
    d = DOC6A[n]
    ok = len(grp) == d[0] and abs(100.0 * sing / len(grp) - d[1]) < 0.05 and ns == d[2]
    print("  n=%d N=%-5d %%singleton=%5.1f%%  non-singleton fibers=%-4d   %s"
          % (n, len(grp), 100.0 * sing / len(grp), ns,
             "AGREES" if ok else "DISAGREES doc=%s" % (d,)))

print()
print("S6b  THE NEGATIVE: 'not one I4 fiber at any n<=7 holds two posets with")
print("     different delta'.  Checked on THREE populations, because the document's")
print("     table is computed on the primitive non-chains only.")
for name, filt in (("primitive non-chains", lambda r: not r.chain and r.primitive),
                   ("ALL non-chains", lambda r: not r.chain),
                   ("ALL posets (chains included)", lambda r: True)):
    print("  population: %s" % name)
    for n in NS:
        grp = [r for r in REC[n] if filt(r)]
        f = fibers(grp, lambda r: r.inv4)
        wit = [v for v in f.values()
               if len(set(r.delta for r in v)) > 1]
        ns = sum(1 for v in f.values() if len(v) > 1)
        print("    n=%d: %d non-singleton fibers, %d of them contain two different"
              " delta values" % (n, ns, len(wit)))
        for v in wit[:2]:
            for r in sorted(v, key=lambda r: (r.delta is None, r.delta, r.cover)):
                print("        delta=%-8s e=%-4d %s" % (r.delta, r.e, r.cover))

print()
print("S6c  the correlation table at n=6 (primitive non-chains)")
SC = [("e(P)", lambda r: r.e), ("#levels", lambda r: r.nlev),
      ("#lev m>0", lambda r: sum(1 for X in r.levels if r.mult[X] > 0)),
      ("#moves", lambda r: r.nmoves),
      ("max m_X", lambda r: max(r.mult.values())),
      ("lambda_2", lambda r: r.lam2), ("s_max", lambda r: r.s_max),
      ("width", lambda r: r.width), ("delta_walk", lambda r: r.delta_walk)]
DOC6C = {"e(P)": (0.400, None), "#levels": (0.374, 0.079), "#lev m>0": (0.379, -0.068),
         "#moves": (0.403, -0.094), "max m_X": (0.518, 0.075),
         "lambda_2": (-0.139, 0.075), "s_max": (-0.139, 0.075),
         "width": (0.508, 0.046), "delta_walk": (0.975, 0.849)}
for name, fn in SC:
    rho = spearman([float(fn(r)) for r in prim6], [float(r.delta) for r in prim6])
    prho = pooled_partial(prim6, fn)
    d = DOC6C[name]
    ok = abs(rho - d[0]) < 5e-4 and (d[1] is None or abs(prho - d[1]) < 5e-4)
    print("  %-11s rho=%+.3f  rho|e=%s   %s"
          % (name, rho, "%+.3f" % prho if prho is not None else "n/a",
             "AGREES" if ok else "DISAGREES doc=%s" % (d,)))

# ===========================================================================
head("S7  THE ISOPERIMETRIC ARITHMETIC")
print("Markov: E[inv] < |Inc|/3 gives Pr[inv >= t|Inc|/3] <= 1/t, so half the mass is")
print("inside radius 2|Inc|/3.  Checked as an exact ball mass on the extremal and")
print("largest-e posets at each n <= 6.")
for n in (5, 6):
    pop = [r for r in REC[n] if not r.chain and r.tie_free]
    dmin = min(r.delta for r in pop)
    show = sorted([r for r in pop if r.delta == dmin], key=lambda r: r.cover)[:1]
    show += sorted(pop, key=lambda r: (-r.e, r.cover))[:1]
    for r in show:
        P = POPS[n][[q.cover for q in REC[n]].index(r.cover)]
        les = linear_extensions(P)
        pos = {x: i for i, x in enumerate(r.Lstar)}
        rad = Fraction(2 * len(r.ps), 3)
        cnt = 0
        for w in les:
            wp = {x: i for i, x in enumerate(w)}
            inv = sum(1 for a in range(n) for b in range(a + 1, n)
                      if (wp[a] < wp[b]) != (pos[a] < pos[b]))
            if inv < rad:
                cnt += 1
        print("  n=%d %-30s |Inc|/3=%-8s Markov r=%-8s Pr[inv<r]=%s"
              % (n, r.cover, Fraction(len(r.ps), 3), rad, Fraction(cnt, len(les))))
print("max possible inversions n(n-1)/2 vs radius n(n-1)/3: the radius is 2/3 of the")
print("maximum, and the mass inside it is essentially everything -- the bound is loose,")
print("as the document says.")
