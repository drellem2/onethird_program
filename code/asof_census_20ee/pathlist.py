#!/usr/bin/env python3
"""PATHLIST -- HOW BIG IS THE CLASS liveindex.py CAN ALREADY ANSWER ABOUT?

mg-bdc0's carry-forward, in its own words: *how many other committed
transcripts in this estate are functions of the tracked path list alone, and
therefore already checkable by this instrument at zero execution cost.*

THE ANSWER IS SMALLER THAN THE QUESTION ASSUMES, AND THAT IS THE FINDING.
`liveindex.py`'s method is cheap only because a path-list-valued figure can be
re-derived at an old commit by a SHORT RE-STATEMENT over `git ls-tree` output --
consumers.py's `freq` loop is eleven lines.  A figure that is a function of file
CONTENT cannot be re-derived that way: re-deriving it means running the
instrument at the old commit, which is TODAY'S RULE AGAINST AN OLD TREE, the
comparison liveindex.py refuses to make.  So `checkable at zero execution cost`
is a property of the PRODUCER'S INPUTS, and it is decidable from source.

    WHAT THIS FILE IS.  A NET, in census.py's sense and pinned like it, over
    every committed transcript under code/ at a declared AS_OF.  It classifies
    each transcript's PRODUCER by what that producer reads, and reports a
    FUNNEL with the drop measured at every stage rather than a single number.
    It is a HAND-RUN and is NOT in run_all.sh -- out_pathlist.txt is one dated
    run, which is pinnable.py's arrangement in this same directory and the same
    declared blind spot.

    THE RULE IS ONE-DIRECTIONAL, WHICH IS WHY IT IS WORTH HAVING.
    PATH-LIST-ONLY is a PROOF: a producer whose only repository input is a
    tracked path list has a transcript that is a function of that path list,
    necessarily, and liveindex.py's method applies to it at zero execution
    cost.  MIXED is NOT a refutation: consumers.py is MIXED -- it greps content
    in sections A, B and C -- and three of its figures are path-list-valued
    anyway.  MIXED means A READER PER FIGURE IS STILL OWED, which is exactly
    the work mg-ede8 did by hand for one transcript, and this file's claim is
    that MIXED IS THE NORMAL CASE rather than the exception.

    THE IMPORT CLOSURE IS NOT TIDINESS AND IT IS WHERE THE FIRST DRAFT WAS
    WRONG.  Scanning each producer's own file reported 32 path-list-only
    producers.  THREE OF THE FIRST THREE SPOT-CHECKED WERE FALSE POSITIVES:
    `code/audit_c067/c2_anchors.py`, `code/transcript_census_1abe/t1_population.py`
    and `code/truncate_sweep_ec63/s1_population.py` each read everything through
    a sibling `lib_*.py` that this file could not see.  A fourth,
    `code/asof_census_20ee/exemplars.py`, was a false positive for a DIFFERENT
    reason -- `git blame --line-porcelain` emits the LINE TEXT, so blame is a
    content read and the first draft's pattern did not list it.  Following
    same-directory imports and widening the read pattern takes the class from
    32 to 2.  THE MEASURED FALSE-POSITIVE DIRECTION IS THE POINT: three
    tranches running have filed successors saying `its false-positive direction
    is unmeasured`, and here it is 4 of the first 4 looked at.

    THE UNDER-COUNT IS PRINTED AND NOT HIDDEN.  A transcript is paired to its
    producer by the estate's `out_X.txt` <-> `X.py`/`X.sh` naming convention,
    which is mechanical and cannot be argued with.  It does not reach every
    transcript, and the ones it misses are COUNTED and reported by directory
    rather than dropped -- git_grep_l's defect one file over, a census that
    reports a number because it never looked.

    python3 code/asof_census_20ee/pathlist.py         # at AS_OF
    python3 code/asof_census_20ee/pathlist.py <rev>   # anywhere else
"""

import collections
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))

# The commit every figure on this page is a function of.  An ancestor of
# origin/main -- mg-20ee's condition 1 -- and the reason this transcript has a
# fixed point while several of its subjects do not.
AS_OF = "3f6d8d6"

# A TRACKED PATH LIST, in every spelling this estate uses.  `ls-files` reads the
# INDEX and `ls-tree` a named tree; `walk`/`listdir`/`glob`/`find` read the
# WORKTREE.  All four give a path list and nothing else.
PATHLIST = re.compile(
    r'os\.walk|os\.listdir|glob\.glob|glob\.iglob|\.rglob\(|'
    r'"ls-files"|"ls-tree"|\bgit ls-files\b|\bgit ls-tree\b|\bfind \.')

# ANYTHING ELSE THE REPOSITORY CAN BE ASKED FOR.  Content (`open`, `read_text`,
# `cat-file`, `show`, `grep`), history (`log`, `rev-list`, `diff`) and BLAME --
# which is in this list because `--line-porcelain` emits the line text, and
# leaving it out is what made exemplars.py read as path-list-only in the first
# draft.  A producer matching this is MIXED: some of its figures may still be
# path-list-valued, and saying WHICH needs a reader per figure.
OTHER = re.compile(
    r'\bopen\(|read_text\(|readlines\(|"cat-file"|"blame"|"show"|"log"|'
    r'"diff"|"grep"|"rev-list"|"rev-parse"|\bgit show\b|\bgit grep\b|'
    r'\bgit log\b|\bgit blame\b|\bgit diff\b|\bcat-file\b|\bcat \b')

IMPORT = re.compile(r'^\s*(?:import|from)\s+([A-Za-z_][A-Za-z0-9_]*)', re.M)
SOURCED = re.compile(r'^\s*(?:\.\s+|source\s+)\S*?([A-Za-z0-9_]+)\.sh', re.M)

_SRC = {}


def git(*args):
    got = subprocess.run(["git", "-C", ROOT, *args], capture_output=True)
    if got.returncode != 0:
        raise SystemExit("pathlist: git %s failed: %s"
                         % (" ".join(args),
                            got.stderr.decode("utf-8", "replace").strip()))
    return got.stdout.decode("utf-8", "surrogateescape")


def source_at(rev, path):
    """The bytes of `path` at `rev`.  Cached -- a lib is read once per suite."""
    key = (rev, path)
    if key not in _SRC:
        _SRC[key] = git("show", "%s:%s" % (rev, path))
    return _SRC[key]


def closure(rev, producer, tracked):
    """`producer` plus every same-directory module it pulls in, transitively.

    DECLARED AS A LIMIT: it follows imports WITHIN THE PRODUCER'S OWN DIRECTORY
    and no further, because this estate's suites are self-contained by
    convention and a cross-directory import would be a finding in itself.  A
    producer that reached outside would be UNDER-read here, and the direction of
    that error is the same as every other error in this file -- it makes the
    path-list-only class look BIGGER than it is.
    """
    here = os.path.dirname(producer)
    seen, queue = [producer], [producer]
    while queue:
        body = source_at(rev, queue.pop())
        for name in sorted(set(IMPORT.findall(body)) | set(SOURCED.findall(body))):
            for ext in (".py", ".sh"):
                cand = os.path.join(here, name + ext)
                if cand in tracked and cand not in seen:
                    seen.append(cand)
                    queue.append(cand)
    return seen


def pairs_at(rev, tracked):
    """(transcript, producer) by the estate's own naming convention, and the
    transcripts that convention does not reach.

    `code/D/out_X.txt` is produced by `code/D/X.py` or `code/D/X.sh`.  That rule
    is mechanical and reads no run_all.sh: parsing the runners was the first
    approach and it reached 18 directories of 233, because the invocation is
    written five different ways and half of them go through a shell variable.
    An under-count you can MEASURE beats a parse you cannot.
    """
    got, missed = [], []
    for path in tracked:
        base = os.path.basename(path)
        if not (path.startswith("code/") and base.startswith("out_")
                and path.endswith(".txt")):
            continue
        stem = os.path.join(os.path.dirname(path), base[4:-4])
        hit = [stem + e for e in (".py", ".sh") if stem + e in tracked]
        (got.append((path, hit[0])) if hit else missed.append(path))
    return got, missed


def scan(rev=AS_OF):
    """Every figure this file publishes, from one commit and nothing else."""
    tracked = set(git("ls-tree", "-r", "--name-only", rev).splitlines())
    pairs, missed = pairs_at(rev, tracked)
    rows = []
    for transcript, producer in pairs:
        files = closure(rev, producer, tracked)
        body = "\n".join(source_at(rev, f) for f in files)
        reads_paths = bool(PATHLIST.search(body))
        reads_other = bool(OTHER.search(body))
        rows.append({
            "transcript": transcript, "producer": producer,
            "closure": files,
            "grade": ("PATH-LIST-ONLY" if reads_paths and not reads_other
                      else "MIXED" if reads_paths
                      else "NO PATH-LIST READ"),
        })
    return {"rev": rev, "tracked": len(tracked), "rows": rows,
            "missed": missed}


def main(argv):
    rev = argv[1] if len(argv) > 1 else AS_OF
    bar = "=" * 78
    result = scan(rev)
    rows, missed = result["rows"], result["missed"]
    by = collections.Counter(r["grade"] for r in rows)

    print(bar)
    print("mg-bdc0 -- HOW MANY TRANSCRIPTS IS liveindex.py's METHOD FREE ON?")
    print(bar)
    print()
    print("  AS_OF = %s.  Every figure on this page is a function of that one" % rev)
    print("  commit, read through `git ls-tree` and `git show`, so this")
    print("  transcript has a fixed point.  NO INSTRUMENT IS EXECUTED.")
    print()

    print("-" * 78)
    print("1  THE RULE, AND WHY IT IS DECIDABLE FROM SOURCE")
    print("-" * 78)
    print()
    print("  liveindex.py is cheap because a PATH-LIST-VALUED figure can be")
    print("  re-derived at an old commit by a short re-statement over")
    print("  `git ls-tree` output.  A CONTENT-VALUED figure cannot: re-deriving")
    print("  it means running the instrument at that commit, which is today's")
    print("  rule against an old tree.  So the question `is this transcript")
    print("  already checkable` is a question about WHAT ITS PRODUCER READS,")
    print("  and that is in the source.")
    print()
    print("      PATH-LIST-ONLY  reads a tracked path list and NOTHING ELSE.")
    print("                      A PROOF: the transcript is a function of the")
    print("                      path list, so the method applies for free.")
    print("      MIXED           reads a path list AND content/history/blame.")
    print("                      NOT a refutation -- consumers.py is MIXED and")
    print("                      three of its figures are path-list-valued")
    print("                      anyway.  It means A READER PER FIGURE IS")
    print("                      STILL OWED, which is the cost mg-ede8 paid")
    print("                      by hand for one transcript.")
    print()

    print("-" * 78)
    print("2  THE FUNNEL, WITH THE DROP MEASURED AT EVERY STAGE")
    print("-" * 78)
    print()
    print("  %5d  tracked paths at this commit" % result["tracked"])
    print("  %5d  committed transcripts under code/ (out_*.txt)"
          % (len(rows) + len(missed)))
    print("  %5d  paired to a producer by the out_X.txt <-> X.py|X.sh rule"
          % len(rows))
    print("  %5d  NOT paired -- the convention does not reach them, and they"
          % len(missed))
    print("         are COUNTED here rather than dropped (see section 4)")
    print()
    print("  Of the %d paired, by what the producer and its same-directory"
          % len(rows))
    print("  imports read:")
    print()
    for grade in ("PATH-LIST-ONLY", "MIXED", "NO PATH-LIST READ"):
        print("      %-20s %5d" % (grade, by[grade]))
    print()

    print("-" * 78)
    print("3  THE PATH-LIST-ONLY CLASS, IN FULL")
    print("-" * 78)
    print()
    only = [r for r in rows if r["grade"] == "PATH-LIST-ONLY"]
    if not only:
        print("      none.")
    for r in only:
        print("      %s" % r["transcript"])
        print("          producer %s  (closure: %s)"
              % (r["producer"], ", ".join(os.path.basename(f)
                                          for f in r["closure"])))
    print()
    print("  THE ANSWER TO THE TICKET'S QUESTION IS THIS LIST AND NOT ITS")
    print("  LENGTH.  `Already checkable at zero execution cost` is %d" % len(only))
    print("  transcript(s) out of %d paired -- so the population mg-ede8's" % len(rows))
    print("  method is FREE on is not a population, and the cost it does not")
    print("  remove is the reader.  A MIXED transcript is still checkable for")
    print("  its path-list-valued figures; somebody has to say WHICH, per")
    print("  figure, per transcript, which is what mg-ede8 did once by hand.")
    print()
    print("  liveindex.py's own subject is in the MIXED class, and that is the")
    print("  non-vacuity check: the one worked example of this method is a case")
    print("  where the reader had to be written.  If consumers.py had come back")
    print("  PATH-LIST-ONLY, this file would be measuring its own pattern.")
    print()

    print("-" * 78)
    print("4  WHAT THIS FILE CANNOT SEE, COUNTED RATHER THAN DECLARED")
    print("-" * 78)
    print()
    print("  %d transcript(s) have no producer under the naming convention."
          % len(missed))
    print("  They are not classified and are NOT counted as clean.  By")
    print("  directory, largest first:")
    print()
    per = collections.Counter(os.path.dirname(p) for p in missed)
    for directory, n in per.most_common(12):
        print("      %-58s %3d" % (directory, n))
    if len(per) > 12:
        print("      ... and %d more directory/ies" % (len(per) - 12))
    print()
    print("  THE OTHER LIMIT IS THE PATTERN ITSELF AND ITS DIRECTION IS")
    print("  DECLARED: every error this file can make -- a read spelled a way")
    print("  the pattern misses, an import reaching outside its directory --")
    print("  makes PATH-LIST-ONLY look BIGGER than it is.  The first draft")
    print("  reported 32 and 4 of the first 4 adjudicated by hand were false")
    print("  positives; following imports and adding `blame` took it to %d."
          % len(only))
    print()

    print(bar)
    print("PATH-LIST: %d of %d paired transcript(s) are PATH-LIST-ONLY and so"
          % (len(only), len(rows)))
    print("           already checkable by liveindex.py's method at zero")
    print("           execution cost; %d are MIXED and owe a reader per figure;"
          % by["MIXED"])
    print("           %d read no path list at all.  %d transcript(s) are"
          % (by["NO PATH-LIST READ"], len(missed)))
    print("           unpaired and unclassified, at AS_OF %s." % rev)
    print(bar)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
