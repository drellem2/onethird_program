"""negative_control.py (audit mg-3345): the audit's instruments must be able to say NO.
Each block plants a statement the audit found false (or a deliberately wrong one) and must print CAUGHT."""
from fractions import Fraction as F
from indep import info
import itertools

def caught(tag, ok): print(("CAUGHT " if ok else "SILENT (control did not fire) ") + tag); return ok

res = []
# 1. doc section 3.2: "{f(x) <= j+1} is contained in cap_U {x before u}" for j beyond k.  Y-gadget + isolated x.
d = info("4 0 1 1 0"); x, U = 3, [1, 2]
bad = [dd for dd in d['pos'] if dd[x] <= 2 and not all(dd[x] < dd[u] for u in U)]
res.append(caught("section 3.2 inclusion at j=k+1 (extension %s)" % (bad[0] if bad else None,), bool(bad)))
# 2. doc verdict 6(a): "every pair touching {x} u Inc(x) for an extreme x is outside [1/3,2/3]" on P_9.
d = info("9 0 0 2 2 3 b 2b 2f 7f")
W = set().union(*[{x, *d['I'][x]} for x in d['mins'] + d['maxs']])
touching = [(a, b) for a, b, _ in d['bal'] if a in W or b in W]
res.append(caught("verdict 6(a) 'every pair touching the end windows is unbalanced' on P_9: %s" % touching, bool(touching)))
# 3. narrowed balance window [0.34,0.66] must reject 2+1's only pairs (sharpness at 1/3): checker can fail.
d = info("3 0 0 2")
res.append(caught("narrowed balance [0.34,0.66] on 2+1", not any(F(34, 100) <= v <= F(66, 100) for _, _, v in d['bal'])))
# 4. Remark 2.6's labelling '(v_1,v_2) = (y,x)': y<a<b<c plus isolated x.
d = info("5 0 1 3 0 7")
H = {v: F(sum(dd[v] + 1 for dd in d['pos']), d['e']) for v in range(5)}
res.append(caught("Remark 2.6 labelling x = v_2", sorted(H, key=H.get)[1] != 3))
# 5. the self-duality test must reject a poset that is not self-dual: V = two minimal below one top.
d = info("3 0 0 3"); n, less = d['n'], d['less']
dual = [[less[j][i] for j in range(n)] for i in range(n)]
iso = any(all(less[i][j] == dual[g[i]][g[j]] for i in range(n) for j in range(n)) for g in itertools.permutations(range(n)))
res.append(caught("self-duality test rejects V (3 0 0 3)", not iso))
print("ALL CONTROLS FIRED" if all(res) else "A CONTROL WAS SILENT"); raise SystemExit(0 if all(res) else 1)
