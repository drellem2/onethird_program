#!/bin/sh
# mg-54b1 -- THE EXPENSIVE ARM.  Re-run instruments in the blind spot and keep
# the diff each one produces, so `classify.py` can ask whether a VERDICT moved
# rather than only whether a BYTE did.
#
# COST AND SIDE EFFECTS, STATED, because this is not a cheap check and because
# mg-20ee's ground_truth.sh states the same and was right to.  It EXECUTES
# every instrument in the sample.  A sample of 40 took 42 minutes on the host
# that produced out_sweep_54b1.txt.
#
# IT RUNS IN A CLONE AND NEVER IN YOUR WORKTREE, which is the one way it
# differs from ground_truth.sh.  These instruments mutate the tree; several
# mutate directories OTHER than their own and restore them; and one killed by
# the timeout is killed MID-PROBE, with somebody else's file half-written.
# `git checkout -- .` in the tree you are working in is not a restore, it is a
# loss.  So:
#
#     git clone --no-hardlinks . /tmp/sweep54b1
#     sh code/verdict_staleness_census_54b1/sweep_54b1.sh /tmp/sweep54b1 /tmp/sweepout 40 120
#     python3 code/verdict_staleness_census_54b1/classify.py /tmp/sweepout
#
# TIMEOUT IS A REPORTED CLASS AND NOT A DROP.  An instrument the sweep could
# not finish inside its budget appears as TIMEOUT with its budget printed, and
# `classify.py` counts it as unmeasured rather than as reproducing.  Silently
# skipping it would read as coverage.
set -u
REPO="$1"; OUTDIR="$2"; N="${3:-40}"; TMO="${4:-120}"
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$OUTDIR/diffs"
python3 -B "$HERE/c1_population.py" --sample "$N" > "$OUTDIR/sample.txt" || exit 1
cd "$REPO" || exit 1
: > "$OUTDIR/sweep.tsv"
i=0
total=$(grep -c . "$OUTDIR/sample.txt")
while IFS= read -r d; do
  [ -n "$d" ] || continue
  i=$((i+1))
  slug=$(echo "$d" | tr '/' '_')
  start=$(date +%s)
  timeout -s KILL "$TMO" sh "$d/run_all.sh" >/dev/null 2>&1
  rc=$?
  end=$(date +%s)
  git diff > "$OUTDIR/diffs/$slug.diff" 2>/dev/null
  changed=$(git diff --name-only | tr '\n' ',')
  untracked=$(git ls-files --others --exclude-standard | tr '\n' ',')
  n=$(git diff --numstat | awk '{a+=$1;b+=$2} END{printf "%d+/%d-", a, b}')
  if [ -z "$changed" ]; then cls=REPRODUCES; else cls=DIFFERS; fi
  [ "$rc" = "137" ] && cls=TIMEOUT
  # LOAD IS RECORDED BECAUSE A TIMEOUT IS NOT A PROPERTY OF THE INSTRUMENT.
  # The run that produced out_sweep_54b1.txt shared a 10-core host whose load
  # average was measured by hand at 16 when it started and 60 an hour later,
  # and an instrument that needs 60 s idle can miss a 120 s budget at that
  # load.  Without this column a reader cannot tell a slow instrument from a
  # busy host, and the first run of this sweep could not tell them apart.
  load=$(uptime | sed 's/.*averages*: *//' | awk '{print $1}' | tr -d ',')
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$d" "$cls" "$rc" "$((end-start))" "$n" "$changed" "$untracked" "$load" \
    >> "$OUTDIR/sweep.tsv"
  echo "[$i/$total] $d $cls rc=$rc $((end-start))s $n" >> "$OUTDIR/progress.log"
  git checkout -q -- . 2>/dev/null
  git clean -fdqx -e '.git' 2>/dev/null
done < "$OUTDIR/sample.txt"
echo "SWEEP DONE $i/$total" >> "$OUTDIR/progress.log"
