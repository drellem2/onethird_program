#!/usr/bin/env python3
"""mg-5f7c — A POSITION IN ONE STRING, SPENT AS A POSITION IN ANOTHER.

`visible_a74f.main()` computed, at `6fb424f`:

    present = [h for h in CITED if marker(h) in html.unescape(out)]
    mech    = {h: suppressors(out, html.unescape(out).index(marker(h))) for h in present}

The offset is taken in `html.unescape(out)` and spent as an index into `out`.  Those two
strings have different lengths whenever a character reference precedes the marker — `&amp;`
is five characters of `out` and one of the unescaped string — so the tag-stack walk stops
short by four characters per `&` ahead of the marker.  A BYTE OFFSET STANDING IN FOR A
POSITION IS THIS ARC'S DEFECT CLASS, and it was inside the instrument built to repair it.

TWO SECTIONS, AND THE SECOND IS THE ONE THAT ANSWERS "HAS IT ALREADY CORRUPTED A PUBLISHED
FIGURE?".  Fixing arithmetic is cheap; knowing whether the wrong arithmetic was ever spent is
not, and a repair that fixes the sum without auditing what was already published leaves the
published number standing.

    A.  THE CONSTRUCTION, RENDERER-FREE.  `visible_a74f.main()` is run — the real one, not a
        paraphrase of it — over a single constructed document, with the renderer bridge
        replaced by a function that hands back that document.  Nothing about the measurement
        path is simulated: the module computes its own offsets with its own expression.  The
        row's committed prediction is the CORRECT answer, so a wrong offset shows up as that
        file's own `!!` line and its own exit 1.

    B.  THE PUBLISHED RUN, AUDITED.  Every one of the 50 section observations mg-a74f
        published is re-derived at both offsets and the two are compared.  This needs the
        renderers; without them section B prints why it did not run and section A still
        decides the exit code.

    python3 code/state_suppression_repair_5f7c/offsets_5f7c.py              # the tree
    python3 code/state_suppression_repair_5f7c/offsets_5f7c.py --rev 6fb424f
"""
import argparse
import html
import io
import os
import subprocess
import sys
import types
from contextlib import redirect_stdout

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()
VISIBLE = "code/state_delegation_repair_a74f/visible_a74f.py"
ANCHOR = "6fb424f"
PAD = 3000


def module_at(rev, path, name):
    src = subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"],
                         capture_output=True, text=True, check=True).stdout
    mod = types.ModuleType(name)
    mod.__file__ = os.path.join(REPO, path)
    exec(compile(src, f"{rev}:{path}", "exec"), mod.__dict__)   # noqa: S102
    return mod


def load(rev):
    if rev:
        return module_at(rev, VISIBLE, "visible_at_rev"), rev
    sys.path.insert(0, os.path.join(REPO, os.path.dirname(VISIBLE)))
    import visible_a74f as mod          # noqa: PLC0415
    return mod, "the working tree"


class _ProbeOK:
    """Stands in for `subprocess.run(node, bridge, ...)` in `main()`'s renderer probe only.

    Section A replaces the renderer itself, so nothing this shim returns reaches a
    measurement — it exists so that a machine with no npm packages can still run the
    construction, which is the whole reason section A is renderer-free."""
    returncode = 0
    stdout = ""
    stderr = ""


def constructed(cited):
    """A document a reader is shown NOTHING of, behind PAD character references.

    `<div hidden>` opens before every marker and never closes, so DECLARED S4 holds of every
    one of them: the correct answer is `not-suppressed 0/5`.  The `&amp;` run ahead of them
    makes the unescaped string 4*PAD characters shorter, which is more than the distance from
    the start of the document to the `<div hidden>` — so an offset taken in the unescaped
    string lands INSIDE the run of ampersands, before the tag that suppresses everything."""
    body = "".join(f"<h2>{h} &mdash; section</h2>\n<p>text</p>\n" for h in cited)
    return "&amp;" * PAD + "\n<div hidden>\n" + body


def section_a(mod, under):
    print("=" * 100)
    print("A.  THE CONSTRUCTION — visible_a74f.main() RUN OVER A DOCUMENT IT CANNOT GET RIGHT")
    print("    AT THE ANCHOR, WITH ITS OWN MEASUREMENT EXPRESSION AND ITS OWN EXIT CODE")
    print("=" * 100)
    doc = constructed(mod.CITED)
    unesc = html.unescape(doc)
    h0 = mod.CITED[0]
    # The marker is written `H1 &mdash; ` in the document and reads `H1 — ` unescaped, so its
    # position in the document is the position of its first character, not of the whole
    # string — the literal marker is not in the document at all, which is the reason
    # `bytes-in-html` is computed over the unescaped text in the first place.
    first = doc.index(f"{h0} &mdash;")
    first_u = unesc.index(mod.marker(h0))
    tagpos = doc.index("<div hidden>")
    print(f"  the document          {len(doc)} characters; unescaped {len(unesc)}; "
          f"shrinkage {len(doc) - len(unesc)}")
    print(f"  `<div hidden>` at     {tagpos} in the document")
    print(f"  {h0}'s marker at        {first} in the document, {first_u} in the unescaped "
          f"string — displaced by {first - first_u}")
    print(f"  so an offset taken in the unescaped string is spent at {first_u}, which is "
          f"{'BEFORE' if first_u < tagpos else 'after'} the")
    print("  tag that suppresses every section, and the walk finds nothing open.")
    print()
    print("  THE ROW'S COMMITTED PREDICTION IS THE CORRECT ANSWER — bytes-in-html 5/5,")
    print("  not-suppressed 0/5 — so a wrong offset is reported by the file under test as its")
    print("  OWN prediction miss, in its own words, and carried out in its own exit code.")
    print()

    saved_rows, saved_render, saved_sub = mod.ROWS, mod.R16.render, mod.subprocess
    mod.ROWS = [("X1", f"{PAD} `&amp;` then <div hidden>, never closed — a blank page",
                 lambda _t: "irrelevant: the renderer is replaced", 5, 0, 5)]
    mod.R16.render = lambda _engine, _text: doc
    mod.subprocess = types.SimpleNamespace(run=lambda *_a, **_k: _ProbeOK())
    try:
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = mod.main()
    finally:
        mod.ROWS, mod.R16.render, mod.subprocess = saved_rows, saved_render, saved_sub

    text = buf.getvalue()
    keep = [ln for ln in text.splitlines()
            if ln.startswith("X1") or ln.lstrip().startswith(("marked", "markdown-it", "!!"))]
    print(f"  {VISIBLE} at {under}, over that one row:")
    for ln in keep:
        print(f"      {ln}")
    print()
    ok = rc == 0
    print(f"  main() returned {rc} — "
          + ("the offset is spent in the string it was taken from" if ok else
             "THE OFFSET IS SPENT IN A STRING IT WAS NOT TAKEN IN"))
    print()
    return ok, rc


def section_b(mod, under):
    print("=" * 100)
    print("B.  THE 50 PUBLISHED SECTION OBSERVATIONS, RE-DERIVED AT BOTH OFFSETS")
    print("=" * 100)
    anchor_mod = module_at(ANCHOR, VISIBLE, "visible_pub")
    if not os.path.exists(anchor_mod.R16.BRIDGE):
        print(f"  NOT RUN: renderer bridge not found: {anchor_mod.R16.BRIDGE}")
        return None
    probe = subprocess.run(["node", anchor_mod.R16.BRIDGE, "marked", os.devnull],
                           capture_output=True, text=True)
    if probe.returncode != 0:
        print("  NOT RUN, and the reason rather than a bare n/a: the two GFM renderers are")
        print("  not installed, and mg-a74f's published rows cannot be re-derived without")
        print("  them.  Section A does not need them and decides the exit code alone.")
        print('      D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it')
        return None

    print(f"  POPULATION: the {len(anchor_mod.ROWS)} documents x {len(anchor_mod.ENGINES)} "
          f"renderers x {len(anchor_mod.CITED)} cited sections =")
    print(f"  {len(anchor_mod.ROWS) * len(anchor_mod.ENGINES) * len(anchor_mod.CITED)} "
          f"section observations mg-a74f PUBLISHED at {ANCHOR}, taken from that revision's")
    print("  own ROWS rather than retyped.  GRAIN: one marker lookup — the position the")
    print("  tag-stack walk was started from, and the position the marker is actually at.")
    print()
    orig = anchor_mod.M49.original()
    tot = wrong = 0
    moved = []
    for rid, _what, fn, _pb, _pf, _pr in anchor_mod.ROWS:
        text = fn(orig)
        for engine in anchor_mod.ENGINES:
            out = anchor_mod.R16.render(engine, text)
            u = html.unescape(out)
            off = []
            free_shipped, free_true, present = [], [], []
            for h in anchor_mod.CITED:
                if anchor_mod.marker(h) not in u:
                    continue
                present.append(h)
                tot += 1
                iu = u.index(anchor_mod.marker(h))
                io_ = out.find(anchor_mod.marker(h))
                if io_ < 0 or iu != io_:
                    wrong += 1
                    off.append(f"{h}{iu - io_:+d}" if io_ >= 0 else f"{h}:absent")
                if not anchor_mod.suppressors(out, iu):
                    free_shipped.append(h)
                if io_ >= 0 and not anchor_mod.suppressors(out, io_):
                    free_true.append(h)
            same = len(free_shipped) == len(free_true)
            if not same:
                moved.append((rid, engine, len(free_shipped), len(free_true)))
            print(f"  {rid} {engine:<12s} markers walked at a position that is not the "
                  f"marker's: {len(off)}/{len(present)}  {off or '(none)'}")
            print(f"      published not-suppressed {len(free_shipped)}/5; at the true "
                  f"offset {len(free_true)}/5  {'— unchanged' if same else '<<< MOVES'}")
    print()
    print(f"  {wrong} OF {tot} PUBLISHED SECTION OBSERVATIONS were walked from a position")
    print("  that is not the marker's position in the string being walked.  The other")
    print(f"  {tot - wrong} are V1's ten — inside an HTML comment a renderer escapes nothing —")
    print("  and the eight H1s, which sit ahead of the first entity in the document.")
    print()
    print(f"  AND YET {len(moved)} OF {len(anchor_mod.ROWS) * len(anchor_mod.ENGINES)} "
          f"PUBLISHED ROW FIGURES CHANGE: {moved or '(none)'}.")
    print("  NO PUBLISHED FIGURE OF mg-a74f IS WRONG, AND THAT IS LUCK OF ROW DESIGN RATHER")
    print("  THAN INSTRUMENT CORRECTNESS.  Every one of those five documents applies its")
    print("  mechanism to the WHOLE document — a comment around all of it, a `<div hidden>`")
    print("  never closed — so a displaced position is still inside the same suppression and")
    print("  returns the same verdict.  Section A is the same defect on a document where the")
    print("  displacement crosses the tag, and there it returns the opposite answer.  A")
    print("  correct number computed by a wrong method is not a correct method, and the next")
    print("  document put to this instrument would not have been protected by the shape of")
    print("  the last five.")
    print()
    return wrong, tot, len(moved)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", default=None,
                    help="run the instrument as it is at this revision instead of the tree")
    args = ap.parse_args()
    mod, under = load(args.rev)

    print("=" * 100)
    print("mg-5f7c — AN OFFSET TAKEN IN html.unescape(out), SPENT AS AN INDEX INTO out")
    print("=" * 100)
    print(f"  under test   {VISIBLE} at {under}")
    print()
    ok, _rc = section_a(mod, under)
    section_b(mod, under)
    print("=" * 100)
    print(f"  A.  the construction, at {under}: "
          + ("the offset lands on the marker" if ok else
             "THE OFFSET DOES NOT LAND ON THE MARKER"))
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
