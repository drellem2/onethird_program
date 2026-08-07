#!/bin/sh
# mg-407f: INDEPENDENT AUDIT of mg-cf83 -- BY RUNNING IT, not by reading it.
#
#     sh run_all.sh          # ~6 min; a1 clones 4 real repos and runs 9 scripts
#
# Pure Python 3 + git, no third-party packages.
#
# ⚠️ THIS RUNNER CLONES AND BREAKS REMOTES -- ALL INSIDE A TEMPDIR.  It makes
# four real clones, breaks the `origin` URL of two of them AFTER cloning (so
# `origin/main` still resolves and an UNKNOWN is a FAILED FETCH rather than an
# absent ref), and removes the tempdir on exit.  It NEVER touches the source
# repos: it does not fetch, check out, pull, stash, or write in either one.
#
# ⚠️ IT SHARES NO CODE WITH THE SUBJECT.  a1 does not import `lib_f3ff`.  It
# runs mg-cf83's scripts as SUBPROCESSES and greps their REAL stdout.  mg-4d3b's
# F-series began with a `force_fail=True` that returned before `git fetch` was
# ever spawned; a1 puts a `git` SHIM on PATH and asserts the fetch was actually
# spawned and actually exited 128, because an audit verified by a stub
# reproduces the exact mistake it was sent to find.
#
# ⚠️ a2 READS a1's TRANSCRIPT.  Run a1 first (this script does).  a2 classifies
# each idiom site LIVE or LATENT by whether that site's own output appears in
# a1's real ARM B run, so `out_a1_arms.txt` is an INPUT and not just a record.
#
# EXIT: 0 if no check of THIS INSTRUMENT failed.  ⚠️ FINDINGS ABOUT mg-cf83 DO
# NOT SET IT -- a1 reports 6 findings against the subject's sibling scripts and
# still exits 0.  An instrument that exited 1 for successfully finding what it
# was sent to find could not distinguish `the subject has a defect` from `the
# auditor is broken`, and those need different responses.  This is the same rule
# mg-f3ff's own run_all.sh states, kept deliberately.
cd "$(dirname "$0")"

echo "== mg-407f: mg-cf83 run against real broken clones =="
status=0
for s in a1_arms a2_idiom; do
    # stderr goes INTO the transcript: a crash and a fired check are both
    # exit 1, and a transcript keeping only stdout ends mid-section with no
    # reason given.
    python3 "$s.py" > "out_$s.txt" 2>&1 || status=$?
    cat "out_$s.txt"
done

echo
echo "== mg-407f aggregate exit: $status =="
exit "$status"
