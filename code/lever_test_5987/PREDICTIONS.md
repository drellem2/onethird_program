# mg-5987 — predictions, written before the arms were run

Each line is what I expected, what happened, and — per this estate's rule — **what the prediction
was exposed to**, because a prediction nobody could have got wrong is not evidence of anything.

| # | prediction | exposure | outcome |
|---|---|---|---|
| P1 | The frozen class is empty at every `n ≤ 7`. | **None.** `mg-9b6b` and `mg-0b96` both measured it to `n = 8`. Re-established here because a directory that prints zeros over a class it did not check is printing zeros about nothing. | **CONFIRMED** (`g1` §1). |
| P2 | Both statements are FALSE unconditionally, so the hypothesis is load-bearing. | Low — `(B)` is known false for abstract frozen laws (`STATE.md`, obstruction 4). What was not on the record is a single explicit family refuting **both** with closed forms at every `n`. | **CONFIRMED** — the antichain, `bias = (n−1)/2`, `ρ = (n−2)/3` (`g1` §2). |
| P3 | The reference order `e` is defined at almost no reachable poset, so `(EQ)` and `(B-cov)` cannot be evaluated off-class without a convention. | Real. I did not expect the equivalence to be exact: *fully decided* **is** `δ(P) ≤ 1/3`, so the definedness of the notation and the emptiness of the class are ONE fact. | **CONFIRMED and sharper than predicted** (`g1` §3). |
| P4 | The barycentric order minimises the bias over all reference orders, so a price computed under it is a lower bound on the price under every reading. | Real, and it is the load-bearing half of the reading argument. | **CONFIRMED, 224 of 224 primitives at `n ≤ 6`** (`g1` §4a). |
| P5 | …and the same order does the same job for `(B-cov)`. | Real. | **REFUTED.** It sits at the **max** over `e` for `ρ` — 224 of 224 — because it roughly minimises inversions and inversions are `(B-cov)`'s denominator. The favourable end is a different end for the two objects; each verdict is now stated at the end that cannot flatter it. |
| P6 | `(B-cov)` and `(EQ)` **escape** step 2 — their contrapositives do not imply the conjecture on a class. | Real, and this was the ticket's hoped-for outcome. | **REFUTED, and by a triviality.** Contraposition is an equivalence, so *every* frozen-conditional statement is the conjecture restricted to the complement of its conclusion. Step 2 cannot return NO on this kind of object at all. The content is entirely in the price. |
| P7 | The primitive floors of both quantities decay with `n`, like `d`'s `2/n`. | Real. | **REFUTED over the swept range.** `floor_bias` = `1/3, 2/5, 4/11, 4/13, 4/13, 37/123` and `floor_ρ` = `1/3, 8/25, 2/5, 2/5, 176/399, 140/319` at `n = 3…8` — neither monotone, neither near zero, and an explicit primitive family caps both at every `n`. |
| P8 | A non-decaying floor is GOOD for the lever — it means the contrapositive never covers a whole order. | Real, and this one was **backwards**, which computing it is what said. A decaying floor is what makes `(R)`'s delivery **stop** at `n = 2/D`. A floor pinned at `Θ(1)` is never overtaken by a fixed setting, so below the floor the delivery has no cutoff at all. | **REFUTED — direction reversed** (`g2` §2, `g3` §5). |
| P9 | The orders counter and the coverage fraction agree, so the refinement is a formality. | Real. | **REFUTED.** At `C = 2/5` the counter says `(EQ)` delivers **nothing** and the coverage says it settles **99.8%** of the primitives at `n = 8` — 31 posets of 12 524 carry the entire difference. |
| P10 | The unreached-order figure — mg-9b6b's own currency — is computable for both once the sweep is done. | Real, and this is the finding the ticket's *"or say why the test does not apply"* branch was written for. | **REFUTED.** The currency is a function of the floor **above `n = 14`**; `(R)` has that as a theorem (`2/n`) and neither of these has anything. No sweep closes it — `n = 12` is still inside the verified range. |
| P11 | The zigzag's two limits are ordinary algebraic numbers. | None — arithmetic. | **CONFIRMED**, and prettier than expected: `bias → 1/φ² = (3−√5)/2` and `ρ → 1 − 1/√5`, with `bias(Z_n) = F_{n−1}/F_{n+1}` **exactly** at every `n`. |
| P12 | Three planted defects, all live. | Real. | **REFUTED, twice.** Two of the five candidates came back **inert** — one branch is unreachable for a structural reason and one for an **imported invariant** (`lib6ff4`'s canonical labelling is a linear extension). Both are printed rather than swapped out, and the second is checked in both directions: reverse the loop and the case arises 455 times, where the operation is a no-op. |

## What I would have got wrong without the instrument

**P8 is the one.** The first draft of this directory's verdict read *"the floors do not decay, so the
price is zero and both residuals escape"* — and the arithmetic says the opposite: it is `(R)`'s
decaying floor that **caps** its price at 96 orders, and a floor that does not decay is the worse
case, not the better one. The sentence survived long enough to be written down and was killed by
the table under it.

**P9 is the second.** Without the coverage column the honest-looking verdict *"delivers 0 orders at
`C = 2/5`"* would have shipped, and it is 31 posets away from *"delivers the whole order"*.
