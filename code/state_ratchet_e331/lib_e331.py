"""mg-e331 — the measurement and the rule, shared by the ratchet, the characterisation and
the positive control.

THE ONE DEFINITION OF SIZE IS HERE AND NOWHERE ELSE.  Three producers in this directory
report a word count and a fourth (`negative_control_e331.py`) mutates one; if any of them
computed it locally, this instrument could pass its own probes while the gate read a
different number.  `measure()` is the single site.  E4 in PREDICTIONS.md stands: a word count
is a proxy for what a reader must read, not the thing itself.

WHY THE WORKING TREE AND NOT THE COMMIT.  `read_state()` reads `STATE.md` off disk.  The
refinery runs the gate on the REBASED TREE — a working tree that exists at no commit — and a
probe that answers `git show HEAD:STATE.md` is answering a question nobody asked.  mg-d19f's
D1 is exactly that defect (a committed-state probe answering a working-tree question, green
at every moment before the commit), and mg-724a's live run turned up its sibling: the gate
observed a count this worktree could not, because someone else's branch had landed.  The
characteriser and the positive control DO read commits, because their subject IS history;
they say so at each call site.
"""

import json
import os
import re
import subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
STATE = os.path.join(ROOT, "STATE.md")
CEILING_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CEILING.json")

# mg-ea0e's own stated target and the two readings that bracket this ticket.  These are
# LITERALS OF RECORD — they are what other documents say — and they are never used as a
# threshold.  The threshold is CEILING.json and only CEILING.json.
EA0E_TARGET_WORDS = 6000
EA0E_LANDED = ("cc4c663e8", 32772, 4658)          # the restructure's own landing
EA0E_PARENT = ("b80dea0ec", 186710, 29094)        # the file it replaced


class Refusal(Exception):
    """This instrument could not reach its own decision.  Never mapped onto a verdict."""


# ---------------------------------------------------------------------------------------
# measurement
# ---------------------------------------------------------------------------------------

def measure(text):
    """The single definition of STATE.md's size.  `words` is the gated quantity."""
    if not isinstance(text, str):
        raise Refusal("measure() was handed %r, not text" % type(text).__name__)
    lines = text.split("\n")
    return {
        "bytes": len(text.encode("utf-8")),
        "words": len(text.split()),
        "lines": len(lines),
        "max_line_chars": max((len(l) for l in lines), default=0),
        "lines_over_2000": sum(1 for l in lines if len(l) > 2000),
    }


def read_state():
    """The WORKING TREE STATE.md — see this module's docstring for why, not the commit."""
    try:
        with open(STATE, encoding="utf-8") as fh:
            return fh.read()
    except OSError as exc:
        # THE PATH IS REPOSITORY-RELATIVE, AND ABSOLUTE IS AN OPERATOR-VALUED TRANSCRIPT
        # (mg-bdb0, on mg-4020's finding and mg-1344's rule).  `STATE` is absolute, so N14's
        # committed row read `cannot read /Users/<someone>/.pogo/polecats/p92xx/STATE.md` —
        # a transcript that reproduces for exactly ONE operator and for nobody else, ever.
        # mg-4020 found the class, mg-1344 repaired out_gate.txt's S1 row the same way and
        # left this one alone BECAUSE ITS BRANCH ONLY MOVED THE TIMING and re-pointing it
        # would have swapped one polecat for another and bought nothing.  This branch moves
        # the row's CONTENT — 5,987 words become 4,851 — so the file has to be committed, and
        # committing it with an absolute path would plant the defect on behalf of every later
        # operator instead of leaving it where it was.  That is mg-1344's own reasoning about
        # its own transcript, applied to the file it explicitly named as still carrying this.
        try:
            shown = os.path.relpath(STATE, ROOT)
        except ValueError:
            shown = STATE
        raise Refusal("cannot read %s: %s\nThe subject of this ratchet is absent, which is "
                      "neither green nor red." % (shown, exc))


def show(rev, path="STATE.md"):
    """A file AT A COMMIT.  Only for producers whose subject is history."""
    p = subprocess.run(["git", "-C", ROOT, "show", "%s:%s" % (rev, path)],
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise Refusal("git show %s:%s failed: %s" % (rev, path, p.stderr.strip()))
    return p.stdout


def git(*args):
    p = subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True, text=True)
    if p.returncode != 0:
        raise Refusal("git %s failed: %s" % (" ".join(args), p.stderr.strip()))
    return p.stdout


# ---------------------------------------------------------------------------------------
# the declared ceiling
# ---------------------------------------------------------------------------------------

REQUIRED = ("words_ceiling", "tighten_below", "why", "set_by", "set_at_words")


def load_ceiling(path=None):
    path = path or CEILING_PATH
    try:
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
    except OSError as exc:
        raise Refusal("cannot read the declared ceiling at %s: %s" % (path, exc))
    return parse_ceiling(raw, path)


def parse_ceiling(raw, path="<text>"):
    try:
        obj = json.loads(raw)
    except ValueError as exc:
        raise Refusal("%s is not JSON: %s\nA ratchet whose threshold cannot be read must "
                      "refuse, not default." % (path, exc))
    if not isinstance(obj, dict):
        raise Refusal("%s is %s, not an object" % (path, type(obj).__name__))
    missing = [k for k in REQUIRED if k not in obj]
    if missing:
        raise Refusal("%s is missing required field(s): %s\nA ceiling with no `why` is a "
                      "number nobody can argue with later." % (path, ", ".join(missing)))
    for k in ("words_ceiling", "tighten_below", "set_at_words"):
        if not isinstance(obj[k], int) or isinstance(obj[k], bool) or obj[k] < 0:
            raise Refusal("%s: %s is %r, not a non-negative integer" % (path, k, obj[k]))
    if not str(obj["why"]).strip():
        raise Refusal("%s: `why` is empty.  See REQUIRED in lib_e331.py." % path)
    if obj["tighten_below"] > obj["words_ceiling"]:
        raise Refusal("%s: tighten_below (%d) is above words_ceiling (%d), so EVERY value is "
                      "simultaneously too big and too small and the rule has no green band."
                      % (path, obj["tighten_below"], obj["words_ceiling"]))
    return obj


# ---------------------------------------------------------------------------------------
# the rule
# ---------------------------------------------------------------------------------------

GREEN, ABOVE, SLACK = "GREEN", "ABOVE-CEILING", "SLACK-UNRATCHETED"


def verdict(words, ceiling):
    """RED IN EITHER DIRECTION, which is mg-724a's rule and not a new one.

    ABOVE  — the file grew past the declared ceiling.  This is the regression.
    SLACK  — the file is materially BELOW the ceiling and the ceiling was left where it was.
             A ceiling far above its subject is a decorative check, and a restructure that
             cuts 150 KB without lowering the number it is measured against is mg-ea0e
             happening again with a control watching it happen.
    """
    if not isinstance(words, int) or isinstance(words, bool) or words < 0:
        raise Refusal("verdict() was handed words=%r" % (words,))
    cap, floor = ceiling["words_ceiling"], ceiling["tighten_below"]
    if words > cap:
        return ABOVE, ("%d words is %+d past the declared ceiling of %d"
                       % (words, words - cap, cap))
    if words < floor:
        return SLACK, ("%d words is %d below the declared ceiling of %d, past the %d-word "
                       "tighten point" % (words, cap - words, cap, floor))
    return GREEN, "%d words, ceiling %d, tighten below %d" % (words, cap, floor)


REMEDY = """\
WHAT TO DO — and both branches are a one-line diff in THIS commit, never a later one.

  ABOVE-CEILING.  Either the bytes belong somewhere else — `docs/state-history/` is the
  destination mg-ea0e created for exactly this and it already holds 9 attempt-*.md files — in which case
  move them and leave a pointer; or the growth is right, in which case RAISE `words_ceiling`
  in CEILING.json IN THIS COMMIT and write the reason into `why`.  What is not available is
  landing the growth and leaving the declared size behind it.  That is the whole of what this
  ratchet buys and it is the thing mg-ea0e did not have.

  SLACK-UNRATCHETED.  You made the file smaller.  LOWER `words_ceiling` to what you achieved,
  in this commit, and set `set_at_words` to the same number.  A cleanup that does not move the
  ceiling has bought four days, which is measured: mg-34bf cut 28,321 bytes on 2026-07-30 and
  the file was back eight hours later; mg-ea0e cut 153,938 and it was 59% back in four days.
"""


# ---------------------------------------------------------------------------------------
# section decomposition — used by the characteriser and RECORDED by the ratchet
# ---------------------------------------------------------------------------------------

HEADING = re.compile(r"^(#{1,6}) (.*)$")


def sections(text):
    """Ordered [(heading, bytes, words)].  The heading text is the key; a renamed heading is
    a new section and the characteriser reports it as one rather than guessing at identity."""
    cur, agg, order = "(preamble)", {}, ["(preamble)"]
    for line in text.split("\n"):
        m = HEADING.match(line)
        if m:
            cur = m.group(2).strip()
            if cur not in agg:
                order.append(cur)
        a = agg.setdefault(cur, [0, 0])
        a[0] += len(line.encode("utf-8")) + 1
        a[1] += len(line.split())
    return [(k, agg[k][0], agg[k][1]) for k in order if k in agg]


TABLE_SEP = re.compile(r"^\s*\|[\s:|-]+\|\s*$")


def table_rows(text, heading, key_cell):
    """Rows of the markdown table under `heading`, keyed on cell `key_cell`.

    THE KEY IS LOAD-BEARING AND IT IS NOT THE WHOLE ROW.  Keying on the row's bytes makes
    every edited row a delete plus an insert, and the question this instrument exists to
    answer — did the section grow by GAINING ROWS or by ROWS GETTING LONGER — is then
    unanswerable by construction.  mg-2ff6 lost a figure to the mirror error (a key too
    coarse, merging two rows into one).  Keys are truncated so that a row which grew is still
    the same row; a row whose FIRST 60 characters changed is reported as new, and the
    characteriser prints the key set so that is visible rather than silent.
    """
    out, inside = {}, False
    for line in text.split("\n"):
        if HEADING.match(line):
            inside = line.startswith(heading)
            continue
        if not inside or not line.startswith("|") or TABLE_SEP.match(line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) <= key_cell:
            continue
        out[cells[key_cell][:60]] = len(line)
    return out
