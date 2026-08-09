# `STATE.md` — the *"either disjunct"* CLAIM, repaired at three rows, and `mg-fa70`'s own *"greps clean"* falsified one directory further on (`mg-3329`)

**Landing ticket.** No mathematics is re-derived, no population re-enumerated, no number in the
corpus moves, no claim is withdrawn. What is repaired is a **scope clause**: `L2` is a
**DISJUNCTION** — *"a dominant standard eigenvector is monotone in the distinguished order, **or at
least yields a low-conductance prefix**"* — so *"under L2"* is *"under either disjunct"* with the
words removed, and the constant `C₃^(III) = 1` is established on the **FIRST** disjunct only.
`mg-fa70` repaired that at its origin (`bb6a0ff`, thirteen sites in
[`OneThird-C3-PrefixCapture-mg-76b2.md`](OneThird-C3-PrefixCapture-mg-76b2.md)) and **flagged, did
not edit,** the two `STATE.md` sites, because `STATE.md` is `pm-onethird`'s. This lands them.

**Sequencing.** `mg-a1db` landed `mg-65f5`'s R1 patch into the same file at `25cc5b2`, before this
ran, and was directed not to touch `:164`/`:169`. **It did not:** its five edits are at `:13`,
`:74`, `:76`, `:79`, `:81`, it kept the file at 210 lines, and `:164`/`:169` are byte-identical to
their pre-`mg-a1db` state. No unanticipated overlap to report. The sentences here were nonetheless
found by **content**, not by the line numbers the ticket carried.

---

## 1. What changed — three rows, and only three

`git diff` on `STATE.md` touches exactly `:116`, `:164`, `:169`. Line count is unchanged (210), and
the pipe count of each table row is unchanged, so **no `STATE.md` line reference anywhere in the
corpus moves.**

### 1.1 `:164` — the contested sentence, carried VERBATIM

The ticket that produced `mg-fa70` recorded *"`STATE.md` carries NEITHER contested sentence …
so nobody re-checks it."* That was false at `:164`, which read:

> *"…the omission is not optimistic but **CORRECT**, because `C₃^(III) = 1` **under either disjunct
> of L2**, so under Step 3 there is nothing to omit (mg-76b2)."*

Replaced with `mg-fa70` §3.1's proposed text, **clause only**, the rest of rider (ii) intact:

> *"…the omission is not optimistic but **CORRECT ON L2's FIRST DISJUNCT**, because `C₃^(III) = 1`
> **there**, so under Step 3's **first clause** there is nothing to omit; on L2's **SECOND**
> disjunct there is no **CONVERSION** to charge for, but the delivered prefix's constant is **L2's
> own and is UNNAMED IN THE SOURCE**, so `C₃` is **UNQUANTIFIED there rather than `1`**."*

**A fourth spelling of the same claim sat in the very next sentence and the ticket did not name
it:** *"**(ii) IS CONDITIONAL ON L2** AND L2 IS OPEN"*. `L2` is **weaker** than its first disjunct,
so claiming (ii) is conditional on `L2` claims a weaker hypothesis suffices — an over-claim in the
same direction as the sentence it follows. Repaired to name the first disjunct and to point at row
`9` for the mark.

### 1.2 `:169` — the sentence the ticket asked about is fine; the row it sits in was not

Three edits, matching `mg-fa70` §3.2's three-way split:

| | what | done |
|---|---|---|
| (1) | *"under L2's second disjunct there is no `C₃` either, because the prefix is the output"* | **NOT struck, NOT rewritten** — it is TRUE. The clause `mg-fa70` called *"a nicety"* is **appended beside it** rather than folded into it: what the second disjunct establishes is that there is **no CONVERSION STEP to charge for**; what it does **not** establish is `Φ ≤ √(2ε_spec)` rather than `K√(ε_spec)`, an effective `C₃ = K²/2` whose `K` is L2's own. So on that branch `C₃` is **RELOCATED, not eliminated**. |
| (2) | the row's **HEADLINE**, *"under L2, `C₃^(III) = 1` UNIFORMLY IN `n`"* | **REPAIRED** to *"under L2's FIRST DISJUNCT"* — the defect in a different spelling, and the same repair `mg-76b2`'s own THEOREM header took at `bb6a0ff`. The row's GREEN title now carries the scope too, since this row's own standing rule (`mg-957a`) is that the condition belongs **at** the claim. |
| (3) | *"mg-76b2's 'either disjunct' framing is doing real work"* | **QUALIFIED.** It was an **inherited endorsement**, offered as the reason row `9`'s `FP✗` is not fatal. After `mg-39bf` §2.2 the framing does **LESS** work: leaning on the second disjunct means leaning on the branch whose constant is unnamed. The rescue is **real but NOT free** — it buys the LEMMA-count reduction, not a quantified `C₃` — and the row presented it as free. It now **cites** `mg-76b2` §9 row 7's `(a)`/`(b)` split instead of asserting the framing. |

### 1.3 `:116` — ledger row 9, found by sweeping for the CLAIM

Row 9 read `| 9 | L2 standard-eigenvector monotonicity | FP✗ | false as stated (2/126) | n=6 data |`.
It has **no matching phrase** and a phrase-grep returns nothing here. It is the same defect
**pointing the other way**: the row names `L2` and marks it *false as stated*, when what is refuted
is L2's **first disjunct**. `L2` itself is **OPEN, not refuted** (`mg-76b2` §9 row 23). This matters
directly, because `:169` leans on row 9 as the reason the *"either disjunct"* framing is load-bearing.

Repaired to name the first disjunct, quote the disjunction, and state that L2 as a disjunction is
`OPEN`. **Nothing is withdrawn:** the `FP✗` mark and the `2/126` stand, on the first disjunct.

---

## 2. The remedy is an artifact of the same kind as the defect

Each clause added here was checked against **both** disjuncts before landing, and against
`mg-fa70` §4's two recorded over-corrections:

- **The LEMMA-count claims were left alone, deliberately.** *"This REDUCES `C₃` TO L2"* (`:169`'s
  title) and *"L3 IS NOT AN INDEPENDENT LEMMA"* (`:169`'s body) **survive on both disjuncts** —
  `mg-76b2` §9 row 8, repaired: *"the LEMMA count falls on both disjuncts; the CONSTANT is
  discharged only on the first."* Withdrawing either would have been `mg-fa70` §4 item 2's
  over-correction, and an over-correction is **not** the safe error here: it re-opens a lemma count
  the programme has banked.
- **The second disjunct is nowhere struck and nowhere called false.** It is **UNQUANTIFIED**, which
  is different and weaker. Both branches stay visible (`mg-fd7c`'s (I)=(III) precedent).
- **Restatement replaced by citation where possible** — the one place inheritance has worked in this
  lineage (`mg-76b2` §9 rows 9/10 needed no edit because they read *"CONDITIONAL on 6"*). Row 9 now
  points at `:169` instead of restating it; `:169`'s framing clause points at `mg-76b2` §9 row 7
  instead of asserting it; `:164`'s condition points at row `9`.
- **Two figures are quoted that this ticket did not measure**, and both say so **in the row**: the
  `L2` quote (`spectral_near_ordinal_sum_program.tex:560–566`) and the `5×`-unquantified
  *"low-conductance"* count. **That `.tex` is not in this repository.** They are carried on
  `mg-76b2` §2 and `mg-fa70` §12's at-source check — inherited claims, labelled as inherited,
  which is the whole lesson of the ticket that produced them.

---

## 3. `code/chain_selection_9461/s1_chains.py` — repaired, and here is why that is not re-opening `mg-9461`

`mg-fa70` §3.3 flagged `:86`: chain (I)'s open-statement label read `"L2 (either disjunct) — Step 3
as written"`, and chain (I) is the `C₃`-**free** chain (`ε_dem = ε_leak²/2`), so on the second
disjunct that label asserts precisely the unestablished half. The ticket permitted repair **only if
`mg-9461` is not re-opened.**

**Two more sites in the same file, found by sweeping for the claim rather than the phrase:** the E3
guard message (`:75`, *"`C_3 = 1` is PROVEN (under L2)"*) and chain (III)'s report row label
(`:134`, *"C_3 = 1, PROVEN under L2"*). Only these last two reach the committed output.

**Numbers-neutrality is VERIFIED, not asserted:**

1. `python3 s1_chains.py` reproduced the committed `out_s1_chains.txt` **byte-identically** before
   any edit — so the script is deterministic and the baseline is exact.
2. After the three label edits, the regenerated output differs from the committed one at **exactly
   three lines** (`:17`, `:34`, `:101`), **all of them label text**. Every `ε_dem`, every ratio,
   every count, every guard verdict is unchanged.
3. `s0_selftest.py` output is unchanged. `s2`/`s3` do not import `s1_chains`.

No formula, parameter, population, threshold or verdict is touched, and `mg-9461`'s ruling is not
re-opened. Chain (I)'s `needs` string is never printed at all.

---

## 4. FLAGGED, NOT EDITED — and one of them falsifies a recorded clean check

Out of this ticket's scope (`STATE.md` plus the one flagged instrument). Listed with line numbers so
that *"not repaired"* and *"not looked at"* stay distinguishable.

### 4.1 `mg-fa70`'s *"`code/c3_prefix_capture_76b2/` (greps clean)"* is FALSE

`mg-fa70` §2.1 records that directory on its **checked and deliberately left** list as *"greps
clean"*. Re-run for the **claim** instead of the phrase:

```
code/c3_prefix_capture_76b2/s2_sweep.py:2    """s2 — THE SWEEP, and the theorem `C_3 = 1 given L2`.
code/c3_prefix_capture_76b2/s2_sweep.py:57   print("s2 — THE SWEEP, and the theorem  C_3 = 1  given L2")
code/c3_prefix_capture_76b2/out_s2_sweep.txt:2   s2 — THE SWEEP, and the theorem  C_3 = 1  given L2
code/c3_prefix_capture_76b2/s4_budget.py:85  print("  s2 shows that under L2 it does not degrade anything, …")
code/c3_prefix_capture_76b2/out_s4_budget.txt:23   s2 shows that under L2 it does not degrade anything, …
```

`grep -rn "either disjunct" code/c3_prefix_capture_76b2/` returns **0**. `grep -rnE "under L2|given
L2"` returns **5** (plus `PREDICTIONS.md:68`, never edited). So *"greps clean"* is **true of the
phrase and false of the claim** — which is `mg-fa70`'s own headline finding, committed one directory
further on, in the same amendment that stated it. **This is the sixth instance in this lineage,
and the second time a recorded clean check has been the thing that was wrong.**

### 4.2 `docs/OneThird-ChainSelection-mg-9461.md` — two live sites survived `mg-fd7c`'s repair

`mg-fd7c` repaired `:140` (`c20ad80`) and `:36`/`:290` are correctly scoped to the first disjunct.
Still carrying the unqualified claim:

- `:102` — *"a constant `mg-76b2`'s theorem sets to **1** under L2"*.
- `:328` — the currency table's `C₃^(III)` row: *"**flat — and PROVEN flat, under L2**"*.

### 4.3 `code/c3_audit_a94c3/a3_currency.py` and its output

`:210`, `:217` (the `C5` banner *"chain (III) at C_3 = 1, under L2"*), `:241` (*"CONFIRMED on this
population, under L2's hypothesis"*), mirrored at `out_a3_currency.txt:89`, `:95`, `:107`. The
measured population **is** the 1032 first-disjunct posets, so these are **true as measured and
under-scoped as written** — the cheapest possible place for the next instance to hide.

### 4.4 Checked and deliberately LEFT

- **`STATE.md:169`, *"`C₃^gap` is not `1` under L2, so the substitution is FALSE"*.** Blanket scope,
  but a **negative** claim erring **conservative** — it converts an unknown into a refusal, not into
  a licence. Left for exactly the reason `mg-fa70` §2.1 left the identical phrasing in its title;
  repairing one and not the other would be worse than repairing neither.
- **`STATE.md:15`**, *"`C₃` unquantified and NOT an L4 question"* — pessimistic, not the disjunct
  defect, and `:164`'s rider (ii) is the sentence that qualifies it.
- **`STATE.md:164`'s title** *"UNBLOCKS mg-6bc2 ON ITS OWN SECOND DISJUNCT"* and its
  *"mg-6bc2's FIRST disjunct"* — these are **`mg-6bc2`'s** disjuncts, not `L2`'s. Not this defect.
- **The mermaid `C → D` edge (`:65`)** — states L3's `FP` support at `125/126`; carries no `L2` scope
  claim.
- **All `PREDICTIONS.md` files** — never edited, per standing practice.

---

## 5. Scope

- **No mathematics re-derived.** `C₃` not re-derived, `L2` not attempted, no instrument written, no
  population re-enumerated, no number moved, no claim withdrawn.
- **`mg-9461` not re-opened** — label strings only, numbers-neutrality verified by byte-diff (§3).
- **Two files changed** besides this record: `STATE.md` (3 lines) and
  `code/chain_selection_9461/s1_chains.py` (+ its regenerated `out_s1_chains.txt`, 3 label lines).
- **`Op-Form` not edited.** `roadmap.md` does not exist in this tree and was not created.
