# `compression_rate_409a` — W4's instrument: **pin the rate**

Work item `mg-409a`. Subject: [`docs/imports/compression.tex`](../../docs/imports/compression.tex)
§5's `alpha_n`, which the note writes and never defines. Full write-up:
[`docs/OneThird-Compression-W4-Rate-mg-409a.md`](../../docs/OneThird-Compression-W4-Rate-mg-409a.md).

```
./run_all.sh          # r0 gates; r1..r6 only run if it passes
```

## The finding in two numbers

```
  THE BAR      alpha_n must EXCEED (n-1)/(gamma n),  gamma = delta(P) <= 1/3
               = 3(n-1)/n at the most generous gamma:  2 at n=3, rising to 3.
               IT IS A CONSTANT.  It does not decay with n.

  THE CEILING  alpha(P) <= 1 at EVERY poset with |L(P)| >= 2, and 1 is ATTAINED.
```

`1 < 2`. The shortfall is a property of the operator `2I - Pi_o - Pi_e`, not of anyone's
argument about it, so no theorem — including the two-projection theory W3 named — can close it.

## Arms

| file | what it establishes | exact? |
|---|---|---|
| `r0_selftest.py` | **gate.** Hand-known LE counts; both compressions cross-checked against `lib8bc7` (W2's independently written library); `M` is PSD, kills constants, and its form is the note's `:234`; `(*)` is an equality on linear statistics and an inequality in general (W2's repair); two controls shown to **go red** on planted defects | yes |
| `r1_ceiling.py` | `0 < alpha(P) <= 1` at 4 468 posets by **exhibited rational witness** (no eigensolver); positivity by union-find on the fiber graph; `alpha(Z_n) = 1` exactly at `n = 4..12` | yes |
| `r2_bar.py` | the bar. `R_M(f_xy) = ((n-1)/2) R_BK(f_xy)` at 25 431 instances; `step8.tex`'s Step 1 (`sum E <= 1/2`) re-derived at 4 449 posets; the bar-vs-ceiling table | yes |
| `r3_rate.py` | the uniform-in-poset reading: `R_M(f_w) = 6/(n(n+1))` on the antichain, **independent of `w`**, `n = 3..7` | yes |
| `r4_quantifier.py` | `alpha_full` vs `alpha_lin` — the quantifier W2's repair moves, and why §5's subspace is the wrong target | measurement |
| `r5_pairbias.py` | the note's own "purely in terms of a pair bias" ask. **Split:** the scalar `delta` is refuted; the full bias multiset is **not** refuted and determines `alpha` on every population tested | (a) exact, (b) measurement |
| `r6_twoprojection.py` | `alpha = 1 - cos theta_min` (Halmos), verified to `1e-14`; what the literature settles and what it cannot | measurement |

## Independence, stated rather than implied

`lib409a.py` builds everything on a verdict path from scratch — posets, linear extensions, both
compressions, the fibers, `Pi_o`/`Pi_e`, `M`, and the BK Dirichlet form. `lib8bc7` (W2) is
imported by **`r0` only**, as a second implementation to check mine against. **`r1`–`r6` share
one library, mine, and are therefore not independent witnesses of each other** — same shape as
W2's own D6, recorded because it applies here too.

## Float discipline

Every `PASS` in `r0`, `r1`, `r2`, `r3` and `r5.1` is an exact rational comparison or an
exhibited rational witness. `alpha_measured` (Jacobi) is a **float** and appears only in tables
and in `r4`/`r6`, which are measurement arms. No verdict rests on a float.

## Defects of my own, kept

- **D1** — my first control **could not fire**: dropping `C_e`'s trailing singleton for even
  `n` leaves `(*)` exact, because the last position of a linear extension is determined by the
  other `n-1` and the coarser group list induces the *same* partition. Replaced with two that
  do fire; the reason the first could not is now an arm (`r0.7`).
- **D2** — `r5.2`'s first key (`p_xy` over label-ordered pairs) is **not an isomorphism
  invariant** — an isomorphism can flip `p -> 1-p` — so it split isomorphism classes and
  reported 30 buckets at `n = 4` where there are 16 classes. Caught only because `30 > 16` on a
  class count I had not planned to run. Corrected; **the answer did not change**, which is the
  case in which such a defect normally goes unrecorded.
- **D3** — a prediction of mine that **lost**: I expected the pair-bias multiset to fail to
  determine `alpha` and built `r5.2` as a refutation search. 0 collisions on every population.
- **D4** — no `PREDICTIONS.md` was filed before the instrument existed, unlike several tickets
  in this repo. My reason: the load-bearing content is an inequality between two derived
  numbers rather than a search. That is a judgement, not a rule, and D3 is the one prior I had.
- **D5** — see *Independence* above.
- **D6** — see *Float discipline* above.
- **D7** — `n = 6, 7` rows are **samples** and small ones (150 / 120 / 60 / 60 / 25). Every
  table names its population. The ceiling and the bar are proved, not sampled.

## Not done here

`docs/imports/compression.tex` is not edited (its README reserves that directory for verbatim
copies). `STATE.md` is not touched. Theorem E is not re-proved — only its Step 1 is re-derived
and its statement is read. `lambda_std` is not computed anywhere in this directory.
