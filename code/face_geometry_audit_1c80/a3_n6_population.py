"""mg-1c80 part 3 -- THE HALF OF 'FORCED AT EVERY n' NOBODY MEASURED.

This is the item this audit adds that no brief in the chain names.

`controls.py`'s section docstring, as mg-da45 leaves it, says the answer is
"forced at every n and not merely measured to n = 5", and the argument it gives
is the rotation argument checked in part 2.  That argument is about ANTICHAINS:
`rot` maps L(P) onto L(P) only when L(P) is all of S_n.  It says nothing about
the other half of the statement -- that at larger n no OTHER poset has row I4's
diagonal preserved, which is what would put a pair into the parity system and
make the absorbability answer a decision after all.

mg-f1b2's own instrument measured the four-mutation gate split at n <= 5 and the
antichain alone at n = 6.  mg-da45's verifier does the same.  Nobody has run the
gate split over the WHOLE n = 6 population, which is where a non-antichain with a
surviving diagonal would first have to appear.

Run here, from the part-1 rebuild: all 318 posets on 6 elements, all four scored
mutations, plus NEGATIVE CONTROL 3's gauge for contrast.
"""

import sys
import time

sys.path.insert(0, "../face_geometry")

from posets import all_posets                                        # noqa: E402
from kern1c80 import (SCORED_MUTATIONS, absorbable_2col, census, eq,
                      gate_execution, gate_priority, parity_gauge,
                      target, twisted)                               # noqa: E402

BAR = "=" * 78
N = 6

t0 = time.time()
ps = all_posets(N)
print(BAR)
print("mg-1c80 part 3 -- the gate split over the FULL n = %d population (%d posets)"
      % (N, len(ps)))
print(BAR)
print()
print("   %-6s %-24s %6s | %5s %5s %5s | %5s %5s %5s | %8s %8s"
      % ("row", "corruption", "bites", "diag", "mag", "par",
         "diag", "mag", "par", "sign-any", "absorb"))
print("   %-6s %-24s %6s | %-17s | %-17s | %8s %8s"
      % ("", "", "", " deciding_gate()", " predicate's own", "", ""))

tot_app = tot_par = tot_sign = tot_absorb = tot_differ = 0
diagok_posets = []
for tag, mode in SCORED_MUTATIONS:
    app = differ = absorb = sign_all = 0
    pri = {"diagonal": 0, "magnitude": 0, "parity": 0, "shape": 0}
    exe = dict(pri)
    for P in ps:
        Lt, Lm, tg = twisted(P), twisted(P, mode), target(P)
        if eq(Lm, Lt):
            continue
        app += 1
        absorb += absorbable_2col(Lm, tg)
        gp, ge = gate_priority(Lm, tg), gate_execution(Lm, tg)
        pri[gp] += 1
        exe[ge] += 1
        differ += (gp != ge)
        _, ds = census(Lm, tg)
        sign_all += ds
        if gp != "diagonal":
            diagok_posets.append((tag, P, gp))
    print("   %-6s %-24s %6d | %5d %5d %5d | %5d %5d %5d | %8d %8d"
          % (tag, mode, app, pri["diagonal"], pri["magnitude"], pri["parity"],
             exe["diagonal"], exe["magnitude"], exe["parity"], sign_all, absorb))
    tot_app += app
    tot_par += pri["parity"]
    tot_sign += sign_all
    tot_absorb += absorb
    tot_differ += differ

nc3_app = nc3_par = nc3_abs = 0
for P in ps:
    Lt, Lp, tg = twisted(P), parity_gauge(P), target(P)
    if eq(Lp, Lt):
        continue
    nc3_app += 1
    nc3_par += (gate_priority(Lp, tg) == "parity")
    nc3_abs += absorbable_2col(Lp, tg)
print("   %-6s %-24s %6d | %5d %5d %5d | %5s %5s %5s | %8s %8d   (NOT scored)"
      % ("NC3", "facet-parity gauge", nc3_app, 0, 0, nc3_par, "-", "-", "-",
         "-", nc3_abs))
print()
print("   SECTION TOTALS at n = %d, over the four SCORED rows:" % N)
print("     biting (poset, mutation) pairs ............ %d" % tot_app)
print("     reaching the PARITY system ................ %d" % tot_par)
print("     entries differing in SIGN ALONE, all pairs. %d" % tot_sign)
print("     reported absorbable ....................... %d" % tot_absorb)
print("     gate attributions the two readings differ . %d" % tot_differ)
print()
print("   EVERY pair at n = %d whose diagonal SURVIVED, with the poset named:" % N)
for tag, P, gp in diagok_posets:
    covers = sorted((a, b) for (a, b) in P.less
                    if not any((a, c) in P.less and (c, b) in P.less
                               for c in range(P.n)))
    print("     %s  %s  antichain=%s  covers=%s  gate=%s"
          % (tag, "n=%d" % P.n, P.is_antichain(),
             covers if covers else "(none)", gp))
print()
print("   Took %.1f s." % (time.time() - t0))
print()
