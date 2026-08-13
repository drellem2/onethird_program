# `ε_spec` AT THE BOUNDARY `δ(P) = 1/3` — THE DISTRIBUTION, THE TREND, AND THE REALIZABILITY GAP MEASURED

`mg-6ff4`, 2026-08-13, filed by `pm-onethird` off Daniel asking where the real constant actually
sits. Instrument: [`code/boundary_epsilon_6ff4/`](../code/boundary_epsilon_6ff4/) — five arms,
standard library only, exact rationals on every verdict path, no float and no solver anywhere a
number is compared.

---

> ## THE VERDICT
>
> **The boundary class is not a population with a distribution. It is ONE POSET, ordinally summed
> with itself and with singletons, and its `ε_spec` is a closed form: `4k/(n²−1)` where `k` is how
> many copies of the 3-element `V` the poset contains.** Exhaustive over **every isomorphism class
> to `n = 9`** — 183 230 posets at `n = 9` alone — and the boundary population there is **49 posets
> total across `n = 3…9`**, every one of them an ordinal sum of singletons and copies of
> `V = (a < b, c free)`, and **exactly one of the 49 is primitive: the `V` itself, at `n = 3`.**
>
> **THE TREND FALLS, AND IT FALLS AT THE RATE THE WHOLE QUESTION TURNS ON.** `max_P ε_obs =
> 4⌊n/3⌋/(n²−1) ~ 4/(3n)` — `1/2` at `n = 3` down to `3/20` at `n = 9`, and to `16/143 ≈ 0.112` at
> `n = 12` under a width-`≤2` restriction. It is **not** monotone: it
> sawtooths upward at every `n` divisible by 3 (`1/6` at `n = 5` up to `8/35` at `n = 6`), and any
> reading of it as a clean decreasing sequence is wrong. The **envelope** falls like `1/n`.
>
> **THE REALIZABILITY GAP, MEASURED.** The pair-marginal supremum `n/(n+1)` is attained by the
> two-atom law, which is not a poset. The worst actual poset at the boundary sits a factor of
> **at least `3(n−1)/4`** below it — exactly that when `3 | n`, larger otherwise: `1.5×` at
> `n = 3`, **`6×` at `n = 9`**, and growing **linearly in `n` without bound**. ⚠️ **The honest unit is the RATIO, not the difference.** The difference
> `n/(n+1) − max_P ε_obs` merely saturates at `1` and makes realizability look like it buys a
> constant. It buys a factor that grows.
>
> **`e` IS CANONICAL HERE, AND NOT FOR THE REASON THE CORPUS USUALLY GIVES.** The strict `> 2/3`
> tournament — the one the no-3-cycle argument actually proves acyclic — orients **0 of 82**
> incomparable pairs on this class: at `δ = 1/3` **every** pair sits at exactly `2/3`, so the usual
> argument gives nothing at all. What rescues `e` is a different and weaker argument (§6): a weak
> 3-cycle forces all three pairs to `2/3` exactly, a comparable pair has probability `1` and
> `1 + 2/3 + 2/3 > 2`, so a cycle needs a **3-element antichain** — and the boundary class has
> **none**. `e` is unique at all 31 members at `n ≤ 8` and no tie-break is ever exercised. **This
> matters: `ε` at the worst alternative reference order is up to `1/2` higher — more than the whole
> measured value.**
>
> ⚠️ **AND NONE OF IT IS A FROZEN-CLASS NUMBER.** `δ = 1/3` is **outside** the frozen hypothesis,
> which is **strict**. The frozen class is empty at every `n` reached, here as everywhere. What
> these numbers support is a **trend argument** and a **measured lower bound on what realizability
> buys**. Quoted as the constant, they would be `STATE.md` row 3b's `0/132` in a new index.

---

## §1. What was measured, and on what

    ε_obs(P)  =  6 · E[inv_e] / (n² − 1)          (`ε_spec`, Op-Form:437 / STATE.md:15)

over the **boundary class** `δ(P) = 1/3` **exactly** — every incomparable pair `≥ 2/3`-decided and
at least one exactly `2/3`-decided — against the two constants that bracket the question: the
proven pair-marginal supply `ε_sup < 1` (`mg-6bc2` Claim 3.1: `= n/(n+1)`, attained) and the demand
`ε_dem ≈ 2·10⁻²`.

**Why the boundary and not the class the question is about.** The frozen class `δ(P) < 1/3` is
**empty at every `n` any enumerator reaches** — `δ < 1/3` *is* the counterexample condition and the
conjecture is verified through order 11 refereed / order 14 unrefereed (`mg-33f5`). `c1` prints the
`0` with that reason attached, exactly as `mg-7c78`'s `a5` does, so it cannot be re-quoted as a
clean sweep.

**The one identity the instrument is built on**, and why no arm has to enumerate `L(P)`:

> `e` orients every incomparable pair toward its `≥ 2/3` side, so
> `Pr[σ disagrees with e on {x,y}] = min(p_xy, 1−p_xy)`, and by linearity
> **`E[inv_e] = Σ_{x∥y} min(p_xy, 1−p_xy) = m·q̄`.**

`c0` T3 checks it against brute-force enumeration of `L(P)` rather than trusting it, and — the part
worth reading — **checks it OUT of scope too**: applied to posets where the `≥ 2/3` tournament is
not total, the same shortcut is **WRONG at 192 of 388** posets at `n ≤ 6`. The shortcut is
co-extensive with the boundary/frozen condition itself. Every arm applies it only inside its scope.

---

## §2. The census, exhaustive to `n = 9`

`c1` `m1`. Every isomorphism class, `n = 2…9`. Posets with no incomparable pair (chains) are
excluded because `δ` is undefined on them.

| `n` | posets | min `δ` | `δ = 1/3` | `δ < 1/3` (**FROZEN**) |
|---|---|---|---|---|
| 2 | 1 | `1/2` | 0 | **0** |
| 3 | 4 | `1/3` | 1 | **0** |
| 4 | 15 | `1/3` | 2 | **0** |
| 5 | 62 | `1/3` | 3 | **0** |
| 6 | 317 | `1/3` | 5 | **0** |
| 7 | 2 044 | `1/3` | 8 | **0** |
| 8 | 16 998 | `1/3` | 12 | **0** |
| **9** | **183 230** | **`1/3`** | **18** | **0** |

`n ≤ 8` reproduces `mg-7c78` `a5` exactly (`c0` T2, independent code, four columns per row).
**`n = 9` is new here.**

⚠️ **The last column is empty by construction and carries no information.** It is printed for the
reason `a5` printed it.

---

## §3. The structure — the boundary class is one poset, repeated

`c1` `m4`, and it is the finding everything else follows from.

**Every one of the 49 boundary posets at `n = 3…9` is an ordinal sum of singletons and copies of the
3-element `V`** (`a < b`, `c` incomparable to both), with at least one copy. **Zero exceptions.**

Why that collapses the whole question. `L(A ⊕ B) = L(A) × L(B)` and every incomparable pair lies
inside one summand, so

- `δ(A ⊕ B) = max(δ(A), δ(B))` — `δ` is a **max** over the primitive summands;
- `E[inv_e](A ⊕ B) = E[inv_e](A) + E[inv_e](B)` — `E[inv_e]` is **additive** over them.

(Both checked directly on 305 explicit ordinal sums, `c0` T5, rather than assumed.) So **the entire
boundary class is determined by the PRIMITIVE posets with `δ ≤ 1/3`**, and exhaustively to `n = 9`
there is exactly **one**: the `V`, with `L = {acb, abc, cab}`, `e = (a, c, b)`, `E[inv_e] = 2/3`,
`ε = 1/2` (`c0` T4, by hand).

Consequently, for a boundary poset with `k ≥ 1` copies of `V` on `n` elements:

| quantity | value | |
|---|---|---|
| incomparable pairs `m` | `2k` | |
| density `d = m/C(n,2)` | `4k/(n(n−1))` | `Θ(1/n)` at the maximiser |
| mean bias `q̄` | **`1/3` exactly** | pinned at the cap, at **every** member |
| `E[inv_e]` | `2k/3` | |
| **`ε_obs`** | **`4k/(n²−1)`** | verified at every one of the 49 |
| class size at `n` | `Σ_{k≥1} C(n−2k, k)` | `1, 2, 3, 5, 8, 12, 18` — measured exactly |

⚠️ **`ε_obs` does not depend on WHERE the copies sit**, only on how many there are. So "the poset
attaining the max" is not a single poset: at each `n` it is every arrangement with `k = ⌊n/3⌋`, and
`c1` `m3` prints one representative per `n`.

⚠️ **48 of the 49 are ORDINAL SUMS. Exactly one is primitive, and a minimal counterexample is
primitive** (`STATE.md:55`). **That is the scope limit of every figure in this document and it
travels with them.**

---

## §4. The distribution and the trend

`c1` `m3`. **Exhaustive over every isomorphism class, `n = 3…9`**; exact rationals; the population
of each row is the whole boundary class at that `n` and nothing is sampled.

| `n` | count | min `ε` | median `ε` | max `ε` | max (dec) | max/`ε_dem` |
|---|---|---|---|---|---|---|
| 3 | 1 | `1/2` | `1/2` | `1/2` | 0.500000 | 25.0 |
| 4 | 2 | `4/15` | `4/15` | `4/15` | 0.266667 | 13.3 |
| 5 | 3 | `1/6` | `1/6` | `1/6` | 0.166667 | 8.3 |
| 6 | 5 | `4/35` | `4/35` | `8/35` | 0.228571 | 11.4 |
| 7 | 8 | `1/12` | `1/12` | `1/6` | 0.166667 | 8.3 |
| 8 | 12 | `4/63` | `2/21` | `8/63` | 0.126984 | 6.3 |
| **9** | **18** | **`1/20`** | **`1/10`** | **`3/20`** | **0.150000** | **7.5** |

**The trend is FALLING, and it is NOT monotone.** `max_P ε_obs = 4⌊n/3⌋/(n²−1)` sawtooths: it jumps
**up** at every `n ≡ 0 (mod 3)`, where a new copy of `V` becomes affordable — `1/6` at `n = 5` to
`8/35` at `n = 6`, `8/63` at `n = 8` to `3/20` at `n = 9`. `c1` prints
`strictly FALLING at every step: False`, and this correction is against **my own filed prediction**
(§8, P4). The **envelope** is `~ 4/(3n)`; the **minimum** `4/(n²−1)` falls monotonically like `1/n²`.

**Against the two bracketing constants.** At every `n` measured, the boundary maximum is far below
the supply `ε_sup` and still **above** the demand `ε_dem ≈ 2·10⁻²` — by `25×` at `n = 3` and `7.5×`
at `n = 9`.

**Where it would cross, and this is EXTRAPOLATION and is labelled as such** (`c3` `m4`): continuing
`4⌊n/3⌋/(n²−1)`, the boundary maximum first falls to or below `ε_dem = 1/50` at **`n = 65`** — and
then **comes back above it at `n = 66`** (`88/4355 ≈ 2.021·10⁻²`), because of the same `mod 3`
sawtooth. It is below the demand **for good only from `n = 67`**. ⚠️ **"First crossing" and "last `n`
above" are different numbers here and only the second means anything**; reporting the first alone
would have published a monotone reading of a non-monotone sequence. Both assume no new primitive
poset with `δ ≤ 1/3` exists at any `n`, which is exactly what nothing here checks above its range.
**It is a consequence of a closed form, not a measurement.**

**What the trend argument is, stated so it can be attacked.** A falling trend across the boundary is
evidence that the interior — if it were ever non-empty — would sit far below the demand, because the
boundary is the *most* inversion-rich place the `δ ≤ 1/3` condition permits at each `n` and it is
already falling like `1/n`. The counter-reading is available and is not refuted here: the boundary
falls because it is populated by ordinal sums, and a minimal counterexample is **primitive**, so the
population driving the trend is disjoint from the population the conjecture is about, save for one
3-element poset.

### §4.1 Reach beyond `n = 9`, and what it is bought with

`c2`. Past the exhaustive range the population is **restricted by width**, and the restriction is
named at every row. The prune is sound and complete for its class: width is monotone under induced
subposets, so deleting a maximal element cannot raise it and the generator reaches every poset of
that width.

| population | reach | classes swept at the top `n` | boundary posets | new primitives with `δ ≤ 1/3` | `ε = 4k/(n²−1)` |
|---|---|---|---|---|---|
| **every isomorphism class** (`c1`) | `n ≤ 9` | 183 230 | 49 | **0** | holds at all 49 |
| width `≤ 3`, exhaustive (`c2` `m1`) | `n ≤ 10` | 397 221 | 76 | **0** | holds at all 76 |
| width `≤ 2`, exhaustive (`c2` `m2`) | `n ≤ 12` | 91 140 | 175 | **0** | holds at all 175 |

The class counts continue to match `Σ_{k≥1} C(n−2k, k)` exactly at every `n` reached: **27, 40, 59**
at `n = 10, 11, 12`. The maxima are `4/33`, `1/10`, `16/143` — `k = ⌊n/3⌋` is `3, 3, 4`, so `n = 11`
is the sawtooth's flat stretch and `n = 12` is its next jump. **The frozen count is `0` in every
restricted population too**, for the reason it is `0` everywhere.

⚠️ **A width-`≤3` sweep that finds nothing is silent about width `≥ 4`.** That is `mg-c47a`'s
width-`≥4`, `n ≥ 10` residual, **DROPPED** on tractability grounds (`STATE.md` attempt index), and
this arm inherits the gap unchanged rather than reopening it.

---

## §5. The realizability gap, measured rather than argued

`c3` `m1`–`m2`. The ticket's item 3.

`mg-6bc2` Claim 3.1: `max{ 6E_μ[inv_e]/(n²−1) : μ ∈ M_n(0) } = n/(n+1)`, **attained** by the
two-atom law `μ = (2/3)δ_e + (1/3)δ_{rev e}`, a measure on **2 of `n!`** orders. `c0` T6 rebuilds it
explicitly and confirms the value at `n = 3…9`, so the gap below is a gap against an object that
**exists** and is simply not a poset's `L(P)`.

**Population: every isomorphism class, `n = 3…9`, exhaustive.** The right-hand column is the one
that scales.

| `n` | sup `= n/(n+1)` | worst real poset at the boundary | difference | **ratio** |
|---|---|---|---|---|
| 3 | `3/4` | `1/2` | `1/4` | **1.500** |
| 4 | `4/5` | `4/15` | `8/15` | **3.000** |
| 5 | `5/6` | `1/6` | `2/3` | **5.000** |
| 6 | `6/7` | `8/35` | `22/35` | **3.750** |
| 7 | `7/8` | `1/6` | `17/24` | **5.250** |
| 8 | `8/9` | `8/63` | `16/21` | **7.000** |
| **9** | **`9/10`** | **`3/20`** | **`3/4`** | **6.000** |

**The ratio is `3(n−1)/4` wherever `3 | n`, and larger elsewhere.** Substituting the closed form:
`(n/(n+1)) ÷ (4⌊n/3⌋/(n²−1)) = n(n−1)/(4⌊n/3⌋) → 3(n−1)/4`.

> **THE NUMBER.** Realizability does not buy a constant. **It buys a factor that grows linearly in
> `n`**, and at the largest exhaustively-enumerated `n` that factor is **6**. The difference column
> is the misleading one: it saturates at `1` and invites the reading that the whole gap is bounded.

**Which of `mg-6bc2`'s two levers carries it** (`c3` `m3`, the identity `ε_spec = 3·d·q̄·n/(n+1)`
verified at all 49 members): **`q̄ = 1/3` exactly at every boundary poset** — pinned at the cap, the
same thing `mg-6bc2` §3.1 reports at its LP optimisers, now measured on **real posets**. The entire
fall lives in the **density `d`**. So the operative lever is residual **`(R)`**, the *number* of
incomparable pairs, and this is that statement measured rather than derived from an optimum.

---

## §6. How `e` was chosen — the ticket's item 4, and it is not a formality

`c4`. The ticket is right that this could dominate the measurement: `λ_std` moves by up to `1/3`
across reference orders (`STATE.md` glossary, `mg-c4f5`) and `ε_spec` is a functional of the same
choice. Measured, at `n = 3…8`, all 31 boundary posets, 82 incomparable pairs:

**`m1` — THE STRICT ARGUMENT GIVES NOTHING HERE.** The `> 2/3` tournament — the one the no-3-cycle
argument proves acyclic — orients **0 of 82 pairs**, at **0 of 31** posets. At `δ = 1/3` on this
class *every* incomparable pair sits at **exactly** `2/3` (which is `q̄ = 1/3` exactly, §3, seen from
the other side). The argument usually quoted for why `e` exists is **completely vacuous on the
boundary class.** ⚠️ This is not a defect in the argument; it is precisely the strictness the
boundary gives up, and it is the same sensitivity `FACTS.md` F18's last rider records for a
different statement.

**`m2` — THE WEAK ARGUMENT RESCUES IT, AND IT IS A DIFFERENT ARGUMENT.** The `≥ 2/3` relation is a
**complete** tournament on the boundary (by definition of `δ = 1/3`), it is **acyclic at all 31**,
and the topological order is **forced at every step** — so `e` is **unique**. **No tie-break is ever
exercised, and none is implemented**, so no tie-break policy can be blamed for any figure here.

**`m5` — WHY it held, and this is a proof with a measured hypothesis:**

1. A weak 3-cycle `x→y→z→x` needs all three cyclic probabilities `≥ 2/3`; they sum to `≤ 2`; so all
   three are **exactly** `2/3`.
2. A pair comparable in `P` has probability `1`, and `1 + 2/3 + 2/3 = 7/3 > 2`. So a cycle cannot
   contain a comparable pair — all three pairs are incomparable, i.e. `{x,y,z}` is a **3-element
   antichain**.
3. **No 3-element antichain ⟹ the weak tournament is acyclic and `e` is unique.**

The boundary class contains **0** three-element antichains at all 31 members (it has width 2 —
`FACTS.md` F19). ⚠️ **The implication is a proof; its hypothesis is a MEASUREMENT of this class, not
a theorem about it.** Separately, a search over **every** poset at `n = 3…8` for a 3-antichain with
all three cyclic probabilities `≥ 2/3` finds **0** — the configuration is not realized anywhere in
that range either, which is again a measurement.

**`m3` — `e` is a linear extension of `P` at all 31**, so `inv_e` over incomparable pairs equals
`inv_e` over all pairs. That is the step `mg-c4f5`'s audit calls *"unstated-but-true"*; here it is
stated and checked.

**`m4` — WHAT THE CHOICE IS WORTH, so `m2` is not filed as a formality.** Recomputing `ε` against
every linear extension of `P` as reference, and against all `n!` total orders at `n ≤ 7`:

| `n` | poset | `ε` at `e` | max over `L(P)` | max over `n!` |
|---|---|---|---|---|
| 3 | `V` | `1/2` | `3/4` | **`1`** |
| 4 | `V ⊕ 1` | `4/15` | `2/5` | `8/15` |
| 6 | `V ⊕ V` | `8/35` | `12/35` | `16/35` |
| 7 | `V ⊕ V ⊕ 1` | `1/6` | `1/4` | `1/3` |

**Widest gap between `ε` at `e` and `ε` at the worst reference order: `1/2`** — at `n = 3`, where
the measured value *is* `1/2`. **The choice of `e` is worth as much as, or more than, the entire
quantity being measured.** Without `m2`, `ε_obs` at the boundary would be a range and not a number.

---

## §7. What these numbers do and do not license

**THEY DO:**

- **A trend argument.** The maximum of `ε_spec` over the closest-to-frozen posets that exist falls
  like `4/(3n)` (with a `mod 3` sawtooth), exhaustively verified to `n = 9` and, under a width
  restriction, beyond (`c2`).
- **A measured lower bound on what realizability buys**, in the honest unit: a factor `3(n−1)/4`,
  `= 6` at `n = 9`, growing without bound. As far as this corpus records, that number had not been
  computed. It is a **lower** bound on the gap in the sense that the boundary is the most
  inversion-rich `δ ≤ 1/3` population available; it says nothing about a class that is empty.
- **A correction to how `e`'s canonicity is justified at the boundary** (§6): the usual argument
  orients `0 of 82` pairs.

**THEY DO NOT:**

- ⚠️ **Measure the frozen class.** `δ = 1/3` is **outside** the hypothesis, which is **strict**. The
  frozen class is empty at every `n` reached. **No number in this document is a frozen-class number
  and none may be quoted as one.** That is `STATE.md` row 3b's `0/132` error, and this programme has
  paid for it once.
- **Bear on a minimal counterexample except through one 3-element poset.** A minimal counterexample
  is **primitive**; **48 of the 49** boundary posets are ordinal sums. The population that produces
  the falling trend is almost disjoint from the population the conjecture concerns.
- **Settle `ε_dem`.** The boundary maximum is *above* the demand at every `n` measured (`7.5×` at
  `n = 9`) and falls below it only under extrapolation, at `n = 67`. Read as "the demand is
  comfortable", that would be the extrapolation quoted as a measurement.
- **Say anything about width `≥ 4` at `n ≥ 10`.** `c2` buys reach with a width restriction and
  inherits `mg-c47a`'s **DROPPED** residual unchanged (`STATE.md` attempt index).

**The single object that would kill all of it**: a **new primitive poset with `δ ≤ 1/3`** at some
`n ≥ 10`. Everything in §§3–5 is the ordinal-sum algebra applied to the one primitive member that
exists; a second one moves every number. `c1` (exhaustive to `n = 9`) and `c2` (width-restricted
above it) are exactly the search for that object, and both come back empty over the range they
cover — which is a range, not a proof.

---

## §8. Predictions scored

[`code/boundary_epsilon_6ff4/PREDICTIONS.md`](../code/boundary_epsilon_6ff4/PREDICTIONS.md), filed
before any code existed, with the exposure disclosed rather than laundered — **P1–P5 were declared
REPORTS at zero credit at filing time**, because the closed form was derived on paper and already
matched `mg-7c78`'s published census before a line was written.

| # | outcome |
|---|---|
| P1, P2, P3, P5 | **HELD** — and were reports when filed, so they earn nothing |
| **P4** | **HELD IN DIRECTION, REFUTED IN FORM.** The trend falls, but it is **not** monotone: it sawtooths up at every `n ≡ 0 (mod 3)`. My prediction said `Θ(1/n)` "falling" without qualification; `c1` prints `strictly FALLING at every step: False`. |
| **P6** | **FORMULA HELD, MY ARITHMETIC WRONG.** I predicted the `n = 9` count as `C(7,1) + C(5,2) = 17`, dropping the `k = 3` term `C(3,3) = 1`. The measured count is **18**, and the formula `Σ_k C(n−2k, k)` — which I also filed — gives 18. **The live half (no new primitive at `n = 9`) HELD; the number I wrote down was wrong by one and the error was mine, not the formula's.** |
| P7 | **HELD** — ratio `3(n−1)/4`, difference saturating at `1`, measured |
| **P8** | **HELD, AND THE SECOND HALF UNDERSTATED IT.** I predicted the strict tournament would not be total. It orients **0 of 82** pairs — not "not total", but **empty**. |
| P9 | **HELD** — widest gap `1/2`, i.e. `100%` of the measured value at `n = 3` |
| **P10** | **HELD** — `q̄ = 1/3` exactly at every member. (The prediction file contains a visible false start mid-sentence; it was left in rather than tidied, because a prediction file edited after the measurement is worth nothing.) |
| P11 | **HELD** — identity verified at all 49; `d` carries the entire fall |
| P12, P13 | **HELD** over the ranges `c2` reaches, and those ranges are stated at every table |

---

## §9. What this document does not do

- **It does not measure the frozen class**, and no arm could. §7 says so in the terms the ticket
  asked for.
- **It does not prove the structure theorem.** "The `V` is the only primitive poset with
  `δ ≤ 1/3`" is `FP` at `n ≤ 9` exhaustive and `FP` under a width restriction above that. It is not
  a theorem, it is not claimed as one, and everything downstream of it inherits that kind.
- **It does not reopen `mg-c47a`'s width-`≥4` residual.** That was DROPPED on tractability grounds
  and `c2` inherits the gap.
- **It ran no eigenvalue, no float, and no solver on any verdict path.**
- **It proposes no consumer.** What `STATE.md:21` needs is a realizability fact bounding `d` **under
  the frozen hypothesis**; what this measures is `d` **at the boundary**, where the hypothesis does
  not hold. Those are different statements and this document does not bridge them.
