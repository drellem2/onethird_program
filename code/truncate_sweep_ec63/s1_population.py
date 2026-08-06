"""mg-ec63 / S1 -- THE POPULATION, RE-DERIVED, AND WHERE IT DISAGREES WITH 86.

The ticket hands me three numbers -- 109 runners, 86 truncating, 43 biting --
and says in capital letters to re-derive them before building on them.  This
probe re-derives the first two.  S2 re-derives the third.

WHAT A NUMBER HERE MEANS.  Every count is printed with the population it is
taken over and the unit one of it counts, because this arc has now twice
produced a rigorous count of the wrong population.  Two counts that agree at a
total are not two counts over the same set: see D-2 in PREDICTIONS.md, where my
109 and mg-03d1's 109 are shown to be different sets.

Exit code = the number of runners this resolver could not fully parse.  A
non-zero exit here is a statement about MY instrument, not about the arc.
"""

import collections
import os
import sys

import lib_ec63 as B

print("mg-ec63 / S1 -- THE POPULATION OF THE TRUNCATE-BEFORE-PROBE SHAPE")
print("HEAD: %s" % B.head())

# ---------------------------------------------------------------------------
B.hdr("S1a  THE RUNNERS")

TREES = B.trees()
print("  population: directories under `code/` holding a `run_all.sh`,")
print("  enumerated by the glob `code/*/run_all.sh` -- a PROPERTY, not a list.")
print()
B.plain("...RUNNERS in the arc", len(TREES), "one `run_all.sh`")
alldirs = [d for d in sorted(os.listdir(os.path.join(B.REPO, "code")))
           if os.path.isdir(os.path.join(B.REPO, "code", d))]
B.plain("...DIRECTORIES under `code/`", len(alldirs), "one directory")
B.plain("...of those, holding NO runner", len(alldirs) - len(TREES),
        "one directory")
print()
print("  mg-03d1's sweep also says 109.  THE TOTALS AGREE AND THE POPULATIONS")
print("  DO NOT: its count includes `code/grain_axis_audit_03d1`, its own tree,")
print("  which is not on this branch --")
print("      code/grain_axis_audit_03d1 present here:  %s"
      % ("yes" if "code/grain_axis_audit_03d1" in TREES else "NO"))
print("  -- so at least one member of its 109 is not a member of mine, and the")
print("  two 109s cannot both be over the same set.  A number that matches is")
print("  not a population that matches.")

# ---------------------------------------------------------------------------
B.hdr("S1b  HOW EACH RUNNER WRITES ITS TRANSCRIPTS")

print("  Resolved by walking the shell, not by matching its text.  The arc has")
print("  at least SIX runner idioms and they disagree about ARGUMENT ORDER:")
print()
print("      python3 X.py > out_X.txt                    direct")
print("      run <probe> <out>                           helper, probe first")
print("      run <out> <probe>                           helper, OUT first")
print("      expect <code> <probe>, out from the stem    helper, derived name")
print("      run <name> ; python3 \"$HERE/$name.py\"       helper, no extension")
print("      for s in a b c ; python3 \"$s.py\" > out_$s   a LOOP, N steps not 1")
print()
print("  A regex keyed on `python3 ... > out_` gets the second wrong (it reads")
print("  the transcript as the probe), cannot see the third or fourth at all,")
print("  and counts the sixth once.")
print()

steps = {}
unres = {}
for t in TREES:
    s, u = B.parse_runner(t)
    steps[t] = s
    unres[t] = u

nsteps = sum(len(v) for v in steps.values())
B.plain("...STEPS resolved across all %d runners" % len(TREES), nsteps,
        "one (probe, transcript, operator) triple")
op_of_tree = {}
for t in TREES:
    ops = set(o for _, _, o in steps[t])
    if "TRUNC" in ops:
        op_of_tree[t] = "TRUNC"
    elif "STRUCT" in ops:
        op_of_tree[t] = "STRUCT"
    elif "APPEND" in ops:
        op_of_tree[t] = "APPEND"
    elif "STREAM" in ops:
        op_of_tree[t] = "STREAM"
    else:
        op_of_tree[t] = "NONE"
c = collections.Counter(op_of_tree.values())
print()
print("  population: the %d RUNNERS of S1a, classified by the STRONGEST"
      % len(TREES))
print("  operator any one of their steps uses (a runner with one `>` step is a")
print("  truncating runner, whatever else it does):")
print()
B.plain("...RUNNERS that truncate a transcript with a plain `>`", c["TRUNC"],
        "one `run_all.sh`")
B.plain("...RUNNERS with the `.new`+`mv` structural fix", c["STRUCT"],
        "one `run_all.sh`")
B.plain("...RUNNERS that only append with `>>`", c["APPEND"], "one `run_all.sh`")
B.plain("...RUNNERS that write NO transcript (stdout only)", c["STREAM"],
        "one `run_all.sh`")
B.plain("...RUNNERS with no python step this resolver found", c["NONE"],
        "one `run_all.sh`")
print()
for t in sorted(t for t in TREES if op_of_tree[t] == "STRUCT"):
    print("      STRUCTURAL FIX: %s" % t)
print()
print("  I MAKE IT %d TRUNCATING, NOT 86, over a population of %d."
      % (c["TRUNC"], len(TREES)))
print("  The gap is not a disagreement about the arc; it is a disagreement")
print("  about the RULE.  %d runners here write no transcript at all and are"
      % c["STREAM"])
print("  in no truncation population -- `code/state_claims_repair_0120` streams")
print("  every section to stdout, and its transcript is captured outside the")
print("  runner.  Those are not fixed and are not broken; they are not members.")

# ---------------------------------------------------------------------------
B.hdr("S1c  WHAT THE RESOLVER REFUSED TO GUESS AT")

bad = [(t, u) for t, u in sorted(unres.items()) if u]
print("  population: the %d RUNNERS of S1a" % len(TREES))
B.plain("...RUNNERS with at least one UNRESOLVED line", len(bad),
        "one `run_all.sh`")
B.plain("...UNRESOLVED lines in total", sum(len(u) for u in unres.values()),
        "one shell statement")
print()
print("  Printed rather than binned.  A resolver that reports zero unresolved")
print("  lines over 109 hand-written shell scripts is guessing somewhere.")
print()
for t, u in bad:
    for ln in u:
        print("      %-40s %s" % (t.replace("code/", ""), ln.strip()[:110]))
print()
print("  Each is a `cd` into another directory or a `python3 -c`, so the probe")
print("  it names is NOT resolvable against this tree.  They are excluded from")
print("  the step population and counted here instead of guessed at.")

# ---------------------------------------------------------------------------
B.hdr("S1d  THE STEPS THAT CAN ACTUALLY BITE, AND WHY THE FILTER IS THIS ONE")

print("  A `>` empties a file that HAD BYTES.  A step whose transcript is not")
print("  committed empties nothing on a clean checkout -- there was no content")
print("  for the probe to miss.  So the population S2 sweeps is:")
print()
print("      a step with operator TRUNC whose transcript EXISTS in the tree.")
print()
cand = []
for t in TREES:
    for p, o, op in steps[t]:
        if op == "TRUNC" and o and os.path.exists(os.path.join(B.REPO, o)):
            cand.append((t, p, o))
ntrunc = sum(1 for t in TREES for _, _, op in steps[t] if op == "TRUNC")
B.plain("...TRUNC steps in total", ntrunc, "one step")
B.plain("...of those, whose transcript is COMMITTED", len(cand), "one step")
B.plain("...of those, whose transcript is NOT in the tree", ntrunc - len(cand),
        "one step")
B.plain("...RUNNERS contributing at least one such step",
        len(set(t for t, _, _ in cand)), "one `run_all.sh`")

B.save("population", {
    "head": B.head(),
    "trees": TREES,
    "steps": {t: steps[t] for t in TREES},
    "op_of_tree": op_of_tree,
    "candidates": cand,
    "unresolved": {t: u for t, u in unres.items() if u},
})

print()
print("S1 TOTAL UNRESOLVED RUNNERS: %d" % len(bad))
sys.exit(min(len(bad), 120))
