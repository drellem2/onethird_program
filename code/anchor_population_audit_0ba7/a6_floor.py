#!/usr/bin/env python3
"""a6_floor.py -- THE FLOOR ITEM: A POPULATION DEFINED BY THE WORD `log`.

The standing instruction: FLOOR, NOT SCOPE -- audit one thing no list in the
brief names.  This is that one, and it was named in PREDICTIONS.md (P-10)
before any script here existed.

mg-330a's `classify_call` returns `None` unless the call carries BOTH a `log`
argument AND a hash format.  mg-b2af inherited it deliberately and refined
the result `without touching the denominator`.  So every population this arc
has published -- 36, 37, 40, 16, 19 -- is a population of

    REVISION-PRODUCING CALLS THAT USE `git log` WITH AN EXPLICIT HASH FORMAT.

`git rev-parse`, `git rev-list`, `git merge-base` and `git describe` produce
revisions and carry neither.  `git rev-parse HEAD` is the `UNRESTRICTED`
defect -- the one mg-b2af's STILL-OPEN list calls `the loudest form` -- in
four fewer characters.

Predicted exit: 1.
"""
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_0ba7 as L                                          # noqa: E402

R = L.Report(
    selfpop="a6's own command classification",
    findpop="the revision-producing call sites of this repository that are "
            "in no published population of this arc")

L.banner("mg-0ba7 a6", "THE FLOOR: REVISIONS PRODUCED WITHOUT `log`")

# ---------------------------------------------------------------------------
L.rule("(i) THE POPULATION NOBODY HAS ENUMERATED")
# ---------------------------------------------------------------------------

MINE_DIR = "code/anchor_population_audit_0ba7"
rows = [r for r in L.rev_command_sites()
        if not r["file"].startswith(MINE_DIR + "/")]
print("   EXCLUDING %s/ -- see a1 (i), DEFECT #4." % MINE_DIR)
c = Counter(r["cmd"] for r in rows)
R.total("call sites using one of %s" % (L.REV_COMMANDS,), len(rows),
        "every ast.Call under code/ whose direct string arguments name one "
        "of those four commands", "one CALL SITE")
for k in sorted(c):
    R.total("  %s" % k, c[k], "the same call sites", "one CALL SITE")

anchor_rows, _bad = L.anchor_sites()
anchor_rows = [r for r in anchor_rows
               if not r["file"].startswith(MINE_DIR + "/")]
anchor_keys = {(r["file"], r["line"]) for r in anchor_rows}
overlap = [r for r in rows if (r["file"], r["line"]) in anchor_keys]
R.total("of those, ALSO in my `git log` census", len(overlap),
        "the rev-command call sites", "one CALL SITE")
R.total("in NO population this arc has published", len(rows) - len(overlap),
        "the rev-command call sites minus the overlap", "one CALL SITE")

# ---------------------------------------------------------------------------
L.rule("(ii) WHICH OF THEM ARE ANCHORS, AND WHICH ARE NORMALISATIONS")
# ---------------------------------------------------------------------------

print("""
   Not every one is a defect and saying so would be A-2's mistake in the
   other direction -- a term denoting more than it covers.  `rev-parse` of a
   literal 40-character sha NORMALISES a revision somebody already chose; it
   cannot re-point.  `rev-parse HEAD` DERIVES one, and re-points on every
   commit to the repository rather than to any one file.

   The split below is by whether the call's own string arguments mention
   `HEAD` or name no revision at all.  That rule is stated because it is
   approximate: a call whose revision arrives as a PARAMETER is counted
   MOVING here and mg-b2af's own refinement would call it a facility.  Both
   readings are printed.
""")
moving = [r for r in rows if r["moving"]]
pinned = [r for r in rows if not r["moving"]]
R.total("MOVING -- mentions HEAD, or names no revision", len(moving),
        "the %d rev-command call sites" % len(rows), "one CALL SITE")
R.total("otherwise", len(pinned),
        "the %d rev-command call sites" % len(rows), "one CALL SITE")

head_only = [r for r in rows if "HEAD" in " ".join(r["strs"])]
R.total("mentioning HEAD explicitly", len(head_only),
        "the %d rev-command call sites" % len(rows), "one CALL SITE")
dirs = {os.path.dirname(r["file"]) for r in head_only}
R.total("  directories they live in", len(dirs),
        "dirname() of those rows", "one DIRECTORY")

print()
print("   THE `HEAD` ONES, BY DIRECTORY -- the UNRESTRICTED shape, spelled")
print("   without `log`:")
bydir = Counter(os.path.dirname(r["file"]) for r in head_only)
for d, n in sorted(bydir.items(), key=lambda kv: (-kv[1], kv[0]))[:12]:
    print("     %3d  %s" % (n, d))
if len(bydir) > 12:
    print("     ... and %d more directories" % (len(bydir) - 12))

print("""
   mg-b2af's STILL OPEN list, READ:

       `code/repair_69d1/p3_reason.py (i-b) still anchors its control on
       HEAD -- UNRESTRICTED, the loudest form of the defect ... the one site
       in the 19 that no pin can help, because HEAD moves on every commit to
       the repository rather than to a file.`

   The sentence is right about `HEAD`.  `the one site` is a count over a
   population that cannot contain any of the %d above, because none of them
   says `log`.
""" % len(head_only))

R.gate(not head_only,
       "%d call sites in %d directories derive a revision from HEAD through "
       "rev-parse/rev-list/merge-base/describe; every population this arc "
       "has published requires the word `log` and a hash format, so none of "
       "them has ever been counted, and the STILL-OPEN list calls the one "
       "site it can see `the one site`"
       % (len(head_only), len(dirs)))

# ---------------------------------------------------------------------------
L.rule("(iii) A SAMPLE, NAMED, SO THE NUMBER IS CHECKABLE")
# ---------------------------------------------------------------------------

print("   %-52s %-11s %s" % ("site", "command", "source"))
for r in sorted(head_only, key=lambda r: (r["file"], r["line"]))[:20]:
    print("   %-52s %-11s %s"
          % ("%s:%d" % (r["file"], r["line"]), r["cmd"], r["src"][:44]))
if len(head_only) > 20:
    print("   ... and %d more; the full list is this script's own output "
          "under a wider terminal" % (len(head_only) - 20))

# ---------------------------------------------------------------------------
L.rule("(iv) AND THE HONEST LIMIT OF MY OWN FLOOR")
# ---------------------------------------------------------------------------

print("""
   `REV_COMMANDS` is a four-entry tuple in `lib_0ba7.py`.  IT IS A
   NAME-LIST, and a name-list is what this whole audit is about.  Commands
   that also produce a revision and are not in it include `git show
   --format=%H`, `git for-each-ref`, `git reflog`, `git name-rev`, `git
   blame` and `git stash list`, and a call that builds its argv from a
   variable is invisible to every AST rule here.

   So the number in (i) is A LOWER BOUND, and it is labelled one.  I am not
   going to close this audit by claiming the enumeration I criticise others
   for not having is complete in my hands.
""")
extra = ("show", "for-each-ref", "reflog", "name-rev", "blame")
files, _ = L.py_files()
files = [f for f in files if not f[0].startswith(MINE_DIR + "/")]
import ast                                                    # noqa: E402
more = 0
for rel, _src, tree in files:
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            s = L.direct_strings(n)
            if any(x in s for x in extra) and not any(
                    x in s for x in L.REV_COMMANDS):
                more += 1
R.total("call sites naming one of %s, not counted above" % (extra,), more,
        "every ast.Call under code/ naming one of those five commands and "
        "none of the four in REV_COMMANDS", "one CALL SITE")
print("   -- not all of these produce a revision.  The figure is printed to")
print("      size the gap, not to be added to anything.")

L.rule("(v) PREDICTIONS SCORED")
L.score(R, "P-10", "5..40 sites in no published population",
        len(rows) - len(overlap),
        hit=(5 <= len(rows) - len(overlap) <= 40),
        note="I was an order of magnitude low; I predicted the CLASS "
             "existed and guessed its size from nothing")

R.done()
