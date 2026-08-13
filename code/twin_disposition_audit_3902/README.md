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

### Reachability is now GRADED (mg-daba), and this file said the opposite for one run

It shipped as **reported and never graded**, on this argument: a polecat re-pinning on its own
branch legitimately names a commit that has not merged, and grading that would make the gate
red on every correct in-flight reconciliation — a red for a non-reason, shipped inside a remedy
for reds for non-reasons.

**The argument is right about in-flight commits and was applied one class too wide.** `c308368`
was not in flight on the branch that carried it; it was on **somebody else's** unmerged branch,
`origin/polecat-p0e8c`, which no merge would ever bring into `main`. Ungraded, that is a pin
whose referent is a branch nobody maintains. pm-onethird's acceptance criterion for all pinning
work is **main-ancestry AND byte-identity**, not byte-identity alone; the tie-break when they
conflict is **regenerate at the main-reachable commit**, never keep the orphan because its
bytes agree.

So the three worlds are separated instead of merged, and only the third is red:

| world | test | graded? |
|---|---|---|
| **integration** | an ancestor of `origin/main` (or `main`) | GREEN — both halves hold |
| **in flight** | an ancestor of *this* `HEAD` but of no integration ref | **reported, not graded** — the one legitimate way to name an unmerged commit, and still not acceptable: **the refinery rebases**, so this hash is rewritten out of existence when the branch lands. `2fbd5ce` died that way at mg-cdd5 |
| **orphan** | an ancestor of neither | **RED** — `c308368` exactly |
| *unknown* | no integration ref resolves in this checkout | reported, not graded — *"git cannot answer" is not "the answer is no"*, and this suite already reproduced that defect once (below) |

Telling in-flight from orphan does **not** need a human, which is what the original note
assumed. An ancestor of this `HEAD` is in flight *here*; an ancestor of neither is on somebody
else's branch or on none.

**Byte-identity does not rescue an orphan, and that is demonstrated rather than argued.**
`a3_negative_control.py` builds one with `git commit-tree` on the pinned commit's own tree: its
`STATE.md` hashes to the pin's digest *exactly*, and no ref points at it. One input, two
checkers — **this file as shipped calls it `CLEAN`, exit 0; as it now stands, `BROKEN`, exit
2.** (That fixture — used by `a3`'s sixth mutation and `a1`'s third row, which construct the
*same* object — is the only thing in this suite that writes anything: one loose, unreachable
object in `.git`, with fixed identity and dates so its hash is stable and it is created once
and thereafter found rather than rewritten. `git gc` prunes it. Nothing in the working tree is
touched.)

**THE COST, STATED RATHER THAN DISCOVERED LATER.** A branch that reconciles and pins its *own*
commit is `in flight` and green while it runs locally — and the refinery then **rebases it**,
which moves that commit and leaves the pin an `orphan`. So that branch now goes **RED at the
merge gate** where it previously merged silently and landed a dead pin. That is the intended
behaviour and it is the moment the falsehood is created, but it is a real new refusal on a real
workflow, and the remedy is the tie-break: **re-pin at a commit already reachable from
`origin/main`** — for a reconciliation that does not itself change `STATE.md`, that is
available, because the digest is unchanged by the twin-only edit.

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
| `a1_prerepair.py` | runs the false-pin inputs through `twin_pin.py` **as of `origin/main`** — the old checker is CLEAN on 3 of 3, the third being the orphan-but-byte-identical one |
| `a2_pin_resolves.py` | the control: does the pin resolve, name the revision it digests, and name one this repository integrates? |
| `a3_negative_control.py` | six ways the pin can lie, each caught and each expect string absent from the unmutated report; plus the classifier's four branches, including the two that must **not** grade |
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
