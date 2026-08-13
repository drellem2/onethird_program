#!/usr/bin/env python3
"""mg-2959 — THE ARM THIS DIRECTORY DID NOT HAVE: ITS OWN PROSE.

WHY IT EXISTS, AND THE INSTANCE IS THIS DIRECTORY'S OWN README.

`report.py` is a pure function of the frozen sweep record, and two consecutive
runs of `run_all.sh` produce byte-identical transcripts.  Every figure in the
TRANSCRIPTS is therefore regenerated on every run and cannot go stale.  Nothing
regenerated the figures in the PROSE, and three of them were wrong:

    README.md  §4   "Together these took the first reported figure 186 -> 157
                    -> 156"          — the shipped figure is not 156
    README.md  §4   "186 suites to 187 without disturbing the other 186"
    run_all.sh      "re-runs 192 suites in isolated clones"

All three describe the FIRST sweep — the one this directory's own `--only` bug
truncated and which had to be retaken — narrated in the present tense and never
updated when §7 was.  §7 and §8 carry the shipped record's figures and §4 does
not, in the same file, with nothing between them saying so.

THE CONSEQUENCE WAS NOT HYPOTHETICAL AND IT IS WHY THIS ARM IS WORTH A FILE.
The mayor read §4 and filed mg-2959 with a headline number and a whole derived
breakdown that appears in NO committed artifact of this repository.  A stale
prose figure inside the instrument built to count stale verdicts, propagated
into a work item's title within hours.  That is this directory's own subject,
one surface out — the surface it did not cover.

------------------------------------------------------------------------------
THE RULE IS BORROWED AND NOT RE-SPELLED.

`lib7522.figures()` is this estate's rule for *is this number a FIGURE — a
measurement that must be backed by a transcript?*, and `lib7522.
transcript_figures()` is its rule for *what does a transcript back?*.  Both are
imported.  A second definition of "figure" is a second place for the definition
to drift, which is the reason `lib30bd` imports `lib_f771.verdict_for` rather
than re-implementing "benign", and the reason is the same here.

The verdict is mg-7522's, quoted from `s5_self.py`: *a USE is BACKED when every
figure on its line appears in one of this tree's committed transcripts, and
UNBACKED otherwise.*  What is NOT borrowed is its restriction to lines carrying
a strength marker: mg-7522 was asking whether a figure stood on a word like
"verified", and none of the three defects above stands on one.

------------------------------------------------------------------------------
TWO POLARITIES, AND THE SECOND IS `report.py`'s OWN.

  IN THE README'S OWN VOICE — a line outside a fenced block.  An unbacked
    figure here is a claim this directory makes and cannot support.  GRADED.
    A finding exits 1.

  INSIDE A FENCED BLOCK — a quotation.  This README fences three things: the
    ALL-CAPS derivation table §2's token set came from, the gate hunk §4 quotes
    from a sandbox run, and §7's own figure table.  A quotation of a run this
    directory did not keep cannot be checked against a transcript it does not
    have, and this arm CANNOT TELL A STALE QUOTATION FROM A FAITHFUL ONE.  So
    an unbacked figure in a fence is COUNTED, LISTED IN FULL, AND NOT GRADED —
    exactly the polarity `report.py` gives a run that was killed or refused, and
    for the same reason: unmeasured is not clean.  §5 says what that costs.

    A BACKED figure inside a fence is still reported as BACKED, so §7's table —
    the strongest figures in this README — is positively checked and is not
    merely un-condemned.

------------------------------------------------------------------------------
THE EXCLUSION THAT MAKES THIS ARM NOT SELF-CONFIRMING.

This arm PRINTS the unbacked figures it finds.  Its own transcript is therefore
a committed transcript of this directory that prints `156` — so on the next run
`156` would be BACKED, by the report of its being unbacked, and the finding
would erase itself.  A repair operation destroying the thing repaired is this
estate's recurring shape and it turned up inside `sweep.py` already; here it
would have turned the arm green on its second run and left the README wrong.

`out_prose_30bd.txt` is excluded from the backing corpus BY NAME, and §4 plants
the world that proves the exclusion is load-bearing rather than tidy.

Exit codes:  0  every figure in the README's own voice is backed
             1  a figure in the README's own voice that no transcript backs
             2  refused — the borrowed rule or the backing corpus is missing
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

# mg-7522's rule, imported.  `lib7522` derives its REPO from the process's cwd;
# a runner's cwd is whatever the caller's was, so the root is taken from
# __file__ — the rule `lib30bd` already uses — and PINNED INTO the borrowed
# module rather than left depending on where somebody happened to stand.
sys.path.insert(0, os.path.join(ROOT, "code", "runner_exit_repair_7522"))
try:
    import lib7522 as L                                             # noqa: E402
except ImportError as exc:                                          # pragma: no cover
    sys.stderr.write("mg-2959: cannot import lib7522 (%s).  This arm has no rule "
                     "of its own and refuses to invent one.\n" % exc)
    raise SystemExit(2)
L.REPO = ROOT

# The prose artifacts of this directory: what a reader reads INSTEAD OF running
# anything.  The `.py` docstrings are deliberately outside this population and
# §5 says why.
PROSE = ("README.md", "run_all.sh")

# THE ARM'S OWN TRANSCRIPT, EXCLUDED BY NAME.  See the header block.
SELF_OUT = "out_prose_30bd.txt"

W = 78


def bar(t):
    print("=" * W)
    print(t)
    print("=" * W)


def hdr(t):
    print()
    bar(t)
    print()


def own_transcripts(exclude_self=True):
    """This directory's committed out_*.txt, absolute, sorted."""
    names = sorted(n for n in os.listdir(HERE)
                   if n.startswith("out_") and n.endswith(".txt"))
    if exclude_self:
        names = [n for n in names if n != SELF_OUT]
    return [os.path.join(HERE, n) for n in names]


def fenced(text):
    """{line number} -- the lines of `text` that sit inside a ``` fence.

    The fence markers themselves are inside: a marker carries no figure, and a
    rule that had to decide would be deciding about nothing.
    """
    inside, out, open_ = set(), set(), False
    for i, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            open_ = not open_
            inside.add(i)
            continue
        if open_:
            inside.add(i)
        else:
            out.add(i)
    del out
    return inside


def census(paths, corpus):
    """[(rel, lineno, line, figures, missing, in_fence)] -- one row per line
    that carries at least one figure."""
    rows = []
    for p in paths:
        text = L.read(p, None)
        fence = fenced(text)
        rel = os.path.basename(p)
        for i, line in enumerate(text.splitlines(), 1):
            figs = L.figures(line)
            if not figs:
                continue
            missing = [v for v in figs if v not in corpus]
            rows.append((rel, i, line.strip(), figs, missing, i in fence))
    return rows


def show(rel, i, line, miss, width=44):
    return "      %-14s %4d  %-18s %s" % (
        rel, i, ",".join(str(v) for v in miss)[:18], line[:width])


def main():
    outs = own_transcripts()
    if not outs:
        sys.stderr.write("mg-2959: this directory has no committed transcript to "
                         "back anything.  Run the other arms first.\n")
        return 2

    corpus = L.transcript_figures(outs)
    paths = [os.path.join(HERE, n) for n in PROSE]
    missing_prose = [p for p in paths if not os.path.exists(p)]
    if missing_prose:
        sys.stderr.write("mg-2959: prose artifact(s) absent: %s\n"
                         % ", ".join(os.path.basename(p) for p in missing_prose))
        return 2

    bar("mg-2959 -- IS EVERY FIGURE IN THIS DIRECTORY'S PROSE BACKED BY ONE OF ITS")
    print("          OWN TRANSCRIPTS?")
    print("=" * W)
    print()
    print("  the question    : `report.py` regenerates every figure in the TRANSCRIPTS")
    print("                    on every run, so none of them can go stale.  NOTHING")
    print("                    regenerates the figures in the PROSE.  This arm is the")
    print("                    thing that reads them.")
    print("  the rule        : mg-7522's, imported and not re-spelled --")
    print("                    `lib7522.figures` and `lib7522.transcript_figures`.")
    print("  the verdict     : mg-7522's own words: a USE is BACKED when every figure")
    print("                    on its line appears in one of this tree's committed")
    print("                    transcripts, and UNBACKED otherwise.")
    print("  produced by     : python3 -B prose_30bd.py, which is what run_all.sh runs")
    print("                    LAST, so it grades the transcripts this run just wrote.")
    print()

    # ------------------------------------------------------------------ P1
    hdr("P1  THE BACKING CORPUS, AND THE ONE FILE IT EXCLUDES BY NAME")

    for p in outs:
        print("      backs   %s" % os.path.basename(p))
    print("      EXCLUDED  %s   -- this arm's own transcript" % SELF_OUT)
    print()
    print("  THIS ARM PRINTS THE UNBACKED FIGURES IT FINDS, so its own transcript is a")
    print("  committed transcript of this directory that prints them.  Left in the")
    print("  corpus, every finding would be BACKED on the next run BY THE REPORT OF ITS")
    print("  BEING UNBACKED, and the arm would go green with the prose still wrong.")
    print("  That is `sweep.py`'s `--only` defect one surface out: a repair operation")
    print("  destroying the thing it repairs.  P4c plants the world that proves the")
    print("  exclusion does work rather than merely reads as though it should.")
    print()
    print("      %d distinct figure(s) backed by the corpus above" % len(corpus))
    print()

    # ------------------------------------------------------------------ P2
    hdr("P2  THE CENSUS")

    rows = census(paths, corpus)
    voice_bad = [r for r in rows if r[4] and not r[5]]
    fence_bad = [r for r in rows if r[4] and r[5]]
    backed = [r for r in rows if not r[4]]
    print("  %5d  line(s) carrying at least one figure" % len(rows))
    print("  %5d  BACKED                 every figure printed by a transcript above"
          % len(backed))
    print("  %5d  UNBACKED/own-voice     outside a fence -- GRADED, and the finding"
          % len(voice_bad))
    print("  %5d  UNBACKED/quoted        inside a ``` fence -- REPORTED, NOT GRADED"
          % len(fence_bad))
    print()
    print("  A FENCE IS A QUOTATION.  This README fences the ALL-CAPS derivation table")
    print("  §2's token set came from, the gate hunk §4 quotes from a sandbox run, and")
    print("  §7's own figure table.  This arm cannot tell a stale quotation from a")
    print("  faithful one, so it counts them and does not grade them -- the polarity")
    print("  `report.py` gives a run that was killed or refused, for the same reason:")
    print("  UNMEASURED IS NOT CLEAN.  §5 says what it costs.")
    print()
    print("  BACKED, in full -- a check that reports only failures cannot be told from")
    print("  one that checks nothing:")
    print()
    print("      %-14s %4s  %-18s %s" % ("file", "line", "figures", "the line"))
    print("      " + "-" * 70)
    for rel, i, line, figs, _m, in_fence in backed:
        print("%s%s" % (show(rel, i, line, figs), "   [fence]" if in_fence else ""))
    print()

    # ------------------------------------------------------------------ P3
    hdr("P3  THE FINDINGS")

    if not voice_bad:
        print("      none.  Every figure this README states in its own voice is printed")
        print("      by one of this directory's own transcripts.")
    else:
        print("      %-14s %4s  %-18s %s" % ("file", "line", "no transcript", "the line"))
        print("      " + "-" * 70)
        for rel, i, line, _f, miss, _q in voice_bad:
            print(show(rel, i, line, miss, width=44))
        print()
        print("      *** each of those is a figure this directory states and cannot support ***")
    print()
    print("  REPORTED AND NOT GRADED -- the quotations:")
    print()
    if not fence_bad:
        print("      none.")
    for rel, i, line, _f, miss, _q in fence_bad:
        print(show(rel, i, line, miss, width=44))
    print()

    # ------------------------------------------------------------------ P4
    hdr("P4  THE CONTROLS -- THIS ARM IS SHOWN TO FIRE, ON THE BYTES THAT SHIPPED")

    bad = 0

    print("  P4a  THE THREE DEFECTS THAT WERE IN THIS DIRECTORY, VERBATIM.  These are")
    print("       not invented lines: each is the exact text that was committed, and")
    print("       the repair is what makes them absent from P3 rather than an")
    print("       assertion that they never happened.")
    print()
    # Each historical line, with the figure that no transcript of this directory
    # printed at the time and does not print now.
    HISTORY = [
        ("README.md §4",
         "Together these took the first reported figure **186 -> 157 -> 156**, "
         "all downward, before", 156),
        ("README.md §4",
         "186 suites to 187 without disturbing the other 186. `report.py` also "
         "takes the **first**", 186),
        ("run_all.sh",
         "# re-runs 192 suites in isolated clones, takes hours, executes "
         "instrument code across the", 192),
    ]
    for where, line, want in HISTORY:
        figs = L.figures(line)
        miss = [v for v in figs if v not in corpus]
        ok = want in miss
        bad += not ok
        print("      %-14s %-8s %s" % (where, "FIRES" if ok else "*** SILENT ***",
                                       "on %d" % want))
        if not ok:
            print("          figures %s, missing %s" % (figs, miss))
    print()

    print("  P4b  DISCRIMINATION.  A figure no transcript can print must come back")
    print("       UNBACKED, or the census is reporting the absence of a check.")
    print()
    impossible = max(corpus) + 7919 if corpus else 7919
    probe = "the population is %d transcripts" % impossible
    ok = impossible in [v for v in L.figures(probe) if v not in corpus]
    bad += not ok
    print("      a figure of %d, which no transcript here prints        %s"
          % (impossible, "ok" if ok else "*** BACKED ***"))
    probe2 = "the population is %d transcripts" % (sorted(corpus)[-1] if corpus else 0)
    ok2 = not [v for v in L.figures(probe2) if v not in corpus]
    bad += not ok2
    print("      a figure of %d, which one of them does                 %s"
          % (sorted(corpus)[-1] if corpus else 0, "ok" if ok2 else "*** UNBACKED ***"))
    print()

    print("  P4c  THE SELF-CONFIRMING WORLD.  With this arm's own transcript in the")
    print("       backing corpus, a finding is backed by the report of itself.  Planted")
    print("       rather than asserted: the row THIS ARM WOULD HAVE PRINTED is built in")
    print("       the same format P3 prints, put into the corpus, and the line re-graded.")
    print()
    where, line, want = HISTORY[2]                       # run_all.sh, one figure: 192
    row = show("run_all.sh", 7, line, [want])
    synthetic = set(corpus) | set(L.figures(row))
    before = [v for v in L.figures(line) if v not in corpus]
    after = [v for v in L.figures(line) if v not in synthetic]
    ok = before and not after
    bad += not ok
    print("      the row this arm would print:  %s" % row.strip())
    print("      the line, against the shipped corpus         UNBACKED on %s"
          % ",".join(str(v) for v in before))
    print("      the same line, corpus + that row             %s"
          % ("BACKED  <- the finding erases itself" if not after
             else "*** still UNBACKED on %s ***" % after))
    print("      so the exclusion in P1 is load-bearing       %s"
          % ("ok" if ok else "*** THE PLANT DID NOT REPRODUCE ***"))
    print()
    print("       AND THE MULTI-FIGURE ROWS DO NOT CLOSE THE LOOP, WHICH IS AN ACCIDENT")
    print("       OF FORMATTING AND NOT A SECOND DEFENCE.  P3 joins several missing")
    print("       figures with commas, and mg-7522's number rule reads a comma as a")
    print("       thousands separator, so `186,157,156` comes back as one figure:")
    multi = show("README.md", 161, HISTORY[0][1], [186, 157, 156])
    print("           %s" % ", ".join(str(v) for v in L.figures(multi.strip())))
    print("       Nothing chose that.  Change the separator and the loop closes for")
    print("       every row, so the exclusion above is the defence and this is not.")
    print()

    print("  P4d  THE FENCE RULE, ON A PLANTED DOCUMENT rather than on this README,")
    print("       because a boundary measured only on the file it was written for is")
    print("       measured on one point.")
    print()
    doc = "a line\n```\nin a fence\n```\nafter\n"
    got = sorted(fenced(doc))
    want = [2, 3, 4]
    ok = got == want
    bad += not ok
    print("      lines inside the fence: expected %s, got %s        %s"
          % (want, got, "ok" if ok else "*** WRONG ***"))
    unclosed = sorted(fenced("a\n```\nb\nc\n"))
    ok2 = unclosed == [2, 3, 4]
    bad += not ok2
    print("      an UNCLOSED fence swallows the rest: %s              %s"
          % (unclosed, "ok" if ok2 else "*** WRONG ***"))
    print("      -- which is the FAIL-QUIET direction and it is named rather than")
    print("      repaired: an unclosed fence moves lines from GRADED to REPORTED, so")
    print("      a malformed README makes this arm quieter and never louder.  §5.3.")
    print()

    # ------------------------------------------------------------------ P5
    hdr("P5  WHAT THIS ARM CANNOT SEE")

    print("  1  A QUOTATION IS NOT GRADED.  %d unbacked figure(s) sit inside a fence"
          % len(fence_bad))
    print("     and are listed in P3 rather than counted against the verdict.  §2's")
    print("     ALL-CAPS derivation table is the big one: the frequency counts that")
    print("     chose the token set were produced by a run nobody kept, so THE ONLY")
    print("     JUSTIFICATION FOR THE INSTRUMENT IS ITSELF IN THE CLASS THIS DIRECTORY")
    print("     COUNTS.  Making it backed means re-taking that census and keeping it;")
    print("     that is remainder and it is filed, not absorbed here.")
    print()
    print("  2  A FIGURE THAT IS RIGHT IN THE SET AND WRONG IN ITS ROLE IS INVISIBLE,")
    print("     AND THE FOURTH DEFECT IN THIS DIRECTORY WAS ONE.  The rule is set")
    print("     MEMBERSHIP: a number printed ANYWHERE in a transcript of this directory")
    print("     backs the same number written ANYWHERE in its prose.  §4 said")
    print()
    stale17 = ("* **Killed at the limit.** 17 of 187 suites hit the 900 s cap. "
               "A process cut off mid-write")
    print("         %s" % stale17[:70])
    print()
    print("     where the record says 22 timed out, and THIS ARM DOES NOT FIRE ON IT:")
    print("         figures %s, none of them missing -> BACKED"
          % ", ".join(str(v) for v in L.figures(stale17)))
    print()
    print("     The 17 is backed, and by what is worth printing rather than paraphrasing")
    print("     -- a FOREIGN finding quoted inside this directory's own report:")
    for p in outs:
        found = False
        for i, line in enumerate(L.read(p, None).splitlines(), 1):
            if 17 in L.figures(line):
                print("         %s:%d  %s" % (os.path.basename(p), i, line.strip()[:56]))
                found = True
                break
        if found:
            break
    print()
    print("     It was found by reading the record, not by this check.  Role needs a")
    print("     per-figure anchor, an anchor is a hand-typed quotation of the prose,")
    print("     and it rots silently the moment anybody rewords the sentence -- which is")
    print("     why this arm is a membership test and says so instead of pretending.")
    print()
    print("  3  AN UNCLOSED FENCE MAKES THIS ARM QUIETER, NEVER LOUDER.  P4d measures")
    print("     it.  Nothing here validates the README's markdown.")
    print()
    print("  4  THE `.py` DOCSTRINGS ARE OUTSIDE THE POPULATION, BY CHOICE AND NOT BY")
    print("     OVERSIGHT.  A docstring is read beside the code it describes, so a")
    print("     figure in one is usually backed by the CODE (`truncated at column 78`")
    print("     beside `text[:78]`), and a rule demanding a transcript for it would")
    print("     report the code as unbacked by itself.  The README is read INSTEAD of")
    print("     the record, so its figures can only be backed by a transcript.  The")
    print("     cost is real: a stale figure in a docstring is invisible here.")
    print()

    # ------------------------------------------------------------------ verdict
    rc = 2 if bad else (1 if voice_bad else 0)
    print("=" * W)
    if bad:
        print("mg-2959 prose arm: *** %d CONTROL(S) DID NOT HOLD *** -- this arm's own"
              % bad)
        print("verdict is not evidence of anything until they do.  REFUSED.")
    elif voice_bad:
        print("mg-2959 prose arm: %d figure(s) this README states in its own voice that no"
              % len(voice_bad))
        print("transcript of this directory prints.  %d quoted, reported, not graded."
              % len(fence_bad))
    else:
        print("mg-2959 prose arm: every figure this README states in its own voice is")
        print("printed by one of this directory's own transcripts.  %d quoted figure(s)"
              % len(fence_bad))
        print("reported and NOT graded -- see P5.1, which is a hole and not a pass.")
    print("=" * W)
    return rc


if __name__ == "__main__":
    sys.exit(main())
