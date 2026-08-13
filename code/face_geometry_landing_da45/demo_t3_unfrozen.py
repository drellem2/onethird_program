#!/usr/bin/env python3
"""mg-686c -- TARGET 3, FROZEN AND UNFROZEN, WATCHED ON THE SAME EIGHT TREES.

mg-79ba's F2 is a claim about what a control REFUSES, and a claim about a
refusal is worth exactly as much as a run of it.  So this file does not argue
that mg-17aa's TARGET 3 froze the state it shipped: it plants eight trees, runs
BOTH readings of TARGET 3 on each -- the three source literals mg-17aa left,
verbatim, and the role-resolved reading that replaced them -- and tabulates what
each says beside what the battery itself says.

THE COLUMN THAT MATTERS IS THE THIRD, and it is the one the ticket is about:

  * On the five worlds that are REPAIRS or WIDENINGS -- restoring mg-17aa's own
    tautological conjunct, replacing it with a contingent one, annotating it,
    widening the routing to a third disjunct (THE SAME MOVE mg-17aa ITSELF
    MADE), renaming the routing decision -- the battery stays GREEN and the old
    literals REFUSE four of the five.  A control that refuses the repair of the
    defect it froze is not protecting anything; it is holding the defect in
    place.

  * On the three worlds that are SILENT DELETIONS -- the absorbability conjunct
    removed from the builder by hand, the routing written in as a constant, the
    theorem row's scored condition replaced by True -- the battery is STILL
    GREEN at exit 0, and the new reading goes RED on every one.  That is what
    the three literals were for, and it is kept.

AND THE FINDING IS NOT `THE OLD LITERALS MISS THE DELETIONS`.  They catch all
three.  They also refuse all five repairs and the shipped tree, so the one thing
they accept is the single state they were written against.  A verdict that says
RED to a repair and RED to a deletion in the same voice has not told them apart,
which is the whole content of `key it on the property, not on the bytes`.

WHAT THIS FILE PLANTS BY LITERAL AND WHY THAT IS NOT THE DEFECT IT REPORTS.
Every world below is a string edit of a staged copy of controls.py, so this
demonstration is keyed on the bytes of the tree it ships beside and will need
re-writing when they move.  That is the correct trade for a DEMONSTRATION and
the wrong one for a CONTROL: this file is not in any gate, it fails loudly and
locally if a world stops applying (`world did not apply` below, scored), and
nothing downstream depends on its verdict.  The distinction is the ticket's
whole point -- freeze the bytes in the exhibit, key the control on the property.

Run: python3 demo_t3_unfrozen.py        (measured 2026-08-13: 26 s)
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
FG = os.path.join(REPO, "code", "face_geometry")

# mg-17aa's three source literals, verbatim from the TARGET 3 this ticket
# re-aims.  They are quoted rather than described because the finding is about
# these exact bytes; `git show de86fee -- code/face_geometry_landing_da45` is
# where they came from.
OLD_LITERALS = [
    ("clause still in the file",
     lambda s: "if not forced:" in s and 'st["absorb"] == 0' in s),
    ("routing decided by the population",
     lambda s: "forced = (blocked == app)" in s
     and "gate_violations(L_mut, target)" in s),
    ("what it asserted is carried by a row that fails",
     lambda s: "theorem_absorb == 0 and theorem_blocked == theorem_app" in s),
]

TAUTOLOGY = "theorem_absorb == 0 and theorem_blocked == theorem_app"
REPAIRED = "theorem_absorb == 0,"
ROUTING = "forced = (blocked == app)"
CLAUSE_GUARD = "    if not forced:\n"

# (tag, what it is, the edit, what TARGET 3 should say).  A world whose edit
# does not apply is a failure of this file, not a verdict about anything.
WORLDS = [
    ("W0", "the shipped tree, untouched",
     None, "GREEN"),
    ("W1", "mg-17aa's tautological conjunct RESTORED -- the exact state the "
           "three literals demanded",
     (REPAIRED, TAUTOLOGY + ","), "GREEN"),
    ("W2", "the conjunct REPLACED BY A CONTINGENT ONE (mg-79ba's third spelling)",
     (REPAIRED, "theorem_absorb == 0 and theorem_blocked <= theorem_app,"),
     "GREEN"),
    ("W3", "the conjunct KEPT AND ANNOTATED as forced (mg-79ba's second spelling)",
     (REPAIRED, "theorem_absorb == 0 and True,          # forced by the routing"),
     "GREEN"),
    ("W4", "the routing WIDENED to a third disjunct -- mg-17aa's own move, one "
           "generation on",
     (ROUTING, "forced = (blocked == app or blocked_shape > app)"), "GREEN"),
    ("W5", "the routing decision RENAMED",
     ("forced", "routed"), "GREEN"),
    ("W6", "the absorbability conjunct DELETED BY HAND from the builder",
     (CLAUSE_GUARD, "    if False:\n"), "RED"),
    ("W7", "the routing WRITTEN IN instead of computed",
     (ROUTING, "forced = True"), "RED"),
    ("W8", "the theorem row's scored condition replaced by a constant",
     (REPAIRED, "True,"), "RED"),
]


def stage(edit):
    """A tree in which verify_landing.py's own REPO/FG resolution reaches an
    edited copy of code/face_geometry/ and the real tree is never written to."""
    root = tempfile.mkdtemp(prefix="t3world_")
    code = os.path.join(root, "code")
    os.makedirs(code)
    for d in ("face_geometry", "face_geometry_landing_da45"):
        shutil.copytree(os.path.join(REPO, "code", d), os.path.join(code, d),
                        ignore=shutil.ignore_patterns("__pycache__"))
    path = os.path.join(code, "face_geometry", "controls.py")
    src = open(path).read()
    if edit:
        old, new = edit
        if old == "forced":     # W5: rename, at every site including the
                                # builder's own parameter -- the first draft of
                                # this world renamed the call sites and not the
                                # parameter, and the battery died on a NameError
                                # rather than disagreeing, which is why `applied`
                                # is scored and the battery column is printed.
            sites = ((ROUTING, "routed = (blocked == app)"),
                     ("        if forced:\n", "        if routed:\n"),
                     ("nc4_row_conjuncts(localised, forced)",
                      "nc4_row_conjuncts(localised, routed)"),
                     ("    if not forced:\n", "    if not routed:\n"),
                     (") if forced else\n", ") if routed else\n"))
            applied = all(a in src for a, _ in sites)
            for a, b in sites:
                src = src.replace(a, b)
        else:
            applied = src.count(old) == 1
            src = src.replace(old, new, 1)
        open(path, "w").write(src)
    else:
        applied = True
    return root, src, applied


def run_target_3(root):
    """This ticket's TARGET 3, on a staged tree."""
    vl = os.path.join(root, "code", "face_geometry_landing_da45",
                      "verify_landing.py")
    r = subprocess.run([sys.executable, vl, "--target", "3"],
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def run_battery(root):
    """The battery's own verdict on the same tree, RUN rather than read out of
    TARGET 3's report of it.  The column exists to say `these trees are
    indistinguishable to the thing being watched`, and taking that from the
    watcher's own output would make the claim circular -- and would put two
    more `"literal" in out` membership tests into a file whose ticket is about
    exactly that shape (mg-9876's a4 smell index counts them, and it counted
    these two)."""
    r = subprocess.run([sys.executable, "controls.py", "5"],
                       cwd=os.path.join(root, "code", "face_geometry"),
                       capture_output=True, text=True)
    return r.returncode


def main():
    print("mg-686c -- TARGET 3, FROZEN AND UNFROZEN, ON THE SAME EIGHT TREES")
    print("=" * 78)
    print(__doc__.split("\n\n")[1])
    rows, bad = [], []
    for tag, what, edit, want in WORLDS:
        root, src, applied = stage(edit)
        try:
            if not applied:
                bad.append("%s: world did not apply -- the staged tree does not "
                           "contain what this file plants into" % tag)
                rows.append((tag, what, "n/a", "n/a", "n/a", want, "DID NOT APPLY"))
                continue
            old = sum(1 for _, fn in OLD_LITERALS if fn(src))
            brc = run_battery(root)
            rc, out = run_target_3(root)
            battery = "exit %d" % brc
            got = "GREEN" if rc == 0 else "RED"
            red = [l.strip()[:64] for l in out.split("\n")
                   if l.strip().startswith("- [")]
            rows.append((tag, what, battery,
                         "%d/3 pass" % old, got, want,
                         "; ".join(red) if red else ""))
            if got != want:
                bad.append("%s: TARGET 3 said %s, expected %s" % (tag, got, want))
        finally:
            shutil.rmtree(root, ignore_errors=True)

    print()
    print("%-4s %-9s %-11s %-6s %-9s %s"
          % ("", "battery", "OLD T3", "NEW", "expected", "world"))
    print("-" * 110)
    for tag, what, battery, old, got, want, note in rows:
        print("%-4s %-9s %-11s %-6s %-9s %s" % (tag, battery, old, got, want, what))
        if note:
            print("     %s" % note)
    keep = [r for r in rows if r[6] != "DID NOT APPLY"]
    rep = [r for r in keep if r[5] == "GREEN"]
    dele = [r for r in keep if r[5] == "RED"]
    old_ok = lambda rs: sum(1 for r in rs if r[3] == "3/3 pass")
    new_ok = lambda rs: sum(1 for r in rs if r[4] == "GREEN")
    print()
    print("READ THE TWO MIDDLE COLUMNS TOGETHER.  `OLD T3` is how many of "
          "mg-17aa's three")
    print("source literals still match, and three of three is the only passing "
          "score -- so")
    print("any row below three is a tree that instrument REFUSES.")
    print()
    print("  repairs and widenings (%d worlds)   OLD accepts %d   NEW accepts %d"
          % (len(rep), old_ok(rep), new_ok(rep)))
    print("  silent deletions      (%d worlds)   OLD accepts %d   NEW accepts %d"
          % (len(dele), old_ok(dele), new_ok(dele)))
    print("  the battery itself                 green on %d of %d"
          % (sum(1 for r in keep if r[2] == "exit 0"), len(keep)))
    print()
    print("THE OLD READING ACCEPTS EXACTLY ONE TREE AND IT IS THE ONE IT WAS "
          "WRITTEN")
    print("AGAINST -- W1, the state carrying the tautology.  It refuses the "
          "shipped tree,")
    print("it refuses all three of mg-79ba's repair spellings, it refuses the "
          "widening")
    print("mg-17aa itself performed one generation earlier, and it refuses the "
          "three")
    print("silent deletions too.  IT DOES REFUSE THE DELETIONS -- that is not "
          "the finding.")
    print("The finding is that its refusal carries no information: a verdict "
          "that says RED")
    print("to a repair and RED to a deletion alike has not distinguished them, "
          "and the")
    print("battery cannot tell these trees apart either -- all of them exit 0.")
    print("The role-resolved reading separates the two groups completely.")
    print()
    print("=" * 78)
    print("%d world(s); %d unsatisfactory." % (len(rows), len(bad)))
    for b in bad:
        print("   - " + b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
