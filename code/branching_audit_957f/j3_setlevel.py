"""j3_setlevel.py -- THE SET-LEVEL PROPERTY, RE-DERIVED ON READERS WRITTEN HERE.

mg-321d confirmed and mg-7e58 re-derived: 10 of 10 pairs of sources agreeing at
24 of 24 cells, all five of mg-a218's members re-run.  Corroboration is a
property of the SET, so a repair that edits one member and re-runs only that
member has not preserved it -- and this repair edited NONE of the five, which
is exactly why "the member I changed still works" would say nothing at all.

So all five are re-run here, and the ten pairs are compared cell by cell on
readers written in lib957f.py from the file formats.  Nothing is read out of
g4's or k3's output.

And the readers are probed, because a BLIND reader agrees with everything: each
source is corrupted at beta=1, n=6 -- the only n=6 cell no other parameter
carries identically -- and its reader must move at that cell and nowhere else.
A reader that returns no cells at all is a SELF-ERROR and its source is
WITHDRAWN from the comparison, never scored as agreement.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import itertools
import sys

import lib957f as L

R = L.Report("j3", "the %d pair-cell comparisons over the sources that were "
                   "read, the 5 in-place member runs, the 5 reader locality "
                   "probes, and the 5 re-runs of mg-321d's own finders"
                   % (10 * 24))

L.banner("J3", "10 PAIRS AT 24 CELLS, AND ALL FIVE MEMBERS -- RE-DERIVED")

# ---------------------------------------------------------------------------
L.rule("(i) THE FIVE SOURCES, READ")
print("""   Five sources measure the same 24 cells: the target mg-a218 audited,
   two of mg-a218's own members run LIVE, and two committed records from
   instruments outside this arc.  A source whose reader returns nothing is
   WITHDRAWN, with a SELF-ERROR, rather than counted as agreeing.""")
print()

target_txt = L.read_worktree(L.TARGET_REL)
b1_txt = L.read_worktree(L.B1_REL)
e1_txt = L.read_worktree(L.E1_REL)
print("   running c1_branching.py in place ...")
c1_out, c1_rc = L.run_script(L.A218_DIR, "c1_branching.py")
print("   running c2_vertexsets.py in place ...")
c2_out, c2_rc = L.run_script(L.A218_DIR, "c2_vertexsets.py")

SOURCES = [
    ("target out_t1_tl.txt", L.target_cells, target_txt),
    ("c1_branching.py, live", L.c1_cells, c1_out),
    ("c2_vertexsets.py, live", L.c2_cells, c2_out),
    ("mg-2060 out_b1_branching.txt", L.b1_cells, b1_txt),
    ("mg-d330 out_e1_vertexsets.txt", L.e1_cells, e1_txt),
]

read = {}
print()
print("   source                             cells read   all 24 present")
for name, fn, text in SOURCES:
    cells = fn(text)
    have = all(k in cells for k in L.CELLS)
    print("     %-32s %-12d %s" % (name, len(cells), "yes" if have else "NO"))
    if not cells:
        R.selferr("this script's reader for %s returned no cells; the source "
                  "is WITHDRAWN from the comparison rather than scored" % name)
        continue
    if not have:
        R.selferr("this script's reader for %s is missing some of the 24 "
                  "cells; the source is WITHDRAWN" % name)
        continue
    read[name] = cells
print()
print("   sources read: %d of %d." % (len(read), len(SOURCES)))
print()

# ---------------------------------------------------------------------------
L.rule("(ii) THE PAIRS, CELL BY CELL")
names = [n for n, _, _ in SOURCES if n in read]
pairs = list(itertools.combinations(names, 2))
print("   %d sources -> %d pairs, %d cells each, %d cell comparisons."
      % (len(names), len(pairs), len(L.CELLS), len(pairs) * len(L.CELLS)))
print()
print("   pair                                                     cells agreeing")
nfull = 0
ncmp = 0
for a, b in pairs:
    agree = sum(1 for k in L.CELLS if read[a][k] == read[b][k])
    ncmp += len(L.CELLS)
    nfull += agree == len(L.CELLS)
    print("     %-28s vs %-24s %d of %d"
          % (a[:28], b[:24], agree, len(L.CELLS)))
    R.check(agree == len(L.CELLS),
            "%s and %s disagree at %d of %d cells: %s"
            % (a, b, len(L.CELLS) - agree, len(L.CELLS),
               [k for k in L.CELLS if read[a][k] != read[b][k]]))
print()
print("   pairs agreeing at all %d cells : %d of %d" % (len(L.CELLS), nfull,
                                                        len(pairs)))
print("   cell comparisons made          : %d" % ncmp)
print("   population: every unordered pair of the sources that WERE read,")
print("   over the 24 (beta, n) cells with beta in {3,2,1,0} and 1 <= n <= 6.")
print()

# ---------------------------------------------------------------------------
L.rule("(iii) ALL FIVE OF mg-a218'S MEMBERS, RE-RUN IN PLACE")
print("""   Not only the ones this repair touched -- it touched none.  Each is
   run with its stdout captured HERE and never redirected into its committed
   output, which is a record and not a live gate.""")
print()
print("   member                 exit   self/find")
runs = {}
for f in L.FIVE:
    if f == "c1_branching.py":
        out, rc = c1_out, c1_rc
    elif f == "c2_vertexsets.py":
        out, rc = c2_out, c2_rc
    else:
        print("     (running %s ...)" % f)
        out, rc = L.run_script(L.A218_DIR, f)
    s, fi = L.totals_of(out)
    runs[f] = (rc, s, fi)
    print("     %-22s %-6s %s/%s" % (f, rc, s, fi))
green = [f for f in L.FIVE if runs[f][0] == 0]
print()
print("   members re-run : %d of %d" % (len(runs), len(L.FIVE)))
print("   members green  : %d of %d" % (len(green), len(L.FIVE)))
red = [f for f in L.FIVE if f not in green]
print("   red            : %s" % (", ".join(red) or "none"))
R.check(len(runs) == len(L.FIVE),
        "not all five members were re-run: %d of %d" % (len(runs), len(L.FIVE)))
if red == ["c3_withdrawal.py"]:
    print("   c3_withdrawal.py is mg-d330's SECOND FINDING, booked OPEN by")
    print("   mg-58da and untouched by mg-7e58.  It is reported BY NAME here")
    print("   and not counted as a finding of this audit's own.")
else:
    R.check(not red, "members are red that are not the OPEN c3_withdrawal.py: "
                     "%s" % red)
print()

# ---------------------------------------------------------------------------
L.rule("(iv) THE READERS, PROBED -- A BLIND READER AGREES WITH EVERYTHING")
print("""   Each source is corrupted at beta=1, n=6 and its reader must move at
   that cell and NOWHERE ELSE.  beta=1 is the parameter no other carries
   identically at n=6: beta=3 and beta=2 are equal to each other there, so a
   probe aimed at either could not be aimed at all.""")
print()

CELL = (1, 6)


def bend_target(t):
    return L.replace_in_block(t, "n=6  [0:1,1:4,2:9,3:1]\n",
                              "n=6  [0:1,1:4,2:9,3:7]\n")


def bend_c1(t):
    return L.replace_once(t, "set { p=0:dim 1, p=1:dim 4, p=2:dim 9, "
                             "p=3:dim 1 }",
                          "set { p=0:dim 1, p=1:dim 4, p=2:dim 9, "
                          "p=3:dim 7 }")


def bend_c2(t):
    """c2 prints the same list twice on one line; only the half after
    `-- mine, as sets:` is read, so only that half is bent."""
    out = []
    hits = 0
    for line in t.splitlines(True):
        if "-- mine, as sets:" in line and "beta=1" in line:
            head, tail = line.split("-- mine, as sets:", 1)
            tail = L.replace_once(tail, "[1, 4, 9, 1]", "[1, 4, 9, 7]")
            line = head + "-- mine, as sets:" + tail
            hits += 1
        out.append(line)
    if hits != 1:
        raise ValueError("expected exactly 1 beta=1 set row, found %d" % hits)
    return "".join(out)


def bend_b1(t):
    return L.replace_once(t, "dims [1, 4, 9, 1]", "dims [1, 4, 9, 7]")


def bend_e1(t):
    return L.replace_once(t, "[0:1,1:4,2:9,3:1]", "[0:1,1:4,2:9,3:7]")


PROBES = [("target out_t1_tl.txt", L.target_cells, target_txt, bend_target),
          ("c1_branching.py, live", L.c1_cells, c1_out, bend_c1),
          ("c2_vertexsets.py, live", L.c2_cells, c2_out, bend_c2),
          ("mg-2060 out_b1_branching.txt", L.b1_cells, b1_txt, bend_b1),
          ("mg-d330 out_e1_vertexsets.txt", L.e1_cells, e1_txt, bend_e1)]

print("   source                             moved at (1,6)  moved elsewhere")
nlocal = 0
for name, fn, text, bend in PROBES:
    if name not in read:
        R.selferr("%s was withdrawn in (i), so its locality probe is DROPPED "
                  "from the population rather than counted as passing" % name)
        continue
    try:
        bent = bend(text)
    except ValueError as e:
        R.selferr("could not aim the locality probe at %s (%s); it is DROPPED "
                  "from the population rather than counted as passing"
                  % (name, e))
        continue
    after = fn(bent)
    before = read[name]
    moved = sorted(k for k in L.CELLS if before[k] != after.get(k))
    ok = moved == [CELL]
    nlocal += ok
    print("     %-32s %-15s %s"
          % (name, "yes" if CELL in moved else "NO",
             ", ".join(str(k) for k in moved if k != CELL) or "none"))
    R.check(ok, "the locality probe on %s moved %s, not exactly [(1, 6)]; the "
                "reader is not reading the cell it is credited with"
            % (name, moved))
print()
print("   readers moving at their own cell and no other : %d of %d"
      % (nlocal, len(PROBES)))
print("   population: the %d sources read in (i); a source withdrawn there is"
      % len(read))
print("   DROPPED here and named, not counted.")
print()

# ---------------------------------------------------------------------------
L.rule("(v) mg-321d'S OWN FINDERS, UNMODIFIED, ON THE REPAIRED TREE")
print("""   The instrument that RAISED G-1 and G-2, re-run here at today's HEAD
   with not a byte changed, against its own committed record.  h2_grain.py is
   the finder for G-1 and G-2 and is the one that must move; the other four
   must not, because this repair closes G-1/G-2/G-3 and touches neither M-1
   nor M-2 nor c3.""")
print()
H_COMMITTED = {"h1_questions": 0, "h2_grain": 3, "h3_setlevel": 1,
               "h4_mine": 2, "h5_doccheck": 0}
H_MUST_MOVE = {"h2_grain"}
print("   script            committed  re-run  must move  ")
nh = 0
for name in ["h1_questions", "h2_grain", "h3_setlevel", "h4_mine",
             "h5_doccheck"]:
    print("     (running %s.py ...)" % name)
    out, rc = L.run_script(L.S321D_DIR, name + ".py")
    s_, f_ = L.totals_of(out)
    if f_ is None:
        R.selferr("could not read a FINDINGS total out of %s.py's stdout; it "
                  "is DROPPED from the population rather than counted" % name)
        continue
    want_move = name in H_MUST_MOVE
    moved = f_ != H_COMMITTED[name]
    ok = moved == want_move and (f_ == 0 if want_move else True)
    nh += ok
    print("     %-17s %-10d %-7d %-10s %s"
          % (name + ".py", H_COMMITTED[name], f_,
             "yes" if want_move else "no", "HIT" if ok else "MISS"))
    R.check(ok, "mg-321d's %s.py has %d findings against a committed %d; "
                "predicted %s" % (name, f_, H_COMMITTED[name],
                                  "0 (the repair closes it)" if want_move
                                  else "unmoved"))
print()
print("   mg-321d finders whose direction was predicted correctly: %d of 5"
      % nh)
print("   population: all five of mg-321d's h*.py, run unmodified in place")
print("   with their stdout captured HERE and never redirected into their")
print("   committed out_h*.txt.")
print()

sys.exit(R.emit())
