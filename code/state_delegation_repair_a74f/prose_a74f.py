#!/usr/bin/env python3
"""mg-a74f — OPEN 2's STRUCTURAL HALF: AN EXTERNAL CHECKER FOR PROSE CLAIMS.

mg-16eb's OPEN 2 says a deliverable that adds 17 claims and lands 11 has a CLAIM-GENERATION
PROBLEM, not six unrelated slips.  The population says where the problem is: 4 of the 6 broken
claims are in `delta_control.py`, which every checker in this repository reads AS THE GROUND
TRUTH BOX and therefore cannot check; 1 is in a README that nothing reads; 1 is in a
docstring that nothing reads; and 0 are in `COVERAGE.md`, the one added document that has an
external checker — `coverage218d.py` — even though COVERAGE.md names the same script and the
same count, correctly, in the same paragraph where `delta_control.py` gets both wrong.

The difference is not care.  It is whether a program reads the prose as claims.  This file is
that program, for three shapes of claim and one shape of guard, and for nothing else:

    P1  every repo-relative path named in the text EXISTS at the revision being read
    P2  every `section N` reference to a `run_all.sh` RESOLVES to a section of it, and every
        mg-id and script basename named on the referencing line occurs in that section
    P4  every `all N rows` phrase equals the `ROWS` of the script it names, derived from that
        script's own AST (or from the module it imports `ROWS` from)
    P3  every module-level dict of `delta_control.py` keyed by repo paths is ITERATED by
        some `for` in that file.  A pinned table nothing visits cannot fail in the direction
        that would need visiting, which is broken claim 3 exactly; a third such table added
        later joins this population by existing.

WHAT THIS DOES NOT CHECK, AND THE LIST IS THE POINT.  Every other claim in every file it
walks: every count that is not an `all N rows` phrase, every "cannot", every "measured over
N", every claim about what a reader is shown.  Those sentences now sit NEXT TO checked ones
in files this program walks, and a reader who knows this checker exists may take the
neighbours as covered.  They are not.

WHAT IT DOES COVER, OF THE SIX CLAIMS mg-16eb REFUTED: P1 covers claim 1, P4 covers claim 2,
P3 covers claim 3's code half, and P2 covers ONE of the two rows of claim 5.  That is three
and a half of six.  It covers NEITHER claim 4 NOR claim 6, and it cannot: both are a name for
a measured property that claims more than the measurement, and no reference-checker of this
kind can see that.  Those two are caught by putting the instrument to a CONSTRUCTION —
mg-16eb's B3 and C1, and this repair's `visible_a74f.py`.

THE HALF OF CLAIM 5 IT MISSES, stated because a coverage figure without its gap is the defect
one directory over.  mg-0049's README said BOTH batteries were re-run in section 7.  P2's
fail-closed rule is that every mg-id on the referencing line must occur in the section named:
the mg-5644 row fails, because section 7 does not mention mg-5644.  The mg-218d row PASSES at
`bd24efc`, wrongly, because section 7 runs `coverage218d.py` and its echoed title does say
`mg-218d`.  Deciding that the row is about mg-218d's BATTERY and not about mg-218d's coverage
checker needs the sentence's meaning, and this program does not have it.  Claim 5's other
half is caught by `claims_a74f.py`'s anchored check, which is a hand check of two named table
rows and is labelled as one there.

    python3 code/state_delegation_repair_a74f/prose_a74f.py            # the working tree
    python3 code/state_delegation_repair_a74f/prose_a74f.py --rev REV  # any revision

Reading from a revision is not a convenience: this repair must demonstrate its checker
against a commit where the defect is still present, and `--rev bd24efc` is that commit.
"""
import argparse
import ast
import os
import re
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()

# The declared population.  Three directories, every .py, .md and .sh in them; the file list
# is COMPUTED from the tree at the revision being read and printed with its size, never a
# hand list.  This repair's own directory is in it, so this checker checks its own prose.
DIRS = [
    "code/state_landing_control_2da3",
    "code/state_delegation_repair_0049",
    "code/state_delegation_repair_a74f",
]
EXTS = (".py", ".md", ".sh")

# FILES WHOSE PROSE IS A REPORT OF ANOTHER FILE'S CLAIMS.  A checker that reads a report of
# a defect as a fresh instance of the defect is measuring the wrong thing: `claims_a74f.py`
# names `guards_only_0049.py` three times BECAUSE that path does not exist, and quotes "all
# six rows" BECAUSE six is wrong.  These two files are excluded from P1, P2 and P4, and the
# exclusion is FAIL-CLOSED IN BOTH DIRECTIONS: the count of matches each one suppresses is
# printed on every run, an entry naming a file that is not in the population is a FAIL, and
# an entry that suppresses NOTHING is a FAIL, so this list cannot rot into a silent blanket.
# Nothing else is exempt.  In particular delta_control.py, both READMEs, COVERAGE.md,
# render0049.py, every run_all.sh and this file itself are checked.
REPORTS = {
    "code/state_delegation_repair_a74f/PREDICTIONS.md":
        "the predictions, which quote each of the six broken claims verbatim",
    "code/state_delegation_repair_a74f/claims_a74f.py":
        "the report of the six, which names each broken path and count to report it",
}
_suppressed = {}


def reporting(rel):
    return rel in REPORTS


def note_suppressed(rel, n=1):
    _suppressed[rel] = _suppressed.get(rel, 0) + n

_PATH = re.compile(r"\b(?:code|docs)/[A-Za-z0-9_./-]*[A-Za-z0-9_-]\.(?:py|md|sh|js|txt|json)\b")
_SECTION = re.compile(r"\bsection (\d+)\b")
_RUNALL = re.compile(r"run_all\.sh")
_MGID = re.compile(r"\bmg-[0-9a-f]{4}\b")
_SCRIPT = re.compile(r"\b([A-Za-z0-9_]+\.(?:py|sh))\b")
# `run_all.sh` numbers its sections with `echo "### N. title"`.
_ECHOSEC = re.compile(r'^echo "###\s*(\d+)\.\s*(.*?)"\s*$', re.M)

def ls_tree(rev):
    out = subprocess.run(["git", "-C", REPO, "ls-tree", "-r", "--name-only", rev],
                         capture_output=True, text=True, check=True).stdout
    return set(out.splitlines())


def read_at(rev, path):
    return subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"],
                          capture_output=True, text=True, check=True).stdout


def worktree_files():
    got = set()
    for root, _dirs, files in os.walk(REPO):
        if "/.git" in root:
            continue
        for f in files:
            got.add(os.path.relpath(os.path.join(root, f), REPO))
    return got


def population(rev):
    """(the file list, a reader for it, the set of paths that exist).  Computed, printed."""
    if rev:
        tree = ls_tree(rev)
        files = sorted(p for p in tree
                       if any(p.startswith(d + "/") for d in DIRS) and p.endswith(EXTS))
        return files, (lambda p: read_at(rev, p)), tree
    tree = worktree_files()
    files = sorted(p for p in tree
                   if any(p.startswith(d + "/") for d in DIRS) and p.endswith(EXTS))

    def rd(p):
        with open(os.path.join(REPO, p), encoding="utf-8") as fh:
            return fh.read()
    return files, rd, tree


_bad = []


def report(pid, ok, where, what, detail=""):
    print(f"  [{'pass' if ok else 'FAIL'}] {pid}  {where}")
    print(f"         {what}")
    if detail:
        for line in detail.splitlines():
            print(f"         {line}")
    if not ok:
        _bad.append((pid, where, what))
    return ok


def check_paths(files, rd, exists):
    print("=" * 100)
    print("P1.  EVERY REPO-RELATIVE PATH NAMED IN THE TEXT EXISTS AT THIS REVISION")
    print("=" * 100)
    refs = []
    for rel in files:
        text = rd(rel)
        for m in _PATH.finditer(text):
            if reporting(rel):
                if m.group(0) not in exists:
                    note_suppressed(rel)
                continue
            refs.append((rel, text[:m.start()].count("\n") + 1, m.group(0)))
    print(f"  population: {len(refs)} path references over {len(files)} files "
          f"({len(set(r[2] for r in refs))} distinct paths).  Computed from the tree, "
          f"not a hand list.")
    misses = [r for r in refs if r[2] not in exists]
    for rel, line, path in misses:
        report("P1", False, f"{rel}:{line}", f"names {path}", "which is not in the tree")
    if not misses:
        print(f"  [pass] P1  0 of {len(refs)} path references do not resolve")
    print()
    return len(refs), len(misses)


def check_sections(files, rd):
    print("=" * 100)
    print("P2.  EVERY `section N` REFERENCE TO A run_all.sh RESOLVES, AND EVERY mg-ID AND")
    print("     SCRIPT NAMED ON THE REFERENCING LINE OCCURS IN THAT SECTION")
    print("=" * 100)
    runalls = {}
    for rel in files:
        if rel.endswith("run_all.sh"):
            body = rd(rel)
            secs = {}
            hits = list(_ECHOSEC.finditer(body))
            for i, m in enumerate(hits):
                end = hits[i + 1].start() if i + 1 < len(hits) else len(body)
                secs[m.group(1)] = (m.group(2), body[m.start():end])
            runalls[os.path.dirname(rel)] = secs
    print(f"  {len(runalls)} run_all.sh in the population; sections per file: "
          + ", ".join(f"{os.path.basename(d) or d}={len(s)}"
                      for d, s in sorted(runalls.items())))

    refs, quoted_secs = [], []
    for rel in files:
        if rel.endswith("run_all.sh"):
            continue
        d = os.path.dirname(rel)
        if d not in runalls:
            continue
        for ln, line in enumerate(rd(rel).split("\n"), 1):
            if not _RUNALL.search(line) and "re-run in section" not in line:
                continue
            for m in _SECTION.finditer(line):
                if reporting(rel):
                    note_suppressed(rel)
                    continue
                if _quoted(line, m.start()):
                    quoted_secs.append((rel, ln, m.group(0)))
                    continue
                refs.append((rel, ln, m.group(1), line.strip()))
    print(f"  population: {len(refs)} `section N` references to a run_all.sh, over the "
          f"{len([f for f in files if not f.endswith('run_all.sh')])} non-run_all.sh files "
          f"of the declared set.")
    print(f"  {len(quoted_secs)} further reference(s) SKIPPED as quotations:")
    for rel, ln, phrase in quoted_secs:
        print(f"         (quoted, not asserted) {rel}:{ln}  {phrase!r}")
    if not quoted_secs:
        print("         (none)")
    bad = 0
    for rel, ln, num, line in refs:
        secs = runalls[os.path.dirname(rel)]
        if num not in secs:
            report("P2", False, f"{rel}:{ln}", f"names section {num}",
                   f"run_all.sh has sections {', '.join(sorted(secs))}")
            bad += 1
            continue
        title, body = secs[num]
        tokens = sorted(set(_MGID.findall(line)) |
                        {s for s in _SCRIPT.findall(line) if s != "run_all.sh"})
        absent = [t for t in tokens if t not in body]
        ok = not absent
        report("P2", ok, f"{rel}:{ln}", f"names section {num} — \"{title[:64]}\"",
               (f"tokens on the line: {tokens or '(none)'}"
                + ("" if ok else f"\nNOT NAMED ANYWHERE IN SECTION {num}: {absent}")))
        if not ok:
            bad += 1
    print()
    return len(refs), bad


def check_tables(rd, files):
    print("=" * 100)
    print("P3.  EVERY PINNED TABLE OF delta_control.py KEYED BY REPO PATHS IS ITERATED BY")
    print("     THE INSTRUMENT.  A TABLE NOTHING VISITS IS A FAIL, NOT A SILENT PASS.")
    print("=" * 100)
    rel = "code/state_landing_control_2da3/delta_control.py"
    if rel not in files:
        print(f"  [FAIL] P3  {rel} is not in the population at this revision")
        _bad.append(("P3", rel, "not in the population"))
        print()
        return 0, 1
    tree = ast.parse(rd(rel))
    # The population: module-level dicts every key of which is a repo path.  DERIVED from
    # the file, so a third table added later joins the population by existing.
    tables = set()
    for node in tree.body:
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Dict):
            continue
        name = getattr(node.targets[0], "id", None)
        if name is None:
            continue
        keys = [k.value for k in node.value.keys
                if isinstance(k, ast.Constant) and isinstance(k.value, str)]
        if keys and all(re.match(r"^(code|docs)/", k) and "." in k for k in keys):
            tables.add(name)
    # Iterated: the table's name appears in the ITERABLE EXPRESSION of some `for`.  Derived
    # from the code, not from a hand list — the hand list this check started life as was its
    # own first defect, and is recorded as such in README.md.
    iterated = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.For):
            for sub in ast.walk(node.iter):
                if isinstance(sub, ast.Name):
                    iterated.add(sub.id)
    missed = sorted(tables - iterated)
    ok = not missed
    report("P3", ok, rel,
           f"pinned tables keyed by repo paths: {sorted(tables) or '(none)'}",
           f"of those, iterated by some `for` in this file: "
           f"{sorted(tables & iterated) or '(none)'}"
           + ("" if ok else
              f"\nNOT ITERATED BY ANYTHING: {missed}\n"
              ">>> a pinned table nothing visits cannot fail in the direction that would "
              "need visiting"))
    print()
    return len(tables), 0 if ok else 1


_WORD = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
         "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12}
_COUNT = re.compile(r"\ball (\d+|%s) rows\b" % "|".join(_WORD))


def _rows_in(rel, rd, files):
    """How many rows the script at `rel` runs, DERIVED from its own source.

    A module-level `ROWS = [...]` if it has one; otherwise the `ROWS` of the module it
    imports them from, resolved in the same directory.  Returns (count, where) or
    (None, why) — a count this function cannot derive is reported as underivable rather
    than guessed at, because a guessed denominator is the defect one directory over."""
    try:
        tree = ast.parse(rd(rel))
    except Exception as exc:                                   # noqa: BLE001
        return None, f"unparseable: {exc}"
    for node in tree.body:
        if (isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "ROWS"
                and isinstance(node.value, ast.List)):
            return len(node.value.elts), rel
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods |= {a.name for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module:
            mods.add(node.module)
    for mod in sorted(mods):
        cand = os.path.join(os.path.dirname(rel), mod + ".py")
        if cand in files:
            n, where = _rows_in(cand, rd, files)
            if n is not None:
                return n, where
    return None, "no module-level ROWS, and none in anything it imports"


def _quoted(line, col):
    """Is the character at `col` inside a "..." or `...` span on its own line?

    A claim inside quotation marks is a QUOTATION, not an assertion: an audit that writes
    `it runs against "all six rows"` is reporting another file's sentence, and checking that
    sentence against this file's code is a category error.  This exemption is declared, and
    every phrase it skips is printed, so it cannot quietly shrink the population."""
    for q in ('"', "`"):
        spans, i = [], 0
        while True:
            a = line.find(q, i)
            if a < 0:
                break
            b = line.find(q, a + 1)
            if b < 0:
                break
            spans.append((a, b))
            i = b + 1
        if any(a < col < b for a, b in spans):
            return True
    return False


def check_counts(files, rd):
    print("=" * 100)
    print("P4.  EVERY `all N rows` PHRASE NAMING A SCRIPT MATCHES THAT SCRIPT'S OWN ROWS")
    print("=" * 100)
    scripts = {os.path.basename(f): f for f in files if f.endswith(".py")}
    refs, quoted = [], []
    for rel in files:
        text = rd(rel)
        for m in _COUNT.finditer(text):
            raw = m.group(1)
            said = int(raw) if raw.isdigit() else _WORD[raw]
            if reporting(rel):
                note_suppressed(rel)
                continue
            bol = text.rfind("\n", 0, m.start()) + 1
            eol = text.find("\n", m.start())
            line = text[bol:eol if eol >= 0 else len(text)]
            if _quoted(line, m.start() - bol):
                quoted.append((rel, text[:m.start()].count("\n") + 1, m.group(0)))
                continue
            # The script the phrase is about: the nearest .py basename NAMED BEFORE it,
            # within 400 characters.  The window is printed with every row so a reader can
            # see what was and was not attributed.
            window = text[max(0, m.start() - 400):m.start()]
            named = [s for s in _SCRIPT.findall(window) if s in scripts]
            refs.append((rel, text[:m.start()].count("\n") + 1, said,
                         named[-1] if named else None))
    print(f"  population: {len(refs)} `all N rows` phrases over {len(files)} files.  The "
          f"script each is about is the nearest .py named in the 400 characters before it.")
    print(f"  {len(quoted)} further phrase(s) SKIPPED as quotations — inside \"...\" or "
          f"`...` on their own line:")
    for rel, ln, phrase in quoted:
        print(f"         (quoted, not asserted) {rel}:{ln}  {phrase!r}")
    if not quoted:
        print("         (none)")
    bad = 0
    for rel, ln, said, script in refs:
        if script is None:
            report("P4", False, f"{rel}:{ln}", f"says 'all {said} rows'",
                   "no script named within 400 characters before it — the phrase cannot be "
                   "attributed, so it is reported rather than passed")
            bad += 1
            continue
        got, where = _rows_in(scripts[script], rd, files)
        if got is None:
            report("P4", False, f"{rel}:{ln}", f"says '{script} … all {said} rows'",
                   f"could not derive a row count: {where}")
            bad += 1
            continue
        ok = got == said
        report("P4", ok, f"{rel}:{ln}", f"says '{script} … all {said} rows'",
               f"ROWS in {where}: {got}"
               + ("" if ok else "\n>>> the prose count is not the code's"))
        if not ok:
            bad += 1
    print()
    return len(refs), bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", default=None,
                    help="read the population from this revision instead of the tree")
    args = ap.parse_args()
    files, rd, exists = population(args.rev)

    print("=" * 100)
    print("mg-a74f — PROSE CLAIMS, READ AS CLAIMS")
    print("=" * 100)
    print(f"  revision    {args.rev or 'the working tree'}")
    print(f"  population  {len(files)} files: every .py, .md and .sh under")
    for d in DIRS:
        print(f"                  {d}/  "
              f"({len([f for f in files if f.startswith(d + '/')])} files)")
    print("  This checker's own directory is in the population, so it reads its own prose.")
    print()

    n1, b1 = check_paths(files, rd, exists)
    n2, b2 = check_sections(files, rd)
    n3, b3 = check_tables(rd, files)
    n4, b4 = check_counts(files, rd)

    print("=" * 100)
    print("THE EXEMPTION LIST, PRINTED — FILES WHOSE PROSE REPORTS ANOTHER FILE'S CLAIMS")
    print("=" * 100)
    print("  A checker that reads a REPORT of a defect as a fresh instance of it is")
    print("  measuring the wrong thing.  These files are excluded from P1, P2 and P4.  The")
    print("  list is fail-closed both ways: an entry naming a file outside the population is")
    print("  a FAIL, and an entry that suppresses nothing is a FAIL.")
    if args.rev:
        print(f"  NOT EVALUATED AT {args.rev}, with the reason rather than a bare `n/a`:")
        print("  these two files are this deliverable's own and did not exist at that")
        print("  revision, so 'the entry suppresses nothing' would be true of every entry")
        print("  and would say nothing about whether the list has rotted.  The list is")
        print("  fail-closed ON THE WORKING TREE, which is the tree it is a statement about;")
        print("  run this file with no --rev to see it evaluated.")
        for rel, why in sorted(REPORTS.items()):
            print(f"    (not evaluated) {rel}  — {why}")
    else:
        for rel, why in sorted(REPORTS.items()):
            n = _suppressed.get(rel, 0)
            here = rel in files
            ok = here and n > 0
            report("EX", ok, rel, why,
                   f"in the population: {here}; matches suppressed: {n}"
                   + ("" if ok else "\n>>> a stale exemption: it is not doing the job it "
                                    "claims, and an exemption nobody can see is the defect "
                                    "this deliverable exists to repair"))
    print()

    print("=" * 100)
    print("WHAT THIS RUN CHECKED, AND WHAT IT LEFT UNCHECKED")
    print("=" * 100)
    print(f"  P1  {n1:>3} path references                  {b1} do not resolve")
    print(f"  P2  {n2:>3} run_all.sh section references    {b2} unresolved, or naming "
          f"something the section does not")
    print(f"  P3  {n3:>3} pinned tables keyed by repo paths {b3} iterated by nothing")
    print(f"  P4  {n4:>3} `all N rows` phrases             {b4} disagreeing with the "
          f"script's own ROWS")
    print()
    print("  UNCHECKED, in the same files, by this program: every count that is not an")
    print("  `all N rows` phrase or a section number, every claim about what a reader is")
    print("  shown, every 'cannot', every 'measured over N', and every cross-reference")
    print("  that is not a path or a run_all.sh section number.  Those sentences are")
    print("  adjacent to checked ones and are not covered by this checker.  Naming that")
    print("  is the whole of what this program can honestly say about them.")
    print()
    print(f"  {len(_bad)} finding(s).")
    for pid, where, what in _bad:
        print(f"    {pid}  {where}  — {what}")
    print("=" * 100)
    return 1 if _bad else 0


if __name__ == "__main__":
    sys.exit(main())
