"""CONSUMERS -- mg-20ee's THIRD CONDITION, AS AN INSTRUMENT.

mg-20ee's method for pinning a transcript has two conditions, in this order:

    1.  git merge-base --is-ancestor <declared-commit> origin/main   -- YES
    2.  the transcript reproduces byte-identically AT that commit

mg-6e4f found, by breaking three instruments, that there is a third, and the
mayor ruled it adopted:

    3.  BEFORE PINNING, FIND EVERY INSTRUMENT THAT *RUNS* THIS ONE AND
        RE-MEASURE IT.  A consumer asking a question ABOUT THE WORKTREE must
        be given the live override explicitly.

The reason is that a script under `code/**` is not only a transcript producer.
It can also be a SHARED CHECKER: `code/species_remainder_f8fa/w3_scope.py` is
executed by nine other instruments.  Pinning its default reading -- which is
the whole repair -- silently changes what every one of them measures.  Three
were changed and all three announced it, which is the only reason the class was
found at all:

    species_extent_audit_6cb9   plants in the WORKTREE and runs the checker in
                                place.  Q6/Q7 `1 1 as predicted` ->
                                `1 0 *** MISSED ***`, A1 TOTAL BAD 0 -> 2.
    species_extent_d633/e1      its method IS an open() tracer, and a checker
                                reading git opens nothing.  `18 file(s)` ->
                                `0`, E1 TOTAL BAD 0 -> 3.
    species_audit_7dd3/d5       `shutil.copytree`s the repo into a tempdir and
                                runs the checker THERE.  That copy has no
                                `.git`, so the pinned read is impossible: the
                                control M0d `no mutation` became
                                `exit 1, predicted 0 *** PREDICTION MISSED ***`.

THIS FILE IS THE CENSUS THAT CONDITION 3 OTHERWISE LEAVES TO GOOD INTENTIONS.
"Find every instrument that runs this one" is unfalsifiable as an instruction.
A method with a KNOWN blind spot can be improved; a goal cannot.

    THE METHOD, STATED SO THAT IT CAN BE ARGUED WITH:

      * the SUBJECT is a directory under code/.  Its SCRIPTS are the tracked
        *.py and *.sh in it.
      * ONLY *.py AND *.sh ARE SEARCHED.  A README that names a script is not
        a consumer of it; prose cannot execute anything.  Documentation
        mentions are COUNTED and reported as a number, not listed, so the
        exclusion is a stated figure rather than a silence.
      * A BASENAME IS NOT A NAME.  `run_all.sh` is the basename of about 220
        tracked files, and the first version of this census duly reported
        `build.sh` and every README in the repository as consumers of
        `code/species_remainder_f8fa/run_all.sh`.  So: a script whose basename
        is UNIQUE among tracked files is matched by basename; one whose
        basename is SHARED is matched by its FULL REPOSITORY PATH only.  Both
        counts are printed.
      * a mention is an EXECUTION when the mentioning line, or one of the two
        lines after it, also carries an exec-shaped token: subprocess,
        run_checker, run_script, sys.executable, python3, or an `= run(`.
      * an execution is EXPLICIT-PATH when the same line passes an argument
        after the script -- those callers point the checker at a tree they
        chose and are NOT disturbed by a pin.  Otherwise it is NO-ARG, and a
        no-arg caller gets the pinned default and must be re-measured.

    AND THE BLIND SPOT, WHICH IS THE POINT OF WRITING THE METHOD DOWN:

      * A CONSTRUCTED PATH.  `os.path.join(d, "w3_" + name + ".py")` contains
        no basename and this census cannot see it.
      * A WRAPPER.  A consumer that runs `run_all.sh`, which runs the script,
        mentions only the runner.  §C prints those runners for exactly this
        reason -- a directory whose runner is executed elsewhere is a
        SECOND-ORDER consumer -- but the chain is followed ONE hop, not
        transitively.  A SHARED basename reached by `cd <dir> && sh
        run_all.sh`, where the path never appears on one line, is in this
        blind spot by construction of the rule above.
      * IMPORT rather than exec.  `from w3_scope import ...` is reported as a
        mention with no exec token and lands in §B's residue, NOT silently
        dropped, but it is not classified further.
      * ANYTHING OUTSIDE THIS REPOSITORY.  git grep cannot see it, which is
        the same under-count `census.py` declares for addresses.

    THE BLIND-SPOT LIST ABOVE AND SECTION D'S LAST SENTENCE ARE LOAD-BEARING
    AND ARE NOT TO BE TIDIED AWAY.  They read as negative and a later editor
    improving this file will be tempted to cut them.  What they carry is the
    only thing standing between this census and being read as complete: a
    census with no stated blind spot is indistinguishable, to its reader, from
    one that has none.  mg-6e4f found six affected consumers by RUNNING nine,
    not by their announcing themselves -- and the two it found first announced
    themselves only because it happened to be running them for another reason.
    SO THE BACKSTOP IS THE LOAD-BEARING HALF AND THIS CENSUS IS A PREFILTER,
    not the other way round.  Cutting the limit inverts that silently.  If you
    are removing either, you are arguing that the method has no blind spot;
    make that argument in the commit message.

    SO THE CENSUS IS NOT THE BACKSTOP AND MUST NOT BE TREATED AS ONE.  §D
    prints the RE-MEASUREMENT COMMAND for every no-arg consumer it found:
    run the consumer BEFORE and AFTER the pin and diff.  A consumer this
    census MISSES shows up in that diff anyway if it lives in a suite you run;
    a consumer it misses AND you never run is invisible, and saying so here is
    the only honest thing to do about it.

    sh code/asof_census_20ee/run_all.sh          # runs this with the default
    python3 code/asof_census_20ee/consumers.py code/species_remainder_f8fa
"""

import os
import re
import subprocess
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", ".."))
SELF = os.path.join("code", "asof_census_20ee")

EXEC_TOKENS = ("subprocess", "run_checker", "run_script", "sys.executable",
               "python3", "= run(", ", run(")
LOOKAHEAD = 2
CODE_GLOBS = ("*.py", "*.sh")
PROSE_GLOBS = ("*.md", "*.txt")


def git(*args):
    got = subprocess.run(["git", "-C", ROOT, *args], capture_output=True)
    if got.returncode != 0:
        raise SystemExit("consumers: git %s failed: %s"
                         % (" ".join(args),
                            got.stderr.decode("utf-8", "replace").strip()))
    return got.stdout.decode("utf-8", "surrogateescape")


def git_grep_l(needle, globs):
    """`git grep -l -F` over HEAD, where FINDING NOTHING IS AN ANSWER.

    mg-4020, measured: `git grep` exits 1 for NO MATCH and 2 or more for a
    real error, and git() above treats every non-zero the same way.  So a
    subject script that nothing outside its own directory names -- which is
    the ORDINARY case for a library or a numbered step -- killed this census
    outright, after it had printed a correct-looking header.

    IT DIED ON 23 OF THE 27 INSTRUMENTS THE PINNING WORK-LIST STILL HOLDS.
    It ran on 4, one of which is the single subject it was built against, so
    the whole of its evidence that it worked came from the one directory
    where every script happened to be named somewhere else.  That is not a
    rare case reached at last; it is the common case, never reached.

    THE REPAIR THAT MADE THIS CENSUS CORRECT IS WHAT MADE IT FATAL, which is
    mg-6e4f's `a repair can introduce the defect it repairs` arriving by a
    second route.  `A BASENAME IS NOT A NAME` searches a SHARED basename by
    its full repository path, and `code/audit_2c77/run_all.sh` appears in no
    other tracked file -- so the very rule that stopped this census reporting
    every README in the estate as a consumer is the rule that guaranteed it
    would find nothing, and finding nothing was fatal.  Four of the crashes
    above are that rule and nothing else.

    THE TOLERANCE IS DELIBERATELY NARROW.  rc 1 is `no match` and returns
    empty; rc 2 and above is a bad glob, a bad revision, a broken index, and
    stays fatal through git().  Widening this to `any non-zero is empty`
    would turn a mistyped revision into a silent census of nothing -- and a
    census that reports `none` because it never looked is the exact failure
    section A's own wording is written against.
    """
    got = subprocess.run(["git", "-C", ROOT, "grep", "-l", "-F", needle,
                          "HEAD", "--", *globs], capture_output=True)
    if got.returncode == 1:
        return []
    if got.returncode != 0:
        raise SystemExit("consumers: git grep -F %s failed (rc=%d): %s"
                         % (needle, got.returncode,
                            got.stderr.decode("utf-8", "replace").strip()))
    out = []
    for path in got.stdout.decode("utf-8", "surrogateescape").splitlines():
        out.append(path.split(":", 1)[1] if path.startswith("HEAD:") else path)
    return out


def scripts_of(subject):
    """The tracked *.py / *.sh in the subject directory."""
    out = []
    for path in git("ls-files", "--", subject).splitlines():
        if path.endswith(".py") or path.endswith(".sh"):
            out.append(path)
    return sorted(out)


def instrument_of(path):
    parts = path.split("/")
    return "/".join(parts[:2]) if len(parts) > 2 else os.path.dirname(path)


def classify_text(text, needle):
    """(kind, line-number, line) for every occurrence of `needle` in `text`.

    Nested rather than disjoint, which is mg-502f's rule for the same shape:
    a file that both executes no-arg and executes with a path is reported as
    BOTH, because reporting only the first match is how a binding gets erased.

    Split out from the git read so selftest_20ee.py can exercise the three
    classifications on planted lines.  A classifier whose rules are only ever
    run against the real corpus has no evidence it can tell them apart -- which
    is the objection this directory's own selftest exists to answer.
    """
    lines = text.splitlines()
    hits = []
    for i, ln in enumerate(lines):
        if needle not in ln:
            continue
        window = "\n".join(lines[i:i + 1 + LOOKAHEAD])
        if not any(tok in window for tok in EXEC_TOKENS):
            hits.append(("MENTION", i + 1, ln.strip()))
            continue
        after = ln.split(needle, 1)[1]
        explicit = bool(re.search(r"\]\s*\+\s*list\(|,\s*(scratch|tmp|SRC|root|"
                                  r"os\.path\.join|argv)", after))
        hits.append(("EXEC-EXPLICIT-PATH" if explicit else "EXEC-NO-ARG",
                     i + 1, ln.strip()))
    return hits


def classify(path, needle):
    try:
        text = git("show", "HEAD:%s" % path)
    except SystemExit:
        return []
    return classify_text(text, needle)


def main(subject):
    subject = subject.rstrip("/")
    scripts = scripts_of(subject)
    if not scripts:
        raise SystemExit("consumers: %s has no tracked *.py/*.sh -- refusing "
                         "to report an empty census as a clean one" % subject)

    print("=" * 78)
    print("mg-6e4f -- CONSUMERS OF %s" % subject)
    print("=" * 78)
    print()
    print("  mg-20ee condition 3: before pinning, find every instrument that")
    print("  RUNS this one and re-measure it.  METHOD AND BLIND SPOT are in")
    print("  this file's docstring and are not repeated here; what is repeated")
    print("  is the one sentence that matters -- THIS CENSUS IS NOT A")
    print("  BACKSTOP.  See section D.")
    print()
    print("  THE COUNTS BELOW ARE CORPUS-VALUED AND THIS INSTRUMENT IS NOT")
    print("  PINNED, DELIBERATELY.  census.py reads its corpus at a declared")
    print("  commit so that a repair can be watched shrinking.  This one must")
    print("  answer about the tree you are ABOUT TO CHANGE, so it reads HEAD,")
    print("  and its figures move when the estate does -- `run_all.sh (193")
    print("  files)` became `(192)` the day main folded one suite into")
    print("  another.  A moved count here is the corpus moving, not a finding;")
    print("  what would be a finding is a NAME appearing in or leaving")
    print("  section A.")
    print()
    print("  subject scripts: %d" % len(scripts))
    for s in scripts:
        print("      %s" % os.path.basename(s))
    print()

    # A BASENAME IS NOT A NAME.  See the docstring: `run_all.sh` belongs to
    # about 220 tracked files and the first version of this census reported
    # build.sh and every README in the repository as consumers of this
    # instrument's runner.  A script is searched for by BASENAME only when
    # that basename is unique in the repository; otherwise by FULL PATH, and
    # the split is printed so a reader knows which rule covered what.
    tracked = git("ls-files").splitlines()
    freq = {}
    for p in tracked:
        freq[os.path.basename(p)] = freq.get(os.path.basename(p), 0) + 1

    needles, shared = [], []
    for s in scripts:
        base = os.path.basename(s)
        if freq.get(base, 0) > 1:
            needles.append((s, s))
            shared.append((base, freq[base]))
        else:
            needles.append((s, base))

    prose = 0
    by_kind = {"EXEC-NO-ARG": [], "EXEC-EXPLICIT-PATH": [], "MENTION": []}
    unnamed = []
    for s, needle in needles:
        hits = git_grep_l(needle, CODE_GLOBS)
        if not hits:
            unnamed.append(os.path.basename(s))
        for path in hits:
            if path.startswith(subject + "/") or path.startswith(SELF + "/"):
                continue
            for kind, lineno, ln in classify(path, needle):
                by_kind[kind].append((path, os.path.basename(s), lineno, ln))
        for path in git_grep_l(needle, PROSE_GLOBS):
            if not (path.startswith(subject + "/")
                    or path.startswith(SELF + "/")):
                prose += 1

    print("  matched by basename: %d script(s); by FULL PATH: %d, because the"
          % (len(scripts) - len(shared), len(shared)))
    print("  basename is shared -- %s"
          % (", ".join("%s (%d files)" % (b, n) for b, n in shared)
             if shared else "none"))
    print("  documentation mentions in *.md / *.txt, counted and NOT listed")
    print("  because prose cannot execute anything: %d file(s)" % prose)
    print()
    # mg-4020.  THIS LINE IS WHERE THIS CENSUS USED TO DIE.  `git grep` exits
    # 1 for no match, git() treated every non-zero as fatal, and a subject
    # script that nothing outside its own directory names took the whole run
    # down -- on 23 of the 27 instruments still on the pinning work-list.  The
    # count is PRINTED rather than merely tolerated, because it is the one
    # number that says how much of the subject this census could say nothing
    # about, and a repair that turned a crash into a silence would be worse
    # than the crash.  A HIGH FIGURE HERE IS NOT A CLEAN RESULT: it means most
    # of the subject's scripts are reached, if at all, by a route section D's
    # blind-spot list already names.
    print("  subject scripts NAMED IN NO TRACKED *.py / *.sh OUTSIDE their")
    print("  own directory: %d of %d%s"
          % (len(unnamed), len(scripts),
             (" -- " + ", ".join(unnamed)) if unnamed else ""))
    print("  For these the census has NO EVIDENCE EITHER WAY.  A pin to one")
    print("  of them is covered by section D's backstop and by nothing here.")
    print()

    print("-" * 78)
    print("A  EXECUTIONS WITH NO PATH ARGUMENT -- these get the pinned default")
    print("-" * 78)
    print()
    if not by_kind["EXEC-NO-ARG"]:
        print("  none.  A pin here disturbs no other instrument by this")
        print("  method, which is NOT the same as disturbing none.")
    for path, base, lineno, _ln in sorted(by_kind["EXEC-NO-ARG"]):
        print("  %-52s runs %s" % (path, base))
        print("        line %d" % lineno)
    print()

    print("-" * 78)
    print("B  EXECUTIONS THAT PASS A PATH, and mentions with no exec token")
    print("-" * 78)
    print()
    print("  An explicit path is chosen by the caller and a pin does not")
    print("  reach it.  A bare mention is printed rather than dropped: it is")
    print("  the residue of this method, and an import lands here.")
    print()
    for kind in ("EXEC-EXPLICIT-PATH", "MENTION"):
        seen = set()
        for path, base, _lineno, _ln in sorted(by_kind[kind]):
            if (path, base) in seen:
                continue
            seen.add((path, base))
            print("  %-14s %-46s %s" % (kind.split("-")[-1].lower(), path,
                                        base))
    print()

    confirmed = sorted({instrument_of(p)
                        for p, _b, _n, _l in by_kind["EXEC-NO-ARG"]})
    mentioned = sorted({instrument_of(p)
                        for p, _b, _n, _l in by_kind["MENTION"]}
                       - set(confirmed))
    dirs = confirmed + mentioned

    print("-" * 78)
    print("C  THE INSTRUMENTS TO RE-MEASURE, and their runners")
    print("-" * 78)
    print()
    print("  THE WORK-LIST IS C1 PLUS C2, NOT C1.  The exec rule CONFIRMS a")
    print("  consumer; it does not refute one.  A file that names a script in")
    print("  code and whose exec token this rule did not see is UNCONFIRMED,")
    print("  not cleared, and it goes on the list.")
    print()
    print("  THIS IS NOT A PRECAUTION, IT IS A MEASURED MISS.  mg-6e4f had to")
    print("  repair code/species_extent_d633/e1_extents.py -- E1a went")
    print("  `18 file(s)` -> `0` and E1 TOTAL BAD 0 -> 3 under the pin -- and")
    print("  THIS CENSUS DOES NOT CONFIRM IT.  e1 spawns")
    print("  `[sys.executable, TRACER, os.path.basename(path)]`, so the")
    print("  script's name reaches the exec through TWO variables and is")
    print("  nowhere near an exec token on the page.  It lands in C2.  A")
    print("  reader who works C1 only would have shipped that breakage.")
    print()
    print("  C1  CONFIRMED -- an exec token stands beside the name")
    for d in confirmed:
        runner = os.path.join(d, "run_all.sh")
        has = os.path.isfile(os.path.join(ROOT, runner))
        print("      %-42s %s" % (d, "sh %s" % runner if has
                                  else "NO run_all.sh -- run its scripts"))
    if not confirmed:
        print("      none")
    print()
    print("  C2  UNCONFIRMED -- names the script in *.py / *.sh, exec not seen")
    for d in mentioned:
        runner = os.path.join(d, "run_all.sh")
        has = os.path.isfile(os.path.join(ROOT, runner))
        print("      %-42s %s" % (d, "sh %s" % runner if has
                                  else "NO run_all.sh -- run its scripts"))
    if not mentioned:
        print("      none")
    print()

    print("-" * 78)
    print("D  THE BACKSTOP, WHICH IS NOT THIS CENSUS")
    print("-" * 78)
    print()
    print("  Every name above came from a grep for a filename, so a consumer")
    print("  reached by a constructed path, by a wrapper more than one hop")
    print("  away, or from outside this repository IS NOT IN IT.  The census")
    print("  cannot check itself.  What can: run each consumer BEFORE and")
    print("  AFTER the pin and diff the two outputs.  A missed consumer shows")
    print("  up in that diff whether or not it was enumerated -- provided you")
    print("  run the suite it lives in.")
    print()
    print("  For each instrument in section C:")
    print()
    print("      git stash push -- <the pinned file>   # or check out the")
    print("                                            # pre-pin revision")
    print("      sh <dir>/run_all.sh > /tmp/pre.txt 2>&1")
    print("      git stash pop")
    print("      sh <dir>/run_all.sh > /tmp/post.txt 2>&1")
    print("      diff /tmp/pre.txt /tmp/post.txt")
    print()
    print("  An EMPTY diff is the result you want and it is a MEASUREMENT.")
    print("  A non-empty one is either the pin reaching a consumer -- fix the")
    print("  consumer or the pin, do not pin over it -- or that consumer's")
    print("  own pre-existing staleness, which is a FINDING and belongs in")
    print("  its own work item rather than in a pinning commit.")
    print()
    print("  AND THE LIMIT THAT DOES NOT GO AWAY, PRINTED BECAUSE IT IS THE")
    print("  LOAD-BEARING SENTENCE IN THIS RUN: a consumer this census misses")
    print("  AND that nobody runs is INVISIBLE, and no instrument in this")
    print("  directory fixes that.  Six of nine consumers were found affected")
    print("  by RUNNING them.  That is a statistic about things that were run,")
    print("  so it cannot license `a missed consumer would announce itself`.")
    print("  THE BACKSTOP ABOVE IS THE LOAD-BEARING HALF; THIS CENSUS IS A")
    print("  PREFILTER.  A method that says which half is which degrades")
    print("  safely; one that does not degrades silently.")
    print()
    print("=" * 78)
    print("CONSUMERS: %d no-arg execution(s) CONFIRMED across %d instrument(s);"
          % (len(by_kind["EXEC-NO-ARG"]), len(confirmed)))
    print("           %d further instrument(s) UNCONFIRMED.  WORK-LIST: %d."
          % (len(mentioned), len(dirs)))
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1
                  else os.path.join("code", "species_remainder_f8fa")))
