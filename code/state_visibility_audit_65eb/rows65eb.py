#!/usr/bin/env python3
"""mg-65eb — THE ROW LEDGER: THE PROPERTY CLAIMED BESIDE THE QUANTITY COMPUTED, AND A CASE
THAT SEPARATES THEM.

mg-a74f exists because an instrument measured BYTES IN THE HTML while its row claimed WHAT A
READER IS SHOWN.  It publishes nine rows (`claims_a74f.py`, "EVERY INSTRUMENT THIS REPAIR
ADDS, AND WHETHER ITS ROW NAME IS ITS MEASUREMENT"): eight MATCHES and one DOES NOT MATCH.

THAT TABLE IS THE THING UNDER TEST HERE.  For each row this file writes the property the row
NAMES beside the quantity the code COMPUTES and then tries to BUILD A DOCUMENT OR A TREE ON
WHICH THE TWO DISAGREE.  A row that cannot be separated is reported NOT SEPARATED with the
reason, never as a silent pass.

THIS IS A PROXY CHECK, NOT A CORRECTNESS CHECK.  Every instrument below can be perfectly
correct about the quantity it computes and still be the wrong instrument for the property its
row names.  Nothing here says any of these programs has a bug in the thing it does; it says
what set the thing it does is, and where that set is not the set the row claims.

NOTHING IN THE AUDITED DIRECTORIES IS EDITED.  The constructions in section C write to
`code/state_landing_control_2da3/` and `code/state_delegation_repair_0049/` under a snapshot,
a `finally`, and a post-restore sha256 check that hard-aborts, exactly as mg-16eb's harness
does; `run_all.sh` prints `git diff` over all four directories after the run.

    D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
    NODE_PATH="$D/node_modules" python3 code/state_visibility_audit_65eb/rows65eb.py

Without the renderers section B cannot run; it is skipped, section C still runs, and the exit
code is 3 so that a partial transcript cannot be read as a full one.
"""
import hashlib
import html
import os
import re
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, os.path.join(REPO, "code/state_delegation_audit_16eb"))
sys.path.insert(0, os.path.join(REPO, "code/state_delegation_repair_0049"))
sys.path.insert(0, os.path.join(REPO, "code/state_delegation_repair_a74f"))

import render16eb as R16              # noqa: E402
import mutations_0049 as M49          # noqa: E402
import visible_a74f as V              # noqa: E402   the instrument under test, UNMODIFIED

PROSE = "code/state_delegation_repair_a74f/prose_a74f.py"
CTL = "code/state_landing_control_2da3/delta_control.py"
RDM = "code/state_delegation_repair_0049/README.md"
UNTRACKED = "code/state_landing_control_2da3/_65eb_untracked_probe.py"

ENGINES = ["marked", "markdown-it"]
CITED = ["H1", "H2", "H3", "H4", "H5"]


# =========================================================================================
# THE LEDGER.  (row id, file, row name, THE PROPERTY THE ROW NAMES, THE QUANTITY THE CODE
# COMPUTES, what mg-a74f publishes for it, what this audit PREDICTED in PREDICTIONS.md).
# =========================================================================================
LEDGER = [
    ("R1", "visible_a74f.py", "bytes-in-html",
     "the section marker is present in the serialised HTML",
     "the section marker is present in html.unescape(the serialised HTML)",
     "MATCHES", True),
    ("R2", "visible_a74f.py", "not-suppressed",
     "not suppressed by any of the FIVE DECLARED mechanisms, at the marker's position",
     "no mechanism found by a tag-stack walk to an offset taken in the UNESCAPED string, "
     "with `hidden` and `open` matched as words anywhere in an ancestor's attribute text",
     "MATCHES", True),
    ("R3", "visible_a74f.py", "r16 SHOWN",
     "what a reader is shown (mg-16eb's name, kept on purpose)",
     "bytes surviving a tag strip, minus closed-<details> ancestors",
     "DOES NOT MATCH, deliberately", False),
    ("R4", "prose_a74f.py", "P1 path references",
     "every repo-relative path named in the text exists at the revision being read",
     "every string matching `(code|docs)/...\\.(py|md|sh|js|txt|json)` is in the file set, "
     "which on the working tree is every file in the working DIRECTORY",
     "MATCHES", True),
    ("R5", "prose_a74f.py", "P2 section references",
     "every `section N` reference to a run_all.sh resolves and names the tokens on its line",
     "every `section N` on a line that ALSO contains the literal `run_all.sh` or the literal "
     "`re-run in section` resolves and names the tokens on its line",
     "MATCHES", True),
    ("R6", "prose_a74f.py", "P3 pinned tables",
     "every module-level dict of delta_control.py KEYED BY REPO PATHS is iterated",
     "every module-level dict ALL of whose keys start `code/` or `docs/` AND contain a `.` "
     "is iterated",
     "MATCHES", True),
    ("R7", "prose_a74f.py", "P4 `all N rows`",
     "the number equals THAT SCRIPT's own ROWS",
     "the number equals the ROWS of the nearest .py basename in the preceding 400 characters",
     "MATCHES", True),
    ("R8", "battery_a74f.py", "exit codes",
     "the exit code of the mutated control",
     "subprocess returncode read by harness16eb.Tree.run_mutated",
     "MATCHES", False),
    ("R9", "claims_a74f.py", "before / after",
     "the defect is present at bd24efc and absent in the tree",
     "a text or AST predicate over `git show bd24efc:path` and the working-tree file",
     "MATCHES", False),
]

FINDINGS = []          # (row, one-line statement of the separation)
SCORE = []             # (row, predicted separable, observed separable)


def sha(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def rd(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as fh:
        return fh.read()


def wr(rel, text):
    with open(os.path.join(REPO, rel), "w", encoding="utf-8") as fh:
        fh.write(text)


def once(text, needle):
    n = text.count(needle)
    if n != 1:
        raise LookupError(f"anchor matched {n} times, need exactly 1: {needle[:60]!r}")
    return text


def dirty(rels):
    out = subprocess.run(["git", "-C", REPO, "status", "--porcelain", "--"] + list(rels),
                         capture_output=True, text=True, check=True).stdout
    return [ln[3:].strip() for ln in out.splitlines() if ln.strip()]


class Tree:
    """Snapshot, mutate, run, restore under a `finally`, verify the restore by sha256.

    The discipline is mg-16eb's and mg-5644's, re-implemented here rather than imported
    because `harness16eb.Tree` runs delta_control.py and this audit runs prose_a74f.py."""

    def __init__(self, rels):
        self.rels = list(rels)
        bad = dirty(self.rels)
        if bad:
            raise SystemExit("REFUSING TO RUN: already dirty: " + ", ".join(bad))
        self.orig = {r: rd(r) for r in self.rels}
        self.sha0 = {r: sha(self.orig[r]) for r in self.rels}

    def run(self, edits, extra_file=None):
        """edits: rel -> new text.  extra_file: (rel, text) created UNTRACKED and removed.

        Returns (exit code, stdout) of prose_a74f.py on the mutated tree."""
        made = None
        try:
            for rel, text in edits.items():
                if text == self.orig[rel]:
                    raise AssertionError(f"{rel}: mutation is a no-op — it tests nothing")
                wr(rel, text)
            if extra_file:
                made = extra_file[0]
                wr(made, extra_file[1])
            proc = subprocess.run([sys.executable, os.path.join(REPO, PROSE)],
                                  cwd=REPO, capture_output=True, text=True)
            return proc.returncode, proc.stdout
        finally:
            for rel in edits:
                wr(rel, self.orig[rel])
                if sha(rd(rel)) != self.sha0[rel]:
                    raise SystemExit(f"HARD ABORT: {rel} did not restore.  Recover with:\n"
                                     f"    git -C {REPO} checkout -- {rel}")
            if made and os.path.exists(os.path.join(REPO, made)):
                os.remove(os.path.join(REPO, made))


def findings_of(out):
    m = re.search(r"^  (\d+) finding\(s\)\.$", out, re.M)
    return int(m.group(1)) if m else None


def verdict(row, separated, claim, detail):
    pred = dict((r[0], r[6]) for r in LEDGER)[row]
    SCORE.append((row, pred, separated))
    tag = "SEPARATED" if separated else "NOT SEPARATED"
    print(f"    >>> {row}  {tag}   (this audit predicted "
          f"{'SEPARABLE' if pred else 'NOT SEPARABLE'}"
          f"{'' if pred == separated else '  !! OFF PREDICTION'})")
    print(f"        {claim}")
    for line in detail:
        print(f"        {line}")
    if separated:
        FINDINGS.append((row, claim))
    print()


# =========================================================================================
# SECTION B — the three constructions against visible_a74f.py, through two real renderers.
# =========================================================================================
def b_marker_entity(t):
    """Every cited marker written with `&mdash;` instead of the em dash itself.

    A reader is shown `H1 — ` on every engine.  The bytes `H1 — ` are NOT in the serialised
    HTML: `H1 &mdash; ` is.  This is the direction the brief calls "content shown but not a
    byte in that file"."""
    for h in CITED:
        t = once(t, f"{h} — ").replace(f"{h} — ", f"{h} &mdash; ")
    return t


def b_class_hidden(t):
    """`<div class="hidden">` — a CLASS named hidden, not the `hidden` ATTRIBUTE.

    With no stylesheet in the document a reader is shown every cited section.  The declared
    set's S4 is "inside an element carrying the `hidden` attribute" and NOT_COVERED names
    "`display:none` on a class" as OUTSIDE the set."""
    return '<div class="hidden">\n\n' + t


def b_details_titled(t):
    """mg-16eb's own B3 shape with one extra attribute: `<details title="open me">`.

    It carries NO `open` attribute, so the DECLARED S1 holds of it and a reader is shown a
    closed widget and no cited section at all — exactly mg-16eb's B3."""
    return ('<details title="open me"><summary>Details</summary>\n\n' + t)


def b_entity_prefix_hidden(t, pad):
    """`<div hidden>` — mg-a74f's own V3 — behind a paragraph of `&`.

    Each `&` is one byte of markdown and five bytes (`&amp;`) of HTML, so `html.unescape`
    shortens the document by four bytes per `&` BEFORE the marker.  `visible_a74f.main()`
    takes the marker's index in the UNESCAPED string and spends it as an offset in the
    ESCAPED one, so the walk stops before the `<div hidden>` it should have found."""
    return "&" * pad + "\n\n<div hidden>\n\n" + t


def measure(out):
    """The two quantities visible_a74f.main() computes, computed the way it computes them:
    line for line the same expressions, on the same imported functions."""
    u = html.unescape(out)
    present = [h for h in CITED if V.marker(h) in u]
    mech = {h: V.suppressors(out, u.index(V.marker(h))) for h in present}
    free = [h for h in present if not mech[h]]
    return present, free, mech


def true_positions(out):
    """The same measurement with the ONE difference: the offset is taken in the string it is
    spent in.  Nothing else changes."""
    u = html.unescape(out)
    present = [h for h in CITED if V.marker(h) in u]
    mech = {}
    for h in present:
        i = out.find(V.marker(h))
        if i < 0:                       # the marker exists only after unescaping
            i = None
        mech[h] = V.suppressors(out, i) if i is not None else ["(marker not in raw HTML)"]
    free = [h for h in present if not mech[h] or mech[h] == ["(marker not in raw HTML)"]]
    return present, free, mech


def section_b():
    print("=" * 100)
    print("B.  visible_a74f.py — THREE CONSTRUCTIONS, THROUGH TWO REAL GFM RENDERERS")
    print("=" * 100)
    orig = M49.original()
    # the drift must exceed the distance from the injected tag to the LAST marker
    pad = 3000
    print(f"  target: {len(orig)} bytes; entity padding for R2c: {pad} `&` "
          f"= {pad * 4} bytes of unescape shrinkage, against a "
          f"{len(R16.render('marked', orig))}-byte rendered document.")
    print()

    cases = [
        ("R1", "every marker written `&mdash;` — a reader is shown `H1 — `; the HTML has no "
               "such bytes", b_marker_entity, "bytes-in-html"),
        ("R2a", '<div class="hidden"> — a CLASS, not the attribute; with no stylesheet a '
                "reader is shown every section", b_class_hidden, "not-suppressed"),
        ("R2b", '<details title="open me"> — mg-16eb\'s B3 with one extra attribute; a '
                "reader is shown a closed widget", b_details_titled, "not-suppressed"),
        ("R2c", "<div hidden> behind a paragraph of `&` — mg-a74f's own V3, a blank page",
         lambda t: b_entity_prefix_hidden(t, pad), "not-suppressed"),
    ]
    obs = {}
    for cid, what, fn, col in cases:
        doc = fn(orig)
        print(f"  {cid}  {what}")
        for engine in ENGINES:
            out = R16.render(engine, doc)
            present, free, mech = measure(out)
            raw_present = [h for h in CITED if V.marker(h) in out]
            tp, tfree, tmech = true_positions(out)
            allm = sorted({m for v in mech.values() for m in v})
            print(f"      {engine:<12s} bytes-in-html {len(present)}/5   "
                  f"not-suppressed {len(free)}/5   by "
                  f"{'+'.join(allm) if allm else '(nothing)':<9s}   "
                  f"| marker literally in the HTML: {len(raw_present)}/5   "
                  f"| same walk at the TRUE offset: {len(tfree)}/5 free")
            obs[(cid, engine)] = (len(present), len(free), len(raw_present), len(tfree))
        print()

    # ---- R1.  THE RULE THIS AUDIT COMMITTED TO IS `all engines`, AND IT IS NOT WEAKENED
    # AFTER THE FACT.  PREDICTIONS.md predicted a separation "on both engines"; markdown-it
    # decodes `&mdash;` to the em dash itself and marked does not, so the construction
    # separates on one engine of the two and this row is scored NOT SEPARATED with the miss
    # kept.  Rewriting `all` to `any` here would be the re-baselining this arc keeps finding.
    both = [obs[("R1", e)] for e in ENGINES]
    sep1 = all(p == 5 and raw == 0 for p, _f, raw, _t in both)
    per_engine = ", ".join(f"{e}: bytes-in-html {obs[('R1', e)][0]}/5 with the literal "
                           f"marker present {obs[('R1', e)][2]}/5" for e in ENGINES)
    verdict("R1", sep1,
            "CLAIMED `the section marker is present in the serialised HTML`; COMPUTED "
            "`present in html.unescape(...)`.",
            [per_engine + ".",
             "The row is the one mg-a74f prints as `names bytes; measures bytes.  MATCHES.`",
             "ON `marked` THE TWO SETS DIFFER ON ALL FIVE CITED SECTIONS: the reader is shown",
             "`H1 — ` and the bytes `H1 — ` are nowhere in the HTML, which is the direction",
             "the brief calls `content shown but not a byte in that file`.  markdown-it",
             "decodes `&mdash;` itself, so on that engine the two sets agree.",
             "THIS AUDIT'S OWN RULE FOR THIS ROW WAS `separates on every engine`, committed",
             "in PREDICTIONS.md, and it is kept: the row is scored NOT SEPARATED and the miss",
             "is kept as written.  The rule is itself a row-name/measurement mismatch of the",
             "kind this file exists to report — it NAMES `is this row separable` and COMPUTES",
             "`does it separate on both engines` — and it is reported rather than rewritten."])

    # ---- R2, three ways
    r2a = [obs[("R2a", e)] for e in ENGINES]
    r2b = [obs[("R2b", e)] for e in ENGINES]
    r2c = [obs[("R2c", e)] for e in ENGINES]
    sep2 = (all(f == 0 for _p, f, _r, _t in r2a)
            or all(f == 5 for _p, f, _r, _t in r2b)
            or all(f == 5 for _p, f, _r, _t in r2c))
    verdict("R2", sep2,
            "CLAIMED `not suppressed by any of five DECLARED mechanisms`; COMPUTED three "
            "different things, none of them that.",
            [f"R2a  `class=\"hidden\"` scores not-suppressed {r2a[0][1]}/5 and {r2a[1][1]}/5."
             "  S4 is declared as the `hidden`",
             "     ATTRIBUTE and NOT_COVERED names class-based hiding as OUTSIDE the set.  A "
             "reader IS shown",
             "     every section of this document — there is no stylesheet in it.  THIS IS A "
             "FAILURE IN THE",
             "     CLOSED DIRECTION, in the instrument whose safety argument is that it fails "
             "OPEN ONLY.",
             f"R2b  `<details title=\"open me\">` scores not-suppressed {r2b[0][1]}/5 and "
             f"{r2b[1][1]}/5.  That element",
             "     carries no `open` attribute, so DECLARED S1 holds of it; a reader is shown "
             "a closed widget",
             "     and nothing else.  The instrument does not implement its own declared set: "
             "`open` is",
             "     matched as a word ANYWHERE in the attribute text, and `title=\"open me\"` "
             "contains it.",
             f"R2c  `<div hidden>` — mg-a74f's OWN V3 — scores not-suppressed {r2c[0][1]}/5 "
             f"and {r2c[1][1]}/5 when",
             "     3000 `&` precede it, against 0/5 without them.  The same walk at the TRUE "
             f"offset scores",
             f"     {r2c[0][3]}/5 and {r2c[1][3]}/5.  `visible_a74f.main()` takes "
             "`html.unescape(out).index(marker)`",
             "     and spends it as an offset into `out`.  A BYTE OFFSET STANDING IN FOR A "
             "POSITION is the",
             "     defect class this whole arc is about, and it is in the instrument built to "
             "repair it."])
    return obs


# =========================================================================================
# SECTION C — four constructions against prose_a74f.py, on the real tree, under restore.
# =========================================================================================
PAD = ("." * 420)

R4_INVISIBLE = ("\nmg-65eb CONSTRUCTION (restored immediately; see rows65eb.py).  See "
                "code/state_landing_control_2da3/no_such_dir/ and "
                "docs/state-history/no-such.yaml and code/state_landing_control_2da3/gone\n")
R4_VISIBLE = ("\nmg-65eb CONSTRUCTION (restored immediately; see rows65eb.py).  See "
              "code/state_landing_control_2da3/no_such.py\n")
R4_UNTRACKED = ("\nmg-65eb CONSTRUCTION (restored immediately; see rows65eb.py).  See "
                f"{UNTRACKED}\n")

R5_INVISIBLE = ("\nmg-65eb CONSTRUCTION (restored immediately; see rows65eb.py).  The nine "
                "mutations of `battery_0049.py` are exercised again in section 3.\n")
R5_VISIBLE = ("\nmg-65eb CONSTRUCTION (restored immediately; see rows65eb.py).  The nine "
              "mutations of `battery_0049.py` are exercised again in section 3 of "
              "`run_all.sh`.\n")

R7_INVISIBLE = ("\nmg-65eb CONSTRUCTION (restored immediately; see rows65eb.py).  " + PAD +
                "  The battery in `mutations_0049.py`, scored by `render0049.py`, runs "
                "against all five rows.\n")
R7_VISIBLE = ("\nmg-65eb CONSTRUCTION (restored immediately; see rows65eb.py).  " + PAD +
              "  The battery in `mutations_0049.py` runs against all five rows.\n")

_DP = "DELEGATED_PRESENTATION = {\n"
R6_TABLE_PATHS = ('_MG65EB_THIRD_TABLE = {\n'
                  '    "docs/state-history/attempt-mg-276d.md": "a third pinned table",\n'
                  '}\n\n')
R6_TABLE_PLUS_NOTE = ('_MG65EB_THIRD_TABLE = {\n'
                      '    "docs/state-history/attempt-mg-276d.md": "a third pinned table",\n'
                      '    "note": "one key that is not a repo path",\n'
                      '}\n\n')


def section_c():
    print("=" * 100)
    print("C.  prose_a74f.py — FOUR CONSTRUCTIONS ON THE REAL TREE, UNDER RESTORE DISCIPLINE")
    print("=" * 100)
    tree = Tree([RDM, CTL])
    base = subprocess.run([sys.executable, os.path.join(REPO, PROSE)],
                          cwd=REPO, capture_output=True, text=True)
    print(f"  BASELINE on the clean tree: exit {base.returncode}, "
          f"{findings_of(base.stdout)} finding(s).  Every delta below is against this.")
    print()
    if base.returncode != 0:
        print("  !! the baseline is not clean; the deltas below are still measured but the")
        print("     attribution of each finding to its construction is weaker.")
        print()

    rdm = tree.orig[RDM]
    ctl = tree.orig[CTL]
    res = {}

    def run(label, edits, extra=None):
        code, out = tree.run(edits, extra)
        n = findings_of(out)
        res[label] = (code, n)
        print(f"    {label:<6s} exit {code}   {n} finding(s)")
        return code, n

    print("  R4 — P1's population.  Claimed: EVERY repo-relative path named in the text.")
    run("R4a", {RDM: rdm + R4_INVISIBLE})
    run("R4b", {RDM: rdm + R4_VISIBLE})
    run("R4c", {RDM: rdm + R4_UNTRACKED}, extra=(UNTRACKED, "# mg-65eb probe\n"))
    run("R4d", {RDM: rdm + R4_UNTRACKED})
    print()
    sep4 = (res["R4a"][1] == res["R4b"][1] - 1 and res["R4c"][1] < res["R4d"][1])
    verdict("R4", sep4,
            "CLAIMED `every repo-relative path named in the text exists at the revision "
            "being read`; COMPUTED `every string with one of six extensions is somewhere "
            "in the working DIRECTORY`.",
            [f"R4a  three named paths that do not exist "
             f"(`…/no_such_dir/`, `…/no-such.yaml`, `…/gone`): "
             f"{res['R4a'][1]} finding(s) — none of the three is seen.",
             f"R4b  one named path that does not exist, spelled `.py`: {res['R4b'][1]} "
             f"finding(s).  Same sentence, same tree,",
             "     opposite verdict, and the only difference is the extension.",
             f"R4c  a named path that exists ONLY as an UNTRACKED file: {res['R4c'][1]} "
             f"finding(s) — it passes.",
             f"R4d  the same sentence with that file deleted: {res['R4d'][1]} finding(s).  "
             "So `exists at this revision`",
             "     is decided by the working directory, and an untracked file satisfies a "
             "claim about the tree.",
             "     `claims_a74f.in_tree(None, …)` is `os.path.exists` too and moves with it."])

    print("  R5 — P2's population.  Claimed: EVERY `section N` reference to a run_all.sh.")
    run("R5a", {RDM: rdm + R5_INVISIBLE})
    run("R5b", {RDM: rdm + R5_VISIBLE})
    print()
    sep5 = res["R5a"][1] < res["R5b"][1]
    verdict("R5", sep5,
            "CLAIMED `every section N reference to a run_all.sh`; COMPUTED `every section N "
            "on a line that also contains the literal run_all.sh or the literal `re-run in "
            "section``.",
            [f"R5a  a false section reference, no `run_all.sh` on the line: "
             f"{res['R5a'][1]} finding(s) — invisible.",
             f"R5b  the same false claim with `of \\`run_all.sh\\`` appended: "
             f"{res['R5b'][1]} finding(s).",
             "     The claim is identically false in both.  The checker's population is a "
             "property of the",
             "     LINE'S WORDING, not of the claim.  Live instance of the shape it does not "
             "see:",
             "     code/state_delegation_repair_0049/README.md:165 says `section 7's re-runs "
             "mutate tracked",
             "     files`, unchanged at bd24efc and at HEAD, and P2 has never looked at it.  "
             "(This audit",
             "     checked that line and REFUTES its own candidate: section 7 re-runs "
             "coverage218d.py, which",
             "     does mutate through harness218d.Tree, so the sentence stands.  The "
             "population gap does not",
             "     depend on it.)"])

    print("  R6 — P3's population.  Claimed: EVERY module-level dict KEYED BY REPO PATHS.")
    run("R6a", {CTL: ctl.replace(_DP, R6_TABLE_PATHS + _DP, 1)})
    run("R6b", {CTL: ctl.replace(_DP, R6_TABLE_PLUS_NOTE + _DP, 1)})
    print()
    sep6 = res["R6a"][1] > res["R6b"][1]
    verdict("R6", sep6,
            "CLAIMED `every module-level dict keyed by repo paths is iterated`; COMPUTED "
            "`every module-level dict ALL of whose keys start code/ or docs/ AND contain a "
            "dot`.",
            [f"R6a  a third pinned table, keyed by one repo path, iterated by nothing: "
             f"{res['R6a'][1]} finding(s).",
             "     That is mg-a74f's claim working — `a third table joins the population by "
             "existing`.",
             f"R6b  the same table with ONE extra key, `\"note\"`: {res['R6b'][1]} "
             f"finding(s).  It leaves the",
             "     population and its being iterated by nothing is no longer checkable by "
             "this program.",
             "     A pinned table nothing visits is exactly broken claim 3, and one "
             "annotation key hides it.",
             "     `claims_a74f.iterated_tables()` computes the SAME population by a "
             "DIFFERENT rule (no dot",
             "     requirement), so the two halves of this repair do not agree on what the "
             "population is."])

    print("  R7 — P4's attribution.  Claimed: THAT SCRIPT's own ROWS.")
    run("R7a", {RDM: rdm + R7_VISIBLE})
    run("R7b", {RDM: rdm + R7_INVISIBLE})
    print()
    sep7 = res["R7a"][1] > res["R7b"][1]
    verdict("R7", sep7,
            "CLAIMED `the number equals THAT SCRIPT's own ROWS`; COMPUTED `the number equals "
            "the ROWS of the nearest .py basename in the preceding 400 characters`.",
            [f"R7a  `The battery in \\`mutations_0049.py\\` runs against all five rows` "
             f"(ROWS is 9): {res['R7a'][1]} finding(s).",
             f"R7b  the same false sentence with `, scored by \\`render0049.py\\`,` inserted "
             f"before it: {res['R7b'][1]} finding(s).",
             "     render0049.py's ROWS is 5, so the false claim about mutations_0049.py is "
             "checked against a",
             "     different script and passes.  The verdict is decided by a neighbouring "
             "token, not by the",
             "     claim's subject."])
    return res


# =========================================================================================
# SECTION D — the rows this audit could NOT separate, and why.
# =========================================================================================
def section_d():
    print("=" * 100)
    print("D.  THE ROWS THIS AUDIT COULD NOT SEPARATE, AND WHY — stated, not left as absence")
    print("=" * 100)
    print("  R3  visible_a74f `r16 SHOWN`.  The row NAMES what a reader is shown and computes")
    print("      bytes-minus-one-mechanism, and those are different sets — but mg-a74f")
    print("      already publishes this row as DOES NOT MATCH and builds V1/V3/V4 to show it.")
    print("      There is nothing here for an independent audit to separate that the repair")
    print("      has not separated itself.  Confirmed, not re-derived: see section B, where")
    print("      the same rule scores 5/5 on documents a reader is shown nothing of.")
    verdict("R3", False, "CLAIMED and COMPUTED differ, and the row says so.",
            ["mg-a74f keeps mg-16eb's name for mg-16eb's rule on purpose so the mismatch is",
             "legible.  This audit agrees with that choice and adds nothing to it."])
    print("  R8  battery_a74f `exit codes`.  The row names the exit code of the mutated")
    print("      control and reads `subprocess.returncode`.  Those are the same set: the")
    print("      code is read from the process and never inferred from stdout, which is")
    print("      checkable by reading harness16eb.Tree.run_mutated and is what it does.")
    verdict("R8", False, "CLAIMED = COMPUTED.",
            ["The one thing that could separate them — reading section 1's PRINTED `6 of 8`",
             "instead of re-running — is exactly what battery_a74f.py's section 2 refuses to",
             "do, in writing, and section 2 re-runs all eight rows itself.  No construction."])
    print("  R9  claims_a74f `before / after`.  The row names a predicate over two revisions")
    print("      and computes a predicate over two revisions.  For claims 4 and 6 it checks")
    print("      THE WORDING and mg-a74f says so in the same row.  Its `the tree` is the")
    print("      working directory, which R4c moves — but the row says `the tree` and the")
    print("      working directory IS the tree; the row is not separated by that.")
    verdict("R9", False, "CLAIMED = COMPUTED, with the caveat mg-a74f already prints.",
            ["`in_tree(None, path)` is `os.path.exists`, so claim 1's `that path exists`",
             "would be satisfied by an untracked file — reported under R4c, where the row",
             "name is about a REVISION.  Here the row name is `the tree` and it is honest."])


# =========================================================================================
# SECTION E — the surface this repair lays, and what is measurable ONLY through it.
# =========================================================================================
def section_e():
    print("=" * 100)
    print("E.  THE NEW SURFACE, AND THE ONE CLAIM NOW VERIFIABLE ONLY THROUGH IT")
    print("=" * 100)
    r49 = rd("code/state_delegation_repair_0049/render0049.py")
    points_at = "visible_a74f.py" in r49
    old_gone = "WHAT A READER IS SHOWN UNDER THIS REPAIR'S FIVE NEW ROWS" not in r49
    # THE POPULATION RULE, STATED: every .py under code/ that COMPUTES a per-section
    # suppression verdict — that is, one that walks HTML for a hiding mechanism.  Derived by
    # the presence of any of three tokens, printed with the token that matched, so a reader
    # can see the rule and disagree with it.  A keyword sweep for the word "suppress" would
    # count files that only talk about it and is not the question.
    TOKENS = ("closed_details_ancestors", "def suppressors", r"DECLARED = \[",
              r"display\s*:\s*none")
    others = []
    for root, _d, fs in os.walk(os.path.join(REPO, "code")):
        for f in sorted(fs):
            if not f.endswith(".py"):
                continue
            rel = os.path.relpath(os.path.join(root, f), REPO)
            if rel.startswith("code/state_visibility_audit_65eb/"):
                continue
            try:
                with open(os.path.join(REPO, rel), encoding="utf-8") as fh:
                    t = fh.read()
            except Exception:                                   # noqa: BLE001
                continue
            hit = [tok for tok in TOKENS if re.search(tok, t)]
            if hit:
                others.append((rel, hit))
    print(f"  render0049.py points a reader at visible_a74f.py for suppression: {points_at}")
    print(f"  render0049.py's old `WHAT A READER IS SHOWN` header is gone: {old_gone}")
    print("  POPULATION RULE: every .py under code/ carrying a token that COMPUTES a")
    print("  suppression verdict — closed_details_ancestors, def suppressors, DECLARED = [,")
    print("  or a display:none pattern.  Printed with the token, so the rule is legible.")
    print(f"  {len(others)} file(s):")
    for rel, hit in sorted(others):
        print(f"      {rel:<62s} {hit}")
    print()
    print("  THE SINGLE POINT OF FAILURE, NAMED.  After this repair the question `is this")
    print("  section suppressed?` has exactly one instrument in the repository:")
    print("  visible_a74f.py.  render0049.py's R5 was narrowed off the question and now")
    print("  POINTS AT that file; render16eb.py's SHOWN column is demonstrated wrong by that")
    print("  same file; nothing else measures it.  mg-a74f names this surface itself and")
    print("  predicts its next gap as `a mechanism outside the set`.")
    print()
    print("  THIS AUDIT'S FINDING IS THAT THE GAP IS NOT WHERE THE PREDICTION PUT IT.  Two")
    print("  of the three separations in section B are INSIDE the declared set — S1 and S4")
    print("  are not implemented as declared — and the third is an offset bug, not a")
    print("  mechanism at all.  A reader who trusts the prediction watches for stylesheets")
    print("  and JavaScript while `class=\"hidden\"` scores SUPPRESSED and `<div hidden>`")
    print("  behind an ampersand scores NOT SUPPRESSED, and no second instrument disagrees.")
    print()


def main():
    print("=" * 100)
    print("mg-65eb — THE PROPERTY CLAIMED BESIDE THE QUANTITY COMPUTED, ROW BY ROW")
    print("=" * 100)
    print("  Population: the 9 rows mg-a74f publishes in claims_a74f.py under `EVERY")
    print("  INSTRUMENT THIS REPAIR ADDS, AND WHETHER ITS ROW NAME IS ITS MEASUREMENT`.")
    print("  8 of them are published MATCHES and 1 DOES NOT MATCH.")
    print()
    print(f"  {'row':<5s} {'file':<17s} {'row name':<22s} PROPERTY CLAIMED  /  QUANTITY "
          f"COMPUTED")
    for rid, f, name, claimed, computed, pub, _pred in LEDGER:
        print(f"  {rid:<5s} {f:<17s} {name:<22s} [{pub}]")
        print(f"  {'':<5s} {'':<17s} {'CLAIMED':<22s} {claimed}")
        print(f"  {'':<5s} {'':<17s} {'COMPUTED':<22s} {computed}")
    print()

    have = os.path.exists(R16.BRIDGE) and subprocess.run(
        ["node", R16.BRIDGE, "marked", os.devnull],
        capture_output=True, text=True).returncode == 0
    if have:
        section_b()
    else:
        print("=" * 100)
        print("B.  SKIPPED — the two GFM renderers are not installed.  This section is the")
        print("    whole of the visibility evidence; without it this transcript is partial")
        print("    and the exit code is 3.  Install them outside the repo and re-run:")
        print('        D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it')
        print("=" * 100)
        print()
    section_c()
    section_d()
    section_e()

    print("=" * 100)
    print("THE LEDGER, SCORED")
    print("=" * 100)
    off = [(r, p, o) for r, p, o in SCORE if p != o]
    sep = [r for r, _p, o in SCORE if o]
    print(f"  {len(SCORE)} of {len(LEDGER)} published rows reached a verdict.")
    print(f"  SEPARATED: {len(sep)} — {', '.join(sep) or '(none)'}")
    print(f"  NOT SEPARATED: {len(SCORE) - len(sep)}")
    print(f"  off this audit's committed predictions: {len(off)}")
    for r, p, o in off:
        print(f"      {r}  predicted {'SEPARABLE' if p else 'NOT SEPARABLE'}, observed "
              f"{'SEPARATED' if o else 'NOT SEPARATED'}")
    print()
    print("  EVERY SEPARATION, ONE LINE EACH:")
    for r, claim in FINDINGS:
        print(f"    {r}  {claim}")
    print()
    print("  A separation is NOT a bug report.  Each instrument above is correct about the")
    print("  quantity it computes.  What is reported is that the quantity is not the")
    print("  property the row names, and a document or a tree on which the two differ.")
    print("=" * 100)
    if not have:
        return 3
    return 1 if FINDINGS else 0


if __name__ == "__main__":
    sys.exit(main())
