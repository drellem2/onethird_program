# mg-c4f5 — PRE-REGISTERED PREDICTIONS

**INDEPENDENT AUDIT of mg-c3ca** (`docs/OneThird-LIBweak-mg-c3ca.md`, commit `81214a9`).

**Committed BEFORE any script of this audit exists.** Nothing below is amended after the fact.
Anything I had already established by hand or by reading at the time of writing is filed under
**DISCLOSURES** and is explicitly *not* a prediction — I will not be credited for it.

---

## DISCLOSURES — what I had already measured before writing this file

These are measurements, not predictions. They were taken by reading merged text and by hand
derivation, before any code of this audit existed.

**D1. I re-derived mg-210d's master bound by hand, in full, from
`/Users/daniel/research/one_third_width_three/docs/probe-lambda-constant-bound.md` §§1–2.**
Lemma 1.1 (Buser, Rayleigh on `f = 1_A − a·1`), Lemma 2.1 (`Σ_k leak_k = E[F]/2`), Lemma 2.2
(`E[F] ≤ 2E[inv]`, the DG upper half derived from scratch), Lemma 2.3 (`Σ_k k(n−k)/n = (n²−1)/6`),
Theorem 2.4 (mediant). **Every step checks.** The bound is unconditional: it needs only that `L`
is a linear extension of `P` and `σ` uniform on `L(P)`. So the arithmetic of the parent's §2.1 —
`E[inv_e] = o(n²) ⟹ 1−λ_std = o(1)` — is sound at the level I can verify by hand.

**D2. The master bound's `λ_std` is defined relative to a chosen reference linear extension `L`**
(the source says so at `:56–62`: the relabelling "is the only place a choice enters"). STATE.md's
glossary line 40 defines `λ_std` as "top eigenvalue of the symmetrized transport operator on `1⊥`"
with **no mention of `L`**. I have not yet checked whether the value actually moves with `L`.

**D3. `ε_spec` in the parent doc is the SUPERSEDED calibration, and STATE.md said so in bold at
the time the parent ran.** `docs/OneThird-lambda-std-Operative-Form-IndependentAudit.md` (mg-e35c,
merged 2026-07-29 `3710d28`) F5 replaces `ε_spec ≲ 2×10⁻⁴` with `ε_spec ≲ 2×10⁻²` (100× larger),
crossover `10⁵ → n ≈ 900`. STATE.md at `81214a9^` (i.e. as it stood when mg-c3ca was written)
carries, in bold: *"do not carry `2×10⁻⁴` or the `n ≈ 10⁵` crossover as flat text"*. The parent's
§2.3 carries `2×10⁻⁴`, `~5×10³` and `~10⁵` as flat text, citing mg-88bd §7.4.

**D4. STATE.md row 8 self-contradicts in one sentence, LIVE at HEAD.** Row 8 now *leads with* the
constant form (`1 − λ_std ≤ ε_spec`, a constant uniform in `n`) and then says (LIB-weak) "closes
**this row as phrased**" and two clauses later "does *not* supply the constant form this row leads
with". Before `f85a4e8` (mg-2860) row 8 was phrased `frozen ⟹ λ_std→1`, for which "as phrased"
was correct; mg-2860 rewrote the row's lead and introduced the "as phrased" clause in the same
commit. The one-paragraph state has the same shape ("closes **row 8 as phrased**, not the form
above").

**D5. The premise's second half has a named origin.** *"`λ_std → 1` as stated here needs only
(LIB-weak) `E[inv_e] = o(n²)` — never attacked by any arc"* is mg-a58f's sentence, in the mg-a58f
ledger row, audited mg-d112 ("CONFIRMED, 40 ledger rows re-derived, 0 BROKEN"). I have **not** yet
checked whether mg-d112 audited the *"never attacked"* half or only the mathematical half.

**D6. mg-88bd Claim 6.1 is `E[inv_e] < m/3` under freezing**, i.e. `< (2/3)·E_unif[inv]`, i.e.
`ε_spec < n/(n+1) → 1` through the master bound. I read this; I have not re-derived it numerically.

**D7. I have read the parent doc in full, the parent's README, STATE.md at HEAD and at `81214a9^`,
mg-88bd §§0–7.4 in part, and the mg-e35c audit in part. I have not yet run any code of my own.**

---

## THE PREDICTIONS

### A. The premise (audit target 1) — the whole audit

**P1. The premise HOLDS on its mathematical half, and my headline will NOT be "the parent's
deliverable is misaimed".** Specifically: over every naturally labelled poset on `n ≤ 7`, taking
`L` = the natural labelling, the master bound `1 − λ_std ≤ 6·E[inv_L]/(n²−1)` will hold with
**0 violations**, and the footrule form `1 − λ_std ≤ 3·E[F]/(n²−1)` will hold with **0 violations**.
Equality in the footrule form will occur at the antichain and **nowhere else** except degenerate
`n ≤ 2`.
*If this is refuted the headline flips and the parent's whole target is wrong.*

**P2. `λ_std` genuinely DEPENDS on the choice of reference linear extension `L`, and I will exhibit
a witness at `n ≤ 6`** — a poset with two linear extensions giving `λ_std` differing by `> 10⁻⁶`.
Consequence if true: STATE.md's glossary definition of `λ_std` (line 40) is **under-specified at
the site of the wall's own statement**, and row 8's "frozen ⟹ `λ_std → 1`" is only well-posed
because freezing makes `e` canonical — a hypothesis the row does not name. I predict the parent
doc does **not** state this either (0 sites).

**P3. The premise's SECOND half — "never attacked by any arc" — is the weaker of the two and I
predict it survives, but only as a claim about `mg` items and not about mathematics.** Concretely:
searching every `mg` item and every merged doc for a substantive engagement with `E[inv_e] = o(n²)`
*as a target* prior to `81214a9`, I predict **0** items whose deliverable was an attack on it, and
**≥ 3** items that state or restate it without attacking it. I also predict mg-d112 did **not**
separately audit the "never attacked" half (0 mentions of it in the audit doc).

### B. The parent's mathematics, re-derived rather than read (audit target 2)

**P4. The §1 iff is CORRECT and I will confirm it numerically with 0 violations**, but its
statement is loose in one respect I predict I can name: the negation of *"for every `α>0`,
`#{x : m_x ≥ αn} = o(n)`"* is *not* `Ω(n)` for some `α` (as the §3 table writes it) but "not
`o(n)`", i.e. a limsup statement along a subsequence. **Predicted verdict: substance CONFIRMED,
one quantifier written too strongly in the §3 table. Consequence-free.**

**P5. Prop. 4.1 (entropy price) is CORRECT.** `e(P) ≤ 2·C(2E[inv_L]+n, n)` will hold with
**0 violations** over all naturally labelled posets `n ≤ 7`. I predict the bound is **extremely
loose** at this size — median ratio `2C(...)/e(P) > 10³` at `n = 7` — so the numerical check is a
consistency check and not a sharpness check, and I will say so.

**P6. Prop. 4.1's proof has one unstated step that is nevertheless TRUE, and I will state it:**
the inversion-table coding counts inversions of `σ` against `e` *over all pairs*, while `inv_e`
counts only *incomparable* pairs. These coincide **only because `e` is a linear extension** — which
under freezing it is (STATE.md:384's 3-cycle argument), but the proof as written does not say so.
Predicted: the gap is real as an exposition defect, **0 consequence for the result**.

**P7. §4's discharge is the parent's own CONDITIONAL and I will not resolve it** — I do not have
Aires–Kahn and will not read it. I predict the parent's flag is adequate and that STATE.md's
recorded misattribution is against a *different* claim of the same paper (already recorded), so
the flag is correctly aimed. **Predicted: no new finding here.**

### C. The negative, and building what it forbids (audit target 3)

The parent's negative is *"(LIB-weak) is NOT blocked by the arc's named obstruction"* — a negative
about a **blocker**, so the object to construct is the thing the parent says the obstruction cannot
supply: **`Θ(n)` elements of `Θ(n)` inversion mass, simultaneously.**

**P8. THE CONSTRUCTION SUCCEEDS AS A POSET AND FAILS AS A COUNTEREXAMPLE, and that asymmetry is
the finding.** `P = C_p ⊔ A_q` (a `p`-chain disjoint from a `q`-antichain), `p = q = n/2`, has
`Θ(n)` elements each of `Θ(n)` mass and `E[inv_e] = Θ(n²)`. I predict I can verify
`E[inv]/n² ≥ 0.05` exactly at `n = 6, 8, 10`, and `δ = 1/2` exactly. So the configuration the
parent says the obstruction cannot reach **exists in the poset world**; everything stopping it is
`frozen`, not scale.

**P9. The parent's supporting evidence for its negative is WEAKER THAN THE NEGATIVE, at two named
sites, and this is my predicted second-largest finding.**
 (a) *"width-3 caps simultaneous deep crossings at boundedly many per shared chain (Bwall §4)"* —
 I predict this is stated in a **width-3** source, that STATE.md's own header declares width-3
 "old-repo baggage, not part of this program", and that the parent transfers it to an any-width
 claim **with no label**. I further predict `C_p ⊔ A_q` violates the cap as literally transferred.
 (b) *"mg-a1ec Prop. 5.3 says (B) fails only via a **few** elements with `a_x` growing"* — I
 predict this is a statement about the **known/cheapest** violators of a **different and strictly
 stronger** statement, and carries no information about whether `Θ(n)`-scale frozen configurations
 exist. Using it as evidence is the search-instrument fallacy this arc names.
 **Predicted net: the parent's §3 verdict ("not blocked") SURVIVES — it is a statement about
 transfer of an obstruction, and the transfer genuinely fails — but the sentence "the corpus's own
 evidence points the other way at that scale" is UNEARNED and should be struck.**

**P10. I will NOT be able to construct a frozen poset, and I predict 0 frozen posets at `n ≤ 7`**
(the conjecture requires this). I predict the minimum `δ` over **primitive** posets continues to
fall at `n = 7`: strictly below the parent's `0.357` and strictly above `1/3`. I put the interval
at `(0.333, 0.357)` and predict a value in `[0.340, 0.353]`.

**P11. The parent's "near-frozen primitive posets are inversion-LIGHT — `Θ(n)`-shaped" is a
4-point read that I predict does NOT survive a 5th point.** Its `0.67, 1.00, 1.55, 1.64` at
`n = 3..6` has successive ratios `1.49, 1.55, 1.06`. I predict the `n = 7` value will miss a
least-squares linear fit through the four published points by **> 15%**, so "`Θ(n)`-shaped" is not
supported by the data it is drawn from. (I predict the *conclusion* — near-frozen primitives are
inversion-light at reachable `n` — nevertheless holds.)

### D. (LIB-weak) vs (LIB-const) (audit target 4)

**P12. The parent's headline on this — "they differ IN KIND; the gap is a QUANTIFIER, not a
constant" — is CORRECT about the pair it names and is being MISREAD downstream.** I predict I will
find that mayor's relayed framing ("the residual the architecture consumes is a CONSTANT (~50)
rather than a quantifier") sets two *different* gaps in opposition:
 - gap 1: (LIB-weak) `⟹` (LIB-const) only for `n ≥ N₀` — a **quantifier** (the parent's claim);
 - gap 2: what freezing gives for free (`ε_spec ≈ 1`) vs. what the architecture needs
   (`ε_spec ≲ 2×10⁻²`) — a **constant factor** (mg-88bd/mg-e35c's claim).
 **Both are true and they are not competitors.** Predicted: the "rather than" is the error, not
 either number.

**P13. The `~50` is RIGHT and the parent's `~5×10³` is STALE BY 100×.** I predict I will confirm
`(2/3) / ((2/3)·2×10⁻²) = 50` exactly, i.e. the repaired factor is `1/ε_spec = 50`, and that the
parent's doc contains **exactly 3** superseded-calibration figures (`2×10⁻⁴`, `5×10³`, `10⁵`),
each carried as flat text against STATE.md's explicit bold instruction not to. This is a
**CORRECTION TO A MERGED DOCUMENT** and it inflates pessimism by two orders of magnitude.

**P14. The class chain `(LIB) ⊊ (LIB-weak) ⊊ (LIB-const)` is FALSE as a statement about the
posets satisfying the three conditions**, and true only as a statement about growth-rate classes
with `(LIB-const)` read as `O(n²)` rather than as `≤ c n²` at its required `c`. I predict the
parent's §2.3 states it in bullet 1 **without a rider at the site**, and that bullet 2 supplies the
rider — so this is the exact defect mg-325c repaired in STATE.md at four sites, surviving in the
parent doc, **mitigated by adjacency**. Predicted severity: MINOR, 1 site.

### E. Delta_AT drift (audit target 5)

**P15. NO DRIFT. I predict the parent did not touch `Δ_AT`.** Concretely: **0** live uses of
`Δ_AT` / Hodge / Theorem G in the parent doc, with mentions confined to §7 ("what I did not do").
I predict `≤ 2` total occurrences of the Hodge axis in the whole document. *(I am filing the
prediction that a target does NOT fire, because a target that never fires and is never reported
is indistinguishable from a target never checked.)*

### F. Standing targets, and this instrument

**P16. Every printed count in the parent doc moves or is FORCED.** I predict `≥ 1` printed count
in the parent doc is **not reproducible as printed** — my first guess is a count in §5 (`8 088`,
`351`, `16`) or §6 (`0.400, 0.364, 0.357` / `0.67, 1.00, 1.55, 1.64`), because those are the ones
whose population definition ("critical family", "primitive") admits more than one reading. I
predict **≥ 9 of 11** reproduce exactly.

**P17. Bound words.** I predict the parent's own bound words are, unusually for this arc, MOSTLY
EARNED — it is a document whose headline is a correction to its own ticket. I predict `≤ 2`
unearned uses of {"closes", "cannot", "suffices", "strictly", "never"}, and I predict the one that
fails is **"never attacked by any arc"** carried forward as the parent's own assertion rather than
as a quotation of STATE.md.

**P18. THIS AUDIT'S OWN INSTRUMENT WILL HAVE ≥ 3 DEFECTS and I will record them.** I predict at
least one is a check that **passes vacuously** — that is this arc's signature shape and it has
landed inside the auditor's own file in at least three recent tickets.

**P19. I predict I will NOT re-derive:** Theorem E, Theorem G, the Cheeger sandwich, mg-88bd's
backward derivation from L4, mg-3ce3's envelope, or anything about L4/`ε_leak`. I will not read
Aires–Kahn or Ma–Shenfeld. I will say so in §"what I did not do" rather than let silence imply
coverage.

**P20. My own most likely error, filed in advance:** that I read the parent's §3 verdict as a
claim about **existence** when it is a claim about **transfer**, and refute a sentence the parent
did not write. The parent says the obstruction does not *block*; it does not say a `Θ(n)`-scale
frozen configuration does not exist. If I find myself writing "the parent claims no such object
exists", I have made this error.

---

*Written by `uc4f5` for `mg-c4f5`, before any script of this audit existed.*
