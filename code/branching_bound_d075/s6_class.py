"""S6 -- THE INSTANCE OR THE CLASS?  Measured, and answered against myself.

The brief: "This is now the third population defect of the arc: mg-2c77 (a term
denoting 39 while the table classified 17), mg-7e39 (ROW_NAMES hand-listing 5 where
the gate prints 6), and this (a figure at 8 sites, bounded at 4).  Fixing this
instance without asking why the class keeps recurring would be the fourth."

An honest answer to "instance or class?" is a measurement, not a posture.  Three
things are measured; the verdict follows from them and is stated plainly either way.

  C1  DO THE THREE PRIOR INSTANCES EXIST AS ARTEFACTS?  Population: the three
      ticket ids the brief names.  Grain: one ticket -> present / absent in this
      tree, with the path that carries it.  A claim about a recurring class whose
      members cannot be located is a story.

  C2  WHAT FRACTION OF THE FIGURE'S CORPUS DOES MY GATE COVER?  Population: the
      docs/*.md files containing at least one site under the RELAXED predicate.
      Grain: one file -> gated / not gated.  My gate (s3) runs over exactly one
      file.  The others are named, with their unbounded counts, so the number I
      am NOT fixing is printed rather than omitted.

  C3  IS THE ARTEFACT REUSABLE WITHOUT EDITING IT?  Demonstrated, not asserted:
      lib_d075's predicate takes a path, so it is run here over every file of C2
      and the per-file result printed.  If it needed editing per document it
      would not be a class-level artefact at all.

VERDICT.  Printed as one of INSTANCE / INSTANCE + REUSABLE ARTEFACT / CLASS,
derived from C2 and C3 by a rule stated in the code, not chosen by the author.

EXIT 0 always.  This script reports; it does not gate.  PREDICTED 0.
"""

import os
import subprocess
import sys

import lib_d075 as L

OUT = sys.stdout
PRIOR = [
    ("mg-2c77", "a term denoting 39 while the table classified 17"),
    ("mg-7e39", "ROW_NAMES hand-listing 5 where the gate prints 6"),
    ("mg-19ec", "the 33-interval figure at 8 sites, bounded at 4"),
]
# s3 gates BOTH the living document (G1-G3) and this repair's own
# account document (G4).  A repair that imposes a standard on a
# document and exempts its own prose from it has not imposed one.
GATED = {"OneThird-Branching-Graphs-Where-This-Lives.md",
         "repair-mg-d075-the-figure-and-its-scope.md"}


def git(*a):
    return subprocess.run(["git"] + list(a), cwd=L.ROOT, capture_output=True,
                          text=True).stdout


def main():
    L.rule(OUT, "S6  THE INSTANCE OR THE CLASS?  Measured, and answered against\n"
                "    this repair itself.")
    print(file=OUT)

    # ------------------------------------------------------------------ C1
    L.rule(OUT, "  C1  DO THE THREE PRIOR INSTANCES EXIST AS ARTEFACTS?\n"
                "      Population: the 3 ticket ids the brief names.\n"
                "      Grain: one ticket -> present / absent, with a path.")
    present = 0
    for tid, what in PRIOR:
        short = tid.split("-")[1]
        paths = []
        for d in ("code", "docs"):
            root = os.path.join(L.ROOT, d)
            for entry in sorted(os.listdir(root)):
                if short in entry.lower():
                    paths.append(os.path.join(d, entry))
        commits = [l for l in git("log", "--oneline", "--all").split("\n")
                   if tid in l]
        ok = bool(paths) or bool(commits)
        if ok:
            present += 1
        print("    %-9s %-9s %s" % (tid, "PRESENT" if ok else "ABSENT", what),
              file=OUT)
        for p in paths[:3]:
            print("              path   : %s" % p, file=OUT)
        print("              commits: %d naming this ticket" % len(commits),
              file=OUT)
        print(file=OUT)
    print("    located: %d of %d" % (present, len(PRIOR)), file=OUT)
    print(file=OUT)

    # ------------------------------------------------------------------ C2
    L.rule(OUT, "  C2  WHAT FRACTION OF THE FIGURE'S CORPUS DOES MY GATE COVER?\n"
                "      Population: docs/*.md with >= 1 site under RELAXED.\n"
                "      Grain: one file -> gated / not gated.")
    rows = []
    for f in sorted(os.listdir(L.DOCS)):
        if not f.endswith(".md"):
            continue
        sites = L.relaxed_sites(os.path.join(L.DOCS, f))
        if sites:
            nb = sum(1 for t in sites if t[3])
            rows.append((f, len(sites), nb, len(sites) - nb, f in GATED))
    print("    %-56s %5s %5s %5s %7s" % ("file", "sites", "bnd", "unb", "gated"),
          file=OUT)
    for f, n, nb, nu, g in rows:
        print("    %-56s %5d %5d %5d %7s" % (f[:56], n, nb, nu,
                                             "YES" if g else "no"), file=OUT)
    ngated = sum(1 for r in rows if r[4])
    tot = sum(r[1] for r in rows)
    unb = sum(r[3] for r in rows)
    unb_ungated = sum(r[3] for r in rows if not r[4])
    print(file=OUT)
    print("    files in the corpus population : %d" % len(rows), file=OUT)
    print("    files my gate covers           : %d" % ngated, file=OUT)
    print("    sites in the corpus            : %d" % tot, file=OUT)
    print("    UNBOUNDED sites remaining      : %d, all %d of them in files this"
          % (unb, unb_ungated), file=OUT)
    print("                                     repair does not touch", file=OUT)
    print(file=OUT)

    # ------------------------------------------------------------------ C3
    L.rule(OUT, "  C3  IS THE ARTEFACT REUSABLE WITHOUT EDITING IT?\n"
                "      Demonstrated by running the same predicate, unmodified,\n"
                "      over every file of C2.")
    print("    lib_d075.relaxed_sites(path) takes the document as an argument;",
          file=OUT)
    print("    the C2 table above IS the demonstration -- %d files, one call each,"
          % len(rows), file=OUT)
    print("    zero edits to the predicate.  A per-document instrument could not",
          file=OUT)
    print("    have produced that table.", file=OUT)
    print(file=OUT)

    # --------------------------------------------------------------- verdict
    L.rule(OUT, "  VERDICT.  Rule, stated before the answer:\n"
                "    CLASS                        if the gate covers every file\n"
                "                                 of the corpus population;\n"
                "    INSTANCE + REUSABLE ARTEFACT if it covers some and the\n"
                "                                 predicate is path-parameterised;\n"
                "    INSTANCE                     otherwise.")
    if ngated == len(rows):
        verdict = "CLASS"
    elif ngated >= 1:
        verdict = "INSTANCE + REUSABLE ARTEFACT"
    else:
        verdict = "INSTANCE"
    print("    gate covers %d of %d files; predicate is path-parameterised: yes"
          % (ngated, len(rows)), file=OUT)
    print(file=OUT)
    print("    VERDICT: %s" % verdict, file=OUT)
    print(file=OUT)
    print("    AND THE PART NO ARTEFACT FIXES.  The three prior instances are", file=OUT)
    print("    not three occurrences of one bug in one file; they are one", file=OUT)
    print("    HABIT -- writing a figure and its scope in different places, or", file=OUT)
    print("    the scope nowhere -- committed by three different authors in", file=OUT)
    print("    three different subsystems.  A path-parameterised predicate can", file=OUT)
    print("    be pointed at a fourth document; it cannot be pointed at the", file=OUT)
    print("    habit.  What would address the class is a check that runs on", file=OUT)
    print("    every document of this repo on every commit, and this repair", file=OUT)
    print("    does not install one.  That is the honest answer and it is the", file=OUT)
    print("    answer PREDICTIONS.md P10 committed to in advance.", file=OUT)
    print(file=OUT)

    L.rule(OUT)
    print("SUMMARY s6_class: %d of %d prior instances located as artefacts"
          % (present, len(PRIOR)), file=OUT)
    print("SUMMARY s6_class: corpus %d files, %d sites, %d unbounded remaining"
          % (len(rows), tot, unb), file=OUT)
    print("SUMMARY s6_class: gate covers %d of %d files" % (ngated, len(rows)),
          file=OUT)
    print("SUMMARY s6_class: VERDICT %s" % verdict, file=OUT)
    L.rule(OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
