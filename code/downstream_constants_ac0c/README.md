# `code/downstream_constants_ac0c/` — mg-ac0c's instrument

Deliverable: [`docs/OneThird-DownstreamConstants-mg-ac0c.md`](../../docs/OneThird-DownstreamConstants-mg-ac0c.md).
Runtime **1.7 s** on this host, measured by `time sh run_all.sh` and not by addition.

## 1. What this is for, and — first — what it is deliberately NOT for

`mg-ac0c` asks: *enumerate every step and constant between L1b's conclusion and the final
contradiction; pin each non-`PROVED` one or declare it a hole; then say whether the chain
closes.* That is a **corpus enumeration followed by an arithmetic sweep**, not a measurement.

**THIS DIRECTORY ENUMERATES NO POSETS AND MEASURES NOTHING.** Every empirical or measured
input — `ε_leak`, `C₃^gap`, `C₃^cut`, `c`, `17/78`, `1/7`, the `d3c7` family — is **typed in
from the document that measured it, with its status attached in the same object**. Agreement
with those documents is **arithmetic reproduction** and is **never** corroboration of the
underlying measurement. That is `mg-7564`'s refusal, kept, and for the same reason: this
ticket's whole subject is constants quoted away from their scope, so an instrument that could
quote one would be the defect it is auditing.

`libac0c.Const` enforces it structurally: **a constant cannot be constructed without a
`status`, a `scope` and a `source`**, and a non-`PROVED` one cannot be constructed without an
explicit pin-or-hole clause. `a0` §B is the control that the refusals actually fire.

Three things nevertheless had to be **run** rather than read:

1. **The four chains, re-solved from each chain's own `Φ` bound** rather than copied from
   `mg-76b2` §6 / `mg-9461` `s1`, on code sharing no line with `lib9461.py` or `lib7564.py` —
   so a mis-transcription fails the plug-back check (`a0` §C, ten published values).
2. **The closure sweep nothing in the corpus performs** (`a2`). `mg-9461` §5.4 tabulates
   `ε_sup/ε_dem` at seven rows, all at `ε_leak = 1/5`. **Nobody sweeps `ε₀` over its whole
   admissible range**, and that sweep is the ticket's actual question.
3. **The closure requirement solved FOR `ε₀`** rather than checked at pins (`a2` §D):
   `ε₀ ≥ n/(2(n+1))`. `a3` is the novelty sweep for it, with every decisive hit printed.

## 2. Files

| file | what it does |
|---|---|
| `PREDICTIONS.md` | committed at `6a6232d`, before one line of this directory existed — **with the exposure disclosed**: `R1`–`R5` are REPORTS at zero credit because the ticket instructed me to read `mg-7564` first and I read seven more documents with it |
| `libac0c.py` | the enumeration as 25 `Const` objects that cannot exist without their scope; the four chains as four functions; the cap; the supply; the closure test |
| `a0_selftest.py` | seven controls, **three of them wrong-direction worlds**; a red here aborts `run_all.sh` |
| `a1_enumeration.py` | **the deliverable even if nothing else got done** — the table, the census, the holes, the weakest kind |
| `a2_closure.py` | the ladder over every admissible `ε₀`; the closure verdicts; the coarse pin on L2's second disjunct; the requirement solved for `ε₀`; the dial |
| `a3_novelty.py` | six **decisive** patterns with every raw hit printed, three **non-decisive** ones reported as establishing nothing |
| `out_*.txt` | the transcripts, committed |

## 3. The controls, and what each would have caught

| # | control | what it would catch |
|---|---|---|
| C1 | a float on a decision path is **refused**, with the reason printed | a `0.2` silently replacing `1/5` and rounding a verdict |
| C2 | a `Const` with no scope / no source / no pin-or-hole is **refused** | this ticket's own subject matter appearing in this ticket's own instrument |
| C3 | plug-back: ten published `ε_dem` values reproduced from the chain formulas | a mis-transcribed chain |
| C4 | **NEGATIVE**: a chain with the Cheeger square dropped gives `1/10 ≠ 1/50` | C3 agreeing automatically, i.e. proving nothing |
| C5 | **WRONG-DIRECTION**: the cap **refuses** a hypothetical `ε_dem = 3ε_leak` | a cap that admits everything |
| C6 | **WRONG-DIRECTION**: `closes()` says **YES** when fed a supply that does meet the demand | an instrument that says *does not close* whatever it is fed — which is exactly what `a2` reports, so this control is the one that makes `a2` readable at all |
| C7 | `mg-d3c7`'s family reproduced from its closed form at the four `n` `mg-9461` §4.3 prints | a mistyped family |

⚠️ **C7 REPRODUCES ARITHMETIC, NOT A POSET PROPERTY.** That every balanced-in-side pair is
evicted at every `k ≥ 3` is `mg-d3c7`'s measurement and is **not** re-verified here. If that
measurement is wrong, `a2`'s `ε₀ = 0` row is wrong with it and this instrument would not
notice. **That is the control this ticket cannot have, and it is stated rather than left to be
discovered** — the same disclosure `mg-7564` §9 makes about `C₃^gap(S_25)`.

## 4. Reproduce

```sh
sh code/downstream_constants_ac0c/run_all.sh     # 1.7 s, exit 0
```
