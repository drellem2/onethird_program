"""brightwell.py (mg-afa4): Brightwell's semiorder argument, generalised, on interval orders.

(B1) injection lemma, ANY poset, any incomparable (a,a'):  P[a<a', no separator of (a,a') between] <= P[a'<a],
     separators S(a,a') = {z: a covered by z, z||a'} u {z: z covered by a', z||a}.  Checked exactly (+ control).
(B2) combinatorial question: in a counterexample the relation 'P[x<y] > 2/3' is a linear extension L that
     agrees with interval dominance on dominance-comparable pairs, and every L-consecutive incomparable pair
     has >= 2 separators.  Call such an L 'Brightwell-bad'.  If an interval order has no bad L, it satisfies
     1/3-2/3.  Enumerate bad Ls."""
import sys, itertools
from fractions import Fraction as F
from iolib import *

def covers(iv):
    n = len(iv)
    return {(a, b) for a in range(n) for b in range(n) if lt(iv, a, b)
            and not any(lt(iv, a, c) and lt(iv, c, b) for c in range(n))}

def seps(iv, C, a, a2):
    n = len(iv)
    return [z for z in range(n) if ((a, z) in C and inc(iv, z, a2)) or ((z, a2) in C and inc(iv, z, a))]

def linexts(iv):
    n = len(iv)
    def rec(pre, used):
        if len(pre) == n: yield pre; return
        for v in range(n):
            if not used >> v & 1 and all(used >> w & 1 for w in range(n) if lt(iv, w, v)):
                yield from rec(pre + [v], used | 1 << v)
    yield from rec([], 0)

def check_B1(iv):
    n = len(iv); C = covers(iv); bad = 0; bad_ctrl = 0
    exts = list(linexts(iv)); t = len(exts)
    for a in range(n):
        for a2 in range(n):
            if not inc(iv, a, a2): continue
            S = set(seps(iv, C, a, a2)); Sc = {z for z in S if (a, z) in C}   # control: above-separators only
            c1 = c1c = c3 = 0
            for L in exts:
                pos = {v: i for i, v in enumerate(L)}
                if pos[a] < pos[a2]:
                    btw = {L[i] for i in range(pos[a] + 1, pos[a2])}
                    c1 += not (btw & S); c1c += not (btw & Sc)
                else: c3 += 1
            bad += c1 > c3; bad_ctrl += c1c > c3
    return bad, bad_ctrl

def dominance_ok(iv, L):
    pos = {v: i for i, v in enumerate(L)}; n = len(iv)
    for x in range(n):
        for y in range(n):
            if inc(iv, x, y) and iv[x] != iv[y] and iv[x][0] <= iv[y][0] and iv[x][1] <= iv[y][1] and pos[x] > pos[y]:
                return False
    return True

def bad_Ls(iv):
    C = covers(iv); out = []
    for L in linexts(iv):
        if not dominance_ok(iv, L): continue
        ok = True
        for i in range(len(L) - 1):
            a, a2 = L[i], L[i + 1]
            if inc(iv, a, a2) and len(seps(iv, C, a, a2)) < 2: ok = False; break
        if ok: out.append(L)
    return out

if __name__ == '__main__':
    NB1 = 6; tot = bad = badc = 0
    for n in range(2, NB1 + 1):
        for iv in gen(n):
            b, bc = check_B1(iv); tot += 1; bad += b; badc += bc
    print(f"(B1) all interval orders n<=6 ({tot}): injection violations = {bad}; CONTROL (above-separators only) violations = {badc}")
    # B1 on general posets too (not only interval orders): the 2+2, N, and T8
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    for n in range(3, NMAX + 1):
        cnt = 0; ex = None; semibad = 0
        for iv in gen(n):
            if decomposable(iv) or len(set(iv)) < n: continue
            B = bad_Ls(iv)
            if B:
                cnt += 1; ex = ex or (iv, B[0])
                if not any(iv[a][0] < iv[b][0] and iv[b][1] < iv[a][1] for a in range(n) for b in range(n)): semibad += 1
        print(f"(B2) n={n}: indecomposable twin-free interval orders with a Brightwell-bad L: {cnt} (semiorders among them: {semibad})"
              + (f"; e.g. {ex[0]} L={ex[1]}" if ex else ""))
        sys.stdout.flush()
