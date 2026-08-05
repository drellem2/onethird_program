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
# mg-70c7, on mg-dee4's F3.  There is ONE marker rule now and both directions
# use it, so the first thing this file checks is that identity -- a rule this
# tree applies to its subject and a different one it applies to itself is the
# finding, and it can only be prevented at the object.
#
# THE PINNED NUMBER WAS 9 AND IS NOW 10, and this comment is the whole reason
# rather than a note about an edit.  mg-56dc/T2b found that the merged rule was
# the SUBJECT-facing nine VERBATIM and had therefore DROPPED `proven`, the one
# alternative mg-dee4's own transcript records as `in SELF and not in SUBJECT`.
# mg-bf79 restored it.  This pin went RED on that restoration, WHICH IS THE PIN
# WORKING -- a hardcoded expectation that stays green through a rule change is
# not a pin.
#
# THE AUTHORITY FOR 10 IS NOT THAT THE CODE NOW SAYS 10.  It is mg-dee4's D4
# union, which its `out_a4_superlatives.txt` publishes as
# `9 subject + 1 self-only = 10`, and which
# `code/runner_exit_repair_bf79/out_p3_ruleset.txt` re-derives from mg-dee4's
# own source and checks BEHAVIOURALLY against this rule on 20 probe words: 0
# reached by one and not the other.  Updating a pin to match the code is how a
# pin becomes decoration; updating it to match the finding the code was changed
# to satisfy is what a pin is for, and the two are told apart by whether an
# independent artifact publishes the new number.  One does.
ck("the marker rule S3a points at the SUBJECT has %d alternatives"
   % L.alternatives(L.MARK), L.alternatives(L.MARK), 10)
ck("...and that is mg-dee4's D4 UNION, not the subject's nine verbatim",
   bool(L.MARK.search("proven")), True)
ck("the rule this tree used on ITSELF had 3, and is kept only for exhibition",
   L.alternatives(L.MARK_OLD), 3)
ck("`verified` is IN the rule -- the D4 docstring names it and it was not",
   bool(L.MARK.search("verified against the pre-repair output")), True)
ck("...and was not in the old one", bool(L.MARK_OLD.search("verified")), False)
ck("a marker INSIDE a quoted span is a MENTION, not a USE (mg-70c7)",
   [k for _i, _l, k in L.strength_lines(
       "# `verified against the` is the marker here")], ["MENTION"])
ck("a marker written bare is a USE",
   [k for _i, _l, k in L.strength_lines(
       "the eight counts are identical across 8 arms")], ["USE"])

# The verdict itself is S5d's -- population, backing and all -- and duplicating
# it here would give this tree two answers to one question.  What is pinned
# here is the RULE; what S5d prints is the measurement.
uses = []
mentions = 0
for f in allpy + ["run_all.sh"]:
    for i, line, kind in L.strength_lines(L.read("%s/%s" % (TREE, f), None)):
        if kind == "USE":
            uses.append("%s:%d %s" % (f, i, line[:50]))
        else:
            mentions += 1
print("  ..   %d MENTION(s) and %d USE(s) of those words in this tree's code."
      % (mentions, len(uses)))
print("       A mention is not an occurrence; counting one as the other is the")
print("       defect this arc keeps finding.  Whether a USE is BACKED by a")
print("       transcript of this tree is S5d's question and is answered there,")
print("       over a population that includes the `*.md` this file cannot see.")
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
L.hdr("S10  THE CONSUMPTION CLAUSE -- BOTH ARMS, BOTH SENSES  (mg-70c7)")

print("  mg-dee4's F6: the clause tested ERREXIT and the reason written for it")
print("  was about the VALUE.  It is a named disjunction now, and a")
print("  disjunction is only honest if each arm is pinned in both senses --")
print("  otherwise widening a rule is indistinguishable from breaking it.")
print()
_E = "#!/bin/sh\nset -e\n%s\n"
_U = "#!/bin/sh\nset -u\n%s\n"
_LINE = "n=$(git diff a..b | wc -c | tr -d ' ')"
_BARE = "git diff a..b | wc -c"
ck("errexit arm: `set -e`, unguarded pipeline",
   L.consumed(_E % _BARE, _BARE, 3)[1], "ERREXIT")
ck("errexit arm: no `set -e`, output not captured -> NOT consumed",
   L.consumed(_U % _BARE, _BARE, 3)[0], False)
ck("value arm: no `set -e`, captured AND read",
   L.consumed(_U % (_LINE + '\necho "$n"'), _LINE, 3)[1], "VALUE")
ck("value arm: captured and NEVER read -> NOT consumed",
   L.consumed(_U % _LINE, _LINE, 3)[0], False)
ck("both arms at once are reported as both, not as one",
   L.consumed(_E % (_LINE + '\necho "$n"'), _LINE, 3)[1], "ERREXIT+VALUE")
ck("a guarded pipeline under `set -e` is not consumed by errexit",
   L.consumed(_E % (_BARE + " || true"), _BARE + " || true", 3)[0], False)

# ---------------------------------------------------------------------------
L.hdr("S11  SITE vs EXECUTION -- the grain, pinned in both senses  (mg-70c7)")

print("  mg-dee4's F1: `11 of 11 read directly` counted SOURCE LINES over")
print("  source that runs in loops.  These rows pin the difference, including")
print("  the direction that MUST refuse: a loop this parser cannot expand has")
print("  to say so rather than be counted as one iteration.")
print()
_LOOP = ("#!/bin/sh\nset -e\n"
         'for pair in "a1 dir/one" \\\n            "b2 dir/two"; do\n'
         "    base=${pair%% *}; dir=${pair#* }\n"
         "    n=$(git diff \"$base..HEAD\" -- \"$dir\" | wc -c)\n"
         "done\n")
_ex = L.pipeline_executions(_LOOP)
ck("one pipeline SOURCE LINE inside a 2-item loop is 2 EXECUTIONS",
   len(_ex), 2)
ck("...and the loop body's own assignments are followed into the argv",
   [L.argv_of(L.discarded_stages(t)[0], b) for _i, _n, b, t in _ex],
   [["git", "diff", "a1..HEAD", "--", "dir/one"],
    ["git", "diff", "b2..HEAD", "--", "dir/two"]])
_VAR = ("#!/bin/sh\nset -e\nfor d in $DIRS; do\n"
        "    n=$(git diff x -- \"$d\" | wc -c)\ndone\n")
_exv = L.pipeline_executions(_VAR)
ck("a loop over `$DIRS` is NOT statically expandable and says so",
   [n for _i, n, _b, _t in _exv], [None])
ck("...and no argv is derived for it",
   [b for _i, _n, b, _t in _exv], [None])
ck("a pipeline outside any loop is exactly one execution",
   len(L.pipeline_executions("#!/bin/sh\nset -e\nn=$(a | b)\n")), 1)
ck("an unresolvable `$` never survives into a derived argv",
   L.argv_of('git diff "$nope"', {}), None)
ck("a quoted pathspec survives as its own word",
   L.argv_of('git diff "$b..HEAD" -- "$d" \':!*.md\'',
             {"b": "a1", "d": "dir/one"}),
   ["git", "diff", "a1..HEAD", "--", "dir/one", ":!*.md"])

# ---------------------------------------------------------------------------
L.hdr("S12  IS A FIGURE BACKED BY A TRANSCRIPT?  both senses  (mg-70c7)")

ck("a line number is not a figure -- `s3_figure.py:154` does not back 154",
   L.figures("      s3_figure.py:154  if os.path.basename(p)"), [])
ck("...and a bare 154 in a transcript does", L.figures("  changed 154 files"),
   [154])
ck("0, 1 and 2 are not figures -- they are structural in prose",
   L.figures("both of the 2 arms exit 0 at 1 site"), [])

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
