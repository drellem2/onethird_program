#!/usr/bin/env python3
"""a2_oldest.py -- DID `OLDEST` GET ABSORBED, AND COULD THE GATE HAVE SEEN IT?

The brief: CONFIRM `OLDEST` (10) WAS NOT ABSORBED INTO THE DEFECT POPULATION.
Inflating a count by including a stable class is the exact mistake the parent
names -- check the repair did not do it while fixing it.  Confirm whether a
CATEGORY BOUNDARY MOVED SILENTLY.

Two questions, and they have different answers:

  (i)   THE SUBSTANTIVE ONE.  Was any site that one tree calls `OLDEST`
        counted as history-derived at another?  Answered by comparing
        MEMBERSHIP SETS across five trees, not counts.  A count that grows is
        not evidence a boundary held.

  (ii)  THE ONE ABOUT THE GATE.  `t1_population.py:430` gates on
        `not [r for r in pinned if r["kind"] == "OLDEST"]`.  `pinned` is
        `ANCHORS.tsv` -- four rows this ticket wrote.  Can that check see an
        absorption?  CONSTRUCTED, in a clone.

Predicted exit: 0.  (i) is predicted clean and (ii) is a demonstration about
a gate, recorded as a NOTE.
"""
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_0ba7 as L                                          # noqa: E402

R = L.Report(
    selfpop="a2's own constructions",
    findpop="mg-b2af's treatment of the OLDEST class")

L.banner("mg-0ba7 a2", "`OLDEST`: THE BOUNDARY, AND THE GATE THAT WATCHES IT")

TREES = [
    (L.A330A_PRE,      "mg-330a's pre-repair commit, on main"),
    (L.A330A_REPAIR,   "mg-330a's repair, on main"),
    (L.B2AF_REPAIR,    "mg-b2af's repair"),
    (L.B2AF_EVIDENCE,  "mg-b2af's evidence"),
]

# ---------------------------------------------------------------------------
L.rule("(i) THE MEMBERSHIP SET, NOT THE COUNT, AT FIVE TREES")
# ---------------------------------------------------------------------------

print("""
   A site is identified across trees by (FILE, the tuple of its call's own
   string arguments).  Line numbers move when anything above them moves, so
   a set keyed on line number would report churn that is not churn.  That is
   a GRAIN choice and it is stated because the answer depends on it.
""")

sets = {}
counts = {}
for rev, why in TREES:
    d = L.clone_at(rev)
    try:
        rows, bad = L.anchor_sites(repo=d)
        rows = [r for r in rows
                if not r["file"].startswith(
                    "code/anchor_population_audit_0ba7/")]
        sets[rev] = {(r["file"], tuple(r["strs"])) for r in rows
                     if r["kind"] == "OLDEST"}
        hist = {(r["file"], tuple(r["strs"])) for r in rows
                if r["kind"] in L.HISTORY_KINDS}
        counts[rev] = (Counter(r["kind"] for r in rows), hist)
        R.selfgate(not bad, "%s: %d file(s) did not parse" % (rev, len(bad)))
    finally:
        L.rm_tree(d)

MINE_DIR = "code/anchor_population_audit_0ba7"
rows_now, _bad = L.anchor_sites()
rows_now = [r for r in rows_now if not r["file"].startswith(MINE_DIR + "/")]
print("   The worktree row EXCLUDES %s/ --" % MINE_DIR)
print("   this audit's own files are in the tree it is measuring, and its")
print("   selftest fixtures are real `git log` argv lists.  See a1 (i),")
print("   DEFECT #4.  The four cloned trees cannot contain them.")
sets["worktree"] = {(r["file"], tuple(r["strs"])) for r in rows_now
                    if r["kind"] == "OLDEST"}
counts["worktree"] = (Counter(r["kind"] for r in rows_now),
                      {(r["file"], tuple(r["strs"])) for r in rows_now
                       if r["kind"] in L.HISTORY_KINDS})

print("""   TWO GRAINS, PRINTED SIDE BY SIDE, BECAUSE THEY DISAGREE.  a1 counts
   CALL SITES: 12 OLDEST at this worktree.  The set below is keyed on
   (file, argument tuple) and collapses call sites that issue the identical
   command from the same file, so it is smaller.  NEITHER IS WRONG AND THEY
   ARE NOT THE SAME NUMBER.  The boundary question is a question about
   MEMBERSHIP, so it is asked at the set grain; the census question is a
   question about SITES, so a1 asks it at the row grain.  Reporting one
   under the other's name is the mismatch this lineage keeps finding.
""")
print("   %-12s %-30s %9s %7s %9s %7s"
      % ("tree", "what", "OLDEST/set", "/rows", "HIST/set", "/rows"))
order = [t[0] for t in TREES] + ["worktree"]
for rev in order:
    why = dict((a, b) for a, b in TREES).get(rev, "this worktree")
    c, hist = counts[rev]
    print("   %-12s %-30s %9d %7d %9d %7d"
          % (rev[:9], why[:30], len(sets[rev]), c.get("OLDEST", 0),
             len(hist), sum(c.get(k, 0) for k in L.HISTORY_KINDS)))

print()
print("   ABSORPTION IS A SITE THAT IS `OLDEST` AT ONE TREE AND")
print("   HISTORY-DERIVED AT ANOTHER.  Every ordered pair, checked:")
absorbed = []
for i, a in enumerate(order):
    for b in order[i + 1:]:
        moved = sets[a] & counts[b][1]
        back = sets[b] & counts[a][1]
        if moved or back:
            absorbed.append((a, b, moved | back))
        print("     %-10s -> %-10s  OLDEST-turned-history: %d ; "
              "history-turned-OLDEST: %d"
              % (a[:9], b[:9], len(moved), len(back)))
R.total("sites that changed side of the OLDEST boundary", len(absorbed),
        "the 10 ordered tree pairs above", "one SITE (file + argument tuple)")
R.gate(not absorbed,
       "a site crosses the OLDEST/history-derived boundary between two "
       "trees: %s" % absorbed)

print()
print("   AND THE SET IS MONOTONE.  The `OLDEST` membership at each tree,")
print("   against the next:")
nested = True
for i in range(len(order) - 1):
    a, b = order[i], order[i + 1]
    sub = sets[a] <= sets[b]
    lost = sets[a] - sets[b]
    nested = nested and sub
    print("     %-10s subset of %-10s : %-5s  (%d gained, %d lost)"
          % (a[:9], b[:9], sub, len(sets[b] - sets[a]), len(lost)))
    for x in sorted(lost):
        print("        LOST: %s %s" % (x[0], x[1]))
R.total("OLDEST sets nested along the commit order", int(nested),
        "the four consecutive tree pairs", "a BOOLEAN over the whole chain")

print("""
   THE SUBSTANTIVE ANSWER: `OLDEST` WAS NOT ABSORBED.  mg-330a named the
   class apart deliberately -- a file's creation does not move when the file
   is edited -- and mg-b2af did not let its population grow by swallowing it.
   The count moved because the TREE moved, and the membership set grew by
   exactly the sites the new commits added and lost none.  The repair did
   not make A-2's mistake.

   ONE PAIR OF NUMBERS EARNS A WORD.  mg-330a's document says `OLDEST 10`
   and mg-b2af showed the sweep says 11 at every tree it measured, calling
   the document's 10 unreproducible.  At the SET grain above, mg-330a's own
   two commits give 8.  That is not a third answer to the same question --
   it is the answer to a different one, and it is printed here only so that
   nobody reads the 8 as a correction of the 11.  The row-count column is
   the one comparable with mg-b2af's, and it agrees with mg-b2af.
""")

# ---------------------------------------------------------------------------
L.rule("(ii) COULD THE GATE HAVE SEEN IT?  CONSTRUCTED.")
# ---------------------------------------------------------------------------

print("""
   `t1_population.py:424-432` prints

       OLDEST rows in the treated population : N
       R.check(not [r for r in pinned if r["kind"] == "OLDEST"], ...)

   `pinned` is `L.read_anchors()` -- the rows of `code/repair_b2af/
   ANCHORS.tsv`, a four-row file mg-b2af wrote, whose `kind` column mg-b2af
   filled in.  `HISTORY_KINDS` excludes `OLDEST`, and ANCHORS.tsv is drawn
   from the history-derived rows, so no `OLDEST` row can reach `pinned`
   except by mg-b2af typing one.

   THE PREDICATE IS RE-IMPLEMENTED HERE, NOT RUN.  `t1` clones the repo four
   times; running it inside another clone is minutes of work to learn one
   boolean.  The three lines below are the predicate as written at
   `t1_population.py:430`, applied to the same file `read_anchors` reads.
""")


def parent_oldest_gate(tree):
    """`not [r for r in pinned if r["kind"] == "OLDEST"]`, over ANCHORS.tsv."""
    path = os.path.join(tree, "code/repair_b2af/ANCHORS.tsv")
    if not os.path.exists(path):
        return None, []
    rows = []
    with open(path) as fh:
        head = None
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.rstrip("\n").split("\t")
            if head is None:
                head = parts
                continue
            rows.append(dict(zip(head, parts)))
    return (not [r for r in rows if r["kind"] == "OLDEST"]), rows


clone = L.clone_at("HEAD")
try:
    green_before, anchors = parent_oldest_gate(clone)
    R.selfgate(green_before is True,
               "the parent's OLDEST gate is not green on an unmodified "
               "clone; the re-implementation is wrong, not the gate")
    print("   rows in ANCHORS.tsv                      : %d" % len(anchors))
    print("   their kinds                              : %s"
          % sorted({r["kind"] for r in anchors}))
    print("   the parent's OLDEST gate, clean clone    : %s"
          % ("GREEN" if green_before else "RED"))

    rows0, _ = L.anchor_sites(repo=clone)
    old0 = [r for r in rows0 if r["kind"] == "OLDEST"]
    hist0 = [r for r in rows0 if r["kind"] in L.HISTORY_KINDS]

    # THE CONSTRUCTION.  Take one site this tree calls OLDEST and delete
    # `--reverse` from it.  Nothing else changes.  The site is now INDEXED --
    # it has been ABSORBED into the defect population.
    victim = None
    for r in sorted(old0, key=lambda r: (r["file"], r["line"])):
        full = os.path.join(clone, r["file"])
        with open(full) as fh:
            src = fh.read()
        lines = src.splitlines(True)
        if '"--reverse"' in lines[r["line"] - 1]:
            victim = (r, full, lines)
            break
    if victim is None:
        R.selferr("no OLDEST site carries `--reverse` on its own call line; "
                  "the construction below could not be built and (ii) is "
                  "unmeasured")
    else:
        r, full, lines = victim
        print()
        print("   THE CONSTRUCTED ABSORPTION")
        print("     victim site  : %s:%d" % (r["file"], r["line"]))
        print("     before       : %s" % lines[r["line"] - 1].strip()[:64])
        lines[r["line"] - 1] = lines[r["line"] - 1].replace('"--reverse", ',
                                                            "")
        lines[r["line"] - 1] = lines[r["line"] - 1].replace('"--reverse",',
                                                            "")
        print("     after        : %s" % lines[r["line"] - 1].strip()[:64])
        L.commit_in(clone, r["file"], "".join(lines),
                    "constructed: --reverse removed from one OLDEST site")

        rows1, _ = L.anchor_sites(repo=clone)
        old1 = [x for x in rows1 if x["kind"] == "OLDEST"]
        hist1 = [x for x in rows1 if x["kind"] in L.HISTORY_KINDS]
        green_after, _ = parent_oldest_gate(clone)

        print()
        print("     %-46s %6s %6s" % ("", "before", "after"))
        print("     %-46s %6d %6d" % ("OLDEST sites (my classifier)",
                                      len(old0), len(old1)))
        print("     %-46s %6d %6d" % ("history-derived sites", len(hist0),
                                      len(hist1)))
        print("     %-46s %6s %6s" % ("the parent's OLDEST gate",
                                      "GREEN" if green_before else "RED",
                                      "GREEN" if green_after else "RED"))

        moved = (len(old1) == len(old0) - 1) and (len(hist1) == len(hist0) + 1)
        R.selfgate(moved,
                   "the construction did not move a site across the "
                   "boundary (OLDEST %d->%d, history %d->%d), so the gate's "
                   "silence below proves nothing"
                   % (len(old0), len(old1), len(hist0), len(hist1)))
        if moved and green_after:
            R.note(
                "AN OLDEST SITE WAS ABSORBED INTO THE HISTORY-DERIVED "
                "POPULATION AND THE GATE THAT WATCHES FOR EXACTLY THAT "
                "STAYED GREEN.  `t1`'s check reads ANCHORS.tsv -- mg-b2af's "
                "own four-row output -- not the classifier's rows.  It can "
                "only go red if mg-b2af writes the word OLDEST into its own "
                "file.  The substantive answer in (i) is clean; this is "
                "about what the gate is able to say, and the answer is that "
                "it is able to say the repair did not mistype its own TSV.")
        print("""
     THE GATE IS NOT WRONG.  It is asked of the TREATED population, and
     nothing is wrong with checking that.  It is offered under a sentence --
     `Absorbing it would inflate this repair's population` -- about the
     MEASURED population, which is a different set, and the check that
     sentence describes is not made anywhere.  A label/grain mismatch: one
     predicate, two populations, and the narrower one printed under the
     wider one's name.
""")
finally:
    L.rm_tree(clone)

# ---------------------------------------------------------------------------
L.rule("(iii) AND THE SAME QUESTION ASKED OF MY OWN CLASSIFIER")
# ---------------------------------------------------------------------------

print("""
   a1 found 15 call sites mg-330a's classifier cannot see, all of them
   `--format=%h`.  If any of those 15 is an `OLDEST` site, then MY wider
   population would inflate the OLDEST class rather than the defect class,
   and I would be making A-2's mistake in the other direction while
   reporting it.
""")
mine_only = []
sys.path.insert(0, os.path.join(L.REPO, "code", "audit_330a"))
import warnings                                               # noqa: E402
warnings.filterwarnings("ignore", category=SyntaxWarning)
import ast                                                    # noqa: E402
from lib330a import classify_call, _strings_of                # noqa: E402

files, _bad = L.py_files()
theirs = set()
files = [f for f in files if not f[0].startswith(MINE_DIR + "/")]
for rel, _src, tree in files:
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and classify_call(_strings_of(node)):
            theirs.add((rel, node.lineno))
for r in rows_now:
    if (r["file"], r["line"]) not in theirs:
        mine_only.append(r)
c = Counter(r["kind"] for r in mine_only)
R.total("sites only MY classifier sees", len(mine_only),
        "the 59 rows of my census minus the 44 of theirs", "one CALL SITE")
for k in sorted(c):
    print("     %-16s %d" % (k, c[k]))
R.total("of those, OLDEST", c.get("OLDEST", 0),
        "the sites only my classifier sees", "one CALL SITE")
print("   -- %d.  My widening adds nothing to the STABLE class and %d to the"
      % (c.get("OLDEST", 0),
         sum(c.get(k, 0) for k in L.HISTORY_KINDS)))
print("      DEFECT classes.  That is the direction that costs me, not the")
print("      direction that flatters me, and it is why the widening is")
print("      reported rather than argued.")

# ---------------------------------------------------------------------------
L.rule("(iv) PREDICTIONS SCORED")
# ---------------------------------------------------------------------------
L.score(R, "P-4a", "0 OLDEST absorbed, at every tree", len(absorbed),
        hit=(len(absorbed) == 0),
        note="the substantive answer, and it CONFIRMS the repair")
L.score(R, "P-4b", "the parent's gate stays GREEN through it",
        "GREEN" if green_after else "RED", hit=bool(green_after))
b2af_rows = counts[L.B2AF_REPAIR][0].get("OLDEST", 0)
mine_rows_ct = counts["worktree"][0].get("OLDEST", 0)
L.score(R, "P-4c", "mg-b2af's tree 11, mine 12, one new site",
        "mg-b2af's tree %d, mine %d, %d new"
        % (b2af_rows, mine_rows_ct,
           len(sets["worktree"] - sets[L.B2AF_REPAIR])),
        hit=(b2af_rows == 11 and mine_rows_ct == 12),
        note="the growth 11->12 happened BETWEEN mg-330a's commits and "
             "mg-b2af's, not between mg-b2af's and mine; I put the step in "
             "the wrong interval and the set is still nested")

R.done()
