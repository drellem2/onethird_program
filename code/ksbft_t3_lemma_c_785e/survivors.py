"""survivors.py (mg-785e): the 13 LP-feasible survivors of mg-561a (out_lpsurv.txt rows with T1+T2+T3 > 0),
parsed read-only from ../ksbft_t2_two_separator_561a/out_lpsurv.txt."""
import os, re, ast
from t3lib import HERE

def survivors():
    txt = open(os.path.join(HERE, '..', 'ksbft_t2_two_separator_561a', 'out_lpsurv.txt')).read()
    out = []
    for P, L, res in re.findall(r"P=(\[.*?\])\n  L=(\[.*?\])\n  (.*)", txt):
        v = res.split('T1+T2+T3:')[1].strip()
        if v == 'INFEASIBLE' or float(v) <= 0: continue
        iv = ast.literal_eval(P); Lt = ast.literal_eval(L)
        used = set(); Li = []
        for t in Lt:
            i = next(j for j in range(len(iv)) if iv[j] == t and j not in used); used.add(i); Li.append(i)
        out.append((iv, Li, float(v)))
    return out

if __name__ == '__main__':
    S = survivors(); print(len(S))
    from t3lib import downmasks, laws
    for iv, L, v in S: print(len(iv), laws(downmasks(iv))[0], v)
