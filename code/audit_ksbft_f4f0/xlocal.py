"""xlocal.py (audit mg-f4f0): independent re-derivation of mg-785e sec 4.1 (X-local form of Lemma C).
For every canonical interval order of size n (Fishburn-matrix generator, counts certified against A022493)
and every strict-containment pair a inside a' (a first) with |S(a,a')| = 2, S = {s,t}: exact
q = P[a'<a], u_s = P[s<a'], u_t = P[t<a'], w = min(P[s<t], P[t<s]). Region: q, u_s, u_t < 1/3.
Usage: xlocal.py N [shard nshards]."""
import sys, time
from fractions import Fraction as F
from eng import *

def run(n, shard=0, nsh=1):
    tot = reg = twins = 0; nontw = []; cnt_posets = 0; nposets = 0
    for idx, iv in enumerate(fishburn(n)):
        nposets += 1
        if idx % nsh != shard: continue
        R = rel_from_iv(iv); C = covers_rel(R)
        cp = list(cont_twosep(iv, R, C))
        if not cp: continue
        cnt, e = pair_counts(R); cnt_posets += 1
        for a, a2, s, t in cp:
            tot += 1
            q = F(cnt[a2][a], e); us = F(cnt[s][a2], e); ut = F(cnt[t][a2], e)
            if q < F(1, 3) and us < F(1, 3) and ut < F(1, 3):
                reg += 1
                w = min(F(cnt[s][t], e), F(cnt[t][s], e))
                if iv[s] == iv[t]: twins += 1; assert w == F(1, 2)
                else: nontw.append((w, iv, iv[a], iv[a2], iv[s], iv[t], q, us, ut))
    return nposets, cnt_posets, tot, reg, twins, nontw

if __name__ == '__main__':
    n = int(sys.argv[1]); sh = int(sys.argv[2]) if len(sys.argv) > 2 else 0; nsh = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    t0 = time.time()
    npo, cp, tot, reg, tw, nt = run(n, sh, nsh)
    print(f'n={n} shard {sh}/{nsh}: posets {npo} (A022493: {FISH[n]}), with a containment 2-sep pair {cp}; such pairs {tot}; '
          f'in region q,u_s,u_t<1/3: {reg}; twins {tw}; non-twin {len(nt)}; '
          f'min w non-twin = {min(nt)[0] if nt else None}; unbalanced (w<1/3) in region: {sum(1 for x in nt if x[0] < F(1,3))}  [{time.time()-t0:.0f}s]')
    for x in sorted(nt)[:5]:
        print('   ', x[1], 'a', x[2], "a'", x[3], 's', x[4], 't', x[5], 'q,us,ut,w =', ' '.join(f'{float(v):.4f}' for v in (x[6], x[7], x[8], x[0])), 'w =', x[0])
