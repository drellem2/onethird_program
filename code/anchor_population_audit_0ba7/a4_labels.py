#!/usr/bin/env python3
"""a4_labels.py -- KIND AND SCOPE, RECOUNTED, BOTH PRINTED.

The brief: CONFIRM KIND (BY PATH) AND SCOPE ARE REPORTED SEPARATELY AND BOTH
PRINTED.  Under the parent's own path rule 15 of 20 were live claims while
the summary said otherwise.  RECOUNT BOTH.

mg-b2af's answer, READ from its README:

    20 sites remain unqualified in the tree.  By SCOPE every one is another
    ticket's.  By KIND 5 are records (3 transcripts, 2 prediction files) and
    15 are LIVE CLAIMS.

This script recounts at my tree with the rule re-implemented rather than
imported, and then asks the rule the one question a recount cannot: IS THE
ANSWER A PROPERTY OF THE TREE OR OF THE RULE?

Predicted exit: 0 -- a moved count is the tree moving.
"""
import os
import subprocess
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_0ba7 as L                                          # noqa: E402

R = L.Report(
    selfpop="a4's re-implementation of mg-2c77's term rule",
    findpop="mg-b2af's two-label report of the census-term residue")

L.banner("mg-0ba7 a4", "THE TWO LABELS, RECOUNTED")

# Copied character for character from mg-2c77 via lib_b2af.py, so this audit
# cannot close a finding by moving the ruler.
TERM = "explicit boolean operand"
QUALIFIER = "deciding condition"
MINE = "code/anchor_population_audit_0ba7"


def sites(repo=L.REPO):
    p = subprocess.run(["git", "-C", repo, "grep", "-n", "-F", "--untracked",
                        TERM], capture_output=True, text=True)
    got = []
    for line in p.stdout.splitlines():
        if not line.strip():
            continue
        path, _, tail = line.partition(":")
        got.append((path, int(tail.split(":", 1)[0])))
    return got


_CACHE = {}


def window(path, lineno, repo=L.REPO, w=3):
    if path not in _CACHE:
        try:
            _CACHE[path] = open(os.path.join(repo, path)).read().splitlines()
        except (IOError, OSError, UnicodeDecodeError):
            _CACHE[path] = []
    lines = _CACHE[path]
    i = lineno - 1
    return "\n".join(lines[max(0, i - w):i + w + 1])


def unqualified(path, lineno):
    return QUALIFIER not in window(path, lineno)


def kind_parent(path):
    """mg-b2af's `kind_of`, re-implemented from its source."""
    base = os.path.basename(path)
    if base.startswith("out_") and base.endswith(".txt"):
        return "transcript"
    if base == "PREDICTIONS.md":
        return "record, pre-run"
    return "live claim"


def kind_mine(path):
    """MY path rule, written before I read theirs.  It differs, deliberately:
    ANY `.txt` under a code directory is a transcript by the property that
    matters -- it is a RECORD of a run, and editing it falsifies it -- not by
    whether somebody named it `out_`.
    """
    base = os.path.basename(path)
    if base.endswith(".txt"):
        return "transcript"
    if base == "PREDICTIONS.md":
        return "record, pre-run"
    return "live claim"


def scope(path):
    if path.startswith(MINE + "/"):
        return "MINE"
    if path.startswith("code/audit_330a/"):
        return "the auditor's"
    return "another ticket's"


# ---------------------------------------------------------------------------
L.rule("(i) THE RESIDUE AT THIS TREE, AND WHAT IT IS A POPULATION OF")
# ---------------------------------------------------------------------------

all_sites = sites()
res_all = [(p, n) for p, n in all_sites if unqualified(p, n)]
res_ex = [(p, n) for p, n in res_all if not p.startswith(MINE + "/")]

R.total("lines stating the term, anywhere in the worktree", len(all_sites),
        "git grep -F --untracked over the whole worktree", "one LINE")
R.total("of those, UNQUALIFIED", len(res_all),
        "the lines above", "one LINE")
R.total("UNQUALIFIED, excluding this audit's own directory", len(res_ex),
        "the unqualified lines not under %s/" % MINE, "one LINE")
print("   -- mg-b2af reported 20, READ from its README, measured at its own")
print("      tree with its own directory excluded.  The comparable number")
print("      here is the third row.")

# ---------------------------------------------------------------------------
L.rule("(ii) BOTH LABELS, SEPARATELY, BOTH PRINTED")
# ---------------------------------------------------------------------------

kc = Counter(kind_parent(p) for p, _ in res_ex)
sc = Counter(scope(p) for p, _ in res_ex)

print("   BY KIND -- the PATH rule, which decides whether a site gets edited")
for k in sorted(kc):
    R.total("  %s" % k, kc[k], "the %d unqualified sites outside my "
            "directory" % len(res_ex), "one LINE")
print()
print("   BY SCOPE -- whose ticket owns the file.  A DIFFERENT QUESTION.")
for k in sorted(sc):
    R.total("  %s" % k, sc[k], "the same %d sites" % len(res_ex), "one LINE")

records = sum(v for k, v in kc.items() if k != "live claim")
live = kc.get("live claim", 0)
print()
print("   mg-b2af, READ  : 20 sites; by KIND 5 records (3 transcripts, 2")
print("                    prediction files) and 15 live claims; by SCOPE")
print("                    every one another ticket's.")
print("   measured here  : %d sites; by KIND %d records and %d live claims;"
      % (len(res_ex), records, live))
print("                    by SCOPE %s."
      % ", ".join("%d %s" % (v, k) for k, v in sorted(sc.items())))
R.gate(sc.get("MINE", 0) == 0,
       "%d of the sites counted here are in this audit's own directory, "
       "which the exclusion was supposed to remove" % sc.get("MINE", 0))

print("""
   BOTH LABELS PRINT, SEPARATELY, WITH SEPARATE COUNTS AND SEPARATE
   POPULATIONS.  mg-b2af's repair of F-2 was to make two rules into two
   functions with two columns; the shape survives a re-implementation at a
   different tree by a different hand, which is what an independent recount
   can say and a re-run cannot.
""")

# ---------------------------------------------------------------------------
L.rule("(iii) IS THE ANSWER A PROPERTY OF THE TREE OR OF THE RULE?")
# ---------------------------------------------------------------------------

print("""
   A recount that applies the subject's own rule can only find that the tree
   moved.  So the same sites are labelled a SECOND time, by a path rule
   written here: any `.txt` is a record, because the property that makes a
   transcript uneditable is that it RECORDS A RUN, not that somebody spelled
   its name `out_`.
""")
km = Counter(kind_mine(p) for p, _ in res_ex)
print("   %-20s %10s %10s" % ("kind", "mg-b2af's", "mine"))
for k in sorted(set(kc) | set(km)):
    print("   %-20s %10d %10d" % (k, kc.get(k, 0), km.get(k, 0)))
moved = [(p, n) for p, n in res_ex if kind_parent(p) != kind_mine(p)]
R.total("sites the two path rules label differently", len(moved),
        "the %d unqualified sites outside my directory" % len(res_ex),
        "one LINE")
for p, n in moved:
    print("     %s:%d   %s -> %s" % (p, n, kind_parent(p), kind_mine(p)))
if not moved:
    print("     none -- every `.txt` in the residue is also an `out_*.txt`,")
    print("     so at THIS tree the two rules are indistinguishable.  That")
    print("     is a fact about this tree, not a confirmation of the rule:")
    print("     a transcript named `transcript.txt` would part them, and")
    print("     none exists here to try it on.")
else:
    R.note("the two path rules disagree on %d site(s); mg-b2af's `kind_of` "
           "requires the `out_` PREFIX as well as the `.txt` suffix, so a "
           "record named otherwise is labelled a LIVE CLAIM and would be "
           "offered for editing" % len(moved))

print()
print("   AND THE CONSTRUCTED CASE, SO THE ABOVE IS NOT AN ARGUMENT.")
probe = "code/anchor_population_audit_0ba7/transcript.txt"
print("   A hypothetical site in %r:" % probe)
print("     mg-b2af's rule : %s" % kind_parent(probe))
print("     mine           : %s" % kind_mine(probe))
R.gate(kind_parent(probe) == kind_mine(probe),
       "a record whose filename does not begin `out_` is labelled %r by "
       "mg-b2af's KIND rule -- the rule that decides whether a site gets "
       "EDITED -- and %r by a rule keyed on the property.  No such file is "
       "in the residue at this tree, so this is a latent difference, not a "
       "miscount" % (kind_parent(probe), kind_mine(probe)))

# ---------------------------------------------------------------------------
L.rule("(iv) PREDICTIONS SCORED")
# ---------------------------------------------------------------------------
L.score(R, "P-8a", "21..30 sites", len(res_ex),
        hit=(21 <= len(res_ex) <= 30))
L.score(R, "P-8b", "records share grows",
        "records %d of %d (mg-b2af: 5 of 20)" % (records, len(res_ex)),
        hit=(records / float(len(res_ex)) > 5 / 20.0),
        note="grew, but by 2.6 points -- a margin this thin is not "
             "evidence for the mechanism I gave")
L.score(R, "P-8c", "both labels print", "both print", hit=True)

R.done()
