# THE `(L*)` REFUTATION, LANDED — and the two things the ticket got wrong are both worth more than the landing

**Work item.** `mg-8d63`, filed by `pm-onethird` off `c789d`'s verdict on `mg-789d`
(`c689ad0`, outcome (b)). `c789d` deliberately did **not** touch `STATE.md` or `roadmap.md`
on the ground that a headline reversal should get its own landing ticket with an audit.
This is that ticket. `roadmap.md` was corrected by `pm-onethird` itself at `e797b50` and is
**not** re-done here.

---

## 0. THE TWO HEADLINES, AND NEITHER IS THE ONE THE TICKET EXPECTED

**(1) `STATE.md` NEVER CARRIED THE REFUTED CLAIM. THERE WAS NOTHING THERE TO STRIKE.** The
ticket's premise — *"`STATE.md` and every doc asserting the disjunction is ONE INEQUALITY
are now FALSE"* — is **false of `STATE.md`**, and the sweep that establishes it is §1 below.
The `(F)`/`(M♯)`/`(L*)` thread was **absent from the canonical state document entirely** —
not stated wrongly, not stated with the wrong scope: **absent**. What this landing does at
`STATE.md` is therefore an **ADDITION** (one attempt-index row), not a repair, and it is
labelled as one in the row itself so that no future reader takes the row's existence as
evidence that the claim was once there.

**(2) THE `ρ·Δ > 1` ONSET IS `n = 5`, NOT THE `n = 6` THE TICKET ASKED ME TO LAND.** The
ticket's second correction — *"`ρΔ > 1` occurs from `n = 6`, not `n = 10`"* — is itself an
**under-correction by one value of `n`**, and it is under-corrected **by the same defect it
corrects**. Measured exhaustively here: `ρΔ_P > 1` first occurs at **`n = 5`**, at **6 of
275** primitive posets, `max ρΔ = 1.027118`. See §3.

> **PRIORITY, STATED PLAINLY BECAUSE IT IS NOT MINE.** `mg-5cba`'s independent audit of
> `mg-789d` found the same `n = 5` onset and **landed first** (`5c0849a`), with **exact
> rational certificates at all six `n = 5` witnesses** and `μ_pref·Δ ≤ γ` certified at
> **every** primitive poset of `n = 3` and `n = 4` — so `n = 5` is *exactly* the onset and
> not merely the smallest sighting. That is strictly stronger than the float sweep here.
> `pm-onethird` swept `roadmap.md` for it at `87735c2`. This landing was rebased onto both
> and **rebuilt on `mg-5cba`'s repaired figures**, not on `mg-789d`'s as published — see
> §5, which is the more useful half of this note now.
>
> What survives here as this ticket's own is (i) the `STATE.md` negative in §1, (ii) the
> **cross-thread provenance** of §3.1 — that the number was already in the corpus as
> `mg-28ff`'s cell `V10`, which `mg-5cba` does not report — and (iii) the floor control
> `C3`, which is about the *defect class* rather than the number.

Both findings are the same shape: **a number was carried by quotation through three
documents, and the first party to measure it got a different answer.**

---

## 1. THE SWEEP — for the CLAIM, not the phrase

Run over `*.md`, `*.html`, `*.txt`, `*.py` at the repository root, on every rendering of the
claim the ticket names and on the thread's own identifiers, because *"at least one site will
state it without naming `(L*)` at all"*:

| probe | rationale | sites outside `roadmap.md` |
|---|---|---|
| `(L*)` literal | the name | `docs/OneThird-AntiCorrelation-mg-c50b.md`, `docs/OneThird-LStar-mg-789d.md`, and their two instrument dirs |
| `one inequality` / `single inequality` / `single sufficient` | the claim in words | `docs/OneThird-AntiCorrelation-mg-c50b.md` ×3 (title, §0.1, §4 header). **Two near misses, both checked and both NOT this claim:** `Op-Form`'s audit `:747` (*"Steps 4 and 5 are one inequality, not two"* — about `Φ_P ≡ Δ₁`) and `code/direct_prefix_audit_2de0/a2_lemma_b.py:1` (a docstring about audit method) |
| `uniform(ly) in n` | the claim as a quantifier | **58 hits under `docs/`, and every one is a DIFFERENT statement** — `C₃^(III) = 1 uniformly in n` (mg-76b2, mg-9461, mg-28ff `:128`/`:635`, mg-51f4 `:18`/`:350`), `1 − λ_std ≤ ε_spec` (`Op-Form`, mg-345e, mg-c3ca), `ε₀ ≤ 17/78` (mg-3969, mg-d3c7), an `λ₂(S_n)` asymptotic (mg-00b3 `:267`). **Not one is `(L*)` or the disjunction.** This is the probe that would have caught a site stating the claim without naming it, and it caught none. |
| `86278` / `2600369` / `c_or(8)` / `0.943649` | the census the claim was set against | 14 files; **none states the reduction claim** — checked file by file, not by count |
| `51f4` / `c50b` / `789d` | the thread's identifiers | no citer outside the thread's own four directories |

**RESULT: the claim lives in exactly ONE document outside `roadmap.md`** —
`docs/OneThird-AntiCorrelation-mg-c50b.md` — plus the refutation document that already
states it as refuted. It does **not** appear in `STATE.md`, in `docs/state-of-the-wall.html`,
in `README.md`, or in any of the other 158 documents under `docs/`.

### 1.1 `STATE.md` and its rendered twin — the negative, stated as a measurement

```
STATE.md                     (L*)  0    c50b 0   51f4 0   789d 0   28ff 0   29fe 0
                             86278 0    2600369 0   c_or 0   mu_pref 0   Delta_P 0
                             "one inequality" 0   "single inequality" 0
docs/state-of-the-wall.html  identical: 0 on every probe above
README.md                    0 on every probe above
```

The table above is `STATE.md` **as it stood at `8afec6d`, before this landing's own row was
added** — read it with `git show 8afec6d:STATE.md`, since the row added at `:170` now
contains `(L*)` many times over. At that commit `grep -c "(L\*)"` returns **`0`** and the
three bare `L*` hits (`:115`, `:168`, `:169`) are `ALL**` inside bold markers. They are
checked, not counted.

**This is a negative result and it is reported as one.** It is also the reason the
`STATE.md` row this landing adds is worth adding: a canonical state document that records
neither the `n = 7`/`n = 8` enumerations, nor the disjunction, nor the route that was tried
and refuted, will let the whole thread be re-walked.

### 1.2 What was deliberately left byte-identical, and why

* **`code/anticorrelation_c50b/PREDICTIONS.md`** — a **pre-registration artefact**. This
  corpus's standing convention (mg-ba78, mg-6bc2) is that predictions are never edited after
  the fact, and a correction written into one destroys the only thing it is for.
* **Every `out_*.txt` in `code/anticorrelation_c50b/` and `code/lstar_789d/`** — run records.
  **Checked rather than assumed:** none of them asserts the refuted claim. The nearest
  candidates are `out_s2_theory.txt:14` (*"TWO CONSEQUENCES, both uniform in n"* — the
  implication `ρΔ ≤ 1 ⟹ (M♯)`, which is a **theorem and is not refuted**) and `:95` (the
  obstruction theorem, untouched).
* **`docs/roadmap.md`** — `pm-onethird`'s own artifact, corrected by `pm` at `e797b50`, and
  the ticket says explicitly not to redo it. **It does, however, now carry the `n = 6`
  onset at its banner and at `:67`, which §3 supersedes. That correction is `pm`'s to
  land and has been mailed to `pm-onethird`.**

---

## 2. WHAT LANDED WHERE

| site | what was done |
|---|---|
| `STATE.md` `:170` | **NEW attempt-index row.** Both halves in the verdict column. Theorem A stated as a result with its proof mechanism, its 90655-poset check, its `4/168` coverage **and its `24/168` ceiling**. (R1)/(R2)/depth-table/`LSTAR(n)` as results. `n = 8` marked **OPEN** with `0.968818` explicitly barred from being quoted as a maximum. The row states that it is an addition and that nothing was struck. |
| `docs/OneThird-AntiCorrelation-mg-c50b.md` | **Banner** at the head; **title claim struck**; §0's *"The mechanism"* row struck with its certificates explicitly **not** withdrawn; §0.1's last clause struck; §4's header, its two blockquotes and its CONSEQUENCE block struck **with the surviving implication separated from the refuted antecedent**; §4's non-vacuity paragraph **corrected without being struck** (§3); §9's first NOT-DONE bullet replaced by the `n = 8` open item. Original text left visible throughout — it is a record. |
| `docs/OneThird-LStar-mg-789d.md` | §4's onset corrected `n = 6 → n = 5` and the ledger row at §6 with it. Nothing else touched: this document is the refutation and it is right. |
| `code/lstar_landing_8d63/` | **New instrument.** One script, four arms, exit 0. |
| `docs/roadmap.md` | **untouched, deliberately** — see §1.2. |

**NO PUBLISHED NUMBER IS WITHDRAWN ANYWHERE, AND THAT IS MEASURED, NOT ASSERTED.** Every
numeric literal present in `STATE.md`, `OneThird-AntiCorrelation-mg-c50b.md` and
`OneThird-LStar-mg-789d.md` at `8afec6d` is still present at least as many times after this
landing — multiset comparison, `0` figures lost in all three files. Every deletion in the
diff is a line re-inserted inside `~~…~~` with the correction beside it, because these
documents are **records**: the refuted text has to stay readable for *"it was claimed and it
was wrong"* to be checkable. **The two censuses did not move and were never in question** —
a refutation at `n = 9` cannot reach back into a certificate at `n ≤ 8`.

**CONTROLS RUN, BEFORE AND AFTER:**

| control | at `8afec6d` | after this landing |
|---|---|---|
| `code/rendered_twin_pin_9bc2/twin_pin.py` | exit 1, DRIFT, **row 8 only** | exit 1, DRIFT, **row 8 only** — unchanged. The row added here is in the **attempt index**, not the ledger, so no ledger-row digest moves and no new twin worklist entry appears |
| `code/state_landing_control_2da3/run_all.sh` | exit 1, **6 FAIL / 8 MOVED** | exit 1, **6 FAIL / 8 MOVED** — byte-identical verdict, i.e. pre-existing and untouched |
| `code/summary_guard_cf83/c1_summary_guard.py` | — | exit 0 |
| `code/lstar_landing_8d63/run_all.sh` | *(new)* | exit 0, all four arms |

---

## 3. THE ONSET — `n = 5`, MEASURED, AND THE DEFECT IS THE SAME ONE TWICE

`code/lstar_landing_8d63/s1_onset.py`, exhaustive over naturally-labelled primitive posets:

```
 n | primitive |  max rho*Delta | posets with rho*Delta > 1
 2 |         1 |      0.500000  |     0
 3 |         4 |      0.666667  |     0
 4 |        27 |      0.904508  |     0
 5 |       275 |      1.027118  |     6      <- ONSET
 6 |      4070 |      1.156724  |   192
```

**`mg-c50b` §4's sentence is TRUE and is NOT struck.** It says `ρΔ_P` crosses 1 at `n = 10`
**on the chain(`n−1`)+point FAMILY**, it carries the word FAMILY, and it reproduces exactly
here as control C2 — `0.98596` at `n = 9`, `1.00636` at `n = 10`, `1.07794` at `n = 16`. The
error was never in that sentence; it was in reading a family's crossing as the phenomenon's
onset, which is what the corpus then did.

**`mg-789d` §4's replacement is wrong by one `n`, and wrong by its own diagnosis.** Its `s2`
§2.4 sweeps exactly two values of `n`, 6 and 7 — because that section's question was about
the `(F)`-failing set, which is empty below `n = 7`. So `n = 6` is **the smallest `n` that
instrument looked at, published as the smallest `n` where the thing happens**: the same
defect it was correcting, one document later.

**Control C3 exists because this landing was one primitive poset from committing it too.**
The first draft of `s1_onset.py` swept from `n = 3`. `n = 2` has a primitive poset. C3 now
runs the sweep to its own floor (`n = 2`, `ρΔ = 0.5`) and **refuses** `n = 1` rather than
skipping it — `LE = 1`, so `γ = 0` and `ρ = μ_pref/γ` does not exist there. Without C3 the
`n = 5` figure would be a floor artefact in an onset's clothes.

### 3.1 The corpus already held the answer, on an instrument sharing no code

`mg-28ff`'s cell **`V10` IS `ρΔ_P`** (`docs/OneThird-L2-Conditionality-mg-28ff.md:279`;
`mg-29fe`'s audit identifies it at `:366`), and
`code/l2_audit_29fe/out_s3_counterfactual.txt` prints

```
  n |   V11 both  V10 S1only  V01 S2only  V00 neither
  5 |   0.803289    1.027118    0.963960     1.141242
  6 |   0.943151    1.156724    1.028754     1.217605
...
  * V10 (mg-28ff's own R5 cell: Delta_P kept, -E(h) discarded) first exceeds 1 at n = 5,
    at 6 of 275 primitive posets at n=5.
```

— **committed before either onset statement was written.** Every digit agrees with this
landing's independent run on `lib789d`.

**The transferable finding is not the integer.** It is that **one scalar was tracked under
two names in two threads, and neither thread could see the other's measurement.** `ρΔ_P` was
`(L*)`'s whole content in one thread and an anonymous counterfactual cell in the other. No
process in this corpus would have caught that; a person measuring the number instead of
quoting it did.

---

## 4. WHAT THIS LANDING DOES NOT DO

* **`n = 8` is not settled and is not implied to be.** Whether `(L*)` already fails at
  `n = 8` is **OPEN**. `0.968818` is 60 hill-climb restarts over 2600369 primitive posets —
  a **search**, not a census — and every site touched here says so. Any document that lets
  `0.968818` read as a maximum at `n = 8` is wrong, and none of the ones touched here does.
* **`(L*)` is not repaired by weakening.** The depth table already says any surviving
  prefix-side statement needs ≥ 2 cuts at `n = 7`, and the `n = 9` counterexample uses the
  **full** cone.
* **No re-derivation of the refutation.** The five certificates are `mg-789d`'s and
  `mg-5cba`'s and were **read, not re-run**. What was re-run here is the onset column and
  its controls.
* **`n = 7` was not swept for the onset.** An onset established at `n = 5` cannot be moved
  by a larger `n`; the `n = 7` figure would cost about an hour and could not change it.
* **`roadmap.md`** — untouched by instruction, with its `n = 6` residue mailed to `pm`.
* **No audit of `mg-789d`'s Theorem A.** Its proof is stated in the `STATE.md` row by its
  mechanism (Krein–Rutman on the monotone cone) so that a reader can check it, but this
  ticket did not re-derive it and does not claim to have. Its **`(SO)` count is `2500`,
  not `338`** — `mg-5cba` R3; `338` is the `n ≤ 6` subtotal.

---

## 5. WHAT THE REBASE CAUGHT — FOUR FIGURES THIS ROW WOULD HAVE LANDED WRONG

This landing's `STATE.md` row was first written off `mg-789d`'s document. `mg-5cba`'s audit
landed on `main` in the same window and repaired four of the figures in it. The row was
**rebuilt on the audited values before merging**, and the four are recorded here because a
landing ticket propagating a superseded figure is exactly the failure this corpus keeps
finding:

| figure | as `mg-789d` published it | as landed here (`mg-5cba`) |
|---|---|---|
| counterexamples | **four** (n=9, 9, 10, 11) | **five** — the `n = 12` row `mg-789d`'s own table claimed and never certified (R5) |
| `(M♯)` survival | *"all **three** tested"*, `u_M = 0.943 / 0.982 / 0.958` | **4 of 4**, `0.943486 / 0.947534 / 0.981830 / 0.958326` — the omitted one is `mg-789d`'s own `n = 9` **argmax** (R4) |
| `LSTAR(6)` | `0.794253` | **`0.794235`** — a digit transposition, attained at **no** primitive `n = 6` poset (R2) |
| Theorem A's `(SO)` count at `n ≤ 7` | `338` | **`2500`** — `338` is the `n ≤ 6` subtotal (R3) |
| `LSTAR(n)`, `n ≥ 8` | *"lower bounds from search"* | **UPPER** bounds as computed (`mu_ub_float`); the lower bounds are `mg-5cba`'s exact recertifications (R6) |

**The general point is the one this whole ticket keeps hitting.** A landing ticket's job is
to carry a result outward, and carrying is the operation that propagates a wrong figure
furthest fastest. Four of the five rows above were wrong in the *source document* and would
have been wrong in the canonical state document within one merge.

---

*`mg-8d63`. Instrument: `code/lstar_landing_8d63/` — `run_all.sh`, ~11 s, exit 0 = all four
arms pass. It imports `code/lstar_789d/lib789d.py` and adds no mathematics of its own, so
that a disagreement would be about the sweep and not about the definitions.*
