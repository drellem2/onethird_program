"""T5 -- THE PRESERVED TRANSCRIPT, AND THE POPULATION OF PRESERVED TRANSCRIPTS.

mg-70c7 deliberately did NOT regenerate `code/runner_exit_c2b3/out_k1_census.txt`,
because `mg-05eb` cites it as the record of `ticket 1 / re-derived 0 / DIFFERS`
and the regex is repaired, so a re-run would print the opposite and destroy the
citation.  The PM ratified that judgement and named what was missing:

    A transcript that no longer reproduces from HEAD is a hazard unless it
    says so.  A future reader re-runs it, gets the opposite verdict, and
    concludes THE RECORD WAS WRONG -- which is the opposite of the truth.

  T5a  The file was not regenerated: its blob at HEAD against its blob at the
       sweep's own commit, and the row still reads as the record.
  T5b  The hazard, MEASURED: the same census row re-derived live at HEAD.
  T5c  The note -- at the transcript, at `mg-05eb`'s citation, and in
       `k1_census.py`'s docstring -- checked at `main`, where it is absent,
       and at HEAD.  A control that does not exhibit the defect proves
       nothing, so both revisions are read.
  T5d  THE CLASS, COUNTED.  One instance was found by a worker's conscience.
       The population is enumerated here by a predicate: a committed
       transcript CITED from outside its own directory whose producing code
       has changed since the transcript was written.

THE GRAIN OF EVERY COUNT BELOW IS FILES, and each label says so.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib56dc as M

sys.path.insert(0, os.path.join(M.REPO, M.SWEEP))
import libc2b3 as C                                            # noqa: E402

BAD = 0
FINDINGS = []
K1 = "%s/out_k1_census.txt" % M.SWEEP

M.bar("T5  THE PRESERVED TRANSCRIPT, AND THE CLASS IT BELONGS TO")

# ---------------------------------------------------------------------------
M.hdr("T5a  IT WAS NOT REGENERATED -- blob against blob")

# THE MARKER THAT SEPARATES THE LABEL FROM THE RECORD.  A note prepended above
# the transcript labels the record; anything that edited the record would not
# be a label.  So the identity that matters is not the file's -- it is the
# BODY's, below the marker, against the blob at the sweep's own commit.
NOTE_END = "# ---- end of mg-56dc note; the transcript as committed follows ----"
at_sweep = M.read(K1, M.SWEEP_REV)
now = M.read(K1, None)
for text, label in ((at_sweep, "the sweep's own commit %s" % M.SWEEP_REV),
                    (now, "the working tree, here")):
    row = [l.strip() for l in text.splitlines()
           if "pipefail" in l and ("DIFFERS" in l or "AGREES" in l)]
    print("      %-34s %s"
          % (label, row[0] if row else "*** the row is gone ***"))
print()
body_now = now.split(NOTE_END + "\n")[-1]
note_lines = len(now.splitlines()) - len(body_now.splitlines())
print("      the transcript BODY, byte-identical to %s   %s"
      % (M.SWEEP_REV, "yes" if body_now == at_sweep else "*** NO ***"))
print("      label lines prepended above it                %3d line(s)"
      % note_lines)
print("      the record itself, lines                      %3d line(s)"
      % len(body_now.splitlines()))
row_now = [l for l in body_now.splitlines()
           if "pipefail" in l and "DIFFERS" in l]
print("      the row still reads `ticket 1 / re-derived 0 / DIFFERS`   %s"
      % ("yes" if row_now else "*** NO ***"))
if not row_now:
    BAD += 1
    print("      *** the record has been destroyed ***")
if body_now != at_sweep:
    BAD += 1
    print("      *** the record has been EDITED, not labelled ***")
print()
print("  AND THE READER WHO SCANS FOR THE ROW STILL FINDS THE ROW.  mg-dee4's")
print("  `a5_floor.py` reads this file with a scan for the first line carrying")
print("  `pipefail` and a verdict; the label above contains no such line, so")
print("  the scan returns the same row it returned before:")
print("      %s" % ([l.strip() for l in now.split("\n")
                     if "pipefail" in l
                     and ("DIFFERS" in l or "AGREES" in l)] or ["(none)"])[0])

# ---------------------------------------------------------------------------
M.hdr("T5b  THE HAZARD, MEASURED -- the same row re-derived at HEAD")

PIN = C.TICKET_REF
runners = C.runners(PIN)
old_rx = re.compile(r"^\s*set\s+-o\s+pipefail")
new_hits, old_hits = [], []
for p in runners:
    try:
        src = M.read(p, PIN)
    except (RuntimeError, OSError):
        continue
    if C.has_pipefail(src):
        new_hits.append(p)
    for line in src.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if old_rx.match(line):
            old_hits.append(p)
print("  The census row is `runners at %s setting pipefail`.  Re-derived at"
      % PIN)
print("  the ticket's own revision under both spellings of the rule:")
print()
print("      runners in the population                  %3d file(s)" % len(runners))
print("      ...matching the PRE-REPAIR regex `set -o pipefail`   %2d file(s)"
      % len(set(old_hits)))
print("      ...matching the REPAIRED regex                       %2d file(s)"
      % len(set(new_hits)))
for p in sorted(set(new_hits)):
    print("          %s" % p)
print()
print("      the ticket said                              1 file(s)")
print("      the committed transcript recorded            0 file(s), DIFFERS")
print("      a re-run at HEAD would record                %d file(s), %s"
      % (len(set(new_hits)), "AGREES" if len(set(new_hits)) == 1 else "?"))
print()
if len(set(new_hits)) == 1 and len(set(old_hits)) == 0:
    print("  THAT IS THE HAZARD, IN ONE TABLE.  The transcript is a true record")
    print("  of a run under a rule that no longer exists.  A reader who re-runs")
    print("  it gets the opposite verdict and concludes the record was wrong.")
    print("  The record is right; the rule changed.  Nothing about that is")
    print("  visible from the transcript unless the transcript says it.")
else:
    BAD += 1
    print("  *** the control does not exhibit the hazard ***")

# ---------------------------------------------------------------------------
M.hdr("T5c  THE NOTE -- at `main`, where it is absent, and at HEAD")

NOTE = re.compile(r"HISTORICAL RECORD|no longer reproduce|will not reproduce|"
                  r"does not reproduce at HEAD|predates the mg-7522 repair|"
                  r"since repaired", re.I)
WHICH = re.compile(r"mg-7522|1ee1f1b|repaired the regex|PIPEFAIL_RE")
SITES = [(K1, "the transcript itself"),
         ("%s/README.md" % M.A05EB, "mg-05eb's citation of it"),
         ("%s/k1_census.py" % M.SWEEP, "`k1_census.py`'s docstring")]
print("  A note is sufficient only if it says THREE things: that this is a")
print("  historical record, that it will not reproduce at HEAD, and WHICH")
print("  repair closed it.  All three are asked of each site:")
print()
print("  `main` is the CONTROL -- the revision where the defect is still")
print("  present -- and the working tree is this ticket's answer to it.")
print()
print("      %-34s %-9s %-9s %s"
      % ("site", "at main", "here", "names the repair?"))
have = {}
for rel, label in SITES:
    try:
        at_main_text = M.read(rel, "main")
    except RuntimeError:
        at_main_text = ""
    here = M.read(rel, None)
    a = bool(NOTE.search(at_main_text))
    b = bool(NOTE.search(here))
    names = bool(b and WHICH.search(here))
    have[rel] = (a, b, names)
    print("      %-34s %-9s %-9s %s"
          % (label, "yes" if a else "NO", "yes" if b else "*** NO ***",
             "yes" if names else "*** NO ***"))
print()
at_main = sum(1 for v in have.values() if v[0])
at_head = sum(1 for v in have.values() if v[1] and v[2])
print("      sites carrying the note at `main`          %d of %d file(s)"
      % (at_main, len(SITES)))
print("      sites carrying the full note here          %d of %d file(s)"
      % (at_head, len(SITES)))
print()
if at_head < len(SITES):
    BAD += len(SITES) - at_head
    print("      *** the note is still missing somewhere ***")
elif at_main == len(SITES):
    BAD += 1
    print("      *** `main` already carried it everywhere, so this comparison")
    print("          is not a control ***")
else:
    print("  THE CONTROL EXHIBITS THE DEFECT: at `main` the note is at %d of"
          % at_main)
    print("  %d sites, and the two that lacked it are the transcript a reader"
          % len(SITES))
    print("  re-runs and the audit that cites it as evidence.  Preserving")
    print("  evidence without labelling it converts a citation into a false")
    print("  witness, and the label is what this ticket adds.")

# ---------------------------------------------------------------------------
M.hdr("T5d  THE CLASS, COUNTED -- one instance is not a population")

print("  POPULATION, NAMED AND MECHANICAL, AS A FUNNEL.  Every stage is a fact")
print("  about the repository rather than a judgement, and every stage's count")
print("  is printed so a reader can disagree with the stage rather than with a")
print("  total.  GRAIN: files, at every stage.")
print()
print("    1. a committed `out_*.txt`;")
print("    2. CITED by name from OUTSIDE its own directory -- by a `.md`, or a")
print("       `.py`/`.sh` that names it;")
print("    3. it RECORDS A DEFECT: it carries one of this arc's own")
print("       defect verdicts, listed below rather than described;")
print("    4. its producing code has CHANGED SINCE it was written -- some")
print("       `*.py`/`*.sh` in its directory has a newer commit.  That is the")
print("       checkable half of *it will not reproduce*.")
print()
DEFECT = re.compile(r"\bDIFFERS\b|\bSWALLOWED\b|\bWRONG\b|^FINDING:|"
                    r"TOTAL BAD: [1-9]|\bMISSED\b|\*\*\* ", re.M)
print("      the defect verdicts, as a rule and not as a description:")
print("          %s" % DEFECT.pattern.replace("|", "   "))
print()
outs = [p for p in M.git("ls-files", "--", "*/out_*.txt").splitlines() if p]
citers = [p for p in M.git("ls-files", "--", "*.md", "*.py", "*.sh").splitlines()
          if p]
citer_text = {}
for p in citers:
    try:
        citer_text[p] = M.read(p, None)
    except (RuntimeError, OSError):
        continue

# One history walk instead of two `git log` calls per file: `git log
# --name-only` in commit-time order gives every path its most recent commit
# time in a single process.  A per-file `git log` was the first draft and took
# minutes; the answer is the same and this one can be run.
LAST = {}
walk = M.git("log", "--format=@%ct", "--name-only")
ct = None
for line in walk.splitlines():
    if line.startswith("@"):
        ct = int(line[1:])
    elif line.strip() and line not in LAST:
        LAST[line] = ct

cited, defective, stale, noted = [], [], [], []
for t in outs:
    base = os.path.basename(t)
    d = os.path.dirname(t)
    refs = [p for p, s in citer_text.items()
            if base in s and os.path.dirname(p) != d]
    if not refs:
        continue
    cited.append(t)
    try:
        text = M.read(t, None)
    except (RuntimeError, OSError):
        continue
    if not DEFECT.search(text):
        continue
    defective.append(t)
    t_at = LAST.get(t, 0)
    newer = [s for s in LAST
             if s.startswith(d + "/") and s.endswith((".py", ".sh"))
             and LAST[s] > t_at]
    if not newer:
        continue
    stale.append((t, refs, newer))
    if bool(NOTE.search(text)) or all(NOTE.search(citer_text[r]) for r in refs):
        noted.append(t)
print("      committed `out_*.txt` in the repository          %3d file(s)"
      % len(outs))
print("      ...cited by name from outside their directory    %3d file(s)"
      % len(cited))
print("      ...that RECORD A DEFECT by the rule above        %3d file(s)"
      % len(defective))
print("      ...whose producing code has changed since        %3d file(s)"
      % len(stale))
print("      ...of those, carrying a staleness note           %3d file(s)"
      % len(noted))
print()
SHOW = 25
print("  THE %d, with the newest source that post-dates each.  %d are printed"
      % (len(stale), min(SHOW, len(stale))))
print("  and %d are not -- named as a CAP rather than left as a silent"
      % max(0, len(stale) - SHOW))
print("  truncation, because a list that stops without saying so reads as a")
print("  list that ended:")
print()
for t, refs, newer in sorted(stale)[:SHOW]:
    print("      %-52s %s" % (t, "NOTED" if t in noted else "*** NO NOTE"))
    print("          cited by %d artifact(s): %s"
          % (len(refs), ", ".join(sorted(os.path.basename(r) for r in refs)[:3])))
    print("          %d newer source(s) in its directory, e.g. %s"
          % (len(newer), os.path.basename(sorted(newer)[0])))
if len(stale) > SHOW:
    print()
    print("      ... and %d more, every one of them *** NO NOTE ***:"
          % (len(stale) - SHOW))
    for t, _r, _n in sorted(stale)[SHOW:]:
        print("          %s" % t)
print()
if len(stale) > len(noted):
    FINDINGS.append(M.finding(
        "T5d",
        "the class the PM asked to have counted has %d members and %d carry a "
        "note.  A committed transcript that is cited from outside its own "
        "directory AND whose producing code has changed since it was written "
        "is a transcript a reader can re-run and disbelieve; %d of them say "
        "nothing about that.  The one instance mg-70c7 found by its own "
        "conscience is labelled by this ticket -- it is one of the %d noted -- "
        "and the remaining %d are named above and are not this ticket's to "
        "relabel.  One instance found by a conscience is not a population"
        % (len(stale), len(noted), len(stale) - len(noted), len(noted),
           len(stale) - len(noted))))
    print("      *** the class is larger than the instance ***")
print()
print("  EXTENT OF THAT NUMBER, stated rather than implied.  Criterion 3 is")
print("  `the producing code changed`, which is NECESSARY for a transcript to")
print("  stop reproducing and not SUFFICIENT: a source edit that changes no")
print("  output leaves the transcript reproducing perfectly.  So this is an")
print("  UPPER BOUND on the class, and the direction is stated because a")
print("  bound whose direction is unstated is not a bound.  The one member")
print("  known to actually not reproduce -- measured in T5b -- is")
print("  `%s`." % K1)

print()
M.bar("T5 TOTAL FINDINGS: %d   TOTAL BAD: %d" % (len(FINDINGS), BAD))
print()
for f in FINDINGS:
    print(f)
print()
print("EXTENT OF THOSE NUMBERS.  TOTAL BAD counts a destroyed record, a")
print("transcript body that is not byte-identical to the sweep's own commit, a")
print("control that does not exhibit the hazard, and a site still missing the")
print("note.  TOTAL FINDINGS counts the uncounted class.  It ranges over every")
print("committed `out_*.txt` in the repository and every tracked `*.md`,")
print("`*.py` and `*.sh` that could cite one.  It does NOT establish that a")
print("stale-looking transcript really fails to reproduce -- that would take")
print("re-running every suite in the arc, and criterion 3 is an upper bound.")
sys.exit(min(len(FINDINGS) + BAD, 120))
