"""certs_indep.py (audit mg-f4f0): INDEPENDENT exact re-check of the 14 pointwise certificates of
code/ksbft_t3_lemma_c_785e/certs.json (only the JSON data is read; no code imported from that branch).
Rows are rebuilt here from the definitions (Swap Identity, Thm 1.1 of mg-561a; Conditioned Swap Identity,
Prop 1.1 of mg-785e) with this engine's own covers, separators and extension list. Soundness does not depend
on the row labelling: every row built here is checked to sum to 0 over all extensions, and Prop 1.2 needs
nothing else. Also checks the section-3.2 certificate from the PROSE of the doc, and 4 controls."""
import json, sys, os
from fractions import Fraction as F
from itertools import combinations
from eng import *

HERE = os.path.dirname(os.path.abspath(__file__))
CJ = os.path.join(HERE, '..', 'ksbft_t3_lemma_c_785e', 'certs.json')

class Rows:
    def __init__(self, iv):
        self.iv = [tuple(t) for t in iv]; self.n = len(iv)
        self.R = rel_from_iv(self.iv); self.C = covers_rel(self.R)
        self.E = extensions(self.R); self.pos = [{v: i for i, v in enumerate(s)} for s in self.E]
        self.rows = []; self.labels = []
    def lam1(self, a, b):
        A, B = seps_rel(self.R, self.C, a, b); S = A + B
        return [k for k, p in enumerate(self.pos) if p[a] < p[b] and not any(p[a] < p[z] < p[b] for z in S)]
    def S0(self):
        for u in range(self.n):
            for v in range(u + 1, self.n):
                if inc(self.iv, u, v):
                    r = {}
                    for k in self.lam1(u, v): r[k] = r.get(k, 0) + 1
                    for k in self.lam1(v, u): r[k] = r.get(k, 0) - 1
                    self.rows.append(r); self.labels.append(('S0', u, v))
    def SW(self, a, b, W):
        g = {}
        key = lambda k: tuple(sorted(W, key=lambda w: self.pos[k][w]))
        for k in self.lam1(a, b): g.setdefault(key(k), {}); g[key(k)][k] = g[key(k)].get(k, 0) + 1
        for k in self.lam1(b, a): g.setdefault(key(k), {}); g[key(k)][k] = g[key(k)].get(k, 0) - 1
        for kk, r in g.items(): self.rows.append(r); self.labels.append(('SW', a, b, tuple(W), kk))

def build(iv, L, fam):
    m = Rows(iv); m.S0(); n = m.n
    if fam == 'S0+SW2st':
        for k in range(n - 1):
            p = (L[k], L[k + 1])
            if inc(m.iv, *p):
                for W in combinations([w for w in range(n) if w not in p], 2): m.SW(p[0], p[1], list(W))
    elif fam == 'S0+SW2all':
        for u in range(n):
            for v in range(u + 1, n):
                if inc(m.iv, u, v):
                    for W in combinations([w for w in range(n) if w not in (u, v)], 2): m.SW(u, v, list(W))
    return m

def Lidx(iv, Lt):
    used = set(); L = []
    for t in Lt:
        i = next(j for j in range(len(iv)) if tuple(iv[j]) == tuple(t) and j not in used); used.add(i); L.append(i)
    return L

def evalG(m, L, lam, y):
    pos = {v: i for i, v in enumerate(L)}
    for (u, v) in lam:   # charged pairs must be L-ordered incomparable pairs u before v
        assert inc(m.iv, u, v) and pos[u] < pos[v], ('charged pair not an L-ordered incomparable pair', u, v)
    for j in y: assert sum(m.rows[j].values()) == 0, 'row with nonzero sum'
    G = [F(0)] * len(m.E)
    for (u, v), x in lam.items():
        assert x >= 0
        for k, p in enumerate(m.pos):
            if p[v] < p[u]: G[k] += x
    for j, x in y.items():
        for k, c in m.rows[j].items(): G[k] += x * c
    g = min(G); tot = sum(lam.values())
    return g, tot

if __name__ == '__main__':
    C = json.load(open(CJ)); bad = 0; cache = {}
    for c in C:
        L = Lidx(c['P'], c['L']); key = (str(c['P']), c['family'])
        m = cache.get(key) or build(c['P'], L, c['family']); cache[key] = m
        lam = {tuple(map(int, k.split(','))): F(v) for k, v in c['lam'].items()}
        y = {int(k): F(v) for k, v in c['y'].items()}
        g, tot = evalG(m, L, lam, y)
        ok = g > 0 and tot < 3 * g
        bad += not ok
        print(f"{'VALID' if ok else 'INVALID'} {c['family']:10s} win={c['window']} e={len(m.E):6d} rows={len(m.rows):5d} "
              f"used={len(y):3d} charged={len(lam)} ratio={float(tot/g) if g>0 else None:.6f} P={c['P']}", flush=True)
        if c['family'] != 'S0':
            nsw = sum(1 for j in y if m.labels[j][0] == 'SW'); print(f"      conditioned rows used: {nsw}")
    # --- the section 3.2 certificate from the doc prose ---
    iv = [(1,1),(1,2),(1,6),(2,3),(2,8),(3,4),(4,5),(5,6),(5,9),(6,7),(7,8),(8,9),(9,9)]
    Lt = [(1,1),(1,2),(2,3),(3,4),(1,6),(2,8),(4,5),(5,6),(6,7),(5,9),(7,8),(8,9),(9,9)]
    L = Lidx(iv, Lt); m = Rows(iv); ix = {t: i for i, t in enumerate(iv)}
    c = ix[(2,8)]
    lam = {(ix[(2,8)], ix[(4,5)]): F(3,2), (ix[(3,4)], ix[(2,8)]): F(5,4)}
    ds = [(1,2),(2,3),(3,4),(4,5),(6,7),(8,9)]; ws = [F(-1,4), F(-1,2), F(-1,2), F(1), F(1,2), F(1,2)]
    best = None
    from itertools import product
    for signs in product([1, -1], repeat=6):
        m.rows = []; y = {}
        for j, (d, w, sg) in enumerate(zip(ds, ws, signs)):
            r = {}
            for k in m.lam1(c, ix[d]): r[k] = r.get(k, 0) + 1
            for k in m.lam1(ix[d], c): r[k] = r.get(k, 0) - 1
            m.rows.append(r); y[j] = w * sg
        g, tot = evalG(m, L, lam, y)
        if best is None or g > best[0]: best = (g, tot, signs)
        if signs == (1,)*6: g0 = g
    print(f"sec 3.2 prose certificate: e={len(m.E)}; with rows oriented (c,d): min G = {g0}; best over the 64 orientations: "
          f"min G = {best[0]} at signs {best[1+1]}, sum lambda = {best[1]}; valid(ratio<3): {best[0]>0 and best[1]<3*best[0]}")
    # --- controls ---
    c0 = C[1]; L = Lidx(c0['P'], c0['L']); m = cache[(str(c0['P']), c0['family'])]   # Q12, tight (2.983)
    lam = {tuple(map(int, k.split(','))): F(v) for k, v in c0['lam'].items()}; y = {int(k): F(v) for k, v in c0['y'].items()}
    g, t = evalG(m, L, {k: v * F(9, 10) for k, v in lam.items()}, y); print('control Q12 lambda x 9/10:', 'CAUGHT' if not (g > 0 and t < 3*g) else 'NOT CAUGHT')
    jmax = max(y, key=lambda j: abs(y[j])); y2 = dict(y); y2[jmax] = -y2[jmax]
    g, t = evalG(m, L, lam, y2); print('control Q12 largest row weight sign-flipped:', 'CAUGHT' if not (g > 0 and t < 3*g) else 'NOT CAUGHT')
    Lw = list(L); Lw[3], Lw[4] = Lw[4], Lw[3]      # wrong L: containment step reversed -> charged pairs no longer L-ordered
    try:
        evalG(m, Lw, lam, y); print('control wrong L: NOT CAUGHT')
    except AssertionError: print('control wrong L (charged pair not L-ordered): CAUGHT')
    g, t = evalG(m, L, lam, {}); print('control no rows:', 'CAUGHT' if not (g > 0 and t < 3*g) else 'NOT CAUGHT')
    # a row with only above-separators (not an identity): sum must be nonzero somewhere
    fake = 0
    for u in range(m.n):
        for v in range(m.n):
            if inc(m.iv, u, v):
                A, B = seps_rel(m.R, m.C, u, v); A2, B2 = seps_rel(m.R, m.C, v, u)
                s1 = sum(1 for p in m.pos if p[u] < p[v] and not any(p[u] < p[z] < p[v] for z in A))
                s2 = sum(1 for p in m.pos if p[v] < p[u] and not any(p[v] < p[z] < p[u] for z in A2))
                fake += s1 != s2
    print('control A-only rows nonzero sum on', fake, 'ordered pairs:', 'CAUGHT' if fake else 'NOT CAUGHT')
    # a conditioned row on a NON-invariant event (position of a itself) must fail
    a, b = L[3], L[4]; failures = 0
    for kpos in range(m.n):
        s1 = sum(1 for k in m.lam1(a, b) if m.pos[k][a] == kpos); s2 = sum(1 for k in m.lam1(b, a) if m.pos[k][b] == kpos)
        s3 = sum(1 for k in m.lam1(b, a) if m.pos[k][a] == kpos)
        failures += s1 != s3
    print('control F = {pos(a)=k} (not tau-invariant): identity fails for', failures, 'values of k:', 'CAUGHT' if failures else 'NOT CAUGHT')
    print(f'certificates: {len(C)-bad} valid, {bad} invalid')
