"""prop11.py (audit mg-f4f0): tests of Prop 1.1 (Conditioned Swap Identity) of mg-785e.
(1) exhaustive enumeration: random general posets and random interval orders, n = 5..9, random a || a',
    several tau-invariant events F (order of 2 or 3 others; position of a third element = k; a mixed event);
(2) automaton DP on random interval orders n = 12..20 (no enumeration): F = {w1 before w2}.
Controls (must fail): F = {position of a = k} (not tau-invariant), and above-separators only."""
import random, sys
from itertools import combinations
from eng import *

def rand_poset(n, p, rng):
    R = [[False]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if rng.random() < p: R[i][j] = True
    for k in range(n):
        for i in range(n):
            if R[i][k]:
                for j in range(n):
                    if R[k][j]: R[i][j] = True
    perm = list(range(n)); rng.shuffle(perm)
    return [[R[perm[i]][perm[j]] for j in range(n)] for i in range(n)]

def lam1_set(E, pos, S, a, b):
    return [k for k, p in enumerate(pos) if p[a] < p[b] and not any(p[a] < p[z] < p[b] for z in S)]

def enum_test(rng, trials):
    viol = 0; checks = 0; ctl_pos = 0; ctl_A = 0
    for t in range(trials):
        n = rng.randint(5, 9)
        if t % 2: iv = rand_io(n, n, 3, rng); R = rel_from_iv(iv)
        else: R = rand_poset(n, rng.choice([0.2, 0.3, 0.45]), rng)
        C = covers_rel(R); E = extensions(R); pos = [{v: i for i, v in enumerate(s)} for s in E]
        incp = [(x, y) for x in range(n) for y in range(x+1, n) if not R[x][y] and not R[y][x]]
        if not incp or n < 5: continue
        for (a, b) in rng.sample(incp, min(3, len(incp))):
            A, B = seps_rel(R, C, a, b); A2, B2 = seps_rel(R, C, b, a)
            l1 = lam1_set(E, pos, A + B, a, b); l3 = lam1_set(E, pos, A2 + B2, b, a)
            others = [w for w in range(n) if w not in (a, b)]
            events = []
            W2 = rng.sample(others, 2); W3 = rng.sample(others, 3); w = rng.choice(others)
            events.append(lambda k, W=W2: tuple(sorted(W, key=lambda x: pos[k][x])))
            events.append(lambda k, W=W3: tuple(sorted(W, key=lambda x: pos[k][x])))
            events.append(lambda k, w=w: pos[k][w])
            events.append(lambda k, W=W2, w=w: (pos[k][W[0]] < pos[k][W[1]], pos[k][w] <= n // 2))
            for ev in events:
                c1 = {}; c3 = {}
                for k in l1: c1[ev(k)] = c1.get(ev(k), 0) + 1
                for k in l3: c3[ev(k)] = c3.get(ev(k), 0) + 1
                checks += 1; viol += c1 != c3
            # controls
            c1 = {}; c3 = {}
            for k in l1: c1[pos[k][a]] = c1.get(pos[k][a], 0) + 1
            for k in l3: c3[pos[k][a]] = c3.get(pos[k][a], 0) + 1
            ctl_pos += c1 != c3
            ctl_A += len(lam1_set(E, pos, A, a, b)) != len(lam1_set(E, pos, A2, b, a))
    return checks, viol, ctl_pos, ctl_A

def dp_test(rng, trials):
    viol = 0; checks = 0; ctl = 0; maxn = 0
    for t in range(trials):
        n = rng.randint(12, 20); iv = rand_io(n, n + 2, rng.randint(1, 4), rng); R = rel_from_iv(iv); C = covers_rel(R)
        incp = [(x, y) for x in range(n) for y in range(x+1, n) if inc(iv, x, y)]
        if not incp: continue
        a, b = rng.choice(incp); others = [w for w in range(n) if w not in (a, b)]; w1, w2 = rng.sample(others, 2)
        Sab = set(sum(seps_rel(R, C, a, b), [])); Sba = set(sum(seps_rel(R, C, b, a), []))
        Aab = set(seps_rel(R, C, a, b)[0]); Aba = set(seps_rel(R, C, b, a)[0])
        def mk(Sa, Sb):
            # state: (first in {None,'a','b'}, broken, done, wfirst)
            def step(s, v):
                first, brk, done, wf = s
                if v in (w1, w2) and wf is None: wf = v
                if v == a or v == b:
                    if first is None: return (('a' if v == a else 'b'), False, False, wf)
                    return (first, brk, True, wf)
                if first is not None and not done:
                    if (first == 'a' and v in Sa) or (first == 'b' and v in Sb): brk = True
                return (first, brk, done, wf)
            return step
        out = auto_count(R, (None, False, False, None), mk(Sab, Sba))
        for wf in (w1, w2):
            x = sum(c for s, c in out.items() if s[0] == 'a' and not s[1] and s[3] == wf)
            y = sum(c for s, c in out.items() if s[0] == 'b' and not s[1] and s[3] == wf)
            checks += 1; viol += x != y
        out2 = auto_count(R, (None, False, False, None), mk(Aab, Aba))
        x = sum(c for s, c in out2.items() if s[0] == 'a' and not s[1]); y = sum(c for s, c in out2.items() if s[0] == 'b' and not s[1])
        ctl += x != y; maxn = max(maxn, n)
    return checks, viol, ctl, maxn

if __name__ == '__main__':
    rng = random.Random(4040)
    c, v, cp, ca = enum_test(rng, int(sys.argv[1]) if len(sys.argv) > 1 else 300)
    print(f'enumeration (n=5..9, general + interval): {c} (pair, F) checks, {v} violations; '
          f'control F=pos(a): fires on {cp} pairs; control A-only separators: fires on {ca} pairs')
    c, v, ct, mx = dp_test(rng, int(sys.argv[2]) if len(sys.argv) > 2 else 200)
    print(f'automaton DP (random interval orders n=12..{mx}): {c} (pair, w-order) checks, {v} violations; control A-only: fires on {ct}')
