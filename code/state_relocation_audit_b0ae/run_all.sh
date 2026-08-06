#!/usr/bin/env bash
# mg-b0ae — INDEPENDENT AUDIT of the mg-ea0e STATE.md relocation.
#
# Run from the repo root:  bash code/state_relocation_audit_b0ae/run_all.sh
#
# The audited object is pinned in libb0ae.py (OLD_REV=78ae4d9, NEW_REV=cc4c663) rather than
# resolved from HEAD, because HEAD moves and the object under audit does not.  Every script
# reads its inputs through `git show <rev>:<path>`, so a dirty working tree cannot change a
# result -- with ONE deliberate exception, B6's blast-radius scan, which is about the repo as
# it stands.
#
# Each script exits non-zero on its own failure; this runner reports every section's status
# rather than stopping at the first, because a suite that stops early cannot tell you whether
# the later checks would have been red too.  mg-2de0 recorded a runner reporting exit 0
# having executed nothing; the per-section byte counts below are this suite's guard against
# the same thing.

set -u
cd "$(dirname "$0")/../.."
OUT="code/state_relocation_audit_b0ae"
export PYTHONPATH="$OUT:${PYTHONPATH:-}"

rc_all=0
for s in b1_bytes b2_coverage b3_markers b4_prefix_math b5_ids b6_process b7_orphan b8_findability; do
    printf '\n### %s\n' "$s"
    python3 "$OUT/$s.py" > "$OUT/out_$s.txt" 2>&1
    rc=$?
    n=$(wc -c < "$OUT/out_$s.txt" | tr -d ' ')
    if [ "$rc" -ne 0 ]; then rc_all=1; fi
    if [ "$n" -lt 500 ]; then
        echo "  EMPTY-TRANSCRIPT GUARD: $s wrote only $n bytes -- treated as a FAILURE"
        rc_all=1
    fi
    printf '  exit %d, %s bytes -> %s\n' "$rc" "$n" "$OUT/out_$s.txt"
    tail -1 "$OUT/out_$s.txt"
done

printf '\n### SUITE RESULT: %s\n' "$([ $rc_all -eq 0 ] && echo 'every section ran' || echo 'A SECTION FAILED')"
exit $rc_all
