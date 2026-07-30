# `code/species_7d75` — the instrument for mg-7d75

Supports `docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md`.

```
./run_all.sh        # ~46 s, pure Python 3, no dependencies, NO NETWORK
```

Committed outputs: `out_selftest.txt` (759 assertions), `out_t1_grading.txt`,
`out_t2_operation.txt`, `out_t3_bidigare.txt`, `out_t4_one_operation.txt`,
`out_t5_hopf_monoid.txt`, `out_t6_fock_and_record.txt`.

Every `t*` script ends with a `TOTAL BAD` line. All six are `0`.

**REPAIRED 2026-07-30 (mg-6f61), on mg-a61f's X1.** `t1_grading.py`'s T1e used
to **assert** *"the smallest poset with `AC(P) != Pi[n]` is `{a<c, b<d}`"*. That
is **false** — the smallest is the **3-element chain** — and the table T1e prints
eleven lines above it already said so (`19 - 13 = 6` witnesses at `n = 3`). The
claim is now **computed** from the same sweep, and T1e **fails** if it is not the
3-chain with 6 labellings. See `code/species_repair_6f61/` and
`docs/OneThird-Species-Hopf-Monoids-Repair.md`.

**Also repaired in the document, not here:** `t5_hopf_monoid.py`'s five-column
table is correct, but **only two of its columns can fail on a sub-collection** —
associativity, coassociativity and compatibility are identities of the ambient
Hadamard product and are pinned at 0 for every collection. `t5_hopf_monoid.py`
itself already says the right thing (*"what T5 establishes is CLOSURE"*); it was
§0 of the document that disagreed with it. The per-column demonstration is
`code/species_repair_6f61/r2_columns.py`.

**REPAIRED AGAIN 2026-07-30 (mg-f8fa) — three of mg-a61f's findings were fixed
in the document by mg-6f61 and left standing HERE, which is the copy a
successor re-runs.** `t3_bidigare.py` still headed T3d *"three are controls"*
(X4) — the count is now **computed** by a new **T3e**, which shows convention B
is identically the opposite algebra of convention A and **fails if it is not**,
with its own control that must fire and does (0 mismatches at every `n ≤ 5`;
control 2 / 26 / 170 at `n = 3, 4, 5`). Control (ii)'s counts were unread (X5) —
see the conventions section below. And **ledger S4 was unmarked at source**:
`t4_one_operation.py` and `t6_fock_and_record.py` printed the identification of
`k^{Π_n/S_n}` with the **character ring of `S_n`** inside a run reporting
`TOTAL BAD: 0`, with nothing telling a reader that **that step is CITED and not
verified** — to Solomon (1976) and Garsia–Reutenauer/Atkinson, **neither read
here or by mg-a61f**. Both now carry the scope in place. The detector for all
three is `code/species_remainder_f8fa/w3_scope.py`, which reported **12
problems** against this directory before the repair (`out_w3_scope_before.txt`)
and 0 after.

**What is NOT withdrawn by any of that:** Bidigare's theorem still reproduces
entry for entry, the band product is still invisible to the Hopf structure, and
the poset half of the headline is still confirmed independently at 87/87 with
no size cap. Only the control **count**, the control's **reading**, and the
**scope marking** were wrong.

## What each file does

| file | what it decides |
|---|---|
| `kern7d75.py` | posets, set partitions, set compositions, the Tits product, `F(P)`, `AC(P)` by two routes, orbits, exact linear algebra |
| `hopf7d75.py` | the Hopf-monoid layer: Aguiar–Mahajan's poset / set-composition / set-partition (co)products on an arbitrary finite ground set, and the two candidate subspecies |
| `t1_grading.py` | **the grading falsifier, run first.** `|Π[n]| = Bell(n)`; `Π[n]/S_n` = integer partitions, `p(n)` of them; `p(n)` = #conjugacy classes of `S_n`; `AC(antichain) = Π[n]` **as sets** |
| `t2_operation.py` | `Φ : kF(P) → k^{AC(P)}` is a surjective algebra map with nilpotent kernel, so `kF(P)/rad = k^{AC(P)}` — a fresh re-anchor of mg-af28 B5 / mg-6ad0 A4a, with no trace form and no citation |
| `t3_bidigare.py` | **Bidigare's theorem built from both definitions and compared structure constant by structure constant.** Four candidate identifications are run; two hold, two fail — **and the four are two statements each computed twice, so this is ONE control run twice** (mg-a61f X4; see the repair document) |
| `t4_one_operation.py` | `(kF(P))^{Aut(P)}/rad = k^{AC(P)/Aut(P)}` on every poset class to `n ≤ 5`, and both of Daniel's instances read off that one table. **The `n ≤ 5` and `dim ≤ 90` caps bound this instrument and not the identity — it is a three-line corollary of AM §10.10 plus the Reynolds operator (mg-a61f, and §0 of the document).** **The last step of the `S_n` row — `k^{Π_n/S_n}` *is* the character ring — is ledger S4 and is CITED, not verified; marked in place (mg-f8fa)** |
| `t5_hopf_monoid.py` | the bimonoid axioms of Aguiar–Mahajan, checked exhaustively on the ground set `[4]` for both candidate subspecies, with four controls |
| `t6_fock_and_record.py` | the two Fock functors; the Bell(n)/p(n) resolution; the correction to mg-af28's Bergeron–Li negative; the failed candidate map to `Sym`. **What is measured is the two counts to `n = 7`; that they are `K̄` and `K` of one species is ledger S5, quoted and not re-derived — neither functor is evaluated from its definition here. Marked in place (mg-f8fa)** |

## Independence

Written fresh for this ticket. It shares no code with `core_af28.py`,
`kern6ad0.py` or `core1953.py`. Where it recomputes an object those files also
build, it builds it from the geometric definition and cross-checks two routes
against each other inside `selftest.py`.

## Conventions that have bitten this repo before

* `AC(P)` here is the **support semilattice of `F(P)`** = the set partitions of
  `[n]` whose quotient digraph is **acyclic**. It is **not** the set of flats
  meeting the **open** cone; that smaller set additionally requires every block
  to be an antichain, and conflating the two is the error mg-1953 repaired
  (R1). Nothing in this directory uses the smaller set.
* Faces multiply by the **Tits product** (refine the first by the second). The
  Hopf monoid of set compositions multiplies by **concatenation**. These are
  different maps, and `t5` control (ii) fires on them: 1 442 closure failures,
  252 associativity failures, 11 020 compatibility failures.
  **REPAIRED 2026-07-30 (mg-f8fa), on mg-a61f's X5 — those counts do not
  measure "how differently" the two products behave, and that reading was the
  defect.** The control fires on a **type mismatch**: `μ_{S,T}` takes its two
  factors on **disjoint** ground sets, the Tits product intersects blocks, and
  across disjoint non-empty sets every intersection is empty — so the 1 442
  product-closure failures **are exactly** the 1 442 of 11 301 pairs whose two
  ground sets are both non-empty, checked as a **set equality** and not as a
  coincidence of counts (`t5` control (ii), and `code/species_remainder_f8fa/
  w2_typemismatch.py` from disjoint code, where a type-**correct** corruption
  fails the same column 0 times). **The conclusion is unaffected and is NOT
  withdrawn: the band product is invisible to the Hopf structure** — and that
  rests on the types, so it holds at every ground set rather than on `[4]`.

## Size exemptions, each listed in the output it belongs to

* `t2` caps `|F(P)| ≤ 80`; 24 of 63 classes at `n = 5` are skipped.
* `t4` caps `dim (kF(P))^{Aut(P)} ≤ 90` for the nilpotency step only; 4 of 63
  classes at `n = 5` are skipped there and tested for everything else.
* `t3` runs to `n ≤ 5`. `n = 6` needs `4683² ≈ 21.9 M` face products and was not
  run.
* `t5` is exhaustive on the ground set `[4]` (4 399 basis elements of `F`,
  2 685 of `AC`) and not beyond.
