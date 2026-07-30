"""mg-1c80 part 1 -- THE GATE CENSUS, rebuilt.

Answers, from a second implementation (`kern1c80.py`) that never touches
`controls.py` and never calls `face_complex`'s Laplacian, boundary, target or
absorbability routines:

  A. does the rebuild agree with `face_complex` matrix-for-matrix?  (If not,
     nothing below means anything.)
  B. WHICH GATE does `absorbable_by_diagonal_twist` fail at, per row, under BOTH
     definitions of "which gate": the one the predicate executes and the one
     `controls.deciding_gate` reports.
  C. the section totals the artifact prints: 297 biting pairs, 0 reaching the
     parity system, "0 entries anywhere differing in sign alone".
  D. that last one AT THE SCOPE THE ARTIFACT PRINTS IT, which is not the scope
     the artifact computes it at.
"""

import sys

sys.path.insert(0, "../face_geometry")

from posets import all_posets                                    # noqa: E402
import face_complex as fc                                        # noqa: E402
from kern1c80 import (SCORED_MUTATIONS, absorbable_2col, absorbable_brute,
                      build, census, eq, gate_execution, gate_priority,
                      my_linear_extensions, parity_gauge, target, twisted)  # noqa: E402

BAR = "=" * 78
ps = [P for n in range(2, 6) for P in all_posets(n)]

print(BAR)
print("mg-1c80 part 1 -- WHICH GATE, recomputed from a second implementation")
print(BAR)
print()

# ---------------------------------------------------------------------------
# A.  the rebuild is the same object
# ---------------------------------------------------------------------------
print("A. THE REBUILD AGREES WITH `face_complex`, matrix for matrix")
agree = disagree = 0
for mode in ["true"] + [m for _, m in SCORED_MUTATIONS] + ["facet_swap01"]:
    for P in ps:
        td = fc.top_laplacians(P, incidence_mode=mode)
        s = [fc.perm_sign(w) for w in td["les"]]
        ref = [[s[i] * td["L_rel"][i][j] * s[j] for j in range(len(s))]
               for i in range(len(s))]
        mine = twisted(P, mode)
        agree += eq(ref, mine)
        disagree += not eq(ref, mine)
tg_agree = tg_dis = 0
for P in ps:
    _, ref = fc.at_laplacian(P)
    tg_agree += eq(ref, target(P))
    tg_dis += not eq(ref, target(P))
par_agree = par_dis = 0
for P in ps:
    td = fc.top_laplacians(P, sign_mode="parity")
    s = [fc.perm_sign(w) for w in td["les"]]
    ref = [[s[i] * td["L_rel"][i][j] * s[j] for j in range(len(s))]
           for i in range(len(s))]
    par_agree += eq(ref, parity_gauge(P))
    par_dis += not eq(ref, parity_gauge(P))
print("   E.L^rel.E over 6 incidence modes x %d posets : %d agree, %d DISAGREE"
      % (len(ps), agree, disagree))
print("   target D-A                                  : %d agree, %d DISAGREE"
      % (tg_agree, tg_dis))
print("   NC3 facet-parity build                      : %d agree, %d DISAGREE"
      % (par_agree, par_dis))
print()

# ---------------------------------------------------------------------------
# A'.  the absorbability decision is the same decision
# ---------------------------------------------------------------------------
print("A'. THE ABSORBABILITY DECISION, three ways (union-find / 2-colouring /")
print("    brute force over all 2^m sign vectors)")
n2 = n3 = cases = small = 0
for mode in [m for _, m in SCORED_MUTATIONS] + ["facet_swap01"]:
    for P in ps:
        Lm, tg = twisted(P, mode), target(P)
        ref = fc.absorbable_by_diagonal_twist(Lm, tg)
        mine = absorbable_2col(Lm, tg)
        cases += 1
        n2 += (ref == mine)
        if len(Lm) <= 8:
            small += 1
            n3 += (mine == absorbable_brute(Lm, tg))
for P in ps:
    Lp, tg = parity_gauge(P), target(P)
    ref = fc.absorbable_by_diagonal_twist(Lp, tg)
    mine = absorbable_2col(Lp, tg)
    cases += 1
    n2 += (ref == mine)
    if len(Lp) <= 8:
        small += 1
        n3 += (mine == absorbable_brute(Lp, tg))
print("   union-find vs 2-colouring : %d/%d agree" % (n2, cases))
print("   2-colouring vs brute force: %d/%d agree (|L(P)| <= 8)" % (n3, small))
print()

# ---------------------------------------------------------------------------
# B / C.  the census
# ---------------------------------------------------------------------------
print(BAR)
print("B. THE GATE SPLIT, under BOTH readings of 'which gate settles the pair'")
print(BAR)
print()
print("   controls.deciding_gate tests ALL diagonals, then ALL magnitudes.")
print("   absorbable_by_diagonal_twist tests row i's diagonal, then row i's")
print("   magnitudes, then row i+1's -- the two gates are INTERLEAVED BY ROW.")
print("   Where a pair violates both, the two readings can name different gates.")
print()
hdr = ("   %-6s %-24s %5s %5s | %5s %5s %5s | %5s %5s %5s | %6s"
       % ("row", "corruption", "bites", "shape", "diag", "mag", "par",
          "diag", "mag", "par", "differ"))
print(hdr)
print("   %-6s %-24s %5s %5s | %-17s | %-17s | %6s"
      % ("", "", "", "ok", " deciding_gate()", " predicate's own", ""))
tot = {"app": 0, "shape_ok": 0, "par_pri": 0, "par_exe": 0,
       "sign_all": 0, "sign_diagok": 0, "differ": 0, "absorb": 0}
rows = []
for tag, mode in SCORED_MUTATIONS:
    app = shape_ok = differ = absorb = 0
    pri = {"diagonal": 0, "magnitude": 0, "parity": 0, "shape": 0}
    exe = {"diagonal": 0, "magnitude": 0, "parity": 0, "shape": 0}
    sign_all = sign_diagok = mag_diagok = mag_all = 0
    for P in ps:
        Lt, Lm, tg = twisted(P), twisted(P, mode), target(P)
        if eq(Lm, Lt):
            continue
        app += 1
        m = len(Lt)
        absorb += absorbable_2col(Lm, tg)
        if len(Lm) != m or any(len(Lm[i]) != m for i in range(m)):
            continue
        shape_ok += 1
        gp, ge = gate_priority(Lm, tg), gate_execution(Lm, tg)
        pri[gp] += 1
        exe[ge] += 1
        differ += (gp != ge)
        dm, ds = census(Lm, tg)
        mag_all += dm
        sign_all += ds
        if gp != "diagonal":
            mag_diagok += dm
            sign_diagok += ds
    rows.append((tag, mode, app, shape_ok, pri, exe, differ, sign_all,
                 sign_diagok, mag_all, mag_diagok, absorb))
    print("   %-6s %-24s %5d %5d | %5d %5d %5d | %5d %5d %5d | %6d"
          % (tag, mode, app, shape_ok,
             pri["diagonal"], pri["magnitude"], pri["parity"],
             exe["diagonal"], exe["magnitude"], exe["parity"], differ))
    tot["app"] += app
    tot["shape_ok"] += shape_ok
    tot["par_pri"] += pri["parity"]
    tot["par_exe"] += exe["parity"]
    tot["sign_all"] += sign_all
    tot["sign_diagok"] += sign_diagok
    tot["differ"] += differ
    tot["absorb"] += absorb

# the two non-scored corruptions, for context
for tag, mode in [("swap01", "facet_swap01")]:
    app = 0
    pri = {"diagonal": 0, "magnitude": 0, "parity": 0, "shape": 0}
    exe = dict(pri)
    differ = 0
    for P in ps:
        Lt, Lm, tg = twisted(P), twisted(P, mode), target(P)
        if eq(Lm, Lt):
            continue
        app += 1
        gp, ge = gate_priority(Lm, tg), gate_execution(Lm, tg)
        pri[gp] += 1
        exe[ge] += 1
        differ += (gp != ge)
    print("   %-6s %-24s %5d %5s | %5d %5d %5d | %5d %5d %5d | %6d   (NOT scored)"
          % (tag, mode, app, "-", pri["diagonal"], pri["magnitude"], pri["parity"],
             exe["diagonal"], exe["magnitude"], exe["parity"], differ))
nc3_app = nc3_par = nc3_abs = 0
for P in ps:
    Lt, Lp, tg = twisted(P), parity_gauge(P), target(P)
    if eq(Lp, Lt):
        continue
    nc3_app += 1
    nc3_par += (gate_priority(Lp, tg) == "parity")
    nc3_abs += absorbable_2col(Lp, tg)
print("   %-6s %-24s %5d %5s | %5d %5d %5d | %5s %5s %5s | %6s   (NOT scored)"
      % ("NC3", "facet-parity gauge", nc3_app, "-", 0, 0, nc3_par,
         "-", "-", "-", "-"))
print()
print("   SECTION TOTALS over the four SCORED rows:")
print("     biting (poset, mutation) pairs .................. %d" % tot["app"])
print("     of them with the compared matrices same-shape ... %d" % tot["shape_ok"])
print("     reaching the PARITY system (deciding_gate) ...... %d" % tot["par_pri"])
print("     reaching the PARITY system (predicate's order) .. %d" % tot["par_exe"])
print("     reported absorbable ............................. %d" % tot["absorb"])
print("     pairs the two readings attribute DIFFERENTLY .... %d" % tot["differ"])
print()

# ---------------------------------------------------------------------------
# D.  the sign-only count, at both scopes
# ---------------------------------------------------------------------------
print(BAR)
print("C. 'ENTRIES DIFFERING IN SIGN ALONE' -- printed scope vs computed scope")
print(BAR)
print()
print("   `controls.py` accumulates `sign_entries` INSIDE the `diag_preserved`")
print("   branch (controls.py:1001-1005), so `tot_sign` is a sum over the pairs")
print("   whose diagonal survived.  The routing row prints it as")
print("     '%d entries ANYWHERE differ in sign alone', over 'all four rows',")
print("   and the gate table as a 'Section total'.  Both scopes measured here:")
print()
print("   %-6s %-24s %10s %10s %12s %12s"
      % ("row", "corruption", "sign(all)", "sign(diagOK)", "mag(all)", "mag(diagOK)"))
for (tag, mode, app, shape_ok, pri, exe, differ, sa, sd, ma, md, ab) in rows:
    print("   %-6s %-24s %10d %10d %12d %12d" % (tag, mode, sa, sd, ma, md))
print("   %-6s %-24s %10d %10d" % ("TOTAL", "", tot["sign_all"], tot["sign_diagok"]))
print()
print("   pairs the printed number is a total OVER  : %d" % tot["app"])
print("   pairs the printed number is COMPUTED over : %d"
      % sum(1 for (_, _, _, _, pri, _, _, _, _, _, _, _) in rows
            for _ in range(pri["magnitude"] + pri["parity"])))
print()

# ---------------------------------------------------------------------------
# E.  the three posets row I4 cites
# ---------------------------------------------------------------------------
print(BAR)
print("D. THE THREE POSETS ROW I4 KEEPS ABSORBABILITY SCORED FOR")
print(BAR)
print()
for P in ps:
    Lt, Lm, tg = twisted(P), twisted(P, "facet_offbyone"), target(P)
    if eq(Lm, Lt):
        continue
    if gate_priority(Lm, tg) == "diagonal":
        continue
    m = len(Lm)
    mag_all, sgn_all = census(Lm, tg)
    mag_off, sgn_off = census(Lm, tg, offdiag_only=True)
    print("   n=%d |L(P)|=%-4d antichain=%-5s  gate(exec)=%-9s gate(pri)=%-9s"
          % (P.n, m, P.is_antichain(), gate_execution(Lm, tg),
             gate_priority(Lm, tg)))
    print("        magnitude mismatches: whole matrix %4d, off-diagonal %4d "
          "(%.1f per row)" % (mag_all, mag_off, mag_off / float(m)))
    print("        sign-only mismatches: whole matrix %4d, off-diagonal %4d"
          % (sgn_all, sgn_off))
    print("        absorbable (2-colouring) = %s ; (brute force) = %s"
          % (absorbable_2col(Lm, tg),
             absorbable_brute(Lm, tg) if m <= 8 else "n/a (m > 8)"))
print()
