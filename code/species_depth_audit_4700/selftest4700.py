"""SELF-TEST for the mg-4700 instrument.

Every number this audit reports rests on three things being true, and none of
them is obvious:

  1.  THE RESTORE CONTRACT.  Each probe edits the real worktree.  If a restore
      is silently incomplete, every later probe measures a different tree and
      the whole transcript is worthless.  So the contract is tested here, in
      both directions: a probe that puts the tree back must compare EQUAL, and
      a probe that does NOT must RAISE.  A restore checker only ever seen to
      pass is worth nothing.

  2.  THE PIN.  `PRE_REPAIR` must not already carry the repair.  mg-821e's
      `41ac5d4` is the whole reason this assertion exists: two of its
      comparisons were anchored on `HEAD` and stopped comparing the moment the
      repair landed, reporting the pre-repair checker as already fixed.  A pin
      later moved onto a repaired commit must be a LOUD failure and not a quiet
      agreement.

  3.  THE COPIED HELPERS.  `flat`, `delete_at` and `unwire` are copies of, or
      surgery on, the subjects' own logic.  If a copy drifts, the probe that
      uses it stops testing what its label says.

    python3 code/species_depth_audit_4700/selftest4700.py
"""

import os
import shutil
import sys
import tempfile

from kern4700 import (REPO, PRE_REPAIR, REPAIR, sh, git_state, Probe,
                      RestoreFailed, flat, regions, needle_re, delete_at,
                      unwire, WIRE_MARK, CALL_AND_GUARD, CALL_ONLY, PRINTING,
                      predict)

n = bad = 0


def ck(label, cond, detail=""):
    global n, bad
    n += 1
    if not cond:
        bad += 1
        print("*** FAILED *** %s %s" % (label, detail))


RUNNERS = ["code/species_repair_a4ef/run_all.sh",
           "code/species_remainder_f8fa/run_all.sh",
           "code/species_repair_6f61/run_all.sh"]
WALKS = ["code/species_remainder_f8fa/w3_scope.py",
         "code/species_repair_a4ef/s1_extent.py",
         "code/species_extent_d633/e1_extents.py"]

# -- 1.  flat() -------------------------------------------------------------
ck("flat collapses runs", flat("a   b\n\nc") == "a b c")
ck("flat strips blockquote markers", flat("> a\n> b") == "a b")
ck("flat strips nested blockquotes", flat(">> a\n>> b") == "a b")
ck("flat strips ends", flat("  a  ") == "a")
ck("flat is idempotent", flat(flat("> a\n  b ")) == flat("> a\n  b "))
ck("flat joins a wrapped needle", flat("2 of\n45") == "2 of 45")

# -- 2.  needle_re ----------------------------------------------------------
ck("needle_re matches plain", bool(needle_re("2 of 45").search("x 2 of 45 y")))
ck("needle_re matches wrapped", bool(needle_re("2 of 45").search("2 of\n45")))
ck("needle_re escapes dots",
   not needle_re("a.c").search("abc"))
ck("needle_re counts every copy",
   len(needle_re("mg-a61f").findall("mg-a61f mg-a61f")) == 2)

# -- 3.  regions ------------------------------------------------------------
DOCX = ["# A\n", "body\n", "## B\n", "b1\n", "### B1\n", "deep\n", "## C\n"]
R = regions(DOCX)
ck("regions finds every heading", len(R) == 4, [h for h, _a, _b in R])
ck("a region stops at the next heading of ANY level",
   "".join(DOCX[R[1][1]:R[1][2]]) == "## B\nb1\n")
ck("the last region runs to EOF", R[-1][2] == len(DOCX))
ck("regions are contiguous",
   all(R[i][2] == R[i + 1][1] for i in range(len(R) - 1)))

# -- 4.  delete_at ----------------------------------------------------------
T = "# A\nx mg-a61f x\n## B\nmg-a61f and mg-a61f\n"
new, removed, left = delete_at(T, "mg-a61f", r"^## B")
ck("delete_at removes every copy at the site", removed == 2)
ck("delete_at leaves the other site alone", left == 1, left)
ck("delete_at leaves the other site's TEXT alone", "x mg-a61f x" in new)
ck("delete_at on a missing site returns None",
   delete_at(T, "mg-a61f", r"^## NOPE")[0] is None)
new2, rem2, left2 = delete_at("# A\na\n", "zzz", r"^# A")
ck("delete_at with no copies removes nothing", rem2 == 0 and new2 == "# A\na\n")

# -- 5.  the wiring block, and the parts ------------------------------------
for rel in RUNNERS:
    text = open(os.path.join(REPO, rel), encoding="utf-8").read()
    ck("%s carries the wiring marker" % rel, WIRE_MARK in text)
    ck("%s carries the call and guard verbatim" % rel, CALL_AND_GUARD in text)
    ck("%s carries the printing verbatim" % rel, PRINTING in text)
    ck("%s: unwire removes the marker" % rel, WIRE_MARK not in unwire(text))
    ck("%s: unwire removes the call" % rel,
       "e2_crosssection.py" not in unwire(text))
    ck("%s: unwire is a SUFFIX-preserving cut" % rel,
       text.replace(CALL_AND_GUARD, "").replace(PRINTING, "")
       .count("set -e") == unwire(text).count("set -e"))
    ck("%s: CALL_ONLY is the call without the guard" % rel,
       CALL_ONLY.strip() in CALL_AND_GUARD)

# -- 6.  the pin --------------------------------------------------------------
# The pin must be BEFORE the repair.  Asserted in both directions: the
# pre-repair ref must NOT carry the repair, and the repair ref MUST.
for rel in RUNNERS:
    rc, old, _ = sh(["git", "show", "%s:%s" % (PRE_REPAIR, rel)])
    ck("pin %s: %s available" % (PRE_REPAIR, rel), rc == 0)
    ck("pin does not already carry the wiring: %s" % rel, WIRE_MARK not in old)
    rc, new_, _ = sh(["git", "show", "%s:%s" % (REPAIR, rel)])
    ck("the repair ref DOES carry the wiring: %s" % rel, WIRE_MARK in new_)
    ck("unwire(HEAD) == the pinned file, byte for byte: %s" % rel,
       unwire(open(os.path.join(REPO, rel), encoding="utf-8").read()) == old)

rc, oldchk, _ = sh(["git", "show", "%s:code/species_repair_6f61/check_doc.py"
                    % PRE_REPAIR])
ck("pin: check_doc.py is the PRESENCE version",
   "EVERY ANCHOR AT ITS OWN SITE" not in oldchk and "flat(rep)" in oldchk)
# Per file, and NOT a bare `os.walk not in` -- `e1_extents.py` already walked
# `docs/` and `code/` for its markdown sweep before this repair, so the coarse
# form of this assertion fails against a correct pin and would have been
# "fixed" by weakening it.  The needle is the ONE call each repair changed.
WALK_CALL = {
    "code/species_remainder_f8fa/w3_scope.py": "os.walk(SRC)",
    "code/species_repair_a4ef/s1_extent.py": "os.walk(root)",
    "code/species_extent_d633/e1_extents.py": "in os.walk(root):",
}
for rel in WALKS:
    rc, oldw, _ = sh(["git", "show", "%s:%s" % (PRE_REPAIR, rel)])
    call = WALK_CALL[rel]
    ck("pin: %s's scan does not recurse yet" % rel, call not in oldw)
    ck("pin: %s's scan is a listdir" % rel, "os.listdir" in oldw)
    cur = open(os.path.join(REPO, rel), encoding="utf-8").read()
    ck("HEAD: %s's scan recurses" % rel, call in cur)

# -- 7.  the restore contract, BOTH directions -------------------------------
before = git_state()
with Probe("selftest: plant") as pr:
    p = pr.plant("code/species_7d75/selftest_sub/x.md", "planted\n")
    ck("plant creates the file", os.path.isfile(p))
    ck("plant creates the parent", os.path.isdir(os.path.dirname(p)))
    ck("the tree is DIRTY inside the probe", git_state() != before)
ck("plant restored: state equal", git_state() == before)
ck("plant restored: parent gone",
   not os.path.exists(os.path.join(REPO, "code/species_7d75/selftest_sub")))

with Probe("selftest: edit") as pr:
    pr.edit("code/species_7d75/run_all.sh", "set -e", "set -eu")
    ck("edit applied",
       "set -eu" in open(os.path.join(REPO, "code/species_7d75/run_all.sh"),
                         encoding="utf-8").read())
    ck("edit shows in the DIFF channel", git_state()[1] != before[1])
ck("edit restored: state equal", git_state() == before)

tmpd = tempfile.mkdtemp(prefix="st4700_")
try:
    with Probe("selftest: symlink") as pr:
        lp = pr.symlink("code/species_7d75/selftest_link", tmpd)
        ck("symlink created", os.path.islink(lp))
        ck("symlink shows in the PORCELAIN channel", git_state()[0] != before[0])
    ck("symlink restored: state equal", git_state() == before)
finally:
    shutil.rmtree(tmpd, ignore_errors=True)

# edit with the wrong count must refuse rather than mutate something else
try:
    with Probe("selftest: bad count") as pr:
        pr.edit("code/species_7d75/run_all.sh", "set -e", "x", count=99)
    ck("edit with a wrong count raises", False)
except AssertionError:
    ck("edit with a wrong count raises", True)
ck("refused edit left the tree alone", git_state() == before)

# AND THE OTHER DIRECTION: a probe that does not restore must RAISE.  Without
# this row the restore contract is a check only ever seen to pass.
print("  (the next two lines on stderr are DELIBERATE: the restore contract")
print("   is being tested in the direction that must fail)")
raised = False
try:
    with Probe("selftest: sabotaged restore") as pr:
        pr.plant("code/species_7d75/selftest_sab/y.md", "x\n")
        pr.created = []          # forget it, on purpose
except RestoreFailed:
    raised = True
finally:
    shutil.rmtree(os.path.join(REPO, "code/species_7d75/selftest_sab"),
                  ignore_errors=True)
ck("a probe that fails to restore RAISES", raised)
ck("and the sabotage was cleaned up by hand", git_state() == before)

# -- 8.  predict() ------------------------------------------------------------
import io
_out = sys.stdout
sys.stdout = io.StringIO()
a = predict("T1", "x", "x", True)
b = predict("T2", "x", "y", False)
cap = sys.stdout.getvalue()
sys.stdout = _out
ck("predict returns 0 on a hit", a == 0)
ck("predict returns 1 on a miss", b == 1)
ck("predict prints the miss loudly", "*** MISSED ***" in cap)
ck("predict prints the prediction as well as the result",
   "predicted" in cap and "got" in cap)

# -- 9.  the environment ------------------------------------------------------
rc, out, _ = sh([sys.executable, "-c",
                 "import os;print(os.environ.get('PYTHONDONTWRITEBYTECODE'))"])
ck("children run with PYTHONDONTWRITEBYTECODE", out.strip() == "1")

print("selftest4700: %d assertion(s), %d failed" % (n, bad))
sys.exit(1 if bad else 0)
