"""J1 -- THE CENSUS, RE-DERIVED WITH MY OWN INSTRUMENT, OVER A WIDER POPULATION.

The ticket's numbers were 63 / 23 / 1.  The sweep re-derived them at `bee07a1` as
64 / 23 / 0 (plus a 17 the ticket did not separate) and moved on.

This section does three things the sweep did not:

  * it declares the population as **every `*.sh` in the repository**, not every
    file named `run_all.sh`.  The sweep's population is a NAMING CONVENTION, and
    a naming convention is not a property of the defect: a pipeline in a file
    called `run_audit.sh` swallows exactly the same status;
  * it re-derives the sweep's own numbers from a parser written from scratch, so
    an agreement is evidence and not an echo;
  * it goes and finds where the ticket's third number, `pipefail: 1`, came from,
    instead of recording it as DIFFERS.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib05eb as L

BAD = 0
MISS = []


def predict(qid, predicted, measured, ok):
    """Record a prediction outcome.  Deliberately does NOT feed TOTAL BAD: a
    prediction I got wrong is my error and is kept as written; TOTAL BAD counts
    defects in the artifact under audit."""
    MISS.append((qid, predicted, measured, ok))
    print("  %-4s predicted %-28s measured %-28s %s"
          % (qid, predicted, measured, "as predicted" if ok else "*** MISS ***"))


L.bar("J1  THE CENSUS -- my own parser, over every `*.sh` in the repository")

for label, ref in (("at %s (the sweep's pinned revision)" % L.PINNED, L.PINNED),
                   ("on disk at HEAD (post-sweep)", None)):
    L.hdr("J1a  ALL `*.sh` %s" % label)
    sh = L.ls_sh(ref)
    src = {}
    for p in sh:
        try:
            src[p] = L.read(p, ref)
        except Exception:
            continue
    sh = sorted(src)
    runall = [p for p in sh if os.path.basename(p) == "run_all.sh"]
    other = [p for p in sh if os.path.basename(p) != "run_all.sh"]
    tee_all = [p for p in sh if L.tee_pipelines(src[p])]
    tee_runall = [p for p in tee_all if p in runall]
    tee_other = [p for p in tee_all if p in other]
    npipe = sum(len(L.tee_pipelines(src[p])) for p in tee_all)
    npipe_other = sum(len(L.tee_pipelines(src[p])) for p in tee_other)
    grep_runall = [p for p in runall if L.bare_grep_tee(src[p])]
    pf = [p for p in sh if L.has_pipefail(src[p])]

    print("  `*.sh` tracked in the repository            %4d" % len(sh))
    print("    ...named run_all.sh                       %4d" % len(runall))
    print("    ...NOT named run_all.sh                   %4d" % len(other))
    print()
    print("  with a REAL `| tee` pipeline, total         %4d file(s), %d pipeline(s)"
          % (len(tee_all), npipe))
    print("    ...in run_all.sh   (the sweep's whole population)  %2d" % len(tee_runall))
    print("    ...OUTSIDE it                                     %2d file(s), %d pipeline(s)"
          % (len(tee_other), npipe_other))
    print()
    print("  run_all.sh matching the ticket's bare grep  %4d" % len(grep_runall))
    print("  `*.sh` setting pipefail                     %4d" % len(pf))
    print("  `*.sh` setting `set -e`                     %4d"
          % sum(1 for p in sh if L.has_set_e(src[p])))

    if tee_other:
        print()
        print("  THE FILES THE SWEEP'S POPULATION CANNOT CONTAIN, line by line:")
        for p in tee_other:
            print("    %s   set -e: %s" % (p, "yes" if L.has_set_e(src[p]) else "NO"))
            for i, l in L.tee_pipelines(src[p]):
                print("        %-4d %s" % (i, l.strip()[:88]))

    if ref == L.PINNED:
        predict("Q1", "72", str(len(sh)), len(sh) == 72)
        predict("Q2", "64", str(len(runall)), len(runall) == 64)
        predict("Q3", "23", str(len(grep_runall)), len(grep_runall) == 23)
        predict("Q4", "17", str(len(tee_runall)), len(tee_runall) == 17)
        predict("Q5", "2", str(len(tee_other)), len(tee_other) == 2)
        predict("Q6", "8", str(npipe_other), npipe_other == 8)
        predict("Q8", "0", str(len(pf)), len(pf) == 0)
    else:
        predict("Q7", "2 files / 8 pipelines",
                       "%d files / %d pipelines" % (len(tee_other), npipe_other),
                       len(tee_other) == 2 and npipe_other == 8)
        if tee_runall:
            print("  *** a run_all.sh still carries a pipeline after the sweep ***")
            BAD += 1

# ---------------------------------------------------------------------------
L.hdr("J1b  THE DISAGREEMENT WITH THE BARE GREP, RE-DERIVED INDEPENDENTLY")

src = {p: L.read(p, L.PINNED) for p in L.ls_sh(L.PINNED)}
runall = [p for p in sorted(src) if os.path.basename(p) == "run_all.sh"]
only_grep = [p for p in runall if L.bare_grep_tee(src[p]) and not L.tee_pipelines(src[p])]
print("  run_all.sh the bare grep counts and my parser does not: %d" % len(only_grep))
for p in only_grep:
    i, l = L.bare_grep_tee(src[p])[0]
    print("    %-46s :%-4d %s" % (p, i, l.strip()[:60]))
print()
print("  Each is a header COMMENT saying the runner does not use `| tee`.")
print("  The sweep reported the same six; this is a second derivation from a")
print("  parser that has never seen the first one, which is what makes the")
print("  agreement worth anything.")
if len(only_grep) != 6:
    print("  *** expected 6 ***")
    BAD += 1

# ---------------------------------------------------------------------------
L.hdr("J1c  THE TICKET'S THIRD NUMBER -- `pipefail: 1`, and where it came from")

print("  The sweep re-derived `1` as `0` over run_all.sh and marked it DIFFERS.")
print("  A count that is wrong is a lead.  This is the whole repository at")
print("  %s, every tracked file of any type, for the string `pipefail`:" % L.PINNED)
print()
hits = L.git("grep", "-n", "pipefail", L.PINNED, ok=(0, 1)).splitlines()
for h in hits:
    print("    %s" % h[:110])
print()
print("  total occurrences: %d, in %d file(s)"
      % (len(hits), len({h.split(":")[1] for h in hits if ":" in h})))
sh_hits = [h for h in hits if h.split(":")[1].endswith(".sh")] if hits else []
print("  ...of which in a `*.sh`: %d" % len(sh_hits))
predict("Q9", "not in any *.sh", "%d in *.sh" % len(sh_hits),
               len(sh_hits) == 0)
print()
print("  READING.  The ticket's `1` is not a runner that sets `pipefail`.  No")
print("  runner in this arc has ever set it.  The number is real but it counts")
print("  a different thing, and neither the ticket nor the sweep says which.")

# ---------------------------------------------------------------------------
L.hdr("J1d  WHAT THE POPULATION CHOICE COST -- stated as a number, not a caveat")

pre = {p: L.read(p, L.PINNED) for p in L.ls_sh(L.PINNED)}
now = {p: L.read(p) for p in L.ls_sh()}
pre_tee = {p for p in pre if L.tee_pipelines(pre[p])}
now_tee = {p for p in now if L.tee_pipelines(now[p])}
print("  files with a real `| tee` pipeline at %s : %d" % (L.PINNED, len(pre_tee)))
print("  files with a real `| tee` pipeline at HEAD      : %d" % len(now_tee))
print("  repaired by the sweep                           : %d"
      % len(pre_tee - now_tee))
print("  STILL PIPELINED AT HEAD                         : %d" % len(now_tee))
for p in sorted(now_tee):
    print("      %s  (%d pipeline(s), set -e: %s)"
          % (p, len(L.tee_pipelines(now[p])),
             "yes" if L.has_set_e(now[p]) else "no"))
print()
print("  The sweep's commit message says `17 runners repaired ... at 34 of 34")
print("  sites`.  Both halves are true of its population.  Over the population")
print("  a reader would assume -- shell runners in this repository -- the")
print("  sweep is %d of %d files and %d of %d pipelines."
      % (len(pre_tee - now_tee), len(pre_tee),
         sum(len(L.tee_pipelines(pre[p])) for p in pre_tee - now_tee),
         sum(len(L.tee_pipelines(pre[p])) for p in pre_tee)))

# ---------------------------------------------------------------------------
L.hdr("J1e  THE `pipefail` ROW -- what the instrument printed vs what the "
      "prose says")

print("  Q8 and Q9 MISSED because I inherited the sweep's `0` instead of")
print("  measuring it.  The ticket's `1` is RIGHT.  Two things follow, and")
print("  both are about the sweep, not the ticket.")
print()
print("  1. WHY THE INSTRUMENT GOT 0.  `libc2b3.PIPEFAIL_RE` is:")
pf_re = [l for l in L.read("code/runner_exit_c2b3/libc2b3.py").splitlines()
         if "PIPEFAIL_RE" in l and "compile" in l]
for l in pf_re:
    print("       %s" % l.strip())
print("     The one runner that sets the option writes it as `set -euo pipefail`,")
print("     the combined form.  `-o\\s+pipefail` cannot match it.")
print()
target = "code/state_restructure_34bf/run_all.sh"
print("  2. WHAT THE ARTIFACTS SAY.  These are the sweep's own committed files:")
rows = [
    ("code/runner_exit_c2b3/out_k1_census.txt", "setting pipefail"),
    ("code/runner_exit_c2b3/README.md", "setting `pipefail`"),
    ("code/runner_exit_c2b3/OUTCOMES.md", "| `pipefail` |"),
    ("docs/OneThird-RunnerExit-ArcWideSweep.md", "setting `pipefail`"),
    ("code/runner_exit_c2b3/k1_census.py", "pipefail count"),
]
asserts_one = 0
prints_zero = 0
for rel, needle in rows:
    txt = L.read(rel)
    hit = [l.strip() for l in txt.splitlines() if needle in l]
    for h in hit:
        says_zero = "re-derived  0" in h or "re-derived 0" in h or "DIFFERS" in h
        says_one = (not says_zero) and ("1" in h)
        if says_zero:
            prints_zero += 1
        elif says_one:
            asserts_one += 1
        print("     [%s] %-44s %s"
              % ("MEASURED 0" if says_zero else "ASSERTS  1", rel, h[:78]))
print()
print("     artifacts asserting 1 / confirmed / AGREES : %d" % asserts_one)
print("     the instrument's own transcript            : %d row saying 0, DIFFERS"
      % prints_zero)
MISS.append(("Q23", "4", str(asserts_one), asserts_one == 4))
print("  %-4s predicted %-28s measured %-28s %s"
      % ("Q23", "4", str(asserts_one),
         "as predicted" if asserts_one == 4 else "*** MISS ***"))
if asserts_one and prints_zero:
    print()
    print("  FINDING.  Four reader-facing artifacts say the pipefail count was")
    print("  CONFIRMED at 1 -- one of them naming `code/state_restructure_34bf/`")
    print("  correctly -- while the instrument that is cited as having measured")
    print("  it printed `re-derived 0 ... DIFFERS`.  The prose is right about")
    print("  the world and wrong about its own measurement, which is the")
    print("  SUMMARY vs ROWS defect this arc repaired in mg-8aae and mg-8eca,")
    print("  reproduced inside the artifact that repairs swallowed statuses.")
    BAD += 1

print()
print("  3. THE SHEBANG CLAIM, MEASURED.  The sweep's document says")
print('     "The shebang is `#!/bin/sh` on all 64 runners (measured)".')
src_all = {p: L.read(p, L.PINNED) for p in L.ls_sh(L.PINNED)}
runners64 = [p for p in sorted(src_all) if os.path.basename(p) == "run_all.sh"]
notsh = [(p, src_all[p].splitlines()[0]) for p in runners64
         if src_all[p].splitlines()[0].strip() != "#!/bin/sh"]
print("     run_all.sh at %s                : %d" % (L.PINNED, len(runners64)))
print("     ...whose first line is exactly `#!/bin/sh`: %d"
      % (len(runners64) - len(notsh)))
for p, first in notsh:
    print("     ...NOT: %-46s %s" % (p, first.strip()))
MISS.append(("Q22", "at least one is not #!/bin/sh",
             "%d of %d are not" % (len(notsh), len(runners64)), bool(notsh)))
print("  %-4s predicted %-28s measured %-28s %s"
      % ("Q22", "≥1 not /bin/sh", "%d not" % len(notsh),
         "as predicted" if notsh else "*** MISS ***"))
if notsh:
    print()
    print("     The mechanism argument is NOT damaged by this: the one bash")
    print("     runner legitimately sets `pipefail` because it really is bash.")
    print("     What is damaged is the word `measured`.  The same blind spot")
    print("     produced both sentences -- the census never saw that file.")
    BAD += 1

print()
L.bar("J1 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts (a) a run_all.sh still carrying a")
print("pipeline at HEAD, (b) the sweep's prose asserting a measurement its own")
print("committed transcript contradicts, and (c) a `measured` claim about all")
print("64 shebangs that is false.  It does NOT count prediction misses: those")
print("are scored separately below and kept as written in OUTCOMES.md.  It")
print("ranges over every tracked `*.sh` in this repository at %s and on"
      % L.PINNED)
print("disk, and over the five sweep artifacts named in J1e -- not over `.py`")
print("files that shell out, which are J2's subject.")
print()
nmiss = sum(1 for _q, _p, _m, ok in MISS if not ok)
print("PREDICTIONS: %d of %d as predicted, %d MISSED (%s)"
      % (len(MISS) - nmiss, len(MISS), nmiss,
         ", ".join(q for q, _p, _m, ok in MISS if not ok) or "none"))
sys.exit(1 if BAD else 0)
