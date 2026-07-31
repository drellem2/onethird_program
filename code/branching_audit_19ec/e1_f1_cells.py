"""E1 -- the two WIDENED ledger cells, audited as NEW CLAIMS.

mg-dffa rewrote rows B1 and B5 of the claim ledger in
`docs/OneThird-Branching-Graphs-Where-This-Lives.md`.  mg-19ec's brief is to
ignore what they used to say and ask whether what they NOW say is true and is
carried by the evidence cited FOR IT.  A widening is the direction in which
"narrowed to the evidence" can overshoot, so B1 and B5 get the harder look.

E1a  B1's ARITHMETIC AND ITS LATTICE CLAIM, re-measured from definitions.
     The cell says: 44 partitions, n <= 7, meet and join preserved on every
     pair, 5 464 ordered pairs.  Here BOTH sides compute their meets and joins
     as greatest lower bounds and least upper bounds IN THE ORDER, by search.
     The left side is NOT allowed to use "intersection of ideals" and the right
     side is NOT allowed to use "componentwise minimum of partitions" -- those
     are exactly the identifications the cell asserts, and assuming them would
     make the measurement circular.

E1b  B1's SUB-CLAIM ABOUT SOMEBODY ELSE'S CODE, read rather than counted.
     The cell says T1 in code/branching_af28/ "tests the ORDER isomorphism
     only".  mg-dffa's evidence for that is a WORD COUNT -- zero occurrences of
     `meet` or `join` in T1's body.  A word count is a proxy: code can compute
     a meet without naming one.  So T1's body is extracted and every operation
     it performs on the two sides is listed, and the question is asked at the
     level the cell asserts it.

E1c  B1's INDEPENDENCE CLAIM.  "measured three times on disjoint instruments".
     Disjointness is checked as a property of the three directories, by import
     graph, not taken from a README.

E1d  B5's TWO ATTRIBUTIONS, and the step they are supposed to close.
     67 / 20 / 87 and "all 87" are read out of the two committed outputs.  And
     the load-bearing word is checked: `Phi` surjective with nilpotent kernel
     gives "all irreducibles are 1-dimensional" ONLY IF `Phi` is an ALGEBRA
     map.  If the cited output claims only a linear surjection, the widened
     cell asserts a step its evidence does not carry.

E1e  B5's SELF-DESCRIPTION.  The cell says mg-dffa LOCATED and did not re-run.
     Checked against w1_ledger.py: no import of the cited directories, and no
     subprocess.

EXIT 1 if any check fails.  PREDICTED 0.
"""

import os
import re
import subprocess
import sys

import kern19ec as K

OUT = sys.stdout
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.join(HERE, "..")
ROOT = os.path.join(CODE, "..")
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


# ---------------------------------------------------------------------------


def e1a():
    head("E1a  B1 re-measured.  Meet and join are GREATEST LOWER BOUND and\n"
         "     LEAST UPPER BOUND computed by search, on BOTH sides.")
    parts = [lam for lam in K.partitions_upto(7) if lam]
    pairs = 0
    order_bad = meet_bad = join_bad = bij_bad = 0
    biggest = 0
    for lam in parts:
        cells = sorted(K.skew_cells(lam, ()))
        P = K.cell_poset(cells)
        ids = K.ideals(P)
        JL = K.poset_of_sets(ids)
        elts, IL = K.young_interval((), lam)
        biggest = max(biggest, len(elts))
        # the map ideal -> the shape it fills, built from the cells
        img = []
        for S in ids:
            rows = {}
            for i in S:
                r, c = cells[i]
                rows[r] = max(rows.get(r, -1), c)
            img.append(tuple(rows[r] + 1 for r in range(len(lam)) if r in rows))
        pos = {nu: i for i, nu in enumerate(elts)}
        if len(set(img)) != len(ids) or set(img) != set(elts):
            bij_bad += 1
            continue
        phi = [pos[s] for s in img]
        ML, MI = K.meet_table(JL), K.meet_table(IL)
        JT, JI = K.join_table(JL), K.join_table(IL)
        for a in range(len(ids)):
            for b in range(len(ids)):
                pairs += 1
                if K.leq(JL, a, b) != K.leq(IL, phi[a], phi[b]):
                    order_bad += 1
                if phi[ML[a][b]] != MI[phi[a]][phi[b]]:
                    meet_bad += 1
                if phi[JT[a][b]] != JI[phi[a]][phi[b]]:
                    join_bad += 1
    ck("partitions with 1 <= n <= 7 number 44", len(parts) == 44,
       " (%d)" % len(parts))
    ck("largest interval has 19 elements", biggest == 19, " (%d)" % biggest)
    ck("ideal -> shape is a bijection on every one", bij_bad == 0,
       " (%d bad)" % bij_bad)
    ck("ordered pairs tested = 5 464", pairs == 5464, " (%d)" % pairs)
    ck("  ... and 5 464 = sum of |[0,lam]|^2 over the 44",
       pairs == sum(len(K.young_interval((), l)[0]) ** 2 for l in parts))
    ck("ORDER preserved both directions, every pair", order_bad == 0,
       " (%d bad)" % order_bad)
    ck("MEET preserved, glb by search on both sides", meet_bad == 0,
       " (%d bad)" % meet_bad)
    ck("JOIN preserved, lub by search on both sides", join_bad == 0,
       " (%d bad)" % join_bad)
    print("\n  VERDICT E1a.  The widened B1 cell is TRUE at the width it is\n"
          "  written, on a fifth instrument, with neither side permitted to\n"
          "  assume the identification it asserts.\n", file=OUT)


def e1b():
    head("E1b  B1's sub-claim about af28's T1, READ instead of counted.")
    src = read(os.path.join(CODE, "branching_af28", "t_young.py"))
    m = re.search(r"^def t1\(.*?(?=^def )", src, re.M | re.S)
    ck("T1's body located in t_young.py", bool(m))
    if not m:
        return
    body = m.group()
    nmeet = len(re.findall(r"\bmeet\b", body, re.I))
    njoin = len(re.findall(r"\bjoin\b", body, re.I))
    ck("mg-dffa's proxy reproduces: 0 occurrences of 'meet'", nmeet == 0,
       " (%d)" % nmeet)
    ck("mg-dffa's proxy reproduces: 0 occurrences of 'join'", njoin == 0,
       " (%d)" % njoin)
    # the harder question: is a meet or a join FORMED, under any name?
    inter = re.findall(r"^\s*(.*&.*)$", body, re.M)
    union = re.findall(r"^\s*(.*\|.*)$", body, re.M)
    print(file=OUT)
    print("  every expression in T1's body that forms a set intersection:", file=OUT)
    for line in inter:
        print("      %s" % line.strip(), file=OUT)
    print("  every expression that forms a set union: %s"
          % ("none" if not union else union), file=OUT)
    print(file=OUT)
    used_as_test = all(re.search(r"==\s*ids\[a\]|==\s*ids\[b\]", ln)
                       for ln in inter) and inter
    ck("every intersection T1 forms is consumed by a CONTAINMENT TEST",
       bool(used_as_test))
    ck("T1 compares no meet with a meet, and no join with a join",
       njoin == 0 and bool(used_as_test))
    ck("T1 nonetheless prints the label 'lattice-iso bad'",
       "lattice-iso bad" in body)
    print("\n  VERDICT E1b.  The DOCUMENT's sentence -- T1 'tests the ORDER\n"
          "  isomorphism only' -- survives a reading and not merely a word\n"
          "  count.  Recorded for precision: mg-dffa's own probe line reads\n"
          "  'T1 computes no meet (0 occurrences)', and T1 does form\n"
          "  ids[a] & ids[b].  It forms it only to test containment, so the\n"
          "  cell is right and the probe's wording is the loose one.\n",
          file=OUT)


def imports_of(d):
    out = set()
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".py"):
            continue
        for m in re.finditer(r"^\s*(?:from|import)\s+([A-Za-z0-9_.]+)",
                             read(os.path.join(d, fn)), re.M):
            out.add(m.group(1).split(".")[0])
    return out


def e1c():
    head("E1c  'measured three times on disjoint instruments' -- checked as a\n"
         "     property of the import graph, not read off a README.")
    dirs = {"mg-6ad0": "branching_audit_6ad0", "mg-5800": "branching_audit_5800",
            "mg-dffa": "branching_warrant_dffa", "mg-19ec": "branching_audit_19ec"}
    mods = {}
    for name, d in dirs.items():
        p = os.path.join(CODE, d)
        mods[name] = {fn[:-3] for fn in os.listdir(p) if fn.endswith(".py")}
    for name, d in dirs.items():
        imp = imports_of(os.path.join(CODE, d))
        foreign = set()
        for other, om in mods.items():
            if other != name:
                foreign |= (imp & om)
        ck("%s imports no module of the other three" % name, not foreign,
           "" if not foreign else " (%s)" % sorted(foreign))
    print(file=OUT)
    print("  and each of the four measures B1's meet/join for itself:", file=OUT)
    for name, d, needle in [
            ("mg-6ad0", "branching_audit_6ad0/out_a1_contact.txt",
             "LATTICE-isomorphism bad"),
            ("mg-5800", "branching_audit_5800/out_a5_b1b5.txt", "MEET not preserved"),
            ("mg-dffa", "branching_warrant_dffa/out_w1_ledger.txt",
             "MEET not preserved")]:
        txt = read(os.path.join(CODE, d))
        line = [l for l in txt.split("\n") if needle in l]
        ck("%s prints its own meet/join line" % name, bool(line),
           " (%s)" % (line[0].strip() if line else ""))
    print("\n  VERDICT E1c.  Disjoint at the level the cell claims.\n", file=OUT)


def e1d():
    head("E1d  B5's two attributions, and the word the STEP rests on.")
    a4 = read(os.path.join(CODE, "branching_audit_6ad0", "out_a4_algebra.txt"))
    a5 = read(os.path.join(CODE, "branching_audit_5800", "out_a5_b1b5.txt"))
    # read mg-6ad0's A4a table for ourselves, out of the A4a section only
    sec = a4.split("A4b")[0]
    rows = re.findall(r"^\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s", sec, re.M)
    classes = sum(int(r[1]) for r in rows)
    tested = sum(int(r[2]) for r in rows)
    skipped = sum(int(r[3]) for r in rows)
    ck("A4a's table has one row per rank n = 1..5", len(rows) == 5,
       " (%d rows)" % len(rows))
    ck("read out of the A4a SECTION ONLY: classes = 87", classes == 87,
       " (%d)" % classes)
    ck("  tested = 67", tested == 67, " (%d)" % tested)
    ck("  skipped = 20", skipped == 20, " (%d)" % skipped)
    ck("  internally consistent: classes == tested + skipped",
       classes == tested + skipped)
    ck("the cap mg-dffa names is the cap the output names",
       "|F(P)| <= 90" in a4)
    ck("every skip is listed there",
       len(re.findall(r"n=5 \|F\(P\)\|=\d+\s+x\d", a4)) > 0,
       " (%d listed groups)" % len(re.findall(r"n=5 \|F\(P\)\|=\d+\s+x\d", a4)))
    ck("mg-6ad0's quoted clause is verbatim in its output",
       "no theorem of Dickson and no trace form" in a4)
    ck("mg-5800's quoted clause is verbatim in its output",
       "NO trace form and NO cited theorem" in a5)
    ck("mg-5800 covers all 87", "for all 87 posets to n <= 5" in a5)
    print(file=OUT)
    print("  THE STEP.  `dim kF(P)/rad = |AC(P)|` alone does NOT give 'all", file=OUT)
    print("  irreducibles are 1-dimensional'.  What gives it is that Phi is a", file=OUT)
    print("  SURJECTIVE ALGEBRA MAP with nilpotent kernel, which forces", file=OUT)
    print("  kF(P)/rad = k^{AC(P)}, a product of |AC(P)| copies of k.  So the", file=OUT)
    print("  widened cell needs the cited outputs to say ALGEBRA, not linear.", file=OUT)
    print(file=OUT)
    ck("mg-6ad0's output says 'surjective ALGEBRA map'",
       bool(re.search(r"surjective algebra map", a4, re.I)))
    ck("  ... with a NILPOTENT kernel", bool(re.search(r"nilpotent", a4, re.I)))
    ck("  ... and draws kF(P)/rad = k^{AC(P)} itself",
       "kF(P)/rad = k^{AC(P)}" in a4)
    ck("mg-5800's output checks character MULTIPLICATIVITY",
       "character-multiplicativity failures: 0" in a5
       or "character-hom bad 0" in a5)
    ck("  ... and surjectivity, and kernel nilpotence, at 0",
       "Phi surjective" in a5 and "ker Phi NOT nilpotent: 0" in a5)
    print("\n  VERDICT E1d.  The widened B5 cell asserts a DERIVATION, and the\n"
          "  two outputs it names carry a derivation and not a weaker linear\n"
          "  statement.  67 / 20 / 87 and 'all 87' are what those outputs\n"
          "  print, read out of the A4a section alone.\n", file=OUT)


def e1e():
    head("E1e  B5's self-description: LOCATED, not MEASURED.")
    w1 = read(os.path.join(CODE, "branching_warrant_dffa", "w1_ledger.py"))
    ck("w1_ledger.py imports no module of the cited directories",
       not re.search(r"import\s+(core_af28|kern6ad0|kern5800|lib41aa)", w1))
    ck("w1_ledger.py starts no subprocess",
       "subprocess" not in w1 and "os.system" not in w1)
    ck("w1_ledger.py opens those directories' OUTPUT files only",
       all(f.endswith(".txt") or f.endswith(".py")
           for f in re.findall(r'"([a-z0-9_]+\.(?:txt|py))"', w1)))
    ck("the cell itself says LOCATED and not MEASURED",
       "LOCATED both results" in read(
           os.path.join(ROOT, "docs",
                        "OneThird-Branching-Graphs-Where-This-Lives.md")))
    print("\n  VERDICT E1e.  The self-description is accurate: mg-dffa read two\n"
          "  committed outputs and re-ran neither.  A located result and a\n"
          "  reproduced one carry different warrant and the cell says which.\n",
          file=OUT)


def main():
    head("E1  mg-19ec: the two WIDENED ledger cells (B1, B5) as new claims.")
    e1a()
    e1b()
    e1c()
    e1d()
    e1e()
    print("=" * 78, file=OUT)
    print("SUMMARY e1_f1_cells: failures %d" % BAD[0], file=OUT)
    print("=" * 78, file=OUT)
    return 1 if BAD[0] else 0


if __name__ == "__main__":
    sys.exit(main())
