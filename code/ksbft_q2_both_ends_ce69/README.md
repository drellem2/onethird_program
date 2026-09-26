# ksbft_q2_both_ends_ce69 — both-ends / second-order ladder probe (mg-ce69)

Instrument for [`docs/KSBFT-Q2-both-ends.md`](../../docs/KSBFT-Q2-both-ends.md). Pure Python, exact integers
and Fractions. Census files come from mg-eedd's generator (`../ksbft_one_pt/onept.c`, compiled through
`../ksbft_m_margin_6b81/pcert.c`, mode `onept gen`); its control is OEIS A000112, reproduced in `out_gen.txt`.
Computation is used only to probe candidate lemmas; no case search was extended.

```
sh run_all.sh     # ~6 min wall, 3 processes (POGO_WORKER_CORES); temp census dir is deleted; exit 1 on a failed check
```

| file | role |
|---|---|
| `lib.py` | shared exact helpers: ideal DP `analyse`, explicit `extensions` (independent cross-check), windows |
| `gadget.py` | PROVEN Lemmas 1.1 (C-prefix decomposition at the Y-gadget), 1.3 (release-time monotonicity), 2.1 consequence (cyclic sums), XYZ sanity; 4 firing controls → `out_gadget.txt` |
| `swapladder.py` | PROVEN Thm 1.4 (Swap Ladder): step monotonicity + conclusion on every nested pair; controls CTRL_H1 (drop H1) and CTRL_WIN (narrow window) must fire; coverage vs Local Linial → `out_swapladder_{1,2}.txt` |
| `slstruct.py` | Cor 1.6 (opposite full-chain ladders ⇒ balanced pair), no probabilities; 'nested balanced pair' → `out_slstruct*.txt` |
| `goodpair.py` | Zaguia's good pair (Order 2019, Def. 1) coverage vs Thm 1.4 → `out_goodpair*.txt` |
| `slrecords.py` | Thm 1.4 on mg-2912's 2 534 records → `out_slrecords.txt` |
| `longtail.py`, `bothends.py` | long-regime probe: P9 / rec11 bottoms under long zigzag tails; Q_m = both ends, n up to 46 → `out_longtail.txt`, `out_bothends.txt` (control: W6 + tail must keep WIN) |
| `ablate.py` | is P9's balance a two-end interaction? top end replaced by a tail → `out_ablate.txt` |
| `witness.py` | exact dumps of B7_m, Q_m, cross-checked by explicit enumeration where e ≤ 2·10^5 → `out_witness.txt` |
| `explain.py` | every certifying ladder on each witness → `out_explain.txt` |
| `summary.py` | assertions + coverage table → `out_summary.txt` |

Poset format: `n m_0 … m_{n−1}`, `m_i` = strict down-set bitmask of element `i`, hex.
