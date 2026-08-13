#!/bin/sh
# mg-20ee -- THE CORRECTION TO census.py, AND THE NUMBER TO QUOTE.
#
# census.py is a NET: it finds transcripts that carry a computed foreign address,
# and it over-counts twice by construction (see its docstring).  This script is
# the ground truth it cannot reach: for each candidate instrument it RE-RUNS the
# suite and reports whether the committed transcripts still reproduce.  An
# instrument that reproduces is not stale, whatever the classifier thought.
#
# COST AND SIDE EFFECTS, STATED because this is not a cheap check.  It takes
# roughly 70 minutes over the full candidate list, it EXECUTES instrument code,
# and it WRITES then RESTORES each directory with `git checkout`/`git clean`.
# Do not run it on a tree with uncommitted work in code/.
#
# It is NOT a fixed point and does not claim to be: its answers change as the
# corpus moves, which is the very property being measured.  out_ground_truth.txt
# records one dated run.
#
# Usage:  sh ground_truth.sh <instrument-dir>...
set -u
REPO=$(git rev-parse --show-toplevel)
cd "$REPO" || exit 1
OUT=${GROUND_TRUTH_OUT:-/dev/stdout}
: > "$OUT"
for d in "$@"; do
  if [ ! -f "$d/run_all.sh" ]; then echo "$d NO_RUN_ALL" >> "$OUT"; continue; fi
  ( sh "$d/run_all.sh" ) >/dev/null 2>&1
  rc=$?
  changed=$(git -C "$REPO" diff --name-only -- "$d" | tr '\n' ' ')
  if [ -z "$changed" ]; then
    echo "$d REPRODUCES rc=$rc" >> "$OUT"
  else
    n=$(git -C "$REPO" diff --numstat -- "$d" | awk '{a+=$1;b+=$2} END{print a"+/"b"-"}')
    echo "$d DIFFERS rc=$rc lines=$n files=$changed" >> "$OUT"
  fi
  git -C "$REPO" checkout -- "$d" 2>/dev/null
  git -C "$REPO" clean -fdq -- "$d" 2>/dev/null
done
