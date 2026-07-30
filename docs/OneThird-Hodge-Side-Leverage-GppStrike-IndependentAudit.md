# Independent audit of mg-a2bd (`1e61031`) — the strike of ledger row `G″`

**Auditor:** mg-3c24 (pre-filed against mg-a2bd before mg-a2bd produced anything).
**Object audited:** `1e61031` — *"STRIKE ledger row G-double-prime …"*, which lands mg-d39d
finding **A1** and nothing else of that audit.
**Instrument:** `code/hodge_leverage_audit_3c24/` (`run_all.sh`, ~35 s) → `out_audit_join.txt`.
It imports **nothing** from `code/hodge_leverage/` or `code/face_geometry/`. It contains no
mutation and scores no control: it is a **replication**, and is labelled as one (`STATE.md`
Appendix A, *"a proof obligation must be landed as a PROOF, not as a control"*).

---

## Verdict

**OVERSTATED. 0 BROKEN mathematics.**

The strike is **right**, the mechanism recorded beside it is **right**, and — the thing this
ticket was filed to check — it does **not** over-correct. **THEOREM G STANDS**, row **G′** stands
and was **not** narrowed, **N1**, **M2**, the `2^{Θ(n)}` headline and the `A(P)` NOT-BUILT routing
are untouched, and §10 is byte-unchanged. Every committed number reproduces from a route that
shares no code with the deliverable, and the decisive spectral facts are re-decided in **exact
rational arithmetic** rather than in floating point — which turns two of the deliverable's
`≈ 0.500000` measurements into **exact** statements.

Seven findings, **none mathematical**, and all of them in the landing's claims *about itself*:

| # | severity | finding |
|---|---|---|
| **F1** | **MODERATE** | §14: mg-a2bd edited the paragraph that carries mg-d39d's still-open finding **A5**, asserted the row's being unchanged is *"a fact rather than an omission"*, and in the same commit **more than doubled the very mismatch A5 reports** (2 928 → 6 069 chars) while leaving *"the corresponding `STATE.md` row carries the same clauses"* standing |
| **F2** | MINOR–MODERATE | one commit, two incompatible site counts: §6's table says the strike touches **three** sites; §14 says it *"touches §6 and the ledger and **nothing else**"* (two) |
| **F3** | MINOR–MODERATE | the `STATE.md` row states *"the per-level max is attained exactly at the one-big-block face"* with **no condition**, attributing to Theorem **J** alone a conclusion that is J **plus** the computational base case `λ₂(F(A_m)) ≤ 1/2` — the condition both §6.1 and ledger row **G′** correctly carry |
| **F4** | MINOR | the evidence for the new Appendix A rule **mis-enumerates the brief it is about**: mg-a806 is described as *"scoped to land four things"*; the ticket has **six** (B1–B6). The conclusion survives — `G″` is none of the six — but a rule about enumerating a brief should enumerate it correctly. Two sites |
| **F5** | MINOR | *"the four at `n = 5` … i.e. **exactly** the posets where the face's other block is not a singleton"* is not a characterisation: `A_5` at `i = 0` has such a face and is **not** a counterexample |
| **F6** | MINOR | *"the repository was swept … **three sites**"* is presented as a census and omits two files that carry the row label (the mg-d39d audit document and its instrument). Both carry the **refutation**, so the operative finding — *no consumer* — is unaffected |
| **F7** | MINOR (commit message) | *"no shared eigen-route with the prediction side"* — both sides of `J1` run through `linalg.jacobi_eigenvalues`, and `J2` calls the deliverable's own `local_to_global.gammas`, whose `λ₂` is **memoised on Theorem L's block-iso-type key** across the whole population. The documents' own wording is accurate; the commit message's is not |

**A RED verdict was available and is not earned.** The mathematics of this landing is the best in
the arc so far: a false universal struck, the mechanism proved rather than asserted, the second
consequence sized **upward** rather than silently narrowed, and the whole thing checked against
48 846 links.

---

## §1 — What was rebuilt, and how disjointly

`code/hodge_leverage_audit_3c24/rebuild.py` re-derives, from the definitions and with no import
from either existing package:

| object | the deliverable's route | mine |
|---|---|---|
| posets up to iso | `face_complex.Poset.canonical_key` | lexicographically least relation over all `n!` relabellings |
| faces of `F(P)` | chains of proper nonempty ideals | **P-compatible ordered partitions**, peeled off the front |
| link 1-skeleton | brute-force count of facets containing the face | **refinements** of the face, weight = **product of linear-extension counts** of the induced subposets (DP over ideals) |
| `λ₂` decision | floating-point cyclic **Jacobi** on `D^{-1/2}WD^{-1/2}` | **exact rational inertia of `W − tD`**, i.e. `(#{λ>t}, #{λ=t}, #{λ<t})` by symmetric elimination over `Fraction` |
| full spectra | cyclic Jacobi | **Householder tridiagonalisation + implicit-shift QL** |

Calibration before use: my link 1-skeletons and my `λ₂` agree with `links.link_skeleton` +
`linalg.lambda2_weighted_graph` on **all 2 748 links of all posets `n ≤ 5`**, vertex counts and
values, 0 disagreements — so the two routes compute the same object by different means.

The exact inertia test is the substantive upgrade. `P = D^{-1}W` is self-adjoint for `⟨·,·⟩_D`, so
`f ↦ f^T(W − tD)f` is the `D`-quadratic form of `P − tI` and its inertia **is** the eigenvalue count
either side of `t`. `λ₂ < t` iff the inertia is exactly `(1, 0, |V|−1)`. No decision anywhere below
rests on a float.

---

## §2 — Target 1: did it over-correct? **NO — and the confirmations are stronger than the ones landed**

**THEOREM G STANDS.** Re-verified on my own Coxeter complex built from the closed-form weights
`w(S) = |S|!(m−|S|)!`: the eigenfunction identity `(Pf)(S) = f(S)/2` holds **exactly, residual 0 in
rational arithmetic**, for `A_3 … A_9` under two independent `a`-vectors. The proof is `n`-free and
I could not break it.

**Stronger than what is on the page:** the deliverable and `out_verify_join.txt` `J4(a)` report
`λ₂(F(A_m)) = 0.500000000000` as a *float*. Exact inertia settles it:

```
m=3  |V|=  6   inertia(W − D/2) = (1, 2,   3)     λ₂ = 1/2 EXACTLY
m=4  |V|= 14   inertia(W − D/2) = (1, 3,  10)     λ₂ = 1/2 EXACTLY
m=5  |V|= 30   inertia(W − D/2) = (1, 4,  25)     λ₂ = 1/2 EXACTLY
m=6  |V|= 62   inertia(W − D/2) = (1, 5,  56)     λ₂ = 1/2 EXACTLY
m=7  |V|=126   inertia(W − D/2) = (1, 6, 119)     λ₂ = 1/2 EXACTLY
m=8  |V|=254   inertia(W − D/2) = (1, 7, 246)     λ₂ = 1/2 EXACTLY
```

exactly one eigenvalue above `1/2` (the constant), `m−2` equal to it. That is row **G′**'s base case
`λ₂(F(A_m)) ≤ 1/2` promoted from *computed in floating point* to *decided in exact arithmetic*, for
`m ≤ 8`. (`m = 9`, `|V| = 510`, is outside my rational-elimination budget and is left at the float.)

**No bleed anywhere.** Checked site by site: `§0`, `§5`, `§5.3`, `§6`'s conclusion, `§7`/`N1a–N1r`,
`§9`, `§10`, `§12`, `§13`, `§14`, ledger rows `G`, `M2`, `M3`, `LG`, `S1`, and the `STATE.md` row.
`§10`'s control table is **byte-unchanged** by the commit, as claimed. The `A(P)` NOT-BUILT routing
sentence is untouched and the direction is stated correctly in three places — joins **suppress** `γ`,
which makes (LG) **weaker**, so nothing is reopened. A reader of this commit cannot come away unsure
whether Theorem G survived: `§0`, `§6`, the ledger, `STATE.md` row 136 and `out_verify_join.txt`'s
summary each say so explicitly and lead with it.

**The clean negative on `STATE.md` is CONFIRMED, not accepted.** `git show 522048f:STATE.md` — the
tree immediately before the strike — contains **zero** occurrences of `G″` and zero of the claim's
content (`"antichain of size"`). The ticket's premise *"`STATE.md` asserts a FALSE UNIVERSAL"* was
indeed wrong, the audit was right, and mg-a2bd sided with the audit.

---

## §3 — Target 2: is the mechanism recorded correctly? **YES, and Theorem J is a theorem**

Re-derived from the definition rather than read. For `X = X_1 * ⋯ * X_r` with product weights and
`D = dim X = Σ_j(p_j+1) − 1`, the 1-skeleton walk from `u ∈ X_j` picks a facet through `u` weighted
and then one of the `D` other vertices uniformly; exactly `p_j` of them lie in `X_j`, and conditioned
on landing there the step **is** `X_j`'s own walk — so `(P_X f)|_{X_j} = (p_j/D)(P_{X_j}f)` for `f`
supported on `X_j` with `⟨f, π_{X_j}⟩ = 0`. From `u ∈ X_k`, `k ≠ j`, the walk enters `X_j` at
`π_{X_j}` (this is exactly where **product weights** are used), against which `f` integrates to `0`.
The remaining `r − 1` dimensions are the functions constant `c_j` on each factor with
`Σ_j(p_j+1)c_j = 0`, on which `P_X f(u) = (p_k c_k − (p_k+1)c_k)/D = −c_k/D`. Counting:
`Σ_j(V_j−1) + (r−1) = V−1`. **Correct as stated, including the multiplicity `r−1`.**

**Scaling factor and direction both check.** `p_j/D < 1` whenever a second factor is present, since
`D ≥ p_j + p_k + 1 > p_j`; for the two-factor case `p/(p+q+1)`, exactly the ticket's form. The
direction is **suppression**: a factor's `1/2` lands strictly below `1/2`. At the smallest
counterexample `F(A_3) * F(A_2)`, `p = 1`, `q = 0`, `D = 2`, so `(1/2)·(1/2) = 1/4` — and the exact
inertia of `W − D/4` on that link is `(1, 2, 5)`: `γ_0(A_2 ⊕ A_3) = 1/4` **exactly**, not to six
decimals.

**And Theorem J holds on the whole population by my own route.** Link side: my refinement-built
weighted 1-skeleton (no Theorem L). Factor side: assembled from `F(P|_B)` alone. Full spectra
compared:

```
n=4      39 genuine-join links   0 mismatches
n=5   1 426 genuine-join links   0 mismatches
n=6  47 381 genuine-join links   0 mismatches
total 48 846                     0 mismatches, worst deviation 5.274e-16
```

exactly mg-a2bd's population and per-`n` split, by a disjoint construction and a different
eigensolver. The mechanism is not merely *recorded* correctly; it is a theorem and the strike is
right **for the right reason**.

*One point of care, not a defect:* §6.1's compact form
`λ₂(link σ) = max_j (b_j−2)/D · λ₂(F(A_{b_j})) ∨ (−1/D)` is stated inside the `A_n` discussion,
where every block is an antichain. It is **not** valid verbatim for a general poset — a 2-element
**chain** block contributes a factor with `V_j = 1`, i.e. **no** eigenvalue, whereas the compact form
would credit it with a `0`. Row **J** itself is stated correctly (a union over factor spectra) and is
the version that generalises. The document's scoping is right; a future reader lifting the compact
line out of §6.1 would be wrong.

---

## §4 — Target 3: the citation sweep, verified independently

Swept myself for the label in every form (`G″`, `G''`), for the phrase (`free from G`), and for
semantic restatements citing neither (`antichain of size`, `3-antichain`, `weaker than its own
proof`, `immediate strengthening`, `strongest true form`, `γ_i ≥ 1/2`, `every finite poset`,
`hexagon`, `braid hexagon`), across `*.md`, `*.py`, `*.txt`, `*.sh`, `*.html`.

**The substance is confirmed: NOTHING CONSUMED `G″`.** The three assertion sites the document lists
are the three that asserted it, the annotation at `…-IndependentAudit.md:413` leaves the auditor's
text verbatim as claimed, and I found **no** proof, bound, ledger row, `§0` point, `§12` routing
consequence, `§14` row, `STATE.md` row, code path or committed artifact that leans on it.

Two semantic near-misses, checked and cleared:

- **`docs/…Leverage.md:394`** — *"§6 proves `γ_i ≥ 1/2` at every level for every `n`"*. This is
  Theorem **G** (the `A_n` table of §5.3), not `G″`. Clean.
- **`docs/…Leverage.md:417`** — ***"`γ = 1/2` is not about antichains; it is about `F(P)`"***. This
  points the *opposite* way from `G″` (it says `1/2` does **not** need an antichain) and is carried
  by `M3` and the `P_4` row of Theorem H, neither of which the strike touches. Clean. Related:
  §6's *"the one thing `G″` was reached for it never covered anyway — §5.3's `C_a ⊔ C_a` has no
  3-antichain at all"* is **correct** (a width-2 poset has no antichain of size 3).

**F6 · the census undercounts.** *"the repository was swept … **Three sites**"* is presented as a
repository census. Five files carry the row label:

| file | listed by mg-a2bd? |
|---|---|
| `docs/OneThird-Hodge-Side-Leverage.md` (§6 + ledger) | yes |
| `docs/OneThird-Hodge-Side-Leverage-IndependentAudit.md:413` | yes |
| `docs/OneThird-Hodge-Side-Leverage-StateLanding-IndependentAudit.md` (~15 mentions) | **no** |
| `code/hodge_leverage_audit_d39d/{audit_gpp.py, out_gpp.txt, run_all.sh}` | **no** |
| `STATE.md` | correctly reported as **absent before the strike** |

Both omitted sites carry the **refutation**, so no false statement propagates and the operative
finding — *no consumer* — is unaffected. The table's header is *"everything `G″` was **cited by**"*,
under which the omission is defensible; the sentence *"the repository was swept … three sites"* is
the one that overshoots.

---

## §5 — Target 4: do the 55 reproduce? **YES — exactly, and the population with them**

Rebuilt from scratch, every decision exact:

```
      n=2  (poset, level) pairs with such a face=   0   γ_i < 1/2 on  0
      n=3                                     =   1                 0
      n=4                                     =   7                 0
      n=5                                     =  70                 4
      n=6                                     = 676                51
      population      : 754    (mg-a2bd: 754)  AGREE
      COUNTEREXAMPLES :  55    (mg-a2bd:  55)  AGREE
      smallest n      :   5    (mg-a2bd:   5)  AGREE
```

The four at `n = 5` are `A_2 ⊕ A_3`, `A_3 ⊕ A_2`, `A_3 ⊕ C_2`, `C_2 ⊕ A_3`, **all ordinal sums**,
all `γ_0 = 1/4` — the ticket's *"four of the five"* is wrong and mg-a2bd's correction to it (**four,
not five; all four, not four of five**) is right. The distinct `γ` values among the 51 at `n = 6` are
`1/6, 1/4, 1/3, 0.406975, 0.408367`, which contains the ledger's *"values include `1/3` and
`0.408367`"*. The per-face reading reproduces too: **3 901 of 7 989**, i.e. *"nearly half"*, as
written.

Both committed artifacts regenerate byte-identically on this machine —
`hodge_leverage_join/out_verify_join.txt` in **21.1 s** against the claimed `~21 s`, and
`hodge_leverage_audit_d39d/out_gpp.txt` in 14.7 s — so mg-a2bd's *"reproduced the audit's
`out_gpp.txt` byte-identically"* is confirmed by a third party.

**F7 · what "an independent route" means here.** `audit_gpp.py` imports nothing and is a genuine
standalone rebuild. `verify_join.py` imports `face_complex`, `links`, `linalg`,
`local_to_global` and `posets` — so `J2` re-derives the 55 with **the deliverable's own machinery**,
including `local_to_global.link_lambda2`'s memoisation of `λ₂` on `join_type(P, σ)` (the Theorem L
key) via a module-global cache shared across the entire population. Theorem L's *spectral* content
is checked only to `n ≤ 5` (ledger row **L**, and `J1` at `n = 6` is itself part of what that memo
would be assumed for). So `J2` is independent **of the audit**, not of the deliverable; the
commit message's *"no shared eigen-route with the prediction side"* is also not literally right —
`J1`'s measured and predicted spectra both go through `linalg.jacobi_eigenvalues`. §6.1's own
wording (*"the link side is measured by `links.link_skeleton` … never uses Theorem L"*) is accurate
and is the claim that matters. **My rebuild is memo-free and gets 55**, so the number is not at risk;
this is about how the independence is described.

---

## §6 — Target 5: the Appendix A rule, tested adversarially

> **A landing that adds a row beyond its brief has widened its own scope, and the added row is where
> step 4d should look first.**

**Does it fire only on the instance that generated it?** No — but it does not fire everywhere either,
and the boundary is worth recording. Three landings in this arc have been audited:

| landing | audit | would the rule have fired? |
|---|---|---|
| **mg-78c0** `c0cf104` | mg-5630 | **Yes, under the procedure.** The brief said *"Record it so the **next** deliverable's control battery covers construction as well as comparison"* and *"State this accurately: the pipeline SURVIVED the control it was missing"*. It did not authorise *"this battery **now covers** CONSTRUCTION"* — the present-tense coverage claim, which is exactly what mg-5630 struck. Under the literal *"adds a **row**"* it is a near-miss: NC3 itself **was** in brief; the unbriefed thing is the claim about it |
| **mg-a806** `16bee79` | mg-d39d | **Yes.** The generating instance |
| **mg-1319** `db08b4c` | mg-f7bc | **No.** All six mg-f7bc findings sit at **in-brief** sites — F1 and F4 are sentences the commit *edited*, F2 is a site it failed to edit, F5 is an output consequence of the A4 repair, F6 is the commit message. The rule would have pointed at an empty set while six real findings sat elsewhere |

So the rule is **not** a description of a single instance — it generalises to at least one other
landing — but it is **not a sufficient 4d targeting heuristic**, and the wording *"look **first**"*
plus *"read it as an addition to step 4d, not as a separate step"* is correctly calibrated for that.
Two observations, offered rather than asserted:

1. **It still does not fire on a `STATE.md`-only landing that adds no row.** That is the hole
   mg-f7bc's F3 named for the A5 trigger (*"run the whole rule set against a `STATE.md`-only landing
   … NOTHING FIRES"*), and the new rule does not close it. `STATE.md` does not say so.
2. **The literal noun is narrower than the procedure.** *"a **row**"* missed mg-78c0; *"enumerate
   what the commit added **BEYOND its brief**, and treat that set as the primary 4d target"* catches
   it. The procedure is the load-bearing half and should probably be the headline.

**And it fires on mg-a2bd itself, productively** — see §8. That is the strongest evidence for it.

---

## §7 — Target 6: D4's second consequence, sized both ways

**Direction 1 — was a true statement narrowed? NO, and it should not have been.** Row **G′** keeps
`A_3…A_9` and its `PROVEN-by-computation` label. I checked the claim exhaustively and exactly, over
**all faces** of `F(A_n)`:

```
A_4 i= 0   one-big-block faces=  8 (all ≥1/2)   other faces=   6 (any ≥1/2: False, max 0.000000)
A_5 i= 0   one-big-block faces= 10 (all ≥1/2)   other faces=  20 (any ≥1/2: False, max 0.250000)
A_5 i= 1   one-big-block faces= 60 (all ≥1/2)   other faces=  90 (any ≥1/2: False, max 0.000000)
A_6 i= 0   one-big-block faces= 12 (all ≥1/2)   other faces=  50 (any ≥1/2: False, max 0.333333)
A_6 i= 1   one-big-block faces= 90 (all ≥1/2)   other faces= 450 (any ≥1/2: False, max 0.250000)
A_6 i= 2   one-big-block faces=480 (all ≥1/2)   other faces=1080 (any ≥1/2: False, max 0.000000)
   → the argmax set is EXACTLY the one-big-block faces at every level
```

— face counts identical to `J4(b)`, and every *"other"* face decided **strictly below `1/2` by exact
inertia**, not by a float comparison. Extending by L + J over block-size multisets reproduces
`J4(c)` value for value to `A_9`, including the runner-up `(2,7) ↦ 5/12` at `A_9, i = 0`; the
reduction `b_j − 2 ≤ D` with equality **iff** the other blocks are singletons is correct
(`b_j − 1 ≤ Σ_k(b_k − 1)`). So the per-link computation **does** bound its whole level, `G′` is
**true as stated**, and *"do not weaken it"* was the right call.

**Direction 2 — was anything widened past its evidence?** One place, and it is not the deliverable.

**F3.** §6.1 splits the statement correctly into an **unconditional** half (`γ_i ≥ λ₂(F(A_{n−i−1}))
≥ 1/2`, Theorem G) and a half ***"Given `λ₂(F(A_b)) ≤ 1/2` for `3 ≤ b ≤ n` — the computational half,
verified for `b ≤ 9`"***; ledger row `G′` repeats the qualifier (*"what stays computational is only
the base case"*). The `STATE.md` row does not: *"the same fact repairs row `G′` upward … **the
per-level max is attained exactly at the one-big-block face**"*. It is not attained there by *"the
same fact"* alone. J gives `λ₂(link) = max_j (b_j−2)/D · λ₂(F(A_{b_j}))` and `(b_j−2)/D < 1`; to
conclude that the one-big-block face wins you still need `λ₂(F(A_b)) ≤ λ₂(F(A_{n−i−1}))`, and
unconditionally Theorem G gives only `≥ 1/2` in **both** directions. A hypothetical
`λ₂(F(A_4)) = 0.9` would put the `(2,4)` face of `A_6, i = 0` at `0.6 > 1/2`. The base case is
verified to `m ≤ 9` (and by me **exactly** to `m ≤ 8`), so the row is true on its population —
the defect is that the summary drops the population.

This matters because it is the **same shape** as mg-d39d's **A2** (*"the replacement scope clause is
an unhedged universal at 12 of 13 sites"*), which the same `STATE.md` row names as **not landed**
three lines later. The body is careful and the summary is not: step 4c, at a new site.

---

## §8 — Target 7: what mg-a2bd added beyond its brief, and what is in it

The rule this commit lands, applied to the commit landing it. The brief is D1–D5. Beyond it:

| added | in brief? | verdict |
|---|---|---|
| ledger row **G‴** (*"…one antichain of size ≥ 3 **and singletons otherwise**"*), labelled **PROVEN** | **no** | **TRUE, and the proof is right.** Tested rather than accepted: **381** (poset, level) pairs meet the hypothesis over `n ≤ 6`, **0** have `γ_i < 1/2`; the stronger per-face form holds on **4 088 of 4 088** faces. The proof is sound for all finite posets — a singleton block gives `F(A_1) = ∅`, which is the join identity, so `link(σ) ≅ F(A_m)` on the nose and Theorem G's `n`-free eigenfunction applies verbatim. **But note the shape: an unrequested `PROVEN` ledger row is precisely what produced `G″`.** It survives only because it was *also* true |
| ledger row **J** + §6.1 with a full proof | yes (D2: *"write that argument into the ledger"*) | correct; the proof is complete |
| `code/hodge_leverage_join/` (~600 lines, 4 checks) | no | correct, regenerates byte-identically, correctly labelled a **replication** rather than a control — and that label is the right one under Appendix A's *"a proof obligation must be landed as a PROOF"* |
| §14's new status paragraph | **no** | **F1 and F2 live here** |
| the `STATE.md` row-136 rewrite | partly | **F3 lives here** |
| Appendix A tally repairs (*"seven" → "nine"*, *"the other six" → "the other eight"*) | no | **correct**: the two tallies are `8 + 1 = 9` and the 4d location count is `9`, so both stale numbers genuinely needed moving, and the second tally's *"the other eight"* is right |
| two riders on the new rule | no | sound, and the second (*"an audit's own product is not pre-audited"*) is the sharpest thing in the commit |
| the correction to the ticket (*"four, not five"*) | no | **correct**, and confirmed twice more here |

### F1 (MODERATE) — the §14 paragraph asserts its own soundness while enlarging a known-open defect

mg-d39d's finding **A5** (MODERATE, **explicitly not landed** by this commit) reads:

> §14 asserts the `STATE.md` row *"carries the same clauses"*; it carries at least five it does not.

mg-a2bd **edited that paragraph**, inserting:

> **The row below is UNCHANGED by mg-a2bd's strike of `G″`, and that is a fact rather than an
> omission** … The strike therefore touches §6 and the ledger and nothing else.

and left the following sentence — the one A5 is about — in place. Meanwhile the same commit added
~3 100 characters to `STATE.md:136` (the whole *"⚠️ SECOND-GENERATION AUDIT"* block) and nothing to
§14's copy:

```
STATE.md:136  before mg-a2bd : 13 551 chars
STATE.md:136  after  mg-a2bd : 16 692 chars
deliverable §14 row (unchanged) : 10 623 chars
mirror gap : 2 928  ->  6 069 chars   (more than doubled by this commit)
```

So a paragraph that tells the reader *"checking one row checks both"* was edited, in the direction of
reassurance, in the commit that made it twice as untrue. **The individual sentence mg-a2bd added is
true** (`G″` really never was in §14, and the row really is correctly unchanged **with respect to
`G″`**); the defect is that it was inserted **immediately above a sentence a live audit finding says
is false**, without a marker, and that the same commit widened that finding. A2–A8 being "not
landed" is correctly declared three times — but *not landing* a finding and *enlarging* it are
different acts, and only the first is disclosed.

### F2 (MINOR–MODERATE) — two site counts in one commit

- §6: *"**Three sites**, all now carrying the strike"* — §6, the ledger, and
  `…-IndependentAudit.md:413` (annotated).
- §14: *"The strike therefore touches §6 and the ledger and **nothing else**."*

Three versus two, added by the same commit, about the same object. `STATE.md`'s own Appendix A
carries the standing warning that *"the count was reported three incompatible ways in one commit,
and the repair is not to pick a bigger number — it is to stop reporting one number"*. The honest
§14 sentence is *"the strike touches this document at §6 and the ledger, and nothing in §14, §0's
summary or `STATE.md`'s row asserted `G″`"*.

### F4 (MINOR) — the rule's own evidence mis-enumerates the brief

Both `STATE.md` Appendix A and deliverable §13 state:

> mg-a806 was scoped to land **four things**: ledger row B6, the stronger replacement scope sentence,
> N1's label, and the §10 table.

mg-a806's ticket has **six** numbered items. B5 (*"THEOREM G IS CONFIRMED AND THAT SHOULD BE RECORDED
AS PROMINENTLY AS THE CORRECTIONS"*) and B6 (an Appendix A addition moved over from mg-8a12) are
omitted. **The conclusion is unharmed** — I read B1–B6 and `G″` is none of them; B5 is about
recording Theorem G's *confirmation*, not about the step-4b strengthening. But the rule being landed
is *"enumerate what the commit added beyond its brief"*, and its evidence paragraph enumerates the
brief wrongly, at two sites, one of which is `STATE.md`.

### F5 (MINOR) — *"exactly"* is not exact

> the four `n = 5` counterexamples are … all ordinal sums, i.e. **exactly the posets where the face's
> other block is not a singleton and the link is therefore a genuine join**

Not a characterisation. `A_5` at `i = 0` has the qualifying face `({0,1,2},{3,4})` whose other block
is **not** a singleton and whose link **is** a genuine join — and `A_5` is not a counterexample,
because `γ_0(A_5) = 1/2` is attained at the *other* face `({0,1,2,3},{4})`. The true condition is
*"the posets where **every** dimension-`i` face has a non-singleton other block"*, i.e. where no
one-big-block face exists at that level. `STATE.md:241` carries the same gloss. The mechanism is
right; the quantifier in the gloss is not.

---

## §9 — What could not be broken

- Every headline number: **754 / 55 / smallest `n = 5` / four ordinal sums at `γ_0 = 1/4` / 3 901 of
  7 989 / 48 846 links / 0 mismatches / 405 posets**, all reproduced from a route sharing no code.
- **Theorem J** — re-derived by hand, including the `−1/D` eigenvalue of multiplicity `r−1` and the
  role of product weights, and confirmed as a **full-spectrum** identity on the whole population by
  my own construction and my own eigensolver (worst deviation `5.3e-16`).
- **Theorem G** — the eigenfunction identity `Pf = f/2`, residual **exactly 0** in rational
  arithmetic on my own Coxeter complex, `A_3…A_9`, two `a`-vectors. The `2^{Θ(n)}` loss is a theorem.
- **`λ₂(F(A_m)) = 1/2` EXACTLY for `m = 3…8`** by rational inertia — a strengthening of the
  deliverable's own float, and the base case row `G′` rests on.
- **Row `G′`** — true as stated, correctly not narrowed, argmax exactly the one-big-block faces,
  exhaustive and exact for `n ≤ 6` and by L + J to `A_9`.
- **Row `G‴`** — the row this commit volunteered — **true**, 381/381 per level and 4 088/4 088 per
  face, with a correct proof.
- The **clean negative** on `STATE.md`, verified against the pre-strike tree rather than accepted.
- Both artifacts regenerate byte-identically; the `~21 s` figure is honest (21.1 s measured).
- **No over-correction anywhere**: `§10` byte-unchanged, `A(P)` not reopened, `M2`/`M3`/`N1`/`LG`/`S1`
  untouched, and the strike does not read as doubt about Theorem G at any of the five sites that
  mention it.
- **`A2–A8` are correctly and repeatedly declared unlanded** — three sites, as the commit says.

---

## §10 — Actions, in order

1. **F1** — mark or repair the §14 paragraph. Either land A5 (make §14 mirror `STATE.md:136`, now
   6 069 chars apart) or replace *"the corresponding `STATE.md` row carries the same clauses"* with
   *"carries the same clauses **plus** the second-generation block added by mg-a2bd; see mg-d39d A5,
   open"*. Do **not** leave a reassurance sentence sitting on top of an open finding.
2. **F2** — reconcile §14's *"§6 and the ledger and nothing else"* with §6's three-site table.
3. **F3** — put §6.1's condition into the `STATE.md` sentence: *"attained exactly at the
   one-big-block face **given the base case `λ₂(F(A_m)) ≤ 1/2`, verified `m ≤ 9`**"*.
4. **F4** — *"four things"* → *"six items, B1–B6"*, at both sites. `G″` is still none of them.
5. **F5** — *"i.e. exactly the posets where the face's other block is not a singleton"* →
   *"where **every** dimension-`i` face has a non-singleton other block"*, at both sites.
6. **F6** — either drop *"the repository was swept"* in favour of the table's own *"everything `G″`
   was **cited by**"*, or list the two refuting files so the census is a census.
7. **F7** — the commit-message-only independence phrasing needs no repair in the tree; if `J2`'s
   route is ever cited as independent evidence again, say *"independent of the audit"* and note the
   Theorem L memo.
8. **Optional, and free**: `out_verify_join.txt` `J4(a)` can be upgraded from
   `λ₂ = 0.500000000000` to `λ₂ = 1/2 exactly` for `m ≤ 8` — the inertia computation is in
   `code/hodge_leverage_audit_3c24/rebuild.py` and takes seconds.

**NOT CLAIMED.** That any of mg-d39d's A2–A8 has been re-checked here — they are out of scope and
remain open. That row `G‴` should be removed — it is true and its proof is correct; the observation
is about the shape, not the content. Anything about `A(P)`, the routing, or whether the probe should
have been run: untouched, and nothing here disturbs it.
