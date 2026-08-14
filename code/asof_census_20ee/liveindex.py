"""LIVEINDEX -- THE FIGURE WITH THE SHORT HALF-LIFE, MEASURED OVER ITS OWN RECORD.

mg-ede8's finding, in one sentence: `consumers.py` reads the LIVE INDEX by
design, so its figures are a function of WHEN YOU RAN IT and not of the commit
you attach them to -- and out_consumers.txt has therefore shipped STALE AT ITS
OWN COMMIT, repeatedly, with no instrument in the estate able to see it.

THE PART THAT WAS ALREADY KNOWN AND THE PART THAT WAS NOT.  That consumers.py
is unpinned is DELIBERATE and is printed in its own transcript: census.py reads
its corpus at a declared commit so a repair can be watched shrinking, and this
one must answer about the tree you are ABOUT TO CHANGE.  What nobody had drawn
is the consequence.  A figure read at time T is committed at time T+d, and in
between the estate moves -- most reliably in the merge queue, where the refinery
REBASES the branch onto a main that has landed directories since.  So the
staleness is CREATED AFTER THE LAST MOMENT ANY INSTRUMENT ON THE BRANCH CAN RUN,
which is why being careful does not close it: tranche 7 diagnosed the defect in
the commit message of the commit that was carrying it.

    WHAT THIS FILE IS.  A POST-HOC CENSUS, not a gate.  For every committed
    version of a declared live-index transcript it reads the figure OUT OF THE
    TRANSCRIPT AS COMMITTED and RE-DERIVES it AT THE COMMIT THAT CARRIES IT, and
    prints STALE or AGREES.  That comparison needs no instrument execution and no
    dirty tree, so every figure below is a function of ONE COMMIT -- which is why
    THIS transcript reproduces byte-identically while its subject cannot.  That
    is the only honest arrangement for the file whose subject is a transcript
    that has no fixed point, and it is worklist.py's and exemplars.py's
    arrangement arriving on a third subject.

    THE CLASS IT CAN ANSWER ABOUT, DECLARED AS A LIMIT AND NOT AS A SCOPE.
    A figure is re-derivable at an arbitrary commit exactly when it is a
    function of the TRACKED PATH LIST ALONE -- `git ls-tree -r --name-only`.
    Three of out_consumers.txt's figures are, and they are the three below.
    Its CONTENT-valued figures -- the prose count, the unnamed-scripts count,
    and the whole of sections A, B and C -- are functions of the content of
    every *.py/*.sh/*.md/*.txt at that commit, and re-deriving them means
    running the census there, which means running TODAY'S rule against an OLD
    tree and calling the difference staleness.  That conflates the corpus
    moving with the instrument changing, and this file will not do it.  So
    AGREES here is ONE-DIRECTIONAL in exactly the sense worklist.py's NOT
    FALSIFIED is: a STALE verdict proves the transcript was wrong at its own
    commit, and an AGREES verdict proves NOTHING about the figures this file
    cannot see.  N31 asserts that on the rule rather than on an instance.

    AND THE HALF THAT IS NOT A LIMIT BUT A PRICE.  Because the staleness is
    created by the rebase, NO instrument that runs before the merge can prevent
    it.  Wiring this into the gate would turn every branch red whenever main
    landed a directory under code/ -- mg-724a's `a gate that fails for reasons
    the author cannot act on` -- so the live half of this file is REPORTED ON
    STDERR AND GATES NOTHING, which is mg-724a's recorded/gated split applied to
    a live-index figure.  What would close it is a refinery that re-runs and
    amends AFTER the rebase, and that is somebody else's instrument.

    sh code/asof_census_20ee/run_all.sh         # runs this at AS_OF
    python3 code/asof_census_20ee/liveindex.py  # the same, plus the live half
"""

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

# The commit every figure on stdout is a function of.  An ancestor of
# origin/main -- mg-20ee's condition 1 applied to this file's own transcript --
# and the reason that transcript has a fixed point where its subject has none.
# Move it deliberately, and re-run.
AS_OF = "2901996"

# THE REGISTRY.  ONE ROW, AND IT IS ONE ROW BECAUSE ONE TRANSCRIPT IN THIS
# DIRECTORY READS THE LIVE INDEX -- census.py, permuted.py, worklist.py and
# exemplars.py all read a DECLARED COMMIT, and pinnable.py is a hand-run whose
# input is a dirty tree.  That is a statement about this directory and not about
# the estate: nothing here scans code/ for other live-index producers, so a
# transcript one directory over with the same property is invisible to this
# file, which is the second half of N31.
WATCHED = (("code/asof_census_20ee/out_consumers.txt",
            "code/asof_census_20ee/consumers.py"),)

# THE READERS.  Each is a regex over the transcript's own printed line, because
# the figure has to be recovered from a version of the file that was written
# before this instrument existed -- an import cannot reach backwards.  A reader
# that does not match returns UNREADABLE and is PRINTED as such; it is never
# silently skipped, for git_grep_l's reason one file over: a census that reports
# `clean` because it never looked is the failure the method is written against.
SUBJECT = re.compile(r"^mg-\S+ -- CONSUMERS OF (\S+)\s*$", re.M)
SHARED_LINE = re.compile(r"^\s*basename is shared -- (.*)$", re.M)
SHARED_PAIR = re.compile(r"([^\s,]+) \((\d+) files\)")
N_SCRIPTS = re.compile(r"^\s*subject scripts: (\d+)\s*$", re.M)
N_SPLIT = re.compile(r"^\s*matched by basename: (\d+) script\(s\); "
                     r"by FULL PATH: (\d+),", re.M)

UNREADABLE = object()


def git(*args):
    got = subprocess.run(["git", "-C", ROOT, *args], capture_output=True)
    if got.returncode != 0:
        raise SystemExit("liveindex: git %s failed: %s"
                         % (" ".join(args),
                            got.stderr.decode("utf-8", "replace").strip()))
    return got.stdout.decode("utf-8", "surrogateescape")


def paths_at(rev):
    """The tracked path list at `rev`.  `None` means the INDEX.

    The two are the same thing on a clean tree, and the distinction is not
    cosmetic: consumers.py builds its frequency table from `git ls-files`, which
    is the INDEX, while its section A/B/C greps run against HEAD.  So the
    census is already a mixture of two trees and a dirty worktree splits them --
    a separate finding, reported in section 4 and repaired by nothing here.
    """
    if rev is None:
        return git("ls-files").splitlines()
    return git("ls-tree", "-r", "--name-only", rev).splitlines()


def figures_from_paths(subject, paths):
    """consumers.py's THREE PATH-LIST-VALUED FIGURES, from a path list alone.

    A RE-STATEMENT of consumers.main's `freq` loop and its unique/shared split,
    deliberately and not an import: consumers.main is one function that prints
    as it goes, and the figures have to be computable for a tree that is not
    checked out.  A re-statement can drift from the original, so P34 runs the
    REAL consumers.py and requires this to agree with what it printed -- the
    drift is measured rather than promised.
    """
    freq = {}
    for p in paths:
        base = os.path.basename(p)
        freq[base] = freq.get(base, 0) + 1
    scripts = sorted(p for p in paths
                     if p.startswith(subject + "/")
                     and (p.endswith(".py") or p.endswith(".sh")))
    shared = sorted((os.path.basename(s), freq[os.path.basename(s)])
                    for s in scripts if freq.get(os.path.basename(s), 0) > 1)
    return {"n_scripts": len(scripts),
            "n_unique": len(scripts) - len(shared),
            "n_shared": len(shared),
            "shared": shared}


def figures_from_transcript(page):
    """The same three figures, read back out of a committed transcript."""
    m = SUBJECT.search(page)
    subject = m.group(1) if m else None
    got = {"subject": subject}

    m = N_SCRIPTS.search(page)
    got["n_scripts"] = int(m.group(1)) if m else UNREADABLE

    m = N_SPLIT.search(page)
    got["n_unique"] = int(m.group(1)) if m else UNREADABLE
    got["n_shared"] = int(m.group(2)) if m else UNREADABLE

    # A LINE THAT IS PRESENT AND DOES NOT PARSE IS UNREADABLE, NOT ZERO, AND
    # THIS FILE HAD THE OTHER DEFECT ON ITS FIRST RUN.  P34's plant empties the
    # shared line and the first draft graded the result STALE -- `said nothing,
    # tree says one` -- which is a census reporting a FINDING about a figure it
    # had failed to read.  So the payload must be `none` or must be EXACTLY the
    # pairs, reconstructed in consumers.py's own spelling and compared: a
    # partially-parsed line is the shape that turns an unreadable transcript
    # into a confident wrong answer.
    m = SHARED_LINE.search(page)
    if m is None:
        got["shared"] = UNREADABLE
        return got
    payload = m.group(1).strip()
    pairs = sorted((n, int(c)) for n, c in SHARED_PAIR.findall(payload))
    if payload == "none":
        got["shared"] = []
    elif not payload:
        # AN EMPTY PAYLOAD RECONSTRUCTS EXACTLY AND IS STILL UNREADABLE, and
        # this clause is the second half of the same first-run defect: the
        # reconstruction test alone accepts "" as zero pairs, because "" is
        # what joining nothing produces.  consumers.py prints `none` for zero
        # and never prints nothing, so an empty payload is a transcript this
        # reader does not understand rather than a transcript reporting none.
        got["shared"] = UNREADABLE
    elif ", ".join("%s (%d files)" % p for p in pairs) == payload:
        got["shared"] = pairs
    else:
        got["shared"] = UNREADABLE
    return got


# The three figures, in the order they are printed, with the name each is
# reported under.  `shared` is the one that has drifted; the other two are the
# WRONG-DIRECTION half of the same measurement and are not decoration -- an
# instrument that reported STALE on everything it looked at would be
# indistinguishable, in its own transcript, from one that had found something.
FIELDS = (("subject scripts", "n_scripts"),
          ("unique-basename scripts", "n_unique"),
          ("shared-basename scripts", "n_shared"),
          ("shared basename counts", "shared"))


def compare(said, tree):
    """(field, said, tree, verdict) for each declared figure."""
    rows = []
    for label, key in FIELDS:
        was, now = said.get(key, UNREADABLE), tree[key]
        if was is UNREADABLE:
            rows.append((label, "UNREADABLE", now, "UNREADABLE"))
        else:
            rows.append((label, was, now, "AGREES" if was == now else "STALE"))
    return rows


def versions(rev, transcript):
    """The commits that WROTE this transcript, newest first, at `rev`.

    The question is `was it already wrong when it was written`, so the
    population is the commits that changed the file and not every commit --
    a transcript that goes wrong later without being rewritten is the corpus
    moving, which consumers.py's own header declares and which is not a finding.
    """
    return git("log", "--follow", "--format=%H", rev, "--",
               transcript).split()


def scan(rev=AS_OF):
    """Every figure this file publishes on stdout, from one commit and nothing
    else.  SEPARATE FROM THE PRINTING SO THE CONTROLS CAN CALL IT, and it opens
    no file: P33 replaces `open` for the whole scan and asserts the list is
    empty, which is P26's and P29's control on a third subject.
    """
    out = {"rev": rev, "watched": []}
    for transcript, producer in WATCHED:
        rows = []
        for commit in versions(rev, transcript):
            page = git("show", "%s:%s" % (commit, transcript))
            said = figures_from_transcript(page)
            subject = said["subject"]
            if subject is None:
                rows.append({"commit": commit, "subject": None,
                             "rows": [], "verdict": "UNREADABLE",
                             "producer_moved": False})
                continue
            tree = figures_from_paths(subject, paths_at(commit))
            cmp_rows = compare(said, tree)
            grades = [g for _l, _w, _n, g in cmp_rows]
            touched = git("show", "--name-only", "--format=", commit).split()
            rows.append({
                "commit": commit,
                "subject": subject,
                "rows": cmp_rows,
                "verdict": ("UNREADABLE" if "UNREADABLE" in grades
                            else "STALE" if "STALE" in grades else "AGREES"),
                "producer_moved": producer in touched,
            })
        out["watched"].append({"transcript": transcript,
                               "producer": producer, "versions": rows})
    return out


def live(rev="HEAD"):
    """The same rule at `rev` against the INDEX -- the live half.

    IT READS THE COMMITTED TRANSCRIPT AND NOT THE WORKTREE ONE, AND THAT IS THE
    WHOLE DESIGN.  run_all.sh regenerates out_consumers.txt two lines above this
    file, so a comparison against the worktree copy would be a comparison of a
    figure with itself -- it would pass on every run and say nothing.  Reading
    the COMMITTED copy asks the question that is actually open: is the transcript
    THIS TREE CARRIES stale for THIS TREE, right now.
    """
    got = []
    for transcript, _producer in WATCHED:
        said = figures_from_transcript(git("show", "%s:%s" % (rev, transcript)))
        if said["subject"] is None:
            got.append((transcript, None, []))
            continue
        tree = figures_from_paths(said["subject"], paths_at(None))
        got.append((transcript, said["subject"], compare(said, tree)))
    return got


def show(value):
    if value is UNREADABLE or value == "UNREADABLE":
        return "UNREADABLE"
    if isinstance(value, list):
        return ", ".join("%s (%d files)" % (n, c) for n, c in value) or "none"
    return str(value)


def main():
    bar = "=" * 78
    result = scan()
    print(bar)
    print("mg-ede8 -- WAS THE TRANSCRIPT ALREADY STALE AT ITS OWN COMMIT?")
    print(bar)
    print()
    print("  AS_OF = %s.  Every figure on this page is a function of that one" % AS_OF)
    print("  commit, read through `git log`, `git show` and `git ls-tree`, so")
    print("  THIS transcript has a fixed point where its subject has none.")
    print()

    print("-" * 78)
    print("1  THE RULE, AND THE CLASS IT CAN ANSWER ABOUT")
    print("-" * 78)
    print()
    print("  A figure is re-derivable at an arbitrary commit exactly when it is")
    print("  a function of the TRACKED PATH LIST ALONE.  Then the transcript's")
    print("  own printed number can be compared with the number the tree that")
    print("  CARRIES that transcript implies -- no instrument is executed, no")
    print("  worktree is touched, and today's rule is never run against an old")
    print("  tree.  The four figures below are that class for this subject:")
    print()
    for label, _key in FIELDS:
        print("      %s" % label)
    print()
    print("  EVERYTHING ELSE IN out_consumers.txt IS CONTENT-VALUED and is NOT")
    print("  checked here: the prose count, the named-in-no-tracked-file count,")
    print("  and the whole of sections A, B and C.  So STALE is a proof and")
    print("  AGREES is not -- N31, and it is asserted on the rule.")
    print()

    for watched in result["watched"]:
        print("-" * 78)
        print("2  %s" % watched["transcript"])
        print("-" * 78)
        print()
        print("  Produced by %s, which reads the live index." % watched["producer"])
        print("  One line per commit that WROTE this file, newest first.  `said`")
        print("  is what the committed copy printed; `tree` is what the commit")
        print("  carrying it actually held.")
        print()
        for v in watched["versions"]:
            print("  %s   %s%s" % (v["commit"][:7], v["verdict"],
                                   "   (this commit also changed the producer)"
                                   if v["producer_moved"] else ""))
            for label, was, now, grade in v["rows"]:
                if grade == "AGREES":
                    continue
                print("      %-26s said %-22s tree %s"
                      % (label, show(was), show(now)))
            if v["subject"] is None:
                print("      no CONSUMERS OF header -- this file cannot say")
                print("      which subject the figures were about, and reports")
                print("      that rather than guessing one.")
        print()

        total = len(watched["versions"])
        stale = [v for v in watched["versions"] if v["verdict"] == "STALE"]
        agree = [v for v in watched["versions"] if v["verdict"] == "AGREES"]
        bad = [v for v in watched["versions"] if v["verdict"] == "UNREADABLE"]
        print("  %d of %d committed versions were ALREADY WRONG when they were"
              % (len(stale), total))
        print("  written; %d agreed and %d could not be read." % (len(agree), len(bad)))
        print()

        # THE DIRECTION IS PRINTED BECAUSE ONE OF THEM IS NOT THE ONE THE TICKET
        # LOOKED FOR.  A transcript whose count is TOO HIGH was taken on a tree
        # holding MORE of the named file than the commit that carries it -- the
        # estate shrinking under the run, or a run taken on another branch.
        # Reporting only the low direction would have made this a census of
        # `main landed something while I was open`, which is a smaller claim.
        low, high = [], []
        for v in stale:
            for label, was, now, grade in v["rows"]:
                if grade != "STALE" or label != "shared basename counts":
                    continue
                for (n, c), (n2, c2) in zip(was, now):
                    (low if c < c2 else high).append((v["commit"][:7], n, c, c2))
        print("  THE DRIFT GOES BOTH WAYS, and only one of the two directions")
        print("  had been looked for.  %d version(s) UNDER-COUNT a shared" % len(low))
        print("  basename and %d OVER-COUNT one:" % len(high))
        print()
        for commit, name, was, now in low + high:
            print("      %s  %-14s said %-5d tree %-5d  %+d"
                  % (commit, name, was, now, was - now))
        print()

    print("-" * 78)
    print("3  WHY BEING CAREFUL DOES NOT CLOSE THIS")
    print("-" * 78)
    print()
    print("  The figure is read at time T and committed at time T+d.  The")
    print("  reliable value of d is THE MERGE QUEUE: the refinery rebases the")
    print("  branch onto a main that has landed directories since the run, and")
    print("  the rebase happens AFTER the last moment any instrument on the")
    print("  branch can run.  So this cannot be repaired by an author being")
    print("  careful, and tranche 7 is the proof -- it diagnosed the drift in")
    print("  the commit message of the commit whose transcript was carrying it.")
    print()
    print("  WHAT WOULD ACTUALLY CLOSE IT, and none of it is done here:")
    print("      * the refinery re-runs the producer and amends AFTER rebase;")
    print("      * or the figure stops being live-index-valued, which contradicts")
    print("        the reason consumers.py is unpinned and would be a change to")
    print("        what it MEASURES rather than to how it is recorded;")
    print("      * or the gate refuses, which is mg-724a's `a gate that fails")
    print("        for reasons the author cannot act on` and is why the live")
    print("        half below is on STDERR and gates nothing.")
    print()

    print("-" * 78)
    print("4  A SECOND MIXTURE, REPORTED AND NOT REPAIRED")
    print("-" * 78)
    print()
    print("  consumers.py builds its frequency table from `git ls-files`, which")
    print("  is the INDEX, and runs its section A/B/C greps against HEAD.  On a")
    print("  clean tree those are the same tree and the census is coherent; on a")
    print("  dirty one they are not, and the counts and the listings answer")
    print("  about different trees with nothing saying so.  Every figure in")
    print("  section 2 is taken from `git ls-tree` at a COMMIT, so this file is")
    print("  not exposed to it -- which is also why it cannot measure it.")
    print("  It belongs to consumers.py and is left there.")
    print()

    stale_now = []
    for transcript, subject, rows in live():
        for label, was, now, grade in rows:
            if grade != "AGREES":
                stale_now.append((transcript, label, was, now, grade))
    if stale_now:
        sys.stderr.write(
            "liveindex: THE COMMITTED TRANSCRIPT IS STALE FOR THIS TREE RIGHT "
            "NOW --\n")
        for transcript, label, was, now, grade in stale_now:
            sys.stderr.write("    %s  %s: said %s, index holds %s (%s)\n"
                             % (transcript, label, show(was), show(now), grade))
        sys.stderr.write(
            "  Re-run the producer and commit the refresh.  THIS IS NOT A GATE "
            "and it\n  is not on stdout: it is a function of when you ran it, "
            "which is the\n  property this whole file is about.\n")
    else:
        sys.stderr.write("liveindex: the committed transcript agrees with this "
                         "tree on every path-list-valued figure.\n")

    total = sum(len(w["versions"]) for w in result["watched"])
    stale = sum(1 for w in result["watched"] for v in w["versions"]
                if v["verdict"] == "STALE")
    print(bar)
    print("LIVE-INDEX: %d of %d committed version(s) of %d watched transcript(s)"
          % (stale, total, len(WATCHED)))
    print("            were ALREADY STALE at their own commit, at AS_OF %s."
          % AS_OF)
    print("            AGREES is one-directional: it covers the path-list-valued")
    print("            figures and nothing else (N31).")
    print(bar)
    return 0


if __name__ == "__main__":
    sys.exit(main())
