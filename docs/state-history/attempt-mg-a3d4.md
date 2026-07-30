# Attempt index — AMBER-POSITIVE · THE BET IS PRICED (mg-a3d4): does the face/Hodge side carry technique the graph side lacks?

Per-row history for `STATE.md` § *Attempt index*, the **AMBER-POSITIVE · THE BET IS PRICED (mg-a3d4)** row.
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

### H1 — Theorem G's proof, the independent rebuild to A_12, and its methodological sizing

**This is the arc's best METHODOLOGICAL result to date and it is why the row leads with it:** Theorem G is the statement quantified over `n` rather than over posets — the place this arc's failure had landed six times (Appendix A step 4d) — and it is the first such statement in the arc that was **named as the hazard, given a proof rather than a trend, and had the proof survive an external rebuild.**

### H2 — the inherited conditional that was carried nowhere else

**That conditional was declared in the self-audit and carried nowhere else** — not into ledger row N1, not into row S1's condition list, not into the proposed `STATE.md` row whose own opening line was *"carries its own conditions rather than pointing at them"*.

**That is mg-5630's defect class and it is repaired, not annotated** (rows N1a/N1b/N1c/N1r, §7.1).

### H3 — what ledger row B6 used to read, and why "undecided" was a resting place

The proposed row used to read *"`Δ_AT` is NOT a Brown walk … undecided by that test exactly where `\|L(P)\| ≤ 4`"*.

**That "undecided" was a resting place, not a fact.**

**The old clause survived only inside the hedge *"on the tested population"*, and the hedge was doing all the work.**

### H4 — the control battery: absorbability, two repaired calibration defects, and what could not be broken

**CONTROLS — the credit was verified rather than assumed, and it is the half of this that matters most.**

Two calibration defects repaired: **X1a's retirement rested on a false structural claim** (*"uniform weights inflate `γ`, so it can never falsify (LG)"* — measured: smaller `λ₂` on **75 of 2748 links**, smaller `γ_i` on 9 levels, a strictly **larger** mutated bound on **4 posets**; X1a is **empirically silent here, not structurally incapable** — the same instance-read-as-law shape, inside the section the self-audit certified clean), and **X2 is a DISTINGUISHABILITY check, not a falsification control** (its mutation changes 4946 faces and falsifies **nothing** downstream, 0 of 81 — though it is **not** a gauge and **not** unfalsifiable: injecting the exact bug it mutates toward makes it go silent, so it does guard that one alternative construction).

**The four downstream-failure rows are NOT downgraded**; what changed is that the table now states which kind of evidence each row carries.

**The one control gap the deliverable named itself — no control perturbs the Theorem G eigenfunction computation — is CLOSED by the audit's own rebuild.**

**What could not be broken:** Theorem G; the `2^{Θ(n)}` conclusion; the identity-as-evidence trap (absent throughout — §1 states the trap and avoids it, and no comparison in §5 or §9 recomputes `λ₂(Δ_AT)` and calls the agreement evidence); the negative's coverage (all four candidate techniques taken at strength, **no weaker version refuted** — localisation is conceded to be *shared* with the graph side and the missing thing correctly identified as the inequality that consumes it); disclosure (the `A_6` skip in four places, X1a's non-firing in the table not only the prose, T′ carrying HEURISTIC into the STATE row itself).

### H5 — the mechanism recorded beside the G″ strike

**STRUCK, with the mechanism recorded next to the strike, because the mechanism is the valuable part and it is this arc's signature failure stated cleanly: Theorem G's face is one size-`m` block plus `i+1` SINGLETONS; singletons contribute no factor to Theorem L's join, so THERE the link is not a join at all. Drop the singleton requirement — which is exactly what `G″` did — and the link is a genuine join `F(A_m) * Y`, in which a factor's eigenfunction survives SCALED BY `p/(p+q+1) < 1`. An exact `1/2` in a factor is STRICTLY LESS than `1/2` in the join. THE STRENGTHENING WAS NOT FREE: THE DROPPED HYPOTHESIS WAS THE ONE DOING THE WORK.**

### H6 — the sweep that established nothing consumed G″

**Nothing consumed `G″`, and that is swept for rather than assumed**: three sites in the repository (the deliverable's §6 paragraph, the ledger row, and the mg-86a3 audit cell that originated the sentence — now annotated), **no consumer anywhere, and it never appeared in this document at all.**

## Supporting record — derivations, constructions, evidence and audit provenance

*These passages support claims the row still states. They moved so that the row reads as an
assertion rather than as an argument. **No claim moved with them**; where a passage carried
both a claim and its evidence it stayed in the row.*

Every level's link of `F(A_n)` has `λ₂ ≥ 1/2` by an explicit eigenfunction (`f(S) = Σ_{i∈S}a_i`, `Σa_i = 0`, eigenvalue exactly `1/2`, **`n`-free** — Theorem G), so the cited product-form local-to-global bound for the antichain is **at most `2^{3−n}`** against a truth of `2−2cos(π/n) = Θ(n^{−2})` from the cited Caputo–Liggett–Richthammer proof of Aldous' conjecture.

**The deliverable's own §13 named this proof as the single thing an auditor had to rebuild from scratch. The auditor rebuilt it — by hand, AND from the definition of the Coxeter complex with NO shared link code — and it held: `Pf = f/2` exact in rational arithmetic to `A_12` against the deliverable's `A_8`, `λ₂ = 1/2` exact to `A_9` against row G′'s `A_7`, under three different `a`-vectors, with three attempts to break it (a different construction of the complex, different `a`-vectors, `m` to 12) all failing.**

*"Complete, `n`-free, no gap; the strongest thing in the document."*

Under the *other* reading — no boundary quotient, the absolute top Laplacian — the auditor verified on **all 405 posets** that `E·L^abs_top·E = (n−1)I − A`, the shifted adjacency matrix of the same AT graph (`deg + #free = n−1` also 405/405).

Two new theorems license the import — **the AT walk IS the standard down-up walk on the facets, `I − P_du = Δ_AT/(2(n−1))` (PROVEN, 405/405 twice)**, and **localisation: `link_{F(P)}(σ)` is the simplicial join of the `F(Q_i)` over the induced subposets on `σ`'s blocks (PROVEN; a simplicial isomorphism on all 6197 faces, `n ≤ 5`)** — and the cited bound (Alev–Lau; Kaufman–Oppenheim; ALOV) is then **never violated on any of the 404 posets `2 ≤ n ≤ 6` and never worse than a factor 2.6204 there**, while being `2^{Θ(n)}` off on the antichain by Theorem G.

`γ_i ≤ 1/2` on all 404 and attained by 373, so **this is not about antichains**: removing the braid hexagon does not help (`C_a ⊔ C_a` has no 3-antichain and still has `γ_i = 1/2`; the fence reaches `0.46` and still decays geometrically).

**`1/2` is the fixed point of Oppenheim's trickling-down recursion `γ ↦ γ/(1−γ)`, so `F(P)` sits exactly where the hierarchy carries no information** — and the property that puts it there is the **pseudomanifold** property, mg-276d Lemma 3(a), *the same fact that makes the bridge's "relative" well-posed* (that causal reading is labelled HEURISTIC; the codim-2 consequence is proved: 44 055 links over `4 ≤ n ≤ 6` are exactly `C_6`, `C_4`, `P_4`, `P_3`, `P_2`, every per-shape count reproduced identically, which also settles the source's claim (4) **PROVEN and quantitative**).

`F(P)` is a left regular band under successive refinement (0 axiom violations, all 87 posets `n ≤ 5`, and the audit checked the proof step by step: it holds for **all finite posets**, the sweep being a check on it) whose support lattice is exactly the **acyclic partitions** of `P` (which are **not** closed under refinement — witness `{a<c,b<d}` with `{a,d}\|{b,c}`), so **Brown's theorem (CITED) diagonalises every face-driven walk on `L(P)`: `λ_X = Σ_{supp(y) ≤ X} w(y)` indexed by acyclic partitions, multiplicities fixed by `Σ_{Y ≥ X} m_Y = ∏_{B∈X}\|L(P\|_B)\|` — independent of `w`.**

Verified against the actual matrix by exact rational rank computations (eigenvalues, multiplicities **and** diagonalisability) on all 24 posets `n ≤ 4` under three weight families; **the audit re-ran it under SIX, reusing the same `m_X`, which is what "independent of `w`" has to mean operationally, and got 24/24 under all six.**

`A_6` was skipped and that is stated in four places, not hidden.

Sharpest control: the **Tsetlin library** — Brown's prediction reproduces the classical derangement-multiplicity spectrum exactly (`n ≤ 5`) with derangements appearing nowhere in the code.

§9.4's test is only *sufficient*; the actual question is a **finite linear feasibility problem with rational data**, and solving it exactly (Phase-I simplex over `Fraction`) **DECIDES every case the deliverable left open and decides every one POSITIVELY** — the lazy AT walk **IS** a Brown walk there, with exact rational witnesses, on 1/2/4/7 posets at `n = 2..5` (the deliverable's own NOT-counts 0/2/11/55 reproduced exactly, so its test is faithfully implemented and correctly described).

**And the `\|L(P)\| ≤ 4` threshold is an artifact of stopping at `n = 5`:** 12 positives among the `n = 6` posets with `\|L(P)\| ≤ 14`, one of them with `\|L(P)\| = 8`, and the **infinite** family `V_k` — the ordinal sum of `k` two-element antichains, `n = 2k`, `\|L(P)\| = 2^k` unbounded — is positive for every `k` tested.

mg-5630's absorbability test was applied to all six mutations: **NONE is a gauge in disguise, none is absorbable into a parameter the battery already varies, and X1b/X3/X4/X5 are each scored by a downstream FAILURE — so mg-5630's specific defect is NOT repeated here.**
