"""mg-2ff6 / D4 -- MY OWN BETS, MY OWN DEFECTS, AND WHAT I DID NOT DO.

Nine bets were committed in `PREDICTIONS.md` before one line of `lib2ff6.py`
existed and before any probe in either tree was edited.  They are scored here
against the transcripts this suite just wrote, and a bet that lost stays lost:
a scored MISS is not a check failure and does not move the exit code, because
an exit code that punishes a recorded miss is an exit code that rewards tuning
the bet after the fact.

  D4a  THE CONVERGENCE ARM -- P7, and it is the only bet whose evidence had to
       be built into the runner rather than read off a transcript
  D4b  THE BETS
  D4c  THE DEFECTS OF THIS INSTRUMENT, kept
  D4d  WHAT THIS TICKET DID NOT DO

Exit code = 0.
"""

import os
import sys

import lib2ff6 as U

U.bar("mg-2ff6 / D4 -- MY OWN BETS AND MY OWN DEFECTS")
print("HEAD: %s" % U.head())

SNAP = os.path.join(U.HERE, "snap")

# ---------------------------------------------------------------------------
U.hdr("D4a  THE CONVERGENCE ARM -- P7")

print("  Every probe in this suite censuses `code/*/out_*.txt`, and this")
print("  tree's own transcripts are in that glob.  So round 1 reads a corpus")
print("  without them and round 2 reads one with them.  P7 bets that this")
print("  SETTLES: rounds 2 and 3 byte-identical, round 1 not.  The mechanism")
print("  it rests on is cfd9c's S1 -- the SHAPE of a transcript here does not")
print("  depend on the VALUES in it, so the row count stops moving after one")
print("  round even though the values are still catching up.")
print()
print("  `snap/` is round 2's bytes.  This probe is the only thing that reads")
print("  them and they are not committed.")
print()
U.pop("the TRANSCRIPTS this suite rewrites each round")
watched = [
    "../grain_axis_audit_03d1/out_a1_axes.txt",
    "../grain_axis_audit_03d1/out_a6_self.txt",
    "../grain_arity_9160/out_selftest_9160.txt",
    "../grain_arity_9160/out_s1_reproduce.txt",
    "../grain_arity_9160/out_s2_arity.txt",
    "../grain_arity_9160/out_s3_population.txt",
    "../grain_arity_9160/out_s4_open.txt",
    "../grain_arity_9160/out_s5_self.txt",
    "./out_d0_selftest.txt",
    "./out_d1_moved.txt",
    "./out_d2_convention.txt",
    "./out_d3_prose.txt",
]
same = diff = missing = 0
detail = []
for rel in watched:
    cur = os.path.join(U.HERE, rel)
    snap = os.path.join(SNAP, os.path.basename(rel))
    if not os.path.exists(snap) or not os.path.exists(cur):
        missing += 1
        detail.append((rel, "NO SNAPSHOT"))
        continue
    a = open(snap, encoding="utf-8", errors="replace").read()
    b = open(cur, encoding="utf-8", errors="replace").read()
    if a == b:
        same += 1
        detail.append((rel, "identical"))
    else:
        diff += 1
        na = len(U.A.count_rows(a))
        nb = len(U.A.count_rows(b))
        detail.append((rel, "DIFFERS  (count rows %d -> %d)" % (na, nb)))
for rel, verdict in detail:
    print("      %-46s %s" % (os.path.basename(rel), verdict))
print()
U.plain("...TRANSCRIPTS compared, round 2 against round 3", len(watched))
print("      ^ one unit of that number is one transcript file")
U.plain("...of them BYTE-IDENTICAL between the two rounds", same)
print("      ^ one unit of that number is one transcript file")
U.plain("...of them that DIFFER", diff)
print("      ^ one unit of that number is one transcript file")
U.plain("...with NO SNAPSHOT to compare against", missing)
print("      ^ one unit of that number is one transcript file")
print()
print("  `out_d4_self.txt` IS NOT IN THAT LIST AND CANNOT BE.  It is written")
print("  after the comparison, by the probe doing the comparing, so a round")
print("  that included it would be comparing a file that does not exist yet.")
print("  That is cfd9c's S3b/1 arriving in my own self-check, and the honest")
print("  thing is to say which file the arm cannot see rather than to widen")
print("  the arm until it looks total.")
P7 = diff == 0 and missing == 0

# ---------------------------------------------------------------------------
U.hdr("D4b  THE BETS")


def readf(p):
    try:
        return U.read("code/dated_population_2ff6/" + p)
    except Exception:
        return ""


d1 = readf("out_d1_moved.txt")
d2 = readf("out_d2_convention.txt")
d3 = readf("out_d3_prose.txt")


def figure(txt, label, default=-1):
    """The value of the ONE count row with this label.

    RAISES IF THE LABEL IS NOT UNIQUE, and that guard is here because the
    first form of this function returned the FIRST match.  `out_d2_convention`
    printed `...of them carrying a DATED population line` FOUR times -- as
    committed, live, cfd9c's own tree, and excluding mine -- and
    `out_d1_moved` printed `...of them that MOVED` twice.  So P2's evidence
    line was read off the BEFORE block and P3 was scored MISS against D1b's
    total when D1c's arc subset makes it a HIT.  The labels were made unique;
    this raises so that the next ambiguous one is a stack trace and not a
    quietly wrong verdict about my own bet.
    """
    hits = [nums[0] for _i, lab, nums in U.A.count_rows(txt)
            if lab.strip() == label and nums]
    if len(hits) > 1:
        raise RuntimeError(
            "ambiguous label %r -- %d count rows carry it, and reading the "
            "first is how a bet gets scored off the wrong block"
            % (label, len(hits)))
    return hits[0] if hits else default


n_arc = figure(d1, "...ARC-WIDE FIGURES in the re-run transcripts")
n_arcmoved = figure(d1, "...of those ARC-WIDE FIGURES that MOVED")
n_outside = figure(d2, "...FLAGGED ROWS outside the two trees in scope")
n_dated = figure(d2, "...of them carrying a DATED population line")
n_found = figure(d2, "...ARC-WIDE FIGURES S4c found in the arc")
n_exfound = figure(d2, "...ARC-WIDE FIGURES in the arc EXCLUDING this tree")
n_exdated = figure(d2, "...of them DATED, EXCLUDING this tree")
n_changed = figure(d3, "...of them whose FIGURE CHANGED -- must be 0")
n_sites = figure(d3, "...PROSE SITES carrying an arc-wide corpus figure")
n_prosedated = figure(d3, "...of them now carrying a REF beside the figure")
n_literal = figure(d3, "...LINES printing the count as a LITERAL `0`")


BETS = [
    ("P1", 0.80, "the 27 is an over-count; >= 4 of the 5 outside are not "
     "arc-wide", n_outside >= 4,
     "D2d: %d flagged rows outside the two trees, and all %d are a per-tree "
     "census or a control" % (n_outside, n_outside)),
    ("P2", 0.70, "S4c scores 22 of 27 after this ticket, not 27 of 27",
     n_dated == 22 and n_found == 27,
     "D2b: %d of %d -- MISSED AS STATED, and missed by MY OWN E3.  The "
     "denominator is not 27 any more because this tree's own transcripts "
     "entered the corpus S4c censuses and brought %d arc-wide figures with "
     "them, all dated.  With this tree taken out, D2c reads %d of %d, which "
     "is the number the bet meant -- and it is NOT how the bet is scored."
     % (n_dated, n_found, n_found - n_exfound, n_exdated, n_exfound)),
    ("P3", 0.60, "at most 15 of the 22 arc-wide figures actually MOVE",
     0 <= n_arcmoved <= 15,
     "D1c: %d of %d moved" % (n_arcmoved, n_arc)),
    ("P4", 0.75, ">= 3 of mg-9160's 4 flagged rows do not move", True,
     "D1c: 400, 11 and 79800 are FROZEN at 9f1ecaa+eacc5e1 and did not "
     "move; only `the disk at HEAD now` did -- 3 of 4"),
    ("P5", 0.85, "`classifying BOTH` stays 0",
     "...of those grain WORDS classifying BOTH" in d1
     and " 0          0 " in d1,
     "D1a: 0 -> 0, and structurally so: `grain_nouns` returns single "
     "de-pluralised nouns and BOTH needs one string in two word lists"),
    ("P6", 0.85, "`files` interval empty at every OBSERVED figure, and at "
     "least one other field's is not", True,
     "the interval blocks in out_a1_axes.txt and out_s1_reproduce.txt: "
     "`files` empty in both, `rows` and `words` non-empty in both"),
    ("P7", 0.60, "rounds 2 and 3 are byte-identical; round 1 is not", P7,
     "D4a: %d of %d transcripts identical, %d differ" % (same, len(watched),
                                                         diff)),
    ("P8", 0.90, "all 10 prose sites keep their published value",
     n_changed == 0 and n_prosedated == n_sites,
     "D3b: %d of %d figures changed, %d of %d now dated"
     % (n_changed, n_sites, n_prosedated, n_sites)),
    ("P9", 0.70, "cfd9c's S2c prints its ref count as a literal and still "
     "says 0 after this ticket", n_literal == 1,
     "D3c: `s2_drift.py:245` prints the digit; `noref` above it is computed "
     "over the PATH and never used"),
]
U.pop("the 9 BETS of PREDICTIONS.md, one row each")
hit = 0
for pid, p, claim, ok, why in BETS:
    hit += bool(ok)
    print("      %-4s %4.2f %-52.52s %s"
          % (pid, p, claim, "HIT" if ok else "MISS"))
    print("                %s" % why)
print()
U.plain("...BETS scored HIT", hit)
print("      ^ one unit of that number is one prediction")
U.plain("...BETS scored MISS", len(BETS) - hit)
print("      ^ one unit of that number is one prediction")
print()
print("  P4 AND P6 ARE SCORED BY READING AND NOT BY AN EXPRESSION, and saying")
print("  so is cheaper than defending them.  Both are claims about which")
print("  ROWS carry which class, and the class lives on a line that is not a")
print("  count row -- so a scoring expression would have had to parse my own")
print("  layout, which is the weakest possible evidence for a bet about my")
print("  own layout.  The transcripts they cite are in this commit.")

# ---------------------------------------------------------------------------
U.hdr("D4c  THE DEFECTS OF THIS INSTRUMENT, KEPT")

DEFECTS = [
    ("D1", "MY OWN POPULATION LINES WRAPPED, AND S4c WAS RIGHT TO FAIL THEM. "
     "The first form of `a1_axes.py`'s A1d subset line and of `a6_self.py`'s "
     "AS7 line ran past the margin, so `population:` was on one line and the "
     "`@ref` on the next -- and S4c reads the ref off the line carrying the "
     "word.  It scored `grain_axis_audit_03d1` at 15 of 18.  THE TICKET "
     "FORBIDS RESPECIFYING THE CHECKER AND THE CHECKER WAS NOT TOUCHED: the "
     "probes were shortened, and `lib2ff6.pop` now REFUSES a multi-line "
     "population text, because `remember not to wrap` is not a fix."),
    ("D2", "MY PROSE-SITE FOLLOWER REPORTED TWO DATED SITES AS DELETED.  It "
     "matched a fixed 48-character stem, and this ticket's own marker is "
     "inserted at character 35 of both `PREDICTIONS.md:5` and "
     "`README.md:118` -- so the stem no longer occurred and `_follow` "
     "returned None, which D3b prints as `*** GONE`.  A false alarm in the "
     "one direction that reads as `I deleted two published claims`.  Found "
     "by the check firing, not by reading the code; the rule is now longest "
     "common prefix with a floor."),
    ("D3", "I MADE TWO OLD TREES DEPEND ON A NEW ONE.  `lib03d1.convention()` "
     "and `lib9160.convention()` import `lib2ff6`, which imports `libfd9c`. "
     "Neither tree re-runs now in a checkout that lacks either directory. "
     "The alternative was a third and fourth copy of a convention that "
     "already has one definition, and cfd9c's own rule is that a second "
     "definition agreeing today is worse than the first.  The dependency is "
     "the price and it is paid knowingly."),
    ("D4", "THE REF ON EVERY FIGURE HERE IS A COMMIT AND MY RUNS READ THREE "
     "DIFFERENT DISKS.  `libfd9c.at()` returns the committed HEAD, which is "
     "honest about the COMMIT and silent about the WORKING TREE -- and this "
     "suite's three rounds read three different working trees.  D4a is the "
     "only thing standing between that and a false impression of stability, "
     "and it is an arm about BYTES rather than about the ref."),
    ("D5", "AND THE REF IS ONE COMMIT EARLY, IN EVERY TRANSCRIPT IN THIS "
     "COMMIT.  A probe runs before the commit that publishes its output, so "
     "the `@` on every population line names the commit BEFORE the one you "
     "are reading.  cfd9c's `at()` documents this about itself; I inherit it "
     "unrepaired, and a reader reproducing a figure here must check out the "
     "ref printed and not the publishing commit."),
    ("D6", "MY ACCOUNTING CANNOT SEE A CHANGE TO A LINE THAT IS NOT A COUNT "
     "ROW.  `d1` diffs count rows, so a moved percentage (`86.0%` -> "
     "`88.6%`) is INVISIBLE to it -- those are printed as prose, not as "
     "count rows, in both trees.  The figure moved and my accounting does "
     "not name it.  I know of two: A1d's `collapse rate over the corpus's "
     "own grain words` and its `collapse rate on the words it can speak "
     "about`."),
    ("D7", "I SCORE TWO OF MY OWN NINE BETS BY READING.  P4 and P6 are "
     "claims about which class sits beside which row, and the class is not "
     "a count row -- so an expression scoring them would parse my own "
     "layout.  Both are marked in D4b as read rather than computed."),
    ("D10", "AND MY SCORER READ THE WRONG ROW FOR TWO OF MY OWN BETS.  "
     "`figure()` returned the FIRST count row with a given label, and my own "
     "`d2` prints `...of them carrying a DATED population line` four times "
     "and my own `d1` prints `...of them that MOVED` twice -- so P2's "
     "evidence was read off the BEFORE block (`0 of 27`) and P3 was scored "
     "MISS against 17, which is D1b's total over ALL count rows, when D1c's "
     "arc subset is 13 and makes it a HIT.  Caught by reading the scored "
     "table, not by an arm.  The labels are unique now and `figure()` RAISES "
     "on a duplicate."),
    ("D9", "MY OWN ROLL WAS NOT DETERMINISTIC AND ONLY THE CONVERGENCE ARM "
     "SAW IT.  `diff_rows` sorted every row by its line number in whichever "
     "text had it, which interleaves the published numbering with the "
     "current one -- so one added line anywhere transposed two DROPPED rows "
     "and `out_d1_moved.txt` differed between two rounds by nothing else.  "
     "D4a caught it, which is the only job D4a has, and the order is now "
     "published-first with the added rows appended."),
    ("D8", "I LEFT A FALSE CLAIM STANDING IN A FILE I EDITED.  "
     "`s1_reproduce.py` says the HEAD row `OSCILLATES between 1984 and 1966 "
     "without ever converging`, and cfd9c REFUTED that -- the census map "
     "settles at run 2 and the two values are two readings of ONE state.  I "
     "re-ran that probe and republished the sentence.  Repairing it is "
     "mg-fd9c's finding landing in mg-9160's prose, which is a different "
     "ticket's edit, and doing it here would have moved a claim this ticket "
     "was not sent to move."),
]
U.pop("the DEFECT ITEMS of this instrument, found by running it")
for did, text in DEFECTS:
    print()
    import textwrap
    lines = textwrap.wrap(text, 66)
    print("      %-4s %s" % (did, lines[0]))
    for ln in lines[1:]:
        print("           %s" % ln)
print()
U.plain("...DEFECT ITEMS recorded", len(DEFECTS))
print("      ^ one unit of that number is one recorded defect")

# ---------------------------------------------------------------------------
U.hdr("D4d  WHAT THIS TICKET DID NOT DO")

print("  1. IT DID NOT TOUCH THE FOUR OTHER TREES S4c FLAGS.  Five rows in")
print("     `runner_exit_audit_56dc`, `runner_exit_repair_70c7`,")
print("     `runner_exit_repair_bf79` and `state_relocation_audit_b0ae` are")
print("     still undated.  Every one is a per-tree census or a control that")
print("     S4c's label rule over-collects -- D2d prints all five with their")
print("     values -- so dating them would decorate figures that are not")
print("     about the arc at all, and the score would read 27 of 27 for a")
print("     worse reason than it now reads 22.")
print()
print("  2. IT DID NOT REPAIR cfd9c's S2c.  Its `0` is a literal beside an")
print("     unused `noref` computed over the path, and it will report `0 of")
print("     10 dated` after this ticket.  Repairing it means re-running")
print("     cfd9c's suite, which would overwrite the BEFORE reading D2 rests")
print("     on.  Named here so the next ticket does not have to find it.")
print()
print("  3. IT DID NOT RE-RUN `a2`-`a5` OF mg-03d1.  D1d names all five")
print("     transcripts left at their published bytes.  `mg-03d1` is now a")
print("     tree whose transcripts come from two different runs -- which is")
print("     exactly the condition this convention exists to make readable,")
print("     and which every population line in the two re-run transcripts")
print("     now states outright.")
print()
print("  4. IT DID NOT MAKE A GROWING FIGURE COMPARABLE TO ITSELF.  cfd9c's")
print("     S4d says this and it survives adoption: two dated readings of")
print("     `count ROWS in them` are two facts about two corpora, and")
print("     subtracting them measures the arc.  D1a prints those deltas and")
print("     they are measurements of growth, not of the classifier.")
print()
print("  5. IT DID NOT DATE A MEMBERSHIP.  D1b's finding: `out_a6_self.txt`")
print("     carries a table whose ROW SET is a function of the corpus, and")
print("     five rows left it while five joined.  The convention dates")
print("     VALUES.  Nothing in it reaches a table that grows rows.")

print()
print("D4 TOTAL BAD: 0")
sys.exit(0)
