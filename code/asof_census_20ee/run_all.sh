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
# mg-e8b0: worklist.py IS run here, for permuted.py's reason and not for
# ground_truth.sh's: it executes NO instrument code and needs no dirty tree.
# Every figure it prints is a function of two commits, read through `git show`
# and `git log`, so out_worklist.txt reproduces BYTE-IDENTICALLY -- condition 2
# as originally written -- which is the only honest arrangement for the file
# whose subject is that out_ground_truth.txt cannot.  Its own hand-run half is
# the comparison mode, and it is NOT run here because its input comes from
# ground_truth.sh:
#     sh code/asof_census_20ee/ground_truth.sh <dirs> > /tmp/gt.txt
#     python3 code/asof_census_20ee/worklist.py --rerun /tmp/gt.txt
#
# mg-6e4f: consumers.py IS run here.  It is a `git grep` over HEAD and takes
# about a second — unlike ground_truth.sh it executes no instrument code and
# writes nothing outside this directory.  Its default subject is the instrument
# mg-6e4f pinned; pass any directory to ask about another.
# mg-ede8: liveindex.py IS run here, and it is the one file in this directory
# whose subject is another file in it.  consumers.py reads the LIVE INDEX by
# design, so out_consumers.txt is a function of WHEN IT WAS RUN and not of the
# commit it is attached to — and 5 of its 8 committed versions were already
# wrong when they were written.  liveindex.py re-derives the path-list-valued
# figures AT THE COMMIT THAT CARRIES EACH VERSION, which needs no instrument
# execution and no dirty tree, so ITS OWN transcript reproduces BYTE-IDENTICALLY
# at a declared AS_OF while its subject cannot.  ITS LIVE HALF IS ON STDERR AND
# GATES NOTHING: the staleness is created by the refinery's rebase, after the
# last moment anything on the branch can run, so a gate here would be red for
# reasons the author cannot act on (mg-724a's recorded/gated split).
#
# mg-0bf1: exemplars.py IS run here, for worklist.py's reason exactly: it
# executes no instrument code and needs no dirty tree, because every figure --
# the work-list, the 572 markdown records, the blame, the diffs -- is read at a
# declared commit.  So out_exemplars.txt reproduces BYTE-IDENTICALLY, and in
# particular THIS DIRECTORY'S OWN README IS ONE OF ITS SUBJECTS and editing it
# cannot move the transcript.  Its one-pair mode is the hand-run half, and it
# is what P30 calls:
#     python3 code/asof_census_20ee/exemplars.py --pair <record> <name> [<rev>]
#
# mg-5058: semantic.py IS run here, for exemplars.py's reason exactly and with
# one more of its own.  It executes no instrument code, needs no dirty tree, and
# every figure -- the estate-wide population of declared limits, the four
# registry rows, the blame behind each witness, the pre-registration census --
# is read at a declared commit, so out_semantic.txt reproduces BYTE-IDENTICALLY.
# THE ONE OF ITS OWN: two of its four rows read their declaration out of
# selftest_20ee.py, which THIS BRANCH EDITS, and one of its population figures
# counts that same file -- so a version reading off disk would have its numbers
# moved by the commit that adds its own controls.  Its one-row mode is the
# hand-run half:
#     python3 code/asof_census_20ee/semantic.py --row R2
set -e
cd "$(dirname "$0")"
python3 selftest_20ee.py > out_selftest_20ee.txt
python3 census.py        > out_census.txt
python3 consumers.py     > out_consumers.txt
python3 liveindex.py     > out_liveindex.txt
python3 permuted.py      > out_permuted.txt
python3 worklist.py      > out_worklist.txt
python3 exemplars.py     > out_exemplars.txt
python3 semantic.py      > out_semantic.txt
echo "mg-20ee census: $(sed -n '/transcripts carry/p' out_census.txt | tr -s ' ')"
echo "mg-6e4f consumers: $(sed -n '/^CONSUMERS:/p' out_consumers.txt)"
echo "mg-ede8 live-index: $(sed -n '/^LIVE-INDEX:/p' out_liveindex.txt)"
echo "mg-885d condition 2: $(sed -n '/^CONDITION 2:/p' out_permuted.txt)"
echo "mg-e8b0 work-list: $(sed -n '/^CONDITION 0 (work-list):/p' out_worklist.txt)"
echo "mg-0bf1 exemplars: $(sed -n '/^CONDITION 0 (exemplars):/p' out_exemplars.txt)"
echo "mg-5058 semantic: $(sed -n '/^CONDITION 0 (semantic):/p' out_semantic.txt)"
