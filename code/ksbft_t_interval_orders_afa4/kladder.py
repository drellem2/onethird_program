"""kladder.py (mg-afa4): the Brightwell-bad dominance Ls of interval orders n<=10 -- do they survive the extra
constraints a counterexample's order L must satisfy by the (audited) Swap Ladder Thm 1.4?
In a counterexample, L = 'P[x<y]>2/3'.  For x||b with l(x)<=l(b) and chain bottom b=b_0<..<b_m of W=up[b]-up[x]:
  (SL1) if b precedes x in L then b_m precedes x   (else the first crossing is balanced: steps <= t_0 < 1/3);
  (SL2) if W is a chain (full) then x precedes b    (full & t_0<1/3 forces a balanced rung).
and the order-dual statements (r(x)>=r(b), chain top of down[b]-down[x]).  Reports survivors."""
import sys, os
from multiprocessing import Pool
from iolib import *
from kdfs import prep

def ladders(iv):
    """list of (x, b, bm, full) constraints, primal and dual (dual: 'precedes' reversed)."""
    n = len(iv); out = []
    for dual in (False, True):
        L_ = (lambda a, b: lt(iv, b, a)) if dual else (lambda a, b: lt(iv, a, b))
        for x in range(n):
            for b in range(n):
                if not inc(iv, x, b): continue
                ok = (iv[x][1] >= iv[b][1]) if dual else (iv[x][0] <= iv[b][0])
                if not ok: continue
                W = {z for z in range(n) if z == b or L_(b, z)} - {z for z in range(n) if z == x or L_(x, z)}
                ch = [b]; rest = W - {b}; full = True
                while rest:
                    mins = [z for z in rest if not any(L_(w, z) for w in rest)]
                    if len(mins) != 1: full = False; break
                    ch.append(mins[0]); rest.discard(mins[0])
                out.append((x, b, ch[-1], full, dual))
    return out

def sl_ok(L, cons):
    pos = {v: i for i, v in enumerate(L)}
    for x, b, bm, full, dual in cons:
        prec = (lambda u, v: pos[u] > pos[v]) if dual else (lambda u, v: pos[u] < pos[v])   # 'u precedes v' in the ladder's orientation
        if full and not prec(x, b): return False
        if prec(b, x) and not prec(bm, x): return False
    return True

def all_bad(iv):
    n, INC, NS, DOM, down = prep(iv)
    need = [down[v] | sum(1 << w for w in range(n) if DOM[w][v]) for v in range(n)]
    out = []
    def rec(used, last, pre):
        if len(pre) == n: out.append(list(pre)); return
        for v in range(n):
            if used >> v & 1 or need[v] & ~used: continue
            if last >= 0 and INC[last][v] and NS[last][v] < 2: continue
            pre.append(v); rec(used | 1 << v, v, pre); pre.pop()
    rec(0, -1, [])
    return out

def job(iv):
    if all(not inc(iv, a, b) for a in range(len(iv)) for b in range(len(iv))): return None
    B = all_bad(iv)
    if not B: return None
    cons = ladders(iv)
    surv = [L for L in B if sl_ok(L, cons)]
    return (iv, len(B), surv)

if __name__ == '__main__':
    cores = int(os.environ.get('POGO_WORKER_CORES', '3'))
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    with Pool(cores) as pool:
        for n in range(9, NMAX + 1):
            R = [x for x in pool.imap_unordered(job, gen_fast(n), chunksize=256) if x]
            s = [x for x in R if x[2]]
            print(f"n={n}: {len(R)} interval orders with a bad dominance L ({sum(x[1] for x in R)} bad Ls); "
                  f"surviving the Swap-Ladder constraints: {len(s)} posets, {sum(len(x[2]) for x in s)} Ls")
            for iv, nb, surv in R:
                print(f"    {iv}  bad Ls={nb}  SL-survivors={len(surv)}" + (f"  e.g. L={[iv[v] for v in surv[0]]}" if surv else ""))
            sys.stdout.flush()
