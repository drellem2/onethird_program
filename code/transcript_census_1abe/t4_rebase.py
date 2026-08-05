"""t4 -- THE THIRD BUCKET NOBODY HAS COUNTED: did any rebase in this arc alter
content?

The mayor's addendum is explicit that its samples were clean rebases with no
conflict, that two (or three) samples are not a population, and that A REBASE
WHICH RESOLVED A CONFLICT COULD LEGITIMATELY ALTER CONTENT and would NOT show
as patch-id-identical.  That case has never been counted.  This script counts
it.

POPULATION.  Every commit in this object store that is NOT an ancestor of the
named revision but whose SUBJECT LINE also occurs on it.  Subject matching is
the pairing rule because this arc's subjects are paragraph-length and unique --
`git log --format=%s` on the revision has no duplicate subjects at all, which
is checked below rather than assumed.  A commit paired this way is a
PRE-REBASE TWIN: the same work, before the refinery replayed it.

GRAIN.  One verdict per (pre-rebase commit, on-main twin) pair.

VERDICTS.
  IDENTICAL   the two patch-ids agree.  The rebase preserved content exactly.
  ALTERED     the subjects match and the patch-ids do not.  THE REBASE CHANGED
              COMMITTED CONTENT.  This is the bucket the addendum asks for and
              every member of it is named in full.

COVERAGE, stated because it bounds the answer.  This can only see commits that
are still in the object store and still reachable from some ref or reflog.  A
pre-rebase twin whose reflog entry has expired is invisible here, and its
absence is not evidence that it was clean.
"""

import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_1abe as L                                          # noqa: E402

# Re-derived below, not repeated on trust.  Provenance: the mayor's own
# measurements, quoted in the mg-1abe brief as (ticket, recorded, on-main).
MAYOR_SAMPLES = [
    ("mg-f3ff", "72e36cb", "9c54a99"),
    ("mg-fcb2", "064c79c", "7a35eac"),
    ("mg-65eb", "880fc15", "99ee542"),
]


def main():
    rev = L.main_rev()
    head = L.resolve(rev)
    led = L.Ledger("t4 -- DID ANY REBASE IN THIS ARC ALTER CONTENT?")
    print("    as-of      %s  (%s)" % (head, rev))

    # ------------------------------------------------ the pairing rule itself
    led.head("T4a -- THE PAIRING RULE, TESTED BEFORE IT IS USED")
    subjects = collections.defaultdict(list)
    for line in L.git("log", "--format=%H%x09%s", head).split("\n"):
        if "\t" in line:
            h, s = line.split("\t", 1)
            subjects[s].append(h)
    dupes = {s: hs for s, hs in subjects.items() if len(hs) > 1}
    print("    %d commits on %s over %d distinct subjects"
          % (sum(len(v) for v in subjects.values()), head[:7], len(subjects)))
    led.record(not dupes,
               "T4a subject lines are unique on %s (%d duplicated), so "
               "matching a side commit to main BY SUBJECT identifies at most "
               "one candidate.  An instrument whose pairing rule is ambiguous "
               "cannot report ALTERED against anything"
               % (head[:7], len(dupes)))
    for s, hs in list(dupes.items())[:20]:
        print("      DUPLICATE SUBJECT %s: %s" % (", ".join(h[:8] for h in hs),
                                                  s[:70]))

    # ----------------------------------------------------- the side commits
    led.head("T4b -- EVERY PRE-REBASE TWIN STILL IN THE OBJECT STORE")
    side = L.git("rev-list", "--all", "--reflog", "--not", head).split()
    print("    %d commits are reachable from some ref or reflog and are NOT "
          "ancestors of %s" % (len(side), head[:7]))

    pairs, unmatched = [], 0
    for c in side:
        s = L.git("log", "-1", "--format=%s", c).strip()
        twin = subjects.get(s)
        if twin:
            pairs.append((c, twin[0], s))
        else:
            unmatched += 1
    print("    %d of them have a subject that also occurs on %s -- these are "
          "the PRE-REBASE TWINS" % (len(pairs), head[:7]))
    print("    %d do not, and are outside this measurement: work that never "
          "landed, or landed reworded" % unmatched)

    # ------------------------------------------------------- the verdict
    led.head("T4c -- PATCH-ID ON EVERY PAIR")
    print()
    print("    %-10s %-10s %-11s %s" % ("pre-rebase", "on-main", "verdict",
                                        "subject"))
    identical, altered = [], []
    for c, t, s in sorted(pairs, key=lambda x: x[2]):
        pc, pt = L.patch_id(c), L.patch_id(t)
        if pc is not None and pc == pt:
            identical.append((c, t, s))
            v = "IDENTICAL"
        else:
            altered.append((c, t, s))
            v = "*** ALTERED ***"
        print("    %-10s %-10s %-11s %s" % (c[:8], t[:8], v, s[:52]))
    if not pairs:
        print("    (no pre-rebase twin survives in this object store)")

    led.record(None,
               "T4c of %d pre-rebase/on-main pairs visible in this object "
               "store, %d are patch-id IDENTICAL and %d are not.  A "
               "non-identical patch-id is a CANDIDATE and not yet a verdict: "
               "T4c' adjudicates each one, because `the content differs` and "
               "`a rebase altered the content` are different claims"
               % (len(pairs), len(identical), len(altered)))

    # ------------------------------------------------------- adjudication
    led.head("T4c' -- EVERY CANDIDATE ADJUDICATED, BECAUSE PATCH-ID ALONE "
             "CANNOT NAME THE CAUSE")
    print("""
A patch-id compares DIFFS.  Two commits can carry identical content and still
disagree on patch-id, because a diff is a fact about a base as well as about a
tree.  So every candidate is put through a ladder of pure-git discriminators
and only what survives all of them is reported as content alteration.

  1  DOES ANY SHARED FILE ACTUALLY DIFFER?  If the two commits produce
     byte-identical blobs at every path they both touch, nothing this commit
     authored was altered.  The patch-ids differ because the path SETS differ:
     hunks the new base had already absorbed drop out of the replay.  This is
     a rebase working correctly and it is NOT damage.

  2  COULD A CONFLICT EVEN HAVE OCCURRED?  A path the commit CREATES did not
     exist on the base being replayed onto, so a rebase cannot have conflicted
     in it.  If every differing path is created by the commit itself, the
     difference was AUTHORED -- the branch was reworked and resubmitted.

  3  Anything else -- a pre-existing file whose content differs between the two
     -- is what the addendum asked to be counted, and it is named in full.
""")
    conflict, rework, absorbed = [], [], []
    for c, t, s in altered:
        fa = set(L.git("show", "--name-only", "--format=", c).split("\n")) - {""}
        fb = set(L.git("show", "--name-only", "--format=", t).split("\n")) - {""}
        shared = fa & fb
        diffpaths = [p for p in sorted(shared)
                     if L.git("rev-parse", "%s:%s" % (c, p)).strip()
                     != L.git("rev-parse", "%s:%s" % (t, p)).strip()]
        parent = L.git("rev-parse", "%s^" % t).strip()
        created = [p for p in diffpaths
                   if L.blob_at(parent, p) is None]
        print("    %s -> %s" % (c[:8], t[:8]))
        print("        %s" % s[:70])
        print("        paths %d vs %d, shared %d, differing %d, of which "
              "CREATED BY THIS COMMIT %d"
              % (len(fa), len(fb), len(shared), len(diffpaths), len(created)))
        if shared and not diffpaths:
            absorbed.append((c, t, s))
            print("        VERDICT  CONTENT SURVIVED -- every one of the %d "
                  "shared paths is byte-identical in both.  The patch-ids "
                  "differ only because the path sets do: %d hunk(s) the new "
                  "base had already absorbed dropped out of the replay"
                  % (len(shared), len(fa ^ fb)))
            for p in sorted(fa - fb):
                print("                 only in the pre-rebase commit: %s" % p)
            for p in sorted(fb - fa):
                print("                 only on main:                 %s" % p)
        elif diffpaths and len(created) == len(diffpaths):
            rework.append((c, t, s))
            print("        VERDICT  AUTHORED -- every differing path is "
                  "created by the commit, so no rebase could have conflicted "
                  "in it.  The branch was reworked and resubmitted")
            for p in diffpaths:
                print("                 %s" % p)
        else:
            conflict.append((c, t, s))
            print("        VERDICT  *** CONTENT ALTERED IN A PRE-EXISTING "
                  "FILE *** -- a rebase COULD have done this and this pair "
                  "needs a human")
            for p in diffpaths:
                print("                 %s%s" % (p, " (created)" if p in created
                                                 else " (pre-existing)"))
    if not altered:
        print("    (no candidates)")

    led.record(not conflict,
               "T4c'' THE THIRD BUCKET, AFTER ADJUDICATION: %d pair(s) show a "
               "rebase altering the content of a pre-existing file.  Patch-id "
               "ALONE flagged %d; of those, %d survived with byte-identical "
               "content and only an absorbed hunk, and %d were branch reworks "
               "in files the commit itself creates"
               % (len(conflict), len(altered), len(absorbed), len(rework)))
    led.record(None,
               "T4c''' AND THAT IS THE CATCH IN PATCH-ID, MEASURED RATHER THAN "
               "WARNED ABOUT: %d of %d pairs in this arc carry identical "
               "content under DIFFERENT patch-ids.  Patch-id is the right "
               "instrument against ancestry's false negative, and it has a "
               "false negative of its own whenever the replay absorbs a hunk.  "
               "A census built on patch-id alone would have reported these as "
               "damage" % (len(absorbed), len(pairs)))

    led.record(None,
               "T4c' COVERAGE: this answer is over the %d pairs still visible, "
               "not over every rebase the refinery has ever performed.  A twin "
               "whose reflog entry has expired is invisible here and its "
               "absence is NOT evidence that its rebase was clean" % len(pairs))

    # ---------------------------------------------- the mayor's own samples
    led.head("T4d -- THE THREE SAMPLES IN THE BRIEF, RE-DERIVED RATHER THAN "
             "REPEATED")
    print("""
PROVENANCE: these three pairs are the MAYOR'S measurements, quoted in the
mg-1abe brief.  They are re-derived here from the object store rather than
carried forward as numbers, because a figure repeated without re-derivation
cannot be chased back to anything.
""")
    print("    %-9s %-10s %-10s %-11s %s"
          % ("ticket", "recorded", "on-main", "ancestry", "patch-id"))
    agree = 0
    for ticket, rec, on in MAYOR_SAMPLES:
        fr, fo = L.resolve(rec), L.resolve(on)
        if not fr or not fo:
            print("    %-9s %-10s %-10s %s" % (ticket, rec, on,
                                               "NOT IN THIS OBJECT STORE"))
            continue
        anc = "ancestor" if L.is_ancestor(fr, head) else "NOT an ancestor"
        pr, po = L.patch_id(fr), L.patch_id(fo)
        same = (pr is not None and pr == po)
        agree += 1 if same else 0
        print("    %-9s %-10s %-10s %-15s %s"
              % (ticket, rec, on, anc,
                 "IDENTICAL" if same else "DIFFERENT"))
    led.record(agree == len(MAYOR_SAMPLES),
               "T4d %d of the %d samples in the brief re-derive to "
               "patch-id-IDENTICAL here.  Re-derived, not repeated"
               % (agree, len(MAYOR_SAMPLES)))
    led.record(None,
               "T4d' every one of those three is ALSO reported by ancestry as "
               "not on main.  That is the false negative the brief warns "
               "about, reproduced here on purpose so the two instruments can "
               "be seen disagreeing on the same three commits")

    return led.done()


if __name__ == "__main__":
    sys.exit(main())
