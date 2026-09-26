"""bnb.py (mg-785e): spatial branch-and-bound for max eps under the EXACT (nonlinear) XYZ inequalities on
the triples of xyzlp.build.  Node = boxes for pair laws; relaxation = McCormick (valid); split the box of a
pair law occurring in the most violated XYZ instance at the relaxation's value.  Terminates when every open
node has relaxation value <= target (=> the nonlinear system has max eps <= target: a proof, modulo float LP,
re-certified exactly per leaf by certify_leaves) or when a relaxation optimum satisfies every XYZ instance
to tolerance (=> a genuine point of the nonlinear system: XYZ on these triples does NOT kill).
usage: python3 bnb.py [maxnodes]"""
import sys, heapq
from fractions import Fraction as F
from xyzlp import *
from xyzcheck import xyz_violations
import flp

def run(iv, L, target=0.0, maxnodes=400, tol=1e-9, verbose=True):
    n = len(iv); pos = {v: i for i, v in enumerate(L)}
    def key(y, z): return (y, z) if pos[y] < pos[z] else (z, y)
    def lpbox(boxes):
        M, eps, T, nx = build(iv, L, boxes=boxes)
        v, x, d = flp.solve(M, eps)
        return v, x, M, T
    root = {}
    v, x, M, T = lpbox(root)
    heap = [(-v, 0, root, x, M, T)]; cnt = 1; leaves = []
    while heap and cnt < maxnodes:
        nv, _, boxes, x, M, T = heapq.heappop(heap); v = -nv
        if v <= target: leaves.append(boxes); continue
        V = xyz_violations(iv, L, M, x, T)
        if not V or V[0][0] >= -tol:
            return ('FEASIBLE', v, boxes, x, M, cnt)
        slack, typ, xx, y, z = V[0]
        ix = {t: i for i, t in enumerate(iv)}
        xi, yi, zi = ix[xx], ix[y], ix[z]
        # split the wider of the two pair-law boxes
        cands = []
        for (p, r) in ((xi, yi), (xi, zi)):
            k = key(p, r)
            lo, hi = boxes.get(k, (F(2, 3), F(1)))
            name2 = {nm: j for j, nm in enumerate(M.names)}
            val = 1 - x[name2[f'x{iv[k[0]]}{iv[k[1]]}']]
            cands.append((hi - lo, k, lo, hi, val))
        w, k, lo, hi, val = max(cands)
        mid = F(val).limit_denominator(10**6)
        if not (lo < mid < hi): mid = (lo + hi) / 2
        for nb in ((lo, mid), (mid, hi)):
            b2 = dict(boxes); b2[k] = nb
            v2, x2, M2, T2 = lpbox(b2); cnt += 1
            if v2 is None: leaves.append(b2); continue
            heapq.heappush(heap, (-v2, cnt, b2, x2, M2, T2))
        if verbose and cnt % 20 < 2:
            print(f"  nodes {cnt}, open {len(heap)}, best bound {(-heap[0][0]) if heap else None}"); sys.stdout.flush()
    if not heap: return ('REFUTED', target, leaves, None, None, cnt)
    return ('OPEN', -heap[0][0], None, None, None, cnt)

if __name__ == '__main__':
    mx = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    L = mk(Q12, LQ12)
    res = run(Q12, L, maxnodes=mx)
    print(res[0], 'value', res[1], 'nodes', res[5])
    if res[0] == 'FEASIBLE':
        boxes, x, M = res[2], res[3], res[4]
        print('boxes:', {(Q12[a], Q12[b]): (float(l), float(h)) for (a, b), (l, h) in boxes.items()})
