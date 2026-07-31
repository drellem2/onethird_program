"""T1 -- THE GRAIN, EVERYWHERE.  For every count mg-70c7 prints: SITES or RUNS?

mg-dee4's largest finding was that *"11 of 11 read directly"* counted LINES
while the claim was about RUNS, and a line inside a `for` loop is N executions.
mg-70c7 repaired that.  This probe asks the same question of the repair:

  T1a  EVERY printed count row in mg-70c7's seven transcripts, classified by
       its OWN label as SITE-grain, EXECUTION-grain, BOTH or NONE.
  T1b  ONE LOOP, COUNTED BOTH WAYS by a parser written here -- sites beside
       executions, so the two numbers are visible together rather than one of
       them being reported as the other.
  T1c  `out_r4_property.txt` labels 43 and 10 `executing sites`.  Both numbers
       are re-derived here at TWO grains: (site, target) ROWS and distinct
       SITES.  If they differ, the label names one and prints the other.
  T1d  The same quantity as the README, the published document, the probe's
       OWN DOCSTRING and `OUTCOMES.md`'s scored prediction state it.
  T1e  The `c0_repro.sh` caller count, which three artifacts give three
       different values for.

WHAT THIS PROBE DOES NOT DO.  It does not decide whether a grain word is the
RIGHT one for a count -- that is a question about meaning.  It decides whether
the label and the sentence around it say the SAME thing, which is the checkable
half and the half mg-70c7 states it does not check.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib56dc as M

BAD = 0
FINDINGS = []

M.bar("T1  THE GRAIN -- FOR EVERY COUNT, SITES OR EXECUTIONS?")

# ---------------------------------------------------------------------------
M.hdr("T1a  EVERY PRINTED COUNT IN mg-70c7's TRANSCRIPTS, CLASSIFIED")

print("  POPULATION, NAMED: every line of mg-70c7's committed transcripts")
print("  that has the SHAPE of a printed count row -- a label, two or more")
print("  spaces, and an integer ending the line.  A shape rule over the line")
print("  and not a list of interesting labels: a hand-list of labels is how")
print("  this check would become the thing it audits.")
print()

SUBJ_OUTS = M.outs(M.SUBJECT)
by_class = {"EXECUTION": [], "SITE": [], "BOTH": [], "NONE": []}
by_stage = {"label": 0, "prev": 0, "header": 0, "-": 0}
header_only = []
for out in SUBJ_OUTS:
    text = M.read(out, None)
    lines = text.splitlines()
    for i, label, nums in M.count_rows(text):
        above = [lines[j] for j in range(i - 2, max(-1, i - 2 - 8), -1)]
        cls, stage = M.grain_of(label, above)
        by_class[cls].append((out, i, label, nums, stage))
        by_stage[stage] += 1
        if stage == "header":
            header_only.append((out, i, label, nums, cls))

total = sum(len(v) for v in by_class.values())
print("      transcripts read                                  %3d"
      % len(SUBJ_OUTS))
print("      printed count ROWS in them                        %3d" % total)
print()
print("  BY THE GRAIN THE ROW'S OWN LABEL CLAIMS:")
for k in ("EXECUTION", "SITE", "BOTH", "NONE"):
    print("      %-12s grain                                 %3d"
          % (k, len(by_class[k])))
print()
print("  BY HOW FAR AWAY THE GRAIN WORD HAD TO BE FOUND:")
print("      on the count's own label                          %3d"
      % by_stage["label"])
print("      on one of the TWO lines above  (mg-70c7's E1 window)  %3d"
      % by_stage["prev"])
print("      ONLY in a column header further up                %3d"
      % by_stage["header"])
print("      nowhere within %d lines                            %3d"
      % (M.HEADER_LOOKBACK, by_stage["-"]))
print()
print("  THE ROWS WHOSE GRAIN IS ONLY IN A COLUMN HEADER.  A table row takes")
print("  its grain from the header, which can be six lines away; mg-70c7's own")
print("  E1 window is the line and the two above it, so these rows are outside")
print("  the reach of the check that repairs F1.  That is F4's defect --")
print("  line-locality -- asked of the grain check instead of the marker check:")
print()
for out, i, label, nums, cls in header_only:
    print("      %-26s %4d  %-30s %-6s %s"
          % (os.path.basename(out), i, label[:30], cls,
             " ".join(str(n) for n in nums)))
if not header_only:
    print("      (none)")
print()
print("  THE `NONE` ROWS -- a count with no grain word within %d lines, which"
      % M.HEADER_LOOKBACK)
print("  is the shape mg-dee4 found.  Every one is printed, not folded away:")
print()
for out, i, label, nums, _s in by_class["NONE"][:24]:
    print("      %-26s %4d  %-34s %s"
          % (os.path.basename(out), i, label[:34],
             " ".join(str(n) for n in nums)))
if not by_class["NONE"]:
    print("      (none)")
print()
print("  AND EVERY ROW WHOSE LABEL CLAIMS THE EXECUTION GRAIN, in full,")
print("  because those are the ones mg-dee4's F1 is about -- a count of runs")
print("  must be a count of runs:")
print()
for out, i, label, nums, stage in by_class["EXECUTION"] + by_class["BOTH"]:
    print("      %-26s %4d  %-30s %-7s %s"
          % (os.path.basename(out), i, label[:30], stage,
             " ".join(str(n) for n in nums)))
print()
print("      count rows claiming the EXECUTION grain outright   %3d"
      % len(by_class["EXECUTION"]))
print("      ...and rows whose label carries BOTH grains        %3d"
      % len(by_class["BOTH"]))
print()
print("  EXTENT OF THIS CLASSIFICATION, stated rather than implied.  It reads")
print("  the WORD, not the meaning: a count labelled `executions` that is")
print("  really sites is classified EXECUTION here.  T1c is what catches that")
print("  case, by re-deriving one such count at BOTH grains rather than by")
print("  reading its label harder.")

# ---------------------------------------------------------------------------
M.hdr("T1b  ONE LOOP, COUNTED BOTH WAYS -- the two numbers side by side")

print("  Read at %s under a loop expander written in `lib56dc`, which shares" % M.PRE)
print("  no code with `lib7522` or `lib70c7`.  SITES is one row per source")
print("  line; EXECUTIONS is one row per run of that line.")
print()
RUNNERS = ("code/state_delegation_audit_16eb/run_all.sh",
           "code/state_delegation_repair_0049/run_all.sh")
TEE_RUNNERS = ("code/face_geometry_audit_f1b2/run_audit.sh",
               "code/face_geometry_audit_fcf1/run_audit.sh")
print("    %-34s %-14s %5s %10s  %s"
      % ("runner", "loop items", "SITES", "EXECUTIONS", "why"))
site_tot = exec_tot = 0
for rel in RUNNERS:
    src = M.read(rel, M.PRE)
    loops = M.for_loops(src)
    items = ", ".join("%d" % len(it) if it else "NOT EXPANDABLE"
                      for _v, it, _f, _l in loops) or "-"
    s = len(M.pipeline_sites(src, "git diff"))
    e = len(M.pipeline_executions(src, "git diff"))
    site_tot += s
    exec_tot += e
    print("    %-34s %-14s %5d %10d  %d line(s) x %s item(s)"
          % (os.path.basename(os.path.dirname(rel)), items, s, e, s, items))
for rel in TEE_RUNNERS:
    src = M.read(rel, M.PRE)
    loops = M.for_loops(src)
    s = len(M.pipeline_sites(src, "| tee"))
    e = len(M.pipeline_executions(src, "| tee"))
    print("    %-34s %-14s %5d %10d  no loop encloses a `| tee`"
          % (os.path.basename(os.path.dirname(rel)),
             "%d loop(s)" % len(loops), s, e))
print()
tee_s = sum(len(M.pipeline_sites(M.read(r, M.PRE), "| tee"))
            for r in TEE_RUNNERS)
tee_e = sum(len(M.pipeline_executions(M.read(r, M.PRE), "| tee"))
            for r in TEE_RUNNERS)
print("      `git diff`  SITES %2d   EXECUTIONS %2d   ratio %.2f"
      % (site_tot, exec_tot, exec_tot / max(site_tot, 1)))
print("      `| tee`     SITES %2d   EXECUTIONS %2d   ratio %.2f"
      % (tee_s, tee_e, tee_e / max(tee_s, 1)))
print("      -----------------------------------------------")
print("      TOTAL       SITES %2d   EXECUTIONS %2d"
      % (site_tot + tee_s, exec_tot + tee_e))
print()
print("  SO THE PUBLISHED `16 of 16` IS AT THE EXECUTION GRAIN and is sound:")
print("  the 8 `| tee` lines lie in no loop, so their site count and their")
print("  execution count are the same number for a reason, not by luck, and")
print("  that reason is printed above rather than assumed.  `out_s2_status.txt`")
print("  states the same breakdown; this is an independent derivation of it.")
if exec_tot + tee_e != 16 or site_tot + tee_s != 11:
    BAD += 1
    print("      *** the two grains do not come to 11 sites / 16 executions ***")

# ---------------------------------------------------------------------------
M.hdr("T1c  `executing sites` -- RE-DERIVED AT BOTH GRAINS")

TR = "%s/out_r4_property.txt" % M.SUBJECT
PUB = M.git("log", "-1", "--format=%H", "--", TR).strip()[:7]
print("  `out_r4_property.txt` prints `executing sites naming a *.sh  43` and")
print("  `...outside it  10`.  Both are re-derived here under a scan written")
print("  in `lib56dc`, at the ROW grain and at the SITE grain -- and at TWO")
print("  revisions, because a census over the whole repository moves with the")
print("  arc.  `%s` is the commit that PUBLISHED that transcript, read from" % PUB)
print("  `git log -1 -- <the transcript>` rather than named by hand:")
print()
TWO = ("run_all.sh", "run_audit.sh")
by_ref = {}
for ref, label in ((PUB, "at %s, the publishing commit" % PUB),
                   (None, "at HEAD, today")):
    rws = M.exec_site_rows(ref)
    out_rows = [r for r in rws if r[2] not in TWO]
    by_ref[ref] = (rws, out_rows, M.exec_sites(rws), M.exec_sites(out_rows))
    a, o, asites, osites = by_ref[ref]
    print("      %s" % label)
    print("          (site, target) ROWS            all %3d    outside %3d"
          % (len(a), len(o)))
    print("          distinct SITES                 all %3d    outside %3d"
          % (len(asites), len(osites)))
    print("          distinct basenames outside              %3d"
          % len({r[2] for r in o}))
    print("          outside rows READING the status         %3d"
          % sum(1 for r in o if r[3]))
    print()
rws, out_rows, all_sites, out_sites = by_ref[PUB]
dupes = {}
for f, i, base, _c in out_rows:
    dupes.setdefault((f, i), []).append(base)
multi = {k: v for k, v in dupes.items() if len(v) > 1}
print("  THE DIFFERENCE, NAMED SITE BY SITE, at the publishing commit.  A line")
print("  that executes something and names two different shell scripts is ONE")
print("  site and TWO rows:")
print()
for (f, i), bases in sorted(multi.items()):
    print("      %s:%d" % (f, i))
    print("          names %s -- counted %d times under the `sites` label"
          % (", ".join("`%s`" % b for b in bases), len(bases)))
    src = M.read(f, PUB).splitlines()
    print("          %s" % src[i - 1].strip()[:66])
if not multi:
    print("      (no site names more than one script)")
print()
tr = M.read(TR, None)
printed_all = re.search(r"executing sites naming a `\*\.sh`\s+(\d+)", tr)
printed_out = re.search(r"outside it, across \d+ distinct basenames\s+(\d+)",
                        tr)
pa = int(printed_all.group(1)) if printed_all else None
po = int(printed_out.group(1)) if printed_out else None
print("      the transcript prints, under the label `executing sites`:")
print("          all      %s      outside the two names   %s" % (pa, po))
print("      this derivation at the same commit, ROW grain:")
print("          all      %s      outside the two names   %s"
      % (len(rws), len(out_rows)))
print("      ...and at the SITE grain:")
print("          all      %s      outside the two names   %s"
      % (len(all_sites), len(out_sites)))
print()
print("  WHICH OF THOSE REPRODUCE, and which do not -- named rather than")
print("  averaged.  The OUTSIDE column reproduces exactly at both revisions.")
print("  The ALL column does not: the whole-repository census moved between")
print("  the run that wrote the transcript and the commit that ships it,")
print("  which is what a repository-wide census does while an arc is landing.")
print("  This probe therefore rests its finding on the column that")
print("  reproduces, and prints the one that does not rather than dropping it.")
print()
live_rc, live_out = M.run_argv(["python3", "-B", "r4_property.py"],
                               os.path.join(M.REPO, M.SUBJECT))
m_live = re.search(r"outside it, across \d+ distinct basenames\s+(\d+)",
                   live_out)
live_po = int(m_live.group(1)) if m_live else None
print("      mg-70c7's OWN probe, re-run here at HEAD, exit %s" % live_rc)
print("      ...prints, under the label `executing sites`, outside:  %s"
      % live_po)
print("      this instrument, same rule, ROW grain, at HEAD:         %d"
      % len(by_ref[None][1]))
print("      ...at the SITE grain:                                   %d"
      % len(by_ref[None][3]))
if live_po != len(by_ref[None][1]):
    BAD += 1
    print("      *** THIS INSTRUMENT disagrees with the live probe on the ROW")
    print("          count -- that is a defect of mine, not a finding ***")
print()
if live_po == len(by_ref[None][1]) and len(out_rows) != len(out_sites):
    FINDINGS.append(M.finding(
        "T1c",
        "`out_r4_property.txt` labels its outside-the-two-names count %d "
        "`executing sites`; it is a count of (SITE, TARGET) MATCH ROWS, "
        "reproduced exactly here at the publishing commit %s and at HEAD, and "
        "by mg-70c7's own probe re-run live.  The distinct-SITE count is %d.  "
        "One source line -- %s -- names two different `*.sh` and is counted "
        "twice under a label that says `sites`.  The repair whose thesis is "
        "that a count must say what it ranges over prints a row count under a "
        "site label"
        % (po, PUB, len(out_sites),
           ", ".join("%s:%d" % k for k in sorted(multi)))))
    print("      *** the label says SITES and the number counts ROWS ***")

# ---------------------------------------------------------------------------
M.hdr("T1d  THE SAME QUANTITY, AS FOUR ARTIFACTS STATE IT")

print("  A count is not repaired until the sentence carrying it is.  The")
print("  quantity is `executing sites at HEAD naming a *.sh whose basename is")
print("  neither run_all.sh nor run_audit.sh`.  Where each artifact states it:")
print()
WHERE = [("%s/README.md" % M.SUBJECT, "README.md"),
         (M.SUBJECT_DOC, "the published document"),
         ("%s/r4_property.py" % M.SUBJECT, "r4_property.py (its OWN docstring)"),
         ("%s/OUTCOMES.md" % M.SUBJECT, "OUTCOMES.md (the scored R5a)"),
         ("%s/out_r4_property.txt" % M.SUBJECT, "out_r4_property.txt")]
STATED = re.compile(r"(\d+)\s+(?:executing\s+)?sites?\b[^\n]{0,60}?"
                    r"(?:basename is neither|outside the two names)")
rowsx = []
print("    %-38s %-30s %s" % ("artifact", "at", "states"))
for rel, label in WHERE:
    text = M.read(rel, None)
    for i, line in enumerate(text.splitlines(), 1):
        m = STATED.search(line)
        if not m:
            continue
        v = next(g for g in m.groups() if g)
        rowsx.append((label, "%s:%d" % (os.path.basename(rel), i), v,
                      line.strip()))
        print("    %-38s %-30s %s"
              % (label, "%s:%d" % (os.path.basename(rel), i), v))
        print("        %s" % line.strip()[:70])
print()
stated_vals = {int(r[2]) for r in rowsx}
print("      places stating the quantity in prose         %3d" % len(rowsx))
print("      distinct values stated for it                %3d"
      % len(stated_vals))
print("      the value its own instrument prints          %3d" % (po or -1))
print("      the value at the SITE grain                  %3d" % len(out_sites))
print()
if len(stated_vals) > 1 or (stated_vals and po not in stated_vals):
    FINDINGS.append(M.finding(
        "T1d",
        "the quantity `executing sites at HEAD outside the two names` is "
        "stated as %s at %d places -- %s -- while the transcript those "
        "artifacts point at prints %s and mg-70c7's own probe re-run live "
        "prints %s.  %s is the distinct-SITE count and %s is the ROW count, "
        "so the prose is right about the grain its own instrument does not "
        "print, and `r4_property.py`'s docstring adds that this is \"a "
        "measurement and not a citation of mg-dee4\" -- it is a citation of "
        "mg-dee4, which measured %s before the both-senses fixtures landed"
        % ("/".join(str(v) for v in sorted(stated_vals)), len(rowsx),
           ", ".join(r[1] for r in rowsx), po, live_po,
           len(out_sites), len(out_rows),
           sorted(stated_vals)[0] if stated_vals else "?")))
    print("      *** the artifacts and their own transcript state two ***")
    print("      *** different numbers for one quantity                ***")

# ---------------------------------------------------------------------------
M.hdr("T1e  THE `c0_repro.sh` CALLER COUNT -- three artifacts, three numbers")

print("  The same shape once more, on the F6 instance.  Who reads that")
print("  script's exit status?  `r5_population.py`'s own rule is reproduced")
print("  here -- a line naming `c0_repro.sh` and matching")
print("  `returncode|subprocess.|exits`, excluding the script itself -- so the")
print("  comparison is with the rule that printed the number and not with a")
print("  stricter one of mine.  Counted with and without the instrument trees:")
print()
SITE_F = "code/branching_audit_a218/c0_repro.sh"
R5RULE = re.compile(r"returncode|subprocess\.|exits")
readers = []
for f in [x for x in M.git("ls-files", "--", "*.py", "*.sh").splitlines() if x]:
    if f == SITE_F:
        continue
    try:
        s = M.read(f, None)
    except (RuntimeError, OSError):
        continue
    for i, l in enumerate(s.split("\n"), 1):
        if "c0_repro.sh" in l and R5RULE.search(l):
            readers.append((f, i))
INSTR = (M.SUBJECT, M.TREE, M.S7522, M.DEE4)
external = [s for s in readers if not s[0].startswith(INSTR)]
print("      sites, all                                   %3d in %d file(s)"
      % (len(readers), len({f for f, _i in readers})))
print("      ...excluding every instrument tree in this arc %1d in %d file(s)"
      % (len(external), len({f for f, _i in external})))
print()
for f, i in readers:
    print("          %-58s %s" % ("%s:%d" % (f, i),
                                  "AN INSTRUMENT'S OWN LINE"
                                  if f.startswith(INSTR) else ""))
print()
CLAIMS = [("%s/out_r5_population.txt" % M.SUBJECT,
           r"status read:\s+(\d+) in (\d+) file"),
          (M.SUBJECT_DOC, r"(nine|\d+)\s+sites\s+in\s+(four|three|\d+)\s+files"),
          ("%s/lib7522.py" % M.S7522,
           r"read by (nine|\d+)\s+sites\s+in\s+(three|four|\d+)\s+files"),
          ("%s/out_a1_outside.txt" % M.DEE4,
           r"and (\d+) external caller\(s\) read that status")]
seenvals = []
for rel, rx in CLAIMS:
    text = M.read(rel, None)
    m = re.search(rx, text)
    val = (m.group(1), m.group(2) if m.lastindex and m.lastindex > 1 else "-") \
        if m else ("-", "-")
    seenvals.append(val)
    print("      %-56s %s sites / %s files"
          % (os.path.basename(rel), val[0], val[1]))
print()
vals = {v[0] for v in seenvals if v[0] != "-"}
if len(vals) > 1:
    FINDINGS.append(M.finding(
        "T1e",
        "one quantity -- the sites reading `c0_repro.sh`'s exit status -- is "
        "published as %s.  Re-derived here under `r5_population.py`'s own "
        "rule: %d sites in %d files counting every instrument tree's own "
        "lines, %d in %d without them.  The published numbers differ by "
        "whether the instrument counts itself and by sites against files, and "
        "no artifact says which reading it is at -- which is the same defect "
        "as a count that does not say whether it ranges over sites or runs"
        % (" / ".join("%s sites in %s files" % v for v in seenvals),
           len(readers), len({f for f, _i in readers}),
           len(external), len({f for f, _i in external}))))
    print("      *** four artifacts, more than one reading, none of them   ***")
    print("      *** stating whether the instrument's own line is counted  ***")

print()
M.bar("T1 TOTAL FINDINGS: %d   TOTAL BAD: %d" % (len(FINDINGS), BAD))
print()
for f in FINDINGS:
    print(f)
print()
print("EXTENT OF THOSE NUMBERS.  TOTAL BAD counts a failure of THIS")
print("instrument -- a loop expansion that does not come to 11 sites / 16")
print("executions, or a row-grain derivation that disagrees with the")
print("transcript it is re-deriving.  TOTAL FINDINGS counts a label whose")
print("grain differs from the number it prints, or a quantity published at")
print("two grains without saying which.  It ranges over mg-70c7's %d"
      % len(SUBJ_OUTS))
print("transcripts, its 4 reader-facing artifacts, and every tracked `*.py`")
print("and `*.sh` at HEAD.  It does NOT range over mg-c2b3's 34, which are")
print("inherited from a transcript nobody in this chain has re-run.")
sys.exit(min(len(FINDINGS) + BAD, 120))
