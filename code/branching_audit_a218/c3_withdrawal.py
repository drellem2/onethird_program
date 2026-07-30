"""c3_withdrawal.py -- is the withdrawal complete, is D10 a conjecture, is the
retraction IN the document, and did the near-miss disclosure survive?

Everything here is a check on TEXT, so every check names the exact string it
looked for and where it looked.  No check is passed by a synonym.

Populations searched:
  * the delivered document, docs/OneThird-Bratteli-Path-Algebras-Where-This-Lives.md
  * every file in code/branching_locate_db09/ (source AND committed output),
    because this repo has twice found a correction that lived in the prose
    while the instrument still asserted the error (mg-73df X3 / mg-a4ef).
  * the pre-repair document at commit 03d7f91, for the survival test.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DOCPATH = "docs/OneThird-Bratteli-Path-Algebras-Where-This-Lives.md"
DOC = open(os.path.join(ROOT, DOCPATH)).read()
INSTR_DIR = os.path.join(ROOT, "code", "branching_locate_db09")

SELF, FIND = [], []
CHECKS = 0


def report(name, ok, detail=""):
    global CHECKS
    CHECKS += 1
    print("    %-4s %-62s %s" % ("[ok]" if ok else "[!!]", name,
                                 "pass" if ok else "FAIL"))
    if detail:
        print("         " + detail)
    if not ok:
        FIND.append(name + (" -- " + detail if detail else ""))
    return ok


def norm(s):
    return re.sub(r"\s+", " ", s)


NDOC = norm(DOC)

print("=" * 74)
print("c3  WITHDRAWAL COMPLETENESS, D10's STATUS, AND THE SURVIVAL OF THE")
print("    NEAR-MISS DISCLOSURE")
print("=" * 74)
print()

# ---------------------------------------------------------------------------
print("(1) IS THE WITHDRAWAL STATED AS A WITHDRAWAL?")
print()
report("the word WITHDRAWN appears in the section-0 banner",
       "WITHDRAWN" in DOC.split("## 0. THE HEADLINE")[0])
report("the separating example is called WITHDRAWN, not refined/clarified",
       "The separating example is WITHDRAWN" in NDOC)
report("the withdrawal is NOT dressed as a refinement",
       not re.search(r"(refined|clarified|nuanced) (the )?separating example",
                     NDOC, re.I))
report("D2 in the claim ledger is struck through and marked WITHDRAWN",
       "**WITHDRAWN (mg-e8b8, on mg-2060's finding).**" in DOC
       and "| **D2** | ~~" in DOC)
report("section 8 reports it as a withdrawal, 'not as a refinement, not as a "
       "clarification'",
       "not as a refinement, not as a clarification" in NDOC)
print()

# ---------------------------------------------------------------------------
print("(2) IS THE VERDICT ATTRIBUTED TO THE THEOREM?")
print()
report("section 0 says the verdict survives ON THE THEOREM and not on the builds",
       "The verdict of §0 survives, but on the THEOREM and not on the builds"
       in NDOC or "survives, but on the THEOREM and not on the builds" in NDOC)
report("the Wedderburn equivalence is stated as the basis",
       "A ≅ ⊕_λ End(V_λ) ⟺ A is semisimple" in NDOC
       or "semisimple, so for *every*" in NDOC)
report("D4's status says its basis is corrected and rests on the QUOTED THEOREMS",
       "It is a consequence of the QUOTED THEOREMS, not a synthesis of the builds"
       in NDOC)
report("section 0 says the 2x2 table is not the evidence for the verdict",
       "it is not the evidence for the verdict" in NDOC)
print()

# ---------------------------------------------------------------------------
print("(3) IS THE WITHDRAWN CLAIM STILL ASSERTED ANYWHERE -- PROSE OR INSTRUMENT?")
print()
WITHDRAWN_PHRASES = [
    "same multiplicity-free graph at each",
    "held fixed down that column",
    "held FIXED",
    "MEASURED (not cited)",
    "measured (not cited)",
]
# The marker list was WIDENED ONCE, after inspection, and the widening is
# recorded here rather than made silently.  The first run of this script flagged
# exactly one occurrence: the delivered document's
#     'The failing phrase was **`"MEASURED (not cited)"`**: the invariant was
#      *asserted*.'
# That occurrence IS inside the withdrawal -- it is the sentence that performs
# it -- but it says so with the words "failing phrase" and "asserted", neither
# of which was in the original marker list.  Both are added; nothing else is.
MARKERS = ["WITHDRAW", "withdraw", "CORRECTED", "corrected", "WHAT WAS CLAIMED",
           "used to say", "used to read", "no longer", "wrong", "USED TO SAY",
           "was wrong", "NO LONGER", "failing phrase", "was *asserted*",
           "was ASSERTED"]

files = [(DOCPATH, DOC)]
for fn in sorted(os.listdir(INSTR_DIR)):
    p = os.path.join(INSTR_DIR, fn)
    if os.path.isfile(p) and (fn.endswith(".py") or fn.endswith(".txt")
                              or fn.endswith(".md") or fn.endswith(".sh")):
        try:
            files.append(("code/branching_locate_db09/" + fn, open(p).read()))
        except UnicodeDecodeError:
            pass

occurrences = 0
unmarked = []
for name, text in files:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        for ph in WITHDRAWN_PHRASES:
            if ph in line:
                occurrences += 1
                window = "\n".join(lines[max(0, i - 12):i + 13])
                if not any(m in window for m in MARKERS):
                    unmarked.append((name, i + 1, ph, line.strip()[:90]))
print("    occurrences of a withdrawn phrase: %d, population: %d files "
      "(the delivered document plus every .py/.txt/.md/.sh in "
      "code/branching_locate_db09/), searched for %d phrases"
      % (occurrences, len(files), len(WITHDRAWN_PHRASES)))
print("    the phrases: %s" % "; ".join(repr(p) for p in WITHDRAWN_PHRASES))
print("    a marked occurrence is one with a withdrawal/correction marker within")
print("    12 lines either side; the markers are: %s" % ", ".join(sorted(set(
    m.lower() for m in MARKERS))))
report("every occurrence sits inside a withdrawal or correction",
       not unmarked,
       "" if not unmarked else "unmarked: " + "; ".join(
           "%s:%d %r" % (n, l, ph) for (n, l, ph, _) in unmarked))
print()

# ---------------------------------------------------------------------------
print("(4) DOES D10 READ AS A CONJECTURE?")
print()
d10_row = [l for l in DOC.splitlines() if l.startswith("| **D10**")]
report("the D10 ledger row exists", len(d10_row) == 1)
if d10_row:
    report("the D10 ledger row's status says CONJECTURE and NOT A RESULT",
           "A CONJECTURE" in d10_row[0] and "NOT A RESULT" in d10_row[0])
report("section 2 row 2's verdict says CONJECTURED, not 'contains both'",
       "CONJECTURED TO CONTAIN BOTH" in DOC)
report("the section-0 deliverable block is headed as a conjecture",
       "THIS SECTION IS A CONJECTURE, AND IT WAS DELIVERED AS A RESULT" in NDOC)
report("the answer to the umbrella question is stated as 'open', not 'yes'",
       'is **"open"**, not **"yes, quasi-hereditary"**' in NDOC
       or 'is **"open"**' in NDOC)
report("no sentence still asserts kF(P) IS quasi-hereditary without a hedge",
       not re.search(r"kF\(P\)` is quasi-hereditary(?![^.]*(conjectur|unverified|"
                     r"NOT A RESULT|CONJECTURE))", NDOC)
       or "that `kF(P)` **is** quasi-hereditary (D10 is a conjecture)" in NDOC)
# what-would-establish-it, concretely
steps = re.findall(r"^\d\.\s+\*\*", DOC.split("**What would establish it**")[1]
                   .split("**The retraction of record.**")[0], re.M)
report("'what would establish it' is stated as concrete numbered steps (>= 3)",
       len(steps) >= 3, "steps found: %d" % len(steps))
report("step 1 is READ PUTCHA", "1. **Read Putcha, *J. Algebra* 205 (1998) 53–76**"
       in DOC)
print()

# ---------------------------------------------------------------------------
print("(5) IS THE RETRACTION RECORDED IN THE DOCUMENT ITSELF?")
print()
report("the retracting commit hash f4eaea6 is named in the document",
       "f4eaea6" in DOC)
report("the delivery time 19:50 is in the document", "19:50" in DOC)
report("the retraction time 20:45 is in the document", "20:45" in DOC)
report("the document says a retraction living only in mail/roadmap is not one",
       "a retraction that lives only in a roadmap entry and in mail is not a "
       "retraction" in NDOC or "a retraction that lives only in mail and in a "
       "roadmap is not a retraction" in NDOC)
n_sites = sum(1 for s in ["## 0. THE HEADLINE", "### D10 IN FULL"]
              if "20:45" in DOC.split(s)[1].split("\n## ")[0])
report("the retraction is recorded at BOTH the section-0 banner and D10 in full",
       "20:45" in DOC.split("THIS SECTION IS A CONJECTURE")[1].split("## 1.")[0]
       and "20:45" in DOC.split("### D10 IN FULL")[1])
print()

# ---------------------------------------------------------------------------
print("(6) ARE THE OTHER UNVERIFIED ITEMS MARKED, NOT SILENTLY RETAINED?")
print()
items = {
    "the n = 6 95.7% figure is marked as still arithmetic / not re-derived":
        ("95.7" in DOC and ("remains arithmetic" in DOC or "still arithmetic" in DOC)
         and ("re-derived by nobody" in DOC or "not re-derived" in DOC)),
    "'a band is a regular monoid' is marked NOT CHECKED and owned":
        ("a band is a **von Neumann regular** monoid | **NOT CHECKED. One line, "
         "and it is mine.**" in NDOC)
        or ("NOT CHECKED. One line, and it is mine." in NDOC),
    "CMPX (A2)(ii), (A4), (A5), (A6) are marked untested":
        (re.search(r"\(A2\)\(ii\).{0,40}\(A4\).{0,20}\(A5\).{0,20}\(A6\)", NDOC)
         is not None
         and ("untested" in NDOC or "are all untested" in NDOC)),
    "the Putcha characteristic hypothesis is marked NOT VERIFIED":
        "NOT VERIFIED against the primary source" in NDOC,
    "Putcha is marked NOT read": "NOT read" in DOC and "Putcha" in DOC,
    # quote characters in this document are straight, not curly; matched on the
    # ASCII form after the first run showed the curly form matches nothing
    "T1a's 'iff' is named as open and NOT repaired":
        re.search(r"T1a's \*+\"iff\"", NDOC) is not None
        and "Deliberately NOT repaired" in NDOC,
    "section 1's unconditional VO Prop 1.4 reading is named as open":
        "unconditional reading of VO Prop. 1.4" in NDOC,
    "D5's 'each listed with its size' is named as open":
        "each listed with its size" in DOC and "X5" in DOC,
    "section 7's count of one-line derivations is named as open":
        "count of four one-line derivations" in NDOC or "count of one-line "
        "derivations" in NDOC,
}
for name, ok in items.items():
    report(name, ok)
print()

# ---------------------------------------------------------------------------
print("(7) DID THE NEAR-MISS DISCLOSURE SURVIVE THE REPAIR?")
print("    A DELETION TEST: every sentence of the PRE-REPAIR section-4 item 3")
print("    must still be present in the repaired document, verbatim.")
print()
old = subprocess.run(["git", "show", "03d7f91:" + DOCPATH], cwd=ROOT,
                     capture_output=True, text=True)
if old.returncode != 0:
    SELF.append("could not read the pre-repair document at 03d7f91")
    print("    SELF-ERROR: git show 03d7f91 failed")
else:
    oldtxt = old.stdout
    m = re.search(r"\n3\. \*\*Attack T1's identification of the branching graph"
                  r".*?(?=\n4\. \*\*)", oldtxt, re.S)
    if not m:
        SELF.append("could not locate item 3 in the pre-repair document")
    else:
        item3_old = m.group(0)
        sentences = [norm(s).strip() for s in re.split(r"(?<=\.)\s+", item3_old)
                     if len(norm(s).strip()) > 25]
        missing = [s for s in sentences if s not in NDOC]
        print("    sentences in the PRE-REPAIR item 3: %d, population: every "
              "sentence of item 3 at 03d7f91 longer than 25 characters"
              % len(sentences))
        report("every pre-repair sentence of item 3 survives verbatim",
               not missing,
               "" if not missing else "missing %d: %s" % (len(missing), missing[:2]))
        report("the phrase 'its dimension shadow' survives",
               "dimension shadow" in DOC)
        report("the question 'whether that shadow is enough' survives",
               "check whether that shadow is enough for what §0 claims" in NDOC)
        report("item 3 now carries its OUTCOME appended in place, not a rewrite",
               "OUTCOME (mg-2060): THE SHADOW IS NOT ENOUGH" in DOC)
        report("the document says deleting the disclosure would be a loss",
               "would remove the only evidence the near-miss discipline works"
               in NDOC or "would delete the only evidence that the near-miss "
               "discipline works" in NDOC)
        # the whole list, not just item 3
        allitems = re.findall(r"\n(\d)\. \*\*Attack", oldtxt)
        newitems = re.findall(r"\n(\d)\. \*\*Attack", DOC)
        report("all %d pre-filed attack items survive (none deleted)"
               % len(allitems), set(allitems) == set(newitems),
               "old %s new %s" % (allitems, newitems))
print()

print("-" * 74)
print("SELF-ERRORS: %d, population: the git reads and section locations this "
      "script needs" % len(SELF))
for s in SELF:
    print("   SELF-ERROR: " + s)
print("FINDINGS: %d, population: the %d named text checks above" % (len(FIND), CHECKS))
for f in FIND:
    print("   FINDING: " + f)
print("TOTAL BAD: %d" % (len(SELF) + len(FIND)))
sys.exit(1 if (SELF or FIND) else 0)
