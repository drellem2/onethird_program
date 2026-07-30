# Independent audit of mg-24a3 / f5d3485

*`docs/OneThird-Counterexample-Under-The-Action.md` and `code/counterexample_probe_24a3/`.
Audit work item mg-a7b4, pre-filed. Everything numerical here is produced by
`code/counterexample_audit_a7b4/`, which shares **no code** with the target's instrument and
rebuilds every object from its definition in exact rational arithmetic. Regenerate with
`code/counterexample_audit_a7b4/run_all.sh`.*

---

## VERDICT: OVERSTATED — 1 BROKEN, 1 UNDERSTATED, 1 UNDER-EVIDENCED NEGATIVE

**The mathematics is sound.** All seven results the document nominates as *proved* — Theorem 1,
Propositions 2, 5 and 6, Theorems 3, 4 and 7 — are correct as theorems, and I reproduced every
computation supporting them from an independent instrument. The conditionality discipline the
brief demanded is maintained throughout: I found no sentence asserting a property of a
counterexample as a fact. The deliverable's two headline answers — the bridge object is a
theorem, and the concentration quantity is not a filter — both stand, exactly as stated, with
every figure confirmed.

**The one BROKEN item is a universal quantifier in section 4**, and it is the arc's signature
defect in its purest form: correct arithmetic on nine printed rows, generalised to a sentence
about sixteen posets, where the seven rows that were never printed say the opposite. The
correction runs **against** the document's own verdict — a separation survives the `e(P)`
control that the document reports as dissolved.

| | |
|---|---|
| **BROKEN** | §4 (and §0 headline 3, §8 item 3): *"Every extremal poset is rank 1 — and **tied with every other member of their group**"*; *"within a fixed `e(P)` the statistic does not distinguish the extremal posets from anything at all — not weakly, but by an exact tie"*; *"entirely accounted for by the linear-extension count"*. **False.** 4 of the 16 extremal posets are not tied with every member of their group, and in the only control group that contains a contrast the statistic separates **perfectly**. |
| **UNDERSTATED** | Theorem 4 (`λ₂ = max_{x∥y} s(x,y)`) is stated for the uniform-move weight. Its proof uses only weight-independent facts and it holds for **every** weight — including the `w_t` family of the document's own Theorem 7. Verified on 405 (poset, weight) cases, 0 failures. |
| **UNDER-EVIDENCED NEGATIVE** | §2's *"no cycle in 4200 random posets at each of `n` = 8, 9, 10"* rests on a search that **is not in the committed instrument**, is not reproducible by `run_all.sh`, and is false at `n = 9`: I exhibit a witness. The document's own `n = 11` witness contains an isolated element, so it is an `n = 10` witness already. |

Everything else reproduced. Nothing in the deliverable's mathematics is wrong.

---

## TARGET ZERO — what was added beyond the brief

Enumerated first, as the standing rule requires. The brief (mg-24a3 + its addendum + Daniel's
correction) asked for: (a) a separation test with a null model; (b) necessary conditions;
the bridge object `L*` and the bound `E[inv] < |Inc|/3`; the quotient-side test; the
isoperimetric question written as a question; and the transitivity theorem stated as a result.

Material in the deliverable that is **not** traceable to those asks:

1. **§2's general-poset majority-cycle apparatus** — the exhaustive `n ≤ 7` cycle sweep, the
   random searches at `n = 8, 9, 10`, and the `n = 11` witness with its three exact margins.
   The brief's correction said *"do not spend any effort on the cyclic branch."* This is not
   the cyclic branch of a counterexample; it is an independent demonstration that the general
   obstruction is real, used to justify the correction. **Per Daniel's instruction I do not
   score its existence as a defect of the author's** — but it is beyond-brief material and it
   is where the under-evidenced negative lives (finding 3 below). Its positive content — the
   `n = 11` witness — reproduces **exactly**: `e(P) = 78474`, `p(5,9) = 597/1189`,
   `p(9,6) = 599/1189`, `p(6,5) = 1784/3567`, 3-cycle `5 → 9 → 6 → 5`.
2. **§5.5's Theorem 7 (no free lunch) and the exact `q`-reformulation.** Not asked for. The
   theorem is correct and I verified it on the actual transition matrix (95 (poset, `t`) cases,
   exact rationals, 0 failures). Its *consequence sentence* over-reaches — minor item 2.
3. **§6's collision-witness open question.** Arises naturally from the sweep, correctly left
   open, and — see the confirmations — it holds on **wider** populations than the document
   claims.

**So for the second time in this arc the worst finding is not in the beyond-brief material.**
The BROKEN item is in §4, which the addendum explicitly commissioned. I record that plainly
rather than manufacturing a beyond-brief finding to fit the pattern.

---

## 1. BROKEN — section 4's universal, and the separation it hides

### What the document says

> *Controlling for `e(P)`.* Compare each extremal poset only against tie-free posets with the
> **same** linear-extension count. Every extremal poset is rank 1 — and **tied with every other
> member of their group**: rank 1 of 3 tied with 2 at `n = 5`, rank 1 of 4 tied with 3 at
> `n = 6`, rank 1 of 5 tied with 4 at `n = 7`.
>
> **Verdict on the quotient side: NULL, quantified.** … Within a fixed `e(P)` the statistic does
> not distinguish the extremal posets from anything at all — **not weakly, but by an exact tie**.

### What is true

There are 16 `δ`-extremal posets in the population (3 at `n = 5`, 5 at `n = 6`, 8 at `n = 7`).
Checked on **all** of them, with no cap and no minimum group size:

- **rank 1: 16 of 16.** That half of the sentence is correct (and trivially so — extremal
  posets have `qmass = 1`, which is the maximum).
- **tied with every other member of their group: 12 of 16.** The four exceptions are the
  extremal posets with `e(P) = 9`: one at `n = 6` and three at `n = 7`.

| `n` | `e(P)` group | group size | extremal in it | `qmass = 1` in it | other `qmass` values present |
|---|---|---|---|---|---|
| 5 | 3 | 3 | **3** | 3 | — |
| 6 | 3 | 4 | **4** | 4 | — |
| 6 | **9** | **7** | **1** | **1** | `2/3`, `8/9` |
| 7 | 3 | 5 | **5** | 5 | — |
| 7 | **9** | **13** | **3** | **3** | `2/3`, `8/9` |

At `n = 6` the extremal poset in the `e = 9` group is **strictly above all six other members**.
At `n = 7`, within the `e = 9` group of 13, `qmass = 1` holds for exactly three posets and those
three **are exactly the extremal ones** — a perfect separation inside the control group. Under
the null that puts three marks at random on the 13 members, that has probability
`1/C(13,3) = 1/286 ≈ 0.0035`.

### Why the instrument could not see it

Two compounding causes, both visible in `probe.py`:

1. The reporting loop breaks after **three** printed rows per `n` (`if lines >= 3: break`) and
   skips any `e`-group of size `< 3`. The committed output contains exactly nine rows, three
   per `n`, and **every one of them is an `e = 3` group**. The `e = 9` groups were never
   printed.
2. **The `e = 3` control group is vacuous by construction.** A non-chain poset with `e(P) = 3`
   has `δ = 1/3` *exactly*, for an elementary reason: for an incomparable pair the two augmented
   counts are positive integers summing to 3, hence `{1, 2}`, so `min(p, 1−p) = 1/3` for every
   pair. Therefore **every** member of an `e = 3` group is `δ`-extremal, and "tied with every
   other member of the group" is a tautology with no non-extremal poset in it to compare
   against. (Checked: at `n = 3…7` the non-chain posets with `e = 3` number 1, 2, 3, 4, 5 and
   all have `δ = 1/3`.)

So the control the document ran had **no contrast at all**, and the only groups that do provide
contrast show the opposite of its verdict.

### The corrected statement

> The `qmass` effect is real (`z = +2.64` at `n = 7`, confirmed) and is **mostly** explained by
> `e(P)`: in the `e = 3` groups the comparison is vacuous because every member is extremal.
> In the only `e`-groups that contain both extremal and non-extremal posets — `e = 9` at `n = 6`
> and `n = 7` — the statistic **does** separate, and at `n = 7` it separates perfectly
> (3 of 13, `p ≈ 0.0035`). On the evidence in the commit the quotient side is **not** a
> quantified null; it is an effect measured on a control population too small and too degenerate
> to settle either way.

The document's `check_doc.py` cannot catch this: its entry for these rows checks that the string
`rank 1 of 5 tied with 4` appears in both the prose and the output. It does, and the arithmetic
behind it is right. The defect is entirely in the quantifier.

---

## 2. UNDERSTATED — Theorem 4 holds for every weight, not the uniform one

> **Theorem 4.** For the weight uniform on all `P`-compatible moves and any non-chain `P`,
> `λ₂ = max over incomparable pairs {x,y} of s(x,y)`.

The proof given in §5.2 uses exactly two inputs: that `λ_X` is non-increasing as `X` coarsens,
and the multiplicity `m_X`. **Neither depends on the weight** — `m_X` is a combinatorial
invariant of `P`, and monotonicity of `λ_X` holds for any probability distribution on moves.
Tested on every non-chain poset at `n = 3, 4, 5` with three random rational weights each, plus
the `w_t` family of Theorem 7: **405 (poset, weight) cases, 0 failures.**

This is not pedantry. §5.5's whole point is that a spectral detector must be evaluated on
weights *other* than the uniform-move one, and the `w_t` family is where Theorem 7 does its
work. Under `w_t` the theorem reads `λ₂ = t = max_{x∥y} s_{w_t}(x,y)` — which is exactly the
identity Theorem 7's proof establishes by hand. **The general form is the one the document
needs, it is the form the document proves, and it is stated one weight narrower.** This is the
arc's under-claiming failure mode, and it costs the deliverable a strictly stronger
necessary-condition theorem it already owns.

---

## 3. UNDER-EVIDENCED NEGATIVE — the `n = 8, 9, 10` search

> Found by random search (seed 4242); **no cycle in 4200 random posets at each of `n` = 8, 9,
> 10.** **`n = 11` is not claimed to be minimal** — only that a witness exists, and hence that
> the exhaustive range is too small to see one.

Three separate problems, in increasing order of severity.

**(a) The search is not in the commit.** `probe.py` hard-codes the `n = 11` witness and rebuilds
it; the search that produced it, and the three negative searches, exist nowhere in
`code/counterexample_probe_24a3/`. The only use of `random` in the instrument is the permutation
p-values (`SEED = 20260730`). So `run_all.sh`'s byte-identical reproduction — which I verified,
see below — reproduces the *printing of the sentence*, not the search. `check_doc.py`'s entry
for it (`"4200 random posets"` in the doc ↔ `"4200 random posets"` in the output) is a string
compared against a `print` statement: **a self-verifying assertion**.

**(b) The `n = 11` witness is an `n = 10` witness.** Element 8 appears in none of its cover
relations — it is isolated. Deleting it gives a 10-element poset with `e(P) = 7134` (and
`78474 = 11 × 7134`, the free element inserted into 11 slots), identical pair probabilities, and
the same 3-cycle. So the document's own object refutes the `n = 10` line of its own negative.

**(c) There is a cycle at `n = 9`.** Found by my own random search (density 0.30, 2 hits in 4000
posets — so the phenomenon is roughly one in two thousand at that density, and a 4200-sample
search should be expected to find it):

```
covers  0<5 0<8 1<4 1<6 2<3 2<7 3<6 4<8 5<7        n = 9,  e(P) = 1431,  tie-free
majority 3-cycle  0 -> 2 -> 1 -> 0
    p(0,2) = p(2,1) = p(1,0) = 80/159 = 0.50314    all INSIDE the forbidden band
```

No isolated elements, and no single-element deletion preserves the cycle, so it does not shrink
by the trick that shrinks theirs. **The smallest known majority-cycle witness therefore drops
from 11 to 9.** I did *not* find one at `n = 8` (0 in 30,000 random posets across six densities)
and I did not enumerate `n = 8` exhaustively, so `n = 8` remains open — stated as a limit of my
own search, not as a negative result.

None of this touches Theorem 1 or the methodological point §2 makes, both of which are correct
and neither of which needs the search. **And the document is careful not to claim minimality** —
it says so explicitly, which is to its credit. What it does assert is the search result itself,
with a sample size attached, and a reader takes `4200 × 3` samples as evidence that cycles are
scarce below `n = 11`. That reading is wrong: they exist at `n = 9`, they exist at `n = 10` by
deleting an element of the document's own witness, and the negative that says otherwise cannot
be re-run from the commit. **A negative reported with a number on it is evidence-shaped; this
one is not evidence, because the instrument that produced it is not here.**

---

## 4. Minor items

1. **§0, first sentence.** *"No counterexample … exists at any size this document reaches."* The
   exhaustive range is `n ≤ 7`. At `n = 8…12` the document examines named families and one
   `n = 11` poset only. Read as a statement about *sizes* it claims more than was computed;
   read as a statement about the posets examined it is correct. One clause fixes it.
2. **§5.5's consequence.** *"No spectral quantity of a measure-correct walk can be a function of
   `δ`."* Theorem 7 shows `λ₂` sweeps `[0,1]` on the uniformising polytope while `δ` is fixed;
   that rules out every spectral quantity **that is non-constant along the `w_t` line**, not
   every spectral quantity (a quantity constant on `W_unif(P)` is not excluded by the argument).
   The very next sentence — *"a spectral detector must pin the weight by a rule outside the
   stationarity requirement"* — is the correct statement and does all the work.
3. **§5.1's boxed consequence.** *"Any necessary condition on a counterexample derivable from
   `(Q(P), m)` is a condition on the function `B ↦ e(P|_B)` over convex subsets."* What is
   proved is that `m` is determined by the convex restriction counts **given `Q(P)`**. That
   `Q(P)` is itself a function of that data is not shown, and the box drops it. The downstream
   argument (the frozen condition is about relation extensions, not induced subposets) is
   unaffected.
4. **§6's `n = 3` column.** The trend table is introduced as being *"on the primitive
   non-chains"* and gives `N = 4` at `n = 3`. There are **2** primitive non-chains at `n = 3`;
   `4` is the all-non-chains count. The target's own code silently falls back to the wider
   population when `|prim| < 4` (`group = prim if len(prim) >= 4 else pop`) and prints which it
   used; the deliverable does not carry that caveat. Correct values for the stated population:
   `N = 2`, 100% singleton, 0 non-singleton fibers. Every other column is right.
5. **§6's *"Every trend in this document points the same way."*** The error trend is right
   (max per-pair `δ_walk` error `1/40`, `5/132`, `5/114` at `n = 4,5,6`, and `182/3447` at
   `n = 7` — I extended it). But the **controlled** correlation of `δ_walk` with `δ` *rises* at
   `n = 7`: `ρ|e` goes `0.8703 → 0.8919 → 0.9234` (all non-chains) and `0.849 → 0.894`
   (primitive) from `n = 5,6` to `n = 7`. The document's instrument stops at `n = 6`, so the one
   trend that points the other way was not measured.
6. **§6's cost reason.** *"Computing it requires `e(P|_B)` for every convex `B`, which strictly
   subsumes the `O(2ⁿ·n)` count DP that yields `δ` directly."* The subset DP does **not** yield
   `δ`; `δ` needs the pair counts, a further `|Inc|` DPs or an equivalent. The *conclusion* is
   right and I measured it — on my implementation the `(Q(P), m)` route costs **14.2×** the `δ`
   route at `n = 7` — but the stated reason is not the reason.
7. **§0/§3.3's naming of the extreme case.** *"the posets that satisfy it most strongly are this
   programme's own canonical unfrozen family"* (`C_n ⊔ C_n`, `δ = 1/2`). The genus is right —
   wherever `min R < 1` (i.e. `n = 5, 6, 7`; below that `min R = 1` is attained by many posets)
   the minimiser is a disjoint union of two chains — but it is the **unequal** split in each
   case: `C_3⊔C_2` (`R = 4/5`, `δ = 2/5`), `C_4⊔C_2` (`R = 3/4`, `δ = 2/5`),
   `C_4⊔C_3` (`R = 24/35`, `δ = 3/7`). None of them has `δ = 1/2`, so the
   strongest satisfiers are not the maximally-unfrozen family. The `C_k ⊔ C_k` table is
   nonetheless exact.
8. **Commit message only.** *"`check_doc.py` verifies all 53 figures quoted in the deliverable."*
   It verifies 53 **selected** figures; the deliverable contains 143 distinct numeric tokens.
   And its *"guards against unconditional counterexample claims"* is a blacklist of three
   literal phrases (`the counterexample is`, `counterexamples are frozen and have`, `we have
   shown that no counterexample`), which provides no real coverage. The conditionality
   discipline **is** in fact maintained — I checked it by reading the document — but not because
   of that guard.

---

## 5. What reproduced exactly

My instrument shares no code with the target's and, where a route was available, deliberately
takes a different one (enumeration by adjoining a **minimal** element rather than a maximal one;
`p(x,y) = e(P ∪ {x<y})/e(P)` by a DP on the augmented poset rather than by splitting `L(P)` at
`x`'s placement; DFS three-colouring rather than Kahn for acyclicity; a subset DP rather than a
recursion for topological-sort counts).

**Instrument certification (`selfcheck.py`, all pass).** The enumeration is certified against
**two** external sequences, one of which the target does not use: poset counts
`1, 2, 5, 16, 63, 318, 2045` against **A000112**, and the orbit count
`Σ_classes n!/|Aut| = 1, 3, 19, 219, 4231, 130023, 6129859` against **A001035** (labelled
posets) — an identity that detects over- *and* under-merging of isomorphism classes, which is
the exact failure that produced labelled counts for isomorphism classes earlier in this arc.
Move enumeration is certified against **A000670** (the antichain's moves are the Fubini
numbers `1, 3, 13, 75, 541`). `e(P)` is checked against direct enumeration of `L(P)`;
`p(x,y)` against direct counting; the level description against brute force over all block
orders; and the predicted spectrum against `dim ker(M − λI)` in exact rationals on the actual
transition matrix.

Reproduced from that instrument, all agreeing exactly:

- **§3.1 Proposition 2** — brute-forced on all **398** non-chain posets at `n ≤ 6` by
  enumerating `L(P)` and counting inversions against `L*`: 0 mismatches. Tie-break independence
  checked on the **290** posets with a tied pair, against two differently-constructed
  completions: 0 disagreements.
- **§3.2, every cell** — non-chains `4, 15, 62, 317, 2044`; `min 3δ = 1` at every `n`;
  `min R = 1, 1, 4/5, 3/4, 24/35`; `#R < 1 = 0, 0, 11, 124, 1232`; `60.3%` at `n = 7`;
  `#3δ < 1 = 0` everywhere.
- **§3.3, every cell** — `C_k ⊔ C_k` at `n = 4…12` with `3δ = 3/2` and
  `R = 1, 4/5, 24/35, 64/105, 128/231`; the `1+2`-under-a-chain family with `e = 3`, `3δ = 1`,
  `R = 1` at `n = 3…9`. **Stronger than the document states:** *every one* of the 16
  `δ`-extremal posets at `n = 3…7` has `R = 1` exactly, not just the named family — so
  "they sit exactly on the boundary and never inside it" is true of the whole extremal set.
- **§4's raw table** — tie-free `16, 88, 671`; `#extremal 3, 5, 8`; `qmass` `1.000` vs `0.825 /
  0.734 / 0.593` with `z = +1.16 / +1.95 / +2.64`; `qfrac` `0.642/0.590/0.541` vs
  `0.446/0.316/0.203` with `z = +2.90 / +3.40 / +4.49`; saturation clubs `6 of 16`, `11 of 88`,
  `20 of 671` at `50.0% / 45.5% / 40.0%` extremal. The assertion that all `2ⁿ⁻¹` interval
  partitions of `L*` are levels held for every tie-free poset at `n ≤ 7`.
- **§5.1** — `0` non-convex blocks in **3,246,401** (level, block) pairs; `0` failures of
  "`{B}∪singletons` is a level iff `B` is convex" over **281,977** (poset, nonempty subset)
  pairs.
- **§5.2** — `λ₂ = max s(x,y)`, 0 bad of **2442** non-chains; the supporting fact 0 bad of
  **65,481** all-chain levels; per-pair `ρ = 0.9945` over **2195** pairs with mean error
  `0.00939`; `ρ(δ, δ_walk) = 0.9855` and `0.8919` controlled on all 317; `0.975` and `0.849` on
  the 184 primitive; `759` of 2195 pairs and `37` of 317 posets going the wrong way; max errors
  `1/40, 5/132, 5/114`; the named false-positive poset with `δ_walk = 12/37`, `δ = 5/14` (and it
  is the *only* false positive at `n = 6`); the one-sided filter retaining `0.5%`.
- **§5.3** — **139,765** 2-block partitions, 0 failures of the level description *and* 0
  failures of the excess identity; "primitive ⟺ positive excess at every 2-block level" 0 bad of
  **2447**.
- **§5.4** — extremal posets with `e(P) = 3`: `1/1, 2/2, 3/3, 4/5, 5/8`.
- **§5.2's Proposition 5** — verified against the **exact stationary vector** of the actual
  transition matrix, solved over `Q` by Gaussian elimination rather than assumed: 73 posets,
  **273** incomparable pairs at `n ≤ 5`, 0 mismatches (the document's own control C8 covers 52
  pairs).
- **§5.5** — Theorem 7 on the actual matrix in exact rationals (uniform stationarity *and*
  `λ₂ = t`), 95 (poset, `t`) cases, 0 failures; `717` of 2195 pairs with `π = p` exactly, worst
  gap `5/114`.
- **§6** — the ladder at `n = 6` (`54 / 88 / 111 / 111 / 111` fibers, `P[collide]`
  `0.0219 / 0.0094 / 0.0043`, `5.4% / 13.0% / 20.7%` singleton); the whole correlation table
  including `λ₂` at `ρ = −0.139` and `δ_walk` at `0.975 / 0.849`; `ρ(λ₂, δ) = −0.020` at
  `n = 7`; the trend row `71.4 / 35.5 / 20.7 / 7.3` and `1 / 10 / 73 / 626` non-singleton fibers
  (`n = 3` excepted, minor item 4).
- **§6's negative, on a wider population than claimed** — no `I4` fiber containing two posets
  with different `δ` at any `n ≤ 7`, not only over the 626 non-singleton fibers of the primitive
  non-chains but over **963** non-singleton fibers of all posets including chains. The
  document's open question is left open for a stronger reason than it gives.
- **§2** — 0 majority cycles in all **2447** posets at `n ≤ 7`, ties included; the `n = 11`
  witness in full.
- **§7** — the Markov arithmetic and the exact ball masses (`Pr[inv < 2|Inc|/3] = 1` on the
  posets shown, confirming the bound is loose).
- **Reproducibility** — I re-ran `run_all.sh` from a clean copy: `probe_output.txt` and
  `selftest_output.txt` are both **byte-identical** to the committed files.

---

## 6. What I could not establish

- **Whether `n = 8` admits a majority cycle.** My search was negative (0 in 30,000 across six
  densities) and I did not enumerate `n = 8` exhaustively (16,999 classes). The minimum is
  therefore known only to lie in `{8, 9}`.
- **Whether `Q(P)` is a function of the convex restriction counts** (minor item 3). I did not
  test it; I only observe that the document's box asserts it implicitly.
- **Whether some non-trivial spectral quantity is constant on `W_unif(P)`** (minor item 2). The
  claim as written is unproven in that direction; I did not attempt to construct a counterexample
  beyond the degenerate one.
- **Anything about `n ≥ 8` for the concentration or detection statistics.** I reached the same
  boundary the target did, and for the same reason.

---

## 7. Files

```
code/counterexample_audit_a7b4/kernel.py           the independent instrument
code/counterexample_audit_a7b4/records.py          per-poset records (n = 3..7)
code/counterexample_audit_a7b4/selfcheck.py        10 controls, incl. A000112/A001035/A000670
code/counterexample_audit_a7b4/check_bridge.py     section 2 + the n=11 witness
code/counterexample_audit_a7b4/check_main.py       sections 3.1-3.3
code/counterexample_audit_a7b4/check_sections.py   sections 4, 5.1-5.4
code/counterexample_audit_a7b4/check_egroups.py    the e(P)-controlled comparison (finding 1)
code/counterexample_audit_a7b4/check_prop5.py      Prop 5 vs the exact stationary vector
code/counterexample_audit_a7b4/check_spectral.py   sections 5.2, 5.5, 6, 7
code/counterexample_audit_a7b4/check_leftovers.py  named witnesses, filters, cost
code/counterexample_audit_a7b4/witness9.py         the n = 9 majority-cycle witness (finding 3)
code/counterexample_audit_a7b4/shrink_witness.py   shrinking the document's n = 11 witness
```

*Audit by mg-a7b4. The verdict is raw and goes to pm-onethird; STATE.md is untouched.*
