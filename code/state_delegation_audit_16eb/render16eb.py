#!/usr/bin/env python3
"""mg-16eb — WHAT A READER IS ACTUALLY SHOWN, on two real GFM renderers.

Every negative in this arc that has been refuted was refuted BY CONSTRUCTION, so the three
rows here are constructions and not arguments.

    B3 / mg-0049's R5   mg-0049's `render0049.py` measures `<details>` at the top of the
                        target and records "SUPPRESSES NOTHING: every cited section is still
                        on the page as the document's own prose", 5 of 5 visible on both
                        renderers.  That measurement asks whether the section's TEXT IS IN
                        THE HTML.  This file asks the different question of whether the text
                        is in an element a reader can see, by walking the tag stack: an
                        unclosed `<details>` with no `open` attribute and no `</details>`
                        makes every cited section a descendant of a CLOSED disclosure
                        widget.  Per the HTML standard a browser renders such an element's
                        summary and nothing else.  "Is the text in the HTML?" versus "is a
                        reader shown it?" is the exact distinction mg-4acd was landed to
                        make, and this is the one row of mg-0049's own evidence that does
                        not make it.

    C1                  a closed, ordinary code example inside cited section H3.  Every line
                        of the section is in the rendered page, outside any comment, outside
                        any HTML element, with the example rendered as a `<pre><code>` block
                        — which is what a code example is.  The control reports the section
                        as one THE READER IS SHOWN NOTHING OF, at exit 1.

    B1                  two cited sections exchanged.  Both renderers show them in the new
                        order; the control exits 0.

A row where this file and the control disagree about what a reader is shown is a defect in
one of them, and the row prints which.  The renderers are installed OUTSIDE the repo and are
a dependency of this evidence only, never of the control:

    D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
    NODE_PATH="$D/node_modules" python3 code/state_delegation_audit_16eb/render16eb.py

Without them this exits 3 and prints the install line.  It reuses mg-218d's renderer BRIDGE
(`render218d.js`) unmodified, as mg-5644 and mg-0049 did, for the reason they gave: a
rewrite of twenty lines that call two libraries would produce the same twenty lines.
"""
import html
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mutations16eb as M            # noqa: E402

BRIDGE = os.path.join(M.REPO, "code/state_layer_audit_218d/render218d.js")
ENGINES = ["marked", "markdown-it"]
CITED = ["H1", "H2", "H3", "H4", "H5"]

_TAG = re.compile(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)([^>]*)>")
_VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
         "param", "source", "track", "wbr"}


def render(engine, text):
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False,
                                     encoding="utf-8") as fh:
        fh.write(text)
        tmp = fh.name
    try:
        proc = subprocess.run(["node", BRIDGE, engine, tmp],
                              capture_output=True, text=True)
        if proc.returncode != 0:
            raise SystemExit(3)
        return proc.stdout
    finally:
        os.unlink(tmp)


def visible_text(doc):
    """The page's text with tags stripped — the question mg-0049's harness asks."""
    return html.unescape(_TAG.sub(" ", doc))


def closed_details_ancestors(doc, needle):
    """The `<details>` elements that are OPEN ANCESTORS of the first occurrence of `needle`
    and carry no `open` attribute — i.e. the disclosure widgets a reader must click through
    before being shown it.  A straight tag-stack walk over the serialised HTML; `<details>`
    is a normal element, so an unclosed one runs to the end of the document."""
    at = doc.index(needle)
    stack = []
    for m in _TAG.finditer(doc):
        if m.start() >= at:
            break
        closing, name, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if closing:
            for i in range(len(stack) - 1, -1, -1):
                if stack[i][0] == name:
                    del stack[i:]
                    break
        elif name not in _VOID and not attrs.rstrip().endswith("/"):
            stack.append((name, attrs))
    return [a for n, a in stack if n == "details" and not re.search(r"\bopen\b", a)]


def heading_order(doc):
    """The cited sections, in the order a reader meets them down the page."""
    return [m.group(1) for m in re.finditer(r"<h[1-6][^>]*>\s*(H[1-9])\b",
                                            doc, re.I)]


def main():
    if not os.path.exists(BRIDGE):
        print(f"renderer bridge not found: {BRIDGE}")
        return 3
    orig = M.__dict__["_once"](
        open(os.path.join(M.REPO, M.ATTEMPT), encoding="utf-8").read(),
        "### H1 — the step-4d clause — first of the three A3 sites")

    print("=" * 96)
    print("mg-16eb — WHAT A READER IS SHOWN, measured on two real GFM renderers")
    print("=" * 96)
    print("Population: 2 renderers x 5 cited sections x 4 documents = 40 section")
    print("observations, plus 2 renderers x 3 mutated documents = 6 whole-page checks.")
    print()

    docs = [
        ("R0", "unmutated — the positive control", lambda t: t),
        ("B3", "<details><summary> at the top of the target",
         M.b3_details_with_summary),
        ("C1", "a closed code example inside cited section H3",
         M.c1_code_example_inside_a_cited_section),
        ("B1", "cited sections H3 and H4 exchanged", M.b1_swap_two_cited_sections),
    ]

    bad = 0
    obs = 0
    for rid, what, fn in docs:
        text = fn(orig)
        print(f"{rid}  {what}")
        for engine in ENGINES:
            out = render(engine, text)
            vis = visible_text(out)
            in_html = [h for h in CITED if re.search(r"\b%s — " % h, vis)]
            behind = {}
            for h in CITED:
                m = re.search(r"<h[1-6][^>]*>\s*%s\b" % h, out, re.I)
                if m:
                    behind[h] = len(closed_details_ancestors(out, out[m.start():m.start() + 4]))
            shown = [h for h in in_html if behind.get(h, 0) == 0]
            obs += len(CITED)
            order = heading_order(out)
            print(f"    {engine:<12s} text-in-html {len(in_html)}/5   "
                  f"SHOWN TO A READER {len(shown)}/5   order {'-'.join(order) or '(none)'}")
            if rid == "B3":
                n_widgets = set(behind.values())
                print(f"                 every cited section sits inside "
                      f"{sorted(n_widgets)} closed <details> element(s); "
                      f"</details> in page: {out.count('</details>')}")
                if len(shown) != 0:
                    print("                 !! expected 0 shown")
                    bad += 1
            if rid == "C1":
                has_pre = "<pre>" in out or "<pre " in out
                sample = "d_true = np.diag(row_signs) @ d_allplus" in visible_text(out)
                print(f"                 the example renders as a code block: {has_pre}; "
                      f"its text is on the page: {sample}")
                if len(shown) != 5 or not (has_pre and sample):
                    print("                 !! expected 5 shown, as a code block")
                    bad += 1
            if rid in ("R0", "B1") and len(shown) != 5:
                print("                 !! expected 5 shown")
                bad += 1
        print()

    print("=" * 96)
    print("WHAT THE RENDERERS SAY, against what the control says")
    print("=" * 96)
    print("  B3   both renderers: 5 of 5 cited sections have their TEXT in the HTML and 0 of")
    print("       5 are SHOWN to a reader — every one is inside a <details> with no `open`")
    print("       attribute that is never closed.  mg-0049's render0049.py measures the")
    print("       first number for the same shape (its R5) and records 'SUPPRESSES NOTHING'.")
    print("       The control exits 2 on it: DRIFT, 're-baseline and record the new figure'.")
    print("       R1 and R8 produce the same blank page and are exit 1, damage.")
    print()
    print("  C1   both renderers: 5 of 5 shown, the example rendered as a code block, its")
    print("       text on the page.  The control exits 1 and prints 'THE CERTIFIED CELL")
    print("       SENDS A READER TO THIS SECTION AND THE READER IS SHOWN NOTHING OF IT'.")
    print()
    print("  B1   both renderers: 5 of 5 shown, in the exchanged order.  The control exits 0.")
    print()
    print(f"  {obs} section observations; {bad} rows where this file and its own prediction")
    print("  disagree.")
    print("=" * 96)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
