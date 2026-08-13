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
    changed = [c for c in (f[5].split(",") if len(f) > 5 else []) if c]
    slug = d.replace("/", "_")
    dp = os.path.join(OUT, "diffs", slug + ".diff")
    diff = open(dp, encoding="utf-8", errors="replace").read() if os.path.exists(dp) else ""
    if cls == "TIMEOUT":
        verdict, ev = "TIMEOUT", {}
    else:
        verdict, ev = L.classify_diff(diff)
    foreign = [c for c in changed
               if L.TRANSCRIPT.match(c) and not c.startswith(d + "/")]
    load = f[7] if len(f) > 7 else ""
    rows.append((d, verdict, rc, secs, n, ev, foreign, load))

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
for _r in rows:
    v = _r[1]
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

hdr("§1b  OF THE TRANSCRIPTS THAT DIFFER, HOW MANY DIFFER ONLY IN ADDRESSES?")

vm = counts.get("VERDICT MOVED", 0) + counts.get("DEAD", 0)
ao = counts.get("ADDRESSES ONLY", 0)
differing = vm + ao
print("""  This is the number that decides whether mg-20ee's remedy -- pin the
  instrument at an AS_OF commit so the addresses stop moving -- would help
  this population at all.  An AS_OF pin removes an ADDRESSES ONLY difference
  and does nothing whatever for a moved verdict.""")
print()
print("  transcripts that DIFFER at all              %5d" % differing)
print("      of those, only ADDRESSES moved          %5d" % ao)
print("      of those, a VERDICT moved               %5d" % vm)
print()
if differing and ao == 0:
    print("""  NOT ONE of the differing transcripts in this sample differs only in its
  addresses.  That is the opposite of what mg-20ee measured, and the reason is
  that the two populations were SELECTED DIFFERENTLY: its 44 were nominated by
  a classifier FOR FOREIGN ADDRESSES, so a difference that was nothing but an
  address is exactly what it went looking for and exactly what pinning fixed.
  This sample was selected for nothing, and in it a transcript that moves at
  all has moved a verdict.  ON THIS EVIDENCE, PINNING IS NOT THE REMEDY HERE:
  what these instruments lack is not a declared commit but ANYTHING THAT
  RE-RUNS THEM.

  AND THE ZERO IS A MEASUREMENT RATHER THAN A CLASSIFIER THAT CANNOT SAY IT.
  A count of zero is worthless from a detector nobody has watched produce a
  nonzero one, which is this arc's own recurring complaint.  ADDRESSES ONLY is
  reachable and is watched being reached: c0_controls.py lands EIGHT planted
  worlds in it -- a moved sha, a corpus size, line numbers, a duration, a date,
  a worktree root, a changed path, and a duration on a VERDICT line -- plus the
  real diff of 6c9ab90, whose own commit message says the row that scores
  stayed put.  The class fires; this sample simply contains none of it.""")
elif differing:
    print("""  %d of %d differing transcripts moved only addresses, so an AS_OF pin --
  mg-20ee's remedy -- would settle that fraction of this population and would
  do nothing for the rest.""" % (ao, differing))
else:
    print("  Nothing in this sample differs, so this arm has nothing to split.")
print()

hdr("§2  EVERY INSTRUMENT, WITH ITS CLASS")

print("  %-46s %-14s %-6s %5s %-10s %s" % ("instrument", "class", "rc", "secs", "lines", "load"))
for d, v, rc, secs, n, _e, _f, ld in sorted(rows, key=lambda r: (order.get(r[1], 9), r[0])):
    print("  %-46s %-14s rc=%-3s %5s %-10s %s" % (d, v, rc, secs, n, ld or "-"))
print()

hdr("§3  THE EVIDENCE FOR EVERY `VERDICT MOVED`")

print("""  Quoted so this number can be checked rather than believed.  c0's R3 is a
  real diff this classifier over-counts, so a reader who wants the catch and
  not the net should read these.  At most three lines per file.""")
print()
for d, v, _rc, _s, _n, ev, _f, _l in sorted(rows):
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
for d, v, _rc, _s, _n, ev, _f, _l in sorted(rows):
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

hdr("§3c  DID ANY INSTRUMENT REWRITE SOMEBODY ELSE'S TRANSCRIPT?")

print("""  The sweep keeps the WHOLE-REPO diff a run produced, not just the diff of
  its own directory, because a runner that writes outside itself is exactly
  the kind of thing this sweep should not hide.  But it also means a
  transcript could be attributed to the run that touched it rather than to
  the instrument that owns it, which would inflate the count.  So the two are
  separated and printed.""")
print()
foreign_rows = [(d, f) for d, _v, _rc, _s, _n, _e, f, _l in sorted(rows) if f]
if not foreign_rows:
    print("  0 instruments changed a transcript outside their own directory,")
    print("  so every class above is attributed to the instrument that owns it.")
else:
    for d, f in foreign_rows:
        print("  %s wrote %d transcript(s) outside its own directory:" % (d, len(f)))
        for c in f:
            print("      %s" % c)
print()

dead = [d for d, v, _r, _s, _n, _e, _f, _l in rows if v == "DEAD"]
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

to = [(d, s, l) for d, v, _r, s, _n, _e, _f, l in rows if v == "TIMEOUT"]
if to:
    hdr("§5  TIMEOUT -- NOT MEASURED, AND NOT COUNTED AS REPRODUCING")
    print("""  Killed at the sweep's budget, mid-run.  These are UNMEASURED, and a
  TIMEOUT IS NOT A PROPERTY OF THE INSTRUMENT: it is a property of the
  instrument, the budget AND the host.  The run that produced the committed
  transcript shared a 10-core machine with other agents whose load average was
  measured by hand at 16 when it started and 60 an hour later, so an
  instrument needing 60 s on an idle host can miss a 120 s budget here.  The
  `load` column exists so a later reader does not have to take my word for
  that; where it reads `not recorded`, the column was added after that row was
  produced.""")
    print()
    print("  percentage above is over the measured set and says so.  Re-run")
    print("  sweep_54b1.sh with a larger timeout to close them.")
    print()
    for d, s, l in to:
        print("      %-46s killed at %ss, host load %s" % (d, s, l or "not recorded"))
    print()

print("=" * 78)
print("SWEEP TOTAL STRONG: %d of %d measured (%d unmeasured)"
      % (strong, measured, counts.get("TIMEOUT", 0)))
print("=" * 78)
print()
print("""WHY A PARTIAL SWEEP IS STILL A SAMPLE AND NOT A PREFIX.  The work list is the
137 runnable blind-spot directories ordered by the md5 of their path, which is
independent of anything this measures, so the ordering is a random permutation
and ANY PREFIX OF IT IS A SIMPLE RANDOM SAMPLE.  That is the property that
makes a sweep stopped on a clock still worth quoting, and it is why the order
is md5 and not alphabetical -- the names are alphabetical by topic, and a
prefix of THAT is a sample of nothing.

AND THE STOPPING RULE IS DISCLOSED, because I could see the rows as they
landed: this run was stopped on a TIME BUDGET and not on a count and not on
its answer.  A reader who wants that dependency removed should re-run with a
larger N; the sample is a function of the path, so the rows above reappear
unchanged and the new ones are appended.

EXTENT OF THIS NUMBER.  It is a SAMPLE of the blind spot, not a count of it:
c1_population.py prints the population's size and this prints the sample's.
The classifier's two rules and both directions of its error are planted in
c0_controls.py and its one measured over-count on a real diff is published
there rather than tuned away.  It says NOTHING about the instruments in
./build.sh's loop, which mg-f771 regrades on every merge, nor about mg-20ee's
44, which its own ground truth already re-ran.  And a TIMEOUT is not a
reproduction: an instrument too slow for the budget is unmeasured here and
should not be read as healthy.

THE RULE I ALMOST ADDED, AND THE ROW THAT SHOWED IT WOULD HAVE BEEN WRONG.
DEAD is detected by a Traceback in the transcript, which only appears when the
runner redirects stderr into it.  A runner that does NOT would leave a
TRUNCATED transcript instead -- many deletions, almost no additions -- and
every removed verdict line in it would be counted as a moved verdict.  The
obvious guard is a ratio: call a diff DEAD when deletions swamp additions.

IT WOULD HAVE BEEN WRONG ON THE FIRST ROW IT MET.  code/hodge_leverage_repair_8eca
came back `4+/143-`, the exact shape, and it is not a crash: the run reports
`green` -> `STILL RED` and `rows that failed: 1` -> `29`, and the transcript
shrank because the run STOPPED CONFIRMING things it used to confirm.  A
vanished [CONFIRMED] block is the strongest form of a moved verdict, not
evidence of a dead instrument.  So no ratio rule is added, and the reason is
a measurement rather than a preference: the shape of the diff does not
distinguish a truncated run from a run with less to say.""")
