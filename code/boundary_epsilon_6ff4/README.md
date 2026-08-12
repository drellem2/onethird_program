# `code/boundary_epsilon_6ff4/` — `ε_spec` at `δ(P) = 1/3` exactly

The instrument for `mg-6ff4`. Deliverable:
[`docs/OneThird-BoundaryEpsilon-mg-6ff4.md`](../../docs/OneThird-BoundaryEpsilon-mg-6ff4.md).
Predictions, filed before any code existed and with the exposure disclosed:
[`PREDICTIONS.md`](PREDICTIONS.md).

**What it measures.** `ε_obs(P) = 6·E[inv_e]/(n²−1)` over the **boundary class** `δ(P) = 1/3`
exactly — the closest non-empty approximation to the frozen class, which is empty at every `n` any
enumerator reaches.

⚠️ **`δ = 1/3` is OUTSIDE the frozen hypothesis, which is strict.** Nothing produced here is a
frozen-class number. Every arm says so in its own output.

## The arms

| arm | what it does | cost |
|---|---|---|
| `c0_selftest.py` | the controls, **including two that must fail**: a deliberately wrong reference order (must move `ε`) and a constructed frozen pair table (must not be classified as boundary). Also checks class counts vs OEIS A000112, the census against `mg-7c78` `a5`'s printed table, the `E[inv_e]` shortcut against brute-force enumeration of `L(P)` **in and out of scope**, ordinal additivity on 305 explicit sums, and the two-atom law's saturation of `n/(n+1)`. | ~45 s |
| `c1_census.py [nmax]` | the census and the distribution, **exhaustive over every isomorphism class** to `nmax` (default 9). Min/median/max of `ε` per `n`, the argmax poset, and the structural check that every boundary poset is an ordinal sum of singletons and copies of the 3-element `V`. | ~5 min at `n = 9` |
| `c2_reach.py` | reach beyond the exhaustive range, bought with a **width restriction** that is named at every table: width `≤ 3` exhaustive to `n = 10`, width `≤ 2` exhaustive to `n = 12`. The one question it asks is whether a **new primitive** poset with `δ ≤ 1/3` appears. | ~10 min |
| `c3_gap.py [nmax]` | the realizability gap: `n/(n+1)` (attained by the two-atom law, which is not a poset) against the worst actual boundary poset, as a **difference and a ratio**; the `mg-6bc2` identity `ε_spec = 3·d·q̄·n/(n+1)` at every member; and the extrapolated crossing with `ε_dem`, labelled as extrapolation. | ~5 min |
| `c4_e_choice.py [nmax]` | how `e` is chosen and whether the choice is forced: the strict `> 2/3` tournament, the weak `≥ 2/3` one, uniqueness, whether `e ∈ L(P)`, `ε` against every alternative reference order, and the 3-cycle that would break it. | ~3 min at `n = 8` |

`sh run_all.sh` runs all five and reports the worst exit. **This suite is NOT in `build.sh`** — it
is a one-off measurement, not a control, and the committed `out_*.txt` are its record.

## The one identity everything rests on

`e` orients every incomparable pair toward its `≥ 2/3` side, so `Pr[σ disagrees with e on {x,y}] =
min(p_xy, 1−p_xy)` and `E[inv_e] = Σ_{x∥y} min(p_xy, 1−p_xy) = m·q̄`. No arm has to enumerate `L(P)`
to get `E[inv_e]`; `p_xy` alone suffices, which is what makes an exhaustive `n = 9` sweep affordable.

⚠️ **It is valid ONLY where the `≥ 2/3` tournament is total, i.e. exactly where `δ(P) ≤ 1/3`.** `c0`
T3 measures the failure out of scope: **192 of 388 posets at `n ≤ 6`**. Every arm applies it inside
its scope only.

## Independence

Imports nothing from this repository — standard library only, own canonical form, own linear-
extension counter. That is deliberate: this arm re-measures a census `mg-7c78` `a5` already
published, and a re-measurement sharing that arm's code could not distinguish "the census is right"
from "the two runs share a bug". `c0` T1/T2 are the two independent ways a silent class merge would
be caught.
