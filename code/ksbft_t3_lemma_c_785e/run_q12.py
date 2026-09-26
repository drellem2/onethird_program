import sys, time
from xyzlp import *
import flp
L = mk(Q12, LQ12)
for tools in (('T1','T2','T3'),):
  for xyz in (False, True):
    t0 = time.time()
    M, eps, T, nx = build(Q12, L, tools=tools, xyz=xyz)
    v, x, d = flp.solve(M, eps)
    print(f"Q12 {'+'.join(tools)} +TRI/JT {'+XYZ(McCormick on L-boxes)' if xyz else ''}: eps* ~ {v:.6f} (1/eps={1/v if v else 0:.2f}) [{M.nv} vars, {len(M.rows)} rows, {len(T)} triples, {nx} XYZ rows, {time.time()-t0:.1f}s]")
