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
run() {   # run <name> <expected-exit> <script...>
    local name="$1" want="$2"; shift 2
    printf '\n=== %s (expecting exit %s)\n' "$name" "$want"
    python3 -u "$@" > "$WORK/out_$name.txt" 2>&1
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
