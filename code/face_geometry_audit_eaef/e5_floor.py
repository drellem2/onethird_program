"""mg-eaef e5 -- THE FLOOR ITEM: two things the task list does not name.

An audit that only answers the questions it was handed can only ever confirm or
deny them.  Two things were chosen here, both outside every list in the ticket.

  FLOOR 1 -- RUN THE SUBJECT'S OWN INSTRUMENT AT HEAD AND READ ITS EXIT CODE.
  The landing document's Numbers paragraph says `92 claims, 0 BROKEN` and lists
  `d2 49`.  Every earlier round in this arc has been an argument about a
  transcript regenerating, so the cheapest unasked question is whether this one
  does.  It does not, and the reason is the repair itself: mg-f7e1 spelled the
  `shape` guard back into a TWO-CLAUSE condition, and `d2_deletion.py` carries a
  claim that the two-clause pin `b6bc2ef` is the NEWEST commit with a two-clause
  `shape` condition.  The commit that landed the repair is newer and has one.
  The document discloses a DIFFERENT and smaller consequence -- one transcript
  line about a commit count -- so this is not the disclosure being repeated.

  FLOOR 2 -- RUN THE COUNTERFACTUAL THE SUBJECT ASSERTS AND DOES NOT RUN.
  The repair's answer to the uncovered ORDER half is disclosure plus a named
  remedy: one pair, written out at `UNREACHED_GATE_PAIRS`, and the assertion
  that adding it "makes clause 1 go CHANGES, its registered prediction MISS, and
  the coverage claim go red saying so".  Nothing runs it.  It is run here, at
  HEAD and at `b6bc2ef` -- THE COMMIT WHERE THE DEFECT IS STILL PRESENT -- so
  the new control is shown catching the thing it exists for and not merely
  co-existing with a tree that no longer has it.
"""

import ast
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kern_eaef import (                                         # noqa: E402
    BAR, INSTR, REPO, SEPARATOR_ANCHOR, SEPARATOR_ROW, SHAPE_GUARD,
    SHAPE_GUARD_WIDTH_ONLY, build_tree, claim, finding, head, report,
    run_battery, run_instrument, show, source_at,
)

TRANSCRIPT = os.path.join(INSTR, "out_d2_deletion.txt")

# The two-clause guard as it stood at b6bc2ef, with the return beneath it so the
# anchor is unique -- `gate_violations` carries the same condition there.
OLD_GUARD = ('    if m != len(B) or any(len(A[i]) != len(B[i]) '
             'for i in range(m)):\n'
             '        return Trace(False, "shape", 0)')
OLD_GUARD_WIDTH_ONLY = ('    if any(len(A[i]) != len(B[i]) for i in range(m)):\n'
                        '        return Trace(False, "shape", 0)')


def shape_guard_clauses(src):
    """How many top-level clauses the `shape` guard of `absorb_trace` has in
    `src`, located by WHAT IT RETURNS rather than by any anchor of source text.
    0 means the condition is not a boolean expression at all."""
    tree = ast.parse(src)
    for fn in ast.walk(tree):
        if not isinstance(fn, ast.FunctionDef) or fn.name != "absorb_trace":
            continue
        for node in ast.walk(fn):
            if not isinstance(node, ast.If):
                continue
            labels = [n.value for n in ast.walk(node)
                      if isinstance(n, ast.Constant) and n.value == "shape"]
            if not labels or not any(isinstance(s, ast.Return)
                                     for s in node.body):
                continue
            return len(node.test.values) if isinstance(node.test, ast.BoolOp) \
                else 0
    return None


def commits_touching(path):
    r = subprocess.run(["git", "-C", REPO, "log", "--format=%H", "--", path],
                       capture_output=True, text=True)
    return [h for h in r.stdout.split() if h]


def main():
    print(BAR)
    print("mg-eaef e5 -- the floor item: the exit code, and the unrun remedy")
    print(BAR)
    print("\nPREDICTIONS, registered before these runs (PREDICTIONS.md e5):")
    print("   e5.1  `d2_deletion.py` re-run unmodified at HEAD exits 1 with "
          "exactly 1 BROKEN")
    print("   e5.2  8 commits have touched face_complex.py and 2 of them have "
          "a two-clause\n         `shape` guard; the newer is not the pin")
    print("   e5.3  with the named pair added, deleting the ORDER clause "
          "CHANGES the artifact\n         at HEAD -- and at b6bc2ef, where the "
          "same defect is still present\n")

    # ------------------------------------------------------------- FLOOR 1
    head("1.  THE INSTRUMENT THAT RAISED THE FINDINGS, RE-RUN UNMODIFIED")
    text, code = run_instrument(os.path.join(REPO, "code",
                                             "face_geometry_instr_5f9a"))
    committed = open(TRANSCRIPT).read()
    broken = [ln for ln in text.splitlines() if ln.startswith("  [BROKEN]")]
    summary = [ln for ln in text.splitlines() if "claim(s) scored" in ln]
    print("   run in place, nothing edited:  exit %d" % code)
    print("   summary line               :  %s"
          % (summary[-1] if summary else "(none)"))
    print("   committed transcript says  :  %s"
          % [ln for ln in committed.splitlines()
             if "claim(s) scored" in ln][-1])
    for ln in broken:
        print("\n   " + ln.strip())
    diff = [(a, b) for a, b in zip(text.splitlines(), committed.splitlines())
            if a != b]
    print("\n   lines that differ from the committed transcript: %d" % len(diff))
    for a, b in diff:
        print("      committed: %s" % b.strip()[:110])
        print("      re-run   : %s" % a.strip()[:110])
    claim("THE SUBJECT'S OWN `d2_deletion.py`, RUN IN PLACE WITH NOTHING "
          "EDITED, EXITS %d WITH %d BROKEN CLAIM(S) out of the 49 it scores"
          % (code, len(broken)),
          code == 1 and len(broken) == 1,
          "the pin claim being restated, or the pin being moved to this "
          "commit.  This claim is about the tree as committed at HEAD and is "
          "the reason the number below is not taken from the transcript",
          "the broken claim is the two-clause pin")

    head("2.  WHY IT BROKE -- and it is the repair's own respelling")
    hist = commits_touching("code/face_geometry/face_complex.py")
    two = []
    print("   %-10s %-8s %s" % ("commit", "clauses", "subject"))
    for h in hist:
        n = shape_guard_clauses(show(h, "code/face_geometry/face_complex.py"))
        subj = subprocess.run(["git", "-C", REPO, "log", "-1", "--format=%s", h],
                              capture_output=True, text=True).stdout.strip()
        if n == 2:
            two.append(h)
        print("   %-10s %-8s %s" % (h[:9], "n/a" if n is None else n, subj[:58]))
    pin = subprocess.run(["git", "-C", REPO, "rev-parse", "b6bc2ef"],
                         capture_output=True, text=True).stdout.strip()
    print("\n   commits that have ever touched face_complex.py : %d"
          % len(hist))
    print("   of those, with a TWO-CLAUSE `shape` guard      : %d (%s)"
          % (len(two), ", ".join(h[:9] for h in two)))
    print("   the newest of them                             : %s" % two[0][:9])
    print("   what the pin `b6bc2ef` resolves to             : %s" % pin[:9])
    claim("THE COMMIT THAT BROKE THE PIN IS THE REPAIR ITSELF: %d commit(s) "
          "have a two-clause `shape` guard, the newest is %s, and the pin "
          "resolves to %s -- so the claim `the NEWEST of them is b6bc2ef` "
          "became false at the moment mg-f7e1 landed"
          % (len(two), two[0][:9], pin[:9]),
          len(two) == 2 and two[0] != pin and two[-1] == pin,
          "a later commit merging the guard back into one comparison, which "
          "would restore the claim and lose the repair.  The guard is located "
          "here by the gate label it RETURNS, not by an anchor of source text, "
          "so a respelling does not hide a commit from this count",
          "history: %d commit(s); two-clause: %s"
          % (len(hist), ", ".join(h[:9] for h in two)))
    finding("E8", "THE INSTRUMENT DOES NOT REGENERATE AT HEAD, AND THE "
            "DISCLOSURE IS NARROWER THAN THE CONSEQUENCE.  The landing "
            "document says `92 claims, 0 BROKEN` and discloses that one "
            "transcript line -- `of the 7 commits that ever touched "
            "face_complex.py` -- will not regenerate once the commit lands.  "
            "What actually happens is that the pin claim's TRUTH CONDITION "
            "fails: `the NEWEST two-clause commit is b6bc2ef` is false because "
            "the repair reintroduced a two-clause guard, the claim reads "
            "[BROKEN], and `d2_deletion.py` exits 1 instead of 0.  The claim's "
            "own WOULD DIFFER UNDER names the event exactly -- `a later commit "
            "reintroducing a two-clause condition` -- and the commit that did "
            "it is the one that printed the sentence.",
            "population: the 49 claims d2_deletion.py scores; 1 BROKEN, %d "
            "transcript line(s) different, exit 0 -> 1.  d1, d3 and d4 "
            "regenerate byte-identically and exit 0." % len(diff))

    # ------------------------------------------------------------- FLOOR 2
    head("3.  THE REMEDY THE SUBJECT NAMES, RUN")
    print("The subject's own words: one pair `[[0,1],[1,0]]` against "
          "`[[0,1],[1,0],[0,0]]`\nwould cover the ORDER half in one line, and "
          "`adding it makes clause 1 go CHANGES,\nits registered prediction "
          "MISS, and the coverage claim go red saying so`.  That is\nan "
          "assertion about a run nobody has made.  Here it is, as a row of "
          "`UNREACHED_GATE_PAIRS[\"shape\"]`.\n")
    live_ctl = source_at(None, "controls.py")
    claim("THE ROW GOES WHERE THE SUBJECT SAYS IT GOES: the anchor it is "
          "spliced before occurs exactly once in controls.py, inside the "
          "`shape` list",
          live_ctl.count(SEPARATOR_ANCHOR) == 1,
          "`UNREACHED_GATE_PAIRS` being restructured, at which point this "
          "section is patching a table that no longer exists and says so "
          "instead of splicing into the wrong list",
          "anchor occurrences: %d" % live_ctl.count(SEPARATOR_ANCHOR))

    print("   %-38s %-11s %-10s %-5s" % ("tree", "new pair?", "artifact",
                                         "exit"))
    results = {}
    for ref, label, guard, width_only in (
            (None, "HEAD -- the repaired tree", SHAPE_GUARD,
             SHAPE_GUARD_WIDTH_ONLY),
            ("b6bc2ef", "b6bc2ef -- the defect still present", OLD_GUARD,
             OLD_GUARD_WIDTH_ONLY)):
        for added in (False, True):
            ctl = ([("controls.py", SEPARATOR_ANCHOR, SEPARATOR_ROW)]
                   if added else [])
            base, bcode = run_battery(build_tree(ctl, ref=ref))
            if not base:
                raise SystemExit(
                    "the %s tree %s the new row produced NO artifact -- the "
                    "battery did not run, so no IDENTICAL/CHANGES below would "
                    "mean anything" % (label, "with" if added else "without"))
            out, ocode = run_battery(build_tree(
                ctl + [("face_complex.py", guard, width_only)], ref=ref))
            changed = out != base
            results[(label, added)] = (changed, ocode, bcode, len(base))
            print("   %-38s %-11s %-10s %-5d   (baseline %d bytes, exit %d)"
                  % (label, "with" if added else "without",
                     "CHANGES" if changed else "IDENTICAL", ocode, len(base),
                     bcode))
    head_off = results[("HEAD -- the repaired tree", False)]
    head_on = results[("HEAD -- the repaired tree", True)]
    old_off = results[("b6bc2ef -- the defect still present", False)]
    old_on = results[("b6bc2ef -- the defect still present", True)]
    claim("THE NAMED PAIR IS THE COVERAGE IT IS SAID TO BE: at HEAD, deleting "
          "the ORDER clause alone is %s without it and %s with it, at exit %d "
          "-> %d"
          % ("BYTE-IDENTICAL" if not head_off[0] else "CHANGES",
             "CHANGES" if head_on[0] else "BYTE-IDENTICAL",
             head_off[1], head_on[1]),
          not head_off[0] and head_on[0] and head_on[1] == 1,
          "the pair being decided by the WIDTH half as well, which `zip` "
          "prevents by truncating at the shorter shape profile")
    claim("AND THE CONTROL IS DEMONSTRATED AGAINST A COMMIT WHERE THE DEFECT "
          "IS STILL PRESENT: at b6bc2ef -- mg-c4c8's two-clause tree, whose "
          "first clause deleted alone was byte-identical -- the same row turns "
          "that %s into %s at exit %d"
          % ("BYTE-IDENTICAL" if not old_off[0] else "CHANGES",
             "CHANGES" if old_on[0] else "BYTE-IDENTICAL", old_on[1]),
          not old_off[0] and old_on[0] and old_on[1] == 1,
          "the older tree's first clause already being covered, which would "
          "mean this row is not the thing that covers it.  A control shown "
          "only on a tree that no longer has the defect is a control nobody "
          "has seen bite",
          "b6bc2ef baseline %d bytes without the row, %d with it"
          % (old_off[3], old_on[3]))
    finding("E9", "THE REMEDY IS ONE LINE, IT WORKS, AND NOTHING RUNS IT.  The "
            "subject names the covering pair, states what adding it would do, "
            "and declines to add it -- correctly, since its point is that the "
            "reader should be able to see the uncovered row.  But the "
            "assertion about what would happen is unmeasured in a commit whose "
            "whole argument is that unmeasured assertions are how this lineage "
            "keeps going wrong.  Run here: it is exactly right at HEAD and at "
            "b6bc2ef.  The cost of leaving it unrun is that `NOT COVERED` "
            "cannot be told apart from `not coverable`.",
            "population: 2 trees x 2 states = 4 baselines and 4 deletions, all "
            "8 batteries regenerated in this run")
    return report()


if __name__ == "__main__":
    sys.exit(main())
