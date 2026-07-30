# Independent audit — the FINAL STATE of the species / Hopf-monoid document

**Work item:** mg-73df. **Date:** 2026-07-30. **Subject:** `83ac472` (mg-6f61) **+**
`a13b4a9` (mg-f8fa), i.e. `docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md` as a
reader meets it, together with `code/species_7d75`, `code/species_repair_6f61` and
`code/species_remainder_f8fa`.
**Instrument:** `code/species_audit_73df/`, `run_all.sh`, ~100 s, NO NETWORK,
5 384-assertion self-test anchored to A001035 / A000670 / A000110 / A000112 / A000041 /
A000142, sharing no code with any of the three trees it audits.

---

## 0. THE VERDICT

**THE REPAIR IS REAL, IT WENT THE RIGHT WAY, AND NOTHING RETREATED.** §0 was brought
**up** to §5 and not §5 down to §0; the headline is still a theorem; the poset half is
still 87/87 with no cap and 179/179 out of sample; control (ii)'s conclusion is not
merely un-withdrawn but strengthened from a count on `[4]` to a statement about the two
maps' types at every ground set. All four of mg-f8fa's brief items are done. Every
figure I checked reproduces, and `code/species_7d75`'s seven committed outputs
regenerate **byte for byte**.

**0 BROKEN.** Nothing in the final state is mathematically false.

**1 MAJOR, and it is the audited work's own finding arriving one iteration later.**
mg-f8fa's §14.3 says the fix for a checker that misses things is *"one line of scope:
the checker must take the code directory as a target too"*. **The scope was widened.
The LIST was not.** `w3_scope.py` enforces two of mg-6f61's eight corrections, reports
`PASS (0 problems)`, and **two others are still in force in `code/species_7d75`** — one
of them **X3, the repair's own central defect**, and it is in a committed output inside
a run ending `T6 TOTAL BAD: 0`. Both sentences are named **verbatim in
`check_doc.py`'s own `STRICKEN` table**, so this is not a correction anybody forgot to
make; it is one that was enumerated as stricken and then enforced in one file only.

**4 MINOR**, three of them at the **seam** between the two repairs, which is where this
brief predicted the finding would be and where it was.

| # | severity | what |
|---|---|---|
| **Y1** | **MAJOR** | X3 and the AM §17.5 quotation are corrected in the document and **still asserted at source**, in `t6_fock_and_record.py`; `w3_scope.py` cannot see either |
| **Y2** | MINOR | §0's headline box says the left side **is** Solomon's descent algebra; four other places in the document, and AM Thm 10.13 as §0 itself quotes it, say **anti**-isomorphic — and T3d measures the plain reading to fail by **472** structure constants |
| **Y3** | MINOR | §14 carries its self-assessment limitation **twice**, 56 % similar and **not in agreement**; one copy miscounts the banner it cites |
| **Y4** | MINOR | §14.2 calls mg-f8fa's filing *"a second, **shelved** filing"* — §14.3, eleven lines below, is that filing's own record |
| **Y5** | MINOR | two instruments' docstrings disagree with their own committed runs: `w3_scope.py` says **6** problems where its evidence file says **12**; `r2_columns.py` says **40** cells where it prints **45** |

---

## 1. WHAT I CHOSE TO AUDIT THAT NO LIST NAMED, AND WHY

The brief says its own list is a floor and asks for at least one deliberate
beyond-list target, named. I picked four, and **three of the five findings came from
them**:

1. **The corrections at source, scanned for ALL EIGHT rather than the three mg-f8fa
   named.** Chosen because §14.3's stated fix widens the *target* of a checker, and the
   obvious next question — the one its own reasoning raises and does not ask — is what
   the *list* misses. → **Y1**.
2. **§0's headline box, word by word, against the body.** Chosen because §0-vs-body is
   the exact shape of X3, the defect this repair existed to fix, so §0 is precisely
   where a recurrence would sit and precisely where nobody would look twice. → **Y2**.
3. **A duplicate-passage sweep over all 17 block quotes in the document.** Chosen
   because two workers editing one file is what a seam *is*, and saying the same thing
   twice in two versions that disagree is what a seam produces. → **Y3**, **Y4**.
4. **Whether the measuring routine itself skips.** Chosen because *"three columns
   cannot fail"* is only a result if the routine actually evaluates them; if it skipped
   tests whose intermediate values leave the collection, the `0` would be vacuity and
   *"cannot fail"* would be a statement about the instrument. It does not skip — this
   one came back clean, and it is reported as a **negative result** rather than left
   unsaid (`C2a`).

---

## 2. Y1 — MAJOR: THE SCOPE WAS WIDENED, THE LIST WAS NOT

### What is still in force

`code/species_7d75/t6_fock_and_record.py`, unmarked, with no repair named within six
lines:

| line | what it says | what the document says |
|---|---|---|
| **149–150**, and **`out_t6_fock_and_record.txt`:66–67** | *"That same concatenation **IS** `mu_{S,T}`, and T5 measured it against **every Hopf monoid axiom** with **0 failures on 4399 basis elements**."* | §0 **strikes** *"~~it passes every Hopf-monoid axiom with 0 failures on 4 399 basis elements (T5)~~"* and replaces it with *"what 4 399 basis elements measure is CLOSURE, and only closure … two can fail on our subspecies and three cannot"* |
| **15–16** | *"Recall from Section 17.4 that `K-bar(Pi)` is the algebra of symmetric functions in noncommuting variables and `K(Pi)` is the familiar Hopf algebra of symmetric functions"*, introduced as *"Section 17.4 is quoted in Section 17.5 as:"* | §4 **strikes** that exact string and records *"**The book's species is `Π*` in both slots**"* |

**The X3 one is in a committed output**, so it is not only in a file a successor reads
— it is in a run that ends `T6 TOTAL BAD: 0`, which is the property §14.3 identifies as
the reason the last three went unnoticed: *"a passing checker is read as coverage."*

### Why this is not a missed correction but an unenforced one

`code/species_repair_6f61/check_doc.py` lines 55–72 declare `STRICKEN`, and **both**
sentences are in it, verbatim, with their section numbers:

```
    ("§0, the five-axiom count",
     "it passes every Hopf-monoid axiom with 0 failures on 4 399 basis elements (T5)"),
    ...
    ("§4, the AM §17.5 quotation",
     "Recall from Section 17.4 that `K̄(Π)` is the algebra of symmetric functions in
      noncommuting variables and `K(Π)` is the familiar Hopf algebra of symmetric
      functions"),
```

mg-6f61 enumerated six stricken sentences and enforced them **in one file**. mg-f8fa
moved the enforcement into the code and **narrowed the list to two** —
`w3_scope.py`'s `FORBIDDEN` table has exactly `X4` and `X5`. Six stricken sentences,
two enforced; the two unenforced ones that also live at source are still there.

### Demonstrated, not argued

`c4_scope.py` scans all eight corrections across three trees, with four controls:

```
  w3_scope.py against code/species_7d75 : W3 SCOPE: PASS   (0 problem(s))
  this file against the same tree       : 4 statement(s) still asserted
      X3      out_t6_fock_and_record.txt:66      X6/X7   t6_fock_and_record.py:15
      X3      t6_fock_and_record.py:149          X6/X7   t6_fock_and_record.py:16
```

* **control (a)** — the same detector on the pre-repair tree at `83ac472` reports **8**
  still asserted against **4** now, and catches X4 and X5 there, the two `w3_scope`
  covers. So the detector detects.
* **control (b)** — `w3_scope.py` PASSES the tree this detector has four hits on. That
  is the coverage gap measured rather than asserted.
* **control (c)** — the document claims `w3_scope` *"fails if a ninth is added
  unmarked"*. I added a ninth to a scratch copy: `9 occurrence(s) checked` /
  `W3 SCOPE: FAIL (1 problem)`. **The claim is true.**
* **control (d)** — injecting *"three are controls"* into a scratch copy raises this
  detector from 4 to 5. So it is not reporting a fixed number.

`code/species_repair_6f61` and `code/species_remainder_f8fa` — the two trees nobody
points a checker at — come back **0 still asserted**, reported as a negative result.

### Severity, and the honest half

**MAJOR, not BROKEN.** Neither sentence is *false*. The 4 399 and the 0s are right; the
AM §17.5 quotation differs by `Π` vs `Π*`, which §17.4.1 makes harmless and which the
document says so. What is wrong is that both are the **overstated form the document
formally withdrew**, left in force in the copy a successor re-runs, invisible to the
checker built for exactly that, inside `TOTAL BAD: 0`.

**And mg-f8fa said this would happen, accurately, in its own commit:** *"No independent
search for defects mg-a61f and mg-6f61 both missed was conducted."* That sentence is
correct and it is the reason for Y1. The finding is not that the repair claimed
coverage it lacked — it is that **the document's banner does**: *"`w3_scope.py` is the
checker for the instrument"*, unqualified, where it is the checker for two of six.

**Suggested fix, one line and no new mechanism:** move `check_doc.py`'s `STRICKEN`
table into `w3_scope.py`'s `FORBIDDEN`, so the two checkers enforce one list over two
targets instead of two lists over one target each.

---

## 3. Y2 — MINOR: §0 STATES THE READING ITS OWN §2.2 MEASURES TO FAIL

§0's headline box, line 87:

> * **`P` the antichain, `Aut(P) = S_n`** → the left side **is Solomon's descent
>   algebra** …

Four other places in the same document say otherwise, one of them thirty lines below
the box, in §0 itself:

| where | what it says |
|---|---|
| §0, quoting AM Thm 10.13 | *"The descent algebra is isomorphic to `(Σ[n]^{S_n})^{op}`"* |
| §2.2 | *"The identification is an **anti-isomorphism**"* — `iso/A` fails by **4, 54, 472** |
| §9 row 3 | *"verified as an **anti**-isomorphism"* |
| ledger **S2** | *"`(kΣ_n)^{S_n}` is **anti**-isomorphic to Solomon's descent algebra"* |
| §9 row 8, quoting Saliola | *"the invariant subalgebra is **anti**-isomorphic to Solomon's descent algebra"* |

I rebuilt both algebras from their definitions and reproduced T3d entry for entry —
`0 / 0 / 4 / 54 / 472` for `iso/A` and `0` throughout for `anti/A` — and T3e's
opposite-algebra identity with its control (`0` everywhere; the un-swapped control fires
**2, 26, 170** at `n = 3, 4, 5` and cannot fire below, where `kS_n` is commutative).

**Is it loose wording or false?** Decidable: if the two were anti-isomorphic *and*
isomorphic then `Sol(S_n) ≅ Sol(S_n)^{op}`, and then `dim {x ∈ J : Jx = 0}` and
`dim {x ∈ J : xJ = 0}` must agree, since an isomorphism preserves the first and an
anti-isomorphism exchanges them. Computed exactly over `ℚ`, radical by Dickson's
criterion:

| `n` | `dim` | `dim rad` | `{x ∈ J : Jx = 0}` | `{x ∈ J : xJ = 0}` |
|---|---|---|---|---|
| 3 | 4 | 1 | 1 | 1 |
| 4 | 8 | 3 | 2 | 2 |
| 5 | 16 | 9 | 5 | 5 |

(`dim rad = 2^{n-1} − p(n)` throughout, which is the check on the radical routine.)
**Not refuted.** So this invariant does not separate `Sol` from `Sol^{op}` at `n ≤ 5`,
and I report Y2 as **wording, deliberately not as BROKEN**.

It still matters, and it is the reason I looked: §0 asserting what the body measures to
fail is **X3's exact shape**, in the same section, surviving a repair whose stated job
was to remove it. **The fix is one word:** *"the left side is the **opposite** of
Solomon's descent algebra"*, or *"is anti-isomorphic to"*. Nothing downstream moves —
the radical quotient is commutative, so the `op` is invisible after `/rad`, which is
presumably why it was written this way.

---

## 4. Y3 / Y4 — MINOR: THE SEAM

`c5_doc.py` compares every block quote in the document with every other. One pair
crosses the threshold, at **56 % similarity**:

* **lines 1010–1019**, an unheaded box at the end of §14, and
* **lines 1047–1058**, the whole of **§14.2**, which is titled
  *"The limitation that applies to this section"*.

Both open with *"THE SAME LIMITATION APPLIES TO … AND IT IS STATED HERE RATHER THAN
LEFT FOR THE NEXT AUDITOR TO FIND"*. **They do not say the same thing.**

| | first copy (1010–1019) | second copy (§14.2) |
|---|---|---|
| what mg-6f61's list is | *"the **five items in the banner at the top**"* | *(no count)* |
| where it came from | mg-a61f alone | mg-a61f *"**plus four folded in from a second, shelved filing**"* |
| how complete | *"only to the extent that **mg-a61f's audit** was"* | *"only to the extent that **those two** were"* |
| the direct evidence | *(absent)* | *"two readers of one audit produced two different lists, and neither was a subset of the other"* |

Three separate problems, all of them in the section about self-assessment:

1. **It is said twice**, and the second copy is strictly better — it carries the
   evidence and the honest two-source account. The first is the weaker draft, left
   standing.
2. **The first copy miscounts the thing it cites.** The banner it points at says
   **"Eight things changed."** It calls it five.
3. **§14.3, added by mg-f8fa, answers §14.2 by name** — *"§14.2 predicted that a
   further defect, if one existed, would be outside every beam"* — and reports that the
   eighth defect **was found**. The first copy is left twelve lines above §14.3 still
   saying *"an eighth defect, **if there is one**"*, pointing at nothing.

**Y4** is in the same box and is a second-pass staleness: §14.2 calls mg-f8fa's work
*"a second, **shelved** filing"*. It was not shelved — it was dispatched, it ran, and
**§14.3, eleven lines below, is its record.** The final state describes one filing as
shelved and as executed within twelve lines.

Both were introduced by mg-6f61 (`git show 83ac472` has both boxes) and survived
mg-f8fa, which edited §14 and added §14.3 without reconciling them. **This is exactly
the seam: two correct passes, jointly inconsistent, and neither brief covers it.**

**Fix:** delete the first copy; change *"shelved"* to a phrase that survives the filing
having run.

---

## 5. Y5 — MINOR: TWO DOCSTRINGS DISAGREE WITH THEIR OWN RUNS

| file | its docstring | its own committed run | the document |
|---|---|---|---|
| `species_remainder_f8fa/w3_scope.py` line 25 | *"it reported **6** problems there"* | `out_w3_scope_before.txt`: `FAIL (12 problems)` | §14.3 and **S14**: **12** |
| `species_repair_6f61/r2_columns.py` line 32 | *"predicted-vs-actual for all **40** cells"* | `out_r2_columns.txt`: *"**45** cells"*, `MISSED: 2 of 45` | §5: **45** |

The document and the outputs agree; only the docstrings are wrong. It is small, and it
is in the one place §14.3 argues matters — *"nothing said which files it read"* — a
checker's own account of the run that falsified it. A successor reading `w3_scope.py`
before running it is told the falsification was half the size it was.

---

## 6. WHAT REPRODUCES, AND WHAT DID NOT RETREAT

### Everything runs, and the outputs are byte-identical

| tree | result |
|---|---|
| `code/species_7d75` | 47 s, six scripts, all `TOTAL BAD: 0`, 759-assertion self-test — **seven committed `out_*.txt` regenerate BYTE FOR BYTE** (`git status` clean) |
| `code/species_repair_6f61` | 27 s, `CHECK_DOC: PASS`, `R1/R2/R3 TOTAL BAD: 0`, `R2 PREDICTIONS MISSED: 2 of 45`, 3 188 assertions — byte-identical |
| `code/species_remainder_f8fa` | 4 s, `W3 SCOPE: PASS`, 2 114 assertions — byte-identical |
| `code/species_audit_a61f` re-run **unmodified** | 456 328 assertions, `A4 TOTAL BAD: 1` (which is X1, against the text as originally filed) and 0 elsewhere — **byte-identical**, exactly as `a13b4a9` claims |

`|F| = 4399`, `|AC| = 2685`, `|P × Σ| = 16425` on `[4]` rebuilt from scratch by
`selftest73df.py` and agreeing. **24 of 24** figures I cross-checked are present both in
the document and in the output file the document cites them to.

### The axiom battery, per column, on MY mutations

The brief asks for per-column falsifiability verified with my own mutations, not the
author's. Seven collections and five operation mutations, all chosen here, 60 cells,
**every one predicted before the run**:

| column | fails on a COLLECTION? | fails on an OPERATION? | my witness |
|---|---|---|---|
| product closure | **YES** | **YES** | 626 on odd-block-count; 9 148 on `reverse(concat)` |
| coproduct closure | **YES** | **YES** | 14 938 on odd-block-count; 13 874 on an opposed right factor |
| associativity | **NO** — pinned at 0 | **YES** | 12 192 on `reverse(concat)` |
| coassociativity | **NO** — pinned at 0 | **YES** | 113 076 on an opposed right factor |
| compatibility | **NO** — pinned at 0 | **YES** | 6 110 on the **linked union** |

**This agrees with mg-6f61's R2c on every cell**, reached from mutations that share
nothing with it. My compatibility control is structurally different from the repair's:
mg-6f61's control (v) merges **blocks** and leaves the poset alone; mine adds **order
relations** and leaves the face alone. Both isolate compatibility, and — worth
recording — **compatibility was the only column just one of my five mutations reached**,
which independently corroborates mg-6f61's judgement that §5's four original controls
left it without one.

**Both closure columns return 0 for the full ambient (16 425) and for the deliberately
wrong pairing**, confirmed from my own code. So §5's limiting reading — *"what they
establish is CLOSURE and not IDENTIFICATION"* — is right, and **the repair resolved the
§0/§5 disagreement by bringing §0 up to §5**, which is the direction that makes the
document better. `c5_doc.py` checks the honest paragraph is intact and that every
withdrawn sentence survives only inside its strike or beside a named repair: **15 of 15
required survivals present, 5 of 5 withdrawn sentences properly struck**.

### "Cannot fail on a sub-collection" — swept, and non-vacuously

Five collections do not establish a claim quantified over every sub-collection. I swept
**24** sub-collections chosen by an arithmetic rule with no geometric content:
**72 of 72 pinned cells zero**, each holding on **at least 2 346 evaluated associativity
triples**, with the identical sweep under a mutated product firing on associativity for
**all 24**. And the load-bearing check: neither `axioms` nor my `five_columns` **skips**
a test when an intermediate value leaves the collection, so a `0` there is an identity
and not an absence of testing.

### My four missed predictions, kept as written

`C1 PREDICTIONS MISSED: 4 of 60`. Three of them are one lesson:

* **O2** — a coproduct that is non-zero when **`T`** is a lower set instead of `S`:
  predicted `+` on coassociativity and compatibility, got **0 on all five columns**. It
  is not a corruption at all; it is a legitimate bimonoid structure, joining mg-7d75's
  controls (i) and (iii) as a third *"the corruption produced a different published
  object, not a broken one"*.
* **O3** and **O4** — predicted `+` on compatibility, got `0`. Compatibility is
  genuinely hard to reach, which is the point above.

I report these because a battery that misses nothing is a battery whose expectations
were written afterwards. **Which is also the only honest thing I can say about the
audited battery's ordering:** nothing verifies it mechanically. What I can say is that
`r2_columns.py` reads as a prediction — its rows carry *reasons* rather than outcomes,
its two misses are exactly the two an author writing afterwards would have quietly
fixed, and the miss on the even-block predicate is **against** the repair's own framing
and is published anyway. I ran the mirror test it implies: the repair explains its miss
by *"concatenation ADDS block counts, so parity survives"*, which requires **odd**
block count to fail that column. It does — **626**. The explanation is not
post-hoc.

---

## 7. THE FOUR ITEMS OF THE WIDENED SCOPE, EACH CHECKED

1. **The four hedges on §2.3 — removed, and the located status stated rather than
   merely un-hedged.** §2.3 now reads *"it holds for every `n`, because it is a
   corollary of the theorem quoted in §0 rather than a measurement … The caps above
   bound this instrument, not the identity"*; §6 item 6 is struck and replaced with
   *"it is PROVED, in three lines"*; §10 item 2 is struck and its errand withdrawn; S1
   is upgraded to **QUOTED + PROVED, and separately MEASURED**; S12 is **WITHDRAWN as a
   claim about the literature**. **All four positive, none merely deleted.** ✓
2. **T3d reports TWO statements, not four.** ✓ — and `t3_bidigare.py` now **computes**
   it as T3e with its own control, which I reproduced independently (`0` everywhere;
   control **2, 26, 170**).
3. **Control (ii)'s accounting fixed AND its conclusion still stated.** The 1 442 are
   shown to **be** the 1 442 disjoint-ground-set pairs as a set equality, at source and
   from disjoint code; and *"the band product is invisible to the Hopf structure"* is
   marked **NOT withdrawn** in §5, §6 item 5, S7 and in `t5_hopf_monoid.py` itself.
   **It is strengthened**, from a count on `[4]` to a type statement at every ground
   set. ✓ **Nothing reads as withdrawn.**
4. **S4 and the two unfetched sources named at every occurrence.** Solomon and
   Garsia–Reutenauer/Atkinson appear by name in §0 item 4, §3, §6 item 1, §9 row 3, S4
   and S5, and at **8 of 8** occurrences in `code/species_7d75` — and `w3_scope.py`
   really does fail on a ninth, which I verified by adding one. ✓

**The doomed successor literature search.** The *instruction* is gone from the text:
§10 item 2 is struck and boxed *"THIS ITEM IS CLOSED AND ITS ERRAND IS WITHDRAWN"*, §0
carries *"DO NOT FILE THE SUCCESSOR LITERATURE SEARCH"*, and §7 item 3 is re-scoped to
*"it is not a prerequisite for anything and it should not be filed as one"*. **I did
not go looking for a ticket.** ✓

---

## 8. OVER-CORRECTION: CHECKED IN BOTH DIRECTIONS, NONE FOUND

After a BROKEN finding the comfortable error is hedging, so I tested for it explicitly
rather than only for the corrections. **15 of 15** required survivals are present:

* the headline is still *"IT IS A THEOREM, NOT ONLY A MEASUREMENT"* — **not** downgraded
  back to a measurement;
* *"no `n` dependence"* survives; the caps are stated to bound the instrument, not the
  identity;
* the poset half is still **87 of 87 with no cap** and **179 of 179 out of sample**;
* control (ii)'s conclusion survives and is stronger;
* the boundary does not slide **either** way: *"the `S_n` half is **NOT INDEPENDENTLY
  VERIFIED**"* is there, and so is *"**Being located is a real result.** It is not the
  same as being verified"* — the guard against reading *located* as *doubtful*. §4's
  *"Located, not verified"* and S5's *"MEASURED (the counts) + LOCATED (the functors)"*
  say the same thing in the same two directions.

Every withdrawn sentence I tested survives **only** inside the strike that replaces it
or in a passage naming the repair — including *"measured, not proved"*, *"not located
… in that generality"* and *"fires hard"*. **Nothing was hedged back.**

---

## 9. OUT OF SCOPE, NOT RE-OPENED

Per the brief and confirmed by mg-a61f: the headline (holds, and is a theorem), 20 of
21 numbers, 11 of 13 quotations verbatim against the PDFs, the poset half (87/87 no
cap, 179/179 out of sample). I did not re-fetch a PDF and did not re-run the quotation
battery. Y1's second half touches a quotation **only** as a string still asserted at
source; I make no new claim about what the book says.

**Also not done, and stated rather than implied.** Solomon, Garsia–Reutenauer/Atkinson,
AM 2020/2017, Saliola and Commins were **not read here either** — S4 and S5 are
unchanged by this audit. Y2's refutation attempt is one invariant at `n ≤ 5` and is
**inconclusive**, not negative: `Sol(S_n) ≇ Sol(S_n)^{op}` may still be true and I did
not establish it. My battery runs on the ground set `[4]` and to `n ≤ 5`, the same caps
as the work it audits, so it does not extend any range.

---

## 10. FOR THE NEXT READER — WHAT THIS ARC KEEPS DOING

§14.3 said the fix was *"one line of scope, not more diligence"*. **That was right and
it was not enough**, and Y1 is why: widening a checker's *target* while its *list* stays
where it was reproduces the defect one level out, and the passing run reads as coverage
exactly as before. The generalisable form:

> **A checker has two scopes — what it reads and what it looks for — and fixing one
> reads as fixing both.** `check_doc.py` had the full list over one file. `w3_scope.py`
> has a two-item list over a directory. Between them every file is covered and every
> statement is covered, and **no statement is covered in every file**.

And the seam finding (Y3/Y4) has its own form, which is not in this arc's record yet:

> **Two correct passes over one document produce a defect neither pass could have
> caught**, because each is complete against its own brief. The first pass wrote a
> self-assessment twice, in two versions; the second improved one copy, added a section
> answering it by name, and never saw the other. Nobody's brief covers a seam, so the
> seam needs its own check — and a duplicate-passage sweep is a cheap one that found it
> in under a second.

---

## 11. LEDGER

| # | claim | status |
|---|---|---|
| **A1** | The three instruments and mg-a61f's battery all reproduce; `species_7d75`'s seven committed outputs are **byte-identical** after a full re-run | **MEASURED** |
| **A2** | `\|F\| = 4399`, `\|AC\| = 2685`, `\|P × Σ\| = 16425` on `[4]` | **MEASURED**, from a kernel sharing no code |
| **A3** | All five columns are demonstrated able to fail under mutations chosen by this audit; the per-column verdict agrees with R2c cell for cell | **MEASURED**, 60 predicted cells, 4 missed and kept |
| **A4** | Associativity, coassociativity and compatibility are pinned at 0 over 24 arbitrary sub-collections, non-vacuously, with a firing control | **MEASURED** |
| **A5** | Both closure columns return 0 for the full ambient and for the wrong pairing — §5's reading is right and §0 was brought **up** to it | **MEASURED + CHECKED IN THE TEXT** |
| **A6** | T3d (`0/0/4/54/472`) and T3e (`0`; control `2, 26, 170`) reproduce entry for entry | **MEASURED**, disjoint code |
| **Y1** | X3 and the AM §17.5 quotation are **still asserted** in `code/species_7d75`; `w3_scope.py` PASSES the same tree; both are in `check_doc.py`'s own `STRICKEN` table | **MAJOR — MEASURED**, 4 controls |
| **Y2** | §0's *"the left side **is** Solomon's descent algebra"* contradicts §2.2, §9 row 3, S2 and AM 10.13 as §0 quotes it | **MINOR — wording.** Refutation attempted and **inconclusive** at `n ≤ 5` |
| **Y3** | §14's limitation box appears twice, 56 % similar, disagreeing; one copy calls an eight-item banner *"the five items"* | **MINOR — MEASURED** by a general duplicate sweep |
| **Y4** | §14.2 calls mg-f8fa's filing *"shelved"*; §14.3, eleven lines below, is its record | **MINOR** |
| **Y5** | `w3_scope.py` says **6** problems where its evidence says **12**; `r2_columns.py` says **40** cells where it prints **45** | **MINOR — MEASURED** |
| **NOT CLAIMED** | that anything here is false; that the ordering of any predicted-vs-actual battery was verified (nothing can); that Solomon or Garsia–Reutenauer/Atkinson were read; that `Sol(S_n) ≇ Sol(S_n)^{op}`; that any range was extended | |

---

## 12. REPRODUCE

```
cd code/species_audit_73df && ./run_all.sh    # ~100 s, pure Python 3, NO NETWORK
```

Outputs: `out_selftest.txt` (5 384 assertions), `out_c1_columns.txt`,
`out_c2_pinned.txt`, `out_c3_bidigare.txt`, `out_c4_scope.txt`, `out_c5_doc.txt`.
`TOTAL BAD` here counts **findings against the audited work**, following
`code/species_audit_a61f`; `C1 PREDICTIONS MISSED` is on its own line and is not folded
into it.

**Two defects this instrument found in itself and kept** are in its README: a first
sweep that was vacuous because the arithmetic rule emptied the low-degree components,
and a first exoneration rule that an adjacent unrelated *"is not the framework this
ticket is about"* disarmed — `w3_scope.py`'s own recorded false negative, reproduced
against this file by the same mechanism.
