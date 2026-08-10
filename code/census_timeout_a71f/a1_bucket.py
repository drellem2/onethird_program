"""a1 -- THE BUCKET THAT COULD NOT FIRE, BEFORE AND AFTER, ON THE SAME STATES.

mg-1abe's README §2 states the rule that makes its `112` mean what it says:

    "`TIMED-OUT` is never folded into `DIFFERS`.  'I did not finish measuring'
     and 'it does not reproduce' are different claims and only one is about the
     subject."

cf8e5 measured that the instrument does the opposite of that rule, always, and
deliberately did not repair it.  mg-a71f applies the repair.  This script is
the control that has to be able to REFUSE it, and it is built to refuse in four
different directions:

  A1a  the two classifiers below are TRANSCRIPTIONS, and a transcription is
       inadmissible until it is checked against the text it transcribes.  Both
       are checked against real blobs -- the BEFORE against `81214a9`, the
       commit every published census figure was measured at, and the AFTER
       against `HEAD`.  If the repair is not in the tree, A1a says so and every
       row below is scored against a claim rather than against code.
  A1b  the four states a SIGKILL at the budget can leave, through both.
  A1c  what the DIFFERS route then computes: `conclusion_verdict(x, "")`.
  A1d  THE ARM THAT GUARDS MY OWN REPAIR.  A repair to a classifier is a
       classifier, so it can mis-bucket.  Every non-timeout status is
       enumerated and the two classifiers must agree on EVERY one of them: the
       repair is licensed to change the timeout column and nothing else.
  A1e  and the reach: how much of the arc the unreachable bucket covered.

WHY BYTE-IDENTICAL-UNDER-A-KILL IS STILL `REPRODUCES`, since that is the one
place the repair is a judgement rather than a mechanism.  The conservative
repair buckets EVERY row of a killed suite as TIMED-OUT.  This one keeps a row
that already matched the committed blob byte-for-byte, because a truncated
write cannot forge the whole blob -- the match is proof the producer finished
that file before the axe fell.  A1b prints both columns so a reader who
disagrees can subtract, and T2f in the census transcript names each such row.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_a71f as L                                            # noqa: E402

T2 = L.CENSUS_DIR + "/t2_census.py"
FF3E = "code/hodge_leverage_repair_ff3e/out_repair_ff3e.txt"


def main():
    rev = L.resolve(L.main_rev())
    led = L.Ledger("a1 -- THE CENSUS'S `TIMED-OUT` BUCKET, BEFORE AND AFTER "
                   "THE mg-a71f REPAIR")
    print("    as-of      %s" % rev)
    print("    before     blob %s  (the pre-repair t2_census.py, seen at %s)"
          % (L.BEFORE_BLOB[:12], L.BEFORE_SEEN_AT[:7]))
    print("    after      HEAD  (this working tree)")
    print("""
    ⚠️  THE `BEFORE` SIDE IS A BLOB SHA AND NOT A COMMIT, AND NOT `81214a9`.
    Two defects of mine are behind that constant and both are recorded in
    `lib_a71f.py`: `81214a9` is the revision the census MEASURED and the
    census's own code does not exist there, and `git log -1 main -- <path>`
    would name THE REPAIR the moment this merges -- the same moving-ref defect
    this ticket annotates elsewhere, committed inside the annotation.
""")

    # ------------------------------------------------------------------ A1a
    led.head("A1a -- BOTH CLASSIFIERS ARE TRANSCRIPTIONS, AND BOTH ARE CHECKED")
    print("""
t2's bucketing lives inside a threaded worker holding a lock over three shared
dicts; there is no seam to import.  So it is transcribed, twice, and the
transcription is what is checked here -- a reader does not have to take my word
that `lib_a71f.bucket_before` is what ran.
""")
    before_src = L.blob_by_sha(L.BEFORE_BLOB)
    after_src = L.blob_at("HEAD", T2)
    if before_src is None:
        led.self_error("the pre-repair t2_census.py blob %s does not resolve "
                       "in this object store" % L.BEFORE_BLOB[:12])
        return led.done()
    if after_src is None:
        led.self_error("%s absent at HEAD" % T2)
        return led.done()
    b_txt = before_src.decode("utf-8", "replace")
    a_txt = after_src.decode("utf-8", "replace")

    OLD_GUARD = r"if got\[p\] is None:\s*\n\s*if status == \"timeout\""
    NEW_GUARD = (r"if got\[p\] is None or \(status == \"timeout\"\s*\n\s*"
                 r"and got\[p\] != committed\[p\]\)")
    seen = L.blob_at(L.BEFORE_SEEN_AT, T2)
    checks = [
        ("BEFORE: that blob IS the t2_census.py committed at %s"
         % L.BEFORE_SEEN_AT[:7], seen is not None and seen == before_src),
        ("BEFORE: the TIMED-OUT branch is guarded by the file's ABSENCE",
         re.search(OLD_GUARD, b_txt) is not None),
        ("BEFORE: and there is no timeout-status guard anywhere in it",
         re.search(NEW_GUARD, b_txt) is None),
        ("AFTER: the TIMED-OUT branch is guarded by the timeout STATUS",
         re.search(NEW_GUARD, a_txt) is not None),
        ("AFTER: the absence-only guard is gone",
         re.search(OLD_GUARD, a_txt) is None),
        ("BOTH: the runner is still started as `sh run_all.sh`, so the shell "
         "still creates the file",
         'subprocess.Popen(["sh", "run_all.sh"]' in b_txt
         and 'subprocess.Popen(["sh", "run_all.sh"]' in a_txt),
        ("BOTH: collect() still returns bytes for any file that EXISTS -- the "
         "repair did not touch it",
         "if os.path.exists(full):" in b_txt and "if os.path.exists(full):"
         in a_txt),
    ]
    for what, ok in checks:
        led.record(ok, "A1a %s" % what)
    if not all(ok for _, ok in checks):
        led.self_error("A1a a transcription does not match its source; every "
                       "row below is about a paraphrase and must not be read "
                       "as a measurement of the census")

    # ------------------------------------------------------------------ A1b
    led.head("A1b -- THE FOUR STATES A SIGKILL AT THE BUDGET CAN LEAVE")
    committed_b = L.blob_at(rev, FF3E)
    if committed_b is None:
        led.self_error("%s absent at %s" % (FF3E, rev[:7]))
        return led.done()
    partial = committed_b[:len(committed_b) // 3]

    print("""
The FIRST thing a POSIX shell does with `python3 t.py > out_t.txt` is CREATE
`out_t.txt`.  The producer has not run.  So of the four states below, the only
one the pre-repair guard could ever see is the first -- and the first requires
the shell never to have started, which is the one thing a runner always does.
""")
    print("    %-46s %-14s %-14s" % ("state left by a SIGKILL at the budget",
                                     "BEFORE", "AFTER"))
    print("    %s %s %s" % ("-" * 46, "-" * 14, "-" * 14))
    cases = [
        ("file never created (no shell ran at all)", None,
         "TIMED-OUT", "TIMED-OUT"),
        ("created, EMPTY (python buffered its stdout)", b"",
         "DIFFERS", "TIMED-OUT"),
        ("created, PARTIAL (one buffer flush landed)", partial,
         "DIFFERS", "TIMED-OUT"),
        ("created, COMPLETE (killed by a LATER script)", committed_b,
         "REPRODUCES", "REPRODUCES"),
    ]
    for label, got, exp_b, exp_a in cases:
        gb = L.bucket_before("timeout", got, committed_b)
        ga = L.bucket_after("timeout", got, committed_b)
        print("    %-46s %-14s %-14s" % (label, gb, ga))
        led.record(gb == exp_b and ga == exp_a,
                   "A1b `%s` -> BEFORE %s (expected %s), AFTER %s (expected "
                   "%s)" % (label, gb, exp_b, ga, exp_a))

    reach_before = sum(1 for _, g, _, _ in cases
                       if L.bucket_before("timeout", g, committed_b)
                       == "TIMED-OUT")
    reach_after = sum(1 for _, g, _, _ in cases
                      if L.bucket_after("timeout", g, committed_b)
                      == "TIMED-OUT")
    led.record(reach_before > 1,
               "A1b' BEFORE the repair, %d of the 4 states a killed run can "
               "leave reach TIMED-OUT, and the one that does requires the "
               "SHELL NEVER TO HAVE RUN.  Every runner in this arc redirects, "
               "so the shell always runs and always creates the file: the "
               "bucket is unreachable by construction, not by bad luck"
               % reach_before)
    led.record(None,
               "A1b'' AFTER the repair, %d of the 4 reach it.  The fourth is "
               "byte-identical-under-a-kill and is kept as REPRODUCES on "
               "purpose: a truncated write cannot forge the whole blob"
               % reach_after)

    # ------------------------------------------------------------------ A1c
    led.head("A1c -- AND THE DIFFERS ROUTE DOES NOT MERELY LOSE THE ROW")
    print("""
DIFFERS is not a dead end in this instrument.  Every DIFFERS is handed to
`conclusion_verdict(committed, got)`, and its answer is what the census
publishes as a FALSE RECORD.  So the pre-repair guard did not lose information
about a slow suite; it MANUFACTURED damage out of slowness.
""")
    committed_t = committed_b.decode("utf-8", "replace")
    for label, other in (("against an EMPTY file", ""),
                         ("against a PARTIAL file",
                          partial.decode("utf-8", "replace"))):
        v = L.conclusion_verdict(committed_t, other)
        print("    conclusion_verdict(committed, %-24s = %s" % (label + ")", v))
        led.record(v != "FLIPS",
                   "A1c a killed run of this suite, %s, is scored `%s` -- and "
                   "`FLIPS` is the census's word for A FALSE RECORD AT ITS "
                   "CARRYING COMMIT" % (label, v))
    print()
    print("    THE ONE THIS ACTUALLY HAPPENED TO:")
    print("      %s" % FF3E)
    print("      mg-1abe published it as 1 of its FIVE FALSE RECORDS.  cf8e5 "
          "ran it to completion")
    print("      at its carrying commit: it REPRODUCES BYTE-FOR-BYTE in "
          "1470 s against a 900 s budget.")

    # ------------------------------------------------------------------ A1d
    led.head("A1d -- THE ARM THAT GUARDS THE REPAIR: NOTHING BUT THE TIMEOUT "
             "COLUMN MAY MOVE")
    print("""
A repair to a classifier is a classifier and is subject to the defect it
repairs.  The licence mg-a71f was given is narrow -- make the timeout status
reachable -- so every OTHER cell of the classifier must be unchanged, and that
is checkable exhaustively rather than by inspection.  Statuses x states, every
combination, both classifiers.  Any disagreement outside the `timeout` row is a
SELF-ERROR: it would mean the repair moved rows nobody authorised it to move.
""")
    states = [("absent", None), ("empty", b""), ("partial", partial),
              ("identical", committed_b)]
    statuses = ["ok", "failed:1", "failed:2", "failed:127", "timeout"]
    drift = []
    for st in statuses:
        cells = []
        for sname, got in states:
            gb = L.bucket_before(st, got, committed_b)
            ga = L.bucket_after(st, got, committed_b)
            cells.append("%s%s" % (gb, "" if gb == ga else " -> " + ga))
            if gb != ga and st != "timeout":
                drift.append((st, sname, gb, ga))
        print("    %-11s %s" % (st, " | ".join("%-22s" % c for c in cells)))
    print("    %-11s %s" % ("", " | ".join("%-22s" % s for s, _ in states)))
    led.record(not drift,
               "A1d the two classifiers agree on EVERY combination of the %d "
               "non-timeout statuses with the %d file states.  The repair "
               "moves the timeout row and nothing else"
               % (len(statuses) - 1, len(states)))
    for st, sname, gb, ga in drift:
        led.self_error("A1d status=%s state=%s moved %s -> %s and nothing "
                       "authorised that" % (st, sname, gb, ga))

    # ------------------------------------------------------------------ A1e
    led.head("A1e -- THE REACH: HOW MUCH OF THE ARC THE UNREACHABLE BUCKET "
             "COVERED")
    print("""
A bucket that cannot fire matters in proportion to how many suites could have
needed it.  A suite is UNREACHABLE-BY-CONSTRUCTION when its own `run_all.sh`,
at the carrying commit, CREATES the transcript by redirection or by `tee`
before the producer writes a byte of it.

⚠️  THIS IS A PROXY AND IS STATED AS ONE.  It reads the runner's text for a
redirection into an `out_*`-shaped target; a runner that builds its target
through a variable this pattern cannot see is counted UNDETERMINED rather than
silently as reachable, and the undetermined count is printed.  The direction it
can be wrong in is therefore named: it UNDER-counts the reach.
""")
    redirect = re.compile(r"(>\s*\"?\$?\{?[\w./${}%-]*out_)|(\|\s*tee\s+\"?\$?"
                          r"\{?[\w./${}%-]*out_)")
    population = L.transcripts(rev)
    groups = {}
    for p in population:
        groups.setdefault((p.split("/")[1], L.carrying_commit(p, rev)),
                          []).append(p)
    dirs = sorted({d for d, _ in groups})
    unreachable, no_runner, undetermined = [], [], []
    for d, c in sorted(groups):
        blob = L.blob_at(c, "code/%s/run_all.sh" % d)
        if blob is None:
            no_runner.append(d)
        elif redirect.search(blob.decode("utf-8", "replace")):
            unreachable.append(d)
        else:
            undetermined.append(d)
    unreachable = sorted(set(unreachable))
    print("    population              %d transcripts in %d directories at %s"
          % (len(population), len(dirs), rev[:7]))
    print("    runner CREATES the file %4d directories   <- TIMED-OUT could "
          "never fire for any of these" % len(unreachable))
    print("    no runner at all        %4d directories   <- nothing to fire"
          % len(sorted(set(no_runner))))
    print("    undetermined            %4d directories   <- the proxy cannot "
          "read the runner's target" % len(sorted(set(undetermined))))
    led.record(not unreachable,
               "A1e the TIMED-OUT bucket was unreachable by construction for "
               "%d of the %d transcript-carrying directories at %s, and the "
               "proxy under-counts by design"
               % (len(unreachable), len(dirs), rev[:7]))

    return led.done()


if __name__ == "__main__":
    sys.exit(main())
