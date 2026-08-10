"""mg-724a — HOW THIS GATE CAN FAIL.  Imported by gate.py and run on every gated merge.

WHY THIS IS A MODULE AND NOT A SECOND PRODUCER.  Every other suite in this arc ships its
negative control as a separate script with its own committed transcript, and this one does
not.  The reason is a coupling those suites do not have: this gate's subject is THE BYTES
THE SAME RUN JUST CAPTURED from the two suites.  A separate producer would have to read them
off disk, and a transcript on disk is either re-produced (doubling the gate's cost on the
merge critical path, for the same measurement) or read from a previous run — and a control
scoring last run's transcript while reporting on this one is a failure with no symptom.
mg-f8e5 spent a ticket on the version of that mistake where the file was empty.

WHY IT IS RUN ON EVERY MERGE RATHER THAN ONCE AT AUTHORING TIME.  Because the thing this
whole line of work is about is controls that are not asked.  A falsification proof that ran
in August and is cited in December is a claim about August.  It costs ~0.1 s here — measured,
in the gate's own §4/§5 output — because none of these probes re-runs the suites.

THE RULE EVERY PROBE OBEYS, ADOPTED FROM mg-9876 RATHER THAN PARAPHRASED.  Before a mutation
may be credited with being CAUGHT, the UNMUTATED report must not already say what the
mutation expects.  A predicate satisfied by the good input cannot fail, and crediting it is
how `"8 9" in out` satisfied a positive control about a drift worklist for its entire life.

AND EVERY MUTATION IS DERIVED FROM THE CAPTURED BYTES, NEVER TYPED.  `worklist + " 99"`, not
`"8" -> "7 8"`; `N + 1`, not `1 -> 2`.  mg-2f44 lost two fixtures to values typed against a
subject that then moved; mg-9876 lost two planted worlds to borrowing them from the subject
it was repairing.  A mutation that no longer mutates anything looks exactly like one that was
caught, so a transform that changes nothing is SETUP FAILED and is red.
"""

import copy
import os
import re

import lib724a as L


# ---------------------------------------------------------------------------------------
# transforms
# ---------------------------------------------------------------------------------------

# THESE TWO REPLACE THE CAPTURED SPAN, NOT A SUBSTRING OF THE MATCH (mg-188d).
#
# They used to end `m.group(0).replace(m.group("v"), new, 1)` — a SUBSTRING REPLACE, which is
# this file's own smell #1, in the file whose header is about `"8 9" in out` satisfying a
# positive control for its entire life.  It replaced the first occurrence of the group's TEXT
# anywhere in the match, not the group.  `audit.arms_not_shown` reads `\d+ not;` out of
#
#     VERDICT: 50 arms probed, 50 shown to discriminate, 0 not; 0 demonstrated holes ...
#
# so T6's flip of `0` -> `1` landed on the `0` inside `50`, mutated audit.arms_PROBED, and left
# the field the probe is named for untouched: T6 scored HOLE.  IT WAS INVISIBLE UNTIL mg-188d
# MOVED THE VALUES.  At mg-724a's own baseline the group was `1` and the match carried no other
# `1` before it, so the wrong rule and the right rule agreed, on that day, on those numbers.
# The bug was never in the probe that failed — a probe that mutates a DIFFERENT field than the
# one it scores is a probe about nothing, and nothing said so for as long as the arithmetic
# happened to line up.
def _sub_group(text, pattern, new):
    m = re.search(pattern, text, re.M)
    if not m:
        return text
    s, e = m.span("v")
    return text[:s] + new + text[e:]


def _bump_int(text, pattern, delta=1):
    m = re.search(pattern, text, re.M)
    if not m:
        return text
    return _sub_group(text, pattern, str(int(m.group("v")) + delta))


def _set_str(text, pattern, new):
    return _sub_group(text, pattern, new)


WORKLIST_PAT = r"^The worklist, READ OUT OF SECTION 2 rather than typed here: (?P<v>.*)$"
CONTROL_EXIT_PAT = r"^control exit\s+:\s+(?P<v>\d+)\s"
VERDICT_PAT = r"^control verdict: VERDICT: (?P<v>[A-Z ]+?) —"
CAUGHT_PAT = r"^(?P<v>\d+) of \d+ caught; \d+ hole\(s\)\.$"
UNFALS_PAT = r"^(?P<v>\d+) row\(s\) UNFALSIFIABLE"
NOTSHOWN_PAT = r"^VERDICT: \d+ arms probed, \d+ shown to discriminate, (?P<v>\d+) not;"
ARMS_PAT = r"^CENSUS (?:COMPLETE|INCOMPLETE) — (?P<v>\d+) arms,"
SELFTEST_PAT = r"^(?P<v>\d+) of \d+ planted worlds scored as required\.$"
FINDINGS_PAT = r"^producers with findings\s+:\s+(?P<v>\d+)$"
SWEEP_MEM_PAT = r"^SWEEP (?:OK|BROKEN) — (?P<v>\d+) membership candidates"
A2_VERDICT_LINE = r"^VERDICT: \d+ arms probed, .*$"


def _grow_worklist(text):
    m = re.search(WORKLIST_PAT, text, re.M)
    if not m:
        return text
    return _set_str(text, WORKLIST_PAT, m.group("v") + " 99")


def _flip_verdict(text):
    m = re.search(VERDICT_PAT, text, re.M)
    if not m:
        return text
    return _set_str(text, VERDICT_PAT, "CLEAN" if m.group("v") != "CLEAN" else "DRIFT")


def _zero_or_one(text, pattern):
    m = re.search(pattern, text, re.M)
    if not m:
        return text
    return _set_str(text, pattern, "0" if m.group("v") != "0" else "1")


def _drop_line(text, pattern):
    return re.sub(pattern + r"\n?", "", text, count=1, flags=re.M)


def _duplicate_line(text, pattern):
    m = re.search(pattern, text, re.M)
    if not m:
        return text
    return text[:m.end()] + "\n" + m.group(0) + text[m.end():]


# (id, what it plants, suite, transform, (expectation-kind, target))
#   ("diverged", field)  the field's row must read DIVERGED and must be gated
#   ("recorded", field)  the field must MOVE and must gate NOTHING — a declared blind spot
#   ("refuse", field)    extract/compare must REFUSE, and the refusal must name that field
TEXT_MUTATIONS = [
    ("T1", "the twin's drift worklist gains a row (a published ledger row moved)",
     "twin", _grow_worklist, ("diverged", "twin.worklist")),
    ("T2", "the twin control's exit code changes",
     "twin", lambda t: _bump_int(t, CONTROL_EXIT_PAT), ("diverged", "twin.control_exit")),
    ("T3", "the twin control's VERDICT grade flips",
     "twin", _flip_verdict, ("diverged", "twin.verdict_grade")),
    ("T4", "the twin's negative control catches one fewer mutation",
     "twin", lambda t: _bump_int(t, CAUGHT_PAT, -1), ("diverged", "twin.mutations_caught")),
    ("T5", "a row of the twin's negative control becomes UNFALSIFIABLE",
     "twin", lambda t: _bump_int(t, UNFALS_PAT), ("diverged", "twin.unfalsifiable_rows")),
    # THE LABEL NO LONGER NAMES A DIRECTION (mg-188d).  It read "(1 not -> 0 not)", which was
    # the flip that existed on mg-724a's day; `_zero_or_one` has always flipped whichever way
    # the observed value points, and after C3's repair the live direction is 0 -> 1.  A probe
    # description that hardcodes a value the probe itself derives is the same expiry-dated
    # fixture as E2 below, one severity down: wrong prose rather than a dead check.
    ("T6", "the audit's non-discriminating-arm count moves in either direction",
     "audit", lambda t: _zero_or_one(t, NOTSHOWN_PAT), ("diverged", "audit.arms_not_shown")),
    ("T7", "the audited directory grows an arm the census did not have",
     "audit", lambda t: _bump_int(t, ARMS_PAT), ("diverged", "audit.arms")),
    ("T8", "the auditor's selftest stops returning the known answer in one planted world",
     "audit", lambda t: _bump_int(t, SELFTEST_PAT, -1), ("diverged", "audit.selftest_scored")),
    ("T9", "the audit runner reports NO producer with findings (the laundered-green direction)",
     "audit", lambda t: _zero_or_one(t, FINDINGS_PAT), ("diverged", "audit.producers_with_findings")),
    ("T10", "the corpus-wide smell counts move (RECORDED, not gated — the declared blind spot)",
     "audit", lambda t: _bump_int(t, SWEEP_MEM_PAT, 100),
     ("recorded", "audit.sweep_membership_candidates")),
    ("T11", "the twin runner never prints its worklist line (it died before deciding)",
     "twin", lambda t: _drop_line(t, WORKLIST_PAT), ("refuse", "twin.worklist")),
    ("T12", "the audit's VERDICT line appears twice and the two readings could disagree",
     "audit", lambda t: _duplicate_line(t, A2_VERDICT_LINE), ("refuse", "audit.arms_probed")),
]

# Mutations of the captured EXIT STATUS rather than of the transcript.  Both runners map some
# non-zero instrument exits onto a zero runner exit deliberately, so the status is a field to
# be read like any other and not a classifier to be trusted.
# THE PLANTED STATUS IS DERIVED FROM THE OBSERVED ONE, NOT TYPED (mg-188d).
#
# E2 read `("audit", 0)` — plant exit 0 — with its description saying "where the baseline says
# 1".  Both halves were a bet on the audit suite staying RED, and it stayed red for exactly as
# long as arm C3 stayed UNFALSIFIABLE.  mg-188d repaired C3, the audit runner started exiting 0,
# and E2 came back SETUP FAILED: `the planted exit status equals the real one`.  A fixture that
# spells out the value it expects to find is a check with an expiry date — this file's OWN rule,
# stated at the top of it about drifted rows and pinned commits, and not applied to the two
# lines below.  `_other_exit` returns something the runner did not return, whatever it returned.
def _other_exit(observed):
    return 0 if observed else 1


EXIT_MUTATIONS = [
    ("E1", "the twin runner's own exit status changes", "twin", _other_exit,
     ("diverged", "twin.runner_exit")),
    ("E2", "the audit runner's own exit status changes", "audit", _other_exit,
     ("diverged", "audit.runner_exit")),
]


def _rows_by_field(transcripts, exits, baseline):
    observed = L.extract(transcripts, exits)
    rows, gated = L.compare(observed, baseline)
    return {r["field"]: r for r in rows}, gated


def _score(mid, what, transcripts, exits, baseline, base_rows, base_gated, kind, target):
    if kind == "refuse":
        try:
            _rows_by_field(transcripts, exits, baseline)
        except L.Refusal as exc:
            if target in str(exc):
                return (mid, what, "CAUGHT", "REFUSED, naming %s" % target)
            return (mid, what, "HOLE",
                    "refused, but the refusal does not name %s: %s" % (target, str(exc)[:110]))
        return (mid, what, "HOLE", "the gate reached a verdict on a transcript it cannot read")

    # The good side FIRST.  If the field is already not MATCH on the unmutated input, this
    # probe cannot fail on this run and must not be credited with catching anything.
    base_status = base_rows[target]["status"]
    if kind == "diverged" and base_status != "MATCH":
        if target in base_gated:
            return (mid, what, "UNFALSIFIABLE (explained)",
                    "this field is LIVE-DIVERGED on the unmutated input, so the probe cannot "
                    "fail on this run; that divergence is itself the gate's finding")
        return (mid, what, "UNFALSIFIABLE",
                "the unmutated report already reads %s for %s" % (base_status, target))

    try:
        rows, gated = _rows_by_field(transcripts, exits, baseline)
    except L.Refusal as exc:
        return (mid, what, "HOLE",
                "the gate REFUSED where it should have reported: %s" % str(exc)[:110])

    got = rows[target]["status"]
    if kind == "diverged":
        if got == "DIVERGED" and target in gated:
            return (mid, what, "CAUGHT", "%s reads DIVERGED and is gated" % target)
        return (mid, what, "HOLE",
                "%s reads %r after the mutation; expected DIVERGED" % (target, got))

    if got.startswith("MOVED") and set(gated) == set(base_gated):
        return (mid, what, "CAUGHT (silent, as declared)",
                "%s moved and the gate stayed at %d gated divergence(s) — the blind spot "
                "BASELINE.json declares, shown rather than asserted" % (target, len(base_gated)))
    return (mid, what, "HOLE",
            "%s reads %r and gated divergences went %s -> %s; a RECORDED field must move "
            "visibly and gate nothing" % (target, got, sorted(base_gated), sorted(gated)))


def run_mutations(transcripts, exits, baseline, base_rows, base_gated):
    """§4 — the two-sided control against the bytes THIS run captured."""
    results = []
    for mid, what, suite, transform, (kind, target) in TEXT_MUTATIONS:
        muts = dict(transcripts)
        before = muts[suite]
        muts[suite] = transform(before)
        if muts[suite] == before:
            results.append((mid, what, "SETUP FAILED",
                            "the transform changed nothing, so this world is not bad and "
                            "CAUGHT would mean nothing"))
            continue
        results.append(_score(mid, what, muts, exits, baseline, base_rows, base_gated,
                              kind, target))

    for mid, what, suite, plant, (kind, target) in EXIT_MUTATIONS:
        mex = dict(exits)
        newcode = plant(mex[suite]) if callable(plant) else plant
        if mex[suite] == newcode:
            results.append((mid, what, "SETUP FAILED",
                            "the planted exit status equals the real one"))
            continue
        mex[suite] = newcode
        results.append(_score(mid, what, transcripts, mex, baseline, base_rows, base_gated,
                              kind, target))
    return results


# ---------------------------------------------------------------------------------------
# §5 — SYNTHETIC WORLDS: can this gate REFUSE?
# ---------------------------------------------------------------------------------------
#
# Entirely self-contained.  mg-9876's own selftest borrowed two of its planted worlds FROM
# THE SUBJECT UNDER AUDIT and its repairs then destroyed them — a selftest that stops working
# when the audit succeeds.  Nothing below reads a file outside this module except the one
# world that asserts a named file's ABSENCE.

def run_synthetic_worlds(baseline, observed):
    worlds = []

    def w(wid, what, fn, marker):
        try:
            fn()
        except L.Refusal as exc:
            worlds.append((wid, what, "CAUGHT" if marker in str(exc) else "HOLE",
                           str(exc).splitlines()[0][:104]))
            return
        worlds.append((wid, what, "HOLE", "no refusal — this world was accepted"))

    w("S1", "BASELINE.json does not exist",
      lambda: L.load_baseline(path=os.path.join(L.HERE, "BASELINE.json.no-such-file")),
      "is missing")
    w("S2", "the baseline declares a schema this gate cannot read",
      lambda: L.load_baseline(raw={"schema": 99, "fields": {}}), "schema")
    w("S3", "a baseline field carries no `why`",
      lambda: L.load_baseline(raw={"schema": 1, "fields": {"x": {"class": "gated", "value": 1}}}),
      "no `why`")
    w("S4", "a baseline field is neither gated nor recorded",
      lambda: L.load_baseline(raw={"schema": 1, "fields": {
          "x": {"class": "informational", "value": 1, "why": "w"}}}), "class")
    w("S5", "the baseline carries no `fields` object at all",
      lambda: L.load_baseline(raw={"schema": 1}), "`fields`")

    short = copy.deepcopy(baseline)
    dropped = sorted(short["fields"])[0]
    del short["fields"][dropped]
    w("S6", "the extractor produces a field the baseline never declared (%s)" % dropped,
      lambda: L.compare(observed, short), dropped)

    wide = copy.deepcopy(baseline)
    wide["fields"]["audit.a_field_nothing_measures"] = {
        "class": "gated", "value": 0, "why": "planted"}
    w("S7", "the baseline declares an expectation the extractor can no longer produce",
      lambda: L.compare(observed, wide), "a_field_nothing_measures")

    w("S8", "a suite this gate is wired to has been deleted",
      lambda: L.run_suite("code/control_gate_724a/no_such_runner.sh"), "does not exist")
    return worlds
