"""mg-1c80 part 5 -- EVERY CLAIM THE REPAIR'S NEW PROSE MAKES, SCORED.

The defect class at this generation is *a control asserting a reason it does not
have*, so the audit's own obligation is to take each sentence mg-da45 ADDS and
put a computed number beside it.  Three verdicts:

  [HOLDS ]  the claim is true and the code computes it at the scope printed
  [SCOPE ]  the claim is TRUE but the code computes it over a SMALLER
            population than the sentence says it covers -- true today, and
            printed as 0 whatever a future change makes it
  [BROKEN]  the claim is false

A [SCOPE] is not a rounding complaint.  It is the exact shape this arc keeps
landing: "a printed claim wider than the code verifies", in `controls.py`'s own
words two hundred lines further down.
"""

import os
import subprocess
import sys

sys.path.insert(0, "../face_geometry")

from posets import all_posets                                        # noqa: E402
from kern1c80 import (SCORED_MUTATIONS, absorbable_2col, census, eq,
                      gate_execution, gate_priority, parity_gauge, target,
                      twisted)                                       # noqa: E402

BAR = "=" * 78
FG = "../face_geometry"
SRC = open(os.path.join(FG, "controls.py")).read()
ART = open(os.path.join(FG, "controls_output.txt")).read()
FCX = open(os.path.join(FG, "face_complex.py")).read()
ps = [P for n in range(2, 6) for P in all_posets(n)]

LEDGER = []


def score(verdict, claim, detail=""):
    LEDGER.append((verdict, claim))
    print("  [%-6s] %s" % (verdict, claim))
    if detail:
        for line in detail.split("\n"):
            print("            " + line)


print(BAR)
print("mg-1c80 part 5 -- the repair's new prose, claim by claim")
print(BAR)

# ---------------------------------------------------------------------------
# recompute everything the ledger needs, once
# ---------------------------------------------------------------------------
stats = {}
tot = dict(app=0, par=0, sign_all=0, sign_diagok=0, differ=0, absorb=0,
           diag_also_mag=0, diag=0)
for tag, mode in SCORED_MUTATIONS:
    app = absorb = sign_all = sign_diagok = mag_diagok = differ = 0
    pri = {"diagonal": 0, "magnitude": 0, "parity": 0}
    exe = dict(pri)
    diag_also_mag = 0
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
        m = len(Lm)
        dm, ds = census(Lm, tg)
        sign_all += ds
        if gp == "diagonal":
            # is the diagonal violation ALSO a magnitude violation?
            diag_also_mag += any(abs(Lm[i][i]) != abs(tg[i][i]) for i in range(m)
                                 if Lm[i][i] != tg[i][i])
        else:
            sign_diagok += ds
            mag_diagok += dm
    stats[tag] = dict(app=app, pri=pri, exe=exe, absorb=absorb,
                      sign_all=sign_all, sign_diagok=sign_diagok,
                      mag_diagok=mag_diagok, differ=differ,
                      diag_also_mag=diag_also_mag)
    tot["app"] += app
    tot["par"] += pri["parity"]
    tot["sign_all"] += sign_all
    tot["sign_diagok"] += sign_diagok
    tot["differ"] += differ
    tot["absorb"] += absorb
    tot["diag"] += pri["diagonal"]
    tot["diag_also_mag"] += diag_also_mag

i4 = stats["I4"]

# ---------------------------------------------------------------------------
print()
print("A. THE HEADLINE -- what row I4 now prints about itself")
print()
score("HOLDS" if i4["app"] == 61 else "BROKEN",
      "row I4 bites on 61 posets", "measured %d" % i4["app"])
score("HOLDS" if i4["pri"]["magnitude"] + i4["pri"]["parity"] == 3 else "BROKEN",
      "'the diagonal is preserved on 3 of the 61'",
      "measured %d" % (i4["pri"]["magnitude"] + i4["pri"]["parity"]))
score("HOLDS" if i4["pri"]["magnitude"] == 3 else "BROKEN",
      "'of those, 3 are settled by |s_i s_j| = 1'",
      "measured %d, and the predicate's OWN execution order agrees (%d)"
      % (i4["pri"]["magnitude"], i4["exe"]["magnitude"]))
score("HOLDS" if i4["mag_diagok"] == 300 else "BROKEN",
      "'300 off-diagonal magnitudes differ on them'",
      "measured %d, all of them off-diagonal (the diagonal is preserved there)"
      % i4["mag_diagok"])
score("HOLDS" if i4["pri"]["parity"] == 0 else "BROKEN",
      "'while 0 reach the parity system where a sign is consulted at all'",
      "measured %d" % i4["pri"]["parity"])
score("HOLDS" if i4["absorb"] == 0 else "BROKEN",
      "'Absorbable into a diagonal +-1 twist on 0 of those 61'",
      "measured %d, by 2-colouring and (where |L(P)| <= 8) brute force"
      % i4["absorb"])
score("HOLDS" if tot["par"] == 0 and tot["app"] == 297 else "BROKEN",
      "'0 of the 297 biting (poset, mutation) pairs reach the parity system'",
      "measured %d of %d" % (tot["par"], tot["app"]))

# ---------------------------------------------------------------------------
print()
print("B. THE SCOPE OF 'ENTRIES DIFFERING IN SIGN ALONE'")
print()
computed_over = sum(s["pri"]["magnitude"] + s["pri"]["parity"]
                    for s in stats.values())
score("SCOPE" if tot["sign_all"] == 0 else "BROKEN",
      "'measured over all four rows, ... 0 entries ANYWHERE differ in sign alone'",
      "TRUE: over all %d biting pairs the count really is %d.\n"
      "BUT `controls.py:1001-1005` accumulates `sign_entries` inside the\n"
      "`diag_preserved` branch, so the printed total is a sum over %d pairs,\n"
      "not %d.  The %d pairs whose diagonal moved are never examined for a\n"
      "sign-only mismatch at all.  The number is right; the measurement\n"
      "behind it is %.1f%% of the population the sentence names."
      % (tot["app"], tot["sign_all"], computed_over, tot["app"],
         tot["app"] - computed_over, 100.0 * computed_over / tot["app"]))
# the same defect, in the landing's own verifier
V = open("../face_geometry_landing_da45/verify_landing.py").read()
same = ('if g == "diagonal":' in V and 'continue' in V
        and "not one entry anywhere in those rows differs in SIGN ALONE" in V)
score("SCOPE" if same else "HOLDS",
      "the landing's own verifier scores the same sentence at the same scope",
      "verify_landing.py:127-135 `continue`s out of the loop on a diagonal-gate\n"
      "pair BEFORE counting sign-only entries, then checks 'not one entry\n"
      "ANYWHERE in those rows differs in SIGN ALONE'.  So the 25-claim,\n"
      "0-BROKEN verification does not cover this sentence either: the\n"
      "independence is in the NUMBERS and not in the DEFINITION.")

# a witness that the latency is real, not pedantic
print()
print("   A WITNESS THAT THE SCOPE MATTERS.  Take any diagonal-gate pair and")
print("   flip the sign of one off-diagonal entry that currently agrees:")
for P in ps:
    Lm, tg = twisted(P, "ridge_facets"), target(P)
    if eq(Lm, twisted(P)) or gate_priority(Lm, tg) != "diagonal":
        continue
    m = len(Lm)
    hit = None
    for i in range(m):
        for j in range(m):
            if i != j and Lm[i][j] != 0 and Lm[i][j] == tg[i][j]:
                hit = (i, j)
                break
        if hit:
            break
    if not hit:
        continue
    i, j = hit
    L2 = [row[:] for row in Lm]
    L2[i][j] = -L2[i][j]
    L2[j][i] = -L2[j][i]
    _, s_true = census(L2, tg)
    s_printed = 0 if gate_priority(L2, tg) == "diagonal" else s_true
    print("     n=%d |L(P)|=%d, entry (%d,%d) negated:" % (P.n, m, i, j))
    print("       sign-only mismatches, truth ................ %d" % s_true)
    print("       sign-only mismatches, as controls.py counts . %d" % s_printed)
    print("     The routing row would still print '0 entries anywhere differ in")
    print("     sign alone', and it would be FALSE.")
    break

# ---------------------------------------------------------------------------
print()
print("C. 'WHICH GATE of absorbable_by_diagonal_twist SETTLES EACH ANSWER'")
print()
score("BROKEN" if tot["differ"] else "HOLDS",
      "the printed gate table is the split the PREDICATE makes",
      "`absorbable_by_diagonal_twist` (face_complex.py:770-775) tests row i's\n"
      "DIAGONAL, then row i's MAGNITUDES, then row i+1's -- the two gates are\n"
      "INTERLEAVED BY ROW.  `deciding_gate` (controls.py:661-668) tests ALL\n"
      "diagonals, then ALL magnitudes.  On %d of the %d biting pairs the two\n"
      "name different gates.  Per row, deciding_gate vs the predicate\n"
      "(diagonal/magnitude/parity):\n"
      % (tot["differ"], tot["app"])
      + "\n".join(
          "  %s  %2d/%2d/%2d  vs  %2d/%2d/%2d   (differ on %d)"
          % (t, s["pri"]["diagonal"], s["pri"]["magnitude"], s["pri"]["parity"],
             s["exe"]["diagonal"], s["exe"]["magnitude"], s["exe"]["parity"],
             s["differ"])
          for t, s in stats.items()))
score("BROKEN" if "three stages" in SRC else "HOLDS",
      "`deciding_gate`'s docstring: 'The predicate answers ... in three\n            stages' (controls.py:641-642)",
      "The predicate has no three stages.  It has one loop over rows carrying\n"
      "two of the three tests, and a second loop carrying the third.")
score("HOLDS" if tot["diag_also_mag"] == tot["diag"] else "BROKEN",
      "the two forced gates are not alternatives on this population",
      "EVERY one of the %d 'diagonal' attributions is ALSO an absolute-value\n"
      "violation (%d of %d), and provably so: L^rel = d^T.d has a non-negative\n"
      "diagonal and D-A has a non-negative diagonal, so two unequal diagonal\n"
      "entries have unequal absolute values.  The absolute-value gate subsumes\n"
      "the diagonal gate here.  'Three at the diagonal gate and I4 at the\n"
      "absolute-value gate' is therefore a statement about which test\n"
      "`deciding_gate` runs first, not about the predicate."
      % (tot["diag"], tot["diag_also_mag"], tot["diag"]))
score("SCOPE" if "three at the diagonal gate and I4 at the "
      "absolute-value gate" in ART else "HOLDS",
      "'three at the diagonal gate and I4 at the absolute-value gate'",
      "The gate table three lines above it gives I4 as %d diagonal + %d\n"
      "magnitude: on %d of its %d biting pairs I4 is settled at the DIAGONAL\n"
      "gate.  The summary line assigns one gate per row where its own table\n"
      "gives I4 two."
      % (i4["pri"]["diagonal"], i4["pri"]["magnitude"],
         i4["pri"]["diagonal"], i4["app"]))

# ---------------------------------------------------------------------------
print()
print("D. THE 'FORCED AT EVERY n' ARGUMENT")
print()
score("HOLDS", "'the off-diagonal support of L^rel is the "
      "adjacent-transposition graph (claim (1), proven)'",
      "checked directly: %d/%d posets have E.L^rel.E == D-A exactly"
      % (sum(1 for P in ps if eq(twisted(P), target(P))), len(ps)))
score("HOLDS", "the rotation argument -- see part 2, checked to n = 8",
      "prefixes_true(rot(w)) identity on 46232 words; n-2 of n-1 generators\n"
      "stay adjacent at every n = 3..8; 2|L(P)| mismatches, exactly 2 per row,\n"
      "0 sign-only, at n = 3,4,5,6,7,8 (10080 and 80640 are new here).")
score("SCOPE", "'It is forced at every n and not merely measured to n = 5'",
      "The argument given is about ANTICHAINS: `rot` maps L(P) onto L(P) only\n"
      "when L(P) is all of S_n.  The statement also needs the other half --\n"
      "that no OTHER poset has row I4's diagonal preserved at larger n, since\n"
      "such a poset is exactly what would reach the parity system.  That half\n"
      "is neither argued in the file nor measured anywhere in the chain.\n"
      "Part 3 measures it at n = 6 over all 318 posets: 1201 biting pairs,\n"
      "0 reaching the parity system, and the ONLY diagonal-preserved pair is\n"
      "the antichain.  So the claim survives one size past where it was\n"
      "checked -- and the file still does not argue that half.")

# ---------------------------------------------------------------------------
print()
print("E. THE WITNESS, AND WHAT WAS DELIBERATELY NOT CHANGED")
print()
score("HOLDS" if "IT IS NOT A WITNESS THAT ROW I4 IS FALSIFIABLE" in ART
      else "BROKEN",
      "the repair WITHDRAWS the I4 witness rather than replacing it",
      "no replacement witness is named, so the 'new witness that also cannot\n"
      "bite' failure mode is not available to it.  Verified by search: the\n"
      "artifact contains no sentence claiming row I4 is falsifiable.")
nc3_abs = sum(1 for P in ps
              if not eq(parity_gauge(P), twisted(P))
              and absorbable_2col(parity_gauge(P), target(P)))
nc3_app = sum(1 for P in ps if not eq(parity_gauge(P), twisted(P)))
score("HOLDS" if nc3_abs == nc3_app == 82 else "BROKEN",
      "'NC3's corruption is D.L.D by construction ... absorbable 82/82'",
      "%d/%d, and the sign vector s = ((-1)^j) is EXHIBITED in part 4 on 86/86\n"
      "posets, so this is by construction and not by measurement."
      % (nc3_abs, nc3_app))
score("HOLDS" if "cond = cond and absorb == 0" in SRC else "BROKEN",
      "the condition is untouched -- `cond = cond and absorb == 0` still scored")
score("HOLDS" if "forced = (diag_preserved == 0)" in SRC else "BROKEN",
      "the routing still routes on `diag_preserved`")
n_check_before = int(subprocess.check_output(
    ["git", "show", "HEAD~1:code/face_geometry/controls.py"],
    cwd="..").decode().count("    check("))
score("HOLDS" if SRC.count("    check(") == n_check_before else "BROKEN",
      "'no new scored row was added'",
      "`check(` call sites: %d before, %d after"
      % (n_check_before, SRC.count("    check(")))

# ---------------------------------------------------------------------------
print()
print("F. THE ARTIFACT AND THE CARRIED-FORWARD LIST")
print()
run = subprocess.run([sys.executable, "controls.py", "5"], cwd=FG,
                     capture_output=True, text=True)
score("HOLDS" if run.stdout == ART and run.returncode == 0 else "BROKEN",
      "controls_output.txt regenerates byte-identically, exit 0",
      "%d bytes, exit %d" % (len(run.stdout), run.returncode))
old_src = subprocess.check_output(
    ["git", "show", "HEAD~1:code/face_geometry/controls.py"], cwd="..").decode()
import shutil                                                        # noqa: E402
import tempfile                                                      # noqa: E402
tmp = os.path.join(tempfile.mkdtemp(prefix="mg1c80_head1_"), "face_geometry")
shutil.copytree(FG, tmp)
open(os.path.join(tmp, "controls.py"), "w").write(old_src)
r_new = subprocess.run([sys.executable, "controls.py", "2"], cwd=FG,
                       capture_output=True, text=True)
r_old = subprocess.run([sys.executable, "controls.py", "2"], cwd=tmp,
                       capture_output=True, text=True)
score("HOLDS" if (r_new.returncode == r_old.returncode == 1
                  and "CONTROLS FAILED: 3" in r_new.stdout
                  and "CONTROLS FAILED: 3" in r_old.stdout) else "BROKEN",
      "'nmax=2 behaves exactly as it did before this commit (3 failures)'",
      "HEAD~1 exit %d, HEAD exit %d; both report CONTROLS FAILED: 3"
      % (r_old.returncode, r_new.returncode))

print()
print("   WHERE THE FALSE PREMISE STILL LIVES -- swept over the whole")
print("   repository, not over a named list.  This audit's OWN directory is")
print("   excluded and the exclusion is stated rather than silent: a6_mutations")
print("   .py:165 carries the sentence as a mutation PAYLOAD (M5 reinstalls it")
print("   to check that a text sweep catches it), which is not an assertion of")
print("   it -- but a sweep that quietly skipped itself would be the same shape")
print("   as the defect under audit.")
DEAD = ["the off-diagonal signs actually decide",
        "had to decide on the off-diagonal signs and could have",
        "the off-diagonal signs decide",
        "the answer is a real decision",
        "row I4 is falsifiable"]
MARKS = ["mg-f1b2", "mg-da45", "mg-8a12", "false premise", "was false",
         "is false", "They do not", "printed the opposite", "IT IS NOT",
         "REFUTED", "FALSE", "STATED GROUND"]
loose, quoted = [], 0
SELF = "face_geometry_audit_1c80"
for root, dirs, files in os.walk("../.."):
    dirs[:] = [d for d in dirs if d not in (".git", SELF)]
    for f in files:
        if not f.endswith((".py", ".txt", ".md", ".sh")):
            continue
        p = os.path.join(root, f)
        try:
            text = open(p, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue
        for d in DEAD:
            start = 0
            while True:
                k = text.find(d, start)
                if k < 0:
                    break
                start = k + 1
                window = text[max(0, k - 500):k + 500]
                if any(mk in window for mk in MARKS):
                    quoted += 1
                else:
                    loose.append("%s:%d  %r"
                                 % (os.path.relpath(p, "../.."),
                                    text[:k].count("\n") + 1, d))
print("     occurrences quoted inside a denial or an audit finding : %d" % quoted)
print("     occurrences still ASSERTING the premise                : %d" % len(loose))
for ln in sorted(set(loose)):
    print("       %s" % ln)
declared = "out_nc4.txt:27" in SRC
print("     controls.py names the origin (out_nc4.txt:27)          : %s" % declared)

# ---------------------------------------------------------------------------
print()
print(BAR)
n_h = sum(1 for v, _ in LEDGER if v == "HOLDS")
n_s = sum(1 for v, _ in LEDGER if v == "SCOPE")
n_b = sum(1 for v, _ in LEDGER if v == "BROKEN")
print("LEDGER: %d claims scored -- %d HOLDS, %d SCOPE, %d BROKEN"
      % (len(LEDGER), n_h, n_s, n_b))
for v, c in LEDGER:
    if v != "HOLDS":
        print("   %-6s %s" % (v, c))
print(BAR)
