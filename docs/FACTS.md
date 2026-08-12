# FACTS — the registry of true things that connect to nothing yet

**What this file is for.** `STATE.md` has three homes for a result and none of them fits a
fact with no consumer: *"The proof, and what's proven"* is what is **load-bearing** for the
current argument, *"The single lemma to prove"* is the **open target**, and the *"Attempt
index"* is the routes **already walked** so that nothing is re-walked. A statement that is
true, measured, and attached to no argument has to be filed as one of those three, and each
reading is wrong in its own way — load-bearing when it bears nothing, an open problem when it
is settled, or a dead end when it is alive. So in practice it stays in whichever deliverable
produced it and is findable only by whoever remembers that arc. **That is how a fact gets
rediscovered instead of reused**, and it is the exact failure the attempt index prevents for
dead ends with no counterpart for live ones.

Filed on Daniel's framing (`mg-03cf`, 2026-08-12): *"I would frame our research structure as
collecting useful facts and constructions which may at some point connect into a proof … AI is
demonstrably vastly better at closing problems within reach than identifying fruitful long term
research directions, so please try to be somewhat open minded about what could be useful
later."* **A fact does not need a consumer to be worth keeping.** Entries are admitted for
being true and measured, not for being useful, and an entry marked `UNEXPLAINED` is not a
lesser entry.

**What this file is NOT.** It is not a summary of `STATE.md` and it does not restate anything
`STATE.md` carries — where a row exists there, that row is authoritative and this file cites
it. It is not a verdict store: the compression arc's four verdicts live in their own documents
(§0 below) and are deliberately not paraphrased here, because a paraphrase drifts and a
citation cannot. And it is not a place to record that something *might* be true. **An entry is
a statement someone has either proved or measured, carrying the frame that makes it true.**

---

## THE ONE RULE THIS FILE EXISTS TO ENFORCE

> **Every entry carries its scope, and the scope travels with the number, always.**

A registry of figures separated from their populations would be a machine for manufacturing
`STATE.md` row 3b's `0/132` at scale — zero failures inside a frame chosen so that the known
failures are outside it, quoted afterwards as though it meant zero failures. So every entry
below states, without exception:

| field | what it must say |
|---|---|
| **STATEMENT** | the claim, with its quantifiers written out |
| **KIND** | `STATE.md:99`'s vocabulary — `U` / `U-id` / `FP` / `FP✗` / `OPEN`, or an explicit *weaker than `FP`* |
| **SCOPE** | proved, or verified over **which** population — exhaustive or sampled, to which `n`, with the caps |
| **FROM** | work item and document, so the entry can be re-read at source rather than trusted here |
| **NOT** | the near-miss reading it must not be mistaken for, where one exists |

**Kinds, one line each, `STATE.md:99` authoritative.** `U` proven for every finite poset ·
`U-id` an exact identity or definitional equivalence · `FP` an exhaustive check over a finite
set of small posets, saying **nothing** above the largest `n` checked · `FP✗` a finite
population exhibiting a **counterexample**, which is universal-strength · `OPEN` no warrant.

**And `STATE.md:99`'s standing rule (mg-957a) binds this file too:** *any prose that aggregates
entries must state the **weakest** kind in the set it names.* A sentence saying "the compression
arc proved …" over a set containing an `FP` entry is false however true each entry is on its
own.

**Admission test, so this file does not become a scrapbook.** An entry must be (1) true, with a
proof or a measurement behind it; (2) **homeless** — not a row in `STATE.md` and not the
headline verdict of its own deliverable, since a verdict is findable from its own title; and
(3) stated so that someone who has not read the source arc can use it. Facts failing (2) are
cited, not copied.

---

## §0. Where the source arc's verdicts live — cited, not restated

Every entry below comes from the **compression arc** of 2026-08-12 (`docs/imports/compression.tex`,
imported at `mg-2ffd`/`44d08ea`). **That arc has no row in `STATE.md` at all**, which is why so
many of its true statements are homeless at once — this is a first harvest, not a steady-state
rate.

| item | document | its own verdict, in its own words — **not re-derived here** |
|---|---|---|
| `mg-bb60` | [`OneThird-Compression-W1-LinearEigenfunction-Provenance-mg-bb60.md`](OneThird-Compression-W1-LinearEigenfunction-Provenance-mg-bb60.md) | the claim `compression.tex:217` attributes to us is **absent from every artifact searched** |
| `mg-623a` | [`OneThird-Compression-Novelty-mg-623a.md`](OneThird-Compression-Novelty-mg-623a.md) | **`duplicates-literature`** — the checkerboard compression is Wilson's even/odd sweeps |
| `mg-8bc7` | [`code/compression_audit_8bc7/README.md`](../code/compression_audit_8bc7/README.md) | §§1–3 **confirmed exactly**; (B)'s premise right and its conclusion refuted |
| `mg-409a` | [`OneThird-Compression-W4-Rate-mg-409a.md`](OneThird-Compression-W4-Rate-mg-409a.md) | the required rate **is not a rate**; `alpha ≤ 1` against a bar in `[2, 3)` |
| `mg-8d66` | [`OneThird-Compression-kFoliation-mg-8d66.md`](OneThird-Compression-kFoliation-mg-8d66.md) | the bar and the ceiling are both **`k`-independent**; `class-closed-by-ceiling` at every `k` |
| `mg-145f` | [`OneThird-Compression-Consumers-mg-145f.md`](OneThird-Compression-Consumers-mg-145f.md) | **`no-consumer-exists`** — the identity computes the numerator and not the denominator |

**Notation used below, fixed once.** `P` a finite poset on `n` elements, `L(P)` its linear
extensions with the uniform measure, `x ∥ y` incomparable. `p_xy = Pr[x before y]`;
`δ(P) = max_{x∥y} min(p_xy, 1−p_xy)` (`STATE.md:42`), and `δ(P) < 1/3` is **frozen**, the
(1/3)–(2/3) counterexample condition. `C_o`, `C_e` the odd and even sweep foliations, `Π_o`,
`Π_e` the corresponding conditional-expectation projections, `M = 2I − Π_o − Π_e`, `P_BK` the
Karzanov–Khachiyan chain, `A^o_xy`/`A^e_xy` the probability that `{x,y}` is a free 2-block of
`C_o`/`C_e`, `A_xy = A^o_xy + A^e_xy = Pr[x, y adjacent]` on incomparable pairs.
`alpha(P) = min` of `⟨f,Mf⟩/Var(f)` over non-constant `f`.

---

# THE REGISTRY

## F1 · Bias controls adjacency

**STATEMENT.** For every finite poset `P` and every incomparable pair `x ∥ y`,
`Pr[x, y occupy adjacent positions] ≤ 2·min(p_xy, 1−p_xy)`.

**KIND.** `U` — proved. The adjacent transposition of `x` and `y` is an involution of `L(P)`
carrying `{x,y adjacent, x first}` bijectively onto `{x,y adjacent, y first}`, so each has
probability `P(adj)/2`, and each is at most its own unconditional side.

**SCOPE.** Proved for every finite poset and every incomparable pair. Corroborated
exhaustively over every labeled poset at `n = 3, 4, 5` — 18 373 incomparable pairs, 0
failures — as one of the four links of `mg-8d66` `k4.2`, and **independently re-checked here**
on an implementation importing nothing from this repository: 21 063 pairs (`n = 3,4,5`
exhaustive + `n = 6` sampled 400, seed 20260812), 0 failures, `n ≤ 5` sub-population
reproducing `mg-8d66`'s 18 373 exactly
([`code/facts_registry_03cf/out_f1_adjacency_corollary.txt`](../code/facts_registry_03cf/out_f1_adjacency_corollary.txt)).
**ATTAINED**, with zero slack, at `n = 3` where a pair has `p = 2/3` and is adjacent in every
extension.

**FROM.** `mg-8d66` §4.2 Step 2,
[`OneThird-Compression-kFoliation-mg-8d66.md`](OneThird-Compression-kFoliation-mg-8d66.md)
(`ed3a949`). **Daniel named this entry specifically** when the registry was commissioned.

**COROLLARY, derived at `mg-03cf` and stated nowhere in the corpus.** Since
`min(p_xy, 1−p_xy) ≤ δ(P)` for every incomparable pair by definition of `δ`:

> **at every frozen poset, `Pr[x, y adjacent] ≤ 2·δ(P) < 2/3` for EVERY incomparable pair.**

**KIND `U`, and its warrant is the derivation and NOTHING ELSE.** ⚠️ **No measurement of this
corollary is possible.** Frozen *is* the counterexample condition and the conjecture is verified
to `n = 14` (`mg-33f5`), so the population of frozen posets any instrument can enumerate is
**empty**. `f1_adjacency_corollary.py` runs it anyway and prints `0 frozen posets` with the
reason attached, precisely so that its `0 failures` is never read as a clean sweep. That number
is zero failures in an empty population and carries no information.

**NOT.** ⚠️ **The implication runs bias ⟹ adjacency and NOT the reverse.** A pair that is
rarely adjacent may be perfectly balanced: at `p = 1/2` the bound reads `P(adj) ≤ 1` and is
vacuous, so **no adjacency measurement certifies balance** and nothing here bounds `δ(P)` from
below. It is also not a bound on the *number* of adjacent pairs — that is F2, which is exact
and goes the other way.

---

## F2 · The adjacency budget is exactly `n − 1`

**STATEMENT.** For every finite poset `P` on `n` elements,
`Σ_{all pairs {x,y}} A_xy = n − 1` **exactly**, where `A_xy = Pr[x, y adjacent]`.

**KIND.** `U-id` — an identity by slot counting. Every linear extension has exactly `n − 1`
adjacent position slots and each slot is occupied by exactly one pair; take expectations.

**SCOPE.** Proved, by counting alone, with **no foliation, fiber, projection or block system in
either path**. Verified at 328 posets (`n = 3, 4` exhaustive; `n = 5` sampled 60, seed 31;
`n = 6` sampled 30, seed 37), 0 failures, exact rationals; a second, pair-indexed route
reproduces it at 80 of them (`mg-145f` `e3.1`, `e3.4`). Control: distance-2 in place of
distance-1 does **not** give `n − 1`.

**SATURATION.** The antichain `A_n` has **zero slack** at `n = 3, 4, 5, 6, 7` — its
incomparable pairs alone exhaust the whole budget, because it has no comparable pairs
(`mg-145f` `e3.3`, `FP` at `n ≤ 7`).

**FROM.** `mg-145f`, [`OneThird-Compression-Consumers-mg-145f.md`](OneThird-Compression-Consumers-mg-145f.md)
§0 and `code/compression_consumers_145f/out_e3_density.txt` (`e09226c`).

**NOT.** ⚠️ **`= n − 1` is over ALL pairs; over INCOMPARABLE pairs only it is `≤ n − 1`,** with
the difference taken by comparable pairs that happen to be adjacent. Quoting the equality with
the population dropped is the whole error class this file guards against. And because a
density-`1` poset satisfies it with **equality**, it cannot certify any density bound
`d(P) ≤ D < 1` — that is `mg-145f`'s reason for ruling target **(R)** unreachable, and it is a
reason the identity is too weak, not evidence about `(R)` itself.

---

## F3 · The within-fiber share of an element's position variance is capped at `1/4`

**STATEMENT.** For every finite poset `P` and every element `x`,
`E Var(pos_x | C_o) = (1/4) Σ_{y ∥ x} A^o_xy ≤ 1/4`, uniformly in `n`; likewise for `C_e`.

**KIND.** `U` — proved, from `Σ_y A^o_xy = Pr[x lies in a free odd 2-block] ≤ 1`. **And
attained.**

**SCOPE.** Proved for every poset and every element. The identity form and the cap are both
checked directly against the fiber computation at **2 666** (poset, element, parity) triples —
`n = 3, 4` exhaustive, `n = 5` sampled 50 (seed 5), `n = 6` sampled 25 (seed 23) — 0 failures,
maximum observed exactly `1/4` (`mg-145f` `e2.3`).

**AND THE CONSEQUENCE THAT MAKES IT WORTH KEEPING.** Against `Var(pos_x) = (n²−1)/12` on the
antichain, the share the identity computes falls `0.250 → 0.200 → 0.100 → 0.0857 → 0.0536` over
`n = 3…7`, i.e. `Θ(n⁻²)` (`e2.4`, exact rationals, `FP` at `n ≤ 7` for the tabulated values and
`U` for the `1/4` cap that forces the decay). **A degree-one statistic's within-fiber variance
is a bounded local quantity; the `(B)` quantity it would have to control is global.**

**FROM.** `mg-145f` §0 and §4(c).

**NOT.** Not a bound on `Var(pos_x)`, which is unbounded. It is a bound on the **first summand
of the law of total variance** `Var(pos_x) = E Var(pos_x|C_o) + Var(E[pos_x|C_o])` — the
between-fiber summand is where the programme's `(B)` and `(B-cov)` targets live (F11).

---

## F4 · `E_BK(inv_e) ≤ 1/2`, by a second route

**STATEMENT.** For every finite poset `P`, `inv_e` being the inversion count against the
distinguished order, `E_BK(inv_e) = Σ_{x∥y} E_BK(f_xy) = (1/(2(n−1))) Σ_{x∥y} A_xy ≤ 1/2`,
**attained**.

**KIND.** `U` — follows from F2 and F3.

**SCOPE.** Proved. Verified at **295 posets** (the `n ≤ 6` population of F2, minus those with
no incomparable pair), 0 failures, exact rationals, maximum exactly `1/2` (`mg-145f` `e3.5`).

**WHY IT IS HERE AND NOT MERELY A RE-PROOF.** This is `step8.tex`'s own **Step 1**, reached from
the compression identity by a different route on an implementation that had never seen it —
an independent re-derivation of a load-bearing step of the corpus's own Theorem E.

**FROM.** `mg-145f` §3 row 6 and `e3.5`; the target it reproduces is `step8.tex` Step 1 via
`mg-409a` L3.

**NOT.** ⚠️ **`E_BK(inv_e)` is not `E[inv_e]`, and the `1/2` says nothing about the latter.** A
Dirichlet form is not a mean: the value is `≤ 1/2` **whatever `E[inv_e]` is**, so it carries
**zero** information about `STATE.md` row 8 / (LIB), which is a statement about `E[inv_e]`.
Sharpening it buys nothing downstream either, because Theorem E consumes a **cut** and not a
number.

---

## F5 · The full-space operator inequality

**STATEMENT.** For every finite poset `P` and **every** `f ∈ L²(L(P))`,

> `⟨f, (I − P_BK) f⟩ ≥ (2/(n−1)) ⟨f, (2I − Π_o − Π_e) f⟩`,

with **equality exactly when `f` is affine (degree ≤ 1) on every fiber of both foliations**.
Consequently `λ₂(I − P_BK) ≥ (2/(n−1)) λ₂(M)`, unconditionally.

**KIND.** `U` — proved by hand (per-fiber cube-Fourier expansion: the odd swaps inside an odd
fiber are exactly the `d` coordinate flips, the cube Dirichlet form acts on `χ_S` with
eigenvalue `2|S| ≥ 2` with equality iff `|S| = 1`; same for even; add). ⚠️ The **certification**
below is `FP`; the proof is the warrant.

**SCOPE.** Certified by **exact rational Schur reduction of the full `|L(P)| × |L(P)|` matrix**,
PSD at **599/599** posets — all 209 labeled posets at `n ≤ 4` with at least two linear
extensions, plus 390 at `n = 5` with `|L(P)| ≤ 48`. No float on the verdict path.

**SHARPNESS, measured rather than asserted.** The constant `2` is **optimal**: raising it to
`5/2` breaks PSD at **192/192** posets, while lowering it to `1` keeps PSD at **0/192**
failures, so `2` is the boundary and not merely a value that happens to work. The reverse
inequality fails at **139/192** posets, so the two operators are not equal and the statement is
not vacuous.

**FROM.** `mg-8bc7`, [`code/compression_audit_8bc7/README.md`](../code/compression_audit_8bc7/README.md)
§*The finding*, arms `a5.1`–`a5.2`, controls `C1`–`C3` (`fa29801`).

**NOT.** ⚠️ **The constant `2/(n−1)` is tied to a normalization and does not travel further than
the sentence that states it.** Under the lazy variant — draw a position, then swap with
probability `1/2` — the Dirichlet form halves while `E Var(f|C)` does not, and the constant
becomes `1/(n−1)` (`mg-8bc7` `a2` control N5, 0/268 disagreements). Also **not** the identity
`(*)`: `(*)` is the **equality case** of this inequality, so it is a statement about
fiber-affine `f` and this is a statement about all `f`. And the useful direction is the one
written: a **small** eigenvalue of `M` is not evidence against the programme.

---

## F6 · The refinement family's ceiling IS the spectral gap

**STATEMENT.** For the `k`-foliation family indexed by partitions `S` of the `n−1` swap
positions: (i) if `S'` refines `S` then `Q_{S'} − Q_S` is PSD, hence `alpha_S ≤ alpha_{S'}`;
(ii) the refinement order has a top, admissible at every `n`, namely all singletons `k = n−1`;
(iii) **at the top, `Q_finest = ((n−1)/2)(I − P_BK)` as an exact matrix identity**. Therefore
`sup_k alpha_k = ((n−1)/2)·gap_BK`, **attained**, and the family's own bound at `S = finest`
reads `gap_BK ≥ gap_BK`.

**KIND.** `U-id` for (iii) — `Π_p = (I + T_p)/2` on legal swaps and `I` on illegal ones, so
`Σ_p Π_p = ((n−1)/2)I + (1/2)Σ_p T_p` while `(n−1)P_BK = Σ_p T_p`. `FP` for the verifications.

**SCOPE.** (iii) checked **entrywise in exact rationals at 373 posets** (`n = 3, 4` exhaustive;
`n = 5` sampled 120; `n = 6` sampled 60; 8 posets with `|L(P)| > 130` skipped **and counted**)
— `mg-8d66` `k2.1`. (i) at **2 032** (poset, refinement) instances, 0 failures, exact, with the
reversed comparison refused at 38 of 61 (`k3.1`, `k3.2`). And the constant is **one constant
for every partition**: `((n−1)/2)(I − P_BK) − Q_S` is PSD at **1 728 of 1 728** (poset, `S`)
pairs, over *every* admissible partition at each poset (`k2.2`).

**FROM.** `mg-8d66` §5, [`OneThird-Compression-kFoliation-mg-8d66.md`](OneThird-Compression-kFoliation-mg-8d66.md)
(`ed3a949`).

**NOT.** ⚠️ **Not a route to a better bound.** The family is a family of **weakenings** of the
spectral gap indexed by how coarse the foliation is; refining recovers loss and can never
exceed the gap. The `k` at which the ceiling is highest is the `k` at which each fiber is a
**one-dimensional** cube — a single swap — i.e. where the compression has compressed nothing.

---

## F7 · `alpha > 0` is free

**STATEMENT.** For every finite poset `P` with `|L(P)| ≥ 2`, `alpha(P) > 0`.

**KIND.** `U` — one line. `Mf = 0` iff `Π_o f = Π_e f = f` iff `f` is constant on every odd and
every even fiber, i.e. invariant under all `τ_odd` and all `τ_even`, i.e. constant on each
component of `G_BK`; and `G_BK` is connected (Karzanov–Khachiyan).

**SCOPE.** Proved. Connectivity checked independently at **4 468/4 468** posets (`n ≤ 5`
exhaustive plus `n = 6` sampled) by pure union–find — no eigenvalue, no float (`mg-409a`
`r1.1`).

**FROM.** `mg-409a` §3, [`OneThird-Compression-W4-Rate-mg-409a.md`](OneThird-Compression-W4-Rate-mg-409a.md).

**NOT.** ⚠️ **Positivity buys nothing here and the entry is registered as a construction, not a
lead.** Positivity of the BK gap is *already* unconditional in this corpus (connectivity;
Bubley–Dyer `n³ log n`), and `alpha` is capped at `1` against a bar in `[2, 3)` — see §0's
`mg-409a` and `mg-8d66` rows, which is where the ceiling lives. What is worth keeping is the
**one-line route**, which is cheap and reusable, not the conclusion.

---

## F8 · The full pair-bias multiset determines `alpha` — UNEXPLAINED

**STATEMENT.** Keyed on the isomorphism-invariant multiset `{ min(p_xy, 1−p_xy) : x ∥ y }`,
**no two posets sharing a key have different `alpha`** on any population tested. Meanwhile the
**scalar** `δ(P)` does **not** determine `alpha`: `A_n` (antichain) and `Z_n` (ordinal sum of
`n/2` two-element antichains) both have every incomparable pair at `p = 1/2` exactly, hence
`δ = 1/2`, while `alpha(A_n) ≤ 6/(n(n+1)) → 0` and `alpha(Z_n) = 1` — a factor `Θ(n²)` apart at
the same `δ`.

**KIND.** The **refutation** for the scalar is `FP✗` and therefore universal-strength —
verified exactly at `n = 4, 6, 8` (`mg-409a` `r5.1`), with `alpha(Z_n) = 1` checked to `n = 12`.
The **regularity** for the multiset is `FP` and nothing more.

**SCOPE.** It is the whole content of this entry.

| `n` | population | buckets | buckets merging **>1** iso class | buckets with `alpha` spread |
|---|---|---|---|---|
| 4 | exhaustive | 10 | 4 | **0** |
| 5 | exhaustive | 33 | 22 | **0** |
| 6 | **sampled (60)** | 39 | 5 | **0** |

The third column is the **vacuity control**: the buckets genuinely merge non-isomorphic posets,
so "0 spread" is not the tautology "isomorphic posets agree". `n ≤ 5` exhaustive, `n = 6`
sampled at 60, **nothing above `n = 6`**.

**STATUS: UNEXPLAINED.** No proof, no mechanism, no counterexample. It is registered because it
is a clean measurement of an unexplained regularity.

**FROM.** `mg-409a` §6(b) and D3.

**PROVENANCE OF THE ENTRY ITSELF, on `pm-onethird`'s instruction to put it on the record.**
`pm-onethird` told `p409a` **not** to ticket this finding, on the reasoning that `alpha` is
capped and useless for (1/3)–(2/3) so the finding had *"no route value however pretty it is"*.
That decision is **reversed here**: a fact does not need a consumer to be worth keeping, and an
unexplained regularity with a clean measurement is exactly what this file is for.

**NOT.** ⚠️ **Not evidence that `alpha` is *computable* from pair biases, and not a theorem.**
It is 0 collisions on three populations, the largest of which is `n = 5`; `n = 6` is a sample of
60. It also does **not** revive the compression route — `mg-409a` §2's ceiling is a statement
about `alpha`'s **value**, and no representation of a quantity raises it. ⚠️ And a warning from
the source: the first version of this measurement keyed on the multiset of `p_xy` over
**label-ordered** pairs, which is **not** an isomorphism invariant, and returned a clean answer
anyway (30 buckets at `n = 4`, where there are only 16 isomorphism classes). The corrected key
gives the same "0 spread" — so the defect did not change the finding, which is exactly the case
in which such a defect normally goes unrecorded.

---

# SWEPT — further homeless facts from the same arc

Eight additional entries, found by reading the arc's five deliverables and their instrument
transcripts rather than their verdicts. Each meets the same admission test.

## F9 · The bottom BK eigenfunction is usually not a pair-orientation statistic

**STATEMENT.** `gap_lin ≥ gap_BK` always (the minimisation is over a subspace), and the
inequality is **strict at a rising fraction of posets**.

**KIND.** `U` for the direction — the variational principle. `FP` for every fraction below.

**SCOPE.** `[FLOAT]` — both quantities are eigenvalues, by cyclic Jacobi, worst off-diagonal
residual `9.8e-13` over the run. Population caps stated at source: posets with `|L(P)| > 24`
are skipped (301 of 4231 at `n = 5`, **including every large antichain**), and the measurement
stops at `n = 5`.

| `n` | posets | in population | skipped | `gap_lin > gap_BK` | `gap_lin < gap_BK` |
|---|---|---|---|---|---|
| 3 | 19 | 13 | 0 | **0 of 13** | 0 |
| 4 | 219 | 195 | 0 | **61 of 195** | 0 |
| 5 | 4231 | 3810 | 301 | **2260 of 3810** | 0 |

Worst ratio `1.063001` at `n = 5`. `gap_lin < gap_BK` never occurs, as it must not.

**FROM.** `mg-623a` §3, [`OneThird-Compression-Novelty-mg-623a.md`](OneThird-Compression-Novelty-mg-623a.md)
(`9b692d7`). The parallel measurement on `M` rather than `I − P_BK` — `alpha_full ≤ alpha_lin`,
strict at 61 of 195 at `n = 4` — is `mg-409a` §0.

**NOT.** Not a claim that the fraction tends to 1; `0 %, 31 %, 59 %` is three points under a
cap that excludes the antichains, which are exactly the posets with the largest `|L(P)|`.

---

## F10 · The energy identity is sign-blind and level-blind

**STATEMENT.** The identity's entire measure-dependent output is `(A^o, A^e)`, and it depends
on the coefficient vector `c` only through `c²`. Hence (i) flipping the sign of any coefficient
leaves the output **exactly** fixed, and (ii) the output is invariant under `f ↦ f + a`, so
**no first moment of any pair-orientation statistic is ever emitted**.

**KIND.** `U-id` for the output map — two lines from `compression.tex:94` by taking
expectations. `FP` for the non-vacuity measurements.

**SCOPE.** Output map verified at **1 475** (poset, coefficient-vector) instances over 328
posets (`n = 3, 4` exhaustive; `n = 5` sampled 60, seed 7; `n = 6` sampled 30, seed 13), exact
rationals, 0 failures. Non-vacuity of sign-blindness: a one-coefficient flip moves `Var(f)` at
**201 of the 250** posets of that population having at least two incomparable pairs (49 do not;
worst relative move 4), so the blindness costs something real. Level-blindness checked at the
**74** posets with an incomparable pair among the first 80 of the population: 0 output changes
against 74 mean changes.

**FROM.** `mg-145f` `e1.1`–`e1.3`.

**NOT.** Not a statement that the identity is weak in general — it computes the numerator of the
Rayleigh quotient **exactly**. It is a statement about which targets are **reachable**: every
first moment (`E[inv_e]`, `E[pos_x]`, `p_xy`, the position matrix, `δ(P)`, `Δ₁`), everything
sensitive to coefficient signs (pair-indicator covariances, i.e. `(B-cov)`), and every
degree-two statistic (`E[Σ disp²]`, i.e. `(B)`) are outside its range.

---

## F11 · The covariance the compression kills is not the covariance `(B-cov)` needs

**STATEMENT.** Inside a fiber the covariance is **zero for a trivial reason** — every pair
indicator is either a free Bernoulli on its own 2-block or constant, and distinct free blocks
are disjoint. The `(B-cov)` residual's same-side covariance `C_x = Σ_{y≠z} Cov(s_xy, s_xz)` is a
**between-fiber** quantity and sits entirely in the other summand of the law of total variance.

**KIND.** `FP` — both halves are measurements at `n ≤ 6`, partly sampled.

**SCOPE.** Within-fiber: **0 nonzero / 1 326** (fiber, pair, pair) triples. Between-fiber:
`C_x > 0` at **555 of 555** (poset, element) rows and `< 0` at **none** — the FKG/XYZ wrong sign,
reproduced. Population: `n = 3, 4` exhaustive, `n = 5` sampled 50 (seed 5), `n = 6` sampled 25
(seed 23).

**FROM.** `mg-145f` §4(a)–(b), `e2.1`–`e2.2`.

**NOT.** ⚠️ **`compression.tex:98`'s "no covariance terms whatsoever inside a compressed fiber"
is TRUE and is about a quantity that was never nonzero.** The shapes of the two claims match
exactly and the objects do not. Registering the near-miss is the point of the entry.

---

## F12 · The parity aggregation is a genuine loss

**STATEMENT.** `A^o` and `A^e` **are** the per-slot adjacency probabilities aggregated into two
parity buckets — and the aggregation is lossy, collapsing two or more nonzero per-slot summands
into one bucket at a measurable fraction of pairs.

**KIND.** `FP`.

**SCOPE.** The identification holds with **0 mismatches**; the collapse occurs at **70 of 921**
incomparable pairs, over the first 100 posets of a population that is `n = 3, 4` exhaustive,
`n = 5` sampled 50 (seed 41), `n = 6` sampled 25 (seed 43) — `mg-145f` `e4.3`.

**FROM.** `mg-145f` §0 and `e4.3`.

**NOT.** Not a claim that the per-slot data is unavailable — it is, from the chain directly. It
is a claim about what **the identity emits**, which is strictly weaker than what `STATE.md:158`'s
adjacency-symmetry consumer took as its input.

---

## F13 · Order reversal exchanges the two foliations iff `n` is odd

**STATEMENT.** Reversal `L ↦ (x_n,…,x_1)` is a bijection `L(P) → L(P^op)` sending 0-indexed
position `p` to `n−1−p`, which **preserves position parity iff `n` is even**. Hence for `n` odd
the pair `(C_o, C_e)` on `P` is carried to `(C_e, C_o)` on `P^op` — a genuine symmetry up to
duality — and for `n` even each foliation is carried to **itself**.

**KIND.** `U-id` for the parity arithmetic. `FP` for the verifications and for the non-vacuity
count.

**SCOPE.** `n` odd: **0/479** violations as fiber-size multisets. `n` even: **0/282** for
self-preservation, and the exchange genuinely **FAILS** at **197 of 279** posets — so the
distinction is not vacuous. `n = 2…7` (`mg-8bc7` `a4.3`).

**FROM.** `mg-8bc7` §(A), [`code/compression_audit_8bc7/README.md`](../code/compression_audit_8bc7/README.md).

**NOT.** Not a symmetry of `P` — it is a symmetry **up to duality**, relating `P` to `P^op`.

---

## F14 · The two projections are not interchangeable

**STATEMENT.** `M = 2I − Π_o − Π_e` is symmetric in **form** and the two projections are not
symmetric in **fact**: `rank Π_o < rank Π_e` at **127 of 219** posets at `n = 4` (equal at 80,
greater at 12).

**KIND.** `FP`.

**SCOPE.** Exhaustive at `n = 4`. Nothing above.

**FROM.** `mg-8bc7` §(A), `a4.4`.

**NOT.** ⚠️ Not a defect in the energy identity `(*)`, which is unperturbed at both parities
(4 420 statistics, 0 violations in every cell) because it never **compares** the two foliations
— it adds them, and they are free to be arbitrarily lopsided (the extreme case: at `n = 2`,
`Π_e = I` and one term of `(*)` vanishes identically, and `(*)` is still exact). What it
constrains is **arguments**: no step in `compression.tex` §4 or §5 may treat `Ran Π_o` and
`Ran Π_e` as interchangeable.

---

## F15 · The equality set of F5 is strictly larger than the linear-statistic space

**STATEMENT.** The equality case of F5 — `ker D`, `f` affine on every fiber of both foliations —
is **strictly larger** than `V`, the space of pair-orientation linear statistics.

**KIND.** `FP` for the strictness count; `U-id` for the two-route identification of `ker D`.

**SCOPE.** `ker D` is *exactly* the fiber-affine space, computed by **two independent routes**
(null space of `D`; vanishing of every order-2 cube difference) agreeing at **112/112** posets.
`dim ker D > dim V` at **37 of those 112**.

**FROM.** `mg-8bc7` `a5.2`, `code/compression_audit_8bc7/out_a5_general.txt`.

**NOT.** Not the same as `V` being invariant — it is not, under any of `Π_o`, `Π_e`, `M`,
`(I − P_BK)`, with the 3-element antichain as the smallest certificate. The relation `(***)` is
a **pointwise identity of functions** on `V` (checked at 8 720 (poset, `f`) pairs), which is
strictly stronger than equality of quadratic forms and needs no invariance.

---

## F16 · `alpha` has a two-projection closed form, and `θ_min(A_n) = π/n`

**STATEMENT.** By Halmos's 1969 two-projection theory,
`alpha(P) = 1 − cos θ_min` with `cos θ_min = √(λ_max(Q_o Q_e Q_o))`, `Q_o = Π_o − P_1`,
`Q_e = Π_e − P_1`; and on the antichain the angle has a clean closed form,
`θ_min(A_n) = π/n` (45.00° at `A_4`, 36.00° at `A_5`).

**KIND.** `U-id` for the closed form — the two-projection decomposition, with the `Ran Q_o ∩
Ran Q_e` part shown empty at every poset by F7's connectivity. `FP` for `θ_min(A_n) = π/n`,
which is checked at **`n = 3, 4, 5` only**.

**SCOPE.** `[FLOAT]` — the closed form is verified on this instrument at **233 posets**, worst
disagreement `7.8e-15` (`mg-409a` `r6.1`). `Z_n` is the degenerate case: `Ran Q_o = {0}`, every
angle `π/2`, `alpha = 1` — the largest a principal-angle bound can ever return.

**FROM.** `mg-409a` §6 / `r6.1`.

**NOT.** ⚠️ **`1 − cos θ ≤ 1` is an identity**, so the closed form is also the proof that no
principal-angle theorem, published or future, puts `alpha` over the bar — the ceiling is a
property of the object and not a limit of the tools. The `π/n` law is three data points and is
registered as a `FP` curiosity, not a theorem.

---

# Housekeeping

**Adding an entry.** Append it with all five fields. If you cannot write the **SCOPE** line —
proved, or which population, exhaustive or sampled, to which `n`, with the caps — the entry is
not ready, and the fix is to go and measure the scope rather than to soften the statement. If
you cannot write **NOT**, say so explicitly rather than omitting the field, so that a reader can
tell "no near-miss exists" from "nobody looked".

**Removing an entry.** An entry that is **refuted** is not deleted — it is restated as `FP✗`
with the refuter, because a refutation is a fact. An entry that gets a consumer is **not**
deleted either: it is cited from `STATE.md`, and the registry entry stays as the record of its
scope. Deletion is for entries found to have been **false as stated**, and then the reason goes
in the same commit.

**Why here and not in `STATE.md`.** Three reasons, in order of weight.

1. **A registry grows monotonically, and `STATE.md` is size-ratcheted** against a declared
   ceiling (`mg-e331`, [`code/state_ratchet_e331/CEILING.json`](../code/state_ratchet_e331/CEILING.json)),
   which `./build.sh` enforces as a **merge gate**. Putting a permanently-growing structure
   under a monotone floor makes every future fact a ceiling raise, and the predictable outcome
   is not a smaller registry — it is facts not being logged. That is how a control gets deleted
   or quietly suppressed inside a week, and `CEILING.json`'s own text names that failure mode.
2. **`STATE.md`'s three sections are all defined by their relation to the current argument.** A
   fact with no relation to the argument can only be filed by pretending it has one, and each
   available pretence — load-bearing, open, walked — is a different wrong reading.
3. **The two files are ordered by different things.** `STATE.md` is ordered by the argument, so
   its rows move when the argument moves. A fact's row should not move when the argument moves;
   this file is ordered by provenance and kind.

**And the pointer in `STATE.md` is not optional.** A registry nobody links to is exactly as
findable as the deliverables it was built to rescue facts from. `STATE.md` carries one
sentence pointing here, and those words could not live in `docs/state-history/` for the reason
`mg-e331` gives about its own pointer: **a pointer is only discoverable at the site the reader
already reads.**
