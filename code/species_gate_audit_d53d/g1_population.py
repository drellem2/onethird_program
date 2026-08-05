"""G1 -- THE DELETION POPULATION, CHECKED FROM OUTSIDE ITS OWN DEFINITION.

mg-6ef4's finding was not "`set -e` was load-bearing".  It was:

    the line whose removal breaks the gate was OUTSIDE THE POPULATION THAT
    CERTIFIES THE GATE -- and the exclusion looks like nothing, because the
    certificate still reads 100%.

mg-4adb answered by making the population EVERY LINE OF THE RUNNER FILE, with
no exclusion list.  This section does not read that definition and check it
looks complete.  It takes the source, deletes each line in turn ITSELF, and
records which deletions the certified population would have missed.

And it asks the question of THE WHOLE VERDICT PATH, not of the file mg-4adb
chose.  A red verdict travels:

    e2_crosssection.py -> its process exit code -> the runner's exit code
                       -> the reader

so the path is the three runners (255 lines) PLUS `e2_crosssection.py` (299)
PLUS `kernd633.py` (252), which computes the finding.  806 lines, of which
mg-4adb's certificate covers the first 255.  Every one of the 806 is deleted
here.

  G1a  the population, stated, and re-derived rather than quoted
  G1b  the attribution control -- e2 red, runners unmodified, both directions
  G1c  every line of every runner, deleted alone, with the strike live
  G1d  those 255 dispositions against mg-4adb's own 255 rows, row for row
  G1e  what the certified population contains, read out of that transcript
  G1f  every line of e2_crosssection.py, deleted alone, with the strike live
  G1g  each G1f survivor, with the three runners executed
  G1h  every line of kernd633.py, deleted alone
  G1i  the arithmetic: deletions that lose the gate, inside and outside

    python3 code/species_gate_audit_d53d/g1_population.py
"""

import os
import re
import sys

from kern_d53d import (hdr, Rows, REPO, RUNNERS, E2, KERN, CALL, SETE,
                       E2_SAYS, Pool, clone, run_runner, run_e2, plant_strike,
                       unplant_strike, source_lines, Deletion, disposition,
                       cleanup)

WORKERS = int(os.environ.get("D53D_WORKERS", "6"))
R = Rows()

# mg-4adb's transcript.  It is read ONLY here, only as the object of a
# measurement, and never as the source of a figure this audit reports as its
# own -- G1a re-derives every count in it from the source first.
V1 = os.path.join(REPO, "code", "species_rung_repair_4adb",
                  "out_v1_population.txt")


# ---------------------------------------------------------------------------
hdr("G1a  THE POPULATION, STATED -- AND EVERY COUNT RE-DERIVED")
# ---------------------------------------------------------------------------

base = clone()
RUNNER_RELS = [os.path.join("code", r, "run_all.sh") for r in RUNNERS]
runner_src = {rel: source_lines(base, rel) for rel in RUNNER_RELS}
e2_src = source_lines(base, E2)
kern_src = source_lines(base, KERN)

R.note("Counted from the source in the sandbox, not quoted from any document:")
for rel in RUNNER_RELS:
    R.note("    %-46s %3d lines" % (rel, len(runner_src[rel])))
n_runner = sum(len(v) for v in runner_src.values())
R.note("    %-46s %3d lines" % ("(the three runners)", n_runner))
R.note("    %-46s %3d lines" % (E2, len(e2_src)))
R.note("    %-46s %3d lines" % (KERN, len(kern_src)))
n_path = n_runner + len(e2_src) + len(kern_src)
R.note("    %-46s %3d lines" % ("THE VERDICT PATH", n_path))
print()

R.predicted(
    "disc.4",
    "83, 85 and 87 (255); e2 299; kernd633 252 -- counted from the source "
    "before any probe existed",
    "%s (%d); e2 %d; kernd633 %d"
    % (", ".join(str(len(runner_src[rel])) for rel in RUNNER_RELS),
       n_runner, len(e2_src), len(kern_src)),
    [len(runner_src[rel]) for rel in RUNNER_RELS] == [83, 85, 87]
    and len(e2_src) == 299 and len(kern_src) == 252,
    "PREDICTIONS.md discloses this count as already made.  It is scored so\n"
    "that a reader can see the disclosure was true, not so that it counts\n"
    "as a hit.")

R.note("")
R.note("NO EXCLUSION LIST.  Every line of every one of the five files above is")
R.note("deleted below, one at a time, with the file restored afterwards --")
R.note("blank lines, comments, the shebang and the docstrings included.  There")
R.note("is no line here whose exclusion has to be justified, which is the only")
R.note("answer to mg-6ef4's F3 that does not rest on somebody having guessed")
R.note("correctly which lines matter.")
R.note("")
R.note("TOTAL PROCESS EXECUTIONS IN G1c/G1f/G1h: %d runner runs + %d e2 runs"
       % (n_runner, len(e2_src) + len(kern_src)))


# ---------------------------------------------------------------------------
hdr("G1b  THE ATTRIBUTION CONTROL -- BOTH DIRECTIONS")
# ---------------------------------------------------------------------------

R.note("Nothing below means anything if the planted strike does not make the")
R.note("runners red, and it means the WRONG thing if they are red for any")
R.note("other reason.  Both are measured, and the clean tree first: an")
R.note("instrument that reddens a correct tree is measuring itself.")
print()

clean = {}
for rn in RUNNERS:
    rc, out = run_runner(base, rn)
    clean[rn] = (rc, E2_SAYS in out)
    R.note("    CLEAN  %-26s exit %-4s prints %s: %s"
           % (rn, rc, E2_SAYS, "yes" if E2_SAYS in out else "no"))
R.row("3 of 3 runners GREEN on a clean tree and e2 silent",
      all(rc == 0 and not says for rc, says in clean.values()))
print()

plant_strike(base)
rc_e2, out_e2 = run_e2(base)
n_standing = out_e2.count("*** %s ***" % E2_SAYS)
R.note("    e2 alone, strike planted: exit %s, %d occurrence(s) STANDING"
       % (rc_e2, n_standing))
R.row("the plant arms exactly one finding and e2 exits non-zero",
      rc_e2 == 1 and n_standing == 1,
      "kernd633.NEGATES exonerates on refut/struck/misquot/corrected/\n"
      "retract and eleven more.  A plant whose restating paragraph trips one\n"
      "of them is silently exonerated and every sweep below would then be\n"
      "measuring a green tree.  That is why this row exists.")

red = {}
for rn in RUNNERS:
    rc, out = run_runner(base, rn)
    tot = re.findall(r"^([A-Z0-9_]+ TOTAL BAD): (\d+)", out, re.M)
    others = [(k, v) for k, v in tot if not k.startswith("E2")]
    red[rn] = (rc, E2_SAYS in out, others)
    R.note("    RED    %-26s exit %-4s prints %s: %s"
           % (rn, rc, E2_SAYS, "yes" if E2_SAYS in out else "no"))
    R.note("           every OTHER total in that run: %s"
           % (", ".join("%s %s" % kv for kv in others) or "(none)"))
R.row("3 of 3 runners RED, and red BECAUSE of e2 and nothing else",
      all(rc == 1 and says and all(v == "0" for _k, v in others)
          for rc, says, others in red.values()),
      "The third column is the attribution: if any other checker in the run\n"
      "also went non-zero, a deletion sweep below could be reading its\n"
      "verdict and calling it the gate's.")


# ---------------------------------------------------------------------------
hdr("G1c  EVERY LINE OF EVERY RUNNER, DELETED ALONE, WITH THE STRIKE LIVE")
# ---------------------------------------------------------------------------

R.note("One row per line.  The three dispositions, defined once and applied")
R.note("everywhere in this instrument:")
R.note("")
R.note("  GATE HELD            runner non-zero AND e2's sentence in its output")
R.note("  GATE LOST            runner exited 0.  THE CLASS THIS ARC IS ABOUT.")
R.note("  DIED BEFORE THE GATE runner non-zero, e2 never spoke")
R.note("")
R.note("GATE LOST is decided on the exit code alone: that is what a reader's")
R.note("`&&` sees.  Whether the finding was printed anyway is the next column")
R.note("and is never a mitigation -- mg-6ef4's whole finding is a case where")
R.note("it WAS printed.")
print()

tasks = []
for rel in RUNNER_RELS:
    for i in range(len(runner_src[rel])):
        tasks.append((rel, i))
# interleave, so one slow runner does not serialise the pool at the end
tasks.sort(key=lambda t: (t[1], t[0]))

pool = Pool(WORKERS)
for root in pool.roots:
    plant_strike(root)


def sweep_runner(root, task):
    rel, i = task
    runner = rel.split(os.sep)[1]
    with Deletion(root, rel, i) as d:
        rc, out = run_runner(root, runner)
    return (rel, i, d.text, rc, disposition(rc, out), E2_SAYS in out)


sys.stderr.write("  G1c: %d runner executions on %d sandboxes\n"
                 % (len(tasks), WORKERS))
res = pool.map(tasks, sweep_runner, progress=25)
by_rel = {}
for rel, i, text, rc, disp, says in res:
    by_rel.setdefault(rel, {})[i] = (text, rc, disp, says)

MINE = {}
for rel in RUNNER_RELS:
    print("  %s" % rel)
    rows = by_rel[rel]
    for i in sorted(rows):
        text, rc, disp, says = rows[i]
        MINE[(rel, i + 1)] = (rc, disp, says)
        print("      line %3d  exit %-4s %-20s finding printed: %-4s %s"
              % (i + 1, rc, disp, "yes" if says else "no", text[:38]))
    print()

lost = {rel: [i + 1 for i in sorted(by_rel[rel])
              if by_rel[rel][i][2] == "GATE LOST"] for rel in RUNNER_RELS}
per = [len(lost[rel]) for rel in RUNNER_RELS]
lost_text = {rel: [by_rel[rel][i - 1][0] for i in lost[rel]]
             for rel in RUNNER_RELS}

for rel in RUNNER_RELS:
    R.note("  %-46s GATE LOST at line(s) %s"
           % (rel, ", ".join(str(x) for x in lost[rel]) or "(none)"))
    for t in lost_text[rel]:
        R.note("        %s" % t)

all_lost_are_call = all(t.strip() == CALL for rel in RUNNER_RELS
                        for t in lost_text[rel])
R.predicted(
    "Q1", "1, 1, 1 -- and in each case the line is `%s`" % CALL,
    "%s -- %s" % (", ".join(str(p) for p in per),
                  "every one of them is that call" if all_lost_are_call
                  else "NOT all of them are that call"),
    per == [1, 1, 1] and all_lost_are_call,
    "This is mg-4adb's own headline figure, re-derived by an instrument that\n"
    "shares no code with it.  If it had not reproduced, that would have been\n"
    "a larger finding than anything else in this audit.")

counts = {}
for v in MINE.values():
    counts[v[1]] = counts.get(v[1], 0) + 1
R.note("")
R.note("  dispositions over the 255: %s"
       % ", ".join("%s %d" % kv for kv in sorted(counts.items())))
printed_while_lost = [k for k, v in MINE.items()
                      if v[1] == "GATE LOST" and v[2]]
R.note("  of the GATE LOST rows, %d printed e2's finding anyway"
       % len(printed_while_lost))


# ---------------------------------------------------------------------------
hdr("G1d  MY 255 DISPOSITIONS AGAINST mg-4adb's OWN 255 ROWS")
# ---------------------------------------------------------------------------

R.note("mg-4adb's transcript is read here as the OBJECT of a measurement.  Its")
R.note("vocabulary is `gate fired` / `GATE LOST` / `BROKE EARLY`; mine is the")
R.note("three above.  The mapping is stated, and then every row is compared:")
R.note("    gate fired  <-> GATE HELD      BROKE EARLY <-> DIED BEFORE THE GATE")
print()

MAP = {"gate fired": "GATE HELD", "GATE LOST": "GATE LOST",
       "BROKE EARLY": "DIED BEFORE THE GATE"}
THEIRS = {}
cur = None
with open(V1, encoding="utf-8") as fh:
    for ln in fh:
        m = re.match(r"^  (code/\S+/run_all\.sh)\s*$", ln)
        if m:
            cur = m.group(1).replace("/", os.sep)
            continue
        m = re.match(r"^      line\s+(\d+)\s+exit (\S+)\s+"
                     r"(gate fired|GATE LOST|BROKE EARLY)\s+"
                     r"finding printed: (yes|no)", ln)
        if m and cur:
            THEIRS[(cur, int(m.group(1)))] = (int(m.group(2)),
                                              MAP[m.group(3)],
                                              m.group(4) == "yes")

R.note("  rows parsed out of mg-4adb's out_v1_population.txt: %d" % len(THEIRS))
agree = [k for k in MINE if k in THEIRS and MINE[k] == THEIRS[k]]
differ = [k for k in MINE if k in THEIRS and MINE[k] != THEIRS[k]]
absent = [k for k in MINE if k not in THEIRS]
for k in sorted(differ):
    R.note("  DIFFERS  %s line %d: mine %s, theirs %s"
           % (k[0], k[1], MINE[k], THEIRS[k]))
for k in sorted(absent):
    R.note("  NOT IN THEIRS  %s line %d" % k)

R.predicted(
    "Q2", "255 of 255 agree, row for row",
    "%d of %d agree; %d differ; %d of mine have no row there"
    % (len(agree), len(MINE), len(differ), len(absent)),
    len(agree) == len(MINE) == 255 and not differ and not absent,
    "Exit code, disposition and finding-printed all three, per row.")


# ---------------------------------------------------------------------------
hdr("G1e  WHAT THE CERTIFIED POPULATION CONTAINS")
# ---------------------------------------------------------------------------

files_in_cert = sorted(set(k[0] for k in THEIRS))
outside_runners = [f for f in files_in_cert if f not in RUNNER_RELS]
R.note("  files enumerated by the certified population:")
for f in files_in_cert:
    R.note("      %-52s %3d row(s)"
           % (f, len([1 for k in THEIRS if k[0] == f])))
R.predicted(
    "Q3", "255 rows, and 0 of them a line of a file other than the three runners",
    "%d rows, %d of them outside the three runners"
    % (len(THEIRS), sum(1 for k in THEIRS if k[0] not in RUNNER_RELS)),
    len(THEIRS) == 255 and not outside_runners)

R.note("")
R.note("  So `e2_crosssection.py` (%d lines) and `kernd633.py` (%d) -- which"
       % (len(e2_src), len(kern_src)))
R.note("  BETWEEN THEM DECIDE THE EXIT CODE THE RUNNER RETURNS -- are outside")
R.note("  it, exactly as `set -e` was outside the three populations that")
R.note("  preceded mg-4adb's.  G1f and G1h ask what that costs.")


# ---------------------------------------------------------------------------
hdr("G1f  EVERY LINE OF e2_crosssection.py, DELETED ALONE, STRIKE LIVE")
# ---------------------------------------------------------------------------

R.note("Same rule, same three dispositions, and the same no-exclusion-list.")
R.note("EVERY ROW IS PRINTED, here and in G1h, as mg-4adb prints all 255 of")
R.note("its own.  A section that shows only the rows that fired reports its")
R.note("population as a number, and a number standing in for a population is")
R.note("the thing this audit is about.")
R.note("Here `GATE LOST` means: e2 exited 0 with the strike live -- so the")
R.note("runner whose last command it is exits 0 too, and the reader is told")
R.note("nothing.  The column after it says whether the finding was printed")
R.note("while that happened.")
print()


def sweep_e2(root, task):
    rel, i = task
    with Deletion(root, rel, i) as d:
        rc, out = run_e2(root)
    return (rel, i, d.text, rc, disposition(rc, out), E2_SAYS in out)


e2_tasks = [(E2, i) for i in range(len(e2_src))]
sys.stderr.write("  G1f: %d e2 executions\n" % len(e2_tasks))
e2_res = pool.map(e2_tasks, sweep_e2, progress=50)

e2_lost = []
print("  %s" % E2)
for rel, i, text, rc, disp, says in sorted(e2_res, key=lambda r: r[1]):
    print("      line %3d  exit %-6s %-20s finding printed: %-4s %s"
          % (i + 1, rc, disp, "yes" if says else "no", text[:36]))
    if disp == "GATE LOST":
        e2_lost.append((i + 1, text, says))

e2_counts = {}
for _rel, _i, _t, _rc, disp, _s in e2_res:
    e2_counts[disp] = e2_counts.get(disp, 0) + 1
print()
R.note("  dispositions over the %d: %s"
       % (len(e2_res), ", ".join("%s %d" % kv for kv in sorted(e2_counts.items()))))
print()
for n, text, says in e2_lost:
    R.note("  GATE LOST  line %3d  finding printed: %-4s  %s"
           % (n, "yes" if says else "no", text.strip()[:60]))

R.predicted(
    "Q4", "2 -- `bad += len(fires)` and `sys.exit(1 if bad else 0)` -- "
          "and both print the finding",
    "%d: %s; finding printed on %d of them"
    % (len(e2_lost), "; ".join(t.strip()[:44] for _n, t, _s in e2_lost),
       sum(1 for _n, _t, s in e2_lost if s)),
    len(e2_lost) == 2
    and sorted(t.strip() for _n, t, _s in e2_lost)
    == sorted(["bad += len(fires)", "sys.exit(1 if bad else 0)"])
    and all(s for _n, _t, s in e2_lost),
    "THE PRIMARY CLAIM OF THIS AUDIT, first half.")


# ---------------------------------------------------------------------------
hdr("G1g  EACH OF THOSE LINES, WITH THE THREE RUNNERS EXECUTED")
# ---------------------------------------------------------------------------

R.note("e2's own exit code is not the finding.  The finding is what a READER")
R.note("of the runner sees, so each line above is deleted again and all three")
R.note("runners are run over it.")
print()

g1g = []
for n, text, _s in e2_lost:
    for rn in RUNNERS:
        with Deletion(base, E2, n - 1):
            rc, out = run_runner(base, rn)
        says = E2_SAYS in out
        g1g.append((n, rn, rc, says))
        R.note("    e2 line %-4d %-26s exit %-4s prints %s: %s"
               % (n, rn, rc, E2_SAYS, "yes" if says else "no"))

R.predicted(
    "Q5", "6 of 6 exit 0, and 6 of 6 print `%s` while doing it" % E2_SAYS,
    "%d of %d exit 0; %d of %d print it"
    % (sum(1 for _n, _r, rc, _s in g1g if rc == 0), len(g1g),
       sum(1 for _n, _r, _rc, s in g1g if s), len(g1g)),
    len(g1g) == 6 and all(rc == 0 and s for _n, _r, rc, s in g1g),
    "THE PRIMARY CLAIM OF THIS AUDIT, second half: a green runner printing\n"
    "the finding in full.  That is mg-6ef4's F3 word for word, one level\n"
    "down the same verdict path, after the repair that closed it.")

if g1g and all(rc == 0 for _n, _r, rc, _s in g1g):
    R.row("the class mg-6ef4 found is still reachable on this path", False,
          "Recorded as a finding of THIS instrument, not of mg-4adb's: the\n"
          "repair did what its ticket asked and its own certificate is\n"
          "honest.  What is wrong is the SCOPE of the population, which is\n"
          "the same shape of error the repair was written to answer.")


# ---------------------------------------------------------------------------
hdr("G1h  EVERY LINE OF kernd633.py, DELETED ALONE, STRIKE LIVE")
# ---------------------------------------------------------------------------

kern_tasks = [(KERN, i) for i in range(len(kern_src))]
sys.stderr.write("  G1h: %d e2 executions\n" % len(kern_tasks))
kern_res = pool.map(kern_tasks, sweep_e2, progress=50)

kern_lost = []
print("  %s" % KERN)
for rel, i, text, rc, disp, says in sorted(kern_res, key=lambda r: r[1]):
    print("      line %3d  exit %-6s %-20s finding printed: %-4s %s"
          % (i + 1, rc, disp, "yes" if says else "no", text[:36]))
    if disp == "GATE LOST":
        kern_lost.append((i + 1, text, says))

k_counts = {}
for _rel, _i, _t, _rc, disp, _s in kern_res:
    k_counts[disp] = k_counts.get(disp, 0) + 1
print()
R.note("  dispositions over the %d: %s"
       % (len(kern_res), ", ".join("%s %d" % kv for kv in sorted(k_counts.items()))))

for n, text, says in kern_lost:
    R.note("  GATE LOST  line %3d  finding printed: %-4s  %s"
           % (n, "yes" if says else "no", text.strip()[:60]))

R.predicted(
    "Q6", "0 -- Python's indentation turns most of them into a raise, and "
          "E2b's controls catch the ones that quietly disable the detector",
    "%d" % len(kern_lost),
    len(kern_lost) == 0,
    "E2b is e2's own control block: five constructed documents it must fire\n"
    "on or stay silent for.  A deletion that disables the detector without\n"
    "raising is caught there and counted into `bad`, so the gate holds.")

if kern_lost:
    for n, text, says in kern_lost:
        R.row("kernd633.py line %d loses the gate" % n, False,
              "%s\nfinding printed: %s" % (text.strip(), says))
    R.note("")
    R.note("  Each of these is run through all three runners, because e2's")
    R.note("  exit code is not what a reader sees:")
    for n, text, _s in kern_lost:
        for rn in RUNNERS:
            with Deletion(base, KERN, n - 1):
                rc, out = run_runner(base, rn)
            R.note("    kernd633 line %-4d %-26s exit %-4s prints %s: %s"
                   % (n, rn, rc, E2_SAYS, "yes" if E2_SAYS in out else "no"))


# ---------------------------------------------------------------------------
hdr("G1i  THE ARITHMETIC")
# ---------------------------------------------------------------------------

inside = sum(per)
outside = len(e2_lost) + len(kern_lost)
R.note("  verdict path                                        %3d lines"
       % n_path)
R.note("  covered by mg-4adb's certified population           %3d lines"
       % len(THEIRS))
R.note("  NOT covered                                         %3d lines"
       % (n_path - len(THEIRS)))
R.note("")
R.note("  deletions that lose the gate, INSIDE that population %3d" % inside)
R.note("  deletions that lose the gate, OUTSIDE it             %3d" % outside)
R.note("")
R.note("  and the certificate over the covered %d reads 100%% -- correctly."
       % len(THEIRS))

R.predicted(
    "Q7", "2, against a verdict path of 806 lines of which the certificate "
          "covers 255",
    "%d, against a verdict path of %d lines of which the certificate covers %d"
    % (outside, n_path, len(THEIRS)),
    outside == 2 and n_path == 806 and len(THEIRS) == 255)

R.tail("G1")
print()
print("EXTENT OF THAT NUMBER.  It ranges over %d runner executions in G1c,"
      % n_runner)
print("%d e2 executions in G1f, %d in G1h, %d runner executions in G1g and"
      % (len(e2_src), len(kern_src), len(g1g)))
print("%d in G1b -- every one of them this instrument's own, in a git clone of"
      % (2 * len(RUNNERS)))
print("this worktree, none of them read from any transcript.  IT RANGES OVER")
print("NOTHING ELSE: the population is the three runner files, e2 and its")
print("kernel, and a deletion is one line of one of those five.  Two lines")
print("deleted together, a line EDITED rather than removed, and every other")
print("file the runners call -- s1_extent.py, w3_scope.py, r2_columns.py and")
print("the rest -- are outside it and this number says nothing about them.")
print("mg-4adb's population is a strict subset of this one and G1d compares")
print("the overlap row for row rather than trusting either.")

cleanup()
sys.exit(1 if R.bad else 0)
