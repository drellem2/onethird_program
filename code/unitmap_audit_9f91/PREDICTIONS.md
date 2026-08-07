# mg-9f91 — PREDICTIONS, committed before the landed diff is read

Independent audit of **mg-9adf** (`21ee93f`), which lands the `ε_spec`/`ε_c3ca` unit
map into `STATE.md` row 8 and the L1b blockquote.

**This file is committed BEFORE I run `git show 21ee93f` or any diff of it.** What I
have read at the time of writing is listed under "NOT BLIND" below; everything there
is disclosed as a **hand measurement (H)**, not laundered into a prediction.

---

## NOT BLIND — inputs already in hand, disclosed rather than scored

**H1. I have already re-derived the whole map by machine** (`m1_map.py`, run before this
file was written; output committed alongside). Exact rational arithmetic, `n ∈ {3..8,10,100,1000}`:

    E[inv_e] ≤ n(n−1)/6                              (the one theorem)
      ε_c3ca := E/n²        = (n−1)/(6n)   ↗ 1/6     (STRICTLY BELOW 1/6 at every finite n)
      ε_spec := 6E/(n²−1)   = n/(n+1)      ↗ 1       (STRICTLY BELOW 1 at every finite n)
      ε_spec/ε_c3ca         = 6n²/(n²−1)   ↘ 6       (STRICTLY ABOVE 6 at every finite n)

  `ε_spec = n/(n+1)` **identically** — 9/9 n values. So the closure value the ticket asks
  to be carried (`max 6E[inv_e]/(n²−1) = n/(n+1)`) is not a separate fact bolted onto the
  map; it is *the same computation*. Ratio `= 6n²/(n²−1)` **identically**, 9/9.
  So the ticket's arithmetic is right and P1 below is a near-formality.

**H2. The commit subject of `21ee93f` is in my dispatch prompt verbatim** — *"`ε_sup < 1`
AND "pair bias gives 1/6" ARE THE SAME THEOREM, AND ROW 8 NOW SAYS SO WHERE A READER
MEETS THE `1`"*. It says "same theorem", not "confirmed"/"refuted". **This materially
inflates P3 and I am not claiming it as a blind hit.**

**H3. I have read row 8 at the PARENT commit `72a6e33`** (i.e. before mg-9adf). Both
guards are present there: mg-d1a2's `DO NOT CITE THE LITERATURE BOUND AGAINST THIS N₀` /
`that discharges nothing here`, and mg-5ce3's `N₀ IS NOT UNSPECIFIED: NO N₀ WORKS FOR THE
CLASS AT ALL`. So P6/P7 are tests of *survival*, with the exact target strings known.

**H4. I have read mg-9adf's ticket body**, including its `== DO NOT ==` block. Predictions
about whether it obeyed its own brief are therefore predictions about *compliance*, not
about *intent*.

**H5. The cited site `OneThird-LIBweak-mg-c4f5-IndependentAudit.md:415` reads
"Freezing unconditionally gives only `ε < 1/6 ≈ 0.167`"** — I have read it. Note it is
**strict `<`**, consistent with H1's `(n−1)/(6n) < 1/6`.

**H6. Three tickets edited row 8 today**: mg-d1a2 (`a682e1d`), mg-5ce3 (`4ef64d7`),
mg-9adf (`21ee93f`). Confirmed from the log before writing this.

**H7. Row 8 at the parent already contains the phrase "`ε_sup < 1`"** (in the clause
*"already proven at `ε_sup < 1` (mg-345e)"*) — while the ticket's map is written in
`ε_spec`. Whether those two names denote one quantity is **not stated at the parent**.
This is the observation P10 is built on, and it predates the diff.

---

## PREDICTIONS

Scored strictly. "BROKEN" = the audit finding the ticket names as a failure.

| # | conf | prediction |
|---|------|------------|
| **P1** | 90% | The landed ratio is written `6n²/(n²−1) → 6` and re-derives exactly (H1). Residual risk is a transcription inversion (`(n²−1)/6n²`) or a `→` written as `=`. |
| **P2** | 60% | The `/6` is attributed to **ε_spec's DEFINITION** — i.e. the landed text says in words that the explicit `/6` in `E ≤ (ε_spec/6)(n²−1)` *is* the whole difference — rather than presenting 6 as a factor that was discovered or derived. I put this only at 60% because the natural prose for a "unit map" is *"they differ by 6"*, which is the discovered-factor framing. |
| **P3** | 85% | It did **NOT** decide which 1/6 Daniel meant: no "confirmed", no "refuted", no "Daniel's conjecture is right/wrong" in the landed text; the two normalisations are laid out and the choice is left open. **Inflated by H2 — report as a reproduction, not a hit.** |
| **P4** | 65% | The **CLOSURE travelled**: the landed row carries `max 6E[inv_e]/(n²−1) = n/(n+1)` over `M_n`, **ATTAINED**, and says in words that this makes the pair-marginal route an *equality/closure* rather than a bound awaiting sharpening. This is the half a minimal edit most often drops, because the ticket's headline ask is the map. |
| **P5** | 55% | The n-range split is marked **AT THE CLAIM** — the word "attained" carries its finite population `n ∈ {3,4,5,6,8}` in the same sentence/clause, and the `≤` directions are separately marked all-n. |
| **P5b** | 35% | *Failure mode of P5, scored separately:* at least one attainment statement in the landed text has its n-range qualifier in a **different sentence** from the word "attained", so a reader quoting one sentence gets a blanket all-n attainment claim. (P5 and P5b can both be partly right if there are two attainment sites.) |
| **P6** | 80% | mg-d1a2's guard survived **intact**: both `DO NOT CITE THE LITERATURE BOUND AGAINST THIS N₀` and `that discharges nothing here` are byte-identical to `72a6e33`. |
| **P7** | 80% | mg-5ce3's N₀ text survived **intact**: `NO N₀ WORKS FOR THE CLASS AT ALL`, the `2³⁰⁰ ≈ 10⁹⁰` figure, and both the *"what that closes"* / *"what it does not claim"* halves are byte-identical to `72a6e33`. |
| **P7b** | 30% | *Failure mode of P6/P7:* something survives in **substance** but was reflowed — reordered, re-bolded, or had a clause spliced through it — so a byte-diff shows a change inside the guarded span even though no claim was lost. I predict this is the *most likely* form of damage from a third edit to one cell, far likelier than outright deletion. |
| **P8** | 55% | The 1/6 form is **CITED** with a file reference to `OneThird-LIBweak-mg-c4f5-IndependentAudit.md` (ideally `:415`) and/or `mg-c3ca.md:172` for the definition, rather than restated as a fresh derivation with no pointer. |
| **P9** | 25% | The landed text mis-states the **strictness**: writes `ε_c3ca = 1/6` or `ε_spec = 1` (attained) where H1 gives strict `<` at every finite n with `1/6` and `1` as unattained limits. What *is* attained is `n/(n+1)`. Confusing the attained closure value with the limit is a live trap here precisely *because* the ticket uses the word ATTAINED. |
| **P10** | 40% | **Currency conflation, the class this lineage has already committed twice** (mg-345e P8, mg-76b2 P14): the landed text uses both `ε_sup` and `ε_spec` and **does not say whether they denote the same quantity** (H7). If `ε_sup` is row 8's existing name for the pair-bias route's constant and `ε_spec` is the ledger's, a unit map that maps `ε_spec ↔ ε_c3ca` while the surrounding prose says `ε_sup < 1` leaves the reader with three symbols and two identifications. |
| **P11** | 20% | The edit touched something the ticket said not to: row 11, `C_3`, or `ε_dem`. |
| **P12** | 30% | The landed text asserts the map is `→ 6` and **omits the direction** — that the ratio approaches 6 from **above** (`> 6` at every finite n) and `ε_c3ca` approaches 1/6 from **below**. Harmless asymptotically; but a reader at `n = 3` who applies a flat factor 6 to `ε_c3ca = 1/9` gets `2/3`, not the true `3/4`. |

---

## MY OWN MOST LIKELY ERRORS, filed in advance

**P13** (my most likely error, 40%): **Scoring a reflow as a loss.** Three tickets edited
one cell today. A diff of one enormous single-line table cell renders as "whole line
changed", and I will be tempted to report mg-d1a2's or mg-5ce3's text as damaged when the
only thing that moved was its position in the cell. **Guard I am binding myself to now:**
for P6/P7 I will extract the guarded spans by *string search on the landed file*, not by
reading the diff, and compare them byte-for-byte against the same spans extracted from
`git show 72a6e33:STATE.md`. A substring that is present and identical is INTACT
regardless of what the diff hunk looks like.

**P14** (second most likely, 30%): **Auditing the ticket instead of the landing.** I have
read mg-9adf's brief (H4) before its diff, so I risk checking whether the landed text
matches the brief's *wording* rather than whether it is *true and complete*. The brief is
not the standard — the corpus is. Specifically: if the landed text is correct but
differently worded than the brief's block, that is not a defect, and if it matches the
brief verbatim but the brief was wrong, that IS one.

**P15** (30%): **Deciding Daniel's question myself while checking that mg-9adf didn't.**
H1 shows his 1/6 is proven *in the ε_c3ca normalisation* and 6× weaker than the ε_spec
statement. Writing "so his conjecture is proven" anywhere in my verdict commits exactly
the reserved-question violation I am auditing for. Which 1/6 he meant is his.

---

## WHAT I AM NOT PREDICTING

I make no prediction about mg-6bc2's LP or its `n/(n+1)` extremal construction being
correct — the ticket forbids re-deriving them and I will cite, not re-run, them. So any
verdict I reach about the CLOSURE is a verdict about whether it **travelled onto the
page with its scope**, not about whether it is **true**.
