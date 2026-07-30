# Independent audit of mg-a893 / `90db267` — the dependence repair

*Audit by mg-c6bc, 2026-07-30, pre-filed at dispatch per mg-0e24. Subject: `90db267`, mg-a893's repair
of `docs/OneThird-Counterexample-Under-The-Action-Repair.md` and
`docs/OneThird-Counterexample-Under-The-Action.md` following mg-0a11's audit of mg-dea5. Everything
numerical here is produced by `code/counterexample_audit_c6bc/`, which imports **nothing** from
`code/counterexample_repair_dea5/` (the subject), `code/counterexample_probe_24a3/` (the target) or
`code/counterexample_audit_0a11/` (the previous audit). Its definitions are rebuilt from the sentences of
the documents. Regenerate with `code/counterexample_audit_c6bc/run_all.sh` — pure Python 3, no
dependencies, about 4 minutes, exact integer and rational arithmetic; every output reproduces
byte-identically.*

---

## 0. VERDICT

| | |
|---|---|
| **THE COMPUTATION REPRODUCES, ALL OF IT** | Every figure mg-a893 added reproduces from this instrument: 63 / 318 / 2045 / **16999** posets, 16 / 88 / 671 / **6420** population, **691** `e`-groups at `n = 8`, groups of **2 / 7 / 13 / 20**, extremal **1 / 3 / 6**, **13 of 13** and **20 of 20** with a cut element, **C = 5** at all three sizes, and the five cores with their cover strings character for character. The cut-element theorem is correct as stated. The withdrawal of "new population" is correct. **The separation is real and this audit extends it**, member by member, to `n = 9` (10 of 29) and `n = 10` (15 of 39) — one size past mg-0a11. |
| **BROKEN 1 — THE OVER-CORRECTION, AND IT IS THE SENTENCE THE REPAIR LEANS ON** | §3.4 asserts, in bold and without a range, **"Nothing enters the family after `n = 6`."** It is **false**. At `n = 9` the `e = 9` family acquires a **cut-free** member — `C₈` with one isolated element beside it — carrying a **sixth core** that no cut extension can produce. The repair's own document contradicts it two paragraphs later ("over **six** distinct cores"), and **mg-a893's own brief states the six-core figure**. Consequence: the repair **understates its own evidence**. The separation survives a genuinely new core, which is a real independent replication, and the repair's framing discards it. |
| **BROKEN 2 — THE DEPENDENCE IS NOT EXHAUSTED BY CUT ELEMENTS, AND THE OBJECT IS BUILT** | The `1/5` counts five cores as five independent chances for the hypothesis to fail. Two pairs of them are **order duals**: `C₂ = C₁ᵒᵖ` and `C₄ = C₃ᵒᵖ`. `(e, δ, qmass)` is **exactly** dual-invariant — proved here in five lines and measured on the whole population, **775 of 775, 0 failures** — so duality collapses cores by the same rule cut extension does, and needs no measurement to do it. Duality is **not** a cut extension: cores are cut-free, so neither member of a dual pair is an extension of the other. **The five cores are three independent units.** |
| **THE HONEST NUMBER, WITH BOTH CORRECTIONS APPLIED** | Six cores over `n = 5 … 12`, falling into **four duality classes**, exactly one of them extremal. **`p = 1/4`**, not `1/5`. The two findings point in opposite directions and do not cancel: duality takes `1/5 → 1/3`, the sixth core takes it back to `1/4`. |
| **THE CHECKER GATE IS HONOURED; THE FIX IS FITTED TO ITS TEST SET** | `code/counterexample_audit_0a11/` is byte-for-byte untouched, and its battery re-run from this worktree is **byte-identical** to the committed `out_battery_0a11_rerun.txt`: 0 silent misses, 0 skipped. Six new probes its author never saw: **6 of 6 silent**. The sharpest — mg-0a11's M1a re-created for the *new* headline, pointing the other way. |
| **3 MINOR** | NC1 is a control that **cannot fail**; `cores.py`'s "extremal" is a different quantity from the document's at `n = 5`; the `257` is a `(poset, cut point)` count and `209` up to isomorphism. |

**None of this touches the mathematics.** As with mg-0a11's audit of mg-dea5, this is an audit of an
inference. §4's null is still false, the `e = 3` control is still vacuous, `qfrac` is still null after the
same control, `ρ|e` is still `≈ −0.27`, and `qmass = 1` still picks out exactly the `δ`-extremal posets in
every group where it could fail — at more sizes than before.

---

## 1. WHAT WAS RE-DERIVED, AND FROM WHAT

`code/counterexample_audit_c6bc/kern6bc.py` is a fourth independent implementation. It takes `δ` and
`Inc` from §1 of the target, the `P`-compatible move / level / `m_X` triple from §1 of
`OneThird-Semigroup-Walk-Family-Note.md`, `qfrac` / `qmass` / `L*` from §4 and §2 of the target, and cut
element / cut extension / core from §3.4 of the repair. It shares no line with any instrument in the
lineage.

Its own controls are in `out_selftest.txt`, labelled the way mg-3b51 asked: **positive** controls
(A000112 to `n = 7`; `e` on a chain and an antichain; `canonical()` blind to 120 relabellings), one
**theorem with an implementation check** (`Σ m_X` over all levels `= e(P)`, 19 posets, 0 disagreements),
and **three negative controls that fire** — breaking the level test changes `qmass` on 3 of 16; the
identical duality loop run on `#minimal elements` differs on 50 of 88, so "invariant under duality" is a
measurement and not a property of the loop; a mean-instead-of-max `δ` changes extremal status on 4 of 16.

**Two published figures pin the `qmass` implementation before it is used on anything new**: the target's
own saturation counts, `6 of 16` at `n = 5` (50.0% of them extremal) and `11 of 88` at `n = 6` (45.5%),
both reproduce exactly.

---

## 2. WHAT HOLDS

| claim | source | this audit |
|---|---|---|
| posets up to iso, `n = 5 … 8` | A000112 | 63 / 318 / 2045 / **16999** ✓ |
| population (non-chain, tie-free, majority-acyclic) | `out_cores.txt` §0 | 16 / 88 / 671 / **6420** ✓ |
| `e`-groups at `n = 8` | `out_cores.txt` §4 | **691**, `C = N` in 553, `C < N` in 138 ✓ |
| `e = 9` group sizes | repair §3.1 | 2 / 7 / 13 / **20** ✓ |
| `δ`-extremal in them | repair §3.1 | — / 1 / 3 / **6** ✓ |
| members with a cut element | repair §3.4 | 0 / 4 / **13 of 13** / **20 of 20** ✓ |
| `group(n+1)` = cut extensions of `group(n)` | repair §3.4 | no / **YES** / **YES**, 3 new at `n = 6` ✓ |
| distinct cores per group | repair §3.4 | 2 / **5** / **5** / **5** ✓ |
| the five cores, `δ`, `qmass`, covers | repair §3.4 | identical, character for character ✓ |
| cut extensions measured | repair §3.4 | **257** `(P, D)` pairs, 0 failures ✓ |
| non-cut adjunctions | repair §3.4 | **1378** ✓ |
| `qmass = 1` saturation | target §4 | 6 of 16, 11 of 88 ✓ |
| `out_controls` / `out_cycles` / `out_theorem4` did not move a byte | commit message | ✓ (`git diff` empty) |
| `out_section4.txt` changed in prose only | commit message | ✓ (every number identical) |
| pm-onethird mailed per acceptance item 4 | commit message | ✓ (mail from `a893`, 2026-07-30) |
| mg-0a11's battery re-run **unmodified** | repair §8.2 | ✓ byte-identical to a fresh run here |

**The cut-element theorem is correct.** Re-derived rather than cited in `out_a2_theorem.txt` §1: if `x` is
comparable to everything then `D ∪ U` is all of `P`, transitivity puts `D` below `U` inside `P`, so every
linear extension of `P` already lists `D` before `U` and there is exactly one slot for `x`. Insertion is a
bijection, so `e(Q) = e(P)`, `Inc(Q) = Inc(P)`, every `p(y,z)` is unchanged, `δ(Q) = δ(P)`. The repair is
explicit that `qmass` is not covered by the argument and measures it, which is the right way round.

**And the separation extends.** `qmass` computed directly on every member, not inherited:

| `n` | `N` | extremal | `qmass = 1` | perfect in both inclusions |
|---|---|---|---|---|
| 9 | 29 | 10 | 10 | **YES** |
| 10 | 39 | 15 | 15 | **YES** |

---

## 3. BROKEN 1 — "Nothing enters the family after `n = 6`" is FALSE

§3.4 of the repair, in bold, ending the paragraph that carries the reduction tables:

> The two tables say the same thing twice: `group(n+1)` sits inside the cut extensions of `group(n)`
> exactly when `group(n+1)` has no cut-free member, and after `n = 6` it has none. **Nothing enters the
> family after `n = 6`.**

The premise is right for `n ≤ 8` and the conclusion is stated for all `n`. It is false at `n = 9`.
`out_a4_extend.txt` enumerates the whole `e ≤ 9` family to `n = 12` — **completely**, not by search: the
restriction map `L(Q) → L(Q − x)` is onto for a maximal `x`, so `e(Q − x) ≤ e(Q)`, so `{P : e(P) ≤ 9}` is
closed under deleting a maximal element and incremental generation with pruning reaches every member.
(The control on that argument is in `out_selftest.txt`: the pruned enumeration and the full enumeration
agree exactly on `n = 5 … 8`, 32 / 60 / 97 / 144.)

| `n` | `e ≤ 9` posets | `N` | **cut-free** | `C` | `k` extremal | cores so far |
|---|---|---|---|---|---|---|
| 6 | 60 | 7 | 3 | 5 | 1 | 5 |
| 7 | 97 | 13 | 0 | 5 | 3 | 5 |
| 8 | 144 | 20 | 0 | 5 | 6 | 5 |
| **9** | 202 | 29 | **1** | **6** | 10 | **6** |
| 10 | 271 | 39 | 0 | 6 | 15 | 6 |
| 11 | 352 | 50 | 0 | 6 | 21 | 6 |
| 12 | 446 | 62 | 0 | 6 | 28 | 6 |

The group sizes `2 + 7 + 13 + 20 + 29 + 39 + 50` sum to **160** over `n = 5 … 11`, which is mg-0a11's
"160 group memberships" exactly — an independent confirmation of this enumeration at the three sizes
mg-a893's own instrument does not reach.

**The sixth core, exhibited.** Size 9, `δ = 4/9`, `qmass = 1/3`, self-dual, covers
`0<2 2<3 3<4 4<5 5<6 6<7 7<8` — the 8-chain with one isolated element beside it. Its `e` is exactly 9
because the loose element has nine slots, which is why it cannot appear before `n = 9` and does appear
there. It is **cut-free**: the loose element is comparable to nothing, so nothing is comparable to
everything.

**Three things follow, and the third is the finding.**

1. The sentence is false as published. It is true of `n = 5 … 8`, which is the range of the tables above
   it, and it is not written with that range.
2. The document refutes itself two paragraphs later — *"mg-0a11 carried the same measurement to `n = 11`
   … over **six** distinct cores"*. Five cores at `n ≤ 8` and six at `n ≤ 11` is precisely a family that
   something entered. **mg-a893's own brief carries the same figure** ("6 at n=9,10,11"), so the
   contradicting datum was in the ticket before the sentence was written.
3. **This is the over-correction.** The repair's case is *"the three sizes are one observation and not
   three"*, and that case rests on nothing entering. At `n = 9` something does enter — a new core, not
   reachable by cut extension, that gives the hypothesis a fresh chance to fail. It does not fail: the new
   core has `qmass = 1/3` and is not extremal, and it is correctly not marked. **That is a replication the
   repair's framing throws away**, and it is exactly what acceptance item 2 told the repair not to do.

The commit message says **"AND NOT OVER-CORRECTED"** and lists what survives. Per the standing target for
this lineage: naming the failure mode is not handling it. The named risk landed in the sentence next to
the disclaimer.

---

## 4. BROKEN 2 — order duality, a dependence route that is not a cut extension

The repair's step is: two members with the same core have the same `(δ, qmass)`, so they are not two
independent chances for the hypothesis to fail; a group with `C` cores offers `C` chances and the exact
`p` is `1/C(C, c)`.

**That step never mentions cut elements.** It needs only a map that fixes `(δ, qmass)` and is not the
identity. Here is a second one.

> **`P ↦ Pᵒᵖ`.** `Inc(Pᵒᵖ) = Inc(P)` and `p_{Pᵒᵖ}(x,y) = p_P(y,x)`, so `min(p, 1−p)` is unchanged pair by
> pair and `δ(Pᵒᵖ) = δ(P)`; `e(Pᵒᵖ) = e(P)` by reversing every linear extension; the majority relation
> reverses, so `L*` is read backwards and the partitions into `L*`-intervals are the **same partitions**;
> a partition's block digraph reverses, so it is a level of `Pᵒᵖ` iff it is a level of `P`, and
> `e(P|_B) = e(Pᵒᵖ|_B)` block by block, so every `m_X` is unchanged. Hence **`qmass(Pᵒᵖ) = qmass(P)`,
> exactly, with nothing measured.** ∎

Measured anyway, on the whole population: closed under duality at `n = 5, 6, 7` (16 / 88 / 671), and
`(e, δ, qmass)` differs on **0 of 775**. The negative control on that loop is in `out_selftest.txt`.

**The five cores are three duality classes.**

| core | size | `δ` | `qmass` | dual | covers |
|---|---|---|---|---|---|
| `C₁` | 5 | `4/9` | `8/9` | `C₂` | `0<2 0<3 1<3 2<4` |
| `C₂` | 5 | `4/9` | `8/9` | `C₁` | `0<2 1<3 1<4 2<4` |
| `C₃` | 6 | `4/9` | `2/3` | `C₄` | `0<2 1<5 2<3 3<4 3<5` |
| `C₄` | 6 | `4/9` | `2/3` | `C₃` | `0<2 0<3 1<3 3<4 4<5` |
| **`C₅`** | **6** | **`1/3`** | **`1`** | `C₅` (self) | `0<2 1<3 1<4 2<3 2<4 3<5` |

`{C₁, C₂}`, `{C₃, C₄}`, `{C₅}`. Duality is **not** a cut extension — a core is cut-free by construction,
so neither member of a dual pair is an extension of the other, and no chain of cut extensions relates
them. Applying the repair's own rule to its own cores gives **three** independent units and
`p = 1/C(3,1) = 1/3` at `n ≤ 8`.

**With BROKEN 1 folded in**: six cores over `n = 5 … 12`, the sixth self-dual, so **four** duality
classes, exactly one extremal.

> **THE HONEST EXACT `p` IS `1/4`.** The repair's `1/5` is wrong in both of its factors — too many units
> because it does not quotient by duality, too few because it stops at `n = 8` — and the two errors
> partially cancel, which is why `1/5` looks reasonable.

**What this does not touch.** The separation is still perfect in both inclusions everywhere it can fail;
`qmass = 1` still holds on the extremal class and no other; §4's null is still false. Only the strength
moves, and it moves less than the repair's own correction moved it.

---

## 5. MINOR

**M1 — NC1 is a control that cannot fail.** `out_cores.txt` labels it *"A NEGATIVE CONTROL, and it
fires"*: over 1378 non-cut adjunctions, `(e, δ, qmass)` is inherited 0 times. But the criterion is a
conjunction and its first conjunct is impossible. If `D` is a **proper** down-set then `P \ D` contains a
maximal element `m` of `P`; put `m` last in a linear extension of `P` and the new element `x` may go last
or immediately before `m`, so `e(Q) > e(P)` for **every** such `D`. The "0 of 1378" is a theorem about `e`
alone. This is mg-3b51's finding against mg-1953, and the repair applies that lesson explicitly to `C2`
two paragraphs earlier while leaving `NC1` billed as a control that fires.

Re-run on the statistic the theorem is actually *used* for, the control is not vacuous and not perfect:

| | of 1378 |
|---|---|
| `e(Q) = e(P)` — cannot happen | **0** |
| `δ(Q) = δ(P)` | **53** |
| `qmass(Q) = qmass(P)` | **29** |
| both | 9 |

So *"inherited is a property of cut extension and not of adjoining an element"* is true as a tendency
(96.2%) and false as an implication. Nothing downstream depends on the converse — the dependence argument
uses the theorem only forwards — so this is a labelling defect, not a mathematical one.

**M2 — "extremal" means two different things.** `cores.py` computes `dmin = min δ within the group` and
calls the members attaining it extremal. The documents define `δ`-extremal absolutely, as `δ(P) = 1/3`.
At `n = 6, 7, 8` the two coincide. At `n = 5` they do not: the `e = 9` group's two members both have
`δ = 4/9`, so it contains **no** `δ`-extremal poset, while `out_cores.txt` prints *"extremal in it  2"*
and a row `n=5 · N=2 · k extremal=2 · extremal cores=2 · p = 1/1`. The `n = 5` row is not carried into
either document (the published core tables start at `n = 6`), so this is an instrument-output defect that
does not propagate. It is beyond-brief material.

**M3 — `257` is a `(poset, cut point)` count, `209` up to isomorphism.** Both give 0 inheritance
failures, so the figure is right; the convention is worth naming because "cut extensions inside the
population: 257" reads as a count of posets and is a count of pairs.

---

## 6. THE CHECKER — the gate is honoured, and the fix is fitted to its test set

**The gate is real.** `code/counterexample_audit_0a11/` is byte-for-byte identical to what mg-0a11
committed (`git diff 20fab09 HEAD` on that directory is empty), and running `check_locator.py` unmodified
from this worktree produces output **byte-identical** to the committed `out_battery_0a11_rerun.txt`:
19 mutations in all (15 against the subject's checkers, 4 self-mutations against mg-0a11's own),
**0 skipped**, **0 silent misses**, all four self-mutations still firing, all three doc-checkers baseline
clean. The claim is exactly true.

**Six new probes, none of which mg-a893's author saw.** `out_a5_battery.txt`.

| | probe | result |
|---|---|---|
| **C1** | the §3.4 conclusion is **reversed by a pure insertion** — no needle deleted, no count changed, no cell moved, no heading touched | **SILENT** |
| **C2** | the **unkeyed** row of the §3.4 core table (`n = 7`) is rewritten to say the separation there was 2 of 4 | **SILENT** |
| **C3** | *"over **six** distinct cores"* at `n = 11` changed to *"five"* | **SILENT** |
| **C4** | the whole `n = 11` clause deleted | **SILENT** |
| **C5** | the honest `p` falsified **in the target document only** | **SILENT** |
| **C7** | the five-core table HTML-commented out of the rendered page | **SILENT** |
| C6 | *(control)* `out_cores.txt`'s honest-`p` line falsified | **fires** ✓ |

C6 is the control and it fires, so what is one-sided is the **coverage**, not the mechanism.

**C5 is the finding.** P1 — *"every figure names its document and its exact occurrence count"* — is the
property mg-0a11's M1a existed to force, and it is the property mg-a893 built. `FIGURES` carries
`("honest p over the cores", "repair", ...)` and **no entry for the target**, so the sentence the whole
repair exists to install can be silently falsified in the target document. That is M1a re-created for the
new headline, pointing the other way. The same shape appears in C2: the §3.4 core table gained row keys
for `n = 6` and `n = 8` and none for `n = 7`.

**C3 / C4 are semantic and outside a quote-checker's power** — the repair says so plainly, and that is
fair. What is worth recording anyway: the sentence the checker *does* protect in §3.4 is
`**Nothing enters the family after n = 6.**` (a `FIGURES` entry, count 1, paired with the `out_cores.txt`
line `6 -> 7  13  YES`, which does not support it), and the sentence it does **not** protect is the one
that contradicts it. **The checker certifies the false claim and leaves its refutation unguarded.**

**C7 confirms the named boundary is real.** §8.2 says *"a figure of this document wrapped in an HTML
comment would still pass this file"*. It does. Naming is not handling.

**The mg-4acd cross-check, answered by construction rather than by argument.** §8.2 concludes the two
mechanisms are *"complementary, not redundant"*. That is correct and it is not the whole answer.
`delta_control.py`'s `CERTIFIED` table names exactly two files — `STATE.md` (row `:135`'s content cell)
and `docs/state-history/README.md` (nine correction blocks). Neither counterexample document is a
certified region, so:

* **C8** guts the `readme.F1` block — a region mg-4acd's presentation digest certifies — and
  `check_doc_repair.py` exits **0**;
* conversely, no edit to either counterexample document can change the bytes or the presentation record of
  any certified region, because none of them is in either file. That needs no run: it follows from the
  region list.

**So the two mechanisms coexist and do not compose.** "Complementary" here means **disjoint**, and the
hole between them is exactly the *presentation* of the two counterexample documents — which is what C7
walks straight through. `presented` is the one mg-4acd field with no analogue in this checker, and it is
the one C7 needs.

---

## 7. BEYOND-BRIEF MATERIAL

The brief (mg-a893) asked for four things: restate the claim honestly and retire "new population"; do not
over-correct; fix the checker per-document and re-run mg-0a11's battery unmodified, cross-checking
mg-4acd; and tell whoever relayed the number outward. All four were delivered. **The delivered change goes
beyond all four**, principally in `cores.py` (507 new lines), which the brief did not ask for — it asked
for the number, not for a third derivation of it.

Auditing the beyond-brief material first, as the standing target for this lineage requires:

* **BROKEN 1** is beyond-brief: *"Nothing enters the family after `n = 6`"* appears nowhere in the brief,
  is derived in the delivered change, and is contradicted by a figure the brief supplied.
* **M1** (NC1) and **M2** (the `n = 5` "extremal" row) are both inside `cores.py`'s unbriefed controls and
  its unbriefed `n = 5` row.
* **BROKEN 2** is against a briefed claim, but against the *unstated* generalisation of it — the brief
  said "report the exact `p` over distinct cores", and cores are the right unit only if nothing else
  collapses them.

**Four of five findings sit in material with no acceptance criterion**, and the fifth is against the
unstated generalisation of a briefed one. This audit does not re-verify the standing claim that the same
has held for roughly seven consecutive generations; it adds one more instance to it. The pattern is worth
acting on rather than re-observing: *a derivation added beyond the brief should carry its own acceptance
line, written before it is run.*

---

## 8. WHAT THIS AUDIT COULD NOT ESTABLISH

* **Whether four is the final count of independent units.** Duality is one further collapsing map; this
  audit did not prove there is no third. The honest reading of `1/4` is *an upper bound on the strength*,
  the same status `1/5` had. Any map fixing `(δ, qmass)` reduces it further.
* **The member-level separation beyond `n = 10`.** `qmass` was computed directly to `n = 10`; at `n = 11`
  and `n = 12` only the core set was checked (unchanged at six, `qmass = 1` on the extremal core and no
  other). The member-level statement there rests on the measured half of the inheritance, as the repair's
  does.
* **Whether `e = 9` is special.** Unexplained here as in the repair. The sixth core arriving exactly at
  `n = 9` for an arithmetic reason (nine slots for a loose element) is suggestive and is not a mechanism.
* **`presentation.py` as a model of a renderer.** Not re-examined; mg-218d's finding stands and is out of
  scope here.

---

## 9. FILES

```
code/counterexample_audit_c6bc/kern6bc.py         the instrument, built from the documents
code/counterexample_audit_c6bc/selftest6bc.py     its controls, 3 of which are negative -> out_selftest.txt
code/counterexample_audit_c6bc/a1_recount.py      every figure recounted            -> out_a1_recount.txt
code/counterexample_audit_c6bc/a2_theorem.py      the theorem, and NC1              -> out_a2_theorem.txt
code/counterexample_audit_c6bc/a3_duality.py      BROKEN 2, by construction         -> out_a3_duality.txt
code/counterexample_audit_c6bc/a4_extend.py       BROKEN 1, to n = 12               -> out_a4_extend.txt
code/counterexample_audit_c6bc/a5_battery.py      six new probes + composition      -> out_a5_battery.txt
code/counterexample_audit_c6bc/run_all.sh         regenerates all six, ~4 min
                                                  and re-runs mg-0a11's battery for the diff
```

*Audit by mg-c6bc. No document under audit is edited by this ticket: the findings are here and in
`code/counterexample_audit_c6bc/`, for the repair stage to action. The `1/5` has already been relayed to
`pm-onethird` for Daniel comms (mail from `a893`, 2026-07-30); **that relay needs a correction to `1/4`**,
and it is the one part of this audit that is time-sensitive.*
