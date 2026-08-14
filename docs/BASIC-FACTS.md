# BASIC FACTS — the problem itself, read before the archive

**Read this before `STATE.md`, `docs/FACTS.md`, or any `docs/OneThird-*.md`.** If you are about to
assert something about the 1/3–2/3 conjecture and your warrant is *"a previous arc concluded X"*,
check it against these four first. Each is one line from the definitions; none needs the archive.

**Four facts, and the shortness is the point.** Daniel, 2026-08-14 (`mg-3e5e`), after correcting the
same elementary property twice in one exchange: *"you are again anchoring too heavily on past
research … ditto for very basic facts about the problem for your agents **but don't overdo it**."*
The failure is not missing information — it is reaching for **what a past arc concluded** instead of
**what is true of the object**, which yields answers that are well-cited and about the wrong thing.
**If this file grows past a screen it has stopped working**, because the next agent will skim it.

```
P          a finite poset on n elements, NOT a chain
L(P)       its linear extensions, uniform measure
p(x,y)     Pr[x <_L y] for L uniform on L(P)
b(x,y)     = p(x,y) − 1/2, the BIAS.  Antisymmetric: b(y,x) = −b(x,y)
           x ∥ y ⟹ |b| < 1/2 (both orders occur)      x <_P y ⟹ p = 1, b = 1/2

CONJECTURE            some incomparable pair has p ∈ [1/3, 2/3], i.e. |b| ≤ 1/6
COUNTEREXAMPLE HYP.   EVERY incomparable pair has |b| > 1/6
```
Verified to `n = 14` (`mg-33f5`), so a counterexample is larger than that.

---

**1 · THE TRIANGLE INEQUALITIES HOLD**, for any distribution over linear orders:
`1 ≤ p(x,y) + p(y,z) + p(z,x) ≤ 2`.
*Derivation.* A single linear order satisfies exactly one or two of `x<y`, `y<z`, `z<x` — never zero
and never three, since three is a 3-cycle. Take expectations. These are the 3-dicycle facets of the
**linear ordering polytope**; nothing here is specific to posets.

**2 · IN A COUNTEREXAMPLE THE MAJORITY RELATION IS A LINEAR EXTENSION OF `P`.** Orienting `x → y`
iff `p(x,y) > 2/3` gives a total, transitive `L* ⊇ P`, canonically determined by `P` — not a choice.
*Derivation.* **Total:** `1/2` lies in the forbidden band so every pair is oriented, and comparable
pairs have `p = 1` and orient with `P`. **Transitive:** a 3-cycle needs all three of
`p(x,y), p(y,z), p(z,x) > 2/3`, summing `> 2` against Fact 1; a tournament with no 3-cycle is
transitive.
*Not.* **Not a fact about posets in general** — majority cycles are real. `mg-24a3` exhibits one at
`n = 11` with edges decided by margins ≈ 0.50014, and finds none in the exhaustive sweep to `n = 7`,
so that sweep must not be read as general transitivity. The forbidden *middle band* is what closes
the composition; *"every pair has a majority"* alone would not.
([`code/counterexample_probe_24a3/probe_output.txt`](../code/counterexample_probe_24a3/probe_output.txt) §1a/§1a')

**3 · A COUNTEREXAMPLE'S BIAS CANNOT BE EXACT.** If `b(x,y) = f(y) − f(x)` for one function `f` on
the elements, then `P` is not a counterexample, at every `n ≥ 4` — unconditionally. So establishing
exactness on the frozen class **is** proving the conjecture, and the only room a counterexample has
is exactly the **failure of closure**.
*Derivation.* Suppose it is a counterexample and walk `L* = z_1 < … < z_n` (Fact 2). Every
consecutive step has `b(z_i, z_{i+1}) > 1/6` — incomparable pairs by hypothesis, comparable ones at
`1/2`. Exactness telescopes: `b(z_1, z_n) = f(z_n) − f(z_1) = Σ b(z_i, z_{i+1}) > (n−1)/6`. But
`b(z_1, z_n)` is a single bias value, hence `≤ 1/2`. Contradiction for `n ≥ 4`.
*Use it as a wall-detector.* Any proposed structure making the bias telescoping, a potential or a
coboundary proves the conjecture in one line — check for that **before** building on it.

**4 · THE MEASURE CARRIES DATA THE PAIR MARGINALS DO NOT — THE POSET DOES NOT.** `supp(μ)` and the
weights are surplus a marginal vector does not determine. Realizability does not reduce to the
pair-marginal map, and compressions can be defined on **all** subsets of `S_n`, not only via the BK
graph. (Daniel's correction, 2026-08-13/14.)
*Derivation.* The marginal map is many-to-one already at `n = 3`: uniform on `{123, 321}` and
uniform on all six of `S_3` both give `p = 1/2` at every pair, with supports of size 2 and 6.
*Not.* **Not** *"the poset `P` is more than its pair marginals"* — that form was measured **false**:
`P = {(x,y) : p(x,y) = 1}` reads the poset straight off the marginal vector and `P ↦ p(Unif L(P))`
is injective, exhaustively at all labelled posets `n = 3,4,5`
([`code/marginal_factoring_8b32/`](../code/marginal_factoring_8b32/) `b1`). The surplus is the
measure's, and the support-level witness for it exists (`b3`).

---

**Where this is read from, and what is deliberately not here.** Routed from
[`../README.md`](../README.md) and [`../EXECUTIVE-SUMMARY.md`](../EXECUTIVE-SUMMARY.md), the two
unratcheted entry documents, both ahead of the archive on the read path — a registry nobody is
routed to is the defect `mg-ea7f` was filed for. **`STATE.md` is deliberately untouched:** measured
at `mg-3e5e` it stood at exactly its ceiling, 5199 of 5199 words, so even a one-line pointer cost a
ceiling raise and this ticket forbids spending that budget (re-run
`code/state_ratchet_e331/ratchet.py` rather than trusting that figure; if a later ticket raises the
ceiling anyway, a `STATE.md` pointer is the cheapest thing to add alongside it). **Not
[`FACTS.md`](FACTS.md):** that registry admits **homeless** facts and these four are the opposite —
what everything else is built on — so they fail its admission test (2); and its gate checks the
entry count against `STATE.md`'s pointer paragraph, so four entries there would force the `STATE.md`
edit just declined. **Facts only** — no strategy, no open directions, no account of what is walled.
The archive carries that, and the complaint this file answers is that the archive is reached for
**first**.
