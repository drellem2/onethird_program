# OneThird — INDEPENDENT AUDIT of mg-c3ca's (LIB-weak) deliverable

**Work item:** `mg-c4f5`. **Subject:** `docs/OneThird-LIBweak-mg-c3ca.md` at commit `81214a9`.
**Method:** hand re-derivation + an instrument written from scratch (`code/libweak_audit_c4f5/`,
exact integer/`Fraction` arithmetic; one declared tolerance, `1e-9`, at the eigenvalue step and
nowhere else). **Predictions pre-registered at `1661c7f`, before any script of this audit existed,
and never amended.** **What I did not do: §9.**

---

## 0. Verdict

> **THE PREMISE HOLDS. The parent's deliverable is correctly aimed, and my headline is not the
> one the ticket most feared.** `(LIB-weak) ⟹ λ_std → 1` is sound: it runs through mg-210d's
> master bound, which mg-c3ca explicitly did **not** re-derive and which I have now re-derived by
> hand in full (§1) and tested at **0 violations over 101 658 posets, `n ≤ 7`** (§2). The corpus
> half — "never attacked by any arc" — also holds: **0** of the 2 360 items in the store had
> (LIB-weak) as a deliverable before mg-c3ca (§3).

Six things do not survive. In order of how far they have already travelled:

1. **§5's headline refutation refutes a different statement from the one it names.** The document
   says the linear form `min(p,1−p) ≥ (1/3)(1−TV)` is **FALSE**, with 8 088 counter-pairs at
   `n = 6`. `p3_window.py` does not evaluate that. It evaluates `1−TV ≥ 1/2 ∧ min(p,1−p) < 1/3`,
   which is the refutation condition for a **threshold** statement at threshold `1/2`, not the
   negation of the linear form. This instrument reproduces `16 / 351 / 8 088` **exactly** under
   the parent's own predicate, and finds **0 counterexamples to the linear form at every `n ≤ 7`,
   over 1 168 036 pairs**. The parent's own quoted "worst" case — `1−TV = 0.5`,
   `min(p,1−p) = 0.212` — *satisfies* the inequality it is offered as refuting, with room
   (`(1/3)·0.5 = 0.167`). **This is in STATE.md**, as "its forward vector's marginal form is
   **false**". §4.
2. **The `ε_spec` figures are superseded by two orders of magnitude, and STATE.md said so in bold
   at the parent's own base commit.** §2.3 carries `2×10⁻⁴`, `~5×10³` and `~10⁵` as flat text.
   mg-e35c (merged 2026-07-29, a week earlier) replaced them with `2×10⁻²`, `~50`, `n ≈ 900`, and
   STATE.md at `81214a9^` reads: *"do not carry `2×10⁻⁴` or the `n ≈ 10⁵` crossover as flat
   text"*. **The error inflates the pessimism by 100×.** §5.
3. **STATE.md's row 8 contradicts itself inside one sentence, live at HEAD, in the clause that
   travelled.** It leads with the constant form, then says (LIB-weak) "closes **this row as
   phrased**", then says it "does *not* supply the constant form this row leads with". §6.
4. **`λ_std` is not a function of the poset.** It depends on the reference linear extension:
   **4 069 of 4 824 posets at `n = 6`**, maximum spread **1/3**. STATE.md's glossary defines it
   with no reference order in it, and the architecture's target for `1 − λ_std` is `≈ 0.02` —
   about **17× smaller than the ambiguity**. §7.
5. **`N₀` is not merely unspecified — no `N₀` exists.** §2.2's "only for `n ≥ N₀` unspecified" is
   right and understates itself: for *any* `N₀`, an `o(n²)` function violating (LIB-const) below
   it exists. For the concrete witness `n²/log₂ n` at the repaired constant, the threshold is
   `2³⁰⁰ ≈ 10⁹⁰`. §5.3.
6. **§3's verdict survives; the sentence supporting it does not.** "The corpus's own evidence
   points the other way at that scale" rests on a **width-3** result transferred to an any-width
   claim without a label, and on a statement about the cheapest violators of a *different and
   stronger* condition. I built the object the transferred cap forbids, exactly: `C_p ⊔ A_q` has
   `Θ(n)` elements each of `Θ(n)` mass **sharing one chain**, with `E_maj/n² = 0.125`. §8.

**Everything arithmetic in the parent reproduces.** All 11 printed figures of §6 reproduce
exactly from an independent parser, as do §5's three counts under §5's own predicate. The six
findings above are about **statements**, not about numbers.

---

## 1. The master bound, re-derived by hand — the step the parent skipped

mg-c3ca §7: *"I did not re-derive the mg-210d master bound."* Since §2.1's entire content is one
division through that bound, the bound **is** the premise. Re-derived here from
`one_third_width_three/docs/probe-lambda-constant-bound.md` §§1–2, every step:

| step | statement | check |
|---|---|---|
| L1.1 | `1−λ_std ≤ n·leak(A)/(\|A\|\|Aᶜ\|)` | Rayleigh on `f = 1_A − a·1`; `‖f‖² = \|A\|\|Aᶜ\|/n` ✓; `⟨1_A,S1_A⟩ = \|A\| − leak(A)` by index swap ✓; `\|A\| − \|A\|²/n = \|A\|\|Aᶜ\|/n` ✓ |
| L2.1 | `Σ_k leak_k = E[F]/2` | `Σ_k #{x ≤ k < σ(x)} = Σ_x (σ(x)−x)⁺`, and `Σ_x(σ(x)−x)=0` ✓ |
| L2.2 | `E[F] ≤ 2E[inv]` | `σ(x)−x = Σ_{y∥x} δ_y`, comparable `y` contribute `0` because **both** orders are linear extensions ✓ |
| L2.3 | `Σ_{k=1}^{n−1} k(n−k)/n = (n²−1)/6` | `n·n(n−1)/2 − (n−1)n(2n−1)/6`, over `n` ✓ |
| T2.4 | `1−λ_std ≤ 3E[F]/(n²−1) ≤ 6E[inv]/(n²−1)` | mediant `min a_k/b_k ≤ Σa/Σb` ✓ |

**It is unconditional.** It needs only that `L` is a linear extension of `P` and `σ` uniform on
`L(P)`. It does **not** consume freezing. (mg-e35c already recorded this as F6 against mg-88bd's
attribution; I reached it independently and agree.)

**Therefore §2.1 is correct**: `E[inv_e] = o(n²)` gives `1−λ_std ≤ 6·o(n²)/(n²−1) = o(1)`.
The implication is one division, and the content is entirely in the bound.

**One thing §2.1 does not say and should.** `E[inv_e]` and `λ_std` must be taken against the
**same** reference order. They are, because freezing makes `e` canonical and a linear extension.
But that is a hypothesis doing real work, and neither STATE.md's row 8 nor §2.1 names it. §7.

---

## 2. The premise, tested

`a1_premise.py`, over every naturally labelled poset on `n ≤ 7` (the A006455 population
`1, 1, 2, 7, 40, 357, 4824, 96428`, verified as such in `selftest_c4f5.py` §A):

| `n` | posets | violations, footrule form | violations, inversion form | equality cases |
|---|---|---|---|---|
| 2 | 2 | 0 | 0 | 2 |
| 3 | 7 | 0 | 0 | 2 |
| 4 | 40 | 0 | 0 | 2 |
| 5 | 357 | 0 | 0 | 2 |
| 6 | 4 824 | 0 | 0 | 2 |
| 7 | 96 428 | 0 | 0 | 2 |

**101 658 posets, 0 violations of either form.** The bound holds.

**A correction to my own prediction, kept.** P1 predicted equality "at the antichain and nowhere
else except degenerate `n ≤ 2`". There are **two** equality cases at *every* `n`: the antichain,
and **the chain** — where the equality is `0 = 0`. mg-210d claims equality *at* the antichain and
does not claim uniqueness; the uniqueness-among-non-degenerate-posets that I checked does hold.
My characterisation of the degenerate case was wrong. **P1 partially MISSED.**

---

## 3. "Never attacked by any arc" — the premise's second half

The sentence is mg-a58f's, in its STATE.md row, and mg-c3ca's §0 promotes it to *"'never
attacked' is an opportunity, not an oversight."* `a7_history.sh`:

- **Population searched, printed before the answer:** 2 360 `mg` item files; 115 merged docs and
  1 473 merged code files at `81214a9`; 329 commits.
- **16 item files contain the literal string `LIB-weak`.** Split at mg-c3ca's own filing
  (2026-08-05 23:49Z): **4 before** (`mg-d112`, `mg-1fdb`, `mg-88bd`, `mg-e768`), 10 after — every
  one of the "after" items being a consequence of mg-c3ca itself.
- **Of the 4 before, 0 have (LIB-weak) as a deliverable.** `mg-e768` is Daniel's capture question;
  the other three are the operative-form thread, which *states* the class and does not attack it.
- **Merged docs before mg-c3ca mentioning it: 3** — `STATE.md` and the two operative-form
  documents. Again: statements, not attacks.

**VERDICT: the claim HOLDS**, as a claim about the record. **P3 HIT.**

**One thing I could not check, stated rather than passed over.** STATE.md credits the mg-a58f row
to `docs/OneThird-Bbias-Locality-Lemma-IndependentAudit.md` (mg-d112, "CONFIRMED"). **That file
is not in this repository at `81214a9^`, is not at HEAD, and is not in
`one_third_width_three/docs/`.** So whether mg-d112 audited the *"never attacked"* half — as
opposed to the mathematics next to it — is **not verifiable from the record**. That is a measured
absence and I am not treating it as an accusation; the claim independently survives my own search
above.

---

## 4. §5 — THE REFUTATION IS OF A DIFFERENT STATEMENT

This is the largest finding and the one that has already travelled.

**What §5 says (verbatim):**
> The linear form `min(p,1−p) ≥ (1/3)(1−TV)` is **FALSE**: 8 088 counter-pairs at `n = 6`
> (worst `1−TV = 0.5` with `min(p,1−p) = 0.212`), 351 at `n = 5`, 16 at `n = 4`.

**What `p3_window.py` evaluates (its line 100):**
```python
if sim >= 0.5 and mn < 1 / 3:
    refuters.append(...)
```

`sim ≥ 1/2 ∧ mn < 1/3` is the refutation condition for **`1−TV ≥ 1/2 ⟹ balanced`** — a threshold
statement at threshold `1/2`. It is not the negation of `mn ≥ (1/3)·sim`. The document's own
quoted worst case makes the gap visible without any code: `(1/3)(0.5) = 0.1667 ≤ 0.212`, so that
pair **satisfies** the linear form.

**Both predicates, on one walk of one population** (`a5_window.py`):

| `n` | pairs | counterexamples to **(LIN)** `mn ≥ (1/3)·sim` | rows matching **(THR)** `sim≥½ ∧ mn<⅓` | mg-c3ca published |
|---|---|---|---|---|
| 3 | 11 | 0 | 0 | — |
| 4 | 130 | **0** | 16 | 16 ✓ |
| 5 | 1 984 | **0** | 351 | 351 ✓ |
| 6 | 41 044 | **0** | 8 088 | 8 088 ✓ |
| 7 | 1 168 036 | **0** | 250 023 | (new) |

The population sizes `11 / 130 / 1 984 / 41 044` match `out_p3_window.txt` line for line, and the
(THR) column reproduces the published counts exactly. **So this is not a parser disagreement and
not a population disagreement. It is the predicate.**

**How much room the linear form has** — `c*(n) := min over pairs of mn/sim`, the best constant for
which `mn ≥ c·sim` holds:

| `n` | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|
| `c*(n)` | 1/2 | 1/2 | 5/12 | 2/5 | **7/20** |
| | 0.500 | 0.500 | 0.417 | 0.400 | **0.350** |

Strictly above `1/3` at every reachable `n`, **and falling toward it.** This is a better
instrument for §5's own question than the refuter count, and it is not in the parent.

**Two further reporting errors in the same paragraph.** (a) `p3_window.py` sorts its refuter list
by `(mn, −sim)` and prints the top three, so the printed row is the one with the **smallest**
`min(p,1−p)`; §5 reports it as the **largest** `1−TV`. The actual largest `1−TV` among those rows
is `s*(n)` itself — `0.7368` at `n = 6`, not `0.5`. (b) §5's surviving threshold floors
(`0.316 / 0.450 / 0.500` at `1−TV ≥ 0.7 / 0.9 / 0.99`, `n = 6`) reproduce exactly, and **all three
fall at `n = 7`**: `0.300 / 0.448 / 0.496`. The floor at `≥ 0.7` is now **below `1/3`**. §5's
worry that the threshold moves with `n` applies to the floors too, and is now measured on five
points rather than three.

**What survives §5 intact:** `s*(n) = —, 0.500, 0.636, 0.737` reproduces **exactly**, and extends
to `0.7545` at `n = 7`. The "race between two measurable rates" framing is right, the vector is
correctly reported as undecided, and building a probe designed to kill one's own forward vector is
the right instinct. The defect is in what the probe was said to have killed.

**What this does NOT establish, said plainly.** The linear form surviving is not the same as step
2 working. The pigeonhole delivers `sim = 1 − O(1/n)`, so `(LIN)` at `c = 1/3` yields only
`mn ≥ 1/3 − O(1/n)`, which does not contradict `frozen` (that needs `mn ≥ 1/3` strictly). The
correct status of the forward vector is **still undecided** — it is undecided for a different
reason than the document gives.

---

## 5. (LIB-weak) vs (LIB-const) — audit target 4

### 5.1 The parent's headline is right, and is being misread downstream

*"They differ IN KIND, not in constant; the gap is a QUANTIFIER"* — **CONFIRMED** for the pair it
names. A limit gives the threshold only eventually; the minimal-counterexample argument needs it
at its own `n`.

**But there are two different gaps in this material and they are being set against each other:**

| | what it compares | what it is |
|---|---|---|
| **gap 1** | (LIB-weak) `o(n²)` vs (LIB-const) `≤ c n²` at fixed `c` | a **quantifier** over `n` |
| **gap 2** | what freezing gives free (`ε_spec ≈ 1`) vs what the architecture needs (`ε_spec ≲ 2×10⁻²`) | a **constant factor**, `≈ 50` |

Both are true. **A relay of the form "the residual is a constant (~50) *rather than* a
quantifier" is a category error** — the "rather than" is the mistake, not either number. I am
recording this because it is the shape in which this material has been reaching people.

### 5.2 The `~50` is right and the parent's `~5×10³` is stale by 100×

Same arithmetic, one input changed (`a6_calibration.py` C1). Freezing gives
`E[inv_e] < m/3 ≤ n(n−1)/6 = (2/3)·E_unif[inv]`, i.e. `ε_spec = n/(n+1) → 1`. The needed value as
a fraction of uniform is `(ε_spec/6)/(1/4) = 2ε_spec/3`. So the gap factor is `1/ε_spec`:

| `ε_spec` | gap factor | source |
|---|---|---|
| `2×10⁻⁴` | **5 000** | mg-88bd §6.4 — carried by mg-c3ca §2.3 |
| `2×10⁻²` | **50** | mg-e35c **F5**, audited and merged 2026-07-29; STATE.md |

`2×10⁻⁴`, `5×10³` and `10⁵` each appear **exactly once** in the parent, as flat text, at lines 88
and 90 — against STATE.md's own bolded instruction at `81214a9^` not to carry them. **P13 HIT.**

### 5.3 `N₀` is not unspecified — it does not exist

§2.2 says (LIB-weak) supplies the threshold "only for `n ≥ N₀` with `N₀` **unspecified**". That is
correct and it understates itself. `f(n) = n²/log₂ n` is `o(n²)`, and `f(n) ≤ (ε_spec/6)n²`
requires `log₂ n ≥ 6/ε_spec = 300`, i.e. **`n ≥ 2³⁰⁰ ≈ 10⁹⁰`** (at the *repaired* constant; at the
superseded one, `10⁹⁰³¹`). And more strongly: for **any** `N₀`, `g(n) := n²` below `N₀` and
`n²/log₂ n` above is `o(n²)` and violates (LIB-const) throughout `[1, N₀)`. **No `N₀` works for
the class.** The quantifier gap is unbounded, not merely unquantified.

### 5.4 The class chain needs its rider at its own site

§2.3 bullet 1 states `(LIB) ⊊ (LIB-weak) ⊊ (LIB-const)` as an inclusion — which **is** an
implication — and bullet 2 says "neither implies the other outright". Both cannot be read
literally. **Bullet 2 is right.** The chain is correct only as a statement about growth-rate
classes with (LIB-const) read as `O(n²)`; as a statement about the objects satisfying the three
conditions at the architecture's own constant, `(LIB-weak) ⊆ (LIB-const)` is **false**, per §5.3.
This is the defect mg-325c repaired in STATE.md at four sites, surviving here. **Severity: MINOR,
one site, mitigated by bullet 2's adjacency.** **P14 HIT.**

---

## 6. STATE.md row 8 contradicts itself in one sentence — LIVE at HEAD

Row 8 currently reads (elisions mine):

> **L1b — the wall**: frozen ⟹ **`1 − λ_std ≤ ε_spec`**, a constant uniform in `n` … **(B) ⟹ LIB
> ⟹ (LIB-weak)**, which closes **this row as phrased** … but **(LIB-weak) ⟹ (LIB-const) only for
> `n ≥ N₀` unspecified**, so it does *not* supply the constant form this row leads with.

"This row as phrased" and "the constant form this row leads with" are the same thing. The sentence
asserts and denies the same claim eight words apart.

**Provenance, so the repair goes to the right place.** Before `f85a4e8` (mg-2860), row 8 was
phrased `frozen ⟹ λ_std→1`, and mg-c3ca's own wording — "closes ledger row 8 **as written**" —
was accurate against it. mg-2860 rewrote row 8's lead **and** introduced the "as phrased" clause
in the same commit, so the phrase now points at the opposite of what it meant. mg-325c repaired
the neighbouring implication defect and left this one. The one-paragraph state carries the same
shape ("closes **row 8 as phrased**, not the form above").

**Repaired in this commit**, at both sites, by naming the form instead of the row.

---

## 7. `λ_std` is not a function of the poset

`λ_std = max spec(S|1⊥)` with `S = (T + Tᵀ)/2` and `T[x,i] = Pr[σ(x)=i]` **after relabelling by a
chosen reference linear extension `L`**. mg-210d says so (`:56–62`: the relabelling "is the only
place a choice enters"). STATE.md's glossary line 40 does not.

Sweeping every linear extension of every poset (`a1_premise.py` §B):

| `n` | posets whose `λ_std` moves with `L` | max spread | witness |
|---|---|---|---|
| 3 | 3 | 0.1667 | `0<2`, `1` free: `0.500 → 0.667` |
| 4 | 26 | 0.2500 | `0.500 → 0.750` |
| 5 | 274 | 0.3000 | `0.500 → 0.800` |
| 6 | **4 069 of 4 824** | **0.3333** | `0,1,2,3 < 5`, `4` free: `0.500 → 0.833` |

**The ambiguity is `1/3`. The architecture's target for `1 − λ_std` is `ε_spec ≲ 2×10⁻²`.** A
quantity that moves by `0.333` under an unstated choice cannot be constrained to `0.02` until the
choice is stated.

**Nothing here breaks the chain**, because freezing makes `e` canonical and every consumer uses
it — that is exactly mg-210d §3.1's "freezing removes the choice", and it is a good argument. The
finding is that **the removal is load-bearing and is not recorded where `λ_std` is defined.**

**One measured aside, offered and not pursued:** at `n = 5`, `λ_std(e)` is the **maximum** over
reference orders in 97 of 141 cases and strictly below it in **44**. So `e` is not the reference
order that makes `λ_std` largest, and the architecture is not using the friendliest available
frame. I did not investigate whether that matters.

---

## 8. §3 — the verdict survives, the supporting sentence does not

**P20 filed in advance the error I most expected to make here**: reading §3 as a claim that no
`Θ(n)`-scale object *exists*. It is not. §3 claims the named obstruction does not **transfer**,
and that claim is **CORRECT**: the block-cross is one-element-scale, (LIB-weak) is `n`-element
scale, and `Σ_x m_x = 2E[inv_e]` makes the scale gap exact. The iff is right (§10). **The verdict
stands.**

What does not stand is the sentence offered in its support:

> The corpus's own evidence points the other way at that scale: width-3 caps simultaneous deep
> crossings at boundedly many per shared chain (Bwall §4), and mg-a1ec Prop. 5.3 says (B) fails
> only via a **few** elements with `a_x` growing.

**(a) A width-3 result carried into an any-width claim, unlabelled.** STATE.md's own header:
*"Everything here is **any-width** — width-3 is old-repo baggage, not part of this program."*
The transfer may well be legitimate; it is not argued, and it is not marked.

**(b) The transferred cap is violated by an explicit poset.** `C_p ⊔ A_q` — a `p`-chain and `q`
free points, all `q` incomparable to the whole chain — is exactly "`q` elements each block-crossing
the **same** `Θ(n)` chain". Exact, at every size (`a3_construct.py` §A):

| `n` | 4 | 6 | 8 | 10 | 12 | 14 |
|---|---|---|---|---|---|---|
| `E_maj/n²` | 0.1146 | 0.1250 | 0.1219 | 0.1250 | 0.1235 | **0.1250** |
| `#{x : m_x ≥ n/4}` | 2 | 4 | 4 | 6 | 6 | 8 |
| `δ` | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 |

`Θ(n)` elements, each of `Θ(n)` mass, sharing one chain, with `E_maj = Θ(n²)`. **The
configuration exists as a poset.** What stops it being a counterexample is `δ = 1/2` — i.e.
**freezing, not scale**. Removing the free-free pairs (`C_p ⊔ C_q`, §B) keeps the mobility and
still gives `δ = 1/2`, now by reflection symmetry; breaking the symmetry (`p ≠ q`, §C) never gets
`δ` below `0.412` up to `n = 14`.

**(c) "(B) fails only via a few elements" is evidence about a different, stronger statement.**
It describes the *cheapest known* violators of (B). An instrument that finds the cheapest violator
of a stronger condition says nothing about whether expensive violators of a weaker one exist.

**Net.** §3's verdict is **CONFIRMED**. The clause *"the corpus's own evidence points the other
way at that scale"* is **UNEARNED and should be struck.** The honest replacement is what the
constructions above show: the `Θ(n)`-scale configuration is realisable as a poset and is stopped
only by `δ`, which is the whole difficulty and not an argument that it will not happen.

### 8.1 A measurement §3 wanted and did not take: the frontier

The question "can `Θ(n)` mass and near-freezing coexist" is answerable at reachable `n` as
`max E_maj/n²` subject to a **ceiling on `δ`** — not, as §6 does it, at the minimum `δ` only.
All naturally labelled posets, `n ≤ 7` (`a3_construct.py` §D; population size printed under each
cell so an empty band and a tiny band cannot print alike):

| `n` | `δ≤1/2` | `δ≤0.45` | `δ≤0.4` | `δ≤0.375` | `δ≤0.35` | `δ≤1/3` |
|---|---|---|---|---|---|---|
| 5 | 0.2000 | 0.0912 | 0.0912 | 0.0618 | 0.0267 | 0.0267 |
| 6 | 0.2083 | 0.0814 | 0.0633 | 0.0456 | 0.0370 | 0.0370 |
| 7 | 0.2143 | 0.0980 | 0.0789 | 0.0481 | 0.0272 | 0.0272 |
| *(count at n=7)* | 96 427 | 12 105 | 1 225 | 191 | 42 | 42 |

Primitive only, the band `δ ≤ 0.35` is **EMPTY at every `n ≥ 4`** — over populations of
27 / 275 / 4 070 / 86 278. **It does not collapse toward 0 at the ceilings that are non-empty**,
which is the honest state: `n ≤ 7` cannot see the asymptotic regime, and this is evidence about
the boundary, exactly as mg-c3ca says of its own §6.

---

## 9. What I did not do

- **I did not prove or disprove (LIB-weak).** Nothing here is progress on the wall.
- **I did not re-derive** Theorem E, Theorem G, the Cheeger sandwich, mg-88bd's backward
  derivation from L4, mg-3ce3's envelope, L3, or L4. Read, cited, not retested.
- **I did not read** Aires–Kahn 2509.11549 or Ma–Shenfeld 2211.14252, so §4's discharge is left
  exactly as mg-c3ca left it: **CONDITIONAL**, correctly flagged, correctly aimed at the
  neighbouring-claim misattribution STATE.md already records. **No new finding there.**
- **I did not settle** whether mg-d112 audited the "never attacked" half — the audit document
  STATE.md names is not locatable (§3).
- **I did not test the conditional form** of §5's step 2 on `I_x(τ)`, which is where mg-c3ca says
  the vector must actually be run. Everything in §4 is the **marginal** law.
- **I did not investigate** why `λ_std(e)` is below the reference-order maximum in 44 of 141
  cases (§7).
- **Everything empirical here is `n ≤ 7`,** and `n ≤ 7` cannot contain a `Θ(n)`-mobility
  configuration in the asymptotic sense. No claim in §§2, 4, 8 is asymptotic.
- **I did not re-run mg-c3ca's own scripts.** Every number attributed to it was read from its
  committed transcripts and re-derived from scratch here.

---

## 10. The parent's mathematics, checked by re-derivation

**§1's iff — CONFIRMED.** `Σ_x m_x = 2E[inv_e]` verified exactly on 101 658 posets (`a2_maths.py`
§A, max error `0`). Both Markov directions verified as finite-`n` inequalities over 4 values of
`α` (§B): **0 violations of either.** The proof is right.

*One quantifier written too strongly, no consequence.* §1 states the iff correctly (`= o(n)` for
every `α`). §3's table states its negation as "`= Ω(n)` for some `α`". The correct negation is
"is **not** `o(n)`", which permits a subsequence; `Ω(n)` as normally read demands it at every `n`.
A subsequence violator is still a violator, so the verdict is untouched. **P4 HIT.**

**§4's Prop. 4.1 — CONFIRMED.** `e(P) ≤ 2·C(2E[inv]+n, n)`: **0 violations**, `n ≤ 7`. The
asymptotic form `e(P)/n! ≤ 2(2e²ε + e²/n)^n` re-derives exactly.

*And two riders the parent does not carry.*
- **The bound is loose by two orders of magnitude at this size** — median
  `2C(·)/e(P)` of `3, 6.7, 11.7, 36, 104, **316**` at `n = 2..7`. "0 violations" without that
  ratio would overstate what the check tested — a bound this loose cannot be falsified by a
  population this small. (P5 predicted `> 10³` at `n = 7`; measured 316. **REFUTED**.)
- **Prop. 4.1 is VACUOUS for `ε ≥ 1/(2e²) ≈ 0.0677`**, since its base `2e²ε + e²/n` then exceeds
  1 and the bound reads `e(P)/n! ≤ 2`. **Freezing unconditionally gives only `ε < 1/6 ≈ 0.167`.**
  So at the unconditional frozen value **the entropy price says nothing**. The parent's claim is
  the `ε → 0` contrapositive and is unaffected — but "the price of (LIB-weak)" invites the reading
  that it bites at the frozen value, and it does not.

**§4's unstated-but-true step.** The inversion-table coding counts inversions of `σ` against `e`
over **all** pairs; `inv_e` counts only **incomparable** pairs. They coincide **only because `e`
is a linear extension** — which under freezing it is. The proof does not say so. **Exposition
gap, 0 consequence. P6 HIT.**

**§6 — every printed figure reproduces exactly** (`a4_census.py`, independent parser):

| figure | mg-c3ca | this audit | |
|---|---|---|---|
| min `δ`, all posets | `1/3` exactly, `n=3..6` | `1/3` exactly, `n=3..7` | ✓ |
| frozen posets found | 0 | 0 (detector drilled on a constructed frozen table) | ✓ |
| min `δ`, primitive | `0.400, 0.364, 0.357` | `2/5, 4/11, 5/14` | ✓ |
| max `E_maj`, primitive critical | `0.67, 1.00, 1.55, 1.64` | `2/3, 1, 17/11, 23/14` | ✓ |
| `E_maj/n²` falls | `0.074 → 0.046` (primitive) / `0.074 → 0.037` (all) | both reproduce | ✓ |
| `k`-V-gadget | `E_maj = (2/9)n` exactly | exact at `k = 1,2,3,4` | ✓ |

**11 of 11. P16's "≥ 9 of 11" HIT; its "≥ 1 not reproducible as printed" REFUTED.**

**What the fifth point does to §6's four-point reads:**
- **min `δ` primitive RISES at `n = 7`**: `0.400, 0.364, 0.357, **0.359**` (`14/39`). §6 claims
  only "strictly above `1/3`", which survives — but the natural reading of a descending sequence
  approaching `1/3` does not, and nothing supports "approaching". **P10 REFUTED** (I predicted
  `[0.340, 0.353]`).
- **max `E_maj` primitive critical**: `0.67, 1.00, 1.55, 1.64, **2.36**`. Against a
  least-squares line through the four published points the `n = 7` value misses by **+13.4%**,
  with the published four themselves missing by up to 11.3%. **"`Θ(n)`-shaped" is not supported
  by the data it is drawn from** — a four-point read of a sequence this rough cannot establish a
  rate. The *conclusion* (near-frozen primitives are inversion-light at reachable `n`) survives.
  **P11 REFUTED** — I predicted a miss of more than 15%.
- **`E_maj/n²` is not monotone in either population**: all-poset `0.074, 0.042, 0.027, 0.037,
  0.027`; primitive `0.074, 0.063, 0.062, 0.046, **0.048**`. "Falls `0.074 → 0.046`" is an
  endpoint statement about a sequence that rises in its last step.

**Δ_AT drift check (P15) — reported although it does not fire.** Ten terms
(`Delta_AT`, `Δ_AT`, `Hodge`, `Theorem G`, `Garland`, `Kaufman`, `ALOV`, `Alev`, `link bound`,
`Coxeter`) over the parent: **1 occurrence**, at line 229, inside §7 *"what I did not do"*
(*"the Cheeger sandwich, or Theorem G. Read, cited, not retested"*). Non-vacuity control: the same
term list over STATE.md hits 4 times, so the near-zero is a clean document and not a broken
search. **NO DRIFT. mg-c3ca did not repeat pm-onethird's error. P15 HIT.**

**Bound words.** `closes` ×5, `cannot` ×3, `suffices` ×1, `strictly` ×1, `never` ×1. Adjudicated:
all of `closes` are ridered at their own site (§2.2 is the parent's own correction to its ticket);
`never attacked` is a quotation and it holds (§3). **The unearned bound word is not in my list at
all** — it is **"is false"** in §0 item 5 and §5, and it is the subject of §4. **P17 REFUTED on
its named case** (I predicted the failure would be `never attacked`).

---

## 11. Corrections to pm-onethird's framing, as the ticket requires

1. **"mg-c3ca is unaudited" is now discharged**, and the discharge is mostly favourable: the
   premise holds, the mathematics is right, the negative's verdict survives, and every printed
   number reproduces. The caveat that has been attached to two mails and to STATE.md can come
   off — **replaced by the six items in §0, not simply removed.**
2. **The ticket's fear was misdirected.** It said: *"If (LIB-weak) does NOT close L1b as stated,
   the parent's whole deliverable is misaimed and that is your headline."* It does close it. The
   live defect was in the part of the deliverable nobody flagged — §5's own self-refutation.
3. **The ticket's fifth target ("check it did not drift onto Δ_AT") is clean**, and I am saying so
   explicitly because a target that never fires and is never reported cannot be told apart from a
   target never run.
4. **"The residual is a constant (~50) rather than a quantifier" — the `~50` is right, the
   `rather than` is wrong.** Two different gaps. §5.1.
5. **mg-c3ca's §8 correction to its ticket is itself correct and should be kept**: closing L1b
   alone does not close the chain (L4 is open, row 3b and L3 are empirical).

---

## 12. Instrument

`code/libweak_audit_c4f5/` — `lib_c4f5.py` (posets, order-ideal DP, exact pair laws, a Jacobi
eigensolver written here because there is no numpy and because sharing no linear algebra is a
stronger control), `selftest_c4f5.py` (**68 checks, 0 failures**), and probes `a1`–`a7`.
Exact `Fraction`/integer arithmetic; **one** tolerance (`1e-9`), at the eigenvalue step, declared
at its call site. No sampling. No import of `lib_c3ca`. Populations are stated at every printed
count, and every band prints the size of the population behind it.

**Five defects of this instrument, recorded in `README.md` and left in place in the code:**
its first two positive controls asserted the wrong object and the wrong reference order (the same
shape as mg-c3ca's own recorded defect 1, committed by its auditor); it accused two published
figures of contradicting each other **before measuring them**, and they do not; it printed "the
primitive sequence is monotone" one row above the `n = 7` value that refutes it; and a search with
a cap at `10⁶` **printed `None` as though `None` were the answer** — a cap reported as a
measurement, inside the section whose whole subject is a predicate reported as a different
predicate.
