# `code/branching_locate_db09` — the instrument for mg-db09

Supports `docs/OneThird-Bratteli-Path-Algebras-Where-This-Lives.md`.

```
./run_all.sh          # ~6 min, pure Python 3, no dependencies, NO NETWORK
./fetch_sources.sh    # the ONE network script; run_all.sh does not call it
```

Committed outputs: `out_selftest.txt` (699 520 assertions), `out_t1_tl.txt`,
`out_t2_gz.txt`, `out_t3_ours.txt`, `out_t4_quotes.txt`. Every `t*` script ends
with a `TOTAL BAD` line and all four are `0`.

## What each file decides

| file | what it decides |
|---|---|
| `kerndb09.py` | exact linear algebra over `Q`; "monomial algebras" (a basis in which a product of basis elements is a scalar times a basis element — Temperley–Lieb, group algebras and band algebras are all of this shape); the radical by the trace form **with an independent nilpotency check**; Temperley–Lieb diagrams, cell modules, Gram forms and Hom-spaces; symmetric group algebras, centres and Gelfand–Tsetlin subalgebras; posets, `F(P)`, `AC(P)`. **Added by mg-e8b8:** the action of a whole diagram on a cell module, the irreducibles `L(n,p)` with their characters, the embedding `TL_{n-1} ⊂ TL_n`, and an exact solver that reports non-uniqueness rather than swallowing it |
| `t1_tl.py` | **the Temperley–Lieb tower at four parameters, and a WITHDRAWN separating example.** It was delivered as the multiplicity-free non-semisimple object; it is not one. `T1b2` (added by mg-e8b8 on mg-2060's finding) measures the branching graph as Vershik–Okounkov define it — vertices the **irreducibles** `L(n,p) = V_{n,p}/rad⟨,⟩`, edges the restriction multiplicities — **at every parameter**: the vertex set differs at `β = 0` (1,1,2,2,3,3 against 1,2,2,3,3,4) and multiplicities reach 2 at `β = 1` and `β = 0`. Multiplicity-freeness moves in exact step with semisimplicity, so the tower separates nothing and `T1d` withdraws the claim. What stands: the path-pair count is 132 at `n = 6` at every parameter, the algebra is a sum of endomorphism algebras at two of them and not at the other two (132/132/99/42), and six published controls reproduce |
| `t2_gz.py` | **the semisimple NON-multiplicity-free object, built.** Okounkov–Vershik's Remark 1.3 and Prop. 1.4 tested as equalities on symmetric-group towers with a level removed, and on `C ⊂ M_2(C)`. The conclusion survives; the canonical basis does not |
| `t3_ours.py` | `kF(P)` against both hypotheses: `\|F(P)\|` vs `\|AC(P)\|`, `dim kF(P)/rad = \|AC(P)\|` through the trace form, the Cartan matrix by Margolis–Saliola–Steinberg's route, and the census of posets for which `kF(P)` is semisimple |
| `t4_quotes.py` | 19 quotations checked verbatim against the committed `pdftotext` windows, with 5 near-miss negative controls that must all be rejected |

## Independence

Written fresh for this ticket. It imports nothing from `code/species_7d75`,
`code/branching_af28`, `code/branching_audit_6ad0` or `code/branching_repair_41aa`.
Where it recomputes an object those directories also build — `F(P)`, `AC(P)`,
`dim kF(P)/rad` — it builds it from the geometric definition and cross-checks
two routes against each other inside `selftestdb09.py`.

## Two disjoint routes, deliberately

* **The radical** is computed as the radical of the trace form (Dickson,
  characteristic 0) and then **verified** to be a two-sided nilpotent ideal.
  The verification does not use the theorem.
* **The semisimple quotient of `TL_n(β)`** is computed a second time as
  `Σ_p (rank of the Gram matrix of V_{n,p})²`. The trace form never sees a cell
  module and the Gram matrices never see the regular representation. **0
  disagreements** on 20 `(n, β)` pairs.
* **`AC(P)`** is computed both as the supports of `F(P)` and as the set
  partitions with acyclic quotient. **0 disagreements**, all classes to `n ≤ 4`.
* **The Cartan matrix** carries its own arithmetic check: for a split basic
  algebra the entries must sum to `dim A`. They do, on every row.
* **The irreducibles of `TL_n(β)`** (mg-e8b8) are tied back to the two routes
  above rather than offered as a third: `Σ_p (dim L(n,p))² = dim A/rad` is
  asserted in the self-test for all 20 `(n, β)` pairs — the trace-form route
  against the Gram route with the new machinery in between. What is genuinely
  new is the whole-diagram action and the character solve; the check on the
  first is that it is asserted **equal** to the generator action `T1b` already
  used, on every `(n, p, β)` they share. The
  branching multiplicities are read from a solve whose **uniqueness,
  integrality, non-negativity** and `Σ_q m_q · dim L(n-1,q) = dim L(n,p)` are
  all checked in `t1_tl.py` rather than assumed.

## Size caps, each stated in the output it belongs to

* `t1` runs to `n = 6` (`dim TL_6 = 132`).
* `t2` runs to `n = 5` (`dim CS_5 = 120`).
* `t3b` caps `|F(P)| ≤ 90` for the trace-form radical: **67 classes tested, 20
  exempt** at `n = 5`, each with its size printed. `t3a`, `t3c` and `t3d` have
  no cap and reach the `n = 5` antichain (`|F| = 541`) and `n = 6` counts.

## Conventions that have bitten this repo before

* `AC(P)` is the **support semilattice of `F(P)`** — the set partitions whose
  quotient digraph is acyclic. It is **not** the smaller set of flats meeting
  the open cone; conflating the two is the error mg-1953 repaired.
* `F(P)` is multiplied by the **Tits product** (refine the first by the
  second), not by concatenation.
* The Temperley–Lieb parameter is `β = q + q⁻¹`. `β = 2` and `β = 0` are
  **not** generic and are included because the published semisimplicity facts
  about them are sharp controls: `TL_n(2)` is semisimple for every `n`, and
  `TL_n(0)` is semisimple exactly for `n` odd.
