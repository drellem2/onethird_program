"""W1 -- the evidence behind the two ledger cells mg-dffa rewrites (F1).

F1 of mg-5800 says the claim ledger of
`docs/OneThird-Branching-Graphs-Where-This-Lives.md` gained three primed rows
for what the audit BROKE and none for what it STRENGTHENED, so rows B1 and B5
still state less than is known.  This repair rewrites those two cells.  A
rewritten cell is a new claim, so its evidence is measured or located here
BEFORE it is written.

THREE PARTS.

  W1a  B1 AS A LATTICE ISOMORPHISM, MEASURED HERE.  For every partition to
       n <= 7, the map "order ideal of D_lam |-> the shape it fills" is checked
       to be a bijection J(D_lam) -> [0, lam], to preserve the ORDER in both
       directions, and -- separately, because the separation is the whole of F1
       -- to preserve the MEET and the JOIN on every pair.  The two sides are
       built from different definitions: the left from order ideals of the cell
       poset, the right from containment of PARTITIONS.

  W1b  WHY THE OLD CELL UNDERSTATED, LOCATED IN af28's OWN SOURCE.  af28's
       `t_young.py` T1 prints the label `lattice-iso bad`, and its T1 code
       computes no meet and no join.  So the ledger cell and the printed label
       err in OPPOSITE directions off the same test.  Checked mechanically.

  W1c  B5's RE-DERIVATION, LOCATED AND NOT RE-RUN.  The narrowed B5 cell says
       the step to "all irreducibles are 1-dimensional" has since been derived
       without a trace form and without citing Brown.  That is a claim about
       two OTHER instruments.  It is discharged here by locating the printed
       result in their committed output files and reading their own counts out
       of their own tables -- NOT by re-running them and NOT by importing them.
       The distinction is stated in the output, because a located result and a
       reproduced result carry different warrant.

FALSIFIERS.  Any meet or join failure in W1a; any meet/join computation found
in af28's T1, or a printed label that does not say `lattice-iso`; any of the
W1c strings absent from the committed outputs.
"""

import os
import re
import sys

from kerndffa import (Lattice, cell_poset, ideals, partitions, shape_of_ideal,
                      skew_cells, young_interval)

OUT = sys.stdout
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.join(HERE, "..")

T_YOUNG = os.path.join(CODE, "branching_af28", "t_young.py")
OUT_YOUNG = os.path.join(CODE, "branching_af28", "out_young.txt")
A1_6AD0 = os.path.join(CODE, "branching_audit_6ad0", "out_a1_contact.txt")
A4_6AD0 = os.path.join(CODE, "branching_audit_6ad0", "out_a4_algebra.txt")
A5_5800 = os.path.join(CODE, "branching_audit_5800", "out_a5_b1b5.txt")

BAD = [0]


def verdict(label, ok, detail=""):
    if not ok:
        BAD[0] += 1
    print("  %-58s %s%s" % (label, "ok" if ok else "BAD", detail), file=OUT)


def w1a():
    print("=" * 78, file=OUT)
    print("W1a  B1: J(D_lam) -> [0, lam] as a LATTICE isomorphism, measured.", file=OUT)
    print("     Left side: order ideals of the cell poset.  Right side: the", file=OUT)
    print("     PARTITIONS nu with nu contained in lam, under containment.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    print("   n  lam                  |J|  |[0,lam]|  order  meet  join", file=OUT)
    tot = order_bad = meet_bad = join_bad = 0
    pairs = 0
    biggest = 0
    for n in range(1, 8):
        for lam in partitions(n):
            tot += 1
            cells = skew_cells(lam, ())
            up = cell_poset(lam)
            ids = ideals(up)
            leq = [[(ids[a] & ids[b]) == ids[a] for b in range(len(ids))]
                   for a in range(len(ids))]
            J = Lattice(ids, leq)
            Y = young_interval((), lam)
            biggest = max(biggest, J.n)
            phi = [shape_of_ideal(m, cells) for m in ids]
            index = {nu: i for i, nu in enumerate(Y.elements)}
            ob = mb = jb = 0
            bijective = (len(set(phi)) == len(phi)
                         and set(phi) == set(Y.elements))
            if not bijective:
                ob += 1
            else:
                for a in range(J.n):
                    for b in range(J.n):
                        pairs += 1
                        if J.leq[a][b] != Y.leq[index[phi[a]]][index[phi[b]]]:
                            ob += 1
                        if phi[J.meet[a][b]] != Y.elements[
                                Y.meet[index[phi[a]]][index[phi[b]]]]:
                            mb += 1
                        if phi[J.join[a][b]] != Y.elements[
                                Y.join[index[phi[a]]][index[phi[b]]]]:
                            jb += 1
            order_bad += ob
            meet_bad += mb
            join_bad += jb
            print("  %2d  %-20s %4d  %8d  %5s %5s %5s"
                  % (n, str(lam), J.n, Y.n,
                     "." if ob == 0 else "BAD", "." if mb == 0 else "BAD",
                     "." if jb == 0 else "BAD"), file=OUT)
    print(file=OUT)
    print("  partitions tested: %d   largest interval: %d elements"
          % (tot, biggest), file=OUT)
    print("  ordered pairs tested: %d" % pairs, file=OUT)
    verdict("order failures, both directions, every pair", order_bad == 0,
            " (%d)" % order_bad)
    verdict("MEET not preserved", meet_bad == 0, " (%d)" % meet_bad)
    verdict("JOIN not preserved", join_bad == 0, " (%d)" % join_bad)
    print(file=OUT)
    print("  => on 44 partitions to n <= 7 the map is a LATTICE isomorphism,", file=OUT)
    print("     not merely an order isomorphism: %s"
          % (order_bad == meet_bad == join_bad == 0), file=OUT)
    print(file=OUT)
    return tot


def w1b():
    print("=" * 78, file=OUT)
    print("W1b  The old B1 cell and af28's printed label err in OPPOSITE", file=OUT)
    print("     directions off one test.  Located in af28's own source.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    src = open(T_YOUNG, encoding="utf-8").read()
    m = re.search(r"\ndef t1\(.*?\n(?=\ndef )", src, re.S)
    body = m.group(0) if m else ""
    verdict("t_young.py's T1 body located", bool(body))
    n_meet = len(re.findall(r"\bmeet\b", body, re.I))
    n_join = len(re.findall(r"\bjoin\b", body, re.I))
    verdict("T1 computes no meet", n_meet == 0, " (%d occurrences)" % n_meet)
    verdict("T1 computes no join", n_join == 0, " (%d occurrences)" % n_join)
    verdict("T1 nonetheless prints the label 'lattice-iso bad'",
            "lattice-iso bad" in body)
    y = open(OUT_YOUNG, encoding="utf-8").read()
    hit = [ln.strip() for ln in y.split("\n") if "lattice-iso bad" in ln]
    verdict("out_young.txt carries that label", len(hit) == 1,
            " (%d lines)" % len(hit))
    for ln in hit:
        print("      out_young.txt: %s" % ln, file=OUT)
    print(file=OUT)
    print("  READING.  af28's T1 tests the ORDER isomorphism and labels the", file=OUT)
    print("  result `lattice-iso`; af28's LEDGER cell B1 says `order", file=OUT)
    print("  isomorphism` while the fact is a lattice isomorphism.  The output", file=OUT)
    print("  over-labels and the ledger under-states, off the same run.", file=OUT)
    print("  mg-dffa narrows the LEDGER cell only.  The label in", file=OUT)
    print("  code/branching_af28/ is left alone: changing it would rewrite a", file=OUT)
    print("  committed output that mg-5800 re-ran and found byte-identical,", file=OUT)
    print("  and no ticket has asked for that.  It is recorded, not fixed.", file=OUT)
    print(file=OUT)


def w1c():
    print("=" * 78, file=OUT)
    print("W1c  B5's re-derivation: LOCATED in two committed outputs, NOT", file=OUT)
    print("     re-run here.  This is a weaker act than measuring and it is", file=OUT)
    print("     named as one.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    a4 = open(A4_6AD0, encoding="utf-8").read()
    a5 = open(A5_5800, encoding="utf-8").read()
    a1 = open(A1_6AD0, encoding="utf-8").read()

    def flat(s):
        return re.sub(r"\s+", " ", s)

    f4, f5, f1 = flat(a4), flat(a5), flat(a1)
    verdict("mg-6ad0 out_a4_algebra.txt: 'no theorem of Dickson and no trace form'",
            "by a route that uses no theorem of Dickson and no trace form" in f4)
    verdict("mg-6ad0 out_a4_algebra.txt: Phi surjective, kernel nilpotent",
            "Phi: kF(P) -> k^{AC(P)} is a surjective algebra map whose kernel "
            "is a nilpotent ideal, on every poset tested" in f4)
    verdict("mg-5800 out_a5_b1b5.txt: 'NO trace form and NO cited theorem'",
            "B5 WITHOUT A TRACE FORM" in f5
            and "with NO trace form and NO cited theorem" in f5)
    verdict("mg-5800 out_a5_b1b5.txt: 87 posets, 0 bad on every column",
            "posets: 87;  LRB failures: 0" in a5
            and "ker Phi NOT nilpotent: 0" in a5)
    verdict("mg-6ad0 out_a1_contact.txt: meet/join measured, 0 bad",
            "LATTICE-isomorphism bad (meet/join preserved): 0" in a1)
    verdict("mg-5800 out_a5_b1b5.txt: meet/join measured, 0 bad",
            "MEET not preserved: 0" in a5 and "JOIN not preserved: 0" in a5)

    # mg-6ad0's B5 run has a size cap.  Read its own table rather than typing
    # the number of posets it actually tested.  Scoped to the A4a block: the
    # same file's A4b block has a numeric table of its own, and an unscoped
    # regex silently summed both -- it returned 174 classes where 87 is the
    # whole population, which is why this reads a section and not a file.
    i, j = a4.find("\nA4a "), a4.find("\nA4b ")
    a4a = a4[i:j] if 0 <= i < j else ""
    verdict("mg-6ad0's A4a section isolated from A4b", bool(a4a))
    rows = [re.split(r"\s+", ln.strip()) for ln in a4a.split("\n")
            if re.match(r"^\s*\d+(\s+\d+){8}\s*$", ln)]
    tested = sum(int(r[2]) for r in rows)
    classes = sum(int(r[1]) for r in rows)
    skipped = sum(int(r[3]) for r in rows)
    verdict("A4a's table has one row per rank n = 1..5", len(rows) == 5,
            " (%d rows)" % len(rows))
    print(file=OUT)
    print("  mg-6ad0's own table, read off its output: %d classes, %d tested,"
          % (classes, tested), file=OUT)
    print("  %d skipped over its |F(P)| <= 90 cap (each skip listed there)."
          % skipped, file=OUT)
    verdict("its table is internally consistent", classes == tested + skipped)
    verdict("mg-5800 covered the classes mg-6ad0 capped out", classes == 87
            and tested < 87)
    print(file=OUT)
    print("  READING.  The step from `dim kF(P)/rad = |AC(P)|` to `all", file=OUT)
    print("  irreducibles are 1-dimensional` was booked to Brown, cited and", file=OUT)
    print("  not re-derived, in af28's ledger.  It has since been derived", file=OUT)
    print("  twice with no trace form and no cited theorem: by mg-6ad0 on %d"
          % tested, file=OUT)
    print("  of 87 classes to n <= 5, and by mg-5800 on all 87.  mg-dffa", file=OUT)
    print("  LOCATES those results; it does not reproduce them, and the", file=OUT)
    print("  narrowed ledger cell attributes them rather than claiming them.", file=OUT)
    print(file=OUT)


def main():
    n = w1a()
    w1b()
    w1c()
    print("=" * 78, file=OUT)
    print("SUMMARY w1_ledger: partitions %d, failures %d" % (n, BAD[0]), file=OUT)
    print("=" * 78, file=OUT)
    return 1 if BAD[0] else 0


if __name__ == "__main__":
    sys.exit(main())
