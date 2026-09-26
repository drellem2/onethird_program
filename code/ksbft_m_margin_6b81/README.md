# ksbft_m_margin_6b81 — prefix certificate, margins, covariance decay for KSBFT-M (mg-6b81)

Instrument for [`docs/KSBFT-M-margin-induction.md`](../../docs/KSBFT-M-margin-induction.md).

```
sh run_all.sh      # ~15 min, 1 process, ~2 GB RAM; poset lists live in a temp dir
```

`pcert.c` `#include`s mg-eedd's `../ksbft_one_pt/onept.c` verbatim (generator, canonical form, exact
`__int128` linear-extension counter) and adds:

| mode | what it does |
|---|---|
| `gencut IN OUT D` | pruned generator: non-CUT classes of range <= D (Lemma 2.5: complete) |
| `cert FILE START STRIDE D` | Theorem 2.4's certificate for every class: robust margin rm(Q,s), CUT flag |
| `e2e FILE START STRIDE t D OFF` | Theorem 2.4 end to end on actual P (OFF=1 is the firing control) |
| `delta FILE START STRIDE THR` | delta(P)-1/3 on indecomposable non-chains; LOW lines below THR |
| `decay FILE START STRIDE` | exact transport error p_P - p_{P-v} vs G(P)-distance, and transport margins |
| `onept ...` | every onept.c mode (fib / brute controls, full census generator) |

| file | content |
|---|---|
| `out_gen.txt` | full-census counts (A000112 control, n<=8; range<=3 to 13) and pruned counts D=3 (t<=13), D=4 (t<=15), D=5 (t<=13) |
| `out_controls.txt` | counter controls, pruned-vs-full cross-check, e2e (0 violations) and its firing control, narrowed-interval firing control |
| `out_cert_d3.txt`, `out_cert_d4.txt`, `out_cert_d5.txt` | the certificate tables (`AGG CT t total CUT fail failCUT`) |
| `out_base.txt` | delta-1/3 minima (`AGG LT pi count below num den n poset`) — the base cases and the exceptional list |
| `out_decay.txt` | `AGG DM pi_v d count num den` (max transport error), `AGG DT d count num den` (worst transport margin) |
| `out_timing.txt` | wall-clock of the big steps (the only non-deterministic file) |
