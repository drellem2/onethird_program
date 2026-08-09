# `mg-c50b` — PREDICTIONS

**Filed before one line of `libc50b.py` exists.** Committed as its own commit, ahead of the
instrument, so that the scoring in the final document is against a fixed target.

---

## H. EXPOSURE — WHAT I ALREADY KNOW, DISCLOSED RATHER THAN LAUNDERED

This is a **very large** dispatch-delivered exposure and I am not going to pretend otherwise.

* **H1.** My ticket body prints `mg-51f4`'s central results verbatim: the `n = 7` population
  (`96428` / `86278`), the failure counts (**168** for `(F)`, **4** for `(M♯)`, **0** for both),
  the maxima (`f* = 1.297074`, `c♯ = 1.018707`), the whole `c_or(n)` sequence
  `0.250, 0.306, 0.551, 0.754, 0.894`, the floor theorem `c♯ ≥ Δ_P − γ/2`, and the γ-bin
  mechanism (`(F)` above 1 only at `γ < 0.1`, `(M♯)` only at `γ ∈ [0.1,0.3)`).
  **Every reproduction of any of those is a `[FORMALITY]`** and is tagged as such below.
* **H2.** Before writing this file I read, in full: `docs/OneThird-SweepLoss-mg-51f4.md`
  (all 401 lines), `docs/OneThird-L2-Conditionality-mg-28ff.md` §0–§4, and
  `docs/OneThird-C3-PrefixCapture-mg-76b2.md` §2–§3. **All definitions used by my instrument
  come from those documents.** Nothing definitional below is a discovery.
* **H3.** I have **not** opened `code/sweep_loss_51f4/lib51f4.py` or any `s*.py` in that
  directory, and I will not open any of them until my own `n ≤ 7` census has been produced and
  committed. That is the only thing that makes my re-derivation worth the word *independent*,
  and the ticket asks for it explicitly ("A merge is not a check").
* **H4.** I derived, on paper before writing this file, the reformulation in P1 below
  (`(M♯)` fails ⟺ `μ_pref > Δ_P − √(Δ_P² − 2γ)`), the bound `μ_pref ≤ 2Φ*_pref`, and the
  bound `M ≤ Δ_P`. These are **mine and pre-run**, but they are elementary and I claim no
  priority over anyone who writes the same two lines.

---

## THE PLAN, BOUND IN ADVANCE

The ticket admits two outcomes, **(a)** prove the disjointness uniformly in `n`, **(b)**
exhibit a poset where both routes fail. I commit in advance to attacking **both** and to
reporting whichever lands, and to a **third** deliverable that is neither:

> **(c) DELIMIT THE PROOF SPACE.** Reduce "both routes fail" to an exact scalar system in the
> route invariants, then decide whether that system is *feasible* under every unconditional
> inequality this corpus holds. If it is feasible, **no proof of the disjunction can be built
> out of those invariants alone**, and the missing lemma can be named exactly.

I state now, so it cannot be retro-fitted: **I expect (c), not (a) or (b).**

---

## THE BETS

Probabilities are my honest credences at filing time. `[FORMALITY]` = pre-answered by H1.

| | bet | p |
|---|---|---|
| **P1** | `[DERIVED PRE-RUN]` `(M♯)` fails at `P` **iff** `Δ_P² > 2γ` **and** `μ_pref > t*(P) := Δ_P − √(Δ_P² − 2γ)`; and `(F)` fails **iff** `M > √(2γ)`. So the disjunction is exactly: *at every primitive poset, `M ≤ √(2γ)` or `μ_pref ≤ t*`.* I expect this to be an identity, not an approximation, and to reproduce all 168/4/0 counts. | 0.93 |
| **P2** | **PRINCIPAL LIVE BET.** The scalar relaxation is **FEASIBLE**: there is an assignment of `(γ, Δ_P, Φ*_pref, M, μ_pref)` satisfying *every* unconditional inequality I can establish (`γ ≤ μ_pref`, `μ_pref ≤ 2Φ*_pref`, `Φ*_pref ≤ M ≤ Δ_P ≤ 1`, `φ_k ≤ Δ_P`, and `γ ≤ n·ℓ_k/(k(n−k))` for every `k`) at which **both** routes fail. Hence **the disjunction is NOT a consequence of the route invariants**, and every proof attempt that works only with them is dead before it starts. **Guard, bound now:** I must exhibit the feasible point numerically AND list the inequalities it satisfies one by one, or P2 is scored LOST regardless of how obvious it looks. | 0.80 |
| **P3** | The exhaustive `n = 7` counts re-derive **exactly** on my instrument: `96428` posets, `86278` primitive, `(F)` false at **168**, `(M♯)` false at **4**, both at **0**. `[FORMALITY]` — but the ticket orders it done and it is the one thing here that could show the lineage is standing on sand. | 0.85 |
| **P4** | ...and if any one of those five numbers disagrees, the disagreement is in **`(M♯)`'s 4**, not in the population or in `(F)`'s 168 — because `(F)` is one exact PSD decision per poset whereas `(M♯)`'s needs a copositivity bracket, which is the only place a subtle bug can hide. | 0.60 |
| **P5** | **HEIGHT IS THE HIDDEN VARIABLE, and it separates the two failure sets better than `γ` does.** Specifically: every one of the 168 `(F)`-failures at `n = 7` has height ≤ 3, and every one of the 4 `(M♯)`-failures has height ≥ 4. **Guard:** I must print the full height distribution of both failure sets and of the whole population before scoring, so that "better than `γ`" is a measured statement about overlap and not a slogan. | 0.45 |
| **P6** | `μ_pref = γ` (i.e. `ρ = 1`, L2's first disjunct) at **every** height-2 poset, at every `n` I test. If it holds it is a uniform-in-`n` sufficient condition for `(M♯)`, since `ρ = 1 ⟹ c♯ = Δ_P − γ/2 < 1`. | 0.35 |
| **P7** | I will **not** find a poset where both routes fail — not at `n = 8` on whatever population I reach, not on any family, not by local search. Outcome **(b) does not land.** | 0.75 |
| **P8** | `c_or(8) > c_or(7) = 0.894`, i.e. the sequence is still rising at the next point. **This is a bet about `n = 8` only. It is NOT an extrapolation and I will not print a projection to any `n > 8`** (scope guard 3). If I cannot reach `n = 8` on a defensible population, P8 is scored **NOT RUN**, not held. | 0.55 |
| **P9** | The `min_{k,ℓ} Q_{kℓ}/N_{kℓ}` entrywise-nonnegativity certificate is a *valid* lower bound on `μ_pref` (trivially — it certifies copositivity of `Q − tN`), and it is **attained on the diagonal**, hence **equal to `μ_pref` exactly**, at ≥ 50 % of primitive posets at `n ≤ 6`. If true this is a cheap exact `μ_pref` at large `n`, which is what any counterexample hunt past `n = 15` needs. | 0.30 |
| **P10** | The two routes' failure sets stay disjoint but the **margin closes**: `max_P min(c♯,f*)` at `n = 8` is attained at a poset where *neither* route is anywhere near its own maximum — i.e. the `c_or` argmax is a third population, not the union of the two extremal families. | 0.55 |
| **P11** | `[FORMALITY]` reproduce `mg-28ff`/`mg-51f4`'s `n ≤ 6` population: `5230` total, `4377` primitive, `1/4/27/275/4070` primitive by `n`, `c_true(6) = 0.327508`, `c♯(6) = 0.943151`. | 0.90 |
| **P12** | The sixth-decimal disagreement `mg-51f4` records at `f*(6)` (`0.811654` vs `0.8116489`) resolves in **`mg-51f4`'s** favour on my instrument. It is not mine to adjudicate and I will report it and stop. | 0.70 |

---

## ERRORS I EXPECT TO MAKE — filed so I cannot discover them as surprises

* **E1. I publish a maximum over a FAMILY as a maximum over `n`.** This lineage has now
  committed this defect at least three times by its own count. Guard: every number in my
  document that is not from an exhaustively enumerated population carries the word
  **FAMILY** or **SEARCH** in its own cell.
* **E2. I extrapolate `c_or`.** Scope guard 3 forbids it and it is the single most tempting
  thing in the ticket. Guard: the string `n ≥ 99` may appear in my document **only** in a
  sentence saying that nothing here reaches it.
* **E3. I report `(M♯)` FAILS off an exhibited-vector `c♯`.** An exhibited monotone vector
  bounds `μ_pref` from **above**, so it can certify that `(M♯)` HOLDS and can **never**
  certify that it fails. `mg-51f4` names this exact trap. Guard: the FAILS verdict is
  emitted only behind an exact copositivity certificate, and every uncertified row prints
  `n/a`, never `FAILS`.
* **E4. My copositivity face enumeration silently skips singular faces** and I read the
  resulting `min` as exact. Guard: singular faces are counted and printed; if the count is
  nonzero at a poset whose verdict depends on it, the instrument **refuses** rather than
  guesses.
* **E5. I re-attack `(M♯)` with a better test vector without noticing.** The floor theorem
  kills that class in advance and scope guard 1 forbids it. Guard: if I find myself searching
  for a better monotone vector for any reason other than *bounding `c♯` from above to certify
  that `(M♯)` HOLDS*, I have left the ticket.
* **E6. I confuse the profile `φ_k = leak(A_k)/min(k,n−k)` with `leak(A_k)` itself.**
  `mg-51f4` §5 prints the `(M♯)` witness's profile as `(5/19,…)`; that is `φ`, not `leak`, and
  reading it as `leak` inverts `Φ*_pref`. Guard: reproduce that witness's `Φ*_pref = 5/19`,
  `Δ_P = 18/19`, `μ_pref = 0.226537524`, `c♯ = 1.018707` to every printed digit as a **forced
  arm of the selftest**, before any census runs.
* **E7. I score P2 on a feasible point that violates an inequality I forgot to list.** The
  whole value of P2 is the completeness of the constraint list, and nothing checks that list
  but me. Guard: the constraint list is machine-checked against the *actual* `n ≤ 6`
  population — every listed inequality must hold at 4377 of 4377 posets, or it is not an
  inequality and comes out of the list.
* **E8. I claim "independent" while having read the parent's instrument.** Guard: H3, and a
  `git log` timestamp showing my census committed before any file under
  `code/sweep_loss_51f4/` is opened.
* **E9. I treat a `min` over a *sampled* `n = 8` population as `c_or(8)`.** Guard: P8's own
  wording — NOT RUN unless the population is exhaustive or explicitly labelled a SEARCH
  lower bound on `c_or(8)`, which is a different object and is printed under a different name.

---

## WHAT I WILL NOT TOUCH

L2. `ε₀`. `17/78`. `STATE.md`. `roadmap.md`. `mg-28ff`'s, `mg-51f4`'s or anyone else's
document. The sweep's loss `Λ_M` (scope guard 2 — closed). A better monotone test vector for
`(M♯)` (scope guard 1 — dead by the floor). Any projection of `c_or` past the largest `n` I
actually compute (scope guard 3).
