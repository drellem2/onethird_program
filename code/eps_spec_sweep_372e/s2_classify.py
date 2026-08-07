#!/usr/bin/env python3
"""mg-372e — the classification, and a detector that can FAIL.

s1 counts spellings.  This one carries the hand classification of every
occurrence in `docs/` and CHECKS the two claims that a reader would otherwise
have to take on trust:

  1. the per-file occurrence counts are what the verdict says they are, and
  2. in the two REPAIRED documents, every occurrence is either inside a strike
     / refutation marker, or on the short EXPLICIT allowlist of sites that are
     true as written and were deliberately left.

Claim 2 is the one with teeth: delete a `~~` or a `REFUTED` marker and this
script fails.  A sweep that reports "done" with no distribution cannot be
checked, and a silent zero is indistinguishable from a sweep that never ran.

CLASSES
  LIVE      printed as a current value, or as a thing the programme still has
            (an OPEN conjecture counts: the reader is not told it is false)
  CITED     named as the refuted formula, or as historical/superseded
  DERIVED   inside mg-131e's or mg-94c3's own argument ABOUT it
  COLLISION the same expression, a DIFFERENT quantity -- not a site at all
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

EPS = re.compile(r"2\s*/\s*\(\s*n\s*[+]\s*1\s*\)|\\[dt]?frac\{2\}\{n\s*[+]\s*1\}")
EINV = re.compile(r"\(\s*n\s*[-−]\s*1\s*\)\s*/\s*3")
DQ = re.compile(r"2\s*/\s*\(\s*3\s*n\s*\)")
PROSE = re.compile(r"two over n plus one|per-slot constant", re.I)
ALL = [("EPS", EPS), ("EINV", EINV), ("DQ", DQ), ("PROSE", PROSE)]

# A site is MARKED if the refutation travels with it.  Scope is the enclosing
# BLOCK (the contiguous run of non-blank lines), not the line: a `~~strike~~` in
# reflowed markdown routinely opens on one line and closes two lines later, and
# the first version of this check -- scoped to the line -- fired 13 times against
# correctly-marked prose.  Widened, not tuned: the block is the unit a reader
# actually reads, and no site was moved onto the allowlist to silence it.
MARKED = re.compile(r"~~|REFUTED|STRUCK|VOID|mg-131e|mg-372e|mg-00a1|⛔")

# file -> (occurrences_expected, classification, note)
LEDGER = [
    ("docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md", "REPAIRED",
     "5 LIVE struck in place + 1 left (`:320`, scoped to n=3,4,5 and TRUE)"),
    ("docs/OneThird-PerSlot-AdjacencySymmetry-mg-200d.md", "REPAIRED",
     "8 LIVE struck in place; THEOREM 4.2, the n<=5 table and the headline left"),
    ("docs/OneThird-C3-PrefixCapture-mg-76b2.md", "CITED",
     "both sites read 'if the mg-200d route survives mg-131e' -- already correct"),
    ("docs/OneThird-C3-PrefixCapture-mg-94c3-IndependentAudit.md", "DERIVED",
     "an audit whose subject IS the supply/demand relation; labelled at every site"),
    ("docs/OneThird-DualCertificate-mg-131e.md", "DERIVED",
     "the refutation itself -- correcting it would make it disagree with its subject"),
    ("docs/state-history/audit-mg-2eed-of-mg-b488.md", "CITED",
     "an audit OF the STATE.md landing; quotes it. Archival state-history."),
    ("docs/OneThird-lambda-std-Operative-Form-IndependentAudit.md", "COLLISION",
     "`1 - lambda_std(W_n) <= 2/(n+1)` is the Cheeger bound on the poset W_n"),
    ("docs/state-history/attempt-mg-88bd.md", "COLLISION",
     "same W_n spectral-gap bound; archival state-history"),
    ("docs/OneThird-Counterexample-Under-The-Action.md", "COLLISION",
     "`n(n-1)/3` is an inversion RADIUS -- the regex matched a substring"),
]

# sites in the two repaired files that are TRUE AS WRITTEN and deliberately unmarked.
# Keyed by a distinctive substring, not a line number, so the check survives reflow.
ALLOWLIST = {
    "docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md": [
        "satisfies `6E/(n²−1) = 2/(n+1)` **exactly** at `n = 3,4,5`",
        # Two sites inside mg-372e's OWN banner.  They print the formula in order
        # to say which sites were deliberately left and what never depended on it.
        # The detector fired on both, correctly -- they carry no marker token.
        # Resolved by naming them here rather than by widening MARKED: a pattern
        # relaxed until it returns 0 is unfalsifiable, and this corpus has said so.
        "is **NOT** struck:",
        "which never depended on `2/(n+1)`",
    ],
    "docs/OneThird-PerSlot-AdjacencySymmetry-mg-200d.md": [
        "| `n` | branches | feasible |",                 # 4.2's exact n<=5 table
        "**THEOREM 4.2 (lower bound, every `n ≥ 3`).**",  # survives; mg-131e upgraded it
        "one atom, so `q = 1/3` for each and `E[inv] = (n−1)/3`",
        "- at `n = 6` the same construction's branch gives exactly `5/3 = (n−1)/3`",
        "deterministic random sweep found **nothing above `(n−1)/3`**",
        "What imposing transitivity would do is shrink the feasible set further",
        "hits `E[inv] = (n−1)/3` **and** the `1/3` cap at every `n`",
        # 4.3's own suspicion note: an assessment OF 4.3, correct as written and
        # VINDICATED by the refutation, sitting directly under the struck 4.3.
        "**Treat 4.3 with suspicion proportional to its strength.**",
    ],
}


def blocks(lines):
    """Map 1-indexed line number -> the text of its enclosing blank-line-delimited
    block.  A markdown strike spans a block, not a line."""
    out, start = {}, 0
    runs = []
    for i, line in enumerate(lines):
        if line.strip() in ("", ">"):
            if i > start:
                runs.append((start, i))
            start = i + 1
    if start < len(lines):
        runs.append((start, len(lines)))
    for a, b in runs:
        text = "\n".join(lines[a:b])
        for i in range(a, b):
            out[i + 1] = text
    return out


def scan(rel):
    path = os.path.join(ROOT, rel)
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    blk = blocks(lines)
    out = []
    for i, line in enumerate(lines, 1):
        forms = [n for n, p in ALL if p.search(line)]
        if forms:
            out.append((i, forms, line, blk.get(i, line)))
    return out


def main():
    print("mg-372e CLASSIFICATION — every occurrence in docs/, with its class")
    print("=" * 78)
    print()
    failures = []
    totals = {"occurrences": 0, "lines": 0}
    for rel, cls, note in LEDGER:
        hits = scan(rel)
        n_occ = sum(len(f) for _, f, _, _ in hits)
        totals["occurrences"] += n_occ
        totals["lines"] += len(hits)
        print(f"[{cls:9s}] {rel}")
        print(f"             {len(hits)} lines / {n_occ} form-hits — {note}")
        if cls != "REPAIRED":
            continue
        allow = ALLOWLIST.get(rel, [])
        for ln, forms, line, block in hits:
            if MARKED.search(block):
                continue
            if any(a in line for a in allow):
                continue
            failures.append(f"{rel}:{ln} UNMARKED and not on the allowlist: {line.strip()[:90]}")
        print(f"             allowlist: {len(allow)} site(s) left deliberately, true as written")
    print()
    print(f"docs/ total: {totals['lines']} lines carrying a spelling, "
          f"{totals['occurrences']} form-hits across {len(LEDGER)} documents")
    print()

    # the HTML twin, checked by name -- it has been stale before (mg-9bc2)
    twin = "docs/state-of-the-wall.html"
    tp = os.path.join(ROOT, twin)
    if not os.path.exists(tp):
        failures.append(f"{twin} ABSENT — the twin check could not run")
    else:
        n = sum(len(f) for _, f, _, _ in scan(twin))
        print(f"HTML twin {twin}: {n} occurrences -> "
              f"{'NOT a site' if n == 0 else 'A SITE — REPAIR IT'}")
        if n:
            failures.append(f"{twin} carries {n} occurrences and was not repaired")

    print()
    if failures:
        print(f"FAIL — {len(failures)} unmarked site(s):")
        for f in failures:
            print("   " + f)
        return 1
    print("PASS — every occurrence in the two repaired documents is either marked with the")
    print("       refutation or on the explicit leave-alone allowlist, and the twin is clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
