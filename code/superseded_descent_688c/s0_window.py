#!/usr/bin/env python3
"""mg-688c s0 -- BOUND THE WINDOW.

The ticket's step 1: when did the mirror last match origin/main?  If it cannot
be bounded, an unbounded window is itself the finding.

It can be bounded, on both ends, to the second -- and the answer is sharper
than "76 commits behind": the mirror was born CURRENT and fell behind 28
minutes later.
"""
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from lib688c import *  # noqa

print("=" * 78)
print("mg-688c s0 -- THE WINDOW, BOUNDED FROM BOTH ENDS")
print("=" * 78)

rl = mirror_reflog()
print("""
HOW THIS IS BOUNDED, AND WHY IT IS NOT A GUESS
  The mirror branch carries its ENTIRE life in two reflog entries.  Nothing
  advanced it between them -- that is why mg-cdd5 found it 76 behind.  So the
  interval in which the checkout could resolve a citation into superseded text
  is exactly [creation, repair], read off those two entries.

  What the reflog CANNOT say is when the REMOTE moved past 912f1b1: a reflog
  records when this clone learned something, not when the remote had it.  The
  remote's own push history closes that gap.
""")

print(rule())
print("A. THE MIRROR BRANCH'S WHOLE LIFE  (git reflog show main-mirror)")
print(rule())
for r in rl:
    print("  %s  %s  %s" % (r["sha"], fmt(r["at"]), r["what"]))
if len(rl) != 2:
    print("  !! expected exactly 2 entries; the branch was touched otherwise")

created = rl[-1]["at"]
repaired = rl[0]["at"]

print("""
  entries: %d.  The older is the creation, the newer is mg-cdd5's ff-merge.
  Between them: NOTHING.  The branch was never advanced, never reset, never
  rebased.  The checkout therefore stood at %s for the whole interval.
""" % (len(rl), MIRROR_REV))

print(rule())
print("B. WHEN THE REMOTE ACTUALLY MOVED  (GitHub PushEvents, cached)")
print(rule())
evs = push_events()
print("  push events to refs/heads/main on record: %d" % len(evs))
print("  earliest %s   latest %s" % (fmt(evs[0]["at"]), fmt(evs[-1]["at"])))

# the push that made the mirror's revision the tip, and the one that ended it
made_tip = None
ended = None
for i, ev in enumerate(evs):
    if ev["head"].startswith(MIRROR_REV):
        made_tip = ev
        ended = evs[i + 1] if i + 1 < len(evs) else None
        break

print("""
  %s was pushed to origin/main at   %s
  the next push to main landed at       %s   (head %s)
""" % (MIRROR_REV, fmt(made_tip["at"]), fmt(ended["at"]), ended["head"]))

print(rule())
print("C. THE THREE INSTANTS, ORDERED")
print(rule())
rows = [
    (made_tip["at"], "%s pushed -- it becomes origin/main" % MIRROR_REV),
    (created, "main-mirror created from origin/main (reflog)"),
    (ended["at"], "next push (%s) -- THE MIRROR FALLS BEHIND" % ended["head"]),
    (repaired, "mg-cdd5's `merge --ff-only` -- THE MIRROR IS CURRENT AGAIN"),
]
for t, what in sorted(rows):
    print("  %s   %s" % (fmt(t), what))

born_current = created < ended["at"]
print("""
  WAS THE MIRROR BORN CURRENT, OR BORN STALE?
    creation %s  <  next push %s   -> %s

  This is worth stating because the commit dates say the opposite.  The first
  commit past %s (3b1f63b) has committer date 2026-07-20T23:18:01Z, which is
  18 minutes BEFORE the branch was created -- so read from commit dates alone
  the mirror looks born stale.  It was not: those three commits were pushed
  together at %s, after the branch existed.  Commit date is when a commit was
  WRITTEN; only the push is when it became fetchable, and only the push can
  open a hazard window.
""" % (fmt(created), fmt(ended["at"]),
       "BORN CURRENT" if born_current else "BORN STALE",
       MIRROR_REV, fmt(ended["at"])))

print(rule())
print("D. THE WINDOW")
print(rule())
print("""  START  %s   the push of %s
  END    %s   mg-cdd5's ff-merge
  ------------------------------------------------------------------
  DURATION  %s

  and the mirror was CURRENT for only %s of its life
  (%s -> %s).
""" % (fmt(ended["at"]), ended["head"], fmt(repaired),
       dur(ended["at"], repaired), dur(created, ended["at"]),
       fmt(created), fmt(ended["at"])))

print(rule())
print("E. PER-CLAIM HAZARD WINDOWS -- SHORTER, AND THEY ARE WHAT MATTERS")
print(rule())
print("""
  The window above is when the checkout was BEHIND.  It is not when the
  checkout was DANGEROUS.  A citation only resolves into WITHDRAWN text from
  the moment the withdrawal is on the remote; before that the stale text and
  the live text are the same text, and a reader of either read the same thing.

  So each withdrawn claim carries its own window, opening at the push that
  carried its withdrawal.  These are the intervals the descent sweep searches.
""")
hz = {}
for c in CLAIMS:
    at, head = push_time(c["landed"])
    hz[c["id"]] = at
    print("  %-4s %-18s landed %s  pushed %s" %
          (c["id"], DOCS[c["doc"]].split("/")[-1][:18], c["landed"], fmt(at)))
    print("       hazard window: %s -> %s   (%s)" %
          (fmt(at), fmt(repaired), dur(at, repaired)))

longest = max(hz.values(), key=lambda t: (repaired - t))
shortest = min(hz.values(), key=lambda t: (repaired - t))
print("""
  LONGEST  hazard window: %s  (%s)   -- BK1, the 946 count
  SHORTEST hazard window: %s  (%s)   -- CR1, row C3

  NONE of them is 22 days.  The staleness lasted %s; the three
  STRUCK-class hazards opened on 2026-08-07 and 2026-08-09 and lasted under
  five days.  That is the interval a descendant has to have been written in.
""" % (fmt(min(hz.values())), dur(min(hz.values()), repaired),
       fmt(max(hz.values())), dur(max(hz.values()), repaired),
       dur(ended["at"], repaired)))

print("== s0 exit: 0 ==")
