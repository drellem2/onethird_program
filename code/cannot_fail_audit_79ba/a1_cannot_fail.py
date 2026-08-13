"""mg-79ba A1 -- THE [CANNOT FAIL] ROW ACQUIRED A CONJUNCT THAT CANNOT FAIL.

mg-17aa was sent to remove forced conjuncts from scored conditions.  Its own
new code put one into the row named `[CANNOT FAIL]`.

    forced = (blocked == app)               # per row
    if forced:
        theorem_blocked += blocked
        theorem_app     += app
    ...
    check("PROVEN PROPERTY, ...",
          theorem_absorb == 0 and theorem_blocked == theorem_app,
          cannot_fail=True)

Both sums range over exactly the rows on which `blocked == app` holds term by
term, so `theorem_blocked == theorem_app` is an IDENTITY.  No input to this
program can make it false, and the artifact never says FORCED of it.

THAT ALONE WOULD BE A SMALL THING -- a redundant true conjunct beside a live
one, which is the class mg-17aa itself defines as "FORCED GIVEN A SCORED ROW"
and keeps on purpose.  What makes it a finding is the SENTENCE THE ROW PRINTS
BESIDE IT:

    "A FALSE theorem is still a failure: if some pair cleared both forced
     gates, or the predicate did report absorbable, this row FAILS"

The first disjunct is false as printed, and section 2 below DEMONSTRATES it by
running: a pair that clears both forced gates leaves the battery GREEN at
exit 0.  It does not fail the row, it removes the row's own evidence from the
row.  A row name that is not its measurement -- this arc's most repeated
defect -- one sentence along, inside the instrument built to remove it.

AND IT IS A REGRESSION, NOT AN INHERITANCE (section 4).  The conjunct this
replaced, `theorem_diag == theorem_app` under `forced = (diag_preserved == 0)`,
WAS falsifiable: `diag_moved` is counted after the shape guard, so a biting
pair with a shape mismatch is in `app` and in neither diagonal bucket.  That
input is exhibited here.  Against the pinned pre-mg-17aa tree it turns the
[CANNOT FAIL] row RED; against the shipped tree the same input leaves it GREEN.
mg-17aa closed the last gap that made the row falsifiable -- correctly, on the
mathematics, since a shape mismatch really does block absorbability -- and did
not notice that closing it left the conjunct with nothing to say.

WHAT THIS SECTION DOES NOT CLAIM.  Not that the theorem is false; the audit
takes no position on the mathematics of the two forced gates.  Not that
`theorem_absorb == 0` is forced -- it is not, and section 3 exhibits the world
that turns it red.  The finding is scoped to ONE conjunct of ONE row.

Run: python3 a1_cannot_fail.py
"""

import ast
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kern79ba import (                                          # noqa: E402
    BAR, FG, PRELUDE, Score, head, inject_absorbable,
    inject_clear_gate, inject_shape_mismatch, mutate, pinned_source,
    ANCHOR_COND, ANCHOR_COND_OLD, rows, row_diff, run, sandbox,
)

S = Score()
CANNOT_FAIL_KEY = "PROVEN PROPERTY, not a control row"


def find_fn(tree, name):
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    return None


def section_1_structural():
    """The identity, read out of the source by `ast` rather than argued."""
    head("A1.1 -- THE CONJUNCT IS AN IDENTITY, READ OUT OF THE SOURCE")
    src = open(os.path.join(FG, "controls.py")).read()
    fn = find_fn(ast.parse(src), "negative_control_incidence")
    S.claim("`negative_control_incidence` is present and parses", fn is not None)
    if fn is None:
        return

    # (a) the routing assignment, and what it compares
    routing = [n for n in ast.walk(fn)
               if isinstance(n, ast.Assign)
               and len(n.targets) == 1
               and isinstance(n.targets[0], ast.Name)
               and n.targets[0].id == "forced"]
    ok_routing = (
        len(routing) == 1
        and isinstance(routing[0].value, ast.Compare)
        and len(routing[0].value.ops) == 1
        and isinstance(routing[0].value.ops[0], ast.Eq)
        and isinstance(routing[0].value.left, ast.Name)
        and routing[0].value.left.id == "blocked"
        and isinstance(routing[0].value.comparators[0], ast.Name)
        and routing[0].value.comparators[0].id == "app")
    S.claim("`forced` is assigned exactly once in the function, and it is "
            "exactly `blocked == app` -- two plain names, no arithmetic",
            ok_routing,
            "%d assignment(s) to `forced`; line %s"
            % (len(routing), routing[0].lineno if routing else "-"))

    # (b) every write to the two accumulators, and where it sits
    def writes(name):
        out = []
        for n in ast.walk(fn):
            if isinstance(n, ast.AugAssign) and isinstance(n.target, ast.Name) \
                    and n.target.id == name:
                out.append(("+=", n))
            if isinstance(n, ast.Assign):
                for t in n.targets:
                    for nm in ast.walk(t):
                        if isinstance(nm, ast.Name) and nm.id == name:
                            out.append(("=", n))
        return out

    wb, wa = writes("theorem_blocked"), writes("theorem_app")
    aug_b = [n for k, n in wb if k == "+="]
    aug_a = [n for k, n in wa if k == "+="]
    S.claim("`theorem_blocked` and `theorem_app` are each written exactly "
            "twice: initialised to 0, then incremented at exactly one site",
            len(wb) == 2 and len(wa) == 2
            and len(aug_b) == 1 and len(aug_a) == 1,
            "theorem_blocked: %d write(s); theorem_app: %d write(s)"
            % (len(wb), len(wa)))

    ok_operand = (
        len(aug_b) == 1 and isinstance(aug_b[0].value, ast.Name)
        and aug_b[0].value.id == "blocked"
        and len(aug_a) == 1 and isinstance(aug_a[0].value, ast.Name)
        and aug_a[0].value.id == "app")
    S.claim("and each increment adds exactly the name the routing compares -- "
            "`theorem_blocked += blocked`, `theorem_app += app`", ok_operand)

    # (c) both increments guarded by `if forced:` and nothing else
    def guards(node):
        """Every `if` whose body (transitively) contains `node`."""
        found = []
        for n in ast.walk(fn):
            if isinstance(n, ast.If):
                for sub in n.body:
                    if node in list(ast.walk(sub)):
                        found.append(n)
        return found

    gb = guards(aug_b[0]) if aug_b else []
    ga = guards(aug_a[0]) if aug_a else []

    def is_forced_test(ifs):
        return (len(ifs) == 1 and isinstance(ifs[0].test, ast.Name)
                and ifs[0].test.id == "forced")

    S.claim("both increments sit under exactly one `if`, and its test is the "
            "bare name `forced` -- so the two sums range over the SAME rows, "
            "namely those with `blocked == app`",
            is_forced_test(gb) and is_forced_test(ga),
            "theorem_blocked guarded by %d if(s); theorem_app by %d"
            % (len(gb), len(ga)))

    S.claim("THEREFORE `theorem_blocked == theorem_app` IS AN IDENTITY.  Sum "
            "of `blocked` over {rows : blocked == app} equals sum of `app` "
            "over the same set, term by term.  No input to this program can "
            "make the conjunct false, and none is attempted below because "
            "none exists",
            ok_routing and ok_operand and is_forced_test(gb)
            and is_forced_test(ga))

    # (d) and the artifact does not say so
    art = open(os.path.join(FG, "controls_output.txt")).read()
    theorem_row = [l for l in art.split("\n") if CANNOT_FAIL_KEY in l]
    S.claim("the [CANNOT FAIL] row is in the committed artifact (it appears "
            "%d times -- once as the row and once in the closing summary)"
            % len(theorem_row), len(theorem_row) >= 1)
    row = theorem_row[0] if theorem_row else ""
    S.claim("and it prints the failure condition this section refutes -- "
            "\"if some pair cleared both forced gates ... this row FAILS\"",
            "if some pair cleared both forced gates" in row
            and "this row FAILS" in row)
    S.claim("and NOWHERE in the artifact is that conjunct called forced, "
            "identical, tautological or arithmetic -- the words the file uses "
            "freely of the OTHER forced conjuncts two screens away",
            not any(w in row for w in
                    ("theorem_blocked == theorem_app is forced",
                     "is an identity", "is arithmetic", "tautolog")),
            "the same row calls `rej == app` and `shape_ok == app` FORCED by "
            "name; this conjunct is not named at all")


def section_2_clears_both_gates():
    """The world the row's own sentence says it fails on."""
    head("A1.2 -- A PAIR THAT CLEARS BOTH FORCED GATES: THE ROW STAYS GREEN")
    base_tree = sandbox()
    code0, out0 = run(base_tree)
    base = rows(out0)
    S.claim("baseline: the shipped battery exits 0", code0 == 0,
            "%d scored rows" % len(base))

    worlds = []
    for mode, label in (("facet_offbyone", "row I4"),
                        ("ridge_facets", "row I1")):
        tree = sandbox()
        missed = mutate(tree, [PRELUDE, inject_clear_gate(mode, 1)])
        S.claim("the injection into %s lands as exactly one substitution at "
                "each of its two anchors" % label, not missed,
                "; ".join("%r matched %d times" % (o[:40], c) for o, c in missed)
                or "both anchors matched once")
        code, out = run(tree)
        worlds.append((label, mode, code, out))
        shutil.rmtree(tree, ignore_errors=True)

    for label, mode, code, out in worlds:
        changed, gone, added = row_diff(base, rows(out))
        theorem = [t for t, k in rows(out) if k.startswith(CANNOT_FAIL_KEY)]
        fails = [k for t, k in rows(out) if t == "[FAIL]"]
        print("\n  %s: exit %d, %d FAIL row(s), [CANNOT FAIL] row present=%s"
              % (label, code, len(fails), bool(theorem)))
        for a, b, k in changed:
            print("    verdict %s -> %s : %s" % (a, b, k[:70]))
        S.claim("%s -- one pair cleared BOTH forced gates and the battery "
                "still exits 0 with 0 FAIL rows.  The [CANNOT FAIL] row's own "
                "sentence says it FAILS here.  It does not: the row's routing "
                "drops that mutation out of `forced_rows`, so the row simply "
                "reports one corruption fewer" % label,
                code == 0 and not fails and bool(theorem),
                "exit %d; FAIL rows: %s" % (code, fails or "none"))
        S.claim("%s -- and the clause DID move where mg-17aa says it moves: "
                "`absorb == 0` is back in that row's scored condition, which "
                "is the half of the design that works" % label,
                "row DOES score it" in out,
                "the `else` branch mg-17aa kept is reached")
    shutil.rmtree(base_tree, ignore_errors=True)
    return base


def section_3_deletion_test(base):
    """Is the conjunct load-bearing on ANY world this audit can build?

    The method is mg-5f9a's, which mg-17aa itself applies to `rej == app` and
    `shape_ok == app` in its V5: delete the conjunct and require the artifact
    to CHANGE on some world.  Applied to the conjunct mg-17aa added.
    """
    head("A1.3 -- DELETION TEST ON THE CONJUNCT mg-17aa ADDED")
    DELETED = "              theorem_absorb == 0,   # mg-79ba deletion test"
    built = [
        ("real population", []),
        ("a pair of I4 clears both forced gates",
         [inject_clear_gate("facet_offbyone", 1)]),
        ("a pair of I1 clears both forced gates",
         [inject_clear_gate("ridge_facets", 1)]),
        ("a pair of I4 has a SHAPE mismatch",
         [inject_shape_mismatch("facet_offbyone", 1)]),
        ("a pair of I4 is reported ABSORBABLE while its gates stay violated",
         [inject_absorbable("facet_offbyone", 1)]),
    ]
    load_bearing = []
    for label, edits in built:
        keep_tree, del_tree = sandbox(), sandbox()
        m1 = mutate(keep_tree, ([PRELUDE] + edits) if edits else [])
        m2 = mutate(del_tree,
                    ([PRELUDE] + edits if edits else [])
                    + [(ANCHOR_COND, DELETED)])
        S.claim("world %r: every anchor of both trees matched exactly once"
                % label, not m1 and not m2,
                "keep: %d missed, delete: %d missed" % (len(m1), len(m2)))
        c1, o1 = run(keep_tree)
        c2, o2 = run(del_tree)
        same = rows(o1) == rows(o2)
        moved = "" if same else " <-- LOAD-BEARING"
        print("  %-62s keep exit %d / delete exit %d%s"
              % (label[:62], c1, c2, moved))
        if not same:
            load_bearing.append(label)
        shutil.rmtree(keep_tree, ignore_errors=True)
        shutil.rmtree(del_tree, ignore_errors=True)

    S.claim("`theorem_blocked == theorem_app` is load-bearing on NO world "
            "built here, including the two the row's own sentence names.  "
            "That is the same verdict mg-17aa's V5 reaches about `rej == app` "
            "and `shape_ok == app` -- and mg-17aa CLASSIFIES those two and "
            "names them in the artifact.  This one it does not",
            load_bearing == [],
            "load-bearing on: %s" % (", ".join(load_bearing) or "no world"))
    S.claim("and the row is NOT unfalsifiable overall -- its other conjunct "
            "`theorem_absorb == 0` does go red, on the world where the two "
            "procedures disagree.  So the finding is scoped to one conjunct, "
            "not to the row",
            True,
            "see the ABSORBABLE world above: it is the only world in this "
            "suite that turns the [CANNOT FAIL] row red")

    # and show that red explicitly
    tree = sandbox()
    mutate(tree, [PRELUDE, inject_absorbable("facet_offbyone", 1)])
    code, out = run(tree)
    theorem_fail = [k for t, k in rows(out)
                    if t == "[FAIL]" and k.startswith(CANNOT_FAIL_KEY)]
    S.claim("exhibited: with one pair reported absorbable, the [CANNOT FAIL] "
            "row goes RED at exit %d.  WHAT THAT WORLD IS, said plainly: two "
            "procedures disagreeing, not a corruption behaving differently.  "
            "`gate_violations` and `absorbable_by_diagonal_twist` are both "
            "derived from S.A.S = B, so no honest input reaches it -- the "
            "row's remaining measured content is a CONSISTENCY CHECK BETWEEN "
            "TWO IMPLEMENTATIONS, which is worth having and is not what the "
            "row says it is" % code,
            code != 0 and len(theorem_fail) == 1,
            "exit %d; [CANNOT FAIL] row red: %s" % (code, bool(theorem_fail)))
    shutil.rmtree(tree, ignore_errors=True)


def section_4_regression():
    """Was the conjunct it REPLACED falsifiable?  Same input, both trees."""
    head("A1.4 -- THE CONJUNCT IT REPLACED WAS FALSIFIABLE.  SAME INPUT, "
         "BOTH TREES")
    old = pinned_source()
    S.claim("the pre-mg-17aa controls.py is readable at its pinned blob "
            "(%d bytes)" % (len(old) if old else 0),
            old is not None and len(old) > 10000)
    if old is None:
        return
    S.claim("it carries the conjunct mg-17aa replaced, verbatim",
            ANCHOR_COND_OLD in old,
            "the literal %r is present" % ANCHOR_COND_OLD.strip())
    S.claim("and it routes on the single gate", "forced = (diag_preserved == 0)" in old)

    inj = inject_shape_mismatch("ridge_facets", 1)
    results = {}
    for label, src in (("pre-mg-17aa (pinned blob)", old), ("shipped", None)):
        tree = sandbox(src)
        missed = mutate(tree, [PRELUDE, inj])
        S.claim("the SHAPE-MISMATCH input applies to the %s tree at both "
                "anchors" % label, not missed,
                "; ".join("%r x%d" % (o[:40], c) for o, c in missed) or "ok")
        code, out = run(tree)
        red = [k for t, k in rows(out)
               if t == "[FAIL]" and k.startswith(CANNOT_FAIL_KEY)]
        results[label] = (code, bool(red), out)
        print("  %-28s exit %d, [CANNOT FAIL] row RED = %s"
              % (label, code, bool(red)))
        shutil.rmtree(tree, ignore_errors=True)

    old_red = results["pre-mg-17aa (pinned blob)"][1]
    new_red = results["shipped"][1]
    S.claim("ONE INPUT, TWO TREES: a biting pair with a shape mismatch turns "
            "the PRE-mg-17aa [CANNOT FAIL] row RED and leaves the SHIPPED one "
            "GREEN.  The conjunct mg-17aa removed had a falsifying input; the "
            "conjunct it installed has none.  `diag_moved` is counted after "
            "the shape guard `continue`, so such a pair is in `app` and in "
            "neither diagonal bucket -- `blocked` is asked BEFORE that guard, "
            "deliberately and with a comment saying why, which is what closed "
            "the gap",
            old_red and not new_red,
            "pre: RED=%s, shipped: RED=%s" % (old_red, new_red))
    S.claim("AND THE CHANGE WAS RIGHT ON THE MATHEMATICS, which is why this "
            "is a reporting finding and not a repair request: a shape "
            "mismatch DOES block absorbability, so counting it as blocked is "
            "correct and the old row's red there was a false alarm.  What is "
            "owed is that the row stop printing a falsification condition it "
            "no longer has",
            True,
            "the recommendation is in README.md section 4 and is one sentence "
            "of prose, not a scoring change")


def main():
    print(BAR)
    print("mg-79ba A1 -- THE [CANNOT FAIL] ROW'S OWN [CANNOT FAIL] CONJUNCT")
    print(BAR)
    section_1_structural()
    base = section_2_clears_both_gates()
    section_3_deletion_test(base)
    section_4_regression()
    return S.report()


if __name__ == "__main__":
    sys.exit(main())
