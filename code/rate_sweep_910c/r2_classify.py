"""mg-910c R2 -- the hand classification, and the CHECK that every LIVE site is repaired.

R1 counts.  This carries the judgement, one row per site, and then asserts mechanically that
every row marked LIVE now has the refutation travelling with it in the block a reader actually
reads.  A classification is a JUDGEMENT and this script does not check that the class is right;
it checks that each LIVE site is marked and that each LEFT site is named with its reason.

FIVE CLASSES.  mg-372e's sweep found the fourth and it saved three documents; this sweep needed
a fifth, because the rate had already been half-corrected once.

  LIVE      asserted as current.  STRUCK IN PLACE with mg-00a1 cited beside it.
  LIVE-OPEN asserted as an OPEN QUESTION -- "the rate is UNKNOWN", "what IS the true growth?".
            Also a claim, and also now false: mg-00a1 SETTLED it.  These exist only because
            mg-372e correctly struck the FORMULA and left the rate marked unknown; that was
            right on 2026-08-07 and stopped being right when mg-00a1 returned the same evening.
  CITED     named as the refuted claim, or inside a ~~strike~~ that already says so.  LEAVE.
  SURVIVES  a Theta(n) statement about ONE BRANCH -- the consecutive-pairs theorem
            val = (n-1)/3, or the (5n-8)/12 chord sub-family.  Both are CORRECT and LINEAR.
            A max-over-all-branches result does not touch them.  LEAVE, and do not let a
            careless reader think the strikes reached them.
  COLLISION `Theta(n^2)` or `Theta(n)` describing a DIFFERENT QUANTITY.  LEAVE, and say so.
            This is the trap: mg-00a1's own new theorem IS Theta(n^2), the baseline n(n-1)/6
            IS Theta(n^2), the two-atom law's inversion count IS Theta(n^2), the Hodge side's
            headline is 2^{Theta(n)}, and LIBweak's mobility configurations ARE Theta(n).
            A sweep on the string would have struck the new theorem.

FOUR SITES WERE NOT REACHABLE BY ANY PATTERN and were found by reading.  They are in the table
below with class LIVE-OPEN and pattern `-`.  That is the honest form of "grep is not enough":
three of them spell the claim as a bare table cell reading `unknown`, and the fourth is a
presupposition -- a sentence whose own content is TRUE and whose implied contrast is now false.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# (file, anchor substring as it appears ON MAIN, class, pattern that found it, reason)
#
# The anchor is matched against the CURRENT tree for CITED/SURVIVES/COLLISION rows (they must
# still be there, unedited) and against the current tree for LIVE rows too -- a strike keeps the
# original words inside `~~ ~~`, this corpus's own practice, so the anchor survives repair.
SITES = [
    # ---- docs/OneThird-PerSlot-AdjacencySymmetry-mg-200d.md -- the headline document ----
    ("docs/OneThird-PerSlot-AdjacencySymmetry-mg-200d.md",
     "what *is* the true growth of the disjunctive per-slot value? — is `mg-00a1`",
     "LIVE-OPEN", "RATEQ", "mg-372e's banner routes the reader to an open question mg-00a1 closed"),
    ("docs/OneThird-PerSlot-AdjacencySymmetry-mg-200d.md",
     "HEADLINE is deliberately NOT struck",
     "LIVE", "GROWS", "mg-372e deliberately left the headline; mg-00a1 refuted it"),
    ("docs/OneThird-PerSlot-AdjacencySymmetry-mg-200d.md",
     "PER-SLOT ADJACENCY SYMMETRY BUYS A FACTOR THAT GROWS WITH `n`, NOT A CONSTANT",
     "LIVE", "GROWS", "the headline itself -- REFUTED, the factor is at most 6"),
    ("docs/OneThird-PerSlot-AdjacencySymmetry-mg-200d.md",
     "STRUCK and the rate is UNKNOWN",
     "LIVE-OPEN", "RATEQ", "the rate is not unknown; mg-00a1 settled it at Theta(n^2)"),
    ("docs/OneThird-PerSlot-AdjacencySymmetry-mg-200d.md",
     "down to ~~**`(n−1)/3`** — from `Θ(n²)` to `Θ(n)`",
     "LIVE", "ARROW", "each half in its OWN code span -- MISSED by the first ARROW pattern, "
                      "found by reading, and it is why R1's separator class exists"),
    ("docs/OneThird-PerSlot-AdjacencySymmetry-mg-200d.md",
     "REFUTED at `n = 6` — UNKNOWN",
     "LIVE-OPEN", "-", "table cell, n->infinity, per-slot row -- NOT REACHED BY ANY PATTERN"),
    ("docs/OneThird-PerSlot-AdjacencySymmetry-mg-200d.md",
     "| ratio | `2/3` | `1/2` | `2/5` |",
     "LIVE-OPEN", "-", "table cell reading `unknown` -- NOT REACHED BY ANY PATTERN"),
    ("docs/OneThird-PerSlot-AdjacencySymmetry-mg-200d.md",
     "The gain is not a constant factor.",
     "LIVE", "GROWS", "it IS a constant factor and it is at most 6"),
    ("docs/OneThird-PerSlot-AdjacencySymmetry-mg-200d.md",
     'the reason is now *"the rate is unknown"*',
     "LIVE-OPEN", "RATEQ", "same paragraph; the reason is now the rate is Theta(n^2)"),
    ("docs/OneThird-PerSlot-AdjacencySymmetry-mg-200d.md",
     "becomes past `n = 5` is UNKNOWN",
     "LIVE-OPEN", "-", "§6 strike-note -- NOT REACHED BY ANY PATTERN"),
    ("docs/OneThird-PerSlot-AdjacencySymmetry-mg-200d.md",
     "whatever the aggregate form buys, it is not the `Θ(n²) → Θ(n)` drop",
     "LIVE", "ARROW", "presupposes a drop that does not exist; aggregate half is TRUE and kept"),
    ("docs/OneThird-PerSlot-AdjacencySymmetry-mg-200d.md",
     "and the all-`n` rate is UNKNOWN*",
     "LIVE-OPEN", "ARROW,RATEQ", "the closing one-line form; the rate is settled"),
    ("docs/OneThird-PerSlot-AdjacencySymmetry-mg-200d.md",
     "worth `Θ(n²) → Θ(n)` at `n ≤ 5` and the all-`n` statement is open.*~~",
     "CITED", "ARROW", "inside mg-372e's ~~strike~~ of the pre-refutation wording"),
    ("docs/OneThird-PerSlot-AdjacencySymmetry-mg-200d.md",
     "law has `Θ(n²)` inversions with every pair frozen",
     "COLLISION", "THETA2", "the TWO-ATOM LAW's inversion count -- obstruction 4, a different quantity"),

    # ---- docs/OneThird-DualCertificate-mg-131e.md -- the site the ticket named ----
    ("docs/OneThird-DualCertificate-mg-131e.md",
     "headline is not refuted.** Every value here is still linear in",
     "LIVE", "ARROW", "THE site: mg-131e left the rate standing on three points and no proof"),
    ("docs/OneThird-DualCertificate-mg-131e.md",
     "`n(n−1)/6` is still `Θ(n²) → Θ(n)` on this sub-family",
     "SURVIVES", "ARROW", "(5n-8)/12 on ONE named chord sub-family -- correct and LINEAR"),
    ("docs/OneThird-DualCertificate-mg-131e.md",
     "*What is the true growth of the disjunctive per-slot",
     "LIVE-OPEN", "RATEQ", "the successor question mg-00a1 was filed to answer, and did"),

    # ---- docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md ----
    ("docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md",
     "the ASYMPTOTIC rendering rests on the same three points and no proof",
     "LIVE", "ARROW", "'thin' understates it: the asymptotic rendering is REFUTED"),
    ("docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md",
     "**REFUTED — see below** |",
     "CITED", "ARROW", "§5.1 table cell, already struck by mg-372e and marked REFUTED"),
    ("docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md",
     "question that replaces the formula: what *is* the true growth",
     "LIVE-OPEN", "RATEQ", "mg-372e's banner routes to an open question mg-00a1 closed"),
    ("docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md",
     "an UNKNOWN rate",
     "LIVE-OPEN", "RATEQ", "§5.3 route ordering step 2 -- the rate is settled, not unknown"),
    ("docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md",
     "on ONE named sub-family as all that is established",
     "SURVIVES", "ARROW", "the sub-family clause is CORRECT; the block around it is repaired"),
    ("docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md",
     "it does not move `E[inv_e]` out of `Θ(n²)`",
     "LIVE", "-", "TRUE of the aggregate form; the implied contrast is false -- NOT REACHED BY ANY PATTERN"),

    # ---- state-history: archival ----
    ("docs/state-history/audit-mg-2eed-of-mg-b488.md",
     "### The `Θ(n²) → Θ(n)` rate is kinded too, at both sites",
     "CITED", "ARROW", "an audit OF a STATE.md landing, quoting its kinding. Archival state-history."),

    # ---- code/ : one site, and it is a stated CONCLUSION, not a transcript ----
    ("code/dual_certificate_131e/d3_refutation.py",
     "here refutes mg-200d's `Theta(n^2) -> Theta(n)` headline",
     "LIVE", "ARROW", "d3's docstring conclusion 2; output verified byte-identical after the edit"),

    # ---- the generated twin ----
    ("docs/state-of-the-wall.html",
     "every pair frozen yet <span class=\"q\">Θ(n²)</span> inversions",
     "COLLISION", "THETA2", "the TWO-ATOM LAW again. The twin carries NO per-slot rate claim at all."),
]

# A LIVE site is repaired when its enclosing block carries BOTH a citation of THIS ticket and a
# word that says the site is wrong.  Keyed on the refutation being SAID, not on the glyph -- R3's
# N1 control confirms stripping `~~` alone leaves a marked site marked.
#
# WHY `mg-910c` AND NOT `mg-00a1`.  The first version of this detector accepted either, and R3's
# N0 control then reported only 7 of the sites as unrepaired on `main` instead of 18.  The reason
# is the whole point of this ticket: mg-372e's strikes ALREADY cite `mg-00a1` -- as the OPEN
# QUESTION that replaces the formula.  A block reading "the rate is UNKNOWN (mg-00a1)" contains
# the citation and the word "REFUTED" (about the formula) and passed.  Citing mg-00a1 is exactly
# what a LIVE-OPEN site does; it is not evidence of repair.  So the check is narrowed to this
# ticket's own marker, and what it therefore establishes is honestly small: "mg-910c touched this
# block and said something was wrong in it".  The SUBSTANCE is the hand classification above --
# same disclosure mg-372e made ("s2 checks that each site is marked, not that the class is right").
CITE = re.compile(r"mg-910c")
SAYS = re.compile(r"REFUTED|refuted|STRUCK|struck|ANSWERED|is now FALSE|now false|"
                  r"Θ\(n²\)|Theta\(n\^2\)|constant factor of at most", re.I)

LIVE_CLASSES = ("LIVE", "LIVE-OPEN")


def blocks(text):
    """Blank-line-delimited blocks -- the unit a reader actually reads.

    mg-372e's s2 was line-scoped in its first version and fired 13 times against correctly
    marked prose, because a markdown strike routinely opens on one line and closes two later.
    Same widening here, for the same reason, and it is not a relaxation to reach PASS: R3
    plants live sites and confirms the block-scoped detector still fires on them.
    """
    out, cur, start = [], [], 1
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip() == "":
            if cur:
                out.append((start, "\n".join(cur)))
            cur, start = [], i + 1
        else:
            if not cur:
                start = i
            cur.append(line)
    if cur:
        out.append((start, "\n".join(cur)))
    return out


def check(root=ROOT, verbose=True):
    cache, failures, missing = {}, [], []
    counts = {}

    for path, anchor, cls, pat, reason in SITES:
        counts[cls] = counts.get(cls, 0) + 1
        full = os.path.join(root, path)
        if full not in cache:
            try:
                with open(full, encoding="utf-8") as fh:
                    cache[full] = blocks(fh.read())
            except OSError:
                cache[full] = None
        bs = cache[full]
        if bs is None:
            missing.append((path, anchor, "file not readable"))
            continue
        hit = [(ln, b) for ln, b in bs if anchor in b]
        if not hit:
            missing.append((path, anchor, "anchor not found -- the site moved or was deleted"))
            continue
        if cls in LIVE_CLASSES:
            ok = any(CITE.search(b) and SAYS.search(b) for _, b in hit)
            if not ok:
                failures.append((path, hit[0][0], anchor, cls))

    if verbose:
        print("mg-910c R2 -- CLASSIFICATION AND REPAIR CHECK")
        print("=" * 78)
        print()
        cur = None
        for path, anchor, cls, pat, reason in SITES:
            if path != cur:
                print()
                print(path)
                cur = path
            print("  [%-9s] %-11s %s" % (cls, pat, reason))
            print("               anchor: %s" % anchor[:88])
        print()
        print("=" * 78)
        print("DISTRIBUTION")
        for k in ("LIVE", "LIVE-OPEN", "CITED", "SURVIVES", "COLLISION"):
            print("  %-10s %2d" % (k, counts.get(k, 0)))
        print("  %-10s %2d" % ("TOTAL", len(SITES)))
        print()
        print("  repairable (LIVE + LIVE-OPEN): %d"
              % (counts.get("LIVE", 0) + counts.get("LIVE-OPEN", 0)))
        print("  left with a reason:            %d"
              % (counts.get("CITED", 0) + counts.get("SURVIVES", 0) + counts.get("COLLISION", 0)))
        print()

    return failures, missing, counts


def main():
    failures, missing, _ = check()
    for path, anchor, why in missing:
        print("MISSING  %s\n         %s\n         %s" % (path, anchor[:88], why))
    for path, ln, anchor, cls in failures:
        print("UNMARKED %s:%d  [%s]\n         %s" % (path, ln, cls, anchor[:88]))
    if failures or missing:
        print()
        print("FAIL — %d unmarked LIVE site(s), %d missing anchor(s)."
              % (len(failures), len(missing)))
        return 1
    print("PASS — every LIVE and LIVE-OPEN site carries this ticket's marker AND a word saying")
    print("       it is wrong, in the block a reader reads; every anchor still resolves; and")
    print("       every CITED / SURVIVES / COLLISION site is named with a reason and left.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
