# Independent audit of mg-af28 / `358beff` — the towers-of-algebras / branching-graphs search

**Work item:** mg-6ad0 (pre-filed at mg-af28's filing time). **Date:** 2026-07-30.
**Target:** `docs/OneThird-Branching-Graphs-Where-This-Lives.md` and `code/branching_af28/`.
**Instrument:** `code/branching_audit_6ad0/`, 7 files, 68-assertion self-test, sharing no
code with the audited directory. `./run_all.sh`, ~30 s plus two network fetches.

---

## 0. VERDICT

**The headline is CONFIRMED and comes out stronger than mg-af28 claimed. The apparatus
around it is OVERSTATED, with 2 BROKEN — and both BROKEN items, plus the largest of the
overstatements, are on the NEGATIVE side, which is the defect this ticket was filed to fix.**

> **B1 holds.** `J(D_λ) = [∅, λ]` is not merely an order isomorphism but a **lattice**
> isomorphism — meet and join preserved, checked on every pair, 44 partitions to `n ≤ 7`,
> **0 bad** — on an instrument that builds Young's lattice from the add-a-corner cover rule
> rather than by containment, and computes `f^λ` by the branching recursion rather than by
> hook lengths. The maximal chains of `[∅, λ]` and of `J(D_λ)` are the same set under the
> same map, and both count `f^λ`. **This is the expensive direction and it survives.**

**BROKEN**

| # | where | what |
|---|---|---|
| **X1** | ledger **B2**; `t_young.py` T2 docstring; `out_young.txt` lines 68–70 | *"the posets `P` for which `J(P)` is an interval of Young's lattice are **exactly** the cell posets"* is **false**. Refuted by construction. The three "vanishing fraction" numbers count a strictly smaller family than the one named |
| **X2** | §0 consequence 3; pre-filed at §5 item 5(c) | *"that grid is `J(C_p ⊔ C_q)`, which for `p, q ≥ 1` is **not** an interval of Young's lattice"* is **false**. Refuted by construction, for all 16 `(p,q)` tested |

**OVERSTATED**

| # | where | what |
|---|---|---|
| **X3** | §3 row 3; §2 item 5; ledger **B7** | the "no tower" negative is licensed against Bergeron–Li **§3.1, titled *"Tower of Algebras (Preserving unities)"***. The **same paper's §3.6 is titled *"Tower of Algebras (not Preserving unities)"*** and takes as input *"an algebra injection not necessarily preserving unities"* — exactly what mg-af28 measured concatenation to be. Not mentioned |
| **X4** | ledger **B4**; §2 item 2; §3 row 10 | *"Brown §4.3 reaches the Young graph and no other differential poset"* / *"the lattice it realises is the one Brown §4.3 provably cannot consume"*. At the level where mg-af28's **own** contact lives — finite intervals — **28 of the 33** finite intervals of Young–Fibonacci to rank 6 **are** distributive lattices. I build the `P` with `J(P) =` interval for each of the 28, **0 bad** |
| **X5** | ledger **B6**, **B7** | booked **MEASURED** with sample sizes (6 197 moves; 64 pairs) that cannot do any work. Both answers are forced for **every** poset of **every** size by a two-line argument |
| **X6** | ledger **B8** | the extractor drops `fi`/`ff` ligatures — measured. **2 of the 12** absent-keywords bear a ligature; **0 of the 5** controls does. A genuine *"differential"* in Brown would have scored 0 with every control still green. Re-run ligature-aware: **the finding survives**, the warrant does not |
| **X7** | §2 item 5 | *"which lands back at the classical antichain case"* drops the condition its own §1 row 2 states. The derivation forces `P_n = P_1^{⊔n}` for an **arbitrary** `P_1` |

**Beyond the brief — the standing target.** mg-af28 flagged **three** elementary derivations
as its own (§5 item 5). One is correct and correctly used (5b). One is correct and
**mis-used downstream** (5a → X7). One is **false** (5c → X2). mg-3b51 recorded the first
generation in this arc where beyond-brief material was correct; **that exception did not
hold.** The worst finding in this document is again in material the ticket forbade in the
sentence mg-af28 quotes back at itself in its own §8.

---

## 1. X1 — B2's "exactly" is false, and T2 never tested it

**What B2 says.** *"the posets `P` for which `J(P)` is an interval of Young's lattice are
exactly the cell posets, and they are a vanishing fraction: 6/318 (`n=6`), 8/2 045 (`n=7`),
12/16 999 (`n=8`)"*, marked **MEASURED + CITED**.

**What T2 measures.** `{canon(cell_poset(λ)) : λ ⊢ n}`, and nothing else. The word
*"exactly"* is asserted in the docstring, in the committed output header and in the ledger,
and is **never tested by any line of `code/branching_af28/`**.

**Why it is false.** An interval `[μ, λ]` of Young's lattice is the set of `ν` with
`μ ⊆ ν ⊆ λ`; under `ν ↦ ν/μ` it is the ideal lattice of the **skew** cell poset `λ/μ`. So
the class named is the **skew** cell posets, which strictly contains the straight ones.

**The smallest witness, built and printed** (`out_a2_intervals.txt`, A2a):

* `P` = the **2-element antichain**. Both 2-cell straight shapes `(2)` and `(1,1)` give the
  2-**chain**, so `P` is **not** a cell poset.
* `J(P)` = the diamond. The Young-lattice interval `[(1), (2,1)] = {(1), (2), (1,1), (2,1)}`
  has 4 elements, and `J((2,1)/(1))` is isomorphic to it **as a poset** — checked by
  canonical form, not by eye.

**The corrected counts** (A2c). `n = 8` is behind `SKEW8=1` because it takes ~4 min; its
value was computed by the same function and is stated with that provenance.

| `n` | straight `D_λ` (af28) | skew = interval posets | all posets | af28's fraction | corrected |
|---|---|---|---|---|---|
| 4 | 3 | 11 | 16 | 0.1875 | 0.6875 |
| 5 | 4 | 26 | 63 | 0.0635 | 0.4127 |
| 6 | **6** | **62** | 318 | **0.0189** | **0.1950** |
| 7 | **8** | **149** | 2 045 | **0.0039** | **0.0729** |
| 8 | **12** | **360** | 16 999 | **0.0007** | **0.0212** |

At `n ≤ 3` **every** poset is a skew cell poset (fraction 1.0000).

**What survives and what does not.** Consequence 1's *direction* — "ours contains theirs,
as a vanishing fraction" — survives: the corrected column still falls. Its three numbers do
not; they are understated by a factor of 10 to 30, and the class they count is not the class
B2 names. mg-af28's §0 **headline** is correctly restricted (*"its finite intervals `[∅, λ]`
are exactly the `J(P)` for `P` a cell poset"*) — the defect is that the restriction is
dropped in the ledger, in the code and in the output, and one downstream sentence is false
because of it (§2).

**This correction is not a technicality of the programme.** Intervals `[μ, λ]` index the
**skew** standard tableaux, which are the paths of the same branching graph starting at `μ`
instead of at `∅`. Checked on 7 skew shapes: linear extensions of the skew cell poset =
saturated `μ → λ` paths in Young's lattice, **0 bad** (A2d).

---

## 2. X2 — Brown's own example lattice *is* an interval of Young's lattice

§0 consequence 3, in support of *"Brown does not make the identification"*:

> *"His worked `§4.3` example is the `p × q` grid of lattice paths … that grid is
> `J(C_p ⊔ C_q)`, which for `p, q ≥ 1` is **not** an interval of Young's lattice — `D_λ` has
> a minimum and `C_p ⊔ C_q` does not."*

The reason rules out intervals of the form `[∅, λ]` only. A general interval's poset is a
skew shape and need not have a minimum — and this one does not need to.

**Constructed** (A2b): take `λ = (q+p, q)` and `μ = (q)`. Row 0 keeps columns `q … q+p-1`;
row 1 keeps columns `0 … q-1`; every cell of row 0 is strictly right of every cell of row 1
and strictly above it, so the two blocks are incomparable and `λ/μ ≅ C_p ⊔ C_q`. Verified by
canonical form for all `p, q ∈ {1,…,4}`, **0 bad**, with `|[μ, λ]| = (p+1)(q+1)` in every
case:

```
   p  q   witness lambda / mu     |[mu,lam]|  (p+1)(q+1)
   2  3   (5, 3) / (3,)                  12          12
   4  4   (8, 4) / (4,)                  25          25
```

So Brown's worked example **is** a Young-lattice interval. The sentence is false as written.

**What this does and does not touch.** Consequence 3's actual claim — that Brown does not
make the identification — rests on the keyword census (B8), not on this sentence, and
survives (§6). What is lost is the supporting sentence, and it is lost in exactly the
category the ticket named: an elementary derivation the author added himself and flagged.

---

## 3. X3 — the "no tower" negative was tested against the wrong section of the cited paper

mg-af28 §3 row 3 books towers of algebras **ADJACENT — axiom tested and failed**, on:

> *"Bergeron–Li axiom (2), quoted verbatim from `arXiv:math/0612170` §3.1 … block
> concatenation is injective and multiplicative (0 bad over 64 pairs) and unital in 0 of 64."*

**The quotation verifies.** Re-read from the PDF (A6a): the whole clause, punctuation and
all, occurs once. mg-af28 quoted accurately.

**But §3.1 is titled** `Tower of Algebras (Preserving unities)` — and the same paper has:

> **`3.6. Tower of Algebras (not Preserving unities) and Result 2.`** *"In [3], we consider a
> semi-tower of algebras with `ρ` not preserving unities. If we weaken the condition of `ρ`
> and modify the definitions of induction and restriction we can still get results similar
> as above. … Let `φ : B → A` be **an algebra injection not necessarily preserving
> unities**. …"*

All three strings located verbatim in the PDF (A6c); the two section titles are printed side
by side in `out_a6_quotes.txt`.

**Why this matters.** The **only** clause of axiom (2) that mg-af28 measured to fail is
unitality. Everything else it measured — injective, multiplicative, algebra map — is
precisely the input §3.6 asks for. Condition (1) also holds: `kF(P)` is finite-dimensional
with unit `1_P` (the one-block move), and `A_0 = kF(∅) = k`. Combined with X7 below, which
shows the `ℕ`-grading permits `P_n = P_1^{⊔n}` for **any** `P_1`, the object mg-af28 ruled
out is one whose ruling-out rests on a clause the cited source itself offers to drop.

**What I am *not* claiming.** I am **not** claiming this is a tower. Bergeron–Li's
conditions (3), (4) and (5) — projectivity of `A_{m+n}` over `A_m ⊗ A_n`, the idempotent
condition, and the Mackey-type identity — are **untested by mg-af28 and untested here**, and
testing them is new mathematics, which both tickets forbid. The finding is that **row 3's
"no" is not carried by what was measured**, and that the section which would carry or refute
it sits four pages later in the same PDF.

**This is the ticket's own defect, inside the enumeration meant to cure it.** mg-af28 exists
because mg-d673 found a *"no"* licensed over a candidate space of two. Row 3's *"no"* is
licensed over a definition space of **one**, in a paper containing two.

---

## 4. X4 — "reaches the Young graph and no other" is false where the contact lives

Three places say a version of this: ledger **B4**, §2 item 2, and §3 row 10 (*"the lattice it
realises is the one Brown §4.3 provably cannot consume (T8)"*).

**At the level of whole differential posets the statement is true and empty.** Brown §4.3
needs a **finite** distributive lattice. **No** differential poset is finite — they are
locally finite with infinitely many ranks, which is §2 item 1's own observation. So Brown
consumes **no** differential poset at all, Young's lattice included. mg-af28's contact is
therefore not with Young's lattice; it is with its finite **intervals**.

**At that level the statement is false.** Reproducing T8 exactly on an independently coded
Young–Fibonacci lattice — **33 intervals, 5 non-distributive** (A3b, same numbers) — leaves
**28 distributive** ones. Each is a finite distributive lattice, so Brown §4.3 consumes it,
and by Birkhoff each is `J(P)`. I build `P` from the join-irreducibles of the interval and
check `J(P) ≅` interval by canonical form: **28 reconstructions, 0 bad.**

```
    w              |[0,w]|   P with J(P) = [0,w]
    (2, 1)               5   3 elements, 2 relations
    (2, 2)               7   4 elements, 4 relations
    (2, 1, 1, 2)        11   6 elements, 11 relations
```

So the **Okada monoid's** branching graph (row 10) has **the same kind of index-set contact**
with this construction that mg-af28 headlines for Young — for 28 of its 33 finite intervals.
Row 10's "provably cannot consume" is the reason it gives for booking Okada as merely
ADJACENT, and that reason does not hold.

**Controls on my Young–Fibonacci implementation**, all three PASS: rank sizes are Fibonacci
to rank 6; `DU − UD = rI` below the top with `r = 1`; every interval `[0̂, w]` is a lattice
(the modularity property mg-af28 asserts in its output's reading but does not test).

---

## 5. X5 — two ledger rows whose measurements cannot fail

**B6** — *"no move acts on `L(P)` bijectively without acting as the identity map"*,
**MEASURED**, 6 197 moves over 87 classes, 0.

`F(P)` is a **band**: `x · x = x`. Verified here on all 440 moves to `n = 4`, 0
non-idempotent. So `act(x, ·)` is an idempotent map; an idempotent bijection of a finite set
is the identity. The count is 0 for **every** poset of **every** size, by two lines.

**B7** — *"unital in 0 of 64"*, **MEASURED + QUOTED**.

`1_P` is the one-block move. Concatenation sends `(1_P, 1_Q)` to a **two**-block move, which
is `1_{P⊔Q}` only if a block is empty. All 64 pairs have `|P|, |Q| ∈ {1,2,3}`, so all are
nonempty: **64 of 64 give a two-block image, by counting blocks, with no reference to `F(P)`
at all.**

**Neither is wrong, and neither is hidden** — mg-af28 states both arguments in prose
(`out_young.txt`, §2 item 4; `out_branching.txt`, §1 row 1). The defect is that the **ledger**
books them as MEASURED with a sample size, so a reader who reads only §6 sees evidence where
there is arithmetic. This is exactly what mg-3b51 reported against mg-1953's R1d — *"the
control that must fire CANNOT FAIL"* — recurring one document later in a ledger row instead
of a control.

---

## 6. X6 — B8's controls could not have caught B8's one documented failure mode

mg-af28 §5 item 6 documents that the extraction routine **drops ligatures** — *"it renders
`finite` as `nite`"* — and asks an auditor to re-read the two **quotations**. The same caveat
is not applied to the **census** produced by the same routine, and it should have been.

**Measured** (`out_a5_scan.txt`, Step 1) on Brown's PDF, each control word searched both as
spelt and as a ligature-dropping reader renders it:

| word | as spelt | dropped spelling | count |
|---|---|---|---|
| finite | 2 | `nite` | **57** |
| defined | 0 | `dened` | **26** |
| fixed | 0 | `xed` | **15** |
| different | 0 | `dierent` | **9** |

So `fi` and `ff` are both gone. Now:

* of the **12** absent-keywords, **2** bear a ligature: `differential` and
  `differential poset` (the `ff`);
* of the **5** controls, **0** does: `distributive lattice`, `maximal chains`,
  `left regular band`, `Tsetlin`, `derangement`.

A genuine occurrence of *"differential"* in Brown would have been reported as **0
occurrences with all five controls green.**

**Re-run ligature-aware, B8's conclusion SURVIVES**: all twelve keywords are absent in
**both** spellings, including `dierential` (0) and `dierentialposet` (0). The **finding** is
right. The **warrant** in B8's scope column — *"keyword census … with five present-word
controls"* — is not; the controls establish that the extractor emits text, not that it emits
the two words the finding needs.

**And the extractor drops more than ligatures** (A6b): Brown's *"can be worked out
explicitly"* comes out as `canbeworkedoutexplcitly`. mg-af28's §5 item 6 says both quoted
strings *"are ligature-free and were checked by eye"* — the by-eye check evidently repaired
this, and the repair is correct, but the routine is less trustworthy than that sentence says.

---

## 7. X7 — §2 item 5 drops a condition its own §1 row 2 states

§1 row 2, **correctly conditioned**: *"an `ℕ`-indexed subfamily closed under the `⊔` that the
external product needs satisfies `P_m ⊔ P_n = P_{m+n}`, hence `P_n = P_1^{⊔n}` … **at `P_1` =
a point** this is the antichain sequence, i.e. the classical braid case."*

§2 item 5, condition dropped: *"the `ℕ`-grading it presupposes forces disjoint powers,
**which lands back at the classical antichain case**."*

**The derivation is correct** (put `m = 1` and induct). **The conclusion does not follow**:
`P_1` is an arbitrary finite poset. Exhibited (A4b):

| `P_1` | `\|P_2\|` | `\|F(P_2)\|` | `\|AC(P_2)\|` | `P_2` an antichain? |
|---|---|---|---|---|
| a point | 2 | 3 | 2 | yes |
| the 2-chain | 4 | 26 | 14 | **no** |
| the 3-chain | 6 | 252 | 106 | **no** |
| V | 6 | 730 | 174 | **no** |

The **conclusion** of §2 item 5 ("no tower") still stands on its other leg, unitality — but
that leg is X3, where it is weaker than stated. So §2 item 5 rests on one reason that is
wrong and one that the cited paper offers to remove.

---

## 8. WHAT IS CONFIRMED, AND HOW

| claim | verdict | how, on my instrument |
|---|---|---|
| **B1** `J(D_λ) = [∅, λ]`, maximal chains `= SYT(λ)`, `e(D_λ) = f^λ` | **CONFIRMED and STRENGTHENED** | 44 partitions to `n ≤ 7`; order isomorphism both directions on every pair, **0 bad**; **lattice** isomorphism (meet ↔ intersection, join ↔ union) — a check mg-af28 did not run — **0 bad**; `f^λ` by **branching recursion**, `[∅,λ]` from the **cover rule**; maximal chains of the two sides equal as sets and equal `f^λ`, **0 bad** |
| **B5** `dim kF(P)/rad = \|AC(P)\|` | **CONFIRMED by a disjoint route** | no trace form, no Dickson. Built the `\|AC(P)\|` characters from the product alone, checked each is multiplicative, checked `Φ` is onto, checked `ker Φ` is **nilpotent** in exact rational arithmetic. **0 bad** on every class with `\|F(P)\| ≤ 90`; **20 skipped, each listed**. Independently, Brown's *"Every irreducible representation of `kS` is 1-dimensional"* and his character `χ_X(y) = 1` iff `supp y ≤ X` both located **verbatim** — the character I built is his |
| **B3** (the informative half) | **CONFIRMED** | the truncated column, the one that could have gone either way, reproduced independently: **1 of 405**, the one-element poset. The full column is a theorem, and mg-af28 says so |
| **B4** (whole-lattice reading) | **CONFIRMED** | 30 Young intervals distributive, 33 Young–Fibonacci intervals with 5 non-distributive — reproduced exactly. See X4 for the reading that fails |
| **B8** (the conclusion) | **CONFIRMED** | ligature-aware re-run, all 12 keywords absent in both spellings. See X6 for the warrant |
| both **verbatim quotations** | **VERIFIED** | Bergeron–Li axiom (2) whole clause, 1 occurrence; Brown's `(they are all 1-dimensional)`, 1 occurrence |
| §5 item 5(**b**), `Aut(P) = S_n` iff antichain | **CONFIRMED** | brute force over all 87 classes to `n = 5`, **0 counterexamples** |
| §5 item 5(**a**), the `⊔`-power derivation | **CONFIRMED as a derivation** | but mis-used downstream — X7 |
| §2 item 1's parenthetical, *"a truncation of an infinite lattice is not even a lattice"* | **CONFIRMED** | two distinct elements of the top rank have no common upper bound in the truncation, so no join; a finite lattice has a top |
| every arithmetic figure I could recompute | **CONFIRMED** | 44 partitions, 405 classes, 87 classes, 6 197 moves, 64 pairs, 30 and 33 intervals, 6/318, 8/2 045, 12/16 999, radical 90.4% at `n=5` and 95.7% at `n=6`, 532 339 bytes downloaded |

---

## 9. THE CAVEATS, CHECKED AGAINST WHAT THEY QUALIFY

Every hedge in the deliverable, and whether it is doing work.

| caveat | verdict |
|---|---|
| §0's *"harshest available reading"* — the identification is about **index sets**; the walk's operators are non-invertible; the `S_n`-interaction is **untested** | **DOING REAL WORK, and it is needed.** §0's headline says *"the repo's states `L(D_λ)` are the standard Young tableaux … which are, by Okounkov–Vershik, the Gelfand–Tsetlin **basis**"* — `SYT(λ)` **indexes** that basis, it is not a basis. The caveat corrects the headline. **The frozen commit subject carries the uncorrected form** (*"our states are SYT(λ), the Gelfand-Tsetlin basis of S^λ"*) with no caveat attached |
| §2 item 2's *"I read neither original"* on Stanley 1988 / Byrnes 2012, with the argument using only Stanley | **HONEST AND CORRECTLY SCOPED** — but the argument it protects is X4, which fails for a different reason |
| §2 item 7's *"this argument does not depend on the exact form of the realisation theorem, which I did not read"* | **DOING WORK.** The claim (any graded rooted graph is some AF algebra's Bratteli diagram, so the observation is empty) is insensitive to the theorem's precise form, as stated |
| §2 item 6's *"as stated in the secondary literature; I did not read Bidigare's thesis"* | **HONEST, AND UNAUDITED HERE** — I did not read them either (§10) |
| §3 row 10's *"located from abstracts; not read"* | **HONEST — and X4 shows the row's stated reason fails.** A caveat about *how* a source was located does not protect a claim about *what it says* |
| §5 item 6's ligature caveat | **UNDER-STATED** — it applies to the census too, and the routine drops more than ligatures. X6 |
| §7's *"~5 min"* and the item-by-item size caps in T5 | **ACCURATE.** Every skip is listed with its `\|F(P)\|`, as claimed |
| §8's *"it does not develop mathematics … two elementary one-line derivations"* | **UNDER-COUNTS ITS OWN EXPOSURE.** §5 item 5 lists **three**, not two; of the three, one is false (X2) and one is mis-used (X7) |

---

## 10. WHAT I COULD NOT ESTABLISH

Stated so that nothing here reads as more settled than it is.

1. **The third link of §0's chain — `SYT(λ)` indexes the Gelfand–Tsetlin basis of `S^λ` — I
   did not verify representation-theoretically.** I verified only its combinatorial shadow:
   `Σ_λ (f^λ)² = n!` to `n = 7`, and `#`maximal chains `= f^λ`. mg-af28 named this its own #1
   attack point and it remains the least-tested link in the headline. It is textbook, and I
   am not disputing it — I am recording that neither document has tested it.
2. **§5 item 4 is NOT discharged.** mg-af28 asked an auditor to rebuild Young–Fibonacci
   *"from Stanley (1988) directly"*. **I did not read Stanley (1988).** I coded the same
   published neighbour rule independently and certified it three ways (Fibonacci rank sizes;
   `DU − UD = I` below the top; every interval a lattice), reproducing T8's 33/5 exactly. An
   independent *implementation* is not an independent *definition*.
3. **§2 item 6 (Bidigare → `NSym` → the 0-Hecke tower) is unaudited.** mg-af28 named it its
   own #2 attack point and read none of the three sources; **neither did I.**
4. **Rows 7, 9, 10, 11 of the candidate table are unaudited as searches.** I re-read exactly
   one candidate's source — row 3's — and that re-read produced X3. That is a reason to think
   the other from-abstract rows deserve the same treatment, not evidence that they are wrong.
5. **Whether `A_n = kF(P_1^{⊔n})` satisfies Bergeron–Li conditions (3), (4), (5) under the
   §3.6 weakening is untested by anyone.** Testing it is new mathematics, which both tickets
   forbid. X3 is a finding about the *warrant* for row 3's "no", not a claim that a tower
   exists.
6. **A4a skips 20 classes at `n = 5` with `|F(P)| > 90`**, each listed with its `|F(P)|` in
   `out_a4_algebra.txt`; the largest is the antichain at 541. Nothing is skipped at `n ≤ 4`.
   mg-af28's T5 covers those 20 by its own route, so the union of the two instruments is
   complete to `n = 5`; neither alone is.
7. **The skew counts stop at `n = 8`.** `n ≥ 9` was not computed.
8. **I did not re-run `code/branching_af28/`.** Every number attributed to mg-af28 above is
   read from its committed outputs; every number attributed to me is produced by
   `code/branching_audit_6ad0/`.

---

## 11. PRE-FILED AUDIT OF *THIS* DOCUMENT

1. **Attack X1 and X2 through the meaning of "interval".** My whole refutation turns on
   reading *"an interval of Young's lattice"* as `[μ, λ]` rather than `[∅, λ]`. If the
   intended reading throughout was `[∅, λ]`, X1 collapses to a wording defect and X2
   collapses entirely. I claim it cannot be: §0's headline uses the restricted form
   **explicitly** (`[∅, λ]`), and B2, the T2 docstring and the output header all use the
   unrestricted form — so the document distinguishes them, and X2's sentence reasons about
   the unrestricted one with an argument valid only for the restricted one. Check that.
2. **Attack X3 by reading Bergeron–Li §3.6 properly.** I read it out of the PDF, in flattened
   text, and it defers its details to reference [10] (Li's thesis), which I did not read. If
   §3.6's weakened conditions are *not* satisfiable by anything of our shape for a reason
   visible in [10], X3 weakens to a bookkeeping complaint.
3. **Attack X4 by disputing "where the contact lives".** I argue mg-af28's contact is at
   interval level because Young's lattice is infinite. Someone could argue the contact is
   with the *branching graph* as a whole and that intervals are incidental. I think that
   makes X4 stronger, not weaker — but the reading is mine.
4. **Attack the skew-shape enumeration.** `trimmed_skew_shapes(n)` argues that deleting empty
   rows and columns lands every skew shape inside the `n × n` box. If that trimming argument
   is wrong, the corrected counts in X1 are **lower** bounds and the direction of the
   correction is unchanged, but the numbers move.
5. **Attack my Young–Fibonacci** — same attack mg-af28 pre-filed against its own, and for the
   same reason (§10 item 2). My three controls agree with its three, which is consistency,
   not independence.
6. **Attack X6 as pedantry.** B8's conclusion survives my re-run. The finding is entirely
   about warrant. Whether a surviving finding with a broken warrant is worth a row is a
   judgement, and I have marked it OVERSTATED rather than BROKEN for that reason.
7. **Attack the two `MEASURED`-that-cannot-fail rows (X5) as already-disclosed.** mg-af28
   states both arguments in prose. My claim is only that the **ledger** does not, and the
   ledger is the artefact downstream readers quote.

---

## 12. CLAIM LEDGER

| # | claim | status | scope |
|---|---|---|---|
| **A1** | B1 is an order **and lattice** isomorphism; max chains agree and count `f^λ` | **MEASURED** | 44 partitions `n ≤ 7`, every pair both directions, 0 bad on four separate checks; `f^λ` by branching recursion, `[∅,λ]` by cover-rule closure |
| **A2** | B2's *"exactly"* is **false**; the class is the skew cell posets | **REFUTED BY CONSTRUCTION** | explicit witness (2-antichain / `(2,1)/(1)`), isomorphism checked by canonical form |
| **A3** | the corrected fractions are 62/318, 149/2 045, 360/16 999 | **MEASURED** | skew shapes enumerated in the `n × n` box after trimming; straight counts reproduce af28's 6, 8, 12 exactly |
| **A4** | §0 consequence 3's grid sentence is **false** | **REFUTED BY CONSTRUCTION** | `(q+p, q)/(q) ≅ C_p ⊔ C_q` and `\|[μ,λ]\| = (p+1)(q+1)`, all 16 pairs `p,q ≤ 4`, 0 bad |
| **A5** | Bergeron–Li has a *"not Preserving unities"* tower definition in §3.6 that mg-af28 does not mention | **QUOTED** | three strings located verbatim in `arXiv:math/0612170`; both section titles printed |
| **A6** | 28 of 33 finite Young–Fibonacci intervals are distributive, each `= J(P)` for an explicit `P` | **MEASURED** | 28 reconstructions from join-irreducibles, isomorphism by canonical form, 0 bad; T8's 33/5 reproduced |
| **A7** | B6 and B7 are forced for every poset of every size | **PROVED, then illustrated** | band property verified on 440 moves; block-count argument verified on all 64 pairs |
| **A8** | the extractor drops `fi`/`ff`; 2 of 12 keywords bear one, 0 of 5 controls does; B8's conclusion nevertheless survives | **MEASURED** | four control words found only in the dropped spelling; all 12 keywords 0 in both spellings |
| **A9** | B5 holds by characters + nilpotent kernel, with no trace form and no cited theorem | **MEASURED** | exact rational arithmetic, 0 bad, `\|F(P)\| ≤ 90`, 20 skips listed |
| **A10** | §2 item 5's *"lands back at the classical antichain case"* does not follow | **REFUTED BY CONSTRUCTION** | four non-antichain `P_1` exhibited with their `\|F\|`, `\|AC\|` |
| **NOT CLAIMED** | that a tower of algebras exists over this family; that row 3, 7, 9, 10 or 11 is wrong as a *search*; that `SYT(λ)` is not the GT index set; that mg-af28's headline is wrong in any respect; anything about `λ₂`, `Δ_AT`, the pricing, or publishability | | |

---

## 13. NOTE FOR pm-onethird

* **The headline stands and is stronger than claimed** — it is a lattice isomorphism.
  Nothing here argues against folding §3 back into row Q.
* **Three things should be corrected before anything cites them:** B2's *"exactly"* and its
  three numbers (X1); §0 consequence 3's grid sentence (X2); and row 3's and row 10's stated
  reasons (X3, X4). The first two are in the ledger and the committed instrument output, so
  they will propagate.
* **X3 re-opens a candidate, it does not close one.** Row 3 should read *"axiom (2) of
  §3.1 fails on unitality; §3.6 weakens exactly that clause and was not evaluated"*, which is
  a **hedge, not a no** — the same repair mg-1953 correctly applied to row Q.
* **This document does not edit `docs/OneThird-Branching-Graphs-Where-This-Lives.md`,
  `STATE.md`, the landscape document, or anything in `code/branching_af28/`.** It adds one
  document and one instrument directory.
