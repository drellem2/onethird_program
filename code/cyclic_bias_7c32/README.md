# mg-7c32 — the pair bias as a 1-cochain, and what its coboundary buys

**One sentence.** The research line filed as `mg-7c32` is correct at every step, its step 1
is a genuine dictionary entry this corpus did not have — *the coboundary of the pair bias
is the cyclic-orientation bias* — and its step 4 is **measured here to be the conjecture
restated rather than a reduction of it**, because the "average triple bias" is the defect
`D` divided by `n − 2` and `D` is the same scalar step 3 already bounds.

**Run it:** `sh run_all.sh` — standard library only, ~75 s, four arms, exit 0 on green.
Two consecutive runs are byte-identical on all four transcripts: there is no clock, no
randomness and no sampling anywhere in the suite.

---

## 1. What the ticket asked for, and what came back

The ticket's own instruction was *"it is elementary throughout and every step is one line,
so it should be cheap to check or break — do that first"*, with four first moves in cost
order. All four were run.

| First move | Result |
|---|---|
| 1 · check steps 1–3 symbolically and numerically to `n = 7–8` | **Steps 1, 2, 3 all confirmed exactly.** c1 (471 804 ordered triples, two independent routes), c2 (152 609 telescopes over every base point; 39 426 over every chain at `n ≤ 5`), c3 §1 (19 446 posets). Nothing in the derivation is wrong. |
| 2 · measure how close real posets get to the bound | **Done, c3 §3–§4, and it cuts against step 4.** On the extremal class `δ(P) = 1/3` at `n = 8` — the closest population to the counterexample hypothesis that exists — the average `db` is `5/18 ≈ 0.278`, and `0 of 12` reach step 4's target of `< 1/6` at **any** base point. |
| 3 · search the literature and this corpus before proving anything | **The corpus half is decisive and the ticket's assumption was wrong.** `docs/BASIC-FACTS.md`, landed the same night at `73af2f3`, already carries step 1's triangle inequalities (fact 1), step 2 verbatim (fact 2) and step 3 with `D = 0` (fact 3). See §3. |
| 4 · only then, the base-point / bracketing optimisation of step 4 | **Both resources priced, and one of them is empty.** The bracketing buys *nothing* — `D` is bracketing-invariant (c2 §2, P5 refuted). The base point does move `D`, and c2 §1 shows an **end point is optimal**, so the ticket's "lazy" choice was already the right one. |

## 2. The finding, as an inequality

Write `L* = x_1 < … < x_n` for the majority order and `A` for the mean bias over its
`n − 1` consecutive pairs. Then, exactly and unconditionally (c3 §2, 19 441 posets, 0
violations):

```
avg db  =  ( (n-1) A  -  b(x_1, x_n) ) / (n-2)         so    | avg db  -  A |  <=  1/(n-2)
```

**The average cyclic bias is the average pair bias plus `O(1/n)`.** Dividing `D` by `n − 2`
does not produce a new object with its own theory: no step of the argument ever bounds an
*individual* `db`. Steps 3 and 4 are a lower and an upper bound on the same scalar,
computed from the same two inputs.

Consequently:

- **Under the hypothesis**, `A > 1/6` gives `avg db > 1/6 − 1/(3(n−2))`, which *is* step 3
  divided by `n − 2`. Proving `avg db < 1/6 − ε` under the hypothesis means proving the
  hypothesis inconsistent — i.e. proving the conjecture, not reducing it.
- **Without the hypothesis** the target is false: a chain has `avg db = 1/2` (c2 §3), and
  `db = 1/2` holds at exactly the chain triples (c1 §3).

There is no third reading. The intended contradiction is *sound* — the strategy would work
if the bound existed — but the bound is the conjecture in the star's coordinates.

## 3. The dedup result, which the ticket asked for and predicted wrong

The ticket says a search *"on 'cyclic order', 'triple bias', '3-cycle probability',
'linear ordering polytope' returned nothing here"*. It returns `docs/BASIC-FACTS.md`,
committed at `73af2f3` on 2026-08-14 — the same night — under different vocabulary:

| ticket | `docs/BASIC-FACTS.md` |
|---|---|
| step 1, the `1 ≤ Σp ≤ 2` half | **fact 1**, *the triangle inequalities hold*, with the same `N ∈ {1,2}` derivation |
| step 2 | **fact 2**, *in a counterexample the majority relation is a linear extension of `P`*, same proof |
| step 3 with `D = 0` | **fact 3**, *a counterexample's bias cannot be exact*, same telescope |
| step 1, the `db = Pr[cyclic] − 1/2` half | **absent — this is the new content** |
| step 3 with `D` carried, and step 4 | **absent, and priced above** |

Fact 3's own closing line is the ticket's step 4 already answered from the other side:
*"any proposed structure making the bias telescoping, a potential or a coboundary proves
the conjecture in one line — check for that **before** building on it."* Step 4 asks for
an approximate version of exactly that structure, and §2 above is what the approximation
costs.

## 4. What survives, and it is not nothing

`db` **is** the cyclic-orientation bias (c1 §2, exhaustive, two routes). That makes a
**per-triple** bound a well-posed and strictly stronger question than the average, and one
that correlation machinery can be pointed at:

> does the counterexample hypothesis force `db(x_1, x_{k−1}, x_k) ≤ 1/6 − ε` for **every**
> `k`, or is only the aggregate controlled?

The aggregate is `D` and `D` is already step 3. An individual `db` is not. c3 §4's
`max db` / `min db` columns are the first data on it, and they are not encouraging —
`max db = 1/2` on the extremal class, attained wherever the star crosses a chain triple.

## 5. What this directory deliberately does not do

- **It is not in `build.sh`.** Nothing else in the repository consumes it, its subject is a
  research line rather than a control, and it costs 75 s against a gate measured at 47.5 s.
  Adding it is a separate decision with a separate price, and it belongs to whoever wants
  the gate to hold this.
- **It does not open a cohomology arc**, which the ticket forbids in so many words. The
  word *coboundary* appears because it is the correct name for `b(x,y)+b(y,z)+b(z,x)` and
  for nothing else; there is no complex, no `H^1`, and no claim about either. `mg-01ce`
  (F31, RED) and `mg-d0fa` (F28, AMBER) are what that arc costs and none of it is invoked.
- **It touches `STATE.md` not at all**, so the ratchet and the twin pin are untouched and
  no ledger row moves. It adds **no** entry to `docs/FACTS.md`: every measurement here is
  consumed by the write-up that lands with it, which fails that registry's homelessness
  test (`mg-3da1`'s reason).
- **It measures nothing about the counterexample class**, because that class is empty at
  every reachable `n` (c3 §1: `min δ(P) = 1/3` at `n = 3..8`; the conjecture is verified to
  `n = 14`, `mg-33f5`). Both c3 §3 and c3 §4 carry that warning, in opposite directions,
  because the population supports a wrong reading either way.

## 6. Files

| file | what it is |
|---|---|
| `lib7c32.py` | posets, exact marginals, the coboundary by two routes, the star telescope |
| `c0_selftest.py` | six planted defects; five must be **CAUGHT**, D6 must be **INERT** |
| `c1_identity.py` | step 1, exhaustive `n ≤ 7`, two routes; and where the ceiling `db = 1/2` sits |
| `c2_telescope.py` | step 3 at every base point, two bracketings, the degenerate cases |
| `c3_bound.py` | step 2 exhaustive `n ≤ 8`; what `avg db` reduces to; the verdict on step 4 |
| `PREDICTIONS.md` | ten predictions, **four refuted**, including two of this directory's own |
