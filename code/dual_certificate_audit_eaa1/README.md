# `code/dual_certificate_audit_eaa1/` — independent audit of `mg-131e` (`mg-eaa1`)

Document: [`docs/OneThird-DualCertificate-Audit-mg-eaa1.md`](../../docs/OneThird-DualCertificate-Audit-mg-eaa1.md)
Predictions: [`PREDICTIONS.md`](PREDICTIONS.md), committed at `61f7f5b` **before any script here
existed** and before one byte of `code/dual_certificate_131e/` or `STATE.md` was read.
Outcomes: [`OUTCOMES.md`](OUTCOMES.md).

Audited: `mg-131e` (`b7b6941`), its document, and **`STATE.md` at
`491d42c79f7628c18cb7a5d197faa9f4600cd6c1`** (`mg-b488`).

## The one-line result

**All seven checks in the brief PASS.** Every count in `mg-131e` reproduces from code that
shares nothing with it; its `n = 6` refutation is rediscovered here independently — my solver's
optimum on my own probe is their published witness, atom for atom; and the `n`-indexed pattern
the brief told me to break **survives** its first out-of-sample prediction at `n = 6` and holds
to `n = 12`, because that pattern was never the claim that died.

## Files

| file | what it is |
|---|---|
| `lib_eaa1.py` | my combinatorics, my branch-program builder, my exact two-phase simplex, my **arithmetic** dual verifier, my primal substitution checker |
| `selftest_eaa1.py` | 8 control groups, 3 mutations, a hand-solved LP, cross-implementation check against `lp200d`. **Exits 1 on failure.** |
| `a1_program.py` | check 2 — is the certified program the DISJUNCTIVE one, or the INFEASIBLE literal one? |
| `a2_certificates.py` | check 1 — the `≤` direction re-certified from scratch on my own rows, every branch at `n = 3,4,5` |
| `a3_n6.py` | check 3 — extrapolate the `n`-indexed pattern to `n = 6..12`, then break the `≤` direction independently |
| `a4_verdict.py` | check 4 — the negatives, unboxed: the dual optimal face, and the mechanism claim whose caveat was dropped |

## Running

```
python3 selftest_eaa1.py          # controls; exit 1 on failure
python3 a1_program.py 3 4 5       # ~5s
python3 a2_certificates.py 3 4 5  # ~67s  (1024 branches at n=5)
python3 a3_n6.py 2                # ~2s   (the canonical, depth-2 probe)
python3 a3_n6.py 4                # the deep probe: |S| <= 4, 386 branches.  ~30s.
python3 a4_verdict.py 5           # ~35s
```

Committed transcripts: `out_selftest_eaa1.txt`, `out_a1_program.txt`,
`out_a2_certificates.txt`, `out_a3_n6.txt`, `out_a3_n6_deep.txt`, `out_a4_verdict.txt`.

## The one thing to read before using any number here

**Independence is the whole point of this directory, and it has exactly one deliberate
exception.** Every combinatorial primitive, the row builder, the simplex and the verifier are
written here from the definitions. `lib_eaa1.rows_agree_with_lp200d` is the single call into
`mg-200d`'s code, and it exists only to **assert** that my rows are its rows — which is audit
check 2, not a dependency. If that assertion had failed, everything I say about `mg-131e`'s
numbers would be about a different LP and would be worthless. It does not fail: the row sets are
identical as multisets **and in order**, at `n = 3,4,5,6`.

**Three kinds of object here, and they are not interchangeable.**

* **Dual certificates** are **upper** bounds, checked by `verify_dual` — sign conditions plus
  `Σᵢ yᵢ A_ij ≥ c_j` on every column, pure `Fraction` arithmetic, no simplex reachable from it.
  A certificate on a primal-**infeasible** branch is **vacuous**; `a2` splits every count by
  primal class so a vacuous one is never read as evidence.
* **Feasible measures** are **lower** bounds, checked by `check_measure` — mass, caps,
  no comparable pair flipped, per-slot symmetry. A lower bound above `(n−1)/3` **refutes** and
  can never confirm.
* **The simplex** proves nothing on its own. It is used only to *reproduce* values and to *find*
  candidate duals; everything it produces is then re-checked by one of the two arithmetic
  checkers, which cannot see it.

**`a3`'s `n ≥ 6` numbers are LOWER bounds on NAMED branches.** The probe is restricted to
branches whose incomparable set is `consecutive ∪ S` with `|S| ≤ 4` — a declared restriction, not
an exhaustive `n = 6` search, which the parent ticket forbids. Within that family of `386`
branches the maximum is exactly `11/6`, and `8` branches attain it — **every one of them
containing the chord `(1,4)`**, which corroborates `mg-131e`'s mechanism claim from the search
side. Outside it (a branch omitting a consecutive pair, or `|S| ≥ 5`) nothing is known here. So
the `n = 6` maximum is `≥ 11/6` and this directory does not say what it is.
