"""G5 -- FLOOR, NOT SCOPE: THE FOURTH SPECIES RUNNER.

Nothing in mg-6ef4's ticket or in mg-4adb's names `code/species_7d75/
run_all.sh`.  It is the fourth species runner.  mg-4adb's P3h used its exit 0
as evidence that the repair does not redden a clean tree, and it is in NO
deletion population in this arc, mg-4adb's included.

The question this audit asks of it is the one the ticket asks of the other
three: CAN IT GO RED?  And the answer has two halves that are usually
conflated -- red for a CRASH, and red for a FINDING.

  G5a  every script the runner calls, and how each one ends, from the source
  G5b  those scripts run standalone
  G5c  the runner's last command, read from the source
  G5d  a step replaced by a stand-in that reports a finding and exits 0
  G5e  a step forced to exit 1
  G5f  the same question asked of the three repaired runners, for contrast

    python3 code/species_gate_audit_d53d/g5_fourth.py
"""

import ast
import os
import re
import sys

from kern_d53d import (hdr, Rows, FOURTH, RUNNERS, clone, run_runner,
                       run_script, read_lines, write_lines, source_lines,
                       cleanup)

R = Rows()
base = clone()
REL = os.path.join("code", FOURTH, "run_all.sh")


# ---------------------------------------------------------------------------
hdr("G5a  EVERY SCRIPT THE RUNNER CALLS, AND HOW IT ENDS")
# ---------------------------------------------------------------------------

R.note("  Asked of the PARSED SOURCE, not of a sample of runs: `ast` finds")
R.note("  every call to sys.exit / exit / os._exit in the file, and the last")
R.note("  top-level statement is read directly.  A checker that ends in an")
R.note("  unconditional `sys.exit(0)` returns 0 whatever it computed, so its")
R.note("  own TOTAL BAD cannot reach the runner.")
print()

lines = source_lines(base, REL)
called = []
for ln in lines:
    m = re.match(r"^python3\s+(\S+\.py)", ln.strip())
    if m:
        called.append(m.group(1))
R.note("  scripts the runner calls, in order: %s" % ", ".join(called))
print()


def exit_calls(tree):
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        name = (f.attr if isinstance(f, ast.Attribute)
                else getattr(f, "id", None))
        if name in ("exit", "_exit"):
            arg = None
            if node.args:
                try:
                    arg = ast.literal_eval(node.args[0])
                except Exception:            # noqa: BLE001
                    arg = "<expression>"
            out.append((node.lineno, arg))
    return out


verdict = {}
for name in called:
    path = os.path.join(base, "code", FOURTH, name)
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    tree = ast.parse(src)
    calls = exit_calls(tree)
    last = tree.body[-1] if tree.body else None
    last_is_exit0 = False
    if isinstance(last, ast.Expr) and isinstance(last.value, ast.Call):
        c = exit_calls(ast.Module(body=[last], type_ignores=[]))
        last_is_exit0 = bool(c) and c[0][1] == 0
    unconditional = last_is_exit0 and len(calls) == 1
    verdict[name] = unconditional
    R.note("    %-24s %d exit call(s) %-22s last top-level statement is "
           "`sys.exit(0)`: %-4s  UNCONDITIONAL EXIT 0: %s"
           % (name, len(calls),
              "(" + ", ".join("line %d -> %s" % c for c in calls) + ")",
              "yes" if last_is_exit0 else "no",
              "YES" if unconditional else "no"))

n_uncond = sum(1 for v in verdict.values() if v)
not_uncond = sorted(k for k, v in verdict.items() if not v)
R.predicted(
    "Q21",
    "6 of the 7 (t1..t6) end in an unconditional sys.exit(0) and contain no "
    "other exit; selftest.py is the one that does not",
    "%d of %d; the exception(s): %s"
    % (n_uncond, len(called), ", ".join(not_uncond) or "(none)"),
    len(called) == 7 and n_uncond == 6 and not_uncond == ["selftest.py"])


# ---------------------------------------------------------------------------
hdr("G5b  THOSE SCRIPTS RUN STANDALONE")
# ---------------------------------------------------------------------------

R.note("  The source says what they return.  This runs them and reads it.")
print()

standalone = []
for name in called:
    if not verdict[name]:
        continue
    rc, out = run_script(base, os.path.join("code", FOURTH, name))
    tot = [ln.strip() for ln in out.splitlines() if "TOTAL BAD" in ln]
    standalone.append((name, rc, tot))
    R.note("    %-24s exit %-4s %s" % (name, rc, "; ".join(tot)[:56]))

R.predicted(
    "Q22", "exit 0, 6 of 6, whatever TOTAL BAD they print",
    "%d of %d exit 0" % (sum(1 for _n, rc, _t in standalone if rc == 0),
                         len(standalone)),
    len(standalone) == 6 and all(rc == 0 for _n, rc, _t in standalone))


# ---------------------------------------------------------------------------
hdr("G5c  THE RUNNER's LAST COMMAND")
# ---------------------------------------------------------------------------

R.note("  A POSIX script's exit status is its LAST COMMAND's.  That sentence")
R.note("  is the whole of mg-4adb's repair: it moved the gate to the end of")
R.note("  the three runners so the CALL carries e2's status out of the file.")
R.note("  So the question for a fourth runner is simply: what is its last")
R.note("  command?")
print()

last_cmd = lines[-1]
R.note("    line %d, the last line of %s:" % (len(lines), REL))
R.note("        %s" % last_cmd)
is_grep = last_cmd.strip().startswith("grep ")
R.predicted(
    "Q23",
    "`grep -h \"TOTAL BAD\" out_t*.txt` -- not a checker call, so the rung "
    "mg-4adb installed in three runners is absent from the fourth",
    "`%s` -- %s" % (last_cmd.strip(),
                    "a grep, not a checker call" if is_grep
                    else "not a grep"),
    is_grep and "TOTAL BAD" in last_cmd)

R.note("")
R.note("  And `grep` exits 0 when it MATCHES.  It matches `TOTAL BAD` whatever")
R.note("  number follows, so the higher the battery's findings the more")
R.note("  certainly this runner exits 0.  G5d constructs that.")


# ---------------------------------------------------------------------------
hdr("G5d  A STEP THAT REPORTS A FINDING AND EXITS 0")
# ---------------------------------------------------------------------------

R.note("  The stand-in prints exactly what the real script prints for a")
R.note("  non-zero count and returns exactly what the real script returns for")
R.note("  ANY count -- because the real script's last statement is an")
R.note("  unconditional `sys.exit(0)`, which G5a read out of its source.  So")
R.note("  this is not a weakened checker: it is the checker's own contract.")
print()

keep = list(lines)
i = next(i for i, ln in enumerate(lines) if ln.startswith("python3 t1_"))
lines[i] = ("python3 -c \"print('T1 TOTAL BAD: 7')\"        "
            "> out_t1_grading.txt")
write_lines(base, REL, lines + [""])
try:
    rc_d, out_d = run_runner(base, FOURTH)
finally:
    write_lines(base, REL, keep + [""])

printed = [ln.strip() for ln in out_d.splitlines() if "TOTAL BAD: 7" in ln]
R.note("    the runner exits %s" % rc_d)
for ln in printed:
    R.note("    and its own output says: %s" % ln)
R.predicted(
    "Q24",
    "the runner exits 0 while its own output prints `TOTAL BAD: 7`",
    "exit %s; `TOTAL BAD: 7` printed %d time(s)" % (rc_d, len(printed)),
    rc_d == 0 and bool(printed))

if rc_d == 0 and printed:
    R.row("code/%s/run_all.sh cannot go red over a finding its own battery "
          "makes" % FOURTH, False,
          "This is mg-6ef4's F3 in the one runner mg-4adb did not repair, and\n"
          "it is a WIDER failure than F3 was: there the finding reached the\n"
          "runner and the runner dropped it, here no checker in the battery\n"
          "can return anything but 0 by construction.  This arc has already\n"
          "found and repaired exactly this defect once -- `w3_scope.py`'s own\n"
          "comment records it: 'mg-a4ef: this was `sys.exit(0)`\n"
          "unconditionally' -- in a tree three directories away.")


# ---------------------------------------------------------------------------
hdr("G5e  A STEP FORCED TO EXIT 1")
# ---------------------------------------------------------------------------

R.note("  The distinction that matters: this runner CAN go red.  It goes red")
R.note("  for a CRASH.  `set -e` is at its top and every step is a bare")
R.note("  command, so a step that dies aborts the file.  What it cannot do is")
R.note("  go red for a FINDING, because no step ever returns one.")
print()

keep = list(lines)
lines = source_lines(base, REL)
lines[i] = ("python3 -c \"import sys; sys.exit(1)\"        "
            "> out_t1_grading.txt")
write_lines(base, REL, lines + [""])
try:
    rc_e, out_e = run_runner(base, FOURTH)
finally:
    write_lines(base, REL, keep + [""])
R.note("    the runner exits %s" % rc_e)
R.predicted(
    "Q25", "the runner exits 1 -- it can go red for a crash, and that is the "
           "distinction",
    "exit %s" % rc_e, rc_e == 1)


# ---------------------------------------------------------------------------
hdr("G5f  THE SAME QUESTION ASKED OF THE THREE REPAIRED RUNNERS")
# ---------------------------------------------------------------------------

R.note("  A finding about the fourth runner is worth what the contrast is")
R.note("  worth, so the same two properties are read off the other three.")
print()

for rn in RUNNERS + [FOURTH]:
    rel = os.path.join("code", rn, "run_all.sh")
    ls = source_lines(base, rel)
    last = ls[-1].strip()
    kind = ("a checker call" if last.startswith("python3 ")
            else "a %s" % last.split()[0])
    R.note("    %-26s last command: %-52s (%s)"
           % (rn, last[:52], kind))

R.note("")
R.note("  Three of the four end in the call whose exit code is the finding.")
R.note("  The fourth ends in a `grep` that matches the finding's own text.")

R.tail("G5")
print()
print("EXTENT OF THAT NUMBER.  It ranges over the 7 scripts")
print("code/%s/run_all.sh calls, parsed with `ast`; %d of them run"
      % (FOURTH, len(standalone)))
print("standalone; 2 step substitutions in that runner; and the last line of")
print("4 runner files.  IT RANGES OVER NOTHING ELSE.  In particular G5a asks")
print("`does this file end in an unconditional sys.exit(0) and contain no")
print("other exit` and NOT `can this file ever return non-zero`: an uncaught")
print("exception returns 1 from any of them, which is precisely what G5e")
print("measures and is why the finding is stated as `cannot go red over a")
print("FINDING` and not as `cannot go red`.  The other 100 directories under")
print("code/ have runners too and none of them is in this number.")

cleanup()
sys.exit(1 if R.bad else 0)
