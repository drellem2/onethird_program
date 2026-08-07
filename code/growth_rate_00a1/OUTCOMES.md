# `mg-00a1` — outcomes, scored against [`PREDICTIONS.md`](PREDICTIONS.md) as written

`PREDICTIONS.md` was committed at `f4d50a2`, **before any script in this directory existed**.
Nothing below has been edited into it after the fact. Predictions that were wrong are scored
`REFUTED` and kept verbatim.

## 0. The verdict, and how it differs from what I predicted

**The disjunctive per-slot value is `Θ(n²)`. The route is DEAD.** That is `P4`, and it held.

But it held **for a better reason than I predicted**. `P2`–`P4` were predictions about a
*table*: would the fourth point land on the three-point fit, and would the class survive? What
actually happened is that the fourth point *did* land (`P2`, at a self-assigned 50%), and then
the family turned out to have a **closed-form construction with a proof for every even `n`** —
so the answer no longer rests on any table at all. `s1` verifies the proof at `n = 4..24` by
direct arithmetic; the verification is a check on the proof, not the evidence for it.

That is also why `P13` — my pre-filed most-likely error, *"fitting `n(n+5)/36` on three points
and reporting the FORMULA as the answer"* — **did not fire**. It nearly did: `H6` already had
the formula written down. What stopped it was going back to find *why* the family worked
(the corner-symmetry bookkeeping of §4 of the document) instead of adding a fifth point.

## 1. Scores

| # | prediction (abbreviated) | verdict | what actually happened |
|---|---|---|---|
| **P1** | controls reproduce | **HELD** | `s2`: `mg-200d`'s attaining branches give `2/3, 1, 4/3` at `n = 3,4,5`; `mg-131e`'s consecutive branch gives `(n−1)/3` at all of `n = 3..10`, `8/8`. And `s3` PART A independently reproduces `mg-200d`'s **exhaustive `n = 5` maximum of `4/3` over all `1024` branches**, which I had not promised. |
| **P2** | `n = 12` value is exactly `17/3` | **HELD** (self-assigned 50%) | Exactly `17/3`. Float first, then exact rationals in `s2`. |
| **P3** | `n = 12` value `≥ 5.5` | **HELD** | `17/3 ≈ 5.667`, against `49/9 ≈ 5.444` for a linear continuation. This was the prediction designed to decide linear-vs-superlinear at the first untested point, and it decided it. |
| **P4** | **the answer is SUPERLINEAR, `Θ(n²)`; the route is DEAD** | **HELD** | And upgraded from "80% belief" to a theorem: `n(n+5)/36 ≤ val ≤ n(n−1)/6`, the lower end by explicit construction at every even `n`, the upper by `mg-131e`'s trivial dual. |
| **P5** | `mg-200d`'s `Θ(n²) → Θ(n)` headline is REFUTED; the gain is a constant `≈ 6` | **HELD** | `n²/6 → n²/36` is the bracket. The *exact* constant is not determined — only bracketed in `[1/36, 1/6]` — which is weaker than "about 6" reads; see §2. |
| **P6** | tc-reduction verifies, `0` exceptions, max attained closed | **HELD, and wider than promised** | `0` violations on **all 64** branches at `n = 4` and **all 1024** at `n = 5` (I promised a *sample* at `n = 5`), and the maximum is attained on a transitively closed branch at both. |
| **P7** | two-chain infeasible for `a+b ≤ 10` | **HELD** | Every `(a,b)` with `a+b ≤ 10` infeasible in exact rationals, phase-1 residual rising throughout. |
| **P8** | an explicit measure family verified by arithmetic, no LP, at `n = 6..16` | **HELD, and much wider** | Not a hard-coded list of measures but a **closed-form construction for every even `n`**, verified by arithmetic at `n = 4..24` (both parities). I gave this 60% because I did not yet know the pattern; the pattern turned out to be forced rather than fitted. |
| **P9** | greedy at `n = 12` re-selects the same family | **PARTLY HELD / NOT RUN AT 12** | The greedy re-selects exactly the staircase family at `n = 6, 8, 10` (`s4`), from scratch, in exact rationals. **`n = 12` was not run** — the hill-climb costs `O(n²)` exact LPs per step at `429`+ columns. So the prediction as stated (at `n = 12`) is **unscored**, and I am not claiming it. |
| **P10** | no linear upper bound exists; `c·n + O(1)` is not the answer returned | **HELD** | Direct consequence of `P4`, now a theorem rather than an inability to find one — which is exactly the distinction `P10` was filed to keep. |
| **P11** | `E[des] ≤ (n−1)/2` holds and `E[inv]/E[des] → ∞` | **HELD** | `s1` PART E: `E[des] = n/4` exactly on the witness, always under `(n−1)/2`; the ratio is `(n+5)/9`, growing without bound. So `mg-131e`'s H6 identity is not merely insufficient — it is off by an unbounded factor. |
| **P12** | the `n = 14` value is computable and `≥ 7.0` | **HELD for the WITNESS, NOT for the BRANCH** | The witness value at `n = 14` is `133/18 ≈ 7.389`, by arithmetic, no LP. The **exact LP on the branch** at `n = 14` (`1430` columns) was attempted and **did not finish**; it is not reported and not interpolated. `s2` therefore stops at `n = 12`. |

**Errors filed in advance:**

| # | filed error | fired? |
|---|---|---|
| **P13** | fitting a quadratic on three points and reporting the FORMULA as the answer | **DID NOT FIRE.** See §0. The formula in `H6` is the same formula the proof derives, but it is now derived, not fitted, and the document says so at the site. |
| **P14** | reading "the relaxation is quadratic" as "the frozen-poset conjecture is refuted" | **DID NOT FIRE**, and the guard is on the page: document §5.2 lists five things that must not be read as killed, and `README.md` and `lib00a1.py`'s module docstring both carry it. |
| **P15** | treating a named-branch value as the maximum | **DID NOT FIRE**, and is stated at every site (`s1` header, `README`, document §6) together with *why* the asymmetry is harmless in this direction and would be fatal in the other. |

## 2. Things I got wrong or left weaker than they sound

* **`P5`'s "a constant factor of about 6" is looser than it reads.** What is proved is
  `n(n+5)/36 ≤ max over branches ≤ n(n−1)/6`. The true constant is somewhere in `[1/36, 1/6]`
  and **is not determined here**. "Per-slot symmetry buys at most a factor 6" is right; "buys a
  factor 6" would not be.
* **`P9` is unscored at the `n` it names.** The greedy was run at `n = 6, 8, 10` and not at
  `n = 12`. I am recording that as unscored rather than quietly rescoring it against the `n` I
  did run.
* **`P12` split.** The witness value at `n = 14` is a theorem; the *branch* value at `n = 14`
  is not computed. Those are different objects and the row above keeps them apart.
* **`H8` in the predictions is the reason to trust anything here.** My float simplex was wrong
  on first writing and reported `13/9` where the exact solver reports `4/3`. It was caught only
  because I cross-checked against `lp200d.relaxation` on 364 branches. The verdict was
  subsequently moved off the simplex entirely — `s1` uses none — but the near miss is why.
* **The `1/6` limit of `ε_spec` is a numeral coincidence with `STATE.md` row 8's "pair bias
  gives `1/6`", and I am NOT claiming they are the same object.** The document flags this
  explicitly as the site where a third currency conflation would go (`mg-76b2` filed the same
  class of error in advance as its `P14`).

## 3. Not done

Listed in full in document §7. The load-bearing ones: no exhaustive `n = 6` (forbidden, and not
needed); **no proof that this family is the maximum** — only that it is a lower bound at every
`n`, optimal on its own branch at `n = 6,8,10,12`, and locally maximal under adding any single
further pair at `n = 6,8,10`; no upper bound sharper than the trivial dual, so the constant is
bracketed and not determined; and **no edit to any other document**. On which: I very nearly
shipped the sentence *"`STATE.md` carries `mg-200d`'s headline and needs a correction"*. It
does not — `STATE.md` does not mention `mg-200d`, `mg-131e`, `per-slot` or `2/(n+1)` anywhere.
The three documents that do are `OneThird-PerSlot-AdjacencySymmetry-mg-200d.md`,
`OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md`, and `OneThird-DualCertificate-mg-131e.md`
(`:171`). Each is another landing's document; the corrections are named in the mail to
`pm-onethird` rather than performed here.
