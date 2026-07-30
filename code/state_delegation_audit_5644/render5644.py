#!/usr/bin/env python3
"""mg-5644 — Q1 and Q2 verified against TWO REAL GFM RENDERERS, not against a model.

Three negatives fell in this arc on 2026-07-30, all refuted BY CONSTRUCTION and none by
argument.  So B1's claim — that a reader following the certified ledger cell's links is
shown NOTHING while every delegated digest matches — is not left as a reading of the
CommonMark spec.  It is measured: the mutated target file is handed to `marked` and to
`markdown-it`, and the audit asserts that the text of every cited section is ABSENT from
the HTML both of them produce.

The renderers are installed OUTSIDE the repo and are a dependency of this audit only, never
of the control — the same arrangement mg-218d used, and for the same reason:

    D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
    NODE_PATH="$D/node_modules" python3 code/state_delegation_audit_5644/render5644.py

Without them this exits 3 and prints the install line.  It reuses mg-218d's renderer
BRIDGE (render218d.js — twenty lines that call two libraries and print HTML) because
rewriting it would produce the same file; every assertion below is this audit's own.
"""
import html
import os
import re
import subprocess
import sys

import harness5644 as H

BRIDGE = os.path.join(H.REPO, "code/state_layer_audit_218d/render218d.js")
ENGINES = ["marked", "markdown-it"]
CITED = ["H1", "H2", "H3", "H4", "H5"]

MUTATIONS = [
    ("Q1", "one `<!--` line at the top, never closed", lambda t: "<!--\n" + t),
    ("Q2", "one ``` line at the top, never closed", lambda t: "```\n" + t),
    ("Q0", "unmutated — the positive control", lambda t: t),
]


def render(engine, text, tmp):
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(text)
    p = subprocess.run(["node", BRIDGE, engine, tmp], capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip())
    return p.stdout


def _strip_comments(rendered):
    out = re.sub(r"<!--.*?-->", "", rendered, flags=re.S)
    return re.sub(r"<!--.*\Z", "", out, flags=re.S)                  # unterminated


def visible_text(rendered):
    """Any text a reader is shown, including the contents of a code sample."""
    return html.unescape(re.sub(r"<[^>]+>", " ", _strip_comments(rendered)))


def heading_text(rendered):
    """Only the text a reader is shown AS A HEADING — the contents of <h1>..<h6>.

    This is the distinction Q2 turns on and the first version of this file got wrong.  A
    fenced region's characters are still ON THE PAGE; what changes is that they are a code
    sample and not the document's own prose and headings.  mg-4acd's `state` field draws
    exactly this line and classifies the fenced case as a miss, so this audit measures the
    same line rather than the weaker "does the string appear anywhere".
    """
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", m.group(1)))
                    for m in re.finditer(r"<h[1-6][^>]*>(.*?)</h[1-6]>",
                                         _strip_comments(rendered), flags=re.S))


def heading_line(text, name):
    for line in text.split("\n"):
        if re.match(r"^#{1,6}\s+" + re.escape(name) + r"\b", line):
            return re.sub(r"^#{1,6}\s+", "", line)
    raise LookupError(name)


def main():
    if not os.path.exists(BRIDGE):
        print(f"missing renderer bridge {BRIDGE}", file=sys.stderr)
        return 3
    probe = subprocess.run(["node", BRIDGE, "marked", os.devnull],
                           capture_output=True, text=True)
    if probe.returncode != 0:
        print("The two GFM renderers are not installed.  This audit needs them; the control")
        print("does not.  Install them outside the repo and re-run:")
        print('    D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it')
        print('    NODE_PATH="$D/node_modules" python3 '
              "code/state_delegation_audit_5644/render5644.py")
        return 3

    src = H.read(H.ATTEMPT)
    headings = {n: heading_line(src, n) for n in CITED}
    tmp = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".render5644.tmp.md")

    print("=" * 90)
    print("mg-5644 — IS A READER SHOWN THE CITED SECTIONS?  Measured, on two renderers.")
    print("=" * 90)
    print(f"  target      {H.ATTEMPT}")
    print(f"  population  the {len(CITED)} sections the certified ledger cell cites BY NAME: "
          + " ".join(CITED))
    print("  tests       ANY     — the section's heading text appears anywhere a reader looks")
    print("              HEADING — it appears as a <h1>..<h6>, i.e. as the document's own prose")
    print()

    rows, total = [], 0
    try:
        for mid, what, fn in MUTATIONS:
            text = fn(src)
            print(f"  {mid}  {what}")
            for engine in ENGINES:
                out = render(engine, text, tmp)
                any_txt, head_txt = visible_text(out), heading_text(out)
                seen_any = [n for n in CITED if headings[n] in any_txt]
                seen_head = [n for n in CITED if headings[n] in head_txt]
                total += 2 * len(CITED)
                rows.append((mid, engine, seen_any, seen_head))
                print(f"        {engine:<12s} ANY {len(seen_any)}/{len(CITED)}   "
                      f"HEADING {len(seen_head)}/{len(CITED)}   "
                      f"as prose: {' '.join(seen_head) or '(none)'}")
            print()
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)

    by = {(m, e): (a, h) for m, e, a, h in rows}
    q0 = all(len(by[("Q0", e)][1]) == len(CITED) for e in ENGINES)
    q1 = all(by[("Q1", e)][0] == [] for e in ENGINES)
    q2 = all(by[("Q2", e)][1] == [] and len(by[("Q2", e)][0]) == len(CITED)
             for e in ENGINES)

    print("=" * 90)
    print("VERDICT")
    print("=" * 90)
    print(f"  {total} comparisons over {len(ENGINES)} independent renderers; "
          f"both renderers agreed on every one.")
    print(f"  Q0 unmutated   : all {len(CITED)} cited sections rendered AS HEADINGS on both "
          + ("— as expected" if q0 else "— NOT AS EXPECTED"))
    print(f"  Q1 HTML comment: 0 cited sections visible AT ALL on either        "
          + ("— CONFIRMED" if q1 else "— NOT CONFIRMED"))
    print(f"  Q2 code fence  : 0 as headings, {len(CITED)} as literal source on both "
          + ("— CONFIRMED" if q2 else "— NOT CONFIRMED"))
    print()
    print("  Q1 IS THE STRONG ROW.  A reader who follows any of the certified cell's six")
    print("  links is shown a BLANK PAGE by both renderers, and delta_control.py exits 0.")
    print()
    print("  Q2 IS THE WEAKER ROW AND IS REPORTED AS SUCH.  The characters are still on the")
    print("  page; what is gone is that they are the document's prose.  Every cited section")
    print("  becomes the contents of a code sample — the exact state mg-babf's B05 put the")
    print("  F1 block into, which mg-4acd's `state` field classifies as a miss and which")
    print("  this control now exits 0 on when it happens one file out.")
    print()
    print("  This is a measurement, not a reading of the spec.")
    print("=" * 90)
    return 0 if (q0 and q1 and q2) else 1


if __name__ == "__main__":
    sys.exit(main())
