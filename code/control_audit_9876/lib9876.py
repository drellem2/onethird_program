#!/usr/bin/env python3
"""mg-9876 — the arm registry for `code/rendered_twin_pin_9bc2`, and the sandbox its probes run in.

WHY THIS FILE EXISTS.  Three separate controls in one directory each certified their own
execution rather than the property they were named for: `run_all.sh` read `tee`'s exit code
and printed `CLEAN` over a `DRIFT`; section 5 matched a raw line and so was blind to the
one string it was written for; and `negative_control.py`'s positive control asserted
`"8 9" in out` against the WHOLE report, which section 1 satisfies on every healthy run,
forever.  Three is not three mistakes.  This module is the enumeration that makes the fourth
findable before it is written.

THE UNIT IS THE ARM, NOT THE FILE OR THE SECTION.  An arm is one place that can say NO.
`twin_pin.py` section 5 is two arms, because `Generated <date>` and an unattributed
canonicity claim are two different things that could stop happening independently.
`run_all.sh` is four arms, because its four branches classify four different worlds and
three of them were written without ever being entered.

THE QUESTION EVERY ARM IS SCORED ON is the ticket's: what would this report if the thing it
names STOPPED HAPPENING?  If the answer is "the same as now", the arm is LAUNDERED — it is
read as coverage and is not.  The answer is DEMONSTRATED, never asserted: `a2_discriminate.py`
runs each arm's subject twice, once on a known-good input and once on a known-bad one, and
requires the arm's own report to differ.  A predicate that is satisfied by the GOOD input is
not a weaker check, it is the mg-2f44 defect exactly, and it is scored as a finding against
THIS instrument rather than against the arm.

REGISTRY, NOT INFERENCE.  The arms below are typed out by hand, because a regex over source
cannot tell an arm from a print.  What is NOT typed out is the CLAIM THAT THE LIST IS
COMPLETE: `a1_census.py` rediscovers every arm-shaped site in the five source files
mechanically and refuses if any site is unclaimed.  That is the only part of this
enumeration that can be wrong quietly, so it is the part that is checked by machine.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
TARGET_DIRNAME = "rendered_twin_pin_9bc2"
TARGET = os.path.join(ROOT, "code", TARGET_DIRNAME)
STATE = os.path.join(ROOT, "STATE.md")
TWIN = os.path.join(ROOT, "docs", "state-of-the-wall.html")

SOURCES = ["twin_pin.py", "lib9bc2.py", "negative_control.py", "seed_pin.py", "run_all.sh"]


# ======================================================================================
# arm-shaped site discovery — the mechanical half, which is what makes the hand list
# falsifiable.  A site is a source location that can say NO (or say the PASS that a NO
# would replace).  Discovery is deliberately over-broad: an extra site that no arm claims
# fails the census, and that is the outcome we want when somebody adds a check.
# ======================================================================================

SITE_PATTERNS = {
    "twin_pin.py": [
        (re.compile(r"""^\s*emit\(f?['"]\s{2}(PASS|FAIL|DRIFT|DIFFERS)"""), "verdict-emit"),
        (re.compile(r"^\s*sys\.exit\((?!main\(\))"), "refusal"),
    ],
    "lib9bc2.py": [
        (re.compile(r"^\s*raise\s+\w+Error"), "parser-raise"),
    ],
    "negative_control.py": [
        (re.compile(r"^@mutation\("), "mutation"),
        (re.compile(r'"SETUP FAILED"'), "setup-guard"),
        (re.compile(r'"UNFALSIFIABLE"'), "baseline-absence-guard"),
        (re.compile(r"^\s*return 1$"), "harness-verdict"),
    ],
    "seed_pin.py": [
        (re.compile(r"^\s*sys\.exit\((?!main\(\))"), "refusal"),
    ],
    "run_all.sh": [
        # INDENTED BRANCHES COUNT.  `^if \[` missed the nested guard inside the DRIFT branch,
        # which is a check that can say NO and was therefore an arm nobody was auditing —
        # the census's own version of the defect it exists to find.
        (re.compile(r"^\s*if \["), "branch"),
        (re.compile(r'^echo "CLEAN'), "fallthrough"),
    ],
}


def discover_sites(target_dir=TARGET):
    """[(file, lineno, kind, text)] for every arm-shaped site in the target directory."""
    found = []
    for name in SOURCES:
        path = os.path.join(target_dir, name)
        with open(path, encoding="utf-8") as fh:
            for lineno, line in enumerate(fh.read().split("\n"), 1):
                for pattern, kind in SITE_PATTERNS[name]:
                    if pattern.search(line):
                        found.append((name, lineno, kind, line.strip()))
                        break
    return found


# ======================================================================================
# the registry
# ======================================================================================

class Arm:
    """One place that can say NO.

    `subject` is the thing whose STOPPING the arm is supposed to report.  It is written as a
    sentence about the world and not about the code, because the ticket's question — what
    would this report if the thing it names stopped happening? — is unanswerable when the
    subject is stated as "line 178 compares two strings".
    """

    def __init__(self, arm_id, source, section, name, subject, sites, grade):
        self.id = arm_id
        self.source = source
        self.section = section
        self.name = name
        self.subject = subject
        self.sites = sites            # substrings that must resolve to discovered sites
        self.grade = grade            # the verdict grade the arm contributes when it fires

    def __repr__(self):
        return f"<Arm {self.id}>"


def _a(*args):
    return Arm(*args)


ARMS = [
    # ------------------------------------------------------------------ twin_pin.py
    _a("C1a", "twin_pin.py", "1", "pin block present",
       "the twin names a STATE.md revision at all",
       ['emit("  FAIL  no STATE-PIN block in the twin.")'], 2),
    _a("C1b", "twin_pin.py", "1", "row sets agree",
       "STATE.md, the twin and the pin describe the same set of ledger rows",
       ['PASS  all three row sets agree', 'FAIL  the row sets disagree'], 2),
    _a("C1c", "twin_pin.py", "1", "ledger columns are pinned",
       "the ledger's columns are the ones the pinned per-row digests were taken over",
       ['FAIL  the pin does not record the ledger columns',
        'PASS  the ledger\'s columns are the ones',
        "FAIL  the ledger's column set has changed since the pin"], 2),
    _a("C2", "twin_pin.py", "2", "per-row digests",
       "no STATE.md ledger row has moved since the twin was reconciled against it",
       ['DRIFT  {len(moved)} of', 'PASS  all {len(unmoved)} pinned rows'], 1),
    _a("C3", "twin_pin.py", "3", "whole-file digest",
       "STATE.md is byte-identical to the revision recorded in the pin",
       ['PASS  STATE.md is byte-identical', 'DIFFERS  STATE.md has changed since the pin'], 1),
    _a("C3a", "twin_pin.py", "3", "the pin CARRIES a whole-file digest",
       "the pin records a well-formed STATE.md digest at all, as opposed to disagreeing "
       "with one",
       ['FAIL  the pin carries no well-formed `state-sha256` field'], 2),
    _a("C4", "twin_pin.py", "4", "kind marks agree",
       "every ledger row carries the same controlled-vocabulary Kind mark in both documents",
       ['FAIL  the Kind column disagrees', 'PASS  all {len(state_rows)} rows carry'], 2),
    _a("C5a", "twin_pin.py", "5", "banned: Generated <date>",
       "the twin does not claim to have been generated on a date",
       ['FAIL  :{line_no} matches', 'PASS  no banned self-description'], 2),
    _a("C5b", "twin_pin.py", "5", "banned: unattributed canonicity",
       "the twin does not claim canonicity on a line that fails to name STATE.md",
       ['FAIL  :{line_no} matches', 'PASS  no banned self-description'], 2),
    _a("C6a", "twin_pin.py", "6", "visible provenance present",
       "a reader who opens the page in a browser is shown which STATE.md this renders",
       ['FAIL  no <span id="provenance">'], 2),
    _a("C6b", "twin_pin.py", "6", "visible provenance names EXACTLY the pin",
       "the visible provenance line and the machine pin name the same commit and no other",
       ['PASS  the visible line names exactly the pinned commit',
        'FAIL  the visible provenance line does not name exactly'], 2),
    _a("C6c", "twin_pin.py", "6", "the pin has a commit field",
       "there is a pinned commit for the visible line to be compared against",
       ['FAIL  the pin carries no `commit:` field'], 2),

    # ------------------------------------------------- twin_pin.py --reconcile refusals
    _a("R1", "twin_pin.py", "reconcile", "--reconcile requires --rows",
       "a re-pin names the rows whose cells were actually reconciled",
       ['sys.exit("--reconcile requires --rows'], 2),
    _a("R2", "twin_pin.py", "reconcile", "refuse unknown row labels",
       "every row named for re-pinning is a row that exists in STATE.md",
       ['REFUSED: no such ledger row(s)'], 2),
    _a("R3", "twin_pin.py", "reconcile", "refuse re-pinning an unmoved row",
       "a re-pin records a reconciliation that actually happened",
       ['have not moved since the pin'], 2),
    _a("R4", "twin_pin.py", "reconcile", "exactly one provenance span",
       "the visible provenance line moves with the machine pin, wholly or not at all",
       ['REFUSED: expected exactly one <span id="provenance">'], 2),

    # ------------------------------------------------------------------ lib9bc2.py
    _a("L1", "lib9bc2.py", "parse", "STATE.md ledger header present",
       "STATE.md still contains the ledger table this instrument reads",
       ['raise ValueError("no ledger header'], 2),
    _a("L2", "lib9bc2.py", "parse", "ledger row has five cells",
       "the ledger's column count is the one the digest is taken over",
       ['has {len(cells)} cells, expected 5'], 2),
    _a("L3", "lib9bc2.py", "parse", "ledger header has rows under it",
       "the ledger is not empty",
       ['raise ValueError("ledger header found but no rows'], 2),
    _a("L4", "lib9bc2.py", "parse", "twin has ledger rows",
       "the twin still renders a ledger table",
       ['raise ValueError("no ledger rows found in the twin")'], 2),
    _a("L5", "lib9bc2.py", "parse", "pin block is terminated",
       "a pin that starts is a pin that ends, so the parse cannot silently truncate",
       ["present with no {PIN_END!r}"], 2),

    # ------------------------------------------------------------------ seed_pin.py
    _a("S1", "seed_pin.py", "seed", "seed commit is readable",
       "the commit the pin is seeded at still exists in this repository's history",
       ['cannot read STATE.md at {PIN_COMMIT}'], 2),
    _a("S2", "seed_pin.py", "seed", "seed commit touches both files",
       "the seed commit is a RECONCILIATION and not a one-sided edit",
       ['does not touch {required}'], 2),
    _a("S3", "seed_pin.py", "seed", "refuse to re-seed over a pin",
       "seeding is a one-time act and cannot silently overwrite a reconciled pin",
       ['REFUSED: the twin already carries a pin'], 2),

    # ------------------------------------------------------------- negative_control.py
    _a("N1", "negative_control.py", "1", "mutation: pin block deleted",
       "C1a fires when the pin is removed",
       ['@mutation("pin block deleted entirely"'], 1),
    _a("N2", "negative_control.py", "1", "mutation: twin row deleted",
       "C1b fires when a row exists in one document only",
       ['@mutation("a ledger row deleted from the twin only"'], 1),
    _a("N3", "negative_control.py", "2", "mutation: one char in an undrifted row",
       "C2 fires on a one-character change to a row that was not already drifted",
       ['@mutation("one character changed in an UNDRIFTED'], 1),
    _a("N4", "negative_control.py", "2", "mutation: ledger cell emptied",
       "C2 fires when a whole cell is deleted",
       ['@mutation("a whole STATE.md ledger cell emptied'], 1),
    _a("N5", "negative_control.py", "4", "mutation: twin kind flipped",
       "C4 fires when the twin's Kind mark is wrong",
       ["@mutation(\"twin's KIND mark for row 10 flipped"], 1),
    _a("N6", "negative_control.py", "4", "mutation: STATE.md kind flipped",
       "C4 fires when STATE.md's Kind mark is wrong",
       ["@mutation(\"STATE.md's KIND mark for row 9 flipped"], 1),
    _a("N7", "negative_control.py", "5", "mutation: Generated re-introduced",
       "C5a fires when the false claim comes back",
       ['@mutation("`Generated <date>` re-introduced into the header"'], 1),
    _a("N8", "negative_control.py", "5", "mutation: canonicity re-claimed",
       "C5b fires when the twin calls itself the source of truth",
       ['@mutation("the twin re-claims canonicity'], 1),
    _a("N9", "negative_control.py", "6", "mutation: visible provenance desynced",
       "C6b fires when the two provenance copies disagree",
       ['@mutation("visible provenance line points at a DIFFERENT'], 1),
    _a("N10", "negative_control.py", "6", "mutation: visible provenance removed",
       "C6a fires when the pin becomes machine-only",
       ['@mutation("visible provenance line removed'], 1),
    _a("N14", "negative_control.py", "1", "mutation: the ledger gains a column",
       "C1c fires when the ledger grows a column outside every pinned digest",
       ['@mutation("the ledger GAINS A COLUMN'], 1),
    _a("N15", "negative_control.py", "3", "mutation: state-sha256 deleted",
       "C3a fires when the pin stops recording a whole-file digest",
       ["@mutation(\"the pin's `state-sha256` field is deleted outright\""], 1),
    _a("N16", "negative_control.py", "1", "mutation: columns field deleted",
       "C1c fires when the pin stops recording the columns",
       ["@mutation(\"the pin's `columns` field is deleted outright\""], 1),
    _a("N17", "negative_control.py", "5", "mutation: Generated behind `<!--`",
       "C5a fires on the bypass mg-9876 demonstrated",
       ['@mutation("`Generated <date>` re-introduced BEHIND'], 1),
    _a("N18", "negative_control.py", "6", "mutation: two commits in the visible line",
       "C6b fires when the visible line names the pin AND another revision",
       ['@mutation("visible provenance names the pinned commit AND a second one'], 1),
    _a("N19", "negative_control.py", "-", "the baseline-absence guard",
       "a mutation's expect string is absent from the UNMUTATED report, so a CAUGHT means "
       "the mutation caused it",
       ['"UNFALSIFIABLE"'], 1),
    _a("N11", "negative_control.py", "-", "the positive control (baseline)",
       "the unmutated tree reports EXACTLY the drift worklist derived from the pin",
       ['@mutation("NO MUTATION — the baseline"'], 1),
    _a("N12", "negative_control.py", "-", "mutation-was-a-no-op guard",
       "a fixture whose search string has rotted is reported rather than scored CAUGHT",
       ['"SETUP FAILED"'], 1),
    _a("N13", "negative_control.py", "-", "holes are a non-zero exit",
       "a hole in the instrument reaches the runner instead of stopping at a printed table",
       ["return 1"], 1),

    # ------------------------------------------------------------------ run_all.sh
    _a("H1", "run_all.sh", "runner", "structural failure is reported",
       "a broken pin mechanism reaches the reader as a non-zero exit",
       ['if [ "$CONTROL" -eq 2 ]'], 2),
    _a("H2", "run_all.sh", "runner", "a hole in the negative control is reported",
       "an instrument that cannot see something it should reaches the reader",
       ['if [ "$NEGATIVE" -ne 0 ]'], 2),
    _a("H3", "run_all.sh", "runner", "drift is reported as drift",
       "a drifted ledger row is named as a worklist rather than swallowed",
       ['if [ "$CONTROL" -eq 1 ]'], 0),
    _a("H4", "run_all.sh", "runner", "the CLEAN fallthrough",
       "a green from this runner means the control ran and found nothing",
       ['echo "CLEAN'], 0),
    _a("H5", "run_all.sh", "runner", "the control REACHED ITS VERDICT",
       "the control got to a decision, as opposed to dying before one",
       ['if [ -z "$VERDICT_LINE" ]'], 2),
    _a("H6", "run_all.sh", "runner", "a drift report names a non-empty worklist",
       "the DRIFT branch's worklist has rows in it, so the grade came from section 2",
       ['if [ -z "$WORKLIST" ]'], 2),
    _a("H7", "run_all.sh", "runner", "an unknown exit code is BROKEN, not CLEAN",
       "the control's exit code is one of its three declared verdicts",
       ['if [ "$CONTROL" -ne 0 ]'], 2),
]

ARMS_BY_ID = {a.id: a for a in ARMS}


# ======================================================================================
# sandbox
# ======================================================================================

def make_sandbox(prefix="ca9876-"):
    """A throwaway tree with the same shape the target expects: <root>/{STATE.md,docs,code}.

    Probes mutate INSIDE here.  Nothing in this instrument writes the working tree; the one
    place that could — `twin_pin.reconcile()`, which writes `TWIN` — is exercised with the
    module's globals repointed here, and `assert_sandboxed` refuses if they are not.
    """
    tmp = tempfile.mkdtemp(prefix=prefix)
    os.makedirs(os.path.join(tmp, "docs"))
    os.makedirs(os.path.join(tmp, "code"))
    shutil.copytree(TARGET, os.path.join(tmp, "code", TARGET_DIRNAME))
    shutil.copy2(STATE, os.path.join(tmp, "STATE.md"))
    shutil.copy2(TWIN, os.path.join(tmp, "docs", "state-of-the-wall.html"))
    return tmp


def assert_sandboxed(*paths):
    """Refuse to proceed if a probe is about to write outside a temp directory."""
    real_targets = {os.path.realpath(STATE), os.path.realpath(TWIN)}
    for p in paths:
        rp = os.path.realpath(p)
        if rp in real_targets or rp.startswith(os.path.realpath(ROOT) + os.sep + "docs"):
            raise AssertionError(f"REFUSED: probe would write the working tree at {p}")


def run_control(state_path, twin_path, target_dir=TARGET):
    """Run twin_pin.py over the given pair.  Returns (exit_code, combined_output)."""
    proc = subprocess.run(
        [sys.executable, os.path.join(target_dir, "twin_pin.py"),
         "--state", state_path, "--twin", twin_path],
        capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def write(path, text):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
