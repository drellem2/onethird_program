"""a0 -- THE PARSERS, AGAINST PLANTED WORLDS THAT SAY HOW THEY CAN FAIL.

a4's entire result is a comparison of two census transcripts read back as text.
A parser that quietly returned `{}` would make a4 print `0 rows moved` -- a
green, produced by a broken instrument, that reads exactly like the answer
`nothing needed repairing`.  Two instances of that shape are on record in this
arc and they are CITED rather than counted: mg-9bc2's `run_all.sh` printing
`CLEAN` over a control that never ran, and mg-2f44's positive control, whose
predicate `"8 9" in out` was matching a section listing for its whole life.  So
the parsers are exercised against worlds built to break them BEFORE they are
pointed at the real thing.

EVERY WORLD BELOW IS PLANTED, and each says what a passing parser must NOT do:

  W1  a well-formed table -- the only world where a parser may agree.
  W2  a path longer than T2a's 52-character column, which the producer
      TRUNCATES.  A parser reading fixed column offsets mis-keys exactly the
      long rows and no others, so this is invisible on a sample.
  W3  a detail column containing the word `DIFFERS` -- the repair's own detail
      strings say `the PRE-mg-a71f guard called this DIFFERS`, so a parser
      that searches the line for a bucket name instead of reading the verdict
      FIELD will score a TIMED-OUT row as DIFFERS.  This world exists because
      the repair introduced the hazard.
  W4  an EMPTY table.  The parser must return nothing, and a4 must be able to
      tell "nothing moved" from "nothing was read" -- which is why a4 checks
      the population size rather than trusting a length-zero diff.
  W5  a T2b block whose counts do NOT sum to its denominator.
  W6  a `FLIPS` list terminated by a blank line, and one that says `(none)`.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_a71f as L                                            # noqa: E402

W1 = """
T2a -- EVERY TRANSCRIPT, ONE ROW EACH, NOTHING TRUNCATED
    transcript                                           carry    verdict          producer        detail
    alpha_1/out_a.txt                                    aaaaaaa  REPRODUCES       a.py            12s
    beta_2/out_b.txt                                     bbbbbbb  DIFFERS          b.py            conclusion FLIPS
T2b -- THE COUNTS, WITH THE DENOMINATOR NAMED
    REPRODUCES            1  of 2
    DIFFERS               1  of 2
    TIMED-OUT             0  of 2
T2c -- CLASS 2
"""

W2 = """
T2a -- EVERY TRANSCRIPT, ONE ROW EACH, NOTHING TRUNCATED
    a_directory_with_a_very_long_name_indeed_1234/out_a_long_name.t ccccccc  TIMED-OUT        c.py            suite exceeded 900s
T2b -- THE COUNTS, WITH THE DENOMINATOR NAMED
    TIMED-OUT             1  of 1
T2c -- CLASS 2
"""

W3 = """
T2a -- EVERY TRANSCRIPT, ONE ROW EACH, NOTHING TRUNCATED
    gamma_3/out_g.txt                                    ddddddd  TIMED-OUT        g.py            suite exceeded 900s; the shell had already created this file (0 bytes) -- the PRE-mg-a71f guard called this DIFFERS
T2b -- THE COUNTS, WITH THE DENOMINATOR NAMED
    TIMED-OUT             1  of 1
T2c -- CLASS 2
"""

W4 = """
T2a -- EVERY TRANSCRIPT, ONE ROW EACH, NOTHING TRUNCATED
    transcript                                           carry    verdict          producer        detail
T2b -- THE COUNTS, WITH THE DENOMINATOR NAMED
T2c -- CLASS 2
"""

W5 = """
T2b -- THE COUNTS, WITH THE DENOMINATOR NAMED
    REPRODUCES            3  of 9
    DIFFERS               2  of 9
T2c -- CLASS 2
"""

W6A = """
    every FLIPS, named:
      code/x/out_x.txt
      code/y/out_y.txt

    every NONDETERMINISTIC producer, named
"""

W6B = """
    every FLIPS, named:
      (none)

    every NONDETERMINISTIC producer, named
"""


def main():
    led = L.Ledger("a0 -- mg-a71f's parsers against planted worlds",
                   reads_outside_tree=False)

    led.head("A0a -- W1: A WELL-FORMED TABLE.  The only world where agreement "
             "is allowed to mean anything")
    r = L.parse_t2_rows(W1)
    led.record(r == {"alpha_1/out_a.txt": ("aaaaaaa", "REPRODUCES"),
                     "beta_2/out_b.txt": ("bbbbbbb", "DIFFERS")},
               "A0a two rows, both keyed and both verdicts read: %r" % (r,))
    led.record(L.parse_t2_counts(W1) == {"REPRODUCES": 1, "DIFFERS": 1,
                                         "TIMED-OUT": 0},
               "A0a' the T2b counts read back exactly, INCLUDING the zero -- a "
               "parser that dropped zero rows would make an empty bucket "
               "indistinguishable from an absent one")

    led.head("A0b -- W2: A PATH THE PRODUCER TRUNCATED AT 52 CHARACTERS")
    r = L.parse_t2_rows(W2)
    key = "a_directory_with_a_very_long_name_indeed_1234/out_a_long_name.t"
    led.record(list(r) == [key] and r[key][1] == "TIMED-OUT",
               "A0b the truncated row is keyed by the truncated path and its "
               "verdict is read from the FIELD, not from an offset: %r" % (r,))

    led.head("A0c -- W3: A DETAIL COLUMN CONTAINING THE WORD `DIFFERS`")
    print("""
The repair itself created this hazard: its detail string for a mis-bucketed row
ends `the PRE-mg-a71f guard called this DIFFERS`.  A parser that asked `is
DIFFERS in this line` would score the repaired verdict as the defect it
repairs, in the exact rows the repair moved -- and nowhere else.
""")
    r = L.parse_t2_rows(W3)
    led.record(r.get("gamma_3/out_g.txt", (None, None))[1] == "TIMED-OUT",
               "A0c a TIMED-OUT row whose detail says the word DIFFERS is read "
               "as TIMED-OUT: %r" % (r,))
    led.record("DIFFERS" not in [v for _, v in r.values()],
               "A0c' and no row of W3 is scored DIFFERS by substring")

    led.head("A0d -- W4: AN EMPTY TABLE MUST READ AS EMPTY, NOT AS AGREEMENT")
    led.record(L.parse_t2_rows(W4) == {},
               "A0d an empty T2a yields no rows.  a4 must therefore check the "
               "POPULATION SIZE and not infer `nothing moved` from a diff of "
               "length zero, which is what it does")
    led.record(L.parse_t2_counts(W4) == {},
               "A0d' an empty T2b yields no counts")

    led.head("A0e -- W5: COUNTS THAT DO NOT SUM TO THEIR DENOMINATOR")
    c = L.parse_t2_counts(W5)
    led.record(sum(c.values()) == 5 and c == {"REPRODUCES": 3, "DIFFERS": 2},
               "A0e the parser reports what is there (%r, summing to %d against "
               "a stated 9) rather than repairing it.  Adjudicating the sum is "
               "the census's own T2b ledger row and not this parser's job"
               % (c, sum(c.values())))

    led.head("A0f -- W6: THE FLIPS LIST, POPULATED AND EMPTY")
    led.record(L.parse_t2_flips(W6A) == ["code/x/out_x.txt",
                                         "code/y/out_y.txt"],
               "A0f a populated FLIPS list reads back exactly and stops at the "
               "blank line: %r" % (L.parse_t2_flips(W6A),))
    led.record(L.parse_t2_flips(W6B) == [],
               "A0f' `(none)` reads back as the empty list and NOT as a path "
               "called `(none)`")

    return led.done()


if __name__ == "__main__":
    sys.exit(main())
