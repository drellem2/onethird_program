# Gate on the unified-framework question: what the representation-theoretic negative says, and whether the quotient lattice is `S_n`-preserved

**Work item:** mg-8fd1. **Date:** 2026-07-30. **Computation:** permitted, used, committed
(`code/unified_gate_8fd1/`, 2 min 50 s total).

**This document is not the unified-framework survey.** It is the two checks that determine what that
survey's question *is*. Both were cheap and both returned a definite answer. The survey is the next
ticket and its scope is set by §3 below.

The framing being gated is Daniel's (2026-07-30 11:15Z): the lattice indexing the eigenvalues of the
face-driven walks is the lattice of **poset quotients** of `P` — the acyclic-cut condition is
exactly the condition for the quotient to exist — so that partitions-as-set-quotients and
faces-as-poset-quotients might be two instances of **one mechanism**, with a graded category,
dynamics and representations *"very similar to `S_n`"*.

**Answers in one line each.**

* **L1 — it rules out ONE ROUTE, not the leg.** Proposition N2 is a statement about the *ambient*
  `S_n`-action on *all* ordered partitions of a given shape. It proves that the `P`-compatible ones
  never span an `S_n`-submodule off the antichain. It says nothing about any other group or algebra
  — and the same document's §9 supplies a representation-theoretic mechanism that *does* work, whose
  index set is exactly Daniel's poset quotients. **But it bites on one wording:** the similarity to
  `S_n` cannot be an `S_n`-module structure, at any `n`, for any non-antichain.
* **L2 — WORLD ONE, with the ticket's own description of the degenerate ends corrected in two
  places.** The class of posets whose quotient lattice is `S_n`-stable is **strictly larger than
  antichains** — it is `2(n−1)` isomorphism classes, antichains and *stars* — but **chains are not in
  it** (for `n ≥ 3`), and **every member has quotient lattice equal to the full partition lattice
  `Π_n`**. Stability happens exactly where the quotient lattice degenerates. There is no poset whose
  quotient lattice is a *proper* `S_n`-stable sublattice. So the honest framing is **one shape, many
  symmetry groups** — and this is not a refutation of Daniel's idea, it is a change of its subject.

---

## §1 — L1: what the audited negative actually says

**Source:** `docs/OneThird-Hodge-Side-Leverage.md` §8, *"Negative: representation theory does not
descend"*, lines 691–723; ledger rows **N2** and **N2′** (lines 1019–1020); audited under mg-86a3
(`docs/OneThird-Hodge-Side-Leverage-IndependentAudit.md`, rows at lines 75, 475, 500–501 — *"proof
checked line by line"*, no finding against it).

### 1.1 The statement, quoted

> ### Proposition N2 — PROVEN
> Let `α` be a composition of `n` with at least two parts. `S_n` acts transitively on the set of
> **all** ordered partitions of shape `α` (that set is `S_n/S_α`, whose span is
> `Ind_{S_α}^{S_n}1`). The subset of `P`-compatible ones is
> * **never empty** — cut any linear extension into consecutive blocks of sizes `α_i`; and
> * **proper whenever `P` has a relation** — if `a <_P b`, place `b` in an earlier block than `a`.
>
> A subset of a transitive `G`-set spans a `G`-submodule only if it is empty or everything.
> Therefore for **every non-antichain** the span of the shape-`α` faces is **not** an
> `S_n`-submodule, the isotypic decomposition of the Young module does not induce a decomposition
> of the face space, and a fortiori cannot block-diagonalise `L^rel`, `L^abs` or `Δ_AT`. ∎

and, immediately after it, the second half:

> **And where the symmetry *is* present, it still does not diagonalise.** For the antichain
> `L(P) = S_n` and the full `S_n`-action is available — but `Σ_i s_i` is **not central** in `C[S_n]`
> for `n ≥ 3`, since `{s_1,…,s_{n−1}}` has `n−1` elements while the conjugacy class of transpositions
> has `\binom{n}{2}`. Characters therefore do not give the spectrum of `Δ_AT` even in the fully
> symmetric case — which is the historical reason the antichain gap needed Aldous' conjecture and its
> Caputo–Liggett–Richthammer proof rather than a character computation. So candidate 3 of the ticket
> fails twice: the symmetry is absent off the antichain, and inert on it.

and the residue it explicitly leaves standing:

> The one thing representation theory does give is eigenvalue interlacing: `Δ_amb = (n−1)I − A` is a
> compression of the ambient `Σ_i(1−s_i)`, so its spectrum lies in the ambient range `[0, 2(n−1)]`.
> That is true and says nothing about `λ₂`.

The ledger's own scope line for N2 (line 1019): *"all finite posets, all `α` with `≥ 2` parts;
checked on all posets `n ≤ 5` (exactly 1 exception per `n`, the antichain)"*. N2′ (line 1020): *"all
`n ≥ 3`"*.

### 1.2 What it establishes, with its quantifiers

**Universally quantified over:** all finite posets `P`; all compositions `α` of `n` with at least two
parts. **Not** an `n ≤ 5` statement — the `n ≤ 5` sweep is a check, not the evidence.

**Hypothesis actually used:** that `OP_α` (all ordered partitions of shape `α`) is a *transitive*
`S_n`-set, and that the `P`-compatible subset `F_α(P) ⊆ OP_α` is nonempty and proper.

**Conclusion actually reached:** `span F_α(P)` is not an `S_n`-submodule of `Ind_{S_α}^{S_n}1`;
therefore the Young module's isotypic decomposition does not restrict to the face space, and cannot
block-diagonalise `L^rel`, `L^abs`, `Δ_AT`.

**The mechanism is a one-line orbit argument.** No property of `P` beyond *"has at least one
relation"* enters, and no property of the operators enters at all. The auditor's own restatement of
the whole section (line 75) is: *"the AT graph of a non-antichain has no `S_n` symmetry" — "No —
obvious"* — filed as **correctly a NEGATIVE**, with *"the Young-module dress adds nothing but costs
nothing."*

### 1.3 The deliverable: one route, or the leg?

**It rules out one route.** Precisely: the route *"take the ambient `S_n`-action on ordered
partitions, decompose the Young permutation module into isotypics, and read off a block-diagonalisation
of the face-space operators."* That route is dead for every non-antichain and every `n`, and N2′
kills it on the antichain too by a different mechanism. Two routes, both `S_n`-based, both dead.

**It does not touch the representation-theory leg of Daniel's proposal, for a reason internal to the
same document.** N2's quantifier is over subsets of a *transitive `S_n`-set*. It is silent about:

* representations of `Aut(P)`, or of any group other than the ambient `S_n`;
* representations of any **algebra** attached to `P`;
* in particular, the **face semigroup algebra** — and §9 of the very same document establishes that
  this one works. `F(P)` is a left regular band whose support lattice is exactly the acyclic
  partitions, and Brown's theorem diagonalises every face-driven walk with
  `λ_X = Σ_{supp(y) ≤ X} w(y)` indexed by those acyclic partitions, multiplicities fixed by
  `Σ_{Y ≥ X} m_Y = ∏_{B∈X}|L(P|_B)|` **independent of the weights**. That index set *is* Daniel's
  lattice of poset quotients.

So the document contains, side by side, a dead `S_n` route and a live semigroup-representation route
whose index set is the object Daniel identified. **N2 is not an obstruction to the framework; it is a
statement about which algebra the framework has to be built on.**

**Where N2 does bite, stated without softening.** If *"representations very similar to `S_n`"* is
read as *"the face space carries an `S_n`-module structure whose isotypic pieces do the work"*, that
is **false for every non-antichain, proven, all `n`**. And N2′ removes the fallback of treating the
antichain as the solved end by `S_n` character theory: even there, `Σ_i s_i` is not central and
characters do not diagonalise `Δ_AT`.

**That second point cuts in Daniel's favour and is worth stating separately.** The antichain end of
the proposed unification is *not* handled by `S_n` representation theory either. What handles it is
the Bidigare–Hanlon–Rockmore / Brown–Diaconis braid-arrangement theory — the same left-regular-band
mechanism, specialised. The repo already carries this as a verified identity of families (mg-66a6:
*"on an antichain the family is the BHR/Brown-Diaconis braid hyperplane-walk family as an IDENTITY OF
FAMILIES"*). So the two ends Daniel wants to unify are **already** handled by one mechanism — the
semigroup one — and `S_n` representation theory is not that mechanism at either end.

**One scope note, so this is not read as wider than it is.** §9.4 of the source restricts what the
semigroup technique buys *for `λ₂(Δ_AT)`*: it reaches `Δ_AT` only where `Δ_AT` is already free. That
limit is about the bridge quantity of a different work item. It does not bear on Daniel's question,
which is about the index lattice and the mechanism, not about `Δ_AT`.

---

## §2 — L2: is the quotient lattice preserved by `S_n` off antichains and chains?

### 2.1 Method

`code/unified_gate_8fd1/quotient_symmetry.py` and `characterise.py`, written from scratch — no import
from `code/hodge_leverage/`. The acyclicity test is a bitmask transitive closure with a self-loop
check, against `lrb.py`'s DFS three-colouring; the poset enumeration, the partition enumeration and
the group action are all independent.

For a poset `P` on `[n]`, `AC(P) = { π ∈ Π_n : P/π has no directed cycle among distinct blocks }` —
the partitions for which the quotient exists. Posets are enumerated by taking every transitively
closed subset of `{(i,j) : i<j}` (so `0<1<⋯<n−1` is a linear extension, which every poset admits) and
canonicalising under `S_n`; class counts **1, 2, 5, 16, 63, 318** for `n = 1…6` reproduce the known
numbers of unlabelled posets. For each class we compute the full subgroup

`G(P) = { σ ∈ S_n : σ·AC(P) = AC(P) }`  (equivalently `{σ : AC(σP) = AC(P)}`),

by brute force over all of `S_n` — `|S_6| = 720` against `B_6 = 203` partitions, no sampling.

### 2.2 Population

| `n` | iso classes | `G(P) = S_n` | fraction |
|---|---|---|---|
| 1 | 1 | 1 | 1.0000 |
| 2 | 2 | 2 | 1.0000 |
| 3 | 5 | **4** | 0.8000 |
| 4 | 16 | **6** | 0.3750 |
| 5 | 63 | **8** | 0.1270 |
| 6 | 318 | **10** | 0.0314 |

The stable count is `2(n−1)` at every `n ≥ 2`, and the members are, at every `n`:

* the **antichain**; and
* the **stars**: one element below a nonempty set of pairwise-incomparable elements (`n−1` classes,
  by the size of the set), or one element above such a set (`n−2` further classes — size 1 is the
  same poset both ways), each with the remaining elements isolated.

**In every one of these cases `|AC(P)| = |Π_n|`: the quotient lattice is the *full* partition
lattice.** (n=6: `203 of 203` on all ten.)

### 2.3 Two corrections to the ticket's description of the degenerate ends

**Chains are not `S_n`-stable, and their quotient lattice is not trivial.** Measured:

| | `|AC|` | `|G(P)|` | `S_n`-stable |
|---|---|---|---|---|
| chain `C_3` | 4 of 5 | 2 | **No** |
| chain `C_4` | 8 of 15 | 2 | **No** |
| chain `C_5` | 16 of 52 | 2 | **No** |
| chain `C_6` | 32 of 203 | 2 | **No** |

`AC(C_n)` is the set of partitions into **consecutive intervals**, size `2^{n−1}` — the Boolean
lattice, not the trivial one — and `G(C_n) = {id, order-reversal}` for `n ≥ 3`. Chains are a
degenerate end for `|AC|` — they are the **unique** minimiser of `|AC(P)|` at each of `n = 3,4,5,6` —
but they are not a degenerate end for the symmetry, and they are not stable. Nothing downstream in the repo depends on
the ticket's phrasing here; the correction is recorded so the next ticket does not inherit it.

**Antichains are not the only stable posets.** The stars are stable too, and they are not antichains.
But — see 2.4 — they carry no new lattice.

### 2.4 The characterisation, proven for all `n`

> **Theorem (mg-8fd1).** For a finite poset `P` on `[n]`, the following are equivalent.
> 1. `AC(P)` is stable under the `S_n` relabelling action.
> 2. `AC(P) = Π_n` — every set partition is acyclic.
> 3. No two strict relations `x < y`, `u < v` of `P` have both `x ≠ u` and `y ≠ v`.
> 4. `P` is an antichain, or its strict relations are exactly `{(a,s) : s ∈ S}` for a single `a` and
>    nonempty `S`, or exactly `{(s,a) : s ∈ S}`.

*Proof.* **(2)⇒(1)** is immediate. **(3)⇒(2):** if every relation has the same bottom `a` (the
shared-top case is dual; `≤ 1` relation satisfies both), then in any quotient every arrow leaves the
block containing `a`, since an arrow `B → B'` needs `x ∈ B` with `x <_P y`, forcing `x = a`. A
directed cycle would need an arrow whose head is that block and whose tail is another block, which
does not exist. **(1)⇒(3)**, in two steps. *Step 1: (1) forbids a 3-chain.* If `x < u < y` then
`{x,y}` + singletons has the 2-cycle `{x,y} → {u} → {x,y}`, while `{x,u}` + singletons is acyclic
(every arrow leaves it); the two have the same shape `(2,1^{n−2})`, hence lie in one `S_n`-orbit, so
`AC(P)` is not a union of orbits. *Step 2.* Assume (1), so no 3-chain, and suppose (3) fails via
`x<y`, `u<v` with `x ≠ u`, `y ≠ v`. Then `y ≠ u` (else `x<y=u<v` is a 3-chain) and `x ≠ v` (else
`u<v=x<y` is), so `x,y,u,v` are four distinct elements. Now `{x,v}|{y,u}` + singletons has the
2-cycle `{x,v} → {y,u}` (from `x<y`) and `{y,u} → {x,v}` (from `u<v`), so it is not acyclic — while
`{x,u}|{y,v}` + singletons **is** acyclic: any arrow into `{x,u}` or any path returning to it would
supply one of `y<z<x`, `y<z<u`, `v<z<x`, `v<z<u`, `x<z<u`, `u<z<x`, `y<z<v`, `v<z<y` or a direct
`y<x`, `y<u`, `v<x`, `v<u`, and each of these combines with `x<y` or `u<v` to give a 3-chain (or an
impossibility). The two partitions share the shape `(2,2,1^{n−4})`, so again `AC(P)` is not a union
of orbits. **(3)⇔(4):** if `P` has two distinct relations `r₁, r₂` then (3) forces them to share a
bottom or a top, and not both (they would be equal); if `r₁ = (a,y₁)`, `r₂ = (a,y₂)` with `y₁ ≠ y₂`,
then any third relation must share an end with each, and cannot have top `y₁` and top `y₂`, so it has
bottom `a`. Hence all relations share one end. Such a relation set is transitively closed, and
counting gives `1 + (n−1) + (n−2) = 2(n−1)` classes. ∎

**Evidence.** The equivalence (1)⇔(2)⇔(3) is checked **exhaustively on every isomorphism class at
`n ≤ 6`** — 405 classes, zero disagreements — and on 400 random posets at each of `n = 7, 8, 9`,
where no exhaustive evidence exists: **0 disagreements** at each, with stability tested on the
adjacent transpositions (which generate `S_n`, so the condition tested is the full one, not a sample
of it). The random sweep exercises **both** directions rather than only the negative — 168 / 151 /
123 of the 400 came out stable at `n = 7 / 8 / 9`, and the theorem predicted every one of them.
Note that *"no 3-chain"* is strictly weaker than the three
equivalent conditions and is correctly reported as such (`n = 6`: 56 classes of height `≤ 2` against
10 stable), so the intermediate step of the proof is not being mistaken for the conclusion.

### 2.5 Which world this puts us in

**World one: "one shape, many symmetry groups."** Stated exactly:

The set of posets whose quotient lattice is `S_n`-stable is nonempty, is larger than the ticket
anticipated, and **contributes no lattice that the antichain does not already contribute** — by the
Theorem, `S_n`-stability holds *if and only if* `AC(P) = Π_n`. There is **no** poset, at any `n`,
whose quotient lattice is a proper `S_n`-stable sublattice of `Π_n`. So the hoped-for "natural home
for the unification" — a non-degenerate class where the full symmetric group acts — **does not
exist**, and the reason is not a coverage gap: it is a theorem.

Off that class the symmetry group is genuinely different in each case, and it is a **new invariant**,
not a repackaging of `Aut(P)`:

* `|G(P)|` over the 318 classes at `n = 6`: **1**(×72), **2**(×123), **4**(×52), **6**(×12),
  **8**(×13), **12**(×24), **16**(×6), **24**(×2), **48**(×3), **72**(×1), **720**(×10).
* `G(P)` always contains `D(P) = {σ : σP ∈ {P, P^op}}` — acyclicity is invariant under reversing all
  arrows, so every self-duality of `P` preserves `AC(P)` — but it is **strictly larger** than `D(P)`
  on **24 of 63** classes at `n = 5` and **55 of 318** at `n = 6`.
* The reason is that `P ↦ AC(P)` is far from injective: at `n = 5`, **4231** labelled posets give only
  **1316** distinct quotient lattices, the largest fibre containing **131** posets (precisely the
  antichain and all labelled stars, all with `AC = Π_5`). **The quotient lattice does not remember the
  poset.**

**This is not a refutation of Daniel's idea and must not be reported as one.** Both instances are
real, the analogy is real, and §1 shows the mechanism that covers both ends is real and already in the
repo. What L2 settles is that the mechanism is *not* "one group acting on one family" — it is one
*construction* (`P ↦ AC(P)` and the left regular band over it) whose symmetry group varies with the
input. That is a different research programme from the one "unification" suggests, and it is the one
the next ticket should survey.

### 2.6 One caveat on the word "lattice", found on the way

`AC(P)` **is** a lattice under refinement (verified: every pair has a unique minimal common
coarsening inside `AC(P)`, on all 86 classes at `2 ≤ n ≤ 5`), as it must be, being an LRB support lattice.
But it is **not a sublattice of `Π_n`**: it is not closed under the `Π_n`-join, on **7 of 16** classes
at `n = 4` and **49 of 63** at `n = 5`. The source's own named witness is exactly a join failure and
not only a refinement failure — for `P = {a<c, b<d}`, the partitions `{a,d}|{b}|{c}` and
`{a}|{b,c}|{d}` are both acyclic and their `Π_4`-join is `{a,d}|{b,c}`, which is not:

```
 the document's own named witness, P = {a<c, b<d} at n=4:
   03|1|2 acyclic=True ; 0|12|3 acyclic=True ; join = 03|12 acyclic=False
```

The source (§9.1) records that acyclic partitions are *"NOT closed under refinement"* with this same
witness; that they also fail the **join** appears to be unrecorded, and it matters here, because
"partitions-as-set-quotients and faces-as-poset-quotients are two instances of one mechanism" is at
its most natural if `AC(P)` embeds in `Π_n` as a sublattice. It does not. It is a lattice in its own
right whose join disagrees with `Π_n`'s. Flagged, not pursued — this is a gate, and the observation
belongs to whoever takes the survey.

---

## §3 — What this sets for the next ticket

Recorded as the consequence of the two answers, not as a plan I am authorised to execute.

1. **The survey question is not "is there one mechanism".** §1 says there already is a candidate one
   — the left regular band and its support lattice — covering both ends, with the classical braid
   case as a verified specialisation. The survey question is what is known about **that** family
   (LRB / hyperplane-walk / Saliola-style decompositions indexed by a support lattice) and whether
   the poset-quotient instance is known in it.
2. **It is not a question about `S_n` representation theory.** L1's route is closed by a theorem at
   both ends. Any literature search framed around Young modules or isotypic decompositions of the
   face space will return nothing usable, and knowing that in advance is what this gate bought.
3. **"One shape, many symmetry groups" is the frame.** The object that varies across `Pos_n` is
   `G(P)`, and §2.5 shows it is a new invariant rather than `Aut(P)` in disguise. Whether it has been
   studied is a fair survey question.
4. **Not started here, deliberately:** no literature survey, no categorical formalism, no touching of
   the conjecture pricing in `docs/roadmap.md`, and nothing about "other set-represented categories"
   — which L2 makes premature rather than merely out of scope, since the `Pos_n` instance turns out
   not to have the uniform symmetry that would have motivated generalising.

## §4 — Reproduce

```
cd code/unified_gate_8fd1
python3 quotient_symmetry.py 6     # 34 s       -> out_quotient_symmetry.txt
python3 characterise.py            # 2 min 16 s -> out_characterise.txt
```

Committed outputs: `out_quotient_symmetry.txt`, `out_characterise.txt`.

## §5 — Claim ledger for this document

| # | claim | status | scope |
|---|---|---|---|
| **Q1** | N2 rules out the ambient-`S_n`/Young-module route, not representation theory as such | **READING OF A PROVEN SOURCE** | quoted in full at §1.1; the source is audited under mg-86a3 with no finding against it |
| **Q2** | the similarity to `S_n` cannot be an `S_n`-module structure, for any non-antichain | **PROVEN** (the source's N2) | all finite posets, all `α` with `≥2` parts |
| **Q3** | `S_n`-stability of `AC(P)` ⟺ `AC(P) = Π_n` ⟺ every two relations share an end ⟺ antichain-or-star | **PROVEN** (§2.4) | all finite posets, all `n`; exhaustive at `n ≤ 6` (405 classes, 0 disagreements); random at `n = 7,8,9` (400 each, 0 disagreements) |
| **Q4** | the stable classes number `2(n−1)` for `n ≥ 2` | **PROVEN** (corollary of Q3) | all `n ≥ 2`; measured 2, 4, 6, 8, 10 at `n = 2…6` |
| **Q5** | chains are not `S_n`-stable for `n ≥ 3`, and `|AC(C_n)| = 2^{n−1}` | **PROVEN + MEASURED** | `|G(C_n)| = 2` measured at `n ≤ 6`; the interval description is elementary |
| **Q6** | `G(P)` is strictly larger than `{σ : σP ∈ {P,P^op}}` on some posets | **MEASURED** | 24 of 63 at `n = 5`, 55 of 318 at `n = 6`; not proven in general |
| **Q7** | `AC(P)` is a lattice under refinement but not a sublattice of `Π_n` | **MEASURED** (lattice: `n ≤ 5`; join failure: `n = 4,5`) | the lattice half is a consequence of the cited LRB theorem; the join failure is exhibited by explicit witness |
| **NOT CLAIMED** | anything about whether the LRB/support-lattice family is the right home — that is the survey. Anything about other set-represented categories. Anything about `λ₂`, `Δ_AT`, or the pricing. That `G(P)` has been or has not been studied in the literature. | | |
