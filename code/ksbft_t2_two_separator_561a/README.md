# ksbft_t2_two_separator_561a (mg-561a)

Instrument for `docs/KSBFT-T2-two-separator.md`: the two-separator lemma for interval orders.
Everything is exact (`Fraction`s). `sh run_all.sh` regenerates every `out_*.txt` and asserts the headline
facts and every control (about 6 min at 3 processes; pools are sized from `POGO_WORKER_CORES`).

Generation and pair laws are imported read-only from `../ksbft_t_interval_orders_afa4/iolib.py`
(OEIS-certified generator; audited by mg-5ecf). Separators are computed from the cover relation.

| file | what it tests | control |
|---|---|---|
| `t2lib.py` | typed separators, automaton DP for joint events (Lambda_1/2/3) | twin case gives L1 = L3 exactly |
| `verify.py` | Thm 1.1 Swap Identity (all posets), Cor 1.2 (dominance exact), Prop 2.2 (Z = S) | above-only separators break the identity; Prop 2.2 fails when Z != S |
| `verify3.py` | the unconditional inequality behind Thm 3.1 (all triples) | over-cancellation fails |
| `localcc.py`, `enlarge.py` | no-go for local lemmas: locally counterexample-compatible configurations, nested enlargements | XALL column must be 0 (1/3-2/3 holds) |
| `shape.py`, `contprobe.py` | split by dominance / containment; containment pairs never locally compatible (n <= 9) | — |
| `csearch.py`, `tiefam.py` | local Lemma C boundary: T11 at slack exactly 0 (Prop 2.4 equality) | — |
| `kprime.py` | step rules (candidate lemmas) vs every Claim-K obstruction | rule K reproduces 2 / 24 / 547 |
| `kts.py`, `kstar.py` | Thm 3.1 (TS) and the non-local forms 2.1*, 3.1* vs ALL K-bad L | — |
| `general.py`, `kstar_gen.py` | Q3: the same on random general posets | — |
| `xlp.py`, `lpcheck.py`, `iis.py`, `lpsurv.py` | the LP of proven linear facts; irreducible infeasible subsystems (certificates) | K-good L refuted; 13/22 survivors stay feasible |

`csearch.py` is stochastic and is not re-run by `run_all.sh`; its finding (T11) is re-derived by `tiefam.py`.
