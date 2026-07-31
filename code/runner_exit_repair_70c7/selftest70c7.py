"""selftest70c7 -- every rule in `lib70c7`, in BOTH senses.

A rule pinned in one sense only cannot tell a widening from a break.  Every
rule below therefore has at least one row that must MATCH and one that must
REFUSE, and the refusing rows are the ones that matter: three of the six
findings this tree repairs are rules that matched too little, and the way a
repair of such a rule goes wrong is by matching everything.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib70c7 as M

N = 0
BAD = 0


def ck(label, got, want):
    global N, BAD
    N += 1
    ok = got == want
    if not ok:
        BAD += 1
    print("  %-4s %-62s" % ("ok" if ok else "FAIL", label))
    if not ok:
        print("       got  %r" % (got,))
        print("       want %r" % (want,))


M.bar("selftest70c7 -- both senses at every rule")

# ---------------------------------------------------------------------------
M.hdr("A.  for_loops -- the literal expansion, and the refusal")

ck("a two-item literal loop expands",
   [(v, i) for v, i, _f, _l in M.for_loops(
       '#!/bin/sh\nfor p in "a" "b"; do\n  echo $p\ndone\n')],
   [("p", ["a", "b"])])
ck("a continuation-joined header is ONE loop with all its items",
   [(v, i) for v, i, _f, _l in M.for_loops(
       '#!/bin/sh\nfor p in "a" \\\n        "b" \\\n        "c"; do\n'
       '  echo $p\ndone\n')],
   [("p", ["a", "b", "c"])])
ck("a loop over `$VAR` REFUSES rather than counting one item",
   [i for _v, i, _f, _l in M.for_loops(
       "#!/bin/sh\nfor p in $DIRS; do\n  echo $p\ndone\n")],
   [None])
ck("a loop over a glob REFUSES too",
   [i for _v, i, _f, _l in M.for_loops(
       "#!/bin/sh\nfor p in code/*.sh; do\n  echo $p\ndone\n")],
   [None])
ck("a file with no loop has none", M.for_loops("#!/bin/sh\necho hi\n"), [])

# ---------------------------------------------------------------------------
M.hdr("B.  pipeline_executions -- SITES are not RUNS")

PIPE = re.compile(r"(?<!\|)\|(?!\|)(?!&)")
_LOOP = ('#!/bin/sh\nfor p in "a" "b" "c"; do\n'
         "  n=$(git diff $p | wc -c)\ndone\n")
ck("one pipeline line in a 3-item loop is 3 executions",
   len(M.pipeline_executions("x.sh", _LOOP, PIPE)), 3)
ck("...and they are numbered 1,2,3",
   [n for _i, n, _b, _t in M.pipeline_executions("x.sh", _LOOP, PIPE)],
   [1, 2, 3])
ck("a pipeline outside any loop is exactly one execution",
   len(M.pipeline_executions("x.sh", "#!/bin/sh\nn=$(a | b)\n", PIPE)), 1)
ck("a COMMENTED pipeline is no execution",
   M.pipeline_executions("x.sh", "#!/bin/sh\n# n=$(a | b)\n", PIPE), [])
ck("a pipeline in an unexpandable loop is one row saying so",
   [n for _i, n, _b, _t in M.pipeline_executions(
       "x.sh", "#!/bin/sh\nfor p in $D; do\n  n=$(a | b)\ndone\n", PIPE)],
   [None])

# ---------------------------------------------------------------------------
M.hdr("C.  expand / argv_of -- and the refusal that matters most")

ck("`${p%% *}` takes the head", M.expand("${p%% *}", {"p": "a1 dir/one"}), "a1")
ck("`${p#* }` takes the tail", M.expand("${p#* }", {"p": "a1 dir/one"}),
   "dir/one")
ck("`$p` is the whole", M.expand("$p", {"p": "x"}), "x")
ck("an unbound name REFUSES", M.expand("$nope", {"p": "x"}), None)
ck("an unimplemented expansion REFUSES",
   M.expand("${p:-default}", {"p": "x"}), None)
ck("a quoted pathspec survives as ONE word",
   M.argv_of('git diff "$b..HEAD" -- "$d" \':!*.md\'',
             {"b": "a1", "d": "dir/one"}),
   ["git", "diff", "a1..HEAD", "--", "dir/one", ":!*.md"])
ck("...and the SAME line without the pathspec is a different argv",
   M.argv_of('git diff "$b..HEAD" -- "$d"', {"b": "a1", "d": "dir/one"}),
   ["git", "diff", "a1..HEAD", "--", "dir/one"])
ck("an assignment prefix is stripped, not classified",
   M.argv_of('n=$(git diff x', {}), ["git", "diff", "x"])
ck("an unresolvable `$` NEVER survives into an argv",
   M.argv_of('git diff "$nope"', {}), None)

# ---------------------------------------------------------------------------
M.hdr("D.  the VALUE arm -- captured AND read, both senses")

ck("a captured pipeline names its variable",
   M.captured_var("n=$(git diff x | wc -c)"), "n")
ck("`local n=$(...)` too", M.captured_var("  local n=$(a | b)"), "n")
ck("a bare pipeline captures nothing",
   M.captured_var("git diff x | wc -c"), None)
ck("a redirect captures nothing",
   M.captured_var("git diff x > f.txt"), None)
ck("`$n` elsewhere counts as a read",
   [i for i, _l in M.var_reads('n=$(a|b)\necho "$n"\n', "n", 1)], [2])
ck("`${n}` counts as a read",
   [i for i, _l in M.var_reads("n=$(a|b)\necho ${n} bytes\n", "n", 1)], [2])
ck("the assignment line itself does NOT count as a read",
   M.var_reads("n=$(a|b)\n", "n", 1), [])
ck("a mention in a COMMENT does not count",
   M.var_reads('n=$(a|b)\n# $n is the count\n', "n", 1), [])
ck("a different variable does not count",
   M.var_reads('n=$(a|b)\necho "$m"\n', "n", 1), [])

# ---------------------------------------------------------------------------
M.hdr("E.  figures -- what is a measurement and what is a label")

ck("a plain count is a figure", M.figures("changed 154 files"), [154])
ck("a LINE REFERENCE is not -- `s3_figure.py:154`",
   M.figures("      s3_figure.py:154  if os.path.basename(p)"), [])
ck("`on line 89` is not either", M.figures("with its figure on line 89"), [])
ck("`lines 37-41` is not", M.figures("at lines 37-41 of the runner"), [])
ck("0, 1 and 2 are structural, not figures",
   M.figures("both arms exit 0 at 1 site of 2"), [])
ck("several figures on one line are all returned",
   M.figures("P2 is 20 files / 27 pipelines"), [20, 27])
ck("a thousands separator is one figure",
   M.figures("699,520 assertions"), [699520])

# ---------------------------------------------------------------------------
M.hdr("F.  alternatives -- 9 against 3 is the whole of F3")

ck("a bare pattern is one alternative", M.alternatives(r"abc"), 1)
ck("two top-level alternatives", M.alternatives(r"a|b"), 2)
ck("a group's inner `|` is NOT a top-level alternative",
   M.alternatives(r"(?:a|b)|c"), 2)
ck("an ESCAPED pipe is not an alternative", M.alternatives(r"a\|b"), 1)
ck("mg-7522's subject-facing rule has 9",
   M.alternatives(r"confirmed exactly|byte-identical|byte for byte|\bverified\b"
                  r"|\(measured\)|\bidentical\b|\bconfirmed\b"
                  r"|\ball (?:\d+|of)\b|\bexactly \d+\b"), 9)
ck("...and the self-facing one it replaced had 3",
   M.alternatives(r"confirmed exactly|byte-identical|\bproven\b"), 3)

# ---------------------------------------------------------------------------
M.hdr("G.  transcript_numbers -- the corpus, and the defect it had")

_tmp = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "_selftest_corpus.txt")
with open(_tmp, "w", encoding="utf-8") as fh:
    fh.write("s3_figure.py:154  a line reference\nchanged 166 files\n")
try:
    rel = "%s/%s" % (M.TREE, os.path.basename(_tmp))
    got = M.transcript_numbers([rel])
    ck("a real figure enters the corpus", 166 in got, True)
    ck("a LINE NUMBER does not -- this is the defect recorded in OUTCOMES",
       154 in got, False)
finally:
    os.unlink(_tmp)

print()
M.bar("selftest70c7: %d assertions, %d failed" % (N, BAD))
print()
print("EXTENT.  These exercise `lib70c7`'s seven rules in both senses.  They do")
print("NOT exercise the probes' reporting -- R1 through R6 are their own")
print("controls and each carries a TOTAL BAD with its own extent -- and they")
print("do not exercise `lib7522`'s copies of the same rules, which")
print("`selftest7522.py` pins in its own S10, S11 and S12.")
sys.exit(1 if BAD else 0)
