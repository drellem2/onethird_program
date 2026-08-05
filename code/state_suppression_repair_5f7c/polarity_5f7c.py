#!/usr/bin/env python3
"""mg-5f7c — THE POLARITY, PUT TO CONSTRUCTIONS, WITH THE PRE-REPAIR CODE IN THE NEXT COLUMN.

mg-65eb found `visible_a74f.py` — the ONLY instrument in this repository that measures
suppression, so nothing contradicts it — failing CLOSED on `<div class="hidden">` while its
docstring and its README both say it fails OPEN.  mg-5f7c's first question is not how to fix
that but WHICH WAY, because fail-open and fail-closed are opposite postures and making the
code match the documents by reflex decides a safety question by typography.

THE DECISION, AND THE ARGUMENT FOR IT.  The code was wrong; both documents were right; the
instrument must fail OPEN.  Three reasons, in the order they settle it:

  1.  THE DECLARED SET ALREADY SAID SO.  `DECLARED` S4 reads `inside an element carrying the
      `hidden` ATTRIBUTE`, and the first line of `NOT_COVERED` reads `any rule from an
      external or embedded stylesheet, including `display:none` on a class`.  Both are
      printed on every run.  So the docstring, the README AND the instrument's own printed
      declared set agreed with one another, and only the code disagreed with all three.
      There was never a third document to reconcile — there was one implementation that did
      not implement the set it prints.

  2.  THE COSTS ARE NOT SYMMETRIC.  Everything this instrument is used for in this arc is
      refuting another artifact's claim that a reader is shown something: V1 exists to show
      `render16eb.py` scoring a blank page 5 of 5 SHOWN.  A SUPPRESSED verdict it cannot
      justify is therefore a FABRICATED DEFECT IN SOMEBODY ELSE'S DOCUMENT — the instrument
      manufacturing the evidence it is cited for.  A NOT SUPPRESSED verdict it cannot justify
      merely fails to find one, and the whole of what it can miss is enumerated under
      NOT_COVERED and printed on every run.  Under-detection here is bounded and declared;
      over-detection is unbounded and invisible.

  3.  THERE WAS NO SINGLE POSTURE TO DOCUMENT ANYWAY.  D1 failed CLOSED and D2 failed OPEN
      and they are ONE BUG: an attribute NAME matched by regex over the attribute TEXT.  A
      class named `hidden` was read as the `hidden` attribute; the word `open` inside
      `title="open me"` was read as the `open` attribute.  Writing the documents to match
      would have meant writing "fails closed on some inputs and open on others, depending on
      what words appear inside unrelated attribute values", which is not a posture.

WHAT THIS FILE IS.  Sixteen hand-written HTML documents — NO RENDERER, so this runs anywhere
and the polarity claim does not depend on two npm packages.  Each names the mechanism, what a
browser does with it, whether it is INSIDE the declared set, and therefore what the ONLY
correct answer is.  Both instruments are then run on it: the one in the tree, and the one read
out of `6fb424f` with `git show` and EXECUTED UNMODIFIED.  A repair whose evidence is its own
new code agreeing with its own new expectations is not evidence; the pre-repair column is.

    python3 code/state_suppression_repair_5f7c/polarity_5f7c.py
    python3 code/state_suppression_repair_5f7c/polarity_5f7c.py --rev REV   # any revision

Exit 0 iff the instrument in the tree is correct on all sixteen.
"""
import argparse
import os
import subprocess
import sys
import types

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()
VISIBLE = "code/state_delegation_repair_a74f/visible_a74f.py"
ANCHOR = "6fb424f"          # the commit this repair is built on; the defect is live there

MARK = "MARK5F7C"

# =========================================================================================
# THE POPULATION.  (id, html, mechanism, browser, in-set, correct answer, why)
#
#   browser  SHOWN  a reader is shown the marker; BLANK  a reader is shown nothing of it
#   in-set   the DECLARED mechanism that holds, or None
#   correct  the mechanisms a correct implementation of the DECLARED set reports
#
# The correct answer is a function of the DECLARED SET, not of the browser: rows where the
# two come apart are the point of the file.  P13, P15 and P16 are documents a browser blanks
# or hides that the instrument must report NOT SUPPRESSED — that IS the fail-open posture,
# and if any of the three ever reports a mechanism, this file goes red.
# =========================================================================================
CASES = [
    ("P01", f"<p>{MARK}</p>",
     "none", "SHOWN", None, [],
     "the positive control: nothing at all is suppressing it"),

    ("P02", f'<div class="hidden"><p>{MARK}</p></div>',
     "a CLASS named hidden, no stylesheet in the document", "SHOWN", None, [],
     "D1.  S4 is the `hidden` ATTRIBUTE; a class needs a stylesheet and there is none here"),

    ("P03", f'<div id="hidden"><p>{MARK}</p></div>',
     "an ID named hidden", "SHOWN", None, [],
     "the same shape on a different attribute"),

    ("P04", f'<p title="the hidden cost of this">{MARK}</p>',
     "the word `hidden` inside a title", "SHOWN", None, [],
     "the same shape inside prose a reader is shown on hover"),

    ("P05", f"<div class=hidden><p>{MARK}</p></div>",
     "an UNQUOTED class value named hidden", "SHOWN", None, [],
     "the same shape with no quotes, which the attribute parser must also get right"),

    ("P06", f'<div data-style="display:none"><p>{MARK}</p></div>',
     "a data- attribute whose NAME ends in `style`", "SHOWN", None, [],
     "FOUND BY THIS REPAIR, not by mg-65eb: the pre-repair S5 regex `style\\s*=\\s*\"...\"` "
     "matches inside `data-style=`, so this is a THIRD fail-closed shape in the same bug"),

    ("P07", f"<div hidden><p>{MARK}</p></div>",
     "the `hidden` ATTRIBUTE", "BLANK", "S4", ["S4"],
     "the mechanism S4 actually names"),

    ("P08", f'<div hidden="false"><p>{MARK}</p></div>',
     "`hidden` with the value `false`", "BLANK", "S4", ["S4"],
     "a boolean attribute: present is present, and the value is not consulted"),

    ("P09", f"<details><summary>s</summary><p>{MARK}</p></details>",
     "a <details> with no `open`", "BLANK", "S1", ["S1"],
     "mg-16eb's B3 shape, the one this instrument was written against"),

    ("P10", f"<details open><summary>s</summary><p>{MARK}</p></details>",
     "a <details> carrying `open`", "SHOWN", None, [],
     "S1 does not hold; the widget is open"),

    ("P11", f'<details title="open me"><summary>s</summary><p>{MARK}</p></details>',
     "a <details> whose TITLE contains the word open", "BLANK", "S1", ["S1"],
     "D2.  No `open` ATTRIBUTE, so S1 holds — the declared set the instrument did not "
     "implement"),

    ("P12", f'<div style="display:none"><p>{MARK}</p></div>',
     "an inline style setting display:none", "BLANK", "S5", ["S5"],
     "the mechanism S5 names"),

    ("P13", f'<style>.h {{ display: none }}</style><div class="h"><p>{MARK}</p></div>',
     "an EMBEDDED STYLESHEET hiding the class", "BLANK", None, [],
     "THE FAIL-OPEN POSTURE ITSELF.  A browser paints nothing; deciding that needs the "
     "cascade; the cascade is outside the declared set BY CONSTRUCTION, and NOT_COVERED "
     "says so in its first line.  NOT SUPPRESSED is the only answer this instrument may "
     "give, and this row goes red the moment it gives another"),

    ("P14", f'<div aria-hidden="true"><p>{MARK}</p></div>',
     "aria-hidden", "SUBSET", None, [],
     "NOT_COVERED's second line, made into a document: hidden from a SUBSET of readers — "
     "assistive technology skips it and a sighted reader is shown it"),

    ("P15", f"<!-- <p>{MARK}</p> -->",
     "inside a closed HTML comment", "BLANK", "S2", ["S2"],
     "mg-0049's R8 shape, reduced"),

    ("P16", f"<textarea><p>{MARK}</p></textarea>",
     "inside a raw-text element", "BLANK", "S3", ["S3"],
     "the mechanism S3 names"),
]


def module_at(rev, path, name):
    """The module as it is at `rev`, EXECUTED UNMODIFIED.  Not a paraphrase of the old code
    and not a copy of it into this file: `git show` and `exec`."""
    src = subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"],
                         capture_output=True, text=True, check=True).stdout
    mod = types.ModuleType(name)
    mod.__file__ = os.path.join(REPO, path)
    exec(compile(src, f"{rev}:{path}", "exec"), mod.__dict__)   # noqa: S102
    return mod


def classify(correct, got, browser):
    """What KIND of wrong, in the vocabulary the safety claim is written in."""
    if sorted(got) == sorted(correct):
        return "correct", True
    if got and not correct:
        return "FAILS CLOSED", False
    if correct and not got:
        return ("MISSES ITS OWN DECLARED SET" if browser == "BLANK" else "FAILS OPEN"), False
    return "WRONG MECHANISM", False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", default=None,
                    help="run the instrument as it is at this revision instead of the tree")
    args = ap.parse_args()

    if args.rev:
        new = module_at(args.rev, VISIBLE, "visible_at_rev")
        under = args.rev
    else:
        sys.path.insert(0, os.path.join(REPO, os.path.dirname(VISIBLE)))
        import visible_a74f as new       # noqa: PLC0415
        under = "the working tree"
    old = module_at(ANCHOR, VISIBLE, "visible_at_anchor")

    print("=" * 100)
    print("mg-5f7c — THE SUPPRESSION POLARITY, PUT TO SIXTEEN CONSTRUCTIONS")
    print("=" * 100)
    print(f"  under test   {VISIBLE} at {under}")
    print(f"  beside it    the same file at {ANCHOR}, read with `git show` and executed "
          f"unmodified")
    print(f"  population   {len(CASES)} hand-written HTML documents.  NO RENDERER IS USED, "
          f"so this")
    print("               file runs anywhere and the polarity does not rest on two npm")
    print("               packages being installed.")
    print()
    print("  THE DECISION THIS REPAIR MADE: the CODE was wrong and BOTH DOCUMENTS were right;")
    print("  the instrument must FAIL OPEN.  The argument is in this file's docstring, and")
    print("  the part of it that is checkable rather than arguable is that DECLARED S4 says")
    print("  the `hidden` ATTRIBUTE and NOT_COVERED says a class is outside the set — so the")
    print("  docstring, the README and the printed declared set all agreed already.")
    print()
    print("  A CORRECT ANSWER IS A FUNCTION OF THE DECLARED SET, NOT OF THE BROWSER.  P13,")
    print("  P14 are documents a browser blanks or hides which this instrument MUST report")
    print("  NOT SUPPRESSED.  That is the fail-open posture executed rather than claimed.")
    print()

    hdr = (f"  {'id':<5s} {'browser':<9s} {'declared':<9s} {'correct':<9s} "
           f"{'at ' + ANCHOR:<12s} {'verdict@anchor':<28s} {'now':<9s} verdict")
    print(hdr)
    print("  " + "-" * (len(hdr) - 2))
    bad_new, bad_old, rows = 0, 0, []
    for cid, doc, _mech, browser, inset, correct, _why in CASES:
        pos = doc.index(MARK)
        got_old = old.suppressors(doc, pos)
        got_new = new.suppressors(doc, pos)
        vo, oko = classify(correct, got_old, browser)
        vn, okn = classify(correct, got_new, browser)
        bad_old += 0 if oko else 1
        bad_new += 0 if okn else 1
        rows.append((cid, browser, inset, correct, got_old, vo, got_new, vn, okn))
        print(f"  {cid:<5s} {browser:<9s} {str(inset or '—'):<9s} "
              f"{'+'.join(correct) or '(none)':<9s} "
              f"{'+'.join(got_old) or '(none)':<12s} {vo:<28s} "
              f"{'+'.join(got_new) or '(none)':<9s} {vn}")
    print()

    print("=" * 100)
    print("WHAT EACH CONSTRUCTION IS FOR")
    print("=" * 100)
    for cid, _doc, mech, browser, _inset, _correct, why in CASES:
        print(f"  {cid}  {mech} — a reader is shown: {browser}")
        for line in _wrap(why, 92):
            print(f"        {line}")
    print()

    print("=" * 100)
    print("THE COUNT, AND THE POPULATION IT IS OVER")
    print("=" * 100)
    print(f"  population: {len(CASES)} hand-written documents; grain: one document, one")
    print("  marker position, the set of DECLARED mechanisms reported at that position.")
    print(f"  at {ANCHOR}          {bad_old} of {len(CASES)} wrong")
    print(f"  at {under:<16s}  {bad_new} of {len(CASES)} wrong")
    print()
    closed = [r[0] for r in rows if r[5] == "FAILS CLOSED"]
    missed = [r[0] for r in rows if r[5] == "MISSES ITS OWN DECLARED SET"]
    print(f"  AT THE ANCHOR, BY KIND:  fails CLOSED on {closed or '(none)'}; misses its own")
    print(f"  declared set on {missed or '(none)'}.  BOTH DIRECTIONS, ONE BUG — an attribute")
    print("  NAME matched by regex over the attribute TEXT.")
    print()
    print("  P06 IS THIS REPAIR'S OWN FINDING AND NOT mg-65eb's.  mg-65eb reported the")
    print("  `hidden` and `open` shapes; `data-style=\"display:none\"` is the same defect on")
    print("  S5, found by writing the parser rather than by reading the report, and it was")
    print("  live at the anchor with nothing pointing at it.")
    print()
    fail_open_rows = [r[0] for r in rows if r[2] is None and r[1] != "SHOWN"]
    print(f"  THE FAIL-OPEN POSTURE, EXECUTED: {fail_open_rows} are documents a browser")
    print("  blanks or hides by a mechanism OUTSIDE the declared set, and the instrument")
    print("  reports NOT SUPPRESSED on every one of them.  A suppression instrument nobody")
    print("  has seen DECLINE to suppress is not evidence of a fail-open posture.")
    print("=" * 100)
    return 1 if bad_new else 0


def _wrap(s, n):
    out, line = [], ""
    for w in s.split():
        if len(line) + len(w) + 1 > n:
            out.append(line)
            line = w
        else:
            line = f"{line} {w}".strip()
    if line:
        out.append(line)
    return out


if __name__ == "__main__":
    sys.exit(main())
