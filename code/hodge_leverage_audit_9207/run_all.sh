#!/bin/sh
# mg-9207: INDEPENDENT AUDIT of the mg-8eca repair (d59ecd9 + bee07a1) of the
# two items mg-8aae left open.  One step, one output.
#
# Pure Python 3 + git, no third-party packages.  Measured runtime 2026-07-31 on
# a 2024 laptop: ~7 min, almost all of it the ~21 runs of the real landing
# runner, the ~19 runs of the mg-8a5c instrument, and the two long runs of
# mg-8aae's and mg-8916's own instruments in S.
#
# PREDICTED EXIT CODE, WRITTEN BEFORE THE FIRST RUN: 1.  Not because the repair
# fails -- H-1 and H-2 both hold, and the sections that measure them are green
# -- but because this audit predicted three findings and an instrument that
# raises findings and exits 0 is the defect this arc keeps meeting.
#
# WHAT THIS INSTRUMENT IS FOR.  mg-8aae's defect was A CHECK THAT FIRED ONLY
# THROUGH A PURPOSE-BUILT HOOK WHILE BEING `x == x` AGAINST THE ARTIFACT.  So
# the question this audit exists to answer is not "does the repair contain more
# code" but "does the new check fire on the SAME PATH A REAL DEFECT WOULD".
# Every demonstration here therefore:
#
#   * writes the mutation TO DISK, into the real document, and
#   * scores it by running the real runner AS A SUBPROCESS, and
#   * sets NO environment variable, and
#   * never calls the gate function in memory.
#
# ⚠️ AND IT SCORES AT GATE GRANULARITY, NOT AT THE EXIT CODE.  The landing
# runner can exit 1 without the gate having seen anything: its own negative
# control freezes three literal strings lifted out of the live documents and
# `assert`s each occurs exactly once, so an edit at those lines raises
# AssertionError.  E2 is exactly that case -- 0 gate rows refuted, exit 1.  An
# exit code produced by a traceback and an exit code produced by a gate are the
# same integer and different sentences, which is finding J-3.
#
# IT MUTATES THE TREE AND RESTORES IT.  STATE.md, the deliverable, the row
# history and code/hodge_leverage_audit_8a5c/audit_repair_8e30.py are written to
# and restored inside a `finally`, every restoration CHECKED BY sha256.  It
# REFUSES TO RUN if any of them is already dirty -- a `git checkout --` over an
# uncommitted edit destroys it.  Every site mutation is LENGTH-PRESERVING,
# because four of the five live figures are lengths of the very text mutated.
#
# IT NEVER RUNS `code/hodge_leverage_landing_e1d0/run_all.sh`.  That runner
# redirects into `out_verify.txt`, which is a COMMITTED transcript; an audit
# that regenerates the record it is checking has destroyed its own evidence.
# It runs `verify_landing.py` directly and sha256-verifies five committed
# transcripts untouched afterwards.
#
# REPRODUCTION CONTRACT, in terms of the FILES READ rather than a commit.
# out_audit_9207.txt regenerates for any tree in which STATE.md, the
# deliverable, docs/state-history/attempt-mg-a3d4.md,
# code/hodge_leverage_landing_e1d0/verify_landing.py,
# code/hodge_leverage_audit_8a5c/audit_repair_8e30.py,
# code/hodge_leverage_audit_8aae/ and code/hodge_leverage_repair_8916/ are
# unchanged.  It embeds no sha of its own.
#
# AND THE RUNNER REPORTS THE AUDITOR'S STATUS.  It redirects rather than piping
# into tee, captures the status and exits with it -- mg-f922 finding F, three
# generations on, applied to the instrument that reports it.
set -e
cd "$(dirname "$0")"

echo "== mg-9207: the mg-8eca repair, re-measured on disk against the real runner =="
status=0
python3 audit_8eca_repair.py > out_audit_9207.txt || status=$?
cat out_audit_9207.txt
exit "$status"
