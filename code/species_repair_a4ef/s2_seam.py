"""S2 -- THE SEAM, AND A CHECK THAT OUTLIVES THIS PARTICULAR SEAM.

mg-73df, Y3/Y4: §14's limitation box appeared TWICE, at 56 % similarity, in
two versions that did not agree.  One called mg-6f61's list "the FIVE items in
the banner at the top" where that banner says EIGHT; the other traced it to
two sources and carried the evidence.  §14.3, added by the SECOND worker,
answers §14.2 by name -- so the stale copy was load-bearing for a later
section, twelve lines above a paragraph reporting that the eighth defect had
been found while the stale copy still said "if there is one".

Neither worker's brief covered the seam.  Both passes were complete against
their own brief, and the defect is what fell between them.

THIS FILE IS THE CHECK NOBODY'S BRIEF ASKED FOR, KEPT.  It is deliberately
GENERAL -- it does not look for §14's box, it looks for any two passages that
say the same thing twice:

  S2a  every block quote against every other, and every prose paragraph
       against every other.  mg-73df swept the 17 block quotes; a paragraph
       sweep is added here because the pair it found need not have been in
       quotes, and a check written to catch the instance you already know
       about catches exactly that instance.
  S2b  every internal cross-reference RESOLVES: a §14.N referred to by name
       exists, and a back-reference to a count agrees with the count.
  S2c  the three specific staleness patterns this seam produced, so a
       regression is caught by name as well as by shape.

    python3 code/species_repair_a4ef/s2_seam.py
"""

import difflib
import os
import re
import sys

from kerna4ef import hdr

bad = 0
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
DOC = os.path.join(REPO, "docs",
                   "OneThird-Species-Hopf-Monoids-Where-This-Lives.md")
TEXT = open(DOC, encoding="utf-8").read()
LINES = TEXT.splitlines()

# mg-73df's pair measured 56 %.  The threshold is set BELOW that, at 45 %, so
# this file would have caught that pair with room to spare and catches a
# weaker duplicate than the one that prompted it.
THRESHOLD = 0.45
MIN_CHARS = 300


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


def sweep(name, items):
    global bad
    big = [(a, b, t) for (a, b, t) in items if len(norm(t)) > MIN_CHARS]
    print("  %-22s %3d passage(s), %3d longer than %d characters"
          % (name, len(items), len(big), MIN_CHARS))
    worst = (0.0, None, None)
    dups = []
    for i in range(len(big)):
        for j in range(i + 1, len(big)):
            r = difflib.SequenceMatcher(None, norm(big[i][2]),
                                        norm(big[j][2])).ratio()
            if r > worst[0]:
                worst = (r, big[i], big[j])
            if r > THRESHOLD:
                dups.append((r, big[i], big[j]))
    if worst[1] is not None:
        print("  %-22s worst pair %.0f%%  (lines %d-%d vs %d-%d), "
              "threshold %.0f%%"
              % ("", 100 * worst[0], worst[1][0], worst[1][1],
                 worst[2][0], worst[2][1], 100 * THRESHOLD))
    for r, x, y in sorted(dups, key=lambda d: -d[0]):
        bad += 1
        print("  *** NEAR-DUPLICATE  %.0f%% similar: lines %d-%d and %d-%d"
              % (100 * r, x[0], x[1], y[0], y[1]))
        sm = difflib.SequenceMatcher(None, norm(x[2]).split(),
                                     norm(y[2]).split())
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                continue
            a = " ".join(norm(x[2]).split()[i1:i2])
            b = " ".join(norm(y[2]).split()[j1:j2])
            if a.strip():
                print("        first  only: %s" % a[:150])
            if b.strip():
                print("        second only: %s" % b[:150])
    print()


hdr("S2a  THE SAME THING SAID TWICE -- every passage against every other")
print("  mg-73df found ONE pair at 56%%, in the block quotes.  The threshold")
print("  here is %.0f%%, below what it found, and the sweep is run over prose"
      % (100 * THRESHOLD))
print("  paragraphs as well -- a check written to catch the instance you")
print("  already know about catches exactly that instance.")
print()
sweep("block quotes", blocks_of(lambda ln: ln.startswith(">")))
sweep("prose paragraphs",
      blocks_of(lambda ln: ln.strip() and not ln.startswith(">")
                and not ln.startswith("#") and not ln.startswith("|")))


hdr("S2b  CROSS-REFERENCES RESOLVE, AND BACK-REFERENCED COUNTS AGREE")

headings = set(re.findall(r"(?m)^#{2,4}\s*(\d+(?:\.\d+)?)[.\s]", TEXT))
subheaded = {h.split(".")[0] for h in headings if "." in h}
# Only sections that ACTUALLY USE sub-headings are checked.  This document
# writes "§6.1" for "§6 item 1" of a numbered list, and "§17.4" / "§4.1" for
# sections of Aguiar-Mahajan and of Brown.  A first version of this check
# flagged all eleven of those as dangling -- a checker firing on a convention
# instead of a defect, which is the failure this whole arc is about, so the
# restriction is stated rather than tuned away silently.

# ... and a reference is internal only if nothing immediately before it names
# ANOTHER document.  "mg-af28 §2.6" is a reference to a different ticket's
# document and this one is not required to have a §2.6.
EXTERNAL = re.compile(r"(?:mg-[0-9a-f]{4}(?:'s)?|AM|Aguiar[^\s]*|Brown|"
                      r"Marshall[^\s]*|Saliola|Bergeron[^\s]*|Joyal)\s*$")
refs = sorted({m.group(1) for m in re.finditer(r"§(\d+\.\d+)", TEXT)
               if m.group(1).split(".")[0] in subheaded
               and not EXTERNAL.search(TEXT[max(0, m.start() - 40):m.start()])})
print("  sections that use sub-headings: %s" % ", ".join(sorted(subheaded)))
print("  sub-sections referred to      : %s" % ", ".join(refs))
for r in refs:
    ok = r in headings
    bad += (not ok)
    print("      §%-6s %s" % (r, "resolves" if ok
                              else "*** REFERS TO NOTHING ***"))
print()

WORDS = {"five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
banner = re.search(r"(Eight|Seven|Six|Five|Nine|Ten) things changed", TEXT)
print("  the banner announces          : '%s things changed'"
      % (banner.group(1) if banner else "-"))
if not banner:
    bad += 1
    print("      *** the banner no longer announces its own item count ***")
backrefs = re.findall(r"the (five|six|seven|eight|nine|ten) items in the "
                      r"banner", TEXT, re.I)
if not backrefs:
    print("  back-references to that count : none")
for w in backrefs:
    ok = banner is not None and WORDS[w.lower()] == WORDS[banner.group(1).lower()]
    bad += (not ok)
    print("      back-reference says '%s'  %s"
          % (w, "agrees" if ok else "*** DISAGREES WITH THE BANNER ***"))
print()


hdr("S2c  THE THREE STALENESS PATTERNS THIS SEAM PRODUCED")

# Each is (label, must-be-absent regex, must-be-present regex or None).
PATTERNS = [
    ("a filing described as shelved AND as executed",
     r"shelved\s+filing", r"14\.3 The eighth defect was found"),
    ("§14.2 answered by name by §14.3, and present exactly once",
     None, r"THE SAME LIMITATION APPLIES TO §14 ITSELF"),
]
for label, absent, present in PATTERNS:
    okA = absent is None or not re.search(absent, TEXT, re.I)
    okP = present is None or bool(re.search(present, TEXT))
    ok = okA and okP
    bad += (not ok)
    print("  %-62s %s" % (label[:62], "ok" if ok else "*** STALE ***"))

# The conditional prediction "an eighth defect, IF there is one" is NOT stale
# in itself -- it is the prediction §14.3 answers by name, and §14.2 is
# entitled to make it.  It was stale in the DELETED copy because that copy sat
# outside the §14.2 / §14.3 exchange and nothing resolved it.  So the rule is
# not "the phrase must be absent" but "every occurrence must lie in the
# passage a later section resolves".
#
# mg-73df's own c5_doc.py used the blunter rule and would still report NO
# after the fix it recommended, because §14.2's legitimate copy matches it.
# Recorded here rather than adopted.
h142 = TEXT.find("### 14.2")
h143 = TEXT.find("### 14.3")
cond = [m.start() for m in
        re.finditer(r"an eighth defect, if (?:there is one|one exists)",
                    TEXT, re.I)]
inside = [p for p in cond if h142 < p < h143]
ok = (len(cond) == len(inside) and h142 != -1 and h143 != -1)
bad += (not ok)
print("  %-62s %s"
      % ("every 'an eighth defect, IF ...' is inside §14.2 (%d of %d)"
         % (len(inside), len(cond)), "ok" if ok else "*** STALE ***"))

# §14.3 answers §14.2 by name -- so §14.2 must exist, once, and must contain
# the sentence §14.3 quotes back at it.
quoted = "outside\nevery beam currently pointed at this document"
n142 = TEXT.count("THE SAME LIMITATION APPLIES TO §14 ITSELF")
ok = (n142 == 1)
bad += (not ok)
print("  %-62s %s" % ("the §14 limitation box occurs exactly ONCE (found %d)"
                      % n142, "ok" if ok else "*** NOT RESOLVED ***"))
ok = "§14.2 predicted" in TEXT and "### 14.2" in TEXT
bad += (not ok)
print("  %-62s %s" % ("§14.3's 'as §14.2 predicted' still has a §14.2 to name",
                      "ok" if ok else "*** DANGLING ***"))
print()

print("=" * 78)
print("S2 TOTAL BAD: %d" % bad)
print("=" * 78)
print()
print("EXTENT.  S2a is a similarity sweep over ONE document and cannot see a")
print("duplicate spread across two documents, or one paraphrased below %.0f%%."
      % (100 * THRESHOLD))
print("S2b resolves numbered sub-section references only, not prose")
print("references such as 'the banner at the top'.  S2c is three named")
print("patterns and is a regression guard, not a search.")
sys.exit(1 if bad else 0)
