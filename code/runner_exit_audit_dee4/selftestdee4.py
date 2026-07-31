"""selftestdee4 -- the classifier in BOTH SENSES at every rule, and this tree
checked for the defects it audits.

A rule that only ever fires is not a rule.  Every predicate in `libdee4.py`
that a finding rests on is driven with an input it MUST see and an input it
MUST NOT, on fixtures that are strings and are never executed.

Then the four defects this audit is about, on this tree's own bytes:

  D1  A POPULATION DEFINED BY A NAME.  `ls_tracked()` takes a `suffixes`
      argument, so unlike `lib7522.ls_sh()` a name filter CAN be applied here.
      That is deliberate -- A1b's whole question is whether `.sh` is a name
      rule, and a primitive that hard-codes the extension cannot ask it.  So
      the check is not "no filter exists"; it is "every call site that passes
      one is enumerated and says why".
  D2  AN ENUMERATION ANCHORED TO A STALE REVISION.  Every anchor passed
      anywhere in this tree is listed with the question it serves.
  D3  A PIPELINE WHOSE STATUS IS DISCARDED.  This tree ships a `run_all.sh`,
      so it is a member of its own population and is run through A1's P2.
  D4  A STRENGTH MARKER STANDING IN FOR A CHECK.  Over EVERY file of this
      tree including the `.md`, because A4b's finding is that mg-7522's
      equivalent check excluded them.
"""

import ast
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libdee4 as L

BAD = 0
HERE = os.path.dirname(os.path.abspath(__file__))
TREE = "code/runner_exit_audit_dee4"
# THE POPULATION OF THIS TREE'S OWN ARTIFACTS.  It includes the PUBLISHED
# DOCUMENT under `docs/`, not only the files in this directory.  That is the
# direct consequence of A4b: mg-7522's equivalent check ranged over its own
# `*.py` and `*.sh` and excluded every `.md`, and the published document is
# exactly the artifact kind mg-05eb's OPEN 2 defect lived in.  A self-check
# that stops at its own directory boundary has a population defined by a path.
DOC_REL = "../../docs/OneThird-RunnerExit-PopulationRepair-Audit.md"
MINE = sorted(f for f in os.listdir(HERE)
              if f.endswith((".py", ".sh", ".md"))) + [DOC_REL]


def ck(label, got, want):
    global BAD
    ok = got == want
    if not ok:
        BAD += 1
    print("  %s  %-62s got %r" % ("ok" if ok else "**", label, got))
    if not ok:
        print("       want %r" % (want,))


L.bar("selftestdee4  BOTH SENSES AT EVERY RULE")

print()
print("S1  `pipelines` -- a real pipe, and the three things that are not one")
ck("IN : a real pipeline", [i for i, _l in L.pipelines("a | b\n")], [1])
ck("OUT: `||` is not a pipe", L.pipelines("a || b\n"), [])
ck("OUT: `|&` is not a pipe", L.pipelines("a |& b\n"), [])
ck("OUT: a `|` inside single quotes is an argument",
   L.pipelines("grep 'A\\|B' f\n"), [])
ck("OUT: a `|` inside double quotes is an argument",
   L.pipelines('grep "A|B" f\n'), [])
ck("OUT: a comment quoting `| tee` is not a pipeline",
   L.pipelines("# x.py | tee out.txt\n"), [])
ck("IN : a pipe after an inline `#` that is not at line start",
   [i for i, _l in L.pipelines("a | b  # note\n")], [1])

print()
print("S2  `tee_pipelines` -- the SHAPE, distinguished from the property")
ck("IN : a real `| tee`", [i for i, _l in L.tee_pipelines("x.py | tee o\n")],
   [1])
ck("OUT: a pipeline that is not a tee",
   L.tee_pipelines("x.py | wc -c\n"), [])
ck("OUT: the word tee not after a pipe",
   L.tee_pipelines("echo tee\n"), [])

print()
print("S3  `has_set_e` -- every spelling that sets it, and one that does not")
for spelling in ("set -e", "set -eu", "set -euo pipefail", "set -o errexit"):
    ck("IN : `%s`" % spelling, L.has_set_e("%s\n" % spelling), True)
ck("OUT: `set -u` alone", L.has_set_e("set -u\n"), False)
ck("OUT: `set -e` inside a comment", L.has_set_e("# set -e\n"), False)

print()
print("S4  `guarded` -- what stops errexit reading a status, and what does not")
ck("IN : `cmd || true`", L.guarded("a | b || true"), True)
ck("IN : `cmd || {`", L.guarded("a | b || { echo x; exit 1; }"), True)
ck("IN : an `if` condition", L.guarded("if a | b; then"), True)
ck("OUT: a bare pipeline", L.guarded("a | b"), False)
ck("OUT: `VAR=$(...)` is NOT guarded -- POSIX gives an assignment-only "
   "command the status of its last substitution",
   L.guarded("n=$(a | b)"), False)

print()
print("S5  `discarded_stages` -- all but the last, in order")
ck("three stages discard two", len(L.discarded_stages("a | b | c")), 2)
ck("one stage discards none", len(L.discarded_stages("a")), 0)
ck("the FIRST stage is first",
   L.discarded_stages("a | b | c")[0].strip(), "a")

print()
print("S6  `stage_can_fail` -- the conservative default, and the exceptions")
ck("OUT: `echo` has no failure mode",
   L.stage_can_fail("code/x/run_all.sh", "echo hi", None)[0], False)
ck("OUT: `printf` likewise",
   L.stage_can_fail("code/x/run_all.sh", "printf x", None)[0], False)
ck("IN : an unknown external command counts as ABLE to fail",
   L.stage_can_fail("code/x/run_all.sh", "frobnicate", None)[0], True)
ck("IN : an assignment prefix is stripped before classifying",
   L.stage_can_fail("code/x/run_all.sh", "n=$(git diff a..b", None)[1],
   "external command `git` can return non-zero")

print()
print("S7  `invocation` -- the interpreter and the script, not the redirect")
ck("IN : python3", L.invocation("python3 a.py | tee o"), ("python3", "a.py"))
ck("IN : sh", L.invocation("sh b.sh | tee o"), ("sh", "b.sh"))
ck("OUT: no interpreter", L.invocation("cat a.py | tee o"), None)

print()
print("S8  `ls_tracked` -- the population primitive, in both directions")
sh = L.ls_tracked(None, (".sh",))
allf = L.ls_tracked(None, ("",))
ck("IN : the suffix filter selects", all(p.endswith(".sh") for p in sh), True)
ck("IN : the empty suffix selects everything", len(allf) > len(sh), True)
ck("OUT: a suffix nothing has", L.ls_tracked(None, (".nope",)), [])
ck("this tree's own `run_all.sh` is in the population",
   "%s/run_all.sh" % TREE in sh, True)

L.hdr("D1  A POPULATION DEFINED BY A NAME -- every filter site, enumerated")

print("  `ls_tracked(ref=None, suffixes=('.sh',))` CAN take a name filter.")
print("  That is on purpose and it is the opposite of mg-7522's structural")
print("  answer, for a stated reason: A1b's question is `is `.sh` itself a")
print("  name rule?` and a primitive that hard-codes `.sh` cannot ask it.")
print("  So the obligation here is enumeration, not absence.  Every call")
print("  site that passes a suffix or tests a basename:")
print()
SITES = []
for f in [x for x in MINE if x.endswith(".py")]:
    src = open(os.path.join(HERE, f), encoding="utf-8").read()
    for i, l in enumerate(src.split("\n"), 1):
        if re.search(r"ls_tracked\(|basename\(|run_all|run_audit|\.sh\"|"
                     r"'\.sh'|TWO_NAMES", l) and not l.strip().startswith("#"):
            SITES.append((f, i, l.strip()))
print("      call sites that name a file kind or a filename: %d" % len(SITES))
DISP = [
    (r"ls_tracked\(None, \(\"\"\,?\)?\)|ls_tracked\(None, \(\"\"\)\)",
     "the NO-filter call -- A1b's population"),
    (r"ls_tracked\(.*\.sh", "the `*.sh` population, measured AGAINST the "
     "no-filter one in A1b"),
    (r"ls_tracked\(.*\.py", "the `*.py` population for A1c's AST walk"),
    (r"ls_tracked\(.*\.nope|ls_tracked\(None, \(\"\.sh\",\)\)",
     "a self-test fixture"),
    (r"basename", "reporting or grouping, not selecting the population"),
    (r"ls_tracked\(\)|takes a `suffixes`",
     "this file's own docstring, explaining why the primitive takes the "
     "argument -- a mention, and the third time in this arc that a rule has "
     "matched the documentation of its own absence"),
    (r"run_all|run_audit|TWO_NAMES",
     "mg-c2b3's or mg-7522's OWN name rule, being measured next to the "
     "property rule"),
    (r"\.sh\"|'\.sh'", "a suffix test inside a rule that is itself the subject"),
]
undisp = [s for s in SITES if not any(re.search(rx, s[2]) for rx, _w in DISP)]
for rx, why in DISP:
    n = len([1 for s in SITES if re.search(rx, s[2])])
    print("      %-4d %s" % (n, why))
ck("every name-filter site has a disposition", len(undisp), 0)
for f, i, l in undisp:
    print("          *** %s:%d  %s" % (f, i, l[:60]))

L.hdr("D2  EVERY ANCHOR IN THIS TREE, WITH THE QUESTION IT SERVES")

ANCH = []
for f in [x for x in MINE if x.endswith(".py")]:
    src = open(os.path.join(HERE, f), encoding="utf-8").read()
    for i, l in enumerate(src.split("\n"), 1):
        if l.strip().startswith("#"):
            continue
        if re.search(r"L\.PINNED|L\.PRE_REPAIR|L\.REPAIR\b|L\.SWEEP|"
                     r"\"HEAD\"|ref=None|, None\)", l):
            ANCH.append((f, i, l.strip()))
print("      anchor uses: %d" % len(ANCH))
kinds = {"census (ref=None / HEAD)": 0, "comparison (a pinned revision)": 0}
for f, i, l in ANCH:
    if re.search(r"L\.PINNED|L\.PRE_REPAIR|L\.REPAIR\b|L\.SWEEP|\"HEAD\"", l):
        kinds["comparison (a pinned revision)"] += 1
    else:
        kinds["census (ref=None / HEAD)"] += 1
for k, v in kinds.items():
    print("      %-34s %3d" % (k, v))
print()
print("  THE DEFAULT.  `ls_tracked`, `read` and `exists` all default to")
print("  `ref=None`, so a census that forgets to think about its anchor gets")
print("  the current world and a comparison has to ask for a revision.")
ck("`ls_tracked` defaults to the current world",
   "def ls_tracked(ref=None" in open(os.path.join(HERE, "libdee4.py")).read(),
   True)

L.hdr("D3  THIS TREE'S OWN `run_all.sh`, THROUGH A1'S OWN P2 PREDICATE")

for name in [x for x in MINE if x.endswith(".sh")]:
    rel = "%s/%s" % (TREE, name)
    src = L.read(rel, None)
    ps = L.pipelines(src)
    p2 = L.p2_pipelines(rel, None)
    print("      %-16s set -e: %-4s pipelines: %d   in P2: %d"
          % (name, "yes" if L.has_set_e(src) else "no", len(ps), len(p2)))
    for i, l in p2:
        print("          *** %4d  %s" % (i, l.strip()[:64]))
    ck("%s has 0 pipelines of any kind" % name, len(ps), 0)
    steps = [l for _i, l in L.command_lines(src) if "python3" in l]
    guarded_steps = [l for l in steps if ">" in l and ("||" in l or "\\" in l)]
    print("      steps that redirect and guard: %d of %d"
          % (len(guarded_steps), len(steps)))
    ck("every step of %s redirects and guards" % name,
       len(guarded_steps), len(steps))

print()
print("  AND THE PYTHON, structurally.  Every subprocess here takes a LIST")
print("  argv.  There is ONE deliberate `/bin/sh -c`, in A2d, because")
print("  reproducing the pre-repair PIPELINE is the measurement -- it is")
print("  named here rather than hidden by a rule that would not see it.")
shell_sites, sh_c_sites = [], []
for f in [x for x in MINE if x.endswith(".py")]:
    tree = ast.parse(open(os.path.join(HERE, f), encoding="utf-8").read())
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            fn = n.func
            nm = ("%s.%s" % (getattr(fn.value, "id", "?"), fn.attr)
                  if isinstance(fn, ast.Attribute) else
                  getattr(fn, "id", ""))
            if nm in ("os.system", "os.popen"):
                shell_sites.append((f, n.lineno, nm))
            for kw in (n.keywords or []):
                if kw.arg == "shell" and not (isinstance(kw.value, ast.Constant)
                                              and kw.value.value is False):
                    shell_sites.append((f, n.lineno, "shell=True"))
        if isinstance(n, ast.Constant) and n.value == "-c":
            sh_c_sites.append((f, n.lineno))
ck("no file in this tree CALLS with shell=True or os.system", shell_sites, [])
print("      declared `/bin/sh -c` sites: %d  %s"
      % (len(sh_c_sites), ", ".join("%s:%d" % s for s in sh_c_sites)))
ck("the declared `/bin/sh -c` sites are a2_direct.py and this file's own "
   "detector",
   sorted({f for f, _i in sh_c_sites}), ["a2_direct.py", "selftestdee4.py"])

L.hdr("D4  A STRENGTH MARKER -- OVER EVERY FILE OF THIS TREE, `.md` INCLUDED")

print("  The population is EVERY file, not `*.py` and `*.sh`.  That is the")
print("  direct consequence of A4b: mg-7522's equivalent check excluded the")
print("  `.md`, which is where three of its subject's four wrong artifacts")
print("  were.  The rule is the NINE-alternative one mg-7522 applied to its")
print("  subject, not the three-alternative one it applied to itself.")
print()
MARK = re.compile(r"confirmed exactly|byte-identical|byte for byte"
                  r"|\bverified\b|\(measured\)|\bidentical\b|\bconfirmed\b"
                  r"|\ball (?:\d+|of)\b|\bexactly \d+\b|\bproven\b", re.I)
NUM = re.compile(r"\b\d+\b")
DELIM = "\"'`*"
SIGNALS = ("re.compile", "MARK", "STRENGTH", "ck(", "<- USE", "<- MENTION",
           "SELF_ALTS", "SUBJ_ALTS", "NAMED =")
print("  AND THE FIRST DRAFT OF THIS CHECK FIRED 26 TIMES ON ITS OWN")
print("  SOURCE -- on the regexes that detect the markers and on the")
print("  sentences quoting mg-7522's wording while dispositioning it.  That")
print("  is mg-7522's own recorded defect, reproduced here, and mg-7522's")
print("  own conclusion is followed: the fix is not a better pattern but a")
print("  different question.  So an occurrence is not scored PASS/FAIL; it")
print("  is DISPOSITIONED, with coverage checked in both directions.")
print()
DISP4 = [
    ("the detecting rule itself",
     r"^\s*r?\"|^\s*\(\"|MARK|_STRENGTH|SUBJ_ALTS|SELF_ALTS|NAMED|"
     r"verified byte counts|verified against\" in|DISP"),
    ("a QUOTATION of mg-c2b3's or mg-7522's own wording, being dispositioned",
     r"mg-7522|mg-c2b3|OUTCOMES\.md|artifacts said|S2c|the sweep|"
     r"verified against the pre-repair"),
    ("a figure THIS RUN recomputes in the run that prints it",
     r"A2c|A2d|A5e|identical before and after|8 of 8|survives at the|"
     r"covering 4 of the 8|of those transcripts|regenerate byte for byte|"
     r"to the last row|worktree is byte-identical|identical afterwards"),
]
uses, mentions, undisp4 = [], 0, []
for name in MINE:
    text = open(os.path.join(HERE, name), encoding="utf-8").read()
    for i, l in enumerate(text.split("\n"), 1):
        for m in MARK.finditer(l):
            a = l[m.start() - 1] if m.start() else ""
            b = l[m.end()] if m.end() < len(l) else ""
            if (a in DELIM and b in DELIM) or any(s in l for s in SIGNALS):
                mentions += 1
                continue
            uses.append((name, i, l.strip()))
            if not any(re.search(rx, l) for _w, rx in DISP4):
                undisp4.append((name, i, l.strip()))
print("      files scanned                    %3d" % len(MINE))
print("      MENTIONs (delimited or signalled)%3d" % mentions)
print("      bare occurrences, dispositioned  %3d" % (len(uses) - len(undisp4)))
for why, rx in DISP4:
    n = len([1 for _n, _i, l in uses if re.search(rx, l)])
    print("          %-4d %s" % (n, why))
    ck("disposition rule `%s...` matches something" % why[:28], n > 0, True)
print("      UNDISPOSITIONED                  %3d" % len(undisp4))
for name, i, l in undisp4:
    print("          *** %s:%d  %s" % (name, i, l[:62]))
ck("every bare strength marker in this tree has a disposition",
   len(undisp4), 0)

print()
L.bar("selftestdee4 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts a rule that fires in only one")
print("direction, an undispositioned name filter, a mis-defaulted population")
print("primitive, a pipeline in this tree's own runner, a step that does not")
print("guard, a `shell=True`, and a bare strength marker.  It ranges over")
print("this tree's %d files -- `*.py`, `*.sh` AND `*.md`." % len(MINE))
sys.exit(1 if BAD else 0)
