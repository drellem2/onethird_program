# OneThird — INDEPENDENT AUDIT of mg-5ce3's landing of mg-c4f5 §5.3 into STATE.md

**Auditor:** mg-3e06 (pre-filed in the same action as mg-5ce3, started only after it landed).
**Parent:** mg-5ce3, commit `4ef64d7`, one file, `4 insertions(+), 4 deletions(-)`.
**Source of the claim:** `docs/OneThird-LIBweak-mg-c4f5-IndependentAudit.md` §5.3.

## 0. Verdict

**CONFIRMED — the strengthening is right, it did NOT overshoot, and the guard survived.**
All four brief checks pass. **The four sites carry a scope qualifier in their own sentence,
including the mermaid label I predicted would drop it**, and the landed page is *more* careful
than both the ticket that commissioned it and, at one point, than §5.3 itself.

**The file I read: STATE.md at commit `491d42c79f7628c18cb7a5d197faa9f4600cd6c1`, blob
`7f73bfc87b4bc4caab6c836f8c3922a2416863cf`.** This matters more than usual here: **`4ef64d7`
is an ANCESTOR of `491d42c`** — mg-b488 rewrote STATE.md *after* mg-5ce3 landed. mg-5ce3 could
not have verified its own survival past that rewrite, and its commit subject makes no claim
about it. **That survival check is the one thing this audit contributes that no parent could,
and everything survives: 6/6 guard components, 4/4 sites.**

One finding, and it is **not** against the conclusion:

> **§5.3's own witness is not a realizable `E[inv_e]`.** `inv_e` counts *incomparable* pairs,
> so `E[inv_e] ≤ n(n−1)/2` for every `n`; §5.3's `g(n) = n²` exceeds that ceiling at
> **5000/5000** of `n ∈ [1,5000]`, and exceeds the *frozen* ceiling `m/3 ≤ n(n−1)/6` by ≈6×.
> The witness is a **function**, not a poset family. **I repaired it and the negative
> survives**: `g(n) = n(n−1)/6·(1−10⁻⁶)` below `N₀` sits under the frozen ceiling at every `n`
> and still violates (LIB-const) throughout `[2, N₀)` at all five `N₀` tested. So §5.3's
> conclusion does not depend on its unrealizable witness — but the page prints that witness in
> `E[inv_e]` notation, and a reader may take it for an attainable value.

## 1. Check 1 — §5.3 RE-DERIVED, AND THE VIOLATOR BUILT

§5.3 verbatim, from the source (not from mg-5ce3's rendering, and not from the ticket's):

> `f(n) = n²/log₂ n` is `o(n²)`, and `f(n) ≤ (ε_spec/6)n²` requires `log₂ n ≥ 6/ε_spec = 300`,
> i.e. **`n ≥ 2³⁰⁰ ≈ 10⁹⁰`** … And more strongly: for **any** `N₀`, `g(n) := n²` below `N₀` and
> `n²/log₂ n` above is `o(n²)` and violates (LIB-const) throughout `[1, N₀)`. **No `N₀` works
> for the class.** The quantifier gap is unbounded, not merely unquantified.

**It supports the strong reading.** The quantifier is explicit (`for **any** N₀`), the
conclusion is scoped (`for the class`), and it is a statement of *non-existence*, not of
ignorance. **P1 HIT.**

**I did not take §5.3's instance.** The content is a lemma, and the instance is decoration:

> **(LIB-weak) is an asymptotic hypothesis and is therefore invariant under modification on a
> finite prefix. (LIB-const) is a pointwise inequality and a finite prefix can violate it
> outright.**

So *any* `o(n²)` tail, redefined below `N₀` to exceed the bound, is a counterexample. I built
**4 prefixes × 5 tails**, sharing no line with §5.3's pair, in exact `Fraction` arithmetic with
no float on any decision path and `log₂` never evaluated numerically (every statement about
`log₂ n` reduced to an integer comparison against a power of 2):

- tails: `n²/log₂ n`, `n²/log₂log₂ n`, `n²/√(log₂ n)`, `n^{3/2}`, `0` (the n-chain)
- prefixes: `n²`, `n(n−1)/2` (pair ceiling), `n(n−1)/4` (antichain, uniform), `n(n−1)/6·(1−10⁻⁶)` (just under the frozen ceiling)

**40/40** (prefix × bound-form × `N₀`) combinations violate (LIB-const) throughout `[2, N₀)` at
`N₀ = 15, 100, 900, 10⁶, 10¹⁸`, under **both** renderings of the bound — §5.3's `(ε/6)n²` and
STATE.md's `(ε/6)(n²−1)`. **The negative holds, and it holds for reasons far more general than
the witness §5.3 chose. P2, P3 HIT.**

*(Cap disclosed rather than hidden: `n` is capped at 4000 values per `N₀`, so the `10⁶` and
`10¹⁸` columns are sampled prefixes, not exhausted.)*

### 1.1 The realizability gap — the one finding

`inv_e` counts **incomparable** pairs (mg-c3ca:75), so `E[inv_e] = Σ_{incomparable pairs}
Pr[inverted] ≤ n(n−1)/2`, and under (LIB-weak)'s own frozen antecedent `E[inv_e] < m/3 ≤
n(n−1)/6` (mg-c4f5 §5.2). Measured:

| `n` | `g(n) = n²` | pair ceiling | frozen ceiling | over pair? | over frozen? |
|---|---|---|---|---|---|
| 2 | 4 | 1 | 1/3 | YES | YES |
| 10 | 100 | 45 | 15 | YES | YES |
| 900 | 810000 | 404550 | 134850 | YES | YES |

**5000/5000** of `n ∈ [1,5000]`; there is no `n` at which `n²` is an attainable `E[inv_e]`.
**Repaired witness, checked:** prefix `n(n−1)/6·(1−10⁻⁶)` is under the frozen ceiling at
**13/13, 98/98, 898/898, 4000/4000, 4000/4000** and violates (LIB-const) at the same counts.
**The negative survives the realizability objection.** This was not predicted by me and is not
a defect in the conclusion — it is a defect in the *illustration*, inherited by the page.

### 1.2 Both §5.3 figures, exact

`6/(2×10⁻²) = 300`; first `n` is exactly `2³⁰⁰`, which has **91** decimal digits, and
`2³⁰⁰ < 10⁹⁰·√10`, so nearest is `10⁹⁰` — **the page's `10⁹⁰`.** Checked from both sides,
integer-only: `log₂(2³⁰⁰−1) ≥ 300` is **False**, `log₂(2³⁰⁰) ≥ 300` is **True**.
`6/(2×10⁻⁴) = 30000`; `2³⁰⁰⁰⁰` has **9031** digits and `2³⁰⁰⁰⁰ ≥ 10⁹⁰³⁰·√10`, so nearest is
**`10⁹⁰³¹`** — the page's figure, under a consistent nearest convention. **P5 HIT.**

**Exactness note, NOT a defect and flagged as such:** under the `(ε/6)(n²−1)` form STATE.md
actually prints, at `n = 2³⁰⁰` the LHS exceeds the RHS by exactly `1/300`, so the first
satisfying `n` is `2³⁰⁰ + 1`. A shift of 1 in an object of size `10⁹⁰`. The `≈10⁹⁰` is
unaffected and nothing on the page needs changing.

**P6 HIT — `ε_spec = 2×10⁻²` is not the refuted `2/(n+1)`.** Per the mayor's note I say where I
saw it: `2/(n+1)` occurs at **STATE.md:167–168 only**, in the attempt-index rows where mg-b488
landed its refutation, correctly marked. It occurs at **none** of mg-5ce3's four sites and
**0 times** in §5.3. §5.3's `2×10⁻²` is the calibrated scalar target, a different object.

## 2. Check 2 — DID IT OVERSHOOT?  No.

Two things §5.3 does **not** prove, which a site must not assert:
**(X)** no single (LIB-weak) family has a threshold of its own; **(Y)** (LIB-const) never holds.

**Every site carries a scope qualifier inside its own sentence:**

| site | qualifier found |
|---|---|
| line 15 (one-paragraph state) | `FOR THE CLASS`, `from the o(n²) hypothesis` |
| line 23 (Axis 1) | `for the class`, `from the hypothesis` |
| line 64 (mermaid label) | `for the class` |
| line 115 (ledger row 8) | `for the class`, `FOR THE CLASS`, `from the o(n²) hypothesis` |

**0 occurrences of any (X)/(Y) phrasing at any site.** Row 8 carries the rider explicitly —
*"a single family satisfying (LIB-weak) does have some threshold of its own"* — and, better
than that, **names the surviving route**: *"Only a rate would give one ((LIB)'s `O(n)`, or
`o(n²)` carrying an explicit modulus)."*

**My principal live bet LOST and I report it as a loss. P8 MISS (predicted 0.40).** I named the
mermaid label as the most likely offender because mg-5ce3's own subject said it was "kept
short", and short is exactly the pressure that drops qualifiers. It kept the qualifier.
**P9 MISS too**, in the same direction: I bet the implication-vs-programme-use distinction
would arrive as a by-product. It was drawn deliberately and the route is named.

### 2.1 Where the closure does and does not reach — the number the page points at

§5.3 quantifies over the class of `o(n²)` **functions**. The programme's object is the
**frozen poset** class. These differ, and the difference is decidable in one direction: **if
the frozen class satisfies LIB (`E[inv_e] ≤ Cn`) — which mg-c3ca §6 reports the reachable data
as saying — then an `N₀` DOES exist for the frozen class.** Computed here:

| `C` | smallest `n` with `Cn ≤ (ε_spec/6)(n²−1)` |
|---|---|
| 1 | **301** |
| 2 | 601 |
| 10 | 3001 |

**This does not contradict §5.3 and it does not contradict the page** — it is precisely row 8's
"what it does not claim", and `301` is the number row 8's *"only a rate would give one"* points
at. It sits inside the live range (`n ≥ 100` primitive, `n ≈ 900` crossover). Recorded because
the short sites say *"find `N₀` is closed, not open"*, and **the reading that must not be
welded to them is "finding `N₀` for the frozen class is closed"** — that one is open, and the
page says so where it has room.

## 3. Check 3 — THE SITES, EACH ON ITS MERITS

| | occurrences | lines | per line |
|---|---|---|---|
| pre (`4ef64d7^`) | **6** | 15, 23, 64, 115, 207 | 115 carries **two** |
| post (`4ef64d7`) | 3 | 23, 115, 207 | — |
| now (`491d42c`) | 3 | 23, 115, **209** | — |

The ticket said four; there are six occurrences on five lines. **P10 HIT.** mg-5ce3 changed
**4 lines** and removed **3 of the 6 occurrences** — its subject's phrase "landed at four of
STATE.md's six 'unspecified' sites" conflates lines with occurrences in the very sentence that
corrects the ticket for that conflation, though its next clause discloses the surviving one.
**Not a defect; a wording snag, and it is self-disclosed.**

**No blanket replace. P12 HIT.** Exactly lines `[15, 23, 64, 115]` differ; line count unchanged
at 208. A `sed` over "unspecified" would have taken all five lines.

**The three survivors are each a different use — but not for the reason the ticket predicted:**

- **line 23** — contrastive by design: *"the threshold is not \*unspecified\* but **underivable
  from the hypothesis**"*. The word is the thing being denied. Correct to keep.
- **line 115** — inside the attributed quotation of mg-d1a2's original reason. Correct to keep.
- **line 209** — **the ticket's premise fails here.** It is *not* "about a different `N₀`"; it
  names the same one explicitly (*"the `N₀` of `(LIB-weak) ⟹ (LIB-const)`"*). mg-5ce3 left it
  on two other grounds, both of which I verify and accept: it is mg-33f5 material this ticket
  was told not to re-open, **and its own sentence already carries §5.3 verbatim in the same
  parenthetical**, closing *"so **no `N₀` works for the class at all**"*. A reader there is not
  left with the weaker claim. **P11 — HIT on the substance, MISS on the stated reason.**

**Residue for a future ticket, explicitly NOT a defect of mg-5ce3** (which declined line 209 by
instruction and named it in its NOT DONE): at 209 the *weaker* reason still leads (*"that
threshold is unspecified, so the comparison is … UNDEFINED"*) with §5.3 appended
parenthetically — the mirror of the ordering mg-5ce3 corrected at row 8.

## 4. Check 4 — THE mg-d1a2 GUARD SURVIVED, AND IS NOW OVER-DETERMINED

Byte-for-byte substring tests over the whole file, never line numbers — bound in
`PREDICTIONS.md` P16 before the file was opened, because row 8 was edited by four tickets in
one day. **6/6 present at `491d42c`:**

| component | pre | now |
|---|---|---|
| `DO NOT CITE THE LITERATURE BOUND AGAINST THIS N₀` | ✓ | **✓** |
| `and that discharges nothing here` | ✓ | **✓** |
| mg-d1a2's original reason, kept | ✓ | **✓** |
| …and **attributed** to mg-d1a2 | ✗ | **✓** |
| the strengthened reason (`there is no threshold to exceed`) | ✗ | **✓** |
| `n ≥ 12` Peczarski 2006 / `n ≥ 15` Gupta 2026 | ✓ | **✓** |

**The instruction is untouched, the refusal is untouched, and the reason was strengthened
without deleting the old one.** I checked the subtler failure mode explicitly — a strengthening
can leave the instruction intact while replacing the reason, so that the guard falls if the new
reason ever falls. **It does not: both reasons are live and each is independently sufficient.**
The guard is over-determined, which is strictly better than it was. **P13, P14, P15 HIT.**

**Mermaid integrity** (line 64 was edited inside a diagram): all **5** edges well-formed, one
quoted label each, 2 quotes each, **no `|` inside any label**. Two commas were added; commas are
safe inside a quoted mermaid edge label.

## 5. Check 5 — not applicable

mg-5ce3 did **not** conclude that §5.3 fails to support the strong reading. It landed. So the
negative-audit branch of the brief is moot.

## 6. Predictions, scored

**HIT:** P1, P2, P3, P4 (they did start at `n = 2`), P5, P6, P7, P10, P12, P13, P14, **P15**.
**MISS:** **P8** (0.40, my principal live bet — no site overshot, and the mermaid label I named
kept its qualifier), **P9** (the distinction was drawn deliberately, not inherited).
**SPLIT:** P11 (right that leaving 209 is correct; wrong that the survivors are "a different `N₀`").
**Guards held:** P16 (every guard test was a byte substring; lines moved 207→209 and 115 stayed,
and I scored none of it as loss), P17 (I credit the audit's "for the class" over the ticket's
looser "NO N_0 EXISTS" — mg-5ce3 landed the stricter wording and said so), P18 (every
H1-contaminated check is tagged FORMALITY below and reported as a byte check, not a re-derivation).

**My exposure is disclosed, not laundered.** My first search returned `4ef64d7`'s essay-length
commit subject in full, before I wrote one prediction. It pre-answered checks 1, 3 and 4.
Those were tagged `[FORMALITY]` in `PREDICTIONS.md` and are reported here as **byte checks, not
independent rediscovery**. What is genuinely independent: the re-derivation of §5.3 from the
source document, the 4×5 violator matrix, the realizability ceiling, the exact-integer figures,
and the survival check past `491d42c`.

## 7. Six defects of my own, kept in the source

All six fired **against correct claims**, which is the point of keeping them:

1. My `o(n²)` ladder stopped at `2⁴⁰` and reported §5.3's own tail as **not** `o(n²)`. Ladder's
   failure, not the tail's — `n²/log₂ n` needs `n > 2^k` to reach `1/k`.
2. `len(str(2**30000))` raised `ValueError` (Python's 4300-digit int→str cap). Replaced with an
   integer-only binary-search digit count.
3. My pass criterion was "reaches `1/10⁶`", which **no** log tail can reach on any feasible
   ladder. NC3 fired against correct code; the criterion was the bug.
4. I then gated on an arbitrary `h(last) > 10·h(first)`, and `n²/log₂log₂ n` failed it
   (divisor runs 2..14 over the whole feasible ladder). **No finite ladder can establish
   unboundedness at all** — the honest position, now in the source: strict increase is
   necessary and is what the ladder decides (it is what kills the constant-divisor impostors);
   sufficiency is analytic and is *stated*, not measured.
5. My ladder straddled the prefix boundary, so composites with `N₀ ≥ 900` failed. That artifact
   **is the lemma**: `o(·)` is a tail property and cannot see a finite prefix. Ladder now starts
   above `N₀`.
6. My A11 regex required backticks around `N₀` and reported the mermaid label as carrying no
   class-scoped phrase — the label correctly omits backticks (they render literally in a
   diagram). A9 had already found `for the class` there by plain substring; the two disagreed
   and **the regex was wrong**, not the page.

Negative controls, after the repairs: **NC1** (`n²/2`) and **NC2** (`n²/1000`) correctly
rejected as not `o(n²)`; **NC3/NC3b** correctly accepted; **NC4** (a zero prefix) correctly
violates nothing, `0/98`.

## 8. WHAT I DID NOT DO

- **I did not re-derive the poset-side meaning of `E[inv_e]`, `λ_std`, or frozenness.** §5.3 is
  an argument about function classes and I audited it as one. My realizability ceiling uses only
  "a sum over incomparable pairs of probabilities is at most the number of pairs" and mg-c4f5
  §5.2's `m/3`, both taken **by reading**, not re-proved.
- **I did not determine whether the frozen class satisfies LIB.** §2.1's `N₀ = 301` is
  **conditional** on that, and mg-c3ca §6 is *reachable data*, not a theorem. I did not run a
  single poset. Nothing in this document asserts a frozen `N₀` exists.
- **I did not check whether `n²/log₂ n` is realizable as an `E[inv_e]` tail.** My repaired
  witness dodges the question by construction; §5.3's tail may or may not be attainable and I
  did not decide it.
- **I did not audit any other section of mg-c4f5**, and did not re-open line 209, the mg-33f5
  document, or `docs/OneThird-LIBweak-mg-c3ca.md:100` — all named by mg-5ce3 as out of scope and
  all still carrying the older reading, as it said.
- **I did not verify mg-5ce3's own machine counts** (`13/13, 98/98, 898/898, 4998/4998`); it
  committed no code, so there was nothing to run. My counts are my own and the first three
  coincide; my `10⁶` column is capped at 4000, theirs sampled 4998, so those two are not
  comparable and I do not compare them.
- **I did not render the mermaid diagram.** Integrity is checked structurally (quote balance,
  no unescaped `|`), not by a parser.
- **I edited no file of the programme.** This audit adds one document and one instrument
  directory and changes no claim on STATE.md.
