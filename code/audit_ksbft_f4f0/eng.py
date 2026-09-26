"""eng.py (audit mg-f4f0): independent engine for the audit of mg-785e (KSBFT-T3).
No code imported from the audited branches. Interval orders: x < y iff r(x) < l(y).
Separators from covers, as in mg-561a's definitions:
  A(a,a') = {z : a <. z, z || a'},  B(a,a') = {w : w <. a', w || a}.
Lambda_1(a,a') = a before a' with no element of A u B strictly between."""
from fractions import Fraction as F
from itertools import combinations
import random

def lt(iv, x, y): return iv[x][1] < iv[y][0]
def inc(iv, x, y): return x != y and not lt(iv, x, y) and not lt(iv, y, x)

def rel_from_iv(iv):
    n = len(iv); return [[lt(iv, x, y) for y in range(n)] for x in range(n)]

def covers_rel(R):
    n = len(R)
    return [[R[x][y] and not any(R[x][z] and R[z][y] for z in range(n)) for y in range(n)] for x in range(n)]

def seps_rel(R, C, a, b):
    n = len(R)
    incp = lambda x, y: x != y and not R[x][y] and not R[y][x]
    A = [z for z in range(n) if C[a][z] and incp(z, b)]
    B = [w for w in range(n) if C[w][b] and incp(w, a)]
    return A, B

def downmask_rel(R):
    n = len(R); return [sum(1 << y for y in range(n) if R[y][x]) for x in range(n)]

def extensions(R):
    """all linear extensions, lexicographic DFS order (v in increasing index)."""
    n = len(R); dn = downmask_rel(R); out = []; seq = []
    def rec(I):
        if len(seq) == n: out.append(tuple(seq)); return
        for v in range(n):
            if not I >> v & 1 and dn[v] & ~I == 0:
                seq.append(v); rec(I | 1 << v); seq.pop()
    rec(0); return out

def ideals_dp(R):
    """forward/backward counts over the ideal lattice. returns (f, b, e)."""
    n = len(R); dn = downmask_rel(R); full = (1 << n) - 1
    f = {0: 1}; layer = [0]; order = [0]
    for _ in range(n):
        nxt = {}
        for I in layer:
            for v in range(n):
                if not I >> v & 1 and dn[v] & ~I == 0:
                    J = I | 1 << v
                    if J not in f: f[J] = 0; nxt[J] = 1
                    f[J] += f[I]
        layer = list(nxt); order += layer
    b = {full: 1}
    for I in reversed(order):
        if I == full: continue
        s = 0
        for v in range(n):
            if not I >> v & 1 and dn[v] & ~I == 0: s += b[I | 1 << v]
        b[I] = s
    return f, b, f[full], dn

def pair_counts(R):
    """cnt[x][y] = #extensions with x before y; exact ints. e = total."""
    n = len(R); f, b, e, dn = ideals_dp(R)
    cnt = [[0] * n for _ in range(n)]
    for I, fi in f.items():
        for x in range(n):
            if not I >> x & 1 and dn[x] & ~I == 0:
                J = I | 1 << x; w = fi * b[J]; row = cnt[x]
                rest = ~J
                for y in range(n):
                    if rest >> y & 1: row[y] += w
    return cnt, e

def auto_count(R, init, step, accept=None):
    """count extensions by final automaton state: DP over (ideal, state)."""
    n = len(R); dn = downmask_rel(R); full = (1 << n) - 1
    cur = {(0, init): 1}
    for _ in range(n):
        nxt = {}
        for (I, s), c in cur.items():
            for v in range(n):
                if not I >> v & 1 and dn[v] & ~I == 0:
                    t = step(s, v)
                    if t is None: continue
                    k = (I | 1 << v, t); nxt[k] = nxt.get(k, 0) + c
        cur = nxt
    out = {}
    for (I, s), c in cur.items(): out[s] = out.get(s, 0) + c
    return out

# ---------- canonical interval orders = Fishburn matrices ----------
def fishburn(n):
    """all canonical interval representations of size n: upper-triangular m x m nonneg integer
    matrices, total n, no zero row, no zero column. Yields sorted interval lists."""
    for m in range(1, n + 1):
        cells = [(i, j) for i in range(1, m + 1) for j in range(i, m + 1)]
        # fill cells in order; prune: rows/cols needing a nonzero later
        k = len(cells)
        # last index of each row / col among cells
        lastrow = {}; lastcol = {}
        for idx, (i, j) in enumerate(cells): lastrow[i] = idx; lastcol[j] = idx
        vals = [0] * k
        def rec(idx, rem, rowok, colok):
            if idx == k:
                if rem == 0 and all(rowok.values()) and all(colok.values()):
                    iv = []
                    for (c, v) in zip(cells, vals): iv += [c] * v
                    yield iv
                return
            i, j = cells[idx]
            need = sum(1 for r, ok in rowok.items() if not ok) + 0
            lo = 0
            if lastrow[i] == idx and not rowok[i]: lo = 1
            if lastcol[j] == idx and not colok[j]: lo = 1
            for v in range(lo, rem + 1):
                vals[idx] = v
                ro = rowok[i]; co = colok[j]
                if v: rowok[i] = True; colok[j] = True
                # feasibility: remaining units must cover still-missing rows (weak bound)
                miss = sum(1 for ok in rowok.values() if not ok)
                if rem - v >= 0 and (rem - v) >= (miss if idx + 1 < k else 0):
                    yield from rec(idx + 1, rem - v, rowok, colok)
                rowok[i] = ro; colok[j] = co
            vals[idx] = 0
        yield from rec(0, n, {i: False for i in range(1, m + 1)}, {j: False for j in range(1, m + 1)})

FISH = [1, 1, 2, 5, 15, 53, 217, 1014, 5335, 31240, 201608]

def cont_twosep(iv, R=None, C=None):
    """strict containment pairs a inside a2 (l(a2)<l(a)<=r(a)<r(a2)), a first; S(a,a2) of size 2.
    yields (a, a2, s, t) with (A,B) typed."""
    R = R or rel_from_iv(iv); C = C or covers_rel(R); n = len(iv)
    for a in range(n):
        for a2 in range(n):
            (la, ra), (lb, rb) = iv[a], iv[a2]
            if not (lb < la and ra < rb): continue
            A, B = seps_rel(R, C, a, a2)
            if B: raise AssertionError('containment with a below-separator')
            if len(A) == 2: yield a, a2, A[0], A[1]

def rand_io(n, span, maxlen, rng):
    iv = []
    for _ in range(n):
        l = rng.randint(1, span); r = min(span, l + rng.randint(0, maxlen)); iv.append((l, r))
    return sorted(iv)

def canonical(iv, keep_order=False):
    """canonical (Fishburn) representation of the interval order given by any interval list:
    D_1 < ... < D_m the distinct down-sets (a chain); l(x) = index of down(x); r(x) = (first index j with
    x in D_j) - 1, or m if x is in none."""
    n = len(iv); R = rel_from_iv(iv)
    down = [frozenset(y for y in range(n) if R[y][x]) for x in range(n)]
    D = sorted(set(down), key=len)
    for i in range(len(D) - 1): assert D[i] < D[i + 1], 'down-sets not a chain: not an interval order'
    m = len(D); idx = {d: i + 1 for i, d in enumerate(D)}
    out = []
    for x in range(n):
        j0 = next((i + 1 for i, d in enumerate(D) if x in d), m + 1)
        out.append((idx[down[x]], j0 - 1))
    return out if keep_order else sorted(out)
