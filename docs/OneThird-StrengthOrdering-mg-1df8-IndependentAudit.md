# OneThird — INDEPENDENT AUDIT of the STATE.md strength-ordering correction (mg-1df8)

**Audited object:** `STATE.md` at commit
**`491d42c79f7628c18cb7a5d197faa9f4600cd6c1`** (blob `7f73bfc8…`, 210 lines,
82 559 bytes). `origin/main` was at `dafe759` when I read it; `491d42c` is the
last commit touching `STATE.md`, and it is the SHA the mayor named in the
dispatch. **It had not moved when I read it, so I audited the named version.**

**The correction under audit:** `905526f` (mg-325c), later strengthened by
`4ef64d7` (mg-5ce3).

**Predictions:** `code/state_ordering_audit_1df8/PREDICTIONS.md`, committed at
`e57ae3b` before one byte of `STATE.md` was read. The mathematics instrument
was committed at `bca8e10`, **also before** the file was opened, so the
re-derivation is timestamped as independent rather than checked against the
parent.

---

## 0. Verdict

> **CONFIRMED. The ordering as it now stands in `STATE.md` is right, I reached
> it independently, and the quantifier gap sits WITH the claim at all three
> prose sites rather than one row away.** The correction did not reproduce its
> own defect class; there is no third inversion.
>
> **TWO MINOR FINDINGS**, neither touching the ordering.
>
> **AND THE BRIEF IS WRONG IN FOUR PLACES.** I was told to correct the framing
> and weight it down, so this is not a courtesy: obeying checks 4 and 5
> literally would have made me file findings against *correct* sentences and
> re-introduce a refuted claim.

**Checks 1–6, as dispatched:**

| # | check | result |
|---|---|---|
| 1 | re-derive the ordering | **CONFIRMED** — and the brief's rendering is imprecise, see §1 |
| 2 | "differ in kind" visible | **PASS** — at all 3 prose sites, in their own contiguous unit |
| 3 | quantifier gap sits with the claim | **PASS** — 3/3 prose sites; not a cross-reference |
| 4 | neither-proved-nor-blocked survives | **PASS** — and the brief's premise is superseded |
| 5 | mg-c3ca unaudited / has mg-c4f5 run | **BRIEF STALE** — mg-c4f5 ran; its verdict outranks, and `STATE.md` is right to say AUDITED |
| 6 | diff the mathematics | **PASS** — 0 theorem statements move; only characterisations |

---

## 1. Check 1 — the ordering, re-derived from the definitions alone

Instrument: `code/state_ordering_audit_1df8/m1_ordering.py`
(output `out_m1_ordering.txt`). Exact `Fraction`s, no float on any decision
path. **The symbol `<` appears nowhere in it**, deliberately: "stronger" for a
*hypothesis* is the reverse of "larger" for a *bound*, and this arc has already
inverted on exactly that, so every result is an implication with a named
direction and every non-implication carries an exhibited witness.

| | statement | result |
|---|---|---|
| **R1** | `(LIB) ⟹ (LIB-weak)` | **HOLDS — but only if `γ = ω(1/n)`.** At `γ(n) = 1/n` the bound is exactly `n²` (ratio to `n²` identically 1 at every `n`), so it FAILS |
| **R2** | `(LIB-weak) ⟹ (LIB-const)` for all `n` | **FALSE.** Witness `E(n) = M·n^{3/2}`, `o(n²)` for every `M`, violating `(ε/6)(n²−1)` on a prefix |
| **R3** | some `N₀` works for the class `o(n²)` | **FALSE.** For any `N₀` and any `ε`, a member violating at `n = N₀` exists; `M` grows with `N₀` but is always finite |
| **R4** | `(LIB-const) ⟹ (LIB-weak)` | **FALSE.** `E(n) = (ε/6)(n²−1)` is a member with equality at every `n` and is `Θ(n²)` |
| **R6** | the surviving threshold | `N₀ ~ (6M/ε)²` — measured exactly at `37, 145, 577, 2305, 9217` for `ε = 1, ½, ¼, ⅛, 1/16`, tracking `(6/ε)²` to within `+1` |

Four negative controls fire, including **NC2** (a member that never acquires an
`N₀` at all, so "eventually" is not vacuous) and **NC4** (the deliberately wrong
direction is rejected). A bisecting `N₀` finder is cross-checked 5/5 against an
exhaustive linear scan.

### CONCLUSION, and it is the brief's direction

**`(LIB)` is strictly the strongest of the three. `(LIB-weak)` is stronger than
`(LIB-const)`.** The "opposite" that the brief says merged this morning would
have been wrong.

### CORRECTION 1 TO THE BRIEF — the ordering is not a chain

By **R2 + R4**, as *sets of functions of `n`* **`(LIB-weak)` and `(LIB-const)`
are INCOMPARABLE**: neither implies the other. The brief's
`(LIB) < (LIB-weak) < (LIB-const)` is defensible **only** under an *eventually*
/ growth-class reading. A reader who takes it literally is wrong in the second
direction.

**`STATE.md` is more precise than the brief that audits it.** All three sites
printing `⊊` carry the rider *"As asymptotic classes"* **in their own
contiguous unit** (T1, `m4_riders.py`, with a negative control proving the
detector is not vacuous). So my incomparability result — true as it is — **does
not convict this file**, and my own P17 guard forbids me scoring it as a
defect. mg-c4f5 §5.4 reached the same requirement independently and records the
same repair as landed.

---

## 2. Check 3 — THE QUANTIFIER GAP SITS WITH THE CLAIM

This is the check the brief says the whole failure turned on, so I bound myself
to the acceptance criterion **in advance** (P15): fix the site by line number,
quote the *contiguous byte range*, and score against that range alone — a
cross-reference **fails**, because that is precisely what already existed and
already failed.

`STATE.md` is written one-logical-unit-per-line, so the contiguous unit *is* the
line. `(LIB-weak)` appears on **5 lines: 15, 23, 64, 115, 209.**
Instrument `m3_sites.py`, **4/4 negative controls firing** — including NC1, the
actual pre-correction wording, which the detector correctly rejects, and NC3,
the "differ by a constant" misreading it must also reject.

| line | what it is | verdict |
|---|---|---|
| **15** | L1b blockquote, § *The one-paragraph state* | **CARRIES IT** |
| **23** | Axis 1 bullet | **CARRIES IT** |
| **115** | ledger row 8 | **CARRIES IT** |
| 64 | mermaid edge label | quantifier only — **acceptable, see below** |
| 209 | § *Literature status* | quantifier only — **acceptable, see below** |

The three prose sites each carry, inline and in the same sentence, all of:
(a) that `(LIB-weak)` does **not** supply the operative form, (b) that the gap
is a **quantifier**, (c) that the two **differ IN KIND, not by a constant**.
Row 8 is the fullest and says it in as many words:

> "**(LIB-weak) ⟹ (LIB-const) only for `n ≥ N₀`, and `N₀` IS NOT UNSPECIFIED:
> NO `N₀` WORKS FOR THE CLASS AT ALL** … **So it does *not* supply the constant
> form this row leads with.**"

**The cross-references are present but are not doing the work** — the substance
is inline at each site. That is the distinction the brief asked for and it
holds.

**Line 64** is a mermaid edge label. It carries the quantifier
(*"only for n ≥ N₀, and NO N₀ works for the class"*) and omits only "in kind".
It cannot assert the plain implication, which is the hazard; mg-5ce3 records the
label was kept short and pipe-free so the diagram parses. **Not a finding.**

**Line 209** is the literature row, not a site introducing `(LIB-weak)` as a
hypothesis. It retains the older word *"that threshold is **unspecified**"*, but
**the same parenthetical carries the stronger landed claim** (*"so no `N₀` works
for the class at all"*), and the conclusion it draws — that no finite bound
helps — is correct and, if anything, understated. mg-5ce3 disclosed leaving this
line as NOT DONE with its reason. **A known, disclosed, conservative residue —
not a finding.**

### Check 2 — "differ in kind" is visible

**PASS.** Every prose site says the words. `m1` R2+R4 confirm the substance:
one is a limit statement, the other a uniform-in-`n` inequality with an explicit
constant, and **no constant converts one into the other**.

---

## 3. Check 4 — neither-proved-nor-blocked, and no manufactured optimism

**PASS**, and the brief's premise is superseded.

`m4_riders.py` T3: line 15 says *"Not blocked"* and carries, **in the same
unit**, *"neither proved nor blocked"*, *"no route"* and *"undecided"*. Across
the whole file, **0 optimism markers** at any `(LIB-weak)` site.

The brief's *"its surviving threshold MOVES WITH n"* is present verbatim.

### CORRECTION 2 TO THE BRIEF — its check-4 premise is a refuted claim

The brief demands the text say *"mg-c3ca's forward vector's marginal form is
FALSE"*. **It is not false.** mg-c4f5 §4 showed the parent's refutation refutes
a *different statement* from the one it names: `p3_window.py` evaluates a
threshold condition, while the document names the *linear* form
`min(p,1−p) ≥ ⅓(1−TV)`, which has **0 counterexamples over 1 168 036 pairs at
`n ≤ 7`**. `STATE.md` therefore says **"undecided"** and prints the correction.
**Had I enforced the brief here I would have re-introduced a known error.**

Far from manufacturing optimism, the row prints the number that is closing on
the threshold that would kill it: `c*(n) = ½, ½, 5/12, ⅖, 7/20`, margin above ⅓
collapsing **1/6 → 1/60, a factor of exactly 10** (verified, `m2` C6). The one
wording note: *"falling"* is non-strict — the first two entries are equal. Not a
finding.

---

## 4. Check 5 — mg-c4f5 HAS run, and it outranks

**mg-c4f5 is `done`; its audit landed at `05a0061` (2026-08-07 01:49), 71
minutes after the correction I am auditing.** By the brief's own rule its
verdict outranks everything above.

### CORRECTION 3 TO THE BRIEF — check 5 is stale, and `STATE.md` is right

The brief says *"CONFIRM IT SAYS mg-c3ca IS UNAUDITED"*. `905526f` did say
exactly that (*"UNAUDITED — mg-c4f5 has not run"*) — correct when written. The
current file says **"mg-c3ca … is now AUDITED — mg-c4f5"**. That is the true
statement. **Obeying check 5 literally would have meant filing a finding against
a sentence that is right.**

**All three of mg-c4f5's findings against `STATE.md` are FIXED at `491d42c`** —
checked, not assumed:

| mg-c4f5 finding | status at `491d42c` |
|---|---|
| **1** — "forward vector's marginal form is **false**" | **FIXED** — now "status is **undecided**" + the correction printed |
| **3** — row 8 contradicts itself in one sentence ("closes **this row as phrased**") | **FIXED** — 0 occurrences; now "closes the **limit** rendering `λ_std → 1`" |
| **4** — `λ_std` glossary omits the reference order | **FIXED** — glossary now carries *"relative to a chosen reference linear extension"*, the `1/3` spread and 4 069/4 824 |

---

## 5. Check 6 — DIFF THE MATHEMATICS

**PASS. No theorem statement moves.** Word-level diff of `905526f` over
`STATE.md`: every `+`/`−` token is characterisation, qualification or
attribution. The three definitions pass through **byte-identical** —
`E[Σ disp²] = O(E[inv_e])`, `E[inv_e] = O(n/γ)`, `E[inv_e] = o(n²)` — and no
numeral changes.

### And every figure at these sites re-derives: 22/22

Instrument `m2_figures.py`. Exact arithmetic; the two big-integer figures are
cross-checked against exact decimal digit counts so no decision rests on a float.

- **Unit map** — `÷n² ⟶ (n−1)/(6n) ⟶ 1/6` and `÷(n²−1)/6 ⟶ n/(n+1) ⟶ 1`, ratio
  `6n²/(n²−1) ⟶ 6`: verified as **identities** at `n = 3,4,5,6,40`, not fits.
- **mg-5ce3's witness** — `13/13`, `98/98`, `898/898` violations at
  `N₀ = 15, 100, 900`: **reproduced exactly**.
- **`log₂ n ≥ 6/ε_spec = 300 ⟹ n ≥ 2³⁰⁰ ≈ 10⁹⁰`**, and `10⁹⁰³¹` at the
  superseded `2×10⁻⁴`: both correct, and **both use the same rounding
  convention** (round-to-nearest: `90.309 → 90`, `9030.9 → 9031`). Floor would
  give `(90, 9030)`; a mixed convention would have been a finding. It is not
  mixed.
- **Literature shortfalls** — `85`, `≥ 885`, `6 of 91 = 6.6%`, `0.67%`: all
  reproduce, including the dead zone `{9,…,99}` being exactly 91 orders.
- **mg-131e's refuted `2/(n+1)` vs the live `n/(n+1)`**: not a conflict —
  different quantities in the same units, and `2/(n+1) ≤ n/(n+1)` for all
  `n ≥ 2` as a max must dominate a particular value. **0 occurrences of
  `2/(n+1)` in `STATE.md` at `491d42c`**, so the in-flight mg-372e correction
  has nothing left to do in this file.

### The negatives carry their candidate space

The load-bearing negative — *"NO `N₀` WORKS FOR THE CLASS"* — is quantified over
**all** candidate `N₀` and proved by **explicit construction** at each, which I
re-derived independently before reading it. Row 8 additionally states the
complement it does *not* claim (*"a single family … does have some threshold of
its own — it is simply not a function of the hypothesis"*). That is a properly
bounded negative.

---

## 6. FINDINGS

### FINDING 1 — MINOR. `γ` is load-bearing in the ordering and is defined nowhere in `STATE.md`

`(LIB)` is written `E[inv_e] = O(n/γ)` at **lines 15 and 129**, and `γ` also
appears in mg-7ae7's rate `1 − λ_std ≤ C/(γn)`. **`γ` is not in the glossary** —
its 10 symbol rows are `δ(P)`, `Δ₁(A)`, `λ_std`, `inv_e(σ)`, `disp(x)`, `e`,
`frozen`, `primitive`, `R`, `log e(P)`. It is never given a value or an
`n`-dependence anywhere in the file.

**Why this matters here specifically:** by **R1**, the chain's *first* link
`(LIB) ⟹ (LIB-weak)` holds **only if `γ = ω(1/n)`**. At `γ(n) = 1/n` it fails
outright. So the ordering this ticket exists to fix rests on a property of a
symbol the file never defines.

**It is sound, and here is how I established that** — not by assuming it.
Line 209 gives the crossover as `18C/ε_spec`. My own closed form for the same
crossover, from the definitions, is `6C/(γ·ε)`. Equating them:

```
6C/(γ·ε) = 18C/ε    ⟺    γ = 1/3
```

and `γ = 1/3` is the **unique** value that reproduces `900C` (checked against
`γ = 1, ½, ⅓, 1/6` → `300, 600, 900, 1800`). `1/3` is an absolute constant, so
`γ = ω(1/n)` holds and the link is sound.

**But I recovered that by inverting a figure three sections away.** A reader who
meets `O(n/γ)` at line 129 cannot do this. Note also that line 23 renders the
same hypothesis **`inv_e = O(n)`, γ-free**, and line 131 says the `(B) ⟹ LIB`
derivation lands at `Cn`, "`γ`-free" — two renderings that coincide **only**
because `γ` is `n`-free, which is never stated.

**Suggested repair:** one glossary row for `γ`, or the clause "`γ` an absolute
constant" at line 129. **I did not make this edit** (see §8).

### FINDING 2 — MINOR. Line 15 carries both gaps without naming them as two

mg-c4f5 §5.1 names this as a live hazard *"because it is the shape in which this
material has been reaching people"*: there are **two** gaps here —

- **gap 1**, `(LIB-weak)` vs `(LIB-const)`: a **quantifier**;
- **gap 2**, `ε_sup` vs `ε_dem`: a **constant factor ≈ 50**;

and *"a relay of the form 'the residual is a constant (~50) **rather than** a
quantifier' is a category error"*.

**Line 15 carries both** — *"The published gap factor of ~50"* and *"The gap is
a QUANTIFIER and it is UNBOUNDED, not a constant"* — **1 316 characters apart in
one paragraph, with neither labelled as one of two distinct gaps.** `STATE.md`
names the two gaps as two **nowhere**: 0 occurrences of "two gaps" / "gap 1" /
"gap 2" in the file. So mg-c4f5 §5.1's recommendation has not landed.

**Mitigations, stated so the severity is not inflated:** each mention names its
own operands (`~50` is explicitly `ε_sup/ε_dem`; the quantifier sentence is
locally scoped to `N₀`), the separation is large, and **row 8 — the fullest
site — does not carry `~50` at all**, so the hazard is confined to one site.
**MINOR.**

---

## 7. Corrections to pm-onethird's framing

Four, in decreasing importance. The brief asked to be weighted down; this is
that.

1. **The ordering is not a chain of implications** (§1). `(LIB-weak)` and
   `(LIB-const)` are incomparable as function classes. `STATE.md` carries the
   rider that makes it right; **the brief does not**. Had the file been written
   to the brief's literal wording, it would be *less* correct than it is.
2. **Check 4's premise is a refuted claim** (§3). Demanding "the marginal form
   is FALSE" would have re-introduced the error mg-c4f5 found.
3. **Check 5 is stale** (§4). `STATE.md` correctly says AUDITED; obeying check 5
   would have meant filing a finding against a correct sentence.
4. **"I asserted the opposite this morning and it merged" is false as a
   statement about this file.** I checked every `STATE.md` version: the
   pre-correction text at `f85a4e8` reads *"in strength order and each arrow
   one-way: **(B) ⟹ LIB ⟹ (LIB-weak) ⟹ (LIB-const)**"* — the **direction is
   correct**; the defect was that the last arrow was rendered as a *plain,
   unqualified* implication. **The inversion was never in the file.** Every
   other occurrence of "weakest" in the file's history belongs to the unrelated
   "weakest kind" ledger rule. *(Disclosed: `905526f`'s own subject already says
   this, and my dispatch prompt contained `cf476ba`, an audit whose headline is
   "THE BRIEF'S OWN PREMISE IS THE THING THAT WAS WRONG". This is a pattern I
   was handed, not one I found — discount accordingly.)*

**Did the deliverable reproduce its own defect class?** No. The defect class was
*"the two forms are both present and joining them is left to the reader"*. The
correction puts both forms in the same sentence at all three prose sites. **The
nearest thing to a recurrence is FINDING 2** — and it is a *different pair* of
things (the two gaps), at *one* site, with the operands named at each.

---

## 8. WHAT I DID NOT DO

- **I made no edit to `STATE.md`, to any theorem statement, or to any other
  document.** Both findings are proposals. This is an audit.
- **I did not re-prove `(LIB-weak) ⟹ λ_std → 1`.** That is mg-c4f5's §1–§2 and
  it is done; I did not re-derive mg-210d's master bound, and I did not re-run
  its 101 658-poset test.
- **I did not attack `(LIB-weak)` itself**, and I did not assess whether it is
  reachable.
- **I did not re-derive mg-c3ca's forward vector.** I checked only that
  `STATE.md`'s *characterisation* of it matches mg-c4f5's verdict. I did **not**
  independently verify mg-c4f5's own "0 counterexamples over 1 168 036 pairs" or
  its `c*(n)` sequence — I checked those five rationals are above `⅓` and
  non-increasing, which is a **consistency check, not a reproduction**.
- **I did not verify `ε_spec ≈ 2×10⁻²` itself.** Every figure of mine that uses
  it (`300`, `2³⁰⁰`, `900C`, `885`, `0.67%`) is **conditional on that input**,
  which the file itself calls "unpinned by ~2 orders of magnitude".
- **`γ = 1/3` is INFERRED, not read.** It is the unique value consistent with
  the file's own `900C`. I did not confirm it against `step8.tex` or any source,
  and if `900C` is itself wrong, my inference is wrong with it — which is
  precisely why FINDING 1 asks for `γ` to be *stated*.
- **I checked no HTML twin, no `docs/` file other than mg-c4f5's**, and I did
  not verify mg-c4f5's own arithmetic beyond what `STATE.md` quotes from it.
- **I ran no poset computation of any kind.** This audit's mathematics is about
  asymptotic classes and needs none — which also means **it supplies no
  evidence about any poset**.
- **The `2/(n+1)` sighting is a location report, not a finding** — the dispatch
  pre-disclosed mg-131e/mg-372e. I found **0** occurrences in `STATE.md`.

---

## 9. Predictions, scored

Full text and the seven disclosed exposures: `PREDICTIONS.md` at `e57ae3b`.

| # | prediction | outcome |
|---|---|---|
| P1 | ordering direction correct (**declared a formality — H1/H2**) | **HELD**, no credit claimed |
| P2 | the ordering is not a chain; the two are incomparable | **HELD as mathematics** — and **P17's guard fires**: `STATE.md` carries the rider, so **NOT scored as a finding** |
| P3 | `(LIB) ⟹ (LIB-weak)` is conditional on `γ`, stated flat | **HELD** → **FINDING 1** |
| P4 | the kind is limit-vs-uniform | **HELD** |
| P5 | no `N₀` for the class (reproduction, H3) | **HELD**, no credit |
| P6 | `N₀` moves with `ε` | **HELD** — `(6/ε)²`, measured |
| P7 | gap at the claim — **refused a lean, 50/50** | **PASS at 3/3 prose sites.** I predicted this could go either way and it went right |
| P8 | the brief's premise is stale | **HELD** — contaminated by H5, discounted |
| P9 | ≥1 site states the ordering without its quantifier | **MISSED** — 0 such sites; the file is cleaner than I bet |
| P10 | "not blocked" loses its teeth | **MISSED** — both halves present, balanced |
| P11 | mg-c4f5 has run (reproduction, H4) | **HELD**, worth nothing |
| P12 | the "unaudited" marker is stale | **HELD** — now correctly says AUDITED |
| P13 | no theorem statement moves | **HELD** |
| P14 | `2/(n+1)` somewhere | **MISSED** — 0 occurrences |
| P15–P18 | my own likely errors | **P17 FIRED and stopped me converting P2 into a finding.** P15's byte-range guard was enforced mechanically by `m3_sites.py`. P16 held — `<` appears nowhere in `m1`. P18 held — every claim is quoted from the blob at the named SHA |

**Three of my substantive predictions MISSED in the file's favour (P9, P10,
P14).** I bet the document would be sloppier than it is.

---

## 10. Instrument

`code/state_ordering_audit_1df8/` — `m1_ordering.py` (the re-derivation, 4 NCs),
`m2_figures.py` (22/22 figures, exact), `m3_sites.py` (contiguity, 4 NCs),
`m4_riders.py` (riders / two gaps / status language, 1 NC), with committed
outputs. `PREDICTIONS.md` predates all of them.
