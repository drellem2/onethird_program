"""t1_population.py -- THE POPULATION, AND WHETHER THE PUBLISHED FIGURES
REPRODUCE ANYWHERE.

  (i)   THE THREE STATEMENTS OF THE SAME CENSUS, side by side.
  (ii)  DOES EITHER REPRODUCE AT THE COMMIT IT WAS PUBLISHED AT?  Run at the
        commits as they now sit on main AND at their pre-rebase twins.
  (iii) THE REFINEMENT `classify_call` CANNOT MAKE -- pinned revision, literal
        path -- with the denominator left where mg-330a's classifier put it.
  (iv)  THE REFINEMENT DEMONSTRATED BY CONSTRUCTION, not asserted.
  (v)   PIN-AND-COMPARE: ANCHORS.tsv, re-resolved.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import os
import sys

import lib_b2af as L

R = L.Report(
    selfpop="every clone, sweep, parse and git read this script performs, "
            "plus the requirement that each figure attributed to a published "
            "source really appear in that source",
    findpop="the 7 figures the mg-330a document states and the 7 its "
            "transcript states, each checked for reproduction at four "
            "commits, plus every history-derived site's refinement checked "
            "by construction and every ANCHORS.tsv row re-resolved")

L.banner("T1", "THE POPULATION -- STATED THREE TIMES, MEASURED AT FOUR "
               "COMMITS")

# ---------------------------------------------------------------------------
L.rule("(i) THE THREE STATEMENTS OF ONE CENSUS")
# ---------------------------------------------------------------------------
print("""   mg-330a swept the repo once and the answer is written down in
   three places: the brief for THIS ticket, the document
   docs/audit-mg-330a-the-anchor-and-the-term.md, and the transcript
   code/audit_330a/out_s1_anchors.txt.  The document and the transcript
   landed in the SAME COMMIT, fba5f63.

   Every figure below is READ, and the reading is checked: the selftest
   requires each `evidence` string to be present in the file it is
   attributed to.  A figure quoted from a source that does not contain
   it is the failure this whole arc is about.
""")

DOC = "docs/audit-mg-330a-the-anchor-and-the-term.md"
TRANSCRIPT = "code/audit_330a/out_s1_anchors.txt"

# label -> (doc figure, transcript figure, evidence in doc, evidence in
# transcript).  None means the source does not state that figure.
PUBLISHED = [
    ("ALL call sites", 36, 37,
     "**36** revision-producing `git log` call sites",
     "ALL                   37      call sites, walked by ast"),
    ("NEWEST", 7, 7,
     "| **7** | HISTORY-DERIVED",
     "NEWEST                7"),
    ("INDEXED", 8, 8,
     "| **8** | HISTORY-DERIVED",
     "INDEXED               8"),
    ("UNRESTRICTED", 1, 1,
     "| **1** | HISTORY-DERIVED",
     "UNRESTRICTED          1"),
    ("OLDEST", 10, 11,
     "| 10 | **stable** against later edits |",
     "OLDEST                11"),
    ("PICKAXE", 6, 6,
     "| 6 | PROPERTY-DERIVED |",
     "PICKAXE               6"),
    ("RANGE", 4, 4,
     "| 4 | a set, not an anchor |",
     "RANGE                 4"),
    ("HISTORY-DERIVED", 16, 16,
     "**16 history-derived call sites across 13 directories.**",
     "by explicit git log call (ast-walked)        : 16"),
    ("directories", 13, 12,
     "**16 history-derived call sites across 13 directories.**",
     "12 directories.  The two the repair named are two of them."),
    ("helper CALL sites", 16, 12,
     "Plus **16 call sites of the two named helpers**",
     "12 call site(s)"),
]

MEASURED_KEY = {
    "ALL call sites": "ALL", "NEWEST": "NEWEST", "INDEXED": "INDEXED",
    "UNRESTRICTED": "UNRESTRICTED", "OLDEST": "OLDEST",
    "PICKAXE": "PICKAXE", "RANGE": "RANGE",
    "HISTORY-DERIVED": "HISTORY", "directories": "dirs_history",
    "helper CALL sites": "helper_CALL",
}

for label, docfig, trfig, ev_doc, ev_tr in PUBLISHED:
    src_doc = L.git_quiet("show", "%s:%s" % (L.DOCS_POST, DOC))
    src_tr = L.git_quiet("show", "%s:%s" % (L.DOCS_POST, TRANSCRIPT))
    R.check(ev_doc in src_doc,
            "the figure %r is attributed to %s and the string %r is not in "
            "that file at %s" % (label, DOC, ev_doc, L.DOCS_POST))
    R.check(ev_tr in src_tr,
            "the figure %r is attributed to %s and the string %r is not in "
            "that file at %s" % (label, TRANSCRIPT, ev_tr, L.DOCS_POST))

print("   %-22s %-10s %-12s %s" % ("figure", "the doc", "the transcript",
                                   "agree?"))
disagreeing = []
for label, docfig, trfig, _ed, _et in PUBLISHED:
    same = docfig == trfig
    if not same:
        disagreeing.append(label)
    print("   %-22s %-10d %-12d %s"
          % (label, docfig, trfig, "yes" if same else "*** NO"))
print()
print("   figures where the document and its own transcript disagree : %d "
      "of %d" % (len(disagreeing), len(PUBLISHED)))
print("   they are: %s" % ", ".join(disagreeing))
print()
print("   Both landed in %s.  So the disagreement is not two measurements"
      % L.DOCS_POST)
print("   taken at different times -- it is one sweep, written down twice.")

# ---------------------------------------------------------------------------
L.rule("(ii) DO THEY REPRODUCE AT THE COMMITS THEY WERE PUBLISHED AT?")
# ---------------------------------------------------------------------------
print("""   The refinery REBASES a branch before merging it.  Every commit
   gets a new sha and a new base, and a transcript committed on the
   pre-rebase branch then sits inside a commit whose tree it was never
   run against.  mg-132a named that state DISPLACED.

   So the sweep is re-run at FOUR commits: mg-330a's two as they now
   sit on main, and their PRE-REBASE TWINS -- found in the object store
   by matching the subject line, not assumed.
""")

twins = {}
for post, pre_expected in ((L.INSTR_POST, L.INSTR_PRE),
                           (L.DOCS_POST, L.DOCS_PRE)):
    found = L.pre_rebase_twin(post)
    twins[post] = found
    print("   %s %-58s" % (post, L.subject(post)[:58]))
    print("      pre-rebase twin(s) found by subject : %s"
          % (", ".join(h[:7] for h in found) or "NONE"))
    R.check(len(found) == 1,
            "the search for a pre-rebase twin of %s returned %d commits; "
            "this instrument's DISPLACED verdict rests on there being "
            "exactly one" % (post, len(found)))
    if found:
        R.check(found[0].startswith(pre_expected),
                "the pre-rebase twin of %s found in the object store is %s, "
                "and this file names %s.  The written-down value is wrong or "
                "the object store has changed"
                % (post, found[0][:7], pre_expected))
        R.check(not L.is_ancestor(found[0], "HEAD"),
                "%s is reachable from HEAD, so it is not a pre-rebase "
                "original and the whole displacement argument is wrong"
                % found[0][:7])

WHERE = [("%s (on main)" % L.INSTR_POST, L.INSTR_POST),
         ("%s (on main)" % L.DOCS_POST, L.DOCS_POST),
         ("%s (pre-rebase)" % L.INSTR_PRE, L.INSTR_PRE),
         ("%s (pre-rebase)" % L.DOCS_PRE, L.DOCS_PRE),
         ("the worktree", None)]

measurements = {}
for name, rev in WHERE:
    tree = L.REPO if rev is None else L.clone_at(rev)
    measurements[name] = L.census(repo=tree)
    R.check(measurements[name]["unparsed"] == 0,
            "%d file(s) under code/ did not parse at %s; the sweep's own "
            "population is incomplete there"
            % (measurements[name]["unparsed"], name))

print()
print("   %-22s %s" % ("figure", "".join("%-22s" % n for n, _ in WHERE)))
for label, _d, _t, _ed, _et in PUBLISHED:
    key = MEASURED_KEY[label]
    print("   %-22s %s"
          % (label, "".join("%-22d" % measurements[n][key] for n, _ in WHERE)))

print()
print("   AND EVERY PUBLISHED FIGURE, AGAINST EVERY COMMIT.  A figure")
print("   reproduces if SOME commit in the table above gives it.")
print()
print("   %-22s %-8s %-30s %s"
      % ("figure", "stated", "reproduces at", "source"))

unreproducible = []
for label, docfig, trfig, _ed, _et in PUBLISHED:
    key = MEASURED_KEY[label]
    for src, fig in (("the doc", docfig), ("the transcript", trfig)):
        at = [n for n, _ in WHERE if measurements[n][key] == fig]
        if not at:
            unreproducible.append((src, label, fig))
        print("   %-22s %-8d %-30s %s"
              % (label, fig, ", ".join(a.split(" ")[0] for a in at)
                 or "*** NOWHERE", src))

print()
print("   published figures that reproduce at NO commit measured : %d"
      % len(unreproducible))
for src, label, fig in unreproducible:
    print("      %s: %s = %d" % (src, label, fig))

# THE TRANSCRIPT, AS A WHOLE
tr_all = all(measurements["%s (pre-rebase)" % L.INSTR_PRE][MEASURED_KEY[l]]
             == t for l, _d, t, _e, _f in PUBLISHED)
tr_post = all(measurements["%s (on main)" % L.INSTR_POST][MEASURED_KEY[l]]
              == t for l, _d, t, _e, _f in PUBLISHED)
print()
print("   THE TRANSCRIPT'S SEVEN FIGURES, AS ONE SET:")
print("      reproduce at %s, where the commit now sits on main : %s"
      % (L.INSTR_POST, "yes" if tr_post else "*** NO"))
print("      reproduce at %s, its pre-rebase twin                : %s"
      % (L.INSTR_PRE, "yes" if tr_all else "*** NO"))

R.gate(tr_post or not tr_all,
       "mg-330a's transcript %s reproduces EXACTLY at %s -- its pre-rebase "
       "twin -- and at neither of the commits it now sits behind on main.  "
       "The figures are not wrong: they are DISPLACED, in mg-132a's word.  "
       "The refinery rebased the branch, and the tree the sweep ran against "
       "is not the tree inside the commit that carries its output.  Between "
       "the two, mg-132a's own publication_anchor_132a/ landed -- three "
       "history-derived sites in one file -- and hodge_leverage_repair_3f3b/"
       "repair_7e39.py lost the one it had, which is why the census moves "
       "by four sites and the named list moves by five"
       % (TRANSCRIPT, L.INSTR_PRE))

for src, label, fig in unreproducible:
    R.gate(False,
           "%s states %s = %d, and that figure reproduces at NO commit "
           "measured here -- not at either of the two it was published at, "
           "not at their pre-rebase twins, and not at the worktree.  It is "
           "not displaced; it does not correspond to a sweep of this "
           "repository at any of those trees" % (src, label, fig))

print("""
   AND WHAT THE TWO UNREPRODUCIBLE DOCUMENT FIGURES ACTUALLY ARE.
   Named, because a figure said to be wrong without saying what it is
   instead is half an answer:
""")
pre = measurements["%s (pre-rebase)" % L.DOCS_PRE]
print("     `16 call sites of the two named helpers`: the sweep found")
print("     %d DEF and %d CALL rows there, %d in all.  16 is the ROW count"
      % (pre["helper_DEF"], pre["helper_CALL"], pre["helper_rows"]))
print("     reported as a CALL-SITE count -- one number over two")
print("     populations, which is F-2's shape in the census that names it.")
print()
print("     `OLDEST 10`: the sweep found %d.  The document's own table"
      % pre["OLDEST"])
print("     sums to its own ALL -- 7+8+1+10+6+4 = %d -- so the 36 is"
      % (7 + 8 + 1 + 10 + 6 + 4))
print("     arithmetic over the rows, not a measurement, and it inherits")
print("     the row that is off by one.")
print()
print("     `16 history-derived across 13 directories`: %d and %d at the"
      % (pre["HISTORY"], pre["dirs_history"]))
print("     pre-rebase commit, %d and %d at the worktree.  NO commit"
      % (measurements["the worktree"]["HISTORY"],
         measurements["the worktree"]["dirs_history"]))
print("     measured here gives 16 AND 13 together: the two halves of one")
print("     sentence reproduce at DIFFERENT commits.")

R.gate(False,
       "the document's sentence `16 history-derived call sites across 13 "
       "directories` has no single tree behind it: 16 is the pre-rebase "
       "figure (%d directories there) and 13 is the post-rebase figure (%d "
       "history-derived sites there).  Each half is right about a different "
       "tree, which is why neither reading catches it"
       % (pre["dirs_history"], measurements["the worktree"]["HISTORY"]))

# ---------------------------------------------------------------------------
L.rule("(iii) THE REFINEMENT `classify_call` CANNOT MAKE")
# ---------------------------------------------------------------------------
print("""   `classify_call` reads the flags of one call.  It cannot see that

       log -1 --format=%H e5787e1 -- <path>     CANNOT move
       log -1 --format=%H          -- <path>    moves on ANY edit

   are different, and it calls both NEWEST.  Nor can it see that a
   site whose <path> is a PARAMETER is not an anchor at all -- it is a
   facility, and the anchor is at its call sites.  That is F-1's lesson
   one level down: the property is where the value is SPENT.

   THE DENOMINATOR DOES NOT MOVE.  The population below is whatever
   mg-330a's classifier says it is.  Both numbers are printed.
""")

wt = measurements["the worktree"]
hist = sorted(wt["_hist"], key=lambda r: (r["file"], r["line"]))
refined = [(r, L.refine(r)) for r in hist]

print("   %-13s %-53s %-9s %-10s %s"
      % ("kind (theirs)", "site", "revision", "path", "moves?"))
for r, ref in refined:
    print("   %-13s %-53s %-9s %-10s %s"
          % (r["kind"], "%s:%d" % (r["file"], r["line"]), ref["rev"],
             ref["path"], "no -- PINNED" if ref["frozen"] else "yes"))

frozen = [x for x in refined if x[1]["frozen"]]
param = [x for x in refined if x[1]["path"] == "PARAMETER"]
literal_moving = [x for x in refined
                  if x[1]["path"] == "LITERAL" and not x[1]["frozen"]]
print()
print("   POPULATION BY mg-330a's CLASSIFIER, UNCHANGED       : %d"
      % len(refined))
print("     of which the revision is PINNED, so frozen        : %d"
      % len(frozen))
print("     of which the path is a PARAMETER, so the site is")
print("     a facility and the anchor is at its call sites    : %d"
      % len(param))
print("     of which a literal path and no pinned revision")
print("     meet -- an actual, moving, file-anchored anchor   : %d"
      % len(literal_moving))
print("     remainder (no path at all, or a path this")
print("     instrument could not resolve)                     : %d"
      % (len(refined) - len(frozen) - len(param) - len(literal_moving)))

R.check(len(frozen) + len(param) + len(literal_moving) <= len(refined),
        "the refinement's classes overlap; they are reported as a partition")

# ---------------------------------------------------------------------------
L.rule("(iv) THE REFINEMENT, DEMONSTRATED BY CONSTRUCTION")
# ---------------------------------------------------------------------------
print("""   Asserted twice is still asserted once.  A clone, a COSMETIC
   commit -- a comment line -- to each path a spendable site derives
   from, and every such site's answer re-resolved before and after.

   A site called FROZEN must give the same revision across that commit.
   A site called MOVING must give a different one.  A site that
   contradicts its label is a defect in THIS instrument and is reported
   as one.
""")

spendable = [(r, ref) for r, ref in refined if ref["spendable"]]
print("   sites that can be re-resolved from outside : %d of %d"
      % (len(spendable), len(refined)))
print()

probe = L.clone_at("HEAD")
before = {(r["file"], r["line"]): L.resolve_site(r, None, repo=probe)
          for r, _ in spendable}
for path in sorted({ref["literal"] for _r, ref in spendable}):
    L.cosmetic_commit(probe, path)
after = {(r["file"], r["line"]): L.resolve_site(r, None, repo=probe)
         for r, _ in spendable}

print("   %-53s %-8s %-8s %s" % ("site", "label", "moved?", "verdict"))
contradicting = []
for r, ref in spendable:
    key = (r["file"], r["line"])
    moved = before[key] != after[key]
    agrees = moved != ref["frozen"]
    if not agrees:
        contradicting.append(key)
    print("   %-53s %-8s %-8s %s"
          % ("%s:%d" % key, "FROZEN" if ref["frozen"] else "moving",
             "yes" if moved else "no",
             "agrees" if agrees else "*** CONTRADICTS ITS LABEL"))

print()
print("   sites contradicting their label : %d" % len(contradicting))
print("   NON-VACUITY -- distinct outcomes observed : %d"
      % len({before[(r['file'], r['line'])] != after[(r['file'], r['line'])]
             for r, _ in spendable}))
R.check(len({before[(r['file'], r['line'])] != after[(r['file'], r['line'])]
             for r, _ in spendable}) >= 2,
        "every spendable site moved the same way under the cosmetic commit, "
        "so this construction distinguishes nothing and the frozen/moving "
        "split below is unsupported")
R.gate(not contradicting,
       "%d site(s) re-resolved to the opposite of the label this instrument "
       "gave them: %s"
       % (len(contradicting), ", ".join("%s:%d" % k for k in contradicting)))

# ---------------------------------------------------------------------------
L.rule("(v) PIN-AND-COMPARE -- ANCHORS.tsv, RE-RESOLVED")
# ---------------------------------------------------------------------------
print("""   The brief: convert the history-derived sites to property-derived,
   or pin-and-compare each, and report converted-count against the
   population.

   CONVERTED TO PROPERTY-DERIVED: 0, and that is written as 0 rather
   than replaced by a count of some other treatment.  Every one of
   these sites lives in another ticket's directory, most of them carry
   committed transcripts that a signature change would invalidate, and
   rewriting another ticket's instrument to make this ticket's number
   come out is the failure this arc exists to avoid.

   So: PINNED AND COMPARED, in ONE file.  Drift in any of the
   directories below becomes loud HERE.  A site whose path or revision
   comes from a parameter has no revision to pin and is NOT in the
   file -- it is counted and named below instead, because a population
   that quietly drops what it cannot handle is the shape this whole
   arc is about.
""")

pinned = L.read_anchors()
print("   rows in ANCHORS.tsv : %d" % len(pinned))
R.check(len(pinned) == len(spendable),
        "ANCHORS.tsv holds %d rows and %d sites are spendable at this tree; "
        "the file is stale or the population moved" % (len(pinned),
                                                       len(spendable)))

print()
print("   %-53s %-10s %s" % ("site", "pinned", "re-resolved"))
drift = []
for row in pinned:
    match = [r for r, _ in spendable
             if r["file"] == row["file"] and str(r["line"]) == row["line"]]
    if not match:
        drift.append((row["file"], row["line"], row["resolved"], "GONE"))
        print("   %-53s %-10s %s"
              % ("%s:%s" % (row["file"], row["line"]), row["resolved"][:8],
                 "*** THE SITE IS GONE"))
        continue
    got = L.resolve_site(match[0], None)
    same = got == row["resolved"]
    if not same:
        drift.append((row["file"], row["line"], row["resolved"], got))
    print("   %-53s %-10s %s"
          % ("%s:%s" % (row["file"], row["line"]), row["resolved"][:8],
             (got or "NONE")[:8] + ("" if same else "   *** DRIFTED")))

print()
print("   OLDEST rows in the treated population : %d"
      % len([r for r in pinned if r["kind"] == "OLDEST"]))
print("   -- OLDEST is stable against later edits and is NOT the defect.")
print("   Absorbing it would inflate this repair's population, which is")
print("   the mistake mg-330a named and declined to make.")

R.check(not [r for r in pinned if r["kind"] == "OLDEST"],
        "an OLDEST row is in the treated population; the count has grown by "
        "absorbing a class that does not have the defect")
R.gate(not drift,
       "%d pinned anchor(s) no longer resolve to what ANCHORS.tsv records: %s"
       % (len(drift), "; ".join("%s:%s %s -> %s" % d for d in drift)))

print()
print("   CONVERTED TO PROPERTY-DERIVED : 0 of %d" % len(refined))
print("   PINNED AND COMPARED           : %d of %d" % (len(pinned),
                                                       len(refined)))
print("   NOT PINNABLE, AND WHY -- named, not dropped:")
for r, ref in refined:
    if ref["spendable"]:
        continue
    why = ("its path is a parameter" if ref["path"] == "PARAMETER"
           else "it restricts no path at all" if ref["path"] == "NONE"
           else "its revision comes from a parameter"
           if ref["path"] == "LITERAL" else "this instrument could not "
           "resolve its path")
    print("      %-53s %s" % ("%s:%d" % (r["file"], r["line"]), why))

# ---------------------------------------------------------------------------
L.rule("PREDICTIONS SCORED")
# ---------------------------------------------------------------------------
print("   Every row scored against PREDICTIONS.md, committed before any")
print("   script of this instrument existed.  Misses are printed and kept.")
print()

docs_post_ok = all(
    measurements["%s (on main)" % L.DOCS_POST][MEASURED_KEY[l]] == t
    for l, _d, t, _e, _f in PUBLISHED)

L.score(R, "P-2a", True, tr_post,
        note="reproduces exactly at %s" % L.INSTR_POST)
print("          -- the row says `reproduces EXACTLY at %s`.  It does not."
      % L.INSTR_POST)
print("             It reproduces exactly at %s, that commit's PRE-REBASE "
      "twin." % L.INSTR_PRE)
print("             So the figures are DISPLACED and not wrong, which is the")
print("             sentence P-2 reserved for this outcome -- but the row as")
print("             WRITTEN named the wrong commit and is scored a MISS.")
L.score(R, "P-2b", True, docs_post_ok,
        note="reproduces at %s too" % L.DOCS_POST)
print("          -- also a miss, and for the same reason.  The REASON given "
      "for it")
print("             holds: no revision-anchor call site was added between the")
print("             two commits.  %s and %s measure identically, %s and %s"
      % (L.INSTR_PRE, L.DOCS_PRE, L.INSTR_POST, L.DOCS_POST))
print("             measure identically.  The prediction was right about the")
print("             repo and wrong about which tree the commits carry.")
L.score(R, "P-2c", True, len(unreproducible) > 0,
        note="some published figure reproduces nowhere")
print("          -- the two named in advance were `OLDEST 10` and the 16 "
      "helper CALL")
print("             sites.  Both are in the list above, and `ALL 36` is a "
      "third.")
L.score(R, "P-2d", True,
        measurements["%s (pre-rebase)" % L.DOCS_PRE]["dirs_history"] == 13,
        note="13 = history-derived dirs alone, pre-rebase")
print("          -- the row's FIRST half holds: the doc's 13 does reproduce")
print("             somewhere.  Its MECHANISM is refuted.  At the pre-rebase")
print("             commit history-derived-alone and history-union-helpers "
      "are")
print("             BOTH %d; at the worktree both are %d.  The two readings "
      "never"
      % (measurements["%s (pre-rebase)" % L.DOCS_PRE]["dirs_history"],
         wt["dirs_history"]))
print("             differ, so they cannot be what separates 12 from 13.  "
      "The 13")
print("             is the POST-rebase directory count printed beside a "
      "PRE-rebase")
print("             site count -- which is the same displacement again, "
      "inside one")
print("             sentence.  Scored on the mechanism: MISS.")
L.score(R, "P-3a", lambda n: 2 <= n <= 4, len(frozen), note="2 to 4")
L.score(R, "P-3b", lambda n: 8 <= n <= 12, len(param), note="8 to 12")
L.score(R, "P-3c", lambda n: n < 6, len(literal_moving), note="fewer than 6")
L.score(R, "P-3d", 0, len(contradicting))
L.score(R, "P-4a", 0, 0, note="converted to property-derived")
L.score(R, "P-4b", lambda n: 6 <= n <= 10, len(pinned), note="6 to 10")
L.score(R, "P-4c", 1, len([f for f in os.listdir(L.HERE)
                           if f == "ANCHORS.tsv"]),
        note="one file")
L.score(R, "P-4d", 0, len([r for r in pinned if r["kind"] == "OLDEST"]),
        note="no OLDEST absorbed")

L.rule("VERDICT")
print("""   THE POPULATION IS NOT 16 AND IT IS NOT 19.  It is 16 at the tree
   mg-330a swept and 19 at the tree their commit now sits in, and the
   difference is a rebase rather than a mistake.  The number that IS
   wrong is the document's, in three places, and one of those three --
   `16 call sites of the two named helpers` -- is a DEF count and a
   CALL count added together and reported under the CALL label.

   That is F-2's defect, one word over two populations, committed
   inside the census that names F-2.  Seventh consecutive deliverable
   to carry its own defect class.
""")

sys.exit(R.emit())
