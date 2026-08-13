# `code/compression2_scope_0fc6/` — mg-0fc6's instrument for scoping `compression2.tex`

Deliverable: [`docs/OneThird-Compression2-Scope-mg-0fc6.md`](../../docs/OneThird-Compression2-Scope-mg-0fc6.md).
Subject: [`docs/imports/compression2.tex`](../../docs/imports/compression2.tex), Daniel's second
compression drop, imported verbatim by `mg-69f1` at 2026-08-13T00:02Z and **not read by anything
until this ticket**.

## 1. What this is for, and what it deliberately is not

`mg-69f1` imported the note and said so plainly: *"the file was not read for content and no
scoping was done."* This directory is the reading. It answers three questions and nothing else:

1. **What does the note propose?** (`a1`, `a4`)
2. **Does it inject realizability** — the target Daniel named unprompted at 00:40Z, *"compression
   as a vehicle for realizability"*? (`a2`)
3. **What is it worth, and does anything here consume it?** (`a3`, `a5`)

**It does not re-litigate `mg-8d66` or `mg-145f`.** Both are settled, both were adversarial, and
both are about a **spectral** target. The main body of `compression2` lands on `log₂ e(P)`, a
counting quantity, and those two tickets are **silent** about it. They are quoted at exactly one
place — the note's own closing paragraph, which aims back at the spectral problem by name — and
`a4.2` measures that `mg-8d66`'s ceiling does **not** apply to this construction even there.

## 2. Provenance, which is not ordinary and matters

| | |
|---|---|
| `2edf68a` | **the pre-registration**, filed before one line of `lib0fc6.py` existed, with the exposure disclosed rather than laundered |
| `91b0448` | the instruments and the `a0`/`a1`/`a2` transcripts, committed **on top of** `2edf68a` so the ordering is a fact about the DAG rather than an assertion |
| this commit | `a3` and `a4` **run** and transcripted, the new `a5`, and this README |

The ticket was worked by **two** polecats. The first (`p0fc6`) was stopped at 00:51Z for the
02:00–06:00 redeploy quiesce with `a3` and `a4` written but never run; its worktree was preserved
and its work recovered rather than re-derived. The second (`q0fc6`) ran them.

Three consequences are recorded here because they are visible in the artifacts:

- **`out_a0`, `out_a1`, `out_a2` were NOT regenerated.** They are `p0fc6`'s output, committed at
  `91b0448`, and they are the evidence as produced. A re-run in a different worktree changes the
  embedded checkout path and buys nothing (`mg-f771`).
- **`out_a3_pricing.txt` did not exist as a 0-byte file by accident, and was not committed as
  one on purpose.** `p0fc6` left an empty transcript; committing it would have asserted *"this
  arm ran and produced nothing"*, which is false. Absent was honest, empty was a false claim in a
  file that looks like evidence, and `a4` — which had no transcript at all — arrived in the same
  honest state as a result.
- **`a5` is POST-HOC.** It was written after `a0`–`a4` had run, and it is **not covered by
  `2edf68a`'s pre-registration**. Its own docstring says so. Nothing in it is scored.

## 3. Files

| file | what it does |
|---|---|
| `PREDICTIONS.md` | committed at `2edf68a`. **H1 is the disclosure that matters**: the ticket ORDERS the note read first, so `P1`–`P3` are REPORTS of a paper derivation at zero credit. The live bets are `P4`–`P11` |
| `lib0fc6.py` | posets, `L(P)`, the merge encoding and its decoder, word statistics, the note's own constants, the max-entropy solver over `M_n`, BK edges, the dyadic tree and `lca_node`. Written independently of `lib8d66.py` **on purpose** — `a4.0` then cross-checks the two, and agreement is only evidence if the code paths differ |
| `a0_selftest.py` | poset counts and `e(P)` against published values · `inv` and the prefix area by hand on `CA`/`AC`/`ACCA` · the note's own `0.9399` reproduced · **four planted worlds**, including a wrong decoder that must break the round trip and a max-entropy solver run on a problem whose answer is known |
| `a1_chain.py` | the note's chain (2)–(6) on **89,926 linear extensions**: bijectivity, the two identities, the hypothesis population, the per-node bound, the entropy lemma against the *exact* per-node entropy, and the crossover at which (6) first beats `e(P) ≤ n!` |
| `a2_realizability.py` | **the ticket's crux.** A realizability oracle, *watched discriminating* first (`a2.1`), then the note's entire chain run on a measure that is not any poset's, then two measures with **identical pair marginals**, one realizable and one not |
| `a3_pricing.py` | the sharp form `max{H(μ) : μ ∈ M_n}` solved exactly; the DIRECTION question against `STATE.md:158`'s untried slot; and `max E[inv_e]` over `M_n` re-derived by a route sharing no code with `Op-Form` Claim 6.1 |
| `a4_operators.py` | identity (8) exactly, on 197,520 BK edges; whether the scale partition is `mg-8d66`'s object (**it is not**); and Daniel's convex-combination step, answered separately for the two notes because they are two different kinds of family |
| `a5_scale_gap.py` | **post-hoc.** The note's own closing question — does the Dirichlet form decompose by scale? — answered, and **the lemma this arm was written to assert is refuted by its own run** (§a5.3) |
| `out_*.txt` | committed output of each. `a0`/`a1`/`a2` from `p0fc6`; `a3`/`a4`/`a5` from `q0fc6` |

## 4. The controls, and what each is for

- **`a2.1` — the realizability oracle is watched discriminating BEFORE it is used.** It accepts
  all **4,469** uniform linear-extension measures at `n ≤ 5` and rejects three constructed
  non-examples, including the corpus's own two-atom law. An oracle that accepts everything would
  have produced `a2`'s headline for free.
- **`a0.6` — the separation detector on a population where it SHOULD fire.** `a2`'s finding is
  that a statistic does *not* separate; a detector that cannot detect separation would produce
  that finding on any input.
- **`a0.7` — a wrong-direction world for the entropy lemma.** The unconstrained word must
  *exceed* the note's bound, or the bound has no content. It does, at `m = 32, 64, 128` — and
  the same arm measures that below `m = 27` the bound is **weaker than `log₂ C(2m,m)`**, i.e.
  says less than *"the word is a word"*.
- **`a4.0` — `L(P)` cross-checked against `lib8d66` at every labelled poset `n ≤ 5`**, 4,469
  posets, 0 disagreements, through a deliberate representation change (matrix vs. pair set).
- **`a5.2c` — the planted world for `a5.2`.** The same statement with the level read off the word
  *position* instead of the LCA must fail, and does. Without it `a5.2` could be a property of
  gradings in general rather than of this one.

## 5. What the arms found

**`a1` — the construction, and `P8`.** The encoding `L ↔ (W_B)` is a **bijection**: it forgets
nothing. `compression2`'s "compression" is a **re-coordinatisation** (merge sort's recording
tape) plus an entropy estimate — a different *kind* of object from `compression.tex`'s `C_o`,
which is a genuine quotient. Identities (2)–(5) hold as written. Headline (6) also holds, and is
**numerically vacuous below a measured crossover of `n = 16,777,063`**: below it, `0.9399·n log₂ n`
is *weaker than the free bound* `e(P) ≤ n!`. `P8` predicted the crossover in `[10⁶, 10⁸]`.

**`a2` — realizability, and `P5`. This is the answer to Daniel's question.** The note is
**realizability-blind**, and the wash-out has a named site rather than a hand-wave:

    mu1 and mu2 have IDENTICAL pair marginals
    mu1 IS a linear-extension measure · mu2 is NOT (not uniform on its support)
    BOTH sit inside hypothesis (1), same value, max flip = 1/3
    every step of the note returns the SAME verdict on both

> *"The poset-dependence washes out at exactly one place: `L*` and (1) are both functions of the
> PAIR MARGINALS, and the dyadic tree is a function of `L*`. Nothing downstream reads `P` again."*

**`a3` — pricing.** `max{H(μ) : μ ∈ M_n}` is `0.907, 0.900, 0.893, 0.887, 0.883` of `log₂ n!` at
`n = 3…7` — so the note's ceiling is used to **52–59%** and the bound is true but far from sharp
(`P7`). The DIRECTION is the decisive half: the two-atom law has `H = 0.9183` bits **at every
`n`** and simultaneously the **largest** `E[inv_e]` anything in `M_n` can have, so an entropy
bound cannot deliver an inversion bound and `STATE.md:158`'s untried slot does not follow from a
bound of this shape. `a3.3` then reproduces `Op-Form` Claim 6.1 / `mg-6bc2` Claim 3.1 by a route
sharing no code with them: the note's hypothesis **is** that information set, and the wall's
currency on it is already at **equality**.

**`a4` — the operator side, and Daniel's convex combination.** Identity (8) is **exact** (`P4`),
on 197,520 BK edges. The scale partition is **not** an admissible `k`-foliation (`P9`) — its
fibers have non-power-of-2 sizes, so `mg-8d66` does not reach it and must not be quoted at it.
And the convex-combination step has **two different answers** because there are two families:
transverse on `compression.tex` (a convex combination is **not** a projection — and the programme
already uses that object, `mg-8d66`'s `kI − Σ Π_i`), **nested** on `compression2`, where the
increments are mutually orthogonal and a weighted combination is a genuine Littlewood–Paley
multiplier. *That is the one place Daniel's stated design is better than the closed arc's objects.*

**`a5` — the note's own last question, and a refutation of this arm's own lemma.** The Dirichlet
form **is** graded by scale (`E = Σ_l E_l`, exact) and the grading **annihilates the coarse
filtration** (`E_l(Π_l f) = 0`, exact — identity (8) restated as a statement about forms). The
step the note needs is the stronger `E_l(f) = E_l(D_l f)`, which would make the Rayleigh quotient
a ratio of two sums over the same index. **It is false**, at 3 of 5 posets measured: `E_l`
annihilates everything coarser than `l` but *reads everything finer*. The form is graded, the
norm is graded, and **the two gradings do not match** — the structure is triangular, not diagonal.
Written down anyway, `gap_BK ≥ min_l μ_l` is not lossy but **empty**: `μ = 0` at the finest scale
at every poset measured, for a reason visible at `n = 4`.

**That refutation was this arm's own assertion, and it is kept rather than quietly rewritten**,
because it is the note's risk too: grading a form is not decoupling it, and the step from (8) to
*"a multiscale family of median-graph problems"* is exactly that step.

## 6. Score of `2edf68a`'s live bets

`P1`–`P3` were filed as **REPORTS at zero credit** and are not scored. `a5` is post-hoc and
scores nothing.

| bet | p | outcome | where |
|---|---|---|---|
| `P4` (8) is exact | 0.90 | **CONFIRMED** | `a4.1`, 197,520 edges |
| `P5` realizability-blind | 0.90 | **CONFIRMED**, constructively | `a2.3` |
| `P6` the closure that bites is the pair-bias one | 0.85 | **CONFIRMED** | `a3.3` |
| `P7` bound true but not sharp on `M_n` | 0.65 | **CONFIRMED**, both clauses | `a3.1`, `a3.1b` |
| `P8` (6) numerically vacuous below `~10⁷` | 0.80 | **CONFIRMED**, crossover 16,777,063 | `a1.6` |
| `P9` not an `mg-8d66` foliation | 0.85 | **CONFIRMED** | `a4.2` |
| `P10` `compression2`'s family is nested | 0.75 | **CONFIRMED** | `a4.3b` |
| `P11` the two notes are two families | 0.70 | **CONFIRMED** | `a1.1` vs `a4.3a` |

**`P5` is the one worth the pre-registration.** It is a *negative* answer to the thing the
ticket's addendum was most hopeful about, filed at 0.90 before any instrument existed, by a route
(`STATE.md:21`) that is neither of the two tickets the ticket forbade quoting. None of the four
named conditions under which `P5` would have lost fired.

## 7. What this instrument deliberately does NOT do

1. **It does not decide anything.** The ticket asks for a scope *recommendation* to
   `pm-onethird`, and the deliverable is written as one.
2. **It touches no canonical file.** `STATE.md`, `docs/FACTS.md` and `docs/CONCEPTS.md` are
   `pm-onethird`'s. In particular `CONCEPTS.md` §5 (*"Intuitions that have been killed"*) is
   where `a2`'s finding would go if the recommendation is accepted, and this ticket does not put
   it there.
3. **It is not a gate.** It is not in `build.sh`, it guards no invariant, and it prices a drop.
4. **It does not attempt the note's remaining open direction.** `a5.3` names what would have to
   be true for the multiscale route to work and measures that it is not; proving or refuting the
   general statement is not this ticket.

## 8. Runtime

`a3` 5.7 s · `a4` 6.6 s · `a5` 0.2 s, measured by `time` on this host. `a0`/`a1`/`a2` were
measured in `p0fc6`'s worktree; `run_all.sh` reports ~35 s for the whole suite. **Re-running
`run_all.sh` regenerates `out_a0`/`out_a1`/`out_a2`,** which this ticket was instructed not to do
and did not; the warning is in the script.
