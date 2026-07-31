"""The classifier, driven in BOTH SENSES at every rule.

A rule exercised only on cases it should accept is not tested, it is
demonstrated.  Every check below comes in pairs: something the rule must find
and something it must not, and the second half is where every defect in this
arc's instruments has actually been.

The fixtures are STRINGS.  Nothing here is executed, so no exit status exists
to be discarded -- which is the branch of this file that cannot exhibit the
defect under repair, with the reason.

Section S9 is the one exception: it runs `/bin/sh` on two four-line scripts to
establish, on this machine rather than from POSIX prose, that `n=$(cmd)` under
`set -e` DOES abort and `n=$(cmd | wc -c)` does NOT.  That pair is the entire
justification for `lib7522.guarded` refusing to treat an assignment as a guard,
and a rule this repair depends on is measured and not cited.
"""

import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib7522 as L

HERE = os.path.dirname(os.path.abspath(__file__))
TREE = "code/runner_exit_repair_7522"
N = 0
BAD = 0


def ck(what, got, want):
    global N, BAD
    N += 1
    ok = got == want
    if not ok:
        BAD += 1
    print("  %-4s %-62s %s" % ("ok" if ok else "BAD", what,
                               "" if ok else "got %r want %r" % (got, want)))


L.bar("SELFTEST mg-7522 -- every rule driven in both senses")

# ---------------------------------------------------------------------------
L.hdr("S1  command_lines -- a comment is not a command")

ck("a plain command is a command line",
   [l for _i, l in L.command_lines("python3 x.py > f\n")], ["python3 x.py > f"])
ck("a comment mentioning `| tee` is NOT",
   L.command_lines("# NOT `python3 x.py | tee f`\n"), [])
ck("an indented comment is NOT", L.command_lines("    # x | tee f\n"), [])
ck("a blank line is NOT", L.command_lines("\n   \n"), [])
ck("a command with a trailing comment IS",
   len(L.command_lines("python3 x.py > f  # done\n")), 1)

# ---------------------------------------------------------------------------
L.hdr("S2  unquoted / pipelines -- a `|` inside quotes is an argument")

ck("a real pipeline is found", len(L.pipelines("a | b\n")), 1)
ck("`||` is not a pipeline", L.pipelines("a || b\n"), [])
ck("a `\\|` inside single quotes is not",
   L.pipelines("grep -E 'a\\|b' f\n"), [])
ck("a `|` inside double quotes is not",
   L.pipelines('echo "a|b"\n'), [])
ck("a pipeline AND a quoted bar on one line is one pipeline",
   len(L.pipelines("grep -E 'a\\|b' f | tee g\n")), 1)
ck("a `| tee` in a comment is not a pipeline",
   L.pipelines("# python3 x.py | tee f\n"), [])
ck("tee_pipelines finds a real one", len(L.tee_pipelines("a | tee f\n")), 1)
ck("tee_pipelines does not find `| grep`", L.tee_pipelines("a | grep b\n"), [])
ck("the BARE GREP does count the comment (the ticket's rule, reproduced)",
   len(L.bare_grep_tee("# NOT `x | tee f`\n")), 1)

# ---------------------------------------------------------------------------
L.hdr("S3  stages / discarded_stages -- which status the shell throws away")

ck("two stages for one pipe", len(L.stages("a | b\n")), 2)
ck("three stages for two pipes", len(L.stages("a | b | c\n")), 3)
ck("the LAST stage is not discarded",
   [s.strip() for s in L.discarded_stages("a | b | c")], ["a", "b"])
ck("a line with no pipe discards nothing", L.discarded_stages("a b c"), [])

# ---------------------------------------------------------------------------
L.hdr("S4  set -e / guarded / pipefail -- both senses, and the spelling bug")

ck("`set -e` is found", L.has_set_e("set -e\n"), True)
ck("`set -eu` is found", L.has_set_e("set -eu\n"), True)
ck("`set -euo pipefail` is set -e", L.has_set_e("set -euo pipefail\n"), True)
ck("`set -o errexit` is found", L.has_set_e("set -o errexit\n"), True)
ck("a bare `set -u` is NOT set -e", L.has_set_e("set -u\n"), False)
ck("`set -e` inside a comment is NOT", L.has_set_e("# set -e\n"), False)

ck("`cmd || true` is guarded", L.guarded("a | b || true"), True)
ck("`cmd || { ... }` is guarded", L.guarded("a | b || { echo x; }"), True)
ck("an `if` condition is guarded", L.guarded("if a | b; then"), True)
ck("a bare pipeline is NOT guarded", L.guarded("a | b"), False)
ck("`VAR=$(...)` is NOT guarded -- see S9 for why",
   L.guarded("n=$(a | b)"), False)

ck("the OLD rule finds `set -o pipefail`",
   L.has_pipefail("set -o pipefail\n", L.PIPEFAIL_RE_OLD), True)
ck("the OLD rule MISSES `set -euo pipefail` -- the mg-c2b3 defect",
   L.has_pipefail("set -euo pipefail\n", L.PIPEFAIL_RE_OLD), False)
ck("the NEW rule finds `set -o pipefail`",
   L.has_pipefail("set -o pipefail\n"), True)
ck("the NEW rule finds `set -euo pipefail`",
   L.has_pipefail("set -euo pipefail\n"), True)
ck("the NEW rule does not fire on a comment",
   L.has_pipefail("# set -euo pipefail\n"), False)
ck("the NEW rule does not fire on `set -e` alone",
   L.has_pipefail("set -e\n"), False)

ck("shebang read", L.shebang("#!/bin/sh\nset -e\n"), "#!/bin/sh")
ck("no shebang reads as empty", L.shebang("set -e\n"), "")

# ---------------------------------------------------------------------------
L.hdr("S5  invocation / arguments / stage_can_fail")

ck("a python invocation is parsed", L.invocation("python3 a.py | tee f"),
   ("python3", "a.py"))
ck("a `sh` invocation is parsed", L.invocation("sh ./b.sh | tee f"),
   ("sh", "./b.sh"))
ck("a bare `echo` is not an invocation", L.invocation("echo hi | grep x"), None)
ck("arguments stop at the pipe",
   L.arguments("python3 a.py 5 | tee f", "a.py"), ["5"])
ck("arguments stop at a `;`",
   L.arguments("python3 a.py | tee f ; tail -1 f", "a.py"), [])
ck("`echo` cannot fail", L.stage_can_fail(TREE + "/x.sh", "echo hi")[0], False)
ck("`printf` cannot fail",
   L.stage_can_fail(TREE + "/x.sh", "printf x")[0], False)
ck("`git diff` CAN fail",
   L.stage_can_fail(TREE + "/x.sh", "git diff a..b")[0], True)
ck("an assignment prefix is stripped before naming the command",
   "git" in L.stage_can_fail(TREE + "/x.sh", "n=$(git diff a..b")[1], True)
ck("a continuation line says so rather than inventing a command",
   "continued" in L.stage_can_fail(TREE + "/x.sh", "   ")[1], True)

# ---------------------------------------------------------------------------
L.hdr("S6  THIS TREE'S OWN RUNNER, BY THIS TREE'S OWN RULES")

own = L.read("%s/run_all.sh" % TREE, None)
ck("this runner contains no pipeline of any kind", L.pipelines(own), [])
ck("this runner sets -e", L.has_set_e(own), True)
ck("this runner is #!/bin/sh", L.shebang(own), "#!/bin/sh")
ck("every step redirects and guards",
   len(re.findall(r">\s*out_\w+\.txt\s*\|\|\s*\{", own)),
   len(re.findall(r"^python3 ", own, re.M)))
# MENTION vs USE.  The first draft of both checks below was a grep, and both
# failed on this tree's own documentation -- the `shell=True` grep matched the
# sentence saying `shell=True` is never used, and the strength-marker grep
# matched the regex that detects strength markers.  Recorded in OUTCOMES.md,
# not quietly fixed: it is the same defect the arc keeps finding, in the
# instrument built to find it.
allpy = [f for f in sorted(os.listdir(HERE)) if f.endswith(".py")]
uses = []
mentions = 0
for f in allpy + ["run_all.sh"]:
    for i, line, kind in L.strength_lines(L.read("%s/%s" % (TREE, f), None)):
        if kind == "USE":
            uses.append("%s:%d %s" % (f, i, line[:50]))
        else:
            mentions += 1
ck("no file in this tree USES `confirmed exactly` / `byte-identical`",
   uses, [])
print("  ..   %d MENTION(s) of those words -- the regexes that detect them, the"
      % mentions)
print("       assertions of their absence, and quotations of mg-c2b3's own")
print("       wording.  A mention is not an occurrence; counting one as the")
print("       other is the defect this arc keeps finding.")
sh_true = [(f, L.shell_true_sites("%s/%s" % (TREE, f), None))
           for f in allpy]
ck("no file in this tree CALLS with shell=True or os.system",
   [f for f, s in sh_true if s], [])

# ---------------------------------------------------------------------------
L.hdr("S7  THE POPULATION PRIMITIVE TAKES NO NAME ARGUMENT")

lib = L.read("%s/lib7522.py" % TREE, None)
ck("ls_sh's signature is (ref=None)",
   re.search(r"def ls_sh\(ref=None\)", lib) is not None, True)
ck("ls_sh's CODE contains no runner-filename literal (docstring excluded --"
   " it explains why there is none)",
   "run_all.sh" in L.function_code("%s/lib7522.py" % TREE, "ls_sh", None),
   False)
ck("callers() defaults to the current world",
   re.search(r"def callers\(ref=None\)", lib) is not None, True)
ck("read() defaults to the current world",
   re.search(r"def read\(path, ref=None\)", lib) is not None, True)

# ---------------------------------------------------------------------------
L.hdr("S8  THE TWO REPAIRED RUNNERS, BY THESE RULES, AT BOTH REVISIONS")

for r in L.OUTSIDE:
    pre = L.read(r, L.PINNED)
    now = L.read(r, None)
    ck("%s HAD `| tee`" % os.path.basename(os.path.dirname(r)),
       len(L.tee_pipelines(pre)) > 0, True)
    ck("%s has none now" % os.path.basename(os.path.dirname(r)),
       L.tee_pipelines(now), [])
    ck("%s still sets -e" % os.path.basename(os.path.dirname(r)),
       L.has_set_e(now), True)
    ck("%s guards every former site" % os.path.basename(os.path.dirname(r)),
       len(re.findall(r">\s*out_\w+\.txt\s*\|\|\s*\{", now)),
       len(L.tee_pipelines(pre)))
    ck("%s cats each transcript back to stdout"
       % os.path.basename(os.path.dirname(r)),
       len(re.findall(r"^cat out_\w+\.txt", now, re.M)),
       len(L.tee_pipelines(pre)))

# ---------------------------------------------------------------------------
L.hdr("S9  THE SHELL ITSELF -- the rule in `guarded` is MEASURED, not cited")

print("  `lib7522.guarded` refuses to call `VAR=$(...)` a guard.  That is a")
print("  claim about POSIX errexit, and mg-c2b3's own rule said the opposite.")
print("  Both senses are run on `/bin/sh` on this machine:")
print()

d = tempfile.mkdtemp(prefix="mg7522_")
try:
    for name, body, want_rc, want_reached in (
            ("assignment of a failing command aborts",
             'n=$(false)\necho "reached"\n', 1, False),
            ("assignment of a failing PIPELINE does not",
             'n=$(false | wc -c)\necho "reached"\n', 0, True)):
        p = os.path.join(d, "probe.sh")
        with open(p, "w") as fh:
            fh.write("#!/bin/sh\nset -e\n" + body)
        r = subprocess.run(["/bin/sh", "probe.sh"], cwd=d,
                           capture_output=True, text=True)
        ck("%s (exit)" % name, r.returncode, want_rc)
        ck("%s (later step ran)" % name, "reached" in r.stdout, want_reached)
finally:
    import shutil
    shutil.rmtree(d, ignore_errors=True)

print()
print("  So a pipeline inside an assignment is a place where a status is")
print("  consumed and thrown away at the same time, and treating the")
print("  assignment as a guard would have removed three real sites from the")
print("  population.  The rule is measured here and applied in S1.")

# ---------------------------------------------------------------------------
print()
L.bar("selftest: %d assertions, %d failed" % (N, BAD))
print()
print("EXTENT.  These exercise the CLASSIFIER, in both senses at every rule,")
print("plus this tree's own runner and the two repaired runners by those same")
print("rules, plus the one claim about the shell that the population rule")
print("rests on.  They do not exercise the probes' reporting -- S1 to S5 are")
print("their own controls and each carries a TOTAL BAD with its extent.")
sys.exit(1 if BAD else 0)
