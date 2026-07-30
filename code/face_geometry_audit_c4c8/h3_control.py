"""mg-c4c8 H3 -- THE NEGATIVE CONTROL, RE-RUN, AND THREE CORRUPTIONS NO LIST
NAMES.

THE BRIEF'S SECOND ITEM, verbatim: the broken artifact is committed and the
repaired check exits 1 on it; re-run it and report the exit code; do not accept
that it still holds because nothing touched it.  A repair that restructures the
gates can silently stop the control from firing while leaving it in the tree --
and mg-9220 restructured a gate AND regenerated the broken artifact, which is
exactly the pair of edits that could do it.

So: the exit status of `checkrun.py` as a PROCESS, on the committed all-`[FAIL]`
artifact, is reported first and everything else follows it.

THEN THREE CORRUPTIONS OF THIS AUDIT'S OWN, chosen because no list names them and
because they vary the KIND rather than the direction or the scale.  mg-e7bc's
five vary direction (all-`[PASS]`), scale (one row), channel (a lying summary)
and kind (a row deleted).  Deletion has a dual and two neighbours that nobody has
run:

  D1  a scored row LINE DUPLICATED -- the dual of mg-e7bc's B-drop;
  D2  a scored row RENAMED, its marker untouched -- the row is still there and
      is no longer the row the battery scored;
  D3  two scored rows EXCHANGED IN POSITION, markers and names untouched.

and one that must go RED, so that "my corruptions are invisible" cannot be a
statement about my corruptions:

  D4  one `[CANNOT FAIL]` row PROMOTED to `[FAIL]`.

PREDICTIONS ARE REGISTERED BEFORE THE RUNS.  Nothing here writes to
../face_geometry or to the subject's directory; the corrupted artifacts are
written into this directory and removed.
"""

import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kernc4c8 import (ART, BAR, E7BC, INSTR, ROOT, claim, finding,     # noqa: E402
                      footer, head, read, retag, scored_rows,
                      summary_fail_names)

HERE = os.path.dirname(os.path.abspath(__file__))
PC_THEIRS = os.path.join(INSTR, "positive_control_all_fail.txt")
PC_E7BC = os.path.join(E7BC, "pc_all_pass.txt")

# (tag, what, predicted exit of the repaired check)
PREDICTIONS = [
    ("A-clean", "the committed artifact, untouched", 0),
    ("A-broken", "positive_control_all_fail.txt -- the committed broken one", 1),
    ("D1", "MINE: one [PASS] row LINE duplicated", 0),
    ("D2", "MINE: one [PASS] row RENAMED, marker untouched", 0),
    ("D3", "MINE: two scored rows EXCHANGED in position", 0),
    ("D4", "MINE: one [CANNOT FAIL] row promoted to [FAIL]", 1),
]


def run_check(path):
    """The repaired check as a process.  Its exit status is the measurement."""
    proc = subprocess.run([sys.executable, "checkrun.py", path, "0"],
                          cwd=E7BC, capture_output=True, text=True)
    verdict = [l for l in proc.stdout.split("\n") if l.startswith("verdict")]
    return proc.returncode, (verdict[0].split(":", 1)[1].strip()
                             if verdict else proc.stderr.strip()[:110])


def row_lines(text):
    """Indices of the lines that ARE scored rows."""
    out = []
    for i, ln in enumerate(text.split("\n")):
        s = ln.strip()
        if any(s.startswith(m) for m in ("[PASS]", "[FAIL]", "[CANNOT FAIL]")):
            out.append(i)
    return out


def duplicate_row(text, which):
    lines = text.split("\n")
    idx = row_lines(text)[which]
    return "\n".join(lines[:idx + 1] + [lines[idx]] + lines[idx + 1:])


def rename_row(text, which):
    lines = text.split("\n")
    idx = row_lines(text)[which]
    ln = lines[idx]
    s = ln.lstrip()
    marker = "[PASS]"
    lines[idx] = (ln[:len(ln) - len(s)] + marker
                  + " a row this battery never scored")
    return "\n".join(lines)


def exchange_rows(text, a, b):
    lines = text.split("\n")
    ia, ib = row_lines(text)[a], row_lines(text)[b]
    lines[ia], lines[ib] = lines[ib], lines[ia]
    return "\n".join(lines)


def tmp(name, text):
    path = os.path.join(HERE, "_tmp_" + name + ".txt")
    with open(path, "w") as fh:
        fh.write(text)
    return path


def main():
    print(BAR)
    print("mg-c4c8 H3 -- the negative control re-run, and three corruptions "
          "no list names")
    print(BAR)

    clean = read(ART)
    rows = scored_rows(clean)
    npass = sum(1 for m, _ in rows if m == "[PASS]")
    ncf = sum(1 for m, _ in rows if m == "[CANNOT FAIL]")
    nfail = sum(1 for m, _ in rows if m == "[FAIL]")

    head("THE POPULATION -- named, because a bare total is not a measurement")
    print("  code/face_geometry/controls_output.txt, %d bytes" % len(clean))
    print("  %d scored rows: %d [PASS], %d [CANNOT FAIL], %d [FAIL]"
          % (len(rows), npass, ncf, nfail))
    print("  the bottom line names %d failure(s)"
          % len(summary_fail_names(clean)))
    claim(len(rows) == 43 and npass == 41 and ncf == 2 and nfail == 0,
          "the artifact this section measures against carries 43 scored rows "
          "(41 PASS, 2 CANNOT FAIL, 0 FAIL)",
          "a row being added to or removed from controls.py.  mg-9220 moved "
          "the artifact 23,680 -> 23,684 bytes without moving a row, and this "
          "is the check that distinguishes those two kinds of edit",
          "%d bytes; row parser re-derived in kernc4c8, not imported from the "
          "subject or from mg-e7bc" % len(clean))

    print("\nPREDICTIONS, registered before the runs "
          "(0 = the check says yes, 1 = RED):")
    for tag, what, pe in PREDICTIONS:
        print("   %-10s %-58s %d" % (tag, what, pe))

    head("1. THE PRIMARY MEASUREMENT -- the exit code, re-run and not assumed")
    broken = read(PC_THEIRS)
    cases = [
        ("A-clean", clean),
        ("A-broken", broken),
        ("D1", duplicate_row(clean, 0)),
        ("D2", rename_row(clean, 1)),
        ("D3", exchange_rows(clean, 2, 3)),
        ("D4", retag(clean, "[FAIL]",
                     lambda i: i == [j for j, (m, _n) in enumerate(rows)
                                     if m == "[CANNOT FAIL]"][0])),
    ]
    observed = {}
    print("   %-10s %-8s %-8s %-8s %s"
          % ("tag", "exit", "(pred)", "match", "verdict"))
    for tag, text in cases:
        path = tmp(tag, text)
        try:
            rc, verdict = run_check(path)
        finally:
            os.remove(path)
        pe = [p for p in PREDICTIONS if p[0] == tag][0][2]
        observed[tag] = (rc, verdict)
        print("   %-10s %-8d %-8d %-8s %s"
              % (tag, rc, pe, "match" if rc == pe else "*** MISS ***",
                 verdict[:70]))

    misses = [t for t, _w, pe in PREDICTIONS if observed[t][0] != pe]
    print("\n  %d of %d matched.%s"
          % (len(PREDICTIONS) - len(misses), len(PREDICTIONS),
             "" if not misses else "  MISSES: " + ", ".join(misses)))

    claim(observed["A-broken"][0] == 1,
          "THE NEGATIVE CONTROL STILL FIRES: `checkrun.py "
          "positive_control_all_fail.txt` EXITS %d, re-run against the tree "
          "mg-9220 left behind" % observed["A-broken"][0],
          "the repaired check reverting to a comparison against the "
          "baseline's own labels, or the committed control drifting off the "
          "artifact it is the flip of -- mg-9220 regenerated it, so this run "
          "is the first that could have caught a bad regeneration",
          "verdict: %s" % observed["A-broken"][1])
    claim(observed["A-clean"][0] == 0,
          "and it is not red on everything: on the unmutated artifact it "
          "exits 0",
          "the check acquiring an expectation the clean artifact violates, "
          "which makes a red-on-everything control look like a working one")

    head("2. AND THE CONTROL FILE IS STILL THE FLIP OF THE CURRENT ARTIFACT")
    mine = retag(clean, "[FAIL]")
    claim(broken == mine,
          "positive_control_all_fail.txt is byte-equal to this audit's own "
          "all-[FAIL] retagging of controls_output.txt (%d bytes)" % len(mine),
          "controls_output.txt moving without the control being regenerated.  "
          "mg-9220 moved it by four bytes and regenerated three derived "
          "files; this is the check that says the regeneration was right, "
          "done with a retagger written here rather than with the subject's "
          "`flip_all_rows`",
          "%d of %d rows read [FAIL] in the committed control"
          % (sum(1 for m, _ in scored_rows(broken) if m == "[FAIL]"),
             len(scored_rows(broken))))
    e7 = read(PC_E7BC)
    claim(e7 == retag(clean, "[PASS]"),
          "and mg-e7bc's own control, pc_all_pass.txt, is still the all-[PASS] "
          "retagging -- the file mg-9220 regenerated inside another audit's "
          "directory",
          "the same drift in the other direction.  mg-9220 edited a file under "
          "code/face_geometry_audit_e7bc/, which is a generated control and "
          "not a transcript; whether that edit was correct is a question with "
          "an answer, and this is it",
          "%d bytes" % len(e7))

    head("3. THREE CORRUPTIONS NO LIST NAMES, AND WHAT THEY SAY")
    invisible = [t for t in ("D1", "D2", "D3") if observed[t][0] == 0]
    finding(len(invisible) == 3,
            "THE GUARD IS OVER LABELS AND NOT OVER THE ROW SET, IN THREE MORE "
            "DIRECTIONS.  mg-e7bc found that DELETING a scored row line leaves "
            "the repaired check green.  Its dual and its two neighbours do the "
            "same: DUPLICATING a row (D1), RENAMING one while keeping its "
            "marker (D2) and EXCHANGING two rows' positions (D3) all exit 0.  "
            "The check derives an expectation for each row PRESENT from that "
            "row's own name, so a row that is duplicated, renamed or moved "
            "carries its expectation with it.  D4 -- a [CANNOT FAIL] row "
            "promoted to [FAIL] -- exits 1, so this is the extent of the "
            "guard and not a failure of these four to be corruptions.  "
            "mg-04a8's sentence 'an artifact whose rows have been edited -- by "
            "a corruption, a bad merge, or a hand -- disagrees with its own "
            "summary, and the check below is what notices' remains wider than "
            "what the code does, one audit later and in four ways"
            if len(invisible) == 3 else "")
    claim(observed["D4"][0] == 1,
          "and this audit's corruptions are not all invisible by construction: "
          "D4, a [CANNOT FAIL] row promoted to [FAIL], EXITS 1",
          "the baseline CANNOT FAIL set no longer being read from the clean "
          "artifact's summary block -- which is the derivation that makes a "
          "promotion detectable at all",
          "verdict: %s" % observed["D4"][1])

    head("4. THE SUBJECT'S OWN INSTRUMENTS, RE-RUN AS PROCESSES")
    print("Not a paraphrase of their transcripts: the exit statuses and the "
          "claim counts,\nnow.  BELIEVE THE ROWS OVER THE SUMMARY: mg-9220's "
          "landing reports '72 claims, 0\nBROKEN, exit 0 (d1 17, d2 33, d3 6, "
          "d4 16)'.  That is a summary of four processes,\nand the four "
          "processes are here.\n")
    # (label, cwd, script, the count the landing declares for it)
    DECLARED = [("mg-9220 d1_trace.py", INSTR, "d1_trace.py", 17),
                ("mg-9220 d2_deletion.py", INSTR, "d2_deletion.py", 33),
                ("mg-9220 d3_reintroduction.py", INSTR,
                 "d3_reintroduction.py", 6),
                ("mg-9220 d4_auditor_rerun.py", INSTR,
                 "d4_auditor_rerun.py", 16),
                ("mg-e7bc g1_positive_control.py", E7BC,
                 "g1_positive_control.py", None)]
    runs = []
    print("   %-32s %-6s %-9s %-9s %s"
          % ("script", "exit", "claims", "declared", "broken"))
    for label, cwd, script, want in DECLARED:
        p = subprocess.run([sys.executable, script], cwd=cwd,
                           capture_output=True, text=True)
        tail = [l for l in p.stdout.split("\n") if "claim(s) scored" in l]
        line = tail[-1].strip() if tail else ""
        n = int(line.split()[0]) if line else -1
        nbroken = int(line.split(";")[1].split()[0]) if ";" in line else -1
        runs.append((label, p.returncode, n, nbroken, want))
        print("   %-32s %-6d %-9d %-9s %d"
              % (label, p.returncode, n,
                 str(want) if want is not None else "-", nbroken))
    claim(all(rc == 0 for _l, rc, _n, _b, _w in runs)
          and all(b == 0 for _l, _rc, _n, b, _w in runs),
          "every one of the five exits 0 with 0 BROKEN claims on this tree: "
          "the repair's four scripts and the audit whose primary measurement "
          "is the control above",
          "any of them going red, which is the thing a re-run can find and a "
          "quotation cannot.  d2_deletion.py runs twelve control batteries and "
          "the eleven mutations checked in H4, so a green exit here is also a "
          "statement that those eleven anchors still apply",
          "; ".join("%s exit %d" % (l, rc) for l, rc, _n, _b, _w in runs))
    declared_rows = [(l, n, w) for l, _rc, n, _b, w in runs if w is not None]
    total = sum(n for _l, n, _w in declared_rows)
    claim(all(n == w for _l, n, w in declared_rows) and total == 72,
          "AND THE LANDING'S SUMMARY AGREES WITH THE ROWS THAT PRODUCE IT: "
          "d1 %d, d2 %d, d3 %d, d4 %d, total %d against a declared 72"
          % tuple([n for _l, n, _w in declared_rows] + [total]),
          "a claim being added to or removed from any of the four without the "
          "landing's parenthesis being regenerated.  A total that disagrees "
          "with its own parts is the defect mg-8aae found one project over, "
          "and the four parts are the thing to believe",
          "; ".join("%s: %d printed, %d declared" % (l, n, w)
                    for l, n, w in declared_rows))

    return footer()


if __name__ == "__main__":
    sys.exit(main())
