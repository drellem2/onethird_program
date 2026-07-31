"""k3_setlevel.py -- THE PROPERTY THAT MUST NOT BE WEAKENED, RE-DERIVED.

mg-321d's ticket is explicit that the set-level corroboration is the thing this
arc was buying and that any repair here must leave it intact, with a weakening
counted as a defect in its own right.  So it is not quoted from g4's output or
from h3's -- a repair that checked itself by reading the numbers its own
predecessor printed would be doing the thing this whole arc is about.  It is
re-derived here, from the files, on readers written for this directory:

  * five sources that state the 24 vertex cells, read five different ways;
  * every unordered pair compared at every one of the 24 cells -- 10 pairs;
  * all five of mg-a218's members re-run in place, with their exit codes;
  * c0_repro.sh, the same property one level down.

AND THE READERS ARE PROBED.  A reader that has gone blind reports agreement
with the same confidence as one that is working -- mg-321d's h3 booked four
findings on exactly that -- so each source is corrupted at one cell and its
reader must move AT that cell and nowhere else.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

import lib7e58 as L

R = L.Report("k3", "the 24 cells of every readable source, every unordered "
                   "pair of them, the 5 members re-run in place, c0_repro.sh, "
                   "and one locality probe per source")

L.banner("K3", "10 OF 10 PAIRS AT 24 OF 24 CELLS -- RE-DERIVED, NOT QUOTED")

HEAD = L.head_rev()

# ---------------------------------------------------------------------------
L.rule("(i) ALL FIVE MEMBERS, RE-RUN IN PLACE")
print("""   Not only the members this repair touched -- it touched none of them.
   Re-running only what changed would prove nothing about corroboration, which
   is a property OF THE SET.  All five are run, in place, with their stdout
   captured here and never redirected into their committed outputs.""")
print()
live = {}
print("   member                  self/find   exit")
for f in L.FIVE:
    out, rc = L.run_script(L.A218_DIR, f)
    s, fi = L.totals_of(out)
    live[f] = (out, rc)
    print("     %-22s %s/%-6s  %d" % (f, s, fi, rc))
green = [f for f in L.FIVE if live[f][1] == 0]
red = [f for f in L.FIVE if live[f][1] != 0]
print()
print("   members actually re-run here : %d of 5 -- %s"
      % (len(L.FIVE), ", ".join(L.FIVE)))
print("   green : %d of 5 -- %s" % (len(green), ", ".join(green)))
print("   red   : %d of 5 -- %s" % (len(red), ", ".join(red) or "none"))
R.check(len(L.FIVE) == 5 and all(f in live for f in L.FIVE),
        "not all five members were re-run here")
for f in red:
    if f == "c3_withdrawal.py":
        print()
        print("   c3_withdrawal.py is red, and it was red before this repair.")
        print("   Its finding is mg-d330's second, booked OPEN by mg-58da and")
        print("   untouched here.  It is reported, not worked around: the")
        print("   set-level property is that ALL FIVE are green and it is not.")
    else:
        R.finding("%s is red on the repaired tree and is not accounted for by "
                  "this repair or by mg-58da" % f)
R.check(sorted(red) == ["c3_withdrawal.py"],
        "the red members on the repaired tree are %s; before this repair the "
        "only red member was c3_withdrawal.py, so this repair moved a member "
        "and that is a weakening of the set-level property" % sorted(red))

# ---------------------------------------------------------------------------
L.rule("(ii) FIVE SOURCES FOR THE 24 CELLS, READ FIVE DIFFERENT WAYS")
sources = []


def add(name, getter):
    try:
        cells = getter()
    except Exception as exc:                                     # noqa: BLE001
        R.selferr("could not read %s: %s -- it is WITHDRAWN and is NOT scored "
                  "as disagreeing with anything" % (name, exc))
        return
    if len(cells) != 24:
        R.selferr("read %d of the 24 cells out of %s; it is WITHDRAWN from "
                  "every comparison below and is NOT scored as disagreeing"
                  % (len(cells), name))
        return
    sources.append((name, cells))


add("out_t1_tl.txt      (mg-e8b8, 1st instrument)",
    lambda: L.target_cells(L.read_worktree(L.TARGET_REL)))
add("c1_branching.py    (mg-a218, 3rd instrument, live)",
    lambda: L.c1_cells(live["c1_branching.py"][0]))
add("c2_vertexsets.py   (mg-a218, 3rd instrument, live)",
    lambda: L.c2_cells(live["c2_vertexsets.py"][0]))
add("out_b1_branching.. (mg-2060, 2nd instrument)",
    lambda: L.b1_cells(L.read_worktree(
        "code/branching_audit_2060/out_b1_branching.txt")))
add("out_e1_vertexsets. (mg-d330, 4th instrument)",
    lambda: L.e1_cells(L.read_worktree(
        "code/branching_audit_d330/out_e1_vertexsets.txt")))

print()
print("   source                                          cells read")
for name, cells in sources:
    print("     %-46s %2d of 24" % (name, len(cells)))
print()
print("   sources this script could read : %d" % len(sources))
R.check(len(sources) == 5,
        "only %d of the 5 sources could be read here, so the pair count below "
        "is not the 10 the property is stated at" % len(sources))

# ---------------------------------------------------------------------------
L.rule("(iii) EVERY UNORDERED PAIR, AT EVERY ONE OF THE 24 CELLS")
pairs, agree = 0, 0
for i in range(len(sources)):
    for j in range(i + 1, len(sources)):
        pairs += 1
        ni, di = sources[i]
        nj, dj = sources[j]
        bad = [c for c in L.CELLS if di.get(c) != dj.get(c)]
        if bad:
            R.finding("%s and %s disagree at %d of the 24 vertex cells: %s"
                      % (ni.strip(), nj.strip(), len(bad), bad[:6]))
        else:
            agree += 1
print("   pairs of sources agreeing on all 24 cells : %d of %d" % (agree, pairs))
print("   population: every unordered pair drawn from the %d sources above,"
      % len(sources))
print("   compared at all %d (beta,n) cells.  A source this script could not"
      % len(L.CELLS))
print("   read is in the SELF-ERROR channel and is not among these pairs.")
print()
print("   cells compared in total : %d" % (pairs * len(L.CELLS)))
R.check(pairs == 10 and agree == 10,
        "the set-level property is weaker here than mg-321d recorded: %d of %d "
        "pairs agree, where the record is 10 of 10" % (agree, pairs))

# ---------------------------------------------------------------------------
L.rule("(iv) THE READERS, PROBED AT ONE CELL EACH")
print("""   A reader that has gone blind agrees with everything.  So each source
   is corrupted at ONE cell and its reader must move at that cell and at no
   other.  The cell is beta=1, n=6 -- dims (1,4,9,1) -- because it is the only
   n=6 cell no other parameter shares: aiming at beta=3's would have hit
   beta=2's identical row as well, which is how the first run of this probe
   found itself unable to aim.

   And the corruption is scoped TO ONE LINE, located by a pattern that must
   match exactly one: the same dim list appears in these files' prose, and a
   probe that changed the prose instead would be testing nothing.""")
print()
CELL = (1, 6)


def probe(name, text, line_pat, old, new):
    """Corrupt `old` -> `new` inside the ONE line matching `line_pat`."""
    hits = [l for l in text.splitlines() if re.match(line_pat, l)]
    if len(hits) != 1:
        R.selferr("the locality probe for %s cannot be aimed: the line pattern "
                  "%r matches %d lines, not 1" % (name, line_pat, len(hits)))
        return None
    line = hits[0]
    if line.count(old) != 1:
        R.selferr("the locality probe for %s cannot be aimed: %r occurs %d "
                  "times on its own line, not once" % (name, old,
                                                       line.count(old)))
        return None
    return text.replace(line, line.replace(old, new, 1), 1)


PROBE_SPECS = [
    ("out_t1_tl.txt", L.target_cells, L.read_worktree(L.TARGET_REL),
     r"\s*n=6\s+\[0:1,1:4,2:9,3:1\]\s*$", "3:1", "3:7"),
    ("out_b1_branching..", L.b1_cells,
     L.read_worktree("code/branching_audit_2060/out_b1_branching.txt"),
     r"\s*n=6\s+vertices p = \[0, 1, 2, 3\]\s+dims \[1, 4, 9, 1\]\s*$",
     "9, 1]", "9, 7]"),
    ("out_e1_vertexsets.", L.e1_cells,
     L.read_worktree("code/branching_audit_d330/out_e1_vertexsets.txt"),
     r"\s*beta = 1\s+\[.*\]\s*$", "[0:1,1:4,2:9,3:1]", "[0:1,1:4,2:9,3:7]"),
    ("c1_branching.py", L.c1_cells, live["c1_branching.py"][0],
     r"\s*n=6\s+count 4\s+set \{ p=0:dim 1, p=1:dim 4, p=2:dim 9, "
     r"p=3:dim 1 \}\s*$", "p=3:dim 1", "p=3:dim 7"),
    # c2 prints the TARGET's sets and its OWN on one line, so '[1, 4, 9, 1]'
    # occurs twice there.  The probe is aimed at the 'mine' side, which is the
    # datum c2_cells() reads; hitting the other side would corrupt something
    # this reader never looks at and the probe would stay green for the wrong
    # reason.
    ("c2_vertexsets.py", L.c2_cells, live["c2_vertexsets.py"][0],
     r"\s*beta=1 : .*-- mine, as sets: \[\[.*\]\]\s*$",
     "mine, as sets: [[1], [1, 1], [1, 1], [1, 3, 1], [1, 4, 1], [1, 4, 9, 1]]",
     "mine, as sets: [[1], [1, 1], [1, 1], [1, 3, 1], [1, 4, 1], [1, 4, 9, 7]]"),
]
print("   source                 baseline   corrupted at (1,6)   moved at")
nfired = 0
for name, reader, text, line_pat, old, new in PROBE_SPECS:
    base = reader(text)
    mutated = probe(name, text, line_pat, old, new)
    if mutated is None:
        continue
    got = reader(mutated)
    moved = sorted(c for c in L.CELLS if base.get(c) != got.get(c))
    ok = moved == [CELL]
    nfired += ok
    print("     %-22s %2d cells   %2d cells             %s   %s"
          % (name, len(base), len(got),
             str(moved[:3]) if moved else "nothing", "OK" if ok else "WRONG"))
    if not ok:
        R.finding("the reader for %s does not move at (3,6) and only there "
                  "when that cell is corrupted (moved at %s); it is not "
                  "reading the cell it reports" % (name, moved))
print()
print("   probes moving exactly their own cell : %d of %d"
      % (nfired, len(PROBE_SPECS)))
print("   population: one corruption per source, each changing one dimension")
print("   of the (beta=%d, n=%d) cell on one line and nothing else." % CELL)

# ---------------------------------------------------------------------------
L.rule("(v) c0_repro.sh -- THE SAME PROPERTY ONE LEVEL DOWN")
print("""   mg-a218's c0 re-runs the TARGET's own five scripts and diffs all five
   committed outputs byte for byte.  This repair changed nothing the target
   reads, so it must still hold.  Run on a scratch copy so nothing here can
   write into the audited directories.""")
tmp = tempfile.mkdtemp(prefix="mg7e58-c0-")
try:
    for d in (L.A218_DIR, L.DB09_DIR):
        shutil.copytree(os.path.join(L.REPO, d), os.path.join(tmp, d))
    p = subprocess.run(["sh", "c0_repro.sh"], cwd=os.path.join(tmp, L.A218_DIR),
                       capture_output=True, text=True)
    ident = re.search(r"identical: (\d+) of (\d+)", p.stdout)
    print()
    for line in p.stdout.splitlines():
        if "IDENTICAL" in line or "DIFFER" in line or "identical:" in line:
            print("     %s" % line.strip()[:110])
    print("   c0_repro.sh exit %d" % p.returncode)
    R.check(p.returncode == 0,
            "c0_repro.sh exits %d on the repaired tree: the target's own five "
            "committed outputs no longer regenerate" % p.returncode)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# ---------------------------------------------------------------------------
L.rule("VERDICT ON THE PROPERTY THIS REPAIR WAS TOLD NOT TO WEAKEN")
print("""   %d of %d pairs of sources agree at all 24 cells, over %d cell
   comparisons; %d of 5 members were re-run in place, not only the changed one
   -- and this repair changed NONE of the five, which is why the check is a
   re-derivation and not a re-run of what moved; c0_repro.sh regenerates the
   target's five committed outputs.  %d of %d readers move at their own cell
   and nowhere else, so the agreement above is a measurement.

   WHAT DOES NOT HOLD, unchanged from before this repair: c3_withdrawal.py is
   red.  That is mg-d330's second finding, booked OPEN by mg-58da, and it is
   reported here rather than worked around.
""" % (agree, pairs, pairs * len(L.CELLS), len(L.FIVE), nfired,
       len(PROBE_SPECS)))

sys.exit(R.emit())
