#!/usr/bin/env python3
"""mg-a74f — OPEN 2: THE SIX, INDIVIDUALLY, CLASSIFIED, AND CHECKED AT BOTH REVISIONS.

mg-16eb: *"Enumerate the six, and for each state whether it is false, unsupported, or
true-but-unevidenced — those need different repairs, and lumping them loses that.  Report the
six individually."*  This file is that report, and every row of it is a MEASUREMENT taken
twice: once at `bd24efc`, where the defect must still be present, and once at the working
tree, where it must be gone.  A row that does not fail at `bd24efc` is a row whose defect this
repair never demonstrated, and it is reported as such rather than passed.

The classification uses one of mg-16eb's three buckets and one it did not name:

    FALSE                        the sentence is refuted by the tree or by construction
    TRUE OF A DIFFERENT PROPERTY the sentence is true of what the instrument measures and
                                 false of what it names.  This is the bucket mg-16eb's list
                                 does not have and it is the bucket its OPEN 1 is about
    UNSUPPORTED                  no evidence either way          — 0 rows land here
    TRUE-BUT-UNEVIDENCED         true, nothing in the tree shows it — 0 rows land here

Two rows are repaired by CORRECTING a fact, one by IMPLEMENTING the missing behaviour, and
three by NARROWING a sentence to the property the code measures.  Those are three different
repairs and the point of enumerating is that they are not interchangeable.

    python3 code/state_delegation_repair_a74f/claims_a74f.py
"""
import ast
import os
import re
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
from prose_a74f import _quoted                                    # noqa: E402

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()
BEFORE = "bd24efc"

CTL = "code/state_landing_control_2da3/delta_control.py"
R49 = "code/state_delegation_repair_0049/render0049.py"
RDM = "code/state_delegation_repair_0049/README.md"
MUT = "code/state_delegation_repair_0049/mutations_0049.py"


def at(rev, path):
    if rev is None:
        with open(os.path.join(REPO, path), encoding="utf-8") as fh:
            return fh.read()
    return subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"],
                          capture_output=True, text=True, check=True).stdout


def in_tree(rev, path):
    if rev is None:
        return os.path.exists(os.path.join(REPO, path))
    return subprocess.run(["git", "-C", REPO, "cat-file", "-e", f"{rev}:{path}"],
                          capture_output=True).returncode == 0


def iterated_tables(rev):
    """The module-level path-keyed dicts of delta_control.py that some `for` iterates."""
    tree = ast.parse(at(rev, CTL))
    tables, iterated = set(), set()
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Dict):
            name = getattr(node.targets[0], "id", None)
            keys = [k.value for k in node.value.keys
                    if isinstance(k, ast.Constant) and isinstance(k.value, str)]
            if name and keys and all(re.match(r"^(code|docs)/", k) for k in keys):
                tables.add(name)
    for node in ast.walk(tree):
        if isinstance(node, ast.For):
            for sub in ast.walk(node.iter):
                if isinstance(sub, ast.Name):
                    iterated.add(sub.id)
    return tables, tables & iterated


def rows_of_mutations_0049(rev):
    tree = ast.parse(at(rev, MUT))
    for node in tree.body:
        if (isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "ROWS"
                and isinstance(node.value, ast.List)):
            return len(node.value.elts)
    return None


def unquoted_hits(text, phrase):
    """Occurrences of `phrase` that are NOT inside "..." or `...` on their own line — an
    assertion, as against a quotation of somebody else's assertion.  Same rule as
    prose_a74f.py P4's, imported from it rather than restated."""
    out = []
    for m in re.finditer(re.escape(phrase), text):
        bol = text.rfind("\n", 0, m.start()) + 1
        eol = text.find("\n", m.start())
        line = text[bol:eol if eol >= 0 else len(text)]
        if not _quoted(line, m.start() - bol):
            out.append(text[:m.start()].count("\n") + 1)
    return out


# =========================================================================================
# THE SIX.  Each is (id, where, the sentence, class, repair kind, before-probe, after-probe).
# A probe returns (bool, one line of detail).  `before` must be True (the defect is there)
# and `after` must be True (it is gone); both are printed either way.
# =========================================================================================
def c1_before():
    t = at(BEFORE, CTL)
    named = "code/state_delegation_repair_0049/guards_only_0049.py" in t
    return (named and not in_tree(BEFORE, "code/state_delegation_repair_0049/"
                                          "guards_only_0049.py"),
            f"delta_control.py names guards_only_0049.py: {named}; that path in the tree at "
            f"{BEFORE}: "
            f"{in_tree(BEFORE, 'code/state_delegation_repair_0049/guards_only_0049.py')}")


def c1_after():
    t = at(None, CTL)
    gone = "guards_only_0049.py" not in t
    named = "code/state_delegation_repair_0049/split_0049.py" in t
    return (gone and named and in_tree(None, "code/state_delegation_repair_0049/"
                                             "split_0049.py"),
            f"guards_only_0049.py gone: {gone}; split_0049.py named: {named}; that path "
            f"exists: {in_tree(None, 'code/state_delegation_repair_0049/split_0049.py')}")


def c2_before():
    t = at(BEFORE, CTL)
    hits = unquoted_hits(t, "all six rows")
    n = rows_of_mutations_0049(BEFORE)
    return (bool(hits) and n != 6,
            f"'all six rows' asserted at line(s) {hits}; mutations_0049.ROWS at {BEFORE}: "
            f"{n}")


def c2_after():
    t = at(None, CTL)
    six = unquoted_hits(t, "all six rows")
    nine = unquoted_hits(t, "all nine rows")
    n = rows_of_mutations_0049(None)
    return (not six and bool(nine) and n == 9,
            f"'all six rows' asserted at {six or 'nowhere'}; 'all nine rows' at {nine}; "
            f"mutations_0049.ROWS: {n}")


def c3_before():
    tables, it = iterated_tables(BEFORE)
    return ("DELEGATED_PRESENTATION" in tables - it,
            f"path-keyed tables {sorted(tables)}; iterated by some `for` {sorted(it)}")


def c3_after():
    tables, it = iterated_tables(None)
    t = at(None, CTL)
    grains = ("the PRESENTATION table declares exactly the DELEGATED target files" in t and
              "the sections with a PRESENTATION record are the sections declared" in t)
    return (tables == it and grains,
            f"path-keyed tables {sorted(tables)}; iterated {sorted(it)}; both key checks "
            f"present: {grains}  (the CONSTRUCTION is battery_a74f.py's A1 and A2, 0 -> 2)")


def c4_before():
    t = at(BEFORE, CTL)
    hits = unquoted_hits(t, "NO LONGER PRESENTED TO A READER")
    return (bool(hits),
            f"the exit-1 bullet asserts 'NO LONGER PRESENTED TO A READER' at line(s) {hits}")


def c4_after():
    t = at(None, CTL)
    hits = unquoted_hits(t, "NO LONGER PRESENTED TO A READER")
    narrowed = "PRESENTATION STATE IS NOT `rendered`" in t
    names_both = ("B3  `<details><summary>` at the top of a target" in t and
                  "C1  an ordinary fenced code example inside a cited section" in t)
    doc = ("NOT \"true iff a reader is shown this region\", which is what this docstring "
           "claimed" in t)
    return (not hits and narrowed and names_both and doc,
            f"asserted at {hits or 'nowhere'}; narrowed sentence present: {narrowed}; both "
            f"counterexamples named in the table: {names_both}; is_presented() docstring "
            f"narrowed: {doc}")


def _readme_rows(rev):
    return [ln for ln in at(rev, RDM).split("\n")
            if ln.startswith("| mg-218d's 16-mutation battery")
            or ln.startswith("| mg-5644's own battery")]


def c5_before():
    rows = _readme_rows(BEFORE)
    bad = [r for r in rows if "section 7" in r]
    return (len(rows) == 2 and len(bad) == 2,
            f"{len(rows)} rows found; {len(bad)} of them say 'section 7'")


def c5_after():
    rows = _readme_rows(None)
    ok = [r for r in rows if "section 8" in r and "section 7" not in r]
    body = at(None, "code/state_delegation_repair_0049/run_all.sh")
    eight = 'echo "### 8. mg-5644\'s OWN battery' in body
    return (len(rows) == 2 and len(ok) == 2 and eight,
            f"{len(rows)} rows found; {len(ok)} say section 8 and not section 7; run_all.sh "
            f"section 8 is mg-5644's battery: {eight}")


def c6_before():
    t = at(BEFORE, R49)
    hits = unquoted_hits(t, "SUPPRESSES NOTHING")
    head = "WHAT A READER IS SHOWN UNDER THIS REPAIR'S FIVE NEW ROWS" in t
    return (bool(hits) and head,
            f"'SUPPRESSES NOTHING' asserted at line(s) {hits}; the printed header claims "
            f"'WHAT A READER IS SHOWN': {head}")


def c6_after():
    t = at(None, R49)
    hits = unquoted_hits(t, "SUPPRESSES NOTHING")
    head = "WHAT IS IN THE RENDERED PAGE UNDER THIS REPAIR'S FIVE NEW ROWS" in t
    old = "WHAT A READER IS SHOWN UNDER THIS REPAIR'S FIVE NEW ROWS" in t
    ptr = "visible_a74f.py" in t
    return (not hits and head and not old and ptr,
            f"asserted at {hits or 'nowhere'} (it survives only inside quotation marks, "
            f"where it is a report of what the row used to say); header narrowed: {head}; "
            f"old header gone: {not old}; points at the instrument that does measure "
            f"suppression: {ptr}")


SIX = [
    ("1", f"{CTL}:233",
     "the guards-only decomposition lives in "
     "`code/state_delegation_repair_0049/guards_only_0049.py`",
     "FALSE", "CORRECT the fact — the path is wrong and a path is checkable",
     c1_before, c1_after),
    ("2", f"{CTL}:234",
     "that decomposition runs against \"all six rows\"",
     "FALSE", "CORRECT the fact — six is mg-5644's population, the script's is nine",
     c2_before, c2_after),
    ("3", f"{CTL}:798",
     "\"the two tables cannot drift apart quietly in EITHER direction\"",
     "FALSE", "IMPLEMENT the missing behaviour — the sentence is worth keeping, so the "
     "code is changed to make it true rather than the sentence weakened",
     c3_before, c3_after),
    ("4", f"{CTL}:346",
     "exit 1 is \"a region ... NO LONGER PRESENTED TO A READER\"",
     "FALSE", "NARROW to the measured property — refuted in BOTH directions, so there is "
     "no wording of it that survives; the predicate is named instead and both "
     "counterexamples are printed beside it",
     c4_before, c4_after),
    ("5", f"{RDM}:105-106",
     "mg-218d's and mg-5644's batteries are \"re-run in section 7 of run_all.sh\"",
     "FALSE", "CORRECT the fact — the re-runs happen; the pointer named the wrong section",
     c5_before, c5_after),
    ("6", f"{R49}:11",
     "R5: \"`<details>` at the top SUPPRESSES NOTHING: every cited section is still on the "
     "page as the document's own prose\"",
     "TRUE OF A DIFFERENT PROPERTY",
     "NARROW to the measured property — the two numbers are correct and neither is the "
     "claim; the row now says 'in the page' and points at visible_a74f.py",
     c6_before, c6_after),
]

# Where the six sit, and it is not an accident.  (file, does a program read its prose as
# claims AT bd24efc, how many of the six are in it).
WHERE = [
    (CTL, "no — every checker in this repo reads this file as the ground truth box", 4),
    (RDM, "no — nothing reads this README", 1),
    (R49, "no — nothing reads this docstring", 1),
    ("code/state_landing_control_2da3/COVERAGE.md",
     "YES — coverage218d.py, 40 of 40", 0),
]


def main():
    print("=" * 100)
    print("mg-a74f — THE SIX CLAIMS mg-16eb REFUTED, ONE ROW EACH, MEASURED AT BOTH ENDS")
    print("=" * 100)
    print(f"  before  {BEFORE}   (the defect must still be present)")
    print("  after   the working tree")
    print()

    bad = 0
    classes = {}
    for cid, where, sentence, klass, repair, before, after in SIX:
        ok_b, det_b = before()
        ok_a, det_a = after()
        classes[klass] = classes.get(klass, 0) + 1
        print(f"CLAIM {cid}   {where}")
        print(f"  says       {sentence}")
        print(f"  CLASS      {klass}")
        print(f"  REPAIR     {repair}")
        print(f"  [{'pass' if ok_b else 'FAIL'}] present at {BEFORE}: {det_b}")
        print(f"  [{'pass' if ok_a else 'FAIL'}] repaired in the tree: {det_a}")
        if not ok_b:
            print(f"         >>> this repair did NOT demonstrate claim {cid}'s defect at "
                  f"{BEFORE}; the row is reported, not passed")
            bad += 1
        if not ok_a:
            print(f"         >>> claim {cid} is NOT repaired in the working tree")
            bad += 1
        print()

    print("=" * 100)
    print("THE CLASSIFICATION, TALLIED — mg-16eb ASKED FOR THREE BUCKETS AND TWO ARE EMPTY")
    print("=" * 100)
    for klass in ("FALSE", "TRUE OF A DIFFERENT PROPERTY", "UNSUPPORTED",
                  "TRUE-BUT-UNEVIDENCED"):
        print(f"  {classes.get(klass, 0)}  {klass}")
    print()
    print("  UNSUPPORTED and TRUE-BUT-UNEVIDENCED are both 0, and that is worth saying")
    print("  rather than leaving as an absence: not one of the six was a claim nobody could")
    print("  check.  Every one was checkable by a program, and none of the six was checked")
    print("  by one.")
    print()

    print("=" * 100)
    print("THE CLAIM-GENERATION PROBLEM — WHERE THE SIX SIT")
    print("=" * 100)
    print("  mg-16eb: 'a deliverable that adds 17 claims and lands 11 has a claim-generation")
    print("  problem, not six unrelated slips'.  The population says what the problem is.")
    print()
    print(f"  {'file':<52s} {'read as claims at ' + BEFORE + '?':<48s} of the 6")
    for path, checked, n in WHERE:
        print(f"  {path:<52s} {checked:<48s} {n}")
    print()
    print("  THREE OF THE SIX ARE PURE CROSS-REFERENCE ROT — a path, a count, a section")
    print("  number.  Each is mechanically checkable and none was mechanically checked.")
    print("  prose_a74f.py's P1, P4 and P2 now check exactly those three shapes, over a")
    print("  computed population of three directories, and P3 checks the fourth (claim 3's")
    print("  code half).  Claims 4 and 6 are the SAME defect twice — a name for a measured")
    print("  property that claims more than the measurement — and no checker of this kind")
    print("  can catch that; it is caught by putting the instrument to a CONSTRUCTION, which")
    print("  is what mg-16eb did and what visible_a74f.py does.")
    print()

    print("=" * 100)
    print("EVERY INSTRUMENT THIS REPAIR ADDS, AND WHETHER ITS ROW NAME IS ITS MEASUREMENT")
    print("=" * 100)
    rows = [
        ("visible_a74f.py", "bytes-in-html",
         "the section marker is in the serialised HTML", "MATCHES"),
        ("visible_a74f.py", "not-suppressed",
         "not suppressed by any of five DECLARED mechanisms", "MATCHES — and is weaker "
         "than 'shown', by construction; the uncovered list prints on every run"),
        ("visible_a74f.py", "r16 SHOWN",
         "mg-16eb's rule, kept under mg-16eb's name", "DOES NOT MATCH, deliberately: the "
         "mismatch is the finding"),
        ("prose_a74f.py", "P1 path references",
         "the path is in the tree at that revision", "MATCHES"),
        ("prose_a74f.py", "P2 section references",
         "the section exists and names the tokens on the referencing line", "MATCHES — and "
         "it caught 1 of the 2 rows of claim 5; see README.md"),
        ("prose_a74f.py", "P3 pinned tables",
         "the table's name is in some `for`'s iterable", "MATCHES — it does not check that "
         "the iteration CHECKS anything; battery_a74f.py A1/A2 does"),
        ("prose_a74f.py", "P4 `all N rows`",
         "the number equals len(that script's ROWS)", "MATCHES"),
        ("battery_a74f.py", "exit codes",
         "read from the process by harness16eb.Tree", "MATCHES"),
        ("claims_a74f.py", "present at bd24efc / repaired in the tree",
         "a text or AST predicate over the two revisions", "MATCHES for claims 1, 2, 3 and "
         "5; for 4 and 6 it checks THE WORDING, and the property those two rows are about "
         "is measured by visible_a74f.py, not here"),
    ]
    for f, row, measures, verdict in rows:
        print(f"  {f:<17s} {row:<42s} measures: {measures}")
        print(f"  {'':<17s} {'':<42s} {verdict}")
    print()
    print(f"  {len(rows)} rows checked; the one that does not match its name is the one")
    print("  imported from the instrument under test, under its own name, on purpose.")
    print()

    print("=" * 100)
    print(f"{len(SIX) - 0} claims reported individually; {bad} probe(s) did not hold.")
    print("=" * 100)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
