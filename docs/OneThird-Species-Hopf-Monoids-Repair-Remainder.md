# The remainder of mg-a61f: what the mg-6f61 repair carried, and the three things it left in the instrument

**Work item:** mg-f8fa. **Date:** 2026-07-30. **Target:** the mg-6f61 repair
(`83ac472`) of mg-7d75 (`6a22fbc`), against the independent audit mg-a61f
(`8e61d1a`, `docs/OneThird-Audit-mg-7d75-Species-Hopf-Monoids.md`).
**Computation:** permitted, used, committed (`code/species_remainder_f8fa/`,
`run_all.sh`, ~15 s, 2 114-assertion self-test, `NO NETWORK`).

---

## 0. THE HEADLINE OF THIS TICKET

**mg-6f61 carried every one of the four items this ticket was filed for — in the
document. It left three of them standing in `code/species_7d75/`, which is the
copy a successor re-runs, and its checker could not have caught that because it
reads one file.**

> `code/species_repair_6f61/check_doc.py` opens
> `docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md` and nothing else. Its
> negative half — *every false sentence must survive only inside the strike that
> replaces it* — is the right test. **It was applied to half the artefact.**

So this ticket is not *"mg-6f61 missed four findings"*. It is: **a repair whose
scope was the prose, and a defect class that lives in both.** Three findings
were corrected in one place and left in force in the other. The count is
measured rather than asserted: `code/species_remainder_f8fa/w3_scope.py`, run
unmodified against `code/species_7d75` **as it stood at `83ac472`**, reports
**12 problems**; against the tree after this repair, **0**.

**Nothing here softens the headline, and nothing here is a retraction.** Every
conclusion the corrected numbers were cited for survives, and one of them comes
out **stronger** than it was. See §5.

---

## 1. THE ITEM-BY-ITEM CHECK AGAINST THE BRIEF

The brief for this ticket listed four items and instructed: *if mg-6f61 already
fixed any item below, say so and skip it.* Here is that check, done against the
merged text rather than against the commit message.

| brief item | in the document | in the instrument | this ticket |
|---|---|---|---|
| **1.** four hedges (S1, S12, §6 item 6, §10 item 2) treat §2.3's identity as an unlocated measurement, and route a search that cannot succeed | **CARRIED by mg-6f61.** S1 upgraded to *QUOTED + PROVED*; S12 *WITHDRAWN*; §6 item 6 corrected; §10 item 2 struck and closed; the boxed three-line proof sits in §0; §7 item 3 re-scoped and demoted | the `t4` cap is described as an instrument bound, which is correct | **SKIPPED — not redone.** One line added to the `t4` row of the instrument README so the cap is not read as the statement's range |
| **the successor they point at** | **CARRIED.** *"DO NOT FILE THE SUCCESSOR LITERATURE SEARCH"* is in §0 and §10 item 2. **Verified here: no such work item exists** — `mg list` has no filed literature-search ticket on this row, so there is nothing to delete, only something to keep unfiled | — | **SKIPPED**, with the negative recorded: the search was never filed |
| **2a.** T3d's four candidates are two statements each computed twice | **CARRIED** (§0, §2.2, S2, §14.1 row X4) | **LEFT STANDING** — see §2 | **REPAIRED, and the count is now computed** |
| **2b.** control (ii)'s 1 442 fire on a type mismatch; repair the control, keep the conclusion | **CARRIED** (§5, §6 item 5, S7, all three stating the conclusion survives) | **LEFT STANDING** — see §3 | **REPAIRED, and the set equality is now measured** |
| **3.** the Aguiar–Ardila §12 divergence was not pre-filed and must be recorded with the same treatment as AM §17.5 | **CARRIED.** §4 carries a three-row table splitting the divergences by *pre-flagged? YES / NO / NO*, §1 carries the corrected quotation, §14 item 3 draws the generalisation, S10 records it | `r3_quotes.py` holds the post-repair verdicts | **SKIPPED — not redone** |
| **4.** ledger S4 is unverified; check **every occurrence**, not only the ledger | **CARRIED in the document** — §0 item 4, §0's headline bullet, §3's boxed two-row table, §6 item 1, §9 rows 3 and 11, S4, S5 | **LEFT STANDING** — see §4 | **REPAIRED at the occurrences the document does not cover** |

**Three of six rows were already done and are not redone.** The brief was
written before `83ac472` merged; it is right about the findings and out of date
about who carried them.

---

## 2. X4 — THE CONTROL COUNT, CORRECTED IN PROSE AND STILL PRINTED BY THE RUN

`t3_bidigare.py` headed T3d

> `T3d  THE COMPARISON -- four candidate identifications, three are controls`

and its vacuity branch read *"the three controls did not fire"*. The committed
`out_t3_bidigare.txt` carried the header verbatim. mg-6f61 corrected §2.2, §0,
S2 and the instrument README, and did not open the file that prints it.

**Repaired at source, and the correction is now COMPUTED rather than restated.**
A new **T3e** measures the statement the count rests on:

> `c^U_{S,T}(Sol, B) = c^U_{T,S}(Sol, A)` for every pair of subsets —
> **convention B is identically the opposite algebra of convention A**.

| `n` | pairs `(S,T)` | `B(S,T)` vs `A(T,S)` | **CONTROL:** `B(S,T)` vs `A(S,T)` |
|---|---|---|---|
| 1 | 1 | 0 | 0 |
| 2 | 4 | 0 | 0 |
| 3 | 16 | **0** | **2** |
| 4 | 64 | **0** | **26** |
| 5 | 256 | **0** | **170** |

`T3` now **fails** if the left column is not 0, and fails if the control does
not fire at exactly `n = 3, 4, 5` — it cannot fire at `n ≤ 2`, where `kS_n` is
commutative, and a routine that returns 0 on everything establishes nothing.
Both columns are reproduced independently by `w1_opposite.py`, which rebuilds
the descent algebra from permutations and compares products as **multisets**,
so no expansion in the `d_T` basis is assumed on that side.

**So T3d is ONE control, RUN TWICE.** `iso/B`, listed as a control, is the
surviving identification seen in a mirror.

**NOT WITHDRAWN.** The comparison is still discriminating — 472 mismatching
structure constants at `n = 5` separate *isomorphism* from *anti-isomorphism* —
and Bidigare's Theorem 10.13 still reproduces entry for entry. **Only the
control count was overstated.**

---

## 3. X5 — CONTROL (ii), AND THE ONE PLACE THE NEAR-MISS READING SURVIVED

`code/species_7d75/README.md`, under the heading ***Conventions that have bitten
this repo before***, said:

> ~~*"These are different maps and `t5` control (ii) measures **how
> differently**: 1 442 closure failures, 252 associativity failures, 11 020
> compatibility failures."*~~

That is exactly the near-miss reading mg-a61f refuted, sitting in the section a
successor reads to avoid re-importing an error. `t5_hopf_monoid.py` printed the
three counts with no reading attached at all.

**Repaired at source, and measured as a SET EQUALITY rather than a coincidence
of counts** (`t5` control (ii), and `w2_typemismatch.py` from disjoint code):

```
pairs tested                                        11301
product-closure FAILURES                             1442
pairs with BOTH ground sets non-empty                1442
  failures with an empty side                            0
  failures NOT returning the empty composition           0
```

`μ_{S,T}` takes its two factors on **disjoint** ground sets; the Tits product
intersects blocks; across disjoint non-empty sets every intersection is empty.
So the Tits product returns the **empty composition on a non-empty ground set**,
which is not a face of it. Four predictions were written before the run and all
four were met.

**The controls, and they are what make this a reading rather than a story.**

| control | product-closure failures | what it shows |
|---|---|---|
| `μ_{S,T}` uncorrupted (concatenation) | **0** | the column is not firing on everything |
| **type-CORRECT corruption** — mg-6f61's control (v), last block of `x` merged into first of `y` | **0** | **a wrong product that respects the type fails this column 0 times.** The column is a type check, not a distance |
| control (ii), the Tits product | **1 442** | every both-non-empty pair, and only those |
| control (ii) **with its own guard removed** | **11 300** | the guard — fall back to concatenation when either face is empty — is what confines the failures. Without it the control measures nothing |

**THE CONCLUSION IS NOT WITHDRAWN, AND IT COMES OUT STRONGER.** *The band
product is invisible to the Hopf structure* — so nothing mg-ebd8 or mg-af28
measured about the walk, `λ₂` or `Δ_AT` is a Hopf-theoretic invariant. It rests
on the two maps' **domains**, which makes it true at **every** ground set rather
than on `[4]`, and no count on either side can strengthen or weaken it. A
corrected number printed beside an unmarked conclusion reads as a retraction;
this one is marked, in the instrument as well as in the document.

---

## 4. S4 AND S5 — *"CHECK EVERY OCCURRENCE, NOT ONLY THE LEDGER"*

The document does this thoroughly: §0 item 4, §0's headline bullet, §3's boxed
two-row table, §6 item 1, §9 rows 3 and 11, and ledger rows S4 and S5. **The
instrument did it nowhere.** `t4_one_operation.py` printed

> `Sol(S_n) / rad  =  k^{Pi_n / S_n}  =  the character ring of S_n.`

and `t6_fock_and_record.py` printed *"`K(Π)` = symmetric functions, whose
degree-`n` component is the character ring of `S_n`"* — **both inside runs
ending `TOTAL BAD: 0`**, with nothing to tell a reader that the two equalities
in that line are not of the same kind. The first is measured here. **The second
is ledger S4: cited to Solomon (1976) and to Garsia–Reutenauer / Atkinson,
neither of which was read — not by mg-7d75, and not by the audit.**

Both now carry the scope in place, naming the ledger row, both unread sources,
and the specific untested link (that Solomon's labelling by **cycle types**
agrees with the orbit labelling by **block sizes**). `w3_scope.py` enforces it:
**every** line in `code/species_7d75` identifying the semisimple quotient with
the character ring must carry the marker within eight lines, in the same file.
Eight occurrences, all marked; the rule fails loudly if a future edit adds a
ninth.

**The asymmetry a reader will not otherwise see.** The poset half got the trace
form at **87/87 with no size cap** and **179/179 out of sample at `n = 6`**, plus
an outright proof. The `S_n` half got two citations to unread papers. Both sit
in a document whose headline says *yes*.

---

## 5. WHAT THIS TICKET DOES **NOT** DO, AND WILL NOT

* **It does not soften the headline.** The identity `(kF(P))^{Aut(P)}/rad =
  k^{AC(P)/Aut(P)}` is a **three-line corollary** of AM §10.10 plus the Reynolds
  operator, with **no `n` dependence**, confirmed through a harder instrument
  than mg-7d75 used. Hedging it further would be a second wrong report, and it
  would read as caution.
* **It does not re-open the four hedges, the quotation table, or the ledger's
  S4 wording.** mg-6f61 carried them; §1 is the check, not a re-do.
* **It does not file the §10 item 2 literature search**, and confirms that
  none was ever filed — so there is nothing to delete, only something to keep
  unfiled. If one is ever filed, its brief must open by saying §2.3 is already
  located as a corollary, so a null result reads as *"not stated"* and not as
  *"not true"*.
* **It does not read Solomon, Garsia–Reutenauer/Atkinson, AM 2020, AM 2017,
  Saliola or Commins.** S4 is **marked**, not closed. Fetching them is new
  verification and would need its own controls.
* **It does not touch `code/species_audit_a61f/`.** That battery re-ran
  **unmodified** against the tree after this repair and produced **byte-identical
  output**, `A4 TOTAL BAD: 1` (which is X1) and 0 everywhere else.
  `code/species_repair_6f61/check_doc.py` still reports **PASS, 0 problems**.
* **It conducted no independent search for defects mg-a61f and mg-6f61 both
  missed.** The same limitation those two recorded about themselves applies
  here, and for the same reason: this ticket's list came from an audit, so it
  is complete only to the extent that audit was. **The evidence that this is a
  live risk rather than a formality is this ticket itself** — three findings sat
  in the instrument for a full repair cycle because the only checker pointed at
  the prose.

---

## 6. THE GENERALISATION, AND IT IS ABOUT WHERE A CHECKER POINTS

**A repair is not finished when the document is right. It is finished when the
thing a successor RE-RUNS is right.**

mg-6f61 built the strongest artefact in this arc: a checker that requires every
false sentence to survive only inside the strike that replaces it. It is a real
control and it passes. It reads **one file**, and three corrected statements
lived in the other twelve — including one in a section headed *Conventions that
have bitten this repo before*, which exists precisely to stop a reader
re-importing an error, and which was itself carrying one.

This is the same shape as mg-a61f's §14 finding one level up. A pre-filed attack
list *"aims attention"*; a checker aims it harder, because a passing checker is
read as coverage. **§8 C3 was outside every beam pointed at the document.
`t3_bidigare.py` line 207 was outside every beam pointed at the code — and the
beam pointed at the code did not exist.**

Operationally, and it is one line: **when a repair corrects a statement that
also appears in code or in committed output, the checker for that repair must
take the code directory as a target too.** `w3_scope.py` is that checker for
this arc, it takes the directory as an argument so it can be aimed at any tree,
and it was **observed to fail before it was observed to pass** — 12 problems at
`83ac472`, 0 now.

**And a false negative was found in it while doing exactly that, and is kept on
the record rather than tidied away.** Its first version accepted a bare
*"REPAIRED"* or *"CORRECTED"* near a forbidden string as evidence the string was
being quoted rather than asserted. The pre-repair README disarmed it **by
accident**: an unrelated *"the error mg-1953 repaired"* four lines above the
near-miss bullet made the bullet score `ok` on a tree where it was plainly
false. A checker that can be disarmed by an adjacent unrelated word is a
checker that reports coverage it does not have — which is the finding of this
whole document, arriving one level down and against its own instrument.

---

## 7. REPRODUCE

```
cd code/species_remainder_f8fa && ./run_all.sh   # ~15 s, NO NETWORK
cd code/species_7d75          && ./run_all.sh   # ~46 s, the repaired source instrument
cd code/species_repair_6f61   && ./run_all.sh   # ~30 s, mg-6f61, UNMODIFIED -- still PASS
cd code/species_audit_a61f    && ./run_all.sh   # ~2 min, mg-a61f, UNMODIFIED -- byte-identical
```

Committed outputs: `out_selftest.txt` (2 114 assertions), `out_w1_opposite.txt`,
`out_w2_typemismatch.txt`, `out_w3_scope.txt`, and **`out_w3_scope_before.txt`
— the same checker against the pre-repair tree, `FAIL (12 problems)`, committed
on purpose.**
