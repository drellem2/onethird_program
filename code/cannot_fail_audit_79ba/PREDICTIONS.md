# mg-79ba — PRE-REGISTERED PREDICTIONS

INDEPENDENT AUDIT of mg-17aa (`de86fee`, "THE DEFERRED HALF IS LANDED").

**Filed before one line of audit code exists.** Nothing in
`code/cannot_fail_audit_79ba/` other than this file is present in the commit
that carries it.

---

## 0. EXPOSURE, DISCLOSED RATHER THAN LAUNDERED

This repository's commit subjects carry conclusions. Before filing, I had read:

* `git show de86fee` — the whole subject line, which states its own findings,
  its own five kept defects (D1–D5), and its own unverified list;
* the complete diff of `code/face_geometry/controls.py` in `de86fee`;
* `code/face_geometry/controls_output.txt` rows I1–I4 and the measured block;
* `code/face_geometry/face_complex.py`'s `gate_violations` /
  `diagonal_moves`;
* `mg show mg-17aa`, `mg show mg-79ba`, and mg-17aa's result sidecar.

I had **not** read `verify_17aa.py`, `demo_wrong_way.py`,
`out_verify_17aa.txt`, `out_demo_wrong_way.txt`, the mg-17aa `README.md`, or
any of the three re-aimed foreign instruments
(`d3_reintroduction.py`, `d4_auditor_rerun.py`, `verify_landing.py`) at the
moment of filing. Bets that range over those files are live; bets that range
over `controls.py` are **discounted** and are marked so individually.

### REPORTS (zero credit — these are things I read, not things I bet)

* **R1** Row I4 is `localised=False`. Its scored condition is
  `app > 0 AND rej == app AND shape_ok == app`, plus `absorb == 0` only when
  the routing declines to call it forced. I1/I2/I3 additionally carry
  `caused == app`.
* **R2** On the shipped population (86 posets, n ≤ 5): I4 bites on 61, is
  vacuous on 25, and **all 25 are `blind`** — the mutation applied at the site
  and claim (1) still held. 24 of the 25 build a genuinely different facet
  SET, 14 of those with |L(P)| ≥ 3. I1/I2/I3 have `blind == 0`.
* **R3** mg-17aa widened the routing quantity from `diag_preserved == 0` to
  `blocked == app`, and replaced the row scoring `0 < len(forced_rows) <
  len(muts)` with a row scoring an exhibited falsifying input per row.
* **R4** `code/face_geometry_rows_17aa/run_all.sh` is **not** in `build.sh`'s
  suite list. `controls.py` is nevertheless reached by the gate, through
  `code/face_geometry_repair_e35b/run_all.sh` (its V6c RUNS controls.py).
  So a red in mg-17aa's own instrument does not block a merge; a red in
  `controls.py` does.

---

## 1. CORRECTING MY OWN TICKET'S FRAMING

My brief says: *"check no added row goes RED when the underlying blindness is
FIXED — a control pointing that way is worse than none"*.

That framing presumes the danger is **red-on-improvement**, and it inherits
that presumption from mg-e35b's warning, which was about a specific row shape
(`the split separates`) that mg-17aa demonstrably did not build. **I predict
the framing is aimed at the wrong polarity for this deliverable.** mg-17aa
was, by its own account, hunting wrong-direction rows; the thing a generation
that hunts wrong-direction rows misses is the opposite failure — a row that
**cannot go red at all**. That is P1, and it is my principal live bet.

If P1 is right, my ticket's headline question ("does an added row go red when
the blindness is fixed?") gets the answer **NO** — and the NO is not
reassurance, because the reason is that the row in question cannot go red for
any reason whatsoever.

---

## 2. LIVE BETS

### P1 — 0.85. THE [CANNOT FAIL] ROW ACQUIRED A CONJUNCT THAT CANNOT FAIL.
*(discounted: ranges over `controls.py`, which I have read. I have not run
anything, and I have not tried to build the input that refutes it.)*

`negative_control_incidence` sets, per row, `forced = (blocked == app)`, and
accumulates `theorem_blocked += blocked` / `theorem_app += app` **only inside
`if forced:`**. The [CANNOT FAIL] row then scores

```
theorem_absorb == 0 and theorem_blocked == theorem_app
```

Both sums range over exactly the rows for which `blocked == app` holds
term-by-term, so `theorem_blocked == theorem_app` is an identity. **No input
to this program can make that conjunct false.** I predict I cannot build one,
and that the artifact nowhere says FORCED of it.

That is the defect class mg-17aa was dispatched to repair — a forced conjunct
inside a scored condition — reproduced by mg-17aa in its own new code, in the
row literally named `[CANNOT FAIL]`, in the same commit that adds
`nc4_row_conjuncts` to classify exactly this.

### P2 — 0.80. THE ROW'S PRINTED FALSIFICATION CONDITION IS UNREACHABLE.

The row prints: *"A FALSE theorem is still a failure: if some pair cleared
both forced gates, or the predicate did report absorbable, this row FAILS"*.
I predict the first disjunct is **false as printed**: a pair clearing both
forced gates makes `blocked < app` for its row, which removes that row from
`forced_rows` and therefore from both sums — the row does not fail, it gets
*smaller*. A row name (and here, a row sentence) that is not its measurement.
I predict I can exhibit this by construction.

### P3 — 0.70. mg-17aa MADE THIS CONJUNCT WORSE, NOT NEUTRAL.

The pre-mg-17aa condition was `theorem_absorb == 0 and theorem_diag ==
theorem_app` under `forced = (diag_preserved == 0)`. `diag_moved` is
incremented **after** the shape guard `continue`, so a biting pair with a
shape mismatch is counted in `app` and in neither `diag_moved` nor
`diag_preserved`. I predict `theorem_diag == theorem_app` was therefore
**contingent** — falsifiable by a shape-mismatching biting pair — and that
mg-17aa's `blocked` (asked *before* the shape guard, deliberately, with a
comment saying why) converted a contingent conjunct into a tautology. If so,
the repair removed falsifiability from the row it was repairing.

### P4 — 0.55. THE LITERAL QUESTION, ANSWERED WHERE THE TICKET DID NOT LOOK.

I predict at least one row **does** go red under a fixed-blindness world, and
that it is in mg-17aa's own instrument (`verify_17aa.py` /
`demo_wrong_way.py`) rather than in `controls.py`'s gated battery — because
audit instruments freeze the counts they were written against. Named
candidates: `297`, `61`, `58`, `3`, `4 of 4 forced`.

### P5 — 0.60. THE GATED BATTERY ITSELF SURVIVES THE BENIGN FIX.

I predict that in the world where I4's 25 blind posets become biting and each
new pair violates a forced gate, **no row of `controls.py` goes red** — the
[CANNOT FAIL] row survives (trivially, per P1), row I4 survives, and the new
falsifiability row survives. i.e. on my ticket's headline question, and for
the rows that actually gate merges, mg-17aa **passes**.

### P6 — 0.50. THERE IS AN ADVERSE BRANCH AND mg-17aa DOES NOT NAME IT.

In the world where at least one newly-biting pair is absorbable, row I4 routes
back to scored, gains `absorb == 0`, and that conjunct is FALSE — row I4 goes
RED, and so does the new falsifiability row (`green` is false for I4, so
`ex_ok < 4`). I predict this branch exists, that it is reachable, and that
**neither mg-17aa's prose nor its instrument mentions the fixed-blindness
world at all**. Whether that red is "wrong-direction" is a judgement I will
argue in the finding rather than assert here: it is a control getting worse as
the pipeline gets better, but it is also a true report that the corruption is
a gauge on those posets.

### P7 — 0.65. MATERIAL BEYOND THE BRIEF: THE THREE FOREIGN RE-AIMS.

mg-17aa edited three other tickets' instruments —
`face_geometry_instr_5f9a/d3_reintroduction.py` (R1 anchor),
`face_geometry_instr_5f9a/d4_auditor_rerun.py` (EXPECTATION 4→5),
`face_geometry_landing_da45/verify_landing.py` (TARGET 3) — and its own
`unverified` list admits *"neither re-aim was reviewed by the tickets that own
those instruments"*. I predict at least one of the three is a **weakened
mutation or a re-frozen literal**: specifically that `verify_landing.py`
TARGET 3, re-scoped off the deferral it used to freeze, now freezes mg-17aa's
own post-state in the same way, so the next person to land the next deferred
half hits the identical wall.

### P8 — 0.45. e3_seams.py IS NAMED IN THE SUBJECT AND ABSENT FROM THE DIFF.

The subject says *"e3_seams.py gained a fifth BROKEN claim"*, but no path
under `code/face_geometry_audit_d0e2/` appears in `de86fee`'s 22-file stat. I
predict the committed `out_e3_seams.txt` on main disagrees with what a live
run produces — the exact shape mg-f771's invariant calls RED by construction —
or, failing that, that the subject line describes an edit that was never made.

### P9 — 0.40. A PRINTED COUNT THAT CANNOT MOVE.

The [CANNOT FAIL] row prints `theorem_blocked - theorem_bdiag - theorem_bmag`
as "%d on shape". `blocked_shape` counts pairs whose `gate_violations` is
exactly `{"shape"}`. I predict this is FORCED to 0 on the four shipped
corruptions (no `incidence_mode` changes the facet count — the file says so
itself, and uses that fact to classify `shape_ok == app` as FORCED BY
CONSTRUCTION), and that the artifact does **not** say FORCED of it while
saying FORCED of the sibling clause two screens away.

### P10 — 0.35. At least one of P1–P9 is wrong.

---

## 3. THINGS I DO NOT EXPECT TO ESTABLISH — stated in advance

1. I will **not** re-derive the n = 6 result (1201/1201 blocked, 0
   absorbable). It costs more than my slot has and I have no independent route
   to it.
2. I will **not** verify the closed forms in `DIAGONAL_MOVES` /
   `MAGNITUDE_MOVES` as mathematics. I will only check that the code's use of
   them matches what they say.
3. I will **not** decide whether "fixing the blindness" is mathematically
   possible for `le_to_facet_offbyone`. My worlds are counter-level and
   simulated; the fix itself is hypothetical, and I will say so.

## 4. CONDITIONS FOR REVERSING MY OWN VERDICT — filed in advance

* **P1 dies** if `forced` is computed from any quantity other than the one
  summed into `theorem_blocked`/`theorem_app`, or if a row can enter
  `forced_rows` with `blocked != app`. Either would make the conjunct
  contingent and I would report P1 as a miss.
* **P1 also dies** if the artifact already says FORCED (or equivalent) of
  `theorem_blocked == theorem_app` anywhere I have not read.
* **P4 dies** if `verify_17aa.py` already scores a fixed-blindness world.
* **My whole verdict reverses to "mg-17aa is clean on its brief"** if the
  fixed-blindness enumeration returns no red in `controls.py` *and* P1 turns
  out to be an identity that the artifact already names.
