#!/usr/bin/env python3
"""mg-2da3 — PROVE delta_control.py can fail, and show the pinned battery cannot.

A reproduction is only evidence if the instrument could have failed.  b68db5d's headline
sentence cited a battery that could not, so this file does for the new instrument what
mg-bd41 did to the old one: mutilate the working tree, re-run, and read the exit code.

    WHAT THIS FILE IS AND IS NOT (mg-7870).  mg-2216 showed that this file was the reason
    the instrument's blindness went unseen: NC3 cuts the certified README block INCLUDING
    its header, and the header was the only thing the check tested, so the one mutation the
    author chose was precisely the mutation the check was shaped around.  Eight of mg-2216's
    fourteen independent mutations exited 0.

    So the standing rule for this file is now explicit: IT DEMONSTRATES, IT DOES NOT
    ESTABLISH.  An author's own negative control cannot establish that an instrument is
    sensitive, because the author picks the mutations.  The establishing evidence for the
    digest repair is mg-2216's battery — written before the repair, by someone else, with
    its own table parser — RE-RUN against the repaired instrument and captured verbatim at
    code/state_landing_control_2da3/out_battery_2216_rerun.txt: 14 mutations, 10 caught,
    0 MISSED, 4 tolerated by design, 0 noisy.  Read that file, not this one, for whether
    the control works.  NC5 and NC6 below exist to show the MECHANISM firing in-place; they
    are deliberately not chosen from mg-2216's list.

SIX MUTATIONS, weakest last:

  NC1  THE SAME GUTTING mg-bd41 USED — STATE.md's lines 101-300 deleted outright and line
       1 replaced with "TOTALLY DESTROYED", 175,552 -> ~38,000 bytes.  Under this exact
       mutation the mg-6a2f battery reproduces out_audit.txt BYTE-IDENTICALLY.  The new
       instrument must not.  Both are run here, side by side, because the contrast IS the
       finding: two instruments, one destroyed tree, opposite verdicts.

  NC2  ROW :135 REVERTED TO b68db5d^ — the sharpest control there is, because it undoes
       exactly the edit being certified and nothing else.  A control that survives NC1 by
       accident (any large mutation breaks any parser) still has to fail this one.

  NC3  THE F1 CORRECTION BLOCK CUT OUT OF docs/state-history/README.md — the other half of
       the delta.  STATE.md is untouched, so this isolates the README half.  NOTE, because
       it is the whole of mg-2216's B1: this cut takes the block's HEADER with it, and the
       pre-repair instrument tested only headers.  It is kept here unchanged as the record
       of how a negative control can be satisfied by the mutation it was shaped around.

  NC5  ONE CHARACTER INSIDE A CERTIFIED README REGION, length-preserving: the index note's
       moved-cell figure **7,878** -> **7,879**.  No header touched, no block deleted, no
       length changed — the class of mutation the header-substring check could not see and
       the digest cannot miss.  Expected MOVED (2): the F1 repair's sentences are all
       intact, and only the region's bytes have changed.

  NC6  500 CHARACTERS INSIDE THE CERTIFIED LEDGER CELL, length-preserving: the LETTERS of
       the cell's last 500 characters sorted among the positions letters already occupied.
       Character count, byte count, character multiset and the '**' parity invariant are
       all preserved exactly; the prose is destroyed.  Everything else in the instrument is
       satisfied, so the region digest is the only thing that can fire.  Expected MOVED (2),
       for the same reason as NC5.

SAFETY.  Both files are snapshotted as bytes before anything is written, restored in a
`finally`, and re-checked by sha256 afterwards.  The script REFUSES TO RUN if either file
is already dirty, so it can never restore a working tree to the wrong state.
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

F1_BLOCK_MARKER = "**`no 4d tally` is a correction, and `133` / `220` are its cost"

# NC5's target: a certified README region, mutated by exactly one character.
INDEX_FIGURE = "took row `:135`'s to **7,878**"
INDEX_FIGURE_FALSE = "took row `:135`'s to **7,879**"


def sha(b):
    return hashlib.sha256(b).hexdigest()[:16]


def run_control():
    """Run the new instrument; return (exit code, its RESULT line)."""
    p = subprocess.run([sys.executable, CONTROL], cwd=REPO,
                       capture_output=True, text=True)
    result = [l for l in (p.stdout or "").split("\n") if l.startswith("RESULT:")]
    fails = [l.strip() for l in (p.stdout or "").split("\n")
             if l.strip().startswith(("[FAIL]", "[MOVED]"))]
    return p.returncode, (result[0] if result else "(no RESULT line)"), fails


def run_battery():
    """Run the revision-pinned mg-6a2f battery; return True iff it reproduces its
    committed output byte for byte."""
    p = subprocess.run(["sh", BATTERY], cwd=REPO, capture_output=True)
    with open(BATTERY_OUT, "rb") as fh:
        committed = fh.read()
    return p.stdout == committed, len(p.stdout), len(committed)


def split_row(line):
    bounds = [i for i, ch in enumerate(line)
              if ch == "|" and (i == 0 or line[i - 1] != "\\")]
    if len(bounds) < 2 or bounds[0] != 0:
        return None
    return [line[bounds[i] + 1:bounds[i + 1]] for i in range(len(bounds) - 1)]


def row_index(text, key):
    """0-based index of the unique line whose first two table columns carry `key`."""
    hits = []
    for i, line in enumerate(text.split("\n")):
        if not line.startswith("|"):
            continue
        cells = split_row(line)
        if cells and len(cells) >= 3 and any(key in c for c in cells[:2]):
            hits.append(i)
    assert len(hits) == 1, f"key {key!r} matched {len(hits)} rows"
    return hits[0]


def scramble_cell_tail(text, key, n):
    """Sort the LETTERS of the last `n` characters of row `key`'s content cell, in place.

    Only alphabetic characters move, and they move only among the positions alphabetic
    characters already occupied: every '*', every backtick, every space and every digit
    stays exactly where it was.  So length, byte count, character multiset AND the '**'
    parity invariant of section 6 are all preserved, which is the point — the only thing
    left that can fire is the region digest.  Returns (new text, stripped length before,
    stripped length after); the two lengths are printed so the reader can see the mutation
    is length-preserving rather than being told so.
    """
    lines = text.split("\n")
    i = row_index(text, key)
    bars = [k for k, ch in enumerate(lines[i])
            if ch == "|" and (k == 0 or lines[i][k - 1] != "\\")]
    cells = [lines[i][bars[k] + 1:bars[k + 1]] for k in range(len(bars) - 1)]
    k = max(range(len(cells)), key=lambda x: len(cells[x]))
    raw = cells[k]
    stripped = raw.strip(" \t\r\n")
    lead = raw[:len(raw) - len(raw.lstrip(" \t\r\n"))]
    trail = raw[len(raw.rstrip(" \t\r\n")):]
    tail = stripped[-n:]
    letters = iter(sorted(c for c in tail if c.isalpha()))
    new = stripped[:-n] + "".join(next(letters) if c.isalpha() else c for c in tail)
    assert len(new) == len(stripped), "NC6 is not length-preserving"
    assert sorted(new) == sorted(stripped), "NC6 does not preserve the character multiset"
    assert new.count("**") == stripped.count("**"), "NC6 disturbs the ** parity invariant"
    lines[i] = lines[i][:bars[k] + 1] + lead + new + trail + lines[i][bars[k + 1]:]
    return "\n".join(lines), len(stripped), len(new)


CODES = {}


def report(name, code, result, fails, expect_zero=False, tag=None):
    CODES[tag or name.strip()] = code
    if expect_zero:
        verdict = "as expected" if code == 0 else ">>> UNEXPECTED FAILURE <<<"
    else:
        verdict = "CONTROL FIRES" if code != 0 else ">>> CONTROL DOES NOT FIRE <<<"
    print(f"  {name}: exit {code}   {verdict}")
    print(f"      {result}")
    for f in fails[:6]:
        print(f"      {f}")
    if len(fails) > 6:
        print(f"      ... and {len(fails) - 6} more failing checks "
              f"({len(fails)} in total)")


def main():
    dirty = subprocess.run(
        ["git", "-C", REPO, "status", "--porcelain", "--",
         "STATE.md", "docs/state-history/README.md"],
        capture_output=True, text=True, check=True).stdout.strip()
    if dirty:
        sys.exit("REFUSING TO RUN: STATE.md / the state-history README are dirty.\n"
                 "Commit or restore them first — this script mutates them.\n" + dirty)

    with open(STATE, "rb") as fh:
        state0 = fh.read()
    with open(README, "rb") as fh:
        readme0 = fh.read()
    print(f"STATE.md  at rest: {len(state0)} bytes, sha {sha(state0)}")
    print(f"README.md at rest: {len(readme0)} bytes, sha {sha(readme0)}")
    print()

    print("=" * 78)
    print("POSITIVE CONTROL — clean tree")
    print("=" * 78)
    report("delta_control.py    ", *run_control(), expect_zero=True, tag="clean")
    same, got, want = run_battery()
    print(f"  mg-6a2f battery     : reproduces out_audit.txt byte-identically: {same} "
          f"({got} bytes vs {want} committed)")
    print()

    try:
        # ---- NC1 -------------------------------------------------------------------
        text = state0.decode("utf-8")
        ls = text.split("\n")
        gutted = list(ls)
        del gutted[100:300]
        gutted[0] = "TOTALLY DESTROYED"
        with open(STATE, "w", encoding="utf-8") as fh:
            fh.write("\n".join(gutted))
        with open(STATE, "rb") as fh:
            now = fh.read()
        print("=" * 78)
        print("NC1 — STATE.md GUTTED (mg-bd41's mutation, reproduced exactly)")
        print(f"      {len(state0)} -> {len(now)} bytes, "
              f"{len(ls)} -> {len(gutted)} lines (200 deleted, line 1 replaced)")
        print("=" * 78)
        report("delta_control.py    ", *run_control(), tag="NC1")
        same, got, want = run_battery()
        print(f"  mg-6a2f battery     : reproduces out_audit.txt byte-identically: {same} "
              f"({got} bytes vs {want} committed)")
        if same:
            print("      ^ THE CONTRAST.  Same destroyed tree.  The revision-pinned battery")
            print("        is unmoved because it reads 97cb533 / 60f4dac / 57f962f and never")
            print("        the tree — correct for reproducing mg-6a2f's historical audit,")
            print("        and worthless as evidence about any later commit's edits.")
        print()

        # ---- NC2 -------------------------------------------------------------------
        with open(STATE, "wb") as fh:
            fh.write(state0)
        base = subprocess.run(["git", "-C", REPO, "show", "b68db5d^:STATE.md"],
                              capture_output=True, check=True).stdout.decode("utf-8")
        i_tree = row_index(text, "mg-276d")
        i_base = row_index(base, "mg-276d")
        reverted = list(ls)
        reverted[i_tree] = base.split("\n")[i_base]
        with open(STATE, "w", encoding="utf-8") as fh:
            fh.write("\n".join(reverted))
        print("=" * 78)
        print("NC2 — ROW :135 REVERTED TO b68db5d^ (only the certified edit is undone)")
        print(f"      line {i_tree + 1}: {len(ls[i_tree])} -> "
              f"{len(reverted[i_tree])} characters; every other line untouched")
        print("=" * 78)
        report("delta_control.py    ", *run_control(), tag="NC2")
        print()

        # ---- NC3 -------------------------------------------------------------------
        with open(STATE, "wb") as fh:
            fh.write(state0)
        rtext = readme0.decode("utf-8")
        rlines = rtext.split("\n")
        start = next(i for i, l in enumerate(rlines) if F1_BLOCK_MARKER in l)
        end = start
        while end < len(rlines) and (rlines[end].startswith(">") or rlines[end] == ">"):
            end += 1
        # walk back to the start of the blockquote
        while start > 0 and rlines[start - 1].startswith(">"):
            start -= 1
        cut = rlines[:start] + rlines[end:]
        with open(README, "w", encoding="utf-8") as fh:
            fh.write("\n".join(cut))
        print("=" * 78)
        print("NC3 — THE F1 CORRECTION BLOCK CUT OUT OF THE README (STATE.md intact)")
        print(f"      {len(rlines)} -> {len(cut)} lines "
              f"(blockquote lines {start + 1}-{end} removed)")
        print("=" * 78)
        report("delta_control.py    ", *run_control(), tag="NC3")
        print()

        # ---- NC4 -------------------------------------------------------------------
        with open(README, "wb") as fh:
            fh.write(readme0)
        grown = list(ls)
        grown[i_tree] = grown[i_tree].rstrip()[:-1].rstrip() + " AND ONE MORE WORD. |"
        with open(STATE, "w", encoding="utf-8") as fh:
            fh.write("\n".join(grown))
        print("=" * 78)
        print("NC4 — ROW :135 LEGITIMATELY EDITED (the F1 repair left intact, the cell")
        print("      grown by a sentence).  This is the AGED-OUT path, not a damaged one:")
        print("      the instrument must report MOVED and still exit NON-ZERO, so it can")
        print("      never go on reporting green about a delta that has changed under it.")
        print(f"      line {i_tree + 1}: {len(ls[i_tree])} -> "
              f"{len(grown[i_tree])} characters")
        print("=" * 78)
        report("delta_control.py    ", *run_control(), tag="NC4")
        print()

        # ---- NC5 -------------------------------------------------------------------
        with open(STATE, "wb") as fh:
            fh.write(state0)
        assert rtext.count(INDEX_FIGURE) == 1, "index figure is not unique"
        with open(README, "w", encoding="utf-8") as fh:
            fh.write(rtext.replace(INDEX_FIGURE, INDEX_FIGURE_FALSE, 1))
        print("=" * 78)
        print("NC5 — ONE CHARACTER FALSIFIED INSIDE A CERTIFIED README REGION")
        print(f"      {INDEX_FIGURE!r} -> {INDEX_FIGURE_FALSE!r}: length-preserving, no")
        print("      header touched, no block deleted.  This is the class the pre-repair")
        print("      header-substring check could not see.")
        print("=" * 78)
        report("delta_control.py    ", *run_control(), tag="NC5")
        print()

        # ---- NC6 -------------------------------------------------------------------
        with open(README, "wb") as fh:
            fh.write(readme0)
        scrambled, before, after = scramble_cell_tail(text, "mg-276d", 500)
        with open(STATE, "w", encoding="utf-8") as fh:
            fh.write(scrambled)
        print("=" * 78)
        print("NC6 — 500 CHARACTERS OF THE CERTIFIED CELL SORTED IN PLACE")
        print(f"      cell {before} -> {after} characters (stripped): identical count,")
        print("      identical character multiset, prose destroyed.  Length-and-substring")
        print("      checking is transparent to this; a digest is not.")
        print("=" * 78)
        report("delta_control.py    ", *run_control(), tag="NC6")
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
    assert r1 == readme0, "RESTORE FAILED for the README"
    print("=" * 78)
    print(f"RESTORED — STATE.md sha {sha(s1)} == {sha(state0)}, "
          f"README sha {sha(r1)} == {sha(readme0)}")
    print("=" * 78)
    want_by_tag = {"clean": (0,), "NC1": (1,), "NC2": (1,), "NC3": (1,), "NC4": (2,),
                   "NC5": (2,), "NC6": (2,)}
    for tag, want in want_by_tag.items():
        got = CODES.get(tag)
        label = {0: "must be 0", 1: "must be 1 (FAIL)",
                 2: "must be 2 (MOVED)"}[want[0]]
        print(f"  {tag:<6} exit {got}   {label:<18} "
              f"{'ok' if got in want else 'WRONG'}")
    bad = [t for t, w in want_by_tag.items() if CODES.get(t) not in w]
    if bad:
        print(f"\nVERDICT: THE NEGATIVE CONTROL DID NOT ESTABLISH WHAT IT CLAIMS — {bad}")
        return 1
    print("\nVERDICT: delta_control.py exits 0 on the clean tree and NON-ZERO under all")
    print("         six mutations.  It is a control that can fail, and it fails on the")
    print("         very change b68db5d's cited battery is blind to.")
    print()
    print("         THIS IS A DEMONSTRATION, NOT THE EVIDENCE.  The author of an instrument")
    print("         picks the mutations his own negative control runs, so this file cannot")
    print("         establish sensitivity — that is exactly how the pre-repair version")
    print("         passed while missing 8 of mg-2216's 14.  The establishing evidence is")
    print("         out_battery_2216_rerun.txt: mg-2216's independent battery, written")
    print("         before this repair and re-run against it unmodified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
