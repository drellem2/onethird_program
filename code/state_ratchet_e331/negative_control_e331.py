"""mg-e331 — HOW THIS RATCHET CAN FAIL.  Imported by ratchet.py and run on every gated merge.

WHY ON EVERY MERGE AND NOT ONCE AT AUTHORING TIME.  Because the thing this ticket is about is
a fix that was demonstrated once and then never asked again.  A falsification proof run in
August and cited in December is a claim about August.  These probes cost milliseconds — none
of them re-reads STATE.md or shells out — and they are what stands between this ratchet and
being the decorative check the ticket exists to complain about.

THE RULE EVERY PROBE OBEYS, ADOPTED FROM mg-9876 VIA mg-724a RATHER THAN PARAPHRASED.  Before
a mutation may be credited CAUGHT, the UNMUTATED input must not already produce the verdict
the mutation expects.  A predicate satisfied by the good input cannot fail, and crediting it
is how `"8 9" in out` satisfied a positive control for its entire life.  Here the trap is
sharp and specific: if STATE.md were ALREADY over its ceiling, the probe that plants extra
words would expect ABOVE and get ABOVE for reasons that have nothing to do with the mutation.
It would report CAUGHT on the day the ratchet stopped working.

AND EVERY MUTATION IS DERIVED FROM THE OBSERVED VALUES, NEVER TYPED.  `observed + 1`, not
`18970`.  mg-2f44 lost two fixtures to values typed against a subject that then moved.  A
transform that changes nothing is SETUP FAILED, and SETUP FAILED is red — it is not a pass.
"""

import json

import lib_e331 as L

CAUGHT, HOLE, UNFALS, SETUP = "CAUGHT", "HOLE", "UNFALSIFIABLE", "SETUP FAILED"

# D3, MY OWN, CAUGHT BY MY OWN FIRST RUN AND KEPT.  N5 and N6 check that the boundary values
# are GREEN — and the real input is GREEN, so by the rule stated three paragraphs up they are
# predicates ALREADY SATISFIED BY THE GOOD INPUT and were credited CAUGHT anyway.  Fourteen of
# fourteen, printed by the module whose docstring adopts the rule forbidding exactly that.
# They are not deleted, because the boundary is worth checking: an off-by-one in `>` vs `>=`
# is the likeliest defect this rule will ever have.  They are scored BOUNDARY — checked as a
# TRANSITION (green at the value, red one step past it), reported in full, and counted as
# neither caught nor a hole.  A control that can only be green is not a control, and calling
# it one is how a suite reports 50 arms and discriminates on 48.
BOUNDARY = "BOUNDARY"

# D4, MY OWN, AND IT IS THE WORST DEFECT IN THIS TICKET.  Found by the positive control on its
# first run, which is the only thing that could have found it.
#
# The rule three paragraphs up says a probe whose expectation the good input already satisfies
# is UNFALSIFIABLE, and ratchet.py treated any UNFALSIFIABLE as BROKEN.  Both halves are
# right on their own and together they made this ratchet STRUCTURALLY INCAPABLE OF REPORTING
# THE FINDING IT EXISTS TO REPORT: the moment STATE.md goes over the ceiling, N1 and N2 —
# which expect ABOVE-CEILING — are satisfied by the real input, go UNFALSIFIABLE, and the
# verdict becomes BROKEN (exit 2) instead of RED (exit 1).  Every one of the 20 counterfactual
# landings came back REFUSED; X1 came back BROKEN; the whole `WHAT TO DO` remedy text, which
# is the entire user-facing value of this instrument, could never print.
#
# It was not fail-OPEN — a merge still fails on exit 2 — and that is exactly why it would have
# survived: the gate goes red, the branch does not land, and the message tells the author the
# ratchet is broken rather than that their file grew.  A control that blocks correctly while
# diagnosing wrongly is how an author learns to route around it.
#
# THE FIX IS NOT TO STOP CHECKING.  An UNFALSIFIABLE probe is a hole when nothing explains it
# and a FACT ABOUT THE SUBJECT when the subject's own verdict is the explanation.  So the two
# are now distinct, and the distinction is guarded in the direction that matters: if the
# subject is GREEN, NOTHING can explain a falsification probe being unfalsifiable, and
# ratchet.py is still BROKEN.  Explained-away-ness that only ever runs in one direction is
# laundering; this one cannot fire on a green tree.
UNFALS_EXPLAINED = "UNFALS (explained)"


def _verdict_probe(mid, what, words, ceiling, expect, unmutated):
    """Score one (words, ceiling) world.  `unmutated` is the verdict the REAL input produces;
    a probe whose expectation is already met by it is UNFALSIFIABLE, never CAUGHT."""
    if unmutated == expect:
        return (mid, what, UNFALS_EXPLAINED,
                "the subject itself reads %s — this probe's expectation IS the finding" % expect)
    try:
        got, detail = L.verdict(words, ceiling)
    except L.Refusal as exc:
        return (mid, what, HOLE, "refused where %s was required: %s" % (expect, exc))
    if got == expect:
        return (mid, what, CAUGHT, detail)
    return (mid, what, HOLE, "got %s, required %s (%s)" % (got, expect, detail))


def _refusal_probe(mid, what, fn, unmutated_ok):
    """Score a world that must REFUSE.  `unmutated_ok` records that the real ceiling parses;
    if it did not, a refusal here would be evidence about nothing."""
    if not unmutated_ok:
        return (mid, what, UNFALS,
                "the real CEILING.json does not parse either, so refusing proves nothing")
    try:
        fn()
    except L.Refusal as exc:
        first = str(exc).split("\n")[0]
        return (mid, what, CAUGHT, first[:64])
    except Exception as exc:            # noqa: BLE001 — an uncaught type IS the finding
        return (mid, what, HOLE,
                "raised %s instead of Refusal: %s" % (type(exc).__name__, exc))
    return (mid, what, HOLE, "accepted a world it must refuse")


def run(observed_words, ceiling, ceiling_raw):
    """Every probe, against the values THIS run observed."""
    out = []
    try:
        unmutated, _ = L.verdict(observed_words, ceiling)
        parses = True
    except L.Refusal:
        unmutated, parses = None, False

    cap = ceiling["words_ceiling"]
    floor = ceiling["tighten_below"]

    # ---- the two directions the rule must answer -----------------------------------------
    # D5, MY OWN, FOUND BY THE POSITIVE CONTROL ALONGSIDE D4 AND KEPT.  N2 was `observed * 2`
    # and N4 was mg-ea0e's landed 4,658 typed in as a literal.  Both are fine against THIS
    # tree and both break against a tree the positive control actually plants: doubling 4,658
    # gives 9,316, which is still under the ceiling, so N2 expected ABOVE and got SLACK — a
    # HOLE reported against a probe that was merely badly derived.  And N4's literal EQUALS
    # the observed count on the mg-ea0e landing itself, so its mutation was the identity and
    # N13 correctly called SETUP FAILED.  A mutation must be derived so that it lands where it
    # is aimed FOR EVERY SUBJECT, not for the one in front of me — mg-2f44 lost two fixtures
    # to exactly the second of these.  Both are now derived from the ceiling.
    out.append(_verdict_probe(
        "N1", "one word past the ceiling", cap + 1, ceiling, L.ABOVE, unmutated))
    out.append(_verdict_probe(
        "N2", "the ceiling plus another whole file", cap + max(observed_words, 1), ceiling,
        L.ABOVE, unmutated))
    out.append(_verdict_probe(
        "N3", "one word under the tighten point", floor - 1, ceiling, L.SLACK, unmutated))
    out.append(_verdict_probe(
        "N4", "half the tighten point", floor // 2, ceiling, L.SLACK, unmutated))

    # ---- the boundaries, where an off-by-one lives ----------------------------------------
    # Scored BOUNDARY, not CAUGHT — see the note beside the constant.  Each is a TRANSITION:
    # green AT the value and red ONE STEP past it.  Checking only the green half would be a
    # predicate the good input already satisfies; checking only the red half would not locate
    # the edge.  A HOLE here is an off-by-one in `>` / `<`, which is the defect this rule is
    # most likely to acquire and the one a reader is least likely to see.
    for mid, what, inside, outside, beyond in (
            ("N5", "the ceiling edge is exactly where declared", cap, cap + 1, L.ABOVE),
            ("N6", "the tighten edge is exactly where declared", floor, floor - 1, L.SLACK)):
        try:
            g_in, detail = L.verdict(inside, ceiling)
            g_out, _ = L.verdict(outside, ceiling)
        except L.Refusal as exc:
            out.append((mid, what, HOLE, "refused at a boundary: %s" % exc))
            continue
        if g_in == L.GREEN and g_out == beyond:
            out.append((mid, what, BOUNDARY,
                        "%d -> GREEN, %d -> %s" % (inside, outside, beyond)))
        else:
            out.append((mid, what, HOLE,
                        "edge is not where declared: %d -> %s, %d -> %s"
                        % (inside, g_in, outside, g_out)))

    # ---- worlds the rule must REFUSE rather than answer ------------------------------------
    def _blank_why():
        c = json.loads(ceiling_raw)
        c["why"] = "   "
        L.parse_ceiling(json.dumps(c), "<probe N7>")

    def _drop_field():
        c = json.loads(ceiling_raw)
        c.pop("words_ceiling")
        L.parse_ceiling(json.dumps(c), "<probe N8>")

    def _not_json():
        L.parse_ceiling(ceiling_raw + "\ntrailing garbage\n", "<probe N9>")

    def _inverted():
        c = json.loads(ceiling_raw)
        c["tighten_below"] = c["words_ceiling"] + 1
        L.parse_ceiling(json.dumps(c), "<probe N10>")

    def _string_ceiling():
        c = json.loads(ceiling_raw)
        c["words_ceiling"] = str(c["words_ceiling"])
        L.parse_ceiling(json.dumps(c), "<probe N11>")

    def _negative_words():
        L.verdict(-1, ceiling)

    out.append(_refusal_probe("N7", "a ceiling with an empty `why`", _blank_why, parses))
    out.append(_refusal_probe("N8", "a ceiling missing words_ceiling", _drop_field, parses))
    out.append(_refusal_probe("N9", "a CEILING.json that is not JSON", _not_json, parses))
    out.append(_refusal_probe("N10", "tighten_below above the ceiling", _inverted, parses))
    out.append(_refusal_probe("N11", "a ceiling declared as a string", _string_ceiling, parses))
    out.append(_refusal_probe("N12", "a negative word count", _negative_words, parses))

    # ---- the probe that watches the probes -------------------------------------------------
    # mg-724a: a transform that no longer transforms anything looks exactly like one that was
    # caught.  N13 asserts that the mutations above ACTUALLY DIFFER from the real input, so a
    # future edit that makes cap+1 equal to observed_words is red rather than silent.
    same = []
    if cap + 1 == observed_words:
        same.append("N1's cap+1 equals the observed word count")
    if cap + max(observed_words, 1) == observed_words:
        same.append("N2's plant equals the observed word count")
    if floor - 1 == observed_words:
        same.append("N3's floor-1 equals the observed word count")
    if floor // 2 == observed_words:
        same.append("N4's plant equals the observed word count")
    if json.loads(ceiling_raw) != ceiling:
        same.append("the parsed ceiling is not the declared one")
    out.append(("N13", "every mutation above actually mutates",
                CAUGHT if not same else SETUP,
                "; ".join(same) if same else "4 of 4 planted values differ from the observed"))

    # ---- and the probe that watches the SUBJECT --------------------------------------------
    # A ratchet whose subject stopped existing must not read as green.  This is the one probe
    # that touches the filesystem, and it touches a path that is guaranteed absent.
    def _absent():
        real, L.STATE = L.STATE, L.STATE + ".absent-by-construction-mg-e331"
        try:
            L.read_state()
        finally:
            L.STATE = real

    out.append(_refusal_probe("N14", "STATE.md absent from the tree", _absent, parses))
    return out


def summarise(probes):
    """CAUGHT · HOLE/SETUP · UNFALSIFIABLE · UNFALS (explained) · BOUNDARY — five buckets and
    they do not overlap.  Neither BOUNDARY nor UNFALS (explained) is added to CAUGHT: a probe
    that cannot fail is not evidence that the instrument can, and folding the two together is
    how a suite comes to report a discriminating-arm count larger than the number of arms
    that discriminate."""
    caught = sum(1 for p in probes if p[2] == CAUGHT)
    holes = sum(1 for p in probes if p[2] in (HOLE, SETUP))
    unfals = sum(1 for p in probes if p[2] == UNFALS)
    expl = sum(1 for p in probes if p[2] == UNFALS_EXPLAINED)
    bounds = sum(1 for p in probes if p[2] == BOUNDARY)
    return caught, holes, unfals, expl, bounds
