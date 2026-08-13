#!/bin/sh
# mg-20ee — the census, its controls, and the pointer to the ground truth.
#
# ground_truth.sh is NOT run here.  It takes ~70 minutes, executes every
# candidate instrument, and writes-then-restores directories under code/ —
# none of which belongs on a build path.  out_ground_truth.txt records one
# dated run; re-run it by hand.
set -e
cd "$(dirname "$0")"
python3 selftest_20ee.py > out_selftest_20ee.txt
python3 census.py        > out_census.txt
echo "mg-20ee census: $(sed -n '/transcripts carry/p' out_census.txt | tr -s ' ')"
