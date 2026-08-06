#!/usr/bin/env bash
# mg-ea0e: verify the three-move STATE.md relocation.
#
# The BUILDER (build.py) is idempotent only against the pre-relocation tree, so it is NOT
# run here -- re-running it on an already-relocated STATE.md would append a second copy of
# each cell.  What this script runs is the CHECK, which is what a reader of the transcript
# needs: it reads STATE.md at the base commit out of git and the whole reachable corpus off
# disk, and re-derives the byte accounting, the mg-id population and the marker census from
# scratch every time.
#
# Usage:  bash code/state_restructure_ea0e/run_all.sh [BASE]
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"

BASE="${1:-78ae4d9}"
OUT="code/state_restructure_ea0e/out_verify_relocation_ea0e.txt"

echo "== mg-ea0e verification, base ${BASE}, HEAD $(git rev-parse --short HEAD) =="
python3 code/state_restructure_ea0e/verify_relocation_ea0e.py "${BASE}" 2>&1 | tee "${OUT}"
rc=${PIPESTATUS[0]}
echo "exit ${rc}" | tee -a "${OUT}"
exit "${rc}"
