# `mg-39bf` — INDEPENDENT AUDIT of `mg-9461`'s chain-selection ruling

## CONFIRMED ON THE CENTRAL CLAIM, AND THE REPLACEMENT IS RIGHT AT ITS CORE AND OVER-STATED AT ONE JOINT — chain (III) needs a lemma alone **only on L2's first disjunct**, which is the disjunct `mg-9461`'s own document records as `FP✗`-false as stated

---

## 0. Verdict

> **1. THE CENTRAL CLAIM REPRODUCES, ON AN INSTRUMENT I PROVED CAN FIND SOMETHING.**
> `md5 = db095fbe12ba19f0a8107f962c0d1c8f`, 603 lines, 16 560 bytes, `st_size` equal to
> bytes actually returned — **no eviction, no short read**. `C_3` occurs **0 times** in the
> whole file under five spellings; `Rayleigh`, `prefix capture`, `Cheeger`, `sqrt`, `std`
> occur **0 times in Steps 5–6**. Every one of those zeros carries a positive control from
> the **same read, same regex, same invocation**, and the counters are shown non-tautological
> by injecting `Cheeger` and `C_3` into a copy of the window and catching both (`a1`).
> **Step 6's whole hypothesis is `Δ₁ ≤ ε_leak` and no chain's constant is in it.** The
> ruling stands.
>
> **2. BUT THE `C_3` ZERO IS GENERIC, NOT SELECTIVE, AND THAT CHANGES WHAT IT PROVES.** The
> source names **no** `C_<i>` at all — `C_1` and `C_2` are also 0 — and `absolute constant`
> occurs 0 times (`a1 §B2`; the last figure independently reported by `mg-d3c7` at
> `6e5d88b`). So the zero is not *"the document names constants and omits this one"*. It is
> *"the document is written without explicit constants, and every chain's constant is
> equally absent."* That still supports the ruling — it is why Step 6 **cannot** tell which
> route delivered its hypothesis — but by a weaker argument than the parent's phrasing
> invites, and the weaker argument is the true one.
>
> **3. THE THING I WAS ASKED TO CHECK FIRST — THE REPLACEMENT — IS RIGHT AT ITS CORE.**
> *"Prefix-capture, proved in either form, delivers a constant fraction and no number"* is
> **TRUE AT SOURCE**, and I verified it in the conjecture's own words rather than through
> the parent: `:360–364` reads *"captures a **constant fraction**, or possibly `1−o(1)`, of
> the dominant standard eigenvalue"* — the free parameter is in the conjecture's own text.
> The gap-form repair `1−ρ_pref ≤ C₃(1−λ_std)` is `Op-Form §4.3`'s invention, not the
> source's, so proving the source's conjecture does not even deliver chain (II)'s relation.
>
> **4. AND IT IS OVER-STATED AT EXACTLY ONE JOINT, WHICH IS THE HALF NOBODY HAS CHECKED.**
> *"Chain (III) needs a lemma"* holds on **L2's first disjunct** — monotonicity — where
> `mg-76b2`'s theorem is actually **proved** and delivers `C₃^(III) = 1` with nothing left.
> On L2's **second** disjunct the source writes *"or at least yields a low-conductance
> prefix"* (`:560–562`), under a lemma-list preamble that reads *"established with
> **adequate constants**"* (`:553–554`). `mg-76b2`'s one-sentence treatment — *"the prefix
> is the output and there is no conversion to charge for at all"* — establishes correctly
> that there is no **conversion**; it does **not** establish that the delivered prefix meets
> `Φ ≤ √(2ε_spec)` rather than `K√(ε_spec)`. **The constant is not eliminated on that
> disjunct, it is relocated into the lemma's own unnamed `low-conductance`** — which is the
> same shape of debt, in the source's own vocabulary, that the parent charges Prefix-capture
> with. And the first disjunct is the one the parent itself records as `FP✗`-false as stated
> (`STATE.md` row 9). **So on the disjunct that survives, chain (III) needs a lemma AND a
> constant too.**
>
> **5. IT DOES *NOT* COLLAPSE BACK TO THE TIE IT CORRECTED FROM, AND I SAY SO BECAUSE THE
> TICKET ASKED WHETHER IT WOULD.** Chain (IV) needs its constant to clear a threshold under
> **every** reading; chain (II)'s `C₃^gap` is measured rising. The asymmetry survives
> unconditionally against (IV) and on the first disjunct against (II). **The repaired
> sentence is in §2.4 and it is one clause longer, not a different ruling.**
>
> **6. THE OTHER HALF OF THE `40/49` QUESTION: NO, CHAIN (IV) DOES NOT FAIL TO CLOSE UNLESS
> `c` CLEARS `40/49`.** It fails to close unless `c > 1−ε_leak = 4/5`. `40/49` is the
> **parity** threshold — the `c` at which (IV) delivers the same budget chain (III)
> publishes. Demonstrated rather than asserted (`a2 §E`): at `c = 4/5 + 1/1000`, strictly
> below `40/49`, chain (IV) gives `ε_dem = 1/801 > 0`. It closes, *worse* than (III), which
> is a different fact from not closing. **The parent's own §5.3 states this correctly and
> its own `PREDICTIONS.md` P7 lists `4/5` and `40/49` as two separate numbers** — so this is
> a wording slip, not a derivation error. It landed in §0(i) and §3's table, which are the
> two most-quoted places in the document. **The ruling is unaffected: the measured
> `min c = 0.750` at `n = 3` is below *both* thresholds.**
>
> **7. ONE SIGN-DIRECTION DEFECT, AND IT IS THE ONE THE TICKET SAID WOULD BE WORSE THAN
> NONE.** §0 item 4 asserts ***"There is no reading in which `0.20` is conservative."***
> That is **FALSE as stated, and contradicted by the parent's own §4.3 table**, whose third
> row — `17/78`, the **restricted** scope that skips cuts where either side is a chain —
> prints `0.20` as **below** it. The true sentence needs the scope qualifier: *no
> reading **in the required scope***. The commit subject makes the same claim — *"ERRS
> OPTIMISTIC IN EVERY READING WHERE A COMPARISON EXISTS"* — and drops the row entirely.
> **This is the same shape of defect struck on `main` this morning at `7cd8ae7`** — a claim
> travelling without its scope — running in the opposite direction. The table is right; the
> verdict box and the commit subject are not.
>
> **8. THE `40 %` IS EXACTLY RIGHT AND IS THE MILDEST READING AVAILABLE.** `0.20 / (1/7) =
> 7/5`, excess `2/5`, **40 % on the nose** in exact rationals. But it is the *floor* of a
> quantity with no ceiling: `mg-d3c7`'s **proved** family gives the required-scope ceiling in
> closed form at every `n` — `44 %` at `n = 9`, `282 %` at `n = 21`, `1 880 %` at `n = 101`
> (`a4 §A`). §4.3 leads with `40 %` and does not say it is a floor. **A reader quoting
> "40 % optimistic" as a bounded margin has the direction right and the magnitude
> unboundedly wrong.**
>
> **9. THE UNIVERSAL NEGATIVE SURVIVES — MY PRINCIPAL BET AGAINST IT LOST ON THE MERITS.**
> I named four candidate experiments in `PREDICTIONS.md` **before** reading §4.4, so the
> enumeration cannot have been fitted. All four are disposed of or off-target, and
> **candidate 3's disposal is sharper than the parent's own stated reason**: an experiment
> that refuted `0.20` would have to exhibit a poset where the transfer fails with disjunct
> (i) false — i.e. a poset with `δ(P) < 1/3` — so it cannot be run without already settling
> 1/3–2/3. The parent states that mechanism in §4.2 and does not carry it into §4.4, where
> it is what makes the negative *universal* rather than merely *unattempted*.
>
> **10. RIDER (a) IS A REAL FINDING AND *"NOT ALREADY IN THE CORPUS"* OVER-STATES IT.**
> `Op-Form`'s **own claim ledger** already records claim 17 (*"the chain is `n`-free end to
> end"*) as **CONDITIONAL on claim 16** (*"under either repair of prefix capture, L3's loss
> is a constant `C₃`"*), and `Op-Form`'s audit re-confirms it as conditional. What is
> genuinely new is **both** halves the parent actually needs: that `Op-Form` labels the
> condition as *interpretive* (*"conditional on the quoted sentence being the intended
> one"*) when it is **substantive**, and that it is discharged on **exactly one of the four
> chains**. The second is the operative part and it is new. The conditionality itself is not.
>
> **11. *"NOTHING HAD TO BE DISCARDED"* — CHECKED, NOT ACCEPTED, AND IT HOLDS.** The
> correction's live items were `17/78` and `mg-94c3`'s `10×`. In `3cd39f1` the sole `17/78`
> is an exact-rational example inside a `[FORMALITY]` arithmetic list; `mg-94c3` is not
> cited at all; and the `10×` is explicitly **not yet derived** — *"I have not done this
> arithmetic yet"*. The correction landed on work that had not been done. **And in the
> deliverable, all three SUBSTANTIVE occurrences of `17/78` name the restricted scope in
> the same line** (the other two are meta-references to the numeral itself), so the defect
> struck at `7cd8ae7` is **not** re-committed.
>
> **12. TWO OF §12's THREE TIME FIGURES ARE WRONG AND THE ONE THAT CARRIES THE INCENTIVE IS
> RIGHT.** From artefacts only (`a3`): dispatch `T+0`, correction **sent** `T+5.0`,
> predictions `3cd39f1` **authored** `T+6.0`, correction **read** `T+15.5`, deliverable
> `T+58.8`. So *"~40 minutes after dispatch"* matches **neither** reading, and *"`mg-d3c7`
> merged 22 minutes before I was dispatched"* is **10.0** minutes. **The ordering claim —
> that predictions were committed before the correction reached it — is TRUE**, by 9.5
> minutes, and that is the assertion a worker has a motive to shade. **The wrong figure has
> already made one hop: `mg-39bf`'s own ticket body repeats "~40 minutes in".**

---

## 1. The central claim, re-derived

### 1.1 The read, proved real before anything counted it

| check | expected | measured |
|---|---|---|
| path | `~/Library/…/spectral_near_ordinal_sum_program.tex` | resolved, `-rw-------`, not evicted |
| `st_size` vs bytes returned | equal | `16 560` = `16 560` |
| md5 | `db095fbe…` | `db095fbe12ba19f0a8107f962c0d1c8f` |
| lines (newline count, = `wc -l`) | `603` | `603` |

`mg-3969` hit the eviction case on this exact file and a prior audit on this lineage
shipped an instrument that agreed with the party under audit. `a1` therefore fails the run
on a short or empty read rather than reporting the zeros such a read would produce.

### 1.2 The counts, each with a live control

Step windows located by their own `\item` opener text, not by offsets: Step 1 `489–491`,
2 `492–498`, 3 `499–501`, 4 `502–508`, **5 `509–513`, 6 `514–515`**.

| token | Steps 5–6 | Steps 1–4 | whole file | status |
|---|---|---|---|---|
| `Rayleigh` | **0** | 0 | 3 | sensitive (3 in file) |
| `prefix capture` | **0** | 0 | 2 | sensitive (2 in file) |
| `Cheeger` | **0** | 1 | 9 | sensitive |
| `sqrt` (incl. `√`, `^{1/2}`) | **0** | 1 | 1 | sensitive |
| `std` (incl. `\std`, `standard`) | **0** | 2 | 40 | sensitive |
| `C_3` (5 spellings) | — | — | **0 file-wide** | see §1.3 |

**Mutation control.** `Cheeger` and `C_3` injected into a copy of the Steps 5–6 window:
both caught, `1` and `1`. The counters are not tautological.

**A defect in my own control, and it strengthened the parent.** The first form of the
positive control demanded the hit come from Steps 1–4 and **failed** on `Rayleigh` and
`prefix capture`. That was my control's defect. The failure is a finding in the parent's
favour: those two tokens are absent from **all six steps**, not merely from 5–6.

### 1.3 The `C_3` zero is generic — what it does and does not establish

`C_1` and `C_2` are also 0. No `C_<sub>` of any subscript occurs. `absolute constant` and
`universal constant` occur 0 times; `\varepsilon_{leak|spec|dem}` occurs 0 times. **The
source is written without explicit constants.**

This does not weaken the ruling; it relocates its force. The parent's ruling is that Step 6
**cannot tell** which route delivered `Δ₁ ≤ ε_leak`, and a document that names no constants
anywhere is a document in which no chain is identifiable at Step 6 — which is the claim.
What it forecloses is a *stronger* reading the phrasing invites, in which the source
deliberately declines to charge `C_3`. It does not decline; it never charges anything.

### 1.4 What Steps 5 and 6 actually say

```
509 | \item Interpret this as an \(L^1\) near ordinal sum:
511 | \E K_k\ll\min(k,n-k).
514 | \item Use near-ordinal-sum stability to transfer a balanced pair from
515 | \(P[A_k]\) or \(P[A_k^c]\) to \(P\), contradicting minimality.
```

**One reading the parent does not state, and it is not a defect — it is the sharpened
form.** `≪` is unquantified; `ε_leak` **is** its quantification. So Step 6 does not consume
a chain, and it also **sets the bar every chain must clear**. *"The chain question is not a
Step 6 question"* is right about **identification** and would be wrong about **selection**:
Step 6's threshold is exactly what grades the four routes. The parent's §2 says the
selection happens at Steps 3–4, which is where the *route* is chosen; the *pass mark* is
Step 6's. Both are true and the document only says the first.

---

## 2. The replacement asymmetry — the thing I was asked to check first

### 2.1 The half that is right, verified at source rather than through the parent

`:360–364`, the Prefix-capture conjecture, verbatim:

> *A threshold cut of the dominant standard eigenvector gives a prefix `A_k` whose Rayleigh
> quotient captures a **constant fraction**, or possibly `1−o(1)`, of the dominant standard
> eigenvalue.*

The free parameter is in the conjecture's own text. Proving it as stated hands over a
`c ∈ (0,1]` and no value. **The parent is right, and right for the reason it gives.**

Stronger than the parent says: the gap-form `1−ρ_pref ≤ C₃(1−λ_std)` is `Op-Form §4.3`'s
own repair, introduced there because *"as literally worded, prefix capture is too weak to
use"*. So proving the **source's** conjecture does not deliver chain (II)'s relation at
all — chain (II) needs a repair the source never wrote.

### 2.2 The half that is over-stated

The source, `:552–566`, in its own words:

> *The programme becomes a proof if the following are established **with adequate
> constants**.*
> *… **L2. Monotonicity/prefix lemma.** A dominant standard eigenvector is monotone in the
> distinguished order, **or at least yields a low-conductance prefix**.*
> *… **L3. Prefix Cheeger lemma.** The Cheeger sweep can be restricted to prefixes with
> **quantitatively controlled loss**.*

`C₃` **is** L3's loss. `mg-76b2`'s theorem proves `C₃^(III) = 1` under **L2's first
disjunct** — monotone `v` ⟹ every swept threshold set is already a prefix ⟹ the
restriction costs exactly 1. That proof is sound and I am not re-deriving it (forbidden,
and `mg-94c3` audited it).

Under L2's **second** disjunct `mg-76b2` gives one sentence: *"the prefix is the output and
there is no conversion to charge for at all."* **That establishes there is no conversion
step. It does not establish that the delivered prefix meets `Φ ≤ √(2ε_spec)`.** A direct
prefix theorem yielding `Φ_pref ≤ K√(ε_spec)` gives `ε_dem = ε_leak²/K²`, i.e. an effective
`C₃ = K²/2`. The constant has moved out of the conversion and into the lemma's own
*"low-conductance"* — which the source's own preamble says must be established *"with
adequate constants"*.

**And the disjunct that carries the clean version is the one under strain.** `STATE.md`
row 9 records L2's monotonicity clause as `FP✗` — *false as stated*, `2/126` at `n = 6` —
and the parent quotes that itself, twice.

> **Said fairly, because the parent is entitled to it:** `FP✗` at `n ≤ 6` over primitive
> posets does **not** refute L2 restricted to minimal counterexamples, which is the class
> L2 is about. It is a direction. But it is the parent's *own* label, used by the parent to
> argue the conditioning is load-bearing — and the same label, applied consistently, is
> what puts weight on the disjunct where the asymmetry does not hold.

### 2.3 Does it collapse back to the tie? No.

| | needs a lemma | needs a constant | needs that constant to clear a threshold |
|---|---|---|---|
| **(III), L2 first disjunct** | yes (L2) | **no** — `C₃ = 1` proven | no |
| **(III), L2 second disjunct** | yes (L2) | **YES** — the lemma's own unnamed loss | no |
| **(II)** | yes (Prefix-capture) | yes — `C₃^gap`, measured **rising** | no |
| **(IV)** | yes (Prefix-capture) | yes — `c`, unnamed in the conjecture | **YES** — see §3 |

The count is still a tie (one open statement each) and the parent is right to have struck
that. The asymmetry is still real. What is not right is its *unconditional* form.

### 2.4 The repaired sentence

> **Chain (III) needs a lemma, and a constant only if that lemma is proved in its second
> disjunct. Chains (II) and (IV) need a lemma and a constant under every reading, and (IV)
> additionally needs its constant to clear a threshold it is measured below at every
> `n = 3..6`.**

One clause longer. Same ruling. It is honest about the branch on which chain (III)'s
advantage is a proof and the branch on which it is a hope.

---

## 3. `40/49` — two thresholds, and the parent's verdict box has the wrong one

Chain (IV) re-derived from its own bound (`a2`, no line shared with the parent's `s1`):

`Φ_pref ≤ 1 − ρ_pref ≤ 1 − c·λ_std ≤ (1−c) + c·ε_spec ≤ ε_leak` ⟺
**`ε_spec ≤ (ε_leak − (1−c))/c`**

| `c` | `ε_dem` (unit: `ε_spec`) | |
|---|---|---|
| `1` | `1/5` | matches parent |
| `9/10` | `1/9` | matches parent |
| `40/49` | `1/50` | matches parent — **equal to chain (III)'s budget** |
| `4/5 + 1/1000` | `1/801` | **> 0. It closes.** |
| `4/5` | `0` | the closure threshold |
| `3/4` (measured `min c`, `n = 3`) | `−1/15` | does not close |

**Two different questions, two different numbers:**

- *Does chain (IV) close at all?* — needs `c > 1 − ε_leak = **4/5**`.
- *Does chain (IV) deliver the budget the corpus publishes?* — needs `c ≥ **40/49**`, which
  is `(1−ε_leak)/(1−ε_spec)` at `ε_spec = ε_leak²/2`.

`STATE.md:169` already distinguishes them (*"`c > 1 − ε_leak = 0.80` in prose /
`40/49 = 0.8163` self-consistently"*), and the parent's own `PREDICTIONS.md` P7 lists both.
**§5.3 gets it right.** §0(i) — *"does not even close unless that number clears `40/49`"* —
and §3's table — *"does not close at all unless `c ≥ 40/49`"* — do not.

**Why this matters and why it does not.** It does not change the ruling: the measured
`min c` is below `4/5` at every `n = 3..6`, so chain (IV) fails under either reading. It
matters because the wrong version sits in the verdict box, and §7's proposed `STATE.md`
text is one edit away from carrying it. §7 as written says *"chain (IV)'s own `40/49`
threshold"*, which is safe; §0's and §3's *"close at all"* is not.

---

## 4. The optimism table — direction checked row by row

| reading | ceiling | `0.20` against it | direction |
|---|---|---|---|
| uniform surrogate, **required** scope, uniform in `n` | `0` | above by everything | **optimistic** |
| uniform surrogate, **required** scope, `n ≤ 7` | `1/7` | **exactly 40 % above** (`7/5`, excess `2/5`) | **optimistic** |
| uniform surrogate, **restricted** scope (both sides non-chain), `n ≤ 7` | `17/78` | **8.235 % BELOW** | **conservative** |
| `ε₀^cons` | unmeasurable | no comparison | — |

Three rows, and the third runs the other way. The parent's **table** says so inline and
qualifies it correctly. The parent's **verdict box** says *"There is no reading in which
`0.20` is conservative"*, and the **commit subject** says *"ERRS OPTIMISTIC IN EVERY
READING WHERE A COMPARISON EXISTS"* and omits the row. Both are false without the scope
qualifier, and the scope qualifier is exactly what this corpus struck a claim for lacking
at `7cd8ae7` this morning.

**The `40 %` is a floor, not a margin.** `mg-d3c7`'s family is proved, so its members are
witnesses at every `n` and the required-scope ceiling is available in **closed form** with
no sweep:

| `n` | ceiling `≤` | `0.20` is above by |
|---|---|---|
| `7` | `1/7` (a different witness; the family's own `n=7` member is `4/21`, above `1/7`) | **40 %** |
| `9` | `5/36` | 44 % |
| `21` | `11/210` | 282 % |
| `101` | `51/5050` | 1 880 % |
| `401` | `201/80200` | 7 880 % |

§4.3 leads with the smallest of these.

**And this cuts *for* §4.4, not against it:** the movement needs no experiment. It is
already fixed by a proved family, which is precisely what *"only a proof moves it"*
predicts.

---

## 5. The universal negative — my principal bet against it, lost

Four candidates, named in `PREDICTIONS.md` before §4.4 was opened.

1. **Larger-`n` sweep for a smaller required-scope ceiling.** *Disposed* — §4 above: the
   movement is already in closed form from a proved family. No experiment adds to it.
2. **Numerical search for slack in the consuming inequality.** *Disposed* by the parent's
   own §4.2: on `ε₀^cons`, disjunct (i) is true at `ε = 1` for every exhibitable poset, so
   the inequality is vacuously satisfied everywhere it can be evaluated. There is no slack
   to find.
3. **Adversarial search for a worst family, to refute `0.20`.** *Disposed*, and this is the
   strongest disposal. Such a poset would have the transfer fail with (i) **false**, i.e.
   `δ(P) < 1/3` — refuting 1/3–2/3. **The experiment cannot be run without already settling
   the conjecture.** The parent states the mechanism in §4.2 and does not carry it into
   §4.4, where it is what makes the negative *universal* rather than *unattempted*.
4. **Witness search for `c`.** *Not disposed — and not a counterexample.* It targets chain
   (IV), and the parent proposes exactly this experiment in §11. It moves **which lemma**
   the constant rests on, not the constant.

**P5 LOST.** The sentence is sound. It should carry one qualification: it is about `0.20`'s
**value**, and §4 above shows a figure published beside it is not fixed.

---

## 6. Rider (a) — real, and narrower than claimed

`Op-Form §4.3` reads, verbatim:

> *Under **either** repair the loss is a constant `C_3`, giving `ε_spec ≤ ε_leak²/(2C_3)`.
> … **So there is no reading of the source under which `n` enters at L3.** **[CONDITIONAL
> on the quoted sentence being the intended one]***

And `Op-Form`'s own claim ledger:

| # | claim | § | status |
|---|---|---|---|
| 16 | Under either repair of prefix capture, L3's loss is a constant `C_3`; no reading injects an `n` | 4.3 | **CONDITIONAL** on `:360–364` being the intended statement |
| 17 | L3 is the last candidate site for `n`-dependence; the chain is `n`-free end to end | 4.3 | **CONDITIONAL on 1, 4, 13, 16** |

**Already in the corpus:** that 17 is conditional on 16, i.e. on `C₃` being a constant.
Twice — in `Op-Form`'s ledger and in its audit, which re-confirms it *as conditional*.

**Genuinely new, and it is the operative part:**

1. `Op-Form` labels the condition as **interpretive** — *"conditional on the quoted sentence
   being the intended one"*. It is **substantive**: even granting the sentence is intended,
   *"under either repair the loss is a constant"* is an assumption about what the repair
   delivers, not a theorem. The parent's re-labelling is correct and is not in the corpus.
2. The condition is **discharged on exactly one of the four chains** — `C₃^(III)` proven
   flat, `C₃^gap` and `min c` measured moving. `Op-Form` pre-dates those measurements and
   could not have drawn it.

So §0(iii)'s *"the part that is not already in the corpus"* over-states by including the
conditionality. Both new halves survive; the claim should be made on them rather than on
the conditional's existence.

---

## 7. *"Nothing had to be discarded"* — checked

The correction (`~/.macguffin/mail/q9461/cur/…`, `Date: 2026-08-09T18:11:55Z`) carried three
live items. Against `3cd39f1`, the predictions commit:

| correction item | in `3cd39f1`? | verdict |
|---|---|---|
| do not use `17/78` as a ceiling | once, at line 98, inside a `[FORMALITY]` list of exact-rational arithmetic examples | **not load-bearing** — no prediction's truth value changes |
| do not act on `mg-3969` §7's `(0, 17/78]` release advice | `mg-845e` occurs **0 times** | **nothing to discard** |
| cite `mg-94c3`'s `10×`, do not re-derive it | `mg-94c3` occurs **0 times**; the `10×` appears with *"I have not done this arithmetic yet"* | **the correction pre-empted work not yet done** |

**The claim holds.** My guard was that *"appears in the text"* is not *"was discarded"*, and
on that guard nothing was discarded. In the deliverable `17/78` occurs five times: three
substantive uses, each naming the restricted scope in the same line, and two
meta-references to the numeral (§0's *"not used as a live ceiling"* and §12's own account).

---

## 8. The timeline, from artefacts only

Committer dates are rebase artefacts. Author dates, mail headers and directory ctimes:

| `T+` | UTC | event | evidence |
|---|---|---|---|
| `−10.0` | `17:56:53` | `mg-d3c7` lands on `main` | git author date, `6e5d88b` |
| `0.0` | `18:06:55` | dispatch | the correction mail's own *"dispatched ~5 minutes ago"* |
| `+0.2` | `18:07:08` | `q9461` mailbox created | dir ctime |
| `+5.0` | `18:11:55` | correction **sent** | mail `Date:` |
| `+6.0` | `18:12:52` | `PREDICTIONS.md` committed | git **author** date, `3cd39f1` |
| `+15.5` | `18:22:24` | correction **read** | `cur/` dir ctime (the `new`→`cur` move) |
| `+51.2` | `18:58:08` | instrument committed | git author date |
| `+58.8` | `19:05:40` | deliverable committed | git author date |

- *"~40 minutes after dispatch"* (§12, and the commit subject): matches **neither** sent
  (`5.0`) nor read (`15.5`). **Wrong.**
- *"`mg-d3c7` … merged 22 minutes before I was dispatched"* (§12): **10.0** minutes. Wrong.
- *"after I had read the sources and committed predictions"* (§12): **TRUE**, by 9.5
  minutes. This is the assertion with an incentive attached and it is the one that holds.
- My own ticket's *"the correction landed after it [`3cd39f1`]"*: false on the **sent**
  reading by 57 seconds, true on the **read** reading, which is the only one a worker can
  act on.

> **A defect of my own, caught by this script's assertion.** I first used the mail **file's**
> mtime as the read time. `mv` preserves mtime, so it dates the **delivery** — wrong by 10.5
> minutes, and it made me briefly score the ordering claim FALSE. The `cur/` **directory**
> ctime is what records the move.

---

## 9. Scored predictions

| | bet | outcome |
|---|---|---|
| P1 | md5 + 603 verify | **HELD** (near-formality — `mg-d3c7` had published both) |
| P2 | zero-counts reproduce | **HELD**, and on a control that failed once before it passed |
| **P3** | **the replacement asymmetry is not clean** (0.45) | **PARTIALLY HELD** — over-stated at the joint I named, for the mechanism I named (III's open statement is quantitative on the surviving disjunct); **but I bet it would collapse toward the tie and it does not** |
| P4 | a direction defect in the optimism table (0.30) | **HELD**, though not where I expected — the defect is in the verdict box and commit subject, not in a table row; the rows are right |
| P5 | the universal negative is over-claimed (0.55) | **LOST** on the merits — all four pre-registered candidates disposed of |
| P6 | something was invalidated by the correction (0.40) | **LOST** — the guard I filed is what stopped me scoring line 98 as a discard |
| P7 | rider (a) already in the corpus (0.30) | **HALF HELD** — the conditionality is; the per-chain discharge is not |
| P8 | my own ticket's timeline is wrong (0.35) | **HELD** — and so is the parent's, which is where the ticket got it |

Two of my own defects, both caught by controls before publication: `a1`'s positive control
(mis-specified, and its failure strengthened the parent) and `a3`'s read timestamp (wrong by
10.5 minutes, and it briefly reversed a verdict).

---

## 10. Proposal for `pm-onethird` — three edits, stated as a proposal

1. **§0(i) and §3's table**: replace *"needs a lemma"* with §2.4's sentence, and replace
   *"does not close at all unless `c ≥ 40/49`"* with *"is strictly worse than chain (III)
   below `c = 40/49` and does not close at all below `c = 4/5`"*. §5.3 already says this and
   is the text to copy from.
2. **§0 item 4**: *"There is no reading in which `0.20` is conservative"* → *"…in the
   required scope"*. §4.3's table is already correct and is what the verdict should
   summarise.
3. **§4.3**: mark `40 %` as the `n ≤ 7` reading and the mildest available, with `44 %` at
   `n = 9` beside it. The number is right; what it is a floor *of* is missing.

§7's proposed `STATE.md` text needs only edit 1's qualifier on *"consumes only L2"*. Its
`40/49` wording (*"chain (IV)'s own `40/49` threshold"*) is already safe.

---

## 11. What I did NOT do

- **Did not run any script in `code/chain_selection_9461/`.** By design (E6) — the ticket
  forbids treating the parent's own route as confirmation.
- **Did not re-derive `C₃ = 1`, did not re-attack `ε₀`, did not attempt L2, did not bound
  `C₃`.** All forbidden. Where §2.2 discusses L2's disjuncts it reads `mg-76b2`'s stated
  hypothesis and the source's own wording; it does not re-prove anything.
- **Did not re-run `mg-3969`'s 604 230-cut sweep or `mg-d3c7`'s `n ≤ 7` exhaustive sweep,
  and did not re-verify `mg-d3c7`'s family numerically.** §4 re-evaluates its **closed
  form** only, citing the family as landed.
- **Did not re-measure `mg-76b2` §7's four columns** (`C₃^gap`, `C₃^cut`, `min c`). Read and
  cited, `FP` at `n ≤ 6`, on a population outside the regime.
- **Enumerated no posets at all.** There is no sweep in `code/chain_audit_39bf/`.
- **Did not verify `Op-Form`'s own citations back to the `.tex` beyond `:360–364`,
  `:318–324` and `:552–570`,** which I read directly.
- **Edited neither `STATE.md` nor `mg-9461`'s document.** §10 is a proposal.
