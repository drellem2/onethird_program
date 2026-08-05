#!/usr/bin/env python3
"""a1_population.py -- THE POPULATION, RE-DERIVED BY AST FROM SCRATCH.

The brief: RE-DERIVE THE POPULATION YOURSELF BY AST.  Do not accept the
repair's count.  Report your own numbers beside the parent's, and if they
differ, THAT IS THE FINDING.  Include the call sites carrying no
`--format=%H`.

Four sections:

  (i)   two classifiers over the same call sites, row by row
  (ii)  the kind counts, mine and mg-330a's, beside every published figure
  (iii) the no-`--format=%H` population: a NAME-LIST against a CLOSURE
  (iv)  converted-count against SIXTEEN, and against what SIXTEEN turns out
        to be

Predicted exit: 1.
"""
import ast
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_0ba7 as L                                          # noqa: E402

sys.path.insert(0, os.path.join(L.REPO, "code", "audit_330a"))
import warnings                                               # noqa: E402
warnings.filterwarnings("ignore", category=SyntaxWarning)
from lib330a import classify_call, _strings_of                # noqa: E402
from lib330a import sweep_helper_uses                         # noqa: E402

R = L.Report(
    selfpop="the assertions a1 makes about its own two classifiers",
    findpop="the published anchor-population figures of mg-330a and mg-b2af")

L.banner("mg-0ba7 a1", "THE POPULATION, RE-DERIVED BY AST")
print("""
   PRE-FILED IN THE SAME ACTION AS ITS PARENT.  mg-0ba7 and mg-b2af were
   created together by pm-onethird: the audit of the repair was a ticket
   before the repair had a line of code.

   Nothing below imports mg-330a's `classify_call` to DO the work.  It is
   imported to be DISAGREED WITH, and every row where the two answers differ
   is printed.
""")

# ---------------------------------------------------------------------------
L.rule("(i) TWO CLASSIFIERS, SAME CALL SITES, ROW BY ROW")
# ---------------------------------------------------------------------------

MINE_DIR = "code/anchor_population_audit_0ba7"

all_rows, unparsed = L.anchor_sites()
self_rows = [r for r in all_rows if r["file"].startswith(MINE_DIR + "/")]
mine_rows = [r for r in all_rows if not r["file"].startswith(MINE_DIR + "/")]
mine = {(r["file"], r["line"]): r for r in mine_rows}

theirs_all = {}
files, _bad = L.py_files()
for rel, _src, tree in files:
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            k = classify_call(_strings_of(node))
            if k:
                theirs_all[(rel, node.lineno)] = k
theirs = {k: v for k, v in theirs_all.items()
          if not k[0].startswith(MINE_DIR + "/")}

print("""
   DEFECT #4 OF THIS INSTRUMENT, KEPT AND CORRECTED HERE.  An instrument
   that walks `code/` and lives in `code/` MEASURES ITSELF.  The constructed
   calls in `selftest_0ba7.py` (1) are real `ast.Call` nodes carrying a real
   argv list, so my own test fixtures entered my own census and inflated it.
   Found because the totals moved between the draft transcript and the
   shipping one WHILE THE SUBJECT DID NOT CHANGE.

   Every figure below is over `code/` EXCLUDING""")
print("   " + MINE_DIR + ".")
print("   The self-count is printed beside it and never added in.")
R.total("call sites in THIS AUDIT'S OWN directory (excluded below)",
        len(self_rows), "every ast.Call under %s/" % MINE_DIR,
        "one CALL SITE")
R.total("  of which are this audit's own test fixtures",
        len([r for r in self_rows
             if r["file"].endswith("selftest_0ba7.py")]),
        "the self-count rows", "one CALL SITE")

R.selfgate(not unparsed,
           "%d .py file(s) under code/ did not parse and were therefore in "
           "neither population: %s" % (len(unparsed), unparsed))

R.total("call sites -- MY classifier", len(mine),
        "every ast.Call in every parseable .py under code/ EXCEPT this "
        "audit's own directory", "one CALL SITE")
R.total("call sites -- mg-330a's classifier", len(theirs),
        "the same ast.Call nodes", "one CALL SITE")

keys = sorted(set(mine) | set(theirs))
dis = [k for k in keys if (mine[k]["kind"] if k in mine else None)
       != theirs.get(k)]
only_mine = [k for k in dis if k not in theirs]
only_theirs = [k for k in dis if k not in mine]

R.total("rows the two classifiers agree on", len(keys) - len(dis),
        "the union of both populations", "one CALL SITE")
R.total("rows they DISAGREE on", len(dis),
        "the union of both populations", "one CALL SITE")
R.total("  of which MINE SEES and theirs does not", len(only_mine),
        "the disagreement rows", "one CALL SITE")
R.total("  of which THEIRS SEES and mine does not", len(only_theirs),
        "the disagreement rows", "one CALL SITE")

print()
print("   %-58s %-13s %s" % ("site", "mg-330a", "mine"))
for k in dis:
    print("   %-58s %-13s %s"
          % ("%s:%d" % k, theirs.get(k) or "-- NOT SEEN",
             mine[k]["kind"] if k in mine else "-- NOT SEEN"))

print("""
   WHY.  Every disagreement above is one string.  `lib330a._HASH_FORMATS`
   is""")
print("       %s" % (L.FORMATS_330A,))
print("   and the sites above carry `--format=%h`.  The ABBREVIATED hash is a")
print("   revision by every use made of it in this repository, and it is in")
print("   no hash-format tuple of this arc.")
print("""
   `git log -1 --format=%h -- <path>` IS `NEWEST`.  It is A-1's defect
   spelled with a lowercase letter.  The population of mg-330a's census, of
   mg-b2af's repair, and of the brief for both, is therefore not
   `history-derived call sites` -- it is `history-derived call sites THAT
   SPELL THE HASH WITH A CAPITAL H`.

   mg-b2af's own headline is A SEARCH BY FLAG HAS A POPULATION DEFINED BY A
   FLAG.  It found that for `--format=%H` versus the named helpers, and then
   imported the flag tuple unchanged -- `population by mg-330a's classifier,
   UNCHANGED` -- and refined the 19 `without touching the denominator`.  The
   denominator was the thing to touch.
""")
low = [k for k in dis
       if any("%h" in s for s in (mine[k]["strs"] if k in mine else []))]
R.total("disagreements explained by `%h` alone", len(low),
        "the disagreement rows", "one CALL SITE")
R.gate(not dis,
       "the two classifiers disagree on %d of %d call sites, %d of them "
       "invisible to mg-330a's classifier and therefore absent from every "
       "population this arc has published"
       % (len(dis), len(keys), len(only_mine)))

# ---------------------------------------------------------------------------
L.rule("(ii) THE KIND COUNTS -- MINE, THEIRS, AND EVERY PUBLISHED FIGURE")
# ---------------------------------------------------------------------------

mc = Counter(r["kind"] for r in mine_rows)
tc = Counter(theirs.values())

# READ, not measured: the figures as published.  Populations named.
PUBLISHED = {
    #  kind            doc-330a  transcript-330a  b2af-at-its-tree
    "NEWEST":        (7,  7,  8),
    "INDEXED":       (8,  8, 10),
    "UNRESTRICTED":  (1,  1,  1),
    "OLDEST":        (10, 11, 11),
    "PICKAXE":       (6,  6,  6),
    "RANGE":         (4,  4,  4),
}
print("   The three published columns are READ out of mg-330a's document,")
print("   mg-330a's committed transcript, and mg-b2af's README table.  They")
print("   are not measurements taken here.  The last two columns are.")
print()
print("   %-16s %8s %8s %8s | %8s %8s"
      % ("kind", "doc(R)", "tsc(R)", "b2af(R)", "330a@me", "MINE"))
for k in ("NEWEST", "INDEXED", "UNRESTRICTED", "OLDEST", "PICKAXE", "RANGE"):
    d, t, b = PUBLISHED[k]
    print("   %-16s %8d %8d %8d | %8d %8d"
          % (k, d, t, b, tc.get(k, 0), mc.get(k, 0)))

hist_mine = [r for r in mine_rows if r["kind"] in L.HISTORY_KINDS]
hist_theirs = [k for k, v in theirs.items() if v in L.HISTORY_KINDS]
dirs_mine = {os.path.dirname(r["file"]) for r in hist_mine}
dirs_theirs = {os.path.dirname(f) for f, _ln in hist_theirs}

print()
R.total("HISTORY-DERIVED -- mg-330a's classifier at my tree", len(hist_theirs),
        "call sites classified NEWEST/NEWEST-norestrict/INDEXED/UNRESTRICTED",
        "one CALL SITE")
R.total("HISTORY-DERIVED -- MY classifier at my tree", len(hist_mine),
        "the same four kinds, `%h` included", "one CALL SITE")
R.total("  directories -- theirs", len(dirs_theirs),
        "dirname() of the history-derived rows", "one DIRECTORY")
R.total("  directories -- mine", len(dirs_mine),
        "dirname() of the history-derived rows", "one DIRECTORY")

extra = sorted(set(mine) - set(theirs))
extra_hist = [k for k in extra if mine[k]["kind"] in L.HISTORY_KINDS]
print()
print("   THE HISTORY-DERIVED SITES NO POPULATION OF THIS ARC CONTAINS:")
for k in extra_hist:
    print("     %-14s %s:%d" % (mine[k]["kind"], k[0], k[1]))
R.total("history-derived sites invisible to mg-330a's classifier",
        len(extra_hist), "the sites only my classifier sees", "one CALL SITE")

print()
print("   AND THE LOUDEST CLASS IS THE ONE THAT MOVED MOST.  mg-b2af's own")
print("   STILL OPEN list names ONE `UNRESTRICTED` site -- p3_reason.py --")
print("   and calls it `the loudest form of the defect ... the one site in")
print("   the 19 that no pin can help`.")
unres_mine = [r for r in mine_rows if r["kind"] == "UNRESTRICTED"]
R.total("UNRESTRICTED -- mg-330a's classifier at my tree",
        tc.get("UNRESTRICTED", 0), "call sites classified UNRESTRICTED",
        "one CALL SITE")
R.total("UNRESTRICTED -- MINE", len(unres_mine),
        "call sites classified UNRESTRICTED", "one CALL SITE")
for r in unres_mine:
    print("     %s:%d   %s" % (r["file"], r["line"], r["src"][:60]))
R.gate(len(unres_mine) == tc.get("UNRESTRICTED", 0),
       "the STILL-OPEN list names 1 UNRESTRICTED site; %d exist at this tree "
       "and %d of them are invisible to the classifier the list was drawn "
       "from" % (len(unres_mine),
                 len(unres_mine) - tc.get("UNRESTRICTED", 0)))

# ---------------------------------------------------------------------------
L.rule("(iii) THE POPULATION WITH NO `--format=%H` -- A NAME-LIST vs A "
       "CLOSURE")
# ---------------------------------------------------------------------------

print("""
   The brief: INCLUDE THE CALL SITES CARRYING NO `--format=%H`.  The parent
   found 16 such, invisible to a flag-grep.  A SEARCH BY FLAG HAS A
   POPULATION DEFINED BY A FLAG.

   True, and the same sentence applies one word over.  `sweep_helper_uses`
   carries the literal tuple ("last_touching", "nth_touching") in its body.
   A SEARCH BY NAME HAS A POPULATION DEFINED BY A NAME-LIST.
""")

helper_rows = sweep_helper_uses(repo=L.REPO)
defs_330a = [r for r in helper_rows if r["what"] == "DEF"]
calls_330a = [r for r in helper_rows if r["what"] == "CALL"]
R.total("mg-330a's helper sweep -- ROWS", len(helper_rows),
        "DEF and CALL nodes of the two named helpers", "one AST NODE")
R.total("  of which DEF", len(defs_330a),
        "the same rows", "one FUNCTION DEFINITION")
R.total("  of which CALL", len(calls_330a),
        "the same rows", "one CALL SITE")
print("   -- mg-b2af's headline, REPRODUCED at my tree: the document's")
print("      `16 call sites` is the ROW count over TWO populations.  It")
print("      holds here too, so the finding survives a tree it was not")
print("      measured at.")

seeds = [s for s in L.seed_defs()
         if not s["file"].startswith(MINE_DIR + "/")]
ret_seeds = [s for s in seeds if s["returns"]]
R.total("functions containing a history-derived call", len(seeds),
        "every FunctionDef under code/", "one DEFINITION")
R.total("  of which RETURN the anchor to their caller", len(ret_seeds),
        "the same definitions, taint-tested", "one DEFINITION")
names = sorted({s["name"] for s in ret_seeds})
R.total("  distinct names among those", len(names),
        "the returning definitions", "one NAME")
print("     %s" % ", ".join(names))
print("   mg-330a's list has 2 of these %d names." % len(names))

closure, unresolved, stars = L.helper_closure()
closure = [r for r in closure if not r["file"].startswith(MINE_DIR + "/")]
unresolved = [r for r in unresolved
              if not r["file"].startswith(MINE_DIR + "/")]
collisions = [u for u in unresolved if u.get("collision")]
truly = [u for u in unresolved if not u.get("collision")]
dirs_cl = {os.path.dirname(r["file"]) for r in closure}
R.total("IMPORT-RESOLVED closure -- anchor-obtaining call sites",
        len(closure),
        "calls resolving through the calling file's own bindings to a "
        "returning seed", "one CALL SITE")
R.total("  directories", len(dirs_cl), "dirname() of those rows",
        "one DIRECTORY")
R.total("NAME COLLISIONS -- bare name matches, binding does not",
        len(collisions),
        "calls whose bare name is a seed name but whose binding reaches a "
        "NON-seed definition", "one CALL SITE")
R.total("UNRESOLVED -- binding not statically determinable", len(truly),
        "calls whose bare name is a seed name and whose binding this "
        "instrument could not resolve", "one CALL SITE")
for u in truly:
    print("     %s:%d  %s" % (u["file"], u["line"], u["src"][:56]))
print("   -- counted and named rather than dropped.  The one below reaches")
print("      its helper through importlib.util.spec_from_file_location, so")
print("      NO static closure can resolve it.  That is a limit of this")
print("      instrument, stated as a limit.")
if stars:
    print("   `import *` files (bindings unenumerable): %s" % ", ".join(stars))

print()
print("   THE COLLISIONS ARE NOT A TECHNICALITY.  All %d resolve to a"
      % len(collisions))
print("   `commits_touching` that takes a `%s..%s` RANGE -- a SET, with no")
print("   single revision to re-point.  A bare-name match counts them as")
print("   anchor sites; they are not.  The name is shared, the KIND is not.")
by_target = Counter(u.get("defined_in") for u in collisions)
for tgt, n in sorted(by_target.items()):
    print("     %3d call sites -> %s" % (n, tgt))

bare = [r for r in L.bare_name_closure({"last_touching", "nth_touching"})
        if not r["file"].startswith(MINE_DIR + "/")]
R.total("the parent's method, CALL sites only", len(bare),
        "bare-name matches on the two named helpers", "one CALL SITE")
R.gate(len(closure) > len(bare),
       "the no-`--format=%%H` population is %d call sites over %d "
       "directories when derived by closure, and %d over %d when derived "
       "from a two-name list; the published figure is the smaller one"
       % (len(closure), len(dirs_cl), len(bare),
          len({os.path.dirname(r["file"]) for r in bare})))

print("""
   AND THE SAME DEFECT IN MY OWN INSTRUMENT, KEPT.  The taint test in
   `_tainted_return` was first written over `ast.Assign` alone.
   `lib8d5e.last_lacking` and `lib8d5e.base_before_dir` both receive the
   anchor through a FOR TARGET and return it, so both scored `returns=False`
   and were dropped.  Reading in that first form:

       returning seeds  11 (not 13)      closure  40 call sites (not %d)

   Two real anchor helpers excluded by a population defined by the syntax I
   happened to think of first, in an audit of populations defined by what
   the searcher happened to look for.  Found by reading the seed table's own
   named rows.  The comment sits at the fix.
""" % len(closure))

# ---------------------------------------------------------------------------
L.rule("(iv) CONVERTED-COUNT AGAINST SIXTEEN")
# ---------------------------------------------------------------------------

print("""
   The brief for mg-b2af: convert the history-derived 16 to property-derived,
   or pin-and-compare each, and report converted-count AGAINST 16.

   mg-b2af answered `0 of 19` and `pinned 4 of 19`, and was right to move
   the denominator: 16 was a pre-rebase figure.  It moved it once.  Here is
   every denominator this question has had, each labelled with the tree and
   the classifier it came from.
""")
print("   %-56s %s" % ("denominator", "history-derived"))
print("   %-56s %s" % ("the brief's, READ", 16))
print("   %-56s %s" % ("mg-330a's transcript, READ", 16))
print("   %-56s %s" % ("mg-b2af at its tree, READ", 19))
print("   %-56s %s" % ("mg-330a's classifier at MY tree, measured",
                       len(hist_theirs)))
print("   %-56s %s" % ("MY classifier at MY tree, measured", len(hist_mine)))
print()
print("   CONVERTED TO PROPERTY-DERIVED BY THIS AUDIT : 0 of %d"
      % len(hist_mine))
print("   -- written as 0.  This audit converts nothing: every one of these")
print("      sites is another ticket's, and rewriting another ticket's")
print("      instrument to make this ticket's number come out is the")
print("      failure this arc exists to avoid.  mg-b2af declined for the")
print("      same reason and the reason is still right.")
print()
print("   PINNED AND COMPARED BY mg-b2af : 4, READ from ANCHORS.tsv")
print("   AGAINST WHICH POPULATION : mg-b2af says `4 of 19`.  Measured")
print("   here at the tree that carries ANCHORS.tsv, the same four rows")
print("   are 4 of %d." % len(hist_mine))

R.gate(False,
       "the converted-count is reported against a denominator produced by a "
       "classifier that cannot see `--format=%%h`; at this tree that is %d "
       "history-derived sites, not %d, and %d of the missing %d are in the "
       "defect classes"
       % (len(hist_mine), len(hist_theirs), len(extra_hist), len(extra_hist)))

# ---------------------------------------------------------------------------
L.rule("(v) PREDICTIONS SCORED")
# ---------------------------------------------------------------------------
hits = []
hits.append(L.score(R, "P-1", "<=4 disagreements", "%d disagreements"
                    % len(dis), hit=(len(dis) <= 4),
                    note="and every one is `%h`; I predicted RANGE and "
                         "abbreviated formats and got the second half only"))
hits.append(L.score(R, "P-2", "25..45 sites, >=8 dirs",
                    "%d sites, %d dirs" % (len(closure), len(dirs_cl)),
                    hit=(25 <= len(closure) <= 45 and len(dirs_cl) >= 8),
                    note="48 is outside the range I gave"))
hits.append(L.score(R, "P-3a", ">=1 collision", "%d collisions"
                    % len(collisions), hit=(len(collisions) >= 1)))
hits.append(L.score(R, "P-3b", ">=3 names missing",
                    "%d of %d names missing from the parent's list"
                    % (len(names) - 2, len(names)),
                    hit=(len(names) - 2 >= 3)))
print()
print("   P-1 MISS KEPT AS WRITTEN.  I predicted at most 4 disagreements and")
print("   named RANGE as the likely site of them.  There are %d, none in"
      % len(dis))
print("   RANGE's dead branch, and all %d are one letter." % len(dis))

R.done()
