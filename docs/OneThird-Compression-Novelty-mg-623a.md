# Is the checkerboard compression new? — `docs/imports/compression.tex` against the corpus and the literature

*Work item `mg-623a`, scoped by pm-onethird off Daniel drop `mg-2ffd`. Subject:
`docs/imports/compression.tex` at `44d08ea`. Instrument: `code/compression_novelty_623a/`,
`run_all.sh`, 32.8 s measured.*

---

## VERDICT: **duplicates-literature**

**The compression is David Bruce Wilson's *even and odd sweeps*, stated for linear
extensions by name**, in *Mixing times of lozenge tiling and card shuffling Markov
chains*, [arXiv:math/0102193v2](https://arxiv.org/abs/math/0102193) §7 ("Sweeps versus
independent updates"), pp. 18–19; published as *Ann. Appl. Probab.* **14** (2004)
274–325. Verbatim from that section:

> "So far we have focused on updates where a random site is selected, and then a local
> randomizing operation is performed at that site. Often in practice the various sites
> are updated in systematic "sweeps" rather than at random. **For instance, for
> permutations or linear extensions, rather than randomize a random adjacent pair of
> items, one may instead randomize the items in positions (1, 2) (3, 4) (5, 6) …, and
> then do positions (2, 3) (4, 5) (6, 7) …** … **Call the first set of updates an even
> sweep, and the second set an odd sweep.**"

That is §1 of the note. `C_o` — "remember the unordered blocks `B_j = {x_{2j-1},
x_{2j}}` but forget their internal order" — *is* the state left invariant by Wilson's
even sweep, and `Π_o = E[· | C_o]` *is* Wilson's even-sweep operator: "randomize the
items in positions (1,2) (3,4) …" is uniform resampling inside the `C_o`-fiber.
`C_e`/`Π_e` are the odd sweep. **The naming is flipped** — Wilson's *even* sweep is the
note's *odd* compression — which is a labelling difference and not a mathematical one,
and is recorded here so that nobody reads the two as distinct objects.

**§4's operator formulation is also off-the-shelf, for exactly this operator.** Once
`Π_o` and `Π_e` are the two sweep operators, `(Π_o + Π_e)/2` is a two-component
(two-block) Gibbs sampler, and analysing its gap by alternating projections and
principal angles between `Ran Π_o` and `Ran Π_e` is the standard treatment:
[arXiv:2201.12500](https://arxiv.org/abs/2201.12500) (Qian, *Analysis of two-component
Gibbs samplers using the theory of two projections*) applies Halmos's 1969 two-projection
theory to precisely this object, and [arXiv:2304.02109](https://arxiv.org/abs/2304.02109)
(*Solidarity of Gibbs samplers: the spectral gap*, AAP 2025) rests on "the geometric
interpretation of the Gibbs samplers as alternating projection algorithms" and the
von Neumann–Halperin cyclic alternating-projection rate, noting that in the
two-coordinate case the spectral gap is computable through two-projection theory.

**Wilson also already priced it.** §7 of the same paper says the sweep chain buys a
factor of about two over independent updates and no more — *"The mixing time bounds are
then roughly the same though slightly better … Note that we have not proved that the
mixing time is actually twice as fast, merely that our upper bound on it is half as
large."* The literature therefore knows both the decomposition and that it does not
change the order of the answer for the mixing question.

### The one thing I did not find stated, and what it is worth

The **exact energy identity** — the note's `(*)`/`(**)`/`(***)`, restricted to
pair-orientation linear statistics — I did not find written down. **That is an absence,
and absences are weak**; see §5 for what my search does and does not cover. It is in any
case a two-line consequence of two standard facts: Wilson's sweep decomposition, and the
observation that a pair-orientation statistic is degree ≤ 1 on each sweep fiber. It is
**true** — re-derived exactly below, 0 failures at every labelled poset with `n ≤ 5` —
and it is **an upper bound on the BK gap and not a lower one**, which is measured in §3
and is the reason it does not deliver what §5 wants.

### Not `duplicates-existing-tree-work`, and the three named sites are not counterexamples

**Novel to this tree: yes, all of it.** The term census (§4) returns **0** for *principal
angle*, *canonical correlation*, *maximal correlation*, *two projections*, *checkerboard*,
*foliation*, *partial cube*, *even sweep*, *odd sweep*, *conditional variance*,
*conditional expectation*, *block dynamics* and *Efron* across **all three**
repositories — `onethird_program`, `one_third`, `one_third_width_three` — with five
positive controls nonzero in all three, so the zeros are a property of the corpus and
not of the search.

---

## 1. The three named sites use the same phrase for a different object

The ticket's lead is correct that "alternating projection" is already in the corpus, at
exactly three places, and correct to insist the comparison be drawn against the *claim*.
Drawn there, it is not the same claim.

| | `compression.tex` §4 | the three named sites |
|---|---|---|
| what is projected onto | **two subspaces**: `Ran Π_o`, `Ran Π_e` | **one subspace and a cone**: the bottom eigenspace of the pencil, and the nonnegative orthant |
| what the projections are | **conditional expectations** `E[·\|C_o]`, `E[·\|C_e]` | an eigenspace projector and a coordinate clamp |
| what is being decided | the **spectrum** of `2I − Π_o − Π_e`, i.e. principal angles | **feasibility**: does the top standard eigenspace *meet* the monotone cone, yes/no |
| what it is | a proposed reformulation of the BK gap | a numerical device (POCS) inside one audit instrument |
| where | — | `code/l2_underclaim_audit_3bb9/lib3bb9.py:230` |

All three sites route to the same implementation, whose own comment reads: *"is there a
nonzero `v` in `span(basis)` with `v ≥ 0`? Decided by alternating projection between the
subspace and the **nonnegative orthant** (POCS), from several starts … A "yes" is
CONSTRUCTIVE (a witness is exhibited and checked); only a "no" rests on the search."*
Arm **C1c** reads that source mechanically rather than leaving it to my summary: it
mentions a cone/orthant **YES**, two subspaces **no**, conditional expectation **no**,
principal angles **no**, and projects onto a single span.

What those three sites *establish* is a census: an L2 first-disjunct count of
`0/0/10/166/3164 = 3340` at `n = 2..6` obtained by a route that never mentions `μ_pref`,
agreeing with the `V00` column at all 4377 posets — `mg-3bb9`'s third instrument,
introduced precisely because `mg-29fe`'s agreement was a tautology. That is an
independence check on a published number. It has no bearing, in either direction, on
whether the odd and even prefix compressions are close.

**So: the framing is not new to this tree in the sense the ticket suspected, and the
phrase overlap is a coincidence of vocabulary.** The compression is new to this tree.
It is not new to the literature.

---

## 2. The note's four structural claims are true — re-derived exactly

`a1_identities.py`, exact `Fraction` arithmetic, **no float on any verdict path**,
**all labelled posets** `n = 2..5` (3 + 19 + 219 + 4231 = 4472), three distinct
coefficient vectors each.

| arm | claim | checked | failed |
|---|---|---|---|
| **A1** | §1: `C_o^{-1}(F)` is exactly `Q^{d(F)}`, and the edges inside it are exactly `τ_1, τ_3, …` (and `C_e` with `τ_2, τ_4, …`) | 39 403 fibers | **0** |
| **A2** | §2: `Var(f\|C_o) = ¼ Σ_{j∈D} c_{B_j}²` — no covariance terms | 118 209 fibers | **0** |
| **A3** | §3 `(*)`: `E_BK(f) = (2/(n−1))(E Var(f\|C_o) + E Var(f\|C_e))` | 13 416 | **0** |
| **A4** | §4 `(***)`: `(I − P_BK)f = (2/(n−1))(2I − Π_o − Π_e)f`, pointwise | 13 416 | **0** |

A1 does not merely count `|fiber| = 2^d`: it checks that every member of a fiber has the
*same* block set (so "each `B_j` is fixed" is verified rather than inferred from a
count), and that a BK edge stays inside the fiber **iff** its index has the right parity.

**Three controls, and all three fire.** They are scored inverted — a failure is the pass —
because an identity that also held off its hypothesis would be a fact about the chain
rather than about linear statistics:

| arm | control | fires |
|---|---|---|
| **A5a** | `(*)` on a function that is *not* a pair-orientation statistic | 9 420 / 13 416 |
| **A5b** | `(***)` on the same | 9 420 / 13 416 |
| **A6** | is `P_BK f` again a pair-orientation statistic? | fails at 8 796 / 13 416 |

A5 and A6 are silent at `n ≤ 3` and on the many small posets where `|L(P)|` is too small
for any function to fall outside the span — 3 996 of the 13 416 for A5. That is a
property of the population, stated rather than averaged away.

**A7, a named control against this tree's own hypercube family.**
`docs/OneThird-Hodge-Side-Leverage.md:132,851` records that on `V_k` — the ordinal sum of
`k` two-element antichains — the AT graph **is** the hypercube `Q_k` and `Δ_AT` is
therefore "already diagonal by inspection". The note's compression must degenerate there,
and it does: at `k = 1,2,3,4` the odd compression has **exactly one fiber**, of size
`2^k` = all of `L(P)`, and the even compression has `2^k` **singleton** fibers. So the
family where this tree already knew the answer is exactly the family where the foliation
is trivial and the note adds nothing.

---

## 3. What `(**)` buys without §5's assumption: an upper bound, and it does not reach the gap

The note is explicit that its payoff is conditional — *"assuming your agents' claim that
the relevant standard eigenfunction is linear is correct"*. Arm **A6** already shows why
that hedge cannot be dropped: **the space of pair-orientation statistics is not
`P_BK`-invariant**, so `(***)` is a pointwise identity on that space and not a
restriction of the operator to it. By the variational principle `(**)` is therefore
unconditionally an **upper** bound on the BK spectral gap, and a lower bound only where
the bottom eigenfunction happens to be a pair-orientation statistic.

`a2_tightness.py` measures how often that happens. `gap_lin` is the minimum of
`E_BK(f)/Var(f)` over centered pair-orientation statistics; `gap_BK` is the smallest
nonzero eigenvalue of `I − P_BK`. **[FLOAT]** — both are eigenvalues, by cyclic Jacobi;
worst off-diagonal residual over the whole run `9.8e-13`.

| `n` | posets | in population | skipped (`\|L(P)\| > 24`) | `gap_lin > gap_BK` | `gap_lin < gap_BK` | worst ratio |
|---|---|---|---|---|---|---|
| 3 | 19 | 13 | 0 | **0 of 13** | 0 | 1.000000 |
| 4 | 219 | 195 | 0 | **61 of 195** | 0 | 1.044950 |
| 5 | 4231 | 3810 | 301 | **2260 of 3810** | 0 | 1.063001 |

**By `n = 5` the BK bottom eigenfunction is not a pair-orientation statistic at 59 % of
posets, and the fraction is rising** (0 %, 31 %, 59 %). The `n = 5` argmax is
`[(1,2),(1,4),(3,0),(3,4)]`. `gap_lin < gap_BK` never occurs, as it must not.

**Self-check (B3).** The energy matrix built from the chain and the energy matrix built
from the note's conditional variances agree to `7.8e-16` over every poset and every basis
pair — `A3` again, on a second instrument and in float. Had they disagreed, `a2` would
have been measuring something other than the note.

**Population caps, stated rather than implied.** `a2` skips posets with `|L(P)| > 24`
(301 of 4231 at `n = 5`, including every large antichain) because the Jacobi cost is
cubic; the skipped count is printed in the table. Both `a1` and `a2` stop at `n = 5`.

---

## 4. Term census — how "novel to this tree" was decided

`a3_sites.py`, over `onethird_program` (`docs/`, `code/`, `STATE.md`), `one_third`, and
`one_third_width_three`. Extensions searched: `.tex .md .py .txt .json .lean .html .sh`;
`.git`, `.lake`, `node_modules`, `__pycache__` skipped. `compression.tex` itself and this
instrument are excluded from every count.

| term | `onethird_program` | `one_third` | `one_third_width_three` |
|---|---|---|---|
| alternating projection | 3 / 3 files | 0 | 0 |
| principal angle | 0 | 0 | 0 |
| canonical correlation | 0 | 0 | 0 |
| maximal correlation | 0 | 0 | 0 |
| two projections | 0 | 0 | 0 |
| checkerboard | 0 | 0 | 0 |
| foliation | 0 | 0 | 0 |
| partial cube | 0 | 0 | 0 |
| even sweep / odd sweep | 0 | 0 | 0 |
| conditional variance | 0 | 0 | 0 |
| conditional expectation | 0 | 0 | 0 |
| block dynamics | 0 | 0 | 0 |
| Efron | 0 | 0 | 0 |
| pair-orientation | 0 | 0 | **14 / 6 files** |
| *linear extension* (control) | 610 | 126 | 611 |
| *adjacent transposition* (control) | 35 | 16 | 39 |
| *hypercube* (control) | 27 | 1 | 1 |
| *spectral gap* (control) | 17 | 6 | 75 |
| *Dirichlet* (control) | 5 | 96 | 134 |

**The five control rows are what make the zeros mean anything.** A census that returned 0
everywhere would be searching the wrong files; these do not.

**The one live hit, chased.** `pair-orientation` at 14 hits in `one_third_width_three` is
the *marginal counts* `|L_{x<y}(P)|` — the `Pr[x < y]` of the conjecture itself
(`docs/compatibility-geometry-*`, `docs/state-F32.md:39`) — and not the note's function
space `f(L) = a + Σ c_{xy} 1{x <_L y}` on `L(P)`. Shared substrate, different object.
No variance, no Dirichlet form, no compression.

---

## 5. What this document does not establish

- **The literature verdict rests on one positive hit and several absences.** Wilson §7 is
  a positive identification, quoted verbatim from the paper's own text, and it carries
  the verdict. The claim that the *exact identity* `(*)` is not stated anywhere is an
  **absence** produced by keyword search over web results — it is not a survey, and a
  reader should treat it as "not found" and not as "not there".
- **The corpus verdict is also an absence**, mitigated by positive controls but still a
  census over *terms*. A claim stated in this tree in other words would be missed. I read
  the three named sites in full and the `V_k` material in `OneThird-Hodge-Side-Leverage.md`;
  I did not read all 247 files the control row touches.
- **`a2`'s reading of §5's assumption is operational, not exegetical.** I measure "is the
  BK spectral gap attained on pair-orientation linear statistics". The note's phrase is
  "the relevant standard eigenfunction is linear". These are adjacent, not identical, and
  I do not claim to have measured the note's sentence.
- **No claim is made about `STATE.md` row 3b.** The note's §5 conditional is of the same
  family as this tree's *standard dominance* (`STATE.md:112`), whose unconditional form is
  **REFUTED** (166 refuters at moderate-`λ`, `n = 7`) and whose open form *is* L1b, the
  wall. Whether the note's conditional is that conditional is **not decided here** and is
  flagged for pm-onethird, not answered.
- **Nothing outside `docs/OneThird-Compression-Novelty-mg-623a.md` and
  `code/compression_novelty_623a/` is edited.** `STATE.md` is untouched,
  `docs/imports/compression.tex` is untouched, no ledger row moves, and no existing
  document is corrected.
- **`n ≥ 6` is not enumerated** by either exact arm, and `a2` additionally caps at
  `|L(P)| ≤ 24`.

## 6. Defects of my own, kept

- **D1 — my first `a3` run hung and I nearly reported a timeout as a result.** The term
  census grepped `one_third_width_three` unfiltered; that tree is **8.1 GB**, almost all
  of it a Lean build under `lean/.lake`. Killed at 120 s with zero output. The fix is the
  extension allowlist above, and the blind spot it creates — a term living only inside a
  compiled artifact — is now printed by the instrument rather than left in my head.
- **D2 — `a3` gave a different answer depending on the caller's directory.** It resolved
  the three site paths against `cwd`, so it worked from the repo root and raised
  `FileNotFoundError` from inside its own directory, which is how `run_all.sh` found it.
  It now resolves against the repository root computed from `__file__`. An instrument
  whose answer depends on where you stand is the same defect class as the census whose
  zeros depend on which files it reached.
- **D3 — the runtime in `run_all.sh` is measured on the invocation that wrote these
  transcripts**, 32.8 s, and on one host only. It is not a claim about any other machine.
