#!/bin/sh
# mg-54b1 -- the CHEAP arms.  Under 2 seconds, no network, and it does not
# execute any instrument under audit, so it is safe in your own worktree.
#
# THE EXPENSIVE ARM IS DELIBERATELY NOT HERE.  `sweep_54b1.sh` re-runs every
# instrument in its sample, takes about 40 minutes, and must be pointed at a
# CLONE because those instruments mutate the tree they run in.  Putting it in
# this runner would make `sh run_all.sh` destructive by default, and putting
# it in ./build.sh would add 40 minutes to an 88-second gate.  So
# out_sweep_54b1.txt is ONE DATED RUN and is not a fixed point -- which is the
# same property, and the same admission, as mg-20ee's out_ground_truth.txt.
# c1_population.py §3 counts this directory into its own blind spot for that
# reason rather than exempting it.
#
# Each step REDIRECTS and has its status read by an explicit `||` guard rather
# than piping into `tee`: a pipeline's exit status in POSIX sh is its LAST
# command's, so a `tee` would let a failing arm leave this runner exiting 0.
# mg-c2b3, one directory over.
set -e
cd "$(dirname "$0")"

python3 -B c0_controls.py > out_c0_controls.txt || {
    cat out_c0_controls.txt; echo "c0_controls.py FAILED"; exit 1; }
cat out_c0_controls.txt

python3 -B c1_population.py > out_c1_population.txt || {
    cat out_c1_population.txt; echo "c1_population.py FAILED"; exit 1; }
cat out_c1_population.txt

echo
echo "Headline lines:"
grep -h '^C[01] TOTAL BAD:\|^SWEEP TOTAL STRONG:' out_*.txt || true
echo
echo "C0/C1 TOTAL BAD are scored and MUST be 0: they are controls, not"
echo "findings.  SWEEP TOTAL STRONG is the finding, and out_sweep_54b1.txt"
echo "is one dated run of an arm this runner does not re-take."
