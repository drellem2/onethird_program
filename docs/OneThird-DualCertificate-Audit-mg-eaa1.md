# Independent audit of `mg-131e`'s dual certificates and its `n = 6` refutation

`mg-eaa1` · auditor instrument [`code/dual_certificate_audit_eaa1/`](../code/dual_certificate_audit_eaa1/) ·
audited: `mg-131e` (`b7b6941`), its document
[`OneThird-DualCertificate-mg-131e.md`](OneThird-DualCertificate-mg-131e.md), and
**`STATE.md` at `491d42c79f7628c18cb7a5d197faa9f4600cd6c1`** (`mg-b488`) ·
predictions: [`PREDICTIONS.md`](../code/dual_certificate_audit_eaa1/PREDICTIONS.md), committed
at `61f7f5b` **before any script of this audit existed and before one byte of
`code/dual_certificate_131e/` was read**

---

## 0. Verdict

> **All seven checks in the brief PASS. Every number in `mg-131e` reproduces from code that
> shares nothing with it, its `n = 6` refutation is rediscovered here independently, and the
> `n`-indexed pattern *survives* the out-of-sample test the brief asked me to break it with —
> because that pattern was never the claim that died.**

The brief was written on the hypothesis that an `n`-indexed verdict "reads as a route to the
wall", and instructed me to extrapolate the pattern to `n = 6` and try to break it. The honest
report is that **the pattern does not break**: the dual `λ = 0, t ≡ 1, s = 0` is feasible on the
consecutive-pairs branch at `n = 6` through `n = 12` with bound exactly `(n−1)/3`, and
`mg-200d`'s fence attains it there. That is a theorem and it is `n`-indexed.

What is false is a different statement. The `≤` direction is a maximum over all `2^C(n,2)`
branches, and it dies at `n = 6` on a branch the `n`-indexed dual does not cover. `mg-131e`
draws exactly that distinction and does not overstate it in either direction.

Four findings are recorded in §5. **None of them moves the verdict**, and one of them
(`F2`) resolves *in the parent's favour* — a sentence it published without the caveat its own
transcript carries turns out to be true, and is now checked rather than assumed.

| brief check | verdict | where |
|---|---|---|
| 1 · verify each certificate by substitution, exact rationals, `n = 3,4,5` | **PASS** (+ `F1`) | §2 |
| 2 · certifies the DISJUNCTIVE program, not the infeasible literal one | **PASS** | §1 |
| 3 · extrapolate the `n`-indexed pattern to `n = 6` and try to break it | **PASS — pattern survives; the `≤` direction does not** | §3 |
| 4 · audit the negative as hard as the positive | **PASS** (+ `F2`, `F3`) | §4 |
| 5 · no tightness claim crept in | **PASS** | §4.3 |
| 6 · `≥` and `≤` stayed separate | **PASS** | §4.4 |
| 7 · no poset enumeration, no transitivity imposed | **PASS** | §4.5 |

**Independence.** Every combinatorial primitive, the row builder, the exact-rational two-phase
simplex and the arithmetic dual verifier in `lib_eaa1.py` are written from the definitions. The
single call into `mg-200d`'s code is `rows_agree_with_lp200d`, which exists only to *assert*
that my rows are its rows — and that assertion is check 2, not a dependency. Controls:
`selftest_eaa1.py`, 8 groups, 3 mutations, a hand-solved LP, and a cross-implementation check
of all four primitives against `lp200d` on all `120` permutations at `n = 5`.

---

## 1. Check 2 — is it the right program? (This is the cheapest way to fail, so it is first.)

`mg-200d`'s theorem says the **literal** all-pairs formulation is infeasible: per-slot symmetry
on every pair holds for `uniform L(P)` iff `P` is an antichain, and no antichain is in `M_n`. A
dual certificate for an infeasible program bounds a maximum over the empty set. It would look
immaculate and mean nothing.

`a1_program.py`, four ways:

* **My row builder against `lp200d.build`.** Identical as a **multiset** *and* **in order**, on
  the literal branch, the attaining branch, the consecutive branch and the `n = 6` refuting
  branch, at `n = 3,4,5,6` — `10/5/1/5`, `25/7/1/7`, `51/14/1/9`, `13` rows respectively. Order
  matters: it is what makes a multiplier vector index-comparable across the two builders
  without a re-indexing step I could have got wrong (`PREDICTIONS P15`).
* **The literal program is INFEASIBLE** at `n = 3, 4, 5` on my own two-phase simplex. The trap
  is real and computed, not trusted.
* **The certified branches are not it.** Non-empty comparable set at each `n`
  (`{(0,2)}`; `{(0,2),(0,3),(1,3)}`; `{(0,2),(0,3),(1,4),(2,4)}`), primal-**feasible**, value
  positive, and equal to `(n−1)/3` on my own solver. All three of the other branches `d1`
  reports as attaining `4/3` at `n = 5` also check out.
* **`mg-200d`'s witnesses by substitution** — mass `1`, caps, no comparable pair flipped,
  per-slot symmetry, objective — with no solver in the block at all.

**Check 2: PASS.** The certified object is `mg-200d`'s disjunctive formulation, and the branch
it certifies is feasible and attaining.

---

## 2. Check 1 — the certificates, by substitution

`a2_certificates.py` rebuilds the `≤` direction from scratch: for every one of the
`8 + 64 + 1024` branches it constructs a dual on **my** rows and verifies it by substitution —
sign conditions plus `Σᵢ yᵢ A_ij ≥ c_j` on every column, pure `Fraction` arithmetic, no simplex
reachable from the verifier. Every count `mg-131e` publishes reproduces **exactly**:

| | `n = 3` | `n = 4` | `n = 5` |
|---|---|---|---|
| primal classes (infeasible / zero / positive) | `5 / 2 / 1` | `51 / 8 / 5` | `908 / 64 / 52` |
| tier 0 (trivial) / needing more | `7 / 1` | `46 / 18` | `636 / 388` |
| of the "needing more", infeasible → **vacuous** | `1` | `18` | `386` |
| of the "needing more", feasible → **informative** | `0` | `0` | **`2`** |
| feasible branches with strong duality checked / failures | `3 / 0` | `13 / 0` | `116 / 0` |
| branches attaining `(n−1)/3` | `1` | `1` | `4` |
| **max certified bound over all branches** | **`2/3`** | **`1`** | **`4/3`** |

The **trivial dual is verified as a theorem, not as a computation**: on every branch at every
`n` it is feasible *and holds with equality on every column*, and its bound is exactly
`|I_active|/3`. `selftest_eaa1.py S5` checks the algebraic step under it — `flips(p) ⊆ I_active`
on every column of every branch — rather than taking the identity on trust.

`mg-131e`'s informative-hard sequence `0, 0, 2` is confirmed. **Three points was one point.**

Two details worth confirming separately because they are `mg-131e`'s corrections *against
itself*, and a self-correction is the kind of claim an audit should not wave through. There are
**four** branches attaining `4/3` at `n = 5`, not the one `mg-200d`'s transcript shows — confirmed
— and on **two** of the four the trivial dual is **tight** (`|I_active| = 4`, bound `4/3`),
which does make the `n = 5` certificate look better than it is. Both hold. And the `C = ∅`
branch — the infeasible literal program of §1 — **is** among the certified branches at each `n`,
since it is one of the `2^C(n,2)`; it is correctly classed `infeasible` and counted as vacuous on
`d1`'s own `tier × primal class` line, and nothing in the result rests on it.

### 2.1 `F1` — the tier-2 certificates are not committed as data

My brief says *"a certificate is checkable in a way an LP run is not — so check it, do not
re-run the LP."* For `1 / 18 / 388` of the branches that is **not literally available to a
reader**: `d1` regenerates those multipliers from `budgeted_dual` at run time and its transcript
prints only counts and tiers. The committed artefact there is a *count*, not a *certificate*.

This is a defect of form, not of substance, and I resolved it by doing the stronger thing —
building my own family on my own rows — after which every count matched. My transcript prints
the two informative `n = 5` certificates **as data**, which `mg-131e`'s does not:

```
C = [(0,2), (0,3), (1,4), (2,4)]      val = 4/3      certificate bound = 4/3
    λ            = −2         t(1,2) = 8      t(2,3) = 1      t(3,4) = 1
    s(0,1),k=0   =  3         s(1,2),k=1 = −5     s(1,2),k=2 = −8
    s(1,3),k=1   = −5         s(2,3),k=1 =  4
```

Note `λ = −2 ≠ 0` and `t_(1,3)` absent (`= 0`) — an independent instance of exactly what §4.1
proves is forced.

**Check 1: PASS**, with `F1` recorded.

---

## 3. Check 3 — extrapolate the pattern to `n = 6` and try to break it

This is the check the brief says needs the most scrutiny, and the one my own dispatch prompt had
already half-answered before I started (`PREDICTIONS §0 H1`, disclosed there rather than
laundered into a prediction here).

### 3.1 The pattern survives its first out-of-sample prediction

`mg-131e`'s `n`-indexed object is precise enough to extrapolate without interpretation:
`λ = 0`, `t = 1` on every cap row, `s = 0`, on the branch `I = {(i,i+1)}`. The prediction at
`n = 6` is: dual-feasible, bound exactly `5/3`, fence attains. `a3_n6.py` A3.1:

| `n` | 3 | 4 | 5 | **6** | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|
| columns | 3 | 5 | 8 | **13** | 21 | 34 | 55 | 89 | 144 | 233 |
| cap rows | 2 | 3 | 4 | **5** | 6 | 7 | 8 | 9 | 10 | 11 |
| dual bound | `2/3` | `1` | `4/3` | **`5/3`** | `2` | `7/3` | `8/3` | `3` | `10/3` | `11/3` |
| fence `E[inv]` | `2/3` | `1` | `4/3` | **`5/3`** | `2` | `7/3` | `8/3` | `3` | `10/3` | `11/3` |

**It does not fail.** The column counts are Fibonacci because the columns of that branch are
exactly the matchings of the path on `n` vertices — a permutation flips only consecutive pairs
iff it is a product of disjoint adjacent transpositions. (The direct generator that makes
`n = 11, 12` reachable at all is cross-checked against brute-force filtering of `n!` at every
`n ≤ 8`.) So `val = (n−1)/3` on that branch, both directions, no solver on either side, at
every `n` tested to `12`.

**A pattern that survives its first out-of-sample prediction is not refuted, and I will not
dress this up as if it were.** `mg-131e` says the same thing and does not oversell it: it is a
theorem about **one branch out of `2^C(n,2)`**.

### 3.2 So break it where it lives — independently

The `≤` direction is a statement about the **maximum over all branches**, which the trivial dual
bounds by `|I_active|/3` — useless as soon as a branch has more than `n−1` active pairs. So I
ran a **declared, non-exhaustive** probe *without reading `mg-131e`'s witness*: every branch at
`n = 6` whose incomparable set is `consecutive ∪ S`, `|S| ≤ 2` over the `10` non-consecutive
pairs — `56` branches, `20` primal-feasible, `1.1s`.

**Four of them beat `(n−1)/3 = 5/3`, all at `11/6`.** And the optimum my solver returned on the
`S = {(1,4)}` branch is, atom for atom and mass for mass, `mg-131e`'s published 6-atom witness.
I did not find *a* refutation; I found *theirs*, from the other end.

```
S = {(1,4)}    value 11/6 = 1.8333    ε_spec = 11/35 > 2/7 = 2/(n+1)
  1/6 · (0,1,2,3,5,4) inv 1     1/6 · (0,2,1,4,3,5) inv 2     1/6 · (1,0,2,3,4,5) inv 1
  1/6 · (0,1,3,2,5,4) inv 2     1/6 · (0,2,4,1,3,5) inv 3     1/6 · (1,0,3,2,4,5) inv 2
  q: (0,1)=(1,2)=(2,3)=(3,4)=(4,5)=1/3,  q_(1,4)=1/6      comparable set: TRANSITIVE
```

Mass `1`; every flip probability `≤ 1/3`; no comparable pair flipped; zero per-slot symmetry
violations; `E[inv] = 11/6` recomputed by substitution. **The `≤` direction is false at `n = 6`.**

### 3.2a Deeper, and `11/6` does not move

`mg-131e` is careful to say every `n ≥ 6` number is a lower bound on a **named** branch, so the
true `n = 6` maximum **may exceed `11/6`** (`§7`). Nothing here contradicts that, but it can be
narrowed. Widening the same probe to `|S| ≤ 4` — `386` branches, `39` primal-feasible, `29.7s`:

* **`8` branches beat `5/3`, and every one of them is at exactly `11/6`.** Nothing found is
  larger.
* **Every one of the `8` contains the chord `(1,4)`** — the pair `mg-131e` identifies as
  carrying the whole excess. Independent corroboration of its mechanism claim, from the search
  side rather than the witness side.

So over **every branch at `n = 6` whose incomparable set is `consecutive ∪ S` with `|S| ≤ 4`**,
the maximum is exactly `11/6`. That is a much larger family than one named branch and it is
still not the `2^15` the ticket forbids: branches omitting a consecutive pair, and `|S| ≥ 5`, are
unprobed. `11/6` stands as a lower bound on the `n = 6` maximum, now with more under it.

### 3.3 Their witnesses, in my arithmetic

All five hard-coded witnesses at `n = 6,7,8,9,10` are transcribed by hand into `a3_n6.py` and
re-checked with my own `inv`, `flipped_pairs`, `adjacencies` and cap logic. Every one is
feasible, every claimed value is right, every one beats `(n−1)/3`, and every comparable set is
transitive — `10/10` checks.

### 3.4 `(5n−8)/12` is a branch OPTIMUM, not just a lower bound

`d3` writes *"the value is `(5n−8)/12`"* on a line whose every other number is explicitly a
lower bound, so the wording is doing more work than the object under it. Re-solved here as a
maximum: `n = 6` → `11/6`, `n = 8` → `8/3`, both exactly `(5n−8)/12`. So the claim is sound as
written. (`n = 10` not re-solved — declared in §6.)

**Check 3: PASS.**

---

## 4. Checks 4–7 — auditing the negatives

### 4.1 `F3` — the exclusion argument, unboxed

`mg-131e` does not report "ad hoc". It reports something stronger: at the one informative point,
the natural `n`-indexed shape is **excluded**, by ranging each multiplier over the whole dual
optimal face. A negative of that strength has to be checked, and its `d2` transcript marks
several coordinates `(boxed)` — its ranging LP carries a `±1000` box, and *a conclusion drawn
from a boxed range is a conclusion about the box*.

Recomputed in `a4_verdict.py` with **no box at all**, on both informative hard branches:

```
max λ over the dual optimal face  =  −1        (exact, unboxed, attained)
min λ over the dual optimal face  =  UNBOUNDED BELOW
max t_(1,3) = min t_(1,3)         =   0        (exact, unboxed)
```

**The conclusion stands and is genuine**: `λ < 0` across the entire face, so no certificate there
has `λ = 0`; and `t_(1,3)` is pinned to `0`, so none has `t` an indicator vector. The absence is
**exhibited, not unfound** — which is what my brief asks of a negative.

`F3` is the published range's *lower* end. `λ ∈ [−1995/2, −1]` is printed on a row not marked
`(boxed)`, and `−1995/2` **is** the box: unboxed, `λ` runs to `−∞`. Nothing rests on it, but
anyone quoting `−1995/2` is quoting the `±1000`.

### 4.2 `F2` — a caveat that did not survive the trip from transcript to page

`d2` PART B2 measures that at every one of the `52` value-positive branches at `n = 5` the
optimum flips only consecutive pairs, and then **caveats itself in the transcript**:

> *"the optimum reported is one vertex of the optimal face, so `0` means `no reported optimum
> does`, not `no optimal measure can`."*

That caveat is **absent from the document's §4 and from `STATE.md` row 167**, both of which
state the sentence flat. So as published the claim was stronger than the measurement under it —
the mechanism argument, which is (c) of three load-bearing claims.

I settled it rather than scoring it. For every value-positive branch at `n = 5` and every
non-consecutive pair carrying a cap, maximise that pair's flip mass over the **whole optimal
face** (branch constraints plus `objective ≥ val`, which forces equality). Result: **`0`
everywhere — `0` branches, `0` instances, maximum `0`.**

**So the unqualified sentence is TRUE.** It simply was not established by what was printed under
it, and now it is. This finding resolves in `mg-131e`'s favour.

### 4.3 Check 5 — no tightness claim crept in

A dual certificate says nothing about realisability, and this arc would find it easy to write as
though it did. It does not: the document's §6 and `STATE.md` row 167 both say tightness is open
beyond `n = 3` and do not claim it. The numbers, re-derived (`a3_n6.py` A3.5, one **named**
relation per line, no enumeration):

| relation | `\|L(P)\|` | `E[inv]` | max flip | in `M_n`? |
|---|---|---|---|---|
| `n = 3`, the attaining branch `0 < 2` | `3` | `2/3` | `1/3` | **yes — and it attains `(n−1)/3`** |
| `n = 4`, the attaining branch | — | — | `2/5` | no |
| `n = 5`, the attaining branch | — | — | `4/11` | no |
| `n = 6`, the **refuting** branch | `14` | `23/14` | `5/14` | no |

Tightness holds **at `n = 3` and nowhere else that is claimed**. `mg-131e`'s stated `5/14` is
confirmed exactly. **Check 5: PASS.**

### 4.4 Check 6 — the two directions stayed separate

The `≥` is a theorem for every `n` (a lower bound, and it survives untouched — a *larger* value
does not threaten a lower bound). The `≤` is what died. `mg-131e`'s §0 table splits them
typographically — `= 2/3, = 1, = 4/3` against `≥ 11/6, ≥ 20/9, …` — its §2 states the
`n`-indexed equality with **both** directions and a proof on each, and `STATE.md` row 167 splits
the whole result into `(a)` refuted, `(b)` new theorem, `(c)` not refuted but thinly supported,
with the kind written at each. Nowhere is "the value is `(n−1)/3`" reported flat.
**Check 6: PASS.**

### 4.5 Check 7 — no poset enumeration, no transitivity imposed

Transitivity appears in `mg-131e` exactly once, as `is_transitive(C)` applied to **the answer** —
a checked property of one named comparable set, reported so that the refutation cannot be
dismissed as an artefact of the relaxation's slack over transitivity. It is never a constraint,
never a filter on branches, and no poset is constructed. `uniform_le_measure` is used on named
relations as a realisability *control*. This audit keeps the same discipline.
**Check 7: PASS.**

### 4.6 `F4` — a local over-reach, corrected two sections later

§5 writes *"the statement is false from `n = 6`"*, which reads as all `n ≥ 6`. §7 says plainly
that *"false at `n = 6`" is a theorem here and "false for every `n ≥ 6`" is not*, and
`STATE.md`'s scope-limits sentence says the same. The tension is local and the correction is
present and emphatic; recorded so it is not re-derived by the next reader.

---

## 5. `STATE.md` at `491d42c`, read by a hostile reader who never saw the correction

The requirement was to name the SHA and to say whether the refutation is legible **at** the
claim. It is `491d42c79f7628c18cb7a5d197faa9f4600cd6c1`, and it is.

* All **four** occurrences of `2/(n+1)` in the file are on rows `167` and `168`. Row `167`'s
  headline itself carries `REFUTED — ε_spec = 2/(n+1) IS A SMALL-n COINCIDENCE, AND IT IS FALSE,
  NOT CONJECTURAL`. Row `168`'s two occurrences are (i) the correction pointer and (ii) an
  explicit flag that a *different* document (`mg-6bc2 §5.1`) still prints the formula as live.
  There is no occurrence anywhere that reads as a live claim.
* The retired threshold arithmetic — `n ≥ 11`, `n ≥ 99`, `≈ 2×10⁻²` — appears **only inside the
  sentence that retires it** (`THE THRESHOLD ARITHMETIC IS VOID, NOT UPDATED … do not print a
  new number and do not carry the old one`). No stale threshold survives as a live figure.
* Row `167` carries the relaxation-vs-truth distinction explicitly: *"the frozen-poset
  conjecture itself — the disjunctive value is an upper bound on it, and showing the upper bound
  is bigger than believed weakens the bound and says nothing about the statement underneath."*
  This was the defect I bet near-even on finding (`PREDICTIONS P12`) and it is not there.

The one thing row `167` inherits is `F2`: it states PART B2's mechanism sentence without the
transcript's caveat. §4.2 settles that the sentence is true, so the row is correct — but it was
correct in advance of the measurement, and that is now repaired by measurement rather than by
edit.

---

## 6. What this audit did NOT do

* **No exhaustive `n = 6`.** My probe is restricted to branches whose incomparable set contains
  **all** consecutive pairs, and to `|S| ≤ 4` chords beyond them. Branches that omit a
  consecutive pair are not probed at all, and neither is `|S| ≥ 5`. So I can say the `n = 6`
  maximum is `≥ 11/6`, that it is exactly `11/6` **within that family**, and I **cannot** say
  what it is. A run at `|S| ≤ 10` (all `1024` chord sets) was started and **killed after about
  seven minutes of CPU without finishing** — the large-`|S|` branches approach the `720`-column
  literal program. That is a limit of my patience, not a result, and it is why the committed
  deep transcript is the `|S| ≤ 4` one.
* **No Farkas certificates for the infeasible branches**, in either direction. Like `mg-131e`, I
  discharge them with a dual of objective `≤ (n−1)/3` (always available) plus a recorded
  infeasibility from a **solver**. That step is not arithmetic in my work either, and saying so
  is the point.
* **`(5n−8)/12` not re-solved as an optimum at `n = 10`**, and not proved for any `n` — checked
  at `n = 6, 8` only.
* **No `n ≥ 6` upper bound of any kind.** Nothing here bears on the true growth constant, which
  `mg-131e` correctly names as the live question that replaces the refuted one.
* **`mg-131e`'s `selftest131e.py`, `PREDICTIONS.md` and `OUTCOMES.md` read but not re-run**, and
  its `d1`/`d2`/`d3` scripts **not executed** — every number above is from my own code, which is
  the stronger check but means I have not verified their scripts reproduce their transcripts.
* **No audit of `mg-76b2`'s `C₃ = 1`**, which the ticket's "what it would buy" paragraph leans
  on; no `L4`, no `ε_dem`, no `.tex`.
* **Nothing repaired.** `F1`–`F4` are reported, not fixed; no `mg-131e` file and no `STATE.md`
  row is edited by this ticket.
