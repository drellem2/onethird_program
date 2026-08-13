#!/usr/bin/env python3
"""mg-3902 — does `docs/state-of-the-wall.html`'s pin RESOLVE against git?

THE ONE QUESTION mg-9bc2's SIX SECTIONS NEVER ASK.  The twin's pin block opens with

    THIS IS THE ONLY THING IN THIS FILE THAT SAYS WHICH `STATE.md` IT IS A RENDERING OF.

and then names a commit.  `code/rendered_twin_pin_9bc2/twin_pin.py` checks that pin six ways
and **not one of them asks git about that commit**:

  * section 3 compares the pin's `state-sha256` against the LIVE working-tree `STATE.md`;
  * section 6 compares the pin's `commit:` against the VISIBLE copy of the same string in
    the page header.

So the commit field is checked only against its own duplicate, and two copies of a string
agreeing with each other is consistency, not provenance.  Measured, not argued: setting BOTH
copies to `deadbee` — a commit that does not exist in this repository — leaves the mg-9bc2
control at `VERDICT: CLEAN`, exit 0.  That is `Generated 2026-07-19` in a new field: an
unfalsifiable provenance claim, shipped inside the instrument built to remove unfalsifiable
provenance claims.

AND IT WAS LIVE WHEN THIS WAS WRITTEN, not hypothetical.  The pin named `c308368`, which

  (a) is NOT reachable from `origin/main` — it exists only on the unmerged polecat branch
      `origin/polecat-p0e8c` and dies when that branch is pruned; and
  (b) carries a `STATE.md` whose sha256 is `3d8d56d0…`, while the pin records `118158cb…`,
      which is `STATE.md` at `b364767`, the commit that CARRIES the pin.

The cause is structural rather than a slip, and it is at `twin_pin.py`'s `reconcile()`: it
stamps `git rev-parse --short HEAD` while digesting the WORKING TREE.  Those are the same
tree only when `STATE.md` is clean — and a reconciliation is the case where it is not, since
the natural way to do one is to edit the `STATE.md` row, rewrite the twin's cell, and re-pin,
all in the commit about to be made.  Do that and the pin names the revision BEFORE the edit
and digests the revision AFTER it.  Every reconciliation that touches `STATE.md` produces it.

WHY THIS LIVES HERE AND NOT AS `twin_pin.py`'s SECTION 7.  Inside is where it belongs, and
mg-3902 wrote it there first, ran it, and backed it out — measured reasons, both of them:

  1. `code/control_audit_9876/a1_census.py` REFUSES an arm-shaped site that no registered arm
     claims, by design.  A section 7 plus its two negative-control arms adds 8 such sites, so
     `./build.sh` went to `GATE VERDICT: REFUSED`, exit 2 — which would block every merge
     request in this repository, not just this branch.  That is the census working.
  2. Registering them properly means 5 new entries in `lib9876.ARMS` AND 5 new probes in
     `a2_discriminate.py`, and those probes cannot run: `make_sandbox()` builds a temp tree
     with no `.git`, so the question this file asks has no answer inside it.  Making that
     sandbox a git repository is a change to mg-9876's instrument of about the size of this
     audit, in another ticket's directory.

So the check runs from here, wired into `build.sh` so that something actually runs it, and
FOLDING IT INTO SECTION 7 IS THE SUCCESSOR — filed, not forgotten.  The cost of the split is
honest and is the first thing a reader should know: this is a SECOND control over the same
pin, and a second copy of anything is what this whole lineage keeps being about.  It is a
second CHECKER, not a second CLAIM — it derives everything from the pin it reads and records
no provenance of its own — but a reader who finds them disagreeing should believe `twin_pin.py`
about rows and this file about commits, and should close the split rather than pick a side.

REACHABILITY IS NOW GRADED (mg-daba), AND THIS FILE SHIPPED THE OPPOSITE FOR ITS FIRST RUN.
As written above, reachability was REPORTED AND NEVER GRADED, on the argument that a polecat
re-pinning on its own branch legitimately names an unmerged commit.  That argument is sound
about IN-FLIGHT commits and was applied one class too wide.  `c308368` was not in flight on
this branch: it lived on SOMEBODY ELSE'S unmerged branch, `origin/polecat-p0e8c`, which no
merge would ever bring into `main`.  Ungraded, that is a pin whose referent is a branch nobody
is maintaining — and the acceptance criterion pm-onethird handed down for all pinning work is
that a pin must satisfy BOTH main-ancestry AND byte-identity, not byte-identity alone.

So the three cases are separated instead of merged, and only the third is graded:

  INTEGRATION  an ancestor of `origin/main` (or `main`) — the criterion is met.  GREEN.
  IN FLIGHT    not on an integration branch, but an ancestor of THIS `HEAD`: a reconciliation
               on the current branch that has not merged yet.  REPORTED, NOT GRADED — but it
               does NOT yet satisfy the criterion, and it says so, because THE REFINERY
               REBASES and the hash will be rewritten out of existence when the branch lands.
  ORPHAN       an ancestor of NEITHER.  This is `c308368` exactly, and it is RED.  A pin whose
               referent is reachable from nothing this repository integrates is a provenance
               claim that has already outlived its referent.

WHEN THE TWO HALVES CONFLICT, THIS FILE DOES NOT PICK ONE.  A pin can be byte-identical at an
orphan commit — `git commit-tree` on the pinned tree produces one on demand, and
`a3_negative_control.py` does exactly that rather than describing it.  The remedy is to
REGENERATE at the main-reachable commit, never to keep the orphan because its bytes agree.

EXIT CODES.  0 clean · 2 the pin states something false about git.  There is deliberately no
"1 = drift" grade here: drift is the normal condition of a hand-maintained rendering and
mg-9bc2's section 2 owns it.  A pin that names a revision it does not describe is never
normal.

    python3 code/twin_disposition_audit_3902/a2_pin_resolves.py
"""

import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
TWIN = os.path.join(ROOT, "docs", "state-of-the-wall.html")

PIN_START = "<!-- STATE-PIN v1"
PIN_END = "STATE-PIN end -->"

# The integration branches this repository actually merges to, most authoritative first.
# Reachability against these is GRADED — see `classify_reachability()` and the docstring.
INTEGRATION_REFS = ("origin/main", "main")


def parse_pin(text):
    """The pin's scalar fields.  Deliberately re-implemented rather than imported.

    Importing `lib9bc2.parse_pin` would make this control's answer depend on the parser
    belonging to the instrument it is auditing, and the whole point is to ask the question
    from outside.  If the two parsers ever disagree about what the pin says, that is itself a
    finding and this file is where it would surface.
    """
    i = text.find(PIN_START)
    if i < 0:
        return None
    j = text.find(PIN_END, i)
    if j < 0:
        return None
    fields = {}
    for line in text[i + len(PIN_START):j].split("\n"):
        m = re.match(r"\s*([a-z0-9-]+):\s*(.*?)\s*$", line)
        if m and m.group(1) != "row":
            fields[m.group(1)] = m.group(2)
    return fields


def git(*args, binary=False):
    proc = subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True)
    if binary:
        return proc.returncode, proc.stdout
    return proc.returncode, proc.stdout.decode("utf-8", "replace").strip()


def classify_reachability(full, integration_refs=INTEGRATION_REFS):
    """Which of the four worlds the named commit is in.  Returns (verdict, detail).

    `verdict` is one of `integration`, `in-flight`, `orphan`, `unknown`.  Only `orphan` is
    graded; see the module docstring for why the middle case is not.

    TAKING THE REFS AS AN ARGUMENT IS NOT GENERALITY FOR ITS OWN SAKE.  The `in-flight` branch
    is the escape hatch that keeps this grade off correct in-flight reconciliations, and an
    escape hatch nobody has watched open is the same unfalsifiable thing as a check nobody has
    watched fire.  There is no rot-proof fixture for it in a tree that equals `main` — an
    ancestor of HEAD that is not an ancestor of `main` exists only while a branch is unmerged
    — so `a3_negative_control.py` exercises it by passing a SUBSTITUTE integration ref instead
    of by waiting for the right day.

    `unknown` is separate from `orphan` on purpose, and the distinction is this file's own
    kept defect one turn later: GIT CANNOT ANSWER IS NOT THE ANSWER IS NO.  A checkout with no
    `main` and no `origin/main` — a shallow clone, an export, a fresh worktree of one branch —
    cannot be asked this question, and condemning a correct pin there is the S1/S2/S3 shape
    this suite already reproduced once.
    """
    resolved = [r for r in integration_refs
                if git("rev-parse", "--verify", "--quiet", r)[0] == 0]
    if not resolved:
        return "unknown", "no integration ref resolves in this checkout"
    for ref in resolved:
        if git("merge-base", "--is-ancestor", full, ref)[0] == 0:
            return "integration", ref

    rc_head, _ = git("rev-parse", "--verify", "--quiet", "HEAD")
    if rc_head != 0:
        return "unknown", "HEAD does not resolve, so 'on this branch' has no meaning here"
    rc_anc, _ = git("merge-base", "--is-ancestor", full, "HEAD")
    if rc_anc == 0:
        return "in-flight", "an ancestor of this HEAD but of no integration ref"
    return "orphan", "an ancestor of neither an integration ref nor this HEAD"


def report(twin_text):
    """Returns (exit_code, lines)."""
    out, worst = [], 0

    def emit(s=""):
        out.append(s)

    emit("=" * 86)
    emit("mg-3902 — does the rendered twin's pin RESOLVE against git?")
    emit(f"  twin : {os.path.relpath(TWIN, ROOT)}")
    emit("=" * 86)
    emit()

    pin = parse_pin(twin_text)
    if pin is None:
        emit("  FAIL  no STATE-PIN block — there is no provenance claim to resolve.")
        emit("        (mg-9bc2 section 1 owns this too; it is repeated rather than assumed,")
        emit("        because a control that presumes its input exists is not a control.)")
        emit()
        emit("=" * 86)
        emit("VERDICT: BROKEN — the twin names no STATE.md revision at all.")
        emit("=" * 86)
        return 2, out

    commit = pin.get("commit", "")
    pinned_sha = pin.get("state-sha256", "")
    emit(f"  pin commit    : {commit or '(absent)'}")
    emit(f"  pin sha256    : {pinned_sha or '(absent)'}")
    emit()

    # ------------------------------------------------------------------ availability
    # "GIT CANNOT ANSWER" IS NOT "THE ANSWER IS NO", and this control shipped with that
    # defect for exactly one run.  Its first version went straight to `rev-parse`, so a tree
    # with no repository — an export, a tarball, or mg-9876's `make_sandbox()` — produced
    # `that commit does not exist` and a red verdict about a pin that was correct.  That is
    # character-for-character mg-9876's own S1/S2/S3 (`ROOT was not a git repo and three arms
    # were condemned by one line`), written down in that directory's COVERAGE.md and then
    # reproduced by the next person to write an arm, which is mg-3902's own defect and is
    # kept in the record here rather than quietly fixed.
    rc, _ = git("rev-parse", "--git-dir")
    if rc != 0:
        emit(f"  no git repository at {ROOT}")
        emit("  REPORTED, NOT GRADED — this control resolves a pin against history and there")
        emit("        is none here.  It says nothing about whether the pin is right, and a")
        emit("        red for that reason would be a red for a non-reason.")
        emit()
        emit("=" * 86)
        emit("VERDICT: NOT APPLICABLE — no history to resolve the pin against.")
        emit("=" * 86)
        return 0, out

    if not commit:
        emit("  FAIL  the pin carries no `commit:` field, so it names no revision.")
        worst = 2
    else:
        # -------------------------------------------------------------- does it exist
        rc, full = git("rev-parse", "--verify", "--quiet", commit + "^{commit}")
        if rc != 0:
            emit("  FAIL  that commit DOES NOT EXIST in this repository.")
            emit("        The page names a STATE.md revision nobody can look at, which is")
            emit("        exactly as checkable as `Generated <date>` was.")
            worst = 2
        else:
            emit(f"  resolves to   : {full}")

            # ---------------------------------------------------------- does it match
            rc, blob = git("show", f"{full}:STATE.md", binary=True)
            if rc != 0:
                emit("  FAIL  that commit has no STATE.md, so it cannot be the revision this")
                emit("        page is a rendering of.")
                worst = 2
            else:
                there = hashlib.sha256(blob).hexdigest()
                emit(f"  STATE.md@commit sha256 : {there}")
                emit(f"  sha256 recorded in pin : {pinned_sha or '(absent)'}")
                if not pinned_sha:
                    emit("  FAIL  the pin records no digest, so the commit it names cannot be")
                    emit("        checked against anything.  Absence is not agreement.")
                    worst = 2
                elif there == pinned_sha:
                    emit("  PASS  the commit the page NAMES carries the STATE.md the page was")
                    emit("        DIGESTED against — the two provenance fields agree with git,")
                    emit("        not merely with each other.")
                else:
                    emit("  FAIL  THE PIN NAMES ONE REVISION AND DIGESTS ANOTHER.")
                    emit("        A reader who runs `git show <commit>:STATE.md` to check this")
                    emit("        rendering is handed a different file than the one the row")
                    emit("        digests were taken over.  Either re-pin, or correct")
                    emit("        `commit:` to the revision whose STATE.md hashes to the")
                    emit("        recorded digest.")
                    worst = 2

            # ------------------------------------------------ reachability (GRADED, mg-daba)
            # The three worlds are separated rather than merged, and only the third is red.
            # See the module docstring: "not on main" covers both a correct in-flight
            # reconciliation and a pin that has outlived its referent, and grading them alike
            # would be a red for a non-reason shipped inside a remedy for red-for-a-non-reason
            # — which is why this file shipped ungraded first.  Telling them apart does not
            # need a human: an ancestor of THIS HEAD is in flight HERE, and an ancestor of
            # neither is on somebody else's branch or on none.  `c308368` was the latter.
            emit()
            for ref in INTEGRATION_REFS:
                rc_ref, _ = git("rev-parse", "--verify", "--quiet", ref)
                if rc_ref != 0:
                    emit(f"  reachable from {ref:<12}: (no such ref in this checkout)")
                    continue
                rc_anc, _ = git("merge-base", "--is-ancestor", full, ref)
                emit(f"  reachable from {ref:<12}: {'yes' if rc_anc == 0 else 'NO'}")

            verdict, detail = classify_reachability(full)
            emit()
            if verdict == "integration":
                emit(f"  PASS  the pinned commit is an ancestor of `{detail}`.  BOTH halves of")
                emit("        the acceptance criterion hold: main-ancestry AND byte-identity.")
            elif verdict == "in-flight":
                emit("  IN FLIGHT — REPORTED, NOT GRADED, AND NOT YET ACCEPTABLE.")
                emit(f"        The pinned commit is {detail}, i.e. a reconciliation on this")
                emit("        branch that has not merged.  That is the one legitimate way to")
                emit("        name an unmerged commit and it is why this is not red.  It is")
                emit("        also not done: THE REFINERY REBASES, so this hash is rewritten")
                emit("        out of existence when the branch lands and the pin becomes an")
                emit("        ORPHAN below.  `2fbd5ce` died that way at mg-cdd5.  Re-pin at a")
                emit("        main-reachable commit before merging.")
            elif verdict == "unknown":
                emit(f"  REPORTED, NOT GRADED — {detail}.")
                emit("        Git cannot answer this question here, and 'cannot answer' is not")
                emit("        'the answer is no'.  A red for that reason would condemn a pin")
                emit("        this checkout is simply unable to check.")
            else:
                emit("  FAIL  THE PINNED COMMIT IS REACHABLE FROM NOTHING THIS REPOSITORY INTEGRATES.")
                emit("        It is an ancestor of no integration ref and of no")
                emit("        commit on this branch either, so it lives on somebody else's")
                emit("        unmerged branch — or on none at all — and no merge will ever")
                emit("        bring it into `main`.  `c308368` was exactly this: reachable")
                emit("        only from `origin/polecat-p0e8c`, a branch nobody maintains.")
                emit("        BYTE-IDENTITY DOES NOT RESCUE IT.  A pin can hash correctly at")
                emit("        an orphan commit; that makes the claim reproducible for exactly")
                emit("        as long as the object survives.  REGENERATE the pin at the")
                emit("        main-reachable commit rather than keeping this one.")
                worst = 2

    emit()
    emit("=" * 86)
    emit({0: "VERDICT: CLEAN — the pin resolves, names the revision it digests, and that "
             "revision is one this repository integrates.",
          2: "VERDICT: BROKEN — the pin states something false about git."}[worst])
    emit("=" * 86)
    return worst, out


def main():
    if not os.path.exists(TWIN):
        print(f"no twin at {TWIN} — nothing to check")
        return 0
    with open(TWIN, encoding="utf-8") as fh:
        code, lines = report(fh.read())
    print("\n".join(lines))
    return code


if __name__ == "__main__":
    sys.exit(main())
