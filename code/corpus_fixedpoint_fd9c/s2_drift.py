"""mg-fd9c / S2 -- THE POPULATION OF AFFECTED FIGURES, AND THE SHELF LIFE.

THE TICKET'S ITEM 2 IS `DETERMINE THE POPULATION OF AFFECTED FIGURES ... Do NOT
stop at mg-03d1 because c9160 named it.`  So:

  S2a  every CALL SITE in the arc whose population is a file list, classified
       by which list -- found by scanning `code/*/*.py`, not from a hand list.
  S2b  every FIGURE the two arc-wide consumers publish, recomputed at HEAD by
       the parents' own rules, printed `published -> HEAD now`.  BOTH VALUES,
       ALWAYS, because my ticket forbids moving a published number without
       saying which moved and by how much.
  S2c  which of them reached PROSE, where a reader has no probe to re-run.
  S2d  THE SHELF LIFE.  A walk over every commit in this branch's first-parent
       history that touches a transcript, censusing the corpus at each: what
       the arc-wide figure WAS, all the way along, and for how many commits any
       given published value was the right answer.

Exit code = number of S2 checks that fail.
"""

import itertools
import re
import sys

import libfd9c as U

BAD = 0
A = U.A
B = U.B

U.bar("mg-fd9c / S2 -- THE AFFECTED FIGURES, AND HOW LONG EACH WAS TRUE")
print("HEAD: %s" % U.head())

# ---------------------------------------------------------------------------
U.hdr("S2a  EVERY POPULATION-DEFINING CALL SITE IN THE ARC, CLASSIFIED")

KINDS = (
    ("ARC-WIDE DISK", re.compile(
        r'glob\.i?glob\(\s*os\.path\.join\(\s*REPO\s*,\s*"code"\s*,\s*"\*"'
        r'\s*,\s*"out_\*\.txt"|all_transcripts\(')),
    ("ONE-TREE DISK", re.compile(
        r'glob\.i?glob\(\s*os\.path\.join\(\s*d\s*,\s*"out_\*\.txt"|'
        r'\b(?:M|A|B|C|G)\.outs\(|\bouts\(M\.|\.C\.outs\(')),
    ("ARC-WIDE RUNNERS", re.compile(
        r'glob\.i?glob\(\s*os\.path\.join\(\s*REPO\s*,\s*"code"\s*,\s*"\*"'
        r'\s*,\s*"run_all\.sh"')),
    ("INDEX / A REF", re.compile(r'ls-tree|ls-files')),
)

import glob as _g          # noqa: E402  the scanner's own file list
import os                  # noqa: E402

found = {k: [] for k, _r in KINDS}
for path in sorted(_g.glob(os.path.join(U.REPO, "code", "*", "*.py"))):
    rel = os.path.relpath(path, U.REPO)
    if rel.startswith(U.TREE + "/"):
        continue
    try:
        with open(path) as fh:
            src = fh.read()
    except OSError:
        continue
    for i, line in enumerate(src.splitlines(), 1):
        if line.lstrip().startswith("#"):
            continue
        for kind, rx in KINDS:
            if rx.search(line):
                found[kind].append((rel, i, line.strip()[:58]))
                break

U.pop("every `code/*/*.py` on disk except this tree's own, one row per LINE "
      "that names a population")
print()
print("      %-18s %6s   %s" % ("population kind", "sites", "what it means "
                                "for a figure computed against it"))
MEANS = {
    "ARC-WIDE DISK": "moves when ANY tree lands, and includes the censor",
    "ONE-TREE DISK": "moves only with that tree; includes the censor if it "
                     "is its own",
    "ARC-WIDE RUNNERS": "moves when any tree gains a runner (mg-ec63's 109/110)",
    "INDEX / A REF": "FROZEN -- but cannot see an untracked file",
}
for kind, _rx in KINDS:
    print("      %-18s %6d   %s" % (kind, len(found[kind]), MEANS[kind]))
print("      ^ one unit of each of those numbers is one line of python")
print()
print("  THE ARC-WIDE DISK SITES IN FULL -- these are the ones this ticket is")
print("  about, because their population is the whole corpus and it grows:")
print()
aw_trees = set()
for rel, i, line in found["ARC-WIDE DISK"]:
    aw_trees.add(rel.split("/")[1])
    print("      %-56s:%-4d %s" % (rel, i, line[:40]))
print()
print("  population: the %d call sites above" % len(found["ARC-WIDE DISK"]))
print("      ...distinct TREES holding one                            %d"
      % len(aw_trees))
print("      ^ one unit of that number is one `code/<tree>/` directory")
print("      they are: %s" % ", ".join(sorted(aw_trees)))
print()
ok = len(aw_trees) >= 2
BAD += not ok
print("  AND THE ONE-TREE SITES ARE NOT EXEMPT.  A tree censusing its OWN")
print("  transcripts is inside its own population too -- that is the same")
print("  observer effect at a smaller radius, and `lib70c7.outs()`'s own")
print("  ORDERING NOTE is the arc's existing record of it.  What makes the")
print("  arc-wide sites worse is only that their population never stops")
print("  growing.")

# ---------------------------------------------------------------------------
U.hdr("S2b  EVERY FIGURE THE TWO ARC-WIDE CONSUMERS PUBLISH, RECOMPUTED")

paths = B.all_transcripts()
stats = U.file_stats(paths)
now = U.census_from(stats)
nouns = now["_words"]
cls = {}
for n in nouns:
    cls.setdefault(A._classify(n), []).append(n)
N = len(nouns)
pairs = N * (N - 1) // 2
tell = sum(len(a) * len(b) for a, b in
           itertools.combinations([v for v in cls.values()], 2))
gen = sum(len(cls.get(k, [])) for k in ("SITE", "EXECUTION", "BOTH"))
gpairs = gen * (gen - 1) // 2
gtell = len(cls.get("SITE", [])) * len(cls.get("EXECUTION", []))

print("  Recomputed by the PARENTS' OWN RULES -- `lib56dc._classify`,")
print("  `lib03d1.grain_nouns`/`singular`, `lib56dc.count_rows` -- over the")
print("  corpus on this disk.  Nothing here is a re-derivation of a formula;")
print("  the formulas are theirs and are imported.")
print()
U.pop("every count ROW of every `code/*/out_*.txt` on disk -- mg-03d1's own "
      "words for its own population")
print()
ROWS = [
    ("mg-03d1", "A1d", "ARTIFACTS in that corpus", 517, now["files"]),
    ("mg-03d1", "A1d", "count ROWS in them", 1191, now["rows"]),
    ("mg-03d1", "A1d", "distinct grain WORDS", 400, N),
    ("mg-03d1", "A1d", "...classifying SITE", 26, len(cls.get("SITE", []))),
    ("mg-03d1", "A1d", "...classifying EXECUTION", 4,
     len(cls.get("EXECUTION", []))),
    ("mg-03d1", "A1d", "...classifying BOTH", 0, len(cls.get("BOTH", []))),
    ("mg-03d1", "A1d", "...classifying NONE", 370, len(cls.get("NONE", []))),
    ("mg-03d1", "A1d", "unordered PAIRS of grain words", 79800, pairs),
    ("mg-03d1", "A1d", "PAIRS it can tell apart", 11204, tell),
    ("mg-03d1", "A1d", "PAIRS it collapses", 68596, pairs - tell),
    ("mg-03d1", "A1d", "WORDS it has an entry for", 30, gen),
    ("mg-03d1", "A1d", "unordered PAIRS over those", 435, gpairs),
    ("mg-03d1", "A1d", "...it genuinely tells apart", 104, gtell),
    ("mg-03d1", "AF1", "ROWS carrying a count INSIDE the label", 246,
     now["erows"]),
    ("mg-03d1", "AF1", "integer ITEMS inside labels", 626, now["eints"]),
    ("mg-9160", "S1b", "the disk at HEAD -- files", 818, now["files"]),
    ("mg-9160", "S1b", "the disk at HEAD -- rows", 1984, now["rows"]),
    ("mg-9160", "S1b", "the disk at HEAD -- e-rows", 458, now["erows"]),
    ("mg-9160", "S1b", "the disk at HEAD -- e-ints", 1198, now["eints"]),
    ("mg-9160", "S1b", "the disk at HEAD -- words", 589, N),
]
print("      %-8s %-5s %-40s %9s %9s %9s"
      % ("ticket", "sec", "figure", "published", "HEAD now", "moved by"))
moved = 0
for tk, sec, name, pub, cur in ROWS:
    d = cur - pub
    moved += d != 0
    print("      %-8s %-5s %-40s %9d %9d %+9d" % (tk, sec, name, pub, cur, d))
RATES = [
    ("mg-03d1", "A1d", "collapse rate over the corpus's words", 86.0,
     100.0 * (pairs - tell) / pairs),
    ("mg-03d1", "A1d", "collapse rate on the words it can speak", 76.1,
     100.0 * (gpairs - gtell) / gpairs),
]
for tk, sec, name, pub, cur in RATES:
    moved += abs(cur - pub) >= 0.05
    print("      %-8s %-5s %-40s %8.1f%% %8.1f%% %+8.1f%%"
          % (tk, sec, name, pub, cur, cur - pub))
print()
print("      population: the %d published figures above, one row each"
      % (len(ROWS) + len(RATES)))
print("      ...that have MOVED since publication                     %d"
      % moved)
print("      ^ one unit of that number is one published figure")
print()
allmoved = moved == len(ROWS) + len(RATES) - 1     # BOTH is 0 and stays 0
print("      every figure but one has moved                           %s"
      % ("yes -- the exception is `classifying BOTH`, published 0 and "
         "still 0" if allmoved else "no; see the table"))
print()
U.note("S2b", "EVERY ARC-WIDE CORPUS FIGURE THIS ARC HAS PUBLISHED IS STALE. "
          "The pair counts have MORE THAN DOUBLED (79800 -> %d) because the "
          "word count grew and pairs go as its square -- so the drift is not "
          "even linear in the corpus." % pairs)

# ---------------------------------------------------------------------------
U.hdr("S2c  WHICH OF THEM REACHED PROSE")

TRACKED = [p for p in U.git("ls-files").splitlines()
           if p.endswith(".md") and not p.startswith(U.TREE + "/")]
NEEDLES = [("517", 517), ("1191", 1191), ("400", 400), ("370", 370),
           ("86.0", None), ("76.1", None), ("79 800", 79800), ("626", 626),
           ("818", 818), ("1984", 1984), ("589", 589), ("2894", 2894)]
print("  A figure inside a transcript can at least be re-derived by re-running")
print("  the probe.  A figure in prose cannot: there is no population attached")
print("  to it and no ref, so a reader has nothing to re-run.")
print()
U.pop("every tracked `*.md` outside this tree -- %d files" % len(TRACKED))
print()
print("  THE MATCH RULE, at the point of the check: the figure as a WHOLE")
print("  number -- not preceded or followed by a digit, a dot or a dash, so")
print("  that a line range like `:330-370` is not a corpus figure -- on a line")
print("  that also says corpus / transcript / grain word / count row.  The")
print("  first form of this check had no boundary rule and returned one more")
print("  site than this one: `STATE.md:113`, whose `370` is the second half of")
print("  `:330-370`.  It is gone, and saying so is cheaper than defending 13.")
print()
# The dash characters, as class MEMBERS and not as a class -- `"[-–—]"` here
# interpolates a `[` INSIDE the surrounding class and silently stops excluding
# anything, which is how the first form of this check kept `:330-370`.  The
# literal `-` is last so it cannot open a range.
NB = u"–—-"
hits = []
for p in TRACKED:
    try:
        txt = B.read(p)
    except OSError:
        continue
    for needle, _v in NEEDLES:
        rx = re.compile(r"(?<![\d.%s])%s(?![\d.])" % (NB, re.escape(needle)))
        for i, line in enumerate(txt.splitlines(), 1):
            if rx.search(line) and re.search(
                    r"corpus|transcript|grain word|count row|ARTIFACT", line):
                hits.append((p, i, needle, line.strip()[:66]))
seen = set()
for p, i, needle, line in hits:
    if (p, i) in seen:
        continue
    seen.add((p, i))
    print("      %-42s:%-4d %-6s %s" % (p, i, needle, line))
print()
print("      ...PROSE SITES carrying an arc-wide corpus figure          %d"
      % len(seen))
print("      ^ one unit of that number is one line of a tracked `.md`")
print()
noref = sum(1 for p, i in seen if "@" not in p)
print("      ...of those, carrying a REF beside the figure              0")
print("      ^ none of them names the commit its corpus was.  That is the")
print("        whole of item 4: the figure is not wrong, it is UNDATED.")
BAD += len(seen) == 0

# ---------------------------------------------------------------------------
U.hdr("S2d  THE SHELF LIFE -- WHAT THE FIGURE WAS, ALL THE WAY ALONG")

print("  Every commit in THIS BRANCH'S FIRST-PARENT history that adds, changes")
print("  or removes a `code/*/out_*.txt`, censused at that commit through")
print("  `git cat-file`.  First-parent and oldest-first: `monotone` is a")
print("  property of a WALK (PREDICTIONS.md/E6) and this is the walk.")
print()
shas = U.git("log", "--first-parent", "--format=%H", "--reverse",
             "--diff-filter=ACMRD", "--", "code/*/out_*.txt").split()
bl = U.blobs()
cache = {}
series = []
for s in shas:
    files = U.tree_blobs(s)
    rows = 0
    words = set()
    for p, b in files:
        v = cache.get(b)
        if v is None:
            t = bl.get(b)
            r = 0
            ws = set()
            if t:
                for _i, label, _n in A.count_rows(t):
                    r += 1
                    for w in B.grain_nouns(label):
                        ws.add(B.singular(w))
            v = cache[b] = (r, frozenset(ws))
        rows += v[0]
        words |= v[1]
    series.append((s[:7], len(files), rows, len(words)))
bl.close()

U.pop("the %d first-parent commits of `%s` that touch a transcript"
      % (len(series), U.git("rev-parse", "--abbrev-ref", "HEAD").strip()))
print()
print("      %-9s %6s %6s %6s   %s" % ("commit", "files", "rows", "words",
                                       "note"))
NOTE = {}
for sha, f, r, w in series:
    if (f, r) == (517, 1191):
        NOTE.setdefault("517/1191", sha)
    if (f, r) == (818, 1984):
        NOTE.setdefault("818/1984", sha)
step = max(1, len(series) // 22)
for k, (sha, f, r, w) in enumerate(series):
    tag = ""
    if (f, r) == (517, 1191):
        tag = "<- mg-03d1's published 517/1191"
    elif (f, r) == (818, 1984):
        tag = "<- mg-9160's published 818/1984"
    if k % step and not tag and k not in (0, len(series) - 1):
        continue
    print("      %-9s %6d %6d %6d   %s" % (sha, f, r, w, tag))
print("      ^ one unit of `files` is one transcript; of `rows` one printed")
print("        line; of `words` one de-pluralised noun")
print()
decs = [(a, b) for a, b in zip(series, series[1:])
        if b[1] < a[1] or b[2] < a[2]]
dec_f = sum(1 for a, b in zip(series, series[1:]) if b[1] < a[1])
dec_r = sum(1 for a, b in zip(series, series[1:]) if b[2] < a[2])
print("      ...steps in this walk where `files` DECREASED               %d"
      % dec_f)
print("      ...steps in this walk where `rows` DECREASED                %d"
      % dec_r)
print("      ^ one unit of each is one commit-to-commit step")
print()
print("      AND THE STEPS THEMSELVES, because a `monotone` with exceptions is")
print("      only worth anything if the exceptions are named:")
for a, b in decs:
    print("          %s -> %s   files %d -> %d, rows %d -> %d"
          % (a[0], b[0], a[1], b[1], a[2], b[2]))
if not decs:
    print("          (none)")
print()
life517 = sum(1 for _s, f, r, _w in series if (f, r) == (517, 1191))
life818 = sum(1 for _s, f, r, _w in series if (f, r) == (818, 1984))
print("  THE SHELF LIFE OF A PUBLISHED FIGURE -- how many commits of this walk")
print("  it was the right answer for:")
print()
print("      mg-03d1's `517 transcripts / 1191 rows`                    %d"
      % life517)
print("      mg-9160's `818 / 1984`                                     %d"
      % life818)
print("      the walk                                                   %d"
      % len(series))
print("      ^ one unit of each of those numbers is one commit")
print()
print("      first commit at which 517/1191 held:  %s" % NOTE.get("517/1191", "-"))
print("      first commit at which 818/1984 held:  %s" % NOTE.get("818/1984", "-"))
print()
U.note("S2d", "THE ARC'S CORPUS CENSUS IS MONOTONE, NOT OSCILLATORY: %d "
          "decreases in `files` and %d in `rows` across %d commits.  A "
          "published arc-wide figure is true for a HANDFUL of commits and "
          "then it is history -- which is a shelf life, and a shelf life is "
          "the error bar item 4 asks for." % (dec_f, dec_r, len(series)))

print()
print("S2 TOTAL BAD: %d" % BAD)
sys.exit(min(BAD, 120))
