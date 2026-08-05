"""S1 -- I COUNT THE SITES MYSELF.  Is EIGHT the population?

The brief for this repair says: count the sites yourself rather than inheriting the
figure.  The pre-filed audit mg-aaf4 is told not to take 8 from me either.  So this
script does not consume the number 8 from anywhere -- it derives a count, prints
every site it counted, and compares.

FOUR POPULATIONS, EACH NAMED AT THE POINT IT IS COUNTED.  A bare total is the defect
this arc keeps catching, so no total below appears without the population it is over
and the grain of the value.

  A  STRICT / one document.  Live sentences of
     docs/OneThird-Branching-Graphs-Where-This-Lives.md matching the parent's POP-3
     predicate: the SENTENCE contains 33 and the SENTENCE names Young-Fibonacci.
     Grain: one sentence.  Value: a count of sentences.
     This is the parent's population.  Its published value is 8 / 4 bounded.

  B  RELAXED / one document.  Same file, same liveness, same grain.  One clause
     relaxed: Young-Fibonacci may be named by the sentence OR BY THE TABLE CELL OR
     PARAGRAPH THE SENTENCE SITS IN.  Nothing else differs.

  C  ALL SENTENCES / one document.  Same file, RELAXED predicate, liveness DROPPED
     -- struck and block-quoted units admitted.  This is the ceiling: every place in
     the file where the figure is written down at all.  It is reported so that the
     liveness rule cannot be mistaken for the reason a number is small.

  D  RELAXED / the whole docs corpus.  Live sentences of every docs/*.md.  Reported,
     NOT repaired -- see the README's scope section and P5.

EXIT 1 if population B is not 8, i.e. if EIGHT IS NOT THE POPULATION.  PREDICTED 1.
"""

import os
import re
import subprocess
import sys

import lib_d075 as L

OUT = sys.stdout
ITEM = "mg-d075"
# The docs/*.md this repair itself authors.  Excluded from the PRE-REPAIR corpus.
MINE_DOCS = {"repair-mg-d075-the-figure-and-its-scope.md"}
RELPATH = "docs/OneThird-Branching-Graphs-Where-This-Lives.md"


def git(*a):
    return subprocess.run(["git"] + list(a), cwd=L.ROOT, capture_output=True,
                          text=True).stdout


def prerepair_doc():
    """The document as it stood before this repair, read out of git.

    THE COUNTS THAT ANSWER THE BRIEF ARE PRE-REPAIR COUNTS.  "8 sites, 4
    unbounded" is a measurement of a commit; so is the 9 that refutes it.
    Measuring the repaired tree and calling the result a refutation of mg-19ec
    would be measuring my own edits.  Both states are printed below.
    """
    for row in git("log", "--format=%H\t%s", "--", RELPATH).strip().split("\n"):
        h, _, subj = row.partition("\t")
        if ITEM not in subj:
            break
    tmp = os.path.join(L.HERE, ".prerepair_s1.md")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(git("show", "%s:%s" % (h, RELPATH)))
    return tmp, h, subj


def four(docpath, at=None):
    """(A, B, C, Dtotal, Dbounded, Drows) for one state of the document.

    `at` is a commit.  When given, the CORPUS population D excludes every
    docs/*.md that did NOT exist at that commit, i.e. the documents THIS repair
    adds -- otherwise a "pre-repair" corpus count silently includes this repair's
    own prose, which is a population error of exactly the kind being repaired,
    committed inside the repair.

    NOTE ON WHAT THE EXCLUSION IS AND IS NOT.  The other five files of the corpus
    are untouched by this repair, so they are read AS THEY STAND; only the living
    document is rolled back, and only this repair's own new documents are removed.
    A stricter reading -- the corpus exactly as it was at the anchor -- would also
    drop mg-19ec's own audit document, which post-dates the anchor by one ticket,
    and would answer a question nobody asked.  The count of docs/*.md that
    post-date the anchor is printed so the difference is visible rather than
    buried.
    """
    A = L.strict_sites(docpath)
    B = L.relaxed_sites(docpath)
    C = []
    for start, kind, body in L.units(docpath):
        text = L.unit_text(body)
        for sent in L.sentences(text):
            if L.FIG.search(sent) and (L.YF.search(sent) or L.YF.search(text)):
                C.append((start, kind, sent, bool(L.RANK6.search(sent))))
    names = sorted(x for x in os.listdir(L.DOCS) if x.endswith(".md"))
    if at:
        names = [x for x in names if x not in MINE_DOCS]
    rows, tot, totb = [], 0, 0
    for f in names:
        path = docpath if f == os.path.basename(L.DOC) else os.path.join(L.DOCS, f)
        sites = L.relaxed_sites(path)
        if sites:
            nb = sum(1 for t in sites if t[3])
            rows.append((f, len(sites), nb, len(sites) - nb))
            tot += len(sites)
            totb += nb
    return A, B, C, tot, totb, rows


def table(label, A, B, C, tot, totb, rows):
    print("    %-14s %-8s %8s %8s %10s" % (label, "sites", "bounded",
                                           "unbnd", "note"), file=OUT)
    print("    %-14s %-8d %8d %8d %10s"
          % ("A STRICT", len(A), sum(1 for t in A if t[3]),
             sum(1 for t in A if not t[3]), "one doc"), file=OUT)
    print("    %-14s %-8d %8d %8d %10s"
          % ("B RELAXED", len(B), sum(1 for t in B if t[3]),
             sum(1 for t in B if not t[3]), "one doc"), file=OUT)
    print("    %-14s %-8d %8d %8d %10s"
          % ("C ceiling", len(C), sum(1 for t in C if t[3]),
             sum(1 for t in C if not t[3]), "incl struck"), file=OUT)
    print("    %-14s %-8d %8d %8d %10s"
          % ("D corpus", tot, totb, tot - totb, "%d files" % len(rows)), file=OUT)
    print(file=OUT)


def main():
    L.rule(OUT, "S1  mg-d075: I count the sites myself.  Is EIGHT the population?")
    print(file=OUT)

    PRE, anch, subj = prerepair_doc()
    L.rule(OUT, "  PRE-REPAIR AND AS-IT-STANDS, side by side.  The counts that\n"
                "  answer the brief are the PRE-REPAIR ones: mg-19ec's 8 is a\n"
                "  measurement of a commit, and so is the number that refutes it.")
    print("    anchor commit : %s" % (anch or "")[:40], file=OUT)
    print("    anchor subject: %s" % (subj or "")[:96], file=OUT)
    print(file=OUT)
    pre = four(PRE, at=anch)
    now = four(L.DOC)
    tree = [x for x in git("ls-tree", "--name-only", anch, "docs/").split("\n")
            if x.endswith(".md")]
    ndocs_now = [x for x in os.listdir(L.DOCS) if x.endswith(".md")]
    print("  PRE-REPAIR  (living document rolled back to the anchor; the other", file=OUT)
    print("               corpus files read as they stand; this repair's own %d"
          % len(MINE_DOCS), file=OUT)
    print("               new docs/*.md excluded.  %d docs/*.md exist now, %d at"
          % (len(ndocs_now), len(tree)), file=OUT)
    print("               the anchor, so %d post-date it -- among them mg-19ec's"
          % (len(ndocs_now) - len(tree)), file=OUT)
    print("               own audit document.)", file=OUT)
    table("population", *pre)
    print("  AS IT STANDS", file=OUT)
    table("population", *now)
    print("  THE PRE-REPAIR SITES OF POPULATION B, ALL %d, IN FULL:" % len(pre[1]),
          file=OUT)
    print(file=OUT)
    L.show_sites(pre[1], OUT)
    prekeyA = {(a, re.sub(r"\s+", " ", x)) for a, _, x, _ in pre[0]}
    preextra = [t for t in pre[1]
                if (t[0], re.sub(r"\s+", " ", t[2])) not in prekeyA]
    print("  PRE-REPAIR B \\ A -- the site(s) mg-19ec's predicate cannot see: %d"
          % len(preextra), file=OUT)
    print(file=OUT)
    L.show_sites(preextra, OUT)
    os.remove(PRE)

    us = L.units(L.DOC)
    live = list(L.live_sentences(L.DOC))
    nlive_units = len({(a, b) for a, b, _, _ in live})
    print("  THE UNIVERSE, NAMED", file=OUT)
    print("    document              : %s" % os.path.basename(L.DOC), file=OUT)
    print("    claim sites parsed    : %d" % len(us), file=OUT)
    print("    LIVE sites            : %d" % nlive_units, file=OUT)
    print("    LIVE sentences        : %d" % len(live), file=OUT)
    print(file=OUT)

    A = L.strict_sites(L.DOC)
    B = L.relaxed_sites(L.DOC)

    L.rule(OUT, "  A  STRICT predicate, one document -- the parent's population.\n"
                "     grain: sentences.  value: a count of sentences.")
    print("    population : %d live sentences state the figure 33 about" % len(A),
          file=OUT)
    print("                 Young-Fibonacci intervals, NAMING IT IN THE SENTENCE",
          file=OUT)
    print("    bounded    : %d carry a rank scope in the same sentence"
          % sum(1 for t in A if t[3]), file=OUT)
    print("    unbounded  : %d do not" % sum(1 for t in A if not t[3]), file=OUT)
    print(file=OUT)
    L.show_sites(A, OUT)

    L.rule(OUT, "  B  RELAXED predicate, one document -- attribution may come from\n"
                "     the CELL or PARAGRAPH.  grain: sentences.")
    print("    population : %d live sentences state the figure 33 about" % len(B),
          file=OUT)
    print("                 Young-Fibonacci intervals", file=OUT)
    print("    bounded    : %d carry a rank scope in the same sentence"
          % sum(1 for t in B if t[3]), file=OUT)
    print("    unbounded  : %d do not" % sum(1 for t in B if not t[3]), file=OUT)
    print(file=OUT)
    L.show_sites(B, OUT)

    # ---- what B has that A does not, printed as sites, not as a delta ------
    keyA = {(a, re.sub(r"\s+", " ", s)) for a, _, s, _ in A}
    extra = [t for t in B if (t[0], re.sub(r"\s+", " ", t[2])) not in keyA]
    L.rule(OUT, "  B \\ A  -- THE SITES THE PARENT'S PREDICATE CANNOT SEE")
    print("    count : %d live sentence(s) state the figure about Young-Fibonacci"
          % len(extra), file=OUT)
    print("            intervals WITHOUT spelling the name in the same sentence",
          file=OUT)
    print(file=OUT)
    L.show_sites(extra, OUT)
    for line, kind, s, b in extra:
        print("    line %d: the unit that supplies the attribution is a %s;"
              % (line, kind), file=OUT)
        print("    the sentence itself says \"for Young's\", not \"Young-Fibonacci\","
              , file=OUT)
        print("    so the parent's same-sentence clause drops it.", file=OUT)
        print(file=OUT)

    # ---- C: the ceiling ---------------------------------------------------
    allsent = []
    for start, kind, body in us:
        text = L.unit_text(body)
        for s in L.sentences(text):
            if L.FIG.search(s) and (L.YF.search(s) or L.YF.search(text)):
                allsent.append((start, kind, s, bool(L.RANK6.search(s))))
    L.rule(OUT, "  C  RELAXED predicate, LIVENESS DROPPED -- the ceiling")
    print("    population : %d sentences (live + struck + block-quoted) state the"
          % len(allsent), file=OUT)
    print("                 figure about Young-Fibonacci intervals", file=OUT)
    print("    bounded    : %d" % sum(1 for t in allsent if t[3]), file=OUT)
    print("    unbounded  : %d" % sum(1 for t in allsent if not t[3]), file=OUT)
    print("    live       : %d of %d -- the liveness rule removes %d"
          % (len(B), len(allsent), len(allsent) - len(B)), file=OUT)
    print(file=OUT)

    # ---- D: the corpus ----------------------------------------------------
    L.rule(OUT, "  D  RELAXED predicate, THE WHOLE docs/ CORPUS -- reported, and\n"
                "     NOT repaired.  Historical audit documents are dated records.")
    files = sorted(f for f in os.listdir(L.DOCS) if f.endswith(".md"))
    tot = totb = 0
    rows = []
    for f in files:
        sites = L.relaxed_sites(os.path.join(L.DOCS, f))
        if not sites:
            continue
        nb = sum(1 for t in sites if t[3])
        rows.append((f, len(sites), nb, len(sites) - nb))
        tot += len(sites)
        totb += nb
    print("    files scanned         : %d markdown files in docs/" % len(files),
          file=OUT)
    print("    files stating figure  : %d" % len(rows), file=OUT)
    print("    population            : %d live sentences state the 33-interval"
          % tot, file=OUT)
    print("                            figure about Young-Fibonacci intervals",
          file=OUT)
    print("    bounded               : %d" % totb, file=OUT)
    print("    unbounded             : %d  (%.0f%% of the corpus population)"
          % (tot - totb, 100.0 * (tot - totb) / tot if tot else 0), file=OUT)
    print(file=OUT)
    print("    %-62s %5s %5s %5s" % ("file", "sites", "bnd", "unb"), file=OUT)
    for f, n, nb, nu in rows:
        print("    %-62s %5d %5d %5d" % (f[:62], n, nb, nu), file=OUT)
    print(file=OUT)
    print("    THE REPAIR POPULATION IS ONE FILE OF THESE %d.  The other %d are"
          % (len(rows), len(rows) - 1), file=OUT)
    print("    audit and repair records written by earlier tickets and dated by",
          file=OUT)
    print("    their commits; editing them would destroy the evidence trail this",
          file=OUT)
    print("    arc runs on.  The number above is a REPORT, not a backlog I am", file=OUT)
    print("    silently declining -- see README section 'what I did not repair'.",
          file=OUT)
    print(file=OUT)

    L.rule(OUT)
    print("SUMMARY s1_census: universe %d live sentences in %d live sites of %s"
          % (len(live), nlive_units, os.path.basename(L.DOC)), file=OUT)
    print("SUMMARY s1_census: A strict/one-doc %d sites, %d bounded, %d unbounded"
          % (len(A), sum(1 for t in A if t[3]), sum(1 for t in A if not t[3])),
          file=OUT)
    print("SUMMARY s1_census: B relaxed/one-doc %d sites, %d bounded, %d unbounded"
          % (len(B), sum(1 for t in B if t[3]), sum(1 for t in B if not t[3])),
          file=OUT)
    print("SUMMARY s1_census: B\\A %d site(s) the parent's predicate cannot see"
          % len(extra), file=OUT)
    print("SUMMARY s1_census: C ceiling/one-doc %d sentences incl. struck"
          % len(allsent), file=OUT)
    print("SUMMARY s1_census: D corpus %d sites in %d files, %d unbounded"
          % (tot, len(rows), tot - totb), file=OUT)
    print("SUMMARY s1_census: PRE-REPAIR A %d sites, %d unbounded; B %d sites, "
          "%d unbounded" % (len(pre[0]), sum(1 for t in pre[0] if not t[3]),
                            len(pre[1]), sum(1 for t in pre[1] if not t[3])),
          file=OUT)
    print("SUMMARY s1_census: PRE-REPAIR D corpus %d sites, %d unbounded"
          % (pre[3], pre[3] - pre[4]), file=OUT)
    print("SUMMARY s1_census: EIGHT IS%s THE POPULATION of B (pre-repair B = %d)"
          % ("" if len(pre[1]) == 8 else " NOT", len(pre[1])), file=OUT)
    L.rule(OUT)
    return 1 if len(pre[1]) != 8 else 0


if __name__ == "__main__":
    sys.exit(main())
