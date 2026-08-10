"""mg-223d / R3 -- EVERY RECONSTRUCTION IN THE ARC, AND WHAT THE TWIN WOULD COST.

The ticket asks for the reconstructions specifically, not just the pins.  A
RECONSTRUCTION, for this tree, is a figure whose population is a UNION OF TWO OR
MORE REFS -- not a checkout of one commit, not a glob of the disk.  It is the
class mg-9160 invented and mg-fd9c named, and it is the class the ticket calls
`the arc's ONE stable instrument`.

This probe does two things and refuses to do a third.  It CENSUSES the class
(naming what it rejected, so `one` is a survey result and not a shrug), and it
MEASURES what re-pointing the pin at its on-main twin would do to the published
figures.  It does NOT re-point anything, and it does not recompute a single
figure at HEAD -- the ticket forbids that in its own words and the reason is in
R3d.
"""
import sys

import lib223d as L

led = L.Ledger("mg-223d / R3 -- THE RECONSTRUCTION CENSUS, AND THE COST OF THE TWIN")

# ---------------------------------------------------------------------------
led.head("R3a  THE CLASS, AND THE CANDIDATES REJECTED FROM IT")
# ---------------------------------------------------------------------------
print("""
  A RECONSTRUCTION takes >= 2 refs and unions their contents into ONE
  population.  Three shapes look like it and are not, and saying which is what
  makes `one` a survey rather than a shrug:

    NOT a reconstruction -- A TWO-REF COMPARISON.  `idiom_sweep_audit_18dc`
    reads runner sets at nine refs and DIFFS them.  Nine refs, nine
    populations, no union.  A dead ref there costs one row of a table.

    NOT a reconstruction -- A PIN WITH A FALLBACK.  `repair_b2af` binds
    `INSTR_PRE`/`DOCS_PRE` and reads blobs at them.  One ref per read.

    NOT a reconstruction -- AN ANCHOR.  `publication_anchor_132a`,
    `state_claims_repair_0120` compute a digest over a file list AT one ref.
    One ref, one population, and `0120` already re-pointed its anchor at the
    twin because for a digest the twin IS a substitute.

  THE RULE APPLIED: a directory is a reconstruction if some function of its
  returns a population built from more than one ref.  Searched: every tracked
  `*.py` in every `code/*` directory, for a call to `ls-tree`/`cat-file`/a
  blob read that is parameterised by a ref, appearing more than once with
  DIFFERENT refs inside one population-returning function.""")

dirs = L.suite_dirs("HEAD")
led.record(None, "`code/*` directories searched: %d" % len(dirs))

# The census, by hand and stated as such: the rule above is a reading rule and
# a grep cannot decide `inside one population-returning function`.  What CAN be
# automated is the necessary condition -- more than one distinct ref-bearing
# constant in one file -- and that is what narrows the 179 to the shortlist.
ps = L.pins()
res = L.commits(ps.keys())
byfile = {}
for short, sites in ps.items():
    if short not in res:
        continue
    for p, _i, _t in sites:
        byfile.setdefault(p, set()).add(short)
multi = sorted((p, sorted(v)) for p, v in byfile.items() if len(v) >= 2)
print()
print("      files pinning >= 2 distinct commits (the necessary condition)  %d"
      % len(multi))
for p, shorts in multi:
    print("        %-56s %s" % (p, " ".join(shorts)[:40]))

RECONSTRUCTIONS = [
    ("code/grain_arity_9160", "lib9160.parent_corpus()",
     ["9f1ecaa", "eacc5e1"],
     "everything tracked at 9f1ecaa + mg-03d1's own seven transcripts at "
     "eacc5e1.  THE published 517/1191/246/626/400."),
]
print()
print("      SURVIVORS OF THE READING RULE: %d" % len(RECONSTRUCTIONS))
for d, fn, refs, what in RECONSTRUCTIONS:
    on = [r for r in refs if L.is_ancestor(L.resolve(r), "HEAD")]
    off = [r for r in refs if r not in on]
    print("        %s" % d)
    print("          function : %s" % fn)
    print("          refs     : %s" % ", ".join(refs))
    print("          ancestors of HEAD : %s" % (", ".join(on) or "none"))
    print("          NOT ancestors     : %s" % (", ".join(off) or "none"))
    print("          population: %s" % what)

led.record(None, "reconstructions found: %d" % len(RECONSTRUCTIONS))
led.record(False, "reconstructions with at least one input that is NOT an "
           "ancestor of HEAD: 1 of 1")

# ---------------------------------------------------------------------------
led.head("R3b  THE RECONSTRUCTION STILL REPRODUCES -- TODAY")
# ---------------------------------------------------------------------------
base = L.reconstruction_row()
PUBLISHED = {"files": 517, "rows": 1191, "erows": 246, "eints": 626,
             "words": 400}
print()
print("      %-34s %6s %6s %6s %6s %6s"
      % ("corpus", "files", "rows", "erows", "eints", "words"))
print("      %-34s %6d %6d %6d %6d %6d"
      % ("the reconstruction, run now", base["files"], base["rows"],
         base["erows"], base["eints"], base["words"]))
print("      %-34s %6d %6d %6d %6d %6d"
      % ("mg-03d1's published figures", PUBLISHED["files"], PUBLISHED["rows"],
         PUBLISHED["erows"], PUBLISHED["eints"], PUBLISHED["words"]))
print("      ^ one unit is: one FILE; one printed ROW; one row carrying an")
print("        integer inside its label; one such INTEGER; one de-pluralised NOUN")
led.record(base == PUBLISHED,
           "the reconstruction reproduces the published row field for field")
print("""
      THIS IS THE INSTRUMENT THE TICKET IS ABOUT, and this line is the reason
      it matters: on a disk that has grown by hundreds of files since, a
      figure from an earlier ticket still comes back exactly.  It is the only
      check the arc has that its published numbers were ever right.""")

# ---------------------------------------------------------------------------
led.head("R3c  WHAT THE OBVIOUS REPAIR WOULD COST -- MEASURED, NOT ARGUED")
# ---------------------------------------------------------------------------
twin = L.twin_of(L.resolve("9f1ecaa"))
print()
print("      `9f1ecaa`'s on-main patch-id twin: %s" % (twin[:12] if twin else "none"))
print("      Re-pointing `lib9160.PARENT_REV` at it -- the one-line diff that")
print("      makes every checker in this arc go green -- gives:")
print()
swapped = L.reconstruction_row(twin[:7]) if twin else None
print("      %-34s %6s %6s %6s %6s %6s"
      % ("corpus", "files", "rows", "erows", "eints", "words"))
print("      %-34s %6d %6d %6d %6d %6d"
      % ("PUBLISHED (pin = 9f1ecaa)", base["files"], base["rows"],
         base["erows"], base["eints"], base["words"]))
if swapped:
    print("      %-34s %6d %6d %6d %6d %6d"
          % ("re-pointed  (pin = %s)" % twin[:7], swapped["files"],
             swapped["rows"], swapped["erows"], swapped["eints"],
             swapped["words"]))
    moved = [k for k in PUBLISHED if swapped[k] != base[k]]
    print("      %-34s %6s %6s %6s %6s %6s"
          % ("moved?", *["YES" if k in moved else "no"
                         for k in ("files", "rows", "erows", "eints", "words")]))
    led.record(not moved,
               "columns of the published row that the `obvious repair` would "
               "silently move: %d of 5" % len(moved))
    print("""
      ALL FIVE.  The twin is a different TREE: the rebase replayed the patch
      onto a later main, so `git ls-tree` at the twin returns files that did
      not exist when mg-03d1 ran.  A one-line diff that looks like hygiene
      withdraws five published figures without saying so, and every control in
      this arc would report the result as green because the pin resolves.

      THIS IS E4, IT IS THE MOST AVAILABLE MISTAKE IN THIS TICKET, and the
      only reason it is a printed table here rather than a committed diff is
      that the ticket named it in advance.""")
led.record(None, "the swap was in memory; `lib9160.PARENT_REV` is unchanged on "
           "disk and this tree edits no other tree's files")

# ---------------------------------------------------------------------------
led.head("R3d  AND THE OTHER FORBIDDEN REPAIR: RECOMPUTING AT HEAD")
# ---------------------------------------------------------------------------
print("""
  The ticket: *DO NOT `FIX` THIS BY RECOMPUTING THE FIGURES AT HEAD.*

  I did not, and the reason is not deference.  mg-fd9c already measured what
  recomputation gives -- 832 files / 2093 rows against 517 / 1191 -- and
  established that 21 of 22 arc-wide published figures have moved.  A figure
  recomputed at HEAD agrees with itself and with nothing else; the
  reconstruction's entire value is that it agrees with a number written down
  before the disk changed.  Replacing it would not repair the check, it would
  delete the only one there is.

  WHAT I ALSO DID NOT DO, and it is worth stating because the ticket's
  constraint points at it: I did not make the reconstruction easier to point
  at things.  cfd9c's S3b names four things it cannot do -- it cannot see an
  untracked file, cannot be computed from a single commit, cannot say which
  write regime produced a figure, and needs two refs worked out by hand once
  per figure.  All four are still true.  The repair in R4 makes the two refs
  SURVIVE; it does not make them EASIER TO GET, and a tag on a commit is not
  a method for finding out which commit to tag.""")

sys.exit(led.done())
