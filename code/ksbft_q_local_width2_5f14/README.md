# ksbft_q_local_width2_5f14 — Local Linial probe (mg-5f14)

Instrument for [`docs/KSBFT-Q-local-width2.md`](../../docs/KSBFT-Q-local-width2.md). Pure Python, exact
integers and Fractions. Census files are produced by mg-eedd's generator (`../ksbft_one_pt/onept.c`, compiled
through `../ksbft_m_margin_6b81/pcert.c`, mode `onept gen`). Its control is OEIS A000112, reproduced in
`out_gen.txt`.

```
sh run_all.sh     # ~1 h wall, 3 processes (POGO_WORKER_CORES); temp census dir is deleted
```

| file | role |
|---|---|
| `probe.py` | per indecomposable poset: position laws of minimal elements, pair counts. It checks Thm 2.1 (Local Linial) and Lemma 1.1, which are PROVEN, so a violation would be a bug, and it classifies each poset by LL / structural LL / BR / WIN / minimal-pair tests. Controls: `NEGCTRL=1` narrows "balanced" to [0.34,0.66] (the LL check MUST fire); `MONOCTRL=1` applies Lemma 1.1's test to non-minimal elements (it MUST fire) |
| `records.py` | LL on mg-2912's 2 534 kept records (`../ksbft_range_probe/out/*.jsonl`) → `out_records.txt` |
| `min3.py` | candidate "≥3 minimal ⇒ balanced minimal pair": counterexample histogram → `out_min3.txt` |
| `show.py` | exact dump of one poset (the witnesses of §3) → `out_witnesses.txt` |
| `summary.py` | census table + assertions (exit 1 if a PROVEN check is violated or a control did not fire) → `out_summary.txt` |
| `out_all.txt`, `out_d3..d6.txt` | raw `AGG`/`WIT` transcripts: all posets n ≤ 9; range ≤ 3 (n ≤ 13), ≤ 4 (n ≤ 12), ≤ 5 (n ≤ 11), ≤ 6 (n ≤ 10), for n ≥ 9 |

Poset format: `n m_0 … m_{n−1}`. `n` is decimal, and `m_i` is the strict down-set bitmask of element `i`, in hex.
