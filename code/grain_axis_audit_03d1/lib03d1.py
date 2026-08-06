"""mg-03d1 -- shared predicates for the INDEPENDENT AUDIT of the mg-56dc
label-vs-grain repair as `mg-bf79` landed it.

THE RULE THIS WHOLE DIRECTORY IS UNDER, stated once here because every probe
obeys it: **no bare totals.**  Every count printed by this tree goes through
`row()`, which takes a LABEL, a POPULATION and a GRAIN as three separate
arguments and refuses to print without all three.  It is not a formatting
helper -- it is the check.  The defect this audit is about is a count whose
label and whose grain disagreed, and the cheapest way to commit that defect
again is to have a `print("  total  %d")` anywhere in the tree.

`row()` also asserts, at print time, that the label it is given carries a grain
word ON ITS OWN LABEL under `lib56dc.grain_of` -- stage `label`, never `prev`
and never `header`.  That is the parent's P5b applied to me.

AND THE DEFECT THAT REQUIREMENT CREATES, recorded here rather than in a
footnote, because it is this audit's headline in miniature: passing that check
requires me to phrase every label in `SITE_WORDS`' vocabulary.  My subject is
grain distinctions the classifier HAS NO WORD FOR, and the self-rule obliges me
to describe them using only words it does.  See `a6_self.py`/AS3.
"""

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

sys.path.insert(0, os.path.join(REPO, "code", "runner_exit_audit_56dc"))
sys.path.insert(0, os.path.join(REPO, "code", "runner_exit_repair_70c7"))
sys.path.insert(0, os.path.join(REPO, "code", "runner_exit_repair_7522"))

import lib56dc as A            # noqa: E402  the sixth instrument, the subject
import lib70c7 as C            # noqa: E402
import lib7522 as L            # noqa: E402


# ---------------------------------------------------------------------------
# git, and reading trees
# ---------------------------------------------------------------------------

def git(*args, **kw):
    """stdout of one git command, or None when the code is in `ok`.

    LIST argv, never `shell=True`: there is no pipeline, so the status read is
    git's own.  mg-70c7's F1 with the sign that matters here.
    """
    ok = kw.pop("ok", (0,))
    p = subprocess.run(("git",) + args, cwd=REPO, capture_output=True,
                       text=True)
    if p.returncode not in ok:
        raise RuntimeError("git %s -> %d: %s"
                           % (" ".join(args), p.returncode, p.stderr[:400]))
    if p.returncode != 0:
        return None
    return p.stdout


def read(path, ref=None):
    """The bytes of one path, from the worktree or from a ref."""
    if ref is None:
        with open(os.path.join(REPO, path), encoding="utf-8",
                  errors="replace") as fh:
            return fh.read()
    return git("show", "%s:%s" % (ref, path))


def head():
    return git("rev-parse", "--short", "HEAD").strip()


def trees():
    """[str] -- every `code/<tree>` directory holding a `run_all.sh`.

    GRAIN: one item per DIRECTORY.  On disk rather than from the index, for
    `lib56dc.outs()`'s reason: a tree is untracked on the run that writes it.
    """
    import glob
    return sorted(os.path.relpath(os.path.dirname(p), REPO)
                  for p in glob.glob(os.path.join(REPO, "code", "*",
                                                  "run_all.sh")))


def all_transcripts():
    """[str] -- every `code/*/out_*.txt` on disk, repo-relative and sorted.

    GRAIN: one item per FILE.  This is the corpus every census in this tree
    ranges over, and it is named by a PROPERTY (a path glob over all of
    `code/`), not by a directory literal -- which is O2's fix applied to me.
    """
    import glob
    return sorted(os.path.relpath(p, REPO)
                  for p in glob.glob(os.path.join(REPO, "code", "*",
                                                  "out_*.txt")))


# ---------------------------------------------------------------------------
# PRINTING.  `row()` is the check, not the formatter.  See module docstring.
# ---------------------------------------------------------------------------

_BAD_LABELS = []


def hdr(title):
    print()
    print("=" * 74)
    print(title)
    print("=" * 74)
    print()


def row(label, value, population, grain, indent=6):
    """Print one count row, with its POPULATION and its GRAIN made explicit.

    `label`      what the number is called
    `value`      the number
    `population` what it ranges over -- printed on the line above when it
                 changes, so no total in this tree is bare
    `grain`      what one unit of the value IS: a row, a site, a file, a word,
                 a pair.  THIS IS THE ARGUMENT THE SUBJECT DEFECT WOULD HAVE
                 CAUGHT: `executing sites` holding a row value is exactly a
                 `grain="row"` printed under a label saying site.

    The label is checked against `lib56dc.grain_of` and must classify at stage
    `label`.  A label that does not is recorded in `_BAD_LABELS` and reported
    by `a6_self.py` rather than silently passing.
    """
    g, stage = A.grain_of(label)
    if stage != "label":
        _BAD_LABELS.append((label, g, stage))
    print("%s%-52s %6s" % (" " * indent, label, value))
    if grain is not None:
        print("%s    ^ population: %s; one unit of that number is one %s"
              % (" " * indent, population, grain))


def plain(label, value, indent=6):
    """A count row whose population and grain were stated by the caller's own
    preceding `population:` line.  Still label-checked; still never bare."""
    g, stage = A.grain_of(label)
    if stage != "label":
        _BAD_LABELS.append((label, g, stage))
    print("%s%-52s %6s" % (" " * indent, label, value))


def bad_labels():
    return list(_BAD_LABELS)


# ---------------------------------------------------------------------------
# THE GRAIN-NOUN EXTRACTOR.  My own, and deliberately NOT `lib56dc`'s.
#
# `lib56dc._classify` answers "is this label source-side or run-side".  This
# answers a different and strictly finer question: WHICH NOUN is the label's
# unit?  It is the instrument A1 needs, because you cannot measure how many
# distinctions a two-valued function collapses using that same function.
# ---------------------------------------------------------------------------

# A grain noun is the plural (or singular) common noun a count-row label uses
# for its unit.  Extracted by shape -- the LAST alphabetic word of the label,
# and any word immediately preceding an `of`/`in`/`per` -- rather than from a
# hand list, for `count_rows`' own stated reason: a hand list of interesting
# nouns is how this check would become the thing it audits.
_WORD = re.compile(r"[A-Za-z][A-Za-z-]*")
_STOP = frozenset("""
a an the of in on at to by for and or not it its this that these those is are
was were be been with without from into over under above below out outside
inside still all any both each every no none only same other another one two
three four five six seven eight nine ten more less than as but so which who
whose what when where how why now then here there such via per both-versions
version versions total totals sum summed count counts number numbers distinct
""".split())


def grain_nouns(label):
    """{str} -- the candidate grain NOUNS of one count-row label, lowercased.

    GRAIN of the return value: one item per WORD.  Deliberately over-collects
    rather than under-collects, and `a1_axes.py` prints the whole extracted
    vocabulary so a reader can disagree with any member.  A trimmed-after-the-
    fact list would make the collapse ratio a fact about my trimming.
    """
    out = set()
    ws = [w.lower() for w in _WORD.findall(label)]
    keep = [w for w in ws if w not in _STOP and len(w) > 2]
    if keep:
        out.add(keep[-1])
    for i, w in enumerate(ws):
        if w in ("of", "in", "per") and i and ws[i - 1] not in _STOP:
            out.add(ws[i - 1])
    return out


def singular(w):
    """A crude de-pluraliser, so `rows` and `row` are one grain noun.

    Crude ON PURPOSE and its crudeness is reported: `a1_axes.py` prints the
    pairs it merged, so a wrong merge is visible rather than folded into a
    ratio.
    """
    if w.endswith("ies") and len(w) > 4:
        return w[:-3] + "y"
    if w.endswith("sses") or w.endswith("shes") or w.endswith("ches"):
        return w[:-2]
    if w.endswith("ss"):
        return w
    if w.endswith("s") and len(w) > 3:
        return w[:-1]
    return w


# ---------------------------------------------------------------------------
# THE WIDER COUNT-ROW POPULATION.  THE FLOOR ITEM (AF).
#
# `lib56dc.count_rows` yields ONE (label, value-list) per line and classifies
# the line as a whole.  A label may itself contain an integer -- e.g.
#
#     ...ROWS outside it, across 10 distinct basenames            14
#
# -- which is TWO counts at TWO grains on one line.  The second is not
# mis-classified; it is never classified, because it is not in the population.
# ---------------------------------------------------------------------------

_INT_IN_LABEL = re.compile(r"(?<![\w.:#-])(\d[\d,]*)(?![\w.])")


def embedded_counts(label):
    """[(int, str)] -- (value, the word right after it) inside a count LABEL.

    GRAIN: one item per EMBEDDED COUNT.  The trailing word is the embedded
    count's own grain noun, which is what makes the two grains on the line
    comparable at all.
    """
    out = []
    for m in _INT_IN_LABEL.finditer(label):
        try:
            v = int(m.group(1).replace(",", ""))
        except ValueError:
            continue
        tail = label[m.end():]
        ws = [w for w in _WORD.findall(tail) if w.lower() not in ("distinct",)]
        out.append((v, ws[0].lower() if ws else ""))
    return out


# ---------------------------------------------------------------------------
# A SECOND (site, target) ENUMERATOR, written in this directory.
#
# Written from the STATED rule in `exec_site_rows`' docstring and from the
# prose of `out_r4_property.txt` -- "a line that executes something and names
# two different shell scripts produces two rows", "one source line is one site
# however many scripts it names".  DISCLOSURE: I had read `lib56dc`'s regexes
# before writing these, so this is a SECOND DERIVATION and not a blind one.
# Its value is not independence-in-the-strong-sense; it is that the two can be
# differenced, and every row on which they differ is printed rather than
# summarised.
# ---------------------------------------------------------------------------

_M_EXEC = re.compile(r"subprocess\s*\.|(?<![\w.])sh\s+[\"'./$]"
                     r"|\./run_[A-Za-z_]*\.sh|run_runner\s*\(")
_M_NOT = re.compile(r"[\"']git[\"']|git\s+show|git\s+-C|ls-tree")
_M_SH = re.compile(r"(?:([\w./-]+)/)?(\w[\w-]*\.sh)\b")


def my_rows(ref=None):
    """{(file, line, basename)} -- MY (site, target) rows.

    GRAIN: one member per (SITE, TARGET) PAIR.  `my_sites` below reduces the
    same set to the SITE grain, so both numbers come from one enumeration and
    the gap between them cannot be an artefact of two different scans.
    """
    if ref is None:
        files = [f for f in git("ls-files", "--", "*.py", "*.sh").splitlines()
                 if f]
    else:
        files = [f for f in git("ls-tree", "-r", "--name-only",
                                ref).splitlines() if f.endswith((".py", ".sh"))]
    out = set()
    for f in files:
        try:
            src = read(f, ref)
        except (RuntimeError, OSError):
            continue
        if src is None:
            continue
        for i, line in enumerate(src.split("\n"), 1):
            if not _M_EXEC.search(line) or _M_NOT.search(line):
                continue
            seen = set()
            for m in _M_SH.finditer(line):
                d, base = m.group(1) or "", m.group(2)
                if "%s" in d or d.startswith("/") or base in seen:
                    continue
                if d and os.path.normpath("%s/%s" % (d, base)) == \
                        os.path.normpath(f):
                    continue
                seen.add(base)
                out.add((f, i, base))
    return out


def my_sites(rows_):
    """{(file, line)} -- the SITE grain of my own rows.  One source line is
    one site however many scripts it names."""
    return {(f, i) for f, i, _b in rows_}


TWO = ("run_all.sh", "run_audit.sh")


# ---------------------------------------------------------------------------
# THE LABEL'S OWN GRAIN, at the ROW/SITE resolution `_classify` does not have.
#
# THIS FUNCTION IS THE ONE MY OWN SELF-CHECK CAUGHT (see `a6_self.py`/AS1).
# Its first version took the LAST grain noun of the label, and on
#
#     ...ROWS outside it, across 10 distinct basenames            14
#
# that is `basenames` -- the noun belonging to the EMBEDDED count, not to the
# printed one.  It reported the artifact as defective where the artifact was
# right, which is the audited defect (a value attributed to the wrong noun) run
# backwards by the auditor.  The rule below is the repair and its stage is
# returned rather than folded away, exactly as `lib56dc.grain_of` does.
# ---------------------------------------------------------------------------

_NOUN = re.compile(r"\b(rows?|sites?|basenames?|lines?|files?)\b", re.I)
_CAPS_NOUN = re.compile(r"\b(ROWS?|SITES?|BASENAMES?|LINES?|FILES?)\b")
NOUN_GRAIN = {"row": "row", "rows": "row", "site": "site", "sites": "site",
              "basename": "basename", "basenames": "basename",
              "line": "site", "lines": "site", "file": "file", "files": "file"}


def label_grain(label, above=()):
    """({grain}, stage) -- the grain THE LABEL ITSELF claims, and how it was got.

      `caps`    the grain noun is CAPITALISED.  That is this arc's own
                convention after the repair (`(site,target) ROWS`, `distinct
                executing SITES`) and it is the only marker on the line that
                says WHICH noun the number belongs to.
      `first`   no capitalised noun; the first grain noun NOT claimed by an
                embedded count (no digit within the preceding 12 characters).
      `header`  no grain noun on the label at all -- so the reader takes it
                from the column header, which is what a reader of the
                PUBLISHED version had to do.  Returned as a SET, because a
                header names several columns and the row does not say which.
    """
    m = _CAPS_NOUN.search(label)
    if m:
        return {NOUN_GRAIN[m.group(1).lower()]}, "caps"
    for m in _NOUN.finditer(label):
        if re.search(r"\d[\w\s]{0,12}$", label[:m.start()]):
            continue
        return {NOUN_GRAIN[m.group(1).lower()]}, "first"
    for ln in list(above)[:8]:
        gs = {NOUN_GRAIN[x.lower()] for x in _NOUN.findall(ln)}
        if gs:
            return gs, "header"
    return set(), "-"


def top_alts(src):
    """[str] -- the top-level `|` alternatives of a regex SOURCE, in order.

    GRAIN: one item per ALTERNATIVE.  Depth-0 split, so `(?:a|b)` inside one
    alternative stays one -- `lib7522.alternatives` counts these; this returns
    them, which is what a BY-NAME diff needs.
    """
    out, depth, cur, i = [], 0, "", 0
    while i < len(src):
        c = src[i]
        if c == "\\":
            cur += src[i:i + 2]
            i += 2
            continue
        if c == "[":
            j = src.index("]", i + 1) if "]" in src[i + 1:] else len(src) - 1
            cur += src[i:j + 1]
            i = j + 1
            continue
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        if c == "|" and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += c
        i += 1
    out.append(cur)
    return out
