"""Shared machinery for mg-c2b3 -- the arc-wide `| tee` / exit-status sweep.

THE DEFECT.  In POSIX sh a pipeline's exit status is the status of its LAST
command.  `cmd | tee out.txt` therefore reports `tee`'s status, which is 0
whenever tee could write the file -- i.e. essentially always.  `set -e` sees
that 0.  So a runner can print six failures and exit 0.  mg-821e hit exactly
that in `code/species_sites_821e/run_all.sh` and fixed its own; mg-f922 had
measured the same shape a generation earlier in
`code/hodge_leverage_landing_e1d0/run_all.sh` ("verifier exits 1, its runner
exits 0") and that one was fixed too.  Twice found, twice fixed one runner at a
time.  This module is the arc-wide sweep.

WHY THE CLASSIFIER IS NOT A BARE GREP.  The ticket's census was
`grep '| *tee'` over each runner, and that pattern matches PROSE: six of the
twenty-three "hits" are runners whose header comment says *"NOT `| tee`"*
because they were already fixed or never had it.  A census that cannot tell a
pipeline from a comment about a pipeline reports the repaired trees as broken.
`tee_pipelines()` strips comments and quoted strings before it looks, and
`selftestc2b3.py` drives it with both senses of every rule.
"""

import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))


# ---------------------------------------------------------------------------
# shell source: comments and quotes
# ---------------------------------------------------------------------------

def strip_comment(line):
    """Return `line` with its trailing `#` comment removed.

    A `#` opens a comment only at the start of a word (start of line, or after
    whitespace) and only outside quotes.  `echo a#b` is not a comment, and
    `echo "a # b"` is not a comment.  That is the POSIX rule for the cases a
    runner in this arc can contain; it is not a general sh parser, and
    `selftestc2b3.py` states the boundary and exercises both sides of it.
    """
    out = []
    quote = None
    prev = ""
    for ch in line:
        if quote:
            out.append(ch)
            if ch == quote and prev != "\\":
                quote = None
        elif ch in ("'", '"'):
            quote = ch
            out.append(ch)
        elif ch == "#" and (prev == "" or prev.isspace()):
            break
        else:
            out.append(ch)
        prev = ch
    return "".join(out)


def strip_quoted(text):
    """Return `text` with the CONTENTS of quoted strings blanked out.

    `echo "run it as x | tee y"` must not count as a pipeline.  The quotes
    themselves are kept so the result has the same length and column numbers
    still line up with the original.
    """
    out = []
    quote = None
    prev = ""
    for ch in text:
        if quote:
            out.append(" " if ch != quote or prev == "\\" else ch)
            if ch == quote and prev != "\\":
                quote = None
        elif ch in ("'", '"'):
            quote = ch
            out.append(ch)
        else:
            out.append(ch)
        prev = ch
    return "".join(out)


def code_of(line):
    """The executable part of a source line: no comment, no quoted contents."""
    return strip_quoted(strip_comment(line))


TEE_RE = re.compile(r"\|\s*tee\b")


def logical_lines(src):
    """Yield (lineno_of_first_physical_line, joined_source) for `src`.

    Trailing-backslash continuations are joined, because
    `code/face_geometry_landing_7d5a/run_all.sh` writes its second pipeline
    across two physical lines and a per-physical-line scan sees `| tee ...`
    with no command in front of it.
    """
    lines = src.split("\n")
    i = 0
    while i < len(lines):
        start = i + 1
        buf = lines[i]
        while buf.rstrip().endswith("\\") and i + 1 < len(lines):
            buf = buf.rstrip()[:-1] + " " + lines[i + 1]
            i += 1
        yield start, buf
        i += 1


def tee_pipelines(src):
    """[(lineno, text)] for every REAL `... | tee ...` pipeline in `src`."""
    hits = []
    for lineno, text in logical_lines(src):
        if TEE_RE.search(code_of(text)):
            hits.append((lineno, text.strip()))
    return hits


def grep_tee(src):
    """[(lineno, text)] for the ticket's bare pattern -- comments included.

    Kept so k1 can report the bare grep's answer and the parsed answer side by
    side rather than silently substituting one for the other.
    """
    hits = []
    for i, line in enumerate(src.split("\n"), 1):
        if re.search(r"\|\s*tee\b", line):
            hits.append((i, line.strip()))
    return hits


SET_E_RE = re.compile(r"^\s*set\s+-[a-zA-Z]*e")
# mg-7522: was `^\s*set\s+-o\s+pipefail`, which matches ONE spelling of the
# option.  The single runner in the arc that sets it -- `code/state_restructure_
# 34bf/run_all.sh` -- writes `set -euo pipefail`, so this rule re-derived 0
# where the ticket said 1, `out_k1_census.txt` printed `DIFFERS`, and four
# reader-facing artifacts then reported the number as "confirmed exactly".
# The rule is now "a `set` builtin that enables the option, however spelled".
PIPEFAIL_RE = re.compile(r"^\s*set\s+[^#]*\bpipefail\b")


def has_set_e(src):
    return any(SET_E_RE.match(code_of(l)) for l in src.split("\n"))


def has_pipefail(src):
    return any(PIPEFAIL_RE.match(code_of(l)) for l in src.split("\n"))


# THE CALLER SCAN'S TARGET RULE, AS A PROPERTY.  mg-70c7, on mg-dee4's F5.
#
# `k2_consume.py` matched `run_all\.sh`; mg-7522 made it
# `(?:run_all|run_audit)\.sh`, which is one filename replaced by two.  At HEAD
# nine executing sites name a `*.sh` whose basename is neither -- four of them
# reading the exit status -- and nothing at all names the `run_audit.sh` the
# widening added.  THE PROPERTY IS "a shell script", not "a shell script with
# one of these names": what a runner is called is a fact about its author's
# habits, and an exit status is swallowed by whatever executes it.
#
# Group 1 is the directory component when the line carries one, group 2 the
# basename.  A target invoked as `./c0_repro.sh`, or as `"sh", "run_all.sh"`
# with the directory in a `cwd=` elsewhere, matches with NO group 1 -- the
# site is real and the tree is simply not on that line.  That is a stated
# limit of a line-local rule and not a name rule.
TARGET_RE = re.compile(r"(?:([\w./-]+)/)?(\w[\w-]*\.sh)\b")


def targets(line):
    """[(directory or '', basename)] -- every shell script this line names."""
    out, seen = [], set()
    for m in TARGET_RE.finditer(line):
        d, base = m.group(1) or "", m.group(2)
        if base in seen:
            continue
        seen.add(base)
        out.append((d, base))
    return out


GUARD_RE = re.compile(r"\|\||&&|\bif\b|;\s*then\b|\$\(")


def guarded(text):
    """True if this logical line's status is caught by an explicit construct.

    `cmd > out || { ...; exit 1; }`, `if cmd; then`, `X=$(cmd) || {...}`.
    """
    return bool(GUARD_RE.search(code_of(text)))


# ---------------------------------------------------------------------------
# the tree
# ---------------------------------------------------------------------------

def runners(ref=None):
    """Every `run_all.sh` in the repository, sorted.

    With `ref` (a git revision) the list and the sources come from that
    revision; without it, from the working tree.  Both are needed: the census
    must be re-derivable at the commit the ticket was written against as well
    as against the tree being repaired.
    """
    if ref:
        out = subprocess.run(["git", "-C", REPO, "ls-tree", "-r",
                              "--name-only", ref],
                             capture_output=True, text=True, check=True).stdout
        return sorted(p for p in out.split("\n")
                      if p.endswith("/run_all.sh") or p == "run_all.sh")
    found = []
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d != ".git"]
        if "run_all.sh" in files:
            found.append(os.path.relpath(os.path.join(root, "run_all.sh"),
                                         REPO))
    return sorted(found)


def read(rel, ref=None):
    if ref:
        return subprocess.run(["git", "-C", REPO, "show", "%s:%s" % (ref, rel)],
                              capture_output=True, text=True,
                              check=True).stdout
    with open(os.path.join(REPO, rel), encoding="utf-8") as fh:
        return fh.read()


# The commit the ticket's census was taken against.  Pinned, not `HEAD`:
# mg-821e's own finding was that a comparison anchored to HEAD stops comparing
# the moment the repair lands.
TICKET_REF = "bee07a1"


# ---------------------------------------------------------------------------
# the invocations inside a runner
# ---------------------------------------------------------------------------

INVOKE_RE = re.compile(
    r"(?:^|[;&|(]|\$\()\s*(?:python3?|sh|bash)\s+((?:-\w+\s+)*)([^\s;|&)]+)")


def invocations(text):
    """[(interpreter, script_path)] for every command this line launches."""
    got = []
    c = code_of(text)
    for m in re.finditer(
            r"(?:^|[;&|(]|\$\()\s*(python3?|sh|bash)\s+((?:-[a-zA-Z]+\s+)*)"
            r"([^\s;|&)]+)", c):
        got.append((m.group(1), m.group(3)))
    return got


def bar(title, ch="="):
    print(ch * 78)
    print(title)
    print(ch * 78)
