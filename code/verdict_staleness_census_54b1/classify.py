"""mg-54b1 -- READ A SWEEP AND ANSWER THE TICKET'S QUESTION.

    python3 classify.py <sweep-outdir>

`sweep_54b1.sh` produces `sweep.tsv` (one line per instrument) and one `.diff`
per instrument.  This reads them, applies `lib54b1`, and reports the split
mg-20ee's ground truth could not: of the instruments whose transcripts do not
reproduce, how many moved a VERDICT and how many moved only ADDRESSES.

Every VERDICT MOVED is published WITH ITS QUOTED EVIDENCE.  c0_controls.py
measures one over-count in three real diffs, so the number alone is a net and
the quotes are what let a reader check it against the catch.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib54b1 as L

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
DATE = os.environ.get("SWEEP_DATE", "(date not supplied)")
HOST_NOTE = os.environ.get("SWEEP_NOTE", "")


def hdr(t):
    print("=" * 78)
    print(t)
    print("=" * 78)
    print()


rows = []
tsv = os.path.join(OUT, "sweep.tsv")
for line in open(tsv, encoding="utf-8"):
    f = line.rstrip("\n").split("\t")
    if len(f) < 5:
        continue
    d, cls, rc, secs, n = f[0], f[1], f[2], f[3], f[4]
    slug = d.replace("/", "_")
    dp = os.path.join(OUT, "diffs", slug + ".diff")
    diff = open(dp, encoding="utf-8", errors="replace").read() if os.path.exists(dp) else ""
    if cls == "TIMEOUT":
        verdict, ev = "TIMEOUT", {}
    else:
        verdict, ev = L.classify_diff(diff)
    rows.append((d, verdict, rc, secs, n, ev))

hdr("mg-54b1  IS IT STALE IN THE STRONG SENSE?  A SWEEP OF THE BLIND SPOT")

print("  measured on   : %s" % DATE)
print("  population    : instruments carrying a tracked out_*.txt that are in")
print("                  NEITHER ./build.sh's loop NOR mg-20ee's 44 candidates,")
print("                  sampled by md5 of their path.  c1_population.py sizes")
print("                  the population and picks the sample; this reads the run.")
print("  method        : re-run the suite IN A CLONE, keep the diff, classify it")
print("  produced by   : sh sweep_54b1.sh <clone> <outdir> <N> <timeout>")
if HOST_NOTE:
    print("  note          : %s" % HOST_NOTE)
print()
print("""  THE QUESTION mg-20ee's GROUND TRUTH DOES NOT ASK.  Its answer is DIFFERS
  or REPRODUCES -- any byte.  Its own tranche exists because most of those
  bytes are ADDRESSES, and an AS_OF pin removes them with no verdict having
  moved.  This splits DIFFERS in two.""")
print()

order = {"VERDICT MOVED": 0, "DEAD": 1, "ADDRESSES ONLY": 2,
         "REPRODUCES": 3, "TIMEOUT": 4}
counts = {}
for _d, v, _rc, _s, _n, _e in rows:
    counts[v] = counts.get(v, 0) + 1

print("  %-16s %5s" % ("class", "n"))
for k in sorted(counts, key=lambda x: order.get(x, 9)):
    print("  %-16s %5d" % (k, counts[k]))
print("  %-16s %5d" % ("TOTAL", len(rows)))
print()

measured = len(rows) - counts.get("TIMEOUT", 0)
strong = counts.get("VERDICT MOVED", 0) + counts.get("DEAD", 0)
if measured:
    print("  Of %d instruments the sweep could measure, %d are stale in the"
          % (measured, strong))
    print("  STRONG sense -- a verdict moved, or the instrument no longer runs")
    print("  at all -- which is %.0f%%." % (100.0 * strong / measured))
print()

hdr("§2  EVERY INSTRUMENT, WITH ITS CLASS")

for d, v, rc, secs, n, _e in sorted(rows, key=lambda r: (order.get(r[1], 9), r[0])):
    print("  %-46s %-14s rc=%-4s %4ss %s" % (d, v, rc, secs, n))
print()

hdr("§3  THE EVIDENCE FOR EVERY `VERDICT MOVED`")

print("""  Quoted so this number can be checked rather than believed.  c0's R3 is a
  real diff this classifier over-counts, so a reader who wants the catch and
  not the net should read these.  At most three lines per file.""")
print()
for d, v, _rc, _s, _n, ev in sorted(rows):
    if v != "VERDICT MOVED":
        continue
    print("  --- %s" % d)
    for path, evs in sorted(ev.items()):
        print("      %s" % path)
        for rule, o, n in evs[:3]:
            print("        %s" % rule)
            print("        -  %s" % o[:84])
            print("        +  %s" % n[:84])
        if len(evs) > 3:
            print("        ... %d further changed line(s) not shown" % (len(evs) - 3))
    print()

hdr("§3b  DID THE BRANCH THAT MEASURED THIS PERTURB WHAT IT MEASURED?")

print("""  The sweep runs in a clone of the branch that carries it, so this branch's
  OWN additions are in the corpus these instruments walk.  Several of them
  count markdown files, or directories under code/, and a branch that adds one
  moves those counts -- 6c9ab90 and 417a789 are two commits in this history
  that exist only to recommit transcripts for that reason.

  So every quoted evidence line is screened for this ticket's own strings.  A
  hit does not prove the finding is an artefact, and a clean screen does not
  prove none is; what it does is stop the question going unasked.""")
print()
OWN = ("54b1", "verdict_staleness_census")
hits = 0
for d, v, _rc, _s, _n, ev in sorted(rows):
    if v != "VERDICT MOVED":
        continue
    for path, evs in sorted(ev.items()):
        for rule, o, n in evs:
            if any(t in o or t in n for t in OWN):
                hits += 1
                print("  *** %s" % path)
                print("      -  %s" % o[:80])
                print("      +  %s" % n[:80])
if not hits:
    print("  0 of the quoted evidence lines name this ticket or its directory.")
print()

dead = [d for d, v, _r, _s, _n, _e in rows if v == "DEAD"]
if dead:
    hdr("§4  DEAD -- THE INSTRUMENT RAISED AND PRODUCED NO COMPARABLE TRANSCRIPT")
    print("  A transcript whose instrument no longer RUNS is worse than a stale")
    print("  one: nothing re-derives it and its committed copy reads as a")
    print("  measurement.  code/species_extent_audit_6cb9's a3 arm is this,")
    print("  and it is why the class exists.")
    print()
    for d in dead:
        print("      %s" % d)
    print()

to = [(d, s) for d, v, _r, s, _n, _e in rows if v == "TIMEOUT"]
if to:
    hdr("§5  TIMEOUT -- NOT MEASURED, AND NOT COUNTED AS REPRODUCING")
    print("  Killed at the sweep's budget, mid-run.  These are UNMEASURED; the")
    print("  percentage above is over the measured set and says so.  Re-run")
    print("  sweep_54b1.sh with a larger timeout to close them.")
    print()
    for d, s in to:
        print("      %-46s killed at %ss" % (d, s))
    print()

print("=" * 78)
print("SWEEP TOTAL STRONG: %d of %d measured (%d unmeasured)"
      % (strong, measured, counts.get("TIMEOUT", 0)))
print("=" * 78)
print()
print("""EXTENT OF THIS NUMBER.  It is a SAMPLE of the blind spot, not a count of it:
c1_population.py prints the population's size and this prints the sample's.
The classifier's two rules and both directions of its error are planted in
c0_controls.py and its one measured over-count on a real diff is published
there rather than tuned away.  It says NOTHING about the instruments in
./build.sh's loop, which mg-f771 regrades on every merge, nor about mg-20ee's
44, which its own ground truth already re-ran.  And a TIMEOUT is not a
reproduction: an instrument too slow for the budget is unmeasured here and
should not be read as healthy.""")
