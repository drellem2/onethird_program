"""KERNEL for mg-7dd3 -- a token-stream scanner that shares no code with the
three instruments it audits, and an exoneration rule that reports its REASONS.

WHY NOT REUSE `kerna4ef.py`.  An audit that imports the thing it audits can
only ever confirm it.  mg-a4ef's kernel flattens whitespace and then MASKS the
Python scaffolding (`") and print("`, adjacent string literals) with regexes
tuned to the two shapes it met.  That is a list of shapes, and a list of shapes
is the failure mode this whole arc is about.

THIS KERNEL DOES IT WITHOUT A LIST.  Every character is classified once:

    alphanumeric  -> kept, lowercased
    whitespace    -> a separator
    anything else -> its own one-character token

so `print("... axiom with 0 failures on"\n      "4399 basis elements")` becomes

    ... axiom with 0 failures on " ) \n print ( " 4399 basis elements " )

and a pattern written over the WORDS crosses the scaffolding for free, because
the scaffolding is just more tokens.  No mask, nothing to tune, and the same
normaliser works on Markdown, on `.txt` and on `.sh`.  Agreement with
`kerna4ef` on the same input is then evidence; it is not shared code.

THE EXONERATION RULE REPORTS ITS REASONS, WHICH IS THE POINT.
`w3_scope.py` narrowed its rule once after a false negative, `c4_scope.py`
narrowed it again after another, and `kerna4ef.py` re-derived it and lost both
narrowings before restoring them.  Three workers have now argued about whether
a hit is exonerated.  Nobody has measured how many INDEPENDENT reasons exonerate
each hit.  A hit held down by four reasons at once is a hit whose marker is
decoration: deleting the marker the repair points at changes nothing, and the
`0` survives an edit that ought to break it.  `reasons()` returns the set, and
`d2_extent.py` prints the histogram.
"""

import re

__all__ = ["hdr", "tokens", "stream", "find", "reasons", "REASON_NAMES"]


def hdr(t):
    print("=" * 78)
    print(t)
    print("=" * 78)
    print()


def tokens(text):
    """[(token, 1-based line)] -- the whole file, nothing dropped."""
    out = []
    line = 1
    cur = []
    cur_line = 1
    for ch in text:
        if ch.isalnum():
            if not cur:
                cur_line = line
            cur.append(ch.lower())
            continue
        if cur:
            out.append(("".join(cur), cur_line))
            cur = []
        if ch.isspace():
            if ch == "\n":
                line += 1
            continue
        out.append((ch, line))
    if cur:
        out.append(("".join(cur), cur_line))
    return out


def stream(text):
    """(joined token string, per-character line map)."""
    toks = tokens(text)
    parts, lines = [], []
    for i, (t, ln) in enumerate(toks):
        if i:
            parts.append(" ")
            lines.append(ln)
        parts.append(t)
        lines.extend([ln] * len(t))
    return "".join(parts), lines


def find(text, patterns):
    """Sorted list of 1-based lines where any pattern matches the token
    stream.  Patterns are written over tokens separated by single spaces."""
    s, lmap = stream(text)
    hits = set()
    for p in patterns:
        for m in re.finditer(p, s):
            hits.add(lmap[m.start()] if lmap else 1)
    return sorted(hits)


# ---------------------------------------------------------------------------
# The exoneration rule, split into its independent clauses so each can be
# reported separately.  These are the same three clauses two previous workers
# arrived at -- naming a repair, negating the statement, sitting in a declared
# table -- deliberately NOT re-derived, because re-deriving them is how
# mg-a4ef's first version reported 14 false positives.
# ---------------------------------------------------------------------------
NAMES_A_REPAIR = re.compile(r"mg-(?:6f61|f8fa|a61f|73df|a4ef)", re.I)
NEGATES = re.compile(r"refut|STRICKEN|FORBIDDEN|WITHDRAWN|is\s+FALSE"
                     r"|no\s+longer\s+(?:holds|reads|says|in\s+force)"
                     r"|used\s+to\s+(?:say|read|assert|claim)"
                     r"|must\s+not\s+survive|does\s+not\s+hold"
                     r"|CORRECTED\s+AT\s+SOURCE", re.I)
DECLARED_TABLE = re.compile(
    r"^(STRICKEN|FORBIDDEN|CORRECTIONS|REQUIRED|PREDICTIONS|GONE_FROM_DOC"
    r"|STRICKEN_FIXTURES|CORRECTED_FIXTURES|DISARMERS|MUST_SURVIVE"
    r"|MUST_ONLY_SURVIVE_STRUCK|PATTERNS|STATEMENTS)\b\s*=")
TABLE_REACH = 30
WINDOW = 6

REASON_NAMES = ("names-a-repair", "negates", "own-negation", "declared-table")


def _in_table(raw, ln):
    for j in range(ln - 1, max(-1, ln - 1 - TABLE_REACH), -1):
        line = raw[j] if j < len(raw) else ""
        if DECLARED_TABLE.match(line):
            return True
        if line and not line[0].isspace() and "=" in line.split("#")[0] \
                and not DECLARED_TABLE.match(line):
            return False
    return False


def reasons(text, ln, own=None):
    """The SET of independent clauses that exonerate a hit at line `ln`.

    Empty set == still asserted.  Size > 1 == over-determined: the marker the
    repair points at is not what is holding the verdict up.
    """
    raw = text.splitlines()
    lo, hi = max(0, ln - 1 - WINDOW), min(len(raw), ln + WINDOW)
    near = "\n".join(raw[lo:hi])
    out = set()
    if NAMES_A_REPAIR.search(near):
        out.add("names-a-repair")
    if NEGATES.search(near):
        out.add("negates")
    if own is not None and re.search(own, near, re.I):
        out.add("own-negation")
    if _in_table(raw, ln):
        out.add("declared-table")
    return out
