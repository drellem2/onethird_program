#!/bin/sh
# mg-bee1 — the repair of mg-4acd against mg-218d's audit.  Four sections, ~2 min.
#
#     sh code/state_delegation_repair_bee1/run_all.sh
#
# Sections 2, 3 and 4 mutate tracked files in the WORKING TREE and restore them under a
# `finally` plus a sha256 check; each refuses to run on a dirty tree, because a crash would
# then restore the wrong bytes.  Section 1 mutates nothing.
set -e
cd "$(git rev-parse --show-toplevel)"

echo "############################################################################"
echo "# 1. THE DOCUMENT-GLOBAL ORDINAL, MEASURED — what it would close, what it"
echo "#    would cost, and the mutation it still misses.  Mutates nothing."
echo "############################################################################"
python3 code/state_delegation_repair_bee1/globalpos_bee1.py
echo

echo "############################################################################"
echo "# 2. mg-218d's 16-MUTATION LAYER BATTERY, RE-RUN UNMODIFIED."
echo "#    Not one line of code/state_layer_audit_218d/ is touched by this repair."
echo "############################################################################"
python3 code/state_layer_audit_218d/layers218d.py
echo

echo "############################################################################"
echo "# 3. mg-bee1's OWN 7 MUTATIONS, at the boundary of the new mechanism."
echo "#    Each carries the exit code predicted BEFORE the run.  Three are"
echo "#    predicted silent: they are the stated bound, tested."
echo "############################################################################"
python3 code/state_delegation_repair_bee1/battery_bee1.py
echo

echo "############################################################################"
echo "# 4. THE CONTROL AND ITS OWN DEMONSTRATION — both must still hold."
echo "############################################################################"
python3 code/state_landing_control_2da3/presentation.py > /dev/null && \
    echo "presentation.py self-test: exit 0"
python3 code/state_landing_control_2da3/delta_control.py > /dev/null && \
    echo "delta_control.py on the clean tree: exit 0"
python3 code/state_landing_control_2da3/negative_control.py > /dev/null && \
    echo "negative_control.py: exit 0"
