"""R4 -- this deliverable, checked for the defect it remedies.

mg-5040's general form: *this deliverable is an artifact of the same kind as
the defect it repairs -- it is a claim about coverage, repairing claims about
coverage, and it will make coverage claims of its own.  Identify what kind of
artifact you are producing and check it for the defect it remedies.  Enumerate
what you checked, and if some branch honestly cannot exhibit the defect, say so
with the reason -- a stated reason is checkable, an omission is not.*

WHAT KIND OF ARTIFACT THIS IS.  Four kinds, and each is checked against the
OPEN item that could spoil it:

  1. CODE THAT ENUMERATES BY WALKING (this instrument reads its own files, and
     r3 walks the repository).  Exposed to OPEN 1: a set enumerated by walking,
     quantified over by a sentence.
  2. A SHELL RUNNER (`run_all.sh`).  Exposed to OPEN 2: a multi-part block
     whose parts have different returns.
  3. FIGURES IN PROSE (`README.md`, `OUTCOMES.md`, and the commit message this
     work ships with).  Exposed to OPEN 3: a number copied out of a run into a
     summary that nothing compares back.
  4. A PINNED COMPARISON.  Exposed to mg-821e's own defect: an anchor on HEAD
     stops comparing anything the moment the work lands.

TWO BRANCHES CANNOT EXHIBIT THE DEFECT, AND THE REASONS ARE STATED RATHER THAN
THE BRANCHES OMITTED -- R4e.
"""

import os
import re
import subprocess
import sys

from kern5040 import hdr, REPO, HERE, PRE, sh, git

bad = 0
MINE = os.path.relpath(HERE, REPO)


def files_here():
    """Every regular file of this instrument -- and what the walk declined.

    The same shape as the repair, applied to the repairer.  If this returned
    only the files, R4a would be checking a coverage claim with the very
    enumeration whose silence OPEN 1 is about.
    """
    files, stated, unstated = [], [], []

    def onerror(err):
        p = getattr(err, "filename", None) or HERE
        unstated.append((os.path.relpath(p, HERE),
                         "os.walk raised %s" % err.__class__.__name__))

    for dp, dns, fns in os.walk(HERE, onerror=onerror):
        keep = []
        for d in sorted(dns):
            p = os.path.join(dp, d)
            rel = os.path.relpath(p, HERE)
            if d == "__pycache__":
                stated.append((rel, "directory rule, STATED: __pycache__/"))
            elif os.path.islink(p):
                unstated.append((rel, "symlinked directory"))
            else:
                keep.append(d)
        dns[:] = keep
        for f in sorted(fns):
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, HERE)
            if os.path.isfile(p):
                files.append(rel)
            else:
                unstated.append((rel, "not a regular file"))
    return sorted(files), sorted(set(stated)), sorted(set(unstated))


# ---------------------------------------------------------------------------
# R4a  OPEN 1 applied to this instrument's own enumeration
# ---------------------------------------------------------------------------
hdr("R4a  KIND 1 -- THIS INSTRUMENT ENUMERATES BY WALKING, TOO")

files, stated, unstated = files_here()
print("  %s: %d regular file(s) reached" % (MINE, len(files)))
for r, why in stated:
    print("      declined, STATED:     %s   %s" % (r, why))
for r, why in unstated:
    print("      declined, NOT STATED: %s   %s" % (r, why))
if not stated and not unstated:
    print("      declined: nothing at all")
ok = not unstated
bad += (not ok)
print("  %-58s %s" % ("this instrument's own walk declines nothing unstated",
                      "ok" if ok else "*** %s ***" % unstated))
print()
print("  r3 also walks -- it reads every file tracked by git, twice.  That")
print("  enumeration is `git ls-files`, which has no depth rule, no symlink")
print("  rule and no extension rule to be silent about, because it is not a")
print("  filesystem traversal at all.  It has ONE bound and r3 states it in")
print("  its own output: a file that is not tracked is not in the census.")
rc, tracked = git(["ls-files", "--others", "--exclude-standard"])
untracked = [f for f in tracked.splitlines() if f.strip()]
print("  Untracked files in this worktree right now: %d" % len(untracked))
for f in untracked[:10]:
    print("      %s" % f)
print("  Named, so the bound of r3's census is visible and not asserted.")
print()


# ---------------------------------------------------------------------------
# R4b  OPEN 2 applied to this instrument's own runner
# ---------------------------------------------------------------------------
hdr("R4b  KIND 2 -- THIS INSTRUMENT'S OWN run_all.sh, SPLIT THE SAME WAY")

runner = os.path.join(HERE, "run_all.sh")
if not os.path.exists(runner):
    print("  *** no run_all.sh ***")
    bad += 1
else:
    with open(runner, encoding="utf-8") as f:
        lines = f.read().splitlines()
    steps = [(i, ln) for i, ln in enumerate(lines)
             if ln.strip() and not ln.strip().startswith("#")]
    # The shape mg-4700 F2 found: output CAPTURED into a variable, a brace
    # guard around the call, and a separate `echo` that does the printing --
    # three parts, two of them inert.  `cd "$(dirname "$0")"` is a command
    # substitution and is NOT that shape: it is one statement with one return
    # and nothing downstream depends on a variable holding a checker's
    # output.  The first version of this row flagged it, which is a detector
    # matching a character rather than a structure.
    compound = [(i, ln) for i, ln in steps
                if ("|| {" in ln or ln.strip() == "}"
                    or ln.strip().startswith('echo "$')
                    or re.match(r"^[A-Za-z_][A-Za-z0-9_]*=\$\(", ln.strip()))]
    print("  %d non-comment line(s); %d of them are part of a multi-part"
          % (len(steps), len(compound)))
    print("  block of the kind mg-4700 F2 found inert:")
    for i, ln in compound:
        print("      line %-4d %s" % (i + 1, ln.strip()[:60]))
    if not compound:
        print("      (none -- every step is one statement, and `set -e`")
        print("       carries every verdict)")
    ok = not compound
    bad += (not ok)
    print("  %-58s %s" % ("no multi-part block in this runner",
                          "ok" if ok else "*** %d ***" % len(compound)))
    piped = [(i, ln) for i, ln in steps if "| tee" in ln]
    ok2 = not piped
    bad += (not ok2)
    print("  %-58s %s" % ("no `| tee` swallowing an exit code (mg-c2b3)",
                          "ok" if ok2 else "*** %d ***" % len(piped)))
print()


# ---------------------------------------------------------------------------
# R4c  OPEN 3 applied to this deliverable's own figures
# ---------------------------------------------------------------------------
hdr("R4c  KIND 3 -- EVERY FIGURE THIS DELIVERABLE STATES, AGAINST ITS RUN")

print("  The defect: a number copied out of a run into a summary that nothing")
print("  compares back.  Two commit messages and a document carried one such")
print("  number for a whole ticket (OPEN 3).  So every `Rn TOTAL BAD: k`")
print("  claimed in this instrument's own prose is compared with the")
print("  transcript of that run, here, in the run itself.")
print()
TOTALS = re.compile(r"\b(R[1-4]) TOTAL BAD:?\s*\**(\d+)")
transcripts = {}
for name in ("out_r1_bound.txt", "out_r2_wiring.txt", "out_r3_summaries.txt",
             "out_r4_self.txt"):
    p = os.path.join(HERE, name)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            for tag, val in TOTALS.findall(f.read()):
                transcripts[tag] = int(val)
print("  from the committed transcripts: %s"
      % (", ".join("%s=%d" % kv for kv in sorted(transcripts.items()))
         or "(none yet -- first run)"))
prose_rows = []
for name in ("README.md", "OUTCOMES.md", "PREDICTIONS.md"):
    p = os.path.join(HERE, name)
    if not os.path.exists(p):
        continue
    with open(p, encoding="utf-8") as f:
        for tag, val in TOTALS.findall(f.read()):
            prose_rows.append((name, tag, int(val)))
if not prose_rows:
    print("  no figure of that form is stated in this instrument's prose yet.")
for name, tag, val in prose_rows:
    got = transcripts.get(tag)
    # R4's OWN figure is reported and NOT scored, and here is the reason,
    # which is checkable: out_r4_self.txt is written by the runner AFTER this
    # file exits, so within one run the only transcript available is the
    # PREVIOUS run's.  Scoring it would make the first run of a fresh
    # checkout red for a reason that has nothing to do with the repair, and
    # silently skipping it would be the census going 8 short.
    own = (tag == "R4")
    ok = got is not None and got == val
    if not own:
        bad += (not ok)
    print("  %-34s says %s = %d   transcript %s   %s"
          % (name, tag, val, got,
             ("ok" if ok else "*** DISAGREES ***") if not own
             else "reported, NOT scored: this run's transcript does not "
                  "exist yet"))
print()
print("  R4c CANNOT check the commit message, because the commit does not")
print("  exist when this runs.  That is a real hole and naming it is the")
print("  point: the same hole is what let `A2 TOTAL BAD 1` into two commit")
print("  messages.  What closes it here is that every figure in the commit")
print("  message is required to appear in one of the files above FIRST, so")
print("  the message is a copy of something this check does cover.")
print()


# ---------------------------------------------------------------------------
# R4d  the anchor, applied to this deliverable
# ---------------------------------------------------------------------------
hdr("R4d  KIND 4 -- IS ANY COMPARISON IN THIS INSTRUMENT ANCHORED ON HEAD?")

srcs = [f for f in os.listdir(HERE) if f.endswith(".py")]
hits = []
for f in sorted(srcs):
    with open(os.path.join(HERE, f), encoding="utf-8") as fh:
        for n, ln in enumerate(fh.read().splitlines(), 1):
            if re.search(r"""["']HEAD["']""", ln) and "rev-parse" not in ln:
                hits.append((f, n, ln.strip()))
for f, n, ln in hits:
    print("      %s:%d  %s" % (f, n, ln[:60]))
ok = not hits
bad += (not ok)
print("  %-58s %s" % ("no comparison is anchored on HEAD (it is %s)" % PRE,
                      "ok" if ok else "*** %d site(s) ***" % len(hits)))
print("  e2_crosssection.py DOES ask git for HEAD, and that is the opposite")
print("  case: it is not comparing against HEAD, it is RECORDING which")
print("  revision it measured, so that a stale copy reads as stale.")
print()


# ---------------------------------------------------------------------------
# R4e  the branches that CANNOT exhibit the defect, with reasons
# ---------------------------------------------------------------------------
hdr("R4e  BRANCHES THAT CANNOT EXHIBIT THE DEFECT, AND WHY")

print("  An omission is not checkable; a stated reason is.  Two branches of")
print("  the enumeration above are not checked, and here is each with the")
print("  reason a reader can argue with:")
print()
print("  1. THE MATHEMATICS.  Nothing in this ticket reads, evaluates or")
print("     restates a mathematical claim.  The four checkers it edits match")
print("     SENTENCES; the repair changes which files they read and what")
print("     they say about that set.  A coverage defect cannot reach a")
print("     theorem through a file list.  Checkable: `git diff` touches no")
print("     file under a mathematics tree, which R4f measures rather than")
print("     asserts.")
print("  2. THE AUDITORS' INSTRUMENTS.  mg-6cb9's a2_crosssection.py and")
print("     mg-4700's q1..q4 make coverage claims of their own and are NOT")
print("     checked here -- deliberately, and not because they are safe.  An")
print("     instrument edited or graded by the thing it audits has stopped")
print("     being evidence.  They are run unmodified and whatever they say")
print("     is reported.  The reason this is not a hole: their claims are")
print("     ABOUT this repair, so an error in them shows up as a")
print("     disagreement with these rows, not as silence.")
print()


# ---------------------------------------------------------------------------
# R4f  the mathematics, measured rather than asserted
# ---------------------------------------------------------------------------
hdr("R4f  R4e's FIRST REASON, MEASURED")

rc, names = git(["diff", "--name-only", PRE])
touched = [f for f in names.splitlines() if f.strip()]
rc2, untr = git(["ls-files", "--others", "--exclude-standard"])
touched += [f for f in untr.splitlines() if f.strip()]
print("  %d path(s) differ from %s (including untracked):" % (len(touched), PRE))
for f in sorted(touched):
    print("      %s" % f)
print()
MATH_MARKERS = ("theorem", "lemma", "proposition", "proof")
suspicious = []
for f in touched:
    p = os.path.join(REPO, f)
    if not os.path.isfile(p) or not f.endswith((".md", ".py")):
        continue
    rc3, d = git(["diff", "-U0", PRE, "--", f])
    added = [ln for ln in d.splitlines() if ln.startswith("+")
             and not ln.startswith("+++")]
    for ln in added:
        low = ln.lower()
        if any(m in low for m in MATH_MARKERS):
            suspicious.append((f, ln.strip()[:70]))
print("  Added lines mentioning %s: %d" % ("/".join(MATH_MARKERS),
                                           len(suspicious)))
for f, ln in suspicious:
    print("      %s: %s" % (f, ln))
print("  These are reported and not scored: naming a theorem in a comment is")
print("  not restating one, and a rule that could tell them apart would be a")
print("  claim this instrument cannot support.  The row that IS scored is")
print("  that no file under a mathematics tree changed at all.")
MATH_TREES = ("code/species_7d75/",)
math_changed = [f for f in touched if f.startswith(MATH_TREES)]
ok = not math_changed
bad += (not ok)
print("  %-58s %s" % ("no file under %s changed" % MATH_TREES[0],
                      "ok" if ok else "*** %s ***" % math_changed))
print()


print("=" * 78)
print("R4 TOTAL BAD: %d" % bad)
print("=" * 78)
print()
print("EXTENT OF THIS NUMBER.  FOUR kinds of artifact this deliverable")
print("produces, each checked against the OPEN item that could spoil it, plus")
print("TWO branches named as unable to exhibit the defect with a reason for")
print("each and one of those reasons measured.  It says NOTHING about whether")
print("the repair in r1-r3 is correct -- that is what r1-r3 are for -- and")
print("nothing about any artifact this ticket does not produce.  It cannot")
print("check the commit message, which does not exist yet, and says so above")
print("rather than leaving the reader to notice.")
sys.exit(1 if bad else 0)
