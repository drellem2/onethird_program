"""mg-18dc / V6 -- THE SHAPE ELSEWHERE, AND WHETHER THE REPAIR ADDRESSES IT.

`>` before a reader is one instance of *the artifact is consumed by the same run
that produces it*.  The brief names siblings -- `tee` without `pipefail`, a probe
reading a log still open for write, a transcript regenerated between two readers
-- and asks whether the two populations overlap.

It also asks the harder question, which is not about `>` at all: **does the
repair address the SHAPE, or only the 43?**  That one is answered by counting
what carries the fix at HEAD, and by asking where the four trees mg-ec63 named
as changing their answer are recorded.

Exit code = runners at HEAD still carrying the shape.
"""

import os
import re
import subprocess
import sys

import lib18dc as B

REV = "HEAD"
head = B.git("rev-parse", "HEAD").strip()

print("mg-18dc / V6 -- THE SHAPE ELSEWHERE")
print("HEAD: %s" % B.head())

sbx = B.sandbox(head, tag="head-v6")
TREES = B.runners_at(head)

# ---------------------------------------------------------------------------
B.hdr("V6a  `| tee` AND `pipefail`, RE-DERIVED AT HEAD")

print("  My brief says mg-c2b3 found 23 of 63 runners using `| tee` with only")
print("  1 setting `pipefail`.  mg-c2b3's OWN transcript re-derives that 1 as")
print("  0 and prints `ticket 1  re-derived 0  DIFFERS`.  So the figure handed")
print("  to me is already contradicted inside the tree it cites, and both are")
print("  over a 63-runner population that no longer exists.  Re-derived here")
print("  over the %d runners at HEAD:" % len(TREES))
print()
tee, pf, teepf = [], [], []
for t in TREES:
    src = open(os.path.join(sbx, t, "run_all.sh")).read()
    # SD9 of this instrument: the first draft matched `pipefail` anywhere in
    # the file and reported 31 of 117 runners setting it.  29 of those 31 are
    # COMMENTS explaining why `pipefail` is NOT used ("`set -o pipefail` is not
    # used: /bin/sh is dash on Linux, which rejects the option") -- the single
    # most repeated line in this arc's runners.  A rule that reads a comment as
    # code is mg-ec63's SD6b, and it turned a 2 into a 31.  Comment lines are
    # now dropped before matching, and `code_lines` is used for BOTH halves so
    # the tee count cannot drift from the pipefail count.
    code = B.code_of(src)
    has_tee = re.search(r"\|\s*tee\b", code) is not None
    has_pf = re.search(r"\bset\s+-[a-zA-Z]*o[a-zA-Z]*\b.*\bpipefail\b"
                       r"|\bset\s+-o\s+pipefail\b", code) is not None
    if has_tee:
        tee.append(t)
    if has_pf:
        pf.append(t)
    if has_tee and has_pf:
        teepf.append(t)
print("  population: the %d runners tracked at HEAD" % len(TREES))
B.plain("...RUNNERS piping a probe through `| tee`", len(tee), "one `run_all.sh`")
B.plain("...RUNNERS setting `pipefail` in any spelling", len(pf), "one `run_all.sh`")
B.plain("...RUNNERS doing BOTH -- the exit status survives the pipe",
        len(teepf), "one `run_all.sh`")
B.plain("...RUNNERS using `tee` WITHOUT `pipefail` -- exit status lost",
        len(tee) - len(teepf), "one `run_all.sh`")
print()
print("  A `| tee` without `pipefail` reports the exit status of `tee`, which")
print("  is 0 whenever `tee` could write.  That is the same shape one layer")
print("  over: THE RUN'S OWN VERDICT IS TAKEN FROM THE ARTIFACT-WRITER RATHER")
print("  THAN FROM THE THING BEING MEASURED.")

# ---------------------------------------------------------------------------
B.hdr("V6b  DO THE TWO POPULATIONS OVERLAP?")

print("  Truncation is re-measured at HEAD by execution, the V2 way -- stubbed")
print("  `python3`, and a transcript that is zero bytes when its probe starts.")
print()
trunc = []
for t in TREES:
    res, err = B.stub_run(sbx, t, timeout=120)
    if err or not res:
        continue
    if B.emptied_steps(res):
        trunc.append(t)
    B.sandbox_reset(sbx)
# SD10 of this instrument: the row below was labelled "RUNNERS in BOTH
# populations" while intersecting `tee` (all of it) with `trunc`, under a row
# that had just defined the population of interest as `tee` WITHOUT `pipefail`.
# A row name that is not its measurement.  Both intersections are now printed.
both = sorted((set(tee) - set(teepf)) & set(trunc))
both_anytee = sorted(set(tee) & set(trunc))
print("  population: the %d runners tracked at HEAD" % len(TREES))
B.plain("...RUNNERS starting a probe on an EMPTY transcript", len(trunc),
        "one `run_all.sh`")
B.plain("...RUNNERS using `tee` without `pipefail`", len(tee) - len(teepf),
        "one `run_all.sh`")
B.plain("...RUNNERS in BOTH populations -- `tee` without `pipefail` AND "
        "an emptied transcript", len(both), "one `run_all.sh`")
for t in both[:30]:
    print("          %s" % t.replace("code/", ""))
B.plain("...RUNNERS using `tee` AT ALL and also emptying a transcript",
        len(both_anytee), "one `run_all.sh`")
for t in both_anytee[:30]:
    print("          %s" % t.replace("code/", ""))
print()
print("  These are two different defects of one habit, and a runner in both is")
print("  a runner whose transcript is empty when read AND whose exit status is")
print("  the writer's rather than the probe's.")

# ---------------------------------------------------------------------------
B.hdr("V6c  DOES THE REPAIR ADDRESS THE SHAPE, OR ONLY THE 43?")

newmv = []
for t in TREES:
    src = open(os.path.join(sbx, t, "run_all.sh")).read()
    if B.carries_newmv(src):
        newmv.append(t)
work = []
for t in TREES:
    src = open(os.path.join(sbx, t, "run_all.sh")).read()
    if re.search(r"mktemp\s+-d", B.code_of(src)) and t not in newmv:
        work.append(t)
print("  population: the %d runners tracked at HEAD, AFTER the sweep merged" % len(TREES))
B.plain("...RUNNERS carrying the `.new`+`mv` structural fix", len(newmv),
        "one `run_all.sh`")
for t in newmv:
    print("          %s" % t.replace("code/", ""))
B.plain("...RUNNERS writing transcripts outside the repo (`mktemp -d`)",
        len(work), "one `run_all.sh`")
for t in work:
    print("          %s" % t.replace("code/", ""))
B.plain("...RUNNERS still starting a probe on an EMPTY transcript", len(trunc),
        "one `run_all.sh`")
print()
print("  mg-ec63 says so itself, in WHAT I DID NOT DO: `I did not apply the fix")
print("  to the other 95 runners`, because the ticket orders sweep-then-fix and")
print("  inverting it destroys the evidence.  THAT IS THE RIGHT CALL AND IT IS")
print("  ALSO THE ANSWER TO THIS SECTION: the shape is measured and unrepaired.")
print("  %d of %d runners carry it at the commit the sweep landed in." % (len(trunc), len(TREES)))

# ---------------------------------------------------------------------------
B.hdr("V6d  AND WHERE THE FOUR NAMED TREES ARE RECORDED")

named = ["runner_exit_repair_70c7", "branching_audit_d330",
         "face_geometry_audit_6653", "runner_exit_audit_56dc"]
print("  mg-ec63 names four trees whose probe changes its answer once it can")
print("  see its transcript, and says `I did not open a ticket per finding.")
print("  The four DIFFERENT trees are named here and nowhere else.`  Checked:")
print()
print("  population: the 4 trees mg-ec63 named as DIFFERENT")
found = 0
for n in named:
    hits = subprocess.run(["grep", "-rl", n, "--include=*.md", "."],
                          cwd=B.REPO, capture_output=True, text=True).stdout
    files = sorted(set(h for h in hits.split() if "truncate_sweep_ec63" not in h
                       and "idiom_sweep_audit_18dc" not in h))
    print("      %-34s named in %d .md file(s) outside the sweep's own tree"
          % (n, len(files)))
    for f in files[:3]:
        print("          %s" % f)
    if files:
        found += 1
B.plain("...TREES whose DIFFERENT verdict is recorded outside the sweep's tree",
        found, "one tree")
print()
print("  A finding that lives in exactly one README is a finding that is one")
print("  `git rm` from being unrecorded.  This is not a defect of the sweep --")
print("  it disclosed it -- it is the state of the repair.")

print()
print("V6 TOTAL RUNNERS AT HEAD STILL CARRYING THE SHAPE: %d" % len(trunc))
sys.exit(min(len(trunc), 120))
