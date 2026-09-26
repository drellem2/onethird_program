# audit_ksbft_5ecf (mg-5ecf): audit of mg-afa4 (KSBFT-T, interval orders)

Instrument for `docs/AUDIT-mg-afa4.md`. It shares no code with `code/ksbft_t_interval_orders_afa4/`.

`sh run_all.sh` regenerates every `out_*.txt` and asserts the controls and the reproduced figures. It takes about 3.5 min, and its pools are sized from `POGO_WORKER_CORES`.

| file | what |
|---|---|
| `eng.py` | Own engine. `gen` is a DFS over canonical interval multisets; it is certified by the OEIS A022493 counts plus `recanon`, which recomputes Fishburn's canonical form from the poset. Also: separators from the cover relation, a bad-L DP over (ideal, last element), exact pair laws. |
| `controls.py` | `laws` and `badL` against brute-force enumeration (planted error caught; general 2+2 poset control). Also Prop 3.1 and Cor 3.2 over all pairs with n ≤ 8. |
| `census_k.py` | Claim K over all interval orders with n ≤ 10. |
| `census_delta.py` | δ census and the §5 C1/C2/C7 counts over the author's population with n ≤ 9. |
| `witnesses.py` | T8/T13/T14/N12/P9/Q_m/mg-7bfc hosts/O9a/O9b: interval-order status, δ, and Thm 2.1(b) on every ordered pair. Also 400 random interval orders; the above-only control fires. |
| `props.py` | Prop 2.4 (exhaustive, n ≤ 6); n = 10 obstruction shape; Claim K on the bounded-range interval-order witnesses and on a targeted staircase+long-interval family. |
| `sl.py` | §3.4: bad L filtered by SL1/SL2 and their duals, implemented from the mg-ce69 Thm 1.4 text. |
| `misc.py` | §4 Doubling in interval form (with control); the §0 "equivalent" claim (A ⟹ B fails). |
