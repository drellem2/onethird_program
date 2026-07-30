#!/usr/bin/env python3
"""Diagnose the P2 disagreement: my mu(0,1) of AC(P) vs (-1)^(n-1)*e_C(P)."""
import sys
from audit_populations import (iso_classes, F_of_P, AC_by_acyclicity,
                               moebius_bottom_to_top, linear_extensions,
                               cyclic_classes, is_connected)

for n in (3, 4, 5):
    print(f"--- n={n} ---")
    for rel in iso_classes(n):
        ac = AC_by_acyclicity(rel, n)
        mu = moebius_bottom_to_top(ac)
        e = len(linear_extensions(rel, n))
        eC = cyclic_classes(rel, n)
        pred = ((-1) ** (n - 1)) * eC
        if mu != pred:
            names = lambda r: ",".join(f"{chr(97+i)}<{chr(97+j)}" for i, j in sorted(r))
            print(f"  P = [{names(rel)}]  connected={is_connected(rel,n)}  "
                  f"|AC|={len(ac)}  mu={mu}  e={e}  e_C={eC}  pred={pred}")
