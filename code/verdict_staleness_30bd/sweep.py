#!/usr/bin/env python3
"""mg-30bd — THE SWEEP.  Regenerate every regenerable transcript at HEAD and record what moved.

THIS IS NOT IN `run_all.sh` AND IT IS NOT A FIXED POINT.  It executes instrument code across
the whole corpus, takes hours, and its answers change as the corpus moves — which is the very
property being measured.  `out_sweep_30bd.txt` and `sweep_30bd.jsonl` record ONE DATED RUN,
exactly as `code/asof_census_20ee/out_ground_truth.txt` does, and `report.py` (which IS in
`run_all.sh`) is a pure function of that frozen record.

WHY A CLONE PER WORKER AND NOT `git checkout` IN PLACE, which is what mg-20ee's
`ground_truth.sh` does.  Three reasons, in increasing order of how much they cost when
ignored:

  1. `ground_truth.sh` restores only `$d`, so a suite that writes OUTSIDE its own directory
     leaks into the next suite's measurement.  Several do.
  2. These suites MUTATE THE WORKTREE THEY RUN IN (mg-6cb9's own README says so in
     capitals) and some of them exit non-zero half way.  In a clone the damage is bounded by
     a directory nobody else is reading.
  3. It is the only way to run more than one at a time, and sequential is ~5 hours.

THE SANDBOX HAS TO BE FAITHFUL AND THE FIRST ONE WAS NOT — measured, not feared.  A plain
`git clone` of a polecat worktree has NO LOCAL `main` BRANCH, only `origin/main`.  Run under
that sandbox the gate came back RED at HEAD with
`ancestor of main : (no such ref in this checkout)`, and a second transcript went with it
because it carries the first one's byte count.  Two DISAGREES, both of them the sandbox
talking about itself.  `git branch main origin/main` in every clone, and the same gate at the
same commit is GREEN, exit 0.  That measurement is the fidelity control and it is quoted in
README §4.

Usage:
    python3 -B sweep.py --workers 6 --timeout 900 [--only DIR ...] [--pass2]
"""

import argparse
import json
import os
import queue
import re
import shutil
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import lib30bd as L                                                # noqa: E402

RECORD = os.path.join(HERE, "sweep_30bd.jsonl")


def git(root, *args, **kw):
    return subprocess.run(("git", "-C", root) + args, capture_output=True, text=True, **kw)


def tracked_transcripts(root):
    p = git(root, "ls-files", "code")
    return sorted(r for r in p.stdout.splitlines() if L.lib_f771.is_transcript(r))


def candidate_dirs(root):
    """A directory under code/ with a run_all.sh AND at least one tracked transcript."""
    runners = {os.path.dirname(r) for r in git(root, "ls-files", "code").stdout.splitlines()
               if os.path.basename(r) == "run_all.sh"}
    owners = {os.path.dirname(r) for r in tracked_transcripts(root)}
    return sorted(runners & owners)


# `python3 -B a1_bothways.py > out_a1_bothways.txt` and friends: the producing command for
# one transcript, as written in the runner itself.  Used ONLY by pass 2, and deliberately
# narrow — a producer this regex cannot see is REPORTED as unparsed, never guessed at.
PRODUCER = re.compile(r"^\s*(?P<cmd>[^|;&#]*?)\s*>\s*(?P<out>out_[\w.-]+\.txt)\s*(?:\|\||$|&&)")


def producers(runner_path):
    out = {}
    try:
        text = open(runner_path, encoding="utf-8", errors="replace").read()
    except OSError:
        return out
    for line in text.split("\n"):
        m = PRODUCER.match(line)
        if m and not m.group("cmd").lstrip().startswith(("#", "echo", "cat", ":")):
            out.setdefault(m.group("out"), m.group("cmd").strip())
    return out


class Worker(object):
    def __init__(self, idx, base, head):
        self.dir = os.path.join(base, "w%d" % idx)
        self.head = head
        if os.path.isdir(self.dir):
            shutil.rmtree(self.dir)
        subprocess.run(["git", "clone", "--quiet", "--local", "--shared", ROOT, self.dir],
                       check=True, capture_output=True)
        # THE FIDELITY REQUIREMENT.  See the module docstring: without this the sandbox
        # answers a question about `main` with "no such ref" and two transcripts move.
        git(self.dir, "branch", "main", "origin/main")
        self.restore()

    def restore(self):
        git(self.dir, "reset", "--hard", "--quiet", self.head)
        git(self.dir, "clean", "-fdxq")

    def run(self, cmd, cwd, timeout):
        t0 = time.time()
        env = dict(os.environ)
        env.pop("BUILD_SH_RAN_THE_SUITES", None)
        try:
            p = subprocess.run(cmd, shell=True, cwd=cwd, env=env, timeout=timeout,
                               capture_output=True, text=True)
            rc, timed = p.returncode, False
        except subprocess.TimeoutExpired:
            rc, timed = None, True
        return rc, timed, round(time.time() - t0, 1)


def measure(worker, relpaths, before_mtimes, committed):
    """Classify every tracked transcript in the clone against its committed copy."""
    rows = []
    for rel in relpaths:
        path = os.path.join(worker.dir, rel)
        try:
            mt = os.path.getmtime(path)
        except OSError:
            mt = None
        rewritten = (mt is not None and before_mtimes.get(rel) != mt)
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                now = fh.read()
        except OSError:
            now = None
        if now is None:
            rows.append({"path": rel, "rewritten": rewritten, "bucket": "GONE", "detail":
                         "the run removed this tracked transcript"})
            continue
        if not rewritten:
            continue
        bucket, detail = L.classify(committed[rel], now)
        row = {"path": rel, "rewritten": True, "bucket": bucket, "detail": detail}
        if bucket in L.VERDICT_STALE:
            hunk, dropped = L.verdict_line_diff(committed[rel], now)
            row["hunk"] = hunk
            row["dropped"] = dropped
        rows.append(row)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--base", default=os.environ.get("SWEEP_BASE", "/tmp/mg30bd"))
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--fresh", action="store_true",
                    help="TRUNCATE the record and start a new sweep.  Without it the run is "
                         "APPENDED, and report.py takes the last record per directory — "
                         "which is how one suite is re-measured without losing the rest.")
    ap.add_argument("--pass2-cap", type=int, default=12,
                    help="most transcripts to regenerate individually per directory")
    ap.add_argument("--pass2-timeout", type=int, default=300)
    ap.add_argument("--pass2", action="store_true",
                    help="also try each transcript pass 1 did not rewrite, via the "
                         "producing command written in its own runner")
    args = ap.parse_args()

    head = git(ROOT, "rev-parse", "HEAD").stdout.strip()
    relpaths = tracked_transcripts(ROOT)
    committed = {}
    for rel in relpaths:
        committed[rel] = git(ROOT, "show", "%s:%s" % (head, rel)).stdout
    dirs = args.only or candidate_dirs(ROOT)

    # THE DECLARATION CENSUS (mg-5491), AND IT IS OVER THE WHOLE TREE EVEN UNDER `--only`.
    # `report.py` may not read the worktree — 649b186 removed exactly that from it, in this
    # directory, because a live-tree read makes a committed report drift away from the tree
    # it describes.  So the census is taken HERE, where the committed blobs are already in
    # hand, and travels in the record.  It is deliberately NOT per-directory: a `--only`
    # re-measurement of one suite still refreshes the whole census, so the newest record
    # always carries a COMPLETE list of who has declared rather than a fragment of one.
    declared = {}
    for rel in relpaths:
        d = L.declaration(committed[rel])
        if d is not None:
            declared[rel] = d

    os.makedirs(args.base, exist_ok=True)
    print("mg-30bd sweep: %d candidate dir(s), %d tracked transcript(s), head %s"
          % (len(dirs), len(relpaths), head[:7]), flush=True)

    workers = queue.Queue()
    for i in range(args.workers):
        workers.put(Worker(i, args.base, head))
    print("mg-30bd sweep: %d worker clone(s) ready under %s" % (args.workers, args.base),
          flush=True)

    lock = threading.Lock()
    # APPEND, NOT TRUNCATE, AND THIS LINE COST A TWO-HOUR SWEEP.  It was `open(RECORD, "w")`,
    # and re-measuring ONE directory with `--only` — which is exactly what the report's
    # last-record-per-directory rule exists to support — deleted the 187-suite record it was
    # meant to correct.  A harness whose repair operation destroys the thing being repaired
    # is the shape this whole estate keeps finding; here it is in the instrument that counts
    # it.  `--fresh` is the explicit way to start a new record, and it is now the only way.
    fh = open(RECORD, "w" if args.fresh else "a", encoding="utf-8")
    fh.write(json.dumps({"kind": "header", "head": head, "dirs": len(dirs),
                         "transcripts": len(relpaths), "timeout": args.timeout,
                         "pass2": bool(args.pass2), "tokens": list(L.TOKENS),
                         "declared": declared}) + "\n")
    done = [0]

    def job(d):
        w = workers.get()
        try:
            w.restore()
            before = {}
            for rel in relpaths:
                try:
                    before[rel] = os.path.getmtime(os.path.join(w.dir, rel))
                except OSError:
                    before[rel] = None
            rc, timed, secs = w.run("sh %s/run_all.sh" % d, w.dir, args.timeout)
            rows = measure(w, relpaths, before, committed)
            rec = {"kind": "suite", "dir": d, "rc": rc, "timeout": timed, "secs": secs,
                   "rows": rows,
                   "owned": [r for r in relpaths if os.path.dirname(r) == d],
                   "rewritten": sorted(r["path"] for r in rows if r["rewritten"])}
            if args.pass2:
                rec["pass2"], rec["pass2_capped"] = pass2(
                    w, d, relpaths, committed, min(args.timeout, args.pass2_timeout),
                    set(rec["rewritten"]), args.pass2_cap)
            w.restore()
        finally:
            workers.put(w)
        with lock:
            fh.write(json.dumps(rec) + "\n")
            fh.flush()
            done[0] += 1
            print("[%3d/%3d] %-52s rc=%-4s %6.1fs  %d moved"
                  % (done[0], len(dirs), d, "T/O" if timed else rc, secs,
                     len(rec["rewritten"])), flush=True)

    pending = queue.Queue()
    for d in dirs:
        pending.put(d)

    def drain():
        while True:
            try:
                d = pending.get_nowait()
            except queue.Empty:
                return
            try:
                job(d)
            except Exception as exc:                     # a broken suite is data, not a stop
                with lock:
                    fh.write(json.dumps({"kind": "suite", "dir": d, "error": repr(exc)}) + "\n")
                    fh.flush()

    threads = [threading.Thread(target=drain) for _ in range(args.workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    fh.close()
    print("mg-30bd sweep: done", flush=True)


def pass2(w, d, relpaths, committed, timeout, already, cap):
    """THE RUNNER-BLIND PASS, and it exists because of mg-6cb9 specifically.

    `code/species_extent_audit_6cb9/run_all.sh` gates its three audit scripts behind a
    selftest and `exit 1`s when the selftest fails.  It fails at HEAD today.  So a sweep that
    only runs runners NEVER REGENERATES `out_a1_bothways.txt` — the one transcript in this
    corpus whose verdict move is already known — and would report the motivating instance as
    a two-line selftest wobble.  An enumeration's blind spot is not a footnote when the thing
    it cannot see is the reason the enumeration was commissioned.

    So: for every tracked transcript in `d` that pass 1 did not rewrite, look for its
    producing command in the runner's own text and run THAT, alone.  A producer the regex
    cannot see is recorded as `unparsed` and is NOT guessed at.
    """
    out = []
    capped = []
    prod = producers(os.path.join(w.dir, d, "run_all.sh"))
    ran = 0
    for rel in relpaths:
        if os.path.dirname(rel) != d or rel in already:
            continue
        name = os.path.basename(rel)
        cmd = prod.get(name)
        if not cmd:
            out.append({"path": rel, "status": "unparsed"})
            continue
        if ran >= cap:
            # NO SILENT CAPS.  What was dropped is named, because a truncation nobody
            # states reads as "that was all of it".
            capped.append(rel)
            out.append({"path": rel, "status": "capped", "cmd": cmd})
            continue
        ran += 1
        w.restore()
        rc, timed, secs = w.run("%s > %s" % (cmd, name), os.path.join(w.dir, d), timeout)
        try:
            with open(os.path.join(w.dir, rel), encoding="utf-8", errors="replace") as fh:
                now = fh.read()
        except OSError:
            out.append({"path": rel, "status": "no-output", "cmd": cmd})
            continue
        bucket, detail = L.classify(committed[rel], now)
        row = {"path": rel, "status": "ran", "cmd": cmd, "rc": rc, "timeout": timed,
               "secs": secs, "bucket": bucket, "detail": detail}
        if bucket in L.VERDICT_STALE:
            row["hunk"], row["dropped"] = L.verdict_line_diff(committed[rel], now)
        out.append(row)
    w.restore()
    return out, capped


if __name__ == "__main__":
    main()
