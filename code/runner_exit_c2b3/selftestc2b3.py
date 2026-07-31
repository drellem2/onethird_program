"""mg-c2b3 self-test -- the classifier, driven in BOTH SENSES at every rule.

A census of runners is itself a runner-shaped artifact, and the thing it is
counting is "a check that prints a failure and reports success".  So every rule
below is exercised twice: once on input it must flag, once on input it must
leave alone.  A classifier only ever fed things it should flag is the same
instrument as a gate only ever fed things that pass.

It exits 1 if any row is bad, and `run_all.sh` reads that status without a
pipeline in the way -- which is the defect this whole tree is about, applied to
this tree.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libc2b3 as L

BAD = 0
N = 0


def ck(desc, got, want=True):
    global BAD, N
    N += 1
    ok = (got == want)
    BAD += (not ok)
    print("  %-4s %s" % ("ok" if ok else "BAD", desc))
    if not ok:
        print("       wanted %r, got %r" % (want, got))


L.bar("selftestc2b3 -- the classifier in both senses")
print()

# ---------------------------------------------------------------------------
print("A.  strip_comment -- a `#` opens a comment only at a word start,")
print("    outside quotes.  Both sides of each clause.")
print()
ck("bare trailing comment is removed",
   L.strip_comment("python3 x.py   # was tee").strip(), "python3 x.py")
ck("a `#` mid-word is NOT a comment",
   L.strip_comment("echo a#b").strip(), "echo a#b")
ck("a `#` inside double quotes is NOT a comment",
   L.strip_comment('echo "a # b"').strip(), 'echo "a # b"')
ck("a `#` inside single quotes is NOT a comment",
   L.strip_comment("echo 'a # b'").strip(), "echo 'a # b'")
ck("a whole-line comment becomes empty",
   L.strip_comment("   # NOT `| tee`").strip(), "")

print()
print("B.  strip_quoted blanks quoted CONTENT and keeps the length, so a")
print("    pipeline named inside a string is not a pipeline.")
print()
ck("quoted content is blanked",
   "tee" in L.strip_quoted('echo "x | tee y"'), False)
ck("unquoted content survives",
   "tee" in L.strip_quoted("x | tee y"), True)
ck("length is preserved (column numbers still line up)",
   len(L.strip_quoted('echo "x | tee y"')), len('echo "x | tee y"'))

print()
print("C.  tee_pipelines -- the census rule itself.  The BAD sense of this")
print("    rule is the ticket's own: its bare grep counted six comments.")
print()
ck("a real pipeline is found",
   L.tee_pipelines("python3 a.py | tee out.txt"), [(1, "python3 a.py | tee out.txt")])
ck("a comment ABOUT a pipeline is not",
   L.tee_pipelines("# NOT `python3 a.py | tee out.txt`, and that is deliberate"), [])
ck("a trailing comment about a pipeline is not",
   L.tee_pipelines("python3 a.py > out.txt   # used to be | tee out.txt"), [])
ck("a quoted pipeline is not",
   L.tee_pipelines('echo "build it with x | tee y"'), [])
ck("`| teeny` is not `| tee` (word boundary)",
   L.tee_pipelines("python3 a.py | teeny out.txt"), [])
ck("a BACKSLASH CONTINUATION is joined before the scan",
   len(L.tee_pipelines("python3 a.py \\\n    | tee out.txt")), 1)
ck("...and reported at the line the command STARTS on",
   L.tee_pipelines("python3 a.py \\\n    | tee out.txt")[0][0], 1)

print()
print("D.  grep_tee is the ticket's bare pattern, kept deliberately.  It must")
print("    DISAGREE with tee_pipelines on a comment -- that disagreement is")
print("    the finding k1 reports, so a self-test that did not check it would")
print("    let the two silently converge.")
print()
_c = "# NOT `python3 a.py | tee out.txt`"
ck("bare grep matches the comment", len(L.grep_tee(_c)), 1)
ck("the parser does not", len(L.tee_pipelines(_c)), 0)
_p = "python3 a.py | tee out.txt"
ck("they agree on a real pipeline",
   len(L.grep_tee(_p)) == len(L.tee_pipelines(_p)) == 1, True)

print()
print("E.  set -e / pipefail detection, both senses.")
print()
ck("`set -e` is found", L.has_set_e("#!/bin/sh\nset -e\n"), True)
ck("`set -eu` is found", L.has_set_e("set -eu\n"), True)
ck("a COMMENTED `set -e` is not", L.has_set_e("# set -e\n"), False)
ck("prose mentioning set -e is not",
   L.has_set_e("# a pipeline under set -e cannot see it\n"), False)
ck("`set -o pipefail` is found", L.has_pipefail("set -o pipefail\n"), True)
ck("a bare `set -e` is not pipefail", L.has_pipefail("set -e\n"), False)

print()
print("F.  guarded() -- does an explicit construct catch the status?")
print()
ck("`|| { exit 1; }` guards",
   L.guarded("python3 a.py > o.txt || { echo bad; exit 1; }"), True)
ck("`X=$(cmd) || {...}` guards",
   L.guarded("E2OUT=$(python3 e2.py) || {"), True)
ck("`if cmd; then` guards", L.guarded("if git rev-parse; then"), True)
ck("a bare redirect does NOT guard",
   L.guarded("python3 a.py > o.txt"), False)
ck("a bare pipeline does NOT guard",
   L.guarded("python3 a.py | tee o.txt"), False)

print()
print("G.  invocations() -- what a line launches, for k4's stubbing.")
print()
ck("plain python3", L.invocations("python3 a1.py | tee o.txt"),
   [("python3", "a1.py")])
ck("flags are skipped", L.invocations("python3 -B -u a1.py > o.txt"),
   [("python3", "a1.py")])
ck("`sh ./x.sh` is seen", L.invocations("sh ./b0.sh | tee o.txt"),
   [("sh", "./b0.sh")])
ck("a relative sibling path survives",
   L.invocations("E2OUT=$(python3 ../d633/e2.py) || {"),
   [("python3", "../d633/e2.py")])
ck("an argument is not mistaken for the script",
   L.invocations("python3 audit_spectrum.py 40 | tee o.txt"),
   [("python3", "audit_spectrum.py")])

print()
print("H.  THE GENERAL FORM, ON THIS TREE.  This deliverable is a script that")
print("    reports on scripts, so it can discard its own verdict exactly as")
print("    its subjects did.  Its own runner is classified by its own rules.")
print()
_self = L.read("code/runner_exit_c2b3/run_all.sh")
ck("this tree's run_all.sh has no `| tee` pipeline",
   L.tee_pipelines(_self), [])
ck("...and `set -e` is set, so an unguarded failure aborts it",
   L.has_set_e(_self), True)
_unguarded = [(n, t) for n, t in L.logical_lines(_self)
              if L.invocations(t) and not L.guarded(t)
              and not t.strip().startswith("#")]
ck("every command it launches is inside an explicit guard",
   _unguarded, [])
print("    (the branch that cannot exhibit the defect, with its reason: this")
print("     runner contains NO pipeline at all, so there is no last-command")
print("     status for a first-command status to hide behind.  That is a")
print("     stronger statement than `set -e is set`, and it is the one the")
print("     row above measures.)")

print()
L.bar("selftestc2b3 TOTAL BAD: %d   (of %d rows)" % (BAD, N))
print()
print("EXTENT.  These %d rows range over libc2b3's five public rules" % N)
print("(strip_comment, strip_quoted, tee_pipelines, has_set_e/has_pipefail,")
print("guarded, invocations) and over THIS TREE'S OWN run_all.sh.  They do")
print("NOT range over the 64 runners in the repository -- that is k1's job,")
print("and k1's numbers are only as good as these rows.")
sys.exit(1 if BAD else 0)
