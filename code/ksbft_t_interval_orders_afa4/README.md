# ksbft_t_interval_orders_afa4 (mg-afa4)

Instrument for `docs/KSBFT-T-interval-orders.md`: 1/3-2/3 for interval orders.

- `iolib.py` enumerates unlabelled interval orders as canonical interval multisets. The count is certified against OEIS A022493 for n <= 10, and `gen_fast` agrees with the naive `gen` for n <= 7. It also computes exact pair laws over the ideal lattice.
- `sh run_all.sh` regenerates every `out_*.txt` and asserts the controls and the headline counts. It takes about 3 min at 3 processes; pools are sized from `POGO_WORKER_CORES`.
- Every script's docstring states the claim it tests. The doc's §8 maps each file to a section.

Every negative here has a positive control:
- the planted law error is caught (`xcheck`);
- the injection control fires 653 times (`brightwell`);
- general posets with 2+2 do have bad linear extensions (`bwgeneral`);
- semiorders always have a Zaguia-Thm-3 configuration (`zaguia3`);
- the exact search finds the n = 9 obstructions (`kdfs`).
