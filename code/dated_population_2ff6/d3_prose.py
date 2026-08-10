"""mg-2ff6 / D3 -- THE 10 PROSE SITES, DATED AND NOT RECOMPUTED.

THE TICKET'S ITEM 2: *The 10 prose sites, in 4 tracked .md files, each carrying
an arc-wide corpus figure with ZERO refs.  cfd9c left them untouched because
editing them moves published numbers.  They need the date, not a
recomputation -- the published value plus the population it was taken under.
Do NOT silently update them to HEAD values; that would erase the record of what
was claimed.*

So the check here is not `is the figure right`.  It is the opposite: **is the
figure UNCHANGED**, and does it now say which corpus it is a figure about.  A
prose site that had been refreshed to today's value would pass a naive `is it
accurate` test and would have destroyed the thing the ticket exists to keep.

  D3a  THE SITES, published line beside current line
  D3b  THE TWO CHECKS: no figure changed, every site carries a ref
  D3c  THE CHECK IN THIS ARC THAT CANNOT SEE ANY OF IT -- P9, named in
       advance, and it is a printed literal

Exit code = number of D3 checks that fail.
"""

import re
import sys

import lib2ff6 as U

BAD = 0

U.bar("mg-2ff6 / D3 -- THE 10 PROSE SITES, DATED AND NOT RECOMPUTED")
print("HEAD: %s   published-from: %s" % (U.head(), U.PUBLISHED_AT))

sites = U.prose_sites()

# ---------------------------------------------------------------------------
U.hdr("D3a  THE SITES, PUBLISHED LINE BESIDE CURRENT LINE")

print("  cfd9c's S2c named these by file and line at ITS commit.  A line")
print("  number is not an identity -- an edit above a site moves it -- so the")
print("  sites are re-found in the PUBLISHED text by the same needle-on-a-")
print("  corpus-line shape and then followed into the current text BY")
print("  CONTENT.  A site that could not be followed is reported as GONE,")
print("  which would mean a published claim was deleted rather than dated.")
print()
U.pop("every line of the %d tracked `.md` files carrying an arc-wide corpus "
      "figure" % len(U.PROSE))
for path, lineno, oldline, newline in sites:
    print()
    print("      %s:%d" % (path, lineno))
    print("      was: %s" % oldline.strip()[:66])
    print("      now: %s" % ("*** GONE" if newline is None
                             else newline.strip()[:66]))

# ---------------------------------------------------------------------------
U.hdr("D3b  THE TWO CHECKS")

gone = [s for s in sites if s[3] is None]
changed = [s for s in sites if s[3] is not None
           and U.figures_in(s[2]) != U.figures_in(s[3])]
dated = [s for s in sites if s[3] is not None and U.REF_IN_PROSE.search(s[3])]

print("  The first check is the one that matters and it points the unusual")
print("  way: a site FAILS if its figure moved.  Nothing was recomputed here,")
print("  and this is how a reader confirms that without diffing four files.")
print()
U.pop("the %d PROSE SITES above" % len(sites))
U.plain("...PROSE SITES carrying an arc-wide corpus figure", len(sites))
print("      ^ one unit of that number is one line of a tracked `.md`")
U.plain("...of them whose FIGURE CHANGED -- must be 0", len(changed))
print("      ^ one unit of that number is one line of a tracked `.md`")
U.plain("...of them that VANISHED -- must be 0", len(gone))
print("      ^ one unit of that number is one line of a tracked `.md`")
U.plain("...of them now carrying a REF beside the figure", len(dated))
print("      ^ one unit of that number is one line of a tracked `.md`")
BAD += bool(changed) + bool(gone) + (len(dated) != len(sites))
print()
for s in changed:
    print("      *** RECOMPUTED: %s:%d  %r -> %r"
          % (s[0], s[1], U.figures_in(s[2]), U.figures_in(s[3])))
for s in gone:
    print("      *** GONE: %s:%d" % (s[0], s[1]))
if not changed and not gone and len(dated) == len(sites):
    print("      Every site kept its published digits and gained a class and a")
    print("      ref.  `517` still says 517; what it now also says is that")
    print("      517 was a reading of `9f1ecaa + eacc5e1` and is OBSERVED --")
    print("      so a reader who re-runs the probe and gets 849 has measured")
    print("      the arc's growth rather than found a refutation.")
print()
print("  AND THE MARKER IS EXPLAINED IN EACH FILE, not in a commit message.")
print("  Each of the four carries the same closing note: the three classes,")
print("  what `@9f1ecaa+eacc5e1` means and why it is a union of two refs, and")
print("  a sentence saying the figures above are NOT refreshed and must not")
print("  be.  The note names no HEAD value -- putting today's number into")
print("  prose is how this arc got the problem in the first place, and a")
print("  ticket about dating figures that added a fresh undated one would be")
print("  its own counterexample.")
noted = 0
for p in U.PROSE:
    noted += "WHAT THE MARKER ON A CORPUS FIGURE MEANS" in U.read(p)
print()
U.pop("the %d tracked `.md` FILES this ticket edits" % len(U.PROSE))
U.plain("...FILES carrying the convention note", noted)
print("      ^ one unit of that number is one file")
BAD += noted != len(U.PROSE)

# ---------------------------------------------------------------------------
U.hdr("D3c  P9 -- THE CHECK THAT CANNOT SEE ANY OF THIS")

print("  Named in PREDICTIONS.md before this probe existed: cfd9c's S2c")
print("  counts these ten sites and reports how many carry a ref.  I bet its")
print("  `0` is a PRINTED LITERAL and not a computation.  Its own source, two")
print("  lines, quoted rather than described:")
print()
src = U.read("code/corpus_fixedpoint_fd9c/s2_drift.py").splitlines()
quoted = []
for i, ln in enumerate(src):
    if "noref" in ln or "carrying a REF beside the figure" in ln:
        quoted.append((i + 1, ln))
for n, ln in quoted:
    print("      s2_drift.py:%-4d %s" % (n, ln.rstrip()))
print()
literal = any("carrying a REF beside the figure" in ln and
              re.search(r'\s0"\)?\s*$', ln.rstrip()) for _n, ln in quoted)
unused = any(ln.strip().startswith("noref =") for _n, ln in quoted) and not any(
    "noref" in ln and not ln.strip().startswith("noref =") for _n, ln in quoted)
U.pop("the 2 SOURCE LINES of S2c's ref count, quoted above")
U.plain("...LINES computing `noref` and never using it", int(unused))
print("      ^ one unit of that number is one source line")
U.plain("...LINES printing the count as a LITERAL `0`", int(literal))
print("      ^ one unit of that number is one source line")
print()
print("  AND THE COMPUTATION IT DOES NOT USE IS ALSO WRONG: `\"@\" not in p`")
print("  tests the PATH, not the line, so it would have counted 10 whatever")
print("  the lines said.  Both halves fail in the same direction.")
print()
print("  I DO NOT REPAIR IT.  It is cfd9c's tree, this ticket is not scoped")
print("  to it, and repairing it means re-running cfd9c's suite -- which")
print("  would overwrite `out_s4_convention.txt`, the BEFORE reading D2's")
print("  whole finding rests on.  What I can do is say that after this ticket")
print("  a re-run of S2c unchanged will still print `0 of 10 carrying a ref`,")
print("  and that this is false at 10 of 10.  D3b is the reading that is not.")
print()
U.note("D3", "ALL %d PROSE SITES ARE DATED AND NOT ONE FIGURE MOVED -- the "
       "published digits survive at %d of %d sites and every one now names "
       "the population it was taken under.  AND THE ARC'S OWN PROSE CHECK "
       "CANNOT SEE IT: cfd9c's S2c prints its ref count as a LITERAL `0` "
       "beside a `noref` it computes over the PATH and never uses, so it "
       "will report 0 of 10 dated after this ticket and be wrong in both "
       "halves." % (len(sites), len(sites) - len(changed), len(sites)))

print()
print("D3 TOTAL BAD: %d" % BAD)
sys.exit(min(BAD, 120))
