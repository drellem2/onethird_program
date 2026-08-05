#!/usr/bin/env python3
"""mg-5f7c — THE THREE LOWER-PRIORITY FINDINGS IN prose_a74f.py, PUT TO CONSTRUCTIONS.

mg-65eb's verdict carried three more findings against `prose_a74f.py`, all of the same shape
as the two in `visible_a74f.py`: A NAME THAT IS NOT ITS MEASUREMENT.

    C1  P1 says `every repo-relative path named in the text EXISTS AT THE REVISION BEING
        READ` and resolved references against `os.walk`, which sees UNTRACKED files.  An
        untracked file is at no revision: it exists on one disk until somebody runs
        `git clean`, and every reader of every commit gets the dangling reference P1 passed.

    C2  P3's population was `module-level dicts EVERY key of which is a repo path`.  ONE
        EXTRA KEY — `"note": "..."` — takes a pinned table out of the population entirely,
        the printed count drops by one, and the check passes because there is nothing left
        to fail.  P3's whole subject is a table nothing looks at.

    C3  P4 attributed each `all N rows` phrase to THE NEAREST .py BASENAME IN THE PRECEDING
        400 CHARACTERS, under a heading reading `EVERY all N rows PHRASE NAMING A SCRIPT`.
        A phrase does not name whatever is closest to it.

C1 AND C2 ARE PUT TO CONSTRUCTIONS HERE; C3 IS NOT, AND THE REASON IS PRINTED RATHER THAN
OMITTED.  C1 and C2 are decidable by building the input and running both revisions on it.  C3
is a claim about ATTRIBUTION, and a construction for it would be a sentence I wrote to be
ambiguous — which proves the rule can be fooled by prose designed to fool it and says nothing
about the prose in the repository.  What replaces it is a MEASUREMENT over the real
population, printed by `prose_a74f.py` itself on every run: how many phrases are attributed
ON THE LINE and how many BY PROXIMITY.  That number is about this repository's actual prose.

RESTORE DISCIPLINE.  Two tracked files are mutated and restored with `git checkout --`, and
one untracked file is created and removed, in a `finally`.  The tree is verified clean at the
start and at the end and the run refuses to start on a dirty one, because a construction that
cannot be told apart from somebody's uncommitted work is not a construction.

    python3 code/state_suppression_repair_5f7c/prose_5f7c.py
"""
import io
import os
import subprocess
import sys
import types
from contextlib import redirect_stdout

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()
PROSE = "code/state_delegation_repair_a74f/prose_a74f.py"
ANCHOR = "6fb424f"

CARRIER = "code/state_delegation_repair_0049/mutations_0049.py"     # C1's prose carrier
CONTROL = "code/state_landing_control_2da3/delta_control.py"        # C2's pinned tables
UNTRACKED = "code/state_landing_control_2da3/mg5f7c_untracked_probe.py"


def git(*args):
    return subprocess.run(["git", "-C", REPO, *args],
                          capture_output=True, text=True, check=True).stdout


def module_at(rev, path, name):
    src = git("show", f"{rev}:{path}") if rev else _read(path)
    mod = types.ModuleType(name)
    mod.__file__ = os.path.join(REPO, path)
    exec(compile(src, f"{rev or 'tree'}:{path}", "exec"), mod.__dict__)   # noqa: S102
    return mod


def _read(path):
    with open(os.path.join(REPO, path), encoding="utf-8") as fh:
        return fh.read()


def _write(path, text):
    with open(os.path.join(REPO, path), "w", encoding="utf-8") as fh:
        fh.write(text)


def run_checker(rev, label):
    """prose_a74f.py at `rev` (None = the tree), on the working tree, freshly loaded.

    Freshly loaded on every call because that file keeps its findings in a module-level list;
    a reused module would carry one construction's findings into the next one's count."""
    mod = module_at(rev, PROSE, f"prose_{label}")
    buf = io.StringIO()
    argv = sys.argv
    sys.argv = [PROSE]
    try:
        with redirect_stdout(buf):
            rc = mod.main()
    finally:
        sys.argv = argv
    return rc, buf.getvalue()


def figure(text, needle, default="(not printed)"):
    for line in text.splitlines():
        if needle in line:
            return line.strip()
    return default


def dirty():
    return bool(git("status", "--porcelain").strip())


def main():
    if dirty():
        print("REFUSING TO RUN ON A DIRTY TREE.  This file mutates two tracked files and")
        print("creates one untracked file, and restores all three.  On a dirty tree its")
        print("restore cannot be told apart from discarding somebody's work.")
        print(git("status", "--porcelain"))
        return 2

    print("=" * 100)
    print("mg-5f7c — prose_a74f.py's THREE FINDINGS, TWO OF THEM PUT TO CONSTRUCTIONS")
    print("=" * 100)
    print(f"  under test   {PROSE} at the working tree")
    print(f"  beside it    the same file at {ANCHOR}, read with `git show` and executed")
    print("               unmodified — the repair's evidence is the OLD code disagreeing")
    print("               with it, not the new code agreeing with itself.")
    print()

    findings = []

    # ---------------------------------------------------------------------------------
    print("=" * 100)
    print("C1.  AN UNTRACKED FILE SATISFYING A CLAIM ABOUT A REVISION")
    print("=" * 100)
    print(f"  the construction: create {UNTRACKED} — present on this disk, in no commit —")
    print(f"  and add one line to {CARRIER} that names it.  P1 reads")
    print("  `every repo-relative path named in the text EXISTS AT THE REVISION BEING READ`.")
    print()
    carrier_before = _read(CARRIER)
    try:
        _write(os.path.join(REPO, UNTRACKED),
               "# mg-5f7c construction; removed by prose_5f7c.py's finally\n")
        _write(CARRIER, carrier_before
               + f"\n# mg-5f7c CONSTRUCTION (restored immediately): see {UNTRACKED}\n")
        rc_old, out_old = run_checker(ANCHOR, "c1_anchor")
        rc_new, out_new = run_checker(None, "c1_tree")
    finally:
        _write(CARRIER, carrier_before)
        if os.path.exists(os.path.join(REPO, UNTRACKED)):
            os.remove(os.path.join(REPO, UNTRACKED))

    hit_old = UNTRACKED in out_old and "[FAIL] P1" in out_old
    hit_new = UNTRACKED in out_new and "[FAIL] P1" in out_new
    print(f"  at {ANCHOR}   exit {rc_old}   the untracked path is reported: {hit_old}")
    print(f"      {figure(out_old, 'population:')}")
    print(f"  at the tree   exit {rc_new}   the untracked path is reported: {hit_new}")
    print(f"      {figure(out_new, 'population:')}")
    print(f"      {figure(out_new, '`exists` is')}")
    for line in out_new.splitlines():
        if UNTRACKED in line or (line.strip().startswith("which is present but UNTRACKED")):
            print(f"      {line.strip()}")
    ok1 = (not hit_old) and hit_new
    print(f"  >>> C1 {'REPAIRED' if ok1 else 'NOT SEPARATED'}: the construction passed at "
          f"{ANCHOR} and fails on the tree." if ok1 else
          f"  >>> C1 NOT SEPARATED: anchor reported={hit_old}, tree reported={hit_new}")
    if not ok1:
        findings.append("C1 did not separate")
    print()

    # ---------------------------------------------------------------------------------
    print("=" * 100)
    print("C2.  ONE EXTRA KEY NAMED `note`, AND A PINNED TABLE LEAVES THE POPULATION")
    print("=" * 100)
    control_before = _read(CONTROL)
    rc_base_old, out_base_old = run_checker(ANCHOR, "c2_base_anchor")
    rc_base_new, out_base_new = run_checker(None, "c2_base_tree")
    base_old = figure(out_base_old, "pinned tables")
    base_new = figure(out_base_new, "pinned tables")
    print("  BEFORE the construction:")
    print(f"      at {ANCHOR}   {base_old}")
    print(f"      at the tree   {base_new}")
    print()

    # Add one key to the FIRST pinned table found, by splicing after its opening brace.
    target = None
    for name in ("DELEGATED_PRESENTATION", "DELEGATED"):
        if f"{name} = {{" in control_before:
            target = name
            break
    if target is None:
        print("  NOT RUN: no pinned table of the expected shape in delta_control.py")
        findings.append("C2 could not find a pinned table to mutate")
    else:
        marker = f"{target} = {{"
        at = control_before.index(marker) + len(marker)
        mutated = (control_before[:at]
                   + '\n    "note": "mg-5f7c construction; restored immediately",'
                   + control_before[at:])
        try:
            _write(CONTROL, mutated)
            rc_old2, out_old2 = run_checker(ANCHOR, "c2_anchor")
            rc_new2, out_new2 = run_checker(None, "c2_tree")
        finally:
            _write(CONTROL, control_before)
        aft_old = figure(out_old2, "pinned tables")
        aft_new = figure(out_new2, "pinned tables")
        print(f"  AFTER adding one key `\"note\": \"...\"` to {target}:")
        print(f"      at {ANCHOR}   {aft_old}")
        print(f"      at the tree   {aft_new}")
        print(f"      {figure(out_new2, 'MIXED-KEY')}")
        left_old = target in base_old and target not in aft_old
        stayed_new = target in base_new and target in aft_new
        print()
        print(f"  >>> at {ANCHOR}  {target} LEFT the population: {left_old}")
        print(f"  >>> at the tree  {target} STAYED in the population: {stayed_new}")
        ok2 = left_old and stayed_new
        print(f"  >>> C2 {'REPAIRED' if ok2 else 'NOT SEPARATED'}")
        if not ok2:
            findings.append("C2 did not separate")
    print()

    # ---------------------------------------------------------------------------------
    print("=" * 100)
    print("C3.  ATTRIBUTION BY PROXIMITY — MEASURED, NOT CONSTRUCTED, AND WHY")
    print("=" * 100)
    print("  NO CONSTRUCTION IS OFFERED FOR C3 AND THAT IS A DECISION, NOT AN OMISSION.  A")
    print("  construction here would be a sentence written to be ambiguous; it would prove")
    print("  the rule can be fooled by prose designed to fool it, which is true of every")
    print("  attribution rule and says nothing about the prose in this repository.")
    print()
    print("  WHAT IS OFFERED INSTEAD is a measurement over the real population, printed by")
    print("  prose_a74f.py itself on every run:")
    rc_m, out_m = run_checker(None, "c3_tree")
    print(f"      {figure(out_m, 'attribution:')}")
    print(f"      {figure(out_m, '`all N rows` phrases over')}")
    print("  POPULATION: the `all N rows` phrases of the three declared directories.")
    print("  GRAIN: one phrase, and how its script was decided.")
    print()
    print("  ON THE LINE is a co-occurrence and BY PROXIMITY is a guess, and the run now says")
    print("  which of the two each row used.  A row attributed by proximity whose count")
    print("  disagrees with the chosen script and AGREES with another candidate in the same")
    print("  window is now a FINDING rather than a pass or a fail, because nothing in this")
    print("  checker decides which the sentence means.")
    print()

    print("=" * 100)
    print("RESTORE")
    print("=" * 100)
    still = git("status", "--porcelain").strip()
    print(f"  git status --porcelain: {still or '(clean)'}")
    if still:
        findings.append("the tree was not restored")
    print()
    print("=" * 100)
    print(f"  {len(findings)} finding(s): {findings or '(none)'}")
    print("=" * 100)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
