"""mg-fd9c -- the instrument for THE HEAD CORPUS IS NOT A FIXED POINT.

WHAT THIS FILE MAY AND MAY NOT CONTAIN, GIVEN WHAT IT IS ABOUT.  The subject is
a MEASUREMENT APPARATUS whose readings move.  A library that re-implements the
apparatus measures its own re-typing and nothing else, so:

  IMPORTED, NEVER RESTATED.
    `lib56dc`  -- `count_rows`, `_classify`, `grain_of`, `outs`.  The row rule
                  is THE population under discussion; every row this tree
                  counts is a row `lib56dc.count_rows` returned.
    `lib03d1`  -- `all_transcripts` (the disk glob that is the whole subject),
                  `embedded_counts`, `grain_nouns`, `singular`, `read`, `git`,
                  `head`, `trees`.
    `lib9160`  -- `corpus(ref)`, `parent_corpus()`, `PARENT_REV`, `PARENT_PUB`.
                  c9160 worked out which two refs its parent's figures live at;
                  re-deriving that here would turn a disagreement about the
                  FINDING into a disagreement about a reconstruction.

  WRITTEN HERE, AND WHY EACH IS NOT A COPY.

    `census`            the same composition `s1_reproduce.py`'s local `census`
                        makes -- and it has to be written out because that one
                        is a function inside a PROBE, and importing a probe
                        runs it.  So this is a re-typing, it is the one in this
                        file, and `s0` holds it to the parent's own published
                        numbers at the parent's own reconstruction as a FORCED
                        ARM.  If my composition differs from c9160's by one
                        line, that arm goes red.
    `own_weight`        THE OBSERVER'S WEIGHT: how much of a census is the
                        censor's own transcripts.  Nothing in the arc computes
                        it, and it is the whole of the correction -- D7 reports
                        two values and calls the difference an oscillation; the
                        difference is this number.
    `orbit`             the iterated map, run IN MEMORY over the real corpus.
                        The point of doing it in memory is that a probe which
                        iterates by writing to disk cannot be run twice without
                        changing its own answer, which is the disease.
    `RENDERERS`         three transcript shapes for `orbit` to iterate.  Two of
                        them are NEGATIVE CONTROLS that must cycle, because a
                        detector that reports `no oscillation` is worth nothing
                        until it has been shown able to report one.
    `blobs`             a `git cat-file --batch` reader, so a walk over the
                        arc's history costs one subprocess and not 825 per
                        commit.  Reading, never writing; no ref is created and
                        no worktree is touched.
    `state_of`          the STABILITY CLASS of a figure's population -- the
                        convention this ticket exists to decide.  Adopted from
                        `corpus_universe_1d6c`'s STATE A/B/C, which named the
                        idea for one file list and never generalised it.

WHAT THIS TREE NEVER DOES.  It writes nothing outside its own directory, runs
no other tree's runner, and creates no ref.  Every historical figure is read
through `git cat-file`, which cannot mutate anything.  `x1_orbit.py` is the one
probe that runs another tree's suite, it does it in a THROWAWAY CLONE under a
directory you name on the command line, it is not in `run_all.sh`, and it
refuses to start if the path it is given is inside this repository.
"""

import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

for _p in ("code/runner_exit_audit_56dc", "code/grain_axis_audit_03d1",
           "code/grain_arity_9160"):
    sys.path.insert(0, os.path.join(REPO, _p))

import lib56dc as A            # noqa: E402  the row rule
import lib03d1 as B            # noqa: E402  the disk glob
import lib9160 as G            # noqa: E402  the reconstruction

TREE = "code/corpus_fixedpoint_fd9c"
read = B.read
git = B.git
head = B.head
bar = A.bar
finding = A.finding
hdr = B.hdr


def note(fid, text, width=74):
    """One `FINDING:` line, wrapped.  `lib56dc.finding` RETURNS the string and
    does not print it, and every runner in this arc greps `^FINDING:`, so the
    first line has to start there and the continuations have to not."""
    import textwrap
    for i, ln in enumerate(textwrap.wrap(A.finding(fid, text), width)):
        print(ln if i == 0 else "         " + ln)


def plain(label, value, indent=6):
    print("%s%-56s %8s" % (" " * indent, label, value))


_HEAD = [None]


def at():
    """The ref every population line in this tree is dated by.

    It is the tip of the branch AS THE PROBE RUNS, which is the commit BEFORE
    the one that publishes the transcript -- so a reader reproducing a figure
    here must check out this ref and not the publishing commit.  That is the
    same one-commit offset every tree in this arc has and none of them says so.
    """
    if _HEAD[0] is None:
        _HEAD[0] = head()
    return _HEAD[0]


def pop(text, indent=2, ref=None):
    """A population line, DATED.  S4's checker requires the date; this tree
    obeys its own convention by having exactly one function that prints these
    and no way to print one without a ref."""
    print("%spopulation: %s   @%s" % (" " * indent, text, ref or at()))


# ---------------------------------------------------------------------------
# THE CENSUS.  Composed from the parent instruments; held to c9160's published
# numbers by a forced arm in `s0`.
# ---------------------------------------------------------------------------

FIELDS = ("files", "rows", "erows", "eints", "words")


def census(texts):
    """{files,rows,erows,eints,words} over an iterable of transcript TEXTS.

    GRAIN, field by field: one FILE; one printed LINE that `count_rows`
    returns; one printed LINE carrying an integer inside its label; one INTEGER
    inside a label; one de-pluralised NOUN.  These are mg-03d1's five grains
    and mg-9160's five columns, and they are named here so a reader can check
    that the composition is theirs and not a fourth one.
    """
    rows = erows = eints = 0
    words = set()
    n = 0
    for t in texts:
        n += 1
        if t is None:
            continue
        for _i, label, _nums in A.count_rows(t):
            rows += 1
            e = B.embedded_counts(label)
            if e:
                erows += 1
                eints += len(e)
            for w in B.grain_nouns(label):
                words.add(B.singular(w))
    return {"files": n, "rows": rows, "erows": erows, "eints": eints,
            "words": len(words), "_words": words}


def census_disk(paths=None):
    paths = B.all_transcripts() if paths is None else paths
    return census(read_all(paths))


def read_all(paths):
    for p in paths:
        try:
            yield B.read(p)
        except OSError:
            yield None


def fmt(c):
    return "%6d %6d %6d %6d %6d" % tuple(c[f] for f in FIELDS)


HEADFMT = "%6s %6s %6s %6s %6s" % FIELDS


# ---------------------------------------------------------------------------
# THE OBSERVER'S WEIGHT.  The correction to D7.
# ---------------------------------------------------------------------------

def file_stats(paths=None):
    """[(path, rows, erows, eints, wordset)] -- the census, ONE FILE AT A TIME.

    The whole-corpus census is the sum of these in four fields and the UNION in
    the fifth, and that asymmetry is the reason this exists: `rows`, `erows`
    and `eints` are additive over files, so a tree's contribution to them is
    its own rows.  `words` is not -- a noun two trees both use is removed by
    neither -- so a tree's contribution to the word count is the nouns that
    occur in ITS transcripts AND NOWHERE ELSE.  `weight_of` below is the only
    place in this tree that gets to know that.
    """
    paths = list(B.all_transcripts() if paths is None else paths)
    out = []
    for p in paths:
        try:
            t = B.read(p)
        except OSError:
            t = None
        rows = erows = eints = 0
        ws = set()
        if t is not None:
            for _i, label, _nums in A.count_rows(t):
                rows += 1
                e = B.embedded_counts(label)
                if e:
                    erows += 1
                    eints += len(e)
                for w in B.grain_nouns(label):
                    ws.add(B.singular(w))
        out.append((p, rows, erows, eints, ws))
    return out


def census_from(stats):
    words = set()
    for _p, _r, _er, _ei, ws in stats:
        words |= ws
    return {"files": len(stats),
            "rows": sum(s[1] for s in stats),
            "erows": sum(s[2] for s in stats),
            "eints": sum(s[3] for s in stats),
            "words": len(words), "_words": words}


def weight_of(stats, hit):
    """The observer's weight of the files `hit(path)` selects, from `stats`.

    Equal, field for field, to `own_weight`'s delta -- and `s0` holds the two
    against each other on a real tree, because a fast path that disagrees with
    the reference is a second answer and not a speed-up.
    """
    mine = [s for s in stats if hit(s[0])]
    theirs_words = set()
    for p, _r, _er, _ei, ws in stats:
        if not hit(p):
            theirs_words |= ws
    my_words = set()
    for _p, _r, _er, _ei, ws in mine:
        my_words |= ws
    return {"files": 0,
            "rows": sum(s[1] for s in mine),
            "erows": sum(s[2] for s in mine),
            "eints": sum(s[3] for s in mine),
            "words": len(my_words - theirs_words)}


def own_weight(tree, paths=None):
    """(present, absent, delta) censuses for one TREE's own transcripts.

    `present` is the corpus as globbed.  `absent` is the SAME FILE LIST with
    that tree's own transcripts read as EMPTY -- which is exactly what a plain
    `>` redirect leaves on disk while the probe that will fill it is running.
    `delta` is the observer's weight, field by field.

    THE FILE IS NOT REMOVED FROM THE LIST.  `>` truncates; it does not unlink.
    That is why `files` is unchanged in the delta and every other field moves,
    and it is the fingerprint that tells a TRUNCATION apart from a corpus that
    genuinely lacks the file.
    """
    paths = list(B.all_transcripts() if paths is None else paths)
    if tree.endswith(".txt"):
        hit = lambda p: p == tree            # noqa: E731  one FILE's weight
    else:
        pre = tree.rstrip("/") + "/"
        hit = lambda p: p.startswith(pre)    # noqa: E731  one TREE's weight
    present = census(read_all(paths))
    absent = census("" if hit(p) else t
                    for p, t in zip(paths, read_all(paths)))
    delta = {f: present[f] - absent[f] for f in FIELDS}
    return present, absent, delta


# ---------------------------------------------------------------------------
# THE ITERATED MAP, IN MEMORY.
# ---------------------------------------------------------------------------

def _rows_of(text):
    return len(A.count_rows(text))


def _row_line(label, value):
    """One line in `lib56dc._COUNT_ROW`'s shape -- and NOT a line that merely
    looks like one.

    THE FIRST FORM OF THIS FUNCTION USED A SINGLE SPACE and `count_rows`
    returned 0 for every transcript the renderers below produced.  The whole
    orbit was then a constant map, every renderer `converged`, and the
    fixed-point headline would have been VACUOUS -- true of a state that never
    entered the census.  `_rows_of` is asserted against the intended count at
    every renderer, in `S0`, for that reason.
    """
    return "      %-52s  %d\n" % (label, value)


def r_fixed(c):
    """A transcript whose SHAPE does not depend on the value it reports.

    Every probe in `mg-9160` and `mg-03d1` has this shape: the census is
    printed as a fixed number of rows whatever those rows say.  `len(FIELDS)`
    rows, always.
    """
    return "".join(_row_line("...%s in the corpus" % f, c[f]) for f in FIELDS)


def make_cycler(base_rows, period):
    """NEGATIVE CONTROL: a renderer whose orbit has EXACTLY `period`.

    A detector that has only ever reported `period 1` is not a detector.  This
    builds a transcript shape that provably cannot settle, and it builds it to
    a NAMED period so that `S0` can check the detector reports the right one
    and not merely `something other than 1`.

    The construction, and why it works.  Let `b` be the row count of the corpus
    WITHOUT the virtual transcript.  The renderer emits `k` rows, so the next
    census reads `b + k`.  Define

        k(b + j) = (j mod P) + 1   for j in 1..P,      k(t) = 1 otherwise

    and the orbit walks `b -> b+1 -> b+2 -> ... -> b+P -> b+1`, which has no
    fixed point because `k(b+j) = j` would require `j = (j mod P) + 1`, false
    for every `j` in `1..P` when `P >= 2`.  The shape follows the value; that
    is the only property that distinguishes it from every real arc probe.
    """
    def render(c):
        j = c["rows"] - base_rows
        k = (j % period) + 1 if 1 <= j <= period else 1
        return "".join(_row_line("...arm %d of a cycling census" % i, c["rows"])
                       for i in range(k))
    return render


def orbit(renderer, k=24, paths=None):
    """[(census, state_text)] -- the map `T -> render(census(corpus + T))`.

    This is `the tree writes into the population it counts`, in memory: the
    virtual transcript T joins the corpus that produces the next T.  Nothing is
    written to disk, which is the only reason this probe can be run twice and
    give the same answer.

    Returns the orbit and (start, period) of the cycle it falls into, found by
    hashing the state text.  Every finite deterministic map on a finite state
    space has a cycle; `period == 1` is a FIXED POINT.
    """
    paths = list(B.all_transcripts() if paths is None else paths)
    base_texts = list(read_all(paths))
    seen = {}
    out = []
    state = ""
    for i in range(k):
        c = census(base_texts + [state])
        h = hashlib.sha256(state.encode()).hexdigest()[:12]
        if h in seen:
            return out, seen[h], i - seen[h]
        seen[h] = i
        out.append((c, state))
        state = renderer(c)
    return out, None, None


# ---------------------------------------------------------------------------
# HISTORY.  Read-only, one subprocess for every blob in the walk.
# ---------------------------------------------------------------------------

_OUT = re.compile(r"^code/[^/]+/out_[^/]*\.txt$")


def commits_touching_corpus(limit=None):
    """[sha] -- first-parent commits of HEAD that touch a `code/*/out_*.txt`.

    FIRST-PARENT and oldest-first, stated because `monotone` is a property of
    a WALK and not of a repository (PREDICTIONS.md/E6).
    """
    out = git("log", "--first-parent", "--format=%H", "--reverse",
              "--", "code/").splitlines()
    shas = []
    for s in out:
        s = s.strip()
        if not s:
            continue
        names = git("show", "--name-only", "--format=", s).splitlines()
        if any(_OUT.match(n.strip()) for n in names):
            shas.append(s)
    return shas[-limit:] if limit else shas


def tree_blobs(sha):
    """[(path, blob)] -- every `code/*/out_*.txt` at one commit, with its sha."""
    out = []
    for line in git("ls-tree", "-r", sha).splitlines():
        meta, _, path = line.partition("\t")
        if not _OUT.match(path.strip()):
            continue
        parts = meta.split()
        if len(parts) >= 3 and parts[1] == "blob":
            out.append((path.strip(), parts[2]))
    return out


class blobs(object):
    """`git cat-file --batch` as a dict-like cache.  READS ONLY.

    A history walk needs the same blob many times -- a transcript that never
    changes is one blob at every commit after the one that wrote it -- so the
    cache is what makes the walk affordable, and the batch process is what
    keeps it to one subprocess instead of one per file per commit.
    """

    def __init__(self):
        self.p = subprocess.Popen(
            ["git", "cat-file", "--batch"], cwd=REPO, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
        self.cache = {}

    def get(self, sha):
        if sha in self.cache:
            return self.cache[sha]
        self.p.stdin.write((sha + "\n").encode())
        self.p.stdin.flush()
        hdr_line = self.p.stdout.readline().decode()
        parts = hdr_line.split()
        if len(parts) != 3:
            self.cache[sha] = None
            return None
        n = int(parts[2])
        data = self.p.stdout.read(n)
        self.p.stdout.read(1)
        t = data.decode("utf-8", "replace")
        self.cache[sha] = t
        return t

    def close(self):
        try:
            self.p.stdin.close()
            self.p.wait(timeout=10)
        except Exception:
            self.p.kill()


# ---------------------------------------------------------------------------
# THE CONVENTION.  `corpus_universe_1d6c`'s STATE A/B/C, generalised.
# ---------------------------------------------------------------------------

CLASSES = {
    "FROZEN": ("the population is a COMMIT.  The figure is a constant and a "
               "re-run reproduces it byte for byte, forever."),
    "GROWING": ("the population is the ARC.  The figure is a measurement dated "
                "by a commit; it moves when anything lands, and the honest "
                "published form carries the ref."),
    "OBSERVED": ("the population INCLUDES THE OBSERVER.  On top of GROWING, "
                 "the reading depends on whether the observer's own transcript "
                 "was on disk when the census ran -- so the honest published "
                 "form is an INTERVAL of known width, not a number."),
}


def state_of(population_is_a_ref, observer_in_population):
    """The stability class of a figure, from two facts about its population."""
    if population_is_a_ref:
        return "FROZEN"
    return "OBSERVED" if observer_in_population else "GROWING"


def render_figure(value, cls, low=None, ref=None):
    """The published FORM of a figure, given its class.  This is the answer to
    the ticket's item 4, and it is deliberately a rendering rule and not a
    prose rule, so that a checker can tell whether a transcript obeys it."""
    if cls == "FROZEN":
        return "%d @%s" % (value, ref or "?")
    if cls == "GROWING":
        return "%d @%s (GROWING)" % (value, ref or "?")
    return "%d-%d @%s (OBSERVED)" % (low if low is not None else value, value,
                                     ref or "?")
