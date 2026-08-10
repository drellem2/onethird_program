# OneThird — `mg-3bb9`'s INDEPENDENT AUDIT of `mg-b58d`'s SEVEN LANDED REPAIRS — **THE UNDER-CLAIM REVERSAL SURVIVES EVERY ATTACK I COULD BUILD ON IT AND IS NOW MEASURED BY SOMETHING THAT COULD HAVE FAILED**, because the measurement `mg-b58d` cites for it is a **TAUTOLOGY**; **P11 DID NOT FLIP — the bet is worded `n ≤ 6` and the rescore uses `n = 7`**; and the self-referential blanket that `mg-b58d` repaired at §10 **is still standing at §0, ten lines above the table that falsifies it**

**Work item:** `mg-3bb9` — the independent audit of `mg-b58d` (branch `polecat-qb58d`,
commit `b45aad8`, landed on `origin/main`, one file, `+329/−29`).
**Instrument:** `code/l2_underclaim_audit_3bb9/` — `lib3bb9.py`, written from the
definitions, sharing no line with `lib28ff.py`, `lib29fe.py` or `lib51f4.py`.

---

## §0. VERDICT

> **CONFIRMED WITH REPAIRS.** The largest claim `mg-b58d` landed — the UNDER-claim reversal,
> *"`V00 = ρ` exactly, so without the two steps the L2-free route collapses back onto L2"* —
> is **true, and I have now measured it with an instrument that could have contradicted it**,
> which `mg-b58d`'s own citation could not. **Three landed statements are wrong**, one of them
> a live prediction scored in the bettor's favour on a range its own wording excludes. Nothing
> here withdraws a figure: every number `mg-b58d` landed traces to a file, and I found **no**
> number introduced without a source.

| | what I attacked | outcome |
|---|---|---|
| **1** | the UNDER-claim reversal (repair 6) | **CONFIRMED, and strengthened** — re-derived, not re-read; but the **cited measurement is vacuous** (repair **A**) |
| **2** | did P11 flip from LOST to WON? | **NO. The flip is REFUTED** — P11 is worded `n ≤ 6` and is **LOST**, unambiguously (repair **B**) |
| **3** | is the self-referential fix complete? | **NO — §10 was repaired, §0's identical blanket was not** (repair **C**) |
| **4** | is the negative's candidate space right? | **the negative HOLDS**, over a space I widened from 5 strings × 3 files to every file in the repo that names `28ff` plus 14 derived strings |
| **5** | was a figure introduced without a source? | **NO.** Every added figure traces to a file; one precision caveat is short by one row (repair **D**) |
| **6** | the OVER-claim (repair 5) | **CONFIRMED**, reproduced independently (`192` versus `1`) |
| **7** | *(not on `mg-b58d`'s disclosure list)* repair 3's own population labels | **WRONG — a labelling repair carrying a labelling defect** (repair **E**) |
| **8** | *(not on the list)* is *"(M♯) is FALSE at `n = 7`"* supported? | **ATTACKED AND SURVIVED** — but the file `mg-28ff` cites says the opposite; the resolution is one document away |

---

## §1. THE UNDER-CLAIM REVERSAL — CONFIRMED, AND THE MEASUREMENT BEHIND IT REPLACED

`mg-b58d` landed, at §2 and §7 R5:

> **`V00 = ρ` exactly.** So `mg-76b2`'s un-sharpened sweep, applied to a monotone vector,
> certifies `C₃ = 1` at a poset **iff `ρ ≤ 1`, i.e. iff L2's first disjunct holds** — *"and
> the measurement confirms it exactly: V00's failure counts `0, 0, 10, 166, 3164` equal the
> L2-failure counts at every `n` and sum to `3340`"* — **and it moves the first failure from
> `n = 5` to `n = 4`.**

### 1.1 It is an identity, not a coincidence at the measured `n`

Two facts settle it before any computation, and both are checked below rather than asserted:

* **`ρ ≥ 1` always.** `ψ_k(i) = k/n − 1[i<k]` is centred, so the monotone cone lies **inside**
  `1^⊥`; a minimum over a subset of `1^⊥` cannot beat the minimum over `1^⊥`. Hence
  `μ_pref ≥ 1−λ_std`, i.e. `ρ ≥ 1`, with equality **iff** some minimiser is monotone — which
  is L2's first disjunct in its own existential wording.
* **`V00 = ρ` is algebra.** Drop both steps and `mg-76b2`'s chain gives `Φ*² ≤ 2R(h)`, so
  `c = 2μ_pref / (2(1−λ_std)) = ρ`. `Δ_P` cancels because it was never introduced; the
  `−E(h)` term cancels because it was discarded.

Measured, on `lib3bb9`, at **all 4377** primitive posets `n ≤ 6`
(`code/l2_underclaim_audit_3bb9/out_a1_reversal.txt`):

| check | result |
|---|---|
| `Σ c_k ψ_k` is nondecreasing **iff** `c ≥ 0` | 1364 coefficient vectors, **0 mismatches** — the cone really is the monotone cone |
| `min ρ` over every primitive poset `n ≤ 6` | **`1.000000000000`** — never below 1 |
| the four cells computed **from the raw bounds** (`2R`, `2Δ_P R`, `R(2−R)`, `R(2Δ_P−R)`) versus **from the closed forms in `ρ`** | **0 disagreements** at 4377 posets — so `V00 = ρ` is verified, not assumed |

### 1.2 The counts reproduce exactly, on code that shares nothing with the counts' author

| `n` | primitive | `V11` | `V10` | `V01` | `V00` | **L2 fails, decided WITHOUT `μ_pref`** |
|---|---|---|---|---|---|---|
| 2 | 1 | 0 | 0 | 0 | 0 | 0 |
| 3 | 4 | 0 | 0 | 0 | 0 | 0 |
| 4 | 27 | 0 | 0 | 0 | **10** | **10** |
| 5 | 275 | 0 | **6** | 0 | **166** | **166** |
| 6 | 4070 | 0 | **192** | **1** | **3164** | **3164** |
| **sum** | **4377** | **0** | 198 | 1 | **3340** | **3340** |

Maxima, six decimals, identical to `mg-29fe`'s `out_s3_counterfactual.txt` in every cell:
`V11 0.943151`, `V10 1.156724`, `V01 1.028754`, `V00 1.217605` at `n = 6`.

### 1.3 **REPAIR A — THE CITED MEASUREMENT CANNOT FAIL, AND THAT IS WHY I BUILT ONE THAT CAN**

`mg-b58d` cites `code/l2_audit_29fe/out_s3_counterfactual.txt` for *"the measurement confirms
it exactly"*. In `s3_counterfactual.py` the `L2 fails` column is computed as

```python
        if rlo > 1:
            l2_fail += 1
        ...
        lowb = {"V00": rlo, ...}
        ...
            if lowb[k] > 1:
                cnt[k] += 1
```

— **`l2_fail` and `cnt["V00"]` are the same predicate on the same number.** The verdict line
*"its failure count EQUALS the L2-failure count at every n: True"* is therefore **incapable of
printing `False`**. Nothing is wrong with `mg-29fe`'s *arithmetic*; what is wrong is that a
document points at that line as the confirmation of the equivalence, when the line assumes it.

The equivalence has **real** corroboration, and `mg-b58d` did not cite it either: `mg-28ff`'s
own `out_b2_census.txt` counts L2 failures by a **different** route (`μ_pref == 1−λ_std` on
`lib28ff`) and reads `10 / 166 / 3164` at `n = 4,5,6` and `3340` pooled.

This audit adds a third, and the only one that never mentions `μ_pref` at all: take the
**eigenspace of the pencil's smallest eigenvalue** and ask whether it contains a nonzero
vector with all `ψ`-coefficients `≥ 0` — L2's first disjunct as L2 words it, decided by
alternating projection with a **constructive witness**. It returns `0/0/10/166/3164 = 3340`
and agrees with the `V00` column at **every `n` and at every poset** (`disagree` column, 0
throughout). *That* is a check that could have failed; it did fail, once, against my own code
(see the instrument README, D1).

### 1.4 *"first failure moves to `n = 4`"* — verified at `n = 4` directly, with no float

`a2_n4_exact.py` re-decides all 27 primitive posets on 4 elements with **no float on the
verdict path**: `1−λ_std` bracketed by exact bisection on PSD (all principal minors of an
exact rational matrix), `μ_pref` by exact bisection on **strict copositivity** of `Q − tN`
over the cone (exact minimum of `c'(Q−tN)c` over the standard simplex, every face).

```
  CERTIFIED rho > 1  (V00 FAILS, and L2's first disjunct fails):  10
  CERTIFIED rho = 1 within 2^-20 (V00 certifies; L2 holds):       17
  UNDECIDED:                                                       0
  other variants' certified failure counts at n = 4:  {'V11': 0, 'V10': 0, 'V01': 0}
```

with `ρ` brackets of width `0` at all ten (e.g. `[(0,1),(2,3)]` at `ρ = 1.085410197`, the
`n = 4` maximum). **Confirmed, and the ten are exhibited by relation set** in the output.

### 1.5 And `3340` is one population, not two that agree

`4377 = 1+4+27+275+4070` and `3340 = 10+166+3164` are both over the **same** set — the
primitive naturally labelled posets on `n ≤ 6` — enumerated three times now (`lib28ff`,
`lib29fe`, `lib3bb9`) with the same per-`n` counts. There is no second population in the
neighbourhood for the sum to be coincidentally equal to. **`mg-b58d`'s strongest sentence is
its truest one.**

---

## §2. **REPAIR B — P11 DID NOT FLIP. THE BET IS WORDED `n ≤ 6`, AND THE RESCORE IS OUTSIDE IT**

`mg-b58d` rescored a live `0.35` bet from **LOST** to **WON**. The bet, verbatim, at
`code/l2_conditionality_28ff/PREDICTIONS.md:108`:

> **P11 [BET, 0.35].** Even restricted to primitive posets the footrule route fails
> somewhere at **`n ≤ 6`**.

**The scope is in the bet's own sentence, and it is not ambiguous.** At `n ≤ 6` route (F)
certifies **4377 of 4377** — the document's own §4.3 table, exhaustive, exact, and unchanged
by this repair. **P11 is LOST.** The exhaustive `n = 7` result (F fails at 168 of 86278) is a
real and important fact; it is not a fact about P11.

What made the flip look admissible is a **scope-dropped paraphrase**, and it was dropped in
the parent, not by `mg-b58d`:

| | §9's `bet` column |
|---|---|
| before `b45aad8` | *"it fails somewhere on primitive posets too"* |
| after `b45aad8` | *"route (F) fails somewhere on primitive posets too"* |

Neither carries `n ≤ 6`. The repair then reasoned against the paraphrase rather than the bet,
and reached *"a live bet at 0.35 that I recorded as lost was in fact **right**"*. **This is the
same defect class the repair exists to fix** — a claim read outside the population that
licenses it — one row over from §4.3, running in the direction that flatters the bettor. The
original scoring's **reason** (*"100 % at every `n ≤ 7` tested"*) was indeed over-reaching, in
the other direction; its **verdict** was right.

**The sharpest form of the finding is an asymmetry, not a slip.** P4's cell drops the same
`n ≤ 6` from the same `PREDICTIONS.md` (*"`c* ≤ 1` — i.e. (M) holds at every primitive poset
**at `n ≤ 6`**"* → *"`c* ≤ 1`"*), and P4 is nonetheless scored **at `n ≤ 6`, as filed** — which
is correct, and which is also the only scoring under which it can be a **WIN**, since
`c♯ = 1.018707 > 1` at the exhaustive `n = 7`. **Applied to P4, the reading that wins P11 loses
P4.** It was applied to exactly one of them: `b45aad8` edits **one** row of §9's fourteen, and
it is the row where unscoping pays.

> **PROPOSED REPLACEMENT** — `docs/OneThird-L2-Conditionality-mg-28ff.md:742`
>
> **current:** `| P11 (0.35) | route (F) fails somewhere on primitive posets too | **SCORED
> LOST HERE ON A SAMPLE, AND IT IS WON ON THE TRUTH.** … A live bet at 0.35 that I recorded as
> lost was in fact **right**, and I could not see it because I was scoring against a sample. |`
>
> **replacement:** `| P11 (0.35) | *"Even restricted to primitive posets the footrule route
> fails somewhere at `n ≤ 6`"* (`PREDICTIONS.md:108` — the `n ≤ 6` is the bet's own and was
> dropped from this cell in the original) | **LOST, and it stays lost.** (F) certifies at
> 4377 of 4377 primitive posets `n ≤ 6`, exhaustively and exactly, which decides the bet as
> worded. The old **reason** — *"100 % at every `n ≤ 7` tested"* — was a sample read as an
> enumeration and is withdrawn: at `n = 7` exhaustively (F) FAILS at 168 of 86278 (`mg-51f4`).
> **The bet named `n ≤ 6` and lost there; the `n = 7` failure is outside its range and does
> not win it.** What P11 got right was the *mechanism*, one `n` later than it bet on. |`

---

## §3. **REPAIR C — THE SELF-REFERENTIAL SITE IS FIXED AT §10 AND STILL BROKEN AT §0**

`mg-b58d` reports, correctly, that §10's *"no `n = 7` number in this document is a maximum"*
became false the moment it printed exhaustive rows, and repairs it (`:781`). **The same
sentence, in the same document, at §0, was not repaired** — and it is the one a reader meets
first:

`docs/OneThird-L2-Conditionality-mg-28ff.md:61–63`, **unchanged by `b45aad8`**:

> The `n = 7` figures in this document come from named families plus a deterministic sample of
> **90–200** posets out of a population of order 10⁶, so **the `n = 7` rows are not maxima and
> must never be read as if they were.**

**Ten lines below it**, the block `b45aad8` added prints three `n = 7` rows that **are**
maxima (`c_true 0.340719`, `c♯ 1.018707`, `f* 1.297074`, all exhaustive over 86278) — in §0's
own table. Both clauses of that sentence are now false of the document: the `n = 7` figures do
**not** all come from families plus a sample, and the `n = 7` rows are **not** all non-maxima.
And `:81`, added by the same commit, asserts *"the blanket labelling in **this paragraph** and
in §10 **was right**"* — one of the two it names was repaired for being wrong.

This is exactly the recursion `mg-b58d`'s own §0.0 says it checked for (*"this is a labelling
repair, so it can carry a labelling defect"*). The check it ran was over **figures** — every
`n = 7` figure carries `SAMPLE`/`EXHAUSTIVE`, its provenance, and its size — and every figure
does. The defect is not in a figure; it is in a surviving **universal quantifier over the
rows**, which no per-figure check can see.

> **PROPOSED REPLACEMENT** — `:61–63`
>
> **current:** *"The `n = 7` figures in this document come from named families plus a
> deterministic sample of 90–200 posets out of a population of order 10⁶, so **the `n = 7` rows
> are not maxima and must never be read as if they were.**"*
>
> **replacement:** *"**This instrument's** `n = 7` figures come from named families plus a
> deterministic sample — two different draws, **98 and 208 posets** (`named_posets(7)` plus
> `sample_posets(7, 90)` / `sample_posets(7, 200)`) — out of a population of order 10⁶, so
> **no `n = 7` row produced by `lib28ff.py` is a maximum and none may be read as if it were.**
> The `n = 7` rows labelled **EXHAUSTIVE** in §0, §4.1, §4.2 and §4.3 **are** maxima; they are
> `mg-51f4`'s, over all 86278 primitive posets on `[7]`, and are attributed at every
> appearance."*
>
> and at `:81`, *"The blanket labelling in this paragraph and in §10 was right"* →
> *"**The warning** in this paragraph and in §10 was right, and by a wide margin — though the
> blanket **form** of both sentences became false the moment exhaustive rows were printed
> beside them, and both are re-scoped above."*

A secondary site of the same shape, offered but not pressed: `:50` reads *"My exhaustive
evidence stops at `n = 6` and my `n = 7` evidence is a sample"* in the **same table** whose row
`:49` now quotes exhaustive `n = 7` maxima. The possessive carries it, but §10's repair chose
the explicit *"**this instrument's**"* and parity would cost one word.

---

## §4. THE NEGATIVE — IT HOLDS, OVER A CANDIDATE SPACE I HAD TO WIDEN FIRST

`mg-b58d` re-verified by grep that `STATE.md`, `docs/roadmap.md` and
`docs/state-of-the-wall.html` contain none of `mg-28ff`, `0.943151`, `0.811654`, `0.327508`,
`c_true`. **Five strings, three files.** A clean grep over the wrong population reads exactly
like a clean grep over the right one, so I established the population first:

* **every file in the repo that names `28ff`** (outside `.git`, `lib28ff`'s own directory and
  the audited document): `code/l2_audit_29fe/*`, `code/sweep_loss_51f4/*`,
  `docs/OneThird-L2-Conditionality-mg-29fe-IndependentAudit.md`,
  `docs/OneThird-SweepLoss-mg-51f4.md`. The two documents are the **audit that proposed these
  repairs** and the **instrument that supplied the exhaustive rows** — siblings that carry the
  figures by design, not downstream consumers with stale copies.
* **derived carriers that contain none of the five strings**, over the three named files:
  `0.943`, `0.812`, `0.811`, `0.327`, `0.340`, `86278`, `4377`, `3340`, `1890`, `1037`,
  `L2-free`, `without L2`, `monotone cone`, `(M♯)`, `3.05`, `footrule`. **All absent**, with
  one true-negative worth recording so nobody re-walks it: `footrule` **does** occur in
  `STATE.md` and in `state-of-the-wall.html`, in the `mg-8311`/inversions sense
  (`max{3E[footrule]/(n²−1)}`), **not** route (F).
* `STATE.md:169` is the only place the corpus states the `C₃` result. It is sourced entirely
  to `mg-76b2`/`mg-94c3`, cites `3340` to `mg-94c3`'s red drill, and carries **no** `mg-28ff`
  figure.

**So the negative is CONFIRMED and it is now a negative over the right space.** One standing
gap, which is `mg-28ff`'s by declaration (§10: *"proposals for whoever owns those files, not
landings"*) and not a defect of this repair: `STATE.md:169` still reads **"REDUCES `C₃` TO L2
— IT DOES NOT DISCHARGE L2"** with no mention that two L2-free routes now sit under `C₃ = 1`,
that both are individually **false at `n = 7`**, and that their **disjunction survives at
86278 of 86278**. The ledger is stale in the direction of understating the corpus.

---

## §5. THE CONVERSE — NO FIGURE WAS INTRODUCED WITHOUT A SOURCE

`mg-b58d` checked that every figure in a **replaced** sentence reappears in its replacement.
I checked the other direction: every numeric token the diff **added**, against the repo.

| figure | source |
|---|---|
| `0.340719`, `1.018707`, `1.297074`, `168`, `86278`, `96428`, `0 of 86278` (disjointness) | `code/sweep_loss_51f4/out_s3_n7.txt` |
| `0.753639`, `0.550747`, `0.811649` | `code/sweep_loss_51f4/out_s1_census.txt`, `code/l2_audit_29fe/out_s1_truth_and_sweep.txt` |
| `1.221325`, `1.055556` | `code/l2_audit_29fe/out_s6_verify_q51f4.txt` |
| `1.156724`, `1.028754`, `1.217605`, the four failure columns | `code/l2_audit_29fe/out_s3_counterfactual.txt` |
| `0.752421`, `0.825114`, `0.950000`, `0.900000`, `14.1 %` | `code/l2_audit_29fe/out_s1_truth_and_sweep.txt` (the `14.1 %` at `:58`) |
| `48318`, `65396`, `21120`, `36116`, `5906`, `260` | `code/l2_audit_29fe/out_s4_theorem_and_quantifier.txt` |
| `0.850074`, `0.176145`, `0.832530` | `out_b2_census.txt`, `out_b5_trend.txt`, `out_b1_footrule.txt` (as `0.83253`) |
| `86110` | derived: `86278 − 168`, arithmetic, and correct |

**No orphans.** The one figure that is not in any file is `86110`, and it is a subtraction of
two that are.

> **REPAIR D (minor) — the precision note is short by one row.** The added R7 note says
> `b1_footrule.py:77` brackets `f*` in **20 steps over `[0,4]`** (`3.8e-6` wide) and that the
> instrument printed **five** decimals where six are shown, then gives exact values for the
> `n = 5` and `n = 6` rows (`0.550747`, `0.811649`). The **`n = 7` sample row in the same
> table, `0.832530`, came off the same line of the same bisection** (`out_b1_footrule.txt:38`
> prints `0.83253`) and still shows a padded sixth decimal under a column headed `EXACT`,
> uncaveated — and §0's new table quotes it too. **Replacement:** append to the note — *"and
> the `n = 7` sample row `0.832530` is the same five-decimal print padded, from the same
> bracket; it is a sample and is not a maximum, so no exact value is quoted for it."*

---

## §6. THE OVER-CLAIM — CONFIRMED, AND REPRODUCED RATHER THAN READ

`mg-b58d`'s repair 5 now reads: R5 keeps `Δ_P` and discards only `−E(h)`, so it is the **V10**
cell, establishes **S2** only (`6 of 275` at `n = 5`, `192 of 4070` at `n = 6`), and says
nothing about **S1**; the untested **V01** first fails at `n = 6` at **1 of 4070**; so *"both
are load-bearing"* is true **and true only from `n = 6`**, and the two are unequal by two
orders of magnitude. On `lib3bb9`: **V10 `0/0/0/6/192`**, **V01 `0/0/0/0/1`**. `192` against
`1`. **Every clause holds**, including the `n = 5` clause (`S1` is not load-bearing at all at
the `n` where the old sentence made its claim), and §7's R5 row now scopes itself to the V10
cell so the cited evidence is no longer asked to carry the `Δ_P` half. **Confirmed.**

---

## §7. **REPAIR E — REPAIR 3's OWN POPULATION LABELS ARE WRONG.** *(Not on `mg-b58d`'s disclosure list.)*

Repair 3 exists because §4.2's `n = 7` row was a *different sample* from §4.1's and §4.3's and
that was unstated. The repaired labels attribute the primitive counts to the **draw**:

> §4 `:284` — *"`sample_posets(7, 90)` (**40 primitive**) feeds §4.2, and `sample_posets(7,
> 200)` (**106 primitive**) feeds §4.1 and §4.3"*
> §4.1 `:317`, §4.3 `:385` — *"106 primitive of **200 drawn**"* · §4.2 `:343` — *"40 primitive
> of **90 drawn**"* · §8.1 `:712–714` — *"draw / primitive: `200 / 106`, `90 / 40`"*

But the three scripts evaluate **`named_posets(7) + sample_posets(7, k)`**
(`b1_footrule.py:73`, `b2_census.py:138`, `b5_trend.py:48` — the very lines the repair cites).
Asked of `lib28ff`'s own generators (`out_a3_n7_population_label.txt`):

| | posets | primitive |
|---|---|---|
| `named_posets(7)` | 8 | **5** |
| `sample_posets(7, 90)` | 90 | **35** |
| **the population §4.2 actually evaluates** | **98** *(97 distinct; 1 duplicate, decomposable)* | **40** |
| `sample_posets(7, 200)` | 200 | **101** |
| **the population §4.1/§4.3 actually evaluate** | **208** *(207 distinct)* | **106** |

So *"40 primitive of 90 drawn"* attributes to the draw a count the draw supplies **35** of;
the other **5 are named families — chosen, not drawn** — and likewise `106 = 101 + 5`. The
population sizes are **98** and **208**, not 90 and 200.

Two corroborations from inside the same material, which is why this is a defect and not a
reading: **`lib28ff`'s own output** labels the row *"n=7 [named + sample, 106 primitive]"*
(`out_b1_footrule.txt:38`), and **§3 of the same document** states the union size correctly —
*"machine-checked at all 5230 posets `n ≤ 6` and **98** at `n = 7`"* — while §4, §4.1, §4.2,
§4.3 and §8.1 state the draw size instead. The repaired label is a step **away** from what the
instrument printed.

**Material?** Modestly, and in the direction that matters: a row labelled *"a sample of 200"*
that silently contains five **hand-chosen** family members is a population conflation of
precisely the kind repair 3 was written to end. **Replacement:** *"106 primitive of the 208
evaluated — `named_posets(7)` (8, of which 5 primitive) plus `sample_posets(7, 200)` (200, of
which 101) — SAMPLE PLUS NAMED FAMILIES, NOT a maximum"*, and the same at §4, §4.2 (`40 of
98 = 5 + 35`) and §8.1's table.

---

## §8. ATTACKED AND SURVIVED — *"BOTH HYPOTHESES ARE FALSE AT `n = 7` INDIVIDUALLY"*

The claim runs through §0 `:49`, §4.2 `:357`, §8.1 `:673–679` and `b45aad8`'s own subject. It
looked to me like the biggest unexamined over-claim in the landing, because the file
`mg-28ff` **cites for it** says the opposite in its own words —
`code/sweep_loss_51f4/out_s3_n7.txt:32,106–108`:

```
  c#      (route (M#); UPPER bound -- exhibited vector) = 1.018707
  primitive posets at n=7 where route (M#) fails on the exhibited
      vector (c#_upper > 1; an upper bound, so this OVERCOUNTS):           4 of 86278
```

An **upper** bound on `c♯` exceeding `1` cannot refute `(M♯)` — a better monotone vector could
put it back under — and `mg-51f4` itself states the asymmetry elsewhere (`8b49a78`: *"an
exhibited-vector UPPER bound … can certify that (M♯) holds and can NEVER certify that it
fails"*). `mg-28ff` §10 states the same caveat about its own column.

**It survives**, because `mg-51f4`'s **document** closes the gap that its output file leaves
open (`docs/OneThird-SweepLoss-mg-51f4.md` §5): *"at all 4 posets with `c♯_upper > 1` the exact
bracket confirms genuine failure"*, with the extremal witness carrying an exact copositivity
bracket `μ_pref ∈ [0.226537524, 0.226537524]`. So `(M♯)` is genuinely false at `n = 7`, at
exactly 4 posets, and `c♯(7) = 1.018707` is a maximum and not merely a ceiling.

**What is defective is only the citation.** A reader following §0's pointer to
`out_s3_n7.txt` lands on the word `OVERCOUNTS` and cannot get from there to the claim. One
clause fixes it: cite `mg-51f4` §5 beside the output file wherever `(M♯)`'s `n = 7` failure is
asserted.

---

## §9. WHAT I RANGED OVER, AND WHAT I DID NOT

**Ranged over.** The full `b45aad8` diff, token by token, in both directions (survival of old
figures; sourcing of new ones). All 4377 primitive posets `n ≤ 6` on an independent
instrument, four route variants, two independent L2 censuses, one of them exact at `n = 4`
with no float on the verdict path. `PREDICTIONS.md` for all fourteen bets' wording against
§9's paraphrases. **P11 is not the only cell that drops a scope — but it is the only one where
the dropped scope is what the new verdict rests on, and the asymmetry is the point.** P4's
cell also paraphrases *"`c* ≤ 1` — i.e. (M) holds at every primitive poset **at `n ≤ 6`**"* as
*"`c* ≤ 1`"*; P4 is nevertheless scored **at `n ≤ 6` as filed**, and rightly. Read unscoped —
the reading that won P11 — **P4 would LOSE**, because `c♯ = 1.018707 > 1` at the exhaustive
`n = 7`. The same commit that unscoped the bet that thereby wins left scoped the bet that
would thereby lose. `b45aad8` touched **exactly one** row of §9's table, and it is P11's. Every file in the repo naming `28ff`. Sixteen derived strings across the three declared
consumer files. `b1_footrule.py`, `b2_census.py`, `b5_trend.py` at the cited lines.
`s3_counterfactual.py` in full. `out_s3_n7.txt` and `mg-51f4` §5 for the exhaustive rows.

**Not done, and it is the largest thing still unverified in the deliverable.** **I did not
re-run the exhaustive `n = 7`.** `0.340719`, `1.018707`, `1.297074`, `168 of 86278`, `96428`
and the disjointness `0 of 86278` are verified here as **faithful copies** of
`out_s3_n7.txt` — copies, not truths. `mg-29fe` re-verified the two extremal witnesses on a
third instrument; the *maxima* rest on `mg-51f4` alone. A 21×-larger population than anything
`mg-28ff` enumerated is carrying four of this document's headline numbers on **one**
instrument's word, and no gate in this repository has ever looked at it.

**Also not done:** I did not re-derive `c_true`, did not touch route (F)'s footrule identity
beyond reading it, did not re-run `mg-29fe`'s T1–T4 arms, and did not open `libA94.py` or
`lib76b2.py`. The `1032`-vs-`1037` discrepancy stays open and is still not mine to close.

**Two defects of my own**, both kept and both described in the instrument README: **D1**, a
replacement control that reported the `n = 5` antichain as L2-failing because my eigenspace
search spanned 3 of `d` dimensions — I nearly published a one-poset crack in the identity that
was my sampler; **D2**, `simplex_min` skipping singular faces, which could have inflated
`μ_pref`'s lower bracket and manufactured failures.

**And the finding about the process, which `mg-b58d` filed against itself and I repeat because
it is now twice-observed:** `mg-b58d` landed on `main` through a refinery reporting *"(no
quality gates configured)"*, re-ran no instrument, and its audit was filed **after** the fact.
Two of the three defects above (**B** and **C**) are ones a re-read of the diff against its own
sources would have caught in minutes. The gap is not effort; it is that nothing in the
pipeline requires the re-read to happen before the merge.

---

*`mg-3bb9`. Instrument: `code/l2_underclaim_audit_3bb9/` — `lib3bb9.py` written from the
document's own definitions, sharing no line with `lib28ff.py`, `lib29fe.py` or `lib51f4.py`;
`a1` (4377 posets, four variants, two L2 censuses), `a2` (`n = 4`, exact, 0 undecided), `a3`
(the `n = 7` population labels against their own generators). **No figure withdrawn; five
repairs proposed; none landed.***
