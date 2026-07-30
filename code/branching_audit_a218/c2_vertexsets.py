"""c2_vertexsets.py -- the vertex SET, not the vertex COUNT; and the repair's
own new cross-instrument claim.

Two things, both of which the primary target of my brief requires:

  (A) "Check the vertex sets, not only a count."  The repaired document's
      four-row table in section 0 carries a column headed
      "# irreducibles at n = 1...6" and prints 1, 2, 2, 3, 3, 4 in it for
      beta = 3, beta = 2 AND beta = 1.  That is a COUNT.  This script asks
      whether the vertex SETS are equal wherever the counts are, for every
      ordered pair of parameters at every level.

  (B) The repair introduces a claim no earlier list names: that T1b2
      "agrees ROW FOR ROW with mg-2060's B1a/B1b on a disjoint instrument".
      This script parses BOTH committed outputs and compares all three
      instruments cell by cell, so the row-for-row claim is measured rather
      than accepted.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import os
import re
import sys

from kern_a218 import TL

BETAS = [3, 2, 1, 0]
NMAX = 6
HERE = os.path.dirname(__file__)
T1B2 = os.path.join(HERE, "..", "branching_locate_db09", "out_t1_tl.txt")
B1 = os.path.join(HERE, "..", "branching_audit_2060", "out_b1_branching.txt")
DOC = os.path.join(HERE, "..", "..", "docs",
                   "OneThird-Bratteli-Path-Algebras-Where-This-Lives.md")

SELF, FIND = [], []

print("=" * 74)
print("c2  THE VERTEX SET AGAINST THE VERTEX COUNT, AND THE ROW-FOR-ROW CLAIM")
print("=" * 74)
print()

mine = {}
for beta in BETAS:
    for n in range(1, NMAX + 1):
        mine[(beta, n)] = TL(n, beta).vertices()

# ---------------------------------------------------------------------------
# (A)  set vs count
# ---------------------------------------------------------------------------
print("(A)  IS THE VERTEX SET EQUAL WHEREVER THE VERTEX COUNT IS EQUAL?")
print()
print("     A vertex of the branching graph is an irreducible module.  Two")
print("     graphs have the same vertex set at level n only if the labelled")
print("     vertices agree -- here, the multiset of dim L(n,p).  Counting them")
print("     is a statistic ABOUT the vertex set, not the vertex set.")
print()

pairs = [(a, b) for i, a in enumerate(BETAS) for b in BETAS[i + 1:]]
cells_examined = 0
count_eq_set_ne = []
for (a, b) in pairs:
    print("     beta = %d against beta = %d" % (a, b))
    for n in range(1, NMAX + 1):
        va, vb = mine[(a, n)], mine[(b, n)]
        ca, cb = len(va), len(vb)
        same_count = ca == cb
        same_set = va == vb
        cells_examined += 1
        verdict = ("count %s, set %s"
                   % ("EQUAL" if same_count else "differ (%d vs %d)" % (ca, cb),
                      "EQUAL" if same_set else "DIFFER"))
        print("       n=%d  %-34s  dims %s  vs  %s"
              % (n, verdict, [d for _, d in va], [d for _, d in vb]))
        if same_count and not same_set:
            count_eq_set_ne.append((a, b, n, [d for _, d in va], [d for _, d in vb]))
    print()

print("     LEVELS WHERE THE COUNT AGREES AND THE SET DOES NOT: %d, population: "
      "the %d (parameter-pair, level) cells above (6 ordered pairs of the 4 "
      "parameters x 6 levels)" % (len(count_eq_set_ne), cells_examined))
for (a, b, n, da, db) in count_eq_set_ne:
    print("       beta=%d vs beta=%d at n=%d: both have %d vertices, dims %s vs %s"
          % (a, b, n, len(da), da, db))
print()

# what the document's table column says
doc = open(DOC).read()
row_re = re.compile(r"^\|\s*(\d)\s*\|\s*132\s*\|.*?\|\s*([\d,\s*]+?)\s*\|\s*[^|]*\|\s*$",
                    re.M)
doc_rows = {}
for m in row_re.finditer(doc):
    beta = int(m.group(1))
    nums = [int(x) for x in re.findall(r"\d+", m.group(2))]
    if len(nums) == 6:
        doc_rows[beta] = nums
print("     THE DOCUMENT'S OWN COLUMN, parsed out of section 0's four-row table")
print("     (heading: '# irreducibles at n = 1...6'):")
for beta in BETAS:
    print("       beta=%d : %s   -- mine, as counts: %s"
          % (beta, doc_rows.get(beta, "NOT PARSED"),
             [len(mine[(beta, n)]) for n in range(1, NMAX + 1)]))
for beta in BETAS:
    if beta not in doc_rows:
        SELF.append("could not parse the section-0 table row for beta=%d" % beta)
    elif doc_rows[beta] != [len(mine[(beta, n)]) for n in range(1, NMAX + 1)]:
        FIND.append("section 0's table row for beta=%d prints %s; measured counts "
                    "are %s" % (beta, doc_rows[beta],
                                [len(mine[(beta, n)]) for n in range(1, NMAX + 1)]))
print()

b1_vs_b3 = [c for c in count_eq_set_ne if set((c[0], c[1])) == {3, 1}]
if b1_vs_b3:
    FIND.append(
        "section 0's vertex column is a COUNT and is IDENTICAL for beta = 3, 2 "
        "and 1 (1,2,2,3,3,4), but the vertex SETS at beta = 3 and beta = 1 "
        "differ at %d of the 6 levels (%s). The document substantiates "
        "'the vertex set is not even the same' only at beta = 0. The instrument "
        "(T1b2) prints the dimensions and has the evidence; the table does not "
        "carry it."
        % (len(b1_vs_b3), ", ".join("n=%d: %s vs %s" % (c[2], c[3], c[4])
                                    for c in b1_vs_b3)))

# the document's own scoped sentence, checked
print("     the document's sentence 'At beta = 0 the tower has fewer irreducibles")
print("     at every EVEN level' -- checked level by level:")
ok_even = True
for n in range(1, NMAX + 1):
    c0, c3 = len(mine[(0, n)]), len(mine[(3, n)])
    if n % 2 == 0:
        good = c0 < c3
        ok_even &= good
        print("       n=%d (even): beta=0 has %d, beta=3 has %d   %s"
              % (n, c0, c3, "fewer" if good else "NOT FEWER"))
    else:
        print("       n=%d (odd) : beta=0 has %d, beta=3 has %d   %s"
              % (n, c0, c3, "equal" if c0 == c3 else "DIFFER"))
if not ok_even:
    FIND.append("'fewer irreducibles at every even level' is false at some even level")
print("     verdict: %s, population: the 3 even and 3 odd levels 1 <= n <= 6"
      % ("holds" if ok_even else "FAILS"))
print()

# ---------------------------------------------------------------------------
# (B)  three instruments, cell by cell
# ---------------------------------------------------------------------------
print("(B)  THE REPAIR'S OWN NEW CLAIM: 'agrees ROW FOR ROW with mg-2060's")
print("     B1a/B1b on a disjoint instrument'.  Measured, not accepted.")
print()


def parse_rows(path, start, end):
    txt = open(path).read()
    seg = txt.split(start)[1].split(end)[0]
    cur = None
    rows = {}
    for line in seg.splitlines():
        m = re.match(r"\s*---- beta = (\d+) ----", line)
        if m:
            cur = int(m.group(1))
            continue
        m = re.match(r"\s*L\((\d+),(\d+)\) dim (\d+)\s+->\s+(.*)$", line)
        if m and cur is not None:
            n, p, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
            ed = {int(x[1]): int(x[2])
                  for x in re.findall(r"\[L\((\d+),(\d+)\)\]=(\d+)", m.group(4))}
            rows[(cur, n, p)] = (d, ed)
    return rows


t1b2 = parse_rows(T1B2, "T1b2  THE BRANCHING GRAPH AS VERSHIK-OKOUNKOV DEFINE IT",
                  "T1c  SEMISIMPLICITY")
b1b = parse_rows(B1, "B1b  THE EDGES, from characters, at every parameter",
                 "B1c ") if "B1c " in open(B1).read() else parse_rows(
    B1, "B1b  THE EDGES, from characters, at every parameter", "\nTOTAL BAD")

mine_rows = {}
for beta in BETAS:
    for n in range(2, NMAX + 1):
        A, B = TL(n, beta), TL(n - 1, beta)
        pass  # rows come from c1's measurement, recomputed here for independence
# recompute rows here (cheap) so this script does not depend on c1's output
from kern_a218 import diagrams, embed, solve_exact
for beta in BETAS:
    for n in range(2, NMAX + 1):
        A, B = TL(n, beta), TL(n - 1, beta)
        Dsub = diagrams(n - 1)
        vB = B.vertices()
        chi = [[B.trace_on_L(d, q) for d in Dsub] for (q, _) in vB]
        chiT = [[chi[j][i] for j in range(len(vB))] for i in range(len(Dsub))]
        for (p, dp) in A.vertices():
            tgt = [A.trace_on_L(embed(d, n), p) for d in Dsub]
            sol, uniq = solve_exact(chiT, tgt)
            if sol is None or not uniq:
                SELF.append("solve failed at beta=%d n=%d p=%d" % (beta, n, p))
                continue
            mine_rows[(beta, n, p)] = (dp, {q: int(sol[j]) for j, (q, _) in enumerate(vB)})

print("     rows published by each instrument:")
print("       mg-e8b8  T1b2      : %d rows" % len(t1b2))
print("       mg-2060  B1b       : %d rows" % len(b1b))
print("       mg-a218  this file : %d rows" % len(mine_rows))
allkeys = set(t1b2) | set(b1b) | set(mine_rows)
agree3 = 0
for k in sorted(allkeys):
    vals = {"T1b2": t1b2.get(k), "B1b": b1b.get(k), "a218": mine_rows.get(k)}
    present = {n: v for n, v in vals.items() if v is not None}
    if len(present) < 3:
        FIND.append("row L(%d,%d) at beta=%d is published by only %s"
                    % (k[1], k[2], k[0], sorted(present)))
        continue
    if len(set(map(str, present.values()))) == 1:
        agree3 += 1
    else:
        FIND.append("row L(%d,%d) at beta=%d DISAGREES across instruments: %s"
                    % (k[1], k[2], k[0], present))
print("     rows on which all THREE instruments agree exactly (dimension and every "
      "edge): %d, population: the %d distinct (beta,n,p) rows published by any of "
      "the three" % (agree3, len(allkeys)))
print("     -> the repair's 'agrees ROW FOR ROW with mg-2060's B1a/B1b' is "
      "%s, and this audit is the third instrument"
      % ("CONFIRMED" if agree3 == len(allkeys) else "NOT CONFIRMED"))
print()

print("-" * 74)
print("SELF-ERRORS: %d, population: the %d character solves this script performs"
      % (len(SELF), len(mine_rows)))
for s in SELF:
    print("   SELF-ERROR: " + s)
print("FINDINGS: %d, population: the %d (parameter-pair, level) set-vs-count cells "
      "and the %d cross-instrument rows" % (len(FIND), cells_examined, len(allkeys)))
for f in FIND:
    print("   FINDING: " + f)
print("TOTAL BAD: %d" % (len(SELF) + len(FIND)))
sys.exit(1 if (SELF or FIND) else 0)
