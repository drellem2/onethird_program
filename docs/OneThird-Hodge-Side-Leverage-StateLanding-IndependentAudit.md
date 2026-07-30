# Independent audit of mg-a806 — the mg-86a3 landing (STATE.md + the mg-a3d4 deliverable)

**Work item:** mg-d39d (pre-filed audit of mg-a806). **Target:** the four commits
`f6756c0`, `16bee79`, `5b63037`, `0160cbf` — i.e. `8fc5111..0160cbf`, touching `STATE.md`,
`docs/OneThird-Hodge-Side-Leverage.md`, `code/hodge_leverage/{run_sweep.py,run_lrb.py,run_all.sh}`
and the two regenerated artifacts.

**Audit instrument:** `code/hodge_leverage_audit_d39d/`, sharing **no code** with
`code/hodge_leverage/` or with `code/hodge_leverage_audit_86a3/` — the poset enumeration, the
compatible face complex, the links, the induced weights, the eigenvalue routine, the linear
extensions, the semigroup action and the Brown-walk witness are all rebuilt from their definitions.
The rebuild reproduces A000112 (`1 1 2 5 16 63 318`) and the deliverable's own §9.4 counts
(`0/2/11/55` NOT, `1/2/4/7` undecided, 1 vacuous per `n`) before anything else is asserted.

---

## §0 — Verdict

> ## OVERSTATED · **1 BROKEN** · and the broken one is a *new* row this landing added
>
> **Every repair mg-a806 was asked to land, it landed, and landed correctly.** F1's central
> correction — ledger row **B6 is FALSIFIED as a universal, not coverage-gapped** — is right, and I
> reproduced its evidence independently, including the `|L(P)| = 8` positive at `n = 6`. The
> replacement is genuinely stronger content. Theorem G stands. All four committed artifacts
> regenerate, three of them byte-identically, and the fourth differs only in the two wall-clock lines
> that `run_all.sh` now says are the only things that can differ.
>
> **But this is the first landing in the arc with BROKEN mathematics in it, and it is in a row the
> ticket did not ask for.** Ledger row **G″** — *"`γ_i ≥ 1/2` for every finite poset having a
> dimension-`i` face one of whose blocks induces an antichain of size `≥ 3`"*, labelled **PROVEN**
> and described as *"free from **G** + Theorem **L**"* — is **FALSE**. It fails on **55 (poset,
> level) pairs at `n ≤ 6`**, the smallest at `n = 5`; the per-face reading its own proof sentence
> argues fails on **3901 of 7989** faces. It is false for a structural reason: **Theorem L makes the
> link a JOIN, and a join SUPPRESSES `λ₂`** — an eigenfunction of a factor survives into the join
> scaled by `p/(p+q+1) < 1`. Theorem G escapes this only because it picks the face whose *other*
> blocks are all singletons, which contributes no join factor. **The strengthening was not free; it
> was not available at all.**
>
> **And the repaired clause repeats the defect it repairs, one generation on.** The old B6 was struck
> for a scope threshold read off its tested population and protected by a hedge. Its replacement —
> *"the semigroup technique reaches `Δ_AT` only where `Δ_AT` is already free"* — is a **universal over
> all finite posets** carried by `n ≤ 6` plus `V_{k ≤ 4}`. It appears at **thirteen sites** across the
> two documents and the artifact; **exactly one of the thirteen carries the qualifier**. The hedge did
> not go away: it moved from the prose into ledger row B6′'s *label* column, and §9.4 drops it between
> two adjacent sentences under the word *"Equivalently"*. The same ledger's next row, **B6″**, says
> the question the slogan answers is **NOT CLAIMED — open**.
>
> **Two claims are stated as computations when they are one-line theorems, and both carry the MAJOR
> finding.** *"The **infinite** family `V_k` … is positive for every `k` **tested**"* rests on `k ≤ 4`
> — four data points — while §9.4 concludes *"the positive class is **unbounded** in `|L(P)|`"*.
> There is a witness uniform in `k` (supplied below, verified exactly to `k = 8`, `|L(P)| = 256`), so
> the statement is a **theorem** and the label under-claims while the prose over-claims. Likewise
> *"including all antichains `n ≥ 3`"* — retained verbatim inside the row being repaired — is a
> universal in `n` under a `PROVEN-by-computation (n ≤ 5)` label; it is a two-line theorem (supplied,
> and `A_6` verified directly).
>
> **A proof was landed as the closing of a CONTROL gap** — §10's new *"the one control gap this
> document named itself is now closed, by the auditor"* — in the same commit that lands
> `STATE.md` Appendix A's **PROVING A PROPERTY AND TESTING FOR IT ARE DIFFERENT OPERATIONS**.
> `audit_theoremG.py` contains no mutation; it is a replication, and §13 named a *replication* gap,
> not a control gap.
>
> **A RED here is not a reversal of the landing.** Nothing in the routing changes, `A(P)` stays
> unbuilt, the pricing stays carried by proofs, and the F1 correction stays. What must change is four
> rows and one paragraph.
>
> **Contribution handed back: `n = 6` is now COMPLETE.** mg-86a3 skipped 214 of the 318 posets at
> `n = 6` (`|L(P)| > 14`) and B6′'s label column says so. The §9.4 sufficient test is cheap enough to
> close them: run on all 318, it gives **NOT = 305, vacuous = 1, undecided = 12**, and the 12 are
> **exactly** mg-86a3's 12 positives. So the untested region contains no counterexample, and B6′'s
> negative half upgrades from *"`n ≤ 6` at `|L(P)| ≤ 14`"* to *"`n ≤ 6` complete"*.

**Findings, in severity order.**

| # | severity | finding |
|---|---|---|
| **A1** | **BROKEN** | ledger row **G″** is FALSE — 55 (poset, level) counterexamples at `n ≤ 6`, smallest at `n = 5`; joins suppress `λ₂` and the row ignores the join |
| **A2** | **MAJOR** | the replacement scope clause is an unhedged universal at 12 of 13 sites; the hedge relocated into B6′'s label column; B6″ calls the same question open |
| **A3** | **MAJOR** | *"infinite" / "unbounded"* for `V_k` carried by `k ≤ 4`, and it is a one-line theorem — over-claim and under-claim on the same object |
| **A4** | MODERATE | a **rebuild** recorded as closing a **control** gap (§10), in the commit that lands the rule against exactly that conflation |
| **A5** | MODERATE | §14 asserts the `STATE.md` row *"carries the same clauses"*; it carries at least five it does not, one of them A4 |
| **A6** | MINOR | *"including all antichains `n ≥ 3`"* — a universal in `n` retained inside the repaired row, under an `n ≤ 5` computational label; it is a theorem |
| **A7** | MINOR | the floor paragraph says mg-fcf1 is *"merged and not yet landed here"* in the commit that lands mg-fcf1's Appendix A rule **here** |
| **A8** | MINOR | three wording items: §10's *"all five mutations"* against its own six-row table and its own *"all six mutations"*; *"already diagonal"* for the hypercube Laplacian (it is already **diagonalised**, §9.4 says it correctly and the other sites do not); row G′ extended to `A_9` on a **per-link** computation while `γ_i` is a **per-level max** |

---

## §1 — Method, and what independence means here

Nothing in `code/hodge_leverage/` or `code/hodge_leverage_audit_86a3/` is imported by
`code/hodge_leverage_audit_d39d/`. Specifically rebuilt: poset enumeration up to isomorphism (by
adding one maximal element at a time and canonicalising by brute force over `S_n`), order ideals,
the order complex of the proper part of `J(P)`, facets as maximal chains, links by brute force from
the facet list, the induced measure `w(τ) = #{facets ⊇ τ}`, a cyclic Jacobi eigensolver, linear
extensions, the adjacent-transposition adjacency, compatible ordered partitions, the refinement
action `x·c`, and exact-rational Brown witnesses.

Cross-checks passed **before** any finding was formed:

| check | result |
|---|---|
| isomorphism classes, `n = 0..6` | `1 1 2 5 16 63 318` — A000112 |
| §9.4 sufficient test, `n = 2..5` | NOT `0/2/11/55`, undecided `1/2/4/7`, vacuous 1 per `n` — the committed `lrb_output.txt` §5 exactly |
| the `n = 6` positives | the same 12 posets, same `\|L(P)\|` multiset `{2×5, 4×6, 8×1}`, as `out_n6_brown.txt` |
| `γ_0` on the counterexample posets | my rebuild and `local_to_global.gammas` agree to `0.25` exactly |
| all four committed outputs regenerated | `theorems_output.txt`, `lrb_output.txt`, `controls_output.txt` **byte-identical**; `sweep_output.txt` differs in exactly the two `[NNN.Ns]` lines |

That last row is worth stating as credit before anything else: **mg-a806's narrowing of `run_all.sh`'s
byte-for-byte claim is exactly right, and exactly as wide as it needs to be.** (Amusingly, my
regeneration returned `[80.9s]` for `n = 6` — the value mg-a806 *replaced* — which is precisely why
the caveat was needed.)

---

## §2 — A1 (**BROKEN**): ledger row G″ is false

**The row, as landed** (`docs/OneThird-Hodge-Side-Leverage.md:881`):

> | **G″** | `γ_i ≥ 1/2` for **every finite poset** having a dimension-`i` face one of whose blocks
> induces an antichain of size `≥ 3` | **PROVEN** (§6; free from **G** + Theorem **L**) | all finite
> posets. Added in repair of mg-86a3's step-4b finding that **G is weaker than its own proof** …

**and its prose site** (`:462–466`):

> **Step 4b, from the same audit and adopted here:** Theorem G is *weaker than its own proof*, because
> the proof uses only that some block induces an antichain of size `≥ 3`. The immediate strengthening,
> free from G plus Theorem L, is **`γ_i ≥ 1/2` for every finite poset having a dimension-`i` face one
> of whose blocks induces an antichain of size `≥ 3`** …

### Why it is false

Theorem G (`:417–439`) fixes `i`, sets `m = n−i−1 ≥ 3`, and takes **the face `σ` whose blocks are one
block of size `m` and `i+1` singletons**. Singleton blocks contribute nothing to the join, so
`link(σ) ≅ F(A_m)` *on the nose*, and the eigenfunction argument applies to `F(A_m)` directly.

Drop the singleton requirement and Theorem L gives a genuine **join**, `F(A_m) * Y`. For the walk on
the 1-skeleton of a join of a `p`-dimensional `X` and a `q`-dimensional `Y` with product weights, an
eigenfunction `f` of `X`'s walk with `⟨f, π_X⟩ = 0`, extended by `0` on `Y`, satisfies

```
    (P_{X*Y} f)|_X  =  (p /(p+q+1)) · λ · f ,        (P_{X*Y} f)|_Y  =  0 ,
```

because from a vertex of `X` the walk stays in `X` with probability `p/(p+q+1)` and otherwise jumps
to `Y` at its stationary measure, against which `f` integrates to zero. **The join scales the
eigenvalue down by `p/(p+q+1) < 1`.** (The only other new eigenvalue is the cross one, `−1/(p+q+1)`.)
So a `1/2` in a factor becomes strictly less than `1/2` in the join, and `λ₂` of a join is at most the
max over factors, never more.

Concretely, `F(A_3) * F(A_2)` has `p = 1`, `q = 0`, so the hexagon's `1/2` lands at `1/2 · 1/2 = 1/4`.

### The smallest counterexample, checked twice

`P = A_2 ⊕ A_3` (`n = 5`, `{0,1} < {2,3,4}`; `d = n−2 = 3`, so the level range is `−1 ≤ i ≤ 1`).
At `i = 0` the face `σ = ({0,1})` has blocks `{0,1}` (type `A_2`) and `{2,3,4}` (**an antichain of
size 3**), so G″ asserts `γ_0 ≥ 1/2`. Measured:

```
  my rebuild                          gamma_0 = 0.250000
  code/hodge_leverage local_to_global gammas -> {-1: 0.166667, 0: 0.25, 1: 0.5}
```

`γ_0 = 1/4`. G″ is false on this poset, and **the deliverable's own instrument says so.**

### How far it is from true

`code/hodge_leverage_audit_d39d/audit_gpp.py` → `out_gpp.txt`, all 318 + 63 + 16 + 5 + 2 posets,
every level `−1 ≤ i ≤ d−2`:

| reading | population | counterexamples |
|---|---|---|
| **per-face** — *"one block is an antichain of size `≥ 3` ⟹ `λ₂(link σ) ≥ 1/2`"*, which is what §6's sentence argues | 7989 such faces, `n ≤ 6` | **3901** |
| **per-level** — ledger row G″ as written | 754 (poset, level) pairs, `n ≤ 6` | **55** |

Four of the 55 are at `n = 5`: `A_3 ⊕ A_2`, `A_3 ⊕ C_2`, `A_2 ⊕ A_3`, `C_2 ⊕ A_3`, all with
`γ_0 = 0.25`. At `n = 6` the values include `0.333333` and `0.408367`. **Nearly half the faces the
row quantifies over are counterexamples.** This is not a boundary case.

### Sizing it in both directions, which is the part that matters

- **Theorem G is untouched.** Its face has singleton blocks by construction, `m ≥ 3` comes from
  `i ≤ n−4`, and the audit rebuilt it to `A_12`. The `2^{Θ(n)}` loss remains a theorem, the headline
  remains carried, and **nothing in §0, §5, §6's conclusion, M2, `STATE.md` or the routing depends on
  G″.**
- **The blast radius is two lines.** `G″` occurs at exactly two sites in the deliverable
  (`:466`, `:881`) and **nowhere in `STATE.md`**. The row's own last clause — *"Nothing here consumes
  it"* — is accurate, and the discipline of saying so is what keeps this a two-line repair.
- **The motivating example does not even fall under it.** §6's step-4b passage says the deliverable
  *"instead gets `C_a ⊔ C_a` past the same bar separately, via the `P_4` row of Theorem H"* — but
  §5.3 states that `C_a ⊔ C_a` **has no 3-antichain at all**, so G″ would not have covered it under
  any reading. The strengthening was motivated by a case it does not reach.
- **Provenance, stated because it changes who must fix what.** The false sentence is
  **mg-86a3's**, at `docs/OneThird-Hodge-Side-Leverage-IndependentAudit.md:413`, inside its step-4b
  strength-check table. mg-a806's ticket (B1–B6) does not mention it. mg-a806 promoted an auditor's
  aside into a **PROVEN** ledger row without rebuilding it. Both halves are the defect: an audit's
  own product went unaudited, and *"the audit wins where we disagree"* was applied to a sentence
  neither party had checked.

**Recommended repair.** Strike G″, or replace it with the statement that *is* free:

> **G″ (repaired)** — `γ_i ≥ 1/2` for every finite poset having a dimension-`i` face whose blocks are
> one antichain of size `≥ 3` **and singletons otherwise**. PROVEN, by G + L. And record the reason
> the wider form fails: **Theorem L makes links joins, and joins suppress `λ₂` by `p/(p+q+1)`** —
> which is a fact worth having in the ledger in its own right, because it is also why `γ_i` for `A_n`
> is attained at the one-big-block face and nowhere else.

---

## §3 — A2 (**MAJOR**): the replacement clause is an unhedged universal at 12 of 13 sites

The standing target is *"read the affected sites IN SEQUENCE."* Done. The slogan
*"the semigroup technique reaches `Δ_AT` only where `Δ_AT` is already free"* — and its variants —
appear at thirteen places:

| # | site | carries the population qualifier? |
|---|---|---|
| 1 | `docs/…Leverage.md:119–122` (§0 claim 3) | **no** — and it adds *"It buys no bound on the bridge quantity **anywhere**, and that is now **known** rather than untested"* |
| 2 | `:661` (§9.4 heading) | **no** |
| 3 | `:741–743` (§9.4 blockquote, first sentence) | **YES** — *"not otherwise on any poset **tested** with `\|L(P)\| ≥ 5`"* |
| 4 | `:745–746` (§9.4 blockquote, second sentence) | **no** — and it is introduced by *"**Equivalently**, in one sentence"* |
| 5 | `:748` (§9.4, *"That is a better sentence than …"*) | **no** |
| 6 | `:896` (ledger row **B6′**, claim column) | **no** in the claim column; the label column says `n ≤ 5` complete + `n = 6` at `\|L(P)\| ≤ 14` |
| 7 | `:937` (§12, the routing consequence) | **no** |
| 8 | `:1014` (§13 step 4c) | **no** |
| 9 | `:1059` (§14 row) | **no** — capitalised |
| 10 | `STATE.md:135` (the mg-276d GREEN row, extended by `5b63037`) | **no** — *"reaches `Δ_AT` only where `Δ_AT` is already diagonal. So this row's closing suggestion is DISCHARGED, not pending."* |
| 11 | `STATE.md:136` (the new AMBER row) | **no** — *"⭐ … THIS IS THE WORDING TO QUOTE"* |
| 12 | `STATE.md:239` (Appendix A, the mg-86a3 table row) | **no** |
| 13 | `code/hodge_leverage/lrb_output.txt:61–63` (`run_lrb.py:311–314`) | **no** — capitalised |

**One of thirteen.** And site 4 is the sharpest instance available: the blockquote's own two sentences
are separated by the word *"Equivalently"*, and they are **not** equivalent — the second drops
*"tested"*, converting a statement about a finite verified population into a universal over all finite
posets.

**Why that is not pedantry here.** The ledger's very next row says so:

> | **B6″** | a characterisation of the positive class — the evidence is consistent with *"iff the AT
> graph is a hypercube"* | **NOT CLAIMED — open, cheap, and well-posed** | … |

*"Reaches `Δ_AT` only where `Δ_AT` is already free"* **is** a claim about the positive class: it says
every positive is a poset on which `Δ_AT` is already diagonalised. If the characterisation is open,
the slogan is the open conjecture, asserted. `STATE.md:136` runs both in one row, five sentences
apart — *"THE WORDING TO QUOTE"* and then *"the auditor states \[it] as a conjecture and explicitly
does not claim"*.

**The mechanism is the one the same commit just wrote into Appendix A.** mg-86a3's finding about the
old B6 was: *"it survived only inside the hedge 'on the tested population' — the hedge was doing all
the work."* The repair did not remove the hedge's load; it **moved the hedge into the label column of
a ledger row and dropped it from every quotable surface.** `STATE.md:200`'s own new step-4d text says
to *"audit the SCOPE CLAUSES ATTACHED TO NEGATIVES"* because *"a hedge that makes a false universal
survive is doing all the work."* Site 4 is that hedge, one generation on.

**Sizing it in the other direction, because this must not read as a retreat.** The slogan's *content*
is well-supported and my own work strengthens it (§7). What is unsupported is the **quantifier**, and
the fix is one clause, not a retraction:

> **the semigroup technique reaches `Δ_AT` only where `Δ_AT` is already free — verified exhaustively
> for `n ≤ 6` and on the family `V_k` for every `k`, and open beyond that (row B6″).**

That is still stronger than *"undecided below `|L(P)| ≤ 4`"*, still carries §12's routing, and is the
sentence the evidence supports.

---

## §4 — A3 (**MAJOR**): *"infinite" / "unbounded"* is carried by four data points — and it is a theorem

**The sites.** §0 claim 3 (`:116–117`): *"the positive class contains the **infinite** family `V_k`"*.
§9.4 (`:730–731`): *"So the positive class is **unbounded in `|L(P)|`**, and ledger row B6 has
**genuine counterexamples, not a coverage gap**."* Ledger B6 (`:895`): *"the **infinite** family `V_k`
… is positive for every `k` **tested**"*. Ledger B6′ (`:896`) claim column: *"a Brown walk on an
infinite family (`|L(P)| = 2^k`, unbounded)"*; label column: *"**PROVEN** for the `V_k` half … **the
hypercube identification is by inspection; positivity verified by exact LP for `k ≤ 4`**"*.
`STATE.md:136`: *"the infinite family `V_k` … `|L(P)| = 2^k` unbounded — is positive for every `k`
tested"*. `lrb_output.txt:57–58`: *"the family `V_k` … is positive for every `k` tested"*.

**The evidence is `out_brown_family.txt`: `k = 1, 2, 3, 4`.** Four instances, `|L(P)| ≤ 16`. A row
whose claim column says *"infinite … unbounded"* and whose label column says *"`k ≤ 4`"* is
self-contradicting, and "unbounded in `|L(P)|`" cannot be read off a set with maximum 16. This is the
**instance-read-as-law** shape, and it is carrying the MAJOR finding: *"genuine counterexamples, an
infinite family of them, not a coverage gap."*

**And it is a one-line theorem, so the repair is an upgrade.** `V_k = ` ordinal sum of `k` two-element
antichains, `n = 2k`, AT graph `Q_k`, degree `k`. Take the `2k` faces

```
    x_{i,(u,v)}  =  ( L_0 ∪ … ∪ L_{i−1},  {u},  {v},  L_{i+1} ∪ … ∪ L_{k−1} ) ,
```

one for each level `i` and each order `(u,v)` of that level's pair — each is `P`-compatible, and
`x_{i,(u,v)}·c` is `c` with coordinate `i` forced to `(u,v)`. Give each weight `1/(2(n−1))` and give
the identity face `(P)` weight `(k−1)/(2k−1) ≥ 0`. From any chamber, exactly one of the two faces at
level `i` flips coordinate `i`, at probability `1/(2(n−1))` — the lazy AT edge probability — and the
weights sum to `1`. So `Σ_x w(x) T_x = P_lazy` **for every `k ≥ 1`**. ∎

`code/hodge_leverage_audit_d39d/audit_vk_infinite.py` → `out_vk_infinite.txt` checks this in exact
rational arithmetic for `k = 1..8` (`|L(P)|` up to **256**, sixteen times the largest instance either
document verified), including that the AT graph really is `Q_k` and that the weights are nonnegative
and sum to `1`:

```
  k    n   |L(P)|   AT graph = Q_k   weights sum to 1 (nonneg)   sum_x w(x) T_x == P_lazy
  1    2        2   True             True (True)                 True
  ...
  8   16      256   True             True (True)                 True
```

**Both directions, as required.** *"Positive for every `k` tested"* and *"PROVEN … for `k ≤ 4`"* are
**under**-claims — the statement is a theorem with a witness uniform in `k`. *"The positive class is
unbounded"* and *"the infinite family"* are **over**-claims relative to the evidence the documents
cite. The repair makes both right at once: label it PROVEN for all `k`, cite the witness.

---

## §5 — A4 (MODERATE): a rebuild recorded as closing a *control* gap

`docs/…Leverage.md:859–862`, added by this landing:

> **The one control gap this document named itself is now closed, by the auditor.** No negative
> control here perturbs the **Theorem G eigenfunction computation** — the single load-bearing new
> proof — and §13 says so and says an auditor should rebuild it first.
> `code/hodge_leverage_audit_86a3/audit_theoremG.py` does exactly that, with no shared code, to
> `A_12`.

and `STATE.md:136`: *"The one control gap the deliverable named itself — no control perturbs the
Theorem G eigenfunction computation — is **CLOSED** by the audit's own rebuild."*

Three things are wrong with this, in increasing order of importance.

1. **§13 does not say that.** `:1041–1044` says the self-audit *"cannot see an error in a derivation
   the author would re-read as correct — in particular the eigenfunction computation in §6 … **which
   no independent code path re-derives**"*. That is a **replication** gap. The words *"control"* and
   *"negative control"* do not appear in it. §10 attributes to §13 a statement §13 did not make and
   then closes it.
2. **`audit_theoremG.py` contains no control.** I read it: no mutation, no corruption, no falsifier —
   `G1` checks the closed-form weights against brute force, `G2` checks `Pf = f/2`, `G3` checks that
   `1/2` is the second eigenvalue. Every one of them is a *confirmation*. A negative control on
   Theorem G would perturb the eigenfunction or the complex and demonstrate the check firing; none
   exists, before or after.
3. **It is the exact conflation this commit lands a rule against.** `STATE.md:289`, added by
   mg-a806:

   > **A requirement phrased *"show that X holds"* will be implemented as a GREEN ROW if the
   > surrounding artifact is a control battery … A proof obligation must be landed as a PROOF, not as
   > a control.**

   §10's paragraph is the mirror image: a proof (a replication of one) recorded as a **control**. The
   rule's own framing — *"proving a property and testing for it are different operations"* — is
   symmetric, and this landing violates the other half of it in the same diff.

**What is true and should be said instead:** *the replication gap §13 named is closed — the
eigenfunction proof now has an independent code path, and it held to `A_12`. The control gap is
untouched: no mutation of the Theorem G computation exists in either battery, and closing it would
mean perturbing the eigenfunction and showing the check fires.* That is a smaller claim and a true
one, and it keeps the credit that is genuinely owed.

---

## §6 — A5 (MODERATE): §14 says the `STATE.md` row carries the same clauses; it does not

`:1054–1057`:

> **Status: LANDED by mg-a806** … the row below is the repaired text, and **the corresponding
> `STATE.md` row carries the same clauses.**

Sentence-level diff of `docs/…Leverage.md:1059` (10 623 chars) against `STATE.md:136` (13 551 chars).
Clauses present in `STATE.md` and **absent** from §14:

- *"The one control gap the deliverable named itself … is CLOSED by the audit's own rebuild."*
  (i.e. **A4 is asserted only in `STATE.md`**, the artifact that outlives the deliverable);
- *"`A_6` was skipped and that is stated **in four places**, not hidden"* (§14: *"stated, not
  hidden"*) — the count is correct (`:654`, `:893`, `:1005`, `:1059`, plus `lrb_output.txt:41`), but
  it is a claim only one of the two rows makes;
- *"`I − P_du = Δ_AT/(2(n−1))` (PROVEN, **405/405 twice**)"* (§14: *"(PROVEN)"*);
- *"the audit checked the proof step by step: it holds for all finite posets, the sweep being a check
  on it"* (band axioms) — absent from §14;
- *"the audit re-ran it under SIX … and **got 24/24 under all six**"* (§14 omits the result);
- *"**No exclusion is drawn wrongly.**"*, and the whole *"What could not be broken"* enumeration.

Conversely §14 carries the source's-claim-(4) material as its own sentence while `STATE.md` folds it
into a parenthetical inside (2).

None of these is mathematically false. The finding is the **assertion of identity**: §14 tells a
reader that checking one row checks both, and it does not. Given that step 4c exists in this
programme precisely because *"the summary is the artifact that outlives the deliverable"*, a row
saying *"the `STATE.md` row carries the same clauses"* should either be true or say *"carries the same
clauses plus …"*.

---

## §7 — A6 (MINOR): *"including all antichains `n ≥ 3`"* survives inside the repaired row

Ledger B6 (`:895`), after the repair, still reads:

> What survives is **PROVEN-by-computation on the population**: not a Brown walk on 2/5 at `n=3`,
> 11/16 at `n=4`, 55/63 at `n=5`, **including all antichains `n ≥ 3`**

and §0 claim 3 (`:115`) and §9.4 (`:676`) say the same. `run_lrb.py` loops `range(2, 6)`; mg-86a3's
`n = 6` pass is capped at `|L(P)| ≤ 14` and `A_6` has `|L| = 720`. So the universal *"all antichains
`n ≥ 3`"* rests on `A_3`, `A_4`, `A_5` — **three instances, inside the row that was just rewritten for
resting a quantifier on its population.**

It is true, and it is a two-line theorem. For `A_n`, a face `x = (B_1,…,B_k)` with `k ≥ 2` fails the
candidate test at the chamber `c` that lists the blocks in reverse `x`-order: `x·c` inverts every
cross-block pair, so `inv(x·c, c) = Σ_{i<j}|B_i||B_j| ≥ n−1 ≥ 2`, which is neither `0` nor `1`. Hence
for `n ≥ 3` the **only** candidate face is the identity, no AT edge is reachable, and the lazy AT walk
is not a Brown walk. ∎

`code/hodge_leverage_audit_d39d/audit_antichain_scope.py` → `out_antichain_scope.txt` checks the
arithmetic core on `n = 3..7` (min cross-block product `2,3,4,5,6`; the reversing chamber realises
exactly that many inversions, 0 mismatches) and runs the full sufficient test on `A_6` directly —
one `n` past every population the row cites:

```
A_6 : |L|= 720  faces= 4683  candidate faces=1 [([0,1,2,3,4,5],)]
      directed AT edges=3600  reachable by a candidate=0  UNREACHABLE=3600  ->  NOT a Brown walk
```

Wrong label in **both** directions again: a theorem recorded as a computation, and a computation whose
population does not reach the quantifier.

---

## §8 — A7 (MINOR): the floor paragraph and the rule it lands disagree about mg-fcf1

`STATE.md:253`, added by mg-a806:

> ⚠️ **READ THESE NUMBERS AS A FLOOR, NOT A TOTAL:** they count the instances whose consequences have
> been **landed in this document**. Audits merged and not yet landed here are **not** counted (as of
> 2026-07-30 that includes **mg-f7bc and mg-fcf1**) …

`STATE.md:286`, added by the **same commit**:

> **PROVING A PROPERTY AND TESTING FOR IT ARE DIFFERENT OPERATIONS (added 2026-07-30, **from mg-fcf1
> auditing mg-2789**; landed by mg-a806).**

mg-fcf1's consequences **are** landed in this document, by this commit. Either the parenthetical
should drop mg-fcf1, or — if mg-fcf1's own over-wide statement (*"Closes the gap mg-5630 relocated"*,
which its verdict calls *"one notch too wide"*) is a 4d firing — it belongs in the tally. The floor
language means the count *"eight"* survives either way; what does not survive is the parenthetical's
factual claim.

The rest of the Appendix A arithmetic is **consistent and I could not break it**: the table at `:231`
has exactly eight rows, the two tallies at `:259` read `7 + 1 = 8`, and step 4d at `:200` says
*"EIGHT firings AT LEAST"*. The retirement of the single running count, and the explicit floor, are
the right structural response to the three-way contradiction mg-1319 repaired.

---

## §9 — A8 (MINOR): three wording items

1. **Five against six, inside §10.** `:784` still reads *"**All five mutations** below act on objects
   introduced here"*, above a table with **six** rows, and two paragraphs above mg-a806's own
   *"mg-86a3 applied mg-5630's absorbability test to **all six** mutations"* (`:805`). The *"five"* is
   pre-existing (it counts X1a/X1b as one X1) and §13 repeats it (*"a reader tabulating '5 mutations,
   all fire'"*), but the landing put a *"six"* beside it without reconciling. One word.
2. **"Already diagonal".** The hypercube Laplacian is not diagonal; it is **already diagonalised** in
   a known basis. §9.4 gets this exactly right (`:737–738`: *"a sum of `k` commuting terms whose
   spectrum is known by inspection and which is already diagonalised before Brown's theorem is
   invoked"*). §0 (`:119`), B6′ (`:896`), §14 (`:1059`), `STATE.md:135`, `:136` and
   `lrb_output.txt:61` all say *"already diagonal"*. Harmless as idiom, but it is the one place where
   the artifact says something a literal reader can check and find false.
3. **Row G′ extended to `A_9` on a per-link computation.** `γ_i` is a **max over all dimension-`i`
   faces**. `out_theoremG.txt` `G3` computes the full spectrum of the link of the one distinguished
   face, `F(A_m)`, for `m = 3..9`. For `n ≤ 6` §5.2's 404-poset sweep does bound every face; for
   `A_7`, `A_8`, `A_9` nothing computed rules out another dimension-`i` face exceeding `1/2`. It is
   true — by the same join-suppression fact that kills G″, the max is attained at the one-big-block
   face — but the argument is not in the document, and mg-a806 widened the population from `A_7` to
   `A_9` on evidence one notch narrower than the statement. **The fix is to write the join argument
   down once**; it then repairs G″ and G′ together.

---

## §10 — What STANDS, and what I tried to break and could not

This is the longer half of the audit and it is not a formality.

- **THEOREM G STANDS, and the `2^{Θ(n)}` loss is a theorem.** I checked the proof's structure
  independently (the singleton-blocks face, `m = n−i−1 ≥ 3` from `i ≤ n−4`, the eigenfunction, the
  orthogonality to the stationary weights) and the direction of use: `γ_i ≥ 1/2 ⟹ 1−γ_i ≤ 1/2 ⟹
  bound `≤ 2·(1/2)^{n−2}`, and `γ` is the **second-largest eigenvalue of the link walk**, so an
  explicit eigenfunction gives the `≥` the negative needs. The direction is right, the quantifier is
  right, and `run_sweep.py`'s new header — *"`γ_i ≥ 1/2` at every level is PROVEN … So each bound
  below is a PROVEN UPPER bound, printed at its equality value"* — is **correct**, including the
  otherwise-suspicious word *"UPPER"*.
- **The F1 correction is right and I reproduced its evidence.** B6 as a universal is falsified: the
  `n = 6` poset `0<2 0<3 1<2 1<3 2<4 2<5 3<4 3<5` has `|L(P)| = 8 > 4`, is undecided by the sufficient
  test, and is a Brown walk. My own `n = 6` run finds the same 12 undecided posets with the same
  `|L(P)|` multiset. *"Genuine counterexamples, not a coverage gap"* is the correct characterisation.
- **The repair is not a retreat, and the documents are right to insist on that.** *"Do not read this
  as claim (3) being withdrawn"* appears at §14 and in `STATE.md`, and it is warranted: claim 3 is a
  real technique with exact spectra, correctly labelled an **IMPORT** rather than a discovery, and
  correctly de-Hodged (F9). **I found no over-correction anywhere.** Nothing reads as *"the technique
  was withdrawn"* or *"the instrument was broken"*.
- **All four committed artifacts regenerate.** `theorems_output.txt`, `lrb_output.txt` and
  `controls_output.txt` byte-identically; `sweep_output.txt` in exactly the two timing lines. The
  `run_all.sh` narrowing is honest and correctly scoped, and it is the right size — it names the
  lines, says why, and says what did not move.
- **F6 and F7 land at source and land correctly.** The old §B header *"extrapolating `γ_i = 1/2` …
  and proved for the top level"* did disclaim the headline it supports; the new one does not. The
  `w3[:12]` truncation under a printed count of 29 was real, and all 29 tags are now printed — I
  counted them: 29.
- **F5's arithmetic is right.** In `8fc5111`, `n = 8` carried the PROVEN marker and `12`, `20`, `40`
  did not; the repair adds three markers rather than weakening the sentence, which is the correct
  direction because `≥` is what M2 consumes.
- **F3's numbers reproduce** (`out_controls.txt`: smaller `λ₂` on 75 of 2748 links, smaller `γ_i` on
  9 levels, strictly larger mutated bound on 4 posets, X1a fires on 0). And the deliverable's wording
  is **better than the audit's own**: `out_controls.txt` summarises *"the OPERATIVE half ('X1a
  **cannot** fire') is confirmed"*, while §10 correctly writes *"X1a **does not** fire on this
  population … empirically silent here, not structurally incapable"*. Credit for narrowing where the
  source over-stated.
- **F4's three scorings reproduce** (4946/1245; 0/6191 against the buggy link; 0 of 81 downstream),
  and the four downstream rows are **not** downgraded, which is the correct both-directions sizing.
- **F2/§7.1 is a genuine strengthening.** Splitting N1 into N1a (unconditional) / N1b, N1c
  (conditional on L1) / N1r (the conclusion is robust, `E·L^abs·E = (n−1)I − A` on 405/405) makes the
  pricing *less* fragile than the flat PROVEN label did. This is the model of how the other repairs
  should have been sized.
- **Appendix A's tallies are internally consistent** (§8 above), the new rule is correctly attributed
  to mg-fcf1 and correctly places the cause on the PM's wording, and the `5b63037` change to the GREEN
  row (*"none is queued, and `A(P)` is NOT to be built as a route to `λ₂(Δ_AT)`"*) is exactly the size
  of the routing decision it records.
- **Things I tried and failed to break.** I looked for a face of `F(A_n)` at level `i ≤ n−4` whose
  link beats `1/2` (none — joins only suppress); for a poset at `n = 6` outside mg-86a3's `|L| ≤ 14`
  window that is a Brown walk (none — see §11); for a `V_k` witness with a negative weight (none for
  any `k ≥ 1`); for a discrepancy between my link construction and `links.link_skeleton` on the
  counterexample posets (none); and for a disagreement between my §9.4 test and the committed
  `lrb_output.txt` counts (none, `n = 2..5`).

---

## §11 — Contribution: `n = 6` is now complete

B6′'s label column concedes *"`n = 6` at `|L(P)| ≤ 14`"*, and `out_n6_brown.txt`'s own first line says
*"(skipped 214 larger)"* — i.e. the untested region at `n = 6` is exactly the large-`|L(P)|` region,
which is where B6′'s universal-sounding claim is least supported. The exact LP is expensive there; the
§9.4 sufficient test is not, and wherever it fires the poset is settled **negative** outright.

`code/hodge_leverage_audit_d39d/audit_n6_complete.py` → `out_n6_complete.txt`, all 318 posets at
`n = 6` (and `n = 2..5` as a control on the instrument):

```
n=2  posets=  2   NOT:   0   vacuous:  1   undecided:  1
n=3  posets=  5   NOT:   2   vacuous:  1   undecided:  2
n=4  posets= 16   NOT:  11   vacuous:  1   undecided:  4
n=5  posets= 63   NOT:  55   vacuous:  1   undecided:  7
n=6  posets=318   NOT: 305   vacuous:  1   undecided: 12
```

`n = 2..5` reproduces `lrb_output.txt` §5 exactly. At `n = 6` the twelve undecided posets have
`|L(P)| ∈ {2 ×5, 4 ×6, 8 ×1}` and are **exactly** mg-86a3's twelve positives — so all 214 skipped
posets are decided NEGATIVE by the sufficient test, and **the `n = 6` level contains no counterexample
to B6′ anywhere.**

Consequences, offered for landing:

- **B6′'s negative half upgrades** from *"`n ≤ 5` complete, plus `n = 6` at `|L(P)| ≤ 14`"* to
  ***"`n ≤ 6` complete"***.
- **B6″ gains evidence**: on `n ≤ 6` exhaustively the positive class is exactly `{|L(P)| = 2}` (AT
  graph `Q_1`) ∪ `{|L(P)| = 4}` (AT graph `C_4 = Q_2`) ∪ `{V_3}` (`Q_3`) — so *"iff the AT graph is a
  hypercube"* is now verified exhaustively at `n ≤ 6`, not merely *"consistent with"*.
- The `V_k` theorem of §4 makes the *positive* half of B6′ unconditional in `k`.

Together these make the slogan's **content** stronger than the landing claims, which is precisely why
its **quantifier** should be repaired rather than defended: the honest sentence loses nothing.

---

## §12 — The standing targets, answered

1. **Did every site get fixed, and do they now agree?** For the F1 correction: **yes** — §0 claim 3,
   §9.4, rows B6/B6′/B6″, §14, `STATE.md:136` and `lrb_output.txt` §5 all carry it, and I found no
   site still asserting the struck clause. For the *replacement*: **no** — twelve of thirteen sites
   drop its population (§3), and §14's claim that `STATE.md` carries the same clauses is false (§6).
2. **Did the repair over-correct?** **No.** Every repair is sized at least as wide as its evidence;
   §7.1 and F3 are sized *better* than their sources. The two under-claims found (A3, A6) are both
   claims that should be **stronger**, and both are recorded here with the proofs that make them so.
3. **Does the printed text match what the code verifies?** **Yes**, with one qualification. All four
   artifacts regenerate; `run_sweep.py`'s new header is correct including the direction of the bound;
   `run_lrb.py`'s new block is accurate about the LP and the family. The qualification: the block
   asserts *"THE SEMIGROUP TECHNIQUE REACHES `Δ_AT` ONLY WHERE `Δ_AT` IS ALREADY FREE"* — a universal
   the code below it does not compute (site 13 of §3) — and *"already diagonal"* (§9(2)).
4. **Is any new scored row a tautology?** **No new scored row was added.** `controls.py` is untouched
   by this landing and its output regenerates byte-identically. I checked every new **ledger** row for
   the analogous defect — G, G′, G″, N1a/b/c/r, B6′, B6″, S2, P1–P6 — and the answer is the opposite
   one: G″ is not a row that cannot fail, it is a row that **does** fail (§2).
5. **Is a proof obligation being landed as a control?** **The inverse, and yes** — §10's *"the one
   control gap … is now closed, by the auditor"*, where the closer is a replication with no mutation
   in it, in the same commit that lands the rule against the conflation (§5).
6. **New defects at unwatched locations.** Enumerated: A1 (a new PROVEN ledger row, false), A4 (a new
   §10 paragraph), A5 (a new §14 status line), A7 (a new Appendix A parenthetical contradicted by a
   new Appendix A paragraph), A8(1) (a new *"six"* beside an old *"five"*). **Two of the five are
   inside the commit's own description of its method** — A4 describes what the landing closed, A5
   describes the relation between its two summaries — which is the seventh and eighth time in this arc
   that the over-wide statement has landed in a sentence about method rather than about mathematics.

---

## §13 — Ledger of this audit

| # | claim | label | population / evidence |
|---|---|---|---|
| **D1** | joins suppress `λ₂`: for `X * Y` with product weights, a factor eigenfunction survives scaled by `p/(p+q+1) < 1`, and the only other new eigenvalue is `−1/(p+q+1)` | **PROVEN** (§2) | all weighted joins; instantiated at `F(A_3) * F(A_2) → 1/4` and confirmed numerically |
| **D2** | ledger row **G″** is **FALSE** | **PROVEN-by-computation** + the D1 proof | 55 (poset, level) counterexamples and 3901/7989 per-face counterexamples over all posets `n ≤ 6`; smallest `A_2 ⊕ A_3` at `n = 5`, `γ_0 = 1/4`, confirmed by the deliverable's own `local_to_global.gammas` |
| **D3** | Theorem G, M2 and the `2^{Θ(n)}` headline are **unaffected** by D2 | **PROVEN** | G's face has singleton blocks; `G″` occurs at two sites and in no summary |
| **D4** | `V_k` is a Brown walk for **every** `k ≥ 1` | **PROVEN** (§4), witness uniform in `k` | verified in exact rationals for `k = 1..8`, `\|L(P)\|` to 256 |
| **D5** | the lazy AT walk is not a Brown walk on `A_n` for **every** `n ≥ 3` | **PROVEN** (§7) | arithmetic core checked `n = 3..7`; full sufficient test run on `A_6` (`\|L\| = 720`, 4683 faces, 1 candidate face, 3600 unreachable edges) |
| **D6** | at `n = 6` the sufficient test decides all 318 posets: NOT 305, vacuous 1, undecided 12 — the 12 being exactly mg-86a3's positives | **PROVEN-by-computation** | complete enumeration; `n = 2..5` reproduces `lrb_output.txt` §5 exactly |
| **D7** | the four committed artifacts regenerate; three byte-identical, `sweep_output.txt` in the two timing lines only | **PROVEN-by-computation** | this machine, `run_all.sh`'s four steps |
| **D8** | the replacement scope clause is a universal at 12 of its 13 sites, and B6″ calls the same question open | **PROVEN-by-inspection** (§3) | the thirteen sites, quoted with line numbers |
| **U1** | that the slogan is **false** | **NOT CLAIMED** | no counterexample exists at `n ≤ 6` or on `V_k`; the finding is about the quantifier, not the content |
| **U2** | that mg-86a3's other findings need revisiting | **NOT CLAIMED** | F2–F9 all reproduce; only the step-4b aside (G″) is broken |
| **U3** | anything about `A(P)`, the routing, or whether the probe should have been run | **NOT CLAIMED** | out of scope; the routing is pm-onethird's and nothing here disturbs it |

---

## §14 — What must change, minimally

1. **Strike or restrict ledger row G″** (`:881`) and the sentence at `:462–466`. Replace with the
   singleton-blocks form, and record D1 (joins suppress `λ₂`) as the reason — it is worth a row.
2. **Restore the population to the replacement clause** at the twelve sites that dropped it, or at
   minimum at §0 (`:119–122`), the §9.4 blockquote's *"Equivalently"* sentence (`:745`), B6′'s claim
   column (`:896`), §14 (`:1059`), `STATE.md:135`, `:136` and `lrb_output.txt:61–63`. The wording that
   costs nothing: *"…, verified exhaustively for `n ≤ 6` and on `V_k` for every `k`, open beyond that
   (B6″)."*
3. **Upgrade `V_k` and the antichain clause to PROVEN**, with the two witnesses above; then *"infinite"*
   and *"unbounded"* are earned rather than extrapolated.
4. **Rewrite §10's last paragraph**: the **replication** gap is closed, the **control** gap is not.
   Mirror the change in `STATE.md:136`.
5. **Fix §14's status line** to say what the `STATE.md` row carries in addition, or make the rows
   agree.
6. **Drop mg-fcf1 from the floor parenthetical** at `STATE.md:253`, or count its instance.
7. **Land D6**: B6′'s negative half is now `n ≤ 6` complete.

---

*Instrument: `code/hodge_leverage_audit_d39d/` — `audit_gpp.py` → `out_gpp.txt`,
`audit_vk_infinite.py` → `out_vk_infinite.txt`, `audit_antichain_scope.py` →
`out_antichain_scope.txt`, `audit_n6_complete.py` → `out_n6_complete.txt`; `run_all.sh`, ~18 s measured. Pure Python 3, no
third-party packages, no shared code with `code/hodge_leverage/` or
`code/hodge_leverage_audit_86a3/`. `STATE.md` was NOT edited.*
