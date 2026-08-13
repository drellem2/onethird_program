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
#
# --- mg-602d -------------------------------------------------------------------------------
# A FIFTH SUITE JOINS THE GATE AND IT IS THE CHEAPEST YET — 0.2 s measured.  THE WHOLE GATE IS
# MEASURED AT 44.8 s ON THIS HOST WITH IT IN.  That is BELOW the 47.5 s mg-03cf recorded for the
# four-suite gate, so the fifth suite is not what moved it and the two numbers are two hosts (or
# two load conditions), not a speed-up: read either as a measurement of its own run and neither
# as a property of the gate.  ⚠️ THIS COMMENT FIRST SAID 48.9 s, WHICH WAS THE ADDITION
# ARITHMETIC AND NOT A RUN — mg-17aa's D4, committed inside the very comment that names it,
# and corrected here by running the thing.
#
# It gates docs/CONCEPTS.md, the conceptual document (STATE.md's own pointer paragraph explains
# why that file exists).  WHAT IT BUYS IS THE ONLY THING THAT MAKES A CONCEPTUAL DOCUMENT SAFE
# TO KEEP: prose about MEANING has no population attached and no arithmetic to check, so a
# sentence stays readable forever after the row that earned it has moved.  Every claim row
# therefore carries a pointer and every unearned claim carries the word BELIEF, and the gate
# refuses a merge that drops either.  It also gates LENGTH, which is not decoration — the
# ticket's own words are "succinct is a requirement, not a style note", and the failure mode is
# that the file grows into a second STATE.md and stops being re-read.
#
# The gate is on STRUCTURE, not on truth: it cannot check that a pointer is CORRECT, only that
# one is THERE — the same split as mg-03cf's, and c1 measures it rather than asserting it, with
# a wrong-direction world in which a pointer is swapped for a different well-formed item id and
# the gate stays green ON PURPOSE.
# --- mg-28b6 -------------------------------------------------------------------------------
# A SIXTH SUITE JOINS THE GATE AND IT IS THE CHEAPEST OF ALL — 0.34 s measured.  THE WHOLE GATE
# IS MEASURED AT 45.6 s ON THIS HOST WITH IT IN, and as with mg-602d's entry that number is a
# run and not the addition arithmetic.
#
# WHAT IT GATES IS NOT A FILE — IT IS AN APPLIED FINDING.  mg-0e8c established on Daniel's
# challenge that row 8 stated the programme's central open problem in a form its OWN PROVEN
# constant discharges, restated the row, and reconciled the sites carrying the old phrasing.
# Nothing checked that they STAY restated, and the failure mode is specific rather than generic:
# the discharged phrasing is the SHORTER and more quotable one, so it is what a hurried edit
# reaches for — and this corpus's own record has it being reached for twice (mg-345e:64,
# mg-6bd1:200) before Daniel reached it a third time, from STATE.md's own words, unprompted.
#
# IT ALSO CLOSES A DECLARED BLIND SPOT RATHER THAN ADDING A NEW ONE.  The twin's proof-chain
# prose is outside code/rendered_twin_pin_9bc2's coverage BY ITS OWN COVERAGE.md ("Anything
# outside the ledger table ... its proof-chain prose ... is uncovered ... the historically most
# common form of this defect is out of scope"), which is exactly where mg-0e8c's enumeration
# lost a site and where mg-957a had NAMED the same lag a fortnight earlier and left it.  This
# suite is the first thing in the estate that reads that prose.
#
# THE EDIT IS HERE, AGAIN, for the reason this file's header gives: refinery.toml alone would
# put it on route 1 and leave default discovery reaching a gate list one suite short.
#
# --- mg-f771 -------------------------------------------------------------------------------
# A SEVENTH SUITE JOINS THE GATE, IT RUNS OUTSIDE THE LOOP, AND ITS SUBJECT IS THIS FILE.
# 0.18 s measured.  THE WHOLE GATE IS MEASURED AT 44.7 s ON THIS HOST WITH IT IN.  That is
# BELOW the 45.6 s mg-28b6 recorded for the six-suite gate, and for the reason mg-602d's
# entry already gives: read either as a measurement of its own run and neither as a property
# of the gate.  ⚠️ THIS COMMENT WAS DRAFTED SAYING 46.9 s, WHICH WAS THE ADDITION ARITHMETIC
# AND NOT A RUN — mg-17aa's D4, drafted inside the comment of the very suite whose subject is
# a committed number that disagrees with the thing it describes.  Corrected by running it,
# before the first commit rather than after.
#
# WHAT IT GATES IS THE GATE'S OWN SIDE EFFECT.  Every suite above rewrites the tracked
# transcripts it owns, so every merge into this repository leaves the tree dirty BY
# CONSTRUCTION -- mg-69b4 filed it as D5, "the gate leaves four tracked files modified in two
# directories that are not mine", and nothing owned it.  The cost was not the dirty tree.  It
# was that `code/facts_registry_03cf/out_f0_registry_discipline.txt` sat on main reading
# `VERDICT: GREEN -- 20 entries` about a registry that has 23, for as long as nobody happened
# to commit the refresh.  These transcripts are QUOTED -- docs/FACTS.md:110 links one, and
# code/sweep_evidence_control_d2c2/p1_names.py reads another out of `git HEAD:` on purpose --
# so a stale one is a REPORT, not a build artifact, and the part written to be quotable was
# the wrong half.
#
# THE INVARIANT: a committed out_*.txt must never be able to disagree with the repo it
# describes.  It is enforced by reading what the six suites above have just written and
# comparing it with the committed copy.  IT IS NOT A BYTE COMPARISON, AND IT CANNOT BE:
# these transcripts embed wall-clock timings and ABSOLUTE WORKTREE PATHS, so the same repo
# state produces different bytes in every polecat worktree.  Byte-equality is unsatisfiable
# here and a gate that can never be green is worse than no gate.  Exactly two families are
# declared not to be a function of repo state (checkout root, decimal seconds) and every
# other difference is RED.  code/gate_fixed_point_f771/lib_f771.py holds the two rules and
# nine planted worlds bound them -- six the normaliser MUST catch, three it must NOT.
#
# THE COST, STATED RATHER THAN DISCOVERED: a branch that moves STATE.md must now also carry
# the refreshed transcripts, because `bytes 138335` in the ratchet's transcript IS a function
# of repo state.  That is the current dirty-tree behaviour made mandatory instead of
# accidental, which is the trade mg-f771 named in advance and chose.
#
# IT RUNS OUTSIDE THE LOOP because it must run LAST -- it reads the other suites' side
# effects -- and because it needs the freshness handshake the loop cannot give it.  Run on
# its own it would compare committed transcripts against worktree copies nothing had
# refreshed, find them equal, and print a green meaning only "nobody hand-edited these".  So
# it REFUSES without BUILD_SH_RAN_THE_SUITES=1, which is set on exactly this one line.
#
# --- mg-843d -------------------------------------------------------------------------------
# AN EIGHTH SUITE JOINS THE GATE -- the SEVENTH IN THE LOOP, since mg-f771's runs after it and
# outside it -- AND IT IS THE ONE THAT WAS ALREADY RED.  THE WHOLE GATE IS MEASURED AT
# 88.4 / 87.1 / 85.2 s ON THIS HOST WITH IT IN -- three runs, quoted as three, because mg-602d's
# entry had to correct itself for quoting the addition arithmetic (mg-17aa's D4) and a single
# figure here would hide a 3 s spread that is load, not the gate.  Against 44.8 s measured on the
# same host minutes earlier WITHOUT it.  This is the most expensive addition since mg-06d1's and
# by some way the largest proportional one: it very nearly doubles the gate.  The cost is argued
# below and it is NOT argued as small.
#
# WHY IT IS BEING ANSWERED AT ALL.  `code/face_geometry_repair_e35b/verify_e35b.py` exited 1 on
# main from `de86fee` (2026-08-10) to today: its V6b CENSUS row measured 210 formatted values in
# NEGATIVE CONTROL 4 against a declared 184.  The tripwire was not broken -- it was firing,
# correctly, on a real unconstructed input, and nothing in the estate ran it.  Every merge in
# those three days gated GREEN with a red control in the same tree, including `7025d03` at 45 s.
# That is a control firing into a room with nobody in it, and it is the shape this file exists
# to stop.  The census question is answered in that suite's README and the declaration moved to
# 210 WITH ITS DERIVATION; the suite is green before it is added here, which is the ordering the
# ticket demanded -- a red suite joining the gate blocks every merge in the repository.
#
# WHY THIS SCRIPT AND NOT EVERY SCRIPT IN code/**.  Most of `code/` is one-off audits and
# probes: instruments that measured a tree, published a transcript, and finished.  Re-running
# those on every merge would gate on history.  This suite is not that, and the test is what its
# rows READ rather than what its directory is called:
#
#     V6a ANCHORED     reads code/face_geometry/controls_output.txt   -- another ticket's file
#     V6b CENSUS       reads code/face_geometry/controls.py           -- another ticket's file
#     V6c REGENERATED  RUNS  code/face_geometry/controls.py           -- another ticket's file
#     V6d REACH        RUNS  it and splits V6b's total by fate        -- another ticket's file
#
# Every one of the four is scored against a file OTHER tickets keep editing, and `de86fee` is
# the proof that they do.  A row whose input is a live file is a standing control; a row whose
# input is its own literal is the defect mg-fcb2's F2 was about, and this suite had that row and
# had it removed.  By that test the six suites above belong here and this one does too.
#
# WHAT IT COSTS AND WHAT COULD GO INSTEAD.  The gate grew by 43.6 s; the suite's own runner
# measures 42.3 s standalone, so ~1 s is this loop and the rest is the work.  Of the 42.3 s,
# 7.2 s is the verifier and 35.0 s is `demo_v6d_row_can_go_red.py`, which watches the new V6d
# row go red on four mutations of a throwaway copy of code/face_geometry/.  The demonstration is
# 83% of the addition, and it is named here as the removable half so that dropping it later is a
# decision with a number attached.  It is NOT dropped now, for the reason this ticket is about:
# a demonstration nothing runs is a claim that rots, and this file is where the estate finds out
# whether something runs.
#
# AND IT IS UNDER mg-f771's INVARIANT FROM ITS FIRST GATE RUN, which is the right way round.
# This suite writes two tracked transcripts -- out_verify_e35b.txt and out_demo_v6d.txt -- and
# mg-f771's control reads both, so a committed copy of either that disagrees with what the gate
# just produced is RED.  Neither embeds a wall-clock or a worktree path, so neither leans on
# mg-f771's two normalisation rules; they converge by being deterministic rather than by being
# exempted.  That matters more than usual here: this whole ticket is about a transcript
# (out_demo_f2.txt) that sat on main disagreeing with the tree, and the suite added to stop that
# happening again arriving OUTSIDE the control that stops it would have been the joke version.
# --- mg-479c -------------------------------------------------------------------------------
# NO SUITE JOINS THE GATE HERE, AND THE GATE LIST BELOW IS UNCHANGED.  A THIRD ARM JOINS
# code/alias_agreement_06d1/run_all.sh, and the number is stated here for the same reason
# every entry above states one: 0.02 s measured, because it recomputes no tree.  THE WHOLE
# GATE IS MEASURED AT 93.4 s ON THIS HOST WITH IT IN, against the 88.4 / 87.1 / 85.2 s
# mg-843d recorded — and, as mg-602d's entry insists, read that as a measurement of its own
# run and not as a property of the gate.  What is NOT free is a second effect on the same
# suite: g1's falsification block went 0.1 s -> 0.63 s, because the new RED message computes
# the exact Fraction ratio between the two disagreeing columns in order to be able to say
# "these differ by exactly 2".
#
# WHAT THE ARM BUYS.  Until it, the alias-agreement check compared RAW values and had no
# representation for two names denoting ONE quantity IN DIFFERENT NORMALISATIONS -- so a
# factor of 2 between two live conventions and a genuine 2x error were THE SAME SIGNAL, in
# both directions: a FALSE RED on a gate that blocks merges, which is how gates get
# disabled, and a FALSE PASS in which a real error is waved away as "just a normalisation
# difference".  This corpus demonstrably carries the shape (eps_spec/eps_c3ca; u1's
# dialects), so the exposure is real and it is PROSPECTIVE: nothing fires today, and it
# arrives the moment the check is widened or a new alias is registered.
#
# AND THE EXHIBIT THAT PROVES THIS GATE CAN FIRE HAD STOPPED WORKING, silently, for a reason
# that arrived with mg-f771.  `code/alias_agreement_06d1/x0_exhibit.py` runs THIS FILE twice
# and was invoked as `python3 x0_exhibit.py > out_x0_exhibit.txt`; f771's control compares
# every tracked out_*.txt against its committed copy, so the redirect handed it a TRUNCATED,
# HALF-WRITTEN file, f771 graded it DISAGREES, and the exhibit refused with "the gate is
# ALREADY RED before anything was planted" -- correctly, about a redness it had caused
# itself.  The script now writes its own transcript after the last run instead.  Anything
# else that shells `./build.sh` while writing into `code/**/out_*.txt` has this bug.
# THE EIGHTH LOOPED SUITE IS code/twin_disposition_audit_3902 (mg-3902), AND IT IS HERE FOR
# THE REASON THIS FILE EXISTS AT ALL.  It asks the one question mg-9bc2's six sections never
# ask: does the rendered twin's pin RESOLVE against git?  Section 3 compares the pinned digest
# against the live working tree and section 6 compares the pinned commit against a VISIBLE COPY
# OF ITSELF, so the field whose own header calls itself "the only thing in this file that says
# which STATE.md it is a rendering of" was checked only against its own duplicate.  Setting both
# copies to a commit that does not exist was demonstrated leaving that control at CLEAN, exit 0.
#
# IT WAS RED AGAINST origin/main ON THE DAY IT LANDED, which is the argument for adding it
# rather than a hope about the future: the pin named `c308368`, a commit unreachable from
# origin/main whose STATE.md is not the one the pin digests.  That is a check earning its slot
# on the merge critical path by failing, not by passing.
#
# WHY IT IS A SEPARATE SUITE AND NOT `twin_pin.py`'s SECTION 7, which is where it belongs:
# mg-9876's arm census REFUSES an arm-shaped site no registered arm claims, so adding the
# section took `GATE VERDICT: REFUSED`, exit 2 — measured, and it would have blocked every
# merge request in this repository.  Registering it properly needs 5 new probes in
# `a2_discriminate.py`, and those cannot run: `make_sandbox()` builds a tree with no `.git`,
# so the question has no answer inside it.  Folding this into section 7 is the filed successor.
STATUS=0
for suite in \
    code/control_gate_724a/run_all.sh \
    code/state_ratchet_e331/run_all.sh \
    code/alias_agreement_06d1/run_all.sh \
    code/facts_registry_03cf/run_all.sh \
    code/concepts_gate_602d/run_all.sh \
    code/l1b_application_28b6/run_all.sh \
    code/face_geometry_repair_e35b/run_all.sh \
    code/twin_disposition_audit_3902/run_all.sh
do
    echo
    echo "############################################################ $suite"
    sh "$suite"
    RC=$?
    [ "$RC" -gt "$STATUS" ] && STATUS=$RC
done

echo
echo "############################################################ code/gate_fixed_point_f771/run_all.sh"
BUILD_SH_RAN_THE_SUITES=1 sh code/gate_fixed_point_f771/run_all.sh
RC=$?
[ "$RC" -gt "$STATUS" ] && STATUS=$RC
echo
echo "############################################################ build.sh"
echo "worst suite exit: $STATUS   (0 green · 1 a control fired · 2 refused/broken)"
exit "$STATUS"
