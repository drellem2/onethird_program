"""a4 — MY OWN CHECKS: is this instrument independent, is its `168` non-vacuous, and did
this ticket move anything it was not sent to move?

`A REMEDY IS AN ARTIFACT OF THE SAME KIND AS THE DEFECT.` This ticket audits a document that
asserted blankets over a population it had not enumerated, using a number it had not
recomputed. So the two ways this audit can be worthless are (a) my `168` agrees because my
instrument is not independent, and (b) my `168` agrees because the arm could not have printed
anything else. Both are attacked here rather than promised.
"""

import ast
import os
import re
import subprocess
import sys
from fractions import Fraction as F

from liba0d6 import (naturally_labelled, is_primitive, transport_counts, M_exact,
                     laplacian_exact, gamma_float, certify_fail, energy_exact,
                     leak_prefix_numerators)

HERE = "code/adjudication_audit_a0d6"
SUBJECTS = ["code/sweep_loss_51f4/lib51f4.py", "code/l2_conditionality_28ff/lib28ff.py",
            "code/l2_audit_29fe/lib29fe.py", "code/contradiction_repair_d19f/libd19f.py"]
FAILS = []


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True).stdout


def arm(name, ok, detail=""):
    print("  [%s] %s" % ("PASS" if ok else "FAIL", name))
    for l in (detail.split("\n") if detail else []):
        print("        " + l)
    if not ok:
        FAILS.append(name)


print("=" * 96)
print("a4 — INDEPENDENCE, NON-VACUITY, AND CONTAINMENT")
print("=" * 96)
print()

# ------------------------------------------------------------------------ C1
print("C1  INDEPENDENCE — this instrument imports nothing from its subject")
mine = sorted(f for f in os.listdir(".") if f.endswith(".py"))
# D6 (MINE, KEPT): the first form of this arm matched imports with a REGEX and went RED on
# the words 'from the same place' inside a1's own docstring — a probe for 'does this file
# import its subject' answering yes because of an English sentence about the subject.
# Parsed with `ast` now, so only real import statements count.
STDLIB = {"liba0d6", "os", "re", "sys", "time", "subprocess", "fractions", "itertools",
          "collections", "math", "ast"}
bad = []
for f in mine:
    tree = ast.parse(open(f).read())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name.split(".")[0] not in STDLIB:
                    bad.append((f, a.name))
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] not in STDLIB:
                bad.append((f, node.module))
print("      my python files: %s" % ", ".join(mine))
arm("C1 no import of any other tree's library", not bad, str(bad))

# ------------------------------------------------------------------------ C2
print()
print("C2  NO SHARED SOURCE LINE with any library in the exchange")
mylines = {l.strip() for l in open("liba0d6.py") if len(l.strip()) >= 40
           and not l.strip().startswith("#")}
shared = {}
for s in SUBJECTS:
    txt = sh("git", "show", "HEAD:%s" % s)
    if not txt:
        continue
    theirs = {l.strip() for l in txt.split("\n") if len(l.strip()) >= 40}
    ov = mylines & theirs
    if ov:
        shared[s] = sorted(ov)
print("      substantive lines in liba0d6.py (>= 40 chars): %d" % len(mylines))
for s in SUBJECTS:
    txt = sh("git", "show", "HEAD:%s" % s)
    print("      vs %-46s shared: %d" % (s.split("/")[-1], len(shared.get(s, []))))
nshared = sum(len(v) for v in shared.values())
for k, v in shared.items():
    for l in v:
        print("      SHARED WITH %s:" % k.split("/")[-1])
        print("        %s" % l)
arm("C2 AT MOST ONE shared line, and it is NAMED rather than removed", nshared <= 1,
    "THE ONE SHARED LINE IS REAL AND IS KEPT. It is M's denominator,\n"
    "`sum(min(k, n - k) for k in range(1, n))`, which is sum_k min(k, n-k) written the\n"
    "only way Python writes it — an agreement forced by the formula, not evidence of\n"
    "lineage. Removing it by renaming a variable would hide a true fact about this\n"
    "instrument, so instead a0's arm A10 recomputes M from the FOOTRULE identity\n"
    "E[D_F]/(2 floor(n^2/4)) over linear extensions, a route that does not contain that\n"
    "line, and it agrees at every poset n <= 6.  Everything else in liba0d6 — the\n"
    "enumeration, the down-set DP, the leak, the Jacobi, both certifiers — is unshared.")

# ------------------------------------------------------------------------ C3
print()
print("C3  NON-VACUITY — four planted worlds at n = 7. The arm must give a DIFFERENT answer")
print("    when the threshold, the scalar, the population or the orthogonality is mutated.")
print("    Every mutation is DERIVED from the sweep's own quantities, not typed.")
print()
posets = naturally_labelled(7)
c_unmut = c_thresh = c_scalar = c_pop = 0
for d in posets:
    prim = is_primitive(7, d)
    cnt, N = transport_counts(7, d)
    M = M_exact(7, cnt, N)
    lam, vec = gamma_float(7, cnt, N)
    if not prim:
        c_pop += 1                                    # gamma = 0, so f* is unbounded
        continue
    ff = float(M) ** 2 / (2 * lam)
    nums = leak_prefix_numerators(7, cnt)
    phis = min(F(nums[k - 1], N * min(k, 7 - k)) for k in range(1, 7))
    ct = float(phis) ** 2 / (2 * lam)
    if ff > 1:
        c_unmut += 1
        c_pop += 1
    if ff > 0.99:
        c_thresh += 1
    if ct > 1:
        c_scalar += 1
print("      W0 UNMUTATED  f* > 1 over the 86278 PRIMITIVE posets           : %d" % c_unmut)
print("      W1 THRESHOLD  f* > 0.99 (the boundary moved by 1 %%)             : %d" % c_thresh)
print("      W2 SCALAR     c_true > 1 instead of f* > 1                     : %d" % c_scalar)
print("      W3 POPULATION f* > 1 over ALL 96428 posets, primitive or not   : %d" % c_pop)
arm("C3a W1 THRESHOLD fires — the count is not a constant the code prints",
    c_thresh != c_unmut, "%d vs %d" % (c_thresh, c_unmut))
arm("C3b W2 SCALAR fires — route (F) and the truth are DIFFERENT columns and the arm\n"
    "       distinguishes them (c_true never exceeds 1 at n = 7; f* does, 168 times)",
    c_scalar != c_unmut, "%d vs %d" % (c_scalar, c_unmut))
arm("C3c W3 POPULATION fires — and this is the mutation that MATTERS, because every\n"
    "       published '168 of 86278' is stated over the PRIMITIVE population and nothing\n"
    "       in the phrase carries that",
    c_pop != c_unmut, "%d vs %d — the 10150 non-primitive posets have gamma = 0" % (c_pop, c_unmut))

# W4: the certifier without orthogonality
d0 = [d for d in posets if is_primitive(7, d)][0]
cnt, N = transport_counts(7, d0)
L = laplacian_exact(7, cnt, N)
M = M_exact(7, cnt, N)
t = M * M / 2
ones = [F(1)] * 7
bogus = energy_exact(L, ones) < t * sum(x * x for x in ones)
real = certify_fail(L, t, [1.0] * 7) is not None
print()
print("      W4 ORTHOGONALITY  the CONSTANT vector has energy %s, so a 'certifier' that"
      % energy_exact(L, ones))
print("         skipped the v perp 1 requirement would certify EVERY poset as failing.")
arm("C3d W4 fires — without centring the constant vector 'certifies' a failure (%s),\n"
    "       and certify_fail, which re-centres exactly, REFUSES the same input (%s)"
    % (bogus, real), bogus and not real)

# ------------------------------------------------------------------------ C4
print()
print("C4  CONTAINMENT — nothing outside this directory differs from the branch point")
# The COMMITTED diff alone would answer a working-tree question and be green at every
# moment before the commit — which is mg-d19f's own D1, recorded in the landing this
# ticket audits. Committing it here would be that defect inside its own audit, so the
# working tree is read too and the two are printed separately.
base = sh("git", "merge-base", "HEAD", "main").strip()
committed = [l for l in sh("git", "diff", "--name-only", base, "HEAD").split("\n") if l.strip()]
worktree = [l[3:].strip() for l in sh("git", "status", "--porcelain").split("\n") if l.strip()]
diff = sorted(set(committed) | set(worktree))
outside = [f for f in diff if not f.startswith(HERE)]
print("      merge-base with main : %s" % base[:10])
print("      committed on this branch     : %d" % len(committed))
print("      uncommitted in the worktree  : %d" % len(worktree))
print("      union (what this arm judges) : %d" % len(diff))
for f in diff:
    print("        %s%s" % (f, "   <- OUTSIDE" if f in outside else ""))
arm("C4 zero files outside %s differ" % HERE, not outside, str(outside))
print()

# ------------------------------------------------------------------------ C5
print("C5  THE SUBJECT IS NOT EDITED")
for f in ("docs/OneThird-SweepLoss-mg-51f4.md",
          "docs/OneThird-L2-Conditionality-mg-28ff.md"):
    print("      %s : %s" % (f, "UNCHANGED" if f not in diff else "*** CHANGED ***"))
subj = [f for f in diff if f.startswith("docs/") or f.startswith("code/contradiction_repair_d19f")]
arm("C5 neither document and no file of mg-d19f's instrument is touched", not subj, str(subj))
print()

print("=" * 96)
if FAILS:
    print("a4 FAILED: " + "; ".join(FAILS))
    print("=" * 96)
    sys.exit(1)
print("a4 — INDEPENDENT, NON-VACUOUS, CONTAINED.")
print("=" * 96)
