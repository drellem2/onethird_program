#!/bin/sh
# mg-9134, PART 2 — WHO RUNS `pogo doctor --check` WHEN NOBODY IS TYPING?
#
# mg-7ff8's acceptance condition 2 is "observe it in the context it RUNS in".
# pa518 recorded that the condition IS NOT MET: every measurement of this
# detector — mg-7ff8's, mg-a518's seven mutation arms, and every arm in
# consolidate_9134.py beside this file — is a HAND-RUN.  A hand-run proves the
# detector CAN speak.  It does not prove that the scheduled invocation reaches it
# with the same config, the same store and the same mtimes.
#
# Before waiting for that scheduled invocation it is worth asking whether one
# exists.  THIS SCRIPT ASKS.  It asserts nothing and refuses nothing; it prints
# what every plausible unattended caller on this host actually says, so the
# answer is a transcript a reader can re-derive rather than a sentence of mine.
#
# It reads ONLY host state (launchd, cron, pogo's own scheduler, the pogo source
# tree, agent transcripts).  It changes nothing.  It prints no secret: the
# transcript scan reports timestamps and agent names, never command bodies.

set -u
echo "mg-9134 PART 2 — every unattended path that could run \`pogo doctor --check\`"
echo "=============================================================================="
echo "host date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo
echo "--- 1. THE ONLY CALLER IN THE POGO SOURCE ------------------------------------"
echo "If pogod ran this check itself, there would be an unattended path by"
echo "construction.  Every reference to the check's renderer, tests excluded:"
if [ -d "$HOME/dev/pogo" ]; then
    grep -rn "auditSuccessorLine(" "$HOME/dev/pogo/cmd" "$HOME/dev/pogo/internal" \
        --include='*.go' 2>/dev/null | grep -v _test | sed 's|'"$HOME"'|~|'
else
    echo "  (~/dev/pogo is not present — cannot check)"
fi
echo "  => the definition, and one call site inside \`pogo doctor --check\`."

echo
echo "--- 2. launchd -------------------------------------------------------------"
N=0
for p in "$HOME"/Library/LaunchAgents/com.pogo.*.plist; do
    [ -f "$p" ] || continue
    N=$((N + 1))
    if grep -q "doctor" "$p" 2>/dev/null; then
        echo "  MATCH: $(basename "$p")"
    fi
done
echo "  $N com.pogo.* launch agents scanned; matches printed above (none = none)."

echo
echo "--- 3. cron ----------------------------------------------------------------"
crontab -l 2>&1 | sed 's/^/  /' | head -20

echo
echo "--- 4. pogo's own scheduler -------------------------------------------------"
pogo schedule list 2>/dev/null | grep -ci "doctor" | sed 's/^/  entries mentioning doctor: /'
pogo schedule list 2>/dev/null | wc -l | sed 's/^/  total schedule rows (incl. header): /'

echo
echo "--- 5. host scripts --------------------------------------------------------"
echo "  lines matching 'doctor --check' in ~/.pogo shell scripts:"
grep -rn "doctor --check" "$HOME"/.pogo/bin/*.sh "$HOME"/.pogo/pogo-reminders/bin/*.sh \
    "$HOME"/.pogo/pogo-sleepwake/bin/*.sh 2>/dev/null | sed 's|'"$HOME"'|~|;s/^/    /'
echo "  (nothing listed = no host script invokes it)"

echo
echo "--- 6. THE ONE ROUTINE READER, AND WHETHER IT IS ALIVE ----------------------"
echo "  crew/doctor.md makes it the first-line health check:"
if [ -f "$HOME/dev/pogo/internal/agent/prompts/crew/doctor.md" ]; then
    grep -n "doctor --check" "$HOME/dev/pogo/internal/agent/prompts/crew/doctor.md" | sed 's/^/    /'
fi
echo "  is the doctor agent running?"
pogo agent list 2>/dev/null | grep -i "^doctor" | sed 's/^/    /'
echo "    (nothing listed = not running, not even parked)"
echo "  last agent_stopped event for crew-doctor:"
grep '"agent":"crew-doctor"' "$HOME/.pogo/events.log" 2>/dev/null \
    | grep agent_stopped | tail -1 \
    | sed 's/.*"timestamp":"\([^"]*\)".*"reason":"\([^"]*\)".*/    stopped \1 (reason: \2)/'

echo
echo "--- 7. WHEN DID ANY PROCESS LAST ACTUALLY RUN IT? ---------------------------"
echo "  Tool calls containing 'doctor --check' in agent transcripts, by agent,"
echo "  most recent first.  A polecat or a crew agent typing the command at a"
echo "  human's or a ticket's request is a HAND-RUN however automated it looks;"
echo "  what would count is doctor's own startup checklist."
python3 - <<'PY'
import glob, json, os, time
rows = []
for f in glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl")):
    if os.path.getmtime(f) < time.time() - 30 * 86400:
        continue
    agent = os.path.basename(os.path.dirname(f))
    try:
        with open(f, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if "doctor --check" not in line:
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                msg = rec.get("message") or {}
                cont = msg.get("content")
                if not isinstance(cont, list):
                    continue
                for c in cont:
                    if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("name") == "Bash":
                        cmd = (c.get("input") or {}).get("command", "")
                        # the command must RUN it, not merely mention it
                        if "doctor --check" in cmd and "grep -rn" not in cmd and "grep -rl" not in cmd:
                            rows.append((rec.get("timestamp", ""), agent))
    except Exception:
        pass
rows.sort(reverse=True)
seen = {}
for ts, agent in rows:
    seen.setdefault(agent, [ts, 0])
    seen[agent][1] += 1
for agent, (ts, n) in sorted(seen.items(), key=lambda kv: kv[1][0], reverse=True)[:12]:
    print(f"    {ts}  {n:>4} run(s)  {agent}")
print(f"    ({len(rows)} invocations across {len(seen)} agents, last 30 days of transcripts)")
PY

echo
echo "=============================================================================="
echo "READ THE ABOVE, NOT A CONCLUSION FROM ME.  What it printed on 2026-08-12 is"
echo "recorded in this directory's README under PART 2."
