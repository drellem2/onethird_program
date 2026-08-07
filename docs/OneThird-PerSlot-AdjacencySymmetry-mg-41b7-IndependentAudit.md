# `mg-41b7` — INDEPENDENT AUDIT of `mg-200d` (per-slot adjacency symmetry)

**Work item.** `mg-41b7`. **Subject.** `mg-200d`, *"What does PER-SLOT adjacency symmetry buy?"*
**Instrument.** [`code/perslot_audit_a41b7/`](../code/perslot_audit_a41b7/).
**Predictions.** [`code/perslot_audit_a41b7/PREDICTIONS.md`](../code/perslot_audit_a41b7/PREDICTIONS.md),
committed at **`3c5ed10`** before one byte of `code/perslot_symmetry_200d/`, of the `mg-200d`
document, or of `STATE.md` had been read.

## Commits read

| what | commit |
|---|---|
| `mg-200d`'s landing (finding + instrument + docs) | **`762921d`** |
| `mg-200d`'s evidence transcripts | `ffc5501` |
| `mg-200d`'s post-landing re-check | `731a9ab` |
| `main` at the time of this audit | **`dafe759`** |
| `mg-6bc2`'s landing (the baseline), read as parent only | `e1f7bb2` |

The document as read at `dafe759` is **not** the document as landed: `mg-372e` (`dafe759`) had
already struck the `2/(n+1)` cells **in place**. Both readings are scored below and the
difference is stated wherever it matters.

---

## 0. Verdict

> # **CONFIRMED. EVERY CHECK IN MY BRIEF PASSES, AND EVERY CORRECTION THIS AUDIT PRODUCES IS A CORRECTION OF THE BRIEF, NOT OF `mg-200d`.**
>
> **And the one thing my brief told me to try, I did: I BUILT THE MEASURE THAT BEATS THE
> BOUND — not once, but as a FAMILY at every `n` from 6 to 12, found without reading
> `mg-131e`, `mg-eaa1` or `mg-00a1`.**

| # | brief item | verdict |
|---|---|---|
| 1 | re-solve the LP, exact rationals, no shared code | **PASS.** Own simplex, own rows, own combinatorics. Baseline, both literal forms and the disjunctive value all reproduced, each with a **dual certificate** as well as a primal witness. No float on any decision path. |
| 2 | verify the **constraint matrix**, not the prose | **PASS, AT THE MATRIX.** 219 branches at `n = 3,4,5`: my rows are `lp200d.build(..., 'slot_eq', ...)`'s rows, **0 differ**, with two negative controls proving the comparison is not vacuous. It is the **per-slot** form. |
| 3 | if it reports an improvement, build a measure that beats it | **DONE. `E[inv] = 11/6 > 5/3` at `n = 6`**, six atoms, verified by substitution and dual-certified — and a **family** beating `(n−1)/3` by `1/6` at `n = 6,7,8,9,10,11,12`. |
| 4 | distinguish an INFEASIBLE LP from an unimproved one | **PASS, AND IT WAS THE CRUX.** The literal per-slot form is **INFEASIBLE** at `n = 3,4,5` — empty polytope, phase-1 residual `1/3` — not "unimproved". `mg-200d` says exactly this. I also exhibit the **mechanism**, which `mg-200d` does not print. |
| 5 | check the `n`-range claim **at the claim** (corrected form) | **PASS — `mg-200d` DOES NOT MAKE THIS ERROR.** It states at the same volume as its result that `(n−1)/3` is exact at three points, that `≥` is a theorem for all `n`, and that `≤` is *"a CONJECTURE and is not proven here"*. |
| 6 | check the sizing sentence exists | **PASS.** §6, in the `ε_spec = 3·d·q̄·n/(n+1)` currency, with `1/150` named, and it says the ticket's own sizing instruction cannot be obeyed as written. |
| 7 | confirm no poset enumeration | **PASS.** The index set is subsets of pairs; transitivity is never imposed. Independently confirmed: my `n = 5` optimum lands on a **non-transitive** branch, which no poset enumerator could reach. |

### The corrections, and they are all to my own brief

1. **Brief item 2's premise is FALSE.** It says *"mg-6bc2 measured that the aggregate form
   excludes NOTHING at n=3"* and instructs me to score `mg-200d` against it. I derived by hand,
   **before reading any repository file about this**, that aggregate symmetry together with
   `E[inv] = 1` is infeasible at `n = 3` (`PREDICTIONS.md` H10); my LP then found something
   stronger — **the whole aggregate polytope is EMPTY** at `n = 3, 4, 5`, phase-1 residuals
   `1/3`, `1/5`, `1/6`. The premise traces to `mg-6bc2`'s pre-`mg-ba78` figure of `0` aggregate
   violations, measured on a **sub-probability measure missing a third of its mass**, already
   struck to `2 of 3` by `mg-ba78` — and corrected by `mg-200d` itself at its §8.1. **My brief
   quoted a superseded number as the standard to judge by.**
2. **Brief item 5 was already conceded wrong** by `pm-onethird` at 20:03. Checked at the claim:
   `mg-200d` does not conflate Claim 3.1 with Claim 4.1 in either direction.
3. **The brief's framing is a category error.** It says *"any improvement mg-200d reports is a
   claim that a constraint moved a proven optimum"*. It is not. `mg-6bc2`'s equality is a
   maximum over **all** of `M_n`; the disjunctive value is a maximum over the **realisable
   subset** of `M_n`. A smaller maximum over a smaller set contradicts nothing. I computed both
   side by side (§2, §4) and `mg-6bc2`'s `C(n,2)/3` is **untouched**.

### The load-bearing findings, which the brief did not ask for

`pm-onethird` re-pointed this audit twice by mail (21:02 and 21:12): `mg-200d`'s conclusions are
already dead downstream, but its **instrument** is load-bearing, because `mg-131e` and `mg-00a1`
— *"the reason I told Daniel tonight that a whole research route is dead"* — both ran their own
witnesses through `lp200d.measure_report`. *"Two witnesses through one instrument is one witness
wearing a larger number."* Two separate answers, and they are reported separately because
conflating them is the error this lineage keeps making:

> **(1) IS THE TOOL CORRECT? YES.** `lp200d.measure_report` differential-audited against my
> independent reporter: **111 of 113 checks pass**, including hand-computed expected values,
> sub-probability measures, planted asymmetries and six mutations. The two failures are a single
> **latent** float path that is shown not to bite at any live call site (§7).
>
> **(2) DO THE DOWNSTREAM WITNESSES SURVIVE AN INDEPENDENT CHECK? YES — 203 of 203.**
> `mg-131e`'s witnesses at `n = 6,7,8,9,10` and `mg-00a1`'s staircase family at **`n = 4..24`**
> re-checked by `liba41b7`, sharing no line with `measure_report`: mass, the `1/3` cap,
> comparable pairs at flip `0`, per-slot symmetry on every incomparable pair, transitive
> closure, and each one's claimed `E[inv]`. **Zero failures.** Those two results no longer share
> a tool (§7b).

---

## 1. The object, stated so that a reader can check I audited the right thing

`M_n` is the set of probability measures `μ` on `S_n` such that every pair is flipped against
the reference order `e` with probability at most `1/3`:

```
    maximise   E_μ[inv_e]        over  μ ≥ 0,  Σ μ = 1,
    subject to Pr_μ[ y before x ] ≤ 1/3   for every pair  x < y  in  e.
```

`mg-6bc2`'s theorem is `max E[inv_e] = C(n,2)/3`, equivalently `ε_spec = 6E/(n²−1) = n/(n+1)`.
Per-slot adjacency is `J_k(x,y) = μ{σ : σ places x in slot k and y in slot k+1}`, for
`k = 0..n−2`; the aggregate form is `J = Σ_k J_k`.

**Verified before anything else** (`selftesta41b7.py`, 62 checks): the two-atom law
`μ = (2/3)δ_e + (1/3)δ_{rev e}` has mass `1`, every flip probability **exactly** `1/3`,
`E[inv] = C(n,2)/3` and `ε_spec = n/(n+1)` — at `n = 3,4,5,6,7`. This is `mg-6bc2` Claim 3.1's
attainment and it is a **two-permutation construction**, not a finite-population result, which
is the point my brief's item 5 got backwards.

---

## 2. The literal reading is INFEASIBLE, and I say why — not merely that

`a1_forms.py`, exact rationals, status reported before any value:

| `n` | baseline `M_n` | literal **per-slot** | literal **aggregate** |
|---|---|---|---|
| 3 | `1` = `C(3,2)/3`, `ε_spec = 3/4` | **INFEASIBLE**, phase-1 residual `1/3` | **INFEASIBLE**, residual `1/3` |
| 4 | `2`, `ε_spec = 4/5` | **INFEASIBLE**, residual `1/3` | **INFEASIBLE**, residual `1/5` |
| 5 | `10/3`, `ε_spec = 5/6` | **INFEASIBLE**, residual `1/3` | **INFEASIBLE**, residual `1/6` |

Every baseline row carries a primal witness **and** an arithmetic dual certificate, both
verified by substitution. This reproduces `mg-6bc2`'s theorem on code sharing no line with it.

**Brief item 4 asks me to distinguish an infeasible LP from an unimproved one, and this is
exactly where the distinction bites.** `PREDICTIONS.md` P14 bound me, before any LP ran, to a
two-phase solver that prints its phase-1 residual and to a negative control (`NC1`) requiring
*infeasible*, *feasible-with-optimum-0* and *feasible-with-nonzero-optimum* to come back as
**three different answers**. `NC1` passes in all four of its arms. The residuals above are
**strictly positive**, so these are empty polytopes, not zero optima.

### The mechanism, which `mg-200d` does not print

Imposing per-slot symmetry **alone**, with the `1/3` cap removed, and then minimising and
maximising each pair's flip probability:

| `n` | `E[inv]` under per-slot symmetry alone | every pair's flip probability |
|---|---|---|
| 3 | pinned: `max = min = 3/2 = C(3,2)/2` | **pinned to exactly `1/2`** |
| 4 | pinned: `max = min = 3 = C(4,2)/2` | **pinned to exactly `1/2`** |
| 5 | `[24/5, 26/5]`, not pinned | confined to `[2/5, 3/5]` |

So at every `n` tested the smallest flip probability any per-slot-symmetric measure can
achieve is `1/2, 1/2, 2/5` — all **strictly above** the cap `1/3`. The infeasibility is
quantitative and structural, not incidental: **the symmetry rows alone already force more
disorder than the pair-bias budget allows.** By contrast the aggregate form leaves each
individual flip free in `[1/3, 2/3]` at `n = 4` yet is still infeasible once **all** the caps
are imposed together — a distinction a per-pair diagnostic cannot see, and precisely the shape
of error `mg-ba78` had to repair in `mg-6bc2`.

**`mg-200d`'s §2 says the literal form is unsound and returns INFEASIBLE at `n = 3,4,5`. I
confirm it independently, and its own pre-registered `H4` predicted it before it ran.**

---

## 3. The constraint matrix, verified as a matrix

`PREDICTIONS.md` **P13** was my own most-likely-error, filed before `lp200d.py` was opened:
that I would pick a different formalisation of "per-slot adjacency symmetry", get a different
number, and score a *reading* as *mathematics*. The guard it bound me to is `a4_rowcheck.py`.

Rows are canonicalised to `(sense, rhs, {(permutation word, coefficient)})` — **keyed by the
permutation, not by a column index**, so a different column ordering cannot make two different
systems look alike — and compared as multisets, with each equality also matched against its own
negation.

* **219 branches** across `n = 3, 4, 5`. **0 row-systems differ.** Supports agree too.
* Negative control 1: my **aggregate** rows against their per-slot rows — **rejected**.
* Negative control 2: cap `1/4` instead of `1/3` — **rejected**.

So the comparison is not vacuous and **my rows are its rows**. In `lp200d.build`, `slot_eq`
uses `spans = [(k,) for k in range(n-1)]` — one row per `(slot, pair)`. **It is the PER-SLOT
form, not the aggregate form.** Brief item 2's worry did not occur.

*(This is the only place in this audit that touches `mg-200d`'s code, and it is an assertion,
not a dependency: no number reported anywhere else passes through it.)*

---

## 4. The disjunctive value, re-solved exhaustively and independently

The disjunction — which I derived from realisability before reading `mg-200d`'s §4 — is that
with `e` a linear extension, each pair is **either** comparable, and then its flip probability
is `0`, **or** incomparable, and then swapping an adjacent `x,y` is an involution of `L(P)`,
so `J_k(x,y) = J_k(y,x)` at every slot. That is a union of `2^C(n,2)` polytopes.

`a2_disjunctive.py`, every branch, exact rationals:

| `n` | branches | feasible | **max `E[inv]`** | `(n−1)/3` | `ε_spec` | `2/(n+1)` | attaining branch |
|---|---|---|---|---|---|---|---|
| 3 | 8 | 3 | **`2/3`** | `2/3` ✔ | `1/2` | `1/2` ✔ | `C = {(0,2)}`, transitive |
| 4 | 64 | 13 | **`1`** | `1` ✔ | `2/5` | `2/5` ✔ | `C = {(0,2),(0,3),(1,3)}`, transitive |
| 5 | 1024 | 116 | **`4/3`** | `4/3` ✔ | `1/3` | `1/3` ✔ | `C = {(0,2),(0,3),(1,4),(2,4)}`, **NOT transitive** |

Every row carries a primal witness and a **verified dual certificate**, and each witness is
re-checked by substitution: mass `1`, max flip `1/3`, **0** per-slot symmetry violations on the
incomparable pairs, **0** nonzero flips on the comparable pairs.

`mg-200d`'s `2/3, 1, 4/3` and its `ε_spec = 1/2, 2/5, 1/3` **reproduce exactly**. So does its
§7 claim that the `n = 5` optimum lands on a branch that is not any poset's pattern — I found
the same non-transitive branch without having read that sentence.

Two further published numbers also reproduce (`a5_construction.py`):

* the **sound branch-free surrogate** `J_k(y,x) ≤ J_k(x,y)` gives `1, 2, 10/3` at `n = 3,4,5` —
  identical to the baseline, so it **buys nothing**, as `mg-200d` §3 says;
* the **sound disjunctive aggregate** gives `2/3, 5/3, 7/3` at `n = 3,4,5` — `mg-200d`'s §5
  numbers, to the digit.

---

## 5. The `≥` direction is sound at every `n` I could reach — on my own construction

`mg-200d` splits its result into a `≥` direction it calls a theorem for all `n` and a `≤`
direction it calls a conjecture. **These have different kinds and I checked them separately.**

For `≥` I did not read its §4.2. I built my own: take the poset `i < j ⟺ j ≥ i+2`, whose
incomparable pairs are exactly the `n−1` **consecutive** pairs, and put mass `1/3` on each of

* the identity,
* `A` = the product of the adjacent transpositions `(i,i+1)` over **even** `i`,
* `B` = the same over **odd** `i`.

Even/odd is a proper 2-colouring of the path on the `n−1` consecutive pairs, so each is flipped
by exactly one atom: every flip probability is exactly `1/3` and `E[inv] = (n−1)/3`.

`a5_construction.py` checks this **by substitution, with no LP**, at `n = 3..20`:
mass `1`, value `(n−1)/3`, every flip `≤ 1/3`, every comparable pair at flip `0`, **zero**
per-slot symmetry violations on incomparable pairs, `|I| = n−1`, `C` transitively closed.
**18 of 18, no failures.** A three-atom construction verified at every `n` in range is not a
finite-population result, and `(n−1)/3` is a genuine lower bound on the disjunctive value.

**Negative control**, reproducing `mg-200d`'s own recorded defect 1: the *mod-3* colouring hits
the value and the cap but **violates per-slot symmetry from `n = 4`** — confirmed here at
`n = 4, 5, 6`. Its self-reported defect is real and correctly described.

---

## 6. Brief item 3: I BUILT THE MEASURE. `(n−1)/3` IS NOT THE VALUE FROM `n = 6`

A new upper bound is a negative, and this arc's clearest regularity is that its negatives fall
to auditors constructing the object the negative forbids. So I constructed it.

### 6.1 The witness at `n = 6`

Comparable set `C = {(0,2),(0,3),(0,4),(0,5),(1,3),(1,5),(2,4),(2,5),(3,5)}` — transitively
closed, so it is a genuine poset. Incomparable `I = {(0,1),(1,2),(1,4),(2,3),(3,4),(4,5)}`,
**six pairs, one more than `n−1 = 5`**. The measure is six atoms of mass `1/6`:

```
    012345 (inv 0)   013254 (inv 2)   021435 (inv 2)
    024135 (inv 3)   102354 (inv 2)   103245 (inv 2)
```

Checked by substitution, not by a solver: mass `= 1`; flip probabilities
`(0,1)=(1,2)=(2,3)=(3,4)=(4,5)=1/3` and `(1,4)=1/6`, so **every** flip is `≤ 1/3`; **0** flips
on comparable pairs; **0** per-slot symmetry violations on incomparable pairs. And

```
    E[inv] = 11/6  >  5/3 = (n−1)/3,        ε_spec = 11/35  >  2/7 = 2/(n+1).
```

The `≤` direction is **FALSE at `n = 6`**, and the extra `1/6` is visible in the arithmetic: the
five consecutive pairs each carry the full `1/3`, and the one extra incomparability `(1,4)`
carries `1/6` on top.

### 6.2 It is a FAMILY, not a point

`a7_family.py`: take the same fence poset and **delete** the relation `1 < 4`; delete further
spaced relations `(5,8)`, `(9,12)` for `k = 2, 3`.

| `n` | `(n−1)/3` | `k = 0` (control) | `k = 1` | `k = 2` |
|---|---|---|---|---|
| 6 | `5/3` | `5/3` — exact | **`11/6`**, beats by `1/6` | — |
| 7 | `2` | `2` — exact | **`13/6`**, beats by `1/6` | — |
| 8 | `7/3` | `7/3` — exact | **`5/2`**, beats by `1/6` | — |
| 9 | `8/3` | `8/3` — exact | **`17/6`**, beats by `1/6` | infeasible |
| 10 | `3` | `3` — exact | **`19/6`**, beats by `1/6` | **`10/3`**, beats by `1/3` |

**The `k = 0` control returns exactly `(n−1)/3` at every `n`**, so the machinery is not simply
inflating everything: the `k = 1` gain is the deletion's, and it is the same `1/6` every time.
Every entry is dual-certified and every witness re-checked by substitution.

### 6.3 The complete determination at `n = 6`

Rather than sample, `a3_n6.py` / `a3b_level.py` settle `V_6 > 5/3` **completely**, using two
reductions that are proved and then **verified as controls before being used**:

* **(R1)** `E[inv]` is the sum of the flip probabilities; comparable pairs contribute `0` and
  the rest are capped at `1/3`, so `value(branch C) ≤ |I|/3`. A branch can only beat `5/3` if
  `|I| ≥ 6`. *(0 mismatches at `n = 3,4,5`.)*
* **(R2)** A non-transitive `C` has the **same support** as its transitive closure but a
  **superset** of its rows, so it can never exceed it; the max over all `2^15` branches is the
  max over transitively closed ones. *(0 violations over every branch at `n = 3` and `n = 4`.)*

That leaves `4387` branches, scanned exhaustively by `|I|` level. Completed levels:

| `\|I\|` | branches | feasible | max `E[inv]` |
|---|---|---|---|
| 6 | 423 | **6** | **`11/6`** |
| 7 | 633 | 5 | `5/3` |
| 8 | 809 | 3 | `5/3` |
| 9 | 869 | 1 | `5/3` |
| 10 | 766 | **0** | — (no feasible branch) |

Feasibility collapses as `|I|` grows — `6, 5, 3, 1, 0` — which is the same mechanism as §2: the
more pairs you require to be symmetric, the further the forced flip probabilities rise above the
`1/3` cap. Levels `11..15` (`526, 260, 85, 15, 1` branches) were still running at write-up and
are declared as such in §9. **The refutation does not depend on them**: `V_6 ≥ 11/6 > 5/3` is
settled by the `|I| = 6` level alone, with a primal witness and a dual certificate.

**I did not read `mg-131e`, `mg-eaa1` or `mg-00a1`, and did not reconcile against them.** That
`mg-131e` reports the same `n = 6` failure is, from this audit's side, an out-of-sample
agreement it had no access to.

---

## 7. The instrument, which is the part that is still load-bearing

`pm-onethird` (mail, 21:02): *"mg-200d's conclusions are already dead; its INSTRUMENT is
load-bearing for two live results"*, because `mg-131e` and `mg-00a1` both ran their own
witnesses through `lp200d.measure_report`.

`a6_instrument.py` runs it side by side with my independent reporter on measures chosen to hit
where a reporting bug would hide. **Agreement between two implementations of the same wrong
idea proves nothing**, so every comparison is also checked against a hand-computed value, and
six mutations are fed in that must be rejected.

* **A.** Two-atom law at `n = 3,4,5,6` and uniform at `n = 3,4,5`: mass, `E[inv]`, max flip,
  per-slot violation **set**, aggregate violation **set** — all agree, and `E[inv]`, the
  violation counts and the uniform measure's *zero* violations match hand values derived
  independently.
* **B.** **Sub-probability measures**, the exact class that broke `mg-6bc2`'s diagnostics: mass
  is reported as `2/3`, not silently as `1`, and completing the measure **changes** the
  violation set — which is the substance of `mg-200d` §8.1, confirmed.
* **C.** **Planted asymmetry** at one known `(slot, pair)`: reported when present, not reported
  when absent, in both implementations.
* **D.** Six mutations, all rejected as required, including that the `slot_le` surrogate holds
  on `uniform L(P)` — the population it is claimed on — and **fails** off it, so the predicate
  is not vacuous.
* **F.** The disjunctive optimal witnesses at `n = 3,4,5`, i.e. the objects downstream work
  actually reports on: every field agrees and its `E_inv` equals my LP optimum exactly.

**111 of 113 checks pass. `measure_report` is sound.**

### The one hazard, stated at the size it is

`lp200d.eps_spec` computes `6 * e_inv / (n*n - 1)`. Handed a **Python `int`** it returns a
**float** — `eps_spec(5, 1)` is `0.25`, not `Fraction(1,4)`. That is the exact hazard brief
item 1 names: *a floating-point optimum near a rational is indistinguishable from it*.

**It does not bite anywhere.** `measure_report` accumulates `E_inv` from `F(0)`, so it is a
`Fraction` on every input tested — including integer weights, zero weights and the empty
measure — and every call site in `perslot_symmetry_200d`, `dual_certificate_131e` and
`dual_certificate_audit_eaa1` passes either an LP value or `rep['E_inv']`. So this is a
**hardening note, not a defect**: one `F()` on the argument would close it. The two checks are
left **failing** in `a6_instrument.py` rather than tuned away, because a check tuned until it
returns `0` is unfalsifiable.

---

## 7b. The two downstream witnesses, checked by code that shares nothing with the tool

`pm-onethird`'s second mail: `mg-131e` and `mg-00a1` *"look independent. THEY SHARE ONE
UNAUDITED TOOL."* `a8_downstream.py` takes their **measures** as input data — that is the object
under test and there is no way to test it without reading it — and checks every property with
`liba41b7`, which shares no line with `measure_report`.

| source | `n` | claimed `E[inv]` | **my `E[inv]`** | mass `1` | cap `1/3` | comparable at `0` | per-slot sym on `I` | `C` transitive |
|---|---|---|---|---|---|---|---|---|
| `mg-131e` | 6 | `11/6` | **`11/6`** | ✔ | ✔ | ✔ | ✔ | ✔ |
| `mg-131e` | 7 | `20/9` | **`20/9`** | ✔ | ✔ | ✔ | ✔ | ✔ |
| `mg-131e` | 8 | `8/3` | **`8/3`** | ✔ | ✔ | ✔ | ✔ | ✔ |
| `mg-131e` | 9 | `28/9` | **`28/9`** | ✔ | ✔ | ✔ | ✔ | ✔ |
| `mg-131e` | 10 | `7/2` | **`7/2`** | ✔ | ✔ | ✔ | ✔ | ✔ |
| `mg-00a1` | 4…24 | `n(n+5)/36` (even), `(n−1)(n+4)/36` (odd) | **matches at all 21** | ✔ | ✔ | ✔ | ✔ | ✔ |

**203 checks, 0 failures.** So the two results that shared a tool are now two results that do
not: their witnesses are feasible measures on transitively closed branches by arithmetic that
never touches `lp200d`.

**Corroboration, stated as corroboration and not as proof.** `a41b7` reached `E[inv] = 11/6` at
`n = 6` by its **own exhaustive LP** (§6.3, `|I| = 6` level, 423 branches) **before reading
`mg-131e`'s witness at all**, and my witness and theirs agree on four of six atoms and differ
only in which of two atoms carries the `(4,5)` swap. I did not reach `Θ(n²)` independently and
make **no claim** about the growth rate.

**One observation about `mg-00a1`, outside my scope and reported as an observation.** Its
`s1_witness.py` banner and its table's column header both print the closed form as
`n(n+5)/36` unqualified, while its `lib00a1.witness_target` is correctly **parity-split**.
Its computed values are right — my checker confirms all 21 — and both branches are quadratic,
so nothing of its verdict moves. But the printed label is the even-`n` form only, and the next
agent greps labels. *(This cost me an hour and a near-miss: see defect 6.)*

---

## 8. Items 5, 6, 7 — checked at the claim, not against a summary

**Item 5, `n`-range (in the corrected form).** `mg-200d` does **not** make this error, and it
guards against it in the strongest available way — by saying so at the same volume as the
result. At landing (`762921d`) its §0 reads: *"`(n−1)/3` is EXACT only at `n ∈ {3,4,5}` — a
finite population, three points. The `≥` direction is a theorem for every `n` (an explicit
3-atom construction, §4.2). The `≤` direction is a CONJECTURE and is not proven here."* It then
says a proof at all `n` *"would be a proof of the LIB face"* and *"if a three-point
extrapolation is going to break, this is where."* **It broke exactly there, and this audit
broke it independently.** That is correct labelling of a conjecture, not an over-reach.

**Item 6, the sizing sentence.** Present, §6, in the ticket's own currency
`ε_spec = 3·d·q̄·n/(n+1)` with `d·q̄ = 1/3` today and `1/150` to close the wall. It states that
the ticket's *"milestone or wall-breaker"* instruction **cannot be obeyed as written** because
the gain is not a constant factor, and it gives both sizings with the condition each hangs on:
a **milestone** at `n ≤ 5` unconditionally, a wall-breaker **only** under the conjecture. The
sizing sentence exists, names its condition, and the condition is the one that failed.

*Prediction miss, recorded:* my `P7` predicted the correction would run **pessimistic**. It runs
**optimistic** — a smaller `ε_spec` is a smaller supply and therefore a *nearer* threshold, not
a further one. I had the direction of the inequality backwards. Scored `MISSED`.

**Item 7, no poset enumeration.** Confirmed at the code: `v2_disjunctive.disjunctive` iterates
`combinations(pairs_of(n), r)` — subsets of pairs — and transitivity is never imposed, only
*reported*. The branch family is a strict superset of real posets' comparability patterns,
which is what keeps the maximum an upper bound. **Independently corroborated:** my own `n = 5`
optimum lands on the non-transitive branch `{(0,2),(0,3),(1,4),(2,4)}`, which a poset
enumerator could not have reached and would have under-reported. No frozen-class sampling
occurs anywhere on the path to any number.

---

## 9. Defects of this instrument, and what I did NOT do

### Five defects of mine, kept in the source. Four were caught by my own controls firing against correct code.

1. **My simplex entered on the wrong sign of the reduced cost** (I used the maximisation rule
   inside a minimisation routine). The textbook LP returned `0` instead of `36` and an
   equality-constrained LP returned **`infeasible` with phase-1 residual `1`**. Caught by
   `selftesta41b7.py` before any audit number existed — and note the failure mode: a sign error
   produced a *false infeasibility*, which is precisely `P14`'s hazard, in my own code.
2. **My `>=`-row selftest expected `20` where the answer is `17`.** A negative control of mine
   **failed against a correct solver**, whose dual then verified at `17`. `x ≥ 3` is a floor on
   `x`, not a ceiling on `y`. Corrected and recorded rather than quietly retuned.
3. **My row builders emitted vacuous `0 = 0` rows.** The P13 guard reported **214 of 219**
   branches as DIFFER against a system that was in fact identical. **The guard fired against my
   own code and `mg-200d`'s was right.** Had I trusted the guard's first verdict I would have
   filed a false finding about the constraint matrix — the single most load-bearing check in
   my brief.
4. **`a6_instrument.py`'s M4 asserted the `slot_le` surrogate for the two-atom law**, a measure
   outside the hypothesis the surrogate is claimed on. It failed against correct code. This is
   the same shape of error this arc keeps recording — asserting a conclusion about an object
   its hypothesis excludes — committed by the auditor checking for it. Re-pointed at
   `uniform L(P)`, with the wrong version documented at the call site.
5. **`a5_construction.py` first called `L.perms(20)`** — it tried to enumerate `S_20` and
   produced *no output at all* for forty minutes rather than an error, which is indistinguishable
   from a slow correct run. Replaced with a sparse reporter that never materialises `S_n`.
6. **`a8_downstream.py` checked `mg-00a1` against `n(n+5)/36` at every `n`** — the form printed
   in its banner and column header — where its `witness_target` is **parity-split**. My control
   then reported **10 failures against a correct witness**, one at every odd `n` from 5 to 23,
   in a differential audit whose whole purpose was to find a defect in a live result. **The
   even/odd pattern of the failures is what saved it**: a defect that lands on exactly one
   residue class is a bug in the *checker*, not in the checked. Had I filed it, I would have
   attacked a live negative with an error of my own — the exact failure this audit stage exists
   to prevent, committed by the auditor.

### NOT DONE — declared, not discovered later

* **I did not read `mg-131e`, `mg-eaa1`, `mg-00a1`, or `bb0d7e9`**, and did not reconcile
  against any of them. My `n = 6` refutation is independent of theirs.
* **The `n = 6` exhaustive maximum is incomplete.** Levels `|I| = 6..10` are done
  (`11/6`, `5/3`, `5/3`, `5/3`, no feasible branch); levels `11..15` were still running at
  write-up. `V_6 ≥ 11/6` is established and the refutation does not depend on the rest, but
  **`V_6` itself is not determined here** and I do not assert it.
* **I did not reach `Θ(n²)` independently and make no claim about the growth rate.** My family
  (§6.2) is a lower bound of shape `(n−1)/3 + k/6`; `mg-00a1`'s witnesses, which I *checked*,
  are much stronger. Checking a witness is not reproducing a verdict, and I did not read
  `mg-00a1`'s argument.
* **I did not attempt the true growth rate.** My family is a **lower bound** and says nothing
  about whether the disjunctive value is `Θ(n)`, `Θ(n²)` or otherwise. Anyone reading a rate
  out of §6.2 is reading something that is not there.
* **I did not verify `mg-200d`'s Theorem 2.1** (all-pairs symmetry holds for `uniform L(P)` iff
  `P` is an antichain), nor its nine hand-named posets, nor its `S3`/`S5`/`S6` controls.
* **I did not check its §8.2** unit correction to `mg-6bc2`'s §5 table, nor its `n = 6`
  branch-free runs, nor anything about the **footrule** objective.
* **I did not run any of `mg-200d`'s scripts and did not read its transcripts.** Every number
  in this document comes from `code/perslot_audit_a41b7/`, with the single exception of the row
  comparison in §3, which is an assertion about my rows.
* **Every LP here is `n ≤ 6`**; the construction reaches `n = 20` and the family `n = 12`. Every
  `n`-growth statement in this audit is therefore a **direction**, not a theorem.
* **No edit to `STATE.md`, to `mg-200d`'s deliverable, or to `mg-6bc2`'s.** This audit is a
  finding, not a landing. In particular I do **not** propose striking anything: `mg-372e` has
  already struck the `2/(n+1)` sites, and `mg-200d`'s own conditional labelling was correct
  before it did.

---

## 10. Predictions, scored

Committed at `3c5ed10`. `[REPRO]` marks a figure my dispatch prompt had already handed me
(`PREDICTIONS.md` §0, H1–H8) — those are reproductions and may not be scored as hits.

| # | outcome | note |
|---|---|---|
| P1 | **HELD**, with a note | exact `Fraction` throughout; one latent float path that does not bite (§7) |
| P2 | **HELD** | the value is not from the literal form; the literal form is empty |
| P3 | **HELD** | `mg-200d` reports the infeasibility itself, and predicted it in advance |
| P4 | **HELD** | the weakening is disjunctive: a max over `2^C(n,2)` branches |
| P5 | **[REPRO] HELD** | `2/3, 1, 4/3` reproduced exactly, with dual certificates |
| P6 | **HELD** | no poset enumerated anywhere on the path |
| P7 | **HELD on existence, MISSED on direction** | the sizing sentence exists and names its condition; I predicted the correction runs pessimistic and it runs **optimistic** (§8) |
| P8 | **HELD** | the growth statement is marked a conjecture **at the claim**, not asserted for all `n` |
| P9 | **HELD** | my brief's item-2 premise is false and traces to `mg-6bc2`'s struck figure (§0) |
| P10 | **REFUTED, and this is the finding** | I predicted I would fail to beat the bound. I beat it at `n = 6` and then at every `n` to 12 (§6) |
| P11 | **HELD** | every optimum is exhibited by an explicit measure, verified by substitution |
| P12 | **did not fire** | there is no defect in `mg-200d` to classify: the statement I refuted is one it had already marked unproven |
| P13 | **guard bound and FIRED — against my own code** | 214/219 false DIFFERs from my vacuous `0=0` rows; `mg-200d`'s rows were right (§9 defect 3) |
| P14 | **guard bound and LOAD-BEARING** | `NC1` distinguishes infeasible from optimum-0 in all four arms, and caught defect 1, which was a *false infeasibility* in my own solver |

**Score: 10 held, 1 refuted (and it is the finding), 1 half-missed, 1 did not fire; both
pre-filed errors fired and both fired against me rather than against `mg-200d`.**
