#!/bin/sh
# THE ONLY THING THAT ASKS THIS REPOSITORY'S CONTROLS (mg-724a).
#
# This repository is a mathematics corpus, not a program: there is nothing here to compile.
# `build.sh` is the name because the refinery's DEFAULT gate discovery looks for exactly
# `./build.sh` and `./test.sh` at the root when a repository declares no gates of its own
# (internal/refinery/merge.go, defaultGates).  Naming this file that gives the gate TWO
# independent routes to the same command:
#
#   1. .pogo/refinery.toml names it explicitly, which is what runs today;
#   2. if that file is ever deleted, default discovery finds this one anyway.
#
# There is exactly one definition of what the gate IS — the list below — so the two routes
# cannot drift apart into two gate lists that disagree.  Both routes reaching the same file
# is the point: the hole this whole ticket exists to close is a control that nothing invokes,
# and a config file that can be deleted into silence is that hole with a shorter fuse.
#
# WHAT IT DOES ON RED: it exits non-zero, the refinery FAILS THE MERGE REQUEST, and the
# branch does not land.  See code/control_gate_724a/README.md for who hears about it.
#
# --- mg-e331 -------------------------------------------------------------------------------
# A SECOND SUITE JOINS THE GATE, AND THE EDIT IS HERE RATHER THAN IN .pogo/refinery.toml FOR
# THE REASON THIS FILE ALREADY GIVES.  Adding it to refinery.toml alone would put it on route
# 1 and leave route 2 — default discovery, the route that survives that file being deleted —
# reaching a gate list one suite short.  Two routes that reach different gate lists is exactly
# the drift the header above exists to prevent, so the definition stays in one place and this
# file is that place.  mg-724a's own refinery.toml anticipates this in so many words: "(d) A
# COMBINATION — not needed at 16 s.  It becomes the right answer the moment the scope widens
# past these two directories, and that is where the next ticket starts."
#
# EVERY SUITE RUNS, AND THE WORST EXIT WINS.  Not `&&`: short-circuiting means the first red
# suite hides whether the others are red too, so an author fixes one thing, re-submits, and
# discovers the second only on the next round trip.  A gate that reveals its findings one per
# merge attempt is a gate people learn to run locally in a loop, which is how they learn to
# stop reading it.
#
# --- mg-06d1 -------------------------------------------------------------------------------
# A THIRD SUITE JOINS THE GATE, AND IT IS THE EXPENSIVE ONE — 31 s against the 13 s this
# file cost before it, so the gate goes ~13 s -> ~44 s and the number is stated here rather
# than discovered by whoever next wonders why merges got slower.  It buys the twelve
# controls mg-0d1b's INDEX.md records and nothing has ever cashed: 11 quantities aliased
# across up to 13 names in up to 11 trees, computed independently, never once compared.
# 30 s of the 31 is one recompute of twelve trees over 306 posets, measured per-tree in
# code/alias_agreement_06d1/README.md §1; two trees are 92% of it and NEITHER was dropped,
# because a tree dropped from the gate is a permanent blind spot where a poset dropped is
# a smaller sample.  The alternative subsets are costed in that README and rejected there.
#
# THE EDIT IS HERE, AGAIN, for the reason the header above already gives: refinery.toml
# alone would put this on route 1 and leave default discovery — the route that survives
# that file being deleted — reaching a gate list one suite short.
#
# --- mg-03cf -------------------------------------------------------------------------------
# A FOURTH SUITE JOINS THE GATE AND IT IS THE CHEAP ONE — 1.2 s measured, against the ~44 s
# above.  THE WHOLE GATE IS MEASURED AT 47.5 s ON THIS HOST WITH IT IN, and that is the
# number stated rather than the 45 s the addition arithmetic predicts: a runtime quoted
# without being run is mg-17aa's D4, and this one is run.
# It gates docs/FACTS.md, the facts registry (STATE.md's own pointer paragraph explains why
# that file exists).  WHAT IT BUYS IS THE ONLY THING THAT MAKES A REGISTRY WORTH HAVING:
# every entry carries its KIND and its exact SCOPE, so that no figure in it can be quoted
# away from the population that makes it true.  That discipline is a convention, and a
# convention with no gate is one hurried entry away from being over — an entry with the
# number and without the population is exactly STATE.md row 3b's `0/132` in a new file.
# The gate is on STRUCTURE, not on truth: it cannot check that a SCOPE line is correct, only
# that no entry is missing one, which is the failure mode that scales.  It fired on its own
# author's first draft (F8's SCOPE field renamed in passing) and that is recorded in
# code/facts_registry_03cf/README.md rather than quietly fixed.
STATUS=0
for suite in \
    code/control_gate_724a/run_all.sh \
    code/state_ratchet_e331/run_all.sh \
    code/alias_agreement_06d1/run_all.sh \
    code/facts_registry_03cf/run_all.sh
do
    echo
    echo "############################################################ $suite"
    sh "$suite"
    RC=$?
    [ "$RC" -gt "$STATUS" ] && STATUS=$RC
done
echo
echo "############################################################ build.sh"
echo "worst suite exit: $STATUS   (0 green · 1 a control fired · 2 refused/broken)"
exit "$STATUS"
