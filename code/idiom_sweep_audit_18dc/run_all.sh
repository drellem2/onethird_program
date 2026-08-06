#!/bin/sh
# mg-18dc -- the INDEPENDENT AUDIT of the arc-wide runner-idiom sweep.
#
# THIS RUNNER DOES NOT WRITE A TRANSCRIPT INTO THIS DIRECTORY UNTIL THE LAST
# PROBE HAS EXITED.  Every out_*.txt is built under $V18_WORK, which is a
# `mktemp -d` OUTSIDE THE REPOSITORY, and copied in at the end.  That is
# mg-ec63's structural repair (c1bb466) adopted rather than re-derived: a
# transcript inside the tree is a transcript this arc's own probes can empty
# while it is being written, and this suite runs 100+ of them.
#
# It is also why nothing here needs a `.new`+`mv`: there is no in-tree file to
# truncate at all.
#
# RE-ENTRANCY.  This suite executes other runners.  If one of them executes
# THIS one, the guard below stops it and NAMES THE CALLER -- mg-ec63 found the
# unnamed version of this exact collision (e0a7527).

set -u

if [ -n "${V18_RUNNING:-}" ]; then
  echo "mg-18dc/run_all.sh: REFUSING TO RE-ENTER."
  echo "  already running for: $V18_RUNNING"
  echo "  called from:         ${PWD}"
  exit 0
fi
V18_RUNNING="${PWD}"
export V18_RUNNING

HERE=$(cd "$(dirname "$0")" && pwd)
cd "$HERE" || exit 1

V18_WORK=${V18_WORK:-$(mktemp -d "${TMPDIR:-/tmp}/mg18dc.XXXXXX")}
export V18_WORK
mkdir -p "$V18_WORK"
echo "mg-18dc: work dir (OUTSIDE the repository) = $V18_WORK"

SUMMARY="$V18_WORK/SUMMARY.txt"
: > "$SUMMARY"

run() {
  _name=$1
  _script=$2
  echo "=== $_script"
  python3 -W ignore "$HERE/$_script" > "$V18_WORK/out_$_name.txt" 2>&1
  _rc=$?
  printf '%-22s exit %s\n' "$_name" "$_rc" >> "$SUMMARY"
  echo "    exit $_rc"
}

run selftest_18dc selftest18dc.py
run v1_population  v1_population.py
run v2_truncation  v2_truncation.py
run v3_bite        v3_bite.py
run v4_outcomes    v4_outcomes.py
run v5_convergence v5_convergence.py
run v6_elsewhere   v6_elsewhere.py
run v7_self        v7_self.py

# ONLY NOW does anything land in the tree.
for f in "$V18_WORK"/out_*.txt; do
  [ -f "$f" ] && cp "$f" "$HERE/$(basename "$f")"
done
cp "$SUMMARY" "$HERE/out_summary.txt"

echo
echo "=== SUMMARY"
cat "$SUMMARY"
