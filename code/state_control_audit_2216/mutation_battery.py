#!/usr/bin/env python3
"""mg-2216 — an INDEPENDENT mutation battery against mg-2da3's new working-tree control.

WHY THIS FILE EXISTS, AND WHY IT IS NOT `negative_control.py`.

`bf17716` (mg-2da3) repaired a blind control.  `b68db5d` had cited a revision-pinned
battery as certifying its own edits; mg-bd41 showed the battery could not fail; mg-2da3
built `code/state_landing_control_2da3/delta_control.py`, which reads the WORKING TREE,
and shipped `negative_control.py` to prove it fires.

That is the right shape.  But the deliverable of that ticket IS an instrument, and an
instrument whose only evidence of sensitivity is the negative control its own author
wrote is the defect being repaired, one level up: the author chooses the mutation, and a
control is guaranteed to catch the mutation it was tuned against.  mg-2da3's four
mutations are (NC1) the whole file gutted, (NC2) the certified row reverted wholesale,
(NC3) the certified README block deleted wholesale, (NC4) the certified row grown by a
sentence.  Three of the four are LARGE and OBVIOUS; the fourth is the aged-out path.

So this battery asks the question that one cannot: **what is the SMALLEST change to the
material `delta_control.py` claims to certify that it does not see?**  Fourteen mutations,
none of them mg-2da3's, grouped by class:

    single-character      one character of the certified cell, meaning-changing
    length-preserving     content replaced by content of identical length
    whitespace-only       no visible character changes at all
    reordering            token multiset preserved exactly
    bulk-but-quiet        thousands of characters destroyed under the tracked substrings
    out-of-row            damage elsewhere in the ledger
    readme-interior       the certified correction blocks hollowed from the inside
    tolerance             changes a key-based control SHOULD survive (control on the control)

Every mutation is applied to the working tree, `delta_control.py` is run as a subprocess,
and its exit code is read.  0 = did not see it.  1 = FAIL.  2 = MOVED.

Each mutation carries a VERDICT COLUMN stating what the instrument's own documented scope
implies it should do, so the report distinguishes "missed something it claims" from
"tolerated something it deliberately tolerates".  The tolerance mutations exist so that
this battery cannot be read as a demand for a stricter instrument in every direction:
some of what `delta_control.py` ignores, it ignores CORRECTLY and on the record.

SAFETY.  Identical discipline to the file it audits, independently written: both files are
snapshotted as bytes up front, restored in a `finally`, and re-verified by sha256 at the
end; the script REFUSES TO RUN if either file is already dirty in git.

INSTRUMENT DISCIPLINE.  Nothing shells out to `wc`.  Characters are `len(str)`, bytes are
`len(bytes)`, and every count names its unit.  No mutation is applied on top of another:
the tree is restored to its snapshot before each one.  Imports nothing from
`code/state_landing_control_2da3/`, `code/state_audit_6a2f/` or
`code/state_landing_audit_bd41/` — including the table parser, which is written here from
the file format rather than borrowed, so a parsing defect cannot be shared between the
instrument and its audit.
"""
import hashlib
import os
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()

STATE = os.path.join(REPO, "STATE.md")
README = os.path.join(REPO, "docs/state-history/README.md")
CONTROL = "code/state_landing_control_2da3/delta_control.py"
BATTERY = "code/state_audit_6a2f/run_all.sh"
BATTERY_OUT = os.path.join(REPO, "code/state_audit_6a2f/out_audit.txt")

ROW_KEY = "mg-276d"        # the row b68db5d edited (STATE.md:135 today)
OTHER_KEY = "mg-a3d4"      # the row holding the file's largest cell (:136 today)

NBSP = " "

# ---------------------------------------------------------------------------------------
# my own table parser, written from the format rather than borrowed
# ---------------------------------------------------------------------------------------


def cells_of(line):
    """The raw fields of a markdown table row, or None.

    A cell boundary is an unescaped '|'.  STATE.md writes literal pipes inside cells as
    '\\|', so a '|' preceded by a backslash is content, not a boundary.
    """
    if not line.startswith("|"):
        return None
    bars = []
    for i, ch in enumerate(line):
        if ch == "|" and (i == 0 or line[i - 1] != "\\"):
            bars.append(i)
    if len(bars) < 2:
        return None
    return [line[bars[k] + 1:bars[k + 1]] for k in range(len(bars) - 1)]


def row_line_index(text, key):
    """0-based index of the unique table line whose FIRST TWO fields carry `key`."""
    hits = []
    for i, line in enumerate(text.split("\n")):
        cs = cells_of(line)
        if cs and len(cs) >= 3 and any(key in c for c in cs[:2]):
            hits.append(i)
    if len(hits) != 1:
        raise SystemExit(f"key {key!r} matched {len(hits)} rows — refusing to guess")
    return hits[0]


def content_field(line):
    """(index, raw field) of the row's widest field — its content cell."""
    cs = cells_of(line)
    k = max(range(len(cs)), key=lambda i: len(cs[i]))
    return k, cs[k]


def rebuild(line, k, new_field):
    """Put `new_field` back as field k of `line`, leaving every other byte alone."""
    bars = [i for i, ch in enumerate(line)
            if ch == "|" and (i == 0 or line[i - 1] != "\\")]
    return line[:bars[k] + 1] + new_field + line[bars[k + 1]:]


def edit_cell(text, key, fn):
    """Apply `fn` to the STRIPPED content cell of row `key`, preserving the surrounding
    whitespace of the raw field exactly."""
    lines = text.split("\n")
    i = row_line_index(text, key)
    k, raw = content_field(lines[i])
    stripped = raw.strip()
    lead = raw[:len(raw) - len(raw.lstrip())]
    trail = raw[len(raw.rstrip()):]
    lines[i] = rebuild(lines[i], k, lead + fn(stripped) + trail)
    return "\n".join(lines)


def edit_raw_field(text, key, fn):
    """Apply `fn` to the RAW content field (whitespace included) of row `key`."""
    lines = text.split("\n")
    i = row_line_index(text, key)
    k, raw = content_field(lines[i])
    lines[i] = rebuild(lines[i], k, fn(raw))
    return "\n".join(lines)


def once(hay, needle, repl):
    """Replace `needle` exactly once, asserting it occurs exactly once."""
    n = hay.count(needle)
    if n != 1:
        raise SystemExit(f"expected 1 occurrence of {needle!r}, found {n}")
    return hay.replace(needle, repl, 1)


# ---------------------------------------------------------------------------------------
# the mutations
# ---------------------------------------------------------------------------------------
# Landmarks inside row :135's certified cell.  None of these is a string
# delta_control.py tracks; that is the point of choosing them.
MATH_CLAIM = "every ridge in 1 or 2 facets"
SOUNDNESS = "the proof is sound"
MATHS_HEAD = "**The mathematics.**"

# Landmarks inside the README correction blocks delta_control.py says it certifies.
F1_MARKER = "**`no 4d tally` is a correction, and `133` / `220` are its cost"
F2_FIGURE = "13,188 → 7,703 characters at the landing"
A1_FIGURE = "**175,552 to 37,958 bytes**"


def m_single_char(state, readme):
    """One character: a pseudomanifold's ridge multiplicity, 2 -> 3."""
    return edit_cell(state, ROW_KEY,
                     lambda c: once(c, MATH_CLAIM, "every ridge in 1 or 3 facets")), readme


def m_soundness(state, readme):
    """Five characters, same length: the row's verdict on its own proof, inverted."""
    return edit_cell(state, ROW_KEY,
                     lambda c: once(c, SOUNDNESS, "the proof is bogus")), readme


def m_nbsp(state, readme):
    """Whitespace only, and not even a length change: one ASCII space -> U+00A0.

    Same character count, different bytes, and the markdown no longer renders the
    heading as a heading.
    """
    return edit_cell(state, ROW_KEY,
                     lambda c: once(c, MATHS_HEAD,
                                    MATHS_HEAD.replace(" ", NBSP))), readme


def m_pad_field(state, readme):
    """Whitespace only, outside the stripped cell: 40 spaces before the closing pipe."""
    return edit_raw_field(state, ROW_KEY, lambda raw: raw.rstrip() + " " * 40), readme


def _swap_two_sentences(cell):
    """Swap two adjacent sentences of the cell, entirely after the F1 material.

    Length is preserved exactly and so is the whitespace-separated token multiset.
    """
    start = cell.find(MATHS_HEAD)
    if start < 0:
        raise SystemExit("could not locate the swap region")
    seg = cell[start:]
    parts = seg.split(". ")
    if len(parts) < 4:
        raise SystemExit("not enough sentences to swap")
    parts[1], parts[2] = parts[2], parts[1]
    return cell[:start] + ". ".join(parts)


def m_reorder(state, readme):
    """Reordering: token multiset and length both preserved exactly."""
    return edit_cell(state, ROW_KEY, _swap_two_sentences), readme


def _junk_tail(cell):
    """Replace the last 3,000 characters of the cell with 'x', preserving length and
    every '**' marker (so the parity invariant is untouched)."""
    head, tail = cell[:-3000], cell[-3000:]
    out = []
    i = 0
    while i < len(tail):
        if tail.startswith("**", i):
            out.append("**")
            i += 2
        else:
            out.append("x")
            i += 1
    return head + "".join(out)


def m_bulk_tail(state, readme):
    """38% of the certified cell destroyed, under the tracked substrings."""
    return edit_cell(state, ROW_KEY, _junk_tail), readme


def m_drop_pointer(state, readme):
    """Delete the row's pointer to its own per-row history file.

    Rule 2 of docs/state-history/README.md: "the row keeps a pointer naming it".
    """
    ptr = "*(Full per-row record — every passage relocated from this cell, verbatim:"
    return edit_cell(state, ROW_KEY,
                     lambda c: c[:c.find(ptr)].rstrip() if ptr in c
                     else (_ for _ in ()).throw(SystemExit("pointer not found"))), readme


def m_other_row(state, readme):
    """Delete a whole ledger row that is neither the certified one nor the largest."""
    lines = state.split("\n")
    i135 = row_line_index(state, ROW_KEY)
    i136 = row_line_index(state, OTHER_KEY)
    victim = None
    for i, line in enumerate(lines):
        cs = cells_of(line)
        if (cs and len(cs) == 3 and i not in (i135, i136)
                and len(max(cs, key=len).strip()) > 2000):
            victim = i
            break
    if victim is None:
        raise SystemExit("no victim row found")
    del lines[victim]
    return "\n".join(lines), readme


def m_readme_hollow(state, readme):
    """Hollow the certified F1 correction block: keep its first line, delete its body."""
    lines = readme.split("\n")
    start = next(i for i, l in enumerate(lines) if F1_MARKER in l)
    end = start + 1
    while end < len(lines) and lines[end].startswith(">"):
        end += 1
    return state, "\n".join(lines[:start + 1] + lines[end:])


def m_readme_figure(state, readme):
    """Falsify a measured figure inside the certified F2 correction block."""
    return state, once(readme, F2_FIGURE, "13,188 → 9,703 characters at the landing")


def m_readme_own_figure(state, readme):
    """Falsify the figure the repair's OWN A1 correction block rests on."""
    return state, once(readme, A1_FIGURE, "**175,552 to 137,958 bytes**")


# --- tolerance: things a key-based control SHOULD survive -------------------------------


def m_insert_above(state, readme):
    """60 lines inserted above the certified row (the author's stated design goal)."""
    lines = state.split("\n")
    i = row_line_index(state, ROW_KEY)
    return "\n".join(lines[:i - 1] + ["", "filler paragraph."] * 30 + lines[i - 1:]), readme


def m_move_row(state, readme):
    """The certified row moved to the end of the file, byte-identical."""
    lines = state.split("\n")
    i = row_line_index(state, ROW_KEY)
    row = lines.pop(i)
    return "\n".join(lines + ["", row]), readme


def m_duplicate_key(state, readme):
    """A second row carrying the same attempt id (an ambiguous key)."""
    lines = state.split("\n")
    i = row_line_index(state, ROW_KEY)
    return "\n".join(lines[:i + 1] + [lines[i]] + lines[i + 1:]), readme


MUTATIONS = [
    # name, class, expectation, one-line description, fn
    ("M01", "single-character", "catch",
     "row :135 cell: 'ridge in 1 or 2 facets' -> '1 or 3' (one character, a false theorem)",
     m_single_char),
    ("M02", "length-preserving", "catch",
     "row :135 cell: 'the proof is sound' -> 'the proof is bogus' (5 chars, verdict inverted)",
     m_soundness),
    ("M03", "whitespace-only", "catch",
     "row :135 cell: the spaces in '**The mathematics.**' -> U+00A0 (0 visible change)",
     m_nbsp),
    ("M04", "whitespace-only", "tolerate",
     "row :135 raw field: 40 trailing spaces before the closing pipe",
     m_pad_field),
    ("M05", "reordering", "catch",
     "row :135 cell: two adjacent sentences swapped (length AND token multiset preserved)",
     m_reorder),
    ("M06", "bulk-but-quiet", "catch",
     "row :135 cell: last 3,000 characters replaced by 'x' ('**' markers preserved)",
     m_bulk_tail),
    ("M07", "length-preserving", "catch",
     "row :135 cell: the per-row-history pointer deleted (violates the README's rule 2)",
     m_drop_pointer),
    ("M08", "out-of-row", "tolerate",
     "a different >2,000-character ledger row deleted outright",
     m_other_row),
    ("M09", "readme-interior", "catch",
     "README: the F1 correction block hollowed out, its first line kept",
     m_readme_hollow),
    ("M10", "readme-interior", "catch",
     "README: the F2 block's '13,188 -> 7,703 characters' falsified to 9,703",
     m_readme_figure),
    ("M11", "readme-interior", "catch",
     "README: the repair's OWN A1 block figure '37,958 bytes' falsified to 137,958",
     m_readme_own_figure),
    ("M12", "tolerance", "tolerate",
     "60 lines inserted above the certified row",
     m_insert_above),
    ("M13", "tolerance", "tolerate",
     "the certified row moved to the end of the file, byte-identical",
     m_move_row),
    ("M14", "tolerance", "catch",
     "the certified row duplicated (its key no longer identifies one row)",
     m_duplicate_key),
]


# ---------------------------------------------------------------------------------------
# harness
# ---------------------------------------------------------------------------------------


def sha(b):
    return hashlib.sha256(b).hexdigest()[:16]


def run_control():
    p = subprocess.run([sys.executable, CONTROL], cwd=REPO,
                       capture_output=True, text=True)
    out = p.stdout or ""
    fired = [l.strip() for l in out.split("\n")
             if l.strip().startswith(("[FAIL]", "[MOVED]"))]
    return p.returncode, fired


def run_battery():
    p = subprocess.run(["sh", BATTERY], cwd=REPO, capture_output=True)
    with open(BATTERY_OUT, "rb") as fh:
        committed = fh.read()
    return p.stdout == committed, len(p.stdout)


def verdict_of(expect, code):
    if expect == "catch":
        if code == 1:
            return "CAUGHT (FAIL)"
        if code == 2:
            return "CAUGHT (MOVED)"
        return ">>> MISSED <<<"
    if code == 0:
        return "tolerated, as designed"
    return f"NOISY (exit {code})"


def main():
    dirty = subprocess.run(
        ["git", "-C", REPO, "status", "--porcelain", "--",
         "STATE.md", "docs/state-history/README.md"],
        capture_output=True, text=True, check=True).stdout.strip()
    if dirty:
        sys.exit("REFUSING TO RUN: STATE.md / the state-history README are dirty.\n"
                 "This script mutates both and restores them; it will not restore a tree\n"
                 "to a state that was not committed.\n" + dirty)

    with open(STATE, "rb") as fh:
        state0 = fh.read()
    with open(README, "rb") as fh:
        readme0 = fh.read()
    s_text = state0.decode("utf-8")
    r_text = readme0.decode("utf-8")

    print("mg-2216 — INDEPENDENT mutation battery against mg-2da3's delta_control.py")
    print("=" * 86)
    print(f"STATE.md  at rest : {len(state0)} bytes, {len(s_text)} characters, "
          f"sha {sha(state0)}")
    print(f"README.md at rest : {len(readme0)} bytes, {len(r_text)} characters, "
          f"sha {sha(readme0)}")
    i135 = row_line_index(s_text, ROW_KEY)
    _, raw135 = content_field(s_text.split("\n")[i135])
    print(f"certified row     : line :{i135 + 1}, content cell {len(raw135.strip())} "
          f"characters stripped / {len(raw135)} raw")
    print(f"mutations         : {len(MUTATIONS)}, none of them mg-2da3's; each applied to "
          f"the snapshot, never stacked")
    print()

    print("POSITIVE CONTROL — clean tree")
    code, fired = run_control()
    print(f"  delta_control.py exit {code}   "
          f"{'as expected' if code == 0 else '>>> UNEXPECTED <<<'}")
    print()

    results = []
    try:
        for name, cls, expect, desc, fn in MUTATIONS:
            with open(STATE, "wb") as fh:
                fh.write(state0)
            with open(README, "wb") as fh:
                fh.write(readme0)
            new_state, new_readme = fn(s_text, r_text)
            with open(STATE, "w", encoding="utf-8") as fh:
                fh.write(new_state)
            with open(README, "w", encoding="utf-8") as fh:
                fh.write(new_readme)
            d_state = len(new_state) - len(s_text)
            d_readme = len(new_readme) - len(r_text)
            code, fired = run_control()
            v = verdict_of(expect, code)
            results.append((name, cls, expect, desc, code, v, fired, d_state, d_readme))
            print(f"{name}  [{cls}]  expect: {expect}")
            print(f"      {desc}")
            print(f"      character delta: STATE.md {d_state:+d}, README {d_readme:+d}")
            print(f"      delta_control.py exit {code}   {v}")
            for f in fired[:4]:
                print(f"        {f}")
            if len(fired) > 4:
                print(f"        ... and {len(fired) - 4} more ({len(fired)} in total)")
            print()

        # The independent re-confirmation of mg-bd41 A1, under a mutation that is not
        # mg-bd41's: the pinned battery is blind to a surgically damaged cell too.
        with open(STATE, "wb") as fh:
            fh.write(state0)
        with open(README, "wb") as fh:
            fh.write(readme0)
        new_state, _ = m_bulk_tail(s_text, r_text)
        with open(STATE, "w", encoding="utf-8") as fh:
            fh.write(new_state)
        print("=" * 86)
        print("THE PINNED BATTERY, UNDER M06 (not under mg-bd41's gutting)")
        print("=" * 86)
        same, got = run_battery()
        print(f"  code/state_audit_6a2f/run_all.sh reproduces out_audit.txt "
              f"byte-identically: {same} ({got} bytes)")
        print("  Same conclusion as mg-bd41 A1, reached from a different mutation: the")
        print("  battery is pinned to 97cb533 / 60f4dac / 57f962f and cannot see the tree.")
        print()
    finally:
        with open(STATE, "wb") as fh:
            fh.write(state0)
        with open(README, "wb") as fh:
            fh.write(readme0)

    with open(STATE, "rb") as fh:
        s1 = fh.read()
    with open(README, "rb") as fh:
        r1 = fh.read()
    assert s1 == state0, "RESTORE FAILED for STATE.md"
    assert r1 == readme0, "RESTORE FAILED for the state-history README"
    print("=" * 86)
    print(f"RESTORED — STATE.md sha {sha(s1)} == {sha(state0)}, "
          f"README sha {sha(r1)} == {sha(readme0)}")

    print("=" * 86)
    print("SUMMARY")
    print("=" * 86)
    print(f"  {'':<5}{'class':<20}{'expect':<11}{'exit':<6}verdict")
    for name, cls, expect, desc, code, v, fired, ds, dr in results:
        print(f"  {name:<5}{cls:<20}{expect:<11}{code:<6}{v}")
    missed = [r for r in results if r[5].startswith(">>>")]
    noisy = [r for r in results if r[5].startswith("NOISY")]
    print()
    print(f"  {len(results)} mutations: "
          f"{len([r for r in results if r[5].startswith('CAUGHT')])} caught, "
          f"{len(missed)} MISSED, "
          f"{len([r for r in results if r[5].startswith('tolerated')])} tolerated by design, "
          f"{len(noisy)} noisy")
    if missed:
        print()
        print("  MISSED — damage to material delta_control.py states it certifies, on which")
        print("  it exits 0:")
        for name, cls, expect, desc, code, v, fired, ds, dr in missed:
            print(f"    {name} [{cls}] {desc}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
