# Does `mg-9b6b`'s test kill `(B-cov)` and `(EQ)`? — **NEITHER. IT CANNOT RETURN AN ANSWER ON THEM, AND WHAT IS MISSING IS A THEOREM RATHER THAN A SWEEP**

`mg-5987`, 2026-08-13, `mg-9b6b`'s named successor and the first arc to price a residual that is
not `(R)`. Instrument: [`code/lever_test_5987/`](../code/lever_test_5987/) — four arms, standard
library only, exact rationals on every verdict path, ~4 min, two consecutive runs byte-identical.
Predictions with the exposure disclosed per line, and two of them refuted in the direction that
mattered: [`code/lever_test_5987/PREDICTIONS.md`](../code/lever_test_5987/PREDICTIONS.md).

---

> ## THE VERDICT
>
> **`mg-9b6b`'s three-step test runs on `(B-cov)` and `(EQ)`. Step 1 bites on both, harder than it
> bit on `(R)`. Step 2 bites on both — and on every frozen-conditional object there will ever be,
> because it is a contraposition and not a test. Step 3 is where the answer should be, and it is
> the step that cannot be completed: its currency is a function of a theorem neither residual has.**
>
> **STEP 2 IS A TRIVIALITY AND THAT IS THE FIRST FINDING.** For any `Q` and any constant,
> `frozen ⟹ Q ≤ C` is `Q > C ⟹ δ ≥ 1/3`, i.e. **the conjecture restricted to `{Q > C}`**. So no
> statement of this shape ever escapes step 2, `(R)` was not special in kind, and the whole content
> is the **price** — the orders that restriction delivers.
>
> **THE PRICE IS A FUNCTION OF ONE NUMBER PER ORDER: the primitive floor**
> `floor_Q(n) = min{Q(P) : P primitive at order n}`, because `{Q > C}` covers order `n` exactly when
> `floor_Q(n) > C`. `mg-9b6b` could price `(R)` end to end because `floor_d(n) = 2/n` is a
> **theorem**. Neither of these two has one: the floors here are a **census that stops at `n = 8`**,
> every order of which is already verified, and **no further sweeping closes it** — `n = 12` is
> still inside the verified range. That is why the `unreached orders` column, `mg-9b6b`'s own
> currency, is empty for both and not merely small.
>
> **AND THE FLOOR'S DIRECTION IS THE OPPOSITE OF HOW IT READS.** `{d > D}` covers order `n` while
> `2/n > D` and **stops** at `n = 2/D` — so `(R)`'s **decaying** floor is what makes its price
> *finite* at 96 orders. A floor pinned at `Θ(1)` is never overtaken by a fixed setting, so below it
> the delivery has **no cutoff at all**. This document's first draft said the reverse and the table
> under it is what killed it.
>
> **WHAT THE CENSUS DOES SETTLE IS THE TWO ENDS OF EACH DIAL, AND THEY DISAGREE:**
>
> | | `(EQ)_C` — `max_x \|E[pos_σ x] − rank_e x\| ≤ C` | `(B-cov)_C` — `Σ_x C_x ≤ C·E[inv_e]` |
> |---|---|---|
> | delivers **0 orders at every `n`** | `C ≥ 2/5` | `C ≥ 4/5` |
> | delivers **every order `3…8`** | `C < 37/123 = 0.3008` | `C < 8/25 = 0.3200` |
>
> ⚠️ The lower thresholds are not the numbers an eye picks off the floor table: both minima sit at
> an **end** of the swept range and `(B-cov)`'s is at `n = 4`, neither floor being monotone in `n`.
>
> The upper row is a **theorem** — an explicit **primitive** family caps both floors at every `n`.
> `Z_n` (`x_i < x_j` iff `j − i ≥ 2`) has `L(Z_n)` in bijection with the matchings of a path, so
> `max_x |h − rank_e| = F_{n−1}/F_{n+1} → 1/φ²` and `Σ C_x/E[inv_e] → 1 − 1/√5`, with both caps
> following from one Fibonacci identity. ⚠️ **It is PRIMITIVE at every `n`**, so `mg-f5be`'s
> objection — which lapsed `mg-9b6b` §3's ordinal-sum refutation above `n = 3` — does not touch it.
>
> **AND THE FLIP SITS INSIDE THE WINDOW THE RECORD LEAVES UNPINNED.** The crossing is at
> `≈ 0.3 – 0.8`, i.e. **15× to 40× `ε_dem`**, against a required constant `STATE.md` records as
> *"genuinely small and unpinned by ~2 orders of magnitude"* (audit F5). **So *"is `(B-cov)` a
> lever?"* is not a question about `(B-cov)`.** It is a question about a constant nobody has
> computed end to end, and that is the first time an unpinned constant in this corpus decides
> whether a residual is a lever or the conjecture in disguise.
>
> **THE ORDERS COUNTER IS TOO COARSE HERE, MEASURED RATHER THAN ASSERTED.** It is binary per order.
> At `C = 2/5` it says `(EQ)` delivers **nothing**; the coverage says `(EQ)` settles **99.8%** of the
> primitives at `n = 8` — **31 posets of 12 524** carry the entire difference between *zero price*
> and *the whole order*. Both numbers are true and only one is informative, so every price in this
> arc is reported with its coverage beside it.
>
> ⚠️ **NOTHING HERE IS A MEASUREMENT ON THE FROZEN CLASS.** It is empty at every `n ≤ 7`,
> re-established on this instrument's own population. That emptiness is the subject, not a caveat.

---

## §1. The question, and what `mg-9b6b` handed over

`mg-9b6b` closed `(R)` as a lever and said in its own §8 that it had answered `mg-3da1`'s *"what
remains as a lever at all"* **for the density route only** — *"No arc was opened on `(B-cov)` or
`(EQ)`"* — and in §6 it named the shape of an escape: *an object whose hypothesis is not `frozen`
and whose conclusion is not a restriction of the target.* `STATE.md`'s residual list has two
entries it never touched:

- **`(B-cov)`** — *"break the wrong-signed same-side covariance"*, `C_x = Σ_{y≠z} Cov(s_xy, s_xz)`,
  the term of `E[Σ disp²]` that FKG/XYZ force `≥ 0`, and the object three separate routes converge
  on;
- **`(EQ)`** — `max_x |E[pos_σ x] − rank_e x| = O(1)`, elementary, and *"the only one of the three
  that is a cancellation statement rather than a decay statement"*.

Both are frozen-conditional, so step 1 applies to both at once and the interesting outcome is at
steps 2 and 3. This arc runs all three.

## §2. Step 1 — the hypothesis, and the half `(R)` did not have

The population is empty: **0 frozen classes at every `n ≤ 7`**, with one member of the weak class
`δ ≤ 1/3` at `n = 3` (the boundary poset, `δ = 1/3` exactly). Re-established here rather than
quoted, because a directory printing zeros over a class it did not check is printing zeros about
nothing. So far this is `(R)`'s position exactly.

**Two things then differ, and both cut against these two residuals.**

**(a) There is no unconditional reading, at any constant.** `(R)` has one — `docs/FACTS.md` F26
gives an unconditional density ceiling that owes nothing to the conjecture, and it is what
`mg-9b6b` priced as the dial's provable end. Asked of these two the answer is **NO at every
constant**, and it is a proof rather than a census: the **antichain** `A_n` has
`max_x |h − rank_e| = (n−1)/2` and `Σ C_x/E[inv_e] = (n−2)/3`, both unbounded, both closed form,
and `A_n` is **primitive** so the restriction to primitives does not rescue either. Neither dial
has a provable end at all.

**(b) The conclusions do not merely become false off the class — they stop referring.** Both name
`e`, and `STATE.md`'s glossary defines `e` as *"the >2/3-majority order all biases align with —
reference, not a choice"*, with the `λ_std` row already recording that *"frozen removes the
choice … that is a hypothesis, not a convention"*. Measured here: **`e` is fully decided at 1
primitive over all of `n ≤ 7`**, and the predicate *every incomparable pair `≥2/3`-decided* **is**
`δ(P) ≤ 1/3` at every member — so **the definedness of the notation and the emptiness of the class
are one fact, not two.** `d(P)` needs no reference order, which is why `mg-0b96` and `mg-9b6b`
could evaluate the `(1_D)` dial off-class without choosing anything.

**So the reading is priced rather than picked.** Every quantity here is evaluated at the
**barycentric** reference — sort by `h(x) = E[pos_σ x]`, always a linear extension because `x < y`
forces `h(x) < h(y)` — and two measurements justify it:

- the **envelope over all reference orders** at `n ≤ 6`: barycentric is the **argmin** of the bias
  at **224 of 224** primitives, and the **argmax** of `ρ` at **224 of 224**. ⚠️ **The favourable
  end is a different end for the two objects** — a lower floor delivers fewer orders, and
  barycentric roughly minimises inversions, which are `(B-cov)`'s *denominator*. Each verdict below
  is therefore stated at the end that cannot flatter it;
- where `STATE.md`'s own `e` exists at all, **it is the barycentric order** — **33 of 33** across
  `β = 1/3` and the relaxed `β = 2/5`, where the class is not empty.

## §3. Step 2 — it is a contraposition, not a test

```
frozen(P) ⟹ Q(P) ≤ C        is        Q(P) > C ⟹ ¬frozen(P) ⟹ δ(P) ≥ 1/3
                                       ─────────────────────────────────────
                                       the conjecture, restricted to {Q > C}
```

Contraposition is an equivalence, so **every** frozen-conditional statement is the conjecture
restricted to the complement of its conclusion. Step 2 never returns NO on this kind of object.
`(R)` was not special in kind; it was special in **price**, and the price is one number per order:

| `n` | primitives | `floor` of `max_x \|h − rank_e\|` | `floor` of `Σ C_x/E[inv_e]` | `floor` of `d` |
|---|---|---|---|---|
| 3 | 2 | `1/3` | `1/3` | `2/3` |
| 4 | 7 | `2/5` | `8/25` | `1/2` |
| 5 | 31 | `4/11` | `2/5` | `2/5` |
| 6 | 184 | `4/13` | `2/5` | `1/3` |
| 7 | 1 351 | `4/13` | `176/399` | `2/7` |
| 8 | 12 524 | `37/123` | `140/319` | `1/4` |

The last column is the control: `floor_d(n) = 2/n` exactly, `mg-0b96`'s primitivity bound
reproduced from the census side. **It is a theorem and it decays**, and both properties are
load-bearing. The other two neither decay nor are theorems.

⚠️ **Over all non-chain classes the `(B-cov)` floor is `0` from `n = 4` on**, and that is not a
rival measurement — it is the ordinal sums, whose same-side covariance vanishes identically. Pricing
over that population would report *"delivers nothing"* for a reason that has nothing to do with
`(B-cov)`, which is exactly what `mg-f5be`'s primitivity objection exists to prevent. Every verdict
here is over the **primitives**.

**And the coverage refinement, which the orders counter cannot make.** The counter is binary per
order and returns `0` both for a statement that settles nothing and for one that settles every
primitive but one:

| dial `C` | `(EQ)_C` settles, `n = 5, 6, 7, 8` | `(B-cov)_C` settles, `n = 5, 6, 7, 8` |
|---|---|---|
| `1/50` | 100 · 100 · 100 · 100 % | 100 · 100 · 100 · 100 % |
| `2/5` | 90.3 · 97.3 · 99.4 · **99.8** % | 96.8 · 99.5 · 100 · 100 % |
| `1/2` | 80.6 · 89.7 · 96.5 · 98.5 % | 83.9 · 97.3 · 99.3 · 99.9 % |
| `4/5` | 48.4 · 59.8 · 73.6 · 80.0 % | 48.4 · 69.6 · 86.9 · 95.6 % |

At `C = 2/5` the counter says `(EQ)` delivers **nothing** and 31 posets of 12 524 are the whole
difference. The coverage also **rises with `n` at fixed `C`**, so the exceptional set is shrinking
as a fraction even though §4 shows it is never empty.

## §4. Step 3 — the dial, and the family that carries it past the census

`Z_n`: `x_i < x_j` iff `j − i ≥ 2`. The incomparable pairs are exactly the consecutive ones, so a
linear extension is the identity with a set of pairwise non-adjacent adjacent transpositions
applied — `L(Z_n)` is in bijection with the **matchings of a path**, and everything is closed form:

```
|L(Z_n)| = F_{n+1}        q_i = Pr[(i,i+1) transposed] = F_i·F_{n−i}/F_{n+1}
h(x_i) − i = q_i − q_{i−1}       C_{x_i} = 2·q_i·q_{i−1}       E[inv_e] = Σ q_i
```

so `max_x |h − rank_e| = q_1 = F_{n−1}/F_{n+1} → 1/φ² = 0.381966` and
`Σ C_x/E[inv_e] = 2Σ q_i q_{i−1}/Σ q_i → 1 − 1/√5 = 0.552786`. The caps hold **at every `n`** from
one identity, checked rather than cited:

```
F_{a+b−1} = F_a F_b + F_{a−1} F_{b−1}  ⟹  F_i F_{n−i} ≤ F_{n−1}  ⟹  q_i ≤ q_1
⟹  bias(Z_n) = q_1 ≤ 2/5     and     ρ(Z_n) ≤ 2 q_1 ≤ 4/5
```

**`C_{x_i} = 2 q_i q_{i−1} ≥ 0` derives `docs/FACTS.md` F11's sign rather than measuring it** — the
event *`(i,i+1)` transposed* implies *`(i−1,i)` untransposed*, so the covariance is `q_i q_{i−1}`.
F11 measured `C_x > 0` at 555 of 555 sampled rows; this is that sign with a reason attached, on a
family F11's population does not reach.

**The dial, in `mg-9b6b`'s own table shape:**

| residual | setting | delivers | unreached (`n > 14`) |
|---|---|---|---|
| `(R)` | F26 — **PROVEN** | nothing | 0 |
| `(R)` | `ε_dem·(n+1)/n` — row 8 | `n = 3…98` | **84** |
| `(R)` | F23's `4⌊n/3⌋/(n(n−1))` — the data | every `n ≥ 4` | all of them |
| `(EQ)` | `C ≥ 2/5` — the cap | **nothing, at every `n`** | 0, at every `n` |
| `(EQ)` | `C < 37/123` — below the floor | every `n = 3…8` | **NOT COMPUTABLE HERE** |
| `(B-cov)` | `C ≥ 4/5` — the cap | **nothing, at every `n`** | 0, at every `n` |
| `(B-cov)` | `C < 8/25` — below the floor | every `n = 3…8` | **NOT COMPUTABLE HERE** |

**The two `NOT COMPUTABLE` cells are the finding and not a gap in the sweep.** Unreached orders are
a function of the floor above `n = 14`; that floor is a theorem for `d` and an open question for
both of these; and no census closes it, because a sweep to `n = 12` is still inside the verified
range.

## §5. What would make the test return an answer

**A theorem about `floor_Q(n)` — the analogue of `d ≥ 2/n`.** Two shapes, answering opposite ways:

- **`floor_Q(n) ≥ c > 0` at every `n`.** Then every `C < c` delivers **every** order — the whole
  conjecture in one step, `mg-9b6b`'s data end — and the residual is dead at every setting below
  `c`, with no cutoff, which is **worse** than `(R)`.
- **`floor_Q(n) → 0`.** Then each fixed `C` has a cutoff and the price is finite and computable
  exactly as for `(R)`, and the unreached-order figure becomes something somebody can put in the
  table above.

The measured floors — `1/3, 2/5, 4/11, 4/13, 4/13, 37/123` for `(EQ)` — are consistent with both and
settle neither. They are **not monotone**, which is reported rather than smoothed, and the largest
is at `n = 4`.

## §6. Recommendation to `pm-onethird`

**Do not mark `(B-cov)` or `(EQ)` closed, and do not mark them clear.** The residual list is not
three closures and it is not two levers plus a closure. What it is, stated in the bullet rather
than in a rider 25 lines below — which is `mg-9b6b`'s own repair applied to its own successor — is:

> the two remaining residuals are **priced conditionally**: above an explicit constant their
> contrapositive delivers nothing at any order, below the measured floor it delivers every order a
> census can see, and **the architecture's required constant is not pinned well enough to say which
> side either is on**.

That is a different instruction to a fifth arc than either *"go and prove `(B-cov)`"* or *"`(B-cov)`
is the conjecture in disguise"*, and both of those instructions are currently derivable from the
record.

**`docs/FACTS.md` gets no entry.** Every measurement here is consumed by this landing, which fails
the registry's own homelessness test — `mg-3da1`'s reason, applied a third time.

**`docs/CONCEPTS.md` gets no row.** The conceptual content — *a frozen-conditional statement is the
conjecture restricted, and its price is set by the primitive floor of its conclusion* — is one line
and it belongs to the successor that proves a floor, not to the arc that found the floor missing.

## §7. Where this could be wrong

- **⚠️ THE OPERATIVE FORM OF `(B-cov)` IS A READING, AND IT IS THIS ARC'S.** `STATE.md` states the
  residual in words — *"break the wrong-signed same-side covariance"* — and the quantitative form
  priced here, `Σ_x C_x = O(E[inv_e])`, is read off `mg-dcae`'s variance/bias split as the attempt
  index records it (`(B) ⟺ (B-cov) + (B-bias) = O(E[inv])`) together with F11's `C_x`. `(EQ)` needs
  no such reading — `STATE.md` states it as a formula. If the intended form of `(B-cov)` carries a
  different normalisation, its floor moves and its half of the dial moves with it; the `(EQ)` half
  and every structural finding are untouched.
- **The `n = 8` sweep is primitives only.** No number here is claimed for the `n = 8` non-chain
  population.
- **`(R)`'s column is computed through `lib9b6b`**, the library that published it. Consistency, not
  corroboration; a disagreement would impeach this directory first.
- **`ρ(Z_n) ≤ 4/5` is the provable cap; the measured sup over `n ≤ 399` is `0.5509` and the limit is
  `1 − 1/√5`.** The gap between the provable cap and the true one is not closed here, and `g3`
  prints both rather than the prettier one.
- **F11's sign is reproduced, not independently corroborated** — `p_before` is shared with the
  library F11 was measured through. What is independent is the population and the closed form.
- **Nothing here shows either residual is false.** Both are true if the conjecture is.
- **The verdict is about the TEST, not about the mathematics of either residual.** *"`mg-9b6b`'s
  test cannot price it"* is not *"it cannot be priced"*; a floor theorem prices it immediately.
- **Per `STATE.md`'s standing rule**, every aggregate sentence about this arc's census results is
  `FP`; only §3's contraposition and §4's family caps are `U`.

## §8. What was NOT done

- **Neither residual was attacked.** The question was the shape, not the truth.
- **The floor theorem was not proven.** It is §5's object and the successor's subject.
- **The architecture's required constant was not computed end to end.** That it is unpinned is
  `STATE.md`'s own record (audit F5); that the unpinning now decides a lever question is this
  arc's finding, and closing it is a separate ticket.
- **No ledger row was edited.** `(B-cov)` and `(EQ)` are residuals in *Where the threads converge*,
  not ledger rows, so no twin re-pin is owed.

## §9. Provenance

Instrument [`code/lever_test_5987/`](../code/lever_test_5987/), four arms, `sh run_all.sh`, worst
exit 0, two consecutive runs byte-identical, ~4 min. `lib6ff4` supplies enumeration, `count_ext`,
`p_before` and the canonical form; `lib0b96` supplies `ε_dem` and `density`; `lib9b6b` supplies the
`(R)` control column. Every imported primitive this arc's verdicts stand on is re-checked here —
against OEIS A000112, against brute-force enumeration of `L(P)` at all 405 classes `n ≤ 6`, and
against `mg-9b6b`'s own published 96/84 — because an import whose controls live in another
directory is unchecked from here. `g0` is 27 controls: both per-poset numbers computed twice by
routes sharing no line of code (order-ideal DP vs. full enumeration of `L(P)`), `mg-dcae`'s split
verified at two reference orders, three live planted defects, and **two candidates that came back
inert and are printed rather than swapped out** — one branch unreachable for a structural reason,
one for an imported invariant, the second checked in both directions. One wrong-direction control:
`e` is fully decided at 1 primitive over `n ≤ 7`, and at `β = 2/5`, where the class is **not** empty,
the same machinery returns 32 real reference orders and every one of them equals the barycentric
stand-in.
