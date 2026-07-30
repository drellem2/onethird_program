#!/usr/bin/env python3
"""mg-218d — THE COVERAGE STATEMENT, CHECKED AGAINST THE CODE.

WHY THIS IS THE LOAD-BEARING ARTIFACT NOW.  After five iterations the control's value is
increasingly in KNOWING ITS BOUNDARY rather than in its reach: the next auditor tests the
stated boundary and not the real one.  A coverage claim that has drifted from the code is
therefore worse than no coverage claim at all.  Every checkable sentence in COVERAGE.md is
checked below against the instrument, against the two certified files, and against this
box — never against COVERAGE.md's own summary of itself.

Checks that CANNOT be mechanised are stated as such and left to the report, rather than
counted as passes.

    python3 code/state_layer_audit_218d/coverage218d.py
"""
import importlib.util
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness218d as H                                            # noqa: E402

sys.path.insert(0, os.path.join(H.REPO, "code", "state_landing_control_2da3"))
import delta_control as dc                                         # noqa: E402
import presentation as pres                                        # noqa: E402

CONTROL_DIR = "code/state_landing_control_2da3"
COVERAGE = f"{CONTROL_DIR}/COVERAGE.md"
DOCS_README = "docs/state-history/README.md"

_ok = []
_named = []


def claim(text, held, detail=""):
    """A sentence COVERAGE.md ASSERTS, checked.  DRIFTED means the document is wrong."""
    _ok.append(bool(held))
    print(f"  [{'holds' if held else 'DRIFTED'}] {text}")
    if detail:
        print(f"            {detail}")


def named(text, found, detail=""):
    """A layer this audit found uncontrolled.  NOT NAMED is not the same verdict as
    DRIFTED — COVERAGE.md did not assert anything false here, it is silent — so these
    are tallied separately and never folded into the claims-that-hold count."""
    _named.append(bool(found))
    print(f"  [{'named    ' if found else 'NOT NAMED'}] {text}")
    if detail:
        print(f"            {detail}")


def main():
    print(__doc__)
    cov = H.read(COVERAGE).decode("utf-8")
    ctl = H.read(f"{CONTROL_DIR}/delta_control.py").decode("utf-8")

    print("=" * 90)
    print("1. THE CERTIFIED SET — the table COVERAGE.md prints against the list the code")
    print("   actually iterates.")
    print("=" * 90)
    m = re.search(r"^## Digested regions — (\d+)", cov, re.M)
    claim("COVERAGE.md states a region count at all", m is not None)
    stated = int(m.group(1)) if m else -1
    claim(f"that count ({stated}) is len(CERTIFIED) in the code ({len(dc.CERTIFIED)})",
          stated == len(dc.CERTIFIED))
    claim(f"PRESENTATION has one digest per certified region "
          f"({len(dc.PRESENTATION)} vs {len(dc.CERTIFIED)})",
          len(dc.PRESENTATION) == len(dc.CERTIFIED))
    ids_code = [r[0] for r in dc.CERTIFIED]
    claim("every certified id has a presentation digest",
          all(i in dc.PRESENTATION for i in ids_code),
          "missing: " + (", ".join(i for i in ids_code if i not in dc.PRESENTATION)
                         or "none"))

    tbl = re.findall(r"^\| `([^`]+)` \| (.*?) \| ([\d,]+) \|$", cov, re.M)
    ids_cov = [t[0] for t in tbl]
    claim(f"COVERAGE.md's table lists the same ids as the code, in the same order",
          ids_cov == ids_code,
          f"COVERAGE.md: {ids_cov}\n            code:        {ids_code}")
    chars_cov = {t[0]: int(t[2].replace(",", "")) for t in tbl}
    chars_code = {r[0]: r[4] for r in dc.CERTIFIED}
    bad = [i for i in ids_code if chars_cov.get(i) != chars_code[i]]
    claim("every 'chars after N' figure in the table equals the code's constant",
          not bad,
          "disagreeing: " + (", ".join(f"{i}: doc {chars_cov.get(i)} vs code {chars_code[i]}"
                                       for i in bad) or "none, over "
                             f"{len(ids_code)} regions"))

    # the figures are constants in the code; are they the MEASURED lengths in the tree?
    state = dc.tree("STATE.md").decode("utf-8")
    base = dc.blob(dc.BASELINE, "STATE.md").decode("utf-8")
    readme = dc.tree(dc.README).decode("utf-8")
    measured = {}
    for rid, _label, kind, marker, _c, _s in dc.CERTIFIED:
        _where, text = dc.extract(rid, kind, marker, state, base, readme)
        measured[rid] = len(dc.norm(text).decode("utf-8"))
    bad2 = [i for i in ids_code if measured[i] != chars_code[i]]
    claim("and equals the length MEASURED in the working tree right now",
          not bad2,
          "disagreeing: " + (", ".join(f"{i}: {measured[i]}" for i in bad2)
                             or f"none, over {len(ids_code)} regions"))
    print()

    print("=" * 90)
    print("2. THE NORMALISATION — the rule as published against the rule as coded.")
    print("=" * 90)
    claim("COVERAGE.md publishes `.strip(\" \\t\\r\\n\")` rather than `.strip()`",
          '`.strip(" \\t\\r\\n")`' in cov or '.strip(" \\t\\r\\n")' in cov)
    claim("norm() in the code strips exactly that set",
          'text.strip(EDGE)' in ctl and dc.EDGE == " \t\r\n",
          f"EDGE = {dc.EDGE!r}")
    claim("U+00A0 survives N (COVERAGE.md's stated reason for the explicit set)",
          dc.norm("a ") == "a ".encode("utf-8"),
          f"N('a' + U+00A0) = {dc.norm(chr(97) + chr(160))!r}")
    m = re.search(r"the cell is still ([\d,]+) characters stripped / ([\d,]+) raw", cov)
    claim("COVERAGE.md's '7,876 stripped / 7,878 raw' figures are still the tree's",
          m is not None and int(m.group(1).replace(",", "")) == measured["cell.tree"],
          (f"stated {m.group(1)} / {m.group(2)}; measured stripped "
           f"{measured['cell.tree']}") if m else "figure not found in COVERAGE.md")
    print()

    print("=" * 90)
    print("3. THE PRESENTATION RECORD — the four fields COVERAGE.md tabulates against the")
    print("   fields the code actually hashes.")
    print("=" * 90)
    doc = pres.Doc(readme)
    s, e, _t = dc.quote_block(readme, dc.CERTIFIED[3][3])
    rec = pres.region_record(doc, s - 1, e - 1)
    fields = [k for k, _v in rec]
    claim("region_record emits exactly state | heading | position | presented",
          fields == ["state", "heading", "position", "presented"], f"{fields}")
    claim("COVERAGE.md's formula line names the same four in the same order",
          "P(region) = state | heading | position | presented" in cov)
    hits = dc.find_row(state, dc.ROW_KEY)
    trec = pres.table_record(pres.Doc(state), hits[0][0] - 1, hits[0][1])
    tfields = [k for k, _v in trec]
    claim("the TABLE record emits a fifth field, `columns`, which the formula does not name",
          tfields == ["state", "heading", "position", "columns", "presented"],
          f"{tfields}  — COVERAGE.md's `state` row does mention the column count in prose")
    claim("is_presented() accepts exactly the two states COVERAGE.md names as not-FAIL",
          dc.is_presented([("state", "rendered")])
          and dc.is_presented([("state", "gfm-table-row")])
          and not dc.is_presented([("state", "html-comment")])
          and not dc.is_presented([("state", "fenced-code")])
          and not dc.is_presented([("state", "html-block")])
          and not dc.is_presented([("state", "pipes-in-a-paragraph (x)")]))
    print()

    print("=" * 90)
    print("4. THE GUARDS — COVERAGE.md's 'at rest 0 / on trip exit 2' table, measured.")
    print("=" * 90)
    for label, text in (("STATE.md", state), (dc.README, readme)):
        d = pres.Doc(text)
        claim(f"{label}: block constructs outside the modelled subset = 0",
              not d.anomalies(), f"over {len(d.lines)} lines; found {len(d.anomalies())}")
        claim(f"{label}: raw-HTML tokens in prose = 0",
              not d.html_tokens(),
              f"over {len(d.lines)} lines; found {len(d.html_tokens())}")
    print()

    print("=" * 90)
    print("5. THE RENDERER-ABSENCE CLAIM, audited as a claim and not accepted as stated.")
    print("=" * 90)
    mods = ["markdown", "markdown_it", "mistune", "commonmark", "cmarkgfm"]
    bins = ["pandoc", "cmark", "cmark-gfm"]
    present_m = [m for m in mods if importlib.util.find_spec(m) is not None]
    present_b = [b for b in bins
                 if subprocess.run(["which", b], capture_output=True).returncode == 0]
    claim("no python module from COVERAGE.md's list is importable on this box",
          not present_m, f"checked {mods}; present: {present_m or 'none'}")
    claim("no binary from COVERAGE.md's list is on PATH",
          not present_b, f"checked {bins}; present: {present_b or 'none'}")
    node = subprocess.run(["which", "node"], capture_output=True)
    print(f"  [note ] the list is exhaustive of what it enumerates and no wider: `node` is "
          f"{'PRESENT' if node.returncode == 0 else 'absent'} on this box, so a GFM")
    print("            renderer is one `npm install` away.  That is not a contradiction of")
    print("            the sentence as written; it is the reason render218d.py exists.")
    print()

    print("=" * 90)
    print("6. THE EVIDENCE TABLE — the figures COVERAGE.md quotes against the committed")
    print("   files it quotes them from.")
    print("=" * 90)
    for fname, needles in (
            (f"{CONTROL_DIR}/out_battery_babf_rerun.txt",
             ["0 SILENT MISSES", "11"]),
            (f"{CONTROL_DIR}/out_battery_2216_rerun_4acd.txt", ["MISSED", "M12", "M13"]),
            (f"{CONTROL_DIR}/out_control.txt", ["NC1", "NC10"]),
            ("code/state_control_audit_babf/out_mutations.txt", ["SILENT MISS"]),
            ("code/state_audit_6a2f/out_audit.txt", [])):
        try:
            data = H.read(fname)
        except FileNotFoundError:
            claim(f"{fname} exists", False)
            continue
        claim(f"{fname} exists ({len(data)} bytes)", True)
        txt = data.decode("utf-8", "replace")
        for n in needles:
            claim(f"    and contains {n!r}", n in txt)
    claim("the pinned battery's out_audit.txt is still 96,291 bytes, as COVERAGE.md says",
          len(H.read("code/state_audit_6a2f/out_audit.txt")) == 96291,
          f"measured {len(H.read('code/state_audit_6a2f/out_audit.txt'))} bytes")
    diff = subprocess.run(["git", "-C", H.REPO, "diff", "main", "--stat", "--",
                           "code/state_audit_6a2f", "code/state_control_audit_2216",
                           "code/state_control_audit_babf"],
                          capture_output=True, text=True).stdout.strip()
    claim("and the three frozen directories have an empty diff against main",
          diff == "", f"git diff main --stat said: {diff or '(empty)'}")
    print()

    print("=" * 90)
    print("7. WHAT THE COVERAGE STATEMENT DOES **NOT** NAME.  Searched for mechanically;")
    print("   each row is a layer this audit's battery found silent (layers218d.py).")
    print("=" * 90)
    both = cov + pres.__doc__ + (dc.__doc__ or "")
    for what, terms in (
            ("that `position` and `heading` are SECTION-LOCAL, so a retraction one line "
             "earlier — across a heading — is invisible",
             ["section-local", "outside the region's own section", "across a heading",
              "in a different section", "another section"]),
            ("that the files the certified regions POINT AT are uncertified "
             "(the cell carries 7 links into attempt-mg-276d.md)",
             ["points at", "point at", "link target", "the target of", "outgoing"]),
            ("that the INSTRUMENT itself — CERTIFIED, PRESENTATION, norm() — is certified "
             "by nothing",
             ["delta_control.py is not certified", "certifies itself",
              "nothing certifies the instrument", "self-certif"]),
    ):
        found = [t for t in terms if t.lower() in both.lower()]
        named(what, bool(found),
              f"searched for {terms}; found: {found or 'none of them'}")
    print("  [note     ] `attempt-*.md` IS named in the 'Not covered' list as a FILE not")
    print("            covered.  What is not named is that a certified region DELEGATES to")
    print("            it — see the report; this row is about the delegation, not the file.")
    print()

    print("=" * 90)
    print("8. THE STATED BOUNDARY, TESTED BY MUTATION.  COVERAGE.md's value is that the")
    print("   next auditor tests the stated boundary instead of guessing — which is worth")
    print("   nothing if the stated boundary is not the real one.  Each row below is a")
    print("   sentence from 'Not covered, on purpose', turned into a mutation.")
    print("=" * 90)
    tree_h = H.Tree([H.STATE, H.README])
    snap = {r: tree_h.text(r) for r in (H.STATE, H.README)}

    def del_unrelated_row(t):
        """A ledger row that is neither the certified row nor the largest-cell row.

        NOT mg-a3d4: that row carries the largest cell in the file and section 6 asserts
        an INVARIANT about it, so deleting it exits 1 — correctly, and not as a digest.
        This audit tried mg-a3d4 first and the exit-1 was its own error, recorded here so
        the next reader does not repeat it.
        """
        lines = t[H.STATE].split("\n")
        i = H.row_index(t[H.STATE], "mg-210d")
        return {H.STATE: "\n".join(lines[:i] + lines[i + 1:])}

    def pad_region_edge(t):
        lines = t[H.README].split("\n")
        s, e = H.quote_span(t[H.README], dc.CERTIFIED[3][3])
        lines[e - 1] = lines[e - 1] + "   "
        return {H.README: "\n".join(lines)}

    def move_row_within_table(t):
        lines = t[H.STATE].split("\n")
        i = H.row_index(t[H.STATE], "mg-276d")
        row = lines.pop(i)
        j = H.row_index("\n".join(lines), "mg-a3d4")
        return {H.STATE: "\n".join(lines[:j + 1] + [row] + lines[j + 1:])}

    def inline_edit(t):
        """An INLINE-ONLY edit inside a certified region, on a line that is not the
        locator marker: three words emphasised, no word added or removed."""
        old = "so a\n> recount of Appendix A cannot rot it."
        if old not in t[H.README]:
            raise LookupError("the F1 sentence this mutation emphasises is not in the file")
        return {H.README: t[H.README].replace(
            old, "so a\n> *recount of Appendix A* cannot rot it.", 1)}

    for label, stated, fn in (
            ("'deleting an unrelated ledger row exits 0'", 0, del_unrelated_row),
            ("'padding at the outer edge of a digested region' is tolerated", 0,
             pad_region_edge),
            ("'the row's index within the table' is not certified", 0,
             move_row_within_table),
            ("'inline markup is certified as BYTES' — so an inline edit must fire", 2,
             inline_edit),
    ):
        code, _out = tree_h.probe(fn(snap))
        claim(f"COVERAGE.md says {label}: exit {stated}", code == stated,
              f"measured exit {code}")
    print()

    print("=" * 90)
    held = sum(1 for x in _ok if x)
    print(f"{held} of {len(_ok)} mechanically checkable claims in COVERAGE.md hold against "
          f"the code, the tree and a mutation.")
    print(f"{sum(1 for x in _named if x)} of {len(_named)} layers this audit found "
          f"uncontrolled are NAMED anywhere in COVERAGE.md, presentation.py or "
          f"delta_control.py.")
    print("=" * 90)
    return 0 if held == len(_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
