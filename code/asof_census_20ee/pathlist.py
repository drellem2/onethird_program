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

    THE IMPORT CLOSURE IS NOT TIDINESS AND IT IS WHERE EVERY DRAFT HAS BEEN
    WRONG, TWICE, IN THE SAME DIRECTION.  Scanning each producer's own file
    reported 32 path-list-only producers.  THREE OF THE FIRST THREE
    SPOT-CHECKED WERE FALSE POSITIVES: `code/audit_c067/c2_anchors.py`,
    `code/transcript_census_1abe/t1_population.py` and
    `code/truncate_sweep_ec63/s1_population.py` each read everything through a
    sibling `lib_*.py` that the scan could not see.  A fourth,
    `code/asof_census_20ee/exemplars.py`, was a false positive for a DIFFERENT
    reason -- `git blame --line-porcelain` emits the LINE TEXT, so blame is a
    content read and that draft's pattern did not list it.  Following
    SAME-DIRECTORY imports and widening the read pattern took the class from 32
    to 2.

    THEN BOTH SURVIVORS WERE ADJUDICATED BY HAND AND BOTH WERE FALSE TOO, for
    the third draft's own DECLARED limit rather than for a new reason -- which
    is the part worth keeping.  `code/verdict_audit_f911/a1_controls.py` and
    `code/verdict_staleness_30bd/prose_30bd.py` each `sys.path.insert` a
    directory that is NOT their own and import a lib from it
    (`code/verdict_delivery_bf3f/lib_bf3f.py`,
    `code/runner_exit_repair_7522/lib7522.py`), and BOTH of those libs are
    heavy content readers -- `open(`, `json.load(open(`, `git show`.  A closure
    that stopped at the directory boundary could not see either, and the draft
    that stopped there had written down, in this docstring, that stopping there
    would make the class LOOK BIGGER THAN IT IS.  It did, by exactly the whole
    class.  So the closure now resolves an import to ANY tracked module of that
    name in the estate, preferring the producer's own directory.

    SO THE FALSE-POSITIVE DIRECTION IS NOT AN ESTIMATE HERE.  SIX of the six
    candidates ever adjudicated by hand -- 32 -> 2 -> 0 -- have been false, and
    the class is EMPTY at AS_OF.  That is the answer to the ticket's question
    and it is a stronger one than a small number would have been: mg-ede8's
    method is free on NOTHING, and the reader it cost is not an overhead that
    amortises over a population.

    THE UNDER-COUNT IS PRINTED AND NOT HIDDEN.  A transcript is paired to its
    producer by the estate's `out_X.txt` <-> `X.py`/`X.sh` naming convention,
    which is mechanical and cannot be argued with.  It does not reach every
    transcript, and the ones it misses are COUNTED and reported by directory
    rather than dropped -- git_grep_l's defect one file over, a census that
    reports a number because it never looked.

    AND THIS FILE FAILED ITS OWN HEADLINE CLAIM ON ITS FIRST RE-RUN, WHICH IS
    WHY THE ORDERING IS NOW DECLARED RATHER THAN INCIDENTAL.  It prints `this
    transcript has a fixed point`, and it did not have one: `tracked` was a
    SET, section 4's per-directory table broke ties in dict-insertion order, and
    three runs at one commit produced three different tables.  A transcript
    whose subject is figures that were already wrong at their own commit,
    published as a function of PYTHONHASHSEED, is this directory's subject
    arriving inside the file that measures it.  Every walk over `tracked` is
    sorted now and the tie-break is `(-count, name)`, written down instead of
    inherited.  P43 pins it.

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
# fixed point while several of its subjects do not.  It was the tip of
# origin/main when the measurement was TAKEN and it is not the tip when this
# file LANDS -- mg-5058's semantic.py and code/coarse_unit_fa83 came in while
# this branch sat in the merge queue -- and that gap is the arrangement rather
# than a defect in it.  A PIN AGES AND SAYS SO; the alternative is the live
# figure this whole directory exists to complain about.  worklist.py pins at
# 07a2fd0 and exemplars.py at 0cb0fa4 for the same reason.
AS_OF = "d2d7437"

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
    r'\bgit log\b|\bgit blame\b|\bgit diff\b|\bcat-file\b|\bcat \b|'
    # RUNNING SOMETHING THAT IS NOT git.  A producer that shells out to another
    # binary and reads its stdout is reading a repository input that is neither
    # a path list nor any spelling above -- `a1_controls.py` runs the real `mg`
    # against a sandbox, which matched NEITHER pattern until this clause.  It is
    # narrow on purpose: an argv whose first word is a CONSTANT or an
    # interpreter, plus the two shell-outs that take a string, so a producer
    # whose only subprocess is `git` is untouched.
    #
    # IT IS INERT TODAY AND THAT IS MEASURED, NOT HOPED: re-grading all 840
    # paired producers with this clause amputated moves EXACTLY 0 of them,
    # because `a1_controls.py` is already MIXED through the foreign lib the
    # closure now follows.  It is kept, declared inert, because the shape it
    # names is real and was found in this corpus, and because widening the
    # CONTENT side can only ever move a producer OUT of a class whose
    # membership is a claim of proof -- the direction that cannot publish a
    # false one.  P42 keeps it from being dead code by firing it on the
    # exhibited shape; if P42 ever goes red alone, this clause was quietly
    # broken while its inertness kept the transcript silent.
    r'os\.system\(|os\.popen\(|shutil\.which\(|'
    r'subprocess\.\w+\(\s*\[\s*(?:[A-Z][A-Z_0-9]{2,}|sys\.executable|'
    r'["\'](?:sh|bash|python3?|make)["\'])')

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


def module_index(tracked):
    """module name -> every tracked path in the estate that could supply it.

    Sorted, so the closure it feeds does not depend on set iteration order.
    """
    index = collections.defaultdict(list)
    for path in sorted(tracked):
        base = os.path.basename(path)
        if base.endswith((".py", ".sh")):
            index[base.rsplit(".", 1)[0]].append(path)
    return index


def closure(rev, producer, index):
    """`producer` plus every tracked module it pulls in, transitively.

    IT DOES NOT STOP AT THE DIRECTORY BOUNDARY, AND THE DRAFT THAT DID IS WHY.
    This estate's suites are self-contained BY CONVENTION and not by
    construction: `a1_controls.py` and `prose_30bd.py` each `sys.path.insert` a
    foreign directory and import a content-reading lib out of it, and a
    same-directory closure could see neither.  Those two were the ENTIRE
    path-list-only class, so the limit the previous draft declared in prose was
    also, quantitatively, the whole answer.

    THE RESOLUTION IS BY MODULE NAME AND IS DELIBERATELY OVER-WIDE: where the
    producer's own directory supplies the name, that file alone is read; where
    it does not, EVERY tracked module of that name is read.  Resolving
    `sys.path` properly would mean evaluating it, and reading a file too many
    can only move a producer from PATH-LIST-ONLY to MIXED -- the direction that
    SHRINKS a class whose membership is a claim of proof.  Reading one too few
    is the direction that publishes a false proof, and that is the trade this
    picks, stated rather than left to be inferred.
    """
    here = os.path.dirname(producer)
    seen, queue = [producer], [producer]
    while queue:
        body = source_at(rev, queue.pop())
        for name in sorted(set(IMPORT.findall(body)) | set(SOURCED.findall(body))):
            cands = [p for p in index.get(name, ())
                     if os.path.dirname(p) == here] or index.get(name, [])
            for cand in cands:
                if cand not in seen:
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

    THE WALK IS SORTED AND THAT IS LOAD-BEARING, NOT TIDINESS.  `tracked` is a
    set; iterating it put `missed` in hash order, and section 4's tie-break
    inherited that order from dict insertion, so this file's own table was a
    function of PYTHONHASHSEED and NOT of the commit it declares.  Three runs at
    one commit, three tables.  P43.
    """
    got, missed = [], []
    for path in sorted(tracked):
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
    index = module_index(tracked)
    rows, foreign = [], 0
    for transcript, producer in pairs:
        files = closure(rev, producer, index)
        if any(os.path.dirname(f) != os.path.dirname(producer) for f in files):
            foreign += 1
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
            "missed": missed, "foreign": foreign}


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
    print("  Of the %d paired, by what the producer and every module it"
          % len(rows))
    print("  imports read -- the closure does NOT stop at the directory:")
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
    print("  `Already checkable at zero execution cost` is %d transcript(s)" % len(only))
    print("  out of %d paired, so mg-ede8's method is free on NOTHING and the" % len(rows))
    print("  cost it does not remove is the reader.  A MIXED transcript is")
    print("  still checkable for its path-list-valued figures; somebody has to")
    print("  say WHICH, per figure, per transcript, which is what mg-ede8 did")
    print("  once by hand.  THE ANSWER IS THE EMPTY LIST AND NOT THE NUMBER 0:")
    print("  the class is empty because every candidate was adjudicated and")
    print("  died, not because nothing was looked at.")
    print()
    print("  AN EMPTY CLASS AND A BROKEN DETECTOR PRINT THE SAME PAGE, so this")
    print("  one is falsifiable by construction elsewhere: P40 feeds the real")
    print("  grader a producer that reads `git ls-tree` and NOTHING else and")
    print("  requires PATH-LIST-ONLY, so a rule that can no longer fire is a")
    print("  RED control and not a quieter transcript.")
    print()
    print("  liveindex.py's own subject is in the MIXED class, and that is the")
    print("  non-vacuity check from the other side: the one worked example of")
    print("  this method is a case where the reader had to be written.  If")
    print("  consumers.py had come back PATH-LIST-ONLY, this file would be")
    print("  measuring its own pattern.")
    print()
    print("  %d of the %d paired producers have a closure reaching OUTSIDE" % (result["foreign"], len(rows)))
    print("  their own directory, which is the repair that emptied this class:")
    print("  a same-directory closure could not see any of them.")
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
    # (-count, name): DECLARED, because most_common breaks ties in insertion
    # order and insertion order used to come off a set.  See P43.
    ordered = sorted(per.items(), key=lambda kv: (-kv[1], kv[0]))
    for directory, n in ordered[:12]:
        print("      %-58s %3d" % (directory, n))
    if len(per) > 12:
        print("      ... and %d more directory/ies" % (len(per) - 12))
    print()
    print("  THE OTHER LIMIT IS THE PATTERN ITSELF AND ITS DIRECTION IS")
    print("  DECLARED: every error this file can still make -- a read spelled")
    print("  a way the pattern misses -- makes PATH-LIST-ONLY look BIGGER than")
    print("  it is, and the class is already empty, so the residue is a class")
    print("  that cannot be smaller than it is.  N33.")
    print()
    print("  AND THIS FILE IS OUTSIDE ITS OWN POPULATION, DECLARED HERE RATHER")
    print("  THAN LEFT TO BE FOUND: the AS_OF pin is older than pathlist.py, so")
    print("  out_pathlist.txt is not tracked at the commit it reports on and")
    print("  cannot appear in the %d above.  It is an EXEMPTION BY ARITHMETIC" % len(rows))
    print("  and not by rule -- re-pin past this landing and the file joins its")
    print("  own census.  Graded by hand in the meantime it is MIXED, on its")
    print("  own rule: it reads `git ls-tree` AND `git show`, because deciding")
    print("  what a producer reads means reading the producer.  So the one")
    print("  instrument built to find transcripts that are free is not free")
    print("  itself, which is the same answer section 3 gives about")
    print("  liveindex.py and is not a coincidence.")
    print()
    print("  THAT DIRECTION IS MEASURED AND NOT ASSERTED.  6 of the 6")
    print("  candidates ever adjudicated by hand were false positives:")
    print("  32 -> 2 on same-directory imports and `blame`, and 2 -> %d on" % len(only))
    print("  cross-directory imports, both survivors reaching a content-reading")
    print("  lib through a `sys.path.insert` the closure could not follow.")
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
