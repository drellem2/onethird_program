"""KERNEL for mg-a4ef -- flattened scanning, and the exoneration rule.

WHAT THIS DOES THAT THE TWO CHECKERS IT UNIFIES DO NOT.

  IT MATCHES ACROSS LINE BREAKS.  `w3_scope.py` and mg-73df's `c4_scope.py`
  scan line by line, so a forbidden sentence that wraps -- which is every
  forbidden sentence in a 79-column Python file -- can only be caught by a
  fragment of itself, and X3 had to be reduced to a co-occurrence of "axiom"
  with "4399" within three lines to be catchable at all.  Here the file is
  flattened to one string, the match runs against that, and the offset is
  mapped back to the line the match STARTS on.  A wrapped sentence is one hit
  at one line, not two hits at two, and the pattern can be the sentence.

WHAT IT KEEPS UNCHANGED, ON PURPOSE.

  THE EXONERATION RULE IS mg-73df's, NOT A NEW ONE.  A corrected statement
  may survive only where the surrounding window also says it does not hold,
  in one of three ways: name a repair; negate THIS statement in so many
  words; or sit inside a table the file declares to be a list of stricken or
  forbidden strings, which is what a checker's own source looks like.

  That rule has been narrowed twice by two workers, each time after a
  recorded false negative -- `w3_scope.py`'s bare "REPAIRED" disarmed by an
  adjacent unrelated sentence, and `c4_scope.py`'s generic "is not the ..."
  disarmed by "is not the framework this ticket is about".  A THIRD worker
  re-deriving it from scratch would lose both narrowings.  mg-a4ef's first
  version did exactly that -- it had one global marker regex and no
  per-statement negation -- and reported 19 hits of which 14 were files
  quoting the string in order to refute it.  That miss is recorded in
  OUTCOMES.md rather than quietly fixed.
"""

import re

__all__ = ["hdr", "flat", "scan", "NAMES_A_REPAIR", "NEGATES",
           "DECLARED_TABLE", "WINDOW", "TABLE_REACH"]

# 1.  Name a repair.  Narrow: a ticket id, not a mood.
NAMES_A_REPAIR = re.compile(r"mg-(?:6f61|f8fa|a61f|73df|a4ef)", re.I)

# 2.  Say, in so many words, that the sentence no longer holds.  Deliberately
#     narrow, and narrow in the two specific ways two previous workers had to
#     learn: no bare "REPAIRED", no generic "is not the ...".
NEGATES = re.compile(r"refut|STRICKEN|FORBIDDEN|WITHDRAWN|is\s+FALSE"
                     r"|no\s+longer\s+(?:holds|reads|says|in\s+force)"
                     r"|used\s+to\s+(?:say|read|assert|claim)"
                     r"|must\s+not\s+survive|does\s+not\s+hold", re.I)

# 3.  Sit inside a declared table of forbidden strings.
DECLARED_TABLE = re.compile(
    r"^(STRICKEN|FORBIDDEN|CORRECTIONS|REQUIRED|PREDICTIONS|GONE_FROM_DOC"
    r"|STRICKEN_FIXTURES|CORRECTED_FIXTURES|DISARMERS)\b\s*=")
TABLE_REACH = 30
WINDOW = 6


def hdr(t):
    print("=" * 78)
    print(t)
    print("=" * 78)
    print()


def flat(s):
    """Collapse every run of whitespace to one space and strip blockquote
    markers, so a sentence matches the same whether it is prose, a nested
    quote, or a Python string split across three source lines."""
    s = re.sub(r"(?m)^(?:\s*>)+\s?", "", s)
    # .strip() matters: _offsets() drops leading whitespace and flat() did
    # not, so the two disagreed on the same input.  Two flatteners that
    # disagree is one flattener you cannot reason about.
    return re.sub(r"\s+", " ", s).strip()


# A sentence printed by a Python file is not a sentence in that file: it is
# three string literals in three `print(` calls.  Flattening whitespace is not
# enough -- between "axiom with" and "0 failures" sit the characters `")` and
# `print("`, and no whitespace-tolerant pattern crosses them.  That is why
# mg-73df's c4_scope.py had to reduce X3 from a sentence to a co-occurrence of
# "axiom" with "4399" within three lines.
#
# These masks replace the scaffolding with SPACES OF EQUAL LENGTH, so the
# offset->line map is untouched and a hit still reports the line the sentence
# starts on.  mg-a4ef's first version did the flattening without them and
# MISSED `t6_fock_and_record.py:149` -- the exact line this ticket exists to
# fix, missed by the instrument written to fix it.  Recorded in OUTCOMES.md.
SCAFFOLD = [
    # end of a print()'s string, %-formatting, then the next print()
    re.compile(r"""["']\s*(?:%[^\n]*?)?\)\s*\n\s*print\s*\(\s*["']"""),
    # implicit concatenation of adjacent string literals
    re.compile(r"""["']\s*\n\s*["']"""),
]


def _blank(m):
    """Same length, and NEWLINES KEPT.  Blanking the newlines too costs one
    line of the count per mask, which put the first hit 30 lines above where
    it is.  Recorded in OUTCOMES.md as the second defect in this file."""
    return "".join("\n" if c == "\n" else " " for c in m.group(0))


def _mask_scaffold(text):
    for pat in SCAFFOLD:
        text = pat.sub(_blank, text)
    return text


def _offsets(text):
    """(flattened text, map) where map[i] is the 1-based line of `text` that
    flattened character i came from."""
    text = _mask_scaffold(text)
    out, lines = [], []
    lineno = 1
    prev_space = True          # leading whitespace is dropped, as in flat()
    for ch in text:
        if ch.isspace():
            if not prev_space:
                out.append(" ")
                lines.append(lineno)
                prev_space = True
            if ch == "\n":
                lineno += 1
            continue
        out.append(ch)
        lines.append(lineno)
        prev_space = False
    return "".join(out), lines


def _in_declared_table(raw, ln):
    """True if line `ln` (1-based) is inside a module-level table whose name
    DECLARED_TABLE matches, looking back at most TABLE_REACH lines."""
    for j in range(ln - 1, max(-1, ln - 1 - TABLE_REACH), -1):
        line = raw[j] if j < len(raw) else ""
        if DECLARED_TABLE.match(line):
            return True
        # a new module-level statement ends the reach
        if line and not line[0].isspace() and "=" in line.split("#")[0] \
                and not DECLARED_TABLE.match(line):
            return False
    return False


def scan(text, patterns, own=None):
    """Every match of any of `patterns`, matched against the FLATTENED text,
    as a sorted list of (line, still_asserted).

    `own` is a regex that says THIS statement no longer holds; it is the
    per-statement half of the exoneration rule, and it is what stops the
    file that REFUTES a claim from being read as asserting it.
    """
    ftext, omap = _offsets(text)
    raw = text.splitlines()
    ownre = re.compile(own, re.I) if own else None
    hits = {}
    for pat in patterns:
        for m in re.finditer(pat, ftext, re.I):
            ln = omap[min(m.start(), len(omap) - 1)] if omap else 1
            lo, hi = max(0, ln - 1 - WINDOW), min(len(raw), ln + WINDOW)
            near = "\n".join(raw[lo:hi])
            exonerated = (bool(NAMES_A_REPAIR.search(near))
                          or bool(NEGATES.search(near))
                          or (ownre is not None and bool(ownre.search(near)))
                          or _in_declared_table(raw, ln))
            hits[ln] = hits.get(ln, True) and not exonerated
    return sorted(hits.items())
