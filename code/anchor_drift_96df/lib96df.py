"""mg-96df shared library -- RELOCATING a line anchor by CONTENT, with the
match tier that earned each answer printed next to it.

WHY THIS EXISTS RATHER THAN A QUOTE OF mg-688c's TABLE.  mg-688c's POP-D
answered "does the line at N still carry the text the citing sentence names?"
with an EXACT comparison, and reported five of its nine sites as
`(text no longer present verbatim)`.  That predicate is correct and its
conclusion does not follow: this corpus's repair idiom is to APPEND a strike
and a warning TO the line rather than to replace it, so a line that gained
`~~...~~ WARNING` is byte-different and semantically the same line.  An exact
matcher meets that idiom and reports UNREPAIRABLE.

So the ladder below is ordered from strongest evidence to weakest and every
answer carries the rung it came off.  Nothing here decides that a relocation
is CORRECT -- it decides that a relocation is DETERMINATE, i.e. that exactly
one line at the new revision answers to the old one.  Ambiguity is a distinct
outcome from absence and is never silently resolved.

E1 (inherited from mg-cdd5's E1, and it is the same hazard): an instrument
about stale reads must not itself read a stale checkout.  Every content read
below is `git show <rev>:<path>` in the mirror repo.  There is NO code path in
this module that opens a file inside the mirror's working tree, and the mirror
is opened READ-ONLY -- no fetch, no checkout, no write.

E2: the revision this runs against is REPORTED, never assumed.  mg-688c's
table is pinned to 949c439 and says so; the defect it is about is exactly a
pinned answer outliving its pin.  `mirror_state()` reads the true remote and
the caller prints whether the measured ref is still the remote's `main`.
"""
import os
import re
import subprocess

MIRROR_NAME = "one_third_width_three"

#: Candidate roots for the cited repo, in order.  The environment variable
#: wins so a second host can run this without editing the file.  E4 (mg-cdd5's,
#: kept because this instrument also runs inside a polecat worktree whose
#: parent is /Users/daniel/.pogo/polecats and NOT ~/research): never resolve
#: the sibling repo by a relative path.
MIRROR_CANDIDATES = [
    os.environ.get("ONETHIRD_WIDTH_THREE"),
    os.path.expanduser("~/research/" + MIRROR_NAME),
]

#: The revision the citing authors actually read.  mg-cdd5 established this by
#: catching it in the act: STATE.md's two quoted anchors matched EXACTLY at
#: 912f1b1 and nothing at origin/main.  It is the mirror checkout's pre-repair
#: HEAD, and it is a HISTORICAL fact -- mg-cdd5 then fast-forwarded that branch
#: to 949c439, so this revision is reachable only by name, never off disk.
READ_REV = "912f1b1"

#: The revision mg-688c pinned its table to.  Carried so the run can say
#: whether it still equals the remote's main rather than assuming it does.
PINNED_REV = "949c439"


def here():
    return os.path.dirname(os.path.abspath(__file__))


def git(args, cwd):
    p = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def program_root():
    """This repository's root -- the worktree this instrument is committed in."""
    rc, out, err = git(["rev-parse", "--show-toplevel"], cwd=here())
    if rc != 0:
        raise RuntimeError("not in a git worktree: %s" % err.strip())
    return out.strip()


def find_mirror():
    for c in MIRROR_CANDIDATES:
        if not c:
            continue
        if os.path.exists(os.path.join(c, ".git")):
            return os.path.abspath(c)
    return None


class MirrorState(object):
    def __init__(self):
        self.path = None
        self.head = None
        self.branch = None
        self.origin_main = None
        self.remote_main = None
        self.error = None


def mirror_state():
    """Read the cited repo's commit state.  `ls-remote` READS the true remote;
    it moves nothing.  No fetch: a fetch mutates remote-tracking refs, and the
    honest statement is `the tracking ref agrees with the remote`, not `I
    refreshed it and then trusted it`."""
    st = MirrorState()
    st.path = find_mirror()
    if st.path is None:
        st.error = "cited repo %s not found" % MIRROR_NAME
        return st
    rc, out, err = git(["rev-parse", "HEAD"], cwd=st.path)
    if rc != 0:
        st.error = err.strip()
        return st
    st.head = out.strip()
    st.branch = git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=st.path)[1].strip()
    rc, out, _ = git(["rev-parse", "origin/main"], cwd=st.path)
    if rc == 0:
        st.origin_main = out.strip()
    rc, out, _ = git(["ls-remote", "origin", "refs/heads/main"], cwd=st.path)
    if rc == 0 and out.strip():
        st.remote_main = out.split()[0]
    return st


MISSING = object()      #: distinct from "" -- absence must never compare equal
                        #: to an empty file.


def blob_lines(repo, rev, path):
    """Lines of `path` at `rev`, or MISSING.  THE ONLY CONTENT READ HERE."""
    rc, out, _ = git(["show", "%s:%s" % (rev, path)], cwd=repo)
    if rc != 0:
        return MISSING
    return out.split("\n")


def line_at(lines, n):
    """1-indexed line `n`, or None if out of range."""
    if lines is MISSING or n < 1 or n > len(lines):
        return None
    return lines[n - 1]


# ---------------------------------------------------------------------------
# Normalisation.  Markdown inline markup is not content: a line that gained a
# bold marker is the same line.  Strike markup IS stripped to its contents --
# `~~X~~` normalises to `X` -- because a struck claim is still the claim, and
# an anchor pointing at it still resolves.  What is struck is reported
# separately (see `strike_added`) rather than silently absorbed.
# ---------------------------------------------------------------------------

_MARKUP = re.compile(r"[*_`~]+")
_WS = re.compile(r"\s+")


def norm(s):
    if s is None:
        return None
    return _WS.sub(" ", _MARKUP.sub("", s)).strip()


def strike_added(old, new):
    """True if `new` carries strike markup that `old` did not."""
    return ("~~" in (new or "")) and ("~~" not in (old or ""))


def prefix_key(o):
    """The part of a normalised line that a LATER revision can still be
    expected to open with.

    THE ONE CASE THIS EXISTS FOR, and it is the corpus's commonest line type.
    A markdown table row closes with `|`.  When this corpus withdraws a claim
    it appends the warning INSIDE the last cell, so the row's final `|` stays
    put and everything before it is unchanged:

        old   | ... | 0 / 132 |
        new   | ... | 0 / 132 - **SAMPLING ARTIFACT, NEVER QUOTABLE BARE.** |

    `new.startswith(old)` is FALSE there -- by one character, the closing
    delimiter -- so a naive prefix test rejects the very shape it was written
    to catch, and reports a row that plainly did not move as GONE.  Dropping
    the trailing delimiter is the whole of the concession, and matches are
    still required to be unique and >= MIN_PREFIX characters.

    (mg-cdd5 hit this and solved it by hand, quoting a "unique 74-character
    prefix" for exactly this row.  74 characters is this key.)
    """
    if o and o.endswith("|"):
        return o[:-1].rstrip()
    return o


# ---------------------------------------------------------------------------
# THE MATCH LADDER
# ---------------------------------------------------------------------------
#
# Rungs, strongest first.  Every rung requires UNIQUENESS: a rung that matches
# two lines yields AMBIGUOUS, not a guess.
#
#   SAME-LINE-EXACT     the old line is byte-identical at the SAME number
#   SAME-LINE-AMENDED   the same number still carries the old text as a
#                       prefix, with material appended (the corpus's repair
#                       idiom).  THE ANCHOR IS NOT BROKEN.
#   EXACT               byte-identical, unique, at a different number
#   NORMALISED          identical after markup/whitespace normalisation
#   PREFIX              exactly one line whose normalised form starts with the
#                       old normalised form (>= MIN_PREFIX chars of evidence)
#   CONTAINED           exactly one line containing the old normalised form
#   SAME-LINE-REWRITTEN the same number, sharing >= MIN_PREFIX characters of
#                       head with the old line but NOT a pure append -- the
#                       withdrawal rewrote the middle of the line.  THE ANCHOR
#                       IS NOT BROKEN AND THE QUOTATION IS.
#   GONE                no line answers to it
#   AMBIGUOUS           more than one does, at the rung that first fired
#
# MIN_PREFIX is 25 characters, taken from mg-cdd5's rule ("authorship is
# decided only by a quoted span, >= 25 characters") for the same reason: below
# that a table pipe and two words match half a document.

MIN_PREFIX = 25

#: The cited NUMBER still lands on the cited content.
TIERS_RESOLVING = ("SAME-LINE-EXACT", "SAME-LINE-AMENDED", "SAME-LINE-REWRITTEN")

#: Exactly one line at the new revision answers to the old one.
TIERS_DETERMINATE = ("SAME-LINE-EXACT", "SAME-LINE-AMENDED", "EXACT",
                     "NORMALISED", "PREFIX", "CONTAINED", "SAME-LINE-REWRITTEN")

#: The cited TEXT is still there, character for character modulo markup -- so a
#: citing sentence that QUOTES it is still quoting faithfully.  This is a
#: different question from whether the anchor resolves, and the two answers
#: come apart in both directions.
TIERS_VERBATIM = ("SAME-LINE-EXACT", "EXACT", "NORMALISED")


class Match(object):
    def __init__(self, tier, line=None, text=None, detail=""):
        self.tier = tier
        self.line = line
        self.text = text
        self.detail = detail

    @property
    def base(self):
        """The rung, with the range wrapper removed.  A range's verdict is the
        weakest rung any of its lines came off, so `BLOCK-PREFIX` is a PREFIX
        answer about a block -- and `BLOCK-PREFIX-PARTIAL`, `BLOCK-SPLIT`,
        `BLOCK-BROKEN` are not answers at all and must fall through every
        membership test below rather than half-match one of them."""
        t = self.tier
        return t[6:] if t.startswith("BLOCK-") else t

    @property
    def determinate(self):
        return self.base in TIERS_DETERMINATE

    @property
    def resolves(self):
        """The ORIGINAL number still lands on the cited content."""
        return self.base in TIERS_RESOLVING

    @property
    def verbatim(self):
        """The cited TEXT survives unchanged, so a quotation of it still holds."""
        return self.base in TIERS_VERBATIM


def _unique(hits):
    return hits[0] if len(hits) == 1 else None


def common_prefix_len(a, b):
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n


def relocate(old_lines, old_n, new_lines):
    """Where did line `old_n` of `old_lines` go in `new_lines`?"""
    old = line_at(old_lines, old_n)
    if old is None:
        return Match("SOURCE-ABSENT", detail="line %d not present at read rev" % old_n)
    o = norm(old)
    if not o:
        return Match("SOURCE-BLANK", detail="line %d is blank/markup-only" % old_n)

    key = prefix_key(o)

    def appended(new_line):
        return ("old text kept as a %d-char prefix; %d chars appended%s%s"
                % (len(key), len(norm(new_line)) - len(key),
                   "; strike added" if strike_added(old, new_line) else "",
                   "; trailing table delimiter ignored" if key != o else ""))

    same = line_at(new_lines, old_n)
    if same is not None:
        if same == old:
            return Match("SAME-LINE-EXACT", old_n, same)
        s = norm(same)
        if s == o:
            return Match("SAME-LINE-EXACT", old_n, same, "markup/whitespace only")
        if len(key) >= MIN_PREFIX and s.startswith(key):
            return Match("SAME-LINE-AMENDED", old_n, same, appended(same))

    idx = [(i + 1, ln) for i, ln in enumerate(new_lines)]

    hits = [(n, ln) for n, ln in idx if ln == old]
    if hits:
        m = _unique(hits)
        if m is None:
            return Match("AMBIGUOUS", detail="EXACT matched %d lines" % len(hits))
        return Match("EXACT", m[0], m[1])

    hits = [(n, ln) for n, ln in idx if norm(ln) == o]
    if hits:
        m = _unique(hits)
        if m is None:
            return Match("AMBIGUOUS", detail="NORMALISED matched %d lines" % len(hits))
        return Match("NORMALISED", m[0], m[1], "markup/whitespace only")

    if len(key) >= MIN_PREFIX:
        hits = [(n, ln) for n, ln in idx if norm(ln).startswith(key)]
        if hits:
            m = _unique(hits)
            if m is None:
                return Match("AMBIGUOUS", detail="PREFIX matched %d lines" % len(hits))
            return Match("PREFIX", m[0], m[1], appended(m[1]))

        hits = [(n, ln) for n, ln in idx if key in norm(ln)]
        if hits:
            m = _unique(hits)
            if m is None:
                return Match("AMBIGUOUS", detail="CONTAINED matched %d lines" % len(hits))
            return Match("CONTAINED", m[0], m[1], "old text embedded in a longer line")

    # Last rung, and the one the ComparisonRoute:104 shape needs.  The
    # withdrawal did not APPEND to that row, it rewrote the inside of its last
    # cell and pushed the surviving clause further along -- so the old text is
    # not a prefix of the new one, and no line anywhere carries it.  What IS
    # true is that line 104 is still the same table row: 79 identical leading
    # characters at the same number.  Reporting that as GONE is the error this
    # rung exists to stop, because "the anchor is fine and the QUOTATION is
    # stale" is a different repair from "the anchor moved".
    if same is not None:
        c = common_prefix_len(o, norm(same))
        if c >= MIN_PREFIX:
            return Match("SAME-LINE-REWRITTEN", old_n, same,
                         "same number, %d identical leading chars, then rewritten"
                         " (%d -> %d chars)%s"
                         % (c, len(o), len(norm(same)),
                            "; strike added" if strike_added(old, same) else ""))

    return Match("GONE", detail="no line at the new revision carries it")


def relocate_block(old_lines, first, last, new_lines):
    """Relocate a RANGE.

    A range is decided by CONSENSUS and then VERIFIED WHOLE, in that order,
    because deciding it line by line gets a cited paragraph wrong.  A quoted
    block of prose contains blank lines and one-word lines; those match
    everywhere or nowhere, and an all-lines-must-land rule therefore rejects
    ranges that plainly did move together.  (It did: the first version of this
    function reported the two ranges in this ticket BLOCK-BROKEN at their blank
    lines, having verified by hand that all sixteen lines of one of them are
    byte-identical 53 lines further down.)

    So: the lines that CAN be placed alone vote on an offset; a unique winner
    is then required to carry EVERY line of the range, blanks included.  A
    range that lands only in part is still refused -- a range whose first line
    moved and whose last did not is a worse answer than no answer.
    """
    span = list(range(first, last + 1))
    per = [(n, relocate(old_lines, n, new_lines)) for n in span]
    voters = [(n, m) for n, m in per if m.determinate]
    if not voters:
        return Match("BLOCK-BROKEN",
                     detail="no line of the %d-line range can be placed alone" % len(span))
    offsets = set(m.line - n for n, m in voters)
    if len(offsets) != 1:
        return Match("BLOCK-SPLIT", detail="lines vote for %d different offsets"
                     % len(offsets))
    off = offsets.pop()

    # Verify the whole range at the winning offset, blanks included.  The test
    # is CORRESPONDENCE, not equality: a line inside a quoted block may have
    # gained the same strike-and-warning suffix as any other, and demanding
    # byte equality there would reject the block for the one reason the ladder
    # exists to accept.
    def corresponds(o, s):
        if s is None:
            return False
        a, b = norm(o), norm(s)
        if a == b:
            return True
        k = prefix_key(a)
        return len(k) >= MIN_PREFIX and b.startswith(k)

    mismatched = [n for n in span
                  if not corresponds(line_at(old_lines, n), line_at(new_lines, n + off))]
    if mismatched:
        tiers = [m.tier for _, m in voters]
        worst = max(tiers, key=lambda t: TIERS_DETERMINATE.index(t))
        return Match("BLOCK-" + worst + "-PARTIAL", first + off,
                     line_at(new_lines, first + off),
                     "%d voters agree on offset %+d but %d of %d lines differ there "
                     "(first: %d)" % (len(voters), off, len(mismatched), len(span),
                                      mismatched[0]))
    tiers = [m.tier for _, m in voters]
    worst = max(tiers, key=lambda t: TIERS_DETERMINATE.index(t))
    return Match("BLOCK-" + worst, first + off,
                 line_at(new_lines, first + off),
                 "all %d lines land contiguously at offset %+d (%d could be placed "
                 "alone, and they agree)" % (len(span), off, len(voters)))


# ---------------------------------------------------------------------------
# Section anchors -- the DURABLE form.  mg-a1db, working inside the same hazard
# window, wrote: "Drifted hard refs :288/:310 deliberately not reused --
# section anchors used instead."  A section heading survives an inserted
# banner; a line number does not.  This finds the heading a line sits under so
# the durable form can be REPORTED beside the fragile one.
# ---------------------------------------------------------------------------

_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")


def enclosing_heading(lines, n):
    """(level, text, line) of the nearest heading at or above line `n`."""
    if lines is MISSING:
        return None
    for i in range(min(n, len(lines)), 0, -1):
        m = _HEADING.match(lines[i - 1])
        if m:
            return (len(m.group(1)), norm(m.group(2)), i)
    return None


def heading_is_unique(lines, text):
    """Is that heading text unique in the document?  A section anchor that
    names a heading occurring twice is no more durable than a line number."""
    if lines is MISSING:
        return False
    seen = 0
    for ln in lines:
        m = _HEADING.match(ln)
        if m and norm(m.group(2)) == text:
            seen += 1
    return seen == 1
