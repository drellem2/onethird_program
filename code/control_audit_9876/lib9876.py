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

import atexit
import hashlib
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
       # `{len(moved)}` -> `{len(undeclared)}` at mg-1344: the worklist section 2 grades is
       # now the UNDECLARED half of the moved set.  The arm did not change — the same event
       # (a ledger row moving with nobody accounting for it) is still what it reports.
       ['DRIFT  {len(undeclared)} of', 'PASS  all {len(unmoved)} pinned rows'], 1),
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

    # ----------------------------------------------- twin_pin.py section 7 (mg-7cc3 fold)
    # THE THREE QUESTIONS ARE SEPARATE ARMS BECAUSE THEY CAN STOP HOLDING INDEPENDENTLY, which
    # is this registry's definition of an arm and not a taste about granularity.  `c308368`
    # RESOLVED and was UNREACHABLE; a pin produced by the old `reconcile()` was reachable and
    # digested the wrong revision.  One arm over all three would have been green on the first
    # and is the reason mg-3902's brief had to be corrected mid-flight.
    _a("C7a", "twin_pin.py", "7", "the pinned commit resolves",
       "the revision the page names is one that exists in this repository",
       ['emit("  FAIL  the pinned commit DOES NOT RESOLVE in this repository.")'], 2),
    _a("C7b", "twin_pin.py", "7", "the pinned commit is one this repository INTEGRATES",
       "the revision the page names is an ancestor of an integration branch, so a reader "
       "who fetches `main` can still see it",
       ['emit("  FAIL  THE PINNED COMMIT IS REACHABLE FROM NOTHING THIS REPOSITORY")',
        'PASS  the pinned commit is an ancestor of'], 2),
    _a("C7c", "twin_pin.py", "7", "the named revision carries the digested STATE.md",
       "the commit the page NAMES is the revision the page was DIGESTED against, as opposed "
       "to the two fields merely agreeing with each other",
       ['emit("  FAIL  the pinned commit carries no STATE.md, so it cannot be the")',
        'emit("  FAIL  THE PIN NAMES ONE REVISION AND DIGESTS ANOTHER.")',
        'emit("  PASS  the commit the page NAMES carries the STATE.md the page was")'], 2),

    # ----------------------------------------- twin_pin.py section 8 (mg-1344's protocol)
    # SECTION 8 IS FIVE ARMS AND NOT ONE, BY THIS REGISTRY'S OWN DEFINITION: each names a
    # different way an IN-FLIGHT declaration could buy a subtraction it has not earned, and
    # each could stop holding without the others noticing.  C8d is the one carrying the
    # weight — it is the EXPIRY, and without it the other four describe a permanent excuse
    # with good paperwork.
    _a("C8a", "twin_pin.py", "8", "the declaration is readable as one",
       "a file whose only power is to make this gate accept a moved row is well-formed, so "
       "the weakening it buys can be audited at all",
       ['emit("  FAIL  the in-flight declaration is not readable as one:")',
        'emit(f"  PASS  no {os.path.basename(inflight_path)}'], 2),
    _a("C8b", "twin_pin.py", "8", "declared rows exist and are pinned",
       "a declared relocation names a real ledger row that the pin actually carries, as "
       "opposed to a label that subtracts nothing and hides that it subtracts nothing",
       ["emit(f\"  FAIL  declares row(s) that are not in STATE.md's ledger: \"",
        'emit(f"  FAIL  declares row(s) the pin does not carry:'], 2),
    _a("C8c", "twin_pin.py", "8", "declared rows have actually MOVED",
       "a row is declared in flight because it was relocated, not in advance of being "
       "relocated — the same act R3 refuses one function over",
       ['emit(f"  FAIL  declares row(s) that have NOT moved:',
        'emit(f"  PASS  every declared row is a pinned ledger row that has actu'], 2),
    _a("C8d", "twin_pin.py", "8", "THE DEFERRAL EXPIRES",
       "the excuse for not re-pinning — that no integration-reachable commit carries these "
       "STATE.md bytes — is still TRUE, as opposed to having been true when it was written",
       ['emit("  FAIL  THE DEFERRAL HAS EXPIRED.'], 2),
    _a("C8e", "twin_pin.py", "8", "an unverifiable deferral is not honoured",
       "a checkout that cannot evaluate the expiry declines to apply the subtraction, so "
       "an export or a shallow clone cannot be where a declaration goes unchecked",
       ['emit("  REPORTED, NOT GRADED, AND NOT HONOURED.'], 0),

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
    # THE ROOT CAUSE, ARMED (mg-7cc3).  C7a-C7c DETECT a false pin; this one is the arm that
    # stops the function from MAKING one.  `reconcile()` stamped `rev-parse --short HEAD`
    # while digesting the WORKING TREE, so every reconciliation that also edited STATE.md
    # named the revision before the edit and digested the one after it — the pin was false the
    # instant it was written, and nothing in six sections could say so.
    _a("R5", "twin_pin.py", "reconcile", "refuse to re-pin over an uncommitted STATE.md",
       "the revision a new pin names and the bytes it digests are ONE revision",
       ['REFUSED: STATE.md on disk differs from STATE.md at HEAD'], 2),

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
    _a("N20", "negative_control.py", "7", "mutation: BOTH provenance copies name a "
       "nonexistent commit",
       "C7a fires on the input that left the six-section control CLEAN at exit 0",
       ['@mutation("BOTH copies of the pinned commit name a revision that does not exist"'], 1),
    # ------------------------------------------- negative_control.py, mg-1344's section 8
    _a("N21", "negative_control.py", "8", "mutation: a row declared that has not moved",
       "C8c fires on the cheapest way to abuse a declaration — buying a standing "
       "subtraction for a row that is fine",
       ['@mutation("a declaration for a row that has NOT moved"'], 1),
    _a("N22", "negative_control.py", "8", "mutation: a row declared that does not exist",
       "C8b fires when a declaration names a label the ledger does not have",
       ['@mutation("a declaration for a row that is not in the ledger"'], 1),
    _a("N23", "negative_control.py", "8", "mutation: the declaration is not valid JSON",
       "C8a fires rather than reading an unparseable declaration as an absent one",
       ['@mutation("a declaration that is not valid JSON"'], 1),
    _a("N24", "negative_control.py", "8", "mutation: the declaration names no rows",
       "C8a fires on a declaration that can only weaken this section and let nothing "
       "through",
       ['@mutation("a declaration with an EMPTY row list"'], 1),
    _a("N25", "negative_control.py", "8", "mutation: the declaration carries no reason",
       "C8a fires on an unauditable declaration, and on one that strands whoever meets its "
       "expiry with no instruction",
       ['@mutation("a declaration with no `why` and no `landing_b`"'], 1),
    _a("N26", "negative_control.py", "8", "mutation: the declaration is at another schema",
       "C8a fires rather than reading fields it does not understand",
       ['@mutation("a declaration at an unreadable schema version"'], 1),
    # THE THREE WORLDS THAT NEED A REAL GIT.  Reachability is not a property of any file's
    # text, so these are not `@mutation`s: they build a throwaway repository with a real
    # `main` and run the instrument inside it with `--root`.  A stub git returning what this
    # file expects would be a control scoring its own expectations, which is the class a2
    # calls UNFALSIFIABLE two directories over.
    _a("N27", "negative_control.py", "8", "world: landing A on a branch is HONOURED",
       "the protocol's whole point holds — a declared relocation whose bytes are on no "
       "integration ref MERGES, and the row leaves section 2's worklist",
       ['score("landing A planted in a real git repository"'], 1),
    _a("N28", "negative_control.py", "8", "world: the same declaration once main has it",
       "C8d fires against a REAL history, so the expiry is a fact about git rather than a "
       "sentence in a docstring",
       ['score("landing A after its bytes reach `main`"'], 1),
    _a("N29", "negative_control.py", "8", "world: a declaration with no history to check",
       "C8e fires — the subtraction is declined where it cannot be verified, which is the "
       "fail-open direction this whole section had in its first draft",
       ['def unknown_world('], 1),

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
    # H8 IS H6 FOR mg-1344's SECOND FIELD, AND IT IS AN ARM FOR mg-188d's MEASURED REASON:
    # mg-724a's gate reads `twin.inflight` by exactly-once anchored match, so an absent line
    # is a REFUSAL and not an empty set.  Without this branch the runner would hand the gate
    # a missing field and the gate would say the GATE was broken.
    _a("H8", "run_all.sh", "runner", "section 8 produced a reading at all",
       "the declared-in-flight set is a fact this run reached, as opposed to a line that "
       "vanished because section 8 never ran",
       ['if [ -z "$INFLIGHT" ]'], 2),
]

ARMS_BY_ID = {a.id: a for a in ARMS}


# ======================================================================================
# sandbox
# ======================================================================================

# ---------------------------------------------------------------------------------------
# THE SANDBOX HAS REAL GIT HISTORY (mg-7cc3), AND THAT IS WHAT UNBLOCKED SECTION 7.
#
# It used to be a bare temp tree with no `.git`, and mg-3902 backed its pin-resolution check
# out of `twin_pin.py` for exactly that reason: the probes it would have needed could not run,
# because THE QUESTION SECTION 7 ASKS HAS NO ANSWER INSIDE A TREE WITH NO HISTORY.  So the
# check shipped as a separate suite, a second control over the same pin, with the fold filed
# as its successor.  This is the load-bearing half of that successor.
#
# WHAT THE SANDBOX IS NOW: a self-consistent world.  Its STATE.md and twin are committed on a
# branch called `main`, and the twin's pin is then repointed at THAT commit and at the digest
# of THAT STATE.md — so a probe can construct the good world (the pin names the sandbox's own
# revision and both halves of the acceptance criterion hold) and every bad world beside it: a
# commit that does not resolve, a commit reachable from nothing, a commit whose STATE.md is
# not the one the pin digests.  That is a better fixture than anything writable from outside,
# because nothing in it is borrowed from the repository under audit — the lineage's own
# recurring defect, recorded three times in this directory.
#
# THE PIN IS REPOINTED AFTER THE COMMIT AND THE TREE IS NOT RE-COMMITTED, which is not
# sloppiness: a pin can only name a commit that already exists, so amending it in would change
# the sha the pin names.  That chicken-and-egg IS the root cause mg-3902 found in
# `reconcile()`, and the sandbox reproduces the honest resolution of it — the twin at HEAD is
# one revision behind the twin on disk, and the pin is true about STATE.md, which is what the
# pin claims to be about.
#
# THE IDENTITY AND DATES ARE FIXED so the sandbox's commit sha is a function of its contents
# alone.  A probe transcript that moved every run would be unreadable, and mg-f771 compares
# committed transcripts against what `./build.sh` produces.
_GIT_ENV = {
    "GIT_AUTHOR_NAME": "mg-9876 sandbox", "GIT_AUTHOR_EMAIL": "sandbox@example.invalid",
    "GIT_COMMITTER_NAME": "mg-9876 sandbox", "GIT_COMMITTER_EMAIL": "sandbox@example.invalid",
    "GIT_AUTHOR_DATE": "2026-01-01T00:00:00+00:00",
    "GIT_COMMITTER_DATE": "2026-01-01T00:00:00+00:00",
}

# `-c` overrides rather than inherited config: a global `core.excludesFile` that happens to
# ignore one of the copied files would silently commit a DIFFERENT tree than the sandbox has
# on disk, and a template dir with hooks in it would run somebody's hooks inside an audit.
_GIT_CONF = ["-c", "core.excludesFile=/dev/null", "-c", "init.templateDir=",
             "-c", "commit.gpgsign=false", "-c", "gc.auto=0"]


def sandbox_git(root, *args, check=True):
    """Run git inside a sandbox.  Raises on failure — a silently unbuilt fixture is not a
    fixture, and `SETUP FAILED` is a verdict this harness already knows how to print."""
    env = dict(os.environ)
    env.update(_GIT_ENV)
    proc = subprocess.run(["git", "-C", root] + _GIT_CONF + list(args),
                          capture_output=True, text=True, env=env)
    if check and proc.returncode != 0:
        raise AssertionError("git %s failed in the sandbox: %s"
                             % (" ".join(args), (proc.stderr or proc.stdout).strip()))
    return proc.returncode, proc.stdout.strip()


_PIN_COMMIT = re.compile(r"(\n\s*commit:\s*)[0-9a-f]{7,40}")
_PIN_DATE = re.compile(r"(\n\s*commit-date:\s*)\d{4}-\d\d-\d\d")
_PIN_SHA = re.compile(r"(\n\s*state-sha256:\s*)[0-9a-f]{64}")
_VISIBLE = re.compile(r'(<span id="provenance">.*?@ )[0-9a-f]{7,40}( \()\d{4}-\d\d-\d\d',
                      re.S)


def _repoint(twin_path, commit, date, state_sha):
    """Point BOTH copies of the provenance string at the sandbox's own commit.

    Both, because `twin_pin.py` section 6 checks that they agree and a sandbox whose section 6
    is red by construction would make every probe's good side structurally broken — the
    `borrowed brokenness` defect this directory has recorded three times, arriving by way of
    a fixture instead of a subject.
    """
    text = read(twin_path)
    subs = [(_PIN_COMMIT, commit), (_PIN_DATE, date), (_PIN_SHA, state_sha)]
    for pattern, value in subs:
        text, n = pattern.subn(lambda m, v=value: m.group(1) + v, text, count=1)
        if n != 1:
            raise AssertionError("sandbox: %s matched %d times in the twin, expected 1"
                                 % (pattern.pattern, n))
    text, n = _VISIBLE.subn(lambda m: m.group(1) + commit + m.group(2) + date, text, count=1)
    if n != 1:
        raise AssertionError("sandbox: the visible provenance line matched %d times, "
                             "expected 1" % n)
    write(twin_path, text)


def _copy_tree(tmp):
    os.makedirs(os.path.join(tmp, "docs"), exist_ok=True)
    os.makedirs(os.path.join(tmp, "code"), exist_ok=True)
    # `__pycache__` is IGNORED, because it is the one thing under TARGET whose bytes are not a
    # function of the repository: a `.pyc` carries the source's mtime, and a sandbox commit
    # whose sha moves with a bytecode cache is a fixture nobody can reason about.
    shutil.copytree(TARGET, os.path.join(tmp, "code", TARGET_DIRNAME), dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copy2(STATE, os.path.join(tmp, "STATE.md"))
    shutil.copy2(TWIN, os.path.join(tmp, "docs", "state-of-the-wall.html"))
    return tmp


_TEMPLATE = []


def _template():
    """Build the committed world ONCE per process and hand out copies of it.

    THE REASON IS MEASURED, NOT TIDINESS.  `git init` + `add` + `commit` is 0.26 s and this
    harness builds 61 sandboxes, so building each one from scratch put 15 s on the merge
    critical path — against an 11 s producer.  Copying a built tree is 0.02 s.  Every sandbox
    is still a private, mutable copy: probes commit into theirs (C7c does) and nothing is
    shared but the bytes they start from.
    """
    if not _TEMPLATE:
        tmp = _copy_tree(tempfile.mkdtemp(prefix="ca9876-template-"))
        sandbox_git(tmp, "init", "--quiet")
        # `symbolic-ref` rather than `init -b main`, which git only learned in 2.28.  The
        # branch has to be called `main` because that is one of the integration refs section 7
        # grades against, and a sandbox on `master` would classify its own HEAD an ORPHAN.
        sandbox_git(tmp, "symbolic-ref", "HEAD", "refs/heads/main")
        sandbox_git(tmp, "add", "-A")
        sandbox_git(tmp, "commit", "--quiet", "-m", "sandbox: STATE.md and its rendered twin")
        _rc, commit = sandbox_git(tmp, "rev-parse", "--short", "HEAD")
        _rc, date = sandbox_git(tmp, "log", "-1", "--format=%cs")
        with open(os.path.join(tmp, "STATE.md"), "rb") as fh:
            state_sha = hashlib.sha256(fh.read()).hexdigest()
        _repoint(os.path.join(tmp, "docs", "state-of-the-wall.html"), commit, date, state_sha)
        _TEMPLATE.append(tmp)
        atexit.register(shutil.rmtree, tmp, True)
    return _TEMPLATE[0]


def make_sandbox(prefix="ca9876-", history=True):
    """A throwaway tree with the same shape the target expects: <root>/{STATE.md,docs,code},
    committed on a branch called `main` unless `history=False`.

    Probes mutate INSIDE here.  Nothing in this instrument writes the working tree; the one
    place that could — `twin_pin.reconcile()`, which writes `TWIN` — is exercised with the
    module's globals repointed here, and `assert_sandboxed` refuses if they are not.

    `history=False` exists so that the NO-HISTORY world stays reachable: `twin_pin.py`
    section 7 reports and does not grade when there is no repository to ask, and that branch
    is exactly the S1/S2/S3 shape this directory's COVERAGE.md records — `ROOT was not a git
    repo and three arms were condemned by one line`.  A world nothing enters is a world
    nothing checks.
    """
    tmp = tempfile.mkdtemp(prefix=prefix)
    if not history:
        return _copy_tree(tmp)
    shutil.copytree(_template(), tmp, dirs_exist_ok=True, symlinks=True)
    return tmp


def assert_sandboxed(*paths):
    """Refuse to proceed if a probe is about to write outside a temp directory."""
    real_targets = {os.path.realpath(STATE), os.path.realpath(TWIN)}
    for p in paths:
        rp = os.path.realpath(p)
        if rp in real_targets or rp.startswith(os.path.realpath(ROOT) + os.sep + "docs"):
            raise AssertionError(f"REFUSED: probe would write the working tree at {p}")


def run_control(state_path, twin_path, target_dir=TARGET, inflight_path=None):
    """Run twin_pin.py over the given pair.  Returns (exit_code, combined_output).

    `inflight_path` is passed ALWAYS, defaulting to a path inside the sandbox that does not
    exist (mg-1344).  Leaving it off would let section 8 fall back to the REAL repository's
    IN-FLIGHT.json, so a declaration on the working tree would silently reach every probe in
    this harness — a sandbox that reads one file out of the tree it is isolating.
    """
    inflight_path = inflight_path or os.path.join(target_dir, "IN-FLIGHT.json")
    proc = subprocess.run(
        [sys.executable, os.path.join(target_dir, "twin_pin.py"),
         "--state", state_path, "--twin", twin_path, "--inflight", inflight_path],
        capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def write(path, text):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
