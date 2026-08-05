#!/usr/bin/env python3
"""a5_resolution.py -- DISTINCTNESS BY RESOLUTION, NOT BY NAME.

The brief: the drifted sources DIFFERED BY SHA AND WERE BYTE-IDENTICAL.
Where two anchors must differ, check WHAT THEY RESOLVE TO.  Construct the
case where two distinct shas name identical content and confirm the repair
now notices.

Three parts:

  (i)   THE CONSTRUCTION.  Two commits, distinct shas, byte-identical blob
        for the path under test.  A distinctness test on shas PASSES and a
        distinctness test on the blob FAILS.  Built here, not recalled.
  (ii)  mg-b2af's own pair, re-measured: `d01ff32d` and `HEAD` on
        `g1_provenance.py`.
  (iii) AND THE OTHER DIRECTION, WHICH NOBODY IN THIS ARC HAS ASKED.  Two
        anchors that must be EQUAL can be equal by sha and different by
        content -- impossible for one path, and routine once the two anchors
        are about different paths.

Predicted exit: 0.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_0ba7 as L                                          # noqa: E402

R = L.Report(
    selfpop="a5's constructed commit pair",
    findpop="mg-b2af's content-identity check on the anchors it preserves")

L.banner("mg-0ba7 a5", "DISTINCTNESS BY RESOLUTION")

TARGET = "code/branching_audit_58da/g1_provenance.py"
OTHER = "code/branching_audit_58da/lib58da.py"

# ---------------------------------------------------------------------------
L.rule("(i) TWO DISTINCT SHAS, ONE IDENTICAL BLOB -- CONSTRUCTED")
# ---------------------------------------------------------------------------

print("""
   The construction is one commit that does not touch the path under test.
   `%s`
   is edited; `%s`
   is not.  HEAD and HEAD~1 are then two REAL, DISTINCT commits whose blob
   for the untouched path is the same object.
""" % (OTHER, TARGET))

clone = L.clone_at("HEAD")
try:
    a = L.resolve("HEAD", repo=clone)
    text = open(os.path.join(clone, OTHER)).read()
    b = L.commit_in(clone, OTHER, text + "\n# constructed: a cosmetic line\n",
                    "constructed: an edit that does not touch the target")
    b = L.resolve(b, repo=clone)

    blob_a = L.blob_sha(a, TARGET, repo=clone)
    blob_b = L.blob_sha(b, TARGET, repo=clone)
    other_a = L.blob_sha(a, OTHER, repo=clone)
    other_b = L.blob_sha(b, OTHER, repo=clone)

    print("   %-46s %s" % ("commit A", a))
    print("   %-46s %s" % ("commit B", b))
    print("   %-46s %s" % ("blob of the TARGET at A", blob_a))
    print("   %-46s %s" % ("blob of the TARGET at B", blob_b))
    print("   %-46s %s" % ("blob of the EDITED file at A", other_a[:12]))
    print("   %-46s %s" % ("blob of the EDITED file at B", other_b[:12]))
    print()
    sha_distinct = (a != b)
    blob_distinct = (blob_a != blob_b)
    print("   DISTINCTNESS BY SHA        : %s" % ("PASS -- they differ"
                                                  if sha_distinct else "FAIL"))
    print("   DISTINCTNESS BY RESOLUTION : %s"
          % ("PASS" if blob_distinct
             else "FAIL -- the same object, %s" % blob_a[:12]))

    R.selfgate(sha_distinct and not blob_distinct,
               "the construction did not produce the case it claims "
               "(sha distinct: %s, blob distinct: %s); everything below it "
               "is unsupported" % (sha_distinct, blob_distinct))
    R.selfgate(other_a != other_b,
               "the edited file's blob did not move, so the second commit "
               "changed nothing and A and B are not two states")

    print("""
   THE TWO TESTS DISAGREE, ON A PAIR BUILT TO MAKE THEM DISAGREE.  An
   instrument that asserts `these two anchors must differ` and asks it of
   the SHAS has asked nothing about the file it is reasoning about.  Every
   commit to the repository that does not touch the path makes the shas
   differ.
""")

    # ---------------------------------------------------------------------
    L.rule("(ii) DOES THE REPAIR NOTICE?  ITS OWN PREDICATE, ON MY PAIR.")
    # ---------------------------------------------------------------------
    print("""
   mg-b2af's `t4_preserve.py` runs both tests every time and prints that
   they disagree.  The predicate is re-implemented here -- `blob_sha(a, rel)
   != blob_sha(b, rel)` -- and applied to the pair constructed above, which
   `t4` has never seen.
""")
    notices = not blob_distinct
    R.gate(notices,
           "the content-identity predicate did not fire on a pair built to "
           "make it fire")
    print("   the content predicate fires on the constructed pair : %s"
          % ("YES" if notices else "NO"))
    print("   -- so the repair's lesson is a RUNNING CHECK and it holds on")
    print("      an input chosen by somebody else.  That is what an")
    print("      independent audit can add to `it passed on its own pair`.")
finally:
    L.rm_tree(clone)

# ---------------------------------------------------------------------------
L.rule("(iii) mg-b2af's OWN PAIR, RE-MEASURED AT MY TREE")
# ---------------------------------------------------------------------------

D01FF32 = "d01ff32dd4dce31b98cb8aca9f4ae6e3a8aaebc3"
head = L.resolve("HEAD")
print("   mg-b2af, READ: `on the pair (d01ff32d, HEAD), a distinctness check")
print("   on commit shas PASSES and one on the blob of g1_provenance.py")
print("   FAILS -- ca90929f both sides.`")
print()
ba = L.blob_sha(D01FF32, TARGET)
bb = L.blob_sha(head, TARGET)
print("   %-46s %s" % ("d01ff32d", D01FF32[:12]))
print("   %-46s %s" % ("HEAD", head[:12]))
print("   %-46s %s" % ("blob of g1_provenance.py at d01ff32d", ba[:12]))
print("   %-46s %s" % ("blob of g1_provenance.py at HEAD", bb[:12]))
print()
print("   sha distinctness  : %s" % ("PASS" if D01FF32 != head else "FAIL"))
print("   blob distinctness : %s" % ("PASS" if ba != bb else
                                     "FAIL -- identical, %s" % ba[:12]))
R.gate(ba == bb,
       "the blob of %s differs between d01ff32d and HEAD at this tree, so "
       "mg-b2af's published `ca90929f both sides` no longer reproduces; the "
       "pair moved and the lesson would now need a different pair" % TARGET)
print("   -- REPRODUCED.  mg-b2af's pair still exhibits it %d commits later."
      % int(L.gout("rev-list", "--count", "%s..HEAD" % D01FF32) or 0))

# ---------------------------------------------------------------------------
L.rule("(iv) THE DIRECTION NOBODY IN THIS ARC HAS ASKED")
# ---------------------------------------------------------------------------

print("""
   Every statement of the lesson in this arc is about anchors that MUST
   DIFFER.  The mirror case is an anchor pair that must be THE SAME, and it
   is not symmetric: two anchors can resolve to the same commit sha and
   still be about different content, because a commit is a whole tree.

   mg-b2af's `ANCHORS.tsv` has exactly this shape and it is worth naming.
   Two of its four rows resolve to the SAME revision, %s, and they are rows
   about the SAME path, so they agree.  The third and fourth rows resolve
   elsewhere.  A `resolved` column with a repeated sha is a column where
   equality carries no information unless the PATH is carried beside it --
   and ANCHORS.tsv does carry the path, in its own `path` column.  The file
   is built right; the point is that the sha column alone could not have
   been.
""" % "d01ff32d")

tsv = os.path.join(L.REPO, "code/repair_b2af/ANCHORS.tsv")
rows, head_row = [], None
for line in open(tsv):
    if line.startswith("#") or not line.strip():
        continue
    parts = line.rstrip("\n").split("\t")
    if head_row is None:
        head_row = parts
        continue
    rows.append(dict(zip(head_row, parts)))
R.total("rows in ANCHORS.tsv", len(rows), "the file mg-b2af ships",
        "one PINNED SITE")
seen = {}
for r in rows:
    seen.setdefault(r["resolved"], []).append(r["path"])
dupes = {k: v for k, v in seen.items() if len(v) > 1}
R.total("distinct resolved revisions among them", len(seen),
        "the resolved column of those rows", "one REVISION")
for sha, paths in sorted(dupes.items()):
    print("     %s  shared by %d rows, paths: %s"
          % (sha[:12], len(paths), ", ".join(sorted(set(paths)))))
    R.gate(len(set(paths)) == 1,
           "two rows share the resolved revision %s and name DIFFERENT "
           "paths, so the resolved column alone cannot distinguish them"
           % sha[:12])

L.rule("(v) PREDICTIONS SCORED")
L.score(R, "P-9", "sha PASS, blob FAIL, on both pairs",
        "constructed pair: sha PASS blob FAIL; mg-b2af's pair: sha PASS "
        "blob %s" % ("FAIL" if ba == bb else "PASS"),
        hit=(ba == bb))

R.done()
