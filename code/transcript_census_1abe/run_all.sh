#!/bin/sh
# run_all.sh -- the mg-1abe transcript-reproduction census.
#
#     sh run_all.sh                 # the census as of `main`
#     sh run_all.sh --at <rev>      # the same census as of any commit
#
# Pure Python 3 + git.  No third-party packages, no network.
#
# ⚠️ COST.  t2 re-runs 157 suites at 157 different commits in parallel
# worktrees, and re-runs every suite that produced a differing transcript a
# SECOND time to test the producer for nondeterminism.  It takes ROUGHLY TWO
# HOURS on a ten-core machine.  `--jobs N` and `--timeout S` move both ends of
# that; a producer that exceeds the timeout is reported in its own bucket and
# is NEVER counted as failing to reproduce.  Everything else here is under two
# minutes.
#
# EXIT-CODE CONVENTION, taken from code/repair_b2af/run_all.sh so the ruler is
# somebody else's: every script exits 0 iff SELF-ERRORS == 0 AND FINDINGS == 0.
# A non-zero exit means THAT SCRIPT HAS SOMETHING TO REPORT, never that it is
# broken, and the two counts are printed separately because "I found what I was
# sent to find" and "I am broken" need different responses.
#
# EXPECTED non-zero, and PREDICTIONS.md holds the reasons in advance:
#   t2  the blast radius is not zero
#   t3  recorded shas exist that are not on main
#   t5  the retroactive screen is deliberately kept RED as a failed idea
#   t6  a live instance of the cap shape survives
#
# NO `set -e`: those exits are RESULTS.  A runner that stopped at the first one
# would run selftest and nothing else.
#
# NO PIPE (mg-c2b3): each script REDIRECTS and `$?` is read on the next line.
# A pipeline's status in POSIX sh is the last command's, which is how a
# transcript recording a refutation once came to be committed beside an exit 0.
#
# ⚠️ WRITES ONLY ITS OWN `out_*.txt`.  t2 checks commits out in throwaway
# worktrees under the system temp directory, removes them, and prunes.  It
# never touches this working tree and never moves a ref.

cd "$(dirname "$0")" || exit 2

# ⚠️ THE REVISION IS RESOLVED ONCE, HERE, AND PASSED TO EVERY SCRIPT.
#
# Without this each script resolves `main` at its own start time, and on a
# repository with other agents merging into it `main` MOVES BETWEEN THEM.  It
# did, in this suite's own first full run: t1 measured a population of 537 as
# of `eacc5e1` and by the time t2 started `main` was `81214a9`.  A census whose
# own scripts disagree about their denominator is not a census, and it would
# have been committing the defect it was filed to measure.
#
# Pass `--at <rev>` yourself to override -- and passing the `as-of` printed in
# a committed transcript is how you re-run this suite against the revision that
# transcript is a fact about.
case " $* " in
    *" --at "*) AT="" ;;
    *)          AT="--at $(git rev-parse main)" ;;
esac

WORST=0
for s in selftest_1abe t1_population t2_census t3_shas t4_rebase t7_sightings \
         t5_control t6_caps; do
    printf '===> %s\n' "$s"
    # shellcheck disable=SC2086  # $AT is two words on purpose
    python3 -W ignore "$s.py" $AT "$@" > "out_$s.txt" 2>&1
    RC=$?
    printf '     exit %d   %s\n' "$RC" \
        "$(grep '^TOTAL BAD:' "out_$s.txt" 2>/dev/null | tail -1)"
    [ "$RC" -gt "$WORST" ] && WORST=$RC
done

printf 'worst exit: %d\n' "$WORST"
exit "$WORST"
