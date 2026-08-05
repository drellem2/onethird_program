#!/usr/bin/env python3
"""mg-16eb — EVERY CHECKABLE CLAIM mg-0049 ADDED, checked against the tree.

WHY THIS FILE EXISTS, AND WHY IT IS NOT coverage218d.py.  mg-218d built `coverage218d.py` to
check `COVERAGE.md`'s sentences against the code.  It does that by reading `delta_control.py`
AS THE GROUND TRUTH BOX — so by construction it cannot check a claim made INSIDE
`delta_control.py`.  mg-0049 put fifty-seven lines of new load-bearing prose into exactly
that file's header.  Nothing in this repository can check them, and this file is the check.

THE SCOPE IS THE DIFF, not the repository: every claim below is one mg-0049 ADDED at 9ca11c4
or 5594c69.  A claim inherited from an earlier generation is that generation's to answer for.

REPAIRED BY mg-0120 — SIX ROWS THAT WERE NOT CHECKS.  This file used to say: "Nothing here
mutates anything.  The claims whose test is a mutation are cross-referenced to
`battery16eb.py` and `render16eb.py` ... and their observed values are RESTATED here rather
than re-derived."  Restated meant TYPED IN.  Six of the seventeen rows this file prints
carried the verdict as a literal — four as `False` (lines 94, 142, 194, 217) and two as
`True` (lines 156, 178) — so for those six the quantity computed was a constant.  A constant
returns the same answer on every tree; it reported the same thing before mg-a74f's repair and
after it, and it would report the same thing on an empty repository.  A row whose NAME
asserts a measurement and whose BODY is a typed-in answer is the exact defect this audit
filed as OPEN 1 against mg-0049.

All six are now COMPUTED, in `code/state_claims_repair_0120/verdicts0120.py`, and every one
of them has been SHOWN RETURNING BOTH ANSWERS by `code/state_claims_repair_0120/flip_0120.py`
— at two real revisions where history separates them, and on a constructed input where it
does not.  A computed verdict nobody has seen change is not distinguishable from the literal
it replaced, so that harness is part of the repair and not an extra.

THE SEVENTH LITERAL IS LEFT ALONE ON PURPOSE.  Line 72's `False` sits in the `if m is None:`
guard: it fires only when the sentence its row is about has been deleted from the file.  A
constant there is a deliberate alarm, not a pinned result, and mg-65eb marked the difference.

A THIRD VERDICT STATE.  Two of the six quote a sentence mg-a74f then REWROTE.  Such a row has
not become true — it has become moot — so `claim()` now accepts `None` and prints `[respec]`,
and the summary counts three states rather than rounding the third into either of the other
two.

MUTATION.  The repaired rows construct inputs, and every construction is applied inside a
THROWAWAY `git worktree` that is removed on the way out.  The checkout this program runs in
is never opened for writing.  Rows 4 and 6 need two GFM renderers installed outside the repo
(`npm install --prefix "$D" marked markdown-it`; `NODE_PATH="$D/node_modules"`); without them
they report UNPROBED and are never silently reported as holding.
"""
import os
import re
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()
CTL_DIR = "code/state_landing_control_2da3"
R0049 = "code/state_delegation_repair_0049"

sys.path.insert(0, os.path.join(REPO, CTL_DIR))
sys.path.insert(0, os.path.join(REPO, "code/state_claims_repair_0120"))
import delta_control as DC          # noqa: E402  — imported, never run
import presentation as PRES         # noqa: E402
import verdicts0120 as V0120        # noqa: E402  — mg-0120: the six verdicts, computed

_held, _rows = [], []
_WT = None            # mg-0120: the throwaway worktree the constructions run in
_NODE = None          # mg-0120: are the two GFM renderers present?


def read(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as fh:
        return fh.read()


def blob(rev, rel):
    return subprocess.run(["git", "-C", REPO, "show", f"{rev}:{rel}"],
                          capture_output=True, text=True, check=True).stdout


def claim(where, text, ok, detail=""):
    """`ok` is True (holds), False (BROKEN) or None (RESPECIFIED — mg-0120).

    None is NOT rounded into either of the other two.  A row whose sentence mg-a74f rewrote
    has not been checked and has not failed; reporting it as `holds` would put a green row in
    the numerator for a measurement nobody took, which is the defect this file is about."""
    ok = None if ok is None else bool(ok)
    _held.append(ok)
    _rows.append((where, text, ok, detail))
    print(f"  [{ {True: 'holds', False: 'BROKEN', None: 'respec'}[ok] }] {where}")
    print(f"           {text}")
    if detail:
        for line in detail.split("\n"):
            print(f"           {line}")


def main():
    global _WT, _NODE
    print("=" * 96)
    print("mg-16eb — THE CLAIMS mg-0049 ADDED, CHECKED.  Scope: the 9ca11c4 + 5594c69 diff.")
    print("=" * 96)
    _NODE = V0120.renderers_present()
    print(f"  six verdicts REPAIRED by mg-0120 (they were literals); renderers "
          f"{'present' if _NODE else 'ABSENT — rows 4 and 6 report UNPROBED'}")
    print("  constructions run in a throwaway git worktree; this checkout is never written to")
    print("=" * 96)
    print()
    _WT = V0120.Worktree(None)
    try:
        return _body()
    finally:
        _WT.close()


def _body():

    ctl = read(f"{CTL_DIR}/delta_control.py")
    cov = read(f"{CTL_DIR}/COVERAGE.md")
    runsh = read(f"{R0049}/run_all.sh")

    # ---------------------------------------------------------------------------------
    print("1. delta_control.py's HEADER AND TABLE COMMENTS — the file no checker in this")
    print("   repository can check, because every checker reads it as the ground truth.")
    print()

    m = re.search(r"(code/state_delegation_repair_0049/\S+\.py) runs the guards-only\s+"
                  r"control against\s+all (\w+) rows", ctl)
    if m is None:
        claim("delta_control.py", "the guards-only sentence is still in the file",
              False, "the sentence this audit found is gone — re-read the diff")
    else:
        named, count = m.group(1), m.group(2)
        exists = os.path.exists(os.path.join(REPO, named))
        claim("delta_control.py:233",
              f"the guards-only decomposition lives in `{named}`",
              exists,
              f"os.path.exists -> {exists}.  The script that does this is "
              f"{R0049}/split_0049.py.\n"
              f"COVERAGE.md, {R0049}/README.md and {CTL_DIR}/run_all.sh all name it\n"
              f"correctly; delta_control.py is the one document of the four that does not,\n"
              f"and it is the one no checker reads as a claim.")
        pop = len(re.findall(r'^\s*\("R\d+"', read(f"{R0049}/mutations_0049.py"), re.M))
        claim("delta_control.py:233",
              f"that decomposition runs against \"all {count} rows\"",
              count == {6: "six", 9: "nine"}.get(pop, str(pop)),
              f"mutations_0049.ROWS has {pop} rows and split_0049.py runs all of them; "
              f"COVERAGE.md says\n\"all nine rows\" and README.md's table says 9.  "
              f"delta_control.py says \"{count}\", which is mg-5644's population, not this "
              f"one's.")

    # mg-0120: was the literal False, with battery16eb.py's exit codes RESTATED beneath it.
    # Now the three drifts are CONSTRUCTED and run through delta_control.py as it stands,
    # with a no-op control on every call so a crash cannot be scored as a catch.
    _v, _d = V0120.v3_two_tables(_wt=_WT)
    claim("delta_control.py:757 (the DELEGATED_PRESENTATION comment)",
          "\"the two tables cannot drift apart quietly in EITHER direction\"",
          _v, _d + "\n(computed by mg-0120; at bd24efc the same code says BROKEN, which is "
                   "what\nbattery16eb.py's A1/A2 reported and what this row used to state as "
                   "a constant.)")

    # `position` is inert and says so on every row — measured over the population.
    target = "docs/state-history/attempt-mg-276d.md"
    tdoc = PRES.Doc(read(target))
    positions = []
    for name in sorted(DC.DELEGATED[target], key=lambda s: (len(s), s)):
        s, e, _b = DC.named_section(read(target), name)
        positions.append(dict(PRES.region_record(tdoc, s - 1, e - 1))["position"])
    claim("delta_control.py:748 (the DELEGATED_PRESENTATION comment)",
          "`position` \"reads 'no block (the span opens on an ATX heading ...)' on every row\"",
          all(p.startswith("no block (the span opens on an ATX heading") for p in positions),
          f"population: all {len(positions)} delegated sections; "
          f"{sum(p.startswith('no block (the span opens on an ATX heading') for p in positions)}"
          f" of {len(positions)} read that way.")

    # The stated baseline commit.
    m = re.search(r"Baselined by mg-0049 against the working tree at (\w+)\.", ctl)
    rev = m.group(1) if m else None
    ok = False
    detail = "the provenance sentence is gone"
    if rev:
        old = blob(rev, target)
        odoc = PRES.Doc(old)
        recomputed = {}
        for name in sorted(DC.DELEGATED[target], key=lambda s: (len(s), s)):
            s, e, _b = DC.named_section(old, name)
            recomputed[name] = PRES.record_digest(PRES.region_record(odoc, s - 1, e - 1))
        ok = recomputed == DC.DELEGATED_PRESENTATION[target]
        detail = (f"all {len(recomputed)} records recomputed from {rev}:{target} and "
                  f"compared to the pinned table.\n"
                  f"({rev} is two commits before mg-0049's parent db2b77d; the target file "
                  f"is byte-identical\nat 8ce78fb, db2b77d and HEAD, so the sentence is "
                  f"imprecise about the base and true about the bytes.)")
    claim("delta_control.py:753", f"\"Baselined by mg-0049 against the working tree at "
          f"{rev}\"", ok, detail)

    # The exit-code semantics against the row that meets them.
    # mg-0120: was the literal False, with render16eb.py's counts RESTATED beneath it.  Now
    # the bullet is LOCATED first — mg-a74f narrowed it, so on a repaired tree this row is
    # RESPECIFIED — and where it is still asserted, both directions are refuted by
    # construction.
    _v, _d = V0120.v4_exit_semantics(_wt=_WT, have_node=_NODE)
    claim("delta_control.py:346 (the EXIT CODES table)",
          "exit 1 is \"a region ... NO LONGER PRESENTED TO A READER\"; exit 2 is drift, "
          "\"re-baseline this instrument\"",
          _v, _d)
    print()

    # ---------------------------------------------------------------------------------
    print("2. presentation.py's HEADER — same file class, same absence of a checker.")
    print()
    # mg-0120: was the literal TRUE, justified with a fact about a DIFFERENT property — that
    # the eleven certified digests are byte-identical.  That fact is true and it is not this
    # sentence.  The sentence is about what mg-0049's diff CHANGED, so it is computed over
    # the commit range, at the grain of an executable statement with docstrings removed.
    _v, _d = V0120.v5_presentation_diff()
    claim("presentation.py:24",
          "\"NOTHING IN THIS FILE CHANGED EXCEPT ONE MESSAGE AND FOUR SELF-TEST CASES\"",
          _v, _d + "\n(the 11 certified presentation digests ARE byte-identical to db2b77d's "
                   "and\ndelta_control.py does exit 0 on the clean tree — that is what this "
                   "row used to\noffer as its evidence, and it is a different claim from the "
                   "one the row quotes.)")
    print()

    # ---------------------------------------------------------------------------------
    print("3. COVERAGE.md — the ONE added document that has an external checker "
          "(coverage218d.py).")
    print()
    split_out = read(f"{R0049}/out_split.txt")
    pop = len(re.findall(r'^\s*\("R\d+"', read(f"{R0049}/mutations_0049.py"), re.M))
    claim("COVERAGE.md:276", "\"split_0049.py measures this over all nine rows\"",
          "all nine rows" in cov and pop == 9, f"mutations_0049.ROWS has {pop} rows.")
    for figure in ("— 8 of 9", "— 4 of 9", "— 2 of 9"):
        claim("COVERAGE.md:276-278", f"the regime figure \"{figure.strip('— ')}\"",
              figure in split_out,
              "found in out_split.txt, which this audit reproduced byte-identically "
              "from its own run.")
    # mg-0120: was the literal TRUE.  Now the claimed pair is READ OUT OF the table and the
    # observed pair READ OUT OF mg-5644's own re-run transcript, and the verdict is whether
    # they agree row by row.
    _v, _d = V0120.v6_r1r2_table()
    claim("COVERAGE.md:243-244",
          "the R1/R2 table: exit 0 against mg-bee1, exit 1 against mg-0049",
          _v, _d + "\n(the re-run is byte-identical to the committed out_5644_rerun.txt; "
                   "reproduce16eb.py\nis what checks that, and this row joins on the "
                   "transcript rather than re-running it.)")
    print()

    # ---------------------------------------------------------------------------------
    print("4. THE mg-0049 README's 'What is NOT undone' TABLE — the table that answers the")
    print("   over-correction question, so a wrong cross-reference in it is load-bearing.")
    print()
    sections = dict((int(n), t) for n, t in
                    re.findall(r'^echo "### (\d+)\. (.+)$', runsh, re.M))
    n_218d = [n for n, t in sections.items() if "coverage218d" in t]
    n_5644 = [n for n, t in sections.items() if "mg-5644's OWN battery" in t]
    # mg-0120: was the literal False.  Now the section is RESOLVED BY ITS COMMAND — never by
    # its title, which is how a first draft of this shape got the wrong answer, because
    # section 7 is `coverage218d.py`, a different program of the same audit.
    _v, _d = V0120.v7_section_pointer()
    claim(f"{R0049}/README.md:105-106",
          "mg-218d's and mg-5644's batteries are re-run in the section of run_all.sh the "
          "table names",
          _v, _d + "\n(at bd24efc the same code says BROKEN: both rows said 7 there.  "
                   "mg-a74f corrected\nthem to 8, so what this row used to pin as a constant "
                   "now moves with the tree.)")
    rnd = read(f"{R0049}/out_render.txt")
    claim(f"{R0049}/README.md:152", "render0049.py: \"100 comparisons\"",
          "100 comparisons" in rnd, "found in out_render.txt, reproduced by this audit.")
    covout = read(f"{R0049}/out_coverage218d.txt")
    claim(f"{R0049}/README.md:110", "coverage218d.py: \"40 of 40\"",
          "40 of 40" in covout, "found in out_coverage218d.txt, reproduced by this audit.")
    claim(f"{R0049}/README.md:23", "mg-5644's renderers agreed \"over 60 comparisons\"",
          "60 comparisons" in read("code/state_delegation_audit_5644/out_render.txt"),
          "found in mg-5644's own committed out_render.txt, which this audit reproduced.")
    print()

    # ---------------------------------------------------------------------------------
    print("5. render0049.py's OWN VERDICT — the repair's instrument for 'what a reader is")
    print("   shown', on the one row where it is asked about a container.")
    print()
    # mg-0120: was the literal False, with render16eb.py's counts RESTATED beneath it.  Now
    # R5 is LOCATED first — mg-a74f narrowed it too — and where it still asserts the reader
    # half, the two conjuncts are measured SEPARATELY, because separating them is the finding.
    _v, _d = V0120.v8_r5_details(have_node=_NODE)
    claim(f"{R0049}/render0049.py:11 and out_render.txt",
          "R5: \"`<details>` at the top SUPPRESSES NOTHING: every cited section is still on "
          "the page as the document's own prose\" — 5/5 ANY, 5/5 HEADING, both renderers",
          _v, _d)
    print()

    print("=" * 96)
    held = sum(1 for v in _held if v is True)
    broken = [(w, t) for w, t, ok, _d in _rows if ok is False]
    respec = [(w, t) for w, t, ok, _d in _rows if ok is None]
    # THE POPULATION IS THE 17 PRINTED ROWS AND THE GRAIN IS ONE ROW.  mg-0120: this used to
    # read "N of 17 hold" with two states, which forced a row whose sentence had been
    # rewritten into one of them.  Three states are printed and they sum to the population.
    print(f"POPULATION: the {len(_held)} rows printed above, one per checkable claim mg-0049")
    print(f"ADDED.  GRAIN: one row.  THREE STATES, and they sum to the population:")
    print(f"    {held:>2d}  hold against the tree")
    print(f"    {len(broken):>2d}  do not")
    print(f"    {len(respec):>2d}  RESPECIFIED — the sentence the row checks is no longer in "
          f"the file")
    print()
    if broken:
        print("BROKEN:")
        for where, text in broken:
            print(f"    {where}\n        {text}")
        print()
    if respec:
        print("RESPECIFIED — NOT a pass.  These rows checked a sentence that has since been")
        print("rewritten; the successor sentence is a different claim and needs its own check:")
        for where, text in respec:
            print(f"    {where}\n        {text}")
        print()
    inside = [w for w, _t, ok, _d in _rows if ok is False and "delta_control.py" in w]
    print(f"WHERE THE BROKEN ONES ARE.  {len(inside)} of the {len(broken)} are in")
    print("delta_control.py, the file coverage218d.py reads as the ground truth box and")
    print("therefore cannot check.")
    print()
    print("HOW MANY OF THESE VERDICTS ARE COMPUTED.  All 17.  Six were literals until")
    print("mg-0120 (four `False`, two `True`); each of the six is now computed and each has")
    print("been shown returning BOTH answers by code/state_claims_repair_0120/flip_0120.py.")
    print("A seventh literal remains at line 72 and is meant to: it is a guard branch that")
    print("fires only when the sentence its row is about has been deleted.")
    print("=" * 96)
    return 0


if __name__ == "__main__":
    sys.exit(main())
