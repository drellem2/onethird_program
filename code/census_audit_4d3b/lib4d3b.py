"""mg-4d3b -- the INDEPENDENT audit of mg-f3ff's census repair.

⚠️ THIS FILE SHARES NO CODE WITH `lib_f3ff.py` AND DOES NOT IMPORT IT.  Two of
its mechanics are deliberately different, so that agreement between the two is
evidence and not a tautology:

  * mg-f3ff asks git to do the matching (`git log --grep <parent> -i`) and then
    re-checks the hit in Python.  THIS reader asks git for EVERY commit
    reachable from the ref and does all matching in Python.  A defect in git's
    regex handling, its `-i` semantics, or its pathspec/encoding treatment
    cannot be shared between the two paths because only one of them uses it.
    (Both repos are small -- 387 and 428 commits -- so reading all of them
    costs nothing.)
  * mg-f3ff passes `--no-merges`, which its own POPULATION text does not
    mention.  THIS reader reads merges too and reports the difference, so the
    size of that unstated exclusion is a number rather than a worry.

WHAT THIS AUDIT RANGES OVER, stated here because the thing being audited was
required to state it and the auditor is not exempt:

  POPULATION.  Every commit reachable from `origin/main`, after a fetch whose
  exit status was checked, in the two repos mg-f3ff named.  I did not add a
  third repo: doing so would measure a different population and could not
  settle whether mg-f3ff's own figures reproduce.  That mg-f3ff's repo list is
  supplied rather than discovered is its declared blind spot B2 and remains
  one here.

  WHAT THIS AUDIT CANNOT SEE.  Everything mg-f3ff's B1-B8 cannot see, plus:
  U1 -- I did not read mg-f3ff's polecat's session, so where its transcripts
        and its code disagree I can say which, not why.
  U2 -- I compare against `origin/main` AS IT STANDS NOW.  The four rows are
        date-bounded at 2026-07-31 so later commits cannot enter them, but a
        rewritten history would be invisible to me exactly as to mg-f3ff (B4).
  U3 -- `mg show` is a channel.  Ticket titles in §D4 of PREDICTIONS.md come
        from it, and if the work store were edited after 07-31 I would not
        know.  This is the audited defect's own shape and I do not claim to be
        outside it.
"""
import os
import re
import subprocess
from datetime import datetime, timezone

# ---------------------------------------------------------------- the subject
# The four rows of the census under repair, transcribed from mg-f3ff's ROWS.
# `selftest4d3b.py` re-derives each filing instant from the work store rather
# than trusting this table -- a transcribed constant is a claim.
ROWS = [
    (1, "mg-e35b", "2026-07-31T04:13:24Z", "mg-fcf1", "no landing commit, no successor"),
    (2, "mg-fccb", "2026-07-31T04:12:41Z", "mg-d112", "no landing commit, no successor"),
    (3, "mg-a74f", "2026-07-31T04:22:15Z", "mg-16eb", "no successor"),
    (4, "mg-dffa", "2026-07-31T04:22:50Z", "mg-5800", "no successor"),
]

# Repo 1 is reached through THIS WORKTREE, which shares `.git` with
# /Users/daniel/research/onethird_program -- so `origin/main` is bit-identical
# to the source repo's, and no command of this audit runs inside a directory
# holding another agent's uncommitted state.  `a0` asserts the two agree.
HERE = os.path.dirname(os.path.abspath(__file__))
WORKTREE = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC1 = "/Users/daniel/research/onethird_program"
SRC2 = "/Users/daniel/research/one_third_width_three"
REPOS = [("onethird_program", WORKTREE), ("one_third_width_three", SRC2)]

WORK_STORE = os.path.expanduser("~/.macguffin/work")

OWNER_RE = re.compile(r"\((mg-[0-9a-f]{4})\)\s*$", re.I)
SEP = "\x1e--4d3b--\x1e"


def sh(args, cwd=None, env=None):
    e = dict(os.environ)
    if env:
        e.update(env)
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, env=e)


class Repo:
    """One repo, fetched, resolved, and carrying its own failure.

    ⚠️ `unknown` is the ONLY thing callers may branch on.  There is no code
    path in this module that turns an unreadable repo into an empty list --
    that merger is the defect this audit was sent to check for, and an auditor
    that committed it would be measuring itself."""

    def __init__(self, label, path, fetch=True, remote="origin"):
        self.label, self.path, self.remote = label, path, remote
        self.fetch_rc = None
        self.fetch_err = ""
        self.sha = None
        self.head = None
        self.behind = None
        self.reason = ""
        self._cache = None

        if not os.path.isdir(path):
            self.reason = f"no such directory: {path}"
            return
        if fetch:
            r = sh(["git", "-C", path, "fetch", remote])
            self.fetch_rc, self.fetch_err = r.returncode, r.stderr.strip()
            if r.returncode != 0:
                tail = self.fetch_err.splitlines()[-1] if self.fetch_err else "(no stderr)"
                self.reason = f"FETCH FAILED rc={r.returncode}: {tail}"
                return
        else:
            self.fetch_rc = None
            self.reason = ("NOT FETCHED IN THIS RUN -- 'I could not look' is not "
                           "'I looked and there was nothing'")
            return          # <-- deliberate: see a5, and mg-f3ff's allow_fetch
        rp = sh(["git", "-C", path, "rev-parse", "--verify", "-q",
                 f"{remote}/main^{{commit}}"])
        if rp.returncode != 0 or not rp.stdout.strip():
            self.reason = f"{remote}/main does not resolve"
            return
        self.sha = rp.stdout.strip()
        h = sh(["git", "-C", path, "rev-parse", "--verify", "-q", "HEAD^{commit}"])
        self.head = h.stdout.strip() or None
        b = sh(["git", "-C", path, "rev-list", "--count", f"HEAD..{remote}/main"])
        if b.returncode == 0 and b.stdout.strip().isdigit():
            self.behind = int(b.stdout.strip())

    @property
    def unknown(self):
        return self.sha is None

    @property
    def ref(self):
        return f"{self.remote}/main"

    def line(self):
        if self.unknown:
            return (f"  {self.label:<22} UNKNOWN   {self.reason}\n"
                    f"  {'':<22}           -> EVERY row ranging over this repo is UNKNOWN")
        beh = "n/a" if self.behind is None else str(self.behind)
        flag = "" if not self.behind else "   <-- checkout STALE; derived against the ref anyway"
        return (f"  {self.label:<22} ok        ref={self.ref} sha={self.sha[:12]}\n"
                f"  {'':<22}           HEAD={(self.head or '?')[:12]}  behind by {beh}{flag}")

    def commits(self, include_merges=True):
        """EVERY commit reachable from the ref.  No --grep: the matching is
        done in Python by the caller, which is what makes this reader
        independent of mg-f3ff's."""
        if self.unknown:
            raise RuntimeError("commits() on an UNKNOWN repo -- callers must "
                               "branch on .unknown first")
        key = include_merges
        if self._cache is not None and self._cache[0] == key:
            return self._cache[1]
        # `%x00` is git's own escape: an argv element cannot carry a literal
        # NUL, so the separator must be asked for rather than embedded.
        fmt = SEP.join(["%H", "%an", "%aI", "%cI", "%s", "%B"]) + "%x00"
        args = ["git", "-C", self.path, "log", self.ref, f"--pretty=format:{fmt}"]
        if not include_merges:
            args.append("--no-merges")
        r = sh(args)
        if r.returncode != 0:
            raise RuntimeError(f"git log failed in {self.label}: {r.stderr.strip()}")
        out = []
        for rec in r.stdout.split("\x00"):
            rec = rec.strip("\n")
            if not rec:
                continue
            f = rec.split(SEP)
            if len(f) != 6:
                raise RuntimeError(f"malformed record in {self.label}: {f[:1]}")
            out.append(Commit(self.label, *f))
        self._cache = (key, out)
        return out


class Commit:
    def __init__(self, repo, sha, author, adate, cdate, subject, message):
        self.repo, self.sha, self.author = repo, sha, author
        self.adate, self.cdate = iso(adate), iso(cdate)
        self.subject = subject
        self.message = message          # %B: subject AND body AND trailers
        self.is_merge = None            # filled by callers that care

    @property
    def owner(self):
        m = OWNER_RE.search(self.subject.strip())
        return m.group(1).lower() if m else None

    def names(self, tid):
        return tid.lower() in self.message.lower()

    def date(self, clock):
        return self.adate if clock == "author" else self.cdate


def iso(s):
    s = s.strip()
    if not s:
        return None
    try:
        return datetime.fromisoformat(s).astimezone(timezone.utc)
    except ValueError:
        return None


def utc(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)


# ------------------------------------------------------------------ the method
def successors(repo, parent, instant, clock="author", include_merges=True,
               exclude_own=True):
    """Commits naming `parent`, at or before `instant`, in ONE repo.

    Returns None -- never [] -- when the repo is UNKNOWN.

    `exclude_own` is the switch mg-f3ff hard-codes.  With it True the result is
    mg-f3ff's SUCCESSOR set (a commit owned by the parent is the parent's own
    work, not its successor).  With it False the result additionally contains
    the parent's LANDING commits, which is the OTHER premise two of the four
    row titles assert and which mg-f3ff never measures.  Making it a parameter
    is the whole of a2."""
    if repo.unknown:
        return None
    parent = parent.lower()
    hits = []
    for c in repo.commits(include_merges=include_merges):
        if not c.names(parent):
            continue
        if exclude_own and c.owner == parent:
            continue
        d = c.date(clock)
        if d is None or d > instant:
            continue
        hits.append(c)
    hits.sort(key=lambda c: (c.adate or c.cdate, c.sha))
    return hits


def row_verdict(repos, parent, instant, **kw):
    """UNKNOWN is STICKY: one unreadable repo makes the whole row UNKNOWN,
    because a count taken over part of a population is not a count."""
    per, unk = {}, []
    for r in repos:
        s = successors(r, parent, instant, **kw)
        per[r.label] = s
        if s is None:
            unk.append(r.label)
    if unk:
        return "UNKNOWN", per, unk
    n = sum(len(v) for v in per.values())
    return ("REFUTED" if n else "UPHELD"), per, []


def landings(repos, parent, instant):
    """Commits OWNED BY `parent` at or before `instant` -- the parent's own
    verdict having been committed.  This is the measurement behind the phrase
    `no landing commit`.  Returns None if any repo is UNKNOWN."""
    if any(r.unknown for r in repos):
        return None
    out = []
    for r in repos:
        for c in r.commits():
            if c.owner != parent.lower():
                continue
            d = c.adate
            if d is None or d > instant:
                continue
            out.append(c)
    out.sort(key=lambda c: (c.adate, c.sha))
    return out


def scratch_dir(prefix):
    """A throwaway directory for clones.  `MG4D3B_SCRATCH` is honoured and
    CREATED if absent -- an env var naming a path that does not exist is a
    configuration, not an error, and the first suite run died on exactly
    that."""
    import tempfile
    base = os.environ.get("MG4D3B_SCRATCH")
    if base:
        os.makedirs(base, exist_ok=True)
    return tempfile.mkdtemp(prefix=prefix, dir=base or None)


def open_repos(fetch=True, paths=None):
    src = paths if paths is not None else REPOS
    return [Repo(label, path, fetch=fetch) for label, path in src]


def freshness(repos):
    print("WHICH TREE -- fetched, resolved, stated (mg-f3ff addendum 1 and 2)")
    for r in repos:
        print(r.line())
    print()


def banner(t):
    print("=" * 78)
    print(t)
    print("=" * 78)


def check(label, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f" -- {detail}" if detail else ""))
    return 0 if ok else 1
