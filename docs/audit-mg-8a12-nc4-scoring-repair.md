# INDEPENDENT AUDIT of mg-8a12 (commit 8fc5111) — the NEGATIVE CONTROL 4 scoring repair

**Auditor:** mg-f1b2 (pre-filed audit; no coordination with mg-8a12)
**Target:** `8fc5111` — "probe: repair NEGATIVE CONTROL 4's scoring — three of its four rows
were a THEOREM scored as passing controls, and the output said they were not (mg-8a12)"
**Files audited:** `code/face_geometry/controls.py`, `code/face_geometry/controls_output.txt`,
`code/face_geometry/face_complex.py`, `code/face_geometry/run_all.sh`, plus the commit's own
description of its method
**Audit code:** `code/face_geometry_audit_f1b2/` (`audit_scoring.py`, `audit_gates.py`,
`audit_theorem_and_content.py`, `audit_injections.py`, `audit_nmax2.py`; outputs
`out_scoring.txt`, `out_gates.txt`, `out_theorem.txt`, `out_injections.txt`, `out_nmax.txt`;
`run_audit.sh` regenerates all five). No audit script imports `controls.py`, so a defect in
the repair's own bookkeeping cannot hide inside my counts.

---

## VERDICT: **OVERSTATED**, and the defect it repairs is at a FIFTH generation — inside the repair

**0 BROKEN mathematics.** No statement about the face complex, the Laplacian, or the twist is
wrong. `controls_output.txt` regenerates byte-identically. Every committed count reproduces
from a rebuild that never calls `controls.py`. The demotion of I1/I2/I3 is **the right call,
correctly argued, and not an over-correction** — see WHAT STANDS.

**And the repair repeats the defect it repairs, twice.** mg-8a12 removed a forced condition
from three rows and added two new scored rows, one of which is forced and one of which keeps a
forced condition:

| row | scored condition | can it fail? |
|-----|-----------------|--------------|
| baseline (new) | claim (1) holds on the uncorrupted build, 86/86 | yes, but it is the **third** copy of that measurement in this one output |
| I1 / I2 / I3 | bites + rejection is caused by the corruption | **yes** — genuinely stronger than what was removed |
| **I4** | bites + `absorb == 0` | **NO.** `absorb == 0` is forced on all 61, by the predicate's *absolute-value* gate on exactly the 3 posets the row cites as its reason for scoring it |
| PROVEN PROPERTY (new) | correctly `[CANNOT FAIL]` | — |
| **routing check (new)** | `0 < len(forced_rows) < len(muts)` | **NO** — forced by two theorems this same commit states |

The mechanism is worth stating plainly because it is new: **mg-8a12 took the auditor's word
for the one fact that decides its routing.** The merge note says so —

> "mg-fcf1's instrument is untouched … its counts (I1/I2/I3 FORCED, I4 real work on 3) are
> exactly what the repair routes on, so **the repair agrees with the auditor rather than the
> reverse**."

— and mg-fcf1's `out_nc4.txt:27` is where the false premise lives:

> "-> the predicate does real work on 3 poset(s): the diagonal matches and the off-diagonal
> signs decide."

The off-diagonal signs do not decide. Nothing decides. **Agreeing with the auditor was the
transmission path.** Generations: mg-09ea → mg-60d3 → mg-5630/NC3 → NC4 (mg-fcf1) → **here**.

---

## FINDINGS

### F1 (headline, and it is the same defect one generation on). Row I4's kept absorbability condition is FORCED, and the reason given for keeping it is FALSE

`absorbable_by_diagonal_twist` (`face_complex.py:750-799`) has **three** early exits before
its parity system, and its own docstring names two of them as forced arithmetic
(`face_complex.py:763-765`):

> "Method: `s_i^2 = 1` pins every **diagonal** entry, `|s_i s_j| = 1` pins every **absolute
> value**, and each nonzero off-diagonal entry forces the product `s_i s_j`. What remains is a
> parity system, solved by union-find."

mg-8a12 routes on the first gate only. `diag_preserved` (`controls.py:832`) counts posets
where the diagonal is unchanged, and the code comment beside it reads
`# here the absorbability answer is not forced`. That comment is false, and so is every
sentence built on it. The absolute-value gate is forced by the *same* arithmetic — and on all
3 posets, it is the gate that fires (`out_gates.txt`):

```
  corruption                      bites  diagMV  diagOK   magMM  parity  absorb
                                         forced          forced    REAL
  I1 ridge_facets                    72      72       0       0       0       0
  I2 split_free_as_interior          82      82       0       0       0       0
  I3 ridge_drop                      82      82       0       0       0       0
  I4 facet_offbyone                  61      58       3       3       0       0
  swap01 (rejected candidate)        72      35      37      37       0       0
  NC3 facet-parity (the witness)     82       0      82       0      82      82
```

**Across the four scored mutations, 0 of 297 biting (poset, mutation) pairs reach the parity
system.** Every absorbability answer in every scored row, I4's included, is settled at a gate
that `s_i^2 = 1` or `|s_i s_j| = 1` forces.

On the 3 posets in question there is not one entry a sign decision could have been made on:

```
  n=3 antichain |L(P)|=6    diagonal preserved=True   MAGNITUDE mismatches=12   (2/row)  sign-only=0
  n=4 antichain |L(P)|=24   diagonal preserved=True   MAGNITUDE mismatches=48   (2/row)  sign-only=0
  n=5 antichain |L(P)|=120  diagonal preserved=True   MAGNITUDE mismatches=240  (2/row)  sign-only=0
  n=6 antichain |L(P)|=720  diagonal preserved=True   MAGNITUDE mismatches=1440 (2/row)  sign-only=0
```

**And it is forced at every `n`, not merely measured to n=6.** The off-diagonal support of
`L^rel` *is* the adjacent-transposition graph — that is claim (1), and claim (1) is proven. The
off-by-one map is `prefixes_true(rot(w))` with `rot` the cyclic rotation of positions, which
carries `n-2` of the `n-1` generators `s_1..s_{n-1}` to generators and the remaining one out of
the set. So exactly one neighbour of every vertex changes: `2|L(P)|` mismatched entries, at
every `n >= 3`. The magnitude gate fires for all of them.

**Every site that carries the false premise, in sequence** (target 1 — read together, not
alone):

1. `controls.py:701-702` (section docstring): *"each row measures `diag_preserved`, the number
   of its biting posets on which the diagonal is unchanged **and the off-diagonal signs
   actually decide**"* — the second conjunct is neither measured nor true.
2. `controls.py:704`: *"`diag_preserved > 0` **the predicate did real work**"* — it did not.
3. `controls.py:832` (code comment): *"`# here the absorbability answer is not forced`"* — it is.
4. `controls.py:892-895` (**the printed row**, in `controls_output.txt`): *"Absorbable into a
   diagonal +-1 twist on 0 of those 61, and this row DOES score it: the diagonal is preserved
   on 3 of them, so **the predicate had to decide on the off-diagonal signs and could have
   returned absorbable**."*
5. `controls.py:936-937` (**the printed routing row**): *"the absorbability answer on the remaining
   1 **was decided on the off-diagonal signs** and stays scored."*
6. `controls.py:962-970` (**the printed measured block**): *"the absorbability predicate — which
   after mg-8a12 scores ONE row (I4, where the diagonal is preserved on 3 of 61 and **the answer
   is a real decision**) … So the predicate **CAN** return absorbable and **row I4 is
   falsifiable**; this is the witness."* The inference is invalid twice over: the witness is
   NC3's parity gauge, whose magnitudes are identical **by construction** (`L_parity = D·L·D`),
   so it cannot witness falsifiability for a corruption whose magnitudes differ 2-per-row.
7. The merge note, twice — *"I4 keeps absorbability scored, since its diagonal is preserved on
   3 of 61 and **the off-diagonal signs really decide there**"* and *"(I1/I2/I3 FORCED, **I4
   real work on 3**)"*. That is the arc's "twice inside a commit's own description of its
   method" pattern again (target 6).

**Consequence.** `cond = cond and absorb == 0` (`controls.py:872`) is a forced condition inside a
`[PASS]` row: precisely mg-2789's defect, in the one row mg-8a12 chose to leave it in, and the
bottom line understates by one. The honest bottom line is **3 rows CANNOT FAIL**, not 2.

**Remedy (small, and does not disturb the mathematics).** Drop `absorb == 0` from I4's `cond`;
extend the `[CANNOT FAIL]` row to all four corruptions with the second line of the argument for
I4 (*a diagonal twist pins every absolute value, and the off-by-one moves `2|L(P)|` of them at
every `n >= 3`*); replace `diag_preserved` with a predicate that asks which gate fired, or
delete the routing concept (F2).

### F2. The routing check is a new scored row that cannot fail — and it is a proof obligation landed as a control (target 5, verbatim)

`controls.py:933-941`, scored `[PASS]` on `0 < len(forced_rows) < len(muts)`. Its answer is
determined by two theorems **this same commit states**:

- I1/I2/I3 move a diagonal entry wherever they apply — a theorem, independently rebuilt below
  over all 1449/981/1459 eligible ridge choices. So all three are always forced.
- I4's diagonal is preserved on the antichains at every `n >= 3` (F1). So I4 is never forced.

Hence `3 < 4` at every `nmax >= 3`, by arithmetic, exactly as `absorbable on 0 of N` was. The
row's own justification is the giveaway — *"If it routed every row one way it would be a
relabelling of the whole section"* — because the thing it guards against is impossible for the
same reason the thing mg-2789 guarded against was impossible.

It is also **the requirement's grammar surviving the repair**. mg-8a12's merge note: *"a routing
check **scores** that separation, since a repair that relabelled every row would look attended
to and cover nothing."* Compare mg-2789's bar, whose failure mode this whole arc exists to
record: *"**show** your corruption is NOT absorbable." * "Show that the split separates" got
implemented as a green row inside a control battery. Fourth generation's lesson, fifth
generation's instance.

**Operationally indifferent, measured** (`out_injections.txt`). I injected three genuine
construction errors into the TRUE build — each one the very defect a row is named for — and
recorded which rows react:

| defect in the pipeline's TRUE build | baseline | I1 | I2 | I3 | I4 | **routing check** |
|---|---|---|---|---|---|---|
| D1 one interior ridge dropped (the I3 defect) | FAIL | FAIL | FAIL | FAIL | FAIL | **PASS** |
| D2 `le_to_facet` mis-indexed (the I4 defect) | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL |
| D3 one free ridge counted as interior (the I2 defect) | FAIL | FAIL | FAIL | FAIL | FAIL | **PASS** |

It stays green under two of three, and reddens under the third only because the off-by-one
build makes row I4's mutation vacuous — which row I4 already reports itself. **It detects
nothing that is not already detected**, which is what "cannot fail" means operationally. Note
also that mg-8a12's four verification injections were all into the SCORING (a wrong prediction,
a corruption that stops biting, a predicate that reports absorbable, every row forced), not into
the CONSTRUCTION the section exists to cover — which is why this came out clean for it.

### F3. The `[CANNOT FAIL]` row can print a FALSE theorem, and its own guard cannot see it

`python3 controls.py 2` is a supported invocation (`controls.py:1044`; `run_all.sh` passes 5,
and the merge note records n<=3 and n<=4 as clean — n<=2 is the one it does not mention).
There, I4 routes to forced (`app == 0`), and `DIAGONAL_MOVES.get()`'s fallback
(`controls.py:920-923`) prints:

> "… I3 is `L_true` minus that ridge's rank-one outer product, so both its facets' diagonal
> entries drop by 1; **I4 moves one, though no closed form for it is recorded in
> DIAGONAL_MOVES**."

That asserts the off-by-one moves a diagonal entry — which the same file measures as **false**
on 3 posets at `n >= 3`. The row's guard is
`theorem_absorb == 0 and theorem_diag == theorem_app`, an aggregate over posets where the
mutation applies; at n<=2 the off-by-one applies nowhere, so `0 == 0` passes and the printed
sentence goes unchecked. The row also prints *"(I1 on 0/0, I2 on 1/1, I3 on 1/1, I4 on 0/0),
and those counts are FORCED at every n"* — a theorem asserted over an empty population.
So *"A FALSE theorem is still a failure"* holds for the aggregate half of what this row asserts
and not for the per-row half. Same run: the routing check FAILS, `CONTROLS FAILED: 3`
(`out_nmax.txt`).

### F4. The new baseline row is a verbatim duplicate of a scored row eight lines above it

- `controls.py:789`: `n_base = sum(1 for P in ps if claim1_test(P, incidence_mode="true") is True)`
- `controls.py:509`: `n_true = sum(1 for P in ps if claim1_test(P, sign_mode="true") is True)`

Both are `claim1_test(P)` with every knob at its default: same function, same population, same
printed `86/86`, both `[PASS]`, eight lines apart in one output. And claim (1) is **PROVEN for
every finite poset** (mg-276d, audit-confirmed mg-e0ce), so what the row measures is a theorem
being read out as an 86-poset count — the shape mg-78c0 named. The merge note's *"now a scored
row rather than an assumption"* is one notch too wide: it was already a scored row, in NEGATIVE
CONTROL 3 line 1. This is **not** a `[CANNOT FAIL]` row — a broken pipeline reddens it, as D1/D3
show — but it is the third copy of one measurement, and the third copy is not evidence.

### F5. The causation half DOES have content — and this cuts for mg-8a12. Sized both directions

I expected this to be the tautology and it is not. `pred = twist(delta)` and
`obs = twist(L_mut) - target`, so `pred == obs` iff **claim (1)** holds on the true build AND
`L_mut - L_true == delta`. The second conjunct holds identically (72/72, 82/82, 82/82,
untwisted — `out_theorem.txt`), so I injected a mutation that is not the local edit it
declares: a `ridge_drop` that drops **two** interior ridges.

```
  a two-ridge drop declared as a one-ridge drop: bites on 72 posets
  the ABSORBABILITY half mg-8a12 removed  would score: absorbable 0/72, diagonal moves 72/72 -> GREEN
  the CAUSATION half mg-8a12 added        would score: residual == prediction 0/72          -> RED
```

**mg-8a12's replacement is strictly stronger than what it removed.** That is the substance of
the repair and it survives everything I threw at it. Two sizing caveats, neither fatal:

- the claim-(1) conjunct is now scored **three** times in one output (NC3 line 1, the new
  baseline row, and inside each of I1/I2/I3's condition);
- *"predicted from the corrupted site alone, **without reading the corrupted matrix**"* — the
  prediction does read the corrupted *build*, for the site
  (`top_laplacians(P, incidence_mode=mode)["mutated_ridge"]`), and for I1 it re-implements the
  mutation's site-selection line verbatim (`face_complex.py:445`
  `j3 = next((j for j in range(nc) if j not in (j1, j2)), None)` vs `controls.py:615`
  `j3 = next(j for j in range(nc) if j not in (j1, j2))`). So it constrains **mis-application**
  of the declared edit, not **mis-specification** of it. The printed sentence is true as
  written; the honest strengthening is "predicted from the true build plus the mutated build's
  declared site".

---

## WHAT STANDS — verified, not assumed, and I tried to break each one

- **0 BROKEN mathematics; the output regenerates byte-identically** (`diff` against the
  committed `controls_output.txt`, clean).
- **Every committed count reproduces from a rebuild that never imports `controls.py`**: app
  72/82/82/61, vacuity 14/4/4/25 on the stated `|L(P)|` sets, spectrum moved 66/82/82/58,
  residual size 6/1/4 and up to 240 for I4, shape unchanged on all four rows
  (`out_scoring.txt`).
- **The theorem half is a theorem, and mg-fcf1's numbers are exact.** Rebuilt from the boundary
  matrix with a *second implementation of each corruption*, over every eligible ridge choice
  rather than the first one `controls.py` mutates: 1449/981/1459 biting choices for I1/I2/I3,
  **diagonal moves on 1449/981/1459, reported absorbable on 0**. The residual bounds are
  provable, not just measured (I2's free ridge has one facet → 1 entry; I3's has two → 4;
  I1's `j1j1` term cancels → 6).
- **NOT an over-correction (target 2).** Nothing reads as "the technique was withdrawn" or "the
  instrument was broken". The file states the opposite where it matters — *"The mathematics is
  untouched: the corruptions are not gauges, and that is a **stronger** statement than mg-2789
  claimed for it, just not a measured one"* — and the C3 repairs land the **strong** way: the
  false self-report is named false rather than softened; *"whose spectrum does move"* is
  narrowed to 58 of 61 **with the reason and the attribution**; and the old hedge is *replaced
  by more* knowledge, not less — *"That is a limit of the invariants used here and NOT an open
  question — mg-fcf1 settled every one of them adversely"*. That is the right direction and it
  is the second landing in this arc to do it.
- **The split really is computed, not hand-written.** `diag_preserved` is measured from the
  population. The defect is that the quantity computed is the wrong one — one of the
  predicate's two forced gates — not that an answer was asserted.
- **The scoring plumbing is consistent with mg-1319, which owns it.** `[CANNOT FAIL]` rows are
  not passes, they still fail on a false fact, and the bottom line correctly refuses
  `ALL CONTROLS PASS` (`2 row(s) CANNOT FAIL`). The `scoring_self_test` rows still pass.
- **The section does cover construction.** Under all three injected pipeline defects, the
  baseline row and all four mutation rows react (F2's table). mg-2789's core contribution and
  mg-8a12's preservation of it both stand.
- **Runtime rule respected**, no mg-7db4 defect: NEGATIVE CONTROL 4 measures **1.74 s** CPU and
  the whole battery **2.11 s** on this host, unconditional in `main()`.
- **STATE.md and Appendix A untouched**, as the ticket required, and the merge note says what it
  deliberately did not do (rescoping I4 for mg-fcf1 F1 — correctly deferred).

---

## MINOR / CARRIED FORWARD (not mg-8a12's to fix, recorded so they are not lost)

1. **The false premise originates upstream, in the audit.** `out_nc4.txt:27` (mg-fcf1) asserts
   *"the predicate does real work on 3 poset(s): the diagonal matches and the off-diagonal signs
   decide"*, untested. It should be corrected wherever it is quoted.
2. **STATE.md § Appendix A** (landed by mg-a806, not by mg-8a12) says *"Three of NEGATIVE
   CONTROL 4's four rows then could not fail"*. The accurate statement is that **the
   absorbability answer is forced on all four**; the fourth row can fail, but on its other
   conditions. Not edited by me.
3. **`run_all.sh`'s comment is stale in its numbers**, though not in its conclusion: it says
   `controls.py 1.9 s` of which NEGATIVE CONTROL 4 is `1.4 s`; measured here 2.11 s / 1.74 s
   (+11% / +24%). Still order-seconds, so *"needs no scoping"* holds. mg-8a12 named this and
   left it out of scope, correctly. `run_all.sh` also still calls this "the CI-adjacent battery"
   and there is no CI in the repository (mg-fcf1's minor, unrepaired).
4. **mg-fcf1's F3 tautologies in the unscored block are unrepaired** — *"the target D-A is
   byte-identical … on 344/344"* (forced: `incidence_mode` is never forwarded to
   `at_laplacian`) and *"no ridge lies in >= 3 facets"* (forced by construction for I1/I2/I3).
   Outside mg-8a12's stated scope; they are measurements, not rows; still open.

---

## NET

The repair does the substantive thing it was asked to do: three forced conditions are out of
the scored rows, the property they carried is stated once as a theorem with a correct two-line
argument, the false self-report is named as false, and the replacement scored condition is
**strictly stronger** than what it replaced — established here by injection, not taken on
trust. The mathematics is untouched and nothing is withdrawn that was earned.

And the defect recurred, in the landing that repairs it, at two new locations: a row whose
absorbability answer is still forced (I4, by the gate nobody looked at) and a brand-new row
that cannot fail (the routing check, a *"show that the split separates"* obligation implemented
as a green row). Both were reachable by asking the repair's own question — *can this fail?* — of
the repair's own additions, and the reason neither was asked is recorded in the merge note: the
one fact the routing depends on was adopted from the auditor rather than measured.

**Fifth generation. First one to arrive inside the remedy rather than beside it.**
