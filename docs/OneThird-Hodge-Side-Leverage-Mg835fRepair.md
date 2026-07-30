# The mg-835f repair — the gate reads the *prose*, and the bottom line is derived from its rows

**Work item mg-8916. Lands the two sites mg-835f left open on the mg-a318 repair
(`b80dea0` + `7f66005`).**
**Instrument: `code/hodge_leverage_repair_8916/`, `run_all.sh`, ~30 s. Committed transcript:
`out_repair_8916.txt`. Predicted exit code, written before the first run: 0. Observed: 0.**

---

## What is not re-opened

**mg-835f's primary target held and is the strongest fires-check of that day.** The gate really
does read the figure **at the site**: 12 of 12 reader-facing figures corrupted on disk make the
run red, and 12 of 12 restorations make it green again — both directions, per figure. Nothing
here re-measures it, re-states it, or weakens it. **0 mathematical statements are touched and
no finding of mg-8a5c or mg-835f is re-marked**; the two dispositions this repair adds are
annotated in place in the audit document, which is otherwise unedited.

---

## G-1 — a wrong figure in ordinary prose beside the site

**CLOSED BY WIDENING THE CODE. The stated extent is not narrowed, and this section is the
saying-which the ticket asks for.**

mg-835f wrote the sentence *"the gap is now +9 999 characters."* into the `STATE.md` row, into
§14 and into H8 — in ordinary prose, **length-preservingly**, leaving the labelled statement the
gate reads correct and untouched — and **the run stayed at exit 0 all three times**. The gate
read one **designated statement** per site; a reader reads the **section**. So *"the gate reads
the figure at the site"* was itself an extent claim **wider than the code**.

### The preferred repair was measured first, and there is nothing to remove

The ticket prefers *removing* the duplicate over gating it, on this lineage's own evidence: six
gates were built on this document and most were later found unable to fail in some direction,
while every repair that removed a generator has held. So the first thing R1 measures is whether
a prose duplicate **exists**:

    site                 live figures, and how many times each is written
    the STATE.md row     gap=1  both=1  cell=1  hist=1  copy=1
    §14                  gap=1  both=1  copy=1
    H8                   gap=1  both=1  cell=1  hist=1  copy=5

**0 live figures are written more times than the site licenses, over 3 sites.** That is the
mg-a318 repair and the `WRITTEN ONCE` check keeps it so. **G-1 is not a duplicate that exists —
it is the duplicate the gate would not see if the next correction wrote one**, which is exactly
how F-1 was born out of mg-8e30's own corrected wording. There is nothing to derive and nothing
to transclude, so the preferred repair does not apply, and the fallback — narrowing the printed
claim to *"structured occurrences only"* — would leave the reader-facing hole open.

**So the third thing was done: the code was widened until the sentence a reader already meets is
true.** That is the same choice mg-d633 made for the two wide extents it closed, and it is
recorded here rather than left to be inferred, because **silently widening a gate and silently
narrowing a claim are different repairs with different costs.**

### What the widening is

`figure_gate` gains a third check beside *at the site* and *written once*:

> **(c) THE CENSUS.** Every figure-shaped token the **section** asserts is enumerated, and the
> whole **multiset** is compared against the live figures at the values measured this run plus a
> **declared roster** of that site's historical figures, each entered with what it is.

A **multiset**, not a set, and that is load-bearing: a wrong prose figure that reuses a value
already on the roster — *"the gap is now +755 characters"* — passes a membership test and fails a
census. Both shapes are probed.

### Measured, on disk, in both directions

Every probe writes to the real file, runs the **real runner**, restores by `git checkout --`
inside a `finally`, verifies the restoration **byte-identical by sha256**, and runs the runner
**again**. Every mutation is **length-preserving** — four of the five figures are lengths of the
very text being mutated, so an insertion moves the measurement and a fire proves nothing (that
distinction cost mg-835f a prediction, and its miss is kept as written).

| probe | before mg-8916 | after |
|---|---|---|
| **`+9 999` in ordinary prose** at each of the 3 sites (mg-835f's own U1) | **gate passes ×3** | **GATE FIRES 3 of 3** |
| **`+755` in ordinary prose** at each of the 3 sites — a value already on the roster | not probed | **GATE FIRES 3 of 3** |
| **restoration**, all 6 | — | **silent 6 of 6**, sha256-verified |

**6 of 6 fire; 6 of 6 restorations return the run to exit 0.** A gate that fires on everything is
worth no more than one that fires on nothing, so both directions are reported per probe.

The in-memory battery grows with it: `verify_landing.py`'s negative control goes from **9
mutations to 14**, N10–N12 being mg-835f's U1 probes and N13 the roster-reuse case, all through
`figure_gate` itself rather than a re-implementation. **14 of 14 move the gate as predicted.**

### The extent, printed — and what it does not cover

The gate now **prints its own extent** before running, because an extent that is not printed
becomes the next claim wider than its code:

    the STATE.md row      17 licensed figure tokens ( 6 historical values declared)
    §14                   16 licensed figure tokens ( 9 historical values declared)
    H8                    36 licensed figure tokens (16 historical values declared)

**69 figure tokens are read across the three sites, where the gate previously read 12 designated
statements and nothing else.** Declared **not** covered:

- figures inside **marked quotations** — `assertions()` strips them, on the convention already in
  force at these sites: a quotation of a withdrawn figure is not an assertion of it;
- figures **outside** the section, because a site is a section, not the file that contains it;
- numbers that are not of this arc's character-count shape (a bare `405`, a ticket id).

**And the cost, stated rather than discovered: the census is fail-CLOSED.** A legitimately new
historical figure at a site makes the run red until it is entered on the roster with what it is.
That is the same cost mg-835f reported for U5 — an innocent rewording is a red run — and it is
the direction a locator should fail in. The roster **is** the declaration Appendix A's rule asks
for, kept where a checker reads it rather than only where a reader does.

---

## G-2 — the bottom line that contradicted its own T1

**CLOSED. The summary is fixed to match the rows, not the rows to match the summary.**

Re-run at a tree later than the one it was taken against, `audit_repair_8e30.py` printed two
`[REFUTED]` lines in **T1, its own declared primary target** — *"the three published parts
reproduce from the tree"* and *"THE REPAIR'S FIGURES DID NOT GO STALE"* — and then printed,
**unconditionally**, *"THE PRIMARY TARGET IS CONFIRMED"*. Both in one transcript, with the
summary being the part that travels.

**The rule applied, and it is worth carrying beyond this ticket:** *every time a summary and its
supporting rows have disagreed in this arc, the summary was wrong and the rows were right.*
Bottom lines, banners, `TOTAL BAD` counts, disposition labels — **the summary is written once,
early, by whoever is most invested in the conclusion; the rows are regenerated. When they
disagree, believe the rows.**

So:

1. **The rows that a summary speaks for are tagged.** `record()` takes a `tag`; T1's two
   primary-target rows carry `PRIMARY`.
2. **The sentence is derived from them**, not written beside them. There is no branch that can
   assert a verdict the rows refute.
3. **A `SUMMARY vs ROWS` check** compares the printed verdict with the rows' verdict and is
   recorded like any other check — it counts, and it moves the exit code.

**T1 is not relaxed.** Its expectations are the figures `e16e41c` published, and this instrument
audits `e16e41c`; a later commit that legitimately moves them makes those rows refuted **on a
re-run**, which is a true statement about a later tree. The derived sentence now says so, names
the rows, and says where the verdict as taken lives.

### Demonstrated firing

**A summary-versus-rows check that has never been shown to fire is the vacuous-check defect this
arc has produced three times tonight.** So R2 runs the instrument twice and forces the two apart:

| run | `SUMMARY vs ROWS` | refuted count |
|---|---|---|
| **as it stands** — 2 of 2 `PRIMARY` rows `[REFUTED]`, sentence says REFUTED | **`[CONFIRMED]`** | 3 |
| **summary FORCED** to the sentence it used to print unconditionally | **`[REFUTED]`** | **4** |

The forced run reproduces **the exact shape mg-835f found** — *"THE PRIMARY TARGET IS
CONFIRMED"* printed in the same transcript as its own refuted `PRIMARY` rows — and it is now
reachable only by forcing it, and **forcing it is caught**. The refuted count moves by exactly
one, so the check is not decorative.

---

## Which artifact was written, and which was regenerated

Stated because a document left wrong with its evidence **bent to agree** presents identically in
a diff to a document corrected with its evidence **regenerated to follow**.

| artifact | |
|---|---|
| `code/hodge_leverage_audit_8a5c/out_audit_8e30.txt` | **WRITTEN ONCE AND FROZEN** — the mg-8a5c run as *taken*, at `f58f7fd`. Not regenerated here; its verdict is unchanged. R3 checks it is **byte-identical to `main`** rather than asserting it |
| `code/hodge_leverage_audit_835f/out_audit_a318.txt` | **WRITTEN ONCE AND FROZEN** — the mg-835f run as *taken*. Its reproduction contract is deliberately broken by this repair (it names the two source files this repair edits), and that is recorded in that document rather than left to be discovered. Its §6 U1 rows still read `gate passes`; **they were correct when taken** |
| `code/hodge_leverage_landing_e1d0/out_verify.txt` | **REGENERATED to follow** the widened gate — it gains the census lines, the extent block and N10–N14, and nothing else |
| `code/hodge_leverage_repair_8916/out_repair_8916.txt` | **REGENERATED** — this repair's own run, byte-identical across two consecutive runs |
| the two audit **source** files | **AMENDED**, so a *re-run* tells the truth about the tree it is run against. The frozen transcripts and the amended sources say different things because they are about different trees, and that is the point |

**No document a reader reads for the figures is edited.** `STATE.md`, the deliverable and the
row-history file are untouched by this commit, so **no live figure moves** and there is no
post-commit measurement to publish: the whole of the G-1 repair is in the gate. That is also why
the census roster reproduces without a re-baseline.

---

## Predictions, including what they cost

| prediction | observed |
|---|---|
| instrument exit code | **0**, as predicted |
| the 3 U1 probes fire on disk | **3 of 3**, as predicted |
| the 3 roster-reuse probes fire | **3 of 3**, as predicted |
| all 6 restorations silent | **6 of 6**, as predicted |
| the unmutated tree stays green | **exit 0**, as predicted |
| `SUMMARY vs ROWS` fires when forced | **fires**, as predicted, and moves the refuted count by exactly 1 |
| the preferred repair (remove the duplicate) would apply | **MISSED, and kept as written.** It does not: 0 live figures are over-written at 3 of 3 sites, so there was nothing to remove and the choice was between widening the code and narrowing the claim. The code was widened, and this row is why that is stated rather than assumed |

---

## Reproduction

    sh code/hodge_leverage_repair_8916/run_all.sh     # ~30 s, exit 0

The transcript regenerates byte-identically at any tree in which `STATE.md`,
`docs/OneThird-Hodge-Side-Leverage.md`, `docs/state-history/attempt-mg-a3d4.md`,
`code/hodge_leverage_landing_e1d0/` and `code/hodge_leverage_audit_8a5c/` are unchanged; it
embeds no sha of its own, and it was checked byte-identical across two consecutive runs. It
**mutates the tree and restores it**, refuses to run against a dirty one (scoped to the three
files it will `git checkout --`, plus the one the mg-8a5c instrument restores), and verifies
every restoration by sha256. `git status` is clean after a run except for
`code/hodge_leverage_repair_8916/out_repair_8916.txt`.
