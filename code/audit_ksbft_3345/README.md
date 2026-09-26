# audit_ksbft_3345 — independent audit of mg-5f14 (KSBFT-Q)

Instrument for [`docs/AUDIT-mg-3345.md`](../../docs/AUDIT-mg-3345.md). `sh run_all.sh` regenerates every
`out_*.txt` (~25 s, exact Fractions, <= 2 processes) and asserts the figures the audit relies on.
`negative_control.py` plants five false statements; each must print CAUGHT.
