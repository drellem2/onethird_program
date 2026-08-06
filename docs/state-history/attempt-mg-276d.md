# Attempt index — GREEN · PROVEN, all finite posets (mg-276d): the foundation claims (1)–(3) supply

Per-row history for `STATE.md` § *Attempt index*, the **GREEN · PROVEN, all finite posets · first proof-carried generalisation in the arc (mg-276d)** row.
Split out of the ledger cell by mg-34bf, 2026-07-30.

Every passage below was **moved verbatim** out of that cell. Nothing was rewritten,
condensed, summarised or dropped, and no citation was changed. The row now asserts current
state and points here; `code/state_restructure_34bf/verify_relocation.py` checks, clause by
clause against the pre-restructure `STATE.md`, that every clause of the old cell is still
present in the row or in this file. See [`README.md`](README.md) for the convention.

## Corrections, retractions, supersessions and mechanism notes

*Why this section exists: a ledger row must not be able to contain a claim and its own
retraction. The row states what is true now; what it used to say, what was struck, and why,
is here. Sections are numbered `H1`, `H2`, … and the row cites them by number.*

### H1 — the step-4d clause — first of the three A3 sites

After **five consecutive over-wide generalisations** (mg-d112, mg-e35c, mg-f825, mg-c8c6, mg-09ea — see Appendix A step 4d), the sixth deliverable did the *generalisation* correctly — **and, in the same document, still asserted one universal in §0 off `n ≤ 5` antichain witnesses with no proof present, which is why it appears in the second 4d tally rather than in neither. BOTH FACTS ARE TRUE OF THE SAME DOCUMENT AND NEITHER CANCELS THE OTHER: the theorems that carry its most general statements are PROVED, and one further universal was asserted off witnesses. ⚠️ CONNECTIVE INLINED HERE 2026-07-30 (mg-f7bc F4, landed by mg-f2e1) — mg-1319 EDITED this clause, from *"did it correctly"* to *"did the **generalisation** correctly"*, narrowing it onto the exact faculty the *"Step 4d DID fire here"* correction denies — and as mg-1319 left it those two sat **318 characters apart, clause-start to clause-start, with no connective between them** — while leaving the reconciliation in Appendix A's *"STEP 4d … THEY MUST NOT SHARE ONE TALLY"* paragraph — the **second** tally, *"over-wide but TRUE, and unwarranted at the time"* — six kilobytes away. (Cited without the running count on purpose: that count is recounted as the arc proceeds, and a citation that names it rots on the next recount.) Read alone — which is how a row gets quoted — the row then refuted itself within one sentence. This is the site that gets quoted, so it carries the CONNECTIVE and not just the two halves.**

**⚠️ CORRECTED 2026-07-30 (mg-5630 §5.2, landed by mg-1319) — this clause used to read *"step 4d's own hazard did not fire here; what fired was a label, which is a strictly milder thing"*, and it was the wrong one of three incompatible counts the same commit left in this document. Step 4d DID fire here.**

§0 asserted a universal in `n` off `n ≤ 5` antichain witnesses **with no proof in the document**, which is instance-read-as-law by the mechanism, and it was defused only because an **external auditor supplied a proof afterwards** — so it is not a label error either: the label was wrong *because the mathematics was absent*, and the auditor wrote it.

**What is genuinely different from EVERY OTHER firing is the OUTCOME, not whether 4d fired: the over-wide statement was TRUE and provable, so it was repaired by an upgrade rather than a strike — and it is the ONLY firing so far in that position, which is why it holds the second tally alone.**

That distinction is worth keeping and this clause was the one that got quoted, which is why it is corrected rather than annotated.

See Appendix A, *"STEP 4d … AND THEY MUST NOT SHARE ONE TALLY"*, for the two tallies and the boundary between them.

**⚠️ THE COUNTS THIS SENTENCE USED TO CARRY WERE STALE AND ARE NOW GONE, not bumped (2026-07-30, mg-f2e1).**

It read *"the other **six** firings"* and cited Appendix A as *"STEP 4d HAS NOW FIRED AT **SEVEN** LOCATIONS"*, while Appendix A had been recounted to **nine** (tallies 8 + 1) — **one count, two incompatible values, in one document: the exact A3 defect this row was repaired for, recurring at the repair site because the row hard-codes a number that Appendix A recounts.**

Appendix A's own resolution applies verbatim — *"the repair is not to pick a bigger number, it is to stop reporting one number"* — so this row now points at the tallies instead of restating their sizes, which cannot rot on the next recount.

### H2 — F1, the one over-labelled universal, repaired by an upgrade

**This is F1, the one over-labelled universal: the deliverable's §0 asserted the universal in `n` while its ledger row D2 carried `PROVEN-by-computation on n ≤ 5`. The auditor's proof is adopted and row D2 upgraded, so the statement and its label now agree — a mislabel repaired by an upgrade, not a retraction.**

### H3 — the all-+1 invariance theorem, and the repair of its citation

**That last statement is TRUE and is a THEOREM for every finite poset** — a ridge omits exactly one ideal cardinality, so the deletion index is fixed by the ridge alone and `d_true = diag(row signs) · d_allplus`, a row rescaling `dᵀd` cannot see (mg-5630 §2.2(a)) — **and its citation is repaired here (mg-5630 §3.2): neither run originally cited for it measured it** (the control compared only the twisted `L^rel`, and claims (2)/(3) were never re-run under `sign_mode`).

### H4 — the relocated coverage gap, the gauge-conjugation mechanism, and the positive control on the control

**⚠️ BUT THE COVERAGE GAP IS RELOCATED, NOT CLOSED (mg-5630 §2.2–§2.3, landed by mg-1319), and this row previously read as though it were closed.**

NC3's corruption is a **diagonal `±1` gauge conjugation** — `L_parity = D·L_true·D`, `D = diag((−1)^j)`, verified exactly 82/82 — hence **isospectral**, and **absorbable into the twist**: claim (1) with parity signs and twist `E·D` passes again on **86/86**, so the corruption is observationally identical to corrupting the twist, which M1 and M3 already do.

The positive control on the control nobody had run: a **mis-indexed facet enumeration** leaves NC3's negative lines **silent, still rejecting 82/82 verbatim**.

### H5 — the recommended next probe, and the answer that discharged it

The cheaper next probe is to price the program's actual bet — take one Hodge technique for the top relative Laplacian of a pseudomanifold-with-boundary and ask whether it says anything non-trivial about `λ₂(Δ_AT)`.

**⭐ THAT PROBE WAS RUN AND IS AUDITED — mg-a3d4, audited mg-86a3, landed by mg-a806; see the next row. The answer is NO for `Δ_AT`, and it is carried by a theorem: the standard link-based technique is `2^{Θ(n)}` lossy (Theorem G, rebuilt independently and exact to `A_12`), the top two dimensions are graph theory under either reading of "relative", and the one technique that is genuinely absent from the graph side — Brown's theorem for the face SEMIGROUP — reaches `Δ_AT` only where `Δ_AT` is already diagonal. So this row's closing suggestion is DISCHARGED, not pending.**

## Supporting record — derivations, constructions, evidence and audit provenance

*These passages support claims the row still states. They moved so that the row reads as an
assertion rather than as an argument. **No claim moved with them**; where a passage carried
both a claim and its evidence it stayed in the row.*

The auditor, who re-derived it independently: *"this makes this the first deliverable in the arc whose most general statement is not established by generalising from its instance."*

**The two degenerate subclasses are named as NON-EVIDENCE, not counted as successes** — the antichain (`∂F = ∅`, `L^rel = L^abs`, claim (3) vacuous: the one subclass where the bridge says nothing new) and the chain (`0 = 0`) — which the audit pressed for and found already done.

275 posets with non-trivial `Aut` and 108 disconnected all pass.

**Controls, and the one gap the audit found (F2) — read the framing, it is the point.**

Positive: homology on `S¹`/`S²`/disc/wedge, A000112, `Sur_iso` cross-enumerated against chains, `∂∘∂ = 0`, and `ker L^abs_top` against `H_{n−2}(F(P))` by a **disjoint code path**.

Negative: five named mutations, each rejected on 100% of the posets where it bites, with vacuity **computed**.

**But none of those five perturbed the CONSTRUCTION of the Laplacian** — four perturb the twist or the target — and the control that looked as though it did (all-`+1` simplicial signs) runs on the *homology* path and **cannot fire on the Laplacian at all**: both top Laplacians are unchanged by it, so claims (1)–(3) survive it.

`controls.py` now compares `L^rel` **and** `L^abs` and re-runs all three claims under the corruption — 86/86 on each — so the sentence is measured as well as proved; **prefer the proof to the count.**

---

## Full cell text before the mg-ea0e relocation (2026-08-06)

Appended by **mg-ea0e**, 2026-08-06, on pm-onethird's relocation spec, which finishes here
the convention mg-34bf started: **relocation, not deletion**.  The `STATE.md` row now
carries its status label, its own opening sentence verbatim, and a link to this file.

**Everything below is that ledger cell's ENTIRE text as it stood immediately before that
edit** — all three columns, character for character, from `STATE.md` at `78ae4d9`.  Nothing
was rewritten, condensed, summarised or dropped.  Passages mg-34bf had already relocated
appear above under `H1`…; they recur below only because this is the whole cell, and the
sentence the row retained appears below as well, in its place.

### Status-label column, verbatim

> **GREEN · PROVEN, all finite posets · first proof-carried generalisation in the arc (mg-276d; computation permitted and used — 405 posets, controls both directions; audited mg-e0ce — **CONFIRMED**, GREEN upheld and upheld *for the reason the deliverable gives*: both Laplacians and the whole 405-poset population rebuilt by a disjoint route and the proof re-derived line by line, **0 BROKEN mathematics**, 1 over-labelled universal, 1 control-coverage gap, 4 summary-scope items — all landed by mg-78c0; **the mg-78c0 landing was then itself audited — mg-5630, OVERSTATED: 0 BROKEN mathematics, every committed number reproduced independently and two outputs byte-identically, the D2 upgrade fully earned, and three over-wide claims about METHOD, of which the control-coverage one is the material change to this row — landed by mg-1319**)**

### Attempt column, verbatim

> the **foundation claims (1)–(3) supply** for the intrinsic face-geometry program (doc: `OneThird-Intrinsic-Face-Geometry-Probe.md`; audit: `OneThird-Intrinsic-Face-Geometry-Probe-IndependentAudit.md`; code: `code/face_geometry/`, `run_all.sh`, ~17 s; audit instrument: `code/face_geometry_audit_e0ce/`)

### Result column, verbatim

**⭐ THE METHOD FINDING FIRST, because it is what five previous rows were missing: the generalisation from Daniel's one four-element example to *all finite posets* is carried by a PROOF, and the proof is sound.** **⚠️ STEP 4d DID FIRE HERE, and the OUTCOME — not the firing — is what is different: the over-wide statement was TRUE and provable, so it was repaired by an UPGRADE rather than a strike, which is why it holds the second 4d tally alone. This row states no 4d *tally* of its own and points at Appendix A's two tallies instead, so it cannot rot on the next recount — mg-34bf wrote that as an absolute *"states no count of its own"*, which this cell's own opening sentence falsifies; mg-6a2f F1, narrowed to the true claim by mg-7735. This is the first of the three A3 sites; the other two are Appendix A, *"STEP 4d … AND THEY MUST NOT SHARE ONE TALLY"* and template step `4d`** — [row history H1](docs/state-history/attempt-mg-276d.md). **The mathematics.** With `F(P)` the compatible face complex — exactly the order complex of the proper part of `J(P)`, pure of dimension `n−2`, facets `L(P)`, **every ridge in 1 or 2 facets** (a pseudomanifold with boundary; this is what makes "relative" well-posed) — and `E = diag(sgn w)`: **(1)** `E·L^rel_top·E = D − A = Σ_t(1−τ_t)`, the unweighted adjacent-transposition Laplacian, as an **equality of matrices** (the conjugator `E` is an explicit diagonal `±1` involution, so this *is* a similarity — with a known conjugator, not up to an unknown one, and not up to normalisation); **(2)** `E·L^abs_top·E = (n−1)I − A =` the compression of `Σ_i(1−s_i)` from `C[S_n]`; **(3)** the free ridges at `w` are in **bijection** with the generators forbidden at `w`, and `L^abs − L^rel` is the diagonal **count** of them. The twist is **unique** up to a global sign and is **labelling-independent** (relabelling `P` multiplies every `sgn` by one global sign, which `L ↦ ELE` cannot see). **Three corrections to the source, all audit-confirmed.** (i) The sketch attaches the twist to claim (1) only; it is **equally required for claim (2)** — untwisted, (1) and (2) each hold on only 6 of 405 posets, all chains with `\|L(P)\| = 1`. (ii) The sketch does not say which side `s_i` acts on, and **the readings are not interchangeable**: claim (2) is true for the **right/position** action and **false** for the left/value one. **The antichain refutes the left/value reading at every `n ≥ 3`, and that is PROVEN** — two lines (`s_1 s_2` is a right-neighbour of `s_1` and not a left-neighbour; at `n = 2` the readings coincide), verified to `n = 8`. **F1 — the one over-labelled universal — was repaired by an upgrade, not a retraction** — [row history H2](docs/state-history/attempt-mg-276d.md). (iii) *"records **precisely** the forbidden generators"* is true at the level of the **complex** (which ones) and an overstatement at the level of the **Laplacian difference**, which is diagonal and records only **how many**. **One interpretation, labelled CONDITIONAL:** the source never defines "relative"; the probe reads it as relative to the boundary subcomplex generated by the free ridges — the reading claim (3) itself selects. Everything else is unconditional given it. **Population:** all 405 posets up to iso with `n ≤ 6` (A000112-checked, independently re-enumerated by a different canonicalisation), of which **394 are non-degenerate** (`\|L(P)\| ≥ 2` **and** at least one free ridge) — not an identity between two trivial objects; and separately the general statements are **proved**, so the population is all finite posets. **The all-`+1` invariance is a THEOREM for every finite poset, its citation is repaired, and `controls.py` now measures it as well; prefer the proof to the count** — [row history H3](docs/state-history/attempt-mg-276d.md). The auditor supplied the missing control (facet-parity signs, `audit_extra.py` X3), it **fires on 38/38** posets with `\|L(P)\| ≥ 2` **in its own population, which is 41 = 5+16+20 and NOT 60: `construction_side_control()` iterates `posets_upto_iso(n)[:20]`, so at `n = 5` it saw 20 of 63 posets in enumeration order — a truncation, flagged here because `38/38` is quoted as a headline** (the number that matters is the port's complete `n ≤ 5` population, 82/82). It is now **adopted into the probe's own battery** as NEGATIVE CONTROL 3 (fires 82/82 across all posets `n ≤ 5`), and **the true-sign build passes it. THE PIPELINE SURVIVED THE CONTROL IT WAS MISSING — the gap was in the argument for trusting the instrument, not in the instrument.** Do not read this row as "a control was broken" or "the Laplacian code was wrong"; neither happened, and the port is faithful (same rule, same indexing, per-poset agreement with X3 on 86/86 in all three modes, on a strictly larger population). **⚠️ THE COVERAGE GAP IS RELOCATED, NOT CLOSED (mg-5630 §2.2–§2.3, landed by mg-1319), and this row previously read as though it were closed** — [row history H4](docs/state-history/attempt-mg-276d.md). **So coverage went from ZERO to ONE ABSORBABLE SIGN GAUGE; `le_to_facet` is the named uncovered site and F3 in the same commit calls it load-bearing. Forward consequence: a control battery must cover CONSTRUCTION as well as COMPARISON,** a control on a neighbouring code path does not cover the construction — **and neither does a control whose corruption is absorbable into a parameter the battery already varies.** Full sizing in Appendix A, *"A control battery must cover CONSTRUCTION as well as COMPARISON"*, including the third checkable question that would have caught this. **The auditor's net on the landing, in its own order, and it is the wording to quote: REAL PROGRESS ON D2 — a universal that was asserted-and-unproven is now proved, generally and correctly, and the label matches — and RELOCATION NOT CLOSURE ON THE CONTROL GAP.** **THE HONEST NET, and it must travel with the headline: this is an exact dictionary between two descriptions of one matrix, so it carries no bound and no new tool.** Whether it has leverage depends on whether the Hodge side has techniques the graph side lacks — **the probe took no position on that and did not test it**, and the audit adds nothing except that this is right. It carries **nothing** about BK or block moves, **nothing** about the faces below the top two dimensions, **nothing** about weighted or degree-normalised chains (uniform rescaling *is* covered; `D^{−1/2}(D−A)D^{−1/2}` is **not** the top relative Hodge Laplacian when `D` is non-constant), and the spectral-gap row carries the **eigenvalue only — not the mixing time** (F5: `λ₂` alone does not determine it, and the chain's generator is `(1/(n−1))(D−A)`). The pairing it does deliver: **"restrict the ambient dynamics" vs "build them intrinsically" is exactly "absolute vs relative Hodge theory on `F(P)`"**, and connectivity of the adjacent-transposition graph is exactly `dim H_{n−2}(F(P),∂F(P)) = 1`. **`A(P)` was NOT built** (out of scope). **Recommendation, not action:** the operator-algebra ticket **— none is queued, and `A(P)` is NOT to be built as a route to `λ₂(Δ_AT)` (routing, pm-onethird 2026-07-30; see the next row) —** need not re-establish **the foundation claims (1)–(3) supply** — and that is the *only* foundation established here (F4): the sketch's left-regular-band product, its higher-codimension faces, its Young-module picture and its BK realisation are **all untouched**. **The cheaper next probe this row recommended WAS RUN AND IS AUDITED (mg-a3d4, audited mg-86a3, landed by mg-a806 — the next row): the answer is NO for `Δ_AT` and it is carried by a theorem, so this row's closing suggestion is DISCHARGED, not pending** — [row history H5](docs/state-history/attempt-mg-276d.md). *(Full per-row record — every passage relocated from this cell, verbatim: [`docs/state-history/attempt-mg-276d.md`](docs/state-history/attempt-mg-276d.md).)*
