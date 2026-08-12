# mg-8bc7 — audit of sections 1–4 of `docs/imports/compression.tex`

Scoped by pm-onethird off Daniel drop mg-2ffd. Source: `docs/imports/compression.tex` at 44d08ea.
The imported note is **not edited by this commit** — `docs/imports/README.md` reserves that
directory for verbatim copies and puts assessment in its own commit, which is this one.

---

## VERDICT

**pm-onethird's read of sections 1–3 is CONFIRMED, step by step, in exact rational arithmetic.**
Not one of its steps needed repair. Section 3's "**exactly**" is true, and its scope line at
:152 ("exact for every pair-orientation linear statistic") is correctly placed — a degree-2
statistic breaks the identity at 111 of the posets where one was tried, so the scope is doing
work rather than decorating a claim that would hold anyway.

**(A) — the parity/boundary asymmetry.** REAL, and worse than the ticket states: at n = 2 one of
the two terms in (\*) is **identically zero**. It perturbs **none** of (\*), (\*\*), (\*\*\*),
because none of them ever compares the two foliations — verified separately at each parity.
The n-odd/n-even difference is exact and has a one-line reason: order reversal maps position
p to n−1−p, so it **preserves** position parity iff n is even and **reverses** it iff n is odd.
Hence for n odd the pair (C_o, C_e) on P is carried to (C_e, C_o) on P^op — a genuine symmetry
up to duality — and for n even no such exchange exists. Where the asymmetry does bite is
exactly where the ticket suspected: §4/§5 may not treat Ran Π_o and Ran Π_e as interchangeable.

**(B) — invariance of the linear-statistic subspace.** The **premise is CONFIRMED** and the
**conclusion is REFUTED**, and the distinction is the finding.

* V is **not** invariant — under Π_o, Π_e, M = 2I − Π_o − Π_e, or (I − P_BK). Smallest
  certificate: the 3-element antichain, exhibited in full at `out_a3_operator.txt`.
* But (\*\*\*) is **not** merely a statement about the quadratic form. It is a **pointwise
  identity of functions**: for every f ∈ V, (I − P_BK) f and (2/(n−1)) M f are the *same
  function*, checked exactly at 8720 (poset, f) pairs. That is strictly stronger than equality
  of quadratic forms and it needs no invariance — it says the two operators **agree on** V, not
  that either preserves V. The ticket's dichotomy has a middle term and (\*\*\*) sits in it.
* The ticket is nevertheless right where it counts: because V is not invariant, §4's "the small
  eigenvalues of 2I − Π_o − Π_e" **is** about the full space and not about the space the
  reduction lives on. Three different numbers are in play, and §4 names the first while (\*\*)
  licenses the third.

**And the repair, which is this audit's own contribution.** (\*) is the **equality case of an
operator inequality that holds on all of L²**:

> ⟨f, (I − P_BK) f⟩ ≥ (2/(n−1)) ⟨f, (2I − Π_o − Π_e) f⟩ for **every** f, with equality exactly
> when f is affine on every fiber of **both** foliations.

Certified by exact rational Schur reduction at 599 posets, with the constant 2 shown optimal.
So §4's spectral program is **legitimate in the direction the (1/3)–(2/3) argument needs**:
a principal-angle lower bound on λ₂(M) bounds the **true** BK gap from below, and §5's standing
assumption that the relevant eigenfunction is linear (:217) is **not needed** for that
direction. The price is that the bound may be lossy, and a small eigenvalue of M is **not**
evidence against the program.

---

## What was checked, and against what

Every VERDICT row is decided in exact rational arithmetic (`fractions.Fraction`); no float sits
on any verdict path. Floats appear only in the two clearly-labelled eigenvalue measurement
blocks (a3.4, a5.4), computed by the Jacobi routine in `lib8bc7.py` — this host has no numpy.

`lib8bc7.py` imports **nothing** from this repository. Reusing the corpus's poset and
linear-extension code would have made agreement a second reading of one implementation rather
than a check. Its external corroboration is that the exhaustive generator returns
3, 19, 219, 4231 labeled posets at n = 2, 3, 4, 5 (OEIS A001035) and that linear-extension
counts hit n! on antichains and 1 on chains at every n ≤ 7.

| arm | subject | population |
|---|---|---|
| `a0_selftest` | the instrument, before it may check anything | closed forms, hand-computed cases |
| `a1_fibers` | §1, the cube foliation | every labeled poset to n = 5 (4472) + 120 sampled at n = 6, 7; 52,643 fibers, 154,737 BK edges |
| `a2_energy` | §2 and §3, (\*) and (\*\*) | 4400 posets, 8800 statistics |
| `a3_operator` | §4, (\*\*\*), and question (B) | 8720 (poset, f) pairs pointwise; 4320 for invariance; 186 for eigenvalues |
| `a4_parity` | question (A) | 4196 posets for edge counts, 4420 statistics split by parity |
| `a5_general` | the operator inequality | 599 posets (209 at n ≤ 4 + 390 at n = 5), exact PSD, \|L(P)\| ≤ 48 |

90 rows, 90 PASS. Measured wall clock for `./run_all.sh` on this host: **27.6 s**.

---

## Sections 1–3: pm-onethird's read, confirmed

The ticket asked for confirmation or refutation of a specific sketch rather than a fresh
derivation. Taking its three steps in turn:

**§1.** "Fixing the even prefixes fixes each block B_j as a SET and fixes all cross-block order.
… legality does not couple distinct blocks … So the fiber really is Q^d." **Confirmed**, and the
check is stronger than the count: a1.1 verifies the fiber is *exactly the product set* of
per-block orientations, not merely a set of size 2^d — a count can be right for the wrong
reason, a set equality cannot. 0 violations over 52,643 fibers. "The odd swaps are exactly the
cube edges" is confirmed as an equality of edge sets (a1.2), and G_BK is the **edge-disjoint**
union of the two foliations (a1.3).

One remark on the note rather than on the ticket: :62 justifies the decomposition by
"non-neighbouring swaps act on disjoint position pairs". Disjointness is necessary but is not
what makes the fiber a full cube; what does is that every cross-block relation is already
determined by F, which is the ticket's own argument and is the correct one.

**§2.** "f = a_F + Σ c_Bj Z_j with Z_j iid Bernoulli(1/2), so Var(f|C_o) = (1/4) Σ c_Bj², no
covariance terms." **Confirmed** exactly (a2.1, a2.2), including the affine form itself and not
only the variance it implies.

**§3.** "Σ_j (f − f after flipping j)² = Σ_j c_j² = 4 Var(f|F). Feed that through the
uniform-adjacent-position normalization and the factor 2/(n−1) comes out exactly as claimed."
**Confirmed** (a2.3.1–3.4): E_o, E_e, (\*) and (\*\*) all hold as exact rational equalities, with
the left side computed from the **chain** — a sum over legal adjacent transpositions that knows
nothing about cubes — and the right side from the **foliations**.

**One scope condition the ticket did not name, added here.** The constant 2/(n−1) is tied to the
normalization §3 states at :106 ("choosing one of the (n−1) adjacent positions uniformly").
Under the lazy variant — draw a position, then swap with probability 1/2 — the Dirichlet form
halves while E Var(f|C) does not, and the constant becomes 1/(n−1) (a2 control N5, 0/268
disagreements). §3 states its normalization; §4's (\*\*\*) reuses P_BK without restating it, so
the constant travels only as far as that sentence does. This is a scope note, not a defect.

---

## (A) Parity / boundary asymmetry

**The asymmetry is real and the ticket's count is right.** Measured at a4.1: at n even there are
n/2 odd swap positions and n/2 − 1 even ones (C_e carries singletons at *both* ends); at n odd
there are (n−1)/2 of each (one singleton each, at opposite ends).

**It is worse than the position count.** Edge counts are a property of P as well as of n: over
4196 posets the ratio odd-edges / even-edges ranges over [0, 4], with 184 posets having **zero**
even edges and 165 having zero odd edges. The extreme case is exhibited: at n = 2, C_e = (I₁)
determines L completely, so Π_e = I, E Var(f|C_e) ≡ 0 — one of the two terms of (\*) vanishes
identically — and (\*) is **still exact**: E_BK = 1/2 = 2·(1/4 + 0).

**It perturbs none of (\*), (\*\*), (\*\*\*).** Verified separately at each parity (a4.2, n = 2…7,
4420 statistics, 0 violations in every cell). The reason it cannot: the derivation is a
per-position sum, and 2/(n−1) is a product of three things — the 1/2 in the Dirichlet form,
the 1/(n−1) of the chain's uniform position draw, and the factor 4 relating Σc² to the fiber
variance. **None of them is a count of odd versus even positions.** The two terms of (\*) are
free to be arbitrarily lopsided because the identity never compares them; it adds them.

**Does it differ for n odd vs n even? Yes, exactly.** Order reversal L ↦ (x_n,…,x₁) is a
bijection L(P) → L(P^op) sending 0-indexed position p to n−1−p. That map preserves parity iff n
is even. Therefore:

* **n odd** — C_o's grouping {p₀p₁}{p₂p₃}…{p_{n−1}} is carried to {p₀}{p₁p₂}… , i.e. to C_e's.
  The two foliations are **exchanged** by reversal-plus-duality, so any statement proved for C_o
  over *all* posets transfers to C_e. Verified as an equality of fiber-size multisets:
  0/479 violations.
* **n even** — each foliation is carried to **itself**: 0/282 violations. And the exchange
  genuinely fails at n even (197/279 posets where C_e(P) and C_o(P^op) differ), so the
  distinction is not vacuous.

**What the asymmetry costs.** The symmetric *form* 2I − Π_o − Π_e does not make the two
projections interchangeable objects: they have different ranks (a4.4 — at n = 4, rank Π_o <
rank Π_e at 127 of 219 posets and > at only 12, since C_o has more blocks, hence bigger fibers
and fewer of them). So §5's interlacing intuition (:254) may be used as intuition but **no
argument in §4 or §5 may assume the two projections play symmetric roles**, and none may assume
the extremal function is symmetric under exchanging them. At n odd, that assumption is
available up to duality; at n even it is not available at all. That is the operative answer to
(A): the asymmetry is harmless to everything the note *proves* and is a live constraint on
everything it *proposes to prove*.

---

## (B) Is the linear-statistic subspace invariant?

### B1. No — and it is not close

`a3.2`, over 4320 (poset, f) pairs with V = span{1} ∪ {1{x <_L y} : {x,y} ∈ I(P)}:

| operator | image lands back in V |
|---|---|
| Π_o | 1689 / 4320 |
| Π_e | 1647 / 4320 |
| M = 2I − Π_o − Π_e | 1441 / 4320 |
| I − P_BK | 1441 / 4320 |

(The pairs where it does land in V are the degenerate ones — chains and near-chains whose fibers
are singletons. Note that M and I − P_BK agree at **exactly** the same 1441 pairs: that is
forced by (\*\*\*), and it is an internal corroboration that the two independently-built
matrices are the objects they claim to be.)

The reason, stated so it can be checked without running anything:

> Π_o f = f − Σ_{{x,y}∈I(P)} c_{xy} · S_{xy}(L) · (1{x <_L y} − 1/2),

where S_{xy}(L) = 1 iff {x,y} is an *incomparable 2-block of L's odd decomposition*. S_{xy} is a
joint adjacency-and-position-parity function, not a pair-orientation statistic, so the
correction term leaves V. This is exactly the ticket's intuition ("sends the incomparable-block
coefficients to 1/2"), made into the obstruction.

**Smallest certificate**, exhibited in full at `out_a3_operator.txt` §a3.3 and reproducible by
hand: P = antichain on {0,1,2}, f = 1{0 <_L 1}. Π_o f takes the values 1/2, 1, 1/2, 0, 1, 0 on
012, 021, 102, 120, 201, 210. Matching against {1, 1{0<1}, 1{0<2}, 1{1<2}} forces α = 0 (from
210), β = 1 (201), δ = 0 (120), γ = 1/2 (102) — and then the fit predicts Π_o f(012) = 3/2 where
the table says 1/2. No solution. (A note on the definition: allowing coefficients on
*comparable* pairs as well does not enlarge V, since x <_P y makes 1{x <_L y} the constant 1 on
L(P). a2 control N4 confirms such terms disturb nothing.)

### B2. But (\*\*\*) is not a quadratic-form statement — it is stronger than the ticket allows

The ticket's dichotomy is "operator identity" versus "statement about the quadratic form on that
subspace". There is a middle term, and (\*\*\*) is in it: **two operators agreeing pointwise on
a subspace neither preserves.** a3.1 checks the pointwise equality of functions — not of inner
products — at 8720 (poset, f) pairs, 0 violations. Equality of quadratic forms follows; the
converse would not.

So the reduction from §3 to §4 is sound as written, and (\*\*) is a legitimate identity for
every f ∈ V. What does **not** follow is any statement about M *as an operator on V*.

### B3. Three numbers, and which one §4 names

| | quantity | what it is |
|---|---|---|
| (i) | (2/(n−1)) λ₂(M) | full space — **what §4's "small eigenvalues of 2I − Π_o − Π_e" names** |
| (ii) | λ₂(I − P_BK) | the true BK spectral gap |
| (iii) | (2/(n−1)) · min over V₀ of ⟨f,Mf⟩/Var(f) | **what (\*\*) licenses** — the smallest eigenvalue of the *compression* P_V M\|_V, not of M |

(iii) ≥ (ii) is Rayleigh (a minimum over a subspace is at least the minimum over the whole
space). (i) ≤ (ii) is the operator inequality below. Measured at 186 posets: the ordering holds
at every one, 0 violations. So the ticket is right that §4's phrase is about the full space —
**and the ordering means that is the safe direction**, not the dangerous one.

### B4. Verdict on the spectral reformulation

**Legitimate as a lower-bound route; not legitimate as an equivalence.**

* A principal-angle lower bound on λ₂(M) yields a valid lower bound on the **true** BK gap —
  for every f, not only for linear ones. §5's standing assumption at :217 is not needed for
  this direction. This is *stronger* than what the note claims for itself.
* A **small** eigenvalue of M is not evidence against the program: its witness may be a
  non-linear function far from V, and no obstruction to (1/3)–(2/3) follows from one.
* The route is lossy. On the measured population §4's quantity is strictly below the BK gap at
  27/186 posets, worst factor 1.0705.
* And the linearity assumption is doing real work: the BK gap is attained by a pair-orientation
  linear statistic at only 109 of 186 measured posets. (That does not refute :217, which is a
  claim about a particular standard-representation eigenfunction and not about the global
  bottleneck — but it does mean the assumption is not a formality.)

---

## The finding: (\*) is the equality case of a full-space operator inequality

**Claim.** With M = 2I − Π_o − Π_e and the note's normalization,

> ⟨f, (I − P_BK) f⟩ ≥ (2/(n−1)) ⟨f, M f⟩ for **every** f ∈ L²(L(P)),
> with equality exactly when f is affine (degree ≤ 1) on every fiber of **both** foliations.

**Proof sketch** (checkable by hand; the arms check it by machine). Fix an odd fiber F ≅ Q^{d(F)}
and expand f\|_F in the cube Fourier basis. §1 gives that the odd swaps inside F are exactly the
d coordinate flips, so the odd part of the Dirichlet form restricted to F is the cube Dirichlet
form, which acts on χ_S with eigenvalue 2\|S\|; while Var(f\|C_o = F) = Σ_{S≠∅} f̂_F(S)². Since
2\|S\| ≥ 2 with equality iff \|S\| = 1, the odd part dominates fiberwise. Same for even. Add,
and use E Var(f\|C_o) = ⟨f, (I − Π_o) f⟩. §3's hypothesis "f is degree one on every cube" (:108)
is exactly the \|S\| = 1 case, so (\*) is the equality case rather than a separate fact.

**Certification.** `a5.1`: exact rational Schur reduction of (I − P_BK) − (2/(n−1))M on the full
\|L(P)\| × \|L(P)\| matrix, PSD at **599/599** posets — the 209 labeled posets to n = 4 that have
at least two linear extensions (a poset with a unique linear extension has no BK move and the
inequality reads 0 ≥ 0), plus 390 at n = 5 with \|L(P)\| ≤ 48. `a5.2`: every linear statistic attains equality, and ker D is
*exactly* the fiber-affine space — computed by two independent routes (null space of D; and the
vanishing of every order-2 cube difference) which agree at 112/112 posets. The equality case is
strictly **larger** than V at 37 of those 112 posets: being affine on every fiber is weaker than
being a pair-orientation linear statistic.

**Controls.** C1 — the reverse inequality fails at 139/192 posets, so the two operators are not
equal and the finding is not vacuous. C2 — raising the constant to (5/2)/(n−1) breaks PSD at
**192/192** posets, so 2 is optimal. C3 — lowering it to 1/(n−1) keeps PSD at 0/192 failures, so
C2 is not merely "any change breaks it".

**Consequence for the program.** λ₂(I − P_BK) ≥ (2/(n−1)) λ₂(M), unconditionally. This is what
makes §4's reformulation usable despite (B): the object §4 proposes to bound is the full-space
one, and the full-space one is exactly the one that bounds the true gap in the useful direction.

---

## What this audit does NOT establish

* **Nothing about §5**, which is out of the ticket's scope (sections 1–4). Its equivalence claim
  is consistent with (\*\*) being an identity, but its final inequality is not assessed.
* **Nothing asymptotic.** Every population here is n ≤ 7, and the eigenvalue measurements are
  n ≤ 5 with \|L(P)\| ≤ 60 (a3.4) and ≤ 24 (a5.4). The lossiness figure **1.0705 is a statement
  about tiny posets** and carries no information about how the route behaves as n grows. It is
  the single number here most likely to be misread as more than it is.
* **The operator inequality is proved by hand and certified on a finite population**, not
  machine-verified in general. The proof sketch above is the warrant; a5.1 is corroboration at
  599 posets, not a proof.
* **Connectivity of G_BK is relied upon and not proved here** — it is what makes ker M = ker(I −
  P_BK) = constants, so that "λ₂" means the same thing in both. It is standard, and it is
  corroborated on the measured population by λ₂ > 0 at all 186 posets in a3.4.
* **No claim about which f is the (1/3)–(2/3) obstruction**, and no claim that the standard
  representation eigenfunction is linear. :217's assumption is left exactly as the note leaves
  it, with one measurement (109/186) attached to it.
* `docs/imports/compression.tex` **is not edited**, and neither is `STATE.md`.

---

## Defects of my own

**D1 — the routine that carries the audit's main verdict was wrong, and a hand-known case
caught it.** `psd_exact`'s zero-pivot branch scanned the *whole* row including already-eliminated
entries, so it reported the rank-1 PSD matrix [[1,1],[1,1]] as **not** PSD. That is the routine
a5.1 uses. Had a0.3 not carried a hand-known PSD case *with a zero pivot*, a5.1 would have
reported violations and I would have concluded my own inequality was false. Fixed at
`lib8bc7.py`; the comment there names this defect.

**D2 — my first control could not fire, and said so.** a1's original M1 replaced the even
foliation with the odd one. But the odd foliation is a *valid* foliation, so every check
correctly passed and the control reported 0/278 — a planted "defect" that was not one. Replaced
with the parity mismatch (C_e's fibers paired with the odd swap positions), which is an actual
wrong reading of :51 and which fires at 215/278.

**D3 — a sample rendered as a sweep, inside an audit whose subject includes exactly that.**
a5's population was the full n ≤ 5 list shuffled and truncated to 600, which left **2 of the 19**
posets at n = 3 while the row read like a sweep. Fixed: all of n ≤ 4 exhaustively (of which the
209 with ≥ 2 linear extensions are actually tested), sampled only at n = 5, and the composition
is printed in the transcript rather than left to be inferred from the row.

**D4 — the eigenvalue measurements are capped and the caps are load-bearing.** a3.4 caps
\|L(P)\| ≤ 60, a5.4 caps ≤ 24. The 1.0705 figure and the 109/186 figure are both statements
about what fits under those caps. Not fixed — stated, here and in the transcripts.

**D5 — one of my two harness positive controls did not land where I expected.** Corrupting
`legal_at` (so a comparable pair counts as swappable) leaves a1 **green** and turns a2–a5 red.
That is not a1 being blind: a1's edge sets are decided by membership in the fiber rather than by
`legal_at`, so the mutation cannot reach it. I record it because I predicted a1 would go red and
it did not, and the reason had to be found rather than assumed.

**D6 — three implementations of the same idea are not three witnesses.** a2's (\*) check, a3's
(\*\*\*) check and a5's PSD check all share `lib8bc7`'s fiber and Dirichlet-form code. They test
different claims but they are not independent of each other; a defect in `fibers()` or
`bk_energy()` moves all three together. a0 is the only thing standing between that and a false
green, which is why `run_all.sh` refuses to proceed when a0 fails.

**Harness positive controls.** `run_all.sh` was shown to go red, twice, by real edits to
`lib8bc7.py` restored under a checked `sha256`: (1) reinstating D1's bug — a0 fails, the run
**gates** and exits 1 without running the audit arms; (2) corrupting `legal_at` — a0 passes and
four audit arms fail, exit 1. A merge-gate-shaped script that has never been seen to fail is not
known to be able to fail (mg-06d1's D2).

---

## Running it

```sh
code/compression_audit_8bc7/run_all.sh     # ~27.6 s, writes out_*.txt beside each arm
```

Standard library only. a0 gates: if the instrument self-test fails, the audit arms do not run.
