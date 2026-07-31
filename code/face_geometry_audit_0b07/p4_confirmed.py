"""mg-0b07 p4 -- WHAT mg-c4c8 BOOKED AS DONE: is any of it weaker now?

mg-c4c8's verdict had a green half, and a repair that restructures a condition is
exactly the edit that can quietly reduce what individual deletion can see while
closing the item it was written for.  Three things were confirmed there and are
re-measured here, by this audit's own enumeration and splicer:

  * `absorb_trace`'s SIX `return` statements, each deleted ALONE, all move the
    artifact -- 6 of 6;
  * the inert return is REMOVED from the source rather than annotated, and
    nothing was added to `controls.py` to watch it instead;
  * the negative control, run as a PROCESS, still exits 1.

Each is measured on the live tree AND at `b6bc2ef`, the tree mg-c4c8 measured,
so "unchanged" is a comparison and not a recollection.

mg-c4c8's F3 pair is measured too: its two inert returns are disclosed as NOT
closed by this commit, so they are predicted unchanged.  A disclosure is a claim
like any other.
"""

import ast
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kern0b07 import (                                          # noqa: E402
    BAR, REPO, claim, finding, head, replace_stmt_with_pass, report,
    returns_of, run_battery, scored_rows, source_at, splice, tree_with,
)

MG9220 = "b6bc2ef"
CHECKRUN = os.path.join(REPO, "code", "face_geometry_audit_e7bc", "checkrun.py")
BROKEN_ARTIFACT = os.path.join(REPO, "code", "face_geometry_instr_5f9a",
                               "positive_control_all_fail.txt")

# Registered before the runs: the six returns of `absorb_trace` in SOURCE order,
# with the exit code each deletion is predicted to produce.  mg-c4c8 measured
# these at b6bc2ef as 1, 0, 1, 1, 1, 1 with all six moving the artifact.
PRED = [("shape", True, 1), ("diagonal", True, 0), ("magnitude", True, 1),
        ("find -- the union-find root", True, 1),
        ("parity contradiction", True, 1), ("the accepting return", True, 1)]


def label(src, site):
    seg = ast.get_source_segment(src, site.node) or ""
    return seg.replace("\n", " ")[:52]


def sweep(src, tag):
    base, base_code = run_battery(tree_with("face_complex.py", src))
    sites = returns_of(src, "absorb_trace")
    rows = []
    print("   %s: %d `return` statement(s) in `absorb_trace`, baseline %d "
          "bytes exit %d" % (tag, len(sites), len(base), base_code))
    print("   %-4s %-54s %-16s %-5s %s"
          % ("#", "return", "artifact", "exit", "bytes"))
    for k, site in enumerate(sites):
        out, code = run_battery(tree_with(
            "face_complex.py", replace_stmt_with_pass(src, site)))
        rows.append((site.line, out != base, code, len(out)))
        print("   %-4d %-54s %-16s %-5d %d"
              % (k + 1, label(src, site),
                 "CHANGES" if out != base else "BYTE-IDENTICAL", code,
                 len(out)))
    return rows, base


def guard_returns(src):
    """The two returns mg-c4c8's F3 names: the shape guard of `gate_violations`
    and of `diagonal_moves`, located by function rather than by line."""
    out = []
    for fname in ("gate_violations", "diagonal_moves"):
        sites = returns_of(src, fname)
        out.append((fname, sites[0]))
    return out


def main():
    print(BAR)
    print("mg-0b07 p4 -- what was confirmed: unchanged, or quietly weaker?")
    print(BAR)
    print("\nPREDICTIONS, registered before these runs (PREDICTIONS.md p4):")
    print("   p4.1  6 returns, 6 of 6 CHANGE; exits 1, 0, 1, 1, 1, 1 in source "
          "order")
    print("   p4.2  1 `shape` return; controls.py's constructed pairs "
          "unchanged from b6bc2ef")
    print("   p4.3  the negative control run as a process: exit 1")
    print("   p4.4  mg-c4c8's F3 pair: 2 of 2 BYTE-IDENTICAL, exit 0 "
          "(disclosed as not closed)\n")

    live = source_at(None)
    head("1.  EVERY `return` OF `absorb_trace`, DELETED ALONE -- THIS TREE")
    print("Replaced by `pass` at its own indentation, not deleted as lines: "
          "most of these are\nthe only statement of their block and removing "
          "the lines would remove the enclosing\n`if`, which is a LARGER unit "
          "than the one declared.  That is the error this lineage\nis about and "
          "an auditor can commit it as easily as a repairer.\n")
    rows, base = sweep(live, "live tree")
    hits = sum(1 for (_l, ch, code, _b), (_n, wc, we) in zip(rows, PRED)
               if ch == wc and code == we)
    claim("`absorb_trace` is covered at the granularity of a `return`: %d of %d "
          "move the artifact under INDIVIDUAL deletion, and %d of %d exit codes "
          "match the registered prediction"
          % (sum(1 for _l, ch, _c, _b in rows if ch), len(rows), hits,
             len(PRED)),
          all(ch for _l, ch, _c, _b in rows) and hits == len(PRED),
          "a return whose individual deletion leaves the artifact "
          "byte-identical -- which is mg-e7bc's finding, and which this commit "
          "could have reintroduced by restructuring the gate.  The population "
          "is read from the tree, so a return ADDED by this commit would appear "
          "here without anyone listing it",
          "; ".join("line %d %s exit %d" % (l, "CHANGES" if ch else "IDENTICAL",
                                            c)
                    for l, ch, c, _b in rows))

    head("2.  THE SAME SWEEP AT b6bc2ef -- so 'unchanged' is a comparison")
    prows, _pbase = sweep(source_at(MG9220), MG9220)
    same_count = len(prows) == len(rows)
    same_shape = ([(ch, c) for _l, ch, c, _b in prows]
                  == [(ch, c) for _l, ch, c, _b in rows])
    claim("the tree mg-c4c8 measured and this one give the SAME sweep: %d "
          "returns there and %d here, and the (artifact, exit) pair agrees on "
          "%d of %d" % (len(prows), len(rows),
                        sum(1 for a, b in zip(prows, rows)
                            if (a[1], a[2]) == (b[1], b[2])), len(rows)),
          same_count and same_shape,
          "this commit having merged, split, hoisted or short-circuited a "
          "return.  It restructured the CONDITION of one of them, which is "
          "exactly the edit that can reduce what individual deletion sees "
          "without removing anything -- and this is the measurement that would "
          "notice",
          "there: %s || here: %s"
          % ("/".join("%s%d" % ("C" if ch else "I", c)
                      for _l, ch, c, _b in prows),
             "/".join("%s%d" % ("C" if ch else "I", c)
                      for _l, ch, c, _b in rows)))

    head("3.  THE INERT RETURN: REMOVED, AND NOT REPLACED BY A WATCHER")
    shape_rets = [s for s in returns_of(live, "absorb_trace")
                  if '"shape"' in (ast.get_source_segment(live, s.node) or "")]
    ctl_live = ast.literal_eval(
        [n.value for n in ast.walk(ast.parse(
            source_at(None, "controls.py")))
         if isinstance(n, ast.Assign)
         and any(isinstance(t, ast.Name) and t.id == "UNREACHED_GATE_PAIRS"
                 for t in n.targets)][0])
    ctl_pin = ast.literal_eval(
        [n.value for n in ast.walk(ast.parse(
            source_at(MG9220, "controls.py")))
         if isinstance(n, ast.Assign)
         and any(isinstance(t, ast.Name) and t.id == "UNREACHED_GATE_PAIRS"
                 for t in n.targets)][0])
    n_live = sum(len(v) for v in ctl_live.values())
    n_pin = sum(len(v) for v in ctl_pin.values())
    base_rows = scored_rows(base)
    claim("one `shape` return in `absorb_trace`, counted from the tree; and "
          "`controls.py` carries %d `UNREACHED_GATE_PAIRS` entr(ies) here against %d "
          "at %s -- nothing was added to watch the sub-unit this commit "
          "removed" % (n_live, n_pin, MG9220),
          len(shape_rets) == 1 and n_live == n_pin,
          "a pair added to `controls.py` for the clause, or a return re-added "
          "behind a flag or inside `if False:` -- both counted from the tree "
          "here, so neither could be hidden by being unreachable.  'Removal, "
          "not detection' is the ticket's own wording and this is it, measured",
          "shape returns: %d; UNREACHED_GATE_PAIRS entries %d vs %d; scored rows in the "
          "battery: %d" % (len(shape_rets), n_live, n_pin, len(base_rows)))

    head("4.  THE NEGATIVE CONTROL, RUN AS A PROCESS")
    r = subprocess.run([sys.executable, CHECKRUN, BROKEN_ARTIFACT],
                       capture_output=True, text=True)
    r0 = subprocess.run([sys.executable, CHECKRUN,
                         os.path.join(REPO, "code", "face_geometry",
                                      "controls_output.txt")],
                        capture_output=True, text=True)
    print("   %-52s exit %d" % ("positive_control_all_fail.txt", r.returncode))
    print("   %-52s exit %d" % ("controls_output.txt (the clean artifact)",
                                r0.returncode))
    claim("the repaired check still goes RED on the committed broken artifact "
          "(exit %d) and stays green on the clean one (exit %d)"
          % (r.returncode, r0.returncode),
          r.returncode == 1 and r0.returncode == 0,
          "the control being regenerated into something the check accepts, or "
          "the check being loosened.  This commit regenerated that control "
          "file, which is the pair of edits that can stop a control firing "
          "while leaving it in the tree -- so it is run as a PROCESS with its "
          "status read, not called as a function",
          "%s" % (r.stdout.strip().split("\n")[-1] if r.stdout else ""))

    head("5.  mg-c4c8's F3 PAIR -- disclosed as NOT closed, and predicted so")
    f3 = []
    for fname, site in guard_returns(live):
        out, code = run_battery(tree_with(
            "face_complex.py", splice(live, site.node, "pass")))
        f3.append((fname, out != base, code, len(out)))
        print("   %-24s %-16s exit %d  %d bytes"
              % (fname + " shape guard",
                 "CHANGES" if out != base else "BYTE-IDENTICAL", code,
                 len(out)))
    claim("both are still BYTE-IDENTICAL under individual deletion -- %d of 2, "
          "unchanged, which is what the commit's disclosure says"
          % sum(1 for _f, ch, c, _b in f3 if not ch and c == 0),
          all(not ch and c == 0 for _f, ch, c, _b in f3),
          "either of them becoming visible, which would mean this commit "
          "closed F3 without saying so, or becoming a crash, which would mean "
          "it moved them.  A disclosure that an item is NOT closed is a claim "
          "about the tree and is checked here like any other",
          "; ".join("%s %s exit %d" % (f, "CHANGES" if ch else "IDENTICAL", c)
                    for f, ch, c, _b in f3))
    if all(not ch for _f, ch, _c, _b in f3):
        finding("B5",
                "mg-c4c8's F3 IS OPEN AND UNCHANGED, and this commit's own "
                "sweep names but does not reach it: the two `return`s whose "
                "individual deletion moves not one byte are still there, and "
                "the CLAUSE sweep this commit added runs over the four clauses "
                "of their guards while no mutation deletes either return.",
                "Not a regression and disclosed in the commit message.  It is "
                "recorded because of the shape: the finer grain (clause) is "
                "swept from an ENUMERATED population, and the coarser grain "
                "(return) is still a hand-written table of eleven.  A `return` "
                "added to the predicate layer tomorrow gets no deletion test "
                "and nothing goes red; a CLAUSE added does.  The enumeration "
                "went to the rung the ticket named and not to the one above it.")
    return report()


if __name__ == "__main__":
    sys.exit(main())
