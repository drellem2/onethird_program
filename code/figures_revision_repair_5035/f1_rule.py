"""F1 -- DOES THE REPAIRED RULE DO WHAT ITS DOCSTRING NOW SAYS?

The defect being repaired is a label that did not describe its code.  So the
first probe of the repair is not "is the revision excluded" -- it is "does the
new sentence survive being checked".  Both directions are scored:

  F1a  the CONSTRUCTED all-decimal short revision.  The ticket is explicit that
       a fix verified only on hex-containing revisions proves nothing, because
       those already worked.  Every row here is all decimal.
  F1b  the NEGATIVE CONTROL -- genuine figures of this corpus that carry the
       revision SHAPE.  If any of these is dropped the repair is worse than the
       defect and this probe says so.
  F1c  precision and recall over the whole corpus, scored against the git
       object database used AS AN ORACLE AND NOT AS A RULE.
  F1d  the gap, named and counted rather than left to be discovered.
  F1e  the positive control: mg-56dc's untouched copy still reads them all as
       figures, so a green F1a is a difference and not a tautology.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib5035 as B                                              # noqa: E402

BAD = 0

B.bar("F1  THE REPAIRED RULE, SCORED IN BOTH DIRECTIONS")

# ---------------------------------------------------------------------------
B.hdr("F1a  CONSTRUCTED ALL-DECIMAL SHORT REVISIONS -- are they excluded now?")

print("  Every token below is ALL DECIMAL DIGITS.  A hex-containing revision")
print("  was never the defect: `_NUMBER` cannot match one, so it was already")
print("  excluded and proves nothing.  The last three rows are constructed --")
print("  they name no object in this repository -- which is the point: the")
print("  repaired rule reads the TEXT and never asks the object database, so a")
print("  revision that does not exist yet is excluded exactly as one that does.")
print()
print("      %-14s %-9s %-9s %-8s %-8s" %
      ("token", "alldec", "resolves", "BEFORE", "AFTER"))

CONSTRUCTED = [
    ("at `%s` the census gives 9 sites", "1234567", False),
    ("at `%s` the census gives 9 sites", "3738079", True),
    ("landed at `%s`, completed through", "4785086", True),
    ("`code/x/out_a2.txt`, carried by `%s`,", "8490669", True),
    ("the sibling commit `%s` exists to prevent", "3756553", True),
    ("the number it measured at `%s`, and this tree has 43", "5988134", True),
    ("`git rev-parse` on `ec98300`, `645b5a4`, `%s`, `4203bc8`;", "3942319",
     True),
    ("re-derived at revision %s with the six verdicts", "9999999", False),
    ("pinned to `%s` and nothing else", "0123456789", False),
    ("HEAD is %s today", "12345678901234567890123456789012345678", False),
]
excl = 0
for tmpl, tok, _ in CONSTRUCTED:
    line = tmpl % tok
    before, after = B.verdicts(line)
    inb = int(tok) in before
    ina = int(tok) in after
    gone = inb and not ina
    excl += gone
    print("      %-14s %-9s %-9s %-8s %-8s  %s"
          % (tok, "yes", "yes" if B.resolves(tok) else "no",
             "FIGURE" if inb else "-", "FIGURE" if ina else "-",
             "EXCLUDED" if gone else "*** STILL A FIGURE ***"))
    if not gone:
        BAD += 1
print()
print("  population: the %d CONSTRUCTED all-decimal declared-revision lines"
      % len(CONSTRUCTED))
B.plain("...LINES on which the repair excludes the revision", excl)
print("      ^ one unit of that number is one constructed line")
print()
print("  AND THE ONE THE TICKET NAMES.  `3738079` is the revision mg-bf79's")
print("  own `r6_self.py` E2 reported as A FIGURE NO TRANSCRIPT BACKS.  It is")
print("  row 2 above and it is excluded.")

# ---------------------------------------------------------------------------
B.hdr("F1b  NEGATIVE CONTROL -- genuine figures that carry the revision SHAPE")

print("  These are real measurements of this corpus, all revision-shaped.  A")
print("  magnitude rule drops every one of them; that is why the repair is not")
print("  a magnitude rule.  Each MUST survive.")
print()
KEEP = [
    ("(16999 classes, 431723379 labelled posets)", 431723379),
    ("figures including `2147483647`, an INT_MAX in a fixture", 2147483647),
    ("st = (1103515245 * st + 12345) % (1 << 31)", 1103515245),
    ("n = 5   route: brute force over all 33554432 relations", 33554432),
    ("rng = random.Random(20260730)", 20260730),
    ("6       318    117169     37029       92369333            405", 92369333),
    ("flat evaluations               : 4770003", 4770003),
    ("11 | 50 |         21 | inherit | inherit | 1/67327446062800",
     67327446062800),
]
kept = 0
for line, v in KEEP:
    before, after = B.verdicts(line)
    survives = v in after
    kept += survives
    print("      %-16d %-9s %s" % (v, "kept" if survives else "*** DROPPED ***",
                                   line.strip()[:44]))
    if not survives:
        BAD += 1
print()
print("  population: the %d GENUINE FIGURES above, each revision-shaped" % len(KEEP))
B.plain("...GENUINE FIGURES the repair still reports", kept)
print("      ^ one unit of that number is one figure")

# ---------------------------------------------------------------------------
B.hdr("F1c  PRECISION AND RECALL over every tracked .md/.txt/.py")

print("  Scored against `git rev-parse`, used AS AN ORACLE TO LABEL TOKENS and")
print("  never as a rule -- `lib7522.figures` does not call git.  The oracle is")
print("  itself imperfect and is not treated as truth: F1d reads the rows.")
print()
occ = B.shaped_occurrences()
toks = {}
for p, i, tok, line in occ:
    d = tok in [str(x) for x in B.dropped(line)]
    toks.setdefault(tok, []).append(d)
print("  population: every tracked .md/.txt/.py at HEAD")
B.plain("...OCCURRENCES of a revision-SHAPED token", len(occ))
print("      ^ one unit of that number is one token on one line")
B.plain("...DISTINCT revision-shaped TOKENS", len(toks))
print("      ^ one unit of that number is one distinct token")
res = {t for t in toks if B.resolves(t)}
B.plain("...DISTINCT TOKENS that resolve as a git object (oracle)", len(res))
print("      ^ one unit of that number is one distinct token")
print()
exc_occ = sum(1 for p, i, t, l in occ if t in [str(x) for x in B.dropped(l)])
B.plain("...OCCURRENCES the repair now excludes", exc_occ)
print("      ^ one unit of that number is one token on one line")
exc_tok = {t for t in toks if any(toks[t])}
B.plain("...DISTINCT TOKENS excluded on at least one line", len(exc_tok))
print("      ^ one unit of that number is one distinct token")
print()
tp = len(exc_tok & res)
fp = len(exc_tok - res)
print("  AT THE GRAIN OF ONE DISTINCT TOKEN, against the oracle:")
B.plain("...EXCLUDED TOKENS that resolve   (agreeing exclusions)", tp)
print("      ^ one unit of that number is one distinct token")
B.plain("...EXCLUDED TOKENS that do NOT resolve  (the risk direction)", fp)
print("      ^ one unit of that number is one distinct token")
B.plain("...RESOLVING TOKENS never excluded anywhere  (the gap)",
        len(res - exc_tok))
print("      ^ one unit of that number is one distinct token")
print()
print("  precision %s   recall %s"
      % ("%d/%d" % (tp, len(exc_tok)) if exc_tok else "n/a",
         "%d/%d" % (tp, len(res)) if res else "n/a"))
print()
if fp:
    print("  THE NON-RESOLVING EXCLUSIONS, EVERY ONE PRINTED -- because this is")
    print("  the direction `lib70c7`'s own sentence warns about and a count")
    print("  without the rows is a count nobody can chase:")
    for t in sorted(exc_tok - res):
        where = [(p, i, l) for p, i, tk, l in occ
                 if tk == t and t in [str(x) for x in B.dropped(l)]]
        print("      %-14s %d line(s); first: %s:%d" % (t, len(where),
                                                        where[0][0],
                                                        where[0][1]))
        print("          %s" % where[0][2].strip()[:88])

# ---------------------------------------------------------------------------
B.hdr("F1d  THE GAP, COUNTED RATHER THAN DISCOVERED LATER")

print("  A resolving token the rule does NOT exclude is a MISS.  PREDICTIONS")
print("  P1b/P1c say the misses are dominated by fixed-width transcript table")
print("  columns, where the token has no words to its left at all.  Scored:")
print()
missed = sorted(res - exc_tok)
bare = 0
for t in missed:
    rows = [(p, i, l) for p, i, tk, l in occ if tk == t]
    lead = rows[0][2][:rows[0][2].find(t)] if t in rows[0][2] else ""
    isbare = not any(ch.isalpha() for ch in lead)
    bare += isbare
    print("      %-14s %-4s %s" % (t, "bare" if isbare else "cued",
                                   rows[0][0]))
    print("          %s" % rows[0][2].strip()[:88])
print()
print("  population: the %d RESOLVING TOKENS the repair does not exclude"
      % len(missed))
B.plain("...MISSES whose first occurrence has NO word to its left", bare)
print("      ^ one unit of that number is one distinct token")

# ---------------------------------------------------------------------------
B.hdr("F1f  THE RESIDUAL RISK THE COPULA FILLERS CREATE, MEASURED")

print("  `HEAD is 3738079` did not read as a declaration until F1a went red on")
print("  it, so `is/was/are/were` joined the filler list.  That admits one")
print("  construction where a GENUINE figure could be lost -- a cue word,")
print("  a copula, then a measurement.  It is not asserted rare; it is counted.")
print()
RISK = [
    "at HEAD is 431723379 labelled posets",
    "the count at HEAD was 2147483647",
    "the commit is 3738079",
]
for line in RISK:
    d = B.dropped(line)
    print("      %-46s dropped: %s" % (line[:46], d if d else "nothing"))
print()
print("  Now the corpus, which is the number that matters.  A line is AT RISK")
print("  when the repair drops a token from it AND the token is followed by a")
print("  GRAIN NOUN -- a word, on the same line, right after the number.  A")
print("  revision is not counted in units of anything; a figure is.")
risky = []
for p, i, tok, line in occ:
    if tok not in [str(x) for x in B.dropped(line)]:
        continue
    tail = line[line.find(tok) + len(tok):]
    m = re.match(r"[\s]+([A-Za-z][A-Za-z-]{2,})", tail)
    if m and m.group(1).lower() not in ("and", "the", "in", "at", "is", "was",
                                        "or", "of", "to", "with", "for"):
        risky.append((p, i, tok, m.group(1), line))
print()
print("  population: the %d OCCURRENCES the repair excludes" % exc_occ)
B.plain("...EXCLUDED OCCURRENCES followed by a candidate GRAIN NOUN", len(risky))
print("      ^ one unit of that number is one token on one line")
for p, i, tok, noun, line in risky:
    print("      %-12s followed by `%s`   %s:%d" % (tok, noun, p, i))
    print("          %s" % line.strip()[:88])
if not risky:
    print("      No excluded occurrence in the corpus is followed by a noun.")
    print("      The risk is real and its realised count at HEAD is 0.")

# ---------------------------------------------------------------------------
B.hdr("F1e  THE POSITIVE CONTROL -- can this instrument show the defect?")

print("  A negative needs an instrument that could have shown the positive.")
print("  mg-56dc's `figures(line, small=)` is left UNREPAIRED on purpose")
print("  (PREDICTIONS/P2b).  Put the F1a lines to it: if it excluded them too,")
print("  F1a would be measuring nothing.")
print()
still = 0
for tmpl, tok, _ in CONSTRUCTED:
    line = tmpl % tok
    if int(tok) in B.A.figures(line, small=2):
        still += 1
print("  population: the %d CONSTRUCTED lines of F1a" % len(CONSTRUCTED))
B.plain("...LINES where the UNREPAIRED copy still reads a FIGURE", still)
print("      ^ one unit of that number is one constructed line")
if still != len(CONSTRUCTED):
    BAD += 1
    print("      *** the control has stopped being one; F1a is not evidence ***")
else:
    print("      The control fires on every row.  F1a is a difference.")
print()
print("  AND THE FORWARDER.  `lib70c7.figures` is one statement returning")
print("  `lib7522.figures`, so it inherits the repair without being edited:")
line = "at `3738079` the census gives 9 sites"
fwd_ok = B.C.figures(line) == B.L.figures(line)
print("      lib70c7.figures agrees with lib7522.figures on the F1a line: %s"
      % ("yes" if fwd_ok else "*** NO ***"))
if not fwd_ok:
    BAD += 1

print()
B.bar("F1 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts a constructed declared revision the")
print("repair still reads as a figure, a genuine revision-shaped figure the")
print("repair drops, a control row that stopped firing, and a disagreement")
print("between the forwarder and the implementation.  It ranges over the %d"
      % len(CONSTRUCTED))
print("constructed lines, the %d negative-control figures and the %d shaped"
      % (len(KEEP), len(occ)))
print("occurrences in the corpus.  IT DOES NOT COUNT F1d's misses: an")
print("under-exclusion is the error this rule chooses to make and is a")
print("MEASUREMENT, not a fault.")
print()
print(B.finding("F1a", "the repaired rule excludes %d of %d CONSTRUCTED "
                       "all-decimal declared revisions and drops %d of %d "
                       "genuine revision-shaped figures; over the corpus it "
                       "excludes %d of %d distinct shaped tokens, %d of which "
                       "resolve and %d of which do not, leaving %d resolving "
                       "tokens unreached (%d of them bare table columns)"
                % (excl, len(CONSTRUCTED), len(KEEP) - kept, len(KEEP),
                   len(exc_tok), len(toks), tp, fp, len(missed), bare)))
sys.exit(min(BAD, 120))
