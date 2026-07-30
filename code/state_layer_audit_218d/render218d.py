#!/usr/bin/env python3
"""mg-218d — THE MODEL AGAINST A REAL RENDERER.  The layer mg-4acd named as uncontrolled.

WHAT THIS TESTS.  `presentation.py` is, in its own words, "a MODEL of a renderer, not a
renderer ... it is NOT measured against an implementation, because there is none here to
measure against", and COVERAGE.md ends the paragraph: "the way to test it is to install a
GFM renderer and compare."  This audit did that.  `marked` (GFM) and `markdown-it`
(CommonMark + the GFM table extension) are installed OUTSIDE the repo and the comparison
is run against both, because agreeing with one renderer is agreeing with one renderer.

    npm install --prefix "$DIR" marked markdown-it
    NODE_PATH="$DIR/node_modules" python3 code/state_layer_audit_218d/render218d.py

THE COMPARISON.  For each certified region a SENTINEL is chosen: the longest run of plain
characters in it that carries no inline markdown, so it survives rendering unchanged.  The
rendered HTML is walked with an element stack, and the sentinel is classified by WHERE it
lands — prose, a table cell, a code sample, or nowhere at all.  That classification is set
beside the `state` the instrument PRINTS for the same region.  Agreement is evidence the
model is right about this document; a disagreement is the failure mode the model's own
header names.

WHAT IT CANNOT DO.  Two renderers agreeing on ~120 blocks of two documents is not a proof
that the model matches GFM in general; it is a measurement over the material the control
actually certifies, plus eight mutations.  It is stated that way and not more.
"""
import html.parser
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness218d as H                                            # noqa: E402

sys.path.insert(0, os.path.join(H.REPO, "code", "state_landing_control_2da3"))
import presentation as pres                                        # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
BRIDGE = os.path.join(HERE, "render218d.js")
ENGINES = ["marked", "markdown-it"]

ATTEMPT = "docs/state-history/attempt-mg-276d.md"

M_F1 = "**`no 4d tally` is a correction"
M_A1_7870 = "DID NOT ESTABLISH WHAT THE BLOCK ABOVE CLAIMS"
H_CERT = "## What certifies a change to these files, and what does not"

CODEISH = {"pre", "code"}
CELLISH = {"td", "th"}


class Walk(html.parser.HTMLParser):
    """Rendered text with the element stack it sits under.  No dependency; stdlib only."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.segments = []          # (text, tuple(stack))

    def handle_starttag(self, tag, attrs):
        if tag not in ("br", "hr", "img"):
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.stack:
            while self.stack and self.stack.pop() != tag:
                pass

    def handle_data(self, data):
        self.segments.append((data, tuple(self.stack)))


def walk(html_text):
    w = Walk()
    w.feed(html_text)
    return w.segments


def render(rel, engine):
    env = dict(os.environ)
    p = subprocess.run(["node", BRIDGE, engine, os.path.join(H.REPO, rel)],
                       capture_output=True, text=True, env=env)
    if p.returncode != 0:
        raise SystemExit(f"renderer {engine} failed:\n{p.stderr.strip()}\n\n"
                         "Install it and re-run:\n"
                         "  npm install --prefix <dir> marked markdown-it\n"
                         "  NODE_PATH=<dir>/node_modules python3 "
                         "code/state_layer_audit_218d/render218d.py")
    return p.stdout


def classify(segments, sentinel):
    """WHERE a sentinel lands in the rendered page."""
    where = set()
    n = 0
    for text, stack in segments:
        if sentinel in text:
            n += text.count(sentinel)
            if CODEISH & set(stack):
                where.add("code-sample")
            elif CELLISH & set(stack):
                where.add("table-cell")
            else:
                where.add("prose")
    if not where:
        return "ABSENT (a reader is shown nothing)", 0
    return "+".join(sorted(where)), n


# `(`, `)`, `/` and `:` are DELIBERATELY excluded.  With them in, the longest run in
# STATE.md:382 was "(https://arxiv.org/abs/2005.08390)), never aimed at the 1/3 gap..." —
# a run that spans a markdown LINK DESTINATION, which is source text a renderer never
# shows.  That produced one "the model says rendered, the renderer says ABSENT" row, and
# it was a defect in THIS instrument and not in presentation.py.  It is recorded here
# rather than quietly deleted, because it is the exact shape of false positive this whole
# lineage exists to keep out of a report.
_PLAIN = re.compile(r"[A-Za-z0-9 ,.;'\-]{40,}")


def sentinel_for(text):
    """The longest run of characters in `text` carrying no inline markdown.

    Must be a literal substring of the SOURCE (so it can be checked for uniqueness there)
    and of the RENDERED text (so its absence means suppression, not transformation).
    """
    runs = [m.group(0).strip() for m in _PLAIN.finditer(text)]
    runs = [r for r in runs if len(r) >= 40]
    if not runs:
        raise LookupError("no markup-free run of 40+ characters in this region")
    return max(runs, key=len)


# -----------------------------------------------------------------------------------------
# The instrument's OWN verdict, read from the output it prints — not from its internals.
# -----------------------------------------------------------------------------------------
_HDR = re.compile(r"^\s*\[(pass|FAIL|MOVED)\]\s+(\S+)\s+—.*?(presentation|PRESENTED)\s*$")


def model_states(control_stdout):
    out = {}
    lines = control_stdout.split("\n")
    for i, line in enumerate(lines):
        m = _HDR.match(line)
        if not m:
            continue
        rid = m.group(2)
        for j in range(i + 1, min(i + 4, len(lines))):
            s = lines[j].strip()
            if s.startswith("state "):
                out[rid] = (m.group(1), s[len("state"):].strip())
                break
    return out


# -----------------------------------------------------------------------------------------
# The regions, and where each one lives.  Restated here, not imported.
# -----------------------------------------------------------------------------------------
REGIONS = [
    ("cell.tree", H.STATE, "row", "mg-276d"),
    ("readme.F2", H.README, "quote",
     "**THOSE FIVE FIGURES WERE WRONG, here and in `57f962f`'s commit message"),
    ("readme.F1", H.README, "quote", M_F1),
    ("readme.B1", H.README, "para",
     "**Two corrections to this bullet, from mg-6a2f §B1, made by mg-7735.**"),
    ("readme.B1.A3", H.README, "quote",
     "**`two commits before mg-34bf's parent` was off by one"),
    ("readme.index", H.README, "para",
     "**`cell before` and `cell after` are measured at"),
    ("readme.A1", H.README, "quote",
     "**`b68db5d`'s HEADLINE VERIFICATION SENTENCE IS BLIND TO THE CHANGE IT CERTIFIES"),
    ("readme.A1.7870", H.README, "quote", M_A1_7870),
    ("readme.A1.4acd", H.README, "quote", "mg-babf B1, BROKEN, repaired by mg-4acd"),
]


def region_text(text, kind, marker):
    if kind == "row":
        i = H.row_index(text, marker)
        return text.split("\n")[i]
    lines = text.split("\n")
    if kind == "quote":
        s, e = H.quote_span(text, marker)
        return "\n".join(lines[s:e])
    i = H.marker_line(text, marker)
    s, e = i, i + 1
    while s - 1 >= 0 and lines[s - 1].strip() and not lines[s - 1].lstrip().startswith(">"):
        s -= 1
    while e < len(lines) and lines[e].strip() and not lines[e].lstrip().startswith(">"):
        e += 1
    return "\n".join(lines[s:e])


# =========================================================================================
# The eight context mutations this comparison is run under.  Four are mg-babf's, restated
# from their published prose; two are mg-2216's tolerances that mg-4acd REVERSED and
# COVERAGE.md flags as "the weak point ... not verified against a renderer"; two are mine.
# =========================================================================================
def mu_b04(t):
    lines = t[H.README].split("\n")
    s, e = H.quote_span(t[H.README], M_A1_7870)
    rest = lines[:s] + lines[e:]
    return {H.README: "\n".join(rest + ["", "## Appendix Z — superseded drafts, retained "
                                        "for the record only; nothing below is in force",
                                        ""] + lines[s:e])}


def mu_b05(t):
    lines = t[H.README].split("\n")
    s, e = H.quote_span(t[H.README], M_F1)
    return {H.README: "\n".join(lines[:s] + ["```text"] + lines[s:e] + ["```"] + lines[e:])}


def mu_b06(t):
    lines = t[H.README].split("\n")
    s, e = H.quote_span(t[H.README], M_F1)
    return {H.README: "\n".join(lines[:s] + ["<!--"] + lines[s:e] + ["-->"] + lines[e:])}


def mu_b07(t):
    lines = t[H.README].split("\n")
    s, _ = H.quote_span(t[H.README], M_A1_7870)
    ins = ["**RETRACTED. The correction block below was filed in error and is void.**", ""]
    return {H.README: "\n".join(lines[:s] + ins + lines[s:])}


def mu_m12(t):
    """mg-2216 M12: 60 lines inserted above the certified row, splitting the table."""
    lines = t[H.STATE].split("\n")
    i = H.row_index(t[H.STATE], "mg-276d")
    return {H.STATE: "\n".join(lines[:i] + ["", "filler paragraph."] * 30 + lines[i:])}


def mu_m13(t):
    """mg-2216 M13: the certified row moved to the end of the file, byte-identical."""
    lines = t[H.STATE].split("\n")
    i = H.row_index(t[H.STATE], "mg-276d")
    row = lines.pop(i)
    return {H.STATE: "\n".join(lines + ["", row])}


def mu_p1(t):
    lines = t[H.README].split("\n")
    i = [k for k, l in enumerate(lines) if l.startswith(H_CERT)][0]
    r = "**RETRACTED (mg-218d). Every correction block below is void.**"
    return {H.README: "\n".join(lines[:i + 1] + ["", r] + lines[i + 1:])}


def mu_p2(t):
    lines = t[H.README].split("\n")
    i = [k for k, l in enumerate(lines) if l.startswith(H_CERT)][0]
    r = "**RETRACTED (mg-218d). Every correction block below is void.**"
    return {H.README: "\n".join(lines[:i] + [r, ""] + lines[i:])}


MUTATIONS = [
    ("B04", "readme.A1.7870", H.README, "block moved under 'Appendix Z ... not in force'",
     mu_b04),
    ("B05", "readme.F1", H.README, "block wrapped in a ```text fence", mu_b05),
    ("B06", "readme.F1", H.README, "block wrapped in an HTML comment", mu_b06),
    ("B07", "readme.A1.7870", H.README, "retraction immediately above the block", mu_b07),
    ("M12", "cell.tree", H.STATE, "60 lines inserted above the certified row", mu_m12),
    ("M13", "cell.tree", H.STATE, "the certified row moved to the end of the file", mu_m13),
    ("P1", "readme.A1.7870", H.README, "mg-218d: retraction INSIDE the section", mu_p1),
    ("P2", "readme.A1.7870", H.README, "mg-218d: the SAME line one line earlier", mu_p2),
]


def main():
    print(__doc__)
    have = subprocess.run(["node", "-e", "require('marked');require('markdown-it')"],
                          capture_output=True)
    if have.returncode != 0:
        print("RENDERERS NOT AVAILABLE on this run.")
        print(have.stderr.decode().strip().split("\n")[0])
        print("\nInstall and re-run:")
        print("  D=$(mktemp -d); npm install --prefix $D marked markdown-it")
        print("  NODE_PATH=$D/node_modules python3 "
              "code/state_layer_audit_218d/render218d.py")
        return 3

    ver = subprocess.run(
        ["node", "-e",
         "console.log(require('marked/package.json').version, "
         "require('markdown-it/package.json').version)"],
        capture_output=True, text=True).stdout.split()
    print(f"RENDERER VERSIONS PINNED IN THIS RUN: marked {ver[0]}, "
          f"markdown-it {ver[1]}, node {sys.version and subprocess.run(['node','-v'],capture_output=True,text=True).stdout.strip()}")
    print()

    tree = H.Tree([H.STATE, H.README, ATTEMPT])
    snap = {r: tree.text(r) for r in [H.STATE, H.README, ATTEMPT]}

    sentinels = {}
    for rid, rel, kind, marker in REGIONS:
        sentinels[rid] = sentinel_for(region_text(snap[rel], kind, marker))

    code, out = H.run(H.control_cmd())
    if code != 0:
        raise SystemExit("the control does not pass on the clean tree; aborting.")
    states = model_states(out)

    print("=" * 96)
    print("A. AT REST — the instrument's printed `state` against two real renderers")
    print("=" * 96)
    rendered = {rel: {e: walk(render(rel, e)) for e in ENGINES}
                for rel in (H.STATE, H.README)}
    rows_a = []
    for rid, rel, kind, marker in REGIONS:
        model = states.get(rid, ("?", "?"))[1]
        got = {e: classify(rendered[rel][e], sentinels[rid])[0] for e in ENGINES}
        expect = "table-cell" if model == "gfm-table-row" else "prose"
        ok = all(v == expect for v in got.values())
        rows_a.append((rid, model, got, ok))
        print(f"  {'OK ' if ok else '>>>'} {rid:<16} model={model:<16} "
              f"marked={got['marked']:<34} markdown-it={got['markdown-it']}")
    agree_a = sum(1 for r in rows_a if r[3])
    print()
    print(f"  {agree_a} of {len(rows_a)} certified regions: BOTH renderers put the region "
          f"where the model says it is.")
    print("  (Nine, not ten: `cell.base` is a blob at b68db5d^ and not a file in the tree,")
    print("   so there is nothing on disk for a renderer to read.  It is the same row of")
    print("   the same table as `cell.tree` at an earlier revision.)")
    print()

    print("=" * 96)
    print("A2. EVERY BLOCK IN BOTH FILES — not only the certified ten.  The model resolves")
    print("    the whole document; a model that is right about ten regions and wrong about")
    print("    the document is a model that will be wrong about the eleventh region.")
    print("=" * 96)
    rows_a2 = []
    skipped = {"no markup-free run": 0, "sentinel not unique in the source": 0}
    for rel in (H.STATE, H.README):
        doc = pres.Doc(snap[rel])
        for first, last, _section, _ordinal, _kind in doc.blocks:
            body = "\n".join(pres.strip_quotes(doc.lines[i])[1]
                             for i in range(first, last + 1))
            try:
                sent = sentinel_for(body)
            except LookupError:
                skipped["no markup-free run"] += 1
                continue
            if snap[rel].count(sent) != 1:
                skipped["sentinel not unique in the source"] += 1
                continue
            model = doc.state[first]
            pred = {"rendered": ("prose", "table-cell"),
                    "fenced-code": ("code-sample",),
                    "html-comment": ("ABSENT (a reader is shown nothing)",),
                    "html-block": ("prose", "code-sample", "table-cell",
                                   "ABSENT (a reader is shown nothing)")}[model]
            got = {e: classify(rendered[rel][e], sent)[0] for e in ENGINES}
            ok = all(v in pred for v in got.values())
            rows_a2.append((rel, first + 1, model, got, ok))
    agree_a2 = sum(1 for r in rows_a2 if r[4])
    for rel, ln, model, got, ok in rows_a2:
        if not ok:
            print(f"  >>> {rel}:{ln} model={model} marked={got['marked']} "
                  f"markdown-it={got['markdown-it']}")
    tot_blocks = sum(len(pres.Doc(snap[r]).blocks) for r in (H.STATE, H.README))
    print(f"  {agree_a2} of {len(rows_a2)} compared blocks agree with BOTH renderers; "
          f"{len(rows_a2) - agree_a2} disagree, and every one of them is printed above.")
    print(f"  Population: {tot_blocks} blocks in the two files; "
          f"{len(rows_a2)} carried a sentinel that could be compared, "
          + "; ".join(f"{v} skipped — {k}" for k, v in skipped.items()) + ".")
    print()

    print("=" * 96)
    print("B. UNDER MUTATION — does the model's verdict match what a renderer does?")
    print("   `control` is the exit code delta_control.py returned; `model` is the `state`")
    print("   it printed for that region; the two right-hand columns are the renderers.")
    print("=" * 96)
    rows_b = []
    for mid, rid, rel, desc, fn in MUTATIONS:
        edits = fn(snap)
        try:
            for r, new in edits.items():
                H.write(r, new.encode("utf-8"))
            ccode, cout = H.run(H.control_cmd())
            st = model_states(cout).get(rid, ("?", "?"))
            got = {}
            for e in ENGINES:
                got[e] = classify(walk(render(rel, e)), sentinels[rid])[0]
        finally:
            tree.restore()
        # what the model SAYS a reader sees, mapped onto what a renderer would DO
        pred = {"rendered": "prose", "gfm-table-row": "table-cell",
                "fenced-code": "code-sample",
                "html-comment": "ABSENT (a reader is shown nothing)"}.get(
                    st[1], None)
        if st[1].startswith("pipes-in-a-paragraph"):
            pred = "prose"
        ok = pred is not None and all(v == pred for v in got.values())
        rows_b.append((mid, rid, desc, ccode, st[1], got, ok, pred))
        print(f"  {'OK ' if ok else '>>>'} {mid:<4} {desc}")
        print(f"        region {rid:<16} control exit {ccode}   model state: {st[1]}")
        print(f"        model predicts a reader sees it as: {pred}")
        for e in ENGINES:
            flag = "" if got[e] == pred else "   <-- DISAGREES WITH THE MODEL"
            print(f"        {e:<12} actually renders it as: {got[e]}{flag}")
    print()
    agree_b = sum(1 for r in rows_b if r[6])
    print(f"  {agree_b} of {len(rows_b)} mutations: BOTH renderers did what the model said "
          f"they would.")
    print()

    print("=" * 96)
    print("VERDICT ON THE NAMED RESIDUAL RISK")
    print("=" * 96)
    total = len(rows_a) + len(rows_a2) + len(rows_b)
    ok = agree_a + agree_a2 + agree_b
    print(f"  {ok} of {total} comparisons agree, over 2 independent renderers.")
    print("  This does not establish that presentation.py matches GFM in general.  It is a")
    print("  measurement over the regions this control certifies, every comparable block of")
    print("  the two files it reads, and eight mutations — and that is the whole of what it")
    print("  establishes.  A construct absent from these two documents is not tested here.")
    print()
    print("  The two rows that matter most are M12 and M13: COVERAGE.md reverses mg-2216's")
    print("  published tolerance for them, argues the reversal from the GFM table rules,")
    print("  and says plainly that the argument is NOT verified against a renderer and")
    print("  that 'if a renderer disagrees, mg-2216 was right and these two rows are")
    print("  noise'.  They are verified above.")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
