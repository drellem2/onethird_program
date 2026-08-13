#!/usr/bin/env python3
"""mg-9bc2 — the working-tree control for `docs/state-of-the-wall.html`, the rendered twin.

WHAT WENT WRONG.  The twin carried `Generated 2026-07-19` from 2026-07-19 to 2026-08-10.
In that window `STATE.md` was committed to 55 times and went 36,753 -> 186,710 -> 32,772 ->
110,640 bytes, i.e. it was rewritten wholesale twice under a fixed date.  The
drift was eventually found — ledger row 9, mg-07fd's audit of mg-3329 — by a human reading
the two files against each other.  NOTHING COULD HAVE FAILED.  A generation date tells a
reader WHEN a rendering was made; the question a reader actually has is WHETHER it still
matches, and no date has ever been able to answer it.

WORSE, AND IT IS THE MORE IMPORTANT FINDING: the word `Generated` was FALSE.  There is no
generator.  `git log --follow docs/state-of-the-wall.html` is five commits, the first of
which (`29ffbf7`) adds the twin and `STATE.md` together, and the four after it are hand
edits — mg-957a's says so in as many words, "the .html carried the identical false sentence
verbatim".  Nothing in this repository writes the file.  The three scripts that mention it
by name (`code/eps_spec_sweep_372e/s1_census.py`, `s2_classify.py`,
`code/rate_sweep_910c/r2_classify.py`) all READ it as a corpus member.  So for three weeks
the twin asserted a reproducible relationship to a source that it has never had.

WHAT THIS INSTRUMENT DOES, AND WHAT IT REFUSES TO PRETEND TO DO.  It cannot regenerate the
twin, because there is nothing to regenerate it with.  What it can do is make the twin NAME
THE `STATE.md` IT IS A RENDERING OF — mg-1abe's phrase, A PUBLISHER IS NOT A PIN — and then
check that pin.  The pin lives in the twin, at the top of the file, so it cannot be
separated from the artifact it describes.

EIGHT CHECKS.  Sections 1-3 are the pin; 4 is a cross-document check that does not use the
pin at all; 5 is a default-deny guard on the sentences that caused this; 6 checks the one
duplicate this repair deliberately introduces; 7 and 8 are the ones that ask GIT anything.

    1  the pin is present, parses, and its row set matches both documents
    2  per-row digests: which STATE.md ledger rows have MOVED since the twin was pinned
    3  the whole-file STATE.md digest, as the coarse "has anything at all moved" signal
    4  KIND MARKS agree between the two documents, live, right now
    5  the twin does not claim to be `Generated`, and does not claim canonicity for itself
    6  the VISIBLE provenance line in the header quotes the same commit as the pin
    7  the pinned commit RESOLVES, is one this repository INTEGRATES, and carries the
       STATE.md the pin digests
    8  DECLARED IN-FLIGHT RELOCATIONS: rows whose re-pin is deferred to a second landing,
       and whether that deferral has EXPIRED

SECTION 8 IS mg-1344's, AND IT EXISTS BECAUSE SECTIONS 1-7 CLOSED A DEADLOCK AROUND A ROW
THAT HAS TO MOVE.  Three facts, each read out of the estate:

    (1) moving a pinned ledger row grows section 2's worklist, and `twin.worklist` is a GATED
        field in code/control_gate_724a/BASELINE.json, so the row edit is RED on its own;
    (2) `reconcile()` REFUSES while STATE.md on disk differs from STATE.md at HEAD, so the
        re-pin cannot share the row edit's commit — "THE COST IS TWO COMMITS INSTEAD OF ONE";
    (3) a re-pin in a later commit on the SAME branch names a hash the refinery's rebase
        rewrites out of existence, and section 7 grades the resulting orphan RED.  `2fbd5ce`
        died exactly that way (7e7bfb7, mg-cdd5).

Each is individually correct and they close on each other, so `docs/state-split-proposal`'s
Full-ledger row — 2,887 words down to 600 — could not land at all.  THE FACT THIS SECTION
CHANGES IS (1), AND IT DOES NOT CHANGE IT BY MAKING THE GATE QUIETER.  A ledger-row
relocation is split into two landings:

    LANDING A   move the row's essay out, reconcile the twin's CELL, do NOT re-pin, and
                DECLARE the row in `IN-FLIGHT.json` beside this file.
    LANDING B   once those bytes are on an integration ref, `--reconcile --rows N`.
                `pin_target()` now finds a main-reachable commit and section 7 PASSES.

A declared row is subtracted from section 2's worklist — and that subtraction is the whole
of what could be laundering, so it is bought with a predicate that EXPIRES ON ITS OWN:

    HONOURED       no integration-reachable commit carries these STATE.md bytes, so
                   landing B is IMPOSSIBLE right now.  Reported, not graded — exactly the
                   polarity section 7 already uses for an in-flight COMMIT.
    DISCHARGEABLE  one does.  Landing B is possible, therefore the deferral is over and the
                   declaration is no longer an excuse.  GRADED RED.

The predicate is `reachable_state_commit()` — the SAME search `pin_target()` runs, called
rather than paraphrased, so "the gate honours this" and "a correct pin can be made" cannot
drift apart into two answers.  The consequence is the point: the moment landing A merges,
its own declaration goes RED and stays RED until landing B lands.  A laundered field is
green forever; this one cannot stay green past the moment its excuse expires.

WHAT THIS COSTS, STATED RATHER THAN DISCOVERED.  Between landing A and landing B `main` is
RED for everybody, not only for the author who opened the protocol.  That is a real tax on
an unrelated branch and it is the construction gate.py's own §3 warns about — with one
difference that is why it is taken anyway: the remedy is ONE COMMAND, it is printed in the
failure, and ANY author can run it.  The alternatives were priced and are worse: editing
`twin.worklist` in BASELINE.json is permanent and expires never, and leaving the deadlock in
place means the row never moves at all.  See COVERAGE.md item 6.

SECTION 7 IS mg-3902's CHECK, FOLDED IN (mg-7cc3), AND IT IS HERE BECAUSE SECTIONS 1-6 COULD
NOT SEE THE DEFECT.  Section 3 compares the pinned digest against the LIVE WORKING TREE;
section 6 compares the pinned commit against a VISIBLE COPY OF ITSELF in the page header.  So
the field whose own header calls itself "the only thing in this file that says which STATE.md
it is a rendering of" was checked only against its own duplicate, and two copies of a string
agreeing with each other is consistency, not provenance.  MEASURED, not argued: setting BOTH
copies to `deadbee` — a commit that does not exist — left this control at `VERDICT: CLEAN`,
exit 0.  It was not hypothetical either: at `origin/main` on 2026-08-13 the pin named
`c308368`, a commit reachable only from `origin/polecat-p0e8c` whose STATE.md is not the one
the pin digests.

REACHABILITY IS CHECKED BEFORE BYTE-IDENTITY, AND THE ORDER IS LOAD-BEARING (pm-onethird,
2026-08-13).  `c308368` RESOLVES — it is a real object — so a section 7 that asked only "does
this commit exist?" would go green on the exact pin that motivated the check.  And choosing on
byte-identity first is what produced the bad pin: "which commit does this file reproduce at?"
returns one obviously-correct answer, and if that commit is off main you are then arguing
yourself out of the only candidate you found.  Asking "which main-reachable commits are
eligible?" first cannot produce the bad pin at all.  So an unreachable pin reports NOT AN
ANCESTOR as the primary fault; the digest is printed after it and is a consequence.

EXIT CODES.  0 clean · 1 drift (section 2/3) · 2 structural failure (section 1/4/5/6/7).
Drift is a lower grade than structural failure on purpose: drift is the normal condition of
a hand-maintained rendering between reconciliations, and it is INFORMATION — the row list is
the worklist.  A missing pin, a row set that disagrees, or a re-introduced `Generated` is a
defect in the mechanism itself.

WHAT IS NOT COVERED is stated here and at length in COVERAGE.md.  The twin is a SUMMARY.
Its prose is deliberately shorter than `STATE.md`'s and no byte relation between the two
exists or should, so THIS CONTROL CANNOT TELL YOU THAT AN UNMOVED ROW IS FAITHFULLY
SUMMARISED.  It tells you which rows have moved underneath the summary.  That is strictly
less than "the twin is correct", and it is strictly more than a date.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib9bc2 as L  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
STATE = os.path.join(ROOT, "STATE.md")
TWIN = os.path.join(ROOT, "docs", "state-of-the-wall.html")

# Section 8's declaration.  ABSENCE IS THE NORMAL STATE and is not a finding: a repository
# with no relocation in flight has no file here, which is why the check is not "the file
# exists and is well-formed" but "IF it exists, it is well-formed AND its excuse still holds".
INFLIGHT = os.path.join(HERE, "IN-FLIGHT.json")

# Section 5's default-deny rules.  Each is (regex, why, exemption-predicate-or-None).
# A rule fires when the regex matches a tag-stripped line AND the exemption does not hold.
#
# THE SECOND RULE IS NOT A BAN ON A PHRASE, it is a ban on an UNATTRIBUTED phrase.  The twin
# is allowed to talk about canonicity and about the source of truth — it must, since it is a
# rendering and has to say what of.  What it may not do is use those words about ITSELF.  So
# the rule is: if the line claims canonicity, the same line must name `STATE.md`.  That is
# checkable, it explains itself in the failure message, and it does not require the guard to
# understand English.
_NAMES_SOURCE = re.compile(r"STATE\.md")

# The visible twin of the pin — see section 6 for why a second copy is allowed to exist.
_PROVENANCE = re.compile(r'<span id="provenance">(.*?)</span>\s*$', re.M | re.S)

# Section 6 compares PARSED FIELDS, so it needs to know what a commit looks like in the
# visible line.  `@ <hash>` is the shape `reconcile()` writes; anything hex-and-long in that
# line is treated as a commit reference, because a SECOND revision named there is exactly the
# ambiguity the arm exists to forbid.
_VISIBLE_COMMIT = re.compile(r"\b[0-9a-f]{7,40}\b")

# Section 3 requires the pin to CARRY a whole-file digest, not merely to disagree with one.
_SHA256 = re.compile(r"^[0-9a-f]{64}$")

# The integration branches this repository actually merges to, most authoritative first.
# Reachability against these is what section 7 GRADES.
INTEGRATION_REFS = ("origin/main", "main")

BANNED = [
    (re.compile(r"\bGenerated\b\s*20\d\d-\d\d-\d\d"),
     "a generation date on a file that is NOT generated — the false claim this ticket "
     "exists for.  There is no generator; see this instrument's README.",
     None),
    (re.compile(r"source of truth|\bcanonical\b", re.I),
     "a canonicity claim on a line that does not name STATE.md, i.e. the twin claiming to "
     "be canonical.  STATE.md is; the twin's own lede says so.",
     lambda flat: bool(_NAMES_SOURCE.search(flat))),
]


def sha256_file(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def git(*args, binary=False):
    proc = subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True)
    if binary:
        return proc.returncode, proc.stdout
    return proc.returncode, proc.stdout.decode("utf-8", "replace").strip()


def have_history():
    """Is ROOT the TOP of a git work tree?

    NOT `rev-parse --git-dir`, which is what mg-3902's version of this check asked, and the
    difference is not pedantry: `git -C <tmpdir>` walks UPWARDS, so a temporary tree that
    happens to sit under somebody's repository answers YES and section 7 then resolves this
    tree's pin against a foreign history.  The pin describes THIS root's STATE.md, so the
    question is whether THIS root is a repository, not whether one is above it.
    """
    rc, top = git("rev-parse", "--show-toplevel")
    return rc == 0 and os.path.realpath(top) == os.path.realpath(ROOT)


def ancestry(full, integration_refs=INTEGRATION_REFS):
    """[(ref, is_ancestor_or_None)] for each integration ref; None means the ref is absent.

    Computed once and read twice — the printed table and `classify_reachability` used to ask
    git the same four questions each, which is 8 subprocesses per run against a control that
    `a2_discriminate.py` runs 110 times.  Measured: it is the difference between a 39 s and a
    23 s producer on the merge critical path.
    """
    out = []
    for ref in integration_refs:
        if git("rev-parse", "--verify", "--quiet", ref)[0] != 0:
            out.append((ref, None))
        else:
            out.append((ref, git("merge-base", "--is-ancestor", full, ref)[0] == 0))
    return out


def classify_reachability(full, table=None, integration_refs=INTEGRATION_REFS):
    """Which of four worlds the pinned commit is in.  Returns (verdict, detail).

    `verdict` is one of `integration`, `in-flight`, `orphan`, `unknown`, and only `orphan` is
    graded.  mg-3902 wrote this classifier and mg-daba corrected its polarity; it is carried
    across here rather than re-derived, because the argument behind the four branches is the
    expensive part and it is already paid for.

    WHY `in-flight` IS NOT RED.  A polecat that reconciles on its own branch legitimately
    names a commit that has not merged.  Grading that would make the gate red on every
    correct in-flight reconciliation — a red for a non-reason, shipped inside a remedy for
    reds for non-reasons.  It is REPORTED, and reported as not-yet-acceptable, because THE
    REFINERY REBASES: that hash is rewritten out of existence when the branch lands.

    WHY `orphan` IS RED.  `c308368` was not in flight on the branch that carried it; it was
    on SOMEBODY ELSE's unmerged branch, which no merge would ever bring into `main`.  Telling
    the two apart does not need a human — an ancestor of THIS HEAD is in flight here, and an
    ancestor of neither is on somebody else's branch or on none.

    WHY `unknown` IS SEPARATE FROM `orphan`.  GIT CANNOT ANSWER IS NOT THE ANSWER IS NO.  A
    checkout with no `main` and no `origin/main` — a shallow clone, an export, a fresh
    worktree of one branch — cannot be asked this question, and condemning a correct pin
    there is a red about the checkout rather than about the pin.
    """
    table = ancestry(full, integration_refs) if table is None else table
    if all(anc is None for _ref, anc in table):
        return "unknown", "no integration ref resolves in this checkout"
    for ref, anc in table:
        if anc:
            return "integration", ref

    if git("rev-parse", "--verify", "--quiet", "HEAD")[0] != 0:
        return "unknown", "HEAD does not resolve, so 'on this branch' has no meaning here"
    if git("merge-base", "--is-ancestor", full, "HEAD")[0] == 0:
        return "in-flight", "an ancestor of this HEAD but of no integration ref"
    return "orphan", "an ancestor of neither an integration ref nor this HEAD"


def blob_oid(data):
    """The git object id these bytes WOULD have as a blob.  Writes nothing.

    Used so that "is this STATE.md already on an integration ref?" is answered by comparing
    OBJECT IDS — the same comparison `pin_target()` has always made — rather than by reading
    73 blobs out and hashing them here.
    """
    proc = subprocess.run(["git", "-C", ROOT, "hash-object", "-t", "blob", "--stdin"],
                          input=data, capture_output=True)
    return proc.stdout.decode("utf-8", "replace").strip() if proc.returncode == 0 else ""


def reachable_state_commit(blob, integration_refs=INTEGRATION_REFS):
    """(ref, commit) for the NEWEST integration-reachable commit whose STATE.md is `blob`.

    THE ONE PREDICATE, CALLED TWICE, NEVER PARAPHRASED.  `pin_target()` asks it to decide
    which commit a re-pin may name; section 8 asks it to decide whether a deferred re-pin is
    still deferred.  Those two must be the same question or the gate honours a deferral that
    a re-pin could already have discharged — a second copy of this search that agrees today
    is worse than one (lib724a's own reason for being a library).

    ONE `cat-file --batch-check` PER REF, NOT ONE `rev-parse` PER CANDIDATE.  73 commits
    touch STATE.md on `main` today and section 8 runs on every control run, not only on
    `--reconcile`; 73 subprocesses on the merge critical path, in a control `a2_discriminate`
    already runs 110 times, is a cost paid for nothing.
    """
    if not blob:
        return None
    for ref in integration_refs:
        if git("rev-parse", "--verify", "--quiet", ref)[0] != 0:
            continue
        rc, listing = git("rev-list", ref, "--", "STATE.md")
        candidates = listing.split() if rc == 0 else []
        if not candidates:
            continue
        proc = subprocess.run(
            ["git", "-C", ROOT, "cat-file", "--batch-check=%(objectname)"],
            input="".join(c + ":STATE.md\n" for c in candidates).encode(),
            capture_output=True)
        oids = proc.stdout.decode("utf-8", "replace").split("\n")
        for candidate, oid in zip(candidates, oids):
            if oid.strip() == blob:
                return ref, candidate
    return None


# ---------------------------------------------------------------------------------------
# SECTION 8 — the in-flight relocation declaration
# ---------------------------------------------------------------------------------------

_INFLIGHT_REQUIRED = ("declared_by", "why", "landing_b")


def load_inflight(path):
    """Read IN-FLIGHT.json.  Returns (declaration_or_None, faults).

    A FAULT IS A STRUCTURAL FAILURE, NOT DRIFT, and the reason is the same one BASELINE.json
    gives for refusing a field with no `why`: this file's only job is to make the gate accept
    something it would otherwise refuse, so a malformed one is a weakening nobody can audit.
    Absence returns (None, []) and is silent.

    THE FIELDS ARE REQUIRED FOR THE SAME REASON `--reconcile` REQUIRES `--rows`.  A
    declaration with a one-word reset is a declaration that gets written instead of read.
    `landing_b` is required and PRINTED because the whole protocol is that somebody, possibly
    not the author, has to run it — an expiry with no instruction attached is an expiry that
    strands whoever meets it.
    """
    if not os.path.exists(path):
        return None, []
    try:
        with open(path, encoding="utf-8") as fh:
            raw = json.load(fh)
    except ValueError as exc:
        return None, ["%s is not valid JSON: %s" % (os.path.basename(path), exc)]
    faults = []
    if not isinstance(raw, dict) or raw.get("schema") != 1:
        return None, ["%s declares schema %r; this control reads schema 1 only."
                      % (os.path.basename(path), (raw or {}).get("schema")
                         if isinstance(raw, dict) else None)]
    rows = raw.get("rows")
    # THE LABEL SHAPE IS CHECKED HERE AND NOT LEFT TO `sort_labels`, which does
    # `int(re.match(r"\d+", s).group())` and raises AttributeError on anything that does not
    # start with a digit.  A declaration carrying `"rows": ["foo"]` would then take this
    # control down with a traceback — and a traceback and a finding leave the same exit code
    # (mg-9876), so the runner would have reported a malformed declaration as DRIFT.
    if (not isinstance(rows, list)
            or not all(isinstance(r, str) and re.fullmatch(r"\s*[0-9]+[a-z]?\s*", r or "")
                       for r in rows)):
        faults.append("`rows` must be a list of ledger row labels of the ledger's own shape "
                      "— digits with an optional trailing letter, e.g. [\"3b\", \"6\"].")
        rows = []
    elif not rows:
        faults.append(
            "`rows` is EMPTY.  A declaration that names no row cannot let anything through "
            "and can only weaken this section; delete the file instead.")
    for field in _INFLIGHT_REQUIRED:
        if not str(raw.get(field, "")).strip():
            faults.append("`%s` is missing or empty.  Every field here is load-bearing: this "
                          "file exists to make the gate accept a moved row, and one that does "
                          "not say who, why and how it ends is unauditable." % field)
    raw["rows"] = [r.strip() for r in rows]
    return raw, faults


def sort_labels(labels):
    return sorted(labels, key=lambda s: (int(re.match(r"\d+", s).group()), s))


def state_bytes_of(path, text):
    """The BYTES the discharge test hashes.

    Read from disk rather than re-encoded from the text: `open(..., encoding="utf-8")`
    translates line endings, so a CRLF STATE.md would be hashed as an LF one and the search
    would silently never match — a permanent `honoured`, which is the direction that fails
    open.  The text is only the fallback for a caller with no readable path.
    """
    try:
        with open(path, "rb") as fh:
            return fh.read()
    except OSError:
        return text.encode("utf-8")


def classify_discharge(state_bytes):
    """Has the deferral expired?  Returns (verdict, detail).

    `honoured`      no integration-reachable commit carries these STATE.md bytes, so
                    `--reconcile` CANNOT produce a main-reachable pin and landing B is
                    genuinely impossible.  This is the window the declaration is for.
    `dischargeable` one does.  Landing B is possible NOW, so the deferral is over.
    `unknown`       git cannot be asked here.  GIT CANNOT ANSWER IS NOT THE ANSWER IS NO —
                    section 7's own rule, and the reason an export or a tarball does not get
                    a red about a checkout rather than about a declaration.

    THE THREE `unknown` ROUTES ARE ENUMERATED RATHER THAN LEFT AS AN `else`, BECAUSE EVERY
    ONE OF THEM FAILED OPEN IN THE FIRST DRAFT OF THIS FUNCTION.  No work tree, no integration
    ref, and an unobtainable blob id all reached `reachable_state_commit() -> None`, which is
    the same return value as "searched, and these bytes are on no integration ref" — i.e. the
    search not being ABLE to run was reported as the search having run and come back clean.
    That is the defect this whole directory exists for, re-created inside the arm added to
    remedy it, and it was found by enumerating it rather than by anything failing.
    """
    refs = " or ".join(INTEGRATION_REFS)
    if not have_history():
        return "unknown", "no git work tree at %s" % ROOT
    if all(git("rev-parse", "--verify", "--quiet", r)[0] != 0 for r in INTEGRATION_REFS):
        return "unknown", "no integration ref (%s) resolves in this checkout" % refs
    oid = blob_oid(state_bytes)
    if not oid:
        return "unknown", "git could not compute an object id for these STATE.md bytes"
    hit = reachable_state_commit(oid)
    if hit is None:
        return "honoured", ("no commit reachable from %s carries this STATE.md, so a re-pin "
                            "here could only name an unmerged hash" % refs)
    ref, commit = hit
    return "dischargeable", ("%s is reachable from `%s` and carries this exact STATE.md"
                             % (git("rev-parse", "--short", commit)[1], ref))


def check(state_text, twin_text, state_sha, state_path=STATE, inflight_path=INFLIGHT):
    """Run all eight sections.  Returns (exit_code, list_of_lines)."""
    out = []
    worst = 0
    decl, decl_faults = load_inflight(inflight_path)

    def emit(line=""):
        out.append(line)

    emit("=" * 86)
    emit("mg-9bc2 — rendered-twin pin control")
    emit("  source : STATE.md")
    emit("  twin   : docs/state-of-the-wall.html")
    emit("=" * 86)
    emit()

    # ---------------------------------------------------------------- section 1
    emit("SECTION 1 — the pin is present and its row set matches both documents")
    emit("-" * 86)
    pin = L.parse_pin(twin_text)
    if pin is None:
        emit("  FAIL  no STATE-PIN block in the twin.")
        emit("        The twin does not say which STATE.md it is a rendering of.  That is the")
        emit("        defect this instrument exists to prevent; there is nothing to check.")
        return 2, out

    state_rows = L.parse_state_ledger(state_text)
    twin_rows = L.parse_twin_ledger(twin_text)
    s_labels = set(l for l, _, _ in state_rows)
    t_labels = set(l for l, _ in twin_rows)
    p_labels = set(pin["rows"])

    emit(f"  pin commit      : {pin.get('commit', '(absent)')}")
    emit(f"  pin commit-date : {pin.get('commit-date', '(absent)')}")
    emit(f"  pinned rows     : {len(p_labels)}   STATE.md rows: {len(s_labels)}   "
         f"twin rows: {len(t_labels)}")
    if s_labels == t_labels == p_labels:
        emit(f"  PASS  all three row sets agree: {' '.join(sort_labels(s_labels))}")
    else:
        worst = 2
        emit("  FAIL  the row sets disagree — a row was added or dropped in one document only.")
        emit(f"        in STATE.md not twin : {sort_labels(s_labels - t_labels) or '—'}")
        emit(f"        in twin not STATE.md : {sort_labels(t_labels - s_labels) or '—'}")
        emit(f"        in STATE.md not pin  : {sort_labels(s_labels - p_labels) or '—'}")
    # THE COLUMN LIST IS PART OF THE PIN (mg-9876).  `row_digests` joins FOUR NAMED CELLS,
    # so every column the ledger grows is outside the pin from the day it is added.  A sixth
    # column was demonstrated being added to the header and to all twelve rows with section 2
    # byte-identical and nothing raising — `parse_state_ledger` refuses FEWER than five cells
    # and has no opinion about more.  The pin now records the columns its digests were taken
    # over, so the answer comes from the pin and is not a list typed here.
    pinned_cols = pin.get("columns", "")
    actual_cols = " | ".join(L.ledger_columns(state_text))
    emit(f"  pinned columns  : {pinned_cols or '(absent)'}")
    emit(f"  actual columns  : {actual_cols}")
    if not pinned_cols:
        worst = 2
        emit("  FAIL  the pin does not record the ledger columns its digests were taken over,")
        emit("        so a column added to the ledger would sit outside every digest silently.")
    elif pinned_cols == actual_cols:
        emit("  PASS  the ledger's columns are the ones the pinned digests were taken over.")
    else:
        worst = 2
        emit("  FAIL  the ledger's column set has changed since the pin.  Every per-row digest")
        emit("        below is taken over a DIFFERENT set of cells than the ledger now has.")
        emit(f"        in pin not STATE.md  : {sort_labels(p_labels - s_labels) or '—'}")
    emit()

    # ---------------------------------------------------------------- section 2
    emit("SECTION 2 — per-row digests: which STATE.md rows have MOVED since the twin was pinned")
    emit("-" * 86)
    now = L.row_digests(state_text)
    moved, unmoved = [], []
    # THE DECLARATION IS CONSULTED HERE AND GRADED IN SECTION 8, AND THE SPLIT IS DELIBERATE.
    # Section 2 reports the FACT (which rows moved) and the SPLIT (which of them are
    # declared); whether the declaration is any good is one question asked in one place.
    declared = [] if decl is None else list(decl["rows"])
    discharge, discharge_why = ("none", "no declaration")
    if decl is not None:
        discharge, discharge_why = classify_discharge(state_bytes_of(state_path, state_text))
    # ONLY `honoured` SUBTRACTS, AND `unknown` DELIBERATELY DOES NOT.  Section 7 treats
    # `unknown` as "reported, not graded" because grading it would condemn a pin the checkout
    # cannot check — a red about the CHECKOUT.  Here the polarity is the other way up: the
    # declaration's effect is to REMOVE a row from the field the merge gate exists for, so
    # honouring one whose expiry cannot be evaluated is a subtraction taken on trust.  Not
    # grading it and not honouring it are the same doctrine applied to opposite signs.
    honoured = set(declared) if discharge == "honoured" else set()
    for label in sort_labels(s_labels & p_labels):
        if pin["rows"][label] == now[label]:
            unmoved.append(label)
            emit(f"  row {label:<3}  ok       {now[label]}")
        else:
            moved.append(label)
            mark = "   [DECLARED IN FLIGHT — section 8]" if label in honoured else ""
            emit(f"  row {label:<3}  MOVED    pinned {pin['rows'][label]}  ->  "
                 f"now {now[label]}{mark}")
    undeclared = [l for l in moved if l not in honoured]
    emit()
    # THE WORKLIST IS THE UNDECLARED HALF, AND THE DECLARED HALF IS NOT HIDDEN — IT IS
    # PRINTED ON THE LINE ABOVE, COUNTED HERE, AND GATED SEPARATELY as `twin.inflight`.
    # Subtracting a row from the field mg-724a's gate exists for is the one move in this
    # whole repair that could be laundering, so: the subtraction requires a committed
    # declaration, section 8 grades that declaration on a predicate that expires by itself,
    # and the SUM of the two fields is what it always was.
    if moved and honoured:
        emit(f"  {len(honoured & set(moved))} of the {len(moved)} moved row(s) are DECLARED "
             f"IN FLIGHT: {' '.join(sort_labels(honoured & set(moved)))}")
    if undeclared:
        worst = max(worst, 1)
        emit(f"  DRIFT  {len(undeclared)} of {len(s_labels & p_labels)} ledger rows have "
             f"changed in")
        emit(f"         STATE.md since the twin was last reconciled: {' '.join(undeclared)}")
        emit("         Each is a row the twin renders from text that no longer exists.")
        emit("         This is the WORKLIST.  Reconcile the twin's cell, then re-pin that row:")
        emit(f"             python3 code/rendered_twin_pin_9bc2/twin_pin.py --reconcile "
             f"--rows {','.join(undeclared)}")
    elif moved:
        emit(f"  IN FLIGHT  every one of the {len(moved)} moved row(s) is declared in")
        emit(f"             {os.path.relpath(inflight_path, ROOT)}, so the UNDECLARED worklist")
        emit("             is empty.  That is not the same as clean and section 8 says so.")
    else:
        emit(f"  PASS  all {len(unmoved)} pinned rows still match STATE.md.")
    emit()

    # ---------------------------------------------------------------- section 3
    emit("SECTION 3 — whole-file digest (the coarse signal)")
    emit("-" * 86)
    pinned_sha = pin.get("state-sha256", "")
    emit(f"  pinned STATE.md sha256 : {pinned_sha or '(absent)'}")
    emit(f"  actual STATE.md sha256 : {state_sha}")
    # THE FIELD MUST BE PRESENT AND WELL-FORMED, AND THAT IS A SEPARATE ARM (mg-9876).
    # Without this, deleting `state-sha256` from the pin entirely made section 3 compare the
    # real digest against the empty string and print `DIFFERS` — the same words it prints on
    # every ordinary run, under a heading that says in terms that DIFFERS `is NOT a defect
    # and must not be read as one`.  A broken pin was therefore indistinguishable from the
    # normal condition, and read as it.  COVERAGE.md already records the ancestor of this:
    # the field-name pattern was `[a-z-]+`, `state-sha256` has digits, and section 3 printed
    # the right answer for the wrong reason.  The PATTERN was repaired; the ABSENCE never was.
    if not _SHA256.match(pinned_sha):
        worst = 2
        emit("  FAIL  the pin carries no well-formed `state-sha256` field.  This is a broken")
        emit("        pin, NOT a moved STATE.md, and the two must not print the same word.")
    elif pinned_sha == state_sha:
        emit("  PASS  STATE.md is byte-identical to the revision the twin was pinned against.")
    else:
        # SECTION 3 NO LONGER GRADES, AND THE OLD LINE CONTRADICTED THE FOUR IT PRINTS BELOW
        # (mg-188d).  It ran `worst = max(worst, 1)` while telling the reader in as many words
        # that this state "is NOT a defect and must not be read as one" and that "section 2 is
        # the check that carries the verdict".  COVERAGE.md says the same thing twice more.
        # The contradiction was UNREACHABLE for as long as it existed: rows 8 and 9 had been
        # drifted since the pin was seeded, so section 2 was never 0 while section 3 was 1, and
        # nothing could tell which section the exit code came from.
        #
        # mg-188d reconciled row 8, section 2 went clean, and the state became reachable — and
        # it is not merely reachable, it is what the NEXT STATE.md landing produces, prose or
        # ledger.  MEASURED on this branch before the fix: one appended comment line took
        # twin_pin.py to exit 1 with an EMPTY worklist, the runner's DRIFT branch printed a
        # verdict naming "section 2's worklist" over a section 2 that had named nothing, and
        # then exited 2 BROKEN.  So the first clean twin in this page's history would have made
        # the merge gate red-broken for the next author to touch STATE.md at all, for a reason
        # they could not act on.  Section 3 is a REPORT — mg-724a's word is `recorded`, a dated
        # reading expected to go stale — and section 2 is the expectation.
        emit("  DIFFERS  STATE.md has changed since the pin.")
        emit("           This alone is NOT a defect and must not be read as one, and it no")
        emit("           longer grades: STATE.md changes constantly outside the ledger, and")
        emit("           section 2 is the check that carries the verdict.  This line exists so")
        emit("           that 'the ledger is unmoved' cannot be mistaken for 'the file is")
        emit("           unmoved'.  A MISSING or MALFORMED digest is still structural (above).")
    emit()

    # ---------------------------------------------------------------- section 4
    emit("SECTION 4 — KIND MARKS agree between the two documents (live, does not use the pin)")
    emit("-" * 86)
    twin_kind = {l: L.canonical_kind(d["kind"]) for l, d in twin_rows}
    bad = []
    for label, cells, _raw in state_rows:
        want = L.md_kinds(cells["kind"])
        got = twin_kind.get(label, [])
        if want == got:
            emit(f"  row {label:<3}  ok       {' / '.join(want)}")
        else:
            bad.append(label)
            emit(f"  row {label:<3}  MISMATCH STATE.md {want}  vs  twin {got}")
    emit()
    if bad:
        worst = 2
        emit(f"  FAIL  the Kind column disagrees at {len(bad)} row(s): {' '.join(bad)}")
        emit("        Kind is a controlled vocabulary (U / U-id / FP / FP✗ / OPEN) and is the")
        emit("        one column that IS directly comparable across the summary boundary.")
        emit("        STATE.md's § Kinds says a row's kind decides what may be quoted from it,")
        emit("        so a twin carrying the wrong kind mis-licenses every quote of that row.")
    else:
        emit(f"  PASS  all {len(state_rows)} rows carry the same kind mark in both documents.")
    emit()

    # ---------------------------------------------------------------- section 5
    emit("SECTION 5 — default-deny guard on the two false self-descriptions")
    emit("-" * 86)
    # THE SCAN IS OVER TAG-STRIPPED TEXT, AND THAT IS NOT A REFINEMENT — IT IS THE FIX FOR
    # A DEFECT THIS GUARD SHIPPED WITH.  The first version matched the raw line, and it did
    # not fire on the twin's own `<span><b>Generated</b> 2026-07-19</span>`: the markup sits
    # between the word and the date, so /\bGenerated\b\s+20\d\d/ never matched the one
    # string the guard was written to catch.  A guard against a false claim, blind to that
    # claim, in the file the ticket is about.  Caught only by running it.
    # USE vs MENTION, and this is not a hypothetical.  The repaired lede EXPLAINS the false
    # claim, so it contains the words `Generated 2026-07-19` in order to repudiate them, and
    # the first version of this guard duly failed the very repair that removed the defect.
    # A guard that cannot tell a claim from a quotation of a dead claim forces the fix to be
    # silent about what it fixed, which is worse than the false positive.
    #
    # THE CONVENTION, stated so it is a convention and not a loophole found later: in this
    # file, a superseded string may be quoted ONLY inside <i>…</i> or <s>…</s>.  Both render
    # visibly as quotation / strike-through, so a reader sees a dead string marked dead —
    # the same discipline STATE.md already uses with ~~…~~, which lib9bc2.md_kinds honours.
    # This IS a bypass: wrapping a live claim in <i> hides it from section 5.  It is a
    # declared one, it costs the writer visible italics, and COVERAGE.md records it.
    # THE SKIP IS A LINE RANGE, NOT A TOKEN MATCH, AND THAT IS A REPAIR (mg-9876).  It read
    # `if L.PIN_START.split()[0] in line: continue` — which is the token `<!--`, so EVERY
    # line carrying an HTML comment opener was exempt from the whole guard, and a live
    # `<!----><span><b>Generated</b> 2026-08-10</span>` was demonstrated walking straight
    # past section 5.  It also failed at its stated job in the other direction: only the pin
    # block's FIRST line contains `<!--`, so the rest of the block was scanned anyway.  An
    # exemption wider than the thing it names, and narrower, at once.
    pin_lo = twin_text[:twin_text.find(L.PIN_START)].count("\n") + 1
    pin_hi = twin_text[:twin_text.find(L.PIN_END)].count("\n") + 1
    hits = []
    for line_no, line in enumerate(twin_text.split("\n"), 1):
        if pin_lo <= line_no <= pin_hi:
            continue
        quoted = re.sub(r"<(i|s)>.*?</\1>", " ", line, flags=re.S)
        flat = L.normalise(L.strip_tags(quoted))
        for pattern, why, exempt in BANNED:
            if pattern.search(flat) and not (exempt and exempt(flat)):
                hits.append((line_no, pattern.pattern, why, flat))
    for line_no, pattern, why, flat in hits:
        emit(f"  FAIL  :{line_no} matches /{pattern}/")
        emit(f"        {why}")
        emit(f"        line: {flat[:150]}")
    if hits:
        worst = 2
    else:
        emit(f"  PASS  no banned self-description is present ({len(BANNED)} rules).")
    emit()

    # ---------------------------------------------------------------- section 6
    emit("SECTION 6 — the VISIBLE provenance line quotes the pin (the duplicate is checked)")
    emit("-" * 86)
    emit("  Section 1's pin is an HTML comment: correct, machine-readable, and INVISIBLE to")
    emit("  every reader who opens the page in a browser.  So the header carries the commit")
    emit("  in visible text too — and that is a SECOND copy of a provenance string, i.e.")
    emit("  exactly the kind of thing this whole ticket is about going stale.  It is only")
    emit("  safe because it is checked here.")
    emit()
    m = _PROVENANCE.search(twin_text)
    if not m:
        worst = 2
        emit('  FAIL  no <span id="provenance"> in the twin — the pin is machine-only and no')
        emit("        reader is shown which STATE.md this is a rendering of.")
    else:
        shown = L.normalise(L.strip_tags(m.group(1)))
        pinned_commit = pin.get("commit", "")
        # THE COMMIT IS PARSED OUT OF THE LINE AND COMPARED EXACTLY (mg-9876).  This read
        # `pinned_commit in shown` — a membership test against the whole visible line, which
        # is ticket smell #1 sitting inside the arm added to check a duplicated provenance
        # string.  Truncating the pin's commit to a four-character prefix was demonstrated to
        # PASS, and so would a line that names the pinned commit alongside another one.  What
        # the arm is for is that the two copies name THE SAME revision, and that is an
        # equality between two parsed fields, not a substring relation.
        shown_commits = _VISIBLE_COMMIT.findall(shown)
        emit(f"  visible : {shown}")
        emit(f"  pinned  : {pinned_commit}")
        emit(f"  commits parsed out of the visible line: {shown_commits or '—'}")
        if not pinned_commit:
            worst = 2
            emit("  FAIL  the pin carries no `commit:` field, so there is nothing to quote.")
        elif shown_commits == [pinned_commit]:
            emit("  PASS  the visible line names exactly the pinned commit and no other.")
        else:
            worst = 2
            emit("  FAIL  the visible provenance line does not name exactly the pinned commit.")
            emit("        A reader and the control would be told two different revisions.")
    emit()

    # ---------------------------------------------------------------- section 7
    emit("SECTION 7 — the pin RESOLVES against git (reachability first, then byte-identity)")
    emit("-" * 86)
    emit("  Sections 1-6 ask git nothing.  Section 3 compares the pinned digest against the")
    emit("  LIVE WORKING TREE and section 6 compares the pinned commit against a VISIBLE COPY")
    emit("  OF ITSELF, so the commit field was checked only against its own duplicate.  Setting")
    emit("  BOTH copies to `deadbee` left this control CLEAN at exit 0 (mg-3902, measured).")
    emit()
    pinned_commit = pin.get("commit", "")
    if not have_history():
        emit(f"  no git work tree at {ROOT}")
        emit("  REPORTED, NOT GRADED — this section resolves a pin against history and there")
        emit("        is none here.  GIT CANNOT ANSWER IS NOT THE ANSWER IS NO: an export, a")
        emit("        tarball or a probe's sandbox cannot be asked this question, and a red")
        emit("        for that reason would condemn a pin this checkout cannot check.  It is")
        emit("        mg-9876's own S1/S2/S3 — `ROOT was not a git repo and three arms were")
        emit("        condemned by one line` — and it has now been written twice, so it is")
        emit("        built in rather than remembered.")
    elif not pinned_commit:
        emit("  the pin carries no `commit:` field, so there is no revision to resolve here.")
        emit("  Section 6 already grades that absence (arm C6c) and this section does not")
        emit("  grade it a second time: one defect, one red.")
    else:
        rc, full = git("rev-parse", "--verify", "--quiet", pinned_commit + "^{commit}")
        if rc != 0:
            worst = 2
            emit("  FAIL  the pinned commit DOES NOT RESOLVE in this repository.")
            emit(f"        `{pinned_commit}` names no commit here, so the page names a STATE.md")
            emit("        revision nobody can look at — exactly as checkable as `Generated")
            emit("        <date>` was, in the field that replaced it.")
        else:
            emit(f"  pinned commit  : {pinned_commit}  ->  {full}")
            table = ancestry(full)
            for ref, anc in table:
                shown = "(no such ref in this checkout)" if anc is None else \
                        ("yes" if anc else "NO")
                emit(f"  ancestor of {ref:<12}: {shown}")
            emit()

            # REACHABILITY IS ASKED FIRST AND ITS ANSWER IS PRINTED FIRST.  See the module
            # docstring: the digest is a consequence, and reporting it first sends the reader
            # off to regenerate a digest when the pin itself is what is wrong.
            world, why7 = classify_reachability(full, table)
            if world == "integration":
                emit(f"  PASS  the pinned commit is an ancestor of `{why7}`.  BOTH halves of the")
                emit("        acceptance criterion hold: main-ancestry AND byte-identity.")
            elif world == "orphan":
                worst = 2
                emit("  FAIL  THE PINNED COMMIT IS REACHABLE FROM NOTHING THIS REPOSITORY")
                emit("        INTEGRATES.  It is an ancestor of no integration ref and of no")
                emit("        commit on this branch either, so it lives on somebody else's")
                emit("        unmerged branch — or on none at all — and no merge will ever")
                emit("        bring it into `main`.  `c308368` was exactly this.")
                emit("        THIS IS THE PRIMARY FAULT.  Whatever the digest below says, the")
                emit("        remedy is to REGENERATE the pin at a main-reachable commit;")
                emit("        BYTE-IDENTITY DOES NOT RESCUE AN ORPHAN, because a pin can hash")
                emit("        correctly at a commit that survives only until `git gc`.")
            elif world == "in-flight":
                emit("  IN FLIGHT — REPORTED, NOT GRADED, AND NOT YET ACCEPTABLE.")
                emit(f"        The pinned commit is {why7},")
                emit("        i.e. a reconciliation on this branch")
                emit("        that has not merged.  That is the one legitimate way to name an")
                emit("        unmerged commit and it is why this is not red.  It is also not")
                emit("        done: THE REFINERY REBASES, so this hash is rewritten out of")
                emit("        existence when the branch lands and the pin becomes an ORPHAN.")
                emit("        `2fbd5ce` died that way at mg-cdd5.  Re-pin at a main-reachable")
                emit("        commit before merging — `--reconcile` now picks one for you.")
            else:
                emit(f"  REPORTED, NOT GRADED — {why7}.")
                emit("        Git cannot answer this question here, and 'cannot answer' is not")
                emit("        'the answer is no'.")
            emit()

            rc, blob = git("show", full + ":STATE.md", binary=True)
            if rc != 0:
                worst = 2
                emit("  FAIL  the pinned commit carries no STATE.md, so it cannot be the")
                emit("        revision this page is a rendering of.")
            else:
                there = hashlib.sha256(blob).hexdigest()
                emit(f"  STATE.md AT the pinned commit : {there}")
                emit(f"  STATE.md digest IN the pin    : {pinned_sha or '(absent)'}")
                if not _SHA256.match(pinned_sha):
                    emit("  (no well-formed digest to compare against — section 3 grades that,")
                    emit("   arm C3a.  Absence is not agreement, and it is not graded twice.)")
                elif there == pinned_sha:
                    emit("  PASS  the commit the page NAMES carries the STATE.md the page was")
                    emit("        DIGESTED against — the two provenance fields agree with GIT,")
                    emit("        not merely with each other.")
                else:
                    worst = 2
                    emit("  FAIL  THE PIN NAMES ONE REVISION AND DIGESTS ANOTHER.")
                    emit("        A reader who runs `git show <commit>:STATE.md` to check this")
                    emit("        rendering is handed a different file than the one the row")
                    emit("        digests were taken over.  This is what `reconcile()` produced")
                    emit("        for its whole life before mg-7cc3: it stamped `rev-parse HEAD`")
                    emit("        while digesting the WORKING TREE, so any reconciliation that")
                    emit("        also edited STATE.md named the revision BEFORE the edit and")
                    emit("        digested the one AFTER it.")
    emit()

    # ---------------------------------------------------------------- section 8
    emit("SECTION 8 — DECLARED IN-FLIGHT RELOCATIONS, and whether the deferral has EXPIRED")
    emit("-" * 86)
    emit("  Section 2 subtracts a DECLARED row from its worklist.  That subtraction is the")
    emit("  only thing here that could be laundering, so this section is where it is paid")
    emit("  for: a declared row must have actually moved, and the declaration is honoured")
    emit("  ONLY while `--reconcile` could not produce a main-reachable pin anyway.")
    emit()
    # THE FIELD-SHAPED LINE IS PRINTED ON EVERY RUN, INCLUDING THE EMPTY ONE (mg-188d's rule,
    # inherited deliberately).  Its own directory learnt this the expensive way: the worklist
    # line was printed only in the DRIFT branch, so mg-724a's gate could read the field
    # exactly while the twin was broken and REFUSED the first clean run in the page's history.
    # A field observable only in the failing state cannot report its own success.
    emit(f"  declared in-flight rows: {' '.join(sort_labels(declared)) if declared else '(none)'}")
    emit()
    if decl_faults:
        worst = 2
        emit("  FAIL  the in-flight declaration is not readable as one:")
        for fault in decl_faults:
            emit(f"        - {fault}")
        emit("        A malformed declaration is a STRUCTURAL failure and not drift: this")
        emit("        file's only power is to make the gate accept a moved row, so one that")
        emit("        cannot be read is a weakening nobody can audit.")
    elif decl is None:
        emit(f"  PASS  no {os.path.basename(inflight_path)} — no relocation is in flight, which")
        emit("        is the normal state.  Nothing is subtracted from section 2's worklist.")
    else:
        emit(f"  declared by  : {decl['declared_by']}")
        emit(f"  landing B    : {decl['landing_b']}")
        emit(f"  why          : {str(decl['why']).strip().splitlines()[0][:120]}")
        emit()
        unknown_rows = [r for r in declared if r not in now]
        unpinned = [r for r in declared if r in now and r not in p_labels]
        still = [r for r in declared if r in now and r in p_labels and r not in moved]
        if unknown_rows:
            worst = 2
            emit(f"  FAIL  declares row(s) that are not in STATE.md's ledger: "
                 f"{' '.join(unknown_rows)}")
        if unpinned:
            worst = 2
            emit(f"  FAIL  declares row(s) the pin does not carry: {' '.join(unpinned)}.  There")
            emit("        is no deferred re-pin for a row that was never pinned.")
        if still:
            worst = 2
            emit(f"  FAIL  declares row(s) that have NOT moved: {' '.join(still)}.")
            emit("        Declaring an in-flight relocation for a row nobody relocated is the")
            emit("        same act as re-pinning a row nobody reconciled, one level up — the")
            emit("        move COVERAGE.md item 4 calls the easiest way to defeat this")
            emit("        mechanism.  It buys a standing subtraction for a row that is fine.")
        if not (unknown_rows or unpinned or still):
            emit(f"  PASS  every declared row is a pinned ledger row that has actually moved.")
        emit()
        emit(f"  discharge test : {discharge.upper()} — {discharge_why}")
        if discharge == "dischargeable":
            worst = 2
            emit("  FAIL  THE DEFERRAL HAS EXPIRED.  Landing A's bytes are on an integration")
            emit("        ref, so `pin_target()` can now name a commit that survives the")
            emit("        rebase and landing B is not merely possible but overdue.  From here")
            emit("        the declaration is no longer an excuse, it is an unrepaired pin.")
            emit("        THIS RED IS NOT ONLY THE DECLARER'S TO CLEAR — anyone may run it:")
            emit(f"            {decl['landing_b']}")
            emit(f"        then delete {os.path.relpath(inflight_path, ROOT)} in the same commit")
            emit("        and move `twin.inflight` back to [] in BASELINE.json.")
            emit("        (`reconcile()` also requires STATE.md on disk to equal STATE.md at")
            emit("        HEAD, so commit or restore any unrelated edit to it first.)")
        elif discharge == "honoured":
            emit("  HONOURED — REPORTED, NOT GRADED, AND NOT A CLEAN TWIN.")
            emit("        Landing B is impossible right now for the reason that created this")
            emit("        protocol, so a red here would be a red for a state nobody can leave.")
            emit("        This is the same polarity section 7 gives an in-flight COMMIT, and it")
            emit("        is bought the same way: it expires by itself.  The instant these")
            emit("        bytes reach an integration ref this section goes RED and stays RED")
            emit("        until landing B lands.")
        else:
            emit("  REPORTED, NOT GRADED, AND NOT HONOURED.  Git cannot be asked here, and")
            emit("        'cannot answer' is not 'the answer is no' — so this declaration is")
            emit("        not condemned.  It is also not APPLIED: the declared rows stay in")
            emit("        section 2's worklist, because subtracting them would be a weakening")
            emit("        this checkout has no way to check.  Section 7 declines to grade an")
            emit("        unverifiable pin for the same reason this declines to honour an")
            emit("        unverifiable deferral; the sign differs, the doctrine does not.")
    emit()

    emit("=" * 86)
    if worst == 0 and moved and honoured:
        # A FOURTH VERDICT WORD, BECAUSE `CLEAN` WOULD BE FALSE.  Exit 0 matches section 7's
        # treatment of an in-flight commit — reported, not graded — and the WORD is what
        # mg-724a's gate reads (`twin.verdict_grade`), so this state is a declared baseline
        # movement rather than a silent pass.  The exit code was never the classifier here.
        emit("VERDICT: IN FLIGHT — every moved ledger row is declared in flight and the "
             "deferral has not expired.")
    else:
        emit({0: "VERDICT: CLEAN — the twin is pinned and its ledger rows have not moved.",
              1: "VERDICT: DRIFT — see section 2's worklist.  The twin renders rows that have "
                 "since changed.",
              2: "VERDICT: STRUCTURAL FAILURE — the pin mechanism itself is broken or a banned "
                 "claim is back."}[worst])
    emit("=" * 86)
    return worst, out


def pin_target():
    """The (commit, date) a re-pin should record.  REACHABILITY FIRST, then byte-identity.

    THIS USED TO BE `git rev-parse --short HEAD`, AND THAT ONE LINE IS THE ROOT CAUSE mg-3902
    found (mg-7cc3 repairs it).  It stamped HEAD while `reconcile()` digested the WORKING
    TREE.  Those are the same revision only while STATE.md is clean — and a reconciliation is
    exactly the case where it is not, since the natural way to do one is to edit the STATE.md
    row, rewrite the twin's cell and re-pin, all in the commit about to be made.  Do that and
    the pin names the revision BEFORE the edit and digests the one AFTER it.  Every
    reconciliation that touched STATE.md produced a false pin, and nothing checked it.

    `reconcile()` refuses outright when STATE.md on disk differs from STATE.md at HEAD, so by
    the time this runs the bytes being digested ARE some committed revision's bytes.  The
    question left is WHICH revision to name, and it is asked in the order pm-onethird handed
    down on 2026-08-13: WHICH COMMITS ARE ELIGIBLE (ancestors of an integration ref), and only
    then WHICH OF THOSE REPRODUCES.  Asking it the other way round — "which commit does this
    file reproduce at?" — returns one obviously-correct answer, and when that answer is off
    main you are left arguing yourself out of the only candidate you found.  That is how
    `c308368` was pinned.

    SO A TWIN-ONLY RECONCILIATION NEVER LANDS AN IN-FLIGHT PIN AGAIN.  Its STATE.md is
    unchanged, so an integration-reachable commit carrying these exact bytes exists and is
    named.  A reconciliation whose STATE.md has ALSO landed on this branch and nowhere else
    has no such commit; that falls back to HEAD and SAYS SO, because the alternative is
    refusing a correct act.  Section 7 reports that pin `IN FLIGHT`, and the refinery's rebase
    will turn it into an ORPHAN — so the warning is the whole point of printing it.
    """
    if not have_history():
        return "", ""
    _rc, head_blob = git("rev-parse", "--verify", "--quiet", "HEAD:STATE.md")
    # THE SEARCH MOVED OUT OF THIS FUNCTION AND IS NOT A COPY (mg-1344).  Section 8 asks the
    # SAME question to decide whether a deferred re-pin may still be deferred, and two
    # implementations of "which commit may this pin name?" that agree today would eventually
    # disagree — at which point the gate would honour a deferral this function could already
    # have discharged.
    hit = reachable_state_commit(head_blob)
    if hit is not None:
        ref, candidate = hit
        short = git("rev-parse", "--short", candidate)[1]
        print(f"pinning at {short}, the newest commit reachable from `{ref}` whose "
              f"STATE.md is these bytes.")
        return short, git("log", "-1", "--format=%cs", candidate)[1]
    short = git("rev-parse", "--short", "HEAD")[1]
    print(f"WARNING: no commit reachable from {' or '.join(INTEGRATION_REFS)} carries this")
    print(f"         STATE.md, so the pin names HEAD ({short}), which has not merged.")
    print("         Section 7 will report it IN FLIGHT, and THE REFINERY REBASES: this hash")
    print("         is rewritten out of existence when the branch lands and the pin becomes")
    print("         an ORPHAN, which section 7 grades RED.  Re-run --reconcile after the")
    print("         STATE.md change has landed on main.")
    return short, git("log", "-1", "--format=%cs", "HEAD")[1]


def reconcile(rows_arg, note):
    """Re-pin.  Per-row and deliberate, never a blanket 'make it pass' button.

    THE TRAP THIS AVOIDS.  A detector with a one-word reset is a detector that gets reset
    instead of read — the drift becomes invisible again and the instrument now certifies it.
    So `--reconcile` requires the caller to NAME the rows they actually reconciled in the
    twin.  Naming a row that has not moved is refused, and `--rows all` still prints every
    row it re-pins so the diff shows what was claimed.
    """
    # THE ROOT CAUSE, REFUSED RATHER THAN DETECTED (mg-3902 found it, mg-7cc3 repairs it).
    # See `pin_target()`.  The commit named and the bytes digested have to be one revision,
    # and the only way to guarantee that is to refuse while they are two.  THE COST IS TWO
    # COMMITS INSTEAD OF ONE: land the STATE.md edit, then reconcile the twin against it.
    # The twin is left UNWRITTEN — a half-done re-pin is worse than a refused one.
    if have_history():
        rc, head_blob = git("show", "HEAD:STATE.md", binary=True)
        with open(STATE, "rb") as fh:
            disk = fh.read()
        if rc == 0 and disk != head_blob:
            sys.exit("REFUSED: STATE.md on disk differs from STATE.md at HEAD, so a re-pin "
                     "here would name one revision and digest another — the exact defect "
                     "mg-3902 found in this function.  Commit the STATE.md change first, "
                     "then reconcile the twin against it.  The twin has NOT been written.")

    state_text = open(STATE, encoding="utf-8").read()
    twin_text = open(TWIN, encoding="utf-8").read()
    now = L.row_digests(state_text)
    pin = L.parse_pin(twin_text)

    if pin is None:
        targets = sort_labels(now)
        print(f"no existing pin — seeding all {len(targets)} rows")
    else:
        moved = [l for l in sort_labels(now) if pin["rows"].get(l) != now[l]]
        if rows_arg == "all":
            targets = moved
        else:
            targets = [r.strip() for r in rows_arg.split(",") if r.strip()]
            unknown = [r for r in targets if r not in now]
            if unknown:
                sys.exit(f"REFUSED: no such ledger row(s): {unknown}")
            still = [r for r in targets if r not in moved]
            if still:
                sys.exit(f"REFUSED: row(s) {still} have not moved since the pin — "
                         f"re-pinning them would record a reconciliation that did not happen.")
        if not targets:
            print("nothing to reconcile: no row has moved since the pin.")
            return 0

    merged = dict(pin["rows"]) if pin else {}
    for label in targets:
        merged[label] = now[label]
    for label in list(merged):
        if label not in now:
            del merged[label]

    commit, date = pin_target()
    block = L.render_pin(commit, date, sha256_file(STATE), merged, note,
                         " | ".join(L.ledger_columns(state_text)))

    if pin is None:
        twin_text = block + "\n" + twin_text
    else:
        i = twin_text.find(L.PIN_START)
        j = twin_text.find(L.PIN_END, i) + len(L.PIN_END)
        twin_text = twin_text[:i] + block + twin_text[j:]

    # The visible copy moves with the machine-readable one, ALWAYS — section 6 checks that
    # they agree, so leaving this to the caller would just relocate the drift into the
    # reconciliation step and fail the control on the next run.
    visible = (f'<span id="provenance"><b>Reconciled against</b> '
               f'<span class="q">STATE.md</span> @ {commit} ({date}) '
               f'&mdash; a pin, not a date</span>')
    twin_text, n_sub = _PROVENANCE.subn(lambda _m: visible, twin_text)
    if n_sub != 1:
        sys.exit(f'REFUSED: expected exactly one <span id="provenance">, found {n_sub}. '
                 f'Not writing — a half-updated provenance is worse than a stale one.')

    with open(TWIN, "w", encoding="utf-8") as fh:
        fh.write(twin_text)

    print(f"re-pinned {len(targets)} row(s) at {commit} ({date}): {' '.join(targets)}")
    print("NOTE: this records that the twin's cells for those rows WERE ACTUALLY UPDATED.")
    print("      If they were not, the pin is now a lie and the control will not say so.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--reconcile", action="store_true",
                    help="re-pin rows you have actually reconciled in the twin")
    ap.add_argument("--rows", default="",
                    help="comma-separated ledger rows to re-pin, or 'all'")
    ap.add_argument("--note", default="hand-maintained rendering; reconciled per row",
                    help="the note recorded in the pin block")
    ap.add_argument("--state", default=None, help="override the STATE.md path (tests)")
    ap.add_argument("--twin", default=None, help="override the twin path (tests)")
    ap.add_argument("--inflight", default=None,
                    help="override the IN-FLIGHT.json path (tests)")
    # `--root` EXISTS SO SECTIONS 7 AND 8 CAN BE PLANTED AGAINST A REAL GIT, NOT A FAKE ONE.
    # Both grade REACHABILITY, and reachability cannot be mutated by editing a file — so
    # negative_control.py builds a throwaway repository with a real `main` and runs this
    # instrument inside it.  It narrows nothing: it moves the WHOLE question, and a run
    # pointed at an empty directory answers `unknown` and grades nothing, which is louder
    # than a pass rather than quieter.
    ap.add_argument("--root", default=None,
                    help="override the repository root git is resolved against (tests)")
    args = ap.parse_args()

    # `--root` MOVES ALL THREE DEFAULTS WITH IT, and that is not tidiness.  `reconcile()`
    # reads the module globals, not these arguments, so a `--root` that repointed only git
    # would give this file two roots at once — resolving a pin against one repository while
    # digesting another's STATE.md.  That is mg-3902's defect exactly, re-created by the
    # option added to demonstrate it.
    global ROOT, STATE, TWIN, INFLIGHT
    if args.root:
        ROOT = os.path.abspath(args.root)
        STATE = os.path.join(ROOT, "STATE.md")
        TWIN = os.path.join(ROOT, "docs", "state-of-the-wall.html")
        INFLIGHT = os.path.join(ROOT, "code", "rendered_twin_pin_9bc2", "IN-FLIGHT.json")
    STATE = args.state or STATE
    TWIN = args.twin or TWIN
    INFLIGHT = args.inflight or INFLIGHT

    if args.reconcile:
        if not args.rows:
            sys.exit("--reconcile requires --rows: name the rows you reconciled, or 'all'")
        return reconcile(args.rows, args.note)

    state_text = open(STATE, encoding="utf-8").read()
    twin_text = open(TWIN, encoding="utf-8").read()
    code, lines = check(state_text, twin_text, sha256_file(STATE),
                        state_path=STATE, inflight_path=INFLIGHT)
    print("\n".join(lines))
    return code


if __name__ == "__main__":
    sys.exit(main())
