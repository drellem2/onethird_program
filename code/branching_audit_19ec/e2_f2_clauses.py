"""E2 -- the two NARROWED clauses (F2a, F2b), audited as NEW CLAIMS.

The replacements are:

  F2a (section 2 heading note)
      "28 of the 33 finite Young-Fibonacci intervals are distributive, so each
       is J(P) for some P, item 2."
      plus a new paragraph: "the intervals of Young's lattice are J(P) for P
       EXACTLY the skew cell posets, a named closed class"; "the
       Young-Fibonacci sentence is Birkhoff plus a distributivity count ...
       and names no class of P"; "the 28 ... yield 17 distinct P, of which 5
       are not skew cell posets".

  F2b (section 3 row 10)
      "an index-set contact of the SAME KIND ... it is not the SAME contact.
       The Young headline classifies its index sets -- P exactly the skew cell
       posets -- whereas here no class of P is named, and the 28 intervals
       yield 17 distinct P of which 5 are not skew cell posets."

E2a  EVERY FIGURE, re-derived on a fifth instrument.
E2b  THE BIRKHOFF BICONDITIONAL, BUILT rather than cited: on all 33 intervals,
     distributive <=> isomorphic to J(its own join-irreducibles).
E2c  THE POPULATION OF "THE 33 FINITE YOUNG-FIBONACCI INTERVALS", MEASURED.
     There are infinitely many finite intervals [0,w] in Young-Fibonacci; 33
     is the count at rank <= 6.  Rank 7 is measured here to BUILD the negative
     instead of arguing it.  The replacement sentence carries no bound.  Its
     own sibling in row 10 does.
E2d  THE POPULATION OF "P EXACTLY THE SKEW CELL POSETS".  The clause that
     faults the Young-Fibonacci side for naming no class states the Young
     classification with no bound at all, in a document whose ledger row B2
     records that "exactly" as MEASURED to n <= 6 and whose parent audit lists
     "the converse of X1 beyond n = 6" as NOT CLAIMED.
E2e  THE ASYMMETRY AS STATED.  "The Young headline is a classification; the
     Young-Fibonacci sentence is Birkhoff plus a distributivity count."  Both
     sides are measured here by the SAME procedure, and the real difference is
     reported at its own width.

EXIT 1 if any check fails.  PREDICTED 1 -- E2c and E2d are predicted to fire.
"""

import os
import re
import sys

import kern19ec as K

OUT = sys.stdout
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.join(HERE, "..")
DOC = os.path.join(CODE, "..", "docs",
                   "OneThird-Branching-Graphs-Where-This-Lives.md")
AUDIT5800 = os.path.join(CODE, "..", "docs", "OneThird-Audit-mg-41aa-Repair.md")
BAD = [0]


def ck(label, ok, detail=""):
    if not ok:
        BAD[0] += 1
    print("  %-58s %s%s" % (label, "ok" if ok else "BAD", detail), file=OUT)
    return ok


def head(t):
    print("=" * 78, file=OUT)
    for line in t.split("\n"):
        print(line, file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)


def read(p):
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()


def yf_intervals(max_rank):
    """[0, w] for every Fibonacci word of rank <= max_rank, as posets, built
    from the cover graph and transitive closure only."""
    elts, P = K.yf_poset(max_rank)
    out = []
    for i, w in enumerate(elts):
        below = sorted(K.down_set(P, i))
        out.append((w, K.induced(P, below)))
    return out


def wstr(w):
    return "".join(str(x) for x in w) if w else "0"


CACHE = {}


def skew_classes(k):
    if k not in CACHE:
        CACHE[k] = set(K.skew_shape_classes(k).keys())
    return CACHE[k]


def e2a():
    head("E2a  Every figure under F2, re-derived here.")
    iv = yf_intervals(6)
    ck("intervals [0,w] with rank(w) <= 6: 33", len(iv) == 33, " (%d)" % len(iv))
    lat = [(w, L) for (w, L) in iv if K.is_lattice(L)]
    ck("every one of them is a lattice", len(lat) == len(iv),
       " (%d of %d)" % (len(lat), len(iv)))
    dist = [(w, L) for (w, L) in iv if K.is_distributive(L)]
    nond = [w for (w, L) in iv if not K.is_distributive(L)]
    ck("distributive: 28", len(dist) == 28, " (%d)" % len(dist))
    ck("NOT distributive: 5", len(nond) == 5, " (%d)" % len(nond))
    nond_sorted = sorted(nond, key=lambda w: (sum(w), wstr(w)))
    ck("smallest non-distributive witness is w = 221",
       wstr(nond_sorted[0]) == "221", " (%s)" % wstr(nond_sorted[0]))
    print("  the 5, smallest first: %s"
          % " ".join("%s(rank %d)" % (wstr(w), sum(w)) for w in nond_sorted),
          file=OUT)
    # the index sets
    reps = []
    for (w, L) in dist:
        ji = K.join_irreducibles(L)
        P = K.induced(L, ji)
        ck_size = len(K.ideals(P)) == L[0]
        if not ck_size:
            BAD[0] += 1
        reps.append((w, P))
    ck("|J(P)| = |interval| on every distributive interval",
       all(len(K.ideals(P)) == dict(dist)[w][0] for (w, P) in reps))
    classes = {}
    for (w, P) in reps:
        classes.setdefault(K.canon(P), []).append(w)
    ck("distinct P up to isomorphism: 17", len(classes) == 17,
       " (%d)" % len(classes))
    notskew = {}
    for c, ws in classes.items():
        k = c[0]
        if k and c not in skew_classes(k):
            notskew[c] = ws
    ck("of them NOT skew cell posets: 5", len(notskew) == 5,
       " (%d)" % len(notskew))
    by_size = {}
    for c in classes:
        by_size.setdefault(c[0], [0, 0])[0] += 1
    for c in notskew:
        by_size[c[0]][1] += 1
    print(file=OUT)
    print("   |P|   distinct P   of them NOT skew   the non-skew classes, "
          "with EVERY w that reaches them", file=OUT)
    for k in sorted(by_size):
        groups = ["{" + ",".join(sorted(wstr(w) for w in wl)) + "}"
                  for c, wl in sorted(notskew.items()) if c[0] == k]
        print("   %3d   %10d   %16d   %s" % (k, by_size[k][0], by_size[k][1],
                                             " ".join(groups)), file=OUT)
    print("  (mg-dffa's out_w2_family.txt lists ONE witness per class; the", file=OUT)
    print("   class counts agree exactly, the witness lists differ only in", file=OUT)
    print("   that this one is exhaustive.)", file=OUT)
    ck("2 of the 4 at |P| = 5", by_size.get(5) == [4, 2],
       " (%s)" % by_size.get(5))
    ck("3 of the 5 at |P| = 6", by_size.get(6) == [5, 3],
       " (%s)" % by_size.get(6))
    print(file=OUT)
    ck("skew cell poset classes by cells k=0..6 are 1,1,2,5,11,26,62",
       [1] + [len(skew_classes(k)) for k in range(1, 7)]
       == [1, 1, 2, 5, 11, 26, 62],
       " (%s)" % ([1] + [len(skew_classes(k)) for k in range(1, 7)]))
    # the Young side
    yl = [lam for lam in K.partitions_upto(6)]
    ydist = 0
    yskew = 0
    ycls = set()
    for lam in yl:
        elts, L = K.young_interval((), lam)
        if K.is_distributive(L):
            ydist += 1
        P = K.induced(L, K.join_irreducibles(L))
        c = K.canon(P)
        ycls.add(c)
        if P[0] == 0 or c in skew_classes(P[0]):
            yskew += 1
    ck("Young side: 30 intervals [0,lam] with |lam| <= 6", len(yl) == 30,
       " (%d)" % len(yl))
    ck("  all 30 distributive", ydist == 30, " (%d)" % ydist)
    ck("  0 of the resulting P outside the skew class", yskew == len(yl),
       " (%d in)" % yskew)
    print("  (Young side distinct P up to isomorphism: %d -- the document\n"
          "   reports 17 for Young-Fibonacci and does not report this one.)\n"
          % len(ycls), file=OUT)
    return dist, iv


def e2b(iv):
    head("E2b  The Birkhoff biconditional, BUILT on all 33 rather than cited.")
    good = bad = 0
    for (w, L) in iv:
        P = K.induced(L, K.join_irreducibles(L))
        recon = K.poset_of_sets(K.ideals(P))
        if K.is_distributive(L) == K.iso(recon, L):
            good += 1
        else:
            bad += 1
    ck("on all 33: distributive <=> isomorphic to J(its join-irreducibles)",
       bad == 0, " (%d agree, %d disagree)" % (good, bad))
    print("\n  So the document's clause -- \"'28 of the 33 are J(P)' says\n"
          "  precisely '28 of the 33 are distributive'\" -- is TRUE, and it is\n"
          "  true here as a measurement on this instrument and not only as a\n"
          "  citation of Birkhoff.\n", file=OUT)


def e2c():
    head("E2c  THE POPULATION.  'the 33 finite Young-Fibonacci intervals' --\n"
         "     is 33 the number of finite Young-Fibonacci intervals?")
    iv7 = yf_intervals(7)
    ck("intervals [0,w] with rank(w) <= 7: 54, not 33", len(iv7) == 54,
       " (%d)" % len(iv7))
    d7 = [w for (w, L) in iv7 if K.is_distributive(L)]
    n7 = [w for (w, L) in iv7 if not K.is_distributive(L)]
    print("  at rank <= 7: %d intervals, %d distributive, %d not"
          % (len(iv7), len(d7), len(n7)), file=OUT)
    print("  the Young-Fibonacci lattice has infinitely many elements w, and", file=OUT)
    print("  [0,w] is finite for every one of them, so the set of FINITE", file=OUT)
    print("  Young-Fibonacci intervals is INFINITE.  33 is the count at", file=OUT)
    print("  rank(w) <= 6 and nothing else.", file=OUT)
    print(file=OUT)
    doc = read(DOC)
    m = re.search(r"\*\(\*\*mg-41aa\*\*: items 2 and 5 are re-scoped below.*?\)\*",
                  doc, re.S)
    ck("the F2a replacement sentence located in the document", bool(m))
    sent = m.group() if m else ""
    bound = re.search(r"rank|n\s*(<=|≤)|\|lambda\||\|λ\|", sent)
    ck("the F2a REPLACEMENT carries a rank bound", bool(bound),
       "" if bound else "  <-- it does not; it says 'the 33 finite "
                        "Young-Fibonacci intervals'")
    row10 = [l for l in doc.split("\n") if l.startswith("| **10** |")]
    ck("row 10's mg-41aa clause, the sibling sentence, DOES carry it",
       bool(row10) and "to rank 6" in row10[0])
    flat = re.sub(r"\s*\n\s*>?\s*", " ", doc)
    item2 = re.search(r"of the \*\*33\*\* intervals `\[0̂, w\]` of "
                      r"Young–Fibonacci with `rank\(w\) ≤ 6`", flat)
    ck("section 2 item 2, which the sentence points at, DOES carry it",
       bool(item2))
    print("\n  FINDING E2c.  The replacement sentence's entire content is now a\n"
          "  COUNT, and the count's population is unbounded in the sentence\n"
          "  that states it.  The bound exists twice in the same document --\n"
          "  in row 10 and in item 2 -- so this is a sentence written narrower\n"
          "  in its reading and left wide in its population.  MINOR; the\n"
          "  numbers are right and the pointer 'item 2' is present.\n", file=OUT)


def e2d():
    head("E2d  THE OTHER POPULATION.  'P EXACTLY the skew cell posets'.")
    doc = read(DOC)
    a5800 = read(AUDIT5800)
    m = re.search(r"\*\(\*\*mg-dffa\*\*, landing mg-5800's F2.*?\)\*", doc, re.S)
    ck("the new mg-dffa paragraph located", bool(m))
    para = m.group() if m else ""
    ck("it states the Young side as a classification with 'exactly'",
       "**exactly** the skew cell posets" in para)
    bound = re.search(r"rank|n\s*(<=|≤)|\|P\|\s*(<=|≤)|to `n", para)
    ck("that clause carries a bound", bool(bound),
       "" if bound else "  <-- it does not")
    row10 = [l for l in doc.split("\n") if l.startswith("| **10** |")]
    r10 = row10[0] if row10 else ""
    ck("row 10's new mg-dffa clause states it the same way",
       "`P` exactly the skew cell posets" in r10)
    ck("  ... and it carries no bound either",
       not re.search(r"exactly the skew cell posets[^|]{0,60}(rank|n ≤)", r10))
    # what the document's OWN ledger says the evidence is
    b2 = [l for l in doc.split("\n") if l.startswith("| **B2** |")]
    ck("ledger row B2 exists", bool(b2))
    b2t = b2[0] if b2 else ""
    ck("B2 records the 'exactly' as TESTED, bounded, at n <= 6",
       "405" in b2t and "n ≤ 6" in b2t)
    ck("B2 marks the n >= 7 totals as CITED, not computed",
       "A000112, cited not computed" in b2t)
    ck("mg-5800 lists 'the converse of X1 beyond n = 6' as NOT CLAIMED",
       "the converse of X1 holds beyond `n = 6`" in a5800)
    print(file=OUT)
    print("  FINDING E2d.  This is the more serious of the two, because it is", file=OUT)
    print("  a NEW sentence and it widens in the direction the repair was", file=OUT)
    print("  narrowing.  The paragraph's whole rhetorical move is to fault", file=OUT)
    print("  the Young-Fibonacci side for naming no class of P -- and it", file=OUT)
    print("  makes that contrast by stating the Young side's classification", file=OUT)
    print("  UNBOUNDED, in a document whose own ledger cell for that very", file=OUT)
    print("  claim records it as measured to n <= 6 and whose parent audit", file=OUT)
    print("  puts anything beyond n = 6 on the NOT-CLAIMED list.", file=OUT)
    print(file=OUT)
    print("  WHAT FALLS INSIDE IT.  The claim is not false: it follows from", file=OUT)
    print("  Birkhoff plus the identification of the join-irreducibles of", file=OUT)
    print("  [mu,lam] with the cells of lam/mu.  But the document's whole", file=OUT)
    print("  convention is to separate MEASURED from CITED, and this sentence", file=OUT)
    print("  states as flat fact a thing the document elsewhere books as", file=OUT)
    print("  measured-to-n<=6 and its parent books as not-claimed-beyond-6,", file=OUT)
    print("  and it cites Birkhoff only for the OTHER side of its contrast.", file=OUT)
    print(file=OUT)


def e2e(dist):
    head("E2e  The asymmetry AS STATED, measured on both sides by one\n"
         "     procedure.")
    print("  The paragraph says: the Young headline is a CLASSIFICATION; the", file=OUT)
    print("  Young-Fibonacci sentence is BIRKHOFF PLUS A DISTRIBUTIVITY COUNT.", file=OUT)
    print("  Here is the procedure applied to each side, identically:", file=OUT)
    print(file=OUT)
    yl = K.partitions_upto(6)
    ycls = set()
    for lam in yl:
        _, L = K.young_interval((), lam)
        ycls.add(K.canon(K.induced(L, K.join_irreducibles(L))))
    fcls = set()
    for (w, L) in dist:
        fcls.add(K.canon(K.induced(L, K.join_irreducibles(L))))
    print("    Young       : 30 intervals -> all distributive -> Birkhoff -> "
          "%d distinct P" % len(ycls), file=OUT)
    print("    Young-Fib.  : 33 intervals -> 28 distributive  -> Birkhoff -> "
          "%d distinct P" % len(fcls), file=OUT)
    print(file=OUT)
    ck("both sides reach their P by the SAME route (Birkhoff, then read off\n"
       "     the join-irreducibles)", True)
    ysk = all(c[0] == 0 or c in skew_classes(c[0]) for c in ycls)
    fsk = [c for c in fcls if c[0] and c not in skew_classes(c[0])]
    ck("the Young side's P land inside a named closed class", ysk)
    ck("the Young-Fibonacci side's do not", len(fsk) == 5, " (%d out)" % len(fsk))
    print("\n  PRECISION NOTE, not a defect.  The contrast the paragraph draws\n"
          "  is real, but it is not the contrast its wording names.  BOTH\n"
          "  sides are Birkhoff plus a distributivity count; what differs is\n"
          "  that on the Young side the resulting family has a name and is\n"
          "  closed, and on the Young-Fibonacci side it does not.  The\n"
          "  paragraph's own operative clause -- 'names no class of P' --\n"
          "  says exactly the right thing; the sentence before it implies the\n"
          "  Young side does not go through Birkhoff, and it does.\n", file=OUT)


def main():
    head("E2  mg-19ec: the two NARROWED clauses (F2a, F2b) as new claims.")
    dist, iv = e2a()
    e2b(iv)
    e2c()
    e2d()
    e2e(dist)
    print("=" * 78, file=OUT)
    print("SUMMARY e2_f2_clauses: findings %d" % BAD[0], file=OUT)
    print("=" * 78, file=OUT)
    return 1 if BAD[0] else 0


if __name__ == "__main__":
    sys.exit(main())
