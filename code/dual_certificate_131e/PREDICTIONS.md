# `mg-131e` — predictions for the **DUAL CERTIFICATE** of `mg-200d`'s `≤` direction

**Committed before any script of this instrument exists.** Nothing below has been run. The hand
measurements in §0 were made with pencil and by reading `mg-200d`'s *committed transcripts*
(`code/perslot_symmetry_200d/out_v2_n34.txt`, `out_v2_n5.txt`) — they are disclosed here as
**measurements**, not laundered into predictions, because two of them (H3, H4) already decide
where the content of this ticket is and one of them (H2) already discharges most of the branches.

Parent: `mg-200d`, merged on `main` as `762921d`/`731a9ab`. Its formulation is **used, not
re-derived**, per the ticket. Its row builder `lp200d.build` is reused deliberately: a
certificate for a *different* row set would certify nothing.

---

## 0. Hand measurements, disclosed (made before any script existed)

**H1 — the object to be certified is a MAX OVER BRANCHES, so "a dual certificate" is a
*family*, one per branch, not one certificate.** `mg-200d`'s value is
`max over C ⊆ pairs of val(C)`, with `2^C(n,2)` branches: `8`, `64`, `1024` at `n = 3,4,5`. The
`≤` direction is the statement *`val(C) ≤ (n−1)/3` for every branch `C`*, so a certificate must
cover **every** branch, including the infeasible ones, not just the attaining one.

**H2 — the TRIVIAL DUAL is dual-feasible in every branch of every `n`, and its objective is
`|I|/3` where `I` = the incomparable pairs.** The branch LP is

> `max Σ_p μ_p inv(p)` s.t. `Σ μ = 1` (free multiplier `λ`), `q_ij ≤ 1/3` for `ij ∈ I`
> (multiplier `t_ij ≥ 0`), per-slot symmetry `=0` for `ij ∈ I` (free multipliers `s_{ij,k}`),
> over the columns `p` with `flips(p) ⊆ I`.

Weak duality needs, per column `p`: `λ + Σ_{ij ∈ flips(p)} t_ij + Σ_k σ_k(p) ≥ inv(p)`. Put
`λ = 0`, `t ≡ 1`, `s ≡ 0`. Every column has `flips(p) ⊆ I`, so the middle sum is exactly
`|flips(p)| = inv(p)` and the constraint holds with **equality on every column**. Objective
`λ + (1/3)Σ t = |I|/3`. This is a *proof*, not a computation, and it holds at every `n`.

**H3 — hence every branch with `|I| ≤ n−1` is already certified at every `n`, with no work, and
the entire content of the `≤` direction is the branches with `|I| ≥ n`.** Counts of those:
`1` at `n = 3`, `22` at `n = 4`, `638` at `n = 5` (`Σ_{r≥n} C(C(n,2), r)`).

**H4 — the trivial dual certifies the *attaining* branch at `n = 3` and `n = 4` and FAILS at
`n = 5`.** From `mg-200d`'s own transcripts: the attaining branch has `|I| = 2` at `n = 3`
(`C = {(0,2)}`), `|I| = 3` at `n = 4` (`C = {(0,2),(0,3),(1,3)}`), and `|I| = 6` at `n = 5`
(`C = {(0,2),(0,3),(1,4),(2,4)}`). `2/3 = 2/3` ✓, `3/3 = 1` ✓, `6/3 = 2 > 4/3` ✗. **So `n = 3`
and `n = 4` are almost content-free as certificates and the question this ticket exists to answer
lives at `n = 5`.** I regard the ticket's own "at `n = 3,4,5`" as three points of which two are
nearly free, and I am saying so in advance.

**H5 — a refinement of the trivial dual is available and, by hand, still fails at `n = 5`.** A
pair `ij ∈ I` carries no cap row at all when no column flips it (`lp200d.build` writes the row
only `if col:`), so `t_ij` does not exist and `|I|` may be replaced by the count of *active*
pairs. An inversion set containing `(x,y)`, `x<y`, must contain, for each `m` strictly between,
either `(x,m)` or `(m,y)`. At `n = 5`'s attaining branch `I = {(0,1),(0,4),(1,2),(1,3),(2,3),(3,4)}`
and `m = 2` gives `(0,2) ∉ I` and `(2,4) ∉ I`, so **`(0,4)` is inactive**: the refined objective is
`5/3`. Still `> 4/3`. **Genuine symmetry multipliers `s ≠ 0` are needed at `n = 5`.**

**H6 — `E[inv] = E[des]` on `mg-200d`'s `n = 5` attaining witness, and the slot identity is not
by itself enough.** Per-slot symmetry summed over incomparable pairs gives, at each slot `k`,
`A^C_k + 2 D_k = 1` (a comparable adjacent pair is always an ascent in a branch column), hence
`2 E[des] + E[compAsc] = n−1` and `E[des] ≤ (n−1)/2`. On the witness
`{id, (0,2,1,4,3), (1,0,3,2,4)}` at `1/3` each: `E[des] = E[inv] = 4/3` and `E[compAsc] = 4/3`,
so the identity is satisfied with room — `(n−1)/2 = 2 > 4/3`. Since `inv ≥ des` pointwise,
bounding `des` does **not** bound `inv`, so this identity alone is not the certificate.

**H7 — the attaining witness at `n = 5` puts `1/3` on each of the `n−1` CONSECUTIVE pairs
`(i,i+1)` and `0` on every other pair.** `id` flips nothing, `(0,2,1,4,3)` flips `{(1,2),(3,4)}`,
`(1,0,3,2,4)` flips `{(0,1),(2,3)}`. So `(n−1)/3` is `n−1` pairs at the cap, which is what
`mg-200d`'s `≥`-direction construction already does at `n = 3..20`.

---

## 1. Predictions

Scored `HELD` / `REFUTED` in `OUTCOMES.md`, kept as written either way.

| # | prediction | why I believe it |
|---|---|---|
| **P1** | Re-running `mg-200d`'s `v2_disjunctive.py` reproduces `2/3, 1, 4/3` at `n = 3,4,5`. | Control. If the parent does not reproduce in my worktree, nothing here is readable. |
| **P2** | The trivial dual of H2 verifies, by *direct arithmetic against `lp200d.build`'s own rows*, in **100%** of branches at `n = 3,4,5` — all `8 + 64 + 1024`. | It is a proof (H2), so the only thing being tested is whether I have the sign conventions of `build` right. A failure here is a bug in me, not in H2. |
| **P3** | Every branch is certified at `≤ (n−1)/3` by **some** dual, and the max over branches of the certified bound is **exactly** `(n−1)/3` at `n = 3,4,5`. | This is the `≤` direction; `mg-200d` computed the primal optimum, and LP strong duality guarantees a matching dual exists for each feasible branch. The only question is its *shape*. |
| **P4** | At `n = 3` **every** branch is discharged by the trivial dual alone (the single `|I| = 3` branch is the literal form, which `mg-200d` proved infeasible — but I predict the trivial dual bounds it at `1 > 2/3` and therefore does **not** discharge it, so `n = 3` needs the infeasibility or a real dual). | Two readings of the same branch; I am predicting the trivial dual is **insufficient** at `n = 3` too, on exactly one branch, and that the certificate there must use `s ≠ 0` or exhibit infeasibility. |
| **P5** | The number of branches at `n = 5` where the trivial dual's `|I|/3` exceeds `4/3` (i.e. `|I| ≥ 5`) is `638`, and the number where the *refined* (active-pairs) dual still exceeds `4/3` is **strictly smaller but still in the hundreds**. | H5 shows the refinement bites; it cannot plausibly kill 638 branches. |
| **P6** | Among branches needing `s ≠ 0`, the **majority are primal-INFEASIBLE**, so their certificate is vacuous (weak duality over an empty set) and carries no information about the conjecture. | `mg-200d` reports only `116/1024` feasible at `n = 5` and `13/64` at `n = 4`. So of the `638` hard branches most are empty. **This is the trap of this ticket**: a certificate family that is 80% vacuous can look uniform for a reason that has nothing to do with the bound. |
| **P7** | The number of branches that are simultaneously **feasible**, have `|I| ≥ n`, and have value `> 0` is **small** — I predict `≤ 20` at `n = 5` and `0` at `n = 4`. | `mg-200d` reports `max incomparable over value>0 branches` `= 2, 3, 6` at `n = 3,4,5` — so at `n = 4` no value-positive branch has `|I| ≥ 4`, and at `n = 5` the value-positive ones reach `|I| = 6`. |
| **P8** | **The verdict: the multipliers are NOT uniformly n-indexed in the strong sense.** I predict a *two-part* certificate: a genuinely `n`-indexed part (the trivial dual, H2, which is a proof at all `n` and discharges `|I| ≤ n−1`), and a residue on `|I| ≥ n` whose multipliers I will **not** be able to fit to a formula in `n` from three points — because the residue at `n = 3,4` is empty or vacuous and `n = 5` is therefore a **single** informative data point. | Three points, of which H4 says two are free. One informative point is not a pattern. I am pre-committing to this because it is the failure mode the ticket names, and because the honest answer to "is it n-indexed" may be **"the evidence available cannot say"**, which is neither of the ticket's two offered answers. |
| **P9** | I will nonetheless find a **structural** (not numeric) uniform statement covering more than the trivial dual — some closed-form family of multipliers, `n`-indexed, that discharges a described *class* of branches at all `n`. I predict it will **not** cover all branches with `|I| ≥ n`. | Partial structure is the likeliest outcome; total structure would prove LIB and total chaos is unlikely given the clean `(n−1)/3`. |
| **P10** | The certified bound `max_C dual(C)` will be **exactly** `(n−1)/3` and not merely `≤`, i.e. the certificates are **tight**, at all three `n`. | Strong duality on the attaining branch. |
| **P11** | `n = 6` is **not** attempted (`32768` branches × `720` columns × a dual LP each). What is not computed is declared. | Arithmetic, and the ticket forbids extending the brute force. |

## 2. My two most likely errors, filed in advance

**P12 — that I report a certificate family as "n-indexed" when the uniformity comes from
VACUITY.** Most hard branches are primal-infeasible (P6). A dual that "works" there works because
there is nothing to bound. If I do not separate *feasible-and-positive* branches from the rest
before pronouncing on the pattern, I will hand back a false green light on a route Daniel has
just raised the stakes on. Every pattern claim in the deliverable must be qualified by which
branch class it was measured on.

**P13 — that I let the sign conventions of `lp200d.build` silently invert.** `build` writes the
symmetry row as `bwd − fwd = 0` with `x < y`, and the cap rows as `≤ 1/3`. If I get a sign
backwards, the "verified" certificate certifies a different LP than `mg-200d` solved, and every
number in the deliverable is for the wrong problem. The control is P2: the trivial dual must
verify on **100%** of branches, because it is a theorem that it does.

## 3. Declared out of scope before starting

No `n = 6` exhaustive anything. No poset enumeration and no transitivity closure (`mg-200d`'s and
`mg-345e`'s refusal is kept). No re-derivation of `mg-200d`'s formulation, and no "fixing" of the
literal form's infeasibility. No `L4`, no `C₃`, no `ε_dem`, no `N₀` argument in either direction —
in particular this instrument does **not** discharge Daniel's route by citing `mg-c4f5 §5.3`,
which is about the qualitative hypothesis and not about an explicit rate. No claim of tightness
beyond `n = 3` (`mg-200d`'s standing caveat). The `.tex` sources are not opened.
