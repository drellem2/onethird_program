"""lpsurv.py (mg-561a): run the LP calculus (lpcheck.py) on the (P, L) that survive Thm 2.1, TS, 2.1*, 3.1*
(kstar.py survivors in the staircase family).  Output: max eps per tool set; eps* <= 0 = refuted.
usage: python3 lpsurv.py"""
import sys, os
from multiprocessing import Pool
from t2lib import *
import kprime, kstar
from lpcheck import check

def job(iv):
    A, B, need = kstar.tables(iv)
    out = []
    for L in kstar.all_bad(iv, A, B, need):
        if kstar.classify(iv, L, A, B) != 'SURVIVES': continue
        res = {}
        for tools in (('T1',), ('T1', 'T2'), ('T1', 'T2', 'T3')):
            v, M = check(iv, L, tools); res['+'.join(tools)] = v
        out.append((iv, [iv[x] for x in L], res))
    return out

if __name__ == '__main__':
    fam = list(kprime.staircase_family())
    with Pool(int(os.environ.get('POGO_WORKER_CORES', '3'))) as pool:
        R = pool.map(kprime.job, fam, chunksize=64)
        pop = [iv for iv, o in zip(fam, R) if o and o['K']]
        S = pool.map(kstar.job, pop, chunksize=1)
        pop2 = [iv for iv, k, cnt, surv in S if surv]
        res = [r for rs in pool.map(job, pop2, chunksize=1) for r in rs]
    agg = {}
    for iv, L, r in res:
        for k, v in r.items():
            a = agg.setdefault(k, [0, 0]); a[0] += 1; a[1] += (v is None or v <= 0)
        print(f"P={iv}\n  L={L}\n  " + "  ".join(f"{k}: {'INFEASIBLE' if v is None else float(v)}" for k, v in r.items()))
    print("SUMMARY refuted/total per tool set:", {k: f"{a[1]}/{a[0]}" for k, a in agg.items()})
