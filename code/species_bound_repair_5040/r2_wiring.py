"""R2 -- OPEN 2.  The third structure the deletion test missed, and the answer.

mg-4700's F2 deleted the wiring block one part at a time and found two of its
three parts inert: the `|| { ...; exit 1; }` guard changed no verdict, because
`set -e` already aborts on a failed command substitution, and the two `echo`s
that printed the check's output could be removed with 3 of 3 runners exiting 0
and no trace the check ran.

REPORTED, WITH THE QUESTION mg-5040 ASKS OF IT.  The deletion test has now
missed at the GATE (mg-9220), at the RETURN, at the CLAUSE (mg-64b6) and here
at a MULTI-STATEMENT SHELL BLOCK.  Four levels, each found by the level below
it failing.  That is not a sequence of separate bugs; it is a test whose grain
is chasing the code's structure, and a grain that chases structure never
catches up -- the next level exists as soon as somebody writes a compound
statement the current grain does not split.

SO THE ANSWER IS NOT A FOURTH LEVEL.  This is a FLOOR, not a rung, and it is
reached by removing the structure: running the check and printing its output
are now ONE statement, so the block has exactly one separable part and that
part has the return.  Nothing was made finer.  Something was deleted.

R2c measures the claim in the only way that can fail: the parts are counted
BY SPLITTING THE FILE, at the pin and at HEAD, and each part is deleted alone.
"""

import os
import re
import sys

from kern5040 import (hdr, Probe, RUNNERS, REPO, PRE, sh, extract, git)

bad = 0
E2 = "code/species_extent_d633/e2_crosssection.py"
CALL = "python3 ../species_extent_d633/e2_crosssection.py"
LABEL = 'echo "cross-section check (mg-821e), its own output, unfiltered:"'

# B1: mg-7dd3's finding -- a claim struck in one section of a document and
# standing un-struck in another.  Restoring it is how a runner is made to go
# red for a REASON, so that a red run is attributable to the check and not to
# anything else in the runner.
#
# THE DOCUMENT IS CHOSEN SO THE RED IS ATTRIBUTABLE.  It carries a strike and
# is read by e2 -- which reads every *.md under docs/ and code/ -- and by NO
# other checker in the three runners: it belongs to the Bratteli arc and no
# species checker's extent contains it.  The first version of this probe
# appended to a document those runners' own checkers read, and 2 of 3 went red
# without
# printing STANDING UN-STRUCK, which is a red that proves nothing.
B1_DOC = "docs/OneThird-Bratteli-Path-Algebras-Where-This-Lives.md"


def runner(tree):
    return os.path.join(REPO, "code", tree, "run_all.sh")


def run_runner(tree, root=None):
    root = root or REPO
    return sh(["sh", "run_all.sh"], cwd=os.path.join(root, "code", tree))


def b1_text():
    """The struck claim, and the same claim restated un-struck.

    Taken from the document itself so that this probe cannot drift from what
    e2 actually looks for: the first strike in the document, repeated verbatim
    without the strike markers, in a later section.
    """
    p = os.path.join(REPO, B1_DOC)
    with open(p, encoding="utf-8") as f:
        text = f.read()
    strikes = [m.group(1) for m in re.finditer(r"~~([^~\n]+)~~", text)]
    strikes.sort(key=lambda s: -len(s.split()))
    return text, (strikes[0] if strikes and len(strikes[0].split()) >= 8
                  else None)


# ---------------------------------------------------------------------------
# R2a  the three runners, clean
# ---------------------------------------------------------------------------
hdr("R2a  THE THREE REWIRED RUNNERS, CLEAN")

print("  P2a.  Each runner's OWN stdout must carry the check's output.  A")
print("  call present in a script is not evidence of execution (mg-6cb9 F2),")
print("  so what is read below is the runner's stdout and not its source.")
print()
for t in RUNNERS:
    rc, out = run_runner(t)
    has = "E2 TOTAL BAD:" in out
    ok = rc == 0 and has
    bad += (not ok)
    print("  %-26s exit %d   prints `E2 TOTAL BAD:`  %-3s   %s"
          % (t, rc, "yes" if has else "NO", "ok" if ok else "*** ***"))
print()


# ---------------------------------------------------------------------------
# R2b  the same three with B1 restored -- the red must be attributable
# ---------------------------------------------------------------------------
hdr("R2b  B1 RESTORED ON DISK -- the runners must go red, and for this reason")

doc, claim = b1_text()
if not claim:
    print("  *** could not find a strike to restore in %s ***" % B1_DOC)
    bad += 1
    red = {}
else:
    print("  Restoring: a claim struck in one section, restated UN-STRUCK in")
    print("  another.  The restated text is taken from the document's own")
    print("  first strike, so this probe cannot drift from what e2 looks for.")
    print("  %s..." % claim[:64])
    print()
    with Probe("B1 restored") as pr:
        pr.write(B1_DOC, doc + "\n\n## mg-5040 R2b\n\n" + claim + "\n")
        red = {}
        for t in RUNNERS:
            rc, out = run_runner(t)
            red[t] = rc
            named = "STANDING UN-STRUCK" in out
            ok = rc == 1 and named
            bad += (not ok)
            print("  %-26s exit %d   names STANDING UN-STRUCK  %-3s  %s"
                  % (t, rc, "yes" if named else "NO", "ok" if ok else "***"))
    ok = pr.restored
    bad += (not ok)
    print()
    print("  %-58s %s" % ("the document was restored, porcelain AND full diff",
                          "ok" if ok else "*** NOT RESTORED ***"))
print()


# ---------------------------------------------------------------------------
# R2c  DELETION AT THE FINEST UNIT THAT EXISTS -- there is only one
# ---------------------------------------------------------------------------
hdr("R2c  THE BLOCK, SPLIT AND DELETED ONE PART AT A TIME")

print("  The parts are COUNTED BY SPLITTING THE FILE, not asserted.  A part")
print("  is a non-comment, non-blank line of the wiring block.  Each is")
print("  deleted ALONE, with B1 restored, and the runner is executed.")
print()


def block_lines(path):
    """The non-comment, non-blank lines of the cross-section wiring block."""
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    out = []
    for i, ln in enumerate(lines):
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        if "e2_crosssection" in s or "cross-section check" in s \
                or "E2OUT" in s or s in ("}", "exit 1"):
            out.append((i, ln))
    return lines, out


for t in RUNNERS:
    path = runner(t)
    lines, parts = block_lines(path)
    print("  %s: %d separable part(s) in the wiring block" % (t, len(parts)))
    for i, ln in parts:
        print("      line %-4d %s" % (i + 1, ln.strip()[:60]))
print()

if not claim:
    print("  skipped: no B1 to restore")
else:
    for t in RUNNERS:
        path = runner(t)
        rel = os.path.relpath(path, REPO)
        lines, parts = block_lines(path)
        for i, ln in parts:
            cut = "\n".join(lines[:i] + lines[i + 1:]) + "\n"
            with Probe("delete one line") as pr:
                pr.write(B1_DOC, doc + "\n\n## mg-5040 R2c\n\n" + claim + "\n")
                pr.write(rel, cut)
                rc, out = run_runner(t)
            ran = "E2 TOTAL BAD:" in out
            is_call = CALL in ln
            # Deleting the CALL must make the runner green AND silent: one
            # unit, one return, and the printing is not separable from it.
            # Deleting the label must leave both the verdict and the output.
            want = (0, False) if is_call else (1, True)
            got = (rc, ran)
            ok = got == want and pr.restored
            bad += (not ok)
            print("  %-22s del %-34s -> exit %d, output %-3s  %s"
                  % (t, ln.strip()[:34], rc, "yes" if ran else "no",
                     "ok" if ok else "*** wanted %s ***" % (want,)))
print()
print("  P2e.  The count above IS the claim: one part with a return.  R2d")
print("  runs the same split against the extracted pre-repair tree, so the")
print("  comparison is a measurement and not a quotation of mg-4700.")
print()


# ---------------------------------------------------------------------------
# R2d  the pin: three parts, and how many of them had a return
# ---------------------------------------------------------------------------
hdr("R2d  THE SAME SPLIT AT %s -- how many parts, and what each carried" % PRE)

pre_root = extract(PRE, os.path.join(os.environ.get("TMPDIR", "/tmp"),
                                     "mg5040-pre-%s" % PRE))
pre_doc_path = os.path.join(pre_root, B1_DOC)
with open(pre_doc_path, encoding="utf-8") as f:
    pre_doc = f.read()
_pre_strikes = [m.group(1) for m in re.finditer(r"~~([^~\n]+)~~", pre_doc)]
_pre_strikes.sort(key=lambda s: -len(s.split()))
pre_claim = (_pre_strikes[0] if _pre_strikes
             and len(_pre_strikes[0].split()) >= 8 else None)

for t in RUNNERS:
    path = os.path.join(pre_root, "code", t, "run_all.sh")
    lines, parts = block_lines(path)
    print("  %s: %d separable part(s) at the pin" % (t, len(parts)))
print()
if pre_claim:
    print("  Each part deleted alone at the pin, B1 restored, runner executed.")
    print("  This tree is an extraction, so nothing here can touch the")
    print("  worktree and no restore proof is needed or claimed.")
    print()
    with_return = {}
    for t in RUNNERS:
        path = os.path.join(pre_root, "code", t, "run_all.sh")
        lines, parts = block_lines(path)
        for i, ln in parts:
            with open(pre_doc_path, "w", encoding="utf-8") as f:
                f.write(pre_doc + "\n\n## mg-5040 R2d\n\n" + pre_claim + "\n")
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines[:i] + lines[i + 1:]) + "\n")
            rc, out = run_runner(t, root=pre_root)
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
            key = ln.strip()[:44]
            with_return.setdefault(key, []).append(rc)
            print("  %-22s del %-44s -> exit %d" % (t, key, rc))
        with open(pre_doc_path, "w", encoding="utf-8") as f:
            f.write(pre_doc)
    print()
    inert = [k for k, v in with_return.items() if all(c == 1 for c in v)]
    lost = [k for k, v in with_return.items() if any(c == 0 for c in v)]
    broke = [k for k, v in with_return.items() if any(c not in (0, 1) for c in v)]
    print("  DERIVED FROM THE ROWS ABOVE, in three categories, because")
    print("  \"inert\" and \"the file no longer parses\" are not the same thing")
    print("  and a two-way split would hide one inside the other:")
    print("      %d of %d part(s) INERT -- the runner still exits 1 without"
          % (len(inert), len(with_return)))
    for k in sorted(inert):
        print("          %s" % k)
    print("      %d part(s) LOAD-BEARING -- deleting one loses the verdict"
          % len(lost))
    for k in sorted(lost):
        print("          %s" % k)
    print("      %d part(s) whose deletion leaves a script that does not"
          % len(broke))
    print("      parse, which is not a deletion test at all and is reported")
    print("      rather than scored as either:")
    for k in sorted(broke):
        print("          %s" % k)
    print()
    print("  mg-821e deletion-tested this block AS ONE UNIT, so none of the")
    print("  distinctions above were visible to it.  mg-4700 split it into")
    print("  three by hand; splitting by line gives %d.  That the two counts"
          % len(with_return))
    print("  differ IS the finding: the number of parts a block has depends on")
    print("  how finely you choose to cut it, which is precisely why the")
    print("  answer here is to leave nothing to cut.")
print()


# ---------------------------------------------------------------------------
# R2e  mg-4700's F5, closed as a side effect of deleting the guard
# ---------------------------------------------------------------------------
hdr("R2e  A CRASH IN e2 IS NO LONGER REPORTED AS A FINDING e2 DID NOT MAKE")

print("  mg-4700 F5: the deleted guard printed `a struck claim stands")
print("  un-struck elsewhere` for ANY non-zero exit, so with e2 made to raise")
print("  all three runners announced a specific finding that was never made,")
print("  and stderr was not captured so the traceback went elsewhere.  With")
print("  the guard gone there is nothing left to make the claim.  Measured,")
print("  with e2 made to raise on its first line:")
print()
with open(os.path.join(REPO, E2), encoding="utf-8") as f:
    e2_src = f.read()
with Probe("e2 made to raise") as pr:
    pr.write(E2, "raise SystemError('mg-5040 R2e: deliberate')\n" + e2_src)
    for t in RUNNERS:
        rc, out = run_runner(t)
        claims = "a struck claim stands un-struck elsewhere" in out
        shows = "SystemError" in out or "Traceback" in out
        ok = rc == 1 and not claims
        bad += (not ok)
        print("  %-22s exit %d  claims a finding: %-3s  shows the crash: %-3s  %s"
              % (t, rc, "YES" if claims else "no", "yes" if shows else "no",
                 "ok" if ok else "***"))
ok = pr.restored
bad += (not ok)
print()
print("  %-58s %s" % ("e2_crosssection.py was restored",
                      "ok" if ok else "*** NOT RESTORED ***"))
print()


print("=" * 78)
print("R2 TOTAL BAD: %d" % bad)
print("=" * 78)
print()
print("EXTENT OF THIS NUMBER.  Three runners, one wiring block each, split")
print("into parts BY READING THE FILE and deleted one part at a time with B1")
print("restored on disk, at HEAD and at %s.  It says NOTHING about the" % PRE)
print("other steps in those runners, nothing about the 17 runners mg-c2b3")
print("swept, and nothing about whether e2 is the right check -- only about")
print("whether this block has one unit and whether that unit has a return.")
sys.exit(1 if bad else 0)
