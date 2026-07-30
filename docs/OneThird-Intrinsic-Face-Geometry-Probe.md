# Viability probe: the intrinsic face-geometry program at `n = 4`, `n = 5`, `n = 6`

**Work item:** mg-276d. **Source under probe:** `~/files/intrinsic_face_geometry_program.tex`,
*"Sketch of an Intrinsic Geometric Program for Linear Extension Dynamics"* (Daniel, 2026-07-30).
**Scope:** probe only. **`A(P)` was not built** — see §10.

**Re-derivable:** every number below is produced by `code/face_geometry/run_all.sh`
(pure Python 3, no third-party packages, exact integer arithmetic, ~17 s).
Committed outputs: `code/face_geometry/controls_output.txt`,
`code/face_geometry/probe_output_n6.txt`.

**Post-audit status (independent audit mg-e0ce, `013e073`; repairs landed by mg-78c0).**
The audit verdict is **CONFIRMED — the GREEN stands, and for the reason this document gives.**
Theorems A, B and C were independently re-derived line by line and the full 405-poset population
re-swept by a disjoint route (no ideal lattice); **zero BROKEN mathematics**. Six repairs have been
landed in this document, each marked at its site: **F1** ledger row D2 upgraded to **PROVEN** with
the audit's two-line proof (§4, Corollary B′), so §0's clause and the ledger label now agree;
**F2** the construction-side negative control adopted (§5, NEGATIVE CONTROL 3) — *the pipeline
survived the control it was missing*; **F3** §2's independence paragraph narrowed; **F4** "the
foundation" narrowed in §10 and §12; **F5** §8.2's *"hence the mixing time"* struck; **F6** §0's
*"not a similar one"* corrected. §11 records what the self-audit got wrong about F1, because that is
the finding about method. **Where this document and the audit disagreed, the audit won.**

**Second-round status (independent audit mg-5630 of the mg-78c0 landing, `fcc8a11`; repairs landed by
mg-1319).** Verdict **OVERSTATED**, with **0 BROKEN mathematics** — every committed number reproduced
independently, `controls_output.txt` and `probe_output_n6.txt` byte-identically, the D2 upgrade fully
earned, the adopted control **faithfully ported**, and *"the pipeline survived the control it was
missing"* pressed as self-flattering and found honest. What was overstated is this document's and
`STATE.md`'s claims **about the repair**, in three places where the **text claimed more than the code
verified** — one pattern, not three slips: **(a)** NEGATIVE CONTROL 3's coverage — its corruption is a
diagonal `±1` gauge, isospectral and absorbable into the twist, so **coverage of the construction went
from zero to ONE ABSORBABLE SIGN GAUGE: a relocation of the gap, not a closure**, with `le_to_facet`
the named uncovered site (§5, re-sized); **(b)** the all-`+1` row's *"both matrices unchanged"* — true,
and in fact a theorem, but **measured by neither run cited for it**; now proved *and* measured (§5);
**(c)** the battery's own scoring — a row that provably cannot fail printed `[PASS]` under a bottom
line reading `ALL CONTROLS PASS`; it now scores `[CANNOT FAIL]` and suppresses that bottom line.
Also: the `n ≤ 6` half of F3's coverage sentence corrected to `n ≤ 5` for Lemma 1 — **at §11 by
mg-1319, and at §2, which is the sentence this document itself labels `(F3, …)`, only now by mg-f2e1
(mg-f7bc F2). The entry that stood here tagged that correction `(§11)`, and §11 *was* corrected — but
the same overstatement stood at §2, so the entry named one of two sites while reading as though it
covered the sentence. A2 was a PARTIAL repair and this line was the defect: a changelog is an
assertion ABOUT a diff and nothing checks it against the diff.** The audit's `38/38` population
flagged as a `[:20]` truncation at §5 by mg-1319 — **and at §12 by mg-f2e1, the site mg-1319's
*"flagged at every site where `38/38` appears"* missed (mg-f7bc F1); that claim was false when
written, so the flag at §12 and the class statement in `STATE.md` Appendix A replace it rather than
restating it more confidently.** And F4's last unpatched site patched (§12).

**⚠️ TWO CORRECTIONS TO THIS ENTRY, 2026-07-30 (mg-6653 A4 and its recorded imprecision; landed by
mg-7d5a) — and they are corrections of the kind this entry exists to name, in the entry that names
them.** *First:* it read *"the per-site enumeration in §5 and in `STATE.md` Appendix A"*. **§5 carries
no enumeration** — it carries the truncation FLAG mg-1319 landed — **and §5 is not touched by
`ba3ec79` at all**: that commit's three hunks in this file are the §-head changelog, §2 and §12
(re-measured at `code/face_geometry_landing_7d5a/verify_landing.py` T4, which reads the hunks out of
the commit and the section bounds out of the post-image). A changelog line asserting content absent
from its own diff, inside the sentence that names that failure mode, is the defect at the third
generation. *Second:* *"claimed the correction outright"* was itself imprecise — the replaced entry
did carry `(§11)`. Both are fixed above, and the `STATE.md` claim is now a class statement, which is
what §5 and Appendix A actually support.
**Nothing mathematical is struck. Net: REAL PROGRESS ON D2, RELOCATION NOT CLOSURE ON THE CONTROL GAP.**

---

## §0 — Verdict

**GREEN.** All three claims are **PROVEN for every finite poset**, not merely verified at `n = 4`.
They are not `n = 4` coincidences and they are not artefacts of a lucky poset.

The computation (all **405** posets up to isomorphism on `n ≤ 6`) came first and is reported in §6;
the proof in §4 came after and is what upgrades the verdict from *PROVEN-by-computation on 405
posets* to *PROVEN*. Both are given, and the ledger (§9) labels each claim by which of the two
supports it.

Read §0 with §8 attached, which is the honest half:

- **What is established.** For every finite poset `P`, the top relative Hodge Laplacian of the
  compatible face complex `F(P)`, conjugated by the sign twist, **is** the adjacent-transposition
  Laplacian `D − A` on `L(P)` — the *same matrix* after a relabelling of the basis vectors by signs,
  not one up to normalisation and not an isospectral coincidence. **(F6, repaired: `E` is an
  explicit involution, so the conjugation `L ↦ E L E` *is* a similarity — the point is that the
  conjugator is known, diagonal and `±1`, not that no similarity is performed. §8.1 states this
  correctly and is the form to quote.)** Claims (2) and (3) likewise, in full.
- **What is not.** This is an **exact dictionary between two descriptions of one matrix**, and by
  itself it supplies **no new bound and no new tool**. It is a bridge in the sense the ticket asked
  for — a statement on one side can be read on the other — and it is *only* that. Nothing here
  touches BK dynamics, block moves, weighted or normalised chains, or the faces of `F(P)` below the
  top two dimensions. §8.3 lists exactly what the bridge does not carry.
- **Three corrections to the source.** (i) The sketch attaches *"up to the orientation/sign twist"*
  to claim (1) only; **the twist is needed for claim (2) as well**, by the same conjugation — the
  untwisted forms fail on **399 of the 405** posets tested, the 6 exceptions being exactly the
  chains, where `|L(P)| = 1` and both sides are the zero `1×1` matrix (§6.3). (ii) The sketch writes
  `Σ_i(1−s_i)` without saying which side `s_i` acts on; **only the right/position action makes claim
  (2) true** — the left/value reading fails on the antichain at **every `n ≥ 3`**, and this is now
  **PROVEN** (§4, **Corollary B′**; ledger row D2), not verified on `n ≤ 5` only. **(F1, repaired.
  This clause was over-labelled when written: it asserted the universal in `n` while row D2 carried
  `PROVEN-by-computation on n ≤ 5`, and §11's own self-audit asserted no upgrade had been made. The
  statement was true; the audit supplied the two-line proof and it is adopted here, so the upgrade is
  the repair and the label now matches. See §11.)**
  (iii) *"the boundary correction records **precisely** the forbidden generators"* is true at the
  level of the **complex** and an overstatement at the level of the **Laplacian difference**, which
  is diagonal and records only how many (§4, Theorem C; ledger row C3).

---

## §1 — Pinning the example (ticket step 1)

The sketch says *"the four-element example"* — **singular, and it never says which poset.** The
document contains no figure, no Hasse diagram, no relation list, and no other four-element
reference. Two readings are available and the text does not choose between them: *the* example
could mean a specific poset the author had in hand, or simply *the case `n = 4`*.

**It cannot be determined from the document.** So, per the ticket, no guess was made: **all 16
posets on four elements were tested** (`probe_output_n6.txt`, final table). All 16 satisfy all
three claims, including both degenerate ends (the antichain, where `L(P) = S_4` and `|L| = 24`;
the chain, where `|L| = 1`) and everything between.

This matters for a reason beyond bookkeeping: had the claim held on only some of the 16, "the
four-element example" would have been unresolvable evidence. It holds on all 16, so the ambiguity
is discharged rather than worked around.

---

## §2 — The objects, rebuilt from the definitions

Everything below is built from the sketch's own definitions. Nothing checks the source's
arithmetic; the source reports no numbers to check.

Let `P` be a finite poset on a ground set of `n` elements.

**Order ideals.** `J(P)` = the lattice of order ideals (down-sets) of `P`, ordered by inclusion.
It is distributive (Birkhoff) and graded by cardinality, of rank `n`.

**Face complex.** `F(P) = ⊔_k Sur_iso(P,[k])`, the surjective isotone maps `P → [k]`, equivalently
the ordered set partitions of `P` compatible with `P`. Grading by `k`.

**Linear extensions.** `L(P)`, written as words `w = (w_1,…,w_n)` listing `P` in a compatible order.

**The adjacent-transposition Laplacian.** `Δ_AT := Σ_{t=1}^{n−1} (1 − τ_t)` acting on `C[L(P)]`,
where `τ_t` swaps the entries in positions `t, t+1` if the result is again a linear extension and
acts as the identity otherwise. As a matrix, `Δ_AT = D − A`, with `A` the adjacency matrix of the
adjacent-transposition graph on `L(P)` and `D` its degree matrix. **This is the object the probe
matches against, and §8.3 states precisely which other Laplacians it is not.**

**The ambient Coxeter Laplacian.** `Σ_{i=1}^{n−1} (1 − s_i)` on `C[S_n]`, `s_i` acting on the right
(swap of positions `i, i+1`). Its *compression* to `C[L(P)]` is `ι* (Σ_i(1−s_i)) ι` for the
inclusion `ι : C[L(P)] ↪ C[S_n]`.

**Independence of the implementation.** In the code, `Sur_iso(P,[k])` is enumerated by brute force
directly from the definition; `L(P)` is enumerated by repeated minimal-element choice; the ambient
Coxeter Laplacian is built as a genuine `n! × n!` matrix and then cut down. None of **those three
objects** is built via the chain description of Lemma 1 — that description is *derived* below and
then *checked* against the brute-force enumerations (POSITIVE CONTROL 3).

**(F3, repaired — say what is and is not independent.)** The sentence above is true of the three
objects it names and **must not be read as a statement about the pipeline**: the complex whose two
Laplacians are actually computed **is** built through the chain description (`le_to_facet` inside
`top_laplacians`). So Lemma 1 is load-bearing for the numbers, and the cross-check is what licenses
it. That cross-check reaches `n ≤ 4` here (POSITIVE CONTROL 3); the mg-e0ce audit closed it to
**`n ≤ 5`** by a build that never uses Lemma 1 at all — 87/87 at `n ≤ 5` for all `k`
(`code/face_geometry_audit_e0ce/out_n6.txt:44`). **The audit's `n ≤ 6` figure is PURITY, a different
check — 404/404 at `2 ≤ n ≤ 6` (`.../out_extra.txt`, X1); `404` vs `405` is not a discrepancy, the
purity range starts at `n = 2`. ⚠️ CORRECTED 2026-07-30 (mg-f7bc F2, landed by mg-f2e1): this
sentence read *"closed it to `n ≤ 6`"*, one bound asserted for two checks with the numbers stripped —
and *"it"* is the Lemma-1 cross-check, which reached `n ≤ 5`. This is the site mg-5630 indexed as its
F3 and the site this document labels `(F3, …)`; mg-1319 corrected §11's copy of the same overstatement
and its changelog reported F3's sentence as done, so the surviving defect was the claim of
completeness, not the sentence — which self-corrected in its own em-dash clause. Two checks, two
bounds, and they are not interchangeable.** The independence claim that survives is the audit's, not
this paragraph's.

---

## §3 — Four structural lemmas

These are the content. Claims (1)–(3) are corollaries.

### Lemma 1 (the face complex is an order complex) — PROVEN

The map `f ↦ (f^{-1}{1,…,i})_{i=1}^{k−1}` is a bijection
```
Sur_iso(P,[k])  ≅  { chains  I_1 ⊊ ⋯ ⊊ I_{k−1}  of proper nonempty order ideals of P }.
```

*Proof.* `f` is isotone iff every `f^{-1}{1,…,i}` is a down-set (if `x <_P y` then `f(x) ≤ f(y)`,
so `y ∈ f^{-1}{1..i} ⟹ x ∈ f^{-1}{1..i}`; conversely if every such preimage is a down-set and
`x <_P y`, then `x` lies in the preimage at level `f(y)`, so `f(x) ≤ f(y)`). `f` is surjective iff
all `k` fibres are nonempty, i.e. iff `∅ ⊊ I_1 ⊊ ⋯ ⊊ I_{k−1} ⊊ P`. The inverse sends a chain to
`f(x) = min{ i : x ∈ I_i }` with `I_k := P`. ∎

So `F(P)` **is** the order complex `Δ(J(P) ∖ {∅,P})`: a simplicial complex whose vertices are the
proper nonempty ideals and whose faces are chains of them. An element of `Sur_iso(P,[k])` is a face
with `k−1` vertices, i.e. of dimension `k−2`.

*Verified independently:* POSITIVE CONTROL 3 checks this bijection degree by degree against the
brute-force enumeration of `Sur_iso(P,[k])`, for all 24 posets with `n ≤ 4`, all `k`.

### Lemma 2 (facets = linear extensions; purity) — PROVEN

`F(P)` is **pure of dimension `n−2`**, and its facets are in bijection with `L(P)`.

*Proof.* `J(P)` is graded by cardinality, so a maximal chain in `J(P)` is
`∅ = I_0 ⊊ I_1 ⊊ ⋯ ⊊ I_n = P` with `|I_t| = t`. Setting `w_t := I_t ∖ I_{t−1}` (a single element)
lists `P` in an order compatible with `P`, i.e. a linear extension; and `w ↦ (I_t = {w_1,…,w_t})`
inverts it. Deleting `I_0` and `I_n` leaves `n−1` vertices, so each facet has dimension `n−2`. ∎

*Verified independently:* POSITIVE CONTROL 3, all posets `n ≤ 4`.

### Lemma 3 (`F(P)` is a pseudomanifold with boundary; free ridges = forbidden generators) — PROVEN

Call a codimension-1 face of a facet a **ridge**. Then:

**(a)** every ridge lies in **exactly one or exactly two** facets;

**(b)** for the facet of `w ∈ L(P)` and the ridge `ρ_t` got by deleting `I_t` (`1 ≤ t ≤ n−1`):
```
ρ_t lies in two facets  ⟺  w_t and w_{t+1} are P-incomparable  ⟺  τ_t is legal at w,
```
and in that case the second facet is the one of `w·s_t`. Equivalently,
```
ρ_t is FREE (in one facet)  ⟺  w_t <_P w_{t+1}  ⟺  the generator s_t is FORBIDDEN at w.
```

*Proof.* The facets containing `ρ_t` are the maximal chains of the interval `[I_{t−1}, I_{t+1}]` in
`J(P)`, an interval of rank 2 in a distributive lattice. Every rank-2 interval of a distributive
lattice is either a 3-element chain or a diamond `B_2` — a distributive lattice has no interval
`[x,y]` of rank 2 with three or more atoms, since two distinct atoms already join to `y`, and a
third atom `c` would give `c = c ∧ y = c ∧ (a ∨ b) = (c∧a) ∨ (c∧b) = x`, a contradiction. So there
are one or two maximal chains, proving (a).

For (b): write `a = w_t`, `b = w_{t+1}`, so `I_{t+1} ∖ I_{t−1} = {a,b}` and `I_t = I_{t−1} ∪ {a}`.
The interval is a diamond iff `I_{t−1} ∪ {b}` is also an ideal, i.e. iff every `P`-predecessor of
`b` lies in `I_{t−1}`, i.e. iff `a ≮_P b`. Since `a` precedes `b` in a linear extension, `b ≮_P a`
automatically; so this says exactly that `a` and `b` are incomparable, i.e. that swapping them
yields another linear extension, and the resulting chain is the facet of `w·s_t`. ∎

*Verified independently:* POSITIVE CONTROL 3 checks (a) for all posets `n ≤ 4` from the ridge
incidence table; the probe checks (b) as a set equality, facet by facet, for all 405 posets `n ≤ 6`
(column `(3)bij`).

### Lemma 4 (two facets share at most one ridge) — PROVEN

*Proof.* If `σ ≠ τ` share ridges `ρ_1 ≠ ρ_2`, then `σ ∖ ρ_1` and `σ ∖ ρ_2` are two *different*
vertices of `σ`, and each is "the unique vertex of `σ` not in `τ`" (as `|σ| = |τ| = n−1` and
`ρ_i ⊆ σ ∩ τ` has `n−2` vertices). Contradiction. ∎

---

## §4 — The three claims, proven

**Boundary map.** Order the vertices of every face by inclusion (a chain is totally ordered). For a
facet `σ = (I_1,…,I_{n−1})` the standard simplicial boundary is
```
∂σ = Σ_{t=1}^{n−1} (−1)^{t−1} (I_1,…,Î_t,…,I_{n−1}).
```
Give `C_•(F(P))` the inner product in which faces are orthonormal. `F(P)` has dimension `n−2`, so
in top degree the Hodge Laplacian has no up-part and equals the down-Laplacian `∂*∂`.

**Boundary subcomplex.** `∂F(P)` := the subcomplex generated by the free ridges. Since it has
dimension `≤ n−3`, `C_{n−2}(F,∂F) = C_{n−2}(F)` and `C_{n−3}(F,∂F)` is the span of the **interior**
ridges. So the relative boundary `∂_rel` is `∂` followed by the projection killing free ridges, and
```
L^rel_top := ∂_rel* ∂_rel ,        L^abs_top := ∂* ∂ .
```
*(This is the reading of "relative" the probe adopts; §7 addresses the fact that the sketch does not
define it, and why this reading is the intended one.)*

**Computing both.** For facets `σ, τ`, `⟨∂*∂σ, τ⟩ = Σ_ρ [ρ:σ][ρ:τ]`.

- Diagonal, absolute: `σ` has exactly `n−1` ridges, each contributing `(±1)² = 1`. So
  `(L^abs)_{σσ} = n−1`.
- Diagonal, relative: only interior ridges survive, and by Lemma 3(b) these are exactly the legal
  transpositions at `w`. So `(L^rel)_{σσ} = deg_A(σ)`.
- Off-diagonal, `σ ≠ τ`: by Lemma 4 they share at most one ridge, and by Lemma 3(b) they share one
  iff `τ = σ·s_t` for some `t`. In that case `σ` and `τ` differ only in their `t`-th ideal, so the
  shared ridge sits at **index `t` in both**, and both incidence numbers equal `(−1)^{t−1}`;
  their product is `+1`. A shared ridge lies in two facets, hence is interior, hence survives in
  the relative complex too. So both Laplacians have the same off-diagonal part, namely `+A`.

Therefore, **for every finite poset `P`**:
```
L^abs_top = (n−1)·I + A ,        L^rel_top = D + A .                              (★)
```

**The twist.** Let `ε(w) = sgn(w) = (−1)^{inv(w)}` and `E = diag(ε)`. If `τ = σ·s_t` then `τ`'s word
differs from `σ`'s by a transposition, so `ε(τ) = −ε(σ)`. Hence `E A E = −A`, while `E` commutes
with every diagonal matrix. Conjugating (★):

> ### Theorem A (claim (1)) — PROVEN, all finite posets
> ```
> E · L^rel_top(F(P)) · E   =   D − A   =   Σ_{t=1}^{n−1} (1 − τ_t)   =   Δ_AT .
> ```

> ### Theorem B (claim (2)) — PROVEN, all finite posets
> ```
> E · L^abs_top(F(P)) · E   =   (n−1)·I − A   =   ι* ( Σ_{i=1}^{n−1}(1 − s_i) ) ι .
> ```
> *Proof of the second equality.* `Σ_i (1 − s_i) = (n−1)I − Σ_i R_{s_i}` on `C[S_n]`, and
> `(Σ_i R_{s_i})_{w,v} = 1` exactly when `v = w·s_i` for some `i`. Restricting rows and columns to
> `L(P)` leaves `(n−1)I` on the diagonal and the **induced-subgraph** adjacency `A` off it. ∎
>
> **The twist is required here too.** The sketch attaches "up to the orientation/sign twist" to
> claim (1) alone; without `E`, (2) reads `(n−1)I + A = (n−1)I − A`, false whenever `A ≠ 0`.
>
> **And the side of the action is not optional.** The sketch writes `Σ_i (1 − s_i)` in `C[S_n]`
> without saying whether `s_i` acts on the left (swapping the **values** `i, i+1`) or on the right
> (swapping the **positions** `i, i+1`). Only the **right/position** reading is true. The
> left/value reading holds on just **3/5, 5/16 and 8/63** posets at `n = 3, 4, 5` — the smallest
> witness against it at each `n` is the **antichain**, where `L(P) = S_n` and the two compressions
> are the two different Cayley graphs of `S_n`. This is forced, not a convention: the ridge move of
> Lemma 3(b) swaps `w_t` and `w_{t+1}`, which is a move on positions.

> ### Corollary B′ (the antichain refutes the left/value reading at every `n ≥ 3`) — PROVEN
> **Claim.** For the antichain on `n ≥ 3` elements, the left/value reading of claim (2) is false.
>
> *Proof.* On the antichain `L(P) = S_n`, so the compression is the whole `n!×n!` matrix and the
> left reading asserts `A_left = A_right` on `C[S_n]`. Take `w = s_1`. Its right-neighbours include
> `s_1 s_2`; its left-neighbours are exactly `{s_j s_1}`. Now `s_1 s_2 ≠ s_2 s_1` (the braid
> relation, available because `n ≥ 3`), and for `j ≥ 3`, `s_j s_1 = s_1 s_j ≠ s_1 s_2`. So `s_1 s_2`
> is a right-neighbour and not a left-neighbour, and the two matrices differ. ∎
>
> At `n = 2` the two readings coincide, which is why the statement begins at `n = 3`.
>
> **Provenance, stated because the label depends on it.** This proof is the mg-e0ce auditor's (audit
> §4), supplied in repair of **F1**: §0 asserted the universal in `n` while ledger row D2 carried
> `PROVEN-by-computation on n ≤ 5`. It is adopted verbatim in substance and **row D2 is upgraded to
> PROVEN**. Verified computationally at `n = 3,…,8` by the audit instrument
> (`code/face_geometry_audit_e0ce/out_extra.txt`, X2) — the computation is now a check on a proof
> rather than the support for a universal.

> ### Theorem C (claim (3)) — PROVEN, all finite posets, in two readings
> **Strong (complex-level, and this is the real statement).** For each `w ∈ L(P)`, Lemma 3(b) gives a
> **bijection** between the free ridges of the facet of `w` and the positions `t` at which the
> generator `s_t` is forbidden at `w` (i.e. `w_t <_P w_{t+1}`).
>
> **Weak (Laplacian-level).** `L^abs_top − L^rel_top = diag( (n−1) − deg_A(w) )` = the diagonal
> matrix counting forbidden generators.
>
> **These are not the same statement, and the difference is worth keeping.** The Laplacian
> difference records only *how many* generators are forbidden at each `w`; *which* ones is visible
> only in the face incidence, not in the matrix. The sketch's wording — "records **precisely** the
> forbidden generators" — is true in the strong reading and an overstatement in the weak one.

**Uniqueness of the twist.** `E` is not a convenient choice; it is forced. Any diagonal `±1` matrix
`E' = diag(η)` satisfying `E' L^rel E' = D − A` must have `η(σ)η(τ) = −1` on every edge of the
adjacent-transposition graph. That graph is connected (classical: any linear extension can be
carried to any other by legal adjacent transpositions), so such an `η` is unique up to a global
sign, and `ε = sgn` is one. Equivalently: the twist is the unique orientation of the facets making
`F(P)` coherently oriented, and the adjacent-transposition graph is bipartite with `sgn` as the
bipartition.

**The twist is intrinsic, not a choice of labelling** (the audit's remark on ledger row E, added
because "the twist depends on a choice of labelling of `P`" is the obvious objection and it has an
answer). `sgn(w)` does depend on how `P`'s elements are labelled — but relabelling multiplies every
`sgn(w)` by one global sign, and conjugation by `E = diag(sgn)` is insensitive to a global sign. So
`L ↦ E L E` is labelling-independent. This is covered by the uniqueness argument above rather than
being an extra fact. **NEGATIVE CONTROL M3 exhibits this**: a diagonal `±1` matrix that is *not* of this
form is rejected by the identity test on all 72 posets where it differs from `E` (and coincides with
`E` on the 14 where `|L(P)| ≤ 2`, where there is only one edge to get right).

---

## §5 — Controls (ticket: "run a positive control")

`code/face_geometry/controls.py`; output committed at `controls_output.txt`. **All pass.**

### Positive controls — the machinery reproduces answers known independently of this program

| # | control | result |
|---|---|---|
| P1 | reduced Betti numbers of `S¹` (triangle boundary), a disc, `S²` (octahedron boundary), two disjoint edges, wedge of two circles | all 5 correct, exact arithmetic over `Q` |
| P2 | count of posets up to isomorphism, `n = 1..5`: must be `1, 2, 5, 16, 63` (OEIS A000112) | correct |
| P3 | brute-force `Sur_iso(P,[k])` `≡` chains of proper ideals; `∂∘∂ = 0`; facets `≡` `L(P)`; every ridge in 1 or 2 facets | all pass, all 24 posets `n ≤ 4`, all `k` |
| P4 | reduced homology of `F(P)` against the known theorem: `Δ(J(P)∖{∅,P}) ≃ S^{n−2}` if `P` is an antichain, acyclic otherwise | all pass, all 86 posets `2 ≤ n ≤ 5` |
| P5 | Hodge cross-check: `ker L^abs_top` (computed from the top two dimensions only) vs `H_{n−2}(F(P))` (computed by P4 from the ranks of **every** boundary matrix) | agree on all 405 posets `n ≤ 6` |

P5 is the sharpest of these: the two sides are computed by disjoint code paths over different parts
of the complex, and Hodge theory predicts they must agree.

### Negative controls — the test is shown to fail where it should

The ticket's requirement is that the Laplacian code be demonstrated to produce the **wrong** answer
on a case where the answer is known. Three demonstrations, on two different code paths — and **which
control reaches which path is the thing to read carefully** (F2, below):

**N1 — the homology code is not sign-blind.** Replacing the alternating simplicial signs by all
`+1` and recomputing `S¹` gives reduced Betti `{0: −1, 1: 0}` instead of the truth `{0: 0, 1: 1}` —
a manifestly wrong answer (a negative Betti number), so the machinery is sensitive to exactly the
structure it is supposed to be sensitive to.

**N1 is a control on the *homology* path, and it is not a control on the Laplacian. (F2, repaired.)**
This section previously offered N1 as one of two demonstrations that *the Laplacian code* can produce
the wrong answer. That was wrong on both halves, and the mg-e0ce audit is right: N1 runs a locally
defined `bad_boundary` through the homology path and **never touches `top_laplacians`**; and its
corruption **could not have fired there anyway** — rebuild `L^rel` and `L^abs` with all-`+1`
simplicial signs and **neither matrix changes**, so claims (1)–(3) still hold. **Cite this correctly
(mg-5630 §3.2 → mg-1319): it is a THEOREM, not a count.** The simplicial sign of an incidence depends
only on the ridge (a ridge omits exactly one ideal cardinality, so the deletion index is fixed by the
ridge), giving `d_true = diag(row signs) · d_allplus`, a row rescaling `dᵀd` cannot see — true for
every finite poset. The counts confirm it rather than establishing it, and they are now counts *of
this statement*: `L^rel` unchanged 86/86 **and** `L^abs` unchanged 86/86, claims (1)/(2)/(3) re-run
under the corruption 86/86/86 (`controls_output.txt`, NEGATIVE CONTROL 3). *(The previously cited
figures — the audit's 41/41 and this battery's 86/86 — measured **claim-(1) survival**, not matrix
equality, so neither of them measured the sentence they were attached to.)* Nor does N2 close the gap: of
its five mutations, **only M2 perturbs the construction** of the Laplacian from the complex — M1 and
M3 perturb the twist, M4 and M5 perturb the target. So as originally submitted the battery had **no
negative control on the boundary-matrix construction**. The gap was in the argument for trusting the
instrument, **not in the instrument**: the audit supplied a construction-side control, and the
true-sign build passes it. It is adopted below as N3.

**N3 — the construction-side control (adopted from the audit, `audit_extra.py` X3).** Corrupt the
simplicial signs that `L^rel` is *built from*, not the comparison. Two sign conventions are run
against the true one, and the difference between them is the whole finding:

| sign convention used to build the boundary matrix | effect on `L^abs`, `L^rel` | claim (1) |
|---|---|---|
| true, `(−1)^{t−1}` | — | holds, 86/86 posets `n ≤ 5` |
| all `+1` | **both matrices unchanged** — `L^rel` 86/86 **and** `L^abs` 86/86, each compared | claims (1)/(2)/(3) each re-run under the corruption: 86/86/86 — **this corruption cannot fire here, and that is a THEOREM**; scored `[CANNOT FAIL]`, not `[PASS]` |
| facet-parity (flip every incidence of the odd-indexed facets) | off-diagonal part changes, **by the diagonal conjugation `L ↦ D·L·D`, `D = diag((−1)^j)`** | **rejected on 82/82 posets with `\|L(P)\| ≥ 2`**; vacuous on the 4 with `\|L(P)\| = 1` (one facet, no second column to flip against) |

**(F2, re-sized 2026-07-30 from the mg-5630 audit §2.2, §3.2 — landed by mg-1319; three repairs, all in this table and all in `controls.py`.)** *(i)* The all-`+1` row's *"both matrices unchanged"* is **true and provable for every finite poset** — a ridge omits exactly one ideal cardinality, so the deletion index is fixed by the ridge alone, `d_true = diag(row signs) · d_allplus`, and `dᵀd` cannot see a row rescaling — **but neither run originally cited for it measured it**: the control compared only the twisted `L^rel`, `L^abs` was never compared, and `claim2_test`/`claim3_test` took no `sign_mode`. The code now checks what the message claims, on both matrices and all three claims. **Prefer the proof to the count.** *(ii)* Because that row's corruption **provably cannot change the object under test**, it is a theorem and not a control, and it is now scored `[CANNOT FAIL]` — a battery whose bottom line reads `ALL CONTROLS PASS` over a tautological row is the same reads-as-covered defect one notch down. *(iii)* The facet-parity row covers **one absorbable sign gauge**, not the construction — see the re-sizing note below the next paragraph.

The audit's own run of the same control fires on **38/38** posets with `|L(P)| ≥ 2` in its
population, which is **41 = 5 + 16 + 20** (`out_extra.txt`, X3); the port here runs it on all 86
posets with `2 ≤ n ≤ 5` and fires on 82/82. Both numbers are of the same control on different
populations. **Flagged because `38/38` is quoted as a headline (mg-5630 §3.3 → mg-1319): the audit's
population is a `[:20]` TRUNCATION — `construction_side_control()` iterates `posets_upto_iso(n)[:20]`
for `n = 3,4,5`, so at `n = 5` it saw 20 of the 63 posets, in enumeration order.** This section
previously described it as *"20 posets per `n` at `n = 3,4,5`"*, which is 60 and contradicted the 41
quoted twice here. Substantively harmless — the number that matters is the port's complete `n ≤ 5`
population, 82/82 — but an unflagged truncation under a headline number is not something a reader can
recover. *(The `82`-vs-`86` gap is **not** a truncation and is fully accounted for in the table above.)*

**State the result of adopting it accurately: the pipeline SURVIVED the control it was missing.**
The construction was never wrong — the all-`+1` row is not a failure of the instrument, it is the
proof that the alternating sign is load-bearing for the *homology* of `F(P)` (where N1 does fire) and
**not** for claims (1)–(3). The lesson routes forward rather than backward: **a control battery must
cover construction as well as comparison**, and counting a control on a neighbouring code path as
covering the construction is the specific mistake to avoid.

**⚠️ WHAT N3 COVERS, SIZED CORRECTLY (mg-5630 §2.2–§2.3, landed by mg-1319). This paragraph
previously ended *"what was missing was a control that could distinguish a correct construction from
an incorrect one, and now that one exists the construction passes it."* That is struck: N3 does not
distinguish a correct construction from an incorrect one in general.** Its corruption is a
**diagonal `±1` gauge conjugation** — `d_parity = diag((−1)^i) · d_allplus · diag((−1)^j)`, so
`L_parity = D · L_true · D` with `D = diag((−1)^j)`, verified exactly on 82/82
(`code/face_geometry_audit_5630/out_nc3.txt`, line C). Hence it is **isospectral**, and it is
**absorbable into the twist**: claim (1) run with parity signs and twist `E·D` passes again on
**86/86** (line D), so the corruption is observationally identical to corrupting the *twist* — which
is exactly what N2's **M1** and **M3** already do, and it sits inside the same diagonal-`±1` gauge
that §8.1's own statement of claim (1) is modulo. The positive control on the control, which this
document did not run (line F): a **mis-indexed facet enumeration** — a corruption of `le_to_facet`,
the step F3 above establishes is load-bearing — leaves N3's negative lines **SILENT, still rejecting
82/82 verbatim**; dropping a ridge moves the row only through the bite-count (82 → 78). And N3's one
line with genuine detection power, *"true signs: claim (1) holds 86/86"*, is **not a negative control
at all**: it restates N2's last line. **So the honest sizing is: coverage of the construction went
from ZERO to ONE ABSORBABLE SIGN GAUGE — a relocation of the gap, not a closure — and `le_to_facet`
is the concrete site still uncovered.** A control that would satisfy the rule perturbs the
**incidence structure** (a ridge's facet list, the free/interior split, the facet or ridge
enumeration), i.e. a corruption that is not a diagonal conjugation. **Do not over-correct: the port is
faithful, the true-sign build passes, the instrument was never wrong, and *the pipeline survived the
control it was missing* stands. The defect is the description of what such a control covers.**

**N2 — the claim-(1) identity test rejects corrupted inputs.** Five named corruptions of the
*comparison* (four of the five perturb the twist or the target; only M2 perturbs which Laplacian is
used), each run on every poset with `2 ≤ n ≤ 5`:

| mutation | rejected on | vacuous on | why vacuous there |
|---|---|---|---|
| M1 — drop the sign twist (compare `L^rel` to `D − A` directly) | 82/82 | 4 | `\|L(P)\| = 1`: no off-diagonal to flip |
| M2 — use the absolute Laplacian in place of the relative one | 82/82 | 4 | the antichains (`\|L\| = 2, 6, 24, 120`): `∂F = ∅`, so `L^rel = L^abs` |
| M3 — wrong twist: `−1` on one facet, `+1` elsewhere | 72/72 | 14 | `\|L(P)\| ≤ 2`: one edge, both patterns give product `−1` |
| M4 — scale the target Laplacian by 2 | 82/82 | 4 | `\|L(P)\| = 1`: the target is the zero matrix |
| M5 — delete one edge from the target graph | 82/82 | 4 | `\|L(P)\| = 1`: no edge to delete |

and the **uncorrupted** test passes on 86/86.

**"Vacuous" is computed, not asserted.** A mutation counts as applicable on a poset only when it
actually changes one of the two matrices being compared; where it does not, demanding rejection
would be demanding a false negative. The counts are reported so the reader can see the reach of
each mutation, and the `|L(P)|` values on which each is vacuous are printed by `controls.py` rather
than asserted here. M3's 14 vacuous cases are exactly the posets with `|L(P)| ≤ 2`: with one edge,
both sign patterns give the product `−1` across it, so the mutation is genuinely not a mutation
there.
**This is the failure direction this program has been burned by** (a control that passes because it
cannot fail), so it is stated in the open rather than left to be discovered.

---

## §6 — The computation (ticket steps 2–4)

`code/face_geometry/run_probe.py`; output committed at `probe_output_n6.txt`.

### §6.1 Population tested

**All posets up to isomorphism on `n = 1,…,6` elements — 405 in total** (`1 + 2 + 5 + 16 + 63 + 318`,
matching A000112, checked by P2). Not a sample: the complete isomorphism-class enumeration at each
size. Largest instance: the `n = 6` antichain, `|L(P)| = 720`.

### §6.2 Result

| `n` | posets | claim (1) | claim (2) | claim (3) weak | claim (3) strong | max `\|L(P)\|` |
|---|---|---|---|---|---|---|
| 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| 3 | 5 | 5 | 5 | 5 | 5 | 6 |
| 4 | 16 | 16 | 16 | 16 | 16 | 24 |
| 5 | 63 | 63 | 63 | 63 | 63 | 120 |
| 6 | 318 | 318 | 318 | 318 | 318 | 720 |
| **all** | **405** | **405** | **405** | **405** | **405** | |

**Population tested and population it holds on are the same set: all 405.** No witness against any
of the three claims exists in the tested population.

### §6.3 The twist is load-bearing, not cosmetic

The *untwisted* form of claim (1) holds on **6 of 405** posets, and of claim (2) on the same 6 —
and all 6 have `|L(P)| = 1` (the chains, one per `n`), where both sides are the zero `1×1` matrix.
So on every poset with more than one linear extension, the twist is required. This is the datum
behind the correction in §0.

### §6.4 The identity is not degenerate

An identity that holds only where both sides are trivial is not a bridge. Define **non-degenerate**
as: the adjacent-transposition graph has at least one edge (`|L(P)| ≥ 2`, so `A ≠ 0`) **and** at
least one ridge is free (so `L^rel ≠ L^abs` and claim (3) has content).

**394 of the 405 posets are non-degenerate, and claim (1) holds on all 394.** The 11 excluded are
the 6 chains (`|L(P)| = 1`) and the 5 antichains with `n ≥ 2` (no free ridge). Both sides are
non-trivial on the remaining 394 — for instance at `n = 6` the largest non-degenerate instance has
`|L(P)| = 360`.

### §6.5 Failure modes (ticket step 4)

| subclass | count | (1) | (2) | (3) strong |
|---|---|---|---|---|
| antichain (`L(P) = S_n`) | 6 | 6 | 6 | 6 |
| chain (`\|L(P)\| = 1`) | 6 | 6 | 6 | 6 |
| **disconnected** | 108 | 108 | 108 | 108 |
| **non-trivial `Aut(P)`** | 275 | 275 | 275 | 275 |
| trivial `Aut(P)` | 130 | 130 | 130 | 130 |
| connected, not a chain, not an antichain | 291 | 291 | 291 | 291 |
| `\|L(P)\| ≥ 10` | 291 | 291 | 291 | 291 |

- **Non-trivial automorphisms: no effect.** 275 of the 405 posets have `|Aut(P)| > 1` (up to
  `|Aut| = 720` for the `n = 6` antichain) and all pass. Structurally this is expected: every object
  in the statement is built functorially from the *labelled* poset, and `Aut(P)` acts compatibly on
  both sides, so it cannot separate them.
- **Disconnected posets: no effect.** 108 of 405, all pass. (`J(P ⊔ Q) = J(P) × J(Q)`; nothing in
  Lemmas 1–4 uses connectivity of `P`.)
- **The antichain degenerates to something known, as it should.** `L(P) = S_n`, `F(P)` is the full
  Coxeter complex of `S_n`, no ridge is free, so `∂F(P) = ∅` and `L^rel = L^abs`. Theorems A and B
  then say the same thing, and it is the ambient statement: `E L E = (n−1)I − A(Cayley)` — the
  Coxeter Laplacian itself. Claim (3) is *vacuously* true here (nothing is forbidden). **This is the
  one subclass where the bridge tells you nothing you did not have**, and it is named as such
  rather than counted as a success.
- **The chain degenerates to nothing at all.** `|L(P)| = 1`, both sides the zero `1×1` matrix. Also
  counted, also not evidence.

### §6.6 A structural by-product, verified

`ker(E L^rel_top E) = ker(D − A)` has dimension **1 for all 405 posets**. This is the relative top
homology `H_{n−2}(F(P), ∂F(P); Q)`, and its being 1-dimensional is exactly the classical
connectivity of the adjacent-transposition graph on `L(P)`, read on the other side of the bridge
(§8.2). The generator is the twisted all-ones vector `Σ_w sgn(w)·σ_w` — the relative fundamental
class of `F(P)`.

---

## §7 — "Relative" is not defined in the source. Which reading, and why

The sketch never defines the relative Hodge Laplacian. The probe adopts **relative to the boundary
subcomplex `∂F(P)` generated by the free ridges**, and this must be labelled as an interpretation.

Three reasons to believe it is the intended one, given in order of strength:

1. **Claim (3) selects it.** Under this reading the difference `L^abs − L^rel` is precisely the
   forbidden-generator count and the free ridges are precisely the forbidden generators — which is
   what the sketch's claim (3) says, in the sketch's own words ("the boundary correction records
   precisely the forbidden generators"). A reading of "relative" that did not make claim (3) come
   out true would be the wrong reading of a document that asserts claim (3).
2. **Lemma 3(a) makes it well-posed.** "Relative Hodge Laplacian" is standard for a
   manifold-with-boundary; `F(P)` is not a manifold, but Lemma 3(a) shows it is a **pseudomanifold
   with boundary** (every ridge in one or two facets), which is exactly the structure the relative
   top Laplacian needs.
3. **It is the only reading under which claims (1) and (2) are different statements.** Absolute and
   relative differ precisely on the non-antichains; without the boundary the sketch's (1) and (2)
   would be the same claim written twice.

**Labelled honestly:** the identification of "relative" is `CONDITIONAL` on this reading (§9, row
L1). Everything downstream of it is unconditional given it.

---

## §8 — The bridge, stated precisely (ticket step 5)

### §8.1 Statement

> **The bridge.** For **every finite poset `P`** on `n` elements, with `F(P)` the compatible face
> complex, `∂F(P)` its boundary subcomplex (free ridges), the standard simplicial inner product
> (faces orthonormal, **unweighted**), and `E = diag(sgn w)`:
> ```
>          Δ_AT  =  E · L^rel_top(F(P)) · E
> ```
> where `Δ_AT = Σ_t (1 − τ_t) = D − A` is the unweighted adjacent-transposition Laplacian on `L(P)`.
> `E` is a signed permutation matrix and an involution, so this is **equality of matrices after a
> relabelling of basis vectors by signs** — not similarity up to an unknown conjugator, not equality
> up to normalisation, not an isospectral coincidence.

**Class of poset:** all finite posets, no restriction. **Normalisation:** unweighted; `Δ_AT` as
written, with no `1/(n−1)` and no degree normalisation. **The twist:** `E = diag(sgn)`, unique up to
global sign (§4).

### §8.2 What a statement on one side becomes on the other

| on the dynamics side (`L(P)`, `Δ_AT`) | on the geometry side (`F(P)`, Hodge) |
|---|---|
| the full spectrum of `Δ_AT` | the full spectrum of the top relative Hodge Laplacian of `F(P)` — **identical multiset** |
| `ker Δ_AT` (the constants) | `H_{n−2}(F(P), ∂F(P); Q)`, the relative top homology |
| the adjacent-transposition graph on `L(P)` is **connected** | `F(P)` has a **unique relative fundamental class** — `dim H_{n−2}(F,∂F) = 1` (verified: all 405) |
| the spectral gap `λ_2(Δ_AT)` | the **first nonzero eigenvalue of the top relative Hodge Laplacian** of `F(P)` |
| the forbidden generators at `w` | the free ridges of the facet `w` — the local geometry of `∂F(P)` (Theorem C, strong form) |
| the *ambient* Coxeter Laplacian, compressed to `C[L(P)]` | the top **absolute** Hodge Laplacian of `F(P)` (Theorem B) |
| what the compression loses when passing `S_n → L(P)` | the boundary correction `L^abs − L^rel` (Theorem C) |

**(F5, repaired — the `λ_2` row no longer says "hence the mixing time".)** The bridge carries the
*eigenvalue*, and that is all it carries. `λ_2` alone does not determine a mixing time; and the chain
whose mixing time one would want is generated by `(1/(n−1))(D−A)`, not by `D−A` — §8.3(4) covers the
constant, but the *"hence"* was never covered by anything in this document.

The last two rows are the most useful pairing: **the difference between "restrict the ambient
dynamics" and "build the dynamics intrinsically" is exactly the difference between absolute and
relative Hodge theory on `F(P)`.** That is a genuine reframing of the ambient-vs-intrinsic question
in the ticket's sense — a statement about `S_n` and a statement about the geometry of `F(P)` become
the same statement.

### §8.3 What the bridge does NOT carry — read this before quoting §8.1

Each of these is a scope boundary that Theorems A–C do **not** cross. None is a conjecture about
which the probe is agnostic; each is something simply not established.

1. **It supplies no bound and no new tool.** `Δ_AT` and `E L^rel E` are the same matrix. Any
   statement true of one is true of the other *because they are equal*, which is why the dictionary
   is exact and also why it is, on its own, free of content. Whether it has leverage depends
   entirely on whether the Hodge side carries techniques the graph side does not — **the probe did
   not test that and takes no position on it.**
2. **Nothing about BK.** Claims (1)–(3) concern adjacent transpositions only. Block moves are not
   adjacent transpositions; no part of the proof touches them. The sketch's §"Connection to BK-Type
   Dynamics" is explicitly conditional (*"If block moves can be realized as…"*) and this probe
   neither supports nor undermines it.
3. **Only the top two dimensions are used.** The proof of (1)–(3) uses facets and ridges — i.e.
   `Sur_iso(P,[n])` and `Sur_iso(P,[n−1])` — and nothing else. The sketch's suggestion that the
   higher-codimension faces "record commuting moves, braid relations, and local factorization
   structure" is **untested here** and receives no support from (1)–(3).
4. **Unweighted only.** The identity is for the standard inner product with faces orthonormal. The
   *normalised* Laplacian `D^{-1/2}(D−A)D^{-1/2}` is **not** a scalar multiple of `D−A` when `D` is
   non-constant, and is **not** the top relative Hodge Laplacian in this inner product. Uniform
   rescalings *are* covered: the lazy chain `(1/(n−1))Σ_t τ_t` has generator `(1/(n−1))(D−A)`, an
   overall constant. Any weighted chain (non-uniform generator rates, a non-uniform stationary
   measure) would need a weighted Hodge Laplacian, which is **not tested and not proven**.
5. **It does not build `A(P)`.** No operator algebra was constructed; see §10.
6. **The left-regular-band product is unused.** The sketch equips `F(P)` with an LRB product by
   refinement. Claims (1)–(3) never use it; the probe treats `F(P)` purely as a simplicial complex.

---

## §9 — Claim ledger

Labels: **PROVEN** = proof given here, all finite posets. **PROVEN-by-computation (population)** =
verified by exhaustive computation on a stated population, no proof. **CONDITIONAL (condition)**.
**HEURISTIC**. Reductions asserted in prose are included, as the ticket requires.

| # | claim | label | population / condition |
|---|---|---|---|
| L1 | "relative" in the source means relative to the boundary subcomplex generated by the free ridges | **CONDITIONAL** | the source does not define it; three reasons in §7, the strongest being that claim (3) is true only under this reading. Everything below is unconditional *given* L1. |
| L2 | `Sur_iso(P,[k])` ≅ chains of `k−1` proper nonempty ideals; `F(P) = Δ(J(P)∖{∅,P})` | **PROVEN** (Lemma 1) | all finite posets; independently checked on all 24 posets `n ≤ 4`, all `k` |
| L3 | `F(P)` is pure of dimension `n−2` with facets `≡ L(P)` | **PROVEN** (Lemma 2) | all finite posets; checked `n ≤ 4` |
| L4 | every ridge of `F(P)` lies in exactly 1 or 2 facets (`F(P)` is a pseudomanifold with boundary) | **PROVEN** (Lemma 3(a)) | all finite posets; checked `n ≤ 4`. Uses only distributivity of `J(P)` |
| L5 | free ridges at `w` ↔ forbidden generators at `w`, bijectively | **PROVEN** (Lemma 3(b)) | all finite posets; checked as a set equality on all 405 posets `n ≤ 6` |
| L6 | two distinct facets share at most one ridge | **PROVEN** (Lemma 4) | all finite posets |
| L7 | `L^abs_top = (n−1)I + A` and `L^rel_top = D + A` | **PROVEN** (§4, from L2–L6) | all finite posets |
| **A** | **claim (1):** `E · L^rel_top · E = D − A = Σ_t(1−τ_t)` | **PROVEN** (Theorem A) | **all finite posets.** Also **PROVEN-by-computation** on all 405 posets up to iso with `n ≤ 6`, of which 394 are non-degenerate |
| **B** | **claim (2):** `E · L^abs_top · E =` compression of `Σ_i(1−s_i)` from `C[S_n]` | **PROVEN** (Theorem B) | all finite posets; computation as above |
| **C1** | **claim (3), strong:** free ridges at `w` are in bijection with the forbidden generators at `w` | **PROVEN** (Theorem C / L5) | all finite posets; computation as above |
| **C2** | **claim (3), weak:** `L^abs_top − L^rel_top = diag(#forbidden generators)` | **PROVEN** (Theorem C) | all finite posets; computation as above |
| C3 | the *Laplacian difference alone* identifies **which** generators are forbidden | **FALSE as stated** | it is a diagonal matrix and records only the **count**. The identification of *which* lives in the face incidence (C1), not in the matrix. The source's "records **precisely** the forbidden generators" is correct in reading C1 and an overstatement in reading C2. |
| D | the twist is needed for claim (2) as well as claim (1) | **PROVEN** + **PROVEN-by-computation** | untwisted (1) and (2) each hold on 6 of 405 posets, all with `\|L(P)\| = 1` |
| D2 | claim (2) is true for the **right/position** action of `s_i` and **FALSE** for the left/value action — the left/value reading fails on the antichain at **every `n ≥ 3`** | **PROVEN** (§4, Corollary B′) + **PROVEN-by-computation** | **all finite posets** for the positive half (Theorem B); the refutation of the left/value reading is **proved for every `n ≥ 3`** (Corollary B′: `s_1 s_2` is a right-neighbour of `s_1` and not a left-neighbour; at `n = 2` the two readings coincide). Computation: the left form holds on only 3/5, 5/16, 8/63 posets at `n = 3,4,5`, and the antichain witness is verified to `n = 8` (audit `out_extra.txt`, X2). The source does not state the side; the position reading is forced by Lemma 3(b). **(F1: this row was labelled `PROVEN-by-computation` on `n ≤ 5` while §0 asserted the universal in `n`. Upgraded with the audit's proof — the statement was true and the label was wrong.)** |
| E | `E = diag(sgn)` is the unique diagonal `±1` twist up to global sign | **PROVEN** (§4) | all finite posets; uses connectivity of the adjacent-transposition graph on `L(P)` (classical, not proved here — see H1) |
| F | `dim H_{n−2}(F(P), ∂F(P); Q) = 1`, generated by `Σ_w sgn(w) σ_w` | **PROVEN-by-computation** | all 405 posets `n ≤ 6`. Equivalent to H1 given Theorem A, so it is *proven* modulo the classical fact, but the probe verified it rather than citing a proof |
| G | `ker L^abs_top = H_{n−2}(F(P)) =` 1 iff `P` is an antichain, else 0 | **PROVEN-by-computation** | all 405 posets `n ≤ 6`, by two independent code paths (P4, P5) |
| H1 | the adjacent-transposition graph on `L(P)` is connected | **cited, not proved here** | classical; used only in claim E (uniqueness of the twist) and to interpret F. Nothing in Theorems A–C depends on it |
| H2 | the bridge gives leverage — i.e. Hodge theory supplies tools the graph picture does not | **HEURISTIC / untested** | the probe took no position; §8.3(1) |
| H3 | higher-codimension faces of `F(P)` record braid relations / commuting moves / factorisation | **untested** | not used anywhere in (1)–(3); §8.3(3) |
| H4 | the identity extends to weighted or normalised adjacent-transposition chains | **untested** | §8.3(4). The uniform lazy rescaling *is* covered (constant multiple); degree-normalisation is **not** |
| H5 | BK / block-move operators relate to this geometry | **untested** | §8.3(2) |

---

## §10 — Recommendation (recommend, do not act)

The ticket says: if GREEN, the operator-algebra construction is the next ticket, and pm-onethird
scopes it. `A(P)` was **not** built. Two observations offered as scoping input, not as work:

- **The foundation claims (1)–(3) supply** is **sound and is a theorem, not an example.** The
  operator-algebra ticket does not need to re-establish *that* much. **(F4, repaired: this bullet
  originally read "the foundation the sketch rests on", which is wider than what was proved. The
  sketch also rests on the left-regular-band product (§8.3(6), unused here), the higher-codimension
  faces (§8.3(3), untested), the Young-module picture (never touched) and the BK realisation
  (§8.3(2), untested). None of those is established by Theorems A–C, so none of them is covered by
  "the foundation" in this bullet.)**
- **The cheapest next probe is not `A(P)`.** Theorems A–C use only the top two dimensions of
  `F(P)`, so they say nothing about whether the *rest* of the complex carries dynamical content.
  The program's actual bet (§8.3(1)) is that the Hodge side has tools the graph side lacks. A
  probe of *that* — pick one concrete Hodge-theoretic technique for the top relative Laplacian of a
  pseudomanifold-with-boundary and ask whether it says anything non-trivial about `λ_2(Δ_AT)` —
  would price the program's central bet far more cheaply than constructing `A(P)`. Offered as a
  recommendation; the routing decision is pm-onethird's.

---

## §11 — Self-audit (Appendix A steps 4c, 4d)

Run on this document before submission, per the standing process. Recorded rather than merely
performed, because the arc is five-for-five on sound arithmetic with an over-wide generalisation.

**Step 4d — what is the most general statement this document writes, and what does its
establishing instance hold fixed?** The most general statements are **Theorems A, B, C**, quantified
over *all finite posets*. They are supported by a **proof** (§3–§4), not by generalisation from the
405-poset computation — which is the specific hazard the ticket named. The proof's inputs, stated so
they can be attacked: (i) `J(P)` distributive, hence rank-2 intervals are chains or diamonds
(Lemma 3(a) — this is where finiteness and the poset axioms enter, and it is the load-bearing step);
(ii) `J(P)` graded by cardinality (Lemma 2); (iii) the standard simplicial signs and the orthonormal
inner product (§4); (iv) reading L1 of "relative". **No step uses `n ≤ 6`, connectivity of `P`,
triviality of `Aut(P)`, or any property of a particular poset.** (iv) is the only one that is an
interpretation rather than a fact — it is labelled CONDITIONAL in the ledger.

**(F2b, repaired.)** This paragraph originally closed *"Removing any of (i)–(iv) breaks the result"*.
That is **false for the sign half of (iii)**, as a computed fact: replace the alternating simplicial
signs by all `+1` and both top Laplacians are **unchanged**, so claims (1)–(3) survive (NEGATIVE
CONTROL 3; audit 41/41, reproduced 86/86). The **inner-product half of (iii) is** load-bearing — the
orthonormal inner product is what makes `∂*∂` the matrix computed here, and §8.3(4) records that
degree-normalised inner products are not covered. The defensible reading of the struck clause is that
removing the alternating sign breaks *"`L^rel` is a Hodge Laplacian at all"* as a general statement
about simplicial complexes; as written it named a load-bearing input to Theorems A–C that is not one.

**Scope axes other than `n`, checked separately** (the axis the mg-09ea instance missed):
*regime* — the population is the complete isomorphism-class enumeration at each `n ≤ 6`, not a
sample from a regime, so there is no off-class inference; *inference* — the general statement is a
proof, so the instance-to-law step that has misfired five times in this arc is not being taken here;
*normalisation* — this is the axis where an over-wide reading is available, and §8.3(4) and ledger
row H4 close it explicitly (degree-normalised Laplacians are **not** covered); *object* — §8.3(2,3)
close the BK and higher-face axes.

**Step 4c — the summaries diffed against the body, clause by clause.** §0, the §8.1 box, the ledger
and the proposed `STATE.md` row (§12) are four separate summaries of one body and they fail
independently. Diffed:

- §0 says "PROVEN for every finite poset" — matches ledger rows A/B/C1/C2 and §4. It carries the
  conditional on L1 by pointing at §8 rather than by restating it, so **§0's second bullet and §8
  must not be separated when quoted**; that instruction is in §0 itself.
- §0's three corrections match rows D, D2 and C3 respectively. Correction (i) is stated as
  *extending* the twist to claim (2), not as "the source is wrong about the twist" — the source's
  claim (1) attribution is correct as far as it goes. Correction (ii) is now **PROVEN** in row D2 and
  in §0, by Corollary B′ (§4).

  > **⚠️ This bullet is where the self-audit failed, and the failure is the finding worth keeping.**
  > As submitted it read: *"Correction (ii) is labelled **PROVEN-by-computation on `n ≤ 5`** in row D2
  > and **is not** upgraded to 'proven' in §0 or §12, because no proof of the left-action failure is
  > given here — only witnesses."* Both halves were wrong about this document. §0 **did** upgrade it,
  > to *"fails on the antichain at every `n ≥ 3`"*, attributed to Theorem B — a universal in `n`
  > supported by witnesses at `n ≤ 5`. So step 4c asserted the absence of exactly the defect it was
  > checking for, in the clause it was checking, and the assertion is what let the mislabel through.
  > The external audit (mg-e0ce, F1) found it in one pass and supplied the proof that resolves it.
  > **A self-audit cannot see the sentence it is auditing** — that is the standing reason the external
  > pass is not substitutable, and it is recorded in `STATE.md` Appendix A with this instance as its
  > evidence. Note what the failure was *not*: the mathematics was right, and the repair was an
  > upgrade rather than a retraction. The mislabel was still real, and it sat in a summary.
- §8.1 carries "unweighted" and "all finite posets, no restriction" inline, not by reference.
- The strong/weak split of claim (3) is stated in Theorem C, in ledger rows C1/C2/C3, and in
  §8.3 — and row C3 is labelled **FALSE as stated** rather than being quietly dropped, because the
  source's word "precisely" is true in one reading and not the other.
- The word "bridge" appears in §0 and §8.1 and is qualified in both by §8.3(1). It is **not**
  claimed anywhere that the bridge yields a bound.

**What this self-audit cannot do.** It cannot catch an error in the part of the derivation the
author would re-read as correct. The external audit stage is not substituted for.

**What it turned out not to be able to do, which is sharper (recorded after mg-e0ce).** This is the
second deliverable in the arc to run step 4d on itself and the **first to run 4c on itself as well**.
Both self-audits were careful, and both were run in good faith on the right clauses. The defect
landed **inside the clause 4c was checking** — see the boxed note above — and the external pass found
it immediately. The limit is not carelessness and cannot be fixed by more care: **a self-audit cannot
see the sentence it is auditing.** Two things the external pass also did that no self-audit produces:
it closed **purity to `n ≤ 6` (404/404 on `2 ≤ n ≤ 6`) and the Lemma-1 cross-check to `n ≤ 5`
(87/87, all `k`)** from `n ≤ 4`, by a build that never uses Lemma 1, and it supplied the control this
battery was missing (F2). Neither is a correction; both are coverage a second instrument buys and a
re-reading does not. *(Sentence corrected 2026-07-30, mg-5630 §4.2 → mg-1319: it previously said
`n ≤ 6` for **both** checks, contradicting the corrective numbers §2 states above. Only purity reached
`n ≤ 6`. `404` vs `405` is not a discrepancy — the audit's range starts at `n = 2`.)*

---

## §12 — Proposed `STATE.md` row

Audited as an artifact per step 4c; **it carries its own conditions rather than pointing at them.**

**Status: landed (mg-78c0), with the audit's three repairs applied here first** — (1) correction (ii)
now states the `n ≥ 3` refutation as **proven** rather than importing §0's old label; (2) *"the
foundation"* named as **the foundation claims (1)–(3) supply** (F4); (3) the five mutations explicitly
**not** read as covering the construction, with the construction-side control named (F2). The row as
it stands in `STATE.md` is the authority and carries these plus the audit's own verdict; the version
below is the proposal it was derived from.

**The F4 site below is now patched, and the call is explicit (mg-5630 §4.3 → mg-1319).** The audit
found the F4 narrowing applied at §10, at §12's recommendation clause and in the live `STATE.md` row,
but **not** in this proposed row's *subject line*, and judged it a stale-proposal artifact rather than
a live over-claim because the disclosure note above exists. **The call taken here: patch it, and keep
the provenance visible in-line rather than rely on the disclosure.** Reason — a reader who lands on
the block below by search or by quotation does not necessarily read the note above it, and *"the
foundation"* unqualified is exactly the phrase F4 was raised to remove; an unpatched site a future
reader finds without the disclosure is how a narrowing silently un-narrows. The original wording is
preserved in the marker so nothing about what was proposed is lost. **Two further sizings below are
superseded by the mg-5630 audit and are corrected in §5 and in the live `STATE.md` row, not here:**
the construction-side control's coverage (**one absorbable sign gauge, a relocation of the gap, not a
closure**) and the all-`+1` row's citation.

**⚠️ THAT LAST CALL IS REVERSED — the sizings below are now marked in-line as well (2026-07-30,
mg-f7bc F1, landed by mg-f2e1).** mg-1319 applied the reasoning in the paragraph above to F4's subject
line and declined it, **in the same line of the same file**, for the `38/38` truncation and for the
closure reading — and then asserted in `STATE.md` and in its commit message that *"the truncation is
flagged at every site where `38/38` appears"*, which this block made false. **A disclosure paragraph is
not a flag.** The argument that justified patching F4 in-line justifies patching these; holding both
positions in one commit is the inconsistency, not either position on its own. The block below therefore
carries `⟪…⟫` markers at both sites, with the proposal's original wording preserved inside each.

> **GREEN · PROVEN, all finite posets (mg-276d; computation permitted and used — 405 posets, controls both directions)** | the **foundation claims (1)–(3) supply** for the intrinsic face-geometry program ⟪F4 — subject line narrowed 2026-07-30 by mg-1319; as originally proposed it read *"the **intrinsic face-geometry program's foundation**"*⟫ (doc: `OneThird-Intrinsic-Face-Geometry-Probe.md`; audit: `OneThird-Intrinsic-Face-Geometry-Probe-IndependentAudit.md`; code: `code/face_geometry/`, `run_all.sh`, ~17 s) | **All three `n = 4` claims in `intrinsic_face_geometry_program.tex` are theorems for every finite poset, not `n = 4` coincidences.** With `F(P)` the compatible face complex — which is exactly the order complex of the proper part of `J(P)`, pure of dimension `n−2`, with facets `L(P)` and **every ridge in 1 or 2 facets** (a pseudomanifold with boundary; this is the structural fact that makes "relative" well-posed) — and `E = diag(sgn w)`: **(1)** `E·L^rel_top·E = D − A = Σ_t(1−τ_t)`, the unweighted adjacent-transposition Laplacian, as an **equality of matrices**; **(2)** `E·L^abs_top·E = (n−1)I − A =` the compression of `Σ_i(1−s_i)` from `C[S_n]`; **(3)** the free ridges at `w` are in **bijection** with the generators forbidden at `w`, and `L^abs − L^rel` is the diagonal count of them. **Three corrections to the source.** (i) The twist is attached to claim (1) only in the sketch but is **equally required for claim (2)** — untwisted, (1) and (2) each hold on only 6 of 405 posets, all of them chains with `\|L(P)\| = 1`. (ii) The sketch writes `Σ_i(1−s_i)` without saying which side `s_i` acts on, and **the two readings are not interchangeable**: claim (2) is true for the **right/position** action and **false** for the left/value one, which holds on only 3/5, 5/16, 8/63 posets at `n = 3,4,5`. The **antichain refutes the left/value reading at every `n ≥ 3`, and that is PROVEN** (two lines: `s_1 s_2` is a right-neighbour of `s_1` and not a left-neighbour; at `n = 2` the readings coincide) — verified computationally to `n = 8`. The position reading is forced — the ridge move swaps `w_t` with `w_{t+1}`. (iii) *"records **precisely** the forbidden generators"* is true at the level of the **complex** (which ones) and an overstatement at the level of the **Laplacian difference**, which is diagonal and records only **how many**. **One interpretation, labelled CONDITIONAL:** the source never defines "relative"; the probe reads it as relative to the boundary subcomplex generated by the free ridges, which is the reading claim (3) itself selects. Everything else is unconditional given it. **Population:** all 405 posets up to isomorphism with `n ≤ 6` (A000112-checked), of which **394 are non-degenerate** (`\|L(P)\| ≥ 2` **and** at least one free ridge) — so this is not an identity between two trivial objects; and separately the general statements are **proved**, so the population is all finite posets. **No failure mode found:** 275 posets with non-trivial `Aut`, 108 disconnected, all pass; the antichain degenerates correctly to the ambient Coxeter Laplacian (`∂F = ∅`, `L^rel = L^abs`) and is **named as the one subclass where the bridge says nothing new**; the chain degenerates to `0 = 0`. **Controls both directions:** homology reproduced on `S¹`/`S²`/disc/wedge, A000112 counts, `Sur_iso` cross-enumerated against chains, `∂∘∂ = 0`, and `ker L^abs_top` agreeing with `H_{n−2}(F(P))` computed by a **disjoint code path** — plus **five named mutations of the identity test, each rejected on 100% of the posets where it bites**, with vacuity *computed* and reported (M3 is vacuous exactly where `\|L(P)\| ≤ 2`). **Those five do not cover the construction:** four of them perturb the twist or the target, and the submitted battery had **no negative control on the boundary-matrix construction** — the one that looked like it did (all-`+1` simplicial signs) runs on the homology path and **cannot fire on the Laplacian at all** (both top Laplacians are unchanged by it). The construction-side control is the **audit's** (`code/face_geometry_audit_e0ce/audit_extra.py` X3, facet-parity signs, fires 38/38 where `\|L(P)\| ≥ 2` ⟪`38/38` IS ON A TRUNCATED POPULATION — flagged here 2026-07-30 by mg-f2e1 (mg-f7bc F1): `construction_side_control()` iterates `posets_upto_iso(n)[:20]` for `n = 3,4,5`, so its population is 41 = 5+16+20 and at `n = 5` it saw 20 of the 63 posets, in enumeration order. The number that matters is the port's complete `n ≤ 5` population, 82/82. mg-1319 asserted the truncation was *"flagged at every site where `38/38` appears"*; this was the site it was not, in the same line it had already patched in-line for F4.⟫), now adopted into the probe's own battery as NEGATIVE CONTROL 3 (fires 82/82 on all posets `n ≤ 5`) — and **the true-sign build passes it. The pipeline survived the control it was missing:** the gap was in the argument for trusting the instrument, not in the instrument. ⟪COVERAGE RE-SIZED, and this sentence read as a closure — flagged here 2026-07-30 by mg-f2e1 (mg-f7bc F1), superseded by §5 and by the live `STATE.md` row: NC3's corruption is a **diagonal `±1` gauge**, `L_parity = D·L_true·D` with `D = diag((−1)^j)` verified 82/82, hence isospectral and **absorbable into the twist** (claim (1) with parity signs and twist `E·D` passes again 86/86). So coverage of the construction went from **ZERO to ONE ABSORBABLE SIGN GAUGE — a RELOCATION of the gap, not a closure** — with `le_to_facet` the named uncovered site. *"The pipeline survived the control it was missing"* STANDS; *"the battery now covers construction"* does not.⟫ **THE HONEST NET, and it must travel with the headline: this is an exact dictionary between two descriptions of one matrix, so it carries no bound and no new tool.** Whether it has leverage depends on whether the Hodge side has techniques the graph side lacks — **the probe took no position on that and did not test it.** It also carries **nothing** about BK or block moves, **nothing** about the faces below the top two dimensions (the proof uses facets and ridges only, so the sketch's "higher faces record braid relations" is untouched), and **nothing** about weighted or degree-normalised chains (uniform rescaling *is* covered; `D^{−1/2}(D−A)D^{−1/2}` is **not** the top relative Hodge Laplacian when `D` is non-constant). The most useful pairing the bridge does deliver: **"restrict the ambient dynamics" vs "build them intrinsically" is exactly "absolute vs relative Hodge theory on `F(P)`"**, and connectivity of the adjacent-transposition graph is exactly `dim H_{n−2}(F(P),∂F(P)) = 1`. **`A(P)` was NOT built** (out of scope, per ticket). **Recommendation, not action:** the operator-algebra ticket need not re-establish **the foundation claims (1)–(3) supply** — and that is the only foundation established here: the sketch's left-regular-band product, its higher-codimension faces, its Young-module picture and its BK realisation are **all untouched**; but the cheaper next probe is to price the program's actual bet — take one Hodge technique for the top relative Laplacian of a pseudomanifold-with-boundary and ask whether it says anything non-trivial about `λ₂(Δ_AT)`. |
