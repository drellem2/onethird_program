# `lib2de0.E_leak` — THE DEFECT IS REAL, THE DEFINITION WINS, AND EXACTLY ONE PUBLISHED FIGURE MOVES

*mg-8311. Instrument: [`code/eleak_repair_8311/`](../code/eleak_repair_8311/). Predictions
committed before any script of this instrument existed:
[`PREDICTIONS.md`](../code/eleak_repair_8311/PREDICTIONS.md).*

---

## 0. The result, and the figure correction, first

⚠️ **A PUBLISHED FIGURE MOVED.**
[`OneThird-Direct-Prefix-Route-mg-2de0-Audit.md:202`](OneThird-Direct-Prefix-Route-mg-2de0-Audit.md)
said `Φ* ≤ min_k Δ₁(A_k)` is **`strict on 65 of them`**. It is **`strict on 16 of them`**.
`65` was wrong when that document was published. The same figure was carried at
`code/direct_prefix_audit_2de0/out_a3_nonvacuity.txt:80`
(`strictly smaller on 65 of 431 posets; EQUAL on 366`) and cited by number in
`selftest2de0.py` and `out_selftest_2de0.txt`. **All four sites are corrected.** They are the
only four; the ledger is in §5.3 and it was built by grep and read, not assumed.

**The defect.** `lib2de0.E_leak(A)` computed `|A| − |A ∩ set(p[:|A|])|` — the first `|A|`
**positions** — where `Δ₁(A) = E|A∖σ(A)| / min(|A|,|Aᶜ|)` (`STATE.md:41`) needs the positions
**indexed by** `A`. `phi_star()` called it on every subset. Found by mg-76b2 beside its `C₃`
work, correctly judged outside that ticket's scope, and offered rather than silently repaired
([`OneThird-C3-PrefixCapture-mg-76b2.md`](OneThird-C3-PrefixCapture-mg-76b2.md) §8).

**Confirmed independently, not adopted.** The 2-chain witness reproduces by hand. The
divergence re-derives to **8178 of 11316** `(poset, cut)` pairs at `n ≤ 5` from an enumerator
and leak functions that import neither `lib2de0` nor `lib76b2` — and carried to `n = 6`,
**259702 of 310404 (83.7%)**.

**The ruling is for the DEFINITION, and not because it is the definition.** The convention is
**not a conductance**: it violates `|A∖σ(A)| = |Aᶜ∖σ(Aᶜ)|` on **457132 of 683656**
`(permutation, cut)` pairs to `n = 7`, so *the cut did not determine its value* — and
`lib2de0.py`'s own docstring calls `Φ_P` "the same quantity, read as a **conductance**,
minimised over ALL cuts `A`". §3 gives all three grounds.

**And the honest other half: NO CONCLUSION OF mg-2de0 CHANGES.** Both halves of its `P9`
re-verify at `0 / 12702` and `0 / 431`. `A3.5` re-verifies at `0 / 6`. Every `Δ₁(A_k)` figure
— and therefore `2/3`, `1/2`, `√2`, `4/3` and everything in `A1`, `A2`, `A4`, `A5` — is
untouched. **Re-running mg-2de0's entire suite after the repair changed one line of one
transcript.** The instrument was wrong on 71.8% of its own inputs and its published verdicts
were right anyway; those are two claims and §5 measures them separately.

---

## 1. The witness, reproduced before anything was repaired

The ticket's instruction was to reproduce the 2-chain witness first and to **stop and report**
if it did not, because then the finding would be wrong and that would be the result. It
reproduced, by hand, in a six-line one-liner, before this instrument's first file existed.

2-chain `0 < 1`. `L(P) = {(0,1)}`, one linear extension. `A = {1}`.

| reading | `σ(A)` | `\|A∖σ(A)\|` |
|---|---|---|
| positions indexed by `A` (the definition) | `{p[1]} = {1}` | **0** |
| `σ⁻¹(A)`, the other natural reading | `{1}` | **0** |
| first `\|A\|` positions (`lib2de0`) | `{p[0]} = {0}` | **1** |

**The ruling is a two-way choice, not a three-way one.** `|A∖σ(A)| = |A∖σ⁻¹(A)|` for every
`σ` and `A`, because `|A ∩ σ(A)| = |σ⁻¹(A) ∩ A|` — apply the bijection `σ⁻¹` to both members
of the intersection. Machine-checked at **0 exceptions on 695482** `(permutation, subset)`
pairs over all permutations to `n = 7` and **all `2ⁿ` subsets including `∅` and the full set**.
So `set(p[:|A|])` is not "the other reading of `σ(A)`" — it is neither reading. *(This is
mg-76b2's observation; the proof is re-derived here rather than cited.)*

---

## 2. The divergence, re-derived (`R2`)

The ticket forbids taking `8178 of 11316` from its own body, so it is not an input to any
script here. The population is reproduced first, so the denominator is not adopted either:
posets on `{0..n−1}` with the identity a linear extension, **grown-and-closed** (add one pair,
close, dedup) rather than `lib2de0`'s **masked-and-filtered** over `2^C(n,2)` candidates —
two algorithms, so agreement is a check.

| `n` | posets | cuts each | pairs | diverge | % |
|---|---|---|---|---|---|
| 2 | 2 | 2 | 4 | 1 | 25.0 |
| 3 | 7 | 6 | 42 | 18 | 42.9 |
| 4 | **40** | 14 | 560 | 329 | 58.8 |
| 5 | **357** | 30 | 10710 | 7830 | 73.1 |
| **n ≤ 5** | **406** | | **11316** | **8178** | **72.3** |
| 6 | 4824 | 62 | 299088 | 251524 | 84.1 |
| **n ≤ 6** | **5230** | | **310404** | **259702** | **83.7** |

The bolded `40` and `357` are the counts `lib2de0` prints in its own transcript; `5230` and
`310404` are the counts mg-76b2 prints in its. **All four reproduce exactly from this
instrument's disjoint enumerator** — so the denominator of this arc's whole `Φ` programme is
now confirmed from two independent enumerations. *(A check on mg-76b2's **population**, not on
its conclusion. `lib76b2` is never imported and `C₃` is not touched.)*

The smallest witness, found by this instrument's own search order (`n` ascending, then
relation-size, then cut-size) rather than quoted, **is** the 2-chain `0 < 1` with `A = {1}`.

**The defect gets worse with `n`, so `72%` understates it.** The fraction of cuts that are
prefixes of `e` is `(n−1)/(2ⁿ−2)` and decays exponentially, and prefixes are exactly where the
two readings agree.

---

## 3. THE RULING — the definition, on three grounds, stated before any code changed (`R3`)

### 3.1 The convention is not a conductance

`Φ_P` is a **cut** functional. mg-76b2's Lemma 3.2 is `|A∖σ(A)| = |Aᶜ∖σ(Aᶜ)|`, which makes it
one. Re-derived here on this instrument's own enumeration:

| | `\|A∖σ(A)\| = \|Aᶜ∖σ(Aᶜ)\|` |
|---|---|
| **definition** | **0** / 683656 |
| **convention** | **457132** / 683656 — first failure `n=2`, `σ=(0,1)`, `A={0}→0`, `Aᶜ={1}→1` |

*(all permutations `n = 2..7` × all `2ⁿ−2` proper cuts)*

Under the convention **the cut does not determine the value**, so "minimise over all cuts" is
not the well-posed operation the Cheeger argument consumes. This is the heaviest ground and it
is not an appeal to notation.

### 3.2 The definition is what the corpus's own matrix identity computes

The corpus identity (`Op-Form :220–227`, quoted at mg-76b2 Lemma 2.1) is
`⟨1_A,(I−S_P)1_A⟩ = E|A∖σ(A)|`. It has a **matrix** on one side and a **combinatorial count**
on the other, so it can arbitrate between two candidate counts. Derivation, so the machine is
checking something known: `S_P` averages permutation matrices with `(M_σ)[x,y] = 1` iff
`y = σ(x)`, and `⟨1_A,(I−M_σ)1_A⟩ = |A| − |A ∩ σ⁻¹(A)| = |A∖σ⁻¹(A)| = |A∖σ(A)|` by §1.

| | vs `⟨1_A,(I−S_P)1_A⟩` |
|---|---|
| **definition**, `n ≤ 5` | **0** / 11316 |
| **convention**, `n ≤ 5` | **8178** / 11316 |
| **definition**, `n ≤ 6` | **0** / 310404 |
| **convention**, `n ≤ 6` | **259702** / 310404 |

The convention fails the identity on **exactly** the pairs where it diverges from the
definition — the two counts coincide, which is the coherence one wants. `S_P` is built here
from `Pr[pos_σ(x)=i]` and symmetrised; **no eigenvalue is taken anywhere in this instrument**,
and mg-76b2's 310404-pair check of the same identity is **reproduced, not re-run**.

The convention has no such representation at all: `|A| − |A ∩ set(p[:|A|])|` is not a bilinear
form in `1_A`, because it reads `|A|` twice — once as a set, once as a **length**.

### 3.3 The convention is not load-bearing

Asked as the ticket asks it: *is any published assertion of mg-2de0 true under the convention
and false under the definition?* Evaluated on this instrument's own population:

| mg-2de0 assertion | convention | definition |
|---|---|---|
| (i) `Φ_P(A) ≤ 1` for every cut | 0 / 11316 | 0 / 11316 |
| (ii) `Φ* ≤ min_k Δ₁(A_k)` | 0 / 406 | 0 / 406 |
| (iii) `Φ* = min_k Δ₁(A_k)` at the antichain | 0 / 6 | 0 / 6 |

**Nothing mg-2de0 concluded requires the convention.** And the blast radius is bounded by
**parsing** rather than grepping — mg-4d3b recorded a source census that read its own prose as
code, and a grep for `phi_star` matches this document. An `ast` walk over mg-2de0's seven
`.py` files finds 42 sites; **9 reach `E_leak`, all through `phi`/`phi_star`, in exactly two
files** (`a3_nonvacuity.py`, `selftest2de0.py`). The prefix machinery (`K_k`, `E_K`,
`delta_1_prefix`) never routes through it.

### 3.4 What the convention actually *is*, named so it is not mistaken for sloppiness

`|A| − |A ∩ set(p[:|A|])|` measures **how far `A` is from being an initial segment under `σ`**.
That is a real quantity, and it is the natural generalisation of `K_k` in the direction of
*prefix-ness* instead of *function application* — which is exactly why the slip is an easy one
to make and why it agrees with `K_k` on every prefix. It is simply not `Δ₁` and not `Φ_P`.

### 3.5 Where the two readings agree — stated narrowly, with the guard that keeps it narrow

`A_k = {0,…,k−1}` **is** the set of the first `k` positions, so the readings agree on every
**prefix of `e`**: `0 / 34406`. This is filed in `PREDICTIONS.md` as **P14**, the slip I bet
35% on committing — the temptation is to state it as "they agree on prefixes" and let a reader
hear "intervals" or "suffixes". The guard is a measurement on the suffix of the same size:
**19530 / 34406 disagree.** The agreement is exactly as wide as *prefix of `e`* and no wider.

---

## 4. The repair

`lib2de0.Poset.E_leak` now computes `a - len(A & frozenset(p[i] for i in A))`. The docstring
carries the defect, the witness, the divergence count, the ruling and the moved figure, so a
reader meeting the function meets its history.

**The selftest now has drills that would have caught it** — `S7b`, five of them, **every one on
a NON-prefix cut**, because a drill that only tests prefixes cannot see this defect. That is
precisely why it survived a whole audit's two-sided closure: `selftest2de0.py`'s existing `Φ`
drills were all at the **antichain**, where §5.2 shows the two readings coincide at every cut.

**Verified by running the new drills against the old code**: 4 of the 5 go **RED**
(witness `1≠0`; cross-cut asymmetry; `576 / 864` asymmetric pairs; every cut of `chain n=4`
leaking `0`, which the old code gave as `0,1,1,1,0,1,1,1,1,2,0,1,1,1`), and the selftest exits
`1`. The 5th (`Φ*(chain n=4) == 0`) passes under **both** and is **recorded in the source as a
positive control that is NOT a detector**, so no reader counts it as evidence the repair
landed.

---

## 5. THE CONSEQUENCES — the actual deliverable (`R4`)

Measured on mg-2de0's **own** population: `named_posets(7) + all_posets(4) + all_posets(5)`,
imported from `lib2de0` so the poset list is certainly theirs, re-wrapped so the leak
arithmetic is certainly mine. Reproduces at **431 posets / 12702 cuts**. Both columns are
computed by `lib8311`, so `R4` prints the same before/after table whether the repaired or the
defective `E_leak` is on disk — the comparison cannot silently become before/before.

### 5.1 What did NOT move — and was never at risk, provably

| figure | published | convention | definition |
|---|---|---|---|
| `A3.2` / `P9` first half: `Φ_P(A) ≤ 1` | `0 / 12702` | 0 / 12702 | **0 / 12702** |
| `A3.4` / `P9` second half: `Φ* ≤ min_k Δ₁(A_k)` | `0 / 431` | 0 / 431 | **0 / 431** |
| `A3.5`: `Φ* = min_k Δ₁(A_k)` at the antichain | `0 / 6` | 0 / 6 | **0 / 6** |

These were forced, and the proofs were written by hand into `PREDICTIONS.md` (H5–H7) **before
this instrument existed**, so they are reported as reproductions and not as findings:

- **`Φ_P ≤ 1` under either reading.** The convention's leak is `|A∖P|` with `|P| = |A|`, so it
  equals `|P∖A| ≤ n−|A|`, and trivially `≤ |A|`; hence `≤ min(|A|,|Aᶜ|)`.
- **`Φ* ≤ min_k Δ₁(A_k)` under either reading.** `Φ*` minimises over a family containing the
  prefixes, where §3.5 measured the readings agreeing.
- **The antichain is a fixed point of the defect.** Over all `n!` permutations both `σ(A)` and
  `set(p[:a])` are uniform random `a`-subsets, so both leaks equal `a(n−a)/n`. Verified
  directly: the two readings **coincide at all 240 antichain cuts**, `n = 2..7`.

### 5.2 Therefore mg-2de0's Priority-2 arithmetic is untouched

`2/3`, `1/2`, `√2`, `4/3` are **all** evaluated at the antichain, and `A3.1`/`A3.3`/`A3.6`
report nothing else. `A1`, `A2`, `A4`, `A5` never compute `Φ` (`A4` mentions `Φ*` in prose
only). Every `Δ₁(A_k)` figure routes through `E_K`. **Confirmed by re-running the whole suite:
all 6 sections on their pre-registered exit codes, and `a1`, `a2`, `a4`, `a5` transcripts
byte-identical.**

### 5.3 What DID move — the ledger, and it is one figure at four sites

*Line numbers are **as published**, i.e. before this repair shifted them, so that a reader
auditing the correction can find each figure where it stood.*

| site | figure | moves? |
|---|---|---|
| `docs/…mg-2de0-Audit.md:183` | `Φ_P(A) ≤ 1` on all 12702 pairs | no |
| `docs/…mg-2de0-Audit.md:202` | `0 exceptions / 431 posets` | no |
| **`docs/…mg-2de0-Audit.md:202`** | **`strict on 65 of them`** | **YES → `16`** |
| `docs/…mg-2de0-Audit.md:204` | `Φ* = min_k Δ₁(A_k)` at the antichain | no |
| `code/direct_prefix_audit_2de0/README.md:60` | `P9 HIT (0 / 12702; 0 / 431)` | no |
| `…/out_a3_nonvacuity.txt:34`, `:77`, `:88` | the three `0 /` counts | no |
| **`…/out_a3_nonvacuity.txt:80`** | **`strictly smaller on 65 of 431; EQUAL on 366`** | **YES → `16` / `415`** |
| **`…/out_selftest_2de0.txt:73`** | cites `65 of 431` by number | **YES** |
| **`…/selftest2de0.py:147`** | the same citation in a source comment | **YES** |

**All four moving sites carry the same figure.** Nothing outside
`code/direct_prefix_audit_2de0/` and `docs/OneThird-Direct-Prefix-Route-mg-2de0-Audit.md`
carries a `Φ` figure from mg-2de0 — checked by grep across `*.md`, `*.txt`, `*.py`, `*.html`.
**`STATE.md` carries no `Φ*` number sourced from mg-2de0**; its mg-2de0 mentions are the `2/3`
prefix bound and `ε_leak ≈ 0.20`, and `2/3` is a prefix figure that cannot move. `STATE.md` is
therefore **deliberately not edited** — see §8.

### 5.4 How far the underlying quantity actually moved

The honest measure of blast radius, separate from what any verdict says:

- `E_leak` differs on **9116 of 12702 (71.8%)** of mg-2de0's own `(poset, cut)` pairs.
- `Φ*` changed on **65 of 431 posets (15.1%)**, **higher on all 65, lower on none**. Largest
  change `P28 n=4`: `1/10 → 2/5`.
- `{posets whose Φ* moves}` **is the same set as** `{posets mg-2de0 published as strictly
  smaller}` — which is why both counts read `65`. Forced once the direction is known:
  `Φ*_def ≥ Φ*_conv` and `Φ*_def ≤ m_pre`, so a moving `Φ*` implies `Φ*_conv < m_pre`. **The
  repair acts on exactly the posets A3.4's figure counts and on no others.**
- Of those 65, **49 flip `strict → equal`** and 16 stay strict. **None flip the other way.**

### 5.5 Why my own predicted direction was wrong, and the caution that is worth more than the prediction

`PREDICTIONS.md` **P9** bet 70% that the convention only ever **over**-charges, and inferred
the repair would *lower* `Φ*` and *raise* the strict count. **Both clauses lost**, and this is
the measurement that explains it rather than explaining it away:

| | conv `>` def | conv `<` def | equal |
|---|---|---|---|
| over all 12702 cuts | 6762 | 2354 | 3586 |
| **at the 431 cuts attaining `Φ*_conv`** | **0** | **102** | 329 |

The convention over-charges on the **majority** of cuts and under-charges, without exception,
at the cuts that **attain the minimum**. `Φ*` is an extremal statistic, so the population sign
carries no information about it — **an aggregate sign is not a bound on an extremum.** That
caution is the useful residue of a lost bet.

---

## 6. Predictions, scored (full text: [`PREDICTIONS.md`](../code/eleak_repair_8311/PREDICTIONS.md))

| # | prediction | conf | outcome |
|---|---|---|---|
| P1 | my independent recount lands on exactly `8178 of 11316` | 80% | **HIT** |
| P2 | poset counts `2, 7, 40, 357` | 90% | **HIT** |
| P3 | ruling to the definition, on the cut-symmetry and the identity, not on notation | 95% | **HIT** |
| P4 | identity holds for the definition, fails for the convention on > 2000 pairs | 85% | **HIT** (0 / 11316; 8178 / 11316) |
| P5 | `P9` first half unmoved, `0 / 12702` both | 97% | **REPRODUCTION** — forced by H6, scored as such |
| P6 | `P9` second half unmoved, `0 / 431` both | 97% | **REPRODUCTION** — forced by H7 |
| P7 | `A3.5` unmoved, `0 / 6` | 98% | **REPRODUCTION** — forced by H5 |
| P8 | `65 of 431` moves | 75% | **HIT** — it is `16 of 431` |
| P9 | and it moves **up**, because conv `≥` def pointwise | 70% | **MISSED, both clauses.** conv `<` def on 2122 / 11316; the count moved **down**, 65 → 16. Kept as written; §5.5 |
| P10 | `Φ*` moves on 150–350 of 431 | 50% | **MISSED** — 65. Kept as written |
| P11 | mg-2de0's three Priority-2 verdicts survive | 90% | **HIT** |
| P12 | nothing outside the two named locations moves; `STATE.md` has no `Φ*` from mg-2de0 | 85% | **HIT** |
| P13 | `run_all.sh` green first attempt after retargeting the `65` | 70% | **HIT** — 6/6 on pre-registered exit codes |
| P14 | *my likely error*: stating the prefix agreement too widely. Bet 35% | — | **NOT FIRED.** Guarded in advance by the suffix control of §3.5, which is the only reason that is checkable |
| P15 | *my likely error*: reporting a moved function as a moved verdict. Bet 30% | — | **NOT FIRED**, and it was the right thing to file: the instrument is wrong on 71.8% of its own inputs and **zero** published verdicts change. That contrast is where the overclaim would have gone |

---

## 7. Defects of this instrument, kept on the page

1. **A dead assignment in `r4_consequences.py`.** I wrote a name-prefix filter to pick the
   `n = 4` posets, decided it was the wrong population, replaced it with `all_posets(4)` on the
   next line — and left the first line in, computing a value that was then discarded. Found by
   re-reading my own source, not by any check. Removed. Recorded because a filter that looks
   used and is not is exactly how a wrong population gets published.
2. **One of my five new red drills is not a detector.** `Φ*(chain n=4) == 0` passes under the
   old convention too, because the chain's *prefix* cuts leak `0` either way and `Φ*` is a
   minimum. Found by running the new drills against the old code — the control I nearly
   skipped. It is kept in `selftest2de0.py` **with a note in the transcript saying it is not a
   detector**, so it cannot be miscounted as evidence.
3. **`_close()` has an unreachable guard.** It returns `None` if closure would need a
   non-upward pair, which cannot happen when every seed pair is upward. An untested branch,
   declared rather than trimmed, because trimming it would remove the assertion that the
   invariant holds.
4. **`R3.3` and `R4` measure the same three assertions on different populations** (mine, then
   mg-2de0's). That is redundancy, not coverage, and the second is the one that counts.

---

## 8. Not done, declared

- **`STATE.md` is not edited.** It carries no `Φ*` figure from mg-2de0, so there is nothing to
  correct; adding a row for a repair that moved no conclusion would overstate it. The four
  moving sites are all inside mg-2de0's own instrument and document.
- **mg-76b2's instrument and its `C₃ = 1` result are untouched**, per the ticket. `lib76b2` is
  never imported. Where this instrument checks the same identity mg-76b2 checked, it is a
  **second** instrument on the same population, and it confirms mg-76b2's **population and
  identity** — not its conclusion, which does not rest on `lib2de0`.
- **The Cheeger argument is not re-derived and `L2` is not attempted**, per the ticket.
- **`λ_std` is never computed.** `S_P` appears only as a matrix whose quadratic form is
  compared against a combinatorial count.
- **`n ≥ 7` is not measured.** `n = 6` was a declared stretch goal and it finished; `n = 7`
  would be `2^21` masks and `5040` linear extensions per poset and was not attempted.
- **`selftest2de0.py`'s pre-existing drills were not otherwise re-audited.** `S7b` was added;
  `S1`–`S8` are mg-2de0's and were left as they stand.

---

## 9. Claim ledger

| # | claim | § | label |
|---|---|---|---|
| 1 | the 2-chain witness is real: definition `0`, convention `1` | 1 | **CONFIRMED**, by hand then by machine |
| 2 | `\|A∖σ(A)\| = \|A∖σ⁻¹(A)\|`, so the ruling is a two-way choice | 1 | **PROVEN**, 0 / 695482 |
| 3 | divergence is `8178 of 11316` at `n ≤ 5`, `259702 of 310404` at `n ≤ 6` | 2 | **CONFIRMED INDEPENDENTLY** — the ticket's figure is not an input |
| 4 | the population `40 / 357 / 5230 / 310404` reproduces from a disjoint enumerator | 2 | **CONFIRMED**, 4 of 4 |
| 5 | the convention is not a function of the cut | 3.1 | **MEASURED**, 457132 / 683656 |
| 6 | the definition is what `⟨1_A,(I−S_P)1_A⟩` computes | 3.2 | **PROVEN** (derivation) + 0 / 310404 |
| 7 | the convention is not load-bearing for any published assertion | 3.3 | **CONFIRMED**, 3 of 3 in both columns |
| 8 | the readings agree on prefixes of `e` and **only** there | 3.5 | **PROVEN**, 0 / 34406 with a 19530 / 34406 guard |
| 9 | `THE DEFINITION IS CORRECT; E_leak IS REPAIRED` | 3 | **RULING**, on claims 5–7 |
| 10 | `P9` both halves, and `A3.5`, do not move | 5.1 | **REPRODUCTION** — hand-proved in `PREDICTIONS.md` before the instrument |
| 11 | `strict on 65 of 431` → `16 of 431` | 5.3 | **CORRECTED**, and the four carrying sites named |
| 12 | `Φ*` moves on exactly the 65 posets A3.4's figure counts, upward on all | 5.4 | **MEASURED**, set equality checked |
| 13 | an aggregate error sign is not a bound on an extremum | 5.5 | **MEASURED** (0 / 102 / 329 at the argmin) and it is why P9 lost |
| 14 | no conclusion of mg-2de0 changes | 5.2 | **CONFIRMED** — 6/6 sections, one transcript line moved |
