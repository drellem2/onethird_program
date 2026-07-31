# The four warrant findings of mg-5800, landed — as written, the evidence, as narrowed

**Work item:** mg-dffa. **Date:** 2026-07-31. **Target:**
`docs/OneThird-Branching-Graphs-Where-This-Lives.md` (mg-af28, repaired by mg-41aa /
`504ab6c`) and `code/branching_repair_41aa/check_doc.py`. **Audit landed:**
`docs/OneThird-Audit-mg-41aa-Repair.md` (mg-5800, `8ce78fb`), findings **F1–F4**, all MINOR,
all about warrant. **Computation:** permitted, used, committed
(`code/branching_warrant_dffa/`, `run_all.sh`, 5 s measured, 42-assertion self-test).

**Nothing in the target was wrong.** mg-5800 confirmed the mg-41aa repair with 0 BROKEN,
reproduced every figure from a disjoint instrument, and closed the repair's own weakest link
by measuring the converse of X1 at `n = 6` without Birkhoff. The four open findings are all
of one kind: **a claim stated with more warrant than its evidence carries.** No number moves
here, no measurement is withdrawn, and no measurement is added to except where the wider
claim was one worth having.

**This deliverable is of the same kind as the defect it repairs** — its entire content is
rewriting claim statements, which is where a wrong new statement is likeliest. §5 enumerates
what was checked before each new sentence was written, and §6 states what this repair could
not establish.

---

## 0. THE FOUR, IN ONE TABLE

| | site | direction | cost as filed | cost as landed |
|---|---|---|---|---|
| **F1** | §6 ledger, rows **B1** and **B5** | **widened** to the evidence | two ledger cells | two ledger cells |
| **F2** | §2 heading note; §3 row 10 | **narrowed** to the evidence | one clause | one clause each |
| **F3** | `check_doc.py` | control that could not fire | one line | two checks, plus a both-directions control |
| **F4** | §0 consequence 3 | premise unaffirmed | one clause | **the premise was read** |

**F1 runs the opposite way from F2 and F4.** F1's two cells state *less* than what was
measured; F2's two clauses state *more*. Both are the same defect — a sentence that is not
the width of its evidence — and both are fixed by moving the sentence, not the evidence.

**No hedges were used.** mg-5800's brief forbids splitting the difference, on the grounds
that this arc has just produced a case where a hedge covered exactly the adverse cases. Each
of the eight rewritten sentences below is a definite statement of what is known.

---

## 1. F1 — the ledger recorded what the audit broke and not what it strengthened

mg-6ad0 did not merely confirm B1 and B5; it strengthened both. mg-41aa added three primed
rows (**B2′**, **B4′**, **B7′**) for what was **BROKEN** and none for what was
**STRENGTHENED**, so B1 and B5 stayed byte-identical to their pre-repair text — recording
the strengthening everywhere except the ledger, which the repair itself quotes mg-6ad0 as
calling *"what downstream readers quote"*.

### F1a — ledger row B1, scope column

**AS WRITTEN**

> 44 partitions, `n ≤ 7`, order isomorphism checked on every pair in both directions, 0 bad;
> `f^λ` against an independently coded hook length formula, 0 bad

**THE EVIDENCE THAT EXISTS**

* **mg-6ad0**, `code/branching_audit_6ad0/out_a1_contact.txt`:
  `LATTICE-isomorphism bad (meet/join preserved): 0`, 44 partitions — and the verdict line
  *"CONFIRMED, and strengthened to a lattice isomorphism"*.
* **mg-5800**, `code/branching_audit_5800/out_a5_b1b5.txt`: `MEET not preserved: 0`,
  `JOIN not preserved: 0`, 44 partitions, largest interval 19 elements.
* **mg-dffa**, `code/branching_warrant_dffa/out_w1_ledger.txt`: re-measured here, 44
  partitions, **5 464 ordered pairs**, order 0 bad, meet 0 bad, join 0 bad — with the two
  sides built from different definitions (order ideals of the cell poset on the left,
  containment of **partitions** on the right).
* And, located in af28's own source: `t_young.py`'s T1 computes **no** meet and **no** join
  (0 occurrences of either word in its body) while printing the label `lattice-iso bad`.

**AS NARROWED** *(widened, in this case — the cell was below its evidence)*

> 44 partitions, `n ≤ 7`. **Meet and join preserved on every pair, not the order alone**:
> measured three times on disjoint instruments — mg-6ad0 (…`out_a1_contact.txt`), mg-5800
> (…`out_a5_b1b5.txt`) and mg-dffa (…`out_w1_ledger.txt`, 5 464 ordered pairs, the two sides
> built from order ideals and from containment of **partitions** respectively) — **0 bad each
> time**. T1 in `code/branching_af28/` itself tests the **order** isomorphism only, on every
> pair in both directions, 0 bad, though it prints the label `lattice-iso bad`. `f^λ` against
> an independently coded hook length formula, 0 bad

**Why the last sentence is in the cell.** The output over-labels and the ledger under-states,
off one test. Recording only the strengthening would leave a reader who opens
`out_young.txt` unable to tell which of the two is load-bearing. The label in
`code/branching_af28/` is **not** changed: that would rewrite a committed output mg-5800
re-ran and found byte-identical, and no ticket has asked for it.

### F1b — ledger row B5, scope column

**AS WRITTEN**

> trace-form rank in exact rational arithmetic; all 87 classes to `n ≤ 5` and 308 of 318 at
> `n = 6`, 0 bad. **The step from this to "all irreducibles are 1-dimensional" is Brown's
> theorem, cited, not re-derived here**

**THE EVIDENCE THAT EXISTS**

* *"not re-derived here"* is **still true of `code/branching_af28/`**, and that half is kept.
* **mg-6ad0**, `out_a4_algebra.txt`: `Φ : kF(P) → k^{AC(P)}` surjective with nilpotent
  kernel, *"B5 CONFIRMED by a route that uses no theorem of Dickson and no trace form"* — on
  **67** of the 87 classes to `n ≤ 5`, **20** skipped over its cap of 90 on the size of
  `F(P)`, each skip listed. (67/20/87 are read out of its own table by
  `code/branching_warrant_dffa/w1_ledger.py`, not typed.)
* **mg-5800**, `out_a5_b1b5.txt`: the same, *"with NO trace form and NO cited theorem"*, on
  **all 87** — the classes mg-6ad0's cap excluded included.

**AS NARROWED**

> trace-form rank in exact rational arithmetic; all 87 classes to `n ≤ 5` and 308 of 318 at
> `n = 6`, 0 bad. **The step from this to "all irreducibles are 1-dimensional" is Brown's
> theorem, cited and not re-derived in `code/branching_af28/`** — but it has since been
> derived without it: `Φ : kF(P) → k^{AC(P)}` built from the product alone, surjective,
> `ker Φ` a nilpotent ideal, 0 bad — by mg-6ad0 on 67 of the 87 classes to `n ≤ 5` (20 over
> its cap of 90 on the size of `F(P)`, each listed) *"by a route that uses no theorem of
> Dickson and no trace form"*, and by mg-5800 on all 87 *"with NO trace form and NO cited theorem"* (…).
> **mg-dffa LOCATED both results in those committed outputs; it did not re-run them and does
> not re-derive the step itself**

**LOCATED, NOT MEASURED — and the cell says so.** This is the one place in this repair where
a new sentence rests on somebody else's run. The alternative was to re-derive `kF(P)/rad` a
third time, which is evidence-gathering that mg-5800's brief tells this repair not to do
unless the wider claim is one we want; the wider claim here is *"someone has derived it"*,
and locating their printed result is exactly the evidence for it. The two verbs are kept
apart in the cell so a downstream reader can see which is which.

---

## 2. F2 — "the same index-set contact" reads as parity with a classification

mg-41aa's brief was X1–X4. Five items exceed it; four are bookkeeping or declared. The fifth
carries a **new positive claim**, in two places. Every number in it reproduces — 33
intervals, 5 non-distributive with witness `221`, 28 distributive, 28 reconstructions 0 bad,
30 of 30 on the Young side; all re-measured here on a fourth instrument. **The wording is
what is wrong.**

**THE EVIDENCE THAT EXISTS** (shared by F2a and F2b;
`code/branching_warrant_dffa/out_w2_family.txt`)

* Young–Fibonacci to rank 6: **33** intervals `[0̂, w]`, all of them lattices; **28**
  distributive, **5** not, smallest witness **`w = 221`**.
* Birkhoff gives each of the 28 as `J(P)`; `|J(P)| = |interval|` on every one, 0 bad. **That
  is all it gives — it names no class of `P`.**
* The 28 yield **17 distinct `P`** up to isomorphism, of which **5 are not skew cell
  posets**: 2 of the 4 at `|P| = 5`, 3 of the 5 at `|P| = 6`.
* The Young side, same code: **30 of 30** intervals `[∅, λ]`, `|λ| ≤ 6`, distributive; each
  one's join-irreducible poset **is** the cell poset `D_λ`; **0** of the resulting `P`
  outside the skew class.
* Controls on that measurement, because it carries a negative: the cover rule is checked
  against `DU − UD = I` as an **operator identity** (the rank sizes are not a control —
  **two** wrong cover rules were written here and both returned 1, 1, 2, 3, 5, 8, 13); the
  skew-shape search box is grown from `k` to `k+1` and the class **set**, not merely its
  size, is required to be identical.

### F2a — §2's heading note

**AS WRITTEN**

> At the level of finite **intervals** the index-set contact **does** extend — to 28 of the
> 33 finite Young–Fibonacci intervals, item 2.

**AS NARROWED**

> At the level of finite **intervals** a contact of the same **kind** extends: **28 of the
> 33** finite Young–Fibonacci intervals are distributive, so each is `J(P)` for some `P`,
> item 2.

with a second paragraph carrying the divergence: that the Young headline is a
**classification** (`P` **exactly** the skew cell posets, a named closed class), that the
Young–Fibonacci sentence is **Birkhoff plus a distributivity count** and names no class of
`P`, and that the 28 yield 17 distinct `P` of which 5 are not skew cell posets.

### F2b — §3 row 10

**AS WRITTEN**

> Row 10 therefore has the **same index-set contact** this document headlines for Young's,
> on 28 of 33 intervals

**AS NARROWED**

> Row 10 therefore has an index-set contact of the **same kind** as the one this document
> headlines for Young's, on 28 of 33 intervals

followed by: *"it is not the SAME contact. The Young headline classifies its index sets — `P`
exactly the skew cell posets — whereas here no class of `P` is named, and the 28 intervals
yield 17 distinct `P` of which 5 are not skew cell posets."*

**The verdict on row 10 does not move**: it stays **ADJACENT**, for the reason mg-41aa gave
(a different monoid) and not the reason it withdrew.

---

## 3. F3 — a control that could not fire on the thing it appeared to certify

**AS WRITTEN** — `code/branching_repair_41aa/run_all.sh` and that directory's `README.md`
say the `n = 8` number *"is computed, not copied"*.

**THE EVIDENCE THAT EXISTS.** The chain was open at one link. The `360` that reaches the
document and `code/branching_af28/out_young.txt` comes from `cited_skew = {7: 149, 8: 360}`,
typed into `t_young.py`; `check_doc.py` certified that row against its **own** typed
`(8, 12, 360)`; the `SKEW8_COUNT` pipe in `run_all.sh` fed only `r1_exactly.py`'s table.
So nothing compared the **computed** 360 with the **published** 360.

**AS NARROWED — the control was closed instead of the sentence.** F3 is the one of the four
where narrowing the prose would have been the wrong repair: the sentence *"computed, not
copied"* is what we want to be able to say, and one line makes it true. `check_doc.py` now
reads the machine-readable `SKEW8` line off `out_r1b_skew8.txt` — the same line `run_all.sh`
already feeds to `r1_exactly.py` — and compares it with the row it certifies. A missing or
unreadable file is a **failure**, not a skip.

**AND THE NEW CONTROL IS EXERCISED IN BOTH DIRECTIONS**
(`code/branching_warrant_dffa/out_w4_control.txt`), because adding a control that cannot fire
either would be the same defect:

| | tree | expected | got |
|---|---|---|---|
| **W4a** | faithful copy | exit 0 | exit 0, no failures |
| **W4b** | `SKEW8 360` → `SKEW8 361` | exit 1, **only** the new check named | exit 1, exactly `['the COMPUTED n=8 skew count equals the one out_young.txt PUBLISHES']` |
| **W4c** | `out_r1b_skew8.txt` deleted | exit 1 | exit 1 |
| **W4d** | **pre-repair** `check_doc.py` (from `504ab6c`) on `SKEW8 361` | **exit 0** — else F3 was wrong | exit 0, no failures |

**W4d is the pre-repair predicate**, and it is the check that makes this a repair rather than
a decoration: the old file really does pass while the computed count says 361 and the
published one says 360.

**The number never moved.** 360 is what `r1b_skew8.py` computed; the skew class counts
re-derived here agree at every `n` this instrument reaches (1, 1, 2, 5, 11, 26, 62 for
`k ≤ 6`, matching af28's T2 column). What changed is whether anything would notice if it did
move.

---

## 4. F4 — the premise the headline stands on was inside a STRUCK block

The strongest new sentence mg-41aa wrote is *"Brown's OWN §4.3 example lattice IS a Young
interval"*. It has two premises:

* **(a)** Brown's worked `§4.3` example is the `p × q` grid of lattice paths;
* **(b)** that grid is the interval `[(q), (q+p, q)]` of Young's lattice.

**(b) is measured** — 25 pairs by mg-41aa, 36 by mg-5800 from three definitions, 0 bad.
**(a) is a locating claim about Brown (2000)**, and after the repair it appeared in the
document **only** inside the block quote marked **STRUCK**, under live prose saying the
correction *"removes the sentence"*. Nobody in this arc had read Brown for it: **B8 is a
keyword census, not a reading.**

**AS WRITTEN** — the live text carried the conclusion and struck text carried the premise.

**THE EVIDENCE THAT EXISTS — now, because it was gone and got**
(`code/branching_warrant_dffa/out_w3_brown.txt`). mg-5800's stated fix was one clause: either
re-affirm (a) outside the strike, or attach *"on mg-af28's reading, which nobody in this arc
has re-read"* to the headline. **The second is a hedge on the premise of the headline, which
this ticket forbids, and (a) is a claim we actually want.** So it was read.
`arXiv:math/0006145` was downloaded and its content streams extracted with the same
pure-Python reader af28's `scan_brown.py` uses, and these were located **by position**:

* the `§4.3` heading — *"4.3. Distributive lattices"* — exactly once;
* the `§4.4` heading — *"4.4. The kids walk"* — exactly once, after it;
* **strictly between them**, and exactly once in the whole paper, *"As an example of a
  distributive lattice, consider the product `{0,1,…,p} × {0,1,…,q}` of a chain of length p
  by a chain of length q"*;
* in the same span, *"The maximal chains are the lattice paths from (0,0) to (p,q)"*;
* and **exactly one** occurrence of the word *example* in the whole of `§4.3`, so *"the §4.3
  example"* denotes something.

**AS NARROWED — re-affirmed, at the width of what was read.** A live paragraph in §0
consequence 3, outside the struck block, states (a) and (b), attributes (b) to its two
measurements, gives Brown's sentences as above, and closes: *"What is now read is `§4.3` and
the opening of `§4.4`, and nothing else: the rest of Brown (2000) remains unread by this arc
and B8 remains a keyword census."*

**One clause deliberately kept narrower than it could have been.** Brown prints **no size**
for the lattice. He counts the chains `0̂ < x < 1̂` at `(p+1)(q+1) − 2`, which agrees with
`|L| = (p+1)(q+1)`. That size follows from the definition of a product of two chains; Brown's
line corroborates it and is not the source of it, and both the probe and the document say so
rather than crediting Brown with a count he did not print.

---

## 5. WHAT WAS CHECKED BEFORE THESE SENTENCES WERE WRITTEN, ENUMERATED

The instrument is `code/branching_warrant_dffa/` — seven Python files and a runner, with a
42-assertion self-test, importing
nothing from `branching_af28/`, `branching_audit_6ad0/`, `branching_repair_41aa/` or
`branching_audit_5800/`. Where it cites one of those it reads their **committed output**, and
says so.

1. **The canonical form.** `canon` is the plain minimum over all `n!` relabellings — no
   refinement, no heuristic ordering. mg-5800 recorded a control firing on its own canonical
   form (a colour class chosen by dict-insertion order, with A000112 coming out exactly to
   16 999 while the bug was live), so this repair pays for the definition rather than a
   shortcut. Checked invariant under 6 random relabellings of every cell poset to `n ≤ 6`,
   checked to separate all 5 posets on 3 elements, and checked against brute-force
   isomorphism testing on every pair of 4-cell skew shapes.
2. **The Young–Fibonacci cover rule.** `DU − UD = I` as an operator identity, 0 bad on every
   word of rank < 7; the down-covers checked to be exactly the inverse of the up-covers on
   every word. **Two wrong rules were written before the right one and both reproduced the
   Fibonacci rank sizes** — the first failed the operator identity on 10 words checked to
   rank 6, the second on 22 words checked to rank 7 (two different bounds, because that is
   what each was run at; they are not a comparison). The self-test
   asserts that a wrong rule passes the rank-size check and fails the operator check, so the
   distinction cannot quietly rot.
3. **Distributivity, both directions.** M3 and N5 are required to come out non-distributive;
   `J(P)` is required to come out distributive for every `P` to `n ≤ 5`; a non-lattice (the
   2+2 bowtie) is required to be rejected as a lattice at all.
4. **Skew-shape membership, both directions.** Every straight `D_λ` to `n ≤ 4` and the
   3-antichain must be **in**; three minimal elements under a common top must be **out** —
   and that object is separately checked to be a genuine 4-element poset with 9 order ideals,
   so the negative is a real refusal and not a malformed input. The search box is grown from
   `k` to `k+1` and the class **set** required to be identical.
5. **B1's lattice isomorphism, re-measured** (F1a): 44 partitions, 5 464 ordered pairs, meet
   and join, 0 bad, both sides from independent definitions.
6. **The claim that af28 under-states and over-labels off one test** (F1a): checked
   mechanically against `t_young.py`'s source and `out_young.txt`, not by eye.
7. **B5's two re-derivations** (F1b): located as strings in two committed outputs, with
   mg-6ad0's 67/20/87 read out of its own table — and read out of the **A4a** section
   specifically, after an unscoped regex silently summed A4a's table with A4b's and returned
   174 classes where the whole population is 87. That error was in this repair's own probe
   and was caught by an internal-consistency assertion (`classes == tested + skipped`).
8. **Every F2 figure, re-derived** (F2): 33 / 5 / 28, witness `221`, 17 distinct `P`, 5 not
   skew, 2 at `|P| = 5` and 3 at `|P| = 6`, 30 of 30 on the Young side.
9. **The new `check_doc.py` line, fired in four configurations** (F3), including the
   pre-repair predicate, which must **pass** the mutation for F3 to have been a real finding.
10. **Brown `§4.3`, read** (F4), located by position between two section headings.
11. **The document itself, after editing** (`out_w5_doc.txt`, 41 checks): the eight narrowed
    or widened phrasings must be **present**; the four wide phrasings mg-5800 quoted must be
    **absent everywhere**; and mg-41aa's six struck quotations must still occur **exactly
    once each, in a block still carrying a strike marker** — this repair must not disturb the
    previous one.
12. **mg-41aa's own `check_doc.py` re-run against the edited document**: 31 checks, 0 failed.

**A note on why the wide phrasings are deleted rather than struck in place.** mg-41aa's
discipline is to quote every sentence it strikes where it stood, because those sentences were
**false** and the reader needs to see what was withdrawn. F1–F4 are not false sentences; they
are true sentences stated too wide, and a too-wide sentence quoted in place still reads as an
assertion. So they are edited, and this document carries the before-and-after instead. That
is a deliberate departure from the target document's convention and it is stated rather than
performed silently.

---

## 6. WHAT THIS REPAIR DID NOT ESTABLISH, SAID RATHER THAN LEFT TO BE DISCOVERED

* **B5's step is not re-derived here.** It is attributed to mg-6ad0 and mg-5800 and their
  outputs are located. A third derivation would be evidence-gathering this repair was told
  not to do.
* **Brown (2000) is still substantially unread.** `§4.3` and the opening of `§4.4` were read.
  Nothing here licenses any claim about any other section, and **B8 remains a keyword
  census** — its row is unchanged.
* **The converse of X1 beyond `n = 6`** is where mg-5800 left it. Untouched.
* **Bergeron–Li conditions (3), (4), (5)** under the `§3.6` weakening remain untested by
  anyone. Untouched.
* **mg-6ad0's X5, X6, X7** remain deliberately unlanded; see the target document's §9.
* **The label `lattice-iso bad` in `code/branching_af28/`** is recorded and **not fixed**.
  Fixing it means rewriting a committed output that mg-5800 re-ran byte-identical, which is
  outside this brief.
* **mg-5800's F5** is an observation, not a defect, and is not landed: `§3.6`'s *"semi-tower"*
  wording narrows *"two tower definitions"* toward *"a tower definition and a sketched
  semi-tower variant"*, but row 3 is a hedge either way and X3's conclusion does not move.
  Named here so the next reader does not have to re-derive that it was considered.

---

## 7. REPRODUCE

```
cd code/branching_warrant_dffa && ./run_all.sh    # ~5 s, pure Python 3
cd code/branching_repair_41aa && python3 check_doc.py   # 31 checks, 0 failed
```

`w3_brown.py` is the only step needing network; if the download fails it says so and exits 0,
and the committed `out_w3_brown.txt` records the run that was made.

**One thing about the committed outputs, stated because it is a partial run.**
`code/branching_repair_41aa/out_check_doc.txt` was regenerated by running `check_doc.py`
alone, not by re-running that directory's whole `run_all.sh`. Its output is a function of
three files on disk — the document, `out_young.txt` and `out_r1b_skew8.txt` — none of which
this repair regenerated, so the result is the same either way; but a reader comparing
timestamps should know which command produced it. **No other file under
`code/branching_repair_41aa/`, `code/branching_af28/`, `code/branching_audit_6ad0/` or
`code/branching_audit_5800/` is touched.**

---

## 8. SCOPE

No `STATE.md` edit. No edit to row Q or to the landscape document. Nothing about `λ₂`,
`Δ_AT`, pricing or publishability. No new mathematics: every measurement here re-derives a
figure that already existed, except the 17-distinct-`P` / 5-non-skew split, which mg-5800
measured first and this repair reproduces. Not relayed to Daniel.
