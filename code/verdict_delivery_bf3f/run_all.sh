#!/usr/bin/env bash
# mg-bf3f -- the verdict-delivery suite.
#
# Transcripts are written OUTSIDE the repository and moved in only after the
# last probe exits. That is not fastidiousness: mg-ec63 recorded that this arc's
# own probes execute any run_all.sh they find on disk, and that two runners
# sharing a directory share their out_*.txt paths -- which produced a ZERO-BYTE
# transcript beside a non-zero exit and a summary with the row simply missing.
# A transcript being written IS a dirty tree, and a suite that writes into its
# own subject makes its subject fail (mg-40e4).
#
# Exit codes are DECLARED, not discovered. verdictwatch is expected to exit 1:
# it is a detector for a live defect, and today the defect is live.
set -u -o pipefail

if [ -n "${BF3F_RUNNING:-}" ]; then
    echo "REFUSING: BF3F_RUNNING is already set (inherited from pid ${BF3F_RUNNING})."
    echo "This runner is being executed from inside another run of itself, which is"
    echo "how mg-ec63's transcript got emptied. Naming the caller instead of retrying."
    exit 3
fi
export BF3F_RUNNING=$$

cd "$(dirname "$0")" || exit 4
WORK="$(mktemp -d "${TMPDIR:-/tmp}/bf3f-run-XXXXXX")"
trap 'rm -rf "$WORK"' EXIT

fail=0

# THE FOUR PROBES THAT READ THE LIVE STORE, NAMED HERE AND NOWHERE ELSE (mg-5491).
# d1_population and selftest_bf3f are NOT in this list: they are functions of this tree
# and they reproduce, which is why the list is a list and not "everything here".
LIVE_PROBES=" d2_cause d3_fire d4_live verdictwatch "

# The declaration a live-reading probe's transcript carries, emitted by the RUNNER and not
# by the probe.  verdictwatch.py is a shipped CLI whose stdout is a contract -- its --json
# mode must stay NDJSON -- so a banner printed from inside it would be a defect.  The runner
# knows which probes read the store; the probes do not need to.
declaration() {
    cat <<'DECL'
# =============================================================================
# NOT-A-FIXED-POINT: it reads the live mg store, which is outside this repository
# and moves every hour, so no commit can make the figures below reproduce.
# =============================================================================
# A re-run is a NEW measurement of a different afternoon and not a check of this
# one.  The figures below are DATED EVIDENCE for the finding this directory's
# README states -- the 122, the 25, the 16 of 191 -- so they are pinned:
# re-running this suite replaces them.  The marker above is the literal
# code/verdict_staleness_30bd reads (lib30bd.DECLARATION), which was grading
# these four probes as stale verdicts about the corpus.  Written by run_all.sh,
# not by the probe, because verdictwatch.py is a shipped CLI whose stdout is a
# contract -- its --json mode must stay NDJSON.  mg-5491.
DECL
}

run() {   # run <name> <expected-exit> <script...>
    local name="$1" want="$2"; shift 2
    printf '\n=== %s (expecting exit %s)\n' "$name" "$want"
    case "$LIVE_PROBES" in
        *" $name "*) declaration > "$WORK/out_$name.txt" ;;
        *)           : > "$WORK/out_$name.txt" ;;
    esac
    python3 -u "$@" >> "$WORK/out_$name.txt" 2>&1
    local got=$?
    printf '    exit %s' "$got"
    if [ "$got" = "$want" ]; then
        printf '  OK\n'
    else
        printf '  *** MISSED ITS DECLARED EXIT (%s) ***\n' "$want"
        fail=1
    fi
    printf '%s\n' "$name exit=$got expected=$want" >> "$WORK/SUMMARY.txt"
}

: > "$WORK/SUMMARY.txt"
run selftest_bf3f  0 selftest_bf3f.py
run d1_population  0 d1_population.py
run d2_cause       0 d2_cause.py
run d3_fire        0 d3_fire.py
run d4_live        0 d4_live.py
run verdictwatch   1 verdictwatch.py --filer pm-onethird

printf '\n=== SUMMARY\n'
cat "$WORK/SUMMARY.txt"

# Only now, with every probe exited, do the transcripts enter the tree.
cp "$WORK"/out_*.txt "$WORK/SUMMARY.txt" . || exit 5
printf '\nTranscripts moved into the tree. suite fail=%s\n' "$fail"
exit "$fail"
