# audit_ksbft_af00 — instrument for docs/AUDIT-mg-0b78.md (mg-af00)

Independent of `code/ksbft_p1_walled_0b78` (no shared code). Exact integers/Fractions, seeded, one process.

```
sh run_all.sh    # ~70 s
```

| file | what |
|---|---|
| `check_af00.py` → `out_check_af00.txt` | Prop 5.5 closed form vs brute force (C_m ⊔ C_n, m≤4, n≤7; C_2 ⊔ C_D, D=2..8); the §5.3 range-4 exhibit; Ex 5.7 arithmetic; exhaustive labelled n≤6 + 300 seeded random n=7,8: Prop 3.1(6) support, Lemma 5.1, Lemma 5.2, Stanley, Ma–Shenfeld k=1 consistency, mg-48ab Thm 5.2 (VACUOUS here: no poset n≤8 has δ<1/3); Z_m least deficit |
| `check_af00_ctl.py` | negative controls: Lemma 5.1 summed over ALL j-subsets and Lemma 5.2 with bound π(z)−1 must FIRE; observation that π(z) already suffices in Lemma 5.2 |
| `subfamily_af00.py` → `out_subfamily_af00.txt` | the audit's §5.5(b) remark (deficit = q²/(1+2q), q quantised) and the finite (L*)/(F)&(M♯) witness ranges re-decoded with this audit's own closure |
