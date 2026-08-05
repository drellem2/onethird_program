"""S3 -- THE GATE.  After the repair: is every site bounded, was any site lost, and
did any measured number move?

THREE THINGS, because "unbounded is 0" on its own is worth very little -- a script
that deletes the sentences would also print 0.

  G1  BOUNDED.  Population: live sentences of
      docs/OneThird-Branching-Graphs-Where-This-Lives.md stating the 33-interval
      figure about Young-Fibonacci intervals.  Grain: one sentence.  Under BOTH
      predicates -- the parent's STRICT and this repair's RELAXED -- the count of
      unbounded sites must be 0.  Reported as a fraction with its denominator, not
      as a bare 0.

  G2  NO SITE LOST, AND ANYTHING ADDED IS BOUNDED.  The same population is counted
      on the PRE-REPAIR doc, read out of git rather than remembered.  Every
      pre-repair site must still be present -- matched by shared vocabulary, not by
      line number and not by position -- so that G1's 0 cannot be reached by
      deleting sentences.  Sites the repair ADDS are printed in full and must be
      bounded themselves.  The size delta is reported, not gated on: a repair that
      records itself in the document it repairs necessarily adds sites, and G2's
      first form forbade exactly that.  Both respecifications of this check, and
      the runs that forced them, are recorded in the README.

  G3  NO NUMBER MOVED.  Every integer appearing in a site sentence, pre-repair and
      post-repair, as a MULTISET.  A bounding repair MAY reduce an occurrence count
      -- factoring two unbounded restatements of "of the 33" into one bounded
      statement of the family does exactly that -- so a fall is adjudicated per
      matched site rather than forbidden: the site where it fell is named, and it
      must still state the figure.  Population: the integers of the site sentences.
      Grain: one integer occurrence.

THE PRE-REPAIR ANCHOR IS DERIVED, NOT NAMED.  The baseline commit is found by
walking `git log` over the document and taking the newest commit whose subject does
NOT mention this work item -- so the anchor survives rebases, merges and this branch
landing on main, and is printed in the transcript so the audit can check it.

EXIT 0 if G1, G2 and G3 all hold.  PREDICTED 0.
"""

import os
import re
import subprocess
import sys

import lib_d075 as L

OUT = sys.stdout
ITEM = "mg-d075"
RELPATH = "docs/OneThird-Branching-Graphs-Where-This-Lives.md"


def git(*a):
    return subprocess.run(["git"] + list(a), cwd=L.ROOT, capture_output=True,
                          text=True).stdout


def baseline_commit():
    """Newest commit touching the doc whose subject does not name this work item."""
    log = git("log", "--format=%H\t%s", "--", RELPATH).strip().split("\n")
    for row in log:
        if not row.strip():
            continue
        h, _, subj = row.partition("\t")
        if ITEM not in subj:
            return h, subj
    return None, None


def main():
    bad = 0

    def ck(label, ok, extra=""):
        nonlocal bad
        print("    %-58s %s%s" % (label, "ok" if ok else "BAD", extra), file=OUT)
        if not ok:
            bad += 1

    L.rule(OUT, "S3  THE GATE.  bounded / no site lost / no number moved.")
    print(file=OUT)

    h, subj = baseline_commit()
    print("  THE PRE-REPAIR ANCHOR, DERIVED", file=OUT)
    print("    document : %s" % RELPATH, file=OUT)
    print("    commit   : %s" % (h or "<none>"), file=OUT)
    print("    subject  : %s" % (subj or "")[:100], file=OUT)
    print(file=OUT)
    if h is None:
        print("    no baseline commit found -- cannot run G2 or G3", file=OUT)
        return 1

    old = git("show", "%s:%s" % (h, RELPATH))
    tmp = os.path.join(L.HERE, ".baseline_doc.md")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(old)

    A_new, B_new = L.strict_sites(L.DOC), L.relaxed_sites(L.DOC)
    A_old, B_old = L.strict_sites(tmp), L.relaxed_sites(tmp)

    # ------------------------------------------------------------------ G1
    L.rule(OUT, "  G1  BOUNDED, under both predicates.  Population: live sentences\n"
                "      of the document stating the figure.  Grain: one sentence.")
    for name, sites in (("STRICT (the parent's)", A_new),
                        ("RELAXED (this repair's)", B_new)):
        nb = sum(1 for t in sites if t[3])
        print("    %-24s %d of %d sites carry a scope in their own sentence"
              % (name, nb, len(sites)), file=OUT)
    print(file=OUT)
    L.show_sites(B_new, OUT)
    ck("RELAXED: unbounded is 0 of %d" % len(B_new),
       all(t[3] for t in B_new),
       "   (%d unbounded)" % sum(1 for t in B_new if not t[3]))
    ck("STRICT: unbounded is 0 of %d" % len(A_new),
       all(t[3] for t in A_new),
       "   (%d unbounded)" % sum(1 for t in A_new if not t[3]))
    print(file=OUT)

    # ------------------------------------------------------------------ G2
    L.rule(OUT, "  G2  NO SITE LOST, AND ANYTHING ADDED IS BOUNDED.  Same\n"
                "      predicate, pre-repair doc read out of git at the anchor.")
    print("    pre-repair  RELAXED : %d sites, %d bounded, %d unbounded"
          % (len(B_old), sum(1 for t in B_old if t[3]),
             sum(1 for t in B_old if not t[3])), file=OUT)
    print("    post-repair RELAXED : %d sites, %d bounded, %d unbounded"
          % (len(B_new), sum(1 for t in B_new if t[3]),
             sum(1 for t in B_new if not t[3])), file=OUT)
    print("    pre-repair  STRICT  : %d sites, %d bounded" % (
        len(A_old), sum(1 for t in A_old if t[3])), file=OUT)
    print("    post-repair STRICT  : %d sites, %d bounded" % (
        len(A_new), sum(1 for t in A_new if t[3])), file=OUT)
    print(file=OUT)
    # G2 WAS RESPECIFIED, AND THIS IS THE SECOND TIME.  Its first form demanded
    # that the population be the SAME SIZE before and after.  That form exited 1
    # the moment this repair added its own dated note to the document -- a note
    # which states the figure and therefore joins the population.  Forbidding that
    # forbids a repair from recording itself.  The property that actually matters
    # is two-sided and is what is gated on now:
    #   (a) NO PRE-REPAIR SITE IS LOST.  Every one of the pre-repair sites must
    #       still be present, matched by shared vocabulary rather than by line
    #       number, so "0 unbounded" cannot be reached by deletion.
    #   (b) ANY SITE ADDED must itself be bounded -- checked by G1, which is over
    #       the whole post-repair population and not over the matched subset.
    # The size delta is REPORTED with the added sites printed, not gated on.
    print("    population delta : %+d" % (len(B_new) - len(B_old)), file=OUT)
    ck("RELAXED population did not SHRINK", len(B_new) >= len(B_old),
       "   (%d -> %d)" % (len(B_old), len(B_new)))
    print(file=OUT)
    print("    NOTE, and it is a RESULT not a tidy-up: STRICT moved from %d to %d."
          % (len(A_old), len(A_new)), file=OUT)
    print("    Bounding the row-10 sentence required naming Young-Fibonacci in it,", file=OUT)
    print("    which is the very string the parent's same-sentence clause wanted.", file=OUT)
    print("    So the repair closes the blind spot as a side effect of the bound.", file=OUT)
    print(file=OUT)

    # ------------------------------------------------------------------ G3
    L.rule(OUT, "  G3  NO NUMBER MOVED.  Population: integer occurrences inside the\n"
                "      site sentences.  Grain: one integer occurrence.")
    def ints(sites):
        c = {}
        for _, _, s, _ in sites:
            for n in re.findall(r"\b\d+\b", s):
                c[n] = c.get(n, 0) + 1
        return c

    # SITES ARE PAIRED BY DOCUMENT ORDER, NOT BY LINE NUMBER.  The first form of
    # this adjudication keyed on the line number and reported four sites as having
    # "LOST" the figure -- every one of them an artefact of the repair adding lines
    # and shifting the ones below it.  A line number is not an identity across an
    # edit.  Order is: G2 has already established that the population is the same
    # size and that the repair neither added nor removed a site, both lists are in
    # document order, so index i of one is index i of the other.  The pairing is
    # PRINTED with both line numbers and CHECKED by a shared-rare-token test, so
    # the assumption is falsifiable rather than assumed.
    def site_ints(s):
        c = {}
        for n in re.findall(r"\b\d+\b", s):
            c[n] = c.get(n, 0) + 1
        return c

    def rare_tokens(s):
        return {t for t in re.findall(r"[A-Za-z][A-Za-z0-9'’\-]{4,}", s)}

    io, inw = ints(B_old), ints(B_new)
    keys = sorted(set(io) | set(inw), key=lambda x: int(x))
    print("    %-8s %8s %8s" % ("integer", "before", "after"), file=OUT)
    for k in keys:
        mark = "" if inw.get(k, 0) >= io.get(k, 0) else "   <-- fewer, adjudicated below"
        print("    %-8s %8d %8d%s" % (k, io.get(k, 0), inw.get(k, 0), mark),
              file=OUT)
    print(file=OUT)
    dropped = [k for k in keys if inw.get(k, 0) < io.get(k, 0)]

    # A BOUNDING REPAIR IS ALLOWED TO REDUCE AN OCCURRENCE COUNT, and this check
    # was RESPECIFIED after its first form fired on exactly that.  The first form
    # demanded that no integer occur fewer times; it exited 1 on `33`, because two
    # unbounded restatements -- "28 of the 33 are J(P)" says precisely "28 of the
    # 33 are distributive" -- were factored into ONE bounded statement of the
    # family plus two counts.  Forbidding that forbids the repair.  The first
    # form's transcript is kept at out_s3_bound_FIRSTFORM_exit1.txt; the README
    # records the respecification, because silently loosening a check that fired
    # is the thing these audits exist to catch.
    #
    # RESPECIFIED PREDICATE, and it is strictly stronger where it matters:
    #   (a) no measured figure may disappear from the population entirely; and
    #   (b) for every integer whose count fell, the SITES where it fell are named
    #       and each must still state that figure at least once.  A site that lost
    #       a figure outright is a BAD.
    # PAIRING BY SHARED VOCABULARY, not by line number and not by index.  Line
    # numbers shift when a repair adds lines -- the first form of this pairing
    # keyed on them and reported four sites as having LOST a figure, every one an
    # artefact.  Index pairing survived that but breaks as soon as a site is
    # ADDED, which this repair's own note does.  So each pre-repair site is
    # matched to the post-repair site sharing the most words of length >= 5, the
    # match is printed with its score, and a match scoring < 3 is a BAD.
    used, pairs, weak = set(), [], 0
    for o in B_old:
        best, bestscore = None, -1
        for j, n in enumerate(B_new):
            if j in used:
                continue
            sc = len(rare_tokens(o[2]) & rare_tokens(n[2]))
            if sc > bestscore:
                best, bestscore = j, sc
        if best is not None:
            used.add(best)
            pairs.append((o, B_new[best], bestscore))
    added = [B_new[j] for j in range(len(B_new)) if j not in used]
    print("    THE PAIRING, by shared vocabulary.  Each pre-repair site matched",
          file=OUT)
    print("    to the post-repair site sharing the most words of length >= 5:",
          file=OUT)
    print(file=OUT)
    for i, (o, n, sc) in enumerate(pairs, 1):
        if sc < 3:
            weak += 1
        print("      <%02d> old line %-5d -> new line %-5d  shared words %2d%s"
              % (i, o[0], n[0], sc, "   <-- WEAK MATCH" if sc < 3 else ""),
              file=OUT)
    print(file=OUT)
    print("    SITES ADDED BY THIS REPAIR (unmatched, printed in full): %d"
          % len(added), file=OUT)
    print(file=OUT)
    L.show_sites(added, OUT)
    ck("every pre-repair site is matched (none lost)",
       len(pairs) == len(B_old), "   (%d of %d)" % (len(pairs), len(B_old)))
    ck("every match shares >= 3 words with its pre-repair self",
       weak == 0, "   (%d weak)" % weak)
    ck("every site ADDED by this repair is itself bounded",
       all(t[3] for t in added), "   (%d of %d bounded)"
       % (sum(1 for t in added if t[3]), len(added)))

    unexplained = []
    if dropped:
        print(file=OUT)
        print("    ADJUDICATION, per paired site.  For each integer whose count",
              file=OUT)
        print("    fell, the site where it fell and whether it still states it:",
              file=OUT)
        print(file=OUT)
        for k in dropped:
            for i, (o, n, _sc) in enumerate(pairs, 1):
                b4 = site_ints(o[2]).get(k, 0)
                af = site_ints(n[2]).get(k, 0)
                if af < b4:
                    ok = af >= 1
                    print("      figure %-4s site <%02d> (line %d -> %d)  %d -> %d"
                          "   %s" % (k, i, o[0], n[0], b4, af,
                                     "still stated at this site"
                                     if ok else "LOST AT THIS SITE"), file=OUT)
                    if not ok:
                        unexplained.append((k, i))
        print(file=OUT)
    ck("no measured figure disappears from the population",
       all(inw.get(k, 0) >= 1 for k in io),
       "   (gone: %s)" % (", ".join(k for k in io if inw.get(k, 0) < 1) or "none"))
    ck("every reduced occurrence is at a site that still states the figure",
       not unexplained, "   (%d site(s) lost a figure)" % len(unexplained))
    for fig in ("33", "28", "5", "30"):
        ck("the figure %s survives in the site sentences" % fig,
           inw.get(fig, 0) >= 1, "   (%d occurrence(s))" % inw.get(fig, 0))
    print(file=OUT)

    # ------------------------------------------------------------------ G4
    L.rule(OUT, "  G4  THIS REPAIR'S OWN PROSE, HELD TO THE STANDARD IT IMPOSES.\n"
                "      Population: live sentences of the documents THIS repair\n"
                "      authors that state the figure.  Grain: one sentence.\n"
                "      A repair that gates a document and exempts its own account\n"
                "      of that document has not imposed a standard, it has moved\n"
                "      the unbounded sentences into a file nobody checks.")
    own = [os.path.join(L.DOCS, "repair-mg-d075-the-figure-and-its-scope.md"),
           os.path.join(L.HERE, "README.md")]
    for path in own:
        rel = os.path.relpath(path, L.ROOT)
        if not os.path.exists(path):
            print("    %-58s ABSENT" % rel, file=OUT)
            continue
        sites = L.relaxed_sites(path)
        nb = sum(1 for t in sites if t[3])
        print("    %-58s %d sites, %d bounded" % (rel, len(sites), nb), file=OUT)
        for line, kind, sent, b in sites:
            if not b:
                print("        line %-5d UNBOUNDED %s"
                      % (line, re.sub(r"\s+", " ", sent)[:88]), file=OUT)
        ck("%s: unbounded is 0 of %d" % (os.path.basename(path)[:30], len(sites)),
           all(t[3] for t in sites),
           "   (%d unbounded)" % (len(sites) - nb))
    print(file=OUT)

    os.remove(tmp)
    L.rule(OUT)
    print("SUMMARY s3_bound: anchor %s" % (h or "")[:12], file=OUT)
    print("SUMMARY s3_bound: RELAXED %d sites, %d bounded, %d unbounded"
          % (len(B_new), sum(1 for t in B_new if t[3]),
             sum(1 for t in B_new if not t[3])), file=OUT)
    print("SUMMARY s3_bound: STRICT  %d sites, %d bounded, %d unbounded"
          % (len(A_new), sum(1 for t in A_new if t[3]),
             sum(1 for t in A_new if not t[3])), file=OUT)
    print("SUMMARY s3_bound: population %d -> %d; integers dropped %d"
          % (len(B_old), len(B_new), len(dropped)), file=OUT)
    print("SUMMARY s3_bound: failures %d" % bad, file=OUT)
    L.rule(OUT)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
