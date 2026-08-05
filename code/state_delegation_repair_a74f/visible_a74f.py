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

    IT DID NOT FAIL OPEN WHEN THIS PARAGRAPH WAS FIRST WRITTEN, AND mg-5f7c IS THE REPAIR.
    mg-65eb put `<div class="hidden">` — a CLASS named hidden, in a document with no
    stylesheet, every section of which a reader is shown in full — to this file and got
    `not-suppressed 0/5` on both engines.  A FAILURE IN THE CLOSED DIRECTION, in the only
    instrument in this repository that measures suppression, under a docstring and a README
    that both said it fails open.  The same run found `<details title="open me">` scoring
    `5/5` when DECLARED S1 holds of it.  One bug, both directions: `open` and `hidden` were
    matched as WORDS ANYWHERE IN THE ATTRIBUTE TEXT, values included, so a class named
    `hidden` was read as the `hidden` attribute and the word `open` inside a `title` was read
    as the `open` attribute.  Attributes are now PARSED BY NAME (`parse_attrs`), and
    `polarity_5f7c.py` runs this file's `suppressors` beside the one at `6fb424f` on the
    documents that separate them.

    WHICH WAY IT WAS FIXED, AND WHY IT WAS NOT FIXED THE OTHER WAY.  The two ways to make the
    code and the documents agree are opposite safety postures and only one of them was
    available.  A false SUPPRESSED verdict is this instrument MANUFACTURING EVIDENCE: every
    use it is put to in this arc is refuting another artifact's claim that a reader is shown
    something, so a suppression it reports and cannot justify is a fabricated defect in
    somebody else's document.  A false NOT SUPPRESSED verdict only fails to find one, and the
    whole of what it can miss is printed under NOT_COVERED on every run.  Those costs are not
    symmetric, and the asymmetry is the entire argument for the column being named
    `not-suppressed` rather than `shown`.  The declared set settles it independently: S4 says
    the `hidden` ATTRIBUTE and NOT_COVERED's first line says `display:none` on a class is
    OUTSIDE the set, so the docstring, the README and this file's own printed set all agreed
    with each other and only the code disagreed.  There was no third document to reconcile —
    and no single posture to document either, because the same bug failed closed on one input
    and open on another.

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


def parse_attrs(attrs):
    """[(name, value)] — the attributes of a start tag, BY NAME, lowercased.

    THIS FUNCTION IS mg-5f7c's REPAIR AND THE REASON IS WORTH THE LINES.  What it replaces was
    `re.search(r"(?<![-\\w])hidden(?![-\\w])", attrs)` — the word `hidden` ANYWHERE in the
    attribute text of the tag.  That predicate is true of `class="hidden"`, `id="hidden"`,
    `data-state="hidden"` and `title="the hidden cost"`, none of which is the `hidden`
    attribute and none of which suppresses one byte without a stylesheet to act on it.  The
    same shape read `title="open me"` as a `<details>` carrying `open`.

    A value is a value: nothing inside `"..."`, `'...'` or a bare run of non-space is ever a
    name.  Unquoted values, missing values (boolean attributes) and a trailing `/` are all
    handled, because each of them appears in the output of one of the two real renderers this
    file is run through."""
    out, i, n = [], 0, len(attrs)
    while i < n:
        while i < n and (attrs[i].isspace() or attrs[i] == "/"):
            i += 1
        if i >= n:
            break
        j = i
        while j < n and not attrs[j].isspace() and attrs[j] not in "=/":
            j += 1
        name = attrs[i:j].lower()
        i = j
        while i < n and attrs[i].isspace():
            i += 1
        value = ""
        if i < n and attrs[i] == "=":
            i += 1
            while i < n and attrs[i].isspace():
                i += 1
            if i < n and attrs[i] in "\"'":
                q = attrs[i]
                k = attrs.find(q, i + 1)
                k = n if k < 0 else k
                value, i = attrs[i + 1:k], k + 1
            else:
                k = i
                while k < n and not attrs[k].isspace():
                    k += 1
                value, i = attrs[i:k], k
        if name:
            out.append((name, value))
        elif i == j:                      # nothing consumed: step, or this loops forever
            i += 1
    return out


_CHARREF = re.compile(r"&(#[0-9]+;?|#[xX][0-9a-fA-F]+;?|[^\t\n\f <&#;]{1,32};?)")


def unescape_with_map(s):
    """(text, index) where `text == html.unescape(s)` and `index[k]` is the offset IN `s` of
    the character `text[k]`.

    THIS IS mg-5f7c's OTHER REPAIR.  `main()` used to take `html.unescape(out).index(marker)`
    and spend it as an offset into `out`.  Every entity before the marker makes those two
    strings different lengths — `&amp;` is five bytes of `out` and one of the unescaped
    string — so the walk stopped somewhere earlier than the marker, and on mg-a74f's OWN V3
    blank page with 3000 `&` in front of it, earlier than the `<div hidden>` that suppresses
    it.  A POSITION IN ONE STRING SPENT AS A POSITION IN ANOTHER is the defect class this
    whole arc is about, and it was inside the instrument built to repair it.

    The unescaping is not dropped, because it is load-bearing: a marker a reader is shown as
    `H1 — ` may be `H1 &mdash; ` in the HTML, and `bytes-in-html` is deliberately computed
    over the unescaped text.  What changes is that the offset is now carried back to the
    string it will be spent in instead of being assumed equal to it.  `main()` asserts on
    every document that `text` here is byte for byte `html.unescape(s)`."""
    parts, index, pos = [], [], 0
    for m in _CHARREF.finditer(s):
        parts.append(s[pos:m.start()])
        index.extend(range(pos, m.start()))
        rep = html.unescape(m.group(0))
        parts.append(rep)
        if rep == m.group(0):             # not a reference after all; it stands for itself
            index.extend(range(m.start(), m.end()))
        else:                             # every char of the replacement is AT the `&`
            index.extend([m.start()] * len(rep))
        pos = m.end()
    parts.append(s[pos:])
    index.extend(range(pos, len(s)))
    return "".join(parts), index


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
        # PARSED BY NAME, mg-5f7c.  `class="hidden"` is not the `hidden` attribute and
        # `title="open me"` is not the `open` attribute; see parse_attrs.
        attr = dict(parse_attrs(attrs))
        if name == "details" and "open" not in attr:
            found.append("S1")
        if "hidden" in attr:
            # A BOOLEAN ATTRIBUTE, so any value hides — `hidden=""`, `hidden="hidden"` and
            # even `hidden="false"`.  `hidden="until-found"` hides until a find or a fragment
            # navigation reveals it, which is still suppressed as this file's rows are read.
            found.append("S4")
        if re.search(r"display\s*:\s*none|visibility\s*:\s*hidden",
                     attr.get("style", ""), re.I):
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


# --- mg-5f7c.  FOUR ROWS THAT EXIST TO SHOW THE POLARITY RATHER THAN ASSERT IT.  V5 and V8
# are documents a reader is shown IN FULL and must score NOT SUPPRESSED; V6 and V7 are
# documents a reader is shown NOTHING of and must score SUPPRESSED.  An instrument nobody has
# seen decline to suppress is not evidence of a fail-open posture, and one nobody has seen
# suppress is not evidence of anything at all.  V5, V6 and V7 are mg-65eb's OWN constructions,
# imported in shape rather than quoted, and each was a live defect at 6fb424f.
AMP_PAD = 3000


def v5_class_hidden(t):
    """`<div class="hidden">` at the top — a CLASS named hidden, and NO STYLESHEET anywhere
    in the document.  A browser paints every cited section.  DECLARED S4 is the `hidden`
    ATTRIBUTE and NOT_COVERED's first line puts class-based hiding outside the set, so the
    only answer consistent with this file's own declared set is NOT SUPPRESSED.  At `6fb424f`
    it scored 0/5 — SUPPRESSED — and that is the failure in the CLOSED direction mg-5f7c
    exists to repair."""
    return '<div class="hidden">\n\n' + t


def v6_details_titled(t):
    """`<details title="open me">` — mg-16eb's own B3 with one extra attribute.  It carries no
    `open` attribute, so DECLARED S1 holds of it and a reader is shown a closed widget and no
    cited section.  At `6fb424f` it scored 5/5 NOT SUPPRESSED: the instrument did not
    implement its own declared S1."""
    return '<details title="open me"><summary>Details</summary>\n\n' + t


def v7_amp_padded_hidden(t):
    """V3 — this file's own blank page — behind a paragraph of 3000 `&`.

    Each `&` is one byte of markdown and five (`&amp;`) of HTML, so the unescaped string is
    12000 bytes shorter than the rendered one before the marker is reached.  At `6fb424f` this
    scored 5/5 NOT SUPPRESSED against V3's 0/5 — THE SAME SUPPRESSION, THE SAME MECHANISM, THE
    OPPOSITE ANSWER, decided by punctuation in front of it."""
    return "&" * AMP_PAD + "\n\n<div hidden>\n\n" + t


def v8_stylesheet_class(t):
    """AN EMBEDDED STYLESHEET THAT REALLY DOES HIDE EVERY CITED SECTION, and the instrument
    must report NOT SUPPRESSED anyway.

    This is the first entry of NOT_COVERED — `display:none` on a class — made into a document.
    A browser shows a reader a blank page.  This file scores it 5/5 NOT SUPPRESSED, because
    deciding it needs the CSS cascade and the cascade is outside the declared set by
    construction.  THAT IS THE FAIL-OPEN POSTURE, EXECUTED RATHER THAN CLAIMED, and this row
    goes red the moment the instrument starts scoring an out-of-set mechanism as suppression —
    which is what happened to `class="hidden"` at `6fb424f`."""
    return '<style>.h5f7c { display: none }</style>\n<div class="h5f7c">\n\n' + t


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
    # mg-5f7c.  Predicted before this repair's first run; misses are kept in its README.
    ("V5", '<div class="hidden"> at the top — a CLASS, no stylesheet in the document',
     v5_class_hidden, 5, 5, 5),
    ("V6", '<details title="open me"> — DECLARED S1 holds of it', v6_details_titled,
     5, 0, 5),
    ("V7", f"V3's blank page behind {AMP_PAD} `&` — the same suppression, padded",
     v7_amp_padded_hidden, 5, 0, 5),
    ("V8", '<style> hiding a class that every section is inside — NOT COVERED, on purpose',
     v8_stylesheet_class, 5, 5, 5),
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
    print("THAT SENTENCE WAS FALSE UNTIL mg-5f7c AND IS NOW EXECUTED RATHER THAN CLAIMED.")
    print("At 6fb424f `<div class=\"hidden\">` — the first NOT COVERED entry, in a document")
    print("with no stylesheet — scored 0/5, SUPPRESSED, on both engines: a failure in the")
    print("CLOSED direction under a docstring and a README that both said this instrument")
    print("fails open.  V8 below is that posture made into a standing row: an embedded")
    print("stylesheet that really does blank the page, which this file must and does report")
    print("NOT SUPPRESSED.  V5 is the repaired case and V6 and V7 are the two rows in the")
    print("other direction — a suppression this file must and does find.")
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
    selfcheck = [0]
    for rid, what, fn, p_bytes, p_free, p_r16 in ROWS:
        text = fn(orig)
        print(f"{rid}  {what}")
        for engine in ENGINES:
            out = R16.render(engine, text)
            # mg-5f7c.  The offset is taken in the unescaped text — which is where the marker
            # has to be looked for, because a renderer may write it `H1 &mdash; ` — and then
            # carried back to `out`, which is the string `suppressors` walks.  Before this
            # repair the raw index was spent directly and the walk stopped short by four bytes
            # per entity ahead of the marker.
            unesc, index = unescape_with_map(out)
            if unesc != html.unescape(out):
                raise AssertionError(
                    f"{rid}/{engine}: unescape_with_map does not reproduce html.unescape — "
                    "the offset map cannot be trusted and no row below it is evidence")
            selfcheck[0] += 1
            present = [h for h in CITED if marker(h) in unesc]
            mech = {h: suppressors(out, index[unesc.index(marker(h))]) for h in present}
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
    print("  THE POLARITY, SHOWN IN BOTH DIRECTIONS (mg-5f7c).  V5 and V8 are documents a")
    print("  reader is shown IN FULL and this file DECLINES TO SUPPRESS them; V6 and V7 are")
    print("  documents a reader is shown NOTHING of and this file SUPPRESSES them.  V8's")
    print("  stylesheet really does blank the page and is reported NOT SUPPRESSED anyway —")
    print("  that is the fail-open posture executed, and the row goes red the moment an")
    print("  out-of-set mechanism starts scoring as suppression.")
    print()
    print(f"  unescape_with_map reproduced html.unescape on {selfcheck[0]} of "
          f"{len(ROWS) * len(ENGINES)} documents; a single disagreement raises rather than")
    print("  prints, because an offset map that is wrong makes every row above it not")
    print("  evidence.")
    print()
    print(f"  {obs} section observations; {bad} renderer rows where this file and its own")
    print(f"  committed prediction disagree; {len(disagree)} of "
          f"{len(ROWS) * len(ENGINES)} renderer rows where this file and mg-16eb's rule")
    print("  disagree.")
    print("=" * 100)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
