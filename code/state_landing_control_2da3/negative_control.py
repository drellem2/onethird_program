#!/usr/bin/env python3
"""mg-2da3 — PROVE delta_control.py can fail, and show the pinned battery cannot.

A reproduction is only evidence if the instrument could have failed.  b68db5d's headline
sentence cited a battery that could not, so this file does for the new instrument what
mg-bd41 did to the old one: mutilate the working tree, re-run, and read the exit code.

THREE MUTATIONS, weakest last:

  NC1  THE SAME GUTTING mg-bd41 USED — STATE.md's lines 101-300 deleted outright and line
       1 replaced with "TOTALLY DESTROYED", 175,552 -> ~38,000 bytes.  Under this exact
       mutation the mg-6a2f battery reproduces out_audit.txt BYTE-IDENTICALLY.  The new
       instrument must not.  Both are run here, side by side, because the contrast IS the
       finding: two instruments, one destroyed tree, opposite verdicts.

  NC2  ROW :135 REVERTED TO b68db5d^ — the sharpest control there is, because it undoes
       exactly the edit being certified and nothing else.  A control that survives NC1 by
       accident (any large mutation breaks any parser) still has to fail this one.

  NC3  THE F1 CORRECTION BLOCK CUT OUT OF docs/state-history/README.md — the other half of
       the delta.  STATE.md is untouched, so this isolates the README half.

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
    want_by_tag = {"clean": (0,), "NC1": (1,), "NC2": (1,), "NC3": (1,), "NC4": (2,)}
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
    print("         four mutations.  It is a control that can fail, and it fails on the")
    print("         very change b68db5d's cited battery is blind to.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
