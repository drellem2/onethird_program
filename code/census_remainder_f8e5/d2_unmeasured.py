"""d2_unmeasured -- THE 31 THAT WERE NEVER MEASURED AGAINST THEIR BYTES.

mg-1abe bucketed 31 of 541 transcripts `NO-RUNNER` and said, correctly, that
its census says NOTHING about them -- "not *they are fine*: nothing".  Its
defect 7 keeps that as a defect rather than a footnote.

"REPORTED AS SUCH" WAS THE RIGHT CALL FOR A CENSUS AND IT IS NOT A RESTING
PLACE.  A denominator with a permanent hole in it is one nobody can close, and
"no `run_all.sh`" is a fact about a FILENAME, not about whether the transcript
can be reproduced.  So this script asks the two questions the census did not:

    WHY was each one unmeasurable?
    CAN it be made measurable -- and if so, WHAT DOES IT SAY?

RECOVERY IS TIERED AND EVERY TIER IS EXECUTED.  It would be cheap and wrong to
answer "yes, measurable" by pointing at a script whose name matches: a filename
that maps is not a producer that reproduces (this item's own E3).  So every
recovered producer is RUN, in a detached worktree at the transcript's carrying
commit, and the bytes are compared.

  T1-RUNNER    `run_all.sh`, the census's own rule.  None of the 31 has one --
               that is what put them here.
  T2-OTHER-SH  a runner under another name, parsed by mg-1abe's OWN
               `parse_producers`.  This arc spells runners `run_audit.sh` as
               well as `run_all.sh`, and the census's rule is a string.
  T3-NAME-MAP  `out_<stem>.txt` <- `<stem>.py` or `audit_<stem>.py`.  A GUESS,
               labelled as one, and the reason mg-1abe refused to guess is
               kept: guessing wrong makes the damage look smaller.  What makes
               it safe here is that the guess is then RUN, so a wrong guess
               shows up as a producer that writes nothing or writes garbage --
               not as a reproduction.
  T4-NONE      no producer at that commit by any rule.  Genuinely unmeasurable.

⚠️ A T3 REPRODUCTION IS STRONGER EVIDENCE THAN A T3 DIFFERENCE.  If a guessed
producer emits the committed bytes exactly, the guess was right and the
transcript reproduces.  If it does not, either the guess was wrong or the
transcript does not reproduce, and this script CANNOT TELL THOSE APART.  Every
T3 non-reproduction is therefore reported as `T3-UNRESOLVED`, never as
`DIFFERS`.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_f8e5 as L


def arg(name, default):
    a = sys.argv
    return type(default)(a[a.index(name) + 1]) if name in a else default


def main():
    at = L.main_rev()
    rev = L.resolve(at)
    timeout = arg("--timeout", 900)
    led = L.Ledger("d2 -- THE 31 NEVER MEASURED AGAINST THEIR BYTES",
                   reads_outside_tree=True)
    print("    as-of: %s   producer timeout: %ds" % (rev[:12], timeout))

    # ------------------------------------------------------------ D2a
    led.head("D2a -- THE POPULATION, RE-DERIVED RATHER THAN QUOTED")
    print("""The 31 are re-derived from the census's own rule -- a tracked
`code/<dir>/out_*.txt` whose directory has no `run_all.sh` at its CARRYING
COMMIT -- rather than copied out of `out_t2_census.txt`.  If the count comes
out at something other than 31 at this revision that is itself worth knowing,
because the population is a fact about a moving `main`.
""")
    pop = []
    for p in L.transcripts(rev):
        c = L.carrying_commit(p, rev)
        if c and L.blob_at(c, os.path.dirname(p) + "/run_all.sh") is None:
            pop.append((p, c))
    by_dir = {}
    for p, c in pop:
        by_dir.setdefault(os.path.dirname(p), []).append((p, c))
    print("    transcripts with no `run_all.sh` at their carrying commit: %d"
          % len(pop))
    print("    over %d directories" % len(by_dir))
    led.record(None,
               "D2a the NO-RUNNER population at %s is %d transcripts over %d "
               "directories (mg-1abe measured 31 over 10 at 81214a9; a "
               "different number here is `main` having moved, not a "
               "disagreement)" % (rev[:7], len(pop), len(by_dir)))

    # ------------------------------------------------------------ D2b
    led.head("D2b -- WHY EACH WAS UNMEASURABLE, AND BY WHICH RULE IT IS "
             "RECOVERED")
    rows = []
    for d in sorted(by_dir):
        for p, c in sorted(by_dir[d]):
            spec, tier, note = L.recover_producer(p, c)
            listing = [ln.split("\t", 1)[1] for ln in
                       L.git("ls-tree", "%s:%s" % (c, d)).split("\n")
                       if "\t" in ln]
            shs = [x for x in listing if x.endswith(".sh")]
            rows.append({"path": p, "carrier": c, "spec": spec, "tier": tier,
                         "note": note, "shs": shs})
    print("    %-52s %-8s %-12s %s" % ("transcript", "at", "tier", "producer"))
    for r in rows:
        print("    %-52s %-8s %-12s %s"
              % (r["path"][5:], r["carrier"][:7], r["tier"],
                 r["spec"]["script"] if r["spec"] else "(none)"))

    print()
    print("    WHY, by directory -- the reason is a property of the directory, "
          "not of the file:")
    for d in sorted(by_dir):
        rs = [r for r in rows if os.path.dirname(r["path"]) == d]
        tiers = sorted({r["tier"] for r in rs})
        shs = rs[0]["shs"]
        if "T2-OTHER-SH" in tiers:
            why = ("HAS A RUNNER UNDER ANOTHER NAME: %s.  The census's rule is "
                   "the literal string `run_all.sh`" % ", ".join(shs))
        elif "T3-NAME-MAP" in tiers:
            why = ("NO RUNNER OF ANY NAME (%s).  Its scripts were run by hand, "
                   "and only the filename convention connects a transcript to "
                   "one" % (", ".join(shs) if shs else "no `.sh` at all"))
        else:
            why = "NO RUNNER AND NO SCRIPT THAT MAPS TO THE TRANSCRIPT"
        print("      %-42s %d transcript(s): %s" % (d[5:], len(rs), why))

    tier_counts = {}
    for r in rows:
        tier_counts[r["tier"]] = tier_counts.get(r["tier"], 0) + 1
    print()
    for t in ("T1-RUNNER", "T2-OTHER-SH", "T3-NAME-MAP", "T4-NONE"):
        print("    %-14s %d" % (t, tier_counts.get(t, 0)))
    led.record(None,
               "D2b of %d unmeasured transcripts, %d are recovered by widening "
               "ONE STRING (`run_all.sh` -> any tracked `*.sh` the census's own "
               "parser can read), %d by the arc's filename convention, and %d "
               "by nothing at all"
               % (len(rows), tier_counts.get("T2-OTHER-SH", 0),
                  tier_counts.get("T3-NAME-MAP", 0),
                  tier_counts.get("T4-NONE", 0)))

    # ------------------------------------------------------------ D2c
    led.head("D2c -- EVERY RECOVERED PRODUCER IS RUN, AND THE BYTES COMPARED")
    print("""E3's guard, filed in advance: a filename that maps is not a producer
that reproduces.  Each recovered producer below is executed in a detached
worktree at the transcript's own carrying commit, with the worktree asserted
CLEAN before it starts.
""")
    print("    %-52s %-12s %-16s %s"
          % ("transcript", "tier", "verdict", "detail"))
    verdicts = {}
    for r in rows:
        if r["spec"] is None:
            r["verdict"] = "UNMEASURABLE"
            r["detail"] = r["note"]
        else:
            res = L.rerun_at(r["carrier"], r["path"], r["spec"],
                             timeout=timeout)
            if res["error"]:
                r["verdict"] = "RUNNER-FAILED"
                r["detail"] = res["error"][:60]
            elif res["bytes"] is None:
                r["verdict"] = "NOT-REGENERATED"
                r["detail"] = "producer wrote nothing (exit %s)" % res["rc"]
            elif res["bytes"] == L.blob_at(rev, r["path"]):
                r["verdict"] = "REPRODUCES"
                r["detail"] = "%.0fs" % res["seconds"]
            elif r["tier"] == "T3-NAME-MAP":
                # A guessed producer that disagrees cannot distinguish `the
                # guess was wrong` from `it does not reproduce`.  Reported as
                # its own bucket rather than as DIFFERS.
                r["verdict"] = "T3-UNRESOLVED"
                r["detail"] = "guessed producer, bytes differ (%s)" % (
                    L.conclusion_verdict(
                        L.blob_at(rev, r["path"]).decode("utf-8", "replace"),
                        res["bytes"].decode("utf-8", "replace")))
            else:
                r["verdict"] = "DIFFERS"
                r["detail"] = "conclusion %s" % L.conclusion_verdict(
                    L.blob_at(rev, r["path"]).decode("utf-8", "replace"),
                    res["bytes"].decode("utf-8", "replace"))
        verdicts[r["verdict"]] = verdicts.get(r["verdict"], 0) + 1
        print("    %-52s %-12s %-16s %s"
              % (r["path"][5:], r["tier"], r["verdict"], r["detail"][:44]))

    print()
    for k in sorted(verdicts):
        print("    %-16s %d" % (k, verdicts[k]))
    measured = sum(v for k, v in verdicts.items()
                   if k in ("REPRODUCES", "DIFFERS"))
    led.record(None,
               "D2c %d of the %d previously-unmeasured transcripts are now "
               "MEASURED AGAINST THEIR BYTES (%d reproduce, %d do not); %d are "
               "T3-UNRESOLVED, where a guessed producer disagreeing cannot be "
               "told from a transcript that does not reproduce; %d remain "
               "unmeasurable by any rule"
               % (measured, len(rows), verdicts.get("REPRODUCES", 0),
                  verdicts.get("DIFFERS", 0), verdicts.get("T3-UNRESOLVED", 0),
                  verdicts.get("UNMEASURABLE", 0)))

    # ------------------------------------------------------------ D2d
    led.head("D2d -- WHAT IS LEFT, AND WHETHER IT CAN EVER BE CLOSED")
    left = [r for r in rows if r["verdict"] in
            ("UNMEASURABLE", "T3-UNRESOLVED", "RUNNER-FAILED",
             "NOT-REGENERATED")]
    if not left:
        print("    Nothing.  Every one of the %d is measured." % len(rows))
    for r in left:
        print("    %s" % r["path"][5:])
        print("        at %s, tier %s: %s"
              % (r["carrier"][:7], r["tier"], r["detail"][:100]))
        if r["verdict"] == "UNMEASURABLE":
            print("        CAN IT BE CLOSED? Not from this repository.  There "
                  "is no script at that commit\n"
                  "        that the transcript's name reaches and no runner "
                  "that names it.  Closing it\n"
                  "        needs the producer, which was never committed.")
        elif r["verdict"] == "T3-UNRESOLVED":
            print("        CAN IT BE CLOSED? Yes, by ONE piece of information "
                  "nobody has to re-derive:\n"
                  "        the command that produced it.  Under the convention "
                  "adopted in `d3`, a\n"
                  "        transcript declares its own producer, so this "
                  "bucket cannot recur.")
        else:
            print("        CAN IT BE CLOSED? The producer exists and did not "
                  "produce the file here;\n"
                  "        that is a fact about the run, and re-running it "
                  "with a larger budget or on\n"
                  "        a different machine may move it.")
    led.record(bool(left),
               "D2d %d of the %d are NOT closed by this script and each carries "
               "the reason and whether it can ever be closed.  `reported as "
               "such` is now `reported as such WITH A ROUTE OUT OR A REASON "
               "THERE IS NONE`" % (len(left), len(rows)))

    return led.done()


if __name__ == "__main__":
    sys.exit(main())
