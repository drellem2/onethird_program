"""mg-18dc / V2 -- 86, RE-DERIVED BY EXECUTION RATHER THAN BY READING.

mg-03d1 got 86 with a regex.  mg-ec63 got 96 with a shell parser and said the
regex was wrong.  Both are STATEMENTS ABOUT SOURCE TEXT, and an audit that
writes a third rule of the same kind can only join the argument.

So this does not read the runner at all.  It RUNS it, in a disposable clone,
with `python3` replaced by a stub that writes a fixed marker and records the
size of every `out_*.txt` in its directory AT THE INSTANT IT IS INVOKED.  Then:

    a transcript is EMPTY WHEN ITS PROBE STARTS   <- the defect, observed
    a transcript still holds bytes                <- no defect, observed

The stub writes a marker rather than nothing on purpose: a silent stub leaves
every transcript at zero bytes and makes `.new`+`mv` look exactly like `>`,
which is the collapse this whole ticket is about.

Population is mg-03d1's own: the runners at d33970b, the revision where its 109
reproduces.  Same tree state, different instrument.  That is the only way a
disagreement means anything.

Exit code = runners where my rule and mg-03d1's rule disagree.
"""

import os
import re
import sys

import lib18dc as B

REV = "d33970b"

print("mg-18dc / V2 -- TRUNCATION, MEASURED BY RUNNING THE SHELL")
print("HEAD: %s" % B.head())
print("MEASURED AT: %s  (mg-03d1's own audit commit)" % REV)

sbx = B.sandbox(REV)
TREES = B.runners_at(REV)

# ---------------------------------------------------------------------------
B.hdr("V2a  RUNNING ALL %d RUNNERS WITH `python3` STUBBED" % len(TREES))

print("  Each runner is executed once.  Nothing it calls does any work: every")
print("  `python3` is a stub that writes %r and exits 0." % B.MARKER.strip())
print("  What is recorded is the SHELL's behaviour -- which files it truncates,")
print("  in what order, relative to the probe invocations.")
print()

rows = {}
for t in TREES:
    res, err = B.stub_run(sbx, t, timeout=120)
    if err:
        rows[t] = {"status": err, "steps": [], "n": 0}
        continue
    committed = res["committed"]
    steps = []
    for i, r in enumerate(res["rows"]):
        zero_known = sorted(f for f, n in r["snap"].items()
                            if n == 0 and committed.get(f, 0) > 0)
        zero_new = sorted(f for f, n in r["snap"].items()
                          if n == 0 and f not in committed)
        if zero_known or zero_new:
            steps.append({"i": i, "argv": r["argv"],
                          "zero": zero_known, "zero_new": zero_new})
    rows[t] = {"status": res["err"] or "ok", "steps": steps,
               "n": len(res["rows"])}
    B.sandbox_reset(sbx)

ok = [t for t in TREES if rows[t]["status"] == "ok"]
noinvoke = [t for t in ok if rows[t]["n"] == 0]
timedout = [t for t in TREES if rows[t]["status"] == "TIMEOUT"]
trunc = [t for t in TREES if rows[t]["steps"]]
inert = [t for t in ok if not rows[t]["steps"] and rows[t]["n"] > 0]

print("  population: the %d runners tracked at %s" % (len(TREES), REV))
B.plain("...RUNNERS that ran to completion under the stub", len(ok), "one `run_all.sh`")
B.plain("...RUNNERS killed at the 120 s timeout", len(timedout), "one `run_all.sh`")
B.plain("...RUNNERS that invoked no `python3` at all", len(noinvoke), "one `run_all.sh`")
print()
B.plain("...RUNNERS OBSERVED to start a probe on an EMPTY transcript",
        len(trunc), "one `run_all.sh`")
B.plain("...RUNNERS where no probe ever started on an empty one",
        len(inert), "one `run_all.sh`")
print()
print("  EVERY COUNT HERE IS A LOWER BOUND, and the two reasons are printed")
print("  above rather than footnoted: a runner killed at the timeout may")
print("  truncate after the kill, and a runner that invokes no `python3` is")
print("  invisible to an instrument that measures at `python3`.")

# ---------------------------------------------------------------------------
B.hdr("V2b  MY NUMBER, mg-03d1'S 86, AND mg-ec63'S 96")

print("  mg-03d1's rule, applied by me to the same %d runners, from its own" % len(TREES))
print("  source at %s.  A regex over the runner text:" % REV)
print()
TRUNC_RE = re.compile(r"(?<![>2])>\s*[\"']?\$?\{?_?[oO]|(?<![>2])>\s*[\"']?out_")
their = []
for t in TREES:
    src = open(os.path.join(sbx, t, "run_all.sh")).read()
    if re.search(r"\.new", src) and re.search(r"\bmv\b", src):
        continue
    if TRUNC_RE.search(src):
        their.append(t)
print("      mg-03d1  regex over source            %3d   (it printed 86)"
      % len(their))
print("      mg-ec63  shell parser over source     %3s   (it printed 96 over 110)"
      % "-")
print("      mg-18dc  execution of the shell       %3d" % len(trunc))
print()
print("  ^ one unit of each of those is one `run_all.sh`.  The first two are")
print("    over the %d runners at %s; mg-ec63's 96 is over a DIFFERENT" % (len(TREES), REV))
print("    population of 110 at 3fc870a and is not comparable by subtraction.")

fp = [t for t in their if t not in set(trunc)]
fn = [t for t in trunc if t not in set(their)]
print()
print("  population: the %d runners at %s, by whether the two rules agree" % (len(TREES), REV))
B.plain("...RUNNERS both rules call truncating",
        len(set(their) & set(trunc)), "one `run_all.sh`")
B.plain("...RUNNERS the REGEX calls truncating and execution does NOT",
        len(fp), "one `run_all.sh`")
B.plain("...RUNNERS EXECUTION calls truncating and the regex does NOT",
        len(fn), "one `run_all.sh`")
print()
print("  THE REGEX'S FALSE POSITIVES -- source says `>`, no probe ever starts")
print("  on an empty transcript:")
for t in sorted(fp):
    why = rows[t]["status"]
    if rows[t]["n"] == 0:
        why = "no python3 invoked"
    elif why == "ok":
        why = "%d probes, none on an empty file" % rows[t]["n"]
    print("      %-46s %s" % (t.replace("code/", ""), why))
print()
print("  THE REGEX'S FALSE NEGATIVES -- source does not match, and a probe")
print("  demonstrably starts on an empty transcript anyway:")
for t in sorted(fn):
    z = rows[t]["steps"][0]
    print("      %-46s step %d starts with %s empty"
          % (t.replace("code/", ""), z["i"],
             ", ".join(z["zero"] + z["zero_new"])[:40]))

# ---------------------------------------------------------------------------
B.hdr("V2c  AND THE `.new`+`mv` TREES, CHECKED THE SAME WAY")

newmv = []
for t in TREES:
    src = open(os.path.join(sbx, t, "run_all.sh")).read()
    if B.carries_newmv(src):
        newmv.append(t)
print("  population: the %d runners at %s" % (len(TREES), REV))
B.plain("...RUNNERS whose source carries the `.new`+`mv` fix", len(newmv),
        "one `run_all.sh`")
for t in newmv:
    st = rows[t]
    verdict = "NO probe starts on an empty transcript" if not st["steps"] \
        else "*** %d probes DO start on an empty transcript ***" % len(st["steps"])
    print("          %-44s %s" % (t.replace("code/", ""), verdict))
print()
print("  This is the control that makes V2a mean anything.  If my instrument")
print("  called the fixed trees truncating too, it would be measuring `does a")
print("  runner write files` and not `does the fix work`.")

disagree = len(fp) + len(fn)
print()
print("V2 TOTAL RUNNERS WHERE THE RULES DISAGREE: %d" % disagree)
sys.exit(min(disagree, 120))
