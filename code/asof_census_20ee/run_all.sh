#!/bin/sh
# mg-20ee — the census, its controls, and the pointer to the ground truth.
#
# ground_truth.sh is NOT run here.  It takes ~70 minutes, executes every
# candidate instrument, and writes-then-restores directories under code/ —
# none of which belongs on a build path.  out_ground_truth.txt records one
# dated run; re-run it by hand.
#
# mg-4020: pinnable.py is NOT run here, and not for cost -- it is a diff read
# and takes no time at all.  It REQUIRES the subject suite to have been run and
# NOT restored, because it classifies a drift rather than producing one, and a
# build path must not be in that state.  It REFUSES an empty diff rather than
# reporting it clean, so wiring it here would make it fail on every clean tree.
# Run it by hand, between running a suite and restoring it:
#     sh code/species_repair_a4ef/run_all.sh
#     python3 code/asof_census_20ee/pinnable.py code/species_repair_a4ef
#     git checkout -- code/species_repair_a4ef
# out_pinnable_a4ef.txt and out_pinnable_b0ae.txt are one dated hand-run each
# and NO SUITE RE-TAKES THEM -- the declaration out_ground_truth.txt already
# makes about itself, and the same blind spot.
#
# mg-885d: permuted.py IS run here, and unlike pinnable.py it can be, because
# it needs no dirty tree: its estate scan reads a DECLARED COMMIT through
# `git ls-tree` and `git cat-file`.  That is also why its own transcript
# reproduces BYTE-IDENTICALLY -- condition 2 as originally written -- which is
# the only honest arrangement for the file arguing that other transcripts
# cannot.  Its comparison mode is the hand-run one:
#     python3 code/asof_census_20ee/permuted.py <transcript> <old-rev> [<new-rev>]
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
python3 permuted.py      > out_permuted.txt
echo "mg-20ee census: $(sed -n '/transcripts carry/p' out_census.txt | tr -s ' ')"
echo "mg-6e4f consumers: $(sed -n '/^CONSUMERS:/p' out_consumers.txt)"
echo "mg-885d condition 2: $(sed -n '/^CONDITION 2:/p' out_permuted.txt)"
