# `code/alias_index_0d1b/` — THE ALIASED-SCALAR SWEEP (mg-0d1b)

```
sh run_all.sh        # ~55 s;  exit 0 = x0's seven planted worlds CAUGHT and x3's six arms pass
```

**The deliverable is [`INDEX.md`](INDEX.md), and it is generated, not written.** The rows
exist because two or more trees computed the same number; the names were read afterwards,
only to print them.

---

## THE HEADLINE

**The ticket says two names in two threads. The corpus has ELEVEN QUANTITIES ALIASED
ACROSS UP TO THIRTEEN NAMES, and every one of them AGREES.**

| quantity | names | trees | max spread over 306 primitive posets |
|---|---|---|---|
| `leak(A_1)` | **13** | 11 | `0.0` exact |
| primitivity (a PREDICATE, not a scalar) | **10** | 10 | 0 disagreements at 404 posets |
| `gamma` | **9** | 9 | `4.7e-10` |
| `Delta_P` | 7 | 7 | `0.0` exact |
| `Phi*_pref` | 7 | 7 | `0.0` exact |
| `mu_pref` | 7 | 7 | `9.1e-13` |
| **`rho*Delta_P` — the ticket's own scalar** | **6** | **6** | `7.3e-12` |
| `Phi*_all` | 6 | 5 | `0.0` exact |
| `E_footrule` | 4 | 4 | `0.0` exact |
| `M` | 4 | 4 | `0.0` exact |
| `rho` | 3 | 3 | `4.4e-15` |
| `1 - rho(A_1)` | 3 | 3 | `0.0` exact |
| `mu_pref` (upper bound) | 2 | 2 | `1.1e-07` |

**ZERO DISAGREEMENTS.** Not one aliased scalar in the value layer disagrees with itself
across trees. That is the answer to the ticket's question 2, and it is the *worse* answer
of the two available: the hazard here is not error, it is **silence**. Twelve independent
instruments have been computing the same twelve quantities and nothing has ever compared
them. Every row above is a control the arc already paid for and has never cashed.

**`ρ·Δ_P` IS SIX NAMES, NOT TWO.** `V10` (`mg-28ff` doc `:279`, recomputed independently
in `mg-29fe` and again in `mg-3bb9`), `rho*Delta` (`mg-789d`, `mg-c50b`), and `v_L`
(`mg-5cba`) are one column, agreeing to `7.3e-12` at every one of the 306 primitive posets
of `n ≤ 5`. And `l2_underclaim_audit_3bb9/out_a1_reversal.txt:53` prints
`first n at which each variant exceeds 1: {'V11': None, 'V10': 5, 'V01': 6, 'V00': 4}` —
a **third** instrument stating the `n = 5` onset, which nobody has ever cited.

---

## THE THREE FINDINGS THAT ARE NOT COUNTS

### 1. THE LARGEST ALIAS IN THE CORPUS IS NOT A SCALAR AT ALL

**Ten trees carry ten names for the primitivity predicate** — `is_primitive` (four trees),
`primitive` (three), `decomposable` negated (two), `not P.decomposable` (one) — and they
agree at all 404 posets (`x3` arm V4). A sweep looking for *computed number columns* would
never have found it, and it matters more than any scalar row: **it is the predicate that
defines the population every published `ρΔ` figure is stated over.** If two trees disagreed
about which posets are primitive, "6 of 275" and "6 of 275" would be different claims
wearing the same words.

### 2. `u_M` AND `c#` ARE TWO NUMBERS SHARING ONE PREDICATE, AND THE SHARING IS POPULATION-BOUND

`anticorrelation_c50b/out_s2_theory.txt:31` says `(M#) fails ⟺ u_M > 1`. `sweep_loss_51f4`
and `audit_5cba/a6` price the same route with `c#` and reason from `c# > 1` for the same
event. They are **not** the same number — 0 of 306 primitive posets have `u_M = c#` — and:

```
POP-ALL   comparable  357   numerically equal   6   THRESHOLD disagreements  45
POP-PRIM  comparable  306   numerically equal   0   THRESHOLD disagreements   0
```

On the primitive population the substitution is exactly safe. Off it, the two names
disagree about the very event they both claim to decide, at one poset in eight. **This is
the alias shape that would cost a fourth correction**, because the interchangeability is
real, is used, and is silently conditional on a population neither name carries.

`anticorrelation_c50b/s2_theory.py:87` already contains this control (`if (u_M > 1) != (cs
> 1): bad += 1`) and reports 0 — inside the loop that skips non-primitive posets. **The
control exists, is correct, and is invisible to every other tree**, which is this ticket's
thesis in one line.

### 3. ONE NAME COLLISION, RUNNING THE OPPOSITE WAY

`λ₂` in `chain_iv_c_81ff` **is** `gamma` — the value probe puts `lambda2_bracket` in the
nine-name gamma cluster without being told. `λ₂` in `hodge_leverage*` is the second
eigenvalue of a **link-graph Laplacian**, a different object. So the corpus has both
failure modes: one quantity under many names, and one name over several quantities. An
index that only listed synonyms would have missed the second.

---

## WHAT WAS SEARCHED (the ticket's step 4, answered on a result that is not clean)

| layer | population |
|---|---|
| name | **184** trees under `code/`, **967** `.py`, **897** transcripts, **285** `.md` under `code/`, **146** canonical documents in `docs/`, `STATE.md` |
| value | **404** posets — *every* naturally-labelled poset at `n = 3,4,5` — of which **306** primitive; **12** trees with adapters; **76** scalar columns compared |

**The 172 trees not in the value layer are classified by machine, not waved at** (`x1`):

* **112** compute no poset mathematics at all — meta trees about transcripts, pins, gates, provenance.
* **1** has no Python (`row3b_audit_eba7`).
* **59 DO the arc's mathematics and have no adapter here.** They are listed by name in
  `out_x1_population.txt`. Of those, **5** define an already-indexed *unambiguous* name and
  are the next ticket: `chain_iv_audit_00b3` (`lambda2_bracket`), `unified_gate_audit_446b`
  (`Delta`), `eps0_threshold_3969` and `eps0_audit_d3c7` (`delta1`), `unitmap_audit_9f91`
  (`E_inv`).

**`M` is defined in 34 trees and this index cannot tell which ones mean route (F)'s mean.**
Excluded from the residue ranking under a stated rule (a name defined in more than 8 trees
is not evidence), and named rather than dropped, because it is a finding about the name.

**THE BIGGEST THING NOT SWEPT is `δ(P)` itself** — nine name-forms in eight trees
(`delta_bruteforce`, `delta_lazy`, `delta_nosym`, `delta_dp`, `delta_1_dp`, `hand_delta_1`,
`delta_le`, `delta_of`, `delta_R`) with three different argument conventions. It is the
arc's own subject and it is a `DECLARED` row, not a `MEASURED` one.

---

## WHAT THIS SWEEP DOES NOT ESTABLISH

* **Nothing at `n > 5`.** Two scalars agreeing over 306 posets at `n ≤ 5` can differ at
  `n = 8`. No row of `INDEX.md` claims otherwise.
* **Nothing about families.** Every published `ρΔ` statement at `n ≥ 6` is about a family
  (chain(`n−1`)+point, near-ordinal antichains). This instrument has no family arm.
* **Nothing about `DECLARED` rows.** They were matched *by name* — the failure mode this
  ticket exists to fix. A `DECLARED` row is a lead.
* **The onset is not re-opened.** It is `n = 5`, certified in exact rationals by `mg-5cba`
  and independently reproduced by `mg-8d63`. The `ρΔ` column appears here only as a
  fingerprint for alias detection; no arm returns a verdict on it, and the maximum this
  instrument happens to observe (`1.027118`) is the published one.
* **Nothing is renamed.** `git diff --stat` against the merge base shows 0 files changed
  outside this directory.

---

## SHARES-CODE — which agreements are controls and which are re-runs (x3 V3)

An agreement is a free control only if the two trees computed it independently. All three
cross-tree edges among the probed set were read out of the source and resolved:

* `l2_underclaim_audit_3bb9 → l2_conditionality_28ff`: the import is in
  `a3_n7_population_label.py:21-22`, for **population labels**. `lib3bb9.py:5` states its
  own independence and the probed scalars are all `lib3bb9`'s. **Independent.**
* `eleak_repair_8311 → direct_prefix_audit_2de0`: `lib8311.py:3` — *"This file imports
  NOTHING from lib2de0 … That is deliberate"*. The mentions are specification.
  **Independent.**
* `lstar_landing_8d63 → lstar_789d` (outside the probed set, and the reason this column
  exists): `mg-8d63`'s own README says it imports `lib789d` and adds no mathematics. Its
  agreement with `mg-789d` is a **RE-RUN**; its agreement with `mg-29fe` is the independent
  one. **`mg-8d63` says this itself**, which is why it is the right precedent and not the
  counterexample.

So all 12 probed trees compute on their own code and every agreement above is real.

---

## SEVEN PLANTED WORLDS (x0) — 7 CAUGHT, 0 UNFALSIFIABLE, 0 MISSED

| world | plants | must say |
|---|---|---|
| W1 | a column `Δ + 1e-3` | must NOT join `Δ`'s cluster |
| W2 | a column equal to `Δ` | MUST join it — else W1 is silence, not refusal |
| W3 | two constant columns | DEGENERATE, not "an alias" |
| W4 | the real `ρΔ` columns on both populations | clusters on `POP-PRIM`, does **not** on `POP-ALL` |
| W5 | every real column nudged by `4e-10` | the spread clustering keeps what the rounding key splits |
| W6 | two all-`None` columns | must NOT cluster — else every absent scalar aliases every other |
| W7 | the 12 adapters | each still yields ≥ 3 live scalars |

W5's mutation is **derived from the captured columns**, not typed: the first real column
whose rounding key changes under a sub-tolerance nudge becomes the world
(`anticorrelation_c50b:Delta`). W4 is the arm that matters — it is the population claim
**exercised** rather than asserted.

---

## FIVE DEFECTS OF MY OWN, ALL KEPT

* **D1 — I BUILT AN ALIAS DETECTOR THAT ANSWERED BY ROUNDING.** The first clustering keyed
  each column by `round(v/1e-9)` and grouped equal keys. Two columns agreeing to `4.7e-10`
  can round to different buckets: it **split the 9-name `gamma` cluster and the 7-name
  `mu_pref` cluster**, and reported `chain_iv_c_81ff:lambda2_bracket` as a *different
  scalar* from `l2_audit_29fe:bracket_gap`. A detector for "same number under two names"
  that answers by rounding is a detector for "same number *and* same rounding". Repaired
  with single-linkage on max-absolute-difference; `fingerprint()` is **kept in the file**
  because `x3` arm V5 runs the old rule beside the new one and prints what it loses.

* **D2 — I MIS-STATED A POPULATION WHILE REPORTING THAT MIS-STATED POPULATIONS CAUSE WRONG
  FIGURES.** My first reading of `u_M` vs `c#` printed **27 threshold disagreements of
  144** as a finding. It ran over `POP-ALL` with `mu_upper` where
  `anticorrelation_c50b/s2_theory.py:70` uses `mu_exhaustive` over primitive posets only.
  On the subject's own population and quantity the answer is **0 of 306**, and the
  subject's own control at `s2_theory.py:87` was already there saying so. The finding that
  survived — that the equivalence is *conditional* — is worth more than the false alarm,
  but I got there by making the ticket's mistake first.

* **D3 — MY INDEX'S FIRST SITE COLUMN REPORTED `M` AT 1652 `.py` SITES.** A bare capital
  `M` matches every matrix variable in the arc. A site count that large is the regex
  telling you the token is ambiguous, and printing it beside `EDF` at 8 made the index's
  own numbers incomparable row to row. Repaired by scoping `MEASURED` site counts to the
  owning tree and adding an explicit *other trees defining this NAME* column — which turns
  the defect into the index's most useful field.

* **D4 — MY DEFINITION POINTER FIRST POINTED AT SELFTESTS.** The "where it is computed"
  column took the alphabetically first `.py` hit, which is usually `selftest*.py` — a line
  *asserting* the value, not defining it. A lookup table whose pointers land on assertions
  sends the next thread to the wrong file. Repaired by preferring `lib*`/`kern*`.

* **D5 — THE VALUE LAYER IS 12 TREES OF 184 AND I CHOSE THE 12.** Nothing mechanical
  selected them; I wrote adapters where the API was cheap. The 59-tree residue in `x1` is
  the honest statement of that, and the fact that it took a *hand-written adapter* to bring
  each tree into the comparison is the real reason nobody had done this before. **My index
  is still partly my own vocabulary (E4), and the 5 named residue trees are where it shows.**

---

## PREDICTIONS SCORED (`PREDICTIONS.md`, committed at `9c9dc2d`, before any code)

| # | bet | p | outcome |
|---|---|---|---|
| P1 | a ≥3-name, ≥3-tree alias group that is NOT `ρΔ`, `Δ_P` or `γ` | 0.75 | **HIT**, and by a wide margin — `leak(A_1)` at 13/11, `Φ*_pref` at 7/7, `μ_pref` at 7/7, `Φ*_all` at 6/5, `E_footrule` at 4/4, `M` at 4/4, `ρ` at 3/3, `1−ρ(A_1)` at 3/3 |
| P2 | the aliases AGREE; zero new numeric disagreements | 0.70 | **HIT** — 0 disagreements in 12 measured groups |
| P3 | no second unadjudicated numeric disagreement | 0.65 | **HIT** in the value layer; **not tested** in the `DECLARED` layer, and said so |
| P4 | `u_M` ≠ `c#` numerically but interchangeable in threshold statements | 0.60 | **HIT, WITH A RIDER THAT IS THE REAL FINDING** — interchangeable on `POP-PRIM` (0 of 306), NOT on `POP-ALL` (45 of 357). I bet on an unconditional equivalence and got a conditional one |
| P5 | fewer than 15 of 184 trees reachable | 0.70 | **HIT** — 12 |
| P6 | at least one group is a re-run, not an independent control | 0.90 | **MISS.** All three cross-tree edges resolved to independence; the one true re-run (`mg-8d63 → mg-789d`) is *outside* the probed set. I bet the sweep would catch a laundered control and it did not — the arc's trees are more independent than I gave them credit for |
| P7 | some quantity under ≥5 distinct symbol names | 0.80 | **HIT** — `leak` at 13, `γ` at 9 |
| P8 | a name-level false positive only the values can kill | 0.55 | **HIT** — `λ₂`, and it resolved the *opposite* way to my guess: `chain_iv`'s `λ₂` **is** `γ` (so the value probe **merged** what the name suggested was separate), while `hodge_leverage`'s is a different object |
| P9 | the value probe forms a group over a name my hand table does not list | 0.60 | **HIT** — `delta_1_prefix(1)` (`mg-2de0`) and `delta1(A_1)` (`mg-a94c3`) are in the `leak` cluster, and `prefix_min` (`mg-8311`) is in the `Φ*_pref` cluster. Not one of those three contains the string `leak` or `phi`. **This is the arm that makes the instrument more than my own vocabulary, and it fired.** |

**8 of 9 hit.** The miss is P6, and it is the one I was most confident in (0.90).

---

## THE ONE-LINE RULE THIS PRODUCES

> **Before you publish a figure, find its row in `INDEX.md` and read what the other trees
> in that row already say. If the row is `MEASURED`, they are computing your number right
> now on code that shares nothing with yours.**

*mg-0d1b. Nothing is renamed. 0 files outside this directory differ.*
