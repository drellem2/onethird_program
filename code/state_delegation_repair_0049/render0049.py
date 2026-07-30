#!/usr/bin/env python3
"""mg-0049 — THE FIVE NEW ROWS PUT TO TWO REAL GFM RENDERERS.

mg-5644 measured R1 and R2 (its Q1 and Q2) this way and this repair does not re-litigate
them; `run_all.sh` re-runs mg-5644's own `render5644.py` unmodified for those.  What is
measured HERE is the set of claims this repair makes that nobody has measured yet, and every
one of them is a claim about what a reader is shown:

    R8  a CLOSED comment around the whole file shows a reader nothing, exactly as R1's
        unclosed one does — so exiting 1 on it is not an artefact of malformed input
    R5  `<details>` at the top SUPPRESSES NOTHING: every cited section is still on the page
        as the document's own prose.  This repair fires on it from the raw-HTML guard alone
        and says so; if the renderers disagreed, the guard would be a false positive and the
        row would be reported as one
    R6  the cited sections under an "Appendix Z — nothing below is in force" heading are
        STILL SHOWN.  The catch is the heading path, not suppression, and the measurement is
        what separates those two claims
    R9  one tab in an uncited paragraph changes NOTHING a reader sees.  It exits 2 anyway.
        That is the running cost of default-deny and it is measured rather than conceded

A row where the model and the renderers disagree is a defect in the model, and this file
exits non-zero on one.  The renderers are installed OUTSIDE the repo and are a dependency of
this evidence only, never of the control:

    D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
    NODE_PATH="$D/node_modules" python3 code/state_delegation_repair_0049/render0049.py

Without them this exits 3 and prints the install line; every other section of `run_all.sh`
is unaffected.  It reuses mg-218d's renderer BRIDGE (`render218d.js`) for the same reason
mg-5644 did: rewriting twenty lines that call two libraries would produce the same file.
"""
import html
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mutations_0049 as M          # noqa: E402

BRIDGE = os.path.join(M.REPO, "code/state_layer_audit_218d/render218d.js")
ENGINES = ["marked", "markdown-it"]
CITED = ["H1", "H2", "H3", "H4", "H5"]

# (id, what, mutation, cited sections expected VISIBLE AT ALL, expected AS HEADINGS)
ROWS = [
    ("R0", "unmutated — the positive control", lambda t: t, 5, 5),
    ("R8", "the whole file inside a CLOSED HTML comment", M.r8_whole_file_commented_closed,
     0, 0),
    ("R5", "a <details> wrapper at the top", M.r5_details_wrapper, 5, 5),
    ("R6", "an 'Appendix Z — nothing below is in force' heading above H1",
     M.r6_appendix_heading_above_h1, 5, 5),
    ("R9", "one tab in the target's uncited opening paragraph", M.r9_tab_in_uncited_prose,
     5, 5),
]

# What delta_control.py does about each row, from battery_0049.py's measured exit codes.
CONTROL = {"R0": "exit 0", "R8": "exit 1 (FAIL)", "R5": "exit 2 (MOVED)",
           "R6": "exit 2 (MOVED)", "R9": "exit 2 (MOVED)"}


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
    """Only the text shown AS A HEADING — the same line mg-5644's file draws, restated so
    the two measurements are of the same thing."""
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
        print("The two GFM renderers are not installed.  This evidence needs them; the")
        print("control does not.  Install them outside the repo and re-run:")
        print('    D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it')
        print('    NODE_PATH="$D/node_modules" python3 '
              "code/state_delegation_repair_0049/render0049.py")
        return 3

    src = M.original()
    headings = {n: heading_line(src, n) for n in CITED}
    tmp = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".render0049.tmp.md")

    print("=" * 92)
    print("mg-0049 — WHAT A READER IS SHOWN UNDER THIS REPAIR'S FIVE NEW ROWS")
    print("=" * 92)
    print(f"  target      {M.ATTEMPT}")
    print(f"  population  the {len(CITED)} sections the certified ledger cell cites BY NAME: "
          + " ".join(CITED))
    print("  tests       ANY     — the section's heading text appears anywhere a reader looks")
    print("              HEADING — it appears as <h1>..<h6>, i.e. as the document's own prose")
    print(f"  engines     {', '.join(ENGINES)}, independent implementations")
    print()

    total, wrong, agree = 0, [], True
    try:
        for rid, what, fn, want_any, want_head in ROWS:
            text = fn(src)
            print(f"  {rid}  {what}    (delta_control.py: {CONTROL[rid]})")
            seen = {}
            for engine in ENGINES:
                out = render(engine, text, tmp)
                any_txt, head_txt = visible_text(out), heading_text(out)
                seen_any = [n for n in CITED if headings[n] in any_txt]
                seen_head = [n for n in CITED if headings[n] in head_txt]
                seen[engine] = (seen_any, seen_head)
                total += 2 * len(CITED)
                ok = len(seen_any) == want_any and len(seen_head) == want_head
                if not ok:
                    wrong.append((rid, engine, len(seen_any), len(seen_head)))
                print(f"        {engine:<12s} ANY {len(seen_any)}/{len(CITED)}   "
                      f"HEADING {len(seen_head)}/{len(CITED)}   "
                      f"expected ANY {want_any} HEADING {want_head}   "
                      f"{'ok' if ok else 'NOT AS PREDICTED'}")
            if len({(tuple(a), tuple(h)) for a, h in seen.values()}) != 1:
                agree = False
                print("        >>> THE TWO RENDERERS DISAGREE on this row")
            print()
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)

    print("=" * 92)
    print("VERDICT")
    print("=" * 92)
    print(f"  {total} comparisons over {len(ENGINES)} independent renderers; they agreed on "
          + ("every one." if agree else "NOT every one — see the rows above."))
    print(f"  {len(wrong)} rows did not match what this repair predicted"
          + ("." if not wrong else f": {wrong}"))
    print()
    print("  R8 CONFIRMS that the blank page is not about the comment being unclosed: a")
    print("  well-formed comment around the whole document shows a reader nothing either,")
    print("  and this repair exits 1 on it.")
    print()
    print("  R5, R6 AND R9 ARE THE HONEST HALF.  In all three, every cited section is still")
    print("  on the page, as the document's own prose, on both renderers — and the control")
    print("  exits 2.  It is right to: R5 puts raw HTML the model does not resolve around")
    print("  the certified surface, and R6 puts every cited section under a heading that")
    print("  says nothing below it is in force, which is what a reader reads.  R9 is a pure")
    print("  cost — a tab a reader cannot see, re-baselined at exit 2 — and it is printed")
    print("  here rather than left for the next auditor to find.")
    print("=" * 92)
    return 0 if (agree and not wrong) else 1


if __name__ == "__main__":
    sys.exit(main())
