# OneThird — (LIB-weak): what it is, what it costs, and where the named obstruction stops

**Work item:** `mg-c3ca`. **Method:** reading + hand argument + one small exact census
(`code/libweak_c3ca/`, all counts exact integer arithmetic, no sampling).
**Ticket premise corrected in §2 and §3.** **What I did not do: §7.**

---

## 0. Verdict, in five lines

1. **(LIB-weak) is not blocked by the obstruction that blocks (B) and LIB.** The arc's fatal
   object — the flat-long block-cross — is a **one-element** configuration. (LIB-weak) is
   untouched until **Θ(n) elements do it simultaneously** (§3, proven). That gap is the answer
   to the ticket's question and it is the reason "never attacked" is an opportunity, not an
   oversight.
2. **But (LIB-weak) does not close the wall as the architecture consumes it** — it closes ledger
   row 8 *as literally written*. The difference is a quantifier over `n`, already recorded at
   STATE.md's own mg-88bd row, and the ticket's framing did not carry it (§2).
3. **(LIB-weak) and (LIB-const) differ IN KIND, not in constant** — and the ticket's strength
   ordering is inverted: as asymptotic classes `(LIB) ⊊ (LIB-weak) ⊊ (LIB-const)` (§2.3).
4. **Price, proven here:** (LIB-weak) ⟹ the counterexample's entropy deficit `log(n!/e(P))` is
   `ω(n)`. Elementary, and **discharged** (not an obstruction) under a width statement (§4).
5. **A forward vector, with its own probe run against it, and the probe fired** (§5–6). The
   marginal form of the last step is **false** — 8 088 exhibited counter-pairs at `n = 6` — and
   what survives is a threshold form whose threshold is **moving with `n`** in the reachable
   range. Reported as a race between two measurable rates, not as progress.

---

## 1. The statement, with `frozen` spelled out

`P` a finite poset, `n = |P|`, `σ` uniform on `L(P)`. For incomparable `x ∥ y`,
`p(x,y) := Pr[y ≺_σ x]`. `δ(P) := max` over incomparable pairs of `min(p, 1−p)`.

> **frozen** `:⟺ δ(P) < 1/3` — every incomparable pair is `>2/3`-decided. This is the
> minimal-counterexample condition, so **the class is conjecturally empty**; see §7.

`e` (the distinguished order) is not a choice. For any three elements
`Pr[x≺y] + Pr[y≺z] + Pr[z≺x] ≤ 2`, since each of the 6 orders makes at most 2 of the three
cyclic events true; so no three pairwise orientations all exceed `2/3`. Under `δ < 1/3` the
strong-majority relation is a complete tournament with no 3-cycle, hence transitive, hence a
total order. *(This is STATE.md:384's argument; I re-derived it rather than citing it, because
`inv_e` is undefined without it. Not mine — theirs.)*

> **(LIB-weak):** for frozen `P`, `E_σ[inv_e(σ)] = o(n²)`, where `inv_e` counts incomparable
> pairs ordered against `e`.

**Equivalent reformulation (proven here, both directions elementary).** Write
`m_x := Σ_{z≠x} Pr[z on the wrong side of x]` (per-element inversion mass), so
`Σ_x m_x = 2E[inv_e]`. Then

> **(LIB-weak) ⟺ for every `α > 0`, `#{x : m_x ≥ αn} = o(n)`.**

*Proof.* (⟹) Markov: `#{x : m_x ≥ αn} ≤ Σ_x m_x/(αn) = o(n²)/(αn)`. (⟸) Split the sum:
`Σ_x m_x ≤ o(n)·n + αn·n` for every `α`, and `m_x ≤ n`. ∎
Equivalently again: **almost every incomparable pair is asymptotically fully decided** —
for every `ε > 0`, `#{pairs with min(p,1−p) ≥ ε} = o(n²)`.

---

## 2. Does it close L1b? — yes as row 8 is written, no as the architecture consumes it

**2.1 It closes row 8.** Via mg-210d's master bound (merged, audited; I did **not** re-derive it),
`1−λ_std ≤ 6E[inv_e]/(n²−1)`, so `E[inv_e] = o(n²)` gives `1−λ_std = o(1)`, i.e. `λ_std → 1`.
STATE.md's claim is **correct as stated**. Arithmetic only.

**2.2 Row 8 is not what the architecture consumes — and STATE.md already says so.**
mg-88bd (`docs/OneThird-lambda-std-Operative-Form.md` §5, merged, audited mg-e35c) derives the
operative form backwards from L4: `1−λ_std ≤ ε_spec` for an **absolute constant uniform in `n`**,
explicitly *not* the limit. A limit hypothesis supplies the threshold only for `n ≥ N₀` with `N₀`
**unspecified**, and the minimal-counterexample argument needs the contradiction *at the actual
`n`*, with a verified base case below it. So:

> **(LIB-weak) closes the wall as row 8 phrases it, and leaves the wall the architecture
> actually needs open by exactly one quantifier.** This is not new mathematics — it is mg-88bd's
> result, applied to the ticket's premise, which did not carry it. The ticket's
> "(LIB-weak) … closes the wall" is the claim that needs the rider.

**2.3 (LIB-weak) vs (LIB-const): different in KIND.** The ticket asks. Four points:

- As asymptotic classes, mg-88bd §6.2: `(LIB) O(n) ⊊ (LIB-weak) o(n²) ⊊ (LIB-const) ≤ cn²`.
  **(LIB-weak) is the STRONGER of the two**, not the weaker — the ticket's ordering is inverted.
- Neither implies the other *outright*: `o(n²)` gives a constant threshold only eventually;
  `(LIB-const)` at the required constant gives it at every `n`. **The difference is the
  quantifier over `n`, not a constant.**
- `(LIB-const)` is meaningless without its constant attached: mg-88bd Claim 6.1 shows freezing
  **already** delivers `E[inv_e] < m/3`, i.e. `(LIB-const)` with constant `2/3`, unconditionally
  — while the consumer wants ~~`ε_spec ≈ 2×10⁻⁴`~~ **`ε_spec ≈ 2×10⁻²`**. A factor of
  ~~`~5×10³`~~ **`~50`**, with no `n` in it. **[SUPERSEDED INPUT REPAIRED — mg-e35c F5, landed
  mg-5827: the budget was calibrated under a branch-(iii) reading its own source document proves
  broken; the repaired figure is 100× larger and the stale one inflated the gap 100×.]**
- Numerically the "weaker" form is **stronger**: mg-88bd §7.4 — the required constant makes
  `(LIB-const)` harder than LIB at every `n` below ~~`~10⁵`~~ **`~900`** (same repair). **(LIB-weak) is constant-free and is
  the only one of the three that is not hostage to `ε_spec`.**

---

## 3. THE FINDING — the named obstruction is one-element-scale, and (LIB-weak) is n-element-scale

The arc's fatal object is the **block-cross** (`one_third_width_three/docs/
OneThird-L1b-Bwall-state.md` §4): an element `x` versus a length-`p` chain `C` with slot law
`a ≈ [1−c, 0, …, 0, c]` — before the whole chain w.p. `1−c`, after all of it w.p. `c < 1/3`.
It is frozen, and `E[S_C²]/E|S_C| = p`. mg-a1ec §6.2 shows the three exclusions of the two-atom
law (uniformity, support diameter, AF interior-zero) are **provably vacuous** on it: it has full
support, is uniform, has no interior zero. That is the obstruction, and it is real.

**Its scale is one element.** Re-derived here from `Σ_x m_x = 2E[inv_e]`:

| statement | what it takes to violate it |
|---|---|
| **(B)** (`Σ_x a_x² = O(Σ_x a_x)`, mg-a1ec Prop. 5.3) | **ONE** block-crosser of a `Θ(n)` chain suffices: `E[S²]/E|S| = p = Θ(n)` |
| **(LIB)** `E[inv_e] = O(n)` | survives `O(1)` crossers (`k` of them give only `Σ_x m_x = Ω(kn)`); needs `ω(1)` crossers, or `ω(1)` average mass spread diffusely |
| **(LIB-weak)** `E[inv_e] = o(n²)` | **`Θ(n)` elements of macroscopic mass, and nothing less** — this one is an **iff**, §1: `#{x : m_x ≥ αn} = Ω(n)` for some `α > 0` |

The corpus states the same scale in its own coordinate and I am quoting it, not deriving it
twice: mg-a1ec §4 — `log e(P)` is carried "by `Θ(n)` elements of `O(1)` mobility
(near-ordinal-sum, (B) TRUE) or by **`O(1)` elements of `Θ(n)` mobility** (flat-long block-cross,
(B) FALSE)"; and Bwall-state §4 — the (B) residual is "no `ω(1)`-sized family of elements each
block-crossing a `Θ(n)` chain".

> **Verdict on the ticket's question. (LIB-weak) is NOT blocked by the arc's named obstruction.**
> The obstruction lives at `O(1)` crossers. (LIB-weak) does not notice a configuration until
> `Θ(n)` of them occur *simultaneously* — a hypothesis a factor `n` stronger than anything the
> obstruction supplies. The corpus's own evidence points the other way at that scale: width-3
> caps simultaneous deep crossings at boundedly many per shared chain (Bwall §4), and mg-a1ec
> Prop. 5.3 says (B) fails only via a **few** elements with `a_x` growing.

**Sanity check that this is not word-play:** STATE.md:102's own separator `W_m = C_m ⊔ C_1` — the
canonical one-element-of-`Θ(n)`-mobility witness, on which (B) fails by `Θ(n)` — has
`E[inv_e] = Σ_i min(i, m+1−i)/(m+1) = Θ(n)`, i.e. it satisfies **LIB**, let alone (LIB-weak).
Verified exactly at `m = 4, 6, 8` against the hand formula (`selftest_c3ca.py` §E).

*(Lineage correction, no consequence: STATE.md:102's parenthetical says `W_m` has `δ = 1/2`.
Exactly, `δ(W_m) = ⌊(m+1)/2⌋/(m+1)`, which is `1/2` only for odd `m` — `2/5, 3/7, 4/9` at
`m = 4, 6, 8`. The audit's point stands unchanged: `δ ≥ 2/5 ≫ 1/3` either way, so `W_m`
separates the two quantities and not the two frozen-conditional statements.)*

---

## 4. The price of (LIB-weak), proven — and its discharge

> **Prop. 4.1 (entropy price).** If `E[inv_e] ≤ εn²` then `e(P) ≤ 2·C(2εn²+n, n)`, hence
> `e(P)/n! ≤ 2(2e²ε + e²/n)^n`. Contrapositive: **`e(P) ≥ n!·γⁿ` for fixed `γ>0` ⟹ (LIB-weak)
> FAILS.** So **(LIB-weak) ⟹ `log(n!/e(P)) = ω(n)`.**

*Proof.* Markov: at least half of `L(P)` has `inv_e ≤ 2E[inv_e] =: K`. Permutations with
`inv ≤ K` are injectively coded by inversion tables `(c_1,…,c_n)`, `c_i ≤ i−1`, `Σc_i ≤ K`, of
which there are at most `C(K+n, n)`. Then `n! ≥ (n/e)^n` and `C(a,n) ≤ (ea/n)^n`. ∎

**This is a necessary condition, not a proof route** (the converse direction is exactly what the
two-atom law breaks). Its value is that it is **discharged**: by Dilworth, a width-`w` poset has
`e(P) ≤ n!/Π nᵢ!`, so `log(n!/e(P)) ≥ n·log(n/w)`, which is `ω(n)` as soon as `w = o(n)`. Given
the large-width result cited in mg-a1ec §7 (width `Ω(n)` ⟹ `δ → 1/2`, so frozen ⟹ `w = o(n)`),
the entropy budget **permits** (LIB-weak). **CONDITIONAL** — I did not read Aires–Kahn, and
STATE.md:123 records a misattribution against a *neighbouring* claim of that same paper (the
`O(log n)`-minimals one), so this citation needs checking before it is leaned on.

---

## 5. Forward vector — and the probe I built to kill it

By §3, a (LIB-weak) violation needs `Θ(n)` elements with mobility windows of length `Θ(n)`
(mg-a1ec Prop. 4.1: `pos_σ(x) | τ ~ Uniform(I_x(τ))`). Then:

1. **Pigeonhole (not in doubt).** `αn` windows of length `≥ αn` inside `[n]`: two have left
   endpoints within `1/α`, so their symmetric difference is `O(1/α)` against length `αn` —
   **two of the crossers have near-identical windows**, with TV gap `O(1/(α²n))`.
2. **Micro-lemma (the whole content).** Two *incomparable* elements with near-identical position
   laws should be near-balanced — contradicting frozen, hence proving (LIB-weak).

Step 2 is where this stands or falls, and it is **different in mechanism** from the
Kahn–Saks/BFT selection step, which the corpus has already shown freezing cannot improve
(`entropy-probe-frozen-constraint.md` §4): that argument picks a pair by an expected-**height**
pigeonhole and feeds a fixed local optimization capped at `0.2764`. This one does not select a
pair out of an arbitrary poset — it consumes the very strong extra hypothesis that `Θ(n)`
elements are macroscopically mobile. **That extra hypothesis is what makes (LIB-weak)
potentially easier than the conjecture**, and it is exactly what the contrapositive hands you
for free.

**P3 tested step 2 in its marginal form and the probe fired on me.**
Population: all naturally labelled non-chain posets `n ≤ 6`; grain: one incomparable pair.

- The linear form `min(p,1−p) ≥ (1/3)(1−TV)` is **FALSE**: 8 088 counter-pairs at `n = 6`
  (worst `1−TV = 0.5` with `min(p,1−p) = 0.212`), 351 at `n = 5`, 16 at `n = 4`.
- What survives is a **threshold** form, and the data supports it in the regime the pigeonhole
  delivers: the floor of `min(p,1−p)` rises with similarity — `0.316` at `1−TV ≥ 0.7`,
  `0.450` at `≥ 0.9`, `0.500` at `≥ 0.99` (`n = 6`).
- **But the threshold moves with `n`.** `s*(n) := sup{1−TV : the pair is NOT balanced}` is
  `—, 0.500, 0.636, 0.737` at `n = 3,4,5,6`. If `1−s*(n)` keeps shrinking at least as fast as
  the pigeonhole's own `O(1/(α²n))` margin, step 2 **fails asymptotically at a fixed constant**
  and the vector dies. Three points cannot tell those two rates apart.

> **Honest status of the vector: undecided, and now measurable.** It is a race between
> `1−s*(n)` and the pigeonhole margin. Both are computable. The next step is *not* more prose:
> it is (i) `s*(n)` at `n = 7, 8` on the primitive population, and (ii) the **conditional**
> form of step 2 on `I_x(τ)` rather than the marginal law — mg-a1ec Prop. 4.1 is stated for one
> element, and a two-element version is the missing lemma.

---

## 6. What the reachable data says about (LIB-weak) itself

Population: every naturally labelled poset on `n ≤ 6` (each iso class once per compatible
labelling); grain: one such poset. `E_maj := Σ min(p,1−p)`, which **is** `E[inv_e]` when the
majority order is linear and is a lower bound on `E[inv_r]` for every reference order otherwise.

- **Positive control.** `min δ = 1/3` exactly at every `n = 3..6`; **0 frozen posets found**, as
  the conjecture requires. The instrument is nonetheless shown able to report `δ < 1/3`
  (`selftest` §F).
- **The critical family (`δ = 1/3`) is decomposable**, hence excluded — minimal counterexamples
  are primitive (STATE.md rows 1–2). On the **primitive** population `min δ` is strictly above
  `1/3`: `0.400, 0.364, 0.357` at `n = 4,5,6`. *(That `0.357` coincides with the lowest `δ` ever
  seen for a block-cross, mg-dbd1's `0.357`; different populations, and I make no claim that it
  is the same fact.)*
- **Near-frozen posets are inversion-light.** Max `E_maj` over the primitive critical family:
  `0.67, 1.00, 1.55, 1.64` at `n = 3..6` — growing like `Θ(n)`, i.e. LIB-scale, with
  `E_maj/n²` falling `0.074 → 0.046`. The `δ = 1/3` ordinal-sum family
  (`k` V-gadgets, `n = 3k`) has `E_maj = (2/9)n` **exactly** at every `k` — the boundary of the
  frozen class satisfies LIB, not merely (LIB-weak).
- **No discontinuity at `δ = 1/3` is visible in `E[inv_e]`.** Whatever mechanism is discontinuous
  there (mg-a1ec's balance spectrum), the inversion functional is not the one that jumps.

**Reach caveat, stated plainly:** `n ≤ 6` cannot see a `Θ(n)`-mobility configuration at all, so
this data is silent on the actual threat and is evidence about the boundary only.

---

## 7. What I did not do

- **I did not prove (LIB-weak).** §5 is a sketch with its own refutation-probe attached.
- **I did not re-derive** the mg-210d master bound, mg-88bd's backward derivation, Theorem E,
  the Cheeger sandwich, or Theorem G. Read, cited, not retested.
- **I did not read** Aires–Kahn 2509.11549 or Ma–Shenfeld 2211.14252. §4's discharge is
  CONDITIONAL on the first; mg-a1ec's AF-equality lever depends on the second and I confirmed
  only that it is *not* touched by anything in §3.
- **I did not settle the STATE.md ⇄ mg-a1ec disagreement** over the Aires–Kahn attribution.
- **I did not attack Q1 of the original ticket** (superseded mid-session by the mayor). One
  observation I had already made before the stop, offered as a pointer and not as a finding:
  the tex's Cheeger sandwich (`:317–324`) is introduced as *"the usual Cheeger inequalities
  give…"*, and Step 4 consumes its **lower** half, while ledger row 5 records only the easy/Buser
  **upper** half as proven. Whether the lower half is proven for `S_P` specifically is a
  question I did not pursue and it may well be settled elsewhere.
- **Everything empirical here is `n ≤ 6`.** No claim in §6 is asymptotic.

---

## 8. Strategy — is this an alternative or a complement?

**A complement, and a cheap one.** mg-344a's live direction (bespoke finite/rigid combinatorics
on the quotient-to-chain frame) and (LIB-weak) attack the **same** open implication L1b, but from
opposite ends: the live direction works at fixed structure, (LIB-weak) is a purely asymptotic,
constant-free statement whose contrapositive hands you a `Θ(n)`-scale hypothesis to work with.
Two independent attacks on one open implication is a good position and should be recorded as
one — but §2.2 is the rider that has to travel with it: **on its own (LIB-weak) closes row 8,
not the wall**, and a route to the wall still needs the uniformity that only a constant-threshold
statement supplies.

**Correction to the ticket's framing, as requested.** The ticket says "L1b IS THE WHOLE REMAINING
GAP" and "the Cheeger chain is PROVEN end to end except this one implication". STATE.md's own
ledger says two links are open — **L1b primary and L4 secondary (AMBER)** — plus row 3b
(standard dominance) is *empirical* (0/132, `n ≤ 7`) and L3 best-cut-is-a-prefix is *empirical*
(125/126, `n ≤ 6`). Closing L1b alone does not close the chain.
