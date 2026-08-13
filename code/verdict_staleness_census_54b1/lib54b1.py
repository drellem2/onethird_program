"""mg-54b1 -- IS THIS TRANSCRIPT STALE IN THE STRONG SENSE?

mg-20ee's `ground_truth.sh` answers DIFFERS / REPRODUCES.  That is the WEAK
sense: any byte.  Its whole tranche exists because most of those bytes are
ADDRESSES -- a sha, a line number, a corpus size, a timing -- and pinning an
`AS_OF` commit removes them without any verdict having moved.

`code/species_extent_audit_6cb9` is the counter-example that separates the two
populations.  Three of its VERDICTS moved (`*** MISSED ***` -> `as predicted`,
`*** EXTENT WIDER ***` -> `extent TRUE here`, `A1 TOTAL BAD: 1` -> `0`), and it
carries no foreign address at all, so `census.py`'s classifier was never going
to nominate it and `ground_truth.sh` never asked it the question.

This module classifies a diff between a committed transcript and a fresh one:

    REPRODUCES        byte-identical
    DEAD              the fresh run raised; there is no comparable transcript
    VERDICT MOVED     at least one adjudication changed          <- the strong sense
    ADDRESSES ONLY    lines changed, no adjudication among them

TWO RULES DECIDE `VERDICT MOVED`, AND ONLY THE SECOND USES A VOCABULARY.

  RULE A -- A WORD CHANGED.  Erase from both sides of a changed line every
  token this corpus treats as an ADDRESS or a MAGNITUDE: worktree roots,
  repo-relative paths, sha-like hex, dates, clock times, durations, and then
  every remaining digit run.  If the line STILL differs, something that is not
  an address changed, and on a result line in these transcripts that is a
  verdict.  This rule names no verdict words, so it catches vocabularies
  nobody has enumerated -- `*** MISSED ***` -> `as predicted`, `ok` ->
  `*** FAILED ***`, `SILENT` -> `fired`, `[PASS]` -> `[FAIL]` -- and it cannot
  be defeated by an instrument that invents its own.

  RULE B -- A SCORED COUNTER CHANGED.  Rule A erases digits, so a verdict whose
  digit IS the verdict survives it: `TOTAL BAD: 1` -> `TOTAL BAD: 0` is a line
  that says nothing else.  SCORED_COUNTERS is the DECLARED, SHORT list of
  shapes where the number is the adjudication.  It is a vocabulary and is
  therefore the half of this classifier that can be blind; `c0_controls.py`
  holds it to its length and prints it, so growing it is visible.

  A `*** ... ***` marker or a `[TAG]` on an UNPAIRED added or removed line is
  also VERDICT MOVED: a finding that appeared or vanished is the strongest form
  of the thing being measured.

WHICH DIRECTION THIS ERRS, STATED.  Rule A erases addresses, so a diff whose
only change is WHICH FILE a finding is about reads as ADDRESSES ONLY --
under-counting.  Rule A also fires on any prose that changed beside a result,
which over-counts.  `classify.py` therefore prints the classifier's count AND
the quoted evidence line for every VERDICT MOVED, so a reader can do what
mg-20ee did to `census.py`: check the net against the catch.  Reporting the
number without the evidence would be quoting a net as if it were a catch.
"""

import re

# --- Rule A: what an ADDRESS or a MAGNITUDE looks like in this corpus. -------
# Order matters: paths before sha (a path can contain hex), sha before digits.
NORMALISERS = [
    (re.compile(r'/(?:Users|home|tmp|private|var)/[^\s,;:)\'"]*'), '<root>'),
    (re.compile(r'\b(?:code|docs|tests?)/[A-Za-z0-9_./+-]*'), '<path>'),
    (re.compile(r'\b[A-Za-z0-9_.+-]+\.(?:py|sh|md|txt|json|toml|yml|yaml)\b'), '<file>'),
    # An instrument's BARE directory name.  Every instrument under code/ is
    # `<topic>_<4 hex>`, and a census that lists them one per column carries
    # those names as ADDRESSES.  Without this, a sweep that gains a directory
    # because the branch added one reads as a word change -- measured on the
    # real diff of 417a789, whose own commit message says the verdict row did
    # not move.  R3 holds it.
    (re.compile(r'\b[a-z][a-z0-9]*(?:_[a-z0-9]+)*_[0-9a-f]{4}\b'), '<instr>'),
    (re.compile(r'\b[0-9a-f]{7,40}\b'), '<sha>'),
    (re.compile(r'\b\d{4}-\d{2}-\d{2}(?:T[\d:.]+Z?)?\b'), '<date>'),
    (re.compile(r'\b\d{1,2}:\d{2}(?::\d{2})?\b'), '<time>'),
    (re.compile(r'\b\d+(?:\.\d+)?\s?(?:s|ms|sec|secs|seconds|min|mins|h)\b'), '<dur>'),
    (re.compile(r'\d+'), '<n>'),
]

# --- Rule B: the DECLARED shapes where the NUMBER is the adjudication. -------
# Each entry is (name, compiled pattern).  The pattern's groups are the scored
# part.  Every one of these is a real line shape in this corpus; the count of
# sites is printed by c0_controls.py so that adding a seventh is not silent.
SCORED_COUNTERS = [
    ("TOTAL BAD",      re.compile(r'TOTAL BAD:\s*(\d+)')),
    ("assertions",     re.compile(r'(\d+)\s+assertion\(s\),\s*(\d+)\s+failed')),
    ("failure tally",  re.compile(r'(\d+)\s+(?:failed|BROKEN|unsatisfactory|'
                                  r'bad|wrong|refuted|disagree)\b')),
    # The noun is REQUIRED.  Written as `VERDICT:[^0-9]*(\d+)` this entry read
    # the `0` of `VERDICT: CLEAN  0.11s` as a scored counter, so a run that got
    # 0.03 s slower reported a moved verdict -- a MAGNITUDE counted as a
    # finding, on the exact line shape mg-f771's W3 declares NOISE, inside the
    # rule written to keep magnitudes out.  Found by probing this list against
    # the negative worlds rather than by a world failing.  N8 holds it.
    ("VERDICT count",  re.compile(r'VERDICT:.*?\b(\d+)\s+[A-Za-z]+\(s\)')),
    ("fired ratio",    re.compile(r'(?:INSIDE|OUTSIDE)\s+(\d+)\s*/\s*(\d+)\s+'
                                  r'(?:fired|silent)')),
    ("found wrong",    re.compile(r'FOUND\s+(\d+)\s+THING')),
]

MARKER = re.compile(r'\*\*\*[^*]+\*\*\*')
TAG = re.compile(r'\[[A-Z][A-Z0-9 _-]*\]')
TRACEBACK = "Traceback (most recent call last):"
# mg-f771's watched class, verbatim: every tracked file under code/ named out_*.txt.
TRANSCRIPT = re.compile(r'code/.*/out_[^/]*\.txt$')


# The placeholders that stand for an ADDRESS.  `<n>` is deliberately NOT here:
# see `residue`.
ADDRESS_PLACEHOLDERS = re.compile(r'<(?:root|path|file|instr|sha|date|time|dur)>')
PUNCT = re.compile(r'[^A-Za-z<>]+')


def normalise(line):
    """Rule A's erasure.  Returns the line with every address and magnitude gone."""
    for pat, rep in NORMALISERS:
        line = pat.sub(rep, line)
    return line.strip()


def residue(line):
    """What is left of a line when every ADDRESS is deleted rather than marked.

    `normalise` replaces an address with a placeholder, which keeps its
    POSITION.  A census line that lists one entry per instrument therefore
    still differs when the corpus gains a directory -- every later placeholder
    shifts -- and that read as a moved verdict.  Measured on the real diff of
    417a789, whose commit message says the row that scores stayed at 27.

    Deleting the placeholders instead compares only the words, so a listing
    that gained an address is equal on both sides while `ok` -> `FAILED` is
    not.  `<n>` is NOT deleted, because a count is not always an address --
    which is what RULE B is for, and what §5's named miss is about.
    """
    return PUNCT.sub(' ', ADDRESS_PLACEHOLDERS.sub('', normalise(line))).strip()


def scored(line):
    """Rule B.  Returns the tuple of scored numbers this line carries, by name."""
    out = []
    for name, pat in SCORED_COUNTERS:
        for m in pat.finditer(line):
            out.append((name, m.groups()))
    return tuple(out)


def verdict_signature(line):
    """Everything about a line that is an ADJUDICATION and not an address."""
    return (residue(line), scored(line))


def moved(old, new):
    """Did a verdict move between these two lines?  (bool, why)"""
    so, sn = verdict_signature(old), verdict_signature(new)
    if so[0] != sn[0]:
        return True, "RULE A: a word changed"
    if so[1] != sn[1]:
        return True, "RULE B: a scored counter changed"
    return False, ""


def unpaired_is_verdict(line):
    """An added or removed line with no partner.  Is it an adjudication?"""
    if MARKER.search(line):
        return True, "RULE A: a *** marker *** line appeared or vanished"
    if TAG.search(line):
        return True, "RULE A: a [TAG] row appeared or vanished"
    if scored(line):
        return True, "RULE B: a scored counter line appeared or vanished"
    return False, ""


def parse_hunks(diff_text):
    """Split a unified diff into (path, [(minus_lines, plus_lines)]) per file."""
    files, path, hunks, minus, plus = {}, None, [], [], []

    def flush():
        if minus or plus:
            hunks.append((list(minus), list(plus)))
        del minus[:], plus[:]

    for line in diff_text.splitlines():
        if line.startswith("diff --git "):
            flush()
            if path:
                files.setdefault(path, []).extend(hunks)
            hunks = []
            path = line.split(" b/")[-1]
        elif line.startswith("@@"):
            flush()
        elif line.startswith("-") and not line.startswith("---"):
            if plus:                       # a new run of minuses starts a new pair
                flush()
            minus.append(line[1:])
        elif line.startswith("+") and not line.startswith("+++"):
            plus.append(line[1:])
        else:
            flush()
    flush()
    if path:
        files.setdefault(path, []).extend(hunks)
    return files


def classify_file(diff_text_for_file):
    """[(minus, plus)] hunks for ONE file -> (verdict_moved, [evidence])."""
    evidence = []
    for minus, plus in diff_text_for_file:
        for i in range(max(len(minus), len(plus))):
            o = minus[i] if i < len(minus) else None
            n = plus[i] if i < len(plus) else None
            if o is not None and n is not None:
                yes, why = moved(o, n)
                if yes:
                    evidence.append((why, o.strip(), n.strip()))
            else:
                line = o if o is not None else n
                yes, why = unpaired_is_verdict(line)
                if yes:
                    evidence.append((why,
                                     line.strip() if o is not None else "",
                                     line.strip() if n is not None else ""))
    return (len(evidence) > 0), evidence


def classify_diff(diff_text, fresh_text=""):
    """Whole-repo diff -> (class, {path: evidence}).

    `fresh_text` is the concatenated fresh output, used only for DEAD.
    """
    if TRACEBACK in diff_text or TRACEBACK in fresh_text:
        return "DEAD", {}
    if not diff_text.strip():
        return "REPRODUCES", {}
    per_file, any_moved = {}, False
    for path, hunks in parse_hunks(diff_text).items():
        # THE POPULATION IS TRANSCRIPTS, and mg-f771's watched class is its
        # definition: tracked files under code/ named out_*.txt.  A runner that
        # rewrites its own SOURCE is a different finding and is not this one --
        # without this line the classifier reported reworded code comments as
        # moved verdicts, measured on the real diff of 13df87b.
        if not TRANSCRIPT.match(path):
            continue
        yes, ev = classify_file(hunks)
        if yes:
            any_moved = True
            per_file[path] = ev
    return ("VERDICT MOVED" if any_moved else "ADDRESSES ONLY"), per_file
