# mg-fd7c — the verdict box and its table: `mg-39bf`'s three edits, applied

**Work item:** `mg-fd7c`. **Parent:** `mg-9461` (the chain-selection ruling, `cf1d7ef`).
**Finding repaired:** `mg-39bf` §10 — the three edits proposed by the independent audit of that
ruling (`f39ccce`), which **CONFIRMED the central claim**.
**Date:** 2026-08-09. **Files edited:** `docs/OneThird-ChainSelection-mg-9461.md` (the live
document) and one pointer paragraph in
`docs/OneThird-ChainSelection-mg-39bf-IndependentAudit.md` §10.
**`STATE.md` is NOT edited** — `mg-9461` §7 is still a proposal for `pm-onethird`, and it is the
proposed text that was repaired, not `STATE.md` (§6).
**No code written, no derivation re-run** — deliberately, and §5 says why.

---

## 0. WHAT WAS WRONG, IN TWO SENTENCES

1. **A verdict box contradicted a table in its own document.** §0 item 4 said *"There is no
   reading in which `0.20` is conservative"*, while §4.3's own third row printed `0.20` as
   **below** `17/78` in the restricted both-sides-non-chain scope. The table qualified itself
   inline; the box did not — **and the box is what gets quoted.**
2. **Two threshold slips.** The asymmetry *"chain (III) needs a lemma; the others need a lemma
   and a constant"* holds on **L2's first disjunct** and is unconditional as written; and
   *"chain (IV) does not close at all unless `c ≥ 40/49`"* names the **parity** threshold where
   the **closing** threshold is `4/5`.

**Nothing is withdrawn and the ruling does not move.** Step 6 consumes none of the four chains;
the constant is still `ε_spec ≤ 2×10⁻²` on chain (III) ≡ chain (I) at `C₃ = 1`; the entitlement
still favours chain (III). The corrections make three sentences one clause longer. They do
**not** collapse the entitlement back to the tie `mg-9461` §3 corrected *from* — `mg-39bf` §2.3
checked that explicitly and the check is carried into the document's claim ledger, row 16.

---

## 1. THE THREE EDITS, AND WHERE EACH LANDED

### Edit 1 — the asymmetry gains its disjunct

`mg-76b2` proves `C₃^(III) = 1` under **L2's first disjunct**: a monotone dominant standard
eigenvector means every set the Cheeger sweep visits is already a prefix, so restricting the
sweep to prefixes costs exactly `1`. Under **L2's second disjunct** the source asks only for

> *"…or at least yields a **low-conductance prefix**"* (`:560–562`)

under a preamble reading

> *"The programme becomes a proof if the following are established **with adequate constants**."*
> (`:553–554`)

and `mg-76b2` gives one sentence: *"the prefix is the output and there is no conversion to
charge for at all."* **That establishes there is no conversion step. It does not establish that
the delivered prefix meets `Φ ≤ √(2ε_spec)` rather than `K√(ε_spec)`.** A direct prefix theorem
at `Φ_pref ≤ K√(ε_spec)` gives `ε_dem = ε_leak²/K²`, i.e. an effective `C₃ = K²/2`. **The
constant is not eliminated on that branch — it is relocated** out of the conversion and into the
lemma's own unnamed *"low-conductance"*, which is the same shape of debt `mg-9461` §3 charges
Prefix-capture with.

The replacement sentence is `mg-39bf` §2.4's, used verbatim:

> **Chain (III) needs a lemma, and a constant only if that lemma is proved in its second
> disjunct. Chains (II) and (IV) need a lemma and a constant under every reading, and (IV)
> additionally needs its constant to clear a threshold it is measured below at every
> `n = 3..6`.**

**Landed at:** §0(i) (headline and body), §3's table (the `(I) ≡ (III)` row **split by disjunct**
rather than deleted, so both branches are visible) and the sentence beneath it, §7's proposed
`STATE.md` text (the *"consumes only L2"* qualifier `mg-39bf` §10 asks for).

**And the disjunct carrying the clean version is the one under strain.** `STATE.md` row 9
records L2's monotonicity clause as `FP✗` — *false as stated*, `2/126` at `n = 6` — which
`mg-9461` quotes twice, itself, to argue the conditioning is load-bearing. The same label
applied consistently is what puts weight on the branch where the asymmetry does not hold.
**Said fairly, as `mg-39bf` says it:** `FP✗` at `n ≤ 6` over primitive posets does **not** refute
L2 restricted to minimal counterexamples, which is the class L2 is about. It is a direction.

### Edit 2 — `40/49` is the parity threshold, not the closing threshold

Chain (IV)'s own bound gives `ε_dem = (ε_leak − (1−c))/c`. Two different questions, two
different numbers:

| question | threshold |
|---|---|
| does chain (IV) **close at all**? | `c > 1 − ε_leak = **4/5**` |
| does chain (IV) **deliver the budget the corpus publishes**? | `c ≥ **40/49** = 0.8163`, being `(1−ε_leak)/(1−ε_leak²/2)` |

At `c = 4/5 + 1/1000` — strictly **below** `40/49` — chain (IV) gives `ε_dem = 1/801 > 0`. **It
closes.** Worse than chain (III), but it closes. Replacement wording, from `mg-39bf` §10:
*"is strictly worse than chain (III) below `c = 40/49` and does not close at all below
`c = 4/5`."*

**This is a wording slip, not a derivation error, and `mg-9461` §5.3 already had it right** —
*"Below `c = 1−ε_leak = 4/5` the chain does not close at all"* — so §5.3 is the text copied
from. `STATE.md:169` already distinguishes the two (*"`c > 1 − ε_leak = 0.80` in prose /
`40/49 = 0.8163` self-consistently"*), and `mg-9461`'s own `PREDICTIONS.md` P7 lists both.

**It changes nothing about the ruling on chain (IV):** the measured `min c` is
`0.750, 0.618, 0.536, 0.453` at `n = 3..6`, **below `4/5` at every one**, so chain (IV) fails
under *both* readings.

**Landed at:** §0(i), §3's table row for (IV), claim-ledger row 8, and §11's re-scope question
for `mg-81ff` (which asks whether `min c` clears `40/49` on the small-gap stratum and then
concludes *"chain (IV) is dead"* — an inference that needs the `4/5` level, now said).
**Not touched:** §5.3 (already correct), §7's *"chain (IV)'s own `40/49` threshold"* (already
safe — `mg-39bf` §3 says so), §2.3 and §6, which use the same safe phrase.

### Edit 3 — the universal negative gains its scope, and `40 %` is labelled a floor

*"There is no reading in which `0.20` is conservative"* → *"There is no reading **in the
required scope** in which `0.20` is conservative."*

**The table was already right.** §4.3's third row prints the restricted-scope ceiling `17/78`
and says in the same line *"but this scope is not the one Step 6 must survive"*. What it did not
print is the **direction**, and the verdict box then summarised three rows as two. The row is
now labelled `conservative` with its exact excess (`7/85 = 8.235 %` below `0.20`), and a note
under the table says in as many words that without the scope qualifier the verdict box
**contradicts this table**.

`40 %` is **exactly right** — `0.20/(1/7) = 7/5`, excess `2/5` in exact rationals — so this half
is a completeness fix, not a correction. What was missing is what it is a floor *of*.
`mg-d3c7`'s refuting family is **proved**, so the required-scope ceiling is available in closed
form at every `n` with no sweep, and the `n ≤ 7` reading is the **mildest**:

| `n` | required-scope ceiling `≤` | `0.20` is above it by |
|---|---|---|
| `7` | `1/7` | **40 %** |
| `9` | `5/36` | **44 %** |
| `21` | `11/210` | 282 % |
| `101` | `51/5050` | 1 880 % |
| `401` | `201/80200` | 7 880 % |

**And this cuts *for* §4.4, not against it:** the movement needs no experiment, which is exactly
what *"only a proof moves it"* predicts.

**Landed at:** §0 item 4 (headline, body, and a struck-and-explained note recording what the box
used to say), §4.3 (direction column, the note, and the closed-form floor table), §5.2's
`ε_leak` status row, §7's proposed `STATE.md` text, claim-ledger row 11.

---

## 2. THE FOUR FURTHER SITES NO TICKET SENT ME TO

`mg-39bf` §10 names §0(i), §3's table, §0 item 4, §4.3 and §7. Sweeping the document for the
same two defects found four more, all of which would have re-introduced the contradiction the
repair exists to remove:

1. **§0(ii)** — *"`C₃^(III) = 1`, uniformly in `n`, **under either disjunct of L2**"*. This is
   the strongest single statement of the thing §0(i) has just been qualified for, sitting one
   item below it in the same box. Qualified to *"on L2's first disjunct"*, with the reason and
   with the observation that *"the only one of the four"* survives either way — the other three
   constants are **measured** under every reading — so what is conditional is the word
   **proven**, not the comparison.
2. **§5.2's `C₃^(III)` row** — *"PROVEN CONDITIONAL ON L2"*. Now names the disjunct.
3. **§5.2's `ε_leak` row** — *"errs **optimistic**"*, unqualified. Now carries the scope and the
   restricted-scope reading beside it.
4. **Claim-ledger rows 4, 8, 11 and 16** — the ledger is the document's machine-readable
   summary, so an unqualified row there is the verdict box's defect with a smaller font. All
   four repaired; row 16 additionally carries `mg-39bf` §2.3's finding that the asymmetry does
   **not** collapse back to the tie, so the repair cannot be read as a reversal.
5. **§11's re-scope question for `mg-81ff`** — uses the *safe* `40/49` phrasing, but then infers
   *"if it falls in the stratum too, chain (IV) is dead"*, and death is the `4/5` level. Both
   levels are now named.

**And four sites were checked and left alone because they are already correct:** §5.3 (the text
edit 2 copies *from*), §2.3, §6, and §7's *"chain (IV)'s own `40/49` threshold"* — which
`mg-39bf` §3 explicitly certifies as safe. Recorded so that "not repaired" and "not looked at"
stay distinguishable.

---

## 3. THE ERRATUM THAT CANNOT BE APPLIED — `cf1d7ef`'s COMMIT MESSAGE

`mg-9461`'s landing commit `cf1d7ef` carries both defects in a place no edit reaches:

> *"…and it **ERRS OPTIMISTIC IN EVERY READING WHERE A COMPARISON EXISTS**: 40% above the
> required scope's n<=7 ceiling 1/7, and above the uniform value 0 by everything…"*

> *"…and **chain (IV) does not close at all unless that number clears 40/49**."*

The first is the unqualified universal negative **with the `17/78` row dropped entirely** — so
unlike the verdict box, it does not even have the table beside it to correct the reader. The
second is the wrong threshold. Rewriting the commit is not available: it is an ancestor of
`main` and of every branch since.

**So it is recorded as wrong where the reader will be**, in the repair banner at the top of
`docs/OneThird-ChainSelection-mg-9461.md` — the document that commit points at. A commit subject
is a claim that can rot; the document is the thing that can be repaired, and the banner says
which sentences of the subject are superseded and by what.

---

## 4. WHY THIS IS THE THIRD OF THE SAME DEFECT TODAY, AND WHAT THE SHAPE IS

Three instances on this lineage in one day:

| | claim | scope it needed | how it surfaced |
|---|---|---|---|
| 1 | `ε₀ ≤ 17/78`, *"cannot be raised by more than 9 %, ever"* | **both** sides non-chain — not the architecturally required population, where the threshold is `0` | `mg-d3c7`'s audit; published unqualified as far as `docs/roadmap.md` and **struck at `7cd8ae7`**; document repaired by `mg-5214` at `cf4672e` |
| 2 | `mg-3969` §10's proposed `STATE.md` text, carrying the same figure | same | caught by `mg-5214` **before landing** — the proposal was repaired, not the ledger |
| 3 | *"There is no reading in which `0.20` is conservative"* | **required** scope — and the exception is the very `17/78` of rows 1–2 | `mg-39bf`'s audit; repaired here |

**The number is right every time. The qualifier is what is missing.** And instance 3 runs in the
**opposite direction** from instances 1 and 2 — there an unqualified claim was too *generous* to
the programme, here an unqualified claim is too *harsh* — which is the useful observation: the
defect is not optimism, it is a claim travelling without the population it was measured on.

**And the standing rule was followed rather than the shortcut:** `17/78` is **not** deleted from
§4.3. It keeps its number and gains its direction and its scope, per `mg-5214` — a number with a
scope is worth more than a number withdrawn.

---

## 5. NO INDEPENDENT AUDIT WAS PRE-FILED, DELIBERATELY

Per the 2026-08-07 tightening. This is a **stating-and-scoping repair** whose replacement wording
was supplied verbatim by a **landed** independent audit that had already re-derived the central
claim on a sensitive instrument (`code/chain_audit_39bf/`: md5-verified read with `st_size`
equal to bytes returned so no eviction or short read, every zero-count carrying a positive
control from the same read/regex/invocation, plus a mutation test injecting `Cheeger` and `C_3`
that catches both). **It is a chore, not a claim.** Pre-filing an audit for it is exactly the
drift that tightening was written to stop.

**What that means for what is in this document:** every number here is either quoted from a
landed document or is one line of exact-rational arithmetic over quoted inputs. The second kind
was recomputed in `Fraction`s before being written — `ε_dem(c) = (ε_leak − (1−c))/c` at
`c = 1, 9/10, 40/49, 4/5+1/1000, 4/5, 3/4` giving `1/5, 1/9, 1/50, 1/801, 0, −1/15`; the closing
threshold `1 − ε_leak = 4/5`; the parity threshold `(1−ε_leak)/(1−ε_leak²/2) = 40/49`;
`0.20/(1/7) = 7/5` excess `2/5`; `0.20/(5/36) = 36/25` excess `11/25 = 44 %`;
`(17/78 − 1/5)/(17/78) = 7/85 = 8.235 %`; and the family's `Δ₁ = (k+1)/((2k+1)k)` at
`k = 3, 4, 10, 50, 200`. All agree with `mg-39bf` §3 and §4 exactly. **That is reproduction of
arithmetic, not independent derivation, and it is not offered as more.**

---

## 6. WHAT I DID NOT DO

- **`STATE.md` NOT EDITED.** `mg-9461` §7 is a proposal; landing it is `pm-onethird`'s call. What
  was repaired is the **proposed text**, so that if it lands it lands with the qualifier rather
  than propagating the defect — which is instance 2's lesson exactly. `STATE.md` was grepped for
  the two contested sentences before starting and carries neither.
- **`docs/roadmap.md` NOT EDITED.** It is generated; the affected figures were already struck
  from it at `7cd8ae7`.
- **The ruling NOT softened.** Step 6 consumes no chain; the constant is `2×10⁻²`; chain (III) is
  the entitled route; chain (IV) fails on the measured `min c` under both thresholds. Nothing in
  §1–§2 above weakens any of that, and the count-is-a-tie correction `mg-9461` made of its own
  accord stands.
- **Nothing re-derived.** L2 not attempted, `C₃` not bounded, no poset enumerated, no script in
  `code/chain_selection_9461/` or `code/chain_audit_39bf/` run. `mg-39bf`'s audit is taken as
  landed, which is what it is.
- **No instrument file edited, and that was checked rather than assumed.**
  `code/chain_selection_9461/README.md:74` uses the *safe* *"chain (IV)'s own `40/49` threshold"*
  phrasing, and `code/chain_audit_39bf/README.md` carries neither claim.
  `code/chain_selection_9461/PREDICTIONS.md:76` contains *"no reading that rescues 0.20 as
  conservative"* — that file is a **pre-registered commitment** and is deliberately left exactly
  as written; it records what was bet, not what was found.
- **`mg-39bf`'s document not otherwise edited** beyond the one pointer paragraph at its §10
  recording that its proposal was applied.
- **No new figure published anywhere.** Every number in the repaired document was already in the
  corpus; the closed-form ceiling table at §4.3 is `mg-39bf` §4's, cited as such.

## 7. FLAGGED, NOT FIXED — TWO SITES OUTSIDE THIS TICKET CARRY EDIT 1's PHRASE

Grepping the corpus for the repaired phrases found the *"either disjunct"* formulation at two
sites that are **not** `mg-9461`'s and are **not** mine to edit:

- **`docs/OneThird-C3-PrefixCapture-mg-76b2.md:42` and `:557`** — *"`C₃ = 1`, uniformly in `n`,
  **under either disjunct of L2** — in chain (III)'s currency"*. This is the **origin** of the
  phrase; `mg-9461` inherited it. `mg-39bf` §2.2 read `mg-76b2`'s second-disjunct sentence at
  source and its finding is **not** that `mg-76b2` is wrong — it is that *"the prefix is the
  output and there is no conversion to charge for"* establishes there is no **conversion step**,
  which is a different statement from *"the delivered prefix meets `Φ ≤ √(2ε_spec)`"*. Whether
  `mg-76b2`'s own wording needs the same qualifier is a question about **that** document, which
  was audited by `mg-94c3` and repaired by `mg-01ea` at `ade980b`. Not opened here.
- **`STATE.md:169`** — the `C₃` ledger row, carrying *"under L2's second disjunct there is no
  `C₃` either, because the prefix is the output"* and *"`mg-76b2`'s 'either disjunct' framing is
  doing real work"*. `STATE.md` is `pm-onethird`'s and is out of scope for this ticket by its own
  terms.

**Flagged to `pm-onethird` by mail rather than edited.** Recorded here so the next reader does
not have to re-run the grep, and so that "the site was not found" and "the site was found and
left" stay distinguishable.
