"""mg-821e kernel -- IN-PLACE mutation, a verified restore, and a RUNNER.

This instrument answers mg-6cb9's three OPEN items, and two of the three are
about the difference between an artifact being present and a behaviour
happening.  So the harness has to be able to do two things that mg-d633's
sandbox could not:

  1.  MUTATE THE REAL WORKTREE.  mg-6cb9 established why: a `shutil.copytree`
      sandbox has no `.git`, so `s1_extent.py`'s controls (a) and (b) fall
      into their `git archive` failure branch and contribute nothing.  Every
      probe here edits the tree it will be committed in, and proves the
      restore rather than asserting it -- `git status --porcelain` AND the
      full `git diff` before and after, byte for byte, and the run stops if
      they differ.  Porcelain alone is not enough here; see `git_status`.

  2.  RUN A `run_all.sh`, not a checker.  OPEN 2 is `merged is not live` at
      script level: the check that closes B1 existed, was correct, and was
      called by 0 of the 3 species runners.  A call written into a script is
      not evidence that the script executes it -- a guarded branch, an early
      exit or a swallowed error all leave the line in place.  So the
      measurement is the RUNNER'S OWN STDOUT, and `run_runner` below is what
      produces it.

`PYTHONDONTWRITEBYTECODE` is not optional and mg-6cb9 paid for the lesson: a
probe that patches a `.py`, runs it and restores the source leaves a
`__pycache__/*.pyc` validated on (source mtime in WHOLE SECONDS, source size).
Restoring a same-length line in the same second leaves the stale bytecode
VALID, and every later run in that tree imports a constant its source does not
contain, with `git status` clean throughout.  It inverted one of that audit's
results.  Here `-B` is set for every child, and every `__pycache__` under a
mutated file's directory is emptied on the way out.
"""

import os
import re
import subprocess
import sys

__all__ = ["hdr", "REPO", "sh", "git_status", "Probe", "run_checker",
           "run_runner", "flat", "plant", "replace_once", "preserve",
           "delete_at_site", "sections", "out_files", "WIRE_MARK", "unwire",
           "PRE_REPAIR"]

# The wiring block mg-821e adds to the three species runners, and the deletion
# test that takes it out again.  BOTH LIVE HERE rather than in `p3_wiring.py`
# because `selftest821e.py` needs the second: `p3_wiring.py` runs its probes at
# module level, so importing it to borrow one function ran the whole
# instrument -- twelve `run_all.sh` -- from inside the self-test.  That is in
# OUTCOMES.md, and it cost more than the refactor.
WIRE_MARK = "# mg-821e, on mg-6cb9's F2.  THE CROSS-SECTION CHECK, WIRED."

# THE PRE-REPAIR REF, PINNED, AND NOT `HEAD`.
#
# Two measurements in this instrument compare the repaired artifact with the
# one it replaced: `p2_sites.py` runs `check_doc.py` as it stood before this
# ticket, and `selftest821e.py` asserts that undoing the wiring gives back the
# runner byte for byte.  Both were written against `HEAD`, and both were true
# until the moment the repair was committed -- at which point `HEAD` BECAME the
# repair, `p2_sites.py` reported the old checker firing 7 of 7, and the
# self-test reported the wiring absent from three runners that carry it.
#
# A comparison against `HEAD` does not fail when the repair lands.  It silently
# changes what it is comparing, and starts measuring the repair against itself.
# That is this ticket's own finding one level out: a check whose meaning
# depends on a condition nobody stated -- here, `HEAD does not contain this
# work` -- and the condition went false in the ordinary course of doing the
# work.  So the ref is PINNED, the way `s1_extent.py` pins `ebecd89` and
# `83ac472` and `d2_deletion.py` pins its own.
PRE_REPAIR = "b6bc2ef"          # the commit this branch left from (mg-9220)

# The one-line mutations that REMOVE THE RECURSION, one per repaired site.
# Each declares the unit it deletes: the line telling `os.walk` which
# directories to descend into.  Setting it to `[]` is exactly "stop after the
# root", which is the state mg-6cb9 measured.  They live in the kernel so that
# `selftest821e.py` can assert against them without importing `p1_depth.py`,
# which runs eighteen probes at module level.
NO_RECURSE = [
    ("w3_scope.py", "code/species_remainder_f8fa/w3_scope.py",
     "    _dns[:] = sorted(_d for _d in _dns if _d != PYCACHE)",
     "    _dns[:] = []"),
    ("s1_extent.py", "code/species_repair_a4ef/s1_extent.py",
     "        dirnames[:] = sorted(d for d in dirnames if d != PYCACHE)",
     "        dirnames[:] = []"),
    ("e1_extents.py", "code/species_extent_d633/e1_extents.py",
     "        dns[:] = sorted(d for d in dns if d != PYCACHE)",
     "        dns[:] = []"),
]


def unwire(text):
    """Remove the wiring block from a runner, and insist it was there.

    The block is ONE unit: from the marker comment to the last line that
    mentions `$E2OUT`.  The LAST, not the first -- the block contains two, and
    an earlier version of this function cut between them and left a dangling
    `}`.  Every runner then exited 1 on a syntax error and the deletion test
    read as "the check is gone" when what was gone was the script.  A deletion
    test that breaks the thing it deletes from measures nothing.
    """
    if WIRE_MARK not in text:
        raise AssertionError("the wiring block is not in this runner")
    lines = text.splitlines(True)
    i = next(k for k, ln in enumerate(lines) if WIRE_MARK in ln)
    j = max(k for k in range(i, len(lines)) if 'echo "$E2OUT"' in lines[k])
    out = lines[:i] + lines[j + 1:]
    # The block was inserted after a blank line and ends before one, so cutting
    # it out leaves two blanks touching.  Close the seam, and the result is
    # BYTE-IDENTICAL to the runner before this ticket -- which the self-test
    # asserts against `git show PRE_REPAIR:`, because "the wiring is a pure
    # addition" is a claim and that comparison is the measurement of it.
    if i > 0 and out[i - 1:i] == ["\n"] and out[i:i + 1] == ["\n"]:
        del out[i]
    return "".join(out)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))


def hdr(title):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)
    print()


def sh(args, cwd=None):
    p = subprocess.run(args, cwd=cwd or REPO, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def git_status():
    """The restore contract: `git status --porcelain` AND the full diff.

    `--porcelain` alone is not enough and the self-test is what showed it.  A
    file that is already modified reads ` M path` before a probe and ` M path`
    after one, so a probe that mutated it and failed to put it back would
    compare EQUAL.  This instrument necessarily runs against a worktree where
    the four repaired files are modified, so that is not a corner case, it is
    every probe.  The diff makes the comparison byte-level for tracked files;
    `--porcelain` still covers the untracked ones the probes create.
    """
    return (sh(["git", "status", "--porcelain"])[1] + "\n----\n"
            + sh(["git", "diff"])[1])


def flat(s):
    return " ".join(s.split())


def run_checker(rel, args=()):
    """Run one checker where it lives, in the real worktree.  (exit, output)."""
    path = os.path.join(REPO, rel)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, "-B", os.path.basename(path)]
                       + list(args),
                       cwd=os.path.dirname(path), capture_output=True,
                       text=True, env=env)
    return p.returncode, p.stdout + p.stderr


def run_runner(tree, timeout=600):
    """Run a tree's `run_all.sh` AS A SCRIPT.  (exit, combined output).

    This is the whole of OPEN 2's measurement.  `grep`ping a runner for the
    name of a check tells you the call is written; only this tells you it
    executed.
    """
    path = os.path.join(REPO, "code", tree, "run_all.sh")
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run(["sh", "run_all.sh"], cwd=os.path.dirname(path),
                       capture_output=True, text=True, env=env,
                       timeout=timeout)
    return p.returncode, p.stdout + p.stderr


def out_files(tree):
    """Every committed `out_*.txt` of a tree, repo-relative.

    A probe that runs a `run_all.sh` rewrites these, and a mutated run writes
    mutated output.  They are handed to `Probe` so they are saved and put back
    with everything else: a harness that can leave the tree dirty is worse
    than no harness, and this one runs whole scripts.
    """
    d = os.path.join(REPO, "code", tree)
    return ["code/%s/%s" % (tree, f) for f in sorted(os.listdir(d))
            if f.startswith("out_") and f.endswith(".txt")]


class Probe(object):
    """One mutation, applied and undone, with the undo verified.

    `edits` is [(repo-relative path, callable)]; the callable takes the current
    text (None if absent) and returns the new text (None to delete).  Parent
    directories created for a new path are removed on the way out.
    """

    def __init__(self, edits):
        self.edits = edits
        self.saved = {}
        self.made_dirs = []

    def __enter__(self):
        for rel, fn in self.edits:
            p = os.path.join(REPO, rel)
            if os.path.exists(p):
                with open(p, encoding="utf-8", errors="surrogateescape") as fh:
                    old = fh.read()
            else:
                old = None
            if rel not in self.saved:
                self.saved[rel] = old
            d, made = os.path.dirname(p), []
            while not os.path.isdir(d) and len(d) > len(REPO):
                made.append(d)
                d = os.path.dirname(d)
            for m in reversed(made):
                os.mkdir(m)
                self.made_dirs.append(m)
            new = fn(old)
            if new is None:
                if os.path.exists(p):
                    os.unlink(p)
            else:
                with open(p, "w", encoding="utf-8",
                          errors="surrogateescape") as fh:
                    fh.write(new)
        return self

    def __exit__(self, *exc):
        for rel, old in self.saved.items():
            p = os.path.join(REPO, rel)
            if old is None:
                if os.path.exists(p):
                    os.unlink(p)
            else:
                with open(p, "w", encoding="utf-8",
                          errors="surrogateescape") as fh:
                    fh.write(old)
        for d in sorted(self.made_dirs, key=len, reverse=True):
            try:
                os.rmdir(d)
            except OSError:
                pass
        for rel in self.saved:
            pc = os.path.join(REPO, os.path.dirname(rel), "__pycache__")
            if os.path.isdir(pc):
                for f in os.listdir(pc):
                    try:
                        os.unlink(os.path.join(pc, f))
                    except OSError:
                        pass
        return False


def plant(text_to_add):
    """Append a block, creating the file if it is new."""
    def fn(old):
        if old is None:
            return text_to_add
        return old.rstrip("\n") + "\n\n" + text_to_add
    return fn


def preserve(old):
    """An edit that changes nothing: it exists so `Probe` SAVES the file.

    Used for the `out_*.txt` a `run_all.sh` rewrites.  Without it the restore
    is incomplete and the status comparison stops the run -- correctly, which
    is how this function came to be written.
    """
    return old


def replace_once(old_s, new_s):
    """Replace the FIRST occurrence, and insist it was there.  A mutation that
    silently did nothing is a probe that measures nothing."""
    def fn(old):
        if old is None or old_s not in old:
            raise AssertionError("mutation target absent: %r" % old_s[:70])
        return old.replace(old_s, new_s, 1)
    return fn


def sections(text):
    """[(heading line, body)] for every ATX heading region, in order.

    A region runs to the next heading of ANY level, so `## 2.` does not
    swallow `### 2.1`.  This is re-implemented here rather than imported from
    `check_doc.py`: an instrument that computes a subject's answer with the
    subject's own code cannot disagree with it, which is the shape of mg-6cb9's
    F1 and the reason `e1_extents.py` certified an extent over a file it also
    could not see.
    """
    lines = text.splitlines()
    starts = [i for i, ln in enumerate(lines) if ln.startswith("#")]
    out = []
    for j, i in enumerate(starts):
        end = starts[j + 1] if j + 1 < len(starts) else len(lines)
        out.append((lines[i], "\n".join(lines[i:end])))
    return out


def delete_at_site(site_pat, needle, repl):
    """Rewrite `needle` -> `repl` ONLY inside the heading region matching
    `site_pat`, leaving every other copy in the file untouched.

    This is the mutation mg-6cb9's F3 is about.  A presence test over a whole
    document cannot see it when another copy survives; a site check must.
    """
    def fn(old):
        if old is None:
            raise AssertionError("file absent")
        secs = sections(old)
        hit = [i for i, (h, _b) in enumerate(secs) if re.search(site_pat, h)]
        if not hit:
            raise AssertionError("no such site: %r" % site_pat)
        i = hit[0]
        head, body = secs[i]
        if needle not in body:
            raise AssertionError("needle %r not at site %r"
                                 % (needle[:40], site_pat))
        new_body = body.replace(needle, repl)
        # Reassemble by position, not by string replacement: two sections can
        # be byte-identical and `str.replace` would edit the wrong one.
        parts = [b for _h, b in secs]
        parts[i] = new_body
        pre = "\n".join(old.splitlines()[:old.splitlines().index(secs[0][0])])
        joined = "\n".join(parts)
        tail = "\n" if old.endswith("\n") else ""
        return (pre + "\n" + joined + tail) if pre else (joined + tail)
    return fn
