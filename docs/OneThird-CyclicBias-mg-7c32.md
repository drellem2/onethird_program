# Is the pair bias's coboundary a route to the conjecture? — **STEP 1 IS A REAL DICTIONARY ENTRY, STEPS 2–3 LANDED IN THIS REPOSITORY HOURS EARLIER UNDER OTHER NAMES, AND STEP 4 IS THE CONJECTURE RESTATED RATHER THAN A REDUCTION OF IT**

`mg-7c32`, 2026-08-14, filed on Daniel's instruction (*"file this approach"*) out of a live
exchange with `pm-onethird`. Instrument:
[`code/cyclic_bias_7c32/`](../code/cyclic_bias_7c32/) — four arms, standard library only, exact
rationals on every verdict path, ~75 s, two consecutive runs byte-identical. Ten predictions with
four refuted, two of them this directory's own:
[`code/cyclic_bias_7c32/PREDICTIONS.md`](../code/cyclic_bias_7c32/PREDICTIONS.md).

---

> ## THE VERDICT
>
> **Every step of the filed line is CORRECT. Nothing here breaks it. What the checks return is a
> map of where its content actually is, and it is not where the ticket puts it.**
>
> **STEP 1 IS THE NEW THING AND IT SURVIVES EXHAUSTIVELY.** The coboundary of the pair bias is
> the **cyclic-orientation bias**:
> `(db)(x,y,z) = b(x,y)+b(y,z)+b(z,x) = Pr[the induced order rotates (x,y,z)] − 1/2`.
> Confirmed at **471 804 ordered triples** over every poset `n ≤ 7`, by two routes sharing no line
> of code — one from the pair marginals alone, one by enumerating `L(P)` and reading each word.
> Zero disagreements, zero `|db| > 1/2`. This is a genuine dictionary entry the corpus did not
> have, and it is what makes a *per-triple* question well posed.
>
> **STEPS 2 AND 3 ARE ALREADY IN THIS REPOSITORY, LANDED THE SAME NIGHT.**
> `docs/BASIC-FACTS.md` at `73af2f3` carries step 1's `1 ≤ Σp ≤ 2` half as **fact 1**, step 2
> verbatim as **fact 2**, and step 3 with `D = 0` as **fact 3**. The ticket's standing assumption
> that a dedup search *"returned nothing here"* is therefore **refuted** — the grep missed it
> because that file says *coboundary* once and *cyclic* never (P8).
>
> **STEP 4 IS NOT A REDUCTION, AND THE MECHANISM IS ONE LINE OF ARITHMETIC.** With `A` the mean
> bias over the `n − 1` consecutive pairs of `L*`, exactly and unconditionally:
>
>     avg db  =  ( (n−1)·A − b(x_1, x_n) ) / (n−2)          hence   |avg db − A| ≤ 1/(n−2)
>
> measured over **19 441 posets, 0 violations**. The average cyclic bias **is** the average pair
> bias plus `O(1/n)`. Dividing `D` by `n − 2` does not create a new object: **no step of the
> argument ever bounds an individual `db`**, and steps 3 and 4 are a lower and an upper bound on
> the same scalar `D`, computed from the same two inputs.
>
> **SO THE TARGET HAS EXACTLY TWO READINGS AND BOTH CLOSE.** *Without* the counterexample
> hypothesis it is **false**: a chain has `avg db = 1/2`, and on this population `db = 1/2` holds
> at the chain triples and **nowhere else** (43 644 ordered triples = 3 × 14 548 chains). *With*
> the hypothesis it is **the conjecture**: the hypothesis gives `A > 1/6`, hence
> `avg db > 1/6 − 1/(3(n−2))`, which is step 3 divided by `n − 2` — so proving `avg db < 1/6 − ε`
> under the hypothesis is proving the hypothesis inconsistent.
>
> **ONE OF THE TWO FREE RESOURCES IS EMPTY AND THE OTHER WAS ALREADY SPENT WELL.** `D` is
> **bracketing-invariant** — 19 441 of 19 441 posets reach the same `D` under the star and under
> the balanced binary tree, while 19 392 of them visit a *different* multiset of `db` values
> (P5, refuted). Every bracketing spends exactly `n − 2` triples, a binary tree with `n − 1`
> leaves having `n − 2` internal nodes. The base point *does* move `D`, and an **end point is
> optimal**: the general identity is `D = Σ consec − b(base, x_n) + b(base, x_1)`, so an end point
> spends one bias and an interior point spends two over one fewer term. The ticket's "lazy"
> bracketing was the right choice already.
>
> **WHAT SURVIVES.** A **per-triple** bound is strictly stronger than a bound on the average and
> is untouched by any of the above: *does the hypothesis force `db(x_1, x_{k−1}, x_k) ≤ 1/6 − ε`
> for every `k`, or is only the aggregate controlled?* The aggregate is `D` and `D` is step 3. An
> individual `db` is not — and by step 1 it is the cyclic-orientation bias, an object correlation
> machinery can be pointed at.

---

## 1. Setup, and the one convention

`P` a finite poset on `n` elements, `L(P)` its linear extensions under the uniform measure,
`p(x,y) = Pr[x <_L y]`, and the bias `b(x,y) = p(x,y) − 1/2`. `b` is antisymmetric,
`x <_P y ⟹ b = 1/2`, and `x ∥ y ⟹ |b| < 1/2`. The **counterexample hypothesis (CE)** is that
every incomparable pair has `|b| > 1/6`, equivalently `δ(P) < 1/3` in this corpus's notation.

`b` is a 1-cochain and `(db)(x,y,z) = b(x,y) + b(y,z) + b(z,x)` is its coboundary. **That word
carries no programme here.** There is no complex, no `H^1`, and no claim about either; the ticket
forbids opening a cohomology arc and this document does not, on the ticket's own grounds —
`mg-01ce` (F31, RED) and `mg-d0fa` (F28, AMBER) are what that costs, and F31 §6.5's list of what
its RED does *not* retract is where the live half of that arc is indexed (`mg-ea7f`).

## 2. Step 1 — the coboundary is the cyclic-orientation bias

Let `N` count how many of `x<y`, `y<z`, `z<x` hold in a random `L`. A linear order admits neither
a 3-cycle (`N = 3`) nor its reverse (`N = 0`), so `N ∈ {1,2}` always, with `N = 2` exactly on the
three rotations of `x<y<z`. Hence `E[N] = 1 + Pr[cyclic class is (x,y,z)]` and

```
(db)(x,y,z)  =  E[N] − 3/2  =  Pr[ the induced order rotates (x,y,z) ] − 1/2
```

**Checked, not asserted.** `c1 §1` observes `N ∈ {1,2}` and nothing else over every word of every
`L(P)` at `n = 3..7`. `c1 §2` computes `db` twice — once from the three pair marginals with no
linear extension built, once by enumerating `L(P)` and classifying each word — and the two agree
at all **471 804** ordered triples, with `|db| ≤ 1/2` everywhere. The `1 ≤ Σp ≤ 2` inequalities of
the linear ordering polytope are `N ∈ {1,2}` restated and are already `BASIC-FACTS` **fact 1**;
the reading of `db` as a *cyclic-orientation probability* is the part that is new.

**Where the ceiling sits, and it is the whole of §5's argument in one line.** `db = 1/2` requires
`Pr[cyclic] = 1`. On every poset `n ≤ 7` that happens at **exactly the chain triples**
`x <_P y <_P z` — 43 644 ordered instances, which is `3 × 14 548` because each cyclic class is
counted once per rotation. Symmetrically for `db = −1/2`. So the ceiling is not an exotic
configuration: it is what a comparability looks like.

## 3. Step 2 — checked as far as it can be, and the half that cannot

Orienting `x → y` iff `p(x,y) > 2/3` gives a relation that is **acyclic** (a 3-cycle would need
`Σp > 2`, against fact 1) and **consistent with `P`**. Both verified exhaustively over **19 446**
posets at `n = 3..8`: 0 cyclic, 0 inconsistent.

**Those zeros are not evidence for step 2 and must not be quoted as if they were.** Step 2's
conclusion is that the relation is *total*, hence a linear extension `L*`, and totality is
supplied by CE — which no reachable poset satisfies. The relation is total on **6 of 19 446**
posets here, the six chains. `c0`'s D6 makes the same point from the plant side and is the
required-**inert** plant: relaxing the threshold from `2/3` to `1/2` changes nothing anywhere on
this population, so `0 cyclic` at `2/3` is not a test of the band. The instance the population
cannot supply is `mg-24a3`'s majority cycle at `n = 11` with margins ≈ `0.50014`, and
`BASIC-FACTS` fact 2 already carries that *Not*.

## 4. Step 3 — the telescope, and the two resources

From `b(x,z) = b(x,y) + b(y,z) − (db)(x,y,z)`, walking `L*` gives the ticket's

```
b(x_1, x_n)  =  Σ_{i=1}^{n−1} b(x_i, x_{i+1})  −  D,        D = Σ_{k=3}^{n} (db)(x_1, x_{k−1}, x_k)
```

and under CE, `Σ consec > (n−1)/6` with `b(x_1,x_n) ≤ 1/2` gives `D > (n−4)/6`. All correct.

**The general form is what prices the base point.** Supplying the diagonal `b(x,x) = 0`, the star
based at any element obeys

```
D_base  =  Σ consec  −  b(base, x_n)  +  b(base, x_1)
```

exactly — **152 609** telescopes over every poset `n ≤ 8` and every base point, 0 disagreements;
and **39 426** over every *chain*, not only the majority one, at `n ≤ 5`, since the identity is
algebra in `b` and does not use that the chain is a linear extension. At an end point the second
correction vanishes and one bias is spent, giving `(n−4)/6` over `n − 2` live terms; at an
interior point two are spent, giving `(n−7)/6` over `n − 3`. **The base point is free but not free
in this direction**, and the ticket's lazy choice is the optimal one.

**The bracketing resource is empty.** `D` is `b(x_1,x_n)` subtracted from a sum that never
mentions the bracketing, so rebracketing can only redistribute the defect. Measured: the star and
the balanced binary tree reach the **same** `D` on 19 441 of 19 441 posets while visiting a
different multiset of `db` values on 19 392 of them, and both spend exactly `n − 2` triples. This
refuted P5. The freedom is real for choosing *which* triples an argument must bound — and worth
nothing against the aggregate.

**The degenerate cases the ticket flags, run rather than reasoned** (`c2 §3`). `n < 4` makes the
bound non-positive. The **chain** has no incomparable pair, so CE is vacuously true of it and
step 3's conclusion is correct for it (`D = 3/2 > 1/6` at `n = 5`) with `avg db = 1/2`; it is
excluded as a counterexample by the conjecture's own statement, not by anything in step 3. The
**antichain** has `b ≡ 0`, fails CE at every pair, and gives `D = 0` — the exact case, which
`BASIC-FACTS` fact 3 says forces the conjecture, and it does.

## 5. Step 4 — priced, and the price is the whole conjecture

Write `A = (Σ consec)/(n−1)`. Then at an end base point, exactly:

```
avg db  =  D/(n−2)  =  ( (n−1)·A  −  b(x_1, x_n) ) / (n−2)          ⟹   |avg db − A| ≤ 1/(n−2)
```

Verified over **19 441** posets, 0 violations, largest observed gap `7/36` at `n = 4` against a
ceiling of `1/2` there. So:

* **Unconditionally the target is false.** `A` reaches `1/2` on comparability-rich chains, so no
  theorem bounds `avg db` below `1/6` over an arbitrary star. §2's ceiling result says the same
  thing locally: `db = 1/2` at every chain triple.
* **Under CE the target is the conjecture.** `A > 1/6` gives `avg db > 1/6 − 1/(3(n−2))`, which is
  step 3 divided by `n − 2`. Establishing `avg db < 1/6 − ε` under CE for large `n` *is* deriving
  the contradiction, not preparing for it.

The intended contradiction is **sound as a strategy** — that is worth saying plainly, because the
line is not wrong, it is circular. What it lacks is any handle that step 3 did not already have.

**And the population agrees, in the direction that hurts.** On the extremal class `δ(P) = 1/3` at
`n = 8` — 12 posets, the closest thing to CE that exists at any reachable `n` — the average `db`
is `5/18 ≈ 0.278` (`7/30 ≈ 0.233` with the base point spent well) against step 3's floor of
`1/9 ≈ 0.111`, and **0 of 12** reach `< 1/6` at any base point. This refuted P6, which had
predicted a slack of order `1/(n−2)`.

⚠️ **Neither that result nor its mirror is evidence about the counterexample class, which is
empty.** `min δ(P) = 1/3` at every `n = 3..8` and the conjecture is verified to `n = 14`
(`mg-33f5`). `c3 §3` warns against reading the 95.4% of posets whose best-base average falls below
`1/6` as *support* for step 4; `c3 §4` warns against reading its own contrary figure as
*refutation*. The population supports a wrong reading in both directions and both warnings ship.

## 6. What is left, and where a successor should start

The one object step 1 hands over that step 3 does not already own is an **individual** `db`. So:

> **Open.** Does CE force `db(x_1, x_{k−1}, x_k) ≤ 1/6 − ε` for **every** `k` along `L*`, or is
> only the aggregate `D` controlled?

This is strictly stronger than the average statement and is not circular in the way §5 is: it is
not a restatement of `Σ consec`, and by step 1 it is a statement about
`Pr[the triple's induced order is cyclic]` — the kind of quantity XYZ / Shepp-type correlation
results and Kahn–Saks machinery are about. `c3 §4`'s `max db` / `min db` columns are the first
data on it and they are **not encouraging**: `max db = 1/2` across the extremal class, attained
wherever the star crosses a chain triple, which suggests the honest per-triple question has to be
asked over the *incomparable* triples only.

### 6.1 The literature half of first move 3 — POINTERS, NOT FINDINGS

⚠️ **These were surfaced by one web search and NOT READ.** They are recorded so a successor does
not repeat the search, and nothing in this document rests on any of them. Anyone citing them owes
the reading.

- *The Polytope of Probability Functions on a Finite Poset*, arXiv **2502.01604** (2025) — the
  image of `P ↦ (p(x,y))` as a polytope. On the title alone this is the closest object to §2's
  two-route identity and to the triangle inequalities, and it is where a per-triple bound would
  live if one is known.
- *Variance vs. range for linear extensions, and balancing extensions in posets of bounded width*,
  arXiv **2510.26134** (2025) — recent, and about the quantities `mg-dcae`'s variance/bias split
  already uses.
- *A correlational inequality for linear extensions of a poset* (Shepp, `Order` 1980) — the XYZ
  theorem itself. ⚠️ This corpus already records that FKG/XYZ are **wrong-signed** for the
  neighbouring residual `(B-cov)` (`STATE.md`, obstruction 4), so an unexamined appeal to them
  here would be repeating a mistake this repository has already paid for.

`docs/BASIC-FACTS.md` fact 3 closes with the general form of this warning and it applies to the
successor as much as to this ticket: *"any proposed structure making the bias telescoping, a
potential or a coboundary proves the conjecture in one line — check for that before building on
it."* Step 4 asks for an approximate version of that structure. §5 is what the approximation
costs.

## 7. What this landing deliberately does not move

`STATE.md` is untouched, so the ratchet is untouched, no ledger row moves and no twin re-pin is
owed — measured at `mg-3e5e` the file stood at exactly its ceiling, 5199 of 5199 words, and this
ticket has no claim on that budget. `docs/FACTS.md` gets **no entry**: every measurement here is
consumed by this document, which fails that registry's homelessness test (`mg-3da1`'s reason).
`docs/CONCEPTS.md` gets no row. `code/cyclic_bias_7c32/` is **not** in `build.sh` — nothing
consumes it, its subject is a research line rather than a control, and it costs 75 s against a
gate measured at 47.5 s; adding it is a separate decision with a separate price.

**The census movement is attributed rather than left as drift.** `mg-9876`'s arm census moves
`232 → 234` directories and **only one of the two is this branch's**: the other is
`verdict_invariance_585e`, `main`'s own landing whose census refresh `main` did not take. §3's
`ships a file named for negative/self/positive-control` goes `153 → 155` (`c0_selftest.py` here,
one site there) and `a committed transcript records a demonstrated failure` goes `153 → 155`
(`out_c0_selftest.txt` carries `CAUGHT` from the five live plants). ⚠️ **§1's smell index moves
`220 → 222` in `76 → 77` directories and NONE of it is this branch's** — the whole delta is
`verdict_invariance_585e:2` and `cyclic_bias_7c32` does not appear in the full list at all, which
was checked by diffing that list rather than assumed. `NEITHER, though the directory ships code`
stands still at 27, the `| tee` count stands still at 30 (this suite's only `| tee` is inside a
comment, which a4 skips), and `out_gate.txt`'s byte counts `11818` and `55076` are **unchanged**,
which is the half of those lines that is repo state saying this branch adds nothing either census
counts by size. Restored and not committed on `mg-f771` g0's own CORPUS grading, with
`alias_agreement`'s two, `out_gate.txt` and `out_g1_controls.txt` restored on its NOISE grading
(`mg-4020`) — all four differ only in wall-clock. `./build.sh` is **GREEN**, `worst suite exit: 0`,
with g0 reporting `0 red, 3 NOISE, 1 CORPUS`.
