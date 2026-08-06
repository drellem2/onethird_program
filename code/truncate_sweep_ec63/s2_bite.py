"""mg-ec63 / S2 -- WHERE THE SHAPE ACTUALLY BITES, MEASURED BY OPENING FILES.

mg-03d1's rule for "the shape bites here" is: the runner matches a truncation
regex AND SOME `.py` in the tree matches a regex over its SOURCE TEXT.  That is
a claim about text, at the grain of the tree.  This probe asks the process
instead: a `sys.addaudithook` on the `open` audit event records every path the
probe really opens, and the question becomes

    DID THIS PROBE OPEN THE TRANSCRIPT ITS OWN RUN HAD JUST EMPTIED?

which is the ticket's own sentence, at the grain of the STEP.

THE TWO CLASSES THE TREE-GRAIN RULE MERGES.  Under `>`, at the instant probe X
starts, `out_X.txt` is EMPTY -- it was truncated a microsecond ago.  Every OTHER
`out_*.txt` in the tree still holds THE PREVIOUS RUN'S BYTES.  So:

    EMPTIED   probe X reads out_X.txt        -> it reads nothing, guaranteed
    STALE     probe X reads out_W.txt, W!=X  -> it reads last run's bytes

Both are defects.  Only the first is the one this ticket is about, and merging
them inflates the count of the thing being repaired.  Both are reported, apart.

THIS PASS RUNS EVERY CANDIDATE STEP ONCE, WITH THE TRANSCRIPT POPULATED.  That
run is also run B of S3's A/B comparison, so it is not repeated there.

Exit code = steps in the EMPTIED class (a finding, not a breakage).
"""

import os
import sys
import time

import lib_ec63 as B

print("mg-ec63 / S2 -- WHERE THE SHAPE BITES, BY OBSERVED FILE OPENS")
print("HEAD: %s" % B.head())

pop = B.load("population")
if not pop:
    print("  (run s1_population.py first -- it writes the ledger this reads)")
    sys.exit(1)
CAND = [tuple(x) for x in pop["candidates"]]
TIMEOUT = int(os.environ.get("EC63_TIMEOUT", "45"))

# ---------------------------------------------------------------------------
B.hdr("S2a  THE RUN")

print("  population: the %d CANDIDATE STEPS of S1d" % len(CAND))
print("  Each is run ONCE, from its own tree, with its transcript holding the")
print("  committed bytes, under an `open` audit hook.  Output goes to memory --")
print("  NOTHING in the subject tree is rewritten by this sweep -- and the tree")
print("  is `git checkout`-restored after every single probe.")
print()
print("  timeout per probe: %d s.  A probe that does not finish is recorded as"
      % TIMEOUT)
print("  TIMEOUT and is neither counted as biting nor as clean, because a probe")
print("  that did not run has not answered the question.")
print()

WORKERS = int(os.environ.get("EC63_WORKERS", "6"))
print("  workers: %d.  THIS PASS TRUNCATES NOTHING -- every run here has its"
      % WORKERS)
print("  transcript populated -- so concurrent workers cannot empty a file out")
print("  from under each other.  S3, which does truncate, runs SERIALLY.")
print()

import concurrent.futures
import itertools

_slots = itertools.count()
_local = __import__("threading").local()


def one(job):
    i, (tree, probe, out) = job
    if not hasattr(_local, "slot"):
        _local.slot = next(_slots)
    rel = os.path.relpath(probe, tree)
    ob = os.path.basename(out)
    r = B.run_probe(tree, rel, ob, empty_first=False, timeout=TIMEOUT,
                    trace=True, slot=_local.slot)
    return i, {
        "tree": tree, "probe": probe, "out": out,
        "exit": r["exit"], "timeout": r["timeout"],
        "own": B.opened_own(r, tree, ob),
        "own_child": B.opened_own(r, tree, ob, key="child_read"),
        "own_write": B.opened_own(r, tree, ob, key="written"),
        "others": B.opened_other_outs(r, tree, ob),
        "nopen": len(r.get("opened", [])),
        "B_text": r["text"],
    }


recs = [None] * len(CAND)
t0 = time.time()
done = 0
with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
    for i, rec in ex.map(one, enumerate(CAND)):
        recs[i] = rec
        done += 1
        if done % 25 == 0:
            sys.stderr.write("  ... %d/%d  %.0fs\n"
                             % (done, len(CAND), time.time() - t0))
recs = [r for r in recs if r]

B.plain("...STEPS run", len(recs), "one step")
nto = sum(1 for r in recs if r["timeout"])
B.plain("...STEPS that TIMED OUT at %ds" % TIMEOUT, nto, "one step")
B.plain("...STEPS that exited non-zero", sum(1 for r in recs
                                             if r["exit"] not in (0, None)),
        "one step")
print()
print("  THE TIMEOUTS ARE A CEILING ON WHAT THIS PASS COULD SEE, AND THEY ARE")
print("  STATED HERE RATHER THAN AT THE BOTTOM.  A probe killed at %ds may not"
      % TIMEOUT)
print("  have reached the line that opens its own transcript, so it is recorded")
print("  as not-reading when the truth is not-known.  Every count below is")
print("  therefore a LOWER BOUND over the %d steps, exact only over the %d that"
      % (len(recs), len(recs) - nto))
print("  finished.  The arc's own runners take ten minutes in places; this")
print("  suite runs 422 probes and cannot give each of them ten.")

# ---------------------------------------------------------------------------
B.hdr("S2b  THE EMPTIED CLASS -- THE ONE THIS TICKET IS ABOUT")

emptied = [r for r in recs if r["own"]]
stale = [r for r in recs if not r["own"] and r["others"]]
clean = [r for r in recs if not r["own"] and not r["others"]]

print("  population: the %d STEPS run in S2a" % len(recs))
B.plain("...STEPS whose probe OPENS ITS OWN emptied transcript", len(emptied),
        "one step")
B.plain("...STEPS whose probe opens ANOTHER transcript (STALE, not empty)",
        len(stale), "one step")
B.plain("...STEPS whose probe opens no transcript of its tree", len(clean),
        "one step")
print()
ch = [r for r in recs if r["own_child"] and not r["own"]]
B.plain("...STEPS where a CHILD PROCESS read it, not the probe itself",
        len(ch), "one step")
print()
print("  THE PID IS WHY THAT ROW EXISTS.  `EC63_TRACE` and `PYTHONPATH` are")
print("  inherited by every process the probe spawns, and this arc's probes")
print("  routinely RE-RUN OTHER PROBES as subprocesses.  Without the pid in")
print("  the trace, a child's read of a transcript is recorded against the")
print("  parent -- and it is not stable, because whether the child gets that")
print("  far depends on load.  An earlier pass of this suite had exactly that:")
print("  `d3_reintroduction.py` came out reading its own transcript in a")
print("  parallel pass and not reading it when run alone, and the two numbers")
print("  it produced disagreed with each other inside one run's transcripts.")
print("  The EMPTIED class above is the STRICT one: the probe's own process.")
print()
wr = [r for r in recs if r["own_write"]]
B.plain("...STEPS whose probe WRITES its own transcript itself", len(wr),
        "one step")
print()
print("  THAT ROW IS PRINTED EVEN THOUGH IT IS %d.  A probe that writes its own"
      % len(wr))
print("  transcript opens EXACTLY THE SAME PATH as one that reads it, and an")
print("  `open`-event hook that ignores the mode counts both.  The first")
print("  version of this pass did.  So the distinction is a REAL correctness")
print("  fix whose MEASURED EFFECT HERE IS %d, and both halves of that sentence"
      % len(wr))
print("  are load-bearing: the fix is right, and it changed nothing, and")
print("  reporting it as though it had rescued a count would be attributing a")
print("  repair to evidence that does not support it.")
print()
print("  AND WHAT PROMPTED THE FIX WAS A DIFFERENT DEFECT.  Two transcripts")
print("  came out of an early pass MODIFIED, and the first explanation reached")
print("  for was `their own probes write them`.  It was not: they were written")
print("  by probes of OTHER trees, which this suite's timeout had killed before")
print("  their cleanup `finally` could run.  A rigorous fix, a confident")
print("  mechanism, and the mechanism was wrong.  S6/SD3a and SD6c keep both.")
for r in wr:
    print("      writes: %-38s %s" % (r["tree"].replace("code/", ""),
                                      os.path.basename(r["probe"])))
print()
et = sorted(set(r["tree"] for r in emptied))
st = sorted(set(r["tree"] for r in stale) - set(et))
B.plain("...RUNNERS with at least one EMPTIED step", len(et),
        "one `run_all.sh`")
B.plain("...further RUNNERS with only STALE steps", len(st),
        "one `run_all.sh`")
print()
print("  mg-03d1 reports 43 trees where 'a probe of the same run reads a")
print("  transcript that run HAS ALREADY EMPTIED'.  Under its own rule the")
print("  reading probe need not be the one whose transcript was emptied, so")
print("  its 43 covers BOTH classes above.  Mine at the tree grain, and by")
print("  observed opens rather than source text:")
print()
print("      EMPTIED trees   %d" % len(et))
print("      + STALE-only    %d" % len(st))
print("      = both classes  %d      (mg-03d1's rule, my measurement)" %
      (len(et) + len(st)))
print()
print("  I DO NOT GET 43 EITHER WAY, and the reason is the rule and not the")
print("  arc.  The number that answers the ticket's own sentence -- a probe")
print("  reading a file THE SAME RUN EMPTIED -- is %d trees / %d steps."
      % (len(et), len(emptied)))

# ---------------------------------------------------------------------------
B.hdr("S2c  THE TREES, NAMED, SO EVERY ROW CAN BE CHECKED")

for t in et:
    rows = [r for r in emptied if r["tree"] == t]
    print("      %-42s %s" % (t.replace("code/", ""),
                              ", ".join(os.path.basename(r["probe"])
                                        for r in rows)))

# ---------------------------------------------------------------------------
B.hdr("S2d  THE TEXT RULE, SCORED AGAINST THE OBSERVED OPENS")

READS_OWN = __import__("re").compile(
    r"\bouts\s*\(|glob\.glob\([^)]*out_|[\"']out_[a-z0-9_]*\.txt[\"']"
    r"|\bout_\*\.txt\b")
fp = fn = agree = 0
fps, fns = [], []
for r in recs:
    try:
        src = B.read(r["probe"])
    except OSError:
        continue
    text_says = bool(READS_OWN.search(src))
    really = r["own"] or bool(r["others"])
    if text_says and not really:
        fp += 1
        fps.append(r)
    elif really and not text_says:
        fn += 1
        fns.append(r)
    else:
        agree += 1

print("  mg-03d1's `READS_OWN` regex, run over the SAME probes, and compared")
print("  with what those probes were then observed to open.")
print()
print("  population: the %d STEPS run in S2a" % len(recs))
B.plain("...STEPS where text rule and observed opens AGREE", agree, "one step")
B.plain("...STEPS the text rule flags that open NOTHING (false positive)", fp,
        "one step")
B.plain("...STEPS that DO open a transcript with no match (false negative)", fn,
        "one step")
print()
print("  FALSE POSITIVES -- source mentions a transcript, process never opens")
print("  one (a docstring, a dead branch, a `--flag` guard):")
for r in fps[:12]:
    print("      %-42s %s" % (r["tree"].replace("code/", ""),
                              os.path.basename(r["probe"])))
if len(fps) > 12:
    print("      ... and %d more" % (len(fps) - 12))
print()
print("  FALSE NEGATIVES -- the process opens a transcript the source never")
print("  spells (a path built from a variable, an `os.path.join`, a `Path`):")
for r in fns[:12]:
    print("      %-42s %s   own=%s others=%d"
          % (r["tree"].replace("code/", ""), os.path.basename(r["probe"]),
             r["own"], len(r["others"])))
if len(fns) > 12:
    print("      ... and %d more" % (len(fns) - 12))

left = B.restore_arc()
print()
print("  every tree but this one restored, tracked and untracked: %s"
      % ("clean" if not left else "FAILED on %s" % left))

B.save("bite", {"recs": recs})

print()
print("S2 TOTAL EMPTIED STEPS: %d" % len(emptied))
sys.exit(min(len(emptied), 120))
