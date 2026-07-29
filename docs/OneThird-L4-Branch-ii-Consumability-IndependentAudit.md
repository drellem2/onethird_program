# Independent adversarial audit — `OneThird-L4-Branch-ii-Consumability.md` (mg-63e3, commit `a3164dd`)

**Auditor work item:** mg-f825 · **Target:** `docs/OneThird-L4-Branch-ii-Consumability.md`, added by `a3164dd`
on `origin/main`, repo `onethird_program` (target path derived from the parent's merge commit per
STATE.md Appendix A; that commit adds exactly one file and it is this one).
**Method:** paper-and-pencil, **zero computation**. Every rational below was re-derived from the poset
definitions on ≤ 8 elements; nothing was run, and no script or dataset is committed with this audit.
**Independence:** I did not author the target. Every `.tex` line range it cites was pulled and read
directly, not accepted from the quotation.

---

## 0. Verdict

**OVERSTATED.**

> **The hand witness is entirely CONFIRMED.** I rebuilt family **W** from scratch — poset axioms, the
> slot bijection, all thirteen exact rationals, the `n = 8` instance element-by-element, the second
> (both-chains) family, and the `d_TV` figures. **Every number in the document is right.** `Δ₁ = 1/n` at
> `t = 2`, `p^{P[A]}_{xy} = 1/2`, `p^P_{xy} = 1/4`, `{x,y}` the sides' only incomparable pair,
> `p^P_{x,b_1} = 1/2`, `δ(W) = 1/2`. The witness does what it claims. There is no arithmetic defect.
>
> **The headline over-reaches at exactly one quantifier, and it is the load-bearing one.**
> Cor. 4.3 / ledger claim 13 — *"there is no modulus `F` for which (T) is true"* — is **BROKEN as a
> universal**. Family **W** lives entirely inside the regime `Δ₁·n = 2t/(t+2) < 2`, and a witness only
> enters branch (ii) if `|S| ≤ F(ε)n`. So the family constrains `F` **only** along its own sequence
> `ε_a`, and it provably **cannot** refute any modulus with `F(ε) ≤ ε/2` (§3.1, one line). `F(ε) = ε/4`
> is an ordinary modulus — it tends to `0`, and `F(ε)n → ∞` for every fixed `ε > 0`, so branch (ii) is
> not thereby degenerate — and **W** says nothing against it. What the document proved is
> *"transport fails for every modulus of order `ε` or larger"*, which is a real and useful theorem. What
> it wrote is *"there is no modulus"*.
>
> **The document's own §4 contains the refutation of its own corollary.** It derives the tolerance
> `F(ε)n ≤ 1` and then infers *"not a modulus in `ε` at all"*. But in **W** the pair `(ε, n)` is locked —
> at `t = 2`, `ε = 1/n` **identically** — so `F(ε) = ε` satisfies `F(ε)n ≤ 1` exactly. The inference to
> `n`-dependence silently re-reads the constraint as holding at *fixed* `ε` for *all* `n`, and the family
> never supplies such a pair. **This is the Appendix A step-4b falsifier-quantifier defect verbatim**,
> and its stakes are unusually high: STATE row `:132` records that if L4 needs an `n`-dependent modulus,
> **the mg-88bd answer flips**. The proposed row would land that flip on a quantifier error.
>
> **The candidate repair (IB) is FALSE as stated**, refuted by a 3-element poset (modulus-free) and again
> at `n = 8` with genuine leakage `Δ₁ = 1/20` and one genuine modification (§5). The defect is the
> **interface** clause, not the lemma's substance: the half that actually consumes branch (ii) —
> *"`P` has a `1/3`-balanced pair"* — survives all my attacks. The fix is free, and precisely because it
> is free it must be made before the row lands. §7's fifth property is the best paragraph in the
> document and it is unaffected.
>
> **The document also UNDERSTATES its own strongest result**, and that result is missing from the
> ledger (§6). **Branch (iii) as a standalone universal is refuted at every `ε > 0`, for every modulus**
> — (iii) has no budget clause, so the quantifier problem above does not touch it. That refutation is
> modulus-free, decisive, and it upgrades §9's tentative "flag" into a theorem: **no `ε`-calibration of
> the repaired branch-(iii) predicate exists**, so whatever mg-3ce3's `0 RED / 6681 up to ε = 0.20`
> measured, it is not the threshold of a true statement.

**Scope check: CLEARED, and the document deserves credit here.** It does **not** strawman. I pulled
`:464–474`, `:513–515`, `:527`, `:476–479`, `:567–569` myself; the quotations are verbatim-accurate and
the object attacked is the architecture's actual wording. It also does **not** commit the
"this route fails ⟹ no route works" conflation the brief warned about — §1's C1/C2/C3 table and ledger
claim 27 decline C3 explicitly and correctly. **But it commits the same shape of error one level down,
at the modulus quantifier.** It guarded the conflation it was briefed on and walked into its twin.

**Net (honest).** A correct, well-built, genuinely informative witness; a correct conditional theorem
about the ordinal-sum route; one false universal in the headline and the proposed row; one false
proposed lemma with a free fix; and one strong modulus-free result the document owns but does not
claim. The RED on Step 6 **survives**, at strength *"for any modulus `F(ε) = Ω(ε)`"* — which is almost
certainly the operative case, but *almost certainly* is not what a `PROVEN` row says.

---

## 1. Re-derivation of the witness — every rational, independently

Per brief item 2: recomputed, not read. Family **W**: `a ≥ 3`, `1 ≤ t ≤ a−1`, `n = 2a`;
`A = {c_1 < ⋯ < c_{a−2}} ∪ {x,y}` with all `c_j < x`, all `c_j < y`, `x ∥ y`; `B = C_a`; all `A < B`
except `x < b_1, …, x < b_t` deleted.

**Poset axioms.** Transitivity survives the deletions: the only elements below `x` are the `c_j`, and
`c_j < b_i` is retained directly, so no deleted relation is forced back by a chain through `x`. Nothing
lies strictly between `x` and any `b_i` (`i ≤ t`). ✔ **CONFIRMED.**

**Down-set.** `A` is a down-set (below `c_j`: `c_i, i<j`; below `x`, `y`: only `c`'s), so `(A,B)` is a
legitimate prefix cut and `Δ₁` is defined with `min(|A|,|B|) = a ≠ 0`. ✔

**Slot bijection (Lemma 4.1).** The `2a−1` non-`x` elements form the chain
`c_1 < ⋯ < c_{a−2} < y < b_1 < ⋯ < b_a` — checked link by link. `x` is above exactly `c_1..c_{a−2}`,
below exactly `b_{t+1}..b_a`. The open gap contains `y, b_1, …, b_t`, i.e. `t+1` elements, hence
**`t+2` insertion slots**, uniform. ✔ **CONFIRMED.**

| quantity | document | my derivation | |
|---|---|---|---|
| `#LE(P)` | `t+2` | `t+1` elements in the gap ⟹ `t+2` slots | ✔ |
| `p^P_{xy}` | `1/(t+2)` | `x ≺ y` in slot 0 only | ✔ |
| `p^{P[A]}_{xy}` | `1/2` | `P[A] = C_{a−2} ⊕ AC_2`, exactly 2 LEs | ✔ |
| `E\|A ∖ σ(A)\|` | `t/(t+2)` | `x` at position `a+j−1` in slot `j`; escapes iff `j ≥ 2` ⟹ `t` slots | ✔ |
| `Δ₁(A,B)` | `t/((t+2)a)` | divide by `min(a,a) = a` | ✔ |
| sides' incomparable pairs | `{x,y}` only | every `c_j` comparable to all of `A`; `P[B]` a chain | ✔ |
| `t = 0` | `p^P = 1/2` | 2 slots | ✔ |
| `t = 1` | `p^P = 1/3` exactly | 3 slots | ✔ |
| `t = 2` | `Δ₁ = 1/(2a) = 1/n`, `p^P = 1/4` | 4 slots, `E = 2/4` | ✔ |
| `p^P_{x,b_i}` | `(i+1)/(t+2)` | `x ≺ b_i` in slots `0..i` | ✔ |
| `t=2`: `p^P_{x,b_1}` | `1/2` | slots 0,1 of 4 | ✔ |
| `δ(W)` at `t=2` | `1/2` | pairs at `1/4, 1/2, 3/4` ⟹ `max min = 1/2` | ✔ |
| amplification `t=⌈√n⌉` | `Δ₁ < 2/n`, `p = Θ(n^{−1/2})` | `t/(t+2) < 1`; `p = 1/(t+2)` | ✔ |
| `d_TV(σ_P, σ_{P'})` at `t=2` | `1/2` | `½(2·\|½−¼\| + 2·¼) = ½` | ✔ |
| `d_TV` general | `→ 1` | `= t/(t+2)` | ✔ |

**The `n = 8` instance (§9), checked element by element.** `a = 4, t = 2`:
`A = {c_1<c_2<x, y}`, `B = {b_1<b_2<b_3<b_4}`, `x ∥ b_1, b_2`. The four listed linear extensions are
exactly the four slots for `x` (before `y`; between `y` and `b_1`; between `b_1` and `b_2`; between
`b_2` and `b_3`), and `x ≺ b_3` is forced. `p^P_{xy} = 1/4`; first-4 prefixes are
`{c_1,c_2,x,y}, {c_1,c_2,y,x}, {c_1,c_2,y,b_1}, {c_1,c_2,y,b_1}` so `E|A∖σ(A)| = 2/4 = 1/2` and
`Δ₁ = (1/2)/4 = 1/8`. ✔ **CONFIRMED, all of it.**

**Second family (§7), independently.** `P = C_a ⊕ C_a` minus `c_a < b_1, …, c_a < b_t`. Non-`c_a`
elements form the chain `c_1 < ⋯ < c_{a−1} < b_1 < ⋯ < b_a`; the gap contains `b_1..b_t`, so **`t+1`
slots**; `c_a ≺ b_i` in slots `0..i−1`, giving `p^P_{c_a,b_i} = i/(t+1)`; `c_a` escapes the first `a`
positions in slots `1..t`, so `Δ₁ = t/((t+1)a)`. At `t = 2`: `1/3` and `2/3`, both balanced, branch (i)
holds. ✔ **CONFIRMED.** Both sides are chains, so R4 fails and minimality yields nothing — the chain
escape is real and the source does flag it unhandled at `:477–478`.

**Verdict on the witness: nothing to break.** Ledger claims 1–12, 15, 18, 20–22 are CONFIRMED as stated.

---

## 2. Scope check — the source, pulled directly (brief press-point 4)

I read the `.tex` rather than the document's characterisation of it.

- **`:464–474`** is the L4 conjecture, and branch (ii) reads exactly: *"after removing or modifying at
  most `F(ε)n` **interface elements**, `P` becomes `P[A] ⊕ P[B]`."* ✔ quoted correctly.
- **`:514–515`** is Step 6: *"Use near-ordinal-sum stability to transfer a balanced pair from `P[A_k]`
  or `P[A_k^c]` to `P`, contradicting minimality."* ✔ verbatim. (`:513` is blank; the document's
  `:513–515` overshoots by one line. Harmless.)
- **`:527`** reads exactly `⟹ text{balanced pair by minimality}`. ✔
- **`:476–479`**: *"Since `P[A]` and `P[B]` are smaller than a minimal counterexample, minimality should
  provide a balanced pair on one side unless that side is a chain. The task is to show that the thin
  interface cannot destroy all such pairs."* ✔
- **`:567–569`** (L4 in the open-lemma list): *"Sufficiently small prefix leakage contradicts minimality
  by preserving a balanced pair from one side."* ✔

**No strawman.** The refutation targets what the architecture says. Two calibrations, neither fatal:

1. **Step 6's licence is L4, not minimality.** The document's §0 says the mechanism is *"transfer a
   balanced pair … justified by minimality"*. The source's division of labour is: minimality supplies
   the *side* pair (`:476–477`), near-ordinal-sum stability supplies the *transfer* (`:514`), and
   minimality is contradicted at the end. The substance of the document's reading is right; the phrasing
   muddles which ingredient does what. Cosmetic.
2. **`:478–479` already concedes the missing step.** The source itself calls transport *"the task"* —
   it is stated as open, not as delivered. So *"the box at `:527` is **wrong** on branch (ii)"* is
   sharper than the source earns. The exact statement is: **the box at `:527` is justified only on
   branches (i) and (iii); on (ii) the source's own `:478–479` identifies the gap, and this document
   shows the gap cannot be closed by transport at any modulus `F(ε) = Ω(ε)`.** That is still a genuine
   strengthening — open → impossible-by-this-mechanism — and it should be phrased that way.

**The "this route fails vs no route works" test: PASSED.** §1's C1/C2/C3 table is the correct
instrument, claim 27 declines C3 explicitly, and §0's AMBER is consistent with it. This is the
best-executed part of the document and I could not break it.

**One counter-attack I ran and it fails — recording it because it is the obvious one.** *Objection:* the
architecture only needs transport for a **minimal counterexample** (frozen, `δ < 1/3`), and `δ(W) = 1/2`,
so **W** is out of scope. *Rebuttal:* Step 6 cites near-ordinal-sum stability as a **general lemma**;
a general lemma with a counterexample cannot be cited. And restricting the lemma's hypothesis to frozen
`P` does not rescue it — a frozen `P` has no balanced pair anywhere by definition, so "transport into a
frozen `P`" is false unless the class *"minimal counterexample ∧ branch (ii)"* is empty, which just
renames the problem. **The document is right and its §7 property 5 says exactly this.** The objection
does not land. *(It does land against §9 — see §7 below.)*

---

## 3. F1 — **BROKEN**: "shrinking `ε` does not help, so no modulus exists" is a false universal

This is press-point 2 of the dispatch, and it is where the document breaks.

### 3.1 The one-line lemma the document needed and did not run

Branch (ii) is not a free hypothesis: a poset is in branch (ii) **only if** `|S| ≤ F(ε)n`. So a witness
refutes (T) *for a given `F`* only if it is admitted by that `F`'s budget.

> **Lemma (mine).** In family **W**, `Δ₁ · n = t/((t+2)a) · 2a = 2t/(t+2) < 2` for **every** `a` and
> **every** `t`. Hence for any modulus with `F(ε) ≤ ε/2`, the budget at the witness's own leakage is
> `F(ε)n ≤ εn/2 < 1`, so **no member of family W is admitted into branch (ii) at all** — and the family
> refutes nothing about that `F`. ∎

That is the whole objection, and it is hand-checkable in one line. Working the threshold out exactly:

- **Counting relations** (`|S| = t`, the document's primary count): admission needs
  `t ≤ F(ε)·2a`, i.e. `F(ε) ≥ ε(t+2)/2`, minimised at `t = 2` ⟹ **`F(ε) ≥ 2ε`**.
- **Counting elements** (`|S| = 1` — only `x`'s relations change, for every `t`): admission needs
  `F(ε) ≥ ε(t+2)/(2t)`, which decreases in `t` to **`ε/2`** and never below it.

**Either way there is a strictly positive threshold constant, and every modulus below it is untouched.**
`F(ε) = ε/4` is untouched. `F(ε) = ε/4` is not a degenerate choice: it tends to `0` as required, and for
each fixed `ε > 0` its budget `F(ε)n → ∞`, so branch (ii) remains a substantive alternative everywhere
except in the `εn = O(1)` corner — which is precisely and only where **W** lives.

### 3.2 The document refutes its own corollary, in its own §4

> *"This requires `F(ε)·n ≤ 1`, i.e. `F(ε) ≤ 1/n` — **not a modulus in `ε` at all**."* (§4)

In **W** at `t = 2`, `ε = Δ₁ = 1/n` **identically** — `ε` and `n` are not independent, there is one
`(ε,n)` pair per `a`. So `F(ε) = ε` satisfies `F(ε)n = 1 ≤ 1` exactly, and it is a function of `ε`
alone. The step from *"`F(ε)n ≤ 1` at the witness's parameters"* to *"`F` must depend on `n`"* requires
a witness at **fixed `ε` and growing `n`**, and by the Lemma of §3.1 family **W** contains none: it is
confined to `εn < 2`. **The inference is invalid, and it is invalid in the same way as the mg-dbd1 §3.2
defect Appendix A step 4b was written to catch — a constraint established at one distinguished
parameter pair, generalised over a quantifier the witness never ranged across.**

### 3.3 What is true, and it is worth having

The document's *hypothesis*-side claim is correct and I confirm it: **shrinking `ε` does not evade the
family**, because **W** exists at every `ε` of the form `1/n`. Steps 2–5 cannot escape by producing a
smaller `ε`. That is real. What does not follow is anything about `F`. The two are different objects —
`ε` is the hypothesis Steps 2–5 deliver, `F` is L4's own budget — and Cor. 4.3 merges them in its last
sentence.

**Correct replacement, and it is a better result than the false one, because it is a dichotomy rather
than a kill:**

> **Either** L4's modulus satisfies `F(ε) = Ω(ε)`, in which case family **W** shows Step 6's stated
> transfer cannot consume branch (ii), at any `ε`, and no improvement to Steps 2–5 repairs it;
> **or** L4 holds only with `F(ε) = o(ε)`, in which case branch (ii) is unavailable exactly in the
> minimal-leakage regime `εn = O(1)` — and **L4 is thereby a strictly stronger conjecture than the
> source's wording suggests**, since shrinking `F` strengthens (ii) *and* (iii) simultaneously.
> **The route is not refuted; it is priced.** The second horn is a real cost and it has never been
> recorded anywhere in the corpus.

### 3.4 Why this one matters more than a normal over-claim

STATE `:132` records, as the load-bearing condition on the mg-88bd result: *"if L4 needs an
`n`-dependent modulus the answer flips."* The proposed row (§10) asserts flatly that transport needs
`F(ε)n ≤ 1`, *"an **`n`-dependent condition**, vindicating the shape of mg-88bd §3.3's own dismissed
steelman and tightening it from `O(1)` to `≤ 1`"*. **Pasted as written, that flips a canonical row on
the strength of §3.2's invalid inference.** mg-e35c F1 flagged §3.3's dismissal as a false universal;
the correct response is not to install the opposite universal.

### 3.5 Ledger self-contradiction — the document already knows

| row | text | label |
|---|---|---|
| 13 | *"Shrinking `ε` does not repair it; **there is no modulus `F`**"* | **PROVEN** |
| 16 | tolerance is `t ≤ 1`, *"requires `F(ε)n ≤ 1`"* | **PROVEN for family `W`** · *"**Conditional as a general claim** — it is a lower bound on the demand, **from one family**"* |

Row 16 is the honest statement of row 13's content, and the two carry different labels. **Row 16 is
right and row 13 is wrong.** Row 13's stated basis is also F2's false premise (§4). Row 17 inherits
from 16 and is labelled *"PROVEN given 16"* — honest in the ledger, and then stated flat in §10.

### 3.6 One more unit problem, which the document waves off

§4 says the modification count is *"`t` relations, touching `t+1` elements — **either count is
`t + O(1)`**"*. But branch (ii) counts **elements** (`:469–470`, verified), and under element-counting
`|S| = 1` for every `t`, since `x` is the only element whose relations change. `t + O(1)` and `1` are
not the same function of `t`. This is dismissed as `O(1)` in a document whose central quantitative
claim is the difference between a budget of **1** and a budget of **2**. It changes the §3.1 threshold
from `2ε` to `ε/2` — a factor of 4 in the one constant the argument is about.

---

## 4. F2 — **BROKEN premise**: `1/n` is not the smallest nonzero prefix leakage

Cor. 4.3's stated basis: *"leakage `1/n`, which is (up to constants) **the smallest nonzero leakage a
prefix cut can have**."* Also ledger row 13's entire "Basis" cell.

**This is false, by a factor of `n`.** Since `Δ₁ = E|A∖σ(A)|/min(|A|,|B|)` and `E|A∖σ(A)|` is a
multiple of `1/#LE(P)`, nothing bounds `Δ₁` below by `c/n`. **Hand counterexample, `n = 8`:**

> `c_1 < c_2 < c_3` a chain; `x` incomparable to every `c_j` **and** to `b_1`, with `x < b_2, b_3, b_4`;
> `b_1 < b_2 < b_3 < b_4` a chain; every `c_j < ` every `b_i`.
> `A = {c_1,c_2,c_3,x}` (a down-set), `B = {b_1,…,b_4}`.

The non-`x` elements are totally ordered, and `x` may be inserted before `c_1`, between consecutive
`c`'s, after `c_3`, or after `b_1` — **5 linear extensions**, uniform. `x` leaves the first 4 positions
in the last slot only, so `E|A∖σ(A)| = 1/5` and

> **`Δ₁ = (1/5)/4 = 1/20`, nonzero, on `n = 8`** — versus `1/n = 1/8`.

In general this family gives `Δ₁ = 1/(a(a+1)) = Θ(1/n²)`. So the leakage floor for a prefix cut is
`Θ(1/n²)`, not `Θ(1/n)`, and **W** does not sit at it. This does not damage the witness — `Δ₁ → 0` is
all the witness needs — but it removes Cor. 4.3's "nowhere further to go" rhetoric, and it removes the
only stated basis for ledger row 13. It also matters for §3: there is an entire `n`-fold range of
leakage scales below `1/n` at which a modulus could be calibrated and at which **W** is silent.

---

## 5. F3 — **REFUTED as stated**: the candidate repair (IB)

Dispatch press-point 5: *a proposed repair inside a refutation is the least-audited kind of claim.*
Correct. (IB) is false as written.

> **(IB)** *"…if `P` is not a chain and `P` is within `G(ε)n` interface modifications of an ordinal sum
> `P[A] ⊕ P[B]` across a cut with `Δ₁(A,B) ≤ ε`, then `P` has a `1/3`-balanced pair — **and one may take
> it to be an interface pair**, i.e. a pair `x ∥ y` with `x ∈ A, y ∈ B`."*

**Counterexample 1 — modulus-free, `n = 3`.** `P = AC_2 ⊕ C_1`: `{u,v} < w`, `u ∥ v`. Take
`A = {u,v}`, `B = {w}`. `P` is not a chain ✔. `P` **is** `P[A] ⊕ P[B]` exactly, so it is within
`G(ε)n` modifications for **every** `G ≥ 0` ✔. `Δ₁(A,B) = 0/1 = 0 ≤ ε` ✔. `P` does have a balanced pair
(`p_{uv} = 1/2`) — but **`P` has no incomparable interface pair at all**, so the second clause fails.
Every exact ordinal sum with a non-chain side does this. ∎

**Counterexample 2 — with a genuine modification and genuine leakage, `n = 8`.** Take the §4 poset
above: `Δ₁ = 1/20`, and it is one interface modification away from `P[A] ⊕ P[B]` (restore `x < b_1`).
Its **only** interface incomparable pair is `{x, b_1}`, and `x ≺ b_1` in 4 of the 5 extensions, so
`p^P_{x,b_1} = 4/5` — `min = 1/5 < 1/3`, **not balanced**. `P` *does* have a balanced pair —
`p^P_{x,c_2} = 2/5` — but both endpoints lie in `A`. So (IB)'s interface clause fails at leakage
`1/20`, with a real modification, admitted by any modulus `G(ε) ≳ √ε` (the very shape the document's own
amplification paragraph works with). ∎

**Severity, stated precisely, because it would be easy to over-read this.** The clause that does the
architectural work — *"`P` has a `1/3`-balanced pair"* — is **untouched by both counterexamples** and I
could not break it. So:

- **Claim 23** (*"(IB) would consume branch (ii)"*) survives: consuming (ii) needs only the balanced
  pair, not its location.
- **Claim 24** (*"(IB) is minimality-free, hence a special case of the 1/3–2/3 conjecture"*) survives,
  and I confirm it: (IB)'s statement contains no minimality hypothesis, and it does not relocate one —
  I checked whether minimality re-enters through `P[A], P[B]` being smaller, and it does not, because
  (IB) never invokes any property of the sides. **This part of the document is correct and it is the
  architecturally important part.** §7 property 5 — that a minimal counterexample is exactly where the
  migration mechanism is excluded — is the sharpest observation in the document and is unaffected.
- **The stated (IB) must not be pasted into STATE.md.** Minimal fix: drop the interface clause, or
  weaken it to *"and if no side of the cut supplies one, it may be taken at the interface."* The
  migration **observation** (claims 21, 22 — verified true of both families) stands; only its
  universalisation into (IB) fails.
- Cosmetic: (IB) opens *"There is `c > 0` and a modulus `G`"* and `c` never appears again. Dead
  quantifier.

The two supporting hand families both have `t ≥ 1` and both have a balanced interface pair by
construction, so *"supported by two hand families and by nothing else"* is accurate — and the boundary
case `t = 0`, which refutes it, was never tested.

---

## 6. F4 — the document's strongest claim is modulus-free, understated, and **missing from the ledger**

§5's table contains, as a row: *"Branch (iii) as a **standalone universal** (`Δ₁ ≤ ε ⟹ some side pair
preserved`) — **REFUTED**."* I checked it and it is **CONFIRMED, and it is the best thing here**:

- (iii)'s hypothesis is `Δ₁ ≤ ε` **alone** — there is no `|S| ≤ F(ε)n` clause (verified at `:471–472`).
  So **the §3 quantifier objection does not apply to it at all.**
- For every `ε > 0`, choose `n ≥ 1/ε`: **W** at `t = 2` has `Δ₁ = 1/n ≤ ε`, its only side balanced pair
  sits at exactly `1/2` in `P[A]`, and at `1/4` in `P`. The repaired predicate (`p^P ∈ [1/3,2/3]`) fails
  outright; the stated one fails once `F(ε) < 1/12`, which holds for small `ε` since `F(ε) → 0`.
- Therefore: **there is no `ε > 0` at which the repaired branch-(iii) predicate is a true universal.**

**This claim appears in no ledger row.** Claim 12 is `(T)` under the *branch-(ii)* hypothesis; claim 19
is `(ii) ⟹ (iii)`. Both carry the budget clause; this one does not, so it is strictly stronger and
strictly distinct. **The exhaustive-ledger discipline the document was specifically briefed on — and
which it invokes in §11's preamble — missed the document's own best result.** Same failure mode as
mg-88bd's 36-row ledger, one level up: not a prose implication left undrawn, but a boxed table row left
unledgered.

**Consequence the document leaves on the table.** §9 asks tentatively whether **W** contradicts
mg-3ce3's `0 RED / 6681 up to ε = 0.20`. Given the above, the logical question is already settled:
counterexamples exist at **arbitrarily small** `Δ₁`, so no `ε` calibrates that predicate. mg-3ce3's
`ε ≈ 0.20` cannot be the threshold of a true statement whatever the probe did — and mg-e35c F5 uses
exactly that number to move `ε_spec` by two orders of magnitude (STATE `:132`). That is an
**understatement to correct upward**, not a claim to trim.

---

## 7. F5 — §9 offers one explanation where there are two, and misses the likelier one

§9 attributes the mg-3ce3 discrepancy to family selection (antichain sides shift by `O(1/a²)`; one cross
removal is the zero-slack boundary). Both sub-facts are fine — the `O(1/a²)` is correctly labelled
HEURISTIC at claim 30, and the boundary fact is claim 16.

**The alternative it never considers: `δ(W) = 1/2`, so `W` is not frozen.** The document proves this
itself, in §5, two pages earlier. If mg-3ce3's search is restricted to the architecture-relevant class —
frozen (`δ < 1/3`) or minimal-counterexample-shaped posets — then **W** was never in its search space
and there is **no discrepancy at all**. That is at least as likely as family selection and it is one
line from facts the document has already established. Claim 29's *"UNVERIFIED (that it contradicts
mg-3ce3)"* is honestly labelled, so this is an incompleteness, not a broken label — but the recommended
action to pm-onethird ("hand this to whoever owns mg-3ce3 as a one-line falsifier check") should carry
**both** hypotheses, or the check will be run against the wrong one.

**Confirmed independently:** the probe doc is genuinely not in-tree — `git ls-tree -r main` finds no
`OneThird-L4-NearOrdinalSum-Stability-Probe.md` and no probe artifact of any kind. The document's
statement about its own evidential limits is accurate.

---

## 8. F6 — cross-doc: the correction is proposed at **one** of **three** STATE.md sites

The document's central corrective claim is that mg-e35c F3's *"no repair available"* is OVERSTATED. I
verified F3's wording at the source (`OneThird-lambda-std-Operative-Form-IndependentAudit.md:379–381`):
*"…with no repair available, because (ii) genuinely does not deliver a balanced pair."* ✔ quoted
accurately, and the OVERSTATED finding against it is **correct** — F3 argued from (ii)'s *wording* and
never tested the ordinal-sum route. Claim 28 CONFIRMED.

**But the phrase has propagated to three places in STATE.md, and §10 proposes a replacement for one:**

| site | text | covered by §10? |
|---|---|---|
| `STATE.md:89` (row 11) | *"branch (ii) is **unconsumed, with no repair available**"* | ✔ yes |
| `STATE.md:132` (mg-88bd row) | *"Step 6 has nothing to consume and **there is no repair available** — unlike (iii)"* | ✘ **no** |
| `STATE.md:168` (prose, *what the wall's conclusion has to deliver*) | *"and (ii) is unconsumed **with no repair available**"* | ✘ **no** |

**This is the mg-d112 cross-doc miss shape exactly** — the one the dispatch flagged: correct the site you
quoted, leave the site you did not read. Two of the three surviving sites would leave STATE.md
internally contradictory the moment row 11 is amended. pm-onethird must fix all three, and the
deliverable should have enumerated them.

---

## 9. F7 — an unledgered, under-specified numeric assertion in prose

§6, removal-reading bullet: *"e.g. in `C_m ⊕ AC_2`-plus-free-point configurations **a single deletion
moves a pair from `1/3` to `1/2`**."* No ledger row, no derivation, and the configuration is not pinned
down (which free point, which deletion, which pair). I could not reconstruct it as written and so cannot
grade it either way. It is doing rhetorical work — it is the only support offered for *"induced
subposets do **not** preserve `p_{xy}`"* — and it is **exactly the class of object §11's preamble
promises to catch** (*"including reductions asserted in prose — which is the failure mode this ticket
exists to avoid"*). The surrounding qualitative point is true and is already carried by Prop. 4.5;
the numeric instance should be specified or dropped.

---

## 10. Ledger audit — all 33 rows plus the 4 prose reductions

Re-derived, not read. **`CONFIRMED` = I reproduced it; `BROKEN` = the label is unearned.**

| # | subject | doc label | my finding |
|---|---|---|---|
| 1 | LE(`A⊕B`) = concatenations; pairwise-exact `p` | PROVEN | **CONFIRMED** — bijection re-derived; the pairwise strengthening is real and is free |
| 2 | `δ(A⊕B) = max(δA, δB)` | PROVEN | **CONFIRMED** |
| 3 | identity is about `P'`, not `P` | PROVEN | **CONFIRMED** (trivial and correctly labelled) |
| 4 | `P[A],P[B]` strictly smaller, in scope | PROVEN | **CONFIRMED** — `A,B ≠ ∅` from `Δ₁`'s denominator ✔ |
| 5 | "strictly smaller" survives both readings | PROVEN | **CONFIRMED** |
| 6 | both-chains ⟹ R4 fails, minimality yields nothing | PROVEN | **CONFIRMED**; source flags it unhandled at `:477–478` ✔ |
| 7 | (T) is verbatim (iii)'s conclusion, unavailable inside (ii) | PROVEN | **CONFIRMED** — a disjunct may not be assumed inside a sibling case ✔ |
| 8 | `W` is a poset; (ii) holds with `\|S\| = t` | PROVEN | **CONFIRMED** on the poset; **unit-ambiguous** on `\|S\|` (§3.6) |
| 9 | `σ_P` uniform on `t+2` extensions | PROVEN | **CONFIRMED** |
| 10 | `p^P = 1/(t+2)`, `p^{P[A]} = 1/2`, `Δ₁ = t/((t+2)a)` | PROVEN | **CONFIRMED**, including the `n=8` case |
| 11 | `{x,y}` the sides' only incomparable pair | PROVEN | **CONFIRMED** |
| 12 | R5/(T) false: `Δ₁ = 1/n`, `1/2 → 1/4` | PROVEN | **CONFIRMED** as an instance; see 13 for its universal reading |
| 13 | **no modulus `F` exists** | PROVEN | **BROKEN** (§3). True as *"for every `F(ε) = Ω(ε)`"*; false as stated; its stated basis is also false (§4). Contradicts row 16 |
| 14 | Step 6 as written cannot consume (ii) | PROVEN | **CONFIRMED CONDITIONALLY** on `F(ε) = Ω(ε)`; inherits 13 |
| 15 | amplification `t = ⌈√n⌉` | PROVEN | **CONFIRMED** |
| 16 | tolerance `t ≤ 1`; needs `F(ε)n ≤ 1` | PROVEN for `W`; conditional in general | **CONFIRMED and correctly labelled** — this row is right and row 13 is its over-statement |
| 17 | vindicates mg-88bd §3.3's steelman, tightens `O(1)` → `≤1` | PROVEN given 16 | **CONDITIONAL** — inherits 16's family-conditionality; the `n`-dependence reading is invalid (§3.2) |
| 18 | non-Lipschitz; `p_{xy}` is global | PROVEN | **CONFIRMED** — `d_TV` figures re-derived; the mechanism (`y` participates in no modification; `t` deletions buy `t` slots of slide) is right and is the document's best explanation |
| 19 | `(ii) ⟹ (iii)` REFUTED | PROVEN | **CONFIRMED CONDITIONALLY** on `F(ε) = Ω(ε)` (same budget clause). See also §11 on how §10 states it |
| 20 | `W` refutes neither L4 nor the conjecture | PROVEN | **CONFIRMED** — `δ(W) = 1/2` re-derived; correct and important |
| 21 | `p^P_{x,b_i} = (i+1)/(t+2)` | PROVEN | **CONFIRMED** |
| 22 | second family; `1/3, 2/3` at `t=2` | PROVEN | **CONFIRMED** |
| 23 | (IB) would consume (ii) | CONDITIONAL on (IB) | **CONFIRMED** for the balanced-pair clause; the **interface** clause is false (§5) |
| 24 | (IB) minimality-free ⟹ special case, not a reduction | PROVEN (logic) | **CONFIRMED** — checked for relocated minimality; there is none |
| 25 | minimality spent once, not twice; `:527` wrong on (ii) | PROVEN given 14+24 | **CONFIRMED given 14**, so conditional as 14 is; and *"wrong"* overshoots `:478–479` (§2) |
| 26 | in a minimal counterexample the migration is excluded | PROVEN | **CONFIRMED** — immediate from `δ < 1/3`, and it is the sharpest point in the document |
| 27 | C3 (no argument can consume (ii)) | NOT ESTABLISHED — declined | **CORRECT, and correctly declined** |
| 28 | mg-e35c F3's "no repair available" OVERSTATED | PROVEN | **CONFIRMED** — F3's text pulled and read (§8) |
| 29 | `W` at `n=8` is a RED for the repaired (iii) predicate | PROVEN / UNVERIFIED split | **CONFIRMED**, and the split is exactly right |
| 30 | likely cause is family selection | HEURISTIC | **CORRECTLY LABELLED**, but incomplete — the frozen-restriction hypothesis is missing (§7) |
| 31 | mg-88bd's `ε_spec` pinning untouched | PROVEN (logic) | **CONFIRMED** — `ε_spec` prices Step 2's input, upstream ✔ |
| 32 | removal reading adds "pair must avoid `S`" | PROVEN | **CONFIRMED** |
| 33 | cross-only modification is the adopted reading | CONDITIONAL on the reading | **CONFIRMED** — `:469–470` says "interface elements" and names `P[A],P[B]`; both point that way ✔ |
| **—** | **(iii) as a standalone universal is REFUTED at every `ε`** (§5 table) | **absent** | **CONFIRMED — and MISSING from the ledger** (§6). Strongest result in the document |
| **—** | *"a single deletion moves a pair from `1/3` to `1/2`"* (§6) | **absent** | **UNGRADEABLE** — under-specified (§9) |
| R-a | route reduces (ii) to (iii) | PROVEN | **CONFIRMED** |
| R-b | minimality's only output on (ii) is side pairs | PROVEN | **CONFIRMED** |
| R-c | (IB) closes (ii) | CONDITIONAL | **CONFIRMED** as conditional; (IB) needs the §5 repair first |
| R-d | restructuring, not completing, at `:527` — branch (ii) only | PROVEN for (ii) only | **CONFIRMED**, and the "not asserted for (i)/(iii)" restriction is correct and important |

**Tally:** 27 CONFIRMED · 3 CONFIRMED-conditionally (14, 17, 19) · 1 **BROKEN** (13) · 1 **REFUTED as
stated** ((IB)'s interface clause, inside 23) · 1 ledger omission (the strongest claim) · 1 ungradeable
prose numeric · 0 arithmetic errors anywhere.

---

## 11. Appendix A step 4c — the proposed STATE.md text, audited clause by clause

*The proposed row is a primary target, not a précis. Third arc in a row where the body is more careful
than the row.*

| clause in §10 | body support | verdict |
|---|---|---|
| *"branch (ii) is unconsumable by Step 6 **as written** — PROVEN"* | claim 14 | **CONDITIONAL, not PROVEN** — must read *"for any modulus `F(ε) = Ω(ε)`"* |
| *"a quantitative failure that survives `ε → 0`"* | claims 12, 15 | **CONFIRMED** |
| the witness parameters, `Δ₁ = 1/n`, `1/2 → 1/4`, "**two** interface modifications" | §4 | **CONFIRMED** arithmetically; "two" is the *relation* count while (ii) counts **elements**, where it is one (§3.6) — the row must fix the unit, since the whole argument turns on 1 vs 2 |
| *"**Shrinking `ε` does not help**"* | Cor. 4.3 | **CONFIRMED** |
| *"no improvement to Steps 2–5 supplies the missing modulus, **because there is no modulus**"* | claim 13 | **BROKEN** — the clause before "because" is true, the clause after is the false universal (§3) |
| the non-Lipschitz structural cause | claim 18 | **CONFIRMED** — accurate and well stated |
| *"transport needs `F(ε)n ≤ 1`, an **`n`-dependent condition**, vindicating … and tightening `O(1)` to `≤ 1`"* | claims 16, 17 | **BROKEN** — row 16 labels this family-conditional; the `n`-dependence step is §3.2's invalid inference; and STATE `:132` says this flips the mg-88bd answer. **Highest-stakes clause in the row** |
| *"`(ii) ⟹ (iii)` is REFUTED, so the cheap repair 'drop (ii), keep (i)∨(iii)' is **unavailable**"* | claim 19, §5 | **OVERSTATED.** In **W**, branch **(i)** holds (`δ = 1/2`), so the *statement* `(i)∨(iii)` is **true** in **W** and is untouched. What dies is only the **absorption derivation** of `(i)∨(iii)` from L4. §5's table says this correctly (*"(ii) cannot be absorbed into (iii)"*); §10 restates it as the repair itself being unavailable. Plus the same budget-quantifier caveat as 19 |
| *"R4 has a second, prior gap … if both sides are chains"* | claim 6 | **CONFIRMED**, and correctly attributed to `:477` |
| *"`W` refutes implications, not theorems: L4 itself survives via branch (i)"* | claim 20 | **CONFIRMED** — the best-calibrated sentence in the row |
| *"**Do not record this as 'branch (ii) is unrepairable'** — that is a different claim and it is not established"* | claim 27 | **CONFIRMED, and this instruction should be kept verbatim** |
| *"mg-e35c F3's 'no repair available' is OVERSTATED; its reason clause is CONFIRMED"* | claim 28 | **CONFIRMED** — but the row fixes one of three STATE.md sites (§8) |
| *"balance migrates from the side to the interface"* + both families' numbers | claims 21, 22 | **CONFIRMED** as observations about the two families |
| **(IB)** stated verbatim, with the **interface** clause | §7 | **REFUTED as stated** (§5, `n=3` modulus-free and `n=8` with real leakage). **Must not be pasted.** Drop or condition the interface clause; the rest survives |
| *"(IB) is minimality-free, hence a special case of the 1/3–2/3 conjecture itself, not a reduction of it"* | claim 24 | **CONFIRMED** — the durable architectural finding, and it survives the (IB) repair |
| *"the `⟹ balanced pair by minimality` box at `:527` is **wrong** on that branch"* | claim 25 | **CONFIRMED in substance, OVERSTATED in word** — `:478–479` already calls transport "the task", so *"justified only on (i)/(iii); on (ii) the source's own prose concedes the gap and this shows the gap cannot be closed by transport at any `F(ε) = Ω(ε)`"* is the exact claim |
| *"(IB) is new, unproven, implied by nothing in L1–L3, appears nowhere in the corpus"* | claim 23 | **CONFIRMED** — I checked L1–L4 at `:556–570`; nothing there implies it |
| *"in a minimal counterexample its rescue mechanism is exactly what `δ(P) < 1/3` forbids — which is either why 'minimal counterexample + (ii)' is empty, or why it is not. **That is the live question**"* | claim 26 | **CONFIRMED, and this is the most valuable sentence in the row.** It should be promoted, not buried at the end |
| the mg-3ce3 flag paragraph | §9, claims 29, 30 | **CONFIRMED but doubly incomplete** — understates the logical side (§6: no `ε` calibrates that predicate, for *any* modulus) and omits the frozen-restriction explanation (§7) |
| the `STATE.md:64` graph-edge amendment | §10 | **CONFIRMED** — `:64` reads exactly as quoted; the proposed replacement label is accurate |

**Row verdict: do not paste.** Three clauses need repair before it lands (the "no modulus" universal,
the `n`-dependence inference, and (IB)'s interface clause), one needs a unit fix, one needs narrowing
("unavailable" → "not absorbable"), and one needs its two missing STATE.md sites added.

---

## 12. Object / coordinate check (Appendix A step 5)

No object conflation found. `δ` (balance, Axis 2) and `Δ₁` (cut geometry, Axis 1) are kept distinct
throughout — §5's *"`W` is not a counterexample"* row turns on exactly that distinction and gets it
right. `ε_spec` versus `ε_leak` is handled correctly in §8: the document explicitly declines to disturb
mg-88bd's pinning on the ground that `ε_spec` prices Step 2's *input*, upstream of the R5 failure
(claim 31, CONFIRMED). `p_{xy}` is consistently a functional of the **whole** poset — that is the
content of Prop. 4.5 and it is right. **One coordinate the document introduces and does not name:**
`F` has two distinct roles in L4 — a *budget* in (ii) (`F(ε)n` elements) and an *error tolerance* in
(iii) (`F(ε)` in probability). §3's quantifier failure is the direct consequence of running them
together, since only the first admits or excludes a witness.

---

## 13. Constraint compliance (Appendix A step 7) — **CLEAN**, verified against the commit

Verified at `a3164dd`, not from the document's own sentence: `git show a3164dd --name-status` reports
**`A docs/OneThird-L4-Branch-ii-Consumability.md`** and nothing else — one markdown file, zero scripts,
zero datasets, zero enumerations. Every table in the document is a slot count over `t+2 ≤ 6` linear
extensions of a poset on `≤ 8` elements; every constant is a rational with a denominator of `t+2`,
`t+1`, or `a`. **All of it is plausibly — and, as of this audit, actually — hand-derived: I reproduced
every one of them by hand.** No number in the document required or suggests computation. The `O(1/a²)`
estimate in §9 is a sketch and is labelled HEURISTIC. This audit likewise commits one markdown file and
ran nothing.

---

## 14. What pm-onethird should do

Ordered by cost of getting it wrong. **I have not edited STATE.md; these are consequences for
pm-onethird to land, and this audit is not a report to Daniel.**

1. **Strike the "no modulus" universal from the row and from §0's framing.** Replace with the dichotomy
   of §3.3. The RED on Step 6 survives at *"for any modulus `F(ε) = Ω(ε)`"* — state the condition; it is
   short and it is almost certainly satisfied, and "almost certainly" is not `PROVEN`.
2. **Do not land the `n`-dependence clause.** STATE `:132` makes it a row-flipper for mg-88bd, and it
   rests on an invalid quantifier step (§3.2). The document's own ledger row 16 already labels the
   underlying claim family-conditional.
3. **Repair (IB) before recording it** — drop or condition the interface clause (§5). Claims 23, 24 and
   §7's property 5 survive the repair untouched; property 5 is the finding worth promoting.
4. **Correct "no repair available" at all three STATE.md sites** — `:89`, `:132`, `:168` (§8), not just
   row 11.
5. **Add the modulus-free result to the record**: branch (iii) as a standalone universal is refuted at
   every `ε`, for every modulus. This is the document's strongest claim, it is missing from its ledger,
   and it settles the §9 flag logically: **no `ε` calibrates the repaired branch-(iii) predicate**, so
   mg-e35c F5's use of `ε ≈ 0.20` to move `ε_spec` by two orders of magnitude needs re-examining on its
   own terms.
6. **When routing the `n = 8` falsifier to mg-3ce3, carry both hypotheses** — family selection *and*
   the frozen restriction (`δ(W) = 1/2`, so **W** may simply be out of the probe's class, in which case
   there is no discrepancy).
7. **Keep, verbatim**: the C1/C2/C3 separation, the explicit declining of C3, "`W` refutes implications,
   not theorems", "do not record this as branch (ii) is unrepairable", and §7 property 5. Those are the
   document's durable contribution and they are correct.

**Honest net.** A genuinely good witness and a genuinely informative negative about the ordinal-sum
route, carrying one false universal in its headline, one false lemma in its proposed repair, and one
true theorem it did not claim. **The mathematics is right; the quantifiers are not** — which is the same
verdict shape as the last two audits in this arc, at a different quantifier each time.
