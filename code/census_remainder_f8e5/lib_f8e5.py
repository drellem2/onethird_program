"""lib_f8e5 -- shared machinery for mg-f8e5, the DISPOSAL of mg-1abe's remainder.

THIS LIBRARY IMPORTS `lib_1abe` AND SAYS SO.  mg-f8e5 is not an independent
audit of mg-1abe; it is the disposal of what mg-1abe measured.  Re-deriving its
population rule, its carrying-commit rule and its conclusion grain in different
words would produce a second definition that agrees with the first by accident,
and every disagreement would then be a question about which definition was
meant.  So the definitions are the census's own, imported, and every number
here that is a REPRODUCTION of one of its numbers is tagged as one.

WHAT IS NEW HERE, and it is a distinction the census did not need to draw:

    A DECISION THAT CHANGES ON RE-RUN HAS TWO CAUSES AND ONLY ONE IS DAMAGE.

      RECORD-IS-FALSE   the world at the carrying commit disagrees with what
                        the transcript asserts.  The record is wrong there.

      RERUN-CANNOT-SEE  the world at the carrying commit is as the transcript
                        describes it, and the INSTRUMENT can no longer observe
                        it -- a ref was deleted, a branch was pruned, an input
                        moved out of reach.  The record is the only surviving
                        witness and re-running DESTROYS it.

    mg-1abe's `FLIPS` is the union of the two, correctly, because at its grain
    the question was "does the recorded conclusion still hold".  Disposal has
    to split them, because the remedies are opposites: one says RE-RUN AND
    RE-COMMIT and the other says DO NOT RE-RUN, EVER.
"""

import contextlib
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

sys.path.insert(0, os.path.join(REPO, "code", "transcript_census_1abe"))
import lib_1abe as C  # noqa: E402  -- the census's own definitions, imported

git = C.git
git_ok = C.git_ok
resolve = C.resolve
blob_at = C.blob_at
carrying_commit = C.carrying_commit
transcripts = C.transcripts
parse_producers = C.parse_producers
producer_for = C.producer_for
verdict_lines = C.verdict_lines
verdict_tags = C.verdict_tags
conclusion_verdict = C.conclusion_verdict
code_digest = C.code_digest
declared_digest = C.declared_digest
Ledger = C.Ledger
main_rev = C.main_rev

SELF_DIR = "census_remainder_f8e5"

# The five, as mg-1abe named them.  Quoted, not recomputed: they are the
# census's finding and this item disposes of them.
THE_FIVE = [
    "code/audit_c067/out_c1_rebase.txt",
    "code/hash_population_6e58/out_p2_population.txt",
    "code/hash_population_6e58/out_p3_unrestricted.txt",
    "code/hodge_leverage_audit_f922/out_audit.txt",
    "code/hodge_leverage_repair_ff3e/out_repair_ff3e.txt",
]


# ------------------------------------------------------------- worktrees

@contextlib.contextmanager
def worktree(rev, prefix="f8e5"):
    """A throwaway detached worktree at `rev`, removed and pruned on exit.

    NEVER touches the working tree this script runs in, and never moves a ref.
    """
    d = tempfile.mkdtemp(prefix=prefix + "-")
    path = os.path.join(d, "wt")
    r = subprocess.run(["git", "worktree", "add", "--detach", path, rev],
                       cwd=REPO, capture_output=True)
    if r.returncode != 0:
        shutil.rmtree(d, ignore_errors=True)
        raise RuntimeError("worktree add %s: %s"
                           % (rev, r.stderr.decode("utf-8", "replace")))
    try:
        yield path
    finally:
        subprocess.run(["git", "worktree", "remove", "--force", path],
                       cwd=REPO, capture_output=True)
        shutil.rmtree(d, ignore_errors=True)
        subprocess.run(["git", "worktree", "prune"], cwd=REPO,
                       capture_output=True)


def dirty_paths(wt):
    """Paths git reports as modified in a worktree.  E1's guard.

    mg-f8e5's own D5: a producer killed mid-run left four files mutated, the
    next run REFUSED, and the refusal read exactly like a census result.  Any
    re-run whose worktree is not clean BEFORE it starts is measuring the
    previous run's wreckage.
    """
    out = subprocess.run(["git", "status", "--porcelain"], cwd=wt,
                         capture_output=True).stdout.decode("utf-8", "replace")
    return [ln[3:] for ln in out.splitlines() if ln.strip()]


def run_in(wt, directory, cmd, timeout=1800):
    """Run one producer command inside a worktree.  Returns (rc, seconds).

    `cmd` is the command string the suite's OWN runner spells, taken from
    `producer_for`.  It is executed with `sh -c` from the producing directory,
    exactly as the runner would, with stdout+stderr folded when the runner
    folds them.
    """
    t0 = time.time()
    try:
        r = subprocess.run(["sh", "-c", cmd], cwd=os.path.join(wt, directory),
                           capture_output=True, timeout=timeout)
        rc = r.returncode
    except subprocess.TimeoutExpired:
        rc = None
    return rc, time.time() - t0


def produced_bytes(wt, path):
    p = os.path.join(wt, path)
    if not os.path.exists(p):
        return None
    with open(p, "rb") as fh:
        return fh.read()


def rerun_at(rev, path, spec, timeout=1800, overlay_dir_from=None):
    """Re-run a transcript's producer at `rev` and return what it wrote.

    Returns a dict with keys: bytes, rc, seconds, dirty_before, dirty_after,
    error.  `bytes` is None if nothing was written.

    `overlay_dir_from` checks the producing DIRECTORY out from that commit on
    top of `rev`'s tree.  THAT IS A SYNTHETIC STATE NOBODY EVER COMMITTED and
    every caller must label it as one -- it is mg-1abe's own device for
    mg-b2af's twin, where the twin's tree does not contain the suite at all.
    """
    d = os.path.dirname(path)
    out = {"bytes": None, "rc": None, "seconds": 0.0, "error": None,
           "dirty_before": [], "dirty_after": []}
    try:
        with worktree(rev) as wt:
            if overlay_dir_from:
                r = subprocess.run(
                    ["git", "checkout", overlay_dir_from, "--", d],
                    cwd=wt, capture_output=True)
                if r.returncode != 0:
                    out["error"] = "overlay of %s from %s failed" % (
                        d, overlay_dir_from[:7])
                    return out
                subprocess.run(["git", "reset"], cwd=wt, capture_output=True)
            out["dirty_before"] = dirty_paths(wt)
            if out["dirty_before"] and not overlay_dir_from:
                out["error"] = ("worktree DIRTY before the run: %s"
                                % ", ".join(out["dirty_before"][:4]))
                return out
            if not os.path.exists(os.path.join(wt, d, spec["script"])):
                out["error"] = "%s absent at %s" % (spec["script"], rev[:7])
                return out
            out["rc"], out["seconds"] = run_in(wt, d, spec["cmd"] + " > " +
                                               os.path.basename(path) +
                                               (" 2>&1" if spec.get("combined")
                                                else ""), timeout=timeout)
            out["bytes"] = produced_bytes(wt, path)
            out["dirty_after"] = dirty_paths(wt)
    except RuntimeError as exc:
        out["error"] = str(exc)
    return out


# --------------------------------------------------- producer RECOVERY

# The census's rule is `run_all.sh`, and a directory without one is bucketed
# NO-RUNNER and NOT measured.  That is the right call for a census -- guessing
# a producer inflates the reproducing count -- but "reported as such" is not a
# resting place.  Recovery is TIERED so that every recovered producer carries
# how confident its recovery is, and tier 3 is EXECUTED like every other.

TIER_RUNNER = "T1-RUNNER"        # run_all.sh: the census's own rule
TIER_OTHER_SH = "T2-OTHER-SH"    # a runner under another name, e.g. run_audit.sh
TIER_NAME_MAP = "T3-NAME-MAP"    # out_<stem>.txt <- <stem>.py / audit_<stem>.py
TIER_NONE = "T4-NONE"            # no producer at this commit by any rule


def _name_candidates(out_name):
    """Scripts that could produce `out_<stem>.txt`, in decreasing confidence."""
    stem = out_name[len("out_"):-len(".txt")]
    return ["%s.py" % stem, "audit_%s.py" % stem, "%s.sh" % stem,
            "audit_%s.sh" % stem, "verify_%s.py" % stem,
            "attack_%s.py" % stem, "%s.py" % stem.replace("_", ""),
            "rebuild.py" if stem in ("n5", "n6", "nc4") else None]


# A FOURTH RUNNER FORM THE CENSUS'S PARSER DOES NOT READ.
#
# `lib_1abe.parse_producers` reads three shapes -- straight-line `>`
# redirections, `for` loops and shell functions -- and this arc writes a
# fourth: `python3 audit_gates.py | tee out_gates.txt`.  Five of the ten
# NO-RUNNER directories spell their runner that way, so a recovery rule built
# only on `>` scores them T3 (a GUESS) when their own runner names the producer
# outright.
#
# `tee` is also the form mg-c2b3 warns about -- a pipeline's status in POSIX sh
# is the LAST command's, which is `tee`'s, so these runners cannot report their
# producer's exit code at all.  That is somebody else's finding to act on; what
# it means here is only that the producer is NAMED and can be recovered
# exactly.
_RE_TEE = re.compile(
    r"^[ \t]*(?:python3|python|sh)[ \t]+(?P<cmd>[^|\n]*?)[ \t]*\|[ \t]*"
    r"tee[ \t]+(?:-a[ \t]+)?\"?(?P<out>out_[^\"\s]+\.txt)\"?", re.M)


def parse_tee_producers(sh_text):
    """{out_name: {'cmd','combined'}} for `... | tee out_x.txt` runners."""
    found = {}
    for m in _RE_TEE.finditer(sh_text):
        out = m.group("out")
        if "$" in out:
            continue
        found[out] = {"cmd": m.group("cmd").strip(), "combined": False}
    return found


def recover_producer(path, commit):
    """(spec, tier, note).  spec is None only for TIER_NONE.

    Tier 2 reads any tracked `*.sh` in the directory as a runner and parses it
    with the census's own `parse_producers`, so a suite whose runner is called
    `run_audit.sh` is measured by the same code that measures `run_all.sh`.
    """
    d = os.path.dirname(path)
    name = os.path.basename(path)
    spec, why = producer_for(path, commit)
    if spec is not None:
        return spec, TIER_RUNNER, "run_all.sh"

    listing = [ln.split("\t", 1)[1] for ln in
               git("ls-tree", "%s:%s" % (commit, d)).split("\n")
               if "\t" in ln]
    for sh in sorted(x for x in listing if x.endswith(".sh")):
        text = blob_at(commit, "%s/%s" % (d, sh))
        if text is None:
            continue
        body = text.decode("utf-8", "replace")
        got = parse_producers(body).get(name)
        if got is None:
            got = parse_tee_producers(body).get(name)
        if got is None:
            continue
        script = None
        for tok in got["cmd"].split():
            tok = tok.strip('"\'')
            if tok.endswith(".py") or tok.endswith(".sh"):
                script = tok[2:] if tok.startswith("./") else tok
                break
        if script is None or script not in listing:
            continue
        got["script"], got["dir"] = script, d
        return got, TIER_OTHER_SH, sh

    for cand in _name_candidates(name):
        if cand and cand in listing:
            return ({"cmd": "python3 -u %s" % cand, "combined": True,
                     "script": cand, "dir": d},
                    TIER_NAME_MAP, cand)
    return None, TIER_NONE, why


# ------------------------------------------- the convention, made checkable

REACH_PREFIX = C.REACH_PREFIX          # "reads-outside-tree:"
DECLARE_PREFIX = C.DECLARE_PREFIX      # "code-digest:"

_RE_REACH = re.compile(r"^\s*%s\s*(yes|no)\b" % re.escape(REACH_PREFIX), re.M)


def declared_reach(text):
    """The `reads-outside-tree:` a transcript declares, or None.

    mg-1abe shipped R2 as an AUTHOR'S DECLARATION and said in its own §8 that
    nothing verifies it.  `static_reach` below is the check it said was worth
    building.
    """
    m = _RE_REACH.search(text)
    return m.group(1) if m else None


# Tokens that make a producer's output a fact about the OBJECT STORE rather
# than about a tree: a moving ref, or a walk over history/refs/the file list.
_REACH_TOKENS = (
    '"log"', "'log'", '"rev-list"', "'rev-list'", '"for-each-ref"',
    "'for-each-ref'", '"reflog"', "'reflog'", '"ls-files"', "'ls-files'",
    '"branch"', "'branch'", '"merge-base"', "'merge-base'",
    '"rev-parse"', "'rev-parse'", '"ls-tree"', "'ls-tree'",
    '"show-ref"', "'show-ref'", '"cat-file"', "'cat-file'",
    "git log", "git rev-list", "git for-each-ref", "git ls-files",
    "git ls-tree", "git rev-parse", "git show-ref", "git merge-base",
)


def static_reach(directory, rev):
    """Does ANY `.py`/`.sh` of `directory` at `rev` read outside its own tree?

    A STATIC PROXY and labelled as one everywhere it is printed: it establishes
    that the producer CAN read repository-global state, not that this
    transcript's bytes came from such a read.  That is the same grain mg-1abe
    used for its 103/9 split, deliberately, so the two are comparable.

    Returns (True/False, [evidence lines]).
    """
    hits = []
    for line in git("ls-tree", "-r", "%s:%s" % (rev, directory)).split("\n"):
        if "\t" not in line:
            continue
        name = line.split("\t", 1)[1]
        if not name.endswith((".py", ".sh")):
            continue
        blob = blob_at(rev, "%s/%s" % (directory, name))
        if blob is None:
            continue
        text = blob.decode("utf-8", "replace")
        for i, ln in enumerate(text.split("\n"), 1):
            if any(tok in ln for tok in _REACH_TOKENS):
                hits.append("%s:%d" % (name, i))
                break
    return (bool(hits), hits)


# ------------------------------------------------ the moving-ref detector

# mg-1abe's own defect 2: its scripts each resolved `main` at their own start
# time and `main` MOVED between them, so t1 measured 537 transcripts at
# `eacc5e1` while t2 started at `81214a9`.  Two scripts, one runner, two trees,
# one reported census.
#
# THE SHAPE, stated so the detector's population is what its name says (E5):
#
#   (a) a runner drives TWO OR MORE scripts, and
#   (b) TWO OR MORE of those scripts independently resolve a MOVING REF, and
#   (c) the runner passes NO resolved revision down to them.
#
# One script resolving `main` twice is not the shape: it is one tree.  A runner
# that resolves once and passes the sha is the FIX, not the defect.  A suite
# that never names a moving ref cannot exhibit it at all.

MOVING_REFS = ("main", "HEAD", "origin/main", "@")

_RE_MOVING = re.compile(
    r"""(?x)
    (?: git\( [^)]*? ["'](?:main|HEAD|origin/main)["']
      | \[ \s* ["']git["'] [^]]*? ["'](?:main|HEAD|origin/main)["']
      | git \s+ (?:rev-parse|log|rev-list|describe) [^\n]*? \b(?:main|HEAD|origin/main)\b
      | rev_parse\( \s* ["'](?:main|HEAD|origin/main)["']
      | ["']rev-parse["'] \s*, \s* ["'](?:main|HEAD|origin/main)["']
      | return \s+ ["'](?:main|HEAD|origin/main)["']
      | = \s* ["'](?:main|HEAD|origin/main)["'] \s*(?:\)|,|$|\#)
    )""")

# ONE LEVEL OF INDIRECTION, and it is not an optional refinement: mg-1abe's
# eight scripts do not name `main` at all.  They call `lib_1abe.main_rev()`,
# whose default IS `main`, and each call resolves it at its own start time.  A
# detector that reads only the driven scripts scores that suite ONE-SCRIPT --
# which is what mine did, and the D4b control caught it before it shipped, at
# the one directory in this repository where the answer is known in advance.
_RE_DEF = re.compile(r"^def\s+(\w+)\s*\(", re.M)


def _ref_helpers(directory, rev, listing):
    """Directory-local function names whose BODY resolves a moving ref."""
    names = set()
    for fname in listing:
        if not fname.endswith(".py"):
            continue
        blob = blob_at(rev, "%s/%s" % (directory, fname))
        if blob is None:
            continue
        text = blob.decode("utf-8", "replace")
        bounds = [(m.group(1), m.start()) for m in _RE_DEF.finditer(text)]
        for i, (name, start) in enumerate(bounds):
            end = bounds[i + 1][1] if i + 1 < len(bounds) else len(text)
            if _RE_MOVING.search(text[start:end]):
                names.add(name)
    return names

# A revision handed DOWN from the runner: the fix mg-1abe landed, plus the
# spellings other suites in this arc use for the same thing.
_RE_PASSDOWN = re.compile(
    r"""(?x)
    (?: \$\( \s* git \s+ rev-parse [^)]*\) [^\n]*  (?: \$AT | \$REV | \$SHA | \$AS_OF | --at )
      | AT=.*git \s+ rev-parse
      | REV=.*git \s+ rev-parse
      | SHA=.*git \s+ rev-parse
      | AS_OF=.*git \s+ rev-parse
    )""")


def moving_ref_scan(directory, rev):
    """(verdict, detail) for one suite directory at `rev`.

    verdict is one of:
      SHAPE          (a)+(b)+(c) all hold -- the suite measures >1 tree
      PASSES-DOWN    the runner resolves a revision and hands it to the scripts
      ONE-SCRIPT     only one script names a moving ref: one tree, no seam
      NO-MOVING-REF  no script names a moving ref
      NO-RUNNER      nothing drives the scripts together
    """
    listing = [ln.split("\t", 1)[1] for ln in
               git("ls-tree", "%s:%s" % (rev, directory)).split("\n")
               if "\t" in ln]
    runners = sorted(x for x in listing if x.endswith(".sh"))
    if not runners:
        return "NO-RUNNER", {"scripts": [], "runners": []}

    runner_text = ""
    driven = set()
    for sh in runners:
        blob = blob_at(rev, "%s/%s" % (directory, sh))
        if blob is None:
            continue
        text = blob.decode("utf-8", "replace")
        runner_text += "\n" + text
        for spec in parse_producers(text).values():
            for tok in spec["cmd"].split():
                tok = tok.strip('"\'')
                if tok.endswith((".py", ".sh")):
                    driven.add(tok[2:] if tok.startswith("./") else tok)
                    break

    helpers = _ref_helpers(directory, rev, listing)
    helper_re = (re.compile(r"\b(?:\w+\.)?(?:%s)\s*\("
                            % "|".join(sorted(map(re.escape, helpers))))
                 if helpers else None)

    movers = []
    for name in sorted(driven):
        blob = blob_at(rev, "%s/%s" % (directory, name))
        if blob is None:
            continue
        text = blob.decode("utf-8", "replace")
        m = _RE_MOVING.search(text)
        how = "names it"
        if m is None and helper_re is not None:
            m = helper_re.search(text)
            how = "via a local helper"
        if m:
            line = text[:m.start()].count("\n") + 1
            movers.append("%s:%d (%s)" % (name, line, how))

    detail = {"scripts": sorted(driven), "movers": movers, "runners": runners,
              "helpers": sorted(helpers)}
    if len(driven) < 2:
        return "ONE-SCRIPT", detail
    if not movers:
        return "NO-MOVING-REF", detail
    if _RE_PASSDOWN.search(runner_text):
        return "PASSES-DOWN", detail
    if len(movers) < 2:
        return "ONE-SCRIPT", detail
    return "SHAPE", detail


def suite_dirs(rev):
    """Every `code/<dir>` at `rev` that holds a tracked `.py` or `.sh`."""
    seen = set()
    for p in git("ls-tree", "-r", "--name-only", rev, "code/").split("\n"):
        m = re.match(r"^code/([^/]+)/[^/]+\.(?:py|sh)$", p)
        if m:
            seen.add("code/" + m.group(1))
    return sorted(seen)


# ------------------------------------------------------------- misc

_RE_SHA = re.compile(r"\b[0-9a-f]{7,40}\b")


def shas_named_in(text):
    """Every token in a transcript's own bytes that RESOLVES to a commit."""
    out = []
    for tok in dict.fromkeys(_RE_SHA.findall(text)):
        full = resolve(tok)
        if full and full not in out:
            out.append(full)
    return out


def sha256_16(b):
    return hashlib.sha256(b).hexdigest()[:16]


def provenance_block(rev="HEAD"):
    """R1+R2, this directory's own declaration.  See d3_adopt.py for the check."""
    return C.provenance_block("code/" + SELF_DIR, rev)


class Ledger(C.Ledger):
    """mg-1abe's ledger, with the declaration pointed at THIS directory.

    A DEFECT OF MINE, CAUGHT BY WRITING THE CHECK BEFORE READING THE HEADER.
    `lib_1abe.Ledger.__init__` prints `provenance_block("code/" + SELF_DIR)`
    where `SELF_DIR` is bound in ITS module -- so every transcript I produced
    while importing it unmodified declared `code/transcript_census_1abe`'s
    digest as its own provenance.  It was a TRUE digest of the wrong directory,
    which is the worst kind: `d3`'s R3 control recomputes the declared digest
    from the tree and would have found it AGREEING, because it did agree -- with
    a directory I had not edited.

    The first adopter of a convention getting the convention wrong in the
    direction the check cannot see is worth more than the adoption.
    """

    def __init__(self, title, reads_outside_tree=True):
        self.findings = 0
        self.self_errors = 0
        print("=" * 78)
        print(title)
        print("=" * 78)
        print("    " + C.provenance_block("code/" + SELF_DIR, "HEAD"))
        print("    %s %s" % (C.REACH_PREFIX,
                             "yes" if reads_outside_tree else "no"))
        if reads_outside_tree:
            print("    ^ THIS TRANSCRIPT IS NOT PINNABLE BY ANY TREE.  It reads"
                  " repository-global state\n      -- refs, history, the file "
                  "list of `main` -- so it is a fact about the object store as"
                  " it\n      stood at the run, and the NEXT commit anyone "
                  "makes displaces it.  Declaring that\n      is the only "
                  "honest thing an instrument in this class can do.")
