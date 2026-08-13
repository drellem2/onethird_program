# Predictions — `mg-9b6b`, with the exposure disclosed per line

**Written before the arms were written, and the one thing that was already known when they were
written is disclosed at P4 rather than left for a reader to notice.** A prediction whose exposure
is not stated is decoration; a prediction made after the measurement is worse than none.

**WHAT WAS ALREADY MEASURED WHEN THESE WERE WRITTEN.** One exploratory probe, in the scratchpad
and not committed: the envelope `min{δ : d ≥ t}` over every isomorphism class at `n ≤ 7`, which is
what suggested this directory's subject in the first place. So **P4 and P7 were made with the
`n ≤ 7` staircase already in front of me** and are predictions about `n = 8` only; P1, P2, P3, P5,
P6, P8 and P9 were made blind. Every arm was written after that probe. Nothing else was run.

| | prediction | exposure — what a wrong answer would cost |
|---|---|---|
| **P1** | `S_f ⟹ (2_D) ⟹ (1_D)` and back, with the `>`/`≥` gap exactly one density quantum `1/C(n,2)` | If the converse needs more than the step `f`, the collapse is ONE-directional and §2's headline must read *"at least as strong as"* rather than *"is"*. |
| **P2** | The frozen class `δ < 1/3` is empty at every `n ≤ 8` | A single member REFUTES the (1/3)–(2/3) conjecture. This is the arm's own strongest self-check and its most valuable failure. |
| **P3** | `(1_D)` and `(2_D)` have the SAME counterexample set at every `D` and every `β`, while their HYPOTHESIS populations differ by three orders of magnitude at `β = 1/3` | If the counterexample sets differ, the implementation is wrong — the two are contrapositives and a run cannot improve a tautology's warrant, only catch a coding error. |
| **P4** | The envelope's first step at `n = 8` sits at F23's `4⌊n/3⌋/(n(n−1)) = 1/7` | Agreement is computed through `lib6ff4`, the library F23 was measured with, so it is a CONSISTENCY check. Disagreement would be the informative outcome and would impeach this directory, not F23. |
| **P5** | `F(D_needed, n) = 1/3` EXACTLY at every `n ≤ 8` — the needed density-to-balance bound is tight with zero slack, witnessed by the boundary class | If the envelope at `2e-2` were strictly above `1/3`, the needed `f` would have slack at reachable `n` and the *"zero slack"* half of the finding is gone. |
| **P6** | `G(s) = max{d : δ ≤ s}` is non-empty and RISING for `s ≥ 1/3` and EMPTY for every `s < 1/3`, at every `n ≤ 8` | Same exposure as P2 on the empty side. On the non-empty side, a FLAT `G` would mean there is no density-to-balance relation at all and §3's *"it rises in the wrong place"* becomes *"it does not rise"*. |
| **P7** | At `n = 8` the envelope has at least 4 distinct steps | A relation that is real is what makes this route keep looking alive; if it were flat the route would have died on its own years ago and this document would have no subject. |
| **P8** | Feeding the dial the ceiling the DATA exhibits — `D(n) = 4⌊n/3⌋/(n(n−1))` — forbids a primitive poset from being frozen at every `n ≥ 4`, i.e. delivers the whole conjecture rather than 84 orders | If the crossing were at some large `n`, the data end would be a genuinely weaker statement than the target and the dial would have a usable point on it. **This is the prediction that decides the document.** |
| **P9** | The wrong-direction control — the same dial at `β = 2/5`, where the class is NON-empty — returns a real ceiling strictly below `1` at every `n = 3…7` and fires on explicit counterexamples at a `D` below it | Without this, every *"empty"* and every *"no lever"* in this directory could be a property of the tool. If the control cannot make the machinery fire, nothing here is falsifiable by this suite. |

---

## Outcome, filled in after the run — and the refuted ones are kept, not edited

*This table is filled in from the committed transcripts after the run. It is left empty in the
commit that writes the predictions and in no other.*

| | outcome |
|---|---|
| **P1** | **HELD.** Both directions instantiate; the `>`/`≥` gap is exactly the posets sitting ON the threshold, non-empty in 1 of the 60 cells (`e1` m2). |
| **P2** | **HELD.** 0 frozen posets at every `n ≤ 8` — 16 998 non-chain classes at `n = 8` (`e0` T6). |
| **P3** | **HELD.** Identical counterexample sets in all 60 `(n, β, D)` cells; hypothesis populations `0` against `2 044` at `β = 1/3`, `n = 7` (`e1` m2). |
| **P4** | **HELD.** `1/7` at `n = 8`; the closed form reproduces at every `n = 3…8` (`e2` m3). Consistency, not corroboration, and the table says so. |
| **P5** | **HELD.** Slack exactly `0` at every `n = 3…8`, witnesses the boundary class (`e2` m4). |
| **P6** | **HELD** on both sides: `G` is non-decreasing and non-empty for `s ≥ 1/3`, EMPTY in all 15 cells below it (`e2` m1). |
| **P7** | **HELD, and by more than the threshold asked**: 10 distinct steps at `n = 8`, running `1/3 → 1/2` (`e2` m2). |
| **P8** | **HELD, AND THE CROSSING IS AT `n = 4`.** The data end delivers the conjecture at every `n ≥ 4` — a strictly worse buy than the 84 orders `mg-0b96` priced at the constant end (`e3` m4). |
| **P9** | **HELD, with figures I did not predict**: ceilings `2/3, 1/3, 1/2, 2/5, 4/7` at `n = 3…7` — **not monotone in `n`**, which I had not thought about — and the machinery FIRES at all five (`e0` T7). |

**Nothing was refuted, and that is stated rather than enjoyed**, because it is the outcome a
prediction list is worth least: seven of the nine are consequences of things already on the record
(P1 is contraposition, P2 is the conjecture at small `n`, P3 is a coding check, P4 is F23, P5
follows from P4, P6's empty half follows from P2). **The two that could have gone either way are
P8 and P9**, and P8 is the one the document turns on. P7's threshold was set from the `n ≤ 7` probe
and is not a blind prediction.

**Three things came out differently from how they were written, and none of them is a prediction:**

- **P9's ceilings are NOT monotone in `n`** (`2/3, 1/3, 1/2, 2/5, 4/7`). Nothing rests on it; it is
  recorded because a control whose shape surprises you is worth a line.
- **`e1` m3's witness set is RAGGED.** The first draft asserted *"every `n ≤ 66`"* and the arm was
  changed to COMPUTE the set instead, which found the hole at `n = 65` — `65 = 3·21+2`, so `⌊n/3⌋`
  sticks at 21 while `D_needed` keeps falling. The claim that would have shipped was false at
  exactly one value.
- **`e3` m5's threshold is `2/15` and is NOT ATTAINED.** The first draft searched a grid of `2/k`
  and reported the largest hit, `1/8` — a fact about the grid, not about the question. The check
  now tests both sides of the strict bound.

