"""mg-724a — the shared parts of the merge gate: extraction, comparison, mutation.

WHY A LIBRARY AND NOT ONE SCRIPT.  gate.py runs the two suites once and then asks four
different questions of the same captured bytes (does it match the baseline; can the
comparison go red; can it REFUSE; does a declared blind spot stay silent).  Those questions
share one extractor, and a second copy of the extractor that agrees today is worse than one
— mg-f8e5's disposal imported mg-1abe's census for exactly this reason rather than
paraphrasing it.

THE ONE RULE THIS FILE EXISTS TO ENFORCE.  A field is read by an ANCHORED pattern that must
match the transcript EXACTLY ONCE.  Zero matches and two matches are both REFUSALS, never a
default and never a "close enough".  The alternative — `"some string" in output` — is smell
#1 in mg-9876's sweep, which counts 206 live instances of it across `code/`, and it is how
`"8 9" in out` satisfied a positive control about a drift worklist for its whole life
(mg-2f44, generalised by mg-9876).  A membership test cannot tell a string the run PRODUCED
from a string the report prints unconditionally.  Exactly-once matching can.
"""

import json
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

# THE TWO SUITES THIS GATE WIRES.  mg-724a's scope is the two directories mg-9876 audited
# and NOTHING ELSE.  c9876's population index says the estate is far wider (202 whole-output
# membership tests in 66 directories, 24 directories with no falsification evidence at all);
# wiring all of it in one step is how a gate acquires a failure nobody can attribute and gets
# switched off.  Prove the mechanism on the audited two, then widen.
SUITES = (
    ("twin", "code/rendered_twin_pin_9bc2/run_all.sh"),
    ("audit", "code/control_audit_9876/run_all.sh"),
)

BASELINE_PATH = os.path.join(HERE, "BASELINE.json")


class Refusal(Exception):
    """The gate could not reach a verdict.  NOT a finding, and never reported as green."""


# ---------------------------------------------------------------------------------------
# FIELD REGISTRY
# ---------------------------------------------------------------------------------------
#
# Each row: field name -> (suite, anchored pattern, group names, caster).
#
# The pattern is matched with re.MULTILINE against the suite runner's WHOLE stdout+stderr,
# and `extract` requires exactly one match.  Nothing here is scoped by "the section between
# these two headings" — mg-9876's own auditor scored a report LAUNDERED because its `sect()`
# returned the empty string for a section that ends the file, and a whole-transcript anchored
# match with a count check has no such edge.

_FIELDS = [
    # ---- code/rendered_twin_pin_9bc2 -------------------------------------------------
    ("twin.control_exit", "twin",
     r"^control exit\s+:\s+(?P<v>\d+)\s", int),
    ("twin.negative_exit", "twin",
     r"^negative exit\s+:\s+(?P<v>\d+)\s", int),
    ("twin.verdict_grade", "twin",
     r"^control verdict: VERDICT: (?P<v>[A-Z ]+?) —", str),
    # The worklist is read as a SET OF ROW IDS, not as the line's text.  `7 8` and `8 7` are
    # the same fact and must not be two verdicts.
    ("twin.worklist", "twin",
     r"^The worklist, READ OUT OF SECTION 2 rather than typed here: (?P<v>.*)$",
     lambda s: sorted(s.split())),
    ("twin.mutations_caught", "twin",
     r"^(?P<v>\d+) of \d+ caught; \d+ hole\(s\)\.$", int),
    ("twin.mutations_total", "twin",
     r"^\d+ of (?P<v>\d+) caught; \d+ hole\(s\)\.$", int),
    ("twin.holes", "twin",
     r"^\d+ of \d+ caught; (?P<v>\d+) hole\(s\)\.$", int),
    ("twin.unfalsifiable_rows", "twin",
     r"^(?P<v>\d+) row\(s\) UNFALSIFIABLE", int),
    # ---- code/control_audit_9876 -----------------------------------------------------
    ("audit.broken_producers", "audit",
     r"^broken producers\s+:\s+(?P<v>\d+)\s", int),
    ("audit.producers_with_findings", "audit",
     r"^producers with findings\s+:\s+(?P<v>\d+)$", int),
    ("audit.census_grade", "audit",
     r"^CENSUS (?P<v>COMPLETE|INCOMPLETE) —", str),
    ("audit.arms", "audit",
     r"^CENSUS (?:COMPLETE|INCOMPLETE) — (?P<v>\d+) arms, \d+ sites", int),
    ("audit.sites", "audit",
     r"^CENSUS (?:COMPLETE|INCOMPLETE) — \d+ arms, (?P<v>\d+) sites", int),
    ("audit.arms_probed", "audit",
     r"^VERDICT: (?P<v>\d+) arms probed, \d+ shown to discriminate, \d+ not; \d+ demonstrated holes", int),
    ("audit.arms_discriminating", "audit",
     r"^VERDICT: \d+ arms probed, (?P<v>\d+) shown to discriminate, \d+ not; \d+ demonstrated holes", int),
    ("audit.arms_not_shown", "audit",
     r"^VERDICT: \d+ arms probed, \d+ shown to discriminate, (?P<v>\d+) not; \d+ demonstrated holes", int),
    ("audit.aux_holes", "audit",
     r"^VERDICT: \d+ arms probed, \d+ shown to discriminate, \d+ not; (?P<v>\d+) demonstrated holes", int),
    ("audit.selftest_scored", "audit",
     r"^(?P<v>\d+) of \d+ planted worlds scored as required\.$", int),
    ("audit.selftest_total", "audit",
     r"^\d+ of (?P<v>\d+) planted worlds scored as required\.$", int),
    ("audit.sweep_grade", "audit",
     r"^SWEEP (?P<v>OK|BROKEN) —", str),
    ("audit.sweep_membership_candidates", "audit",
     r"^SWEEP (?:OK|BROKEN) — (?P<v>\d+) membership candidates", int),
    ("audit.sweep_tee_sites", "audit",
     r"^SWEEP (?:OK|BROKEN) — \d+ membership candidates, (?P<v>\d+) tee sites", int),
    ("audit.sweep_dirs_without_evidence", "audit",
     r"^SWEEP (?:OK|BROKEN) — \d+ membership candidates, \d+ tee sites, (?P<v>\d+) directories", int),
]

# The runner's own exit status is a field like any other, and it is READ, not inferred.
# Both runners deliberately map some non-zero instrument exits onto a zero runner exit
# (`rendered_twin_pin_9bc2/run_all.sh` exits 0 on DRIFT, on purpose — drift is the normal
# condition of a hand-maintained rendering).  That is why the exit code alone cannot be this
# gate's classifier, and it is measured below rather than argued about.
_RUNNER_EXIT_FIELDS = {"twin": "twin.runner_exit", "audit": "audit.runner_exit"}

FIELD_NAMES = sorted([f[0] for f in _FIELDS] + list(_RUNNER_EXIT_FIELDS.values()))


def run_suite(rel_path):
    """Run one suite runner and return (exit_code, transcript).

    NO PIPE.  `cmd | tee f` makes `$?` tee's status, which is how the first laundered green
    in this lineage was produced (mg-9bc2's own runner, printing CLEAN over a control that
    had exited 1).  subprocess.run with captured output has no such hazard, and the exit code
    returned here is the runner's own.
    """
    path = os.path.join(ROOT, rel_path)
    if not os.path.isfile(path):
        raise Refusal(
            "%s does not exist.  The gate is wired to a suite that is not there; an absent "
            "control is not a passing one." % rel_path)
    proc = subprocess.run(
        ["sh", path], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.returncode, proc.stdout.decode("utf-8", "replace")


def extract(transcripts, exits, only=None):
    """Read every registered field out of the captured transcripts.

    transcripts: {suite: text}.  exits: {suite: int}.
    Raises Refusal naming the field if any pattern does not match EXACTLY once.

    `only` restricts the read to one suite and exists for x1_exhibit.py, which runs the twin
    suite alone.  IT DOES NOT WEAKEN THE GATE, and the reason is structural rather than a
    promise: gate.py never passes it, and `compare` refuses outright when the observed field
    set and the baseline's disagree in EITHER direction — so a partial extraction cannot
    reach a verdict, it can only reach a refusal.  A narrowing option that could be used to
    quietly gate less would be the same shape as the defect this directory exists to catch.
    """
    observed = {}
    for suite, name in _RUNNER_EXIT_FIELDS.items():
        if only is not None and suite != only:
            continue
        if suite not in exits:
            raise Refusal("no exit status captured for suite %r" % suite)
        observed[name] = exits[suite]

    for name, suite, pattern, cast in _FIELDS:
        if only is not None and suite != only:
            continue
        text = transcripts.get(suite)
        if text is None:
            raise Refusal("no transcript captured for suite %r (field %s)" % (suite, name))
        hits = re.findall(pattern, text, re.M)
        if len(hits) != 1:
            raise Refusal(
                "field %s matched its pattern %d time(s) in the %s transcript; exactly one "
                "is required.  0 means the suite did not reach that decision (a traceback and "
                "a finding leave the same exit code — mg-9876); 2 means the pattern no longer "
                "identifies a single fact and its readings could disagree." % (name, len(hits), suite))
        observed[name] = cast(hits[0])
    return observed


# ---------------------------------------------------------------------------------------
# BASELINE
# ---------------------------------------------------------------------------------------

def load_baseline(path=None, raw=None):
    """Load and structurally validate BASELINE.json.

    A missing or malformed baseline is a REFUSAL.  It is not "no expectations, so nothing can
    be wrong" — that reading is the same shape as the unrun control this whole ticket is
    about.
    """
    if raw is None:
        path = path or BASELINE_PATH
        if not os.path.isfile(path):
            raise Refusal(
                "%s is missing.  A gate with no declared baseline cannot say whether anything "
                "changed, and MUST NOT read that as nothing having changed." % path)
        try:
            with open(path) as fh:
                raw = json.load(fh)
        except ValueError as exc:
            raise Refusal("%s is not valid JSON: %s" % (path, exc))
    if not isinstance(raw, dict) or raw.get("schema") != 1:
        raise Refusal("baseline schema is not 1; this gate cannot read it")
    fields = raw.get("fields")
    if not isinstance(fields, dict):
        raise Refusal("baseline has no `fields` object")
    for name, spec in fields.items():
        if not isinstance(spec, dict):
            raise Refusal("baseline field %s is not an object" % name)
        if spec.get("class") not in ("gated", "recorded"):
            raise Refusal(
                "baseline field %s declares class %r; every field must be `gated` (a change "
                "is RED) or `recorded` (a change is printed and not gated, with a stated "
                "reason).  There is no unlabelled third class, because an unlabelled field "
                "is one nobody decided about." % (name, spec.get("class")))
        if "value" not in spec:
            raise Refusal("baseline field %s carries no `value`" % name)
        if not str(spec.get("why", "")).strip():
            raise Refusal(
                "baseline field %s carries no `why`.  A number in a baseline with no reason "
                "beside it is an assertion nobody can audit, and updating it costs nothing." % name)
    return raw


def compare(observed, baseline):
    """Compare observed fields against the baseline.

    Returns (rows, gated_diffs) where rows is a list of dicts suitable for printing.
    Raises Refusal when the field SETS disagree in either direction:

      - observed has a field the baseline does not: a new reading has appeared and nobody
        decided whether it is gated.  Defaulting it to ungated is how coverage goes missing
        quietly; defaulting it to gated is how a gate fails on arrival for no reason.
      - the baseline has a field the extractor no longer produces: the expectation is now
        unfalsifiable.  It cannot fail, and a check that cannot fail is worth nothing —
        mg-9876's UNFALSIFIABLE class, applied to this instrument.
    """
    b_fields = baseline["fields"]
    missing = sorted(set(b_fields) - set(observed))
    extra = sorted(set(observed) - set(b_fields))
    if missing or extra:
        raise Refusal(
            "the baseline and the extractor disagree about WHICH fields exist.\n"
            "  declared in BASELINE.json but not produced by the extractor: %s\n"
            "  produced by the extractor but not declared in BASELINE.json: %s\n"
            "Neither direction may be defaulted: the first is an expectation that can no "
            "longer fail, the second is a reading nobody decided to gate."
            % (", ".join(missing) or "(none)", ", ".join(extra) or "(none)"))

    rows, gated_diffs = [], []
    for name in sorted(observed):
        spec = b_fields[name]
        want, got = spec["value"], observed[name]
        same = want == got
        if same:
            status = "MATCH"
        elif spec["class"] == "gated":
            status = "DIVERGED"
            gated_diffs.append(name)
        else:
            status = "MOVED (recorded, not gated)"
        rows.append({"field": name, "class": spec["class"], "baseline": want,
                     "observed": got, "status": status, "why": spec["why"]})
    return rows, gated_diffs


def render_report(rows):
    """Render the comparison as text.  The mutation control reads THIS, so it is the same
    bytes a human reads — a control that scores a report nobody sees is not a control."""
    out = []
    width = max(len(r["field"]) for r in rows)
    for r in rows:
        out.append("%-*s  %-8s  %-26s  baseline=%s  observed=%s"
                   % (width, r["field"], r["class"], r["status"],
                      json.dumps(r["baseline"]), json.dumps(r["observed"])))
    return "\n".join(out)


def comparison_report(transcripts, exits, baseline):
    """extract + compare + render, in one call.  Returns (report_text, gated_diffs)."""
    observed = extract(transcripts, exits)
    rows, gated_diffs = compare(observed, baseline)
    return render_report(rows), gated_diffs
