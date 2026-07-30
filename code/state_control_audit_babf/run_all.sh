#!/bin/sh
# mg-babf — INDEPENDENT AUDIT of mg-7870 / e924590, the digest-based repair of the
# working-tree control for b68db5d's delta.  THIRD control in this lineage.
#
# WHAT THIS AUDITS.  mg-2da3 built a working-tree control; mg-2216 got 8 of 14 mutations
# past it; mg-7870 replaced the certifying mechanism with a SHA-256 per certified region,
# stated the normalisation in full, and stated the coverage boundary in COVERAGE.md.  A
# digest cannot be fooled by a length-preserving edit, so everything that is left lives in
# what the implementation decides is INSIGNIFICANT BEFORE HASHING.  That is where this
# audit aims.
#
# WHAT IT DOES NOT DO.  It does not re-run mg-7870's negative control and treat the result
# as evidence, and it does not re-run mg-2216's battery and treat THAT as evidence either:
# mg-7870 built against mg-2216's fourteen, so those fourteen are now the repair's
# known-answer set.  Every mutation in mutations_babf.py is mine and none is one of the
# fourteen.  mg-2216's five B2 mutations are re-run — RE-IMPLEMENTED from their published
# descriptions, sharing no code with either predecessor — because "did the repair close its
# own stated finding?" is a question only they can answer.
#
# SAFETY.  Steps 2 and 3 MUTATE STATE.md and docs/state-history/README.md in the working
# tree and restore them under a finally + sha256 check.  They refuse to run if either file
# is already dirty.  Step 5 runs the pinned battery twice (~2 min of the total).
#
#   1. claims_audit.py        the coverage statement, audited against the code
#   2. regression_2216_b2.py  THE REGRESSION — mg-2216's five B2 mutations must now fail
#   3. mutations_babf.py      my own 15 mutations, none of them mg-2216's
#   4. statements_audit.py    do the published statements and the control agree?
#   5. preservation.py        did the repair preserve what was already right?
#
# The committed outputs are out_claims.txt / out_regression.txt / out_mutations.txt /
# out_statements.txt / out_preservation.txt beside this script, plus out_all.txt, which is
# this script's own output.  All six reproduce byte-identically at this commit.  The audit
# document is docs/OneThird-STATE-Control-Digest-mg7870-IndependentAudit.md.
# NO `set -e` HERE, deliberately.  mutations_babf.py exits 1 when it finds a silent miss
# and regression_2216_b2.py exits 1 if B2 fails to close — those are this audit's FINDINGS,
# not failures of the script, and aborting the run on the first one would hide steps 4 and
# 5 behind them.  Each step's exit code is printed instead, so nothing is swallowed.
set -u
cd "$(git rev-parse --show-toplevel)"
D=code/state_control_audit_babf

step() {
    echo "### $1"
    shift
    python3 "$@"
    echo "--- exit $?"
    echo
}

step "1. claims_audit.py       — mg-7870's coverage statement, against the code" \
     $D/claims_audit.py
step "2. regression_2216_b2.py — mg-2216's five B2 mutations, re-implemented" \
     $D/regression_2216_b2.py
step "3. mutations_babf.py     — my own battery, none of it mg-2216's  (exit 1 = findings)" \
     $D/mutations_babf.py
step "4. statements_audit.py   — do the statements and the control agree?" \
     $D/statements_audit.py
step "5. preservation.py       — did the repair preserve what was already right?" \
     $D/preservation.py
