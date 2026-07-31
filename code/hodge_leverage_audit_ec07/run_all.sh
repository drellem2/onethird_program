#!/bin/sh
# mg-ec07: INDEPENDENT AUDIT of mg-ff3e's repair of mg-9207 -- "the census is
# position-aware over the WHOLE record".  One step, one output.
#
# Pure Python 3 + git, no third-party packages.  ~4 min.
#
# THE THREE QUESTIONS, in the assignment's order:
#
#   1. DID IT FIX THE SET OR THE NEXT FIELD?  "Whole record" is a strong claim
#      and this artifact has been fixed field-by-field twice.  A1 substitutes
#      EVERY CHARACTER of every site alone -- 37 866 of them, a population
#      nobody wrote down -- and A5 hunts on disk for a field the record still
#      does not reach.
#   2. DID THE SAME-KIND ENUMERATION HAPPEN?  A different question from
#      whether the fix works.  A8 checks it exists, is the parent's own, and
#      that each item was CHECKED rather than named -- from git and from the
#      runner's own stdout, not from mg-ff3e's summary of itself.
#   3. DO NOT DISTURB WHAT IS CONFIRMED.  A3 re-derives mg-9207's 12 of 12 at
#      847 exchanges over 3 sites, enumerated from `partition`.
#
# Plus A7, which no list in the assignment names: THE BLESSING PATH.
#
# NOT A REPLICATION.  `repair_9207.py` and `audit_8eca_repair.py` are not run
# and their bottom lines are not quoted -- replication is not corroboration
# when the copies share a source.  The only thing imported from the artifact
# is the GATE ITSELF, because an audit that re-implements the gate is auditing
# its own re-implementation.
#
# AND EVERY NEW CONTROL IS DEMONSTRATED AGAINST A COMMIT WHERE THE DEFECT IS
# STILL PRESENT.  A1 runs its byte census against `verify_landing.py` at
# eb600f7 -- the parent of the repair -- as well as at HEAD.
#
# REPRODUCTION CONTRACT, in terms of the FILES READ rather than a commit.
# This transcript regenerates byte-identically for any tree in which STATE.md,
# docs/OneThird-Hodge-Side-Leverage.md, docs/state-history/attempt-mg-a3d4.md,
# code/hodge_leverage_landing_e1d0/ and code/hodge_leverage_audit_9207/ are
# unchanged, and in which eb600f7 is reachable.  It embeds no sha of its own.
#
# IT MUTATES THE TREE AND RESTORES IT, sha256-verified, and REFUSES TO RUN
# against a dirty tree scoped to the files it will restore: a restore over an
# uncommitted edit to one of them destroys it.
#
# AND THE RUNNER REPORTS THE INSTRUMENT'S STATUS.  It redirects rather than
# piping into `tee`: under `set -e` a pipeline's status is tee's, which is how
# a transcript recording a refutation came to be committed beside an exit 0
# (mg-c2b3).  Exit 1 here is CORRECT and expected -- this audit raises
# findings, and the arc's convention is that an audit with findings exits 1.
set -e
cd "$(dirname "$0")"

echo "== mg-ec07: did mg-ff3e fix the SET, or the next field? =="
status=0
python3 audit_ec07.py --full > out_audit_ec07.txt || status=$?
cat out_audit_ec07.txt
exit "$status"
