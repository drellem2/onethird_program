#!/bin/sh
# run_all.sh -- mg-f8e5, the DISPOSAL of mg-1abe's remainder.
#
#     sh run_all.sh                 # as of `main`
#     sh run_all.sh --at <rev>      # the same, as of any commit
#
# Pure Python 3 + git.  No third-party packages, no network.
#
# ⚠️ THE REVISION IS RESOLVED ONCE, HERE, AND PASSED TO EVERY SCRIPT.
#
# This is mg-1abe's own fix (a7d7fb9) and it is copied deliberately rather than
# re-derived, because `d4_movingref.py` sweeps the whole arc for suites that do
# NOT do this and it must not be one of them.  Without it each script resolves
# `main` at its own start time, and on a repository other agents are merging
# into, `main` MOVES BETWEEN THEM: in mg-1abe's own first full run t1 measured
# 537 transcripts at `eacc5e1` while t2 started at `81214a9`.
#
# Pass `--at <rev>` yourself to override.  Passing the `as-of` printed in a
# committed transcript is how you re-run this suite against the revision that
# transcript is a fact about.
#
# ⚠️ COST, and it is UNEVEN.
#
#   selftest  ~1 min      d5  ~1 min      d3  ~3 min      d4  ~2 min
#   d2        ~10-30 min  -- it EXECUTES 31 recovered producers at 31 commits
#   d1        ~30-45 min  -- ONE of its five producers (hodge_leverage_repair_
#                            ff3e) writes into three documents, runs a gate as
#                            a subprocess per probe and re-runs four other
#                            instruments.  It takes over TWENTY MINUTES on its
#                            own, and that is the entire point of `d5`.
#
# `--timeout S` moves the producer budget and `--armb-budget S` moves the point
# at which d1 stops asking "which revision is this a fact about".  BOTH ARE
# BUDGETS AND NEITHER IS A VERDICT: a producer that exceeds one is reported in
# its own bucket and is NEVER counted as failing to reproduce.  That rule is
# mg-1abe's, from its §2, and `out_d5_timeout.txt` is the measurement of what
# happens when an instrument states it and does not implement it.
#
# ⚠️ WRITES ONLY ITS OWN `out_*.txt`.  Every re-run happens in a throwaway
# detached worktree under the system temp directory, which is removed and
# pruned.  Nothing here touches this working tree and nothing moves a ref.
#
# ORDER MATTERS FOR ONE ROW.  `d3_adopt.py` checks that the transcripts of THIS
# directory declare THIS directory's digest, and it can only see the ones
# already written -- mg-1abe's defect 6.  It is run LAST so that set is as
# large as it can be, and its own transcript is still outside it.  That is
# stated in the row rather than hidden by it.
#
# EXIT-CODE CONVENTION, taken from mg-1abe, which took it from code/repair_b2af:
# every script exits 0 iff SELF-ERRORS == 0 AND FINDINGS == 0.  A non-zero exit
# means THAT SCRIPT HAS SOMETHING TO REPORT, never that it is broken.
#
# EXPECTED non-zero, with the reason held in advance by PREDICTIONS.md:
#   d5  the census's TIMED-OUT bucket is unreachable, and one of the five is a
#       casualty of it
#   d1  four of the five are disposed of as damage
#   d2  not all 31 can be made measurable
#   d3  coverage of the convention is 8 of 812 and UNDECLARED is a finding
#   d4  the moving-ref shape survives in other suites
#
# NO `set -e`: those exits are RESULTS.  NO PIPE (mg-c2b3): each script
# REDIRECTS and `$?` is read on the next line, because a pipeline's status in
# POSIX sh is the last command's -- which is how a transcript recording a
# refutation once came to be committed beside an exit 0.

cd "$(dirname "$0")" || exit 2

case " $* " in
    *" --at "*) AT="" ;;
    *)          AT="--at $(git rev-parse main)" ;;
esac

WORST=0
for s in selftest_f8e5 d5_timeout d1_five d2_unmeasured d4_movingref d3_adopt; do
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
