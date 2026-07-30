# `code/species_audit_7dd3` — the instrument for mg-7dd3

Independent audit of **mg-a4ef / `106e121`**, the repair of mg-73df's `0 BROKEN, 1 MAJOR,
4 MINOR` on the species / Hopf-monoid document.

```
cd code/species_audit_7dd3 && ./run_all.sh     # ~3 min, pure Python 3, NO NETWORK
```

`git show` / `git diff` are used against **this** repository, which is local. Nothing else
leaves the machine and nothing outside this directory is written.

## What is here

| file | what it does | its own extent |
|---|---|---|
| `kern7dd3.py` | token-stream scanner and the exoneration rule, **sharing no code with any instrument it audits** | — |
| `statements7dd3.py` | the 12 statements: the document's own 11 `~~strikes~~` plus Y2 | — |
| `selftest7dd3.py` | 46 assertions, about half of them that the detector does **not** fire | — |
| `d1_source.py` | every correction mg-a4ef claims, read **at source**, through no checker | 7 corrections, 6 files + the document |
| `d2_extent.py` | the extent lines measured against what the code reads; the whole repository swept | 12 statements, 644 files |
| `d3_seam.py` | the duplicate sweep re-run from scratch, all 17 block quotes, no length floor | one document, block quotes and prose |
| `d4_survivals.py` | mg-73df's 15 survivals re-checked, and the whole diff | 15 + 5 + every changed line |
| `d5_mutations.py` | **34 mutations, each with its exit code predicted before the run** | 5 checkers, both directions |
| `d6_exitcodes.py` | the exit-code discipline across all 31 scripts in the arc | 6 trees, 2 run |

**Every one prints its own EXTENT under its total.** That is the property this audit exists
to check, applied to itself — and `d2` and `d3` both find that a printed extent can be a
false statement, so the discipline is necessary and is not sufficient.

## Reading the totals

`TOTAL BAD` counts **findings against the audited work**, following
`code/species_audit_73df`. `d2`, `d3`, `d5` and `d6` are **expected to be nonzero**: that is
what this audit found. The self-test is the only exit code that is a statement about this
instrument.

```
D1 TOTAL BAD: 0          every claimed correction is true at source
D2 TOTAL BAD: 4          the extent findings
D3 TOTAL BAD: 3          the seam sweep's own extent
D4 TOTAL BAD: 0          nothing retreated
D5 PREDICTIONS MISSED: 2 of 34
D6 TOTAL BAD: 1          a checker that reports a finding and exits 0
selftest7dd3: 46 assertion(s), 0 failure(s)
```

## Reproduction checked by hand, and its result

Not folded into `run_all.sh`, because re-running the audited trees overwrites their
committed outputs, and those are the record:

```
cd code/species_7d75          && ./run_all.sh    # T1-T6 all TOTAL BAD: 0
cd code/species_repair_6f61   && ./run_all.sh    # CHECK_DOC: PASS
cd code/species_remainder_f8fa && ./run_all.sh   # W3 SCOPE: PASS
cd code/species_repair_a4ef   && ./run_all.sh    # S1/S2 TOTAL BAD: 0
git status --short                               # clean
```

All four regenerate **byte for byte**. `code/species_audit_73df/c4_scope.py` and `c5_doc.py`,
re-run unmodified, reproduce `code/species_repair_a4ef/out_c4_scope_73df_after.txt` and
`out_c5_doc_73df_after.txt` **byte for byte**.

## The two defects this instrument found in itself and kept

Seven, in fact, all in `OUTCOMES.md`. The two that matter:

* **The first version of `d1_source.py` matched a wrapped sentence against raw bytes and
  failed on a sentence that is present** — which is the identical defect this audit had
  already predicted in `s2_seam.py`'s dead `quoted` variable, committed in the same session
  by the instrument that predicted it.
* **The first version of `d2_extent.py`'s lead-in test reported the CORRECTED line as the
  leak**, because `[0-9a-z]+` collapses `K̄(Π)` and `K(Π*)` to the same token `k` — throwing
  away the star and the Greek letter, which are the entire correction.
