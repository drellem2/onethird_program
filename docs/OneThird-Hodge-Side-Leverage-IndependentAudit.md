# Independent audit of mg-a3d4 — "Pricing the bet: does the face/Hodge side carry technique the graph side lacks?"

**Audit work item:** mg-86a3 (pre-filed, per STATE.md Appendix A). **Target:** commit `2919d28`,
`docs/OneThird-Hodge-Side-Leverage.md` (706 lines) + `code/hodge_leverage/`. **Path derived from the
parent's merge commit**, not from the parent's body.

**Read in full before anything was computed:** the deliverable; `~/files/intrinsic_face_geometry_program.tex`;
the audited foundation `docs/OneThird-Intrinsic-Face-Geometry-Probe.md` and its audit
`...-IndependentAudit.md`; `code/hodge_leverage/*.py` and all four committed outputs.

**Everything below is re-derivable from `code/hodge_leverage_audit_86a3/run_all.sh`** (pure Python 3,
no third-party packages, ~10 min). The audit shares **no code** with `code/hodge_leverage/` or
`code/face_geometry/`: posets are enumerated by element extension and canonicalised by colour
refinement (A000112 = 1,1,2,5,16,63,318 is the check), linear extensions by minimal-element
recursion, ideals by direct down-closure test, `λ₂(Δ_AT)` by a from-scratch Lanczos with full
reorthogonalisation cross-checked against dense Jacobi and against `2−2cos(π/n)`.

---

## §0 — Verdict

# OVERSTATED

**0 broken mathematics.** Every headline number reproduced independently — 405, 404, 44 055, 6197,
97, 2.6204, 373/29, `2^{3−n}`, and every row of §5.3's two width-2 families. **Theorem G — the
single load-bearing new proof, and the one the deliverable's own §13 names as the thing an auditor
must rebuild — is CONFIRMED**: I re-derived the eigenfunction by hand, rebuilt the Coxeter complex
from its definition with no shared link code, and the identity `Pf = f/2` holds in exact rational
arithmetic for `A_3 … A_12` (the deliverable reached `A_8`), with `λ₂ = 1/2` exactly for `A_3 … A_9`
(the deliverable's row G' claims `A_3 … A_7`). It is complete, it is `n`-free, and the `2^{Θ(n)}`
loss is a theorem, not an extrapolation. **The headline stands and the A(P) recommendation does not
reverse.**

Four things must be repaired before §14 lands, and one of them is a claim with infinitely many
counterexamples.

| # | finding | severity | does the routing reverse? |
|---|---|---|---|
| **F1** | **§9.4's "undecided" is not undecided.** Every case the deliverable leaves open is decided by a finite exact rational LP, and every one is decided **positively**: the lazy AT walk **IS** a Brown walk there. The `\|L(P)\| ≤ 4` boundary is an artifact of stopping at `n = 5` — at `n = 6` there is a poset with `\|L(P)\| = 8`, and an **infinite family** `V_k` with `\|L(P)\| = 2^k`, on which the AT walk is a Brown walk. Ledger row **B6 has genuine counterexamples, not a coverage gap.** | **MAJOR** | **No** — see below |
| **F2** | the **inherited L1 conditional is dropped** from ledger row N1 and from the §14 STATE row, which announces that it "carries its own conditions rather than pointing at them". A conditional presented as PROVEN in the text destined for STATE.md. | MODERATE | No — I verified the conclusion is robust to the other reading |
| **F3** | **X1a is retired on a false structural claim.** §10 says uniform link weights are always `γ`-inflating so the mutation "can never falsify (LG)". Measured: smaller `λ₂` on **75 of 2748 links**, smaller `γ_i` on 9 levels, and a strictly **larger** mutated bound on **4 posets**. X1a *can* move the bound in the falsifying direction; it just doesn't go far enough. | MODERATE | No |
| **F4** | **X2 is a distinguishability check, not a falsification control.** Its mutation changes 4946 faces and falsifies **nothing** downstream (0 of 81 posets get a false (LG)). It is not a gauge and not unfalsifiable — but its "fires on 4946" sits in the same table column as X1b's "398 posets yield a **false** (LG)", which are not the same kind of evidence. | MINOR | No |
| **F5** | §0 and §14 say the antichain bound is "**exactly** `2^{3−n}`"; only `≤` is proven. §13's 4c pass says §5.3's rows for `n = 8,12,20,40` are "marked in the table itself as resting on G" — true of **one** of the four. Conservative direction; nothing breaks. | MINOR | No |
| **F6** | the committed artifact **disclaims the headline it supports**: `sweep_output.txt` §B reads "*extrapolating* `gamma_i = 1/2` at every level … and proved for **the top level**". §5.3 says the opposite and is right. | MINOR | No |
| **F7** | `run_sweep.py:84` prints `w3[:12]` under the label "posets with every gamma_i < 1/2: **29**" — 12 of 29 tags, silently. All 29 listed here. | MINOR | No |
| **F8** | §2's "*the free ridges are exactly the holding probability of the canonical down-up walk*" is false as an identification: holding `= ((n−1−deg) + deg/2)/(n−1)`, i.e. free ridges **plus half the interior ridges**. The intended content is stated correctly in the next sentence. Not ledgered. | MINOR | No |
| **F9** | **§1's operational test is too weak to support the word "Hodge"** — the primary value press. Under it, anything not literally the AT graph qualifies. What claim 3 actually uses is the monoid of `P`-compatible ordered partitions: no complex, no boundary map, no Laplacian, no "relative", **no Hodge theory**. | FRAMING, decision-relevant | No, but it **changes what A(P) should be** |

**What the decision may rest on:** Theorem G and M2 (the `2^{Θ(n)}` pricing of claim 2) —
unconditional, `n`-free, rebuilt from scratch. N1's operative content (the top two dimensions are
graph theory) — verified 405/405 and **robust to L1**, see F2. N2. Theorems D, L, H. The whole
measurement layer.

**What it may not rest on as written:** B6's `|L(P)| ≤ 4` scope (false one `n` further out);
N1's unqualified PROVEN label; the §10 table's uniform reading of "fires".

**The A(P) call is not reversed, and F1 sharpens rather than weakens it.** On the family where the
AT walk *is* a Brown walk, `Δ_AT` is the hypercube Laplacian — already diagonal by inspection. So the
honest form of the scope clause is stronger than the one written: *the semigroup technique reaches
`Δ_AT` only where `Δ_AT` is already free.* That is a better sentence for STATE.md than "undecided
below `|L(P)| ≤ 4`", and it is the sentence the evidence supports.

---

## §1 — Press 1 (primary): does any claimed advantage survive translation back to the graph?

Taken claim by claim. The characteristic failure being hunted is a true statement restated in Hodge
language and presented as gained.

| claimed | graph-side statement | harder on the graph side? | verdict |
|---|---|---|---|
| **claim 1** (§7, N1) `Δ_AT = E L^rel E = NᵀN`; the top two dimensions are graph theory verbatim | "`Δ_AT = NᵀN` for `N` the signed incidence matrix"; "`∂∂*` is the line-graph matrix" | **No — routine.** First-week spectral graph theory | **Correctly filed as a NEGATIVE.** No advantage is claimed, and none exists. Sound. |
| **claim 2** (§5–§6) link-based local-to-global imports and is exponentially lossy | "the product-form HDX bound, evaluated on this complex, is `2^{Θ(n)}` off" | The *import* needs Theorems D and L, which are genuinely face-side work; the *conclusion* is a negative | **Correctly filed as a priced-out negative.** Sound, and the strongest thing in the document. |
| **claim 3** (§9) Brown's theorem diagonalises every face-driven walk on `L(P)` | there is no AT-graph statement — the walk `c ↦ x·c` is not an AT walk | **Genuinely absent** from the AT graph | **Real technique — but not Hodge.** See F9. |
| **§8** (N2) representation theory does not descend | "the AT graph of a non-antichain has no `S_n` symmetry" | No — obvious | **Correctly filed as a NEGATIVE.** Sound; the Young-module dress adds nothing but costs nothing. |

**F9, stated properly.** §1's test is:

> *A technique lives on the Hodge/face side iff its hypothesis is a statement about an object that
> has no presentation in the adjacent-transposition graph, and its conclusion is a statement about
> `L(P)`.*

This is too weak to carry the word "Hodge". The Bruhat order, descent statistics, coupling, strong
stationary duality and Diaconis–Saloff-Coste comparison all pass it. Applied to claim 3 it returns
YES — but the hypothesis of Brown's theorem is about **the monoid of `P`-compatible ordered
partitions under refinement**. Nothing simplicial is used: not the order complex, not a boundary
map, not a Laplacian, not the pseudomanifold property, not "relative", not `E`. It is the face
semigroup of the braid arrangement restricted to the order cone `C_P` — an object the source's own
*Universal Picture* lists **separately** from the compatible face complex, and one definable from `P`
in a single line.

So the sharp answer to the ticket's question is:

> **The Hodge side carries nothing.** Claims 1, 2 and N2 are all negatives, and I confirm all three.
> The positive is not Hodge and does not need the face complex.

The deliverable is *mostly* aware of this — §0 says "the face SEMIGROUP is where the technique
actually is", §12 says the `A(P)` case "should be rewritten around the face semigroup, not around
Hodge theory", §14 capitalises SEMIGROUP. **That is not a small piece of honesty and it is why this
is a framing finding rather than a broken claim.** But §1's test is what licenses answering the
ticket YES at all, and §14's headline is the ticket's own question — so the reader who stops at the
STATE row gets "the face/Hodge side carries technique: YES", when the audited answer is "the
semigroup does; the Hodge side does not."

**Why this is decision-relevant and not a quibble.** It changes what `A(P)` is. The source's Program
specifies an algebra "generated entirely from compatible faces, their incidences, residues, and
quotient structures". If the win is Brown's theorem for a left regular band, the object to build is
the **semigroup algebra of that band** — an object with known structure theory (Brown 2000; Saliola
on quivers of LRB algebras) — which is a far cheaper build than an operator algebra generated from
face incidences, and delivers the Brown-diagonalisable family directly. §12's first bullet
("`A(P)` … would contain the whole Brown-diagonalisable family") is true, and is the expensive route
to something the cheap route already gives.

**Press 4 — the concrete instance demanded of a positive.** The deliverable does **not** supply a
statement about `L(P)` *proved* using a face-side object with no natural graph-side proof and no
prior literature. It supplies Brown's theorem, correctly CITED, instantiated to a band. Its sharpest
concrete instance (control P4, the Tsetlin library) is the **antichain** case — a classical theorem.
For non-antichain `P` the document verifies that the prediction matches the matrix; it does not
derive a statement previously out of reach. **The deliverable does not claim otherwise** (§0: "new to
this programme"). The correct label for claim 3 is therefore **an import, correctly attributed** —
and the ledger should say import, because "a real technique and it is new to this programme" reads,
in a STATE row, as a discovery.

**Press 2 — is the identity used as evidence?** **No. Clean.** §1's opening sentence states the point
explicitly ("An identity between two descriptions of one matrix transfers every *statement* and no
*method*"), and §1 closes with "Nothing here computes `λ₂(Δ_AT)` a second way and calls the agreement
evidence." I checked every comparison in §5 and §9 and this holds. No finding.

**Press 3 — is the negative about the right thing?** **Yes, and it did not refute weaker versions.**
All four named candidates were taken at strength:

- *localisation by the quotient grading* — Theorem L, and §3 explicitly concedes the **decomposition
  is shared** with the graph side (the induced subgraph is the Cartesian product of the blocks' AT
  graphs) and correctly identifies the missing thing as **the inequality that consumes it**. That is
  the strong refutation, not a weak one.
- *the boundary correction* — §2 (laziness) and §4 (truncation of hexagon to path), with the
  mechanism quantified.
- *the Young-module isotypic decomposition* — §8, with a proof, plus the sharper second half
  (`Σ_i s_i` is not central even where the symmetry exists).
- *higher faces* — §4, proven and quantitative, and the `1/2` it produces is the number that kills §6.

I found no weaker-version refutation. **Credit.**

---

## §2 — F1: §9.4 decided, not left undecided

**This was the clause the routing depended on, and it does not survive as written.**

§9.4 uses a *sufficient* condition only (some AT edge unreachable from the candidate faces). Where
it does not bite, the deliverable stops. But the question is a **finite linear feasibility problem
with rational data**:

```
    exists w >= 0 on faces with   sum_x w(x) T_x = P_lazy ,   sum_x w(x) = 1 ,
    where T_x[c,d] = [ x·c = d ].
```

I solved it exactly (Phase-I simplex with Bland's rule over `Fraction`, `exact_lp.py`).

**First, my rebuild of the deliverable's own test reproduces its counts exactly** — NOT-a-Brown-walk
on 0/2/11/55 at `n = 2,3,4,5`, vacuous 1 per `n`, undecided 1/2/4/7. The test is faithfully
implemented and correctly described.

**Then the LP decides every undecided case, and every one comes out positive:**

| `n` | NOT a Brown walk | **IS a Brown walk** | vacuous |
|---|---|---|---|
| 2 | 0 | **1** | 1 |
| 3 | 2 | **2** | 1 |
| 4 | 11 | **4** | 1 |
| 5 | **55** | **7** | 1 |

with exact rational witnesses printed in `out_brown.txt`. For `|L(P)| = 2` the witness is
`w = (1 − 2/(2(n−1)))` on the identity face and `1/(2(n−1))` on each of the two chambers. For
`|L(P)| = 4` (AT graph `C_4`) it is the identity face at weight `1/2` plus the four one-coordinate
collapses at `1/8` each.

**And the `|L(P)| ≤ 4` threshold is an artifact of stopping at `n = 5`.** Extending §9.4's own
population by one `n` (all 318 posets at `n = 6` with `|L(P)| ≤ 14`) turns up **12** positives,
including one with **`|L(P)| = 8`**. It is not a sporadic case: let `V_k` be the ordinal sum of `k`
two-element antichains (`n = 2k`, AT graph the hypercube `Q_k`, `|L(P)| = 2^k`).

| `k` | `n` | `\|L(P)\|` | §9.4's test | exact answer |
|---|---|---|---|---|
| 1 | 2 | 2 | undecided | **IS a Brown walk** |
| 2 | 4 | 4 | undecided | **IS a Brown walk** |
| 3 | 6 | **8** | undecided | **IS a Brown walk** |
| 4 | 8 | **16** | undecided | **IS a Brown walk** |

So **ledger row B6 has infinitely many counterexamples, not an untested corner.** Four places state
the boundary as if it were the shape of the answer and must be corrected:

- **§0 claim 3**: "(§9.4 — proven for 55 of 63 posets at `n = 5`, undecided only where `|L(P)| ≤ 4`)"
- **§9.4**: "the AT walk is not a Brown walk wherever `|L(P)| ≥ 5`, **on the tested population**, and
  undecided by this test below that" — the hedge is doing all the work, and one `n` further out the
  unhedged reading is false
- **ledger B6**: "Undecided by this test exactly where `|L(P)| ≤ 4`"
- **§14**: "undecided by that test **exactly where `|L(P)| ≤ 4`**"

**The routing does not reverse, and the correct statement is better than the one written.** On `V_k`,
`Δ_AT` is the hypercube Laplacian — a sum of `k` commuting terms, spectrum known by inspection. So
Brown's theorem reaches `Δ_AT` exactly where `Δ_AT` needs no help. The repaired clause:

> **`Δ_AT` is a Brown walk on an infinite family (`|L(P)| = 2^k` unbounded) and not otherwise on any
> poset tested with `|L(P)| ≥ 5`. On that family `Δ_AT` is already diagonal, so the technique of §9
> buys no bound on the bridge quantity anywhere.**

That is the load-bearing fact behind "the case for `A(P)` is claim 3, not claim 2", and it survives
in a stronger form. **A characterisation of the positive class is now a well-posed and cheap open
question** (the evidence is consistent with "iff the AT graph is a hypercube", which I state as a
conjecture on `n ≤ 6` plus `V_{k≤4}` and **do not** claim) — and it would tell pm-onethird exactly
when the semigroup technique touches the bridge quantity, which is a sharper input than "not,
mostly".

---

## §3 — F2: the inherited conditional, and whether the conclusion is robust to it

**The deliverable declines to re-litigate L1, which is correct. It does not carry it, which is not.**

§13(iv): "reading L1 of 'relative' from mg-276d, which that document labels CONDITIONAL and which
this document **inherits** — every statement here about `L^rel` and about free ridges is conditional
on it". mg-276d's own ledger: "L1 … **CONDITIONAL** … the source does not define it".

**Is the conditionality carried into every affected row?** No.

| site | carries L1? |
|---|---|
| §13 | **yes**, in full |
| ledger row **N1** (`Δ_AT = E L^rel E = NᵀN`) | **no** — labelled **PROVEN**, "all finite posets; checked on all 405 posets `n ≤ 6`" |
| ledger row **N1'** | no |
| ledger row **S1** (the verdict row) | **no** — its condition list is "the two citations (LG, Brown) and … the population of B4/B6" |
| **§14**, the proposed STATE row | **no** — and §14 opens "*Carries its own conditions rather than pointing at them*" |

A conditional presented as proven in the text destined for STATE.md is precisely mg-5630's defect
class. **But the size of it is small, and I can say so with a computation rather than an opinion.**

**Does the CONCLUSION survive an alternative reading of "relative"?** **Yes, and provably.** I
verified on **all 405 posets `n ≤ 6`** that under the other reading — no boundary quotient, i.e. the
*absolute* top Laplacian — the twisted operator is

```
    E · L^abs_top · E   =   (n−1)·I − A ,
```

the shifted adjacency matrix of the same adjacent-transposition graph (using `deg + #free = n−1`,
also verified 405/405). So:

- **relative reading** → `Δ_AT = D − A`, a graph Laplacian;
- **absolute reading** → `(n−1)I − A`, a shifted graph adjacency matrix.

Under **either** reading the top-degree Hodge operator is a graph object, and claim 1's conclusion —
"no technique using only facets and ridges can be new" — holds unchanged. **The pricing is robust to
the condition; only the equation as written is conditional.**

Repair, and it is two lines. Split row N1:

- **N1a** `Δ_AT = NᵀN`, `N` the signed vertex–edge incidence matrix — **PROVEN, unconditional**, pure
  graph theory, verified 405/405 here by a disjoint route.
- **N1b** `Δ_AT = E L^rel_top E` — **PROVEN given L1**, i.e. **CONDITIONAL**, inherited from mg-276d.
- **N1c** (the actual new clause) `∂_rel E = N` up to a sign per row — verified 405/405 here; the
  twisted signs at the two facets of every interior ridge are always opposite.
- and a sentence in §14: *the conclusion is robust to the reading — under the absolute reading the
  operator is `(n−1)I − A`, still a graph object (checked 405/405).*

---

## §4 — What I reproduced

Every number, by a disjoint route. Two are reproduced digit-for-digit including the ratio quartiles.

| deliverable | independent | agree |
|---|---|---|
| 405 posets `n ≤ 6` (A000112) | 1, 2, 5, 16, 63, 318 by element extension + colour refinement | ✅ |
| **404** posets in the sweep | 404 = 405 − the single `n = 1` poset. **Confirmed: it is the `n=1` exclusion, not a dropped poset** | ✅ |
| Theorem **D** on 405/405 (317 with `\|L\|≥2`) | 405/405, 317 | ✅ |
| Theorem **N1** on 405/405 | 405/405, and separately N1a/N1b/N1c all 405/405 | ✅ |
| Theorem **L**: 6197 faces, 0 failures | 1+5+37+397+5757 = 6197 | ✅ |
| **P5**: 97 block-type keys `n ≤ 5`, 0 clashes | 97, 0 | ✅ |
| Theorem **H**: 44 055 links, exactly 5 shapes | 44 055; C_4 10539, C_6 3714, P_2 6431, P_3 17816, P_4 5555 — **every per-shape count identical** | ✅ |
| (LG) violations: 0 at every `n` | 0 at every `n` | ✅ |
| truth/bound min/median/**max**: `n=4` 1.0000/1.1716/1.3333, `n=5` 1.0000/1.6000/1.8127, `n=6` 1.0000/2.3290/**2.6204** | identical to 4 d.p. | ✅ |
| **2.62** | **2.6204**, at `n = 6` | ✅ |
| `γ_i ≤ 1/2` on all 404, attained by **373**, all-below on **29** | 373, 29 (all 29 tags listed in `out_sweep.txt`) | ✅ |
| `2^{3−n}` on the antichain | **exact, not fitted**: `bound = 2·(1/2)^{n−2}`, `n−2` levels; equality verified `n ≤ 6` | ✅ |
| §5.3 `C_a ⊔ C_a` and fence rows (`\|L\|` 6/20/70 and 5/16/61/272; `γ` 0.333/0.407/0.442/0.460) | identical | ✅ |
| **Theorem G** `Pf = f/2`, `A_3…A_8` exact | `A_3…A_12` exact, **three** different `a`-vectors, no shared link code | ✅ **extended** |
| **G'** `λ₂ = 1/2` exactly, `A_3…A_7` | `A_3…A_9` | ✅ **extended** |
| LRB axioms, supports = acyclic partitions, `n ≤ 5` | 0 violations, 0 mismatches, 87/87 | ✅ |
| Brown multiplicities nonneg, summing to `\|L(P)\|` | 0 negative, 0 wrong totals, `n ≤ 5` | ✅ |
| Brown spectrum vs matrix, exact ranks, `n ≤ 4`, **3** weight families | correct on 16/16 at `n=4` under **6** weight families (adding uniform-on-all-faces, chambers-only, `3^k`-on-`k`-blocks), **with the same `m_X` reused** | ✅ **extended** |
| §9.4 counts 0/2/11/55 NOT-a-Brown-walk | identical | ✅ |
| X2 fires 4946 / vacuous 1245 | identical | ✅ |

**Theorem G, re-derived by hand.** For the antichain, the dimension-`i` face with one block of size
`m = n−i−1 ≥ 3` and `i+1` singletons has `link ≅ F(A_m)`, the Coxeter complex of `S_m`, vertices the
proper nonempty `S ⊆ [m]` with induced weight `|S|!(m−|S|)!` (I checked the closed form against
brute-force facet counting, `m = 3..7`). The 1-skeleton walk picks a uniform `k ∈ [m−1]∖{s}` and
outputs the length-`k` prefix of a uniform flag through `S`. For `f(S) = Σ_{i∈S} a_i` with `Σa_i = 0`:
`k < s` gives `(k/s)f(S)`; `k > s` gives `f(S) + ((k−s)/(m−s))f(S^c) = f(S)(m−k)/(m−s)`. Summing,
`(1/(m−2))[(s−1)/2 + (m−s−1)/2] = 1/2`, **independent of `s` and of `n`**. Orthogonality to the
constants is the `S_m`-symmetry of `w`. `f ≠ 0`. Since `λ₂` is the max over the orthocomplement of the
constants of a reversible operator, `λ₂(link σ) ≥ 1/2`, hence `γ_i ≥ 1/2` — the max over faces at
level `i`, so **one** witnessing face suffices, which is the right direction.

**The proof is complete, `n`-free, and uses `m ≥ 3` exactly where `i ≤ n−4` supplies it.** The
`A_3…A_8` computation is a check on a proof, as claimed — not its support. **`M2`'s `2^{Θ(n)}` loss
is a theorem.** The deliverable's restraint in not upgrading the *equality* `γ_i = 1/2` is
**correctly placed**: nothing downstream needs it (M2 uses only `≥`, and a smaller bound only
strengthens the negative), and I found no easy proof of `≤ 1/2` — trickling-down at the fixed point
returns `1` and gives nothing. See F5 for the two places the equality nonetheless leaks into prose.

**Brown multiplicity independence of `w`** (targeting item 6): the formula
`Σ_{Y ≥ X} m_Y = ∏_{B∈X} |L(P|_B)|` contains no `w`, so `w`-freeness is definitional; what has to be
checked is that the *same* numbers work against the actual matrix for genuinely different `w`. I
computed `m_X` once per poset and reused it across **six** weight families, verifying by exact
rational rank that `dim ker(M − ΛI)` matches for every distinct predicted `Λ` and that the dimensions
sum to `|L(P)|` (which also certifies diagonalisability). **Correct on all 24 posets `n ≤ 4` under all
six.** ✅

**The LRB property is a property of all finite posets, not of `n ≤ 5`** (targeting item 6). §9.1's
proof is genuine and I checked each step: closure holds because lexicographic order on `(i,j)`
respects both constraints; `x·x = x` because `B_i ∩ B_j ≠ ∅` only for `i = j`; `xyx = xy` and
associativity because both sides order the same nonempty intersections by the same tuple; `(P)` is
two-sided identity. `supp(x·y) = supp(x) ∨ supp(y)` is the common refinement by construction. Ledger
B1 is correctly labelled PROVEN and the `n ≤ 5` sweep is a check on it. **Ledger B2's restraint (the
supports = acyclic-partitions equality labelled by-computation on `n ≤ 5`) is if anything
under-claimed** — topological sorting the blocks of an acyclic `P/π` gives a compatible ordered
partition, and the converse is immediate, which is a proof for all finite posets.

---

## §5 — F3/F4: the mg-5630 test applied to the control battery

**Credit first, and it is real rather than assumed.** I applied mg-5630's absorbability test to all
six mutations. **None of X1a, X1b, X2, X3, X4, X5 is a gauge in disguise.** The battery varies weight
families and posets; the corruptions act on the weighted link, the down-up walk, the band product and
the multiplicity rule — **none is absorbable into a parameter the battery already varies**, and none
is a diagonal conjugation or any other isospectral relabelling. X1b, X3, X4 and X5 are each scored by
a **downstream failure** (a false (LG); Theorem D failing; the band axioms or Brown spectrum failing;
negative multiplicities). **That is a direct and unprompted response to the NC3 lesson and it holds
up.** The two findings below are calibration defects inside a battery that is, in kind, the right one.

### F3 — X1a's retirement rests on a false structural claim

§10: "*The reason is structural, not luck: (LG) is a lower bound, and uniform link weights come out
with `λ₂` at least as large as the induced-measure ones on every poset here, so the mutated bound is
smaller and still true. A mutation that inflates `γ` can never falsify (LG).*"

The last sentence is correct and structural. The premise it is applied to is false. Measured over all
posets `n ≤ 5`:

| | |
|---|---|
| links where uniform weights give a **smaller** `λ₂` | **75 of 2748** |
| levels where uniform weights give a **smaller** `γ_i` | **9** |
| posets where the mutated bound is **strictly larger** than the true bound | **4** |
| posets where X1a fires | **0** (vacuous on 81; bound value changed on 55) |

So the mutation is **not** `γ`-inflating, the mutated bound is **not** always smaller, and X1a is
**not** structurally incapable of falsifying (LG) — on 4 posets it moves the bound in the falsifying
direction and simply does not move it far enough. **The operative conclusion is right** (X1a doesn't
fire on this population; X1b is the usable control; keeping X1a in the report with a diagnosis is
good practice). **The reason given for it is exactly backwards**, and it is the same shape as
mg-5630's defect — a property incidental to the instance read as a law. It lands inside §10, which
§13's own 4c pass certifies as clean.

Repair: replace "The reason is structural, not luck" with the true statement — *X1a does not fire on
this population; on 4 posets the mutation does deflate `γ` and enlarge the bound, but never past the
truth. It is empirically silent here, not structurally incapable.*

### F4 — X2 is a distinguishability check, not a falsification control

`controls.py:304` scores X2 as `mut == set(verts)` → vacuous, else fires: **"the mutated vertex set
differs from the link as this codebase computes it."** Three measurements:

| scoring | result |
|---|---|
| as implemented, vs the correct link | fires on 4946 faces, vacuous on 1245 *(matches the committed output exactly)* |
| as implemented, vs a link carrying the very bug X2 mutates toward | fires on **0**, vacuous on 6191 → returns FAIL |
| **downstream: does the X2 mutation falsify (LG)?** | **fires on 0 posets, vacuous on 81** |

**Explicitly not the mg-5630 finding.** X2 is not a gauge and not unfalsifiable: injecting the exact
bug it mutates toward makes it go silent, so it *does* guard that one alternative construction. What
it does not do is detect anything else, and its mutation — though it changes 4946 faces — **breaks no
downstream result**. Its "fires on 4946 faces" therefore sits in the same table column as X1b's "398
posets — the perturbed construction yields a **false** (LG)", and those are not the same kind of
evidence. §10's framing ("All five mutations below act on objects introduced here … Vacuity is
**computed**") is accurate but incomplete: what is not computed is whether firing *means* anything.

Also, the criterion in `controls.py:287–288` — "*the vertex count must stop matching
`Σ_i #proper ideals of Q_i`*", a comparison against Theorem L's **independent** prediction — is not
the criterion implemented. On this population the two agree face-for-face (4946/1245 either way), and
**the true link's vertex count matches Theorem L on 6191 of 6191 faces**, which is itself an extra
independent confirmation of Theorem L. So the mismatch is inconsequential here; the code and its own
docstring nonetheless describe different tests.

Repair: score X2 by the (LG) criterion or by the Theorem-L count, and label the current number as a
distinguishability check.

**The control gap that remains, and the deliverable names it itself.** No negative control perturbs
the **Theorem G eigenfunction computation**, the single load-bearing new proof; §13 says so and says
an auditor should rebuild it first. **That gap is now closed by this audit** (`audit_theoremG.py`,
no shared code, `A_3…A_12`).

---

## §6 — Appendix A step 4b: strength check and falsifier quantifier

| claim | falsifier, with quantifier | is this the strongest true form? |
|---|---|---|
| **G** `γ_i ≥ 1/2` for `A_n`, `∀ n ≥ 3, ∀ −1 ≤ i ≤ n−4` | one `(n, i)` with every dimension-`i` face of `F(A_n)` having `λ₂(link) < 1/2` | **No — it is weaker than its own proof.** The proof uses only that *some* block is an antichain of size `≥ 3`. The immediate strengthening, free from G + Theorem L: **`γ_i ≥ 1/2` for every finite poset having a dimension-`i` face one of whose blocks induces an antichain of size `≥ 3`.** The deliverable instead gets `C_a ⊔ C_a` past the same bar separately, via the `P_4` row of Theorem H. Strengthening in the direction of its own conclusion. **⚠️ ANNOTATION ADDED 2026-07-30 BY mg-a2bd — the cell's own text is left verbatim as the record of what this audit proposed; the proposed strengthening is FALSE.** mg-a806 adopted it as ledger row **G″** of the deliverable, and mg-d39d (finding A1) refuted it: **55 (poset, level) counterexamples at `n ≤ 6`**, smallest at `n = 5`, and 3901/7989 faces under the per-face reading. It is **not free**: Theorem L makes a non-singleton link a **join**, and a join **suppresses** `λ₂` by `p/(p+q+1) < 1` (row **J**, §6.1 of the deliverable), so an exact `1/2` in a factor is strictly below `1/2` in the join. Theorem G escapes only because its face's other blocks are **singletons**, which contribute no join factor — the dropped hypothesis was the one doing the work. **Theorem G itself is unaffected and this audit's CONFIRMATION of it stands.** See `docs/OneThird-Hodge-Side-Leverage-StateLanding-IndependentAudit.md` §2 and the strike in `docs/OneThird-Hodge-Side-Leverage.md` §6. |
| **M2** `2^{Θ(n)}` loss on `A_n` | a proof that `λ₂(Δ_AT(A_n))` is not `Θ(n^{−2})`, or that some `γ_i < 1/2` | Yes, given G and CLR. Both sides are theorems. |
| **N1** `Δ_AT = E L^rel E = NᵀN`, all finite posets | one poset where the twisted relative Gram matrix differs from `D − A` | Yes for the `NᵀN` half; the `E L^rel E` half inherits L1 (**F2**) |
| **N1'** no top-two-dimension technique is new | a top-two-dimension technique with no graph translation | Correctly split: PROVEN for two named instances, **HEURISTIC as a universal**, and §13 flags §0 as broader than the row. Honest. |
| **B6** the lazy AT walk is not a Brown walk | **one poset with `\|L(P)\| ≥ 5` where it is** | **Falsified under the natural reading.** `V_3`: `n = 6`, `\|L(P)\| = 8`. Survives only inside the hedge "on the tested population" (**F1**). |
| **LG** the cited product-form bound | one poset where `λ₂(Δ_AT) < 2∏(1−γ_i)` | Correctly CITED-and-checked; row LG states the consequence of misremembering it. Exemplary. |
| **M1** truth/bound `≤ 2.62`, ratio grows with `n` | a poset `n ≤ 6` exceeding 2.6204 | Yes for that population; "grows with `n`" is correctly stated as an observation, not extrapolated |
| **B4** the instantiation is correct | a poset/weight where the predicted ranks miss | Yes; `A_6` skip stated in the code output **and** in §9.3 **and** in the ledger **and** in §14 — three-deep, and correct |

---

## §7 — Appendix A step 4d: generalisation audit

**The family establishing the most general statement, and what it holds fixed.**

| statement | establishing family | holds fixed | `n`-free? |
|---|---|---|---|
| D, L, H, H', NV, N1, N2, N2', B1, B2' | proofs, no family | mg-276d Lemmas 1–3; `J(P)` distributive; standard simplicial signs; **L1** (F2) | yes |
| **G** | the antichain `A_n`, face = one size-`m` block + `i+1` singletons | the block is an **antichain**; facet-count induced weights; the non-lazy 1-skeleton walk. **`n` is not held fixed** | **yes — confirmed by rebuild** |
| G' (equality) | computation `A_3…A_7` (`A_3…A_9` here) | `n ≤ 7` (`≤ 9`) | no, and **correctly not upgraded** |
| M1, M3 | the complete iso-class enumeration `n ≤ 6`; `C_a⊔C_a` `n ≤ 8`; fences `n ≤ 7` | those populations, stated | no, and stated |
| **B6** | the swept population **`n ≤ 5`** | **`n ≤ 5` — and that is exactly what manufactures the `\|L(P)\| ≤ 4` threshold** | **no, and the threshold is presented as the shape of the answer** |

**The deliverable's own 4d pass named Theorem G as "the statement quantified over `n` rather than
over posets … where this arc's failure has landed six times", gave it a proof, and cleared it. That
was the right call and G survives.** But 4d was run on G only. **B6's quantifier — over a population,
with a numeric boundary read off that population — was not examined**, and that is where the
over-wide statement is this time: **a scope threshold inside a negative result**, at a new location
again. The deliverable's protection against 4d (supply a proof) was applied to the claim it expected
to fail and not to the one that did.

Note also **F5** as a small 4c/4d hybrid: §13 asserts "§5.3's rows for `n = 8,12,20,40` are marked in
the table itself as resting on G, not on the trend". The `n = 8` row is marked
("`1/2 ×6 (§6: ≥ 1/2 PROVEN)`"); the `n = 12`, `20`, `40` rows read plain "`1/2 ×10`", "`1/2 ×18`",
"`1/2 ×38`" and their bound/ratio columns are **equality** values. **A self-audit cannot see the
sentence it is auditing** — the miss is inside the clause 4c certifies.

---

## §8 — Appendix A step 4c: §14, the proposed STATE row, clause by clause

Run here regardless of the deliverable having run it, because a self-audit cannot see the sentence it
is auditing. §14 is a **primary** target.

| clause of §14 | status |
|---|---|
| "AMBER-POSITIVE · the bet is priced" | **Sound.** Both halves earned. |
| "(1) … `Δ_AT = E L^rel E = NᵀN` … **(PROVEN, all finite posets; checked 405/405)**" | **F2.** The `E L^rel E` term is conditional on L1, which §13 says the document inherits. `Δ_AT = NᵀN` is unconditional. Reproduced 405/405 here. **Repair: split, and add the robustness sentence — the conclusion holds under the absolute reading too, `(n−1)I − A`, checked 405/405.** |
| "any new leverage must come from the faces below the top two dimensions" | **Sound**, and this is the sharpest thing in the row. |
| "(2) … `I − P_du = Δ_AT/(2(n−1))` (PROVEN)" | **Sound.** 405/405 independently. |
| "localisation … verified as a simplicial isomorphism on all 6197 faces, `n ≤ 5`" | **Sound.** 6197 reproduced. |
| "never violated on any of the 404 posets `2 ≤ n ≤ 6` and never worse than a factor 2.62" | **Sound.** 0 violations; 2.6204; 404 = 405 − the `n=1` poset, confirmed. |
| "for the antichain it is **exactly `2^{3−n}`**" | **F5.** Only `≤` is proven; the equality is by computation to `A_7` (`A_9` here). Conservative direction. **Repair: "at most `2^{3−n}` (and exactly that for every `n` computed)".** |
| "a `2^{Θ(n)}` loss that is **PROVEN, not extrapolated** … explicit eigenfunction … `Σa_i = 0`, eigenvalue exactly 1/2" | **Sound, and this is the load-bearing clause. Rebuilt from scratch and extended.** The eigenfunction is exactly as stated. |
| "`γ_i ≤ 1/2` holds on all 404 and is attained by 373 … the fence reaches 0.46" | **Sound.** 373/29 and 0.460 reproduced. |
| "`1/2` is the fixed point … pseudomanifold … (this last causal reading is labelled HEURISTIC; the codim-2 consequence is proved)" | **Sound.** The label travels with the clause, in the row, not by reference. Exemplary. |
| "(3) The face SEMIGROUP does carry technique" | **F9.** True, and correctly says SEMIGROUP — but the row's own headline question is "does the face/**Hodge** side carry technique", and the audited answer to *that* is no. **Repair: one clause saying claim 3 uses no simplicial or Hodge structure at all.** |
| "0 axiom violations, all 87 posets `n ≤ 5`" ; "acyclic partitions … NOT closed under refinement — witness `{a<c,b<d}`" | **Sound.** Reproduced; the witness checks out. |
| "Brown's theorem (CITED) … multiplicities … **independent of `w`**" | **Sound**, and verified operationally here across **six** weight families with the same `m_X`. |
| "exact rational rank computations … on all 24 posets `n ≤ 4` under three weight families … **`A_6` was skipped and that is stated, not hidden**" | **Sound.** Correct and well-disclosed. |
| "Sharpest control: the **Tsetlin library** … derangements appear nowhere in the code" | **Sound as a control.** Note it is the **antichain** case, i.e. a classical theorem — good as a control, not evidence of new reach (press 4). |
| "**Scope … `Δ_AT` is NOT a Brown walk** … undecided by that test **exactly where `\|L(P)\| ≤ 4`**" | **F1 — the one clause that must change.** Decided, decided positively, and the threshold fails at `n = 6`. **Repair as in §2 above; the replacement is stronger.** |
| "Also settled, negatively: representation theory does not descend" | **Sound.** Proof checked line by line, including the transitive-`G`-set argument and the "place `b` in an earlier block" witness. |
| "the source's claim (4) is now PROVEN and quantitative … 44 055 links … exactly these five" | **Sound.** All five per-shape counts reproduced identically. |
| "**NOT CLAIMED:** … no other Hodge technique … BK … weighted chains" | **Correctly scoped. I find no exclusion drawn wrongly.** U1 and U3 correctly record the two axes deliberately untested. |
| "**`A(P)` was NOT built.**" | **Sound.** |
| "**Recommendation, not action:** … the case for it is (3) … not the Hodge/localisation hope" | **Sound in direction; incomplete in content (F9).** The case for (3) does not require `A(P)` as the source specifies it. |

**One clause is missing from §14 entirely and should be added:** the L1 conditional (F2).

---

## §9 — Exhaustive ledger, including reductions asserted in prose

`✅` reproduced/confirmed · `⚠️` repair needed · `➕` strengthened by this audit

| # | claim | deliverable's label | audit |
|---|---|---|---|
| D | `I − P_du = Δ_AT/(2(n−1))` | PROVEN | ✅ 405/405, independent route |
| L | `link(σ) ≅ *_i F(P\|_block)`, product weights | PROVEN | ✅ 6197/6197; vertex count matches on 6191/6191 faces |
| H | codim-2 links are exactly `P_2,P_3,P_4,C_4,C_6` | PROVEN | ✅ 44 055, all five per-shape counts identical |
| H' | `λ₂ ≤ 1/2` at codim 2 | PROVEN | ✅ |
| NV | links of dim `≥ 1` connected, (LG) `> 0` | PROVEN | ✅ proof checked |
| **G** | `γ_i ≥ 1/2` for `A_n`, all `n ≥ 3` | PROVEN | ✅➕ **rebuilt from scratch, `n`-free, complete**; exact to `A_12`. Weaker than its own proof (§6) |
| G' | `γ_i = 1/2` exactly | PROVEN-by-computation `A_3…A_7` | ✅➕ extended to `A_9`; **restraint correctly placed**; but see ⚠️ **F5** |
| N1 | `Δ_AT = E L^rel E = NᵀN` | PROVEN | ⚠️ **F2** — split into unconditional (`NᵀN`) and L1-conditional (`E L^rel E`); both verified 405/405 |
| N1' | no top-two-dimension technique is new | PROVEN (2 instances) + HEURISTIC (universal) | ✅ correctly split, and §13 flags §0 as broader |
| N2 | shape-`α` face span is not an `S_n`-submodule | PROVEN | ✅ proof checked line by line |
| N2' | `Σ_i s_i` not central for `n ≥ 3` | PROVEN | ✅ |
| B1 | `F(P)` is a left regular band | PROVEN | ✅ **all finite posets, not `n ≤ 5`** — proof checked |
| B2 | supports = acyclic partitions, join-closed | PROVEN + by-computation | ✅ (if anything **under**-claimed: the equality is provable in two lines) |
| B2' | acyclic partitions not refinement-closed | PROVEN (witness) | ✅ |
| B3 | Brown's theorem | CITED | ✅ correctly cited, not re-derived |
| B4 | the instantiation is correct | by-computation, `n ≤ 4` × 3 families | ✅➕ 6 families, same `m_X` |
| B5 | `m_X` nonneg integers summing to `\|L(P)\|` | by-computation, 405 | ✅ |
| **B6** | the lazy AT walk is **not** a Brown walk | by-computation; undecided where `\|L(P)\| ≤ 4` | ⚠️ **F1 — decided, positively; infinitely many counterexamples; threshold is an `n ≤ 5` artifact** |
| LG | the cited product-form bound | CITED, checked | ✅ 0 violations on 404 |
| M1 | truth/bound `≤ 2.62`, grows with `n` | by-computation | ✅ 2.6204 |
| M2 | `2^{Θ(n)}` loss on `A_n` | PROVEN given G + CLR | ✅ **the headline survives** |
| M3 | removing the hexagon does not repair the bound | by-computation | ✅ every row of both families reproduced |
| T | `1/2` is the trickling-down fixed point | CITED + arithmetic | ✅ |
| T' | the cause is the pseudomanifold property | HEURISTIC | ✅ correctly labelled, and the label travels into §14 |
| S1 | the verdict | CONDITIONAL on LG, Brown, B4/B6 populations | ⚠️ **add L1 (F2); B6's population is now decided (F1)** |
| U1/U2/U3 | not claimed | NOT CLAIMED | ✅ **no exclusion drawn wrongly** |
| — | **§1's operational test for "lives on the Hodge side"** *(prose)* | unledgered | ⚠️ **F9 — too weak to carry "Hodge"** |
| — | **§2 "the free ridges are exactly the holding probability"** *(prose)* | unledgered | ⚠️ **F8 — false as an identification**; holding `= (free + deg/2)/(n−1)` |
| — | **§10 "The reason is structural, not luck"** *(prose)* | unledgered | ⚠️ **F3 — the premise is false on 4 posets** |
| — | **§10 X2 "fires on 4946 faces"** *(table)* | scored as a control | ⚠️ **F4 — distinguishability, not falsification** |
| — | **§13 "§5.3's rows for `n = 8,12,20,40` are marked in the table itself"** *(prose)* | self-audit | ⚠️ **F5 — one of four** |
| — | **`sweep_output.txt` §B "extrapolating … proved for the top level"** *(artifact)* | committed output | ⚠️ **F6 — the artifact disclaims the headline it supports** |
| — | **`run_sweep.py:84` `w3[:12]` under a count of 29** *(artifact)* | committed output | ⚠️ **F7 — silent truncation** |
| — | claim 3 is "a real technique and it is **new to this programme**" *(prose)* | unledgered | ✅ **accurate as written** — but reads as discovery in a STATE row; it is an **import**, correctly attributed |

---

## §10 — What I could not break

Recorded because a clean result is information, and because a negative that is comfortable in one
direction is comfortable in the other.

- **Theorem G.** I tried to break it in three ways: a different construction of the Coxeter complex,
  three different `a`-vectors, and pushing to `m = 12`. It held exactly. The proof has no gap.
- **The `2^{Θ(n)}` conclusion.** Unconditional, `n`-free, resting on a proof plus a correctly-cited
  theorem. It is the strongest thing in the document.
- **The identity-as-evidence trap.** Not present anywhere. The deliverable states the trap in §1 and
  avoids it throughout.
- **The negative's coverage.** All four candidates taken at strength; no weaker version refuted.
- **Absorbability.** None of the six mutations is a gauge. mg-5630's specific defect is **not**
  repeated.
- **Disclosure.** The `A_6` skip is stated in four places; X1a's non-firing is in the table and not
  only the prose; T' carries HEURISTIC into the STATE row itself. This document discloses better
  than its predecessors.

**The two comfortable answers, checked in both directions.** A negative was cheap here and the
deliverable did not take the cheap version — §9 is a genuine positive that cost work. A positive
founds an expensive programme and the deliverable did not inflate it — §9.4 travels in the same
breath as §9. **The one place the balance slipped is §9.4 itself (F1), where "undecided" was a
resting place, and it slipped toward the negative** — which is the direction the document's own
verdict wanted.

---

## §11 — Routing

**Verdict: OVERSTATED. 0 broken mathematics; the headline and the `A(P)` recommendation both stand;
four repairs required before §14 lands, one of them a claim with infinitely many counterexamples.**

Recommended before the STATE row is landed, in order:

1. **F1** — rewrite B6, §0 claim 3's parenthetical, §9.4's closing sentence, and §14's scope clause.
   The replacement is stronger than the original and is given in §2 above.
2. **F2** — split ledger row N1; add L1 to row S1 and to §14; add the robustness sentence
   (`(n−1)I − A` under the absolute reading, checked 405/405).
3. **F9** — one clause in §14 recording that claim 3 uses no simplicial or Hodge structure, and one
   sentence in §12 noting that the cheap form of the claim-3 case is the LRB semigroup algebra rather
   than `A(P)` as the source specifies it.
4. **F3, F4** — fix §10's X1a diagnosis and re-score or re-label X2.
5. **F5–F8** — small, local.

`STATE.md` **not edited**, per the ticket. §14's row remains a proposal. Raw verdict to pm-onethird;
not relayed to Daniel.

**Audit artifacts:** `code/hodge_leverage_audit_86a3/` — `run_all.sh` and nine committed outputs.
