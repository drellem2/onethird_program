#!/usr/bin/env python3
"""mg-502f — THE GUARD.  A script that runs `./build.sh` must not be writing into a file
`./build.sh` is about to read.

THE MECHANISM IT REFUSES, in one line: the shell opens the redirect target BEFORE the
script starts, so `python3 s.py > code/d/out_s.txt` leaves that tracked transcript
TRUNCATED for the whole of s.py's run — and `./build.sh` ends with mg-f771's control,
which grades every tracked `code/**/out_*.txt` that differs from its committed copy.  A
truncated file has a different line count from its committed copy, so `texts_equivalent`
returns False on the length test before any normalisation rule is consulted: DISAGREES,
`./build.sh` exits 1, and the script is looking at a gate its own invocation reddened.

WHY A GUARD AND NOT ONLY A REPAIR.  mg-479c repaired `x0_exhibit.py` by having it buffer
its output and write its own transcript last.  That is correct and it is not sufficient:
the OLD invocation still exists — in this repository's own `build.sh` header at the mg-479c
block, in mg-502f's ticket body, and in the fingers of anyone who has typed it — and typing
it again re-creates the defect against the repaired script, because the shell truncates the
file whether or not the script later rewrites it.  A repair changes the default; a guard
changes what happens when the default is not taken.

WHAT IT CANNOT SEE, stated so the green is not over-read:

  * `cmd | tee code/d/out_s.txt`.  stdout is a PIPE; nothing in this process can name tee's
    argument.  The estate already forbids the pipe form for an unrelated and older reason
    (`cmd | tee f` makes `$?` tee's status — mg-9bc2, restated in three runners), so the
    forbidden form and the invisible form coincide.  That is luck, not design.
  * a script that WRITES a tracked transcript by name, with `open()`, while `./build.sh`
    runs.  The guard reads stdout's identity, not the process's future writes.
  * `> code/d/out_s.txt` on a file that is not TRACKED.  Correct rather than a gap: f771
    watches tracked files, so an untracked transcript is outside the control and outside
    the defect.

THE TEST IS ON INODE IDENTITY, NOT ON A PATH STRING, because the defect does not care how
the redirect was spelled: `> out_s.txt` from the directory, `> code/d/out_s.txt` from the
root, `>>` in append mode, and a path through a symlink are one situation and `os.fstat`
gives them one answer.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

# ONE DEFINITION OF THE WATCHED CLASS, AND IT IS THE CONTROL'S OWN.  Re-spelling
# `out_*.txt under code/` here would be a second definition that could drift from the one
# that actually grades the files, which is the shape mg-e331's own docstring warns about
# ("importing a rule is one refactor away from re-specifying it") pointed the other way:
# here the rule is IMPORTED precisely so it cannot be re-specified.
sys.path.insert(0, os.path.join(ROOT, "code", "gate_fixed_point_f771"))
import lib_f771 as F  # noqa: E402


def tracked_transcripts(root=ROOT):
    """Every tracked `code/**/out_*.txt`, from git rather than from a walk of the disk:
    the class f771 grades is the TRACKED one, and an untracked file of the same name is
    outside both the control and this guard."""
    p = F._git(root, "ls-files", "--", "code")
    if p.returncode != 0:
        return None
    return [rel for rel in p.stdout.splitlines() if F.is_transcript(rel)]


def stdout_transcript(root=ROOT, stream=None):
    """The tracked transcript this process's stdout IS, or None.

    Returns None when stdout is not a regular file (a terminal, a pipe, a capture buffer),
    when git cannot be reached, or when no tracked transcript shares its inode.
    """
    stream = sys.stdout if stream is None else stream
    try:
        st = os.fstat(stream.fileno())
    except (OSError, ValueError, AttributeError):
        return None                      # not a real fd: a StringIO, a closed stream
    import stat as _stat
    if not _stat.S_ISREG(st.st_mode):
        return None                      # a tty or a pipe — nothing is being truncated
    rels = tracked_transcripts(root)
    if rels is None:
        return None                      # no git: this guard cannot answer, and says so
    for rel in rels:
        try:
            fs = os.stat(os.path.join(root, rel))
        except OSError:
            continue
        if (fs.st_dev, fs.st_ino) == (st.st_dev, st.st_ino):
            return rel
    return None


REFUSAL = 2                              # the estate's third verdict: could-not-tell


def refuse_if_self_red(script, stream=None, root=ROOT, exit_fn=None):
    """Call this FIRST in any script that runs `./build.sh`.  Refuses (exit 2) rather than
    running, because a run under this invocation produces a coherent-looking transcript of
    a gate the run itself reddened — which is the failure mode mg-502f exists about: not a
    crash, a well-formed wrong answer."""
    rel = stdout_transcript(root=root, stream=stream)
    if rel is None:
        return None
    out = sys.stderr
    out.write("\n")
    out.write("REFUSED — %s runs `./build.sh`, and its stdout IS %s.\n" % (script, rel))
    out.write("\n")
    out.write("  The shell truncated that file when it opened the redirect, before this\n")
    out.write("  process started.  `./build.sh` ends with mg-f771's control, which compares\n")
    out.write("  every tracked code/**/out_*.txt against its committed copy — so this run\n")
    out.write("  would hand it a half-written file, the gate would exit 1, and this script\n")
    out.write("  would report on a redness it had caused itself.  mg-479c found exactly that\n")
    out.write("  in code/alias_agreement_06d1/x0_exhibit.py; mg-502f swept for the rest.\n")
    out.write("\n")
    out.write("  Run it WITHOUT the redirect.  Scripts in this class write their own\n")
    out.write("  transcript after the last gate run.\n")
    out.write("\n")
    (exit_fn or sys.exit)(REFUSAL)
    return rel
