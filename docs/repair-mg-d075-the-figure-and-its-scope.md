# mg-d075 — the figure and its scope: EIGHT IS NOT THE POPULATION EITHER

**Work item:** mg-d075. **Parent:** mg-19ec (whose verdict was recovered from commit
messages and never routed). **Pre-filed independent audit:** mg-aaf4, which is instructed
not to take my numbers on trust. **Date:** 2026-08-05. **Instrument:**
`code/branching_bound_d075/` — 6 scripts, a self-test, a runner, and a predictions file
committed at `ec98300` before any script of this repair existed.

---

## 0. THE HEADLINE

**mg-19ec found that `docs/OneThird-Branching-Graphs-Where-This-Lives.md` states the
33-interval Young–Fibonacci figure — the 33 intervals `[0̂, w]` with `rank(w) ≤ 6` — at 8
live sentences and bounds it at 4. Counted again,
over the same file with the same liveness rule and the same sentence grain, the population
is 9 and the unbounded count is 5.**

The ninth site is the row-10 sentence of §3:

> *Row 10 therefore has an index-set contact of the **same kind** as the one this document
> headlines for Young's, on 28 of 33 intervals; …*

It states the figure. It is about Young–Fibonacci intervals. It carries no rank bound.
mg-19ec's POP-3 predicate could not see it, because that predicate requires the string
*"Young–Fibonacci"* to appear **in the same sentence as the numeral**, and this sentence
says *"for Young's"* instead.

**And mg-19ec already had it.** The POP-1 block of the same transcript
(`code/branching_audit_19ec/out_e5_population.txt`) prints this exact sentence as its `[09]`
and scores it unbounded. So the ninth site is not new evidence: it is one audit's two
instruments disagreeing with each other across 1 site, and only the smaller of the two
numbers reaching the verdict.

**All 9 are now bounded, and so is this repair's own note.** Nothing is deleted, no measured
number is withdrawn, and every one of the 9 pre-repair sites is matched site-for-site in the
post-repair population of 10 — see §3.

---

## 1. THE COUNT, WITH ITS POPULATION AND GRAIN

Every number in this document is stated with the population it is over and the grain of the
value, because the defect being repaired is figures stated without either.

| population | definition | grain | sites | bounded | unbounded |
|---|---|---|---|---|---|
| **A** STRICT / one doc | live sentences of `OneThird-Branching-Graphs-Where-This-Lives.md` where the **sentence** contains the figure `33` — the interval count at `rank(w) ≤ 6` — **and** the **sentence** names Young–Fibonacci; mg-19ec's own POP-3 predicate | one sentence | **8** | 4 | 4 |
| **B** RELAXED / one doc | the same, with attribution allowed from the **table cell or paragraph** the sentence sits in — exactly one conjunct of A relaxed | one sentence | **9** | 4 | **5** |
| **C** ceiling / one doc | B with the liveness rule dropped: struck and block-quoted units admitted | one sentence | 10 | 5 | 5 |
| **D** corpus | B over the **101 `docs/*.md`** that are not this repair's own | one sentence | **29** in 6 files | 12 | **17** |

All four are pre-repair values, printed side by side with the post-repair ones by
`s1_census.py` (`out_s1_census.txt`), the living document rolled back to the derived anchor
`645b5a4` and the other five corpus files read as they stand. A and B are the two that matter: **B is A plus one site,
and retracts nothing.** `s2_reproduce.py` establishes that before it establishes anything
else — mg-19ec's published 8 / 4 / 4 is reproduced row-by-row against its own committed
transcript, all 8 line numbers and all 8 verdicts, by a re-implementation that imports none
of its code. A disagreement with a published figure is worth nothing until the published
figure has been reproduced.

**FOUR was not the population, and EIGHT is not either.** The brief for this repair told me
not to inherit 8; mg-aaf4 is told not to inherit 9. It should not.

---

## 2. WHAT WAS BOUNDED, AND WITH WHAT

Five sentences were unbounded. Each now carries a **numeric scope in its own sentence** — not
a softening word, and not a bound sitting helpfully in the next sentence.

| § | site, pre-repair | what was added |
|---|---|---|
| §2 heading note | *(the version this replaces)* *"**28 of the 33** finite Young–Fibonacci intervals are distributive"* | the family named: *"the **33** intervals `[0̂, w]` of Young–Fibonacci with `rank(w) ≤ 6`"* |
| §2 mg-dffa note | *(the version this replaces)* *"so "28 of the 33 are `J(P)`" says precisely "28 of the 33 are distributive""* | the family factored out once, bounded: *"of the **33** intervals `[0̂, w]` with `rank(w) ≤ 6`, "28 are `J(P)`" says precisely "28 are distributive""* |
| §3 row 10 | *(the version this replaces)* *"on 28 of 33 intervals"* | *"on 28 of the 33 Young–Fibonacci intervals `[0̂, w]` with `rank(w) ≤ 6`"* |
| §9 ledger B4 | *(the version this replaces)* *"30 Young intervals, 0 non-distributive; 33 Young–Fibonacci intervals, 5 non-distributive"* | both families scoped: `λ` of size ≤ 6, and `rank(w) ≤ 6` |
| §9 ledger B4′ | *(the version this replaces)* *"**28 of 33** Young–Fibonacci intervals are distributive"* | *"**28 of the 33** Young–Fibonacci intervals `[0̂, w]` with `rank(w) ≤ 6`"* |

`s4_hedge.py` prints, for each of the sites, the **exact substring** carrying the bound and
classifies it NUMERIC SCOPE or SOFTENING WORD. **10 of 10 are numeric scopes.** It also takes
the **14** sentences this repair introduced into the living document and scans each against
**33 hedge tokens** — mg-19ec's own 25 verbatim, plus 8 this repair adds, `kind` and `some`
among them on purpose because they are the tokens a bounding repair is most tempted to lean
on. **3 of the 14 carry a hedge token, and all 3 state numerically what falls inside it** —
the standard mg-19ec set when it defended *"of the same KIND"* by enumeration rather than by
assertion. That is a **refutation of this repair's own P7**, which predicted the count of
hedged new phrasings would be 0; see the README's scorecard.

### 2.1 THE SHARPEST SITE — the criticism that was itself unbounded

The brief singled this out and it deserves the space. §2's mg-dffa note faults
Young–Fibonacci for **naming no class of `P`** — and stated the **Young** classification it
was contrasting against with no bound at all, over a family this repo has measured at
exactly **30 intervals `[∅, λ]` with `|λ| ≤ 6`** and nowhere beyond:

> *The Young headline is a **classification** — the intervals of Young's lattice are `J(P)`
> for `P` **exactly** the skew cell posets, a named closed class …*

A sentence criticising another for unbounded naming, unbounded. **Bounding only the
Young–Fibonacci half would have left the defect exactly where it was**, so both halves were
bounded: the Young half now carries the measurement that actually carries it — **30
intervals with `|λ| ≤ 6`, 30 of 30 distributive, 30 of 30 with `P` a skew cell poset, 0
outside the class**, with the underlying isomorphism checked over **44 partitions to
`n ≤ 7`** (`code/branching_warrant_dffa/out_w2_family.txt`, `code/branching_af28/`).

---

## 3. WHAT THE GATE CHECKS, AND WHAT IT CANNOT

`s3_bound.py` is the standing gate. It reads the pre-repair document **out of git at an
anchor it derives** (the newest commit touching the file whose subject does not name
mg-d075), so it survives rebases and this branch landing on main.

- **G1** — 0 unbounded, under **both** predicates, reported as a fraction with its
  denominator.
- **G2** — every pre-repair site still present, matched by shared vocabulary rather than by
  line number, so *0 unbounded* cannot be reached by deleting sentences. Sites this repair
  **adds** are printed in full and must be bounded themselves.
- **G3** — no measured figure disappears; each fall in an occurrence count is adjudicated at
  the matched site that caused it.

`selftest_d075.py` breaks the repaired document **17 times** — once at each of the 10 sites,
plus 3 hedge substitutions, a deletion, a block-quoting, a strike and an injection — and
requires the gate to notice each — including the one that matters most: **replacing a bound with `roughly` /
`essentially` / `broadly` must NOT score as a bound.** Every mutation asserts
`mutated != original` before asserting the verdict moved, so no green row can rest on a
corruption that was a no-op.

**What the gate cannot do:** it runs over one file. See §5.

---

## 4. THE DEFECTS THIS REPAIR'S OWN INSTRUMENTS FOUND IN THIS REPAIR

The brief said: *"Whoever repairs this should expect to do the same thing somewhere in the
repair, and should look for it deliberately."* `PREDICTIONS.md` P9 committed to that in
advance. Here is what was found, and none of it is retro-fitted:

1. **A bound written into the NEXT sentence rather than its own.** Bounding the Young
   classification, I first attached the `|λ| ≤ 6` measurement after a semicolon — and the
   sentence splitter this repair inherits treats `; **` as a sentence boundary, so the
   criticism clause stood alone and unbounded with the bound one sentence away. That is the
   §2.1 defect reproduced by me, at the finest grain, in the act of repairing it. Caught by
   re-running `s1_census.py` on my own edit before committing it.
2. **A markdown table broken by the bound itself.** Writing `|λ| ≤ 6` inside a table cell
   split ledger row B4 into extra cells: the pipe is the column separator. `s3_bound.py`'s
   G3 caught it as the figure `30` vanishing from the site population. Rewritten as
   *"`λ` of size ≤ 6"*, with no pipes.
3. **My own repair note, unbounded.** The note added at the head of the document states the
   33-interval figure — so it joins the population it describes, and the first version of it
   carried no scope. It also asserted *"the population is 9 before and after"*, which its own
   note had already made false. Both fixed; the current count is printed by the instrument
   rather than asserted in prose.
4. **A grain mismatch in my own output.** `s4_hedge.py` printed *"live sentences before:
   297, after: 316"* — a `set` compared against a `list`. Distinct-vs-occurrence, in a
   repair about population and grain. Both are now printed, labelled.
5. **Two checks respecified after they fired on me**, recorded because silently loosening a
   check that fires is exactly what these audits exist to catch. G3's first form forbade any
   integer occurring fewer times, and fired on the deliberate factoring of two unbounded
   *"of the 33"* restatements into one bounded statement; G2's first form demanded the
   population be the same size, and fired the moment this repair recorded itself in the
   document. The first-form transcript is committed as
   `code/branching_bound_d075/out_s3_bound_FIRSTFORM_exit1.txt`. **The reasoning is in the
   code at the point of the check, not only here.**
6. **A line-number identity that was not one.** G3's per-site adjudication first keyed on
   line numbers and reported 4 sites as having lost a figure — every one an artefact of the
   repair shifting lines below its own edits.

---

## 5. INSTANCE OR CLASS — the honest answer

`s6_class.py` measures it rather than posturing, against a rule stated in the code before
the answer is computed.

- **All 3 prior instances the brief names are present as artefacts in this tree** —
  mg-2c77 (4 commits, `code/audit_2c77`), mg-7e39 (6 commits,
  `code/hodge_leverage_audit_7e39`), mg-19ec (10 commits, `code/branching_audit_19ec`).
- **The corpus of this figure is now 7 files of `docs/`, 36 sites** (7 rather than 6 because
  this repair's own account document states the figure and therefore joins the population it
  describes). **My gate covers 2 of the 7** — the living document under G1–G3 and this
  document under G4. After this repair **12 sites remain unbounded, every one of them in the
  5 files this repair does not touch**, and they are named with their counts in
  `out_s6_class.txt`.
- **The predicate is path-parameterised** — the 7-file table is the demonstration, one call
  per file, zero edits.

**VERDICT: INSTANCE + REUSABLE ARTEFACT. Not the class.** That string is computed by
`s6_class.py` from a rule written above the answer, not chosen after seeing it.

The 5 files left alone are audit and repair records written by earlier tickets and dated by
their commits; editing them would destroy the evidence trail this arc runs on. That is a
scope decision, taken in `PREDICTIONS.md` P5 before the corpus was counted, and it is stated
here rather than left as a silent omission.

**And the part no artefact fixes.** The three prior instances are not three occurrences of
one bug in one file. They are one **habit** — writing a figure and its scope in different
places, or the scope nowhere — committed by three different authors in three different
subsystems. A path-parameterised predicate can be pointed at a fourth document; it cannot be
pointed at the habit. What would address the class is a check that runs over every document
in this repo on every commit. **This repair does not install one.**

---

## 6. HANDED TO mg-aaf4, NOT SCORED AGAINST THIS REPAIR

Two figures of the predecessor's, measured by `s4_hedge.py`'s H4 and left alone otherwise:

- `docs/OneThird-Warrant-Repair-mg-dffa-IndependentAudit.md` states, **twice**, that the
  phrasings were scanned *"against 26 hedge tokens"*. The `HEDGES` list in
  `code/branching_audit_19ec/e2_f2_clauses.py` has **25** entries, and that audit's
  transcript never prints a token count at all — so **26** is a hand-written literal no
  instrument computes.
- The phrasing population is **15** in the transcript and in the published audit, and **13**
  in the recovered verdict that reached mg-d075's brief.

Both are the same shape as the defect this repair lands. **Neither is repaired here** —
mg-19ec's audit document is a dated record — and neither is scored against this repair: a
finding against a predecessor is not a reason for a successor's gate to fail.

---

## 7. PREDICTIONS — kept as written

`code/branching_bound_d075/PREDICTIONS.md`, committed at `ec98300` **before any script of
this repair existed**, with a full disclosure of the 10 hand commands run before it was
written. **12 predictions and 9 exit values: 10 predictions held, 2 were REFUTED, and 9 of 9
exit values matched.** The two refuted are P6 (which predicted the population would still be
9 after the repair — it is 10, because this repair's own note joined it) and P7 (which
predicted 0 new phrasings would carry a hedge token — 3 of 14 do, all of them rescued by
enumeration under mg-19ec's own standard). The scorecard is
`code/branching_bound_d075/README.md` §7. **No prediction in that file was revised after a
run, and neither refutation was argued away.**
