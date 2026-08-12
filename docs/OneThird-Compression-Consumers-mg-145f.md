# OneThird — ENUMERATE THE CONSUMERS: **the identity computes the NUMERATOR of the Rayleigh quotient exactly and the DENOMINATOR not at all, and every open target in this programme lives in the denominator.** `no-consumer-exists`

**Work item.** `mg-145f` (repo `onethird_program`), filed by `pm-onethird` on Daniel's
suggestion after `mg-409a`. The **target** half; `mg-8d66` is the `k` half and is independent.
**Subject.** [`docs/imports/compression.tex`](imports/compression.tex) §§1–3 — the cube
foliation and its exact energy identity `(*)` at `:149`.
**Depends on.** `mg-409a` ([`OneThird-Compression-W4-Rate-mg-409a.md`](OneThird-Compression-W4-Rate-mg-409a.md)) — read in full.
`mg-8bc7` (W2, `fa29801`), `mg-bb60` (W1, `7058fbd`), `mg-623a` (W3, `9b692d7`) — read, cited, not re-measured.
**Instrument.** [`code/compression_consumers_145f/`](../code/compression_consumers_145f/), `run_all.sh`, **7.2 s measured**, no float anywhere.

---

## 0. VERDICT

> ### **`no-consumer-exists`.**
>
> Every candidate in the programme is one of the ticket's four known negatives in disguise,
> or fails **test 1** — and test 1 fails for a *structural* reason that is provable rather
> than a matter of search coverage.
>
> ### **THE STRUCTURAL REASON, which is this document's own contribution.**
>
> The identity's **entire measure-dependent output** is the pair-adjacency probability vector
>
> ```
>     A^o_xy = Pr[ {x,y} is a 2-block of C_o ],   A^e_xy = Pr[ {x,y} is a 2-block of C_e ]
>
>     E Var(f | C_o) = (1/4) Σ_{x∥y} c_xy² A^o_xy        (compression.tex :94)
>     E_BK(f)        = (1/(2(n−1))) Σ_{x∥y} c_xy² (A^o_xy + A^e_xy)
> ```
>
> **0 failures / 1 475 (poset, coefficient-vector) instances, exact rationals** (`e1.1`).
> Two blindnesses follow and are measured, not asserted:
>
> - **SIGN-BLIND** — the output depends on `c` only through `c²`. A one-coefficient sign flip
>   leaves it exactly fixed while `Var(f)` moves at **201 of 250** posets (`e1.2`).
> - **LEVEL-BLIND** — invariant under `f ↦ f + a`. **No first moment is ever emitted**
>   (`e1.3`).
>
> Said the other way, and this is the whole finding in one line:
>
> > **`E_BK(f)` is the NUMERATOR of the Rayleigh quotient and the identity computes it
> > exactly. `Var(f) = E Var(f|C_o) + Var(Π_o f)` is the DENOMINATOR and the identity supplies
> > only the first summand. The ratio between what it computes and what it does not IS
> > `alpha` — which is why `alpha` is its only output, and mg-409a priced `alpha` dead
> > (ceiling `1`, bar `≥ 2`).**
>
> ### **AND THE QUANTITATIVE FORM, which is sharper than the qualitative one.**
>
> **`E Var(pos_x | C_o) ≤ 1/4` at EVERY poset and every element** — because
> `Σ_y A^o_xy = Pr[x lies in a free odd 2-block] ≤ 1`. Proved, and the bound is **attained**
> (`e2.3`, 2 666 checks, max `= 1/4` exactly). Meanwhile `Var(pos_x) = (n²−1)/12` on the
> antichain. So the share of the `(B)` quantity the identity computes is `Θ(n^{-2})` and falls
> `0.250 → 0.054` over `n = 3…7` (`e2.4`). **The identity's view of the programme's central
> statistic is a bounded local quantity; the statistic is global.**
>
> ### The one candidate of the right shape, named because it exists:
>
> **per-slot adjacency symmetry** `J_k(x,y) = J_k(y,x)` — mg-92e6's *"the extra juice is one
> joint fact"* (`STATE.md:158`). It passes **test 1** and **test 2**. It fails **test 3**, and
> it fails it three times over:
>
> 1. **It is already ours and does not need the identity.** One involution — `τ_k` is a
>    bijection between the two events, verified as a bijection at **843 (poset, pair, slot)**
>    triples with no block system, fiber or cube anywhere in the check (`e4.2`).
> 2. **The identity emits something strictly WEAKER than what the consumer took.** `A^o, A^e`
>    are the per-slot data **aggregated into two parity buckets** (`e4.3`, 0 mismatches), and
>    the aggregation collapses `≥ 2` nonzero summands at 70 of 921 incomparable pairs.
> 3. **The consumer is REFUTED.** `STATE.md:169` (mg-200d → mg-131e → mg-00a1): the
>    disjunctive per-slot value is **`Θ(n²)`, superlinear**; per-slot adjacency symmetry
>    *"BUYS A CONSTANT FACTOR OF AT MOST 6, NOT AN ORDER"*; *"THE ROUTE IS DEAD, NOT
>    RE-BASED"*. Read from the ledger, not re-measured.
>
> ### And the ticket's positivity lead, answered:
>
> **Nothing in the programme consumes bare positivity, and the one target whose deliverable
> IS a crude constant fails test 1.** `alpha > 0` is free (mg-409a `r1.1`) — but positivity of
> the BK gap is *already* unconditional in this corpus (connectivity, Karzanov–Khachiyan;
> Bubley–Dyer `n³ log n`), so there is nothing for it to buy. **(R)** — *is there `D < 1` with
> `d(P) ≤ D` on every frozen poset?* — is the right *shape* (a constant, and `STATE.md:17`
> says a constant is what the architecture consumes). It fails test 1: the identity's **only**
> density-facing relation is `Σ_{all pairs} A_xy = n − 1` **exactly**, and on the antichain,
> where **`d = 1`**, it holds with **equality and zero slack at `n = 3…7`** (`e3.3`). A
> relation a density-`1` poset satisfies with equality cannot certify `d ≤ D < 1`.

---

## 1. The machinery, stated precisely enough to filter against

`compression.tex` §§1–3. `C_o(L) = (I_2, I_4, …)` has fibers that are **exact hypercubes**
`Q^{d(F)}` whose edges are `τ_1, τ_3, …`; `C_e(L) = (I_1, I_3, …)` likewise with `τ_2, τ_4, …`.
For a pair-orientation linear statistic `f(L) = a + Σ_{x∥y} c_xy 1{x <_L y}`, inside one fiber
every inter-block orientation is frozen and the free blocks are **independent** Bernoullis, so

```
    Var(f | C_o) = (1/4) Σ_{j ∈ D(C_o)} c_{B_j}²        — "no covariance terms
                                                          whatsoever inside a
                                                          compressed fiber" (:98)
    E_BK(f) = (2/(n−1)) ( E Var(f|C_o) + E Var(f|C_e) )  — (*) at :149
```

**That is real machinery and this document does not dispute a line of it.** `e1.1` reproduces
`(*)` and both conditional-variance identities at 1 475 instances with 0 failures, on an
implementation that shares no code with mg-409a's or mg-8bc7's.

**What it emits.** Taking expectations of the fiber formula turns the sum over blocks into a
sum over pairs weighted by the probability that the pair *is* a block:

```
    E Var(f | C_o) = (1/4) Σ_{x∥y} c_xy² · A^o_xy
```

and `A^o_xy + A^e_xy = Pr[x, y adjacent]`, since every adjacent slot `(i, i+1)` belongs to
exactly one system by the parity of `i`. **This is the output map, and it is the whole of it.**

**W2's full-space repair is a DIFFERENT object and is priced separately.** `mg-8bc7`'s
`⟨f,(I − P_BK)f⟩ ≥ (2/(n−1))⟨f,(2I − Π_o − Π_e)f⟩` holds for every `f ∈ L²`, not only
degree-one ones, and its output is `alpha_full(P)`. That object is **mg-409a's**, and mg-409a
closed it: `alpha ≤ 1` at every poset (five lines, 4 468 exhibited rational witnesses,
attained at `Z_n`) against a bar of `alpha_n > (n−1)/(γn) ∈ [2, 3)`. **This ticket is about
the identity**, per its own framing (*"conditional variances of statistics that are degree one
on cube fibers"*), and §5 below records the one thing that is left to say about the operator.

---

## 2. The filter — the ticket's three tests, made operational

| test | as the ticket states it | as it is applied here |
|---|---|---|
| **1** | reachable by the machinery | does the target's dependence on the LE measure **factor through `(A^o, A^e)`**? |
| **2** | not pre-capped | does it reduce to `λ₂^BK`, and so inherit Theorem E's cap (mg-409a)? |
| **3** | actually connected to (1/3)–(2/3) | is there a live consumer, or only an unproven bridge? |

Test 1 is the one that does the work, and §0's two blindnesses are why. It **excludes at
minimum**:

- every **first moment** of a pair-orientation statistic — `E[inv_e]`, `E[pos_x]`, `p_xy`, the
  position matrix `T[x,i]`, `δ(P)`, `Δ₁`;
- every quantity sensitive to the **signs** of pair coefficients — covariances between pair
  indicators, i.e. `(B-cov)`;
- every **degree-two** statistic — `E[Σ disp²]`, i.e. `(B)`.

It **admits**: the BK Dirichlet form of a degree-one statistic, and functionals of the
adjacency probabilities.

---

## 3. THE ENUMERATION

**Sources walked, named as the ticket requires.** [`STATE.md`](../STATE.md) — the full ledger
(rows 1–11, `:109–120`), the machinery bullets L1b's reduction stands on (`:76–81`), *The
single lemma to prove* (`:126–137`), *Where the threads converge* (`:178–197`), the glossary
(`:40–51`), the equivalence dictionary (`:28–34`), and **all 26 rows** of the attempt index
(`:145–172`). Plus [`docs/state-history/attempt-mg-210d.md`](state-history/attempt-mg-210d.md)
for (R)'s definition, [`docs/state-history/threads-chronology.md`](state-history/threads-chronology.md),
mg-409a's own §2 and §7, `compression.tex` §5's own ask, and
`one_third_width_three/step8.tex` (§5 below).

### 3.1 The ledger

| row | target | T1 | T2 | T3 | disposition |
|---|---|---|---|---|---|
| 1, 2, 3a, 4, 5, 7 | `λ_std = 1 ⟺` ordinal sum; ordinal sum ⟺ disconnected; `S_P = ρ_std(η_P)`; (A) SPREAD; easy/Buser; GID + DG | — | — | — | **`U`/`U-id`, proven — not targets.** Row 4 is additionally **struck off the critical path** (mg-a58f, `STATE.md:81`) |
| 3b | standard dominance | — | — | ✗ | **KNOWN NEGATIVE.** Unconditional **refuted**; conditional **is L1b** |
| 6 | Theorem E | **✓ numerator only** | — | ✗ | The identity's *upper*-bound direction uses Theorem E's own test vector, the pair indicator — and **`e3.5` re-derives `step8.tex` Step 1 from the output map**: `E_BK(inv_e) = Σ_{x∥y} E_BK(f_xy) = (1/(2(n−1)))Σ A_xy`, **max exactly `1/2`, 0 failures / 295 posets**, on an implementation that has never seen it. But the *bound* is a **ratio**, and the identity supplies only `E_BK`; `Var(f_xy)` must come from elsewhere, as it does in `step8.tex`. Sharpening buys nothing regardless: the architecture consumes the **cut**, and the open link downstream is L1b whatever the gap bound's size |
| 8 | **L1b — the wall**, `1 − λ_std ≤ ε_spec` | ✗ | — | — | **KNOWN NEGATIVE.** `λ_std` is an `n × n` transport object (`STATE.md:78`), a functional of `T[x,i]` — **first moments**, which §0 shows are never emitted |
| 9 | L2 (first disjunct `FP✗`; L2 `OPEN`) | ✗ | — | — | A **standard eigenvector** of the transport operator. Not a BK object; first-moment-determined |
| 10 | L3 best-cut-is-a-prefix | ✗ | — | — | A cut indicator `1_A` is **not** a pair-orientation linear statistic; the identity computes no conductance |
| 11 | L4 thin interface ⟹ balanced pair | ✗ | — | — | `Δ₁(A) = E|A ∖ σ(A)|/min(|A|,|Aᶜ|)` is a **first moment** |

### 3.2 The single lemma, and the three residuals

| target | source | T1 | why |
|---|---|---|---|
| **(B)** `E[Σ disp²] = O(E[Σ|disp|])` | `STATE.md:130` | ✗ | **degree two.** Quantified in `e2`: the identity's share of `Var(pos_x)` is capped at `1/4` **uniformly**, against `(n²−1)/12` on the antichain |
| **(LIB)** `E[inv_e] = O(n/γ)`, and (LIB-const)/(LIB-weak) | `STATE.md:131`, row 8 | ✗ | **first moments — and this is the cleanest single case.** `inv_e` **is** a pair-orientation linear statistic (all `c = 1`), so the identity *does* compute something about it: `E_BK(inv_e) = (1/(2(n−1)))Σ A_xy`, which is **`≤ 1/2` at every poset and attains `1/2`** (`e3.5`). The **same `1/2` whatever `E[inv_e]` is.** A Dirichlet form is not a mean, and here the quantity the identity can compute carries **zero** information about the quantity row 8 needs |
| **(B-cov)** the wrong-signed same-side covariance | `STATE.md:181`, the residual listed **first** | ✗ | **§4 below — the sharpest near-miss on the board** |
| **(R)** density ceiling `d(P) ≤ D < 1` | `STATE.md:183`, mg-210d | ✗ | **§0 and `e3`.** Right shape (a crude constant), wrong reachability: the only relation is an **equality at `d = 1`** |
| **(EQ)** `max_x |E[pos_σ x] − rank_e x| = O(1)` | `STATE.md:186` | ✗ | a **first moment**, and `STATE.md` itself calls it *"a cancellation statement"* — cancellation is exactly what a `c²` functional cannot see |
| **(RD)** which reading branch (ii) carries | `STATE.md:192` | ✗ | a question about the **wording** of `:469–470`, not a quantity |
| the **Step 6 hole** (mg-3af9) | `STATE.md:193` | ✗ | architecture-level; reaches the identity only through L4/`Δ₁` |

### 3.3 The attempt index — all 26 rows

Grouped by why each is excluded; every row is accounted for.

| group | rows | T1 | why |
|---|---|---|---|
| **transport / marginal objects** — position matrix `T[x,i]`, slot laws, `p_xy`, `μ_pref`, `Δ_P`, `C₃` | mg-210d; mg-92e6 (probe B's diagonal-capacity half); mg-f82f (probe C, incl. window conjecture **W3**); mg-88bd; mg-76b2; mg-51f4 → mg-c50b → mg-789d ((F)/(M♯)/(L\*)); mg-345e; mg-6bc2; mg-ba78 | ✗ | first moments. `e5` supplies a **hard** negative for this group: `max_{x∥y} p_xy` **SPLITS** inside an `(A^o, A^e)` bucket at both `n = 4` and `n = 5` — two posets the identity cannot tell apart carry different pair-bias marginals, so no argument whatever can extract them from its output |
| **entropy / order-polytope / AF** — `log e(P)`, Stanley absolute-position `N_i`, Ma–Shenfeld equality cases | *untried · open* (`:150`); *untried · convergent target* (`:151`); `dead ≠ AF` (`:152`); mg-a1ec; mg-48ab; mg-dcae | ✗ | joint-law counts and log-concavity of counting sequences. The identity emits no entropy and no `N_i` |
| **face geometry / Hodge** | mg-276d; mg-a3d4 | ✗ | order-polytope faces, a different object; and mg-a3d4's Theorem G prices that side at a `2^{Θ(n)}` loss |
| **graph-combinatorial** — incomparability graph `G(P)` | *untried · new object* (`:153`); mg-e2de (probe D) | ✗ | no LE measure in the object at all. mg-e2de is additionally a **sound negative** already |
| **already retired** | `dead end` Bruhat-convexity (`:148`); `avoid this aim` Kahn–Saks (`:149`); DROP width ≥ 4 (`:145`); the C.md correction (`:147`); mg-0ed7's `Φ→Var` (**refuted**, mg-8f56); the tempering/deformation route (**dead**, mg-4a86) | — | not live targets |
| **coherence** | mg-61bb (probe A) | ✗ | **proven INERT** already: coherence is a *consequence* of `δ < 1/3` and shrinks the class by zero |
| **adjacency** | mg-92e6's *one joint fact*; mg-200d → mg-131e → mg-00a1 | **✓** | **the one candidate of the right shape — §0 and `e4`. Passes T1 and T2; fails T3.** |

### 3.4 The four known negatives — confirmed as such, not re-derived

`λ₂^BK` (capped, mg-409a), `λ_std` (incomparable, mg-d1be / `STATE.md:78`), the L1b route
(row 8, the wall), standard dominance unconditional (refuted, 166 refuters at `n = 7`). **None
is re-measured here.** Every candidate above that is one of them in disguise is marked as such
and the ticket's instruction not to rediscover them is kept.

---

## 4. The sharpest near-miss, and it is worth its own section

`STATE.md:180–182` orders three residuals and puts **(B-cov)** first: *"break the wrong-signed
same-side covariance"* (FKG/XYZ force it `≥ 0`), *"the sharp edge"*, and *"the object three
separate routes converge on"*. `compression.tex:98` advertises **"no covariance terms
whatsoever inside a compressed fiber."** The shapes appear to match exactly. They do not, and
the reason is a clean split.

**(a) The covariance the identity kills is ZERO FOR A TRIVIAL REASON.** Inside an odd fiber
every pair indicator is either a free Bernoulli on its own 2-block or **constant**, and
distinct free blocks are disjoint. So `Cov(s_xy, s_uv | C_o) = 0` identically —
**0 nonzero / 1 326** (fiber, pair, pair) triples (`e2.1`). The claim at `:98` is *true* and it
is a statement about a quantity that was never nonzero.

**(b) (B-cov)'s covariance is a BETWEEN-fiber quantity.** By the law of total variance
`Var(pos_x) = E Var(pos_x|C_o) + Var(E[pos_x|C_o])`, and the identity computes only the first
summand. The same-side covariance `C_x = Σ_{y≠z} Cov(s_xy, s_xz)` sits entirely in the second.
Measured: `C_x > 0` at **555 of 555** (poset, element) rows and `< 0` at **none** — the
FKG/XYZ wrong sign, reproduced (`e2.2`).

**(c) And the split is quantitative, not just structural.**
`E Var(pos_x|C_o) = (1/4) Σ_{y∥x} A^o_xy ≤ 1/4`, **at every poset, every element, uniformly in
`n`**, because `Σ_y A^o_xy ≤ 1`. Attained. Against it:

| `n` | `Var(pos_x)` on `A_n` | `E Var(pos_x\|C_o)` | share |
|---|---|---|---|
| 3 | `2/3` | `1/6` | `0.250000` |
| 4 | `5/4` | `1/4` | `0.200000` |
| 5 | `2` | `1/5` | `0.100000` |
| 6 | `35/12` | `1/4` | `0.085714` |
| 7 | `4` | `3/14` | `0.053571` |

This is **mg-409a §4's `alpha(A_n) ≤ 6/(n(n+1))` seen from the `(B)` side rather than the
spectral side**, and it is the same mechanism: a degree-one statistic's within-fiber variance
is a bounded *local* quantity while the `(B)` quantity it would have to control is *global*.
Two independent arcs landing on `Θ(n^{-2})` at the antichain by different routes is the
strongest consistency check available here, and it was not arranged.

---

## 5. Is there any consumer of a BK-gap LOWER bound at all?

mg-409a §7 files this as the named condition its verdict could fail on (*"Some consumer of a
BK-gap lower bound exists that I did not find"*). **Walked independently here, and the answer
is no.**

- **`step8.tex`, the file that proves Theorem E, never consumes one.** `lambda_2` occurs
  **0 times**; `spectral` twice; and all **25** occurrences of `gap` are *"open gap"* (proof
  gaps: G3, G4, Case C, the layered reduction) or *"one of `ℓ+1` gaps"* — **not one is a
  spectral gap being bounded below**.
- **Theorem E runs the other way.** It produces an *upper* bound `E_BK(f_xy)/Var(f_xy) ≤
  2/(γn)` and hands the architecture a **cut**, not a number. Steps 3–6 consume the cut.
- **So the only use of a lower bound is contradiction with Theorem E** — which is precisely
  mg-409a's §2, and it is closed: `alpha ≤ 1` unconditionally against a bar of `≥ 2`.

**This is confirmation of mg-409a's condition 2, on a second reading of a third file, and not
a new result.**

---

## 5.5 THE KIND OF THIS VERDICT — `STATE.md:99`'s standing rule, applied to my own document

The rule is *"any prose that **aggregates** rows must state the **WEAKEST** kind in the set it
names"*, and §0 aggregates. So, at the claim:

| statement | kind | warrant |
|---|---|---|
| the output map `E Var(f\|C_o) = (1/4)Σ c² A^o` | **`U-id`** | an identity — two lines from `compression.tex:94` by taking expectations; verified at 1 475 instances |
| `E Var(pos_x\|C_o) ≤ 1/4`, every poset, every `x` | **`U`** | proved from `Σ_y A^o_xy ≤ 1`; **attained** |
| `Σ_{all pairs} A_xy = n − 1` | **`U-id`** | slot counting; second route in `e3.4` |
| the antichain saturates it at `d = 1` | **`U`** | exhibited at `n = 3…7`, zero slack |
| `E_BK(inv_e) ≤ 1/2`, attained | **`U`** | follows from the two above |
| `J_k(x,y) = J_k(y,x)` and its involution proof | **`U`** | `τ_k` is a bijection; `FP` only in the *checking*, `U` in the argument |
| within-fiber `Cov = 0`; `C_x > 0`; the `e5` splits | **`FP`** | `n ≤ 6`, `n = 5`/`6` **sampled** |
| the `e5` **nulls** | **weaker than `FP`** | 4 and 10 comparisons — see D3; **not evidence** |
| *"no consumer exists in the programme"* | **not a mathematical kind at all** | it is a claim over a **corpus**, and §6 condition 2 is where it can fail |

**The weakest kind in the set §0 aggregates is therefore the last row, and it is the one to
attack.** The mathematics under it is `U`/`U-id`; the *enumeration* is a search, and a search
over a corpus is exactly the shape that `0/132` was (`STATE.md` row 3b) — zero findings inside
a frame. **My frame is named in §3's source list and in §6 condition 2, and it should be
carried with the verdict.**

---

## 6. What would have to be true for this verdict to be wrong

Filed as named conditions so a reversal cannot be assembled after the fact.

1. **The output map is wrong.** It is verified at 1 475 instances on exact rationals and
   follows in two lines from `compression.tex:94` by taking expectations. If it is wrong the
   instrument's `e1.1` fails, which is one command.
2. **A target exists that is a functional of `(A^o, A^e)` and that I did not enumerate.** This
   is the real exposure and I state it as such: §3 walks the ledger, the residuals and all 26
   attempt-index rows, but *"every target in the programme"* is a claim over a corpus, and a
   target living only in a `docs/` document with no ledger row would be outside my sweep. What
   narrows it is that the admitted class is small and concrete — Dirichlet forms of degree-one
   statistics, and adjacency functionals — and §3.3's last row is the only member of it I
   found.
3. **mg-00a1 is wrong and the per-slot adjacency route is live.** Then §0's candidate passes
   all three tests and the verdict flips to `candidate-found`. I **read** that row and did not
   re-derive it; `STATE.md:169` states it as a construction (an explicit closed-form measure,
   no simplex in the verification path), not a failed search.
4. **The `1/4` cap is wrong.** Proved from `Σ_y A^o_xy ≤ 1` and checked at 2 666 (poset,
   element, parity) triples with max exactly `1/4`. If wrong, some witness is wrong, which is
   checkable directly.
5. **The full-space operator, not the identity, is the intended machinery.** Then the
   governing document is mg-409a and not this one — and its answer is the same (`alpha ≤ 1`
   against a bar `≥ 2`). I record this as a hypothetical because the ticket scopes itself to
   the degree-one identity, and because *both* answers are already on the board.

---

## 7. Defects of my own, all kept

Six, in full, in [`code/compression_consumers_145f/README.md`](../code/compression_consumers_145f/README.md).
The two that a reader of this document needs:

**D1 — I keyed an isomorphism-invariant question on an ordered-pair key and got a "finding".**
`e4.3`'s first version reported `P1 = [(2,3)]` against `P2 = [(3,2)]` — **one poset
relabelled** — as two posets the identity cannot tell apart. That is **mg-409a's own D2
recurring in the document that cites it**, which is the part worth recording: reading a
predecessor's defect list is not the same as applying it. Caught because the "collision" was
absurd on its face, not because anything checked. Replaced by a direct demonstration, and the
defective key is now armed as `e5.0`'s positive control (359 relabellings move it).

**D3 — `e5`'s null rows have almost no power and are not evidence.** The collision test
compares **4 distinct-class pairs at `n = 4` and 10 at `n = 5`**. `max p_xy` **SPLITS**, which
is a hard negative and is used in §3.3. The other four targets come back *"constant"* — a null
over ten comparisons, and **not** evidence that the identity determines `δ`, `E[inv_e]`, the
`(B)` variance diagonal or `(EQ)`. **My own prior lost here**: I expected `E[inv_e]` to split.
The verdict rests on `e1` (a theorem), `e2.3` (a theorem), `e3.3` (an equality at `d = 1`) and
`e4.4` (the ledger) — not on those rows, and the power figure is printed beside them.

---

## 8. What this document does not do

- **`docs/imports/compression.tex` is NOT edited.** Its README reserves that directory for
  verbatim copies; W1, W2 and mg-409a left it alone and so does this.
- **`STATE.md` is NOT touched** and `mg-e331`'s ratchet is not exercised. Nothing here is a
  ledger movement: the finding is about a document that is not on the ledger, and it changes
  no row's kind or status.
- **No known negative is re-measured.** `λ₂^BK`'s cap, `λ_std`'s incomparability, L1b and the
  166 refuters are all read.
- **mg-00a1's refutation is read, not re-derived.** §6 condition 3 states the exposure.
- **The frozen class is empty at every `n` enumerable here** (`1/3–2/3` verified to `n = 14`,
  mg-33f5; `n ≥ 12` refereed / `n ≥ 15` preprint, `STATE.md:213`). mg-345e's and mg-6bc2's
  refusal of the sweep is kept, and every frozen-conditional statement in §3 is a statement
  about a *relation*, not a measurement over the class.
- **No claim is made that the compression is worthless as mathematics.** `(*)` is exact and
  reproduces here at 1 475 instances; W2's full-space inequality is a real unconditional
  theorem. The claim is narrower and is the one in §0: **this programme has nothing for it to
  feed.**
- **`mg-8d66` (the `k` half) is untouched.** A different `k` changes the fiber dimension and
  therefore the adjacency structure; nothing here forecloses it, and nothing here should be
  quoted against it.
