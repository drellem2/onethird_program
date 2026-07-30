#!/bin/sh
# mg-0049 — the SEVENTH control in this lineage: the repair of mg-5644's B1.
#
# WHAT WAS BROKEN.  mg-bee1 closed mg-218d's B2 by DELEGATING: the certified ledger cell
# cites five sections of docs/state-history/attempt-mg-276d.md by name, and mg-bee1 gave each
# of them a content digest.  It gave them nothing else.  The two files the instrument READS
# carry a content digest, a presentation record AND section 8's default-deny guards; the file
# it POINTS AT carried the first of the three.  mg-5644 collected: one `<!--` line at the top
# of the target, every cited section byte-identical, every delegated digest matching, and both
# `marked` and `markdown-it` agreeing that a reader following the certified cell's six links
# is shown a BLANK PAGE — at exit 0.
#
# WHAT THIS DOES.  No new mechanism.  presentation.py is applied to the delegated surface the
# way it is already applied to the certified one: section 2c takes a PRESENTATION RECORD per
# cited section, and section 8's guards read every declared target file.  Both halves were
# needed — see split_0049.py, which measures that the guards alone close R1 and NOT R2.
#
# ~8 min, most of it the batteries' full runs of the control.  Sections 3, 4, 7 and 8 MUTATE
# tracked files in the working tree and restore them under a `finally` + sha256 check; each
# refuses to run on a dirty tree — so RUN THIS ON A COMMITTED TREE, or section 7's and
# section 8's mutations of delta_control.py itself will refuse and say so.  Sections 0, 1, 2,
# 5 and 6 mutate nothing on disk.
#
# SECTION 6, and section 8's own section 3, need two real GFM renderers, installed OUTSIDE
# the repo.  They are a dependency of the EVIDENCE only, never of the control:
#
#     D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
#     NODE_PATH="$D/node_modules" sh code/state_delegation_repair_0049/run_all.sh
#
# Without them those sections print the install line and exit 3; everything else is
# unaffected and the repair stands on sections 4 and 5.
set -e
cd "$(git rev-parse --show-toplevel)"

echo "### 0. THE TWO PREDECESSOR AUDIT DIRECTORIES ARE UNMODIFIED — proof, not assertion"
echo "###    (a battery edited by the party it tests is not evidence about that party)"
for pair in "a4aeeb9 code/state_layer_audit_218d" "3a80d99 code/state_delegation_audit_5644"; do
    base=${pair%% *}; dir=${pair#* }
    n=$(git diff "$base..HEAD" -- "$dir" | wc -c | tr -d ' ')
    echo "    git diff $base..HEAD -- $dir/   ->   $n bytes of diff"
done
echo

echo "### 1. delta_control.py — the repaired control on the clean working tree (expect 0)"
python3 code/state_landing_control_2da3/delta_control.py
echo

echo "### 2. presentation.py — the model's own declared subset, incl. the DELEGATED SHAPE"
python3 code/state_landing_control_2da3/presentation.py
echo

echo "### 3. negative_control.py — the control can still fail, on all ten of its own rows"
python3 code/state_landing_control_2da3/negative_control.py
echo

echo "### 4. battery_0049.py — NINE mutations on the delegated surface, exit codes PREDICTED"
echo "###    FIRST, run on mg-5644's harness imported unmodified"
python3 code/state_delegation_repair_0049/battery_0049.py
echo

echo "### 5. split_0049.py — WHICH MECHANISM catches which row: the guards alone would have"
echo "###    closed R1 and NOT R2, measured rather than argued"
python3 code/state_delegation_repair_0049/split_0049.py
echo

echo "### 6. render0049.py — this repair's five NEW claims against two real GFM renderers"
python3 code/state_delegation_repair_0049/render0049.py || echo "(section 6 exited $?)"
echo

echo "### 7. coverage218d.py — COVERAGE.md checked against the code, not against itself"
echo "###    (this repair edited COVERAGE.md, so mg-218d's external check on it is re-run)"
python3 code/state_layer_audit_218d/coverage218d.py
echo

echo "### 8. mg-5644's OWN battery, re-run UNMODIFIED — the audit that found this defect"
echo "###    (its section 5 is mg-218d's SIXTEEN, on mg-218d's own harness, also unmodified)"
sh code/state_delegation_audit_5644/run_all.sh
