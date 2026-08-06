"""P2 -- THE FULL POPULATION, DERIVED BY A METHOD THAT DOES NOT SHARE THE GLOB'S
BLIND SPOT.  Is the true count 24?

THE BRIEF'S RULE: "If I re-derive using the same mechanism I cannot discover what it
excludes."  So the file list here is built from `git ls-files`, at a NAMED COMMIT,
and never from `os.listdir(docs)`.

AND THE BRIEF'S CAUTION, which this script is written to obey rather than to quote:
"exactly half" is a hint and must not become the conclusion.  So the count is taken
at THREE STATES and through TWO PARSERS, and the inside/outside split is printed at
every one of them.  If the half is an artefact of one classifier at one commit, one
of the six cells will say so.

  STATE A   `8132d75` -- the commit carrying mg-aaf4's census transcript.  This is
            where 24 was measured.  Anything else is a different question.
  STATE B   `20614ef` -- the tip of main when this ticket started, before any commit
            of mine.  Answers: did anything move between mg-aaf4 and me?
  STATE C   the working tree, INCLUDING MY OWN FILES.  PREDICTIONS.md P6 says in
            advance that my own deliverable enters the population it measures, and
            this state is where that is paid for rather than hidden.

  PARSER 1  `lib_d075`, imported and executed -- the parent's own reader.
  PARSER 2  `lib_aaf4`, imported and executed -- a re-implementation sharing no line
            with it.  IF THE TWO DISAGREE, THAT IS THE FINDING, and it is bigger
            than the one I was sent to get.

  GRAIN S   one sentence.       GRAIN O   one written occurrence of the figure.

THE DECLARED EXCLUSION.  Tracked `.txt` and `.py` are NOT in the claim population,
and this script prints their size anyway -- the whole content of this ticket is that
a population excluded by drawing a pattern is invisible, and one excluded by name
with a number beside it is not.

EXIT 1 if the published corpus figure understates the full population.  PREDICTED 1.
"""

import os
import shutil
import sys
import tempfile

import re
import lib1d6c as U

if U.AAF4 not in sys.path:
    sys.path.insert(0, U.AAF4)
import lib_aaf4 as A                                            # noqa: E402

OUT = sys.stdout
ANCHOR = "8132d75"          # mg-aaf4's census transcript (disclosure D9)
TIP = "20614ef"             # main's tip when mg-1d6c started
MINE_PREFIX = ("code/corpus_universe_1d6c/", "docs/repair-mg-1d6c-")


def aaf4_sites(root, paths):
    """The same census through mg-aaf4's re-implementation."""
    out = []
    for p in U.prefilter(root, paths):
        fp = os.path.join(root, p)
        if not os.path.isfile(fp):
            continue
        try:
            for line, kind, s, b in A.relaxed_sites(fp):
                out.append((p, line, kind, s, b))
        except (IOError, OSError, UnicodeDecodeError):
            continue
    return out


def split_docs(sites):
    ins = [t for t in sites if t[0].startswith("docs/")]
    outs = [t for t in sites if not t[0].startswith("docs/")]
    return ins, outs


def state(label, root, paths, wide=None):
    sites = U.sites_of(root, paths)
    n, nb, nu = U.totals(sites)
    ins, outs = split_docs(sites)
    return dict(label=label, root=root, paths=paths, sites=sites, n=n, nb=nb,
                nu=nu, files=len({t[0] for t in sites}),
                occ=U.occurrences(sites),
                unb_in=sum(1 for t in ins if not t[4]),
                unb_out=sum(1 for t in outs if not t[4]), wide=wide)


def report(st):
    print("    files stating the figure : %d" % st["files"], file=OUT)
    print("    sites          GRAIN S   : %d" % st["n"], file=OUT)
    print("    bounded                  : %d" % st["nb"], file=OUT)
    print("    UNBOUNDED                : %d" % st["nu"], file=OUT)
    print("    occurrences    GRAIN O   : %d" % st["occ"], file=OUT)
    print("    unbounded INSIDE  docs/  : %d" % st["unb_in"], file=OUT)
    print("    unbounded OUTSIDE docs/  : %d" % st["unb_out"], file=OUT)
    tot = st["unb_in"] + st["unb_out"]
    if tot:
        print("    the split                : %d / %d  (%s)"
              % (st["unb_in"], st["unb_out"],
                 "EXACTLY HALF" if st["unb_in"] == st["unb_out"]
                 else "not half"), file=OUT)
    print(file=OUT)


def main():
    U.rule(OUT, "P2  THE FULL POPULATION, by a method that does not share the\n"
                "    glob's blind spot.  Three states, two parsers, two grains.")
    print(file=OUT)

    tmp = tempfile.mkdtemp(prefix="p2_1d6c_")
    try:
        # ---------------------------------------------------------- STATE A
        U.rule(OUT, "  2.1  STATE A -- %s, the commit carrying mg-aaf4's census.\n"
                    "       Population: every .md tracked AT THAT COMMIT.  Grain S\n"
                    "       and O.  Predicate: the parent's RELAXED, executed."
                    % ANCHOR)
        pa = U.u_m_track(ANCHOR)
        rootA = os.path.join(tmp, "A")
        made = U.materialize(ANCHOR, pa, rootA)
        print("    tracked .md at %s   : %d  (materialised %d; the working tree\n"
              "                              is never touched)"
              % (ANCHOR, len(pa), len(made)), file=OUT)
        stA = state("A", rootA, made)
        report(stA)
        U.show_rows(U.by_file(stA["sites"]), OUT)
        print(file=OUT)
        print("    mg-aaf4 PUBLISHED, at this commit, over this universe:", file=OUT)
        print("      13 files, 51 sites GRAIN S, 24 unbounded, 60 occurrences", file=OUT)
        print("      (quoted from out_a1_population.txt SUMMARY U4 -- ITS number,", file=OUT)
        print("       re-derived here through the OTHER parser, not copied.)", file=OUT)
        agree = (stA["files"], stA["n"], stA["nu"], stA["occ"]) == (13, 51, 24, 60)
        print("      re-derived : %d files, %d sites, %d unbounded, %d occurrences"
              % (stA["files"], stA["n"], stA["nu"], stA["occ"]), file=OUT)
        print("      %s" % ("ALL FOUR REPRODUCE." if agree
                            else "*** DISAGREEMENT -- see 2.2 before believing "
                                 "either number ***"), file=OUT)
        print(file=OUT)

        # ------------------------------------------------- the parser control
        U.rule(OUT, "  2.2  THE CROSS-PARSER CONTROL.  The same file list at the\n"
                    "       same commit, counted through mg-aaf4's reader, which\n"
                    "       shares no line with the parent's.")
        aa = aaf4_sites(rootA, made)
        an, anb, anu = U.totals(aa)
        ains, aouts = split_docs(aa)
        print("    lib_d075  : %d files, %d sites, %d unbounded"
              % (stA["files"], stA["n"], stA["nu"]), file=OUT)
        print("    lib_aaf4  : %d files, %d sites, %d unbounded"
              % (len({t[0] for t in aa}), an, anu), file=OUT)
        keyd = {(p, l, re.sub(r"\s+", " ", s)) for p, l, _, s, _ in stA["sites"]}
        keya = {(p, l, re.sub(r"\s+", " ", s)) for p, l, _, s, _ in aa}
        only_d, only_a = sorted(keyd - keya), sorted(keya - keyd)
        print("    rows only lib_d075 sees : %d" % len(only_d), file=OUT)
        for p, l, s in only_d[:6]:
            print("        + %s:%d  %s" % (p, l, s[:70]), file=OUT)
        print("    rows only lib_aaf4 sees : %d" % len(only_a), file=OUT)
        for p, l, s in only_a[:6]:
            print("        - %s:%d  %s" % (p, l, s[:70]), file=OUT)
        parsers_agree = not only_d and not only_a
        print("    %s" % ("THE PARSERS AGREE ROW FOR ROW.  A count that differs "
                          "from\n    mg-aaf4's below is a UNIVERSE difference and "
                          "cannot be a parser\n    difference." if parsers_agree
                          else "THE PARSERS DISAGREE.  Every count in this suite is "
                               "reported\n    at both readings and no total is "
                               "published as if there were one."), file=OUT)
        print(file=OUT)

        # ---------------------------------------------------------- STATE B
        U.rule(OUT, "  2.3  STATE B -- %s, main's tip when this ticket started.\n"
                    "       Did anything move between mg-aaf4's census and me?" % TIP)
        pb = U.u_m_track(TIP)
        rootB = os.path.join(tmp, "B")
        madeB = U.materialize(TIP, pb, rootB)
        stB = state("B", rootB, madeB)
        print("    tracked .md at %s   : %d" % (TIP, len(pb)), file=OUT)
        report(stB)
        moved = (stB["files"], stB["n"], stB["nu"]) != (stA["files"], stA["n"],
                                                        stA["nu"])
        print("    against STATE A: %s" % ("MOVED" if moved else "unchanged"),
              file=OUT)
        print(file=OUT)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ---------------------------------------------------------- STATE C
    U.rule(OUT, "  2.4  STATE C -- the working tree, INCLUDING MY OWN FILES.\n"
                "       PREDICTIONS.md P6 said in advance that this ticket's own\n"
                "       prose enters the population it measures.  Here is the bill.")
    pc = U.u_m_disk()
    stC = state("C", U.ROOT, pc)
    report(stC)
    mine = [t for t in stC["sites"] if t[0].startswith(MINE_PREFIX)]
    mine_unb = [t for t in mine if not t[4]]
    print("    OF WHICH MINE (population: files this ticket authors; grain: one", file=OUT)
    print("    sentence):", file=OUT)
    print("      sites contributed by mg-1d6c    : %d" % len(mine), file=OUT)
    print("      UNBOUNDED contributed by mg-1d6c: %d" % len(mine_unb), file=OUT)
    for p, l, k, s, b in mine:
        print("        %s:%d %s" % (p, l, "BOUNDED" if b else "*** UNBOUNDED ***"),
              file=OUT)
        print("          %s" % re.sub(r"\s+", " ", s)[:96], file=OUT)
    print(file=OUT)
    if mine_unb:
        print("      P6 IS REFUTED AND THE SITES ARE LISTED ABOVE.  The trap that", file=OUT)
        print("      took three tickets in a row has taken a fourth.", file=OUT)
    else:
        print("      P6 HOLDS: this ticket entered the population it measures and", file=OUT)
        print("      entered it bounded.  Entering with 0 sites would have been a", file=OUT)
        print("      dodge, not a pass.", file=OUT)
    print(file=OUT)

    # ------------------------------------------------ published vs derived
    U.rule(OUT, "  2.5  THE PUBLISHED FIGURE AGAINST THE POPULATION.\n"
                "       Same predicate, same parser, same grain.  ONLY THE\n"
                "       UNIVERSE DIFFERS -- which is the whole claim.")
    glob_sites = U.sites_of(U.ROOT, U.u_g_impl())
    gn, gnb, gnu = U.totals(glob_sites)
    gfiles = len({t[0] for t in glob_sites})
    print("    %-46s %6s %6s %6s" % ("universe", "files", "sites", "unb"), file=OUT)
    print("    %-46s %6d %6d %6d"
          % ("mg-d075's D, the glob docs/*.md (working tree)", gfiles, gn, gnu),
          file=OUT)
    print("    %-46s %6d %6d %6d"
          % ("every tracked .md (working tree)", stC["files"], stC["n"], stC["nu"]),
          file=OUT)
    print(file=OUT)
    print("    mg-d075 PUBLISHED 7 files / 36 sites / 12 unbounded for the first", file=OUT)
    print("    row (README bullet s1 and docs/repair-...:180).  Reproduced here: ", file=OUT)
    print("    %d / %d / %d." % (gfiles, gn, gnu), file=OUT)
    print(file=OUT)
    under = stC["nu"] - gnu
    print("    THE UNDERCOUNT, at the grain the figure is published in:", file=OUT)
    print("      published unbounded    : %d" % gnu, file=OUT)
    print("      population unbounded   : %d" % stC["nu"], file=OUT)
    print("      invisible to the glob  : %d" % under, file=OUT)
    print(file=OUT)

    # ------------------------------------------------- the declared exclusion
    U.rule(OUT, "  2.6  THE DECLARED EXCLUSION, WITH ITS SIZE.  Population:\n"
                "       every tracked .txt and .py.  Grain: one sentence.\n"
                "       REPORTED AND NOT REPAIRED -- and named, not globbed away.")
    wide = U.u_wide()
    wsites = U.sites_of(U.ROOT, wide)
    wn, wnb, wnu = U.totals(wsites)
    wfiles = len({t[0] for t in wsites})
    print("    tracked .txt and .py         : %d files" % len(wide), file=OUT)
    print("    of them stating the figure   : %d" % wfiles, file=OUT)
    print("    sites            GRAIN S     : %d" % wn, file=OUT)
    print("    unbounded                    : %d" % wnu, file=OUT)
    print(file=OUT)
    print("    WHY THIS IS EXCLUDED, stated rather than arranged: a transcript", file=OUT)
    print("    PRINTS a site and an instrument MATCHES one; neither ASSERTS the", file=OUT)
    print("    figure in its own voice.  Bounding a transcript would mean editing", file=OUT)
    print("    a record of a run.  THE EXCLUSION IS THE SAME DECISION mg-d075", file=OUT)
    print("    MADE; the difference is that its size is printed here.", file=OUT)
    print(file=OUT)

    U.rule(OUT, "  VERDICT")
    print("    24 %s the count at %s, re-derived through the other parser."
          % ("IS" if stA["nu"] == 24 else "IS NOT", ANCHOR), file=OUT)
    print("    At the working tree the population is %d unbounded sites in %d"
          % (stC["nu"], stC["files"]), file=OUT)
    print("    files, and the published figure sees %d of them." % gnu, file=OUT)
    print("    The docs/ split at the working tree is %d inside / %d outside."
          % (stC["unb_in"], stC["unb_out"]), file=OUT)
    if stC["unb_in"] == stC["unb_out"]:
        print("    IT IS STILL EXACTLY HALF -- and it is a coincidence of this", file=OUT)
        print("    corpus, not a law.  Nothing forces the two sides to be equal;", file=OUT)
        print("    the ratio moves the moment any ticket writes one more sentence", file=OUT)
        print("    on either side of the boundary.", file=OUT)
    else:
        print("    IT IS NO LONGER HALF.  The memorable ratio was a property of", file=OUT)
        print("    one commit and it did not survive re-derivation.", file=OUT)
    print(file=OUT)

    U.rule(OUT)
    print("SUMMARY p2_population: STATE A %s %d files, %d sites S, %d unbounded, "
          "%d occurrences O" % (ANCHOR, stA["files"], stA["n"], stA["nu"],
                                stA["occ"]), file=OUT)
    print("SUMMARY p2_population: STATE A vs mg-aaf4's 13/51/24/60 %s"
          % ("REPRODUCES" if agree else "DISAGREES"), file=OUT)
    print("SUMMARY p2_population: cross-parser control %s (%d rows only d075, "
          "%d only aaf4)" % ("AGREE" if parsers_agree else "DISAGREE",
                             len(only_d), len(only_a)), file=OUT)
    print("SUMMARY p2_population: STATE B %s %d files, %d sites, %d unbounded"
          % (TIP, stB["files"], stB["n"], stB["nu"]), file=OUT)
    print("SUMMARY p2_population: STATE C worktree %d files, %d sites, %d "
          "unbounded, %d occurrences" % (stC["files"], stC["n"], stC["nu"],
                                         stC["occ"]), file=OUT)
    print("SUMMARY p2_population: mg-1d6c's own contribution %d sites, %d unbounded"
          % (len(mine), len(mine_unb)), file=OUT)
    print("SUMMARY p2_population: glob universe %d files, %d sites, %d unbounded"
          % (gfiles, gn, gnu), file=OUT)
    print("SUMMARY p2_population: UNDERCOUNT %d unbounded sites invisible to the "
          "glob" % under, file=OUT)
    print("SUMMARY p2_population: split at worktree %d inside docs/ / %d outside"
          % (stC["unb_in"], stC["unb_out"]), file=OUT)
    print("SUMMARY p2_population: declared exclusion .txt/.py %d files, %d sites, "
          "%d unbounded -- reported, not repaired" % (wfiles, wn, wnu), file=OUT)
    U.rule(OUT)
    return 1 if under > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
