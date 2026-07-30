#!/usr/bin/env python3
"""mg-bee1 — SEVEN NEW MUTATIONS AT THE LAYERS THIS REPAIR TOUCHES.

WHY THESE SEVEN AND NOT MORE.  mg-218d's sixteen are re-run UNMODIFIED (out_layers_bee1.txt)
and they are the evidence; a battery written by the author of a repair cannot establish that
the repair works, for the reason mg-2216 gave and this lineage has repeated four times since.
These seven exist to do the one thing the auditor's battery cannot: test the BOUNDARY OF THE
NEW MECHANISM, which did not exist when that battery was written.  Three of them are
expected to be SILENT, and those are the informative rows — a repair that reports its own
bound is worth more than one that reports its own successes.

THE PREDICT-FIRST DISCIPLINE IS mg-218d'S AND IS KEPT.  Every row below carries the exit
code THIS REPAIR PREDICTED BEFORE THE RUN, written into this file before it was executed.
A battery whose expectations are written after the run is a battery that cannot be wrong.

THE HARNESS IS NOT MINE, AND THAT IS DELIBERATE.  These rows run under mg-218d's
`harness218d.py` — the auditor's snapshot/restore/exit-code reader, not one written by the
author of the code under test.  Writing a fifth harness here would put the author's
assumptions on both sides of the measurement, which is the shape of defect this cluster
exists to catch.

    python3 code/state_delegation_repair_bee1/battery_bee1.py

SAFETY.  Mutates tracked files in the WORKING TREE (`STATE.md` is not among them; the attempt
file, the state-history README and `delta_control.py` are) and restores them under a `finally`
plus a sha256 check, via mg-218d's harness.  It refuses to run on a dirty tree.
"""
import os
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, os.path.join(REPO, "code", "state_layer_audit_218d"))
import harness218d as H                                            # noqa: E402

ATTEMPT = "docs/state-history/attempt-mg-276d.md"

RETRACTION = ("**RETRACTED 2026-08-02 (mg-bee1). Everything under this heading was filed "
              "in error, is void, and is retained only so this retraction has something to "
              "point at.**")


def heading_index(text, prefix):
    lines = text.split("\n")
    hits = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    if len(hits) != 1:
        raise LookupError(f"heading {prefix!r} matched {len(hits)} lines")
    return hits[0]


def section_span(text, prefix):
    """[first, last) of the ATX section whose heading line starts with `prefix`."""
    lines = text.split("\n")
    i = heading_index(text, prefix)
    level = len(lines[i]) - len(lines[i].lstrip("#"))
    j = i + 1
    while j < len(lines):
        s = lines[j]
        if s.startswith("#"):
            lv = len(s) - len(s.lstrip("#"))
            if lv <= level:
                break
        j += 1
    return i, j


# =========================================================================================
# L1 — the DELEGATED sections.  These are the rows the new mechanism claims.
# =========================================================================================
def d1_empty_target(t):
    """The file the certified cell cites five sections of, emptied to ZERO bytes.

    Distinct from mg-218d's T3, which left a title line behind: this leaves nothing at all,
    so the target still EXISTS and every cited section is gone.
    """
    return {ATTEMPT: ""}


def d2_retitle_cited_section(t):
    """`### H3` RETITLED, its body left exactly as it was.

    The digest spans the heading line, on the same rule that makes a hollowed README block
    with its header kept a MOVED: what a section is called is part of what it says.
    """
    txt = t[ATTEMPT]
    lines = txt.split("\n")
    i = heading_index(txt, "### H3 —")
    lines[i] = "### H3 — (see the note below)"
    return {ATTEMPT: "\n".join(lines)}


def d3_append_inside_cited_section(t):
    """A sentence appended INSIDE cited section H5, contradicting what the row says of it."""
    txt = t[ATTEMPT]
    _i, j = section_span(txt, "### H5 —")
    lines = txt.split("\n")
    ins = ["", "**LATER NOTE (mg-bee1): the answer recorded above is withdrawn; the probe "
           "this section says was DISCHARGED is open again.**"]
    return {ATTEMPT: "\n".join(lines[:j] + ins + lines[j:])}


# =========================================================================================
# L1 BOUNDARY — the two rows this repair expects to be SILENT.  The mechanism digests the
# sections a certified region cites BY NAME, and nothing else in the target.  A bound that
# is stated and not tested is a bound nobody has to believe.
# =========================================================================================
def d4_edit_uncited_section(t):
    """A paragraph appended to the target's `## Supporting record` — cited by NO link."""
    txt = t[ATTEMPT]
    _i, j = section_span(txt, "## Supporting record")
    lines = txt.split("\n")
    return {ATTEMPT: "\n".join(lines[:j] + ["", RETRACTION] + lines[j:])}


def d5_retract_target_at_top(t):
    """A document-wide retraction at the TOP of the target, above every cited section.

    This is the residual of the new mechanism and the place the blind spot has moved to:
    the target's own framing is not delegated, only its cited sections are.
    """
    txt = t[ATTEMPT]
    lines = txt.split("\n")
    return {ATTEMPT: "\n".join(lines[:1]
                               + ["", "**RETRACTED 2026-08-02 (mg-bee1): nothing in this "
                                  "file is in force. Every section below was withdrawn and "
                                  "is retained as a historical draft only.**"]
                               + lines[1:])}


# =========================================================================================
# L0 — the instrument.  mg-218d's I2 widened norm() by editing the RETURN LINE.  This one
# widens it by editing the CONSTANT, which is the same defect by a different edit: if the
# new check were textual rather than behavioural, this row would walk past it.
# =========================================================================================
def i3_widen_edge_constant(t):
    """`EDGE = " \\t\\r\\n"` widened to include U+00A0 — norm() untouched."""
    txt = t[H.CONTROL]
    old = 'EDGE = " \\t\\r\\n"'
    if old not in txt:
        raise LookupError("EDGE does not read as published")
    return {H.CONTROL: txt.replace(old, 'EDGE = " \\t\\r\\n\\u00a0"', 1)}


# =========================================================================================
# L4 — the row that decides the document-global ordinal.  See globalpos_bee1.py, which runs
# the same mutation against an implementation of that alternative and finds it silent there
# too.  This row is the control's actual verdict on it.
# =========================================================================================
def p7_replace_paragraph_elsewhere(t):
    """An EXISTING paragraph in an unrelated README section REPLACED by a retraction.

    No block is added and none removed, so no ordinal moves under ANY scoping — and a
    reader is shown a document that says the corrections below are void.
    """
    txt = t[H.README]
    lines = txt.split("\n")
    i = heading_index(txt, "## How completeness is checked")
    j = i + 1
    while j < len(lines) and not lines[j].strip():
        j += 1
    k = j
    while k < len(lines) and lines[k].strip():
        k += 1
    if k == j:
        raise LookupError("no prose block under the target heading")
    return {H.README: "\n".join(lines[:j] + [RETRACTION] + lines[k:])}


# -----------------------------------------------------------------------------------------
# id, layer, description, PREDICTED EXIT (written before the run), files, fn
# -----------------------------------------------------------------------------------------
BATTERY = [
    ("D1", "L1 delegated content", "the cited file emptied to ZERO bytes", 1,
     [ATTEMPT], d1_empty_target),
    ("D2", "L1 delegated content", "a cited section RETITLED, its body untouched", 2,
     [ATTEMPT], d2_retitle_cited_section),
    ("D3", "L1 delegated content", "a contradicting sentence appended INSIDE cited H5", 2,
     [ATTEMPT], d3_append_inside_cited_section),

    ("D4", "L1 stated boundary", "the target's UNCITED section edited (expected silent)", 0,
     [ATTEMPT], d4_edit_uncited_section),
    ("D5", "L1 stated boundary", "a retraction at the TOP of the target (expected silent)", 0,
     [ATTEMPT], d5_retract_target_at_top),

    ("I3", "L0 instrument", "the EDGE constant widened, norm() untouched", 1,
     [H.CONTROL], i3_widen_edge_constant),

    ("P7", "L4 presentation", "a paragraph elsewhere REPLACED in place (no block added)", 0,
     [H.README], p7_replace_paragraph_elsewhere),
]

MUTABLE = [H.STATE, H.README, ATTEMPT, H.CONTROL]


def main():
    print(__doc__)
    tree = H.Tree(MUTABLE)
    snapshot = {r: tree.text(r) for r in MUTABLE}

    code, _out = H.run(H.control_cmd())
    print(f"BASELINE: the control on the unmutated tree -> {H.VERDICT.get(code, code)}")
    if code != 0:
        raise SystemExit("the tree is not clean to the control; nothing below would mean "
                         "anything.  Aborting.")
    print()

    rows = []
    for mid, layer, desc, predicted, _files, fn in BATTERY:
        try:
            edits = fn(snapshot)
        except LookupError as exc:
            print(f"  {mid}: COULD NOT BUILD — {exc}")
            rows.append({"id": mid, "layer": layer, "desc": desc, "expect": "n/a",
                         "code": -1, "agrees": False, "out": str(exc)})
            continue
        code, out = tree.probe(edits)
        rows.append({"id": mid, "layer": layer, "desc": desc,
                     "expect": f"exit {predicted}", "code": code,
                     "agrees": code == predicted, "out": out})

    H.report(rows, "mg-bee1 — 7 NEW MUTATIONS AT THE BOUNDARY OF THE NEW MECHANISM",
             "'expected' is what THIS REPAIR PREDICTED BEFORE RUNNING.  Three rows are "
             "predicted SILENT on purpose: they are the stated bound, tested.")
    print()

    print("=" * 90)
    print("WHAT THE SILENT ROWS MEAN — read them as the coverage statement, not as misses")
    print("=" * 90)
    for r in rows:
        if r["code"] == 0:
            print(f"  {r['id']}  {r['layer']:<22} {r['desc']}")
    print()
    print("  D4 and D5 are the DELEGATION's bound: what is delegated is what a certified")
    print("  region CITES BY NAME, so the target's uncited sections and its own framing")
    print("  are outside coverage.  Both are named in COVERAGE.md and in delta_control.py's")
    print("  header, and this battery is where they stop being assertions.")
    print()
    print("  P7 is mg-218d's B1 residual, and it is the row that decides the mechanism")
    print("  question: it changes what a reader sees, adds no block, and is silent under a")
    print("  DOCUMENT-GLOBAL ordinal too — see globalpos_bee1.py, which implements that")
    print("  alternative and measures what it would cost.  The property is restated to its")
    print("  bound rather than the mechanism widened, and this is why.")
    print()

    surprises = [r for r in rows if not r["agrees"]]
    if surprises:
        print("MUTATIONS THAT SURPRISED THIS REPAIR (predicted != observed):")
        for r in surprises:
            print(f"    {r['id']}  predicted {r['expect']}, got exit {r['code']}")
        return 1
    print("No mutation surprised this repair: every predicted exit code was the observed "
          "one.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
