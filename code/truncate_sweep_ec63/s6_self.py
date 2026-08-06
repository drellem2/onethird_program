"""mg-ec63 / S6 -- THE DEFECTS OF THIS INSTRUMENT.

Every audit in this arc that has looked has found its own subject inside itself.
mg-bf79 found the truncate-before-probe shape in the runner of the repair of
that shape.  mg-03d1's sweep swallowed the auditor the moment the auditor
adopted the fix, and then ran itself.  So this section is not a formality.

Each item is MEASURED here, not asserted.  Exit code = defects found.
"""

import os
import re
import sys

import lib_ec63 as B

print("mg-ec63 / S6 -- THE DEFECTS OF THIS INSTRUMENT")
print("HEAD: %s" % B.head())

DEFECTS = 0


def defect(tag, title):
    global DEFECTS
    DEFECTS += 1
    print()
    print("  %-5s %s" % (tag, title))


# ---------------------------------------------------------------------------
B.hdr("S6a  THE POPULATION SWALLOWS ME, AND BOTH NUMBERS ARE PRINTED")

TREES = B.trees()
mine_in = B.MINE in TREES
steps, un = B.parse_runner(B.MINE) if mine_in else ([], [])
ops = sorted(set(o for _, _, o in steps))

defect("SD1", "this tree is a member of the population it counts")
print("        `code/*/run_all.sh` is a property, and the moment this suite")
print("        has a runner it satisfies it.  mg-03d1 recorded exactly this")
print("        and its A4b prediction went from right to wrong because of it.")
print()
B.plain("...RUNNERS in the arc, including mine", len(TREES), "one `run_all.sh`")
B.plain("...RUNNERS of the arc this sweep is ABOUT",
        len(TREES) - (1 if mine_in else 0), "one `run_all.sh`")
print()
print("      my own runner's operators: %s" % (", ".join(ops) or "(none yet)"))
if "TRUNC" in ops:
    defect("SD1b", "AND MY OWN RUNNER CARRIES THE DEFECT I AM SWEEPING FOR")
else:
    print("      -- it uses the structural fix, so this suite is not an")
    print("         instance of its own subject.  Which is the ONLY reason")
    print("         S3's numbers are not partly about itself.")

# ---------------------------------------------------------------------------
B.hdr("S6b  THE TRACE HOOK CANNOT SEE OUTSIDE ITS OWN PROCESS")

bite = B.load("bite") or {"recs": []}
recs = bite["recs"]
subp = 0
for r in recs:
    try:
        src = B.read(r["probe"])
    except OSError:
        continue
    if re.search(r"\bsubprocess\.|os\.system|os\.popen", src):
        subp += 1

defect("SD2", "the audit hook cannot see a NON-PYTHON child")
print("        `EC63_TRACE` and `PYTHONPATH` are inherited, so a probe that")
print("        spawns another PYTHON process IS traced -- and the pid tells")
print("        the child's opens from the parent's, which S2b now counts")
print("        apart.  A probe that reads a transcript by spawning `cat` or")
print("        `grep` is still invisible: no Python, no audit hook.  That is")
print("        a FALSE NEGATIVE of the same kind as the text rule's, one layer")
print("        further in, and the number of probes it could apply to is:")
print()
B.plain("...STEPS run in S2 whose probe spawns a subprocess at all", subp,
        "one step")
B.plain("...STEPS run in S2 in total", len(recs), "one step")
print()
print("      Most of those `subprocess` calls are `git`, not `cat`.  The bound")
print("      is stated as a BOUND -- %d is the most this could have cost --" % subp)
print("      rather than as a measurement of what it did cost, because")
print("      measuring that needs a second instrument this ticket did not")
print("      build.")

# ---------------------------------------------------------------------------
B.hdr("S6c  TWO DEFECTS FOUND IN THIS RESOLVER BY ITS OWN SELFTEST")

defect("SD3", "the resolver invented probes called `can`, `the` and `ridge`")
print("        `step \"F2: can the V6 row go red?\" f2.py` was split on")
print("        whitespace, so argument 2 was the word `can`.  Three trees'")
print("        steps were wrong and every one of them looked like a filename.")
print("        Found by validating each parsed path against the disk, not by")
print("        reading the output.  Fixed with `shlex`; T3 holds the line.")

wr = sum(1 for r in recs if r.get("own_write"))
defect("SD3a", "the trace counted a WRITE as a READ, and then I MISATTRIBUTED "
               "the evidence for it")
print("        `sys.addaudithook`'s `open` event fires for both, and the first")
print("        version of this hook logged only the path.  A probe that WROTE")
print("        its own transcript would have been recorded as READING the file")
print("        its run had emptied -- the exact false positive this suite was")
print("        built to remove from the text rule, one layer further in.")
print("        The hook now records the mode.  MEASURED EFFECT: %d steps of the"
      % wr)
print("        %d write their own transcript, so the fix changed no count."
      % len(recs))
print()
print("        AND THAT IS THE HALF WORTH KEEPING.  What sent me looking was")
print("        two transcripts left MODIFIED by an early pass, and I wrote")
print("        into the instrument that their own probes had written them.")
print("        They had not: probes of OTHER trees wrote them, having been")
print("        killed by this suite's timeout before their cleanup could run.")
print("        A rigorous fix, a confident mechanism, and the mechanism was")
print("        wrong -- which is this arc's own recurring failure, committed")
print("        here inside the sweep for it.  The real defect is SD6c.")

defect("SD3b", "the restore rested on the files happening to be TRACKED")
print("        `run_probe` emptied a transcript and put it back with")
print("        `git checkout --`.  Git cannot restore a file it does not")
print("        track, so on T4's untracked fixture the transcript stayed")
print("        empty -- and the assertion that CHECKS the restore is the")
print("        thing that caught it.  Every tree in the sweep is tracked, so")
print("        no number here was ever affected; the guarantee was resting on")
print("        a coincidence, which is this ticket's own subject.  `run_probe`")
print("        now keeps the bytes itself and writes them back.")

defect("SD4", "a `shift` on the same line as an assignment was invisible")
print("        `want=\"$1\"; shift` is two statements and was read as one, so")
print("        every positional parameter after it was off by one and the")
print("        `expect` trees resolved to a probe named `0`.  Fixed by")
print("        splitting on `;`; T1 carries both argument orders side by side")
print("        because that is the error that does not look like an error.")

# ---------------------------------------------------------------------------
B.hdr("S6d  WHAT THE COMMENT STRIPPER THROWS AWAY")

hashy = 0
for t in TREES:
    src = B.read("%s/run_all.sh" % t)
    for ln in src.splitlines():
        s = ln.strip()
        if s.startswith("#"):
            continue
        if " #" in ln and (ln.count('"') % 2 or ln.count("'") % 2):
            hashy += 1

defect("SD5", "a `#` inside an unbalanced quote is treated as a comment")
B.plain("...RUNNER LINES where that could bite", hashy, "one line")
print("      Bounded rather than fixed.  A shell parser that gets quoting")
print("      exactly right is a different program; this one reports the lines")
print("      it could be wrong about and reports 3 UNRESOLVED besides.")

# ---------------------------------------------------------------------------
B.hdr("S6d2  THE ARC RAN THIS SUITE'S OWN RUNNER, MID-RUN")

log = os.path.join(B.HERE, "recursion_ec63.log")
lines = []
if os.path.exists(log):
    with open(log, errors="replace") as f:
        lines = [ln.rstrip("\n") for ln in f if ln.strip()]
n_ref = sum(1 for ln in lines if ln.startswith("REFUSED"))
B.plain("...RECURSIVE INVOCATIONS of this runner, refused", n_ref,
        "one attempted run")
print()
if n_ref:
    defect("SD6e", "a probe of the arc EXECUTED THIS SUITE'S RUNNER while it "
                   "was running")
    print("        Several of the arc's probes execute runners they find on")
    print("        disk.  Once this directory had a `run_all.sh`, it became")
    print("        one of them.  A second run in this directory shares the")
    print("        `out_*.txt.new` paths with the first, so it TRUNCATES THE")
    print("        TRANSCRIPT THE OUTER RUN IS STILL WRITING -- which is the")
    print("        defect this whole ticket is about, arriving from OUTSIDE")
    print("        the tree rather than from its own runner.  It destroyed")
    print("        this suite's S2 transcript twice before the cause was")
    print("        found, and what it left behind was a ZERO-BYTE transcript")
    print("        beside a summary with the S2 line simply missing.  A")
    print("        vacuous pass of exactly the shape being swept for.")
    print()
    print("        WHO ASKED, as recorded at the moment the guard fired:")
    for ln in lines[:24]:
        print("          %s" % ln[:130])
    if len(lines) > 24:
        print("          ... and %d further lines" % (len(lines) - 24))
else:
    print("      None this run.  The guard is in `run_all.sh` and fires on an")
    print("      inherited `EC63_RUNNING`, so a zero here means no probe this")
    print("      suite started tried to run this suite -- not that the guard")
    print("      is untested: it is what this transcript exists to record.")

# ---------------------------------------------------------------------------
B.hdr("S6e  DID THE SWEEP LEAVE THE ARC AS IT FOUND IT?")

porc = [ln for ln in B.git("status", "--porcelain", "--", "code",
                           "docs").splitlines()
        if ln.strip() and B.MINE not in ln]
print("  population: `git status --porcelain -- code/ docs/`, less this tree")
print("  and `restore_arc()` walks EVERY DIRECTORY under `code/`, not every")
print("  RUNNER: 7 directories have no runner, and one of them is where a")
print("  killed probe kept leaving an armed shell script.  A restore scoped to")
print("  the population being MEASURED misses exactly the places the")
print("  measurement spills into.")
print("  `docs/` is in the population because two probes of this arc APPEND A")
print("  SECTION to the prose and undo it in a `finally` -- which a killed")
print("  probe never reaches.  A sweep that checks only `code/` reports itself")
print("  clean with the arc's documentation edited.")
B.plain("...LINES of change outside this tree", len(porc), "one status line")
for ln in porc[:20]:
    print("      %s" % ln)
if porc:
    defect("SD6", "THE SWEEP LEFT SOMETHING BEHIND")
    print("        Every probe is restored with `git checkout -- <its tree>`.")
    print("        A probe that writes into ANOTHER tree is outside that scope,")
    print("        and this is the check that says so.")
else:
    print()
    print("      Clean.  Every one of the probes run by S2/S3/S5 was restored,")
    print("      including the ones that write.")

# ---------------------------------------------------------------------------
B.hdr("S6f  THE ONE THIS SUITE CANNOT ANSWER ABOUT ITSELF")

nto = sum(1 for r in recs if r["timeout"])
if nto:
    defect("SD6b", "%d of %d steps were KILLED before they could answer"
           % (nto, len(recs)))
    print("        A probe killed at the timeout may never have reached the")
    print("        line that opens its own transcript.  S2 records it as")
    print("        not-reading, and the truth is not-known.  Every count in")
    print("        S2b is a LOWER BOUND, and S2a says so where the number is")
    print("        printed rather than in a footnote.  The population that is")
    print("        exact is the %d steps that finished." % (len(recs) - nto))

ch = sum(1 for r in recs if r.get("own_child") and not r.get("own"))
defect("SD6d", "the first pass ATTRIBUTED A CHILD'S READ TO ITS PARENT, and "
               "the two numbers it produced disagreed inside one run")
print("        Before the pid went into the trace, a subprocess's opens were")
print("        recorded against the probe that spawned it.  That is not merely")
print("        wrong, it is UNSTABLE: whether a child reaches the read depends")
print("        on load, so `face_geometry_instr_5f9a/d3_reintroduction.py` came")
print("        out reading its own transcript under the parallel pass and not")
print("        reading it when run alone.  The tell was arithmetic: S2 printed")
print("        37 EMPTIED steps and S3, reading the same ledger, swept 36.")
print("        A suite whose own two sections disagree by one is the shape")
print("        this whole ticket is about, committed by the sweep for it.")
print()
B.plain("...STEPS now attributed to a CHILD rather than the probe", ch,
        "one step")

defect("SD6f", "the sweep's own transcript was DESTROYED BY THE ARC IT "
               "WAS SWEEPING, twice")
print("        Two full passes produced a ZERO-BYTE `out_s2_bite.txt` beside")
print("        an exit code of 32 -- the probe ran, found 32 emptied steps,")
print("        and its transcript was gone.  The summary that reads every")
print("        `S[0-9] TOTAL` line out of the transcripts simply had no S2")
print("        row: A VACUOUS PASS OF EXACTLY THE SHAPE THIS TICKET IS ABOUT,")
print("        produced by the sweep for it.  A 40-step subset of the same")
print("        probe writes its transcript perfectly, so the destroyer is one")
print("        of the arc's own probes and not this code -- and I did not")
print("        identify WHICH.  That is in README.md under WHAT I DID NOT DO.")
print("        The repair is structural rather than another guard: a suite")
print("        that runs 422 of the arc's probes cannot keep its in-flight")
print("        output inside the arc.  Every transcript, the ledger, the shim")
print("        and the trace files now live under `$EC63_WORK` outside the")
print("        repository, and land in the tree only after the last probe has")
print("        exited -- the only moment nothing else is running.")

defect("SD7", "A and B are two runs, not one run observed twice")
print("        `diff(A, B)` is attributed to the shape.  The determinism")
print("        control in S3 re-runs B and drops any step where B != B', which")
print("        catches a probe that varies BETWEEN RUNS.  It does not catch a")
print("        probe that varies WITH THE CLOCK in a way that happens to be")
print("        stable across two adjacent runs and not across the minutes")
print("        between A and B.  No row is currently attributed to that, and")
print("        no row is currently ruled out of it either.")

print()
print("S6 TOTAL DEFECTS OF THIS INSTRUMENT: %d" % DEFECTS)
sys.exit(min(DEFECTS, 120))
