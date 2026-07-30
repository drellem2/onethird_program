#!/usr/bin/env python3
"""mg-2da3 — a WORKING-TREE control for b68db5d's delta (mg-7735's landing).

WHY THIS EXISTS.  b68db5d's headline evidence sentence is

    "I re-ran both: `sh code/state_audit_6a2f/run_all.sh` reproduces out_audit.txt
     BYTE-IDENTICALLY with these edits applied."

Every script in that battery pins fixed revisions (97cb533 / 60f4dac / 57f962f) and reads
the committed docs/state-history/*.md at 57f962f.  Not one of them opens the working tree
or resolves HEAD.  So the sentence is TRUE and carries NO INFORMATION about the edits:
mg-bd41 gutted STATE.md from 175,552 to 37,958 bytes and the battery still emitted the
identical 96,291 bytes.  The battery is not wrong — reproducing an audit of a specific
historical state is exactly what mg-6a2f built it to do, and pinning is a FEATURE there.
What was wrong was re-running it in a later commit and describing the result as certifying
that commit's own new edits.

THIS FILE IS THE MISSING INSTRUMENT, NOT A REPLACEMENT FOR THAT ONE.  It reads the
WORKING TREE for everything it certifies.  `b68db5d^` appears only as the BEFORE side of a
measured delta, which is what a baseline is for.  Run negative_control.py to see it fail.

WHAT IT CERTIFIES — the two files b68db5d changed:

    STATE.md                       row :135, the F1 repair (one line, +173 characters)
    docs/state-history/README.md   the F1 / F2 / B1 correction blocks

HOW IT LOCATES THINGS, and this is deliberate.  Every check keys on CONTENT — the ledger
row is found by its attempt id, the cell by being the row's widest — never by line number
and never by a frozen blob comparison.  The scope mismatch this arc keeps hitting (mg-6a2f
F1: "a claim about a cell, checked against a clause") is what line-anchored checking buys
you.  A key-based check also survives legitimate later commits that insert lines above the
row, so this instrument does not age out the way a line-pinned one would.

EXIT CODES, both non-zero on failure and distinguishable on purpose:

    0   every check passed
    1   FAIL   — a certification check failed.  b68db5d's repair is damaged in the tree.
    2   MOVED  — the repair is intact but a measured constant of the landing has changed,
                 i.e. row :135 or the README index was legitimately edited after b68db5d.
                 That is not a defect; it means this instrument must be re-baselined and
                 the new figure recorded.  It exits non-zero so it CANNOT go on quietly
                 reporting green about a delta that is no longer the delta it was written
                 for — which is the whole failure this file was filed against.

INSTRUMENT DISCIPLINE (this arc has been bitten by all three):
  * `wc -m` counts BYTES on this box (LC_CTYPE=C) and agrees with `wc -c`, so cross-checking
    the two reads as confirmation while both are wrong.  Nothing here shells out to wc:
    characters are len(str), bytes are len(bytes).
  * Every figure names its UNIT and, for cells, its CONVENTION.  b68db5d's message measures
    cells STRIPPED (7,703 -> 7,876); the README index measures them RAW, i.e. including the
    space either side of the boundary pipe (7,705 -> 7,878).  Both are printed, both are
    labelled, and the split is REPORTED not silently reconciled — it is mg-bd41's A4, a
    MINOR finding outside this ticket's brief, and it stays open.
  * Every tally is over UNBOUNDED input.  No head/tail/sed -n/--limit anywhere; each count
    prints the population it was taken over.

Imports nothing from code/state_restructure_34bf/, code/state_audit_6a2f/ or
code/state_landing_audit_bd41/.
"""
import os
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()

BASELINE = "b68db5d^"          # the BEFORE side of the delta.  Never the certified side.
LANDING = "b68db5d"            # named in prose only; nothing here reads it as evidence.

ROW_KEY = "mg-276d"            # the attempt id of the row b68db5d edited (STATE.md:135)
BIGGEST_KEY = "mg-a3d4"        # the row holding the largest cell in the file (:136)

# --- the measured constants of the landing, from b68db5d's own SCOPE paragraph -----------
CELL_AFTER_STRIPPED = 7876
CELL_BEFORE_STRIPPED = 7703
CELL_DELTA = 173
BIGGEST_STRIPPED = 8440
GAP_CHARS = 399                # counterexample -> F1 sentence, inside row :135's cell
GAP_WORDS = 72

# --- the text the F1 repair put in the tree ----------------------------------------------
F1_NARROW = "This row states no 4d *tally* of its own"
F1_ABSOLUTE_QUOTED = 'mg-34bf wrote that as an absolute *"states no count of its own"*'
F1_ATTRIBUTION = "mg-6a2f F1, narrowed to the true claim by mg-7735"
F1_COUNTEREXAMPLE = "five previous rows"
F1_OLD_ABSOLUTE = "This row states no count of its own"

README = "docs/state-history/README.md"
README_MARKERS = [
    ("F2 correction block",
     "**THOSE FIVE FIGURES WERE WRONG, here and in `57f962f`'s commit message"),
    ("F2 names the frozen message as still carrying it",
     "`57f962f`'s commit message is frozen and still carries its list"),
    ("F1 correction block",
     "**`no 4d tally` is a correction, and `133` / `220` are its cost"),
    ("B1 attribution correction",
     "**Two corrections to this bullet, from mg-6a2f §B1, made by mg-7735.**"),
    ("index note carries the moved cell figure",
     "mg-7735's F1 correction took row `:135`'s to **7,878**"),
]

FAIL, MOVED = 1, 2
_seen = {FAIL: 0, MOVED: 0}


def exit_code():
    """FAIL outranks MOVED: a damaged repair is the more serious report, and a
    non-zero code is produced by either."""
    if _seen[FAIL]:
        return FAIL
    if _seen[MOVED]:
        return MOVED
    return 0


def blob(rev, path):
    """Bytes of `path` at `rev`.  Baselines only — never the certified side."""
    return subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"],
                          capture_output=True, check=True).stdout


def tree(path):
    """Bytes of `path` in the WORKING TREE.  This is what the instrument certifies."""
    with open(os.path.join(REPO, path), "rb") as fh:
        return fh.read()


def split_row(line):
    """Escape-aware markdown table split.

    Literal pipes inside STATE.md cells are written `\\|`, so a cell boundary is a '|'
    NOT preceded by a backslash.  Returns the RAW fragments between boundary pipes
    (leading/trailing space intact), or None if the line is not a table row.
    """
    bounds = [i for i, ch in enumerate(line)
              if ch == "|" and (i == 0 or line[i - 1] != "\\")]
    if len(bounds) < 2 or bounds[0] != 0:
        return None
    return [line[bounds[i] + 1:bounds[i + 1]] for i in range(len(bounds) - 1)]


def all_rows(text):
    """(1-indexed line number, raw cell list) for every table row in `text`."""
    out = []
    for n, line in enumerate(text.split("\n"), start=1):
        if line.startswith("|"):
            cells = split_row(line)
            if cells:
                out.append((n, cells))
    return out


def find_row(text, key):
    """The unique ledger row carrying `key` in one of its first two columns.

    Columns 1 and 2 (verdict, attempt) are what mg-34bf's restructure left untouched —
    "which is also what makes the completeness check's row key stable", in the README's
    words — and b68db5d changed neither.  So they are the stable key, and the third
    (content) column, which is the thing being certified, is deliberately not searched.
    """
    hits = [(n, cells) for n, cells in all_rows(text)
            if len(cells) >= 3 and any(key in c for c in cells[:2])]
    return hits


def widest(cells):
    """The row's CONTENT cell: its widest.  Returned raw; strip at the call site.

    'The third column' is not portable — STATE.md holds tables of different arities.
    """
    return max(cells, key=len)


def check(label, ok, detail="", kind=FAIL):
    verdict = "pass" if ok else ("FAIL" if kind == FAIL else "MOVED")
    print(f"  [{verdict}] {label}")
    if detail:
        print(f"         {detail}")
    if not ok:
        _seen[kind] += 1
    return ok


def main():
    print("mg-2da3 — working-tree control for b68db5d's delta")
    print(f"certified side  : the WORKING TREE (STATE.md, {README})")
    print(f"baseline side   : {BASELINE}  — used ONLY as the BEFORE of a measured delta")
    print()

    state_tree_b = tree("STATE.md")
    state_tree = state_tree_b.decode("utf-8")
    state_base = blob(BASELINE, "STATE.md").decode("utf-8")
    readme_tree = tree(README).decode("utf-8")

    lines_tree = state_tree.split("\n")
    print(f"STATE.md in the working tree: {len(state_tree_b)} bytes, "
          f"{len(state_tree)} characters, "
          f"{len(lines_tree) - (1 if lines_tree[-1] == '' else 0)} lines")
    rows_tree = all_rows(state_tree)
    cells_tree = [c for _, cells in rows_tree for c in cells]
    print(f"                             {len(rows_tree)} table rows, "
          f"{len(cells_tree)} cells (the population every whole-file tally below is over)")
    print()

    # ---- 1. locate the row b68db5d edited, by key, in the tree ---------------------------
    print("1. THE ROW b68db5d EDITED, located by attempt id (not by line number)")
    hits = find_row(state_tree, ROW_KEY)
    if not check(f"exactly one ledger row keys to {ROW_KEY} in the working tree",
                 len(hits) == 1, f"found {len(hits)}"):
        print()
        print("=" * 78)
        print("RESULT: FAIL (exit 1) — the row b68db5d edited is not identifiable in the")
        print("        working tree at all, so nothing below it can be certified.")
        print("=" * 78)
        return FAIL
    row_line, row_cells = hits[0]
    cell_raw = widest(row_cells)
    cell = cell_raw.strip()
    check("it is a three-column row", len(row_cells) == 3, f"columns: {len(row_cells)}")
    print(f"         at line :{row_line} in this tree "
          f"(observed, not asserted — the check above is key-based)")
    print()

    base_hits = find_row(state_base, ROW_KEY)
    if not check(f"the same key locates exactly one row at {BASELINE}",
                 len(base_hits) == 1, f"found {len(base_hits)}"):
        print()
        print("=" * 78)
        print(f"RESULT: FAIL (exit 1) — no baseline row at {BASELINE} to measure against.")
        print("=" * 78)
        return FAIL
    base_cell_raw = widest(base_hits[0][1])
    base_cell = base_cell_raw.strip()

    # ---- 2. the F1 repair itself --------------------------------------------------------
    print("2. THE F1 REPAIR — present in the tree, absent at the baseline")
    check("tree row states the NARROW claim", F1_NARROW in cell,
          f'"{F1_NARROW}"')
    check("tree row QUOTES the false absolute it replaced", F1_ABSOLUTE_QUOTED in cell)
    check("tree row ATTRIBUTES the correction", F1_ATTRIBUTION in cell)
    check("baseline row carried the bare absolute", F1_OLD_ABSOLUTE in base_cell)
    check("baseline row did NOT carry the narrow claim", F1_NARROW not in base_cell)
    print()

    # ---- 3. the counterexample the repair exists because of ------------------------------
    print("3. THE COUNTEREXAMPLE THAT MADE THE ABSOLUTE FALSE — still in the cell,")
    print("   and still EARLIER in it than the sentence that used to deny it")
    i = cell.find(F1_COUNTEREXAMPLE)
    j = cell.find(F1_NARROW)
    if check(f'the cell still opens on "{F1_COUNTEREXAMPLE}"', i >= 0):
        check("it precedes the F1 sentence", 0 <= i < j,
              f"counterexample at char {i}, F1 sentence at char {j}")
        gap = cell[i:j]
        check(f"the gap is {GAP_CHARS} characters", len(gap) == GAP_CHARS,
              f"measured {len(gap)} characters "
              f"(from the start of the phrase to the start of the sentence)",
              kind=MOVED)
        check(f"the gap is {GAP_WORDS} words", len(gap.split()) == GAP_WORDS,
              f"measured {len(gap.split())} whitespace-separated words", kind=MOVED)
    print()

    # ---- 4. the measured delta ----------------------------------------------------------
    print("4. THE MEASURED DELTA — tree against baseline, both conventions printed")
    print(f"         stripped: {len(base_cell)} -> {len(cell)} characters")
    print(f"         raw     : {len(base_cell_raw)} -> {len(cell_raw)} characters "
          f"(raw = including the space either side of the boundary pipe)")
    print(f"         bytes   : {len(base_cell.encode())} -> {len(cell.encode())} "
          f"(stripped convention)")
    check(f"baseline cell is {CELL_BEFORE_STRIPPED} characters (stripped)",
          len(base_cell) == CELL_BEFORE_STRIPPED, f"measured {len(base_cell)}", kind=MOVED)
    check(f"tree cell is {CELL_AFTER_STRIPPED} characters (stripped)",
          len(cell) == CELL_AFTER_STRIPPED, f"measured {len(cell)}", kind=MOVED)
    check(f"the delta is +{CELL_DELTA} characters",
          len(cell) - len(base_cell) == CELL_DELTA,
          f"measured {len(cell) - len(base_cell):+d}", kind=MOVED)
    print()

    # ---- 5. whole-file invariants b68db5d claims, measured on the TREE -------------------
    print("5. WHOLE-FILE INVARIANTS, measured on the working tree")
    odd = [(n, k) for n, cells in rows_tree for k, c in enumerate(cells)
           if c.count("**") % 2]
    check("** parity is even in every cell",
          not odd,
          f"over all {len(cells_tree)} cells; "
          + (f"odd at {odd}" if odd else "0 odd"))

    big_hits = find_row(state_tree, BIGGEST_KEY)
    if check(f"exactly one ledger row keys to {BIGGEST_KEY}", len(big_hits) == 1,
             f"found {len(big_hits)}"):
        big_cell = widest(big_hits[0][1]).strip()
        largest = max(cells_tree, key=lambda c: len(c.strip()))
        check(f"the {BIGGEST_KEY} row still holds the largest cell in the file",
              largest.strip() == big_cell,
              f"largest cell is {len(largest.strip())} characters (stripped), "
              f"over all {len(cells_tree)} cells")
        check(f"and it is still {BIGGEST_STRIPPED} characters (stripped)",
              len(big_cell) == BIGGEST_STRIPPED, f"measured {len(big_cell)}", kind=MOVED)
        check("the edited row is still smaller than it",
              len(cell) < len(big_cell), f"{len(cell)} < {len(big_cell)}")
    print()

    # ---- 6. the README half of the delta -------------------------------------------------
    print(f"6. {README} — the correction blocks b68db5d added, in the tree")
    print(f"         {len(readme_tree.encode())} bytes, {len(readme_tree)} characters, "
          f"{len(readme_tree.split(chr(10)))} lines")
    for label, marker in README_MARKERS:
        check(label, marker in readme_tree,
              "" if marker in readme_tree else f"missing: {marker!r}")
    print()

    worst = exit_code()
    print("=" * 78)
    if worst == 0:
        print("RESULT: PASS — every check above read the working tree and every one held.")
        print("        This instrument CAN fail; negative_control.py makes it fail.")
    elif worst == MOVED:
        print("RESULT: MOVED (exit 2) — the F1 repair is intact, but a measured constant")
        print("        of the landing has changed.  Row :135 or the README index was")
        print("        edited after b68db5d.  That is not necessarily a defect: RE-BASELINE")
        print("        this instrument, record the new figure, and say which commit moved")
        print("        it.  It exits non-zero rather than quietly reporting green about a")
        print("        delta that is no longer the delta it was written for.")
    else:
        print("RESULT: FAIL (exit 1) — b68db5d's repair is DAMAGED in the working tree.")
        if _seen[MOVED]:
            print(f"        ({_seen[FAIL]} FAIL, {_seen[MOVED]} MOVED; FAIL is reported"
                  " because it is the more serious of the two.)")
    print("=" * 78)
    return worst


if __name__ == "__main__":
    sys.exit(main())
