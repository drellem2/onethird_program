"""mg-e7bc G4 -- SEAM-CHECK THE ARTIFACT, REPORT THE THRESHOLD, AND RE-RUN.

Three things this audit is asked for that the first three sections do not cover.

THE THRESHOLD.  `controls_output.txt` ends with a control on ITSELF: nothing
above the bottom line may carry the all-pass banner.  Its extent is printed live
-- "lines scanned: N (the whole artifact above this row; M row names among
them)" -- and N is the threshold: everything at or below it is `summarise`'s
bottom line, the one place the banner is licensed.  Both numbers moved when this
repair added two rows (62 -> 64, 40 -> 42), which is exactly the situation that
produces a stale figure.  So N and M are re-derived here from the file and the
row is made to FIRE, because a threshold nobody has watched a control cross is a
number, not a control.

THE SEAM.  A figure stated at more than one site is a figure that can go stale
at one of them.  Six are checked across five sites, each against a value
measured from the live tree rather than quoted from any transcript.

THE RE-RUN.  mg-a318 found an instrument in this repository whose committed
transcript did not survive being re-run.  The two scripts this repair wrote or
rewrote are run again and compared byte for byte with what was committed.

PREDICTIONS REGISTERED BEFORE THE RUNS and printed with the results.
"""

import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kerne7bc import (ART, BAR, FC, FINDINGS, INSTR, ROOT, SCORE,      # noqa: E402
                      claim, finding, head, read, run_battery, scored_rows)

BANNER = "ALL CONTROLS PASS"

# Plant the banner literal in a row NAME.  The artifact's own control has to
# find it; if it does not, the threshold is decoration.
PLANT_BANNER = [(
    '''    check("instrument check: a genuine diagonal +-1 conjugation of L^rel is "''',
    '''    check("ALL CONTROLS PASS instrument check: a genuine diagonal +-1 conjugation of L^rel is "''')]

PREDICTIONS = [
    ("T1", "the banner control's threshold is re-derivable from the file",
     "lines scanned == the number of lines strictly above the row"),
    ("T2", "plant the banner in a row name -> the artifact's own control FIRES",
     "artifact CHANGES, exit 1, and the banner row is among the failures"),
    ("T3", "six figures, five sites, all agreeing with the live tree",
     "0 disagreements"),
    ("T4", "d2_deletion.py and d4_auditor_rerun.py re-run byte-identically",
     "both identical to their committed transcripts"),
]


def main():
    print(BAR)
    print("mg-e7bc G4 -- the threshold, the seam, and the re-run")
    print(BAR)
    print("\nPREDICTIONS, registered before the runs:")
    for tag, what, pred in PREDICTIONS:
        print("   %-3s %-62s %s" % (tag, what[:62], pred))

    art = read(ART)
    lines = art.split("\n")
    rows = scored_rows(art)

    # ------------------------------------------------------------------- T1
    head("T1. THE THRESHOLD, RE-DERIVED FROM THE FILE")
    hit = [i for i, ln in enumerate(lines) if "lines scanned:" in ln]
    idx = hit[0]
    m = re.search(r"lines scanned: (\d+) \(the whole artifact above this row; "
                  r"(\d+) row names among them\)", lines[idx])
    stated_n, stated_m = int(m.group(1)), int(m.group(2))
    actual_n = idx                       # lines strictly above, 0-based index
    actual_m = len(rows) - 1             # every scored row but this one
    print("  the row is line %d of the artifact (1-based)" % (idx + 1))
    print("  IT STATES      : lines scanned %d, row names %d"
          % (stated_n, stated_m))
    print("  RE-DERIVED HERE: lines above  %d, other rows %d"
          % (actual_n, actual_m))
    print("  THE THRESHOLD  : %d.  Everything at or below line %d is "
          "`summarise`'s bottom\n                   line, which is the one "
          "place the banner is licensed." % (stated_n, idx + 1))
    claim(stated_n == actual_n and stated_m == actual_m,
          "THE THRESHOLD IS %d AND IT IS MEASURED, NOT FROZEN: the row's two "
          "printed extents equal the extents re-derived from the committed "
          "file" % stated_n,
          "a row being added or removed without the row re-measuring -- which "
          "is what mg-04a8 did (62 -> 64, 40 -> 42) and what mg-a4ef/mg-7dd3 "
          "found printed as a stale literal elsewhere in this repository",
          "%d scored rows in the file, of which this is one" % len(rows))
    above = sum(1 for ln in lines[:idx] if BANNER in ln)
    below = sum(1 for ln in lines[idx + 1:] if BANNER in ln)
    claim(above == 0,
          "and the property it enforces holds: the banner literal occurs %d "
          "time(s) above the threshold" % above,
          "a row name or a detail string acquiring the literal, which is "
          "mg-6653's ATTACK B and what T2 constructs",
          "and %d time(s) below it -- the licensed occurrence is ABSENT from "
          "this artifact, because the battery has 2 [CANNOT FAIL] rows and "
          "`summarise` therefore prints the denial instead of the banner.  So "
          "on THIS artifact the row is comparing 0 above against 0 anywhere; "
          "what keeps it from being vacuous is not the file but T2, where the "
          "literal is planted and the row fires" % below)

    # ------------------------------------------------------------------- T2
    head("T2. AND THE CONTROL THAT CARRIES IT FIRES")
    print("The banner is planted in ONE row name -- `check(\"ALL CONTROLS PASS")
    print("instrument check: a genuine diagonal ...\")` -- and the battery re-run.\n")
    base, base_code = run_battery({}, "g4base")
    out, code = run_battery({"controls.py": PLANT_BANNER}, "g4plant")
    changed = out != base
    mut_rows = scored_rows(out.decode())
    failing = [n for lab, n in mut_rows if lab == "[FAIL]"]
    banner_row = [n for n in failing if "all-pass banner literal" in n]
    print("  artifact %s (%d -> %d bytes), exit %d, %d row(s) fail"
          % ("CHANGED" if changed else "BYTE-IDENTICAL", len(base), len(out),
             code, len(failing)))
    for f in failing:
        print("    FAILING: %s" % f[:150])
    claim(changed and code == 1 and len(banner_row) == 1,
          "the artifact's own control FIRES on a planted banner: exit %d, and "
          "the failing row is the one that owns the threshold" % code,
          "the control narrowing back to `ROW_NAMES` from the byte stream -- "
          "the mg-7d5a widening.  A row NAME carrying the literal is caught "
          "either way; mg-6653's ATTACK B put it in a `detail=` string, which "
          "the narrow version missed",
          "%d row(s) failed in total" % len(failing))

    # ------------------------------------------------------------------- T3
    head("T3. THE SEAM -- six figures, five sites, against the live tree")
    d2t = read(os.path.join(INSTR, "out_d2_deletion.txt"))
    d4t = read(os.path.join(INSTR, "out_d4_auditor_rerun.txt"))
    doc_d0e2 = read(os.path.join(ROOT, "docs",
                                 "landing-mg-d0e2-vacuous-check.md"))
    doc_1c80 = read(os.path.join(ROOT, "docs",
                                 "landing-mg-1c80-instrumented-predicate.md"))
    sites = [("controls_output.txt", art), ("out_d2_deletion.txt", d2t),
             ("out_d4_auditor_rerun.txt", d4t),
             ("landing-mg-d0e2-vacuous-check.md", doc_d0e2),
             ("landing-mg-1c80-instrumented-predicate.md", doc_1c80)]

    # WHY A BARE GREP IS NOT A SEAM CHECK, and this file's first attempt was
    # one.  "23680" and "20738" and "24879" all appear as byte counts in these
    # files; only the first is the current artifact.  The others are MUTANT
    # artifacts printed by the deletion test, and the PRE-REPAIR artifact
    # correctly quoted as history.  A regex for `\d+ bytes` reports 12
    # disagreements and every one of them is the instrument's fault, not the
    # subject's.  So each figure is anchored to the SENTENCE that asserts it as
    # current, the anchors are listed here to be argued with, and the
    # occurrences that are deliberately NOT checked are counted and named.
    n_claims = {}
    for t in ("d1_trace", "d2_deletion", "d3_reintroduction",
              "d4_auditor_rerun"):
        txt = read(os.path.join(INSTR, "out_%s.txt" % t))
        mm = re.search(r"^(\d+) claim\(s\) scored", txt, re.M)
        n_claims[t] = int(mm.group(1)) if mm else -1

    # (figure, live value, [(site name, anchored regex capturing it)])
    FIGURES = [
        ("scored rows", len(rows), [
            ("out_d2_deletion.txt", r"BASELINE: (\d+) scored row\(s\)"),
            ("landing-mg-d0e2-vacuous-check.md",
             r"Battery: \*\*(\d+) scored rows\*\*"),
            ("landing-mg-d0e2-vacuous-check.md",
             r"repair takes the artifact to a genuine (\d+)"),
            ("landing-mg-1c80-instrumented-predicate.md",
             r"As of mg-04a8: (\d+) rows"),
        ]),
        ("artifact bytes", len(art), [
            ("out_d2_deletion.txt",
             r"regenerates byte-identically\n\s+(\d+) bytes regenerated"),
            ("out_d2_deletion.txt",
             r"regenerates byte-identically\n\s+\d+ bytes regenerated, (\d+) committed"),
            ("landing-mg-d0e2-vacuous-check.md", r"exit 0, ([\d,]+) bytes"),
        ]),
        ("lines scanned (the threshold)", stated_n, [
            ("controls_output.txt", r"lines scanned: (\d+) \(the whole"),
            ("out_d4_auditor_rerun.txt", r"'lines scanned: (\d+)' with \d+"),
            ("out_d4_auditor_rerun.txt", r"'lines scanned: \d+' with (\d+) lines"),
            ("landing-mg-d0e2-vacuous-check.md",
             r"the artifact now says \*\*(\d+)\*\*"),
        ]),
        ("row names among them", stated_m, [
            ("controls_output.txt", r"; (\d+) row names among them"),
            ("out_d4_auditor_rerun.txt", r"'(\d+) row names' with \d+ scored"),
            ("landing-mg-d0e2-vacuous-check.md",
             r"the artifact now says \*\*\d+\*\* and \*\*(\d+)\*\*"),
        ]),
        ("instrument claims", sum(n_claims.values()), [
            ("landing-mg-d0e2-vacuous-check.md",
             r"\*\*(\d+) claims, 0 BROKEN\*\*"),
        ]),
        ("deletion test bites, of 9", 9, [
            ("out_d4_auditor_rerun.txt",
             r"THE DELETION TEST NOW BITES ON (\d+) OF 9"),
            ("landing-mg-d0e2-vacuous-check.md",
             r"\*\*(\d+) of 9 mutations change the artifact"),
        ]),
    ]
    by_name = dict(sites)
    print("   %-30s %8s %9s   %s"
          % ("figure", "live", "sentences", "sites"))
    disagreements, n_sent, unanchored = [], 0, 0
    for name, live, anchors in FIGURES:
        vals = []
        for sname, pat in anchors:
            mm = re.search(pat, by_name[sname])
            if mm is None:
                unanchored += 1
                print("       ANCHOR NOT FOUND: %s in %s" % (pat, sname))
                continue
            v = int(mm.group(1).replace(",", ""))
            vals.append((sname, v))
            n_sent += 1
            if v != live:
                disagreements.append((name, sname, v, live))
        print("   %-30s %8d %9d   %s"
              % (name, live, len(vals),
                 ", ".join(sorted(set(s for s, _ in vals)))))
        for s, v in vals:
            if v != live:
                print("       DISAGREES: %s says %d" % (s, v))
    claim(not disagreements and unanchored == 0,
          "each of %d anchored sentences across %d sites states the figure the "
          "live tree carries -- %d figures, 0 disagreements"
          % (n_sent, len(set(s for _n, _l, a in FIGURES for s, _p in a)),
             len(FIGURES)),
          "a figure being restated at a site that is not regenerated when the "
          "tree moves -- the mg-8e30 defect.  The artifact grew two rows in "
          "this very commit, so every figure here is one that MOVED.  And "
          "under an anchor going missing, which is scored above rather than "
          "passing as 'nothing found, nothing wrong'",
          "; ".join("%s at %s: %d vs %d" % d for d in disagreements)
          or "no disagreement; %d anchor(s) unmatched" % unanchored)
    finding(bool(disagreements),
            "a figure disagrees between sites: %s"
            % "; ".join("%s at %s says %d, live %d" % d
                        for d in disagreements))

    head("AND WHAT THIS SEAM CHECK DELIBERATELY DOES NOT COUNT")
    print("  T3's prediction was 0 disagreements.  THIS FILE'S FIRST VERSION "
          "REPORTED 20,")
    print("  and all 20 were its own fault: it grepped `\\d+ bytes` and counted "
          "mutant")
    print("  artifacts and correctly-quoted history as stale figures.  The "
          "instrument was")
    print("  corrected, not the prediction -- and the correction is recorded "
          "here rather")
    print("  than left to look like a clean first run.\n")
    stale = [(s, v) for s, t in sites
             for v in re.findall(r"\b(2[0-9],?[0-9]{3})\s+bytes", t)
             if int(v.replace(",", "")) != len(art)]
    hist = [(s, v) for s, v in stale if v.replace(",", "") == "20738"]
    print("  %d byte-figures at these sites are NOT the live artifact's %d."
          % (len(stale), len(art)))
    print("  %d of them are the PRE-REPAIR artifact (20,738), quoted as "
          "history;" % len(hist))
    print("  the rest are MUTANT artifacts the deletion test printed -- a "
          "figure a run")
    print("  produced, not a figure a site asserts.  Counting them as seam "
          "disagreements")
    print("  is what this file's first version did, and it is the same error "
          "as scoring")
    print("  a check by whether it CAN fire rather than by what it fires on.")
    print("  Also not counted: `lines scanned: 62` and `40 row names` at two "
          "sites --")
    print("  both are mg-d0e2's frozen literals, QUOTED AS STALE by the "
          "sentence that")
    print("  carries them, and the same sentence states the live 64 and 42 "
          "beside them.")

    # ------------------------------------------------------------------- T4
    head("T4. THE RE-RUN -- do the repair's own transcripts survive it?")
    print("mg-a318 found an instrument here whose committed transcript did not.")
    print("The two scripts mg-04a8 wrote or rewrote are re-run and compared.\n")
    same = []
    for script, out_name in (("d2_deletion.py", "out_d2_deletion.txt"),
                             ("d4_auditor_rerun.py", "out_d4_auditor_rerun.txt")):
        proc = subprocess.run([sys.executable, script], cwd=INSTR,
                              capture_output=True, text=True)
        got = proc.stdout + proc.stderr
        committed = read(os.path.join(INSTR, out_name))
        ident = got == committed
        same.append(ident)
        print("   %-24s exit %d, %d bytes re-run vs %d committed -- %s"
              % (script, proc.returncode, len(got), len(committed),
                 "BYTE-IDENTICAL" if ident else "DIFFERS"))
        if not ident:
            a, b = got.split("\n"), committed.split("\n")
            moved = [i for i in range(min(len(a), len(b))) if a[i] != b[i]]
            print("       %d line(s) differ; first at line %d"
                  % (len(moved) + abs(len(a) - len(b)),
                     (moved[0] + 1) if moved else min(len(a), len(b)) + 1))
    claim(all(same),
          "both of the repair's own scripts re-run BYTE-IDENTICALLY to their "
          "committed transcripts -- the transcript is a record of a run that "
          "can be had again, not of one run once",
          "a timestamp, a temporary path, a dict ordering or a `main`-relative "
          "reference entering the output.  mg-04a8 pinned d2's BEFORE half to "
          "a commit for exactly this reason: while it read `main` the claim "
          "moved whenever the branch did",
          "run from %s" % INSTR)
    finding(not all(same),
            "a committed transcript of this repair does not survive a re-run")

    print("\n" + BAR)
    print("%d claim(s) scored; %d BROKEN.  %d FINDING(s)."
          % (len(SCORE), SCORE.count(False), len(FINDINGS)))
    for f in FINDINGS:
        print("  FINDING: %s" % f)
    print(BAR)
    return 1 if not all(SCORE) else 0


if __name__ == "__main__":
    sys.exit(main())
