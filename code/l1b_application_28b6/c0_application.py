#!/usr/bin/env python3
"""mg-28b6 — A FINDING THAT IS MERGED AND NOT APPLIED IS INDISTINGUISHABLE, TO A READER, FROM A
FINDING NOBODY MADE — AND THIS ARM IS SUBJECT TO THAT DEFECT AS MUCH AS THE DOCUMENTS ARE.

`mg-0e8c` established, on Daniel's challenge, that row 8 stated the programme's central open
problem in a form its OWN PROVEN constant discharges: *an explicit absolute constant, uniform in
`n`* is exactly what `ε_sup < 1` is (`Op-Form` Claim 6.1, all `n`, L4-independent; §6.3 there
says it outright — *"(LIB-const) already holds, with constant 2/3"*), and at that constant the
SPECTRAL rendering `1 − λ_std ≤ 1` is VACUOUS, true at all 5,230 posets `n ≤ 6` with no
hypothesis at all. The open content is the SIZE — the ~50× between `ε_sup` and `ε_dem`.

`mg-0e8c` restated the row and reconciled nine sites. **Nothing checks that they stay restated.**
The phrasing that was wrong is the phrasing a hurried edit reaches for, because it is the shorter
and more quotable one, and the corpus's own record shows the sentence being reached for twice
before Daniel reached it a third time (`mg-345e:64`, `mg-6bd1:200`). This arm is what asks.

WHAT IT CHECKS

    SITES        every canonical site the restatement moved still carries its rider — the twelve
                 anchors below, each located by an ANCHOR PHRASE and each with its own stated
                 expectation. Two of them (the mermaid node and its edge) expect CONTENT rather
                 than a rider, because a diagram label has no room for a citation and the thing
                 that must survive there is `ε_sup`.
    BARE FORM    anywhere in the four canonical files, an occurrence of the existence phrasing
                 IN AN L1b CONTEXT must carry a rider or a strike within reach. This is the
                 anti-regression half: it fires on a NEW site introduced without one.

WHAT IT DOES NOT CHECK, said here so its green is not over-read.

    * **It is on STRUCTURE, not on truth** — the same split `code/facts_registry_03cf` and
      `code/concepts_gate_602d` declare, for the same reason. A rider TOKEN next to a sentence
      that says the wrong thing passes. `c1`'s wrong-direction world measures exactly that and
      stays GREEN on purpose.
    * **The BARE FORM sweep is windowed, not parsed.** A new bare sentence inserted INSIDE an
      already-ridered block passes, because the rider is within the window. It catches a new
      site elsewhere in the file, which is the failure mode that scales.
    * **Four files.** The archival sites — `docs/state-history/`, and the write-ups that state
      the form as their own subject at the time they were written — are deliberately OUT of
      scope and must NOT be edited: an attempt file records what was believed when it was
      written, and rewriting it destroys the only evidence of when the belief changed
      (`docs/OneThird-L1b-Restatement-mg-0e8c.md` §5 lists them).

A RENAME MUST BE LOUD. If an anchor is not found, or is found more than once, this arm REFUSES
(exit 2) rather than passing. A gate that quietly stops checking is worse than no gate.

EXITS 0 if the restatement is applied at every site, 1 if a site has lost it, 2 if the arm could
not reach a decision — 'could not tell' must not map onto 'nothing wrong'.
"""

import os
import re
import sys

# The tree to check. The env override exists for ONE caller — c1, which mutates COPIES of the
# four files into a scratch tree and asks this arm what it says about them. It cannot turn a red
# run green: it only relocates the tree being read, and every rule below is evaluated against
# whatever tree that is. The live tree is never written by either arm.
ROOT = os.environ.get("L1B_28B6_ROOT") or os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

STATE = "STATE.md"
CONCEPTS = os.path.join("docs", "CONCEPTS.md")
SHAPE = os.path.join("docs", "OneThird-ProofShape-mg-3af8.md")
TWIN = os.path.join("docs", "state-of-the-wall.html")

FILES = [STATE, CONCEPTS, SHAPE, TWIN]

# The rider tokens. mg-0e8c is the finding; mg-28b6 is the application of it to the site the
# finding's own enumeration missed. A strike is accepted as a rider in its own right, because
# this corpus's convention is that superseded text is struck AT THE SITE and not deleted.
RIDER = re.compile(r"mg-0e8c|mg-28b6|~~|<s>|STRUCK")

# The existence phrasing itself — the form that is DISCHARGED, in both the markdown and the
# HTML spellings.
EXISTENCE = re.compile(r"uniform(?:ly)?\s+in\s+`?n`?|explicit\s+absolute\s+constant", re.I)

# L1b context. `uniform in n` is a phrase this corpus uses about at least four DIFFERENT
# statements — `C₃^(III) = 1`, `(L*)`, `ε₀`'s form, and this one — so the sweep without this
# filter is a sweep for a phrase and not for a claim, which is `mg-8d63`'s own finding
# (docs/landing-mg-8d63-the-lstar-refutation.md:57: 58 hits under docs/, every one a different
# statement). Requiring an L1b token nearby is what makes it a claim sweep.
CONTEXT = re.compile(r"λ_std|ε_spec|ε_dem|ε_sup|inv_e|L1b|LIB-const|&lambda;_std|&epsilon;_s")

CONTEXT_CHARS = 240   # how near an L1b token must be for the phrase to be about L1b
RIDER_CHARS = 600     # how near a rider must be; also satisfied anywhere on the same line

# (label, file, anchor regex, expectation regex, scope, what the expectation means)
#
# SCOPE is `line` or `block`, and the choice is not cosmetic: it is the difference between a
# check that discriminates and one that cannot. `block` is the maximal run of non-blank lines,
# which is right for hard-wrapped markdown prose whose rider lands two lines down. It is WRONG
# for a table row, a diagram edge and an HTML element, because those sit in runs of dozens of
# sibling lines — a block-scoped check on row 8 is satisfied by a rider on row 3b, i.e. by
# something else entirely. Every site whose neighbours are siblings is therefore `line`.
SITES = [
    ("STATE.md L1b blockquote", STATE, r"^> \*\*L1b \(the wall\):\*\*",
     r"mg-0e8c", "block", "the rider naming the finding"),
    ("STATE.md Axis-1 bullet", STATE, r"^- \*\*Axis 1 — near-ordinal-sumness\*\*",
     r"mg-0e8c", "line", "the rider naming the finding"),
    ("STATE.md mermaid node C", STATE, r'^\s*C\["',
     r"ε_sup", "line", "the PROVEN constant, in the label itself — a diagram node has no room "
               "for a citation and `ε_sup` is the thing that must survive there"),
    ("STATE.md mermaid edge B->C", STATE, r'^\s*B -->\|"KIND OPEN ★ THE WALL',
     r"ε_sup", "line", "the PROVEN constant, in the edge label itself"),
    ("STATE.md row 8", STATE, r"^\| 8 \| \*\*L1b — the wall\*\*",
     r"mg-0e8c", "line", "the rider naming the finding"),
    ("CONCEPTS.md §4 the bridge", CONCEPTS, r"remaining gap: L1b",
     r"mg-0e8c", "block", "the rider naming the finding"),
    ("ProofShape §1 move 3", SHAPE, r"^> \*\*3\. L1b without the word",
     r"mg-0e8c", "block", "the rider naming the finding"),
    ("ProofShape §4 statement", SHAPE, r"^> \*\*L1b \(the wall\) — row 8",
     r"mg-0e8c", "block", "the rider naming the finding"),
    ("twin formula block", TWIN, r'<div class="form"><b>δ\(P\)',
     r"mg-0e8c", "line", "the rider naming the finding"),
    ("twin row-8 cell", TWIN, r'<td class="rowlabel">8</td>',
     r"mg-0e8c", "line", "the rider naming the finding"),
    ("twin chain link B->C", TWIN, r'<div class="clink open"><span class="pill open">open · the wall</span><span class="why"><b>L1b</b>',
     r"mg-28b6", "line", "the rider naming the application — this is the site mg-0e8c's own "
                 "enumeration missed, because the twin pin does not cover proof-chain prose"),
    ("twin chain node C", TWIN, r'<div class="cnode">E\[inv_e\]',
     r"mg-28b6", "line", "the rider naming the application"),
]


def blocks_for_anchor(text, anchor_line_index, lines):
    """The block an anchor's expectation may live in: the maximal run of non-blank lines
    containing the anchor. For the twin that is the single element line; for markdown it is the
    paragraph, blockquote (`>` separators are non-blank) or fenced diagram."""
    i = anchor_line_index
    lo = i
    while lo > 0 and lines[lo - 1].strip() != "":
        lo -= 1
    hi = i
    while hi + 1 < len(lines) and lines[hi + 1].strip() != "":
        hi += 1
    return "\n".join(lines[lo:hi + 1]), lo + 1, hi + 1


def main():
    print("=" * 92)
    print("mg-28b6 c0 — IS mg-0e8c's RESTATEMENT ACTUALLY APPLIED, AT EVERY SITE, RIGHT NOW?")
    print("=" * 92)

    refusals = []
    failures = []

    texts = {}
    for f in FILES:
        p = os.path.join(ROOT, f)
        if not os.path.exists(p):
            refusals.append("file missing: %s" % f)
            continue
        texts[f] = open(p, encoding="utf-8").read()

    if refusals:
        for r in refusals:
            print("REFUSE  %s" % r)
        print("\nc0 REFUSED (exit 2): the arm could not reach a decision.")
        return 2

    # ---- SECTION 1 — the anchored sites -------------------------------------------------
    print("\n-- 1. SITES — every canonical site the restatement moved ------------------------\n")
    print("%-28s %-34s %s" % ("site", "file", "verdict"))
    print("-" * 92)
    for label, f, anchor, expect, scope, meaning in SITES:
        lines = texts[f].split("\n")
        arx = re.compile(anchor)
        hits = [i for i, l in enumerate(lines) if arx.search(l)]
        if len(hits) != 1:
            refusals.append("site %s: anchor %r in %s matched %d lines, expected exactly 1 — "
                            "a rename must be LOUD, so this is a REFUSAL and not a pass"
                            % (label, anchor, f, len(hits)))
            print("%-28s %-34s ANCHOR NOT UNIQUE (%d)" % (label, f, len(hits)))
            continue
        if scope == "line":
            block, lo, hi = lines[hits[0]], hits[0] + 1, hits[0] + 1
        else:
            block, lo, hi = blocks_for_anchor(texts[f], hits[0], lines)
        if re.search(expect, block):
            print("%-28s %-34s ok   (lines %d-%d, carries %s)" % (label, f, lo, hi, expect))
        else:
            failures.append("%s (%s:%d) has LOST %s — %s" % (label, f, hits[0] + 1, expect, meaning))
            print("%-28s %-34s *** LOST %s ***" % (label, f, expect))

    # ---- SECTION 2 — the bare-form sweep ------------------------------------------------
    print("\n-- 2. BARE FORM — the existence phrasing in an L1b context, with no rider -------\n")
    occurrences = 0
    bare = []
    for f in FILES:
        t = texts[f]
        lines = t.split("\n")
        for m in EXISTENCE.finditer(t):
            a, b = m.start(), m.end()
            if not CONTEXT.search(t[max(0, a - CONTEXT_CHARS):b + CONTEXT_CHARS]):
                continue          # a different statement that shares the phrase
            occurrences += 1
            ln = t.count("\n", 0, a)
            window = t[max(0, a - RIDER_CHARS):b + RIDER_CHARS]
            if not (RIDER.search(window) or RIDER.search(lines[ln])):
                bare.append("%s:%d — %r with no rider or strike within reach"
                            % (f, ln + 1, m.group(0)))
    print("occurrences of the existence phrasing in an L1b context : %d" % occurrences)
    print("…of those, BARE (no rider, no strike)                    : %d" % len(bare))
    for s in bare:
        print("    *** %s" % s)
    failures.extend(bare)

    # ---- verdict -------------------------------------------------------------------------
    print()
    print("=" * 92)
    if refusals:
        for r in refusals:
            print("REFUSE  %s" % r)
        print("c0 REFUSED (exit 2): could not reach a decision — that is not the same as green.")
        return 2
    if failures:
        for x in failures:
            print("FIRED   %s" % x)
        print("c0 FIRED (exit 1): mg-0e8c's restatement is no longer applied everywhere it was.")
        return 1
    print("c0 GREEN: all %d canonical sites carry the restatement, and %d occurrences of the "
          "existence phrasing in an L1b context are each ridered or struck."
          % (len(SITES), occurrences))
    print("Green here means the STRUCTURE is intact. It does NOT mean the sentences are true — "
          "see this file's docstring and c1's wrong-direction world.")
    print("=" * 92)
    return 0


if __name__ == "__main__":
    sys.exit(main())
