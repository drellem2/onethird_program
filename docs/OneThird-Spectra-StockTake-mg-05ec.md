# OneThird — TAKE STOCK: what the spectra are, how they relate, and whether the spectral route is *the* bridge

**Filed by** `mg-05ec` on Daniel's direct request, 2026-08-12. **Kind of this document:** a
stock-take. It assembles and clarifies what is already in the corpus and **produces no new
mathematics**. Two textual measurements are re-run here rather than quoted (§4.2, §6); everything
else is cited, with its kind and its frame, per [`STATE.md:99`](../STATE.md).

**Provenance of the sources.** `STATE.md` at `c5cd288` (this repository). The
`one_third_width_three` corpus at two revisions, and the difference matters once: its
**`origin/main` is `949c439`** and its **checked-out `main-mirror` is `912f1b1`**. `mg-d1be`'s
repair (§3) is on `origin/main` at `bde9610` and is **not** in the mirror — a reader who opens
`docs/OneThird-L1b-Reverse-Cheeger-Proof-Attempt.md` in the mirror sees the *struck* claim
standing unstruck. Read that file at `origin/main`.

---

## 0. VERDICT — the one paragraph, and it stands alone

> **No. The spectral route is not *the* bridge, and the ledger has not supported calling it that
> for some time.** There is exactly one bridge — **L1b**, the implication from *frozen*
> (`δ(P) < 1/3`) to *near-ordinal-sum* — and that bridge is real, is `OPEN`, and is the whole
> remaining gap. What is not true is that it is **spectral in any load-bearing sense**. Three
> things say so, each already on the ledger. **(1) The far side of the bridge is a naming, not a
> mechanism.** `1 − λ_std ≤ ε_spec` is one of about five interchangeable renderings of a single
> axis (`STATE.md:15`, `:25`), and mg-210d's master bound `1 − λ_std ≤ 6·E[inv_e]/(n²−1)` converts
> the combinatorial rendering into the spectral one — so a proof would be *done* in inversions and
> merely *reported* in eigenvalues. **Not one** of the three residuals the ledger lists as live is
> an attack on a spectrum: two are counting statistics of `L(P)` and the third is a count on `P`
> itself (§4.4). **(2) The one genuinely
> BK-spectral ingredient runs the other way.** Theorem E is an *upper* bound on the BK gap; it
> hands the architecture a **cut**, not a number, and **nothing in the programme consumes a BK-gap
> lower bound at all** (mg-145f §5; re-measured here at §6: `lambda_2` occurs **0** times in
> `step8.tex`, and all **25** lowercase occurrences of `gap` are proof gaps or *"one of `ℓ+1`
> gaps"*). A BK-gap lower bound is in any case **already proven, unconditionally and sharply**, by
> Wilson (2004), so there is nothing there to buy. **(3) The transfer that would make the route
> spectral is refuted unconditionally, and conditionally it *is* the wall.** `λ_std` and `λ₂^BK`
> are **incomparable in both directions** on exact rationals (mg-d1be), never equal (0/4306 at
> `n = 4,5`), and `L(P)` carries no `S_n` action, hence no invariant standard sector for a
> Cheeger-style transfer to live in. **What it should be called instead:** *two axes, one bridge —
> and the bridge is a **rigidity** statement whose live currency is inversions.* The spectral
> objects keep two honest jobs: a **dictionary** (row 3a, `S_P = ρ_std(η_P)`, which is what
> licenses the word *"standard"*) and **one proven ingredient** (row 5, Buser, consumed inside the
> master bound). A vocabulary and a lemma are not a route.

---

## 1. THE DISTINCTION, in plain language, before any notation

There are **three** spectra in play, not two, and the third is the one that makes the other two
easy to tell apart. Each is a different question you can ask about the same poset `P`.

**Picture A — the destination (the transport picture).** Draw a uniformly random linear extension
of `P`. Ask, for each element `x` and each position `i`: *how often does `x` land in slot `i`?*
That fills an `n × n` table of probabilities. This table is a **static summary of the measure** —
it contains no notion of time or motion. Symmetrise it and look at its largest eigenvalue in the
directions orthogonal to the constant one. **That number is `λ_std`.** It measures how *rigid* the
element-to-position assignment is: `λ_std = 1` exactly when `P` is an **ordinal sum** — a stack of
blocks that never interleave — and `λ_std` drops away from 1 as the poset lets its elements slosh
around. Near-ordinal-sumness *is* `λ_std → 1`.

**Picture B — the journey (the BK picture).** Now take the *set of all linear extensions* of `P`
and make it the vertex set of a graph: join two extensions when they differ by swapping a single
adjacent pair of incomparable elements. Run the natural random walk on that graph. **`λ₂^BK` is
its second eigenvalue** — how *slowly* the walk mixes. This is a **property of a dynamics**, not of
the measure alone; the measure is only its stationary distribution.

> **The distinction in one sentence: `λ_std` is a property of the *measure*; `λ₂^BK` is a property
> of a *walk* whose stationary distribution is that measure. One lives on `n` elements. The other
> lives on `|L(P)|` linear extensions, which is typically exponentially larger.**

**Picture C — the `S_n` picture, which is where `λ_std` actually lives.** Consider a random walk on
*all* of `S_n` (not on `L(P)`) whose step is: pick a uniformly random linear extension of `P`,
viewed as a permutation, and multiply — symmetrised. `S_n` acts on itself, so this walk decomposes
by representation theory. **The block belonging to the standard `(n−1)`-dimensional irrep is
exactly the symmetrised transport matrix of Picture A.** That is ledger row 3a,
`S_P = ρ_std(η_P)`, kind `U-id`, **proven**. So by Schur's lemma `λ_std` is **guaranteed** to be an
eigenvalue of this `S_n` walk.

**And that guarantee is exactly what is missing on the BK side.** `L(P)` carries **no `S_n` action
at all** — a BK move at position `i` only fires when the two elements sitting there are
incomparable, so which positions are available depends on *which* extension you are standing on.
There is therefore no irrep decomposition of `ℝ^{L(P)}`, no "standard sector" inside it, and **no
guarantee `λ_std` appears anywhere in the BK spectrum**. (`ComparisonRoute` §3.2 measures this
directly: the operator norm of the leak of the one-particle span under the BK operator is machine
zero on antichains — where the constraint is empty and `L(P) = S_n` — and `Θ(0.1)` on constrained
posets. `[proven]` + measured, `n ≤ 5`.)

**That is the whole distinction, and it is why the two can be neither identified nor compared.**
`λ_std` is the `S_n`-side object; `λ₂^BK` is not. `STATE.md:78` puts the same point in one clause,
and it is the sentence to remember:

> `λ_std` is *"an `n × n` transport object over the **elements of `P`**, **not** a block of the BK
> spectrum over `L(P)`."*

### 1.1 Why it gets re-conflated — the specific mechanism, so it can be watched for

Three different statements have all been called *"standard dominance"* (`ComparisonRoute` §1), and
one number was measured on one of them and cited for another:

| name | statement | lives on | status |
|---|---|---|---|
| **SD-Cayley** | `λ₂(Cayley walk on S_n) = λ_std` | `S_n` | Coherent and **near-automatic in shape**: by Schur, `λ_std` is *guaranteed* to be in the spectrum, so the claim is only that no *other* irrep out-eigenvalues it. **This is what `0/132` measured.** |
| **SD-BK** | `λ₂^BK = λ_std` | `L(P)` | **FALSE** — `0/4306`, exhaustive at `n = 4,5`. Failure is **two-sided**. |
| **SD-quant** | the slowest BK mode has an `Ω(1)` component in the one-particle span | `L(P)` | Coherent, well-posed *without* invariance, and **the programme's actual need**. Measured once (§3.4). |

> ⚠️ **`0/132` IS `S_n`-SIDE EVIDENCE AND DOES NOT TRANSFER TO THE BK SIDE.** This is recorded at
> `STATE.md` row 3b — *"mg-4a86's audit found the `0/132` is **Cayley-walk** evidence, not BK-chain
> evidence, and was mis-attributed"* — and independently at `ComparisonRoute` §1.1. **And it must
> never be quoted bare on either side:** its frame is `n ≤ 6` exhaustive **+ `n = 7` top-λ spot
> only**, a frame chosen so that the known moderate-λ `n = 7` refuters are outside it. It is zero
> failures in a population that excludes the known failures. `STATE.md:5` and row 3b(c) both say
> so; this document repeats the frame every time the number appears, which is the standing rule.

### 1.2 What a bound on each would buy

| object | a **lower** bound on the gap (`1 − λ`) buys | an **upper** bound on the gap buys |
|---|---|---|
| `λ_std` (transport / `S_n`-standard) | nothing the programme wants — it says the poset is *far* from an ordinal sum | **everything: this is the wall.** `1 − λ_std ≤ ε_spec` under `δ < 1/3` is L1b, row 8, and the conjecture reduces to it |
| `λ₂^BK` (BK chain on `L(P)`) | **nothing — no consumer exists** (§4.3), and it is already proven anyway (Wilson 2004) | Theorem E produces one, row 6, `U`, **proven** — and what the architecture actually consumes from it is the **cut**, not the number (§4.2) |

---

## 2. WHAT EACH ONE IS, precisely

Notation from here. Nothing in §1 depends on this section.

**`λ_std` — transport / standard.** `(T_P)_{x,a} := Pr_{σ ~ Unif L(P)}[σ(a) = x]`, doubly
stochastic and `n × n`; `S_P := (T_P + T_Pᵀ)/2`; `λ_std(P) :=` top eigenvalue of `S_P` on
`H = 𝟙^⊥ ⊂ ℝⁿ`. Depends **only** on the measure `Unif L(P)` — there is no dynamics in it.
`1 − λ_std = min_{f ⊥ 𝟙} ⟨f,(I − S_P)f⟩/‖f‖²`. **`λ_std = 1 ⟺ P` is an ordinal sum** (row 1, `U`,
proven). ⚠️ **`λ_std` is defined relative to a chosen reference linear extension** and *"moves by
up to `1/3` across reference orders (4,069 of 4,824 posets at `n = 6`)"* against a target of
`ε_spec ≈ 0.02` (`STATE.md:44`, mg-c4f5). The frozen hypothesis is what removes the choice — `e` is
canonical — so this is **a hypothesis doing work, not a convention**.

**`λ₂^BK` — the BK chain.** The **Bubley–Karzanov graph** on `L(P)`: two extensions adjacent iff
they differ by transposing an adjacent incomparable pair (`step1.tex:20–26`). Lazy walk, step
`1/(2(n−1))` per position. `λ₂^BK` is its second eigenvalue; `gap_BK := 1 − λ₂^BK`. *(Naming note,
so a literature search does not come up empty: the corpus uses **both** *"Bubley–Karzanov"* — the
graph and the 1998 mixing result — and **"Karzanov–Khachiyan chain"**, which is what Wilson (2004)
Table 1 calls the same object. `mg-409a:170` and `mg-145f:78` use the latter. **Same chain, two
names.**)*

**The Cayley walk on `S_n`.** Generating measure `η_P = (μ_P + μ_P^∨)/2` with `μ_P` uniform on
`L(P)` viewed inside `S_n`. **`ρ_std(η_P) = S_P` exactly** — ledger row 3a, `U-id`, proven.

---

## 3. THEIR RELATIONSHIP — and the answer includes a hard negative

### 3.1 The hard negative: incomparable in **both** directions

**Kind: `FP✗` — a finite population exhibiting counterexamples, which per `STATE.md:94` refutes a
universal at every `n` and is therefore as strong as anything on the ledger.** All certificates are
**exact rational arithmetic**; no floating point is on any verdict path (mg-d1be, landed
`bde9610`, on `one_third_width_three` `origin/main`, §5.0′ of the Reverse-Cheeger document).

**Direction 1 — `λ_std ≤ λ₂^BK` is FALSE.** Witnesses, exact:

| witness | `n` | width | `\|L(P)\|` | `λ_std` | `λ₂^BK` | excess |
|---|---|---|---|---|---|---|
| `A₂ ⊕ A₂` | 4 | 2 | 4 | **1** | **2/3** | **1/3** |
| `A₃ ⊕ A₃` | 6 | 3 | 36 | **1** | **9/10** | **1/10** |

`λ_std = 1` by an exact eigenvector of `S_P` orthogonal to `𝟙` (and `λ_std ≤ 1` always); `λ₂^BK ≥ c`
by an exact rational eigenvector from the nullspace of `W − cI`, and `λ₂^BK ≤ c` by exact symmetric
elimination showing `cI + (1−c)J/N − W ⪰ 0`.

**Direction 2 — `λ_std ≥ λ₂^BK` is FALSE.** On the antichain `A_n`: `λ_std = 0` (by symmetry
`T_P = J/n`, which acts as `0` on `𝟙^⊥`) while `λ₂^BK = 1 − (1 − cos(π/n))/(n−1) → 1`. At `n = 3`
that is `0` against `3/4`; at `n = 7`, `0` against `0.983…`.

**And they are never equal:** `0 / 4306`, exhaustive over all posets at `n = 4` (195) and `n = 5`
(4111). **The failure is two-sided in that same population** — 33 of 195 and 550 of 4111 have
`λ_std > λ₂^BK`, the rest have `<`.

> ⚠️ **DO NOT REACH FOR THE RESCUE "it fails exactly on the ordinal sums" — that is itself
> refuted.** `ComparisonRoute:75` (row C3) records the set equality as `[proven]` at `n = 4,5`, and
> mg-d1be re-ran it **exhaustively up to isomorphism at `n ≤ 6`** (1, 2, 5, 16, 63, 318 classes,
> enumerator self-checked against those counts): the equality holds through `n = 6` and **breaks at
> `n = 7`**. The witness is **indecomposable** — its incomparability graph is a path, hence
> connected — with `|L(P)| = 21`, width 2, `δ(P) = 8/21`, and
> `λ_std = 0.943925792… > 0.943488101… = λ₂^BK`, certified by the **separating rational
> `9437/10000`**: a *proved strict* separation at margin `4.4e-4`, not a numerical one.
> Indecomposability does not rescue the claim either. `ComparisonRoute` §1.2 and §2.4 predate this
> and are superseded by it.

**Why the inequality was believed, and why the reason was never a reason.** The justification on
record was *"the standard sector is a subspace"* — restricting a max to a subspace lowers it, which
is a **valid schema with a false hypothesis**: there is no containment, because the two numbers are
extrema of **different operators over different spaces**, a *static* functional of the measure on
`ℝⁿ` versus a *dynamic* functional on `ℝ^{L(P)}`. The Dirichlet forms are not comparable term by
term either: the transport form pairs `f` at a *position* with `f` at the *element occupying it*,
`½·E_σ Σ_a (f(a) − f(σ(a)))²`, while the BK form pairs two extensions differing by one adjacent
transposition.

**They do not even scale alike.** On the antichain the transport gap is `1 − λ_std = 1`, i.e.
`Θ(1)`, while the BK gap is `(1 − cos(π/n))/(n−1) ≍ π²/(2n³)`, i.e. `Θ(n⁻³)`. **No constant
reconciles `Θ(1)` with `Θ(n⁻³)`** (`ComparisonRoute` §3.1, `[proven]`). If you want one number to
carry away from this section, that is a good one: the obstruction is **maximal exactly where the
poset constraint is empty**, which inverts the intuition that the constraint is what breaks the
comparison.

### 3.2 What this costs the architecture, stated exactly

The struck bullet's **conclusion survives and is strengthened**. §5 of the Reverse-Cheeger document
used `λ_std ≤ λ₂^BK` to conclude that Theorem E's bound points the wrong way for the transport
quotient. That conclusion is correct and now rests on incomparability instead: since **neither**
inequality is universal, a bound on `λ₂^BK` carries **no information about `λ_std` in either
direction** — a *strictly stronger* obstruction than a wrong-way inequality, which would at least
have been an inequality.

**And the helpful direction is available only where it is vacuous.** At every size checkable
exhaustively (`n ≤ 6`) the direction that *would* have helped, `λ_std ≥ λ₂^BK`, holds **exactly on
the ordinal sums** — i.e. exactly where `λ_std = 1` and the target is already trivially true.
**Kind: `FP`, `n ≤ 6`** — and per §3.1 it is *false* one size up.

### 3.3 What IS known to connect them, and under what conditions

1. **On the `S_n` side the connection is a theorem, not a hope.** `ρ_std(η_P) = S_P` (row 3a,
   `U-id`, **proven**) *guarantees* `λ_std` sits in the Cayley spectrum. **SD-Cayley** — that it is
   the *top* nontrivial one — is the empirical `0/132`, **frame: `n ≤ 6` exhaustive + `n = 7`
   top-λ spot only**.
2. **On the BK side there is nothing of that shape**, because there is no invariant sector (§1).
   The correct formulation of the need is an **overlap**, `SD-quant`, which is well-posed without
   invariance.
3. **Standard dominance, the unconditional statement, is REFUTED.** `mg-8b64`'s BK-transport probe
   exhibits **166 explicit refuters at moderate-λ `n = 7`**. ⚠️ **EVIDENCE BOUND, carried rather
   than laundered:** the figure `166` is **read from that probe document and has not been
   re-measured** — not by mg-65f5, not by mg-55f2, not here.
4. **And the conditional statement IS the wall.** *"`L1b ⟺ all-pairs-frozen ⇒ standard
   dominance"`* (Reverse-Cheeger `:310`). **So row 3b is not independent support for L1b: the half
   of it that is open is L1b** (`STATE.md` row 3b(b); the `FP` mark was withdrawn at mg-55f2).
   Reading it as support records the open problem as its own evidence.
5. **Why the refuters do not touch the conditional — a real limit on them, not a rescue.** Every
   one of the 166 has `δ(P) ∈ {0.473, 0.474, 0.500}`, i.e. possesses a near-balanced or balanced
   pair. **None of them is a counterexample**, and none is in the all-pairs-frozen regime. They
   kill the unconditional form and leave the conditional untouched.
6. **The mechanism behind the refuters is irrep-level and is worth knowing.** Off-regime (a *lone*
   frozen pair): a genuinely slow BK mode exists — `λ₂^BK ≈ 0.98` — but it is **degree-2**, the
   lone pair, so the transport quotient still mixes fine at `λ_std ≈ 0.77`. **The low-energy cut
   lands in the wrong irrep.** In-regime (all pairs frozen, `δ → 1/3`): the two gaps track each
   other (`0.057` vs `0.056` at `enum-n7-#945`). All-pairs-frozen appears to push the slow mode
   *into* the standard sector — which is the whole conditional, and is why it is a conjecture and
   not a corollary.

### 3.4 `SD-quant` — the one thing measured that points the right way, with its frame attached

`SD-quant(c)`: the top nontrivial BK eigenfunction `f` satisfies `‖P_U f‖² ≥ c‖f‖²`, `U` the
one-particle span. Measured once (`ComparisonRoute` §7):

| set | posets | min `c` |
|---|---|---|
| `n = 5` informative stratum (`dim U ≤ \|L(P)\|/2`) | 841 | 0.990257 |
| `n = 6` random sample, informative stratum | 2043 | **0.978898** |

⚠️ **Two frames travel with these numbers, and the second is fatal to over-reading them.**
**(i)** `c ≈ 1` is **vacuous** when `dim U ≈ |L(P)|`, since then `P_U ≈ I`; at `n = 4` the median
ratio is `1.0`, so the `n = 4` row carries **no information** and is not shown. **(ii)** The sweep
**does not reach the `n = 7` off-regime refuters**, where the slow mode is explicitly degree-2 and
the source's own prediction is `c ≈ 0`. So this is **`FP` support for the conditional inside its
regime, and is not evidence that `SD-quant` is universal** — the source says so itself and files
the decisive experiment as *"the single highest-value follow-on"*, not run.

---

## 4. IS THE SPECTRAL ROUTE TRULY *THE* BRIDGE?

### 4.1 What it would deliver if it worked, and via which theorem

The intended chain (`STATE.md:57–72`) is: **minimal counterexample ⟹ (Theorem E, row 6, `U`) a
low-conductance BK cut ⟹ (L1b, row 8, `OPEN`, ★THE WALL) `1 − λ_std ≤ ε_spec` ⟹ (rows 5 + 10) a
thin low-conductance prefix interface ⟹ (L4, row 11, `OPEN`) a balanced pair survives ⟹
contradiction with `δ < 1/3` ⟹ no counterexample ⟹ 1/3–2/3 holds.**

So the spectral route's deliverable is the **entire conjecture**, and the theorem it would run
through is **Theorem E** for the input and **L1b** for the transfer. That is the case for calling
it *the* bridge, and it is why the framing was adopted. The rest of this section is why it no
longer holds up.

### 4.2 Theorem E caps the gap — it runs the OTHER way, and it hands over a cut

**Theorem E** (`step8.tex` §G1, row 6, `U`, **proven**): a `γ`-counterexample on `n ≥ 2` elements
contains an incomparable pair with `E_BK(f_xy)/Var(f_xy) ≤ 2/(γn)`, hence a cut `S ⊆ L(P)` with
`vol(S) ≥ γ·vol(L(P))` and `Φ(S) ≤ 2/(γn)`.

Read the direction. This is an **upper bound on the BK gap** — *some* mode mixes slowly. Its output
to the architecture is a **cut**, a combinatorial object, and Steps 3–6 consume the cut. It is not
a number anybody downstream reads off.

*(Row-6 scope, carried because it is easy to lose: the source states Theorem E for **width-3**
posets. mg-957a checked and found the hypothesis **present and inert** — no step of any of the four
proofs consumes it, so the ledger's "any" is earned. But the **cascade downstream** of Theorem E in
`step8.tex` **is** genuinely width-3 and stays out.)*

### 4.3 Does anything in the programme consume a BK-gap **lower** bound? **No.**

mg-145f §5 walked this independently and answered `no-consumer-exists`. **Re-measured here** on
`step8.tex` at `912f1b1` — this is one of the two things this document does not merely quote:

| measurement | mg-145f §5 reports | measured here |
|---|---|---|
| `lambda_2` occurrences in `step8.tex` | 0 | **0** ✓ |
| lowercase `gap` occurrences | 25 | **25** ✓ |
| …and each is a *proof* gap or *"one of `ℓ+1` gaps"* | claimed | **confirmed** by inspecting all 25 contexts: `[GAP:]` notes, G3/G4, Case C, the layered reduction, one *"`ℓ+1` gaps"*, and formalisation gaps. **Not one is a spectral gap being bounded below.** |
| `spectral` occurrences | 2 | **2** ✓ |

*(There are additionally **26** occurrences of uppercase `GAP` — the `\textbf{[GAP:]}` proof-gap
labels. They are the same category and do not disturb the finding; the count is stated so a reader
who greps case-insensitively and gets 51 does not think the measurement failed.)*

**The only conceivable consumer, and it is priced dead.** A BK-gap **lower** bound cannot serve
L1b, because nothing about `λ₂^BK` transfers to `λ_std` (§3.1). What it *could* do is **contradict**
Theorem E's upper bound and empty the counterexample class. That requires the compression
quantity `alpha_n` to exceed the cap:

```
    THE BAR:     alpha_n  >  (n−1)/(γn),    γ ≤ 1/3       — a CONSTANT in [2, 3), not a rate
    THE CEILING: alpha(P) ≤ 1  at EVERY poset, and 1 is ATTAINED  (mg-409a, proved; `U`)
```

The bar **does not decay**: `2.000` at `n = 3`, `2.850` at `n = 20`, `2.997` at `n = 1000`, all at
`γ = 1/3`. And mg-8d66 closed the obvious escape: the ceiling is **not** an artefact of the `k = 2`
proof — `alpha_k ≤ 1` at **every** poset and **every** `k`, attained at every `k`, so the class is
**closed by ceiling at every `k`**. Its own sharpest line is the relevant one here:
`sup_k alpha_k = ((n−1)/2)·gap_BK`, attained at `k = n−1` — i.e. **the compression route's best
possible output just *is* the BK gap, rescaled**, and that is capped at 1 against a bar of ≥ 2.

**And even if a BK-gap lower bound were wanted, it is already proven — sharply, since 2004.**

> **Theorem (Karzanov–Khachiyan chain; Wilson 2004, Table 1 + Prop. 3, on Bubley–Dyer 1999).** For
> **every** `n`-element poset `P`, `gap_BK(P) ≥ (1 − cos(π/n))/(n−1) = Θ(n⁻³)` — the free/antichain
> value. **The unconstrained chain is the minimizer**: adding poset relations never decreases the
> gap.

Independently verified in the corpus, exhaustively: `0 / 195` violations at `n = 4` and `0 / 4111`
at `n = 5`, **attained exactly** in both. *(Citation caveat, from the source: this is Wilson's
Table 1 plus Proposition 3, **not** a numbered theorem in that paper; the `Ω(n⁻³)` order predates
him — Bubley–Dyer §4 — and Wilson supplies the sharp constant. Cite it that way.)*

> **So the BK-spectral side of the programme is closed at both ends.** The upper bound is proven
> and hands over a cut; the lower bound is proven, sharply, by someone else, and **no consumer for
> it exists**. There is no third thing to ask the BK spectrum for.

### 4.4 What the live route to the wall actually consumes — and node B falls out of it

This is the observation that decides the framing question, and it is **documentary**, not
mathematical — it is a reading of what `STATE.md` says its own chain consumes.

`STATE.md:76–83` settled, at mg-a1db, what L1b's reduction stands on: **rows 5 and 7 and nothing
else** — the Buser test vector on `S|_{𝟙⊥}` and Diaconis–Graham, assembled into mg-210d's master
bound

```
    1 − λ_std  ≤  6·E[inv_e]/(n²−1)          (Thm 2.4)
```

*"no sector decomposition, no representation theory, and no claim about which irrep carries `λ₂`
appears anywhere in that chain, which runs entirely inside the `n × n` transport matrix."*

Now notice what that does to the diagram. Row 8 states L1b with hypothesis **frozen**, not
*"bad mixing"*:

- The **mermaid diagram** routes `A → B → C`: minimal counterexample → low-conductance BK cut → the
  `λ_std` bound, with the BK cut as L1b's input.
- **Row 8 and the machinery paragraph** route `A → C` **directly**: frozen ⟹ `(LIB-const)` ⟹ (by
  the master bound) `1 − λ_std ≤ ε_spec`, consuming rows 5 and 7 only.

**These are two renderings of the same link, and only the second is where the work is being done.**
Check it against the three residuals `STATE.md:180–193` lists as live, because they are the actual
work-in-progress and **not one of them is an attack on a spectrum**:

| residual | what it is an attack on | spectral? |
|---|---|---|
| **(B-cov)** — break the wrong-signed same-side covariance | the covariance term of `E[Σ disp²]`, a counting statistic of `L(P)` | no |
| **(EQ)** — `max_x \|E[pos_σ x] − rank_e x\| = O(1)` | a **first moment** of the position law; `STATE.md:186` calls it *"a cancellation statement rather than a decay statement"* | no |
| **(R)** — is there `D < 1` with `d(P) ≤ D` on every frozen poset? | the **incomparability density** `d(P) = m/C(n,2)`, a pure count on `P` itself | no — it *feeds* the already-proven `λ_std > 1 − d·n/(n+1)` |

Two are counting statistics of `L(P)`; the third is a count on `P`. The spectral statement is what
each of them would be *converted into* on arrival. So **on the routes that are actually live,
Theorem E's output is not consumed by anything**: if `(LIB-const)` is ever proved from frozen, the
chain runs `A → C` and node B drops out.

**This is the same shape as row 4.** `(A) SPREAD` was struck from the critical path at mg-a58f: it
remains **proven and true**, and it is simply **not consumed**. Node B is presently in that
position, with one difference worth stating: SPREAD was struck because a *later* unconditional
bound superseded the certificate route, whereas node B's consumer is the wall itself, so it would
return to the critical path if L1b were ever proved *through* the BK cut rather than through
inversions. **Kind of this observation: documentary, over the corpus at `c5cd288`. It is not a
proof that no BK-mediated route to L1b exists** — it is the report that none is live.

### 4.5 The non-spectral routes, so "the bridge" is judged against alternatives

*Assembled from `STATE.md`'s attempt index and literature status. Kinds are the ledger's.*

**(a) Kahn–Saks / Kahn–Linial entropy (Brunn–Minkowski on the order polytope).** The field's main
line. **Stuck at `δ ≥ 0.2764` for 30 years**, and **structurally cannot reach 1/3** — the *"blind"*
half, confirmed. `STATE.md:149` marks this *"avoid this aim"* and says the programme was **built to
escape it**. Additional hard negative: **coherence is INERT against it** (mg-61bb, `PROVEN`) —
coherence is a logical *consequence* of `δ < 1/3`, so it shrinks the class by zero, has zero
content on the ≤ 3 elements KS/BFT sees, and its only residual is a system of *upper* bounds that
can never force a positive lower bound.

**(b) Alexandrov–Fenchel / the combinatorial atlas** (Chan–Pak–Panova). The field's tool for
rational-rigidity extremal facts, **never aimed at the 1/3 gap**. Status here is a sharp negative:
**AF is *saturated*** — the fatal flat law and the Kahn–Linial `1/φ` optimum are *both* Stanley
equality cases, so **no AF *inequality* can separate them** (mg-a1ec). The remaining lever was AF
**equality-case** theory (Ma–Shenfeld), which produced a genuine **Window Rigidity Lemma** and
Theorem 5.2 (*full-support flat absolute-position law ⟹ `δ ≥ 1/3`*, independently verified,
non-circular) — but only **at the exact Stanley-equality endpoint**, leaving the
conjecture-relevant *approximate* flat law untouched. The residual, a **k=1 quantitative stability
theorem**, was then **REFUTED by hand unconditionally** and **mg-48ab's reduction to it proven
circular** (mg-dcae): a hypothesis-free Stanley-stability tool cannot exist, so any usable
statement *"must consume the frozen hypothesis directly."*

**(c) Correlation inequalities (FKG / XYZ).** **Wrong-signed.** `(B-cov)`, the same-side covariance,
is the residual `STATE.md` lists **first** and calls *"the sharp edge"* and *"the object three
separate routes converge on."* Also: marginal-only tools are dead by construction — **both faces
of the single lemma are false for abstract frozen distributions** (the two-atom law has every pair
frozen and `Θ(n²)` inversions), so the proof **must** reach into the joint law. That obstruction is
not spectral and is not avoided by any spectral rendering.

**(d) Width-2 and special classes.** **Width 2 is PROVEN** (Sah, arXiv:1811.01500: `δ ≥ ≈0.33876`,
a family reaching `≈0.34884`) — *"but by opaque casework, with no articulated reason."* Genuine
partial results here: probe C proves the **full conjecture for `s ≤ 2` free slots** and gives
`δ ≥ 5/18 ≈ 0.278 > 0.2764` on part of the `s = 3` family (**not** a global record beat — the
extremal posets have `s ≥ 4`, where the count dies at `≤ 1/s`); probe D proves **co-degree ≤ 1 ⟹
`δ ≥ 1/3`** but *"provably stops"* (the local bound decays like `2⁻ᵐ`, collapsing to `1/6` at
`m = 2`, exactly where frozen posets sit); probe B's diagonal-capacity bound certifies `δ ≥ 1/3` on
**~19% of `n = 7` posets**.

**(e) Verification ranges — and they clear nothing.** `n ≥ 12` **refereed** (Peczarski 2006, GPC
for all posets on ≤ 11 elements); `n ≥ 15` **unrefereed preprint** (Gupta 2026, through order 14,
carrying *"No independent per-poset check is made above order 9"*). **Both are verification ranges,
not structural bounds.** They fall short of `n ≥ 100` (master-bound route on primitive posets) by
85 and of the `n ≈ 900C` crossover by ≥ 885; against the `N₀` of `(LIB-weak) ⟹ (LIB-const)`
**no finite bound helps even in principle, because no `N₀` works for the class at all** (mg-c4f5
§5.3). **No structural lower bound on a minimal counterexample's size exists in the literature.**

**Reading the comparison honestly.** The non-spectral routes are **not** a rival that is winning.
(a) is stuck below the target and provably blind to it; (b) is saturated at the inequality level
and circular at the stability level; (c) is wrong-signed; (d) is real but confined to classes a
minimal counterexample need not be in. **The spectral programme's advantage over them is real and
is architectural** — it is the only route on the board that reduces the whole conjecture to *one*
named implication, which is a genuine achievement and is why `STATE.md` is organised around it.
**That advantage is a property of the *architecture*, not of the spectra.**

---

## 5. AN HONEST VERDICT ON THE FRAMING

**"Two axes, one bridge" is right. "The spectral route is the bridge" is not.**

**What survives, unqualified.** There are two axes and they are the right two:
*near-ordinal-sumness* and *balance/frozenness*. There is **one** bridge between them, it is
**L1b**, and the conjecture reduces to it. `STATE.md`'s central organising claim is intact, and it
is the programme's real asset.

**What does not survive is the word *spectral* attached to that bridge as a method.**

1. **The far side is a naming.** `STATE.md:15` says it itself: *"Almost every quantity we track —
   `λ_std`, inversion count, squared displacement, interface thinness, entropy — is the **same
   axis** in different units."* `λ_std` is **one unit among five**. Row 8 states the wall in *two*
   units in a single sentence. The master bound is the conversion. A proof would be delivered in
   inversions.
2. **The BK spectrum's one live contribution is an upper bound, and the architecture takes a cut
   from it, not a number** (§4.2). Nothing consumes a BK-gap lower bound (§4.3), and one is
   already proven sharply by Wilson.
3. **The transfer that would make the route spectral is refuted unconditionally and, conditionally,
   is the wall itself** (§3). A route whose conditional form is identical to its destination is
   not a route to that destination — it is a restatement of it. That is exactly the circularity
   mg-65f5 caught at `STATE.md:76`, and it is worth noticing that it was caught **inside** the
   spectral framing, by a reader asking what L1b's reduction consumes.
4. **Node B is presently unconsumed by any live route** (§4.4) — the row-4 shape.

**What it should be called instead.** Three candidates, in order of how much they change:

- **Minimal and accurate:** *"Two axes, one bridge — and the bridge is a **rigidity** statement
  whose live currency is `E[inv_e]`."* Keeps the whole architecture and demotes only the claim
  that the spectra are the mechanism.
- **More honest about the machinery:** call the spectral objects what they demonstrably are — a
  **dictionary** (row 3a licenses the word *"standard"*; row 1 licenses *"near-ordinal-sum"*) and
  **one proven ingredient** (row 5, Buser, inside the master bound). Both are `U`/`U-id` and both
  are genuinely used. Neither is a route.
- **The sharpest version, if the framing is to be tested rather than trimmed:** the programme is a
  **near-ordinal-sum programme** that *happens to be stated spectrally*. Its live obligation is
  `E[inv_e] ≤ (ε_spec/6)(n²−1)` under `δ < 1/3`, and its hardest known obstruction — that both
  faces are **false for abstract frozen distributions**, so the proof must reach the **joint law** —
  is a statement about measures on `L(P)`, with no eigenvalue anywhere in it.

**One thing this verdict does not say.** It does **not** say the spectral work was wasted or should
be unwound. The spectral framing produced Theorem E (`U`, proven, any width), row 3a's dictionary,
row 1's characterisation, the Buser inequality, and — through mg-210d — the master bound that is
the reason the wall has a clean combinatorial form at all. **It also produced the audits that
found its own circularity.** The claim here is narrower and it is the one Daniel asked to have
tested: *given all that, is the spectral route still the thing that will get us across?* **The
ledger says no, and it has been saying so, one row at a time, since mg-4a86.**

---

## 6. KINDS AND SCOPE — the standing rule applied to this document

`STATE.md:99`: *"Any prose that **aggregates** rows must state the **WEAKEST** kind in the set it
names."* §0 aggregates. So, at the claim:

| statement | kind | warrant |
|---|---|---|
| `S_P = ρ_std(η_P)`; `λ_std = 1 ⟺` ordinal sum; Buser; GID+DG; Theorem E; `alpha ≤ 1` | **`U` / `U-id`** | ledger rows 1, 3a, 5, 6, 7 and mg-409a/mg-8d66, on the ledger's own authority — **not re-audited here** |
| `λ_std` and `λ₂^BK` are incomparable in both directions | **`FP✗`** | exact rationals, mg-d1be; a refutation, hence at universal strength |
| `λ₂^BK ≠ λ_std` at every poset | **`FP`**, `n = 4,5` exhaustive (`0/4306`) | the *inequality* is `FP✗`; the *never-equal* claim is `FP` and says nothing above `n = 5` |
| the "exactly the ordinal sums" characterisation | **`FP`** to `n ≤ 6`, **`FP✗`** at `n = 7` | mg-d1be; the `n=7` witness refutes it |
| standard dominance, unconditional | **`FP✗`** — refuted | 166 refuters, **read from mg-8b64, not re-measured here** |
| standard dominance, all-pairs-frozen conditional | **`OPEN`** | **it is row 8**, not support for row 8 |
| `SD-quant` `c ≥ 0.978898` | **`FP`**, `n ≤ 6`, **informative stratum only**, and **the `n = 7` refuters are outside the sweep** | frame is load-bearing; source predicts `c ≈ 0` there |
| Wilson's `gap_BK ≥ (1−cos(π/n))/(n−1)` | **literature**, verified `FP` at `n = 4,5` | Table 1 + Prop. 3, **not a numbered theorem** |
| `step8.tex` contains no BK-gap lower bound consumer | **re-measured here**, `912f1b1` | `lambda_2`: 0; lowercase `gap`: 25, all proof gaps; `spectral`: 2 |
| *"no consumer of a BK-gap lower bound exists in the programme"* | **not a mathematical kind at all** | a claim over a **corpus**. It is a search, and a search over a corpus is the same shape `0/132` was. mg-145f files its own frame at its §6 condition 2; **mine is §7 below** |
| *"node B is unconsumed by any live route"* | **documentary**, over `STATE.md` at `c5cd288` | a reading of what the ledger says its chain consumes — **not** a proof that no BK-mediated route exists |

**The weakest kinds in the set §0 aggregates are the last two rows**, and they are the ones to
attack.

---

## 7. WHAT THIS DOCUMENT DOES NOT DO, and where it can be wrong

1. **No new mathematics.** No eigenvalue was recomputed here. The `A₂ ⊕ A₂`, `A₃ ⊕ A₃`, antichain
   and `n = 7` witnesses are **read from mg-d1be's certificates**, which are exact-rational and
   reproducible at `scripts/onethird_mgd1be_reverse_cheeger_ineq_audit.py` on
   `one_third_width_three` `origin/main`. **I did not run them.**
2. **`166` and `0/132` are read, not measured** — here as everywhere; both are inherited three
   citations deep and both carry frames that have already been mis-stated once.
3. **The `no-consumer-exists` verdict is a corpus search, and I inherited it.** I re-measured only
   its `step8.tex` half. My frame: `STATE.md` at `c5cd288`; `docs/` of this repository;
   `one_third_width_three`'s `step8.tex`, `step1.tex`, `main.tex` and four `docs/` files. **I did
   not read the Lean artifact, `spectral_near_ordinal_sum_program.tex` (which is not in this
   repository), or the rest of `one_third_width_three/docs/`.** A consumer outside that frame
   would falsify §4.3.
4. **§4.4 is the strongest claim I make and it is documentary.** If someone produces a live route
   to L1b that runs *through* the BK cut, node B returns to the critical path and the verdict in
   §5 weakens from *"not the bridge"* to *"not the only bridge."* It does not reverse: §3's
   incomparability is `FP✗` and independent of that.
5. **`STATE.md` is deliberately NOT edited.** It is size-ratcheted (mg-e331) and this ticket asked
   for a document, not a ledger change. If the §5 verdict is accepted, the edits it implies are to
   the *"Two axes, one bridge"* heading (`:23`) and possibly a rider on the mermaid diagram's
   `A → B → C` routing (`:65–66`); **both would need the documented ceiling raise**, and neither is
   made here.
6. **A defect of my own, kept.** My first pass counted `gap` case-insensitively in `step8.tex` and
   got **51**, against mg-145f's 25, and I briefly had a discrepancy where there was none: the 25
   is lowercase-only and the other 26 are `\textbf{[GAP:]}` labels — the *same* category, so the
   finding was never in doubt, only my measurement of it. It is recorded because a number quoted
   without its frame is this document's own subject, and I reproduced the failure inside it on the
   first try.

---

## 8. Sources

- [`STATE.md`](../STATE.md) — `:15` (one-paragraph state), `:23–26` (two axes), `:44` (glossary,
  `λ_std`), `:57–72` (the chain), `:76–83` (what L1b's reduction consumes), `:85–103` (kinds),
  `:109–120` (ledger rows 1–11), `:126–137` (the single lemma), `:141–172` (attempt index),
  `:178–197` (where the threads converge), `:207–213` (why 1/3; literature status).
- [`docs/OneThird-Compression-Consumers-mg-145f.md`](OneThird-Compression-Consumers-mg-145f.md) —
  §3 (the enumeration), **§5 (is there any consumer of a BK-gap lower bound at all)**, §5.5.
- [`docs/OneThird-Compression-W4-Rate-mg-409a.md`](OneThird-Compression-W4-Rate-mg-409a.md) — §2
  (the bar), §3 (the ceiling), §4.
- [`docs/OneThird-Compression-kFoliation-mg-8d66.md`](OneThird-Compression-kFoliation-mg-8d66.md) —
  the bar and ceiling are both `k`-independent; `sup_k alpha_k = ((n−1)/2)·gap_BK`.
- [`docs/OneThird-TheoremE-Width-and-Row-Kinds-mg-957a.md`](OneThird-TheoremE-Width-and-Row-Kinds-mg-957a.md)
  — row 6's width hypothesis, present and inert.
- `one_third_width_three` @ `origin/main` `949c439` —
  `docs/OneThird-L1b-Reverse-Cheeger-Proof-Attempt.md` **§5 and §5.0′** (the mg-d1be repair, landed
  `bde9610`; **not in the `main-mirror` checkout**);
  `docs/OneThird-StandardDominance-ComparisonRoute.md` §1 (three statements), §2 (SD-BK is false),
  §3 (static vs dynamic; no standard sector), §4 (Wilson), §7 (SD-quant);
  `step8.tex` §G1 (Theorem E), `step1.tex:20–26` (BK graph), `main.tex:283–291`.
- Work items: `mg-d1be` (incomparability), `mg-4a86` (the comparison route, Wilson),
  `mg-8b64` (the 166 refuters — read), `mg-b0a6` (the `0/132` — read, with its frame),
  `mg-55f2` / `mg-65f5` / `mg-a1db` (row 3b's restatement and the `:76` strike),
  `mg-210d` (the master bound), `mg-a58f` (row 4 struck off the critical path).
