# audit_ksbft_f889: independent audit instrument for mg-6b81 (KSBFT-M)

Report: [`docs/AUDIT-mg-6b81.md`](../../docs/AUDIT-mg-6b81.md).

```
sh run_all.sh      # serial, 1 process, ~70 min, ~1 GB temp (deleted); ends with check_controls_f889.py
```

`indep_f889.py` is pure Python, exact (`Fraction`), and shares no code with `pcert.c`/`onept.c`. Its canonical form is the least down-row tuple over all natural labellings. It counts by DP over order ideals.
Step 5 of `run_all.sh` re-runs the **author's** `pcert` to obtain the D=4 t=14/15 lists (a reproduction, not an independent check), and applies `indep_f889.py` to its failures, its extremes, and a 1 % stride sample.

| file | content |
|---|---|
| `out_a000112.txt` / `out_control_brokencanon.txt` | canonical-form positive control / NEGATIVE CONTROL (broken canon overcounts) |
| `out_full3.txt` | unpruned range<=3 census, CUT counted afterwards (generator completeness without Lemma 2.5(b)) |
| `out_gen3.txt`, `out_gen4.txt` | pruned non-CUT counts, D=3 t<=13, D=4 t<=13 |
| `out_cert3.txt`, `out_cert4.txt` | Theorem 2.4 certificate, D=3 t=9..12 (+ s=8 at t=11), D=4 t=10..13 |
| `out_control_narrow.txt` | NEGATIVE CONTROL: interval [2/5,3/5] leaves classes uncertified |
| `out_base3.txt`, `out_base_all8.txt` | delta-1/3 on indecomposable posets (Pi_3 n<=11; all posets n<=8) |
| `out_witness.txt` (`witness_f889.py`) | mg-2912's n=21 range-4 witness: delta-1/3 = 721/46455 < 5/318 |
| `out_e2e.txt` | Theorem 2.4 on random large P vs directly counted p_P; OFF=1 is the NEGATIVE CONTROL |
| `out_pcert_rerun.txt` | the author's pcert re-run: gencut D=4 to t=15, cert t=14/15, delta n=12..15 |
| `out_sample_d4.txt` | my certifier on pcert's 14 t=14 failures, its t=14/15 extremes, a 1 % sample of t=15 |
| `out_check_controls_f889.txt` | every assertion; VERDICT GREEN/RED |
