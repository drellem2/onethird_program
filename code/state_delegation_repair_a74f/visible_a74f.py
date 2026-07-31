#!/usr/bin/env python3
"""mg-a74f — OPEN 1: THE VISIBILITY INSTRUMENT, MEASURING THE PROPERTY ITS ROW NAMES.

mg-16eb's OPEN 1 says a proxy is standing in for the property a row claims: bytes present in
the markup and content presented to a reader are different sets.  It offers two repairs —
measure the claimed property, or narrow the claim to the measured one — and forbids a third,
keeping the wording and swapping the intent.

WHICH OF THE TWO IS TAKEN HERE, AND WHY.  A static walk over serialised HTML CANNOT decide
what a browser paints: that needs the CSS cascade, layout, and whatever JavaScript does after
load.  So the claimed property is not measurable by any instrument of this kind, and the
honest repair is the second one — NARROW THE CLAIM TO THE MEASURED ONE, and make the measured
one large enough to be worth having.  Every row of this file is named
`not-suppressed-by-any-mechanism-in-the-declared-set`.  THE PHRASE "SHOWN TO A READER" DOES
NOT APPEAR AS A COLUMN HEADING ANYWHERE IN THIS FILE.

WHAT IS WRONG WITH THE INSTRUMENT THIS REPLACES, MEASURED AND NOT ARGUED.  `render16eb.py`
computes its `SHOWN TO A READER` column as: the section's text survives tag-stripping, MINUS
the sections that sit inside a `<details>` with no `open` attribute.  One mechanism.  Its
tag-stripping regex `<(/?)([a-zA-Z]...)>` does not match `<!--`, so the contents of an HTML
comment survive it intact.  Rows V1, V3 and V4 below are three documents on which that rule
reports every cited section SHOWN TO A READER and no reader is shown any of them — and V1 is
mg-0049's own R8, the document `render0049.py` scores `ANY 0/5` and `delta_control.py` exits 1
on, calling it damage.  The rule is imported from `render16eb.py` UNMODIFIED and applied by
its own two functions, so the disagreement is a measurement and not a reading.

THE DECLARED SET IS THE POINT AND IT FAILS OPEN.  Five suppression mechanisms are declared,
printed on every run, and a section suppressed by none of them is reported NOT SUPPRESSED —
never "shown".  A mechanism outside the set (a stylesheet, `aria-hidden`, off-screen
positioning, `color: transparent`, JavaScript) makes this instrument report NOT SUPPRESSED for
a section a reader is shown nothing of.  That is the failure mode, it is named on every run,
and it is the reason the column is not called `shown`.

The renderers are installed OUTSIDE the repo and are a dependency of this evidence only,
never of the control:

    D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
    NODE_PATH="$D/node_modules" python3 code/state_delegation_repair_a74f/visible_a74f.py

Without them this exits 3 and prints the install line.  It reuses mg-218d's renderer BRIDGE
(`render218d.js`) unmodified, as mg-5644, mg-0049 and mg-16eb did, for the reason they gave.
"""
import html
import os
import re
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                       capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, os.path.join(_REPO, "code/state_delegation_audit_16eb"))
sys.path.insert(0, os.path.join(_REPO, "code/state_delegation_repair_0049"))

import mutations16eb as M16          # noqa: E402
import mutations_0049 as M49         # noqa: E402
import render16eb as R16             # noqa: E402   the instrument under test, UNMODIFIED

ENGINES = ["marked", "markdown-it"]
CITED = ["H1", "H2", "H3", "H4", "H5"]

# =========================================================================================
# THE DECLARED SET.  A section is SUPPRESSED iff one of these holds of the position its
# marker occupies in the serialised HTML.  Each is a property of the markup alone, decidable
# without a CSS cascade and without layout, which is why each is in the set.
# =========================================================================================
DECLARED = [
    ("S1", "inside a <details> element carrying no `open` attribute"),
    ("S2", "inside an HTML comment (terminated or running to the end of the document)"),
    ("S3", "inside the content of a <script>, <style>, <template> or <textarea>"),
    ("S4", "inside an element carrying the `hidden` attribute"),
    ("S5", "inside an element whose inline style sets display:none or visibility:hidden"),
]

# What the declared set does NOT cover.  Every one of these suppresses content in a real
# browser and every one of them is scored NOT SUPPRESSED by this file.  This instrument
# FAILS OPEN, and this list is the shape of the failure.
NOT_COVERED = [
    "any rule from an external or embedded stylesheet, including `display:none` on a class",
    "`aria-hidden`, `inert`, and anything else that hides from a subset of readers",
    "off-screen positioning, zero size, `clip`, `overflow:hidden`, `opacity:0`",
    "`color: transparent` and any other paint the text in the page's own background",
    "anything JavaScript does to the DOM after load, including `<noscript>` branches",
    "media queries, print stylesheets, and anything conditional on the reader's device",
    "the difference between shown and shown YET — scrolling, clicking, a second tab",
]

_TAG = re.compile(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)([^>]*)>")
_VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
         "param", "source", "track", "wbr"}
_RAWTEXT = {"script": "S3", "style": "S3", "template": "S3", "textarea": "S3"}


def raw_regions(doc):
    """[(start, end, mechanism)] — spans whose bytes no reader is shown whatever surrounds
    them.  Comments and raw-text element contents.  An unterminated one runs to the end of
    the document, which is the browser's own rule and is the case mg-5644's Q1 is."""
    out, i, n = [], 0, len(doc)
    while i < n:
        c = doc.find("<!--", i)
        r = None
        for name in _RAWTEXT:
            m = re.compile(r"<%s\b[^>]*>" % name, re.I).search(doc, i)
            if m and (r is None or m.start() < r[0].start()):
                r = (m, name)
        if c < 0 and r is None:
            break
        if r is None or (c >= 0 and c < r[0].start()):
            end = doc.find("-->", c + 4)
            out.append((c, n if end < 0 else end + 3, "S2"))
            i = n if end < 0 else end + 3
        else:
            m, name = r
            close = re.compile(r"</%s\s*>" % name, re.I).search(doc, m.end())
            out.append((m.start(), n if close is None else close.end(), _RAWTEXT[name]))
            i = n if close is None else close.end()
    return out


def suppressors(doc, pos):
    """The mechanisms of the DECLARED set that suppress the byte at `pos`.  A tag-stack walk
    over the tags that are not themselves inside a comment or a raw-text element, because a
    `<div>` written inside a comment opens nothing."""
    regions = raw_regions(doc)
    found = [m for s, e, m in regions if s <= pos < e]
    stack = []
    for t in _TAG.finditer(doc):
        if t.start() >= pos:
            break
        if any(s <= t.start() < e for s, e, _m in regions):
            continue
        closing, name, attrs = t.group(1), t.group(2).lower(), t.group(3)
        if closing:
            for k in range(len(stack) - 1, -1, -1):
                if stack[k][0] == name:
                    del stack[k:]
                    break
        elif name not in _VOID and not attrs.rstrip().endswith("/"):
            stack.append((name, attrs))
    for name, attrs in stack:
        if name == "details" and not re.search(r"(?<![-\w])open(?![-\w])", attrs):
            found.append("S1")
        if re.search(r"(?<![-\w])hidden(?![-\w])", attrs):
            found.append("S4")
        style = re.search(r'style\s*=\s*"([^"]*)"', attrs) or \
            re.search(r"style\s*=\s*'([^']*)'", attrs)
        if style and re.search(r"display\s*:\s*none|visibility\s*:\s*hidden",
                               style.group(1), re.I):
            found.append("S5")
    seen, ordered = set(), []
    for m in found:
        if m not in seen:
            seen.add(m)
            ordered.append(m)
    return sorted(ordered)


# =========================================================================================
# THE FIVE DOCUMENTS.  V1 and V2 are not new: V1 is mg-0049's own R8 and V2 is mg-16eb's own
# B3, both imported from their authors' modules rather than rewritten, so no row here can be
# said to have been shaped to make a point.  V3 and V4 are new and are the two mechanisms
# nobody in this lineage has put to an instrument.
# =========================================================================================
def v3_hidden_div(t):
    """`<div hidden>` at the top of the target, never closed.  `hidden` is a global HTML
    attribute and the UA stylesheet gives it `display: none`; every cited section is a
    descendant of it and a reader is shown a blank page."""
    return "<div hidden>\n\n" + t


def v4_display_none_div(t):
    """`<div style="display:none">` at the top of the target, never closed.  The same blank
    page by the other of the two routes a browser takes to it."""
    return '<div style="display:none">\n\n' + t


# (id, what, mutation, predicted bytes-in-html, predicted not-suppressed,
#  predicted render16eb SHOWN)  — every figure written before the run except V1's, which
# PREDICTIONS.md discloses as probed.
ROWS = [
    ("V0", "unmutated — the positive control", lambda t: t, 5, 5, 5),
    ("V1", "the whole file inside a CLOSED HTML comment (mg-0049's own R8)",
     M49.r8_whole_file_commented_closed, 5, 0, 5),
    ("V2", "<details><summary> at the top, never closed (mg-16eb's own B3)",
     M16.b3_details_with_summary, 5, 0, 0),
    ("V3", "<div hidden> at the top, never closed", v3_hidden_div, 5, 0, 5),
    ("V4", '<div style="display:none"> at the top, never closed', v4_display_none_div,
     5, 0, 5),
]


def render16eb_shown(out):
    """mg-16eb's OWN rule, computed with mg-16eb's OWN functions, imported unmodified.

    Lifted line for line out of `render16eb.py`'s `main()`: strip the tags, ask which cited
    sections survive, subtract the ones behind a closed `<details>`.  Nothing here is a
    paraphrase of it — `R16.visible_text` and `R16.closed_details_ancestors` are the two
    functions that file uses and they are called, not reimplemented."""
    vis = R16.visible_text(out)
    in_html = [h for h in CITED if re.search(r"\b%s — " % h, vis)]
    behind = {}
    for h in CITED:
        m = re.search(r"<h[1-6][^>]*>\s*%s\b" % h, out, re.I)
        if m:
            behind[h] = len(R16.closed_details_ancestors(out, out[m.start():m.start() + 4]))
    return [h for h in in_html if behind.get(h, 0) == 0]


def marker(name):
    return "%s — " % name


def main():
    if not os.path.exists(R16.BRIDGE):
        print(f"renderer bridge not found: {R16.BRIDGE}")
        return 3
    probe = subprocess.run(["node", R16.BRIDGE, "marked", os.devnull],
                           capture_output=True, text=True)
    if probe.returncode != 0:
        print("The two GFM renderers are not installed.  This evidence needs them; the")
        print("control does not.  Install them outside the repo and re-run:")
        print('    D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it')
        print('    NODE_PATH="$D/node_modules" python3 '
              "code/state_delegation_repair_a74f/visible_a74f.py")
        return 3

    orig = M49.original()
    for name in CITED:
        if orig.count(marker(name)) != 1:
            raise LookupError(f"{marker(name)!r} occurs {orig.count(marker(name))} times in "
                              f"the target, need exactly 1 — this row has rotted")

    print("=" * 100)
    print("mg-a74f — SUPPRESSION, MEASURED; VISIBILITY, NOT CLAIMED")
    print("=" * 100)
    print(f"Population: {len(ROWS)} documents x {len(ENGINES)} renderers x {len(CITED)} "
          f"cited sections = {len(ROWS) * len(ENGINES) * len(CITED)} section observations.")
    print()
    print("THE DECLARED SET — a section is SUPPRESSED iff one of these holds, and NOT")
    print("SUPPRESSED otherwise.  This is the whole of what this instrument measures:")
    for sid, what in DECLARED:
        print(f"    {sid}   {what}")
    print()
    print("WHAT THE DECLARED SET DOES NOT COVER.  Each of these suppresses content in a real")
    print("browser and each is scored NOT SUPPRESSED here.  THIS INSTRUMENT FAILS OPEN:")
    for what in NOT_COVERED:
        print(f"    -   {what}")
    print()
    print("COLUMNS.  `bytes-in-html` is the section marker present in the serialised HTML —")
    print("the property `render0049.py` and `render16eb.py` both actually measure.")
    print("`not-suppressed` is the marker present AND suppressed by no mechanism above.")
    print("`r16 SHOWN` is mg-16eb's own rule, computed by importing render16eb.py unmodified")
    print("and calling its own two functions.  No column here is named `shown to a reader`.")
    print()

    bad = 0
    obs = 0
    disagree = []
    for rid, what, fn, p_bytes, p_free, p_r16 in ROWS:
        text = fn(orig)
        print(f"{rid}  {what}")
        for engine in ENGINES:
            out = R16.render(engine, text)
            present = [h for h in CITED if marker(h) in html.unescape(out)]
            mech = {h: suppressors(out, html.unescape(out).index(marker(h)))
                    for h in present}
            free = [h for h in present if not mech[h]]
            r16 = render16eb_shown(out)
            obs += len(CITED)
            allmech = sorted({m for v in mech.values() for m in v})
            print(f"    {engine:<12s} bytes-in-html {len(present)}/5   "
                  f"not-suppressed {len(free)}/5   "
                  f"by {'+'.join(allmech) if allmech else '(nothing)':<9s}   "
                  f"r16 SHOWN {len(r16)}/5")
            miss = []
            if len(present) != p_bytes:
                miss.append(f"bytes-in-html predicted {p_bytes}")
            if len(free) != p_free:
                miss.append(f"not-suppressed predicted {p_free}")
            if len(r16) != p_r16:
                miss.append(f"r16 SHOWN predicted {p_r16}")
            if miss:
                print(f"                 !! {'; '.join(miss)}")
                bad += 1
            if len(free) != len(r16):
                disagree.append((rid, engine, len(free), len(r16)))
        print()

    print("=" * 100)
    print("WHERE THE TWO INSTRUMENTS DISAGREE, AND WHICH ONE IS WRONG")
    print("=" * 100)
    if not disagree:
        print("  (none)")
    for rid, engine, free, r16 in disagree:
        print(f"  {rid} / {engine:<12s} not-suppressed {free}/5   r16 SHOWN {r16}/5")
    print()
    print("  V1 IS THE ROW THAT SETTLES IT.  It is mg-0049's own R8, unedited: the whole")
    print("  target inside a CLOSED HTML comment.  mg-0049's render0049.py scores it ANY 0/5")
    print("  and HEADING 0/5 on both renderers; delta_control.py exits 1 on it and calls it")
    print("  damage; mg-16eb's own audit calls it 'R1's and R8's blank page'.  Every party in")
    print("  this arc agrees a reader is shown nothing.  mg-16eb's SHOWN TO A READER rule")
    print("  scores it 5 of 5, because its tag-stripping regex requires a letter after `<`")
    print("  and `<!--` has a `!`, so the comment's contents survive the strip and its one")
    print("  suppression mechanism is <details>, which a comment is not.")
    print()
    print("  V3 AND V4 ARE THE SAME DEFECT ON MECHANISMS NOBODY IN THIS ARC HAS USED.  A")
    print("  `hidden` attribute and an inline `display:none` each produce the same blank")
    print("  page and each is scored 5 of 5 SHOWN by that rule.")
    print()
    print("  V2 IS THE ROW IT GETS RIGHT, and it is the only shape it was written against.")
    print()
    print("=" * 100)
    print("DOES EACH ROW OF THIS FILE MEASURE THE PROPERTY ITS NAME CLAIMS?  (mg-16eb OPEN 3)")
    print("=" * 100)
    print("  bytes-in-html    names bytes; measures bytes.  MATCHES.")
    print("  not-suppressed   names 'suppressed by no mechanism in the declared set';")
    print("                   measures exactly that, over the set printed above.  MATCHES,")
    print("                   and it is weaker than 'shown to a reader' BY CONSTRUCTION —")
    print("                   the NOT COVERED list above is the size of the gap.")
    print("  r16 SHOWN        names what a reader is shown; measures bytes-in-html minus one")
    print("                   mechanism.  DOES NOT MATCH.  That is this file's finding, and")
    print("                   the column keeps mg-16eb's own name for it so the mismatch is")
    print("                   legible rather than laundered.")
    print()
    print(f"  {obs} section observations; {bad} renderer rows where this file and its own")
    print(f"  committed prediction disagree; {len(disagree)} of "
          f"{len(ROWS) * len(ENGINES)} renderer rows where this file and mg-16eb's rule")
    print("  disagree.")
    print("=" * 100)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
