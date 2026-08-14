#!/usr/bin/env python3
"""mg-cd8d r1 — WHAT DOES `verdict_for` RETURN FOR A CENSUS READING TAKEN BEFORE THE REBASE?

pm-onethird put the question as a command rather than an argument, and this is the command.
Seven worlds, each two real commits of `main` with the REAL producer run over each archived
corpus and the REAL `lib_f771.verdict_for` asked about the pair.  `r0_selftest.py` holds the
harness to both directions first; read it before reading this.

THE ANSWER IS NOT `AGREES`, SO mg-05c6 IS NOT BLIND TO THE PRE-REBASE READING.  W1 and W2
differ, which is the whole of the ticket's step 1: a reading taken before the rebase is graded
by a different clause from one taken after it, and the difference is visible in the build log.

WHAT DOES NOT FOLLOW, AND IS THE PART WORTH CARRYING.  W1's grade is `CORPUS`, which is NOT in
`lib_f771.RED_VERDICTS` (r0 D4), and W3 shows it is the SAME grade the innocent branch gets —
the one that published nothing and whose committed copy is simply main's older reading.  The
instruction that goes with the grade is g0's `Restore it rather than committing it — the
refresh is owed by whoever trips the bound, not by this branch`, and in W3 that is right.  In
W1 the committed copy IS this branch's own pre-rebase reading, so restoring it keeps the figure
computed on a tree that is not the tree being merged, which is the thing the ticket's carry
forward asked an instrument to refuse.  `verdict_for(committed, worktree, relpath)` has no
argument for who wrote the committed copy (r0 D5), so no clause inside it can separate the two.

AND W6 IS THE SHARP END OF THAT.  Under mg-05c6 the standing instruction to every branch is
RESTORE, so the only branch that commits a census reading at all is the one whose gate went
STALE.  W4 is that branch, red at 11 directories of drift.  W6 hands the same branch a refresh
taken BEFORE its rebase — and the red clears to CORPUS.  The bound is discharged by a reading
that is not the merged tree's, which is the residue this arm reports.

EXITS 0 always: every line below is a measurement and none of it is a gate.  The gate on this
question is g0's, and it is g0's answer that is being reported.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_cd8d as L  # noqa: E402

W = 92


def rows(name):
    """The commits at or before AS_OF that touched `name`, as a set of hashes."""
    p = L._git("rev-list", L.AS_OF, "--", name)
    return set(p.stdout.decode().split())


def window(n):
    p = L._git("rev-list", "-n", str(n), L.AS_OF)
    return set(p.stdout.decode().split())


def count(*args):
    p = L._git("rev-list", "--count", *args)
    return int(p.stdout.decode().strip())


def main():
    print("=" * W)
    print("mg-cd8d — A CENSUS READING TAKEN BEFORE THE REBASE, GRADED BY THE REAL INSTRUMENT")
    print("=" * W)
    print()

    L.require_commits()

    pre, _ = L.reading(L.MAIN_BEFORE, extra_dirs=(L.BRANCH_DIR,))
    post, _ = L.reading(L.AS_OF, extra_dirs=(L.BRANCH_DIR,))
    far, _ = L.reading(L.MAIN_FAR, extra_dirs=(L.BRANCH_DIR,))
    main_only, _ = L.reading(L.MAIN_BEFORE)

    pop_pre, cpin_pre, ppin_pre = L.figures(pre)
    pop_post, cpin_post, ppin_post = L.figures(post)
    pop_far = L.figures(far)[0]
    pop_main = L.figures(main_only)[0]

    print("§0  THE WORLDS, AND WHAT IS REAL IN THEM")
    print("-" * W)
    print("  Each world is a COMMITTED reading and a WORKTREE reading.  The worktree side is")
    print("  always the reading the gate takes on the MERGED tree, because `./build.sh` runs")
    print("  after the refinery has rebased; the committed side is what the branch carried in.")
    print("  The corpus at each commit is the real one, `git archive`d; today's producer is")
    print("  overlaid on both sides so the PRODUCER pin cannot move (r0 D3); the only synthetic")
    print("  object is the simulated branch's own new directory, one file holding VALUE = 1.")
    print()
    print("  merge base        %s   population %d" % (L.MAIN_BEFORE, pop_main))
    print("  + the branch's own directory            population %d   <- the pre-rebase tree"
          % pop_pre)
    print("  merged tree       %s   population %d   <- the tree being merged"
          % (L.AS_OF, pop_post))
    print("  far behind        %s   population %d   <- %d directories of drift, bound %d"
          % (L.MAIN_FAR, pop_far, abs(pop_post - pop_far), L.F.CORPUS_DRIFT_LIMIT))
    print()
    print("  corpus pin  pre-rebase vs merged: %s        producer pin: %s"
          % (L.moved(cpin_pre, cpin_post), L.moved(ppin_pre, ppin_post)))
    print("  The digests themselves are NOT printed.  A corpus pin covers the content of every")
    print("  .py and .sh under code/, so a digest in this transcript would move whenever")
    print("  anybody edited anything — which is the defect this directory is about, one file")
    print("  over.  Populations are counts at fixed commits and cannot move.")
    print()

    tampered = post.replace("population: %d" % pop_post, "population: %d" % (pop_post + 700))

    worlds = [
        ("W1", "THE TICKET'S EVENT.  The branch took its reading on the PRE-REBASE tree and "
               "committed it; the refinery rebased onto a main that had gained %d directories."
               % (pop_post - pop_pre),
         L.verdict(pre, post), "CORPUS"),
        ("W2", "THE DISCIPLINE FOLLOWED.  The same branch takes the reading AFTER the rebase.  "
               "This world is why W1's answer means something: the two are distinguishable.",
         L.verdict(post, post), "AGREES"),
        ("W3", "THE INNOCENT BRANCH.  It published nothing; the committed copy is main's own "
               "older reading and the drift is somebody else's.  SAME GRADE AS W1.",
         L.verdict(main_only, post), "CORPUS"),
        ("W4", "THE BOUND.  A committed reading %d directories behind the merged tree, past "
               "the declared limit of %d." % (abs(pop_post - pop_far), L.F.CORPUS_DRIFT_LIMIT),
         L.verdict(far, post), "STALE"),
        ("W5", "THE FENCE.  The merged tree's own reading with one figure tampered, so the "
               "pin is UNCHANGED beside a text that moved: the instrument changed its answer "
               "on an unchanged corpus.",
         L.verdict(tampered, post), "DISAGREES"),
        ("W6", "THE STALE REFRESH.  W4's branch is told to refresh and refreshes with a "
               "PRE-REBASE reading.  The red clears.",
         L.verdict(pre, post), "CORPUS"),
        ("W7", "THE EXEMPTION IS A DECLARED LIST AND NOT A SHAPE.  W1's two texts at a path "
               "that is not in CORPUS_SCOPED.",
         L.verdict(pre, post, "code/somewhere_else/out_reading.txt"), "DISAGREES"),
    ]

    print("§1  THE VERDICTS")
    print("-" * W)
    agreed = True
    for tag, text, got, expected in worlds:
        mark = "as scoped" if got == expected else "NOT AS SCOPED"
        print("  %s  %-9s  (%s)" % (tag, got, mark))
        for line in _wrap(text, W - 6):
            print("      %s" % line)
        print()
        agreed = agreed and got == expected
    if not agreed:
        print("  AT LEAST ONE VERDICT IS NOT THE ONE THIS ARM WAS WRITTEN AGAINST.  The prose")
        print("  in §2 was written from the run above and must be re-read against it before it")
        print("  is quoted; a paragraph is not a measurement.")
        print()

    print("§2  WHAT THE ANSWER IS, AND WHAT IT LEAVES")
    print("-" * W)
    print("  STEP 1'S ANSWER IS `%s`, WHICH IS NOT `AGREES`." % worlds[0][2])
    print("  So the after-the-rebase rule is already an INSTRUMENT and not only a discipline:")
    print("  mg-05c6's pin sees the pre-rebase reading, and W2 shows it grades the same branch")
    print("  differently when the reading is taken after the rebase.  The ticket's carry")
    print("  forward — `refuse to emit a figure computed on a tree that is not the tree being")
    print("  merged` — is DETECTED at gate time by a mechanism that already shipped.")
    print()
    print("  R1  IT IS DETECTED AND NOT REFUSED, AND THE GRADE IS SHARED WITH THE INNOCENT")
    print("      CASE.  CORPUS is not in RED_VERDICTS (r0 D4), and W1 and W3 are the same word")
    print("      in the same build log beside the same instruction: restore, the refresh is")
    print("      somebody else's.  In W3 that is correct.  In W1 the committed copy is this")
    print("      branch's own pre-rebase reading, and restoring keeps it.  Nothing inside")
    print("      verdict_for can separate them — it is handed two texts and a path, and who")
    print("      WROTE the committed copy is not among its arguments (r0 D5).  What could")
    print("      separate them is outside it: whether THIS BRANCH modified the file, which is")
    print("      a question about the diff against the merge base and not about HEAD.")
    print()
    print("  R2  THE BOUND IS DISCHARGED BY A READING THAT NEED NOT BE THE MERGED TREE'S.")
    print("      W4 -> W6 is the whole of it: the one branch that mg-05c6 does ask for a")
    print("      census is the branch whose gate went STALE, and a pre-rebase refresh clears")
    print("      that red as surely as a correct one.  The figure that lands is then wrong for")
    print("      the tree it lands in, which is the defect mg-f771 exists to find, arriving")
    print("      through the exemption mg-05c6 added to it.")
    print("      AND IT BUYS PARTIAL CREDIT, WHICH IS ARITHMETIC RATHER THAN A WORRY.  The")
    print("      drift that decides the next STALE is measured against the COMMITTED figure,")
    print("      so on these worlds' own numbers: %d directories before any refresh, %d after"
          % (abs(pop_post - pop_far), abs(pop_post - pop_pre)))
    print("      a PRE-rebase refresh, %d after a post-rebase one.  A wrong refresh does not"
          % 0)
    print("      only clear the red; it postpones the next honest reading by the distance it")
    print("      happens to be right about.")
    print()

    print("§3  HOW OFTEN THIS CAN HAPPEN, MEASURED ON THE RECORD AND PINNED AT %s" % L.AS_OF)
    print("-" * W)
    touched = rows(L.CENSUS)
    since = count("%s..%s" % (L.PIN_05C6, L.AS_OF))
    since_touched = len(touched & set(
        L._git("rev-list", "%s..%s" % (L.PIN_05C6, L.AS_OF)).stdout.decode().split()))
    last200 = len(touched & window(200))
    print("  commits on main since mg-05c6 landed (%s..%s)  : %3d"
          % (L.PIN_05C6, L.AS_OF, since))
    print("  of those, commits that touched the census           : %3d" % since_touched)
    print("  of the 200 commits at %s, commits touching it  : %3d" % (L.AS_OF, last200))
    print("  COUNTED AS AN INTERSECTION and not as `git log -200 -- <path>`, which limits to")
    print("  200 MATCHING commits and answers a different question; taking it the loose way")
    print("  during scoping returned %d." % len(touched))
    print()
    committed = L._git("show", "%s:%s" % (L.AS_OF, L.CENSUS)).stdout.decode("utf-8", "replace")
    pop_committed = L.figures(committed)[0]
    tree_only, _ = L.reading(L.AS_OF)
    pop_tree = L.figures(tree_only)[0]
    drift = abs(pop_tree - pop_committed)
    print("  the census as COMMITTED at %s says population       : %3s"
          % (L.AS_OF, pop_committed))
    print("  the tree at %s actually holds                       : %3s"
          % (L.AS_OF, pop_tree))
    print("  so the live drift is %d of a bound of %d, headroom %d directories"
          % (drift, L.F.CORPUS_DRIFT_LIMIT, L.F.CORPUS_DRIFT_LIMIT - drift))
    print()
    print("  THESE ARE THIS ARM'S OWN NUMBERS AND NOT mg-05c6's.  mg-05c6 priced its bound at")
    print("  34 refreshes over 200 commits becoming 6; the %d above is re-derived at a later"
          % last200)
    print("  AS_OF and is a different window, so it neither confirms nor contradicts that.")
    print("  WHAT IT DOES SAY IS THE STRONGER HALF: %d of the %d commits since the pin landed"
          % (since_touched, since))
    print("  have carried a census at all, because the bound has not been tripped yet.  So the")
    print("  population of branches exposed to R1 and R2 today is small, and the hazard is")
    print("  unchanged per occurrence — an argument about scheduling, which is pm-onethird's")
    print("  own reading of the 82% figure and is repeated here rather than re-decided.")
    print()

    print("=" * W)
    print("MEASURED — step 1 answers %s.  The carry forward is discharged as a DETECTOR; R1"
          % worlds[0][2])
    print("and R2 are what is left, and they are the successor's, not this arm's to build.")
    print("=" * W)
    return 0


def _wrap(text, width):
    out, line = [], ""
    for word in text.split():
        if line and len(line) + 1 + len(word) > width:
            out.append(line)
            line = word
        else:
            line = ("%s %s" % (line, word)).strip()
    out.append(line)
    return out


if __name__ == "__main__":
    try:
        sys.exit(main())
    except L.Refused as exc:
        sys.stderr.write("mg-cd8d r1: REFUSED — %s\n" % exc)
        sys.exit(2)
