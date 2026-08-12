# OneThird — THE SHAPE OF THE ARGUMENT: where L1b sits, and whether *bound → prefix → contradiction* is it

**Filed by** `mg-3af8` on Daniel's direct question, 2026-08-12, following `mg-05ec`'s verdict that
the spectral route is not *the* bridge:

> *"So if spectra aren't the bridge how do we reframe L1b and understand its role in the proof at a
> high level? Is it linear statistic bound -> assemble prefix set -> contradiction etc"*

**Kind of this document:** a **reframing**, and like its parent it **produces no new mathematics**.
It re-describes an argument that is already in the corpus; every claim about that argument points at
the row, item, or document that earns it. `mg-05ec`'s verdict is an **input** here and is not
re-litigated: one bridge, it is L1b, it is `OPEN`, and it is not spectral in any load-bearing sense.

**Companion, not a fork.** [`docs/CONCEPTS.md`](CONCEPTS.md) (`mg-602d`) describes **the space** —
what the objects mean. **This describes the argument** — what the chain is and where each piece
enters. Where they touch, `CONCEPTS.md` §4 is the conceptual statement of the bridge and this is the
structural one; each cites the other and neither restates it.

---

## 0. VERDICT — the four answers, and they stand alone

> **1. The chain.** It is a **closed loop on one hypothesis, not a line.** *Assume a minimal
> counterexample: every incomparable pair of `P` is more than 2/3-decided toward one order `e`
> (frozen).* From that, **(L1b — the wall, `OPEN`)** derive that a random linear extension barely
> moves off `e` — `E[inv_e] ≤ (ε_spec/6)(n²−1)`. From that, **(rows 5 + 10)** cut `P` at a prefix
> with a thin interface. From that, **(L4, `OPEN`)** find a pair inside one side whose balance
> survives being lifted back to `P`. That pair is balanced — which contradicts the assumption we
> started from. **The premise and the contradiction are the same statement**, and everything between
> them is machinery.
>
> **2. Daniel's shape: YES on all three moves and in that order — and it is closer to the live
> argument than `STATE.md`'s own diagram is, because it has no spectral node in it.** Three joints
> are wrong, and naming them is more use than either a yes or a rewrite. **(J1) It has no premise.**
> The chain does not begin at a bound; it begins at *frozen*, the only hypothesis in it with any
> content, and the closing contradiction is with that same hypothesis. **(J2) The
> linear-statistic bound is the OPEN move, not the input** — it is L1b itself, row 8, the whole
> remaining gap; and the word *linear* is precisely what is **exhausted**: every bound derivable
> from the pair marginals alone is capped at `ε_sup < 1` by an **equality** (`mg-6bc2` Claim 3.1),
> against a demand near `2×10⁻²`. **(J3) *Contradiction* is two links, and one of them is separately
> open** — L4 (row 11) does the transfer, and only then does minimality bite; folding them into one
> word makes a two-hole chain read as a one-hole chain.
>
> **3. L1b without the word *spectrum*.** *If every question about `P` is nearly settled one pair at
> a time, then `P` is nearly settled all at once.* Formally: **frozen ⟹ `E[inv_e] ≤ (ε_spec/6)(n²−1)`
> for an explicit absolute constant, uniform in `n`.** It is a **rigidity** statement — what is
> asserted to be rigid is the assignment of elements to positions — and its whole difficulty is that
> the local-to-global upgrade it asserts is **false for abstract measures** (a two-atom law is frozen
> and has `Θ(n²)` inversions). So L1b is the claim that *being a real poset's linear-extension
> measure* is what turns pairwise near-decidedness into global near-order. `E[inv_e]` carries it
> because that is the unit both sides of the live gap are already stated in, the unit the conversion
> to `λ_std` consumes, and the unit the three live residuals feed.
>
> **4. What changed and what did not — one line.** **The description changed and the dispatch
> changed; the mathematics and the size of the hole did not.** No row's kind moved, no row's status
> moved, row 8 is still `OPEN` and still the whole gap, the supply is still `ε_sup < 1` against a
> demand near `2×10⁻²`, and the obstruction is still that the proof must reach the joint law. The
> single operational consequence is that work should not be aimed at node `B`.

---

## 1. THE CHAIN, in the register a reader can hold

Six sentences. Notation only where it is the shortest way to say the thing.

1. **Suppose the conjecture is false.** Take a smallest poset `P` where it fails: no incomparable
   pair splits its linear extensions anywhere near evenly. Every incomparable pair is more than
   2/3-decided, and all the biases point the same way — they line up into one distinguished order
   `e` (`STATE.md` glossary; **frozen** is `δ(P) < 1/3`).
2. **That is a statement about pairs, one at a time.** The whole proof is an attempt to upgrade it
   into a statement about the *whole* random linear extension at once: if every pair is nearly
   decided, then a random linear extension of `P` should sit near `e`. **That upgrade is L1b, and it
   is the wall** (row 8, `OPEN`). In its live unit it says `E[inv_e] ≤ (ε_spec/6)(n²−1)` — a random
   extension inverts only a small constant fraction of the pairs it could invert.
3. **A poset that near `e` has a thin place.** Sweep `e` from the front and cut: at some prefix
   `A_k = {1,…,k}` the interface — the elements that cross it under a random extension — is thin
   (row 5, Buser, `U`, **proven**; that the *best* cut is a prefix is row 10, `FP`, `125/126` at
   `n ≤ 6`).
4. **A thin interface means the two sides barely interact**, so `P` looks locally like `P[A_k]`
   stacked on `P[A_kᶜ]` — and each side is *smaller* than `P`, so by minimality each side has a
   balanced pair.
5. **Push that pair back up into `P`.** This is **L4** (row 11, `OPEN`, secondary): a pair that is
   balanced inside one side must still be balanced in the whole poset. The interface being thin is
   what is supposed to protect it.
6. **The pair is balanced, and we assumed no such pair exists.** Contradiction. No minimal
   counterexample, so 1/3–2/3 holds.

**The shape of that is a loop, and reading it as a line is the single most common way to lose the
plot.** Step 1 assumes *no balanced pair*; step 6 produces one. Everything between is the cost of
that round trip, and both open links — L1b and L4 — are open **because of what they must do with the
frozen hypothesis**, not for independent reasons. `mg-dcae` reached the same point from the
Alexandrov–Fenchel side and stated it as a rule: any usable statement here *"must consume the frozen
hypothesis directly."*

---

## 2. THE MAP — Theorem E, Steps 1–6, the three residuals, and where L1b enters

The programme's own six steps, quoted at `mg-9461` §1.1 from
`spectral_near_ordinal_sum_program.tex` `:486–516`:

```
Step 1  Assume P is a minimal counterexample and label it by its distinguished order e=12…n.
Step 2  Port the known bad-mixing argument … to obtain  λ_std(P) ≥ 1 − ε   with sufficiently small ε.
Step 3  Prove that the dominant standard eigenvector is monotone in e, or directly produce a
        low-conductance prefix.
Step 4  Apply Cheeger sweeping to obtain  A_k = {1,…,k},  Φ_P(A_k) ≲ √ε.
Step 5  Interpret this as an L¹ near ordinal sum:  E K_k ≪ min(k, n−k).
Step 6  Use near-ordinal-sum stability to transfer a balanced pair from P[A_k] or P[A_kᶜ] to P,
        contradicting minimality.
```

⚠️ **Provenance of that quote, stated rather than assumed.** It is **read from `mg-9461` §1.1**, not
re-verified at the source: the `.tex` lives outside this repository (`STATE.md` row 9 says so of the
same file), and on this host it is an unmaterialised iCloud file that cannot be opened. **Kind:
documentary, at second hand.** Nothing below turns on the wording; what it is used for is the
*shape*, which `STATE.md`'s ledger states independently.

| link in `STATE.md`'s diagram | source step | rows it consumes | weakest kind | on a live route? |
|---|---|---|---|---|
| **A** — assume a minimal counterexample (primitive · frozen) | Step 1 | — | hypothesis | **yes** — the only premise |
| **A → B** — Theorem E: frozen pair ⟹ low-conductance BK cut | the intended supply for Step 2's *"port"* | row 6 | `U`, **proven**, any width (`mg-957a`) | **NO — node `B` is unconsumed** (`STATE.md:78`, ⚠️ **documentary**) |
| **B → C** *(as drawn)* / **A → C** *(as worked)* — **L1b, ★ the wall** | Step 2's **conclusion**, reached without the port | rows 5 + 7, via `mg-210d`'s master bound | **`OPEN`** | **yes — this IS the gap** |
| **C → D** — thin, low-conductance prefix interface | Steps 3–4, landing Step 5 | rows 5 (`U`) + 10 (`FP`, `125/126`, `n ≤ 6`); Step 3 is row 9 | **`FP`** | **yes** |
| **D → E** — L4: thin interface ⟹ a balanced pair survives | Step 6 | row 11 | **`OPEN`** (secondary) | **yes**, and it carries `mg-3af9`'s hole |
| **E → F** — a balanced pair contradicts `δ < 1/3` | Step 6's *"contradicting minimality"* | — | `U` by minimality | **yes** |

**Three readings fall out of that table, and they are the answer to *where does everything sit*.**

**(a) L1b enters as Step 2 — but not as Step 2 is written.** The source's Step 2 says *"**Port** the
known bad-mixing argument"*: its intended supply is Theorem E's BK cut, which is exactly the
`A → B → C` route. The live work reaches Step 2's **conclusion** by a different road — frozen ⟹
`(LIB-const)` ⟹, by `mg-210d`'s master bound `1 − λ_std ≤ 6·E[inv_e]/(n²−1)`, the `λ_std` form —
consuming **rows 5 and 7 and nothing else**, with no sector decomposition and no representation
theory (`STATE.md:82–84`, settled at `mg-a1db` on `mg-65f5`'s R1). **The word *"Port"* is the entire
spectral framing of this programme, and replacing it with *"prove directly from frozen"* is what
`mg-05ec`'s verdict amounts to at the level of the argument.**

**(b) Theorem E sits off the live chain, and its return condition is nameable.** It is proven, it is
any-width (row 6, `U`, the width-3 hypothesis found present-and-inert by `mg-957a`), and what it
hands the architecture is a **cut, not a number** — an upper bound on the BK gap, running the other
way. Nothing live consumes it. ⚠️ **That observation is DOCUMENTARY, not mathematical** (`mg-05ec`
§4.4, landed at `STATE.md:78`): it is a reading of what the ledger says its own chain consumes at
`c5cd288`, **not** a proof that no BK-mediated route to L1b exists. Theorem E **returns to the
critical path the moment anyone proves L1b through the BK cut rather than through inversions** — and
that would weaken `mg-05ec`'s verdict from *"not the bridge"* to *"not the only bridge"*, not reverse
it, its third leg being `FP✗` and independent.

**(c) The three residuals all sit on the `A → C` link, and none of them is spectral.** They are the
actual work in progress (`STATE.md` § *Where the threads converge*, `mg-a58f` ordered, `mg-d112`
audited): **(B-cov)** — break the wrong-signed same-side covariance, the covariance term of
`E[Σ disp²]`, *"the sharp edge"*; **(EQ)** — `max_x |E[pos_σ x] − rank_e x| = O(1)`, a first moment
of the position law and *"a cancellation statement rather than a decay statement"*; **(R)** — is
there `D < 1` with `d(P) ≤ D` on every frozen poset, a pure count on `P` itself. Two are counting
statistics of `L(P)`; the third counts incomparabilities in `P`. **All three are attacks on move 1
of Daniel's shape**, and the spectral statement is only what each would be *converted into* on
arrival.

---

## 3. DANIEL'S SHAPE, TESTED — *linear statistic bound → assemble prefix set → contradiction*

**Verdict: yes on all three moves, yes on the order, and three joints wrong.** Taken as a
description of the argument's spine it is correct where `STATE.md`'s own mermaid diagram is
misleading, and the reason is worth stating first because it is a point *for* the framing, not
against it.

**What it gets right that the diagram does not.** The shape has **no spectral node and no BK cut in
it at all**. That is the `A → C`-direct rendering — the one row 8 and the machinery paragraph
actually use — and it is why the diagram needed the rider `mg-c59e` landed at `STATE.md:78`. A
dispatcher working from Daniel's three moves would aim at the three live residuals; a dispatcher
working from the diagram would aim at node `B`.

And the middle move is not an approximation of the argument — **it is literally the surviving half
of the source's Step 3.** Step 3 reads *"the dominant standard eigenvector is monotone in `e`, **or**
directly produce a low-conductance prefix."* The **first** disjunct is row 9, refuted as stated
(`FP✗`, `2/126` at `n = 6`) — L2 itself is `OPEN` as a disjunction, and what remains standing is the
prefix clause. **The eigenvector half of Step 3 is already dead; *assemble prefix set* is the live
half, in the source's own words.**

### The three joints

**J1 — the shape has no premise, and the premise is the whole reason the links are hard.**

The chain does not start at a bound. It starts at **frozen** (`δ(P) < 1/3`, Axis 2) and the
contradiction at the far end is with **that same statement**. Two things follow that a
bound-first reading loses:

- **The argument is a loop.** *No balanced pair* in; *a balanced pair* out. A reader who holds only
  the three moves will look for what the contradiction is *with*, and there is nothing downstream to
  find — it is upstream, in the assumption.
- **The premise is load-bearing in a way no other hypothesis in the chain is.** Both faces of the
  single lemma are **false for abstract frozen distributions** (`STATE.md:145`, obstruction 4), so
  the proof must use that `σ` ranges over a **real poset's** linear extensions. `λ_std`'s own
  definition depends on a reference order and *"moves by up to `1/3` across reference orders"*
  (4,069 of 4,824 posets at `n = 6`, `mg-c4f5`) against a target near `2×10⁻²` — **frozen is what
  removes that choice**, because `e` is canonical. That is a hypothesis doing work, not a
  convention.

**J2 — *linear statistic bound* is the OPEN move, and the modifier *linear* names the exhausted
route.**

The **currency is exactly right**: `E[inv_e]` is a linear statistic — the expectation of a sum of
one indicator per incomparable pair — and it is the live currency of the wall. But two corrections:

*It is the target, not the input.* Move 1 **is** L1b, row 8, `OPEN`, the whole remaining gap. A
shape that opens with it reads as though a bound were in hand and the work were downstream; the
opposite is true. Rows 5, 7, 10 and the sweeping machinery are the proven part, and everything the
shape lists *after* move 1 is cheaper than move 1.

*And information that is linear in the pair marginals is closed, not merely unsharpened.* This is
the sharp point:

```
    max{ 6·E_μ[inv_e]/(n²−1) : μ ∈ M_n(η) }  =  (1 − 3η)·n/(n+1)
```

— attained at **every** `η > 0`, both directions **proven for all `n`** (`mg-6bc2` Claim 3.1;
`M_n(η)` is every measure on `S_n` with each pair flipped against `e` with probability `≤ 1/3 − η`).
⚠️ **Carry the `η`: `n/(n+1)` is a SUPREMUM over the frozen class, not a maximum in it** (`mg-832f`
Correction 2) — frozen is `δ < 1/3` **strict**, and the `η = 0` witness has every pair at exactly
`1/3`, i.e. outside the hypothesis. **The closure is unaffected**: `Op-Form` Claim 6.1 is an
**equality for the information it consumes**, so `ε_sup < 1` is not a bound awaiting a better
argument — every route below it must add a **realizability** fact (`mg-92e6`'s adjacency symmetry is
the first that bites). Against that, the constant that suffices is `ε_dem ≈ 2×10⁻²`, and the
published gap factor is **~50**. ⚠️ **Frames, because these numbers are frame-sensitive:** the
`2×10⁻²` is the **repaired** calibration and is **unpinned by ~2 orders of magnitude**, and
`ε_dem = ε_leak²/(2C₃)` with **`C₃` unquantified** (`STATE.md:21`). ⚠️ **And do not read the `1/6`
that appears elsewhere as a sharpening of this `1`** — they are the same theorem in two
normalisations, `÷n²` versus `÷(n²−1)/6`, and proving `ε_spec = 1/6` from pair bias would be proving
a statement **6× stronger** than the `1/6` already proven (`mg-6bc2` §2.1).

**So move 1 is the right target in the wrong tense, and its modifier is the exact thing that is
spent.** The bound must be linear *in the statistic* and cannot be linear *in the information*: it
has to reach the **joint law**.

**J3 — *contradiction* is two links, and one of them is separately open.**

Prefix ⟹ contradiction is not one step. Between them sits **L4** (row 11, `OPEN`, secondary): the
transfer of a balanced pair from `P[A_k]` or `P[A_kᶜ]` up to `P`. Only after that does minimality
bite, and minimality is the cheap part. Two riders:

- **L4 is not merely open; Step 6 has a hole `mg-3af9` opened that is independent of L1b.** Branch
  (ii) of L4 is **unconsumed by Step 6's stated transfer for every strictly positive modulus** —
  unconditional, via the witness `W*`; the only escape, `F ≡ 0`, reads (ii) as *exact* ordinal sum,
  which makes L4 strictly stronger rather than repairing Step 6 (row 11, audited `mg-c8c6`).
- **Naming both links matters for how the programme reads.** With `contradiction` as one word, the
  chain has one hole; with L4 named, it has two, and the second is not downstream of the first.

### One more thing move 2 buys, which is not a correction

**There is already a route in this corpus that does Daniel's middle and last moves with no spectral
statement anywhere in them** — the **direct-prefix route** (`mg-00b9`, repaired `mg-2de0`). Its
audit asked exactly the question the reframe raises — *"does the contradiction follow with NO
spectral statement?"* — and answered **yes on the route repaired**, the repair being one character
wide (`n²` ⟶ `n² − 1`). It reaches `Δ₁ ≤ 2/3` against `ε_leak ≈ 0.20`: short by a factor of about
3.3 — *that ratio is this document's arithmetic on `STATE.md:21`'s two figures, not a figure either
source states* — so short by a factor, not by a category. `STATE.md:21` names its consequence — **if it ever closed it would make the
counterexample class empty**, rather than making the constant L4-dependent. **It is the closest
existing object to the shape Daniel proposed, and it is filed under a name that does not advertise
that.**

---

## 4. WHAT L1b IS, with no spectrum in it

> **L1b (the wall) — row 8, `OPEN`.** Let `P` be a finite poset on `n` elements in which every
> incomparable pair is more than 2/3-decided in the direction of one distinguished order `e` — that
> is, `δ(P) < 1/3`, *frozen*. Then a uniformly random linear extension `σ` of `P` is **close to
> `e`**: the expected number of incomparable pairs it inverts satisfies
>
> ```
>     E[ inv_e(σ) ]  ≤  (ε_spec / 6) · (n² − 1)
> ```
>
> for an **explicit absolute constant `ε_spec`, uniform in `n`**. The constant, not a limit, is what
> the architecture consumes (`mg-88bd`, audited `mg-e35c`).

**What is asserted to be rigid.** The assignment of elements to positions. The hypothesis is a
statement about pairs **one at a time**: each incomparable pair, considered alone, is nearly decided.
The conclusion is a statement about the permutation **all at once**: it barely moves off `e`. So L1b
is a **local-to-global rigidity** statement — *local near-decidedness forces global near-order* — and
the picture `CONCEPTS.md` §4 gives is the same one in a sentence: *if every question about `P` is
nearly settled, then `P` is nearly a stack of blocks.*

**And the reason it is hard is that the upgrade is false in general.** For an *abstract* measure you
can have every pair frozen and still `Θ(n²)` inversions — the two-atom law (`STATE.md:145`). So the
only thing that can make L1b true is that `σ` ranges over the linear extensions of a **real poset**.
**L1b is precisely the claim that being a real poset's linear-extension measure is what turns
pairwise near-decidedness into global near-order.** That sentence is the whole content, and it has no
eigenvalue in it — nor any spectrum, walk, mixing time, or sector.

**Why `E[inv_e]` is the quantity that carries it.** Five reasons, in order of how much they bind:

1. **Both sides of the live gap are already stated in it.** The supply — `ε_sup < 1`, **proven**,
   pair-bias, and **independent of L4** (`mg-345e`; `Op-Form` Claim 6.1) — and the demand,
   `ε_dem ≈ 2×10⁻²`. The whole remaining quantitative gap is a ratio of two numbers in inversion
   units, and **its numerator is L4-independent, so shrinking it from the left needs no L4 answer at
   all** (`STATE.md:21`).
2. **The spectral form is a report of it, not a source for it.** `mg-210d`'s master bound
   `1 − λ_std ≤ 6·E[inv_e]/(n²−1)` (Thm 2.4) is the conversion, and its whole proof spends **row 5**
   (Buser test vector on `S|_{𝟙⊥}`) and **row 7** (Diaconis–Graham) and nothing else. A proof would
   be *done* in inversions and merely *stated* in eigenvalues.
3. **Every other unit on Axis 1 maps into it by exact identity** — `Σ disp² = 2ΣK_m + 2ΣM_{k,l}`
   (GID), `ΣK_m ≤ inv ≤ 2ΣK_m` (DG), `footrule ≍ inv` — row 7, `U-id`, **proven**. `λ_std` is *one
   unit among five* (`STATE.md:19`), which is the first of `mg-05ec`'s three legs.
4. **The three live residuals feed it.** `(B-cov)` is a term of `E[Σ disp²]`, `(EQ)` a first moment
   of the position law, `(R)` a count on `P` that feeds the already-proven
   `λ_std > 1 − d·n/(n+1)`. None of them is an eigenvalue statement.
5. **The obstruction is stated in it too.** The two-atom law is a statement about inversions, not
   about a spectrum — which is why the hardness survives every change of unit.

⚠️ **One thing this section does not do.** It does not make L1b easier, restate it more weakly, or
supply any part of it. Row 8's status is unchanged and this is a *description* of an open problem.

---

## 5. WHY THE REFRAME DOES NOT SHRINK THE GAP

The risk in any reframe is that a cleaner sentence reads as progress. Stated flatly, so it cannot:

**WHAT CHANGED — two things, both about people rather than about posets.**

- **The description.** *"Two axes, one bridge"* survives unqualified and is the programme's real
  asset; what was struck is the word *spectral* attached to that bridge **as a method** (`mg-05ec`
  §5, landed `mg-c59e` at `STATE.md:25`). The bridge is now described as a **rigidity** statement
  whose live currency is `E[inv_e]`.
- **The dispatch.** Node `B` is marked unconsumed, so work aimed through the BK cut is aimed at a
  node nothing currently reads (`STATE.md:78`, ⚠️ **documentary**). The two legs of `mg-05ec`'s
  verdict that carry ledger kinds — `FP✗` (`mg-d1be`, `mg-8b64`) and `U`/`U-id` (rows 3a, 5, 6) —
  **are the ones to attack**; its two weakest legs are a corpus search and a documentary reading,
  and `mg-05ec` §6 says so itself.

**WHAT DID NOT CHANGE — everything mathematical.**

- **Row 8 is `OPEN`, is the wall, and is the whole remaining gap.** No row's kind moved and no row's
  status moved. `STATE.md:25` states this in as many words: *"This renames the route. It moves no
  row's kind and no row's status."*
- **The size of the hole is the same number it was.** `ε_sup < 1` against `ε_dem ≈ 2×10⁻²`, a
  published gap factor of **~50**, with the calibration **unpinned by ~2 orders of magnitude** and
  `C₃` **unquantified**.
- **The obstruction is the same obstruction.** Pair-marginal information is **closed at an
  equality**, both faces of the single lemma are **false for abstract frozen distributions**, and the
  proof must reach the **joint law**. None of that mentions a spectrum, which is the point — it was
  never the spectral framing that made it hard.
- **The second hole is still there.** L4 is `OPEN` and `mg-3af9`'s Step-6 hole is independent of
  L1b.
- **Nothing was proven here, and nothing was measured here.** This document ran no code and
  re-derived nothing.

**One line, if only one is read:** *the reframe changed what we call the bridge and where we point
work — it did not move a single row, and the hole is exactly as wide as it was yesterday.*

---

## 6. KINDS AND SCOPE — the standing rule applied to this document

`STATE.md:99`: *any prose that **aggregates** rows must state the **weakest** kind in the set it
names.* §0 aggregates.

| statement in §0 | kind | warrant |
|---|---|---|
| the six links exist and consume the rows named in §2's table | **documentary**, over `STATE.md` at `3ed1700` | a reading of the ledger and its diagram; **not** re-audited mathematics |
| the six steps, quoted | **documentary, at second hand** | read from `mg-9461` §1.1; the `.tex` is outside this repo and unopenable on this host |
| Theorem E; Buser; GID/DG; `λ_std = 1 ⟺` ordinal sum; `S_P = ρ_std(η_P)` | **`U` / `U-id`** | rows 6, 5, 7, 1, 3a, on the ledger's own authority — **not re-audited here** |
| L1b, and L4 | **`OPEN`** | rows 8 and 11 |
| best-cut-is-a-prefix | **`FP`**, `125/126`, `n ≤ 6` | row 10 — the load-bearing `FP` on the critical path |
| L2's first disjunct (the eigenvector clause of Step 3) refuted; L2 itself open | **`FP✗`** (`2/126`, `n = 6`) / **`OPEN`** | row 9, scope repaired at `mg-3329` |
| pair-marginal information is closed at `(1−3η)·n/(n+1)` | **proven for all `n`**, both directions; **supremum** over the frozen class, not a maximum in it | `mg-6bc2` Claim 3.1, `mg-832f` Correction 2 |
| `ε_sup/ε_dem ≈ 50`; `ε_dem ≈ 2×10⁻²` | **calibration, unpinned by ~2 orders of magnitude**, `C₃` unquantified | `STATE.md:21` |
| standard dominance refuted unconditionally (166 refuters) | **`FP✗`** — ⚠️ **read from `mg-8b64`, never re-measured, here or anywhere** | row 3b(a) |
| **node `B` is unconsumed by any live route** | ⚠️ **documentary, not mathematical** | `mg-05ec` §4.4, `STATE.md:78` — **not** a proof that no BK-mediated route to L1b exists |
| *"no consumer of a BK-gap lower bound exists"* | **not a mathematical kind at all** — a corpus search | `mg-145f` §5, re-measured in part at `mg-05ec` §4.3 |

**The weakest kinds in the set §0 aggregates are the last two rows.** They are `mg-05ec`'s own two
weakest legs, carried forward unlaundered, and they are the ones to attack.

---

## 7. WHAT THIS DOCUMENT DOES NOT DO, and where it can be wrong

1. **It proves nothing and measures nothing.** No script was run, no eigenvalue computed, no row
   re-audited. Every mathematical claim is a citation.
2. **The six-step quote is at second hand** (§2). If `mg-9461` mis-transcribed it, §2's *"Port"*
   reading — the sharpest single observation here — is wrong at the word level. It would not disturb
   §2(a)'s substance, which `STATE.md:82–84` states independently: the reduction consumes rows 5 and
   7 and nothing else.
3. **The mapping table is a reading, not a derivation.** It aligns `STATE.md`'s diagram, the source's
   steps, and the ledger's rows. Two of those three are documents this document did not verify
   against their own sources. Where the alignment is contestable it is at `C → D`, which the diagram
   labels with rows 5 and 10 while the source's Step 3 is row 9 — §3 treats that as *the eigenvector
   half of Step 3 being dead*, and a reader could instead treat it as the diagram having dropped a
   row. **Both readings agree that the live rendering of Step 3 is its prefix clause**, which is all
   §3 uses it for.
4. **It takes `mg-05ec`'s verdict as input and does not re-test it.** If that verdict is wrong, this
   document is wrong in the same direction.
5. **It does not say the spectral work was wasted**, and neither did its parent. The spectral framing
   produced Theorem E, row 3a's dictionary, row 1's characterisation, Buser, and — through `mg-210d`
   — the master bound that is the reason the wall has a clean combinatorial form at all.
6. **`STATE.md` carries no pointer to this document.** Adding one is a ledger edit against a
   size-ratcheted file and is outside this item's scope; it is reachable from
   [`docs/CONCEPTS.md`](CONCEPTS.md) §4, which `STATE.md` does point at. **Flagged for
   `pm-onethird`, not done here.**

---

## 8. Sources

- [`STATE.md`](../STATE.md) at `3ed1700` — the ledger, the diagram (`:63–78`), the node-`B` rider
  (`:78`), the machinery paragraph (`:82–91`), rows 1–11, § *The single lemma to prove* (`:134–145`),
  § *Where the threads converge* (`:186–205`).
- [`docs/OneThird-Spectra-StockTake-mg-05ec.md`](OneThird-Spectra-StockTake-mg-05ec.md) — the parent
  verdict; §4.4 is the node-`B` observation and §5 the framing verdict.
- [`docs/CONCEPTS.md`](CONCEPTS.md) §4 — the same bridge as a mental model rather than as a chain.
- [`docs/OneThird-ChainSelection-mg-9461.md`](OneThird-ChainSelection-mg-9461.md) §1.1 — the six
  steps, quoted.
- [`docs/OneThird-Direct-Prefix-Route-mg-2de0-Audit.md`](OneThird-Direct-Prefix-Route-mg-2de0-Audit.md)
  — the non-spectral prefix route, its repair, and the `2/3` against `ε_leak ≈ 0.20`.
- [`docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md`](OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md)
  Claim 3.1 and [`docs/OneThird-PairBias-EpsSup-mg-832f-IndependentAudit.md`](OneThird-PairBias-EpsSup-mg-832f-IndependentAudit.md)
  Correction 2 — the closure of the pair-marginal route, and its `η`.
- [`docs/OneThird-PairBias-Independence-mg-345e.md`](OneThird-PairBias-Independence-mg-345e.md) —
  `ε_sup` is L4-independent.
- Ticket bodies `mg-3af8`, `mg-c59e`, `mg-602d`, `mg-05ec`.
