#!/usr/bin/env python3
"""mg-0049 — WHICH MECHANISM CATCHES WHICH ROW.  Measured, because the obvious summary of
this repair is wrong.

mg-5644's own recommendation reads:

    "The fix is available and cheap — section 8's two default-deny guards already do
     exactly this job for the two files the instrument reads, and neither is applied to a
     delegated target."

and the work item filed from it says "extend the existing section-8 default-deny guards to
the delegated surface.  Do not invent a second mechanism."  Taken literally and ALONE, that
closes ONE of mg-5644's two rows.  A fenced code block is INSIDE presentation.py's declared
subset, so `anomalies()` is silent about it by design, and `html_tokens()` skips fenced
lines by construction — the guards cannot see `Q2` and were never going to.  What sees `Q2`
is the PRESENTATION RECORD, on `state = fenced-code`, which is exactly how the same mutation
is caught in the two files the instrument reads.

So the repair is still ONE mechanism and not two: it is presentation.py, applied to the
delegated surface the way it is already applied to the certified one.  The section-8 guards
and the presentation record are the two halves of that one mechanism, and both halves had to
cross the file boundary.  This file MEASURES that rather than asserting it.

HOW.  Every mutation of `mutations_0049.py` is applied to the target's text IN MEMORY —
nothing here touches the working tree, nothing runs a subprocess — and for each one the four
questions the instrument asks are answered separately:

    content    does a cited section's content digest move, or the section vanish?
    guards     does section 8's default-deny fire on the target file?
    presented  is any cited section no longer shown to a reader at all?
    record     has any cited section's presentation record moved while still shown?

Three regimes are then derived from those four columns, FAIL outranking MOVED exactly as
`exit_code()` does: mg-bee1 (content only), a guards-only extension, and this repair.  The
authority on the real exit codes is `battery_0049.py`, which runs the actual control as a
subprocess; the last column here is that battery's PREDICTED code and the two are printed
side by side so a disagreement is visible rather than reconcilable in prose.
"""
import os
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, os.path.join(REPO, "code", "state_landing_control_2da3"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import delta_control as DC           # noqa: E402  — the instrument, imported, not copied
import presentation as pres          # noqa: E402
import mutations_0049 as M           # noqa: E402

FAIL, MOVED = DC.FAIL, DC.MOVED
TARGET = M.ATTEMPT


def worst(codes):
    """FAIL outranks MOVED, exactly as delta_control.exit_code() ranks them."""
    if FAIL in codes:
        return FAIL
    if MOVED in codes:
        return MOVED
    return 0


def measure(text):
    """The four questions, answered separately, for one version of the target file."""
    doc = pres.Doc(text)
    want_content = DC.DELEGATED[TARGET]
    want_record = DC.DELEGATED_PRESENTATION[TARGET]
    content, presented, record = [], [], []
    for name in sorted(want_content, key=lambda s: (len(s), s)):
        try:
            s, e, body = DC.named_section(text, name)
        except LookupError:
            content.append(FAIL)              # cited by name and not there
            continue
        if DC.digest(body) != want_content[name][1]:
            content.append(MOVED)
        rec = pres.region_record(doc, s - 1, e - 1)
        if not DC.is_presented(rec):
            presented.append(FAIL)
        elif pres.record_digest(rec) != want_record[name]:
            record.append(MOVED)
    guards = [MOVED] if (doc.anomalies() or doc.html_tokens()) else []
    return {"content": worst(content), "guards": worst(guards),
            "presented": worst(presented), "record": worst(record)}


CODE = {0: "0", FAIL: "1", MOVED: "2"}


def main():
    orig = M.original()
    base = measure(orig)
    print("=" * 100)
    print("mg-0049 — WHICH MECHANISM CATCHES WHICH ROW, on the delegated surface")
    print("=" * 100)
    print(f"  target: {TARGET}")
    print(f"  population: all {len(M.ROWS)} mutations of mutations_0049.py, every one of "
          f"them applied to a string in memory.")
    print(f"  the UNMUTATED target scores {base} — every column silent, which is the "
          f"control on this file itself.")
    if any(base.values()):
        print("  >>> the unmutated target is not silent; every row below is measured "
              "against a moved baseline and the table is not readable.")
    print()
    print(f"  {'row':<5} {'content':>8} {'guards':>7} {'presented':>10} {'record':>7}   "
          f"{'mg-bee1':>8} {'guards-only':>12} {'mg-0049':>8}   {'battery':>8}  what")
    print("  " + "-" * 116)
    bee1_silent, guards_silent, ours_silent = [], [], []
    for rid, _layer, what, want, fn in M.ROWS:
        m = measure(fn(orig))
        bee1 = worst([m["content"]])
        gonly = worst([m["content"], m["guards"]])
        ours = worst([m["content"], m["guards"], m["presented"], m["record"]])
        if bee1 == 0:
            bee1_silent.append(rid)
        if gonly == 0:
            guards_silent.append(rid)
        if ours == 0:
            ours_silent.append(rid)
        print(f"  {rid:<5} {CODE[m['content']]:>8} {CODE[m['guards']]:>7} "
              f"{CODE[m['presented']]:>10} {CODE[m['record']]:>7}   "
              f"{CODE[bee1]:>8} {CODE[gonly]:>12} {CODE[ours]:>8}   "
              f"{CODE[want]:>8}  {what}")
    print()
    print(f"  silent (exit 0) under mg-bee1        : {bee1_silent or '(none)'}  "
          f"— {len(bee1_silent)} of {len(M.ROWS)}")
    print(f"  silent under a GUARDS-ONLY extension : {guards_silent or '(none)'}  "
          f"— {len(guards_silent)} of {len(M.ROWS)}")
    print(f"  silent under mg-0049                 : {ours_silent or '(none)'}  "
          f"— {len(ours_silent)} of {len(M.ROWS)}")
    print()
    print("  READ THE THIRD LINE AGAINST THE SECOND.  A guards-only extension — the literal")
    print("  reading of the recommendation this repair was filed on — leaves R2 at exit 0:")
    print("  the fence is inside the modelled subset, so no guard is meant to see it, and a")
    print("  reader following the certified cell's links is still shown a wall of unrendered")
    print("  source.  Only the presentation record catches it, on `state = fenced-code`, and")
    print("  it is the SAME record and the SAME presentation.py that catch it in the two")
    print("  files the instrument reads.  One mechanism, both halves of it, across the file")
    print("  boundary the repair drew.")
    print()
    print("  R3 and R4 are silent in every regime INCLUDING this one, and that is the bound:")
    print("  they are text a reader IS shown, outside every cited section.  R9 is silent")
    print("  under mg-bee1 and fires here on the guards alone — the cost, not the win.")
    print("=" * 100)
    disagree = [rid for (rid, _l, _w, want, fn) in M.ROWS
                if worst(list(measure(fn(orig)).values())) != want]
    if disagree:
        print(f"  NOTE: this decomposition and battery_0049.py's PREDICTED codes disagree "
              f"on {disagree}.")
        print("  battery_0049.py runs the real control and is the authority; this file is a")
        print("  decomposition of it and a disagreement is a defect in this file.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
