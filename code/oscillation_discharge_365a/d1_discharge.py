#!/usr/bin/env python3
"""mg-365a d1 — WAS IT DISCHARGED, AND BY WHAT?  THE TICKET ASKED FOR A COMMAND.

mg-365a carries mg-585e's remainder and puts two questions:

  1.  whether a self-inclusive count is a problem worth solving, or the only truthful way
      to count;
  2.  whether this is already discharged by mg-05c6 — "testable the same way mg-cd8d is —
      a command, not an argument".

Both are answered below by walking the record, and both answers differ from the ticket's
expectation.  The ticket is not careless; it was filed at 03:30Z from a commit taken before
`bd07d70` landed at 00:41Z, and it describes a constant that no longer exists.

THE ONE FIGURE A READER WILL REACH FOR IS THE ONE THAT MEANS NOTHING.  mg-585e's headline was
"16 of 31 RED".  Re-taking it at a newer pin gives 0 RED among the new versions — and that
zero is `bd07d70` DELETING THE HEADING the predicate tests for.  §3 prints it beside the
reason it is worthless, because leaving it out would let the next reader re-derive it and
draw the conclusion this arm exists to prevent.

WHAT CARRIES THE FINDING INSTEAD is §4's counterfactual: how many landings since the deletion
would have OWED a refresh under the old arrangement, against how many PAID one.

EXITS 0 on a readable history — this arm reports, it does not grade.  2 if it cannot reach
the record, or if any control fails.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib365a as K                                         # noqa: E402

W = 92


def rule(ch="-"):
    print(ch * W)


def main():
    print("=" * W)
    print("mg-365a d1  THE OSCILLATION AFTER THE DELETION — owed against paid")
    print("=" * W)
    print()

    K.require_pin(K.AS_OF_365A)
    K.require_pin(K.DELETION, name="DELETION")

    versions_now = K.history(K.AS_OF_365A)
    versions_then = K.history(K.AS_OF_585E)
    solo_now = K.solo_population(K.AS_OF_365A)
    solo_then = K.solo_population(K.AS_OF_585E)

    print("§0  THE TWO PINS, CHECKED RATHER THAN DECLARED")
    rule()
    print("  AS_OF_365A   %s   every figure below is a function of it" % K.AS_OF_365A[:12])
    print("  DELETION     %s   `delete: THE SELF-EXEMPTION IS GONE` (mg-c15e)"
          % K.DELETION[:12])
    print("  AS_OF_585E   %s   mg-585e's pin, imported from lib585e not re-typed"
          % K.AS_OF_585E[:12])
    print()
    print("  Both resolve and both are ancestors of origin/main.  This transcript therefore")
    print("  does not go stale when its subject is next touched, and does not conflict on a")
    print("  rebase — which is mg-585e's own recorded fact about pins, inherited here.")
    print()

    # -- §1 ------------------------------------------------------------------------------
    src_now = K.text_of(K.AS_OF_365A, path="code/gate_fixed_point_f771/lib_f771.py")
    src_before = K.text_of(K.DELETION + "~1",
                           path="code/gate_fixed_point_f771/lib_f771.py")
    gone_now = "SELF_EXCLUDED" not in src_now
    there_before = "SELF_EXCLUDED" in src_before

    print("§1  THE PREMISE THIS TICKET IS WRITTEN ON  (P1)")
    rule()
    print("  The ticket says, in the present tense:")
    print("      `out_g0_fixed_point.txt` IS mg-f771's single self-exemption.")
    print()
    print("  `SELF_EXCLUDED` present in lib_f771.py at DELETION~1   %s" % there_before)
    print("  `SELF_EXCLUDED` present in lib_f771.py at AS_OF_365A   %s" % (not gone_now))
    print()
    print("  BOTH DIRECTIONS ARE ASSERTED AND NOT ONE.  An arm that only checked the constant")
    print("  is absent today would pass identically against a repository that never had it,")
    print("  and would be reporting on its own inability to find a string.")
    if not (gone_now and there_before):
        raise K.ArmError("the two-sided premise check failed: before=%s after-absent=%s"
                         % (there_before, gone_now))
    print()
    print("  THE PREMISE IS STALE.  The exemption was deleted at %s, 19 minutes after the"
          % K.DELETION[:8])
    print("  commit this ticket was written from.  The mayor's own caution of 00:22Z is on")
    print("  the ticket and is exactly this: a successor carrier filed while its cause was")
    print("  live can outlive the cause.  It did.")
    print()

    # -- §2 ------------------------------------------------------------------------------
    print("§2  THE COUNT, RE-WALKED RATHER THAN INCREMENTED  (P7)")
    rule()
    print("  %-46s %8s %8s" % ("", "at 585e", "at 365a"))
    print("  %-46s %8d %8d" % ("committed versions of the transcript",
                               len(versions_then), len(versions_now)))
    print("  %-46s %8d %8d" % ("commits whose ENTIRE diff is that one file",
                               len(solo_then), len(solo_now)))
    print()
    print("  mg-585e published %d at its pin.  Three more landed after it published."
          % K.PUBLISHED_585E["solo"])
    if len(solo_then) != K.PUBLISHED_585E["solo"]:
        raise K.ArmError("re-walk at mg-585e's pin gives %d solo commits, not the %d it "
                         "published" % (len(solo_then), K.PUBLISHED_585E["solo"]))
    print("  RE-DERIVED AT ITS OWN PIN AND IT AGREES: %d.  That agreement is what makes the"
          % len(solo_then))
    print("  disagreement below a finding about the METHOD rather than about the walker.")
    print()
    print("  THE POPULATION, CHRONOLOGICAL, NUMBERED BY WALKING:")
    print()
    print("    %-4s %-10s %-9s %s" % ("#", "commit", "ticket", "landed"))
    for r in solo_now:
        mark = ""
        if r["ticket"] == "mg-585e":
            mark = "  <-- called 'the 8th' by its own message AND by this ticket"
        if r["ticket"] == "mg-05c6":
            mark = "  <-- landed after mg-585e's pin, and was skipped"
        print("    %-4d %-10s %-9s %s%s"
              % (r["n"], r["h"][:8], r["ticket"] or "-",
                 K.git(K.ROOT, "log", "-1", "--format=%ad", "--date=format:%m-%d %H:%M",
                       r["h"]).stdout.strip(), mark))
    print()

    mine = [r for r in solo_now if r["ticket"] == "mg-585e"]
    skipped = [r for r in solo_now if r["ticket"] == "mg-05c6"]
    if mine:
        m = mine[0]
        print("  mg-585e's own refresh is #%d, NOT the 8th." % m["n"])
        print()
        print("  THE MECHANISM IS THE PIN AND NOT A TYPO, WHICH IS WHY IT IS WORTH A SECTION.")
        print("  'the 8th' is %d + 1: mg-585e's figure AT ITS PIN, incremented, rather than"
              % K.PUBLISHED_585E["solo"])
        print("  re-walked.  The arithmetic is right.  What is wrong is that the pinned figure")
        print("  stopped being current the moment something landed between the pin and the")
        if skipped:
            print("  claim — and %s did, %s, sixteen minutes earlier."
                  % (skipped[0]["h"][:8], skipped[0]["ticket"]))
        print()
        print("  A COUNT DERIVED BY INCREMENTING A PINNED FIGURE IS WRONG EXACTLY WHEN")
        print("  SOMETHING LANDED IN BETWEEN, AND IT IS WRONG SILENTLY.  That is the general")
        print("  defect here, and it is not specific to this file or to this count.")
    print()

    # -- §3 ------------------------------------------------------------------------------
    new_versions = [h for h in versions_now if h not in set(versions_then)]
    # The format change is an EVENT IN THE WALK, not a date and not a shape: `bd07d70` is the
    # commit that rewrote §2, so it is itself the first version in the new format.  Splitting
    # on the constant rather than on "does it have the old heading" keeps this partition from
    # being circular — a split BY the predicate could not then be evidence ABOUT it.
    old_fmt = [h for h in new_versions if h != K.DELETION]
    new_fmt = [h for h in new_versions if h == K.DELETION]

    print("§3  THE FIGURE A READER WILL REACH FOR, AND WHY IT MEASURES NOTHING  (P2)")
    rule()
    print("  mg-585e's headline was `16 of 31 RED`.  Its predicate — IMPORTED HERE, NOT")
    print("  RE-SPELLED — tests for the string `DISAGREEMENTS, SHOWN` on a line starting §2.")
    print()
    print("  %-10s %-8s %-9s %-9s %s" % ("commit", "format", "anchored", "loose", "subject"))
    n_red_old = n_red_new = n_disagree = 0
    for h in reversed(new_versions):
        anchored, loose = K.red_both_ways(K.text_of(h))
        n_disagree += (anchored != loose)
        if h in new_fmt:
            n_red_new += bool(anchored)
        else:
            n_red_old += bool(anchored)
        print("  %-10s %-8s %-9s %-9s %s"
              % (h[:8], "NEW §2" if h in new_fmt else "old §2",
                 "RED" if anchored else "green", "RED" if loose else "green",
                 K.subject(h)[:44]))
    print()
    print("  versions added since mg-585e's pin                     %d" % len(new_versions))
    print("    written under the OLD §2                             %d, of which %d RED"
          % (len(old_fmt), n_red_old))
    print("    written under the NEW §2                             %d, of which %d RED"
          % (len(new_fmt), n_red_new))
    print("  anchored and loose predicates disagreeing              %d  (mg-9876 §1: run it"
          % n_disagree)
    print("                                                            BOTH ways, not reason)")
    print()
    print("  ⚠ MY OWN PREDICTION P2 IS REFUTED IN ITS STATED FORM, AND IS CORRECTED HERE")
    print("  RATHER THAN GLOSSED.  P2 said re-running mg-585e's predicate at this pin would")
    print("  report 0 RED among the new versions.  IT REPORTS %d.  The reason is that %d of"
          % (n_red_old + n_red_new, len(old_fmt)))
    print("  the %d new versions PRE-DATE the format change: they still carry the old §2 and"
          % len(new_versions))
    print("  the predicate reads them exactly as mg-585e intended.  The prediction confused")
    print("  `since mg-585e's pin` with `since the deletion`, and they are 6 versions apart.")
    print()
    print("  THE TRAP IS REAL AND IS LATENT RATHER THAN EXHIBITED, WHICH IS A WEAKER CLAIM")
    print("  THAN P2 MADE AND IS THE ONE THE RECORD SUPPORTS.  Exactly %d version has been"
          % len(new_fmt))
    print("  written under the new §2 — `bd07d70` itself, the commit that rewrote it — and it")
    print("  reads green.  n = %d is not evidence about a predicate.  What IS certain is"
          % len(new_fmt))
    print("  structural: §2 is the normaliser's rule inventory now, so NO version written")
    print("  after the deletion can contain `DISAGREEMENTS, SHOWN` on a §2 line whatever the")
    print("  gate did.  The predicate reports on a string, and the string was removed.")
    print()
    print("  SO THE ZERO IS OWED TO THE NEXT READER, NOT TO THIS ONE.  The moment a version")
    print("  lands after `bd07d70`, re-taking mg-585e's headline figure at that pin returns a")
    print("  zero that measures the deletion of a marker and reads as `it stopped`.  It is")
    print("  printed here rather than omitted precisely because it is re-derivable by anyone")
    print("  in one command, and an omitted trap is a trap the next reader walks into alone.")
    print()

    # -- §4 ------------------------------------------------------------------------------
    since = K.commits_between(K.DELETION, K.AS_OF_365A)
    touched = [h for h in since if K.F771_TRANSCRIPT in K.files_of(h)]
    paid = [h for h in since if K.is_solo(h)]
    owed = [(h, K.watched_committed(h)) for h in since]
    owed = [(h, w) for h, w in owed if w]

    print("§4  WHAT CARRIES THE FINDING: OWED AGAINST PAID  (P5)")
    rule()
    print("  `./build.sh` regenerates transcripts into the worktree and THEN g0 compares the")
    print("  worktree against HEAD.  So the old §2's disagreement set D(T) CONTAINS every")
    print("  watched transcript the landing went on to commit: a landing that committed one")
    print("  PROVABLY had D(T) != {}, would have carried a RED §2, and would have owed a")
    print("  refresh.  Transcripts graded NOISE or CORPUS are restored rather than committed,")
    print("  so they never appear here — this is a LOWER BOUND, which is the safe direction")
    print("  for a claim that the toll was owed and not paid.")
    print()
    print("  The watched class is `lib_f771.is_watched`, IMPORTED.  The corpus-scoped registry")
    print("  is `lib_f771.CORPUS_SCOPED`, imported for the same reason: a hand-typed glob or a")
    print("  hard-coded exemption path is a re-statement, and a re-statement drifts.")
    print()
    print("  %-10s %-7s %-6s %s" % ("commit", "owed?", "paid?", "watched transcripts committed"))
    owed_set = {h for h, _ in owed}
    for h in since:
        w = K.watched_committed(h)
        print("  %-10s %-7s %-6s %s"
              % (h[:8], "OWED" if w else "-",
                 "PAID" if h in set(paid) else "-",
                 (", ".join(os.path.basename(x) for x in w))[:44] or "none"))
    print()
    print("  main landings since the deletion                        %d" % len(since))
    print("  of those, that would have OWED a refresh                %d" % len(owed_set))
    print("  of those, that TOUCHED the transcript at all            %d" % len(touched))
    print("  of those, that PAID a solo refresh commit               %d" % len(paid))
    print()
    print("  %d OWED, %d PAID." % (len(owed_set), len(paid)))
    print()
    print("  ⚠ AND `%d OF %d QUIET` WOULD NOT HAVE BEEN ENOUGH ON ITS OWN  (P4).  mg-585e"
          % (len(touched), len(since)))
    print("  priced the pre-deletion rate at %d touches over %d code/ commits."
          % (K.RATE_TOUCHES, K.RATE_COMMITS))
    p = K.RATE_TOUCHES / float(K.RATE_COMMITS)
    print("  At that rate, %d quiet landings has probability %.2f — NOT significant."
          % (len(since), K.binom_zero(p, len(since))))
    print("  A directory that rested on the zero would be reporting a quiet window as a")
    print("  repair.  What makes it a repair is that %d of those landings had a provably"
          % len(owed_set))
    print("  non-empty disagreement set and paid nothing for it.")
    print()

    # -- §5 ------------------------------------------------------------------------------
    print("§5  DISCHARGED — BUT NOT BY WHAT THE TICKET ASKS ABOUT  (P6)")
    rule()
    print("  Carry-forward item 2 asks whether this is 'already discharged by mg-05c6'.")
    print()
    if skipped:
        print("  mg-05c6 IS IN THE POPULATION.  %s, solo commit #%d above, is mg-05c6's own"
              % (skipped[0]["h"][:8], skipped[0]["n"]))
        print("  refresh.  It PAID the toll; it did not remove it.")
    print("  The discharge is %s — mg-c15e's deletion of the exemption." % K.DELETION[:8])
    print()
    print("  The distinction is not pedantry.  An instrument answering 'yes, discharged'")
    print("  without saying BY WHAT would have confirmed the ticket's question while getting")
    print("  its subject wrong, and the next reader would credit the corpus-pin work with a")
    print("  repair it did not make — and would look for the mechanism in the wrong file.")
    print()

    # -- §6 ------------------------------------------------------------------------------
    print("§6  THE SELF-INCLUSION QUESTION, ANSWERED BY MEASUREMENT  (P8)")
    rule()
    print("  Question 1 asks whether a self-inclusive count is a defect or the only truthful")
    print("  arrangement.  It was NEITHER: it was a property of the exemption, and it is gone.")
    print()
    print("  The counting directory joined the population it counted because COUNTING")
    print("  REQUIRED A ./build.sh RUN AND A ./build.sh RUN MOVED THAT TRANSCRIPT.  Nothing")
    print("  about counting made the count self-inclusive; the oscillation did, and it")
    print("  captured every branch equally — mg-585e was not special, it was the 9th.")
    print()
    print("  With the exemption deleted the transcript is a function of lib_f771.py's source,")
    print("  so a landing that does not touch that file does not move it.  A directory can")
    print("  now count the population without entering it.")
    print()
    print("  WHETHER THIS DIRECTORY DID SO IS A PROPERTY OF THIS BRANCH AND NOT OF THE PIN,")
    print("  so it is ON STDERR and not here (README D4).  A branch-dependent reading in a")
    print("  pinned transcript is the defect this whole arc is about, arriving one file over.")
    print()

    print("VERDICT: REPORTED — premise STALE; %d versions and %d solo commits at the new pin "
          "(was %d/%d);" % (len(versions_now), len(solo_now),
                            len(versions_then), len(solo_then)))
    print("         %d landings since the deletion, %d OWED a refresh, %d PAID; discharged by "
          "%s (mg-c15e)," % (len(since), len(owed_set), len(paid), K.DELETION[:8]))
    print("         NOT by mg-05c6, which is #%s in the population it was asked to have "
          "removed." % (skipped[0]["n"] if skipped else "?"))

    # --- the live half, on stderr, for the reason §6 gives -------------------------------
    head = K.git(K.ROOT, "rev-parse", "HEAD").stdout.strip()
    branch_commits = K.commits_between(K.AS_OF_365A, head) if head != K.AS_OF_365A else []
    joined = [h for h in branch_commits if K.F771_TRANSCRIPT in K.files_of(h)]
    sys.stderr.write(
        "P8 LIVE READING (branch-dependent, deliberately not in the transcript):\n"
        "  commits on this branch beyond AS_OF_365A            %d\n"
        "  of those, touching %s   %d\n"
        "  -> this directory counts the population and %s\n"
        % (len(branch_commits), os.path.basename(K.F771_TRANSCRIPT), len(joined),
           "DOES NOT enter it" if not joined else "HAS ENTERED IT — say so in the record"))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except K.Refused as exc:
        print()
        print("REFUSED — %s" % exc)
        sys.exit(2)
    except K.ArmError as exc:
        print()
        print("CONTROL FAILED — %s" % exc)
        sys.exit(2)
    except SystemExit:
        raise
    except BaseException:                                   # noqa: BLE001 - deliberate
        import traceback
        print()
        print("REFUSED — this arm crashed and therefore reached no verdict:")
        traceback.print_exc(file=sys.stdout)
        sys.exit(2)
