"""mg-365a — shared plumbing for "was the oscillation discharged, and by what?"

THIS DIRECTORY EXISTS BECAUSE ITS TICKET'S PREMISE IS STALE, AND SAYS SO IN A COMMAND.

mg-365a is mg-585e's successor carrier.  It is written in the present tense about
`lib_f771.SELF_EXCLUDED` — "`out_g0_fixed_point.txt` **is** mg-f771's single self-exemption" —
and that constant was DELETED by `bd07d70` (mg-c15e) at 00:41Z, nineteen minutes after the
commit the ticket was written from.  The mayor's own caution of 00:22Z is on the ticket:

    a successor carrier filed while its cause was live can outlive the cause, and derived
    work can be discharged by the fix rather than needing its own slot.

That caution is correct and this directory is the measurement of it.  The ticket asks for a
command rather than an argument; what follows is the command.

WHY IMPORTING RATHER THAN RE-SPELLING IS THE WHOLE DESIGN (mg-d2c2, mg-1344's P5).

Every predicate this directory decides with is IMPORTED from the instrument it is reporting
on, never re-typed here:

  * `v1_oscillation.is_red`   — mg-585e's own RED-shape test.  The central finding is that
    THIS PREDICATE now reads green for a reason that has nothing to do with the verdict, and
    a re-spelling of it would make that finding a statement about the re-spelling.
  * `lib_f771.is_watched`     — the watched class, from the instrument that defines it.  The
    counterfactual in `d1` §4 counts landings that would have owed a refresh; computing that
    with a hand-written `out_*.txt` glob would be a re-statement, and a re-statement drifts.
  * `lib_f771.CORPUS_SCOPED`  — the corpus-scoped registry, so that a transcript exempted
    from per-branch grading cannot be counted here as evidence of a disagreement.
  * `lib585e.git` / `Refused` — the same subprocess and refusal discipline as the directory
    whose figures are being re-taken.

NOTHING IN `code/verdict_invariance_585e/` OR `code/gate_fixed_point_f771/` IS MODIFIED.  Both
are imported read-only.  That is not tidiness: mg-585e's transcripts are pinned and byte-
identical, and touching either directory would cost a refresh commit — which, in a directory
whose subject IS refresh commits, would be the eleventh instance filed by the arm that counted
ten.  P8 is the check that it did not happen.

THE PIN, AND WHY THERE IS ONE.

Every figure is a function of `AS_OF_365A` and the walk it defines, not of HEAD.  The history
of the file this directory measures grows every time that file is touched; walked from HEAD,
this transcript would go stale on the next landing and this directory would be shipping its own
subject.  mg-585e's v1 avoided that the same way and the reasoning is taken from it wholesale.

A SECOND CONSEQUENCE, WHICH IS THE ONE THAT MATTERS IN THE MERGE QUEUE: a pinned transcript
does not conflict on a rebase.  mg-585e recorded that as a fact about pins after its own
`out_v1_oscillation.txt` came through a rebase byte-identical while two unpinned siblings
moved.  Three branches hit rebase conflicts on generated transcripts the night this was
written.  This one cannot.

WHAT THIS DIRECTORY CANNOT SEE, said before the numbers rather than after.

It reads COMMITTED history.  A red run repaired before its author committed leaves no trace, so
every count is a LOWER BOUND on how often the oscillation happened and an EXACT count of how
often it reached main.  That is mg-585e's own caveat and it is inherited unchanged.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

_585E = os.path.join(ROOT, "code", "verdict_invariance_585e")
_F771 = os.path.join(ROOT, "code", "gate_fixed_point_f771")

for _p in (_585E, _F771):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import lib585e as L585                                      # noqa: E402
import lib_f771 as LF                                       # noqa: E402
import v1_oscillation as V1                                 # noqa: E402

# The refusal type and the subprocess wrapper come from mg-585e rather than being written
# again here, so this directory cannot disagree with that one about what "git failed" means.
Refused = L585.Refused
git = L585.git

# The path under measurement, taken from mg-585e's constant.  Re-typing this string would be
# the cheapest possible way for this directory to end up reporting on a different file than
# the one it claims to.
F771_TRANSCRIPT = L585.F771_TRANSCRIPT

# ---------------------------------------------------------------------------------------
# THE TWO PINS
# ---------------------------------------------------------------------------------------

# The commit every figure in this directory is a function of.
AS_OF_365A = "b5d8a757441d8f99eacc995925ab3fe511ef4cd4"

# THE EVENT.  `delete: THE SELF-EXEMPTION IS GONE AND THE WATCHED CLASS IS TOTAL` (mg-c15e).
# This is the commit the whole directory is a before/after of, and it is a CONSTANT rather
# than something the arms search for by subject line: a rule that located it by grepping
# commit messages would be a rule about English, and would silently pick a different commit
# the day somebody writes a similar subject.
DELETION = "bd07d705a2fc26d28336491d99554bd8c895b54c"

# mg-585e's pin, imported rather than re-typed, so the "then vs now" comparison cannot drift
# apart from the figures it is being compared against.
AS_OF_585E = L585.AS_OF

# mg-585e's published figures at ITS pin, quoted here so that `d1` can re-derive them and
# report agreement or disagreement rather than assuming.  These are the numbers in that
# directory's own transcript and in `bd07d70`'s commit message.
PUBLISHED_585E = {"versions": 31, "red": 16, "flips": 24, "solo": 7}

# The pre-deletion touch rate mg-585e priced, used by `d1` §3 to say out loud that `0 of 8`
# is NOT significant on its own.  30 touches over 129 code/ commits across 137bc4ce..0cb0fa4.
RATE_TOUCHES, RATE_COMMITS = 30, 129


class ArmError(Exception):
    """A control failed.  Distinct from `Refused`, which means the arm could not run at all."""


# ---------------------------------------------------------------------------------------
# THE WALK
# ---------------------------------------------------------------------------------------

def require_pin(pin, root=ROOT, name="AS_OF_365A"):
    """P10.  The pin must RESOLVE and be an ANCESTOR OF origin/main.

    A pin that resolves only in this worktree is a pin to a commit that may never land, and
    every figure hanging off it would be unreproducible for the next reader.  This is
    mg-585e's `require_as_of` applied to a second pin; the reasoning is that directory's.
    """
    p = git(root, "rev-parse", "--is-inside-work-tree")
    if p.returncode != 0 or p.stdout.strip() != "true":
        raise Refused("%s is not inside a git work tree" % root)
    p = git(root, "rev-parse", "--verify", "%s^{commit}" % pin)
    if p.returncode != 0:
        raise Refused("%s %s does not resolve in this repository" % (name, pin[:8]))
    q = git(root, "merge-base", "--is-ancestor", pin, "origin/main")
    if q.returncode != 0:
        raise Refused("%s %s is not an ancestor of origin/main — a pin to a commit that may "
                      "never land is not a pin" % (name, pin[:8]))
    return pin


def history(pin, root=ROOT, path=None):
    """Committed versions of the transcript at `pin`, newest first.

    P9.  An EMPTY walk is a REFUSAL and not a zero.  This directory's entire finding is a
    zero — `0 of 8 landings touched the file` — and a zero printed because the walk found
    nothing is indistinguishable on the page from a zero that is the answer.
    """
    path = path or F771_TRANSCRIPT
    p = git(root, "log", "--format=%H", "--follow", pin, "--", path)
    if p.returncode != 0:
        raise Refused("git log failed on %s: %s" % (path, (p.stderr or "").strip()))
    out = p.stdout.split()
    if not out:
        raise Refused("the walk of %s at %s returned NO versions — a scan that read nothing "
                      "must refuse rather than report 0" % (path, pin[:8]))
    return out


def files_of(h, root=ROOT):
    """Every path in a commit's diff."""
    p = git(root, "show", "--format=", "--name-only", h)
    if p.returncode != 0:
        raise Refused("cannot read the file list of %s" % h[:8])
    return [x for x in p.stdout.split("\n") if x.strip()]


def text_of(h, root=ROOT, path=None):
    path = path or F771_TRANSCRIPT
    p = git(root, "show", "%s:%s" % (h, path))
    if p.returncode != 0:
        raise Refused("cannot read %s:%s" % (h[:8], path))
    return p.stdout


def subject(h, root=ROOT):
    return git(root, "log", "-1", "--format=%s", h).stdout.strip()


def ticket_of(h, root=ROOT):
    """The trailing `(mg-xxxx)` on a commit subject, or '' — a label for the report, never a
    decision.  Nothing in this directory branches on it."""
    s = subject(h)
    if s.endswith(")") and "(mg-" in s:
        return s[s.rfind("(mg-") + 1:-1]
    return ""


def is_solo(h, root=ROOT, path=None):
    """Is this commit's ENTIRE diff that one transcript?

    THE HONEST PREDICATE (P3).  It is defined without reference to §2's text, so it survives
    `bd07d70` deleting the RED heading — unlike `v1.is_red`, which does not and whose zero
    after the deletion measures the deletion.
    """
    path = path or F771_TRANSCRIPT
    return files_of(h, root) == [path]


def commits_between(lo, hi, root=ROOT):
    """Commits in (lo, hi], oldest first."""
    p = git(root, "rev-list", "%s..%s" % (lo, hi))
    if p.returncode != 0:
        raise Refused("git rev-list %s..%s failed" % (lo[:8], hi[:8]))
    return list(reversed(p.stdout.split()))


def watched_committed(h, root=ROOT, exclude_self=True, watched=None):
    """The watched transcripts this commit COMMITTED, corpus-scoped ones removed.

    THE COUNTERFACTUAL'S ONE MOVING PART (P5).  `./build.sh` regenerates transcripts into the
    worktree and THEN `g0` compares the worktree against HEAD, so the old §2's disagreement
    set D(T) CONTAINS every watched transcript the landing went on to commit.  A landing with
    a non-empty result here therefore PROVABLY had D(T) != {} and would have carried a RED §2.

    IT IS A LOWER BOUND, WHICH IS THE SAFE DIRECTION.  Transcripts graded NOISE or CORPUS are
    RESTORED rather than committed (mg-4020), so they never appear here; D(T) as g0 reported
    it is at least this set and may be larger.  A lower bound on "would have owed" is what
    the finding needs, since the finding is that the toll was owed and not paid.

    `is_watched` is IMPORTED from `lib_f771`, not re-typed.  The corpus-scoped registry is
    imported for the same reason: a transcript that g0 grades against a pin rather than
    against this tree is not evidence of a per-branch disagreement, and hard-coding that one
    path here would leave this arm wrong the day a second one is registered.
    """
    watched = LF.is_watched if watched is None else watched
    out = []
    for f in files_of(h, root):
        if not watched(f):
            continue
        if exclude_self and f == F771_TRANSCRIPT:
            continue
        if f in LF.CORPUS_SCOPED:
            continue
        out.append(f)
    return out


def solo_population(pin, root=ROOT, path=None):
    """Every solo commit at `pin`, CHRONOLOGICAL and numbered from 1.

    NUMBERED BY RE-WALKING AND NEVER BY INCREMENTING A PUBLISHED FIGURE.  That is P7's whole
    subject: `15af11d3` is called "the 8th" by its own commit message and by this ticket,
    which is mg-585e's pinned 7 plus one — and `65c647bf` landed between the pin and the
    claim.  The arithmetic was right and the answer was wrong.
    """
    versions = history(pin, root, path)
    rows = []
    for h in reversed(versions):                            # oldest first
        if is_solo(h, root, path):
            rows.append({"h": h, "n": len(rows) + 1, "ticket": ticket_of(h, root),
                         "subject": subject(h, root)})
    return rows


def red_both_ways(text):
    """mg-585e's two RED predicates, both IMPORTED, returning (anchored, loose).

    mg-9876 §1 requires a membership-shaped predicate to be run BOTH ways rather than reasoned
    about, and mg-585e's v1 §1 prints the disagreement between these two.  This directory
    re-takes that comparison at a pin seven versions later, where the answer could have
    changed and where nothing would have announced it if it had.
    """
    return V1.is_red(text), V1.loose_red(text)


def binom_zero(p, n):
    """P(0 successes | n trials, per-trial probability p).  Used ONCE, to say out loud that
    `0 of 8` is not significant on its own — a directory that rested on that zero would be
    reporting a quiet window as a repair."""
    return (1.0 - p) ** n
