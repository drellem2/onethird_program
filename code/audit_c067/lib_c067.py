"""mg-c067 -- shared machinery for the independent audit of the mg-132a
publication-anchor repair.

⚠️ THE POPULATION IS DERIVED HERE, NOT IMPORTED.  The thing under audit is a
claim that a named commit's tree yields a named count.  Verifying that with the
audited instrument's own `py_files_at()` would be a comparison of a function
with itself: any bug in the glob, the path filter, or the `.py` test would be
invisible because both sides would share it.  So this module walks
`git ls-tree` itself, with its own filter, and its own digest over the sorted
path list using a DIFFERENT hash (sha256, not the parent's).

The one place the parent's code IS imported is `c3_shopping.py` and
`c4_independence.py`, and there it is deliberate and the opposite case: those
scripts feed constructed inputs to `verdict_from_text()` in order to observe
what THEIR rule does.  Re-implementing the rule there would test my
understanding of it rather than the rule itself.
"""
import hashlib
import re
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True,
                      check=True).stdout.strip()


def git(*args, ok=False):
    r = subprocess.run(["git", "-C", REPO, *args], capture_output=True,
                       text=True)
    if r.returncode != 0:
        if ok:
            return None
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout


def resolve(rev):
    """`rev` as a full sha, or None.  `^{commit}` so a tag or a tree cannot
    masquerade as a commit."""
    out = git("rev-parse", "--verify", "-q", f"{rev}^{{commit}}", ok=True)
    return out.strip() if out else None


# --------------------------------------------------------------------------
# THE POPULATION -- my own derivation, sharing no code with the parent's
# --------------------------------------------------------------------------
def population_at(rev):
    """The sorted list of `.py` paths under `code/` in the tree at `rev`.

    ⚠️ WRITTEN FROM THE SCOPE STRING `code/**/*.py`, not from the parent's
    implementation.  `-r` recurses; the `blob` filter drops submodule commits
    and symlinks, which a name-only listing would silently include."""
    out = git("ls-tree", "-r", "--full-tree", rev, "--", "code/", ok=True)
    if out is None:
        return None
    paths = []
    for line in out.splitlines():
        meta, _, path = line.partition("\t")
        if not path:
            continue
        parts = meta.split()
        if len(parts) >= 2 and parts[1] == "blob" and path.endswith(".py"):
            paths.append(path)
    return sorted(paths)


def population_count(rev):
    p = population_at(rev)
    return None if p is None else len(p)


def population_key(rev):
    """A digest over the sorted path list.  sha256, deliberately NOT the
    parent's hash: two independent digests that disagree is a finding, two
    copies of one digest that agree is a tautology."""
    p = population_at(rev)
    if p is None:
        return None
    h = hashlib.sha256()
    for path in p:
        h.update(path.encode() + b"\0")
    return h.hexdigest()[:16]


def reachable(commit, frm):
    """True if `commit` is an ancestor of `frm` (or is `frm`)."""
    r = subprocess.run(["git", "-C", REPO, "merge-base", "--is-ancestor",
                        commit, frm], capture_output=True)
    return r.returncode == 0


def refs_containing(commit):
    out = git("for-each-ref", "--contains", commit,
              "--format=%(refname:short)", ok=True)
    return [x for x in (out or "").splitlines() if x]


# --------------------------------------------------------------------------
# READING A TRANSCRIPT -- again, my own regexes
# --------------------------------------------------------------------------
# The figure a transcript publishes.  Written from the shape the transcripts
# actually use ("495 .py files under `code/`"), not copied.
#
# ⚠️ THE INNER CLASS IS `[\d, ]` AND NOT `[\d,\s]`, AND THIS IS A BUG THAT WAS
# CAUGHT RATHER THAN AVOIDED.  With `\s` the group crosses a NEWLINE, and in
# this audit's own banner the line above the figure ends in a commit sha:
#
#     audited as of            : 378cf011b463
#     510 .py files under `code/` in the tree at that rev
#
# so `...b463` + newline + `510` parsed as the single figure `4611510`, and
# `C2b` -- the row asserting that every declared anchor's tree yields the
# published figure -- REFUTED on all six of this instrument's own transcripts.
# The parent's `POP_FIGURE` uses literal spaces here and never had the defect.
# An audit of figure provenance whose own figure grammar read the tail of a
# commit sha as part of the population is worth the two lines it takes to say
# so; see the third entry under `Two defects of this instrument` in README.md.
FIGURE_RE = re.compile(r"(\d[\d, ]*?)\s*`?\.py`?\s+files")
DECLARED_RE = re.compile(
    r"POPULATION ANCHOR:\s*commit=([0-9a-f]{7,40})\s+count=(\d+)"
    r"\s+digest=([0-9a-f]+)\s+scope=(\S+)")
HEX_RE = re.compile(r"\b[0-9a-f]{7,40}\b")


def published_figure(text):
    m = FIGURE_RE.search(text)
    if not m:
        return None
    return int(re.sub(r"[,\s]", "", m.group(1)))


def declared_anchor(text):
    m = DECLARED_RE.search(text)
    if not m:
        return None
    sha, count, digest, scope = m.groups()
    return {"commit": sha, "count": int(count), "digest": digest,
            "scope": scope}


# A figure stated with its commit on the same line: the anchoring form
# `out_audit_97fb.txt` uses, which is per-ROW rather than per-FILE.
INLINE_RE = re.compile(
    r"\b([0-9a-f]{7,40})\b[^\n]{0,80}?(\d[\d,]*)\s*`?\.py`?\s+files")


def figure_kind(text):
    """`QUOTED` if the first population figure sits inside quote marks,
    else `LIVE`.

    ⚠️ THIS RULE IS THIS ARC'S, NOT MINE.  `repair_7e39.py`'s `S4b` exempts a
    figure inside a QUOTATION, on the ground that a correction note has to be
    able to state the figure it corrects.  Applying it here is what keeps the
    swept population from being inflated by transcripts that merely QUOTE a
    number in order to call it stale -- which is how the first draft of `C2a`
    got the population wrong."""
    m = FIGURE_RE.search(text)
    if not m:
        return "NONE"
    lo = max(0, m.start() - 60)
    before = text[lo:m.start()]
    after = text[m.end():m.end() + 60]
    for q in ("'", '"', "`"):
        if q in before.split("\n")[-1] and q in after.split("\n")[0]:
            return "QUOTED"
    return "LIVE"


def figures_with_inline_anchors(text):
    """Every `(sha, figure, context)` where a population figure is stated on
    the same line as a commit that names it."""
    out = []
    for line in text.splitlines():
        m = INLINE_RE.search(line)
        if m:
            out.append((m.group(1), int(re.sub(r"[,\s]", "", m.group(2))),
                        line.strip()))
    return out


def blob_at(rev, path):
    return git("show", f"{rev}:{path}", ok=True)


def publishing_commit(path, as_of):
    """The commit at or before `as_of` that last wrote `path`.  This is answer
    (1)'s query, kept here so the audit can ask BOTH questions and compare
    them rather than taking the parent's word for the difference."""
    out = git("log", "-1", "--format=%H", as_of, "--", path, ok=True)
    return (out or "").strip() or None


def transcripts_publishing_a_population(as_of):
    """EVERY committed file under `code/` at `as_of` that publishes a `.py`
    population figure -- the population of this audit, swept rather than
    listed.  Returns [(path, figure)].

    ⚠️ NAMED, NOT COUNTED: the caller prints the list.  `no bare totals` is a
    rule this instrument is also bound by."""
    out = git("ls-tree", "-r", "--name-only", "--full-tree", as_of, "--",
              "code/", ok=True) or ""
    found = []
    for path in sorted(out.splitlines()):
        if not path.endswith(".txt"):
            continue
        text = blob_at(as_of, path)
        if text is None:
            continue
        fig = published_figure(text)
        if fig is not None:
            found.append((path, fig))
    return found


# --------------------------------------------------------------------------
# SCORING
# --------------------------------------------------------------------------
CHECKS = []


def record(ok, desc):
    """`ok is None` -> a measurement, neither pass nor fail."""
    tag = "MEASURED " if ok is None else ("CONFIRMED" if ok else "REFUTED  ")
    CHECKS.append((tag, desc))
    print(f"  [{tag}] {desc}")


def finding(desc):
    """A defect OF THE PARENT.  Not a refutation of one of my own controls --
    keeping the two apart is what stops a script from exiting 1 because it
    successfully found what it went looking for."""
    CHECKS.append(("FINDING  ", desc))
    print(f"  [FINDING  ] {desc}")


def head(title, rule="-"):
    print(f"\n{title}\n{rule * max(len(title), 66)}")


def banner(as_of):
    """⚠️ THE DEFECT I AM AUDITING, APPLIED TO MY OWN OUTPUT."""
    n = population_count(as_of)
    print("=" * 78)
    print("mg-c067 -- INDEPENDENT AUDIT of the mg-132a publication-anchor repair")
    print("=" * 78)
    print(f"    audited as of            : {as_of[:12]}")
    print(f"    {n} .py files under `code/` in the tree at that rev")
    print(f"    POPULATION ANCHOR: commit={as_of} count={n} "
          f"digest={population_key(as_of)} scope=code/**/*.py")
    print("""
⚠️  THIS TRANSCRIPT IS A MEASUREMENT AT THE COMMIT ABOVE, NOT A LIVE PROPERTY OF
    THE REPOSITORY.  It was written by a run, and the step that displaces it is
    A MERGE -- the refinery will rebase this file onto a tree that has grown,
    and nothing re-runs after one.  The figure above will then be RIGHT WHEN
    WRITTEN and DISPLACED, which is the parent's word and is used here on
    purpose.  Re-check with:

        sh code/audit_c067/run_all.sh --at <rev>

    An audit that printed `0 REFUTED` and let you read it as `0 now` would be
    committing the defect it was filed to examine.""")


def summary(as_of):
    n = {"CONFIRMED": 0, "MEASURED ": 0, "REFUTED  ": 0, "FINDING  ": 0}
    for tag, _ in CHECKS:
        n[tag] += 1
    head("SUMMARY")
    print(f"    checks          : {len(CHECKS)}")
    print(f"    confirmed       : {n['CONFIRMED']}")
    print(f"    measured        : {n['MEASURED ']}")
    print(f"    findings        : {n['FINDING  ']}   (defects of the PARENT)")
    print(f"    refuted         : {n['REFUTED  ']}   (controls of THIS instrument that failed)")
    print(f"\n    measured at     : {as_of[:12]}  -- re-run after any merge")
    return 1 if n["REFUTED  "] else 0


def as_of_from_argv(argv):
    rev = "HEAD"
    if "--at" in argv:
        rev = argv[argv.index("--at") + 1]
    full = resolve(rev)
    if not full:
        sys.exit(f"cannot resolve --at {rev}")
    return full
