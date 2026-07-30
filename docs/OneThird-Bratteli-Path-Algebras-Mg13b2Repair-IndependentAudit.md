# Independent audit of the mg-a218 repair — mg-13b2 / `ed9cde4`

**Work item:** mg-d330, pre-filed in the same action as its parent. **Date:**
2026-07-30. **Target:** `docs/OneThird-Bratteli-Path-Algebras-Where-This-Lives.md`,
`code/branching_locate_db09/` and `code/branching_audit_a218/c2_vertexsets.py`
at commit `ed9cde4`. **Instrument:** `code/branching_audit_d330/`, `run_all.sh`,
~4 min, 867-assertion self-test, five test scripts.

**This audit shares no code with any instrument it audits.** `kern_d330.py`
rebuilds Temperley–Lieb half-diagrams, the cellular bilinear form and
`dim L(n,p) =` rank of the Gram matrix over `Q` from the combinatorial
definition. It is the **fourth** instrument to measure this object — mg-db09's
`T1b2` the first, mg-2060's `B1a`/`B1b` the second, mg-a218's `c1` the third.

---

## 0. HEADLINE

**The column really does report the set, the labels really are true, and I
could not break either. What broke is the auditing instrument that
commissioned this repair: mg-13b2 saw that a re-run would make mg-a218 score
its own repair as a bug, fixed exactly one of mg-a218's five scripts, and
`c1_branching.py` — the script that produced the 198-cell reproduction — now
reports 24 FINDINGS against the target where its own parser has gone blind.**

* **THE COLUMN SEPARATES THE SETS, AND I CONSTRUCTED THE PAIR THAT TESTS IT.**
  All 24 vertex sets re-measured on a fourth instrument, agreeing with the
  document's four rows **character for character**. The rendering is injective
  over **all 276** unordered pairs of the 24 cells — the target checks 36 — with
  **0 collisions**. The column is not injective on *arbitrary* vertex sets, and
  I built the pair that shows it; but the side condition that makes it faithful
  is **gated**, and the gate is load-bearing under deletion: RED 3 → GREEN 0
  (§2). **No count column stands beside it** and **no digest stands in for the
  set**.
* **EVERY DISPOSITION IN §8'S STATUS TABLE IS TRUE, BOTH DIRECTIONS.** X2's
  **four** sites checked one at a time against `03d7f91`, `2e66d03` and the
  working tree, including that two were closed *unmarked* at `2e66d03` and are
  marked now, and that the markers **reach the committed output** and not only
  the source. X3, X5, X6 and the 95.7 % figure are genuinely open, tested in
  the harder direction. **A whole-tree sweep over 728 files finds NO fifth site
  of X2**, calibrated so that an injected bare assertion still fires (§3).
* **X1 — `c1_branching.py` GOES RED, AND IT IS BOOKED AS THE TARGET'S FAULT.**
  Re-run on the repaired tree, mg-a218's primary script reports **24 FINDINGS**,
  every one of them `target ?`, because the count table its parser reads is the
  very thing mg-13b2 correctly deleted. **They are FINDINGS, not SELF-ERRORS.**
  174 of the 198 cells still compare and still agree; **24 have gone dark and
  are reported as red** (§4).
* **X2 — `c3_withdrawal.py` GOES RED ON THE REPAIR'S OWN NEW SCRIPT.** The
  check that exists because a repair once fixed the prose while the instrument
  went on asserting the error now finds **4 unmarked occurrences** of two
  withdrawn phrases, all four inside `t5_labels.py` and its committed output,
  where they sit as search needles (§4).
* **X3 — mg-a218'S DOCUMENT NOW MISDESCRIBES ITS OWN INSTRUMENT.** §10 says, in
  the present tense under REPRODUCE, *"`c2`, `c4` and `c5` exit `1`"*. On the
  repaired tree the scripts that exit 1 are **`c1` and `c3`** (§4).
* **X4 — "EVERY DISPOSITION LABEL" IS UNMEASURED.** `t5_labels.py` is a
  hand-written list of 29 labels with **no denominator derived from the
  document**. Swept independently, **8 of the 26 disposition-marked blocks are
  reached by no needle it looks for**, including the whole Sources
  bibliography — where *"Putcha … **NOT read**, and D10 rests on it"* is as
  load-bearing a disposition as any in §8 (§5).
* **X5 — THE FIGURES ABOUT THE LABEL INSTRUMENT ARE WRITTEN AT 7 SITES AND
  DERIVED AT 0.** `29 labels, 100 checks` and `all 7 fire` are correct today;
  nothing keeps them correct (§5).
* **THE WITHDRAWAL AND THE INVARIANT ARE UNDISTURBED.** The withdrawal is real
  and complete, `D2` is struck, `D10` reads as a conjecture, and the four
  `⊕End` figures `132 / 132 / 99 / 42` fall out of my own measurement as the
  sums of squares of the four rows. The invariant reproduces on a **fourth**
  instrument in every cell it touches (§1, §2).
* **The seam sweep found nothing**, at threshold **0.80** over **61 522**
  comparisons — 17 survivors, **17 marked, 0 unmarked** — and §6 says what would
  have counted, with two probes built from lines the repair really deleted.

**Direction, stated plainly: the repair is right and it is thorough.** The two
things mg-a218 left outstanding are both closed, at source and in prose, and
the third finding I went looking for — a fifth site of X2 — is not there. Every
finding below is about **what the repair did to the instruments around it**,
not about the document it repaired.

---

## 1. WHAT MY BRIEF TOLD ME, AND THE ONE THING NO LIST NAMES

My brief says its list is a **floor** and requires me to audit at least one
thing no list names, and to say what I chose.

**What I chose: what the repair did to the audit that commissioned it.**
mg-13b2 edited a file inside `code/branching_audit_a218/` — the instrument
belonging to the audit whose findings it repairs — and said exactly why:

> *"mg-a218's own `c2_vertexsets.py` is widened to accept either column form so
> that a RE-RUN tells the truth instead of scoring its own repair as a
> SELF-ERROR."*

That is the right instinct, precisely stated, and it is applied to **one of
mg-a218's five `c*.py` scripts**. Four of the five read the same rewritten
target. My brief names the delivered document, the vertex column, the labels
and the withdrawal. It does not name the auditing instrument's own health —
and *an audit whose repair silently breaks its auditor is the same defect one
level up*. So I re-ran all five (§4).

**I also checked, unprompted, that the invariant survives a fourth
instrument.** My brief tells me the 198-cell reproduction must not be weakened
and to flag any weakening. Verifying that it *holds* is a stronger answer than
verifying that nobody wrote it down wrong, so `kern_d330.py` measures it from
the definition.

---

## 2. THE PRIMARY TECHNICAL TARGET — A SET, OR A RENDERING OF ONE?

My brief: *"Verify two genuinely different vertex sets cannot present as equal
in the repaired column. Construct such a pair and confirm the column
distinguishes them — this is the deletion test's cousin and it is the only
thing that settles it."*

### The measurement, on a fourth instrument

| `β` | `n=1` | `n=2` | `n=3` | `n=4` | `n=5` | `n=6` |
|---|---|---|---|---|---|---|
| 3 | `[0:1]` | `[0:1,1:1]` | `[0:1,1:2]` | `[0:1,1:3,2:2]` | `[0:1,1:4,2:5]` | `[0:1,1:5,2:9,3:5]` |
| 2 | `[0:1]` | `[0:1,1:1]` | `[0:1,1:2]` | `[0:1,1:3,2:2]` | `[0:1,1:4,2:5]` | `[0:1,1:5,2:9,3:5]` |
| 1 | `[0:1]` | `[0:1,1:1]` | **`[0:1,1:1]`** | **`[0:1,1:3,2:1]`** | **`[0:1,1:4,2:1]`** | **`[0:1,1:4,2:9,3:1]`** |
| 0 | `[0:1]` | **`[0:1]`** | `[0:1,1:2]` | **`[0:1,1:2]`** | `[0:1,1:4,2:5]` | **`[0:1,1:4,2:5]`** |

Section 0's four rows agree with this **character for character**, and the sums
of squares at `n = 6` are `132 / 132 / 99 / 42`, which is the `dim ⊕_λ End(L_λ)`
column two places to the left — so the column is tied to a figure two other
routes compute, on my instrument as well as on the target's.

### Injectivity, over a wider population than the target checks

`T1b2` checks that the dimensions-only rendering separates exactly the pairs the
full form separates on the **36 same-level** `(parameter-pair, level)` cells. I
checked it over **every unordered pair of the 24 cells — 276 of them**, across
levels as well as across parameters. **0 pairs where the rendering agrees and
the set does not.** Of the 36 same-level pairs, **10** have an equal count and
an unequal set, which is mg-a218's figure and `T1b2`'s, reproduced here on a
third route.

### The constructed pair, which is what settles it

The column prints dimensions alone. That is a **function of** the vertex set,
not the set. Take

```
A = [0:1, 1:1]        two irreducibles, labelled p = 0 and p = 1
B = [0:1, 2:1]        two irreducibles, labelled p = 0 and p = 2
```

`A` and `B` are **different sets** — `B`'s second vertex is `L(n,2)` and `A`'s
is `L(n,1)`, different modules of the same dimension. A count shows them equal:
both are 2. **And so does the repaired column: both render `[1,1]`.**

**So the column does not separate arbitrary vertex sets.** What makes it
faithful is a **side condition** — the live labels `p` are an unbroken run from
`0` — and the honest question is not whether the rendering is injective in
general (it is not) but whether the side condition is **gated**. A rendering
with an unchecked side condition is a count in disguise. A rendering with a
checked one is not.

### The deletion test, and the guards are load-bearing

`B` was injected into `t1_tl.py`'s own `vtx` at `(n=2, β=3)` in a scratch copy.
The injected cell renders `[1,1]`, exactly as the real one does, so **the column
does not move and only a guard can see it**.

| variant | `TOTAL BAD` |
|---|---|
| unpatched | **0** |
| `B` injected, both guards intact | **3** |
| `B` injected, both guards deleted | **0** |

The run-from-0 guard names the injected cell by name and the collision guard
fires. **RED 3 → GREEN 0**: those two guards are the whole of what stands
between the delivered column and a false equality, and they are load-bearing.

**Verdict: the column reports the set.** It reports it through an abbreviation
whose faithfulness is a side condition rather than an identity, and the target
says so in its own words — *"the document's shorter dims-only form is not
argued to be faithful"* — and gates it. That is the correct standard and it is
met.

**One wording note, not scored as a finding.** §0 calls the dimensions-only
form *"the canonical form"* and the `[p:dim]` form *"the fuller form"*, while
`T1b2` says *"Canonical form of a vertex: the pair `(p, dim L(n,p))`"*. The two
use the same word for different things, in the one place in this document where
the distinction between a structure and a rendering of it is the whole subject.

### Was a count column retained?

**No.** Section 0's table has six columns and none of them counts irreducibles.
The withdrawn rendering `1,2,2,3,3,4` survives at exactly **one** site in the
document, §8's own repair note, which begins *"It printed"* — a marked
historical quotation. Recorded and not scored: the same six numbers survive in
`T1b2 (i)`'s output ten lines under the vertex sets, as *"the number of CELL
modules at level n … parameter-free"*, which is a different object and says so
on its own line.

### Was a hash accepted?

**There is none to accept.** The column carries the dimensions themselves.
`t1_tl.py` makes no digest call. The four in `t5_labels.py` are `sha256` over
**whole file contents** in `unchanged_since`, which is a file-identity check
and not a rendering of a set.

---

## 3. EVERY DISPOSITION IN SECTION 8, AGAINST THE DIFF, BOTH DIRECTIONS

My brief: *"A label is a claim. Partial states are the trap. Check every site
of every multi-site finding."* `e3_dispositions.py` shares nothing with
`t5_labels.py`; it is written afresh against `git show`.

**55 site-checks. 0 findings.**

### X2 — **CLOSED, at four sites, in two commits.** True at every site.

| site | open at `03d7f91` | at `2e66d03` | now | marker |
|---|---|---|---|---|
| §0's 2×2 cell | yes, `Path-pair *basis* survives` | **closed, unmarked** | closed | added by mg-13b2 |
| `T1d`'s printed line — **source and committed output** | yes, both | **closed, unmarked**, both | closed, both | added by mg-13b2, **and it reaches the committed output** |
| `T1a`'s *"iff"* — source and committed output | yes, both | **still open**, both | closed, both | `ONLY IF`, plus `T1c2` |
| §1's clause table — the fourth site | yes | **still open** | closed | *"named by no list"* |

Both directions hold. The two silently-closed sites really were silent at
`2e66d03` and really are marked now; the two mg-13b2 closed really were still
open at `2e66d03`, so the fourth site is genuinely a fourth. `T1c2`'s own
figures read `7 of the 20` pairs in the committed output, which is what §8
says. And the counting claim itself — *"four, not the three mg-2060 named"* —
holds: mg-2060's audit document names **3** of the four by their text and does
not name §1's clause table.

**The markers reach the reader.** Checking the marker in `t1_tl.py` is not
enough — the reader reads `out_t1_tl.txt`. `MARKED IN PLACE (mg-13b2)` is in
both.

### X3, X5, X6, the 95.7 % figure — **OPEN**, and open is the harder direction

An `OPEN` label is falsified by a site that has been **silently closed**, so
each is tested that way. X3: exactly **1** unqualified `(VO Prop. 1.4)` line
stands, and both `2e66d03` and `ed9cde4` move **0** lines carrying it. X5 and
the 95.7 % figure: `t3_ours.py` is byte-identical to its state at all three
commits. X6: §7 says *"Four elementary"* and enumerates exactly **4**
derivations `(a)`–`(d)`, with the dispute disclosed.

### `Repaired 1` — five sites

All five present, none standing unmarked outside its correction.

### A fifth site of X2 — swept over the whole tree

§8 says the fourth site was found by sweeping. A sweep of the same document
would find the same four, so mine is over **728 tracked `.md`/`.py`/`.txt`/`.sh`
files**: 53 occurrences of an X2-shaped claim, **0 unmarked**. Every one sits
inside a withdrawal, a correction, a refutation, or a checker's needle.

**What would have counted, and it fires.** The marker vocabulary was widened
once during construction — recorded in the source with its reason — so the
sweep is calibrated rather than trusted: a bare unmarked assertion injected
into a scratch copy **is caught** (2 hits), and the same assertion with a
marker beside it **is not** (0 hits).

---

## 4. WHAT THE REPAIR DID TO mg-a218'S INSTRUMENT

Every one of mg-a218's scripts, re-run in place against the repaired tree with
its stdout captured here — never redirected into its committed outputs, which
are the record of what that audit found.

| script | committed | live now | |
|---|---|---|---|
| `selftest_a218.py` | 0 bad, exit 0 | 0 bad, **exit 0** | unchanged |
| `c1_branching.py` | 0 self / 0 find, exit 0 | 0 self / **24 find**, **exit 1** | **X1** |
| `c2_vertexsets.py` | 0 self / 1 find, exit 1 | 0 self / 0 find, **exit 0** | **repaired, and widened** |
| `c3_withdrawal.py` | 0 self / 0 find, exit 0 | 0 self / **1 find**, **exit 1** | **X2** |
| `c4_seam.py` | 0 self / 1 find, exit 1 | 0 self / 0 find, **exit 0** | **repaired** |
| `c5_record.py` | 0 self / 1 find, exit 1 | 0 self / 0 find, **exit 0** | **repaired** |

**Three of the five moved the right way.** `c2`, `c4` and `c5` are mg-a218's
E3, E7 and E6 — the vertex column, the seam, and the disposition list — and all
three are now green **on their own instrument**, which is the strongest
available confirmation that the repair is real. `c0_repro.sh` still reports
**5 of 5 IDENTICAL**, as mg-13b2's commit message claims.

### X1 — `c1_branching.py` reports 24 findings, and they are the target's fault

`c1` is mg-a218's **primary** script. It produced **E1** — *"24 vertex-count
cells, 53 vertex-dimension cells and 121 edge cells, 0 disagreements"* — the
198-cell reproduction my brief tells me must not be weakened.

Of its 24 live findings:

| | |
|---|---|
| vertex-**COUNT** cells reading `target ?` | **24 of 24** |
| vertex-**DIMENSION** cells disagreeing | **0 of 53** |
| **EDGE** cells disagreeing | **0 of 121** |

**Mechanism, read out of the source rather than guessed.** `c1` parses the
target's committed `T1b2` block for a count table — a line of a `β` followed by
six integers:

```python
m = re.match(r"\s*(\d)\s+((?:\d+\s+){5}\d+)\s*$", line)
```

Lines in the **current** `out_t1_tl.txt` that this matches: **0**. mg-13b2
deleted that count table **on purpose** — it is mg-a218's own finding X1 that
the count was the defect. The parser that read it was not widened with `c2`'s.

**What is and is not weakened, stated precisely.** The mathematics is
untouched: `c1`'s own measurement of the vertex sets, the dimensions and the
five multiplicity-2 edges is unchanged, and every one of E1's numbers is
reproduced afresh by this audit on a fourth instrument. **174 of the 198 cells
still compare and still agree.** What is lost is the other 24: they no longer
compare against anything.

**And they are booked as FINDINGS, not SELF-ERRORS.** That distinction is
mg-a218's own — *"a non-zero exit means 'this script has something to report',
not 'this script is broken'"* — and here it goes the wrong way. The instrument
prints `vertex COUNT disagrees at beta=3 n=1: target ?, mine 1` **24 times**: an
accusation against the target at every cell where its own parser went blind.
mg-13b2 wrote, of `c2`, that the alternative would be *"an audit instrument
scoring its own repair as its own bug"*. That is exactly what `c1` now does,
and worse, because `c2` would have raised a SELF-ERROR and `c1` raises a
finding.

**And `c1`'s own population line is now false.** It still prints
*"vertex counts: 24 cells compared, population: every `(beta,n)` …"*. Zero were
compared. Twenty-four were compared against nothing.

### X2 — `c3_withdrawal.py` goes red on the repair's own new script

`c3` is the mg-73df-shaped check: it sweeps 16 files for the withdrawn phrases
and requires every occurrence to sit inside a withdrawal or correction.
mg-a218 reported **8 occurrences, all marked**. Live now it reports **4
unmarked**:

```
code/branching_locate_db09/out_t5_labels.txt:145  'measured (not cited)'
code/branching_locate_db09/out_t5_labels.txt:146  'held fixed down that column'
code/branching_locate_db09/t5_labels.py:393       'measured (not cited)'
code/branching_locate_db09/t5_labels.py:395       'held fixed down that column'
```

All four are inside **mg-13b2's own new `t5_labels.py`** and its committed
output, where the withdrawn phrases sit as **search needles** — the strings the
label checker looks for. In substance they are benign: a needle is not an
assertion. But the check exists precisely because a repair once fixed the prose
while an instrument went on printing the error inside a run ending
`TOTAL BAD: 0`, and it cannot distinguish the two. The fix is one marker
comment on each side; the point is that **nobody ran the check**.

### X3 — mg-a218's document now misdescribes its own instrument

`docs/OneThird-Bratteli-Path-Algebras-Mge8b8Repair-IndependentAudit.md` §10,
under **REPRODUCE**, in the present tense:

> **Exit codes are the finding channel, deliberately.** … `c2`, `c4` and `c5`
> exit `1`; those are E3, E7 and E6.

On the repaired tree the scripts that exit 1 are **`c1` and `c3`**. mg-13b2
edited that instrument and left the sentence describing it unchanged and
unmarked. **This is the label-versus-diff defect one document over** — a
present-tense claim about code, falsified by a commit that edited the code, with
no marker. A reader following §10 runs the instrument and gets a different
answer from the one the document promises.

**Not scored, and it is the right call.** mg-a218's committed
`out_c2_vertexsets.txt` is deliberately **not** regenerated, mg-13b2 says so,
and it gives the precedent (mg-a318's call for mg-8a5c). A committed audit
output is the record of what was found, not a live gate. What is scored is the
**sentence**, because it is present-tense instruction to a reader.

---

## 5. IS "EVERY DISPOSITION LABEL" EVERY DISPOSITION LABEL?

The repair's claim, at three sites: *"every disposition label in this document
— 29 of them, 100 checks"*. `29` is a numerator. I derived the denominator by
sweeping the document for the disposition vocabulary **`t5_labels.py`'s own
docstring names**, plus the eleven markers the document uses and that docstring
does not.

| | |
|---|---|
| lines of the document | 885 |
| lines carrying a marker from t5's own named vocabulary | 35 |
| lines carrying only a marker its docstring does not name | 14 |
| **blocks** carrying a disposition marker | **26** |
| of those, blocks t5 reaches through some needle | 18 |
| **blocks t5 reaches nowhere** | **8** |

A line is not a label, so the block is the unit: a label spans a paragraph or a
table row, and t5 may reach it through any line of that block. Only a block t5
reaches **nowhere** is a disposition its instrument cannot see. The eight:

| lines | what is dark |
|---|---|
| 118 | *"### The two objects, built — one of them WITHDRAWN"* |
| 155–166 | *"…is exactly how the withdrawn claim above broke"* |
| 239–245 | **`CORRECTED (mg-e8b8)`** — the 2×2 cell placement note *(its claim is checked in the neighbouring block; its own attribution is not)* |
| 537–544 | **`OUTCOME (mg-2060): NOT ESTABLISHED`** — the disposition on **D10, the deliverable** |
| 707–719 | §6's *"What `mg-13b2` added to the instrument"* |
| **741–749** | **the whole Sources bibliography** — *"Graham–Lehrer … **NOT read**"*, *"Goodman–de la Harpe–Jones … **located, NOT read**"*, *"Putcha … **located, NOT read, and D10 rests on it**"*, *"CMPX … **located, NOT evaluated here**"* |
| 828–835 | §8's *"It was wrong about its first entry"* — the repair's central self-correction |
| 847–877 | §8's *"What `mg-13b2` repaired"*, items 1–4 |

**The finding is a completeness defect in the word "every", not a wrong
disposition.** Every label t5 does check, it checks correctly — I re-derived
§8's whole status table independently in §3 and found nothing. But the
population is a **hand-written list with no derived denominator**, so *"every"*
is unmeasured, and `29` is a bare total. The bibliography is the substantive
gap: *"Putcha … NOT read, and D10 rests on it"* is a disposition on the
deliverable, and step 1 of what would establish D10 is **read Putcha** — the
day someone does, that line becomes false and nothing turns red.

### The figures about the label instrument: 7 sites, 0 gates

| figure | sites | live | |
|---|---|---|---|
| `29 labels, 100 checks` | 3 — the document twice, the README once | 29 / 100 | agree |
| the `7`-mutation battery, `all 7 fire` | 4 — the document three times, the README once | 7 / 7 | agree |

**Written at 7 sites, derived at 0.** No check in `t5_labels.py` and nothing in
`run_all.sh` compares the document's stated `29`/`100`/`7` to what the script
produces. The figures are correct today; nothing keeps them correct. Adding or
removing one label makes the document *and* its README wrong with every gate in
the tree still green — which is mg-a318's rule (*a gate must read the figure at
the site*) and mg-8e30's (*a duplicated literal is the defect*), applied to the
instrument built to enforce exactly that discipline on everything else.

---

## 6. THE SEAM CHECK, AND ITS THRESHOLD

My brief: *"Seam-check the document and report the threshold."*

**Threshold: 0.80**, `difflib.SequenceMatcher` ratio on whitespace-, markup-
and case-normalised text; minimum passage 60 characters after normalisation;
marker window 12 lines either side. Same threshold as mg-a218's, so the two
sweeps are comparable.

**Touched passages: 38** distinct lines `ed9cde4` deleted. **Swept population:
1 619 lines in 6 files** — the delivered document (636), mg-a218's audit
document (260), mg-2060's audit document (325), and the target instrument's
`t1_tl.py` (201), `out_t1_tl.txt` (151) and `README.md` (46). **61 522
comparisons.**

**17 survivors at or above the threshold: 11 EDIT IN PLACE, 6 SECOND COPY, 17
marked, 0 unmarked.** mg-a218's sweep found one unmarked in-place edit and it
was X2; mg-13b2 marked it, and this sweep finds no successor.

**What would have counted.** Any of the 38 deleted passages standing anywhere
in the 1 619 units with no disposition marker within 12 lines. Two calibration
probes, both **lines the repair really deleted** and both from the delivered
document: each is matched by the sweep, each is classified unmarked when placed
in marker-free prose (or, for the struck `D2` ledger row, correctly classified
*marked* because it carries its own `~~`), and neither fires when a marker is
put beside it.

*(My first two probes were sentences I wrote in the shape of the withdrawn
claims. Both scored ~0.41 and the script raised a SELF-ERROR against itself —
correctly. That miss is kept in `PREDICTIONS.md` as P17.)*

---

## 7. WHAT MUST NOT BE DISTURBED — AND IS NOT

My brief: *"The withdrawal is real and the invariant reproduces in all 198
cells on a third instrument. Flag any weakening."*

**The withdrawal is undisturbed.** `D2` is struck in the ledger; §0's banner
carries *"The separating example is WITHDRAWN"*; §0's two object headings are
struck in place; the 2×2 cell placement holds; §3's two corrected sentences
hold; and `T1d` prints the withdrawal rather than the withdrawn claim. §3's
`Repaired 1` list — five sites — checks out site by site. Nothing in `ed9cde4`
walks any of it back, and the seam sweep found no second copy of anything it
deleted.

**The invariant is not weakened — it is corroborated on a fourth instrument.**
`kern_d330.py` measures the vertex sets, and hence the dimensions and the
`⊕End` figures, from the combinatorial definition: all 24 cells agree, and
`132 / 132 / 99 / 42` falls out as the sums of squares of the four `n = 6`
rows. `c1`'s own measurement of the 53 dimension cells, the 121 edge cells and
the five multiplicity-2 edges is unchanged and still agrees with the target.

**What IS weakened is the reporting of it, and only that.** 24 of mg-a218's 198
cross-instrument cells no longer compare, and are reported as red. The claim
E1 makes is still true; the instrument that made it can no longer make it, and
does not say so.

---

## 8. PREDICTIONS AGAINST OUTCOMES

`code/branching_audit_d330/PREDICTIONS.md` was written before each script was
run and the misses are kept as written. **15 of 18 right.** The two substantive
misses:

* **P8.** I predicted `c1`'s breakage would be booked as **SELF-ERRORS** — the
  milder failure. It is booked as 24 **FINDINGS**. I predicted the wrong
  failure mode and the real one is worse.
* **P5.** I got mg-a218's `run_all.sh` exit code right for entirely the wrong
  reason: I predicted `c4` and `c5` would still be red. They are green — the
  repair genuinely closed both — and the `1` comes from `c1` and `c3` instead.
  **The number was right and every word behind it was wrong**, which is exactly
  what a bare exit code hides and the reason this audit reports per-script
  verdicts rather than a worst-of.
* **P17** is a miss against my own instrument and is why the seam calibration
  is now built from real deleted passages.

---

## 9. CLAIM LEDGER FOR THIS AUDIT

| # | claim | status |
|---|---|---|
| **F1** | the 24 vertex sets, the four `⊕End` figures `132/132/99/42` and the 10-of-36 count-agrees-set-differs cells reproduce on a fourth instrument built from the combinatorial definition | **MEASURED**, `kern_d330.py`, 867-assertion self-test |
| **F2** | §0's four rows agree with that measurement **character for character**, and the dimensions-only rendering is injective over **all 276** unordered pairs of the 24 cells, 0 collisions | **MEASURED** |
| **F3** | the column is **not** injective on arbitrary vertex sets — `[0:1,1:1]` and `[0:1,2:1]` both render `[1,1]` — but the side condition that makes it faithful is gated, and the gate is load-bearing by deletion: **RED 3 → GREEN 0** | **MEASURED, by construction and deletion** |
| **F4** | no count column stands beside it; the withdrawn `1,2,2,3,3,4` survives at one marked historical site; no digest stands in for the set | **MEASURED** |
| **F5** | every row of §8's status table is true in both directions across `03d7f91`, `2e66d03` and the tree — X2 closed at four sites with markers reaching the committed output, X3/X5/X6/95.7 % genuinely open — over **55 site-checks, 0 findings** | **MEASURED**, `e3`, sharing no code with `t5_labels.py` |
| **F6** | **no fifth site of X2** exists in 728 tracked files: 53 occurrences, 0 unmarked, with the sweep calibrated to catch an injected bare assertion | **MEASURED** |
| **F7** | mg-a218's `c1_branching.py` reports **24 FINDINGS** against the target on the repaired tree, all `target ?`, because mg-13b2 deleted the count table its parser reads; 174 of the 198 cells still compare and still agree | **MEASURED**, re-run in place. **RESOLVED by `mg-58da`:** all 24 established individually as **parser artifacts** (0 confirmed, 0 unknown), the 174 non-findings shown live by 7 of 7 corruption probes, and `c1` widened so a cell it cannot read is a `SELF-ERROR`. It exits 0 with 198 cells compared |
| **F8** | `c3_withdrawal.py` reports 4 unmarked withdrawn-phrase occurrences, all inside `t5_labels.py` and its committed output | **MEASURED** |
| **F9** | mg-a218's document says in the present tense that `c2`, `c4` and `c5` exit 1; the scripts that exit 1 are `c1` and `c3` | **MEASURED**. **RESOLVED by `mg-58da`:** the sentence is struck at its site and replaced by a table of all three revisions, because that ticket's own widening of `c1` moved the exit codes a third time |
| **F8 note** | `c3_withdrawal.py`'s finding is **still OPEN** after `mg-58da`, which reports it rather than closing it: `g4_fleet.py` books it as a FINDING and exits 1, because the set-level property is that *all five* are green and 4 of 5 are | — |
| **F10** | `t5_labels.py`'s population is a hand-written list of 29 with no derived denominator; **8 of the 26** disposition-marked blocks are reached by no needle it looks for, including the whole Sources bibliography | **MEASURED**, by an independent sweep |
| **F11** | the figures `29 labels, 100 checks` and `all 7 fire` are written at **7** sites and derived at **0**; all are correct today | **MEASURED** against a live run |
| **F12** | the seam sweep at threshold **0.80** over **61 522** comparisons returns **17** survivors, **17 marked, 0 unmarked**, with two calibration probes scored | **MEASURED** |
| **NOT CLAIMED** | that anything in the target's mathematics is wrong; that the withdrawal should have been anything else; that `kF(P)` is or is not quasi-hereditary; that the `n = 6` 95.7 % figure was re-derived (it was not, by anyone, and not here either); that any label t5 *does* check is false — none is; that my disposition vocabulary is exhaustive, or that my whole-tree sweep is; that mg-a218's committed outputs should have been regenerated; that anything here is new mathematics | |

---

## 10. REPRODUCE

```
cd code/branching_audit_d330 && ./run_all.sh    # ~4 min, pure Python 3, NO NETWORK
```

Committed outputs: `out_selftest_d330.txt`, `out_e1_vertexsets.txt`,
`out_e2_labels.txt`, `out_e3_dispositions.txt`, `out_e4_rerun.txt`,
`out_e5_seam.txt`.

**Exit codes are the finding channel.** Every `e*.py` exits `0` iff
`SELF-ERRORS == 0` **and** `FINDINGS == 0`, both printed separately, every count
naming its population. **`e2` and `e4` exit `1`; those are F10/F11 and
F7/F8/F9.** `e4` runs mg-a218's scripts in place with their stdout captured
here and **never** redirects into their committed outputs.

There is no network script in this directory. The one object this audit
measures it builds itself.

---

## 11. NOTE FOR pm-onethird

Four things, none of them touching the mathematics and none of them in the
document that was repaired.

1. **Widen `c1_branching.py`'s parser the way `c2`'s was widened**, or make the
   missing count table a **SELF-ERROR** rather than 24 findings. As it stands
   mg-a218's primary script accuses the target 24 times at cells where it has
   gone blind, and its own *"24 cells compared"* line is false.
2. **Put a marker beside the four withdrawn-phrase needles in
   `t5_labels.py`** so `c3` reads them as what they are. One comment.
3. **mg-a218's §10 exit-code sentence is now false** and should carry a note
   saying which commit changed the instrument under it. The committed outputs
   are correctly left alone; it is the present-tense sentence that has rotted.
4. **`t5_labels.py` should derive its denominator.** A sweep of the document's
   own disposition vocabulary, with the covered set subtracted from it, would
   turn *"every disposition label"* from a claim into a measurement — and would
   catch the Sources bibliography, where *"Putcha … NOT read"* is the
   disposition on the deliverable. While it is a hand-written list, the
   `29 labels, 100 checks` figure should be **derived at its three sites**
   rather than typed at seven.

**And one thing this audit is deliberately not doing.** It does not edit the
target document, `STATE.md`, the roadmap, mg-a218's document or any
`Where-This-Lives` file. Whether to fold these back is pm-onethird's call.
