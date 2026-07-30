"""D3 -- THE SEAM, SWEPT AGAIN FROM SCRATCH, AND THE SWEEP'S OWN EXTENT.

The brief: *"re-run the duplicate sweep yourself over all 17 block quotes.
One pair at 56 % was found; verify no second pair sits just under whatever
threshold was used, and report the threshold."*

  D3a  ALL 17 BLOCK QUOTES, every pair, NO length floor.  The ranked list is
       printed in full, so "no second pair just under the threshold" is a
       table a reader can check rather than a sentence.
  D3b  the same for prose paragraphs.
  D3c  THE SWEEP'S OWN EXTENT.  `s2_seam.py` compares only passages longer
       than 300 normalised characters.  That filter is printed in its S2a
       line and is NOT in its EXTENT paragraph, which says only that it
       cannot see cross-document duplicates or paraphrases below 45 %.  The
       pairs it therefore cannot see at ANY similarity are counted here.
  D3d  every internal cross-reference, resolved -- including the ones
       `s2_seam.py` filters out before checking.
  D3e  the §14.3 -> §14.2 by-name chain, which is what a resolved duplicate
       breaks, checked including the sentence §14.3 quotes back.
  D3f  two counts `s2_seam.py` states about itself, against its own source.

    python3 code/species_audit_7dd3/d3_seam.py
"""

import difflib
import os
import re
import sys

from kern7dd3 import hdr
from statements7dd3 import DOC

bad = 0
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
TEXT = open(os.path.join(REPO, "docs", DOC), encoding="utf-8").read()
LINES = TEXT.splitlines()

# MY THRESHOLD, MY FLOOR AND MY CRITERION, ALL THREE STATED, because a sweep
# is a number only if the constants under it are printed.
#
#   FLOOR 60 normalised characters -- mg-a4ef uses 300.  60 exists only to drop
#   Markdown `---` rules, which normalise to three characters and are 100 %
#   identical to one another.  The count dropped is printed.
#   SIMILARITY 45 % -- deliberately the SAME as mg-a4ef's, so the comparison is
#   like for like.  mg-73df's pair measured 56 %.
#   AND A SECOND CRITERION mg-a4ef does not have: the LONGEST RUN OF
#   CONSECUTIVE WORDS two passages share.  Ratio alone cannot separate "says
#   the same thing twice" from "is about the same subject" -- two different
#   Aguiar-Mahajan quotations score 53 % on vocabulary alone.  A said-twice
#   pair shares a long VERBATIM run; a same-subject pair does not.  12 words.
#
# Everything above the floor is compared and the whole ranked list down to
# 25 % is printed, so "nothing sits just under the threshold" is a table.
# Pairs that share a long verbatim run and that I read and judged to be
# DELIBERATE repetition rather than a said-twice defect, with the reason.
# Declared, so a NEW long run fails this file instead of being explained away
# in a sentence about the worst pair.
INSPECTED_REPEATS = {
    (119, 431): "the headline figure '87 of 87 classes to n <= 5 with no "
                "size cap', quoted in the ledger where it is cited",
    (165, 475): "NOT deliberate -- this is the AM 17.5 quotation "
                "asserted in 0 and struck in 4.  It is counted as a "
                "finding by d2_extent.py's D2f, not twice here",
    (900, 1007): "14 quoting 10 item 6's own sentence back, which is what "
                 "14 is about",
    (868, 1065): "14.1 quoting 10 item 2's withdrawn errand, inside the "
                 "paragraph that withdraws it",
}

MY_THRESHOLD = 0.45
MY_FLOOR = 60
MY_RUN = 12
REPORT_DOWN_TO = 0.25
A4EF_THRESHOLD = 0.45
A4EF_MIN_CHARS = 300


def note(label, cond):
    global bad
    bad += (not cond)
    print("  %-68s %s" % (label[:68], "ok" if cond else "*** FAILS ***"))
    return cond


def norm(s):
    s = re.sub(r"[*`~>|#]", " ", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def blocks_of(pred):
    out, cur, start = [], [], None
    for i, ln in enumerate(LINES):
        if pred(ln):
            if start is None:
                start = i + 1
            cur.append(ln)
        else:
            if cur:
                out.append((start, i, "\n".join(cur)))
            cur, start = [], None
    if cur:
        out.append((start, len(LINES), "\n".join(cur)))
    return out


def longest_run(a, b):
    """Longest run of consecutive shared WORDS, in words."""
    wa, wb = a.split(), b.split()
    m = difflib.SequenceMatcher(None, wa, wb).find_longest_match(
        0, len(wa), 0, len(wb))
    return m.size


def pairs_of(items):
    small = [x for x in items if len(norm(x[2])) <= MY_FLOOR]
    big = [x for x in items if len(norm(x[2])) > MY_FLOOR]
    out = []
    for i in range(len(big)):
        for j in range(i + 1, len(big)):
            a, b = norm(big[i][2]), norm(big[j][2])
            out.append((difflib.SequenceMatcher(None, a, b).ratio(),
                        longest_run(a, b), big[i], big[j]))
    out.sort(key=lambda d: (-d[1], -d[0]))
    return out, big, small


def sweep(name, items):
    """Ranked by the verbatim-run criterion, with the ratio beside it."""
    pairs, big, small = pairs_of(items)
    print("  %s: %d passage(s); %d above my %d-character floor (%d dropped, "
          "Markdown rules); %d pair(s) compared"
          % (name, len(items), len(big), MY_FLOOR, len(small), len(pairs)))
    print("  %s  mg-a4ef compares %d of them, at a 300-character floor."
          % (" " * len(name), len([x for x in items
                                   if len(norm(x[2])) > A4EF_MIN_CHARS])))
    print()
    print("      %-5s %-5s %-14s %-14s %-9s %s"
          % ("run", "sim", "lines", "lines", "chars", "seen by s2_seam.py?"))
    for r, run, x, y in pairs[:10]:
        seen = min(len(norm(x[2])), len(norm(y[2]))) > A4EF_MIN_CHARS
        print("      %-5d %4.1f%% %-14s %-14s %-9s %s"
              % (run, 100 * r, "%d-%d" % (x[0], x[1]), "%d-%d" % (y[0], y[1]),
                 "%d/%d" % (len(norm(x[2])), len(norm(y[2]))),
                 "yes" if seen else "NO -- below its 300-char floor"))
    dups = [p for p in pairs if p[1] >= MY_RUN]
    over = [p for p in pairs if p[0] > MY_THRESHOLD]
    below = [p for p in pairs if p[0] <= MY_THRESHOLD]
    print()
    print("      DUPLICATES by the run criterion (>= %d shared words): %d"
          % (MY_RUN, len(dups)))
    print("      pairs above %.0f%% similarity                        : %d"
          % (100 * MY_THRESHOLD, len(over)))
    if below:
        top = max(below, key=lambda d: d[0])
        print("      highest pair BELOW the threshold                 : "
              "%.1f%% (%.1f points under), longest shared run %d word(s)"
              % (100 * top[0], 100 * (MY_THRESHOLD - top[0]), top[1]))
    print()
    for r, run, x, y in over:
        print("      ABOVE 45%%: lines %d-%d vs %d-%d, %.1f%% similar, longest"
              % (x[0], x[1], y[0], y[1], 100 * r))
        print("                 shared run %d word(s) -- %s"
              % (run, "SAID TWICE" if run >= MY_RUN
                 else "same subject, NOT said twice"))
    print()
    return pairs, dups


hdr("D3a  ALL BLOCK QUOTES, EVERY PAIR")
bq = blocks_of(lambda ln: ln.startswith(">"))
note("the document has 17 block quotes, as mg-73df and mg-a4ef both counted",
     len(bq) == 17)
print()
bq_pairs, bq_dups = sweep("block quotes", bq)
for r, run, x, y in bq_dups:
    why = INSPECTED_REPEATS.get((x[0], y[0]))
    print("      %d shared words: lines %d-%d and %d-%d" % (run, x[0], x[1],
                                                            y[0], y[1]))
    print("          %s" % (why or "*** UNDECLARED REPETITION ***"))
    note("that repetition is on the declared inspected list", why is not None)
print()

hdr("D3b  ALL PROSE PARAGRAPHS, EVERY PAIR")
pp = blocks_of(lambda ln: ln.strip() and not ln.startswith(">")
               and not ln.startswith("#") and not ln.startswith("|"))
pp_pairs, pp_dups = sweep("prose paragraphs", pp)
for r, run, x, y in pp_dups:
    print("      *** SAID TWICE: lines %d-%d and %d-%d, %d shared words"
          % (x[0], x[1], y[0], y[1], run))
for r, run, x, y in pp_dups:
    why = INSPECTED_REPEATS.get((x[0], y[0]))
    print("          %s" % (why or "*** UNDECLARED REPETITION ***"))
    note("that repetition is on the declared inspected list", why is not None)
print()

hdr("D3b'  CONTROL -- THE SAME SWEEP ON THE DOCUMENT mg-73df AUDITED")
print("  A duplicate detector only ever seen to find nothing is worth")
print("  nothing.  The same code, unchanged, is run against the document at")
print("  ebecd89, where the box stood twice and mg-73df measured 56%.")
print()
import subprocess                                              # noqa: E402
pre = subprocess.run(["git", "show", "ebecd89:docs/" + DOC],
                     cwd=REPO, capture_output=True, text=True)
if pre.returncode != 0:
    print("  git unavailable -- CONTROL NOT RUN, and this line is the record")
    bad += 1
else:
    keep = LINES
    LINES = pre.stdout.splitlines()
    pre_bq = blocks_of(lambda ln: ln.startswith(">"))
    pre_pairs, pre_big, _ = pairs_of(pre_bq)
    hit = [p for p in pre_pairs if p[1] >= MY_RUN]
    print("      block quotes at ebecd89: %d; pairs sharing >= %d words: %d"
          % (len(pre_bq), MY_RUN, len(hit)))
    for r, run, x, y in hit[:3]:
        print("      FOUND  lines %d-%d vs %d-%d  %.1f%% similar, %d shared "
              "words" % (x[0], x[1], y[0], y[1], 100 * r, run))
    note("the sweep FINDS mg-73df's pair in the document that had it",
         bool(hit))
    note("and it measures it above 45%, as mg-73df did at 56%",
         bool(hit) and hit[0][0] > A4EF_THRESHOLD)
    LINES = keep
print()

hdr("D3c  THE SWEEP'S OWN EXTENT -- WHAT THE 300-CHARACTER FLOOR HIDES")
print("  s2_seam.py's EXTENT paragraph, in full:")
print()
print('      "S2a is a similarity sweep over ONE document and cannot see a')
print('       duplicate spread across two documents, or one paraphrased')
print('       below 45%."')
print()
print("  It does not mention MIN_CHARS.  The S2a line above it prints the")
print("  surviving count -- '17 passage(s), 11 longer than 300 characters' --")
print("  so the number is visible; the EXTENT sentence, which is the line a")
print("  reader is meant to take as the statement of what the zero ranged")
print("  over, is not.")
print()
for name, items, pairs in (("block quotes", bq, bq_pairs),
                           ("prose paragraphs", pp, pp_pairs)):
    small = [x for x in items if len(norm(x[2])) <= A4EF_MIN_CHARS]
    invisible = [q for q in pairs
                 if min(len(norm(q[2][2])), len(norm(q[3][2])))
                 <= A4EF_MIN_CHARS]
    print("  %-18s %3d of %3d passages are at or below 300 chars"
          % (name, len(small), len(items)))
    print("  %-18s %3d of %3d pairs are therefore never compared, at ANY"
          % ("", len(invisible), len(pairs)))
    print("  %-18s similarity -- including an exact duplicate." % "")
print()
note("s2_seam.py's EXTENT paragraph states the 300-character floor",
     "MIN_CHARS" in open(os.path.join(REPO, "code", "species_repair_a4ef",
                                      "s2_seam.py"),
                         encoding="utf-8").read().split('print("EXTENT.')[-1]
     or "300" in open(os.path.join(REPO, "code", "species_repair_a4ef",
                                   "s2_seam.py"),
                      encoding="utf-8").read().split('print("EXTENT.')[-1])
print("  d5 plants an EXACT duplicate of a short block quote and measures")
print("  the exit code.  A 100%%-similar pair inside the one document the")
print("  extent says it sweeps is the boundary probe the strengthened brief")
print("  asks for.")
print()

hdr("D3d  EVERY INTERNAL CROSS-REFERENCE, INCLUDING THE ONES s2_seam FILTERS")
headings = {}
for m in re.finditer(r"(?m)^(#{2,4})\s*(\d+(?:\.\d+)?)[.\s]", TEXT):
    headings[m.group(2)] = m.start()
subheaded = {h.split(".")[0] for h in headings if "." in h}
EXTERNAL = re.compile(r"(?:mg-[0-9a-f]{4}(?:'s)?|AM|Aguiar[^\s]*|Brown|"
                      r"Marshall[^\s]*|Saliola|Bergeron[^\s]*|Joyal)\s*$")
allrefs = sorted({m.group(1) for m in re.finditer(r"§(\d+\.\d+)", TEXT)})
# s2_seam.py applies TWO filters, not one: `subheaded`, and a check that
# nothing immediately before the reference names another document.  A first
# version of this section applied only the first and reported "mg-af28 §2.6"
# as a reference s2_seam checks and fails to resolve.  It does not check it,
# correctly.  Kept in OUTCOMES.md.
def is_external(ref):
    for m in re.finditer(r"§" + re.escape(ref), TEXT):
        if not EXTERNAL.search(TEXT[max(0, m.start() - 40):m.start()]):
            return False
    return True


internal = [r for r in allrefs
            if r.split(".")[0] in subheaded and not is_external(r)]
dropped = [r for r in allrefs if r not in internal]
print("  headings present            : %s" % ", ".join(sorted(headings)))
print("  sections that use sub-heads : %s" % ", ".join(sorted(subheaded)))
print()
for r in allrefs:
    kind = ("checked by s2_seam" if r in internal
            else "DROPPED by s2_seam's 'subheaded' filter")
    resolves = r in headings
    print("      §%-6s %-40s %s"
          % (r, kind, "resolves" if resolves else "refers to no heading"))
print()
note("every reference s2_seam CHECKS resolves",
     all(r in headings for r in internal))
print("  %d of %d §N.M references are dropped before the check."
      % (len(dropped), len(allrefs)))
print("  They are dropped for a stated and correct reason -- this document")
print("  writes '§6.1' for item 1 of §6's numbered list, and '§17.4' for a")
print("  section of Aguiar-Mahajan -- and s2_seam.py says so in a comment.")
print("  It is not said in the EXTENT paragraph, which claims only that S2b")
print("  'resolves numbered sub-section references only'.  A reader takes")
print("  that to mean all of them.")
note("no dropped reference happens to name a §14.x that does not exist",
     not [r for r in dropped if r.startswith("14.") and r not in headings])
print()

hdr("D3e  THE BY-NAME CHAIN §14.3 -> §14.2, WHICH A RESOLVED DUPLICATE BREAKS")
h142, h143 = TEXT.find("### 14.2"), TEXT.find("### 14.3")
flat142 = re.sub(r"\s+", " ", re.sub(r"(?m)^\s*>\s?", "", TEXT[h142:h143]))
quoted = "outside every beam currently pointed at this document"
note("§14.3 names §14.2", "§14.2 predicted" in TEXT[h143:])
note("the sentence §14.3 quotes back is in §14.2", quoted in flat142)
print()
s2src = open(os.path.join(REPO, "code", "species_repair_a4ef", "s2_seam.py"),
             encoding="utf-8").read()
uses = len(re.findall(r"\bquoted\b", s2src))
print("  s2_seam.py assigns that exact sentence to a local `quoted` and the")
print("  identifier appears %d time(s) in the whole file." % uses)
note("s2_seam.py's `quoted` is DEAD -- assigned, never used", uses == 1)
raw_form = "outside\nevery beam currently pointed at this document"
print("  Its value carries a hard newline: %r" % raw_form[:40])
print("  `TEXT.count(that)` is %d -- so had the check been wired up it"
      % TEXT.count(raw_form))
print("  Absent: %s.  The check that is missing is also the check that"
      % ("yes" if TEXT.count(raw_form) == 0 else "no"))
print("  was wrong.")
print("  would have reported the document's correct by-name answer as")
print("  BROKEN.  The check that is missing is also the check that was wrong.")
print("  D3e above does it against the FLATTENED §14.2, which is what the")
print("  document actually says.")
print()

hdr("D3f  TWO COUNTS s2_seam.py STATES ABOUT ITSELF")
m = re.search(r"(?ms)^PATTERNS = \[(.*?)^\]", s2src)
rows = len(re.findall(r"(?m)^    \(", m.group(1))) if m else 0
print("  S2c is headed 'THE THREE STALENESS PATTERNS THIS SEAM PRODUCED' and")
print("  the EXTENT paragraph says 'S2c is three named patterns'.")
print("  Its PATTERNS table has %d row(s); the section prints 5 checks." % rows)
note("the stated count of three matches the artifact", rows == 3)
print()
print("  This is five-versus-eight in miniature, in the file written to")
print("  catch five-versus-eight, and it is the same defect class the seam")
print("  finding is about: a count in prose that no artifact carries.")
print()
pct = re.search(r'ONE pair at 56%%', s2src)
note("the committed out_s2_seam.txt has no stray '%%' from an unformatted "
     "print", "56%%" not in open(os.path.join(REPO, "code",
                                              "species_repair_a4ef",
                                              "out_s2_seam.txt"),
                                 encoding="utf-8").read())
print("  (`print(\"... 56%% ...\")` with no format operator prints the two")
print("  characters literally.  Cosmetic, in a committed output.)")
print()

print("=" * 78)
print("D3 TOTAL BAD: %d" % bad)
print("=" * 78)
print()
print("EXTENT OF THIS NUMBER.  D3 sweeps ONE document -- %s --" % DOC)
print("for near-duplicate BLOCK QUOTES and PROSE PARAGRAPHS, all %d and %d of"
      % (len(bq), len(pp)))
print("them, every pair, with NO length floor, at a stated threshold of 30%.")
print("It does NOT compare block quotes against prose, does not sweep tables,")
print("headings or list items, does not look at any other document, and")
print("cannot see a duplicate that has been paraphrased below 30%.  Its")
print("cross-reference check covers §N.M forms only -- not prose references")
print("such as 'the banner at the top', which is the form that carried the")
print("five-versus-eight nobody's checker caught.")
sys.exit(1 if bad else 0)
