"""mg-cdd5 shared library -- locating the two repos, resolving citations, and
reading blobs AT A NAMED REVISION AND NEVER OFF DISK.

The single rule this file exists to enforce is E1 of PREDICTIONS.md: an
instrument sent to find "the checked-out tree is stale" must never read the
checked-out tree.  Every content read below goes through `blob_at(rev, path)`,
which is `git show <rev>:<path>` and nothing else.  There is no code path in
this module that opens a file inside the mirror repo.

The one working-copy fact that IS read is the mirror's `HEAD` -- that is the
subject of the measurement, not an input to it.
"""
import os
import re
import subprocess
import sys

# ---------------------------------------------------------------------------
# Locating the repos.  E4: `../one_third_width_three` is relative to THIS
# repo's parent, and this instrument runs inside a polecat worktree whose
# parent is /Users/daniel/.pogo/polecats/.  Naive relative resolution finds
# nothing and reports zero citations with the authority of having looked.
# ---------------------------------------------------------------------------

MIRROR_NAME = "one_third_width_three"

#: Candidate roots for the mirror repo, in order.  The environment variable
#: wins so a second host can run this without editing the file.
MIRROR_CANDIDATES = [
    os.environ.get("ONETHIRD_WIDTH_THREE"),
    os.path.expanduser("~/research/one_third_width_three"),
]


def here():
    return os.path.dirname(os.path.abspath(__file__))


def program_root():
    """This repository's root -- the worktree the instrument is committed in."""
    return git(["rev-parse", "--show-toplevel"], cwd=here()).strip()


def git(args, cwd, check=True):
    p = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError(
            "git %s in %s failed rc=%d: %s" % (" ".join(args), cwd, p.returncode,
                                               p.stderr.strip())
        )
    return p.stdout


def git_rc(args, cwd):
    p = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def find_mirror():
    """Return the mirror repo path, or None.  Never guesses by relative path."""
    for c in MIRROR_CANDIDATES:
        if not c:
            continue
        if os.path.isdir(os.path.join(c, ".git")) or os.path.isfile(
                os.path.join(c, ".git")):
            return os.path.abspath(c)
    return None


# ---------------------------------------------------------------------------
# Revisions
# ---------------------------------------------------------------------------

class RepoState(object):
    def __init__(self, path):
        self.path = path
        self.ok = path is not None
        self.head = None
        self.branch = None
        self.origin_main = None
        self.remote_main = None       # from ls-remote: the TRUE remote
        self.behind = None
        self.ahead = None
        self.dirty = None
        self.error = None


def read_state(path, do_ls_remote=True):
    """Read a repo's commit state.  `ls-remote` is a READ of the true remote;
    it moves nothing.  We deliberately do NOT fetch here -- a fetch is a
    mutation of remote-tracking refs, and s0 shows the tracking ref already
    agrees with the remote, which is a stronger statement than 'I refreshed
    it and then trusted it'."""
    st = RepoState(path)
    if path is None:
        st.error = "repo not found"
        return st
    try:
        st.head = git(["rev-parse", "HEAD"], cwd=path).strip()
        st.branch = git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=path).strip()
        st.origin_main = git(["rev-parse", "origin/main"], cwd=path).strip()
        st.dirty = bool(git(["status", "--porcelain"], cwd=path).strip())
        counts = git(["rev-list", "--left-right", "--count",
                      "HEAD...origin/main"], cwd=path).split()
        st.ahead, st.behind = int(counts[0]), int(counts[1])
        if do_ls_remote:
            rc, out, _ = git_rc(["ls-remote", "origin", "refs/heads/main"],
                                cwd=path)
            if rc == 0 and out.strip():
                st.remote_main = out.split()[0]
    except Exception as exc:                       # pragma: no cover
        st.error = str(exc)
        st.ok = False
    return st


def is_ancestor(repo, a, b):
    rc, _, _ = git_rc(["merge-base", "--is-ancestor", a, b], cwd=repo)
    return rc == 0


def short(sha, n=12):
    return sha[:n] if sha else "-"


# ---------------------------------------------------------------------------
# Blob reads.  THE ONLY CONTENT READ IN THIS INSTRUMENT.
# ---------------------------------------------------------------------------

MISSING = object()          #: distinct from "" -- E3


def blob_at(repo, rev, path):
    """Content of `path` at `rev`, or MISSING if the path does not exist there.

    E1: this is the only way this instrument reads a file in the mirror.
    E3: absence is a distinct value, not the empty string, so `absent at both
    revisions` can never compare equal to `unchanged`.
    """
    rc, out, _ = git_rc(["show", "%s:%s" % (rev, path)], cwd=repo)
    if rc != 0:
        return MISSING
    return out


# ---------------------------------------------------------------------------
# Citation extraction
# ---------------------------------------------------------------------------

#: A markdown link whose target lands in the mirror repo.
_MD = re.compile(r"\]\(([^)\s]*" + MIRROR_NAME + r"/[^)\s#]+)")
#: An HTML href doing the same (E6 -- the twin is HTML, not markdown).
_HREF = re.compile(r"""href=["']([^"'>\s]*""" + MIRROR_NAME + r"""/[^"'>\s#]+)""")
#: A bare path in backticks, e.g. `one_third_width_three/docs/foo.md:65`.
_TICK = re.compile(r"`([^`\s]*" + MIRROR_NAME + r"/[^`\s]+)`")


def _normalise(target):
    """Strip the leading `../`/`./` chain and everything up to and including the
    mirror repo name, returning a repo-relative path plus an optional :LINE.

    E4 lives here: we never join the target onto a filesystem directory.  The
    only thing taken from the link is the part AFTER `one_third_width_three/`.
    """
    i = target.find(MIRROR_NAME + "/")
    if i < 0:
        return None, None
    rel = target[i + len(MIRROR_NAME) + 1:]
    line = None
    # A cited line, or a cited RANGE.  The corpus writes ranges with an EN
    # DASH (`step8.tex:389–394`), and a `:(\d+)$` reader leaves the whole
    # `tex:389–394` in the path, where it resolves at neither revision and is
    # then reported as a BROKEN CITATION -- a parser defect wearing the
    # clothes of a corpus defect, and a worse-sounding finding than the true
    # one.  Measured, not guessed: this cost 3 false ABSENT-AT-BOTH rows on
    # the first run of this instrument (README §6, D2).
    m = re.match(r"^(.*?):(\d+)(?:\s*[-–—]\s*\d+)?$", rel)
    if m:
        rel, line = m.group(1), int(m.group(2))
    rel = rel.strip().rstrip(".,;")
    return (rel or None), line


class Citation(object):
    def __init__(self, src, srcline, raw, path, line, kind):
        self.src = src           # citing file, repo-relative
        self.srcline = srcline   # 1-indexed line in the citing file
        self.raw = raw           # the link target as written
        self.path = path         # mirror-relative path
        self.line = line         # cited line number, if the citation gave one
        self.kind = kind         # md | href | tick
        self.sections = []       # section labels cited on the same source line

    def key(self):
        return (self.src, self.srcline, self.path)

    def __repr__(self):                            # pragma: no cover
        return "<cite %s:%d -> %s>" % (self.src, self.srcline, self.path)


#: Section references that appear ALONGSIDE a link on the same line, e.g.
#: "... §5 and §5.0′" or "sec 2.3".  Used for the section-level check (E5).
_SEC = re.compile(r"(?:§|&sect;|\bsec(?:tion)?\.?\s*)\s*([0-9]+(?:\.[0-9]+)*[′'′]?)")


def extract_citations(text, src):
    """All citations to the mirror repo in `text`, with their source lines."""
    out = []
    for n, ln in enumerate(text.splitlines(), 1):
        seen_on_line = set()
        for rx, kind in ((_MD, "md"), (_HREF, "href"), (_TICK, "tick")):
            for m in rx.finditer(ln):
                path, cited_line = _normalise(m.group(1))
                if not path:
                    continue
                if (path, kind) in seen_on_line:
                    continue
                seen_on_line.add((path, kind))
                c = Citation(src, n, m.group(1), path, cited_line, kind)
                c.sections = sorted(set(_SEC.findall(ln)))
                out.append(c)
    return out


def dedupe(cits):
    """One row per (citing file, citing line, cited path)."""
    seen, out = set(), []
    for c in cits:
        if c.key() in seen:
            continue
        seen.add(c.key())
        out.append(c)
    return out


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

#: Markers whose APPEARANCE between the two revisions means the cited text was
#: withdrawn rather than merely edited.
STRIKE_MARKERS = ["~~", "STRUCK", "REFUTED", "WITHDRAWN", "RETRACTED",
                  "<del", "<s>"]

UNCHANGED = "UNCHANGED"
CHANGED = "CHANGED"
STRUCK = "CHANGED-WITH-STRIKE"
ABSENT_BOTH = "ABSENT-AT-BOTH"
ABSENT_MIRROR = "ABSENT-IN-MIRROR"
ABSENT_TIP = "DELETED-BY-TIP"
DIRECTORY = "DIRECTORY-REF"

#: Classes that mean a reader of the checked-out tree is being shown something
#: other than what is true.  DIRECTORY-REF is deliberately NOT here: "the rest
#: of `one_third_width_three/docs/`" is a reference to a directory, and
#: `git show rev:docs/` prints a tree listing that differs whenever ANY file
#: was added -- scoring that CHANGED reports 123 additions as a stale
#: citation.  It is counted, named, and kept out of the hazard tally.
HAZARD_CLASSES = (CHANGED, STRUCK, ABSENT_BOTH, ABSENT_MIRROR, ABSENT_TIP)


def is_directory_target(path):
    return path.endswith("/")


def classify(old, new, path=None):
    """Compare two blob reads.  E3: MISSING is never equal to MISSING."""
    if path is not None and is_directory_target(path):
        return DIRECTORY
    if old is MISSING and new is MISSING:
        return ABSENT_BOTH
    if old is MISSING:
        return ABSENT_MIRROR
    if new is MISSING:
        return ABSENT_TIP
    if old == new:
        return UNCHANGED
    added = _added_marker_count(old, new)
    return STRUCK if added else CHANGED


def _added_marker_count(old, new):
    """How many strike markers the tip has that the mirror does not."""
    total = 0
    for mk in STRIKE_MARKERS:
        d = new.count(mk) - old.count(mk)
        if d > 0:
            total += d
    return total


def added_markers(old, new):
    if old is MISSING or new is MISSING:
        return {}
    out = {}
    for mk in STRIKE_MARKERS:
        d = new.count(mk) - old.count(mk)
        if d > 0:
            out[mk] = d
    return out


# ---------------------------------------------------------------------------
# Section-level reading (E5)
# ---------------------------------------------------------------------------

def section_present(text, label):
    """Is a heading or bold marker for section `label` present in `text`?

    Deliberately loose: it answers 'can a reader following "§5.0′" find
    anything called that here', not 'is the section byte-identical'.  Both a
    markdown heading (`### 5.0'`) and a bare `§5.0'` mention count.
    """
    if text is MISSING:
        return False
    norm = label.replace("′", "'").replace("’", "'")
    variants = {label, norm, norm.replace("'", "′")}
    # The suffix guard, and it is the whole subtlety.  `\b` is wrong in both
    # directions here: it FAILS after a prime (`5.0'` then a space is not a
    # word boundary) and it SUCCEEDS where it must not (`5` matching inside
    # `5.0'`).  What must be excluded after the label is a prime, or a further
    # digit-bearing component -- but NOT the `.` that terminates a numbered
    # markdown heading (`## 5. Dual view`).
    guard = r"(?!['′’]|\.?[0-9])"
    for v in variants:
        e = re.escape(v)
        if re.search(r"^#{1,6}\s*" + e + guard, text, re.M):
            return True
        if re.search(r"(?:§|\bsec(?:tion)?\.?\s*)" + e + guard, text):
            return True
        if re.search(r"^\*\*" + e + guard, text, re.M):
            return True
    return False


def section_heading_set(text):
    """Every heading label this document defines, for the renumbering check."""
    if text is MISSING:
        return set()
    out = set()
    for m in re.finditer(r"^#{1,6}\s*([0-9]+(?:\.[0-9]+)*[′'′]?)", text, re.M):
        out.add(m.group(1).replace("′", "'"))
    return out


# ---------------------------------------------------------------------------
# Output helpers -- matched to the house style of code/census_repair_f3ff
# ---------------------------------------------------------------------------

BAR = "=" * 78


def banner(title):
    print(BAR)
    print(title)
    print(BAR)


def die_unreadable(msg):
    print("  UNREADABLE: %s" % msg)
    print("  This instrument reports UNKNOWN rather than an empty sweep: a")
    print("  zero produced by a repo it could not open is not a measured zero.")
    sys.stdout.flush()
