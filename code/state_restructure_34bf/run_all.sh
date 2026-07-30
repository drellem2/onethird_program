#!/usr/bin/env bash
# mg-34bf: rebuild the STATE.md ledger restructure from the base commit, then check it.
# Runtime ~3 s, no dataset, no enumeration.
set -euo pipefail
cd "$(dirname "$0")/../.."
BASE="${1:-60f4dac0be109513c75ba6985694ec1a0eb4e8d3}"

echo "=== 1. verify nothing was lost (independent of the builder) ==="
python3 code/state_restructure_34bf/verify_relocation.py "$BASE"

echo
echo "=== 2. verify the three A3 sites read in sequence in under a minute ==="
python3 code/state_restructure_34bf/a3_reading_path.py

echo
echo "=== 3. rebuild from the base commit and confirm it reproduces the committed file ==="
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
git show "$BASE:STATE.md" > "$tmp/STATE.md"
cp STATE.md "$tmp/STATE.committed.md"
git show "$BASE:STATE.md" > STATE.md
python3 code/state_restructure_34bf/build.py > "$tmp/build.log"
if diff -q STATE.md "$tmp/STATE.committed.md" >/dev/null; then
  echo "OK    the builder reproduces the committed STATE.md byte-identically"
  cat "$tmp/build.log"
else
  cp "$tmp/STATE.committed.md" STATE.md
  echo "FAIL  the builder does not reproduce the committed STATE.md"; exit 1
fi
