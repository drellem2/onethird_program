"""lib_aaf4 -- the reader for mg-aaf4's INDEPENDENT AUDIT of the mg-d075 bounding repair.

WHAT THIS IS, AND WHAT IT DELIBERATELY IS NOT.  It is a markdown claim-site reader
written for this audit.  It imports neither `lib_d075` nor
`code/branching_audit_19ec/e5_population.py`.  The brief is explicit about why:

  "COUNT THE SITES YOURSELF RATHER THAN TAKING 8.  An audit that inherits the
   parent's new number repeats the parent's method and can only confirm it.  Derive
   the population independently, and say what instrument you used, because the
   instrument is what decides whether you could have found a different answer."

So the instrument is named here, at the top, and every choice it makes is a choice
that could have gone the other way.

--------------------------------------------------------------------------------
THE UNIT.  One paragraph, or one table cell of more than 30 characters.  Fenced
code contributes nothing.  THIS IS THE PARENT'S UNIT AND IT IS KEPT ON PURPOSE:
`a2_reproduce.py` has to be able to return the parent's published rows, and a
disagreement about a count must not be allowed to hide inside a disagreement about
a parser.  Where I differ from the parent I differ in the POPULATION and the GRAIN,
which are stated differences, not parser accidents.

THE LIVENESS RULE.  A unit is live if it is outside a block quote and carries no
strike marker.  Same rule, re-derived from the parent's prose description rather
than copied from its regex: the bold-caps forms STRUCK / CORRECTED / RE-SCOPED, and
the three phrases the living document uses to open a superseded reading.

--------------------------------------------------------------------------------
THE TWO GRAINS.  This is where I am not the parent.

  GRAIN S -- one SENTENCE.  The parent's grain, and the grain mg-19ec used.  Its
             published numbers are 8 / 9 / 10 at this grain.

  GRAIN O -- one OCCURRENCE of the figure.  The unit of count is a single match of
             the numeral, not the sentence around it.  Two statements of the figure
             inside one sentence are TWO units at grain O and ONE at grain S.
             The parent's own section 1 insists every number be stated with the
             grain of the value; it then publishes one grain.  Grain O is the other
             one, and it is not a refinement of grain S -- it is a different
             question with a different answer.

--------------------------------------------------------------------------------
THE UNIVERSE.  The parent's widest population is `docs/*.md`.  Mine is a list of
FILES, and the list is allowed to contain files that are not in `docs/`, because
two of the four documents mg-d075 authored that state the figure are not in `docs/`
and are therefore outside every population the parent counts.

--------------------------------------------------------------------------------
BOUNDED, AND THE THING THAT IS NOT A BOUND.  `is_bounded` asks for a rank scope on
the Young-Fibonacci interval family in the SAME sentence -- the parent's standard,
kept.  `scope_class` is the part the parent has and does not apply to itself: it
separates a NUMERIC SCOPE (an inequality, a count with its denominator, a numeral
with a named unit) from a KEYWORD (the bare words population / grain / STRICT /
RELAXED / a file path).  `s4_hedge.py`'s H3 applies exactly this separation to the
living document's ten sites.  `s5_own_criticism.py`'s OWNSCOPE regex does not apply
it to the parent's own ten criticism sentences, and that gap is what `a3` measures.
"""

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
DOCS = os.path.join(ROOT, "docs")
DOC = os.path.join(DOCS, "OneThird-Branching-Graphs-Where-This-Lives.md")
PARENT = os.path.join(ROOT, "code", "branching_bound_d075")

# --------------------------------------------------------------- the parser

_STRIKE_WORDS = ("STRUCK", "CORRECTED", "RE-SCOPED")
_STRIKE_PHRASES = ("the version this replaces",
                   "the reading this replaces",
                   "the scope this adds")


def _strike_hits(text):
    """(marker, start) for every strike marker in `text`, in order."""
    hits = []
    for w in _STRIKE_WORDS:
        for m in re.finditer(r"\*\*" + w + r"\b", text):
            hits.append((m.group(0), m.start()))
    for p in _STRIKE_PHRASES:
        for m in re.finditer(re.escape(p), text):
            hits.append((p, m.start()))
    return sorted(hits, key=lambda h: h[1])


def _has_strike(text):
    return bool(_strike_hits(text))


_QUOTE = set("`\"'“‘*")


def strike_evidence(text):
    """Every strike marker in `text`, classified USE or MENTION.

    THE USE/MENTION PROBLEM, WHICH NO BRIEF IN THIS LINEAGE NAMES.  The liveness
    rule is a text match.  It cannot tell a unit that IS struck from a unit that
    QUOTES the marker while describing the rule.  A document that documents the
    liveness rule is therefore scored dead BY that rule, and every claim in it
    leaves the population silently.  MENTION here is the conservative heuristic:
    the marker is immediately flanked by a quoting character.
    """
    out = []
    for marker, i in _strike_hits(text):
        before = text[i - 1] if i else ""
        after = text[i + len(marker)] if i + len(marker) < len(text) else ""
        out.append((marker, "MENTION" if (before in _QUOTE or after in _QUOTE)
                    else "USE"))
    return out


def dead_units(path):
    """(line, kind, unit text) for every unit the liveness rule removes."""
    return [(start, kind, unit_text(body))
            for start, kind, body in units(path) if not is_live(body)]


_SENT_BOUNDARY = re.compile(r"(?<=[.!?;])\s+(?=[A-Z*`(\"“])")


def sentences(text):
    """GRAIN S.  Split on terminal punctuation followed by an opening token."""
    return [p.strip() for p in _SENT_BOUNDARY.split(text) if p.strip()]


def units(path):
    """(line, kind, [raw lines]) for every claim site.  kind in {'para','cell'}."""
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    out, in_fence, para, start = [], False, [], 0
    for i, raw in enumerate(lines, 1):
        s = raw.strip()
        if s.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if s.startswith("|"):
            if para:
                out.append((start, "para", para))
                para = []
            cells = [c.strip() for c in s.strip("|").split("|")]
            if cells and set(cells[0]) <= set("-: "):
                continue                      # the header rule of a table
            for c in cells:
                if len(c) > 30:
                    out.append((i, "cell", [c]))
            continue
        if not s:
            if para:
                out.append((start, "para", para))
                para = []
            continue
        if not para:
            start = i
        para.append(raw)
    if para:
        out.append((start, "para", para))
    return out


def unit_text(body):
    return " ".join(l.lstrip("> ").rstrip() for l in body)


def is_live(body):
    if any(l.lstrip().startswith(">") for l in body):
        return False
    return not _has_strike(unit_text(body))


def live_sentences(path):
    """(line, kind, sentence, unit text) for every live sentence of `path`."""
    for start, kind, body in units(path):
        if not is_live(body):
            continue
        text = unit_text(body)
        for s in sentences(text):
            yield start, kind, s, text


# ------------------------------------------------------------ the predicates

FIG = re.compile(r"\b33\b")
FIG_WORD = re.compile(r"thirty[- ]three", re.I)
YF = re.compile(r"Young–Fibonacci|Young-Fibonacci|`\[0̂, w\]`|`\[∅̂, w\]`")
RANK6 = re.compile(r"rank\s*\(?w?\)?\s*(?:≤|<=)\s*6|to rank 6|rank 6", re.I)


def is_bounded(sentence):
    return bool(RANK6.search(sentence))


def strict_sites(path):
    """mg-19ec's POP-3, at GRAIN S.  Name and numeral in the same sentence."""
    return [(l, k, s, is_bounded(s))
            for l, k, s, _ in live_sentences(path)
            if FIG.search(s) and YF.search(s)]


def relaxed_sites(path):
    """mg-d075's predicate, at GRAIN S.  Name may come from the unit."""
    return [(l, k, s, is_bounded(s))
            for l, k, s, u in live_sentences(path)
            if FIG.search(s) and (YF.search(s) or YF.search(u))]


def occurrences(path, relaxed=True):
    """GRAIN O.  One row per OCCURRENCE of the figure, not per sentence.

    Returns (line, kind, sentence, bounded, ordinal-within-sentence).  A sentence
    stating the figure twice yields two rows; the parent's grain yields one.
    """
    out = []
    for l, k, s, u in live_sentences(path):
        named = YF.search(s) or (relaxed and YF.search(u))
        if not named:
            continue
        b = is_bounded(s)
        for n, _ in enumerate(FIG.finditer(s), 1):
            out.append((l, k, s, b, n))
    return out


# ------------------------------------ what is a scope, and what merely reads like one

NUMERIC_SCOPE = re.compile(
    r"(?:≤|<=|≥|>=|<|>)\s*\d+"                       # an inequality with a number
    r"|\b\d+\s*(?:of|/)\s*(?:the\s+)?\d+\b"          # a count with its denominator
    r"|\brank\s*\(?w?\)?\s*(?:≤|<=)\s*\d"            # the family's own scope
    r"|\bto rank \d\b"
    r"|\ball\s+\d+\b"
    # A numeral with a named unit -- but NOT one that is the tail of a hyphenated
    # LABEL.  RESPECIFIED, and the first form's transcript is committed as
    # `out_a3_criticism_FIRSTFORM_exit1.txt`.  The first form scored "the row-10
    # sentence of section 3" and "the line-307 sentence" as numeric scopes: they
    # are ordinal labels naming ONE object, not counts of a population, and a
    # classifier that reads them as scopes says a sentence carries a scope it does
    # not carry.  The `(?<![-\w])` is the whole of the change.  DISCLOSURE: this
    # respecification moves the count in the direction of my own finding, so the
    # reasoning is here at the point of the check and both transcripts are kept.
    r"|(?<![-\w])\d+\s+(?:sites?|sentences?|files?|rows?|cells?|tokens?"
    r"|intervals?|commits?|partitions?|occurrences?|phrasings?|predictions?"
    r"|figures?|entries|instruments?|scripts?|mutations?|documents?)\b")

KEYWORD_ONLY = re.compile(
    r"\bpopulation\b|\bgrain\b|live sentences?\b|\bSTRICT\b|\bRELAXED\b"
    r"|\bPOP-\d\b|code/[a-z0-9_]+|docs/[A-Za-z0-9_.\-]+|out_[a-z0-9_]+\.txt")


def strip_emphasis(s):
    """Drop markdown emphasis before classifying.

    RESPECIFIED, and the first form's transcript is committed as
    `out_a3_criticism_FIRSTFORM_exit1.txt`.  The first form read the raw
    markdown, so `**25** entries` did not match `\\d+\\s+entries` -- the bold
    markers sit between the numeral and its unit -- and a sentence that plainly
    states a count was scored as carrying no numeric scope.  DISCLOSURE: this
    change moves the count AGAINST my own finding, and it is made for the same
    reason as the one that moves it towards it: the classifier should measure the
    sentence, not its typography.
    """
    return re.sub(r"[*`_]+", "", s)


def scope_class(sentence):
    """NUMERIC SCOPE / KEYWORD ONLY / NONE -- the H3 separation, applied to prose.

    NUMERIC wins when both are present: a sentence that says "10 of 254" has a
    scope whatever else it also says.
    """
    s = strip_emphasis(sentence)
    if NUMERIC_SCOPE.search(s):
        return "NUMERIC SCOPE"
    if KEYWORD_ONLY.search(s):
        return "KEYWORD ONLY"
    return "NONE"


def numeric_scope_text(sentence):
    m = NUMERIC_SCOPE.search(strip_emphasis(sentence))
    return m.group(0) if m else ""


def keyword_text(sentence):
    m = KEYWORD_ONLY.search(sentence)
    return m.group(0) if m else ""


# ------------------------------------------------------------------ printing


def rule(out, title=None):
    print("=" * 78, file=out)
    if title is not None:
        print(title, file=out)
        print("=" * 78, file=out)


def wrap(out, text, width=104, indent=39):
    txt = re.sub(r"\s+", " ", text)
    print(txt[:width], file=out)
    for j in range(width, len(txt), width):
        print(" " * indent + txt[j:j + width], file=out)


def show_sites(sites, out, width=104):
    for n, row in enumerate(sites, 1):
        line, kind, s, b = row[0], row[1], row[2], row[3]
        tail = "  occ #%d" % row[4] if len(row) > 4 else ""
        print("  <%02d> line %-4d %-5s %-9s " % (n, line, kind,
              "BOUNDED" if b else "UNBOUNDED"), end="", file=out)
        wrap(out, s + tail, width)
        print(file=out)


def rel(path):
    return os.path.relpath(path, ROOT)
