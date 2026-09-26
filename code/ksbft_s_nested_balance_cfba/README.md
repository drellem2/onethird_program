# ksbft_s_nested_balance_cfba — instrument for KSBFT-S (mg-cfba)

Instrument for [`docs/KSBFT-S-nested-balance.md`](../../docs/KSBFT-S-nested-balance.md).
Computation here is an INSTRUMENT only (ticket rule): cross-checks, named families, sampling and
adversarial counterexample searches. No census is extended.

```
sh run_all.sh      # ~35 s, 1 process, exit 1 on any failed assertion
sh run_search.sh   # the adversarial searches of doc sec. 2.3, 3 processes, ~25 min
```

| file | what |
|---|---|
| `nb.c` | Exact pair laws over the ideal lattice with `__int128` counts. Prints `delta`, `deltaN` (nested pairs), `deltaP` (primal-nested only), the counts, and exact NB/PNB flags. `-v` prints every pair. |
| `fam.py` | Helpers. Reuses mg-ce69's `grow`/`dual`/`glue` (`Q_m`) and mg-7bfc's `fib`/`attach_*`/`hub`/`prime`. Also the structural and firing good-pair detectors. |
| `xcheck.py` | `nb.c` vs explicit linear-extension enumeration on 401 random posets (0 mismatches), with discrimination controls. |
| `witnesses.py` | Exact Fractions (mg-ce69 `lib.analyse`) for `T8`, `T13`, `T14` and `N12`, asserted, plus their ladder mechanism. CONTROL: open-window nested balance must FAIL on the ties. |
| `families.py`, `io.py` | NB on the named extremal families; which of them are interval orders (control: `2+2`). |
| `randprime.py` | NB on random prime indecomposable posets of range 8–14. |
| `records.py` | mg-2912's 2 534 records: NB, the price of nesting, (PNB), interval-order share. |
| `primal.py` | (PNB) on 11 456 random indecomposable posets with n ≤ 10. |
| `search.py`, `search2.py` | Beam searches minimising `deltaN` (or `deltaP`), optionally restricted to posets with no firing full-chain good pair. |
