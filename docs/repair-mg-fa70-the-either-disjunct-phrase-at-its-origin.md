# `mg-fa70` — *"UNDER EITHER DISJUNCT OF L2"*, REPAIRED AT ITS ORIGIN — and the grep that was recorded as already run, wasn't

**Work item.** `mg-fa70`. Flagged by `mg-fd7c` §7 and deliberately not edited by it, because it
is a question about `mg-76b2`'s document rather than about `mg-9461`'s. Correct call.

**Target.** [`docs/OneThird-C3-PrefixCapture-mg-76b2.md`](OneThird-C3-PrefixCapture-mg-76b2.md) —
the **origin** of the phrase. `mg-9461` inherited it; `mg-fd7c` repaired the inheriting copy at
`c20ad80`; the source still read unqualified, so the phrase would simply have propagated again.

**Not done, per the ticket and stated so nobody re-walks it.** `C₃ = 1` is **not** re-derived
(`mg-76b2`, audited `mg-94c3`, repaired `mg-01ea` at `ade980b`). L2 is **not** attempted.
`mg-9461` is **not** re-opened. No instrument was written and no number in the corpus moves.

---

## 0. Verdict

> **THE QUALIFIER IS NEEDED AT THE ORIGIN, AND IT IS NEEDED AT THIRTEEN SITES RATHER THAN THE
> TWO THE TICKET NAMED — INCLUDING THE LEDGER ROW THAT WAS THE PHRASE'S ACTUAL LICENCE.**
>
> `mg-76b2`'s **theorem** is not in question and nothing it proves has changed. What is
> over-stated is the **scope clause**. On L2's **second** disjunct the constant is
> **RELOCATED, not eliminated**: what that disjunct establishes is that there is no
> **conversion step** to charge for — the prefix is the output, L3 never runs — and what it
> does **not** establish is that the delivered prefix meets `Φ_pref ≤ √(2ε_spec)` rather than
> `K√(ε_spec)`, which is an effective `C₃ = K²/2`. The constant moves into L2's own unnamed
> *"low-conductance"*.
>
> **THE LEDGER CHECK THE TICKET SENT ME TO RUN HAS AN ANSWER, AND IT IS THE WORST SITE IN THE
> DOCUMENT.** `§9` **row 7** read *"L2's second disjunct also removes `C₃`; **both disjuncts
> do**"* with the bare label **PROVEN**. That is the machine-readable summary row, it is the
> entry every downstream *"either disjunct"* cited as its licence, and it is now **split
> (a)/(b)**: (a) removes `C₃` as L3's conversion loss — **PROVEN**; (b) removes the constant
> from the chain — **NOT ESTABLISHED**. Rows 6 and 8 qualified with it; rows 9 and 10 needed
> **no** edit and that is itself the finding — they read *"CONDITIONAL on 6"*, a **live pointer
> rather than a copied phrase**, so they inherited the repair automatically. That is the one
> place in this lineage where inheritance worked, and it worked because the row cited a row
> instead of restating its content.
>
> **AND THE TICKET'S OWN SCOPE PREMISE IS FALSE — WHICH IS THE FIFTH INSTANCE, NOT THE FOURTH.**
> The ticket records *"STATE.md carries NEITHER contested sentence — `mg-fd7c` grepped before
> starting and I am recording that so nobody re-checks it."* Re-run, the grep returns **two**
> `STATE.md` hits, and `STATE.md:164` carries the contested sentence **verbatim**:
> *"…the omission is not optimistic but **CORRECT**, because `C₃^(III) = 1` **under either
> disjunct of L2**, so under Step 3 there is nothing to omit (mg-76b2)."* The phrase is landed,
> in the programme's own state ledger, in the very row `mg-76b2` §10 was written to amend.
> `STATE.md` is `pm-onethird`'s: **flagged with exact proposed replacement text, not edited.**
>
> **AND THIS AMENDMENT REPRODUCED THE DEFECT IT REPAIRS, ON ITS FIRST PASS.** §6's four-chain
> prose reads *"which **under L2** it does not"* — the same claim with the words *"either
> disjunct"* absent, which is exactly the spelling a grep for the phrase cannot see. It was on
> my own **"checked and left"** list until the sweep was re-run for the **claim** instead of the
> **phrase**. Recorded as a thirteenth site rather than folded silently into the twelve.

---

## 1. The finding, and why it is not *"`mg-76b2` was wrong"*

`mg-39bf` §2.2 turns on two statements that are easy to read as one:

| | statement | status |
|---|---|---|
| **TRUE** | on L2's second disjunct the prefix is the output, so there is **no conversion step** to charge for | **PROVEN** — a reading of the source at `:560–562` |
| **NOT ESTABLISHED** | the delivered prefix meets `Φ_pref ≤ √(2ε_spec)` | the constant is **RELOCATED** into L2's own unnamed *"low-conductance"* |

`mg-76b2`'s theorem is proved on L2's **first** disjunct — monotone `v` ⟹ every swept threshold
set is already a prefix ⟹ the restriction costs exactly `1` — and `mg-94c3` confirmed it there at
`1032/1032`. That proof is sound and is not re-derived here. What asserts more than the second
disjunct supports is the **clause covering both with one phrase**.

### 1.1 Re-checked at source, not taken from `mg-39bf`

In `spectral_near_ordinal_sum_program.tex` (603 lines):

- *"low-conductance"* occurs **5×** — `:40`, `:325`, `:500`, `:525`, `:562` — and is
  **unquantified at every one**.
- The open-lemma preamble (`:552–553`): *"The programme becomes a proof if the following are
  established **with adequate constants**."*
- **New citation, not previously used in this lineage** — the Remark at `:327–331`:
  > *"Cheeger theory does not by itself imply that the cut is a prefix. That requires
  > monotonicity of the dominant standard eigenvector in the distinguished order, **or a direct
  > prefix theorem**."*

  The source itself calls the second disjunct *a direct prefix theorem* — an unproved theorem,
  with no constant attached. So the second disjunct's constant is not merely unnamed by
  `mg-76b2`; it is **unnamed by the source**.

**The adversarial check on my own repair, run because it could have killed it:** is there
anywhere the source *does* pin the second disjunct's constant? If so, the qualifier would be
wrong. Five occurrences checked, none quantified, and the one Remark that names the alternative
names it as an open theorem. The repair survives its own falsification arm.

---

## 2. The thirteen sites

Twelve are tabulated in the target document's new **§12.1**, plus §6 recorded at **§12.2**.
Summarised by kind:

| kind | sites |
|---|---|
| **ticket-named** | §0 verdict headline (`:42`), §10's proposed `STATE.md` text (`:557`) |
| **ledger — the check the ticket asked for** | §9 rows **6**, **7**, **8** |
| **theorem statement** | §3 header (*"Under L2"* → *"Under L2's FIRST disjunct"*), §3's `[PROVEN, given L2 …]` label |
| **the strongest single form** | §4 item 2, *"**Both disjuncts of L2 kill `C₃`**"* |
| **consequences** | §4 clause (b) (*"follows from L2 alone"*), §4's L3 closing (*"Given L2, L3 holds with loss 1"*), §10's `mg-845e` proposal |
| **title and banner** | `H1`, and a new `mg-fa70` amendment paragraph beside `mg-01ea`'s |
| **found on re-sweep, phrase absent** | §6's four-chain prose |

**Split by disjunct rather than deleted, per the ticket and per `mg-fd7c`'s (I)=(III) precedent:
BOTH BRANCHES STAY VISIBLE.** Nowhere is the second disjunct struck, and nowhere is it called
false — it is **unquantified**, which is a different and weaker thing, and the document now says
which.

### 2.1 Checked and deliberately left

Recorded in target §12.2 so that *"not repaired"* and *"not looked at"* stay distinguishable:
§1's verbatim source quotes; §9 rows 9/10 (live pointers, inherit correctly); §9 row 23; §4
item 3; §5, §7, §8, §11; the title's *"the gap-form `C₃` is NOT 1 under L2"* (blanket scope, but
a **negative** claim erring conservative — it converts an unknown into a refusal, not into a
licence); `code/c3_prefix_capture_76b2/` (greps clean); and `PREDICTIONS.md`, never edited.

---

## 3. `STATE.md` — judged, flagged, not edited

`STATE.md` is `pm-onethird`'s. `mg-76b2` §10 is explicit that *"nothing here has been written into
`STATE.md`"* and that `:164` is `mg-345e`'s row. `mg-fd7c` §7 flagged rather than edited. Same
here — with exact replacement text supplied so it lands in one paste.

### 3.1 `:164` — carries the contested sentence VERBATIM

The ticket's premise was that it does not. It does. Proposed replacement, **clause only**, the
rest of `(ii)` intact:

> *"…the omission is not optimistic but **CORRECT ON L2's FIRST DISJUNCT**, because
> `C₃^(III) = 1` there, so under Step 3's first clause there is nothing to omit; on L2's
> **second** disjunct there is no CONVERSION to charge for but the delivered prefix's constant is
> L2's own and is UNNAMED IN THE SOURCE, so `C₃` is UNQUANTIFIED there rather than `1`
> (mg-76b2, qualified mg-39bf §2.2 / mg-fa70)."*

### 3.2 `:169` — the sentence the ticket asked me to judge on its own terms. **The answer splits three ways, and the ticket was right about the part it named and missed the part beside it.**

1. ***"under L2's second disjunct there is no `C₃` either, because the prefix is the output"* —
   TRUE, and the ticket's guess that it *"may be fine, since it is a statement about the
   conversion"* is correct.** Under `mg-76b2`'s own dictionary `C₃` **is** L3's conversion loss,
   and on that disjunct L3 does not run. **Not struck and not repaired.** One clause naming what
   it does *not* establish would make it safe to quote alone; that is a nicety, not a defect.
2. **The row's headline — *"under L2, `C₃^(III) = 1` UNIFORMLY IN `n`"* — IS the defect, in a
   different spelling.** `L2` is a disjunction, so *"under L2"* is *"under either disjunct"* with
   the words removed. **This is what needs repairing at `:169`**, and the ticket did not name it
   because the search was for the **phrase** rather than for the **claim** — the same miss that
   left `:164` uncaught, and the same one I made at §6.
3. ***"mg-76b2's 'either disjunct' framing is doing real work"* — an inherited endorsement,
   needs a clause.** It is offered as the reason L2's `FP✗` monotonicity clause is not fatal:
   if the first disjunct is false as stated, the second carries the programme. After `mg-39bf`
   the framing does **less** work than that, because leaning on the second disjunct means leaning
   on the branch whose constant is unnamed. The rescue is real but it is **not free**, and the
   row presents it as free.

**So: the sentence the ticket asked about is fine; the row it sits in is not.**

### 3.3 `code/chain_selection_9461/s1_chains.py:86`

Chain (I)'s open-statement label reads `"L2 (either disjunct) — Step 3 as written"`. Chain (I) is
the `C₃`-free chain (`ε_dem = ε_leak²/2`), so on the second disjunct that label asserts precisely
the unestablished half. It is `mg-9461`'s instrument and the ticket forbids re-opening `mg-9461`
(`mg-fd7c` repaired that document at `c20ad80`). **Flagged, not edited.**

---

## 4. The remedy is an artifact of the same kind as the defect

The defect repaired here is *a scope clause covering two cases with one phrase, true of one of
them*. This amendment adds thirteen scope clauses. Each was checked against **both** disjuncts
before landing. **Three failed that check on the first attempt:**

1. **§4 item 2** was first written as *"only the first disjunct kills `C₃`"* — **false on the
   lemma-count reading**, since both disjuncts do remove `C₃` as a **separate lemma**. Rewritten
   to name which reading it holds in.
2. **§9 row 8** was first written as a **withdrawal** of *"L3 is not an independent lemma"*. That
   claim **survives on both branches**; only the loss `= 1` is first-disjunct. Withdrawing it
   would have been an over-correction of the same shape in the opposite direction — and an
   over-correction is not the safe error here, because it would have re-opened a lemma count the
   programme has already banked.
3. **§6** was on the *"checked and left"* list, wrongly, because the first sweep searched for the
   **phrase**. Re-running it for the **claim** — bare `under L2` / `given L2` / `from L2 alone` —
   found it.

**The generalisable bit, sharpened by what happened here.** The ticket's own closing said a scope
clause covering two cases with one phrase is the cheapest place for this defect to hide, *because
the phrase is true of one case and nobody re-reads it against the other*. Two things this
amendment adds to that:

- **The phrase is not the defect; the claim is.** Grepping for *"either disjunct"* misses
  *"under L2"*, *"given L2"*, *"from L2 alone"* and *"both disjuncts"* — four spellings of one
  assertion, and three of the thirteen sites here had no matching phrase at all. `mg-fd7c` §7
  reported one `STATE.md` site, `:169`, and described it accurately; whether its grep also
  returned `:164` and the row was read as covered is not determinable from the artifacts, so it
  is not asserted here. What **is** determinable: `:164` carries the phrase, `mg-fd7c` did not
  name it, and the ticket then recorded a clean `STATE.md` for a ledger that was not clean.
- **A recorded clean check is an inherited claim, and inherits the same way.** The ticket wrote
  *"so nobody re-checks it"*. That sentence is the defect class applied to the audit trail rather
  than to the mathematics, and it cost one command to falsify.

---

## 5. Scope

- **No mathematics re-derived.** No script written, none re-run, no population re-enumerated.
- **No number moves** anywhere in the corpus. No claim is withdrawn. `§3`'s theorem, `§6`, `§7`
  and all `16/16` of `§7`'s independently reproduced figures stand exactly as they were.
- **L2 not attempted; `mg-9461` not re-opened; `mg-94c3`/`mg-01ea` not re-audited.**
- **`STATE.md` not edited** — two sites judged, both flagged to `pm-onethird` with proposed text.
- **`Op-Form` not edited.** `roadmap.md` does not exist in this tree and was not created.
- **One file changed** besides this record: `docs/OneThird-C3-PrefixCapture-mg-76b2.md`.
