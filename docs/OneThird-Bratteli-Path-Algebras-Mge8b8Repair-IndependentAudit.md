# Independent audit of the mg-db09 repair — mg-e8b8 / `2e66d03`

**Work item:** mg-a218, pre-filed in the same action as its parent. **Date:**
2026-07-30. **Target:** `docs/OneThird-Bratteli-Path-Algebras-Where-This-Lives.md`
and `code/branching_locate_db09/` at commit `2e66d03`. **Instrument:**
`code/branching_audit_a218/`, `run_all.sh`, ~1.5 min, 80 001-assertion
self-test, one reproduction script and five test scripts.

**This audit shares no code with either instrument it audits.** `kern_a218.py`
rebuilds Temperley–Lieb diagrams, link states, the cell modules, the cellular
bilinear form, `L(n,p) = V(n,p)/rad⟨,⟩` and the trace form of the regular
representation from the definitions. It is the **third** instrument to measure
this object: mg-db09's `T1b2` is the first, mg-2060's `B1a`/`B1b` the second.

---

## 0. HEADLINE

**The withdrawal is real, and the invariant survives a third instrument in
every cell. Two things the repair did not do: its own repaired table still
reports a COUNT where the hypothesis is about a SET, and it silently repaired
two of the three sites of the one finding it books as "deliberately NOT
repaired".**

* **The example was WITHDRAWN, and my brief says that is acceptable and must
  not be scored as failure. It is not scored as one.** It is stated as a
  withdrawal and not as a refinement, it is corrected **at source** and not
  only in prose, the verdict D4 is re-attributed to the quoted theorems, and
  D2 is struck through in the ledger. **38 of 38 named text checks pass**,
  and the sweep for the withdrawn phrases finds **8 occurrences across 16
  files, every one of them inside a withdrawal or correction** (§4).
* **THE INVARIANT REPRODUCES IN EVERY CELL.** Measured here under
  Vershik–Okounkov's definition at every parameter: **24 vertex-count cells,
  53 vertex-dimension cells and 121 edge cells, 0 disagreements** with
  mg-e8b8's `T1b2`. All five multiplicity-2 edges the document names are
  confirmed one by one, and **no sixth exists** in the 121 cells. Uniqueness,
  integrality, non-negativity and `Σ_q m_q·dim L(n-1,q) = dim L(n,p)` are
  checked on every one of the 53 character solves (§2).
* **X1 — THE VERTEX COLUMN IS STILL A COUNT.** §0's repaired four-row table
  heads its vertex column *"# irreducibles at `n = 1…6`"* and prints
  `1, 2, 2, 3, 3, 4` **identically for `β = 3`, `β = 2` and `β = 1`**.
  Measured, the vertex **sets** at `β = 3` and `β = 1` differ at **4 of the 6
  levels**. The document substantiates *"the vertex set is not even the same"*
  only at `β = 0`. **This is the repair's own failure mode in miniature — a
  second matching statistic standing in for identity of a structure** — and
  the evidence to fix it is already in the repair's own `T1b2` output (§3).
* **X2 — TWO SITES WERE REPAIRED AND BOOKED AS UNREPAIRED.** §8's
  *"Deliberately NOT repaired, and each is open"* lists mg-2060's X2. The
  repair in fact removed *"Path-pair **basis** survives"* from §0's 2×2 table
  and *"the pairs-of-paths basis exists throughout"* from `T1d`'s printed
  output — 2 of X2's 3 sites — with **no correction note at either**, while
  **6 other sites** in the same document carry an explicit
  `CORRECTED (mg-e8b8)` or `WITHDRAWN (mg-e8b8)` marker. **The changes go
  the right way**; the disclosure does not (§5).
* **5 of 5 committed outputs regenerate BYTE-IDENTICALLY** against the repaired
  code, on this audit's own scratch copy, and the stated `699 520` assertions
  and four `TOTAL BAD: 0` lines are what the run produces (§7).
* **The near-miss disclosure SURVIVED.** All 6 pre-filed attack items are
  present; **every sentence of the pre-repair §4 item 3 is present verbatim**,
  with its outcome appended in place rather than rewritten (§4).
* **The seam sweep found one stale site out of 34**, at threshold **0.80**, and
  it is X2's — see §6, which also says what would have counted.

---

## 1. WHAT MY BRIEF TOLD ME, AND THE ONE THING NO LIST NAMES

My brief says its list is a floor and requires me to audit at least one thing
no list names, and to say what I chose.

**What I chose: the retraction of record, as a record.** My brief tells me to
verify that the retraction is *recorded in the document*. It does not tell me
to check whether the record is **accurate**, or whether the place the document
points a reader to **still contains it**. The document stakes a specific
factual claim — 19:50 delivery, 20:45 retraction, `f4eaea6`, *"55 minutes"* —
and a retraction whose own record is wrong is precisely the failure the
document is arguing against. `docs/roadmap.md` is rebuilt several times an hour
in this repo, so *"see the roadmap"* is a pointer that can rot.

**Result: the record holds where it matters and is loose where it does not.**
The headline really is in `docs/roadmap.md` at `6c0f0da`; `f4eaea6` really is
the retraction; the **current** roadmap still carries it, still names the 19:50
delivery, and no longer asserts the headline as a result; and the document
carries the retraction independently. **Two notes, recorded and not scored as
findings:** the commits are at **19:52:23** and **20:42:49**, so the two stated
clock times are rounded in *opposite* directions and the stated **55 minutes**
is **50.4 minutes** measured commit-to-commit. The overstatement runs *against*
the author's interest — a longer time-to-retract is the worse number — and 55
is exactly right given the two times the document states, which are the
roadmap's own. It is booked as a note because nothing rests on it.

I also audited, unprompted, whether the repair's **own new** cross-instrument
claim is true (§2), and whether §8's *"deliberately NOT repaired"* list is
accurate (§5). The second of those is X2 and it is a finding.

---

## 2. THE PRIMARY TARGET — THE INVARIANT, MEASURED IN EVERY CELL

My brief: *"if the repair re-establishes the example, verify the branching
graph is measured under the definition in play, IN EVERY CELL … a second
matching statistic is not proof either."*

**The repair does not re-establish the example — it withdraws it.** But it
*also* measures the invariant, at every parameter, and puts the measurement in
the document as the reason for the withdrawal. So the measurement is
load-bearing and I measured it myself.

**Definition used, and it is the one in play** because it is the one the target
quotes: vertices at level `n` are the irreducible modules of the `n`-th
algebra, edges are the restriction multiplicities. Graham–Lehrer: the
irreducibles of `TL_n(β)` are the non-zero `L(n,p) = V(n,p)/rad⟨,⟩`.
Multiplicities recovered from characters on the diagram basis of `TL_{n-1}`,
with **uniqueness, integrality, non-negativity and
`Σ_q m_q·dim L(n-1,q) = dim L(n,p)` all checked** on every solve.

### The vertex set, as a set of labelled vertices

| `β` | `n=1` | `n=2` | `n=3` | `n=4` | `n=5` | `n=6` |
|---|---|---|---|---|---|---|
| 3 | `[1]` | `[1,1]` | `[1,2]` | `[1,3,2]` | `[1,4,5]` | `[1,5,9,5]` |
| 2 | `[1]` | `[1,1]` | `[1,2]` | `[1,3,2]` | `[1,4,5]` | `[1,5,9,5]` |
| 1 | `[1]` | `[1,1]` | **`[1,1]`** | **`[1,3,1]`** | **`[1,4,1]`** | **`[1,4,9,1]`** |
| 0 | `[1]` | **`[1]`** | `[1,2]` | **`[1,2]`** | `[1,4,5]` | **`[1,4,5]`** |

(entries are `dim L(n,p)` for `p = 0, 1, …`, bold where they differ from `β = 3`)

### Agreement with the target, cell by cell

| what | cells compared | population | disagreements |
|---|---|---|---|
| vertex counts | **24** | every `(β, n)`, `β ∈ {3,2,1,0}`, `1 ≤ n ≤ 6` | **0** |
| vertex dimensions | **53** | every `L(n,p)` `T1b2` prints, `2 ≤ n ≤ 6`, plus every vertex I measure | **0** |
| edge multiplicities | **121** | every ordered pair `(p,q)` of vertices at consecutive levels, every `β`, `2 ≤ n ≤ 6` | **0** |

**The four `Σ_λ dim End(L_λ)` figures at `n = 6` reproduce: `132 / 132 / 99 /
42`.** All **five** multiplicity-2 edges the document names by name are
confirmed individually, and **there is no sixth**: over all 121 edge cells, the
number of cells with multiplicity ≥ 2 that the document does not name is **0**.

**A second matching statistic is not proof — so here is a third, disjoint
route.** My self-test computes `dim A/rad` twice on 24 `(n, β)` pairs: once as
`Σ_p (rank of the Gram matrix)²` and once as the **rank of the trace form of
the regular representation**, which never sees a cell module. **0
disagreements.** All five published Ridout–Saint-Aubin controls reproduce:
`TL_n(2)` and `TL_n(3)` semisimple for every `n ≤ 6`, `TL_n(0)` semisimple
**exactly** for `n` odd, `TL_n(1)` not semisimple for `3 ≤ n ≤ 6`.

### The repair's own new cross-instrument claim, measured

§0 says `T1b2` *"agrees ROW FOR ROW with mg-2060's B1a/B1b on a disjoint
instrument"*. No list names this; it is a claim the repair itself introduced.
Parsing both committed outputs and adding my own:

| instrument | rows published |
|---|---|
| mg-e8b8 `T1b2` | 53 |
| mg-2060 `B1b` | 53 |
| mg-a218 (this audit) | 53 |

**All three agree exactly — dimension and every edge — on 53 of the 53 distinct
`(β, n, p)` rows published by any of them.** The claim is confirmed, and this
audit is the third instrument.

---

## 3. X1 — THE REPAIRED TABLE'S VERTEX COLUMN IS A COUNT

My brief: *"Check the vertex sets, not only a count."*

### What the document prints

§0's four-row table, the one the repair rewrote, has a column headed
**"# irreducibles at `n = 1…6`"**:

| `β` | … | # irreducibles at `n = 1…6` | branching, **MEASURED** |
|---|---|---|---|
| 3 | | 1, 2, 2, 3, 3, 4 | multiplicity-free |
| 2 | | 1, 2, 2, 3, 3, 4 | multiplicity-free |
| 1 | | 1, 2, 2, 3, 3, 4 | **NOT multiplicity-free** |
| 0 | | **1, 1, 2, 2, 3, 3** | **NOT multiplicity-free** |

and the prose under it reads **"The vertex set is not even the same."** followed
by *"At `β = 0` the tower has fewer irreducibles at every even level."*

### What is measured

**The counts in that column are all correct** — 24 of 24 cells agree with my
measurement. But a vertex of a branching graph is an **irreducible module**,
and counting them is a statistic *about* the vertex set, not the vertex set.
Measured over every ordered pair of parameters at every level — **36
(parameter-pair, level) cells** — there are **10 cells where the count agrees
and the set does not**:

| pair | level | both have | dims |
|---|---|---|---|
| `β=3` vs `β=1` | `n=3` | 2 vertices | `[1,2]` vs `[1,1]` |
| `β=3` vs `β=1` | `n=4` | 3 vertices | `[1,3,2]` vs `[1,3,1]` |
| `β=3` vs `β=1` | `n=5` | 3 vertices | `[1,4,5]` vs `[1,4,1]` |
| `β=3` vs `β=1` | `n=6` | 4 vertices | `[1,5,9,5]` vs `[1,4,9,1]` |
| `β=2` vs `β=1` | `n=3,4,5,6` | (the same four) | (the same four) |
| `β=1` vs `β=0` | `n=3` | 2 vertices | `[1,1]` vs `[1,2]` |
| `β=1` vs `β=0` | `n=5` | 3 vertices | `[1,4,1]` vs `[1,4,5]` |

**So the `β = 1` graph and the `β = 3` graph have the same number of vertices
at every level and do not have the same vertices at four of the six.**

### Why this is a finding and what it is not

**It is not a false statement.** The document nowhere claims the vertex sets
agree at `β = 1`; its sentence is scoped to `β = 0` and that sentence is true —
*"fewer irreducibles at every even level"* holds at all 3 even levels and the
odd levels are equal, checked here.

**It is a finding because of what the repair is for.** The defect being
repaired was *equality of one statistic taken for identity of the structure* —
the path-pair count `132`. The repaired table then presents the vertex set
through **another single statistic, a count**, printed identically down three
of its four rows. A reader who takes the repaired table at face value learns
that the graphs at `β = 3, 2, 1` have the same vertices; they do not. The
correction is one column wide and **the evidence is already in the repair's own
`T1b2` output**, which prints `dim L(n,p)` on every row — it simply does not
reach the table.

**Scope.** This is a defect in one column of one table, not in the
measurement, the withdrawal, or the verdict. Everything the instrument prints
is right.

---

## 4. WHAT THE REPAIR GOT RIGHT — 38 OF 38 TEXT CHECKS

My brief: *"If the repair WITHDRAWS the example, that is acceptable and must
not be scored as failure. Verify the withdrawal is complete and stated as a
withdrawal, and that the verdict is attributed to the theorem."*

**All of it passes.** 38 named checks, each looking for an exact string in a
named place; no check is passed by a synonym.

* **Stated as a withdrawal, not a refinement.** The word appears in the §0
  banner; *"The separating example is WITHDRAWN"*; D2 struck through in the
  ledger with **WITHDRAWN**; §8 says explicitly *"not as a refinement, not as
  a clarification"*; nothing dresses it as a clarification.
* **The verdict is attributed to the theorem.** *"The verdict of §0 survives,
  but on the THEOREM and not on the builds"*; the Wedderburn equivalence is
  stated as the basis; D4's status reads *"a consequence of the QUOTED
  THEOREMS, not a synthesis of the builds"*; and §0 says the 2×2 table *"is not
  the evidence for the verdict"*.
* **Corrected at source, not only in prose.** I swept **16 files** — the
  delivered document plus every `.py`/`.txt`/`.md`/`.sh` in
  `code/branching_locate_db09/` — for **5** withdrawn phrases. **8
  occurrences, every one inside a withdrawal or correction.** This is the check
  that caught mg-73df's X3, where the prose was fixed and the instrument still
  asserted the error inside a run ending `TOTAL BAD: 0`. It does not fire here.
* **D10 reads as a conjecture.** The ledger row says **A CONJECTURE. NOT A
  RESULT**; §2 row 2 says **CONJECTURED TO CONTAIN BOTH**; the §0 block is
  headed *"THIS SECTION IS A CONJECTURE, AND IT WAS DELIVERED AS A RESULT"*;
  the umbrella answer is *"open"*, not *"yes"*. **What would establish it is
  concrete: 4 numbered steps, step 1 being READ PUTCHA.**
* **The retraction is IN the document**, at **both** the §0 banner and §5's
  *D10 in full* — `f4eaea6`, 19:50, 20:45 — together with the sentence saying
  why it is repeated. See §1 for the two notes on its accuracy.
* **The other unverified items are each marked, not silently retained.** The
  `n = 6` **95.7%** is *"remains arithmetic"* and *"re-derived by nobody"*;
  *"a band is a von Neumann regular monoid"* is **NOT CHECKED. One line, and it
  is mine.**; **CMPX (A2)(ii), (A4), (A5), (A6)** are *"all untested"*; the
  Putcha characteristic hypothesis is **NOT VERIFIED against the primary
  source**; Putcha is **NOT read**. T1a's *"iff"*, §1's unconditional Prop. 1.4,
  D5's *"each listed with its size"* and §7's derivation count are each named
  as open — with the qualification in §5 about what *"open"* now means for X2.

### The near-miss disclosure survived, and I tested it by deletion

My brief: *"If the repair deletes it while fixing the row, that is a defect."*

It does not. **All 6 pre-filed attack items are present.** I extracted §4 item
3 **from the pre-repair document at `03d7f91`**, split it into sentences, and
required each to be present verbatim in the repaired document: **6 of 6
sentences survive**, including *"its dimension shadow"* and *"An auditor should
check whether that shadow is enough for what §0 claims."* The outcome is
**appended in place**, and the document states that deleting the disclosure
would remove the only evidence the near-miss discipline works.

---

## 5. X2 — TWO SITES REPAIRED, BOOKED AS UNREPAIRED

**Found by the seam sweep**, not by inspection, which is what the sweep is for.

§8 of the repaired document says:

> **Deliberately NOT repaired, and each is open** — they were named by mg-2060
> and are outside this ticket: **T1a's *"iff"*** (mg-2060 X2) — false in the
> "if" direction …

and §4 item 3's appended outcome says the two further defects are *"**not
repaired by mg-e8b8**, whose scope was the two withdrawn claims"*.

**mg-2060's X2 names three sites.** Checked against `03d7f91` and `2e66d03`:

| site | pre-repair | post-repair |
|---|---|---|
| T1a's *"a basis … exists **iff** `dim A = Σ(#paths)²`"*, in `t1_tl.py` and its committed output | present | **still present** |
| §0's 2×2 table cell, *"Path-pair **basis** survives"* | present | **REMOVED** — now *"Path-pair *count* survives"* |
| `T1d`'s printed *"so the pairs-of-paths basis exists throughout"* | present | **REMOVED** — and *"the BASIS"* became *"the COUNT"* |

**2 of X2's 3 sites were changed by the very commit that books X2 as
untouched.** Neither carries a correction note. The same document carries an
explicit `CORRECTED (mg-e8b8)` / `Corrected (mg-e8b8)` / `WITHDRAWN (mg-e8b8)`
marker at **6 sites** — lines 76, 209, 423, 447, 573 and 576 — so the omission
is not the document's house style.

**The direction matters and I state it plainly: the changes are right.** They
delete a false claim mg-2060 proved false. The defect is disclosure, and it has
two costs. A successor reading §8's list goes looking for *"Path-pair basis
survives"* in the 2×2 table and finds *"Path-pair count survives"* — which
reads as though the auditor mis-transcribed the target. And the repo's own
standing rule from mg-8e30 — a commit that measures something it also modifies
must publish the post-commit state — is the same rule one level up: **a commit
that repairs something it also books as unrepaired must say so.**

**Not overstated.** X2's *primary* site — T1a's *"iff"* header — **is** still in
force, printed verbatim by `t1_tl.py` and standing in the committed
`out_t1_tl.txt` inside a run ending `TOTAL BAD: 0`. About that site §8 is
exactly right.

---

## 6. THE SEAM CHECK, AND ITS THRESHOLD

My brief: *"Duplicate-sweep the block quotes for a stale copy of any passage an
earlier repair also touched. Report the similarity threshold. If it finds
nothing, say what would have counted."*

**Threshold: 0.80**, `difflib.SequenceMatcher` ratio on whitespace-, markup-
and case-normalised text; minimum passage length 60 characters after
normalisation.

**Method, and it is the literal reading of the brief.** A *touched passage* is
a line a correcting commit **deleted**: every `-` line of `2e66d03` (the
repair) and `f4eaea6` (the retraction) — **101 passages, 88 from the first and
13 from the second**. The swept population is **1 360 units in 6 files**: the
delivered document (574), mg-2060's audit document (353), `docs/roadmap.md`
(178), and the target instrument's `out_t1_tl.txt` (87), `t1_tl.py` (127) and
`README.md` (41). **137 360 comparisons.**

**34 distinct sites survive at or above the threshold.** Each is classified —
**EDIT IN PLACE** (the survivor is itself an added line of the same commit, so
the question is whether the edit is disclosed) or **SECOND COPY** — and each is
a finding only if **unmarked**, meaning no withdrawal/correction/status marker
within 12 lines either side.

**Result: 33 marked, 1 unmarked.** The unmarked one is
`code/branching_locate_db09/t1_tl.py:368` at ratio **0.926** — *"What survives
without semisimplicity is the **COUNT**, not the"* against the deleted *"is the
**BASIS**, not the"*. That is X2, and it is §5.

**What would have counted, and it did not fire.** A copy of any deleted line
standing somewhere with no correction marker near it. Two real deleted lines
are scored explicitly in the output as calibration: `T1d`'s *"Multiplicity-
freeness is held FIXED across those four rows"* — matched among the deleted
passages at **0.935**, best surviving copy at **0.928** in mg-2060's audit
document, **MARKED** by that document's own *"1 BROKEN"*; and §3's *"the
branching graph is unchanged and multiplicity-free"* — best surviving copy
**0.806**, **MARKED**. Had either been standing unmarked, it would be a finding
of the mg-73df shape.

**Two marker lists were widened after their first run, and neither silently.**
`c3` gained `"failing phrase"` and `"asserted"` after the first run flagged the
one sentence that *performs* the withdrawal; `c4` gained `"not read"` and
`"NOT evaluated"` after the first run flagged two bibliography lines whose
**added** text already carries that status. Both widenings are recorded in the
source with the reason. **The X2 finding survives both widenings.**

---

## 7. REPRODUCTION

`c0_repro.sh` copies `code/branching_locate_db09/` to a scratch directory, runs
its `run_all.sh` **against the repaired code**, and diffs.

| file | result |
|---|---|
| `out_selftest.txt` (699 520 assertions) | **IDENTICAL** |
| `out_t1_tl.txt` | **IDENTICAL** |
| `out_t2_gz.txt` | **IDENTICAL** |
| `out_t3_ours.txt` | **IDENTICAL** |
| `out_t4_quotes.txt` | **IDENTICAL** |

**5 of 5, population: the five committed `out_*.txt` files.** The document's
stated `699 520` assertions is what the run produces, and **4 of the 4 test
scripts** end `TOTAL BAD: 0`. mg-e8b8's claim that `t2`, `t3` and `t4` are
untouched and byte-identical holds against a scratch copy this audit made
itself.

*(My first version of this check counted the self-test as a fifth `TOTAL BAD`
file and reported "4 of 5". The self-test prints `selftest: 699520 assertions,
all passed` and is not one of the four test scripts. That was my instrument's
error and the population is corrected in the script with a note.)*

---

## 8. PREDICTIONS AGAINST OUTCOMES

`code/branching_audit_a218/PREDICTIONS.md` was written **before any script was
run**, and the two wrong predictions are kept there as written.

| # | script | predicted | actual | |
|---|---|---|---|---|
| 1 | `selftest_a218.py` | 0 | **0** | right |
| 2 | `c1_branching.py` | 0 | **0** | right |
| 3 | `c2_vertexsets.py` | 1 | **1** | right |
| 4 | `c3_withdrawal.py` | 0 | **0** | right |
| 5 | `c4_seam.py` | **0** | **1** | **WRONG** |
| 6 | `c5_record.py` | **0** | **1** | **WRONG** |
| 7 | `c0_repro.sh` | 0 | **0** | right |
| 8 | `run_all.sh` | 1 | **1** | right |

**6 of 8 right; the 2 wrong are wrong in the same direction** — I predicted the
artifact clean on the seam and on the record, and it was not, both times
because of X2. I predicted the seam sweep would *"find nothing"* and wrote out
what would have counted; what counted was a class I had not imagined — not a
stale second copy but an **undisclosed in-place edit**, which only became
visible once I classified survivors into EDIT IN PLACE and SECOND COPY. The
prediction I got right and cared most about — X1, the vertex column — was
predicted in words as well as in exit code, before the measurement.

---

## 9. CLAIM LEDGER FOR THIS AUDIT

| # | claim | status |
|---|---|---|
| **E1** | the branching graph of `TL_n(β)` under VO's definition agrees with mg-e8b8's `T1b2` on **24** vertex-count cells, **53** vertex-dimension cells and **121** edge cells, 0 disagreements; all 5 named multiplicity-2 edges confirmed and no sixth in the 121 | **MEASURED, third instrument**, with uniqueness/integrality/non-negativity/dimension checked on all 53 solves |
| **E2** | `dim A/rad` by two disjoint routes — Gram ranks and the trace form of the regular representation — agrees on **24 of 24** `(n, β)` pairs; 5 of 5 published RSA controls reproduce | **MEASURED**, `selftest_a218.py`, 80 001 assertions |
| **E3** | §0's vertex column is a **count**, identical for `β = 3, 2, 1`, while the vertex **sets** differ at **10 of the 36** (parameter-pair, level) cells where counts agree — 4 of them between `β = 3` and `β = 1` | **MEASURED**. A defect of one table column; **not** a false sentence, and the instrument already has the evidence |
| **E4** | the withdrawal is complete and stated as a withdrawal, the verdict is attributed to the quoted theorems, D10 reads as a conjecture with 4 concrete steps, the retraction is in the document at two sites, and every other unverified item is marked | **MEASURED**, 38 of 38 named text checks |
| **E5** | the near-miss disclosure survived: 6 of 6 pre-filed items present, 6 of 6 sentences of the pre-repair §4 item 3 present **verbatim**, outcome appended in place | **MEASURED by deletion test** against `03d7f91` |
| **E6** | mg-2060's X2 was repaired at **2 of its 3 sites** by the commit that books it as *"deliberately NOT repaired"*, with no correction note at either; the third site is genuinely untouched | **MEASURED**, pre/post text at both commits |
| **E7** | the seam sweep at threshold **0.80** over **1 360 units in 6 files** against **101** deleted passages returns **34** sites, **33 marked, 1 unmarked**, and the unmarked one is E6 | **MEASURED**, with the two calibration probes scored |
| **E8** | 5 of 5 of the target's committed outputs regenerate byte-identically against the repaired code | **MEASURED**, `c0_repro.sh`, this audit's own scratch copy |
| **E9** | `T1b2` agrees **row for row** with mg-2060's `B1a`/`B1b` — 53 of 53 rows, all three instruments, dimension and every edge | **MEASURED**; the repair's own new claim, named by no list |
| **E10** | the retraction record: the headline is in the roadmap at `6c0f0da`, `f4eaea6` is the retraction, the current roadmap still carries it | **MEASURED**. **Note, not a finding:** the commits are 19:52:23 and 20:42:49, so *"55 minutes"* is 50.4 measured, the rounding running against the author's interest |
| **NOT CLAIMED** | that the withdrawal should have been a re-establishment; that anything in the target's mathematics is wrong; that `kF(P)` is or is not quasi-hereditary; that the `n = 6` 95.7% figure was re-derived (it was not, by anyone, and this audit did not either); that CMPX (A2)(ii)/(A4)/(A5)/(A6) were evaluated; that a band was checked to be von Neumann regular; that my searches were exhaustive; that anything here is new mathematics | |

---

## 10. REPRODUCE

```
cd code/branching_audit_a218 && ./run_all.sh    # ~1.5 min, pure Python 3, NO NETWORK
```

Committed outputs: `out_selftest_a218.txt`, `out_c0_repro.txt`,
`out_c1_branching.txt`, `out_c2_vertexsets.txt`, `out_c3_withdrawal.txt`,
`out_c4_seam.txt`, `out_c5_record.txt`.

**Exit codes are the finding channel, deliberately.** Every `c*.py` exits `0`
iff `SELF-ERRORS == 0` **and** `FINDINGS == 0`, and both numbers are printed
separately, so a non-zero exit never means the instrument is broken.
~~`c2`, `c4` and `c5` exit `1`; those are E3, E7 and E6.~~ **Every count in every
output names its population.**

**CORRECTED (`mg-58da`), and this sentence is why the correction is here rather
than in a commit message: it was written in the present tense about code a
reader will run, and a reader who ran it got another answer.** The struck
sentence was true when this audit was taken, at `286d5030`. It is not true now,
and the exit codes have moved twice since:

| revision | scripts exiting `1` | why |
|---|---|---|
| `286d5030` — as audited | `c2`, `c4`, `c5` | E3, E7, E6, as written above |
| `ed9cde4` — after the mg-13b2 repair | `c1`, `c3` | the repair closed E3/E6/E7 and *opened* two: `c1`'s vertex parser went blind on the rewritten `T1b2` (i) and booked it as 24 findings against the target; `c3` swept up the withdrawn phrases sitting unmarked in the repair's own new `t5_labels.py` |
| after `mg-58da` | `c3` only | `c1`'s parser is widened to read either form and to book what it cannot read as a **SELF-ERROR**, so it exits `0` with all 198 cells compared; `c3` remains **OPEN** — it is mg-d330's second finding and is not repaired there |

**`out_c1_branching.txt` is deliberately NOT regenerated**, the call `mg-a318`
made for `mg-8a5c` and `mg-13b2` made for `c2` here: a committed audit output is
the record of what that audit found, not a live gate. `code/branching_audit_58da/g1_provenance.py`
re-runs `c1_branching.py` at `286d5030` against the target as it stood there and
confirms that file **byte for byte** — so the record is checkable rather than
merely preserved.

There is **no network script in this directory at all** — every source this
audit needs was fetched and committed by mg-db09 and by mg-2060, and this audit
reads those.

---

## 11. NOTE FOR pm-onethird

Two corrections, both small, neither touching the mathematics.

1. **§0's four-row table should print the vertex *set*, not its size** — the
   dimensions are already in `T1b2`'s output. One column. Without it the
   repaired table asserts, by omission, the thing the repair withdrew: that a
   matching statistic is identity of a structure.
2. **§8's "deliberately NOT repaired" list should say that 2 of X2's 3 sites
   were in fact repaired here**, and the two edited sites should carry the
   correction note the commit's other five sites carry. The edits are right;
   only the books are wrong.

**And one thing this audit is deliberately not doing.** It does not edit the
target document, `STATE.md`, the roadmap, or any other `Where-This-Lives` file.
Whether to fold these back is pm-onethird's call.
