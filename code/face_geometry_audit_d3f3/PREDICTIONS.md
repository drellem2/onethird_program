# mg-d3f3 — predictions, committed BEFORE any audit script exists

Independent audit of **mg-8af0**, pre-filed as a SAME ACTION alongside it. The brief:

> verify F2 was fixed BEFORE F1 — if the verifier still scores against a string literal,
> the mechanism that hid the defect is intact whatever happened to the count

and, from the 2026-08-05 21:00 addendum, the primary target is **the parent's own
volunteered disclosure**:

> "V6b WOULD NOT HAVE CAUGHT F1. Substituting a different expression into an existing
>  %d moves no specifier. The census closes the NEXT count, not this one."

Nothing below has been run in this worktree. `verify_e35b.py`, `controls.py`,
`demo_f2_row_can_go_red.py`, `probe_f1_count_moves.py`, `PREDICTIONS.md` (mg-8af0's) and
`README.md` (mg-8af0's) have been **read**, and `git log`/`git show --stat` have been run.
No interpreter has been started against any of them. Misses are kept as written.

---

## R0 — REPORTS, at zero credit, because I read them before predicting

These are not bets. They are things I already know from reading, written down here so that
they cannot later be presented as findings.

- **R0.1** The four commit hashes the addendum names (`41bdbfa`, `903a2e9`, `a8d1723`,
  `12a1553`) are **not on main**. The rebased equivalents are `c420303`, `0c3a2ba`,
  `534c06b`, `66130f8`, plus `2657490`. This is a refinery rebase, not work loss.
- **R0.2** `verify_e35b.py` has moved since mg-8af0 landed: **mg-843d** (`d7208fc`) added
  **V6d REACH** and re-declared the census **184 → 210**, and **mg-36f5** (`7025d03`)
  ported `probe_f3_tightness.py`. mg-8af0's README on main carries block-quoted
  annotations from both. So "the deliverable" has two datings and I will keep them apart.
- **R0.3** `controls_output.txt` is the output of **ten** sections of `controls.py`, not of
  `negative_control_incidence` alone (`main()` calls `scoring_self_test`,
  `positive_control_homology`, `negative_control_signs`, three more positive controls,
  `negative_control_identity`, `negative_control_construction`,
  `negative_control_incidence`, `artifact_banner_check`).
- **R0.4** `probe_f1_count_moves.py` does not open `controls.py`. It rebuilds the measured
  numerator from `top_laplacians` and **transcribes** the tautology as `len(ps)`.

---

## The populations and grains, once, for everything below

- **ROWS** — the scored `check(...)` calls in `code/face_geometry_repair_e35b/verify_e35b.py`.
  Grain: one check. Today's count is 29.
- **CENSUS** — the `%`-format conversion specifiers lexically inside
  `negative_control_incidence`. Grain: one specifier. This is mg-8af0's own population and
  I do not redefine it.
- **ART** — the bytes of `code/face_geometry/controls_output.txt`.
- **F1-SHAPED** — a source edit that changes *which expression* is substituted into an
  existing conversion specifier **and leaves ART byte-identical**. This is the definition
  the parent's own E1 forces: F1's repair changed no digit, so F1's *return* changes no
  digit either.

---

## P1 — THE FRAMING CORRECTION I OWE THE TICKET (my principal live bet)

The addendum instructs:

> "V6a is the row that must catch an F1-shaped defect. CONSTRUCT ONE and confirm V6a goes
>  red."

**I predict that instruction rests on a false premise and that V6a cannot go red on an
F1-shaped defect, by construction.** V6a is `anchor in artifact` over 12 literal strings.
An F1-shaped defect leaves ART byte-identical (that is what E1 measured). A substring test
on unchanged bytes cannot move.

- **P1a** (0.90) — Reverting the F1 repair at the source (`% (site_rows[3][1], N, …)` →
  `% (N, N, …)` at `controls.py:2261`) leaves ART **byte-identical**.
- **P1b** (0.88) — Under that revert, **V6a, V6b, V6c and V6d are all GREEN**, and so is
  **V7**, and `verify_e35b.py` exits **0** with **29 checks, 0 refuted**.
- **P1c** (0.92) — Under that revert, `probe_f1_count_moves.py` also exits **0** and prints
  the same six cells, because of R0.4 — it never reads the file it is vouching for.
- **P1d** (0.90) — Therefore the number of artefacts in this repair that go red when F1 is
  reintroduced is **0**, and the count of ROWS that do is **0**.

**What that does and does not mean.** It does *not* mean the repair failed: the repair's
job was to make the printed number a measurement, and it is one. It means the *guard* on
that repair is prose, not a row — and the brief's framing ("V6a is the row that must catch
it") names a row that cannot.

## P2 — IS THE DISCLOSURE COMPLETE?

The limit is declared in four places (V6b's row name, the demonstration's NOT-SHOWN line,
mg-8af0's PREDICTIONS E12, and the README's "did NOT do" list).

- **P2a** (0.85) — **All four name only V6b.** None of the four says that V6a, V6c, V6d and
  V7 share the limit, and none states P1d's count. The disclosure understates the gap by
  naming one row of five.
- **P2b** (0.80) — The README's line *"That is why F1 needed V7 and not just a census"*
  is the site where the understatement becomes a positive claim: it offers V7 as the
  remedy for exactly the gap V7 does not close. I predict V7's own row text hedges this
  correctly ("What this row CANNOT do is tell whether 86/86 is the right answer for the
  right reason") — so the file is honest and **the README is the site that is not**.
- **P2c** (0.55, low confidence, stated because I want it scored either way) — there is no
  source-level (`ast`) check anywhere in the repair that the F1 site's `%`-expression does
  not repeat an operand, even though `V4a` establishes the pattern of doing exactly that
  kind of check for exactly this kind of claim.

## P3 — IS "TRIPWIRE" THE HONEST WORD? What V6b catches and does not

V6b's row name asserts: *"NEGATIVE CONTROL 4 prints 210 formatted values and **no count
has been added or removed** since this table was written."* I predict the name is not the
measurement, in two separate directions, and that "TRIPWIRE" excuses neither because both
are inside the population the row claims.

- **P3a** (0.85) — **ADD-AND-REMOVE.** A source edit that deletes one `%d` site inside
  `negative_control_incidence` and adds a different `%d` site inside it leaves
  `CENSUS_DECLARED`'s seven-field dict **identical** → **V6b GREEN**; ART regenerates so
  **V6c GREEN**; the twelve anchors survive so **V6a GREEN**; and `printed` stays 194 so
  **V6d GREEN**. A count *was* added and one *was* removed, and the row that says so is
  green.
- **P3b** (0.92) — **OUT-OF-POPULATION.** A printed count added to
  `negative_control_construction` (a sibling section whose output is in ART, R0.3) moves
  **none of V6a/V6b/V6c/V6d**. The docstring's claim for V6c — *"a count cannot be added to
  the artifact without moving V6b"* — is **false** under this input, as is the file
  docstring's *"RED when a count is added or removed at the source."*
- **P3c** (0.70) — This is the arc's most-repeated defect (**a row name that is not its
  measurement**) reproduced **inside the instrument built to repair a row name that was not
  its measurement**. I am predicting the instrument's own defect class in advance because
  eight consecutive generations have had it and I have no reason to be the ninth exception.
- **P3d** (0.75) — "TRIPWIRE" *is* the honest word for the row's **mechanism** and is
  **not** an honest summary of its **scope**. The right repair is not to delete the word
  but to move the population into the name: *the specifier multiset of one function*.

## P4 — C4 IS RED FOR V6a ALONE: verify rather than accept

- **P4a** (0.85) — `demo_f2_row_can_go_red.py` run today exits **0**, 20/20 cells, matching
  `out_demo_f2.txt` byte for byte (mg-843d's block quote says it drifted away and back).
- **P4b** (0.90) — The claim "C4 is red for V6a alone" **reproduces**, so no replacement row
  is redundant.
- **P4c** (0.95) — **But C4 is not F1-shaped.** C4 drops backticks *in the printed string*,
  so ART changes. It separates V6a from V6b/V6c; it does not show V6a catching the defect
  class the addendum wants it to catch. The demonstration's five constructions contain **no
  F1-shaped input at all** — which is consistent with its own NOT-SHOWN line and is the
  reason that line exists.
- **P4d** (0.60) — The demonstration scores **three** rows (V6a/V6b/V6c). V6d, added by
  mg-843d, has its own five-construction demo; I predict `demo_f2_row_can_go_red.py` was
  **not** extended to a fourth column, so the 20-cell matrix is 5×4 counting the old row,
  not 5 constructions × 4 replacement rows.

## P5 — ARE THE ROWS REALLY SCORED AGAINST SOMETHING OUTSIDE THE FILE?

- **P5a** (0.85) — **Yes, all four.** V6a's measured side is ART; V6b's is `controls.py`'s
  source text; V6c's is a subprocess run; V6d's is an instrumented run. In every case the
  in-file literal is the *declared* side and the *measured* side comes from outside. **F2
  has not been reintroduced literally.**
- **P5b** (0.70) — The one place a number is still read from a literal and printed as
  though measured is the **V6 heading line**, which prints `CENSUS_DECLARED["specifiers"]`
  and `CENSUS_REACH_DECLARED["printed"]`. I predict the file **says so** in a comment
  (a quoted declaration, deliberately), so this is disclosed and not a defect.
- **P5c** (0.80) — `forced` is computed from `TABLE` and **printed**, and the line says
  "PRINTED, NOT SCORED". I predict that is accurate: nothing scores `forced`.

## P6 — CAVEATS CHECKED AGAINST THEIR HYPOTHESIS (E6a and the tripwire)

The addendum says E6a's 2.2× size miss and V6b's tripwire limitation "are the same fact and
should agree". The README says: *"with 184 sites and 12 table entries there is no per-count
mapping available, so V6b **cannot** be a coverage check and is scored as a tripwire."*

- **P6a** (0.80) — **They do not agree, and the README's causal claim is false.** mg-8af0's
  own E6a *already derived* "no per-row mapping is available and the census must be
  reported at its own grain" from **SITES > 11** — before any measurement, at the predicted
  85. The magnitude of the miss changes nothing about the conclusion: 85 > 11 and 184 > 11
  give the same verdict. So the miss is **not** "the reason" V6b is a tripwire; the reason
  was in the prediction that missed.
- **P6b** (0.70) — What the miss *does* bear on is different and is not claimed: at 85 the
  band 55–120 would have held, so the miss is evidence about **reading a function by eye**,
  not about census design. I predict the README does not say this.

## P7 — ORDER, AND THE TWO KEPT MISSES

- **P7a** (0.95) — `git log --reverse` on main shows F2 (`0c3a2ba`) strictly before F1
  (`534c06b`), and the **F2 commit touches no file under `code/face_geometry/`** — so the
  count was still a tautology when the verifier was repaired. Order held.
- **P7b** (0.90) — At the F2 commit the verifier **exits 1** on the real tree with exactly
  **one** refuted row, and I predict that row is the one keyed on the F1 site — i.e. the
  repair was *watched failing on the defect it had not yet fixed*.
- **P7c** (0.95) — E9's second clause is **false as recorded**: `534c06b` changes
  `verify_e35b.py` (+32 lines). The README scores it HALF-MISS. Confirmed.

## P8 — WHAT WAS DELIBERATELY NOT DONE: in scope or quietly dropped?

For each, I predict **genuinely out of scope**:

- **P8a** (0.85) — mg-fcb2's **F4** is not assigned in mg-8af0's brief (which names F1/F2/F3
  only). Out of scope.
- **P8b** (0.85) — **STATE.md** untouched by all of mg-8af0's commits, matching the choice
  mg-2789 and mg-e35b made at the same site. Out of scope.
- **P8c** (0.90) — **n > 6** genuinely not swept, and the README says so under "Not shown".
- **P8d** (0.90) — mg-fcb2's **A1.4a** scores `worst >= 3`, a claim about the *mathematics*
  and not about the artifact's wording, so it correctly stays `[REFUTED]`.

## P9 — MATERIAL BEYOND THE BRIEF (the standing target)

mg-8af0's own **E11** predicted that this audit would find "at least one printed count in
code this repair adds that this repair does not classify."

- **P9a** (0.95) — **E11 is a HIT for the parent, comfortably.** The three scripts mg-8af0
  adds print counts of their own (the 20-cell matrix, the 6-cell table, the multiplicity
  sweep), none of which is in `TABLE` and none of which any census covers. Because the
  parent called it in advance, I score it as **called, not discovered**, and it is not the
  audit's headline.
- **P9b** (0.50) — The genuinely-beyond-the-brief material with the worst finding in it is
  **not** the probes but the **README's "Predictions, scored" table** — prose the brief did
  not ask for, carrying P6a's false causal claim.

## P10 — AGAINST MYSELF

- **P10a** — My audit will print counts. I commit in advance to classifying every one and
  labelling the FORCED ones. I predict **at least two** of my own printed counts are FORCED,
  and I name one now: *"the number of rows that go red when F1 is reintroduced"* is **0**
  and is forced the moment P1a holds, because a byte-identical artifact cannot move an
  artifact-scored row. It is FORCED and I will print it as FORCED.
- **P10b** — My own headline (P1) is a **negative**, and a negative requires its candidate
  space. The space is *every scored artefact in the repair*: 29 verifier rows + 5 demo
  constructions + probe_f1 + probe_f3. I will enumerate it rather than assert it.
- **P10c** (0.35) — I predict at least one of P1a/P3a/P3b comes out **wrong**, because the
  parent's file is more careful than my reading of it, and I would rather record that
  expectation than a clean sweep.

---

## What I intend NOT to do, stated in advance

- I will **not** repair anything in `code/face_geometry/` or
  `code/face_geometry_repair_e35b/`. This is an audit; its output is a record.
- I will **not** re-audit mg-e35b's mathematics (the dichotomy, the gauge splits, the
  vacuity separation). mg-fcb2 and mg-8af0 both did; a third pass is not this brief.
- I will **not** re-run the n ≤ 6 multiplicity sweep or extend it to n > 6.
- I will **not** edit any frozen transcript of mg-8af0, mg-fcb2 or mg-e35b, and I will not
  regenerate `out_demo_f2.txt` or `out_verify_e35b.txt`. If they disagree with the tree I
  will say so and leave them.
