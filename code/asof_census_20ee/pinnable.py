"""PINNABLE -- THE PRE-CONDITION ON mg-20ee's CONDITIONS 1-3.

mg-20ee's method for pinning a transcript has three conditions, in this order:

    1.  git merge-base --is-ancestor <declared-commit> origin/main   -- YES
    2.  the transcript reproduces byte-identically AT that commit
    3.  every instrument that RUNS this one is re-measured (consumers.py)

All three assume the question has already been settled.  This file asks it:

    0.  IS A PIN THE REMEDY FOR THIS INSTRUMENT'S DRIFT AT ALL?

WHY THIS EXISTS, AND IT IS NOT A HYPOTHETICAL.  mg-20ee's 44 candidates were
nominated by census.py, which is a classifier FOR FOREIGN ADDRESSES -- so an
address-only difference is exactly what it went looking for.  Working the
remaining work-list IN ITS OWN DRIFT ORDER, mg-4020 took the two cheapest
instruments on it and NEITHER IS PINNABLE, for two different reasons:

    code/species_repair_a4ef        2+/5-.  Its whole drift is three lines
                                    naming `__pycache__` directories in
                                    SIBLING trees.  Those are in .gitignore,
                                    so they are in NO COMMIT, and no AS_OF
                                    can restore them.  MEASURED BOTH WAYS at
                                    HEAD with no pin whatever: create the
                                    three empty directories and the committed
                                    transcript reproduces BYTE-IDENTICALLY;
                                    remove them and the 2+/5- returns.  The
                                    transcript is a function of WHICH SUITES
                                    THE OPERATOR HAS RUN, not of repo state.

    code/state_relocation_audit_b0ae  7+/7-.  ALREADY PINNED -- libb0ae.py
                                    declares OLD_REV=78ae4d9 and
                                    NEW_REV=cc4c663 and reads every input
                                    through `git show <rev>:<path>`.  Its
                                    drift is entirely in B8.2, a section its
                                    own runner header declares to be "about
                                    the repo as it stands".  A pin there
                                    would not repair the section; it would
                                    DELETE THE QUESTION THE SECTION ASKS.

A third, for contrast, IS reachable by a pin: code/landscape_repair_1953,
whose drift is a walk of docs/ that has gone `23` -> `44` occurrences as the
corpus grew from 267 to 530 files.  Those addresses are tracked files.  That
is the shape mg-20ee's remedy was built for.

    SO THE POPULATION IS NOT 26 PINNINGS.  Whether it is mostly pinnings is
    NOT KNOWN AND IS NOT CLAIMED HERE -- three instruments is three
    instruments.  What is established is that the work-list is a list of
    instruments whose transcripts DRIFT, and that "drifts" and "wants an
    AS_OF" are different properties, so the second must be measured per
    instrument rather than inherited from membership of the list.
    mg-54b1's sweep reached the same conclusion from the other direction on
    an UNSELECTED sample, which is why this is written down as a rule and
    not as an anecdote.

    THE METHOD, STATED SO THAT IT CAN BE ARGUED WITH:

      * INPUT IS A DIFF, NOT A GUESS.  This reads `git diff -- <subject>` in
        the worktree as it stands, so you must have RUN the suite and NOT yet
        restored it.  An empty diff is REFUSED rather than reported clean:
        nothing to classify is not the same as nothing to fix, and this
        instrument has no way to tell a reproducing suite from one you forgot
        to run.  ground_truth.sh already makes exactly this run.

      * R1  IGNORED ADDRESS.  A changed line names a path that `git
        check-ignore` matches.  Git is configured never to track it, so it is
        in no commit, so NO AS_OF PIN REACHES IT.  Both `<path>` and
        `<path>/` are tested, because `__pycache__/` in .gitignore carries a
        trailing slash and matches DIRECTORIES ONLY -- `check-ignore` returns
        1 for the same path written without it, and a rule that tested one
        form would have missed the instance this was built from.

      * R2  ALREADY PINNED.  A tracked script in the subject carries a 7-to-40
        character hex token that `git cat-file -e` RESOLVES IN THIS
        REPOSITORY.  Resolution is what makes this a rule rather than a
        regex: `deadbeef` and an eight-letter word are both hex-shaped, and
        only a real object means somebody declared a revision.

      * R2 OVER-COUNTS, DECLARED AND MEASURED ON THE FIRST SUBJECT IT MET.
        It fires on a declared revision ANYWHERE in the subject's scripts,
        and a revision may be a CONTROL's rather than the corpus read's:
        species_repair_a4ef declares ebecd89 and 83ac472 in s1_extent.py,
        which are its controls (a) and (b) reading the PRE-REPAIR trees, and
        its corpus read is not pinned at all.  So R2 firing means "a revision
        is declared here, go and read why", and a rule that could tell a
        control's revision from a corpus pin would be a rule about the
        difference between an instrument's subject and its evidence -- which
        is not decidable from the token.  The bias is stated rather than
        tuned away, in the form census.py states its two.

      * NEITHER RULE IS A VERDICT.  R1 says a pin cannot remove THAT LINE.
        R2 says a pin already EXISTS.  Both are reasons to stop and look
        before spending the forty-five minutes conditions 1-3 cost; neither
        says the instrument is healthy, and R2 in particular is compatible
        with the instrument being badly wrong.

    AND THE BLIND SPOT, WHICH IS THE POINT OF WRITING THE METHOD DOWN:

      * R1 READS ADDRESSES, SO A BARE COUNT IS INVISIBLE TO IT.  This is not
        a supposition: species_repair_a4ef's own drift has TWO hunks, and the
        second is `9 stated, 0 not stated` -> `6 stated, 0 not stated` --
        the same defect, carrying no path at all.  R1 catches that instrument
        only because its FIRST hunk lists the directories.  An instrument
        that printed the count and not the list would be in this blind spot
        entirely, and would look like clean residue.
      * R2 CONFIRMS A PIN, NOT ITS COVERAGE.  b0ae is pinned and drifts
        anyway, which is the instance R2 was built from -- so R2 firing tells
        you where to read, not what to conclude.
      * RESIDUE IS NOT A PROMISE.  A drift this file cannot attribute to
        either rule may still be a moved verdict, a dead runner, or an
        operator-specific absolute path -- mg-20ee's own tranche 1 hit all
        three.  Residue means "conditions 1-3 are worth starting", nothing
        more.
      * THE DIFF IS THE ONLY EVIDENCE.  An instrument that writes outside its
        own directory, or that writes nothing at all because its runner is
        dead, produces a diff this file will read at face value.  mg-54b1
        measured that exact failure -- `NOTHING CHANGED` is not `IT
        REPRODUCED` -- and no rule here detects it.

    THE BLIND-SPOT LIST ABOVE IS LOAD-BEARING AND IS NOT TO BE TIDIED AWAY,
    for the reason consumers.py states one file over: a triage rule with no
    stated blind spot is indistinguishable, to its reader, from a verdict.
    THIS IS A PREFILTER.  THE BACKSTOP IS CONDITIONS 1-3 THEMSELVES -- search
    for the AS_OF and measure both directions -- and if you skip them because
    this file printed RESIDUE, you have used it as the opposite of what it is.

    sh code/asof_census_20ee/run_all.sh          # NOT run there: needs a
                                                # suite to have been run
    sh code/species_repair_a4ef/run_all.sh
    python3 code/asof_census_20ee/pinnable.py code/species_repair_a4ef
    git checkout -- code/species_repair_a4ef
"""

import os
import re
import subprocess
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", ".."))

# A repository-shaped path token: at least one `/`, no whitespace.  Deliberately
# looser than census.py's ADDR, which requires BOTH a known extension and a
# `:line` -- the instance this file was built from addresses a DIRECTORY with
# neither.  A trailing `:123` is stripped; trailing punctuation is not part of
# a path.
PATHTOK = re.compile(r"(?:[A-Za-z0-9_.\-]+/)+[A-Za-z0-9_.\-]+")
HEXTOK = re.compile(r"\b[0-9a-f]{7,40}\b")


def git(*args):
    got = subprocess.run(["git", "-C", ROOT, *args], capture_output=True)
    if got.returncode != 0:
        raise SystemExit("pinnable: git %s failed: %s"
                         % (" ".join(args),
                            got.stderr.decode("utf-8", "replace").strip()))
    return got.stdout.decode("utf-8", "surrogateescape")


def is_ignored(path):
    """True when git is CONFIGURED never to track `path`.

    Both `path` and `path + "/"` are tested.  `.gitignore`'s `__pycache__/`
    carries a trailing slash and so matches directories only; `check-ignore`
    answers 1 for the same path written without one, and the instance this
    rule exists for -- `code/species_7d75/__pycache__`, as a4ef prints it --
    is written without one.  Testing a single form silently halves the rule.
    """
    for form in (path, path.rstrip("/") + "/"):
        got = subprocess.run(["git", "-C", ROOT, "check-ignore", "-q", form],
                             capture_output=True)
        if got.returncode == 0:
            return True
    return False


def changed_lines(diff_text):
    """The added and removed lines of a unified diff, without its headers.

    `+++`/`---` are excluded: a diff header names the file under change, and
    counting it would make every diff address its own instrument.
    """
    out = []
    for ln in diff_text.splitlines():
        if ln[:3] in ("+++", "---") or not ln:
            continue
        if ln[0] in "+-":
            out.append(ln)
    return out


def addresses_of(diff_text):
    """Every distinct repository-shaped path token in a diff's changed lines."""
    seen = []
    for ln in changed_lines(diff_text):
        for tok in PATHTOK.findall(ln):
            tok = tok.rstrip(".,;:)")
            if tok and tok not in seen:
                seen.append(tok)
    return seen


def declared_revs(text, resolves):
    """Hex tokens in `text` that `resolves` accepts as real objects.

    `resolves` is injected so the control can plant a source without needing
    the planted revision to exist here.  RESOLUTION IS THE RULE: a regex over
    hex alone fires on `deadbeef`, on `accede`, and on the first eight
    characters of a hash printed in prose, and this rule is asserting that
    somebody DECLARED A REVISION.
    """
    return [t for t in dict.fromkeys(HEXTOK.findall(text)) if resolves(t)]


def resolver():
    def resolves(tok):
        got = subprocess.run(["git", "-C", ROOT, "cat-file", "-e",
                              tok + "^{commit}"], capture_output=True)
        return got.returncode == 0
    return resolves


def main(subject):
    subject = subject.rstrip("/")
    diff_text = git("diff", "--", subject)
    if not diff_text.strip():
        raise SystemExit(
            "pinnable: `git diff -- %s` is EMPTY, and this instrument\n"
            "  classifies a drift it is given rather than one it produces.\n"
            "  RUN THE SUITE FIRST and do not restore it:\n"
            "      sh %s/run_all.sh\n"
            "  An empty diff is refused rather than reported clean, because a\n"
            "  suite that reproduces and a suite you forgot to run look the\n"
            "  same from here -- which is mg-54b1's `NOTHING CHANGED is not IT\n"
            "  REPRODUCED`, and this file has no way to tell them apart."
            % (subject, subject))

    scripts = [p for p in git("ls-files", "--", subject).splitlines()
               if p.endswith(".py") or p.endswith(".sh")]

    print("=" * 78)
    print("mg-4020 -- IS A PIN THE REMEDY?  %s" % subject)
    print("=" * 78)
    print()
    print("  mg-20ee condition 0, asked BEFORE conditions 1-3 are paid for.")
    print("  METHOD AND BLIND SPOT are in this file's docstring and are not")
    print("  repeated here; what is repeated is the sentence that matters --")
    print("  THIS IS A PREFILTER AND NOT A VERDICT.  See the residue section.")
    print()
    print("  THIS INSTRUMENT ANSWERS ITS OWN TWO RULES AND THE ANSWERS ARE")
    print("  PRINTED RATHER THAN LEFT TO BE FOUND.  R2 fires on its own")
    print("  directory: census.py declares AS_OF = 5a62e8c.  And its OUTPUT")
    print("  carries ignored addresses whenever R1 does, so a committed")
    print("  transcript of this file is itself a document R1 would flag.")
    print("  Neither is a defect; both are the reason the rules are stated as")
    print("  `go and read why` rather than as verdicts.")
    print()
    print("  IT IS ALSO NOT PINNED AND NOT ON A BUILD PATH, DELIBERATELY.  It")
    print("  reads HEAD and the LIVE worktree diff because it must answer")
    print("  about the tree you are ABOUT TO CHANGE -- consumers.py's")
    print("  declaration, for the same reason.  It cannot go in run_all.sh")
    print("  because it REQUIRES a suite to have been run and not restored,")
    print("  which is a state no build path should be in.")
    print()

    lines = changed_lines(diff_text)
    addrs = addresses_of(diff_text)
    print("  changed lines: %d      distinct path tokens in them: %d"
          % (len(lines), len(addrs)))
    print("  subject scripts read for a declared revision: %d" % len(scripts))
    print()

    ignored = [a for a in addrs if is_ignored(a)]

    print("-" * 78)
    print("R1  IGNORED ADDRESSES -- git is configured never to track these,")
    print("    so they are in NO COMMIT and NO AS_OF PIN REACHES THEM")
    print("-" * 78)
    print()
    for a in ignored:
        print("      %s" % a)
    if not ignored:
        print("      none.  Which is NOT evidence that the drift is repo state:")
        print("      R1 reads ADDRESSES, and a drift that moved only a COUNT")
        print("      carries none.  species_repair_a4ef's own second hunk is")
        print("      exactly that shape.")
    print()

    resolves = resolver()
    pinned = []
    for s in scripts:
        for rev in declared_revs(git("show", "HEAD:%s" % s), resolves):
            pinned.append((s, rev))

    print("-" * 78)
    print("R2  DECLARED REVISIONS IN THE SUBJECT'S OWN SCRIPTS -- if these")
    print("    exist, SOMETHING HERE IS ALREADY PINNED")
    print("-" * 78)
    print()
    for s, rev in pinned:
        print("      %-52s %s" % (s, rev))
    if not pinned:
        print("      none")
    print()
    if pinned:
        print("  A REVISION IS DECLARED HERE AND THE TRANSCRIPT DRIFTS ANYWAY.")
        print("  READ THE INSTRUMENT BEFORE PINNING FURTHER:")
        print("  state_relocation_audit_b0ae is pinned twice over and its")
        print("  runner header DECLARES the exception -- B8.2 is 'about the")
        print("  repo as it stands', and pinning it would not repair the")
        print("  section, it would delete the question it asks.")
        print()
        print("  BUT THIS RULE OVER-COUNTS, DECLARED: a revision may be a")
        print("  CONTROL's rather than the corpus read's.  MEASURED on the")
        print("  first subject it met -- species_repair_a4ef's ebecd89 and")
        print("  83ac472 are its controls (a) and (b) reading the PRE-REPAIR")
        print("  trees, and its corpus read is not pinned at all.  R2 says GO")
        print("  AND READ WHY, and it does not say the corpus is pinned.")
        print()

    print("-" * 78)
    print("RESIDUE -- what a pin is CAPABLE of reaching.  NOT A PROMISE")
    print("-" * 78)
    print()
    residue = [a for a in addrs if a not in ignored]
    print("  %d of %d path token(s) are not ignored." % (len(residue), len(addrs)))
    print()
    print("  This is where conditions 1-3 BEGIN, not where they are answered.")
    print("  A residual drift may still be a moved verdict, a dead runner, or")
    print("  an absolute path that reproduced for exactly one operator --")
    print("  mg-20ee's tranche 1 hit all three, and none of them is a pin.")
    print("  IF YOU SKIP CONDITIONS 1-3 BECAUSE THIS SECTION IS NON-EMPTY,")
    print("  YOU HAVE USED THIS FILE AS THE OPPOSITE OF WHAT IT IS.")
    print()

    if ignored:
        verdict = "NOT WHOLLY PINNABLE -- %d ignored address(es)" % len(ignored)
    elif pinned:
        verdict = "ALREADY PINNED -- %d declared revision(s)" % len(pinned)
    else:
        verdict = "NO PRE-CONDITION FIRED -- proceed to conditions 1-3"
    print("=" * 78)
    print("PINNABLE: %s" % verdict)
    print("=" * 78)
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: pinnable.py <instrument-dir>   "
                         "(run its suite first, and do not restore it)")
    sys.exit(main(sys.argv[1]))
