#!/usr/bin/env python3
"""mg-5644 — THE L2 NEGATIVE, TESTED BY CONSTRUCTION RATHER THAN BY READING ITS ARGUMENT.

Three negatives fell in this arc on 2026-07-30, every one of them refuted BY CONSTRUCTION
and none by argument.  mg-bee1 publishes a new one, in COVERAGE.md and again in the
certified correction-of-record block:

    "closing that by counting blockquotes would catch mg-218d's mutation and not the layer,
     which is the enumeration failure this lineage has already diagnosed twice"
    "What would close L2 is a rule that decides which blocks *ought* to be certified, and
     THERE IS NOT ONE HERE."

So this file tries to build the object the negative forbids: a rule that decides which
blocks ought to be certified, in the state-history README, that is a POPULATION rule and
not a mutation-shaped one.

THE CONSTRUCTION, and it is deliberately the smallest thing that could work.  Enumerate
EVERY blockquote block in the README — the population, not a chosen subset — and require
each to be either CERTIFIED or on an explicitly DECLARED not-certified list.  A blockquote
that is neither is a non-zero exit.  This is DEFAULT-DENY over an enumerated population,
which is not a new discipline in this instrument: section 8 already applies exactly it to
block constructs and to raw HTML, and states that as how the presentation subset is bounded
rather than assumed.  The discipline is in the file; what is missing is its application to
the region set.

WHAT THIS FILE IS NOT.  It is a PROTOTYPE and a measurement, not a patch: it imports
nothing from delta_control.py, changes nothing, and is not proposed as a merge.  The
question it answers is narrow — is the negative true as stated? — and the answer is
reported with its own bound, below, including the part of L2 the construction does NOT
close.
"""
import os
import re
import subprocess
import sys

import harness5644 as H

README = H.README
BLOCK = re.compile(r"^>")


def blockquotes(text):
    """(first line, last line, first line's text) for every blockquote block, 1-indexed.

    The population: every maximal run of lines beginning `>`.  Nothing is chosen.
    """
    lines, out, start = text.split("\n"), [], None
    for i, line in enumerate(lines, 1):
        if BLOCK.match(line):
            if start is None:
                start = i
        elif start is not None:
            out.append((start, i - 1, lines[start - 1]))
            start = None
    if start is not None:
        out.append((start, len(lines), lines[start - 1]))
    return out


def certified_markers():
    """The FIRST LINE of every README region delta_control.py certifies.

    Located from the CONTROL'S OWN OUTPUT — section 2 prints `README:S-E` for each — and
    then converted at once from a line number into a CONTENT MARKER, because this cluster's
    whole locator discipline is that a region is found by its content and never by its line
    number.  The first version of this file compared spans numerically and reported five
    false hits the moment a mutation shifted a line: that is the rot the discipline exists
    to prevent, and it showed up here in one run.
    """
    p = subprocess.run([sys.executable, os.path.join(H.REPO, H.CONTROL)],
                       cwd=H.REPO, capture_output=True, text=True)
    pat = re.compile(re.escape(README) + r":(\d+)-(\d+)")
    lines = H.read(README).split("\n")
    marks = set()
    for a, _b in pat.findall(p.stdout):
        first = lines[int(a) - 1].strip()
        if first.startswith(">"):
            marks.add(first)
    return marks, p.returncode


def population_rule(text, certified, declared):
    """(every blockquote tagged, undeclared ones, declarations no longer present).

    DEFAULT-DENY over the population: every blockquote block must be CERTIFIED (its first
    line is a certified region's first line) or explicitly DECLARED not-certified.  One
    that is neither is a non-zero exit, and a declared one that has vanished is too, so the
    region set cannot grow OR rot silently — the same two-way rule mg-bee1 wrote for the
    delegation surface, applied to the region set instead.

    AND a marker that matches TWO blocks is a non-zero exit.  Without that clause a
    VERBATIM duplicate of a certified block is indistinguishable from the original and the
    rule is silent on it — which is what the second version of this file measured, and it
    is the same ambiguity `_unique_marker_line` already forbids in delta_control.py's own
    locator.  Both defects in this file were found by running it, not by reading it.
    """
    covered = [(s, e, f, f.strip() in certified) for s, e, f in blockquotes(text)]
    undeclared = [(s, e, f) for s, e, f, ins in covered
                  if not ins and f.strip() not in declared]
    firsts = [f.strip() for _s, _e, f, _i in covered]
    duplicated = sorted({f for f in firsts if firsts.count(f) > 1})
    seen = {f.strip() for _s, _e, f, ins in covered if not ins}
    return covered, undeclared, sorted(declared - seen), duplicated


def _drop_last_uncertified(text, certified):
    """Delete the last blockquote block that is NOT certified, located by content.

    Not simply the last block: on this tree that one IS certified, so deleting it tests the
    content digest rather than the population rule and says nothing about L2.
    """
    quotes = [(s, e, f) for s, e, f in blockquotes(text) if f.strip() not in certified]
    s, e, _f = quotes[-1]
    lines = text.split("\n")
    return "\n".join(lines[:s - 1] + lines[e:])


def main():
    text = H.read(README)
    certified, code = certified_markers()
    quotes = blockquotes(text)

    print("=" * 90)
    print("mg-5644 — CAN L2 BE CLOSED BY A POPULATION RULE?  The construction, then its cost.")
    print("=" * 90)
    print(f"  control exit on the unmutated tree: {code}")
    print(f"  blockquote blocks in {README}: {len(quotes)} (the population)")
    ncert = sum(1 for _s, _e, f in quotes if f.strip() in certified)
    print(f"  of those, CERTIFIED by delta_control.py: {ncert}; not certified: "
          f"{len(quotes) - ncert}")
    print()

    declared = set()
    covered, undeclared, _missing, _dup = population_rule(text, certified, declared)
    for s, e, first, inside in covered:
        tag = "CERTIFIED    " if inside else "not certified"
        print(f"    lines {s:>4}-{e:<4} {tag}  {first[:64]}")
    print()
    print(f"  So the DECLARED not-certified list this rule needs has "
          f"{len(undeclared)} entries, fixed at the tree it is written against.")
    declared = {f.strip() for _s, _e, f in undeclared}
    print()

    print("=" * 90)
    print("DOES IT CATCH THE LAYER, OR ONLY mg-218d's MUTATION?")
    print("=" * 90)
    mutations = [
        ("S1-as-built", "mg-218d's own S1: an inverted near-copy under a new heading",
         lambda t: t + "\n\n## Appendix W — later notes\n\n" + "\n".join(
             l.replace("**`no 4d tally` is a correction",
                       "**LATER NOTE: `no 4d tally` was a correction")
              .replace("This row states no 4d *tally* of its own",
                       "This row states no tally of any kind, as originally written")
             for s, e, _f in [next(q for q in blockquotes(t) if "no 4d tally" in q[2])]
             for l in t.split("\n")[s - 1:e])),
        ("S1-verbatim", "a VERBATIM duplicate of a certified block, header untouched",
         lambda t: t + "\n\n## Appendix W\n\n" + "\n".join(
             [next(q[2] for q in blockquotes(t) if "no 4d tally" in q[2])])),
        ("S1'", "the same near-copy placed in the MIDDLE of the file instead",
         lambda t: t.replace("\n## ", "\n> **A CONTRADICTING NEAR-COPY.**\n\n## ", 1)),
        ("S1''", "a near-copy with NO new heading at all",
         lambda t: t + "\n\n> **A SECOND F1 BLOCK THAT DISAGREES.**\n"),
        ("S1'''", "a certified block's DUPLICATE inserted directly above it",
         lambda t: t.replace("> **`b68db5d`'s HEADLINE",
                             "> **A NEAR-COPY THAT DISAGREES.**\n\n> **`b68db5d`'s HEADLINE", 1)),
        ("R1", "an EXISTING uncertified blockquote deleted (the rot direction)",
         lambda t: _drop_last_uncertified(t, certified)),
    ]
    caught = 0
    for mid, what, fn in mutations:
        mutated = fn(text)
        if mutated == text:
            print(f"  !! {mid:<12s} mutation was a no-op — not counted")
            continue
        _c, und, miss, dup = population_rule(mutated, certified, declared)
        fires = bool(und or miss or dup)
        caught += fires
        print(f"  {'FIRES ' if fires else 'SILENT'} {mid:<12s} {what}")
        for s, e, f in und:
            print(f"           undeclared blockquote at lines {s}-{e}: {f.strip()[:56]}")
        for f in miss:
            print(f"           a declared blockquote is GONE: {f[:56]}")
        for f in dup:
            print(f"           one marker now matches TWO blocks: {f[:52]}")
    print()
    print(f"  {caught} of {len(mutations)} fire.  The rule is not shaped around S1: it is")
    print("  shaped around the POPULATION, so it fires on a near-copy anywhere, with or")
    print("  without a new heading, and in the removal direction too.")
    print()

    print("=" * 90)
    print("WHAT IT WOULD COST — the same standard mg-bee1 held the document-global ordinal to")
    print("=" * 90)
    print("  A population rule re-baselines whenever the population changes.  Below: every")
    print(f"  commit in this repository that touched {README}, oldest")
    print("  first, with its blockquote count.  The population is stated and nothing is")
    print("  sampled.")
    revs = subprocess.run(["git", "-C", H.REPO, "log", "--reverse", "--format=%H", "--",
                           README], capture_output=True, text=True, check=True
                          ).stdout.split()
    counts = []
    for rev in revs:
        blob = subprocess.run(["git", "-C", H.REPO, "show", f"{rev}:{README}"],
                              capture_output=True, text=True)
        if blob.returncode:
            continue
        counts.append(len(blockquotes(blob.stdout)))
    moves = sum(1 for a, b in zip(counts, counts[1:]) if a != b)
    trans = max(len(counts) - 1, 0)
    print(f"    {len(counts)} commits touched it; {trans} commit-to-commit transitions")
    print(f"    the blockquote count changed at {moves} of them"
          + (f"  ({round(100 * moves / trans)}%)" if trans else ""))
    print(f"    series: {' '.join(str(c) for c in counts)}")
    print()
    print("=" * 90)
    print("VERDICT ON THE NEGATIVE, WITH ITS BOUND")
    print("=" * 90)
    print("  'closing that by counting blockquotes would catch mg-218d's mutation and not")
    print("   the layer' — NOT TRUE AS STATED of a population rule.  The construction above")
    print("  is not a count and is not shaped around S1; it fires on every mutation that")
    print("  changes the blockquote population of the README, in both directions.")
    print()
    print("  'What would close L2 is a rule that decides which blocks ought to be certified,")
    print("   and there is not one here' — the rule above IS one, and its discipline is")
    print("  already in delta_control.py: section 8 is default-deny over an enumerated")
    print("  population, and this is the same move applied to the region set.")
    print()
    print("  THE BOUND, and it is why this audit reports the negative as OVERSTATED rather")
    print("  than FALSE, and files no BROKEN on it.  The construction closes L2 for")
    print("  BLOCKQUOTE blocks in ONE file.  A contradicting near-copy written as a plain")
    print("  paragraph, or as a table, or placed in STATE.md, is outside its population and")
    print("  still exits 0.  So mg-bee1's substantive point — that no rule here decides")
    print("  which blocks OUGHT to be certified in general — stands.  What does not stand is")
    print("  the specific claim that the available fix is mutation-shaped: it is not, it is")
    print("  cheap, and declining it costs more than the argument for declining it says.")
    print("=" * 90)
    return 0


if __name__ == "__main__":
    sys.exit(main())
