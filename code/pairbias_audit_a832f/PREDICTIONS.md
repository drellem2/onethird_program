# PREDICTIONS — mg-832f, INDEPENDENT AUDIT of the `eps_spec` derivation (mg-6bc2)

**Committed before any script of this audit exists and before one line of
`docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md` or
`docs/OneThird-PairBias-Independence-mg-345e.md` is read.**

## Provenance of what I read, named as the dispatch requires

`STATE.md` as I read it is the object at **blob `7f73bfc87b4bc4caab6c836f8c3922a2416863cf`**,
which is the version landed by commit **`491d42c79f7628c18cb7a5d197faa9f4600cd6c1`**
(mg-b488, *"eps_spec = 2/(n+1) IS ON THE PAGE AS FALSE, NOT AS A CONJECTURE"*) — verified
by `git log -1 --format=%H -- STATE.md` on `origin/main` returning exactly `491d42c`, and
by `git rev-parse origin/main:STATE.md` = `git rev-parse HEAD:STATE.md` = `7f73bfc8…`.
**The file has NOT moved since the dispatch note was written**; the SHA I name and the file
I read are the same object, and I name the blob as well as the commit because the commit is
what can be re-pointed and the blob is what cannot.

Worktree HEAD at the time of this pre-registration: `65866c2` (mg-8311).

---

## SECTION H — HAND MEASUREMENTS ALREADY MADE, DISCLOSED RATHER THAN LAUNDERED INTO PREDICTIONS

The brief's point 1 orders the re-derivation to happen **before** the parent's derivation is
read. I obeyed that literally: everything in this section was derived by hand from
`STATE.md`'s own statement of the premises, with `docs/…mg-6bc2.md` unopened. That means
these are **not predictions** — they are results, and scoring them as predictions would be
laundering. They are here so that the predictions below can be read at their true
information content.

**H1 — the master pair-bias inequality, re-derived from the premises in three ingredients.**
Frozen is `δ(P) < 1/3`: every incomparable pair is `>2/3`-decided toward `e`, i.e. for each
incomparable pair the probability that `σ` flips it against `e` is `< 1/3`. Then

>   `E[inv_e] = Σ_{incomparable pairs {x,y}} Pr[{x,y} flipped]  <  m/3  ≤  (1/3)·C(n,2) = n(n−1)/6`

with `m` the number of incomparable pairs. **The ingredient list is exactly three: (i) the
frozen hypothesis read per-pair; (ii) linearity of expectation; (iii) `m ≤ C(n,2)`.** No
poset structure beyond the definition of `inv_e`, no spectral input, no `L4`, no `C₃`. This
is a five-line derivation and I did not need the parent for it.

**H2 — the unit map, re-derived.** `ε_c3ca` is defined by `E[inv_e] ≤ ε·n²`
(`OneThird-LIBweak-mg-c3ca.md:172`) and `ε_spec` by `E[inv_e] ≤ (ε/6)(n²−1)` (row 8). Divide
H1 by each:

| divide H1's `n(n−1)/6` by | get | limit |
|---|---|---|
| `n²` | `ε_c3ca < (n−1)/(6n)` | `1/6` |
| `(n²−1)/6` | `ε_spec < 6·n(n−1)/(6(n²−1)) = n/(n+1)` | `1` |

and `ε_spec/ε_c3ca = 6n²/(n²−1) → 6`. **So `1/6` and `1` are one theorem divided two ways.**
I reproduce `STATE.md:15`'s map exactly, from the definitions, without reading mg-6bc2 §2.1.

**H3 — Claim 3.1's `≥` direction is a two-line construction and I built it.** Take
`μ* = (2/3)·δ_e + (1/3)·δ_{rev(e)}` on `S_n`. Every pair is flipped by exactly one of the two
atoms, so every pair's flip probability is exactly `1/3 ≤ 1/3` and `μ* ∈ M_n`; and
`E_{μ*}[inv_e] = (1/3)·C(n,2) = n(n−1)/6`, so `6E_{μ*}[inv_e]/(n²−1) = n/(n+1)` **exactly, at
every `n`**. Together with H1 this is `max{6E_μ[inv_e]/(n²−1) : μ ∈ M_n} = n/(n+1)`,
attained, both directions, all `n`. **This is the same two-atom law `STATE.md:135` already
names as obstruction 4** — so Claim 3.1's `≥` is not new mathematics, it is the file's own
standing counterexample re-pointed at the LP.

**H4 — a strictness gap I found while doing H3, and it is mine, not read.** `M_n` as
`STATE.md:15` defines it uses `≤ 1/3`. The **frozen hypothesis is `< 1/3`, STRICT.** Over the
strict class the value `n/(n+1)` is a **supremum that is NOT attained** (take
`(2/3+η)δ_e + (1/3−η)δ_rev`, which is frozen for every `η > 0` and tends to it). The closure
conclusion survives unharmed — no constant below `n/(n+1)` is provable from the strict
hypothesis either — but **"ATTAINED" is a property of the closed relaxation `M_n`, not of the
frozen class**, and a reader who takes "attained" as "a frozen configuration sits on the
bound" has been given a witness that is not frozen.

**H5 — the footrule `≤` is a corollary, not a second theorem.** Diaconis–Graham gives
`inv ≤ footrule ≤ 2·inv` (`STATE.md:29` records `ΣK_m ≤ inv ≤ 2ΣK_m` and `:30` the footrule
equivalence). Hence `3E[F]/(n²−1) ≤ 6E[inv]/(n²−1) ≤ n/(n+1)` by H1 alone. **Attainment,
however, needs `F = 2·inv` pointwise on the optimiser AND every flip at exactly `1/3`
simultaneously** — a DG equality case, which is why I expect the footrule attainment to be
finite-population where the inversion attainment is all-`n`, and why the two claims correctly
carry different kinds.

**H6 — realizability already bites at `n = 3`, computed by hand.** `tight3` = `{a < c}` with
`b` free. `L(P) = {abc, bac, acb}`, so `Pr[b before a] = 1/3`, `Pr[c before b] = 1/3`,
`δ = 1/3` exactly; the `≥2/3`-majority order is `e = abc`; `inv_e` is `0, 1, 1` on the three
extensions, so `E[inv_e] = 2/3` and `6E[inv_e]/(n²−1) = 4/8 = 1/2`. **Against `n/(n+1) = 3/4`
that is a factor `3/2` of headroom that realizability supplies for free at the smallest
non-trivial `n`.** (It also happens to equal `2/(n+1)` at `n = 3`, which is where I expect
mg-200d's refuted formula got its first point.)

**H7 — every attainment figure in this lineage is necessarily about the relaxation, and the
reason is on `STATE.md`'s own last page.** The frozen class `δ < 1/3` is **EMPTY for
`n ≤ 11`** (Peczarski 2006, refereed) and empty for `n ≤ 14` on the Gupta preprint
(`STATE.md:209`). So a machine confirmation "at `n = 3,4,5,6`" of Claim 3.1 **cannot contain a
single poset** — it is an LP fact about measures on `S_n`. mg-345e and mg-6bc2 both
*declare and refuse* poset enumeration on exactly that ground (`STATE.md:164`, `:167`).
**I intend to run the enumeration anyway**, over the nearest NON-empty realizable class
`δ ≤ 1/3` (non-empty: `tight3`), because it is the boundary family the frozen class is the
strict interior of, and because nobody in this lineage has measured it.

**H8 — the free bound, and the price of the theorem.** `inv_e(σ) ≤ m ≤ C(n,2)` **pointwise,
with no hypothesis at all**, so `ε_spec ≤ 6·(n(n−1)/2)/(n²−1) = 3n/(n+1) → 3` is FREE.
Pair bias moves `3n/(n+1)` to `n/(n+1)`: **a factor of exactly 3, which is exactly the `1/3`
of the hypothesis, transmitted once, linearly.** I did not read this anywhere; it falls out
of H1 the moment you write down what the bound is being compared against.

---

## SECTION P — PREDICTIONS PROPER

Scored HELD / MISSED / REFUTED against what I find. Predictions marked **(FORMALITY)** are
already settled by Section H and say so; they are recorded for completeness of the
comparison step the brief's point 1 demands, and they earn no credit.

### About the parent's mathematics

- **P1 (FORMALITY at the `≤`).** mg-6bc2's Claim 3.1 `≤` direction is H1 and nothing more —
  linearity of expectation against a per-pair `1/3`, then `m ≤ C(n,2)`. No spectral input,
  no `C₃`, no `L4`.
- **P2 (FORMALITY at the `≥`).** mg-6bc2's Claim 3.1 `≥` direction is H3's two-atom measure
  (masses `2/3`, `1/3` on `e` and `rev(e)`), or an affine relabelling of it.
- **P3.** mg-6bc2 does **not** state H4's strictness caveat — i.e. it does not anywhere
  distinguish the closed relaxation `M_n` (`≤ 1/3`, max attained) from the strict frozen class
  (`< 1/3`, sup unattained). Predict **ABSENT**, and predict `STATE.md` is silent on it too.
- **P4.** mg-6bc2's constant is **DERIVED, not the mg-3ce3 calibration in proof's clothes**.
  The `2×10⁻²` will appear in it only on the **demand** side (`ε_dem`), never as the value of
  `ε_sup`. **Brief point 4 will NOT fire.**
- **P5.** **Brief point 5 (inequality direction) will NOT fire on Claim 3.1**: `ε_sup < 1` is
  an upper bound on a constant that is better when smaller, and Claim 3.1's attainment is a
  *lower* bound on the best constant provable from pair marginals — both point the right way.
  Riskier half: I predict I find **at least one site in the corpus** where a
  supply-side `ε` and a demand-side `ε` are compared without the direction being stated.
- **P6.** The `L4` gate was respected by **disjunct (b)** — the parent showed / inherited from
  mg-345e that the pair-bias route is L4-INDEPENDENT — and **not** by answering L4's modulus
  question, which `STATE.md:118` still records as OPEN. Predict **HELD**, and predict I can
  confirm the independence *by construction* (H1's ingredient list) rather than by citation.
- **P7.** mg-6bc2 does **not** bend toward `1/6`: in `ε_spec` units it lands on `n/(n+1) → 1`
  and says in as many words that `1/6` there would be `6×` stronger. **Brief point 6 will NOT
  fire.** *(Low information — `STATE.md:15` already summarises this and I have read it.
  Disclosed as such.)*
- **P8.** The parent's document still prints `ε_spec = 2/(n+1)` as a live value in its §5.1
  "what it buys" table. *(REPRODUCTION, not a finding — `STATE.md:168` says so explicitly.
  Disclosed. What I am actually predicting is the **count**: I predict **2 to 6** live sites
  of `2/(n+1)` across `docs/…mg-6bc2.md`.)*

### About the measurements I am going to make

- **P9.** My own poset enumerator returns **1, 2, 7, 40, 357, 4824** naturally-labelled posets
  at `n = 1…6`, the `n = 6` entry matching the `4,824` `STATE.md:42` attributes to mg-c4f5.
  *(This is a movable number and a real cross-check of an independently-written enumerator
  against a figure already on the page.)*
- **P10.** Over the realizable class `δ(P) ≤ 1/3`, `max 6E[inv_e]/(n²−1)` is **strictly below
  `n/(n+1)` at every `n ∈ {3,4,5,6}`** — realizability bites at every `n` I can reach.
  *(At `n = 3` this is a FORMALITY: H6 already gives `1/2 < 3/4`.)*
- **P11.** That realizable maximum is **non-increasing in `n`** over `n = 3,4,5,6`, and its
  `n = 4,5,6` values are **strictly below `1/2`**. *(Genuinely risky — I have computed only
  `n = 3`.)*
- **P12.** The realizable class `δ(P) ≤ 1/3` is **non-empty at every `n` from 3 to 6**, and
  every member of it has `δ = 1/3` **exactly** (never `< 1/3`), because the 1/3–2/3 conjecture
  is verified to `n = 11`. Predict `0` posets with `δ < 1/3` found, at every `n ≤ 6`.
  **If this prediction MISSES I have refuted the 1/3–2/3 conjecture, so a MISS here is far
  more likely to be a bug in my enumerator than a discovery, and I will treat it that way.**
- **P13.** I can construct, by my own search on the branch `STATE.md:167` names, a feasible
  measure at `n = 6` with `E[inv] > 5/3 = (n−1)/3`, independently re-deriving mg-131e's
  refutation of `ε_spec = 2/(n+1)`. Predict the optimum I find on that branch is **exactly
  `11/6`**.
- **P14.** The trivial/free comparison of H8 is **not stated anywhere in `STATE.md` or
  mg-6bc2**: predict `0` sites saying the pair-bias theorem's entire content is a factor of 3
  off a hypothesis-free bound. *(If this HOLDS it is material beyond the brief; if it MISSES,
  I have merely re-derived something already recorded and must say so.)*

### My two most likely errors, filed in advance

- **P15 — I mis-specify `e`.** `e` is the `>2/3`-majority order, not the poset's natural
  labelling and not "some linear extension". For a poset with `δ > 1/3` the `≥2/3`-majority
  tournament is **incomplete**, so `e` does not exist and `inv_e` is undefined; if my code
  silently falls back to the natural labelling I will print numbers that are not `ε_spec` at
  all and they will look plausible. **Guard, bound now so I cannot tune it later: I will
  ASSERT that the `≥2/3`-majority relation is a complete transitive tournament on every poset
  I report a number for, and I will let that assertion crash rather than fall back.**
- **P16 — I score a change of units as a discovery.** The single most likely way this audit
  goes wrong is that I write up *"pair bias does not give `1/6` in `ε_spec` units"* as a
  finding when it is `STATE.md:15`'s own headline, already landed by mg-9adf. **Guard: my
  verdict block must separate CONFIRMED-BY-INDEPENDENT-RE-DERIVATION from NEW, at every
  numbered item, and anything that appears in `STATE.md` at blob `7f73bfc8…` is
  CONFIRMED-BY-RE-DERIVATION and never NEW, however I arrived at it.**

### Negative controls I bind myself to run

- **NC1.** Feed the checker three deliberately wrong closed forms for the `M_n` maximum —
  `2/(n+1)` (mg-200d's refuted value), `n/(n+2)`, and `(n−1)/(6n)` (the `ε_c3ca` value put in
  the wrong currency, i.e. the exact unit-mismatch this lineage has now committed twice) —
  and require **all three to be REJECTED** at some `n ≤ 6`. If a wrong form survives, my
  checker is vacuous and the agreement of the right one means nothing.
- **NC2.** Run the enumeration's `δ` computation against `tight3` and against the 3-element
  antichain, whose `δ` I know by hand to be `1/3` and `1/2`. Require both exact.
- **NC3.** Verify the two-atom witness is genuinely **in** `M_n` by checking all `C(n,2)` flip
  probabilities at `n = 3…8`, not by asserting it — a witness that is out of the feasible set
  proves the reverse of what it is offered for, which is this arc's most repeated defect
  shape.

### Pre-committed verdict shape

- **P17.** I predict the verdict is **CONFIRMED WITH CORRECTIONS** — the algebra holds, the
  gate holds, and the corrections are about **what the result is worth and what "attained"
  attaches to**, not about arithmetic. I record now that if I find myself writing a REFUTED
  verdict on the algebra, I have almost certainly made an error, because H1–H3 are five lines
  each and I have already checked them.

---

*Committed by mg-832f before any script of this instrument exists.*
