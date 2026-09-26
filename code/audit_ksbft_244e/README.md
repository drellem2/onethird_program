# audit_ksbft_244e — independent instrument for the audit of KSBFT-R (mg-7bfc)

Audit: [`docs/AUDIT-mg-7bfc.md`](../../docs/AUDIT-mg-7bfc.md). **Shares no code** with
`code/ksbft_r_window_padding_7bfc/`. Every poset is rebuilt from the doc's words, and the mechanics differ:
`e(S)` is memoised top-down by removing maximal elements, and `P[x before y] = e(P + x<y)/e(P)`.

```
sh run_all.sh     # ~1 min, exact Fractions, fixed seeds; exits non-zero unless 0 failed checks and every control fires
```

| file | what |
|---|---|
| `indep.py` | poset class: closure, e(S), pair laws, slot laws, range, both connectivities, module closure, ideals |
| `audit.py` → `out_audit.txt` | §A Thm 2.1 closed form at EVERY admissible i; §A' primality of attach_low (R>=4 prime, R=3 not); §B probe B on attach_both; §C double hub + Lemma 1.3(1) formula + U=W edge case; §D W*_t decomposition, the sides' only pair, insulated W* incl. the (M,6,M) family to M=30; §E non-module exact embedding; §F A28 witnesses; §G controls |
| `texists.py` → `out_texists.txt` | (T∃^any) of Prop 5.1, ideal-only vs ideal-or-filter, on random prime both-connected hosts n<=8 (instrument, not a census); POSITIVE CONTROL: the detector returns False on the V poset |

Controls that must fire (asserted): a wrong closed form (P(A∩B) replaced by P(A)P(B)) is REJECTED; probe B CERTIFIES on bare F_12;
the uniform-law detector FIRES on a module embedding; the module detector finds the single hub's non-chain module; the (T∃) detector FIRES on V.
