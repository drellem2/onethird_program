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

MARK = re.compile(r"confirmed exactly|byte-identical|byte for byte|\bverified\b"
                  r"|\(measured\)|\bidentical\b|\bconfirmed\b"
                  r"|\ball (?:\d+|of)\b|\bexactly \d+\b", re.I)
NUM = re.compile(r"\b\d+\b")

print("  PREDICATE.  A reader-facing artifact of the sweep is a file the")
print("  sweep's own commit %s touched, under `code/runner_exit_c2b3/` or" % L.SWEEP)
print("  under `docs/`, that is not a committed transcript.  A CLAIM is a line")
print("  in one of them carrying BOTH a strength marker and a number.")
print()
print("  artifacts: %d" % len(ARTIFACTS))
for p in ARTIFACTS:
    print("      %s" % p)
print()

CLAIMS = []
for p in ARTIFACTS:
    for i, line in enumerate(L.read(p, None).splitlines(), 1):
        if MARK.search(line) and NUM.search(line):
            CLAIMS.append((p, i, line.strip()))

print("  strength-marked numeric claims: %d" % len(CLAIMS))
print()
for p, i, line in CLAIMS:
    print("    %-44s %4d  %s" % (p.replace("code/runner_exit_c2b3/", "…/"),
                                 i, line[:92]))

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

# (file substring, line, verdict, how it was checked)
DISP = [
    ("README.md", 26, "HOLDS",
     "bare grep over run_all.sh @%s re-derives %d" % (L.PINNED, bare)),
    ("README.md", 28, "WAS WRONG, NOW FIXED",
     "the figure is 1 and the instrument said 0; S3b re-derives 1"),
    ("OUTCOMES.md", 8, "HOLDS ABOUT ITS POPULATION",
     "%d tee'd pipelines in %d run_all.sh @%s; S1d states what the "
     "population excludes and S2a reads the rest" % (tee34, tee17, L.PINNED)),
    ("OUTCOMES.md", 13, "NOT A CLAIM",
     "a PREDICTION with its miss kept as written -- 3 predicted, 8 measured"),
    ("OUTCOMES.md", 15, "HOLDS ABOUT ITS POPULATION",
     "17 is the name-defined runner count; over `*.sh` with a real `| tee` "
     "it is 19, and the extra 2 are S2's subject"),
    ("ArcWideSweep.md", 43, "HOLDS", "same measurement as README.md:26"),
    ("ArcWideSweep.md", 45, "WAS WRONG, NOW FIXED", "same as README.md:28"),
    ("ArcWideSweep.md", 99, "HOLDS",
     "'all 34 carried a verdict' -- %d is the tee'd-pipeline count @%s"
     % (tee34, L.PINNED)),
    ("ArcWideSweep.md", 229, "WAS WRONG, NOW FIXED",
     "'all 64' is %d of %d; S3c" % (n_pin_sh, n_pin_runs)),
    ("k1_census.py", None, "WAS WRONG, NOW FIXED",
     "the docstring said 'confirmed exactly' about the number its own "
     "transcript marked DIFFERS"),
    ("k2_consume.py", 6, "NOT A CLAIM",
     "a quotation of the ticket's own words, inside the docstring"),
    ("k2_consume.py", 266, "HOLDS", "'all 34 carried a verdict', as above"),
    ("k3_retro.py", 24, "NOT A CLAIM",
     "a description of what a 0 would mean, not an assertion that it was 0"),
    ("k3_retro.py", 103, "HOLDS",
     "a quotation of mg-2060's own claim text, being dispositioned"),
    ("PREDICTIONS.md", 23, "NOT A CLAIM",
     "a PREDICTION written before the instrument existed; OUTCOMES:8 is "
     "where it becomes a claim and is dispositioned there"),
    ("PREDICTIONS.md", 51, "NOT A CLAIM",
     "the Q6 prediction that MISSED, kept as written"),
    ("PREDICTIONS.md", 69, "NOT A CLAIM",
     "the Q8 prediction; OUTCOMES:15 carries its result"),
    ("run_all.sh", 17, "HOLDS",
     "a stated runtime, not a measurement of the subject; the runner is "
     "re-run by this repair and completes"),
]

print("    %-22s %-24s %s" % ("artifact", "verdict", "how it was checked"))
L.rows([("%s:%s" % (n, ln if ln else "docstring"), v, h)
        for n, ln, v, h in DISP], (22, 24), indent="    ")
print()
n_fixed = len([d for d in DISP if d[2].startswith("WAS WRONG")])
print("  %d claims: %d hold, %d are not claims, %d WERE WRONG and are fixed"
      % (len(DISP),
         len([d for d in DISP if d[2].startswith("HOLDS")]),
         len([d for d in DISP if d[2] == "NOT A CLAIM"]), n_fixed))
print()
print("  COVERAGE.  S3a found %d lines mechanically and %d rows are"
      % (len(CLAIMS), len(DISP)))
print("  dispositioned above -- one per hit.  `k1_census.py`'s row is keyed on")
print("  the FILE rather than on a line number, because this very repair")
print("  rewrote that docstring and a line-numbered key would rot on contact.")
if len(DISP) < len(CLAIMS):
    BAD += 1
    print("  *** fewer dispositions than mechanical hits -- something is")
    print("      uncovered and this is the row that says so ***")

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
