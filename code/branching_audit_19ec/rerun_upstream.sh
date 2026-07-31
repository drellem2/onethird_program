#!/bin/sh
# mg-19ec -- "do not disturb what stands": the five earlier suites re-run on a
# clean tree, with every exit code predicted before the run.
#
# Slow (about ten minutes; branching_af28 reaches n = 8).  Separated from
# run_all.sh for that reason, and because it REGENERATES committed outputs in
# directories this audit does not own.  It classifies every difference and then
# RESTORES those directories with `git checkout --`, so the audit's own branch
# carries none of them.
#
# Exit status is the number of exit-code misses, as in run_all.sh.
set -u
cd "$(dirname "$0")"
ROOT=$(cd ../.. && pwd)
OUT=out_upstream.txt
MISSES=0

{
  echo "=============================================================================="
  echo "mg-19ec: the five earlier suites, re-run.  Exit codes predicted BEFORE"
  echo "the run, in PREDICTIONS.md section 1b (committed at 170094f)."
  echo "=============================================================================="
  echo
} > "$OUT"

run() {                          # run <predicted> <dir> <command...>
    want="$1"; dir="$2"; shift 2
    ( cd "$ROOT/$dir" && "$@" ) > /tmp/mg19ec_up.log 2>&1
    got=$?
    if [ "$got" -eq "$want" ]; then verdict=ok; else verdict=MISS; MISSES=$((MISSES+1)); fi
    printf '  %-34s predicted %s  got %s  %s\n' "$dir" "$want" "$got" "$verdict" >> "$OUT"
    tail -3 /tmp/mg19ec_up.log | sed 's/^/        /' >> "$OUT"
    echo >> "$OUT"
}

run 0 code/branching_warrant_dffa ./run_all.sh
run 0 code/branching_repair_41aa  python3 check_doc.py
run 0 code/branching_audit_5800   ./run_all.sh
run 0 code/branching_repair_41aa  ./run_all.sh
run 0 code/branching_audit_6ad0   ./run_all.sh
run 0 code/branching_af28         ./run_all.sh

{
  echo "=============================================================================="
  echo "WHICH COMMITTED OUTPUTS MOVED, AND WHY"
  echo "=============================================================================="
  echo
  echo "  A regenerated output that differs is not automatically a break.  Each"
  echo "  file below is normalised -- elapsed times '(12.3s)' and 'line NNN'"
  echo "  replaced by placeholders -- and re-compared.  A file that is identical"
  echo "  after that carries no moved FIGURE."
  echo
} >> "$OUT"

cd "$ROOT"
git diff --name-only -- code/branching_af28 code/branching_audit_6ad0 \
    code/branching_audit_5800 code/branching_repair_41aa \
    code/branching_warrant_dffa > /tmp/mg19ec_moved.txt

if [ ! -s /tmp/mg19ec_moved.txt ]; then
    echo "  no committed output moved at all." >> "$OUT"
else
    while IFS= read -r f; do
        git show "HEAD:$f" | sed -E 's/\([0-9]+\.[0-9]+s\)/(Ns)/g; s/line [0-9]+/line N/g' \
            > /tmp/mg19ec_a.txt
        sed -E 's/\([0-9]+\.[0-9]+s\)/(Ns)/g; s/line [0-9]+/line N/g' "$f" \
            > /tmp/mg19ec_b.txt
        if cmp -s /tmp/mg19ec_a.txt /tmp/mg19ec_b.txt; then
            printf '  %-46s TIMINGS / LINE NUMBERS ONLY\n' "$f" >> "$OUT"
        else
            printf '  %-46s CONTENT MOVED:\n' "$f" >> "$OUT"
            diff /tmp/mg19ec_a.txt /tmp/mg19ec_b.txt | head -20 | sed 's/^/        /' >> "$OUT"
        fi
    done < /tmp/mg19ec_moved.txt
fi

{
  echo
  echo "  RESTORING those directories now, so this audit's branch carries no"
  echo "  regenerated output of a directory it does not own."
} >> "$OUT"
git checkout -- code/branching_af28 code/branching_audit_6ad0 \
    code/branching_audit_5800 code/branching_repair_41aa \
    code/branching_warrant_dffa 2>/dev/null
{
  printf '  git status over those five directories after restore: '
  if [ -z "$(git status --porcelain -- code/branching_af28 \
      code/branching_audit_6ad0 code/branching_audit_5800 \
      code/branching_repair_41aa code/branching_warrant_dffa)" ]; then
      echo "CLEAN"
  else
      echo "NOT CLEAN"
  fi
  echo
  echo "=============================================================================="
  if [ "$MISSES" -eq 0 ]; then
      echo "SUMMARY upstream: 6 of 6 exit codes matched their prediction."
  else
      echo "SUMMARY upstream: $MISSES exit code(s) MISSED."
  fi
  echo "=============================================================================="
} >> "$OUT"

cat "$OUT"
exit "$MISSES"
