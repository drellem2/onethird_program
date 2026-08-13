# mg-79ba — INDEPENDENT AUDIT of mg-17aa

**Subject.** `de86fee`, "THE DEFERRED HALF IS LANDED AND THE TREE ALREADY HELD
FOUR CONTROLS THAT GO RED WHEN IT IS" (mg-17aa), which extended NEGATIVE
CONTROL 4's `[CANNOT FAIL]` treatment from three I-rows to four.

**Ticket.** *"the CANNOT FAIL extension: check no added row goes RED when the
underlying blindness is FIXED — a control pointing that way is worse than
none."*

**Predictions** are in `PREDICTIONS.md`, committed at `412fb54` **before any
audit code existed**. Scoring is section 5.

---

## 1. THE HEADLINE QUESTION, ANSWERED — AND IT IS THE WRONG QUESTION

**No row mg-17aa added to `controls.py` goes red because the blindness is
fixed.** `a2_fixed_blindness.py` builds four fixed-blindness worlds — a
pipeline that SEES the corrupted `le_to_facet` on row I4's 25
`applied-but-unseen` posets — and runs the whole battery in each.

| world | what the newly-seen pairs look like | battery | mg-17aa rows red |
|---|---|---|---|
| FB-diag | move a diagonal entry | exit 0 | none |
| FB-mag | move an off-diagonal magnitude, diagonal intact | exit 0 | none |
| FB-sign | clear BOTH forced gates, still not absorbable | exit 0 | none |
| FB-gauge | clear both gates AND are absorbable | exit 1 | the falsifiability row |

FB-sign is the one the design is for: the routing correctly returns row I4 to a
**scored** absorbability decision, `absorb == 0` comes back into its condition
and is true, and nothing reddens. That is `forced = (blocked == app)` doing
exactly what its comment claims — *"a corruption that CAN be absorbed puts the
clause back with no edit"* — and it is a real property, not a stated one.

FB-gauge does redden, and the red points the **right** way: what reddens is the
section reporting that its own corruption is a gauge on those posets, which is
the question NEGATIVE CONTROL 4 exists to answer. That is not mg-e35b's shape.

**So on the brief as written, mg-17aa passes.** The finding is elsewhere, and
the brief's framing is what pointed away from it — see section 4.

## 2. F1 — THE `[CANNOT FAIL]` ROW ACQUIRED A CONJUNCT THAT CANNOT FAIL

`a1_cannot_fail.py`, 31 claims, 0 broken.

```
forced = (blocked == app)                  # per row
if forced:
    theorem_blocked += blocked
    theorem_app     += app
...
check("PROVEN PROPERTY, ...",
      theorem_absorb == 0 and theorem_blocked == theorem_app,
      cannot_fail=True)
```

Both sums range over exactly the rows on which `blocked == app` holds term by
term. `theorem_blocked == theorem_app` is an **identity**. This is read out of
the source by `ast` — one assignment to `forced`, comparing two bare names; one
increment each, adding exactly those names; both under one `if forced:` — so
there is no second route to disagree with.

**Why it is a finding and not a tidy-up.** The row prints, beside it:

> *"A FALSE theorem is still a failure: if some pair cleared both forced gates,
> or the predicate did report absorbable, this row FAILS"*

The first disjunct is false as printed, and A1.2 **runs the world it names**: a
pair that clears both forced gates leaves the battery **green at exit 0**. It
does not fail the row — the routing drops that mutation out of `forced_rows`,
so the row reports one corruption fewer. A row sentence that is not its
measurement, inside the instrument built to remove exactly that.

**It is a regression, not an inheritance.** A1.4 exhibits one input — a biting
pair with a shape mismatch — and runs it against both trees: the pinned
pre-mg-17aa `[CANNOT FAIL]` row goes **RED**, the shipped one stays **GREEN**.
`diag_moved` was counted after the shape guard, so such a pair was in `app` and
in neither diagonal bucket; `blocked` is asked *before* that guard, and that is
what closed the gap.

**And the change was right on the mathematics.** A shape mismatch really does
block absorbability, so counting it as blocked is correct and the old row's red
there was a false alarm. What is owed is not a scoring change — it is that the
row stop printing a falsification condition it no longer has, and that the
conjunct be classified the way mg-17aa's own `nc4_row_conjuncts` classifies
`rej == app` and `shape_ok == app` two screens away.

**What is left of the row.** Its other conjunct `theorem_absorb == 0` is *not*
forced: A1.3 exhibits the world that reddens it (one pair reported absorbable
while its gate violations stand). But read what that world is — two procedures
disagreeing, not a corruption behaving differently. `gate_violations` and
`absorbable_by_diagonal_twist` are both derived from `S.A.S = B`. The row's
remaining measured content is a **consistency check between two
implementations**. Worth having; not what the row says it is.

The deletion test (mg-5f9a's method, the one mg-17aa applies to `rej == app` in
its own V5) confirms it: the conjunct is load-bearing on **no world** built
here, including both of the two its own sentence names.

## 3. F2 — THE REPAIR OF F1 IS BLOCKED BY mg-17aa's OWN RE-AIMED CONTROL

`a3_repair_blocked.py`, 19 claims, 0 broken. **This is the finding with my
ticket's polarity, and it is in the material beyond the brief.**

mg-17aa re-aimed three instruments belonging to other tickets, and its own
`unverified` list says *"neither re-aim was reviewed by the tickets that own
those instruments"*. One is `face_geometry_landing_da45/verify_landing.py`
TARGET 3. mg-17aa's diagnosis of the old version is correct and is written into
the file: the three source literals it scored *froze the deferral*, so the
verifier necessarily went red the day the deferred item landed.

The replacement scores three more source literals — of the post-mg-17aa state.
One is

```python
check("... (`theorem_absorb == 0 and theorem_blocked == theorem_app`) ...",
      "theorem_absorb == 0 and theorem_blocked == theorem_app" in src)
```

a **verbatim freeze of the conjunct F1 shows is a tautology**. A3.1 applies
three different spellings of the minimal honest repair, on a staged tree.
Every time: the **battery stays green at exit 0** and `verify_landing.py`
**goes red at exit 1**, on that check.

A control that goes red the day its own ticket's defect is fixed is the shape
mg-e35b named, the shape mg-17aa found four instances of, and the shape mg-17aa
wrote a fifth instance of in the act of removing the fourth.

A second literal in the same target freezes `"forced = (blocked == app)"`, so
widening the routing to a **third** forced gate — the same kind of change
mg-17aa itself made when it widened one gate to two — breaks it too.

### smaller, and said to be smaller

* **A3.2** `d4_auditor_rerun.py` scores another audit's BROKEN count with exact
  equality against a literal, and mg-17aa moved the literal `4 -> 5` rather
  than the shape. Fixing one more of `e3_seams.py`'s flagged claims makes it 6
  and reddens the instrument. The shape is **inherited from mg-5f9a**, not
  introduced here; what mg-17aa did was keep it while writing a paragraph about
  why the same shape elsewhere was a defect. **Reported, not demonstrated** —
  turning it red needs an edit to a third ticket's frozen audit document.
* **A3.4** The `[CANNOT FAIL]` row prints `0 on shape` in every forced row, and
  that 0 is forced by the same argument the file uses two screens away to class
  `shape_ok == app` as FORCED BY CONSTRUCTION. It is not named as forced where
  it is printed. This is the smallest item in the suite.

## 4. CORRECTING MY OWN TICKET'S FRAMING

My brief asks whether an added row goes **RED when the blindness is FIXED**.
That framing inherits mg-e35b's warning about one row shape, and it aimed me at
`controls.py`'s battery, where A2 finds nothing. Two corrections:

1. **The polarity was wrong for the battery.** A generation hunting
   wrong-direction rows misses the row that **cannot go red at all**. F1 is
   that row, it is in mg-17aa's own new code, and no amount of red-on-
   improvement testing would have found it.
2. **The polarity was right for the material beyond the brief.** F2 is exactly
   a red-on-improvement control — it is just not in the file the brief points
   at. Every generation in this arc has put its worst finding in what a commit
   added past what it was asked for, and this one did too.

I filed this correction in `PREDICTIONS.md` §1 before opening the instruments.

## 5. SCORING THE PRE-REGISTRATION

| bet | filed | outcome |
|---|---|---|
| **P1** 0.85 the `[CANNOT FAIL]` row has a tautological conjunct | live (discounted: ranges over source I had read) | **HIT**, `ast` + deletion test |
| **P2** 0.80 its printed falsification condition is unreachable | live | **HIT**, run: exit 0 on the world it names |
| **P3** 0.70 the conjunct it replaced was contingent | live | **HIT**, one input, two trees |
| **P4** 0.55 a red appears in mg-17aa's *own instrument* | live | **MISS on the file I named** — the red is in the *foreign* instrument it re-aimed (F2), not in `verify_17aa.py` |
| **P5** 0.60 the gated battery survives the benign fix | live | **HIT**, 3 of 4 worlds exit 0 |
| **P6** 0.50 an adverse branch exists and is unnamed | live | **HIT on existence, and my own gloss was wrong**: I called it possibly wrong-direction; it is not — see §1 |
| **P7** 0.65 one foreign re-aim is a re-frozen literal | live | **HIT, and larger than predicted** — it blocks the repair of F1 specifically |
| **P8** 0.45 `e3_seams.py` named in the subject, absent from the diff | live | **MISS.** The transcript IS stale, but it was already stale at mg-d0e2's own commit, the artifact has moved 7 times since, and mg-17aa states its policy in terms. My bet guessed at an edit never made or a concealment that did not happen. |
| **P9** 0.40 a printed count that cannot move | live | **HIT**, and it is the smallest thing here |
| **P10** 0.35 at least one of P1–P9 is wrong | live | **HIT** — two are (P4, P8) |

Seven of nine live bets hit. **That is weaker than it looks and the reason is
specific:** P1, P2 and P3 are one finding read three ways, and I had read the
whole of `controls.py`'s diff before filing them, which `PREDICTIONS.md` §0
discloses. The bets I could not have derived from reading are P5, P6 and P7,
and one of those (P6) I got right for the wrong reason.

## 6. WHAT I DID NOT DO

* **This suite is NOT added to `build.sh`, deliberately.** `a1` and `a3` score
  claims of the form *"this goes RED"*, so their green depends on the defects
  they report **staying present**. A gate whose pass condition is "the defect I
  found is still there" is the wrong-direction shape this entire ticket is
  about — it would redden the day F1 or F2 is repaired. Shipping it inside an
  audit of that defect class would be the ninth consecutive generation to
  reproduce its own subject. The suite is run by hand, its transcripts are
  committed, and `run_all.sh` says this at the top.
* **Nothing in `code/face_geometry/` or any other ticket's directory is
  edited.** No repair is landed. F1 and F2 are reported with an exhibited
  repair (three spellings, all shown to leave the battery green) and left for
  the ticket that owns the file. The one-line prose change F1 asks for is a
  scoring-adjacent edit to a gated file and is not mine to make in an audit.
* **The mathematics is not re-derived.** I take no position on the two forced
  gates, on `DIAGONAL_MOVES`/`MAGNITUDE_MOVES` as closed forms, or on
  mg-17aa's n = 6 result (1201/1201). All three were filed in advance as
  things I did not expect to establish.
* **The fixed pipeline is SIMULATED, not built.** A2's four worlds patch
  `claim1_pair` so that `L^rel` differs on the blind posets. Whether claim (1)
  admits an invariant that separates them is a mathematical question this audit
  does not answer. The worlds say what the section *does* when its counters
  move that way; they do not say the mathematics permits it.
* **A fifth world was built and dropped, with the reason recorded** in
  `a2_fixed_blindness.py`: a fixed pipeline returning a smaller square `L^rel`
  does not redden anything, it **crashes** `controls.py` at
  `code/face_geometry/controls.py:1478`, which indexes `A[i][j]` over
  `range(len(L_true))`. That line predates mg-17aa (it is verbatim in the
  pinned pre-mg-17aa blob), is unreachable by any shipped corruption, and is
  not a model of *this* blindness. Reported, not fixed, not counted against
  mg-17aa.
* **`verify_17aa.py` and `demo_wrong_way.py` were not re-run against the
  fixed-blindness worlds.** P4 predicted a stale frozen literal there and I did
  not chase it once F2 turned out to be the real instance of that shape. It
  remains unexamined and I am not asserting it is clean.
* **A3.2 is structural only.** I did not turn `d4_auditor_rerun.py` red.

## 7. MY OWN DEFECT, KEPT

**A2.0 is in the transcript and is mine.** My first fixed-blindness injection
patched `L_mut` inside the sweep and nowhere else. `negative_control_incidence`
computes its five counters **twice** — once in that loop and once through
`nc4_row_stats`, the second route mg-17aa added — so the patch moved one route
and not the other. That is not a fixed pipeline, it is a corrupted instrument,
and for as long as it took me to notice I had a run in which mg-17aa's
falsifiability row went red in *all four* worlds and a finding written up
saying so.

**What caught it was mg-17aa's own agreement check.** That row requires
`nc4_row_stats` to reproduce the sweep's counters on the real input before any
exhibit is believed, and mg-17aa's docstring gives the reason: *"two procedures
computing one quantity is how this lineage got a gate name that was not the
code's"*. It is kept in the suite as a scored section rather than deleted,
because a control that fires on a live example is better evidence for that
control than any of my prose about it — and because an auditor who reports the
defect and hides the near-miss is running the same file-drawer that produced
the defects it audits.

## 8. FILES

| file | what it is |
|---|---|
| `PREDICTIONS.md` | pre-registration, committed at `412fb54` before any code |
| `kern79ba.py` | sandbox + source injector; no number the tree also computes |
| `a1_cannot_fail.py` | F1 — `ast` identity, the run, the deletion test, the regression |
| `a2_fixed_blindness.py` | the ticket's question — four worlds, plus my own kept defect |
| `a3_repair_blocked.py` | F2 — the repair blocked, three spellings; and P8/P9 |
| `out_*.txt` | transcripts, byte-current with `run_all.sh` at the committing tree |
| `run_all.sh` | runs all three; **not** in `build.sh`, for the reason in §6 |
