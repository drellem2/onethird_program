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
