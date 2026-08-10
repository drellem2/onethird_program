# mg-17aa — predictions, committed BEFORE any script of this ticket exists

The ticket: extend the `[CANNOT FAIL]` treatment to all four I-rows of NEGATIVE
CONTROL 4. mg-e35b landed the row for three of them and recorded the fourth as
its own item; this is that item.

Everything below is written against a tree at `744cfd5` on which I have run
exactly one command — `python3 controls.py 5`, the unmodified battery — and read
source. No probe of this ticket exists yet.

## Exposure, disclosed rather than laundered

These are not forecasts. They are things I already know from reading, and every
prediction that depends on one is marked.

- **H1 — I have read the whole of `negative_control_incidence` and both parent
  READMEs.** So I know the shipped routing quantity is `diag_preserved == 0`,
  that I4's is 3 of 61, and that mg-f1b2's F1 argument says the three
  diagonal-preserving posets are settled by `|s_i s_j| = 1`. P1 is therefore a
  bet about whether that argument *survives being asked mechanically of every
  pair*, not a bet about what the shipped counts say.
- **H2 — the ticket's stated input is already refuted on `main`.** The ticket
  says to take as input that three of the four `>= 3 facets` zeros are FORCED
  and "only I4's is a result", and to check it. `mg-8af0` (`12a1553`,
  `66130f8`, 2026-08-05, one day after this ticket was filed) landed the finding
  that **all four are forced**, and mg-e35b's README carries a struck-through
  correction saying so. I read that before writing this. So P9 is a report, not
  a bet, and I say so where it appears.
- **H3 — I have not run any absorbability sweep, any deletion test, or any
  planted world.** Every count in P1–P8 below is unmeasured at the time of
  writing.

## The bets

| # | p | claim | what falsifies it |
|---|---|---|---|
| **P1** | **0.90** | **I4's `absorb == 0` is FORCED**: on every one of its biting posets the pair `(L_mut, target)` violates at least one of the two gates that are forced by `s_i^2 = 1` / `|s_i s_j| = 1`, so no sign vector can absorb it and the count could not have come out otherwise. | one biting poset where `gate_violations(L_mut, target)` is empty — the pair clears both forced gates and the answer really is decided by signs. |
| **P2** | 0.85 | The forcing is a **disjunction of two theorems and neither alone covers I4**: the diagonal theorem covers 58 of 61 and the magnitude theorem is needed for the remaining 3 (the antichains). So the shipped `[CANNOT FAIL]` row's condition `theorem_diag == theorem_app` is the wrong generalisation and has to become "each pair is blocked by *a* checked theorem". | diagonal-preserved count for I4 is 0 (one theorem suffices), or the 3 are not covered by the magnitude gate either. |
| **P3** | 0.80 | **The tree already contains a control that goes RED the day this ticket is done.** The routing row scores `0 < len(forced_rows) < len(muts)`. Routing I4 to forced makes that `0 < 4 < 4` = False, so the battery exits 1 on a row whose failure means the section became *more* honest. This is the exact shape mg-e35b warned this ticket about — and it was already in the tree, pointing at this ticket. | the extension leaves the battery exiting 0, i.e. the routing row does not go red. |
| **P4** | 0.75 | `rej == app` is a forced conjunct in **all four** rows — forced *given the baseline row*, not absolutely: `app` counts `L_mut != L_true`, the baseline row scores `L_true == target` on the whole population, and the two together force `L_mut != target`. Deleting the clause from all four changes no verdict on the real population. | a poset with `L_mut == target != L_true`, or a verdict that moves under the deletion. |
| **P5** | 0.70 | `shape_ok == app` is forced by construction in all four: the compared matrices are `|L(P)| x |L(P)|` and no `incidence_mode` changes the number of facets. Deleting it changes no verdict. | any of the five modes producing a facet list of a different length on any poset. |
| **P6** | 0.60 | After the extension, **I4 is the row with the LEAST measured content of the four**, not the most: it has no `caused` clause (it is not localised), so its scored condition reduces to `app > 0` plus forced conjuncts, while I1/I2/I3 keep `caused == app`. The row that was kept scored *because* its absorbability answer was supposedly a decision is the one with a single contingent conjunct. | I4 retaining two or more contingent conjuncts. |
| **P7** | 0.65 | **Every one of the four rows CAN fail, and I can exhibit the input**: for each row there is a constructible input on which its remaining scored condition, evaluated by the same predicate the battery uses, is FALSE — 4 of 4 for `app > 0` (a no-op mutation) and 3 of 3 for `caused == app` (a mis-predicted residual). So the answer to the ticket's question is *not* that any I-row is itself a `[CANNOT FAIL]` row; it is that one **clause** of one row is. | any row for which no falsifying input is exhibited. |
| **P8** | 0.50 | The `>= 3 facets` bound and the `absorb == 0` forcing are **independent** questions, and mg-8af0's finding does not settle mine: a corruption could raise no ridge's facet count and still be absorbable. So H2 corrects the ticket's premise without answering the ticket. | the two turn out to be the same forcing. |
| **P9** | — | **Report, not a bet** (see H2): the ticket's input premise "only I4's `>= 3 facets` zero is a result" is FALSE and was corrected on `main` by mg-8af0 the day after this ticket was filed. I will check it rather than re-derive it, and say which commit answers it. | — |

## Named conditions for NOT making the change

Filed in advance so that a refusal cannot be assembled after the fact. I will
**not** route I4 into the `[CANNOT FAIL]` row if any of these holds:

1. **P1 falsifies** — some biting pair clears both forced gates, so the answer
   there is a real decision and the clause belongs in a scored condition.
2. The forcing holds at `n <= 5` but I find a **constructible poset at n = 6**
   where it does not, i.e. it is a measurement of this population and not a
   theorem at every `n`.
3. Removing the clause would leave a row with **no** contingent conjunct at all
   — a row that is entirely theorem should be a `[CANNOT FAIL]` row in full, not
   a scored row with an empty condition, and that is a different change.

## The trap, and how I intend not to walk into it

mg-e35b declined to score the I4 vacuity split because *"a row scoring 'the
split separates' would go RED the day somebody FIXED the blindness"*. P3 says
the **routing row already has that shape** with respect to *this* ticket. So the
routing row cannot simply be left alone (it fails) and cannot simply be deleted
(the concern it names — that a repair routing every row to `[CANNOT FAIL]`
would look attended to and cover nothing — becomes live exactly now).

What I intend instead: replace *"the row split separates"* with *"every scored
row has an EXHIBITED falsifying input"*, evaluated through the same predicate
the row itself is scored by. That points the right way — it goes red if a row
becomes unfalsifiable, and never because a row was honestly relabelled — and it
is strictly stronger than a count of rows routed each way. The row-grain count
(4 of 4 forced) becomes a printed measurement.

I also predict I will need a **green-on-real + red-on-planted** pair for it: a
probe satisfied by the good input alone is unfalsifiable, which is the defect
mg-e331 recorded as its own D3.

## What I expect to say I did NOT do

- Not re-derive mg-8af0's `>= 3 facets` forcing (P9 checks it, does not repeat
  the 2424-build sweep).
- Not edit `STATE.md`, `docs/OneThird-Intrinsic-Face-Geometry-Probe.md`, or any
  frozen audit document.
- Not rescope the vacuity split into a scored row — that refusal stands and is
  not mine to overturn.
