"""d3_adopt -- THE CONVENTION, ADOPTED AND MADE CHECKABLE.

mg-1abe proposed R1/R2/R3 and adopted them in exactly one directory: its own.
It said so, and it put the size of that honestly: **"Coverage over the existing
arc is 0 of 541 and will stay there until something adopts it."**

A convention no control enforces is how the arc got here, so this script is
BOTH halves: the second adopter, and the control.

  R1  DECLARE THE CODE, NOT THE COMMIT.  Every transcript prints a
      `code-digest:` over the sorted `.py`/`.sh` BLOB SHAS of the directory
      that produced it.  Blob shas survive a rebase; commit shas do not, which
      is the whole subject of the arc.  `out_*.txt` and `.md` are excluded so
      that COMMITTING THE TRANSCRIPT CANNOT INVALIDATE THE DECLARATION.

  R2  DECLARE THE REACH.  Every transcript prints `reads-outside-tree:`.  If
      yes, it is DECLARED UNPINNABLE: no digest can make it a fact about a
      tree, because it is not one.

  R3  CHECK R1 WITH A CONTROL THAT NEVER RE-RUNS ANYTHING.  Recompute the
      declared digest from the tree at the transcript's CARRYING COMMIT and
      compare.  Pure git, O(1) per transcript, no execution.

WHAT IS NEW HERE, AND IT IS THE HALF mg-1abe SAID WAS NOT BUILT:

  * R3 is run over **the whole arc**, not over one directory, and a directory
    that has not adopted is reported as `UNDECLARED` -- a FINDING with a
    number -- rather than as silence.  mg-1abe scored its own P5.2 a MISS for
    shipping a control that was "vacuously green"; a control whose only
    reachable answer is green has not been shown able to refuse.

  * **R2 IS MADE CHECKABLE.**  mg-1abe: "R2 is declared by the author and is
    not verified.  A checkable version needs the producer run under a harness
    that intercepts `git`.  That is worth building and is not built here."  A
    `git`-intercepting harness is one way; it is not the only way.  A STATIC
    read of the producing code answers the same question at the same grain the
    census already trusts for its own 103/9 cause split -- and it is checkable
    against the author's declaration, which is what R2 lacked.

  * The **first-adopter defect is kept**: my own first transcripts declared
    `code/transcript_census_1abe`'s digest, because `lib_1abe.Ledger` binds
    `SELF_DIR` in its own module and I imported it unmodified.  A TRUE digest
    of the WRONG DIRECTORY -- and R3 would have called it green, because it
    agreed.  See `lib_f8e5.Ledger`.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_f8e5 as L


def main():
    at = L.main_rev()
    rev = L.resolve(at)
    head = L.resolve("HEAD")
    led = L.Ledger("d3 -- THE CONVENTION, ADOPTED AND MADE CHECKABLE",
                   reads_outside_tree=True)
    print("    as-of: %s      (this directory is scanned at HEAD %s)"
          % (rev[:12], head[:12]))

    # ------------------------------------------------------------- D3a
    led.head("D3a -- R3 OVER THE WHOLE ARC, WITH `UNDECLARED` COUNTED")
    print("""Population: every tracked `code/<dir>/out_*.txt` at this revision --
mg-1abe's own denominator.  Grain: one verdict per transcript.  Nothing is
executed; each row is a digest recomputed from the tree at that transcript's
carrying commit and compared with what the transcript declares about itself.
""")
    pop = L.transcripts(rev)
    verdicts = {}
    disagree = []
    for p in pop:
        b = L.blob_at(rev, p)
        if b is None:
            continue
        text = b.decode("utf-8", "replace")
        dec = L.declared_digest(text)
        if dec is None:
            v = "UNDECLARED"
        else:
            carrier = L.carrying_commit(p, rev)
            actual = L.code_digest(os.path.dirname(p), carrier)
            if actual is None:
                v = "NO-CODE"
            elif actual == dec:
                v = "AGREES"
            else:
                v = "DISAGREES"
                disagree.append((p, dec, actual, carrier))
        verdicts[v] = verdicts.get(v, 0) + 1
    for k in ("AGREES", "DISAGREES", "NO-CODE", "UNDECLARED"):
        print("    %-12s %4d  of %d" % (k, verdicts.get(k, 0), len(pop)))
    for p, dec, actual, carrier in disagree:
        print("      DISAGREES  %s" % p)
        print("                 declares %s, tree at %s gives %s"
              % (dec, carrier[:7], actual))
    led.record(not disagree,
               "D3a R3 refuses %d transcript(s): a transcript that declares a "
               "digest its own carrying commit does not produce was made by a "
               "different version of its own code than the one it is committed "
               "beside" % len(disagree))
    led.record(not verdicts.get("UNDECLARED"),
               "D3a' COVERAGE IS %d OF %d (%.1f%%).  %d transcripts declare "
               "nothing and are counted as UNDECLARED rather than as passing -- "
               "a control that cannot report its own blind spot is the vacuous "
               "green mg-1abe scored as its P5.2 miss"
               % (verdicts.get("AGREES", 0) + verdicts.get("DISAGREES", 0),
                  len(pop),
                  100.0 * (verdicts.get("AGREES", 0)
                           + verdicts.get("DISAGREES", 0)) / max(len(pop), 1),
                  verdicts.get("UNDECLARED", 0)))

    # ------------------------------------------------------------- D3b
    led.head("D3b -- THE SECOND ADOPTER, CHECKED AT ITS OWN PUBLISHING STEP")
    print("""mg-1abe's first-adopter row could not see the end of its own output --
`t5` read its own directory while its own transcript was still being written,
and printed 6 of 7 where the answer was 8 of 8 (its defect 6).  The same thing
is true here and the answer is not to hide it: this row is a fact about the
transcripts ALREADY WRITTEN when it runs, and the runner's order is what makes
that a shrinking set rather than a growing one.
""")
    mine_dir = "code/" + L.SELF_DIR
    want = L.code_digest(mine_dir, head)
    print("    digest of %s at HEAD %s : %s" % (mine_dir, head[:7], want))
    here = sorted(f for f in os.listdir(os.path.dirname(os.path.abspath(__file__)))
                  if f.startswith("out_") and f.endswith(".txt"))
    agree = 0
    for f in here:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f),
                  encoding="utf-8", errors="replace") as fh:
            dec = L.declared_digest(fh.read())
        ok = dec == want
        agree += 1 if ok else 0
        print("      %-28s declares %-18s %s"
              % (f, dec, "AGREES" if ok else "DISAGREES"))
    led.record(bool(here) and agree == len(here),
               "D3b %d of %d transcripts written so far declare this "
               "directory's OWN digest at HEAD.  A transcript that declared a "
               "true digest of somebody else's directory would pass R3 and be "
               "wrong, which is the defect this suite committed first and "
               "keeps in `lib_f8e5.Ledger`" % (agree, len(here)))

    # ------------------------------------------------------------- D3c
    led.head("D3c -- THE CONTROL, SHOWN REFUSING SOMETHING")
    print("""A control that has only ever been green has not been shown able to
fire.  Three constructions against a real tree, all three FORCED:
""")
    carrier = L.carrying_commit(mine_dir.rstrip("/") + "/PREDICTIONS.md", rev) \
        or head
    census = "code/transcript_census_1abe"
    census_rev = L.resolve("main")
    true_dig = L.code_digest(census, census_rev)
    arms = [
        ("a transcript declaring %s's TRUE digest at %s"
         % (census[5:], census_rev[:7]),
         "code-digest: %s\n" % true_dig, census, census_rev, True),
        ("the same transcript with ONE HEX DIGIT changed",
         "code-digest: %s\n" % (("0" if true_dig[0] != "0" else "1")
                                + true_dig[1:]), census, census_rev, False),
        ("a transcript declaring a digest of the WRONG DIRECTORY",
         "code-digest: %s\n" % (L.code_digest(mine_dir, head) or "0" * 16),
         census, census_rev, False),
    ]
    for label, blob, d, r, expect in arms:
        dec = L.declared_digest(blob)
        actual = L.code_digest(d, r)
        got = dec == actual
        print("      %-58s R3 says %s" % (label, "accept" if got else "REFUSE"))
        led.record(got == expect,
                   "D3c %s -> %s (expected %s)"
                   % (label, "accept" if got else "REFUSE",
                      "accept" if expect else "REFUSE"))
    led.record(None,
               "D3c' the third arm is the one that matters and it is this "
               "suite's own first defect: a digest that is TRUE, of a directory "
               "nobody edited, declared by a transcript produced somewhere else")

    # ------------------------------------------------------------- D3d
    led.head("D3d -- R2 MADE CHECKABLE WITHOUT A `git`-INTERCEPTING HARNESS")
    print("""mg-1abe left R2 as an author's declaration and named the check it
wanted: a harness that intercepts `git`.  That is one instrument.  A STATIC read
of the producing code is another, at exactly the grain the census already
trusts -- its own 103-of-112 cause split is the same static proxy, and it says
so on the row.

WHAT IT CAN AND CANNOT DO, stated before the numbers:
  IT CAN     refuse a `reads-outside-tree: no` from a producer that calls `git
             log`.  That is the direction that matters: a FALSE `no` is a
             transcript claiming to be pinnable when it is not.
  IT CANNOT  confirm a `yes`.  A producer may import git and never reach the
             call on the path that produced these bytes.  A `yes` that the
             static read agrees with is CONSISTENT, not verified.
""")
    checked = consistent = contradicted = 0
    for p in pop:
        b = L.blob_at(rev, p)
        if b is None:
            continue
        dec = L.declared_reach(b.decode("utf-8", "replace"))
        if dec is None:
            continue
        checked += 1
        carrier = L.carrying_commit(p, rev)
        static, ev = L.static_reach(os.path.dirname(p), carrier)
        if dec == "no" and static:
            contradicted += 1
            print("      CONTRADICTED  %s declares `no`, its producer calls "
                  "git at %s" % (p, ", ".join(ev[:2])))
        else:
            consistent += 1
    print("    transcripts declaring a reach : %d" % checked)
    print("      consistent with the code    : %d" % consistent)
    print("      CONTRADICTED by the code    : %d" % contradicted)
    led.record(contradicted == 0,
               "D3d R2 is now CHECKED and not merely declared, at %d of %d "
               "declaring transcripts, and %d are contradicted by their own "
               "producer's source" % (checked, len(pop), contradicted))

    print()
    print("    AND THE STATIC READ IS SHOWN GOING BOTH WAYS, or it is not a "
          "check:")
    both = []
    for d in L.suite_dirs(rev)[:400]:
        s, _ = L.static_reach(d, rev)
        both.append((d, s))
    yes = [d for d, s in both if s]
    no = [d for d, s in both if not s]
    print("      directories whose producing code DOES reach outside : %d"
          % len(yes))
    print("      directories whose producing code DOES NOT           : %d"
          % len(no))
    for d in no[:6]:
        print("        %s" % d[5:])
    led.record(bool(yes) and bool(no),
               "D3d' the static read answers BOTH ways over %d directories "
               "(%d reach outside, %d do not).  A test that returned `yes` "
               "everywhere would be `x == x` wearing a name" % (len(both),
                                                                len(yes),
                                                                len(no)))

    # ------------------------------------------------------------- D3e
    led.head("D3e -- WHAT ADOPTION IS AND IS NOT")
    print("""    ADOPTED HERE      : %s (%d transcripts)
    ADOPTED BY mg-1abe: code/transcript_census_1abe (8 transcripts)
    EVERYWHERE ELSE   : nothing, and the number is above.

R1-R3 fix NOTHING retroactively and this script does not pretend otherwise.
What it changes is that the gap is now a NUMBER a control prints, every run,
instead of a sentence in a README.  Adoption is one directory at a time and
each one is cheap: import the ledger, declare, and this script's D3a row
counts it.

WHAT IS STILL NOT DONE:
  * Nothing MAKES a suite adopt.  A convention with a control is not a gate,
    and wiring this into a gate would refuse merges for a state that is normal
    across the whole arc -- mg-1abe measured that trade and refused it, and
    nothing here reopens it.
  * The static R2 check cannot confirm a `yes`, only refuse a `no`.  Named
    above, before the count.
""" % (mine_dir, len(here)))
    led.record(None,
               "D3e coverage is %d of %d transcripts arc-wide, in 2 "
               "directories of %d -- reported as a number by a control rather "
               "than as a sentence in a README"
               % (verdicts.get("AGREES", 0) + verdicts.get("DISAGREES", 0),
                  len(pop), len({os.path.dirname(p) for p in pop})))
    return led.done()


if __name__ == "__main__":
    sys.exit(main())
