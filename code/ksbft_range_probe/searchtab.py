"""searchtab.py -- tabulate annealing witnesses (mg-2912).  Exact values."""
import json, sys
from fractions import Fraction as F
rows = {}
for f in sys.argv[1:]:
    for l in open(f):
        o = json.loads(l); r = o["rec"]; e = int(r["e"])
        rows.setdefault(o["tag"], []).append((o["D"], r["n"], r["pi"], r["width"], F(int(r["M_num"]), e), F(int(r["delta_num"]), e)))
for tag, L in rows.items():
    print(tag, "(D = range cap; witness pi, width; M; delta)")
    for D, n, pi, w, M, dl in sorted(L):
        print(f"  D={D} n={n:2d} pi={pi} w={w}  M={float(M):.6f}  delta={float(dl):.6f}   M={M}  delta={dl}")
