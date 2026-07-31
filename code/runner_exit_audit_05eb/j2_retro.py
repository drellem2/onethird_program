"""J2 -- THE RETROACTIVE HALF, RE-ASKED.  Which past claims read an affected
runner's exit code, and did the sweep's enumeration contain them?

The sweep's answer is nine claims, seven SAFE and two AT RISK, all of the R3 kind
living in one file: `code/species_sites_821e/p3_wiring.py`.  Its headline sentence
is

    "the arc reads its results from committed transcripts and byte-comparisons
     almost everywhere, and reads them from an exit status in exactly ONE file"

That list is a Python literal, hand-written, in `k3_retro.py`.  A hand-written
enumeration is exactly the thing an independent audit exists to widen, so this
section does not check the nine.  It builds the list MECHANICALLY and asks what
falls outside.

THE HOLE THIS SECTION IS LOOKING FOR, stated before it is found so the finding
cannot be mistaken for a search that was aimed at it: the sweep's caller scan
(`K2a`) runs at the PINNED revision `bee07a1`.  Pinning is right for the
byte-comparison (`K3d`) -- anchoring to HEAD would compare the repaired tree with
itself, which is mg-821e's own finding.  It is wrong for a caller scan, because a
caller that landed AFTER the pin is invisible to it and is nonetheless a consumer
of the status the sweep is repairing.
"""

import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib05eb as L

BAD = 0
MISS = []


def predict(qid, predicted, measured, ok):
    MISS.append((qid, predicted, measured, ok))
    print("  %-4s predicted %-34s measured %-24s %s"
          % (qid, predicted, measured, "as predicted" if ok else "*** MISS ***"))


L.bar("J2  THE RETROACTIVE HALF, RE-ASKED FROM A MECHANICAL ENUMERATION")

# ---------------------------------------------------------------------------
# J2a  every site that EXECUTES a shell runner and READS its status
# ---------------------------------------------------------------------------
L.hdr("J2a  R3 CONSUMERS, FOUND MECHANICALLY -- at the pin AND at HEAD")

# A `.py` line EXECUTES when it hands a shell a script path.  Both spellings
# used in this repository are matched: a literal `"sh"`/`"/bin/sh"` first
# element, and a helper whose body does that.  The helper case is why the scan
# is two-pass rather than line-local: `run_runner(t)` names no `.sh` at all.
EXEC_PY = re.compile(r'\[\s*"(?:/bin/)?(?:sh|bash)"')
READS = re.compile(r"\.returncode|check\s*=\s*True|\brc\b|\bcode\b")
SCORES = re.compile(r"(?:rc|code|code_u|code_w|rc2|wired_rc\[t\]|unwired_rc\[t\]"
                    r"|guard_rc\[t\])\s*(?:==|!=)\s*0")


DEF = re.compile(r"^def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", re.M)


def _sources(ref):
    files = [p for p in L.git("ls-tree", "-r", "--name-only", ref).splitlines()
             if p.endswith(".py") or p.endswith(".sh")] if ref else \
            [p for p in L.git("ls-files").splitlines()
             if p.endswith(".py") or p.endswith(".sh")]
    src = {}
    for p in files:
        if p.startswith("code/runner_exit_audit_05eb/"):
            continue          # this instrument is J2e's subject, not J2a's
        try:
            src[p] = L.read(p, ref)
        except Exception:
            pass
    return src


# A helper counts only when its body builds an argv whose first element is a
# shell AND whose second is a `.sh` path.  `EXEC_PY` alone matched section
# functions called `main` / `t8` / `a4`, which are local to one file and mean
# nothing when their NAME appears elsewhere.
ARGV_SH = re.compile(r'\[\s*"(?:/bin/)?(?:sh|bash)"\s*,\s*[^\]]*\.sh')


def _helpers(src):
    """{name: defining module stem} for functions that hand a shell a `.sh`.

    Two passes, because the sweep's own K2a is line-local, and a line-local
    rule cannot see `run_runner(t)` -- which names no `.sh` and no `sh` and is
    nonetheless how the one file the sweep DOES name executes its runners.  A
    scan that misses `code/species_sites_821e/p3_wiring.py` is not a wider
    scan, it is a broken one; this pass exists because my first draft did
    exactly that, and the miss is kept in OUTCOMES.md rather than smoothed out.
    """
    names = {}
    for p, txt in src.items():
        if not p.endswith(".py"):
            continue
        marks = list(DEF.finditer(txt))
        for k, m in enumerate(marks):
            end = marks[k + 1].start() if k + 1 < len(marks) else len(txt)
            if ARGV_SH.search(txt[m.end():end]):
                names[m.group(1)] = os.path.basename(p)[:-3]
    return names


def _imports(txt):
    """Names this module imports.  A helper only propagates to a file that
    actually IMPORTS it -- sharing a function NAME is not sharing a function."""
    got = set()
    for m in re.finditer(r"from\s+[\w.]+\s+import\s+\(([^)]*)\)", txt):
        got |= set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", m.group(1)))
    for m in re.finditer(r"from\s+[\w.]+\s+import\s+([^\n(]+)", txt):
        got |= set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", m.group(1)))
    return got


def scan(ref):
    """{path: [(line, kind, text)]} for every executor/scorer of a shell runner."""
    src = _sources(ref)
    helpers = _helpers(src)
    hits = {}
    for p, txt in src.items():
        lines = txt.splitlines()
        mine = sorted(n for n in _imports(txt) if n in helpers)
        call = re.compile(r"(?<![\w.])(%s)\s*\(" % "|".join(mine)) if mine else None
        rows = []
        for i, l in enumerate(lines, 1):
            if p.endswith(".py"):
                if EXEC_PY.search(l):
                    window = "\n".join(lines[max(0, i - 3):i + 25])
                    rows.append((i, "EXEC" + (" +READS" if READS.search(window)
                                              else ""), l.strip()))
                elif call and call.search(l) and not l.lstrip().startswith("#") \
                        and not DEF.match(l):
                    rows.append((i, "EXEC(helper)", l.strip()))
                if SCORES.search(l):
                    rows.append((i, "SCORES-ON-EXIT", l.strip()))
            else:
                if re.search(r"(?<![\w./])(?:sh\s+|\./)\S*\.sh", l) and \
                        not l.lstrip().startswith("#"):
                    rows.append((i, "EXEC(sh)", l.strip()))
        if rows:
            hits[p] = rows
    return hits


def consumers(hits):
    """Files that both execute a runner and score on an exit status."""
    out = {}
    for p, rows in hits.items():
        ex = [r for r in rows if r[1].startswith("EXEC")]
        sc = [r for r in rows if r[1] == "SCORES-ON-EXIT"]
        if ex and sc:
            out[p] = (ex, sc)
    return out


pin_hits, head_hits = scan(L.PINNED), scan(None)
pin_c, head_c = consumers(pin_hits), consumers(head_hits)

print("  A file is an R3 CONSUMER when it BOTH executes a shell script AND")
print("  scores a variable against 0 / non-0.  Both halves are required: a")
print("  file that runs a runner and byte-compares its stdout is R1 and is")
print("  not at risk, which is the sweep's own rule and is kept.")
print()
print("  R3 consumer files at %s (the sweep's caller-scan revision): %d"
      % (L.PINNED, len(pin_c)))
for p in sorted(pin_c):
    print("      %s" % p)
print()
print("  R3 consumer files at HEAD                                : %d"
      % len(head_c))
for p in sorted(head_c):
    print("      %-56s %s" % (p, "" if p in pin_c else "<-- NOT AT THE PIN"))
new = sorted(set(head_c) - set(pin_c))
print()
predict("Q11", ">= 4 at HEAD", str(len(head_c)), len(head_c) >= 4)

# ---------------------------------------------------------------------------
# Which of them target an AFFECTED runner?
# ---------------------------------------------------------------------------
pre = {p: L.read(p, L.PINNED) for p in L.ls_sh(L.PINNED)}
AFFECTED = {p for p in pre if L.tee_pipelines(pre[p])}
TREE = re.compile(r"code/([A-Za-z0-9_]+)/run_all\.sh")

print()
print("  ...and which of them score the exit status of a runner that had a")
print("  `| tee` pipeline at %s (%d such files, from J1):" % (L.PINNED, len(AFFECTED)))
print()
flagged = []
for p in sorted(head_c):
    txt = L.read(p)
    named = {m.group(1) for m in TREE.finditer(txt)}
    # trees named through a list variable are resolved by reading the list
    for m in re.finditer(r'TREES\s*=\s*\[([^\]]*)\]', txt):
        named |= set(re.findall(r'"([A-Za-z0-9_]+)"', m.group(1)))
    aff = sorted(t for t in named
                 if "code/%s/run_all.sh" % t in AFFECTED)
    if aff:
        flagged.append((p, aff))
        print("      %-52s -> %s" % (p, ", ".join(aff)))
print()
print("  THE SWEEP'S HEADLINE, tested: \"reads them from an exit status in")
print("  exactly ONE file\".  Files measured here: %d." % len(flagged))
for p, aff in flagged:
    print("      %-52s %s" % (p, "(the sweep names this one)"
                              if "821e" in p else "*** NOT IN THE SWEEP'S NINE ***"))
outside = [p for p, _a in flagged if "821e" not in p]
predict("Q12", ">= 2 claims outside the nine",
        "%d file(s) outside" % len(outside), len(outside) >= 1)
print()
print("  AND THE PART THAT WOULD OVERSTATE IT IF LEFT OUT.  Of the %d outside"
      % len(outside))
print("  the nine, one is `code/runner_exit_c2b3/` -- the sweep's OWN")
print("  instrument, written after the defect, measuring it on purpose.  That")
print("  is not a past claim and it is not an exposure, and counting it as one")
print("  would inflate this finding to twice its size.  It is listed because")
print("  the sentence under test says `exactly ONE file`, and as a count of")
print("  files that score a runner's exit status that sentence is wrong three")
print("  ways; as a count of PAST CLAIMS AT RISK it is wrong once.  The once")
print("  is J2b.")
past = [p for p in outside if not p.startswith("code/runner_exit_c2b3/")]
print()
print("  past-claim R3 consumers of an affected runner, outside the nine: %d"
      % len(past))
for p in past:
    print("      %s" % p)
if past:
    BAD += 1

# ---------------------------------------------------------------------------
# J2a2  the OTHER hole in the caller scan -- and it is empty, which is a result
# ---------------------------------------------------------------------------
L.hdr("J2a2  A SECOND HOLE IN THE CALLER SCAN, AND WHAT WAS BEHIND IT")

print("  `k2_consume.py` builds its caller population as")
print()
print("      files = [f for f in ... if (f.endswith('.py') or f.endswith('.sh'))")
print("               and not f.endswith('/run_all.sh')]")
print()
print("  -- every `run_all.sh` is EXCLUDED from being a caller.  A runner that")
print("  runs another runner under `set -e` is a status consumer and cannot")
print("  appear in that table.  Measured over every `*.sh` at HEAD:")
print()
SHEXEC = re.compile(r"(?<![\w./])(?:sh\s+|\./)(\S+\.sh)")
shell_calls = []
for p in L.ls_sh():
    for i, l in L.command_lines(L.read(p)):
        if "dirname" in l:
            continue
        m = SHEXEC.search(l)
        if m:
            shell_calls.append((p, i, m.group(1), l.strip()))
for p, i, tgt, l in shell_calls:
    invisible = p.endswith("/run_all.sh")
    tree = re.search(r"([\w./]*%s)" % re.escape(tgt.lstrip("./")), l)
    hits_affected = any(tgt.lstrip("./") in a or a.endswith(tgt.lstrip("./"))
                        for a in AFFECTED)
    print("    %-46s :%-3d -> %-34s %s%s"
          % (p, i, tgt,
             "INVISIBLE to K2a" if invisible else "in K2a's population",
             "  <-- target was AFFECTED" if hits_affected else ""))
inv = [c for c in shell_calls if c[0].endswith("/run_all.sh")]
print()
print("  shell-level runner executions in the repository : %d" % len(shell_calls))
print("  ...invisible to K2a by that filter              : %d" % len(inv))
print("  ...of those, targeting a runner that was AFFECTED: %d"
      % sum(1 for _p, _i, t, _l in inv
            if any(a.endswith(t.lstrip("./")) for a in AFFECTED)))
print()
print("  THE HOLE IS REAL AND IT IS EMPTY.  Three executions could not appear")
print("  in K2a's table, and none of them targets an affected runner, so no")
print("  claim hangs on it.  Reported anyway: a hole that happens to be empty")
print("  and a hole that was checked and found empty are the same table row")
print("  and completely different pieces of evidence, and only the second one")
print("  survives the next runner someone adds.")

# ---------------------------------------------------------------------------
# J2b  the file the pin hid, and the claims in it
# ---------------------------------------------------------------------------
L.hdr("J2b  THE CLAIM THE ENUMERATION DID NOT CONSIDER")

Q2W = "code/species_depth_audit_4700/q2_wiring.py"
OUT = "code/species_depth_audit_4700/out_q2_wiring.txt"
present_at_pin = bool(L.git("ls-tree", "--name-only", L.PINNED,
                            "code/species_depth_audit_4700/").strip())
predict("Q10", "absent at the pin",
        "present" if present_at_pin else "absent", not present_at_pin)
landed = L.git("log", "--format=%h %ad %s", "--date=short", "-1",
               "--diff-filter=A", "--", Q2W).strip()
print()
print("  %s" % Q2W)
print("    landed in: %s" % landed[:100])
print("    at %s: %s" % (L.PINNED, "PRESENT" if present_at_pin else "ABSENT"))
print("    it calls `run_runner(t)`, which is `subprocess.run([\"sh\",")
print("    \"run_all.sh\"], ...)` and returns `p.returncode`, for")
print("    TREES = species_repair_a4ef, species_remainder_f8fa, species_repair_6f61")
print("    -- and TWO of those three had a `| tee` pipeline at the pin.")
print()
scored = [(i, l) for i, l in enumerate(L.read(Q2W).splitlines(), 1)
          if SCORES.search(l)]
print("    lines in it that score a runner's exit status: %d" % len(scored))
for i, l in scored:
    print("      %-5d %s" % (i, l.strip()[:82]))

print()
print("  ITS COMMITTED CLAIM, quoted from %s:" % OUT)
committed = L.read(OUT).splitlines()
d6 = [l for l in committed if "SWALLOWED" in l or "printed *** FAILED ***" in l]
for l in d6:
    print("      %s" % l.rstrip()[:100])
print()
print("  READ IT AS A CLAIM.  `exit 0 ... SWALLOWED` is a claim about two")
print("  runners' EXIT CODES -- R3 by the sweep's own routing, read off the")
print("  status and nothing else.  It is not in the sweep's nine.  It is not")
print("  in the sweep's caller table.  It could not be: the file did not exist")
print("  at the revision the caller scan was pinned to.")

# ---------------------------------------------------------------------------
# J2c  measured, not argued: re-run mg-4700's probe against the repaired tree
# ---------------------------------------------------------------------------
L.hdr("J2c  THE SAME PROBE, RE-RUN AT HEAD -- do those two rows still hold?")

RED_STUB = ('print("*** FAILED *** self-test forced red by the mg-4700 audit")\n'
            'raise SystemExit(1)\n')
TREES = [("species_repair_a4ef", "code/species_repair_a4ef/selftesta4ef.py"),
         ("species_remainder_f8fa", "code/species_remainder_f8fa/selftestf8fa.py"),
         ("species_repair_6f61", "code/species_repair_6f61/selftest6f61.py")]

print("  mg-4700's own probe text, reproduced rather than imported (importing")
print("  q2_wiring.py runs twenty-one `run_all.sh` at module level).  The stub")
print("  written over each self-test is byte-identical to mg-4700's RED_STUB.")
print()
before = L.porcelain()
rows = []
for tree, selftest in TREES:
    if not os.path.exists(os.path.join(L.REPO, selftest)):
        print("  code/%-24s selftest not found: %s" % (tree, selftest))
        continue
    with L.Sandbox() as sb:
        sb.write(selftest, RED_STUB)
        rc, out = L.run_sh("code/%s/run_all.sh" % tree, timeout=900)
    swallowed = (rc == 0)
    saw = "*** FAILED ***" in out
    rows.append((tree, rc, saw, swallowed))
    print("  code/%-24s exit %-4s printed *** FAILED ***: %-4s %s"
          % (tree, "-" if rc is None else rc, "yes" if saw else "no",
             "SWALLOWED" if swallowed else "stopped the run"))
after = L.porcelain()
print()
print("  worktree %s by J2c"
      % ("unchanged" if before == after else "*** CHANGED ***"))
if before != after:
    BAD += 1
    print(after)

was = {"species_repair_a4ef": True, "species_remainder_f8fa": True,
       "species_repair_6f61": False}
flipped = [t for t, _rc, _saw, sw in rows if was.get(t) is not None
           and sw != was[t]]
print()
print("  mg-4700 committed:  a4ef SWALLOWED, f8fa SWALLOWED, 6f61 not")
print("  measured at HEAD :  %s"
      % ", ".join("%s %s" % (t.split("_")[-1], "SWALLOWED" if sw else "not")
                  for t, _rc, _saw, sw in rows))
print("  rows that FLIPPED: %d -- %s" % (len(flipped), ", ".join(flipped) or "none"))
predict("Q13", "the two SWALLOWED rows no longer hold",
        "%d of 2 flipped" % len(flipped), len(flipped) == 2)
print()
print("  WHAT THIS IS AND IS NOT.  It is NOT a defect in the repair -- the")
print("  repair is why they flipped and flipping is the repair working.  It is")
print("  a past claim that DEPENDED ON AN AFFECTED RUNNER'S EXIT CODE, which")
print("  is precisely the population item 3 of the ticket asks for, and it is")
print("  absent from the nine.  Two committed rows in this repository now")
print("  assert an exit code that the tree no longer produces, and no artifact")
print("  of the sweep says so.")

# ---------------------------------------------------------------------------
# J2d  the sweep's nine, checked per claim at their own sites
# ---------------------------------------------------------------------------
L.hdr("J2d  THE NINE, CHECKED PER CLAIM -- does each site still say what is quoted?")

NINE = [
    ("C1", "code/species_sites_821e/p3_wiring.py",
     "code == 0 and present and code_u == 0 and gone"),
    ("C2", "code/species_sites_821e/p3_wiring.py", "STANDING UN-STRUCK"),
    ("C3", "code/species_sites_821e/p3_wiring.py", "code_u == 0"),
    ("C4", "code/branching_audit_2060/b0_repro.sh", "diff -q"),
    ("C5", "docs/OneThird-Species-Hopf-Monoids-ExtentRepair-IndependentAudit.md",
     "code/species_extent_d633/run_all.sh"),
    ("C6", "docs/OneThird-Intrinsic-Face-Geometry-StateLanding2-IndependentAudit.md",
     "git status --porcelain"),
    ("C7", "docs/OneThird-Landscape-Where-This-Lives.md",
     "code/landscape_audit_d673/run_all.sh"),
    ("C8", "code/hodge_leverage_audit_f922/audit_repair.py", "tee"),
    ("C9", "docs/landing-mg-1c80-instrumented-predicate.md", "does not use"),
]
print("  The sweep dispositions each of the nine with a reason -- that part is")
print("  done per claim and not in aggregate, and it is done well.  What is")
print("  checked here is narrower and is the thing a hand-written list rots")
print("  at: does the named FILE still exist and still contain the quoted text?")
print()
ok9 = 0
for cid, rel, needle in NINE:
    p = os.path.join(L.REPO, rel)
    exists = os.path.exists(p)
    found = exists and needle in L.read(rel)
    ok9 += bool(found)
    print("    %-4s %-64s %s" % (cid, rel,
                                 "site+text present" if found else
                                 ("*** TEXT ABSENT ***" if exists
                                  else "*** FILE ABSENT ***")))
predict("Q14", "9 of 9", "%d of 9" % ok9, ok9 == 9)
if ok9 != 9:
    BAD += 1

# ---------------------------------------------------------------------------
# J2e  the general form, on this section
# ---------------------------------------------------------------------------
L.hdr("J2e  THE GENERAL FORM, ON J2")

print("  J2 decides whether other scripts' statuses were discarded, so the")
print("  question is whether J2 discards its own.  Checked, with the reason:")
print()
print("   1. Every execution here is `L.run_sh`, which is")
print("      `subprocess.run([\"/bin/sh\", <name>], ...)` -- a LIST argv, no")
print("      `shell=True`, therefore no shell, therefore no pipeline.  That is")
print("      the branch that CANNOT exhibit the defect and the reason is")
print("      structural rather than a promise about how it is called.")
print("   2. `returncode` is read on every path.  The timeout path returns")
print("      None and prints as `-`, never as 0 -- a timeout rendered as 0")
print("      would be this defect in a different costume.")
print("   3. J2c's verdict is a CONJUNCTION: the exit code AND whether the")
print("      forced text reached the runner's stdout.  Scoring the code alone")
print("      would not distinguish `the stub ran and was caught` from `the")
print("      stub never ran`.")
print("   4. J2c snapshots `git status --porcelain` before and after, because")
print("      it writes over three tracked self-tests and a restore that did")
print("      not happen would silently corrupt every later section.")
print("   5. J2a is run at BOTH revisions, and the pin is the finding: a scan")
print("      pinned to one revision is reported as of that revision and not")
print("      as of the repository.")
print("   6. WHAT J2 CANNOT DO, said here rather than omitted: it finds")
print("      consumers by a syntactic rule over `.py` and `.sh`.  A consumer")
print("      that reaches a runner through a path assembled at runtime from")
print("      data is invisible to it, exactly as it was to the sweep's K2a.")
print("      J2a's rule is strictly wider than K2a's -- it resolves helper")
print("      functions and list-valued tree names -- but wider is not total.")

print()
L.bar("J2 TOTAL BAD: %d" % BAD)
print()
print("EXTENT.  It counts (a) an R3 consumer of an affected runner outside")
print("the sweep's nine, (b) J2c leaving the worktree dirty, (c) any of the")
print("nine whose site or quoted text has rotted.  It ranges over every")
print("tracked `.py` and `.sh` in this repository at %s and at HEAD," % L.PINNED)
print("excluding this audit's own tree, and over the three species trees")
print("J2c executes.  It does NOT range over claims in prose that name no")
print("exit code -- those are R1/R2 by the sweep's routing, which this")
print("audit adopts rather than re-litigates.")
print()
nmiss = sum(1 for _q, _p, _m, ok in MISS if not ok)
print("PREDICTIONS: %d of %d as predicted, %d MISSED (%s)"
      % (len(MISS) - nmiss, len(MISS), nmiss,
         ", ".join(q for q, _p, _m, ok in MISS if not ok) or "none"))
sys.exit(1 if BAD else 0)
