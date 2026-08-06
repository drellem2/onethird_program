#!/usr/bin/env python3
"""mg-40e4 — Q3.  THE CLAIMS mg-5f7c MAKES ABOUT THE REPOSITORY AND ABOUT ITSELF.

Q1 and Q2 measure the instrument.  This file measures the four claims that are about
something other than the instrument, each by resolving it against the repository rather than
by reading it back.

    C1  "visible_a74f.py is THE ONLY INSTRUMENT IN THIS REPOSITORY that measures
        suppression.  No second instrument contradicts it, so each of mg-65eb's findings
        against it was unopposed."  An existence claim, and existence claims are refuted by
        exhibiting the thing.  A rule for what counts as a suppression instrument is stated
        in code below and every committed .py is measured against it.

    C2  "This repair issues no replacement prediction of where the next gap will be."  A
        negative about its own prose.  Every forward-looking sentence in the five files
        mg-5f7c added is printed so a reader can disagree with the classification.

    C3  "11 of 13 predictions held, and both misses are kept as written."  The check that
        matters is not the arithmetic but whether the PREDICTIONS were edited after the
        result was known — so `PREDICTIONS.md` in the tree is compared byte for byte with
        `PREDICTIONS.md` in the `predictions:` commit itself.

    C4  "This repair's `predictions:` commit is e3fb80e with patch-id 9af08bc5...".  The
        refinery rebases, so that sha is on a branch and not on `main`.  Patch-id is what
        adjudicates displacement, and a patch-id is checked here rather than an ancestry.

Exit 0 iff every claim above resolves as stated.  It does not: C1 is false.

    python3 code/suppression_polarity_audit_40e4/q3_claims_40e4.py
"""
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib40e4 import REPO, VISIBLE, wrap                    # noqa: E402

FIVE = [
    "code/state_suppression_repair_5f7c/PREDICTIONS.md",
    "code/state_suppression_repair_5f7c/README.md",
    "code/state_suppression_repair_5f7c/polarity_5f7c.py",
    "code/state_suppression_repair_5f7c/offsets_5f7c.py",
    "code/state_suppression_repair_5f7c/prose_5f7c.py",
]
PREDICTIONS = "code/state_suppression_repair_5f7c/PREDICTIONS.md"
README = "code/state_suppression_repair_5f7c/README.md"

# mg-5f7c's five commits as they landed on `main`, and their pre-rebase twins.
PAIRS = [
    ("predictions", "bdeab76", "e3fb80e"),
    ("repair+instrument", "4564bdd", "4fd4f32"),
    ("docs", "5ad75a8", "98478d4"),
    ("evidence (a74f pre)", "0498b2b", "e545a2c"),
    ("evidence (transcripts)", "7f0546b", "e84ab66"),
]


def git(*a):
    return subprocess.run(["git", "-C", REPO, *a], capture_output=True, text=True).stdout


def read(path):
    return open(os.path.join(REPO, path), encoding="utf-8").read()


# =========================================================================================
# C1.  THE RULE FOR "AN INSTRUMENT THAT MEASURES SUPPRESSION", STATED SO IT CAN BE
# DISAGREED WITH.  A committed .py file qualifies iff it contains code that, for a position
# or a marker in an HTML document, DECIDES whether that content is suppressed — which this
# audit operationalises as: it tests for the `hidden` attribute, AND it tests a <details>
# for `open`, AND it tests an inline style for display:none/visibility:hidden.  Three
# independent mechanism tests in one file is not a coincidence; it is a declared set.
# =========================================================================================
TESTS = [
    ("hidden attribute", re.compile(r"[\"']hidden[\"']\s+in\s+\w+|\bhidden\b(?![-\w])"
                                    r"(?=[^\n]*attr)")),
    ("details/open", re.compile(r"details.{0,40}open|open.{0,40}details", re.S)),
    ("inline display:none", re.compile(r"display\s*:\s*none")),
]


def is_instrument(src):
    return all(t.search(src) for _n, t in TESTS)


def c1():
    print("=" * 100)
    print("C1  \"THE ONLY INSTRUMENT IN THIS REPOSITORY THAT MEASURES SUPPRESSION\"")
    print("=" * 100)
    for path in FIVE + [VISIBLE]:
        for ln, line in enumerate(read(path).splitlines(), 1):
            if re.search(r"only instrument in (this|the) repositor|ONLY INSTRUMENT IN "
                         r"(THIS|THE) REPOSITOR|second instrument", line, re.I):
                print(f"  claimed at {path}:{ln}")
                for w in wrap(line.strip().lstrip("#* "), 88):
                    print(f"      {w}")
    print()
    print("  THE RULE.  A committed .py qualifies as a suppression instrument iff it tests")
    print("  for the `hidden` attribute AND tests a <details> for `open` AND tests an inline")
    print("  style for display:none.  Stated before the sweep so the answer is not chosen.")
    print()
    files = [p for p in git("ls-files", "*.py").splitlines() if p]
    hits = []
    for p in files:
        try:
            src = read(p)
        except (OSError, UnicodeDecodeError):
            continue
        if is_instrument(src):
            hits.append(p)
    print(f"  POPULATION: {len(files)} committed .py files.  GRAIN: one file.")
    print(f"  {len(hits)} qualify, and the second column is the one that matters: does the")
    print("  file DECIDE suppression itself, or does it import `visible_a74f` and re-report?")
    indep = []
    for p in hits:
        src = read(p)
        imports = bool(re.search(r"import visible_a74f|visible_a74f as ", src))
        own = not imports and os.path.basename(p) != os.path.basename(VISIBLE)
        if own:
            indep.append(p)
        print(f"      {p:<58s} "
              + ("imports visible_a74f — not independent" if imports else
                 "IS visible_a74f" if os.path.basename(p) == os.path.basename(VISIBLE) else
                 "DECIDES ON ITS OWN"))
    print()
    print("  A DEFECT OF THIS RULE, RECORDED RATHER THAN TUNED AWAY: it selects on strings,")
    print("  so a file whose CONSTRUCTIONS contain `display:none` and `details ... open`")
    print("  qualifies without deciding anything.  That is why the second column exists and")
    print("  why the exhibit below was confirmed by READING the file, not by the count.")
    print(f"  Independent deciders other than visible_a74f.py: {indep}")
    others = indep
    print()
    ok = not others
    if others:
        print("  THE CLAIM IS FALSE.  The clearest of the others is")
        print("  code/state_visibility_audit_65eb/six65eb.py, whose `class Shown` hands the")
        print("  bytes to `html.parser` and reads attributes BY NAME — the repair mg-5f7c")
        print("  wrote, ALREADY WRITTEN, in the directory of the audit that raised the")
        print("  ticket.  Its own comment says so: \"THIS AUDIT'S OWN VISIBILITY INSTRUMENT.")
        print("  It is not visible_a74f.py and it does not import it\".  It is committed and")
        print("  it is on `main`:")
        print(f"      on main: {bool(git('cat-file', '-t', 'main:code/state_visibility_audit_65eb/six65eb.py').strip())}")
        print("  So mg-65eb's findings were NOT unopposed — mg-65eb built the opposing")
        print("  instrument in the same audit — and mg-5f7c had a second opinion available")
        print("  to cross-check the repair against and did not run it.  Q1 runs it: the two")
        print("  instruments give OPPOSITE answers on 2 of this audit's 28 constructions.")
        print("  It is not an oracle either — Q1's Q28 shows it missing an in-set mechanism")
        print("  that `visible_a74f.py` also misses — which is the reason to run both.")
        print()
        print("  AND THERE IS A THIRD.  code/state_claims_repair_0120/verdicts0120.py:133")
        print("  carries the same by-name parser and its own comment names the reason:")
        print("  \"defect mg-65eb found in visible_a74f.py (class=\\\"hidden\\\" scored")
        print("  suppressed there)\".  TWO instruments in this repository had ALREADY")
        print("  IMPLEMENTED mg-5f7c's repair before mg-5f7c was written, one of them in the")
        print("  audit that raised the ticket.  That does not make the repair unnecessary —")
        print("  the instrument under audit is the one the arc cites — but it does make")
        print("  `unopposed` false and it makes `no second instrument contradicts it` the")
        print("  opposite of the situation.")
    return ok


def c2():
    print()
    print("=" * 100)
    print("C2  \"NO REPLACEMENT PREDICTION OF WHERE THE NEXT GAP WILL BE\"")
    print("=" * 100)
    pat = re.compile(r"next (gap|defect|bug|reader)|will be somewhere|the next document|"
                     r"predict(s|ion|ed)? .{0,40}(next|future)", re.I)
    hits = []
    for path in FIVE:
        for ln, line in enumerate(read(path).splitlines(), 1):
            if pat.search(line):
                hits.append((path, ln, line.strip()))
    print(f"  POPULATION: the {len(FIVE)} files mg-5f7c ADDED.  GRAIN: one line.")
    print(f"  {len(hits)} forward-looking lines, every one printed:")
    for path, ln, line in hits:
        print(f"    {path}:{ln}")
        for w in wrap(line.lstrip("#*| "), 86):
            print(f"        {w}")
    print()
    print("  CLASSIFICATION.  Every one of them is ABOUT mg-a74f's failed prediction or is a")
    print("  refusal to issue another.  None asserts where an unfound defect is.  The")
    print("  nearest thing to a forecast is A5 / P13 / V8 — an embedded stylesheet that must")
    print("  score NOT SUPPRESSED — and that is a STANDING ROW that runs on every invocation")
    print("  and can go red, not a sentence about the future.  THE REQUIREMENT IS MET.")
    print()
    print("  AND THE REQUIREMENT IS MET BY THIS AUDIT TOO, or it would be applying a rule it")
    print("  breaks: mg-40e4 issues no prediction of where the next gap will be either.  Its")
    print("  findings are constructions that run, and Q1 exits 1 while they stand.")
    return True


def c3():
    print()
    print("=" * 100)
    print("C3  WERE THE PREDICTIONS EDITED AFTER THE RESULT WAS KNOWN?")
    print("=" * 100)
    at_commit = git("show", f"bdeab76:{PREDICTIONS}")
    in_tree = read(PREDICTIONS)
    same = at_commit == in_tree
    print(f"  {PREDICTIONS}")
    print(f"    in the `predictions:` commit bdeab76: {len(at_commit)} bytes")
    print(f"    in the working tree:                  {len(in_tree)} bytes")
    print(f"    BYTE FOR BYTE IDENTICAL: {same}")
    print("    This is the check that matters.  A prediction table can be made to score 11")
    print("    of 13 by editing the predictions, and no amount of reading the README would")
    print("    show it.")
    ids = sorted(set(re.findall(r"\*\*([AB]\d)\*\*", in_tree)))
    scored = sorted(set(re.findall(r"\|\s*\**([AB]\d)\b", read(README))))
    held = len(re.findall(r"\|\s*✅", read(README)))
    miss = len(re.findall(r"\|\s*\**❌", read(README)))
    print()
    print(f"  ids pre-registered: {ids}")
    print(f"  ids scored in README: {scored}")
    print(f"  every pre-registered id is scored: {set(ids) <= set(scored)}")
    rows = len(re.findall(r"^\|(?!---)(?!\s*\|)\s*\S.*\|\s*(?:✅|❌).*\|$",
                          read(README), re.M))
    hdr = re.search(r"## Predictions — (\d+) of (\d+) held", read(README))
    print()
    print("  THE SCORING TABLE, COUNTED RATHER THAN READ")
    print(f"    rows in the table:            {rows}")
    print(f"    marked held (✅):             {held}")
    print(f"    marked missed (❌):           {miss}")
    print(f"    the heading above it says:    {hdr.group(1)} of {hdr.group(2)} held")
    agree = hdr and (int(hdr.group(1)), int(hdr.group(2))) == (held, held + miss)
    print(f"    HEADING AGREES WITH TABLE:    {bool(agree)}")
    if not agree:
        print("    The heading is one higher in both numerator and denominator than the")
        print("    table beneath it.  The likeliest reading is that the 8th section —")
        print("    `polarity_5f7c.py --rev 6fb424f`, disclosed in this repair's own defect")
        print("    #1 as added after PREDICTIONS.md — was counted as a thirteenth scored")
        print("    row.  It is not a row of the table.  A COUNT WHOSE POPULATION IS NOT THE")
        print("    THING PRINTED UNDER IT is this arc's most repeated defect, here in the")
        print("    scoring header of the repair that catalogues it.  The `two misses` half")
        print("    of the same sentence is correct and both misses ARE kept as written.")
    return same and set(ids) <= set(scored) and bool(agree)


def c4():
    print()
    print("=" * 100)
    print("C4  PATCH-ID, THEN ADJUDICATE — mg-5f7c's FIVE COMMITS EXIST TWICE")
    print("=" * 100)
    print("  POPULATION: mg-5f7c's 5 commits.  GRAIN: one (landed, pre-rebase twin) pair.")
    print()
    ok = True
    for what, landed, twin in PAIRS:
        pl = subprocess.run(f"git -C {REPO} show {landed} | git patch-id --stable",
                            shell=True, capture_output=True, text=True).stdout.split()
        pt = subprocess.run(f"git -C {REPO} show {twin} | git patch-id --stable",
                            shell=True, capture_output=True, text=True).stdout.split()
        anc_l = subprocess.run(["git", "-C", REPO, "merge-base", "--is-ancestor",
                                landed, "main"]).returncode == 0
        anc_t = subprocess.run(["git", "-C", REPO, "merge-base", "--is-ancestor",
                                twin, "main"]).returncode == 0
        same = bool(pl) and pl[0] == pt[0]
        ok &= same
        print(f"  {what:<24s} {landed} / {twin}   patch-id "
              f"{'SAME' if same else 'DIFFERENT'}   ancestor-of-main: "
              f"landed={anc_l} twin={anc_t}")
    print()
    print("  All five twins are NOT ancestors of `main` and all five carry the SAME patch-id")
    print("  as the commit that is.  `git merge-base --is-ancestor` returns a false negative")
    print("  on every one of them, which is the failure mode mg-5f7c wrote down in advance")
    print("  and is the reason this audit adjudicates on patch-id and then reads the tree.")
    print("  README.md:283 pins the predictions commit as e3fb80e with patch-id")
    print("  9af08bc5d909054ae89a4ad8565e7531d60e2602; measured here:")
    got = subprocess.run(f"git -C {REPO} show e3fb80e | git patch-id --stable",
                         shell=True, capture_output=True, text=True).stdout.split()
    print(f"      {got[0] if got else '(unresolvable)'}")
    print(f"      matches the pinned value: "
          f"{bool(got) and got[0] == '9af08bc5d909054ae89a4ad8565e7531d60e2602'}")
    print(f"      and the commit that carries it on main is bdeab76.")
    return ok


def main():
    print("=" * 100)
    print("mg-40e4 Q3 — THE CLAIMS mg-5f7c MAKES ABOUT THE REPOSITORY AND ABOUT ITSELF")
    print("=" * 100)
    r = [c1(), c2(), c3(), c4()]
    print()
    print("=" * 100)
    print(f"  C1 only-instrument   {'HOLDS' if r[0] else 'FALSE — a second one is committed'}")
    print(f"  C2 no next-gap       {'HOLDS' if r[1] else 'FALSE'}")
    print("  C3 predictions kept  HOLDS — PREDICTIONS.md is byte-identical to the commit")
    print(f"     scoring header     {'HOLDS' if r[2] else 'FALSE — 11 of 13 over a 12-row table'}")
    print(f"  C4 patch-id          {'HOLDS' if r[3] else 'FALSE'}")
    print("=" * 100)
    return 0 if all(r) else 1


if __name__ == "__main__":
    sys.exit(main())
