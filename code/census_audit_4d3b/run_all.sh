#!/bin/sh
# mg-4d3b: the INDEPENDENT AUDIT of mg-f3ff's census repair.
#
#     sh run_all.sh          # ~3 min; a3 and a4 clone repos and dominate
#
# Pure Python 3 + git, no third-party packages.
#
# ⚠️ THIS RUNNER FETCHES, and it clones.  Every section calls `git fetch origin`
# and derives against `origin/main`, because that is mg-f3ff's addendum and
# because a census run against a stale checkout returns the same wrong answer
# with the authority of having read the tree.  It does NOT check out, pull,
# stash, or otherwise touch either working tree.  Repo 1 is reached through
# THIS WORKTREE, which shares `.git` with /Users/daniel/research/onethird_program
# -- a0 asserts the two resolve `origin/main` to the same sha -- so no command
# here runs inside a directory holding another agent's uncommitted state.
#
# ⚠️ EVERY CLONE THIS SUITE MAKES IS THROWAWAY, under $MG4D3B_SCRATCH (default:
# a mkdtemp).  a3 breaks remotes and a4 writes commits; both do so ONLY inside
# those clones.
#
# ⚠️ THE RUNNER REPORTS THE INSTRUMENT'S STATUS, NOT `tee`'s.  Under a pipeline
# the exit status is the LAST command's, which is how a transcript recording a
# refutation once came to be committed beside an exit 0 (mg-c2b3).  Each script
# redirects; the status is captured; the transcript is then `cat`.
#
# EXIT: 0 if no control of THIS AUDIT failed.  ⚠️ FINDINGS ABOUT mg-f3ff DO NOT
# SET IT.  a3 reports five, a4 two and a5 three, and this still exits 0: an
# auditor that exited 1 for successfully finding what it was sent to find could
# not distinguish `the subject has a defect` from `the auditor is broken`, and
# those need different responses.
cd "$(dirname "$0")"

echo "== mg-4d3b: the INDEPENDENT AUDIT of mg-f3ff's census repair =="
status=0
for s in selftest4d3b a0_which_tree a1_rows a2_landing a3_fetchfail \
         a4_move a5_selfdefect; do
    # stderr goes INTO the transcript: a crash and a fired check are both
    # exit 1, and a transcript keeping only stdout ends mid-section with no
    # reason given.
    python3 "$s.py" "$@" > "out_$s.txt" 2>&1 || status=$?
    cat "out_$s.txt"
done

echo
echo "== mg-4d3b aggregate exit: $status =="
exit "$status"
