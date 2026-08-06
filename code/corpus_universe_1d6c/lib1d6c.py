"""lib1d6c -- the universe library for mg-1d6c.

WHAT THIS IS, AND WHAT IT DELIBERATELY IS NOT.

This ticket's finding is about a UNIVERSE, so the one thing this library must not do
is introduce a second variable.  mg-aaf4 kept mg-d075's UNIT on purpose -- "so a
disagreement about a count could not hide inside a disagreement about a parser" --
and re-implemented the reader anyway.  I go one step further in the same direction:

  I IMPORT `lib_d075` AND CHANGE ONLY THE FILE LIST.

The predicate, the unit, the liveness rule, the sentence splitter and the RANK6
bound test are the parent's own code, executed, not re-typed.  So when a count of
mine differs from a count of the parent's, the difference cannot be my parser --
there is no parser of mine.  The cost of that choice is that a defect in the
parent's reader is invisible to me, and the compensation is `p2`'s cross-parser
control: the same universe is also counted through `lib_aaf4`, which shares no line
with `lib_d075`, and the two are printed side by side.  IF THE PARSERS DISAGREE
THAT IS THE FINDING, and it is bigger than the one I was sent to get.

THE UNIVERSES.  Each is a FILE LIST with its size and its derivation named at the
point of definition, because a population that is named by a pattern rather than by
its members is exactly what this ticket is about.

  G_IMPL   `os.listdir(docs)` filtered on `.endswith('.md')` -- mg-d075's universe D
           AS IMPLEMENTED.  Working tree.  NOT recursive.
  G_SHELL  the shell glob `docs/*.md` -- what the prose says.  Working tree.  Not
           recursive either; printed so the two are compared rather than assumed
           equal.
  D_TRACK  every `.md` tracked by git under `docs/`, AT ANY DEPTH.
  M_TRACK  every `.md` tracked by git, anywhere -- mg-aaf4's universe.
  M_DISK   every `.md` on disk outside `.git/`, tracked or not.
  WIDE     every tracked `.txt` and `.py` -- the population this ticket DECLARES as
           excluded, with its size, instead of drawing a pattern so that it never
           appears.

THE PREFILTER, AND WHY IT IS SOUND.  Scanning several thousand files with the
parent's parser is slow, so a file is parsed only if it contains both `33` and a
Young-Fibonacci naming string.  That is a SUPERSET of the site population by
construction: RELAXED requires `\\b33\\b` inside a sentence and a naming string
inside the unit that sentence sits in, so both substrings are present in any file
holding a site.  `p1` runs the `.md` universe BOTH WAYS and prints the difference,
so the soundness argument is checked and not merely asserted.
"""

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
D075 = os.path.join(ROOT, "code", "branching_bound_d075")
AAF4 = os.path.join(ROOT, "code", "branching_bound_audit_aaf4")

if D075 not in sys.path:
    sys.path.insert(0, D075)
import lib_d075 as L                                            # noqa: E402

DOCS = L.DOCS
DOC = L.DOC
RELDOC = "docs/OneThird-Branching-Graphs-Where-This-Lives.md"

# The two substrings a site cannot be without.  Used only as a prefilter.
PRE_FIG = re.compile(r"\b33\b")
PRE_YF = re.compile(r"Young–Fibonacci|Young-Fibonacci|\[0̂, w\]|\[∅̂, w\]")


def git(*a, **kw):
    root = kw.get("cwd", ROOT)
    return subprocess.run(["git"] + list(a), cwd=root, capture_output=True,
                          text=True).stdout


def lines(s):
    return [x for x in s.split("\n") if x.strip()]


# ------------------------------------------------------------------ universes

def u_g_impl(root=None):
    """mg-d075's universe D exactly as its code computes it."""
    d = os.path.join(root, "docs") if root else DOCS
    if not os.path.isdir(d):
        return []
    return sorted("docs/" + x for x in os.listdir(d) if x.endswith(".md"))


def u_g_shell(root=None):
    """The shell glob `docs/*.md`, run by a shell, in the working tree."""
    r = root or ROOT
    out = subprocess.run(["sh", "-c", 'ls -1 docs/*.md 2>/dev/null'], cwd=r,
                         capture_output=True, text=True).stdout
    return sorted(lines(out))


def u_d_track(commit=None):
    """Every tracked `.md` under docs/, at any depth."""
    return sorted(p for p in _tracked_md(commit) if p.startswith("docs/"))


def u_m_track(commit=None):
    """Every tracked `.md`, anywhere -- mg-aaf4's universe."""
    return sorted(_tracked_md(commit))


def u_m_disk(root=None):
    """Every `.md` on disk outside .git/, tracked or not."""
    r = root or ROOT
    out = []
    for dirpath, dirnames, filenames in os.walk(r):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for f in filenames:
            if f.endswith(".md"):
                out.append(os.path.relpath(os.path.join(dirpath, f), r))
    return sorted(out)


def u_wide(commit=None):
    """Every tracked `.txt` and `.py` -- the DECLARED exclusion."""
    if commit:
        src = git("ls-tree", "-r", "--name-only", commit)
    else:
        src = git("ls-files")
    return sorted(p for p in lines(src)
                  if p.endswith(".txt") or p.endswith(".py"))


def _tracked_md(commit=None):
    if commit:
        src = git("ls-tree", "-r", "--name-only", commit)
    else:
        src = git("ls-files")
    return [p for p in lines(src) if p.endswith(".md")]


# --------------------------------------------------------------- materialising

def materialize(commit, paths, dest):
    """Write `paths` as they stood at `commit` into `dest`, preserving layout.

    The working tree is never touched.  A path absent at that commit is skipped
    and reported by the caller as absent rather than as empty.
    """
    made = []
    for p in paths:
        blob = subprocess.run(["git", "show", "%s:%s" % (commit, p)], cwd=ROOT,
                              capture_output=True, text=True)
        if blob.returncode != 0:
            continue
        out = os.path.join(dest, p)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(blob.stdout)
        made.append(p)
    return made


# ------------------------------------------------------------------- counting

def prefilter(root, paths):
    """The sound superset: files containing both substrings anywhere."""
    keep = []
    for p in paths:
        fp = os.path.join(root, p)
        try:
            with open(fp, encoding="utf-8", errors="replace") as f:
                t = f.read()
        except (IOError, OSError):
            continue
        if PRE_FIG.search(t) and PRE_YF.search(t):
            keep.append(p)
    return keep


def sites_of(root, paths, use_prefilter=True):
    """[(path, line, kind, sentence, bounded)] under the parent's RELAXED predicate.

    Population: the live sentences of `paths`.  Grain: one sentence.  Predicate,
    unit, liveness and bound test: `lib_d075`'s, executed.
    """
    cand = prefilter(root, paths) if use_prefilter else paths
    out = []
    for p in cand:
        fp = os.path.join(root, p)
        if not os.path.isfile(fp):
            continue
        try:
            for line, kind, s, b in L.relaxed_sites(fp):
                out.append((p, line, kind, s, b))
        except (IOError, OSError, UnicodeDecodeError):
            continue
    return out


def occurrences(sites):
    """Grain O: how many times the figure is written, not how many sentences."""
    return sum(len(PRE_FIG.findall(s)) for _, _, _, s, _ in sites)


def by_file(sites):
    rows = {}
    for p, _, _, _, b in sites:
        n, nb = rows.get(p, (0, 0))
        rows[p] = (n + 1, nb + (1 if b else 0))
    return [(p, n, nb, n - nb) for p, (n, nb) in sorted(rows.items())]


def totals(sites):
    n = len(sites)
    nb = sum(1 for t in sites if t[4])
    return n, nb, n - nb


def show_rows(rows, out, width=66):
    print("    %-*s %6s %6s %6s" % (width, "file", "sites", "bnd", "unb"),
          file=out)
    for p, n, nb, nu in rows:
        print("    %-*s %6d %6d %6d" % (width, p[:width], n, nb, nu), file=out)


def show_sites(sites, out, width=98):
    for i, (p, line, kind, s, b) in enumerate(sites, 1):
        txt = re.sub(r"\s+", " ", s)
        print("  <%02d> %-56s :%-4d %-5s %-9s"
              % (i, p[-56:], line, kind, "BOUNDED" if b else "UNBOUNDED"),
              file=out)
        for j in range(0, len(txt), width):
            print("       %s" % txt[j:j + width], file=out)
        print(file=out)


def diff_sets(a, b):
    sa, sb = set(a), set(b)
    return sorted(sa - sb), sorted(sb - sa)


def rule(out, title=None):
    L.rule(out, title)


# ------------------------------------------------- the H3 numeric-scope standard

# mg-d075's s4 H3 classifies a bound as NUMERIC SCOPE iff the substring carrying it
# contains a digit.  Applied to a scope token, a bare digit is not enough: `POP-3`,
# `H3`, `s4`, `mg-d075` and `row-10` all carry digits and none of them is a count or
# a bound.  A LABEL IS NOT A SCOPE.  The exclusion list is written here, at the
# point of the check, and every accepted substring is printed per row so that the
# classifier can be argued with rather than trusted.
LABELISH = re.compile(
    r"^(?:POP-\d+|H\d+|[A-Z]\d+|s\d+|p\d+|mg-[0-9a-f]{4}|row-\d+|"
    r"[0-9a-f]{7,40}|L\d+|P\d+[a-z]?|\d+\.\d+\.\d+)$", re.I)


def numeric_scope(sub):
    """H3's standard, tightened by one clause: a digit that is a count or a bound."""
    if not sub:
        return False
    if not re.search(r"\d", sub):
        return False
    return not LABELISH.match(sub.strip().strip("`"))
