#!/usr/bin/env python3
"""z1 -- THE CENSUS.  How much of the estate collapses EMPTY onto 0, and can a
matcher see it?

Sections
  1  the pin, the population, and the funnel
  2  the five classes
  3  COMPLIANCE -- the rule the estate already follows, in two spellings
  4  the guarded class by OPERATION, by whether it is PRINTED, by fallback
  5  the verdict rule, computed -- and what it cannot decide
  6  the hand table for the 23 it cannot decide
  7  THE HEADLINE: collapses whose value reaches a page
  8  the wrong-direction control -- the requirement that carries the census
  9  the family no matcher can judge, and the grep that proved it by failing
 10  the reflexive scan -- this directory measured by its own rule

EXIT 0 GREEN, 2 REFUSED.  This arm never exits 1: it is a census and not a
gate, and nothing here is a property the estate must hold.  It REFUSES -- and
that is exit 2 -- if the pin will not resolve, if the hand table is incomplete,
or if the hand table names a site that is not in the census, because each of
those makes every figure below it a statement about the instrument.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib3c92 as L  # noqa: E402


# --------------------------------------------------------------------------
# THE HAND TABLE.
#
# Section 5's rule decides 70 of the 93 guarded sites from the operation alone.
# It CANNOT decide the other 23, and this is where a hand does it -- separately,
# so that a computed verdict and a judged one are never mixed in one column.
#
# Every entry is `path:line -> (verdict, reason)`.  The arm REFUSES if a site
# here is missing, and REFUSES if an entry here names a site the census did not
# find, because a hand table that has rotted past its subject reports on a
# repository that no longer exists.  Both are impossible at a PIN and both are
# checked anyway: the pin is a line of code and lines of code get edited.
# --------------------------------------------------------------------------
HAND = {
    "code/audit_330a/s1_anchors.py:160": (
        L.COLLAPSE,
        "a non-ancestor has no distance; the next line prints `0 commit(s)`"),
    "code/audit_c067/selftest_c067.py:81": (
        L.COLLAPSE,
        "a file that does not exist has no size, and 0 is a size"),
    "code/branching_af28/core_af28.py:372": (
        L.SOUND,
        "the largest part of the empty partition IS 0"),
    "code/branching_audit_a218/kern_a218.py:499": (
        L.SOUND,
        "the rank of the zero space is 0, by definition and not by choice"),
    "code/compression_audit_8bc7/a1_fibers.py:108": (
        L.SOUND,
        "the guard only avoids 2**-1; the product is 0 at d = 0 either way"),
    "code/counterexample_repair_dea5/controls.py:96": (
        L.SOUND,
        "n = 0 has exactly one poset with one labelling, and 1 is the count"),
    "code/face_geometry_audit_e0ce/audit_rebuild.py:543": (
        L.SOUND,
        "the rank of a matrix with no rows is 0, by definition"),
    "code/face_geometry_audit_e7bc/g3_differs_under.py:111": (
        L.COLLAPSE,
        "the regex did not match; `0 claim(s) scored` is not what that means"),
    "code/face_geometry_instr_5f9a/d2_deletion.py:1399": (
        L.COLLAPSE,
        "no matching row is printed into the message as the row's value 0"),
    "code/face_geometry_landing_7d5a/verify_landing.py:397": (
        L.SOUND,
        "the unified-diff format OMITS a hunk count of 1; 1 is the spec"),
    "code/grain_axis_audit_03d1/a2_blindspot.py:236": (
        L.SOUND,
        "at 0 disagreements the repaired row count is 0 on both readings"),
    "code/image_geometry_c776/c2_no_inequality.py:125": (
        L.COLLAPSE,
        "no argmax poset was found, and `e(P) = 1` is printed for it"),
    "code/landscape_repair_audit_3b51/audit_r3_r4.py:64": (
        L.SOUND,
        "outside M0 the closed form's own value IS 0 -- a definition"),
    "code/lstar_789d/s0_selftest.py:43": (
        L.SOUND,
        "the down-set below the bottom element is empty, i.e. the mask 0"),
    "code/runner_exit_repair_bf79/p1_grain.py:345": (
        L.SOUND,
        "at 0 disagreements the repaired version has 0 blind-spot rows"),
    "code/runner_exit_repair_bf79/p3_ruleset.py:120": (
        L.COLLAPSE,
        "the regex did not match; the figure is absent rather than zero"),
    "code/runner_exit_repair_bf79/p3_ruleset.py:121": (
        L.COLLAPSE,
        "the regex did not match; the figure is absent rather than zero"),
    "code/species_audit_7dd3/kern7dd3.py:93": (
        L.COLLAPSE,
        "no line map means the line number is unknown, and 1 is a line"),
    "code/species_audit_a61f/a1_headline.py:221": (
        L.SOUND,
        "the rank of an empty integer matrix is 0, by definition"),
    "code/species_extent_d633/e1_extents.py:453": (
        L.COLLAPSE,
        "an empty `under` has no first passage to name; 1 is a sentinel"),
    "code/species_extent_d633/trace_open.py:79": (
        L.SOUND,
        "`SystemExit(None)` IS exit 0 -- the language defines it, not the arm"),
    "code/um_frontier_b417/b4_certify.py:78": (
        L.COLLAPSE,
        "a missing lower bound prints as 0.000000 beside genuine ones"),
    "code/unified_gate_8fd1/quotient_symmetry.py:262": (
        L.SOUND,
        "the chain C_0 has exactly one antichain, the empty one"),
}

REFUSED = 0


def refuse(why):
    global REFUSED
    REFUSED = 1
    print()
    print("*** REFUSED: %s" % why)


def main():
    L.head("z1 -- EMPTY IS NOT ZERO: the census",
           "mg-3c92, carrying mg-9b6b's rule for the whole estate")

    # ---------------------------------------------------------------- 1
    L.rule("1.  THE PIN, THE POPULATION, AND THE FUNNEL")
    full, reachable = L.check_pin()
    print("    AS_OF                       %s" % full[:12])
    print("    ancestor of origin/main     %s" % ("yes" if reachable else
                                                  "NO"))
    if not reachable:
        refuse("the pin is not an ancestor of origin/main: every figure below "
               "is about a tree no other reader can reach")
        return 2
    sites, broken, paths = L.census()
    print("    tracked .py under code/     %d" % len(paths))
    print("    parsed                      %d" % (len(paths) - len(broken)))
    print("    would not parse             %s"
          % L.count_or_empty(len(broken), paths))
    for path, err in broken:
        print("        %-60s %s" % (path, err))
    print()
    print("    Unparseable files are COUNTED and named rather than dropped.  A")
    print("    census that reports a number because it never looked is this")
    print("    estate's oldest defect, and it is the same defect this whole")
    print("    directory is about, one layer down.")

    kinds = L.by_kind(sites)
    guarded = kinds[L.GUARDED]

    # ---------------------------------------------------------------- 2
    L.rule("2.  THE FIVE CLASSES")
    print("    %-26s %6s  %s" % ("class", "sites", "what a site proves"))
    print("    %-26s %6d  %s" % (L.GUARDED, len(guarded),
                                 "a NUMBER was chosen for the empty case"))
    print("    %-26s %6d  %s" % (L.PRESERVING, len(kinds[L.PRESERVING]),
                                 "something that is NOT a number was"))
    print("    %-26s %6d  %s" % (L.DEFAULTED, len(kinds[L.DEFAULTED]),
                                 "the same as the first, linter-visible"))
    print("    %-26s %6d  %s" % (L.DEFAULTED_NONE,
                                 len(kinds[L.DEFAULTED_NONE]),
                                 "the same as the second, linter-visible"))
    print("    %-26s %6d  %s" % (L.UNGUARDED, len(kinds[L.UNGUARDED]),
                                 "NOTHING -- see section 9"))
    print()
    print("    ⚠️  ONE-DIRECTIONAL.  A site is a PROOF that a number was chosen")
    print("    for the empty case.  ABSENCE of a site proves nothing at all:")
    print("    the collapse can live in a helper, in a `dict.get(k, 0)`, or in")
    print("    `sum([])`, where there is no fallback in the source to match on.")

    # ---------------------------------------------------------------- 3
    L.rule("3.  COMPLIANCE -- THE RULE THE ESTATE ALREADY FOLLOWS")
    print("    The carry-forward asks for a fallback a reader cannot mistake")
    print("    for a computed answer.  That is decidable: `None` and a string")
    print("    are not numbers.  TWO DISJOINT SPELLINGS ANSWER IT SEPARATELY.")
    print()
    pres, coll = len(kinds[L.PRESERVING]), len(guarded)
    dn, dnum = len(kinds[L.DEFAULTED_NONE]), len(kinds[L.DEFAULTED])
    print("    %-34s %6s %6s %8s" % ("spelling", "keeps", "loses", "keeps %"))
    print("    %-34s %6d %6d %7.1f%%"
          % ("f(X) if X else <fallback>", pres, coll,
             100.0 * pres / (pres + coll)))
    print("    %-34s %6d %6d %7.1f%%"
          % ("max/min/next(..., default=...)", dn, dnum,
             100.0 * dn / (dn + dnum)))
    print()
    print("    of the %d preserving ternaries: %d use `None`, %d a string"
          % (pres, sum(1 for s in kinds[L.PRESERVING] if s.fallback == "None"),
             sum(1 for s in kinds[L.PRESERVING] if s.fallback == "str")))
    print("    of the %d preserving defaults:  %d use `None`, %d a string"
          % (dn,
             sum(1 for s in kinds[L.DEFAULTED_NONE] if s.fallback == "None"),
             sum(1 for s in kinds[L.DEFAULTED_NONE] if s.fallback == "str")))
    print()
    print("    THE TWO NUMBERS AGREE TO ONE PART IN FORTY OVER SPELLINGS THAT")
    print("    SHARE NO SYNTAX AND NO POPULATION, WHICH IS THE FINDING.  The")
    print("    rule mg-9b6b proposes is not a reform: it is a DESCRIPTION of")
    print("    what this estate already does about nine times in ten, arrived")
    print("    at without the rule ever being written down.  A proposal that")
    print("    is already practice is worth proposing for one reason only --")
    print("    to make the one-in-ten visible -- and that is sections 5 to 7.")
    print()
    print("    ⚠️  THE 550 STRING FALLBACKS ARE COUNTED AND ARE NOT A CLAIM OF")
    print("    INTENT.  Most are display defaults (`\" %s\" % x if x else \"\"`)")
    print("    that satisfy the criterion incidentally.  The criterion is")
    print("    about what a READER can recover, not about what an author")
    print("    meant, and it is stated that way everywhere in this directory.")
    print("    The `default=` row carries no such doubt: 89 of its 101 are")
    print("    `None`, on the same call, by the same author, in the same line.")

    # ---------------------------------------------------------------- 4
    L.rule("4.  THE GUARDED CLASS BY OPERATION, BY REACH, BY FALLBACK")
    print("    %-8s %6s %8s %8s" % ("op", "sites", "printed", "zero"))
    for op in (L.DIV, L.MAXMIN, L.SUM, L.LEN, L.OP_OTHER):
        rows = [s for s in guarded if s.op == op]
        print("    %-8s %6d %8d %8d"
              % (op, len(rows), sum(1 for s in rows if s.printed),
                 sum(1 for s in rows if s.zero)))
    print("    %-8s %6d %8d %8d"
          % ("TOTAL", len(guarded), sum(1 for s in guarded if s.printed),
             sum(1 for s in guarded if s.zero)))
    print()
    print("    PRINTED is SYNTACTIC CONTAINMENT in a `print`, a `%`-format, an")
    print("    f-string or a `.write`, and it is a DECLARED UNDER-COUNT: a site")
    print("    assigned to a name on one line and printed on the next is not")
    print("    counted.  `code/audit_330a/s1_anchors.py:160` is exactly that")
    print("    and it is in this census as NOT printed, one line above a")
    print("    `print` that renders it.  The direction is the safe one --")
    print("    PRINTED is a proof, NOT-PRINTED is not.")

    # ---------------------------------------------------------------- 5
    L.rule("5.  THE VERDICT RULE, COMPUTED FROM THE OPERATION ALONE")
    print("    Is the fallback the operation's OWN VALUE on the empty input,")
    print("    or a CHOICE made because the operation has no value there?")
    print()
    print("        sum(∅) = 0   len(∅) = 0        DEFINITIONS   -> SOUND")
    print("        max(∅)  min(∅)  x/0            NO VALUE      -> COLLAPSE")
    print("        anything else                  NOT DECIDABLE -> section 6")
    print()
    print("    ⚠️  COLLAPSE IS NOT AN ACCUSATION.  It says the printed value")
    print("    cannot be inverted by a reader -- EMPTY and 0 arrive as one")
    print("    number.  Whether that matters is a question about the reader,")
    print("    and mg-9b6b is the one case in this estate where it is known to.")
    print()
    computed = {L.SOUND: 0, L.COLLAPSE: 0, L.UNDECIDED: 0}
    for s in guarded:
        computed[s.verdict] += 1
    for v in (L.SOUND, L.COLLAPSE, L.UNDECIDED):
        print("    computed %-10s %4d" % (v, computed[v]))

    # ---------------------------------------------------------------- 6
    L.rule("6.  THE HAND TABLE -- THE 23 THE RULE CANNOT DECIDE")
    undecided = [s for s in guarded if s.verdict == L.UNDECIDED]
    missing = [s.key for s in undecided if s.key not in HAND]
    census_keys = {s.key for s in guarded}
    orphan = sorted(k for k in HAND if k not in census_keys)
    if missing:
        refuse("%d undecided site(s) carry no hand verdict: %s"
               % (len(missing), ", ".join(missing)))
    if orphan:
        refuse("%d hand verdict(s) name a site this census did not find: %s"
               % (len(orphan), ", ".join(orphan)))
    if missing or orphan:
        return 2
    hand_counts = {L.SOUND: 0, L.COLLAPSE: 0}
    for s in undecided:
        verdict, why = HAND[s.key]
        hand_counts[verdict] += 1
        print("    %-9s %s" % (verdict, s.key))
        print("              %s" % why)
        print("              %s" % L.squeeze(s.text, 84))
    print()
    print("    hand  %-9s %4d" % (L.SOUND, hand_counts[L.SOUND]))
    print("    hand  %-9s %4d" % (L.COLLAPSE, hand_counts[L.COLLAPSE]))

    final = {}
    for s in guarded:
        final[s.key] = (HAND[s.key][0] if s.verdict == L.UNDECIDED
                        else s.verdict)
    total_collapse = sum(1 for v in final.values() if v == L.COLLAPSE)
    total_sound = sum(1 for v in final.values() if v == L.SOUND)
    print()
    print("    TOTAL %-9s %4d   (%d computed + %d judged)"
          % (L.COLLAPSE, total_collapse, computed[L.COLLAPSE],
             hand_counts[L.COLLAPSE]))
    print("    TOTAL %-9s %4d   (%d computed + %d judged)"
          % (L.SOUND, total_sound, computed[L.SOUND], hand_counts[L.SOUND]))

    # ---------------------------------------------------------------- 7
    L.rule("7.  THE HEADLINE -- COLLAPSES WHOSE VALUE REACHES A PAGE")
    reaching = sorted((s for s in guarded
                       if final[s.key] == L.COLLAPSE and s.printed),
                      key=lambda s: s.key)
    print("    %d of %d collapses are rendered into text at the site itself."
          % (len(reaching), total_collapse))
    print()
    print("    THIS IS THE FAMILY mg-9b6b's FINDING IS ABOUT.  Each of these")
    print("    prints a number for a question that has no answer, onto a page")
    print("    a later reader takes figures off.  A `0.0%` printed for an EMPTY")
    print("    population is not wrong arithmetic -- it is a reading of the")
    print("    population that the population does not support.")
    print()
    for s in reaching:
        print("    %-6s %s" % (s.op, s.key))
        print("           %s" % L.squeeze(s.text, 86))

    # ---------------------------------------------------------------- 8
    L.rule("8.  WRONG-DIRECTION CONTROL -- IS THE REQUIREMENT LOAD-BEARING?")
    loose, _, _ = L.census(strict=False)
    loose_guarded = [s for s in loose if s.kind == L.GUARDED]
    ratio = len(loose_guarded) / float(len(guarded)) if guarded else None
    print("    strict (guard named in the true branch)    %4d" % len(guarded))
    print("    loose  (requirement dropped)               %4d"
          % len(loose_guarded))
    print("    ratio                                      %s"
          % ("%.1fx" % ratio if ratio is not None else "EMPTY"))
    print()
    print("    Without the requirement, every `sys.exit(1 if bad else 0)` and")
    print("    every matrix indicator `(deg[i] if i == j else 0)` joins the")
    print("    class.  A requirement whose removal changed nothing would be")
    print("    decoration and this census would be a grep wearing an AST.")

    # ---------------------------------------------------------------- 9
    L.rule("9.  THE FAMILY NO MATCHER CAN JUDGE")
    unguarded = kinds[L.UNGUARDED]
    print("    sum(<comprehension with an `if`>)          %4d sites"
          % len(unguarded))
    print("    ... of which rendered into text            %4d"
          % sum(1 for s in unguarded if s.printed))
    print()
    print("    `sum([]) == 0` IS THE LANGUAGE'S COLLAPSE AND NOT THE AUTHOR'S.")
    print("    There is no fallback in the source, no guard to find, and the")
    print("    printed 0 is byte-identical whether the selection was empty or")
    print("    genuinely summed to nothing.  NONE OF THESE %d IS A DEFECT AND"
          % len(unguarded))
    print("    THIS ARM DOES NOT SAY THEY ARE.  They are the measurement of")
    print("    what a matcher cannot reach: a rule enforced by looking would")
    print("    be silent on a class %.0fx the size of the one it can see."
          % (len(unguarded) / float(len(guarded))))
    print()
    print("    THE LINTER'S OWN SPELLING, AND THE GREP THAT MISSED IT")
    print("    %-42s %4d sites" % ("max/min/next with a numeric fallback",
                                   len(kinds[L.DEFAULTED])))
    for s in kinds[L.DEFAULTED]:
        print("        %-58s %s" % (s.key, L.squeeze(s.text, 40)))
    print()
    print("    PREDICTIONS.md §0.1 SAID THIS CLASS WAS EMPTY.  IT IS NOT, AND")
    print("    THE MECHANISM IS THIS DIRECTORY'S OWN SUBJECT ARRIVING IN ITS")
    print("    OWN PRE-REGISTRATION.  The scoping probe was")
    print()
    print("        git grep -E '\\b(max|min)\\([^)]*default=' -- 'code/**.py'")
    print()
    print("    and it fails TWICE, independently, in the same direction:")
    print()
    print("      (a) `\\b` IS NOT A WORD BOUNDARY IN git grep's POSIX ERE.  It")
    print("          matches nothing and does not complain -- `git grep -c -E")
    print("          '\\bmax\\(' code/search_reach_abe8/s4_reach.py` returns no")
    print("          lines where `max\\(` returns 3.  THIS is what made the")
    print("          probe return the literal 0.")
    print("      (b) `[^)]*` cannot cross the `)` in `max((len(l) for l in")
    print("          lines), default=0)`, which is how 12 of the 16 are")
    print("          written.  Repairing (a) alone gives 3 of 16 -- a number")
    print("          small enough to be believed and wrong by a factor of 5.")
    print()
    print("    So (a) produced the zero and (b) would have kept the count")
    print("    wrong after it was fixed.  P1 IS REFUTED, and it is refuted by")
    print("    exactly the confusion the ticket is about: a tool returned")
    print("    NOTHING AT ALL, `nothing at all` was read as `0 sites exist`,")
    print("    and the pre-registration published it as a measured fact.")
    print("    That is mg-9b6b's sentence about `G` with the nouns changed.")

    # --------------------------------------------------------------- 10
    L.rule("10. THE REFLEXIVE SCAN -- THIS DIRECTORY BY ITS OWN RULE")
    print("    ⚠️  READ FROM THE WORKTREE AND NOT FROM THE PIN, AND THAT IS AN")
    print("    EXEMPTION BY ARITHMETIC RATHER THAN BY RULE: this directory is")
    print("    younger than %s and is in no tree the pin can name.  It is the"
          % full[:12])
    print("    one figure on this page that is not a function of one commit.")
    print()
    mine = sorted(f for f in os.listdir(L.HERE) if f.endswith(".py"))
    own, own_broken = [], []
    for name in mine:
        with open(os.path.join(L.HERE, name)) as fh:
            got, err = L.classify("code/empty_vs_zero_3c92/" + name, fh.read())
        if err:
            own_broken.append((name, err))
        own.extend(got)
    own_guarded = [s for s in own if s.kind == L.GUARDED]
    print("    files scanned                              %4d" % len(mine))
    print("    %-42s %4s" % (L.GUARDED,
                             L.count_or_empty(len(own_guarded), mine)))
    print("    %-42s %4s"
          % (L.DEFAULTED,
             L.count_or_empty(sum(1 for s in own if s.kind == L.DEFAULTED),
                              mine)))
    print("    %-42s %4s"
          % (L.PRESERVING,
             L.count_or_empty(sum(1 for s in own if s.kind == L.PRESERVING),
                              mine)))
    print("    %-42s %4s"
          % (L.UNGUARDED,
             L.count_or_empty(sum(1 for s in own if s.kind == L.UNGUARDED),
                              mine)))
    for s in own_guarded:
        print("        %s | %s" % (s.key, L.squeeze(s.text, 70)))
    print()
    print("    `0` HERE MEANS I LOOKED AND THERE WERE NONE.  `EMPTY` would")
    print("    mean there was nothing to look at.  They are printed by one")
    print("    function (`lib3c92.count_or_empty`) so that no arm in this")
    print("    directory can print one for the other by accident -- which is")
    print("    the rule this directory is about, applied to itself.")

    print()
    print("=" * 78)
    print("z1: %s"
          % ("REFUSED" if REFUSED else
             "GREEN -- %d collapses, %d of them reaching a page, over %d files"
             % (total_collapse, len(reaching), len(paths))))
    return 2 if REFUSED else 0


if __name__ == "__main__":
    sys.exit(main())
