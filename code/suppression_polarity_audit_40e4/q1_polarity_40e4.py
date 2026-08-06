#!/usr/bin/env python3
"""mg-40e4 — Q1.  THE POLARITY, PUT TO CONSTRUCTIONS THIS AUDIT WROTE, ON TWO AXES AND
WITH A SECOND INSTRUMENT IN THE THIRD COLUMN.

mg-5f7c decided that `visible_a74f.py` must FAIL OPEN and repaired the code to that decision.
`polarity_5f7c.py` puts sixteen constructions to it and reports `0 of 16 wrong`.

WHY THAT SUITE CANNOT ANSWER THE QUESTION IT IS ASKED, and what this file does instead.
`polarity_5f7c.py`'s `correct` column is, in its own words, *a function of the DECLARED SET,
not of the browser*.  So a document the declared set gets wrong is scored CORRECT by it, by
construction.  The claim under audit is not "the code implements DECLARED"; it is the sentence
`visible_a74f.py` prints on every run — **THIS INSTRUMENT FAILS OPEN** — and mg-5f7c's own
argument for choosing that posture is that a SUPPRESSED verdict the instrument cannot justify
is *the instrument manufacturing evidence against somebody else's document*.  That is a claim
about the reader, not about the set.

SO EVERY ROW HERE IS SCORED ON TWO AXES:

    vs SET       does the code report what a correct implementation of the PRINTED declared
                 set reports?  This is mg-5f7c's axis, re-derived on constructions it did not
                 write.
    vs POSTURE   does the instrument ever report SUPPRESSED for a marker a reader IS SHOWN?
                 One such row falsifies "FAILS OPEN" whatever the declared set says, because
                 the posture is what the sentence promises and the set is only how it is
                 implemented.

    AND A THIRD COLUMN: `six65eb.Shown`, A SECOND SUPPRESSION INSTRUMENT THAT IS IN THIS
    REPOSITORY AND ON `main`.  mg-5f7c's README opens *"`visible_a74f.py` is the only
    instrument in this repository that measures suppression.  No second instrument
    contradicts it, so each of mg-65eb's findings against it was unopposed."*  That sentence
    is inherited from the ticket and is false: `code/state_visibility_audit_65eb/six65eb.py`
    carries `class Shown`, which hands the bytes to `html.parser` and reads attributes BY
    NAME — the repair mg-5f7c wrote, already written, in the directory of the audit that
    produced the ticket.  It is run here unmodified, and the rows where the two instruments
    give OPPOSITE answers are the contradiction the sentence says does not exist.

WHAT THIS FILE DOES NOT DO.  No browser is run.  The `reader` column is my reading of the HTML
and CSS specifications and every row carries the rule it rests on in its `spec` field, so a
reader can disagree with a citation instead of with an assertion.  mg-5f7c disclosed the same
limit for its own suite (its defect #4); this file carries the citations that disclosure did
not.

    python3 code/suppression_polarity_audit_40e4/q1_polarity_40e4.py
    python3 code/suppression_polarity_audit_40e4/q1_polarity_40e4.py --rev 6fb424f

Exit 0 iff the instrument in the tree holds BOTH axes on all rows.  It does not.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib40e4 import ANCHOR, REPO, SIX65EB, VISIBLE, module_at, wrap   # noqa: E402

MARK = "MARK40E4"

SHOWN, BLANK, SUBSET = "SHOWN", "BLANK", "SUBSET"

# =========================================================================================
# THE POPULATION.  (id, html, mechanism, reader, spec, inset, correct, why)
#
#   reader   SHOWN   a sighted reader with CSS and no JavaScript is shown the marker
#            BLANK   a reader is shown nothing of it
#            SUBSET  hidden from some readers and shown to others
#   spec     the rule the `reader` column rests on — a citation, not an assertion
#   inset    the DECLARED mechanism that holds of it, or None
#   correct  what a correct implementation of the PRINTED declared set reports
#
# GROUPS.  A: control.  B: in-set suppressions that must be found.  C: out-of-set
# suppressions that must be DECLINED — with and without stylesheets, which is what this
# audit's ticket asks for by name.  D: the four attribute-VALUE shapes mg-5f7c repaired.
# E: STYLE VALUES, the shape it did not.  F: where the declared set itself parts company
# with the reader.  G: misses that `NOT_COVERED` does not enumerate.
# =========================================================================================
CASES = [
    # --- A.  control -----------------------------------------------------------------
    ("Q01", f"<p>{MARK}</p>", "nothing", SHOWN,
     "no suppressing construct is present", None, [],
     "the positive control: if this reports a mechanism nothing below is evidence"),

    # --- B.  in-set suppressions that must be found --------------------------------
    ("Q02", f"<div hidden><p>{MARK}</p></div>", "the `hidden` attribute", BLANK,
     "HTML s3.2.6.5: the UA stylesheet gives [hidden] display:none", "S4", ["S4"],
     "the mechanism S4 names, and the row that must not be lost to a fail-open repair"),
    ("Q03", f'<div style="display:none"><p>{MARK}</p></div>', "an inline display:none",
     BLANK, "CSS Display 3 s2.5: display:none generates no boxes", "S5", ["S5"],
     "the mechanism S5 names"),
    ("Q04", f"<details><summary>s</summary><p>{MARK}</p></details>",
     "a <details> with no `open`", BLANK,
     "HTML s4.11.1: contents other than the summary are hidden while open is absent",
     "S1", ["S1"],
     "the mechanism S1 names"),
    ("Q05", f"<!-- <p>{MARK}</p> -->", "a closed HTML comment", BLANK,
     "HTML s13.2: comment tokens are not inserted into the DOM as element content",
     "S2", ["S2"],
     "the mechanism S2 names"),
    ("Q06", f'<script>var x = "{MARK}";</script>', "inside a <script>", BLANK,
     "HTML s4.12.1: script content is script, not text flow", "S3", ["S3"],
     "the mechanism S3 names, on the member of S3's list that is least arguable"),
    ("Q07", f"<div HIDDEN><p>{MARK}</p></div>", "the `hidden` attribute, UPPERCASE", BLANK,
     "HTML s13.2.5: attribute names are ASCII case-insensitive", "S4", ["S4"],
     "a repair that parses attributes by name must lowercase the name"),
    ("Q08", f'<div style="DISPLAY : NONE"><p>{MARK}</p></div>',
     "display:none, spaced and uppercased", BLANK,
     "CSS Syntax 3 s4: property names and keywords are ASCII case-insensitive",
     "S5", ["S5"],
     "S5 must survive the whitespace and case a real stylesheet contains"),

    # --- C.  out-of-set suppressions that must be DECLINED -------------------------
    ("Q09", f'<style>.h {{ display: none }}</style><div class="h"><p>{MARK}</p></div>',
     "AN EMBEDDED STYLESHEET hiding the class", BLANK,
     "CSS Cascade 5 s6: an author rule applies; deciding it needs the cascade",
     None, [],
     "THE FAIL-OPEN POSTURE ITSELF, with a stylesheet.  A browser paints nothing and the "
     "instrument must still say NOT SUPPRESSED, because NOT_COVERED's first line puts the "
     "cascade outside the set"),
    ("Q10", f'<link rel="stylesheet" href="x.css"><div class="h"><p>{MARK}</p></div>',
     "an EXTERNAL stylesheet", BLANK,
     "NOT_COVERED line 1 names external stylesheets; the bytes are not even in the document",
     None, [],
     "the same posture where the deciding bytes are not in the document at all"),
    ("Q11", f'<div aria-hidden="true"><p>{MARK}</p></div>', "aria-hidden", SUBSET,
     "WAI-ARIA 1.2 s6.7: removed from the accessibility tree, still painted",
     None, [],
     "NOT_COVERED line 2: hidden from a SUBSET of readers"),
    ("Q12", f'<div style="opacity:0"><p>{MARK}</p></div>', "opacity:0", BLANK,
     "CSS Color 4 s4: fully transparent, and still generates boxes",
     None, [],
     "NOT_COVERED line 3.  IN THE STYLE ATTRIBUTE, so it is the row that shows S5 is a "
     "list of two properties and not `the style attribute hides things`"),
    ("Q13", f'<div style="position:absolute;left:-9999px"><p>{MARK}</p></div>',
     "off-screen positioning", BLANK,
     "CSS Position 3: painted outside the viewport", None, [],
     "NOT_COVERED line 3 again, and the second S5-adjacent row that must not fire"),

    # --- D.  the four attribute-VALUE shapes mg-5f7c repaired ----------------------
    ("Q14", f'<div class="hidden"><p>{MARK}</p></div>',
     "a CLASS named hidden, NO STYLESHEET in the document", SHOWN,
     "HTML s3.2.6: class has no presentational effect without a rule to select on it",
     None, [],
     "mg-65eb's D1, reconstructed rather than imported.  It scored SUPPRESSED at the anchor"),
    ("Q15", f'<div id="hidden"><p>{MARK}</p></div>', "an ID named hidden", SHOWN,
     "HTML s3.2.6: id has no presentational effect", None, [],
     "the same shape on a different attribute"),
    ("Q16", f'<p title="the hidden cost of this">{MARK}</p>',
     "the word `hidden` inside a title", SHOWN,
     "HTML s3.2.6: title is advisory text, shown on hover", None, [],
     "the same shape inside prose the reader is additionally shown"),
    ("Q17", f'<div data-style="display:none"><p>{MARK}</p></div>',
     "a data- attribute whose NAME ends in `style`", SHOWN,
     "HTML s3.2.6.6: data-* is author data and has no presentational effect", None, [],
     "mg-5f7c's own P06, reconstructed.  The repair's NAME parse is what fixes it"),
    ("Q18", f'<details data-open="open" title="open me"><summary>s</summary>'
            f"<p>{MARK}</p></details>",
     "`open` in two attribute VALUES and not as an attribute", BLANK,
     "HTML s4.11.1: the open ATTRIBUTE is what opens the widget", "S1", ["S1"],
     "mg-65eb's D2, doubled: if the repair reads names, two decoy values change nothing"),

    # --- E.  STYLE VALUES — the shape mg-5f7c did not repair -----------------------
    ("Q19", f'<div style="xdisplay:none"><p>{MARK}</p></div>',
     "AN UNKNOWN PROPERTY whose name ends in `display`", SHOWN,
     "CSS Syntax 3 s5.4.4 + CSS Cascade 5 s4.1: a declaration with an unrecognised "
     "property name is INVALID AT PARSE TIME and is dropped",
     None, [],
     "THIS IS mg-5f7c's OWN P06 ONE LEVEL DOWN.  P06 was a NAME matched inside a longer "
     "name; this is a PROPERTY matched inside a longer property, in the attribute VALUE, by "
     "the same kind of unanchored regex, on the line the repair rewrote"),
    ("Q20", f'<div style="--display:none"><p>{MARK}</p></div>',
     "a CUSTOM PROPERTY named --display", SHOWN,
     "CSS Variables 1 s2: a custom property sets no CSS property; --display is not display",
     None, [],
     "a declaration that is VALID, that a browser keeps, and that hides nothing"),
    ("Q21", f'<div style="/* display:none */ color:red"><p>{MARK}</p></div>',
     "display:none INSIDE A CSS COMMENT", SHOWN,
     "CSS Syntax 3 s4.3.2: comments are consumed by the tokenizer and produce no tokens",
     None, [],
     "the declaration is not merely invalid, it does not exist"),
    ("Q22", f"<div style=\"font-family:'display:none'\"><p>{MARK}</p></div>",
     "display:none INSIDE A QUOTED STRING", SHOWN,
     "CSS Syntax 3 s4.3.5: a string token's contents are not declarations", None, [],
     "the same defect class the whole arc is about: a value read as a name"),
    ("Q23", f'<div alt="display:none"><p>{MARK}</p></div>',
     "display:none in an attribute that is not `style`", SHOWN,
     "HTML s3.2.6: alt is not a presentational attribute", None, [],
     "the control for E: if THIS fires, the repair's name parse is broken too and E says "
     "nothing about style values in particular"),

    # --- F.  where the DECLARED SET parts company with the reader ------------------
    ("Q24", f"<details><summary>{MARK}</summary><p>body</p></details>",
     "a marker inside the SUMMARY of a closed <details>", SHOWN,
     "HTML s4.11.1: the FIRST SUMMARY CHILD IS THE WIDGET'S OWN LABEL and is always "
     "rendered; only the other children are hidden while open is absent",
     "S1", ["S1"],
     "S1 says `inside a <details> carrying no open attribute`, and a summary is inside one. "
     "The code implements the set exactly and reports SUPPRESSED for a heading a reader is "
     "shown in full.  A DECLARED-SET DEFECT, not a code defect, and the fail-open sentence "
     "is printed without that qualification"),
    ("Q25", f"<textarea>{MARK}</textarea>",
     "a marker inside a <textarea>", SHOWN,
     "HTML s4.10.11: the textarea's child text is its DEFAULT VALUE and is rendered in the "
     "control",
     "S3", ["S3"],
     "S3 lists textarea beside script, style and template.  The other three are not painted "
     "and textarea IS.  `polarity_5f7c.py`'s P16 is this document and its browser column "
     "says BLANK — A ROW NAME THAT IS NOT ITS MEASUREMENT, in the suite written to prove "
     "the polarity"),
    ("Q26", f'<style>[hidden] {{ display: block !important }}</style>'
            f"<div hidden><p>{MARK}</p></div>",
     "A STYLESHEET THAT UN-HIDES AN IN-SET MECHANISM", SHOWN,
     "CSS Cascade 5 s6.2: an important author declaration beats the UA stylesheet rule "
     "[hidden]{display:none}",
     "S4", ["S4"],
     "THE ROW THE TICKET ASKS FOR BY NAME — the polarity claim on a document WITH a "
     "stylesheet.  NOT_COVERED is written as though a stylesheet can only ADD suppression "
     "the instrument misses.  A stylesheet can equally REMOVE one the instrument reports, "
     "and then the instrument is manufacturing exactly the evidence mg-5f7c's own argument "
     "says must never be manufactured"),

    # --- G.  misses NOT_COVERED does not enumerate ---------------------------------
    ("Q27", f'<div title="a>b" hidden><p>{MARK}</p></div>',
     "an in-set `hidden`, behind a `>` inside an earlier attribute VALUE", BLANK,
     "HTML s13.2.5.34: a `>` inside a quoted attribute value does not end the tag",
     "S4", ["S4"],
     "`_TAG`'s `[^>]*` stops at the first `>`, so the tag is never seen and `hidden` is "
     "never parsed.  A MISS PRODUCED BY AN IN-SET MECHANISM AND A PARSER.  mg-5f7c's README "
     "says `the whole of what it can miss is enumerated under NOT_COVERED` and "
     "`under-detection here is bounded and declared`.  It is not in those seven lines"),
    ("Q28", f"<div hidden /><p>{MARK}</p>",
     "an in-set `hidden` on a tag written with a trailing slash", BLANK,
     "HTML s13.2.5.6: a solidus on a non-void HTML element is ignored; the div stays open",
     "S4", ["S4"],
     "`suppressors` treats any tag whose attribute text ends in `/` as self-closing and "
     "never stacks it.  A second miss of the same kind, and also not in NOT_COVERED"),
]


def by_set(correct, got):
    if sorted(got) == sorted(correct):
        return "correct", True
    if got and not correct:
        return "REPORTS OUT-OF-SET", False
    if correct and not got:
        return "MISSES ITS OWN SET", False
    return "WRONG MECHANISM", False


def by_posture(reader, got):
    """The safety claim, checked against the READER rather than against the set.

    FAILS CLOSED is the only verdict that falsifies `THIS INSTRUMENT FAILS OPEN`.  A miss is
    the posture working as designed, EXCEPT that a miss of an IN-SET mechanism is a miss the
    instrument's own documents say cannot happen, so it is named separately."""
    if reader == SHOWN and got:
        return "FAILS CLOSED", False
    return "ok (fails open)", True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", default=None)
    args = ap.parse_args()

    if args.rev:
        new = module_at(args.rev, VISIBLE, "visible_at_rev")
        under = args.rev
    else:
        sys.path.insert(0, os.path.join(REPO, os.path.dirname(VISIBLE)))
        import visible_a74f as new           # noqa: PLC0415
        under = "the working tree"
    six = module_at("HEAD", SIX65EB, "six65eb_at_head")

    print("=" * 100)
    print("mg-40e4 Q1 — THE SUPPRESSION POLARITY, ON TWO AXES, WITH A SECOND INSTRUMENT")
    print("=" * 100)
    print(f"  under test     {VISIBLE} at {under}")
    print(f"  third column   {SIX65EB} `class Shown` at HEAD, executed unmodified")
    print(f"  population     {len(CASES)} HTML documents written for this audit.  NO ROW IS")
    print("                 IMPORTED FROM polarity_5f7c.py; the shapes mg-65eb and mg-5f7c")
    print("                 named are RECONSTRUCTED from their descriptions so that a row")
    print("                 agreeing is a re-derivation and not a copy.")
    print("  grain          one document, one marker position, the set of DECLARED")
    print("                 mechanisms reported at that position.")
    print("  no browser     the `reader` column is a reading of the HTML/CSS specs and every")
    print("                 row prints the rule it rests on below the table.")
    print()
    print("  AXES.  `vs SET` is mg-5f7c's question: does the code implement the set it")
    print("  prints?  `vs POSTURE` is this audit's: does it ever report SUPPRESSED for a")
    print("  marker A READER IS SHOWN?  One FAILS CLOSED row falsifies the sentence")
    print("  `THIS INSTRUMENT FAILS OPEN` that the file prints on every run, whatever the")
    print("  declared set says, because the posture is what the sentence promises.")
    print()

    hdr = (f"  {'id':<5s} {'reader':<7s} {'declared':<8s} {'correct':<8s} {'reported':<9s} "
           f"{'vs SET':<19s} {'vs POSTURE':<15s} {'Shown (2nd instr)'}")
    print(hdr)
    print("  " + "-" * (len(hdr) + 4))
    rows = []
    for cid, doc, _mech, reader, _spec, inset, correct, _why in CASES:
        pos = doc.index(MARK)
        got = new.suppressors(doc, pos)
        vs, ok_s = by_set(correct, got)
        vp, ok_p = by_posture(reader, got)
        p = six.Shown(MARK)
        p.feed(doc)
        p.close()
        if not p.hits:
            second = "not in page"
        elif any(h is None for h in p.hits):
            second = "SHOWN"
        else:
            second = "SUPPRESSED"
        rows.append((cid, reader, inset, correct, got, vs, ok_s, vp, ok_p, second))
        print(f"  {cid:<5s} {reader:<7s} {str(inset or '—'):<8s} "
              f"{'+'.join(correct) or '(none)':<8s} {'+'.join(got) or '(none)':<9s} "
              f"{vs:<19s} {vp:<15s} {second}")
    print()

    bad_set = [r for r in rows if not r[6]]
    closed = [r for r in rows if r[7] == "FAILS CLOSED"]
    in_set_miss = [r for r in rows if r[5] == "MISSES ITS OWN SET"]
    opposed = [r for r in rows
               if (r[9] == "SUPPRESSED") != bool(r[4]) and r[9] != "not in page"]

    print("=" * 100)
    print("WHAT EACH CONSTRUCTION IS FOR, AND THE SPEC RULE ITS `reader` COLUMN RESTS ON")
    print("=" * 100)
    for cid, _doc, mech, reader, spec, _inset, _correct, why in CASES:
        print(f"  {cid}  {mech} — a reader is shown: {reader}")
        for line in wrap(f"spec: {spec}", 90):
            print(f"        {line}")
        for line in wrap(why, 90):
            print(f"        {line}")
    print()

    print("=" * 100)
    print("THE COUNTS, AND THE POPULATION AND GRAIN OF EACH")
    print("=" * 100)
    print(f"  POPULATION: {len(CASES)} documents written by this audit.  GRAIN: one document,")
    print("  one marker position, the reported mechanism set.")
    print()
    print(f"  vs SET      {len(bad_set)} of {len(CASES)} wrong "
          f"{[r[0] for r in bad_set] or '(none)'}")
    print(f"  vs POSTURE  {len(closed)} of {len(CASES)} FAIL CLOSED "
          f"{[r[0] for r in closed] or '(none)'}")
    print(f"              — i.e. {len(closed)} documents a reader is shown IN FULL that this")
    print("              instrument reports SUPPRESSED, while printing THIS INSTRUMENT")
    print("              FAILS OPEN above the table it prints them in.")
    print(f"  in-set miss {len(in_set_miss)} of {len(CASES)} "
          f"{[r[0] for r in in_set_miss] or '(none)'} — under-detection by a mechanism that")
    print("              IS in the declared set, so NOT_COVERED does not enumerate it and")
    print("              `under-detection here is bounded and declared` is false.")
    print(f"  opposed     {len(opposed)} of {len(CASES)} "
          f"{[r[0] for r in opposed] or '(none)'} — rows where `six65eb.Shown`, a second")
    print("              suppression instrument ALREADY IN THIS REPOSITORY, gives the")
    print("              opposite answer.  mg-5f7c's README says no second instrument")
    print("              contradicts this one.")
    print()
    print("  THE FAIL-OPEN POSTURE, EXECUTED IN THE DIRECTION IT IS SUPPOSED TO GO:")
    declined = [r[0] for r in rows if r[1] != SHOWN and r[2] is None and not r[4]]
    print(f"  {declined} are documents a browser blanks or hides by a mechanism OUTSIDE")
    print("  the declared set, and the instrument declines to report one on every one of")
    print("  them.  Q09 and Q10 carry a stylesheet and Q12/Q13 put the out-of-set mechanism")
    print("  INSIDE the style attribute S5 reads.  A suppression instrument nobody has seen")
    print("  DECLINE to suppress is not evidence of a fail-open posture, so these rows are")
    print("  the half of the claim that does hold.")
    print("=" * 100)
    return 1 if (bad_set or closed) else 0


if __name__ == "__main__":
    sys.exit(main())
