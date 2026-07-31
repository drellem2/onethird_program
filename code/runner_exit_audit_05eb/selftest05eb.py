"""S -- the classifier, driven in BOTH senses at every rule, plus this tree's own
runner checked by this tree's own rules.

A parser that only ever sees inputs it should accept has not been tested; it has
been demonstrated.  Every rule below is given an input it must accept AND an
input it must reject, and the rejecting half is the half that catches the defect
in `libc2b3.PIPEFAIL_RE` that J1e reports.
"""

import ast
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib05eb as L

BAD = 0
N = 0
HERE = os.path.dirname(os.path.abspath(__file__))


def ck(label, got, want):
    global BAD, N
    N += 1
    ok = got == want
    if not ok:
        BAD += 1
    print("  [%s] %-64s got %r" % ("ok " if ok else "BAD", label, got))


L.bar("S  SELF-TEST -- every rule in both senses")

# ---------------------------------------------------------------------------
L.hdr("S1  command_lines -- comments are not commands, commands are")

T = "#!/bin/sh\n# python3 x.py | tee out.txt\n\npython3 x.py > out.txt\n"
# Line 1 is the SHEBANG, and by this rule a shebang is a comment: it starts
# with `#`.  That is correct and it is worth stating, because my first draft
# of this check expected [1, 4] and the parser was right.
ck("only line 4 is a command: shebang and comment are not",
   [i for i, _l in L.command_lines(T)], [4])
ck("an indented comment is not a command line",
   L.command_lines("    # hi\ncmd\n"), [(2, "cmd")])
ck("a blank line is not a command line", L.command_lines("\n\ncmd\n"),
   [(3, "cmd")])

# ---------------------------------------------------------------------------
L.hdr("S2  tee_pipelines -- both senses")

ck("IN : a real pipeline is found",
   [i for i, _l in L.tee_pipelines("python3 x.py | tee out.txt\n")], [1])
ck("IN : `|tee` with no space is found",
   [i for i, _l in L.tee_pipelines("python3 x.py |tee out.txt\n")], [1])
ck("IN : `| tee -a` is found",
   [i for i, _l in L.tee_pipelines("python3 x.py | tee -a out.txt\n")], [1])
ck("OUT: a comment saying `| tee` is NOT a pipeline",
   L.tee_pipelines("# NOT `python3 x.py | tee out.txt`\n"), [])
ck("OUT: `||` is not a pipe",
   L.tee_pipelines("cmd > f || { echo teeny; exit 1; }\n"), [])
ck("OUT: the word `tee` alone is not a pipeline",
   L.tee_pipelines("echo tee\n"), [])
ck("OUT: `| teexyz` is not `tee`",
   L.tee_pipelines("cmd | teexyz f\n"), [])

# ---------------------------------------------------------------------------
L.hdr("S3  bare_grep_tee -- the TICKET's instrument, which must be laxer")

ck("the bare grep DOES count a comment (that is the disagreement)",
   [i for i, _l in L.bare_grep_tee("# NOT `x.py | tee out.txt`\n")], [1])
ck("...and my parser does not, on the same bytes",
   L.tee_pipelines("# NOT `x.py | tee out.txt`\n"), [])
ck("the bare grep finds nothing where there is nothing",
   L.bare_grep_tee("cmd > f\n"), [])

# ---------------------------------------------------------------------------
L.hdr("S4  has_set_e / has_pipefail -- both senses, including the combined form")

ck("IN : `set -e`", L.has_set_e("set -e\n"), True)
ck("IN : `set -eu`", L.has_set_e("set -eu\n"), True)
ck("IN : `set -euo pipefail`", L.has_set_e("set -euo pipefail\n"), True)
ck("IN : `set -o errexit`", L.has_set_e("set -o errexit\n"), True)
ck("OUT: absent", L.has_set_e("cd x\n"), False)
ck("OUT: `# set -e` in a comment", L.has_set_e("# set -e\n"), False)

ck("IN : `set -o pipefail`", L.has_pipefail("set -o pipefail\n"), True)
ck("IN : `set -euo pipefail` -- THE COMBINED FORM.  This is the case",
   L.has_pipefail("set -euo pipefail\n"), True)
ck("     `libc2b3.PIPEFAIL_RE` cannot match, and it is the whole of J1e",
   bool(re.compile(r"^\s*set\s+-o\s+pipefail").match("set -euo pipefail")),
   False)
ck("OUT: absent", L.has_pipefail("set -e\n"), False)
ck("OUT: a comment about pipefail", L.has_pipefail("# set -o pipefail\n"), False)

# ---------------------------------------------------------------------------
L.hdr("S5  redirect_guard_sites -- and whether the guard cats")

G = ('python3 a.py > out_a.txt || {\n'
     '    cat out_a.txt; echo "a FAILED"; exit 1; }\n'
     'python3 b.py > out_b.txt || { echo "b FAILED"; exit 1; }\n'
     'python3 c.py > out_c.txt\n')
sites = L.redirect_guard_sites(G)
ck("two guarded sites found, the unguarded redirect is not one",
   [(t, c) for _i, t, c in sites],
   [("out_a.txt", True), ("out_b.txt", False)])
ck("OUT: a comment showing the idiom is not a site",
   L.redirect_guard_sites("# python3 a.py > out_a.txt || { cat out_a.txt; }\n"),
   [])

# ---------------------------------------------------------------------------
L.hdr("S6  THIS TREE, CHECKED BY THIS TREE'S OWN RULES")

runner = L.read("code/runner_exit_audit_05eb/run_all.sh") \
    if os.path.exists(os.path.join(L.REPO,
                                   "code/runner_exit_audit_05eb/run_all.sh")) \
    else open(os.path.join(HERE, "run_all.sh")).read()

ck("this runner contains NO `| tee` pipeline", L.tee_pipelines(runner), [])
ck("IN : the any-pipeline rule DOES see a real pipe",
   [i for i, _l in L.any_pipelines("cmd | wc -l\n")], [1])
ck("OUT: a `\\|` alternation inside single quotes is NOT a pipe",
   L.any_pipelines("grep -h 'A\\|B' f.txt || true\n"), [])
ck("OUT: `||` is not a pipe", L.any_pipelines("a || b\n"), [])
ck("this runner contains NO pipeline of ANY kind -- the branch that "
   "cannot exhibit the defect", L.any_pipelines(runner), [])
ck("this runner sets `set -e`", L.has_set_e(runner), True)
ncat = [t for _i, t, c in L.redirect_guard_sites(runner) if not c]
ck("every step in this runner is a redirect with a guard that CATS, so a "
   "failing section prints", ncat, [])
nsteps = len(L.redirect_guard_sites(runner))
ck("...and there are 4 such steps (j1..j4) plus the self-test = 5",
   nsteps, 5)

# ---------------------------------------------------------------------------
L.hdr("S7  THE INSTRUMENTS THEMSELVES -- no shell, therefore no pipeline")

print("  Parsed, not grepped.  A grep for the string `shell=True` scores this")
print("  file BAD for the sentence you are reading, and scored four files BAD")
print("  on its first run for saying in a docstring that they do not use it.")
print("  That is the header-comment-counted-as-a-pipeline error, committed by")
print("  the instrument that exists to report it, so the rule now reads the")
print("  SYNTAX TREE: a `shell=` keyword on a real call, and a real call to")
print("  `os.system`.  Both senses are driven below.")
print()


def shells(src):
    """(shell= keywords on real calls, os.system calls) in parsed code."""
    tree = ast.parse(src)
    sh = 0
    osys = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if any(k.arg == "shell" for k in node.keywords):
            sh += 1
        f = node.func
        if isinstance(f, ast.Attribute) and f.attr == "system" and \
                isinstance(f.value, ast.Name) and f.value.id == "os":
            osys += 1
    return sh, osys


ck("IN : the rule DOES see a real `shell=True` call",
   shells("import subprocess\nsubprocess.run('ls', shell=True)\n"), (1, 0))
ck("IN : the rule DOES see a real `os.system` call",
   shells("import os\nos.system('ls')\n"), (0, 1))
ck("OUT: a docstring naming both constructs is not either of them",
   shells('"""we never use shell=True and never call os.system(x)."""\n'),
   (0, 0))

for f in sorted(os.listdir(HERE)):
    if not f.endswith(".py"):
        continue
    src = open(os.path.join(HERE, f)).read()
    ck("%-24s no `shell=` and no `os.system` call" % f, shells(src), (0, 0))

print()
L.bar("S TOTAL BAD: %d   (checks: %d)" % (BAD, N))
print()
print("EXTENT.  These %d checks range over the seven rules in `lib05eb.py`," % N)
print("each driven with an input it must accept and an input it must reject,")
print("over this tree's own `run_all.sh` bytes, and over every `.py` in this")
print("directory for the two constructs that could reintroduce a shell.  They")
print("do NOT range over the correctness of the JUDGEMENTS in j1-j4 -- those")
print("are measurements, and each states its own extent.")
sys.exit(1 if BAD else 0)
