#!/bin/sh
# mg-5f9a: closing mg-1c80's F1 -- regenerate this landing's transcript.
#
# Pure Python 3, no third-party packages.  Measured runtime 2026-07-31 on a 2024
# laptop: 166 s total -- d1 0.6 s, d2 64 s (twenty-nine full control batteries: ten
# on this tree and on the PRE-REPAIR commit's sources, four more on the
# TWO-RETURN commit for the per-return section, eleven for the CLAUSE sweep, one
# for the RESPELLING equivalence and three on the TWO-CLAUSE commit), d3 15 s
# (two more, plus two runs of mg-da45's landing verifier over the whole 86-poset
# population), d4 78 s (mg-d0e2's own e1, e2 and e3, mg-e7bc's g1, g2 and g3 and
# mg-0b07's p3, all run unmodified as subprocesses, two of them against a pinned
# commit materialised with `git archive`).
# 92 claims, 0 BROKEN: d1 17, d2 49, d3 6, d4 20.
#
# d4's mg-0b07 subprocess is REQUIRED to exit 1 and one of its six claims is
# REQUIRED to be BROKEN -- the one asserting the operator this commit put back
# does not exist.  d4 names it rather than counting it, so a different claim
# breaking is red here.
#
# mg-04a8 added d4 and rewrote d2's label check.  d2's BEFORE half now reads a
# PINNED COMMIT rather than `main`: once mg-5f9a merged, "main's artifact
# regenerates from main's sources" was a statement about this tree, and the
# deletion it then attempted did not even apply -- the shipped file stopped at
# `anchor occurs 0 times`.  A check pinned to a branch asks about whatever that
# branch holds today.
#
# mg-f7e1 SPELLED THE DISJUNCTION WITH AN OPERATOR AND STATED THE BOUND.
# mg-0b07 found that `clause` was not the floor: mg-64b6's one-comparison
# condition, `[len(row) for row in A] != [len(row) for row in B]`, is a
# disjunction Python spells with no operator, and its ORDER half could be taken
# out with the width half standing for BYTE-IDENTICAL, exit 0, every row green.
# Merging had removed the HANDLE, not the rung.  So the `or` is back --
# subtraction applied to the implicitness -- both halves are swept by the clause
# sweep that already existed, and the one the battery cannot see is printed as
# NOT COVERED on the row that carries it.  No sixth technique was added.  d2 also
# counts, from the tree, the compounds no deletion reaches (`any(...)`, `x in S`,
# chained and sequence comparisons), so DELETION REACHES THE TOP-LEVEL BOOLEAN
# OPERANDS OF THE DECIDING CONDITIONS IN THE FILES THE SWEEP VISITS, AND NOTHING
# ELSE is a measured number beside the green rows rather than a promise.  d4 runs
# mg-0b07's own grain probe unmodified: one of its six claims is required to go
# RED -- the one asserting the operator does not exist -- and its three
# perturbation rows are required not to move.
#
# mg-69d1 NARROWED THAT SENTENCE TO THE SWEEP AND CLASSIFIED ALL 17 (mg-eaef E5,
# E4).  It read DELETION ESTABLISHES COVERAGE DOWN TO EXPLICIT BOOLEAN OPERANDS
# AND NO FURTHER, which is read as a guarantee about every explicit boolean
# operand, and 6 of the 17 in the census's two files are not on the reached side:
# 4 nested below the top level of their own condition, where the sweep cannot
# reach, and 2 in posets.py, which the sweep does not visit -- while the
# `operands` column printed 2 for posets.py under a heading that said `deletes`.
# d2's bound section now puts every one of the 17 in exactly one NAMED column,
# with `not determined` printed as a column so an operand the classifier cannot
# place has a name instead of an empty cell, and the sweep's file population is
# ONE constant both the sweep and the table read.
#
# d2 EXITS 1 AT HEAD AND HAS SINCE bfd7948 -- mg-eaef's E8, which mg-69d1 does
# NOT close.  The claim AND THE PIN IS WHAT IT SAYS IT IS reads BROKEN because
# bfd7948 is itself a commit with a two-clause `shape` guard and is newer than
# the pin.  That is the one BROKEN claim in d2's transcript; every other claim in
# this instrument holds, and d1, d3 and d4 exit 0.
#
# mg-64b6 made it PER CLAUSE and made the declared unit DERIVED.  mg-c4c8 found
# that mg-9220's merge left a condition of TWO CLAUSES and that deleting the first
# alone moved not one byte -- the same finding one rung lower -- and that the
# declared unit understated its own patch on 8 of 11.  `absorb_trace`'s `shape`
# condition is now a single comparison of the two row-shape profiles, so there is
# no clause under that `return` to delete alone; d2 sweeps the ENUMERATED clause
# population of the predicate layer, runs the same sweep against the pinned commit
# that still has the two clauses (where it goes red, which is how a sweep gets
# tested), and DERIVES every declared unit from its own patch by parsing the tree
# before and after it.  mg-9220's eleven written declarations are kept verbatim as
# the specimen and measured: 8 of 11 understate.
#
# mg-9220 made the deletion test PER RETURN.  mg-e7bc found that d2 deleted the
# `shape` gate's TWO return statements together and its "the artifact CHANGES"
# was read as a statement about each -- and deleting the FIRST alone left the
# artifact byte-identical.  Every mutation now declares the unit it removes, the
# returns it takes out are counted from its own patch text, d1 checks the table
# against the SOURCE (every rejecting return deleted by exactly one mutation),
# and the inert return is GONE: it was merged into the second's condition rather
# than covered by a new row.  Two independent instruments were anchored to the
# text it removed; d4 runs each against this tree AND against the pinned commit
# it was written for, and scores both.
#
# WHAT IT IS FOR.  mg-da45 printed a gate name as the reason its rows answered
# as they did.  mg-1c80 deleted that gate from the predicate and the artifact
# regenerated BYTE-IDENTICALLY, which is the proof that the name was not what
# the code was doing.  This landing does not write a third reason: the predicate
# now RETURNS the gate it returned at and the number of signs it read, so the
# printed reason is produced by the code path.
#
# d2 is the test that has to pass, and it runs on BOTH sides of the repair --
# mg-1c80's deletion re-run at `main` (predicted: byte-identical) and the
# corresponding deletion here (predicted: the artifact CHANGES, with no scored
# row moving).  Every prediction in d2 and d3 was registered before the runs and
# is printed above the results.
#
# Nothing under ../face_geometry is written by any of these: every mutation is
# applied to a copy in a temporary directory and every battery run captures
# stdout instead of tee-ing it.
#
# NOT `python3 x.py | tee out.txt`, and that is deliberate.  A pipeline's exit
# status in POSIX sh is the LAST command's, so `tee` succeeding would mask a
# verifier exiting 1 -- a committed transcript saying BROKEN under a run_all.sh
# that exited 0.  mg-f922 found exactly that shape in this repository.  Here the
# status is captured and re-raised, so `set -e` below is the whole failure
# protocol: if any part prints a false claim, this script fails.
set -e
cd "$(dirname "$0")"

run() {
    out=$1
    shift
    set +e
    python3 "$@" > "$out" 2>&1
    status=$?
    set -e
    cat "$out"
    return $status
}

echo "== d1: the gate label is returned BY the predicate =="
run out_d1_trace.txt d1_trace.py 5

echo
echo "== d2: THE DELETION TEST, before and after =="
run out_d2_deletion.txt d2_deletion.py

echo
echo "== d3: reintroduction, and whether anything sees it =="
run out_d3_reintroduction.txt d3_reintroduction.py

echo
echo "== d4: mg-d0e2's OWN deletion test, unmodified, against the repair =="
run out_d4_auditor_rerun.txt d4_auditor_rerun.py
