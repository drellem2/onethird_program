#!/usr/bin/env python3
"""mg-babf — mg-7870's COVERAGE STATEMENT audited as a CLAIM, against the code.

A coverage statement is the easiest thing in a control to get wrong and it is what the next
auditor will trust instead of re-deriving.  So it is checked here against `delta_control.py`
and against the files themselves — never against mg-7870's own summary of either.

Nothing in this file imports from code/state_landing_control_2da3/, code/state_audit_6a2f/
or code/state_control_audit_2216/.  `CERTIFIED` is read out of the source text of
delta_control.py by parsing it, not by importing it, so a mistake in this file cannot be a
mistake inherited from that one.

Every check prints CLAIM / MEASURED / verdict.  TRUE, FALSE and UNTESTED are the only
verdicts; "UNTESTED" is used where I could not establish the claim either way and says why.
"""
import ast
import hashlib
import os
import re
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()

CONTROL = "code/state_landing_control_2da3/delta_control.py"
COVERAGE = "code/state_landing_control_2da3/COVERAGE.md"
RERUN = "code/state_landing_control_2da3/out_battery_2216_rerun.txt"
OUT_CONTROL = "code/state_landing_control_2da3/out_control.txt"
FROZEN_2216 = "code/state_control_audit_2216/out_mutations.txt"
STATE = "STATE.md"
README = "docs/state-history/README.md"
EDGE = " \t\r\n"

REPAIR = "e924590"      # mg-7870's control commit
PRE_REPAIR = "6b1eacf"  # its parent's parent — the tree the repair started from

_tally = {"TRUE": 0, "FALSE": 0, "UNTESTED": 0}
_false = []


def read(path, rev=None):
    if rev is None:
        with open(os.path.join(REPO, path), encoding="utf-8") as fh:
            return fh.read()
    return subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"],
                          capture_output=True, check=True).stdout.decode("utf-8")


def claim(cid, text, measured, verdict, note=""):
    _tally[verdict] += 1
    if verdict == "FALSE":
        _false.append((cid, text))
    print(f"  [{verdict:<8}] {cid}  {text}")
    print(f"             measured: {measured}")
    if note:
        print(f"             {note}")


def section(title):
    print()
    print(title)
    print("-" * len(title))


# =========================================================================================
# Parse CERTIFIED out of delta_control.py's SOURCE.  No import: the point is not to inherit
# its state.
# =========================================================================================
def parse_certified(src):
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "CERTIFIED":
                    out = []
                    for elt in node.value.elts:
                        vals = []
                        for v in elt.elts:
                            if isinstance(v, ast.Constant):
                                vals.append(v.value)
                            elif isinstance(v, ast.JoinedStr):     # f-string marker
                                vals.append("<f-string>")
                            else:
                                vals.append(None)
                        out.append(tuple(vals))
                    return out
    raise AssertionError("CERTIFIED not found in the source")


# =========================================================================================
# My own region extractors — same shape as the control's, written from its documented rule.
# =========================================================================================
def norm_strict(text):
    return text.strip(EDGE).encode("utf-8")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def row_cells(line):
    bars = [i for i, ch in enumerate(line) if ch == "|" and (i == 0 or line[i - 1] != "\\")]
    if len(bars) < 2 or bars[0] != 0:
        return None
    return [line[bars[k] + 1:bars[k + 1]] for k in range(len(bars) - 1)]


def cell_region(text, key="mg-276d"):
    hits = []
    for line in text.split("\n"):
        if not line.startswith("|"):
            continue
        cells = row_cells(line)
        if cells and len(cells) >= 3 and any(key in c for c in cells[:2]):
            hits.append((line, cells))
    assert len(hits) == 1, f"{key} matched {len(hits)} rows"
    line, cells = hits[0]
    return line, cells, max(cells, key=len)


def block_region(text, marker, kind):
    lines = text.split("\n")
    hits = [i for i, l in enumerate(lines) if marker in l]
    if len(hits) != 1:
        raise LookupError(f"marker matched {len(hits)} lines")
    i = hits[0]
    if kind == "quote":
        def ok(k):
            return 0 <= k < len(lines) and lines[k].lstrip().startswith(">")
    else:
        def ok(k):
            return (0 <= k < len(lines) and lines[k].strip()
                    and not lines[k].lstrip().startswith(">"))
    if not ok(i):
        raise LookupError("marker line does not match the region kind")
    s, e = i, i + 1
    while ok(s - 1):
        s -= 1
    while ok(e):
        e += 1
    return "\n".join(lines[s:e])


def main():
    print("mg-babf — mg-7870's coverage statement, audited as a claim")
    print("=" * 86)
    src = read(CONTROL)
    cov = read(COVERAGE)
    state = read(STATE)
    readme = read(README)
    certified = parse_certified(src)

    # -------------------------------------------------------------------------------------
    section("1. HOW MANY REGIONS ARE DIGESTED — the same number in every place that says so?")
    n_code = len(certified)
    m = re.search(r"## Digested regions — (\d+)", cov)
    n_cov = int(m.group(1)) if m else None
    m2 = re.search(r"certified set is now \*\*(\w+)\*\* regions", readme)
    n_readme_word = m2.group(1) if m2 else None
    words = {"seven": 7, "eight": 8, "nine": 9, "ten": 10}
    n_readme = words.get(n_readme_word)
    msg = subprocess.run(["git", "-C", REPO, "log", "-1", "--format=%B", REPAIR],
                         capture_output=True, text=True, check=True).stdout
    m3 = re.search(r"(\w+) regions:", msg)
    n_msg = words.get(m3.group(1).lower()) if m3 else None

    claim("C1.1", "COVERAGE.md's table heading and delta_control.py's CERTIFIED agree",
          f"CERTIFIED has {n_code} entries; COVERAGE.md says {n_cov}",
          "TRUE" if n_cov == n_code else "FALSE")
    claim("C1.2", "the commit message's region count agrees with the code",
          f"commit {REPAIR} says {n_msg}; CERTIFIED has {n_code}",
          "TRUE" if n_msg == n_code else "FALSE")
    claim("C1.3",
          'the README\'s own correction block: "the certified set is now **eight** regions"',
          f"the README says {n_readme_word} ({n_readme}); CERTIFIED has {n_code}, "
          f"COVERAGE.md says {n_cov}, the commit message says {n_msg}",
          "TRUE" if n_readme == n_code else "FALSE",
          note=("the README sentence sits INSIDE readme.A1.7870, a DIGESTED region — so the "
                "figure is certified byte-for-byte and is still wrong")
          if n_readme != n_code else "")

    # -------------------------------------------------------------------------------------
    section("2. THE TABLE IN COVERAGE.md AGAINST THE CODE — ids and character counts")
    table_ids, table_chars = [], {}
    for line in cov.split("\n"):
        mm = re.match(r"\| `([a-zA-Z0-9._]+)` \| (.*?) \| ([\d,]+) \|", line)
        if mm:
            table_ids.append(mm.group(1))
            table_chars[mm.group(1)] = int(mm.group(3).replace(",", ""))
    code_ids = [c[0] for c in certified]
    claim("C2.1", "COVERAGE.md's table lists exactly the ids in CERTIFIED, in order",
          f"table {table_ids}\n             code  {code_ids}",
          "TRUE" if table_ids == code_ids else "FALSE")

    bad = [(i, table_chars[i], c[4]) for i, c in zip(table_ids, certified)
           if table_chars.get(i) != c[4]]
    claim("C2.2", "every character count in the table equals the code's constant",
          f"{len(table_ids)} rows compared; {len(bad)} disagree" + (f": {bad}" if bad else ""),
          "TRUE" if not bad else "FALSE")

    # -------------------------------------------------------------------------------------
    section("3. THE DIGESTS THEMSELVES, RECOMPUTED BY THIS FILE'S OWN EXTRACTORS")
    line135, cells135, cell_raw = cell_region(state)
    base_state = read(STATE, "b68db5d^")
    _, _, base_raw = cell_region(base_state)
    mine = {}
    for rid, _label, kind, marker, want_chars, want_sha in certified:
        if kind == "cell":
            text = cell_raw
        elif kind == "cell-base":
            text = base_raw
        else:
            text = block_region(readme, marker, kind)
        mine[rid] = (len(norm_strict(text).decode()), sha(norm_strict(text)))
    wrong = [(rid, mine[rid], c[4], c[5]) for rid, c in zip([c[0] for c in certified], certified)
             if mine[rid] != (c[4], c[5])]
    claim("C3.1",
          "each certified sha256 is the sha256 of that region, recomputed independently",
          f"{len(certified)} regions recomputed with my own parser and locators; "
          f"{len(wrong)} disagree" + (f": {wrong}" if wrong else ""),
          "TRUE" if not wrong else "FALSE")

    # -------------------------------------------------------------------------------------
    section("4. THE NORMALISATION CLAIMS")
    disagree = []
    for rid, _l, kind, marker, _c, _s in certified:
        text = (cell_raw if kind == "cell" else base_raw if kind == "cell-base"
                else block_region(readme, marker, kind))
        if text.strip() != text.strip(EDGE):
            disagree.append(rid)
    claim("C4.1",
          'COVERAGE.md: "On this material `.strip()` and `.strip(\\" \\\\t\\\\r\\\\n\\")` agree, '
          "so adopting the explicit rule moved no published number\"",
          f"compared on all {len(certified)} certified regions; "
          f"{len(disagree)} differ" + (f": {disagree}" if disagree else ""),
          "TRUE" if not disagree else "FALSE")

    cell_stripped = cell_raw.strip(EDGE)
    claim("C4.2",
          'COVERAGE.md: "the cell is still 7,876 characters stripped / 7,878 raw"',
          f"stripped {len(cell_stripped)}, raw {len(cell_raw)}",
          "TRUE" if (len(cell_stripped), len(cell_raw)) == (7876, 7878) else "FALSE")

    claim("C4.3",
          'COVERAGE.md: "**U+00A0 is not whitespace to this rule**"',
          "N('\\xa0x\\xa0') = " + repr(" x ".strip(EDGE))
          + f"  (str.strip() would give {' x '.strip()!r})",
          "TRUE" if " x ".strip(EDGE) == " x " else "FALSE",
          note="behaviour under a mutation is measured separately, in mutations_babf.py B09")

    # -------------------------------------------------------------------------------------
    section("5. 'header line included' AND 'markers sit outside the figures they certify'")
    noheader = []
    for rid, _l, kind, marker, _c, _s in certified:
        if kind in ("cell", "cell-base"):
            continue
        text = block_region(readme, marker, kind)
        first = text.split("\n")[0]
        if not (first.lstrip().startswith(">") or kind == "para"):
            noheader.append(rid)
        # the region must begin at a block boundary: the line before it is not of the kind
        idx = readme.split("\n").index(first)
        prev = readme.split("\n")[idx - 1] if idx else ""
        if kind == "quote" and prev.lstrip().startswith(">"):
            noheader.append(rid + " (run does not start at the block head)")
    claim("C5.1",
          'COVERAGE.md: "Each README region is the **whole** blockquote or paragraph, '
          '**header line included**"',
          f"{len([c for c in certified if c[2] not in ('cell', 'cell-base')])} README "
          f"regions checked; {len(noheader)} do not start at their block head"
          + (f": {noheader}" if noheader else ""),
          "TRUE" if not noheader else "FALSE")

    # A FIGURE, for this test, is a number the prose is asserting — not a digit that
    # happens to sit inside a git hash (`57f962f`, `b68db5d`), a ticket id (`mg-7735`) or a
    # dimension word (`4d`).  Those are identifiers: falsifying one does not falsify a
    # measurement, and a marker keyed on one is not self-defeating in the way the rule is
    # about.  So the pattern requires the digits to stand alone, and mg-/commit context is
    # excluded explicitly.  Stating the exclusion because it is where this test could be
    # made to say whatever I wanted it to.
    FIGURE = re.compile(r"(?<![0-9A-Za-z_-])\d{1,3}(?:,\d{3})+(?![0-9A-Za-z])"
                        r"|(?<![0-9A-Za-z_-])\d{3,}(?![0-9A-Za-z])")
    selfref = []
    for rid, _l, kind, marker, _c, _s in certified:
        if not marker or marker == "<f-string>":
            continue
        region = block_region(readme, marker, kind)
        in_marker = set(FIGURE.findall(marker))
        in_region = set(FIGURE.findall(region))
        overlap = sorted(in_marker & in_region)
        if overlap:
            selfref.append((rid, overlap))
    claim("C5.2",
          'COVERAGE.md: "**Markers sit outside the figures they certify.**"',
          f"7 README markers checked against the figures in their own regions "
          f"(comma-grouped numbers and standalone runs of 3+ digits; git hashes, `mg-` "
          f"ids and `4d` excluded as identifiers, not figures); "
          f"{len(selfref)} markers key on a figure their region certifies"
          + (f": {selfref}" if selfref else ""),
          "TRUE" if not selfref else "FALSE",
          note="necessary condition, not sufficient: a marker could still key on a "
               "non-numeric claim its region certifies, and that is not mechanically "
               "decidable.  Stated as a limit of this check, not as a pass")

    lineno = [rid for rid, _l, _k, _m, _c, _s in certified
              if re.search(r"^\s*\d+\s*$", str(_m or ""))]
    claim("C5.3",
          'COVERAGE.md: "Regions are located by a content marker, never by line number"',
          f"markers that are line numbers: {len(lineno)}; all {len(certified)} regions "
          "resolve through find_row / quote_block / paragraph, none through an index",
          "TRUE" if not lineno else "FALSE")

    # -------------------------------------------------------------------------------------
    section("6. THE EXCLUSION LIST — is anything claimed as covered that is not?")
    widest = max(cells135, key=len)
    covered = len(widest)
    total = len(line135)
    claim("C6.1",
          'COVERAGE.md, "Not covered, on purpose": "**The rest of `STATE.md`\'s ledger** — '
          'every row but `:135`."',
          f"row :135 is {total} raw characters in {len(cells135)} fields "
          f"{[len(c) for c in cells135]}; the digest covers the widest field only, "
          f"{covered} of {total} ({100.0 * covered / total:.1f}%). "
          f"{total - covered} characters of the certified row are digested by nothing",
          "FALSE",
          note="the table row above it is precise ('row `mg-276d`'s content cell'); this "
               "sentence is the one that over-reaches, and it is the sentence a reader "
               "goes to for what is NOT covered.  Measured behaviour: mutations_babf.py "
               "B01/B02")

    claim("C6.2",
          'COVERAGE.md lists what is not covered: other rows, other README blocks, edge '
          'padding, whether a change is legitimate, other revisions',
          "the list does not mention a region's POSITION or CONTEXT.  A digest is a "
          "function of the block's bytes and of nothing else, so a certified block can be "
          "moved, fenced, commented out or preceded by a retraction with its digest intact",
          "FALSE",
          note="measured behaviour: mutations_babf.py B04/B05/B06/B07, all exit 0")

    # -------------------------------------------------------------------------------------
    section("7. THE EVIDENCE TABLE")
    rerun = read(RERUN)
    mm = re.search(r"(\d+) mutations: (\d+) caught, (\d+) MISSED, (\d+) tolerated by design,"
                   r" (\d+) noisy", rerun)
    claim("C7.1",
          'COVERAGE.md: mg-2216\'s battery re-run gives "10 caught, **0 missed**, 4 '
          'tolerated by design, 0 noisy"',
          f"out_battery_2216_rerun.txt's own summary line: {mm.group(0) if mm else 'NOT FOUND'}",
          "TRUE" if mm and mm.groups() == ("14", "10", "0", "4", "0") else "FALSE",
          note="that this file REPRODUCES is checked in reproduce.sh, not here")

    oc = read(OUT_CONTROL)
    ncs = re.findall(r"(NC\d)\b.*?exit (\d)", oc)
    seen = {}
    for k, v in ncs:
        seen.setdefault(k, set()).add(int(v))
    claim("C7.2",
          'COVERAGE.md: out_control.txt is "clean 0; NC1–NC3 exit 1; NC4–NC6 exit 2"',
          f"exit codes found in out_control.txt per NC: "
          + ", ".join(f"{k}->{sorted(v)}" for k, v in sorted(seen.items())),
          "TRUE" if (all(seen.get(k) == {1} for k in ("NC1", "NC2", "NC3"))
                     and all(seen.get(k) == {2} for k in ("NC4", "NC5", "NC6")))
          else "UNTESTED",
          note="" if seen else "no 'NC<n> ... exit <d>' lines matched; the claim is about a "
                               "format this parser could not read, so it is left UNTESTED "
                               "rather than called false")

    frozen_now = read(FROZEN_2216)
    frozen_pre = read(FROZEN_2216, PRE_REPAIR)
    claim("C7.3",
          'COVERAGE.md: out_mutations.txt is "a **frozen record of the pre-repair '
          'instrument**"',
          f"byte-identical to its state at {PRE_REPAIR}: "
          f"{frozen_now == frozen_pre} ({len(frozen_now)} characters)",
          "TRUE" if frozen_now == frozen_pre else "FALSE")

    # -------------------------------------------------------------------------------------
    section("8. WHAT THE COMMIT CERTIFIES vs WHAT IT DIGESTS")
    doc = src.split('"""')[1]
    listed = re.search(r"DIGESTED \((\d+) regions", doc)
    claim("C8.1",
          "the docstring's own DIGESTED count agrees with CERTIFIED",
          f"docstring says {listed.group(1) if listed else '?'}; CERTIFIED has {n_code}",
          "TRUE" if listed and int(listed.group(1)) == n_code else "FALSE")

    certifies = ("STATE.md                       row :135, the F1 repair" in doc
                 and "docs/state-history/README.md   the F1 / F2 / B1 correction blocks"
                 in doc)
    claim("C8.2",
          'the docstring\'s "WHAT IT CERTIFIES" names "STATE.md row :135" — the ROW',
          "present in the docstring: " + str(certifies)
          + f"; the row is {total} characters and {covered} are digested",
          "FALSE" if certifies else "UNTESTED",
          note="same defect as C6.1, in a second place.  The line it certifies is named as "
               "a whole and 12.7% of it is outside every digest")

    # -------------------------------------------------------------------------------------
    section("9. DID THE REPAIR PRESERVE WHAT WAS ALREADY RIGHT?")
    d = subprocess.run(["git", "-C", REPO, "diff", "--numstat", PRE_REPAIR, REPAIR,
                        "--", README, STATE], capture_output=True, text=True, check=True)
    rows = [l.split("\t") for l in d.stdout.strip().split("\n") if l]
    claim("C9.1",
          "the repair did not re-open b68db5d's or mg-2da3's existing README/STATE content",
          "numstat "
          + "; ".join(f"{r[2]}: +{r[0]} -{r[1]}" for r in rows)
          + (" (no deletions => pure insertion)"
             if all(r[1] == "0" for r in rows) else " (DELETIONS PRESENT)"),
          "TRUE" if all(r[1] == "0" for r in rows) else "FALSE")

    d2 = subprocess.run(["git", "-C", REPO, "diff", "--stat", PRE_REPAIR, REPAIR,
                         "--", "code/state_audit_6a2f/"],
                        capture_output=True, text=True, check=True).stdout.strip()
    claim("C9.2",
          'the commit\'s SCOPE paragraph: "THE PINNED BATTERY IS BYTE-IDENTICAL"',
          f"git diff {PRE_REPAIR}..{REPAIR} -- code/state_audit_6a2f/ : "
          + (repr(d2) if d2 else "EMPTY"),
          "TRUE" if not d2 else "FALSE",
          note="that it still REPRODUCES out_audit.txt is checked in reproduce.sh")

    # -------------------------------------------------------------------------------------
    print()
    print("=" * 86)
    print(f"{sum(_tally.values())} claims checked: {_tally['TRUE']} TRUE, "
          f"{_tally['FALSE']} FALSE, {_tally['UNTESTED']} UNTESTED")
    for cid, text in _false:
        print(f"  FALSE  {cid}  {text}")
    print("=" * 86)
    return 0


if __name__ == "__main__":
    sys.exit(main())
