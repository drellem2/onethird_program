"""D4 -- OVER-CORRECTION.  THE 15 SURVIVALS, CHECKED AGAIN, AND THE DIFF.

The brief: *"mg-73df was emphatic that nothing retreated -- 15 of 15
survivals, headline still a theorem, control (ii) STRENGTHENED.  A repair
acting on a MAJOR is exactly when a document gets hedged back.  Check all 15
survivals again and flag any weakening as a defect in its own right."*

mg-73df checked them BEFORE mg-a4ef ran.  A repair that hedges would hedge
after that check.  So:

  D4a  the 15, re-checked at HEAD with regexes written here.
  D4b  the 5 that must survive ONLY inside a strike, re-checked.
  D4c  THE DIFF ITSELF.  Every line mg-a4ef removed from the document, and
       every hedging word it added, counted -- because a survival check tests
       what a list remembers to name, and a diff tests everything else.
  D4d  the four trees' verdict lines, before and after.

    python3 code/species_audit_7dd3/d4_survivals.py
"""

import os
import re
import subprocess
import sys

from kern7dd3 import hdr
from statements7dd3 import DOC

bad = 0
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
TEXT = open(os.path.join(REPO, "docs", DOC), encoding="utf-8").read()
FLAT = re.sub(r"\s+", " ", re.sub(r"(?m)^\s*>\s?", "", TEXT))
BEFORE = "ebecd89"


def note(label, cond):
    global bad
    bad += (not cond)
    print("  %-68s %s" % (label[:68], "ok" if cond else "*** FAILS ***"))
    return cond


# The fifteen, restated here as SENTENCES rather than as c5_doc.py's regexes,
# so a survival that has been reworded into something weaker fails.  Where
# c5_doc.py accepts `Solomon` anywhere in the document, this asks for the
# clause that makes it a limitation.
SURVIVALS = [
    ("1  control (ii)'s conclusion is explicitly NOT withdrawn",
     r"AND THAT CONCLUSION SURVIVES THE CORRECTION TO ITS NUMBERS"),
    ("2  the band product is still invisible to the Hopf structure",
     r"band product is invisible to the Hopf structure"),
    ("3  the headline is a THEOREM, not a measurement",
     r"AND IT IS A THEOREM, NOT ONLY A MEASUREMENT"),
    ("4  §2.3 has no `n` dependence", r"no `n` dependence"),
    ("5  the poset half is 87 of 87 classes", r"87 of 87 classes"),
    ("6  with NO size cap", r"87 of 87 classes to `n ≤ 5` with no size cap"),
    ("7  and 179 of 179 out of sample", r"179 of 179"),
    ("8  the `S_n` half is NOT verified here",
     r"THE `S_n` HALF OF THE CORRESPONDENCE IS NOT VERIFIED HERE"),
    ("9  Solomon named as cited and unread",
     r"CITED to Solomon and to Garsia–Reutenauer/Atkinson, and NOT"),
    ("10 Garsia-Reutenauer / Atkinson named as unread",
     r"Garsia–Reutenauer\s*/\s*Atkinson.{0,80}[Nn]either.{0,40}(read|fetched)"),
    ("11 located is distinguished from verified, in both directions",
     r"Being located is a real result\. Presenting it as verified is not"),
    ("12 the successor literature search is cancelled",
     r"DO NOT FILE THE SUCCESSOR LITERATURE SEARCH"),
    ("13 and its errand withdrawn where it was written",
     r"THIS ITEM IS CLOSED AND ITS ERRAND IS WITHDRAWN"),
    ("14 T3d is TWO statements, each computed twice",
     r"the four columns are TWO STATEMENTS, EACH COMPUTED TWICE"),
    ("15 control (ii)'s 1 442 are the disjoint-ground-set pairs",
     r"1 442 of 11 301|1 442 disjoint-ground-set"),
]

STRUCK_ONLY = [
    ("§2.3 re-hedged as 'measured, not proved'", r"measured, not proved"),
    ("§2.3 re-described as not located in that generality",
     r"not located.{0,60}in that generality"),
    ("'three of the four columns are the control'",
     r"[Tt]hree of the four columns are the control"),
    ("'fires hard' as the reading of control (ii)", r"fires hard"),
    ("the smallest witness given as \\{a<c, b<d\\}", r"Smallest witness with"),
]

STRIKES = [(m.start(), m.end()) for m in re.finditer(r"~~.+?~~", TEXT, re.S)]
REPAIR_ID = re.compile(r"mg-6f61|mg-f8fa|mg-a61f|mg-73df|mg-a4ef", re.I)
LINES = TEXT.splitlines()


def struck(pos):
    if any(a <= pos < b for a, b in STRIKES):
        return True
    ln = TEXT.count("\n", 0, pos)
    lo = hi = ln
    while lo > 0 and LINES[lo - 1].strip():
        lo -= 1
    while hi + 1 < len(LINES) and LINES[hi + 1].strip():
        hi += 1
    return bool(REPAIR_ID.search("\n".join(LINES[lo:hi + 1])))


hdr("D4a  THE FIFTEEN SURVIVALS, RE-CHECKED AT HEAD")
for label, pat in SURVIVALS:
    note("survives  " + label, bool(re.search(pat, FLAT)))
print()

hdr("D4b  THE FIVE THAT MUST SURVIVE ONLY INSIDE A STRIKE")
for label, pat in STRUCK_ONLY:
    hits = [m.start() for m in re.finditer(pat, TEXT)]
    loose = [h for h in hits if not struck(h)]
    note("struck    %-58s (%d occurrence(s))" % (label, len(hits)),
         bool(hits) and not loose)
print()

hdr("D4c  THE DIFF -- WHAT mg-a4ef REMOVED, AND WHAT IT HEDGED")
d = subprocess.run(["git", "diff", "%s..HEAD" % BEFORE, "--", "docs/" + DOC],
                   cwd=REPO, capture_output=True, text=True)
if d.returncode != 0:
    print("  git unavailable -- NOT RUN, and this line is the record")
    bad += 1
else:
    removed = [l[1:] for l in d.stdout.splitlines()
               if l.startswith("-") and not l.startswith("---")]
    added = [l[1:] for l in d.stdout.splitlines()
             if l.startswith("+") and not l.startswith("+++")]
    print("  %d line(s) removed, %d added." % (len(removed), len(added)))
    print()
    print("  EVERY REMOVED LINE, so nothing is dropped unseen:")
    for l in removed:
        print("      - %s" % l.strip()[:98])
    print()
    HEDGES = [r"\bmay\b", r"\bmight\b", r"\bperhaps\b", r"\bpossibly\b",
              r"\bappears? to\b", r"\bseems? to\b", r"\bwe think\b",
              r"\bnot (?:fully|entirely) (?:verified|established)\b",
              r"\bonly a measurement\b", r"\bunproven\b", r"\bconjectur"]
    hedged = [(h, l.strip()) for l in added for h in HEDGES
              if re.search(h, l, re.I)]
    print("  HEDGING WORDS IN THE ADDED LINES: %d" % len(hedged))
    for h, l in hedged:
        print("      %-24s %s" % (h, l[:70]))
    note("no hedging word is added to the document", not hedged)
    # "Nothing the deleted copy said is lost -- it said less."  That is
    # mg-a4ef's claim about the box it deleted, and it is testable: for every
    # removed line, the longest run of its tokens that still occurs somewhere
    # in the document.  A line whose content survives is a re-wrap or a
    # re-statement; a line whose content does not is a deletion, and every
    # deletion has to be one of mg-73df's findings.
    #
    # A first version instead pattern-matched the removed lines against a list
    # of phrases, and reported five re-wrapped lines as unaccounted for.  A
    # list of phrases is the failure mode this whole audit is about; it is
    # replaced here by a measurement.  Kept in OUTCOMES.md.
    from kern7dd3 import tokens as _tok
    head_tokens = " " + " ".join(t for t, _ in _tok(TEXT)) + " "
    INTENDED = [
        ("the five items in the banner at the top", "Y3 -- the miscount"),
        ("an eighth defect, if there is one", "Y3 -- the stale prediction"),
        ("second, shelved filing", "Y4 -- 'shelved'"),
        ("mg-a61f's audit was", "Y3 -- the one-source account"),
        ("checker for the instrument", "Y1 -- the coverage overclaim"),
        ("is **Solomon's descent algebra**", "Y2 -- the plain isomorphism"),
    ]
    lost = []
    for l in removed:
        if not l.strip():
            continue
        # the leading `>` is a blockquote marker, not content: leaving it in
        # anchored every run to it and reported a surviving phrase as lost
        w = [t for t, _ in _tok(re.sub(r"^\s*>+\s?", "", l))]
        best = 0
        for i in range(len(w)):
            for j in range(len(w), i + best, -1):
                if " " + " ".join(w[i:j]) + " " in head_tokens:
                    best = j - i
                    break
        # a 4-token line can never show a 6-token run: the bar is the whole
        # line when the line is shorter than the bar.  (First version used a
        # flat 6 and reported "> cannot be wrong." as content lost, while the
        # phrase survives verbatim in 14.2.  OUTCOMES.md.)
        if best < min(6, len(w)):
            why = next((r for k, r in INTENDED if k in l), None)
            lost.append((l.strip(), best, why))
    print()
    print("  IS ANYTHING THE DELETED COPY SAID ACTUALLY LOST?  Longest run of")
    print("  each removed line still present in the document at HEAD:")
    print("      %d removed line(s); %d have a run of 6+ tokens still present"
          % (len([l for l in removed if l.strip()]),
             len([l for l in removed if l.strip()]) - len(lost)))
    for l, best, why in lost:
        print("      run %-2d  %s" % (best, l[:66]))
        print("              %s" % (("DELIBERATE, %s" % why) if why
                                    else "*** CONTENT LOST, ON NO FINDING ***"))
    note("every line whose content did not survive is a named finding",
         all(w for _, _, w in lost))
    print("  So mg-a4ef's 'nothing the deleted copy said is lost -- it said")
    print("  less' is MEASURED, not taken.")

print()

hdr("D4d  EVERY TREE'S VERDICT LINE, BEFORE AND AFTER")
VERDICTS = [
    ("code/species_7d75/out_t6_fock_and_record.txt", r"T6 TOTAL BAD: \d+"),
    ("code/species_7d75/out_t5_hopf_monoid.txt", r"T5 TOTAL BAD: \d+"),
    ("code/species_7d75/out_t3_bidigare.txt", r"T3 TOTAL BAD: \d+"),
    ("code/species_repair_6f61/out_check_doc.txt", r"CHECK_DOC: \w+"),
    ("code/species_repair_6f61/out_r2_columns.txt", r"R2 TOTAL BAD: \d+"),
    ("code/species_remainder_f8fa/out_w3_scope.txt", r"W3 SCOPE: \w+"),
]
for path, pat in VERDICTS:
    now = open(os.path.join(REPO, path), encoding="utf-8").read()
    old = subprocess.run(["git", "show", "%s:%s" % (BEFORE, path)],
                         cwd=REPO, capture_output=True, text=True)
    a = re.search(pat, now)
    b = re.search(pat, old.stdout) if old.returncode == 0 else None
    same = bool(a) and bool(b) and a.group(0) == b.group(0)
    print("      %-46s %-18s %s"
          % (path.split("/")[-1], a.group(0) if a else "-",
             "unchanged" if same else "*** MOVED: was %s ***"
             % (b.group(0) if b else "?")))
    bad += (not same)
print()
print("  Nothing retreated numerically either: a repair that hedged would")
print("  most cheaply do it by letting a count move.")
print()

print("=" * 78)
print("D4 TOTAL BAD: %d" % bad)
print("=" * 78)
print()
print("EXTENT OF THIS NUMBER.  D4 checks the 15 survivals mg-73df enumerated")
print("and the 5 it required to stay struck -- ITS list, not a new one -- plus")
print("every line the mg-a4ef diff touched in the document and 6 verdict")
print("lines.  It does NOT re-verify the mathematics behind any survival, does")
print("not read the code trees for hedging, and cannot see a weakening that")
print("neither changes a listed sentence nor appears in the document diff.")
sys.exit(1 if bad else 0)
