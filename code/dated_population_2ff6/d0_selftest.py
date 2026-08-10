"""mg-2ff6 / D0 -- THE FORCED ARMS.

An instrument whose job is to say `these figures moved and those did not` has
exactly one interesting way to be wrong: to say `did not` because it could not
see.  Every arm below is a case whose answer is known before the run, and at
least one of them is a case where the arm must say NO.

  D0a  cfd9c's selector, EXTRACTED and not re-typed -- and shown to reject
  D0b  the section rule, on a fixture built to break a label-only key
  D0c  the three classes, all four inputs, against cfd9c's own table
  D0d  the interval, INCLUDING the empty one
  D0e  the published ref resolves and carries every transcript
  D0f  the accounting compared against ITSELF -- the null result
  D0g  and nothing this ticket prints into another tree is a count row

Exit code = number of D0 arms that fail.
"""

import sys

import lib2ff6 as U

BAD = 0

U.bar("mg-2ff6 / D0 -- THE FORCED ARMS")
print("HEAD: %s   published-from: %s" % (U.head(), U.PUBLISHED_AT))


def arm(name, got, want):
    global BAD
    ok = got == want
    BAD += not ok
    print("      %-56s %s" % (name, "ok" if ok else "*** NO (%r != %r)"
                              % (got, want)))
    return ok


# ---------------------------------------------------------------------------
U.hdr("D0a  cfd9c's SELECTOR, LIFTED OUT OF cfd9c's OWN FILE")

print("  The checker is inline in `s4_convention.py` and importing a probe")
print("  runs it, so there is no import to make.  There is also no excuse for")
print("  a second copy: the ticket's trap is that this checker has already")
print("  been respecified once by the tree it was checking, and a re-typing")
print("  here is how that would happen a second time without anyone deciding")
print("  to.  So the SOURCE TEXT is lifted and compiled:")
print()
src = U.corpus_label_source()
for ln in src.strip("\n").splitlines():
    print("      %s" % ln.strip())
print()
rx = U.corpus_label_rx()
U.pop("6 label STRINGS whose answer is known before the run")
arm("`...ARTIFACTS in that corpus` is arc-wide",
    bool(rx.search("...ARTIFACTS in that corpus")), True)
arm("`...count ROWS in them` is arc-wide",
    bool(rx.search("...count ROWS in them")), True)
arm("`...distinct grain WORDS in the corpus` is arc-wide",
    bool(rx.search("...distinct grain WORDS in the corpus")), True)
arm("`...probe WORDS classifying as pre-registered` is NOT",
    bool(rx.search("...probe WORDS classifying as pre-registered")), False)
arm("`...ROWS NOT at stage `label`` is NOT",
    bool(rx.search("...ROWS NOT at stage `label`")), False)
arm("`...AXES to be separated` is NOT",
    bool(rx.search("...AXES to be separated")), False)
print("      ^ one unit of each is one label string")
print()
print("  THE THREE `NOT` ROWS ARE THE ARM.  A selector that answered `yes` to")
print("  everything would score this ticket 27 of 27 and mean nothing.")

# ---------------------------------------------------------------------------
U.hdr("D0b  THE SECTION RULE, ON A FIXTURE BUILT TO BREAK A LABEL-ONLY KEY")

FIX = "\n".join([
    "=" * 74, "S1  THE FIRST SECTION", "=" * 74, "",
    "  population: the first thing",
    "      ...count ROWS in them                                    11",
    "",
    "=" * 74, "S2  THE SECOND SECTION", "=" * 74, "",
    "  population: a different thing",
    "      ...count ROWS in them                                    22",
    "      ...count ROWS in them                                    33",
    ""])
k = U.keyed(FIX)
U.pop("1 synthetic transcript carrying the same LABEL 3 times")
arm("3 count rows, 3 distinct keys", len(k), 3)
arm("the first is tagged with its own section",
    sorted(kk[0] for kk in k)[0], "S1  THE FIRST SECTION")
arm("the two in one section are told apart by ORDINAL",
    sorted(kk[2] for kk in k if kk[0].startswith("S2")), [1, 2])
print("      ^ one unit of each is one count row")
print()
print("  `out_a6_self.txt` REALLY DOES PRINT `...count ROWS in them` TWICE IN")
print("  ONE SECTION -- once over this tree's transcripts and once over its")
print("  prose.  A key of (section, label) merges them and reports one of the")
print("  two as unmoved forever.")

# ---------------------------------------------------------------------------
U.hdr("D0c  THE THREE CLASSES, ALL FOUR INPUTS")

U.pop("the 4 (population-is-a-ref, observer-in-population) INPUTS")
arm("(ref, observer outside)   -> FROZEN", U.state_of(True, False), "FROZEN")
arm("(ref, observer inside)    -> FROZEN", U.state_of(True, True), "FROZEN")
arm("(glob, observer outside)  -> GROWING", U.state_of(False, False), "GROWING")
arm("(glob, observer inside)   -> OBSERVED", U.state_of(False, True),
    "OBSERVED")
print("      ^ one unit of each is one pair of booleans")
print()
print("  THE TOP TWO ROWS ARE THE SAME CLASS AND THAT IS NOT AN OVERSIGHT: a")
print("  ref-pinned population cannot contain the censor, because the censor's")
print("  transcript is untracked while it runs.  cfd9c's S4a says so; this arm")
print("  is here so that a later edit to `state_of` cannot quietly disagree.")

# ---------------------------------------------------------------------------
U.hdr("D0d  THE PUBLISHED FORM, INCLUDING THE EMPTY INTERVAL")

U.pop("4 rendered FIGURES whose text is known before the run")
arm("FROZEN carries a ref and no range",
    U.render_figure(1191, "FROZEN", ref="9f1ecaa+eacc5e1"),
    "1191 @9f1ecaa+eacc5e1")
arm("GROWING says so", U.render_figure(832, "GROWING", ref="5c8f879"),
    "832 @5c8f879 (GROWING)")
arm("OBSERVED is an interval",
    U.render_figure(2093, "OBSERVED", low=2019, ref="5c8f879"),
    "2019-2093 @5c8f879 (OBSERVED)")
arm("and an EMPTY interval stays empty",
    U.render_figure(832, "OBSERVED", low=832, ref="5c8f879"),
    "832-832 @5c8f879 (OBSERVED)")
print("      ^ one unit of each is one rendered figure")
print()
print("  THE LAST ROW IS THE ONE THAT MATTERS.  `files` cannot tell the two")
print("  write regimes apart, because `>` truncates and does not unlink, so")
print("  its interval is empty and must STAY empty.  A convention that put a")
print("  range on every field would be decorating the one field not at risk,")
print("  which is how an error bar stops meaning anything.")

# ---------------------------------------------------------------------------
U.hdr("D0e  THE PUBLISHED REF RESOLVES, AND CARRIES EVERY TRANSCRIPT")

U.pop("the %d TRANSCRIPTS this ticket re-runs, at %s"
      % (len(U.MOVED), U.PUBLISHED_AT), ref=U.PUBLISHED_AT)
got = 0
for p in U.MOVED:
    try:
        n = len(U.read(p, U.PUBLISHED_AT).splitlines())
        got += n > 0
    except Exception:
        n = -1
    print("      %-52s %6d" % (p.split("/", 1)[1], n))
print("      ^ one unit of each is one line of a transcript")
arm("...TRANSCRIPTS readable at the published ref", got, len(U.MOVED))

# ---------------------------------------------------------------------------
U.hdr("D0f  THE ACCOUNTING AGAINST ITSELF -- THE NULL RESULT")

print("  A diff that reports movement between a file and ITSELF is broken in")
print("  the direction that would make this whole ticket look busier than it")
print("  is.  Every transcript is compared with its own published text:")
print()
U.pop("the %d TRANSCRIPTS above, each compared with itself at %s"
      % (len(U.MOVED), U.PUBLISHED_AT), ref=U.PUBLISHED_AT)
selfmoved = sum(1 for p in U.MOVED
                for _k, _o, _n, v in U.diff_rows(p, U.PUBLISHED_AT,
                                                 U.PUBLISHED_AT)
                if v != "SAME")
arm("...FIGURES that move when compared with themselves", selfmoved, 0)
print("      ^ one unit of that number is one count row")

# ---------------------------------------------------------------------------
U.hdr("D0g  NOTHING THIS TICKET PRINTS INTO ANOTHER TREE IS A COUNT ROW")

print("  This ticket adds three kinds of line to two other trees' published")
print("  transcripts: a dated `population:` line, a CLASS line, and an")
print("  OBSERVED interval block.  If any of them parsed as a COUNT ROW it")
print("  would enter the arc's own census -- a ticket about dating the census")
print("  would have changed it, in every tree that measures it, silently.")
print("  So the lines are generated HERE and put to `lib56dc.count_rows`:")
print()
import io                                                   # noqa: E402
import contextlib                                           # noqa: E402
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    U.pop("a population line with a ref on it")
    U.pop("one dated at a UNION of two refs", ref="9f1ecaa+eacc5e1")
    U.class_block([("a FROZEN figure", True, False, "9f1ecaa+eacc5e1"),
                   ("a GROWING figure", False, False, None),
                   ("an OBSERVED figure", False, True, None)])
    U.observed_block(U.TREE + "/")
gen = buf.getvalue()
for ln in gen.splitlines():
    print("      |%s" % ln)
print()
U.pop("the %d LINES this ticket's three printers emit" % len(gen.splitlines()))
arm("...of them `lib56dc.count_rows` returns", len(U.A.count_rows(gen)), 0)
print("      ^ one unit of that number is one printed line")
print()
print("  THE ARM IS NOT `I LOOKED AND THEY SEEMED FINE`.  `_COUNT_ROW` wants")
print("  two spaces, a label, two spaces and DIGITS TO END OF LINE; an interval")
print("  ends in `(OBSERVED)` and a population line ends in a ref.  A future")
print("  edit that put the value last would break that, and this is the arm")
print("  that would say so.")

print()
print("D0 TOTAL BAD: %d" % BAD)
sys.exit(min(BAD, 120))
