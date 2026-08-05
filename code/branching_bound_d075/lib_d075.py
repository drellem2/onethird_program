"""lib_d075 -- the shared reader for the mg-d075 bounding repair.

WHAT THIS IS.  A markdown claim-site reader, re-implemented for this repair rather
than imported from `code/branching_audit_19ec/e5_population.py`.  It is deliberately
a re-implementation: the parent's number is the thing under test, and a check that
runs the parent's own code cannot refute the parent's own code.  Where this file
must reproduce the parent exactly -- the liveness rule, the sentence splitter, the
POP-3 predicate -- it does so from the parent's SOURCE as read, and `s2` is the
script that proves the reproduction rather than assuming it.

THE THREE THINGS THIS FILE DEFINES, each with its population and grain named at the
point of definition, because a count whose population is not named is the defect
this whole arc is about.

  UNIT      one paragraph, or one table cell longer than 30 characters.  Fenced
            code blocks contribute no units.  This is the parent's grain and it is
            kept, so that a disagreement in the count cannot be a disagreement in
            the parser.

  LIVE      a unit outside a block quote and carrying no strike marker.  A strike
            marker is `**STRUCK` / `**CORRECTED` / `**RE-SCOPED` in the document's
            own bold-caps form, or one of the three phrases the document uses to
            introduce a superseded reading.  Withdrawn text is not a live claim.

  SENTENCE  the counting grain.  At paragraph grain the defect vanishes -- a
            paragraph can contain a bound anywhere and a coarse test scores the
            whole paragraph bounded -- which is the parent's reason and it is right.

THE TWO PREDICATES.

  STRICT    the parent's POP-3: the SENTENCE contains `33` and the SENTENCE names
            Young-Fibonacci (or the interval notation `[0-hat, w]`).

  RELAXED   this repair's: the SENTENCE contains `33` and Young-Fibonacci is named
            by the sentence OR BY THE UNIT THE SENTENCE SITS IN.  Exactly one
            clause of STRICT is relaxed -- the demand that the naming string share
            a sentence with the numeral -- and nothing else differs.

BOUNDED means the sentence carries a rank scope for the family it counts within.
It does not mean the sentence is softened.  A hedge is not a bound and `s4` is the
script that separates them.
"""

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
DOC = os.path.join(ROOT, "docs", "OneThird-Branching-Graphs-Where-This-Lives.md")
DOCS = os.path.join(ROOT, "docs")

# ---------------------------------------------------------------- the parser

STRUCK = re.compile(r"\*\*(?:STRUCK|CORRECTED|RE-SCOPED)\b"
                    r"|the version this replaces|the reading this replaces"
                    r"|the scope this adds")

SENT_SPLIT = re.compile(r"(?<=[.!?;])\s+(?=[A-Z*`(\"“])")


def sentences(text):
    return [p.strip() for p in SENT_SPLIT.split(text) if p.strip()]


def units(path):
    """(line, kind, [lines]) per claim site.  kind is 'para' or 'cell'."""
    out, fence, para, start = [], False, [], 0
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if s.startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        if s.startswith("|"):
            if para:
                out.append((start, "para", para))
                para = []
            cells = [c.strip() for c in s.strip("|").split("|")]
            if not (cells and set(cells[0]) <= set("-: ")):
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
        para.append(line)
    if para:
        out.append((start, "para", para))
    return out


def unit_text(body):
    return " ".join(l.lstrip("> ").rstrip() for l in body)


def is_live(body):
    text = unit_text(body)
    if any(l.lstrip().startswith(">") for l in body):
        return False
    return not STRUCK.search(text)


def live_sentences(path):
    """yield (line, kind, sentence, unit_text) for every live sentence."""
    for start, kind, body in units(path):
        if not is_live(body):
            continue
        text = unit_text(body)
        for s in sentences(text):
            yield start, kind, s, text


# ------------------------------------------------------- the three predicates

FIG = re.compile(r"\b33\b")
YF = re.compile(r"Young–Fibonacci|Young-Fibonacci|`\[0̂, w\]`"
                r"|`\[∅̂, w\]`")
# BOUNDED: a rank scope on the Young-Fibonacci interval family, in the sentence.
# `rank(w) <= 6` and `to rank 6` are the document's two existing forms; the
# repair adds no third form, so this regex is the parent's unchanged.
RANK6 = re.compile(r"rank\s*\(?w?\)?\s*(?:≤|<=)\s*6|to rank 6|rank 6", re.I)


def strict_sites(path):
    """The parent's POP-3 predicate.  (line, kind, sentence, bounded)."""
    out = []
    for line, kind, s, _ in live_sentences(path):
        if FIG.search(s) and YF.search(s):
            out.append((line, kind, s, bool(RANK6.search(s))))
    return out


def relaxed_sites(path):
    """STRICT with one clause relaxed: attribution may come from the UNIT."""
    out = []
    for line, kind, s, utext in live_sentences(path):
        if FIG.search(s) and (YF.search(s) or YF.search(utext)):
            out.append((line, kind, s, bool(RANK6.search(s))))
    return out


# ------------------------------------------------------------------ printing


def show_sites(sites, out, width=112, indent=39):
    for n, (line, kind, s, b) in enumerate(sites, 1):
        txt = re.sub(r"\s+", " ", s)
        print("  <%02d> line %-4d %-5s %-9s %s"
              % (n, line, kind, "BOUNDED" if b else "UNBOUNDED", txt[:width]),
              file=out)
        for j in range(width, len(txt), width):
            print(" " * indent + txt[j:j + width], file=out)
        print(file=out)


def rule(out, title=None):
    print("=" * 78, file=out)
    if title is not None:
        print(title, file=out)
        print("=" * 78, file=out)
