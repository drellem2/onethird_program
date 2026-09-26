# ksbft_f_b447 — exact checks for KSBFT-F (mg-b447)

Instrument for [`docs/KSBFT-F-L4-step6-under-bounded-range.md`](../../docs/KSBFT-F-L4-step6-under-bounded-range.md).

```
python3 check.py 6 > out_check.txt     # ~6 s, exact Fractions, no clock, no randomness
```

Two consecutive runs are byte-identical (checked with `cmp`). The argument is `NMAX`, the largest
poset size in the exhaustive sections.

| section | what it checks | kind |
|---|---|---|
| `c(D)` | Lemma 2.3's constant `c(D) = 1/(1+f(D))` against `2^(1−2D)` for `D ≤ 20`, and printed beside KSBFT's `q₂` | arithmetic |
| `W` | the range of every witness the ticket names: `W*` (and `W*_t`), `W`, `2+2`, the `n = 4` N-poset, mg-f5be's `n = 8` fence (identified with the Fibonacci poset `Z_8`), `Z_4..Z_12`, the `C_a ⊕ C_a` family. Also the `W*` rationals of mg-3af9 §4 | exact enumeration |
| `X` | over **every naturally labelled poset** on `n ≤ NMAX` elements (so every pair `(P, e)` up to isomorphism), every prefix cut of `e = identity`: X1 `τ ≤ 2π(P)−1` (Prop 2.2), X2 `max_σ K ≤ τ` (mg-3af9 Thm A), X3 `max_σ K ≤ π(P)` (Lemma 2.1), X4 `P[b before a] ≥ c(π(P))` for every incomparable pair (Lemma 2.3), X5 the `(EQ)` identity of §7 | exhaustive, `n ≤ 6` |
| `T` | one-point transport on `W*(4,4,2)`: for each deleted `v`, which balanced pairs of `P−v` stay balanced in `P` | exact |
| `S` | one-point persistence: every non-chain on `3 ≤ n ≤ NMAX` has a pair balanced in `P` and in some `P−v` | exhaustive, `n ≤ 6` |
| `C` | firing controls: X1–X4 re-run with a bound known to be FALSE; each must print `FIRES` | control |

`τ` is computed by brute-force vertex cover of the cross-incomparability bipartite graph, which is
exactly the minimum branch-(ii) certificate under the modification reading (§2 of the doc).
