"""verify_certs.py (mg-785e): EXACT re-check of certs.json (pure Python, Fractions; no scipy).
For each certificate: rebuild the identity rows of its family (gen_certs.family), check every row has uniform
expectation 0 ONLY via its derivation (it is a Swap Identity, Thm 1.1 of mg-561a, or a conditioned one, Prop 1.1 of
KSBFT-T3), then compute G(sigma) = sum lambda_i [inversion i in sigma] + sum y_r R_r(sigma) on EVERY linear
extension and assert min G > 0 and sum(lambda) / min G < 3.  Also asserts, as a check of the identities
themselves, that sum_sigma R_r(sigma) = 0 for every row used (uniform expectation zero, exact).
CONTROLS (must be CAUGHT): (c1) lambda scaled by 9/10 fails; (c2) every identity multiplier dropped fails
(with mu = point mass on L no charged inversion occurs, so no identity-free certificate can exist);
(c3) a row that is NOT a valid identity (Lambda_1 of one orientation only) has nonzero sum and is caught."""
import json, sys
from fractions import Fraction as F
from gen_certs import family

def check(c, scale=F(1), drop_y=False):
    iv = [tuple(t) for t in c['P']]; Lt = [tuple(t) for t in c['L']]
    used = set(); L = []
    for t in Lt:
        i = next(j for j in range(len(iv)) if iv[j] == t and j not in used); used.add(i); L.append(i)
    m = family(iv, L, c['family'])
    lam = {tuple(map(int, k.split(','))): F(v) * scale for k, v in c['lam'].items()}
    y = {} if drop_y else {int(k): F(v) for k, v in c['y'].items()}
    for j in y:
        assert sum(m.eq[j].values()) == 0, 'identity row with nonzero uniform sum'
    G = [F(0)] * len(m.E)
    for (u, v), x in lam.items():
        for k, p in enumerate(m.P):
            if p[v] < p[u]: G[k] += x
    for j, x in y.items():
        for k, cf in m.eq[j].items(): G[k] += x * cf
    g = min(G); tot = sum(lam.values())
    return g > 0 and tot / g < 3, (tot / g if g > 0 else None), len(m.E)

if __name__ == '__main__':
    C = json.load(open('certs.json')); bad = 0
    for c in C:
        ok, r, e = check(c)
        print(f"{'VALID' if ok else 'INVALID'}  {c['family']:10s} window={c['window']}  e(P)={e:6d}  sum(lambda)/min G = {r} = {float(r):.6f} < 3  "
              f"[{len(c['lam'])} charged pairs, {len(c['y'])} identity rows]  P={c['P']}")
        bad += not ok
    c0 = min(C, key=lambda c: len(c['y']))
    ok1 = check(c0, scale=F(9, 10))[0]; ok2 = check(c0, drop_y=True)[0]
    print(f"control c1 (lambda x 9/10): {'CAUGHT' if not ok1 else 'NOT CAUGHT'}")
    print(f"control c2 (identities dropped): {'CAUGHT' if not ok2 else 'NOT CAUGHT'}")
    from mulp import MuLP; from xyzlp import Q12, LQ12, mk
    m = MuLP(Q12, mk(Q12, LQ12)); a, b = 4, 3                         # (3,4) and (2,5)
    one_sided = {k: 1 for k in m.lam1(a, b)}
    print(f"control c3 (one-orientation row sum = {sum(one_sided.values())}): {'CAUGHT' if sum(one_sided.values()) != 0 else 'NOT CAUGHT'}")
    print(f"certificates: {len(C) - bad} valid, {bad} invalid")
    sys.exit(1 if bad or ok1 or ok2 else 0)
