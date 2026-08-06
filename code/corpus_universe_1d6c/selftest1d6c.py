"""SELFTEST -- every check of this suite proved able to fire before its pass is read.

THE RULE THIS FILE EXISTS FOR: a negative needs an instrument that could have shown
the positive.  `p1` reports that the glob's recursion blind spot costs ZERO sites.
That number is worth nothing unless the same code, pointed at a tree where a
subdirectory DOES hold a site, reports it.  Case U1 is that proof, and it is the most
important case in this file.

Each case constructs its input, ASSERTS THE INPUT IS WHAT IT CLAIMS TO BE, and only
then reads a verdict.  A mutation that did not mutate is a pass nobody earned.

EXIT 1 on any failing case.  PREDICTED 0 -- after the defects this file found in its
own suite were fixed; those are recorded in the README rather than erased.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

import lib1d6c as U
import p4_selfcheck as P4
import p5_declaration as P5

OUT = sys.stdout
BAD = []
N = [0]

SITE_UNB = "The Young-Fibonacci intervals number 33 and no scope is given here.\n"
SITE_BND = "The Young-Fibonacci intervals number 33 to rank 6.\n"
NOT_SITE = "There are 33 of them and nothing names the family.\n"


def ck(name, cond, extra=""):
    N[0] += 1
    if not cond:
        BAD.append(name)
    print("  %-64s %s%s" % (name[:64], "ok" if cond else "*** FAIL ***", extra),
          file=OUT)


def write(root, rel, body):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(body)
    return p


def main():
    U.rule(OUT, "SELFTEST mg-1d6c -- every check shown to fire")
    print(file=OUT)

    # ------------------------------------------------- U: the universes
    print("U  THE UNIVERSE CHECKS -- the ones p1's zero depends on", file=OUT)
    tmp = tempfile.mkdtemp(prefix="st1d6c_")
    try:
        write(tmp, "docs/top.md", SITE_UNB)
        write(tmp, "docs/state-history/deep.md", SITE_UNB)
        g = U.u_g_impl(tmp)
        d = U.u_m_disk(tmp)
        ck("U0 the constructed tree really holds 2 markdown files", len(d) == 2)
        ck("U1 THE GLOB MISSES A SUBDIRECTORY FILE (the positive p1's 0 needs)",
           g == ["docs/top.md"] and "docs/state-history/deep.md" in d,
           "   glob %d, disk %d" % (len(g), len(d)))
        gs = U.sites_of(tmp, g)
        ds = U.sites_of(tmp, d)
        ck("U2 and it misses the SITE in it, not merely the file",
           len(gs) == 1 and len(ds) == 2,
           "   glob %d site(s), disk %d" % (len(gs), len(ds)))
        ck("U3 the shell glob agrees with the implemented one on the same tree",
           U.u_g_shell(tmp) == g)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    tmp = tempfile.mkdtemp(prefix="st1d6c_g")
    try:
        subprocess.run(["git", "init", "-q"], cwd=tmp, capture_output=True)
        write(tmp, "a.md", SITE_UNB)
        write(tmp, "b.md", SITE_UNB)
        subprocess.run(["git", "add", "a.md"], cwd=tmp, capture_output=True)
        tracked = [x for x in U.git("ls-files", cwd=tmp).split("\n")
                   if x.endswith(".md")]
        disk = U.u_m_disk(tmp)
        ck("U4 the tracked/worktree hole shows a POSITIVE when one exists",
           tracked == ["a.md"] and sorted(disk) == ["a.md", "b.md"],
           "   tracked %d, disk %d" % (len(tracked), len(disk)))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ------------------------------------------------- P: the predicate
    print(file=OUT)
    print("P  THE PREDICATE AND THE PREFILTER", file=OUT)
    tmp = tempfile.mkdtemp(prefix="st1d6c_p")
    try:
        write(tmp, "unb.md", SITE_UNB)
        write(tmp, "bnd.md", SITE_BND)
        write(tmp, "no.md", NOT_SITE)
        write(tmp, "twice.md",
              "The Young-Fibonacci intervals number 33, and 33 again.\n")
        write(tmp, "struck.md", "**STRUCK** " + SITE_UNB)
        allp = ["unb.md", "bnd.md", "no.md", "twice.md", "struck.md"]
        s = U.sites_of(tmp, allp)
        by = dict((p, n) for p, n, _, _ in U.by_file(s))
        ck("P1 an unbounded site is found and scored unbounded",
           by.get("unb.md") == 1 and not [t for t in s
                                          if t[0] == "unb.md" and t[4]])
        ck("P2 a bounded site is found and scored bounded",
           by.get("bnd.md") == 1 and all(t[4] for t in s if t[0] == "bnd.md"))
        ck("P3 a sentence not naming the family is NOT a site", "no.md" not in by)
        ck("P4 the liveness rule removes a struck unit", "struck.md" not in by)
        occ = U.occurrences([t for t in s if t[0] == "twice.md"])
        ck("P5 GRAIN O counts occurrences, not sentences",
           by.get("twice.md") == 1 and occ == 2, "   1 site, %d occurrences" % occ)
        ck("P6 the prefilter drops exactly the files with no site and no others",
           U.prefilter(tmp, allp) == ["unb.md", "bnd.md", "twice.md", "struck.md"],
           "")
        ck("P7 prefiltered and unfiltered counts agree",
           sorted(U.sites_of(tmp, allp, use_prefilter=False)) == sorted(s))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ------------------------------------------------- S: the scope classifier
    print(file=OUT)
    print("S  THE SCOPE CLASSIFIER (p4 FIX 1)", file=OUT)
    ck("S1 a bare 'population' is not a numeric scope",
       P4.numeric_pass("the parent's population is wrong") is None)
    ck("S2 a count with its denominator is",
       P4.numeric_pass("4 of 9 sites are unbounded") is not None)
    ck("S3 a count with a named unit is",
       P4.numeric_pass("it drops 12 sites") is not None)
    ck("S4 a rank bound is",
       P4.numeric_pass("over the 33 intervals with rank(w) <= 6") is not None)
    ck("S5 an ordinal LABEL is not (the defect the first form had)",
       P4.numeric_pass("the row-10 sentence of section 3") is None)
    ck("S6 a PATH with a hex ticket id is not (the other first-form defect)",
       P4.numeric_pass("printed by code/branching_audit_19ec") is None)
    ck("S7 markdown emphasis does not hide a count",
       P4.numeric_pass("it drops **12** sites") is not None)
    ck("S8 s5's own OWNSCOPE DOES accept what S1 rejects -- the fix has an effect",
       bool(P4.S5.OWNSCOPE.search("the parent's population is wrong")))

    # ------------------------------------------------- F: the fault detector
    print(file=OUT)
    print("F  THE FAULT DETECTOR (p4 FIX 3)", file=OUT)
    for phrase, want in [("mg-19ec's predicate could not see it", True),
                         ("mg-19ec's predicate cannot see it", True),
                         ("mg-19ec's predicate can't see it", True),
                         ("the census never counted them", True),
                         ("the gate fails to cover them", True),
                         ("the parent's blind spot", True),
                         ("the census counted every site", False)]:
        ck("F: %-52s" % phrase[:52], bool(P4.FAULT_PROPERTY.search(phrase)) == want)
    ck("F8 the tense the parent's own regex misses IS missed by it",
       not P4.S5.FAULT.search("mg-19ec's predicate could not see it"))

    # ------------------------------------------------- G: the gate
    print(file=OUT)
    print("G  THE GATE'S PARTITION (p5)", file=OUT)
    for path, want in [("code/x/PREDICTIONS.md", "PRE-REGISTRATION"),
                       ("docs/audit-mg-1234-thing.md", "DATED RECORD"),
                       ("docs/OneThird-Branching-Graphs-Where-This-Lives.md",
                        "LIVING DOCUMENT"),
                       ("code/x/README.md", "INSTRUMENT README"),
                       ("docs/notes.md", None),
                       ("scratch/thing.md", None)]:
        ck("G: %-42s -> %-18s" % (path[-42:], want or "UNCLASSIFIED"),
           P5.classify(path) == want)

    # ------------------------------------------------- M: materialising
    print(file=OUT)
    print("M  READING A COMMIT WITHOUT TOUCHING THE TREE", file=OUT)
    tmp = tempfile.mkdtemp(prefix="st1d6c_m")
    try:
        head = U.git("rev-parse", "HEAD").strip()
        # M3 RESPECIFIED, and the reason is recorded rather than quietly fixed.
        # ITS FIRST FORM asserted that `git status --porcelain` mentioned nothing
        # outside this instrument's own directory -- which is not the property M3
        # claims to test.  It passed for two runs because the tree happened to be
        # clean everywhere else, and FAILED the moment this ticket added a file to
        # `docs/`: a check that reads a global property to test a local one is
        # vacuous exactly until something unrelated changes.  The form below takes
        # the status BEFORE and AFTER and compares them, which is the property.
        before = U.git("status", "--porcelain").strip()
        made = U.materialize(head, ["code/corpus_universe_1d6c/PREDICTIONS.md"], tmp)
        ok = made and os.path.isfile(
            os.path.join(tmp, "code/corpus_universe_1d6c/PREDICTIONS.md"))
        ck("M1 a blob is materialised at the path it has in the commit", bool(ok))
        ck("M2 an absent path is skipped and not invented",
           U.materialize(head, ["docs/does-not-exist-1d6c.md"], tmp) == [])
        after = U.git("status", "--porcelain").strip()
        ck("M3 materialising changes NOTHING in the working tree (before==after)",
           before == after)
        ck("M4 and the blob really landed OUTSIDE the repository",
           os.path.commonpath([tmp, U.ROOT]) != U.ROOT)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ------------------------------------------------- D: the diff machinery
    print(file=OUT)
    print("D  THE DIFF MACHINERY (p1)", file=OUT)
    a, b = U.diff_sets(["x", "y"], ["y", "z"])
    ck("D1 a difference is reported in both directions", a == ["x"] and b == ["z"])
    a, b = U.diff_sets(["x"], ["x"])
    ck("D2 no difference is reported where there is none", a == [] and b == [])

    print(file=OUT)
    U.rule(OUT)
    print("SUMMARY selftest1d6c: %d case(s), %d failing" % (N[0], len(BAD)),
          file=OUT)
    for nm in BAD:
        print("SUMMARY selftest1d6c: FAILED %s" % nm, file=OUT)
    U.rule(OUT)
    return 1 if BAD else 0


if __name__ == "__main__":
    sys.exit(main())
