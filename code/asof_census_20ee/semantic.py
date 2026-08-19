#!/usr/bin/env python3
"""SEMANTIC -- WHICH OF THIS ESTATE'S DECLARED LIMITS ARE DATE QUESTIONS, AND
THE TWO THAT PROVABLY ARE NOT.

mg-0bf1 corrected mg-e8b0's account of its own remedy.  N28 said that telling a
sentence ACCOUNTING for a pin from one OFFERING the same instrument as remaining
work would take a rule about English; it takes a DATE, because an accounting is
necessarily younger than the pin and an offer is older.  That tranche closed with
one question and this file is the answer to it:

    IS ANY REMAINING `READ WHAT THE SENTENCE SAYS` RULE IN THIS ESTATE LIKEWISE A
    DATE QUESTION WEARING SEMANTIC CLOTHES?

THE ANSWER IS YES FOR ONE MORE AND PROVABLY NO FOR TWO, AND THE INTERESTING HALF
IS THE NO.  A limit is not shown to need English by nobody having found a rule --
that is an absence of evidence, and this arc does not publish those.  It is shown
by a COLLISION WITNESS: two real lines in the estate whose readings are opposite
and whose commit is THE SAME.  Every commit-level field -- sha, date, author,
order index, what landed before and after -- is then literally identical across
the two readings, so NO rule reading any of them can separate the pair.  That is
an impossibility rather than a failure to find something, which is the only thing
a rule can have (out_exemplars.txt section 2, one field along).

--------------------------------------------------------------------------------
1.  ONE RULE, FOUR ROWS
--------------------------------------------------------------------------------

Every row of section 2 is the same question asked of a different declared limit:

    Given two witnesses whose readings are opposite, and an EVENT in the
    repository that one reading puts before them and the other after --
    does the event lie strictly between the witnesses in commit order?

  * The witnesses share a commit          -> COLLIDES.  No event can lie strictly
                                             between them.  PROVED, and this is
                                             the direction that proves.
  * The row's field separates them        -> SEPARATED.  Proves only that this
                                             field decides THESE two; it is a
                                             candidate rule, not a theorem.
  * Neither                               -> NOT SEPARATED, which proves nothing.

ONE-DIRECTIONAL, AND THE DIRECTION IS THE OPPOSITE OF exemplars.py's.  There the
rule FIRING was the informative answer; here it is the rule FAILING TO SEPARATE.
Both files publish the direction their evidence can actually carry.

--------------------------------------------------------------------------------
2.  WHERE THE CLASS LABELS COME FROM, WHICH IS NOT FROM ME
--------------------------------------------------------------------------------

A collision witness is worth nothing if the two readings are the author's opinion.
So each row's labels are taken from the record that DECLARED the limit -- aaf4's
section 7 names its own MENTION unit, this directory's N28 names its own two
sentences -- and the declaration is CHECKED PRESENT at AS_OF, printed with its
file, so a row whose declaration has been deleted reads GONE instead of standing
as a claim about a document that no longer says it.

    AND THE SENTENCES THEMSELVES ARE PRINTED.  N28's declared remedy for a rule
    that cannot read English is that THE INSTRUMENT PRINTS THE SENTENCE, and this
    file is the fourth instrument in the arc to have that obligation and the
    first whose whole subject is it.  A reader who disagrees with a label is
    disagreeing with text on the page rather than with a number.

--------------------------------------------------------------------------------
3.  HOW THIS FILE COULD EXHIBIT THE DEFECT IT REPORTS
--------------------------------------------------------------------------------

  * IT COULD READ ITS SUBJECT OFF DISK.  Every figure -- the population, the
    witnesses, the blame, the pins, the arms -- is read THROUGH AS_OF.  P32
    replaces `open` for the whole scan and requires nothing under the repository
    root to be read.  In particular THIS BRANCH EDITS selftest_20ee.py, which is
    one of the files section 1 counts and the site of two declarations section 2
    checks, and it cannot move this transcript.

  * ITS FINDING COULD BE UNFALSIFIABLE.  A file whose every row read COLLIDES
    would be indistinguishable from a file that cannot separate anything.  Two of
    the four rows must come back SEPARATED, one of them the limit mg-0bf1 already
    closed -- the calibration -- and one of them new.  P33 asserts both.

  * THE COLLISION COULD BE AN ARTEFACT OF PICKING TWO LINES FROM ONE PARAGRAPH.
    The two collision rows are 943 lines apart in one record, and 2 documents
    apart in the other.  Section 2 prints the line numbers.

  * A LABEL COULD BE DERIVED FROM THE FIELD IT IS BEING TESTED AGAINST, and
    R4's first draft was: the pre-registration witness was labelled `committed
    before any arm of its directory`, which is the field verbatim, so the row
    would have been asserting that the field separates two labels the field
    had assigned.  A CIRCLE THAT PASSES.  The label is now what a reader can
    check in the file -- it is that directory's only red token and it sits in a
    sentence forbidding the word -- and the date is measured and nothing else.

  * ITS OWN REGISTRY IS A HAND JUDGEMENT.  Which limits are about reading a
    sentence, and which reading each witness carries, are read by a person.  This
    file cannot decide its own registry mechanically and does not claim to; that
    is N31 and it is the limit this tranche leaves.

  * THE POPULATION IS A GREP AND GREPS OVER-COUNT.  Section 1 publishes the loose
    count and the prose-scoped one side by side and lists every site of the
    narrower, so the choice is measured rather than made silently.

--------------------------------------------------------------------------------
4.  USAGE
--------------------------------------------------------------------------------

    python3 semantic.py                     # in run_all.sh
    python3 semantic.py --row <id>          # one registry row, printed whole
"""

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

import exemplars  # noqa: E402
import worklist  # noqa: E402

# IMPORTED AND NOT RE-TYPED, for mg-1344's P5 reason two files along: `blame` and
# `rev_order` are exemplars' own, and `added_revisions` is worklist's rule B.  A
# second copy of `what is a pin` or `whose commit is this line` here would let
# this transcript disagree with out_exemplars.txt about the same sentence.
from exemplars import blame, rev_order  # noqa: E402
from worklist import added_revisions, git, read_rev, text  # noqa: E402

# The commit every figure below is a function of.  CHECKED to resolve and to be
# an ancestor of origin/main at run time, which is why this transcript has a
# fixed point and survives a rebase in the merge queue.
AS_OF = "182d93b"

# ------------------------------------------------------------------ section 1

# THE DECLARATION SHAPE.  `cannot tell` / `cannot distinguish` / `cannot
# separate` is how this estate writes down a limit it has decided not to close.
# It is a grep and it over-counts; the narrowing below is what section 1 prints
# beside it rather than instead of it.
DECLARES = re.compile(r"cannot (?:tell|distinguish|separate)\b", re.I)

# THE PREFILTER, AND IT IS DELIBERATELY WIDER THAN THE RULE.  `git grep` speaks
# POSIX ERE and has neither `(?:` nor `\b`, so the pattern it is given is the
# same alternation with both dropped -- a SUPERSET of DECLARES, which is the only
# safe direction for a prefilter: it may hand over files the rule then rejects,
# and it cannot hide one.  The counting is done by DECLARES alone.
GREP = r"cannot (tell|distinguish|separate)"

# THE NARROWING: the declaration's own words say its subject is TEXT SOMEBODY
# WROTE.  A rule that cannot tell two derivations apart, or two tables, or a
# deletion from a line break, is a limit and is not a limit about reading
# English.  DECLARED RATHER THAN TUNED, and section 1 prints every site it keeps.
PROSE = re.compile(r"\b(sentence|prose|English|wording|says|claim|paragraph)\b",
                   re.I)

# The window either side of the declaration, on the flattened text.  A wrapped
# comment is one clause and a paragraph is one clause; 160 characters is about
# two source lines each way.
WINDOW = 160

# `.txt` IS EXCLUDED AND THE COUNT IS PRINTED ANYWAY.  A transcript is an echo of
# the `.py` that printed it, so counting both scores one declaration twice --
# 77 of the 286 loose hits at AS_OF are exactly that.  Section 1 prints the
# excluded count so the exclusion is a measured choice and not a silence.
SOURCE_EXTS = (".py", ".md", ".sh")
ECHO_EXTS = (".txt",)


def grep_files(rev, pattern, globs):
    """`git grep -l -i -I -E` at `rev`, where FINDING NOTHING IS AN ANSWER.

    mg-4020's crash, one file along and reached by a third route: `git grep`
    exits 1 for NO MATCH and 2 or more for a real error, and worklist's `git()`
    -- which this file imports -- treats every non-zero alike.  Both prefilters
    below would therefore have been FATAL on the day their pattern stopped
    matching, which for the red-token one is a day somebody could bring about by
    tidying the estate.  THE TOLERANCE IS consumers.git_grep_l's AND IT IS
    DELIBERATELY NARROW, restated rather than widened: rc 1 is empty, rc 2 and
    above stays fatal, because a mistyped revision returning `none` is a census
    that reports nothing because it never looked.  P36 runs it.
    """
    got = subprocess.run(["git", "-C", ROOT, "grep", "-l", "-i", "-I", "-E",
                          pattern, rev, "--", *globs], capture_output=True)
    if got.returncode == 1:
        return []
    if got.returncode != 0:
        raise SystemExit("semantic: git grep -E %s failed (rc=%d): %s"
                         % (pattern, got.returncode,
                            got.stderr.decode("utf-8", "replace").strip()))
    out = []
    for path in got.stdout.decode("utf-8", "surrogateescape").splitlines():
        out.append(path.split(":", 1)[1] if ":" in path else path)
    return out


def flatten(body):
    """Join wrapped comment and prose lines so one clause is one string."""
    return re.sub(r"\s*\n\s*(?:#|\*|>|//)?\s*", " ", body)


def declarations(rev):
    """Every declared limit at `rev`, loose and prose-scoped.

    `git grep` at the revision picks the candidate FILES -- the whole tree is
    3,000 files and all but ninety-odd carry nothing -- and only those are read,
    through `git show`.  Nothing is read off disk (P32).
    """
    hits = grep_files(rev, GREP, ("*.py", "*.md", "*.sh", "*.txt"))
    loose_src, loose_echo, prose = 0, 0, []
    for path in sorted(hits):
        body = read_rev(rev, path)
        n = len(DECLARES.findall(body))
        if path.endswith(ECHO_EXTS):
            loose_echo += n
            continue
        if not path.endswith(SOURCE_EXTS):
            continue
        loose_src += n
        flat = flatten(body)
        for m in DECLARES.finditer(flat):
            window = flat[max(0, m.start() - WINDOW):m.end() + WINDOW]
            if PROSE.search(window):
                prose.append((path, " ".join(window.split())))
    return {"loose_src": loose_src, "loose_echo": loose_echo, "prose": prose,
            "files": sorted({p for p, _ in prose})}


# ------------------------------------------------------------------ section 2

class Gone(Exception):
    """A declaration or a witness that does not resolve at AS_OF."""


def one_line(rev, path, needle):
    """The single line of `path` containing `needle`, at `rev`.

    EXACTLY ONE, OR IT IS A SELF-ERROR.  A witness located by a substring that
    matches twice is a witness the reader cannot check, and one that matches
    nothing is a claim about a document that has moved underneath it.
    """
    body = read_rev(rev, path).splitlines()
    got = [i for i, l in enumerate(body, 1) if needle in l]
    if len(got) != 1:
        raise Gone("%s: %d lines match %r, want exactly 1"
                   % (path, len(got), needle[:40]))
    return got[0], body[got[0] - 1].strip()


def commit_body(rev, sha):
    """A commit's message, checked to be reachable from `rev`."""
    order = _ORDER[rev]
    full = text(git("rev-parse", sha)).strip()
    if full not in order:
        raise Gone("%s is not reachable from %s" % (sha[:8], rev))
    return text(git("show", "-s", "--format=%B", full))


_ORDER = {}


def order_of(rev):
    if rev not in _ORDER:
        _ORDER[rev] = rev_order(rev)
    return _ORDER[rev]


_FIRST = {}


def first_commit(rev, path):
    """The commit that introduced `path`, at `rev`.  Cached: section 3 asks for
    the same arm once per PREDICTIONS.md in its directory."""
    key = (rev, path)
    if key not in _FIRST:
        got = [h for h in text(git("log", "--format=%H", "--reverse", rev, "--",
                                   path)).split() if h]
        _FIRST[key] = got[0] if got else None
    return _FIRST[key]


def arms_of(rev, directory, tracked):
    return [p for p in tracked
            if p.startswith(directory + "/") and p.endswith(".py")]


def older_than_every_arm(rev, path, tracked):
    """Is `path` strictly older than every arm in its own directory?

    THE FIELD THAT SEPARATES A PRE-REGISTRATION FROM A TRANSCRIPT, and it is an
    IMPOSSIBILITY in exactly mg-0bf1's shape: a suite's transcript is written BY
    an arm, so it cannot pre-date every arm.  A file that does is not that
    suite's transcript, whatever tokens it contains.  The converse buys nothing --
    a pre-registration committed alongside the first arm is indistinguishable
    here -- and section 3 counts how often that happens.
    """
    order = order_of(rev)
    directory = os.path.dirname(path)
    arms = arms_of(rev, directory, tracked)
    if not arms:
        return None
    mine = first_commit(rev, path)
    return all(order[mine] > order[first_commit(rev, a)] for a in arms)


def pin_commits(rev, directory):
    """worklist's rule B, imported: the commits that pinned that directory."""
    return [h for h in text(git("log", "--format=%H", rev, "--",
                                directory)).split()
            if added_revisions(h, directory)]


# --------------------------------------------------------------- the registry
#
# FOUR ROWS, AND EVERY LABEL IN THEM IS SOMEBODY ELSE'S.  `declared` is the file
# or commit that wrote the limit down, with the substring that must still be
# there at AS_OF.  `witness` is (path, needle, reading).  `field` is the name of
# what the row asks the repository, and `event` -- where the row has one -- is
# the directory whose pin is the thing the two readings straddle.

REGISTRY = [
    {
        "id": "R1",
        "limit": "ACCOUNTING vs OFFERING -- N28, the one mg-0bf1 closed",
        "declared": ("file", "code/asof_census_20ee/selftest_20ee.py",
                     "a SUBSTRING COUNT, so a sentence ACCOUNTING for a pin"),
        "witnesses": [
            ("code/asof_census_20ee/README.md", "are cheap; the large ones",
             "OFFERING -- tranche 1 names it as remaining work"),
            ("code/asof_census_20ee/README.md", "was **pinned at `e29ba2a`**",
             "ACCOUNTING -- tranche 9 annotates it with the pin"),
        ],
        "field": "commit order against the pin on the named instrument",
        "event": "code/species_remainder_f8fa",
        "note": ("THE CALIBRATION, AND IT IS THE WRONG-DIRECTION CONTROL FOR "
                 "THIS WHOLE FILE.  A file every row of which read COLLIDES "
                 "would be indistinguishable from a file that cannot separate "
                 "anything, so the row already known to be a date question is "
                 "asked by the same machinery and must come back SEPARATED."),
    },
    {
        "id": "R2",
        "limit": "a YOUNGER mention: ACCOUNTING vs A QUOTATION OF THE OFFER "
                 "-- N29, the limit mg-0bf1 left",
        "declared": ("file", "code/asof_census_20ee/selftest_20ee.py",
                     "N29 a YOUNGER mention closes the pair whatever it says"),
        "witnesses": [
            ("code/asof_census_20ee/README.md", "was **pinned at `e29ba2a`**",
             "ACCOUNTING -- it names the pin"),
            ("code/asof_census_20ee/README.md",
             "> the small ones (`species_remainder_f8fa`",
             "NOT AN ACCOUNTING -- it is tranche 1's offer, quoted"),
        ],
        "field": "commit order against the pin on the named instrument",
        "event": "code/species_remainder_f8fa",
        "note": ("AND THE SECOND WITNESS IS THE FIRST ROW'S FIRST WITNESS, "
                 "QUOTED.  The same English sentence appears twice in this one "
                 "record: once as tranche 1 wrote it, where the date decides "
                 "it, and once inside tranche 9's quotation of it, where the "
                 "date is tranche 9's and decides nothing.  A QUOTATION MOVES "
                 "THE SENTENCE WITHOUT MOVING THE EVENT, which is `blame is "
                 "the last touch and not the origin` arriving from the other "
                 "side: there a reflow re-dates a sentence nobody changed, "
                 "here a quotation re-dates one somebody deliberately "
                 "reproduced."),
    },
    {
        "id": "R3",
        "limit": "a strike marker USED vs MENTIONED -- mg-aaf4 section 7",
        "declared": ("file", "code/branching_bound_audit_aaf4/README.md",
                     "THE LIVENESS RULE CANNOT TELL USE FROM MENTION"),
        "witnesses": [
            ("docs/OneThird-Counterexample-Under-The-Action.md",
             "**STRUCK (mg-dea5, landing mg-a7b4 finding 3)",
             "USE -- the marker strikes the paragraph it opens"),
            ("docs/OneThird-Counterexample-Under-The-Action-Repair.md",
             "every occurrence must lie inside a",
             "MENTION -- the marker is quoted as the thing a check looks for"),
        ],
        "field": "commit order (there is no second event to straddle)",
        "event": None,
        "note": ("THE ROW WITH NO EVENT IN IT AT ALL, which is why it collides "
                 "rather than merely failing to separate.  A pin is a commit "
                 "and an arm is a commit; `what this marker is FOR` is not an "
                 "event in the repository, so there is no pair of dates to "
                 "order.  The two witnesses land in one commit because the "
                 "author wrote a strike and a description of strikes in one "
                 "landing, and nothing about the repository distinguishes "
                 "them."),
    },
    {
        "id": "R4",
        "limit": "a TRANSCRIPT recording a failure vs a PRE-REGISTRATION "
                 "recording a refuted prediction -- mg-9876's a4 section 3",
        "declared": ("commit", "07a2fd0",
                     "a predictions file recording refuted predictions joins "
                     "a class the row calls"),
        "witnesses": [
            ("code/c3_audit_a94c3/PREDICTIONS.md",
             "Reporting P4 as REFUTED would be wrong",
             "PRE-REGISTRATION -- the only red token in that whole directory, "
             "and it is in a sentence forbidding the word"),
            ("code/lever_shape_9b6b/out_e1_collapse.txt",
             "3  2/3          2/75         yes        REFUTED",
             "TRANSCRIPT -- printed by an arm that already existed"),
        ],
        "field": "is the file older than every arm in its own directory",
        "event": None,
        "note": ("THE NEW ONE, AND IT IS THE ANSWER TO THE QUESTION mg-0bf1 "
                 "CLOSED WITH.  `does this file record a demonstrated failure` "
                 "reads like a question about what the file IS; a suite's "
                 "transcript is written by an arm and therefore CANNOT "
                 "pre-date every arm, so a file that does is not one -- the "
                 "same impossibility as `an older sentence cannot be an "
                 "accounting`, on a different subject, with no English read "
                 "anywhere.  Section 3 measures it over the whole estate "
                 "rather than over these two lines."),
    },
]


def resolve(row, rev):
    """One registry row, measured.  Every failure to resolve is printed."""
    out = {"id": row["id"], "limit": row["limit"], "field": row["field"],
           "note": row["note"], "errors": [], "witnesses": []}
    kind, where, needle = row["declared"]
    try:
        if kind == "file":
            line, txt = one_line(rev, where, needle)
            out["declared"] = ("%s:%d" % (where, line), txt)
        else:
            body = commit_body(rev, where)
            if needle not in flatten(body):
                raise Gone("%s's message no longer carries the declaration"
                           % where)
            out["declared"] = ("commit %s" % where[:7],
                               " ".join(needle.split()))
    except Gone as exc:
        out["declared"] = ("GONE", str(exc))
        out["errors"].append("declaration: %s" % exc)

    order = order_of(rev)
    tracked = tracked_paths(rev)
    for path, needle, reading in row["witnesses"]:
        try:
            line, txt = one_line(rev, path, needle)
        except Gone as exc:
            out["errors"].append("witness: %s" % exc)
            continue
        sha = blame(rev, path).get(line)
        w = {"path": path, "line": line, "text": txt, "reading": reading,
             "sha": sha, "order": order.get(sha)}
        if row["field"].startswith("is the file older"):
            w["value"] = older_than_every_arm(rev, path, tracked)
        else:
            w["value"] = None
        out["witnesses"].append(w)

    if len(out["witnesses"]) != 2:
        out["verdict"] = "UNRESOLVED"
        return out
    a, b = out["witnesses"]
    if a["sha"] == b["sha"]:
        out["verdict"] = "COLLIDES"
        out["why"] = ("both readings were written by %s, so every commit-level "
                      "field is identical across them" % a["sha"][:7])
        return out
    if row["event"]:
        pins = pin_commits(rev, row["event"])
        lo, hi = sorted((a["order"], b["order"]))
        strictly = [h for h in pins if lo < order[h] < hi]
        out["pins"] = pins
        out["between"] = strictly
        if strictly:
            out["verdict"] = "SEPARATED"
            out["why"] = ("the pin %s on %s lies strictly between them"
                          % (strictly[0][:7], row["event"]))
            return out
    if a["value"] is not None and a["value"] != b["value"]:
        out["verdict"] = "SEPARATED"
        out["why"] = ("the field takes %r on the first and %r on the second"
                      % (a["value"], b["value"]))
        return out
    out["verdict"] = "NOT SEPARATED"
    out["why"] = "no event of the row's kind lies between them"
    return out


# ------------------------------------------------------------------ section 3

_TRACKED = {}


def tracked_paths(rev):
    if rev not in _TRACKED:
        _TRACKED[rev] = text(git("ls-tree", "-r", "--name-only",
                                 rev)).splitlines()
    return _TRACKED[rev]


# a4_sweep's OWN token list, read out of that file at AS_OF rather than re-typed,
# for the reason worklist's pin rule is imported: a second spelling here could
# disagree with out_a4_sweep.txt about which files are red.
def red_tokens(rev):
    src = read_rev(rev, "code/control_audit_9876/a4_sweep.py")
    m = re.search(r"RED_TOKENS = re\.compile\(\s*(r\"[^\"]*\"\s*)+\)", src)
    if not m:
        raise Gone("a4_sweep.py no longer spells RED_TOKENS the way this "
                   "file reads it -- REPORTED rather than guessed at")
    pattern = "".join(re.findall(r'r"([^"]*)"', m.group(0)))
    return re.compile(pattern)


def prereg_census(rev):
    """The R4 field over the whole estate, both directions."""
    tracked = tracked_paths(rev)
    red = red_tokens(rev)
    preds = [p for p in tracked if os.path.basename(p) == "PREDICTIONS.md"]
    provable = [p for p in preds if older_than_every_arm(rev, p, tracked)]
    dirs = sorted({"code/" + p.split("/")[1] for p in tracked
                   if p.startswith("code/") and p.count("/") >= 2})
    # THE SAME SUPERSET PREFILTER AS SECTION 1, AND FOR THE SAME REASON: the
    # token rule is a4's own, read out of a4_sweep.py above rather than typed,
    # and `git grep` speaks POSIX ERE with no `\b`.  Dropping the boundaries
    # widens the candidate set; every candidate is then re-read and decided by
    # a4's rule itself, so this cannot hide a file and can only offer spare ones.
    loose = "(%s)" % red.pattern.replace(r"\b", "")
    cand = set(grep_files(rev, loose, ("code/*.txt", "code/*.md")))
    fires, only_pred = [], []
    for d in dirs:
        hits = [p for p in tracked
                if p in cand and p.startswith(d + "/")
                and red.search(read_rev(rev, p))]
        if not hits:
            continue
        fires.append(d)
        if all(os.path.basename(h) == "PREDICTIONS.md" for h in hits):
            only_pred.append((d, hits))
    proved = [(d, h) for d, h in only_pred
              if all(older_than_every_arm(rev, p, tracked) for p in h)]
    return {"dirs": dirs, "preds": preds, "provable": provable,
            "fires": fires, "only_pred": only_pred, "proved": proved}


# ------------------------------------------------------------------- printing

def rule(title):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)
    print()


def wrap(s, indent="  ", width=76):
    out, line = [], indent
    for w in s.split():
        if len(line) + len(w) + 1 > width:
            out.append(line)
            line = indent + w
        else:
            line = (line + " " + w) if line.strip() else indent + w
    if line.strip():
        out.append(line)
    return "\n".join(out)


def main():
    rev = AS_OF
    full = text(git("rev-parse", rev)).strip()
    if not full:
        raise SystemExit("AS_OF %s does not resolve" % rev)
    anc = subprocess.call(["git", "-C", ROOT, "merge-base", "--is-ancestor",
                           full, "origin/main"],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("=" * 78)
    print("mg-5058 -- WHICH DECLARED LIMITS ARE DATE QUESTIONS")
    print("=" * 78)
    print()
    print("  AS_OF %s  (ancestor of origin/main: %s)"
          % (full[:12], "yes" if anc == 0 else "NO -- SAY SO IN THE LANDING"))
    print()
    print(wrap("mg-0bf1 closed with one question: is any remaining `read what "
               "the sentence says` rule in this estate likewise a date "
               "question wearing semantic clothes?  Every figure below is a "
               "function of that one commit, so THIS BRANCH'S OWN EDITS TO "
               "selftest_20ee.py -- a file section 1 counts and section 2 "
               "reads two declarations out of -- CANNOT MOVE THIS "
               "TRANSCRIPT."))

    # ------------------------------------------------------------ section 1
    rule("1.  THE POPULATION -- HOW OFTEN THIS ESTATE DECLARES A LIMIT")
    d = declarations(rev)
    print("  `cannot tell` / `cannot distinguish` / `cannot separate`")
    print()
    print("    in tracked .py / .md / .sh                       : %4d"
          % d["loose_src"])
    print("    in tracked .txt, EXCLUDED as an echo of the .py  : %4d"
          % d["loose_echo"])
    print("    of the first, PROSE-SCOPED by their own words    : %4d in %d files"
          % (len(d["prose"]), len(d["files"])))
    print()
    print(wrap("The narrowing keeps a declaration whose own words say its "
               "subject is text somebody wrote -- sentence, prose, English, "
               "wording, says, claim, paragraph, within %d characters of the "
               "declaration on the flattened text.  It is a grep and it is "
               "printed beside the loose count rather than instead of it.  "
               "FOUR of these are tested in section 2 and %d ARE NOT, which "
               "is the residue this tranche leaves and is listed in section "
               "5." % (WINDOW, len(d["prose"]) - 4)))
    print()
    print("  THE FILES THAT DECLARE ONE (prose-scoped)")
    for p in d["files"]:
        n = sum(1 for q, _ in d["prose"] if q == p)
        print("    %-62s %d" % (p, n))

    # ------------------------------------------------------------ section 2
    rule("2.  THE FOUR ROWS -- IS THE DISTINCTION A DATE QUESTION?")
    print(wrap("COLLIDES is the direction that PROVES: two readings written by "
               "one commit share every commit-level field, so no rule reading "
               "any of them can separate the pair.  SEPARATED proves only that "
               "the row's field decides these two."))
    print()
    rows = [resolve(r, rev) for r in REGISTRY]
    for r in rows:
        print("-" * 78)
        print("  %s  %s" % (r["id"], r["limit"]))
        print("-" * 78)
        print("    declared at : %s" % r["declared"][0])
        print(wrap("| " + r["declared"][1][:300], indent="        "))
        print("    field       : %s" % r["field"])
        for w in r["witnesses"]:
            print()
            print("    %s:%d   %s   order %d"
                  % (w["path"], w["line"], w["sha"][:7], w["order"]))
            print("      reading : %s" % w["reading"])
            if w["value"] is not None:
                print("      field   : older than every arm = %s" % w["value"])
            print(wrap("| " + w["text"][:300], indent="        "))
        for e in r["errors"]:
            print("    !! %s" % e)
        print()
        print("    VERDICT: %s -- %s" % (r["verdict"], r.get("why", "")))
        print()
        print(wrap(r["note"], indent="    "))
        print()
    print("-" * 78)
    print("  SUMMARY")
    for r in rows:
        print("    %-4s %-14s %s" % (r["id"], r["verdict"], r["limit"][:52]))
    sep = [r["id"] for r in rows if r["verdict"] == "SEPARATED"]
    col = [r["id"] for r in rows if r["verdict"] == "COLLIDES"]
    print()
    print("    %d SEPARATED (%s), %d COLLIDES (%s)"
          % (len(sep), ", ".join(sep), len(col), ", ".join(col)))

    # ------------------------------------------------------------ section 3
    rule("3.  THE NEW DATE ROW, MEASURED OVER THE ESTATE AND NOT OVER TWO LINES")
    c = prereg_census(rev)
    print(wrap("R4's field is an impossibility of exactly mg-0bf1's shape: a "
               "suite's transcript is written by an arm, so it cannot "
               "pre-date every arm of its own directory.  Below is how far "
               "that reaches at AS_OF."))
    print()
    print("    PREDICTIONS.md in the tree                        : %4d"
          % len(c["preds"]))
    print("      of those, PROVABLY pre-registered               : %4d"
          % len(c["provable"]))
    print("      born with an arm, so not provable here          : %4d"
          % (len(c["preds"]) - len(c["provable"])))
    print()
    print("    directories under code/                           : %4d"
          % len(c["dirs"]))
    print("      where a4's red-token row fires                  : %4d"
          % len(c["fires"]))
    print("      where it fires ONLY through a PREDICTIONS.md    : %4d"
          % len(c["only_pred"]))
    print("        of those, the date PROVES it is not a         : %4d"
          % len(c["proved"]))
    print("        transcript")
    print()
    for dname, hits in c["only_pred"]:
        mark = "PROVED" if any(dname == x for x, _ in c["proved"]) else "  --  "
        print("      %s  %s" % (mark, dname))
    print()
    print(wrap("ONE-DIRECTIONAL AGAIN.  `older than every arm` proves the file "
               "is not that suite's transcript.  BORN WITH AN ARM PROVES "
               "NOTHING -- a pre-registration committed in the same landing as "
               "the first arm is indistinguishable here, and %d of the %d are "
               "in that state.  REPORTED AND NOT REPAIRED: the row belongs to "
               "mg-9876, and a branch that re-scoped another instrument's "
               "detector to make its own number read better would be doing "
               "the worse thing."
               % (len(c["preds"]) - len(c["provable"]), len(c["preds"]))))

    # ------------------------------------------------------------ section 4
    rule("4.  WHAT THE FOUR ROWS SAY TOGETHER")
    print(wrap("THE ANSWER TO mg-0bf1'S QUESTION IS YES FOR ONE MORE AND "
               "PROVABLY NO FOR TWO, and the criterion that falls out of the "
               "four is one sentence:"))
    print()
    print(wrap("A SEMANTIC-LOOKING DISTINCTION IS A DATE QUESTION EXACTLY WHEN "
               "THE TWO READINGS PUT THE TEXT ON OPPOSITE SIDES OF AN EVENT "
               "THAT IS ITSELF A COMMIT.", indent="    "))
    print()
    print(wrap("R1 has one -- the pin.  R4 has one -- the first commit of an "
               "arm.  R3 has none: `what this marker is FOR` is not an event "
               "in the repository at all, so there are not two dates to "
               "order.  R2 has an event and still collides, and that is the "
               "sharpest row here: the event exists, the rule that used it "
               "works on the sentence's FIRST utterance, and a QUOTATION of "
               "the same sentence carries the quoting commit's date.  The "
               "date is a property of the touch and the reading is a property "
               "of the words, and a quotation is where those two come apart "
               "on purpose."))

    # ------------------------------------------------------------ section 5
    rule("5.  WHAT THIS FILE CANNOT DO")
    print(wrap("N31 -- THE REGISTRY IS A HAND JUDGEMENT AND THIS FILE CANNOT "
               "DECIDE IT.  Which of the %d prose-scoped declarations are "
               "about reading a sentence, and which reading each witness "
               "carries, are read by a person.  The remedy is the one N28 "
               "named and it is the reason every witness is printed with its "
               "line: THE INSTRUMENT PRINTS THE SENTENCE.  A reader who "
               "disagrees with a label disagrees with text on the page."
               % len(d["prose"])))
    print()
    print(wrap("A COLLISION IS ABOUT THE WITNESSES AND NOT ABOUT THE WHOLE "
               "LIMIT.  It proves no commit-level field separates THESE two "
               "readings, which is enough to kill a proposed rule and is not "
               "a proof that the limit is unclosable by any means -- a rule "
               "reading document structure, as exemplars' section 3 does, is "
               "not a rule reading a commit."))
    print()
    print(wrap("%d OF THE %d PROSE-SCOPED DECLARATIONS ARE UNTESTED.  Four "
               "carry witnesses here because a witness pair is a hand "
               "judgement and this tranche affords four.  The other sites are "
               "listed in section 1 for a successor to pick from; the one "
               "worth naming is mg-9876's own `a regex cannot tell an arm "
               "from a print`, whose two readings sit in one directory and "
               "two commits." % (len(d["prose"]) - 4, len(d["prose"]))))
    print()
    print("CONDITION 0 (semantic): %d rows, %d SEPARATED, %d COLLIDES, "
          "%d prose-scoped declarations in %d files, %d untested"
          % (len(rows), len(sep), len(col), len(d["prose"]), len(d["files"]),
             len(d["prose"]) - 4))


def one_row(rid):
    for r in REGISTRY:
        if r["id"] == rid:
            got = resolve(r, AS_OF)
            for k in ("id", "limit", "field", "verdict", "why"):
                print("%-9s %s" % (k + ":", got.get(k, "")))
            for w in got["witnesses"]:
                print("%s:%d %s  %s" % (w["path"], w["line"], w["sha"][:7],
                                        w["reading"]))
                print("   | %s" % w["text"][:200])
            return 0
    print("no such row: %s" % rid)
    return 2


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--row":
        sys.exit(one_row(sys.argv[2]))
    main()
