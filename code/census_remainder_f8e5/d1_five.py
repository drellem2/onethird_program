"""d1_five -- THE FIVE FALSE RECORDS, DISPOSED OF ONE AT A TIME.

mg-1abe measured 5 of 541 committed transcripts as FALSE RECORDS: re-run at the
commit carrying them, a DECISION changes.  It named them and stopped, correctly
-- its ticket said measure and do not repair.  This script disposes of them.

FOR EACH, THREE THINGS AND THEN A REMEDY:

  WHAT THE ARTIFACT ASSERTS   the decision rows the committed bytes carry
  WHAT IS TRUE AT ITS COMMIT  the decision rows the same producer emits when
                              re-run in a detached worktree at that commit
  WHY THEY DIFFER             adjudicated, not assumed -- see below
  REMEDY                      re-run and re-commit / annotate / strike / leave

AND THE ADJUDICATION IS THE POINT.  A changed decision has two causes:

  RECORD-IS-FALSE    the world at the carrying commit disagrees with the
                     record.  A reader who checks out that commit and reads the
                     transcript is misled.  Remedy: re-run and re-commit, or
                     annotate with the revision it is a fact about.

  RERUN-CANNOT-SEE   the world is as the record describes and the INSTRUMENT
                     has lost its view of it -- a ref deleted, a branch pruned.
                     The record is the only surviving witness.  Remedy: DO NOT
                     RE-RUN.  Re-running writes the instrument's blindness over
                     the measurement.

  Collapsing these two into "5 false records" would be a 5-for-4 over-report of
  exactly the kind this ticket exists to prevent -- smaller than the 112-for-5
  one, and the same error.

⚠️ COST.  ARM A re-runs five producers at five commits.  Four are under two
minutes; `hodge_leverage_repair_ff3e` writes into three documents, runs a gate
as a subprocess for every probe and re-runs four other instruments, and takes
TENS OF MINUTES.  ARM B is skipped for any producer whose ARM A exceeded
`--armb-budget` seconds (default 300) and the skip is printed, never silent.

⚠️ E1's GUARD, from this item's own PREDICTIONS.md D5: every re-run asserts its
worktree is CLEAN BEFORE IT STARTS.  A producer that mutates the tree and is
interrupted leaves the next run measuring the previous run's wreckage, and one
of these five refuses to run at all against a dirty tree -- a refusal that
reads exactly like a census verdict if nobody checks.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_f8e5 as L


def arg(name, default):
    a = sys.argv
    return type(default)(a[a.index(name) + 1]) if name in a else default


def decision_diff(committed, rerun):
    """(gone, appeared) decision rows, at mg-1abe's own tag grain."""
    ta, tb = L.verdict_tags(committed), L.verdict_tags(rerun)
    from collections import Counter
    ca, cb = Counter(ta), Counter(tb)
    gone = sorted((ca - cb).elements())
    appeared = sorted((cb - ca).elements())
    return gone, appeared


def line_for(text, tag):
    """The full committed line behind a decision tag, for the report."""
    for ln in L.verdict_lines(text):
        norm = ln[:ln.index("]") + 1] if ln.startswith("[") and "]" in ln else ln
        if norm == tag:
            return ln
    return tag


def unreachable_evidence(text):
    """Commits the transcript names that RESOLVE but hang off no ref.

    This is the mechanical half of the adjudication.  An instrument that finds
    its inputs by walking refs cannot see such a commit; the object is present,
    so the record's claim about it is still checkable BY NAME even though the
    instrument's search no longer reaches it.
    """
    out = []
    for full in L.shas_named_in(text):
        if not L.git_ok("merge-base", "--is-ancestor", full, "main"):
            refs = L.git("for-each-ref", "--contains", full,
                         "--format=%(refname)").split()
            if not refs:
                out.append(full)
    return out


def main():
    at = L.main_rev()
    rev = L.resolve(at)
    budget = arg("--armb-budget", 300)
    timeout = arg("--timeout", 3600)
    only = arg("--only", "")

    led = L.Ledger("d1 -- THE FIVE FALSE RECORDS, DISPOSED OF ONE AT A TIME",
                   reads_outside_tree=True)
    print("    as-of: %s   (`main` resolved ONCE by run_all.sh and passed in)"
          % rev[:12])
    print("    ARM B budget: %ds     producer timeout: %ds" % (budget, timeout))

    led.head("D1a -- THE FIVE, AS mg-1abe NAMED THEM")
    print("""These five are QUOTED from `code/transcript_census_1abe/README.md`
§3 and its `out_t2_census.txt`.  They are the census's finding; re-deriving the
whole 541-transcript sweep to rediscover them would be a second census, not a
disposal.  What is re-derived below, per transcript, is the FLIP itself.
""")
    for p in L.THE_FIVE:
        print("    %s" % p)

    rows = []
    for path in L.THE_FIVE:
        if only and only not in path:
            continue
        led.head("D1b -- %s" % path)
        carrier = L.carrying_commit(path, rev)
        committed_b = L.blob_at(rev, path)
        if carrier is None or committed_b is None:
            led.self_error("%s is not tracked at %s" % (path, rev[:7]))
            continue
        committed = committed_b.decode("utf-8", "replace")
        spec, why = L.producer_for(path, carrier)
        if spec is None:
            led.self_error("no producer for %s at %s: %s"
                           % (path, carrier[:7], why))
            continue
        print("    carrying commit : %s" % carrier[:12])
        print("    producer        : %s   (as %s's own run_all.sh spells it)"
              % (spec["cmd"], os.path.dirname(path)))

        res = L.rerun_at(carrier, path, spec, timeout=timeout,
                         committed=committed_b)
        if res["error"]:
            led.self_error("ARM A on %s: %s" % (path, res["error"]))
            continue
        print("    ARM A           : re-run at the carrying commit, "
              "clean worktree asserted (%d dirty before), %.0fs, exit %s, "
              "status %s"
              % (len(res["dirty_before"]), res["seconds"], res["rc"],
                 res["status"]))
        if res["status"] != "ok":
            # THE GUARD `d5` ARGUES FOR, APPLIED HERE.  A producer that timed
            # out or died is NOT a transcript that disagrees with itself, and
            # comparing the empty file its own redirection created against the
            # committed bytes is exactly the artefact this suite reports.  It
            # is a SELF-ERROR and not a finding: the fault is in this run.
            led.self_error(
                "ARM A on %s is %s (exit %s, %d bytes written) and is NOT "
                "compared against the committed bytes.  A run that did not "
                "finish has not been shown to disagree with anything"
                % (path, res["status"], res["rc"],
                   len(res["bytes"] or b"")))
            continue
        rerun = res["bytes"].decode("utf-8", "replace")
        identical = res["bytes"] == committed_b
        verdict = L.conclusion_verdict(committed, rerun)
        gone, appeared = decision_diff(committed, rerun)

        print()
        print("    bytes identical : %s" % ("YES" if identical else "no"))
        print("    mg-1abe grain   : %s   (census said FLIPS)" % verdict)
        print()
        print("    WHAT THE ARTIFACT ASSERTS -- decision rows in the committed "
              "bytes that the")
        print("    re-run does NOT emit (%d):" % len(gone))
        for t in gone:
            print("      - %s" % line_for(committed, t)[:150])
        print("    WHAT IS TRUE AT ITS COMMIT -- decision rows the re-run emits "
              "that the")
        print("    committed bytes do NOT carry (%d):" % len(appeared))
        for t in appeared:
            print("      + %s" % line_for(rerun, t)[:150])

        unreach = unreachable_evidence(committed)
        reads_out, ev = L.static_reach(os.path.dirname(path), carrier)
        print()
        print("    commits it names that resolve but hang off NO REF : %d%s"
              % (len(unreach),
                 ("  (" + ", ".join(s[:7] for s in unreach[:6]) + ")")
                 if unreach else ""))
        print("    producer reads repository-global state (STATIC PROXY): %s"
              % ("yes -- " + ", ".join(ev[:3]) if reads_out else "no"))

        rows.append({"path": path, "carrier": carrier, "spec": spec,
                     "committed": committed, "committed_b": committed_b,
                     "rerun": rerun, "identical": identical,
                     "verdict": verdict, "gone": gone, "appeared": appeared,
                     "unreach": unreach, "reads_out": reads_out,
                     "seconds": res["seconds"]})

        if identical:
            led.record(False,
                       "D1b %s REPRODUCES for me where mg-1abe measured DIFFERS."
                       " That is a finding about the census, printed rather than"
                       " dropped to keep the number at five (PREDICTIONS E9)"
                       % path)
        elif verdict != "FLIPS":
            led.record(False,
                       "D1b %s re-runs to %s for me, not FLIPS. The census's"
                       " verdict does not replay and the disagreement is"
                       " printed" % (path, verdict))
        else:
            led.record(None, "D1b %s: FLIP re-derived -- %d decision row(s) lost,"
                             " %d gained" % (path, len(gone), len(appeared)))

        if res["seconds"] > budget:
            print()
            print("    ARM B           : SKIPPED -- ARM A took %.0fs against a "
                  "%ds budget.  This transcript's\n                      "
                  "'which revision is it a fact about' question is NOT ANSWERED "
                  "here, and\n                      that is a budget, not a "
                  "verdict.  `--armb-budget %d` runs it."
                  % (res["seconds"], budget, int(res["seconds"]) + 60))
            rows[-1]["armb"] = "SKIPPED"
            continue

        led.head("D1c -- WHICH REVISION IS IT ACTUALLY A FACT ABOUT? (%s)"
                 % os.path.basename(path))
        print("""⚠️ SYNTHETIC STATE, declared.  Each candidate below is a revision the
transcript NAMES IN ITS OWN BYTES.  The producing directory is checked out from
the CARRYING commit on top of that revision's tree, because the candidate's own
tree may not contain the suite at all.  Nobody ever committed the resulting
state.  This is mg-1abe's own device for mg-b2af's twin and it carries the same
caveat: byte equality here says the transcript is a fact about that TREE, not
that it was produced by that COMMIT.
""")
        cands = [s for s in L.shas_named_in(committed) if s != carrier][:8]
        hit = None
        for cand in cands:
            r = L.rerun_at(cand, path, spec, timeout=timeout,
                           overlay_dir_from=carrier, committed=committed_b)
            if r["error"]:
                print("      %s  ERROR  %s" % (cand[:12], r["error"]))
                continue
            same = r["bytes"] == committed_b
            print("      %s  %s  (%.0fs)"
                  % (cand[:12], "IDENTICAL" if same else "differs",
                     r["seconds"]))
            if same and hit is None:
                hit = cand
        rows[-1]["armb"] = hit or "NONE-OF-%d" % len(cands)
        led.record(None,
                   "D1c %s: %s" % (os.path.basename(path),
                                   ("reproduces EXACTLY at %s -- that is the "
                                    "revision it is a fact about" % hit[:12])
                                   if hit else
                                   ("reproduces at NONE of the %d revisions it "
                                    "names; the tree it is a fact about was "
                                    "never committed, or is not named in its "
                                    "own bytes" % len(cands))))

    # ------------------------------------------------------ adjudication
    led.head("D1d -- THE ADJUDICATION: WHICH OF THE FIVE IS THE RECORD WRONG?")
    print("""THE RULE, stated before the table so it can be disagreed with:

  RERUN-CANNOT-SEE  requires BOTH (i) the committed transcript names one or
                    more commits that RESOLVE in this object store but hang off
                    NO REF, and (ii) the re-run LOSES decision rows rather than
                    gaining them -- the instrument reports LESS than it did.
                    Together these say the instrument's search shrank while the
                    objects stayed put.

  RECORD-IS-FALSE   everything else: the re-run sees at least as much as the
                    record and disagrees with it.

  A judgement, not a measurement.  Both inputs ARE measured and printed above,
  so a reader who thinks the rule is wrong can re-adjudicate from the same
  numbers without re-running anything.
""")
    print("    %-52s %-18s %s" % ("transcript", "cause", "evidence"))
    false_records, blind = [], []
    for r in rows:
        cause = ("RERUN-CANNOT-SEE"
                 if (r["unreach"] and len(r["gone"]) > len(r["appeared"]))
                 else "RECORD-IS-FALSE")
        (blind if cause == "RERUN-CANNOT-SEE" else false_records).append(r)
        r["cause"] = cause
        print("    %-52s %-18s %d unreachable, -%d/+%d rows"
              % (r["path"][5:], cause, len(r["unreach"]),
                 len(r["gone"]), len(r["appeared"])))
    led.record(None,
               "D1d of the %d re-derived FLIPS, %d are RECORD-IS-FALSE and %d "
               "are RERUN-CANNOT-SEE.  The second class is NOT damage to the "
               "record and its remedy is the opposite one"
               % (len(rows), len(false_records), len(blind)))

    # ---------------------------------------------------------- remedies
    led.head("D1e -- THE REMEDY, ONE AT A TIME, WITH ITS REASON")
    print("""Three remedies are available and a fourth is the honest answer for one of
them.  The choice follows from the two measurements above -- the cause, and
whether the producer reads repository-global state:

  RE-RUN AND RE-COMMIT   only when the producer is a fact about a TREE.  A
                         repository-global producer re-run today produces a
                         third answer that is stale again at the next commit,
                         so this remedy is a treadmill for it.
  ANNOTATE               state, in the transcript, the revision it is a fact
                         about -- and under R2, that it is UNPINNABLE.
  STRIKE                 only when the assertion is false and worthless.
  DO NOT RE-RUN          when re-running would overwrite a measurement that
                         cannot be re-taken.
""")
    for r in rows:
        names_own_rev = any(s == r["carrier"] for s in
                            L.shas_named_in(r["committed"]))
        if r["cause"] == "RERUN-CANNOT-SEE":
            remedy = "ANNOTATE + DO NOT RE-RUN"
            reason = ("its instrument walks refs, %d of the commits it names "
                      "hang off none, and the objects are still present -- the "
                      "committed bytes are the only reachable record of them. "
                      "A re-run writes 0 over a number that was real."
                      % len(r["unreach"]))
        elif r["reads_out"]:
            remedy = "ANNOTATE (unpinnable under R2)"
            reason = ("its producer's population is the repository, so no tree "
                      "digest can pin it and a re-run is stale at the next "
                      "commit anyone makes. What it needs is to SAY which "
                      "revision it is a fact about.")
        else:
            remedy = "RE-RUN AND RE-COMMIT"
            reason = ("its producer reads only its own tree, so the bytes it "
                      "emits at the carrying commit are a fact about that tree "
                      "and stay one.")
        r["remedy"] = remedy
        print("    %s" % r["path"])
        print("        cause  : %s" % r["cause"])
        print("        remedy : %s" % remedy)
        print("        because: %s" % reason)
        print("        names its own carrying commit in its bytes: %s"
              % ("YES" if names_own_rev else "no"))
        if r.get("armb") not in (None, "SKIPPED") and not str(
                r["armb"]).startswith("NONE"):
            print("        it is a fact about the tree at: %s"
                  % str(r["armb"])[:12])

    led.record(bool(rows) and all(r.get("remedy") for r in rows),
               "D1e every disposed transcript carries a named remedy with a "
               "stated reason: %d of %d" % (len([r for r in rows if
                                                 r.get("remedy")]), len(rows)))
    led.record(False,
               "D1e' NOTHING IN ANOTHER TICKET'S DIRECTORY IS EDITED BY THIS "
               "SCRIPT.  The remedies above are a DISPOSAL RECORD, not an edit: "
               "mg-1abe's rule is that a transcript which does not reproduce is "
               "a MEASUREMENT and overwriting it destroys it, and %d of the %d "
               "carry a remedy that forbids re-running outright"
               % (len(blind), len(rows)))

    return led.done()


if __name__ == "__main__":
    sys.exit(main())
