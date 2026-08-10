"""a3 -- THE REPAIRED CENSUS, FIRED FOR REAL, ON A BUDGET IT CANNOT MEET.

a1 is a control over TRANSCRIBED classifiers.  A transcription that is checked
against its source is admissible and it is still not the thing itself: the
classifier lives inside a threaded worker, downstream of a real `Popen`, a real
`SIGKILL` to a process group, and a real `collect()` off a real disk.  Every one
of those is a place the repair could fail while a1 stayed green.

So this arm runs the ACTUAL `t2_census.py`, unmodified, against ONE directory
with a budget of a few seconds, and requires the bucket that could not fire to
fire.  The subject is chosen rather than picked at random and the choice is the
point:

    code/hodge_leverage_repair_ff3e/out_repair_ff3e.txt

is the transcript mg-1abe PUBLISHED as one of FIVE FALSE RECORDS, which cf8e5
then ran to completion at its carrying commit and found REPRODUCES BYTE-FOR-BYTE
in 1470 s against a 900 s budget.  It is the row the defect actually damaged.

⚠️  THIS IS A DEMONSTRATION AT A FORCED BUDGET AND IT IS NOT THE CENSUS.  The
census's own figures come from `out_t2_census.txt` at the full 900 s; this
proves the mechanism works end to end, at a budget chosen so that it must.
Nothing in this transcript is a verdict about the subject directory.
"""

import os
import re
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_a71f as L                                            # noqa: E402

SUBJECT_DIR = "hodge_leverage_repair_ff3e"
SUBJECT = "code/%s/out_repair_ff3e.txt" % SUBJECT_DIR
BUDGET = 5


def main():
    led = L.Ledger("a3 -- THE REPAIRED CENSUS FIRED FOR REAL AT A BUDGET IT "
                   "CANNOT MEET")
    print("    subject    %s" % SUBJECT)
    print("    budget     %d s (FORCED -- the census runs at 900 s)" % BUDGET)
    print("    as-of      %s" % L.PRIOR_AS_OF[:12])

    led.head("A3a -- RUNNING `t2_census.py` ITSELF, UNMODIFIED")
    print("""
No transcription, no import of a copy: the census's own script, in a
subprocess, so that its exit code is scored as an exit code and its output is
the output a reader would get.
""")
    t0 = time.time()
    r = subprocess.run([sys.executable, "-W", "ignore", "t2_census.py",
                        "--at", L.PRIOR_AS_OF, "--dirs", SUBJECT_DIR,
                        "--timeout", str(BUDGET), "--jobs", "1"],
                       cwd=os.path.join(L.REPO, L.CENSUS_DIR),
                       capture_output=True, text=True)
    secs = time.time() - t0
    out = r.stdout
    print("    exit %d in %.0f s, %d bytes of output" % (r.returncode, secs,
                                                         len(out)))
    if len(out) < 1000:
        led.self_error("A3a the census produced almost no output; stderr was: "
                       "%s" % r.stderr[-400:])
        return led.done()

    row = [l for l in out.splitlines()
           if l.strip().startswith(SUBJECT[len("code/"):][:52])]
    led.record(bool(row), "A3a the subject has a row in T2a")
    if not row:
        return led.done()
    print()
    print("    %s" % row[0].strip()[:150])

    led.head("A3b -- THE BUCKET THAT COULD NOT FIRE, FIRING")
    fields = row[0].split()
    got = fields[2] if len(fields) > 2 else "?"
    led.record(got == "TIMED-OUT",
               "A3b the row is bucketed `%s`.  Before mg-a71f this same run "
               "produced `DIFFERS`, because the shell had already created the "
               "file and `collect()` returned its zero bytes" % got)
    led.record("the shell had already created this file" in row[0],
               "A3b' and the detail column says WHY it is not DIFFERS, in the "
               "transcript, where a reader of the census will see it rather "
               "than having to read this directory")

    led.head("A3c -- AND THE CONSEQUENCE IS GONE FROM THE REPORT")
    m = re.search(r"^\s+FLIPS\s+(\d+)\s", out, re.M)
    flips = int(m.group(1)) if m else None
    led.record(flips == 0,
               "A3c the report's FLIPS count for this run is %s.  A killed run "
               "no longer produces a FALSE RECORD: the row it would have been "
               "computed for is not in DIFFERS at all" % flips)
    tf = re.search(r"already created\s+(\d+)", out)
    led.record(tf is not None and int(tf.group(1)) >= 1,
               "A3c' T2f names %s row(s) the pre-repair guard would have "
               "mis-bucketed, in the census's own transcript"
               % (tf.group(1) if tf else "no"))

    led.head("A3d -- WHAT THIS ARM DOES NOT SHOW")
    print("""
It does not show that the subject fails to reproduce, and it does not show that
it reproduces.  A 5-second budget measures nothing about a producer that needs
1470 s.  That is the entire content of the TIMED-OUT bucket and the reason it
had to exist: `I did not finish measuring` is not a verdict about the subject,
and the whole defect was an instrument that turned it into one.
""")
    return led.done()


if __name__ == "__main__":
    sys.exit(main())
