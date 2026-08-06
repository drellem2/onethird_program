"""mg-18dc -- shared machinery for the INDEPENDENT AUDIT of the runner-idiom sweep.

THREE THINGS THIS LIBRARY REFUSES TO DO, because they are how the parents got
their numbers and repeating them can only reproduce their answers:

  * it does not match a REGEX against runner text  (mg-03d1's rule)
  * it does not PARSE the shell                     (mg-ec63's rule)
  * it does not run anything inside the repository  (both of them did)

Instead it EXECUTES each `run_all.sh` in a DISPOSABLE CLONE with `python3`
replaced by a stub that writes a fixed marker and records, at the instant it is
invoked, the size of every `out_*.txt` in its directory.  The redirection is
then observed rather than inferred, and the observation is at the grain the
defect actually has: not `does this runner use >` but `IS THIS FILE EMPTY AT THE
MOMENT THIS PROBE STARTS`.

The clone is why this audit can run the arc's probes at all.  mg-ec63 ran them
in the tree and one of them emptied its own transcript (SD6f).  Nothing here
touches the worktree: `sandbox()` clones once into $TMPDIR and every probe,
every truncation and every leftover `.new` happens there.
"""

import json
import os
import re
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MINE = "code/idiom_sweep_audit_18dc"

# Where transcripts, ledgers and clones live.  OUTSIDE THE REPOSITORY, for the
# reason mg-ec63 landed structurally in c1bb466: an artifact inside the tree is
# an artifact the arc's own probes can destroy.
WORK = os.environ.get("V18_WORK") or os.path.join(
    os.environ.get("TMPDIR", "/tmp"), "mg18dc-work")

MARKER = "MG18DC-STUB-OUTPUT\n"


# ---------------------------------------------------------------------------
# git, always against the worktree and always read-only

def git(*a, repo=None):
    return subprocess.run(["git"] + list(a), cwd=repo or REPO,
                          capture_output=True, text=True).stdout


def head():
    return git("rev-parse", "--short", "HEAD").strip()


def runners_at(rev, repo=None):
    """The population, as a PROPERTY OF A COMMIT rather than of a disk.

    mg-03d1 and mg-ec63 both globbed the working directory.  A glob counts
    untracked files, so their totals are not reproducible from any commit --
    which is D1/P2a of this audit's predictions.  `git ls-tree` is.
    """
    out = git("ls-tree", "-r", "--name-only", rev, "--", "code/", repo=repo)
    return sorted(p.rsplit("/", 1)[0] for p in out.splitlines()
                  if p.count("/") == 2 and p.endswith("/run_all.sh"))


# ---------------------------------------------------------------------------
# the disposable clone

def sandbox(rev, tag=None):
    """A clone of the repo at `rev`, outside the repository, reused if present.

    Read-only against the source: `git clone --no-hardlinks` copies the object
    store rather than linking into it, so nothing that happens in the sandbox
    can reach the worktree's git.
    """
    tag = tag or rev
    d = os.path.join(WORK, "sbx-%s" % tag)
    stamp = os.path.join(d, ".v18-rev")
    if os.path.isdir(d) and os.path.exists(stamp):
        if open(stamp).read().strip() == rev:
            return d
        shutil.rmtree(d)
    elif os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(WORK, exist_ok=True)
    subprocess.run(["git", "clone", "--no-hardlinks", "--quiet", REPO, d],
                   check=True, capture_output=True)
    subprocess.run(["git", "checkout", "--quiet", "--detach", rev], cwd=d,
                   check=True, capture_output=True)
    open(stamp, "w").write(rev + "\n")
    return d


def sandbox_reset(sbx, tree=None):
    """Back to the committed bytes, and BY CONTENT rather than by status.

    mg-03d1's A4d asserted its restore with `git status --porcelain`.  This
    returns the list of paths whose blob hash differs from the commit, which is
    the check the brief asks for -- hashes, not status -- and it is scoped to
    the WHOLE tree, not to the directory that was run (P7).
    """
    args = ["git", "checkout", "--quiet", "--", "."] if tree is None else \
           ["git", "checkout", "--quiet", "--", tree]
    subprocess.run(args, cwd=sbx, capture_output=True)
    subprocess.run(["git", "clean", "-qfd"], cwd=sbx, capture_output=True)
    return dirty(sbx)


def dirty(sbx):
    """Paths differing from HEAD by CONTENT (hash), plus untracked paths."""
    out = subprocess.run(["git", "status", "--porcelain", "-uall"], cwd=sbx,
                         capture_output=True, text=True).stdout
    return sorted(l[3:] for l in out.splitlines() if l.strip())


# ---------------------------------------------------------------------------
# the stub: python3 that writes a marker and records what it can see

STUB = r'''#!/usr/bin/env %s
import json, os, sys, time
led = os.environ["V18_LEDGER"]
cwd = os.getcwd()
snap = {}
try:
    for f in os.listdir(cwd):
        if f.startswith("out_") and f.endswith(".txt"):
            snap[f] = os.path.getsize(os.path.join(cwd, f))
except OSError:
    pass
with open(led, "a") as fh:
    fh.write(json.dumps({"argv": sys.argv[1:], "cwd": cwd, "snap": snap,
                         "pid": os.getpid(), "ppid": os.getppid(),
                         "t": time.time()}) + "\n")
sys.stdout.write(%r)
sys.exit(0)
'''


def make_stub(dirpath, real_python):
    """A `python3` (and `python`) on PATH that writes MARKER and records.

    It writes SOMETHING rather than nothing on purpose.  A stub that wrote
    nothing would leave every transcript at zero bytes and make the `.new`+`mv`
    runners indistinguishable from the `>` ones -- the exact collapse this
    audit exists to avoid.
    """
    os.makedirs(dirpath, exist_ok=True)
    src = STUB % (real_python, MARKER)
    for name in ("python3", "python"):
        p = os.path.join(dirpath, name)
        open(p, "w").write(src)
        os.chmod(p, 0o755)
    return dirpath


def child_work(tree):
    """A throwaway $V18_WORK for anything this suite EXECUTES.

    SD12 of this instrument, and it is this ticket's own defect committed by
    the audit sent to find it.  `run_all.sh` exports `V18_WORK`; the arc's
    runners inherit the whole environment; `code/idiom_sweep_audit_18dc` is a
    `code/*/run_all.sh` the moment this directory has a runner, so V6's sweep
    of HEAD RAN MY OWN RUNNER, which wrote `$V18_WORK/out_v4_outcomes.txt` --
    the file V4 was writing at that moment.  What was left was a 19-byte
    transcript containing the stub's marker and nothing else.

    THE RE-ENTRANCY GUARD DID NOT FIRE, and that is the finding rather than the
    accident: `V18_RUNNING` is set by `run_all.sh`, and the collision came from
    a probe invoked DIRECTLY.  A guard on the runner does not protect a probe.

    Repaired the way mg-ec63 repaired its own (c1bb466): structurally, by
    moving the artifact out of the collision path rather than by adding a
    second guard.  Everything this suite executes gets its own `V18_WORK`,
    under `$WORK/child/`, which no probe of mine ever writes a transcript to.
    """
    d = os.path.join(WORK, "child", tree.replace("/", "_"))
    os.makedirs(d, exist_ok=True)
    return d


def stub_run(sbx, tree, timeout=120):
    """Run one runner with python3 stubbed.  Returns the ledger of invocations.

    Every entry is one `python3` invocation, in order, carrying the SIZE OF
    EVERY out_*.txt IN ITS DIRECTORY AT THE INSTANT IT STARTED.  That snapshot
    is the whole measurement: `emptied` is a fact about a moment, not about a
    line of shell.
    """
    d = os.path.join(sbx, tree)
    if not os.path.isdir(d):
        return None, "no such tree"
    led = os.path.join(WORK, "ledger-%s.jsonl" % tree.replace("/", "_"))
    if os.path.exists(led):
        os.remove(led)
    stubdir = make_stub(os.path.join(WORK, "stub"), sys.executable)
    env = dict(os.environ)
    env["PATH"] = stubdir + os.pathsep + env.get("PATH", "")
    env["V18_LEDGER"] = led
    env.pop("PYTHONPATH", None)
    env["V18_WORK"] = child_work(tree)
    committed = {}
    for f in os.listdir(d):
        if f.startswith("out_") and f.endswith(".txt"):
            committed[f] = os.path.getsize(os.path.join(d, f))
    err = None
    try:
        subprocess.run(["sh", "./run_all.sh"], cwd=d, env=env, timeout=timeout,
                       capture_output=True)
    except subprocess.TimeoutExpired:
        err = "TIMEOUT"
    except Exception as e:                                    # noqa: BLE001
        err = type(e).__name__
    rows = []
    if os.path.exists(led):
        for line in open(led):
            try:
                rows.append(json.loads(line))
            except ValueError:
                pass
    return {"committed": committed, "rows": rows, "err": err}, None


def emptied_steps(res):
    """Steps whose OWN transcript is empty at the instant the probe starts.

    A step is (probe, out) where `out` is the transcript that step writes.  We
    do not know which out a step writes without parsing -- so we do not claim
    to.  We report, per invocation, EVERY out_*.txt that is zero bytes at that
    moment and was NON-ZERO IN THE COMMITTED TREE.  That set is empty for a
    `.new`+`mv` runner and non-empty for a `>` one, which is the distinction
    the parents drew by reading source.
    """
    if not res:
        return []
    out = []
    for i, r in enumerate(res["rows"]):
        zero = sorted(f for f, n in r["snap"].items()
                      if n == 0 and res["committed"].get(f, 0) > 0)
        if zero:
            out.append({"i": i, "argv": r["argv"], "zero": zero})
    return out


# ---------------------------------------------------------------------------
# source classification, WITH THE COMMENTS TAKEN OUT

def code_of(src):
    """`run_all.sh` with its comment lines removed.

    SD9/SD11 of this instrument: the arc's single most repeated runner line is
    a COMMENT saying `set -o pipefail` is not used, and several runners carry a
    comment explaining why they do or do not need `.new`+`mv`.  A rule that
    matches the file matches those sentences and calls them code -- it turned a
    2 into a 31 once and a 2 into a 4 once.  Every rule of MINE that reads
    runner source goes through here.  (Rules I am REPRODUCING from mg-03d1 do
    not: to re-derive its 86 and its 43 I must apply its rule as written,
    comments included, and I do.)
    """
    return "\n".join(ln for ln in src.splitlines()
                      if not ln.lstrip().startswith("#"))


def carries_newmv(src):
    """The `.new`+`mv` structural fix, in CODE rather than in prose."""
    c = code_of(src)
    return re.search(r"\.new", c) is not None and re.search(r"\bmv\b", c) is not None


# ---------------------------------------------------------------------------
# the read shim: what the process OPENS, and HOW BIG THE FILE WAS AT THAT MOMENT

SHIM = r'''import os, sys
_led = os.environ.get("V18_READS")
if _led:
    _pid = os.getpid()

    def _hook(event, args):
        # `open` fires before the file object exists, so the size recorded here
        # is the size AS THE PROBE SEES IT.  That single number is the whole
        # defect: a read of a file the same run has already emptied is
        # size==0 at mode 'r', observed rather than inferred from a `>`.
        if event != "open":
            return
        try:
            p, mode = args[0], args[1]
        except Exception:
            return
        if not mode or not isinstance(p, (str, bytes)):
            return
        try:
            s = p if isinstance(p, str) else p.decode("utf8", "replace")
            if "out_" not in s:
                return
            ap = os.path.abspath(s)
            sz = os.path.getsize(ap) if os.path.exists(ap) else -1
            with open(_led, "a") as fh:
                fh.write("%d\t%s\t%d\t%s\n" % (_pid, mode, sz, ap))
        except Exception:
            pass

    sys.addaudithook(_hook)
'''


def make_shim():
    d = os.path.join(WORK, "shim")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "sitecustomize.py"), "w").write(SHIM)
    return d


def real_run(sbx, tree, timeout=300):
    """Run one runner FOR REAL under the read shim, in the disposable clone.

    Returns every `out_`-ish open the run performed, with pid, mode and the
    size the opener saw.  The pid is carried because mg-ec63 found (SD6d) that
    this arc's probes run each other as subprocesses and a child's read was
    being attributed to its parent.
    """
    d = os.path.join(sbx, tree)
    if not os.path.isdir(d):
        return None
    led = os.path.join(WORK, "reads-%s.tsv" % tree.replace("/", "_"))
    if os.path.exists(led):
        os.remove(led)
    env = dict(os.environ)
    env["PYTHONPATH"] = make_shim()
    env["V18_READS"] = led
    env["V18_WORK"] = child_work(tree)          # SD12 -- see child_work()
    rec = {"tree": tree, "timeout": False, "exit": None, "opens": []}
    try:
        r = subprocess.run(["sh", "./run_all.sh"], cwd=d, capture_output=True,
                           env=env, timeout=timeout)
        rec["exit"] = r.returncode
    except subprocess.TimeoutExpired:
        rec["timeout"] = True
    if os.path.exists(led):
        for line in open(led):
            parts = line.rstrip("\n").split("\t", 3)
            if len(parts) == 4:
                rec["opens"].append({"pid": int(parts[0]), "mode": parts[1],
                                     "size": int(parts[2]), "path": parts[3]})
    return rec


def own_empty_reads(rec, sbx, tree):
    """Opens for READ, of an `out_*.txt` OF THIS TREE, that were ZERO bytes.

    Three conditions, each of which the parents inferred and this observes:
    the mode is a reading mode, the path is inside the tree being run, and the
    file had no bytes when it was opened.
    """
    root = os.path.realpath(os.path.join(sbx, tree))
    hits = []
    for o in rec["opens"] if rec else []:
        if "r" not in o["mode"] or "+" in o["mode"]:
            continue
        ap = os.path.realpath(o["path"])
        base = os.path.basename(ap)
        if os.path.dirname(ap) != root:
            continue
        if not (base.startswith("out_") and base.endswith(".txt")):
            continue
        if o["size"] == 0:
            hits.append(o)
    return hits


# ---------------------------------------------------------------------------
# printing, in the arc's house style

def hdr(t):
    print()
    print("=" * 74)
    print(t)
    print("=" * 74)


def plain(label, n, unit):
    print("      %-58s %5s" % (label, n))
    print("          ^ one unit of that number is %s" % unit)
