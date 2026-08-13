# mg-3902 — does the rendered twin's pin RESOLVE against git?

The audit this directory belongs to is
`docs/audit-mg-3902-the-twin-disposition-and-its-pin.md`. Read that for the finding; this
file is how to run the check and what its verdict does and does not mean.

```sh
sh code/twin_disposition_audit_3902/run_all.sh     # also runs from ./build.sh
```

## The one question `twin_pin.py`'s six sections never ask

`docs/state-of-the-wall.html` opens with a pin block whose own header says:

    THIS IS THE ONLY THING IN THIS FILE THAT SAYS WHICH `STATE.md` IT IS A RENDERING OF.

`code/rendered_twin_pin_9bc2/twin_pin.py` checks that pin six ways and **not one of them asks
git about the commit it names.** Section 3 compares the pinned `state-sha256` against the
**live working tree**; section 6 compares the pinned `commit:` against **the visible copy of
itself** in the page header. Two copies of a string agreeing with each other is consistency,
not provenance.

**Measured:** setting both copies to `deadbee` — a commit that does not exist in this
repository — leaves that control at `VERDICT: CLEAN`, **exit 0**.

**And it was not hypothetical.** At `origin/main` on 2026-08-13 the pin named `c308368`,
which is not reachable from `origin/main` (it lives only on `origin/polecat-p0e8c`) and whose
`STATE.md` hashes to `3d8d56d0…` against the pin's recorded `118158cb…`. This suite was
**RED against `main` on the day it was written**.

## What a green here means, and what it does not

| it does mean | it does NOT mean |
|---|---|
| the pinned commit exists and carries a `STATE.md` | that the twin's cells are faithful summaries — `COVERAGE.md` §1 owns that, and nothing checks it |
| that `STATE.md` hashes to the digest the pin records | that no ledger row has drifted — `twin_pin.py` section 2 owns that |
| the page's provenance claim is checkable and true | that the page's **prose** matches `STATE.md` — nothing covers that either |

Reachability from `origin/main` is **reported and never graded**. A polecat re-pinning on its
own branch legitimately names a commit that has not merged yet, and grading that would make
the gate red on every correct in-flight reconciliation — a red for a non-reason, shipped
inside a remedy for reds for non-reasons. It is printed loudly anyway, because **the refinery
rebases**: a pin written against an unmerged commit is rewritten out of existence when the
branch lands. `2fbd5ce` died that way at mg-cdd5; `c308368` was dying that way when this was
written.

## The root cause, which this suite detects but does not fix

`twin_pin.py`'s `reconcile()` stamps `git rev-parse --short HEAD` while digesting the
**working tree**. Those are the same tree only while `STATE.md` is clean — and a
reconciliation is the case where it is not, since the natural way to do one is to edit the
`STATE.md` row, rewrite the twin's cell and re-pin in the commit about to be made. The pin
then names the revision *before* the edit and digests the revision *after* it.

**The fix belongs in `reconcile()`** — refuse to re-pin while `STATE.md` on disk differs from
`STATE.md` at `HEAD`, so the commit named and the bytes digested are the same revision. It
was written and demonstrated (the refusal holds and the twin is not written) and then backed
out with the rest of the in-place change, for the reason below.

## Why this is a separate suite and not `twin_pin.py`'s section 7

Inside is where it belongs. It was written there first, run, and backed out — two measured
reasons:

1. `code/control_audit_9876/a1_census.py` refuses an arm-shaped site that no registered arm
   claims. A section 7 plus its two negative-control arms adds 8 such sites, and `./build.sh`
   went to `GATE VERDICT: REFUSED`, **exit 2** — blocking every merge request in the
   repository, not just this branch. That is the census working.
2. Registering them needs 5 entries in `lib9876.ARMS` **and 5 probes** in
   `a2_discriminate.py`, and those probes cannot run: `make_sandbox()` builds a tree with no
   `.git`, so the question has no answer inside it.

**The cost is real and is not laundered:** this is a second control over the same pin.
Folding it into section 7 — and giving mg-9876's sandbox real history so the probes can be
written — is the filed successor.

## Files

| file | what it is |
|---|---|
| `PREDICTIONS.md` | filed at `fe7790a`, before any file under audit was opened, with the exposure disclosed |
| `a1_prerepair.py` | runs both section-7 inputs through `twin_pin.py` **as of `origin/main`** — the old checker was CLEAN on 2 of 2 |
| `a2_pin_resolves.py` | the control: does the pin resolve, and does it name the revision it digests? |
| `a3_negative_control.py` | five ways the pin can lie; each must be caught, each expect string absent from the unmutated report |
| `run_all.sh` | the runner, with the three guards this lineage's runners kept failing (no pipe, verdict-line required, unknown exit refused) |

## The instrument's own defect, kept

The first version of the control called `git rev-parse` without asking whether there *was* a
repository, so a tree with no `.git` produced *"that commit does not exist"* and a red verdict
about a correct pin. `a1_prerepair.py` was the first caller to hit it and **refused rather
than printing a table**, which is the harness working.

It is character-for-character mg-9876's `S1`/`S2`/`S3` — *"`ROOT` was not a git repo and three
arms were condemned by one line"* — written down in that directory's `COVERAGE.md` and then
reproduced by the next person to write an arm. **"Git cannot answer" is not "the answer is
no"**, and it has to be built in: reading that it exists did not stop it being written again.
