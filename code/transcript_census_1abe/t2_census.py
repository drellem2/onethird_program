"""t2 -- THE BLAST RADIUS.  Every committed transcript in the arc, re-run at
the commit that carries it, bucketed, with the denominator named.

This is the deliverable of mg-1abe.  Everything else in this directory is
consequence.

METHOD, and why it is this one.  The ticket says "re-run its producing script
AT THE COMMIT THAT CARRIES IT".  The producing script is not guessed from the
transcript's filename -- 222 of the 510 transcript names cannot be resolved to
a script that way, because this arc's runners spell their producers through
`for` loops, `run()` helpers, `${name%.py}` strips and `$(basename ...)`
substitutions.  Instead the suite's OWN `run_all.sh`, AS IT STOOD AT THE
CARRYING COMMIT, is executed in a detached worktree checked out at that commit,
and every transcript it writes is compared byte-for-byte against the committed
blob.  The instrument is therefore the arc's own reproduction procedure rather
than a second one written by me that agrees with it today.

BUCKETS.  Every transcript lands in exactly one, and they sum to the
denominator.  A census whose buckets do not sum to its population is not a
census.

  REPRODUCES        the runner rewrote the file and the bytes are identical.
  DIFFERS           the runner rewrote the file and the bytes are not.  THIS
                    IS CLASS 2 -- the bucket that corrupts the evidence base.
  NOT-REGENERATED   the runner ran but never wrote this file.  The transcript
                    is committed in a directory whose own runner no longer
                    produces it.
  NO-RUNNER         no `run_all.sh` in that directory at that commit.  Nothing
                    in the tree says how the file was made.
  RUNNER-FAILED     the runner could not start (non-zero before writing).
  TIMED-OUT         the runner exceeded the budget and this file was not
                    written before it did.  NEVER folded into DIFFERS: "I did
                    not finish measuring" and "it does not reproduce" are
                    different claims and only one of them is about the subject.
  SELF              this census's own transcripts.  Re-entering t2 from inside
                    t2 recurses; the bucket is named rather than dropped.

CONCLUSION, for the DIFFERS bucket only.  The ticket is right that displaced is
not the same as wrong.  HOLDS means every conclusion-bearing line of the
transcript is unchanged and only figures or prose around them moved -- true of
the tree it measured, in mg-b2af's sense.  FLIPS means a conclusion-bearing
line changed -- a false record, in mg-c3a2's sense.

DETERMINISM.  Every DIFFERS group is run a SECOND time at the same commit.  If
the two re-runs differ from each other, the producer is nondeterministic and
the transcript could never have reproduced, at any commit, for anyone.  That is
a cause the ticket does not name and it is separated out here.
"""

import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_1abe as L                                          # noqa: E402

# `--jobs` is NOT printed into the transcript and DEFAULTS TO 4 rather than to
# the core count.  Both choices are deliberate.  The job count is a fact about
# the machine, not about the subject, so printing it would make this
# transcript fail to reproduce on a differently-sized box for a reason that has
# nothing to do with the arc -- the exact defect being measured, committed by
# the instrument measuring it.  Four rather than eight because eight put this
# ten-core machine at a load average of 90 and starved the other agents on it.
DEFAULT_JOBS = 4
DEFAULT_TIMEOUT = 900


def arg(name, default, cast=str):
    if name in sys.argv:
        return cast(sys.argv[sys.argv.index(name) + 1])
    return default


class Pool(object):
    """K detached worktrees, created once and reused.  A worktree per job is
    the only way to run 152 different commits without serialising on one
    checkout, and `git worktree` shares the object store so the cost is a
    checkout rather than a clone."""

    def __init__(self, k):
        self.root = tempfile.mkdtemp(prefix="census1abe-")
        self.paths = []
        for i in range(k):
            p = os.path.join(self.root, "wt%d" % i)
            L.git("worktree", "add", "--detach", "-q", p, "main")
            self.paths.append(p)

    def close(self):
        for p in self.paths:
            L.git("worktree", "remove", "--force", p)
        shutil.rmtree(self.root, ignore_errors=True)
        L.git("worktree", "prune")


def run_suite(wt, commit, directory, timeout):
    """Check out `commit` in `wt` and run `directory`'s run_all.sh there.

    Returns (status, seconds).  status is 'ok', 'timeout', or 'failed:<rc>'.
    The runner's own stdout is discarded: the transcripts are the measurement,
    and this arc's runners redirect into them by design.
    """
    L.git("checkout", "--force", "--detach", "-q", commit, cwd=wt)
    L.git("clean", "-xdffq", cwd=wt)
    d = os.path.join(wt, directory)
    t0 = time.time()
    proc = subprocess.Popen(["sh", "run_all.sh"], cwd=d,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            start_new_session=True)
    try:
        rc = proc.wait(timeout=timeout)
        status = "ok" if rc == 0 else "failed:%d" % rc
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except OSError:
            pass
        proc.wait()
        status = "timeout"
    return status, time.time() - t0


def collect(wt, group):
    """{path: bytes-on-disk-or-None} for every transcript of a group."""
    out = {}
    for path in group:
        full = os.path.join(wt, path)
        if os.path.exists(full):
            with open(full, "rb") as fh:
                out[path] = fh.read()
        else:
            out[path] = None
    return out


def main():
    rev = L.main_rev()
    jobs = arg("--jobs", DEFAULT_JOBS, int)
    timeout = arg("--timeout", DEFAULT_TIMEOUT, int)
    only = arg("--dirs", None)
    head = L.resolve(rev)

    ledger = L.Ledger(
        "t2 -- THE BLAST RADIUS: every committed transcript re-run at the "
        "commit that carries it")
    print("""
POPULATION   every tracked file matching `code/<dir>/out_*.txt` at the revision
             named below.  GRAIN one verdict per transcript file.
REVISION     the figures in this transcript are facts about the commit printed
             as `as-of` and about NO OTHER.  `main` moves; this number does not
             move with it, and saying so is the whole subject of mg-1abe.
""")
    print("    as-of      %s  (%s)" % (head, rev))
    print("    budget     %d s per suite run" % timeout)

    population = L.transcripts(rev)
    groups = {}
    for p in population:
        c = L.carrying_commit(p, rev)
        groups.setdefault((p.split("/")[1], c), []).append(p)

    print("    population %d transcripts" % len(population))
    print("    groups     %d distinct (directory, carrying commit) pairs"
          % len(groups))

    committed = {p: L.blob_at(L.carrying_commit(p, rev), p) for p in population}

    verdict = {}
    detail = {}
    concl = {}          # path -> FLIPS / HELD-DRIFTED / HELD / NO-VERDICT
    nondet_set = set()
    work = []
    for (d, c), paths in sorted(groups.items()):
        if d == L.SELF_DIR:
            for p in paths:
                verdict[p] = "SELF"
                detail[p] = "this census's own transcript; not re-entered"
            continue
        if only and d not in only.split(","):
            for p in paths:
                verdict[p] = "SKIPPED"
                detail[p] = "--dirs filter"
            continue
        work.append((d, c, paths))

    pool = Pool(min(jobs, max(1, len(work))))
    lock = threading.Lock()
    cursor = [0]
    done = [0]

    def worker(wt):
        while True:
            with lock:
                if cursor[0] >= len(work):
                    return
                d, c, paths = work[cursor[0]]
                cursor[0] += 1
            directory = "code/" + d
            if L.blob_at(c, directory + "/run_all.sh") is None:
                with lock:
                    for p in paths:
                        verdict[p] = "NO-RUNNER"
                        detail[p] = "no run_all.sh in %s at %s" % (d, c[:7])
                    done[0] += 1
                continue
            status, secs = run_suite(wt, c, directory, timeout)
            got = collect(wt, paths)
            differs = [p for p in paths
                       if got[p] is not None and got[p] != committed[p]]
            second = {}
            if differs:
                # DETERMINISM CONTROL: the same suite, the same commit, twice.
                st2, _ = run_suite(wt, c, directory, timeout)
                if st2 != "timeout":
                    second = collect(wt, paths)
            with lock:
                for p in paths:
                    if got[p] is None:
                        if status == "timeout":
                            verdict[p] = "TIMED-OUT"
                            detail[p] = "suite exceeded %ds" % timeout
                        elif status.startswith("failed"):
                            verdict[p] = "RUNNER-FAILED"
                            detail[p] = "run_all.sh exited %s and never " \
                                        "wrote this file" % status.split(":")[1]
                        else:
                            verdict[p] = "NOT-REGENERATED"
                            detail[p] = "run_all.sh ran to completion and " \
                                        "never wrote this file"
                    elif got[p] == committed[p]:
                        verdict[p] = "REPRODUCES"
                        detail[p] = "%.0fs" % secs
                    else:
                        verdict[p] = "DIFFERS"
                        nd = ""
                        if p in second and second[p] is not None \
                                and second[p] != got[p]:
                            nondet_set.add(p)
                            nd = "; NONDETERMINISTIC (two re-runs at the same " \
                                 "commit differ from each other)"
                        concl[p] = L.conclusion_verdict(
                            committed[p].decode("utf-8", "replace"),
                            got[p].decode("utf-8", "replace"))
                        detail[p] = "conclusion %s%s" % (concl[p], nd)
                done[0] += 1
                sys.stderr.write("\r  %d/%d groups" % (done[0], len(work)))
                sys.stderr.flush()

    threads = [threading.Thread(target=worker, args=(p,)) for p in pool.paths]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    sys.stderr.write("\n")
    pool.close()

    # --------------------------------------------------------------- report
    ledger.head("T2a -- EVERY TRANSCRIPT, ONE ROW EACH, NOTHING TRUNCATED")
    print("""
All %d rows are printed.  A cap here would be the exact defect this arc keeps
finding: a list shortened under a sentence that says `every`.  `carry` is the
transcript's carrying commit; `producer` is the script the suite's runner
spells for it, or `?` where the runner's own spelling cannot be resolved to one
script -- an unresolved producer is a labelling gap, NOT a verdict.
""" % len(population))
    print("    %-52s %-8s %-16s %-15s %s"
          % ("transcript", "carry", "verdict", "producer", "detail"))
    for p in population:
        c = L.carrying_commit(p, rev)
        spec, _ = L.producer_for(p, c)
        print("    %-52s %-8s %-16s %-15s %s"
              % (p[len("code/"):][:52], c[:7], verdict.get(p, "?"),
                 (spec or {}).get("script", "?")[:15], detail.get(p, "")))

    ledger.head("T2b -- THE COUNTS, WITH THE DENOMINATOR NAMED")
    order = ["REPRODUCES", "DIFFERS", "NOT-REGENERATED", "NO-RUNNER",
             "RUNNER-FAILED", "TIMED-OUT", "SELF", "SKIPPED"]
    counts = {k: sum(1 for p in population if verdict.get(p) == k)
              for k in order}
    for k in order:
        print("    %-18s %4d  of %d" % (k, counts[k], len(population)))
    total = sum(counts.values())
    ledger.record(total == len(population),
                  "T2b the buckets sum to %d against a population of %d"
                  % (total, len(population)))

    attempted = counts["REPRODUCES"] + counts["DIFFERS"]
    ledger.record(None,
                  "T2b' of the %d transcripts ACTUALLY RE-RUN TO COMPLETION, "
                  "%d reproduce and %d do not.  The other %d were not measured "
                  "against their bytes at all and are reported in their own "
                  "buckets rather than as reproductions"
                  % (attempted, counts["REPRODUCES"], counts["DIFFERS"],
                     len(population) - attempted))

    ledger.head("T2c -- CLASS 2: DISPLACED IS NOT THE SAME AS WRONG")
    print("""
The ticket's step 2, and it needs three answers rather than two.  A DECISION is
a `[TAG]` or one of the arc's three totals; the sentence after a tag routinely
carries a count, and a count that moved while the decision stood is not the
same defect as a decision that changed.
""")

    def bucket(name):
        return [p for p in population if concl.get(p) == name]

    holds, drifted = bucket("HELD"), bucket("HELD-DRIFTED")
    flips, none_ = bucket("FLIPS"), bucket("NO-VERDICT")
    nondet = [p for p in population if p in nondet_set]
    print("    of the %d DIFFERS:" % counts["DIFFERS"])
    print("      FLIPS         %4d   a decision changed: a FALSE RECORD at its "
          "carrying commit (mg-c3a2's class)" % len(flips))
    print("      HELD-DRIFTED  %4d   every decision stands, a FIGURE INSIDE "
          "one of them moved" % len(drifted))
    print("      HELD          %4d   decisions and their figures intact; only "
          "surrounding rows moved (mg-b2af's class)" % len(holds))
    print("      NO-VERDICT    %4d   states no conclusion this instrument "
          "reads" % len(none_))
    print()
    print("    every FLIPS, named:")
    for p in flips:
        print("      %s" % p)
    if not flips:
        print("      (none)")
    print()
    print("    every NONDETERMINISTIC producer, named "
          "(two re-runs at the SAME commit disagree):")
    for p in nondet:
        print("      %s" % p)
    if not nondet:
        print("      (none)")

    ledger.record(not flips,
                  "T2c %d of %d committed transcripts are FALSE RECORDS at "
                  "their carrying commit: re-run there, a DECISION changes.  "
                  "This is the count that matters, because a reader of one of "
                  "these cannot tell a real run elsewhere from a run against "
                  "different content"
                  % (len(flips), len(population)))
    ledger.record(not drifted,
                  "T2c-ii and a further %d transcripts keep every decision "
                  "while a FIGURE INSIDE a decision moves.  These are not "
                  "false verdicts and they ARE false numbers, which is why "
                  "they are counted apart from both other buckets"
                  % len(drifted))
    ledger.record(counts["DIFFERS"] == 0,
                  "T2c' CLASS 2 is %d of %d transcripts (%.0f%% of the "
                  "population, %.0f%% of those re-run to completion)"
                  % (counts["DIFFERS"], len(population),
                     100.0 * counts["DIFFERS"] / len(population),
                     100.0 * counts["DIFFERS"] / attempted if attempted else 0))
    ledger.record(not nondet,
                  "T2c'' %d transcripts have a NONDETERMINISTIC producer and "
                  "could never have reproduced at any commit, for anyone.  "
                  "Neither rebase nor regeneration explains these"
                  % len(nondet))

    ledger.head("T2e -- CAUSE: WHERE THE TICKET'S FRAMING NEEDS CORRECTING")
    print("""
The ticket names two mechanisms -- the refinery's REBASE, and REGENERATION
(mg-bf79's "a publisher is not a pin") -- and asks for others if there are any.
There is a third and this census expects it to be the largest: A PRODUCER THAT
READS REPOSITORY-GLOBAL STATE.  Such a transcript is displaced by the NEXT
commit anyone makes, on any branch, with no rebase and no regeneration
anywhere near it.  Nothing was done to it; the repository moved underneath it.

The split below is STATIC and it is a proxy, stated as one: a producing
directory counts as a REPO-READER if any `.py`/`.sh` in it, at the carrying
commit, invokes git.  It does not prove that the git call is what moved -- it
establishes which transcripts CAN be moved that way and which cannot.
""")
    git_call = re.compile(
        rb"""['"]git['"]|\bgit\s+(log|rev-list|rev-parse|ls-tree|show|"""
        rb"""cat-file|merge-base|diff|ls-files|describe)\b""")

    def reads_repo(directory, commit):
        for line in L.git("ls-tree", "-r", "--name-only",
                          "%s:%s" % (commit, directory)).split("\n"):
            if line.endswith(L.CODE_SUFFIXES):
                blob = L.blob_at(commit, "%s/%s" % (directory, line))
                if blob and git_call.search(blob):
                    return True
        return False

    cache = {}
    reader, pure = [], []
    for p in population:
        if verdict.get(p) != "DIFFERS":
            continue
        c = L.carrying_commit(p, rev)
        key = (os.path.dirname(p), c)
        if key not in cache:
            cache[key] = reads_repo(key[0], key[1])
        (reader if cache[key] else pure).append(p)
    tot = len(reader) + len(pure)
    print("    of the %d DIFFERS:" % tot)
    print("      producer READS THE REPOSITORY  %4d  (%.0f%%)"
          % (len(reader), 100.0 * len(reader) / tot if tot else 0))
    print("      producer does not              %4d  (%.0f%%)"
          % (len(pure), 100.0 * len(pure) / tot if tot else 0))
    print()
    print("    every DIFFERS whose producer NEVER TOUCHES GIT -- these cannot "
          "be explained by rebase, by regeneration, or by the repository "
          "moving, and are the ones worth reading one at a time:")
    for p in pure:
        print("      %-56s %s" % (p[len("code/"):][:56], detail[p][:70]))
    if not pure:
        print("      (none)")

    ledger.record(None,
                  "T2e %d of %d non-reproducing transcripts have a producer "
                  "that reads repository-global state and %d do not.  If the "
                  "first number dominates, the ticket's two mechanisms are "
                  "not the main cause of the blast radius -- the repository "
                  "moving is, and no rebase policy addresses that"
                  % (len(reader), tot, len(pure)))

    ledger.head("T2d -- WHAT THIS ROW DOES NOT MEASURE")
    print("""
TIMED-OUT is a budget, not a verdict.  A suite that needs longer than the
budget has not been shown to fail; it has not been measured.  Re-run with
`--timeout N` to move the line and the bucket will move with it.

AND THAT MAKES THIS TRANSCRIPT MACHINE-DEPENDENT, WHICH IS DISCLOSED HERE
RATHER THAN DISCOVERED LATER.  A slower box, or a busier one, pushes suites
over the same budget and moves rows out of REPRODUCES/DIFFERS into TIMED-OUT.
`--jobs` is deliberately not printed above -- it is a fact about the machine
and not about the arc -- but it changes how much wall clock each suite gets in
contention, so it can move the same rows.  Every other bucket in this census is
a fact about the repository; TIMED-OUT is a fact about the repository AND the
machine, and the two should not be read the same way.

NOT-REGENERATED is not a defect by itself.  Some of this arc's transcripts are
deliberately kept artefacts -- a FIRSTFORM run, a PRE-repair capture -- that
their own runner is not meant to rewrite.  What it does mean is that NOTHING IN
THE TREE regenerates that file, so no control can ever check it.

SELF is %d rows.  This census does not re-enter itself, and the honest
consequence is that mg-1abe's own transcripts are the only ones in this table
whose reproduction is asserted rather than measured.
""" % counts["SELF"])

    return ledger.done()


if __name__ == "__main__":
    sys.exit(main())
