"""c1_branching.py -- THE PRIMARY TARGET.

mg-e8b8's repair says the invariant is now "MEASURED, at EVERY parameter, in
mg-db09's own instrument" (T1b2).  This script measures it AGAIN, on a third
instrument that shares no code with either, and compares EVERY CELL.

"Every cell" is meant literally:
  * the vertex set at every level of every parameter -- as a SET OF LABELLED
    VERTICES (p, dim L(n,p)), not as a count;
  * the restriction multiplicity [L(n,p) : L(n-1,q)] for EVERY ordered pair
    (p, q) at every level of every parameter, including the zeros.

Then it parses mg-e8b8's committed out_t1_tl.txt and checks the target's
printed numbers cell by cell against mine.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import os
import re
import sys
from fractions import Fraction

from kern_a218 import TL, catalan, diagrams, embed, solve_exact

BETAS = [3, 2, 1, 0]
NMAX = 6
TARGET_OUT = os.path.join(os.path.dirname(__file__), "..",
                          "branching_locate_db09", "out_t1_tl.txt")

SELF = []
FIND = []


def selferr(m):
    SELF.append(m)


def finding(m):
    FIND.append(m)


print("=" * 74)
print("c1  THE BRANCHING GRAPH, MEASURED IN EVERY CELL, ON A THIRD INSTRUMENT")
print("=" * 74)
print("""
Vershik-Okounkov's definition, which is the definition in play because it is
the one the target document quotes: at level n the VERTICES are the
irreducible modules of the n-th algebra and the EDGES are the restriction
multiplicities.  Graham-Lehrer: the irreducibles of TL_n(beta) are the
non-zero L(n,p) = V(n,p)/rad<,>.

Multiplicities are recovered from characters -- in characteristic 0 the
trace functions of pairwise non-isomorphic simples are linearly independent
-- and UNIQUENESS, INTEGRALITY, NON-NEGATIVITY and
sum_q m_q dim L(n-1,q) = dim L(n,p) are all checked here, not assumed.
""")

# ---------------------------------------------------------------------------
# measure
# ---------------------------------------------------------------------------

algebras = {}
for beta in BETAS:
    for n in range(1, NMAX + 1):
        algebras[(n, beta)] = TL(n, beta)

mine_vertices = {}   # (beta, n) -> [(p, dim)]
mine_edges = {}      # (beta, n) -> {(p,q): m}

for beta in BETAS:
    for n in range(1, NMAX + 1):
        mine_vertices[(beta, n)] = algebras[(n, beta)].vertices()

for beta in BETAS:
    for n in range(2, NMAX + 1):
        A, B = algebras[(n, beta)], algebras[(n - 1, beta)]
        Dsub = diagrams(n - 1)
        vB = B.vertices()
        # character table of the level-(n-1) simples on the diagram basis
        chi = [[B.trace_on_L(d, q) for d in Dsub] for (q, _) in vB]
        chiT = [[chi[j][i] for j in range(len(vB))] for i in range(len(Dsub))]
        edges = {}
        for (p, dimLp) in mine_vertices[(beta, n)]:
            target = [A.trace_on_L(embed(d, n), p) for d in Dsub]
            sol, unique = solve_exact(chiT, target)
            if sol is None:
                selferr("no solution for the character of L(%d,%d) at beta=%d"
                        % (n, p, beta))
                continue
            if not unique:
                selferr("multiplicities NOT UNIQUE for L(%d,%d) at beta=%d"
                        % (n, p, beta))
            for j, (q, dimLq) in enumerate(vB):
                m = sol[j]
                if m.denominator != 1:
                    selferr("multiplicity [L(%d,%d):L(%d,%d)] at beta=%d is not an "
                            "integer: %s" % (n, p, n - 1, q, beta, m))
                if m < 0:
                    selferr("multiplicity [L(%d,%d):L(%d,%d)] at beta=%d is negative: %s"
                            % (n, p, n - 1, q, beta, m))
                edges[(p, q)] = int(m)
            tot = sum(edges[(p, q)] * dq for (q, dq) in vB)
            if tot != dimLp:
                selferr("dimension identity fails for L(%d,%d) at beta=%d: "
                        "sum m_q dim L = %d, dim L = %d" % (n, p, beta, tot, dimLp))
        mine_edges[(beta, n)] = edges

# ---------------------------------------------------------------------------
# print: EVERY CELL
# ---------------------------------------------------------------------------

print("(i)  THE VERTEX SET AT EVERY LEVEL OF EVERY PARAMETER")
print("     printed as the SET of labelled vertices p:dim L(n,p), not as a count")
print()
for beta in BETAS:
    print("  beta = %d" % beta)
    for n in range(1, NMAX + 1):
        vs = mine_vertices[(beta, n)]
        print("    n=%d  count %d   set { %s }"
              % (n, len(vs), ", ".join("p=%d:dim %d" % (p, d) for p, d in vs)))
    print()

print("(ii) THE EDGES -- [L(n,p) restricted to TL_{n-1} : L(n-1,q)]")
print("     EVERY ordered pair (p,q), zeros included")
print()
mult2 = []
for beta in BETAS:
    print("  ---- beta = %d ----" % beta)
    for n in range(2, NMAX + 1):
        vA = mine_vertices[(beta, n)]
        vB = mine_vertices[(beta, n - 1)]
        for (p, dp) in vA:
            cells = "  ".join("[L(%d,%d)]=%d" % (n - 1, q, mine_edges[(beta, n)][(p, q)])
                              for (q, dq) in vB)
            flag = ""
            for (q, dq) in vB:
                mval = mine_edges[(beta, n)][(p, q)]
                if mval >= 2:
                    mult2.append((beta, n, p, q, mval))
                    flag = "   <-- MULTIPLICITY %d" % max(
                        mine_edges[(beta, n)][(p, qq)] for (qq, _) in vB)
            print("    L(%d,%d) dim %d  ->  %s%s" % (n, p, dp, cells, flag))
        mf = all(v <= 1 for (pp, qq), v in mine_edges[(beta, n)].items())
    allmf = all(v <= 1 for nn in range(2, NMAX + 1)
                for v in mine_edges[(beta, nn)].values())
    ss = sum(d * d for _, d in mine_vertices[(beta, NMAX)])
    print("    multiplicity-free at beta = %d over 2 <= n <= %d ?  %s"
          "     (sum over the %d vertices at n = %d of (dim L)^2: %d)"
          % (beta, NMAX, "YES" if allmf else "NO",
             len(mine_vertices[(beta, NMAX)]), NMAX, ss))
    print()

print("  the multiplicity-2 edges, over the population of all %d (beta,n,p,q) cells "
      "with beta in {3,2,1,0} and 2 <= n <= 6:"
      % sum(len(mine_edges[(b, n)]) for b in BETAS for n in range(2, NMAX + 1)))
for (beta, n, p, q, m) in mult2:
    print("    beta=%d  [L(%d,%d) : L(%d,%d)] = %d" % (beta, n, p, n - 1, q, m))
print()

# ---------------------------------------------------------------------------
# compare against the target's committed T1b2
# ---------------------------------------------------------------------------

print("(iii) EVERY CELL, AGAINST mg-e8b8's COMMITTED out_t1_tl.txt")
print()

txt = open(TARGET_OUT).read()
seg = txt.split("T1b2  THE BRANCHING GRAPH AS VERSHIK-OKOUNKOV DEFINE IT")[1]
seg = seg.split("T1c  SEMISIMPLICITY")[0]

# the vertex cells.  TWO FORMS, and which one is present is reported.
#
# WIDENED ON A RE-RUN (mg-58da), and the note is here rather than in a commit
# message, per this repo's convention.  This block used to accept only the
# COUNT form -- a beta digit followed by six integers on one line -- which is
# what T1b2 (i) carried when this audit was taken at 286d5030.  mg-13b2
# replaced that table with the labelled vertex SETS, on THIS SCRIPT'S OWN
# finding X1, which said the count was the defect.  c2_vertexsets.py was
# widened to accept either form at the same time.  This one was not, and the
# consequence was measured by mg-d330: on a re-run against the repaired tree
# it reported 24 FINDINGS reading 'target ?' -- one per vertex cell -- because
# `tgt_counts.get(beta, [None] * 6)[n - 1] != mine_c` compares None against an
# integer and None differs from every integer.  ABSENCE WAS RENDERED AS
# DISAGREEMENT, and the instrument accused the target of being wrong where its
# own parser had gone blind.  mg-58da established all 24 as parser artifacts:
# 0 confirmed, 0 unknown, and the target agreeing with this script's own
# measurement label for label at 24 of 24 cells.
#
# Three things change, and each is load-bearing:
#
#   1. the SET form is read, and preferred when present.  It is strictly more
#      information than the count -- the count is len(set) -- so the cells are
#      now compared as LABELLED SETS wherever the target offers them.  That is
#      a stronger comparison than the one this audit originally made, not a
#      weaker one.
#   2. the COUNT form is still read, so a re-run against the target as it
#      stood at 286d5030 still compares all 24 cells and still agrees.
#   3. A CELL THE TARGET DOES NOT STATE IS A SELF-ERROR, NOT A FINDING.  This
#      is the actual defect: an instrument that cannot read its target must
#      say so about ITSELF.  A finding is a statement about the target, and
#      "I could not find it" is not one.
#
# The committed out_c1_branching.txt is NOT regenerated: it is the record of
# what this audit found at 286d5030, not a live gate.  That is the call
# mg-a318 made for mg-8a5c and mg-13b2 made for c2 here, and g1 of
# code/branching_audit_58da re-runs this script at 286d5030 and confirms the
# committed file byte for byte.
tgt_counts = {}
for line in seg.splitlines():
    m = re.match(r"\s*(\d)\s+((?:\d+\s+){5}\d+)\s*$", line)
    if m:
        b = int(m.group(1))
        if b in BETAS and b not in tgt_counts:
            tgt_counts[b] = [int(x) for x in m.group(2).split()]

# the SET form: a 'beta = <b>' header and then 'n=<k>  [p:d,p:d,...]' rows
tgt_sets = {}
_cur = None
for line in seg.splitlines():
    m = re.match(r"\s*beta = (\d+)\s*$", line)
    if m:
        _cur = int(m.group(1))
        continue
    m = re.match(r"\s*n=(\d+)\s+\[([\d:,]*)\]\s*$", line)
    if m and _cur is not None:
        _verts = []
        if m.group(2):
            for _piece in m.group(2).split(","):
                _p, _d = _piece.split(":")
                _verts.append((int(_p), int(_d)))
        tgt_sets[(_cur, int(m.group(1)))] = _verts

vform = "SET" if tgt_sets else ("COUNT" if tgt_counts else "NEITHER")

# edges
tgt_edges = {}
tgt_dims = {}
cur = None
for line in seg.splitlines():
    m = re.match(r"\s*---- beta = (\d+) ----", line)
    if m:
        cur = int(m.group(1))
        continue
    m = re.match(r"\s*L\((\d+),(\d+)\) dim (\d+)\s+->\s+(.*)$", line)
    if m and cur is not None:
        n, p, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        tgt_dims[(cur, n, p)] = d
        for mm in re.finditer(r"\[L\((\d+),(\d+)\)\]=(\d+)", m.group(4)):
            tgt_edges[(cur, n, p, int(mm.group(2)))] = int(mm.group(3))

ncells_v = 0
nblind_v = 0
for beta in BETAS:
    for n in range(1, NMAX + 1):
        mine_v = mine_vertices[(beta, n)]
        mine_c = len(mine_v)
        if (beta, n) in tgt_sets:
            tv = tgt_sets[(beta, n)]
            if len(tv) != mine_c:
                finding("vertex COUNT disagrees at beta=%d n=%d: target %d, "
                        "mine %d" % (beta, n, len(tv), mine_c))
            elif tv != mine_v:
                finding("vertex SET disagrees at beta=%d n=%d: target %s, "
                        "mine %s" % (beta, n, tv, mine_v))
            ncells_v += 1
        elif beta in tgt_counts:
            if tgt_counts[beta][n - 1] != mine_c:
                finding("vertex COUNT disagrees at beta=%d n=%d: target %s, "
                        "mine %d" % (beta, n, tgt_counts[beta][n - 1], mine_c))
            ncells_v += 1
        else:
            # NOT a finding.  The target has not disagreed with anything; this
            # script has failed to read it, and that is a fact about this
            # script.  See the widening note above.
            selferr("I cannot read a vertex cell for beta=%d n=%d out of the "
                    "target in either the SET or the COUNT form; the cell is "
                    "NOT compared and is NOT counted as compared"
                    % (beta, n))
            nblind_v += 1
print("     vertex cells: %d cells compared, %d not compared because this "
      "script could not read them; population: every (beta,n) with beta in "
      "{3,2,1,0} and 1 <= n <= 6, which is 24. Form read: %s"
      % (ncells_v, nblind_v, vform))

ncells_d = 0
for (beta, n, p), d in sorted(tgt_dims.items()):
    mine = dict(mine_vertices[(beta, n)]).get(p)
    if mine != d:
        finding("dim L(%d,%d) at beta=%d disagrees: target %d, mine %s"
                % (n, p, beta, d, mine))
    ncells_d += 1
# and the other way: every vertex I measure must be printed by the target
for beta in BETAS:
    for n in range(2, NMAX + 1):
        for (p, d) in mine_vertices[(beta, n)]:
            if (beta, n, p) not in tgt_dims:
                finding("I measure a vertex the target does not print: "
                        "L(%d,%d) dim %d at beta=%d" % (n, p, d, beta))
print("     vertex dimensions: %d cells compared, population: every L(n,p) the "
      "target prints in T1b2, 2 <= n <= 6, plus every vertex I measure" % ncells_d)

ncells_e = 0
for beta in BETAS:
    for n in range(2, NMAX + 1):
        for (p, q), m in sorted(mine_edges[(beta, n)].items()):
            t = tgt_edges.get((beta, n, p, q))
            if t is None:
                finding("target prints no cell for [L(%d,%d):L(%d,%d)] at beta=%d"
                        % (n, p, n - 1, q, beta))
            elif t != m:
                finding("[L(%d,%d):L(%d,%d)] at beta=%d disagrees: target %d, mine %d"
                        % (n, p, n - 1, q, beta, t, m))
            ncells_e += 1
for k in tgt_edges:
    beta, n, p, q = k
    if (p, q) not in mine_edges[(beta, n)]:
        finding("target prints a cell I do not measure: [L(%d,%d):L(%d,%d)] beta=%d"
                % (n, p, n - 1, q, beta))
print("     edge multiplicities: %d cells compared, population: every ordered pair "
      "(p,q) of vertices at consecutive levels, every beta in {3,2,1,0}, "
      "2 <= n <= 6" % ncells_e)

# the four dim (+) End figures the document quotes
print()
print("     the four figures in the document's own four-row table:")
for beta in BETAS:
    ss = sum(d * d for _, d in mine_vertices[(beta, NMAX)])
    print("       beta=%d   dim TL_6 = %d   sum_lambda dim End(L_lambda) = %d"
          % (beta, catalan(NMAX), ss))
doc_table = {3: 132, 2: 132, 1: 99, 0: 42}
for beta in BETAS:
    ss = sum(d * d for _, d in mine_vertices[(beta, NMAX)])
    if ss != doc_table[beta]:
        finding("dim sum End(L) at beta=%d n=6 disagrees: document %d, mine %d"
                % (beta, doc_table[beta], ss))

# the five multiplicity-2 edges the document names, by name
print()
doc_named = [(1, 4, 1, 3, 0), (1, 6, 2, 5, 1), (0, 3, 1, 2, 0), (0, 5, 1, 4, 0),
             (0, 5, 2, 4, 1)]
print("     the five multiplicity-2 edges the document names, checked one by one:")
for (beta, n, p, nm1, q) in doc_named:
    got = mine_edges[(beta, n)].get((p, q))
    ok = got == 2
    print("       beta=%d  [L(%d,%d) : L(%d,%d)]  document says 2, mine says %s   %s"
          % (beta, n, p, n - 1, q, got, "agree" if ok else "DISAGREE"))
    if not ok:
        finding("named multiplicity-2 edge [L(%d,%d):L(%d,%d)] at beta=%d is %s, "
                "not 2" % (n, p, n - 1, q, beta, got))
mine_named = set((b, n, p, q) for (b, n, p, q, m) in mult2)
doc_named_set = set((b, n, p, q) for (b, n, p, _, q) in doc_named)
extra = mine_named - doc_named_set
if extra:
    finding("I measure multiplicity >= 2 at cells the document does not name: %s"
            % sorted(extra))
print("     multiplicity-2 cells I measure that the document does not name: %d, "
      "population: all %d (beta,n,p,q) cells" % (len(extra), ncells_e))

print()
print("-" * 74)
print("SELF-ERRORS: %d, population: every uniqueness/integrality/non-negativity/"
      "dimension check on the %d character solves in this script, PLUS the 24 "
      "vertex cells this script attempts to read out of the target -- a cell "
      "it cannot read is this script's failure and is booked here, not as a "
      "finding against the target (mg-58da)"
      % (len(SELF), sum(len(mine_vertices[(b, n)]) for b in BETAS
                        for n in range(2, NMAX + 1))))
for s in SELF:
    print("   SELF-ERROR: " + s)
print("FINDINGS: %d, population: the %d vertex cells (read as %s), %d "
      "vertex-dimension cells and %d edge cells COMPARED above -- %d cells in "
      "total; the %d vertex cells this script could not read are in the "
      "SELF-ERROR channel above and are not in this population"
      % (len(FIND), ncells_v, vform, ncells_d, ncells_e,
         ncells_v + ncells_d + ncells_e, nblind_v))
for f in FIND:
    print("   FINDING: " + f)
print("TOTAL BAD: %d" % (len(SELF) + len(FIND)))
sys.exit(1 if (SELF or FIND) else 0)
