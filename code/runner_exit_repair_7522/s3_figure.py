"""S3 -- THE FIGURE THAT WAS "CONFIRMED EXACTLY", AND THE GENERAL FORM OF IT.

mg-c2b3's census reported three numbers against the ticket's.  Two agreed and
one was marked `DIFFERS` by the instrument's own committed transcript:

    setting pipefail        ticket  1   re-derived  0   DIFFERS

and four reader-facing artifacts -- the README, `OUTCOMES.md`, the published
document, and `k1_census.py`'s own docstring -- reported that same number as
**1, "confirmed exactly"**.  The document even named the right file.  The
TICKET WAS RIGHT and the INSTRUMENT WAS WRONG: `libc2b3.PIPEFAIL_RE` was
`^\\s*set\\s+-o\\s+pipefail`, one spelling of the option, and
`code/state_restructure_34bf/run_all.sh` writes `set -euo pipefail`.

THE USEFUL HALF IS THE GENERAL FORM.  "Confirmed exactly", "verified",
"byte-identical" and their relatives mark the place where the author STOPPED
LOOKING, and that is where an error survives longest.  So they are a flag to
check FIRST, not a reason to skip -- and this probe does exactly that: it
enumerates every strength-marked numeric claim in mg-c2b3's reader-facing
artifacts BY A PREDICATE, checks the ones that carry a checkable number, and
dispositions the rest one at a time with a reason each.

The population is derived from `git show --name-only %s`, the sweep's own
commit, rather than from the four files mg-05eb happened to name.  A hand-list
is a filename rule, and a filename rule is what OPEN 1 is about.
""" % "52aeaf4"

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib7522 as L

BAD = 0

L.bar("S3  THE STRONGEST WORDING IS WHERE TO LOOK FIRST")

# ---------------------------------------------------------------------------
L.hdr("S3a  THE POPULATION OF STRENGTH-MARKED CLAIMS, DERIVED NOT LISTED")

TOUCHED = [p for p in L.git("show", "--name-only", "--format=", L.SWEEP).split()
           if p]
ARTIFACTS = sorted(p for p in TOUCHED
                   if p.startswith("code/runner_exit_c2b3/")
                   or (p.startswith("docs/") and p.endswith(".md")))
ARTIFACTS = [p for p in ARTIFACTS if not os.path.basename(p).startswith("out_")]

# mg-70c7: ONE marker rule, owned by the library and pointed in both
# directions.  It used to be defined here, nine alternatives, for the SUBJECT,
# while `s5_self.py` checked THIS TREE with a three-alternative rule of its own
# that did not contain the `verified` its own docstring named.  mg-dee4's F3.
MARK = L.MARK
NUM = re.compile(r"\b\d+\b")
# mg-70c7: the window is the line AND the line after it.  mg-dee4's F4: this
# rule was LINE-LOCAL, and `code/runner_exit_c2b3/OUTCOMES.md:88` carries
# `verified against the` with its figure `0 / 0 / 0 / 0 / 2111 / 0` on line 89
# -- so neither line scored and the strongest claim in the file was invisible
# to the rule built to find strong claims.  A marker and its figure separated
# by a hard wrap is the ordinary shape of wrapped prose, not an edge case.
WINDOW = 1

print("  PREDICATE.  A reader-facing artifact of the sweep is a file the")
print("  sweep's own commit %s touched, under `code/runner_exit_c2b3/` or" % L.SWEEP)
print("  under `docs/`, that is not a committed transcript.  A CLAIM is a")
print("  strength marker with a number WITHIN %d LINE of it, in EITHER"
      % WINDOW)
print("  direction -- a hard wrap puts the figure on the line before as")
print("  readily as on the line after.  The marker rule is `lib7522.MARK`, same")
print("  object `s5_self.py` turns on this tree -- %d alternatives, and the"
      % L.alternatives(L.MARK))
print("  %d-alternative rule this tree used on ITSELF is kept only as"
      % L.alternatives(L.MARK_OLD))
print("  `lib7522.MARK_OLD`, so S5 can exhibit the disagreement.")
print()
print("  artifacts: %d" % len(ARTIFACTS))
for p in ARTIFACTS:
    print("      %s" % p)
print()

CLAIMS = []
LINE_LOCAL = []
for p in ARTIFACTS:
    lines = L.read(p, None).splitlines()
    for i, line in enumerate(lines, 1):
        if not MARK.search(line):
            continue
        near = lines[max(0, i - 1 - WINDOW):i + WINDOW]
        if not any(NUM.search(x) for x in near):
            continue
        CLAIMS.append((p, i, " ".join(x.strip() for x in near)))
        if NUM.search(line):
            LINE_LOCAL.append((p, i))

print("  strength-marked numeric claims: %d" % len(CLAIMS))
print("      ...that a LINE-LOCAL rule would have found: %d" % len(LINE_LOCAL))
print("      ...that the one-line window ADDS:           %d"
      % (len(CLAIMS) - len(LINE_LOCAL)))
print()
for p, i, line in CLAIMS:
    print("    %-44s %4d %s %s"
          % (p.replace("code/runner_exit_c2b3/", "…/"), i,
             " " if (p, i) in LINE_LOCAL else "+", line[:90]))
print()
print("  The `+` rows are the four a hard wrap stepped over.  `20")
print("  strength-marked numeric claims, every one dispositioned` was exact")
print("  about the 20 the rule saw and silent about these.")

# ---------------------------------------------------------------------------
L.hdr("S3b  THE FIGURE ITSELF -- `pipefail`, re-derived under both rules")

pin_src = L.sources(L.ls_sh(L.PINNED), L.PINNED)
runners_pin = {p: s for p, s in pin_src.items()
               if os.path.basename(p) == "run_all.sh"}
head_src = L.sources(L.ls_sh(None), None)

old_pin = [p for p, s in runners_pin.items()
           if L.has_pipefail(s, L.PIPEFAIL_RE_OLD)]
new_pin = [p for p, s in runners_pin.items() if L.has_pipefail(s)]
new_all = [p for p, s in pin_src.items() if L.has_pipefail(s)]
new_head = [p for p, s in head_src.items() if L.has_pipefail(s)]

print("  The defect REPRODUCED and then CAUGHT, on the real bytes:")
print()
print("    rule                                    population         count")
print("    `^\\s*set\\s+-o\\s+pipefail`  (mg-c2b3)   run_all.sh @%s  %5d"
      % (L.PINNED, len(old_pin)))
print("    `^\\s*set\\s+[^#]*\\bpipefail\\b` (mg-7522) run_all.sh @%s  %5d"
      % (L.PINNED, len(new_pin)))
print("    ...same rule, over every `*.sh` @%s              %5d"
      % (L.PINNED, len(new_all)))
print("    ...same rule, over every `*.sh` at HEAD              %5d"
      % len(new_head))
print()
print("    the ticket said                                       %5d" % 1)
print()
for p in sorted(new_pin):
    for i, l in L.command_lines(runners_pin[p]):
        if L.PIPEFAIL_RE.match(l):
            print("    the one runner that sets it: %s:%d" % (p, i))
            print("        %s" % l.strip())
print()
if len(new_pin) == 1 and len(old_pin) == 0:
    print("  RE-DERIVED 1.  AGREES with the ticket.  The old rule re-derives 0")
    print("  on the same bytes, so the disagreement was the instrument's and")
    print("  the ticket's number was right all along.")
else:
    BAD += 1
    print("  *** the re-derivation does not behave as the repair predicts ***")

print()
print("  THE INSTRUMENT IS REPAIRED AT ITS SOURCE, not only in prose:")
sys.path.insert(0, os.path.join(L.REPO, "code/runner_exit_c2b3"))
try:
    import libc2b3 as C  # noqa: E402
    live = [p for p, s in runners_pin.items() if C.has_pipefail(s)]
    print("      `libc2b3.has_pipefail` at HEAD re-derives           %5d"
          % len(live))
    if len(live) != 1:
        BAD += 1
        print("      *** libc2b3 still disagrees with the ticket ***")
except Exception as e:                                   # pragma: no cover
    BAD += 1
    print("      *** could not import libc2b3: %s ***" % e)

# ---------------------------------------------------------------------------
L.hdr("S3c  THE SAME BLIND SPOT, ONE SENTENCE OVER -- the shebang")

print("  The published document says: *\"the shebang is `#!/bin/sh` on all 64")
print("  runners (measured)\"*.  `(measured)` is the strength marker; the")
print("  measurement is checked here rather than trusted.")
print()
for ref, label, srcmap in ((L.PINNED, "@%s" % L.PINNED, pin_src),
                           (None, "at HEAD", head_src)):
    runs = {p: s for p, s in srcmap.items()
            if os.path.basename(p) == "run_all.sh"}
    sh = [p for p, s in runs.items() if L.shebang(s) == "#!/bin/sh"]
    other = sorted(p for p in runs if p not in sh)
    print("    run_all.sh %-10s                       %3d" % (label, len(runs)))
    print("      ...with `#!/bin/sh`                       %3d" % len(sh))
    print("      ...with something else                    %3d" % len(other))
    for p in other:
        print("          %-50s %s" % (p, L.shebang(runs[p])))
    print()
n_pin_runs = len([p for p in pin_src if os.path.basename(p) == "run_all.sh"])
n_pin_sh = len([p for p, s in pin_src.items()
                if os.path.basename(p) == "run_all.sh"
                and L.shebang(s) == "#!/bin/sh"])
print("  \"all 64\" is FALSE: it is %d of %d at %s.  `k2_consume.py` printed"
      % (n_pin_sh, n_pin_runs, L.PINNED))
print("  \"on 59 of the 64\" -- the INSTRUMENT was right and the DOCUMENT")
print("  rounded it up to `all`.  Same shape as the pipefail figure with the")
print("  roles reversed, and both were carrying a strength marker.")

# ---------------------------------------------------------------------------
L.hdr("S3d  EVERY CLAIM IN S3a, DISPOSITIONED -- one at a time, reason each")

bare = len([p for p, s in runners_pin.items() if L.bare_grep_tee(s)])
tee34 = sum(len(L.tee_pipelines(s)) for s in runners_pin.values())
tee17 = len([p for p, s in runners_pin.items() if L.tee_pipelines(s)])

# THE DISPOSITION RULES.  Keyed on a SUBSTRING OF THE LINE, not on a line
# number.  The first draft of this table was keyed on line numbers and this
# very repair moved every one of them by adding its own correction notes -- a
# key that the act of repairing invalidates is the same failure as a census
# pinned to a revision that the act of landing invalidates, one file over.
#
# Each rule is (file substring, line substring, verdict, how it was checked).
# Coverage is checked in BOTH directions: every mechanical hit must match a
# rule, and every rule must match a hit.  A rule that has rotted is as much a
# hole as a hit that has none.
DISP = [
    ("OUTCOMES.md", "34 tee'd targets", "HOLDS ABOUT ITS POPULATION",
     "%d tee'd pipelines in %d run_all.sh @%s; S1d states what that population "
     "excludes and S2a reads the rest" % (tee34, tee17, L.PINNED)),
    ("OUTCOMES.md", "exactly 3", "NOT A CLAIM",
     "a PREDICTION with its miss kept as written -- 3 predicted, 8 measured"),
    ("OUTCOMES.md", "at all 17 runners", "HOLDS ABOUT ITS POPULATION",
     "17 is the name-defined runner count; over `*.sh` with a real `| tee` it "
     "is 19, and the extra 2 are S2's subject"),
    ("OUTCOMES.md", "docstring all reported", "WAS WRONG, NOW FIXED",
     "this file's `pipefail` row read AGREES while the instrument's own "
     "transcript read DIFFERS; mg-7522's note is the correction"),
    ("OUTCOMES.md", "the population of every number", "SCOPE NOTE ADDED",
     "not a wrong figure: mg-7522's note that every count in that section "
     "is defined by a filename, which S1 measures"),
    ("PREDICTIONS.md", "34 tee'd targets", "NOT A CLAIM",
     "a PREDICTION written before the instrument existed; OUTCOMES is where "
     "it becomes a claim and is dispositioned there"),
    ("PREDICTIONS.md", "at exactly 3", "NOT A CLAIM",
     "the Q6 prediction that MISSED, kept as written"),
    ("PREDICTIONS.md", "reach is identical", "NOT A CLAIM",
     "the Q8 prediction; OUTCOMES carries its result"),
    ("README.md", "bare grep", "HOLDS",
     "bare grep over run_all.sh @%s re-derives %d" % (L.PINNED, bare)),
    ("README.md", "used to read", "WAS WRONG, NOW FIXED",
     "the README's `pipefail` row; S3b re-derives the figure as 1 and the "
     "old rule as 0 on the same bytes"),
    ("k1_census.py", "docstring all said", "WAS WRONG, NOW FIXED",
     "the docstring used to assert the figure its own transcript marked "
     "DIFFERS; rewritten by mg-7522"),
    ("k2_consume.py", "all 23 uniformly", "NOT A CLAIM",
     "a quotation of the ticket's own words, inside the docstring"),
    ("k2_consume.py", "all 34 carried a verdict", "HOLDS",
     "%d is the tee'd-pipeline count @%s" % (tee34, L.PINNED)),
    ("k3_retro.py", "past green is confirmed", "NOT A CLAIM",
     "a description of what a 0 would mean, not an assertion that it was 0"),
    ("k3_retro.py", "byte for byte", "HOLDS",
     "a quotation of mg-2060's own claim text, being dispositioned"),
    ("run_all.sh", "About 4 minutes", "HOLDS",
     "a stated runtime, not a measurement of the subject"),
    ("ArcWideSweep.md", "bare grep", "HOLDS",
     "the same measurement as the README's row"),
    ("ArcWideSweep.md", "printed `ticket 1", "WAS WRONG, NOW FIXED",
     "the published document's `pipefail` row"),
    ("ArcWideSweep.md", "all 34 carried a verdict", "HOLDS",
     "%d is the tee'd-pipeline count @%s" % (tee34, L.PINNED)),
    ("ArcWideSweep.md", "all 64", "WAS WRONG, NOW FIXED",
     "the shebang sentence: `all 64` is %d of %d; S3c" % (n_pin_sh, n_pin_runs)),
    # mg-70c7: the four rows the one-line window ADDS (mg-dee4/F4).  Three of
    # them are markers written inside a comment ABOUT the marker, with the
    # adjacent number belonging to the sentence next door -- exactly the
    # mention-for-occurrence distinction this arc keeps re-deriving, arriving
    # here through the window rather than through the line.  They are
    # dispositioned rather than excluded by a rule tuned to drop them: a rule
    # that drops what it does not want is how a population becomes a hand-list.
    ("k1_census.py", "It was not confirmed", "NOT A CLAIM",
     "a comment recording that the docstring's old figure was wrong; the "
     "number on the adjacent line is the correction, not an assertion"),
    ("libc2b3.py", "reported the number as", "NOT A CLAIM",
     "a comment naming the marker the repaired `PIPEFAIL_RE` exists because "
     "of; the adjacent number is the regex's own subject"),
    ("selftestc2b3.py", "Both senses", "NOT A CLAIM",
     "a comment above the both-senses fixtures; the adjacent number is a "
     "fixture's expected count"),
]

def short(path):
    """A label a reader can scan: the basename, with the arc-wide document
    prefix dropped so one long filename does not set the column width."""
    return os.path.basename(path).replace("OneThird-RunnerExit-", "")


matched = {i: [] for i in range(len(DISP))}
unmatched_hits = []
table = []
for p, ln, line in CLAIMS:
    idx = [i for i, d in enumerate(DISP) if d[0] in p and d[1] in line]
    if not idx:
        unmatched_hits.append((p, ln, line))
        table.append(("%s:%d" % (short(p), ln), "UNDISPOSITIONED",
                      "*** no rule matches this line ***"))
        continue
    for i in idx:
        matched[i].append((p, ln))
    d = DISP[idx[0]]
    table.append(("%s:%d" % (short(p), ln), d[2], d[3]))

print("    %-22s %-26s %s" % ("artifact", "verdict", "how it was checked"))
L.rows(table, (22, 26), indent="    ")
print()
counts = {}
for _a, v, _h in table:
    counts[v] = counts.get(v, 0) + 1
print("  %d claims: %s"
      % (len(CLAIMS), ", ".join("%d %s" % (n, k)
                                for k, n in sorted(counts.items()))))
print()
print("  COVERAGE, BOTH DIRECTIONS.")
print("      mechanical hits with no rule                 %3d"
      % len(unmatched_hits))
for p, ln, line in unmatched_hits:
    print("          *** %s:%d  %s" % (p, ln, line[:60]))
dead = [DISP[i] for i, v in matched.items() if not v]
print("      rules matching no hit (rotted)               %3d" % len(dead))
for d in dead:
    print("          *** %s / %r" % (d[0], d[1]))
if unmatched_hits or dead:
    BAD += len(unmatched_hits) + len(dead)
    print("      *** something is uncovered, and this is the row that says so")
else:
    print("      Every hit has a rule and every rule has a hit.")

# ---------------------------------------------------------------------------
L.hdr("S3e  THE PROSE AND THE INSTRUMENT NOW AGREE -- checked, not asserted")

print("  The repaired artifacts must not still assert the old figure.")
print()
STALE = re.compile(r"pipefail.*confirmed exactly|confirmed exactly.*pipefail"
                   r"|`#!/bin/sh` on all \d+ runners", re.I)
stale = []
for p in ARTIFACTS + ["code/runner_exit_c2b3/k1_census.py"]:
    for i, line in enumerate(L.read(p, None).splitlines(), 1):
        if STALE.search(line):
            stale.append((p, i, line.strip()))
if stale:
    BAD += len(stale)
    print("  *** %d artifact line(s) still assert a corrected figure ***"
          % len(stale))
    for p, i, line in stale:
        print("      %s:%d  %s" % (p, i, line[:80]))
else:
    print("  0 of %d artifacts still assert either corrected figure." %
          len(ARTIFACTS))
print()
print("  TRANSCRIPT PROVENANCE, stated rather than backdated.")
print("  `code/runner_exit_c2b3/out_k1_census.txt` is the record of the run")
print("  that produced the sweep's commit, at its own revision, and mg-05eb")
print("  cites it.  It is NOT regenerated here: a transcript is a record of a")
print("  run at a time, and rewriting it would both destroy that citation and")
print("  be unreproducible anyway -- the arc has grown from 64 runners to %d"
      % len([p for p in head_src if os.path.basename(p) == "run_all.sh"]))
print("  since.  The corrected reading is published in THIS file's transcript,")
print("  and `k1_census.py`'s docstring points at it.")

# ---------------------------------------------------------------------------
L.hdr("S3f  THE GENERAL FORM, ON THIS SECTION")

print("  S3 is a probe that checks other people's strongest wording, so the")
print("  question it owes is whether its own is checkable.  Enumerated:")
print()
print("   1. Its population is DERIVED from `git show --name-only %s`, not"
      % L.SWEEP)
print("      hand-listed.  A hand-list is a filename rule.")
print("   2. Every number it prints comes with the predicate that produced")
print("      it, on the same line, so the rule is checkable and not only the")
print("      count.")
print("   3. It states the count of mechanical hits AND the count of")
print("      dispositions, and goes RED if the second is smaller -- silent")
print("      truncation is the failure mode a coverage claim has.")
print("   4. It contains no sentence of the form `confirmed exactly`.  S6 of")
print("      `selftest7522.py` measures that over this file's own bytes and")
print("      fails if an edit adds one.")
print("   5. The branch that CANNOT exhibit the defect, with the reason:")
print("      nothing here asserts a figure it did not compute in the same")
print("      run -- every row in S3b/S3c is a live re-derivation, and the two")
print("      rules are BOTH run so the disagreement is exhibited rather than")
print("      described.")

print()
L.bar("S3 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts (a) a re-derivation that does not")
print("behave as the repair predicts, (b) `libc2b3` still disagreeing with the")
print("ticket, (c) a repaired artifact still asserting a corrected figure, and")
print("(d) a mechanical hit with no disposition.  It ranges over the %d"
      % len(ARTIFACTS))
print("reader-facing artifacts of mg-c2b3 and the %d strength-marked numeric"
      % len(CLAIMS))
print("claims in them.  It does NOT range over the arc's other trees.")
sys.exit(1 if BAD else 0)
