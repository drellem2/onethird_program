"""a4 -- SIZING THE 107, BY COMPARING TWO CENSUSES OF THE SAME POPULATION.

mg-a71f's constraint, in its own words: *Size the 107 DIFFERS: report how many
are timeout artefacts.  That number is the actual correction to the damage
figure.*

WHY THIS NEEDED A ~2 HOUR RE-RUN AND COULD NOT BE DERIVED ON PAPER.  The old
census's transcript records, for every DIFFERS row, `conclusion FLIPS/HELD/...`
and NOTHING ELSE.  The per-group RUN STATUS -- `ok`, `failed:n`, `timeout` --
was never printed for a row that differed; only REPRODUCES rows carry a
duration.  So THE OLD RUN'S TIMEOUTS ARE NOT RECOVERABLE FROM ITS OWN OUTPUT.
There is no arithmetic that turns 112 into `x timeouts and 112-x differences`;
the only instrument that can answer is the repaired census, re-run.  That is
the whole cost of the bucket having been unreachable: the evidence that would
have sized it was never written down.

THE TWO RUNS ARE THE SAME MEASUREMENT IN ONE RESPECT AND NOT IN OTHERS, AND
THIS SCRIPT REFUSES TO CONFLATE THEM.

  SAME       the as-of (`81214a9`), so the population, the carrying commits
             and the committed bytes are identical in both.  A4a checks that
             rather than assuming it: two censuses of different populations
             are not comparable and a diff between them is noise with a
             headline on it.
  DIFFERENT  the INSTRUMENT (repaired), the WALL CLOCK (days apart, `main` far
             ahead, other agents on the box), and therefore the load a 900 s
             budget buys.  A row can move for any of those reasons.

So a4 splits every move into what the repair can explain and what it cannot,
and REFUSES to credit the repair with the second kind.  A row moving
DIFFERS -> TIMED-OUT is the repair's signature.  A row moving REPRODUCES ->
DIFFERS is the repository having moved under a producer that reads it, which is
the census's own T2e finding and nothing to do with mg-a71f.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_a71f as L                                            # noqa: E402

NEW_T2 = os.path.join(L.REPO, L.CENSUS_DIR, "out_t2_census.txt")


def header_facts(text):
    """(as-of, population) as the transcript states them about itself."""
    as_of = re.search(r"^\s*as-of\s+([0-9a-f]{40})", text, re.M)
    pop = re.search(r"^\s*population\s+(\d+) transcripts", text, re.M)
    return (as_of.group(1) if as_of else None,
            int(pop.group(1)) if pop else None)


def main():
    led = L.Ledger("a4 -- SIZING THE 107: THE SAME POPULATION, THE OLD "
                   "INSTRUMENT AND THE REPAIRED ONE")

    if not os.path.exists(NEW_T2):
        led.self_error("the repaired census has not been run: %s absent"
                       % NEW_T2)
        return led.done()
    with open(L.PRIOR_T2, encoding="utf-8", errors="replace") as fh:
        old_t = fh.read()
    with open(NEW_T2, encoding="utf-8", errors="replace") as fh:
        new_t = fh.read()

    # ------------------------------------------------------------------ A4a
    led.head("A4a -- ARE THESE TWO CENSUSES OF THE SAME POPULATION?")
    print("""
Checked, not assumed.  If the as-of or the denominator differ, every row below
is a comparison between two different questions and must not be read as a
correction of anything.
""")
    o_as, o_pop = header_facts(old_t)
    n_as, n_pop = header_facts(new_t)
    print("    %-8s %-42s %s" % ("", "PRIOR (mg-1abe, unrepaired)",
                                 "THIS RUN (mg-a71f, repaired)"))
    print("    %-8s %-42s %s" % ("as-of", o_as or "?", n_as or "?"))
    print("    %-8s %-42s %s" % ("pop", o_pop, n_pop))
    same = (o_as == n_as and o_pop == n_pop and o_pop)
    led.record(bool(same),
               "A4a both transcripts state the same as-of (%s) and the same "
               "denominator (%s).  The comparison below is row-for-row over "
               "one population" % (o_as[:7] if o_as else "?", o_pop))
    if not same:
        led.self_error("A4a' the two runs do not share a population.  "
                       "STOPPING: a transition matrix between different "
                       "denominators is not a measurement")
        return led.done()

    old_rows = L.parse_t2_rows(old_t)
    new_rows = L.parse_t2_rows(new_t)
    led.record(len(old_rows) == o_pop and len(new_rows) == n_pop,
               "A4a' the T2a tables parse to %d and %d rows against stated "
               "populations of %d and %d.  A parser that silently read nothing "
               "would print `0 moved` below, which is why this is a row and "
               "not a comment" % (len(old_rows), len(new_rows), o_pop, n_pop))
    if not old_rows or not new_rows:
        led.self_error("A4a'' a table parsed to nothing; every count below "
                       "would be a fact about the parser")
        return led.done()

    # ------------------------------------------------------------------ A4b
    led.head("A4b -- THE TRANSITION MATRIX, EVERY ROW ACCOUNTED FOR")
    keys = sorted(set(old_rows) | set(new_rows))
    trans = {}
    for k in keys:
        o = old_rows.get(k, ("", "ABSENT"))[1]
        n = new_rows.get(k, ("", "ABSENT"))[1]
        trans.setdefault((o, n), []).append(k)
    order = ["REPRODUCES", "DIFFERS", "NOT-REGENERATED", "NO-RUNNER",
             "RUNNER-FAILED", "TIMED-OUT", "SELF", "SKIPPED", "ABSENT"]
    seen = sorted({b for pair in trans for b in pair},
                  key=lambda b: order.index(b) if b in order else 99)
    print("    rows: PRIOR verdict.  columns: THIS RUN's verdict.")
    print("    %-18s %s" % ("", " ".join("%9s" % b[:9] for b in seen)))
    for o in seen:
        cells = [len(trans.get((o, n), [])) for n in seen]
        if not any(cells):
            continue
        print("    %-18s %s" % (o, " ".join("%9d" % c for c in cells)))
    moved = {p: v for p, v in trans.items() if p[0] != p[1]}
    led.record(not moved,
               "A4b %d of %d rows have the same verdict in both runs; %d moved"
               % (len(keys) - sum(len(v) for v in moved.values()), len(keys),
                  sum(len(v) for v in moved.values())))

    # ------------------------------------------------------------------ A4c
    led.head("A4c -- THE ANSWER TO THE TICKET'S QUESTION")
    old_differs = [k for k in keys if old_rows.get(k, ("", ""))[1] == "DIFFERS"]
    old_flips = [p[len("code/"):] for p in L.parse_t2_flips(old_t)]
    artefacts = [k for k in old_differs
                 if new_rows.get(k, ("", ""))[1] == "TIMED-OUT"]
    still = [k for k in old_differs
             if new_rows.get(k, ("", ""))[1] == "DIFFERS"]
    other = [k for k in old_differs if k not in artefacts and k not in still]
    print("""
Of the transcripts the PRIOR census bucketed DIFFERS, how many does the
REPAIRED census decline to measure at the same budget?
""")
    print("    prior DIFFERS                                   %4d"
          % len(old_differs))
    print("      ...of which prior FLIPS (published as damage) %4d"
          % len(old_flips))
    print("      ...of which the rest -- the ticket's `107`    %4d"
          % (len(old_differs) - len(old_flips)))
    print()
    print("    THIS RUN's verdict for those %d rows:" % len(old_differs))
    print("      TIMED-OUT   %4d   <- NOT MEASURED.  Under the old guard every "
          "one of these was" % len(artefacts))
    print("                        a DIFFERS, and any carrying a decision was "
          "a FALSE RECORD.")
    print("      DIFFERS     %4d   <- re-run to completion and still not the "
          "committed bytes" % len(still))
    print("      other       %4d   <- moved for a reason that is not the "
          "repair; named in A4d" % len(other))
    print()
    print("    every prior DIFFERS this run could not measure, named:")
    for k in artefacts:
        print("      %s" % k)
    if not artefacts:
        print("      (none)")
    led.record(not artefacts,
               "A4c %d of the %d prior DIFFERS are TIMED-OUT under the "
               "repaired instrument at the same %s budget.  Each one is a row "
               "the census reported as non-reproducing having never finished "
               "measuring it"
               % (len(artefacts), len(old_differs), "900 s"))

    print()
    print("    THE FIVE PUBLISHED AS FALSE RECORDS, one at a time:")
    print("      %-56s %-14s %s" % ("transcript", "PRIOR", "THIS RUN"))
    flip_art = 0
    for k in old_flips:
        n = new_rows.get(k, ("", "ABSENT"))[1]
        if n == "TIMED-OUT":
            flip_art += 1
        print("      %-56s %-14s %s" % (k[:56], "DIFFERS/FLIPS", n))
    led.record(not flip_art,
               "A4c' %d of the %d transcripts mg-1abe PUBLISHED AS FALSE "
               "RECORDS are, under the repaired instrument, NOT MEASURED AT "
               "ALL.  That is the correction to the damage figure this ticket "
               "asked for, and it is a correction made by an instrument rather "
               "than by an argument" % (flip_art, len(old_flips)))

    # ------------------------------------------------------------------ A4d
    led.head("A4d -- WHAT THE REPAIR MAY NOT BE CREDITED WITH")
    print("""
Two runs days apart on a shared box, with `main` far ahead of where it was, do
not differ only by the repair.  Every move whose new verdict is NOT TIMED-OUT
is attributed elsewhere and named here, so that the headline above cannot
quietly absorb it.

The census's own T2e says the largest cause of non-reproduction in this arc is
A PRODUCER THAT READS REPOSITORY-GLOBAL STATE.  Such a row moves whenever
anybody commits anything.  Between these two runs, `main` moved a long way.
""")
    unrelated = {p: v for p, v in moved.items() if p[1] != "TIMED-OUT"}
    n_unrel = sum(len(v) for v in unrelated.values())
    for (o, n), v in sorted(unrelated.items(), key=lambda kv: -len(kv[1])):
        print("    %-18s -> %-18s %4d" % (o, n, len(v)))
        for k in v[:6]:
            print("        %s" % k)
        if len(v) > 6:
            print("        ... and %d more" % (len(v) - 6))
    if not unrelated:
        print("    (no row moved to any bucket other than TIMED-OUT)")
    led.record(None,
               "A4d %d rows moved to a bucket that is NOT TIMED-OUT.  The "
               "repair cannot explain these and is not credited with them: "
               "the instrument changed, and so did the repository and the "
               "machine" % n_unrel)

    # ------------------------------------------------------------------ A4e
    led.head("A4e -- WHAT THIS RUN DOES **NOT** SAY")
    o_counts = L.parse_t2_counts(old_t)
    n_counts = L.parse_t2_counts(new_t)
    print("""
⚠️  112 STANDS AS AN UPPER BOUND ON NON-REPRODUCTION WHOSE SLACK IS UNSIZED.
cf8e5 was explicit that nothing in this ticket weakens that, and this run must
not be reported as having weakened it unless it MEASURED it.  It did not.  What
it measured is how many rows the repaired instrument declines to measure at a
900-second budget on this machine today -- a number that moves with the budget
and with the box, and the census's own T2d says so.

⚠️  AND THIS RUN CANNOT SAY WHAT THE OLD RUN'S TIMEOUTS WERE.  A row that is
TIMED-OUT today may have finished inside the budget then, on a quieter machine,
and genuinely differed.  The old transcript records no status for a DIFFERS row,
so that question is closed forever.  The honest reading of A4c is `these rows
are not evidence of non-reproduction`, NOT `these rows reproduced`.

⚠️  THE OLD CENSUS'S NUMBERS ARE NOT OVERWRITTEN.  They stand in this directory
verbatim as `prior_1abe_t2_census_at_81214a9.txt`, and the pair is printed
below rather than the new one alone.
""")
    print("    %-18s %14s %14s" % ("bucket", "PRIOR", "THIS RUN"))
    for b in order:
        if b in o_counts or b in n_counts:
            print("    %-18s %14s %14s" % (b, o_counts.get(b, "-"),
                                           n_counts.get(b, "-")))
    led.record(None,
               "A4e the two censuses stand side by side.  The new one is A "
               "DIFFERENT MEASUREMENT -- same population, repaired instrument, "
               "different day -- and not a correction applied to the old one's "
               "numbers")

    return led.done()


if __name__ == "__main__":
    sys.exit(main())
