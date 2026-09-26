# audit_ksbft_ebbe — independent audit instrument for KSBFT-S (mg-cfba), audit mg-ebbe

Instrument for [`docs/AUDIT-mg-cfba.md`](../../docs/AUDIT-mg-cfba.md). Shares no probability code with the
author's `code/ksbft_s_nested_balance_cfba/` (`nb.c`) or with mg-ce69's `lib.py`. The only imported pieces are
the census generator (`../ksbft_m_margin_6b81/pcert.c`, counts asserted against OEIS A000112) and, for
`families_dump.txt` only, the author's family **constructors** (`fam.py`), whose outputs are then checked here.

```
sh run_all.sh    # ~20 s, 1 process, exit 1 on any failed assertion
```

| file | what |
|---|---|
| `aud.c` | Exact pair laws by forward x backward ideal counts (dense 2^n table, n <= 22). Per poset: e, delta, deltaN, deltaP (primal), deltaD (dual), non-nested count, closed/open NB, PNB, dual-PNB, Lemma 1.1 mismatches (non-nested vs doubly 2+2-trapped), Doubling Lemma violations. `-v` prints pairs; `-control` plants two defects (top-only trap rule, tripling instead of doubling) that must fire. |
| `xcheck.py` | `aud.c` vs explicit permutation enumeration on all posets n <= 6 and 400 random n = 7; control: a planted primal classifier must disagree. |
| `census.py` | NB / PNB / dual-PNB / Lemma 1.1 / Doubling over the full n <= 9 census; open-window failures; deltaN = 1/3 ties; own primality, indecomposability, range. |
| `witnesses.py`, `witnesses_lib.py` | T8, T13, T14, N12 exact values, structure and mechanism; interval-order / non-nested status of all 54 named family members (Q_m m = 0..14, F_5..F_30, B7 tails, mg-7bfc hosts). |
| `goodpair.py` | Own firing full-chain good-pair detector: N12 has none (control T8 has 8). |
| `records.py` | mg-2912's 2 534 records: NB, PNB, dual-PNB, interval-order share. |
| `out_*.txt` | transcripts |
