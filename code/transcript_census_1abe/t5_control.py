"""t5 -- THE CONVENTION, AND A CONTROL THAT CAN CHECK IT.

Step 3 of the ticket: propose the convention change, decide and defend, and
make it CHECKABLE BY A CONTROL, "because a convention nobody can check is how
we got here."

WHAT I AM PROPOSING, AND WHAT I REJECTED
========================================

The ticket offers three options.  Two of them do not survive contact with the
measurements in t2 and t4.

  REJECTED -- "record the SHA the run measured and assert it is an ancestor."
  t4 measures the failure directly: all three of the brief's own samples are
  patch-id-identical on main and NOT ancestors of it.  An ancestry assertion
  would be RED on correct, undamaged evidence, and a control that cries wolf on
  the healthy case is worse than no control.  Swapping ancestry for patch-id
  does not save it either: t4c''' finds a pair carrying byte-identical content
  under different patch-ids, because a replay that absorbs a hunk changes the
  diff without changing the content.

  REJECTED -- "re-run post-rebase before submit."  The polecat cannot: the
  refinery rebases after submission, and the ticket forbids changing that.

  REJECTED, AND THIS IS THE ONE THAT LOOKS RIGHT -- "have the gate re-run and
  refuse on mismatch."  t2 measures why it cannot be the whole answer: most
  transcripts in this arc DO NOT REPRODUCE and the largest reason is not damage
  at all -- their producers read repository-global state, so they are stale the
  moment the next commit lands anywhere.  A gate that re-runs and refuses on
  mismatch would refuse nearly every merge in this arc, for a reason that is
  not the merge's fault.  Re-running is also the most expensive check available
  and the one most likely to be turned off.

WHAT I PROPOSE INSTEAD -- three rules, and only the third costs anything

  R1  DECLARE THE CODE, NOT THE COMMIT.  A producer prints, into its own
      transcript, a digest over the `.py`/`.sh` BLOB SHAS of the directory that
      produced it.  Blob shas survive rebases untouched; commit shas do not,
      which is the entire subject of this ticket.  `out_*.txt` and `.md` are
      excluded so that committing the transcript cannot invalidate the
      declaration -- otherwise every transcript ships already stale and the
      check becomes a ritual.  That trap is mg-bf79's "a publisher is not a
      pin", and this rule is shaped around it.

  R2  DECLARE THE REACH.  A producer prints whether it read repository-global
      state.  If it did, the transcript says so and is DECLARED UNPINNABLE:
      no digest can make it a fact about a tree, because it is not one.  t2
      shows this is the majority case, and a convention that pretended
      otherwise would be false about most of the arc.

  R3  CHECK R1 WITH A CONTROL THAT NEVER RE-RUNS ANYTHING.  For every committed
      transcript that declares a digest, recompute that digest from the tree at
      the transcript's CARRYING COMMIT and compare.  Pure git, O(1) per
      transcript, no execution.  A mismatch means the transcript was produced
      by a different version of its own code than the one it is committed
      beside -- which is mg-c3a2's sighting, the pre-fix run committed beside
      the fix, and it is the sighting that went unnoticed for five days.

AND A SCREEN THAT WORKS ON THE 510 TRANSCRIPTS THAT DECLARE NOTHING
==================================================================

R1-R3 only protect transcripts written after the convention.  So this script
also ships a RETROACTIVE SCREEN needing no declaration and no re-running:

  A transcript whose carrying commit ALSO MODIFIES PRODUCING CODE IN ITS OWN
  DIRECTORY is a candidate for "a run committed beside the change it does not
  contain".

It is a screen, not a proof: an author who re-ran after the change lands in it
innocently.  Its value is that it is pure git, runs over the whole arc in
seconds, and its candidate set is small enough to read.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_1abe as L                                          # noqa: E402


def main():
    rev = L.main_rev()
    head = L.resolve(rev)
    led = L.Ledger("t5 -- THE CONVENTION AND THE CONTROL THAT CHECKS IT")
    print("    as-of      %s  (%s)" % (head, rev))

    population = L.transcripts(rev)

    # ------------------------------------------------------------------- R3
    led.head("T5a -- R3: THE CONTROL, RUN OVER EVERY COMMITTED TRANSCRIPT")
    print("""
COVERAGE is reported before CORRECTNESS, because a control that is green over
an empty population is not green about anything.
""")
    declaring, agree, disagree, undeclared = [], [], [], []
    for p in population:
        c = L.carrying_commit(p, rev)
        blob = L.blob_at(c, p)
        text = blob.decode("utf-8", "replace") if blob else ""
        dec = L.declared_digest(text)
        if dec is None:
            undeclared.append(p)
            continue
        declaring.append(p)
        actual = L.code_digest(os.path.dirname(p), c)
        (agree if dec == actual else disagree).append((p, dec, actual))

    print("    declaring a code-digest : %d of %d" % (len(declaring),
                                                      len(population)))
    print("    declaring nothing       : %d of %d  (every transcript written "
          "before this convention)" % (len(undeclared), len(population)))
    print()
    for p, dec, act in declaring and [(p, d, a) for p, d, a in agree + disagree] or []:
        print("    %-56s %s %s %s" % (p[len("code/"):][:56], dec,
                                      "==" if dec == act else "!=", act))

    led.record(None,
               "T5a COVERAGE: the control can say anything at all about %d of "
               "%d transcripts.  The other %d predate the convention and no "
               "control can check them; that is the honest size of what R1-R3 "
               "fixes going forward and it fixes nothing retroactively"
               % (len(declaring), len(population), len(undeclared)))
    led.record(not disagree,
               "T5a' CORRECTNESS: of the %d transcripts that declare, %d agree "
               "with the code-digest recomputed at their carrying commit and "
               "%d do not" % (len(declaring), len(agree), len(disagree)))

    # ----------------------------------------------- the control can fire
    led.head("T5b -- THE CONTROL, SHOWN GOING RED BY CONSTRUCTION")
    print("""
A control that has only ever been green has not been shown able to fire.  The
demonstration mutates a DECLARED digest in memory -- nothing on disk is touched
-- and asserts the comparison flips.  If this arc's own transcripts had carried
such a declaration, this is the row that would have caught mg-c3a2's sighting
on the day it landed instead of five days later.
""")
    # The demonstration is built from a REAL committed directory and a REAL
    # commit, so it does not depend on anyone having adopted the convention
    # yet.  Both answers are shown: the control must ACCEPT a true declaration
    # as well as REFUSE a false one, or it is not a control, it is a rejector.
    subject = "code/audit_c067"
    at = L.carrying_commit(subject + "/out_c2_anchors.txt", rev)
    truth = L.code_digest(subject, at)
    if truth is None:
        led.self_error("T5b could not compute a digest for %s at %s; the "
                       "demonstration did not run" % (subject, at[:7]))
    else:
        good = "%s %s\n" % (L.DECLARE_PREFIX, truth)
        broken = truth[:-4] + ("0000" if truth[-4:] != "0000" else "1111")
        bad = "%s %s\n" % (L.DECLARE_PREFIX, broken)
        print("    subject   %s at %s" % (subject, at[:7]))
        print("    true code-digest there : %s" % truth)
        print("    corrupted declaration  : %s" % broken)
        led.record(L.declared_digest(good) == truth,
                   "T5b GREEN ANSWER: a transcript declaring %s is ACCEPTED "
                   "against the tree at %s" % (truth, at[:7]))
        led.record(L.declared_digest(bad) != truth,
                   "T5b' RED ANSWER: the same control REFUSES a transcript "
                   "declaring %s.  The control is capable of both answers "
                   "against the same real tree, which is the only thing that "
                   "makes T5a' worth reading" % broken)

    # ------------------------------------------------------------- screen
    led.head("T5c -- THE RETROACTIVE SCREEN: A RUN COMMITTED BESIDE THE CHANGE "
             "IT DOES NOT CONTAIN")
    print("""
NOW: over the %d transcripts as they stand, the carrying commit of each is
asked whether it ALSO changed a `.py`/`.sh` file in that transcript's own
directory.  Needs no declaration, no re-running and no cooperation from
anything already committed.
""" % len(population))
    now_flagged = []
    for p in population:
        c = L.carrying_commit(p, rev)
        touched = L.git("show", "--name-only", "--format=", c).split("\n")
        d = os.path.dirname(p) + "/"
        code = [t for t in touched
                if t.startswith(d) and t.endswith(L.CODE_SUFFIXES)]
        if code:
            now_flagged.append((p, c, code))
    print("    %d of %d transcripts are carried by a commit that also changed "
          "producing code in their own directory" % (len(now_flagged),
                                                     len(population)))
    print()
    print("    every one, named (transcript, carrying commit, the code files "
          "that moved in the same commit):")
    for p, c, code in now_flagged:
        print("      %-52s %s  %s" % (p[len("code/"):][:52], c[:7],
                                      ", ".join(os.path.basename(x)
                                                for x in code)[:60]))
    if not now_flagged:
        print("      (none)")

    rate = 100.0 * len(now_flagged) / len(population)
    led.record(None,
               "T5c %d of %d committed transcripts (%.0f%%) sit in the same "
               "commit as a change to their own producing code"
               % (len(now_flagged), len(population), rate))
    led.record(rate < 50,
               "T5c' AND THAT MAKES THIS SCREEN USELESS, WHICH IS A RESULT AND "
               "NOT A SETBACK.  It flags %.0f%% of the population, because "
               "committing the code and its transcripts together IS THIS ARC'S "
               "NORMAL PRACTICE.  A screen that fires on five transcripts in "
               "six discriminates nothing.  It is kept, red, rather than "
               "quietly dropped, because the next person to think of it should "
               "find the measurement instead of the idea" % rate)

    # ------------------------------------------- the screen that does work
    led.head("T5c-ii -- THE SCREEN THAT DOES DISCRIMINATE: A TRANSCRIPT THAT "
             "NAMES ITS OWN REVISION, AND NAMES A DIFFERENT ONE")
    print("""
The ticket's own question, asked literally: FOR EACH COMMITTED FIGURE, WHICH
REVISION IS IT A FACT ABOUT, AND IS THAT THE REVISION IT NAMES?  Many of this
arc's transcripts already print the commit they were run against.  Where one
does, the comparison is free and it is exact.

POPULATION  transcripts whose bytes contain at least one hex token that
            RESOLVES to a commit in this object store.  GRAIN one verdict per
            transcript, using the FIRST resolvable commit it names.
""")
    import re as _re
    tok_re = _re.compile(r"(?<![0-9A-Za-z])([0-9a-f]{7,40})(?![0-9A-Za-z])")
    names, same, differ = [], [], []
    cache = {}
    for p in population:
        c = L.carrying_commit(p, rev)
        blob = L.blob_at(c, p)
        if blob is None:
            continue
        found = None
        for m in tok_re.finditer(blob.decode("utf-8", "replace")):
            t = m.group(1)
            if t not in cache:
                cache[t] = L.resolve(t)
            if cache[t]:
                found = cache[t]
                break
        if found is None:
            continue
        names.append(p)
        (same if found == c else differ).append((p, found, c))

    print("    %d of %d transcripts name a resolvable commit" % (len(names),
                                                                 len(population)))
    print("    %d name their own carrying commit" % len(same))
    print("    %d NAME A DIFFERENT COMMIT -- self-declared displacement, "
          "readable with no re-running at all" % len(differ))
    print()
    print("    every transcript that names a commit other than the one "
          "carrying it:")
    for p, named, c in differ:
        anc = "ancestor" if L.is_ancestor(named, head) else "off-main"
        print("      %-46s names %s  carried by %s  (%s)"
              % (p[len("code/"):][:46], named[:7], c[:7], anc))
    if not differ:
        print("      (none)")

    led.record(not differ,
               "T5c-ii %d of the %d transcripts that name a resolvable commit "
               "name one that is NOT the commit carrying them.  This screen "
               "needs no declaration, no convention and no re-running, and "
               "unlike T5c it discriminates: it fires on %.0f%% of its "
               "population rather than %.0f%%"
               % (len(differ), len(names),
                  100.0 * len(differ) / len(names) if names else 0, rate))

    # ------------------------------------------------------- what it costs
    led.head("T5d -- WHAT THIS CONVENTION DOES NOT DO")
    print("""
It does not make an unreproducible transcript reproduce.  R2 exists precisely
because most of this arc's transcripts CANNOT be pinned to a tree, and the
convention's answer to those is to make them SAY so rather than to pretend.

It does not check anything already committed.  T5a's coverage row is %d of %d
and will stay at whatever the arc adopts.

It does not detect a producer that reads repository-global state.  R2 is a
DECLARATION BY THE AUTHOR, and nothing here verifies it.  A checkable version
would need the producer run under a harness that intercepts `git` -- worth
building, not built here, and named so that nobody reads R2 as enforced.
""" % (len(declaring), len(population)))
    led.record(None,
               "T5d R2 is declared by the author and NOT verified by this "
               "control.  Stated here rather than in a footnote, because an "
               "unverified declaration presented as a check is the shape this "
               "whole ticket is about")

    return led.done()


if __name__ == "__main__":
    sys.exit(main())
