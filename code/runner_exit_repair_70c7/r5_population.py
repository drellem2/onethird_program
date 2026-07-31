"""R5 -- THE POPULATION HOLE, AND THE DIRECTION OF THE ONE IN IT.  mg-dee4's F6.

THE FINDING.  P2's consumption test was `has_set_e(file) and not guarded(line)`
-- errexit, at FILE grain.  mg-7522's WRITTEN REASON for pulling the three
`git diff` lines into the population is about the VALUE: *"a `git diff` that
failed produced an empty stream, `wc -c` reported 0, and the proof read
`-> 0 bytes`"*.  The two agree on those three lines only because both of those
files happen to set `-e`, so the difference was invisible in the population
that produced it.  `code/branching_audit_a218/c0_repro.sh:47` is where they
come apart: `set -u` and no `-e`, a three-stage pipeline whose discarded `grep`
and `tr` can fail, whose value drives `BAD`, whose `BAD` drives `exit 1`, and
whose exit code is read at nine sites in three files.

THE REPAIR IS TO THE POPULATION.  `lib7522.consumed` is a named disjunction
now, and both arms are printed with every row.  The instance is secondary and
its direction is MEASURED rather than argued: R5c forces the `grep` to fail on
the real bytes and reads what the script does.  A hole in a population is not
the same thing as a live swallow, and the difference is what the control shows.
"""

import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib70c7 as M

sys.path.insert(0, os.path.join(M.REPO, M.SUBJECT))
import lib7522 as L                                            # noqa: E402

BAD = 0
SITE = "code/branching_audit_a218/c0_repro.sh"
LINE = 47

M.bar("R5  CONSUMPTION IS A DISJUNCTION, AND BOTH ARMS ARE NAMED")

# ---------------------------------------------------------------------------
M.hdr("R5a  THE TWO ARMS, COUNTED SEPARATELY, AT BOTH REVISIONS")

print("  Re-derived under this tree's own `captured_var` / `var_reads`, which")
print("  share no code with `lib7522.consumed`.  If the two disagree about")
print("  which pipelines are in the population, this row says so.")
print()
print("    %-12s %-24s %6s %10s" % ("revision", "clause", "files", "pipelines"))


def measure(ref):
    src = L.sources(L.ls_sh(ref), ref)
    arms = {"ERREXIT": set(), "VALUE": set(), "EITHER": set()}
    rows = []
    for p, s in sorted(src.items()):
        se = L.has_set_e(s)
        for i, line in L.pipelines(s):
            if not any(L.stage_can_fail(p, st, ref)[0]
                       for st in L.discarded_stages(line)):
                continue
            errexit = se and not L.guarded(line)
            var = M.captured_var(line)
            value = bool(var) and bool(M.var_reads(s, var, i))
            if errexit:
                arms["ERREXIT"].add((p, i))
            if value:
                arms["VALUE"].add((p, i))
            if errexit or value:
                arms["EITHER"].add((p, i))
                rows.append((p, i, line.strip(), errexit, value))
    return arms, rows


for ref, label in ((L.PINNED, L.PINNED), (None, "HEAD")):
    arms, rows = measure(ref)
    for name in ("ERREXIT", "VALUE", "EITHER"):
        s = arms[name]
        print("    %-12s %-24s %6d %10d"
              % (label, name, len({p for p, _i in s}), len(s)))
    if ref is None:
        head_rows = rows
    else:
        pin_rows = rows
    print()

print("  mg-7522 PUBLISHED 19 files / 26 pipelines for P2 at %s, which is the"
      % L.PINNED)
print("  ERREXIT row above.  The published table now carries both rows, so a")
print("  reader can disagree with one arm without discarding the other.")
print()
print("  AND THE SAME QUESTION PUT TO THE REPAIRED PROBE:")
try:
    t = M.read("%s/out_s1_population.txt" % M.SUBJECT, None)
    m = re.findall(r"P2  \.\.\.status CONSUMED and discarded stage CAN FAIL"
                   r"\s+(\d+)\s+(\d+)", t)
    e = re.findall(r"by the ERREXIT arm alone \(the clause before\s+(\d+)\s+(\d+)",
                   t)
    print("      out_s1_population.txt P2 rows          %s" % (m,))
    print("      out_s1_population.txt errexit rows     %s" % (e,))
except (RuntimeError, OSError):
    print("      (no transcript yet -- first pass of run_all.sh)")

# ---------------------------------------------------------------------------
M.hdr("R5b  THE MEMBER THE VALUE ARM ADDS -- traced forward, not asserted")

src = M.read(SITE, None)
lines = src.splitlines()
line = lines[LINE - 1]
print("      %s:%d" % (SITE, LINE))
print("          %s" % line.strip()[:70])
print()
print("      set -e present in the file        %s"
      % ("yes" if L.has_set_e(src) else "NO -- this is why P2 missed it"))
var = M.captured_var(line)
reads = M.var_reads(src, var, LINE) if var else []
print("      output captured into              `%s`" % var)
print("      ...and READ at %d site(s):" % len(reads))
for i, l in reads:
    print("          %4d  %s" % (i, l[:62]))
print()
stages = L.discarded_stages(line)
print("      DISCARDED stages, and whether each can fail:")
for st in stages:
    v, why = L.stage_can_fail(SITE, st, None)
    print("          %-40s %-5s %s" % (st.strip()[:40], bool(v), why[:30]))
print()
print("  DOES THE VALUE REACH THE SCRIPT'S OWN EXIT STATUS?  Traced, one hop")
print("  at a time, in the file's own bytes:")
print()
chain = []
for i, l in enumerate(lines, 1):
    if i <= LINE:
        continue
    if re.search(r"\$\{?%s\b" % re.escape(var or "x"), l):
        chain.append((i, l.strip(), "reads $%s" % var))
    elif re.search(r"BAD=\$\(\(BAD \+ 1\)\)", l) and chain:
        chain.append((i, l.strip(), "sets BAD"))
    elif re.search(r'\[ "\$BAD" -eq 0 \] \|\| exit 1', l):
        chain.append((i, l.strip(), "BAD -> exit 1"))
for i, l, why in chain:
    print("      %4d  %-52s %s" % (i, l[:52], why))
print()
readers = []
for f in [x for x in M.git("ls-files", "--", "*.py", "*.sh").splitlines() if x]:
    if f == SITE:
        continue
    try:
        s = M.read(f, None)
    except (RuntimeError, OSError):
        continue
    for i, l in enumerate(s.split("\n"), 1):
        if "c0_repro.sh" in l and re.search(r"returncode|subprocess\.|exits", l):
            readers.append((f, i))
print("      external sites naming c0_repro.sh with an execution or a")
print("      status read:                                  %3d in %d file(s)"
      % (len(readers), len({f for f, _i in readers})))
for f, i in readers:
    print("          %s:%d" % (f, i))
print()
print("  AND THE THING THAT CANNOT BE DONE HERE, named rather than skipped.")
print("  mg-c2b3's K3b method -- run the discarded stage directly and read the")
print("  number the pipeline threw away -- is what S2 does to the 8 `| tee`")
print("  and 8 `git diff` executions.  It CANNOT be done to this one:")
print()
for st in stages:
    argv = L.argv_of(st, {})
    print("      %-46s argv derivable: %s"
          % (st.strip()[:46], "yes" if argv else "NO"))
print()
print("      The discarded stages read `$WORK`, a `mktemp -d` created by the")
print("      script at run time.  There is no argv to run: the path does not")
print("      exist until the script that builds it is running.  I PREDICTED")
print("      these could be read directly and they cannot -- kept in")
print("      PREDICTIONS.md as a miss.  R5c is what stands in its place, and")
print("      it is the stronger evidence: instead of asking what the discarded")
print("      stage returns TODAY, it makes the stage fail and reads what the")
print("      script DOES.")

# ---------------------------------------------------------------------------
M.hdr("R5c  THE DIRECTION, MEASURED -- a forced failure on the real bytes")

print("  mg-dee4 called this fail-LOUD and did not run it.  A direction that")
print("  is argued is a direction that has not been checked, so both arms are")
print("  run here on a scratch copy of the REAL script: the file's own bytes,")
print("  with exactly one edit -- the discarded `grep` given an option it")
print("  rejects, so it exits non-zero and prints nothing.  No tracked file")
print("  is touched.")
print()
d = tempfile.mkdtemp(prefix="mg70c7_")
try:
    real = os.path.join(M.REPO, os.path.dirname(SITE))
    forced = src.replace("grep -o '[0-9][0-9 ]*'",
                         "grep --mg70c7-not-an-option -o '[0-9][0-9 ]*'")
    ok = forced != src
    print("      the forced edit applied to exactly one line   %s"
          % ("yes" if ok else "*** NO -- the line has moved ***"))
    if not ok:
        BAD += 1
    for label, text in (("as committed", src), ("`grep` forced to fail",
                                                forced)):
        p = os.path.join(real, "_mg70c7_arm.sh")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(text)
        try:
            code, out = M.run_argv(["/bin/sh", "_mg70c7_arm.sh"], real,
                                   timeout=900)
        finally:
            try:
                os.unlink(p)
            except OSError:
                pass
        says = "DISAGREES" in out
        bad_line = [l for l in out.splitlines() if "TOTAL BAD" in l]
        print("      %-24s exit %-4s prints DISAGREES: %-5s  %s"
              % (label, "-" if code is None else code, says,
                 bad_line[-1].strip() if bad_line else ""))
        if label == "as committed" and (code != 0 or says):
            BAD += 1
            print("          *** the unmodified script does not pass ***")
        if label != "as committed" and (code == 0 or not says):
            BAD += 1
            print("          *** a failing discarded stage is SWALLOWED -- this")
            print("              is a live swallow and not a population hole ***")
finally:
    import shutil
    shutil.rmtree(d, ignore_errors=True)
print()
print("  SO THE DIRECTION IS LOUD, measured rather than asserted: a failing")
print("  discarded stage makes this script REPORT a disagreement and exit")
print("  non-zero, which is the opposite of the silent green mg-c2b3 swept")
print("  for.  That is why the repair is to the POPULATION and the instance")
print("  is left as it is, with the reason in `out_s1_population.txt`'s")
print("  disposition table rather than in a commit message.")

# ---------------------------------------------------------------------------
M.hdr("R5d  ALL THREE RULES, ON THIS ONE FILE")

name = os.path.basename(SITE) in ("run_all.sh", "run_audit.sh")
shape = bool(L.tee_pipelines(src))
prop = L.has_set_e(src)
for label, hit, why in (("mg-c2b3's NAME rule  (`run_all.sh`)", name,
                         "it is %s" % os.path.basename(SITE)),
                        ("mg-c2b3's SHAPE rule (`| tee`)", shape,
                         "there is no tee"),
                        ("mg-7522's PROPERTY rule (errexit arm)", prop,
                         "there is no `set -e`")):
    print("      %-42s %s -- %s" % (label, "FINDS" if hit else "MISSES", why))
print()
print("  Three rules, three different reasons, one file.  That is what makes")
print("  it a population finding rather than an instance: each rule is sound")
print("  about what it defines and none of the three defines the defect.")

print()
M.bar("R5 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts a forced-failure edit that no longer")
print("applies, an unmodified script that does not pass, and a forced failure")
print("that is SWALLOWED rather than reported.  It ranges over ONE file --")
print("`%s` -- and over the P2 census at %s and HEAD."
      % (SITE, L.PINNED))
print("It does NOT establish that the value arm is the RIGHT widening; that is")
print("a disagreement with a definition, and the definition is written out in")
print("`lib7522.consumed` in full so that disagreeing with it is possible.")
sys.exit(1 if BAD else 0)
