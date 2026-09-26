# ksbft_t3_lemma_c_785e (mg-785e)

Instrument for `docs/KSBFT-T3-lemma-C.md`: Lemma C, XYZ on Q12, and the full-measure lift.

- **Exact (pure Python, Fractions):** `probe8.py` (X-law of containment two-separator pairs, n <= 10),
  `xyzlp.py` (pair-LP of mg-561a + triple laws + McCormick XYZ, exact simplex), `verify_certs.py`
  (exact check of the 14 pointwise certificates in `certs.json`, with 3 controls that must be CAUGHT).
- **Float probes (scipy/HiGHS, not installed system-wide; run from a venv via `PY_SCIPY=...`):** `bnb.py`,
  `xyzcheck.py`, `mulp.py` users (`mu_q12*.py`, `mu_surv.py`, `window*.py`, `local_q12.py`), `certify.py`,
  `gen_certs.py`. They only propose multipliers; nothing is claimed from them as a proof except via `verify_certs.py`.
- Imports read-only: `../ksbft_t_interval_orders_afa4/iolib.py`, `../ksbft_t2_two_separator_561a/{t2lib,lpcheck,xlp,out_lpsurv.txt}`.

`sh run_all.sh` regenerates and asserts (exact part ~4 min; + ~35 min with scipy).
