"""a6 -- THE DISCRIMINATOR: THE TIMED-OUT SUBSET, RE-RUN ON A QUIET BOX.

pm-onethird's decision, after the covariate showed 1-minute load excursions to
129.59 inside a single run:

    A 20x excursion lasting minutes, against a 900-second budget, means
    TIMED-OUT is dominated by WHEN a group was scheduled rather than by what its
    code does.  So the full re-run's TIMED-OUT count is a CANDIDATE SET, not an
    answer.

Neither run alone can separate `this suite is slow` from `the box was busy`.
The PAIR can, and that is all this script is:

    a group that times out at load 8 AS WELL AS at load 129   -> slow CODE
    a group that reproduces cleanly at load 8                 -> MACHINE ARTEFACT

SO THREE NUMBERS ARE REPORTED AND NOT ONE:

    timed out under load        the full run's TIMED-OUT bucket -- the candidate
                                set, and a fact about a box during one window
    timed out again when quiet  THE ONLY ONE THAT BELONGS IN ANY STATEMENT
                                ABOUT THE ARC
    reproduced when quiet       machine artefacts, named individually

⚠️  SAME EVERYTHING ELSE.  Same as-of (`81214a9`), same 900 s budget, same
instrument.  Only the machine differs, which is the whole design: change one
thing or the comparison means nothing.

⚠️  `--dirs` FILTERS BY DIRECTORY AND THE CENSUS KEYS ON (DIRECTORY, COMMIT).
A directory carrying transcripts at two commits is two groups, and naming it
re-runs both.  That is conservative -- it can only ADD rows to the comparison,
never drop one -- and A6a prints the difference so it is visible rather than
assumed harmless.

⚠️  THIS SCRIPT MEASURES ITS OWN MACHINE.  A "quiet" re-run that was not quiet
proves nothing, so the load is sampled DURING the subprocess by this script
itself, and A6d refuses the contrast if the second run was not materially
quieter than the first.  A discriminator that cannot tell you it failed to
discriminate is not one.
"""

import os
import subprocess
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_a71f as L                                            # noqa: E402

NEW_T2 = os.path.join(L.REPO, L.CENSUS_DIR, "out_t2_census.txt")
BUDGET = 900
JOBS = 4


class LoadSampler(threading.Thread):
    """1-minute load average every 10 s for as long as the subject runs."""

    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        self.samples = []
        self.stop = threading.Event()

    def run(self):
        while not self.stop.wait(10):
            try:
                self.samples.append(os.getloadavg()[0])
            except OSError:
                pass

    def stats(self):
        s = self.samples
        if not s:
            return None
        return (min(s), max(s), sum(s) / len(s), len(s))


def main():
    led = L.Ledger("a6 -- THE TIMED-OUT SUBSET, RE-RUN ON A QUIET BOX")

    if not os.path.exists(NEW_T2):
        led.self_error("the full re-run has not produced %s" % NEW_T2)
        return led.done()
    with open(NEW_T2, encoding="utf-8", errors="replace") as fh:
        full_t = fh.read()
    full_rows = L.parse_t2_rows(full_t)
    if not full_rows:
        led.self_error("the full re-run's T2a table parsed to nothing; every "
                       "number below would be a fact about the parser")
        return led.done()

    timed = sorted(p for p, (_, v) in full_rows.items() if v == "TIMED-OUT")

    # ------------------------------------------------------------------ A6a
    led.head("A6a -- THE CANDIDATE SET, AND WHAT NAMING IT BY DIRECTORY COSTS")
    dirs = sorted({p.split("/")[0] for p in timed})
    carried = sorted(p for p in full_rows
                     if p.split("/")[0] in dirs)
    print("    transcripts TIMED-OUT in the full run   %4d" % len(timed))
    print("    distinct directories they sit in        %4d" % len(dirs))
    print("    transcripts those directories carry     %4d   <- what `--dirs` "
          "will actually re-run" % len(carried))
    print("    ...so rows swept in beyond the subset   %4d   (a directory "
          "carrying transcripts at two commits is two groups)"
          % (len(carried) - len(timed)))
    for d in dirs:
        print("      %s" % d)
    if not timed:
        led.record(True,
                   "A6a the full run's TIMED-OUT bucket is EMPTY, so there is "
                   "no candidate set and no discriminator to run.  That is an "
                   "outcome: at this budget, on this box, no suite in the "
                   "population went unmeasured")
        return led.done()
    led.record(None,
               "A6a %d transcripts in %d directories are the candidate set.  "
               "They are re-run below at the SAME budget and the SAME as-of; "
               "only the machine differs" % (len(timed), len(dirs)))

    # ------------------------------------------------------------------ A6b
    led.head("A6b -- THE RE-RUN, WITH THIS SCRIPT WATCHING ITS OWN MACHINE")
    try:
        before = os.getloadavg()
    except OSError:
        before = (0, 0, 0)
    print("    load at start   %.2f / %.2f / %.2f" % before)
    print("    budget          %d s   as-of %s   jobs %d"
          % (BUDGET, L.PRIOR_AS_OF[:7], JOBS))
    print("    running         %d directories ..." % len(dirs))
    sampler = LoadSampler()
    sampler.start()
    t0 = time.time()
    r = subprocess.run([sys.executable, "-W", "ignore", "t2_census.py",
                        "--at", L.PRIOR_AS_OF, "--dirs", ",".join(dirs),
                        "--timeout", str(BUDGET), "--jobs", str(JOBS)],
                       cwd=os.path.join(L.REPO, L.CENSUS_DIR),
                       capture_output=True, text=True)
    sampler.stop.set()
    secs = time.time() - t0
    st = sampler.stats()
    print("    exit %d in %.0f s" % (r.returncode, secs))
    if st:
        print("    load during     min %.2f  max %.2f  mean %.2f  (%d samples)"
              % st)
    if len(r.stdout) < 1000:
        led.self_error("A6b the re-run produced almost no output; stderr: %s"
                       % r.stderr[-400:])
        return led.done()
    quiet_rows = L.parse_t2_rows(r.stdout)
    led.record(bool(quiet_rows),
               "A6b the quiet re-run's T2a table parses to %d rows"
               % len(quiet_rows))

    # ------------------------------------------------------------------ A6c
    led.head("A6c -- THE THREE NUMBERS")
    again, repro, differs, other = [], [], [], []
    for p in timed:
        v = quiet_rows.get(p, ("", "ABSENT"))[1]
        if v == "TIMED-OUT":
            again.append(p)
        elif v == "REPRODUCES":
            repro.append(p)
        elif v == "DIFFERS":
            differs.append(p)
        else:
            other.append((p, v))
    print("""
`timed out again when quiet` is the only one of these that belongs in a
statement about the arc.  The first is a fact about a box during one window;
the third and fourth are that box's artefacts, removed.
""")
    print("    timed out under load           %4d   the candidate set"
          % len(timed))
    print("    ...timed out AGAIN when quiet  %4d   <- SLOW CODE.  The only "
          "number that is about the arc" % len(again))
    print("    ...REPRODUCED when quiet       %4d   <- machine artefact, and "
          "the pre-repair census would have called each of these a "
          "non-reproduction" % len(repro))
    print("    ...DIFFERED when quiet         %4d   <- measured at last, and "
          "genuinely not the committed bytes" % len(differs))
    if other:
        print("    ...other verdict when quiet    %4d" % len(other))
    for label, group in (("timed out AGAIN when quiet -- SLOW CODE", again),
                         ("REPRODUCED when quiet -- MACHINE ARTEFACT", repro),
                         ("DIFFERED when quiet", differs)):
        print()
        print("    %s:" % label)
        for p in group:
            print("      %s" % p)
        if not group:
            print("      (none)")
    for p, v in other:
        print("      %-56s %s" % (p, v))

    led.record(not repro,
               "A6c %d of the %d candidates REPRODUCE BYTE-FOR-BYTE at the same "
               "budget on a quieter box.  Each one is a row the full run could "
               "not measure and the PRE-REPAIR census would have reported as a "
               "non-reproduction -- and, where the transcript carries a "
               "decision, as a FALSE RECORD" % (len(repro), len(timed)))
    led.record(not again,
               "A6c' %d of the %d candidates time out AGAIN when the box is "
               "quiet.  This is the only figure here that is a statement about "
               "the arc rather than about a machine: these producers need more "
               "than %d s regardless of load" % (len(again), len(timed), BUDGET))

    # ------------------------------------------------------------------ A6d
    led.head("A6d -- WAS THE SECOND RUN ACTUALLY QUIETER?")
    print("""
A discriminator that cannot tell you it failed to discriminate is not one.  The
contrast above is worth nothing unless the machine really did differ, so the
load this script sampled during its own subprocess is compared with the load
recorded during the full run.
""")
    tsv = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "covariate_load_by_group.tsv")
    full_loads = []
    if os.path.exists(tsv):
        with open(tsv, encoding="utf-8", errors="replace") as fh:
            head = fh.readline().rstrip("\n").split("\t")
            i = head.index("load1") if "load1" in head else None
            for line in fh:
                f = line.rstrip("\n").split("\t")
                if i is not None and len(f) > i:
                    try:
                        full_loads.append(float(f[i]))
                    except ValueError:
                        pass
    if full_loads and st:
        fmean = sum(full_loads) / len(full_loads)
        print("    full run    min %.2f  max %.2f  mean %.2f  (%d samples)"
              % (min(full_loads), max(full_loads), fmean, len(full_loads)))
        print("    quiet run   min %.2f  max %.2f  mean %.2f  (%d samples)"
              % st)
        led.record(st[2] < fmean,
                   "A6d the second run's mean 1-minute load was %.2f against "
                   "the first's %.2f.  If this is NOT materially lower, the "
                   "three numbers above are two readings of one machine state "
                   "and separate nothing" % (st[2], fmean))
        led.record(st[1] < max(full_loads),
                   "A6d' and its PEAK was %.2f against the first's %.2f.  A "
                   "mean can be quiet while a single excursion straddles one "
                   "group's whole budget, so the peak is reported beside it"
                   % (st[1], max(full_loads)))
    else:
        led.self_error("A6d no load record for one of the two runs; the "
                       "contrast cannot be qualified and must not be read as "
                       "a machine comparison")

    led.head("A6e -- WHAT THE PAIR STILL DOES NOT SETTLE")
    print("""
The unsampled prefix.  Groups 1-25 of the full run have no covariate row AND
ran under the highest load -- the covariate's blind spot and the confound's
worst region are THE SAME ROWS.  A candidate from that prefix is bracketed by
this pair exactly as well as any other, because the pair re-runs it; what is
missing is the load it originally failed under, which is not recoverable and is
not estimated here.

And `reproduced when quiet` is not `always reproduces`.  It is one clean
observation at one budget on one box.  The census's own T2d says so about every
row in the bucket, and a second run does not repeal it.
""")
    return led.done()


if __name__ == "__main__":
    sys.exit(main())
