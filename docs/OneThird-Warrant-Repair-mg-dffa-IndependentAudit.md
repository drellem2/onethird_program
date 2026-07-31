# Independent audit of the mg-dffa warrant narrowing — THE FOUR REPLACEMENTS HOLD, AND FOUR IS NOT THE POPULATION

**Work item:** mg-19ec, pre-filed in the same action as its parent. **Date:** 2026-07-31.
**Target:** `645b5a4` (mg-dffa), landing mg-5800's F1–F4 on
`docs/OneThird-Branching-Graphs-Where-This-Lives.md` and
`code/branching_repair_41aa/check_doc.py`. **Account audited:**
`docs/OneThird-Warrant-Repair-mg-dffa.md`. **Instrument:** `code/branching_audit_19ec/`
— a fifth instrument, importing nothing from `branching_af28/`, `branching_audit_6ad0/`,
`branching_audit_5800/`, `branching_repair_41aa/` or `branching_warrant_dffa/`.
**Predictions committed before any probe ran:** `170094f`.

---

## 0. THE VERDICT

| | |
|---|---|
| **The four replacement sentences** | **ALL FOUR TRUE, and all four carried by the evidence cited for them.** Read on their own terms, with the originals ignored. |
| **Narrowed by vagueness?** | **NO — measured, not asserted.** 0 of the 15 new phrasings sits in a hedged sentence, against 26 hedge tokens. The one weaker predicate (*"of the same **kind**"*) is **bounded, not vague**: at both sites the next sentence names the difference and both halves are measured. §1.3a. Where a hedge was on offer — mg-5800's own suggested fix for F4 — it was refused and Brown `§4.3` was read instead. |
| **Every figure** | **REPRODUCES** on this instrument. 44 / 5 464 / 0 bad; 33 / 28 / 5 / `221`; 17 distinct `P`, 5 not skew, 2 at `\|P\|=5`, 3 at `\|P\|=6`; 30 of 30 on the Young side; skew classes 1, 2, 5, 11, 26, 62. |
| **0 BROKEN** | **HOLDS.** Nothing mg-5800 confirmed is disturbed. |
| **The Birkhoff-free converse of X1** | **SURVIVES, and is RE-MEASURED here: 107 of 405, 0 counterexamples in either direction, at `n ≤ 6`, with join-irreducibles never computed on the comparison path.** |
| **Did it stop at four?** | **NO — and nobody had asked. On the sharpest form of the question the population is EIGHT and FOUR are unbounded; mg-dffa edited two of the eight, changed the reading at both and the bound at neither.** |
| **OPEN — 5 MINOR** | **A** the narrowing left its own population unbounded; **B** the clause faulting Young–Fibonacci for naming no class states the Young classification unbounded — a **widening**, in new text, by a repair whose whole job was narrowing; **C** the contrast as worded is not the contrast that holds; **D** four is not the population; **E** the repair's own runner is green with F4's premise unread. |
| **OBSERVATIONS, not defects** | **F** the new `check_doc.py` check does not fire when both ends of the chain move together; **G** two sentences rest on word counts that a reading corroborates. |

**Nothing here withdraws a number and nothing here withdraws a sentence.** All five findings
are MINOR and all five are about warrant — which is what the parent was repairing, and is why
this audit was pre-filed.

---

## 1. THE FOUR REPLACEMENTS, READ AS NEW CLAIMS

Each is audited with the original ignored. The question is only: **is the new sentence true,
and is it carried by the evidence cited for it?**

### 1.1 F1a — ledger row B1, widened to a LATTICE isomorphism — **HOLDS**

> 44 partitions, `n ≤ 7`. **Meet and join preserved on every pair, not the order alone** …
> measured three times on disjoint instruments … **0 bad each time**. T1 in
> `code/branching_af28/` itself tests the **order** isomorphism only … though it prints the
> label `lattice-iso bad`.

Re-measured here (`out_e1_f1_cells.txt`), with **neither side permitted to assume the
identification the cell asserts**: meets and joins are computed as greatest lower bounds and
least upper bounds *in the order*, by search, on both sides. The left side is not allowed to
use "intersection of ideals"; the right side is not allowed to use "componentwise minimum of
partitions".

* 44 partitions with `1 ≤ n ≤ 7`; largest interval 19 elements. ✔
* **5 464 ordered pairs**, and `5 464 = Σ_λ |[∅,λ]|²` over those 44 — the figure is the
  count it claims to be, not a different count that happens to agree. ✔
* order 0 bad, **meet 0 bad, join 0 bad**. ✔

**The sub-claim about somebody else's code was read, not counted.** mg-dffa's evidence that
af28's T1 "tests the order only" is a **word count** — 0 occurrences of `meet` or `join`. A
word count is a proxy: code can form a meet without naming one. T1's body was extracted here
and every operation it performs on the two sides listed. It forms exactly one set
intersection, `ids[a] & ids[b]`, and consumes it in a **containment test**
(`== ids[a]`). So **the document's sentence survives a reading**, not merely a count.

*Precision note, filed as G below: mg-dffa's own probe line reads "T1 computes no meet
(0 occurrences)". T1 does form `ids[a] & ids[b]`. The cell is right; the probe's wording is
the loose one.*

**"Measured three times on disjoint instruments"** is checked here as a property of the import
graph, not read off a README: none of mg-6ad0, mg-5800, mg-dffa or mg-19ec imports a module of
any other, and each prints its own meet/join line. ✔

### 1.2 F1b — ledger row B5, widened to a step DERIVED twice — **HOLDS**

> … **cited and not re-derived in `code/branching_af28/`** — but it has since been derived
> without it … by mg-6ad0 on 67 of the 87 classes to `n ≤ 5` (20 over its cap of 90 …) … and
> by mg-5800 on all 87 … **mg-dffa LOCATED both results in those committed outputs; it did
> not re-run them.**

* `67 / 20 / 87` read here **out of the A4a section alone**, and internally consistent
  (`classes == tested + skipped`). ✔ The cap the cell names is the cap the output names. ✔
  Every skip is listed there. ✔
* Both quoted clauses are verbatim in the outputs they are attributed to. ✔ mg-5800 covers
  all 87. ✔
* **The load-bearing word.** `dim kF(P)/rad = |AC(P)|` alone does not give "all irreducibles
  are 1-dimensional". What gives it is that `Φ` is a **surjective ALGEBRA map** with nilpotent
  kernel, which forces `kF(P)/rad ≅ k^{AC(P)}`, a product of `|AC(P)|` copies of `k`. So the
  widened cell needs the cited outputs to say **algebra**, not linear. mg-6ad0's output says
  *"surjective algebra map"*, says the kernel is nilpotent, and draws
  `kF(P)/rad = k^{AC(P)}` itself; mg-5800's checks character multiplicativity, surjectivity
  and kernel nilpotence at 0. ✔ **The cell asserts a derivation and its evidence carries a
  derivation.**
* **The self-description is accurate.** `w1_ledger.py` imports no module of the cited
  directories, starts no subprocess, and opens only their output files. LOCATED, not
  MEASURED, is the right verb and the cell uses it. ✔

### 1.3 F2a and F2b — the two narrowed clauses — **TRUE, and see A, B, C**

Every figure re-derived here on a fifth instrument (`out_e2_f2_clauses.txt`): 33 intervals to
rank 6, all lattices, **28 distributive, 5 not**, smallest witness `w = 221`; `|J(P)| =
|interval|` on all 28; **17 distinct `P`**, of which **5 are not skew cell posets** — **2 of
the 4** at `|P| = 5`, **3 of the 5** at `|P| = 6`; Young side **30 of 30** distributive with
**0** of the resulting `P` outside the skew class. ✔ Every number.

*(One reporting difference, not a disagreement: mg-dffa lists one witness word per non-skew
class; this audit lists every `w` that reaches each. The class counts are identical.)*

**The Birkhoff clause was built here, not cited.** The replacement says *"every finite
distributive lattice is `J` of its join-irreducibles, so '28 of the 33 are `J(P)`' says
precisely '28 of the 33 are distributive'."* Measured on all 33: distributive ⟺ isomorphic to
`J(` its own join-irreducibles `)`, **33 agree, 0 disagree.** ✔ The clause is true.

**The verdict on row 10 does not move** and neither does any number. What follows are three
findings about the *sentences*.

### 1.3a DID IT NARROW BY VAGUENESS? — **NO**, and this is measured, not asserted

The brief asks specifically. **A sentence that asserts less because it says less precisely is
not a repair**, and the arc has just produced a case where a hedge covered exactly the adverse
cases.

**Scanned** (`out_e2_f2_clauses.txt` §E2f): **all 15** phrasings mg-dffa's own `w5_doc.py`
requires to be **present** in the document, covering all four findings — **all 15 located**,
and for each the **sentence containing it** tested against 26 hedge tokens (*may, might,
appears, seems, arguably, roughly, essentially, in some sense, presumably, on X's reading, has
not re-read, …*). **0 of 15 sit in a hedged sentence**, and the count of phrasings the probe
failed to locate is printed rather than left as a silent skip — see misses 7 and 8 below,
which are two ways this very check under-reported its own population before it was fixed.

**One construction IS less specific than what it replaced**, and it is the one the brief's
warning is aimed at: *"the **same** index-set contact"* became *"a contact of the same
**kind**"*. So — bounded, or merely vague? **Enumerated, which is what the brief asks for:**

| | |
|---|---|
| **inside** *"the same kind"* | both families are ideal lattices; each interval is `J(P)` for some `P`. **Measured here on all 33: the biconditional holds, 0 disagree.** |
| **outside it, and NAMED in the next sentence** | *which* `P`. Young: a named closed class. Young–Fibonacci: 17 distinct `P`, 5 of them not skew cell posets. **Measured here.** |

At **both** sites the weaker predicate is immediately followed, in the same paragraph and in
the same table cell, by *"it is not the same contact"* plus the measured difference — checked
mechanically at both. **So the repair replaced one definite claim with a weaker definite claim
plus its complement, and both halves are measured. That is narrowing to the evidence, not
splitting the difference.**

**And where a hedge was actually on offer it was refused.** mg-5800's own suggested fix for F4
was *"attach 'on mg-af28's reading, which nobody in this arc has re-read' to the headline"*.
mg-dffa declined it and read Brown `§4.3` instead — the harder of the two options, and the only
one that does not leave a headline resting on a hedge.

### 1.4 F4 — the premise, read rather than hedged — **HOLDS, and it is the strongest of the four**

mg-5800 offered two fixes: re-affirm premise (a) outside the strike, **or** attach *"on
mg-af28's reading, which nobody in this arc has re-read"* to the headline. The second is a
hedge on the premise of the headline. **mg-dffa refused it and went and read the paper.** That
is the harder option and the right one, and this audit re-did the reading on a **sixth
extractor** written here (`out_e3_f4_brown.txt`):

* `4.3. Distributive lattices` occurs exactly once; `4.4. The kids walk` exactly once, after
  it; **no other `4.x` heading lies between them.** ✔
* Brown's example sentence occurs **exactly once in the paper** and lies **strictly inside**
  `§4.3`. ✔ Its maximal chains are the lattice paths, in the same span. ✔
* Brown counts the chains `0̂ < x < 1̂` at `(p+1)(q+1) − 2` ✔ and **prints no size for the
  lattice** ✔ — the document states this at exactly that width.

**AND THE SOURCE IS NOW PINNED.** `w3_brown.py` records neither a digest nor an arXiv version,
so a later reader cannot tell whether they read the same bytes. This audit publishes it:

```
https://arxiv.org/pdf/math/0006145
532 339 bytes
sha256 8e3ff96d7a49d60d02ac21ddd59172208849014c328547a533c6cda79a176299
```

**"It introduces exactly one example" rests on a word count, and a reading corroborates it.**
mg-dffa's evidence is one occurrence of the string `example` in `§4.3`. Enumerated here:
`§4.3`'s only `consider` sits inside Brown's one example sentence; the only lattice the
section names explicitly is that same product of two chains, at `p = q = 2`; and the section's
references to Figures 1, 3, 3(a), 3(b), 4 and 5 are **four views of one object** — Figure 3 is
the grid, Figure 4 a step of the walk on it, Figure 5 that grid at `p = q = 2` embedded in a
Boolean lattice, Figure 1 a back-reference to `§4.2`. The sentence stands. Filed under G
because the account states only the word count as its evidence.

---

## 2. THE FIVE FINDINGS

### A — MINOR, WARRANT. The narrowing narrowed the READING and left the POPULATION unbounded

**The sentence as landed:**

> At the level of finite **intervals** a contact of the same **kind** extends: **28 of the
> 33** finite Young–Fibonacci intervals are distributive, so each is `J(P)` for some `P`,
> item 2.

Its entire content is now a **count**, and the count's population is not bounded in the
sentence that states it. **There are infinitely many finite intervals `[0̂, w]` in
Young–Fibonacci** — one for every word — and 33 is the count at `rank(w) ≤ 6` and nothing
else.

**Built, not argued** (`out_e2_f2_clauses.txt` §E2c): at `rank(w) ≤ 7` there are **54**
intervals, **39** distributive and **15** not. The family the sentence names is not the family
it counts.

**The bound exists twice in the same document** — in row 10's mg-41aa clause (*"to rank 6"*)
and in `§2` item 2 (*"of the **33** intervals `[0̂, w]` … with `rank(w) ≤ 6`"*), which is what
the trailing *"item 2"* points at. Both located mechanically. So this is not a missing
measurement; it is a sentence written narrower in its reading and left wide in its population,
by a repair whose subject is exactly that.

**Cost of the fix: three words** — *"to rank 6"*.

### B — MINOR, WARRANT, and the more serious. The clause that faults Young–Fibonacci for naming no class states the YOUNG classification UNBOUNDED

**The sentence as landed** (`§2`, new paragraph; and again in row 10's new clause):

> The Young headline is a **classification** — the intervals of Young's lattice are `J(P)` for
> `P` **exactly** the skew cell posets, a named closed class …

No bound, at either site. Checked mechanically at both.

**What the document itself books that claim as.** Ledger row **B2** records the *"exactly"* as
**tested in both directions for all 405 poset classes to `n ≤ 6`**, exhaustive to `n ≤ 5`, with
the `n ≥ 7` totals marked *"A000112, cited not computed"*. And mg-5800 — the audit this repair
is landing — puts *"that the converse of X1 holds beyond `n = 6`"* on its **NOT CLAIMED** list.
Both located mechanically.

**This is a widening, in new text, by a repair whose whole job was narrowing** — and it is a
widening of the one claim the arc has been most careful about. The paragraph's rhetorical move
is to fault the Young–Fibonacci side for naming no class of `P`; it makes that contrast by
stating the Young side's classification as flat fact.

**It is not false.** It follows from Birkhoff together with the identification of the
join-irreducibles of `[μ, λ]` with the cells of `λ/μ`. **What is wrong is the warrant**: the
document's entire convention is to separate MEASURED from CITED, and this sentence cites
Birkhoff **only for the other side of its own contrast**.

**Cost of the fix: one clause** — either the bound the ledger already carries, or the
attribution the sentence gives its neighbour.

### C — MINOR, PRECISION. The contrast as worded is not the contrast that holds

> The Young headline is a **classification** … The Young–Fibonacci sentence is **Birkhoff plus
> a distributivity count** …

Measured here, with the identical procedure applied to each side:

```
Young       : 30 intervals -> all distributive -> Birkhoff -> 18 distinct P, all skew
Young-Fib.  : 33 intervals -> 28 distributive  -> Birkhoff -> 17 distinct P, 5 not skew
```

**Both sides are Birkhoff plus a distributivity count.** What differs is that the Young side's
`P` land in a named closed class and the Young–Fibonacci side's do not — which is precisely
what the paragraph's own operative clause (*"names no class of `P`"*) says. The sentence
before it implies the Young side does not go through Birkhoff, and it does.

Recorded as imprecision. The operative claim is correct and the measurement under it is
correct.

### D — MINOR. FOUR IS NOT THE POPULATION

**No bare total. The population is named three ways** (`out_e5_population.txt`).

**The universe.** `docs/OneThird-Branching-Graphs-Where-This-Lives.md`: 156 claim sites parsed
(one per paragraph, one per table cell over 30 characters), **98 LIVE** — outside fenced code,
outside block quotes, outside blocks carrying the document's bold-caps `**STRUCK**` /
`**CORRECTED**` / `**RE-SCOPED**` markers, and outside the three primed ledger rows that record
a withdrawn claim — containing **316 live sentences**. Sentence grain, because at paragraph
grain the defect vanishes: mg-dffa's own new paragraph contains the string `|P| = 5`, which any
coarse scope test scores as a bound and which is not a bound on the classification the
paragraph asserts.

**POP-3, the sharpest form, and the one that answers the question.** Every live sentence
stating the figure **33** about Young–Fibonacci intervals, and whether it carries the rank
bound:

| | line | | |
|---|---|---|---|
| **1** | 166 | **BOUNDED** | *"5 of the 33 intervals `[0̂, w]`, `rank(w) ≤ 6` …"* |
| **2** | 166 | **BOUNDED** | *"28 of the 33 Young–Fibonacci intervals **to rank 6** are distributive"* |
| **3** | 175 | **UNBOUNDED** | *"28 of the 33 finite Young–Fibonacci intervals are distributive"* — **mg-dffa's own, finding A** |
| **4** | 181 | **UNBOUNDED** | *"'28 of the 33 are `J(P)`' says precisely '28 of the 33 are distributive'"* — **mg-dffa's own** |
| **5** | 202 | **BOUNDED** | *"5 of its 33 intervals **to rank 6** fail"* |
| **6** | 307 | **BOUNDED** | row 10, mg-41aa: *"28 of the 33 … **to rank 6**"* |
| **7** | 413 | **UNBOUNDED** | ledger **B4**: *"33 Young–Fibonacci intervals, 5 non-distributive"* |
| **8** | 414 | **UNBOUNDED** | ledger **B4′**: *"At interval level, **28 of 33** Young–Fibonacci intervals are distributive"* |

**Eight sites. Four bounded, four not. mg-dffa was handed two of the eight, edited both,
changed the READING at both and the BOUND at neither — and two more (B4, B4′, the ledger rows
downstream readers quote) nobody handed it and nobody fixed.** That is the answer: four was the
number of findings on the desk, not the number of instances in the document.

*(Row 6 is scored BOUNDED for the **33-interval figure**, which is what POP-3 counts: mg-41aa's
clause there says "to rank 6". The **separate** clause mg-dffa added to that same cell —
"`P` exactly the skew cell posets" — is unbounded, and is finding **B** at its second site. One
table cell, two claims, one of each.)*

**The wider census, adjudicated by hand, every site accounted for.** POP-1 (live sentences
stating a count `N of M`): 19, of which **11 unbounded**. POP-2 (live empirical universals,
unattributed): 19, of which **10 unbounded**. The two do not overlap; the union is **21**. All
21 are printed with line numbers in `out_e5_population.txt`, and all 21 are adjudicated here:

| | count | which |
|---|---|---|
| **GENUINE instances of mg-5800's defect** | **7** | lines 175, 181 ×3, 307, 413, 414 |
| self-bounding — the total *is* the population and it is printed | 6 | `0 of 64` ×3, `0 of 405` / `1 of 405` ×2, `2 of the 12` / `0 of the 5` |
| attributed in the same cell (Stanley, Byrnes; *"cited … and not read"*) | 3 | lines 166 ×2, 413 |
| analytic, or not a measurement at all | 5 | the `U(1̂) = 0` proof, the method paragraph, a verdict label, a reading disclosure, `§9`'s X5 |
| | **21** | |

**Of the seven genuine instances, FIVE are sentences mg-dffa wrote** — lines 175, 181 (three
sentences: the `28 of the 33` restatement, the `exactly the skew cell posets` clause, and
*"30 of 30 intervals distributive and **0** of the resulting `P` outside the skew class"*,
which carries no `|λ| ≤ 6`), and 307 (row 10's new clause). At the grain of distinct **claims**
those five carry three: the 33-interval population (finding A), the Young classification
(finding B), and the 30-interval population.

**The other two are ledger rows B4 and B4′ — the rows downstream readers quote — and nobody
handed them to anybody.** That is the answer to the question this ticket was filed to ask:
**four was the number of findings on the desk, not the number of instances in the document,
and the repair added more instances of the defect than it was given.**

### E — MINOR. THE REPAIR'S OWN RUNNER IS GREEN WITH F4's PREMISE UNREAD

*This is the finding no list in the brief named. I chose the instrument's own exit contract,
because F3 — one of the four this commit repaired — is exactly "a control that could not fire
on the thing it appeared to certify", and the natural place for that defect to recur is in the
probes written to repair it.*

**Built, not argued** (`out_e7_instrument.txt` §E7a). A complete copy of the instrument and
every directory and document its probes read was made, `urllib.request.urlopen` was forced to
raise, and the runner was executed:

```
w3_brown.py exit code with no network : 0
run_all.sh  exit code with no network : 0
      done.  Headline lines:
      SELF-TEST: 42 assertions, 0 failed
      SUMMARY w1_ledger: partitions 44, failures 0
      SUMMARY w2_family: intervals 33, distributive 28, non-distributive 5,
      SUMMARY w2_family: distinct P 17, of them not skew cell posets 5,
      SUMMARY w2_family: failures 0
      SUMMARY w4_control: failures 0
      SUMMARY w5_doc: checks 41, failures 0
```

**The only trace of the gap is an ABSENT `SUMMARY w3_brown` line**, which nothing looks for:
`run_all.sh`'s `set -e` is keyed on exit status and `w3_brown.py` returns 0, and the final
`grep … || true` cannot fail.

**What falls inside it, enumerated** — unverified while every status line reads green:

* the `§4.3` heading is *"Distributive lattices"*;
* the `§4.4` heading is *"The kids walk"* and follows it;
* Brown's example sentence lies strictly between them;
* `§4.3` contains exactly one occurrence of *example*;
* the maximal chains are the lattice paths;
* Brown counts the chains at `(p+1)(q+1) − 2`.

**It is DECLARED** — in `w3_brown.py`'s docstring, in `run_all.sh`'s header comment, and in the
account document's `§7`. So it is a warrant defect and not a hidden one, which is the same
category as the four this commit landed. **And the committed `out_w3_brown.txt` records a run
that did reach arXiv, and E3 of this audit re-read the paper and pinned it.** The defect is in
the exit contract, not in the reading.

**What this audit did instead, so the contrast is not just advice.** `e3_f4_brown.py` returns
**2** — not 0 — when it cannot reach arXiv, and `run_all.sh` here is green only when every
probe's exit code equals the one committed in `PREDICTIONS.md` before any of them ran. A probe
that verified nothing cannot report green.

---

## 3. THE OBSERVATIONS

### F — the new `check_doc.py` check, and the one thing it does not catch

Fired in **seven** configurations (`out_e4_f3_control.txt`), four of which mg-dffa did not
build:

| | configuration | exit | failures named |
|---|---|---|---|
| **C1** | faithful copy | 0 | none |
| **C2** | computed `360 → 361` | 1 | **the new check alone** |
| **C3** | `out_r1b_skew8.txt` deleted | 1 | the SKEW8-line check and the new check |
| **C4** | *present but EMPTY* **[new]** | 1 | both |
| **C5** | *TWO `SKEW8` lines* **[new]** | 1 | both |
| **C6** | *`SKEW8` non-numeric* **[new]** | 1 | both |
| **C7** | *BOTH ends moved to 361 together* **[new]** | 1 | `T2 row n=8 prints straight 12 and skew 360` |

A missing, empty, duplicated or unparseable input is a **failure** in every one of them, never
a skip. That is what F3 asked for and it is what was delivered.

**C7 is the one worth naming.** The new check compares the two ends of the chain **with each
other**; move both together and it agrees. What catches C7 is `check_doc.py`'s **older typed
constant** — the very thing F3 correctly identified as not a provenance control. The two are
complements: neither alone closes the chain. *"The control was closed instead of the
sentence"* is true of the **pair**, not of the new line by itself. No number moves either way.

### G — two sentences resting on word counts, both corroborated by a reading

* *"T1 computes no meet (0 occurrences)"* — T1 does form `ids[a] & ids[b]`, and consumes it in
  a containment test. The **document's** cell (*"tests the order isomorphism only"*) is right;
  the **probe's** wording is the loose one. §1.1.
* *"`§4.3` introduces exactly one example"* — one occurrence of the word. Corroborated here by
  enumerating what a word count cannot see. §1.4.
* And *"all located **by position, strictly between the two section headings**"* covers four
  items, **two of which ARE the headings**. A reader checking the sentence literally finds two
  misses; a reader checking the claim finds it discharged. Imprecision, not a defect.

---

## 4. WHAT MUST NOT BE DISTURBED — RE-RUN AND RE-MEASURED

**The converse of X1 at `n = 6` WITHOUT BIRKHOFF is not checked here by re-reading mg-5800's
output. It is measured again** (`out_e6_standing.txt`):

* **405** poset classes on 1..6 elements — 1, 2, 5, 16, 63, 318 — enumerated as transitively
  closed relations with `0 < 1 < ⋯ < n−1` as a linear extension, canonised by the **plain `n!`
  minimum**. ✔
* **107** skew cell poset classes on 1..6 cells — 1, 2, 5, 11, 26, 62. ✔
* **The two heights, MEASURED rather than assumed**, so that restricting the search to skew
  shapes with `|P|` cells is a measurement: `height(J(P)) = |P|` on all 405, 0 bad;
  `height([μ,λ]) = |λ/μ|` on every skew shape to 6 cells, 0 bad. **Assuming them is exactly
  where the Birkhoff-free route would quietly stop being Birkhoff-free.**
* **`J(P)` is a Young interval for exactly 107 of the 405.** Every skew cell poset matches an
  interval; **no non-skew poset matches any interval**. **0 counterexamples in either
  direction.** ✔
* **How it is Birkhoff-free:** the right side is built from PARTITIONS under containment, the
  left from ORDER IDEALS, and they are compared by an isomorphism search on the strict order
  relation. `join_irreducibles` is never called on that path — checked mechanically against
  this audit's own source with docstrings stripped. And mg-5800's `a2_exactly.py`, which owns
  the result, is **unchanged by the repair commit** and forms no join-irreducible in any line
  of its code.
* **mg-dffa touched exactly the rows it says it touched**, read out of `git diff` and not out
  of the commit message: ledger rows **B1** and **B5**, and `§3` row **10**. **B2 — whose
  "exactly" carries the converse — is not among them.** ✔

**The upstream suites, re-run on a clean tree, with the exit codes predicted before the run:**

| | predicted | got |
|---|---|---|
| `code/branching_warrant_dffa/run_all.sh` | 0 | **0** |
| `code/branching_repair_41aa/check_doc.py` | 0 | **0** — 31 checks, 0 failed |
| `code/branching_audit_5800/run_all.sh` | 0 | **0** |
| `code/branching_repair_41aa/run_all.sh` | 0 | **0** |
| `code/branching_audit_6ad0/run_all.sh` | 0 | **0** |
| `code/branching_af28/run_all.sh` | 0 | **0** |
| `git status` over those five directories after restore | empty | **CLEAN** |

**6 of 6 exit codes matched their prediction. 0 BROKEN holds.**

**Every regenerated output was classified, not eyeballed** — normalised by replacing `(12.3s)`
and `line NNN` with placeholders, then re-compared. Two files came back **TIMINGS / LINE
NUMBERS ONLY**. **Three came back as content, and all three are accounted for:**

* **`out_a7_doc.txt` — the F2 repair landing, seen from outside.** mg-5800's beyond-brief diff
  now reads:

  ```
  -  B2  §2 heading note: 'the index-set contact DOES extend' to YF present:True
  +  B2  §2 heading note: 'the index-set contact DOES extend' to YF present:False
  -  B3  §3 row 10: 'the SAME index-set contact ... on 28 of 33'    present:True
  +  B3  §3 row 10: 'the SAME index-set contact ... on 28 of 33'    present:False
  ```

  The two wide phrasings mg-5800 quoted are gone from the document, which is exactly what F2
  asked for. Those lines are **informational, not assertions** — `a7_doc.py:161` prints, it
  does not `check()` — so the suite still reports 27 checks 0 failed. Recorded because a
  reader diffing that file could read `True → False` as a regression when it is the repair.

* **`out_r1b_skew8.txt` — a timing my own normaliser did not recognise.**
  `wall clock: 173 s` → `wall clock: 438 s`, on a machine running three agents at once. No
  figure moved: **16 999 posets on 8 elements, and `SKEW8 360`, both identical.** My
  normaliser handles `(12.3s)` and missed `wall clock: NNN s`, so a timing was filed as
  content. **The classifier is deliberately left as it ran** rather than tuned after the
  fact — a normaliser widened until nothing shows is worth nothing.

* **`out_a6_grep.txt` — an artefact of running the suite, and a small real observation.**
  One extra line appeared: `Binary file ../branching_repair_41aa/__pycache__/
  r3_rescope.cpython-314.pyc matches`. mg-5800's A6 quotation grep is **not restricted to
  source files**, so its output depends on whether Python has left a bytecode cache in a
  sibling directory — which running the suite creates. Nothing about the quotations moved;
  the grep's *population* is just wider than its purpose. Not a defect of this repair, and
  not landed: it is filed here so the next reader of that file knows why the line comes and
  goes.

**The five directories were then restored with `git checkout --`, and `git status` over them
is CLEAN** — so this audit's branch carries no regenerated output of a directory it does not
own.

---

## 5. THE PREDICTIONS, AND THE MISSES, KEPT AS WRITTEN

`PREDICTIONS.md` was committed at `170094f`, before any probe in
`code/branching_audit_19ec/` ran. **All nine exit-code predictions matched**, and this audit's
runner is green **only** because they did — it compares each probe's exit code with the
committed prediction rather than with zero, so a probe predicted to fire and then not firing is
reported as a miss in the same way as the reverse.

```
selftest19ec.py   predicted 0  got 0  ok      e4_f3_control.py  predicted 0  got 0  ok
e1_f1_cells.py    predicted 0  got 0  ok      e5_population.py  predicted 1  got 1  ok
e2_f2_clauses.py  predicted 1  got 1  ok      e6_standing.py    predicted 0  got 0  ok
e3_f4_brown.py    predicted 0  got 0  ok      e7_instrument.py  predicted 1  got 1  ok
```

Substantively: both unbounded populations were predicted and both were found; *"the population
is strictly greater than four"* was predicted and found; **107 of 405** was predicted by name
and came out exactly; the runner-green-without-network was predicted and built; the unpinned
download was predicted and is now pinned.

**Nine misses, all mine, none deleted.**

1. **E3 first fired on the wrong predicate.** It asked whether every `Figure` reference in
   `§4.3` pointed at the same figure NUMBER. It does not — Figures 1, 3, 4, 5 are all cited —
   and the check went BAD, against a prediction of 0. Reading the span showed four views of
   **one** object. The predicate was replaced by a reading (*the only lattice `§4.3` names
   explicitly*), and the miss is recorded in `out_e3_f4_brown.txt` rather than deleted.
2. **My `contains()` mishandled trailing zeros**, so every Young interval whose `μ` ended in a
   zero silently lost its bottom element. **It was caught by E6b's height assertion** — which
   is precisely why the two heights are measured rather than assumed.
3. **E7's first mini-tree omitted the sibling directories**, so mg-dffa's runner went red for
   want of `out_a1_contact.txt` rather than for want of the network: a red runner that proved
   nothing. An isolation bug in a probe about isolation.
4. **E5's first strike filter matched the bare words case-insensitively**, so the live prose
   *"items 2 and 5 are re-scoped below"* excluded the F2a replacement paragraph — the single
   sentence this audit exists to read. Re-keyed on the document's actual bold-caps marker.
5. **E2c's cross-reference regex** did not allow for a block-quote continuation prefix and
   reported a false BAD against `§2` item 2.
6. **E6's Birkhoff-free self-check** searched for the string `irreducible` including
   docstrings, and this audit's own docstring says *"join-irreducible"*, so it fired on itself.
   Re-keyed on the call, with docstrings and comments stripped.
7. **The hedge scan SILENTLY TRUNCATED ITS OWN POPULATION.** It decoded each required phrasing
   with `.encode().decode("unicode_escape")`, which mangles every non-ASCII character, so the
   entry containing an em-dash — *"RE-AFFIRMED OUTSIDE THE STRIKE — AND READ"*, F4's — was
   never found in the document and vanished from the scan **without a word**, leaving the
   reported population at 14 instead of 15. **A silently truncated population is precisely the
   defect this audit is about, in this audit's own instrument.** Drops are now counted and
   printed.
8. **And it scanned the wrong column, then the wrong text.** `w5_doc.py`'s list holds
   `(label, phrasing)` pairs; a bare string-scan collected the labels too and reported 16 of
   them as *"not located in the document"* — they were never meant to be. And a raw
   `doc.find` reported one phrasing missing because it spans a line break, while `w5_doc.py`,
   which passes 41 of 41, flattens first.

9. **AND ONE THAT WAS NOT IN A PREDICATE AT ALL — IT WAS IN THE PROCEDURE.** The upstream
   re-run was started, stopped and restarted. **Killing the wrapper shell did not kill the
   subshell it had spawned**, so for several minutes **two copies of
   `code/branching_audit_5800/run_all.sh` were writing the same output files**, and a stray
   Python job of mine from an abandoned timing measurement was competing for CPU alongside
   them. Detected in the process list, not in any summary: the fix was to kill every
   participant by PID, restore the five directories, and re-run once from a clean tree with
   the process list checked for a singleton first.

   **And the near-miss inside the near-miss, stated at its own width.** What drew attention
   was `out_a2_exactly.txt` at **zero bytes** while later outputs of the same suite already
   had content. That looks like mg-5800's Birkhoff-free A2 failing — and reading it that way
   would have been **the most damaging false finding this audit could have filed**. It is not
   what it was: Python buffers redirected stdout until exit, so a running probe's output file
   is legitimately empty, and the same zero bytes appear in the clean re-run while `a2` is
   simply still working. **The real defect was two writers, and the symptom that exposed it
   was not a defect at all.** An empty output is not a zero, and it is not a failure either.

**Four of the first eight (1, 4, 7, 8) would have produced a false finding or a misstated
population had they not been chased; all eight were in the predicate, not in the target. The
ninth was in the procedure, and it is the one that came closest to putting a false BROKEN into
this document.**

---

## 6. WHAT THIS AUDIT DID NOT ESTABLISH

* **The skew class counts at `n = 7` (149) and `n = 8` (360) are NOT reproduced here.** `canon`
  in this instrument is the plain `n!` minimum and `8!` per poset does not finish. The
  alternative is a refined canonical form — **which is exactly the shortcut mg-5800 recorded a
  control firing on: its cheaper canon reproduced A000112 to 16 999 while the bug was live.**
  So the limit is stated rather than bought with a weaker definition. **360 remains derived by
  `branching_repair_41aa` alone**, and finding F is what its control is worth.
* **Nothing beyond `n = 6` for the converse of X1.** Where mg-5800 left it.
* **Brown (2000) beyond `§4.3` and the opening of `§4.4`** is still unread by this arc, and
  this audit read no more of it than mg-dffa did.
* **B5's step is not derived here either.** It is located, in the same two outputs, and the
  reading of the load-bearing word (`ALGEBRA map`) is the new part.
* **Nothing about `λ₂`, `Δ_AT`, pricing or publishability.** No `STATE.md` edit. No edit to any
  document under audit — this audit changes no file it audits.

---

## 7. REPRODUCE

```
cd code/branching_audit_19ec && ./run_all.sh    # ~35 s; e3 needs network
```

The runner prints each probe's exit code next to the code predicted for it in
`PREDICTIONS.md` and **exits with the number of misses**. `e3_f4_brown.py` returns **2** if it
cannot reach arXiv, which is not its prediction, so a run that could not read Brown goes red
rather than green.

Committed outputs: `out_selftest19ec.txt`, `out_e1_f1_cells.txt`, `out_e2_f2_clauses.txt`,
`out_e3_f4_brown.txt`, `out_e4_f3_control.txt`, `out_e5_population.txt`,
`out_e6_standing.txt`, `out_e7_instrument.txt`, `out_upstream.txt`.

---

## 8. SCOPE

This audit **changes no file it audits**. `docs/OneThird-Branching-Graphs-Where-This-Lives.md`,
`docs/OneThird-Warrant-Repair-mg-dffa.md`, `code/branching_warrant_dffa/`,
`code/branching_repair_41aa/`, `code/branching_af28/`, `code/branching_audit_6ad0/` and
`code/branching_audit_5800/` are untouched. Findings A–E are reported for a successor to land
or to decline; **none of them is landed here**, because landing a finding in the document one
is auditing is how the last three deliverables in this arc acquired the defects they were
filed to repair. No `STATE.md` edit. Not relayed to Daniel.
