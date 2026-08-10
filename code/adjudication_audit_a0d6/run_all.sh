#!/bin/sh
# mg-a0d6 — the independent audit of the mg-d19f adjudication.
#
# Four arms, in order.  a1 is the long one (~60 s: it enumerates all 96428 naturally
# labelled posets on [7] and certifies every route-(F) verdict exactly).  a2 reads a1's
# transcript, so the order matters.
#
# NO `| tee`.  `set -e` reads the exit status of the LAST command in a pipeline, so
# `python3 arm.py | tee out.txt` reports tee's success and swallows the arm's failure —
# mg-9876 indexed 18 live sites of exactly that in this corpus and mg-f8e5's d5 is the
# same defect.  Each arm therefore redirects, its status is captured explicitly, and the
# transcript is printed afterwards.
cd "$(dirname "$0")" || exit 1

fail=0
for pair in \
    "a0_selftest.py|forced arms and planted worlds" \
    "a1_ground_truth.py|the re-derivation (this is the long one)" \
    "a2_sites.py|the three sites, the surviving site, and what was struck" \
    "a3_scope.py|scope: was THREE the right number?" \
    "a4_selfcheck.py|independence, non-vacuity, containment"
do
    script=${pair%%|*}
    label=${pair#*|}
    out="out_$(basename "$script" .py).txt"
    printf '\n### %s — %s\n' "$script" "$label"
    python3 "$script" > "$out" 2>&1
    status=$?
    cat "$out"
    if [ "$status" -ne 0 ]; then
        printf '\n*** %s EXITED %d ***\n' "$script" "$status"
        fail=1
        break
    fi
done

if [ "$fail" -ne 0 ]; then
    echo
    echo "RUN FAILED."
    exit 1
fi

echo
echo "ALL ARMS GREEN — see README.md for the verdict."
