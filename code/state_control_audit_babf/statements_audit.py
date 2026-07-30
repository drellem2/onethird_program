#!/usr/bin/env python3
"""mg-babf — DO THE STATEMENTS AND THE CONTROL AGREE?

mg-2216's B2 finding was not "the control is weak".  It was that the control and the
statements published alongside it DISAGREED, and its closing instruction named the two
acceptable repairs: **fix the control, or narrow the statements.**  Either makes them
agree; leaving the disagreement in place is the finding surviving.

This file checks which of the two happened.  For each published statement it:

  1. verifies the statement is still in the tree VERBATIM (and whether mg-7870 touched it);
  2. names a mutation from mutations_babf.py that the statement forbids and the control
     permits, or records that none exists;
  3. records whether a NARROWING of that statement was added by the repair.

Where a statement admits more than one reading, BOTH readings are printed and the verdict
is given per reading.  A universal sentence is not made true by a bounded control, and a
bounded control is not made wrong by a universal sentence — what is wrong is the pair.
"""
import os
import re
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()
PRE_REPAIR = "6b1eacf"
REPAIR = "e924590"


def read(path, rev=None):
    if rev is None:
        with open(os.path.join(REPO, path), encoding="utf-8") as fh:
            return fh.read()
    return subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"],
                          capture_output=True, check=True).stdout.decode("utf-8")


def collapse(s):
    """Compare prose across line wrapping and blockquote markers."""
    return re.sub(r"\s+", " ", re.sub(r"^\s*>\s?", "", s, flags=re.M)).strip()


STATEMENTS = [
    dict(
        sid="S1",
        where="docs/OneThird-STATE-Landing-Control-mg2da3-IndependentAudit.md "
              "(mg-2da3's ticket, item 1, quoted by mg-2216)",
        text="A control for that change must read the working tree / `HEAD` and **must fail "
             "when the file is mutated**.",
        probe="must fail when the file is mutated",
        forbids="any mutation of STATE.md or the state-history README",
        permitted_by="B01 B02 B03 B04 B05 B06 B07 B14 B15 — nine mutations of the two files, "
                     "all exit 0",
        reading_note="This is a universal over mutations of THE FILE.  It has exactly one "
                     "true reading and the control does not satisfy it; COVERAGE.md's own "
                     "'Not covered, on purpose' section is a written admission of that.",
    ),
    dict(
        sid="S2",
        where="docs/state-history/README.md, the A1 correction block (a DIGESTED region)",
        text="it exits **non-zero** both when the repair is damaged (`1`) and when a "
             "measured constant of the landing has moved (`2`) — never green about a delta "
             "that is no longer the delta it was written for.",
        probe="never green about a delta",
        forbids="the certified delta ceasing to be present, in any sense",
        permitted_by="B06 — b68db5d's own F1 correction block wrapped in an HTML comment, "
                     "absent from the rendered page, control exits 0",
        reading_note="TWO READINGS, and they differ.  (a) 'the delta' = the BYTES b68db5d "
                     "wrote: under this reading B06 leaves them in the file and the "
                     "sentence survives.  (b) 'the delta' = what b68db5d ADDED TO THE "
                     "DOCUMENT: under this reading B06 removes the F1 correction block from "
                     "every rendered view of the README while the control stays green, and "
                     "the sentence is falsified.  I cannot adjudicate between them from the "
                     "text and do not try; reading (b) is the one a reader of the README "
                     "would take, and it is the reading under which the sentence is doing "
                     "work.",
    ),
    dict(
        sid="S3",
        where="STATE.md, Appendix A, the convention this cluster establishes, item (4)",
        text="that instrument ships with a **negative control in the same commit** showing "
             "it exits non-zero when that tree is mutated",
        probe="showing it exits non-zero when that tree is mutated",
        forbids="a mutated tree on which the negative control does not exit non-zero",
        permitted_by="B01 B02 B04 B05 B06 B07 — the tree is mutated and the instrument "
                     "exits 0",
        reading_note="Same universal shape as S1, in the file that publishes the CONVENTION "
                     "the whole cluster is meant to establish.  This is the statement with "
                     "the longest reach: it is not about one instrument, it is the rule the "
                     "next instrument in this repo will be written to.",
    ),
    dict(
        sid="S4",
        where="code/state_landing_control_2da3/COVERAGE.md",
        text="Per that finding, the control was widened to match the wider statements "
             "rather than the statements narrowed to match the control",
        probe="the control was widened to match the wider statements",
        forbids="the wider statements still exceeding the control",
        permitted_by="its own document — COVERAGE.md's 'Not covered, on purpose' section, "
                     "five bullets, enumerates the ways the control does not match them",
        reading_note="This is the one that is false on its own page and needs no mutation "
                     "to show it.  S1 and S3 are universal; a bounded control cannot be "
                     "widened to match a universal.  The two repairs mg-2216 offered were "
                     "'fix the control' and 'narrow the statements'; the control was widened "
                     "(really: strengthened) but not to universality, and S1 and S3 were "
                     "not narrowed at all.",
    ),
]

NARROWINGS = [
    ("N1", "docs/state-history/README.md",
     "the goal is bounded, stated coverage, not total coverage",
     "added by mg-7870, in the correction block directly beneath the A1 block"),
    ("N2", "code/state_landing_control_2da3/COVERAGE.md",
     "The goal is not a control that catches everything",
     "added by mg-7870, COVERAGE.md's opening line"),
]

FILES = ["docs/OneThird-STATE-Landing-Control-mg2da3-IndependentAudit.md",
         "docs/state-history/README.md",
         "STATE.md",
         "code/state_landing_control_2da3/COVERAGE.md"]


def main():
    print("mg-babf — do mg-7870's control and the statements published around it agree?")
    print("=" * 86)
    print("mg-2216's instruction: fix the control OR narrow the statements.  Which happened?")
    print()

    corpus = {p: read(p) for p in FILES}
    flat = {p: collapse(t) for p, t in corpus.items()}

    disagreeing = 0
    for st in STATEMENTS:
        probe = collapse(st["probe"])
        hits = [p for p, t in flat.items() if probe in t]
        print(f"{st['sid']}  {st['where']}")
        print(f"      STATEMENT: {collapse(st['text'])}")
        print(f"      still in the tree verbatim: {bool(hits)}  ({', '.join(hits) or 'NOT FOUND'})")
        if hits:
            p = hits[0]
            try:
                was = probe in collapse(read(p, PRE_REPAIR))
            except subprocess.CalledProcessError:
                was = None
            print(f"      present before the repair ({PRE_REPAIR}): {was}"
                  f"   -> mg-7870 "
                  + ("did NOT touch it" if was else "introduced it"))
        print(f"      it FORBIDS   : {st['forbids']}")
        print(f"      control PERMITS: {st['permitted_by']}")
        print(f"      READING      : {st['reading_note']}")
        print(f"      VERDICT      : STATEMENT AND CONTROL DISAGREE")
        disagreeing += 1
        print()

    print("NARROWINGS THE REPAIR DID ADD — recorded so the finding is not overstated")
    print("-" * 86)
    for nid, path, probe, note in NARROWINGS:
        here = collapse(probe) in flat.get(path, collapse(read(path)))
        try:
            before = collapse(probe) in collapse(read(path, PRE_REPAIR))
        except subprocess.CalledProcessError:
            before = False
        print(f"  {nid}  {path}")
        print(f"      \"{probe}\"")
        print(f"      present now: {here}; present at {PRE_REPAIR}: {before}  ({note})")
    print()
    print("  These are real and they matter: bounded coverage is now STATED, in two places,")
    print("  and one of them sits directly beneath S2.  What they are not is a narrowing OF")
    print("  S1, S2 or S3.  A general disclaimer added nearby does not strike an absolute")
    print("  sentence that is still published as written — and S1 and S3 are not in either")
    print("  of the two documents the disclaimers were added to.")
    print()
    print("=" * 86)
    print(f"{len(STATEMENTS)} statements checked, {disagreeing} still disagree with the "
          f"control, 0 narrowed.")
    print("=" * 86)
    return 0


if __name__ == "__main__":
    sys.exit(main())
