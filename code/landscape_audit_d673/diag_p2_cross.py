#!/usr/bin/env python3
"""Cross-check the P2 disagreement against the TARGET's own functions.

Forensics only: the audit verdict rests on audit_populations.py, which shares
no code with the target.  This script imports the target's implementation
solely to locate where the two disagree.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'landscape_ebd8'))

import identify_lattice as T
import audit_populations as M

n = 4
rel_mine = frozenset({(0, 3), (1, 2)})          # a<d, b<c
rel_theirs = set(rel_mine)

# --- their pipeline
partsT = list(T.set_partitions(n))
A = [pi for pi in partsT if T.acyclic_quotient(n, rel_theirs, pi)]
lesT = T.linear_extensions(n, rel_theirs)
eT = len(lesT)
eCT = T.cyclic_classes(n, lesT)
muT, bot, top = T.mobius_bottom_top(A, T.refines)
connT = T.is_connected(n, rel_theirs)
print("TARGET  : |AC|=%d  e=%d  e_C=%d  connected=%s  mu=%d  predicted_s=%d  predicted_mu=%d"
      % (len(A), eT, eCT, connT, muT, (eT if connT else eCT),
         ((-1) ** (n - 1)) * (eT if connT else eCT)))
print("          bot = %s" % (sorted(sorted(b) for b in A[bot]),))
print("          top = %s" % (sorted(sorted(b) for b in A[top]),))

# --- my pipeline
ac = M.AC_by_acyclicity(rel_mine, n)
muM = M.moebius_bottom_to_top(ac)
eM = len(M.linear_extensions(rel_mine, n))
eCM = M.cyclic_classes(rel_mine, n)
connM = M.is_connected(rel_mine, n)
print("MINE    : |AC|=%d  e=%d  e_C=%d  connected=%s  mu=%d  predicted_mu=%d"
      % (len(ac), eM, eCM, connM, muM, ((-1) ** (n - 1)) * eCM))

print()
print("AC sets identical:", set(tuple(sorted(sorted(b) for b in pi)) for pi in A)
      == set(tuple(sorted(sorted(b) for b in pi)) for pi in ac))
print("linear extensions identical:",
      set(tuple(w) for w in lesT) == set(M.linear_extensions(rel_mine, n)))
print()
print("their linear extensions:", sorted(tuple(w) for w in lesT))
print()
print("--- what does the target's is_connected say on all n=4 posets? ---")
for r in M.iso_classes(4):
    cm = M.is_connected(r, 4)
    ct = T.is_connected(4, set(r))
    if cm != ct:
        print("   CONNECTEDNESS DISAGREES on", sorted(r), "mine", cm, "theirs", ct)
print("   (nothing printed = agree)")
print()
print("--- their per-poset P2 on n=4, verbose ---")
for r in M.iso_classes(4):
    rs = set(r)
    A2 = [pi for pi in partsT if T.acyclic_quotient(4, rs, pi)]
    les2 = T.linear_extensions(4, rs)
    e2 = len(les2)
    eC2 = T.cyclic_classes(4, les2)
    mu2, _, _ = T.mobius_bottom_top(A2, T.refines)
    c2 = T.is_connected(4, rs)
    pred2 = ((-1) ** 3) * (e2 if c2 else eC2)
    flag = "" if mu2 == pred2 else "   <<< P2 FAIL"
    if flag:
        print("   rel=%s conn=%s |AC|=%d mu=%d e=%d eC=%d pred=%d%s"
              % (sorted(rs), c2, len(A2), mu2, e2, eC2, pred2, flag))
print("   (nothing printed = the target's own code reports 0 bad)")
