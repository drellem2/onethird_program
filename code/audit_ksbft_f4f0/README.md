# audit_ksbft_f4f0 (mg-f4f0)

Independent audit instrument for `docs/KSBFT-T3-lemma-C.md` (mg-785e). The verdicts are in `docs/AUDIT-mg-785e.md`.
`sh run_all.sh` regenerates the deterministic transcripts and asserts every headline and control (~2 min, 1 core).
`PROBES=1 sh run_all.sh` also re-runs the stochastic searches (~25 min at 3 cores).
`PY_SCIPY=<python with scipy> sh run_all.sh` also re-runs the float LP probe.

**Independence.** No code is imported from `ksbft_t3_lemma_c_785e/`, `ksbft_t2_two_separator_561a/`, `iolib.py` or earlier audits.
- `eng.py` is my own engine: a Fishburn-matrix generator (counts certified against A022493 up to n = 10), covers, separators, lexicographic extension enumeration, the ideal DP, an automaton DP and `canonical()`.
- Author files are read as **data only**: `certs.json` (the λ, y weights) and mg-561a's `out_lpsurv.txt` (the 22 survivors).
- `out_repro_xyzlp.txt` is the one exception: it is the author's `xyzlp.py` re-run unmodified, and it is labelled a reproduction, not an independent check.

**Controls that must fire (asserted).**
- Certificates: λ×9/10 on Q12; the largest row weight sign-flipped; a wrong `L`; no rows; A-only rows; a non-τ-invariant event.
- Prop 1.1: a conditioning event that is not τ-invariant, and A-only separators.
- `canonical()` fixes every Fishburn representation.
- The n = 10 tight case of mg-785e §4.1 must NOT be an X-local failure.
- K_C search: Q12 with (iii) allowed is found, and the whole pipeline with (iii) allowed finds 49 L (`kc_ctl.py`).

| file | output | what |
|---|---|---|
| `certs_indep.py` | `out_certs_indep.txt` | 14 certificates re-checked exactly with own rows; §3.2 certificate from the prose |
| `prop11.py` | `out_prop11.txt` | Prop 1.1: enumeration n = 5..9 (general + interval), automaton DP n = 12..20 |
| `xlocal.py`, `mech.py` | `out_xlocal.txt`, `out_mech.txt` | §4.1 census n ≤ 10 (own generator); the mechanism on the 29 non-twin cases; Q12, T11 values |
| `xclimb.py` | `out_xclimb_*.txt` | hill-climb counterexample search for the X-local form, n = 11..20 (canonical form) |
| `xfail.py` | `out_xfail.txt` | exact verification (2 DPs + brute force) of X12 and X14, the X-local failures |
| `lcc12.py` | `out_lcc12.txt` | LCC levels of X12/X14 (X, X∪Y, X∪Y∪Inc(S), P) |
| `prop21.py` | `out_prop21.txt` | Prop 2.1 witness point; X12 realises the Prop 2.1 local system (γ computed directly) |
| `kc.py`, `run_kcsearch.sh`, `kc_ctl.py` | `out_kc.txt`, `out_kcsearch_s1{1,2}.txt`, `out_kc_ctl.txt` | K_C patterns on the 22 survivors; K_C counterexample search n = 11..14 + pipeline control |
| `canon_check.py` | `out_canon_check.txt` | control for `canonical()`; the non-canonical n = 18 artifact |
| `lp_indep.py` | `out_lp_indep.txt` | FLOAT: own certificate LP on Q12 (§3.3 locality table, §6 k = 0 value) |
