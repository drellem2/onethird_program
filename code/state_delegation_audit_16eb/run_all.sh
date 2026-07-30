#!/bin/sh
# mg-16eb — the EIGHTH control in this lineage: the independent audit of mg-0049's repair
# of mg-5644's B1 (9ca11c4 + 5594c69).
#
# THE BRIEF, in one line.  Seven for seven the blind spot MOVED rather than closed, and the
# seventh moved onto ground the sixth repair itself laid.  So the question is not "is the fix
# correct" but WHICH SURFACE DOES THIS FIX CREATE.
#
# WHAT THIS AUDIT DOES NOT DO.  It does not inherit a layer verdict, a harness or a figure.
# Section 1 proves the predecessor batteries are unedited with git rather than by assertion,
# and section 5 regenerates every committed output of the repair under test and diffs the
# bytes — because reading a committed out_*.txt IS inheriting a verdict.
#
# ~25 min, most of it the batteries' full runs of the control.  Sections 3 and 5 MUTATE
# tracked files in the working tree — including delta_control.py itself — and restore them
# under a `finally` plus a sha256 check; each refuses to run on a dirty tree, so RUN THIS ON
# A COMMITTED TREE.  Sections 1, 2, 4 and 6 write nothing to a tracked file.
#
# SECTIONS 5 AND 6 need two real GFM renderers, installed OUTSIDE the repo.  They are a
# dependency of the EVIDENCE only, never of the control:
#
#     D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
#     NODE_PATH="$D/node_modules" sh code/state_delegation_audit_16eb/run_all.sh
#
# Without them section 6 prints the install line and exits 3, and section 5 reports the three
# renderer-dependent rows as NOT REPRODUCED rather than silently as reproduced.  BROKEN 1
# stands on section 6, so read that exit code before reading its finding.
set -e
cd "$(git rev-parse --show-toplevel)"

echo "### 1. THE THREE PREDECESSOR DIRECTORIES ARE UNMODIFIED BY mg-0049 — proof, not"
echo "###    assertion.  A battery edited by the party under test is not a control, and"
echo "###    this audit checks it with git rather than by reading the committed outputs."
for pair in "a4aeeb9 code/state_layer_audit_218d" \
            "3a80d99 code/state_delegation_audit_5644" \
            "2a29f30 code/state_delegation_repair_bee1"; do
    base=${pair%% *}; dir=${pair#* }
    n=$(git diff "$base..HEAD" -- "$dir" | wc -c | tr -d ' ')
    nmd=$(git diff "$base..HEAD" -- "$dir" ':!*.md' | wc -c | tr -d ' ')
    echo "    git diff $base..HEAD -- $dir/            -> $n bytes"
    echo "    git diff $base..HEAD -- $dir/ ':!*.md'   -> $nmd bytes  (executable content)"
done
echo "    (mg-bee1's directory is the one with a non-zero .md diff: mg-0049 appended a"
echo "     CORRECTION OF RECORD under its L1 row and left the row verbatim.  No .py file in"
echo "     any of the three moved, so every re-run below is on an unedited instrument.)"
echo

echo "### 2. delta_control.py on the clean tree (expect 0), and the model's self-tests"
python3 code/state_landing_control_2da3/delta_control.py
python3 code/state_landing_control_2da3/presentation.py
python3 code/state_landing_control_2da3/negative_control.py
echo

echo "### 3. battery16eb.py — EIGHT mutations mg-0049's author never saw, every exit code"
echo "###    PREDICTED BEFORE THE RUN, on this audit's own harness — plus the DOCUMENTED"
echo "###    RECOVERY PATH followed to the letter on C1"
python3 code/state_delegation_audit_16eb/battery16eb.py
echo

echo "### 4. claims16eb.py — every checkable claim mg-0049 ADDED, checked.  Scope is the"
echo "###    diff, not the repository."
python3 code/state_delegation_audit_16eb/claims16eb.py
echo

echo "### 5. reproduce16eb.py — mg-0049's SEVEN committed out_*.txt regenerated from their"
echo "###    producers and diffed BYTE FOR BYTE, sha256 printed on both sides"
python3 code/state_delegation_audit_16eb/reproduce16eb.py
echo

echo "### 6. render16eb.py — what a reader is ACTUALLY shown, on two real GFM renderers,"
echo "###    with the tag stack walked rather than the tags stripped"
python3 code/state_delegation_audit_16eb/render16eb.py || echo "(section 6 exited $?)"
echo

echo "### 7. mg-5644's OWN audit, re-run UNMODIFIED — the audit mg-0049 answers, on its own"
echo "###    harness.  Its section 5 is mg-218d's SIXTEEN, also unmodified."
sh code/state_delegation_audit_5644/run_all.sh
