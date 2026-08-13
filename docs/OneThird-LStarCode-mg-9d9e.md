# The `L*` code, built and run — the test is passed where it cannot discriminate, impossible where it can, and the one construction on record is the free bound wearing a different coordinate system

**mg-9d9e.** Scoping recommendation to `pm-onethird`, successor to
[`mg-99f4`](OneThird-SubsetConsumability-mg-99f4.md), filed on its §4.5:
*"The first move is a **run**, not a theorem: build the `L*` code and measure its expected length
against `⌈log₂ n!⌉` at `n = 6…12`."* That is what this is.
Instrument: [`code/lstar_code_9d9e/`](../code/lstar_code_9d9e/), `run_all.sh`, **~20 s measured**.
Predictions pre-registered at `ca9ddcf`, before one line of the arms existed.
Successor: **`mg-872c`**.

---

## 0. The result, in four lines

> 1. **`compression2`'s `L*` construction, read as a code, IS the free code.** The tape is a
>    bijection and the binomials telescope, so indexing its words exactly costs `log₂ n!` at every
>    permutation, every poset, every `n`. It cannot beat `⌈log₂ n!⌉` — it *equals* it. The
>    fixed-width reading is worse: it **loses** at every `n ≥ 3`.
> 2. **The test cannot be passed at all where it would discriminate.** `e(antichain) = n!`, so
>    `E[len] ≥ log₂ n!` there for **every** code by Gibbs. A shape-B bound `log₂ e(P) ≤ c·log₂ n!`
>    with `c < 1` valid at every `P` **does not exist** — not "none found": none can exist.
> 3. **And it is free to pass where it can be run.** On the closest instantiable population to
>    hypothesis (1) — the `δ = 1/3` boundary — `log₂ e(P) = Θ(n)` against a free bound of
>    `Θ(n log n)`, so every code that reads `P` at all wins by a margin that **grows with `n`**.
>    A four-line code delivers a shape-A constant of `0.155` at `n = 12` where `compression2`
>    claims `0.9399`. Passing carries no information.
> 4. **The population the bound is literally about is EMPTY at every `n` the ticket names.**
>    Frozen is `δ < 1/3`; it is empty at `n ≤ 5` on this directory's own enumerator, empty to
>    `n = 8` on the corpus's, and the conjecture is verified to `n = 14`.

So the one-line test is a **real necessary condition and not a screen**. What screens is
`mg-99f4`'s own **Q2**, and §5 puts a code to it and gets an answer: an unconditional, fully
consumable bound `log₂ e(P) ≤ n log₂ w(P)` — which is vacuous exactly where the programme needs
it. **The same dichotomy a third time.**

## 1. The test as worded is passed by the code it compares against

`⌈log₂ n!⌉` is the reference code's length **after rounding**. The reference code's own ideal
length is `log₂ n!`, so it beats its own ceiling at every `n` where `n!` is not a power of two —
`0.5081` bits at `n = 6`, `0.1645` at `n = 12` (`s1.3`).

That is not pedantry, because it is exactly how the antichain row reads: `MERGE-P` at the
antichain has expected length `log₂ n!` **exactly**, and therefore passes the literal test at
every `n = 6…12` — by the rounding and by nothing else. `s1.3` prints three verdicts,
`YES` / `ROUND` / `NO`, rather than two, for that reason.

> **The test with content is `beat log₂ n!`, and the quantity that carries is the MARGIN.**

## 2. `compression2`'s own construction, run

`s1.1`, `n = 6…12`, and no poset appears in the table because none is needed:

| `n` | `⌈log₂ n!⌉` | exact-index tape | fixed-width tape |
|---|---|---|---|
| 6 | 10 | **9.4919 = log₂ n!** | 16 — loses by 6 |
| 8 | 16 | **15.2992 = log₂ n!** | 24 — loses by 8 |
| 12 | 29 | **28.8355 = log₂ n!** | 44 — loses by 15 |

The tape is a bijection `S_n → ∏(words)` — `s0.3`, 0 collisions at `n = 4…8`, `mg-0fc6` a1.1
reproduced on independent code — and `∏ C(a+b,a) = n!` over the tree at every `n ≤ 16` (`s0.4`).
**A re-coordinatisation of the free code is the free code.** `mg-0fc6`'s own sentence says it from
the other side: *"`compression2`'s encoding forgets **nothing** — it is a re-coordinatisation."*

`s0`'s **D5** makes the point from the plant side and is reported as an **inert** plant: bisect the
tree the other way and the exact-index reading is *still* exactly `log₂ n!`, because the
telescoping is a property of **any** binary tree over the elements. **No repair to the tree can
rescue this reading**, so the plant is a defect the claim cannot express — and that is worth more
here than a live plant would be.

**What `compression2` actually bounds is therefore not a codelength.** It is the **entropy** of the
merge words under `Unif(L(P))`, bounded node by node — a statement about the *measure*. `s1.6`
measures those per-node entropies where they can be instantiated, and the chain rule is its own
control: they sum to `log₂ e(P)` **exactly** at `n = 6, 9, 12`.

| `n` | node size | `H(word ∣ earlier)` | note's ceiling `0.9399(a+b)` | overpay |
|---|---|---|---|---|
| 12 | 2 | 3.6732 | 7.5192 | 2× |
| 12 | 3 | 2.6667 | 11.2788 | 4× |
| 12 | 6 | **0.0000** | 11.2788 | **infinite** |
| 12 | 12 | **0.0000** | 11.2788 | **infinite** |

A node whose split falls on a block boundary is **forced** and carries no entropy at all; the
per-node lemma pays `0.9399(a+b)` bits for it. ⚠️ **And which nodes those are is an arithmetic
accident of `n`.** At `n = 9` the elements bisect `4|5` while the blocks are `3|3|3`, so the root
straddles a block and carries `0.6667` bits — where at `n = 6` and `n = 12` the top two levels are
free. **The tree is built from `L*`, and `L*` knows nothing about the block structure.** That is
`mg-0fc6` §2's wash-out in its sharpest form: at the one place the poset could have entered the
construction, it did not.

⚠️ This prices the note's **per-node lemma on one family**. It is not a refutation of its theorem,
which is a worst-case statement and is entitled to be loose anywhere in particular.

## 3. The codes that read `P`, and the answer to the ticket's question

Seven codes, six families, `n = 6…12` (`s1.2`). Every one is presented as a sub-probability `q`
with `Σ q ≤ 1`, so `log₂ e(P) ≤ E[−log₂ q]` by Shannon at every row; `s0.6` checks Kraft **exactly**
and `s0.7` checks the bound itself at all 4 472 posets with `n ≤ 5`.

**The `L*` code — `MERGE-P`, each node's word indexed among the `P`-feasible ones — beats
`log₂ n!` at every non-antichain family and every `n = 6…12`, and ties it exactly at the
antichain.** At `n = 12`: `+22.2` bits of margin on the boundary family, `+19.0` on two chains,
`+0.000` at the antichain.

**It is polynomial per node — a 2-D DP over the two sequences — and never enumerates `L(P)`.** So the ticket's question has a **YES**, and
it is cheap. What the rest of this document is about is what that YES is worth.

### 3.1 `L*` is not what is doing the work

`MINIMALS` — index the next element among the currently minimal ones — reads `P`, **never reads
`L*`**, and is four lines long. Over the 42 `(family, n)` cells: `MERGE-P` wins 11, `MINIMALS`
wins 3, **28 ties** (`s1.5`). On the boundary family they are **equal at every `n`**, both at
`5/3` bits per block against a truth of `log₂ 3 = 1.585`.

> ⚠️ **`P5` REFUTED, kept as written.** It predicted `MINIMALS` would **beat** `MERGE-P` on the
> boundary family (`5/3` against `2`). They tie: the `L*` order inside a block is `a, c, b`, the
> bisection splits it `a | c, b`, and the two codes come out identical. The prediction was right
> about the mechanism and wrong about the arithmetic.

Either way the conclusion is the same: **the win over the free bound is bought by reading `P`, not
by reading `L*`.**

### 3.2 And the `L*`-reading codes are blind exactly where the bound is tight

`L*` **does not exist at the antichain** — every marginal is `1/2`, so the majority tournament ties
at every pair. `LEHMER-L*` is the one row in `s2.1` whose worst case is not at the antichain, and
the reason is that it is *undefined* there. The single poset that decides the worst case is the
one poset an `L*`-reading construction cannot see.

## 4. The two impossibilities, and they are one line each

### 4.1 No code beats the free bound at the antichain

`e(antichain) = n!`, so `log₂ e(P) = log₂ n!` there, and `E[len] ≥ log₂ e(P)` for every code.
Hence `max_P E[len] ≥ log₂ n!` for **every family of codes `{C_P}` that will ever be written**, and

> **a shape-B bound `log₂ e(P) ≤ c·log₂ n!` with `c < 1` valid at every `P` does not exist.**

Measured exhaustively as a control: 7 codes × 219 posets at `n = 4` and × 4 231 at `n = 5`, every
worst case at or above `log₂ n!` (`s2.1`). The best shape-A constant any code can deliver over all
`P` is `log₂ n!/(n log₂ n)`, which **rises to 1**: `0.656` at `n = 10`, `0.790` at `n = 10²`,
`0.938` at `n = 10⁷`.

### 4.2 `16,777,063` is two statements and one number

`s2.2` reproduces `mg-0fc6` a1.6's crossover **to the unit** on this directory's own code
(`c = 1 − 1/(24 ln 2)`), which licenses reading it twice:

| | |
|---|---|
| `n = 16,777,062` | `c·n log₂ n = 378 445 095.033 ≥ log₂ n! = 378 445 095.004` — **VACUOUS**, implied by the free bound |
| `n = 16,777,063` | `c·n log₂ n = 378 445 118.947 < log₂ n! = 378 445 119.004` — **FALSE at the antichain**, so carried entirely by hypothesis (1) |

> **`P8` holds: there is no `n` at which `compression2`'s theorem is both non-vacuous and
> hypothesis-free.** Below `n*` it says nothing; above `n*` it is refuted at the antichain unless
> the hypothesis excludes it — and `δ(antichain) = 1/2 > 1/3`, so it does. The `n` where the bound
> starts to bite is the `n` where it starts to need its hypothesis, and it is the same `n`.

This sharpens `mg-99f4`'s reading of the same number. There, `1.7×10⁷` was *"arithmetic about two
reference scales, not a fact about its merge tree"*. It is also arithmetic about where the
hypothesis becomes load-bearing.

⚠️ The `57,186` discrepancy between the printed `0.9399` and the computed constant is `mg-99f4`'s
finding and is **cited, not rediscovered**.

## 5. What the test cannot say, and what `Q2` can

### 5.1 The target class is empty at every `n` the test can be run at

`s2.3`. Frozen is `δ < 1/3` and non-chain:

| `n` | frozen posets reachable | source |
|---|---|---|
| 3, 4, 5 | **0** | exhaustive, this directory (`s0.9`) |
| 6, 7, 8 | **0** | `mg-9b6b`, exhaustive over iso classes — **cited** |
| 9 … 14 | **0** | the conjecture is verified to `n = 14` — **cited** |
| ≥ 15 | unknown | the only place a frozen poset can be |

**So *"at the `n` you claim it"* names an `n` at which the population is empty.** A run there is a
fact about the population's size, not about the code — `mg-0b96`'s trap arriving one arm along,
which is why `s1` runs on the **boundary** (`δ = 1/3`) and says so in its own header.

### 5.2 On the boundary, passing is free

| `n` | `log₂ n!` | `log₂ e(P)` | `MERGE-P` | shape-A `c` | shape-B `c` |
|---|---|---|---|---|---|
| 6 | 9.492 | 3.170 | 3.333 | 0.2149 | 0.3512 |
| 9 | 18.469 | 4.755 | 5.000 | 0.1753 | 0.2707 |
| 12 | 28.835 | 6.340 | 6.667 | **0.1550** | **0.2312** |

Both constants **fall with `n` and keep falling** — not because the code is good but because the
population has `log₂ e(P) = Θ(n)`. And that is a property of the hypothesis, not of this family.
`s2.4`, exhaustive over all non-chain posets at `n = 5`, bucketed by `δ`:

| `δ ≤` | max `e(P)` over `{δ ≤ this}` | as % of the free bound |
|---|---|---|
| **1/3** | **3** | **22.9%** |
| 2/5 | 25 | 67.2% |
| 1/2 | 120 | 100.0% |

⚠️ **The per-bucket column is NOT monotone and that is printed rather than smoothed** — `δ = 2/5`
carries `e(P) = 25` while `δ = 3/7` above it carries `7`. What is true is the **cumulative**
statement, and it is the cumulative statement a hypothesis consumes.

> **Hypothesis (1) buys exactly the regime where the free bound is already loose by an order.**
> That is why every code passes there, and why passing carries no information about the code.

### 5.3 One code put to `Q2`, and it comes back with a real bound

`mg-99f4`'s Q2 asks whether the value is obtainable without enumerating `L(P)`. For `MINIMALS` it
is, and the argument is one line: **at every step the available minimals form an antichain**, so
there are at most `w(P)` of them, so

> **`log₂ e(P) ≤ E[len] ≤ max_L len(L) ≤ n log₂ w(P)`** — unconditional, and `w(P)` is polynomial
> to compute.

It beats the free bound **exactly when `w(P) < n/e`** (`s2.5`, checked at every family). On the
boundary family `w = 2`, so it gives `n` bits against a truth of `0.528 n` and a free bound of
`n log₂ n − 1.443 n`.

**So a consumable, unconditional, order-beating bound does exist.** And it is vacuous exactly where
the programme needs it: a frozen poset is a **dense** one (`mg-0b96`'s open region is `d ≳ 2×10⁻²`
and **widening**), and dense means wide. ⚠️ *`dense means wide` is stated as the reason it is
expected to be vacuous there; it is **not** measured on the frozen class, because the frozen class
is empty.*

## 6. RECOMMENDATION TO `pm-onethird`

1. **The prefix-code branch has had its run, and the run says the branch is not closed but its
   ACCEPTANCE TEST IS SPENT.** Every code on record either equals the free bound (`MERGE-IDX`,
   which *is* it), loses to it (`MERGE-TAPE`), or beats it by an amount that measures the
   population rather than the code. **Do not ask a proposal whether it beats `⌈log₂ n!⌉`.** The
   answer is yes for anything that reads `P`, and no for anything that does not, and neither
   answer is about the proposal.
2. **Ask the two questions that survive, and they are `mg-99f4`'s own, restated for codes.**
   **Q1′ — what does your code's expected length do at the ANTICHAIN?** If it is not `log₂ n!` your
   code is wrong; if it is, your bound is conditional and you must say on what.
   **Q2′ — is `E[len]` bounded by a formula in `P` that does not enumerate `L(P)`?** A code whose
   length you can only *measure* is `e(P)` with extra steps. `n log₂ w(P)` passes both and is the
   benchmark any proposal now has to beat.
3. **Retire `compression2`'s tape as a CODE and keep it as an ENTROPY DECOMPOSITION.** The two are
   different objects and only the second was ever the note's claim. `s1.6` shows where its slack
   is — at the top of the tree, where the conditional entropies are zero and the per-node lemma
   still charges `0.9399(a+b)`.
4. **`16,777,063` should be quoted with both readings or with neither.** The number where the
   bound starts to bite is the number where it starts to need its hypothesis.
5. **The F24-multiplier branch: SCOPE, do not fund, and NAME THE THIRD AXIS FIRST.** §7.
6. **The prior stands and is now four closures old.** Assume a code will be vacuous unless shown
   otherwise. ⚠️ **What is NOT ruled out here, and is the only object left in this direction:** a
   code whose expected length is bounded *from hypothesis (1)* by something below `log₂ n!` — i.e.
   a proof that `δ(P) ≤ 1/3` forces the merge words to be predictable. That is `compression2`'s
   actual programme, it is not touched by anything above, and §5.2 says what it is up against: the
   hypothesis already gives `Θ(n)`, so a bound of shape `c·n log₂ n` for any `c` is asking for far
   less than the truth.

## 7. The F24-multiplier branch — a scoping recommendation, not a decision

`mg-99f4` §4.4 left this open and named the reason: **the third axis is unnamed**, so the parameter
space has no coordinates. Daniel, 20:20Z: *"compressions trade off between preservation of linear
stats, entropy preservation, and one other metric iirc."*

`s3` runs `mg-99f4`'s screen on the object the two **named** axes are functions of: the **scale
profile** `prof(P, f) = (‖D_l f‖²)_l` of the F24 filtration, with `f = inv_e` because `STATE.md`
names `E[inv_e]` as the live currency.

- **`s3.1` — the variance identity holds exactly** at 595 posets, `n = 4, 5`, exact rationals, 0
  deviation. ⚠️ **Corroboration, not news** — F24's own honest scoping, which the registry requires
  to travel with the entry, says the identity is Pythagoras and holds for *any* filtration.
- **`s3.2` — Q1: PASSES.** `res = 23` at `n = 4`, `387` at `n = 5`; worth `2.42` and `3.87` bits
  against the free bound. ⚠️ **Q1 is a floor, not a signal.** `mg-99f4`'s `|E|` row passed it too —
  it was a near-oracle — and failed anyway.
- **`s3.3` — Q2: FAILS, the same way `T2d` does.** The profile is a variance decomposition *of the
  measure* `Unif(L(P))`; every entry is a conditional expectation under it, so computing it needs
  `L(P)`. **And no choice of weights repairs that**: `M = Σ λ_l D_l` picks a linear combination of
  entries that each individually need `L(P)`. The parameter space does not contain a point that
  changes the cost.

| object | needs `L(P)`? | Q1 | Q2 | verdict |
|---|---|---|---|---|
| `mg-99f4` T2a/T2b/T2c | no | **NO** | — | NO — Q1 |
| `mg-99f4` T2d, BK edge count | YES | yes | **NO** | NO — Q2 |
| **F24 scale profile of `inv_e`** | YES | yes | **NO** | **NO — Q2** |
| this ticket: `MERGE-P` / `MINIMALS` length | no | yes | yes | see §5.3 |

**RECOMMENDATION: the branch is not fundable as stated, and the blocker is one sentence, not a
result.** Name the third axis. Then:

- if it is a functional of the **measure**, it inherits `s3.3` verbatim and fails Q2;
- if it is a functional of **`P` alone**, it is closed already by `mg-8b32`'s C1.

Those two cases are exhaustive over what the phrase can mean, which is the strongest thing that can
be said without the name. **What would change this is a third possibility nobody has proposed: an
a-priori BOUND on the profile computable from `P`** — a different object from a weight.

⚠️ **What `s3` does NOT measure**, stated so it cannot be read as measured: whether some `λ` forces
a bound (untestable against an unnamed axis); realizability (`mg-0fc6` a2 measured the wash-out for
the *marginals*, and the profile is a functional of the measure, so that argument does **not**
transfer — which is not the same as separating, and by `mg-99f4`'s dichotomy whatever the profile
does at a non-realizable measure is worth **zero** toward a bound).

## 8. The control that fired, and it fired on this arm's own construction

`s0.6`'s first draft asserted that `MERGE-P`'s Kraft sum is exactly `1`. **It went RED.** The claim
was wrong; the docstring asserting it has been corrected and the control kept.

Feasibility is checked **locally**. Two locally valid halves need not be interleavable: at
`P = {1<3, 2<0}` with halves `(0,1)` and `(3,2)`, the union with `P` closes the 4-cycle
`2 < 0 < 1 < 3 < 2` and there are **zero** feasible merges. The bottom-up code can reach a dead
end, mass leaks, and the Kraft sum comes out **below** 1 — `3/4` at that witness, worst `2/3` at
`n ≤ 5`, first at `n = 4` (4 of 219 posets, 96 of 4 231 at `n = 5`).

Every bound in this document still stands: `s0.6` checks `Kraft ≤ 1` and `s0.7` checks
`E[len] ≥ log₂ e(P)` directly, at every poset. What the leak costs is **optimality**, and the
repair is the tight version — which is the optimal code, which costs the enumeration. **A remedy is
an artifact of the same kind as the defect**, and here the only remedy is the thing the programme
cannot afford.

## 9. Predictions: 8 of 10 confirmed, 1 refuted, 1 confirmed with a clause it did not have

| | outcome |
|---|---|
| P1 exact-index tape ties `log₂ n!` | **CONFIRMED** (`s1.1`, `s0.4`) |
| P2 fixed-width tape loses at every `n ≥ 3` | **CONFIRMED** (`s1.1`) |
| P3 `MERGE-P` beats it off the antichain, ties on it | **CONFIRMED** (`s1.3`) |
| P4 margin grows with `n` on the boundary family | **CONFIRMED** (`s1.4`) |
| **P5 `MINIMALS` beats `MERGE-P` on the boundary family** | ⚠️ **REFUTED — they TIE** (`s1.5`) |
| P6 no code beats the free bound at the antichain | **CONFIRMED** (`s2.1`) |
| P7 the target class is empty at every reachable `n` | **CONFIRMED** (`s2.3`) |
| P8 `16,777,063` is bite and hypothesis-need at once | **CONFIRMED** (`s2.2`) |
| P9 F24 profile passes Q1, fails Q2 | **CONFIRMED** (`s3.2`, `s3.3`) |
| **P10 zero entropy at block-boundary nodes** | **CONFIRMED, plus a clause it did not have**: which nodes those are is an arithmetic accident of `n` — at `n = 9` the root is not one (`s1.6`) |

## 10. Scope, and what this does NOT establish

- ⚠️ **NOT that no code can carry the programme.** §6.6 names the object that survives.
- ⚠️ **NOT anything about the frozen class.** It is empty at every `n` reached. Every number here
  is on the **boundary** (`δ = 1/3`) or on named families, and `mg-6ff4`'s F1 corollary warning
  applies verbatim.
- ⚠️ **NOT a closure of the F24 branch.** §7 is a screen with its own not-measured list.
- ⚠️ **Nothing above `n = 5` is exhaustive.** `n = 6…12` is six named families. What carries above
  `n = 5` is §4's one-line arguments; the tables are corroboration and are not the warrant.
- ⚠️ **`s3.1` is corroboration of F24 (B), not a second warrant for it.** The identity is
  Pythagoras.
- **NOT DONE, per the ticket's own scope.** `STATE.md` is not edited and the ratchet is untouched;
  `docs/FACTS.md` gets **no** entry — every measurement here is consumed by this landing and its
  successor, which fails the registry's homelessness test (`mg-3da1`'s reason); `docs/CONCEPTS.md`
  gets no row.

---

*`mg-9d9e`. Instrument: [`code/lstar_code_9d9e/`](../code/lstar_code_9d9e/) — `run_all.sh`, ~20 s,
exit 0 = all four arms green. Two consecutive runs are byte-identical on all four transcripts; no
clock, no `random`. It imports nothing from `code/`.*
