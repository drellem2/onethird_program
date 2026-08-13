#!/bin/sh
# mg-20ee — the census, its controls, and the pointer to the ground truth.
#
# ground_truth.sh is NOT run here.  It takes ~70 minutes, executes every
# candidate instrument, and writes-then-restores directories under code/ —
# none of which belongs on a build path.  out_ground_truth.txt records one
# dated run; re-run it by hand.
#
# mg-6e4f: consumers.py IS run here.  It is a `git grep` over HEAD and takes
# about a second — unlike ground_truth.sh it executes no instrument code and
# writes nothing outside this directory.  Its default subject is the instrument
# mg-6e4f pinned; pass any directory to ask about another.
set -e
cd "$(dirname "$0")"
python3 selftest_20ee.py > out_selftest_20ee.txt
python3 census.py        > out_census.txt
python3 consumers.py     > out_consumers.txt
echo "mg-20ee census: $(sed -n '/transcripts carry/p' out_census.txt | tr -s ' ')"
echo "mg-6e4f consumers: $(sed -n '/^CONSUMERS:/p' out_consumers.txt)"
