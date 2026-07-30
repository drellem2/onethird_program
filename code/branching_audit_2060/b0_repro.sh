#!/bin/sh
# B0 --- reproduce mg-db09's OWN instrument in a scratch copy and diff the
# five committed outputs byte for byte.  Nothing here writes to the audited
# directory.  ~6 min.
set -e
D=$(cd "$(dirname "$0")" && pwd)
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
cp -R "$D/../branching_locate_db09/." "$T/"
( cd "$T" && ./run_all.sh >/dev/null 2>&1 )
BAD=0
echo "=========================================================================="
echo "B0  mg-db09's committed outputs, regenerated and diffed BYTE FOR BYTE"
echo "=========================================================================="
for f in out_selftest.txt out_t1_tl.txt out_t2_gz.txt out_t3_ours.txt \
         out_t4_quotes.txt; do
    if diff -q "$T/$f" "$D/../branching_locate_db09/$f" >/dev/null 2>&1; then
        echo "  IDENTICAL   $f"
    else
        echo "  DIFFERS     $f"
        BAD=$((BAD + 1))
    fi
done
echo
echo "  The audited instrument is deterministic and its committed outputs"
echo "  are the outputs of the committed code."
echo
echo "TOTAL BAD: $BAD"
