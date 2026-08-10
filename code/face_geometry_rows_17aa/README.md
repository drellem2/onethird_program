# mg-17aa — the `[CANNOT FAIL]` treatment extended to all four I-rows

mg-e35b landed the `[CANNOT FAIL]` row for three of NEGATIVE CONTROL 4's four
incidence corruptions and recorded the fourth as its own item, in its own words:

> "Row I4's scored condition is NOT rescoped -- `absorb == 0` stays in it. The
> rejections are real on all 297 pairs; what the gauge finding narrows is what a
> rejection is EVIDENCE FOR. Extending `[CANNOT FAIL]` to all four is still its
> own item."

That was a correct refusal. This is the item.

## The answer, per row, in one table

For each row: can its scored condition fail, and on what input? The unit of the
question is the **conjunct**, not the row — and getting that wrong is why this
file deferred the same item four times (see *Why it took four goes* below).

| row | conjunct | class | can it fail? on what input |
|---|---|---|---|
| I1 I2 I3 I4 | `app > 0` | **CONTINGENT** | yes — the mutation replaced by a no-op reaches L^rel on 0 posets. Exhibited and run inside the battery. |
| I1 I2 I3 | `caused == app` | **CONTINGENT** | yes — the residual checked against a prediction made from a *different* corrupted site. Exhibited and run. |
| I1 I2 I3 I4 | `rej == app` | FORCED **given a scored row** | only together with the baseline row. `app` counts `L_mut != L_true`; the baseline scores `L_true == target` on the whole population; `L_mut != target` follows. |
| I1 I2 I3 I4 | `shape_ok == app` | FORCED **by construction** | no — both matrices are `|L(P)| x |L(P)|` and no `incidence_mode` changes the facet count, at any n. |
| I4 | ~~`absorb == 0`~~ | FORCED **by the mutation** | **no — and this is what the ticket is about.** Removed from the row and stated in the `[CANNOT FAIL]` row, where it is still verified. |

**So no I-row is itself a `[CANNOT FAIL]` row** — each can fail on `app > 0`,
and three more on `caused == app`. What is a `[CANNOT FAIL]` fact is one
*clause* of one row, and it is now out of all four. **I4 has ONE contingent
conjunct where the others have two**: the row that was kept scored *because* its
absorbability answer was supposedly a decision is the row with the least
measured content of the four.

## What was actually missing: a second theorem, not a scoring decision

mg-8a12 routed on `diagonal_moves` — the hypothesis of the predicate's first
forced gate, `s_i^2 = 1`. **That hypothesis is FALSE on 3 of row I4's 61 biting
posets.** They are the antichains, where the off-by-one is a bare relabelling of
`L(P) = S_n` and the diagonal survives. So the argument the other three rows were
routed on genuinely does not cover the fourth, and no amount of re-scoring would
have supplied it.

The predicate has a **second** gate forced by the same arithmetic: `|s_i s_j| = 1`
pins every absolute value, so a corruption moving one cannot be absorbed either.
The routing quantity is now *"is every biting pair blocked by a forced gate"*,
asked of each pair by `gate_violations`:

| row | biting | blocked on the diagonal | blocked on a magnitude, diagonal intact | absorbable |
|---|---|---|---|---|
| I1 | 72 | 72 | 0 | 0 |
| I2 | 82 | 82 | 0 | 0 |
| I3 | 82 | 82 | 0 | 0 |
| **I4** | 61 | 58 | **3** | 0 |
| total | 297 | 294 | 3 | 0 |

`verify_17aa.py` re-derives every one of those 297 by **exhibiting the blocking
entry** `(i, j)` and checking it against both values of `s_i s_j` — a
certificate, not a predicate's answer — and cross-checks against
`absorbable_bruteforce` (the definition enumerated over all `2^m` sign vectors,
sharing no line with either) on the 185 pairs with `|L(P)| <= 10`. **It holds at
n = 6 too**: 1201/1201 blocked, 0 absorbable, the magnitude gate needed on the
one antichain — so this is a theorem and not a property of 86 posets. n = 7 is
not swept and the reason is size: `|L(P)|` reaches 5040 there.

## The trap the ticket warned about — and the four instruments already in it

mg-e35b declined to score the I4 vacuity split because *"a row scoring 'the
split separates' would go RED the day somebody FIXED the blindness — the wrong
direction for a control to point."* This ticket was told not to build a row of
that shape.

**It did not have to build one. The section already had one, one screen above
that sentence, pointing straight at the item mg-e35b was deferring** — and three
more instruments downstream did too. Every one of them goes red *because the
tree got better*:

| # | instrument | what it asserted | why landing the deferred item breaks it |
|---|---|---|---|
| 1 | `controls.py`'s routing row | `0 < len(forced_rows) < len(muts)` | `0 < 4 < 4` once every row is correctly labelled. Nothing about the mathematics moved. |
| 2 | `d3_reintroduction.py` R1 | injects the dead premise into row I4's `else` branch | that branch is now unreachable, so the mutation applies to the source and never reaches the artifact — an instrument reporting failure because the injection got harder |
| 3 | `verify_landing.py` TARGET 3 | three source literals: *the clause is still scored, the routing is still on the diagonal gate, the routing row's condition is untouched* | it froze the deferral itself |
| 4 | `e3_seams.py` (mg-d0e2) | *"that verifier's closing prose STILL reads 'the file now MEASURES which gate settled it'"* — a framing mg-1c80 refuted | mg-17aa replaced that prose, so an **audit record goes red the day its own finding is acted on** |

`demo_wrong_way.py` runs #1 rather than arguing it: it takes the pre-mg-17aa
`controls.py` **pinned by blob sha** (`da160f68…`, not by `main`, which moves —
mg-f8e5's `c1_rebase.py:48` is the worked example of a probe that quietly
re-aimed itself), applies the smallest edit that extends the treatment to all
four rows (`diag_preserved == 0` → `>= 0`), and runs the battery. **Two rows go
red and they are not the same kind of red**, which is the finding:

- the `[CANNOT FAIL]` row — a **real** failure. Its condition asserts the
  diagonal moves on every biting pair of every forced row, and I4's does not.
  The single-gate argument is genuinely too narrow.
- the routing row — a **wrong-direction** failure. The row set stopped
  separating because every row became correctly labelled.

### What replaces the routing row, and why it points the right way

A count of rows routed each way never showed that anything could fail: it is
satisfied by a section with one un-routed row whose condition is a tautology, and
refuted by a section in which every forced clause has been honestly removed.
What is scored instead is **an exhibited input per row on which that row's
remaining condition is FALSE**, run through the same conjunct predicates the row
is scored by — so no exhibit can falsify a replica. It is a **green-on-real +
red-on-planted** pair, because a probe satisfied by the good input alone is
unfalsifiable (mg-e331's own D4). It goes red when a row becomes unfalsifiable
and never when one is honestly relabelled. The row-grain count (4 of 4 forced)
is now a printed measurement.

**The weak half, stated:** the exhibits are computed by `nc4_row_stats`, a
*second* route to the same five counters, and two procedures for one quantity is
how this lineage got a gate name that was not the code's (mg-1c80 F1). So that
route is required to reproduce the main sweep's counters on the real input
first, and the row goes red if the two drift.

## Why it took four goes, which is the part worth keeping

`mg-8a12 → mg-da45 → mg-5f9a → mg-e35b` each named this deferral and each left
it. The clause survived because *"can row I4 fail?"* has an honest answer — **yes,
on `app > 0`** — however forced its absorbability clause is. So a row-level
reading kept returning the right answer to the wrong question, and the forced
clause kept its `[PASS]` under a battery whose own SCORING section forbids
exactly that. **A forced conjunct in a scored condition is the defect whatever
the rest of the condition does.**

`rej == app` and `shape_ok == app` are **kept**, not deleted, and named for what
they are. A conjunct that can only fail alongside a scored row is redundant, not
unfalsifiable, and quietly deleting true checks to tidy a table is a different
and worse change than the one this ticket makes. The deletion test in V5
measures it: neither is load-bearing on any world in any row.

## The ticket's own input premise is false, and was already false when it was written

The ticket says to take as input that three of the four `>= 3 facets` zeros are
FORCED and *"only I4's is a result"*, and to check it. **It is false.** mg-8af0
landed the correction on 2026-08-05 — one day after this ticket was filed — and
mg-e35b's README carries the struck-through text. V4 checks that rather than
re-running mg-8af0's 2424-build sweep, and names the commit (`66130f8`).

**And the two questions are independent**, which is why mg-8af0's finding
corrects the premise without answering the ticket: NEGATIVE CONTROL 3's parity
corruption raises no ridge's facet count *and* is absorbable on 82/82 of the
posets where it bites. *"No ridge in ≥ 3 facets"* does not imply *"not
absorbable"*.

## Predictions, scored

Registered in `PREDICTIONS.md` before any script of this ticket existed.

| # | p | outcome |
|---|---|---|
| P1 | 0.90 | **HIT** — 297/297 blocked by an exhibited certificate, 0 absorbable |
| P2 | 0.85 | **HIT** — 58 + 3 for I4; neither gate alone covers the four |
| P3 | 0.80 | **HIT, and larger than predicted** — the routing row does go red, and so does the `[CANNOT FAIL]` row. I predicted one wrong-direction control; there are four, and one of them is an audit record |
| P4 | 0.75 | **HIT** — deleting `rej == app` moves no verdict on any world |
| P5 | 0.70 | **HIT** — same for `shape_ok == app` |
| P6 | 0.60 | **HIT** — I4 has one contingent conjunct, I1/I2/I3 have two |
| P7 | 0.65 | **HIT** — 4 of 4 rows red on a no-op world, 3 of 3 also red on a mis-predicted residual |
| P8 | 0.50 | **HIT** — NC3's corruption separates the two questions |
| P9 | — | report, not a bet: confirmed |

None of the three named conditions for **not** making the change was met.

## Defects of my own, kept

- **D1 — a probe that reported HOLDS because it could not read what it was asked
  about, inside a ticket about clauses that cannot fail.** V2's antichain arm
  read `P.relations` under a `hasattr` guard falling back to `True`. `Poset` has
  `__slots__ = ("n", "less", "name")`, so the attribute does not exist, the
  guard was `False` on every element and the `all(...)` was **vacuously true**.
  It reads `P.less` now and requires a non-empty population, so *"no pairs to
  check"* can never read as *"checked"*. Same shape as mg-a0d6's D2.
- **D2 — I broke `verify_landing.py`'s third check and it passed anyway, for the
  wrong reason.** It looks for the literal `0 < len(forced_rows) < len(muts)`,
  and my replacement row's *comment* quotes that string while explaining why it
  was removed — so a check on the deferral's presence was satisfied by a
  quotation of the deferral. It is re-aimed now, but the false green was mine
  and it was live for an hour.
- **D3 — I truncated three of another audit's committed transcripts** by running
  `g2`/`g3`/`g4` inside a two-minute budget that killed `g4` mid-run, and the
  partial files sat in the worktree as 284 deleted lines. Restored from `HEAD`;
  those three are not regenerated by this ticket and were not by mg-e35b either.
- **D4 — my first `run_all.sh` quoted a runtime I had not measured** (20.7 s
  against a real 13.6 s). Caught re-reading my own file, corrected to measured
  figures, and `code/face_geometry/run_all.sh`'s 19.4 s is re-measured here too
  rather than carried forward — the same discipline mg-a71f's D-list records
  paying for in the other direction.
- **D5 — the exhibit route is a second procedure computing the same five
  counters.** That is the defect shape this lineage has been caught by twice. It
  is mitigated by a scored agreement requirement, not removed.

## What this ticket deliberately did NOT do

- **Score the I4 vacuity split.** mg-e35b's refusal stands and is not mine to
  overturn. The split is still printed and still unscored.
- **Delete `rej == app` or `shape_ok == app`** from any row. They are forced, and
  they are named as forced, and they stay.
- **Re-derive mg-8af0's `>= 3 facets` forcing.** V4 checks the correction is in
  the tree and names the commit; it does not repeat the 2424-build sweep.
- **Edit any frozen audit document.** `e3_seams.py` gained a fifth BROKEN claim
  under this tree and is **not** edited — `d4_auditor_rerun.py`'s expectation
  moved 4 → 5 with the reason written in, which is the treatment mg-e35b used
  when it moved the same expectation 2 → 4.
- **Edit `STATE.md`** or `docs/OneThird-Intrinsic-Face-Geometry-Probe.md`. The
  four-of-four routing and the 58 + 3 split are numbers for pm-onethird's
  ledger and are routed to them, the same choice mg-e35b and mg-2789 made.
- **Sweep n = 7.** `|L(P)|` reaches 5040 and `L^rel` is `|L(P)| x |L(P)|`. The
  forcing is stated as checked to n = 6 and argued (not measured) above it.
- **Re-open the gauge dichotomy, the coverage sizing, or `absorb_trace` itself.**

## State of the runners after this commit

| runner | before | after |
|---|---|---|
| `face_geometry/run_all.sh` | exit 0 | exit 0 |
| `face_geometry_rows_17aa/run_all.sh` | — | exit 0, 37 claims, 0 BROKEN |
| `face_geometry_landing_da45/run_all.sh` | exit 0 | exit 0 |
| `face_geometry_landing_7d5a/run_all.sh` | exit 0 | exit 0 |
| `face_geometry_audit_6653/run_all.sh` | exit 0 | exit 0 |
| `face_geometry_instr_5f9a` d1 / d2 / d3 / d4 | 0 / 1 / 0 / 0 BROKEN | 0 / 1 / 0 / 0 BROKEN |
| `face_geometry_audit_e7bc/run_all.sh` | exit 1, 1 BROKEN | exit 1, 1 BROKEN |

`d2`'s one BROKEN claim is the pre-existing git-pin staleness its own
`run_all.sh` documents (*"d2 EXITS 1 AT HEAD AND HAS SINCE bfd7948"*). `e7bc`'s
is the frozen row-count literal 43 against an artifact carrying 45, which
`d4_auditor_rerun.py` already expects. Neither is caused or fixed here.

## Files

- `PREDICTIONS.md` — committed before any script of this ticket existed.
- `verify_17aa.py` — 27 claims. Certificates for all 297 pairs and again at
  n = 6; the two-gate tightness; the ticket's premise; the conjunct deletion
  test; the new row's own falsifiability; containment by allowlist-with-reasons
  rather than by directory prefix.
- `demo_wrong_way.py` — 10 claims. The pre-existing wrong-direction control,
  run rather than argued, against a blob-pinned pre-mg-17aa tree.
- `run_all.sh`, `out_verify_17aa.txt`, `out_demo_wrong_way.txt`.
