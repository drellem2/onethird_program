# INDEPENDENT AUDIT of the `ε_spec` derivation (`mg-6bc2`)

**Work item.** `mg-832f` (repo `onethird_program`), pre-filed SAME ACTION on `mg-6bc2`.
**Instrument.** [`code/pairbias_audit_a832f/`](../code/pairbias_audit_a832f/) — `run_all.sh`, ~14 min.
No `numpy` on this machine, so the simplex is hand-written and every path is exact
`Fraction`; there is no float anywhere in this audit.
**Predictions** committed at `b9e6d19`, **before any script of this instrument existed and
before one line of `mg-6bc2`'s deliverable was read**, with **eight hand measurements
disclosed rather than laundered into predictions** and two most-likely errors filed as P15
and P16. Both fired. P16 caught Finding 10.

**PROVENANCE, as the dispatch requires.** I read `STATE.md` at **blob
`7f73bfc87b4bc4caab6c836f8c3922a2416863cf`**, the version landed by commit
**`491d42c79f7628c18cb7a5d197faa9f4600cd6c1`** (`mg-b488`). Verified two ways:
`git log -1 --format=%H -- STATE.md` on `origin/main` returns `491d42c`, and
`git rev-parse origin/main:STATE.md` equals `git rev-parse HEAD:STATE.md` equals
`7f73bfc8…`. **The file did not move under me.** I name the blob as well as the commit
because the commit is what can be re-pointed and the blob is what cannot.

---

## 0. Verdict

> ## **CONFIRMED. THE ALGEBRA IS RIGHT, THE `L4` GATE WAS RESPECTED, AND THE CONSTANT IS DERIVED — I RE-DERIVED CLAIM 3.1 BY HAND BEFORE OPENING THE PARENT AND GOT THE SAME THING, INCLUDING THE WITNESS.**
>
> Every one of the brief's six traps was checked and **four of them do not fire**: the
> constant is a derivation and not `mg-3ce3`'s calibration (point 4); the inequalities point
> the way they need to (point 5); the deliverable does **not** bend toward `1/6` — it lands
> on `1` in `ε_spec` units and says `1/6` there would be `6×` stronger (point 6); and the
> `L4` gate was cleared by its second disjunct, which I confirm **by construction** rather
> than by citing `mg-345e` (point 2).
>
> ### Four corrections, none of them to the mathematics
>
> 1. **The banner, not the body** (point 6, at the only place it fires). §0's headline
>    *"DANIEL'S CONJECTURE IS RIGHT, AND IT IS ALREADY PROVEN"* carries **no unit**, and it
>    is the sentence a grep returns. The body splits the readings in the next paragraph and
>    is right. This lineage has already recorded this exact failure mode once tonight
>    (`mg-94c3`: a conditional *"absent from the COMMIT SUBJECT, which is what the next agent
>    greps"*). **Never quote that banner without its next sentence.**
> 2. **`STATE.md` drops the parent's `η`, and that is where "ATTAINED" gets weaker.**
>    `mg-6bc2` states Claim 3.1 over `M_n(η) = {every pair ≤ 1/3 − η}` with maximum
>    `(1−3η)·n/(n+1)` — **correct, and it handles the strictness**. `STATE.md:15` and row 8
>    both restate it at `η = 0` and say **ATTAINED**. The `η = 0` witness has every pair at
>    **exactly** `1/3`, i.e. `δ = 1/3`, i.e. **NOT FROZEN**. The conclusion survives (the
>    supremum over `⋃_{η>0} M_n(η)` is still `n/(n+1)`), but the landing hands a reader
>    "attained" with a witness outside the hypothesis. **The parent is right here and the
>    landing is the weaker rendering** — which is the opposite of what I predicted (P3).
> 3. **§4's *"the two-atom law scores `1/2` in the footrule form"* is exact only at ODD `n`.**
>    The closed form is `⌊n²/2⌋/(n²−1)`: `1/2` at odd `n`, and `8/15, 18/35, 32/63, 50/99,
>    72/143` at even `n` — strictly **above** `1/2`, decreasing to it. Immaterial to the
>    argument (the comparison is `1/2` against `1`) but it is a printed number that does not
>    move, and this arc's standing rule is that printed numbers move.
> 4. **§3.1's *"either lever alone"* names two levers; on every realizable object I can
>    reach, only ONE of them moves.** At **every** boundary maximiser at **every** `n ≤ 7`,
>    `q̄ = 1/3` **exactly** — the mean flip probability is pinned at the cap, and the whole
>    variation is in the density `d`. So the operative lever is residual **(R)**, not `q̄`.
>
> ### Material beyond the brief — and it corrects both parents' *"Not done"* lists and mine
>
> **THE POSET SWEEP `mg-345e` AND `mg-6bc2` BOTH DECLARED AND REFUSED HAD ALREADY BEEN RUN,
> AND ITS OUTPUT IS COMMITTED IN THIS REPOSITORY.**
> [`code/libweak_c3ca/out_p2_primitive.txt`](../code/libweak_c3ca/out_p2_primitive.txt)
> enumerates exactly this population. I reproduce **every** figure in it on code sharing no
> line, in exact rationals, and extend it to `n = 7`. **Neither refusal mentions it exists.**
> **The reason it went unnoticed is a unit mismatch, for the THIRD time in this lineage**:
> `p2_primitive` reports `E_maj/n²`, which is `ε_c3ca`; the whole relaxation lineage reports
> `6E/(n²−1)`, which is `ε_spec`. **The ratio between the two sides — the number `mg-6bc2` §1
> says *"nobody has asked … which is a number"* — has never been formed anywhere.** It is
> formed here: **the price of dropping realizability is `Θ(n)`, not a constant.**
> *(CORRECTING MYSELF, because I first wrote this as "no file computes both" and that is
> false: [`code/libweak_audit_c4f5/a1_premise.py:51`](../code/libweak_audit_c4f5/a1_premise.py)
> computes `6E[inv]/(n²−1)` on every naturally-labelled poset to `n = 7`. It is a **near
> miss, not the thing** — it takes `inv` against the **natural labelling**, not the
> `≥2/3`-majority order `e`, it runs over the **whole** population rather than the `δ ≤ 1/3`
> class, and it is testing the master bound against `λ_std`, not comparing anything to
> `n/(n+1)`. The correct statement is the narrow one above, and I checked it by grepping
> every `*.py` in the repo for files that both enumerate posets and carry an `(n²−1)`.)*
>
> **AND THE EMPIRICAL CALIBRATION IS UNAVAILABLE FOR A REASON STRONGER THAN THE ONE BOTH
> PARENTS GAVE.** They refuse because the frozen class `δ < 1/3` is empty. True, and I
> reproduce it (`0` posets at every `n ≤ 7`). The stronger fact: **above `n = 3`, every poset
> with `δ ≤ 1/3` is an ORDINAL SUM** — `0` primitive at `n = 4,5,6,7` — so each has
> `λ_std = 1` and `1 − λ_std = 0`; and at the primitive minimum of `δ` (`2/5`, `4/11`,
> `5/14`, `14/39`) the `≥2/3`-majority tournament is **INCOMPLETE**, so **`e` does not exist
> and `inv_e` is undefined**. **There is no primitive poset in reach at which `ε_spec` is
> even DEFINED, above `n = 3`.** That is the reason the refusal should carry.
>
> ### Where it stops, with the obstruction named (brief point 3)
>
> I tried to build the forbidden object three ways and **failed all three, for a structural
> reason rather than a search failure.** `E[inv_e]` is a **sum over pairs** and the
> hypothesis caps each summand; **linearity of expectation is an EQUALITY**, so it can
> transmit the per-pair constant and nothing else. That leaves exactly two levers, and the
> candidate space is closed: **(a) the NUMBER of summands** — residual **(R)**, a
> frozen-conditional *upper* bound on `d`, of which the corpus has **zero** (every density
> fact on record runs the other way); **(b) a constraint no product of per-pair caps can
> express** — realizability. **The negative is not a gap in the argument. It is the argument
> being exact.**

---

## 1. What I did, in the order the brief demands

The brief orders the re-derivation **before** the parent's derivation is read. I obeyed it
literally. §1.1 is what I had on paper with `docs/…mg-6bc2.md` unopened; it is recorded in
`PREDICTIONS.md` at `b9e6d19` as H1–H8, **as results and not as predictions**, because
scoring a completed derivation as a prediction is laundering.

### 1.1 The re-derivation, from `STATE.md`'s statement of the premises

Frozen is `δ(P) < 1/3`: every incomparable pair is `>2/3`-decided toward `e`, so each is
flipped by `σ` with probability `< 1/3`. Then

> `E[inv_e] = Σ_{i ∥ j} Pr[{i,j} flipped]  <  m/3  ≤  (1/3)·C(n,2) = n(n−1)/6`

**The ingredient list is exactly three:** (i) the frozen hypothesis read per pair; (ii)
linearity of expectation; (iii) `m ≤ C(n,2)`. Divide by the two normalisations:

| divide by | get | limit |
|---|---|---|
| `n²` (`ε_c3ca`, [`mg-c3ca:172`](OneThird-LIBweak-mg-c3ca.md)) | `ε_c3ca < (n−1)/(6n)` | **`1/6`** |
| `(n²−1)/6` (`ε_spec`, row 8) | `ε_spec < n/(n+1)` | **`1`** |

`ε_spec/ε_c3ca = 6n²/(n²−1) → 6`. **`0` disagreements over 12 values of `n` up to 200**
(`out_a1_unitmap.txt` A1.1).

The `≥` direction: `μ* = (2/3+η)δ_e + (1/3−η)δ_{rev(e)}` puts every pair at flip probability
exactly `1/3 − η`, so `μ* ∈ M_n(η)` and `6E_{μ*}[inv_e]/(n²−1) = (1−3η)·n/(n+1)` exactly.
**Two permutations, no tableau — so the attainment is all-`n`, not finite-population.**
Checked `52/52` over `n ∈ {2,3,4,5,6,7,8,9,11,20,50,137,1000} × η ∈ {0, 1/100, 1/12, 1/6}`.

**This is the same two-atom law `STATE.md:135` already names as obstruction 4.** Claim 3.1's
`≥` is not new mathematics; it is the file's own standing counterexample re-pointed at the LP,
which is *why* it is airtight.

### 1.2 The comparison

Opening `docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md` afterwards: §2.1's unit map is
my table, §3's proof is my two lines, §3's witness is my witness. **It agrees to the letter,
including the `η` I thought I had found on my own** (see Correction 2 — I had, and so had the
parent; only the landing dropped it). P1, P2, P3 were pre-registered as formalities where they
were and are scored as such.

### 1.3 The independent LP

`a1_unitmap.py` re-solves `max 6E_μ[inv_e]/(n²−1)` over **all of `S_n`** at `n = 3,4,5,6`
(`720` columns at `n = 6`) on my own two-phase exact-rational simplex:

| `n` | max `E[inv]` | `= C(n,2)/3`? | `ε_spec` | max `E[F]` | `= 2C(n,2)/3`? | footrule `ε` | `n/(n+1)` |
|---|---|---|---|---|---|---|---|
| 3 | `1` | ✓ | `3/4` | `2` | ✓ | `3/4` | `3/4` |
| 4 | `2` | ✓ | `4/5` | `4` | ✓ | `4/5` | `4/5` |
| 5 | `10/3` | ✓ | `5/6` | `20/3` | ✓ | `5/6` | `5/6` |
| 6 | `5` | ✓ | `6/7` | `10` | ✓ | `6/7` | `6/7` |

**Identical to `mg-6bc2` §4's table, cell for cell, on code sharing no line with it.**

**NC1, run against the LP's own output rather than against itself** — four candidate closed
forms scored on the same four points: `n/(n+1)` **4/4 ACCEPT**; `2/(n+1)` **0/4 REJECT**;
`n/(n+2)` **0/4 REJECT**; `(n−1)/(6n)` **0/4 REJECT**; bare `1/6` **0/4 REJECT**. The last two
are the `ε_c3ca` value in the wrong currency — i.e. **the exact unit mismatch this lineage has
now committed three times** — so the agreement of the right form is not vacuous.

`inv ≤ footrule ≤ 2·inv` verified **pointwise** over `S_3…S_7`, `0` violations in `13,700`
permutations, which makes Claim 4.1's `≤` a corollary of Claim 3.1 needing no new work. Its
attainment reproduces at `n = 3,4,5,6`, and my LP's optimisers satisfy `F = 2·inv` on every
atom of their support — **confirming §4's stated mechanism, not just its number**.

---

## 2. The premise check (brief point 2) — the gate, settled by construction

The parent was sequenced after `L4` because the constant form was thought conditional on
`L4` at an `n`-free modulus. **The gate was cleared by disjunct (b): the pair-bias derivation
is independent of `L4`.** `STATE.md:164` records `mg-345e` establishing that, and `mg-6bc2`'s
header says *"Unblocked … by `mg-345e` on this ticket's own second disjunct; `L4` remains open
and is untouched here."*

**I do not have to take that on citation, and did not.** §1.1's ingredient list is three items
long and `L4` is not one of them. `L4`'s hypothesis is a thin prefix; nothing in
`Σ_{i∥j} Pr[flip] ≤ m/3` mentions a prefix, an interface, a modulus `F`, or `C₃`. The
independence is **visible in the derivation**, and it is independent *by force*: `L4`'s
hypothesis is reachable only through `L1b`'s own conclusion, so a derivation of `L1b`
invoking `L4` would be circular. **HELD. Row 11 is untouched by this audit and stays OPEN.**

**What that does NOT license.** The step from `E[inv_e]` to `1 − λ_std` is `mg-210d`'s master
bound, which I **did not re-derive** (`STATE.md:79` records it as unconditional, and
`mg-c4f5` hand-re-derived it). **Every `ε_spec` figure in this audit is therefore an
inversion-side figure**, and the spectral reading of them is inherited.

---

## 3. Direction of every inequality (brief point 5)

This arc's most repeated arithmetic-adjacent defect. Each is stated with which way "better"
runs, because that is what makes the check meaningful.

| statement | direction | verdict |
|---|---|---|
| `ε_sup < 1` | **upper** bound on the constant we can PROVE; **smaller is better** | correct |
| Claim 3.1 `max = n/(n+1)`, attained | **lower** bound on the best constant provable from per-pair marginals; it is what CLOSES the route | correct |
| `ε_dem = ε_leak²/(2C₃) ≤ 1/50` at `C₃ = 1`, `C₃ ≥ 1` | `1/50` is an **over-estimate of the budget**, so the demand is at most that | correct, and §6 says so |
| §3.1 `ε_spec = 3·d·q̄·n/(n+1)` | exact identity; verified over all `(n, m, q̄)` combinations tested, `0` disagreements | correct |
| §3.1's table requiring `3·d·q̄ ≤ target` | drops `n/(n+1) < 1`, making the requirement **stronger** than needed | **errs on the SAFE side** |
| gap factor `~50 = ε_sup/ε_dem` | `1 ÷ (1/50)`; and in `ε_c3ca` units `(1/6) ÷ (1/300)` is the same `50` | **normalisation-invariant**, so the unit map cannot be laundering a shortfall into a success |

**POINT 5 DOES NOT FIRE.** I looked specifically for a supply-side `ε` compared against a
demand-side `ε` with the direction unstated (the second, riskier half of my P5) and **did not
find one** — P5's second half is scored MISSED, in the parent's favour.

**One pricing the parent does not give, and it is the sharpest way to state what the theorem
is worth.** `inv_e(σ) ≤ m ≤ C(n,2)` holds **pointwise with no hypothesis at all**, so
`ε_spec ≤ 3n/(n+1) → 3` is **FREE**. Pair bias moves `3n/(n+1)` to `n/(n+1)`: **a factor of
exactly 3, at every `n`** — which is exactly the `1/3` of the hypothesis, transmitted once,
linearly. Against `ε_dem = 1/50` the whole distance is a factor of ~150, of which the theorem
covers 3. `grep` over every tracked `*.md`/`*.tex`/`*.html` for this comparison returns **1
line, my own `PREDICTIONS.md`** — so it is not on record (P14, held on this half).

---

## 4. Not a calibration (brief point 4) — **DOES NOT FIRE**

`ε_spec ≲ 2×10⁻²` is `mg-3ce3`'s empirical probe (`0` RED / `6681` up to `ε = 0.20`). In
`mg-6bc2` it appears **only on the demand side**, as `ε_dem ≤ 1/50` in §6 and in §3.1's target
column, explicitly inherited and explicitly not re-derived. The supply constant is `n/(n+1)`,
which comes out of §1.1's three ingredients and out of an LP over `S_n`. **The constant is
DERIVED. The whole ask was met.**

---

## 5. It does not bend toward `1/6` (brief point 6) — except in the banner

`1/6` is Daniel's conjecture. A deliverable that bent toward it would reach `1/6` in `ε_spec`
units through a step that a different conjecture would not survive. **`mg-6bc2` does the
opposite**: in `ε_spec` units it lands on `n/(n+1) → 1`, and it says in as many words that
`1/6` there would be a statement **`6×` stronger** than the `1/6` already proven, and
**provably unavailable** from pair bias. That is the honest answer and it is the one on the
page. **The mathematics does not bend.**

**Where it fires is the banner.** §0's headline sentence carries no unit. §2.1 exists
precisely to stop that weld, and the guard works everywhere except at the top of the document
that built it — the same shape §5's own Defect 5 records (*"a guard aimed outward is not a
check"*). **Correction 1 stands and it is presentational, not mathematical.**

**Which `1/6` Daniel meant is not decided here and is not mine to decide.** It is with him
(`mg-6bc2` §0 routes it; `STATE.md:15` says so). Everything above is true under either
reading.

---

## 6. Material beyond the brief

### 6.1 The sweep both parents refused had already been run

`mg-345e` (`STATE.md:164`): *"no enumeration — the frozen class is empty at every `n` this
corpus can enumerate … so the cheap sweep is **declared and refused**."* `mg-6bc2` §9:
*"**No poset enumeration.** The frozen class is empty at every `n` this corpus can
enumerate."* Both reasons are correct. **Neither says the enumeration already exists.**

I ran mine first and compared afterwards. `code/libweak_c3ca/p2_primitive.py` (from `mg-c3ca`,
the very document `mg-6bc2` §2 quotes for the `1/6`) walks the same population. Its committed
output and my independent one, side by side:

| quantity | `out_p2_primitive.txt` | `a2`/`a4` (mine, exact rationals, no shared line) |
|---|---|---|
| naturally-labelled posets, `n = 3..6` | — | `7, 40, 357, 4824` (`n=7`: `96428`) |
| non-chain posets, `n = 3..6` | `6, 39, 356, 4823` | `6, 39, 356, 4823` ✓ |
| primitive posets, `n = 3..6` | `4, 27, 275, 4070` | `4, 27, 275, 4070` ✓ (`n=7`: `86278`) |
| min `δ`, whole population | `0.3333…` at every `n` | `1/3` at every `n` ✓ |
| min `δ`, **PRIMITIVE only** | `1/3`, `0.400`, `0.363636`, `0.357143` | `1/3`, `2/5`, `4/11`, `5/14` ✓ (`n=7`: `14/39`) |
| critical family (`δ = 1/3`), size | `3, 6, 9, 21` | `3, 6, 9, 21` ✓ (`n=7`: `42`) |
| max `E[inv_e]` on it | `2/3, 2/3, 2/3, 4/3` | `2/3, 2/3, 2/3, 4/3` ✓ (`n=7`: `4/3`) |
| primitive with `δ ≤ 1/3`, `n ≥ 4` | `0 posets` | `0` at `n = 4,5,6,7` ✓ |
| ordinal-sum-of-`V` family | `δ = 1/3`, `E_maj = 2k/3` | same family, `δ = 1/3`, `E[inv_e] = 2k/3` ✓ |

**Every figure reproduces.** Its README already flags the emptiness as *"the finding (no
primitive poset attains `1/3` at those `n`)"* — so **my Finding on emptiness is a
REPRODUCTION, not a discovery, and P16's guard is what caught that.** It also says `n = 7`
*"was not attempted here"*, so `86278` and `14/39` are new.

**Note the near-coincidence and do NOT weld it:** my primitive count at `n = 6` is `4070`;
`STATE.md:42` quotes **`4,069`** of `4,824` for a *different* predicate (posets whose `λ_std`
moves across reference orders, `mg-c4f5`). **They differ by exactly 1 and they are not the
same quantity.** I did not re-measure `mg-c4f5`'s predicate.

### 6.2 The number `mg-6bc2` §1 asks for, formed here for the first time

§1: *"nobody has asked **how much the bound costs**, which is a number."* §3: *"the price of
dropping realizability is precisely the whole gap from `1` down to anything."* The relaxation
side is computed there. **The realizable side, over the `δ ≤ 1/3` class and in the same
units, is not** — and the nearest thing to it in the corpus
([`code/libweak_audit_c4f5/a1_premise.py:51`](../code/libweak_audit_c4f5/a1_premise.py)) takes
`inv` against the **natural labelling** rather than `e`, over the whole population rather
than the class, for a different purpose. **So the ratio has never been formed.**

| `n` | realizable max `ε_spec` over `δ ≤ 1/3` | relaxation max `n/(n+1)` | **price of dropping realizability** |
|---|---|---|---|
| 3 | `1/2` | `3/4` | `3/2` |
| 4 | `4/15` | `4/5` | `3` |
| 5 | `1/6` | `5/6` | `5` |
| 6 | `8/35` | `6/7` | `15/4` |
| 7 | `1/6` | `7/8` | `21/4` |

And an **all-`n`** family on the boundary: `P_k =` the ordinal sum of `k` copies of `tight3`,
`n = 3k`. `δ = 1/3` and `E[inv_e] = 2k/3` exactly (the linear-extension measure of an ordinal
sum factorises over blocks, so the pair probabilities are the blocks' own and `E[inv_e]`
adds), giving

> **`ε_spec(P_k) = 4k/(9k²−1) = Θ(1/n)`**, verified exactly at `k = 1…6`,

against a relaxation maximum tending to `1`. **So the price of dropping realizability is
`Θ(n)`, not a constant.**

**DIRECTION, because it is the whole value of the table.** The `n ≤ 7` column is an
**exhaustive maximum**, hence `FP` and an upper bound only there. The family is an all-`n`
**LOWER** bound on that maximum and bounds nothing from above. **And none of it is a bound on
the frozen class**, which is empty — see 6.3.

### 6.3 Why the empirical calibration is unavailable, for a stronger reason than emptiness

Both parents refuse because `δ < 1/3` is empty (reproduced: `0` posets at every `n ≤ 7`; the
`0` is a measurement, not an inert predicate — the same filter returns `3, 6, 9, 21` at
`≤ 1/3`, `3, 11, 78, 219` at `≤ 2/5` and `6, 39, 356, 4823` at `≤ 1/2`). Two further facts
make the refusal stronger:

1. **Above `n = 3`, every poset with `δ ≤ 1/3` is an ORDINAL SUM.** `0` primitive at
   `n = 4,5,6,7`. `STATE.md:47`: primitive ⟺ not an ordinal sum ⟺ `λ_std < 1`. So each of
   these has `1 − λ_std = 0` and satisfies `L1b` vacuously; **§6.2's realizable maxima are
   measured on objects that cannot be minimal counterexamples**, and I say so at the number.
2. **At the primitive minimum of `δ`, the distinguished order stops existing.** That minimum
   is `2/5`, `4/11`, `5/14`, `14/39` at `n = 4,5,6,7` — **strictly above `1/3` and not
   monotone** (`n = 7` sits above `n = 6`). At `δ > 1/3` the `≥2/3`-majority tournament is
   **incomplete**, so `e` is undefined and `inv_e` with it. My library returns `None` rather
   than falling back to the natural labelling (P15's guard, bound in the library so no script
   can bypass it), and **it fires on real data at every `n ≥ 4`.**

> **So there is no primitive poset anywhere in this corpus's reach at which `ε_spec` is even
> DEFINED, above `n = 3`.** A calibration that quietly used the natural labelling instead of
> `e` would print numbers for a quantity that does not exist, and they would look plausible.
> **That is the reason the refusal should carry**, and it is stronger than the one both
> parents gave.

### 6.4 `mg-131e`'s refutation of `ε_spec = 2/(n+1)`, re-derived from scratch

`STATE.md:167` names the branch. **I did not take its atoms.** I built the poset from the
complement of `I = {(0,1),(1,2),(2,3),(3,4),(4,5),(1,4)}`, **checked the comparable set is
transitive** (it is), enumerated its `14` linear extensions, and re-solved with my own
simplex under the flip caps **and** per-slot adjacency symmetry:

> **`max E[inv] = 11/6 > 5/3 = (n−1)/3`**, so `ε_spec = 11/35`, not `2/7`.

The optimiser my LP found is **6 atoms at mass `1/6` each**, and I verify it from the atoms
alone rather than from the tableau: total mass `1`; flip probabilities `1/3` on the five
consecutive pairs and `1/6` on `(1,4)`, max `1/3`, cap respected; **no comparable pair ever
flipped**; **`0` per-slot symmetry violations**. **`mg-131e` CONFIRMED, independently, in full.**
Control: the same branch **without** per-slot symmetry returns `|I|/3 = 2`, so the constraint
bites by exactly `1/6` and the refutation is not an artefact of an inert constraint. Its
surviving theorem — the consecutive-pairs branch is exactly `(n−1)/3` — reproduces at
`n = 3,4,5,6,7`.

**Where I saw `2/(n+1)` presented as live, as the dispatch note asks:** **6 sites in
`docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md` — `:35`, `:85`, `:310`, `:320`, `:347`,
`:504`** — and the string occurs in 13 tracked files corpus-wide. Known in-flight correction
(`mg-372e`); reported, not re-litigated.

### 6.5 Trying to build what the negative forbids (brief point 3)

Three attempts, **all failed**, and the failures are informative rather than empty.

| attempt | result |
|---|---|
| **1.** find `μ ∈ M_n` with `6E[inv]/(n²−1) > n/(n+1)` | impossible by one line; the LP maximum equals `C(n,2)/3` at every `n` tested |
| **2.** impose the **free** cyclic identity `Pr[x<y]+Pr[y<z]+Pr[z<x] ≤ 2` (`STATE.md:205`) on `M_n` and re-solve | **NO GAIN** at `n = 3,4,5,6` with `2/8/20/40` constraints added; value unchanged. Confirms by machine the hand argument `mg-6bc2` §5 gives (on a frozen triple it reduces to subadditivity of the `q`'s, satisfied with room to spare at `q = 1/3`) |
| **3.** impose per-slot adjacency symmetry **branch-free** on the full relaxation | **INFEASIBLE** at `n = 3,4,5` — reproducing `mg-200d`'s recorded negative independently, and a bound from an infeasible program bounds nothing |

**The obstruction, named.** `E[inv_e]` is a **sum over pairs**; the hypothesis caps each
summand; **linearity of expectation is an equality**. An argument that knows only the per-pair
caps can therefore produce only `Σ (cap)`, and the two-atom law sits on it. **The candidate
space below `n/(n+1)` has exactly two members and both are named on the page already:**

- **(a) the number of summands** — residual **(R)**, a frozen-conditional **upper** bound on
  `d`. `mg-6bc2` §7's re-run grep finds `5` lines and **`0`** proven upper bounds; my §6.2
  measurement adds that at every realizable maximiser `q̄ = 1/3` exactly, so **`d` is the only
  lever that moves** — which points at (R) specifically and not at §3.1's `q̄` alternative.
- **(b) a constraint no product of per-pair caps can express** — realizability. The two-atom
  law's defect is precisely that it correlates all flips **maximally**: one atom of mass `1/3`
  flips every pair at once. `mg-92e6`'s adjacency symmetry is the first proven fact that
  bites; `mg-200d`/`mg-131e` price it (and the constant it was thought to buy is refuted).

**I could not build what the negative forbids, and I do not think it is buildable**, for the
reason above rather than because my search was short.

---

## 7. Predictions, scored — including the misses, kept as written

| # | prediction | outcome |
|---|---|---|
| P1 | Claim 3.1's `≤` is linearity + per-pair `1/3` + `m ≤ C(n,2)`, nothing more | **HELD (FORMALITY, declared as such)** |
| P2 | Claim 3.1's `≥` is the two-atom measure | **HELD (FORMALITY, declared as such)** |
| P3 | the strictness caveat is ABSENT at the parent AND at `STATE.md` | **MISSED at the parent — it is there, as `M_n(η)`, and it is right. HELD at the landing.** Reported that way round: the parent gets the credit and my prediction gets the miss. |
| P4 | the constant is derived, not `mg-3ce3`'s calibration | **HELD** — `2×10⁻²` appears only as `ε_dem` |
| P5 | direction correct on Claim 3.1; **and** ≥1 site mixing supply/demand `ε` without stating direction | **HELD on the first half. MISSED on the second — I looked and found none.** |
| P6 | the `L4` gate cleared by disjunct (b), confirmed by construction | **HELD** |
| P7 | no bending toward `1/6` | **HELD** (low information — disclosed at filing) |
| P8 | 2–6 live `2/(n+1)` sites in the parent | **HELD at the top of the range: exactly 6** |
| P9 | my enumerator returns `1,2,7,40,357,4824` | **HELD**, and `4824` matches `STATE.md:42` |
| P10 | realizable max `<` `n/(n+1)` at every `n ∈ {3,4,5,6}` | **HELD** (formality at `n = 3`) |
| P11 | that maximum is **non-increasing** and `< 1/2` for `n ≥ 4` | **MISSED on monotonicity** — `1/2, 4/15, 1/6, 8/35, 1/6` rises at `n = 6`. HELD on `< 1/2`. |
| P12 | `0` posets with `δ < 1/3` at every `n ≤ 6`; boundary non-empty | **HELD** (and at `n = 7`) |
| P13 | my own search on `mg-131e`'s branch returns exactly `11/6` | **HELD, exactly** |
| P14 | the free-bound framing is nowhere on record | **SPLIT: HELD** for `3n/(n+1)` (1 hit, my own file); **MISSED** for the primitivity emptiness — `code/libweak_c3ca/README.md:61` already records it |
| P15 | *my likely error* — mis-specifying `e` | **GUARD FIRED ON REAL DATA** at every `n ≥ 4`, and prevented four printed numbers for an undefined quantity |
| P16 | *my likely error* — scoring a landed change of units as my discovery | **GUARD FIRED AND CAUGHT §6.1.** Without it I would have published a reproduction as a finding. |
| P17 | verdict shape CONFIRMED WITH CORRECTIONS | **HELD** |

---

## 8. Defects of this instrument, and what I did NOT do

**Defect 1 — one of my own printed counts was wrong before it was right.** A1.3 first printed
`52/51` because I subtracted one from the denominator to skip an `n = 2` case I had not
actually skipped. Caught by reading my own output, corrected to `52/52`, and recorded here
rather than quietly fixed.

**Defect 2 — I printed a false summary sentence over correct data.** A2.4's closing line said
*"BOTH levers move at once: `d < 1` and `q̄ < 1/3`"* while the `q̄` column beside it read
`1/3` at every row. The data was right and my sentence was wrong. It is now Correction 4, and
the correction is stronger than the sentence it replaces.

**Defect 3 — my n = 7 realizable maximum has a coverage caveat.** `86278` primitive posets is
an exhaustive naturally-labelled enumeration, but I did **not** deduplicate by isomorphism, so
the counts are of labelled representatives; maxima are unaffected, counts are not comparable
to unlabelled tallies.

**Defect 4 — the emptiness findings are `FP` and `n ≤ 7`.** Every *"0 primitive with
`δ ≤ 1/3`"* and every *"min primitive `δ`"* is a finite-population statement and says nothing
above `n = 7`. In particular *"primitive ⟹ `δ > 1/3`"* is **not** offered as a theorem.

### Not done, deliberately

- **No `L4` attempt.** Row 11 untouched, exactly as open as before.
- **No re-derivation of `mg-210d`'s master bound**, so the step from `E[inv_e]` to
  `1 − λ_std` is inherited and **every `ε_spec` figure here is inversion-side**. It is
  already re-derived by hand in `mg-c4f5` and machine-tested there at `0` violations over
  every naturally-labelled poset to `n = 7` (`out_a1_premise.txt`), which I read but did not
  re-run.
- **No `λ_std` computed anywhere.** A4's primitivity is combinatorial (incomparability-graph
  connectivity), not spectral; the identification with `λ_std = 1` is `STATE.md:47`'s, read.
- **No `C₃`, `ε_dem`, `ε_leak` or `ε₀`.** `1/50` is inherited from §6 and not re-derived;
  `mg-94c3`'s finding that `C₃ = 1` is a chain-(III)-currency statement is **read and not
  checked**, and it is a live qualification on `ε_dem` that this audit does not resolve.
- **Claim 4.1's attainment at `n = 8` and the hierarchical `7/8` construction: NOT re-derived.**
  I confirmed attainment only at `n = 3,4,5,6`, so the `8/7` ceiling is `mg-6bc2`'s and is
  carried, not checked.
- **No isomorphism-class enumeration, no `n ≥ 8` anywhere.**
- **`mg-200d`'s, `mg-131e`'s, `mg-ba78`'s and `mg-345e`'s instruments and documents were not
  opened.** I worked from `STATE.md`'s summaries and from `mg-6bc2`'s own text; §6.4's branch
  is `STATE.md:167`'s statement of it, re-solved. `code/libweak_c3ca/` was opened **after** my
  own sweep had run, which is why §6.1 is a comparison and not a source.
- **§7's `1/6` adjudication, §5's repaired diagnostics tables and §5.2's superseded table were
  read, not re-run.** `mg-ba78`'s repair is not re-audited here.
- **No edit to `STATE.md`, to `Op-Form`, or to `mg-6bc2`'s deliverable.** Corrections 1–4 and
  §6 are a **proposal**. In particular I do **not** strike the `2/(n+1)` sites: `mg-372e` owns
  that landing and a second hand in the same file is how a correction gets lost.
