"""mg-223d / R2 -- WHY `9f1ecaa` IS OFF THE HISTORY, AND WHETHER IT IS A CLASS.

The ticket's first instruction: *establish why.  Was it rebased away, was it on
a branch that was deleted, is it a refinery pre-merge commit?  The answer
determines whether this is a one-off or a class.*

It is a class, the class has a name, and the name is not new to this arc.  What
is new is the count and the exposure.
"""
import sys

import lib223d as L

led = L.Ledger("mg-223d / R2 -- THE CAUSE, AND ITS SIZE")

ps = L.pins()
res = L.commits(ps.keys())
off = sorted(s for s, f in res.items() if not L.is_ancestor(f, "HEAD"))
offfull = sorted(set(res[s] for s in off))

# ---------------------------------------------------------------------------
led.head("R2a  THE THREE HYPOTHESES THE TICKET NAMES, DECIDED")
# ---------------------------------------------------------------------------
print("""
  (i)   REBASED AWAY.
  (ii)  ON A BRANCH THAT WAS DELETED.
  (iii) A REFINERY PRE-MERGE COMMIT.

  (ii) IS REFUTED BY MEASUREMENT: every one of the off-history commits is
  still held by a live `origin/polecat-*` ref (R1f).  Nothing was deleted.

  (i) AND (iii) ARE THE SAME HYPOTHESIS under two descriptions, and the test
  that decides it is the PATCH-ID TWIN: if the commit was replayed onto main
  by a rebase, a commit with the same patch-id is on main and the original is
  not.  If it were merely an abandoned branch, there would be no twin.""")

table = L.main_patch_ids(400)
twins = {}
for full in offfull:
    twins[full] = L.twin_of(full, table)
have = [f for f in offfull if twins[f]]
print()
print("      %-13s %-13s %s" % ("OFF-HISTORY", "TWIN ON MAIN", "SUBJECT"))
for f in offfull:
    t = twins[f]
    subj = L.git("log", "-1", "--format=%s", f).strip()
    print("      %-13s %-13s %s" % (f[:12], (t[:12] if t else "*** NONE ***"),
                                    subj[:52]))
print()
led.record(None, "off-history pinned commits with a patch-id twin on main: "
           "%d of %d" % (len(have), len(offfull)))
led.record(len(have) != len(offfull),
           "THE CAUSE IS UNIFORM: every one of them is a PRE-REBASE COMMIT "
           "REPLAYED ONTO MAIN BY THE REFINERY")

# ---------------------------------------------------------------------------
led.head("R2b  SO IT IS A CLASS, AND `9f1ecaa` IS 1 OF %d" % len(offfull))
# ---------------------------------------------------------------------------
print("""
  THE MECHANISM, in one sentence: a polecat commits on its own branch, its
  own instrument records the sha it can see, the refinery REBASES the branch
  onto main, and the sha that lands is a different one.  The sha in the
  transcript was true when it was written and was never true of main.

  THE ARC ALREADY KNEW THIS AND I DID NOT DISCOVER IT.  Four prior findings,
  named so this tree is not credited with them:""")
prior = [
    ("code/idiom_sweep_audit_18dc", "names the pairs 9f1ecaa<->6fda370 and "
     "d33970b<->eacc5e1 and prints `patch-id SAME  tree DIFF`"),
    ("code/transcript_census_1abe", "t4_rebase.py carries a table of "
     "(ticket, pre, post) triples -- the same class, tabulated"),
    ("code/publication_anchor_132a", "anchor_132a.py:540 binds "
     "PRE_REBASE, POST_REBASE as a pair, by name"),
    ("code/state_claims_repair_0120", "diagnosed its integrity anchor as "
     "`displaced-by-rebase` and re-pointed it at its patch-id twin"),
]
for d, what in prior:
    print("      %-34s %s" % (d.replace("code/", ""), what))
print("""
  WHAT IS NEW HERE IS THE POPULATION.  Each of those found ITS OWN instance
  and repaired ITS OWN instance.  None of them asked how many there are, and
  the answer -- %d commits across %d directories, held by %d prunable
  branches and by nothing else -- is not derivable from any one of them.""" % (
      len(offfull),
      len(set(p.split("/")[1] for s in off for p, _i, _t in ps[s]
              if p.startswith("code/"))),
      len(set(h for s in off for h in L.holders(res[s])))))

# ---------------------------------------------------------------------------
led.head("R2c  THE TWIN IS AN EXPLANATION, NOT A SUBSTITUTE (E4, E8)")
# ---------------------------------------------------------------------------
print("""
  THE OBVIOUS REPAIR IS TO RE-POINT EVERY PIN AT ITS TWIN, and it is wrong
  twice over.

  WRONG ONCE, BY MEASUREMENT: the twin's TREE is not the original's tree.  A
  rebase replays a patch onto a later base, so the commit that lands carries
  every file the intervening commits added.  `r3` measures what that does to
  the one figure that depends on it.  18dc measured the same thing for its own
  rule and got 108 -> 111 runners.

  WRONG TWICE, BY WHAT THE PINS ARE FOR: for several of these directories the
  PRE-REBASE COMMIT IS THE SUBJECT.  Re-pointing does not degrade the finding,
  it deletes it.  Named, with the line that makes it so:""")
subject_sites = [
    ("idiom_sweep_audit_18dc", "v1_population.py:25",
     "labels 9f1ecaa `(pre-rebase)` in a table whose whole content is the "
     "pre/post difference"),
    ("transcript_census_1abe", "t4_rebase.py:41-43",
     "a (ticket, pre, post) table; the `pre` column IS the measurement"),
    ("publication_anchor_132a", "anchor_132a.py:540",
     "`PRE_REBASE, POST_REBASE = ...` -- the pair is the anchor's diagnosis"),
    ("audit_c067", "c1_rebase.py:143",
     "`the rev the transcript was committed at (pre-rebase)`"),
    ("chain_audit_39bf", "a3_timeline.py:107-109",
     "a timeline of `(pre-rebase)` events; substituting flattens it"),
    ("repair_b2af", "lib_b2af.py:96-97",
     "`INSTR_PRE` / `DOCS_PRE` -- the names say what they are"),
]
print()
for d, site, why in subject_sites:
    print("      %-26s %s" % (d, site))
    print("      %-26s     %s" % ("", why))
led.record(None, "directories where the PRE-REBASE commit is the subject and "
           "substitution would destroy the finding: %d" % len(subject_sites))

# ---------------------------------------------------------------------------
led.head("R2d  IS ANY OF IT DEAD YET?  -- THE DEADLINE, NOT THE CASUALTY")
# ---------------------------------------------------------------------------
alive = [f for f in offfull if L.resolve(f)]
led.record(None, "off-history pinned commits that still resolve: %d of %d"
           % (len(alive), len(offfull)))
led.record(len(alive) == len(offfull),
           "none of them is dead YET -- this is a deadline, not a casualty")
print("""
      NOTHING HAS DIED.  That is the whole shape of this ticket: it is a
      DEADLINE and not a casualty, and the reason it was ranked on
      irreversibility rather than size.  The arc has already been burned once
      by the softer version of this -- `audit_c067/out_c1_rebase.txt` asserts
      `5 commits were REPLAYED` and its own producer now reports 0, not
      because anything died but because a hard-coded WINDOW slid off a growing
      ref.  That was recoverable.  A collected object is not.""")

sys.exit(led.done())
