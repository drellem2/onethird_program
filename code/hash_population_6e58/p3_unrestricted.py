"""p3_unrestricted.py -- THE STILL-OPEN LIST'S `THE ONE SITE`, SCORED.

`code/repair_b2af/README.md` says, under WHAT IS STILL OPEN:

    `code/repair_69d1/p3_reason.py` (i-b) still anchors its control on
    `HEAD` -- `UNRESTRICTED`, the loudest form of the defect. ... it is the
    one site in the 19 that no pin can help

The ticket says the count is wrong.  This script measures the count, and
then asks the question the count does not: IS THE FILE IT NAMES IN THE
POPULATION AT ALL.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.  It is expected to exit 1:
the sentence it scores is in another ticket's document, and this script
cannot make it true.
"""

import ast
import os
import re
import shutil
import subprocess
import tempfile

import lib6e58 as L

R = L.Report(selfpop="this script's reading of `code/repair_b2af/README.md`",
             findpop="the `UNRESTRICTED` claim in mg-b2af's STILL-OPEN list")

CLAIM_FILE = "code/repair_b2af/README.md"
CLAIM_MARK = "still anchors its control on"
NAMED = "code/repair_69d1/p3_reason.py"

print("=" * 74)
print("p3 -- `THE ONE SITE`, AND WHETHER IT IS A SITE")
print("=" * 74)
print()

# ---------------------------------------------------------------------------
print("-- (i) THE CLAIM, READ FROM THE FILE RATHER THAN TYPED HERE")
print()

src = open(os.path.join(L.REPO, CLAIM_FILE)).read()
para = [p for p in src.split("\n\n") if CLAIM_MARK in p]
R.check(len(para) == 1,
        "the claim marker %r matches %d paragraphs of %s; the sentence has "
        "moved and this script is scoring the wrong text"
        % (CLAIM_MARK, len(para), CLAIM_FILE))
for p in para:
    for line in p.splitlines():
        print("      %s" % line.strip())
print()
claim = para[0] if para else ""
# THIS CHECK FIRED ON ME.  Its first form tested `"one site" in claim`
# against the raw file text, where the sentence is wrapped as "it is the one\n
# site in the 19" -- so a literal match was defeated by a LINE BREAK, in a
# ticket about a literal match defeated by a CAPITAL LETTER.  The failing run
# is kept at out_p3_unrestricted_FIRSTFORM_selferr.txt.  The whitespace is
# normalised now; the lesson is that this instrument's own claim-locator was
# an exact-string test one commit after it named exact-string tests.
flat = " ".join(claim.split())
R.check(NAMED in flat, "the claim no longer names %s" % NAMED)
R.check("one site" in flat, "the claim no longer says `one site`")
print()

# ---------------------------------------------------------------------------
print("-- (ii) THE COUNT, AT FOUR COMMITS, UNDER TWO DENOMINATORS")
print()
print("   Population: every `*.py` under `code/` in the tree of that commit.")
print("   Grain: one `ast.Call` node classified `UNRESTRICTED`.")
print()

COMMITS = [
    ("fba5f63", "mg-330a's audit, as it sits on `main`"),
    ("b94cb1e", "its PRE-REBASE twin, where mg-b2af showed the ten figures "
                "reproduce"),
    ("b1c3467", "the commit that ships mg-b2af's transcripts, i.e. the "
                "claim's own tree"),
    ("HEAD", "this branch"),
]

print("   %-9s %-8s %-8s %-8s %s" % ("commit", "POP-A", "POP-C", "69d1?",
                                     "what it is"))
per = {}
for rev, what in COMMITS:
    tmp = tempfile.mkdtemp(prefix="mg6e58_p3_")
    try:
        subprocess.run("git -C %s archive %s code | tar -x -C %s"
                       % (L.REPO, rev, tmp), shell=True, check=True)
        calls, _unp = L.all_calls(repo=tmp)
        ca = L.census(L.POP_A, calls=calls)
        cc = L.census(L.POP_C, calls=calls)
        ua = [r for r in ca["_rows"] if r["kind"] == "UNRESTRICTED"]
        uc = [r for r in cc["_rows"] if r["kind"] == "UNRESTRICTED"]
        in69 = [r for r in cc["_rows"]
                if r["file"].startswith("code/repair_69d1/")]
        per[rev] = (ua, uc, in69)
        print("   %-9s %-8d %-8d %-8d %s"
              % (rev, len(ua), len(uc), len(in69), what))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
print()
print("   The `69d1?` column is the number of `git log` call sites of ANY")
print("   spelling anywhere under `code/repair_69d1/`.")
print()

# ---------------------------------------------------------------------------
print("-- (iii) THE REFERENT.  WHICH FILE IS `THE ONE SITE`?")
print()

for rev, _what in COMMITS:
    ua, uc, in69 = per[rev]
    print("   %-9s POP-A `UNRESTRICTED` sites: %s"
          % (rev, ", ".join(L.site_key(r) for r in sorted(ua,
                                                          key=L.site_key))))
print()
never = all(len(in69) == 0 for _ua, _uc, in69 in per.values())
print("   `%s` CONTRIBUTES ZERO SITES" % NAMED)
print("   at every commit measured -- under the NARROW denominator and under")
print("   the CORRECTED one alike.  There is no `git log` call anywhere in")
print("   `code/repair_69d1/`; its control anchors on HEAD through")
print("   `git grep`, `git show` and `rev-parse`, none of which this census")
print("   can see.")
print()
print("   SO THE SENTENCE IS NOT MERELY OFF BY A COUNT.  It attaches a")
print("   FILE NAME drawn from one population to a COUNT taken over")
print("   another, and the file has never been a member of the counted one.")
print("   The one `UNRESTRICTED` site under mg-330a's own classifier, at")
print("   the claim's own tree, is `code/repair_8d5e/lib8d5e.py:167`.")
print()

R.gate(not never,
       "THE STILL-OPEN LIST NAMES A FILE THAT IS IN NO CENSUS IT CITES: "
       "`%s` has 0 `git log` call sites at all four commits measured, so "
       "`the one site in the 19` names a non-member.  The single "
       "`UNRESTRICTED` site under mg-330a's classifier is "
       "code/repair_8d5e/lib8d5e.py:167." % NAMED)

# ---------------------------------------------------------------------------
print("-- (iv) THE MECHANISM.  HOW A NON-MEMBER GOT INTO THE SENTENCE")
print()

lib = open(os.path.join(L.REPO, "code/audit_330a/lib330a.py")).read()
doc = lib.split('"""')[1]
tree = ast.parse(lib)
returned = set()
for n in ast.walk(tree):
    if isinstance(n, ast.FunctionDef) and n.name == "classify_call":
        for r in ast.walk(n):
            if isinstance(r, ast.Return):
                for c in ast.walk(r):
                    if isinstance(c, ast.Constant) and isinstance(c.value,
                                                                  str):
                        returned.add(c.value)
docnames = set(re.findall(r"^\s{8}([A-Z][A-Z-]+)\s{2,}", doc, re.M))

print("   kinds NAMED in mg-330a's taxonomy docstring : %s"
      % ", ".join(sorted(docnames)))
print("   kinds RETURNED by `classify_call`           : %s"
      % ", ".join(sorted(returned)))
print()
print("   documented but NEVER RETURNED : %s"
      % ", ".join(sorted(docnames - returned)))
print("   returned but NEVER DOCUMENTED : %s"
      % ", ".join(sorted(returned - docnames)))
print()
print("   `HEAD` is a row in the taxonomy PROSE, and the prose row is where")
print("   `p3_reason.py` is named -- mg-330a wrote `the one mg-8d5e's own")
print("   commit message points at in p3_reason.py without repairing`.")
print("   `classify_call` never returns `HEAD`; it returns `UNRESTRICTED`,")
print("   which the prose never mentions.  So the STILL-OPEN sentence took")
print("   a NAME from the docstring's `HEAD` row and a COUNT from the")
print("   code's `UNRESTRICTED` row and joined them with `i.e.`.")
print()
print("   THAT IS mg-b2af's OWN F-2 -- one number over two populations --")
print("   committed inside mg-b2af's list of what it left open.")
print()

R.check("p3_reason" in doc,
        "mg-330a's docstring no longer names p3_reason.py; the mechanism "
        "traced here does not hold at this tree")
R.gate(not (docnames - returned) and not (returned - docnames),
       "mg-330a's taxonomy DOCSTRING and its `classify_call` do not name the "
       "same kinds: documented-never-returned %s, returned-never-documented "
       "%s.  A reader who takes a name from the prose and a count from the "
       "code is joining two taxonomies."
       % (sorted(docnames - returned), sorted(returned - docnames)))

# ---------------------------------------------------------------------------
print("-- (v) THE 19, ADJUDICATED BY HAND")
print()
print("   The corrected count is not a repair on its own.  `UNRESTRICTED`")
print("   is defined by what a call does NOT have -- no `-1`, no `--`, no")
print("   `--reverse` -- so it collects two very different constructs.  Each")
print("   of the %d is read here and marked:" % len(per["HEAD"][1]))
print()
print("      SET-READ   the call's output is split into a LIST and searched")
print("                 or counted.  mg-330a's own words for that shape are")
print("                 `a set, not an anchor; it has no single revision to")
print("                 re-point`.")
print("      ANCHOR     a single revision is taken out and used.")
print()

SETREAD = "SET-READ"
ANCHOR = "ANCHOR"
VERDICTS = {
    "code/audit_c067/c1_rebase.py:47": SETREAD,
    "code/audit_c067/c1_rebase.py:48": SETREAD,
    "code/branching_bound_audit_aaf4/a5_donotdisturb.py:111": SETREAD,
    "code/branching_bound_audit_aaf4/a5_donotdisturb.py:113": SETREAD,
    "code/branching_bound_audit_aaf4/a5_donotdisturb.py:116": SETREAD,
    "code/branching_bound_audit_aaf4/a5_donotdisturb.py:158": SETREAD,
    "code/branching_bound_audit_aaf4/a5_donotdisturb.py:180": SETREAD,
    "code/branching_bound_d075/s6_class.py:75": SETREAD,
    "code/face_geometry_audit_6653/verify_claims.py:107": SETREAD,
    "code/face_geometry_audit_6653/verify_claims.py:128": SETREAD,
    "code/face_geometry_audit_e720/verify_landing_claims.py:459": SETREAD,
    "code/face_geometry_audit_e720/verify_landing_claims.py:461": SETREAD,
    "code/hodge_leverage_audit_97fb/audit_97fb.py:1508": SETREAD,
    "code/repair_8d5e/lib8d5e.py:167": SETREAD,
    "code/repair_b2af/lib_b2af.py:274": SETREAD,
    "code/species_bound_audit_6ef4/t3_census.py:225": SETREAD,
    "code/species_bound_repair_5040/kern5040.py:273": SETREAD,
    "code/species_extent_audit_6cb9/a2_crosssection.py:242": SETREAD,
    "code/state_visibility_audit_65eb/anchor65eb.py:116": SETREAD,
}

uc_head = sorted(per["HEAD"][1], key=L.site_key)
unadjudicated = []
for r in uc_head:
    k = L.site_key(r)
    v = VERDICTS.get(k)
    if v is None:
        unadjudicated.append(k)
    print("   %-9s %-56s %s" % (v or "*** NEW", k, r["src"][:60]))
print()
n_anchor = len([r for r in uc_head if VERDICTS.get(L.site_key(r)) == ANCHOR])
print("   SET-READ : %d" % len([r for r in uc_head
                                if VERDICTS.get(L.site_key(r)) == SETREAD]))
print("   ANCHOR   : %d" % n_anchor)
print("   NEW SINCE THIS ADJUDICATION WAS WRITTEN : %d" % len(unadjudicated))
for k in unadjudicated:
    print("      %s" % k)
print()
print("   NOT ONE OF THE %d TAKES A SINGLE REVISION." % len(uc_head))
print("   Every one reads a list and searches it.  So `the loudest form of")
print("   the defect` is not what this class contains: by mg-330a's own")
print("   RANGE reasoning these have no single revision to re-point.  The")
print("   count went from 1 to %d and the number of unrestricted single"
      % len(uc_head))
print("   anchors went from 0 to 0.")
print()
print("   I am naming that rather than reporting `19 sites of the defect`,")
print("   which would be the same error in the other direction -- a term")
print("   denoting more than it covers is mg-2c77's A-2, and this arc has")
print("   made it once already.")
print()

R.check(not unadjudicated,
        "%d UNRESTRICTED site(s) appeared after this hand adjudication was "
        "written and are counted but unread: %s"
        % (len(unadjudicated), unadjudicated))

# ---------------------------------------------------------------------------
print("-- (vi) THE CORRECTED SENTENCE, AND HOW ITS NUMBER WAS DERIVED")
print()
ua_h, uc_h, _ = per["HEAD"]
print("   `UNRESTRICTED` at this tree:")
print("      %2d  under mg-330a's `_HASH_FORMATS` (3 literals, exact match)"
      % len(ua_h))
print("      %2d  under the spellings git documents (p1, p2 POP-C)"
      % len(uc_h))
print("      %2d  of those %d take a single revision as an anchor"
      % (n_anchor, len(uc_h)))
print("       0  of them are in `code/repair_69d1/`, which has no `git log`")
print("          call of any spelling")
print()
print("   DERIVATION: one `ast` walk of every `*.py` under `code/`, the")
print("   kind rules of mg-330a's taxonomy applied unchanged, and the")
print("   format test replaced by a parse of the format string against the")
print("   two placeholders `man git-log` documents as commit hashes.  Both")
print("   halves measured at THIS tree; the published `1` was measured at")
print("   another.  See `out_p2_population.txt` for the same walk under all")
print("   four denominators.")
print()

# ---------------------------------------------------------------------------
print("-- SCORING PREDICTIONS.md")
print()
L.score(R, "P3-a", 2, len(ua_h),
        note="UNRESTRICTED is already 2 under mg-330a's own classifier")
L.score(R, "P3-b", lambda n: n >= 4, len(uc_h), note=">= 4 under POP-C")
L.score(R, "P3-c", True, False,
        note="predicted the extra sites were a STALENESS -- a directory "
             "that did not exist when the sentence was written.  MISS, and "
             "the truth is worse: the named file has NEVER been in the "
             "population, at any of the four commits measured")
print()

raise SystemExit(R.emit())
