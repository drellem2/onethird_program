# mg-2eed — INDEPENDENT AUDIT of mg-b488's STATE.md landing

**Verdict: CONFIRMED.** No factual defect found. One legibility observation and one
correction *to my own brief* are recorded below; neither is a defect in mg-b488.

**STATE.md audited at commit `491d42c79f7628c18cb7a5d197faa9f4600cd6c1`**
("docs: eps_spec = 2/(n+1) IS ON THE PAGE AS FALSE, NOT AS A CONJECTURE … (mg-b488)"),
blob `7f73bfc87b4bc4caab6c836f8c3922a2416863cf`, 209 lines. That is the current
`STATE.md` — `git log origin/main -- STATE.md` returns `491d42c` as the most recent
commit touching the file, and `origin/main` was at `ba67d39` when I read it, with the
file byte-identical at both. **The SHA I name and the file I read are the same object.**
The file did not move under me.

---

## 0. THE BRIEF'S PREMISE IS SUPERSEDED, AND mg-b488 IS RIGHT WHERE THE BRIEF IS WRONG

My dispatch told me to check whether a reader can tell the `≤` direction of
`ε_spec = 2/(n+1)` is a **CONJECTURE**, exact at `n = 3,4,5` only, and to REFUTE if the
conditionality was understated. **The conditionality is not understated. It is
*obsolete*, and the landed text says something strictly stronger and different: the
formula is FALSE.** mg-131e returned between my parent's filing and its landing and
refuted `2/(n+1)` at `n = 6` by explicit witness.

So the question I was sent to ask has to be re-aimed before it can be answered, and I
answer the re-aimed one: **can a reader who never saw the parent tell that `2/(n+1)` is
false?** Yes, at every site, unmissably. Had mg-b488 obeyed my brief's literal wording
and hedged the formula as a conjecture, it would have put a **known-false figure into the
canonical document behind a hedge that reads as caution** — a worse outcome than the
overclaim my brief was written to catch. It declined, and its commit message says so in
as many words. **That is the correct call and I record it as the audit's first finding.**

---

## 1. THE ONE CHECK THAT MATTERS MOST — DID THE CONDITIONALITY SURVIVE? **YES.**

`2/(n+1)` occurs **exactly 4 times** in the whole file. All 4 are inside the two new
rows. **Every one carries its status at the claim, and in 3 of 4 the status comes
*before* the formula.** Quoted verbatim:

1. **`:167`** — *"**(a) REFUTED — `ε_spec = 2/(n+1)` IS A SMALL-`n` COINCIDENCE, AND IT
   IS FALSE, NOT CONJECTURAL (mg-131e §0, §4).**"* — a reader meets `REFUTED` and
   `FALSE, NOT CONJECTURAL` before meeting the formula.
2. **`:167`** — *"mg-200d's *"Daniel's `1/6` at `n ≥ 11`, the wall's `≈ 2×10⁻²` at
   `n ≥ 99`"* was read off `2/(n+1)`; **with the formula refuted there is no threshold to
   quote, and the replacement constant is UNKNOWN — do not print a new number and do not
   carry the old one.**"*
3. **`:168`** — *"mg-131e has since refuted the per-slot column's `ε_spec = 2/(n+1)` from
   `n = 6`"*.
4. **`:168`** — *"§5.1's *"what it buys"* table still prints `ε_spec = 2/(n+1)` as live;
   correcting mg-6bc2's document is a separate landing and is **not** made here."* — a
   known-stale site in *another* file, named as stale and deliberately not edited.

**Which of the two readings does the landed text support?** Neither of my brief's two.
It supports a third and sharper one: **`≥` is a theorem for all `n`; the *exact formula*
is CERTIFIED at `n = 3,4,5` and REFUTED at `n = 6`; and "false for every `n ≥ 6`" is
explicitly NOT claimed.** The row states that last limit itself:

> *"**SCOPE LIMITS, AT THE CLAIM:** *"false at `n = 6`"* is established; ***"false for
> every `n ≥ 6`" IS NOT*** — no exhaustive `n = 6` was run (`32768` branches over `720`
> columns, deliberately not attempted), so **every `n ≥ 6` figure is a LOWER bound on a
> NAMED branch and the true `n = 6` maximum may EXCEED `11/6`**"*

**The failure mode my brief named is absent in the specific form it named it.** The
heading does not assert `2/(n+1)` flatly with a caveat below it — the heading is
**"RED ON THE CONSTANT · GREEN ON ONE BRANCH · THE RATE SURVIVES ON THREE POINTS AND NO
PROOF"**, which carries the refutation, the survival and the thinness *in the heading
itself*. The row opens by instructing the reader to read the kind at each of its three
statements. This is the opposite of the failure class.

### The `Θ(n²) → Θ(n)` rate is kinded too, at both sites

`:167(c)`: *"**the exact values supporting the RATE are the same `n ≤ 5` that supported
the formula now known false, so the rate is three points and no proof**, and the
`n = 6..10` correction runs **UPWARD**"*. `:168` inherits it: *"the ASYMPTOTIC rendering
of it … **rests on the same three points and no proof**"*. No route by which a reader
picks up the rate as established.

---

## 2. THE FIGURES, RE-READ AT THEIR SOURCES — AND TWO OF THEM RE-DERIVED FROM SCRATCH

mg-b488 is forbidden from restating from its brief. **It obeyed.** Every figure in both
rows is present, verbatim and in the same units, in
`docs/OneThird-DualCertificate-mg-131e.md`,
`docs/OneThird-PerSlot-AdjacencySymmetry-mg-200d.md`, and §5/§5.1/§5.2 of
`docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md`. I read the sources, not the diff
and not the row.

### 2.1 The `n = 6` refutation — REBUILT ON MY OWN CODE, sharing nothing with mg-131e

Row `:167` states the witness. I reconstructed it from the atom table at
`OneThird-DualCertificate-mg-131e.md:122–138` and checked every claim the row makes about
it in exact `Fraction` arithmetic, with my own inversion, flip-probability, transitivity
and per-slot-symmetry code:

| claim in the row | my independent result |
|---|---|
| comparable set is **transitive** (checked, not asserted) | **True**, 9 comparable pairs |
| 6 atoms at mass `1/6` → total mass `1` | **1** |
| every flip probability `≤ 1/3` | max over `I` = **1/3** |
| five consecutive pairs at `1/3`, `(1,4)` at `1/6` | `(0,1)(1,2)(2,3)(3,4)(4,5)` = **1/3**; `(1,4)` = **1/6** |
| **no comparable pair ever flipped** | **[]** — none |
| **zero** per-slot symmetry violations | **0** |
| `E[inv] = 11/6 > 5/3 = (n−1)/3` | **11/6 > 5/3** |
| `ε_spec = 11/35 > 2/7 = 2/(n+1)` | `6·(11/6)/35` = **11/35 > 2/7** |

**The refutation is real, and STATE.md's rendering of it is exact.** Since the
disjunctive per-slot value is a *maximum*, one feasible witness above `(n−1)/3` kills
"exactly `(n−1)/3`" at `n = 6` outright — an `FP✗` in this file's own vocabulary, i.e.
refutation at universal strength. The row's `FALSE, NOT CONJECTURAL` is the correct kind.

### 2.2 The `(b)` theorem — the `≥` is a PROOF, not the `n = 3..20` run

This is the one place a hostile reader could still be misled, so I checked it hardest.
Row `:167(b)` claims `(n−1)/3` **"EXACTLY, for every `n`, BOTH DIRECTIONS, with no solver
on either side"**, and then parenthesises the `≥` as *"checked directly, without the LP,
at every `n` from 3 to 20"*. **Read alone, that parenthetical looks like a
finite-population warrant dressed as a theorem** — the exact confusion this file's
standing rule exists to prevent.

It is not. At source, `OneThird-PerSlot-AdjacencySymmetry-mg-200d.md:230` is
**"THEOREM 4.2 (lower bound, every `n ≥ 3`)"** with a construction proof closed by `∎`;
the `n = 3..20` run is a *confirmation* appended after the `∎`, not the warrant. The `≤`
is mg-131e's trivial dual, whose source says **"This is a proof, not a computation"** and
**"No solver appears on either side"** (`OneThird-DualCertificate-mg-131e.md:62,71`).

I also **re-derived the `≥` myself** rather than take either document's word: on the
branch `I = {(i,i+1)}`, the even- and odd-index matchings partition the `n−1` consecutive
pairs, so each is flipped in exactly one of the three atoms — `q = 1/3 ≤ 1/3` for every
pair, `E[inv] = (n−1)/3`, no comparable pair flipped, and per-slot symmetry holds because
the identity supplies `J_k(k,k+1) = 1/3` against the matching's `J_k(k+1,k) = 1/3`. That
argument is `n`-free. Machine-confirmed independently at **every `n` from 3 to 20**: all
four properties hold at every `n`, `E[inv] = (n−1)/3` exactly. **The claim is TRUE and the
kind is correctly marked.**

**The distinction the row draws is the load-bearing one and it is drawn correctly:**
mg-200d's *Conjecture 4.3* ranges over **all** `2^C(n,2)` branches and is what `n = 6`
kills; mg-131e's *Theorem* is restricted to the **consecutive-pairs branch** and survives.
The row says exactly this — *"a statement about ONE branch out of `2^C(n,2)`, which is
exactly why it survives a refutation about all of them — do not let (a) bury it, and do
not read it as (a)'s repair."*

### 2.3 The corrected section-5 row — right figures, right unit, no PUBLISHED row loose

The brief warned that mg-ba78's defect could reappear one file over. **It did not.**
Row `:168` carries, verbatim from `OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md:274–280`:

| `n` | aggregate | per-slot | source table (`inv-opt`, out of `C(n,2)`) |
|---|---|---|---|
| 3 | `2/3` | `3/3` | **2**, **3** of 3 ✓ |
| 4 | `5/6` | `6/6` | **5**, **6** of 6 ✓ |
| 5 | `6/10` | `7/10` | **6**, **7** of 10 ✓ |
| 6 | `7/15` | `8/15` | **7**, **8** of 15 ✓ |

**The unit is stated at the figures, not in a footnote** — *"**unordered pairs `{x,y}`,
`x < y`, of a PROBABILITY measure, out of `C(n,2)`**"* — which is the source's own unit
sentence (`:265–266`). **No unit mixing anywhere.**

The published row `0, 6, 8, 10` **does** appear — and appears *correctly*, as
*"**The published row was `0, 6, 8, 10` and is wrong in BOTH unit and measure.**"*
It matches §5.2's superseded `inv-opt aggregate` column exactly. Naming a superseded
figure as superseded is the corpus's own practice (cf. the struck `2×10⁻⁴`); carrying it
bare would have been the defect. It is not carried bare.

Also reproduced at source: mass `2/3` (`:21`), *"2 of its 3 pairs"* (`:292`),
`6 → 5, 8 → 6, 10 → 7, 17 → 13` (`:338`), the nesting and its strictness check, the
mutation control reproducing the published `0`. The derived `ε_spec` values in the row —
aggregate `1/2, 2/3, 7/12` against per-slot `1/2, 2/5, 1/3` — are `6E/(n²−1)` on §5.1's
`what it buys` table (`2/3, 5/3, 7/3` and `2/3, 1, 4/3`); I recomputed all six and all six
are right.

**One placement check that could have gone wrong and did not:** the row says the two forms
*"AGREE at `n = 3` and separate from `n = 4`"*, while the violation-count table has
`2` vs `3` at `n = 3` — not equal. The row places that clause inside the *"what they
**buy**"* sentence, which is where the source puts it and where it is true (`2/3` vs
`2/3`). Correct placement; a reader cannot cross the two.

---

## 3. P6's RESCORING LANDED AS A RESCORING, AND THE FLATTERING DIRECTION SURVIVED

The row's **heading** carries it: **"CORRECTS MERGED WORK · P6 RESCORED `HELD` WHERE IT
WAS PUBLISHED `REFUTED`"**. In-cell: *"**P6 IS RESCORED `HELD`. mg-6bc2 published it
`REFUTED`.**"* The fact that a published prediction was wrong is therefore not
recoverable-only-by-inference; it is asserted twice.

**The useful part — the direction — survived intact:**

> *"**NOTE THE DIRECTION OF THE ERROR, because it is the reason this one survived
> review:** a self-refutation reads as *more careful* than a prediction that lands, so
> the defect **flattered its author**, and it supplied the surprise §5's conclusion was
> built on — neither the refutation nor the surprise was real."*

That is the source's own point (`:298–304`) landed without dilution, together with the
*"second unit-mismatch in this lineage in one day"* framing and the observation that
mg-6bc2's §2.1 guard *"was written for the reader and not applied to the author's own
columns."* **Nothing was landed quietly.**

---

## 4. THE INCIDENTAL CLEANUP STAYED INCIDENTAL — PROVED BYTE-EXACTLY

I diffed the whole file rather than trusting the commit's own account. **`STATE.md`
changed in exactly two ways and no others:**

```
changed lines in 1..166: [115]          <- row 8, and nothing else
inserted at after-lines 167, 168        <- the two new rows
tails identical:          True          <- every line after the insert, byte-for-byte
```

`git numstat` = **3 insertions, 1 deletion**, which is the arithmetic of "two rows added,
one row's line rewritten" and admits nothing else.

**Row 8, word-diffed:** exactly **one deletion, zero insertions, zero reorderings.** The
removed span is the duplicated sentence and nothing adjacent to it:

> `` `λ_std→1` is a stronger rendering that happens to be available, not the requirement. ``

Count in row 8: **before = 2, after = 1.** Byte delta = **−88**, which is that sentence
plus its separating space and no more. **A ticket that arrived to add two rows added two
rows.** It did not exceed its brief.

---

## 5. THE FORBIDDEN GROUND IS UNTOUCHED, AND THE GUARDS SURVIVED BYTE-IDENTICAL

Row 11, rows 3b and 10, lines 76 and 81, and `:164`'s `C₃`/optimistic rider are
**byte-identical**, which follows from §4's structural result and which I also checked
line-by-line. The two new rows contain **zero** occurrences of `C₃`, `C_3`, `ε_dem`,
`row 11`, `L4`, `3b`, or `row 10`.

The real exposure was inside **row 8**, the one cell that *was* edited — its fourth edit
in one day. Byte-exact substring counts, before vs after:

| guard | before | after | |
|---|---|---|---|
| mg-5ce3 `NO `N₀` WORKS FOR THE CLASS AT ALL` (row 8) | 1 | 1 | **survives** |
| mg-5ce3, axis bullet + `:15` renderings | 2 + 2 | 2 + 2 | **survives** |
| mg-d1a2 `DO NOT CITE THE LITERATURE BOUND…` (full sentence, Peczarski + Gupta) | 1 | 1 | **survives** |
| mg-d1a2 *"an unspecified threshold is not a size any number can exceed"* clause | 1 | 1 | **survives** |
| mg-d1a2 `n ≥ 100` / `n ≈ 900C` thresholds | 1 | 1 | **survives** |

**Four edits to row 8 in one day and both guards are still exactly the bytes they were.**

---

## 6. IT DID NOT DECIDE WHICH `1/6` DANIEL MEANT

Both sites survive byte-identical: row 8's *"**Which `1/6` was meant is Daniel's question
and is NOT decided here; the map is true either way.**"* and `:15`'s *"**WHICH `1/6` WAS
MEANT IS NOT DECIDED HERE** — that question is Daniel's and is with him"*.

The new rows use `1/6` six times and **not once as the units question**: four are the
witness's own arithmetic (atom mass `1/6`, `q_(1,4) = 1/6`, `E[inv] = 11/6`), one is the
`11/6` scope limit, and the last is inside the *voided* threshold quote *"Daniel's `1/6`
at `n ≥ 11`"* — which the row immediately voids, printing **no** replacement number.
**The question is left exactly where mg-9adf left it.**

---

## 7. TWO OBSERVATIONS — NEITHER IS A DEFECT

**(i) The `n = 3..20` parenthetical in `(b)` is the row's one legibility soft spot.**
The claim is true (§2.2) and the same sentence says *"BOTH DIRECTIONS, with no solver on
either side"*, which cannot be said of a finite check — so the sentence is self-correcting.
But in a document whose standing rule is precisely *don't let a finite population read as
a universal*, a hostile reader meeting *"checked … at every `n` from 3 to 20"* could take
it for the warrant. If a future landing touches this cell, naming it *"mg-200d's Theorem
4.2, a construction proof for every `n` (confirmed numerically at `n = 3..20`)"* would
close the gap. **Not a correction — the row is right as it stands, and I am not filing it
as one.**

**(ii) mg-b488's disclosed line-ref decay is real, exactly `+2`, and BENIGN — its own
report ran pessimistic.** Inserting two rows shifts everything from the old `:167` down
by 2, so `STATE.md:179` and `STATE.md:203`, cited from `mg-6bc2`'s and `mg-200d`'s docs,
now point 2 lines high. Verified: the `(R)` residual moved `:179 → :181`, the cyclic
identity's section `:203 → :205`. **But both refs still land inside the block they name** —
`:179` now hits the `(R)` heading line itself and `:203` the `### Why 1/3` heading whose
section holds the identity. The cost was disclosed accurately and is smaller in effect
than the ticket claimed. **Erring toward self-criticism is the right direction and I
record it as such.**

---

## 8. WHAT I DID NOT DO

- I did **not** re-run mg-131e's or mg-200d's instruments, nor the `8 + 64 + 1024`
  branch certification, nor mg-ba78's LP. The `n = 6` witness and the 3-atom fence I
  rebuilt from scratch; **every other figure is a source read, not a re-measurement** —
  the same evidence bound row `:110` keeps for `166`/`0/132`, and I keep it here.
- I did **not** verify the `(5n−8)/12` sub-family at `n = 7,8,9,10`, the `52`
  value-positive `n = 5` branches, the `99.5%` vacuous-certificate figure, or the
  `0, 0, 2` informative sequence beyond confirming each is printed at source.
- I did **not** re-audit mg-6bc2's Claim 3.1 / Claim 4.1, which row `:168` explicitly
  places out of dispute and does not re-derive.
- I did **not** read mg-b488's ticket body or verdict mail before auditing, by design —
  every figure above was reached from `STATE.md` and the three source documents.
- I did **not** touch `STATE.md`. This audit adds one file and changes nothing else.
- Part 3 of mg-b488's brief was deliberately not landed (mg-94c3 outstanding);
  I confirmed `:164`'s rider is unchanged and did **not** evaluate that decision.

---

## VERDICT

**CONFIRMED.** `STATE.md` at `491d42c79f7628c18cb7a5d197faa9f4600cd6c1`.

Both rows are factually right at their sources, both carry their kind **at** the claim,
the `2/(n+1)` formula is legible as **FALSE** at all four of its occurrences with the
status ahead of the formula in three of them, the published `0, 6, 8, 10` appears only
as an explicitly-superseded figure, P6's rescoring landed as a rescoring with the
flattering direction intact, the incidental edit removed one duplicated sentence and
touched nothing else, and every guard and every forbidden cell survives byte-identical.

**The overclaim I was sent to find is not there — and the reason is that mg-b488
declined to obey the part of its brief that would have created one.**
