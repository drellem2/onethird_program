# ksbft_p1_walled_0b78 — instrument for KSBFT-P1 (mg-0b78)

Instrument for [`docs/KSBFT-P1-walled-routes-under-bounded-range.md`](../../docs/KSBFT-P1-walled-routes-under-bounded-range.md).
Computation here is an INSTRUMENT only (ticket rule): it computes witness ranges instead of guessing them,
and runs one counterexample probe. Nothing is a case extension.

```
sh run_all.sh     # ~15 s, one process, exact Fractions/integers, seeded RNG; asserts every control
```

| file | what | kind |
|---|---|---|
| `lib.py` | poset toolkit: closure, range `π(P)`, width (Dilworth via matching), exact `P[x before y]` and δ by DP over ideals | library |
| `ranges.py` → `out_ranges.txt` | range/width/δ of the named witness FAMILIES (`C_m ⊔ C_m`, `C_m ⊔ C_1`, `C_m ⊔ A_m`, antichain, `Z_m`, `(2+1)^{⊕m}`, `W*_2`) at several sizes. Controls: antichain range 8 width 9, `Z_9` range 2 width 2, δ(2+1) = 1/3 | exact |
| `ranges2.py` → `out_ranges2.txt` | range/width/δ of the FINITE witnesses read from the corpus (`(L*)` and `(F)&(M♯)` refuters from their `dn` bitmasks, the probe-D pair, the mg-131e LP poset, the fence, …) and of the staircase, star, `D_k`, `C_2⊕A_k⊕C_2`, `G(n,g)` families. `from_dn` asserts each bitmask list is a full down-set list | exact |
| `stanley_gap.py` → `out_stanley_gap.txt` | §5 probe: least strict k = 1 Stanley deficit `N_i²/(N_{i−1}N_{i+1}) − 1` per `(D, n)`. Positive control: `C_m ⊔ C_m`, `x = u₁`, `i = 2` reproduces mg-dcae's `1 + 1/(2m−1)` exactly. Negative control: planted floors must be CAUGHT. Consistency: interior equalities must be flat (Ma–Shenfeld k = 1), and Stanley's inequality itself is asserted at every index | exact, seeded random (not exhaustive) |
