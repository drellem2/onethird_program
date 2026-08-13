# mg-3902 — INDEPENDENT AUDIT of the `docs/state-of-the-wall.html` disposition

**Subject:** mg-9bc2's decision to KEEP the rendered twin and pin it per ledger row, plus the
four reconciliations that have landed on top of it (mg-2f44, mg-9876, mg-188d, mg-cdd5,
mg-0e8c, mg-28b6).
**Auditor:** mg-3902. **Predictions filed before any file under audit was opened:**
`code/twin_disposition_audit_3902/PREDICTIONS.md`, committed at `fe7790a`.

---

## THE HEADLINE, WHICH IS NOT WHAT THE TICKET ASKED FOR

**The page's provenance pin named a commit that does not carry the `STATE.md` the pin
digests, and nothing in this repository could have said so.**

At `origin/main` this morning the pin block at the top of `docs/state-of-the-wall.html` read:

    commit: c308368
    state-sha256: 118158cb98ac41a2a6a097e1b833390413653c9d172df84aab59bd0e5bae17b6

Both fields are false together in two independent ways, and neither is a typo:

| what the pin claims | what git says |
|---|---|
| `STATE.md` at `c308368` hashes to `118158cb…` | it hashes to **`3d8d56d0…`**. `118158cb…` is `STATE.md` at **`b364767`** — the commit that *carries the pin* |
| `c308368` is the revision this page renders | `c308368` is **not reachable from `origin/main`**. It exists only on `origin/polecat-p0e8c`, an unmerged polecat branch, and dies when that branch is pruned |

A reader who does the one thing the pin block's own header tells them to do —
*"THIS IS THE ONLY THING IN THIS FILE THAT SAYS WHICH `STATE.md` IT IS A RENDERING OF"* — and
runs `git show c308368:STATE.md` is handed a different file than the one the twelve row
digests were taken over. On a fresh clone of `main` they are handed nothing at all.

**This is the ticket's own defect class, one field along.** `Generated 2026-07-19` was a
provenance claim nobody could check. mg-9bc2 replaced it with a provenance claim nobody
*does* check: sections 1–6 of `twin_pin.py` never ask git a single question about `commit:`.
Section 3 compares the pinned digest against the **live working tree**; section 6 compares
the pinned commit against **the visible copy of itself** in the page header. Two copies of a
string agreeing with each other is consistency, not provenance.

**Demonstrated, not argued.** Setting the pin *and* its visible duplicate to `deadbee` — a
commit that does not exist in this repository — leaves `twin_pin.py` at
`VERDICT: CLEAN`, **exit 0**.

### The cause is structural, not a slip

`twin_pin.py`'s `reconcile()`:

```python
commit = git rev-parse --short HEAD          # the commit BEFORE the re-pin lands
...
block  = L.render_pin(commit, date, sha256_file(STATE), ...)   # the WORKING TREE's digest
```

Those describe the same tree only while `STATE.md` is clean — and **a reconciliation is
exactly the case where it is not**, because the natural way to do one is to edit the
`STATE.md` row, rewrite the twin's cell and re-pin, all in the commit about to be made. Do
that and the pin names the revision *before* the edit while recording the digest of the
revision *after* it. mg-0e8c's `b364767` did precisely this.

Swept over every pin this file has ever carried on `main`:

| carrying commit | pin names | on main? | digest matches named commit? |
|---|---|---|---|
| `9efb3df` (mg-9bc2, seed) | `276aead1a8c5` | yes | **yes** |
| `4fcbc71` (mg-2f44) | `276aead1a8c5` | yes | **yes** |
| `bc965aa`, `cdec2e8` (mg-9876) | `4fcbc71` | yes | **yes** |
| `fe19d13` (mg-188d) | `9dc53a6` | yes | **yes** |
| `7e7bfb7` (mg-cdd5) | `4ce7da3` | yes | **NO** |
| `b364767`, `af09a58` (mg-0e8c, mg-28b6) | `c308368` | **NO** | **NO** |

The mechanism was **sound for its first four re-pins** — those tickets edited the twin only,
so working tree and `HEAD` agreed. It broke the first time a ticket edited `STATE.md` and
re-pinned together.

**And the first break was caused by a repair.** `7e7bfb7`'s subject is *"twin: point the pin
at the commit that survives the rebase — 2fbd5ce did not exist after it (mg-cdd5)"*. mg-cdd5
correctly noticed the pinned commit had been rebased out of existence and repointed
`commit:` at a surviving revision **without re-deriving `state-sha256`**. Before that fix the
pin was *correct and unreachable*; after it, *reachable and wrong*. That is worth stating
plainly because it is the more instructive half: the refinery rebases every polecat branch,
so **any pin written against a not-yet-merged commit is guaranteed to rot**, and the obvious
repair trades one false field for another.

---

## CORRECTING THE FRAMING — MY TICKET'S AND pm-onethird's

The ticket instructs: *"CORRECT THE PARENT'S FRAMING AND MINE."* Four corrections, in
descending order of how much they changed the work.

**1. My ticket's binary is wrong, and the parent was right to refuse it.** mg-3902 offers
`IF REGENERATED` and `IF DELETED` and tells the auditor to pick a branch. mg-9bc2 chose
**neither**: it kept the file and pinned it per ledger row. Deliverables 1–3 and 4–5 are
written for two worlds, and the actual world is a third that is better than both. An auditor
who filed under `IF REGENERATED` and graded the pin as a half-hearted regeneration would be
scoring the parent against a menu it was correct to walk away from. *(P1, confirmed.)*

**2. My ticket's `4,658 words` premise is stale by 4.58×, and the error reverses the
recommendation it is offered in support of.** Deliverable 6 asks me to decide whether the
file should exist *"given STATE.md is now 4,658 words"*. Measured at `HEAD` today:

    STATE.md: 221 lines, 21,328 words, 138,345 bytes

mg-9bc2 already refuted this in July at 16,861 words. It has grown a further 26% since.
The premise does not merely fail — **it points the opposite way**: the readability problem
the page exists to solve is larger now than when the page was made. *(P2, confirmed.)*

**3. `Generated` is present in the file, and that is correct.** Deliverable 3 says to confirm
the word *"no longer appears unless it is true."* It appears once, at line 245, inside the
lede that repudiates it:

> **⚠️ THIS PAGE IS HAND-MAINTAINED, NOT GENERATED, AND IT IS STALE IN PLACES.** It read
> *"Generated 2026-07-19"* for three weeks, and that was false in both halves. **No generator
> has ever existed** (mg-9bc2) …

That is use versus mention, and `twin_pin.py`'s section 5 handles it deliberately: a banned
string inside `<i>` or `<s>` is treated as a quotation, a bypass that `COVERAGE.md` §3
declares rather than hides. The finding the ticket anticipated — *"if the parent reported
there is no generator and the file was hand-built, that is the headline"* — **was already
made by the parent**, is `README.md`'s FINDING 1, and is the first sentence a reader of the
page sees. It is not a discovery of mine, and I scored it a report at zero credit before
starting. *(P6, confirmed in the letter; the deliverable it serves is satisfied.)*

**4. The recurrence note in my own ticket is accurate but incomplete in a way that matters.**
It records that `docs/state-of-the-wall.html` has had "the *same* defect found twice by two
different routes" and that both sightings landed inside the region
`code/rendered_twin_pin_9bc2/COVERAGE.md` **declares uncovered**. True. What it does not say
is that the declared-uncovered region is *prose*, and the defect I found is in the **pin
block itself** — the covered region, the part with a control over it. So this is not a third
instance of "the known gap swallowed another one." It is the first instance of the *checked*
half being wrong, and it survived four reconciliations and a merge gate.

---

## THE DELIVERABLES

### 2 — MAKE THE STALENESS CHECK FAIL ✅

Four mutations, each applied to a copy, each with its setup asserted before the result was
read. Full transcript in `code/twin_disposition_audit_3902/`.

| # | mutation | result |
|---|---|---|
| A | one line of a **pinned ledger row** (row 8: `2×10⁻²` → `9×10⁻⁹`) | **RED.** exit 1, `row 8 MOVED`, worklist exactly `8` |
| B | one line of `STATE.md` **prose** outside the ledger table (line 21) | GREEN, exit 0 |
| C | a **false claim planted in the twin's prose** — *"L1b IS NOW PROVEN and the wall has fallen"* | GREEN, exit 0 |
| D | pin **and** visible line both set to `deadbee`, a commit that does not exist | GREEN, exit 0 |

**A is the check working.** It fails correctly, names the row, and hands back a worklist.

**B and C are the check's declared scope, and they are correct behaviour** — `COVERAGE.md` §2
says only the ledger table is digested. I report them because *"the staleness check passes"*
is meaningless without its scope, and C is worth seeing: a reader can be told the wall has
fallen and every control in this repository stays green.

**D is the finding.** It is *not* a declared limitation. Nothing in `COVERAGE.md` says the
`commit:` field is unchecked; the pin block's header implies the opposite.

*(P3 confirmed. P4 confirmed — I predicted a mutation into the declared blind region would
pass silently, and B and C are that. I did not predict D would be outside the declared
scope; I expected everything I found to be already written down.)*

**One mutation was a no-op and I nearly reported it as a result.** My first attempt at B
targeted the wrong line and the `replace` matched nothing; the run printed `CLEAN` and I was
one step from recording "the control did not see it." The before/after print showed the two
strings identical. Every subsequent mutation asserts its own setup. This is exactly
`negative_control.py`'s `SETUP FAILED` discipline, and I had to rediscover it by tripping
over it.

### 1 — DOES THE HTML MATCH `STATE.md` AT THE COMMIT THE HTML NAMES? ❌ **NO**

This is the deliverable the ticket calls *"the whole point"*, and the answer is the headline
above. The ticket's suspicion was aimed one step off: it warns against checking at `HEAD` or
at *"the commit that carries the HTML if those differ."* In fact **the digest is correct at
the commit that carries the HTML**, and it is the **named commit** that is wrong. The
displacement is real; its direction is the reverse of the one anticipated.

*(P5 scored a partial MISS. I predicted the page would name more than one commit — one per
row — so that "the commit the HTML names" would be ill-defined. It names exactly one, plus
twelve content digests, so the question is well-posed and has a single wrong answer. The
second half of P5 — that a pin would point at a commit not on `main` — is confirmed twice
over, at `2fbd5ce` and at `c308368`.)*

### 6 — WAS THE RECOMMENDATION ARGUED? ✅ **YES, AND BETTER THAN THE TICKET ASKED FOR**

`code/rendered_twin_pin_9bc2/README.md` argues **KEEP, pinned** in three numbered reasons —
the purpose the ticket assumed was gone is not gone; deletion is not the cheap side of the
trade (the maintenance cost is *measured*, 2 of 12 rows, not estimated); and the failure mode
being removed is the unfalsifiable claim, not the file.

It also does the thing that is rarer and worth more: **it states in advance what would
reverse it.**

> **What would change the recommendation:** if the reconciliation debt is not paid down — if
> a later run reports more drifted rows than this one's two — the twin is being carried
> rather than maintained, and deleting it becomes the better call.

**That condition has now been tested and the recommendation survives.** A later run reports
**zero** drifted rows, not more than two. The debt was paid by mg-2f44 (row 9) and mg-188d
(row 8). The keep decision is in better standing today than when it was made.

*(P7 confirmed on its first half and MISSED on its second: I predicted the argument would
have gone stale in its own way. Its numbers moved — `STATE.md` is 21,328 words, not the
16,861 the README quotes — but the falsification condition was written in a form that does
not rot, and it passed. A stated reversal condition that survives a real test is the
strongest thing in this directory.)*

### 4 and 5 — the `IF DELETED` branch

Not applicable, but deliverable 5's reasoning cuts the other way and my pre-registered
reversal condition 3 required me to say so:

**`STATE.md:7` is a live markdown link to this file**, in the first seven lines of the
canonical document:

    Rich rendered version: [`docs/state-of-the-wall.html`](docs/state-of-the-wall.html) …

52 files reference the page by name. Most are prose mentions in audit documents, which a
deletion would leave as stale references rather than broken links — but `STATE.md:7` is a
real link, and deleting the file would have put a 404 at the top of the programme's entry
point. **That is evidence for the keep decision independent of any readability argument, and
it is evidence my own ticket's structure would have hidden**, because it only asked for the
link sweep under `IF DELETED`.

---

## WHAT I CHANGED

**1. The pin now names a commit that carries the `STATE.md` it digests.**
`c308368` → `b364767` in both copies (the machine-readable pin and the visible provenance
line). `b364767` is on `origin/main` and its `STATE.md` hashes to `118158cb…`, exactly the
recorded digest. **No row digest moved and no row was re-pinned** — `COVERAGE.md` §4 names a
re-pin that records a reconciliation which did not happen as *"the single easiest way to
defeat the whole mechanism"*, and correcting a false field is not that. `twin_pin.py` is
byte-for-byte as green after as before.

**2. A new suite, `code/twin_disposition_audit_3902/`, wired into `build.sh` as its eighth
looped suite**, asking the question sections 1–6 never ask: does the pin resolve against git?
It grades two things and reports a third:

- the named commit **exists** and carries a `STATE.md` → else structural;
- that `STATE.md` **hashes to the recorded digest** → else structural;
- whether the commit is **reachable from `origin/main`** → **reported, never graded**.

The asymmetry is deliberate. A polecat re-pinning on its own branch legitimately names an
unmerged commit; grading that would make the gate red on every correct in-flight
reconciliation, which would be a red for a non-reason shipped inside a remedy for reds for
non-reasons. It is printed loudly because the refinery rebases and the hash will not survive.

> **SUPERSEDED at mg-daba — the third bullet is now GRADED, and the paragraph under it is
> right about a narrower class than it claims.** The in-flight case is real, but `c308368` was
> not it: an ancestor of no integration ref *and of no commit on the branch that carried the
> pin* is on somebody else's unmerged branch, and no human is needed to tell the two apart.
> `a2_pin_resolves.py` now separates **integration** (green) from **in flight** (reported) from
> **orphan** (red), and `a3_negative_control.py` reaches all four branches of that classifier
> — including the two that must not grade — on derived inputs. See §*A pin can be
> byte-identical and still false* below.

**It was RED against `origin/main` on the day it was written** — exit 2, naming both halves
of the `c308368` defect. A check that earns its place on the merge critical path by failing
is worth more than one that arrives green.

**It has been shown to fail, six ways** (`a3_negative_control.py`, 6 of 6 caught): pin at a
real-but-wrong commit; pin at a nonexistent commit; `commit:` deleted; `state-sha256` deleted;
whole pin block removed; and — added at mg-daba — **pin at an orphan commit whose `STATE.md`
is byte-identical to the recorded digest**. Each expect string is checked against the
*unmutated* report first — mg-9876's guard — so no row can be satisfied by a string the report
prints anyway.

---

## mg-daba — A PIN CAN BE BYTE-IDENTICAL AND STILL FALSE, AND THIS ONE IS NEITHER

**The pair on `main` is TRUE, and that is a measurement, not a reprieve.** mg-daba was filed to
re-pin the twin to a true pair on the strength of `commit: c308368 / state-sha256: 118158cb…`.
That pair no longer exists: `7eb561e` — the commit that landed *this* audit — repointed
`commit:` to `b364767`, and everything checkable about the result now holds.

| field | check | result |
|---|---|---|
| `commit: b364767` | `git merge-base --is-ancestor b364767 origin/main` | **ancestor** |
| `state-sha256: 118158cb…` | sha256 of `git show b364767:STATE.md` | **118158cb…**, identical |
| `commit-date: 2026-08-13` | `b364767`'s committer date | **2026-08-13** |
| 12 row digests | recomputed over `STATE.md` **at `b364767`**, not the working tree | **12 of 12 match**, columns identical |
| visible header line | `twin_pin.py` §6 | names `b364767` and no other |
| the other 5 commits the page names in prose | `21ee93f 25cc5b2 491d42c 6cd5b1d 9dc53a6` | all exist, all ancestors of `origin/main` |

So **no re-pin was made**, and that is the finding rather than the absence of one. Re-pinning a
correct pin writes a reconciliation that did not happen, which `COVERAGE.md` §4 calls *"the
single easiest way to defeat the whole mechanism"*. The row digests were taken over
`STATE.md@b364767`; moving them to today's `STATE.md` to make the whole-file digest agree would
have destroyed the drift signal §2 exists to carry.

**Which pair was wrong, and which repair made it wrong.** `mg-cdd5` repointed a rebased-away
commit without re-deriving the digest, trading *correct-and-unreachable* for
*reachable-and-wrong*. `7eb561e` then moved `commit:` to the revision whose `STATE.md` hashes to
the recorded digest — the opposite direction from this ticket's requirement (1), and the right
one, because it is the direction that leaves the row digests describing the thing they were
taken over.

**What was actually owed here was the check, not the data.** A pin verified by hand and written
up in prose is a provenance claim nobody can re-run — which is the exact defect this lineage
exists to remove, one document along. So the table above is reproducible:
`code/twin_disposition_audit_3902/run_all.sh`, and it goes **red** if any row of it stops being
true.

**The gap that made this ticket necessary is closed at the acceptance criterion, not at the
data.** Byte-identity alone cannot see an orphan: `git commit-tree` on the pinned commit's own
tree yields a commit whose `STATE.md` hashes to the pin's digest *exactly* and which no ref
reaches. Run against that twin, **the checker as mg-3902 shipped it reports `CLEAN`, exit 0;
with reachability graded it reports `BROKEN`, exit 2** — same input, same repository, two
checkers. That is now `a3`'s sixth mutation and `a1`'s third row.

**The `deadbee` acceptance test, run on the file rather than reasoned about.** Both copies of
the commit set to a revision that does not exist:

| what was run | result |
|---|---|
| `twin_pin.py` — sections 1–6, **unchanged by mg-daba** | `VERDICT: CLEAN`, **exit 0** |
| `code/twin_disposition_audit_3902/run_all.sh` — gated by `build.sh` | `VERDICT: BROKEN`, **exit 2** |

**So the acceptance test passes at the GATE and still fails inside the INSTRUMENT**, and the
distinction is not cosmetic: anyone running `twin_pin.py` directly — which is what its own pin
block tells the reader to do — is still told `CLEAN` about a pin naming a commit that does not
exist. Closing that is `mg-7cc3`'s section 7 and nothing here substitutes for it.

Credit where it is owed: `deadbee` going red at the gate is **mg-3902's**, not this ticket's —
the nonexistent-commit mutation was in the suite as landed. What mg-daba adds is the case that
was red in *neither* column, because it is false about ancestry while being true about every
byte: the orphan.

**Still not done, and still owned by `mg-7cc3`:** the writer. `twin_pin.py`'s `reconcile()`
stamps `git rev-parse --short HEAD` while digesting the **working tree**, so the next
reconciliation that also edits `STATE.md` produces a false pair again — caught now at the gate
instead of silently, which is an improvement and not a fix.

---

## WHAT I DID NOT DO — and the largest item is a decision, not an omission

**I did not land this as `twin_pin.py`'s section 7, which is where it belongs.** I wrote it
there first, ran it, and backed it out. Two measured reasons:

1. `code/control_audit_9876/a1_census.py` **refuses** an arm-shaped site that no registered
   arm claims — by design, and its own P5 probe exists to prove it does. A section 7 plus two
   negative-control arms adds 8 such sites, and `./build.sh` went to
   `GATE VERDICT: REFUSED`, **exit 2 — measured, not predicted**. That would have blocked
   every merge request in this repository, not only this branch.
2. Registering them properly needs 5 entries in `lib9876.ARMS` **and 5 new probes** in
   `a2_discriminate.py` — and those probes cannot run as that suite is built:
   `make_sandbox()` creates a temp tree with no `.git`, so the question has no answer inside
   it. Giving that sandbox real history is a change to mg-9876's instrument of about the size
   of this audit, in another ticket's directory, on a programme Daniel has parked.

I got as far as a working section 7 with both arms caught (18 of 18), the census re-registered
to 55 arms and complete, and `a2` reporting `NO PROBE 5`. The remaining gap is the five
probes. **The cost of my choice is real and is not laundered: this is a SECOND control over
the same pin, and a second copy of anything is what this whole lineage keeps being about.**
It is a second *checker*, not a second *claim* — it derives everything from the pin it reads
and records no provenance of its own — but a reader who finds the two disagreeing should
close the split rather than pick a side. **Filed as the successor.**

Also not done:

- **I did not check whether any unmoved row is faithfully summarised.** `COVERAGE.md` §1
  calls this "the big one" and it remains the biggest uncovered thing about this page. My
  mutation C shows the shape of what could hide there.
- **I did not read the twin's seven prose sections against `STATE.md`.** Nothing does. That
  region is where mg-957a's and mg-28b6's findings both landed.
- **I did not re-audit the twelve row digests** for whether the cells they authorise are
  *right*; I checked that the pin's provenance is true, which is strictly less.
- **I did not verify the `c308368` blob after `origin/polecat-p0e8c` is pruned.** My
  measurement that it resolves today depends on that branch still existing. After it is
  deleted the pin would have named a commit that resolves nowhere — which is the stronger
  form of the same finding and I could not wait for it.
- **I took no measurement of whether anyone reads this page.** I can measure whether it is
  accurate. Usefulness is not something I have an instrument for, and I said so in advance.

---

## PREDICTIONS, SCORED

Filed at `fe7790a` before any file under audit was opened. R1–R3 were declared **reports at
zero credit** — this repository's commit subjects carry conclusions, and reading
`git log -- docs/state-of-the-wall.html` told me the disposition before I filed a bet. They
are excluded from the score.

| # | bet | outcome |
|---|---|---|
| P1 | my ticket's binary framing is the primary defect | **CONFIRMED** |
| P2 | `4,658 words` is stale by ~4.5× and reverses the recommendation | **CONFIRMED** (21,328; 4.58×) |
| P3 | the check goes red on a pinned-row mutation | **CONFIRMED** (exit 1, worklist `8`) |
| P4 | the check has a declared blind region and passes a mutation into it | **CONFIRMED** (B and C) |
| P5 | the page names more than one commit, so "the" commit is ill-defined | **MISS** on the first half, confirmed on the second (a pin off `main`, twice) |
| P6 | `Generated` still appears | **CONFIRMED**, and correctly so |
| P7 | the recommendation was argued; the argument has since gone stale | **CONFIRMED** / **MISS** — its numbers moved, its reversal condition did not, and it passed |
| P8 | the staleness fix has itself gone stale | **MISS** on the half I named, **CONFIRMED** in a form I did not |

**8 live bets, 5 clean confirmations, 1 clean miss, 2 split.** The two splits are where the
information is, and P8 is the one worth reading.

**P8 predicted the committed transcripts would be stale** against the tree they describe,
reasoning from mg-c824's "40 of 98 transcripts ALREADY STALE" days earlier. **Measured:
`code/rendered_twin_pin_9bc2/out_control.txt` is byte-identical to a live run.** mg-f771's
fixed-point gate keeps it that way, and the mechanism I bet against works. But the *class* I
was aiming at — the staleness fix having itself gone stale — was live the whole time, one
field to the left of where I looked: not the transcript, the **pin**. I would have scored P8
a miss and moved on if the transcript check had been the only thing I ran.

## A DEFECT OF MY OWN, KEPT

My first section 7 called `git rev-parse` without first asking whether there *was* a
repository, so a tree with no `.git` produced *"that commit does not exist"* and a structural
failure about a pin that was perfectly correct. My own `a1_prerepair.py` was the first caller
to hit it, and it refused rather than printing a table — the harness working.

It is character-for-character mg-9876's `S1`/`S2`/`S3`: *"imported `seed_pin` from the
sandbox so `ROOT` was not a git repo and three arms were condemned by one line"* — written
down in `COVERAGE.md`, and reproduced by the next person to add an arm to that directory.
Both halves are repaired: the control now reports-without-grading when git cannot answer, and
the harness stages under `code/` so that git can. **"Git cannot answer" is not "the answer is
no"**, and the distinction has to be built in, because reading that it exists did not stop me
writing it again.
