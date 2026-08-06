"""P2 -- EVERY LINE OF THE WIDENED POPULATION, DELETED, BEFORE AND AFTER.

mg-d53d deleted all 806 lines of the verdict path and found SIX deletions
outside mg-4adb's certified 255 that turn a red gate green, FOUR OF THEM
SILENTLY.  Naming a hole is not closing one, and a claim that it is closed,
unaccompanied by a demonstration of the gate firing on each case, is exactly
the kind of assertion this arc's audits keep refuting.

So each of the two files is swept twice -- at its PRE-REPAIR content and at its
repaired content -- and every one of mg-d53d's six is then deleted again with
ALL THREE RUNNERS EXECUTED OVER IT, because e2's own exit code is not what a
reader sees.

  P2a  the tree this sweep runs against, and the attribution control
  P2b  every line of the two files AT THEIR PRE-REPAIR CONTENT
  P2c  every line of the two files AS REPAIRED
  P2d  mg-d53d's six, at the repaired tree, THROUGH ALL THREE RUNNERS
  P2e  loudness: what each of the six now PRINTS while going red
  P2f  the arithmetic

THE SIX ARE ADDRESSED BY CONTENT.  This repair edits both files, so all six of
mg-d53d's line numbers are already wrong -- mg-7522's S3, which is why
`kern1d26.SIX_PRE` and `SIX_POST` carry each line's own text and the text of
the line after it, and `locate()` refuses an entry that does not match exactly
once.  The third entry is the one whose TEXT changed and its correspondence is
written down: `sys.exit(1 if bad else 0)` was the only line in e2 that could
deliver a verdict and `deliver("E2", ...)` is.

    MG1D26_WORKERS=6 python3 code/verdict_path_repair_1d26/p2_widened.py
"""

import os
import sys

from kern1d26 import (hdr, Rows, REPO, RUNNERS, E2, KERN, E2_SAYS,
                      SIX_PRE, SIX_POST, SIX_LABEL, LIVE,
                      Pool, Deletion, cleanup, clone, neutralise, plant,
                      unplant, pre_pair, post_pair, run_e2, run_runner,
                      source_lines, locate, disposition, attribution)

WORKERS = int(os.environ.get("MG1D26_WORKERS", "6"))
R = Rows()


# ---------------------------------------------------------------------------
hdr("P2a  THE TREE THIS SWEEP RUNS AGAINST, AND THE ATTRIBUTION CONTROL")
# ---------------------------------------------------------------------------

R.note("Nothing below means anything if the plant does not make the checker")
R.note("red, and it means the WRONG thing if the checker is red for any other")
R.note("reason -- which on this tree it IS, before anything is planted.")
print()

base = clone()

rc_raw, out_raw = run_e2(base)
standing_raw = out_raw.count("*** %s ***" % E2_SAYS)
R.note("    the untouched tree, nothing planted:   exit %s, %d occurrence(s) "
       "STANDING" % (rc_raw, standing_raw))
R.disclosed(
    "D2", "the tree is ALREADY RED and both parent instruments' clean-tree "
          "rows are false of it",
    "exit %s with %d standing occurrence(s)" % (rc_raw, standing_raw),
    "Named: %s -- struck in one paragraph and asserted live in another, by\n"
    "nobody's probe.  mg-4adb's V1b row `3 of 3 runners are GREEN on a clean\n"
    "tree` and mg-d53d's G1b row `3 of 3 runners GREEN on a clean tree and e2\n"
    "silent` were both true when they ran and are false of this tree.  It is\n"
    "a live cross-section finding doing what e2 exists to do and this ticket\n"
    "does NOT repair it." % LIVE)

live_rel, n_tildes = neutralise(base)
rc_clean, out_clean = run_e2(base)
standing_clean = out_clean.count("*** %s ***" % E2_SAYS)
R.note("")
R.note("    NEUTRALISED IN THE SANDBOX: %d strike marker(s) removed from %s"
       % (n_tildes, live_rel))
R.note("    the neutralised tree, nothing planted: exit %s, %d occurrence(s) "
       "STANDING" % (rc_clean, standing_clean))
R.row("the sandbox is GREEN before any deletion is made",
      rc_clean == 0 and standing_clean == 0,
      "Without this, a deletion that blinds the checker to the PLANT still\n"
      "measures GATE HELD because an unrelated occurrence is still firing.\n"
      "That is not a hypothetical: on the untouched tree, deleting\n"
      "`spans.append((prev, len(text)))` from kernd633 leaves the run red for\n"
      "exactly that reason, and mg-d53d recorded it as GATE LOST because at\n"
      "ITS tree there was no second finding to mask it.")

plant(base)
rc_red, out_red = run_e2(base)
standing_red = out_red.count("*** %s ***" % E2_SAYS)
R.note("")
R.note("    the neutralised tree, plant live:      exit %s, %d occurrence(s) "
       "STANDING" % (rc_red, standing_red))
R.row("the plant arms EXACTLY ONE finding and the checker exits non-zero",
      rc_red == 1 and standing_red == 1,
      "`kernd633.NEGATES` exonerates on refut/struck/misquot/corrected and\n"
      "twelve more.  A plant whose restating paragraph trips one of them is\n"
      "silently exonerated, and every sweep below would then be measuring a\n"
      "tree with no finding in it at all.")

runners_red = []
for rn in RUNNERS:
    rc, out = run_runner(base, rn)
    runners_red.append((rn, rc, E2_SAYS in out))
    R.note("    %-26s exit %-4s prints %s: %s"
           % (rn, rc, E2_SAYS, "yes" if E2_SAYS in out else "no"))
R.row("3 of 3 runners are RED, and red BECAUSE of the plant",
      all(rc == 1 and says for _r, rc, says in runners_red))


# ---------------------------------------------------------------------------
hdr("P2b  EVERY LINE OF BOTH FILES, AT THEIR PRE-REPAIR CONTENT")
# ---------------------------------------------------------------------------

R.note("The population is EVERY LINE of both files.  No exclusion list, so no")
R.note("exclusion to justify: comments, blanks, docstring lines and imports")
R.note("are all in it.  The four dispositions are defined once in kern1d26:")
R.note("")
R.note("  GATE LOST               exit 0.  The reader is told success.")
R.note("  GATE HELD, ATTRIBUTED   non-zero, and the output NAMES what fired.")
R.note("  GATE HELD, UNATTRIBUTED non-zero, and nothing says why.")
R.note("  TIMED OUT               its own row, never a pass.")
R.note("")
R.note("mg-d53d's vocabulary had one red disposition for the gate and one for")
R.note("`died before the gate`.  This repair adds five controls whose whole")
R.note("purpose is to fire INSTEAD of the finding, so the question asked here")
R.note("is not `did e2 speak` but `does the output name what produced the red`.")
print()

pool = Pool(WORKERS)
for root in pool.roots:
    neutralise(root)
    plant(root)
    pre_pair(root)

PRE_LINES = {rel: source_lines(pool.roots[0], rel) for rel in (E2, KERN)}
pre_tasks = [(rel, i) for rel in (E2, KERN)
             for i in range(len(PRE_LINES[rel]))]


def sweep(root, task):
    rel, i = task
    with Deletion(root, rel, i) as d:
        rc, out = run_e2(root)
    disp, what = disposition(rc, out)
    return (rel, i, d.text, rc, disp, what, E2_SAYS in out)


sys.stderr.write("  P2b: %d checker executions on %d sandboxes\n"
                 % (len(pre_tasks), WORKERS))
pre_res = pool.map(pre_tasks, sweep, progress=50)

for rel in (E2, KERN):
    print("  %s (PRE-REPAIR, %d lines)" % (rel, len(PRE_LINES[rel])))
    for r in sorted([x for x in pre_res if x[0] == rel], key=lambda x: x[1]):
        _rel, i, text, rc, disp, what, says = r
        print("      line %3d  exit %-4s %-24s finding printed: %-4s %s"
              % (i + 1, rc, disp, "yes" if says else "no", text[:34]))
    print()

PRE_LOST = [r for r in pre_res if r[4] == "GATE LOST"]
PRE_SILENT = [r for r in PRE_LOST if not r[6]]
counts = {}
for r in pre_res:
    counts[r[4]] = counts.get(r[4], 0) + 1
R.note("dispositions over the %d pre-repair lines: %s"
       % (len(pre_res), ", ".join("%s %d" % kv for kv in sorted(counts.items()))))
R.note("")
for _rel, i, text, rc, _d, _w, says in sorted(PRE_LOST, key=lambda r: (r[0], r[1])):
    R.note("  GATE LOST  %-46s line %3d  finding printed: %-4s  %s"
           % (_rel, i + 1, "yes" if says else "NO -- SILENT", text.strip()[:44]))

pre_named = sorted((r[0], r[2].strip()) for r in PRE_LOST)
six_named = sorted((rel, text) for rel, text, _n in SIX_PRE)
R.predicted(
    "P2a", "exactly 6, and they are the six mg-d53d names",
    "%d: %s" % (len(PRE_LOST),
                "; ".join("%s:%d %s" % (os.path.basename(r[0]), r[1] + 1,
                                        r[2].strip()[:26])
                          for r in sorted(PRE_LOST, key=lambda x: x[1]))),
    len(PRE_LOST) == 6 and pre_named == six_named,
    "Re-derived by an instrument that does not read mg-d53d's transcripts for\n"
    "it.  The tree has moved by many commits since mg-d53d ran, so this is a\n"
    "re-measurement and not a replay.")
R.predicted(
    "P2b", "4 of the 6 are silent -- FILES += _f, spans.append, the os.walk "
           "header and the else:",
    "%d of %d silent: %s"
    % (len(PRE_SILENT), len(PRE_LOST),
       "; ".join(r[2].strip()[:26] for r in PRE_SILENT)),
    len(PRE_SILENT) == 4
    and sorted(r[2].strip() for r in PRE_SILENT)
    == sorted(["FILES += _f", "spans.append((prev, len(text)))",
               "for dp, dns, fns in os.walk(root, onerror=onerror):",
               "else:"]))


# ---------------------------------------------------------------------------
hdr("P2c  EVERY LINE OF BOTH FILES, AS REPAIRED")
# ---------------------------------------------------------------------------

R.note("The same operator, the same tree, the same plant, over the repaired")
R.note("content of both files -- INCLUDING every line the repair itself adds.")
R.note("A repair certified over the population it inherited would be this")
R.note("ticket's own defect, committed by its author.")
print()

for root in pool.roots:
    post_pair(root)
POST_LINES = {rel: source_lines(pool.roots[0], rel) for rel in (E2, KERN)}
post_tasks = [(rel, i) for rel in (E2, KERN)
              for i in range(len(POST_LINES[rel]))]

sys.stderr.write("  P2c: %d checker executions on %d sandboxes\n"
                 % (len(post_tasks), WORKERS))
post_res = pool.map(post_tasks, sweep, progress=50)

for rel in (E2, KERN):
    print("  %s (REPAIRED, %d lines)" % (rel, len(POST_LINES[rel])))
    for r in sorted([x for x in post_res if x[0] == rel], key=lambda x: x[1]):
        _rel, i, text, rc, disp, what, says = r
        print("      line %3d  exit %-4s %-24s finding printed: %-4s %s"
              % (i + 1, rc, disp, "yes" if says else "no", text[:34]))
    print()

POST_LOST = [r for r in post_res if r[4] == "GATE LOST"]
POST_MUTE = [r for r in post_res if r[4] == "GATE HELD, UNATTRIBUTED"]
counts = {}
for r in post_res:
    counts[r[4]] = counts.get(r[4], 0) + 1
R.note("dispositions over the %d repaired lines: %s"
       % (len(post_res), ", ".join("%s %d" % kv for kv in sorted(counts.items()))))
for _rel, i, text, rc, _d, _w, says in sorted(POST_LOST, key=lambda r: (r[0], r[1])):
    R.note("  GATE LOST  %-46s line %3d  %s" % (_rel, i + 1, text.strip()[:44]))

R.note("P3a WAS MISSED ON THE FIRST RUN OF THIS SECTION AND THE TRANSCRIPT OF")
R.note("THAT RUN IS COMMITTED AS `out_p2_FIRSTRUN_one_lost.txt`.  It reported")
R.note("one GATE LOST -- `kernd633.py:172`, the `sys.exit(1 if bad else 0)`")
R.note("INSIDE `deliver` itself: the dead man's switch recorded the FACT of a")
R.note("verdict, so deleting the exit recorded it, returned normally and")
R.note("exited 0.  This ticket's own defect, one function inside its own")
R.note("repair, found by RUNNING the repair and not by reading it.  PREDICTION")
R.note("P4c said the first run would go red for exactly that reason and it is")
R.note("scored as a HIT in OUTCOMES.md; P3a is scored as MISSED ON THE FIRST")
R.note("RUN and whatever this run says.  The switch now records the CODE and")
R.note("returns it, so the verdict is carried by two lines.")
print()
R.predicted(
    "P3a", "0 deletions leave the checker exiting 0 with the plant live, over "
           "the WHOLE repaired population",
    "%d over %d lines" % (len(POST_LOST), len(post_res)),
    len(POST_LOST) == 0)
R.row("no deletion of the repaired files leaves the gate green",
      len(POST_LOST) == 0,
      "\n".join("%s line %d: %s" % (r[0], r[1] + 1, r[2].strip())
                for r in POST_LOST))
R.note("")
R.note("  of the %d red rows, %d are UNATTRIBUTED -- red, and the output does"
       % (len(post_res) - len(POST_LOST), len(POST_MUTE)))
R.note("  not name what fired.  These are tracebacks and are NOT findings:")
R.note("  mg-1d26's instruction is that a deletion must not change the VERDICT")
R.note("  silently, and a traceback on stderr changes nothing silently.  They")
R.note("  are counted and printed so the figure is not left to be inferred.")

R.predicted(
    "P3e", "the repaired verdict path is more than 806 and fewer than 950 "
           "lines",
    "%d lines over the two repaired files alone (%d + %d), and %d over all "
    "five files of the path"
    % (len(post_res), len(POST_LINES[E2]), len(POST_LINES[KERN]),
       len(post_res) + sum(len(source_lines(pool.roots[0],
                                            os.path.join("code", r,
                                                         "run_all.sh")))
                           for r in RUNNERS)),
    806 < len(post_res) + sum(
        len(source_lines(pool.roots[0], os.path.join("code", r, "run_all.sh")))
        for r in RUNNERS) < 950,
    "Scored against the whole verdict path, which is what P1a derives and\n"
    "what `806` was the size of.  A miss here is a miss about the SIZE OF\n"
    "THE PATCH and about nothing else, and it is kept as written.")


# ---------------------------------------------------------------------------
hdr("P2d  mg-d53d's SIX, AT THE REPAIRED TREE, THROUGH ALL THREE RUNNERS")
# ---------------------------------------------------------------------------

R.note("e2's own exit code is not the finding.  The finding is what a READER")
R.note("of the runner sees, so each of the six is deleted again and all three")
R.note("runners are executed over it.  Eighteen rows, one per (line, runner),")
R.note("printed individually: a claim that the hole is closed with no")
R.note("per-case demonstration is what this arc's audits keep refuting.")
print()


def through_runners(root, task):
    idx, rn = task
    rel, text, nxt = SIX_POST[idx]
    i = locate(root, rel, text, nxt)
    with Deletion(root, rel, i):
        rc, out = run_runner(root, rn)
    disp, what = disposition(rc, out)
    return (idx, rn, i + 1, rc, disp, what)


six_tasks = [(idx, rn) for idx in range(len(SIX_POST)) for rn in RUNNERS]
sys.stderr.write("  P2d: %d runner executions\n" % len(six_tasks))
six_res = pool.map(six_tasks, through_runners, progress=3)

for idx in range(len(SIX_POST)):
    R.note("  %s" % SIX_LABEL[idx])
    R.note("      %s, deleted alone" % SIX_POST[idx][1][:60])
    for _i, rn, line, rc, disp, what in [r for r in six_res if r[0] == idx]:
        R.note("      %-26s line %3d  exit %-4s %-24s %s"
               % (rn, line, rc, disp, what or ""))
print()

green = [r for r in six_res if r[3] == 0]
R.row("18 of 18 runner executions over the six go RED", not green,
      "\n".join("%s %s exit %s" % (SIX_LABEL[r[0]], r[1], r[3])
                for r in green))
R.predicted(
    "P3b", "18 of 18 exit non-zero",
    "%d of %d exit non-zero" % (len(six_res) - len(green), len(six_res)),
    not green and len(six_res) == 18)


# ---------------------------------------------------------------------------
hdr("P2e  LOUDNESS -- WHAT EACH OF THE SIX PRINTS WHILE GOING RED")
# ---------------------------------------------------------------------------

R.note("mg-1d26's third instruction: make them loud BEFORE making them")
R.note("impossible.  A deletion that changes the verdict must not be able to")
R.note("do so without printing.  Four of the six were silent before this")
R.note("ticket; this row asks what each of the six says now.")
print()

loud = []
for idx, (rel, text, nxt) in enumerate(SIX_POST):
    i = locate(base, rel, text, nxt)
    with Deletion(base, rel, i):
        rc, out = run_e2(base)
    what = attribution(out)
    loud.append((idx, rc, what))
    R.note("    %-44s exit %-4s attributed to: %s"
           % (SIX_LABEL[idx][:44], rc, what or "*** NOTHING NAMES IT ***"))
print()
R.row("6 of 6 name, in their own output, the control that produced the red",
      all(w for _i, _rc, w in loud))
R.note("  and the exit codes are %s -- three distinct kinds of red over six"
       % ", ".join(str(rc) for _i, rc, _w in loud))
R.note("  lines, which is the point of giving the vacuous case its own code.")


# ---------------------------------------------------------------------------
hdr("P2f  THE ARITHMETIC")
# ---------------------------------------------------------------------------

runner_lines = sum(len(source_lines(pool.roots[0],
                                    os.path.join("code", r, "run_all.sh")))
                   for r in RUNNERS)
R.note("  verdict path, derived in P1a, at this tree      %4d line(s)"
       % (runner_lines + len(post_res)))
R.note("  covered by mg-4adb's certified population       %4d line(s)" % 255)
R.note("  swept here, outside that certificate            %4d line(s)"
       % len(post_res))
R.note("  ")
R.note("  deletions outside the certificate that lost the gate")
R.note("      before this repair                          %4d" % len(PRE_LOST))
R.note("      of those, SILENT                            %4d"
       % len(PRE_SILENT))
R.note("      after this repair                           %4d"
       % len(POST_LOST))
R.note("      of those, SILENT                            %4d"
       % len([r for r in POST_LOST if not r[6]]))
R.note("  ")
R.note("  runner executions over the six, at the repaired tree: %d, of which"
       % len(six_res))
R.note("  %d exited 0." % len(green))

R.tail("P2")
print()
print("EXTENT OF THESE NUMBERS.  %d checker executions in P2b, %d in P2c, %d"
      % (len(pre_res), len(post_res), len(loud)))
print("in P2e, %d runner executions in P2d and %d in P2a -- every one of them"
      % (len(six_res), len(RUNNERS)))
print("this instrument's own, in `git clone --shared` sandboxes, none of them")
print("read from any transcript.  THE POPULATION IS EVERY LINE OF")
print("`e2_crosssection.py` AND `kernd633.py`, and a deletion is one line of")
print("one of the two.  IT SAYS NOTHING about: two lines deleted together; a")
print("line EDITED rather than removed; the 255 runner lines, which mg-4adb's")
print("certificate covers and this instrument does not re-sweep; any failure")
print("mode of the checker other than the planted occurrence; or")
print("`code/species_7d75/run_all.sh`, which mg-d53d's G5 leaves open and this")
print("ticket does not name.  THE SANDBOX IS NEUTRALISED in one named file")
print("(P2a) and every figure here is a figure about that tree.")

unplant(base)
cleanup()
sys.exit(1 if R.bad else 0)
