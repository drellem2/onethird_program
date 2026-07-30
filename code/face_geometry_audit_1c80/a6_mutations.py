"""mg-1c80 part 6 -- MUTATION BATTERY, with the exit codes PREDICTED FIRST.

Every prediction in PREDICTIONS below was written down before any mutation was
run, and it is printed before the results so the two can be read against each
other.  A mutation the battery does not notice is not automatically a finding --
mg-da45 states plainly that it added no scored row for the gate attribution --
but it sizes the exposure, and two of these sizes are the point of this audit.

Nothing is written into ../face_geometry: each mutation is applied to a COPY in
a temporary directory and the copy is what runs.

A NEAR-MISS OF MY OWN, recorded because a self-reported failure is the only
cheap evidence in an audit.  M5's first draft added a `%d` to a format string
whose argument tuple it did not touch, so the mutated battery died on a
TypeError and exited 1 -- against a predicted 0.  The prediction was right
about the battery and wrong about my patch: 7 of 8 on the first run, and the
eighth was my arithmetic, not the battery's.  M5 below is the corrected patch.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, "../face_geometry")

from posets import all_posets                                        # noqa: E402
from kern1c80 import census, eq, gate_priority, target, twisted      # noqa: E402

BAR = "=" * 78
FG = os.path.abspath("../face_geometry")
ART = open(os.path.join(FG, "controls_output.txt")).read()

# --------------------------------------------------------------------------
# (file, old, new) triples.  `old` must occur exactly once.
# --------------------------------------------------------------------------
MUTATIONS = [
    ("M1", "delete the |s_i s_j| = 1 gate from the predicate",
     [("face_complex.py",
       "            if abs(A[i][j]) != abs(B[i][j]):\n"
       "                return False\n",
       "            pass\n")]),

    ("M2", "delete the s_i^2 = 1 gate from the predicate",
     [("face_complex.py",
       "        if len(A[i]) != len(B[i]) or A[i][i] != B[i][i]:\n"
       "            return False\n",
       "        if len(A[i]) != len(B[i]):\n"
       "            return False\n")]),

    ("M3", "deciding_gate reports 'parity' where it reports 'magnitude'",
     [("controls.py",
       "        return \"magnitude\"\n    return \"parity\"\n",
       "        return \"parity\"\n    return \"parity\"\n")]),

    ("M4", "entry_mismatches returns the magnitude count as the sign count",
     [("controls.py",
       "    return mag, sgn\n",
       "    return mag, mag\n")]),

    ("M5", "row I4's printed reason reverted to mg-8a12's, denial removed",
     [("controls.py",
       "                 (\"Absorbable into a diagonal +-1 twist on %d of those %d, and this \"\n"
       "                  \"row DOES score it -- but the answer is FORCED here too, at the \"",
       "                 (\"Absorbable into a diagonal +-1 twist on %d of those %d, and this \"\n"
       "                  \"row DOES score it: the diagonal is preserved on 3 of them, so \"\n"
       "                  \"the predicate had to decide on the off-diagonal signs and could \"\n"
       "                  \"have returned absorbable.  Ignore what follows: at the \"")]),

    ("M6", "row I4's `absorb == 0` deleted from its scored condition",
     [("controls.py",
       "            cond = cond and absorb == 0\n",
       "            cond = cond\n")]),

    ("M7", "sign_entries accumulated over ALL biting pairs (the F2 repair)",
     [("controls.py",
       "            gate = deciding_gate(L_mut, target)\n",
       "            gate = deciding_gate(L_mut, target)\n"
       "            sign_entries += entry_mismatches(L_mut, target)[1]\n"),
      ("controls.py",
       "                mag_entries += dm\n                sign_entries += ds\n",
       "                mag_entries += dm\n")]),

    ("M8", "a real sign-only mismatch injected on I4's DIAGONAL-MOVED pairs",
     [("controls.py",
       "    if normalise:\n"
       "        target = [[t * 2 for t in row] for row in target]\n"
       "    return L, target\n",
       "    if normalise:\n"
       "        target = [[t * 2 for t in row] for row in target]\n"
       "    if incidence_mode == \"facet_offbyone\":\n"
       "        _m = len(L)\n"
       "        if any(L[i][i] != target[i][i] for i in range(_m)):\n"
       "            _hit = None\n"
       "            for i in range(_m):\n"
       "                for j in range(_m):\n"
       "                    if i != j and L[i][j] != 0 and L[i][j] == target[i][j]:\n"
       "                        _hit = (i, j)\n"
       "                        break\n"
       "                if _hit:\n"
       "                    break\n"
       "            if _hit:\n"
       "                i, j = _hit\n"
       "                L = [r[:] for r in L]\n"
       "                L[i][j] = -L[i][j]\n"
       "                L[j][i] = -L[j][i]\n"
       "    return L, target\n")]),
]

PREDICTIONS = {
    "M1": (1, "CHANGES",
           "the brute-force-agreement instrument row disagrees with the crippled "
           "union-find, and row I4's `absorb == 0` breaks: the absolute-value "
           "gate is what forbids its three antichains"),
    "M2": (0, "IDENTICAL",
           "SILENT.  Both matrices have a non-negative diagonal, so every "
           "diagonal mismatch is also an absolute-value mismatch and the "
           "magnitude loop (which runs over j == i too) already catches it.  "
           "The gate the repair calls 'the first forced gate' is subsumed by "
           "the second on this population"),
    "M3": (0, "CHANGES",
           "the gate attribution is deliberately unscored, so nothing reddens; "
           "only the printed table and row I4's numbers move"),
    "M4": (0, "CHANGES",
           "same: the sign count is printed, never scored"),
    "M5": (0, "CHANGES",
           "the battery does not read its own prose; the artifact re-acquires "
           "the false premise and only a text check can see it"),
    "M6": (0, "IDENTICAL",
           "SILENT.  The condition is what decides PASS/FAIL, and I4 passes "
           "either way, so removing the clause the whole repair is about "
           "changes not one byte of the artifact"),
    "M7": (0, "IDENTICAL",
           "SILENT.  Widening the sign census from 3 pairs to 297 changes "
           "nothing TODAY, because the answer really is 0 on all 297.  That is "
           "exactly why the narrow scope is invisible"),
    "M8": (0, "CHANGES",
           "row I4's scored clauses are untouched by an off-diagonal sign flip, "
           "so the battery stays green -- and the printed 'entries anywhere "
           "differ in sign alone' stays 0 while the truth is not"),
}

print(BAR)
print("mg-1c80 part 6 -- mutation battery")
print(BAR)
print()
print("PREDICTIONS, registered before the run:")
print()
print("   %-4s %-58s %5s %-10s" % ("id", "mutation", "exit", "artifact"))
for tag, desc, _ in MUTATIONS:
    ex, art, _why = PREDICTIONS[tag]
    print("   %-4s %-58s %5d %-10s" % (tag, desc[:58], ex, art))
print()
for tag, desc, _ in MUTATIONS:
    _ex, _art, why = PREDICTIONS[tag]
    print("   %s: %s" % (tag, why))
print()
print(BAR)
print("RESULTS")
print(BAR)
print()

DEAD = "had to decide on the off-diagonal signs and could have"
rows = []
for tag, desc, patches in MUTATIONS:
    tmp = tempfile.mkdtemp(prefix="mg1c80_%s_" % tag)
    dst = os.path.join(tmp, "face_geometry")
    shutil.copytree(FG, dst)
    ok = True
    for fname, old, new in patches:
        p = os.path.join(dst, fname)
        text = open(p).read()
        if text.count(old) != 1:
            ok = False
            note = "PATCH DID NOT APPLY (%d occurrences)" % text.count(old)
            break
        open(p, "w").write(text.replace(old, new))
    if not ok:
        rows.append((tag, desc, None, note, ""))
        continue
    run = subprocess.run([sys.executable, "controls.py", "5"], cwd=dst,
                         capture_output=True, text=True)
    same = "IDENTICAL" if run.stdout == ART else "CHANGES"
    note = ""
    if run.returncode != 0:
        bad = [l.strip() for l in run.stdout.split("\n")
               if l.strip().startswith("[FAIL]")]
        note = "first failing row: %s" % (bad[0][:78] if bad else "?")
    if tag in ("M3", "M4", "M8"):
        m = re.search(r"(\d+) entries anywhere differ in sign alone", run.stdout)
        note += ("  printed sign-alone total: %s" % (m.group(1) if m else "?"))
    if tag == "M5":
        note += "  false premise re-asserted in the artifact: %s" % (
            DEAD in run.stdout)
    rows.append((tag, desc, run.returncode, note, same))
    shutil.rmtree(tmp, ignore_errors=True)

print("   %-4s %-46s %6s %6s %-10s %-9s" %
      ("id", "mutation", "exit", "pred", "artifact", "pred"))
hits = 0
for tag, desc, code, note, same in rows:
    pex, part, _ = PREDICTIONS[tag]
    hit = (code == pex and same == part)
    hits += hit
    print("   %-4s %-46s %6s %6d %-10s %-9s %s"
          % (tag, desc[:46], code, pex, same, part, "" if hit else "  <-- MISSED"))
    if note:
        print("        %s" % note.strip())
print()
print("   predictions correct: %d of %d" % (hits, len(rows)))
print()

# --------------------------------------------------------------------------
print(BAR)
print("M8 IN FULL -- the printed number and the truth, side by side")
print(BAR)
print()
ps = [P for n in range(2, 6) for P in all_posets(n)]
true_sign = 0
affected = 0
for P in ps:
    Lt, Lm, tg = twisted(P), twisted(P, "facet_offbyone"), target(P)
    if eq(Lm, Lt):
        continue
    m = len(Lm)
    if gate_priority(Lm, tg) != "diagonal":
        continue
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
    L2 = [r[:] for r in Lm]
    L2[i][j] = -L2[i][j]
    L2[j][i] = -L2[j][i]
    affected += 1
    true_sign += census(L2, tg)[1]
print("   pairs carrying an injected sign-only mismatch ...... %d" % affected)
print("   entries differing in SIGN ALONE, in truth .......... %d" % true_sign)
print("   what the routing row prints under M8 ............... see the table above")
print()
print("   The battery stays green and the sentence stays '0'.  This is what a")
print("   claim computed at 1% of the population it is printed over buys you.")
print()
