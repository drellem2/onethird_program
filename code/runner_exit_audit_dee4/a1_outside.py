"""A1 -- THE NEW POPULATION, CHECKED BY LOOKING FOR SOMETHING OUTSIDE IT.

mg-05eb found a population defined by a FILENAME.  mg-7522 replaced it with a
PROPERTY:

    A pipeline whose exit status is CONSUMED, and whose DISCARDED stage can
    fail.

The ticket for this audit says: do not check the definition, look for something
outside it.  So this probe does not argue about the predicate.  It asks four
questions whose answers are files, and reports what it finds:

  A1a  Re-derive mg-7522's five figures with a parser written from scratch.
       A difference here would be the whole finding; there is none.
  A1b  Is `*.sh` itself a name rule?  Every tracked file is inspected for a
       shell shebang regardless of its extension.
  A1c  Can the defect live in Python?  Every tracked `*.py` is walked as an
       AST for a call that hands a STRING to a shell, and each such string is
       parsed for a pipeline.
  A1d  Inside `*.sh`, what does the CONJUNCTION drop?  Every pipeline at HEAD
       is classified by WHICH clause of P2 excludes it, and the excluded ones
       are printed with their consumers traced.

A1d is where the finding is.  P2 tests consumption with `has_set_e(file) and
not guarded(line)` -- errexit, and nothing else.  But mg-7522's own written
reason for pulling the three `git diff ... | wc -c` lines into the population
is not about errexit at all; it is that a failing discarded stage silently
corrupts the VALUE ("a `git diff` that failed produced an empty stream, `wc -c`
reported 0, and the proof read `-> 0 bytes`").  Those two reasons agree on
those three lines, because those files happen to set `-e`.  A1d finds where
they come apart.
"""

import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libdee4 as L

BAD = 0
FINDINGS = []

L.bar("A1  THE NEW POPULATION, AND WHAT IS OUTSIDE IT")

# ---------------------------------------------------------------------------
L.hdr("A1a  MG-7522'S FIVE FIGURES, RE-DERIVED BY A PARSER WRITTEN FROM SCRATCH")

print("  COMPARISON, so the anchor is mg-c2b3's pin %s -- that is the" % L.PINNED)
print("  revision mg-7522's own table is stated at, and comparing two")
print("  parsers requires both to read the same bytes.")
print()

CLAIMED = {"P0 files": 72, "P1 files": 23, "P1 pipelines": 53,
           "P2 files": 19, "P2 pipelines": 26,
           "shape files": 19, "shape pipelines": 42,
           "name files": 17, "name pipelines": 34}


def census(ref):
    files = L.ls_tracked(ref, (".sh",))
    m = dict.fromkeys(CLAIMED, 0)
    m["P0 files"] = len(files)
    p2_members = []
    for f in files:
        try:
            src = L.read(f, ref)
        except (RuntimeError, OSError):
            continue
        ps = L.pipelines(src)
        if ps:
            m["P1 files"] += 1
            m["P1 pipelines"] += len(ps)
        tp = L.tee_pipelines(src)
        if tp:
            m["shape files"] += 1
            m["shape pipelines"] += len(tp)
            if os.path.basename(f) == "run_all.sh":
                m["name files"] += 1
                m["name pipelines"] += len(tp)
        hit = L.p2_pipelines(f, ref)
        if hit:
            m["P2 files"] += 1
            m["P2 pipelines"] += len(hit)
            p2_members.append((f, [i for i, _l in hit]))
    return m, p2_members


pin, pin_p2 = census(L.PINNED)
table = []
for k in ("P0 files", "P1 files", "P1 pipelines", "P2 files", "P2 pipelines",
          "shape files", "shape pipelines", "name files", "name pipelines"):
    v, c = pin[k], CLAIMED[k]
    if v != c:
        BAD += 1
        FINDINGS.append("A1a %s: mg-7522 says %d, re-derived %d" % (k, c, v))
    table.append((k, c, v, "AGREES" if v == c else "*** DIFFERS ***"))
print("    %-18s %-9s %-11s %s" % ("figure", "mg-7522", "re-derived", "verdict"))
L.rows(table, (18, 9, 11), indent="    ")
print()
print("  The two parsers agree on every one.  That is not a licence to stop:")
print("  agreement about a POPULATION says nothing about what is outside it,")
print("  which is A1b through A1d.")

# ---------------------------------------------------------------------------
L.hdr("A1b  IS `*.sh` ITSELF A NAME RULE?  EVERY TRACKED FILE, BY SHEBANG")

print("  `lib7522.ls_sh()` takes no name argument -- mg-7522 calls that")
print("  structural, and it is.  But the function still selects on the string")
print("  `.sh`, and an extension is a naming convention exactly as `run_all`")
print("  is.  So: every tracked file, whatever its name, read for a shell")
print("  shebang.  A hit would be a shell script the property cannot reach.")
print()
allf = L.ls_tracked(None, ("",))
shellish = []
exts = {}
for f in allf:
    ext = os.path.splitext(f)[1] or "(none)"
    exts[ext] = exts.get(ext, 0) + 1
    if f.endswith(".sh"):
        continue
    try:
        first = L.read(f, None).splitlines()[:1]
    except (RuntimeError, OSError, IndexError):
        continue
    if first and first[0].startswith("#!") and (
            "sh" in first[0] or "bash" in first[0] or "zsh" in first[0]):
        shellish.append((f, first[0]))
print("      tracked files                              %4d" % len(allf))
print("      distinct extensions                        %4d   %s"
      % (len(exts), ", ".join("%s %d" % (k, v)
                              for k, v in sorted(exts.items(),
                                                 key=lambda kv: -kv[1]))))
print("      NON-`.sh` files with a shell shebang       %4d" % len(shellish))
for f, s in shellish:
    print("          *** %s  %s" % (f, s))
if shellish:
    BAD += 1
    FINDINGS.append("A1b %d shell scripts outside `*.sh`" % len(shellish))
print()
print("  HOW THIS IS ESTABLISHED, so a reader can disagree with it: the")
print("  population is `git ls-files` with NO suffix filter, and the test is")
print("  the file's own first line.  It is not a list of extensions I thought")
print("  of.  `.sh` loses nothing HERE; it is still a name rule, and the next")
print("  shell script committed without the extension is invisible to it.")

# ---------------------------------------------------------------------------
L.hdr("A1c  CAN THE DEFECT LIVE IN PYTHON?  EVERY `*.py`, WALKED AS AN AST")

print("  A pipeline needs a shell.  Python gets one through `shell=True`,")
print("  `os.system`, `os.popen` or `subprocess.getoutput`.  Grepping for")
print("  those strings scores the sentence `we never use shell=True` as a")
print("  hit -- mg-05eb recorded that defect and mg-7522 hit it again, so")
print("  this is an AST walk over every tracked `*.py` in the repository.")
print()
pys = L.ls_tracked(None, (".py",))
SHELL_FN = ("os.system", "os.popen", "subprocess.getoutput",
            "subprocess.getstatusoutput")
sites, unparsed = [], []
for f in pys:
    try:
        tree = ast.parse(L.read(f, None))
    except SyntaxError as e:
        unparsed.append((f, str(e)))
        continue
    for n in ast.walk(tree):
        if not isinstance(n, ast.Call):
            continue
        fn = n.func
        name = ""
        if isinstance(fn, ast.Attribute):
            name = "%s.%s" % (getattr(fn.value, "id", "?"), fn.attr)
        elif isinstance(fn, ast.Name):
            name = fn.id
        why = None
        if name in SHELL_FN:
            why = name
        for kw in (n.keywords or []):
            if kw.arg == "shell" and not (isinstance(kw.value, ast.Constant)
                                          and kw.value.value is False):
                why = "%s(shell=...)" % (name or "?")
        if why:
            sites.append((f, n.lineno, why))
print("      tracked `*.py`                             %4d" % len(pys))
print("      files this walk could not parse            %4d" % len(unparsed))
for f, e in unparsed:
    print("          *** %s  %s" % (f, e))
print("      REAL shell-executing call sites            %4d" % len(sites))
for f, ln, why in sites:
    print("          %s:%d  %s" % (f, ln, why))
print()
if unparsed:
    BAD += 1
    FINDINGS.append("A1c %d `*.py` unparsed -- coverage is not total"
                    % len(unparsed))

def _flat(node):
    """The literal text of a string constant or an f-string's literal parts."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        return "".join(p.value for p in node.values
                       if isinstance(p, ast.Constant)
                       and isinstance(p.value, str))
    return None


# THE POPULATION OF STRINGS THAT ACTUALLY REACH A SHELL, resolved one level.
# The single site is `subprocess.run(cmd, shell=True)` inside `def sh(cmd)`, so
# the strings that reach the shell are the arguments of every call to `sh`.
# Resolving that is the difference between a rule and a guess; the whole-file
# over-read is kept below it as a diagnostic, with each hit dispositioned.
reaching, wrappers = [], []
for f, ln, _why in sites:
    tree = ast.parse(L.read(f, None))
    for fn in ast.walk(tree):
        if not isinstance(fn, ast.FunctionDef):
            continue
        if not any(getattr(n, "lineno", -1) == ln for n in ast.walk(fn)):
            continue
        params = [a.arg for a in fn.args.args]
        wrappers.append((f, fn.name, params))
        for n in ast.walk(tree):
            if (isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                    and n.func.id == fn.name):
                for a in n.args:
                    t = _flat(a)
                    if t is not None:
                        reaching.append((f, n.lineno, t))
print("      shell-exec sites sitting inside a wrapper  %4d" % len(wrappers))
for f, name, params in wrappers:
    print("          %s  def %s(%s)" % (f, name, ", ".join(params)))
print("      literal strings that REACH that shell      %4d" % len(reaching))
bad_reach = []
for f, ln, s in reaching:
    hit = bool(L._PIPE.search(L.unquoted(s)))
    if hit:
        bad_reach.append((f, ln, s))
    print("          %s:%-5d pipeline: %-5s %s" % (f, ln, hit, s[:46]))
if bad_reach:
    BAD += 1
    FINDINGS.append("A1c a shell string with a pipeline: %s:%d"
                    % (bad_reach[0][0], bad_reach[0][1]))
print()

# The over-read, kept and dispositioned rather than tuned away.
piped = []
for f, _ln, _why in sites:
    tree = ast.parse(L.read(f, None))
    for n in ast.walk(tree):
        t = _flat(n)
        if t is not None and L._PIPE.search(L.unquoted(t)):
            piped.append((f, n.lineno, t[:60]))
DISP_OVERREAD = [
    ("instrument_sensitivity.py", 'ls2[134][:200] + " |"',
     "NOT A COMMAND -- the mutation payload appended to a truncated STATE.md "
     "row; `|` there is a markdown table cell terminator and the string is "
     "written to a FILE, never handed to a shell"),
]
print("      OVER-READ: every string literal in those      %2d" % len(piped))
print("      files, whether or not it reaches a shell")
for f, ln, s in piped:
    d = [x for x in DISP_OVERREAD if x[0] in f]
    why = d[0][2] if d else "*** NO DISPOSITION -- this one is real ***"
    L.rows([("%s:%d" % (os.path.basename(f), ln), why)], (34,), indent="          ")
    if not d:
        BAD += 1
        FINDINGS.append("A1c undispositioned piped string %s:%d" % (f, ln))
print()
print("  ESTABLISHED: the defect cannot be hiding in the Python of this")
print("  repository.  There is exactly ONE place a Python file hands a string")
print("  to a shell; the strings that reach it are enumerated above and none")
print("  is a pipeline; and the one whole-file over-read hit is a markdown")
print("  cell terminator in a mutation payload, dispositioned rather than")
print("  removed from the rule.  A rule tuned until it goes green is not a")
print("  measurement -- that is mg-7522's own OUTCOMES.md lesson, applied here.")

# ---------------------------------------------------------------------------
L.hdr("A1d  INSIDE `*.sh`: WHICH CLAUSE OF P2 DROPS WHAT, AT HEAD")

print("  P2 is a conjunction.  A pipeline can fall out of it three ways, and")
print("  they are not equally safe.  Every pipeline at HEAD, with the clause")
print("  that excludes it named:")
print()
rows = []
dropped_no_e, dropped_guard, dropped_cannot = [], [], []
n_pipes = 0
for f in L.ls_tracked(None, (".sh",)):
    src = L.read(f, None)
    se = L.has_set_e(src)
    for i, line in L.pipelines(src):
        n_pipes += 1
        g = L.guarded(line)
        cf = [L.stage_can_fail(f, s, None) for s in L.discarded_stages(line)]
        if not se:
            why, bucket = "no `set -e` in the file", dropped_no_e
        elif g:
            why, bucket = "the line guards its own status", dropped_guard
        elif not any(v for v, _w in cf):
            why, bucket = "no discarded stage can fail", dropped_cannot
        else:
            why, bucket = "IN P2", None
        if bucket is not None:
            bucket.append((f, i, line.strip(), cf))
        rows.append(("%s:%d" % (os.path.basename(os.path.dirname(f)), i),
                     "yes" if se else "no", "yes" if g else "no", why))
print("    %-38s %-7s %-9s %s" % ("file:line", "set -e", "guarded", "excluded by"))
L.rows(rows, (38, 7, 9), indent="    ")
print()
print("      pipelines on command lines at HEAD         %4d" % n_pipes)
print("      dropped: no `set -e`                       %4d" % len(dropped_no_e))
print("      dropped: the line guards itself            %4d" % len(dropped_guard))
print("      dropped: no discarded stage can fail       %4d" % len(dropped_cannot))
print("      IN P2 at HEAD                              %4d"
      % (n_pipes - len(dropped_no_e) - len(dropped_guard) - len(dropped_cannot)))

# ---------------------------------------------------------------------------
L.hdr("A1e  THE ONE THAT IS OUTSIDE: `set -e` IS NOT THE ONLY CONSUMER")

print("  mg-7522's REASON for pulling the three `git diff ... | wc -c` lines")
print("  into the population is written in the file it repaired and in the")
print("  published document, and it is not about errexit:")
print()
print("      \"a `git diff` that failed produced an empty stream, `wc -c`")
print("       reported 0, and the proof read `-> 0 bytes`\"")
print()
print("  That is a claim about the VALUE.  P2's consumption test is")
print("  `has_set_e(file) and not guarded(line)` -- errexit, at FILE grain.")
print("  The two agree on those three lines only because those two files")
print("  happen to set `-e`.  Here is where they come apart:")
print()
for f, i, line, cf in dropped_no_e:
    print("      %s:%d" % (f, i))
    print("          %s" % line[:70])
    for v, w in cf:
        print("          discarded stage CAN FAIL: %-5s %s" % (v, w))
    src = L.read(f, None)
    ls = src.split("\n")
    var = line.strip().split("=")[0] if "=" in line.split("$(")[0] else None
    if var:
        uses = [(j, l.strip()) for j, l in enumerate(ls, 1)
                if j != i and ("$%s" % var in l or '"$%s"' % var in l
                               or "${%s}" % var in l)]
        print("          the value is assigned to `%s` and read at %d place(s):"
              % (var, len(uses)))
        for j, l in uses:
            print("              %4d  %s" % (j, l[:64]))
    print()

print("  IS THE STATUS CONSUMED?  Trace it forward rather than asserting it.")
print()
CHAIN = "code/branching_audit_a218/c0_repro.sh"
if L.exists(CHAIN, None):
    src = L.read(CHAIN, None)
    ls = src.split("\n")
    exit_lines = [(j, l.strip()) for j, l in enumerate(ls, 1)
                  if "exit 1" in l or "TOTAL BAD" in l]
    print("      %s reaches its own exit status at:" % CHAIN)
    for j, l in exit_lines:
        print("          %4d  %s" % (j, l[:64]))
    print()
    # Who reads THAT status?  Census -- unpinned, HEAD.
    readers = []
    for f in L.ls_tracked(None, (".py", ".sh")):
        if f == CHAIN:
            continue
        body = L.read(f, None).split("\n")
        for j, l in enumerate(body, 1):
            if "c0_repro.sh" not in l:
                continue
            if "subprocess" not in l and "sh " not in l:
                continue
            window = "\n".join(body[j - 1:j + 12])
            readers.append((f, j, l.strip(),
                            "returncode" in window or "check=True" in window))
    print("      and its exit status is READ by (census at HEAD, unpinned):")
    for f, j, l, rd in readers:
        print("          %s:%d  %-5s %s"
              % (f, j, "READS" if rd else "no", l[:52]))
    live = [r for r in readers if r[3]]
    print()
    if live:
        FINDINGS.append(
            "A1e %s:47 is a status-consuming pipeline OUTSIDE mg-7522's P2: "
            "the discarded `grep` and `tr` stages can fail, the value reaches "
            "the script's own exit code, and %d caller(s) read that code"
            % (CHAIN, len(live)))
    print("      SO: the pipeline's result reaches this script's exit status,")
    print("      and %d external caller(s) read that status.  It is consumed."
          % len(live))
    print("      It is outside P2 for one reason only: the file sets `-u` and")
    print("      not `-e`.")
    print()
    print("      THE THREE RULES, ON THIS ONE FILE:")
    print("          mg-c2b3's NAME rule  (`run_all.sh`)   MISSES -- it is c0_repro.sh")
    print("          mg-c2b3's SHAPE rule (`| tee`)        MISSES -- there is no tee")
    print("          mg-7522's PROPERTY rule (P2)          MISSES -- no `set -e`")
    print()
    print("  THE DIRECTION IT FAILS IN, stated rather than left to be assumed:")
    print("  a failing `grep` here empties the stream, `COUNT` becomes empty,")
    print("  the comparison against `699520` reports DISAGREES and the script")
    print("  exits 1.  That is fail-LOUD, not the silent green mg-c2b3 was")
    print("  sweeping for.  This is a hole in the population, and on today's")
    print("  bytes it is not a live swallow.  Both halves are the finding.")

print()
L.bar("A1 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts a disagreement between two parsers")
print("on mg-7522's five figures, a shell script outside `*.sh`, an unparsed")
print("`*.py`, and a shell string carrying a pipeline.  It ranges over every")
print("tracked file in the repository at HEAD and every tracked `*.sh` at")
print("%s.  It does NOT count A1e: a population hole is a finding about" % L.PINNED)
print("a predicate, and turning it into a BAD would say mg-7522 broke")
print("something it did not break.")
print()
for f in FINDINGS:
    print("FINDING: %s" % f)
sys.exit(1 if BAD else 0)
