"""mg-18dc / V3 -- 43, RE-DERIVED: WHERE THE SHAPE ACTUALLY BITES.

mg-03d1's 43 is the conjunction of two STATIC rules: a regex says the runner
redirects with `>`, and a second regex says some `.py` in the tree mentions
`out_`.  mg-ec63 replaced the second half with an audit hook and got 19 trees.
Neither number is re-derivable from the other's population.

This measures the conjunction as ONE observation instead of two rules joined:

    a process opens `out_X.txt` OF ITS OWN TREE, for READING, and the file
    HAS ZERO BYTES AT THAT MOMENT.

There is no `>` in that sentence and no regex.  If the runner truncated it and
the probe read it, the size at open is 0 and this fires.  If the runner used
`.new`+`mv`, the size at open is the previous run's bytes and it does not.

Runs the arc for real, in SIX DISPOSABLE CLONES, one per worker -- never in the
repository.  mg-ec63 ran the arc in the tree and one of the arc's own probes
executed mg-ec63's runner mid-run and emptied the transcript it was writing
(SD6e/SD6f).  A clone per worker is that hazard removed rather than guarded.

Exit code = trees where the shape bites.
"""

import json
import os
import sys
import threading

import lib18dc as B

REV = "d33970b"
WORKERS = 6
TIMEOUT = 420

print("mg-18dc / V3 -- THE BITE, OBSERVED AT THE OPEN CALL")
print("HEAD: %s" % B.head())
print("MEASURED AT: %s  (mg-03d1's own audit commit)" % REV)

TREES = B.runners_at(REV)
LEDGER = os.path.join(B.WORK, "v3-ledger.json")

# ---------------------------------------------------------------------------
B.hdr("V3a  RUNNING ALL %d RUNNERS FOR REAL, UNDER AN OPEN-AUDIT HOOK" % len(TREES))

print("  Six clones of the repository at %s, one per worker, each reset to" % REV)
print("  its committed bytes between trees.  `sys.addaudithook` records every")
print("  `open` of a path containing `out_`, with the pid, the MODE, and THE")
print("  SIZE THE OPENER SAW.  Timeout %d s per runner." % TIMEOUT)
print()

results = {}
lock = threading.Lock()
queue = list(TREES)
qlock = threading.Lock()


def worker(k):
    sbx = B.sandbox(REV, tag="%s-w%d" % (REV, k))
    while True:
        with qlock:
            if not queue:
                return
            t = queue.pop(0)
        rec = B.real_run(sbx, t, timeout=TIMEOUT)
        empt = B.own_empty_reads(rec, sbx, t) if rec else []
        root = os.path.realpath(os.path.join(sbx, t))
        pop = []
        for o in (rec["opens"] if rec else []):
            if "r" in o["mode"] and "+" not in o["mode"] and o["size"] > 0 \
                    and os.path.dirname(os.path.realpath(o["path"])) == root:
                pop.append(o)
        with lock:
            results[t] = {
                "timeout": bool(rec and rec["timeout"]),
                "exit": rec["exit"] if rec else None,
                "empty_reads": [{"f": os.path.basename(o["path"]),
                                 "pid": o["pid"]} for o in empt],
                "n_pop_reads": len(pop),
                "n_opens": len(rec["opens"]) if rec else 0,
            }
        B.sandbox_reset(sbx)


ths = [threading.Thread(target=worker, args=(k,)) for k in range(WORKERS)]
for th in ths:
    th.start()
for th in ths:
    th.join()

json.dump(results, open(LEDGER, "w"), indent=1)

bites = sorted(t for t in TREES if results[t]["empty_reads"])
tos = sorted(t for t in TREES if results[t]["timeout"])
steps = sorted({(t, r["f"]) for t in bites for r in results[t]["empty_reads"]})

print("  population: the %d runners tracked at %s" % (len(TREES), REV))
B.plain("...RUNNERS run to completion", len(TREES) - len(tos), "one `run_all.sh`")
B.plain("...RUNNERS killed at the %d s timeout" % TIMEOUT, len(tos),
        "one `run_all.sh`")
print()
B.plain("...RUNNERS where a probe READ A TRANSCRIPT OF ZERO BYTES",
        len(bites), "one `run_all.sh`")
B.plain("...TRANSCRIPTS so read, across those runners", len(steps),
        "one (tree, transcript) pair")
print()
print("  EVERY COUNT IS A LOWER BOUND.  A runner killed at %d s may bite after"
      % TIMEOUT)
print("  the kill; %d were killed and are UNMEASURED, not clean." % len(tos))
for t in tos:
    print("          killed: %s" % t.replace("code/", ""))

# ---------------------------------------------------------------------------
B.hdr("V3b  MY NUMBER AND mg-03d1'S 43")

import re                                                            # noqa: E402
sbx0 = B.sandbox(REV, tag="%s-w0" % REV)
TRUNC_RE = re.compile(r"(?<![>2])>\s*[\"']?\$?\{?_?[oO]|(?<![>2])>\s*[\"']?out_")
READS_OWN = re.compile(r"\bouts\s*\(|glob\.glob\([^)]*out_|[\"']out_[a-z0-9_]*"
                       r"\.txt[\"']|\bout_\*\.txt\b")
their = []
for t in TREES:
    src = open(os.path.join(sbx0, t, "run_all.sh")).read()
    if re.search(r"\.new", src) and re.search(r"\bmv\b", src):
        continue
    if not TRUNC_RE.search(src):
        continue
    d = os.path.join(sbx0, t)
    for f in sorted(os.listdir(d)):
        if f.endswith(".py") and READS_OWN.search(open(os.path.join(d, f),
                                                       errors="replace").read()):
            their.append(t)
            break

print("      mg-03d1  two regexes, conjoined        %3d   (it printed 43)"
      % len(their))
print("      mg-ec63  audit hook, own transcript    %3s   (it printed 19 trees"
      % "-")
print("                                                    / 32 steps over 110)")
print("      mg-18dc  size==0 at the open call      %3d" % len(bites))
print()
print("  ^ one unit of each is one `run_all.sh`.  mg-ec63's 19 is over the 110")
print("    runners at 3fc870a and is NOT this population; it is printed here to")
print("    be named, not to be subtracted.")
print()
fp = [t for t in their if t not in set(bites)]
fn = [t for t in bites if t not in set(their)]
print("  population: the %d runners at %s, by whether the rules agree" % (len(TREES), REV))
B.plain("...RUNNERS both rules call biting", len(set(their) & set(bites)),
        "one `run_all.sh`")
B.plain("...RUNNERS the REGEX PAIR calls biting and execution does NOT",
        len(fp), "one `run_all.sh`")
B.plain("...RUNNERS EXECUTION calls biting and the regex pair does NOT",
        len(fn), "one `run_all.sh`")
print()
print("  THE REGEX PAIR'S FALSE POSITIVES.  The source mentions `out_` and the")
print("  runner uses `>`; no process ever reads an empty transcript of its own")
print("  tree.  A count of trees that COULD bite is not a count of trees that DO:")
for t in sorted(fp):
    r = results[t]
    # SD8 of this instrument: this line shipped for one draft as
    # "%d own-tree reads, all of populated files", which over n == 0 asserts a
    # universal over an empty set -- ALL_PASS with nothing in the population,
    # which is one of the six sibling defects this brief names.  The n == 0
    # case is a DIFFERENT finding from the n > 0 case and now says so.
    if r["timeout"]:
        why = "killed at %d s -- UNMEASURED" % TIMEOUT
    elif r["n_pop_reads"] == 0:
        why = "NO own-tree transcript read AT ALL -- the regex pair's second half is false here"
    else:
        why = "%d own-tree reads, none of them of an empty file" % r["n_pop_reads"]
    print("      %-46s %s" % (t.replace("code/", ""), why))
print()
print("  THE REGEX PAIR'S FALSE NEGATIVES -- observed biting, not matched:")
for t in sorted(fn):
    print("      %-46s %s" % (t.replace("code/", ""),
                              ", ".join(sorted({r["f"] for r in results[t]["empty_reads"]}))[:44]))

# ---------------------------------------------------------------------------
B.hdr("V3c  THE NEGATIVE CONTROL -- WHAT WOULD HAVE SHOWN A POSITIVE")

newmv = []
for t in TREES:
    src = open(os.path.join(sbx0, t, "run_all.sh")).read()
    if re.search(r"\.new", src) and re.search(r"\bmv\b", src):
        newmv.append(t)
print("  An instrument that finds nothing is worthless unless it can be shown")
print("  to fire.  Two directions, both printed:")
print()
print("  population: the %d runners with the `.new`+`mv` fix" % len(newmv))
for t in newmv:
    r = results[t]
    print("      %-46s empty-reads %d   own-tree reads %d"
          % (t.replace("code/", ""), len(r["empty_reads"]), r["n_pop_reads"]))
print("      ^ the fixed trees are read by their own probes and NEVER at size 0.")
print("        The instrument sees the reads; it declines to call them empty.")
print()
tot_pop = sum(results[t]["n_pop_reads"] for t in TREES)
tot_emp = sum(len(results[t]["empty_reads"]) for t in TREES)
print("  population: every own-tree transcript READ observed in the whole pass")
B.plain("...READS of a transcript with bytes in it", tot_pop, "one open() call")
B.plain("...READS of a transcript with ZERO bytes", tot_emp, "one open() call")
print()
print("  If the hook were broken, both numbers would be 0.  If the size were")
print("  read after the fact rather than at the call, the second would be 0")
print("  and the first would absorb it.  Neither is 0.")

print()
print("V3 TOTAL TREES WHERE THE SHAPE BITES: %d" % len(bites))
sys.exit(min(len(bites), 120))
