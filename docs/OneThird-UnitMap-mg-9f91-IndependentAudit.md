# Independent audit of `mg-9adf` — the `ε_spec`/`ε_c3ca` unit-map landing

**Auditor:** `mg-9f91`, pre-filed in the same action as `mg-9adf` and started only after it landed.
**Subject:** `21ee93f`, two lines of `STATE.md` (`:15`, the L1b blockquote; `:115`, ledger row 8).
**Predictions:** committed at `440cb05`, **before any diff of `21ee93f` was read**, with seven
hand measurements disclosed as `H1`–`H7` rather than laundered into predictions.

---

## VERDICT

**All six checks the brief asked for PASS. The landing is sound and I found no defect on the page.**

**One finding, and it is NOT in `STATE.md` — it is in the source `STATE.md` now cites.** `mg-9adf`
landed *"attainment PROVEN FOR ALL `n`"* for the inversion form. **That is correct — I re-derived it
at `192/192` exact-rational checks with an explicit witness at `n` up to `137`.** But
`mg-6bc2:450` says the opposite in as many words, and **neither the landed text nor the commit
message names the conflict.** A reader who follows `STATE.md`'s own citation lands on a document
that contradicts `STATE.md`. See **F1**.

**And the brief I was given — my own ticket's item 4 — is WRONG**, in the same way `mg-9adf`'s
ticket was. It told me a blanket all-`n` attainment claim would be BROKEN. It is not; the
finite population `{3,4,5,6,8}` belongs to a *different claim*. **`mg-9adf` caught this and said
so; I nearly scored a correct landing as this lineage's most repeated error.** That is `P14`,
which I filed against myself in advance.

---

## 1. THE MAP RE-DERIVES — `77/77`, and the `/6` is on the DEFINITION

`m1_map.py`, exact `Fraction` arithmetic, no floats in any assertion. From the one theorem
`E[inv_e] ≤ n(n−1)/6`:

| | definition | value at the bound | limit | approached from |
|---|---|---|---|---|
| `ε_c3ca` | `E[inv_e] ≤ ε·n²` | `(n−1)/(6n)` | `1/6` | **below** (strict at every finite `n`) |
| `ε_spec` | `E[inv_e] ≤ (ε/6)(n²−1)` | `n/(n+1)` | `1` | **below** (strict at every finite `n`) |
| ratio | | `6n²/(n²−1)` | `6` | **above** (`> 6` at every finite `n`) |

`77/77` exact checks over `n ∈ {3..8, 10, 12, 100, 1000, 10⁶}`. Every figure in the landed text
matches. **`ε_spec` at the bound is `n/(n+1)` identically — so the closure value is not a second
fact bolted onto the map, it is the same computation**, which is why carrying one without the
other would have been arbitrary.

**The attribution is right at both sites.** `:15` — *"the explicit `/6` in this row's own
**definition** of `ε_spec` is the ENTIRE difference"*. `:115` — *"the explicit `/6` this row's own
`(ε_spec/6)(n²−1)` carries is the entire difference"*. Neither presents `6` as a discovered factor;
both point at the definition that creates it. **P1, P2 HIT** (P1 with H1 disclosed — I had already
re-derived the map before writing the prediction, so it was a formality and was labelled one).

**Strictness is handled correctly and this was the subtlest thing on the page.** The landed text
writes `ε_c3ca < (n−1)/(6n) → 1/6` and `ε_spec < n/(n+1) → 1` with **strict `<`**, and reserves the
word **ATTAINED** for `n/(n+1)` over `M_n`. That is exactly right: `1/6` and `1` are *unattained
limits*, `n/(n+1)` is *attained at fixed `n`*. **P9 (that it would write `ε_spec = 1`, attained) did
not fire.**

---

## 2. IT DID NOT DECIDE DANIEL'S QUESTION — both sites reserve it explicitly

- `:15` — *"**WHICH `1/6` WAS MEANT IS NOT DECIDED HERE** — that question is Daniel's and is with
  him; the map above is true under either reading, and nothing in it says the conjecture is
  confirmed or refuted."*
- `:115` — *"**Which `1/6` was meant is Daniel's question and is NOT decided here; the map is true
  either way.**"*

Three reserving phrases matched at each site. The only occurrences of *"confirmed"* / *"refuted"*
in the inserted text are (a) that **denial** and (b) *"machine-confirmed exactly at `n = 3,4,5,6`"*,
which is a provenance mark on a different sentence. **PASS. P3 — reported as a REPRODUCTION, not a
hit: `H2` records that the commit subject was in my dispatch prompt and already told me the answer.**

**Why the reservation is substantive and not a formula.** `mg-6bc2 §2.1` (`:157–162`) is explicit
that there are **two live `1/6`s**: `ε_c3ca`'s is *"the value pair bias proves"* and `ε_spec`'s is
*"Daniel's conjectured target"*. Those are different statements about different constants and the
map is true whichever he meant. **I do not decide it either** — that is `P15`, filed against myself
in advance, and this document lays out both normalisations and stops.

---

## 3. THE CLOSURE TRAVELLED — to BOTH sites, with all six markers

Not just the unit map. Both `:15` and `:115` carry, mechanically confirmed (`m4_landing.py`, S2):

| marker | `:15` | `:115` |
|---|---|---|
| `max{ 6E_μ[inv_e]/(n²−1) : μ ∈ M_n } = n/(n+1)` | YES | YES |
| the word **ATTAINED** | YES | YES |
| *"EQUALITY for the information it consumes"* | YES | YES |
| *"not a bound awaiting a better argument"* | YES | YES |
| the **realizability** rider — every route below `1` must add one | YES | YES |
| `M_n` defined on the spot | YES | YES |

So `Op-Form` Claim 6.1 is recorded as a **closure**, not bookkeeping. The brief asked for this and
got it at *both* sites rather than the one it strictly required. **P4 HIT.**

---

## 4. THE n-RANGE SPLIT — `mg-9adf` IS RIGHT AND BOTH TICKETS WERE WRONG

This is the load-bearing check and it inverts the brief.

**What my ticket told me.** *"Attainment is finite-population (`n ∈ {3,4,5,6,8}`); the `≤`
directions are theorems for all `n`. A blanket all-`n` attainment claim is BROKEN, and it is this
lineage's most repeated error."*

**What `mg-9adf` landed instead.** Claim 3.1's `≤` **and its attainment** are theorems for all `n`;
`{3,4,5,6,8}` belongs to **Claim 4.1**, the *footrule* statement.

**Settled by exhibiting the witness, not by trusting either.** `m3_attainment.py` brute-forces the
flip probabilities over `S_n` — no LP, nothing inherited from `mg-6bc2`'s tableau. The `≥` witness
is the **two-atom law** `μ = (2/3+η)δ_e + (1/3−η)δ_{rev e}`: **two permutations, `e` and its
reverse.** It is a probability measure, it is feasible for `M_n(η)` (every pair flips with
probability exactly `1/3−η`), and its objective equals `(1−3η)·n/(n+1)` exactly.

    T1 probability measure   48/48
    T2 feasible for M_n(η)   48/48
    T3 objective == Claim 3.1 48/48
    T4 ≤ tight at the witness 48/48        TOTAL 192/192 exact-rational

over `n ∈ {2,3,4,5,6,7,8,9,11,20,50,137} × η ∈ {0, 1/100, 1/12, 1/6}`. **Seven of those `n` are
outside `{3,4,5,6,8}`** — `2, 7, 9, 11, 20, 50, 137` — and the witness is constructible and tight at
every one. **A two-permutation construction is not a finite-population result.**

And `mg-6bc2`'s Claim 4.1 (`:228–230`) reads, verbatim: *"`≤` PROVEN all `n` … attainment MEASURED
at `n = 3,4,5,6` (LP) and `n = 8` (explicit construction). **Not proven for all `n`.**"* — the set
`{3,4,5,6,8}`, exactly, sitting on the **footrule** claim. **That is where both tickets' paraphrase
came from.**

**So the landed split is correct, and it is marked AT the claim** — `:115` reads *"Claim 3.1's `≤`
and its attainment are theorems for all `n`; the parallel **footrule** statement … has `≤` proven
for all `n` but its **ATTAINMENT is FINITE-POPULATION**"*, with the population inside the same
clause as the word. **P5 HIT; P5b (qualifier stranded in a different sentence) did not fire.**

**Landing my brief verbatim would have understated a theorem as a finite check** — the failure this
file's `Kind` column exists to prevent, arrived at from the opposite direction.

---

## 5. TODAY'S OTHER TWO ROW-8 LANDINGS SURVIVED — `13/13` byte-identical, and the edit deleted nothing

Three tickets edited row 8 on 2026-08-07: `mg-d1a2` (`a682e1d`), `mg-5ce3` (`4ef64d7`), `mg-9adf`
(`21ee93f`).

`m2_survival.py` **never looks at the diff** — that guard was written into `PREDICTIONS.md` as
`P13`, my own most likely error, before I could be tempted by it. Row 8 is one 5 245-character
table cell; any edit renders as *"the whole line changed"*. The detector extracts each guarded span
by **string search** from the landed file and compares bytes.

    mg-d1a2  guard: instruction / reason / refereed cite / preprint cite / own reason  5/5 INTACT
    mg-5ce3  headline / counterexample family / 10⁹⁰ / superseded / what-closes /
             not-a-research-direction / what-it-does-not-claim / strictly-stronger    8/8 INTACT

    at mg-9adf : 13 intact, 0 reflowed, 0 LOST
    at HEAD    : 13 intact, 0 reflowed, 0 LOST

**And the structural reason is stronger than the count.** Character-level diff of both changed
lines yields opcodes `['equal','insert','equal']` and `['equal','insert','equal','insert','equal']`
— **pure insertion. Not one byte of the parent was deleted or replaced at either site.** So the
survival of `mg-d1a2`'s and `mg-5ce3`'s text is not a lucky outcome of careful editing; it is a
property of the edit's shape. **P6, P7 HIT; P7b (survives-but-reflowed) did not fire; P13 did not
fire.**

**Line numbers held, and the corpus depends on them.** 208 lines before, 208 after; row 8's table
structure unchanged (6 pipes → 6 pipes); `:135` still lands on the two-atom-law sentence and `:156`
on `mg-92e6`'s probe-B row, both re-grepped here. `mg-9adf` reports reverting a prettier fenced
version for this reason and the artefact matches the report.

---

## 6. THE `1/6` FORM WAS CITED — with both line references, at both sites

Both sites cite `OneThird-LIBweak-mg-c4f5-IndependentAudit.md:415` for the sentence **and**
`OneThird-LIBweak-mg-c3ca.md:172` for the definition of the `ε` it is in. **`:415` and `:172` are
both named explicitly.** No fresh derivation of the `1/6` was written. **P8 HIT.**

**Partial, and I am marking it partial (F2).** The `:415` sentence is *quoted verbatim* at both new
sites, so the corpus now holds **6 verbatim copies** of it: the source `:415`, `mg-6bc2:47` and
`:146`, `pairbias_sharpening_6bc2/PREDICTIONS.md:37`, and now `STATE.md:15` and `:115`. `mg-9adf`
added 2, taking it from 4 to 6 — **it did not create the duplication, but it did extend it.** Each
copy carries its citation, so drift is *detectable*; item 6's concern is **mitigated, not
discharged**.

---

## FINDINGS

### F1 — the landing is right and its own cited source says otherwise, and nobody is told

**`mg-6bc2:450`, Defect 2:** *"Claim 3.1's `≤` and Claim 4.1's `≤` are theorems for all `n`;
**every attainment statement is finite population** and is marked as such."*

**`mg-6bc2:175`, Claim 3.1's own header:** *"**[PROVEN, all `n`, by hand;** machine-confirmed
exactly at `n = 3,4,5,6`]"*.

**These contradict each other, and `:450` is the wrong one** — §4 above proves Claim 3.1's
attainment at every `n` by explicit construction, and the trailing clause *"and is marked as such"*
is falsified by `:175`, which marks it the other way. Defect 2's *heading* is *"the LP is `n ≤ 6`"*
and its *closing* sentence — *"Nothing **here** is evidence at unbounded `n` about attainment"* — is
correctly scoped to the LP. **The middle sentence over-reaches its own section.**

**`mg-9adf` resolved this contradiction in the correct direction and did not record that it had
resolved anything.** `m4_landing.py` S4: the landed text asserts all-`n` attainment (`True`), names
`mg-6bc2`'s blanket caveat (`False`); the commit message names *"Defect 2"* (`False`) and *"every
attainment statement"* (`False`).

**Consequence.** `STATE.md` now sends a reader to `mg-6bc2` for the closure. A careful one reads to
`:450` and finds the cited document apparently contradicting the ledger — with no note saying which
wins or why. The next agent to notice will either weaken row 8 back to a finite-population claim
(**a regression, and this lineage's most repeated error committed by way of a footnote**) or spend a
ticket re-deriving what §4 above already settles.

**The repair belongs in `mg-6bc2`, not in `STATE.md`** — the ledger is right. **I did not make it;
that document is another ticket's landing and this is an audit.** Filed for `pm-onethird` to route.

### F2 — the `:415` quote now has six verbatim copies (see §6)

Mitigated by the citation travelling with each copy. Recorded because item 6 asked, and because
`STATE.md:15` and `:115` are now two of the six.

### F3 — a mis-sited claim in the commit message, not on the page

The commit message says *"**Row 8's** `ε_dem` clause and the whole demand-side account are
untouched"*. **Row 8 has no `ε_dem` clause** — `ε_dem` occurs at `STATE.md:15` and `:164`, and `:15`
is a line `mg-9adf` *did* edit. **The substance is true and I verified it**: `ε_dem = ε_leak²/(2C₃)`
(1 → 1), `C₃` (2 → 2), `~50` (2 → 2) at `:15`, and the edit there is a pure insertion, so the clause
is byte-identical. Only the siting is wrong.

### F4 — an exposition gap with zero consequence, stated because it looks like a contradiction

`ε_spec < n/(n+1)` (**strict**) sits a few clauses from `max{…} = n/(n+1)`, **ATTAINED**. Both are
true and they are about different sets: the strict `<` comes from the frozen hypothesis
`δ(P) < 1/3`, the attained `=` is over `M_n` **defined on the same line with `≤ 1/3`** — non-strict,
so the maximum is achieved. The resolution is derivable from the definitions the landed text
itself supplies; it is not stated. Not a defect. Recorded because a reader meeting both in one
sentence may read a units subtlety as an inconsistency, which is the exact failure class this
landing exists to prevent.

---

## DEFECTS OF THIS INSTRUMENT, KEPT IN THE SOURCE

**D1 — my decider-detector read a DENIAL as an ASSERTION, inside an audit about misreadings.**
`m4_landing.py`'s S1 regex `conjecture is (confirmed|refuted|…)` fires on `:15`, and the string it
matched is *"nothing in it says the conjecture is **confirmed or refuted**"* — the sentence that
**reserves** the question. Had I trusted the detector's headline I would have reported the one site
that most explicitly obeys the brief as the site that violated it. The regex is **kept as written**
and its output is printed with surrounding context precisely so the false positive is visible; the
finding was resolved by reading, not by the scan.

**D2 — `P14` fired: I was handed a false premise and it was the audit's central check.** My ticket
item 4 asserted a population that belongs to another claim. I filed `P14` in advance — *"auditing
the ticket instead of the landing … the brief is not the standard, the corpus is"* — and it is the
only reason I went to `mg-6bc2:174` and `:228` at source instead of scoring the landing against my
own instructions. **The check the brief called this lineage's most repeated error was itself an
instance of it.**

**D3 — the exhaustive `≤` cross-check in `m3_attainment.py` is thin and says so.** It enumerates
only *single-atom* measures at `n ≤ 6`, of which just 4 are feasible. The real `≤` is one line of
linearity of expectation (`E[inv_e] = Σ q_ij ≤ C(n,2)(1/3−η)`) and needs no enumeration; the scan
adds almost nothing and should not be read as an independent verification of the `≤` direction.

---

## PREDICTION SCORING

Predictions at `440cb05`, before any diff was read. `H1`–`H7` are disclosed hand measurements and
are **not** scored.

| # | conf | outcome |
|---|---|---|
| P1 | 90% | **HIT** — but a formality; `H1` had already re-derived it, and the prediction said so. |
| P2 | 60% | **HIT** — `/6` attributed to the definition at both sites. |
| P3 | 85% | **REPRODUCTION, not a hit** — `H2` gave me the answer in the dispatch prompt. |
| P4 | 65% | **HIT** — closure travelled, and to both sites. |
| P5 | 55% | **HIT** — split marked at the claim. |
| P5b | 35% | **did not fire** — no stranded qualifier. |
| P6 | 80% | **HIT** — `mg-d1a2` guard 5/5 byte-identical. |
| P7 | 80% | **HIT** — `mg-5ce3` N₀ text 8/8 byte-identical. |
| P7b | 30% | **did not fire** — nothing reflowed; the edit is a pure insertion. |
| P8 | 55% | **HIT**, partially — cited with both line refs, but the quote is now 6× (F2). |
| P9 | 25% | **did not fire** — strictness is correct; limits strict, `n/(n+1)` attained. |
| P10 | 40% | **MISSED, and kept as written.** I bet the text would use `ε_sup` and `ε_spec` without identifying them. `STATE.md:15` **already** defines them — *"`ε_spec` names two numbers … the constant we can **prove** (`ε_sup`) and the constant that **suffices** (`ε_dem`)"* — immediately upstream of the insertion, and `:115` re-anchors with *"the constant we can PROVE"* plus a pointer to the blockquote. The currency conflation I bet on was already guarded. |
| P11 | 20% | **did not fire** — only `:15` and `:115` changed; row 11 is `:118`, untouched. |
| P12 | 30% | **weak form only** — direction of approach is not stated, but the exact finite-`n` forms `(n−1)/(6n)`, `n/(n+1)`, `6n²/(n²−1)` are all on the page, so the flat-factor-6 error I was worried about (`n=3`: `2/3` vs the true `3/4`) is preventable from the text as landed. |
| P13 | 40% | **did not fire** — my own most likely error. The byte-for-byte substring guard held, and the pure-insertion result made it moot. |
| P14 | 30% | **FIRED, and it was the whole audit** — see D2. |
| P15 | 30% | **did not fire** — I have not decided which `1/6` Daniel meant and this document does not. |

---

## WHAT I DID NOT DO

- **I did not decide which `1/6` Daniel meant.** `mg-6bc2 §2.1` records two live `1/6`s —
  `ε_c3ca`'s *"the value pair bias proves"* and `ε_spec`'s *"Daniel's conjectured target"*. The map
  is true under either. Which he meant is his, and nothing here narrows it.
- **I did not repair F1.** `mg-6bc2:450` is another ticket's landing and this is an audit. Not one
  byte of `docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md` was changed.
- **I did not re-derive `mg-6bc2`'s LP.** I never ran or read its tableau. `m3_attainment.py`
  brute-forces the *witness*, which is two permutations and needs no LP; my `192/192` is a check of
  **attainment**, and the `≤` direction I take from one line of linearity, not from `mg-6bc2`.
- **I did not verify Claim 4.1's `n = 8` explicit construction, the `8/7` footrule cap, or the
  Diaconis–Graham `F ≤ 2I` step.** I read Claim 4.1's marking at `:228–230` and used it to locate
  the `{3,4,5,6,8}` population. Whether that construction is correct is unaudited here.
- **I did not verify `Op-Form` Claim 6.1 at its own source.** I checked only that `STATE.md` now
  describes it as an equality, which is what `mg-6bc2` says it is.
- **I did not audit `STATE.md:164`** (`mg-345e`'s row), which also carries `ε_sup`, nor the `~50`
  gap factor, nor anything downstream of row 8.
- **I did not check the HTML twin beyond counting.** `docs/state-of-the-wall.html` carries 0
  occurrences of `ε_spec`, `ε_sup`, `Claim 6.1` and `1/6`, confirming `mg-9adf`'s absence claim; I
  did not read it for a paraphrase that avoids all four tokens.
- **I did not touch `STATE.md`.** This audit adds a document and an instrument and changes no
  landed text.
