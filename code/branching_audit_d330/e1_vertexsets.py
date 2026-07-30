"""E1 --- IS THE REPAIRED COLUMN A SET, OR A RENDERING OF ONE?

mg-d330, on the mg-13b2 repair.  The primary technical target of my brief:

    "Verify two genuinely different vertex sets cannot present as equal in the
     repaired column.  Construct such a pair and confirm the column
     distinguishes them --- this is the deletion test's cousin and it is the
     only thing that settles it."

    "If a count column was retained beside the set column, flag it."

    "Do not accept a hash without checking it is over the SET and not over a
     rendering of it."

Exit 0 iff SELF-ERRORS == 0 AND FINDINGS == 0.  Both are printed separately
and every count names its population.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

from kern_d330 import vertex_set, dims_render, pairs_render, cell_dims  # noqa

DOC = os.path.join(ROOT, "docs",
                   "OneThird-Bratteli-Path-Algebras-Where-This-Lives.md")
TARGET_DIR = os.path.join(ROOT, "code", "branching_locate_db09")
T1 = os.path.join(TARGET_DIR, "t1_tl.py")
O1 = os.path.join(TARGET_DIR, "out_t1_tl.txt")

BETAS = [3, 2, 1, 0]
NMAX = 6

SELF, FIND = [], []


def selferr(m):
    SELF.append(m)
    print("   SELF-ERROR: " + m)


def finding(m):
    FIND.append(m)
    print("   FINDING: " + m)


print("=" * 74)
print("E1  THE VERTEX COLUMN: A SET, OR A RENDERING OF ONE?")
print("=" * 74)
print("A FOURTH instrument.  kern_d330.py builds Temperley-Lieb half-diagrams,")
print("the cellular form and dim L(n,p) = rank of the Gram matrix over Q from")
print("the combinatorial definition, sharing no code with mg-db09's kerndb09,")
print("mg-2060's kern2060 or mg-a218's kern_a218.")
print()

# ---------------------------------------------------------------------------
# (i)  the vertex sets, measured here
# ---------------------------------------------------------------------------
print("-" * 74)
print("(i) THE VERTEX SETS, MEASURED AFRESH")
print("-" * 74)
mine = {}
for b in BETAS:
    for n in range(1, NMAX + 1):
        mine[(n, b)] = vertex_set(n, b)
for b in BETAS:
    print("   beta = %d   %s"
          % (b, "  ".join(pairs_render(mine[(n, b)]) for n in range(1, NMAX + 1))))
print()
print("   population: the %d (beta, n) cells --- %d parameters x %d levels."
      % (len(BETAS) * NMAX, len(BETAS), NMAX))
print()

# tie to the dim (+)End column, which two other routes compute
print("   sum over the n = 6 vertices of (dim L)^2, against section 0's")
print("   'dim (+)_lambda End(L_lambda)' column:")
WANT_END = {3: 132, 2: 132, 1: 99, 0: 42}
for b in BETAS:
    s = sum(d * d for (p, d) in mine[(6, b)])
    ok = (s == WANT_END[b])
    print("     beta = %d : %d   document says %d   %s"
          % (b, s, WANT_END[b], "agree" if ok else "DISAGREE"))
    if not ok:
        finding("sum of squares at beta=%d is %d, the document's (+)End column "
                "says %d" % (b, s, WANT_END[b]))
print()

# ---------------------------------------------------------------------------
# (ii) the document's column, read at the site and compared
# ---------------------------------------------------------------------------
print("-" * 74)
print("(ii) SECTION 0'S COLUMN, READ AT THE SITE")
print("-" * 74)
doc = open(DOC, encoding="utf-8").read()
row_re = re.compile(
    r"^\|\s*(\d)\s*\|\s*132\s*\|.*?\|\s*`((?:\[[\d,]+\]\s*)+)`\s*\|\s*[^|]*\|\s*$",
    re.M)
doc_rows = {}
for m in row_re.finditer(doc):
    doc_rows[int(m.group(1))] = [g for g in re.findall(r"\[([\d,]+)\]", m.group(2))]
if len(doc_rows) != 4:
    selferr("parsed %d of the 4 section-0 rows" % len(doc_rows))
for b in BETAS:
    got = doc_rows.get(b)
    want = [dims_render(mine[(n, b)])[1:-1] for n in range(1, NMAX + 1)]
    ok = (got == want)
    print("   beta = %d  document %s" % (b, got))
    print("             measured %s   %s" % (want, "agree" if ok else "DISAGREE"))
    if got is not None and not ok:
        finding("section 0's row for beta=%d prints %s; measured %s"
                % (b, got, want))
print()

# ---------------------------------------------------------------------------
# (iii) IS THE RENDERING INJECTIVE?  the target checks 36 cells; check them all
# ---------------------------------------------------------------------------
print("-" * 74)
print("(iii) IS THE COLUMN'S RENDERING INJECTIVE ON THE SETS THAT OCCUR?")
print("-" * 74)
print("   The column prints dimensions alone.  That is a FUNCTION of the vertex")
print("   set, not the set.  It reports the set faithfully exactly when it is")
print("   injective.  T1b2 checks this on the 36 SAME-LEVEL (parameter-pair,")
print("   level) cells.  Checked here over EVERY unordered pair of the 24")
print("   measured cells, across levels as well as across parameters.")
print()
cells = [(n, b) for b in BETAS for n in range(1, NMAX + 1)]
pairs = [(x, y) for i, x in enumerate(cells) for y in cells[i + 1:]]
collisions = [(x, y) for (x, y) in pairs
              if dims_render(mine[x]) == dims_render(mine[y]) and mine[x] != mine[y]]
print("   pairs compared: %d, population: every unordered pair of the %d cells"
      % (len(pairs), len(cells)))
print("   pairs where the RENDERING agrees and the SET does not: %d"
      % len(collisions))
for (x, y) in collisions:
    finding("the dimensions-only column shows (n=%d,beta=%d) and (n=%d,beta=%d) "
            "as equal while the vertex sets differ: %s vs %s"
            % (x[0], x[1], y[0], y[1], pairs_render(mine[x]), pairs_render(mine[y])))
same_level = [(x, y) for (x, y) in pairs if x[0] == y[0]]
print("   of which same-level pairs (the target's own population): %d"
      % len(same_level))
cnt_eq_set_ne = [(x, y) for (x, y) in same_level
                 if len(mine[x]) == len(mine[y]) and mine[x] != mine[y]]
print("   same-level pairs where the COUNT agrees and the SET does not: %d of %d"
      % (len(cnt_eq_set_ne), len(same_level)))
if len(cnt_eq_set_ne) != 10:
    finding("mg-a218 and T1b2 both report 10 of 36 count-agrees-set-differs "
            "cells; this instrument measures %d" % len(cnt_eq_set_ne))
print()
print("   WHY THE RENDERING IS INJECTIVE HERE, and it is a SIDE CONDITION and")
print("   not a property of the rendering: the labels p carried by the live")
print("   vertices are an unbroken run from 0 at every one of the %d cells, so"
      % len(cells))
print("   the dimension list determines the labels.  Measured:")
gaps = [c for c in cells if [p for (p, d) in mine[c]] != list(range(len(mine[c])))]
print("     cells whose labels are NOT an unbroken run from 0: %d of %d"
      % (len(gaps), len(cells)))
if gaps:
    finding("the dimensions-only column is ambiguous at %s" % (gaps,))
print()

# ---------------------------------------------------------------------------
# (iv) THE CONSTRUCTED PAIR --- the thing my brief says settles it
# ---------------------------------------------------------------------------
print("-" * 74)
print("(iv) TWO GENUINELY DIFFERENT VERTEX SETS, CONSTRUCTED")
print("-" * 74)
A = ((0, 1), (1, 1))
B = ((0, 1), (2, 1))
print("   A = %s   --- two irreducibles, labelled p = 0 and p = 1" % pairs_render(A))
print("   B = %s   --- two irreducibles, labelled p = 0 and p = 2" % pairs_render(B))
print()
print("   These are DIFFERENT SETS: B's second vertex is L(n,2) and A's is")
print("   L(n,1), which are different modules of the same dimension.  They are")
print("   the pair a set column must separate and a count column cannot.")
print()
print("   count of A            : %d" % len(A))
print("   count of B            : %d   -> a COUNT column shows them EQUAL" % len(B))
print("   column rendering of A : %s" % dims_render(A))
print("   column rendering of B : %s   -> the REPAIRED COLUMN ALSO SHOWS THEM"
      % dims_render(B))
print("                                    EQUAL.")
print("   full labelled form  A : %s" % pairs_render(A))
print("   full labelled form  B : %s   -> only this separates them"
      % pairs_render(B))
print()
print("   SO THE COLUMN DOES NOT SEPARATE ARBITRARY VERTEX SETS.  What it")
print("   separates is the vertex sets that satisfy the side condition in")
print("   (iii).  Whether that is enough turns entirely on whether the side")
print("   condition is GATED --- which is (v).  A rendering with an unchecked")
print("   side condition is a count in disguise; a rendering with a checked")
print("   one is not.")
print()

# ---------------------------------------------------------------------------
# (v)  THE DELETION TEST --- is the side condition's guard load-bearing?
# ---------------------------------------------------------------------------
print("-" * 74)
print("(v) THE DELETION TEST ON THE GUARD")
print("-" * 74)
print("   B is injected into t1_tl.py's own `vtx` at (n=2, beta=3) in a scratch")
print("   copy --- nothing in the tree is touched.  The injected cell renders")
print("   as [1,1], exactly as the real one does, so the column does not move")
print("   and only a guard can see it.")
print()

ANCHOR = "        vtx[(n, b)] = [(p, d) for (p, d, c) in simples[(n, b)] if d > 0]\n"
INJECT = ANCHOR + "vtx[(2, 3)] = [(0, 1), (2, 1)]  # mg-d330 adversarial injection\n"
GUARD_RUN = '            bad("the live labels at (n,beta)=(%d,%s) are %s, not an unbroken "'
GUARD_COL = '                bad("the dimensions-only abbreviation collides at "'
NOOP = "(lambda *a: None)("


def run_variant(label, patches):
    """Copy the target instrument, apply textual patches, run t1_tl.py."""
    tmp = tempfile.mkdtemp(prefix="d330_")
    dst = os.path.join(tmp, "inst")
    shutil.copytree(TARGET_DIR, dst)
    path = os.path.join(dst, "t1_tl.py")
    src = open(path, encoding="utf-8").read()
    for (old, new) in patches:
        if old not in src:
            selferr("patch target absent for variant %r: %r" % (label, old[:50]))
            shutil.rmtree(tmp)
            return None, None
        src = src.replace(old, new, 1)
    open(path, "w", encoding="utf-8").write(src)
    p = subprocess.run([sys.executable, "-u", "t1_tl.py"], cwd=dst,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.stdout.decode("utf-8", "replace")
    shutil.rmtree(tmp)
    m = re.search(r"^TOTAL BAD: (\d+)$", out, re.M)
    return (int(m.group(1)) if m else None), out


baseline_bad, baseline_out = run_variant("baseline", [])
print("   [baseline]           unpatched t1_tl.py                TOTAL BAD: %s"
      % baseline_bad)
if baseline_bad != 0:
    selferr("the unpatched target does not run clean here; TOTAL BAD %s"
            % baseline_bad)

inj_bad, inj_out = run_variant("inject B", [(ANCHOR, INJECT)])
print("   [B injected]         guards intact                     TOTAL BAD: %s"
      % inj_bad)
run_fired = inj_out is not None and "not an unbroken \nrun from 0" not in inj_out \
    and "are [0, 2], not an unbroken" in inj_out
col_fired = inj_out is not None and "dimensions-only abbreviation collides at" in inj_out
print("        the run-from-0 guard names the injected cell : %s"
      % ("YES" if run_fired else "no"))
print("        the collision guard fires                    : %s"
      % ("YES" if col_fired else "no"))
if inj_bad in (None, 0):
    finding("the repaired column presents two different vertex sets as equal "
            "and NOTHING in the target instrument goes red: TOTAL BAD %s"
            % inj_bad)
if not run_fired:
    finding("the run-from-0 guard does not name the injected cell, so the side "
            "condition the dimensions-only column rests on is not gated")
if not col_fired:
    finding("the dimensions-only collision guard does not fire on a "
            "constructed collision")

del_bad, del_out = run_variant("inject B, both guards deleted",
                               [(ANCHOR, INJECT),
                                (GUARD_RUN, GUARD_RUN.replace("bad(", NOOP, 1)),
                                (GUARD_COL, GUARD_COL.replace("bad(", NOOP, 1))])
print("   [B injected, guards deleted]                          TOTAL BAD: %s"
      % del_bad)
print()
print("   THE TEST: the guards are load-bearing iff injecting B is RED with")
print("   them and GREEN without them.  Anything else means something other")
print("   than the guard caught it, or nothing did.")
if inj_bad and del_bad == 0:
    print("   RESULT: RED %d -> GREEN 0.  The two guards are the whole of what"
          % inj_bad)
    print("   stands between the delivered column and a false equality, and")
    print("   they are load-bearing.")
elif del_bad:
    print("   RESULT: still RED at %s with both guards deleted --- something"
          % del_bad)
    print("   ELSE also catches it, which is stronger, and is reported as such.")
else:
    finding("the deletion test does not separate: injected TOTAL BAD %s, "
            "guards-deleted TOTAL BAD %s" % (inj_bad, del_bad))
print()

# ---------------------------------------------------------------------------
# (vi) WAS A COUNT COLUMN RETAINED?
# ---------------------------------------------------------------------------
print("-" * 74)
print("(vi) IS A COUNT COLUMN RETAINED BESIDE THE SET COLUMN?")
print("-" * 74)
hdr = re.search(r"^\|\s*`β`\s*\|(.*)\|\s*$", doc, re.M)
header_cells = [c.strip() for c in hdr.group(1).split("|")] if hdr else []
print("   section 0's four-row table, its columns:")
for c in ["`β`"] + header_cells:
    print("      %s" % c)
count_hdrs = [c for c in header_cells
              if "#" in c and "irreducible" in c.lower()]
print("   columns that are a count of irreducibles: %d" % len(count_hdrs))
if count_hdrs:
    finding("a count-of-irreducibles column stands beside the set column: %s"
            % count_hdrs)
OLDCOUNT = ["1, 2, 2, 3, 3, 4", "1,2,2,3,3,4", "1, 1, 2, 2, 3, 3"]
print()
print("   the withdrawn count rendering, swept over the delivered document:")
for needle in OLDCOUNT:
    hits = [i + 1 for (i, l) in enumerate(doc.splitlines()) if needle in l]
    print("      %-20r %d line(s) %s" % (needle, len(hits), hits))
    for ln in hits:
        # WIDENED ONCE, and the widening is recorded here with its reason
        # rather than in a commit message, per this repo's convention
        # (mg-a218's c3 and c4 did the same).  The window was the line
        # carrying the rendering.  Section 8's own repair note wraps: the
        # marker "It printed" sits at the END of the line ABOVE the one
        # carrying `1,2,2,3,3,4`, so a line-local window scored a correctly
        # marked historical quotation as a live assertion.  The window is now
        # the line and its predecessor.  This is a real loosening --- a marked
        # line followed by an unmarked assertion would now pass --- and it is
        # why e5's seam sweep exists and this check does not replace it.
        lines = doc.splitlines()
        window = " ".join(lines[max(0, ln - 2):ln])
        marked = any(w in window for w in
                     ("printed", "used to", "old column", "would have",
                      "WITHDRAWN", "CORRECTED", "mg-a218", "mg-13b2"))
        if not marked:
            finding("the withdrawn count rendering %r stands unmarked at "
                    "%s:%d" % (needle, os.path.basename(DOC), ln))
print()
print("   the same sweep over the target instrument's committed output:")
o1 = open(O1, encoding="utf-8").read()
for needle in ["1, 2, 2, 3, 3, 4"]:
    hits = [(i + 1, l) for (i, l) in enumerate(o1.splitlines()) if needle in l]
    print("      %-20r %d line(s) in out_t1_tl.txt" % (needle, len(hits)))
    for (ln, l) in hits:
        print("         %d: %s" % (ln, l.strip()))
print("   NOTE, not scored as a finding: the sequence survives in T1b2 (i) as")
print("   'the number of CELL modules at level n', which is a different object")
print("   (cell modules, not irreducibles), is parameter-free, and says so on")
print("   the same line.  It is recorded because it is the literal sequence the")
print("   withdrawn column printed, ten lines under the vertex sets.")
print()

# ---------------------------------------------------------------------------
# (vii) IS ANY FIGURE IN THIS COLUMN A DIGEST?
# ---------------------------------------------------------------------------
print("-" * 74)
print("(vii) NO DIGEST STANDS IN FOR THE SET")
print("-" * 74)
print("   My brief: do not accept a hash without checking it is over the SET")
print("   and not over a rendering of it.")
t1src = open(T1, encoding="utf-8").read()
t5src = open(os.path.join(TARGET_DIR, "t5_labels.py"), encoding="utf-8").read()
for (name, src) in [("t1_tl.py", t1src), ("t5_labels.py", t5src)]:
    uses = [l.strip() for l in src.splitlines()
            if re.search(r"hashlib|sha256|md5|\bhash\(", l)]
    print("   %-14s digest calls: %d" % (name, len(uses)))
    for u in uses:
        print("        %s" % u)
print("   The vertex column carries the dimensions themselves; no digest")
print("   stands between a reader and the measurement.  The only digests in")
print("   the target are sha256 over WHOLE FILE CONTENTS in t5's")
print("   `unchanged_since`, which is a file-identity check and not a")
print("   rendering of a set.  Nothing to accept or reject here.")
print()

print("-" * 74)
print("SELF-ERRORS: %d, population: the parses and scratch runs this script needs"
      % len(SELF))
print("FINDINGS: %d, population: the %d measured cells, the %d rendering pairs, "
      "the constructed pair, the deletion test, and section 0's table columns"
      % (len(FIND), len(cells), len(pairs)))
for f in FIND:
    print("   FINDING: " + f)
print("TOTAL BAD: %d" % (len(SELF) + len(FIND)))
sys.exit(1 if (SELF or FIND) else 0)
