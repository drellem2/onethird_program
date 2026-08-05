"""mg-f3ff -- shared machinery for the re-derivation of the dropped-verdict
census of 2026-07-31.

WHAT THIS REPLACES.  The census that produced mg-e35b / mg-fccb / mg-a74f /
mg-dffa was built by reading pm-onethird's MAIL: a parent ticket whose verdict
never arrived in the inbox was recorded as having no landing commit and no
successor.  Mail is the channel that was already known to drop -- three of the
four rows say NEVER ROUTED TO ME or RECOVERED FROM COMMIT MESSAGES in their own
titles.  The census took a channel's silence as evidence of absence, on the very
channel whose failure it was filed to document, and it is wrong on at least one
row (mg-e35b's polecat checked the tree and found a five-generation chain).

⚠️ SWITCHING TO THE TREE IS NOT SUFFICIENT ON ITS OWN.  A `git log --grep` run
against a stale checkout reports the same "no successor" for the same rows, for
a completely different reason, and it reports it with the authority of having
read the tree.  pm-onethird's own workspace checkout was measured 25 commits
behind origin/main at 2026-08-04T21:07Z; the `one_third_width_three` checkout
this run started against was 45 behind.  So:

  * every repo is FETCHED before it is read, and the fetch's exit status is
    recorded rather than assumed;
  * every derivation resolves `origin/main` explicitly -- never a bare local
    `main`, never `HEAD`;
  * a repo whose fetch FAILED yields UNKNOWN for every row that ranges over it,
    and UNKNOWN is printed as UNKNOWN.  `I looked and there was nothing` and
    `I could not look` are different answers and this module will not merge
    them.  See `Fetched.unknown` and the forced-failure control in
    `s2_controls.py`, which proves the propagation rather than asserting it.
"""
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

# --------------------------------------------------------------------------
# THE POPULATION -- stated here, in the source, as the ticket requires
# --------------------------------------------------------------------------
POPULATION = """\
POPULATION OF THE REPAIRED METHOD
  For a row (parent ticket P, filing instant T) the method ranges over:
    every commit reachable from `origin/main` in each repo of a NAMED repo
    list, as origin/main stands at the moment of the run, after a fetch whose
    exit status was checked.
  A commit is a SUCCESSOR of P when all three hold:
    (a) its full message -- subject AND body AND trailers -- contains P,
        case-insensitively;
    (b) its owning ticket (the trailing `(mg-xxxx)` of the subject) is not P;
    (c) its date is <= T.  Both clocks are computed: author date (when the
        work was written) and committer date (when it entered this history).
        They differ under rebase and the difference is reported, not hidden.
  The row's premise `no successor` is REFUTED if >= 1 successor exists, UPHELD
  if 0 exist, and UNKNOWN if any repo it ranges over could not be read."""

BLIND_SPOTS = """\
WHAT THE REPAIRED METHOD CANNOT SEE
  B1  Work on a branch never merged into origin/main.  Unreachable is
      indistinguishable from non-existent.
  B2  Work in a repo not on the repo list.  The list is SUPPLIED, not
      discovered; a successor in a third repo is invisible.  This is the mail
      census's defect in a new place: a bounded channel taken for the world.
  B3  A successor commit whose message names neither P nor any ticket that
      descends from P.  The ticket-reference graph (s3) widens this but does
      not close it.
  B4  History rewritten after the fact.  The census reads origin/main as it
      stands NOW, not as it stood at T.  A successor that was squashed or
      force-pushed away is read as never having existed.
  B5  Rebase moves committer dates and not author dates, so a commit written
      before T can carry a committer date after it.  Both are reported; the
      method does not decide for the reader which clock is the truth.
  B6  Landings that are not commits: a verdict acted on inside a ticket body,
      a decision recorded only in mail, a change made outside git.
  B7  Mention is not descent.  A commit saying `unlike mg-fcf1` scores exactly
      as one repairing mg-fcf1.  The reader gets the subject line and decides.
  B8  Tickets deleted from the work store are absent from the graph, though
      their commits remain in the tree."""

# The four rows of the census under repair, and the repo list the method
# ranges over.  ⚠️ The repo list is NOT per-row: every row is searched in BOTH
# repos.  The census being repaired scoped each row to its parent's `repo:`
# field, and row 2's parent has successors in the repo that field does not
# name.  Scoping the search to the ticket's own metadata is the mail defect
# with a different bounded channel (blind spot B2).
REPOS = [
    ("onethird_program", "/Users/daniel/research/onethird_program"),
    ("one_third_width_three", "/Users/daniel/research/one_third_width_three"),
]

ROWS = [
    (1, "mg-e35b", "2026-07-31T04:13:24Z", "mg-fcf1"),
    (2, "mg-fccb", "2026-07-31T04:12:41Z", "mg-d112"),
    (3, "mg-a74f", "2026-07-31T04:22:15Z", "mg-16eb"),
    (4, "mg-dffa", "2026-07-31T04:22:50Z", "mg-5800"),
]

# From PREDICTIONS.md, committed at 72e36cb BEFORE any of these scripts
# existed.  Quoted here so the scoring is done by the instrument and cannot
# drift from what was actually predicted.
PREDICTED = {1: "REFUTED", 2: "REFUTED", 3: "UPHELD", 4: "UPHELD"}
PRED_BLIND = {1: False, 2: False, 3: False, 4: False}   # P1-P4 all disclosed not-blind

TICKET_RE = re.compile(r"\bmg-[0-9a-f]{4}\b", re.I)
OWNER_RE = re.compile(r"\((mg-[0-9a-f]{4})\)\s*$", re.I)

WORK_STORE = os.path.expanduser("~/.macguffin/work")
MAIL_STORE = os.path.expanduser("~/.macguffin/mail")


def _run(args, cwd=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


# --------------------------------------------------------------------------
# FRESHNESS -- the addendum's load-bearing half
# --------------------------------------------------------------------------
class Fetched:
    """One repo, fetched and resolved, carrying its own failure.

    ⚠️ `unknown` is TRUE whenever the fetch failed or origin/main would not
    resolve.  Every caller must branch on it.  The pre-start freshness check
    that this ticket exists because of failed with `ssh: connect to host
    github.com port 22`, reported UNKNOWN, and UNKNOWN was presented as though
    nothing was wrong."""

    def __init__(self, path, label, allow_fetch=True, force_fail=False):
        self.path = path
        self.label = label
        self.fetch_rc = None
        self.fetch_err = ""
        self.ref = "origin/main"
        self.sha = None
        self.head_sha = None
        self.behind = None
        self.reason = ""

        if not os.path.isdir(os.path.join(path, ".git")) and not os.path.isdir(path):
            self.reason = f"no such repo: {path}"
            return
        if force_fail:
            # The forced-failure control.  Not a simulation of the symptom --
            # it takes the same branch the real ssh failure takes.
            self.fetch_rc = 128
            self.fetch_err = "forced by control: fatal: could not read from remote repository"
            self.reason = "fetch failed (forced control)"
            return
        if allow_fetch:
            r = _run(["git", "-C", path, "fetch", "origin"])
            self.fetch_rc = r.returncode
            self.fetch_err = r.stderr.strip()
            if r.returncode != 0:
                self.reason = f"fetch failed rc={r.returncode}: {self.fetch_err.splitlines()[-1] if self.fetch_err else ''}"
                return
        else:
            self.fetch_rc = -1
            self.reason = "fetch skipped by flag"
            # skipping a fetch is not the same as failing one, but it is not
            # freshness either: the ref is whatever the last fetch left.

        rp = _run(["git", "-C", path, "rev-parse", "--verify", "-q",
                   "origin/main^{commit}"])
        if rp.returncode != 0:
            self.reason = "origin/main does not resolve"
            return
        self.sha = rp.stdout.strip()
        hp = _run(["git", "-C", path, "rev-parse", "--verify", "-q", "HEAD^{commit}"])
        self.head_sha = hp.stdout.strip() or None
        cb = _run(["git", "-C", path, "rev-list", "--count", "HEAD..origin/main"])
        if cb.returncode == 0 and cb.stdout.strip().isdigit():
            self.behind = int(cb.stdout.strip())

    @property
    def unknown(self):
        return self.sha is None

    def line(self):
        if self.unknown:
            return (f"  {self.label:<22} UNKNOWN  {self.reason}\n"
                    f"  {'':<22}          -> every row ranging over this repo is UNKNOWN")
        beh = "n/a" if self.behind is None else str(self.behind)
        note = "" if self.behind in (0, None) else "   <-- checkout was STALE; derived against origin/main anyway"
        return (f"  {self.label:<22} ok       ref={self.ref} sha={self.sha[:12]}\n"
                f"  {'':<22}          checkout HEAD={(self.head_sha or '?')[:12]} behind origin/main by {beh}{note}")


def git_log(repo, rev, grep=None, extra=()):
    """`--pretty` with NUL-delimited records so a body containing a newline --
    every commit message in this repo does -- cannot be mistaken for a record
    boundary.  mg-c067's own figure grammar died of exactly that."""
    fmt = "%H%x1f%an%x1f%aI%x1f%cI%x1f%s%x1f%B%x00"
    args = ["git", "-C", repo, "log", rev, f"--pretty=format:{fmt}", "--no-merges"]
    if grep is not None:
        args += ["--grep", grep, "-i", "--regexp-ignore-case"]
    args += list(extra)
    r = _run(args)
    if r.returncode != 0:
        raise RuntimeError(f"git log failed in {repo}: {r.stderr.strip()}")
    out = []
    for rec in r.stdout.split("\x00"):
        rec = rec.strip("\n")
        if not rec:
            continue
        parts = rec.split("\x1f")
        if len(parts) < 6:
            continue
        sha, an, ai, ci, subj, body = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]
        out.append(Commit(sha, an, ai, ci, subj, body))
    return out


class Commit:
    def __init__(self, sha, author, adate, cdate, subject, body):
        self.sha = sha
        self.author = author
        self.adate = parse_iso(adate)
        self.cdate = parse_iso(cdate)
        self.subject = subject
        self.body = body

    @property
    def owner(self):
        m = OWNER_RE.search(self.subject.strip())
        return m.group(1).lower() if m else None

    def names(self, tid):
        return tid.lower() in self.body.lower() or tid.lower() in self.subject.lower()

    def names_subject_only(self, tid):
        return tid.lower() in self.subject.lower()

    def tickets(self):
        return {t.lower() for t in TICKET_RE.findall(self.body)}


def parse_iso(s):
    s = s.strip()
    if not s:
        return None
    try:
        return datetime.fromisoformat(s).astimezone(timezone.utc)
    except ValueError:
        return None


def utc(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)


# --------------------------------------------------------------------------
# THE METHOD
# --------------------------------------------------------------------------
def successors(fetched, parent, instant, clock="author", subject_only=False):
    """Successor commits of `parent` at or before `instant`, in one repo.

    Returns None when the repo is UNKNOWN -- callers must NOT treat None as an
    empty list.  That confusion is the whole subject of this ticket."""
    if fetched.unknown:
        return None
    parent = parent.lower()
    hits = []
    for c in git_log(fetched.path, fetched.ref, grep=parent):
        named = c.names_subject_only(parent) if subject_only else c.names(parent)
        if not named:
            continue
        if c.owner == parent:
            continue                       # the parent's own work is not its successor
        d = c.adate if clock == "author" else c.cdate
        if d is None or d > instant:
            continue
        hits.append(c)
    hits.sort(key=lambda c: c.adate or c.cdate)
    return hits


def census_row(fetch_map, parent, instant, clock="author", subject_only=False):
    """The row verdict across every repo of the list.  UNKNOWN is sticky: one
    unreadable repo makes the whole row UNKNOWN, because a count taken over
    part of the population is not a count."""
    per_repo, unknown_repos = {}, []
    for label, f in fetch_map.items():
        s = successors(f, parent, instant, clock=clock, subject_only=subject_only)
        if s is None:
            unknown_repos.append(label)
        per_repo[label] = s
    if unknown_repos:
        return "UNKNOWN", per_repo, unknown_repos
    total = sum(len(v) for v in per_repo.values())
    return ("REFUTED" if total else "UPHELD"), per_repo, []


# --------------------------------------------------------------------------
# The work store, for the ticket-reference graph
# --------------------------------------------------------------------------
def ticket_files():
    out = {}
    for root, _dirs, files in os.walk(WORK_STORE):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            tid = fn[:-3].lower()
            if not TICKET_RE.fullmatch(tid):
                continue
            p = os.path.join(root, fn)
            # An id can appear in more than one state directory across
            # archive/; first wins and the duplicate is noted by the caller.
            out.setdefault(tid, p)
    return out


def ticket_text(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def generations(fetch_map, parent, instant, clock="author", mode="strict"):
    """The successor CHAIN, breadth-first over commits, at or before `instant`.

    Generation 1 is the commits that name `parent`.  Generation k+1 is the
    commits that name a ticket which OWNS a generation-k commit.  The descent
    is through the TREE -- ticket ids read out of commit messages -- so a
    generation exists only if it was actually COMMITTED, which is the property
    the census got wrong.  Returns None if any repo is UNKNOWN.

    ⚠️ TWO MODES, BECAUSE BLIND SPOT B7 BITES HERE AND THE SIZE OF THE BITE IS
    WORTH PRINTING.  `loose` descends on a mention anywhere in the message;
    from generation 2 on, that admits commits that merely CITE an ancestor and
    the count compounds -- it reports 7 generations and 81 commits for row 1,
    which is the whole neighbourhood, not a chain.  `strict` requires, from
    generation 2 on, that the ancestor be named in the SUBJECT, which is where
    this arc's convention puts the thing a commit is about.  Neither is the
    truth; the pair brackets it, and the gap is the measurement."""
    if any(f.unknown for f in fetch_map.values()):
        return None
    parent = parent.lower()
    seen_sha, seen_tid = set(), {parent}
    gens, frontier = [], {parent}
    depth = 0
    while frontier:
        depth += 1
        gen = []
        for label, f in fetch_map.items():
            for tid in sorted(frontier):
                for c in git_log(f.path, f.ref, grep=tid):
                    if c.sha in seen_sha:
                        continue
                    named = (c.names(tid) if (mode == "loose" or depth == 1)
                             else c.names_subject_only(tid))
                    if not named:
                        continue
                    if c.owner in seen_tid:
                        continue
                    d = c.adate if clock == "author" else c.cdate
                    if d is None or d > instant:
                        continue
                    seen_sha.add(c.sha)
                    gen.append((label, c, tid))
        if not gen:
            break
        gen.sort(key=lambda t: t[1].adate or t[1].cdate)
        gens.append(gen)
        nxt = {c.owner for _, c, _ in gen if c.owner and c.owner not in seen_tid}
        seen_tid |= nxt
        frontier = nxt
    return gens


def fetch_all(allow_fetch=True, force_fail_labels=()):
    """Fetch and resolve every repo of the list.  Called by EVERY script, so
    every transcript states for itself which ref it resolved and to what sha --
    a freshness measured once and imported is a claim, not an observation."""
    return {label: Fetched(path, label, allow_fetch=allow_fetch,
                           force_fail=(label in force_fail_labels))
            for label, path in REPOS}


def print_freshness(fetch_map):
    print("FRESHNESS -- fetched, resolved, and stated (ticket addendum 1 and 2)")
    for f in fetch_map.values():
        print(f.line())
    stale = [f.label for f in fetch_map.values() if not f.unknown and f.behind]
    if stale:
        print(f"  NOTE: {len(stale)} checkout(s) were behind origin/main at start: "
              + ", ".join(stale))
        print("        The derivation below uses origin/main, so the staleness did not")
        print("        reach the answer -- but it is stated because a census whose")
        print("        staleness is unstated is not checkable by the next reader.")
    print()


def banner(title):
    print("=" * 78)
    print(title)
    print("=" * 78)


def check(label, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f" -- {detail}" if detail else ""))
    return 0 if ok else 1
