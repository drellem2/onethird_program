# `code/lstar_code_9d9e/` — the `L*` code, BUILT AND RUN

**`mg-9d9e`**, successor to [`mg-99f4`](../subset_consumability_99f4/), filed on its own
recommendation §4.5: *"The first move is a **run**, not a theorem: build the `L*` code and
measure its expected length against `⌈log₂ n!⌉` at `n = 6…12`."*

Deliverable: [`docs/OneThird-LStarCode-mg-9d9e.md`](../../docs/OneThird-LStarCode-mg-9d9e.md).
Predictions, pre-registered before any arm existed and never edited: [`PREDICTIONS.md`](PREDICTIONS.md).

```
sh run_all.sh        # ~20 s, exit 0 = all four arms green
```

---

## 1. What is in here

| file | what it is |
|---|---|
| `lib9d9e.py` | posets, linear extensions, `δ`, `L*`, the merge tree, **seven codes**, an exact uniform sampler |
| `s0_selftest.py` | controls — A001035 by a second algorithm, `e(P)` by three routes, the tape's bijectivity, **Kraft exactly**, **Gibbs**, five planted defects |
| `s1_run_the_test.py` | **the ticket's test, run** — 7 codes × 6 families × `n = 6…12`, plus the per-node entropies |
| `s2_where_the_test_bites.py` | the antichain theorem, the shape-A ceiling, the empty target class, one code put to Q2 |
| `s3_f24_screen.py` | the F24-multiplier branch under `mg-99f4`'s own two-question screen — **scoping, not closure** |

**It imports nothing from `code/`.** Not `lib99f4`, whose crossover table is this directory's
starting point; not `lib0fc6`, whose merge tree is the object under study; not `lib8748`, whose
F24 variance identity `s3.1` re-measures. The predecessor's reason applies one step along: a
shared enumerator would move the code reading and the poset reading together. What is shared with
the estate is OEIS A001035, the definitions, and two published numbers the arms check against.

**No clock, no `random`.** The one sampled population uses a hand-written LCG. Two consecutive
`run_all.sh` runs are byte-identical on all four transcripts.

## 2. Every code is presented in one shape, and that is what makes the numbers mean anything

A code here is a sub-probability `q` on the permutations with `Σ q ≤ 1` (Kraft). Its ideal length
is `−log₂ q`; its Shannon-integer length is `⌈−log₂ q⌉`, which is an actual prefix code. Then

> `log₂ e(P) = H(Unif(L(P))) ≤ E[len]` — **Shannon, for every code.**

so every row in every table is a valid upper bound on `log₂ e(P)`. `s0.6` checks Kraft exactly
(`Fraction`s — an equality claim cannot be checked in floats) and `s0.7` checks the inequality
itself at all 4 472 posets with `n ≤ 5`. A "code" failing either would print plausible numbers
that mean nothing.

| code | reads | what it is |
|---|---|---|
| `FREE` | nothing | index `L` into `S_n` — the thing the ticket says to beat |
| `MERGE-TAPE` | nothing | `compression2`'s tape at one bit per element per level |
| `MERGE-IDX` | nothing | `compression2`'s tape with each word indexed among `C(a+b,a)` |
| `MERGE-P` | `P`, `L*` | each word indexed among the **`P`-feasible** ones — **the `L*` code** |
| `MINIMALS` | `P` | index the next element among the current minimals — **the `L*`-free control** |
| `LEHMER-L*` | `P`, `L*` | inversion table against `L*`, Elias-gamma coded |
| `OPT` | `e(P)` | `log₂ e(P)` flat — **not consumable**, present as the floor |

## 3. The control that fired, and it fired on this directory's own construction

`s0.6`'s first draft asserted **`MERGE-P` has Kraft sum exactly 1** and it **went RED**. The claim
was wrong and the library docstring saying so has been corrected rather than the control relaxed.

Feasibility is checked **locally**, against the two sequences at a node. Two locally valid halves
need not be interleavable at all: at `P = {1<3, 2<0}` with halves `(0,1)` and `(3,2)` the union of
the two orders with `P` closes the 4-cycle `2 < 0 < 1 < 3 < 2` and there are **zero** feasible
merges. The bottom-up code can paint itself into a corner, mass leaks into dead branches, and the
Kraft sum comes out **below** 1 — `3/4` at that witness, worst `2/3` over `n ≤ 5`, first at `n = 4`
(4 of 219 posets; 96 of 4 231 at `n = 5`).

It is still a code and every bound it gives still stands — that is what `s0.6`'s `≤ 1` row and
`s0.7` are for. It is simply **not optimal**, and the tight version of it is the optimal code,
which costs the enumeration. **A remedy is an artifact of the same kind as the defect:** the
repair here would be a code, and the only repair that closes the leak is the code this whole
programme cannot afford.

## 4. Populations, and which numbers are which kind

- **Exhaustive** at `n ≤ 5` (4 231 labelled posets) for every control and every census; the
  enumerator agrees with A001035 to `n = 6` (130 023).
- **Named families** at `n = 6…12`, chosen so `e(P)` is reachable — which is not a convenience:
  the posets where `e(P)` is out of reach are exactly the posets where the free bound is already
  tight, and `s2.1` handles them by theorem instead.
- **Sampled** at one place only: the antichain at `n ≥ 9`, where every code is constant and the
  sample cannot be wrong. Which rows are sampled is **printed**, not inferred.
- ⚠️ **`n = 6…8` and `n ≤ 14` in `s2.3` are CITED** (`mg-9b6b`; the conjecture's verification),
  not re-measured here. `n ≤ 5` is this directory's own exhaustive count.

## 5. What this directory does NOT do

- **It does not settle whether a code can carry the programme.** It measures what the codes on
  record do, and states two impossibilities that no code can escape. A code with a *bound on its
  expected length provable from hypothesis (1)* is not ruled out here and is named as the open
  object in the deliverable's §6.
- **It does not close the F24-multiplier branch.** `s3` is a screen and says so in its own header
  and in `s3.4`, which lists what is not measured — starting with the third axis, which is still
  unnamed.
- **It does not touch `STATE.md`, the ratchet, `docs/FACTS.md` or `docs/CONCEPTS.md`.** Every
  measurement here is consumed by this landing and its successor, which fails the registry's
  homelessness test (`mg-3da1`'s reason).
- **It does not re-derive `mg-99f4`'s dichotomy, `mg-8b32`'s C1 or `mg-c776`'s image theorem.**
  All three are cited.
