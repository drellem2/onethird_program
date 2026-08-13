"""mg-f771 — shared plumbing for the gate's own fixed point.

THE SUBJECT IS A COMMITTED REPORT THAT DISAGREES WITH THE REPO IT DESCRIBES.
`code/facts_registry_03cf/out_f0_registry_discipline.txt`, as committed at 1d89a29, ended
`VERDICT: GREEN — 20 entries` about a registry that has 23 (F21, F22 and F23 are on main).
The file is quoted, so a stale one is a REPORT and not a build artifact, and the part
written to be quotable was the wrong half.

THE NORMALISER IS THE WHOLE DESIGN, AND IT IS NARROW ON PURPOSE.  The obvious repair is
"fail the merge when a regenerated output differs from its committed copy", and it is
IMPOSSIBLE AS STATED: these transcripts are NOT a pure function of repo state.  Measured on
one gate run in this worktree, four of the seven files the gate re-dirtied differed only in
wall-clock timings (`36.4s` -> `30.7s`, `0.17s` -> `0.31s`, `13.5s` -> `14.0s`) and in
ABSOLUTE WORKTREE PATHS (`/Users/daniel/.pogo/polecats/p28b6/...` -> `.../pf771/...`).  The
path half is fatal on its own: the same repo state produces different bytes in every
polecat worktree, by construction, so a byte-comparison gate would be RED on every merge
from every worktree forever.  A gate that can never be green is worse than no gate.

So exactly two families of difference are declared NOT to be a function of repo state, and
NOTHING ELSE IS:

    N1  ABSOLUTE PATHS to a checkout of this repository -> `<ROOT>`.  Only the root is
        eaten; the tail is compared verbatim, so `<ROOT>/code/g/BASELINE.json.no-such-file`
        still differs from `<ROOT>/code/g/BASELINE.json.OTHER` (world W6).  Two shapes,
        because a transcript may cut the path at a column limit before the tail begins:
        N1a matches the prefix that sits in front of a repo-relative entry and keeps the
        tail; N1b eats whatever absolute path is left, which is the TRUNCATED case
        (`cannot read /Users/daniel/.pogo/polecats/p28`, world W5).  BOTH EMIT THE SAME
        MARKER on purpose -- see N3.
    N2  DECIMAL SECONDS (`36.4s`, `0.55 s`) -> `<t>s`.  Integers are NOT eaten: `12 groups`
        and `20 entries` are counts and are graded (worlds W1, W2, W9).
    N3  ON A LINE CONTAINING `<ROOT>`, THE SHORTER OF THE TWO IS ALLOWED TO BE A PREFIX OF
        THE LONGER.  This is the third rule and it was NOT in the first version; it was
        added after THE REFINERY REFUSED THIS VERY BRANCH.  The refinery does not merge in
        a polecat worktree -- it clones to
        `/Users/daniel/.pogo/refinery/worktrees/onethird_program`, 54 characters against a
        polecat worktree's 34.  A line that embeds an absolute path AND is cut at a fixed
        column therefore loses FIFTEEN MORE CHARACTERS OF ITS TAIL in the refinery than in
        the worktree the bytes were committed from: `...no-such-file is missing.  A gate`
        against `...no-such-file is missin`.  No root-substitution can repair that, because
        what differs is how much of the line survived, and that is a function of WHERE THE
        CHECKOUT LIVES.  So on such lines only the common prefix is compared.  It is the
        weakest of the three rules and the cost is stated: a change that only SHORTENS a
        line after the path reads as noise (world W12, green on purpose).  A change that
        alters the tail before the cut is still caught, which is what keeps W6 alive.

A WIDER NORMALISER IS AN UNFALSIFIABLE ESCAPE HATCH — an operator facing a real
disagreement can silence it by widening the rule, and nothing in the machinery tells that
edit from a correct one.  That is mg-479c's P6 in this file's own subject matter, and the
only defence offered here is that `g1_controls.py` plants six worlds the normaliser MUST
NOT swallow and three it MUST, and that the three it must are named rather than discovered.

WHAT IS WATCHED: every tracked file under `code/` whose basename starts with `out_` and
ends `.txt`.  Not a hardcoded list — a new gate suite is covered the day it lands.  It is
also why this control never touches `code/libweak_audit_c4f5/out_a4_census.txt` (mg-c824),
which must NOT be regenerated: this instrument regenerates nothing.  It compares the
worktree to the committed copy, and a file nothing rewrites is never modified, so it is
never flagged.  STATE.md and docs/ are outside the watched set too, so a human editing them
with the gate running does not trip a control about transcripts.
"""

import difflib
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

# The handshake described in README §3.  This control's question — "does the gate have a
# fixed point?" — is a question about a gate RUN, so asking it without one is a category
# error and the answer is a refusal, not a green.
FRESH_ENV = "BUILD_SH_RAN_THE_SUITES"

ROOT_MARK = "<ROOT>"

# N1.  THE FIRST VERSION ENUMERATED THE CHECKOUT SHAPES IT KNEW -- `.pogo/polecats/<name>`
# and `research/onethird_program` -- AND THE REFINERY REFUSED THE BRANCH, because it merges
# in a third one, `.pogo/refinery/worktrees/onethird_program`, that the enumeration had
# never seen.  A list of known roots is a list of the places somebody has already looked.
# So the shape is no longer enumerated: N1a is "an absolute path that runs into a
# repo-relative entry", which is what a checkout root IS, and the tail after it is kept.
FS_ROOTS = r"(?:Users|home|var|private|tmp|opt|mnt|srv|data|workspace)"
ABS_TO_REPO = re.compile(
    r"/" + FS_ROOTS + r"/[^\s:'\"]*?(?=/(?:code/|docs/|STATE\.md|build\.sh))")
# N1b.  Whatever absolute path is left -- i.e. one CUT before its repo-relative tail began.
# It emits the SAME marker as N1a rather than a distinguishable one, so that a cut path and
# an uncut one on the same line stay prefix-comparable under N3.
ABS_ANY = re.compile(r"/" + FS_ROOTS + r"/[^\s:'\"]*")

# N2.  A decimal second.  `\bs\b` and not `s` so that `10.5seconds` is untouched.
SECONDS = re.compile(r"\b\d+\.\d+\s*s\b")


class Refused(Exception):
    """Raised when this instrument cannot reach a verdict, which is not a finding."""


def normalise(text):
    """Erase N1 and N2, and nothing else.  Pure string -> string, so the controls can
    exercise it without a git repository or a sandbox."""
    text = text.replace(ROOT, ROOT_MARK)
    text = ABS_TO_REPO.sub(ROOT_MARK, text)
    text = ABS_ANY.sub(ROOT_MARK, text)
    text = SECONDS.sub("<t>s", text)
    return text


def lines_equivalent(la, lb):
    """N3.  Equal, or -- on a line that embeds a checkout path -- the shorter is a prefix
    of the longer, because a column-truncated line loses a different amount of its tail
    depending on how long the path in front of it was."""
    if la == lb:
        return True
    if ROOT_MARK not in la or ROOT_MARK not in lb:
        return False
    n = min(len(la), len(lb))
    return la[:n] == lb[:n]


def texts_equivalent(a, b):
    """N3 over a whole file.  A DIFFERENT NUMBER OF LINES IS NEVER EQUIVALENT: the defect
    that opened this ticket was three INSERTED registry rows, and pairing lines across an
    insertion would compare F21 against a blank and call the file unchanged further down."""
    la, lb = a.splitlines(), b.splitlines()
    if len(la) != len(lb):
        return False
    return all(lines_equivalent(x, y) for x, y in zip(la, lb))


def verdict_for(committed, worktree):
    """The decision, isolated so that `g1_controls.py` tests THIS and not a re-spelling.

    AGREES     the bytes are identical.
    NOISE      they differ only in the declared non-repo-state families.
    DISAGREES  the committed copy asserts something this tree contradicts.  RED.
    """
    if committed == worktree:
        return "AGREES"
    a, b = normalise(committed), normalise(worktree)
    if a == b or texts_equivalent(a, b):
        return "NOISE"
    return "DISAGREES"


# THE ONE EXEMPTION, AND IT IS ONE FILE RATHER THAN THIS DIRECTORY.
#
# `g0` writes its own transcript AFTER taking its measurement, and the transcript's content
# depends on the verdict.  So committing a red run's transcript necessarily banks the text
# "RED, N disagreements" alongside the refresh that makes the tree green — and the NEXT run
# reads that committed copy against a green one and grades it DISAGREES.  An innocent branch
# then goes red for a non-reason, which is this ticket's own thesis shipped inside its
# remedy (mg-479c E9).  Measured over five runs, not anticipated: the oscillation is in
# README D4, and it does not damp, because each run's fix is the next run's disagreement.
#
# `out_g1_controls.txt` is NOT exempt and the difference is the point: its content depends on
# the planted worlds, i.e. on code, not on tree state.  Committing the output of the run that
# changed it is stable, so it converges the way every other transcript does.  Verified as
# worlds E1-E3 in g1_controls.py, so the exemption cannot silently widen to the directory.
SELF_EXCLUDED = ("code/gate_fixed_point_f771/out_g0_fixed_point.txt",)


def is_transcript(relpath):
    """The transcript class: a tracked out_*.txt under code/."""
    return (relpath.startswith("code/")
            and os.path.basename(relpath).startswith("out_")
            and relpath.endswith(".txt"))


def is_watched(relpath):
    """The watched class: a transcript, less the one file whose self-reference makes the
    question unanswerable rather than merely awkward."""
    return is_transcript(relpath) and relpath not in SELF_EXCLUDED


def _git(root, *args):
    try:
        p = subprocess.run(("git", "-C", root) + args,
                           capture_output=True, text=True)
    except OSError as exc:                                  # pragma: no cover - no git
        raise Refused("git is not runnable: %s" % exc)
    return p


def require_git(root=ROOT):
    p = _git(root, "rev-parse", "--is-inside-work-tree")
    if p.returncode != 0 or p.stdout.strip() != "true":
        raise Refused("%s is not inside a git work tree; this control reads the COMMITTED "
                      "copy from git and cannot reach a verdict without one" % root)


def changed_transcripts(root=ROOT):
    """Tracked transcripts under code/ that differ from their committed copy at HEAD.

    `git diff --name-only HEAD` and not `git status`, because the question is "does the
    committed copy disagree", and a file that is staged but not committed is still a file
    whose committed copy disagrees.
    """
    require_git(root)
    p = _git(root, "diff", "--name-only", "HEAD", "--", "code")
    if p.returncode != 0:
        raise Refused("git diff --name-only HEAD failed: %s" % p.stderr.strip())
    return sorted(r for r in p.stdout.splitlines() if r and is_watched(r))


def committed_text(relpath, root=ROOT):
    p = _git(root, "show", "HEAD:%s" % relpath)
    if p.returncode != 0:
        raise Refused("cannot read HEAD:%s — a watched transcript with no committed copy "
                      "is a question this control cannot answer" % relpath)
    return p.stdout


def worktree_text(relpath, root=ROOT):
    try:
        with open(os.path.join(root, relpath), "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError as exc:
        raise Refused("cannot read %s: %s" % (relpath, exc))


def first_disagreement(committed, worktree, limit=8):
    """The normalised lines that differ, so the transcript SHOWS the disagreement rather
    than asserting one.  Reported on the normalised text: quoting the raw lines would put
    a worktree path into a tracked transcript and re-create the defect being measured.

    A real diff and not a positional line-by-line walk.  An INSERTED entry -- which is the
    exact shape of the defect that opened this ticket, three new registry rows -- shifts
    every following line, and a positional walk reports the shift instead of the insertion.
    Returns (mark, text) where mark is '-' for the committed copy and '+' for this tree,
    truncated to `limit` hunk lines with a count of what was dropped, because a silent
    truncation reads as 'that was all of it'.
    """
    a = normalise(committed).splitlines()
    b = normalise(worktree).splitlines()
    # Do not report pairs N3 already forgave, or the transcript names lines the verdict
    # did not count -- a report that lists more than it graded is read as the grading.
    if len(a) == len(b):
        for i, (x, y) in enumerate(zip(list(a), list(b))):
            if x != y and lines_equivalent(x, y):
                a[i] = b[i] = x if len(x) < len(y) else y
    rows = []
    for ln in difflib.unified_diff(a, b, lineterm="", n=0):
        if ln.startswith(("---", "+++")):
            continue
        if ln.startswith("@@"):
            rows.append(("@", ln.strip()))
        elif ln[:1] in ("-", "+"):
            rows.append((ln[0], ln[1:].rstrip()))
    dropped = max(0, len(rows) - limit)
    return rows[:limit], dropped
