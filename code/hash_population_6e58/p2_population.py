"""p2_population.py -- THE FOUR DENOMINATORS, AND WHAT MOVES BETWEEN THEM.

The brief: "RE-DERIVE every count in this lineage over the corrected
denominator and publish before/after."

Every figure printed here is at MY tree.  mg-330a's and mg-b2af's published
figures were measured at THEIR trees, and mg-b2af's own headline is that a
figure and the commit carrying it can be two different trees.  So a
before/after is only honest if BOTH halves are measured here, and that is
what this script does: one ast walk, four filters over it, one variable
changed between them.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import lib6e58 as L

R = L.Report(selfpop="this script's own classification, checked against "
                     "mg-330a's over the same ast.Call nodes",
             findpop="`git log` call sites in `code/**/*.py` at this tree")

calls, unparsed = L.all_calls()
cens = {p: L.census(p, calls=calls) for p in L.POPULATIONS}

print("=" * 74)
print("p2 -- THE DENOMINATOR, BEFORE AND AFTER")
print("=" * 74)
print()
print("   tree            : the worktree of branch polecat-z6e58")
print("   file population : every `*.py` under `code/`, walked with `ast`")
print("   ast.Call nodes  : %d" % len(calls))
print("   unparsed files  : %d" % len(unparsed))
for rel, exc in unparsed:
    print("      UNPARSED %s -- %s" % (rel, exc))
print()

R.check(not unparsed, "%d file(s) did not parse; the walk is incomplete"
                      % len(unparsed))

# ---------------------------------------------------------------------------
print("-- (i) THE CONTROL: MY CLASSIFIER IS mg-330a's UNDER POP-A")
print()
print("   `classify_call` here was written from mg-330a's DOCSTRING, not")
print("   imported.  If the two disagree under POP-A, then a difference in")
print("   any count below could be a re-taxonomy rather than a denominator,")
print("   and this whole script would be measuring the wrong thing.")
print()

disagree = []
for c in calls:
    mine = L.classify_call(c["strs"], L.POP_A)
    theirs = L330 = __import__("lib330a").classify_call(c["strs"])
    if mine != theirs:
        disagree.append((L.site_key(c), mine, theirs))
print("   nodes compared               : %d" % len(calls))
print("   kind disagreements under POP-A: %d" % len(disagree))
for k, m, t in disagree[:20]:
    print("      %-58s mine=%s theirs=%s" % (k, m, t))
print()
R.check(not disagree,
        "%d call(s) are classified differently by my classifier and "
        "mg-330a's under the SAME population; the before/after below cannot "
        "be attributed to the denominator: %s" % (len(disagree),
                                                  disagree[:5]))

# ---------------------------------------------------------------------------
print("-- (ii) THE FOUR POPULATIONS")
print()
for p in L.POPULATIONS:
    print("   %-6s %s" % (p, L.POP_WHAT[p]))
print()

kinds = ("ALL", "HISTORY") + L.ALL_KINDS
print("   %-20s %8s %8s %8s %8s" % ("figure", "POP-A", "POP-B", "POP-C",
                                    "POP-D"))
print("   %-20s %8s %8s %8s %8s" % ("", "(mg-330a)", "(+%h)", "(doc)",
                                    "(+dflt)"))
for k in kinds:
    print("   %-20s %8d %8d %8d %8d"
          % (k, cens[L.POP_A][k], cens[L.POP_B][k], cens[L.POP_C][k],
             cens[L.POP_D][k]))
print()
print("   GRAIN: one `ast.Call` node = one site.  POPULATION: every `*.py`")
print("   under `code/` at this tree.  These are NOT mg-330a's published")
print("   figures and are not comparable to them -- see (vi).")
print()

R.check(L.sites(cens[L.POP_A]) <= L.sites(cens[L.POP_B]) <=
        L.sites(cens[L.POP_C]) <= L.sites(cens[L.POP_D]),
        "the four populations are not nested; a wider denominator that "
        "drops a site is a re-taxonomy, not a widening")

# ---------------------------------------------------------------------------
print("-- (iii) POP-B MINUS POP-A: WHAT THE CAPITAL LETTER HID")
print()

sa, sb, sc, sd = (L.sites(cens[p]) for p in L.POPULATIONS)
rows_b = [r for r in cens[L.POP_B]["_rows"] if L.site_key(r) not in sa]
print("   sites recovered by adding the ONE literal `--format=%%h` : %d"
      % len(rows_b))
print()
print("   %-58s %s" % ("site", "kind"))
for r in sorted(rows_b, key=L.site_key):
    print("   %-58s %s" % (L.site_key(r), r["kind"]))
print()
defect_kinds = ("NEWEST", "INDEXED")
in_defect = [r for r in rows_b if r["kind"] in defect_kinds]
print("   of those, in A-1's DEFECT CLASSES (NEWEST/INDEXED)       : %d"
      % len(in_defect))
print("   `git log -1 --format=%h -- <path>` IS `NEWEST`.  It is A-1's")
print("   defect spelled with a lower-case letter, and the classifier that")
print("   named A-1 cannot see it.")
print()

# ---------------------------------------------------------------------------
print("-- (iv) POP-C MINUS POP-B: WHY `+%h` IS NOT THE REPAIR")
print()

rows_c = [r for r in cens[L.POP_C]["_rows"] if L.site_key(r) not in sb]
by_why = {}
for r in rows_c:
    for sp, grain, why in L.hash_emitters(r["strs"]):
        by_why.setdefault((grain, why.split(":")[0].strip()), []).append(
            (L.site_key(r), sp, r["kind"]))

print("   sites STILL hidden after the one-line `+%%h` repair      : %d"
      % len(rows_c))
print()
full_only = [r for r in rows_c
             if all(g == "FULL" for _, g, _ in L.hash_emitters(r["strs"]))]
print("   OF THOSE, HOW MANY EMIT A **FULL** `%%H` HASH            : %d"
      % len(full_only))
print()
print("   THIS IS THE FINDING.  Those sites contain `%H` -- the very")
print("   placeholder `_HASH_FORMATS` is built out of -- and are invisible")
print("   to it anyway, because `f in strs` is EQUALITY and the format")
print("   string is longer than the literal.  `--format=%H %s` is a full")
print("   commit hash with a subject stapled to it and there is no lower")
print("   case anywhere in it.")
print()
print("   SO THE OMISSION WAS NEVER ONLY ABOUT CASE.  A repair that adds a")
print("   fourth literal to the tuple fixes THIS INSTANCE of a class with")
print("   at least two members, and the arc has now done that eight times.")
print()
print("   %-58s %-6s %s" % ("site", "kind", "how it emits a commit"))
for r in sorted(rows_c, key=L.site_key):
    ems = L.hash_emitters(r["strs"])
    print("   %-58s %-6s %s"
          % (L.site_key(r), r["kind"],
             "; ".join("%s [%s]" % (w, g) for _, g, w in ems[:2])))
print()

spellings = {}
for r in cens[L.POP_C]["_rows"]:
    for sp, grain, why in L.hash_emitters(r["strs"]):
        spellings.setdefault(sp, [0, grain, why])[0] += 1
print("   EVERY SPELLING PRESENT AT THIS TREE, and whether mg-330a's tuple")
print("   matches it:")
print()
print("   %-32s %5s %-7s %-22s %s" % ("spelling", "sites", "grain", "why",
                                      "in _HASH_FORMATS?"))
for sp in sorted(spellings):
    n, grain, why = spellings[sp]
    print("   %-32s %5d %-7s %-22s %s"
          % (repr(sp)[1:-1][:32], n, grain, why,
             "YES" if sp in L.A330._HASH_FORMATS else "no"))
print()
print("   The three `YES` rows are the whole of mg-330a's denominator.")
print("   `--format=format:%H` is in the tuple and is at NO site here, so")
print("   the tuple's effective width at this tree is TWO spellings.")
print()

# ---------------------------------------------------------------------------
print("-- (v) POP-D MINUS POP-C: THE UNFORMATTED `git log`")
print()

rows_d = [r for r in cens[L.POP_D]["_rows"] if L.site_key(r) not in sc]
print("   `git log` calls with NO format argument at all           : %d"
      % len(rows_d))
for r in sorted(rows_d, key=L.site_key):
    print("      %-58s %-6s %s" % (L.site_key(r), r["kind"], r["src"][:40]))
print()
print("   git's documented default is `medium` and it prints")
print("   `commit <hash>`, so an unformatted `git log` IS revision-producing")
print("   by the same rule that admits every row above.")
print()
print("   NOW ADJUDICATE THEM BY HAND, because a count nobody looked at is")
print("   how this arc got here.")
print()
print("   THE ADJUDICATION IS KEYED ON THE SOURCE TEXT, NOT ON `file:line`.")
print("   Its first form keyed on `file:line`, and the line for my own")
print("   `lib6e58.py` moved from 353 to 363 when I edited the file above")
print("   it -- so the verdict for a site I had already read came back")
print("   `NOT ADJUDICATED` because an unrelated edit shifted a number.")
print("   That is A-1, mg-2c77's original defect, committed inside its own")
print("   arc's repair by me, and the fix is the one this lineage keeps")
print("   arriving at: key on a PROPERTY, not on a position.")
print()
ADJUDICATED = [
    ("code/audit_330a/lib330a.py", 's == "log" or s.endswith("log")',
     "NOT A GIT CALL.  It is `s.endswith(\"log\")` -- the string 'log' is "
     "an argument to endswith, inside mg-330a's OWN detector."),
    ("code/repair_b2af/lib_b2af.py", 'a.value.endswith(',
     "NOT A GIT CALL.  mg-b2af's copy of the same detector."),
    ("code/hash_population_6e58/lib6e58.py", 's == "log" or s.endswith("log")',
     "NOT A GIT CALL.  MY OWN detector, matching itself.  Disclosed rather "
     "than excluded."),
    ("code/hash_population_6e58/selftest_6e58.py",
     's == "log" or s.endswith("log")',
     "NOT A GIT CALL.  My selftest's residual check, likewise."),
    ("code/census_repair_f3ff/s1_rows.py", "banner",
     "NOT A GIT CALL.  A banner string that ends in 'log'."),
    ("code/runner_exit_c2b3/k4_control.py", "os.path.join",
     "NOT A GIT CALL.  `os.path.join(tmp, \"reach.log\")` -- a FILENAME."),
]


def adjudicate(row):
    for f, mark, verdict in ADJUDICATED:
        if row["file"] == f and mark in row["src"]:
            return verdict
    return None


bad, unread = 0, []
for r in sorted(rows_d, key=L.site_key):
    verdict = adjudicate(r)
    if verdict is None:
        unread.append(L.site_key(r))
    else:
        bad += 1
    print("      %-58s %s" % (L.site_key(r), verdict or "*** NOT ADJUDICATED"))
print()
print("   ALL %d ARE FALSE POSITIVES, and none is a `git log` call." % bad)
print("   NOT ADJUDICATED: %d" % len(unread))
print("   So the honest POP-D increment at this tree is ZERO, and the number")
print("   printed above is a property of the DETECTOR, not of the tree.")
print()
print("   THE DETECTOR IS mg-330a's, AND THIS IS ITS OTHER HALF.  The `log`")
print("   test is `s == \"log\" or s.endswith(\"log\")` -- it matches a")
print("   filename, a banner, and the word inside its own source.  It is")
print("   sound only because the FORMAT half throws those away first.  The")
print("   two halves of that rule have very different error rates, and only")
print("   the format half was ever audited.  I am not repairing the `log`")
print("   half: it is out of this ticket's scope, and every count above")
print("   holds it fixed so the delta is attributable to the denominator.")
print("   Recorded here so it is not found for a tenth time.")
print()
R.check(not unread,
        "%d POP-D row(s) were counted and never read: %s.  An unexamined "
        "count is what this ticket is about." % (len(unread), unread))
print()

# ---------------------------------------------------------------------------
print("-- (vi) THE CONSUMERS.  WHICH PUBLISHED FIGURES INHERIT THE OMISSION")
print()
print("   Not `which constant is wrong` -- WHICH NUMBERS CHANGE.  Every")
print("   figure below was computed over `_HASH_FORMATS`, by")
print("   `lib330a.sweep_anchor_calls` directly or through")
print("   `lib_b2af.census`, which imports it.")
print()

CONSUMERS = [
    ("code/audit_330a/lib330a.py:218", "the constant itself",
     "3 literals", "unchanged by this ticket -- see README"),
    ("code/audit_330a/s1_anchors.py", "the census that produced mg-330a's "
     "table", "37 sites", "re-derived below"),
    ("code/audit_330a/out_s1_anchors.txt", "its committed transcript",
     "37/16/12", "evidence of a run; left as it is"),
    ("code/audit_330a/README.md", "the audit's own table",
     "36/16/13", "annotated, not rewritten"),
    ("docs/audit-mg-330a-the-anchor-and-the-term.md", "**MERGED DOCUMENT**",
     "36 sites; 16 across 13 dirs", "MERGED -- named, not rewritten"),
    ("code/repair_b2af/lib_b2af.py:295", "`census()` imports the sweep",
     "all ten figures", "re-derived below"),
    ("code/repair_b2af/t1_population.py", "the four-commit reproduction",
     "the PUBLISHED table", "its rows inherit the denominator"),
    ("code/repair_b2af/ANCHORS.tsv", "the pin-and-compare file",
     "4 rows", "drawn from the narrow population"),
    ("code/repair_b2af/README.md", "the census table + STILL-OPEN list",
     "36/7/8/1/10/6/4/16/13/16", "STILL-OPEN corrected by p3"),
    ("code/repair_b2af/selftest_b2af.py:272", "the ALL == sum(kinds) identity",
     "structural", "still true; it is a sum, not a denominator"),
    ("code/repair_b2af/PREDICTIONS.md", "37 pre-registered rows",
     "several over the census", "pre-registration; never reworded"),
]
print("   %-46s %s" % ("consumer", "what it states / what happens to it"))
for path, what, fig, fate in CONSUMERS:
    print("   %-46s %s" % (path, what))
    print("   %-46s   states: %s" % ("", fig))
    print("   %-46s   here  : %s" % ("", fate))
print()
print("   ELEVEN consumers, and ONE of them is a MERGED document in")
print("   `docs/`.  That answers the ticket's question directly: yes, a")
print("   figure computed over the narrow denominator is asserted in a")
print("   merged commit.")
print()

# ---------------------------------------------------------------------------
print("-- (vii) BEFORE AND AFTER, FOR THE FIGURES THIS LINEAGE PUBLISHES")
print()
print("   Column 1 is what somebody published and AT WHICH TREE.  Columns 2")
print("   and 3 are BOTH measured here, at my tree, because a before/after")
print("   across two trees measures the trees.")
print()
print("   %-18s %-26s %8s %8s %8s" % ("figure", "published (tree)", "POP-A",
                                      "POP-C", "delta"))
PUBLISHED = [
    ("ALL call sites", "36 doc / 37 transcript (mg-330a)", "ALL"),
    ("NEWEST", "7 (mg-330a)", "NEWEST"),
    ("INDEXED", "8 (mg-330a)", "INDEXED"),
    ("UNRESTRICTED", "1 (mg-330a)", "UNRESTRICTED"),
    ("OLDEST", "10 doc / 11 transcript", "OLDEST"),
    ("PICKAXE", "6 (mg-330a)", "PICKAXE"),
    ("RANGE", "4 (mg-330a)", "RANGE"),
    ("HISTORY-DERIVED", "16 (mg-330a)", "HISTORY"),
]
for label, pub, key in PUBLISHED:
    a, c = cens[L.POP_A][key], cens[L.POP_C][key]
    print("   %-18s %-26s %8d %8d %+8d" % (label, pub, a, c, c - a))
print()
dirs_a = {r["file"].rsplit("/", 1)[0] for r in cens[L.POP_A]["_rows"]
          if r["kind"] in L.HISTORY_KINDS}
dirs_c = {r["file"].rsplit("/", 1)[0] for r in cens[L.POP_C]["_rows"]
          if r["kind"] in L.HISTORY_KINDS}
print("   %-18s %-26s %8d %8d %+8d"
      % ("directories", "13 doc / 12 transcript", len(dirs_a), len(dirs_c),
         len(dirs_c) - len(dirs_a)))
print()
MINE = "code/hash_population_6e58"
for p in (L.POP_A, L.POP_C):
    mine = [r for r in cens[p]["_rows"] if r["file"].startswith(MINE)]
    print("   %-6s including my own directory : %3d   excluding it : %3d"
          % (p, cens[p]["ALL"], cens[p]["ALL"] - len(mine)))
print("   This instrument is INSIDE the population it counts.  Both numbers")
print("   are printed so that neither reading is the one you have to take.")
print("   They are equal: my own directory contributes ZERO sites to POP-A")
print("   and POP-C -- and exactly ONE false positive to POP-D, adjudicated")
print("   in (v).  I am not outside my own population; I am empty in it.")
print()
print("   NONE of the published figures in column 1 was measured at this")
print("   tree, and mg-b2af showed that mg-330a's ten reproduce exactly at")
print("   its PRE-REBASE twin and at neither commit on `main`.  So the")
print("   right reading of this table is the DELTA column: that is what the")
print("   denominator was worth, held at one tree.")
print()

# ---------------------------------------------------------------------------
print("-- SCORING PREDICTIONS.md")
print()
L.score(R, "D-1", 45, cens[L.POP_A]["ALL"],
        note="disclosed as already measured, not predicted")
L.score(R, "D-2", 15, len(rows_b), note="already measured")
L.score(R, "P2-a", 60, cens[L.POP_B]["ALL"])
L.score(R, "P2-b", 87, cens[L.POP_C]["ALL"])
L.score(R, "P2-c", lambda n: n >= 20, cens[L.POP_C]["ALL"] -
        cens[L.POP_B]["ALL"], note="POP-C - POP-B >= 20")
L.score(R, "P2-c*", lambda n: n >= 15, len(full_only),
        note=">= 15 of the increment are FULL-hash sites")
L.score(R, "P2-d", 4, cens[L.POP_D]["ALL"] - cens[L.POP_C]["ALL"])
grew = [k for k in L.ALL_KINDS if cens[L.POP_C][k] > cens[L.POP_A][k]]
L.score(R, "P2-e", True, "RANGE" not in grew and len(grew) >= 4,
        note="every kind except RANGE grows")
L.score(R, "P2-f", True, cens[L.POP_C]["PICKAXE"] > cens[L.POP_A]["PICKAXE"],
        note="low confidence: PICKAXE grows too")
print()
print("   THE MISSES, KEPT AS WRITTEN AND EXPLAINED RATHER THAN CORRECTED:")
print()
print("   P2-b  I predicted 87 by adding up the occurrence counts of each")
print("         spelling.  Occurrences are not sites: %d spelling"
      % sum(n for n, _, _ in spellings.values()))
print("         occurrences sit in %d calls, because one call can carry two"
      % cens[L.POP_C]["ALL"])
print("         spellings.  I predicted a sum over the WRONG GRAIN -- in a")
print("         ticket about naming the grain.  Off by one.")
print("   P2-d  I predicted 4 and there are %d, and ALL of them are FALSE"
      % len(rows_d))
print("         POSITIVES of mg-330a's `log` half (see (v)).  The prediction")
print("         and the measurement are both about a number that should be")
print("         zero.  The figure is not quoted anywhere in this ticket's")
print("         prose and is printed from the run instead, because it MOVED")
print("         WHILE I WAS WRITING: two of the rows are my own scripts,")
print("         which entered the population as I added them.  A sentence")
print("         with the number in it would have been stale by the commit")
print("         that shipped it.")
print("   P2-e  `every kind except RANGE grows` is false in BOTH directions:")
print("         RANGE grew (+%d) and OLDEST did not (+%d).  I had assumed a"
      % (cens[L.POP_C]["RANGE"] - cens[L.POP_A]["RANGE"],
         cens[L.POP_C]["OLDEST"] - cens[L.POP_A]["OLDEST"]))
print("         range never carries a short format and that OLDEST would")
print("         pick up a `--reverse --format=%h`.  Neither held.")
print()

# ---------------------------------------------------------------------------
R.gate(cens[L.POP_C]["ALL"] == cens[L.POP_A]["ALL"],
       "THE DENOMINATOR IS WRONG BY %d SITES AT THIS TREE: mg-330a's "
       "`_HASH_FORMATS` admits %d `git log` call sites and git's own "
       "documented spellings admit %d.  %d of the hidden sites are in the "
       "defect classes NEWEST/INDEXED, and %d of them emit a FULL `%%H` "
       "hash -- so the omission is not only the lower-case `%%h`."
       % (cens[L.POP_C]["ALL"] - cens[L.POP_A]["ALL"], cens[L.POP_A]["ALL"],
          cens[L.POP_C]["ALL"],
          len([r for r in cens[L.POP_C]["_rows"]
               if L.site_key(r) not in sa and r["kind"] in defect_kinds]),
          len(full_only)))

raise SystemExit(R.emit())
