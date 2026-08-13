# `code/marginal_factoring_8b32/` — mg-8b32's instrument for *which functions factor through the pair marginals*

Deliverable: [`docs/OneThird-PairMarginalFactoring-mg-8b32.md`](../../docs/OneThird-PairMarginalFactoring-mg-8b32.md).

Subject: Daniel's question of 2026-08-13 — *"Is there **any** function from bk graph to Z2^n which
could inject realizability?"*, corrected by him the same hour to the broader *"which data does a
construction read?"*, and then to the form the ticket carries:

> **Which functions of `P` factor through the pair marginals, and which do not?**

## 1. The answer, and why this directory is short

**Every function of `P` factors.** `P = {(x,y) : pi_xy = 1}` — the poset is *read off the marginal
vector* by looking at which entries are `1`. So there is no surplus at the poset level to find, the
enumeration Daniel proposed dies at every entry at once rather than one entry at a time, and the
premise the ticket was built on — *"the poset `P` is strictly more than its pair marginals"* — is
false. `b1` proves it and measures it exhaustively at `n <= 5`.

**The surplus is real and it is the MEASURE's**, not the poset's: `supp(mu)` and the weights are the
two things a marginal vector does not determine. `b2` tiers every candidate by which of those four
things it reads; `b3` builds the support-level witness the ticket asks for; `b4` shows why the
surviving surplus still does not buy a bound, and what the target becomes instead.

## 2. What is here

| arm | question | headline |
|---|---|---|
| `b0` | do the four objects everything rests on work? | poset counts against OEIS A001035; `L(P)` against brute force over `S_n`; the realizability oracle against brute force over **every poset**, 1002 measures |
| `b1` | does `P` factor? | **yes** — `P = {pi = 1}`, exact at all 19 / 219 / 4231 labelled posets at `n = 3,4,5`; and the map `P -> pi(Unif(L(P)))` is **injective** |
| `b2` | the tiered table | 4 tier-0 rows and 12 tier-1 rows agree (**factor**); 4 tier-2 and 3 tier-3 rows disagree (**do not factor**); 1 row **blind** |
| `b3` | the missing support-level witness | **it exists, inside hypothesis (1)** — 12 proper subsets of the `n = 6, e(P) = 9` witness's `L(P)` carry its marginals exactly, none a linear-extension set |
| `b4` | does the surplus buy a bound? | **no** — the fiber over a realizable marginal vector is already tight, so all slack in the `M_n` ceiling sits at **non-realizable marginal vectors** |

`b3.2`'s finder is itself controlled before its answer is used: the meet-in-the-middle subset search
is compared against **naive enumeration over every subset** on 207 posets at `n = 3,4` and on the
`n = 6` witness's full `2^9`. It is new code deciding this ticket's headline existence claim, and a
finder that is the only thing able to see its own findings is the defect this directory is about,
arriving inside the remedy.

Run: `sh run_all.sh` — 112 s measured on this host, all five arms green, transcripts committed.
Deterministic: re-running produces byte-identical transcripts (checked), and nothing here prints a
path, so no transcript in this directory is operator-valued (`mg-4020`'s defect, avoided by
construction rather than by luck).

## 3. Independence, which is the point of re-deriving what `lib0fc6.py` already has

Nothing here imports `code/compression2_scope_0fc6/`. That is deliberate and it is the discipline
`mg-8748`'s `c4.1` applied to `mg-0fc6`'s `a2.3`: this whole ticket turns on **two objects
agreeing**, and an instrument that agrees with itself measures nothing. So the poset enumerator, the
linear-extension enumerator, the marginal map, the realizability oracle and the majority order are
re-derived from the definitions, and each is checked in `b0` against a route that shares no code
with it.

**The witness lands in the same place by a different search.** `a2.3` found its `n = 6, e(P) = 9`
witness by looking for a *commuting square* of two disjoint adjacent swaps. `b1.3` looks for a
*non-trivial kernel of the marginal map* — the whole space of such directions rather than one
construction of one of them — and lands on the same `n`, the same `e(P)` and the same `max flip
= 1/3`. That is a third instrument on `a2.3`, after `mg-8748`'s `c4.1`.

**And the search that finds it is exhaustive, not a sample, by an exact restriction.** `L*` is always
a linear extension of `P` (if `x <_P y` then `pi_xy = 1 > 1/2`), so every poset with a coherent `L*`
is a subrelation of the total order `L*`. Relabelling `L*` to the identity, the whole `n = 6`
hypothesis population sits among the transitive subrelations of the 6-chain — `2^15` candidates
rather than `3^15` — and `b1.3` enumerates all of them. It reports that the entire `n = 6`
hypothesis population with `L* = identity` is **5 posets**.

## 4. What this directory does NOT do, and the two places it could be wrong

- **It does not re-run `a2.3` and it does not re-run the `M_n` separation sweep.** `a2.3` is cited
  as a proof (`mg-0fc6` §2, replicated by `mg-8748` `c4.1`); the sweep is `mg-0fc6`'s
  `PREDICTIONS.md` condition 2 and is not touched.
- **It does not build a compression.** The ticket says that is the successor and only if something
  survives. Something survives; the deliverable says what the successor should be.
- **`FACTORS` for tiers 0 and 1 is a proof, not a measurement — but tier ASSIGNMENT is a reading.**
  A candidate placed in tier 1 that secretly reads `supp(mu)` inherits the wrong verdict. The BK
  graph is exactly that trap and `b2.3` puts it in both tiers on purpose.
- **`BLIND` is a third verdict and is not `FACTORS`.** The ticket's own procedure says *"same value
  on both -> it factors -> dead"*, and that is too strong: agreement at one point of a fiber is one
  evaluation. What agreement does prove is that the candidate cannot separate *these* two measures,
  which is the thing the ticket cares about. `b3.4` prints the distinction rather than collapsing it.

## 5. Provenance

`p8b32`, 2026-08-13, from `mg-8b32`. Daniel's three messages that shaped it are quoted in the
ticket body and in the deliverable's §1; the correction that the question is not about the BK graph
is his, and `b2.3`'s two BK-graph rows are the answer to the original form of it.
