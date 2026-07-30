"""mg-c4c8 H4 -- THE DECLARED UNIT IS A CLAIM, CHECKED AGAINST ITS PATCH.

mg-9220's improvement over the rule it was given is that every mutation now
DECLARES the unit it removes, and the `return` count is counted from the patch
text rather than asserted.  That is better than a rule, because it is
self-describing.  It also inherits an obligation: **a declared unit is a claim,
and it is the claim the deletion evidence rests on.**  A mutation that declares
a different unit than it removes reads as evidence about the declared unit, and
the declaration is exactly what a reader consults instead of the patch.

SO EVERY ONE OF THE ELEVEN IS CHECKED HERE, against the tree it is applied to:

  * the patch is applied (their own `text.replace`, their own anchor, on the
    tree their own `run_case` uses -- live, `PRE_REPAIR_REF`, or
    `TWO_RETURN_REF`);
  * both trees are PARSED, and the units removed are counted from the syntax:
    `return` statements, OTHER statements, and top-level boolean CLAUSES;
  * that measurement is compared with the declaration, in a reading of the
    English written down here beside it.

WHAT THIS FILE DOES NOT DO.  It does not parse their prose.  A machine reading
of an English sentence is a claim of this instrument's own, so the reading is
written out as a triple next to the sentence it reads, and a reader who disagrees
with the reading can see both.

THE FLOOR ITEM -- one thing no list in the brief names, chosen by this audit:
THE PROVENANCE OF THE PINNED COMMITS.  `TWO_RETURN_REF = "c7f9673"` is described
as "the last commit in which `absorb_trace`'s `shape` gate had TWO `return`
statements".  R1, R2 and R3 -- the whole reproduction of mg-e7bc's finding -- are
measurements about that tree, and every one of them is worthless if the pin names
a different tree than the sentence does.  Nothing in the subject or in the brief
checks it, so it is checked here by walking every commit that ever touched
`face_complex.py` and counting the `shape` returns in each.
"""

import ast
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kernc4c8 import (BAR, FC, INSTR, PRE_REPAIR_REF, ROOT,           # noqa: E402
                      TWO_RETURN_REF, claim, finding, footer, head, read)

sys.path.insert(0, INSTR)
import d2_deletion as d2                                              # noqa: E402

LANDING = os.path.join(ROOT, "docs", "landing-mg-e7bc-granularity.md")


def census(src):
    """(returns, other statements, boolean clauses) of a source text.

    `pass` is excluded from the statement count: a mutation that replaces a
    statement with `pass` has removed it, and counting `pass` would report that
    nothing went.
    """
    t = ast.parse(src)
    rets = sum(1 for n in ast.walk(t) if isinstance(n, ast.Return))
    stmts = sum(1 for n in ast.walk(t)
                if isinstance(n, ast.stmt) and not isinstance(n, ast.Pass))
    clauses = sum(len(n.values) - 1 for n in ast.walk(t)
                  if isinstance(n, ast.BoolOp))
    return rets, stmts - rets, clauses


def source_at(ref, path="code/face_geometry/face_complex.py"):
    r = subprocess.run(["git", "show", "%s:%s" % (ref, path)], cwd=ROOT,
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("cannot read %s:%s" % (ref, path))
    return r.stdout


# THE READING.  (returns, other statements, clauses) that the declared unit
# would have to remove for the declaration to be exact.  Written here, beside
# the sentence, so the reading is auditable rather than implied.
READING = {
    "BEFORE-1": (0, 0, 1),
    "BEFORE-2": (1, 0, 0),
    "AFTER-1": (1, 0, 0),
    "AFTER-2": (1, 0, 0),
    "AFTER-3": (0, 0, 0),
    "AFTER-4": (0, 1, 0),
    "AFTER-5": (1, 0, 0),
    "AFTER-6": (1, 0, 0),
    "R1": (1, 0, 0),
    "R2": (1, 0, 0),
    "R3": (2, 0, 0),
}

TREE_OF = {"BEFORE": PRE_REPAIR_REF, "AFTER": None, "R": TWO_RETURN_REF}

# Registered before the runs: which declarations this audit expects to be
# EXACT, and which to understate.  A mutation that replaces `if C: return X`
# with nothing or with `pass` removes the `if` as well as the `return`, and the
# declaration says only "one `return` statement".
PREDICTED_EXACT = {"BEFORE-1": True, "BEFORE-2": False, "AFTER-1": False,
                   "AFTER-2": False, "AFTER-3": True, "AFTER-4": True,
                   "AFTER-5": False, "AFTER-6": False, "R1": False,
                   "R2": False, "R3": False}


def main():
    print(BAR)
    print("mg-c4c8 H4 -- every declared unit, checked against its own patch")
    print(BAR)

    live = read(FC)
    trees = {None: live, PRE_REPAIR_REF: source_at(PRE_REPAIR_REF),
             TWO_RETURN_REF: source_at(TWO_RETURN_REF)}

    head("1. THE DECLARED UNIT vs THE PATCH -- all eleven")
    print("PREDICTIONS, registered before the runs (EXACT = the declaration "
          "accounts for\nevery unit the patch removes):")
    for tag, want in PREDICTED_EXACT.items():
        print("   %-9s %s" % (tag, "EXACT" if want else "UNDERSTATES"))
    print()
    print("   %-9s %-22s %-22s %-7s %s"
          % ("tag", "DECLARED (r/s/c)", "MEASURED (r/s/c)", "their n",
             "verdict"))
    rows = []
    for tag, edit, unit in d2.UNITS:
        ref = TREE_OF[tag.split("-")[0] if "-" in tag else "R"]
        src = trees[ref]
        fname, old, new = edit
        if fname != "face_complex.py":
            raise SystemExit("%s patches %s, not face_complex.py" % (tag, fname))
        n_anchor = src.count(old)
        if n_anchor != 1:
            raise SystemExit("%s: anchor occurs %d times in %s"
                             % (tag, n_anchor, ref or "the live tree"))
        mut = src.replace(old, new)
        b, a = census(src), census(mut)
        measured = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
        declared = READING[tag]
        theirs = d2.returns_removed(edit)
        exact = measured == declared
        rows.append((tag, declared, measured, theirs, exact, unit, ref))
        print("   %-9s %-22s %-22s %-7d %s"
              % (tag, "%d/%d/%d" % declared, "%d/%d/%d" % measured, theirs,
                 "EXACT" if exact else "*** UNDERSTATES ***"))

    print("\n   the sentence each reading is a reading OF:")
    for tag, _d, _m, _t, _e, unit, ref in rows:
        print("   %-9s (%s) %s" % (tag, ref or "live tree", unit))

    pmiss = [r for r in rows if r[4] != PREDICTED_EXACT[r[0]]]
    print("\n  prediction score: %d of %d matched."
          % (len(rows) - len(pmiss), len(rows)))
    for tag, _d, _m, _t, exact, _u, _r in pmiss:
        print("   MISS %-9s predicted %s, observed %s"
              % (tag, "EXACT" if PREDICTED_EXACT[tag] else "UNDERSTATES",
                 "EXACT" if exact else "UNDERSTATES"))

    claim(all(r[3] == r[2][0] for r in rows),
          "THE COUNTER IS HONEST: `returns_removed`, which counts lines "
          "beginning `return ` in the patch text, agrees with the number of "
          "`return` nodes the patch actually removes, on %d of %d mutations"
          % (sum(1 for r in rows if r[3] == r[2][0]), len(rows)),
          "a patch whose replacement text contains a `return` inside a string "
          "or a comment, or a multi-line return whose first line does not "
          "begin with the keyword.  The counter is a line heuristic and this "
          "is the parse that says the heuristic is right here",
          "; ".join("%s: counter %d, AST %d" % (t, th, m[0])
                    for t, _d, m, th, _e, _u, _r in rows))

    understating = [r for r in rows if not r[4]]
    finding(bool(understating),
            "THE DECLARED UNIT IS FINER THAN THE PATCH ON %d OF %d MUTATIONS, "
            "AND ON AFTER-5 THE DIFFERENCE IS THE THIRD-LEVEL UNIT ITSELF.  "
            "Each of %s declares 'one `return` statement' (R3: two) and its "
            "patch removes the `return` TOGETHER WITH THE `if` THAT GUARDS "
            "IT -- measured by parsing both trees, not read off the prose.  "
            "AFTER-5 removes, in addition, a boolean condition with TWO "
            "CLAUSES: `m != len(B) or any(len(A[i]) != len(B[i]) for i in "
            "range(m))`.  So the line a reader consults says the unit is one "
            "return, and the unit is a return plus a two-clause condition -- "
            "which is mg-e7bc's own sentence, at the level below the one it "
            "was written about.  THE RESULTS ARE NOT AFFECTED: H1 ran the "
            "strictly-return-only version of AFTER-1, -2, -5 and -6 (returns "
            "#47, #48, #46, #50, each replaced by `pass` with its `if` left "
            "standing) and every artifact verdict and exit code agreed.  This "
            "is a defect of the DECLARATION, which is now the thing the "
            "evidence rests on"
            % (len(understating), len(rows),
               ", ".join(r[0] for r in understating))
            if understating else "")

    head("2. AND THE LANDING DOCUMENT'S TABLE, against the code it describes")
    doc = read(LANDING)
    doc_rows = {}
    for m in re.finditer(r"^\|\s*([A-Z0-9, \-]+?)\s*\|\s*\*{0,2}([0-9, ]+?)"
                         r"\*{0,2}\s*\|", doc, re.M):
        tags, nums = m.group(1), m.group(2)
        tl = [t.strip() for t in tags.split(",")]
        nl = [n.strip() for n in nums.split(",")]
        if len(tl) == len(nl):
            for t, n in zip(tl, nl):
                if t in READING:
                    doc_rows[t] = int(n)
    wrong = [(t, doc_rows[t], dict((r[0], r[2][0]) for r in rows)[t])
             for t in doc_rows if doc_rows[t] != dict((r[0], r[2][0])
                                                      for r in rows)[t]]
    claim(len(doc_rows) == len(rows) and not wrong,
          "docs/landing-mg-e7bc-granularity.md's `ret` column names all %d "
          "mutations and every figure equals the returns its patch removes, "
          "measured here from the trees" % len(doc_rows),
          "a mutation being added to d2_deletion.py without the table being "
          "regenerated, or a figure in the table being edited by hand.  The "
          "table is prose about code and this is the only thing that compares "
          "them",
          "table: %s" % ", ".join("%s=%d" % (t, doc_rows[t])
                                  for t in sorted(doc_rows)))

    head("3. THE INERT RETURN IS GONE RATHER THAN ANNOTATED")
    fn = next(n for n in ast.walk(ast.parse(live))
              if isinstance(n, ast.FunctionDef) and n.name == "absorb_trace")
    shape_rets = [n for n in ast.walk(fn)
                  if isinstance(n, ast.Return) and isinstance(n.value, ast.Call)
                  and getattr(n.value.func, "id", "") == "Trace"
                  and n.value.args[1].value == "shape"]
    old_fn = next(n for n in ast.walk(ast.parse(trees[TWO_RETURN_REF]))
                  if isinstance(n, ast.FunctionDef) and n.name == "absorb_trace")
    old_shape = [n for n in ast.walk(old_fn)
                 if isinstance(n, ast.Return) and isinstance(n.value, ast.Call)
                 and getattr(n.value.func, "id", "") == "Trace"
                 and n.value.args[1].value == "shape"]
    claim(len(shape_rets) == 1 and len(old_shape) == 2,
          "THE SHAPE GATE HAS ONE `return` AND HAD TWO: %d at HEAD, %d at %s.  "
          "The statement mg-e7bc found inert is REMOVED FROM THE SOURCE, not "
          "annotated -- there is no second `shape` return carrying a comment "
          "about why it stays"
          % (len(shape_rets), len(old_shape), TWO_RETURN_REF),
          "the inert return being restored with an explanation beside it, "
          "which is the outcome pm-onethird names as not a fix: a comment is a "
          "reason a statement does not have.  Counted from the tree, so a "
          "return re-added inside an `if False:` or behind a flag would still "
          "be counted here",
          "HEAD: %d `shape` return(s) at line(s) %s; %s: %d at line(s) %s"
          % (len(shape_rets), [n.lineno for n in shape_rets], TWO_RETURN_REF,
             len(old_shape), [n.lineno for n in old_shape]))

    # And nothing was added to controls.py to WATCH the first return instead.
    ctl_now = read(os.path.join(os.path.dirname(FC), "controls.py"))
    ctl_old = source_at(TWO_RETURN_REF, "code/face_geometry/controls.py")
    rows_now = ctl_now.count("UNREACHED_GATE_PAIRS")
    pairs_now = len(re.findall(r'^\s+\("', ctl_now, re.M))
    pairs_old = len(re.findall(r'^\s+\("', ctl_old, re.M))
    claim(pairs_now == pairs_old,
          "and NOTHING WAS ADDED TO controls.py TO WATCH IT INSTEAD: the "
          "number of constructed-pair entries is %d at HEAD and %d at %s"
          % (pairs_now, pairs_old, TWO_RETURN_REF),
          "a pair being added to UNREACHED_GATE_PAIRS whose only purpose is to "
          "make the first return fire -- which is the 'detection' half of the "
          "ticket that mg-9220 declined, and which would leave an inert "
          "statement in the tree with a row built to visit it",
          "UNREACHED_GATE_PAIRS mentioned %d time(s); pair entries %d -> %d"
          % (rows_now, pairs_old, pairs_now))

    head("4. FLOOR ITEM -- the provenance of the pinned commits")
    print("Chosen by this audit; no list in the brief names it.  R1, R2 and R3 "
          "are the whole\nreproduction of mg-e7bc's finding, and they are "
          "measurements about whatever tree\n`TWO_RETURN_REF` names.  The "
          "docstring says it is 'the last commit in which\n`absorb_trace`'s "
          "`shape` gate had TWO `return` statements'.  That is a claim about "
          "the\nhistory of one file, and it is checked by walking the "
          "history.\n")
    log = subprocess.run(
        ["git", "log", "--format=%H", "--", "code/face_geometry/face_complex.py"],
        cwd=ROOT, capture_output=True, text=True).stdout.split()
    two_at = []
    for sha in log:
        try:
            s = source_at(sha)
            f = next((n for n in ast.walk(ast.parse(s))
                      if isinstance(n, ast.FunctionDef)
                      and n.name == "absorb_trace"), None)
        except Exception:                                       # noqa: BLE001
            continue
        if f is None:
            continue
        k = len([n for n in ast.walk(f)
                 if isinstance(n, ast.Return) and isinstance(n.value, ast.Call)
                 and getattr(n.value.func, "id", "") == "Trace"
                 and n.value.args[1].value == "shape"])
        if k == 2:
            two_at.append(sha)
    resolved = subprocess.run(["git", "rev-parse", TWO_RETURN_REF], cwd=ROOT,
                              capture_output=True, text=True).stdout.strip()
    print("  %d commit(s) touched face_complex.py; %d of them have TWO `shape` "
          "returns in\n  `absorb_trace`.  The newest of those is %s."
          % (len(log), len(two_at), two_at[0][:12] if two_at else "none"))
    claim(bool(two_at) and two_at[0] == resolved,
          "THE PIN IS WHAT ITS DOCSTRING SAYS: %s resolves to %s, and that is "
          "the NEWEST commit touching face_complex.py whose `absorb_trace` has "
          "two `shape` returns"
          % (TWO_RETURN_REF, resolved[:12]),
          "a later commit reintroducing a second `shape` return, or the pin "
          "being moved to an ancestor.  Either makes R1/R2/R3 measurements "
          "about a tree the sentence beside them does not describe -- and the "
          "sentence is the only thing a reader has, since a resolved sha in a "
          "transcript cannot be checked against a claim nobody wrote down",
          "newest two-return commit %s; pin resolves to %s; %d two-return "
          "commit(s) in all"
          % (two_at[0][:12] if two_at else "none", resolved[:12], len(two_at)))

    pre = subprocess.run(["git", "rev-parse", PRE_REPAIR_REF], cwd=ROOT,
                         capture_output=True, text=True).stdout.strip()
    pre_src = trees[PRE_REPAIR_REF]
    claim("absorb_trace" not in pre_src and "Trace(" not in pre_src,
          "and PRE_REPAIR_REF (%s -> %s) really is a tree from BEFORE the "
          "predicate was instrumented: it has no `absorb_trace` and no `Trace` "
          "at all" % (PRE_REPAIR_REF, pre[:12]),
          "the pin being moved forward past mg-5f9a, which is the exact defect "
          "mg-04a8 fixed when the ref was `main`: the BEFORE half would then "
          "be contrasting the tree with itself",
          "%d bytes at that ref" % len(pre_src))

    return footer()


if __name__ == "__main__":
    sys.exit(main())
