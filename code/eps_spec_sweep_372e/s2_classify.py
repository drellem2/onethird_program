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

PINNED AT ONE COMMIT SINCE mg-528e, AND THE CHECK IS NOT PINNED WITH IT.  The
per-file counts on STDOUT are read at `lib372e.AS_OF`, so this transcript has a
fixed point.  But claim 2 is a CHECK, and a check pinned to a commit stops being
a check on the repository you have -- `pinnable.py`'s own `b0ae` lesson, that a
pin can DELETE THE QUESTION A SECTION ASKS rather than repair it.  So the same
check is re-run against the WORKING TREE and reported on STDERR, and the EXIT
CODE carries both halves.  Delete a `~~` today and this still exits 1; the
transcript still reproduces byte-for-byte.
"""
import re
import sys

import lib372e

ROOT = lib372e.ROOT

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


def scan(rel, lines=None):
    """Every line of `rel` carrying a spelling, with its enclosing block.

    `lines` defaults to the file AT AS_OF.  Pass the working tree's lines to ask
    the same question of the repository as it stands -- which is what the live
    half on stderr does, and the reason this takes an argument at all.
    """
    if lines is None:
        lines = lib372e.read_lines(rel)
    blk = blocks(lines)
    out = []
    for i, line in enumerate(lines, 1):
        forms = [n for n, p in ALL if p.search(line)]
        if forms:
            out.append((i, forms, line, blk.get(i, line)))
    return out


def unmarked(rel, lines=None):
    """Claim 2, computed: the sites in `rel` that are NEITHER marked NOR allowed.

    ONE SPELLING OF THE CHECK, AND THAT IS THE POINT OF EXTRACTING IT.  `s3` used
    to carry its own copy of this loop under the docstring "s2's
    marked-or-allowlisted check, run against supplied lines" -- so the control
    that proves the detector can fire was proving it about a RE-STATEMENT of the
    detector, and the two could drift with no reader able to tell which was
    wrong (mg-1344's P5).  `s3` calls this now.  A pure extraction is a claim,
    so `P57` asserts that `s3`'s four pre-declared mutations score identically
    across the change.
    """
    allow = ALLOWLIST.get(rel, [])
    bad = []
    for ln, _forms, line, block in scan(rel, lines):
        if MARKED.search(block):
            continue
        if any(a in line for a in allow):
            continue
        bad.append((ln, line))
    return bad


def live_recheck():
    """The same check, against the WORKING TREE, on stderr.  Returns a count.

    THE PIN MUST NOT DELETE THE QUESTION.  Everything on stdout is a function of
    one commit and therefore says nothing whatever about the documents as they
    stand today; before mg-528e this file's stdout was the only thing that did.
    This is `mg-724a`'s recorded/gated split: the RECORD is pinned, the GATE is
    live, and they are on different channels so neither can be mistaken for the
    other.  Its verdict is in the exit code, which is why `run_all.sh` no longer
    pipes any of this through `tee`.
    """
    say = lambda s: print(s, file=sys.stderr)
    bad, missing = [], []
    for rel, cls, _note in LEDGER:
        if cls != "REPAIRED":
            continue
        try:
            lines = lib372e.read_worktree(rel)
        except OSError:
            missing.append(rel)
            continue
        bad += ["%s:%d %s" % (rel, ln, line.strip()[:80])
                for ln, line in unmarked(rel, lines)]
    twin = "docs/state-of-the-wall.html"
    try:
        twin_hits = sum(len(f) for _, f, _, _ in
                        scan(twin, lib372e.read_worktree(twin)))
    except OSError:
        missing.append(twin)
        twin_hits = 0
    say("[live] s2 re-checked against the WORKING TREE (not part of the transcript)")
    say("[live]   unmarked site(s) in the two repaired documents : %d" % len(bad))
    say("[live]   occurrences in %s : %d" % (twin, twin_hits))
    for b in bad:
        say("[live]   UNMARKED  " + b)
    for m in missing:
        say("[live]   ABSENT FROM THE WORKING TREE  " + m)
    if not bad and not missing and not twin_hits:
        say("[live]   -> the repair still holds at the tree as it stands.")
    return len(bad) + len(missing) + twin_hits


def main():
    print("mg-372e CLASSIFICATION — every occurrence in docs/, with its class")
    print("=" * 78)
    print()
    lib372e.banner()
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
        for ln, line in unmarked(rel):
            failures.append(f"{rel}:{ln} UNMARKED and not on the allowlist: {line.strip()[:90]}")
        print(f"             allowlist: {len(allow)} site(s) left deliberately, true as written")
    print()
    print(f"docs/ total: {totals['lines']} lines carrying a spelling, "
          f"{totals['occurrences']} form-hits across {len(LEDGER)} documents")
    print()

    # the HTML twin, checked by name -- it has been stale before (mg-9bc2)
    twin = "docs/state-of-the-wall.html"
    if not lib372e.exists(twin):
        failures.append(f"{twin} ABSENT — the twin check could not run")
    else:
        n = sum(len(f) for _, f, _, _ in scan(twin))
        print(f"HTML twin {twin}: {n} occurrences -> "
              f"{'NOT a site' if n == 0 else 'A SITE — REPAIR IT'}")
        if n:
            failures.append(f"{twin} carries {n} occurrences and was not repaired")

    print()
    rc = 0
    if failures:
        print(f"FAIL — {len(failures)} unmarked site(s):")
        for f in failures:
            print("   " + f)
        rc = 1
    else:
        print("PASS — every occurrence in the two repaired documents is either marked with the")
        print("       refutation or on the explicit leave-alone allowlist, and the twin is clean.")

    # THE LIVE HALF, AND IT IS DELIBERATELY AFTER THE VERDICT: the transcript is
    # finished before anything touches the working tree, so no ordering accident
    # can put a live figure on stdout.
    return 1 if live_recheck() else rc


if __name__ == "__main__":
    sys.exit(main())
