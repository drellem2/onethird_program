# audit_ksbft_6c30 (mg-6c30)

Independent audit instrument for `docs/KSBFT-T2-two-separator.md` (mg-561a); verdicts in `docs/AUDIT-mg-561a.md`.
`sh run_all.sh` regenerates every `out_*.txt` and runs `check.py` (31 assertions, exit 1 on failure), ~5.5 min at 3 cores.

Shares no code with `ksbft_t2_two_separator_561a/`, `ksbft_t_interval_orders_afa4/iolib.py` or `audit_ksbft_5ecf/`,
except `lpprobe*.py`, which import the author's LP builder read-only (labelled as not independent).

Controls that must fire (asserted): above-separators-only breaks the Swap Identity; over-cancelling breaks Thm 3.1;
Z != S breaks Prop 2.2; non-unique maximal breaks Prop 2.4; LCC on all of P is 0 (sanity); the own staircase family
has K-bad L and Thm-3.1 survivors (positive control for the random negative).
