#!/usr/bin/env python3
"""mg-218d — THE LAYER BATTERY.  Mutations at the layers mg-4acd does NOT claim.

THE QUESTION THIS BATTERY ASKS is not "does the presentation record work?".  Four
iterations of this control have each closed their predecessor's gap and exposed a new
layer, so the useful question is WHICH LAYER IS UNCONTROLLED NOW.  Re-running mg-babf's
four is necessary and not sufficient: after mg-4acd they are the author's known-answer
set.  This battery is built at the layers ABOVE the one that was just closed.

THE STACK, named so that a verdict can be attached to each layer:

    L0  INSTRUMENT        the code and the baked-in constants that define every layer below
    L1  FILE SELECTION    which files are read at all — and what the certified text POINTS AT
    L2  REGION SET        which regions inside those files are certified
    L3  REGION LOCATION   which bytes are the region                     (locator)
    L4  PRESENTATION      is a reader shown them, and where              (mg-4acd)
    L5  BYTE CONTENT      are these the certified bytes                  (mg-7870)
    L6  NORMALISATION     the equivalence rule under which L5 is asked   (mg-7870/mg-babf)

Every mutation below carries the exit code THIS AUDIT PREDICTED before it was run, so a
row that surprised me is visible as a row that surprised me.  A battery whose predictions
are written after the run is a battery that cannot be wrong.

    python3 code/state_layer_audit_218d/layers218d.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness218d as H                                            # noqa: E402

ATTEMPT = "docs/state-history/attempt-mg-276d.md"

# markers, restated here from the README's own text — not imported from the instrument
M_F1 = "**`no 4d tally` is a correction"
M_F2 = "**THOSE FIVE FIGURES WERE WRONG, here and in `57f962f`'s commit message"
M_A1_7870 = "DID NOT ESTABLISH WHAT THE BLOCK ABOVE CLAIMS"

H_CERT = "## What certifies a change to these files, and what does not"
H_COMPLETE = "## How completeness is checked"
H_A3 = "## The three A3 sites"

RETRACTION = ("**RETRACTED 2026-08-02 (mg-218d). Every correction block under "
              "*\"What certifies a change to these files\"* below was filed in error, is "
              "void, and is retained only so this retraction has something to point at.**")


def heading_index(text, prefix):
    lines = text.split("\n")
    hits = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    if len(hits) != 1:
        raise LookupError(f"heading {prefix!r} matched {len(hits)} lines")
    return hits[0]


# =========================================================================================
# L3 — REGION LOCATION.  The brief asks explicitly: if a certified region is deleted
# outright, or its locator marker renamed, does anything fire?  These four answer it.
# =========================================================================================
def l3_delete_region(t):
    """A whole certified region DELETED from the README."""
    lines = t[H.README].split("\n")
    s, e = H.quote_span(t[H.README], M_F1)
    return {H.README: "\n".join(lines[:s] + lines[e:])}


def l3_rename_marker(t):
    """The locator MARKER reworded, the block otherwise left in place and in force."""
    txt = t[H.README]
    i = H.marker_line(txt, M_F1)
    lines = txt.split("\n")
    lines[i] = lines[i].replace("**`no 4d tally` is a correction",
                                "**`no 4d tally` is an amendment")
    return {H.README: "\n".join(lines)}


def l3_rename_row_key(t):
    """The ledger row's ATTEMPT ID renamed — the key the cell is located by."""
    txt = t[H.STATE]
    i = H.row_index(txt, "mg-276d")
    lines = txt.split("\n")
    lines[i] = lines[i].replace("mg-276d", "mg-276z", 1)
    return {H.STATE: "\n".join(lines)}


def l3_duplicate_region(t):
    """A certified region DUPLICATED verbatim under a new heading (ambiguous locator)."""
    txt = t[H.README]
    lines = txt.split("\n")
    s, e = H.quote_span(txt, M_A1_7870)
    return {H.README: "\n".join(lines + ["", "## Appendix Y — retained copy", ""]
                                + lines[s:e])}


# =========================================================================================
# L4' — PRESENTATION CONTEXT BEYOND THE REGION'S OWN SECTION.
#
# mg-4acd's `position` field is an ordinal among the blocks OF A SECTION, and `heading` is
# the ATX path.  Both are section-local.  mg-babf's B07 (a retraction inserted immediately
# above a certified block) is caught because it lands INSIDE the block's section.  These
# ask what happens when the same paragraph lands one line earlier, on the other side of a
# heading — and a reader still passes it immediately before the certified block.
# =========================================================================================
def p_retract_inside_section(t):
    """B07 restated: the retraction as the FIRST block INSIDE the certified section."""
    txt = t[H.README]
    lines = txt.split("\n")
    i = heading_index(txt, H_CERT)
    return {H.README: "\n".join(lines[:i + 1] + ["", RETRACTION] + lines[i + 1:])}


def p_retract_across_heading(t):
    """THE SAME PARAGRAPH, moved ONE LINE EARLIER: the last block of the section before.

    From a reader's point of view this is the identical page: retraction, heading,
    certified blocks.  From `position`'s point of view it is a different section.
    """
    txt = t[H.README]
    lines = txt.split("\n")
    i = heading_index(txt, H_CERT)
    return {H.README: "\n".join(lines[:i] + [RETRACTION, ""] + lines[i:])}


def p_retract_far_section(t):
    """A document-wide retraction at the top of an unrelated section."""
    txt = t[H.README]
    lines = txt.split("\n")
    i = heading_index(txt, H_COMPLETE)
    return {H.README: "\n".join(lines[:i + 1] + ["", RETRACTION] + lines[i + 1:])}


def p_new_section_at_top(t):
    """A new `## READ THIS FIRST` section carrying a document-wide retraction."""
    txt = t[H.README]
    lines = txt.split("\n")
    i = heading_index(txt, "## The rule")
    ins = ["## READ THIS FIRST — this document is superseded", "",
           "**Nothing in this file is in force. It is retained as a historical draft; the "
           "corrections below were all withdrawn on 2026-08-02.**", ""]
    return {H.README: "\n".join(lines[:i] + ins + lines[i:])}


def p_rename_h1(t):
    """POSITIVE CONTROL: the document's H1 retitled.  `heading` path[0] moves for every
    certified README region, so this MUST fire.  A battery that only produces zeros is a
    battery that is not connected to the instrument."""
    txt = t[H.README]
    lines = txt.split("\n")
    lines[0] = "# DRAFT — superseded, do not cite"
    return {H.README: "\n".join(lines)}


def p_retract_state_other_section(t):
    """A retraction in STATE.md, in a section other than the certified row's."""
    txt = t[H.STATE]
    lines = txt.split("\n")
    i = heading_index(txt, "## The single lemma to prove")
    ins = ["", "**RETRACTED 2026-08-02 (mg-218d): the Attempt index below is superseded "
           "and every row in it is void.**"]
    return {H.STATE: "\n".join(lines[:i + 1] + ins + lines[i + 1:])}


# =========================================================================================
# L2 — REGION SET.  What is certified is a list of ten regions somebody chose.  A mutation
# that ADDS a contradicting region is invisible to a mechanism that digests the regions on
# the list.
# =========================================================================================
def s_contradicting_copy(t):
    """A near-copy of the F1 correction block, its claim INVERTED, in a new section.

    Its header is altered by two words so the locator still matches exactly one line and
    reports no ambiguity.  A reader now meets two F1 correction blocks that disagree.
    """
    txt = t[H.README]
    lines = txt.split("\n")
    s, e = H.quote_span(txt, M_F1)
    copy = [l.replace("**`no 4d tally` is a correction",
                      "**LATER NOTE: `no 4d tally` was a correction")
             .replace("This row states no 4d *tally* of its own",
                      "This row states no tally of any kind, as originally written")
            for l in lines[s:e]]
    return {H.README: "\n".join(lines + ["", "## Appendix W — later notes", ""] + copy)}


# =========================================================================================
# L1 — FILE SELECTION, and the TARGET of what a certified region points at.
#
# The certified ledger cell carries SEVEN links into `attempt-mg-276d.md` and cites its
# sections H1-H5 by name: the row asserts current state AND POINTS THERE.  A reader who
# follows the certified region reads that file.  Nothing certifies it.
# =========================================================================================
def t_delete_target_section(t):
    """`### H1 — ...`, one of the five sections the certified cell links to BY NAME,
    deleted from the file the cell points at."""
    txt = t[ATTEMPT]
    lines = txt.split("\n")
    i = heading_index(txt, "### H1 — the step-4d clause")
    j = i + 1
    while j < len(lines) and not lines[j].startswith("### "):
        j += 1
    return {ATTEMPT: "\n".join(lines[:i] + lines[j:])}


def t_invert_target_claim(t):
    """The F1 repair INVERTED where the certified row sends the reader to read it."""
    txt = t[ATTEMPT]
    old = ("a mislabel repaired by an upgrade, not a retraction")
    if old not in txt:
        raise LookupError("the H2 sentence this mutation inverts is not in the file")
    return {ATTEMPT: txt.replace(
        old, "a mislabel that was RETRACTED on 2026-08-02 and not repaired at all", 1)}


def t_empty_target(t):
    """The file the certified cell points at seven times, emptied to one line."""
    return {ATTEMPT: "# Attempt index (mg-276d)\n\nThis file is intentionally empty.\n"}


# =========================================================================================
# L0 — THE INSTRUMENT.  The certified set, the digests and the rules are constants in
# delta_control.py.  Nothing in this cluster certifies delta_control.py.
# =========================================================================================
def i_drop_a_region(t):
    """One entry deleted from CERTIFIED — coverage silently narrows from ten to nine."""
    txt = t[H.CONTROL]
    start = txt.index('    ("readme.B1.A3"')
    end = txt.index('    ("readme.index"')
    return {H.CONTROL: txt[:start] + txt[end:]}


def i_widen_normalisation(t):
    """`.strip(" \\t\\r\\n")` widened to `.strip()` — the rule mg-babf probed and cleared,
    silently reversed.  Nothing above the instrument reads this line."""
    txt = t[H.CONTROL]
    old = 'return text.strip(EDGE).encode("utf-8")'
    if old not in txt:
        raise LookupError("norm() does not read as published")
    return {H.CONTROL: txt.replace(old, 'return text.strip().encode("utf-8")', 1)}


# -----------------------------------------------------------------------------------------
BATTERY = [
    # id, layer, description, predicted exit, files, fn
    ("L3a", "L3 region location", "a certified region DELETED outright", 1,
     [H.README], l3_delete_region),
    ("L3b", "L3 region location", "the locator MARKER reworded, block still in force", 1,
     [H.README], l3_rename_marker),
    ("L3c", "L3 region location", "the ledger row's attempt id renamed", 1,
     [H.STATE], l3_rename_row_key),
    ("L3d", "L3 region location", "a certified region duplicated verbatim", 1,
     [H.README], l3_duplicate_region),

    ("P1", "L4 presentation", "B07 restated: retraction INSIDE the certified section", 2,
     [H.README], p_retract_inside_section),
    ("P2", "L4 presentation", "THE SAME PARAGRAPH one line earlier, across the heading", 0,
     [H.README], p_retract_across_heading),
    ("P3", "L4 presentation", "document-wide retraction in an unrelated section", 0,
     [H.README], p_retract_far_section),
    ("P4", "L4 presentation", "a new 'READ THIS FIRST — superseded' section near the top", 0,
     [H.README], p_new_section_at_top),
    ("P5", "L4 presentation", "POSITIVE CONTROL: the README's H1 retitled", 2,
     [H.README], p_rename_h1),
    ("P6", "L4 presentation", "STATE.md: retraction of the Attempt index, other section", 0,
     [H.STATE], p_retract_state_other_section),

    ("S1", "L2 region set", "a contradicting near-copy of a certified block added", 0,
     [H.README], s_contradicting_copy),

    ("T1", "L1 reference target", "a section the certified cell links to BY NAME deleted", 0,
     [ATTEMPT], t_delete_target_section),
    ("T2", "L1 reference target", "the F1 repair INVERTED in the file the cell points at", 0,
     [ATTEMPT], t_invert_target_claim),
    ("T3", "L1 reference target", "that file emptied (7 links from the certified cell)", 0,
     [ATTEMPT], t_empty_target),

    ("I1", "L0 instrument", "one entry deleted from CERTIFIED (ten regions -> nine)", 0,
     [H.CONTROL], i_drop_a_region),
    ("I2", "L0 instrument", "the normalisation widened to .strip() (mg-babf's rule undone)", 0,
     [H.CONTROL], i_widen_normalisation),
]

MUTABLE = [H.STATE, H.README, ATTEMPT, H.CONTROL]


def main():
    print(__doc__)
    tree = H.Tree(MUTABLE)
    snapshot = {r: tree.text(r) for r in MUTABLE}

    code, out = H.run(H.control_cmd())
    print(f"BASELINE: the control on the unmutated tree -> {H.VERDICT.get(code, code)}")
    if code != 0:
        raise SystemExit("the tree is not clean to the control; nothing below would mean "
                         "anything.  Aborting.")
    print()

    rows = []
    for mid, layer, desc, predicted, files, fn in BATTERY:
        try:
            edits = fn(snapshot)
        except LookupError as exc:
            print(f"  {mid}: COULD NOT BUILD — {exc}")
            rows.append({"id": mid, "layer": layer, "desc": desc, "expect": "n/a",
                         "code": -1, "agrees": False, "out": str(exc)})
            continue
        code, out = tree.probe(edits)
        agrees = code == predicted
        rows.append({"id": mid, "layer": layer, "desc": desc,
                     "expect": f"exit {predicted}", "code": code, "agrees": agrees,
                     "out": out})

    H.report(rows, "mg-218d LAYER BATTERY — 16 mutations at L0-L4",
             "'expected' is what THIS AUDIT PREDICTED BEFORE RUNNING, not what the "
             "instrument claims.")
    print()

    # ---- the per-layer verdict, read off the rows above ---------------------------------
    print("=" * 90)
    print("PER-LAYER VERDICT — which layers of the stack fire, read off the rows above")
    print("=" * 90)
    by = {}
    for r in rows:
        by.setdefault(r["layer"], []).append(r)
    for layer in ["L0 instrument", "L1 reference target", "L2 region set",
                  "L4 presentation", "L3 region location"]:
        rs = by.get(layer, [])
        fired = [r for r in rs if r["code"] not in (0, -1)]
        silent = [r for r in rs if r["code"] == 0]
        print(f"  {layer:<22} {len(rs)} mutations: {len(fired)} fire, "
              f"{len(silent)} exit 0")
        if silent:
            print("                         silent: " + ", ".join(r["id"] for r in silent))
    print()

    zeros = [r for r in rows if r["code"] == 0]
    print(f"{len(zeros)} of {len(rows)} mutations changed what a reader is shown and "
          f"exited 0:")
    for r in zeros:
        print(f"    {r['id']}  {r['layer']:<22} {r['desc']}")
    print()
    surprises = [r for r in rows if not r["agrees"]]
    if surprises:
        print("MUTATIONS THAT SURPRISED THIS AUDIT (predicted != observed):")
        for r in surprises:
            print(f"    {r['id']}  predicted {r['expect']}, got exit {r['code']}")
    else:
        print("No mutation surprised this audit: every predicted exit code was the "
              "observed one.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
