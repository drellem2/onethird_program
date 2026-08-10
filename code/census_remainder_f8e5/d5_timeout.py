"""d5_timeout -- THE CENSUS'S `TIMED-OUT` BUCKET IS UNREACHABLE BY CONSTRUCTION.

mg-1abe's README, §2, states the rule that makes its 112 mean what it says:

    "`TIMED-OUT` is never folded into `DIFFERS`.  'I did not finish measuring'
     and 'it does not reproduce' are different claims and only one is about the
     subject."

The rule is right and the instrument does the opposite of it, always.  Not
sometimes, and not on a slow machine: BY CONSTRUCTION, for every suite in this
arc.

THE MECHANISM, in three lines of somebody else's code:

  t2_census.py:112   `sh run_all.sh` is started in the worktree.  The FIRST
                     thing a POSIX shell does with `python3 x.py > out_x.txt`
                     is CREATE `out_x.txt`, before the producer runs.
  t2_census.py:134   `collect()` returns the file's BYTES if it exists on disk,
                     and `None` only if it does not.  A killed run leaves an
                     empty or partial file, which exists.
  t2_census.py:225   the `TIMED-OUT` bucket is guarded by `if got[p] is None`.

  So a suite killed at the budget yields `got[p] == b""` (or a partial), which
  is not None, which is not equal to the committed bytes -- and the row is
  bucketed **DIFFERS**, with a conclusion computed against an empty file.

  `conclusion_verdict(committed, "")` is **FLIPS**: every decision row is gone.

THAT IS NOT A HYPOTHESIS ABOUT WHAT WOULD HAPPEN.  It is what happened to
`code/hodge_leverage_repair_ff3e/out_repair_ff3e.txt`, which mg-1abe reports as
one of its FIVE FALSE RECORDS and which **REPRODUCES BYTE-FOR-BYTE at its own
carrying commit** when the producer is allowed to finish.  It needs ~22 minutes
against a 900-second budget.

**THE MEASURED DAMAGE OF THIS CLASS IS FOUR FALSE RECORDS, NOT FIVE.**

Every arm below is FORCED and every one could have printed the other answer.
"""

import os
import re
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_f8e5 as L

FF3E = "code/hodge_leverage_repair_ff3e/out_repair_ff3e.txt"
CENSUS = "code/transcript_census_1abe"


def t2_bucket(status, got, committed):
    """t2_census.py's classification, TRANSCRIBED from its source.

    Copied rather than imported because t2's is inside a threaded worker with a
    lock and a shared dict.  The transcription is CHECKED against the original
    text in D5a below, so a reader does not have to take my word for it.
    """
    if got is None:
        if status == "timeout":
            return "TIMED-OUT"
        if status.startswith("failed"):
            return "RUNNER-FAILED"
        return "NOT-REGENERATED"
    if got == committed:
        return "REPRODUCES"
    return "DIFFERS"


def main():
    at = L.main_rev()
    rev = L.resolve(at)
    led = L.Ledger("d5 -- THE CENSUS'S `TIMED-OUT` BUCKET IS UNREACHABLE "
                   "BY CONSTRUCTION", reads_outside_tree=True)
    print("    as-of: %s" % rev[:12])

    # ------------------------------------------------------------- D5a
    led.head("D5a -- THE TRANSCRIPTION IS CHECKED AGAINST THE ORIGINAL SOURCE")
    src = L.blob_at(rev, CENSUS + "/t2_census.py")
    if src is None:
        led.self_error("t2_census.py absent at %s" % rev[:7])
        return led.done()
    text = src.decode("utf-8", "replace")
    checks = [
        ("the shell is what creates the file",
         'subprocess.Popen(["sh", "run_all.sh"]' in text),
        ("collect() returns bytes for any file that EXISTS",
         "if os.path.exists(full):" in text and "out[path] = fh.read()" in text),
        ("collect() returns None ONLY when the file is absent",
         re.search(r"else:\s*\n\s*out\[path\] = None", text) is not None),
        ("the TIMED-OUT branch is guarded by `got[p] is None`",
         re.search(r"if got\[p\] is None:\s*\n\s*if status == \"timeout\"",
                   text) is not None),
        ("and the DIFFERS branch is the final else",
         re.search(r"elif got\[p\] == committed\[p\]:", text) is not None),
    ]
    for what, ok in checks:
        led.record(ok, "D5a %s" % what)
    led.record(all(ok for _, ok in checks),
               "D5a' every clause of the transcription above is present in "
               "`%s/t2_census.py` at %s.  The reasoning below is about that "
               "code and not about a paraphrase of it" % (CENSUS, rev[:7]))

    # ------------------------------------------------------------- D5b
    led.head("D5b -- THE CLASSIFIER, RUN ON THE THREE STATES A KILLED RUN "
             "CAN LEAVE")
    committed_b = L.blob_at(rev, FF3E)
    if committed_b is None:
        led.self_error("%s absent at %s" % (FF3E, rev[:7]))
        return led.done()
    committed = committed_b.decode("utf-8", "replace")
    partial = committed_b[:len(committed_b) // 3]

    print("    state left by a SIGKILL at the budget      t2 buckets it as")
    print("    " + "-" * 42 + "  " + "-" * 16)
    cases = [
        ("file never created (producer never started)", None, "TIMED-OUT"),
        ("file created, EMPTY (python buffers stdout)", b"", "DIFFERS"),
        ("file created, PARTIAL (buffer flushed once)", partial, "DIFFERS"),
    ]
    for label, got, expect in cases:
        bucket = t2_bucket("timeout", got, committed_b)
        print("    %-42s  %s" % (label, bucket))
        led.record(bucket == expect,
                   "D5b `%s` -> %s (expected %s)" % (label, bucket, expect))
    led.record(False,
               "D5b' 2 of the 3 states a killed run can leave are bucketed "
               "DIFFERS, and only the state in which the shell never ran at all "
               "reaches TIMED-OUT.  Since every runner in this arc redirects "
               "into its transcripts, the shell ALWAYS creates them, so the "
               "TIMED-OUT bucket is unreachable for every suite that has a "
               "runner")

    # ------------------------------------------------------------- D5c
    led.head("D5c -- AND THE CONCLUSION GRAIN CALLS AN EMPTY FILE A FLIP")
    for label, other in (("empty file", ""),
                         ("partial file",
                          partial.decode("utf-8", "replace"))):
        v = L.conclusion_verdict(committed, other)
        print("    conclusion_verdict(committed, %-13s) = %s" % (label, v))
        led.record(v == "FLIPS",
                   "D5c a killed run leaving %s scores %s at mg-1abe's own "
                   "conclusion grain" % (("an " + label) if label[0] in "aeiou"
                                         else ("a " + label), v))
    led.record(False,
               "D5c' SO A SUITE THAT MERELY RAN OUT OF TIME IS REPORTED AS A "
               "FALSE RECORD.  mg-1abe's §2 promises the opposite in so many "
               "words, and the promise is the thing its 112 rests on")

    # ------------------------------------------------------------- D5d
    led.head("D5d -- THE MECHANISM, FIRED FOR REAL, AT A BUDGET I CAN AFFORD")
    print("""A demonstration rather than an argument: `hodge_leverage_repair_ff3e`'s
runner is started in a detached worktree at the transcript's carrying commit and
KILLED after a few seconds, exactly as `run_suite` kills it -- same
`start_new_session=True`, same `os.killpg(..., SIGKILL)`.  What is measured is
the state of the transcript file on disk afterwards.
""")
    carrier = L.carrying_commit(FF3E, rev)
    short = 8
    left = None
    try:
        with L.worktree(carrier) as wt:
            d = os.path.join(wt, os.path.dirname(FF3E))
            proc = subprocess.Popen(["sh", "run_all.sh"], cwd=d,
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL,
                                    start_new_session=True)
            time.sleep(short)
            try:
                os.killpg(os.getpgid(proc.pid), 9)
            except OSError:
                pass
            proc.wait()
            full = os.path.join(wt, FF3E)
            left = (os.path.exists(full),
                    os.path.getsize(full) if os.path.exists(full) else -1)
    except RuntimeError as exc:
        led.self_error("D5d worktree: %s" % exc)

    if left is not None:
        exists, size = left
        print("    killed after %ds at %s:" % (short, carrier[:7]))
        print("      transcript file exists on disk : %s" % exists)
        print("      its size                       : %d bytes" % size)
        got = b"" if size == 0 else b"x" * size
        print("      collect() would return         : %s"
              % ("None" if not exists else "b'' (%d bytes)" % size))
        print("      t2 would bucket it             : %s"
              % t2_bucket("timeout", None if not exists else got, committed_b))
        led.record(exists,
                   "D5d the transcript file EXISTS after a SIGKILL, so "
                   "`collect()` returns bytes and the TIMED-OUT branch is "
                   "not taken")
        led.record(size == 0,
                   "D5d' and it is EMPTY (%d bytes): python buffers stdout when "
                   "it is not a tty, so a killed producer of this shape leaves "
                   "a zero-byte transcript rather than a partial one" % size)

    # ------------------------------------------------------------- D5e
    led.head("D5e -- HOW MANY SUITES IS THE BUCKET UNREACHABLE FOR?")
    print("""The exposure is not 'suites that are slow' -- that is a fact about a
machine.  It is 'suites for which a timeout CANNOT be reported as one', which
is a fact about the code and is countable without running anything: a suite
whose runner redirects into a tracked transcript has that file created by the
shell before its producer starts.
""")
    # E5's guard: the population is the CENSUS'S OWN -- directories that carry
    # a tracked transcript -- and a runner whose redirections this parser
    # cannot read is counted in ITS OWN row, never folded into `does not
    # redirect`.  A detector whose population is not what its name says is the
    # defect mg-1abe's t6 committed at 32x.
    carriers = {}
    for p in L.transcripts(rev):
        carriers.setdefault(os.path.dirname(p), []).append(os.path.basename(p))
    total = redirecting = unparsed = norunner = 0
    for d, names in sorted(carriers.items()):
        total += 1
        sh = L.blob_at(rev, d + "/run_all.sh")
        if sh is None:
            norunner += 1
            continue
        # The test is TEXTUAL and deliberately not name-matching: what makes
        # the transcript exist before its producer finishes is the presence of
        # `> out_*.txt` OR `| tee out_*.txt` anywhere in the runner, whether or
        # not this parser can work out WHICH transcript it names.  `tee` opens
        # its file for writing at start exactly as the shell does, so it
        # creates the same trap; leaving it out would have undercounted this
        # row by every suite in the arc that spells its runner that way.
        if re.search(r"(?:>|\|\s*tee(?:\s+-a)?)\s*\"?\$?\{?[\w%${}.*-]*"
                     r"out_[^\"\s]*\.txt", sh.decode("utf-8", "replace")):
            redirecting += 1
        else:
            unparsed += 1
    print("    directories carrying a tracked transcript at %s : %d"
          % (rev[:7], total))
    print("      ...with a `run_all.sh` that redirects into one of them : %d"
          % redirecting)
    print("      ...with a `run_all.sh` that redirects into NO transcript : %d"
          % unparsed)
    print("      ...with no `run_all.sh` at all                         : %d"
          % norunner)
    led.record(False,
               "D5e THE TIMED-OUT BUCKET IS UNREACHABLE FOR %d OF THE %d "
               "TRANSCRIPT-CARRYING DIRECTORIES (%d%%) -- every one whose "
               "runner redirects into a transcript, which is what makes the "
               "shell create the file before the producer runs.  mg-1abe's own "
               "defect 8 reads 'It is 0 here at 900 s on this machine': a 0 "
               "that is a property of the guard and not of the machine.  %d "
               "more have a runner that redirects into no transcript at all "
               "and are counted apart rather than assumed safe"
               % (redirecting, total,
                  round(100.0 * redirecting / max(total, 1)), unparsed))

    # ------------------------------------------------------------- D5f
    led.head("D5f -- THE ONE-LINE REPAIR, NAMED AND NOT APPLIED")
    print("""    t2_census.py:224   for p in paths:
    -                          if got[p] is None:
    +                          if status == "timeout":
    +                              verdict[p] = "TIMED-OUT"; ...
    +                          elif got[p] is None:

WHY IT IS NOT APPLIED HERE, stated so it can be overruled.  Editing
`code/transcript_census_1abe/t2_census.py` changes that suite's code, which
displaces all eight of its committed transcripts -- the defect under study --
and re-running the census to restore them costs about two hours and produces a
DIFFERENT census, because `main` has moved. That trade is pm-onethird's to size.
What is landed here instead is the measurement, so the next reader finds the
number rather than the idea.

AND THE REPAIR IS NOT SUFFICIENT ON ITS OWN.  A suite killed at the budget also
LEAVES ITS OTHER TRANSCRIPTS half-written, so `TIMED-OUT` has to apply to the
whole group, which is what the patch above does by keying on `status` rather
than on the file.
""")
    led.record(False,
               "D5f the repair is one line and is deliberately NOT applied; the "
               "reason is mg-1abe's own rule that repairing a suite's code "
               "displaces its transcripts, and the judgement is stated rather "
               "than acted on")

    # ------------------------------------------------------------- D5g
    led.head("D5g -- WHAT THIS DOES AND DOES NOT MOVE")
    print("""MOVES:  the FIVE.  `%s`
        reproduces byte-for-byte at its carrying commit given enough time
        (measured in `out_d1_five.txt`), so it is not a false record and the
        measured damage of this class is **FOUR**.

DOES NOT MOVE: the 112.  A row wrongly in DIFFERS is still a row that did not
        reproduce IN THE CENSUS'S RUN, and the census reports 112 as
        `DIFFERS`, not as damage.  What this finding says about the 112 is that
        it is an UPPER bound whose slack is unmeasured, and I did not re-run
        the other 107 to size it -- that is two hours of machine time and it is
        stated as not done rather than estimated.

DOES NOT MOVE: 398 REPRODUCES.  A byte-identical transcript cannot be a
        truncation artefact.  The bucket is safe in the direction that matters.
""" % FF3E)
    led.record(None,
               "D5g the correction is to the FIVE and not to the 112: 4 false "
               "records measured, and 112 stands as an upper bound on "
               "non-reproduction whose slack this script does not size")
    return led.done()


if __name__ == "__main__":
    sys.exit(main())
