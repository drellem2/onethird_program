"""mg-4700 kernel -- plant, run, restore, and PROVE the restore.

This is an audit of mg-821e, which repaired mg-6cb9's three OPEN items.  Two of
those items are about the difference between a claim being TRUE and a claim
being true BY CONSTRUCTION, and one is about the difference between a call
being PRESENT in a script and the script EXECUTING it.  Neither difference is
visible by reading.  So this kernel does exactly two things:

  1.  MUTATE THE REAL WORKTREE and restore it, proving the restore rather than
      asserting it.  `git status --porcelain` AND the full `git diff` are
      captured before every probe and compared after it.  Porcelain alone is
      not enough: mg-821e's own OUTCOMES.md records that its restore contract
      was porcelain-only while four files were already modified, so a probe
      that failed to restore one would have compared EQUAL.

  2.  RUN A `run_all.sh` and read ITS OWN STDOUT.  A call in a script is not
      evidence of execution -- a guarded branch, an early exit, a swallowed
      error and a `| tee` in front of `set -e` all leave the line in place.

WHY THE PROBES PLANT DIRECTORIES INSTEAD OF READING THE WALK.  mg-6cb9's F1
was that "EVERY REGULAR FILE" was true *only because no tree had a
subdirectory*.  A contingent extent and a sound one are byte-identical from the
outside: both print the same sentence and both exit 0.  The only instrument
that separates them is a subdirectory.  So every depth claim here is measured
by planting one, and none of it is inferred from `os.walk` appearing in the
source.

`PYTHONDONTWRITEBYTECODE` is set for every child.  A probe that patches a
`.py`, runs it and restores the source can leave a `__pycache__/*.pyc`
validated on (source mtime in WHOLE SECONDS, source size) -- restoring a
same-length line inside the same second leaves the stale bytecode VALID and
every later run imports a constant its source does not contain, with
`git status` clean throughout.  That inverted one of mg-6cb9's results and it
is in mg-821e's OUTCOMES.md; it is not re-learned here.
"""

import os
import re
import shutil
import subprocess
import sys

__all__ = ["hdr", "REPO", "HERE", "sh", "git_state", "Probe", "run_checker",
           "run_runner", "restore_paths", "clear_pycache", "PRE_REPAIR",
           "REPAIR", "predict", "flat", "regions", "needle_re", "delete_at",
           "WIRE_MARK", "CALL_AND_GUARD", "CALL_ONLY", "PRINTING", "unwire",
           "RestoreFailed"]

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))

# THE PRE-REPAIR REF, PINNED, NOT `HEAD`.
#
# mg-821e learned this one the expensive way and its `41ac5d4` is the fix: two
# of its comparisons were anchored on `HEAD`, and both were true right up to
# the moment the repair was committed, at which point `HEAD` BECAME the repair
# and the comparisons quietly stopped comparing anything.  D4c below runs
# `check_doc.py` as it stood BEFORE mg-821e, so it names the commit.
PRE_REPAIR = "af432ee~1"        # the parent of mg-821e's repair commit
REPAIR = "af432ee"              # mg-821e's repair


def hdr(t):
    print("=" * 78)
    print(t)
    print("=" * 78)
    print()


def predict(pid, said, got, ok):
    """Print one row against its PREDICTION, which was committed first.

    A run that only ever prints what happened cannot be wrong.  Every row
    here carries what PREDICTIONS.md said would happen, so a miss is visible
    in the transcript instead of being available for quiet re-description.
    """
    verdict = "as predicted" if ok else "*** MISSED ***"
    print("  %-5s predicted %-26s got %-26s %s"
          % (pid, said, got, verdict))
    return 0 if ok else 1


def sh(args, cwd=None, env=None):
    """(returncode, stdout, stderr).  Never raises on a non-zero exit: the
    exit code is the measurement here, not an error."""
    e = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    if env:
        e.update(env)
    p = subprocess.run(args, cwd=cwd or REPO, capture_output=True, text=True,
                       env=e)
    return p.returncode, p.stdout, p.stderr


def git_state():
    """Porcelain AND the full diff.

    Two channels because each is blind where the other sees.  Porcelain names
    untracked files -- a planted `sub/leak.md` or a symlink -- which `git diff`
    cannot see at all.  `git diff` carries the CONTENT of a modification, which
    porcelain reduces to a single ` M` whether one byte moved or a thousand.  A
    probe that edits a file already modified, and restores it wrongly, is
    invisible to porcelain and loud in the diff.
    """
    _, por, _ = sh(["git", "status", "--porcelain"])
    _, dif, _ = sh(["git", "diff"])
    return por, dif


def clear_pycache(*rels):
    for rel in rels:
        d = os.path.join(REPO, rel, "__pycache__")
        shutil.rmtree(d, ignore_errors=True)


def restore_paths(*rels):
    """`git checkout --` the given repo-relative paths, then drop bytecode."""
    sh(["git", "checkout", "--"] + list(rels))
    for rel in rels:
        clear_pycache(rel)


class RestoreFailed(Exception):
    pass


class Probe:
    """One mutation of the real worktree, with the restore proved.

    Usage:

        with Probe("D1a  a subdirectory planted in species_7d75") as pr:
            pr.plant("code/species_7d75/sub/leak.md", LEAK)
            rc, out = run_checker("code/species_remainder_f8fa/w3_scope.py")

    Everything the probe created is removed on the way out, everything it
    edited is written back from the bytes captured on the way in, and the
    `(porcelain, diff)` pair is compared with the pair captured before.  A
    difference raises: a probe that cannot prove it put the tree back has not
    measured anything, it has changed the subject of every later probe.
    """

    def __init__(self, label, restores=()):
        self.label = label
        self.restores = list(restores)
        self.created = []       # paths to remove (files, symlinks, dirs)
        self.edited = {}        # abs path -> original bytes

    def __enter__(self):
        self.before = git_state()
        return self

    # -- mutations ---------------------------------------------------------
    def plant(self, rel, content):
        """Create a file (and any parent directories), recording both."""
        p = os.path.join(REPO, rel)
        made = []
        d = os.path.dirname(p)
        while not os.path.isdir(d) and len(d) > len(REPO):
            made.append(d)
            d = os.path.dirname(d)
        for d in reversed(made):
            os.mkdir(d)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(content)
        self.created.append(p)
        self.created.extend(made)
        return p

    def symlink(self, rel, target):
        """Create a symlink at `rel` pointing at absolute `target`."""
        p = os.path.join(REPO, rel)
        os.symlink(target, p)
        self.created.append(p)
        return p

    def edit(self, rel, old, new, count=1):
        """Replace `old` with `new` exactly `count` times; the original bytes
        are kept verbatim for the restore."""
        p = os.path.join(REPO, rel)
        if p not in self.edited:
            with open(p, "rb") as fh:
                self.edited[p] = fh.read()
        text = self.edited[p].decode("utf-8")
        n = text.count(old)
        if n != count:
            raise AssertionError("%s: expected %d occurrence(s) of %r, found "
                                 "%d" % (rel, count, old[:60], n))
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(text.replace(old, new))
        return p

    def write(self, rel, text):
        """Overwrite a tracked file wholesale, keeping the original bytes."""
        p = os.path.join(REPO, rel)
        if p not in self.edited:
            with open(p, "rb") as fh:
                self.edited[p] = fh.read()
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(text)
        return p

    def read(self, rel):
        with open(os.path.join(REPO, rel), encoding="utf-8") as fh:
            return fh.read()

    # -- restore -----------------------------------------------------------
    def __exit__(self, *exc):
        for p, data in self.edited.items():
            with open(p, "wb") as fh:
                fh.write(data)
        for p in self.created:
            if os.path.islink(p) or os.path.isfile(p):
                os.unlink(p)
            elif os.path.isdir(p):
                shutil.rmtree(p, ignore_errors=True)
        if self.restores:
            sh(["git", "checkout", "--"] + self.restores)
        for p in list(self.edited) + list(self.created):
            shutil.rmtree(os.path.join(os.path.dirname(p), "__pycache__"),
                          ignore_errors=True)
        for rel in self.restores:
            clear_pycache(rel)
        after = git_state()
        if after != self.before and exc[0] is None:
            sys.stdout.flush()
            sys.stderr.write("RESTORE FAILED after probe: %s\n" % self.label)
            for i, name in enumerate(("porcelain", "diff")):
                if after[i] != self.before[i]:
                    sys.stderr.write("  %s differs\n  --- before\n%s\n"
                                     "  --- after\n%s\n"
                                     % (name, self.before[i][:2000],
                                        after[i][:2000]))
            raise RestoreFailed(self.label)
        return False


def run_checker(rel, args=()):
    """(exit code, stdout+stderr) for one checker, run from its own dir."""
    p = os.path.join(REPO, rel)
    rc, out, err = sh([sys.executable, "-B", os.path.basename(p)] + list(args),
                      cwd=os.path.dirname(p))
    return rc, out + err


def run_runner(tree, timeout=600):
    """(exit code, stdout+stderr) for one `run_all.sh`, and the tree restored.

    THIS is the measurement OPEN 2 asks for.  `grep` for the call in the script
    answers a different question -- mg-6cb9's F2 was a check that existed, was
    correct, was named in every reader-facing artifact, and was executed by
    nobody.  A runner's own stdout is the only thing that separates the two.
    """
    d = os.path.join(REPO, "code", tree)
    p = subprocess.run(["sh", "run_all.sh"], cwd=d, capture_output=True,
                       text=True, timeout=timeout,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    out = p.stdout + p.stderr
    # The runners write their own out_*.txt.  Put them back before anything
    # else looks at the tree.
    restore_paths("code/" + tree)
    return p.returncode, out


# ---------------------------------------------------------------------------
# The wiring block, and the three parts of it that can be deleted separately.
#
# These live HERE and not in `q2_wiring.py` for the reason mg-821e records in
# its own OUTCOMES.md: `q2_wiring.py` runs its probes at module level, so
# importing it to borrow one function would run twenty-one `run_all.sh` from
# inside the self-test.  Quoted from the runners rather than described; all
# three carry them byte-identically.
# ---------------------------------------------------------------------------
WIRE_MARK = "# mg-821e, on mg-6cb9's F2.  THE CROSS-SECTION CHECK, WIRED."

CALL_AND_GUARD = (
    'E2OUT=$(python3 ../species_extent_d633/e2_crosssection.py) || {\n'
    '    echo "$E2OUT" | grep \'STANDING UN-STRUCK\' || true\n'
    '    echo "E2 CROSS-SECTION FAILED -- a struck claim stands un-struck'
    ' elsewhere"\n'
    '    exit 1\n'
    '}\n')
CALL_ONLY = 'E2OUT=$(python3 ../species_extent_d633/e2_crosssection.py)\n'
PRINTING = (
    'echo "cross-section check (mg-821e), its own output:"\n'
    'echo "$E2OUT" | grep -E \'strike\\(s\\) measured|^E2 TOTAL BAD:\'\n')


def unwire(text):
    """Remove the whole wiring block: the marker comment through the second
    `echo`, and the blank line that separates it from what precedes it."""
    lines = text.splitlines(True)
    start = next(i for i, l in enumerate(lines) if l.startswith(WIRE_MARK))
    end = next(i for i, l in enumerate(lines)
               if l.startswith('echo "$E2OUT" | grep -E'))
    while start > 0 and lines[start - 1].strip() == "":
        start -= 1
    return "".join(lines[:start] + lines[end + 1:])


# ---------------------------------------------------------------------------
# Document surgery, for Q3.  A "site" is a markdown heading region -- the unit
# a table of contents points at, and the unit `check_doc.py`'s C4 checks in.
# ---------------------------------------------------------------------------
def flat(s):
    """`check_doc.py`'s own flattener, COPIED rather than imported.

    Copied for the reason this whole audit is about: an expectation computed
    by the subject's own code cannot disagree with the subject.  If the two
    drift apart, Q3's row counts stop matching and that is a finding here."""
    s = re.sub(r"(?m)^(?:\s*>)+\s?", "", s)
    return re.sub(r"\s+", " ", s).strip()


def regions(lines):
    """(heading line, start, end) for every ATX heading region.

    A region runs to the next heading of ANY level, so `## 2.` does not
    swallow `### 2.1` -- the same rule `check_doc.py` uses."""
    starts = [i for i, ln in enumerate(lines) if ln.startswith("#")]
    return [(lines[i], i, starts[j + 1] if j + 1 < len(starts) else len(lines))
            for j, i in enumerate(starts)]


def needle_re(s):
    """A whitespace-tolerant regex for a needle.

    `flat()` is what the checker counts with, so a deletion that left a
    line-wrapped copy behind would be testing nothing."""
    return re.compile(r"\s+".join(re.escape(t) for t in s.split()))


def delete_at(text, needle, site_pat):
    """Delete every copy of `needle` inside the ONE heading region matching
    `site_pat`, and nowhere else.

    Returns (new text, copies removed at the site, copies left in the rest of
    the file).  The third number is the point of the probe: the check has to
    fire while eighteen other copies stand."""
    lines = text.splitlines(True)
    hit = next(((h, a, b) for h, a, b in regions(lines)
                if re.search(site_pat, h)), None)
    if hit is None:
        return None, 0, 0
    _h, a, b = hit
    region = "".join(lines[a:b])
    rx = needle_re(needle)
    n = len(rx.findall(region))
    new = "".join(lines[:a]) + rx.sub("", region) + "".join(lines[b:])
    return new, n, len(rx.findall(flat(new)))
