"""mg-18dc / V4 -- THE THIRD OUTCOME, WHICH mg-ec63'S RULE CANNOT REACH.

The ticket names three outcomes and says the third is the worst and the easiest
to miss:

    SAME              the probe finds the same answer -- a harmless ordering bug
    DIFFERENT         the probe finds a different answer -- a published figure is wrong
    CANNOT RUN AT ALL the probe was never exercised against real input

mg-ec63 reports the third as **0**.  Its `classify()` (s3_sweep.py:89-106) is
transcribed verbatim below.  Read the branch that produces it:

    b_broke = row["B_to"] or (B_exit is not None and "Traceback" in B_text)
    a_ok    = (not A_to) and "Traceback" not in A_text
    if b_broke and a_ok:  return "NEVER EXERCISED"

**B is the healthy arm** -- the one with the committed transcript in place.
**A is the defect arm** -- the one the arc has actually been shipping.  So that
verdict is reachable only when the HEALTHY arm breaks and the DEFECT arm works.
A probe that cannot run at all breaks in BOTH arms, is therefore `A == B`, and
falls through to **SAME** -- "the ordering bug cost the arc nothing".

So this section re-runs mg-ec63's own SAME and NONDETERMINISTIC rows, at
mg-ec63's own tree state, and asks of each what its A and B arms actually did.

Exit code = steps whose true outcome is not the one mg-ec63 recorded.
"""

import os
import re
import shutil
import subprocess
import sys
import threading

import lib18dc as B

REV = "3fc870a"          # the revision mg-ec63's own transcripts declare
WORKERS = 4
TIMEOUT = 150

# mg-ec63's own S3d listing, transcribed from out_s3_sweep.txt.  These are ITS
# rows, not mine; the point of the section is to re-run them.
SAME = [
    ("code/counterexample_audit_c6bc", "a5_battery.py"),
    ("code/counterexample_audit_c6bc", "check_locator.py"),
    ("code/hash_population_6e58", "p4_gate.py"),
    ("code/runner_exit_audit_dee4", "a1_outside.py"),
    ("code/runner_exit_repair_70c7", "r3_strength.py"),
    ("code/runner_exit_repair_7522", "s5_self.py"),
    ("code/species_bound_audit_6ef4", "selftest6ef4.py"),
    ("code/species_bound_audit_6ef4", "t4_restore.py"),
    ("code/species_extent_d633", "selftestd633.py"),
    ("code/species_extent_d633", "e3_bothways.py"),
    ("code/species_rung_repair_4adb", "v3_self.py"),
]
NDET = [
    ("code/audit_2c77", "q3_operands.py"),
    ("code/audit_330a", "s4_term.py"),
    ("code/hodge_leverage_audit_97fb", "audit_97fb.py"),
    ("code/repair_69d1", "p3_reason.py"),
    ("code/repair_8d5e", "r4_self.py"),
    ("code/repair_b2af", "t3_term.py"),
    ("code/runner_exit_repair_70c7", "r2_anchor.py"),
    ("code/species_bound_audit_6ef4", "t1_bound.py"),
    ("code/species_bound_repair_5040", "selftest5040.py"),
    ("code/species_bound_repair_5040", "r1_bound.py"),
    ("code/species_bound_repair_5040", "r3_summaries.py"),
    ("code/species_bound_repair_5040", "r4_self.py"),
    ("code/species_repair_a4ef", "s1_extent.py"),
    ("code/species_rung_repair_4adb", "v2_layer2.py"),
]
STEPS = [(t, p, "SAME") for t, p in SAME] + [(t, p, "NDET") for t, p in NDET]

print("mg-18dc / V4 -- THE THIRD OUTCOME")
print("HEAD: %s" % B.head())
print("MEASURED AT: %s  (the revision mg-ec63's own transcripts declare)" % REV)

# ---------------------------------------------------------------------------
B.hdr("V4a  WHICH TRANSCRIPT EACH STEP WRITES, DERIVED AND NOT GUESSED")

print("  `a5_battery.py` -> `out_a5_battery.txt` is a convention, not a rule,")
print("  and this arc has six runner idioms that disagree about it.  So the")
print("  mapping is taken from a stubbed run of each tree: the transcript that")
print("  is ZERO BYTES at the instant that probe is invoked is the one that")
print("  probe writes.  Steps whose transcript cannot be derived are dropped")
print("  and named, rather than guessed at.")
print()

sbx0 = B.sandbox(REV, tag="%s-v4" % REV)
mapping = {}
for tree in sorted({t for t, _, _ in STEPS}):
    res, err = B.stub_run(sbx0, tree, timeout=120)
    B.sandbox_reset(sbx0)
    if err or not res:
        continue
    for r in res["rows"]:
        probe = None
        for a in r["argv"]:
            if a.endswith(".py"):
                probe = os.path.basename(a)
        if not probe:
            continue
        zero = [f for f, n in r["snap"].items()
                if n == 0 and res["committed"].get(f, 0) > 0]
        if len(zero) == 1:
            mapping[(tree, probe)] = zero[0]

resolved = [(t, p, w) for t, p, w in STEPS if (t, p) in mapping]
dropped = [(t, p, w) for t, p, w in STEPS if (t, p) not in mapping]
print("  population: mg-ec63's %d SAME and NONDETERMINISTIC steps" % len(STEPS))
B.plain("...STEPS whose transcript this derives", len(resolved), "one step")
B.plain("...STEPS DROPPED, transcript not derivable", len(dropped), "one step")
for t, p, w in dropped:
    print("          dropped: %-34s %s   (%s)" % (t.replace("code/", ""), p, w))

# ---------------------------------------------------------------------------
B.hdr("V4b  RUNNING BOTH ARMS, AND RECORDING WHAT EACH ARM DID")

print("  A = the transcript emptied first (the defect, as shipped).")
print("  B = the committed bytes in place (the probe as it should have run).")
print("  Both arms capture stdout+stderr TO MEMORY and are never redirected")
print("  onto a transcript.  Every arm runs in a disposable clone.")
print()

rows = {}
lock = threading.Lock()
queue = list(resolved)
qlock = threading.Lock()


def arm(sbx, tree, probe, out, empty):
    d = os.path.join(sbx, tree)
    subprocess.run(["git", "checkout", "--quiet", "--", tree], cwd=sbx,
                   capture_output=True)
    if empty:
        open(os.path.join(d, out), "w").close()
    env = dict(os.environ)
    env["PYTHONPATH"] = B.make_shim()
    env["V18_WORK"] = B.child_work(tree)        # SD12 -- see lib18dc.child_work
    led = os.path.join(B.WORK, "v4-%s-%s-%s.tsv"
                       % (tree.replace("/", "_"), probe, "A" if empty else "B"))
    if os.path.exists(led):
        os.remove(led)
    env["V18_READS"] = led
    rec = {"to": False, "exit": None, "text": ""}
    try:
        r = subprocess.run(["python3", "-W", "ignore", probe], cwd=d, env=env,
                           capture_output=True, text=True, timeout=TIMEOUT)
        rec["exit"] = r.returncode
        rec["text"] = (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired as e:
        rec["to"] = True
        rec["text"] = (e.stdout or b"").decode("utf8", "replace") if e.stdout else ""
    rec["read_empty"] = False
    if os.path.exists(led):
        root = os.path.realpath(d)
        for line in open(led):
            pr = line.rstrip("\n").split("\t", 3)
            if len(pr) == 4 and "r" in pr[1] and "+" not in pr[1] \
                    and int(pr[2]) == 0 \
                    and os.path.dirname(os.path.realpath(pr[3])) == root:
                rec["read_empty"] = True
    subprocess.run(["git", "checkout", "--quiet", "--", tree], cwd=sbx,
                   capture_output=True)
    subprocess.run(["git", "clean", "-qfd", "--", tree], cwd=sbx,
                   capture_output=True)
    return rec


def worker(k):
    sbx = B.sandbox(REV, tag="%s-v4w%d" % (REV, k))
    while True:
        with qlock:
            if not queue:
                return
            t, p, w = queue.pop(0)
        out = mapping[(t, p)]
        a = arm(sbx, t, p, out, True)
        b = arm(sbx, t, p, out, False)
        with lock:
            rows[(t, p)] = {"ec63": w, "out": out, "A": a, "B": b}


ths = [threading.Thread(target=worker, args=(k,)) for k in range(WORKERS)]
for th in ths:
    th.start()
for th in ths:
    th.join()


def broke(r):
    return r["to"] or "Traceback" in r["text"]


def mine(r):
    a, b = r["A"], r["B"]
    if broke(a) and broke(b):
        return "CANNOT RUN AT ALL"
    if broke(a) and not broke(b):
        return "BREAKS ONLY UNDER THE DEFECT"
    if broke(b) and not broke(a):
        return "NEVER EXERCISED (ec63 sense)"
    if a["text"] == b["text"]:
        return "INERT READ" if a["read_empty"] else "SAME (no read observed)"
    return "DIFFERENT"


def ec63_classify(r):
    """mg-ec63's rule, transcribed verbatim from s3_sweep.py:89-106."""
    a, b = r["A"], r["B"]
    if a["to"] and not b["to"]:
        return "A TIMED OUT"
    if a["to"] and b["to"]:
        return "BOTH TIMED OUT"
    b_broke = b["to"] or (b["exit"] is not None and "Traceback" in b["text"])
    a_ok = (not a["to"]) and "Traceback" not in a["text"]
    if b_broke and a_ok:
        return "NEVER EXERCISED"
    if a["text"] == b["text"]:
        return "SAME"
    return "DIFFERENT"


order = ["CANNOT RUN AT ALL", "BREAKS ONLY UNDER THE DEFECT",
         "NEVER EXERCISED (ec63 sense)", "DIFFERENT", "INERT READ",
         "SAME (no read observed)"]
counts = {k: 0 for k in order}
for r in rows.values():
    counts[mine(r)] += 1

print("  population: the %d steps of V4a whose transcript was derived" % len(rows))
for k in order:
    B.plain("...STEPS %s" % k, counts[k], "one step")
print()
print("  THE SAME ROWS, ONE PER LINE, WITH BOTH ARMS' EXIT STATUS:")
print()
print("      %-36s %-22s %-10s %-10s %s"
      % ("TREE :: PROBE", "MY VERDICT", "A", "B", "ec63"))
mismatch = 0
for (t, p), r in sorted(rows.items()):
    v = mine(r)
    e = ec63_classify(r)
    astat = "TO" if r["A"]["to"] else ("TRACEBACK" if "Traceback" in r["A"]["text"]
                                       else "exit %s" % r["A"]["exit"])
    bstat = "TO" if r["B"]["to"] else ("TRACEBACK" if "Traceback" in r["B"]["text"]
                                       else "exit %s" % r["B"]["exit"])
    flag = ""
    if v in ("CANNOT RUN AT ALL", "BREAKS ONLY UNDER THE DEFECT"):
        flag = "  <-"
        mismatch += 1
    print("      %-36s %-22s %-10s %-10s %s%s"
          % (("%s::%s" % (t.replace("code/", ""), p))[:36], v, astat, bstat,
             e, flag))

# ---------------------------------------------------------------------------
B.hdr("V4c  THE COLLAPSE, SHOWN ON A ROW CONSTRUCTED TO HAVE THE THIRD OUTCOME")

print("  A negative result needs an instrument that could have shown the")
print("  positive.  Here is a row whose probe CANNOT RUN AT ALL -- it raises")
print("  the same traceback in both arms -- fed to both rules:")
print()
synth = {"A": {"to": False, "exit": 1, "text": "Traceback (most recent call last)\nValueError\n",
               "read_empty": False},
         "B": {"to": False, "exit": 1, "text": "Traceback (most recent call last)\nValueError\n",
               "read_empty": False}}
print("      mg-ec63's classify()   ->  %s" % ec63_classify(synth))
print("      mg-18dc's rule         ->  %s" % mine(synth))
print()
print("  mg-ec63's `NEVER EXERCISED = 0` is therefore a PROPERTY OF ITS RULE")
print("  before it is a fact about the arc.  The verdict requires the healthy")
print("  arm to break while the defect arm works; the outcome the ticket names")
print("  requires the probe to fail against real input, which fails BOTH arms.")
print("  The two are not the same class, and only one of them was measured.")
print()
print("  THIS DOES NOT MAKE THE 0 FALSE.  It makes it unsupported.  What V4b")
print("  measures is whether the class is empty in fact as well as by rule.")

# ---------------------------------------------------------------------------
B.hdr("V4d  AND THE NONDETERMINISTIC ROWS, WHICH NOBODY FOLLOWED UP")

nd = [(t, p) for (t, p), r in rows.items() if r["ec63"] == "NDET"]
print("  mg-ec63 excluded %d steps from DIFFERENT with a determinism control" % len(NDET))
print("  and says in its own WHAT I DID NOT DO that it did not investigate")
print("  them.  %d of them are re-run here.  A probe that gives two answers to" % len(nd))
print("  the same question in one minute is its own finding:")
print()
print("  population: the %d NONDETERMINISTIC steps re-run" % len(nd))
for k in order:
    n = sum(1 for (t, p) in nd if mine(rows[(t, p)]) == k)
    if n:
        B.plain("...of those, %s" % k, n, "one step")

print()
print("V4 TOTAL STEPS WHOSE TRUE OUTCOME IS NOT THE ONE RECORDED: %d" % mismatch)
sys.exit(min(mismatch, 120))
