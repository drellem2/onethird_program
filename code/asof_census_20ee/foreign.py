#!/usr/bin/env python3
"""FOREIGN -- THE THIRD CLASS pinnable.py HAS NO RULE FOR, MEASURED RATHER THAN
REPORTED, AND THE RESIDUE IS 1 ROW AND NOT 5.

mg-e8b0's tranche 10 offered a successor two things and they turn out to be one
thing.  Priority 1 was `the residue, and it is 5 rows` -- out_worklist.txt's
section 4, the rows recorded DIFFERS that declare no revision and are not
falsified by a pin, described there as `the rows nothing on record has yet given
a reason to skip`.  Priority 2 was a SINGLE observation about a SINGLE PINNED
instrument, anchor_drift_96df, whose transcript still drifts because its address
is in ANOTHER REPOSITORY -- and the ticket declined to build a rule for it:

    It is also a THIRD CLASS pinnable.py has no rule for: R1 is an address in no
    commit, R2 a revision already declared, and this is an address IN ANOTHER
    REPOSITORY.  Reported, not built -- a rule about foreign repos is a change
    whose false-positive direction nobody has measured.

THIS FILE MEASURED IT.  The measurement is the reason the rule exists rather
than an argument for building it, which is mg-23af's shape one rule along: that
tranche declined to widen R3's `find` half for exactly this reason, the next one
measured the exposure of three candidate shapes side by side, and the numbers --
not the idea -- picked the design.  Sections 3 and 4 are those columns.

--------------------------------------------------------------------------------
1.  THE HEADLINE, AND IT IS ABOUT THE WORK-LIST AND NOT ABOUT THE RULE
--------------------------------------------------------------------------------

The class is not one pinned instrument.  It is FOUR OF THE FIVE RESIDUE ROWS,
and every one of them was triaged by hand for this file -- suite run, diff read,
scripts read at AS_OF -- before any rule was written:

    code/summary_guard_audit_407f     SRC2 = "/Users/daniel/research/one_third_width_three"
    code/superseded_descent_688c      MIRROR_REPO = same, and MG_ROOT = ~/.macguffin
    code/verdict_delivery_bf3f        MG_DEFAULT = ~/.macguffin
    code/landing_audit_sweep_64cb     STORE = ~/.macguffin/work, EVENTS = .../events.jsonl
    code/eps_spec_sweep_372e          -- nothing.  THE ONE CLEAN ROW.

So the sentence the record has been carrying forward -- that these five are what
is left -- is TRUE ABOUT THE PREFILTER AND FALSE ABOUT THE WORK.  Four of them
address corpora that NO AS_OF OF THIS REPOSITORY CAN REACH: another repository's
working tree, and the `mg` ticket store under `~/.macguffin`.  Conditions 1-3
cost forty-five minutes each and on those four they cannot succeed, because
there is no commit here whose content decides what those transcripts print.

    THE RESIDUE IS `code/eps_spec_sweep_372e` AND THE OTHER FOUR ARE A DIFFERENT
    QUESTION.  That is the deliverable.  It is not that they are unfixable --
    688c and 64cb could be pinned against the FOREIGN repository's revisions,
    which is a real remedy and a much bigger one -- it is that mg-20ee's remedy
    is the wrong instrument for them and the work-list said otherwise.

--------------------------------------------------------------------------------
2.  THE RULE, STATED SO THAT IT CAN BE ARGUED WITH
--------------------------------------------------------------------------------

    R4  A CORPUS ROOT OUTSIDE THIS REPOSITORY.  A tracked script in the subject
        BINDS A MODULE-LEVEL CONSTANT to a string literal that names an absolute
        or home-relative filesystem root.

R4 IS DECIDABLE AND IS NOT A HEURISTIC, which is the whole reason it is worth
having beside R1's `check-ignore` and R2's `cat-file -e`.  `~/.macguffin` is not
in this repository.  That is not a guess about intent, a spelling convention, or
a judgement about what the author meant; it is a fact about where the path
points, and it settles `can an AS_OF reach this` outright.  Two shapes:

      HOME      a literal beginning `~/` or exactly `~`.
      ABSOLUTE  a literal beginning `/` with at least one further separator.

AND ONE GUARD, WHICH IS WHERE THE MEASUREMENT WENT AND WHICH IS NOT COSMETIC:
the literal must be BOUND TO A MODULE-LEVEL CONSTANT.  Without it R4 fires on
28 of the 44 rows and on 3 of the 8 rows a pin has ALREADY LANDED on, including
`landscape_repair_1953` -- which is pinnable.py's OWN named example of the shape
mg-20ee's remedy was built for.  A rule waving off the estate's model pinning is
not conservative, it is wrong.  With the guard: 9 rows, and the ONE pinned row
left is `anchor_drift_96df`, which is the ticket's own instance and is the
pinned row whose transcript STILL DRIFTS.

    THE GUARD IS ARGUABLE AND HERE IS THE ARGUMENT: A CORPUS ROOT IS BOUND TO A
    NAME BECAUSE THE INSTRUMENT REFERS TO IT REPEATEDLY; AN INLINE PATH IS AN
    ARGUMENT TO ONE CALL.  Every true positive is a named constant (SRC2,
    MIRROR_REPO, MG_ROOT, STORE, EVENTS, MG_DEFAULT); the three false positives
    read by hand first are all inline -- `"/docs/"`, `"/**/mg-*.md"`, `"/bin/sh"`.

    AND THE HONEST CAVEAT: THE GUARD WAS FITTED TO THIS CORPUS.  It was chosen
    AFTER reading those three, so the 44-row figures are the sample it was
    fitted to and NOT independent evidence for it.  What is independent is the
    DIRECTION, and P47 pins it: the named true positives must survive.

`tempfile.mkdtemp` IS COUNTED AND IS NOT IN THE RULE, which the `bound` guard
does for free and which is worth a sentence anyway: a `mkdtemp()` path is in no
commit BY CONSTRUCTION, but ITS CONTENT IS WRITTEN BY THE INSTRUMENT ITSELF, so
it is not a foreign corpus.  It drifts only when the path is PRINTED --
summary_guard_audit_407f's transcript carries its arena path, and that is real
-- and that is a property of the TRANSCRIPT, which pinnable.py's R1 reads and
this file does not.  Section 3 prices it: it is half of all the firing.

    AND IT IS READ FROM THE SCRIPTS AT A DECLARED COMMIT, NOT FROM A DIFF.
    That is the difference that makes this file re-takable.  pinnable.py cannot
    go in run_all.sh because it classifies a WORKTREE DIFF and so REQUIRES a
    suite to have been run and not restored -- a state no build path should be
    in -- and out_pinnable_3b51.txt, out_pinnable_a4ef.txt and
    out_pinnable_b0ae.txt are one dated hand-run each that NO SUITE RE-TAKES, a
    blind spot this arc has now declared in the same words for four tranches.
    R4 reads `git show <AS_OF>:<path>` and TOUCHES NO FILESYSTEM AT ALL (see
    classify_root, where the first draft did and was this file's own subject).
    Every figure is a function of ONE COMMIT, so this transcript reproduces
    BYTE-IDENTICALLY and the file is on the build path -- worklist.py's,
    exemplars.py's and semantic.py's arrangement, on the class that was
    carrying the complaint.

--------------------------------------------------------------------------------
3.  WHY THIS IS NOT ALREADY R1, MEASURED RATHER THAN ASSERTED
--------------------------------------------------------------------------------

R1 asks `git check-ignore`, and the answer for every root in section 1 is NO:

      var/folders/4n/.../T/mg407f_7qyj16h6            check-ignore rc=1
      Users/daniel/research/one_third_width_three     check-ignore rc=1
      Users/daniel/.macguffin/work                    check-ignore rc=1

R1 DID fire on summary_guard_audit_407f, and this is why it must not be read as
coverage: it matched `Users/daniel/.pogo/polecats/<name>/...` against `.pogo/`
in `.git/info/exclude`.  That is this repository's ignore configuration
accidentally matching a path OUTSIDE the repository altogether -- the right
answer (`no AS_OF reaches it`) reached by the wrong mechanism, and the mechanism
is why it generalises to nothing.  Change one line of `.git/info/exclude` and
R1's only hit on this class disappears while the class does not.  On the other
three foreign rows R1 printed `none`.

    ONE ACCIDENTAL HIT AND THREE MISSES IS NOT `R1 ALREADY COVERS IT`, and the
    misses are the silent direction: `none` from R1 reads, to its reader, as
    residue -- which is exactly what put four unreachable rows on a work-list.

--------------------------------------------------------------------------------
4.  THE FALSE-POSITIVE DIRECTION, WHICH IS WHAT THE TICKET SAID NOBODY HAD
--------------------------------------------------------------------------------

Three measurements, all printed, because a rule measured only where it FIRES is
a rule nobody has checked for over-reach:

  * EXPOSURE (section 3 of the output).  Four candidate designs scored over one
    walk of the same corpus -- naive lines, ast, ast-without-arenas, and the
    rule -- with what each ADMITS beside what each FIRES on.  The design is
    chosen on the exposure and not on the delta, which is mg-23af's method.
    ONE COLUMN BOUGHT NOTHING AND IT SAYS SO: excluding docstrings removes 0
    literals here, so it is REQUIRED-INERT and is kept for the shape, not for a
    number it did not move.

  * THE PINNED ROWS (section 4).  R4 asked of the 8 rows a pin HAS landed on.
    3 under the wide shapes, 1 under the rule.

  * THE PRECISION, BY HAND (section 5).  Every literal the rule fires on, read
    at AS_OF and graded CORPUS / SELF / TOOL / FORMAT, as DATA in this source so
    a control can check the grades still cover what the rule does.  11 of 16
    literals and 7 of 9 rows are CORPUS.  THE 2 FALSE ROWS ARE NAMED.

--------------------------------------------------------------------------------
5.  WHAT THIS FILE CANNOT SAY
--------------------------------------------------------------------------------

  * R4 IS ONE-DIRECTIONAL, in worklist.py's and pinnable.py's discipline.
    FIRING PROVES that a root outside this repository is named as a constant in
    a tracked script.  It does NOT prove the drift is caused by it, so firing
    means GO AND READ WHY -- R2's declared over-count arriving on a new rule
    rather than a new claim.  NOT FIRING proves nothing whatever: an instrument
    reaching a foreign root through an environment variable, a relative `../..`,
    or a path assembled from parts is invisible here, so THE COUNT IS A LOW
    WATER MARK.

  * THE OVER-COUNT IS DECLARED AND NOT TUNED AWAY.  `/bin/sh` is outside this
    repository and that is true and useless.  Telling the CORPUS an instrument
    reads from the TOOL it runs is the difference between an instrument's
    subject and its evidence, which pinnable.py already records as not decidable
    from the token -- and a fourth guard fitted to a sixteen-literal sample
    would be the fourth thing chosen after seeing the answer.

  * IT SAYS NOTHING ABOUT WHETHER THE FOREIGN CORPUS SHOULD BE PINNED THERE.
    688c and 64cb read repositories and stores that HAVE revisions; pinning
    against them is a real remedy and a bigger change than this arc has ever
    made.  mg-688c's own table needs re-deriving for the reason tranche 10
    gives, and that is that directory's work.  DO NOT COMMIT A FOREIGN
    REPOSITORY'S HEAD INTO THIS ONE.

  * THE POPULATION IS THE WORK-LIST AND NOT THE ESTATE.  44 rows are scored
    because that is the list this arc is working; nothing here scans code/ for
    the other directories that do this, which is N34.

    python3 code/asof_census_20ee/foreign.py            # at AS_OF
    python3 code/asof_census_20ee/foreign.py <rev>      # anywhere else
    python3 code/asof_census_20ee/foreign.py --dir code/superseded_descent_688c
"""

import ast
import os
import posixpath
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# EVERY PREDICATE THAT ALREADY EXISTS IS IMPORTED AND NONE RE-SPELLED (mg-d2c2,
# mg-1344's P5).  The row list, the sweep transcript's address, the AS_OF and
# the `git show` reader are worklist.py's, so this file CANNOT disagree with
# out_worklist.txt about which 44 rows there are or which commit it read them
# at -- and section 1's `residue` is out_worklist.txt's section 4 recomputed by
# worklist.py's own code rather than copied out of its text.
import worklist                                                # noqa: E402

ROOT = worklist.ROOT
AS_OF = worklist.AS_OF

ARENA_CALLS = ("mkdtemp", "TemporaryDirectory", "mkstemp")

# EVERY LITERAL THE RULE FIRES ON, READ BY HAND AT AS_OF AND GRADED.  This is
# the precision figure, and it is written down as DATA rather than as a
# paragraph so that P48 can check it stays in step with what the rule does: a
# hand adjudication that silently stops covering the firing set is a claim
# about a corpus that has moved underneath it, which is this arc's own subject.
#
# CORPUS  the root is what the instrument READS and its content is not decided
#         by any commit of this repository.  A TRUE positive.
# TOOL    the root is an EXECUTABLE or a runtime the instrument INVOKES.
#         Outside the repository, and irrelevant to whether the transcript
#         drifts.  A FALSE positive, and it is NOT tuned away -- see below.
# FORMAT  the literal is a format template, not a path at all.  FALSE.
# SELF    an absolute path naming THIS repository's own checkout.  No AS_OF
#         reaches it either, so it is not a false positive of the CLAIM -- but
#         its remedy is RELATIVISATION and not a pin, which is a different
#         answer, so it is counted apart from CORPUS rather than with it.
ADJUDICATED = {
    "/Users/daniel/research/onethird_program": "SELF",
    "~/research/": "CORPUS",
    "~/research/one_third_width_three": "CORPUS",
    "/Users/daniel/research/one_third_width_three": "CORPUS",
    "~/.macguffin": "CORPUS",
    "~/.macguffin/work": "CORPUS",
    "~/.macguffin/events.jsonl": "CORPUS",
    "~/.pogo": "CORPUS",
    "/bin/sh": "TOOL",
    "~/go/bin/mg": "TOOL",
    "/%s/": "FORMAT",
}

# THE OVER-COUNT STOPS HERE AND IS DECLARED RATHER THAN TUNED AWAY, which is
# pinnable.py's own decision about R2 arriving on R4.  A guard excluding TOOL
# would be a rule about the difference between what an instrument READS and
# what it RUNS -- and pinnable.py has already recorded that as not decidable
# from the token, in the paragraph where R2 declines to tell a control's
# revision from a corpus pin.  A fourth fitted guard on a ten-literal sample
# would also be the fourth thing chosen after seeing the answer.  So the rule
# keeps them, this table names them, and the reader gets the precision.
OVERCOUNT = ("TOOL", "FORMAT")


def _is_abs_path_literal(s):
    """`/` plus at least one further separator, so a format string is not a path.

    THE SECOND SEPARATOR IS THE WHOLE GUARD AND IT IS NOT COSMETIC.  A single
    leading slash admits `/` itself and every `"/"` used as a JOIN CHARACTER,
    which is most of them; requiring a second one is a fact about what an
    absolute path looks like rather than a judgement about the string, and
    section 4 prints what it costs.
    """
    return s.startswith("/") and s.count("/") >= 2 and " " not in s.strip()


def _is_home_literal(s):
    return s == "~" or s.startswith("~/")


def classify_root(s):
    """AN ABSOLUTE OR HOME-RELATIVE ROOT IS OUTSIDE, FULL STOP -- AND THE FIRST
    DRAFT OF THIS FUNCTION WAS THE DEFECT THIS FILE REPORTS.

    It called `os.path.realpath` on each literal and compared the result against
    this worktree and against the repository's common git dir, taken from `git
    rev-parse --git-common-dir`.  Both halves are reads of the machine:

      * realpath TOUCHES THE FILESYSTEM.  A literal naming a symlinked
        directory resolves differently depending on what exists on disk, so the
        census would have been a function of a tree outside this repository --
        WHICH IS THE CLASS THIS FILE EXISTS TO FIND, in the instrument built to
        find it.  Enumerated because a remedy is an artifact of the same kind
        as the defect it remedies, and found by running it rather than by
        reasoning: exactly ONE literal in the 44 rows came back SELF,
        `/Users/daniel/research/onethird_program` in census_audit_4d3b, and it
        is SELF only because this checkout happens to live there.

      * SO out_foreign.txt WOULD HAVE BEEN A FUNCTION OF WHERE THE REPOSITORY
        IS ON DISK, while its own docstring claimed every figure was a function
        of ONE COMMIT.  Byte-identical for every polecat on this machine, and
        wrong for the next reader who clones it elsewhere -- a transcript that
        reproduces for exactly one operator, which is tranche 1's third class
        and is named in pinnable.py's own residue paragraph.

    THE REPAIR IS NOT A BETTER COMPARISON, IT IS DELETING THE QUESTION.  An
    absolute path naming this repository's own checkout is NOT reachable by an
    AS_OF either -- the transcript still prints an operator-specific absolute
    path, and no pin removes it.  Excluding it was never right; it just looked
    tidy.  So the exclusion is gone, the grade `SELF` in ADJUDICATED carries
    that literal with its own remedy (relativise it, do not pin it), and this
    function reads NO filesystem at all.  P46 asserts that.
    """
    return "OUTSIDE"


def _constant_bound(tree):
    """Every string node reachable from a MODULE-LEVEL assignment's value.

    THIS GUARD WAS CHOSEN ON A MEASUREMENT AND THE MEASUREMENT IS SECTION 3.
    Without it R4 fires on 28 of 44 rows and on 3 of the 8 rows a pin has
    already LANDED on -- which would be a rule telling operators not to do work
    that demonstrably succeeded, the one false-positive direction that matters
    here.  Reading the three hand-adjudicated false positives is what produced
    it, and all three are INLINE:

        code/landscape_repair_1953/selftest.py:213     "/docs/"
        code/landing_audit_sweep_64cb/lib64cb.py:82    "/**/mg-*.md"
        code/runner_exit_audit_dee4/a5_floor.py:225    "/bin/sh"

    while every true positive is BOUND TO A NAME -- SRC2, MIRROR_REPO, MG_ROOT,
    STORE, EVENTS, MG_DEFAULT.  The separator is a fact about the syntax tree
    and not a judgement about the word, which is mg-44da's guard (`a flag's dash
    sits at a word boundary`) and mg-23af's (`a command name is a whole token`)
    on a third subject.  IT IS ALSO ARGUABLE, AND HERE IS THE ARGUMENT: A CORPUS
    ROOT IS BOUND TO A NAME BECAUSE THE INSTRUMENT REFERS TO IT REPEATEDLY; AN
    INLINE PATH IS AN ARGUMENT TO ONE CALL.  A join fragment and an interpreter
    are arguments to one call.  A repository you audit is not.

    AND THE HONEST CAVEAT, WHICH SECTION 3 REPEATS WHERE IT IS READ: this guard
    was chosen AFTER seeing these rows.  The 44-row figures below are therefore
    NOT independent evidence for it -- they are the corpus it was fitted to.
    What is independent is the DIRECTION: every literal it removes was read by
    hand first, and P47 requires it to keep the six named true positives.
    """
    out = set()
    for node in getattr(tree, "body", []):
        value = None
        if isinstance(node, ast.Assign):
            value = node.value
        elif isinstance(node, ast.AnnAssign):
            value = node.value
        if value is None:
            continue
        for sub in ast.walk(value):
            if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                out.add(id(sub))
    return out


def _docstring_nodes(tree):
    """Every string node that is a docstring, so the rule can exclude them.

    Comments never reach the ast at all, which is half of why this is parsed
    rather than grepped; docstrings DO, and a docstring naming `~/.macguffin`
    while the code never touches it is precisely the false positive section 4
    exists to price.
    """
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef,
                             ast.AsyncFunctionDef)):
            body = getattr(node, "body", None)
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                out.add(id(body[0].value))
    return out


def scan_source(src, path):
    """Every candidate in one script, TAGGED WITH WHICH DESIGNS ADMIT IT.

    ONE WALK PRODUCES ALL FOUR COLUMNS, so section 3's comparison cannot be a
    statement about four slightly different walkers.  Each hit carries the two
    guards it passes -- `docstring` and `bound` -- and the columns are then
    filters over one list rather than four scans.

    A file that does not parse is REPORTED rather than skipped silently: a scan
    that read nothing because it could not read is this file's own subject one
    turn along, and the census would look CLEANER for it.
    """
    try:
        tree = ast.parse(src, filename=path)
    except SyntaxError:
        return [], False
    docs = _docstring_nodes(tree)
    bound = _constant_bound(tree)
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            s = node.value
            if _is_home_literal(s):
                kind = "HOME"
            elif _is_abs_path_literal(s):
                kind = "ABSOLUTE"
            else:
                continue
            hits.append({"kind": kind, "val": s, "line": node.lineno,
                         "where": classify_root(s),
                         "docstring": id(node) in docs,
                         "bound": id(node) in bound})
        elif isinstance(node, ast.Call):
            fn = node.func
            name = getattr(fn, "attr", None) or getattr(fn, "id", None)
            if name in ARENA_CALLS:
                # AN ARENA IS NEVER `bound`: mkdtemp() is a call, not a literal
                # assigned to a module constant, so the rule's guard excludes
                # the whole shape.  That is not an accident of the guard and it
                # is not tidied away -- section 3 counts it and says why.
                hits.append({"kind": "ARENA", "val": name + "()",
                             "line": node.lineno, "where": "OUTSIDE",
                             "docstring": False, "bound": False})
    return hits, True


def is_rule(h):
    """R4 AS DECIDED: a NAMED root, outside this repository, not a docstring.

    ARENA is excluded BY THE `bound` GUARD rather than by a special case, and
    that is worth one sentence because the two would print the same number
    today: a `mkdtemp()` path is in no commit BY CONSTRUCTION, but its CONTENT
    IS WRITTEN BY THE INSTRUMENT ITSELF, so it is not a foreign corpus at all.
    It drifts only when the path is PRINTED -- summary_guard_audit_407f's
    transcript carries its arena path and that is real -- and that is a
    property of the TRANSCRIPT, which pinnable.py's R1 reads and this file
    does not.
    """
    return (h["where"] == "OUTSIDE" and not h["docstring"] and h["bound"]
            and h["kind"] in ("HOME", "ABSOLUTE"))


def naive_lines(src):
    """The exposure column a line regex would admit -- comments and all."""
    n = 0
    for line in src.splitlines():
        if "~/" in line or "mkdtemp" in line or "TemporaryDirectory" in line:
            n += 1
        elif "/" in line and any(tok.startswith("/") and tok.count("/") >= 2
                                 for tok in line.replace('"', " ")
                                              .replace("'", " ").split()):
            n += 1
    return n


def scripts_in(directory, rev):
    """Tracked .py/.sh under the subject AT `rev`.  `git ls-tree`, so it is a
    function of the commit and never of the worktree."""
    got = subprocess.run(["git", "-C", ROOT, "ls-tree", "-r", "--name-only",
                          rev, "--", directory], capture_output=True)
    if got.returncode != 0:
        return []
    return sorted(p for p in got.stdout.decode("utf-8", "replace").split("\n")
                  if p.endswith((".py", ".sh")))


def score_dir(directory, rev):
    """R4 for one subject, and every exposure column, from ONE walk per script."""
    out = {"dir": directory, "hits": [], "all": [], "naive": 0,
           "scripts": 0, "unparsed": []}
    for path in scripts_in(directory, rev):
        try:
            src = worklist.read_rev(rev, path)
        except SystemExit:
            continue
        out["scripts"] += 1
        out["naive"] += naive_lines(src)
        if not path.endswith(".py"):
            continue
        hits, ok = scan_source(src, path)
        if not ok:
            out["unparsed"].append(path)
        for h in hits:
            h["path"] = path
            out["all"].append(h)
            if is_rule(h):
                out["hits"].append(h)
    return out


def column(scored, pred):
    """(literals admitted, rows fired) for one candidate design."""
    lits = sum(sum(1 for h in s["all"] if pred(h)) for s in scored)
    rows = sum(1 for s in scored if any(pred(h) for h in s["all"]))
    return lits, rows


def banner(title):
    print()
    print("-" * 78)
    print(title)
    print("-" * 78)


def main(argv):
    rev = AS_OF
    only = None
    args = list(argv)
    if "--dir" in args:
        i = args.index("--dir")
        only = args[i + 1]
        del args[i:i + 2]
    if args:
        rev = args[0]

    print("=" * 78)
    print("mg-3ebf -- A CORPUS ROOT OUTSIDE THIS REPOSITORY.  Read at AS_OF = %s"
          % rev)
    print("=" * 78)
    print()
    print("  R1 is an address in no commit, R2 a revision already declared, R3")
    print("  an unordered walk.  THIS IS AN ADDRESS IN NO COMMIT OF THIS")
    print("  REPOSITORY AT ALL -- another repository's tree, or the `mg` store")
    print("  under ~/.macguffin.  mg-e8b0 reported the class on ONE PINNED")
    print("  instrument and declined to build a rule because the false-positive")
    print("  direction was unmeasured; sections 4 and 5 are that measurement.")
    print("  METHOD AND BLIND SPOTS are in this file's docstring and are not")
    print("  repeated.  THE SENTENCE THAT MATTERS: R4 FIRING IS `GO AND READ")
    print("  WHY', NOT `DO NOT PIN'.  R4 NOT FIRING PROVES NOTHING.")

    if only:
        got = score_dir(only, rev)
        banner("ONE SUBJECT: %s" % only)
        if not got["hits"]:
            print("      none.  Which is NOT evidence the corpus is in this")
            print("      repository: an environment variable, a relative walk")
            print("      or an assembled path is invisible to R4.")
        for h in got["hits"]:
            print("      %-8s %s:%d" % (h["kind"], h["path"], h["line"]))
            print("               %s" % h["val"])
        excluded = [h for h in got["all"] if not is_rule(h)]
        if excluded:
            print()
            print("      admitted by a WIDER design and excluded by the rule: %d"
                  % len(excluded))
            for h in excluded:
                why = ("docstring" if h["docstring"]
                       else "not bound to a module constant"
                       if not h["bound"] else "inside this repository")
                print("        %-8s %s:%d  %-28s (%s)"
                      % (h["kind"], h["path"], h["line"], h["val"][:28], why))
        print()
        print("CONDITION 0 (foreign): %s -- %d root(s) outside this repository, at %s"
              % (only, len(got["hits"]), rev))
        return 0 if not got["hits"] else 0

    # ONE scan().  It is 44 rows x (ls-tree + show per script) and calling it
    # twice would double this file's cost for a figure that cannot have changed
    # between the two calls.
    scan = worklist.scan()
    rows = scan["rows"]
    scored = [score_dir(r["dir"], rev) for r in rows]
    by_dir = {s["dir"]: s for s in scored}
    fires = [s for s in scored if s["hits"]]

    # THE RESIDUE, COMPUTED BY worklist.py's OWN PREDICATE.  Copying the five
    # names out of out_worklist.txt's text would make this file's headline a
    # statement about a transcript rather than about the repository -- which is
    # the exact defect the whole arc is about -- and re-spelling the predicate
    # would let the two files disagree about which rows the residue IS.
    residue = [r["dir"] for r in worklist.residue_rows(rows)]
    pinned_dirs = sorted(set(r["dir"] for r in scan["falsified"]))

    banner("1  THE RESIDUE, RE-TRIAGED.  R4 OVER out_worklist.txt SECTION 4")
    print()
    print("  These are the rows recorded DIFFERS that declare no revision and")
    print("  are not falsified by a pin -- `the rows nothing on record has yet")
    print("  given a reason to skip'.  R4 IS A REASON, AND IT LANDS ON MOST OF")
    print("  THEM.  Every one below was ALSO triaged BY HAND for this file:")
    print("  suite run, worktree diff read, scripts read at AS_OF.")
    print()
    for d in residue:
        got = by_dir.get(d) or score_dir(d, rev)
        if got["hits"]:
            print("  %s" % d)
            for h in got["hits"]:
                print("      %-8s %s:%d" % (h["kind"], h["path"], h["line"]))
                print("               %s" % h["val"])
            print("      -> OUTSIDE THIS REPOSITORY.  No AS_OF here reaches it.")
        else:
            print("  %s" % d)
            print("      -> R4 does not fire.  A pinning candidate, and this is")
            print("         a PREFILTER passing rather than a verdict.")
        print()
    print("      residue rows                                     %d" % len(residue))
    print("        R4 fires -- a root outside this repository      %d"
          % sum(1 for d in residue if (by_dir.get(d) or {}).get("hits")))
    print("        R4 silent -- conditions 1-3 are worth starting  %d"
          % sum(1 for d in residue if not (by_dir.get(d) or {}).get("hits")))

    banner("2  THE SAME RULE OVER ALL %d ROWS OF THE WORK-LIST" % len(rows))
    print()
    for r in rows:
        got = by_dir[r["dir"]]
        if not got["hits"]:
            continue
        kinds = sorted(set(h["kind"] for h in got["hits"]))
        roots = sorted(set(h["val"] for h in got["hits"]))
        print("  %-46s %-10s %s" % (r["dir"], r["verdict"], ",".join(kinds)))
        for root in roots:
            print("      %s" % root)
    print()
    print("      rows scored                                      %d" % len(rows))
    print("        R4 fires                                       %d" % len(fires))
    print("        of the rows recorded DIFFERS                   %d"
          % sum(1 for r in rows if by_dir[r["dir"]]["hits"]
                and r["verdict"] == "DIFFERS"))
    print("        of the rows recorded REPRODUCES                %d"
          % sum(1 for r in rows if by_dir[r["dir"]]["hits"]
                and r["verdict"] == "REPRODUCES"))
    unparsed = sorted(p for s in scored for p in s["unparsed"])
    print("      scripts that did not parse (reported, not skipped) %d"
          % len(unparsed))
    for p in unparsed:
        print("          %s" % p)

    banner("3  THE FALSE-POSITIVE DIRECTION 1 -- EXPOSURE, FOUR DESIGNS")
    print()
    print("  mg-23af's method: the design is chosen on what each SHAPE ADMITS,")
    print("  not on the delta between their verdicts, because three designs")
    print("  agreeing on today's corpus cannot be told apart by today's counts.")
    print()
    out_ = lambda h: h["where"] == "OUTSIDE"
    designs = [
        ("ast, ANY outside literal + arena",
         out_),
        ("  + docstrings excluded",
         lambda h: out_(h) and not h["docstring"]),
        ("  + arena excluded",
         lambda h: out_(h) and not h["docstring"] and h["kind"] != "ARENA"),
        ("  + bound to a module constant (RULE)",
         is_rule),
    ]
    print("      shape                                  literals   rows   pinned")
    print("      naive LINE match (comments included)   %8d   %6s   %6s"
          % (sum(s["naive"] for s in scored), "-", "-"))
    for label, pred in designs:
        lits, nrows = column(scored, pred)
        npin = sum(1 for d in pinned_dirs
                   if any(pred(h) for h in (by_dir.get(d) or {}).get("all", [])))
        print("      %-37s %8d   %6d   %6d" % (label, lits, nrows, npin))
    print()
    print("  THE `pinned` COLUMN IS THE ONE THAT DECIDED THE DESIGN, and it is")
    print("  the direction that would matter if it went wrong: those are rows a")
    print("  pin HAS landed on, so a rule firing there is telling operators not")
    print("  to do work that demonstrably succeeded.  The wide shapes fire on")
    print("  three of the eight, INCLUDING landscape_repair_1953 -- which is")
    print("  pinnable.py's OWN named example of the shape mg-20ee's remedy was")
    print("  built for.  A rule that waves off the estate's model pinning is")
    print("  not a conservative rule, it is a wrong one.")
    print()
    print("  WHAT EACH NARROWING BOUGHT, AND THE DOCSTRING GUARD BOUGHT NOTHING:")
    print("  the docstring column is IDENTICAL to the one above it on this")
    print("  corpus -- 0 literals removed -- so it is REQUIRED-INERT here and")
    print("  is kept for the shape and not for the delta.  Saying so is the")
    print("  point: a guard reported as load-bearing because it was reasonable,")
    print("  rather than because it moved a number, is a figure nothing stands")
    print("  behind, which is what permuted.py found under its own `18 of 129`.")
    print()
    print("  AND THE GUARD THAT DID THE WORK WAS FITTED TO THIS CORPUS.  The")
    print("  `bound` rule was chosen AFTER reading three false positives by")
    print("  hand (`/docs/`, `/**/mg-*.md`, `/bin/sh`), so the row counts above")
    print("  are NOT independent evidence for it -- they are the sample it was")
    print("  fitted to.  What is independent is the DIRECTION, which P47 pins:")
    print("  every literal the guard removes was adjudicated first, and the six")
    print("  named true positives must survive it.")

    banner("4  THE FALSE-POSITIVE DIRECTION 2 -- THE ROWS A PIN LANDED ON")
    print()
    print("  This is the direction that would matter if it went wrong: a rule")
    print("  firing freely on rows that were SUCCESSFULLY PINNED would be")
    print("  telling operators not to do work that demonstrably succeeded.")
    print()
    for d in pinned_dirs:
        got = by_dir.get(d) or score_dir(d, rev)
        wide = [h for h in got["all"] if h["where"] == "OUTSIDE"]
        if got["hits"]:
            mark = "R4 FIRES   " + ", ".join(sorted(set(h["val"] for h in got["hits"])))
        elif wide:
            mark = ("silent -- %d literal(s) a wider design would have fired on: %s"
                    % (len(wide),
                       ", ".join(sorted(set(h["val"][:24] for h in wide)))))
        else:
            mark = "silent"
        print("      %s" % d)
        print("          %s" % mark)
    print()
    print("      rows a pin has landed on                         %d" % len(pinned_dirs))
    print("        R4 fires on                                    %d"
          % sum(1 for d in pinned_dirs if (by_dir.get(d) or {}).get("hits")))
    print()
    print("  THE ONE THAT SURVIVES IS THE TICKET'S OWN INSTANCE, and it is the")
    print("  sharpest thing here: anchor_drift_96df is PINNED, R4 fires on it,")
    print("  and it is the pinned row WHOSE TRANSCRIPT STILL DRIFTS -- which is")
    print("  what mg-e8b0's tranche 10 reported by hand and declined to build.")
    print("  n = 1, SAID PLAINLY: it is the instance the rule was aimed at, so")
    print("  it demonstrates that the rule fires where it was aimed and is NOT")
    print("  independent evidence about the rule.")

    banner("5  THE PRECISION, ADJUDICATED BY HAND AT BOTH GRAINS")
    print()
    print("  Sections 3 and 4 measure where the rule FIRES and where it must")
    print("  NOT.  Neither says whether a firing is RIGHT, and that is a")
    print("  judgement no rule here can make: every literal below was read at")
    print("  AS_OF and graded, and the grades are DATA in this file's source")
    print("  so P48 can check they still cover what the rule does.")
    print()
    lits = [h for s in scored for h in s["hits"]]
    seen, uncovered = {}, []
    for h in lits:
        grade = ADJUDICATED.get(h["val"])
        if grade is None:
            uncovered.append(h)
            grade = "UNADJUDICATED"
        seen.setdefault((h["val"], grade), 0)
        seen[(h["val"], grade)] += 1
    for (val, grade), n in sorted(seen.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        print("      %-9s %-46s x%d" % (grade, val, n))
    true_l = sum(n for (v, g), n in seen.items() if g == "CORPUS")
    self_l = sum(n for (v, g), n in seen.items() if g == "SELF")
    false_l = sum(n for (v, g), n in seen.items() if g in OVERCOUNT)
    true_r = sum(1 for s in scored if any(
        ADJUDICATED.get(h["val"]) == "CORPUS" for h in s["hits"]))
    false_r = sum(1 for s in scored if s["hits"] and all(
        ADJUDICATED.get(h["val"]) in OVERCOUNT for h in s["hits"]))
    fire_r = len([s for s in scored if s["hits"]])
    print()
    print("      literals the rule fires on                       %d" % len(lits))
    print("        CORPUS -- a true foreign corpus root           %d" % true_l)
    print("        SELF -- this repository, absolutely spelled    %d" % self_l)
    print("        TOOL / FORMAT -- the declared over-count       %d" % false_l)
    print("        UNADJUDICATED                                  %d" % len(uncovered))
    for h in uncovered:
        print("            %s:%d  %s" % (h["path"], h["line"], h["val"]))
    print()
    print("      rows the rule fires on                           %d" % fire_r)
    print("        with at least one CORPUS root                  %d" % true_r)
    print("        with at least one CORPUS or SELF root          %d"
          % (fire_r - false_r))
    print("        on the over-count ALONE -- a FALSE row         %d" % false_r)
    print()
    print("  THE TWO FALSE ROWS ARE NAMED AND ARE BOTH THE SAME SHAPE:")
    for s in scored:
        if s["hits"] and all(ADJUDICATED.get(h["val"]) in OVERCOUNT
                             for h in s["hits"]):
            print("      %-46s %s" % (s["dir"],
                                      ", ".join(sorted(set(h["val"]
                                                           for h in s["hits"])))))
    print()
    print("  `/bin/sh` IS OUTSIDE THIS REPOSITORY AND THAT IS TRUE AND USELESS.")
    print("  The rule proves what it claims -- a root outside this repository")
    print("  is named as a module constant -- and `is that root the CORPUS or")
    print("  the INTERPRETER' is the difference between what an instrument")
    print("  READS and what it RUNS.  pinnable.py has already recorded that as")
    print("  not decidable from the token, where R2 declines to tell a")
    print("  control's revision from a corpus pin, and a fourth guard fitted to")
    print("  a ten-literal sample would be the fourth thing chosen after seeing")
    print("  the answer.  SO IT IS DECLARED AND NOT TUNED AWAY, and the")
    print("  ADJUDICATED table above is what a reader gets instead.")

    # THIS FILE ON ITS OWN RULE, AND IT IS ON STDERR FOR THE REASON THE RULE IS
    # ABOUT.  Grading this directory means reading it AS IT STANDS -- foreign.py
    # does not exist at AS_OF, so there is no commit to read it at -- and a
    # figure taken off the worktree is branch-dependent.  Putting it on stdout
    # would make out_foreign.txt a function of the tree rather than of one
    # commit, which is exactly the defect this file reports, committed by the
    # file reporting it.  README D4's rule and liveindex.py's arrangement: the
    # live half is on STDERR and gates nothing.
    self_hits = {}
    for name in ("foreign.py", "selftest_20ee.py", "worklist.py"):
        try:
            with open(os.path.join(HERE, name), encoding="utf-8") as fh:
                hs, _ok = scan_source(fh.read(), name)
        except OSError:
            continue
        self_hits[name] = [h for h in hs if is_rule(h)]

    banner("6  THIS FILE ON ITS OWN RULE -- THE READING IS ON STDERR")
    print()
    print("  A remedy is an artifact of the same kind as the defect, so it is")
    print("  subject to it, and R4 FIRES ON foreign.py.  Every hit is the")
    print("  ADJUDICATED table -- a GRADE SHEET, not a corpus read -- so THE")
    print("  DETECTOR CONTAINS THE TOKENS IT DETECTS.  That is the README's")
    print("  section 4 for the FIFTH time in this arc, and section 4's remedy")
    print("  DOES NOT APPLY: it says assemble the needle at runtime, and A TABLE")
    print("  OF ADJUDICATED LITERALS CANNOT AVOID CONTAINING THOSE LITERALS.")
    print("  pinnable.py's R3 makes the same argument about its own regex.")
    print()
    print("  THE COUNT IS NOT PRINTED HERE, AND THAT IS THE RULE ARRIVING IN THE")
    print("  DIRECTORY WHOSE SUBJECT IT IS.  foreign.py does not exist at AS_OF,")
    print("  so there is no commit to read it at and the grading must read the")
    print("  WORKTREE -- a branch-dependent figure, which on stdout would make")
    print("  this transcript a function of the tree instead of of one commit.")
    print("  It is on STDERR (README D4, liveindex.py's arrangement) and P50")
    print("  asserts it, so it is a run rather than a paragraph.")
    print()
    print("  AND THIS FILE IS OUTSIDE ITS OWN POPULATION BY ARITHMETIC RATHER")
    print("  THAN BY RULE, which is pathlist.py's declared shape: the AS_OF is")
    print("  older than foreign.py, so it is not tracked at the commit it")
    print("  reports on and cannot appear in the 44 -- an exemption nobody wrote")
    print("  and nobody should rely on.  Were this directory ever nominated onto")
    print("  the work-list, R4 would fire on it, and the reason would be its own")
    print("  grade sheet.")

    sys.stderr.write("\nmg-3ebf foreign: THIS DIRECTORY ON ITS OWN RULE, read "
                     "from the WORKTREE and therefore branch-dependent --\n")
    for name in sorted(self_hits):
        sys.stderr.write("  %-20s R4 fires on %d literal(s)\n"
                         % (name, len(self_hits[name])))
        for h in self_hits[name]:
            sys.stderr.write("      %-8s %s:%-4d %s\n"
                             % (h["kind"], name, h["line"], h["val"]))
    sys.stderr.write("  Every foreign.py hit is the ADJUDICATED grade sheet; a "
                     "hit anywhere else would be a real corpus read.\n")

    banner("7  WHAT THIS SECTION CANNOT SAY, RESTATED WHERE IT IS READ")
    print()
    print("  * R4 FIRING IS NOT `DO NOT PIN'.  It proves a root outside this")
    print("    repository is NAMED in a tracked script; it does not prove the")
    print("    drift is caused by it.  Read the line and decide.")
    print("  * R4 NOT FIRING PROVES NOTHING.  An environment variable, a")
    print("    relative `../..`, or a path assembled from parts reaches a")
    print("    foreign corpus with no literal for R4 to see.  The count is")
    print("    therefore A LOW WATER MARK, in this arc's usual direction.")
    print("  * R1 IS NOT THIS RULE AND ITS ONE HIT ON THIS CLASS IS AN")
    print("    ACCIDENT.  `git check-ignore` answers NO for every root in")
    print("    section 1; it fired on summary_guard_audit_407f only because")
    print("    `.git/info/exclude` carries `.pogo/`, which matched a path")
    print("    OUTSIDE the repository as though it were inside it.  Right")
    print("    answer, wrong mechanism, and it generalises to nothing.")
    print("  * THE REMEDY FOR A FIRING ROW IS NOT IN THIS REPOSITORY.  688c")
    print("    and 64cb read a repository and a store that HAVE revisions;")
    print("    pinning against those is a real and much larger change, and")
    print("    mg-688c's own table is tranche 10's open alarm.  DO NOT COMMIT")
    print("    A FOREIGN REPOSITORY'S HEAD INTO THIS ONE.")

    print()
    print("CONDITION 0 (foreign): %d of %d rows name a root outside this "
          "repository (%d adjudicated CORPUS, %d FALSE), %d of %d residue "
          "rows, at %s"
          % (len(fires), len(rows), true_r, false_r,
             sum(1 for d in residue if (by_dir.get(d) or {}).get("hits")),
             len(residue), rev))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
