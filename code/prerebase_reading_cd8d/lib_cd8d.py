"""mg-cd8d — shared plumbing for the pre-rebase-reading experiment.

THE QUESTION IS A COMMAND AND NOT AN ARGUMENT, which is pm-onethird's own framing of it.
mg-99f4 published a census reading it had taken BEFORE the refinery rebased its branch, threw
that reading away, and re-took it after — and said so.  mg-05c6 then landed a corpus pin and
two new verdicts, `CORPUS` and `STALE`.  Whether the pin CLOSES the pre-rebase case or is
BLIND to it decides what, if anything, is left to build, and the two possibilities differ in
what `lib_f771.verdict_for` returns for one specific pair of texts.  So this directory
constructs that pair and asks it.

WHAT IS SIMULATED AND WHAT IS REAL.  Nothing here is a fixture standing in for a census.  A
world is TWO REAL COMMITS OF `main`: the corpus is `git archive`d at each, today's producer is
overlaid onto both, and the REAL `a4_sweep.py` is run over each as a subprocess so that
`lib9876.ROOT` resolves to the sandbox rather than to this repository.  The two readings are
then handed to the REAL `lib_f771.verdict_for` — imported, not re-spelled, because a
re-spelling would make every finding here a statement about the re-spelling (mg-d2c2).  The
only synthetic object in any world is the simulated branch's OWN new directory, which is one
`.py` file holding `VALUE = 1`, and it exists only inside a temporary directory.

WHY TODAY'S PRODUCER IS OVERLAID ONTO BOTH TREES, AND WHY THAT IS NOT THE THING mg-ede8
FORBIDS.  mg-ede8's rule is that today's RULE is never run against an old tree, because that
conflates `the corpus moved` with `the instrument changed`.  Here the conflation is the other
way round and overlaying is what PREVENTS it: a branch open today carries today's producer on
both sides of its own rebase, so a world whose two readings came from two different producers
would differ in the PRODUCER PIN, which `verdict_for` grades `DISAGREES` for a reason that has
nothing to do with when the reading was taken.  Worlds older than mg-05c6 print no pin at all.
Both failure modes are planted in `r0_selftest.py` (D2, D3) rather than described here.

WHAT IS PRINTED AND WHAT IS DELIBERATELY NOT.  Populations, whether each pin MOVED, and the
verdict.  NOT the pin digests themselves: a digest covers the content of the producer's source,
so printing one would put a number in a tracked transcript that moves whenever somebody edits
`a4_sweep.py` — this directory's own subject, one file over.  The populations are counts of
directories at two fixed commits and cannot move; the verdicts are a function of
`lib_f771.verdict_for`, which is the instrument under test and SHOULD move this transcript when
it changes.
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

sys.path.insert(0, os.path.join(ROOT, "code", "gate_fixed_point_f771"))
sys.path.insert(0, os.path.join(ROOT, "code", "control_audit_9876"))
import lib_f771 as F       # noqa: E402  the REAL decider
import a4_sweep as A       # noqa: E402  the REAL detectors, for r0's own count

PRODUCER = os.path.join("code", "control_audit_9876")
CENSUS = "code/control_audit_9876/out_a4_sweep.txt"

# The commits every world is a function of.  PINNED, and checked to resolve and to be an
# ancestor of HEAD before anything is measured — a world built on a commit this checkout does
# not carry is not a smaller measurement, it is a different one (mg-585e's practice).
#
# AS_OF is `main`'s tip when this directory was written.  The refinery rebases, so it stays an
# ancestor of whatever HEAD this branch is merged from, and the populations below stay fixed
# forever.  A figure taken against a moving `origin/main` would be a figure that rots, in the
# directory whose subject is figures that rot.
AS_OF = "b5d8a75"          # main's tip 2026-08-14, population 235
MAIN_BEFORE = "3f6d8d6"    # population 233 — the simulated branch's merge base
MAIN_FAR = "c4190b5"       # population 224 — far enough behind to trip the STALE bound
PIN_05C6 = "8b169b1"       # mg-05c6's landing: the commit that created the corpus pin

BRANCH_DIR = "branch_dir_cd8d"   # the simulated branch's own new directory, sandbox only


class Refused(Exception):
    """This harness could not build the world it was asked about, which is not a finding."""


def _git(*args):
    p = subprocess.run(("git", "-C", ROOT) + args, capture_output=True)
    return p


def require_commits():
    """Every pinned commit resolves in this checkout and is an ancestor of HEAD."""
    p = _git("rev-parse", "--is-inside-work-tree")
    if p.returncode != 0 or p.stdout.decode().strip() != "true":
        raise Refused("%s is not inside a git work tree; every world here is two commits of "
                      "main and there are none to read" % ROOT)
    for c in (AS_OF, MAIN_BEFORE, MAIN_FAR, PIN_05C6):
        if _git("rev-parse", "--verify", "%s^{commit}" % c).returncode != 0:
            raise Refused("pinned commit %s does not resolve in this checkout" % c)
        if _git("merge-base", "--is-ancestor", c, "HEAD").returncode != 0:
            raise Refused("pinned commit %s is not an ancestor of HEAD, so the world built "
                          "on it is not the world this directory claims to measure" % c)


_CACHE = {}


def reading(commit, extra_dirs=(), overlay_producer=True, archive=True):
    """The census as TODAY's `a4_sweep.py` prints it over the corpus at `commit`.

    `overlay_producer` and `archive` are parameters and not constants because r0 needs the
    worlds in which they are FALSE: a harness that silently extracted nothing would report
    two identical readings and a green for the wrong reason, and one that ran each tree's own
    producer would report a moved PRODUCER pin and a red for the wrong reason.
    """
    key = (commit, tuple(extra_dirs), overlay_producer, archive)
    if key in _CACHE:
        return _CACHE[key]
    tmp = tempfile.mkdtemp(prefix="cd8d-")
    try:
        if archive:
            tar = _git("archive", commit, "code")
            if tar.returncode != 0:
                raise Refused("git archive %s failed" % commit)
            p = subprocess.run(["tar", "-x", "-C", tmp], input=tar.stdout,
                               capture_output=True)
            if p.returncode != 0:
                raise Refused("could not extract the corpus at %s" % commit)
        if overlay_producer:
            # SOURCE ONLY.  The producer's own transcripts are rewritten by every run of its
            # suite, and copying them would make this arm's output a function of a file that
            # moves; the corpus pin excludes this directory anyway.
            dst = os.path.join(tmp, PRODUCER)
            shutil.rmtree(dst, ignore_errors=True)
            os.makedirs(dst)
            src = os.path.join(ROOT, PRODUCER)
            for fn in sorted(os.listdir(src)):
                if fn.endswith((".py", ".sh")):
                    shutil.copy2(os.path.join(src, fn), os.path.join(dst, fn))
        for d in extra_dirs:
            os.makedirs(os.path.join(tmp, "code", d), exist_ok=True)
            with open(os.path.join(tmp, "code", d, "x.py"), "w", encoding="utf-8") as fh:
                fh.write("VALUE = 1\n")
        prod = os.path.join(tmp, PRODUCER, "a4_sweep.py")
        if not os.path.exists(prod):
            raise Refused("no producer at %s — there is nothing to run" % PRODUCER)
        p = subprocess.run([sys.executable, prod], capture_output=True, text=True)
        out = p.stdout
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    _CACHE[key] = (out, p.returncode)
    return _CACHE[key]


def figures(text):
    """(population, corpus pin, producer pin) as the producer printed them, or None each."""
    cp = F.corpus_pin(text)
    return (cp[1] if cp else None, cp[0] if cp else None, F.producer_pin(text))


def verdict(committed, worktree, relpath=CENSUS):
    """THE REAL `verdict_for`, and the default `relpath` is the census's own declared path.

    Called through this one name so that r0's identity check covers every call site: there is
    no second spelling of the decision anywhere in this directory.
    """
    return F.verdict_for(committed, worktree, relpath)


def moved(a, b):
    return "MOVED" if a != b else "same"
