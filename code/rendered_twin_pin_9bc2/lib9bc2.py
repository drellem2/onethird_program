#!/usr/bin/env python3
"""mg-9bc2 — parsing and digesting the ledger that `STATE.md` and its rendered twin share.

WHAT THIS IS FOR.  `docs/state-of-the-wall.html` carried the words `Generated 2026-07-19`
for three weeks.  A date answers WHEN a rendering was made and can never answer WHETHER it
still matches its source, so the drift was found by a human reading both files side by side
(mg-07fd, ledger row 9) rather than by anything that could fail.  mg-1abe's phrase for this
class is the one to apply: A PUBLISHER IS NOT A PIN.

The unit this module works in is the LEDGER ROW, because that is where every recorded
instance of the drift landed — mg-957a repaired nine aggregating sentences across both
files, and mg-07fd found row 9 pre-repair in the twin after mg-3329 repaired it in
`STATE.md`.  A whole-file digest would fire on every `STATE.md` commit and say nothing about
where to look; a per-row digest names the rows.

WHAT IS DIGESTED AND WHAT IS NOT.  This module digests the `STATE.md` ledger cells.  It does
NOT digest the twin's cells against them, and it must not be read as doing so: the twin is a
SUMMARY rendering, its prose is deliberately shorter than `STATE.md`'s, and no byte relation
between the two exists or should.  What the pin certifies is narrower and checkable:

    for each ledger row, the twin was last reconciled against THIS TEXT of that row.

So the control answers "which rows of `STATE.md` have moved since the twin was last
reconciled?".  It cannot answer "is the twin's summary of an unmoved row faithful?" — no
digest can, and `COVERAGE.md` beside this file says so in those words.
"""

import hashlib
import re
import unicodedata

# --------------------------------------------------------------------------------------
# normalisation
# --------------------------------------------------------------------------------------

_WS = re.compile(r"\s+")


def normalise(text):
    """Normalise a ledger cell to the bytes the digest is taken over.

    NFC so that a composed and a decomposed `λ` are the same character; whitespace collapsed
    so that re-wrapping a cell is not drift; stripped.  Nothing else — in particular, case,
    punctuation and markdown emphasis are all SIGNIFICANT, because `REFUTED` and `refuted`
    are the kind of difference this instrument exists to notice.
    """
    return _WS.sub(" ", unicodedata.normalize("NFC", text)).strip()


def digest(text):
    """SHA-256 of the normalised cell, truncated to 16 hex chars.

    Truncated because the pin block is read by humans as well as by the control, and 64 hex
    characters twelve times over is a wall.  64 bits is far past what an accidental collision
    needs; this instrument defends against DRIFT, not against a forger.
    """
    return hashlib.sha256(normalise(text).encode("utf-8")).hexdigest()[:16]


# --------------------------------------------------------------------------------------
# STATE.md — the markdown ledger
# --------------------------------------------------------------------------------------

# A ledger row starts at column 0 with `| <label> |` where the label is 1, 3a, 3b, 11, ...
_MD_ROW = re.compile(r"^\|\s*([0-9]+[a-z]?)\s*\|")
_MD_HEADER = re.compile(r"^\|\s*#\s*\|\s*Result\s*\|")


def split_md_cells(line):
    """Split a markdown table row on unescaped pipes.

    Row 5 of the ledger contains `n·leak(A)/(\\|A\\|\\|Aᶜ\\|)`, so a naive `line.split("|")`
    shreds it into six phantom cells.  A pipe preceded by a backslash is cell CONTENT.
    """
    cells, buf, i = [], [], 0
    while i < len(line):
        ch = line[i]
        if ch == "\\" and i + 1 < len(line) and line[i + 1] == "|":
            buf.append("|")          # the escape is not part of the content
            i += 2
            continue
        if ch == "|":
            cells.append("".join(buf))
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    cells.append("".join(buf))
    # A markdown row is `| a | b |`, so the split yields an empty first and last field.
    if cells and not cells[0].strip():
        cells = cells[1:]
    if cells and not cells[-1].strip():
        cells = cells[:-1]
    return [c.strip() for c in cells]


def ledger_columns(text):
    """The ledger's header cells, exactly as STATE.md spells them.

    THE PIN RECORDS THESE (mg-9876).  `row_digests` joins FOUR NAMED CELLS — result, kind,
    status, width — so anything the ledger grows beyond them is outside the pin from the day
    it is added.  A sixth column was demonstrated being added to the header AND to every row
    with section 2 byte-identical and nothing raising: `parse_state_ledger` only refuses
    FEWER than five cells.  Digesting the whole raw row instead would move every pinned
    digest and force a re-pin nobody reconciled, which is the one move this instrument
    forbids; recording the column list and comparing it does not.
    """
    for line in text.split("\n"):
        if _MD_HEADER.match(line):
            return split_md_cells(line)
    raise ValueError("no ledger header `| # | Result | Kind | Status | Width |` in STATE.md")


def parse_state_ledger(text):
    """Return [(label, {'result','kind','status','width'}, raw_line)] for the STATE.md ledger.

    The ledger is located by its header row `| # | Result | Kind | Status | Width |` and runs
    to the first line that is not a table row.  Locating it by header rather than by line
    number is deliberate: `STATE.md` has grown 32,772 -> 110,640 bytes in four days and any
    line number written down here would be wrong within the week.
    """
    lines = text.split("\n")
    start = None
    for i, line in enumerate(lines):
        if _MD_HEADER.match(line):
            start = i
            break
    if start is None:
        raise ValueError("no ledger header `| # | Result | Kind | Status | Width |` in STATE.md")

    rows = []
    for line in lines[start + 1:]:
        if not line.startswith("|"):
            break
        m = _MD_ROW.match(line)
        if not m:
            continue                  # the `|---|---|` separator
        cells = split_md_cells(line)
        if len(cells) < 5:
            raise ValueError(f"ledger row {m.group(1)!r} has {len(cells)} cells, expected 5")
        label = m.group(1)
        rows.append((label,
                     {"result": cells[1], "kind": cells[2],
                      "status": cells[3], "width": cells[4]},
                     line))
    if not rows:
        raise ValueError("ledger header found but no rows under it")
    return rows


# --------------------------------------------------------------------------------------
# the twin — the HTML ledger
# --------------------------------------------------------------------------------------

_HTML_ROW = re.compile(r"<tr>(.*?)</tr>", re.S)
_HTML_TD = re.compile(r"<td[^>]*>(.*?)</td>", re.S)
_HTML_ROWLABEL = re.compile(r'<td class="rowlabel">([0-9]+[a-z]?)</td>')
_HTML_KIND = re.compile(r'<span class="kind [a-z]+">(.*?)</span>')
_TAGS = re.compile(r"<[^>]+>")


def strip_tags(html):
    """Tags out, entities in.  Only the entities this document actually uses."""
    text = _TAGS.sub(" ", html)
    for ent, ch in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&mdash;", "—"),
                    ("&rsquo;", "’"), ("&ldquo;", "“"), ("&rdquo;", "”"),
                    ("&le;", "≤"), ("&ge;", "≥"), ("&minus;", "−"), ("&epsilon;", "ε"),
                    ("&lambda;", "λ"), ("&rarr;", "→"), ("&nbsp;", " "),
                    ("&#10007;", "✗"), ("&#9888;", "⚠"), ("&#65039;", "️")):
        text = text.replace(ent, ch)
    return text


def parse_twin_ledger(text):
    """Return [(label, {'kind': <mark>, 'text': <flattened row>})] for the twin's ledger.

    Only the row LABEL SET and the KIND MARK are extracted, and that is the honest extent of
    what the two documents can be compared on directly.  The kind mark is a controlled
    vocabulary — `U`, `U-id`, `FP`, `FP✗`, `OPEN` — so it is comparable across the summary
    boundary in a way the prose is not.
    """
    rows = []
    for block in _HTML_ROW.findall(text):
        m = _HTML_ROWLABEL.search(block)
        if not m:
            continue                  # the <thead> row
        kinds = [normalise(strip_tags(k)) for k in _HTML_KIND.findall(block)]
        cells = [strip_tags(c) for c in _HTML_TD.findall(block)]
        rows.append((m.group(1), {"kind": kinds, "text": normalise(" ".join(cells))}))
    if not rows:
        raise ValueError("no ledger rows found in the twin")
    return rows


def canonical_kind(marks):
    """Reduce a list of kind marks to the comparable form.

    Row 3b legitimately carries two — `FP✗` unconditional and `OPEN` conditional — and both
    documents say so, so the comparison is on the SET, with the warning glyph and any
    surrounding whitespace removed.
    """
    out = []
    for mark in marks:
        mark = mark.replace("⚠", "").replace("️", "").strip()
        mark = mark.strip("`*").strip()
        if mark:
            out.append(mark)
    return out


_MD_KIND_TOKEN = re.compile(r"`([A-Za-z][A-Za-z0-9✗-]*)`")


def md_kinds(kind_cell):
    """The kind marks a STATE.md kind-cell asserts, in the order it asserts them.

    Row 3b's cell is a paragraph, not a token: it reads ``⚠️ **`FP✗`** (unconditional —
    refuted) / **`OPEN`** (conditional = row 8). ~~`FP`~~ **— the `FP` mark is WITHDRAWN
    …**``.  Backticked tokens are taken in order and a token that is struck through
    (``~~`FP`~~``) or that appears after the word `WITHDRAWN` is DROPPED, because a
    withdrawn mark is the opposite of an asserted one and counting it would make the
    control agree with the twin for the wrong reason.
    """
    text = kind_cell
    # Drop struck-through spans outright.
    text = re.sub(r"~~.*?~~", " ", text)
    # Everything at or after an explicit withdrawal is commentary about a dead mark.
    cut = text.find("WITHDRAWN")
    if cut != -1:
        # keep only up to the start of the sentence that carries it
        head = text[:cut]
        text = head[:head.rfind("**—")] if "**—" in head else head
    seen, out = set(), []
    for tok in _MD_KIND_TOKEN.findall(text):
        if tok in seen:
            continue
        seen.add(tok)
        out.append(tok)
    return out


# --------------------------------------------------------------------------------------
# the pin block, which lives in the twin itself
# --------------------------------------------------------------------------------------

PIN_START = "<!-- STATE-PIN v1"
PIN_END = "STATE-PIN end -->"

_PIN_FIELD = re.compile(r"^\s*([a-z][a-z0-9-]*):\s*(.*)$")
_PIN_ROW = re.compile(r"^\s*row\s+([0-9]+[a-z]?)\s+([0-9a-f]{16})\s*$")


def parse_pin(text):
    """Read the machine-readable pin out of the twin.  Returns None if there is none."""
    i = text.find(PIN_START)
    if i == -1:
        return None
    j = text.find(PIN_END, i)
    if j == -1:
        raise ValueError(f"{PIN_START!r} present with no {PIN_END!r}")
    body = text[i + len(PIN_START):j]
    pin = {"rows": {}}
    for line in body.split("\n"):
        m = _PIN_ROW.match(line)
        if m:
            pin["rows"][m.group(1)] = m.group(2)
            continue
        m = _PIN_FIELD.match(line)
        if m and m.group(1) != "row":
            pin[m.group(1)] = m.group(2).strip()
    return pin


def row_digests(state_text):
    """The per-row digest map this instrument pins: label -> digest of the whole row."""
    out = {}
    for label, cells, _raw in parse_state_ledger(state_text):
        joined = "␟".join(cells[k] for k in ("result", "kind", "status", "width"))
        out[label] = digest(joined)
    return out


def render_pin(commit, commit_date, state_sha, digests, note, columns=""):
    """Render the pin block that goes at the top of the twin."""
    lines = [PIN_START,
             "     THIS IS THE ONLY THING IN THIS FILE THAT SAYS WHICH `STATE.md` IT IS A",
             "     RENDERING OF.  A DATE CANNOT.  Checked by:",
             "         python3 code/rendered_twin_pin_9bc2/twin_pin.py",
             "     Re-pin ONLY after actually reconciling the rows below, with --reconcile.",
             "",
             f"  source: STATE.md",
             f"  commit: {commit}",
             f"  commit-date: {commit_date}",
             f"  state-sha256: {state_sha}",
             f"  columns: {columns}",
             f"  note: {note}",
             "",
             "  Per-row digests of the STATE.md ledger AS OF THAT COMMIT.  A row whose digest",
             "  no longer matches STATE.md has moved underneath this rendering.",
             ""]
    for label in sorted(digests, key=lambda s: (int(re.match(r"\d+", s).group()), s)):
        lines.append(f"  row {label:<3} {digests[label]}")
    lines += ["", PIN_END]
    return "\n".join(lines)
