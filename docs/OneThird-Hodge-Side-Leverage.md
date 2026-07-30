# Pricing the bet: does the face/Hodge side carry technique the graph side lacks?

**Work item:** mg-a3d4. **Question asked:** the bridge of mg-276d is an *identity*
(`Δ_AT = E L^rel E`), so it transfers everything and buys no bound. Does the face-complex /
Hodge side carry **technique** the adjacent-transposition-graph side lacks?
**Not built:** `A(P)`. **Not re-verified:** the foundation (mg-276d, audited CONFIRMED by mg-e0ce);
it is used, not rechecked.

**Sources read in full before anything was computed:** `docs/OneThird-Intrinsic-Face-Geometry-Probe.md`,
`docs/OneThird-Intrinsic-Face-Geometry-Probe-IndependentAudit.md`,
`~/files/intrinsic_face_geometry_program.tex`.

**Re-derivable:** every number below comes from `code/hodge_leverage/run_all.sh`
(pure Python 3, no third-party packages; exact integer/rational arithmetic except where an
eigenvalue is reported, ~13 min). Committed outputs: `sweep_output.txt`, `theorems_output.txt`,
`lrb_output.txt`, `controls_output.txt`. **§6.1 (Theorem J, added by mg-a2bd) is checked separately by
`code/hodge_leverage_join/run_all.sh` (~21 s) → `out_verify_join.txt`; that directory contains no
mutation and scores no control — it is a replication of a proof.**

**Post-audit status (independent audit mg-86a3, `2cc8d57`; repairs landed by mg-a806).** Verdict
**OVERSTATED**, with **0 BROKEN mathematics** — every headline number reproduced by a disjoint route
(405, 404, 44 055, 6197, 97, 2.6204, 373/29, `2^{3−n}`, and every row of §5.3's two width-2
families). Audit instrument: `code/hodge_leverage_audit_86a3/`, sharing **no code** with
`code/hodge_leverage/`.

**⚠️ Second-generation status (independent audit mg-d39d of the mg-a806 landing, `522048f`; finding A1
landed by mg-a2bd).** That landing added a ledger row **its ticket never asked for**, and the added row
is the **first BROKEN mathematics in this arc**: **G″ is FALSE** — 55 (poset, level) counterexamples at
`n ≤ 6` — and it is **struck** (§6, ledger). The reason is now recorded as ledger row **J**: *Theorem L
makes links **joins**, and joins **suppress** `λ₂`*. Two things must be read with it. **THEOREM G
STANDS** — its face's other blocks are singletons, so its link is not a join, and mg-86a3's rebuild to
`A_12` is untouched; the `2^{Θ(n)}` headline, M2, the `A(P)` routing and every summary are unaffected,
because nothing ever consumed G″. And **the rest of mg-d39d is NOT landed here** — its findings A2–A8
(the replacement scope clause's quantifier, the `V_k` and antichain upgrades, §10's control/replication
conflation, §14's *"same clauses"*, and the `n = 6` completion it contributes) remain open at the time
of writing and belong to other tickets. Do not read this document as fully repaired against mg-d39d.

**Read this part first, because it is the largest thing the audit did and it is a confirmation, not a
correction. THEOREM G IS CONFIRMED, AND THE `2^{Θ(n)}` LOSS IS A THEOREM.** §13 named the §6
eigenfunction computation as the single load-bearing new proof and as the first thing an auditor
should rebuild from scratch. The auditor rebuilt it twice over: re-derived the eigenfunction **by
hand**, and rebuilt the Coxeter complex from its definition with **no shared link code**. `Pf = f/2`
holds in exact rational arithmetic for `A_3 … A_12` (this document reached `A_8`), and `λ₂ = 1/2`
exactly for `A_3 … A_9` (row G′ claimed `A_3 … A_7`) — **four orders of `n` past the range each was
stated on**. The proof is complete, it is `n`-free, and it uses `m ≥ 3` exactly where `i ≤ n−4`
supplies it. So **M2's `2^{Θ(n)}` loss is a theorem and the headline stands.** The audit tried to
break it three ways — a different construction of the Coxeter complex, three different `a`-vectors,
and pushing to `m = 12` — and records it as *"the strongest thing in the document"*. This is stated
first deliberately, and it is a **methodological** result as much as a mathematical one: Theorem G is
the statement quantified over `n` rather than over posets, which is where this arc's failure had
landed six times; §13 identified it as exactly that, gave it a proof rather than a trend, and **the
proof held under an independent rebuild.** That is the arc's best methodological result to date and
it must not be read as a footnote to F1 below.

**Repairs landed here, each marked at its site.** **F1 (MAJOR)** — §9.4's *"undecided"* was **not
undecided**: the question is a finite exact rational LP, every case left open is **decided, and
decided positively**, and the `|L(P)| ≤ 4` boundary is an artifact of stopping at `n = 5`. **Ledger
row B6 is FALSIFIED as a universal — it has genuine counterexamples, an infinite family of them, not
a coverage gap.** Repaired at all four sites (§0 claim 3, §9.4, rows B6/B6′, §14). **The replacement
scope clause is STRONGER than the one it replaces and must not be read as a retreat:** claim 3 is a
real technique that does not reach the bridge quantity, and the reason is now known rather than
untested. **F2** — ledger row N1 split into an unconditional half and an L1-conditional half, with
the audit's robustness computation recorded (§7, rows N1a/N1b/N1c, row S1, §14): the **conclusion** is
unconditional, only the **equation** is conditional. **F3** — §10's structural diagnosis of X1a
struck; the premise is measurably false, the operative conclusion is not. **F4** — X2 relabelled a
**distinguishability check**, not a falsification control; the four rows that are scored by a
downstream failure are **not** downgraded. **F5** — *"exactly `2^{3−n}`"* narrowed to *"at most, and
exactly that for every `n` computed"* (§0, §14), and §13's *"marked in the table itself"* corrected
from four rows to one. **F6/F7** — `run_sweep.py`'s printed §B header and its silent `[:12]`
truncation of a 29-item list, both fixed at source. **F8** — §2's identification of the free ridges
with the holding probability corrected. **F9** — §1's operational test recorded as **too weak to
carry the word "Hodge"**, with the consequence carried into §12 and §14: claim 3 uses no complex, no
boundary map, no Laplacian, **no simplicial structure at all**. **Where this document and the audit
disagreed, the audit won.**

**What the audit could not break.** Theorem G. The `2^{Θ(n)}` conclusion. The identity-as-evidence
trap — absent throughout, and §1 both states the trap and avoids it. The negative's coverage — all
four candidates taken at strength, no weaker version refuted. **Absorbability: none of the six
mutations is a gauge in disguise, and mg-5630's specific defect is not repeated here** — checked, not
assumed. Disclosure — the `A_6` skip stated in four places, X1a's non-firing in the table and not
only the prose, T′ carrying HEURISTIC into the STATE row itself.

---

## §0 — Verdict

**YES — but not where the bridge points, and the place the bridge points is priced OUT.**

Three answers, all of them specific:

1. **The top two dimensions of `F(P)` are graph theory verbatim, provably.** After the twist, the
   relative top boundary map **is** the signed vertex–edge incidence matrix of the
   adjacent-transposition graph: `Δ_AT = Nᵀ N` (§7, PROVEN). So the Hodge-theoretic move "pass to
   one dimension down" (`∂*∂ ↝ ∂∂*`) is exactly the classical incidence/line-graph identity, and
   **no technique using only facets and ridges can be new.** This localises where anything new
   would have to live: the faces *below* the top two dimensions — precisely the part mg-276d's
   proof never touched (its §8.3(3)).

2. **The one technique class that does live there — link-based local-to-global — imports
   cleanly, and is exponentially lossy.** Two new theorems license the import: the
   adjacent-transposition walk **is** the standard down-up walk on the facets of `F(P)`
   (§2, Theorem D, PROVEN), and the links of `F(P)` are joins of the face complexes of the
   **induced subposets** on the blocks (§3, Theorem L, PROVEN). So Garland/Kaufman–Oppenheim/
   Alev–Lau applies and, measured against the truth on all **404** posets with `2 ≤ n ≤ 6`, it is
   never violated and never better than a factor `2.62` off — but the gap grows: on the antichain
   family the link bound is **at most `2^{3−n}`** — and exactly that for every `n` computed, `A_3…A_9`
   (**F5**: only `≤` is proven, which is the direction the negative needs) — while
   `λ₂(Δ_AT) = 2 − 2cos(π/n) = Θ(n^{−2})`
   (§5–§6). That is a `2^{Θ(n)}` loss, and it is **PROVEN, not extrapolated**: every level's link
   has `λ₂ ≥ 1/2` by an explicit eigenfunction (§6, Theorem G). The mechanism is structural —
   `1/2` is the fixed point of the trickling-down recursion `γ ↦ γ/(1−γ)`, so `F(P)` sits exactly
   at the value where the whole local-to-global hierarchy becomes vacuous. **The property that
   puts it there is the pseudomanifold property — mg-276d's Lemma 3(a), the same fact that makes
   the bridge's "relative" well-posed.**

3. **The face *semigroup* does carry technique, and it is exact rather than a bound.** `F(P)` is a
   left regular band under successive refinement (§9, verified exhaustively `n ≤ 5`), its support
   lattice is the lattice of acyclic partitions of `P`, and **Brown's theorem then diagonalises
   every face-driven walk on `L(P)`**: for any probability `w` on faces, the walk `c ↦ x·c` has
   eigenvalues `λ_X = Σ_{supp(y) ≤ X} w(y)` indexed by acyclic partitions, with multiplicities
   fixed by `Σ_{Y ≥ X} m_Y = ∏_{B ∈ X} |L(P|_B)|` — **independent of `w`**. Verified against the
   actual matrix, exactly, for all 24 posets with `n ≤ 4` under three weight families, and for
   five named `n = 5` instances (§9). This is a whole family of walks on linear extensions whose
   spectrum is *closed-form*, and the graph side has no counterpart because the hypothesis is
   about a semigroup product that the adjacent-transposition graph does not carry. **It uses
   exactly the left-regular-band product mg-276d recorded as unused (its §8.3(6)).**
   **Scope, stated in the same breath, and it is a sharper statement than an untested corner
   (repaired here — F1).** `Δ_AT` is **not** in that family on any poset tested with `|L(P)| ≥ 5`
   (§9.4 — proven for 55 of 63 posets at `n = 5`, including every antichain `n ≥ 3`). Where it **is**
   in that family, membership is worthless: the positive class contains the **infinite** family `V_k`
   (the ordinal sum of `k` two-element antichains, `n = 2k`, `|L(P)| = 2^k` unbounded), on which the
   AT graph is the hypercube `Q_k` and `Δ_AT` is therefore the hypercube Laplacian — a sum of `k`
   commuting terms, **already diagonal by inspection**. So the honest scope clause is not "undecided
   below `|L(P)| ≤ 4`" but: **the semigroup technique reaches `Δ_AT` only where `Δ_AT` is already
   free.** It buys no bound on the bridge quantity anywhere, and that is now known rather than
   untested.

**The honest net.** The face side is not a change of coordinates with nothing attached — claim 3 is
a real technique, and it is new to *this programme*. **It is an import, correctly attributed, not a
discovery (F9):** it is Brown's theorem instantiated to a band, and the sharpest concrete instance
(control P4, the Tsetlin library) is the antichain case, i.e. a classical theorem. Nor is it *Hodge*:
its hypothesis is about the monoid of `P`-compatible ordered partitions, and it uses no complex, no
boundary map, no Laplacian and no "relative" (F9, §1). But it does not act on `Δ_AT` — and after F1
we know *why* rather than merely *where*: it reaches `Δ_AT` only on a family where `Δ_AT` is already
diagonal. And the technique that *does* act on `Δ_AT` is provably exponentially weak on the one
family where both sides can be evaluated exactly. **If `A(P)` is built, the case for it is claim 3,
not claim 2 — and it is not a route to `λ₂(Δ_AT)`.** §12 says what that changes about scoping.

**What is *not* claimed.** Not that no Hodge-theoretic technique can ever help — §6's result is
about *product-form link bounds* (the shape shared by Garland, Kaufman–Oppenheim, Alev–Lau and
ALOV), and it is stated that way in the ledger. Not anything about BK. Not anything about weighted
or normalised chains. Not that `A(P)` should or should not be built — that routing is
pm-onethird's.

---

## §1 — What "technique" is being tested, and how

An identity between two descriptions of one matrix transfers every *statement* and no *method*. So
"does the Hodge side carry technique" has to be made operational, and the test used here is:

> **A technique lives on the Hodge/face side iff its hypothesis is a statement about an object that
> has no presentation in the adjacent-transposition graph, and its conclusion is a statement about
> `L(P)`.**

Under that test the candidate techniques divide cleanly.

| candidate | hypothesis is about | graph-side presentation? | verdict |
|---|---|---|---|
| `spec≠0(∂*∂) = spec≠0(∂∂*)` in top degree | facets and ridges | **yes** — ridges are edges | §7: it *is* the incidence identity |
| Garland / local-to-global | **links** of faces of dim `≤ d−2` | **no** | §5–§6: applies, exponentially lossy |
| isotypic decomposition of `Ind_{S_α}^{S_n}1` | an `S_n`-action on the face space | — | §8: the action does not exist |
| Brown's theorem for left regular bands | the **semigroup product** on faces | **no** | §9: applies, exact spectra |
| higher faces "record braid relations" | codim-2 **links** | **no** | §4: PROVEN, and it is what caps §6 |

Nothing here computes `λ₂(Δ_AT)` a second way and calls the agreement evidence. Every comparison is
between a bound or a formula produced on one side and a quantity computed independently on the
other.

**⚠️ F9 — this test is too weak to carry the word "Hodge", and that changes what the positive is
(added in repair of mg-86a3's primary value press; the finding is FRAMING, not broken mathematics).**
The test above is a test for *"not the AT graph"*, not a test for *"Hodge"*. The Bruhat order,
descent statistics, coupling, strong stationary duality and Diaconis–Saloff-Coste comparison all pass
it. Applied to claim 3 it returns YES — but the hypothesis of Brown's theorem is about **the monoid
of `P`-compatible ordered partitions under refinement**, and nothing simplicial is used: not the
order complex, not a boundary map, not a Laplacian, not the pseudomanifold property, not "relative",
not `E`. It is the face semigroup of the braid arrangement restricted to the order cone `C_P` — an
object the source's own *Universal Picture* lists **separately** from the compatible face complex,
and one definable from `P` in a single line. So the sharp answer to the ticket's question is:
**claims 1, 2 and N2 are negatives (all three confirmed), and the positive is not Hodge and does not
need the face complex.** §0 and §12 already say "the face SEMIGROUP is where the technique actually
is" and §14 capitalises SEMIGROUP, which is why this is a framing finding rather than a broken claim
— but §1's test is what licenses answering the headline YES at all, so the reader who stops at the
headline must be told: **the semigroup carries technique; the Hodge side does not.** The
decision-relevant consequence is in §12.

---

## §2 — Theorem D: the adjacent-transposition walk *is* the down-up walk on `F(P)`

This is what licenses the import in §5. The bridge of mg-276d is an identity of *matrices*; the
high-dimensional-expander machinery is stated for a specific *walk* on the facets of a complex, so
the identity has to be upgraded before any of it can be quoted.

**The standard down-up walk `P_du` on a pure `d`-complex.** From a facet `σ`, choose one of its
`d+1` ridges uniformly, then choose uniformly among the facets containing that ridge.

> ### Theorem D — PROVEN, every finite poset
> ```
> I − P_du  =  Δ_AT / (2(n−1))
> ```
> so `gap(P_du) = λ₂(Δ_AT)/(2(n−1))`, and the down-up walk on the facets of `F(P)` is the lazy
> adjacent-transposition walk on `L(P)`.

*Proof.* `F(P)` is pure of dimension `d = n−2` with facets `L(P)` (mg-276d Lemma 2), so each facet
has `n−1` ridges, and every ridge lies in one or two facets (mg-276d Lemma 3(a)). By
mg-276d Lemma 3(b) the ridge `ρ_t(σ)` lies in two facets iff `τ_t` is legal at `σ`, and then the
second facet is `σ·s_t`. Hence for `τ = σ·s_t`, `P_du[σ,τ] = 1/(2(n−1))`, distinct `t` giving
distinct `τ`; and
`P_du[σ,σ] = ((n−1−deg σ) + deg σ/2)/(n−1) = 1 − deg σ/(2(n−1))`.
Subtracting from `I` gives `(D−A)/(2(n−1)) = Δ_AT/(2(n−1))`. ∎

*Verified independently:* exact rational check, **all 405 posets `n ≤ 6`**, 405/405
(`theorems_output.txt` §D; 317 of them with `|L(P)| ≥ 2`). The check builds `P_du` from ridge
incidence only — no words, no transpositions — and compares against `Δ_AT` built from words only.

**This also answers the ticket's question 2 in one direction.** The boundary correction is not an
extra object: **the free ridges are exactly the part of the holding probability that the boundary
contributes** — `L^abs − L^rel = diag(#forbidden)` is, in walk terms, the laziness. (**F8, corrected
here:** the earlier wording read *"the free ridges are exactly the holding probability"*, and that is
false as an identification — the proof one line above gives
`P_du[σ,σ] = ((n−1−deg σ) + deg σ/2)/(n−1)`, i.e. the free ridges **plus half the interior ones**.
The intended content is the sentence that follows it and is unaffected.) §4 gives the other, sharper
half of the answer.

---

## §3 — Theorem L: localisation — links are joins of induced-subposet complexes

The ticket's question 1 asked whether the grading by quotient complexity gives a decomposition the
graph presentation does not. It gives this:

> ### Theorem L — PROVEN, every finite poset
> Let `σ = (I_1 ⊊ … ⊊ I_j)` be a face of `F(P)`, with `I_0 = ∅`, `I_{j+1} = P`, and let
> `Q_i = P|_{I_{i+1}∖I_i}` be the induced subposets on the blocks of the ordered partition `σ`.
> Then
> ```
> link_{F(P)}(σ)  ≅  F(Q_0) * F(Q_1) * … * F(Q_j)                 (simplicial join)
> ```
> with the convention that a block of size 1 contributes the empty complex. Consequently the
> induced (facet-count) weights on the link are the product weights, and the weighted link depends
> only on the multiset of **isomorphism types of the induced subposets on the blocks**.

*Proof.* By mg-276d Lemma 1, `F(P) = Δ(J(P)∖{∅,P})`, so a face is a chain of proper nonempty
ideals and `link(σ)` consists of the chains `τ` with `σ ⊔ τ` again a chain — i.e. each vertex of
`τ` lies strictly between two consecutive `I_i`, with no constraint across different gaps. Hence
`link(σ) = Δ((I_0,I_1)) * … * Δ((I_j,I_{j+1}))` with `(I,I')` the open interval in `J(P)`.
And `[I,I'] ≅ J(P|_{I'∖I})`: the map `K ↦ K∖I` is an inclusion-preserving bijection from the ideals
of `P` between `I` and `I'` to the ideals of `P|_{I'∖I}` — if `K` is an ideal then so is `K∖I` in
the induced poset; conversely if `S` is an ideal of `P|_{I'∖I}` and `x <_P y ∈ I ∪ S`, then either
`y ∈ I` (so `x ∈ I`) or `y ∈ S ⊆ I'`, whence `x ∈ I'` (as `I'` is an ideal) and either `x ∈ I` or
`x ∈ S`. So `Δ((I,I')) = F(P|_{I'∖I})`. The weight statement follows because the facets of `F(P)`
containing `σ` are in bijection with `∏_i L(Q_i)` and the measure on facets is uniform. ∎

*Verified independently:* `theorems_output.txt` §L checks the claimed map as a **simplicial
isomorphism** — bijection on vertices onto `⊔_i {proper ideals of Q_i}`, forward preservation of
faces, and equality of the two face counts (the join's `f`-vector is the convolution of the
factors') — for **every face of every poset with `n ≤ 5`: 6197 faces, 0 failures.** Positive control
P5 additionally confirms the *spectral* content: links with the same block-type multiset have the
same `λ₂`, with the memo disabled and every link recomputed (`n ≤ 5`, 97 distinct keys, 0 clashes).

**Is this a decomposition the graph side lacks?** The *decomposition* is shared: the linear
extensions refining a fixed compatible ordered partition are `∏_i L(Q_i)`, and the AT moves that
preserve the partition are the within-block ones, so the induced subgraph is the Cartesian product
of the blocks' AT graphs. What the graph side lacks is not the decomposition but the **inequality
that consumes it** — a theorem whose hypothesis is the *link spectra*. That is what §5 tests.

---

## §4 — Theorem H: codimension-2 links are exactly five graphs

The ticket's question 4 asked for a statement about `L(P)` *proved* using a higher face. Here it
is, and it is also the mechanism behind §6.

> ### Theorem H — PROVEN, every finite poset
> Let `σ` be a face of `F(P)` of codimension 2 (dimension `n−4`). Then `link(σ)` is one of exactly
> five graphs, determined by the block types, with the weighted second eigenvalues shown:
>
> | link | block types (non-singleton blocks) | `λ₂` | reading in `L(P)` |
> |---|---|---|---|
> | `C_6` | one block `≅ A_3` | **1/2** | the **braid hexagon** `s_t s_{t+1} s_t = s_{t+1} s_t s_{t+1}` |
> | `C_4` | two blocks `≅ A_2` | 0 | **two commuting moves** `s_t s_u = s_u s_t`, `\|t−u\| ≥ 2` |
> | `P_4` | one block `≅ A_1 ⊔ C_2` | **1/2** | the hexagon with two facets deleted by the boundary |
> | `P_3` | `A_2 ⊔ C_2`, or one block `≅ V` or `Λ` | 0 | the square, or the hexagon, further truncated |
> | `P_2` | `C_2 ⊔ C_2`, or one block `≅ C_3` | −1 | a single edge: one legal move left |
>
> In particular `λ₂(link σ) ≤ 1/2` at codimension 2, attained exactly at `C_6` and `P_4`.

*Proof.* A codimension-2 face has `n−2` blocks summing to `n`, so either one block of size 3 and
the rest singletons, or two blocks of size 2 and the rest singletons. By Theorem L the link is
`F(Q)` for the one 3-element block, or `F(Q_1) * F(Q_2)` for the two 2-element blocks. There are
five posets on three elements and two on two elements, so the list is a finite check:
`F(C_3) = P_2`, `F(A_3) = C_6`, `F(V) = F(Λ) = P_3`, `F(A_1 ⊔ C_2) = P_4`; `F(A_2) =` two points and
`F(C_2) =` one point, whose joins are `C_4`, `P_3`, `P_2`. The weights are the product weights of
Theorem L, and the five weighted graphs have the stated `λ₂` (`C_m: cos(2π/m)`, `P_m: cos(π/(m−1))`,
with the induced weights coming out uniform on each; positive control P2 checks these closed
forms). ∎

*Verified independently:* `theorems_output.txt` §H enumerates every codimension-2 link of every
poset with `4 ≤ n ≤ 6` — **44 055 links, exactly the five types, exactly the stated block types and
`λ₂` values, nothing else.**

**This is the source's claim (4), proven and made quantitative.** The sketch says the higher faces
"record commuting moves, braid relations, and local factorisation structure". At codimension 2 that
is literally true and it is the complete list: the square *is* commutation, the hexagon *is* the
braid relation, and `P_4/P_3/P_2` are those two pictures truncated by the boundary. And it is not
decoration — the `1/2` in the `C_6` and `P_4` rows is exactly the number that §6 shows to be fatal.

**This also completes the answer to question 2.** The boundary correction does more than supply
laziness: it *truncates* the codimension-2 pictures, and truncation **lowers** `λ₂`
(`C_6: 1/2 → P_4: 1/2 → P_3: 0 → P_2: −1`). So the forbidden generators are the only thing that can
push local expansion below `1/2` — which is real structure, and §5 shows it is not enough (the
fence family has `γ_{−1} < 1/2` and is still exponentially far off).

---

## §5 — The measurement: the link bound against the truth

**The statement used, CITED not proved here.** For a pure `d`-dimensional weighted simplicial
complex, write `γ_i = max{ λ₂(1-skeleton of link σ) : dim σ = i }` for `−1 ≤ i ≤ d−2`. Then
```
gap(P_du)  ≥  (1/(d+1)) · ∏_{i=−1}^{d−2} (1 − γ_i).
```
(Alev–Lau 2020, refining Kaufman–Oppenheim and Dinur–Kaufman; the `γ ≤ 0` case is
Anari–Liu–Oveis Gharan–Vinzant.) With `d = n−2` and Theorem D this reads

```
                 λ₂(Δ_AT)  ≥  2 · ∏_{i=−1}^{n−4} (1 − γ_i) .                          (LG)
```

Because the inequality is cited rather than re-derived, `run_sweep.py` **checks it** on the whole
population; a violation would void the measurement.

### §5.1 Non-vacuity is not an accident — PROVEN

Every link of dimension `≥ 1` is connected, so `γ_i < 1` and **(LG) is strictly positive for every
finite poset.** *Proof.* By Theorem L a link of dimension `≥ 1` is either a join of two nonempty
complexes (connected) or `F(Q)` for a single block with `|Q| ≥ 3`; and `F(Q)` is connected for
`|Q| ≥ 3` — given incomparable proper nonempty ideals `I, J` with `I ∩ J = ∅` and `I ∪ J = P`, one
of them has `≥ 2` elements, say `I`, and then `I ⊋ I∖{max}` and `I∖{max} ⊂ (I∖{max}) ∪ J ⊊ P` give
a path `I — I∖{max} — (I∖{max})∪J — J`; all other pairs are joined through `I ∩ J` or `I ∪ J`. ∎
So the technique never degenerates to "bound = 0". It fails for a different reason.

### §5.2 The full population, `2 ≤ n ≤ 6`

Every poset up to isomorphism (A000112-checked by the mg-276d instrument). `truth` is
`λ₂(Δ_AT)` by Lanczos on a rank-one-shifted operator; `bound` is (LG).

| `n` | posets | (LG) violations | `max γ_i` over all levels and posets | truth/bound: min / median / max |
|---|---|---|---|---|
| 2 | 2 | 0 | — (no level exists) | 1.0000 / 1.0000 / 1.0000 |
| 3 | 5 | 0 | 0.500000 | 1.0000 / 1.0000 / 1.0000 |
| 4 | 16 | 0 | 0.500000 | 1.0000 / 1.1716 / 1.3333 |
| 5 | 63 | 0 | 0.500000 | 1.0000 / 1.6000 / 1.8127 |
| 6 | 318 | 0 | 0.500000 | 1.0000 / 2.3290 / 2.6204 |

- **(LG) is never violated** — the cited form is correct on this population.
- **`γ_i ≤ 1/2` on all 404 posets, never exceeded, and attained at some level by 373 of them.**
  The 29 posets with every `γ_i < 1/2` are narrow ones (the smallest is `0<1 0<2`); by Theorem H
  the codimension-2 level is `< 1/2` exactly when no gap of any codimension-2 face carries an
  induced `A_3` or `A_1 ⊔ C_2`.
- **The bound is remarkably tight at these sizes** (worst factor `2.62` at `n = 6`) and the ratio
  grows monotonically with `n`. §5.3 and §6 say what it grows *like*.

### §5.3 Three families, pushed further

The antichain, where the truth is known in closed form:
`λ₂(Δ_AT(A_n)) = 2 − 2cos(π/n)`. This is Aldous' spectral-gap conjecture for the path graph, proved
by **Caputo–Liggett–Richthammer (2010)** — the interchange process on a graph has the same gap as
the one-particle walk — and positive control P1 reproduces it from the Lanczos solver to `10^{-14}`
for `n ≤ 6`.

| `n` | `γ_i` at every level | (LG) bound | truth `2−2cos(π/n)` | ratio |
|---|---|---|---|---|
| 3 | 1/2 | 1.000000 | 1.000000 | 1.00 |
| 4 | 1/2, 1/2 | 0.500000 | 0.585786 | 1.17 |
| 5 | 1/2 ×3 | 0.250000 | 0.381966 | 1.53 |
| 6 | 1/2 ×4 | 0.125000 | 0.267949 | 2.14 |
| 8 | 1/2 ×6 (§6: `≥ 1/2` PROVEN) | 3.125e−02 | 0.152241 | 4.9 |
| 12 | 1/2 ×10 (§6: `≥ 1/2` PROVEN) | 1.953e−03 | 0.068148 | 34.9 |
| 20 | 1/2 ×18 (§6: `≥ 1/2` PROVEN) | 7.629e−06 | 0.024623 | 3227 |
| 40 | 1/2 ×38 (§6: `≥ 1/2` PROVEN) | 7.276e−12 | 0.006165 | 8.5e+08 |

Rows `n ≥ 8` are **not extrapolation of a trend**: §6 proves `γ_i ≥ 1/2` at every level for every
`n`, so `bound ≤ 2^{3−n}` is a theorem, and the truth is a cited theorem. The `γ_i = 1/2` *equality*
is computational (`A_3…A_9`, extended from `A_3…A_7` by mg-86a3), so the bound column for `n ≥ 12` is
an **equality value standing in for a proven upper bound** — the direction the negative needs.
(**F5**: only the `n = 8` row carried the PROVEN marker before this repair, while §13 asserted all
four did; the three markers are added rather than the sentence weakened, because the mathematics
supports them.)

Two width-2 families, to test whether removing the braid hexagon helps:

| family | `n` | `\|L(P)\|` | `γ_i` | bound | truth | ratio |
|---|---|---|---|---|---|---|
| `C_a ⊔ C_a` | 4 | 6 | 0.500, 0.500 | 0.500000 | 0.585786 | 1.17 |
| | 6 | 20 | 0.500 ×4 | 0.125000 | 0.267949 | 2.14 |
| | 8 | 70 | 0.500 ×6 | 0.031250 | 0.152241 | 4.87 |
| fence `0<1>2<3>…` | 4 | 5 | 0.333, 0.500 | 0.666667 | 0.829914 | 1.24 |
| | 5 | 16 | 0.407, 0.500, 0.500 | 0.296512 | 0.488390 | 1.65 |
| | 6 | 61 | 0.442, 0.500 ×3 | 0.139510 | 0.319444 | 2.29 |
| | 7 | 272 | 0.460, 0.500 ×4 | 0.067501 | 0.226161 | 3.35 |

**Removing the hexagon does not help.** `C_a ⊔ C_a` has no 3-antichain at all, and still has
`γ_i = 1/2` at every level — supplied by the `P_4` row of Theorem H (an element incomparable to a
2-chain) and by the larger single-block links. The fence pushes the *bottom* level down to `0.46`
and the product still decays geometrically. **`γ = 1/2` is not about antichains; it is about `F(P)`.**

---

## §6 — Theorem G: why — `γ = 1/2` is the trickling-down fixed point

> ### Theorem G — PROVEN, every `n ≥ 3`
> For the antichain `A_n` and every level `−1 ≤ i ≤ n−4`, `γ_i ≥ 1/2`. Consequently the (LG) bound
> for `A_n` satisfies
> ```
> 2 · ∏_{i=−1}^{n−4}(1 − γ_i)  ≤  2 · (1/2)^{n−2}  =  2^{3−n},
> ```
> while `λ₂(Δ_AT(A_n)) = 2 − 2cos(π/n) = Θ(n^{−2})` — so the technique is off by `2^{Θ(n)}`.

*Proof.* Fix `i` with `−1 ≤ i ≤ n−4` and let `m = n − i − 1 ≥ 3`. Take the face `σ` of dimension
`i` whose blocks are one block of size `m` and `i+1` singletons; by Theorem L,
`link(σ) ≅ F(A_m)`, the Coxeter complex of `S_m`, whose 1-skeleton has vertex set the proper
nonempty subsets `S ⊆ [m]` with induced weight `w(S) = |S|!(m−|S|)!`.

The 1-skeleton walk from `S` is: pick a uniform maximal chain through `S` — equivalently a uniform
ordering of `S` followed by a uniform ordering of its complement — then output the prefix of a
uniform length `k ∈ [m−1] ∖ {|S|}`. Let `a ∈ ℝ^m` with `Σ_i a_i = 0`, `a ≠ 0`, and set
`f(S) = Σ_{i ∈ S} a_i`. Writing `s = |S|`:

- for `k < s`, the prefix is a uniform `k`-subset of `S`, so `E[f] = (k/s) f(S)`;
- for `k > s`, the prefix is `S` plus a uniform `(k−s)`-subset of the complement, so
  `E[f] = f(S) + ((k−s)/(m−s)) f(S^c) = f(S)(m−k)/(m−s)`, using `f(S) + f(S^c) = Σ_i a_i = 0`.

Hence
```
(Pf)(S) = (1/(m−2)) [ Σ_{k<s} k/s + Σ_{k>s} (m−k)/(m−s) ]  f(S)
        = (1/(m−2)) [ (s−1)/2 + (m−s−1)/2 ] f(S)  =  f(S)/2 ,
```
independently of `S`. And `f` is orthogonal to the constants for the stationary weights: by the
`S_m`-symmetry of `w`, `Σ_S w(S) f(S) = (Σ_i a_i)·Σ_{S ∋ 1} w(S) = 0`. So `1/2` is an eigenvalue of
the link's 1-skeleton walk on the complement of the constants, giving `λ₂(link σ) ≥ 1/2`, hence
`γ_i ≥ 1/2`. ∎

*Verified independently:* `theorems_output.txt` §G evaluates `(Pf)(S) − f(S)/2` in **exact
rational arithmetic** on the 1-skeleton built by the brute-force link code, for `A_3 … A_8`
(1-skeletons of 6 … 254 vertices): **identically 0**. The dense solver additionally confirms
`λ₂ = 1/2` exactly — i.e. that `1/2` is the *second* eigenvalue and not merely an eigenvalue — for
`A_3 … A_7`; at `A_8` the dense solver is capped and only the eigenfunction is checked. For the
theorem as stated only `≥` is needed, and that is the half that is proved.

**✅ CONFIRMED BY INDEPENDENT REBUILD — mg-86a3, and this is the audit's largest single result.** §13
below names this proof as the one thing an auditor must rebuild from scratch, because no independent
code path in `code/hodge_leverage/` re-derives it. The auditor did rebuild it, twice over and with
**no shared link code**: the eigenfunction re-derived **by hand** from the definition of the Coxeter
complex (including the closed form `w(S) = |S|!(m−|S|)!`, checked against brute-force facet counting
for `m = 3..7`), and `Pf = f/2` re-verified in exact rational arithmetic for **`A_3 … A_12`** under
**three** different `a`-vectors, with `λ₂ = 1/2` exactly for **`A_3 … A_9`**
(`code/hodge_leverage_audit_86a3/audit_theoremG.py` → `out_theoremG.txt`). That is four orders of `n`
past `A_8` for the identity and past `A_7` for row G′. The audit's finding: *"the proof is complete,
`n`-free, and uses `m ≥ 3` exactly where `i ≤ n−4` supplies it"* — **so `M2`'s `2^{Θ(n)}` loss is a
theorem**, and the `A_3…A_8` computation above is a check on a proof rather than its support, as
claimed. The audit also **endorses the restraint** in not upgrading the *equality* `γ_i = 1/2`:
nothing downstream needs it (M2 uses only `≥`, and a smaller `γ` only strengthens the negative), and
the auditor likewise found no easy proof of `≤ 1/2` — trickling-down at the fixed point returns `1`
and gives nothing.

**⚠️ Step 4b, from the same audit, adopted here by mg-a806 — and STRUCK by mg-a2bd, because the
strengthening it proposed is FALSE.** The adopted sentence read: *Theorem G is weaker than its own
proof, because the proof uses only that some block induces an antichain of size `≥ 3`; the immediate
strengthening, free from G plus Theorem L, is `γ_i ≥ 1/2` for every finite poset having a dimension-`i`
face one of whose blocks induces an antichain of size `≥ 3`* — recorded as ledger row **G″**. **It is
false.** It fails on **55 (poset, level) pairs at `n ≤ 6`**, the smallest at `n = 5`; the per-face
reading its own sentence argues fails on **3901 of 7989** faces (mg-d39d §2, `out_gpp.txt`;
independently reproduced by `code/hodge_leverage_join/out_verify_join.txt` J2). Row **G″** is struck.

**And the reason is worth more than the row was: THE STRENGTHENING WAS NOT FREE — the dropped
hypothesis was the one doing the work.** Theorem G's face has one block of size `m` and `i+1`
**singletons**. A singleton block contributes no factor to Theorem L's join (`F(A_1)` is the empty
complex), so `link(σ) ≅ F(A_m)` *on the nose* — **in Theorem G's case the link is not a join at all**,
and the eigenfunction applies to `F(A_m)` directly. Drop the singleton requirement — which is exactly
what G″ did — and Theorem L gives a **genuine join** `F(A_m) * Y`. Joins **suppress** `λ₂`: an
eigenfunction of a factor survives into the join scaled by `p/(p+q+1) < 1`, so **an exact `1/2` in a
factor becomes STRICTLY LESS than `1/2` in the join**. That is Theorem J, §6.1 below. It is not a
boundary case: nearly half the faces G″ quantified over are counterexamples, and the four at `n = 5`
are `A_3 ⊕ A_2`, `A_3 ⊕ C_2`, `A_2 ⊕ A_3`, `C_2 ⊕ A_3` — all ordinal sums, i.e. **exactly the posets
where the face's other block is not a singleton and the link is therefore a genuine join.**

**Sized in the other direction, and this is not optional. THEOREM G STANDS, UNTOUCHED.** Its face has
singleton blocks by construction, `m ≥ 3` comes from `i ≤ n−4`, and mg-86a3 rebuilt it to `A_12` with
no shared link code. The `2^{Θ(n)}` loss remains a theorem, the headline remains carried, and
**nothing in §0, §5, §6's conclusion, M2, the routing or `STATE.md` ever depended on G″** — the struck
row's own last clause, *"Nothing here consumes it"*, was accurate, which is what keeps this a strike
rather than a retraction. Joins moreover only **suppress** `γ`, which makes the local-to-global bound
**weaker** on the affected posets, never stronger: nothing about the `A(P)` decision is reopened by
this. The one thing G″ was reached for it never covered anyway — §5.3's `C_a ⊔ C_a` has no
3-antichain at all.

**Everything G″ was cited by, enumerated rather than assumed (mg-a2bd).** A false universal that sat in
a ledger may have been leaned on, so the repository was swept for the row label in every form, for the
phrase *"free from G + Theorem L"*, and for the claim's **content** (*"antichain of size ≥ 3"*,
*"weaker than its own proof"*, *"strongest true form"*). **Three sites, all now carrying the strike, and
no consumer anywhere:**

| site | what it was | disposition |
|---|---|---|
| this §6, the step-4b paragraph | the sentence, adopted by mg-a806 | **STRUCK** above |
| the ledger, row **G″** | the `PROVEN` row | **STRUCK**, with row **J** recording why and row **G‴** the true form |
| `docs/OneThird-Hodge-Side-Leverage-IndependentAudit.md:413` | mg-86a3's step-4b strength-check cell — the **origin** of the sentence | **ANNOTATED** in place; the auditor's text is left verbatim as the record, with the refutation beside it |

**And the clean negative, stated because it is a real result and not an assumption: NOTHING CITED IT.**
No proof, bound, ledger row, §0 point, §12 routing consequence, §14 row, `STATE.md` row, code path or
committed artifact consumes G″ or the phrase *"free from G + Theorem L"*. `STATE.md` never contained
the row at all — its mg-a3d4 attempt-index row was searched in full for the label and for the claim's
content and carries neither. So the blast radius really is the two sites in this document plus
the one annotation, and the struck row's own *"Nothing here consumes it"* was **true when written**.

### §6.1 — Theorem J: joins suppress `λ₂`, and that is why G″ was not available

> **Theorem J (join suppression).** Let `X_1, …, X_r` be weighted pure complexes, `dim X_j = p_j ≥ 0`,
> and let `X = X_1 * ⋯ * X_r` carry the product weights, so `D := dim X = Σ_j (p_j + 1) − 1`. Then the
> spectrum of the 1-skeleton walk of `X`, on the complement of the constants, is exactly
> ```
>     ⋃_j { (p_j / D) · μ  :  μ ∈ spec(X_j on 1⊥) }   ∪   { −1/D, with multiplicity r − 1 }.
> ```
> In particular `λ₂(X) ≤ max_j (p_j/D)·λ₂(X_j)⁺ ∨ (−1/D)`, and since `p_j/D < 1` whenever a second
> factor is present, **a factor's `λ₂` is strictly suppressed by the join.**

*Proof.* A facet of `X` is a union of one facet from each factor, so it has `Σ_j(p_j+1) = D+1`
vertices. From a vertex `u ∈ X_j` the 1-skeleton walk picks a facet through `u` (weighted) and then a
uniform one of the `D` remaining vertices; exactly `p_j` of those lie in `X_j`, and conditioned on
landing there the step is `X_j`'s own 1-skeleton walk. So for `f` supported on `X_j` with
`⟨f, π_{X_j}⟩ = 0`, extended by `0`,
```
    (P_X f)|_{X_j} = (p_j/D) · (P_{X_j} f) ,        (P_X f)|_{X_k} = ⟨f, π_{X_j}⟩ = 0  (k ≠ j),
```
the second equality because from a vertex outside `X_j` the walk enters `X_j` at its stationary
measure, against which `f` integrates to zero. That accounts for `Σ_j(V_j − 1)` eigenvalues. The
remaining `r − 1` dimensions are spanned by the functions constant on each factor and summing to zero
across factors, on which the same computation returns `−1/D`. Counting: `Σ_j(V_j−1) + (r−1) = V − 1`. ∎

**Instantiated at the smallest counterexample.** `F(A_3) * F(A_2)` has `p = 1`, `q = 0`, `D = 2`, so
the hexagon's `1/2` lands at `(1/2)·(1/2) = 1/4`. That is `γ_0(A_2 ⊕ A_3)`, and the deliverable's own
`local_to_global.gammas` returns `{−1: 1/6, 0: 1/4, 1: 1/2}` on that poset — **the instrument that
carries §5 already said G″ was false.**

*Verified independently:* `code/hodge_leverage_join/verify_join.py` → `out_verify_join.txt`. The link
side is measured by `links.link_skeleton`, which builds the weighted 1-skeleton by brute force from
the facet list and **never uses Theorem L**; the factor side is assembled from the factor complexes
`F(P|_B)` alone. On **all 48 846 genuine-join links of all 405 posets `n ≤ 6`** (a genuine join = at
least two non-singleton blocks) the two **full spectra** agree, `0` mismatches, worst deviation
`1.2 × 10⁻¹⁵`. This is a check on a proof, not its support — and it is a **replication**, not a
control: no mutation is scored anywhere in that file, and §10's control table is unchanged by it.

#### The second consequence: `γ_i` for `A_n` is attained at the one-big-block face, and that is what row G′ needed

`γ_i` is a **max over every dimension-`i` face**, while `out_theoremG.txt`'s `G3` computes the spectrum
of the link of **one** face — Theorem G's. mg-a806 widened row **G′** from `A_7` to `A_9` on that
per-link computation, i.e. **on evidence one notch narrower than the statement** (mg-d39d A8(3)). The
repair is not to narrow the row; it is to write the missing step down, and Theorem J *is* the missing
step. **Do not weaken G′: it is true as stated, and the one-big-block case is exactly where it lives.**

A dimension-`i` face of `F(A_n)` is an ordered partition into `i+2` blocks of sizes `b_1,…,b_{i+2}`;
its non-singleton blocks satisfy `Σ_{b_j ≥ 2} (b_j − 1) = n − i − 2 = D + 1`, where `D = n−i−3` is the
link's dimension and depends only on the **level**. By L and J,
```
    λ₂(link σ)  =  max_j (b_j − 2)/D · λ₂(F(A_{b_j}))   ∨   (−1/D),
```
and `b_j − 2 ≤ D` with **equality iff that block is the only non-singleton one** — i.e. iff `b_j = n−i−1`
and the other `i+1` blocks are singletons, which is precisely Theorem G's face. Hence:

- **Unconditionally, every `n`:** `γ_i ≥ λ₂(F(A_{n−i−1})) ≥ 1/2`, the second inequality being Theorem G.
  This is the half M2 consumes and it is a theorem.
- **Given `λ₂(F(A_b)) ≤ 1/2` for `3 ≤ b ≤ n`** — the computational half, verified for `b ≤ 9` — every
  *other* dimension-`i` face has `λ₂(link) ≤ max_j (b_j−2)/(2D) < 1/2`, so **`γ_i = λ₂(F(A_{n−i−1})) = 1/2`
  exactly, attained at the one-big-block faces and at no others.**

So the per-link computation **does** bound every face at its level, and row G′'s population is exactly
as wide as its statement — once J is on the page. Checked both ways in `out_verify_join.txt` `J4`:
exhaustively over **all faces** of `F(A_n)` for `n = 3…6` (the argmax set is exactly the one-big-block
faces at every level, and the best non-conforming face is strictly below — `1/3` at `A_6`, `i = 0`),
and over **block-size multisets** for `n = 7, 8, 9` via L + J, with the `n ≤ 6` face-level agreement as
the control on that shortcut. The runner-up is always the two-non-singleton-block face and it climbs
toward `1/2` without reaching it: at `A_9`, `i = 0` it is `(2,7) ↦ 5/12`. What remains computational is
only the base case `λ₂(F(A_m)) ≤ 1/2` for `m ≤ 9`, recomputed here from the closed-form weights —
so G′ keeps its `PROVEN-by-computation` label and loses its unstated assumption.

**Why this is structural rather than a numerical accident.** Oppenheim's trickling-down theorem
propagates a link bound down one level as `γ ↦ γ/(1−γ)`. The map has fixed point exactly
`γ = 1/2`, where it returns `1` — no information. `F(P)` sits *at* that fixed point, at every
level, for essentially every poset (§5.2: `γ_i ≤ 1/2` on all 404, attained by 373). So this is not
"the constant in the theorem I quoted is loose": **the complex is at the exact value where the
local-to-global hierarchy carries no information, and any bound of the product form
`∏(1−γ_i)` over `Θ(n)` levels is therefore exponentially small.**

**And the reason it sits there is the pseudomanifold property.** By mg-276d Lemma 3(a) every ridge
of `F(P)` lies in at most two facets — which is exactly why "relative" is well-posed and why the
bridge exists at all. That same property forces every codimension-2 link to have maximum degree
`≤ 2`, i.e. to be a path or a cycle (Theorem H), and paths and cycles are the canonical
*non*-expanders. **The feature that makes the bridge work is the feature that blocks the technique.**
This is a description of the two facts and their common cause; it is labelled HEURISTIC in the
ledger, because "pseudomanifold ⟹ no product-form link bound can be useful" is not proved here in
that generality — what is proved is the antichain instance, Theorem G.

---

## §7 — Negative: the top two dimensions are graph theory verbatim

> ### Theorem N1 — PROVEN, every finite poset
> Let `N` be the signed vertex–edge incidence matrix of the adjacent-transposition graph on `L(P)`
> (one row per edge `{σ,τ}`, entries `+1` at `σ` and `−1` at `τ`). Then
> ```
> Δ_AT  =  E · L^rel_top(F(P)) · E  =  Nᵀ N ,
> ```
> and the twisted relative boundary map `∂_rel E` equals `N` up to a sign on each row.

*Proof.* `(∂σ)[ρ_t] = (−1)^{t−1}` for the ridge at index `t`. An interior ridge is shared by `σ` and
`τ = σ·s_t`, sits at index `t` in both (mg-276d §4), and `ε(τ) = −ε(σ)`. So the row of `∂E` at that
ridge is `(−1)^{t−1}ε(σ)·(e_σ − e_τ)ᵀ`. Scaling rows by `±1` does not change `MᵀM`, so
`(∂_rel E)ᵀ(∂_rel E) = NᵀN`; the left side is `E L^rel E` because `E` is a diagonal involution. ∎

*Verified independently:* `theorems_output.txt` §N1, **all 405 posets `n ≤ 6`**, 405/405 (317 with
at least one edge). The check builds `N` from the AT graph and `L^rel` from the simplicial complex,
with no shared code path.

**Consequence, and this is the negative.** `Δ_AT = NᵀN` is the classical incidence factorisation of
a graph Laplacian. The Hodge-theoretic move one dimension down, `∂*∂ ↝ ∂∂*`, is then
`NᵀN ↝ NNᵀ` — the classical edge/line-graph matrix, and the "Hodge duality" `spec≠0(∂*∂) =
spec≠0(∂∂*)` is the classical singular-value pairing between a graph Laplacian and its edge
version. Likewise the Hodge lower bound "`λ₂ ≥ 1/‖h‖²` for any cofilling `h`" is, under this
identification, the Dirichlet/flow duality that gives Poincaré and effective-resistance bounds.

**So every technique available from the top two dimensions of `F(P)` is a graph technique in
different notation.** This is the sharpest single thing this work item establishes about the
bridge, and it is what makes §5–§6 the decisive test rather than one experiment among many: it
proves that any new leverage must come from the faces *below* the top two dimensions, and §6 prices
the standard technique that lives there.

### §7.1 — F2: what is unconditional here, and what leans on L1

**The defect, stated plainly (mg-86a3's F2, MODERATE).** §13(iv) records that this document
**inherits** mg-276d's reading L1 of the word *"relative"* — which mg-276d itself labels
**CONDITIONAL**, because the source does not define it — and says that every statement here about
`L^rel` and about free ridges is conditional on it. That was correct in §13 and was **carried
nowhere else**: ledger row N1 was labelled flat **PROVEN**, row N1′ and row S1's condition list did
not mention L1, and neither did §14, whose opening line is *"carries its own conditions rather than
pointing at them"*. A conditional presented as proven in the text destined for `STATE.md` is exactly
mg-5630's defect class, so it is repaired rather than annotated.

**But the reconciliation is a strengthening, not a retreat, and the auditor settled it with a
computation rather than an opinion.** Split the theorem into the three statements it actually
contains:

| # | statement | label |
|---|---|---|
| **N1a** | `Δ_AT = NᵀN`, `N` the signed vertex–edge incidence matrix of the AT graph | **PROVEN, unconditional** — pure graph theory; nothing simplicial enters. 405/405 by the audit's disjoint route |
| **N1b** | `Δ_AT = E · L^rel_top · E` | **PROVEN given L1** — i.e. **CONDITIONAL**, inherited from mg-276d. 405/405 both here and by the audit |
| **N1c** | `∂_rel E = N` up to a sign per row (this section's own new clause) | **PROVEN given L1**; 405/405 by the audit, which also verified that the twisted signs at the two facets of every interior ridge are always opposite |

**And the conclusion — the negative, which is the operative content — does not inherit the
conditional at all.** The auditor verified on **all 405 posets `n ≤ 6`** that under the *other*
reading of "relative", namely no boundary quotient at all (the **absolute** top Laplacian), the
twisted operator is

```
    E · L^abs_top · E  =  (n−1)·I − A ,
```

the shifted adjacency matrix of the same adjacent-transposition graph (using `deg + #free = n−1`,
also verified 405/405; `code/hodge_leverage_audit_86a3/audit_robustness.py` → `out_robustness.txt`).
So: **relative reading ⟹ `Δ_AT = D − A`, a graph Laplacian; absolute reading ⟹ `(n−1)I − A`, a
shifted graph adjacency matrix. Under either reading the top-degree Hodge operator is a graph
object**, so N1′ — *"no technique using only facets and ridges can be new"* — and everything §5–§6
prices on top of it hold unchanged. **Only the equation is conditional; the pricing is robust to the
condition, and provably so.** That is a stronger position than the flat PROVEN label conveyed,
because the flat label invited the reader to discover the inherited condition and conclude the
conclusion was at risk with it.

---

## §8 — Negative: representation theory does not descend

The source's representation-theoretic section observes that a face with block sizes `α` has
stabiliser `S_α`, so faces sit inside the Young permutation module `Ind_{S_α}^{S_n} 1`. The ticket
asked whether the isotypic decomposition constrains the spectrum.

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

*Verified independently:* `theorems_output.txt` §N2 — over all posets with `n ≤ 5`, the number on
which **every** shape's face span is an `S_n`-submodule is exactly **1 at each `n`, and it is the
antichain**.

**And where the symmetry *is* present, it still does not diagonalise.** For the antichain
`L(P) = S_n` and the full `S_n`-action is available — but `Σ_i s_i` is **not central** in `C[S_n]`
for `n ≥ 3`, since `{s_1,…,s_{n−1}}` has `n−1` elements while the conjugacy class of transpositions
has `\binom{n}{2}`. Characters therefore do not give the spectrum of `Δ_AT` even in the fully
symmetric case — which is the historical reason the antichain gap needed Aldous' conjecture and its
Caputo–Liggett–Richthammer proof rather than a character computation. So candidate 3 of the ticket
fails twice: the symmetry is absent off the antichain, and inert on it.

The one thing representation theory does give is eigenvalue interlacing: `Δ_amb = (n−1)I − A` is a
compression of the ambient `Σ_i(1−s_i)`, so its spectrum lies in the ambient range `[0, 2(n−1)]`.
That is true and says nothing about `λ₂`.

---

## §9 — Positive: the face semigroup gives exact spectra

This is the one place where the face side supplies a method the graph side does not have. It uses
the left-regular-band product — the piece mg-276d explicitly recorded as unused.

### §9.1 `F(P)` is a left regular band, and its support lattice is the acyclic partitions

Write a face as an ordered partition `x = (B_1,…,B_k)` (`k = 1` is the identity face `(P)`), and
define the product by successive refinement: `x·y = (B_i ∩ C_j)` ordered lexicographically by
`(i,j)`, empty blocks dropped.

**Closure.** If `x,y` are `P`-compatible then so is `x·y`: for `a <_P b`, either `x` already
separates them in the right order, or they share an `x`-block and `y` orders them correctly.
**Band axioms.** `x·x = x`, `x·y·x = x·y`, associativity, and `(P)` is a two-sided identity.
**Support.** `supp(x)` = the underlying set partition; `supp(x·y) = supp(x) ∨ supp(y)` where the
join is the common refinement, so the support lattice is ordered by *reverse* refinement
(coarsest = `⊥ = (P)`, finest = `⊤ =` all singletons). The set of supports is exactly the set of
partitions `π` with `P/π` acyclic — the object the source names.

*Verified independently:* `lrb_output.txt` §1–2. Over all posets with `n ≤ 5`: **0 band-axiom
violations** (closure, idempotence, `xyx = xy`, identity), **0 associativity violations** (`n ≤ 4`,
the triple loop), and **supports == acyclic partitions on 87/87 posets**, join-closed on 87/87.
(Note that the acyclic partitions are *not* closed under refinement: for `P = {a<c, b<d}` the
partition `{a,d}|{b,c}` refines the acyclic one-block partition and is cyclic. So `L_P` is a lattice
for the reverse-refinement order and the join is the common refinement, not a sublattice of the
partition lattice under refinement.)

### §9.2 Brown's theorem, instantiated

**CITED** (Brown 2000, *Semigroups, rings, and Markov chains*; Bidigare–Hanlon–Rockmore for the
braid arrangement). For a probability `w` on `F(P)`, the walk on chambers `c ↦ x·c` with `x ~ w`:

> ```
> eigenvalues     λ_X = Σ_{y : supp(y) ≤ X} w(y),      X an acyclic partition of P,
> multiplicities  m_X determined by  Σ_{Y ≥ X} m_Y = ∏_{B ∈ X} |L(P|_B)|,
> and the transition matrix is diagonalisable.
> ```

Two things to notice. The eigenvalues are an explicit *linear* function of `w` — no matrix is
diagonalised. The multiplicities **do not depend on `w` at all**: they are an invariant of `P`,
obtained by Möbius inversion over the acyclic-partition lattice, and the right-hand side
`∏_B |L(P|_B)|` is the same product over induced subposets that Theorem L produced. The two
localisations are the same localisation.

### §9.3 Verified against the actual matrix

`run_lrb.py` builds the transition matrix from the semigroup action, builds the predicted
`(λ_X, m_X)` from the lattice, and then compares by **exact rank computations**: for every distinct
predicted eigenvalue `Λ`, `dim ker(M − ΛI)` must equal the summed predicted multiplicity, and the
dimensions must add to `|L(P)|` — which also certifies diagonalisability.

- **Multiplicities**: nonnegative integers summing to `|L(P)|` on **all 405 posets `n ≤ 6`**.
- **Spectrum, exact rational ranks**: correct and diagonalisable on **all 24 posets with `n ≤ 4`,
  under three weight families** — a generic `w` on all faces, `w` on two-block faces only, and `w`
  on the `({i}, rest)` faces. Three families, so the check is not only on a generic `w`.
- **Spectrum, mod-`p` ranks (`p = 2^31−1`)**: `A_5` (`|L| = 120`, 52 acyclic partitions, 52 distinct
  eigenvalues), the fence at `n = 5`, `C_2 ⊔ C_3`, `V ⊔ A_2`, and the chain — correct and
  diagonalisable on all five. `A_6` (`|L| = 720`) was **skipped**, and it is said here rather than
  left to be noticed: the exact-rank budget does not reach it.
- **Positive control P4** is the sharp one: for the antichain with `w` on the `({i},rest)` faces the
  walk is the **Tsetlin library**, whose spectrum is classical — eigenvalue `Σ_{i∈S} w_i` with
  multiplicity `D(n−|S|)`, the derangement number. The Brown machinery reproduces it exactly for
  `n = 2,…,5`, and neither derangements nor subset-indexing appear anywhere in `lrb.py`.

### §9.4 Scope: this family reaches `Δ_AT` only where `Δ_AT` is already free

*(Heading corrected in repair of **F1**. It previously read "`Δ_AT` is *not* in this family", which is
false as a universal — see the F1 block below, where the replacement is given and is stronger. The
committed artifact `lrb_output.txt` §5 carries the same correction at its own site.)*

Stated with the positive result, not after it.

Any Brown walk supported inside the adjacent-transposition graph must put all its weight on faces
`x` with `x·c ∈ {c} ∪ N_AT(c)` for **every** chamber `c` — weights are nonnegative, so one bad `c`
disqualifies `x`. If, among those candidate faces, some AT edge `(c,d)` is unreachable (no
candidate has `x·c = d`), then the lazy AT walk — which gives `(c,d)` probability
`1/(2(n−1)) > 0` — is not `Σ_x w(x)T_x` for any `w ≥ 0`. No linear program is needed.

*Computed:* `lrb_output.txt` §5. The lazy AT walk is provably **not** a Brown walk on **2 of 5**
posets at `n = 3`, **11 of 16** at `n = 4`, and **55 of 63** at `n = 5`, including every antichain
with `n ≥ 3`. The remaining cases are: one vacuous per `n` (the chain, `|L(P)| = 1`, no AT edge at
all) and the ones this **sufficient** test does not decide, which on this population are exactly the
posets with `|L(P)| ≤ 4`, where the AT graph is complete or a 4-cycle and the test cannot bite.

**⚠️ F1 — THE CASES THIS TEST LEFT OPEN ARE NOT UNDECIDED, AND ROW B6 IS FALSIFIED AS A UNIVERSAL
(mg-86a3, MAJOR; the largest correction in the audit and the one clause that had to change).** This
subsection used to close: *"the AT walk is not a Brown walk wherever `|L(P)| ≥ 5`, on the tested
population, and undecided by this test below that."* The hedge *"on the tested population"* was doing
all the work, and one `n` further out the unhedged reading is **false**.

**First, "undecided" was a resting place, not a fact.** The test above is only *sufficient*. The
actual question is a **finite linear feasibility problem with rational data**:

```
    exists w >= 0 on faces with   sum_x w(x) T_x = P_lazy ,   sum_x w(x) = 1 ,
    where T_x[c,d] = [ x·c = d ].
```

The auditor solved it exactly (Phase-I simplex with Bland's rule over `Fraction`,
`code/hodge_leverage_audit_86a3/exact_lp.py` → `out_brown.txt`) — first reproducing this
document's own NOT-counts exactly (0/2/11/55 at `n = 2..5`, vacuous 1 per `n`, undecided 1/2/4/7, so
the test is faithfully implemented and correctly described) and then **deciding every case this
document left open. Every one comes out POSITIVE: the lazy AT walk IS a Brown walk there**, with
exact rational witnesses printed.

| `n` | NOT a Brown walk | **IS a Brown walk** | vacuous |
|---|---|---|---|
| 2 | 0 | **1** | 1 |
| 3 | 2 | **2** | 1 |
| 4 | 11 | **4** | 1 |
| 5 | **55** | **7** | 1 |

The witnesses have the shape one would guess once the LP is written down — each *directed* AT edge is
supplied at exactly its lazy-walk probability `1/(2(n−1))` by one collapsing face, and the identity
face `(P)` takes up the slack on the diagonal. For `|L(P)| = 2`: `1/(2(n−1))` on each of the two
chambers and `1 − 1/(n−1)` on `(P)`
(so `1/4,1/2,1/4` at `n = 3`; `1/6,2/3,1/6` at `n = 4`; `1/8,3/4,1/8` at `n = 5`). For `|L(P)| = 4`
(AT graph `C_4`): `1/(2(n−1))` on each of the four one-coordinate collapses and `1 − 2/(n−1)` on `(P)`
(`1/6` ×4 with `1/3` at `n = 4`; `1/8` ×4 with `1/2` at `n = 5`).

**Second, the `|L(P)| ≤ 4` boundary is an artifact of stopping at `n = 5`, and there are infinitely
many counterexamples.** Extending this section's own population by one `n` (all 318 posets at `n = 6`,
restricted to `|L(P)| ≤ 14`) turns up **12** positives, one of them with **`|L(P)| = 8`**
(`out_n6_brown.txt`). And it is not sporadic: let **`V_k`** be the ordinal sum of `k` two-element
antichains (`n = 2k`, AT graph the hypercube `Q_k`, `|L(P)| = 2^k`).

| `k` | `n` | `\|L(P)\|` | this test | exact answer |
|---|---|---|---|---|
| 1 | 2 | 2 | undecided | **IS a Brown walk** |
| 2 | 4 | 4 | undecided | **IS a Brown walk** |
| 3 | 6 | **8** | undecided | **IS a Brown walk** |
| 4 | 8 | **16** | undecided | **IS a Brown walk** |

(`out_brown_family.txt`.) So the positive class is **unbounded in `|L(P)|`**, and ledger row B6 has
**genuine counterexamples, not a coverage gap**. It survives only inside the hedge, and the hedge is
struck.

### The repaired scope clause — and it is STRONGER than the one it replaces

**This is not a retreat and must not be written as one.** On `V_k` the AT graph is the hypercube
`Q_k`, so `Δ_AT` is the hypercube Laplacian: a sum of `k` commuting terms whose spectrum is known by
inspection and which is **already diagonalised before Brown's theorem is invoked**. Brown's theorem
reaches `Δ_AT` exactly where `Δ_AT` needs no help. So:

> **`Δ_AT` is a Brown walk on an infinite family (`|L(P)| = 2^k`, unbounded) and not otherwise on any
> poset tested with `|L(P)| ≥ 5`. On that family `Δ_AT` is already diagonal, so the technique of §9
> buys no bound on the bridge quantity anywhere.**
>
> Equivalently, in one sentence: **the semigroup technique reaches `Δ_AT` only where `Δ_AT` is
> already free.**

That is a better sentence than *"undecided below `|L(P)| ≤ 4`"*, it is the sentence the evidence
supports, and it is the load-bearing fact behind *"the case for `A(P)` is claim 3, not claim 2"* —
which survives in this stronger form. What the original wording offered was an untested corner where
the answer might have been favourable; what replaces it is a **reason**.

**One cheap open question is created, and it is deliberately not answered here.** A characterisation
of the positive class is now well-posed: the evidence (`n ≤ 6` exhaustively, plus `V_{k ≤ 4}`) is
consistent with *"iff the AT graph is a hypercube"*, which the auditor states as a **conjecture and
explicitly does not claim** — and neither does this document. It would say exactly when the semigroup
technique touches the bridge quantity, which is a sharper input than "not, mostly". Ledger row **B6″**.

**So the technique of §9 does not deliver a bound on `Δ_AT`.** It delivers exact spectra for a
different, large, natural family of walks on the same state space.

---

## §10 — Controls

`code/hodge_leverage/controls.py`; output committed at `controls_output.txt`.

### Positive controls — the instrument reproduces answers known independently of this programme

| # | control | result |
|---|---|---|
| P1 | `λ₂(Δ_AT(A_n))` against `2 − 2cos(π/n)` — Aldous' conjecture for the path, proved by Caputo–Liggett–Richthammer | agree to `≤ 1.5e−14`, `n = 2..6` |
| P2 | `lambda2_weighted_graph` against `λ₂(C_m) = cos(2π/m)` and `λ₂(P_m) = cos(π/(m−1))` | all 10 exact to `1e−12` |
| P3 | the two eigensolvers (dense Jacobi, sparse Lanczos) on the same `Δ_AT` matrices — disjoint code paths | agree to `1e−9`, `\|L\|` up to 60 |
| P4 | the **Tsetlin library**: Brown's prediction against the classical derangement-multiplicity spectrum | exact match, `n = 2..5` |
| P5 | Theorem L's spectral content: equal block-type multisets ⟹ equal link `λ₂`, memo disabled | 97 keys, 0 clashes, `n ≤ 5` |

P4 is the sharpest: an independently known spectrum, reproduced by machinery that contains none of
its ingredients.

### Negative controls — each perturbs a construction this work item *builds*

This is mg-e0ce's finding F2 applied: a control that only perturbs a downstream comparison does not
show that the construction is right. All five mutations below act on objects introduced here — the
weighted link, the down-up walk, the band product, the multiplicity rule. Vacuity is **computed**
(the mutation left the object unchanged), not asserted.

**⚠️ The "fires on" column does NOT read uniformly, and it must not be quoted as though it did
(mg-86a3's F4). Four of the five rows are scored by a *downstream failure* — a false (LG), Theorem D
failing, the band axioms or Brown spectrum failing, negative multiplicities. X2 is scored by a
*disagreement with this codebase's own link*, which is a different kind of evidence.** The column now
states which kind each row is; nothing else about the four downstream rows changes, and **they are not
downgraded** — see the sizing below.

| mutation | what scores it | fires on | vacuous on |
|---|---|---|---|
| **X1a** link **weights**: uniform instead of the induced measure | downstream: does (LG) become false | **0 posets — see below** (it did change the bound's *value* on 365) | 37 (mutation changed no link, or `\|L(P)\|=1`) |
| **X1b** link **incidence**: keep the vertex set, join every pair (forget that a link face is a *chain*) | **downstream failure** | 398 posets — the perturbed construction yields a **false** (LG) | 4 |
| **X2** link **vertex set**: all proper ideals comparable with `σ`'s top ideal | **⚠️ DISTINGUISHABILITY, not falsification (F4)** — the mutated vertex set differs from the link as this codebase computes it. Downstream, this mutation falsifies **nothing**: 0 of 81 posets get a false (LG) | 4946 faces *(a count of disagreements, not of failures)* | 1245 faces |
| **X3** the **down-up walk**: give free ridges weight `1/2` instead of treating them as self-loops | **downstream failure** | 399 posets — Theorem D fails | 5 (the antichains: no free ridge) |
| **X4** the **band product**: order intersections by `(j,i)` | **downstream failure** | band axioms fail on 20 of the 23 posets `2 ≤ n ≤ 4`; Brown spectrum fails on 20 | 3 (mutation equals the true product) |
| **X5** the **multiplicity rule**: sum over `Y ≤ X` instead of `Y ≥ X` | **downstream failure** | 82 posets — negative multiplicities or wrong total | 4 |

**Credit first, because it was checked rather than assumed, and it is the half of the audit's verdict
on this section that matters most.** mg-86a3 applied mg-5630's absorbability test to all six
mutations: **none of X1a, X1b, X2, X3, X4, X5 is a gauge in disguise.** The battery varies weight
families and posets; the corruptions act on the weighted link, the down-up walk, the band product and
the multiplicity rule, and **none is absorbable into a parameter the battery already varies** — none is
a diagonal conjugation or any other isospectral relabelling (`out_controls.txt`). **mg-5630's specific
defect is not repeated here.** The two findings below are calibration defects inside a battery that
is, in kind, the right one.

**⚠️ F3 — X1a's diagnosis was backwards, and the sentence is struck.** This paragraph used to read:
*"The reason is structural, not luck: (LG) is a lower bound, and uniform link weights come out with
`λ₂` at least as large as the induced-measure ones on every poset here, so the mutated bound is
smaller and still true. A mutation that inflates `γ` can never falsify (LG)."* The **last** sentence
is correct and structural. **The premise it is applied to is false**, measurably, over all posets
`n ≤ 5` (`out_controls.txt` Q4): uniform weights give a **smaller** `λ₂` on **75 of 2748 links**, a
smaller `γ_i` on **9 levels**, and a strictly **larger** mutated bound than the true bound on **4
posets**. So X1a is **not** `γ`-inflating and **not** structurally incapable of falsifying (LG): on 4
posets it moves the bound in the falsifying direction and simply does not move it far enough. The true
statement, which is what stands here: **X1a does not fire on this population; on 4 posets the mutation
does deflate `γ` and enlarge the bound, but never past the truth. It is empirically silent here, not
structurally incapable.** This is the same shape as mg-5630's defect — a property incidental to the
instance read as a law — and it landed inside §10, which §13's own 4c pass certifies as clean.

**What survives F3, unchanged and in the same direction as before.** The **operative** conclusion is
right: X1a does not fire on this population, **X1b — which deflates `γ` and does falsify (LG) — is the
control that covers the link construction**, and keeping the non-firing mutation in the report with a
diagnosis rather than replacing it silently is the correct practice. This programme has been burned by
controls that pass because they cannot fail; what F3 corrects is the *reason given*, not the *reading
of the result*.

**⚠️ F4 — X2 is a distinguishability check, and sizing it in both directions matters.** `controls.py`
scores X2 as *"the mutated vertex set differs from the link as this codebase computes it"*. Measured
three ways by the audit:

| scoring | result |
|---|---|
| as implemented, against the correct link | fires on 4946 faces, vacuous on 1245 *(reproduces `controls_output.txt` exactly)* |
| as implemented, against a link carrying the very bug X2 mutates toward | fires on **0**, vacuous on 6191 → the control returns FAIL |
| **downstream: does the X2 mutation falsify (LG)?** | **fires on 0 posets, vacuous on 81** |

**Both directions, explicitly.** X2 is **not** a gauge and **not** unfalsifiable: injecting the exact
bug it mutates toward makes it go silent, so it *does* guard that one alternative construction, and
that is real. What it does **not** do is detect anything else — its mutation changes 4946 faces and
**breaks no downstream result**. So *"fires on 4946 faces"* must not sit in the same column as X1b's
*"398 posets yield a false (LG)"* without saying which is which, and the table above now says. §10's
framing (*"all five mutations act on objects introduced here … Vacuity is computed"*) is accurate but
incomplete: what was not computed is whether firing **means** anything.

**Also recorded because it is a code/doc mismatch, not a mathematical one.** `controls.py`'s own
comment describes a different criterion from the one implemented — *"the vertex count must stop
matching `Σ_i #proper ideals of Q_i`"*, a comparison against Theorem L's **independent** prediction.
On this population the two criteria agree face-for-face (4946/1245 either way), so the mismatch is
inconsequential here — and the check the comment describes yields a bonus: **the true link's vertex
count matches Theorem L on 6191 of 6191 faces**, an extra independent confirmation of Theorem L.

**The one control gap this document named itself is now closed, by the auditor.** No negative control
here perturbs the **Theorem G eigenfunction computation** — the single load-bearing new proof — and
§13 says so and says an auditor should rebuild it first. `code/hodge_leverage_audit_86a3/audit_theoremG.py`
does exactly that, with no shared code, to `A_12`. See §6.

---

## §11 — Claim ledger

Labels: **PROVEN** = proof given here (or here plus mg-276d's audited lemmas), all finite posets.
**PROVEN-by-computation (population)**. **CITED** = a published theorem used, not re-derived.
**CONDITIONAL**. **HEURISTIC**. Reductions asserted in prose are included.

| # | claim | label | population / condition |
|---|---|---|---|
| **D** | `I − P_du = Δ_AT/(2(n−1))`: the AT walk is the down-up walk on `F(P)` | **PROVEN** (§2) | all finite posets; independently checked exactly on all 405 posets `n ≤ 6` |
| **L** | `link_{F(P)}(σ) ≅ *_i F(P\|_{block i})`; induced weights are product weights; the weighted link depends only on the block iso-types | **PROVEN** (§3) | all finite posets; checked as a simplicial isomorphism on all 6197 faces of all posets `n ≤ 5`, 0 failures; spectral content by P5 |
| **H** | codimension-2 links are exactly `P_2, P_3, P_4, C_4, C_6`, with `λ₂ = −1, 0, 1/2, 0, 1/2`; `C_4` = commutation, `C_6` = braid, the paths = boundary truncations | **PROVEN** (§4, finite case check via L) | all finite posets; 44 055 links enumerated over `4 ≤ n ≤ 6`, exactly these five, nothing else |
| **H'** | `λ₂ ≤ 1/2` at the codimension-2 level | **PROVEN** (§4) | all finite posets |
| **NV** | every link of dimension `≥ 1` is connected, so `γ_i < 1` and (LG) is strictly positive | **PROVEN** (§5.1) | all finite posets |
| **G** | for `A_n`, `γ_i ≥ 1/2` at every level `−1 ≤ i ≤ n−4` | **PROVEN** (§6, explicit eigenfunction) | all `n ≥ 3`; the identity `(Pf) = f/2` verified in exact arithmetic for `A_3…A_8`. **✅ CONFIRMED by independent rebuild (mg-86a3): re-derived by hand, Coxeter complex rebuilt with no shared link code, `Pf = f/2` exact to `A_12` under three `a`-vectors. Complete, `n`-free, no gap — so M2's `2^{Θ(n)}` loss is a THEOREM. The audit's three attempts to break it all failed.** |
| **G'** | `γ_i = 1/2` exactly (not merely `≥`) | **PROVEN-by-computation**, and the **max-over-the-level step is now a THEOREM** (row **J**, §6.1; added by mg-a2bd) | `A_3…A_7`, **extended to `A_3…A_9` by mg-86a3**; and `γ_i ≤ 1/2` on **all 404 posets with `2 ≤ n ≤ 6`**, attained by 373. **The `A_9` extension was made on a PER-LINK computation while `γ_i` is a PER-LEVEL MAX** (mg-d39d A8(3)) — evidence one notch narrower than the statement. **Repaired by writing the missing step down rather than by narrowing the row, because the row is TRUE:** by L + J, `λ₂(link σ) = max_j (b_j−2)/D · λ₂(F(A_{b_j}))` with `b_j − 2 ≤ D` and equality **iff** the other blocks are singletons, so `γ_i = λ₂(F(A_{n−i−1}))`, attained at Theorem G's face and no other. Checked exhaustively over **all faces** for `n ≤ 6` and over block-size multisets to `A_9` (`out_verify_join.txt` `J4`). What stays computational is only the base case `λ₂(F(A_m)) ≤ 1/2`, `m ≤ 9` — hence the label is unchanged. **The restraint in not upgrading this to a theorem is audit-endorsed** (nothing downstream needs it; no easy proof of `≤ 1/2` exists — trickling-down at the fixed point returns 1). See **F5** for the two places the equality nonetheless leaked into prose |
| ~~**G″**~~ | ~~`γ_i ≥ 1/2` for **every finite poset** having a dimension-`i` face one of whose blocks induces an antichain of size `≥ 3`~~ | ⚠️ **STRUCK — FALSE AS A UNIVERSAL (mg-d39d A1; struck by mg-a2bd).** It was labelled `PROVEN (§6; free from G + Theorem L)` and it is **not free and not true**: **55 (poset, level) counterexamples at `n ≤ 6`**, smallest at `n = 5`, and **3901 of 7989** faces under the per-face reading its own proof sentence argues | the counterexamples: `A_3 ⊕ A_2`, `A_3 ⊕ C_2`, `A_2 ⊕ A_3`, `C_2 ⊕ A_3` at `n = 5` (all `γ_0 = 1/4`), 51 more at `n = 6` (values include `1/3` and `0.408367`) — reproduced twice, by `hodge_leverage_audit_d39d/out_gpp.txt` and by `hodge_leverage_join/out_verify_join.txt` `J2`, and confirmed by this document's own `local_to_global.gammas`. **WHY IT FAILED, which is the part worth keeping — see row J: Theorem L makes the link a JOIN and joins SUPPRESS `λ₂`. Theorem G's face is one size-`m` block plus `i+1` SINGLETONS, and singletons contribute no join factor, so there the link is not a join at all. G″ dropped the singleton requirement, and THAT WAS THE HYPOTHESIS DOING THE WORK — the four `n = 5` counterexamples are exactly the ordinal sums, i.e. exactly where the other block stops being a singleton.** Nothing consumed it (§6, and it appears in no summary and never in `STATE.md`), so this is a strike, not a retraction: **G, G′, M2, the `2^{Θ(n)}` headline and the routing are untouched** |
| **G‴** | `γ_i ≥ 1/2` for every finite poset having a dimension-`i` face whose blocks are one antichain of size `≥ 3` **and singletons otherwise** | **PROVEN** (§6, by **G** + **L**) | all finite posets. This *is* the strengthening that is free from G + L, and it is what G″ should have said: with the other blocks singletons the link is `F(A_m)` on the nose, so G's eigenfunction applies verbatim. Nothing here consumes it either; it is recorded because a struck row should leave behind the true statement in its neighbourhood |
| **J** | **joins suppress `λ₂`.** For `X = X_1 * ⋯ * X_r` with product weights, `D = dim X`, the 1-skeleton walk's spectrum on `1⊥` is exactly `⋃_j {(p_j/D)·μ : μ ∈ spec(X_j on 1⊥)} ∪ {−1/D}^{r−1}`. A factor eigenfunction survives **scaled by `p_j/D < 1`**, so an exact `1/2` in a factor is strictly below `1/2` in the join | **PROVEN** (§6.1) | all weighted joins. Checked as a **full-spectrum** identity on **all 48 846 genuine-join links of all 405 posets `n ≤ 6`** — link side measured by brute force from the facet list with no use of L, factor side assembled from the factor complexes alone — `0` mismatches, worst deviation `1.2×10⁻¹⁵` (`hodge_leverage_join/out_verify_join.txt` `J1`). **Two consumers:** it is why G″ is false, and it is the missing step in row G′ (the max over a level is attained at the one-big-block face). **Direction, stated because it would otherwise have to be guessed: joins only make `γ` SMALLER, hence the (LG) bound WEAKER on the affected posets — nothing here reopens `A(P)`** |
| **N1a** | `Δ_AT = NᵀN`, `N` the signed vertex–edge incidence matrix of the AT graph | **PROVEN — unconditional** (§7) | all finite posets; 405/405 here and 405/405 by mg-86a3's disjoint route. Pure graph theory: nothing simplicial enters |
| **N1b** | `Δ_AT = E · L^rel_top · E` | **PROVEN given L1** ⟹ **CONDITIONAL** (§7, §7.1) | all finite posets given L1; 405/405 both routes. **F2: this half inherits mg-276d's CONDITIONAL reading of "relative", which §13(iv) declares and the old flat-PROVEN row N1 did not carry** |
| **N1c** | `∂_rel E = N` up to a sign per row | **PROVEN given L1** (§7) | all finite posets given L1; 405/405 by mg-86a3, which also verified the twisted signs at the two facets of every interior ridge are always opposite |
| **N1r** | the *conclusion* of N1 is **robust to the reading**: under the absolute reading, `E · L^abs_top · E = (n−1)I − A`, still a graph object | **PROVEN-by-computation** (§7.1) | all 405 posets `n ≤ 6` (mg-86a3, `out_robustness.txt`; `deg + #free = n−1` also 405/405). **So only the equation is conditional on L1, not the pricing** |
| **N1'** | therefore no technique using only the top two dimensions of `F(P)` is new: `∂∂*` is the classical edge/line-graph matrix and the cofilling bound is flow duality | **PROVEN** for the two named instances (§7); **HEURISTIC** as a universal over "all techniques" | the two instances are proved; "every conceivable top-two-dimension technique" is an argument by identification, not a theorem, and is labelled as such |
| **N2** | for every non-antichain the span of the shape-`α` faces is not an `S_n`-submodule of `Ind_{S_α}^{S_n}1` | **PROVEN** (§8) | all finite posets, all `α` with `≥ 2` parts; checked on all posets `n ≤ 5` (exactly 1 exception per `n`, the antichain) |
| **N2'** | `Σ_i s_i` is not central in `C[S_n]` for `n ≥ 3`, so characters do not diagonalise `Δ_AT` even on the antichain | **PROVEN** (§8) | all `n ≥ 3` |
| **B1** | `F(P)` is a left regular band under successive refinement, with identity `(P)` | **PROVEN** (§9.1: closure and the three axioms are one-line checks) | all finite posets; 0 violations over all 87 posets `n ≤ 5` (associativity `n ≤ 4`) |
| **B2** | the supports are exactly the acyclic partitions of `P`, and they are closed under join = common refinement | **PROVEN** (§9.1) + **PROVEN-by-computation** | all finite posets for the join; the equality checked on all 87 posets `n ≤ 5`. **mg-86a3: if anything UNDER-claimed** — the equality is provable for all finite posets in two lines (topologically sorting the blocks of an acyclic `P/π` gives a compatible ordered partition; the converse is immediate) |
| **B2'** | the acyclic partitions are **not** closed under refinement | **PROVEN** (witness `{a<c, b<d}`, partition `{a,d}\|{b,c}`) | — |
| **B3** | Brown's theorem: `λ_X = Σ_{supp ≤ X} w(y)`, `Σ_{Y ≥ X} m_Y = ∏_B \|L(P\|_B)\|`, diagonalisable | **CITED** (Brown 2000; BHR) | not re-derived here |
| **B4** | the instantiation of B3 to `F(P)` is correct: predicted eigenvalues **and** multiplicities **and** diagonalisability match the actual matrix | **PROVEN-by-computation** | all 24 posets `n ≤ 4` × 3 weight families, exact rational ranks; 5 named `n = 5` posets mod `p`. **`A_6` was skipped** (`\|L\| = 720`, outside the rank budget) |
| **B5** | the multiplicities `m_X` are nonnegative integers summing to `\|L(P)\|` | **PROVEN-by-computation** | all 405 posets `n ≤ 6` |
| **B6** | the lazy AT walk is **not** a Brown walk | ⚠️ **FALSIFIED AS A UNIVERSAL (mg-86a3 F1) — this row previously read "PROVEN-by-computation … undecided by this test exactly where `\|L(P)\| ≤ 4`", and it has GENUINE COUNTEREXAMPLES, not a coverage gap.** What survives is **PROVEN-by-computation on the population**: not a Brown walk on 2/5 at `n=3`, 11/16 at `n=4`, 55/63 at `n=5`, including all antichains `n ≥ 3`; vacuous where `\|L(P)\| = 1` | the counterexamples: the question is a finite exact rational LP, and **every case this document left "undecided" is DECIDED and decided POSITIVELY** — the lazy AT walk IS a Brown walk on 1/2/4/7 posets at `n = 2..5`, with exact rational witnesses. The `\|L(P)\| ≤ 4` boundary is an **artifact of stopping at `n = 5`**: 12 positives at `n = 6` including one with `\|L(P)\| = 8`, and the **infinite** family `V_k` (`\|L(P)\| = 2^k`) is positive for every `k` tested. **The old row survived only inside the hedge "on the tested population" and the hedge was doing all the work.** Replaced by **B6′** |
| **B6′** | **the semigroup technique reaches `Δ_AT` only where `Δ_AT` is already free.** `Δ_AT` is a Brown walk on an infinite family (`\|L(P)\| = 2^k`, unbounded) and not otherwise on any poset tested with `\|L(P)\| ≥ 5`; on that family the AT graph is the hypercube `Q_k`, so `Δ_AT` is the hypercube Laplacian, **already diagonal by inspection** — so §9 buys no bound on the bridge quantity anywhere | **PROVEN** for the `V_k` half (the hypercube identification is by inspection; positivity verified by exact LP for `k ≤ 4`) + **PROVEN-by-computation** for the negative half (`n ≤ 5` complete, plus `n = 6` at `\|L(P)\| ≤ 14`) | **This is STRONGER than the clause it replaces and must not be read as a retreat** — the original offered an untested corner where the answer might have been favourable; this gives a reason. It is the load-bearing fact behind "the case for `A(P)` is claim 3, not claim 2", which survives in this form. Source: mg-86a3 §2 (§9.4 here) |
| **B6″** | a characterisation of the positive class — the evidence is consistent with *"iff the AT graph is a hypercube"* | **NOT CLAIMED — open, cheap, and well-posed** | consistent with `n ≤ 6` exhaustively and `V_{k ≤ 4}`; **stated as a conjecture by the auditor and claimed by neither document.** It would say exactly when the semigroup technique touches the bridge quantity |
| **LG** | `gap(P_du) ≥ (1/(d+1))∏_{i=−1}^{d−2}(1−γ_i)`, hence `λ₂(Δ_AT) ≥ 2∏(1−γ_i)` | **CITED** (Alev–Lau 2020; Kaufman–Oppenheim; Dinur–Kaufman; ALOV) — **checked, not proved, here** | not violated on any of the 404 posets `2 ≤ n ≤ 6`. If the cited form is misremembered, §5's numbers are void and §6's `γ` computation is not |
| **M1** | on all 404 posets `2 ≤ n ≤ 6`, truth/bound `≤ 2.62`, and the ratio grows with `n` | **PROVEN-by-computation** | that population; `λ₂` by Lanczos, cross-checked against dense Jacobi (P3) and a closed form (P1) |
| **M2** | for `A_n` the (LG) bound is `≤ 2^{3−n}` while `λ₂(Δ_AT) = 2−2cos(π/n)`, so the loss is `2^{Θ(n)}` | **PROVEN** given **G** and the **CITED** Caputo–Liggett–Richthammer theorem | all `n ≥ 3`. Not an extrapolation: both sides are theorems |
| **M3** | removing the braid hexagon does not repair the bound (`C_a ⊔ C_a` has no 3-antichain and still has `γ_i = 1/2`; the fence reaches `γ_{−1} = 0.46` and still decays geometrically) | **PROVEN-by-computation** | `C_a ⊔ C_a` for `n ≤ 8`; fences `n ≤ 7` |
| **T** | `γ = 1/2` is the fixed point of Oppenheim's trickling-down recursion `γ ↦ γ/(1−γ)`, so `F(P)` sits exactly where the hierarchy is vacuous | **CITED** (Oppenheim) + trivial arithmetic | the recursion is cited; `1/2 ↦ 1` is arithmetic |
| **T'** | the *cause* is the pseudomanifold property (mg-276d Lemma 3(a)) — the same fact that makes the bridge's "relative" well-posed | **HEURISTIC** | codimension-2 links have max degree `≤ 2` **is** proved (H); that this forces uselessness of product-form bounds *in general* is **not** proved. The antichain instance (G) is |
| **S1** | the answer to the ticket is: technique exists on the face **SEMIGROUP** side (B3/B4), not on the Hodge-spectral side acting on `Δ_AT` (M2) | **CONDITIONAL** on the two citations (LG, Brown), on **reading L1 of "relative"** (F2 — added here; the *conclusion* is robust to it by **N1r**, only the equation is not), and on the population of B4. **B6's population is no longer a condition: it is DECIDED, and B6′ replaces it with a statement that does not depend on a population** | stated as the verdict in §0 with those conditions attached. **F9: the word to use is SEMIGROUP, not Hodge** — claim 3 uses no complex, no boundary map and no Laplacian (§1) |
| **S2** | claim 3 is *"a real technique and it is new to this programme"* | **accurate as written**, but the correct label is **an IMPORT, correctly attributed** — not a discovery (mg-86a3 press 4) | Brown's theorem, correctly CITED, instantiated to a band. The sharpest concrete instance (control P4, the Tsetlin library) is the **antichain** case — a classical theorem. For non-antichain `P` this document verifies the prediction against the matrix; it does not derive a statement previously out of reach, and it does not claim to. Ledgered here because *"new to this programme"* reads as **discovery** in a `STATE.md` row |
| **U1** | no *other* Hodge-theoretic technique can help | **NOT CLAIMED** | only product-form link bounds were tested. Weighted/normalised Hodge Laplacians, `L_k` for `k` far from the top, discrete Morse theory and the toric/Coxeter geometry the source also mentions are **untouched** |
| **U2** | anything about BK or block moves | **NOT CLAIMED** | out of scope by the ticket; the two-block Brown walks of §9 *are* block moves, and no claim is made that they are BK's |
| **U3** | anything about weighted or degree-normalised chains | **NOT CLAIMED** | inherited from mg-276d §8.3(4) |
| **P1** *(prose, §1)* | the operational test for *"lives on the Hodge/face side"* | ⚠️ **TOO WEAK to carry the word "Hodge" (F9)** — it is a test for *"not the AT graph"*. Ledgered here because it was unledgered and it is what licenses answering the headline YES | Bruhat order, descent statistics, coupling, strong stationary duality and Diaconis–Saloff-Coste all pass it. Claim 3's hypothesis is about the monoid of `P`-compatible ordered partitions: **no complex, no boundary map, no Laplacian, no "relative", no `E`**. §1, §12 |
| **P2** *(prose, §2)* | *"the free ridges are exactly the holding probability of the canonical down-up walk"* | ⚠️ **STRUCK as an identification (F8)** — holding `= ((n−1−deg) + deg/2)/(n−1)`, i.e. free ridges **plus half the interior ridges** | §2, corrected in place. The intended content is the next sentence (`L^abs − L^rel = diag(#forbidden)` is the laziness) and is unaffected |
| **P3** *(prose, §10)* | *"The reason is structural, not luck"* (X1a's retirement) | ⚠️ **STRUCK (F3)** — the premise is false: smaller `λ₂` on 75 of 2748 links, smaller `γ_i` on 9 levels, strictly larger mutated bound on **4 posets**. X1a is empirically silent here, **not structurally incapable** | the operative conclusion (X1a does not fire; X1b is the usable control) **stands**; only the reason is replaced. §10 |
| **P4** *(table, §10)* | X2 *"fires on 4946 faces"* scored alongside four downstream-failure rows | ⚠️ **RELABELLED (F4)** — X2 is a **distinguishability check**: it falsifies nothing downstream (0 of 81), though it is **not** a gauge and **not** unfalsifiable (injecting the bug it mutates toward makes it go silent) | §10. **The four downstream rows are not downgraded**; the column now states which kind of evidence each row carries |
| **P5** *(artifact)* | `sweep_output.txt` §B header *"extrapolating `γ_i = 1/2` … and proved for the top level"* | ⚠️ **CORRECTED at source (F6)** — the committed artifact **disclaimed the headline it supports**; Theorem G proves `γ_i ≥ 1/2` at **every** level `−1 ≤ i ≤ n−4`, not just the top | `run_sweep.py`, regenerated. §5.3 said the opposite and was right |
| **P6** *(artifact)* | `run_sweep.py`'s *"posets with every `γ_i < 1/2`: 29 (tags: …)"* | ⚠️ **SILENT TRUNCATION, fixed at source (F7)** — it printed `w3[:12]` under a count of 29 | all 29 now printed. A silent cap in a battery's output is the fourth checkable question of `STATE.md` Appendix A |

---

## §12 — What this prices (recommend, do not act)

Offered as scoping input; the routing decision is pm-onethird's.

- **The `A(P)` case should be rewritten around the face semigroup, not around Hodge theory.** The
  program's stated hope (source §Program, and mg-276d §8.3(1)) is that Hodge/localisation
  technique on `F(P)` will say something about `L(P)`'s dynamics. For `Δ_AT` that hope is now
  priced: the top two dimensions are graph theory verbatim (N1) and the standard link-based
  technique is off by `2^{Θ(n)}` for a structural reason (G, T). What *is* live is that
  `A(P) ⊆ End(C[L(P)])` would contain the whole Brown-diagonalisable family — operators with
  closed-form spectra indexed by acyclic partitions of `P`, with `P`-invariant multiplicities. That
  is a concrete reason to want the algebra, and it is a different reason from the one in the sketch.
  **Two refinements from mg-86a3, and they cut in the same direction.** *(a)* **F9: the cheap form of
  the claim-3 case is not `A(P)`.** If the win is Brown's theorem for a left regular band, the object
  to build is the **semigroup algebra of that band** — which has known structure theory (Brown 2000;
  Saliola on quivers of LRB algebras), is a far cheaper build than an operator algebra generated from
  face incidences, and delivers the Brown-diagonalisable family directly. The bullet above is true
  and is the **expensive route to something the cheap route already gives**. *(b)* **F1: whichever
  object is built, it is not a route to `λ₂(Δ_AT)`** — the semigroup technique reaches `Δ_AT` only
  where `Δ_AT` is already free (row B6′), so the reason to want it is the Brown family on its own
  terms, never the bridge quantity. **Routing note (pm-onethird, 2026-07-30, recorded here because it
  post-dates this document): `A(P)` is NOT to be built as a route to `λ₂(Δ_AT)`.** The pricing above
  is carried by proofs and F1 sharpens it; nothing here is queued or pending.
- **The cheapest next probe, if one is wanted, is a comparison step, and it is graph-side.** The
  exact Brown spectra are inputs; carrying a gap from a Brown walk to `Δ_AT` needs
  Diaconis–Saloff-Coste comparison or canonical paths — a graph technique consuming a face-side
  computation. Whether that composite beats what coupling already gives for linear extensions is
  not addressed here and should not be assumed.
- **Two axes this work item deliberately did not test**, and which are the honest remaining places
  a Hodge-side win could hide: the **weighted/normalised** Hodge Laplacians (mg-276d H4, still
  open) and the intermediate Laplacians `L_k` for `k` far from the top used other than through a
  product-form link bound. Ledger rows U1 and U3.

---

## §13 — Self-audit (Appendix A steps 4c, 4d)

Run because mg-276d ran it and it helped, and recorded because mg-e0ce showed that running it is
not coverage: **a self-audit cannot see the sentence it is auditing.** The external pass is not
substituted for.

**Step 4d — the most general statement, and what its establishing instance holds fixed.** The most
general statements are Theorems D, L, H, N1, N2 and Proposition NV, quantified over *all finite
posets* and carried by proofs, not by generalisation from the 405-poset sweep. Their inputs, stated
so they can be attacked: (i) mg-276d's Lemmas 1–3 (the order-complex description, purity, the
pseudomanifold property) — audited, and used here rather than reproved; (ii) `J(P)` distributive and
graded by cardinality; (iii) the standard simplicial signs and the orthonormal inner product;
(iv) reading L1 of "relative" from mg-276d, which that document labels CONDITIONAL and which this
document **inherits** — every statement here about `L^rel` and about free ridges is conditional on
it, and that is not re-litigated. **No proof step uses `n ≤ 6`.**

The statement that is quantified over `n` rather than over posets, which is where this arc's failure
has landed six times, is **Theorem G** (`γ_i ≥ 1/2` for `A_n`, every `n ≥ 3`). It is the load-bearing
input to the headline, so it was given a proof rather than a trend: the eigenfunction computation in
§6 is complete and `n`-free, and the computation at `A_3…A_8` is a check on it, not its support.
The clause that is **not** upgraded is the *equality* `γ_i = 1/2` — labelled
PROVEN-by-computation on `A_3…A_7` in ledger row G', deliberately not stated as a theorem in §0 or
§6, and not needed for M2 (which uses only `≥`). §5.3's rows for `n = 8,12,20,40` are marked in the
table itself as resting on G, not on the trend. **⚠️ F5 — when the audit ran, that was true of ONE of
the four.** Only the `n = 8` row carried the marker (`1/2 ×6 (§6: ≥ 1/2 PROVEN)`); `n = 12`, `20`, `40`
read plain `1/2 ×10`, `1/2 ×18`, `1/2 ×38`, with **equality** values in their bound columns. **The
repair adds the three missing markers rather than weakening the sentence**, because the mathematics
supports them — G gives `≥ 1/2` at every level for every `n`, which is the direction the bound needs —
and §5.3 now states explicitly that the printed bound for `n ≥ 12` is an equality value standing in
for a proven upper bound, with the equality itself resting on G′ (`A_3…A_9`, by computation). **This is
the mg-e0ce lesson at its own site: a self-audit cannot see the sentence it is auditing — the miss was
inside the clause step 4c certifies.** Direction is conservative (a smaller `γ` only strengthens the
negative) and nothing downstream breaks.

**⚠️ AND STEP 4d WAS RUN ON THEOREM G ONLY — mg-86a3's central methodological finding, recorded here
because it is about this section (F1's root cause).** The paragraph above identified Theorem G as *the*
statement quantified over `n` rather than over posets, supplied a proof for it, and cleared it. **That
was the right call and G survives an independent rebuild** (§6). But **row B6's quantifier was never
examined** — and B6 is quantified over a *population*, with a **numeric boundary read off that
population** (`|L(P)| ≤ 4`). That boundary is where the over-wide statement was this time: a scope
threshold inside a *negative* result, which is a new location for the defect again. **The protection
against 4d was applied to the claim this document expected to fail and not to the one that did.** The
generalisable lesson, in the auditor's shape: 4d must be run on *every* statement whose quantifier is
not over the object it was verified on — including thresholds, including hedges (*"on the tested
population"*), and including scope clauses attached to negatives, which read as modest and are exactly
where a resting place hides. Landed into `STATE.md` Appendix A step 4d.

**⚠️ AND THE NEXT GENERATION LANDED IN THE REPAIR ITSELF — a row the ticket never asked for (mg-d39d
A1, recorded here by mg-a2bd).** mg-a806 was scoped to land B6, the stronger scope sentence, N1's label
and the §10 table. Row **G″** was none of those: it was an extra generalisation the landing
**volunteered**, promoting an auditor's step-4b aside to a `PROVEN` ledger row without rebuilding it.
So it was **simultaneously the most general claim in the commit and the one no brief anchored an audit
to** — and it is the one that was false. The generalisable shape, landed into `STATE.md` Appendix A:
**a landing that adds a row beyond its brief has widened its own scope, and the added row is where step
4d should look first**, because the usual defence — *audit the deliverable's most general statement* —
has no ticket text pointing at an unrequested row. Note also what this instance says about *"the audit
wins where we disagree"*: the false sentence was **mg-86a3's own**, inside its strength-check table,
and neither party had checked it. **An audit's own product is not pre-audited.**

**Other scope axes.** *Regime*: the sweep is the complete isomorphism-class enumeration at each
`n ≤ 6`, not a sample. *Citation*: two published theorems are load-bearing — (LG) and Brown — and
both are labelled CITED, with (LG) additionally checked on the whole population and the consequence
of its being misremembered stated in ledger row LG. *Object*: BK, weighted chains, and the
toric/Coxeter half of the source are untouched (U1–U3). *Population*: B4's spectrum verification
stops at `n ≤ 4` exactly, plus five named `n = 5` posets, and the skip of `A_6` is printed by the
code and stated in §9.3 rather than left implicit.

**Step 4c — the summaries diffed against the body.** §0, the ledger and the §14 row are three
summaries that fail independently.

- §0's headline is *"YES — but not where the bridge points"*. Diffed against the ledger: the YES is
  rows B3–B5 (CITED + PROVEN-by-computation), the "not where the bridge points" is rows M2 and N1
  (PROVEN). §0 carries the scope of the YES (row B6′: the semigroup technique reaches `Δ_AT` only
  where `Δ_AT` is already free) in the same paragraph rather than by reference, because separating
  them would read as a bound on `Δ_AT`. **(This bullet used to cite row B6, "`Δ_AT` is not a Brown
  walk". F1 falsified that as a universal; the scope clause `§0` now carries is B6′, which is
  stronger, and the practice of carrying it in the same paragraph was right and is unchanged.)**
- §0 claim 1 says "no technique using only facets and ridges can be new". The ledger splits this:
  N1 is PROVEN, N1' is PROVEN for the two named instances and **HEURISTIC as a universal**. §0's
  wording is the universal, so §0 is over-stated relative to row N1' unless read with the two
  instances — **and the sentence in §7 that carries the universal says "in different notation",
  which is an identification claim, not a theorem.** This is the one place where a summary is
  broader than its ledger row; it is flagged here rather than silently narrowed, and the ledger row
  is the operative label.
- §0 claim 2 says "exponentially lossy" and attributes it to a proof. That matches M2 (PROVEN given
  G and the cited CLR theorem). It does **not** claim the general "no Hodge technique works" — U1.
- §6's "the feature that makes the bridge work is the feature that blocks the technique" is a
  description of two proved facts with a common cause; it is labelled **HEURISTIC** (row T') and the
  proved part (H) is stated separately.
- The controls section states X1a's failure to fire **in the table**, not only in the prose, so a
  reader tabulating "5 mutations, all fire" cannot get that from this document. **⚠️ Audit-confirmed
  as far as it goes, and incomplete (F3/F4): the table said *whether* each row fired and not *what
  kind of evidence firing was*, and the prose reason given for X1a's non-firing was false. Both
  repaired in §10; the four downstream-failure rows are unaffected.**
- **§0 claim 1's L1 dependence was not carried into the ledger, row S1 or §14 (F2), even though
  §13(iv) above declares it.** Repaired in §7.1 and rows N1a/N1b/N1c/N1r/S1. This is the failure mode
  step 4c exists for, at the one place §13 had already written the correct sentence: **declaring a
  condition in the self-audit is not the same as carrying it into the summaries, and the summaries are
  what get pasted.**

**What this self-audit cannot do.** It cannot see an error in a derivation the author would re-read
as correct — in particular the eigenfunction computation in §6, which is the single load-bearing
new proof here and which no independent code path re-derives (the exact-arithmetic check confirms
the *identity*, using the same link construction). That is the first thing an auditor should
rebuild from scratch. **✅ That instruction was followed and the proof held** — mg-86a3 rebuilt it by
hand and from the Coxeter complex with no shared code, to `A_12`. **Naming the right target was itself
correct**: of the two things this section examined, the one it cleared (G) survived and the one it did
not examine (B6's threshold) is where the MAJOR finding landed.

---

## §14 — `STATE.md` row, as landed

**Status: LANDED by mg-a806**, with every mg-86a3 repair applied here first. **The row below is
UNCHANGED by mg-a2bd's strike of G″, and that is a fact rather than an omission: G″ never appeared in
this section, in `STATE.md`, or in any other summary — verified by an exhaustive sweep (see §6). The
strike therefore touches §6 and the ledger and nothing else.** This section is a
**primary** audit target (Appendix A step 4c) and it was audited clause by clause; the row below is the
repaired text, and the corresponding `STATE.md` row carries the same clauses. Carries its own
conditions rather than pointing at them — including the one it previously pointed at (**F2**).

> **AMBER-POSITIVE · the bet is priced (mg-a3d4; computation permitted and used — 405 posets, controls both directions incl. one that did not fire and is reported; audited mg-86a3 — OVERSTATED: 0 BROKEN mathematics, every headline number reproduced by a disjoint route, **THEOREM G CONFIRMED, `n`-FREE AND EXTENDED FOUR ORDERS**, one MAJOR falsification, repairs landed by mg-a806)** | **does the face/Hodge side carry technique the graph side lacks?** (doc: `OneThird-Hodge-Side-Leverage.md`; audit: `OneThird-Hodge-Side-Leverage-IndependentAudit.md`; code: `code/hodge_leverage/`, `run_all.sh`, ~13 min; audit instrument: `code/hodge_leverage_audit_86a3/`, no shared code) | **YES, but not where the bridge points, the place it points is priced OUT, and the "YES" is the face SEMIGROUP and not Hodge theory.** **⭐ THE LOAD-BEARING RESULT FIRST, because it is a theorem and it was rebuilt by an independent auditor: the `2^{Θ(n)}` loss is PROVEN, not extrapolated.** Every level's link of `F(A_n)` has `λ₂ ≥ 1/2` by an explicit eigenfunction (`f(S) = Σ_{i∈S}a_i`, `Σa_i = 0`, eigenvalue exactly `1/2`, `n`-free — Theorem G), so the cited product-form bound for the antichain is **at most `2^{3−n}`** against a truth of `2−2cos(π/n) = Θ(n^{−2})` supplied by the cited Caputo–Liggett–Richthammer proof of Aldous' conjecture. **mg-86a3 re-derived the eigenfunction BY HAND and rebuilt the Coxeter complex from its definition with NO shared link code: `Pf = f/2` exact to `A_12` (this document reached `A_8`), `λ₂ = 1/2` exact to `A_9` (row G′ claimed `A_7`) — four orders past the range each was stated on, three attempts to break it all failed, "the strongest thing in the document".** Recorded at this length deliberately: Theorem G is the statement quantified over `n` rather than over posets — the place this arc's failure had landed six times — and it is **the first such statement in the arc that was named as the hazard, given a proof rather than a trend, and had the proof HOLD under independent rebuild.** That is the arc's best methodological result to date. **(1) The top two dimensions of `F(P)` are graph theory verbatim, and the conclusion is unconditional even though one equation is not.** `Δ_AT = NᵀN` with `N` the signed vertex–edge incidence matrix of the AT graph is **PROVEN and UNCONDITIONAL** (row N1a; 405/405 by two disjoint routes); `Δ_AT = E·L^rel_top·E` is **PROVEN GIVEN reading L1 of "relative"**, which mg-276d labels CONDITIONAL and this document inherits (row N1b — **F2**: the old flat-PROVEN label did not carry it and neither did this row). **The pricing is robust to the condition and provably so:** under the other reading, `E·L^abs_top·E = (n−1)I − A`, the shifted adjacency matrix of the same AT graph (405/405, mg-86a3), so **under either reading the top-degree Hodge operator is a graph object** and *"no technique using only facets and ridges can be new"* holds unchanged. Hodge duality in top degree *is* the classical incidence/line-graph identity and the cofilling bound *is* flow duality — any new leverage must come from the faces below the top two dimensions, exactly the part mg-276d's proof never used. **(2) The technique that lives there imports, and it is exponentially lossy.** Two new theorems license the import: **the AT walk IS the standard down-up walk on the facets — `I − P_du = Δ_AT/(2(n−1))` (PROVEN)** — and **localisation: `link_{F(P)}(σ)` is the simplicial join of the `F(Q_i)` over the induced subposets on `σ`'s blocks (PROVEN; verified as a simplicial isomorphism on all 6197 faces, `n ≤ 5`)**. The cited bound (Alev–Lau; Kaufman–Oppenheim; ALOV) is then **never violated on any of the 404 posets `2 ≤ n ≤ 6` and never worse than a factor 2.6204 there** — but exponentially lossy on the antichain by Theorem G above. `γ_i ≤ 1/2` holds on all 404 posets and is attained by 373, so **this is not about antichains**: removing the braid hexagon does not help (`C_a ⊔ C_a` has no 3-antichain and still has `γ_i = 1/2`; the fence reaches `0.46` and still decays geometrically). **`1/2` is the fixed point of Oppenheim's trickling-down recursion `γ ↦ γ/(1−γ)`, so `F(P)` sits exactly at the value where the hierarchy carries no information** — and the property that puts it there is the **pseudomanifold** property, mg-276d Lemma 3(a), *the same fact that makes the bridge's "relative" well-posed* (this last causal reading is labelled HEURISTIC; the codim-2 consequence is proved). **(3) The face SEMIGROUP does carry technique, it is exact rather than a bound, and it is NOT Hodge theory.** `F(P)` is a left regular band under successive refinement (0 axiom violations, all 87 posets `n ≤ 5`) whose support lattice is exactly the **acyclic partitions** of `P` (verified; and they are NOT closed under refinement — witness `{a<c,b<d}` with `{a,d}|{b,c}`), so **Brown's theorem (CITED) diagonalises every face-driven walk on `L(P)`: `λ_X = Σ_{supp(y) ≤ X} w(y)` indexed by acyclic partitions, with multiplicities fixed by `Σ_{Y ≥ X} m_Y = ∏_{B∈X}|L(P|_B)|` — independent of `w`.** Verified against the actual matrix by **exact rational rank computations (eigenvalues, multiplicities AND diagonalisability) on all 24 posets `n ≤ 4` under three weight families** — mg-86a3 re-ran this under **six**, reusing the same `m_X`, which is what *"independent of `w`"* has to mean operationally — plus five named `n = 5` instances mod `p`; **`A_6` was skipped and that is stated, not hidden**. Sharpest control: the **Tsetlin library** — Brown's prediction reproduces the classical derangement-multiplicity spectrum exactly (`n ≤ 5`) and derangements appear nowhere in the code; note it is the **antichain** case, i.e. a classical theorem, so it is a control and not evidence of new reach. **This uses precisely the left-regular-band product mg-276d recorded as UNUSED (its §8.3(6)). But (3) is an IMPORT, correctly attributed — not a discovery — and it is not Hodge (F9): the hypothesis of Brown's theorem is about the monoid of `P`-compatible ordered partitions, and claim (3) uses no complex, no boundary map, no Laplacian, no "relative" and no twist. The headline question says "Hodge"; the audited answer to that question is NO, and the YES belongs to the semigroup.** **⚠️ SCOPE, and it travels with (3) — CORRECTED, and the correction is a STRENGTHENING (mg-86a3 F1, MAJOR).** This row used to read *"`Δ_AT` is NOT a Brown walk — proven on 55 of 63 posets at `n = 5` …; undecided by that test exactly where `|L(P)| ≤ 4`"*. **That is FALSIFIED as a universal, and it has genuine counterexamples rather than a coverage gap.** The question is a finite exact rational LP; **every case left "undecided" is DECIDED, and decided POSITIVELY** (the lazy AT walk IS a Brown walk, with exact rational witnesses, on 1/2/4/7 posets at `n = 2..5`), and the `|L(P)| ≤ 4` boundary is an **artifact of stopping at `n = 5`** — 12 positives at `n = 6` including one with `|L(P)| = 8`, and the **infinite** family `V_k` (ordinal sum of `k` two-element antichains, `|L(P)| = 2^k`) is positive for every `k` tested. **The honest clause, which is stronger than the one it replaces: `Δ_AT` is a Brown walk on an infinite family and not otherwise on any poset tested with `|L(P)| ≥ 5` — and on that family the AT graph is the hypercube `Q_k`, so `Δ_AT` is the hypercube Laplacian, ALREADY DIAGONAL BY INSPECTION. THE SEMIGROUP TECHNIQUE REACHES `Δ_AT` ONLY WHERE `Δ_AT` IS ALREADY FREE.** So (3) is exact technique for a *different* family of walks on the same state space and **buys no bound on `Δ_AT` anywhere** — and that is now a reason rather than an untested corner. **Do not read this as claim (3) being withdrawn: claim (3) is a real technique that does not reach the bridge quantity.** One cheap open question is created and claimed by nobody: characterise the positive class (the evidence is consistent with *"iff the AT graph is a hypercube"*, stated as a conjecture by the auditor on `n ≤ 6` plus `V_{k≤4}`). **Also settled, negatively: representation theory does not descend** — `S_n` acts transitively on the ordered partitions of shape `α`, the `P`-compatible ones are a nonempty proper subset for every non-antichain, so their span is never an `S_n`-submodule (PROVEN; exactly 1 exception per `n ≤ 5`, the antichain) — **and even on the antichain `Σ_i s_i` is not central, so characters do not diagonalise `Δ_AT`**, which is why the antichain gap needed Aldous/CLR rather than a character computation. **And the source's claim (4) is now PROVEN and quantitative: the codimension-2 links of `F(P)` are exactly `C_6` (the braid hexagon, `λ₂ = 1/2`), `C_4` (two commuting moves, 0), `P_4` (1/2), `P_3` (0), `P_2` (−1) — 44 055 links enumerated over `4 ≤ n ≤ 6`, exactly these five, every per-shape count reproduced identically by the audit** — so the boundary correction is (a) the laziness of the down-up walk and (b) the truncation of hexagon to path, which is the only thing that can push `γ` below 1/2 and is not enough. **CONTROLS — the credit is verified, not assumed, and two calibration defects are repaired.** mg-86a3 applied mg-5630's absorbability test to all six mutations: **none is a gauge in disguise, none is absorbable into a parameter the battery already varies, and X1b/X3/X4/X5 are each scored by a downstream FAILURE — mg-5630's specific defect is NOT repeated.** Repaired: **X1a's retirement rested on a false structural claim** (*"uniform weights inflate `γ`, so it can never falsify (LG)"* — measured: smaller `λ₂` on 75 of 2748 links, smaller `γ_i` on 9 levels, a strictly **larger** mutated bound on 4 posets; X1a is **empirically silent here, not structurally incapable**) — **F3**; and **X2 is a DISTINGUISHABILITY check, not a falsification control** (its mutation changes 4946 faces and falsifies nothing downstream, 0 of 81; it is nonetheless not a gauge — injecting the bug it mutates toward makes it go silent) — **F4**. **NOT CLAIMED:** that no other Hodge technique can help (weighted/normalised Laplacians and the toric/Coxeter half of the source are **untouched**); anything about BK; anything about weighted chains. **`A(P)` was NOT built.** **ROUTING (pm-onethird, 2026-07-30): `A(P)` is NOT to be built as a route to `λ₂(Δ_AT)`, and nothing about it is queued or pending.** The pricing is carried by proofs, and F1 **sharpens** it: the case for the algebra, if anyone ever wants it, is (3) on its own terms — and even then the cheap form of (3) is the **LRB semigroup algebra** (Brown 2000; Saliola), not `A(P)` as the source specifies it (**F9**), while the Hodge/localisation hope in the sketch is priced out for `Δ_AT` by a theorem. |
