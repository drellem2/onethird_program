"""kc.py (audit mg-f4f0): K_C of mg-785e Thm 5.1, implemented from the doc text (no imported code).
For (P, L), L dominance-respecting: pattern
  (i)   L-consecutive incomparable step with |S| <= 1;
  (ii)  Thm 3.1 triple (consecutive) with k <= 2, a Thm 2.1* pair, or a Thm 3.1* triple;
  (iii) L-consecutive strict-containment step with |S| = 2.
K_C says every dominance-respecting L of a non-chain interval order has (i), (ii) or (iii).
(a) the 22 staircase survivors of mg-561a (parsed from its out_lpsurv.txt, data only): check L is a
    dominance-respecting linear extension, has no (i)/(ii), and has (iii);
(b) a bounded counterexample SEARCH for K_C on random interval orders (probe, not a census)."""
import sys, os, ast, random, time
from eng import *

def dominates(iv, x, y): return iv[x] != iv[y] and iv[x][0] <= iv[y][0] and iv[x][1] <= iv[y][1]

class K:
    def __init__(self, iv):
        self.iv = iv; self.n = len(iv); self.R = rel_from_iv(iv); self.C = covers_rel(self.R)
        self.S = {}
        for x in range(self.n):
            for y in range(self.n):
                if inc(iv, x, y): self.S[x, y] = seps_rel(self.R, self.C, x, y)
    def k31(self, a, c, b):
        Aac, Bac = self.S[a, c]; Abc, _ = self.S[b, c]; Bcb, Acb_ = self.S[c, b][1], self.S[c, b][0]; Bca = self.S[c, a][1]
        return ([z for z in Aac if z not in Abc], list(Bac), [w for w in Bcb if w not in Bca], list(Acb_))
    def pat(self, L):
        iv = self.iv; n = self.n; pos = {v: i for i, v in enumerate(L)}; out = set()
        for i in range(n - 1):
            a, b = L[i], L[i + 1]
            if not inc(iv, a, b): continue
            A, B = self.S[a, b]
            if len(A) + len(B) <= 1: out.add('i')
            (la, ra), (lb, rb) = iv[a], iv[b]
            if ((lb < la and ra < rb) or (la < lb and rb < ra)) and len(A) + len(B) == 2: out.add('iii')
        for a in range(n):          # 2.1*
            for b in range(n):
                if inc(iv, a, b) and pos[a] < pos[b]:
                    A, B = self.S[a, b]
                    if len(A) + len(B) <= 1 and all(pos[z] > pos[b] for z in A) and all(pos[w] < pos[a] for w in B): out.add('2.1*')
        for i in range(n):          # 3.1 / 3.1*
            for j in range(i + 1, n):
                for l in range(j + 1, n):
                    a, c, b = L[i], L[j], L[l]
                    if not (inc(iv, a, c) and inc(iv, c, b)): continue
                    z1, w1, w2, z2 = self.k31(a, c, b)
                    k = len(z1) + len(w1) + len(w2) + len(z2)
                    if k > 2: continue
                    if l == i + 2 and j == i + 1: out.add('3.1')
                    if all(pos[z] > pos[c] for z in z1) and all(pos[w] < pos[a] for w in w1) and \
                       all(pos[w] < pos[c] for w in w2) and all(pos[z] > pos[b] for z in z2): out.add('3.1*')
        return out
    def is_domresp_ext(self, L):
        pos = {v: i for i, v in enumerate(L)}
        ok_ext = all(pos[x] < pos[y] for x in range(self.n) for y in range(self.n) if self.R[x][y])
        ok_dom = all(pos[x] < pos[y] for x in range(self.n) for y in range(self.n) if dominates(self.iv, x, y))
        return ok_ext and ok_dom

def survivors():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ksbft_t2_two_separator_561a', 'out_lpsurv.txt')
    lines = open(p).read().splitlines(); out = []
    for i, ln in enumerate(lines):
        if ln.startswith('P='):
            P = ast.literal_eval(ln[2:]); Lt = ast.literal_eval(lines[i + 1].strip()[2:]); out.append((P, Lt))
    return out

def Lidx(iv, Lt):
    used = set(); L = []
    for t in Lt:
        i = next(j for j in range(len(iv)) if iv[j] == t and j not in used); used.add(i); L.append(i)
    return L

def search_bad(iv, cap_nodes=200000, use_iii=True):
    """DFS over dominance-respecting linear extensions, pruning any prefix that shows (i), (iii) or a
    consecutive Thm 3.1 triple with k<=2; complete L's are then tested for 2.1*/3.1*. Returns (#local-bad L, #K_C-bad L, example)."""
    k = K(iv); n = k.n; dn = downmask_rel(k.R)
    dommask = [sum(1 << y for y in range(n) if dominates(iv, y, x)) for x in range(n)]   # must precede x
    nodes = [0]; loc = []; seq = []
    def stepbad(a, b):
        if not inc(iv, a, b): return False
        A, B = k.S[a, b]; s = len(A) + len(B)
        if s <= 1: return True
        (la, ra), (lb, rb) = iv[a], iv[b]
        return use_iii and ((lb < la and ra < rb) or (la < lb and rb < ra)) and s == 2
    def rec(I):
        nodes[0] += 1
        if nodes[0] > cap_nodes: return
        if len(seq) == n: loc.append(tuple(seq)); return
        for v in range(n):
            if I >> v & 1 or dn[v] & ~I or dommask[v] & ~I: continue
            if seq and stepbad(seq[-1], v): continue
            if len(seq) >= 2:
                a, c = seq[-2], seq[-1]
                if inc(iv, a, c) and inc(iv, c, v) and sum(map(len, k.k31(a, c, v))) <= 2: continue
            seq.append(v); rec(I | 1 << v); seq.pop()
    rec(0)
    bad = [L for L in loc if not (k.pat(list(L)) & {'2.1*', '3.1*'})]
    return len(loc), bad, nodes[0] > cap_nodes

if __name__ == '__main__':
    S = survivors(); print(f'(a) survivors parsed: {len(S)}')
    tally = {}
    for P, Lt in S:
        k = K(P); L = Lidx(P, Lt); pt = k.pat(L)
        assert k.is_domresp_ext(L), P
        assert canonical(P) == sorted(P), ("survivor not canonical", P)
        key = tuple(sorted(pt)); tally[key] = tally.get(key, 0) + 1
    print('    patterns found per survivor (all are dominance-respecting linear extensions):', tally)
    # positive control: with (iii) NOT forbidden, the search must find Q12's staircase L; with it forbidden, nothing.
    Q12 = [(1,1),(1,2),(2,3),(2,5),(3,4),(4,5),(5,6),(5,8),(6,7),(7,8),(8,9),(9,9)]
    LQ = Lidx(Q12, [(1,1),(1,2),(2,3),(3,4),(2,5),(4,5),(5,6),(5,8),(6,7),(7,8),(8,9),(9,9)])
    nl, bad, tr = search_bad(Q12, use_iii=False)
    print(f'    control Q12 without (iii): K_C-bad L found = {len(bad)}, staircase L among them: {tuple(LQ) in bad} -> ' + ('FIRES' if tuple(LQ) in bad else 'DOES NOT FIRE'))
    nl, bad, tr = search_bad(Q12); print(f'    Q12 with (iii): K_C-bad L = {len(bad)} (truncated: {tr})')
    if len(sys.argv) > 1:
        rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 7); T = float(sys.argv[1]); t0 = time.time()
        tried = locbad = kcbad = trunc = 0; ex = []; tried_by_n = {}; seen = set()
        while time.time() - t0 < T:
            n = rng.randint(11, 14)
            # staircase backbone + random long intervals + random extra units (the shape of every known obstruction)
            m = rng.randint(n - 5, n - 2); iv = [(i, i + 1) for i in range(1, m)] + [(1, 1), (m, m)]
            while len(iv) < n:
                l = rng.randint(1, m); r = min(m, l + rng.choice([0, 1, 2, 3, 4, 5])); iv.append((l, r))
            iv = canonical(iv)   # containment/dominance are read off the CANONICAL representation
            key = tuple(iv)
            if key in seen: continue
            seen.add(key); n = len(iv)
            if all(not inc(iv, x, y) for x in range(n) for y in range(n)): continue
            if len(seen) % 2000 == 0: print('   progress', len(seen), locbad, kcbad, flush=True)
            nl, bad, tr = search_bad(iv)
            tried += 1; tried_by_n[n] = tried_by_n.get(n, 0) + 1; locbad += nl; kcbad += len(bad); trunc += tr
            if bad: ex.append((iv, bad[0]))
        print(f'(b) K_C counterexample search, {T:.0f}s: {tried} DISTINCT (canonical) random staircase-type interval orders n=11..14 {dict(sorted(tried_by_n.items()))}; '
              f'L avoiding (i),(iii),local 3.1: {locbad}; of those also avoiding 2.1*/3.1* (K_C-bad): {kcbad}; truncated DFS: {trunc}')
        for iv, L in ex[:5]: print('    K_C-BAD:', iv, 'L =', [iv[x] for x in L])
