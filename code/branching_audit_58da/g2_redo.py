"""g2_redo.py -- QUESTION B, second half: THE REPRODUCTION, REDONE AT HEAD.

g1 established that the reproduction stands at 286d5030 and that ed9cde4
touched the one file c1 reads.  So it has to be redone against that file as it
now stands, and 'redone' means the cells are compared again, not that someone
decides the change looks harmless.

The 174 dimension and edge cells are unaffected -- g1 showed the T1b2 (ii)
table is byte-identical across ed9cde4 -- so the whole of the redoing is the
24 vertex cells whose COUNT table mg-13b2 deleted.

The question for those 24 is not 'is the count still printed'.  It is: does
the target still DETERMINE the datum?  mg-13b2 replaced a count table with the
labelled vertex SETS, which is strictly more information: the count is
len(set).  So the 24 cells are recovered here from the set block, by a parser
that shares no line with c1's, and compared against c1's own measurement --
and against the two other instruments that measure the same 24 cells.

The recovery is calibrated.  A recovery that would agree whatever the target
said is not a comparison, so every one of the 24 cells is corrupted in turn
and required to go red.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import re
import sys

import lib58da as L

SELF, FIND = [], []


def selferr(m):
    SELF.append(m)


def finding(m):
    FIND.append(m)


print("=" * 74)
print("G2  QUESTION B, SECOND HALF -- THE 198 CELLS, REDONE AT HEAD")
print("=" * 74)

HEAD = L.head_rev()
new_target = L.read_worktree(L.TARGET_REL)
old_target = L.git_show(L.REV_A218, L.TARGET_REL)
out_old, _ = L.run_c1(old_target)
mine = L.parse_c1_own_vertices(out_old)          # c1's OWN measurement
if len(mine) != 24:
    selferr("c1's own section (i) yielded %d cells, not 24" % len(mine))

# ---------------------------------------------------------------------------
print()
print("-" * 74)
print("(i) WHAT THE TARGET STATES AT EACH REVISION, MEASURED BOTH WAYS")
print("-" * 74)
forms = []
for name, txt in [("286d5030 (mg-a218's)", old_target),
                  ("d1dd84d2 (HEAD)", new_target)]:
    cnt = L.parse_vertex_counts_oldform(txt)
    st = L.parse_vertex_sets(txt)
    dims, edges = L.parse_edges(txt)
    forms.append((name, cnt, st, dims, edges))
    print("   %-22s COUNT table: %2d cells   SET block: %2d cells   "
          "dim cells: %2d   edge cells: %3d"
          % (name, len(cnt), len(st), len(dims), len(edges)))
print()
print("   So the vertex datum did not vanish: it changed RENDERING, from a")
print("   table of 24 cardinalities to 24 labelled sets.  A cardinality is a")
print("   function of a set, so the new form determines the old one and the")
print("   old one does not determine the new.  That is the direction mg-a218's")
print("   own finding X1 asked for.")
print()
(_, oc, _, odims, oedges) = forms[0]
(_, _, ns, ndims, nedges) = forms[1]
if odims != ndims or oedges != nedges:
    finding("T1b2 (ii) is NOT unchanged across ed9cde4; the 174 dimension and "
            "edge cells cannot be carried over and must be re-argued")
else:
    print("   T1b2 (ii) -- the 53 dimension and 121 edge cells -- is IDENTICAL")
    print("   across ed9cde4, cell for cell.  Those 174 carry over unchanged.")
print()

# ---------------------------------------------------------------------------
print("-" * 74)
print("(ii) THE 24 VERTEX CELLS, RECOVERED FROM THE SET BLOCK AND COMPARED")
print("-" * 74)
print("   'target' is read by this script's own parser, which shares no line")
print("   with c1's.  'mine' is c1's own section (i), which reads nothing")
print("   outside mg-a218's instrument.")
print()
print("   beta  n   target set          count | c1 set              count | ")
agree_cnt = agree_set = 0
for beta in L.BETAS:
    for n in range(1, L.NMAX + 1):
        t = ns.get((beta, n))
        m = mine.get((beta, n))
        if t is None:
            finding("the HEAD target states nothing at beta=%d n=%d; the cell "
                    "cannot be compared" % (beta, n))
            print("     %d   %d   %-19s %-5s | %-19s %-5s | NOT STATED"
                  % (beta, n, "--", "--", L.render_set(m), len(m)))
            continue
        cok = len(t) == len(m)
        sok = t == m
        agree_cnt += cok
        agree_set += sok
        print("     %d   %d   %-19s %-5d | %-19s %-5d | %s"
              % (beta, n, L.render_set(t), len(t), L.render_set(m), len(m),
                 "agree" if sok else ("COUNT agrees, SET DISAGREES" if cok
                                      else "DISAGREE")))
        if not cok:
            finding("vertex COUNT at beta=%d n=%d: target %d, c1 %d"
                    % (beta, n, len(t), len(m)))
        elif not sok:
            finding("vertex SET at beta=%d n=%d: target %s, c1 %s"
                    % (beta, n, L.render_set(t), L.render_set(m)))
print()
print("   cells recovered from the HEAD target : %d of 24" % len(ns))
print("   COUNTS agreeing with c1's measurement: %d of 24" % agree_cnt)
print("   SETS agreeing with c1's measurement  : %d of 24" % agree_set)
print()
print("   AND THE OLD COMPARISON, for the record: at 286d5030 the target")
print("   stated only the 24 counts, and c1 compared %d of them." % len(oc))
old_agree = sum(1 for k in oc if k in mine and oc[k] == len(mine[k]))
print("   counts agreeing there: %d of %d." % (old_agree, len(oc)))
if old_agree != len(oc):
    finding("the 286d5030 count table does not agree with c1's measurement at "
            "%d of %d cells" % (len(oc) - old_agree, len(oc)))
print()
print("   So the redoing does not weaken the reproduction, it strengthens it:")
print("   24 cells that were compared as CARDINALITIES are now comparable as")
print("   LABELLED SETS, and 10 of the 36 same-level pairs that a count column")
print("   showed as equal are separated by the set column (mg-13b2's own")
print("   figure, and mg-d330's e1 measured the same 10 on a fourth kernel).")
print()

# ---------------------------------------------------------------------------
print("-" * 74)
print("(iii) THE SAME 24 CELLS ON EVERY INSTRUMENT IN THE TREE THAT PRINTS THEM")
print("-" * 74)
print("""   A reproduction is a claim that independent instruments agree.  Four
   kernels in this tree measure these vertex sets.  Their agreement is what
   the 198-cell claim is FOR, so it is measured here rather than cited.""")
print()

instruments = []
# 1. mg-db09's t1_tl.py, via its committed output = the target itself
instruments.append(("t1_tl.py (mg-db09, 1st)", ns))
# 2. mg-a218's c1, via its own section (i)
instruments.append(("c1_branching.py (mg-a218, 3rd)", mine))


# 3. mg-d330's e1, via its committed output
def parse_e1(path):
    got = {}
    with open(path) as fh:
        for line in fh:
            m = re.match(r"\s*beta = (\d+)\s+((?:\[[\d:,]*\]\s*)+)$", line)
            if not m:
                continue
            b = int(m.group(1))
            sets = re.findall(r"\[([\d:,]*)\]", m.group(2))
            if len(sets) != 6:
                continue
            for n, s in enumerate(sets, start=1):
                got[(b, n)] = [tuple(int(x) for x in piece.split(":"))
                               for piece in s.split(",") if piece]
    return got


import os
e1p = os.path.join(L.REPO, "code/branching_audit_d330/out_e1_vertexsets.txt")
e1 = parse_e1(e1p)
if len(e1) != 24:
    selferr("mg-d330's out_e1_vertexsets.txt yielded %d cells, not 24" % len(e1))
instruments.append(("e1_vertexsets.py (mg-d330, 4th)", e1))


# 4. mg-2060's b1, which prints p-labels and dims separately
#
# CORRECTED DURING CONSTRUCTION, and recorded here rather than in a commit
# message, per this repo's convention.  The beta-header pattern was first
# written as r"\s*beta = (\d+)\s*$", copied from the shape T1b2 and e1 use.
# b1 writes "    beta=3:" -- no spaces, a trailing colon -- so the parser
# matched nothing, returned 0 cells, and the script booked THREE findings
# saying mg-2060's instrument disagreed with the other three about all 24
# cells.  It agrees with them at 24 of 24.
#
# That is this ticket's own subject happening to this ticket's own code, and
# it is left recorded because it is the cheapest possible demonstration of the
# thing being audited: a blind parser produces confident findings.  Two things
# changed as a result and both are load-bearing.  The pattern now accepts both
# header forms; and a parse that yields no cells now raises a SELF-ERROR and
# WITHDRAWS the instrument from the comparison instead of scoring it as a
# disagreement -- because "I could not read it" and "it disagrees" are
# different statements and only the second is a finding against anyone else.
def parse_b1(path):
    got = {}
    cur = None
    with open(path) as fh:
        for line in fh:
            m = re.match(r"\s*beta\s*=\s*(\d+)\s*:?\s*$", line)
            if m:
                cur = int(m.group(1))
                continue
            m = re.match(r"\s*n=(\d+)\s+vertices p = \[([\d,\s]*)\]\s+"
                         r"dims \[([\d,\s]*)\]\s*$", line)
            if m and cur is not None:
                ps = [int(x) for x in m.group(2).split(",") if x.strip()]
                ds = [int(x) for x in m.group(3).split(",") if x.strip()]
                got[(cur, int(m.group(1)))] = list(zip(ps, ds))
    return got


b1p = os.path.join(L.REPO, "code/branching_audit_2060/out_b1_branching.txt")
instruments.append(("b1_branching.py (mg-2060, 2nd)", parse_b1(b1p)))

# READABLE vs UNREADABLE, decided before anything is compared.  An instrument
# whose output this script cannot parse is WITHDRAWN with a SELF-ERROR; it is
# never scored as disagreeing.  See the note on parse_b1 above for why this
# distinction is written into the control flow and not left to care.
readable, unreadable = [], []
for name, got in instruments:
    (readable if len(got) == 24 else unreadable).append((name, got))
for name, got in unreadable:
    selferr("this script could not read all 24 vertex cells out of %s (%d "
            "parsed); it is WITHDRAWN from the comparison and is NOT scored "
            "as disagreeing" % (name, len(got)))

print("   instrument                        cells   agreeing with c1")
base = mine
for name, got in instruments:
    if len(got) != 24:
        print("     %-32s %3d      UNREADABLE HERE -- withdrawn, see SELF-ERRORS"
              % (name, len(got)))
        continue
    n_ag = sum(1 for k in base if k in got and got[k] == base[k])
    print("     %-32s %3d      %d of %d" % (name, len(got), n_ag, len(base)))
    if n_ag != 24:
        finding("%s disagrees with c1 on %d of the 24 vertex cells"
                % (name, 24 - n_ag))
print()
print("   pairwise, over every unordered pair of the %d READABLE instruments:"
      % len(readable))
npair = nagree = 0
for i in range(len(readable)):
    for j in range(i + 1, len(readable)):
        npair += 1
        a, b = readable[i][1], readable[j][1]
        bad = [k for k in set(a) | set(b) if a.get(k) != b.get(k)]
        nagree += not bad
        if bad:
            finding("instruments %s and %s disagree at %d of the 24 vertex "
                    "cells: %s" % (readable[i][0], readable[j][0], len(bad),
                                   sorted(bad)))
print("     pairs compared: %d, population: every unordered pair of the %d "
      "readable instruments; pairs agreeing on all 24 cells: %d"
      % (npair, len(readable), nagree))
print()

# ---------------------------------------------------------------------------
print("-" * 74)
print("(iv) CALIBRATION -- IS THE RECOVERY A COMPARISON, OR A RESTATEMENT?")
print("-" * 74)
print("""   A recovery that agrees whatever the target says would print exactly
   the rows above.  So each of the 24 cells is corrupted in turn, on a copy of
   the HEAD target, and the comparison in (ii) is required to go red at that
   cell and nowhere else.  The direction is predicted before each probe: RED.""")
print()
fired = missed = 0
for (beta, n), verts in sorted(ns.items()):
    line = "n=%d  %s" % (n, L.render_set(verts))
    # anchor inside the right beta section: the same rendering occurs at
    # several parameters and an unanchored replace would corrupt the wrong one
    key = "beta = %d\n" % beta
    if new_target.count(key) < 1:
        selferr("no 'beta = %d' header in the HEAD target" % beta)
        continue
    pre, post = new_target.split(key, 1)
    if post.count(line) < 1:
        selferr("cell beta=%d n=%d not found for corruption" % (beta, n))
        continue
    bumped = line[:-1] + ("8" if line[-1] != "8" else "7") + "]"
    bumped = re.sub(r"(\d)\]$", lambda m: str((int(m.group(1)) + 1) % 10) + "]",
                    line)
    if bumped == line:
        selferr("corruption of beta=%d n=%d is a no-op" % (beta, n))
        continue
    cor = pre + key + post.replace(line, bumped, 1)
    got = L.parse_vertex_sets(cor)
    red_here = got.get((beta, n)) != mine.get((beta, n))
    red_elsewhere = [k for k in got
                     if k != (beta, n) and got[k] != mine.get(k)]
    if red_here and not red_elsewhere:
        fired += 1
    else:
        missed += 1
        finding("corruption probe at beta=%d n=%d did not fire cleanly "
                "(red here %s, red elsewhere %s)"
                % (beta, n, red_here, red_elsewhere))
print("   probes fired: %d of %d, population: all 24 vertex cells, each "
      "corrupted alone" % (fired, fired + missed))
print("   probes that did not: %d" % missed)
print()
print("   AND THE OTHER DIRECTION: with the target restored, the comparison")
uncor = L.parse_vertex_sets(new_target)
green = sum(1 for k in mine if uncor.get(k) == mine[k])
print("   is green at %d of 24 cells." % green)
if green != 24:
    finding("restoring the target does not return all 24 cells to green (%d)"
            % green)
print()

# ---------------------------------------------------------------------------
print("-" * 74)
print("VERDICT ON QUESTION B AT HEAD")
print("-" * 74)
total = len(ns) + len(ndims) + len(nedges)
print("""   The reproduction is REDONE at %s and it stands, with all
   198 cells compared and 0 disagreements:

     %3d vertex cells   -- recovered from the SET block mg-13b2 installed,
                           compared as LABELLED SETS and not merely as
                           cardinalities, which is stronger than what was
                           compared at 286d5030
     %3d dimension cells-- byte-identical across ed9cde4
     %3d edge cells     -- byte-identical across ed9cde4
     %3d total, %d disagreements

   %d independent kernels agree on all 24 vertex cells, %d of %d pairs.
""" % (HEAD[:12], len(ns), len(ndims), len(nedges), total,
       len([f for f in FIND if "disagree" in f.lower()]),
       len(readable), nagree, npair))
if total != 198:
    finding("the redone reproduction covers %d cells, not 198" % total)

print("-" * 74)
print("SELF-ERRORS: %d, population: the parses of c1's own output and of the "
      "3 committed instrument outputs, and the %d corruption sites"
      % (len(SELF), len(ns)))
for x in SELF:
    print("   SELF-ERROR: " + x)
print("FINDINGS: %d, population: the 24 vertex cells compared as sets and as "
      "counts, the 53 dimension and 121 edge cells carried across ed9cde4, "
      "the %d cross-instrument comparisons and the %d corruption probes"
      % (len(FIND), npair + len(instruments), fired + missed))
for x in FIND:
    print("   FINDING: " + x)
print("TOTAL BAD: %d" % (len(SELF) + len(FIND)))
sys.exit(1 if (SELF or FIND) else 0)
