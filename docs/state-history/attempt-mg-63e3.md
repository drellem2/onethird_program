# Attempt index — RED-conditional · witness fully CONFIRMED (mg-63e3): can Step 6 consume L4's branch (ii)?

Per-row history for `STATE.md` § *Attempt index*, the **RED-conditional · witness fully CONFIRMED · CORRECTS MERGED WORK (mg-63e3)** row.
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

### H1 — the conditional status this row carried before mg-3af9 discharged it

As of mg-63e3/mg-f825 it was genuinely *conditional* and *almost certainly the operative case* was not what a `PROVEN` row says.

### H2 — the struck universal (Cor. 4.3 / ledger claim 13)

**⚠️ THE UNIVERSAL IS STRUCK — do not restore it.**

The deliverable's Cor. 4.3 / ledger claim 13 — *"there is no modulus `F` for which transport is true"* — is **BROKEN as a universal**.

Branch (ii) is not a free hypothesis: a poset enters it **only if** `\|S\| ≤ F(ε)n`.

Family **W** lives entirely inside `Δ₁·n = 2t/(t+2) < 2`, so it constrains `F` only along its own sequence and **provably cannot refute any modulus with `F(ε) ≤ ε/2`** (element-counting; `2ε` under relation-counting — a factor 4 in the one constant the argument is about, since (ii) counts *elements* and only `x`'s relations change, so `\|S\| = 1` for every `t`).

**`F(ε) = ε/4` is an ordinary modulus** — it tends to `0`, and `F(ε)n → ∞` for every fixed `ε > 0`, so branch (ii) is not thereby degenerate — **and `W` says nothing against it.**

### H3 — the n-dependence clause that was deliberately not landed, and the invalid quantifier step under it

**⚠️ THE `n`-DEPENDENCE CLAUSE IS DELIBERATELY NOT LANDED — this is a decision, not an omission.**

The deliverable proposed recording that transport needs `F(ε)n ≤ 1`, *"an `n`-dependent condition, vindicating mg-88bd §3.3's dismissed steelman and tightening it from `O(1)` to `≤ 1`"*.

**It rests on an invalid quantifier step.**

In **W** the pair `(ε, n)` is **locked** — at `t = 2`, `ε = Δ₁ = 1/n` *identically*, one `(ε,n)` per `a` — so `F(ε) = ε` satisfies `F(ε)n ≤ 1` exactly and is a function of `ε` alone; the inference to `n`-dependence silently re-reads the constraint as holding at *fixed* `ε` for *all* `n`, and the family, confined to `εn < 2`, never supplies such a pair.

**The stakes are why this is recorded and not merely dropped:** the mg-88bd row above states that **if L4 needs an `n`-dependent modulus the answer flips** — landing this clause would have flipped a canonical row on a quantifier error, and mg-e35c F1 had flagged §3.3's *dismissal* as a false universal, to which the correct response is not to install the opposite universal.

The deliverable's own ledger row 16 already labels the underlying claim family-conditional (`PROVEN for W` · *"conditional as a general claim — a lower bound on the demand, from one family"*), and row 16 is right where row 13 is wrong.

### H4 — the second BROKEN premise, "1/n is the smallest nonzero leakage a prefix cut can have"

**Second BROKEN premise, recorded because it removes Cor. 4.3's stated basis:** *"`1/n` is (up to constants) the smallest nonzero leakage a prefix cut can have"* is **false by a factor of `n`** — hand witness at `n = 8` (chain `c_1<c_2<c_3`; `x ∥` every `c_j` and `∥ b_1`, `x < b_2,b_3,b_4`; `b`'s a chain; every `c < ` every `b`) has 5 linear extensions, `E\|A∖σ(A)\| = 1/5`, **`Δ₁ = 1/20`**, and the family gives `Θ(1/n²)` in general.

The witness is undamaged (`Δ₁ → 0` is all it needs), but there is an entire `n`-fold range of leakage scales below `1/n` at which a modulus could be calibrated and at which **W** is silent.

### H5 — (IB)'s false interface clause, and its two refutations

**(IB) IS RECORDED IN REPAIRED FORM — the stated version is FALSE and must not be pasted.**

As proposed it ended *"…and one may take it to be an **interface** pair"*; that clause is refuted twice — modulus-free at `n = 3` (`P = AC_2 ⊕ C_1`, `A = {u,v}`, `B = {w}`: `P` **is** `P[A] ⊕ P[B]` exactly so every `G ≥ 0` admits it, `Δ₁ = 0`, `p_{uv} = 1/2` balanced, but `P` has **no incomparable interface pair at all** — every exact ordinal sum with a non-chain side does this), and again at `n = 8` with genuine leakage `Δ₁ = 1/20` and one genuine modification (only interface incomparable pair `{x,b_1}` has `p = 4/5`, unbalanced; the balanced pair `p_{x,c_2} = 2/5` has **both** endpoints in `A`).

**The defect is the interface clause, not the lemma's substance**, and the fix is free — which is precisely why it was made before the row landed.

(Also dropped: the dead quantifier `c > 0`, which never reappeared.)

### H7 — two calibrations of the deliverable, neither fatal

**Two calibrations, neither fatal:** Step 6's licence is L4, not minimality (minimality supplies the *side* pair at `:476–477`, near-ordinal-sum stability supplies the *transfer* at `:514`); and *"the `⟹ balanced pair by minimality` box at `:527` is **wrong** on branch (ii)"* overshoots — `:478–479` already calls transport *"the task"*, i.e. states it as open, so the exact claim is: **the box at `:527` is justified only on branches (i) and (iii); on (ii) the source's own prose concedes the gap, and this shows the gap cannot be closed by transport at any `F(ε) = Ω(ε)`** (now, per mg-3af9/mg-c8c6, at **every strictly positive** modulus) — open → impossible-by-this-mechanism, still a genuine strengthening.

### H8 — the two roles of `F`, and the audit's ledger tally

**One coordinate the deliverable introduces and never names, and it is the direct cause of the quantifier failure:** `F` has **two roles** in L4 — a *budget* in (ii) (`F(ε)n` elements) and an *error tolerance* in (iii) (`F(ε)` in probability) — and **only the first admits or excludes a witness.**

## Supporting record — derivations, constructions, evidence and audit provenance

*These passages support claims the row still states. They moved so that the row reads as an
assertion rather than as an argument. **No claim moved with them**; where a passage carried
both a claim and its evidence it stayed in the row.*

`W`: `n = 2a`, `A = C_{a−2} ⊕ AC_2`, `B = C_a`, all `A < B` except the crosses `x < b_1, …, x < b_t` deleted; the sides' *entire* supply of balanced pairs is one pair, at exactly `1/2` in `P[A]` and at `1/4` in `P`, and shrinking `ε` does not evade the family (it exists at every `ε = 1/n`).

**Structural cause, CONFIRMED and the document's best explanation:** `p_{xy}` is a *global* functional of the poset and `poset ↦ LE-distribution` is **not Lipschitz in the modification count** — in `W`, `y` (half the destroyed pair) participates in no modification; what moves is `x`'s *position law*, since `t` deletions buy `t` slots of slide and slide is exactly what `p` measures.

So no bound `\|Δp\| ≤ g(\|S\|)` with `g → 0` can hold.

For every `ε > 0` take `n ≥ 1/ε`: **W** at `t = 2` has `Δ₁ = 1/n ≤ ε`, its only side balanced pair sits at exactly `1/2` in `P[A]` and `1/4` in `P`, and the repaired predicate (`p^P ∈ [1/3,2/3]`) fails outright.

**KEEP VERBATIM — the deliverable's durable contribution, and all of it correct:** (1) the **C1/C2/C3 separation** (C1 = branch (ii)'s own statement delivers no balanced pair; C2 = Step 6 as written consumes (ii); C3 = *no* argument can consume (ii)); (2) the **explicit declining of C3** — NOT ESTABLISHED, here or in mg-e35c; (3) ***"`W` refutes implications, not theorems"*** — L4 itself survives via branch (i) (`{x,b_1}` has `p = 1/2`, `δ(W) = 1/2`) and the 1/3–2/3 conjecture is untouched; (4) ***"do not record this as 'branch (ii) is unrepairable'" — that is a different claim and it is not established***; (5) **§7 property 5** — *in a minimal counterexample the rescue mechanism is exactly what is excluded*: if `δ(P) < 1/3` then every incomparable pair is unbalanced, **interface pairs included**, so a minimal counterexample is precisely a `P` where the migration both families exhibit does not happen — **which is either why the class "minimal counterexample + branch (ii)" is empty, or why it is not. That is the live question**, the auditor calls it the best paragraph in the document, and it is unaffected by the (IB) repair; (6) **the scope check passed and the deliverable deserves the credit** — it does **not** strawman: all five cited `.tex` ranges (`:464–474`, `:513–515`, `:527`, `:476–479`, `:567–569`) were pulled and verified verbatim by the auditor; (7) **it did *not* commit the "this route fails ⟹ no route works" conflation it was briefed on** — it guarded the conflation it was warned about and walked into its twin one level down, at the modulus quantifier.

**Ledger tally:** 27 CONFIRMED · 3 CONFIRMED-conditionally · 1 BROKEN · 1 REFUTED-as-stated · 1 omission (its own strongest claim) · 1 ungradeable prose numeric (*"a single deletion moves a pair from `1/3` to `1/2`"* — no derivation, configuration not pinned down; specify or drop) · **0 arithmetic errors**.
