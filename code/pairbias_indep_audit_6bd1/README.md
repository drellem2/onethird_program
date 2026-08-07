# `pairbias_indep_audit_6bd1` — mg-6bd1's instrument

INDEPENDENT AUDIT of `mg-345e` (`550a7f1`), which answered **(A) INDEPENDENT** to
"is the pair-bias derivation of `ε_spec` independent of L4's modulus question?".

Deliverable: [`docs/OneThird-PairBias-Independence-mg-6bd1-IndependentAudit.md`](../../docs/OneThird-PairBias-Independence-mg-6bd1-IndependentAudit.md).
Predictions: [`PREDICTIONS.md`](PREDICTIONS.md), committed at `3cbc554` **before any
script here existed and before one line of mg-345e's derivation was read**.

## Independence of the parent's code

Nothing here imports `lib345e` or reads `code/pairbias_independence_345e/out_*.txt`.
The ledger reader is a two-pass split-on-pipes/token-walk reader, deliberately not a
regex over the label cell, so that mg-345e's own Defect-1 failure mode (an under-reading
quantifier) could not be inherited along with its result. Every figure is re-derived from
`Op-Form` and `mg-c3ca`'s definitions, in exact rationals, with no float on any path that
decides anything.

## Run

    ./run_all.sh          # selftest first, then b1..b5

| file | what it does |
|---|---|
| `lib6bd1.py` | ledger reader, graph closure, and the exact-rational algebra |
| `selftest6bd1.py` | 19 constructions with hand-computable answers, incl. two blind-scan guards |
| `b1_ledger.py` | Op-Form §9 re-parsed; rows, edges, closure, 4 negative controls |
| `b2_algebra.py` | every printed figure re-derived; the currency/unit map; 3 negative controls |
| `b3_census_scope.py` | the `1/6` census at mg-345e's own commit; the scope-conflation reading |
| `b4_branches_and_arch.py` | L4's three branches vs the Step-6 contradiction; the arch graph's information content |
| `b5_depth2_walk.py` | **the one-level-down dependency walk** — the check this ticket exists to run |

## Four defects of this instrument, kept in the source

Numbered as in the deliverable's §D. Two of them are the same shape and both **flatter
the party under audit**, which is why they are on the page rather than quietly fixed.

- **D1** — the ledger reader demanded exactly four `|`-separated cells. Op-Form's claim 1
  contains `$|A|\le n/2$` — literal pipes inside math — so the row was dropped: 35 rows
  and 10 edges against mg-345e's 36 and 11. **mg-345e's numbers were right and mine were
  wrong.** Found by disagreeing with the parent, not by my own control. Guarded now by
  selftest S2.
- **D2** — negative control NC6 (`eps_spec == 2/3` must never hold) scores itself FAILED
  against correct code, because `n/(n+1) = 2/3` at `n = 2` exactly. A genuine small-`n`
  coincidence, disclosed rather than tuned away.
- **D3** — `b3`'s `git ls-tree -r` ran without `--full-tree` from this subdirectory, so
  `docs/` matched nothing and the `1/6` census returned **exactly 2 — mg-345e's own
  number**. A broken instrument that agrees with the audited party. Guarded by S6.
- **D4** — `b5`'s screen passed bare relative paths to `grep` from this subdirectory,
  found no files, and printed *"L4-indicator tokens: NONE"* for every input: it confirmed
  the verdict under audit by failing to open the evidence. Guarded by S3, which requires
  a missing evidence path to **raise** rather than return clean.
