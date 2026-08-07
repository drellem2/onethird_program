# `code/dual_certificate_131e/` — dual certificates for `mg-200d`'s `≤` direction (`mg-131e`)

Document: [`docs/OneThird-DualCertificate-mg-131e.md`](../../docs/OneThird-DualCertificate-mg-131e.md)
Predictions: [`PREDICTIONS.md`](PREDICTIONS.md), committed at `7dc374c` **before any script
here existed**. Outcomes: [`OUTCOMES.md`](OUTCOMES.md).

Parent: `mg-200d` (`762921d`, `731a9ab`, on `main`). Its formulation and its row builder
`lp200d.build` are **used, not re-derived** — a certificate for a re-derived row set would
certify a different LP than the one whose value is in question.

## The one-line result

**`mg-200d`'s `≤` direction is certified at `n = 3, 4, 5` and is FALSE at `n = 6`.** The three
exact points were a small-n coincidence, so the route does not become a proof of `(LIB)` at
large `n` and should not be pursued as one.

## Files

| file | what it is |
|---|---|
| `lib131e.py` | the arithmetic dual **verifier** (no simplex), the dual solver, the named certificate tiers, branch bookkeeping |
| `selftest131e.py` | 9 control groups, 5 of them **mutations**. **Exits 1 on any failure.** |
| `d1_certificates.py` | the certificates: every branch at `n = 3,4,5`, verified, plus strong duality against `mg-200d`'s primal on every feasible branch |
| `d2_pattern.py` | the ticket's actual question — the `n`-indexed piece (a theorem), the residue, and the dual **optimal-face** ranges that exclude the natural guess |
| `d3_refutation.py` | the verdict: hard-coded feasible witnesses beating `(n−1)/3` at `n = 6..10`, re-checked by direct arithmetic |

## Running

```
python3 selftest131e.py            # controls; exit 1 on failure
python3 d3_refutation.py           # the verdict.  Seconds.  Uses NO LP at all.
python3 d1_certificates.py 3 4 5   # the certificates (n = 5 is ~5.5 min: 1024 branches)
python3 d2_pattern.py 3 4 5        # the pattern analysis
```

Committed transcripts: `out_selftest131e.txt`, `out_d1_certificates.txt`,
`out_d2_pattern.txt`, `out_d3_refutation.txt`.

## The one thing to read before using any number here

There are **two** kinds of object in this directory and they are not interchangeable.

* **Dual certificates** (`d1`, `d2`) are **upper** bounds. Each is a vector `y` checked by
  `verify_dual` against `lp200d.build`'s own rows — sign conditions plus
  `Σᵢ yᵢ A_ij ≥ c_j` on every column — by direct `Fraction` arithmetic with no simplex
  anywhere in the path. They prove `val(C) ≤ y·b`.
  **A dual certificate on a primal-INFEASIBLE branch is VACUOUS**: it bounds a maximum over
  the empty set. At `n = 5`, `386` of the `388` branches that need a non-trivial certificate
  are infeasible, and counting those as evidence of a pattern was pre-filed as the error
  `P12`. `d1` and `d2` split them out at every line.

* **Feasible measures** (`d3`) are **lower** bounds. Each is a hard-coded measure re-checked
  for mass `1`, flip caps `≤ 1/3`, per-slot symmetry on every incomparable pair, and no
  comparable pair ever flipped. A lower bound above `(n−1)/3` **refutes** the conjecture and
  can never confirm it — `mg-200d`'s own asymmetry, kept.

`d3`'s numbers are **not** upper bounds at `n ≥ 6`: each is found on one **named** branch, so
the true `n = 6` maximum may be larger still. The exhaustive `n = 6` value is not computed and
is not claimed.
