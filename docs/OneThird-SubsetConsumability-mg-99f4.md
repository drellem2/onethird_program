# Separation and consumability are supported on DISJOINT parts of the domain — so the arbitrary-subset class closes, and it closes without touching prefix codes

**mg-99f4.** Scoping recommendation to `pm-onethird`. Instrument:
[`code/subset_consumability_99f4/`](../code/subset_consumability_99f4/). Successor: **`mg-9d9e`**.

---

## 0. The result, in one line

> A construction `Φ : 2^{S_n} → V` can be **consumed** only at the inputs where an `e(P)` exists
> — and those are exactly `LL_n = {L(P) : P a poset on [n]}`. It can **separate** only by what it
> does elsewhere. A function's value at one point does not constrain its value at another.

So *separation* and *consumability* are **independent coordinates of the same function**. The
ticket's stated asset — the BK graph read on `supp(μ)`, **12 edges against 0** — is a statement
about `Φ` **off** `LL_n`; every bound on `e(P)` is a statement about `Φ` **on** it.

**It is worth exactly zero toward the ticket's requirement. Not "not yet" — provably zero.**

The ticket instructed: *"Assume the third will be [unusable] too unless it is shown otherwise,
and say so early if it is."* It is, and this is the early sentence.

## 1. Why this is a closure and not a failed search

`c776`'s warning was that an exact, non-circular characterisation can still tighten nothing.
This is a different and cheaper kind of statement: it does not examine any separator's content
at all. It observes that the two properties the ticket asks to be **conjoined** are supported on
**disjoint parts of a function's domain**, so one cannot inform the other.

**Made constructive rather than rhetorical** (`s1.3`, `n = 3`). Take `Φ` = the BK edge count and
build two variants:

| construction | on `L(antichain)` | on the witness `S = {id, rev}` | separates? | bounds |
|---|---|---|---|---|
| `phi_bk` | 6 | 0 | YES | identical |
| `phi_sep` — off `LL_n` return `−1` | 6 | −1 | YES | identical |
| `phi_blind` — off `LL_n` read the poset `π` determines | 6 | 6 | **no** | identical |

All three **agree at all 19 consumable inputs**, verified elementwise, so they support literally
the same bounds. Separation moved from `YES` to `no` **without changing a single bound**. The
witness is `S = {id, reverse}`, which has the antichain's marginals (all `1/2`) and is not an
`L(P)` — the ticket's 12-against-0 reproduced in shape at `n = 3` on this directory's own code.
⚠️ **In shape and not in position**: `mg-8b32`'s witness sits inside hypothesis (1); the
antichain has `δ = 1/2` and this one does not.

**And the class does not survive its own enlargement.** `LL_n ↔ posets` is a **bijection**
(`s1.1`, injective at `n = 2…5` against A001035; the inverse `P = ⋂L(P)` is exhibited at `s0.3`).
So `Φ` restricted to the consumable inputs **is a function of `P`** — `mg-8b32`'s C1 reached by a
road that never mentions `π`: the *set* `L(P)` already determines `P`, so reading the set reads
nothing the poset did not carry. Daniel's class survives C1 **only** because `S` ranges wider
than `LL_n`, and `s1.2` prices that width: at `n = 5` the class hands a construction `2^120`
inputs, of which **4231** carry an `e(P)`. Every input the enlargement adds is one at which there
is nothing to bound.

## 2. The screen, and 4 of 4 on record fail it

`s1.4`–`s1.7`. A candidate is consumable only if it passes **both**:

- **Q1 RESOLUTION** — is `Φ` non-constant on `LL_n`? *(one pass over the posets)*
- **Q2 COST** — is `Φ(L(P))` obtainable without enumerating `L(P)`?

Separation is not among them and **cannot be**, by §1.

| `mg-8b32` b2.3 TIER-2 row | `res(Φ)` at `n = 3,4,5` | worth, in bits | verdict |
|---|---|---|---|
| `L* ∈ S` | 1, 1, 1 | **0.0000** | NO — Q1 |
| `\|S\| = e(P(π(S)))` | 1, 1, 1 | **0.0000** | NO — Q1 |
| `S` is a weak-order ideal under `L*` | 1, 1, 1 | **0.0000** | NO — Q1 |
| the BK edge count on `S` | 4, 10, 29 | 2.59 / 4.59 / 6.91 | NO — Q2 |

The **sharpest** bound derivable from `Φ` is `B_Φ(v) = max{e(P) : Φ(L(P)) = v}`; nothing weaker
is a bound and nothing stronger is derivable, so `s1.5` measures the *whole* consumable content.
Three rows come back at **zero bits at every `n`**: each is a predicate whose entire content is
*the realizable inputs are realizable* — perfect separation, no resolution. **That is
`gap(μ) = log₂ e(P) − H(μ)`'s defect wearing different clothes**: there the constant is `0`, here
it is `True`.

The fourth is the survivor. It fails on **cost**: `|E|` is a sum over `L(P)`, and `e(P) − 1 ≤ |E|`
by BK-graph connectivity, so `e(P) ≤ |E| + 1` bounds what we cannot compute by a larger thing we
can compute only by computing it. ⚠️ **The run refuted the prediction here and the refutation
strengthens the verdict**: `|E|` determines `e(P)` **exactly** at `n = 3, 4`, with the first
ambiguity a single value at `n = 5`. A near-oracle, and still unconsumable — on cost alone.

## 3. The acceptance condition for the prefix-code branch — and it moves the dial off the constant

The ticket demanded the crossover be stated first. `s2` answers it for the **family**.

A bound of **shape A**, `log₂ e(P) ≤ c·n log₂ n`, beats the free bound `log₂ n!` exactly when
`log₂ n > log₂(e)/(1−c)`:

> **`n*(c) = 2^(1.442695/(1−c))`** — doubly exponential in `1/(1−c)`, elasticity
> `d(ln n*)/dc = 1/(1−c)²`, which is **277** at `compression2`'s own constant.

`s0.6` reproduces `mg-0fc6` a1.6's published **16,777,063 to the unit** on code sharing nothing
with it, which licenses the table:

| target `n*` | required `c` | saving `1−c` | vs `compression2`'s 6.01% |
|---|---|---|---|
| `10^7` | 0.9380 | 6.20% | 1.0× |
| `10^3` | 0.8559 | 14.41% | 2.4× |
| **`10^2`** | **0.7899** | **21.01%** | **3.5×** |
| `20` | 0.7066 | 29.34% | 4.9× |

**The frontier that matters is `n ~ 10^2`, not `10^7`** — `mg-0b96` prices the `d`-lever at
`n = 99`. The ticket's own bar is the weak form: a proposal clearing `10^7` by 1000× is still
3.5× short of the constant it needs where the programme lives.

**But the finding is the shape, not the constant** (`s2.4`). A bound of **shape B**,
`log₂ e(P) ≤ c·log₂ n!`, bites at **every** `n` for **every** `c < 1`. There is no crossover.
`n log₂ n` exceeds `log₂ n!` by `1.4427·n` — *linear in `n`*, against a saving that is a constant
fraction of `n log₂ n` — so any shape-A saving must first pay back a linear term, and paying it
back costs `log₂ n > log₂(e)/(1−c)`. **That is the entire content of `compression2`'s
`1.7 × 10⁷`: arithmetic about two reference scales, not a fact about its merge tree.**

So the question to put to a proposal is one line, and it is **not** *"what is your constant"*:

> **Does the code's expected length beat `⌈log₂ n!⌉` — the code that indexes `L` into all of
> `S_n` and ignores `P` entirely — at the `n` you claim it?**

**And a code answers that by construction, since it *is* a code: run it.** No asymptotic constant
needs proving to find out. The cheap test the ticket asked for is **cheaper than the ticket
supposed** — the crossover computation is only needed for bounds already stated asymptotically.

## 4. RECOMMENDATION TO `pm-onethird`

1. **CLOSE the arbitrary-subset class as a source of leverage.** Not because its separators are
   unconsumable one by one, but because **its separation is not the kind of thing that could make
   anything consumable**. The class bundles two unrelated properties under one vocabulary. The
   demonstrated 12-against-0 should stop being cited as an asset toward a bound; `mg-8b32` b2.3
   is correct and it measures the coordinate that does not carry.
2. **KEEP the prefix-code direction — and strip the subset framing off it.** Daniel's §1 —
   *"a code's output on a set `S` reads `S`, so it is not a function of `P`"* — is true and is
   **the wrong half**: the reading that bounds `log₂ e(P)` is the one at `S = L(P)`, and that one
   **is** a function of `P`. The correct warrant is simpler and stronger: **both of today's
   closures are about SEPARATION, and a code neither separates nor needs to.** Neither reaches it.
3. **GATE it on the one-line test in §3, run before any bound is proved.**
4. **The F24-multiplier branch is NOT addressed here.** Its third axis is still unnamed. §1
   **scopes** it rather than closing it — a multiplier is a `Φ|_LL` object, on the consumable
   side — and it faces the same two-question screen.
5. **The prior stands.** Three exact closures now, none usable. Assume a code will be vacuous
   unless shown otherwise. The first move is a **run**, not a theorem: build the `L*` code and
   measure its expected length against `⌈log₂ n!⌉` at `n = 6…12`.

All five carried by **`mg-9d9e`**.

## 5. Scope, and what this does NOT establish

- ⚠️ **NOT that no consumable construction exists.** The dichotomy says separation cannot *help*.
  It does not say `Φ|_LL` cannot bound `e(P)` — and prefix codes on `L(P)` are exactly such a
  `Φ|_LL`.
- ⚠️ **NOT that a shape-B bound is achievable.** `s2.5` cites `mg-0fc6` a3.1's five points
  (`0.907 … 0.883`, `n = 3…7`, decreasing) as an **existence** statement about the sharpest
  constant on the information set. Five points do not settle a limit and no code achieving them
  is exhibited. `mg-0fc6` a3.2's caution stands the other way: the two-atom law has `H = 0.9183`
  bits at *every* `n` with simultaneously maximal `E[inv_e]`, so an entropy bound does not
  deliver an inversion bound.
- ⚠️ **Nothing above `n = 5`** for the poset sweeps. What carries above is the one-line argument
  in §0; the tables are corroboration and are not the warrant.
- **A rounding, recorded not repaired.** `OneThird-Compression2-Scope-mg-0fc6.md:113`'s row
  header names `0.9399·n log₂ n`; its code computes `1 − 1/(24 ln 2) = 0.9398877`. The crossovers
  differ by **57,186**. `mg-0fc6`'s number is correct for its own constant — this is a rounding
  in prose, and it is on record here only because the elasticity makes four printed digits of `c`
  insufficient to pin `n*`. `s0.6` went red on it before it went green.
