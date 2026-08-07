# `libweak_c3ca` — the instrument behind `docs/OneThird-LIBweak-mg-c3ca.md` (mg-c3ca)

Exact integer arithmetic throughout; no sampling, no randomness, no `n`-dependence hidden in a
tolerance. Run from this directory:

```
python3 selftest_c3ca.py      # 29/29, exit 0     -> out_selftest_c3ca.txt
python3 p1_census.py 6        #                   -> out_p1_census.txt
python3 p2_primitive.py 6     #                   -> out_p2_primitive.txt
python3 p3_window.py 6        #                   -> out_p3_window.txt
```

## Population and grain (repeated at every printed count)

**POPULATION** — every *naturally labelled* poset on `n` elements: every transitively closed
subset of `{(i,j) : i < j}`. An isomorphism class appears once **per compatible labelling**, not
once. Every readout is a max or a min over the population, and duplication does not move either.
**GRAIN** — one naturally labelled poset (P1, P2); one incomparable pair of one such poset (P3).

`E_maj := Σ over incomparable pairs of min(p, 1−p)`. This **is** `E[inv_e]` whenever the majority
order is a linear order (proven for frozen posets — the doc §1 re-derives it), and is a lower
bound on `E[inv_r]` for **every** reference order `r` otherwise, which is the conservative
direction for a probe hunting *large* `E[inv_e]`.

## What each pass is for, and what it found

| pass | question | answer |
|---|---|---|
| `selftest` | can the instrument be trusted, and can it report both answers? | 29/29. Positive controls: `V` poset (`δ = 1/3`, `E_maj = 2/3`), antichain (`δ = 1/2`), chain (`δ` undefined, **not** 0), `W_m` against the hand formula at `m = 4,6,8`. §F drills the detector on a constructed `δ < 1/3` table so a null result in P1 is not the code's inability to say so. |
| `p1_census` | as `δ` falls to its floor, what happens to `E[inv_e]/n²`? | `min δ = 1/3` **exactly** at every `n ≤ 6`; **0** frozen posets (as the conjecture requires). Max `E_maj/n²` on the critical family falls `0.074 → 0.037`. |
| `p2_primitive` | same, on the population the architecture admits (primitive = incomparability graph connected) | P1's critical witnesses are **ordinal sums** and therefore excluded. Primitive `min δ` is strictly above `1/3`: `0.400, 0.364, 0.357` at `n = 4,5,6`. Max `E_maj` there is `0.67, 1.00, 1.55, 1.64` — `Θ(n)`-shaped, i.e. LIB-scale. |
| `p3_window` | a test of the doc's **own** forward vector, built to be able to kill it | it fired. The marginal form `min(p,1−p) ≥ (1/3)(1−TV)` is **FALSE**: 8 088 counter-pairs at `n = 6`. The surviving threshold form has a threshold that **moves with `n`**: `s* = 0.500, 0.636, 0.737` at `n = 4,5,6`. |

## Reach caveat

`n ≤ 6`. A `Θ(n)`-mobility configuration — the object §3 of the doc identifies as the only thing
that can violate (LIB-weak) — **cannot appear at this size**. None of these numbers is evidence
about the asymptotic threat; they are evidence about the boundary of the frozen class, which is
a different thing, and the doc says so where it uses them.

## Recorded defects of this instrument

1. `selftest` §E first asserted `δ(W_m) = 1/2` from STATE.md:102's parenthetical. **The
   assertion was wrong, not the code** — `δ(W_m) = ⌊(m+1)/2⌋/(m+1)`, which is `1/2` only at odd
   `m`. Fixed to the hand formula; the correction is carried in the doc §3 because it is a
   (consequence-free) correction to merged text, not to this code.
2. ~~`p3_window` was first written with the linear form of (MW) only. It reported 8 088 refuters
   and nothing else — a refutation with no measurement of what survives.~~ The `s*` readout was
   added afterwards, and it is `s*`, not the refuter count, that carries the finding.
   **[CORRECTED — mg-2df8, on mg-c4f5 §4. This note cannot be true as written, and it is the
   RECORD OF HOW THE MISLABEL SURVIVED.** A linear-form predicate over this population returns
   **0** refuters, not 8 088 — measured at every `n ≤ 7` over 1 168 036 pairs. So `p3_window` was
   never linear-form-only *and* 8 088-producing; the committed `:100` evaluates
   `sim >= 0.5 and mn < 1/3`, a **threshold** predicate, and 8 088 is its correct count. The
   predicate was changed to the threshold form while the *label* stayed linear, in this note and
   in the doc's §5 — **which is exactly why the number kept its wrong name for long enough to
   reach STATE.md and Daniel.** The count was never in doubt; nobody re-read the predicate beside
   the sentence quoting it.**]**
3. `p1_census` walks the population twice (once to find `min δ`, once to collect the critical
   family). Correct but wasteful; it is why `n = 7` was not attempted here.
4. `p2_primitive`'s `delta <= 0.3333` band prints `0 posets` for `n ≥ 4`. That is the finding
   (no primitive poset attains `1/3` at those `n`), but a band that is empty for a *coverage*
   reason and a band that is empty for a *mathematical* reason print identically. Read it beside
   the `min delta, PRIMITIVE only` line, which distinguishes them.
