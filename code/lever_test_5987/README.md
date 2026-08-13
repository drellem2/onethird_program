# mg-5987 — `mg-9b6b`'s lever test, run on `(B-cov)` and `(EQ)`

`sh run_all.sh` — four arms, standard library only, exact `Fraction` on every verdict path, ~4 min,
two consecutive runs byte-identical. Predictions with the exposure disclosed per line:
[`PREDICTIONS.md`](PREDICTIONS.md). Deliverable:
[`docs/OneThird-LeverTest-mg-5987.md`](../../docs/OneThird-LeverTest-mg-5987.md).

| arm | question | transcript |
|---|---|---|
| `g0_selftest.py` | are the two numbers per poset what they claim to be? | `out_g0_selftest.txt` |
| `g1_step1.py` | **step 1** — is the hypothesis `frozen`? | `out_g1_step1.txt` |
| `g2_step2.py` | **step 2** — does it imply the target on a class, and what does that cost? | `out_g2_step2.txt` |
| `g3_dial.py` | **step 3** — what does the whole dial do? | `out_g3_dial.txt` |

## 1. The verdict in one paragraph

**The test does not kill `(B-cov)` and `(EQ)`, and it does not clear them either — it cannot
return an answer on them, and the reason is one missing theorem rather than one missing sweep.**
`mg-9b6b`'s currency is *unreached orders*: the orders of the conjecture a residual's contrapositive
delivers above the census frontier of 14. That number is a function of the **primitive floor**
`floor_Q(n) = min{Q(P) : P primitive at order n}` above `n = 14`. For `(R)` the floor is a theorem —
`d ≥ 2/n` — which is exactly what let `mg-9b6b` write *"forbids up to `n = 98`, 84 of them
unreached"*. For these two the floor is a **census stopping at `n = 8`**, every order of which is
already verified, and no further sweeping closes that: `n = 12` is still inside the verified range.

What the census does settle is the **two ends of each dial**, and they disagree:

| | `(EQ)_C` | `(B-cov)_C` |
|---|---|---|
| delivers **0 orders at every `n`** | `C ≥ 2/5` | `C ≥ 4/5` |
| delivers **every order `3…8`** | `C < 37/123 = 0.3008` | `C < 8/25 = 0.3200` |

⚠️ The two lower thresholds are **not** the numbers an eye picks off the floor table: both minima
sit at an **end** of the swept range and `(B-cov)`'s is at `n = 4`, because neither floor is
monotone in `n`. `g3` reads them from `floors.json` — which `g2` writes — rather than carrying a
copy, because a figure typed into two files goes stale in one of them.

The upper row is a **theorem**, not a census: an explicit primitive family caps both floors at
every `n` (§3 below). The lower row is the measured floor. And the flip between them —
`≈ 0.3–0.8`, i.e. **15× to 40× `ε_dem`** — sits **inside the window `STATE.md` leaves unpinned on
the constant the architecture actually consumes** (*"genuinely small and unpinned by ~2 orders of
magnitude"*, audit F5). So *"is it a lever?"* is not a question about either residual's
mathematics. It is a question about a constant nobody has computed end to end.

## 2. What step 2 turned out to be

`mg-9b6b`'s step 2 — *does it imply the target on a class?* — **cannot return NO on a
frozen-conditional object**, and saying so is the first thing this directory did:

```
frozen(P) ⟹ Q(P) ≤ C        is        Q(P) > C ⟹ ¬frozen(P) ⟹ δ(P) ≥ 1/3
                                       ─────────────────────────────────────
                                       the conjecture, restricted to {Q > C}
```

Contraposition is an equivalence, so *every* statement of this shape **is** the conjecture
restricted. `(R)` was not special in kind. The content of step 2 is entirely in the **price**, and
the price is entirely in the floor.

**And the floor's direction runs the opposite way from how it first reads.** `{d > D}` covers order
`n` while `2/n > D` and stops at `n = 2/D` — so `(R)`'s **decaying** floor is what makes its price
*finite*. A floor pinned at `Θ(1)` is never overtaken by a fixed setting, so below it the delivery
has **no cutoff at all**. That sentence was written backwards in this directory's first draft and
the table under it is what killed it (`PREDICTIONS.md` P8).

## 3. The family, and why it is not `mg-9b6b`'s

`Z_n`: `x_i < x_j` iff `j − i ≥ 2`. The incomparable pairs are exactly the consecutive ones, so
`L(Z_n)` is in bijection with the **matchings of a path** and everything is closed form:

```
|L(Z_n)| = F_{n+1}      q_i = Pr[(i,i+1) transposed] = F_i F_{n−i} / F_{n+1}
h(x_i) − i = q_i − q_{i−1}       C_{x_i} = 2 q_i q_{i−1}       E[inv_e] = Σ q_i
```

`max_x |h − rank_e| = F_{n−1}/F_{n+1} → 1/φ²` and `Σ C_x/E[inv_e] → 1 − 1/√5`, and the caps
`≤ 2/5` and `≤ 4/5` are theorems at every `n` from one Fibonacci identity
(`F_{a+b−1} = F_a F_b + F_{a−1} F_{b−1}` ⟹ `q_i ≤ q_1`), checked in `g3` rather than cited.

⚠️ **`Z_n` is PRIMITIVE at every `n`** — its incomparability graph is a path. That is the whole
reason it can carry a verdict: `mg-9b6b`'s refuting family was ordinal sums, so `mg-f5be`'s
primitivity objection lapsed it above `n = 3`. This one is immune to that objection.

**`C_{x_i} = 2 q_i q_{i−1} ≥ 0` derives `docs/FACTS.md` F11's sign instead of measuring it** — the
event *`(i,i+1)` transposed* implies *`(i−1,i)` untransposed*, so the covariance is `q_i q_{i−1}`.
F11 measured `C_x > 0` at 555 of 555 sampled rows; this is the same sign with a reason attached, on
a family F11's population does not reach.

## 4. The refinement `mg-9b6b`'s counter cannot make

The orders counter is binary per order: it returns `0` for a statement that settles nothing **and**
for one that settles every primitive but one. At `C = 2/5` it says `(EQ)` delivers **nothing**, and
the coverage says `(EQ)` settles **99.8%** of the primitives at `n = 8` — 31 posets of 12 524 carry
the whole difference. Both numbers are true and only one of them is informative. Every price in
this directory is therefore reported with its coverage beside it.

## 5. Controls

`g0` is 27 controls and the arms are worth nothing without it.

- **Both numbers computed twice by different routes** — the order-ideal DP that never builds a
  permutation, and brute-force enumeration of `L(P)` that never uses the DP. `h`, `Var(pos_x)`,
  `E[inv_e]` and `mg-dcae`'s split `E[Σ disp²] = Σ Var + Σ b²` all agree at every non-chain class
  `n ≤ 5` plus a sample at `n = 6`, at two reference orders each.
- **The enumerator** against OEIS A000112; **`count_ext`** against brute force at all 405 classes
  `n ≤ 6`.
- **Both closed forms** against the general machinery, term for term, `n = 3…11`.
- **The price machinery** against `mg-9b6b`'s own published figure — `(R)` at row 8 forbids a frozen
  primitive up to `n = 98`, 96 orders, 84 unreached. ⚠️ Computed **through** `lib9b6b`, so it is a
  consistency check on this arm and **not** a second measurement of that figure.
- **A wrong-direction control.** `g1`'s central measurement is a zero — `e` is fully decided at 1
  primitive over `n ≤ 7`. A zero over an empty class is worth nothing, so the same machinery is
  asked at `β = 2/5`, where the class is **not** empty (32 primitives), and it returns real
  reference orders there — and they **equal** the barycentric stand-in at **33 of 33** across both
  thresholds.
- **Three live planted defects, two declared inert.** The inert pair is printed rather than swapped
  out: one branch is unreachable for a structural reason, one for an **imported invariant**
  (`lib6ff4`'s canonical labelling is a linear extension), and the second is checked in both
  directions — reverse the loop and the case arises 455 times, where the operation is a no-op.

## 6. Where this could be wrong

- **⚠️ The operative form of `(B-cov)` is a READING and it is this directory's.** `STATE.md` states
  the residual in words; the quantitative form priced here, `Σ_x C_x = O(E[inv_e])`, is read off
  `mg-dcae`'s variance/bias split as the attempt index records it, together with F11's `C_x`.
  `(EQ)` needs no such reading. A different normalisation moves `(B-cov)`'s floor and its half of
  the dial; the `(EQ)` half and every structural finding are untouched.
- **The `n = 8` sweep is PRIMITIVES ONLY.** No number here is claimed for the `n = 8` non-chain
  population.
- **`(R)`'s column is computed through `lib9b6b`**, the library that published it. Consistency, not
  corroboration; a disagreement would impeach this directory first.
- **The floors are a census to `n = 8` and the whole verdict says so.** Anything read from them
  about `n > 8` is an extrapolation and is marked as one at the table.
- **`ρ(Z_n) ≤ 4/5` is the provable cap; the measured sup over `n ≤ 399` is `0.5509` and the limit
  is `1 − 1/√5 = 0.5528`.** The gap between the provable cap and the true one is not closed here,
  and `g3` prints both rather than the prettier one.
- **`F11`'s sign is REPRODUCED, not independently corroborated** — `p_before` is shared with the
  library F11 was measured through. What is independent is the population and the closed form.
- **Nothing here shows either residual is false.** Both are true if the conjecture is.
- **Per `STATE.md`'s standing rule**, every aggregate sentence about this directory's census
  results is `FP`; only §2's contraposition and §3's family caps are `U`.

## 7. What was NOT done

- **No attempt to prove or disprove either residual.** The question was the shape, not the truth.
- **The floor theorem was not proven** — it is named as the successor and its two possible shapes
  are spelled out in `g3` §5.
- **The architecture's required constant was not computed.** That it is unpinned is `STATE.md`'s
  own record (audit F5); that the unpinning now decides a lever question is this directory's
  finding, and closing it is not in this ticket's scope.
- **No ledger row was edited.** `(B-cov)` and `(EQ)` are residuals in *Where the threads converge*,
  not ledger rows, so no twin re-pin is owed.
