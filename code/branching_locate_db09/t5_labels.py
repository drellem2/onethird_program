"""T5 --- EVERY DISPOSITION LABEL IN THE DELIVERED DOCUMENT, CHECKED.

mg-13b2, on mg-a218's second finding.

A disposition label is a marker that tells a reader what happened to a claim:
WITHDRAWN, CORRECTED, SUPERSEDED, "Updated", "Deliberately NOT repaired",
CLOSED, OPEN.  The convention was adopted on the day this document was written
and it is already load-bearing, because **the label is the artifact a reader
consults precisely so as not to read the diff**.  mg-e8b8 booked mg-2060's X2
under "Deliberately NOT repaired, and each is open" in the same commit that
silently repaired two of X2's three sites: a reader trusting the label believed
all three were open, a reader trusting the diff believed the finding was
addressed, and neither reading was right.

So the labels are measured here rather than read.  Every check is either

  * a statement about the CURRENT TREE (a phrase is present, is absent, or
    occurs only inside a quotation), or
  * a statement about a NAMED HISTORICAL COMMIT (its diff deleted or added a
    line containing a phrase; a file is byte-identical to its state there).

Both kinds are stable under re-running: nothing here reads "the diff of the
commit I am part of", which is the trap mg-8e30 paid for.  A label that stops
being true --- because a later commit reopens a site, or closes one without
saying so --- turns this script red.

NO NETWORK.  Requires `git` and a checkout; refuses to guess if either is
missing.
"""

import hashlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

DOC = "docs/OneThird-Bratteli-Path-Algebras-Where-This-Lives.md"
T1 = "code/branching_locate_db09/t1_tl.py"
O1 = "code/branching_locate_db09/out_t1_tl.txt"
RDM = "code/branching_locate_db09/README.md"
T2 = "code/branching_locate_db09/t2_gz.py"
T3 = "code/branching_locate_db09/t3_ours.py"
T4 = "code/branching_locate_db09/t4_quotes.py"
O2 = "code/branching_locate_db09/out_t2_gz.txt"
O3 = "code/branching_locate_db09/out_t3_ours.txt"
O4 = "code/branching_locate_db09/out_t4_quotes.txt"

# The two commits every label in this document points at, plus the state the
# repair started from.  Named, not inferred.
DELIVERED = "03d7f91"   # mg-db09, the document as delivered
REPAIR = "2e66d03"      # mg-e8b8, the repair mg-a218 audited
RETRACT = "f4eaea6"     # the roadmap retraction of the D10 headline

BAD = 0
CHECKS = 0
FILES = set()
COMMITS = set()


def git(*args):
    p = subprocess.run(["git"] + list(args), cwd=ROOT,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise RuntimeError("git %s failed: %s"
                           % (" ".join(args), p.stderr.decode()[:200]))
    return p.stdout.decode("utf-8", "replace")


def read(path):
    FILES.add(path)
    with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        return fh.read()


_diffs = {}


def diff_lines(commit, path, sign):
    COMMITS.add(commit)
    key = (commit, path)
    if key not in _diffs:
        txt = git("show", "--format=", commit, "--", path)
        _diffs[key] = txt.splitlines()
    out = []
    for line in _diffs[key]:
        if line.startswith(sign) and not line.startswith(sign * 3):
            out.append(line[1:])
    return out


def blob(commit, path):
    COMMITS.add(commit)
    return git("show", "%s:%s" % (commit, path))


# ---- the check vocabulary ---------------------------------------------------

def present(path, needle):
    n = read(path).count(needle)
    return n > 0, "%d occurrence(s) in %s" % (n, path)


def absent(path, needle):
    n = read(path).count(needle)
    return n == 0, "%d occurrence(s) in %s" % (n, path)


def quoted_only(path, needle, markers):
    """The phrase survives in the file ONLY inside blocks that carry a
    disposition marker --- i.e. it is quoted as withdrawn, never asserted.

    WIDENED ONCE, and the reason is recorded here rather than in a commit
    message (mg-13b2).  The window was the block containing the phrase.  T1d
    prints its withdrawn paragraph as an indented quotation with the marker
    'WHAT THIS BLOCK USED TO SAY' in the paragraph ABOVE it, separated by a
    blank line, so a block-only window scored a correctly-marked quotation as
    an unmarked assertion.  The window is now the block and its predecessor.
    This is a real loosening --- a marked block followed by an unmarked
    assertion of the same phrase would now pass --- and it is the reason the
    seam sweep in mg-a218's c4 exists and this script does not replace it.
    """
    txt = read(path)
    blocks = txt.split("\n\n")
    hits = [i for (i, b) in enumerate(blocks) if needle in b]
    if not hits:
        return False, "the phrase is not in %s at all, so nothing quotes it" % path
    live = [i for i in hits
            if not any(m in blocks[i] for m in markers)
            and not (i and any(m in blocks[i - 1] for m in markers))]
    return (not live), ("%d block(s) carry it, %d of them unmarked (window: "
                        "the block and the one before it)"
                        % (len(hits), len(live)))


def removed_in(commit, path, needle):
    hits = [l for l in diff_lines(commit, path, "-") if needle in l]
    return len(hits) > 0, "%d deleted line(s) in %s at %s" % (len(hits), path, commit)


def added_in(commit, path, needle):
    hits = [l for l in diff_lines(commit, path, "+") if needle in l]
    return len(hits) > 0, "%d added line(s) in %s at %s" % (len(hits), path, commit)


def untouched_in(commit, path):
    COMMITS.add(commit)
    names = git("show", "--format=", "--name-only", commit).split()
    return path not in names, "%s in the %d paths %s touched" % (
        "NOT" if path not in names else "IS", len(names), commit)


def unchanged_since(commit, path):
    a = hashlib.sha256(blob(commit, path).encode()).hexdigest()
    b = hashlib.sha256(read(path).encode()).hexdigest()
    return a == b, "sha256 %s vs %s at %s" % (b[:12], a[:12], commit)


def doc_matches_instrument():
    """Section 0's vertex column, read off the DOCUMENT and off the
    INSTRUMENT'S OWN OUTPUT and compared.  The document does not restate a
    figure it was given; the gate reads it at the site (mg-a318's rule)."""
    import re
    doc_rows = {}
    for m in re.finditer(r"^\|\s*(\d)\s*\|\s*132\s*\|.*?\|\s*`((?:\[[\d,]+\]\s*)+)`",
                         read(DOC), re.M):
        doc_rows[int(m.group(1))] = " ".join(m.group(2).split())
    out_rows = {}
    for m in re.finditer(r"^\s*beta = (\d) :\s+((?:\[[\d,]+\]\s*)+)$",
                         read(O1), re.M):
        out_rows[int(m.group(1))] = " ".join(m.group(2).split())
    if len(doc_rows) != 4 or len(out_rows) != 4:
        return False, ("parsed %d document row(s) and %d instrument row(s); "
                       "4 and 4 expected" % (len(doc_rows), len(out_rows)))
    agree = [b for b in doc_rows if doc_rows[b] == out_rows.get(b)]
    return len(agree) == 4, "%d of 4 rows agree character for character" % len(agree)


def subject_contains(commit, needle):
    COMMITS.add(commit)
    s = git("log", "-1", "--format=%s", commit)
    return needle in s, "commit %s subject" % commit


# ---- the labels -------------------------------------------------------------
#
# (section, the label as the document writes it, what it therefore asserts,
#  [checks])

WD = ["WITHDRAWN", "CORRECTED", "Corrected", "used to", "What was claimed",
      "~~", "USED TO SAY", "no longer", "MARKED IN PLACE", "SUPERSEDED"]

LABELS = [
    ("banner 1", "The separating example is WITHDRAWN",
     "the withdrawn phrase is asserted nowhere, at source or in prose, and the "
     "commit named as the withdrawal is the one that deleted it", [
         ("the banner carries the word", present, (DOC, "The separating example is WITHDRAWN")),
         ("the withdrawn phrase survives only inside withdrawals", quoted_only,
          (DOC, "(not cited) to be the same multiplicity-free", WD)),
         ("and the repair is what deleted it", removed_in,
          (REPAIR, DOC, "(not cited) to be the same")),
         ("T1b's old heading is gone from source", absent,
          (T1, "T1b  the BRANCHING GRAPH, measured (not cited)")),
         ("the repair is what deleted that too", removed_in,
          (REPAIR, T1, "the BRANCHING GRAPH, measured (not cited)")),
         ("the committed output no longer asserts it", quoted_only,
          (O1, "the branching graph is the same multiplicity-free graph", WD)),
     ]),

    ("banner 2", "D10 --- the deliverable --- is a CONJECTURE, not a result",
     "the ledger agrees, the NOT-CLAIMED row agrees, and the retraction it "
     "cites is a real commit", [
         ("the banner says it", present, (DOC, "is a CONJECTURE, not a result")),
         ("the ledger row says it", present, (DOC, "**A CONJECTURE. NOT A RESULT")),
         ("the NOT CLAIMED row says it", present, (DOC, "(D10 is a conjecture)")),
         ("the retraction commit exists and says so", subject_contains,
          (RETRACT, "RETRACT the quasi-hereditary headline")),
     ]),

    ("banner 3", "Nothing else in the document is withdrawn",
     "exactly one ledger row carries WITHDRAWN, and it is D2", [
         ("D2 is withdrawn", present, (DOC, "| **D2** | ~~")),
         ("no other ledger row is", lambda: (
             len([l for l in read(DOC).splitlines()
                  if l.startswith("| **D") and "WITHDRAWN" in l]) == 1,
             "%d ledger row(s) carry WITHDRAWN"
             % len([l for l in read(DOC).splitlines()
                    if l.startswith("| **D") and "WITHDRAWN" in l]))),
     ]),

    ("0", "~~Both halves are settled here by BUILDING~~ WITHDRAWN (mg-e8b8)",
     "the struck sentence is struck in place and the repair deleted the "
     "unstruck one", [
         ("struck in place", present, (DOC, "~~Both halves are settled here by BUILDING")),
         ("the repair deleted the assertion", removed_in,
          (REPAIR, DOC, "Both halves are settled here by BUILDING the object each would")),
     ]),

    ("0", "1. ~~Multiplicity-free and NOT semisimple~~ WITHDRAWN (mg-e8b8)",
     "same, for the object-1 heading", [
         ("struck in place", present, (DOC, "~~Multiplicity-free and NOT semisimple")),
         ("the repair deleted the assertion", removed_in,
          (REPAIR, DOC, "**1. Multiplicity-free and NOT semisimple")),
     ]),

    ("0", "CORRECTED (mg-e8b8) --- the 2x2 cell placement",
     "TL_6(1) and TL_6(0) are in the bottom-right cell now and were not before", [
         ("the bottom-right cell holds them", present,
          (DOC, "| **not multiplicity-free** | **`⊕End` HOLDS**")),
         ("with the figures", present, (DOC, "`TL_6(1)`: 99 of 132. `TL_6(0)`: 42 of 132")),
         ("the repair moved them", added_in,
          (REPAIR, DOC, "`TL_6(1)`: 99 of 132. `TL_6(0)`: 42 of 132")),
     ]),

    ("0", "MARKED IN PLACE (mg-13b2) --- 'Path-pair count survives'",
     "this is X2's second site: mg-e8b8 corrected it and booked X2 as "
     "untouched, and the marker now says so", [
         ("the cell reads count", present, (DOC, "Path-pair *count* survives")),
         ("the repair is what changed it", added_in,
          (REPAIR, DOC, "Path-pair *count* survives")),
         ("from basis", removed_in, (REPAIR, DOC, "Path-pair *basis* survives")),
         ("and the marker is here", present, (DOC, "**MARKED IN PLACE (mg-13b2")),
     ]),

    ("0", "the vertex column reports the SET (mg-13b2, on mg-a218's X1)",
     "the column carries the canonical form, the instrument prints the same "
     "form, and no count column sits beside it", [
         ("the header says SET", present, (DOC, "vertex SET at `n = 1…6`")),
         ("the old count header is gone", absent, (DOC, "# irreducibles at `n = 1…6`")),
         ("beta = 1 and beta = 3 are visibly different", lambda: (
             read(DOC).count("`[1] [1,1] [1,1] [1,3,1] [1,4,1] [1,4,9,1]`") == 1
             and read(DOC).count("`[1] [1,1] [1,2] [1,3,2] [1,4,5] [1,5,9,5]`") == 2,
             "beta=1 row present once, the beta=3/2 rows twice")),
         ("the instrument prints the same canonical form", present,
          (O1, "beta = 1 :  [1] [1,1] [1,1] [1,3,1] [1,4,1] [1,4,9,1]")),
         # the gate reads the figure AT THE SITE rather than restating it: the
         # document's four rows must be the instrument's four rows, character
         # for character, so the column cannot drift from what was measured.
         ("and the document's four rows ARE the instrument's", doc_matches_instrument, ()),
         ("and reports the cells a count would hide", present,
          (O1, "cells where the COUNT agrees and the SET does not: 10 of 36")),
     ]),

    ("0", "Where the two percentages stand after the audit (mg-e8b8)",
     "90.4% is derived, 95.7% is still arithmetic, and no commit since the "
     "delivery re-derived it", [
         ("the n=6 figure is booked as arithmetic", present, (DOC, "remains arithmetic")),
         ("the n=5 figure is booked as derived", present, (DOC, "87 of 87")),
         ("and t3 has not moved since delivery", unchanged_since, (DELIVERED, T3)),
         ("nor has its output", unchanged_since, (DELIVERED, O3)),
     ]),

    ("1", "Corrected (mg-13b2) --- the path-algebra row of the clause table",
     "a FOURTH site of X2, named by no list: the row said the matrix units "
     "survive without semisimplicity", [
         ("the row now separates count from matrix units", present,
          (DOC, "the COUNT survives without semisimplicity and the MATRIX UNITS do not")),
         ("the old wording is gone", absent,
          (DOC, "| **this survives without semisimplicity**")),
         ("and it points at the refutation", present, (DOC, "`T1c2`")),
     ]),

    ("3", "CORRECTED (mg-e8b8) --- 'the branching graph is unchanged and "
          "multiplicity-free'",
     "the phrase is quoted as corrected and the repair deleted the assertion", [
         ("quoted only as corrected", quoted_only,
          (DOC, "branching graph is unchanged\nand multiplicity-free", WD)),
         ("the repair deleted it", removed_in,
          (REPAIR, DOC, "branching graph is unchanged and multiplicity-free")),
     ]),

    ("3", "Corrected (mg-e8b8) --- 'are all multiplicity-free' with no qualifier",
     "the qualifier is in and the unqualified line was deleted by the repair", [
         ("the qualifier is in", present, (DOC, "**at generic parameters, which is where they are also")),
         ("the repair deleted the unqualified line", removed_in,
          (REPAIR, DOC, "Non-multiplicity-freeness in this subject arises by **skipping")),
     ]),

    ("4 item 3", "CORRECTED (mg-13b2): this paragraph said 'not repaired by "
                 "mg-e8b8 ... Both are open'",
     "the false 'both are open' is gone and the two findings are booked "
     "separately", [
         ("the correction is recorded", present, (DOC, "**CORRECTED (mg-13b2): this paragraph said")),
         ("'Both are open' is gone", absent, (DOC, "Both are open.")),
         ("X2 is booked closed", present, (DOC, "is now **CLOSED at all FOUR of its sites**")),
         ("X3 is booked open", present, (DOC, "**X3 is\n   > still open**")),
         ("and the fourth X2 site is named", present,
          (DOC, "fourth site in §1's clause table, named by no list")),
     ]),

    ("5", "D2 --- WITHDRAWN (mg-e8b8, on mg-2060's finding)",
     "the claim is struck in the ledger and the repair deleted the standing "
     "version of the row", [
         ("struck", present, (DOC, "| **D2** | ~~there is a multiplicity-free tower")),
         ("the repair deleted the standing row", removed_in,
          (REPAIR, DOC, "| **D2** | there is a multiplicity-free tower")),
     ]),

    ("5", "D2 --- Updated (mg-13b2): the row substantiated the vertex set with "
          "counts",
     "the row now carries vertex sets", [
         ("the row carries sets", present, (DOC, "`[1,4,9,1]` against `[1,5,9,5]` at `n = 6`")),
         ("the count form is gone from it", lambda: (
             not any("**D2**" in l and "1,1,2,2,3,3" in l
                     for l in read(DOC).splitlines()),
             "no D2 row line carries the count form")),
     ]),

    ("5", "D4 --- STANDS, and its basis is CORRECTED (mg-e8b8)",
     "the verdict stands and its basis is the quoted theorem, not the builds", [
         ("the row says so", present, (DOC, "**STANDS — and its basis is CORRECTED (mg-e8b8)")),
         ("the old basis is quoted as replaced", quoted_only,
          (DOC, "THE SYNTHESIS OF D2 AND D3", WD + ["was booked"])),
     ]),

    ("5", "D5 --- Updated (mg-e8b8), and two wording defects NOT repaired (X5)",
     "X5 is open: t3 has not moved since delivery and D5 still discloses it", [
         ("D5 discloses X5", present, (DOC, "T3b prints twelve exempt")),
         ("t3 has not moved since delivery", unchanged_since, (DELIVERED, T3)),
         ("the repair did not touch it", untouched_in, (REPAIR, T3)),
     ]),

    ("5", "D12 --- Updated (mg-e8b8)",
     "mg-2060's CMPX evaluation is carried in the row and in section 2", [
         ("the row carries it", present, (DOC, "evaluated (A1) — holds")),
         ("section 2 row 3 carries the current state", present, (DOC, "(A2)(ii)")),
     ]),

    ("6", "What the repair changed in the instrument (mg-e8b8)",
     "T1b2 was added, T1b was renamed, T1d prints the withdrawal, and t2/t3/t4 "
     "are byte-identical to the delivered state", [
         ("T1b2 is in source", present, (T1, "T1b2  THE BRANCHING GRAPH AS VERSHIK-OKOUNKOV DEFINE IT")),
         ("T1b's heading is the corrected one", present, (T1, "T1b  the CELL-module branching data, measured")),
         ("T1d prints the withdrawal", present, (O1, "THE SEPARATING EXAMPLE IS WITHDRAWN")),
         ("t2 byte-identical to delivery", unchanged_since, (DELIVERED, T2)),
         ("t3 byte-identical to delivery", unchanged_since, (DELIVERED, T3)),
         ("t4 byte-identical to delivery", unchanged_since, (DELIVERED, T4)),
         ("out_t2 byte-identical to delivery", unchanged_since, (DELIVERED, O2)),
         ("out_t3 byte-identical to delivery", unchanged_since, (DELIVERED, O3)),
         ("out_t4 byte-identical to delivery", unchanged_since, (DELIVERED, O4)),
     ]),

    ("7", "SUPERSEDED (mg-e8b8) --- the successor question",
     "the superseded sentence is struck and the replacement names the "
     "antichain family", [
         ("struck in place", present, (DOC, "axioms of a tower of recollement (Cox–Martin–Parker–Xi)?**~~")),
         ("the replacement is there", present, (DOC, "must name the **antichain family**")),
     ]),

    ("8", "Repaired 1 --- five sites of the multiplicity-free assertion",
     "none of the five still asserts it", [
         ("site 1, the 'measured (not cited)' sentence", quoted_only,
          (DOC, "(not cited) to be the same multiplicity-free", WD)),
         ("site 2, 'held fixed down that column'", quoted_only,
          (DOC, "Multiplicity-freeness is held\nfixed down that column", WD)),
         ("site 3, section 0's four-row table", present,
          (DOC, "| 1 | 132 | **99** | **no** |")),
         ("site 4, the 2x2 cell", present, (DOC, "`TL_6(1)`: 99 of 132")),
         ("site 5, section 3's two sentences", present,
          (DOC, "**at generic parameters, which is where they are also")),
     ]),

    ("8", "Repaired 4 --- at source, not only in prose",
     "the instrument and its README carry the repair", [
         ("the instrument measures the real invariant", present, (T1, "T1b2")),
         ("the README says so", present, (RDM, "T1b2")),
         ("and carries the mg-13b2 corrections", present, (RDM, "T1c2")),
     ]),

    ("8", "X2 --- CLOSED, in two commits (mg-e8b8 unmarked, mg-13b2)",
     "all four known sites are closed: the 2x2 cell and T1d at 2e66d03, T1a's "
     "header and the section-1 row here", [
         ("the 'iff' is gone from source", absent, (T1, "with a common endpoint exists iff")),
         ("the corrected header is in source", present, (T1, "endpoint exists ONLY IF dim A = sum over the top-level vertices of")),
         ("the refutation block exists", present, (T1, "T1c2  THE 'iff' OF T1a IS FALSE, MEASURED")),
         ("and is in the committed output", present, (O1, "They part at 7 of the 20 pairs:")),
         ("with mg-2060's own counterexample smallest", present, (O1, "THE SMALLEST IS TL_2(0) = k[e]/(e^2)")),
         ("T1d's site was closed by the repair", removed_in,
          (REPAIR, T1, "so the pairs-of-paths basis exists throughout")),
         ("and is marked in place now", present, (T1, "MARKED IN PLACE (mg-13b2)")),
         ("the 2x2 site was closed by the repair", added_in,
          (REPAIR, DOC, "Path-pair *count* survives")),
         ("and the status table books X2 closed", present, (DOC, "| **X2** |")),
     ]),

    ("8", "X3 --- OPEN",
     "the unqualified reading of VO Prop. 1.4 is still in section 1's table", [
         ("the site is still in force", present,
          (DOC, "equivalently (VO Prop. 1.4)")),
         # not `all(...)` over the matching rows: with no matching row that is
         # vacuously true, and a silently-CLOSED X3 would then leave its OPEN
         # label unguarded, which is the defect this whole script is about.
         ("with no semisimplicity qualifier on it", lambda: (
             len([l for l in read(DOC).splitlines()
                  if "(VO Prop. 1.4)" in l and "semisimple" not in l]) == 1,
             "%d unqualified row(s) --- OPEN asserts exactly 1"
             % len([l for l in read(DOC).splitlines()
                    if "(VO Prop. 1.4)" in l and "semisimple" not in l]))),
         ("untouched by the repair", lambda: (
             not any("equivalently (VO Prop. 1.4)" in l
                     for l in diff_lines(REPAIR, DOC, "+")),
             "not added or rewritten at %s" % REPAIR)),
     ]),

    ("8", "X5 --- OPEN", "T3b's twelve sizes are still twelve", [
         ("t3 unchanged since delivery", unchanged_since, (DELIVERED, T3)),
         ("and the defect is disclosed at D5", present, (DOC, "T3b prints twelve exempt")),
     ]),

    ("8", "X6 --- OPEN", "section 7 still says four one-line derivations", [
         ("section 7 still says four", present, (DOC, "**Four elementary")),
         ("and the count is disclosed as disputed", present, (DOC, "census finds eight")),
     ]),

    ("8", "the n = 6 95.7% figure --- OPEN", "still arithmetic, disclosed where "
     "it is quoted", [
         ("disclosed in section 0", present, (DOC, "remains arithmetic")),
         ("disclosed at D5", present, (DOC, "still arithmetic")),
         ("and nothing re-derived it", unchanged_since, (DELIVERED, T3)),
     ]),

    ("8", "Scope --- CORRECTED (mg-13b2): 'and nothing else' was false",
     "the repair's own diff shows it touched two of X2's sites as well as the "
     "two withdrawn claims it books", [
         ("the correction is recorded", present,
          (DOC, "and it also closed two\nsites of X2")),
         ("the diff carries X2's second site", added_in,
          (REPAIR, DOC, "Path-pair *count* survives")),
         ("and X2's third", removed_in,
          (REPAIR, T1, "so the pairs-of-paths basis exists throughout")),
     ]),

    ("8", "What survived the repair on purpose --- section 4's list is intact",
     "all six pre-filed attack items are present, with their outcomes appended", [
         ("six pre-filed attack items", lambda: (
             len([l for l in read(DOC).splitlines() if "**Attack" in l]) == 6,
             "%d attack items found, mg-2060 counted 6"
             % len([l for l in read(DOC).splitlines() if "**Attack" in l]))),
         ("item 3 keeps its dimension-shadow wording", present,
          (DOC, "**dimension shadow**")),
         ("and its outcome is appended, not substituted", present,
          (DOC, "THE SHADOW IS NOT ENOUGH")),
     ]),
]


# ---- the corruption battery -------------------------------------------------
#
# A checker that never fires is indistinguishable from one that cannot.  Each
# entry puts ONE of the defects this repair closed back into the tree --- in
# memory, so nothing on disk is touched --- and names the check that must go
# red.  If a mutation passes, the check it names is decorative and the label it
# guards is unguarded.

MUTATIONS = [
    ("X2 site 2 reopened: the 2x2 cell says 'basis' again",
     DOC, "Path-pair *count* survives", "Path-pair *basis* survives",
     "the cell reads count"),
    ("X2 site 3 reopened: T1a says 'iff' again",
     T1, "endpoint exists ONLY IF dim A = sum over the top-level vertices of",
     "with a common endpoint exists iff dim A = sum over the vertices of",
     "the 'iff' is gone from source"),
    ("X1 reopened: the vertex column goes back to a count",
     DOC, "`[1] [1,1] [1,1] [1,3,1] [1,4,1] [1,4,9,1]`", "1, 2, 2, 3, 3, 4",
     "beta = 1 and beta = 3 are visibly different"),
    ("the document's column drifts one digit from what the instrument "
     "measured, while staying set-shaped",
     DOC, "`[1] [1] [1,2] [1,2] [1,4,5] [1,4,5]`",
     "`[1] [1] [1,2] [1,2] [1,4,5] [1,4,6]`",
     "and the document's four rows ARE the instrument's"),
    ("the false 'Both are open' restored at section 4 item 3",
     DOC, "See mg-2060 §4, X2 and X3.", "Both are open. See mg-2060 §4.",
     "'Both are open' is gone"),
    ("the instrument stops reporting the cells a count would hide",
     O1, "cells where the COUNT agrees and the SET does not: 10 of 36",
     "number of irreducibles per level, as before",
     "and reports the cells a count would hide"),
    ("X3 silently closed while its label still says OPEN --- the exact "
     "label-versus-diff defect this script exists for",
     DOC, "equivalently (VO Prop. 1.4)",
     "equivalently, for semisimple families (VO Prop. 1.4)",
     "with no semisimplicity qualifier on it"),
]

OVERRIDE = {}
_real_read = read


def read(path):                                    # noqa: F811 --- shadows above
    txt = _real_read(path)
    if path in OVERRIDE:
        old, new = OVERRIDE[path]
        if old not in txt:
            raise RuntimeError("mutation target absent from %s: %r" % (path, old))
        txt = txt.replace(old, new)
    return txt


def failing_checks():
    """Every check, run silently; returns the names of the ones that are red."""
    red = []
    for (sec, label, asserts, checks) in LABELS:
        for check in checks:
            try:
                ok = (check[1]() if len(check) == 2 else check[1](*check[2]))[0]
            except Exception:
                ok = False
            if not ok:
                red.append(check[0])
    return red


def battery():
    global BAD
    print("-" * 74)
    print("THE CORRUPTION BATTERY --- does any of this bite?")
    print("-" * 74)
    print("Each row reopens one closed defect IN MEMORY and names the check")
    print("that must go red.  Population: the %d mutations below, against the"
          % len(MUTATIONS))
    print("%d checks above.  Nothing on disk is modified." % CHECKS)
    print()
    for (name, path, old, new, expect) in MUTATIONS:
        OVERRIDE.clear()
        OVERRIDE[path] = (old, new)
        try:
            red = failing_checks()
            fired = expect in red
            detail = "%d check(s) red%s" % (
                len(red), "" if fired else " and NOT the named one")
        except RuntimeError as exc:
            fired, detail = False, "mutation could not be applied: %s" % exc
        print("  [%s] %s" % ("fires" if fired else " DEAD", name))
        print("         must redden: %-46s %s" % (expect, detail))
        if not fired:
            BAD += 1
    OVERRIDE.clear()
    print()


def run():
    global BAD, CHECKS
    print("=" * 74)
    print("T5  EVERY DISPOSITION LABEL, CHECKED AGAINST THE TREE AND THE DIFF")
    print("=" * 74)
    print("mg-13b2, on mg-a218's finding that a label said 'deliberately NOT")
    print("repaired' while the diff had closed 2 of that finding's 3 sites.")
    print()
    print("A label is checked, never read.  Each check is a statement about the")
    print("CURRENT TREE or about a NAMED HISTORICAL COMMIT --- never about the")
    print("diff of the commit this script is part of, which is why it says the")
    print("same thing on a re-run.")
    print()
    print("commits named by the labels: %s (mg-db09, as delivered), %s"
          % (DELIVERED, REPAIR))
    print("(mg-e8b8, the repair mg-a218 audited), %s (the roadmap retraction)."
          % RETRACT)
    print()
    for (sec, label, asserts, checks) in LABELS:
        print("-" * 74)
        print("SECTION %s   %s" % (sec, label))
        print("  asserts: %s" % asserts)
        for check in checks:
            CHECKS += 1
            name = check[0]
            if len(check) == 2:
                ok, detail = check[1]()
            else:
                ok, detail = check[1](*check[2])
            print("    [%s] %-52s %s" % ("ok" if ok else "BAD", name, detail))
            if not ok:
                BAD += 1
                print("      BAD: the label above is not what the tree says")
    print("-" * 74)
    print()
    battery()
    print("EXTENT OF THIS CHECK, stated so it cannot be read as wider than it is:")
    print("  labels checked      : %d" % len(LABELS))
    print("  individual checks   : %d" % CHECKS)
    print("  corruptions applied : %d, all in memory" % len(MUTATIONS))
    print("  files read          : %d" % len(FILES))
    for f in sorted(FILES):
        print("      %s" % f)
    print("  commits consulted   : %s" % ", ".join(sorted(COMMITS)))
    print()
    print("  WHAT IT DOES NOT COVER.  It checks the labels this document")
    print("  carries; it cannot find a claim that was quietly changed and")
    print("  never labelled at all.  That is a seam sweep (mg-a218's c4), not")
    print("  a label audit, and the fourth X2 site recorded in section 1 was")
    print("  found by sweeping and not by this script.")
    print()
    print("TOTAL BAD: %d" % BAD)
    return BAD


if __name__ == "__main__":
    try:
        git("rev-parse", "--git-dir")
    except Exception as exc:
        sys.stderr.write("t5_labels.py needs a git checkout: %s\n" % exc)
        sys.exit(2)
    sys.exit(1 if run() else 0)
