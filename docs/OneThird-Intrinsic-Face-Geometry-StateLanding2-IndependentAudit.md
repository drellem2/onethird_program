# Independent audit of `db08b4c` (mg-1319 — the mg-5630 landing)

**Auditor:** mg-f7bc (pre-filed, per Appendix A's pre-file rule).
**Target:** `db08b4c`, derived from the parent's merge commit as the derive-from-merge-commit rule requires.
**Scope:** `STATE.md`, `code/face_geometry/controls.py`, `code/face_geometry/controls_output.txt`,
`docs/OneThird-Intrinsic-Face-Geometry-Probe.md` (4 files, +287/−51).

---

## VERDICT: **OVERSTATED**

**0 BROKEN mathematics.** Every number the commit adds reproduced independently; the one claim it
upgraded from a count to a theorem (A6) I re-derived and confirmed on a larger population than it
cites, *including two side conditions its proof sketch does not state and needs*. The scoring repair
(A4) is real, it changes behaviour, and I could not make it lie. The reopening (A1) is complete at
every live site and did **not** over-correct.

**What is overstated is, again, the commit's description of its own repair** — three statements, at
three locations nobody was watching, two of them sentences the commit wrote about its own method:

| # | Finding | Severity |
|---|---|---|
| **F1** | `A8`'s *"the truncation flagged at every site where `38/38` appears"* is **FALSE**; `Probe.md:798` quotes it unflagged, inside the very block this commit chose to patch inline. `STATE.md:264` repeats the claim. | **OVER-WIDE, and it is a claim about this commit's own coverage** |
| **F2** | `Probe.md:132–140` — the sentence mg-5630 **indexed as F3** — still reads *"the mg-e0ce audit closed it to `n ≤ 6`"* for the Lemma-1 cross-check. Untouched by the diff, while the commit's own changelog (`Probe.md:37`) says *"the `n ≤ 6` half of F3's coverage sentence corrected"*. | **A2 IS A PARTIAL REPAIR; the claim of completeness is the defect** |
| **F3** | The A5 trigger fires on **instruments**. `STATE.md` is not one, under its own list. A landing commit touching only `STATE.md` — the shape of `c50ce32` (mg-60d3), and the shape that carried **two of the three defects this commit is repairing** — fires **no** trigger in the whole rule set. | **THE TRIGGER HAS A HOLE AT THE ARC'S HIGHEST-DEFECT-DENSITY ARTIFACT** |
| **F4** | Row 135 retains *"the sixth deliverable did the **generalisation** correctly"* — refuted 318 characters later by its own `⚠️ Step 4d DID fire here`. mg-1319 **edited this clause** (*"did it correctly"* → *"did the **generalisation** correctly"*) and narrowed it **toward** the faculty the correction says failed. Appendix A supplies the reconciliation; row 135 does not. | **NEW over-wide clause, at the repair site** |
| **F5** | `controls_output.txt` now contains the string `ALL CONTROLS PASS` **twice**, on `[PASS]`-prefixed lines, above a bottom line that explicitly denies it. Pre-repair it appeared exactly once — as the true bottom line. Any `grep` on that string is now a false-positive generator. | **artifact regression introduced by the A4 self-test** |
| **F6** | Commit message: *"two GENUINE non-sign construction corruptions leave NC3's negative lines SILENT"*. Its own evidence (`out_nc3.txt` line F) shows the ridge-drop case makes line 3 **FIRE**. Only **one** of the two is silent. `STATE.md` and `Probe.md` get this right; only the commit message is over-wide. | over-wide, commit message only |
| **F7** | **Row 135 GREW by 49.7%** (7,832 → 11,727 bytes). The mechanism that let the original three-way contradiction survive is now stronger, not weaker — and this is true even though every individual correction inside it is right. | **measurement, per TARGET 7** |

**NET, in the order that matters: the instrument repair is SOUND and lands the strong way. The
description of the repair over-claims at three new locations — the eighth, ninth and tenth in this
arc — and two of them are, once again, sentences about the commit's own method.**

---

## TARGET 1 — did the A1 rewrite over-correct? **NO. It is correctly sized in both directions.**

I went looking for the over-correction and did not find it. Sweeping `STATE.md`, `Probe.md` and
`controls.py` for *"worthless" / "instrument was broken" / "control was broken" / "useless"* returns
exactly one hit — `STATE.md:274`, which is the **rule forbidding it**:

> *"Do NOT over-correct into 'the control is worthless' or 'the instrument was broken' — that would
> be a second error and a worse one, because it discards a verified result."*

The narrow true position survives intact, and was **strengthened**, not abandoned:

- `THE PIPELINE SURVIVED THE CONTROL IT WAS MISSING` — **retained verbatim** (row 135, offset 7,997).
- *"Do not read this row as 'a control was broken' or 'the Laplacian code was wrong'; neither
  happened"* — **retained**, and mg-1319 **added** the port-faithfulness clause: *"and the port is
  faithful (same rule, same indexing, per-poset agreement with X3 on 86/86 in all three modes, on a
  strictly larger population)."* I verified that addition against
  `code/face_geometry_audit_5630/out_x3_equivalence.txt`: agreement 86/86 in `true`, `allplus` and
  `parity`; and `L(P)` enumeration order identical on only 63/86, i.e. **23/86 differ**, which is the
  claim that the specific `(−1)^j` does no work. Confirmed.
- The reopening is stated as **relocation**, with the residual coverage named (*one absorbable sign
  gauge*), the uncovered site named (`le_to_facet`), and what a satisfying control looks like.

**Reopening-completeness sweep.** I grepped every occurrence of *"covers CONSTRUCTION" / "covers the
construction" / "closes the gap" / "gap is closed" / "now covers" / "missing control"* across
`STATE.md`, `Probe.md` and `controls.py`. Four live sites; **all four carry the relocation reading**
(`STATE.md:135`, `STATE.md:257`, `STATE.md:264`, `Probe.md` §5). One frozen site does not — see F1.

**One asymmetry worth recording.** Appendix A `:264` puts the ⚠️ *at the head of the paragraph*
(*"THE RULE STANDS; THE CLAIM THAT THIS BATTERY NOW SATISFIES IT DOES NOT … Read the correction
before quoting the rule"*). Row 135 puts its reopening at **byte 8,402 of an 11,544-byte cell**, 544
bytes after the closure-reading it corrects. The correction is adjacent to what it corrects, which is
right; it is also 8.4 KB into a single table cell, which is F7.

---

## TARGET 2 — are all three A3 sites fixed, and do they AGREE?

I read them **in sequence**, which is the only way this class of defect is visible. Quoted with line
numbers, in document order.

### Site 1 — `STATE.md:135` (the row), offset 2,009 of 11,544

> **⚠️ CORRECTED 2026-07-30 (mg-5630 §5.2, landed by mg-1319) — this clause used to read *"step 4d's
> own hazard did not fire here; what fired was a label, which is a strictly milder thing"*, and it was
> the wrong one of three incompatible counts the same commit left in this document. Step 4d DID fire
> here.** §0 asserted a universal in `n` off `n ≤ 5` antichain witnesses **with no proof in the
> document**, which is instance-read-as-law by the mechanism … **What is genuinely different from the
> other six firings is the OUTCOME, not whether 4d fired.**

### Site 2 — `STATE.md:251` + `:253` (the Appendix A paragraph)

> **STEP 4d HAS NOW FIRED AT SEVEN LOCATIONS, AND THEY MUST NOT SHARE ONE TALLY** (added 2026-07-30
> from mg-e0ce; **recounted and split the same day from mg-5630 §5.2–§5.3, landed by mg-1319**). The
> invariant of step 4d held on mg-276d: the over-wide statement was at a **new location** … and it
> fired again one commit later, in **mg-78c0's own description of its control coverage**.

> **⚠️ The count was reported three incompatible ways in one commit** … `c0cf104` left row 135 saying
> step 4d *"did not fire here"*, this paragraph — in its previous form, headed *"SIX for six"* —
> saying *"the invariant of step 4d held"* … and template step 4d still saying *"Five for five now"*.
> **All three are now reconciled to the reading the auditor and pm-onethird both reach — 4d DID fire
> on mg-276d** — and the single running tally that made the contradiction possible is retired.

### Site 3 — `STATE.md:199` (template step 4d)

> **SEVEN firings, at a new location every time, and they do NOT share one tally** (recounted
> 2026-07-30 by mg-1319 from mg-5630 §5.2 — the previous *"five for five"* here was stale,
> contradicted the table below, and its single running count is exactly what let one commit report
> three different numbers) … **mg-e0ce's target asserted a universal in `n` off `n ≤ 5` witnesses
> with no proof in the document — the one firing whose statement was true, repaired by an upgrade.**

### Do they agree? **On the load-bearing fact, YES. The A3 repair lands.**

All three now say **4d fired on mg-276d**, all three say **seven locations**, all three point at the
same split, and the stale *"Five for five"* is gone from the template. The two tallies (`:257`
over-wide **and false** — 6; `:258` over-wide but **true and unwarranted** — 1) are consistent with
every site, `:255` states the naming convention so the tallies can be read at all, and `:260`
explicitly retires *"a label not the mathematics"* rather than keeping it. Site 2's phrase *"the
invariant of step 4d held"* — one of the three originally-incompatible statements — is **correctly
kept**: it was always on the right side (the *invariant* is "a new location every time"), and the
stale *"sixth new location"* was dropped from it. That is a careful call and it is right.

**This is a materially better repair than mg-78c0 managed. It is also not complete — see F4.**

### F4 — the clause row 135 edited without correcting

Row 135, reading **forward** from offset 1,154:

| offset | text |
|---:|---|
| 1,154 | **⭐ THE METHOD FINDING FIRST, because it is what five previous rows were missing:** the generalisation … **is carried by a PROOF, and the proof is sound.** |
| 1,491 | *"this makes this the first deliverable in the arc whose most general statement is not established by generalising from its instance."* |
| 1,691 | After five consecutive over-wide generalisations …, **the sixth deliverable did the *generalisation* correctly.** |
| 2,009 | **⚠️ CORRECTED … Step 4d DID fire here.** |

The clause at 1,691 is **not** untouched inherited text. mg-1319 edited it:

```
-  the sixth deliverable did it correctly.
+  the sixth deliverable did the *generalisation* correctly.
```

The edit **narrowed the sentence onto the exact faculty the next sentence says failed.** Before, *"did
it correctly"* was vague enough to be read as *"got the right answer"* — which is true. After, the
emphasis is on ***generalisation***, and Appendix A `:258` says in terms: *"§0 asserted a universal in
`n` off `n ≤ 5` antichain witnesses with **no proof in the document**. That **is**
instance-read-as-law by the mechanism."*

Appendix A `:262` **has** the reconciliation and it is a good one:

> mg-276d **proved** the theorems that carry its most general statements — and separately still
> asserted one universal in §0 off witnesses, which is why it appears in the second tally rather than
> in neither. **Both facts are true of the same document and neither cancels the other.**

**Row 135 carries the first half of that sentence and the correction, but not the connective.** Read
alone — which is how a row gets quoted — it is a flat self-contradiction 318 characters wide. Read
against Appendix A it resolves. That is a weaker instance of exactly the defect being repaired: one
fact, two sites, and the site that resolves it is the one nobody reaches.

I am sizing this deliberately. It is **not** the three-way contradiction returning: the sites agree on
whether 4d fired, which is the fact that was broken. It **is** a new over-wide clause, written by this
commit, at the repair site, in a sentence about method.

---

## TARGET 3 — the A2 numbers, and the number-stripped-restatement sweep

**The corrected sentence is right.** `STATE.md:249`:

> **⚠️ Numbers corrected 2026-07-30 (mg-5630 §4.2, landed by mg-1319): this sentence previously read
> *"purity and the Lemma-1 cross-check, to `n ≤ 6`"* — one bound asserted for both checks, with the
> numbers stripped. Only purity reached `n ≤ 6`; Lemma 1 reached `n ≤ 5`**

Verified against source, not against the summary:

```
code/face_geometry_audit_e0ce/out_n6.txt:44    their Lemma 1 verified on      : 87/87 (n<=5, all k)
code/face_geometry_audit_e0ce/out_extra.txt:2     404/404 posets (2<=n<=6) PURE; violations: none
```

Both quoted correctly, both sources cited, `404` vs `405` marked as not-an-error at both sites so a
future pass does not "fix" it. `Probe.md` §11 (`:765`) corrected identically, with its own marker.

### F2 — the surviving site is the one mg-5630 actually indexed as F3

`Probe.md:132–140`, **untouched by this diff** (I confirmed: `git show db08b4c` contains no hunk
touching it, and `git show db08b4c^` has the identical text):

> **(F3, repaired — say what is and is not independent.)** … That cross-check reaches `n ≤ 4` here
> (POSITIVE CONTROL 3); **the mg-e0ce audit closed it to `n ≤ 6`** by a build that never uses Lemma 1
> at all — 87/87 at `n ≤ 5` for all `k`, and purity 404/404 at `2 ≤ n ≤ 6`.

*"it"* is the **Lemma-1 cross-check**. The cross-check closed to `n ≤ 5`. This is the same
one-bound-for-two-checks overstatement, self-contradicted by its own em-dash clause — which is
precisely how mg-5630 §4.2 described it:

> *"The doc supplies the corrective numbers in the same sentence (so it self-contradicts)"*

and precisely the site mg-5630's finding table indexes as **F3** (row 10: *"cross-check closed to
`n ≤ 6` | substance CONFIRMED; the `n ≤ 6` half OVERSTATED"*).

**The defect is not the surviving sentence — it is mildly self-correcting. The defect is the claim of
completeness.** `Probe.md:37`, added by this commit:

> Also: **the `n ≤ 6` half of F3's coverage sentence corrected to `n ≤ 5` for Lemma 1 (§11)**

F3's coverage sentence is in **§2**, is labelled `(F3, …)` in the document itself, and still reads
`n ≤ 6`. The sentence corrected is §11's, which carries no F3 label. `STATE.md:249` is honest about
this in the present tense (*"The probe doc supplies the corrective numbers in the same sentence as the
overstatement and **so self-contradicts**"*) — so **`STATE.md` correctly records that the probe doc
still self-contradicts, while the probe doc claims it no longer does.**

**Number-stripped restatements elsewhere: none survive.** I swept every `n ≤ 5` / `n ≤ 6` occurrence
in `STATE.md` and all five `docs/*.md` against `Lemma|cross-check|purity|closed|coverage`. Every live
site either carries both numbers or is a bare purity claim (correctly `n ≤ 6`). `Probe-IndependentAudit.md`
`:112–113` is mg-e0ce's own evidence table and is correct at source (`87/87 at n ≤ 5`, `404/404 at
2 ≤ n ≤ 6`) — the commit's decision to leave that document untouched is right and I endorse it.

---

## TARGET 4 — the A4 scoring change, **RUN, not read**

### It works, and it changes the bottom line

```
$ python3 code/face_geometry/controls.py            # exit 0
  [CANNOT FAIL] all-+1 signs leave both top Laplacians UNCHANGED -- L^rel on 86/86,
                L^abs on 86/86, each compared -- and claims (1)/(2)/(3) re-run under
                the corruption still hold on 86/86/86. …
CONTROLS: 0 failures, but 1 row(s) CANNOT FAIL and are NOT scored as passes:
   - all-+1 signs leave both top Laplacians UNCHANGED -- L^rel on 86/86, L^abs o...
A row that cannot fail covers nothing, so this battery's bottom line is NOT 'all controls pass'.
```

A tautological row scores `[CANNOT FAIL]`, not `[PASS]`; the bottom line cannot read `ALL CONTROLS
PASS`; exit code is 0 as claimed. All three landed.

### I tried to make it lie. Nine attacks; **the logic held on eight**

| # | attack | result |
|---|---|---|
| A1 | genuine `cannot_fail=True` row present | held — banner suppressed, exit 0 |
| **A2** | **tautological row registered WITHOUT the flag** | ***LIED* — bottom line `ALL CONTROLS PASS`** |
| A3 | `cannot_fail=1` (truthy int) | held |
| A3b | `cannot_fail="no"` (truthy string, author means *no*) | held (fails safe — suppresses) |
| A4 | flag passed positionally, lands in `detail` | held — `TypeError`, loud |
| A5 | cannot-fail row whose reported fact is **FALSE** | held — `CONTROLS FAILED: 1`, **exit 1** |
| A6 | exhaustive `score(ok, cf)` sweep for a `PASS` with `cf` set | held — no such path |
| A7 | exhaustive `summarise()` reachability sweep | held — banner unreachable with a non-empty tally |
| A8 | cannot-fail row with an empty (falsy) name | held — still tallied |

**The old failure recurs by exactly one route, and I want to be precise about what that means.**
`summarise()` and `score()` are airtight: the invariant *"`ALL CONTROLS PASS` is reachable only when
both tallies are empty"* is enforced without exception, a false tautology is still a `FAIL` with a
nonzero exit, and no truthiness or arity trick gets past it. What is **not** enforced is the
**classification**. `cannot_fail=True` is a hand-set literal occurring at **exactly one call site in
the file** (`controls.py:511`); nothing derives it, and nothing tests that a tautological row was
labelled. Omit the keyword and the pre-repair behaviour returns verbatim.

**This is the honest size of it: the repair enforces an invariant perfectly over a hand-populated
input.** It is a genuine improvement over the merged defect — the defect was in the *scoring*, and the
scoring is now correct — and it is not, and does not claim to be, a detector of unmarked tautologies.
The commit's docstring is admirably exact about its own reach (*"TWO of the five rows below FIRE on
the pre-repair behaviour"* — I confirmed both do), which is the right instinct applied to the right
object. I note for the record that `NEGATIVE CONTROL 3` is **not** marked `cannot_fail`, and that this
is **correct**: NC3 does reject the corruption 82/82, so it is not a tautology. It cannot fail on
*non-sign* construction errors, which is a coverage statement and is recorded as one.

### F5 — the self-test put the forbidden banner back into the artifact

```
$ grep -n "ALL CONTROLS PASS" code/face_geometry/controls_output.txt
4:  [PASS] a cannot-fail row suppresses the 'ALL CONTROLS PASS' bottom line
5:  [PASS] with no cannot-fail row the bottom line is 'ALL CONTROLS PASS'
```

Before this commit that grep returned **one** line: the true bottom line. It now returns **two**,
both `[PASS]`-prefixed, both near the **top** of the file, on a run whose actual bottom line reads
*"…is NOT 'all controls pass'."* Any consumer, human or scripted, that took the string as the pass
signal is now inverted. The whole point of A4 is that this artifact's text must not claim more than
its code verifies; the row that asserts the banner is suppressed is the row that reintroduces it.

*(Unrelated and pre-existing, noted not filed: `run_all.sh` pipes `controls.py` into `tee` under
`set -e`, so the shell sees `tee`'s status and a nonzero exit from `controls.py` would not stop the
script anyway. The commit's *"exit code is unchanged (0), so `run_all.sh` under `set -e` is
unaffected"* is true, but the `set -e` half of the reasoning is moot.)*

### A6 — independently re-derived, and it needs two conditions it does not state

The claim upgraded from *86/86* to *a theorem for every finite poset*: `d_true = diag(row signs) ·
d_allplus`, so `dᵀd` cannot see the all-`+1` corruption. I rebuilt the boundary matrices from the
module's own face data and checked the **factorisation entrywise** (not the Laplacian equality, which
is the weaker consequence), plus the two side conditions the sketch needs and omits:

```
population: all posets up to iso with n <= 6  ->  405 posets
  factorisation d_true = diag(row signs) . d_allplus : 405/405
  (S1) no incidence cancels to zero                  : 405/405
  (S2) interior/free row set is sign_mode-independent: 405/405
  L^rel unchanged                                    : 405/405
  L^abs unchanged                                    : 405/405
```

**(S1)** if any entry of `d_true` cancelled to `0`, the supports would differ and *"row rescaling"*
would be false. It cannot: a facet and a ridge determine the deleted position uniquely, so each
`(r,j)` entry is a single `±1`. **(S2)** `L^rel` **drops rows**, and a row rescaling only commutes
with row-restriction if the interior/free classification is itself sign-independent — which follows
from (S1). Both hold, both are needed, neither is stated. **The theorem is correct**, and it is
correct for the reason given; I record the two conditions so a future reader does not have to
rediscover that the one-line proof has a gap-free but unstated underside.

`*prefer the proof to the count*` is the right call and the citation repair is real: the code now
compares `L^rel` **and** `L^abs` and re-runs claims (1)/(2)/(3) under `sign_mode`, and I confirmed the
`ok` condition tests **all five** measurements, not a subset.

### Reproducibility

```
$ bash code/face_geometry/run_all.sh   (×2)   →   git status --porcelain: empty
```

`controls_output.txt` and `probe_output_n6.txt` regenerate **byte-identically**, twice. Claim
confirmed. *(Measured wall clock **20.4 s**, user 18.9 s. `run_all.sh`'s header still says "~11
seconds"; mg-5630 measured 18.1 s. The commit explicitly scoped this out and said so — correctly
handled, noted only because my number is higher again.)*

---

## TARGET 5 — is the A5 trigger worded to fire on ARTIFACTS?

`STATE.md:313`:

> **Trigger the audit stage on any commit that ADDS OR MODIFIES an instrument** — a control, a probe,
> a harness, a gate, a scoring rule, or the text an instrument prints — **regardless of what the
> ticket is called.** The auditable object is the instrument's *coverage claim*: what can this thing
> fail on, and what does a pass from it license?

**Both licensing phrases are closed, and closed well.** *"Landing ticket"* is defeated by *"regardless
of what the ticket is called"*. *"No new mathematics"* is defeated explicitly at `:315`: *"The
mathematics being untouched is what makes an instrument change look exempt; it is also exactly the
condition under which a repair can quietly redefine what the battery covers."* The reconciliation with
the narrowing test is also correct and necessary — *"a rescoring changes what future passes mean"* is
the right reason. The ticket asked whether the trigger could be argued away by those two phrases. **It
cannot.**

### Adversarial test 1 — mg-78c0 / `c0cf104`: **FIRES ✓**

Touches `code/face_geometry/controls.py` (+63), `controls_output.txt` (+4), `face_complex.py` (+31) —
it adopted NEGATIVE CONTROL 3. Unambiguously *adds or modifies a control*. Fires on the artifact, and
the *"landing ticket" / "no new mathematics"* defences are both pre-empted. **The trigger would have
caught miss #2.**

### Adversarial test 2 — mg-60d3 / `c50ce32`: **DOES NOT FIRE ✗**

```
$ git show --stat c50ce32
 STATE.md | 18 +++++++++++++-----
 1 file changed, 13 insertions(+), 5 deletions(-)
```

`c50ce32` is mg-60d3's **only** commit in this repository, and it touches nothing but `STATE.md`. Its
own text says why: *"**The consequences of this instance are landed in `one_third_width_three`, not
here** (mg-60d3)"* — the two CI controls (`λ₂^BK`, `CONTROL B`) live in a different repository, and
`grep` confirms neither appears anywhere in this one.

So the trigger, as worded, would fire on the mg-60d3 commit **in `one_third_width_three`** — which is
correct in principle, and **unverifiable from the artifact the audit stage actually watches**. The
trigger names no repository scope. That is not a wording defect so much as a reach defect, and I flag
it rather than fix it: **miss #1's coverage cannot be demonstrated from this repo.**

### F3 — the hole the two named misses do not expose

Run the full rule set against a commit that modifies **only `STATE.md`**:

| rule | fires? | why |
|---|---|---|
| narrowing test (`:287–298`) | **no** | re-triggers on a **widening** or **new mathematical content**. Summary prose is neither. |
| PM-verifies clause (`:300–304`) | **no** | scoped to a **new executable artifact**. There is none. |
| **A5 instrument trigger (`:313`)** | **no** | a control, probe, harness, gate, scoring rule, or **the text an instrument prints**. `STATE.md` is none of these — nothing prints it. |
| pre-file rule (`:183–187`) | **no** | scoped to *"any **research ticket** expected to produce a `[PROVEN]` deliverable"*. A landing ticket is not one. |

**A `STATE.md`-only landing commit fires nothing.** And `STATE.md` is where the damage has been:
of the three defects mg-1319 is repairing, **two were introduced in `STATE.md`** (the `n ≤ 6`
overstatement in Appendix A — which mg-5630 called *"the worse of the two places for it"* — and the
three-way 4d contradiction). Both rode into `main` inside `c0cf104`'s **8-line `STATE.md` hunk**, and
were audited only because that commit *also happened* to touch `controls.py`. Split `c0cf104` into a
code commit and a prose commit and the A5 trigger catches the half that was **not** broken.

Template step 4c (*"the text a deliverable proposes for `STATE.md` is a primary audit target in its
own right"*) is the arc's correct instinct here — but 4c is a **step inside an audit**, telling an
auditor what to look at once the stage has already been triggered. It is not a trigger, and it cannot
substitute for one.

**This is the finding the ticket asked for, arrived at from the other side: the trigger fires on
instruments, and the arc's dominant defect site is not an instrument.** I am not proposing wording —
that is pm-onethird's call, as with the structure question below.

---

## TARGET 6 — new or changed claims, enumerated and checked

Every claim `db08b4c` adds or modifies, with how I checked it.

| claim | check | result |
|---|---|---|
| `L_parity = D·L_true·D`, `D = diag((−1)^j)`, **82/82** | `out_nc3.txt` line C | ✔ *"parity L_rel == diag((-1)^j) . true L_rel . diag((-1)^j) on 82/82"* |
| claim (1) with parity signs + twist `E·D` passes again **86/86** | `out_nc3.txt` line D | ✔ |
| all-`+1`: `L^rel` 86/86 **and** `L^abs` 86/86, claims 86/86/86 | ran `controls.py`; re-derived independently | ✔ (and **405/405**, see A6) |
| *"a mis-indexed facet enumeration leaves NC3's negative lines silent, still rejecting 82/82 verbatim"* | `out_nc3.txt` line F (swap facets) | ✔ line2 SILENT, line3 SILENT-still-rejects-82. Line 1 fires, but line 1 is the *positive* row, so *"negative lines"* is accurate. |
| **`38/38` population is `41 = 5+16+20`, a `[:20]` truncation; at `n=5` it saw 20 of 63** | recomputed from `posets_upto_iso` | ✔ exactly `5+16+20 = 41`; `audit_extra.py:70` is `posets_upto_iso(n)[:20]` |
| *"20 posets per `n`"* (=60) was wrong, corrected | source read | ✔ correction is right |
| **`23/86` differing `L(P)` orders** | `out_x3_equivalence.txt` | ✔ *"identical … 63/86"* → 23 differ |
| per-poset X3 ≡ NC3 on 86/86 in all three modes | `out_x3_equivalence.txt` | ✔ true / allplus / parity, 86/86 each |
| Lemma 1 → `n ≤ 5`, 87/87 | `out_n6.txt:44` | ✔ |
| purity → `n ≤ 6`, 404/404 | `out_extra.txt:2` | ✔ |
| **A6 is a theorem for every finite poset** | rebuilt boundary matrices, entrywise factorisation | ✔ **405/405**, + 2 unstated side conditions confirmed |
| tautological row scores `[CANNOT FAIL]`; banner suppressed; exit 0 | ran it; 9-attack battery | ✔ (see A2 caveat) |
| `probe_output_n6.txt` byte-identical; `run_all.sh` ×2 leaves git clean | ran it twice | ✔ |
| **F1** *"the truncation flagged at every site where `38/38` appears"* | grepped all 13 occurrences | ✘ **`Probe.md:798` is unflagged** |
| **F2** *"F3's coverage sentence corrected"* | diffed `Probe.md` §2 | ✘ **untouched; still `n ≤ 6`** |
| **F6** *"**two** genuine non-sign corruptions leave NC3's negative lines SILENT"* | `out_nc3.txt` line F, both cases | ✘ **one does; the ridge-drop makes line 3 FIRE** |

### F1 in full — the eighth location, and it is a claim about this commit's own coverage

`STATE.md:264` and the commit message (A8) both assert:

> *"the truncation **is flagged wherever `38/38` is quoted**"* / *"flagged at **every site** where
> `38/38` appears, incl. STATE."*

Thirteen occurrences across the tree. Live sites are flagged correctly (`STATE.md:135`, `STATE.md:264`,
`Probe.md:393–396`). **`Probe.md:798` is not**:

> The construction-side control is the **audit's** (`…/audit_extra.py` X3, facet-parity signs, **fires
> 38/38 where `\|L(P)\| ≥ 2`**), now adopted into the probe's own battery as NEGATIVE CONTROL 3 …
> and **the true-sign build passes it. The pipeline survived the control it was missing.**

Unflagged, **and** carrying the closure reading. The §12 preamble does disclose the coverage sizing
above the block — but **that is the exact mechanism this commit rejected**, in this block, for F4, in
its own words (A9):

> *"a reader who lands on that block by search or quotation does not necessarily read the note above
> it … an unpatched site found without its disclosure is how a narrowing silently un-narrows."*

mg-1319 acted on that reasoning for F4's subject line — inserting a `⟪…⟫` marker **inline at
`Probe.md:798`** — and declined to act on it, in the same line of the same file, for the `38/38`
truncation and the closure reading. The preamble's list of superseded sizings names the coverage
sizing and the all-`+1` citation; it does **not** name the truncation. So the claim *"flagged at every
site"* is false at the one site where the commit had already proven it knew how to flag.

**This is the arc's signature defect, at an eighth location, in a sentence the commit wrote about its
own repair coverage.** The scale is small — a reader who misses it loses a caveat, not a theorem. The
shape is exactly the one the arc keeps re-learning.

### F6 — the commit message, briefly

> *"the positive control on the control (line F) shows **two GENUINE non-sign construction
> corruptions leave NC3's negative lines SILENT**"*

`out_nc3.txt` line F:

```
F  CORRUPTED PIPELINE (drop ridge #0 from the complex):
     NC3 line3 parity-rejected  : 78 of 78 biting  FIRES        <-- not silent
F  CORRUPTED PIPELINE (swap facets 0 and 1 (mis-indexed facet enumeration)):
     NC3 line3 parity-rejected  : 82 of 82 biting  SILENT
```

One of the two, not two. The sentence half-corrects itself immediately (*"dropping a ridge moves only
the bite-count"*), and **both `STATE.md` and `Probe.md` state it correctly** — row 135 cites only the
mis-indexing case. So this is confined to the commit message. Recorded because the commit message is
what the next reader greps, and because the pattern is the point.

---

## TARGET 7 — does the correction FUNCTION, or merely EXIST?

### The measurement

`STATE.md` at `db08b4c`: **144,334 bytes / 141,327 characters** over **327 lines**.

*(pm-onethird's figures are byte counts. The character count is 141,327 — the file is not pure ASCII.
Every per-row figure below is bytes, matching the brief; divide by ≈1.016 for characters.)*

| row | **before** `db08b4c` | **after** | change |
|---|---:|---:|---|
| 131 | 5,351 | 5,351 | — |
| 132 | 9,228 | 9,228 | — |
| 133 | 13,487 | 13,487 | — |
| 134 | 10,824 | 10,824 | — |
| **135** | **7,832** | **11,727** | **+3,895 (+49.7 %)** |
| **file** | **126,108** (286 lines) | **144,334** (327 lines) | **+18,226 (+14.5 %)** |

Rows 131–135 are **50,617 bytes — 35.1 % of the file in five lines.** The eight largest lines are
41.6 %.

### Did row 135 grow? **Yes — by half again, and that is a finding.**

Row 135 is a **single markdown table cell**. It is now 11,727 bytes containing **73 bold spans** and
**two `⚠️` blocks correcting its own earlier text**. It is a palimpsest: statements, corrections of
those statements, and statements about why the correction was made rather than annotated — in one
cell, in reading order, with no structural separation between a claim and its retraction.

**The repair made the cell larger.** Every individual correction inside it is right — I checked them
one by one and said so above. But the defect being repaired was *"three statements about one fact,
disagreeing, in one document"*, and that class requires that nobody read the sites together. A 50 %
larger cell makes reading-together **harder**, not easier. F4 is the demonstration and it is not
hypothetical: an over-wide clause and its refutation now sit **318 bytes apart inside this cell** and
still disagree, because the connective that reconciles them is 6 KB away in a different section. **The
mechanism is now more likely to fire, not less, and that is true even though every correction landed.**

### Could I hold the row in view? **No — not as it sits in the file, and I want to be plain about it.**

I could not check row 135's internal consistency by reading `STATE.md`. The row is one 11,544-character
line with no newline in it. To perform the sequence-read this audit's TARGET 2 requires, I had to
mechanically extract line 135, split it on its table pipes, and re-wrap it to 110 columns — producing
**125 wrapped lines** across ten columns, one of which is 4,033 characters on its own. Only then could
I place the ⭐ lede, the auditor quote, the *"did the generalisation correctly"* clause and the
`Step 4d DID fire here` correction in relation to one another — which is how I found F4.

**No markdown renderer performs that transformation.** Rendered, row 135 is one table cell. Any reader
who opens `STATE.md` normally — in an editor with soft wrap, in a browser, in a diff — is reading a
horizontally-scrolling cell in which a claim and its correction are separated by distance they cannot
perceive as distance. The three-way contradiction survived `c0cf104` because nobody read three sites
together; **F4 survived `db08b4c` because nobody could read one site together.**

That is the answer to the question as posed: **the corrections function for a reader who arrives at
them, and row 135 is a document in which arriving at them is a tooling operation.** The `⚠️` markers
help — they are the right instinct, they are consistently applied, and Appendix A's practice of
putting the warning at the **head** of the paragraph (`:264`) is measurably better than row 135's
practice of putting it 8.4 KB in. But a marker only functions once the reader has reached it.

### The form question

**The artifact has outgrown its form.** Five table cells hold 35 % of a 144 KB document; the largest is
13.5 KB; the row this audit examined grew 50 % in one commit and now contains two corrections of
itself. The failure mode that produced tonight's flagship defect — three statements about one fact,
disagreeing, unnoticed — is a direct function of that shape, and this commit, while repairing the
instance, made the shape worse.

**I stop there, as instructed.** The measurement is above; the structure is pm-onethird's call.

---

## What is SOUND, stated for the record

Sizing cuts both ways, so: **all nine items landed, and A6/A7 landed the strong way** — `controls.py`
compares `L^rel` **and** `L^abs` and re-runs all three claims under the corruption, rather than
softening the printed text to match what the old code measured. That was the harder and the right
choice. The A4 scoring logic is airtight under nine attacks. The A6 theorem is genuinely a theorem and
I confirmed it on 405 posets plus two conditions it does not state. The A1 reopening is complete at
every live site, with no over-correction in either direction — *"THE PIPELINE SURVIVED THE CONTROL IT
WAS MISSING"* survives a second attempt to break it, and the port-faithfulness clause was
**strengthened** while the gap was reopened, which is the hard combination to write. The A3 three-way
contradiction is genuinely resolved on the fact that was broken, the single tally is retired for a
stated reason, and *"a label not the mathematics"* was corrected rather than kept. Every number
reproduced; two artifacts regenerate byte-identically. **Reopening a row from CLOSED to OPEN is harder
to write than closing one, and this commit did it without flinching in either direction.**

---

## Recommendations to pm-onethird (not actions — I did not edit `STATE.md`)

1. **F2 / F1 are one-line fixes** at `Probe.md:132–140` (`"closed it to n ≤ 6"` → the split bound) and
   `Probe.md:798` (a `⟪…⟫` marker beside `38/38` and beside *"the pipeline survived the control it was
   missing"*, matching the marker this commit already placed in that line). Then the two completeness
   claims become true.
2. **F4** — row 135's *"the sixth deliverable did the **generalisation** correctly"* needs Appendix A
   `:262`'s connective (*"both facts are true of the same document and neither cancels the other"*), or
   needs striking. As it stands the row refutes itself 318 bytes later.
3. **F5** — the two `[PASS]` rows in `controls_output.txt` that contain the literal `ALL CONTROLS PASS`
   should not contain it. The self-test can assert the invariant without emitting the banner.
4. **F3** is a rule-set question, not a text fix, and it is yours.
5. **F7** is a measurement. It is yours too.

---

*Method note, since this arc records them: I ran the battery rather than reading it (nine adversarial
attacks against the scoring, one of which succeeded), re-derived A6 from the boundary matrices rather
than trusting the Laplacian equality, executed `run_all.sh` twice to test the byte-identity claim,
recomputed the `[:20]` truncation from the enumerator, and read the three A3 sites in sequence rather
than in isolation — which is the only reason F4 is in this document. The one thing I could not do by
reading was read row 135.*
