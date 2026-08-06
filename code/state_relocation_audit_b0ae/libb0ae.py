"""Shared machinery for mg-b0ae — the INDEPENDENT AUDIT of the mg-ea0e STATE.md relocation.

Every function here answers a question about BYTES OF TEXT, not about git plumbing.  This
audit deliberately does NOT use `git patch-id` as an oracle (see PREDICTIONS.md §2): 1 of 234
pairs in this arc has identical content under different patch-ids, so patch-id would answer a
question about diffs-against-bases when the question asked is "did this text survive".

THE POPULATION AND GRAIN CONVENTION.  Every count this suite prints is emitted through
`row()`, which REQUIRES a population string and a grain string.  A bare integer cannot be
printed by this instrument.  That is the label-versus-grain defect this arc keeps finding,
made structurally impossible for the numbers that go in the transcript.
"""

import hashlib
import re
import subprocess
import sys

# The audited commit and its parent.  Passed in by run_all.sh in principle; pinned here
# because they are facts about the object under audit, not about the machine.
OLD_REV = "78ae4d9"          # parent of the audited commit
NEW_REV = "cc4c663"          # the audited commit (mg-ea0e)

MARKERS = ["STRUCK", "RETRACTED", "RETIRED", "CORRECTED", "SUPERSEDED",
           "REFUTED", "DISCHARGED", "BROKEN", "withdrawn", "void"]

MG_ID_RE = re.compile(r"\bmg-[0-9a-f]{4}\b")
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")


def sh(args):
    return subprocess.run(args, capture_output=True, check=True).stdout


def git_show(rev, path):
    """Bytes of `path` at `rev`.  Bytes, not str, so byte counts are byte counts."""
    return sh(["git", "show", "%s:%s" % (rev, path)])


def git_ls(rev, prefix=""):
    cmd = ["git", "ls-tree", "-r", "--name-only", rev]
    if prefix:
        cmd.append(prefix)
    out = sh(cmd).decode()
    return [l for l in out.split("\n") if l]


def text(b):
    return b.decode("utf-8")


def rev_parse(rev):
    return sh(["git", "rev-parse", rev]).decode().strip()


# ---------------------------------------------------------------------------
# printing: no count without its population and its grain
# ---------------------------------------------------------------------------

def hdr(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def row(label, value, population, grain):
    """The ONLY way this suite prints a number.

    population -- the set the value is over, stated as a set and not as a name
    grain      -- what one unit of the value is
    """
    if population is None or grain is None:
        raise ValueError("row() refuses a count without a population and a grain")
    print("  %-46s %14s" % (label, value))
    print("      population: %s" % population)
    print("      grain:      %s" % grain)


def note(s):
    for line in s.rstrip("\n").split("\n"):
        print("  # " + line)


# ---------------------------------------------------------------------------
# atomisation: the grain at which this audit asks "did it survive"
# ---------------------------------------------------------------------------

def atomise(doc_text, source):
    """Split a document into ATOMS.

    An atom is:
      * for a markdown table row (a line whose stripped form starts and ends with '|'):
        each of its CELLS, stripped;
      * for every other line: the whole stripped line.

    Cells rather than lines, because mg-ea0e rewrote the THIRD COLUMN of seven table rows
    while leaving the first two in place.  A line-grain check on those rows can only report
    "changed" and would be unable to distinguish a relocated column from a deleted one.

    Returns list of dicts: {text, lineno, kind, col}.
    """
    atoms = []
    for i, line in enumerate(doc_text.split("\n"), start=1):
        s = line.strip()
        if not s:
            continue
        if s.startswith("|") and s.endswith("|") and s.count("|") >= 2:
            cells = s.strip("|").split("|")
            for c, cell in enumerate(cells):
                cs = cell.strip()
                if cs and set(cs) - set("-: "):     # drop the |---|---| separator row
                    atoms.append(dict(text=cs, lineno=i, kind="cell", col=c, source=source))
        else:
            atoms.append(dict(text=s, lineno=i, kind="line", col=None, source=source))
    return atoms


# ---------------------------------------------------------------------------
# the reachable corpus, derived from the file rather than from the three moves
# ---------------------------------------------------------------------------

def linked_files(new_state_text, rev):
    """Files new STATE.md links to, PARSED OUT OF THE FILE.

    Not a hand-list of mg-ea0e's three destinations: a hand-list would make this audit's
    'reachable' mean 'what the builder said it did', which is the thing under test.
    """
    tracked = set(git_ls(rev))
    found = []
    for m in LINK_RE.finditer(new_state_text):
        target = m.group(1).split("#")[0]
        if target in tracked and target not in found:
            found.append(target)
    return sorted(found)


def link_closure(new_state_text, rev):
    """The TRANSITIVE closure of markdown links out of new STATE.md.

    Returns (set_of_paths, {path: hop_distance}).  Hop 1 is a file STATE.md links to
    directly; hop 2 is a file reachable only through another file.  The distinction matters
    because mg-ea0e publishes its id result as "34 one link away" while its own verifier
    walks the closure — and a marker that only exists at hop 2 is not one link away.

    Bare-basename links inside docs/state-history/ resolve relative to that directory, which
    is how those files cite each other.
    """
    tracked = set(git_ls(rev))
    dist = {}
    frontier = []
    for m in LINK_RE.finditer(new_state_text):
        t = m.group(1).split("#")[0]
        if t in tracked and t not in dist:
            dist[t] = 1
            frontier.append(t)
    while frontier:
        nxt = []
        for p in frontier:
            body = text(git_show(rev, p))
            here = p.rsplit("/", 1)[0] if "/" in p else ""
            for m in LINK_RE.finditer(body):
                t = m.group(1).split("#")[0]
                # DEFECT D1 of this instrument, found and fixed during the run: a bare
                # `README.md` inside docs/state-history/ means the SIBLING, not the repo
                # root.  Resolving relative-to-repo-root first silently swapped a 40-line
                # index for a 6,000-byte project README and changed the closure.
                # Relative-to-the-linking-file is the markdown semantics and comes first.
                for cand in (("%s/%s" % (here, t)) if here else t, t):
                    if cand in tracked:
                        if cand not in dist:
                            dist[cand] = dist[p] + 1
                            nxt.append(cand)
                        break
        frontier = nxt
    return set(dist), dist


def diff_added_lines(old_rev, new_rev, path):
    """Lines ADDED to `path` by the commit taking old_rev -> new_rev.

    Used to separate 'this text arrived in the move' from 'this text was already here'.
    """
    out = sh(["git", "diff", "--unified=0", "%s..%s" % (old_rev, new_rev), "--", path])
    added = []
    for line in text(out).split("\n"):
        if line.startswith("+") and not line.startswith("+++"):
            added.append(line[1:])
    return added


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def commas(n):
    return "{:,}".format(n)
