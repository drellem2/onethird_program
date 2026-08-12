# `mg-7c78` — DANIEL'S ADJACENT-TRIPLES OBSERVATION, MADE PRECISE AND CHECKED

**Work item.** `mg-7c78`, filed high by `pm-onethird` 2026-08-12 as a candidate FACT under
`mg-03cf`'s standing instruction that facts are collected whether or not anything consumes them.
**Instrument.** [`code/adjacent_triples_7c78/`](../code/adjacent_triples_7c78/) — ten arms,
standard library only, exact rationals on every verdict path, importing nothing from this
repository. **Predictions** committed at `9bed392`, before one line of the instrument existed,
with four of the twelve disclosed as already-derived reports.

---

> ## ⛔ THE TICKET'S PREMISE WAS MISFILED, AND IT WAS CORRECTED MID-RUN
>
> `pm-onethird` filed *"adjacent triples in a linear extension"* as **three ELEMENTS at
> consecutive positions inside one linear extension**, and built the ticket's whole framing on
> that — the comparison against `FACTS.md` F1, the no-3-cycle caution, the position-class
> language. He then asked Daniel and retracted it in writing. **Daniel, verbatim:**
>
> > *"i meant pick some permutation of the whole set of linear extensions (for instance one
> > specially crafted) then there will always be 3 adjacent linear extensions sharing a given
> > 'good' edge"*
>
> **The objects being made adjacent are LINEAR EXTENSIONS, not elements.** The ambient object is
> `L(P)` as a sequence or a graph, not the internal layout of any one extension.
>
> **THIS DOCUMENT REPORTS BOTH.** The corrected reading is §§2–4 and is the answer to the ticket.
> The misfiled reading is §5 and is kept rather than deleted for two reasons: everything measured
> under it is **true**, and one of its findings — that the `δ = 1/3` boundary class has **width 2
> and no 3-element antichain at all** — is what closes the last surviving branch of the corrected
> reading in §3.4. A retraction that deletes the work also deletes the reason the retraction was
> checkable.

---

## §0. THE VERDICT

| # | the precise statement | verdict | kind |
|---|---|---|---|
| **Q4** | `> 2/3` ⟹ three **mutually adjacent** linear extensions sharing a good edge | **FALSE at every poset, with no hypothesis** | `U` |
| **Q2** | `> 2/3` ⟹ **every** ordering of `L(P)` has 3 **consecutive** extensions good for a given edge | **TRUE IN A WEAKER FORM** — sharp criterion `g > ⌈2N/3⌉`; `> 2/3` alone suffices **iff `3` divides `\|L(P)\|`** | `U` |
| **Q1** | ∃ **one** ordering of `L(P)` with a good run of 3 for **every** incomparable edge at once | **NOT REFUTED, PARTLY PROVED** — its necessary condition is a theorem under the strict hypothesis; two sufficient certificates fire; general case **OPEN** | `OPEN` with `U` fragments |
| **Q3** | Q1 restricted to **Gray codes** (Hamiltonian paths in the BK graph) | **the run condition is nearly free; the Gray code is NOT** — a Hamiltonian path fails to exist at 6 of 117 posets decided | `FP✗` for the obstruction |
| **THE TRICK** | *"the bigger idea is just to use this combinatorial trick with `> 2/3`"* — Daniel, when asked, §2.5 | **TRUE, AND REPAIRED** so it needs no side condition: `p_xy > 2/3 + 2/N` is sufficient at every `N`. **What it is not is a lever** — §4 | `U` |

**IS IT A REALIZABILITY FACT IN THE LEDGER'S SENSE? NO — AND THE REASON IS THE SHARPEST THING IN
THIS DOCUMENT.** Q2's entire content is a **pigeonhole fact about binary sequences**. It consumes
`p_xy` — one pair marginal — and `|L(P)| mod 3`, and **nothing else about the poset**. It places
no constraint on which combinations of pair-biases can co-occur, so it does not add the
realizability fact `STATE.md:21` says every route below `1` must add. `Op-Form` Claim 6.1 already
consumes `p_xy` at equality, and Q2 asks for no more than that.

**AND THE `2/3` IS NOT THE CORPUS'S `2/3`.** This is the finding most likely to be mis-carried, so
it is stated before anything else:

> The corpus's `2/3` is the **pair-bias threshold**: of three elements at most two of the cyclic
> events can hold, so strong majorities cannot cycle and cohere into `e` (`mg-61bb`). Daniel's
> `2/3` is the **run-density threshold**: an ordering of `N` items carrying more than a `2/3`
> fraction of "good" ones cannot avoid 3 consecutive good ones. **These are two different facts
> that happen to produce the same constant, because `1 − 1/3` appears in both.** The coincidence
> is exactly what makes the observation feel like it should connect to the programme, and it is
> also why it does not.

---

## §1. NOTATION, FIXED ONCE

`P` a finite poset on `n` elements · `L(P)` its linear extensions, `N = |L(P)|`, uniform measure ·
`x ∥ y` incomparable · `p_xy = Pr[x before y]` · `δ(P) = max_{x∥y} min(p_xy, 1−p_xy)`
(`STATE.md:48`), **frozen** `= δ(P) < 1/3` · `e` the distinguished order the `> 2/3` majorities
cohere into.

An extension is **good for the edge `{x,y}`** when it orients that pair the way `e` does;
`g_xy = p_xy · N` counts them (taking `p` on the `e` side). **THE BK GRAPH** is `L(P)` with an
edge between two extensions differing by one **adjacent transposition** — one legal swap of two
adjacent incomparable elements.

**"Good" means aligning with the pair bias** — the `e`-orientation of an incomparable pair.
That is Daniel's own word for it when asked (§2.5) and not this document's guess.

---

## §2. THE CORRECTED READING, MADE PRECISE

Four candidate statements. They are not variants of one claim; they differ in strength and in
whether the hypothesis is used at all.

**Q4 (mutual adjacency).** For each incomparable edge `{x,y}` there are three linear extensions,
**pairwise adjacent** in the BK graph, all good for `{x,y}`.

**Q2 (universal over orderings).** For each incomparable edge `{x,y}` and **every** ordering
`σ_1, …, σ_N` of `L(P)`, there is an `i` with `σ_i, σ_{i+1}, σ_{i+2}` all good for `{x,y}`.

**Q1 (existential over orderings, all edges at once).** There is **one** ordering of `L(P)` such
that for **every** incomparable edge there is such a run of three. This is what *"one specially
crafted"* points at, and it is the reading with content.

**Q3 (Q1 restricted to Gray codes).** Q1, with the ordering required to be a Hamiltonian path in
the BK graph — consecutive extensions differing by a single adjacent transposition.

### §2.5 DANIEL ANSWERED, AND THE ANSWER MOVES THE SUBJECT

Asked at 2026-08-12 22:44Z, answered twice within fifteen minutes. **Verbatim:**

> *"i want to clarify that this reading isn't the only one. the bigger idea is just to use this
> combinatorial trick with `> 2/3`, or keep it in mind for later"*
>
> *"my example was only meant as an example of this trick: imagine you nicely constructed some
> permutation of linear extensions of X. Perhaps it's an extension of the weak bruhat order who
> knows. Then you could guarantee that in this permutation \*of\* all linear extensions there are
> 3 adjacent linear extensions sharing a given edge that aligns with the pair bias"*

**So the object he wants recorded is THE TRICK, not any one of Q1–Q4.** Q1–Q4 were the instantiation
being disambiguated; the trick is the reusable statement underneath, and *"keep it in mind for
later"* is an explicit instruction to log it in the form a future consumer could pick up. That is
§3.5, and the registry entry for it is `FACTS.md` **F18**.

Two things his answer settles that the enumeration could not. **"Adjacent" means CONSECUTIVE in the
crafted ordering** — `Q4`'s mutual-adjacency reading is not what he meant, though §3.1 records that
it is false anyway. **"Good" means aligning with the pair bias** — the `e`-orientation, which is the
reading this document had already taken. And one thing his answer adds: the crafted ordering may
carry structure, his named candidate being **a linear extension of the weak Bruhat order** on
`L(P)`. §3.5 measures what that structure does and does not buy.

---

## §3. THE RESULTS

### §3.1 Q4 IS FALSE AT EVERY POSET, AND `> 2/3` NEVER ENTERS

**THEOREM (`U`, one line).** Three linear extensions **pairwise adjacent** in the BK graph do not
exist, at any poset, at any `n`. *Proof.* One transposition changes the parity of a permutation,
so the BK graph is a subgraph of a bipartite graph — the two sides being the even and odd
permutations — and a bipartite graph is triangle-free. ∎

**AND THE KILL DOES NOT DEPEND ON THE TRANSPOSITIONS BEING ADJACENT.** `b0` `b2` measured the
graph in which two extensions are joined when they differ by a swap of two values at **arbitrary**
positions: **0 triangles over 84 posets**, for the same reason — *every* transposition is odd. So
under **any** transposition-based notion of "adjacent linear extension" the statement is false.

**MEASURED.** `b0` `b1`: every isomorphism class at `n = 2…6` with `|L(P)| ≤ 400` — **403 posets,
1 skipped and counted, 21 941 graph edges, 0 triangles, 0 non-bipartite**. The measurement is a
corroboration of a proof, not the warrant.

**THE ONE ESCAPE, AND THE HYPOTHESIS SHUTS IT.** If "adjacent" is allowed to mean *related by
rotating three consecutive positions* — a 3-cycle, which is **even** — then `σ, σ·c, σ·c²` **is** a
triangle, and `b0` finds **430** of them over 84 posets. Such a triangle exists exactly when the
three rotated positions hold a **free 3-block**, i.e. a 3-element antichain. And §5.3 measures
that the `δ = 1/3` boundary class contains **zero** 3-element antichains. So that escape closes
too, and it closes **because of** the hypothesis rather than in spite of it.

### §3.2 Q2 IS TRUE ON A DIVISIBILITY SIDE CONDITION, AND THAT IS THE WHOLE OF ITS CONTENT

**THE RUN LEMMA (`U`, exact).** The largest number of good items an ordering of `N` items can
carry while containing **no** 3 consecutive good ones is `N − ⌊N/3⌋`, attained by the periodic
pattern `G G B`. Hence:

> **every** ordering of `L(P)` has 3 consecutive extensions good for `{x,y}`
> **iff** `g_xy > N − ⌊N/3⌋ = ⌈2N/3⌉`.

Brute-forced against all `2^N` orderings for `N ≤ 16` — **16 of 16 agree** (`b0` `b3`).

**THE DIVISIBILITY CATCH, AND IT IS NOT A BOUNDARY WOBBLE.** `p_xy > 2/3` gives `g_xy > 2N/3`.
That implies `g_xy > ⌈2N/3⌉` **iff `3` divides `N`**, and fails for **both** other residues at
**every** `N` checked to 21. The smallest counterexample is `N = 4, g = 3` — so `p = 3/4`,
comfortably over `2/3` — with the avoiding ordering `G G B G`.

**MEASURED ON REAL POSETS** (`b1` `m1`, isomorphism classes `n ≤ 6` with a well-defined `e`, plus
the boundary class at `n = 7, 8`):

| `δ` band | edges | `g > ⌈2N/3⌉` | `3 \| N` |
|---|---|---|---|
| `δ = 1/3` (boundary) | 82 | **0** | 82 |
| `1/3 < δ ≤ 2/5` | 126 | 25 | 8 |
| `2/5 < δ < 1/2` | 497 | 209 | 288 |

⚠️ **THE BOUNDARY ROW'S ZERO IS NOT A REFUTATION OF Q2 — IT IS THE PROXY FAILING, AND THE
DISTINCTION MATTERS.** `δ = 1/3` means the most-balanced pair sits at **exactly** `2/3`, so its
`g = 2N/3` is not even `> 2N/3`. Q2 is a statement about the **strict** hypothesis, and the
boundary class gives up exactly the strictness it needs. §5 explains why the same class is
nevertheless the **right** proxy for the misfiled reading's statements: those are not sensitive to
strictness and this one is.

**A theorem whose truth turns on `|L(P)| mod 3` is not the shape a lemma takes**, which is the
evidence — independent of Daniel's answer — that the intended reading is Q1 and not Q2.

### §3.3 Q1 IS NOT REFUTED, AND TWO OF ITS PIECES ARE THEOREMS

**THE NECESSARY CONDITION IS A THEOREM UNDER THE STRICT HYPOTHESIS.** Q1 needs `g_xy ≥ 3` at every
edge — with fewer than three good extensions no ordering, crafted or not, has a good run of three.
And frozen supplies it: `g_xy > 2N/3` with `g_xy` an integer forces `g_xy ≥ 3` as soon as `N ≥ 3`,
and a poset carrying an incomparable pair with `N = 2` has that pair at exactly `1/2`, so is not
frozen. `U`.

**A SUFFICIENT CONDITION, ALSO BY HAND, QUANTIFIED.** Assign the triples one edge at a time; at
most `3(m−1)` extensions are already spent, so a system of pairwise-disjoint good triples exists
whenever `min_xy g_xy > 3(m−1)`, where `m` is the number of incomparable edges. Under frozen that
reads `2N/3 ≥ 3m − 2`. Laying those triples out consecutively at the front of the ordering proves
Q1.

**MEASURED** (`b1` `m2`; the exact certificate is a max-flow decision, not a greedy one — source →
edge with capacity 3 → its good extensions with capacity 1 → sink, feasible iff the flow is `3m`):
see [`out_b1_sequence.txt`](../code/adjacent_triples_7c78/out_b1_sequence.txt) for the table.
**UNDECIDED is reported as undecided.** Disjointness is sufficient and **not** necessary — the
statement permits overlapping runs — so a poset with no disjoint system is not a counterexample,
and counting it as one would be the error this document is most exposed to.

### §3.4 Q3 — THE RUN CONDITION IS NEARLY FREE; THE GRAY CODE IS NOT

**THE STRUCTURAL FACT (`U`, and measured).** In **any** walk in the BK graph, three consecutive
vertices differ by at most **two** swaps, and each swap flips exactly one incomparable pair. So a
run of three is **unanimous on every incomparable edge but at most 2**. Measured over **1 378**
runs of three consecutive vertices of found Hamiltonian paths: the maximum number of edges not
shared by all three is **exactly 2**. What is *not* free is that the shared orientation be the
**good** one.

**AND THE OBSTRUCTION IS SOMEWHERE ELSE ENTIRELY.** A Hamiltonian path in the BK graph **does not
always exist**: `b1` `m3` finds one at **111** posets, proves there is **none** at **6**, and
exhausts its search budget without a decision at **9** (`|L(P)| ≤ 60`, 2 skipped and counted).
**So Q3 can fail for a reason that has nothing to do with triples, edges, or `2/3`** — the
ordering it demands does not exist. Reported as `FP✗` for the obstruction: a finite population
exhibiting counterexamples, which is universal-strength for the claim *"a Gray code always
exists"*.

### §3.5 THE TRICK, IN THE FORM A CONSUMER WOULD WANT IT

**THE TRICK, SHARP.** For an incomparable pair `{x,y}` with `g_xy` extensions good for it out of
`N = |L(P)|`: **every** ordering of `L(P)` — however crafted, however adversarial — contains three
consecutive extensions all good for `{x,y}` **iff `g_xy > ⌈2N/3⌉`**. `U`, §3.2.

**THE TRICK, REPAIRED so no divisibility condition is needed.** `p_xy > 2/3` is not quite enough
(§3.2). What is enough at **every** `N` and every residue is

> **`p_xy > 2/3 + 2/N`.**

*Proof.* `g_xy > 2N/3 + 2` forces `g_xy ≥ ⌊2N/3⌋ + 3 ≥ ⌈2N/3⌉ + 1`, since `⌈2N/3⌉ ≤ ⌊2N/3⌋ + 1`. ∎
Checked at **every `(N, g)` with `3 ≤ N < 200`: 0 failures** (`b2` `t1`). ⚠️ **And it is honestly
unsatisfiable where the trick has no content:** at `N = 4` the repair demands `p > 7/6 > 1`, which
is correct — `N = 4, g = 3` is the counterexample — so the repaired form *says* the trick is empty
there instead of quietly failing.

**CRAFTING THE ORDERING BUYS NOTHING FOR THE GUARANTEE, and this is the finding of `b2`.** Because
the criterion is **universal over orderings**, a weak-Bruhat-refining ordering is guaranteed a good
run of three on **exactly** the edges an adversary is. Measured over **647** incomparable edges at
108 posets: the adversarial `G G B` ordering agrees with the criterion at **647 of 647**, and the
Bruhat-refining ordering happens to get a run at **608** — i.e. at 374 further edges — which is
**luck at that ordering, not a guarantee**. So *"perhaps it's an extension of the weak bruhat
order"* does not strengthen the trick.

**WHAT THE BRUHAT STRUCTURE DOES BUY, and it is a reason about the CONSUMER.** Measured (`b2` `t3`):
the ordering's bottom element is `e` itself at **108 of 108** posets, so the run at the very bottom
is good for **every** incomparable edge at once, for free, and all the content is in the runs
further up. And across **1 820** runs of three consecutive extensions the largest `inv_e` spread
inside a run is **1** — three consecutive extensions of a Bruhat-refining ordering are within one
inversion of each other. **`inv_e` is the currency `STATE.md:29` says a proof would be delivered
in**, so if the trick ever has a consumer, that locality is the property to reach for, not the
guarantee.

---

## §4. IS IT A REALIZABILITY FACT? — THE ANSWER THE TICKET REQUIRED

**NO, AND THE TICKET'S REASON FOR FILING IT HIGH DOES NOT SURVIVE.** `STATE.md:21` is explicit
that pair-marginal information is exhausted — `Op-Form` Claim 6.1 is an **equality** for what it
consumes — and that **every route below `1` must add a realizability fact**, a fact about which
combinations of pair-biases can actually co-occur in a real poset.

Score the four readings against that bar:

| reading | what it consumes about `P` | realizability content |
|---|---|---|
| **Q4** | nothing — permutation parity only | none; it is false for every `P` alike |
| **Q2** | `p_xy` and `\|L(P)\| mod 3` | **none.** One pair marginal plus an arithmetic residue. It constrains no *combination* of biases, so it adds nothing `Op-Form` Claim 6.1 has not already spent |
| **Q1** | `p_xy` at every edge, plus `\|L(P)\|` and the edge count `m` | **marginal.** Its certificates are counting arguments over the pair marginals *severally*; nothing in them forbids a joint profile that an abstract measure could carry |
| **Q3** | the **BK graph's** Hamiltonicity | **yes in kind, no in effect.** This is the one reading that names a structure an abstract measure does not have — and what the structure supplies is an **obstruction** to the claim, not a constraint on bias profiles |

| **the trick** | `p_xy` and `N`, and nothing else | **none**, for Q2's reason — and now confirmed against Daniel's own framing of it as a reusable device rather than a lever |

**So the observation is realizability-*flavoured* only at Q3, and at Q3 the structure works
against the claim.** That is the honest answer, and it is the opposite of the ticket's expectation
that *"a statement forced about the arrangement of `L(P)` itself is exactly the kind of fact that
constrains which pair-bias profiles are jointly achievable"*.

**WHAT WOULD HAVE MADE IT ONE, stated so the next attempt is not re-derived.** A claim of the form
`Pr[configuration] ≥ c > 0` **forced** by `δ(P) < 1/3` — a *production* statement, with the
hypothesis on the left and a lower bound on the right. Every true statement in this document has
the other sign: the hypothesis either **caps** a configuration probability (§5.2) or is consumed
as a **density** in a pigeonhole (§3.2). That sign is the reason none of them is a lever.

---

## §5. THE MISFILED READING — KEPT, BECAUSE IT IS TRUE AND BECAUSE §3.1 NEEDS IT

Measured under `pm-onethird`'s original framing, before his correction arrived. **None of it is
Daniel's observation** and it must not be cited as such. It is here because the ticket's standing
instruction is that facts are collected whether or not anything consumes them, and because §3.1's
last branch closes on §5.3.

### §5.1 The existential element-adjacency reading is true and the hypothesis does no work

For every poset and every `x ∥ y` there is a linear extension placing them at consecutive
positions, in **each** of the two orders — **0 failures over 33 290 incomparable pairs** at 3 243
posets (`n = 2…7` exhaustive over isomorphism classes, `n = 8` sampled 800 of 16 999, seed
20260812). Since both orders occur, the witness is `e`-aligned for **every** reference order at
once, so no bias hypothesis supplies the alignment. The failure count is **0 in every `δ` band
including `δ = 1/2`** — the maximally balanced posets — which is the measurement that shows the
`> 2/3` hypothesis contributes nothing (`a1` `m3`).

### §5.2 The bound family, and the sharpest member of it

For an incomparable pair let `E_xy = {σ ∈ L(P) : σ∘(x y) ∈ L(P)}` — the event that exchanging the
**values** `x` and `y` leaves a linear extension. Then

> **`min(p_xy, 1−p_xy) ≥ (1/2)·Pr[E_xy]`**, `U`, proved: on `E_xy` the value-exchange is a
> measure-preserving involution, so the two orientations split it exactly evenly.

**`FACTS.md` F1 is its `k = 2` slice** (adjacent ⟹ `E_xy`) and the misfiled triple reading is its
`k = 3` slice (inside a free consecutive triple ⟹ `E_xy`). Measured **strictly stronger than both
at 24 904 of 33 290 pairs**; 0 failures; maximum `Pr[E_xy]` observed `1`, attained. The `S₃`
symmetry of a free consecutive triple — all 6 orders exactly equinumerous, **0 failures over
16 672 triples** — **is implied by `mg-92e6`'s involution** and is not independent of it: the two
adjacent swaps inside the block generate `S₃` and each is `mg-92e6`-legal. The consecutive-triple
budget `Σ Pr[triple] = n − 2` **exactly** (0 violations, 3 243 posets) is the triple analogue of
F2's `n − 1`, and over pairwise-incomparable triples only it is `≤ n − 2`, **strict at 3 237 of
3 243** — F2's error class in a new index.

### §5.3 THE BOUNDARY CLASS, AND THE FINDING §3.1 CONSUMES

⚠️ **THE FROZEN CLASS IS EMPTY AT EVERY `n` AN ENUMERATOR REACHES**, and `a5` prints that `0` with
the reason attached so it cannot be re-quoted as a clean sweep: `δ < 1/3` **is** the counterexample
condition and the conjecture is verified to `n = 14` (`mg-33f5`). So the measured population is the
**boundary** class `δ(P) = 1/3` — every incomparable pair `≥ 2/3`-decided — which is non-empty and
enumerable. **31 posets, exhaustive over every isomorphism class `n = 3…8`.** On it:

- **every incomparable pair is ADJACENT in `e`** — maximum position distance **1**, not 2 (`a6` `m1`);
- **width `2` at every member, and ZERO 3-element antichains in the whole class** (`a6` `m2`);
- the cap `Pr[E_xy] ≤ 2δ = 2/3` holds at all 82 pairs and is **attained with zero slack**;
- `R2` — one extension whose consecutive 3-blocks cover every incomparable edge — is **false in
  general** (2 384 of 3 242 posets) and **true here, 31 of 31**, with a monotone `δ`-sweep behind
  it: 100 % → 47.3 % → 15.3 % → 2.3 % (`a6` `m4`);
- ⚠️ **30 of the 31 ARE ORDINAL SUMS.** Exactly **one** is primitive, and a minimal counterexample
  is primitive (`STATE.md:55`). **That is the scope limit of every figure in this subsection and it
  travels with them.**

**NOT.** ⚠️ The width-`2` collapse is **consistent with**, and weaker in kind than,
`STATE.md:154`'s **PROVEN** low-`δ` ⟺ bounded-width equivalence (`mg-c47a` Obs 3.1(a)/(b)). What is
new here is the sharper form — *adjacent in `e`*, not merely bounded width — and it is `FP` at
`n ≤ 8`, saying **nothing** above.

---

## §6. PREDICTIONS SCORED

`PREDICTIONS.md` was written under the misfiled premise, so P1–P12 are all about §5's object.
Scored anyway, because a prediction file that is quietly abandoned when the premise moves is worth
nothing.

| # | outcome |
|---|---|
| P1, P4, P6, P8 | **HELD** — and disclosed as reports at zero credit when filed |
| P2 | **HELD** — R1 true, hypothesis does no work, 0 failures in the `δ = 1/2` band |
| P3 | **HELD** — R2 false, smallest witness the 4-element antichain, exactly as predicted |
| P5, P7, P9, P10 | **HELD** — the converse fails at 1 102 pairs; the joint constraint holds; `E_xy` strictly beats both slices at 24 904 pairs; the "all aligned" reading is refuted by `mg-92e6` |
| P11 | **HELD, and for the corrected reading too** — not a new lever, §4 |
| P12 | **HELD** — boundary non-empty at every `n` from 3 to 8; frozen empty |
| **NOT PREDICTED, AND IT IS THE INTERESTING ONE** | that **R2 flips**: false in general, true on the boundary class. `PREDICTIONS.md` predicted only the unconditional half and had no expectation for the conditional one. `a6` exists because the measurement contradicted the shape of the prediction file, not because the file anticipated it. |
| **PREDICTED WRONGLY IN EMPHASIS** | P9 called `E_xy` "the sharpest member of this family". Under the corrected reading the family is not the subject at all, so the sharpening is a fact about `FACTS.md` F1's neighbourhood and **not** about Daniel's observation. |

---

## §7. WHAT THIS DOCUMENT DOES NOT DO

- **It does not decide whether the trick has a consumer.** Daniel's own framing is *"keep it in
  mind for later"*, and §3.5 records the property a consumer would reach for (`inv_e` spread `≤ 1`
  inside a Bruhat run) without proposing one. Nothing in this corpus currently consumes it.
- **It does not decide Q1.** Two certificates fire and the general case is open. The natural next
  step is whether `2N/3 ≥ 3m − 2` follows from frozen — i.e. whether a frozen poset's linear
  extension count grows fast enough against its incomparable-edge count. **That is a question
  about `log e(P)` against `m`, which is `STATE.md:158`'s untried entropy row**, and it is named
  here rather than attempted.
- **It measured nothing above `n = 8`,** and the `n = 8` layer is sampled for the `a1`–`a4` arms
  (800 of 16 999 classes, seed 20260812) and exhaustive for `a5`/`a6`.
- **It did not verify Hamiltonicity where the search budget ran out** — 9 posets, counted, and
  "could not tell" is not reported as "does not exist".
- **It ran no eigenvalue, no float, and no solver on any verdict path.**
