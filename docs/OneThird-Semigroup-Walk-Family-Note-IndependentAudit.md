# Independent audit of the semigroup walk family note (mg-6016)

**Auditor:** mg-66a6, pre-filed before mg-6016 committed. **Target:**
`docs/OneThird-Semigroup-Walk-Family-Note.md` at `ac5c51e` + `3c9d930` — the expository note that
**goes to Daniel**, with no referee downstream of this audit.
**Instruments:** `code/semigroup_note_audit_66a6/` — `audit_lib.py` (posets, moves, the product, the
action, levels, multiplicities, eigenvalues, exact rational rank, the AT graph, signs, isomorphism
classes, all rebuilt from the definitions), `audit_worked_example.py`, `audit_antichain.py`,
`audit_sweeps.py`, `audit_theorem.py`. **352 checks.** Shares no code with `code/semigroup_note/`
(the artefact under audit), nor with `code/face_geometry/` or `code/hodge_leverage/`. Pure Python 3,
45 s, all four `out_*.txt` regenerate byte-identically.

The author's numbers were **not** consulted while recomputing: each script hard-codes the note's
claimed values as expectations and compares only at the end.

## VERDICT: **CONFIRMED — 0 BROKEN mathematics, 1 BROKEN SENTENCE, and the status error runs the OTHER WAY**

Every number in the worked example reproduces from a disjoint rebuild, including the whole §5a
multiplicity table (both columns), all eighteen eigenvalues under the three weightings, and
`dim ker(M − λI)` against the actual 6 × 6 matrix in exact rationals. The demonstration that is the
note's entire point — change the probabilities, the level→multiplicity table does not move — is
**arithmetic, not assertion**, and it survives a **fourth** weighting I added supported on all 26
moves. The action is stated **correctly**, and the correction to pm-onethird's wrong "monotone
refinement" version is **visible, not silently fixed**. Scope is clean.

**The one unverified claim is SETTLED and it is TRUE**, and I settled it without using the note's
route: I rebuilt the braid arrangement from its own definition (realisable sign vectors) and checked
that the note's product **is** the Tits product and the note's action **is** the Tits chamber action,
over all 292,681 move pairs at n = 5, with two controls that bite. So on an antichain the family is
the Bidigare–Hanlon–Rockmore / Brown–Diaconis braid hyperplane-walk family as an **identity of
families**, and both named specialisations check against independently-known spectra.

Two things must be fixed before this reaches Daniel.

| | finding | class |
|---|---|---|
| **F1** | §5b: *"Under `w2`: `1,1,1,2` summing to 6 of 6."* There are **five** distinct eigenvalues under `w2`, and the four numbers printed **sum to 5**. The instrument prints five dim-ker lines (`1,1,1,1,2`); the prose dropped one. This is the single sentence that certifies §5 against the matrix, in a note whose premise is that a reader checks the arithmetic. | **BROKEN** |
| **F2** | §9 line 6 and §8: *"ours is the identification plus the acyclic-cut description of the levels, **verified to five elements and not proven in general**."* **Both are elementary theorems for every `n`.** Proofs supplied below and verified constructively at n = 6, 7, 8 — where the note has no evidence at all. The note **understates its own contribution**, and the same wrong status is already in pm-onethird's 09:33Z mail to Daniel. | **MAJOR (mispricing)** |
| **F3** | §7's *"(2, 5, 9, 14 distinct eigenvalues)"* holds only for the **unstated** weights `w_i ∝ i`. For generic `w_i` the counts are **2, 5, 12, 27**; the reduction is caused by exactly the level-collision effect §5c is about, unremarked here. Not reproducible by the reader. | **MINOR** |
| **F4** | §1 promises *"Six objects, and no others. Everything later is built from these … That is all six. There is no seventh."* §6, inserted later under R6, then uses the group algebra, `Δ_AT`, the twist `E`, `ONE`, `SGN`, sign-imbalance — and **`L^rel` is never defined**. The stated audience cannot follow §6. §1's promise was not updated when §6 was added. | **MINOR (audience test)** |
| **F5** | §8 attributes the counting identity, RHS included, to Brown. Brown's relation carries a **chamber count** on the right; `Π_B |L(P|_B)|` is an identification of ours (verified below). Credit given away, not taken. | **MINOR** |
| **F6** | Runtime claimed *"about 45 seconds"* in the note header and `run_all.sh`; measured **18.6 s**. | **TRIVIAL** |

---

## F1 (BROKEN) — the sentence that certifies §5 does not add up

§5b, immediately after the eigenvalue table:

> **Checked against the actual 6 × 6 matrix, in exact rational arithmetic**, by computing
> `dim ker(M − λI)` for each predicted `λ`. Under `w1`: dimensions `1,1,1,1,1,1`, summing to 6 of 6 …
> Under `w2`: `1,1,1,2` summing to 6 of 6. Under `w3`: `1,1,1,1,1,1` summing to 6 of 6.

Recomputed from the definitions. Under `w2` the six spectrum-carrying levels evaluate to

```
    ac|bd = 11/32   ac|b|d = 13/32   ad|b|c = 11/32
    a|bd|c = 17/32   a|bc|d = 9/16    a|b|c|d = 1
```

— **five** distinct numbers, because `ac|bd` and `ad|b|c` collide at `11/32` (which §5c then discusses
by name). The exact nullities are

```
    dim ker(M - 11/32 I) = 2      dim ker(M - 13/32 I) = 1
    dim ker(M - 17/32 I) = 1      dim ker(M -  9/16 I) = 1
    dim ker(M -      1 I) = 1                      total = 6 of 6
```

The note's own instrument prints exactly those five lines (`note_check_output.txt:183-187`). The prose
dropped the `13/32` entry, so the list it shows is `1,1,1,2` = **5**, asserted to sum to **6**.

The mathematics is right and the total is right. What is wrong is a sentence a reader will check by
adding four small numbers — and the reader is the person who caught the last error in this thread from
a prose description alone. **Fix: `1,1,1,1,2`.**

---

## F2 (MAJOR) — both of the note's "ours" items are theorems, and §9 says they are not

§8 splits credit carefully, and then:

> - **Ours.** Two things, both modest. First, the **identification**: that this construction …
>   satisfies the hypothesis … Second, the **description of the commitment levels** as exactly the
>   partitions with acyclic quotient …
> - **The status of the second one.** It is **verified exhaustively only to five elements** … It is
>   **not proven in general**. Nothing in this note should be read as saying otherwise.

and §9 line 6 applies the caveat to **both**:

> ours is the identification plus the acyclic-cut description of the levels, verified to five elements
> and not proven in general.

Both are elementary theorems for every `n` and every `P`. Here are the proofs.

**Theorem 1 (closure — "the identification").** Let `x = (B_1..B_k)` and `y = (C_1..C_l)` be
`P`-compatible. A block of `x·y` is a non-empty `B_p ∩ C_q`, and its index in `x·y` is the rank of
`(p,q)` in lexicographic order. Take `i < j` in `P`, with `i ∈ B_p ∩ C_q` and `j ∈ B_p' ∩ C_q'`.
Compatibility of `x` gives `p ≤ p'`; of `y` gives `q ≤ q'`. Hence `(p,q) ≤ (p',q')` lexicographically,
so `index(block of i) ≤ index(block of j)`. So `x·y` is `P`-compatible. No hypothesis on `n`. ∎

**Theorem 2 (the acyclic-cut description).** For a partition `X`, let `Q(X)` be the quotient digraph:
one node per block, an arrow `B → B'` (`B ≠ B'`) whenever some `i ∈ B` has `i < j` in `P` for some
`j ∈ B'`.

*(⟹)* Let `X = supp(x)` for `P`-compatible `x = (B_1..B_k)`. Distinct blocks have distinct indices, and
an arrow `B_p → B_q` forces `p ≤ q`, hence `p < q`. Every arrow strictly increases the index, so a
directed cycle would give `p < p`. `Q(X)` is acyclic.

*(⟸)* Let `Q(X)` be acyclic. Take any topological order of its nodes and let `x` be that ordered set
partition. If `i < j` in `P` then either they share a block (equal indices) or there is an arrow
`block(i) → block(j)`, which the topological order sends to `index(block(i)) < index(block(j))`. So `x`
is `P`-compatible, and `supp(x) = X` by construction. ∎

Both directions are verified **constructively** in `audit_theorem.py` — the (⟸) witness is built and
checked to be compatible with the right support — exhaustively over every labelled poset to n = 5
(148,742 acyclic partitions at n = 5), and then on **random posets at n = 6, 7 and 8**, where beyond
n = 5 the set equality is tested in the equivalent form it reduces to: *is some ordering of `X`'s blocks
`P`-compatible*, brute-forced over block orderings with the acyclicity criterion nowhere in sight.
`7735 / 7735`, `10536 / 10536`, `14135 / 14135`, zero disagreements. The control bites: the worked
example's `{a,d}|{b,c}` yields no witness and no compatible move.

Closure at n = 6, 7, 8 likewise: 0 failures over random posets × 4,000 random move pairs each, together
with both band identities.

**Why this matters rather than being a pleasant surprise.** §8 exists to price what the programme owns.
As written it prices two elementary lemmas as an unproven pattern observed in small cases, and §9 — the
summary line, which is what a busy reader retains — repeats it. Daniel is funding this; being told
"unproven empirical regularity" when the truth is "five-line proof" misprices the asset downward. The
same status is in pm-onethird's 09:33Z mail (R4 item 6), so a correction is owed on that channel too.

Two caveats, in fairness. First, the sentence was *true of mg-6016's evidence* — they had not found a
proof. It is the presentation as a durable property of the result ("It is **not proven in general**")
that misinforms. Second, if more than the set equality is intended — the *lattice* structure of the
supports — the note does not say so; that too follows from the theorems above, and
`supp(x·y) = supp(x) ∧ supp(y)` with the levels closed under common refinement is verified to n = 4.

---

## F3 (MINOR) — the Tsetlin eigenvalue count is weight-specific and the weight is not stated

§7:

> The commitment-level machinery reproduces this exactly for `n = 2,3,4,5` (2, 5, 9, 14 distinct
> eigenvalues) …

I reproduce `2, 5, 9, 14` — but only after discovering by inspection of the instrument that the weights
are `w_i ∝ i`. The number of **distinct eigenvalues** of the Tsetlin library is not a structural
invariant: it is the number of subsets `S` with `D(n−|S|) > 0`, namely **2, 5, 12, 27**, reduced to
2, 5, 9, 14 only because subset sums of `{1,…,n}` collide (`{1,4}` and `{2,3}` both give 5, and so on).

So the parenthetical reports a collision-contaminated count, unremarked, three sections after §5c
carefully explains that *numbers* collide while *levels* do not. The check itself is sound — the
level→multiplicity aggregation matches the classical derangement spectrum exactly at n = 2..5 and
against the matrix at n ≤ 4 — it is only the advertised size of it that is unreproducible. **Fix: state
the weights, or drop the parenthetical.**

---

## F4 (MINOR — this is the audience test) — §6 breaks §1's promise, and `L^rel` is undefined

R3 set the calibration: *a small number of precisely defined objects*, and *"if you find yourself with
more than about six defined terms, cut objects rather than definitions."* §1 delivers exactly that, and
commits to it:

> Six objects, and no others. Everything later is built from these. … That is all six. There is no
> seventh.

§§0–5 and 7–9 honour it. I read them as the stated audience — someone who knows what a poset and a
linear extension are and nothing else — and they follow start to finish; §5's arithmetic is genuinely
pencil-reproducible (I did most of §5a and all of §6's sign arithmetic by hand before running anything).
This does **not** read as a paper. That is the note's main achievement and it should be said plainly.

§6, inserted later under R6, breaks the promise. It introduces the group algebra of the symmetric group,
the span of `L(P)`, the adjacent-transposition graph, `Δ_AT`, the orientation twist `E`, `ONE`, `SGN`,
the sign-imbalance and sign-balancedness — and

> `L^rel`, the top relative Laplacian from the homological side,

is **never defined**, in a section whose conclusion ("the sign-weighted sum spans the kernel on the
homological side") is *about* it. A reader with the stated background cannot evaluate §6; they can only
take it. Two smaller instances of the same: "the compression of the Coxeter element", and §6(b)'s *"the
answer to your question is the first of your three options"* — a dangling reference to three options
that appear nowhere in the note, in the document that is supposed to be the durable written-down version.

None of this is wrong. It is a density defect at exactly the place R3 said density is a defect, and the
cheap fix is one paragraph defining `L^rel` operationally plus deleting the promise in §1 (or moving §6
behind a marked "this part assumes the homological side" line).

---

## F5 (MINOR) — the counting identity's right-hand side is ours, credited to Brown

§8: *"The diagonalisation theorem — that (i) and (ii) plus a weight give a diagonalisable transition
matrix with eigenvalue = total probability of the moves at or below a level, and multiplicities
determined by the counting identity — is **standard**."*

Brown's multiplicity relation carries a **chamber count** on the right. Writing that count as
`Π_B |L(P|_B)|` is a specialisation to this band: for any move `x` with `supp(x) = X`, the set `x·C` of
orderings reachable by `x` has exactly `Π_B |L(P|_B)|` elements. Verified for every move of every
labelled poset to n = 4 (4,399 moves at n = 4), 0 failures. Small, and it errs by giving credit away —
but §8 is the section whose job is exactly this accounting.

---

## What stands, and it is the bulk

**Target 1 — the arithmetic, recomputed independently.** All of it, from the definitions:

* 6 orderings, and they are the note's six; 26 of 75 ordered partitions compatible, with the block
  profile 1/7/12/6, and each of the four lists is exactly the note's; `(b|acd)` and `(ad|b|c)` correctly
  excluded.
* The complete `(ac|bd)` step table including the `cdab → cadb` row the note walks through in prose.
* The four-line commitment-destroyed trace `abcd → acbd → cdab → acdb`, plus: `(a|c|bd)` puts `a` before
  `c` from **every** start, `(cd|ab)` puts `c` before `a` from every start, all six orderings mutually
  reachable, exactly one move fixing all six, **0 absorbing orderings**.
* The action lands in `L(P)` 156/156 and agrees with the product against the ordering-as-move 156/156.
* Band identities on the example: 26/26, 676/676, 676/676 closure, 17,576/17,576 associativity.
* 14 of the 15 partitions are levels; the missing one is `{a,d}|{b,c}`; the cycle argument is correct and
  it is the **only** cyclic partition. The entire level→moves table matches, all 14 rows.
* **The whole §5a table, both columns** — the `Π_B |L(P|_B)|` column and the *"levels refining it"* sets,
  row by row — the multiplicities, the sum 6 = |L(P)|, the six nonzero levels, and the hand-worked
  `ac|bd` row (`2 × 2 = 4`, three proper refiners, `m = 1`).
* All eighteen eigenvalues in the §5b table, as exact rationals including the four bolded
  simplifications; the hand-worked `λ(a|bd|c) = 13/32` **and** that exactly the four named moves
  contribute; `dim ker` against the actual 6 × 6 summing to 6 of 6 under all three weights (so
  diagonalisable), with the per-eigenvalue multiplicities matching the level prediction one by one.
* The sharpest consequence: `w(abcd)` is a partial sum sitting at six levels of multiplicity 0 and
  `dim ker(M − w(abcd)I) = 0` in the actual matrix under **all three** weights.
* The `11/32` collision under `w2` is the **only** collision, and `w1`, `w3` have six distinct values.

**The w-independence demonstration is real.** It is the note's whole point, so I attacked it rather than
confirming it: I added a **fourth** weighting supported on **all 26 moves** (the note's three are
supported on eight). The eigenvalues move to `5/54, 17/108, 11/54, 13/54, 31/108, 1`; the
level→multiplicity table is **byte-identical**; the predicted multiplicities again account for all 6
dimensions of the actual matrix. And the multiplicity solve provably cannot see `w` — its inputs are
counts of linear extensions of induced subposets.

**Target 2 — SETTLED, and TRUE, by a route the note does not use.** I did not accept "moves = faces of
the braid arrangement" as a dictionary. I rebuilt the arrangement from its definition: faces are the
realisable sign vectors `sgn(x_i − x_j)`, enumerated from integer points, giving **1, 3, 13, 75, 541**
faces at n = 1..5 with no ordered set partition in sight; chambers are the zero-free sign vectors, `n!`
of them. The classical product is the **Tits product** `(xy)_H = x_H if x_H ≠ 0 else y_H` — the
definition BHR and Brown–Diaconis use, which mentions no partitions. Then:

* the note's product **is** the Tits product, 0 bad of 292,681 pairs at n = 5;
* the note's action `x·c` **is** the Tits chamber action, 0 bad of 1,800 at n = 4;
* two controls bite: the test detects the **order** of the product (it fails against `tits(y,x)`), and a
  bijection perturbed by a single transposition fails it.

So the map `w ↦ transition matrix` has the same domain and the same values on both sides: it is the
**same set of Markov chains**, an identity of families, not an inclusion. §7's claim is confirmed as
written, and the note is right that it is *stronger* than the belief pm-onethird sent Daniel (which named
only move-to-front / Tsetlin, i.e. one weight).

The **named** specialisations are the right ones:

* **Tsetlin / move-to-front.** Eigenvalue `Σ_{i∈S} w_i` with multiplicity `D(n−|S|)`, with derangements
  brute-forced independently (`1,0,1,2,9,44`); the level machinery reproduces the value→multiplicity map
  exactly at n = 2..5 and `dim ker` matches it at n ≤ 4, total `n!`.
* **Inverse GSR `a`-riffle shuffle.** From the labelling procedure alone: the induced law is exactly
  `w(x) = C(a, #blocks)/a^n`; `λ_X = a^{|X|−n}` on every level, n = 2..5, a = 2,3; the aggregate
  multiplicity at `|X| = m` is the unsigned Stirling number `c(n,m)` (checked against brute-force cycle
  counts); and at n ≤ 4 a transition matrix built **only** from "label i.i.d., stably sort" is *equal*
  to the semigroup matrix, entry for entry.
* The boundary is not oversold: my own exact span tests give **yes / no / no / no** for
  random-to-top / top-to-random / random transpositions / lazy adjacent transpositions at n = 3 and
  n = 4, matching the note's table. The logic is right — span membership is necessary for family
  membership, so a "no" is decisive.

**Target 3 — the action is correct and the correction is visible.** §0 leads with it, quotes Daniel
verbatim, and explains *why* refinement would have been absorbing rather than merely asserting that it
was wrong. §1.3 states the action precisely and separates what the move decides from what it copies.
§2 adds *"Neither identity says, or implies, that information only accumulates"* — closing the specific
door the wrong version came through. §9 line 1 repeats it and concedes the objection was right. Nothing
is silently fixed. And the correction is backed operationally, not just verbally: 0 absorbing orderings,
all six mutually reachable, a commitment made by one move and destroyed by the next.

**Target 4 — no upgrade anywhere.** This is the failure mode the brief anticipated and it does not
occur. I checked every sentence that could be read as a general claim, the §4 blockquote, the §2 table's
"not run" cells, and all six summary lines: wherever the n ≤ 5 scope is claimed it is stated, and §4's
general-looking blockquote is caveated in the next line. The defect is F2, in the opposite direction.

**Target 6 — scope clean.** No new mathematics beyond R6's explicit authorisation; §6 stops at the
one-line calculation and its immediate consequences and flags sign-balance as a different ticket. The
conjecture pricing is **pointed at**, not restated and not argued with (§8: *"This note does not
re-argue any of it — it is settled and priced in `docs/roadmap.md`"*). And the R4 obligation was
discharged properly: mg-6016 mailed pm-onethird at 09:11Z naming both places the note goes beyond the
09:33Z mail to Daniel, left the Daniel channel to pm-onethird, and relayed nothing.

**Every exhaustive sweep reproduces**, from independent enumeration: 1/3/19/219/4231 labelled posets and
1/2/5/16/63 isomorphism classes (canonicalised by sorted tuples — the frozenset-`min` trap mg-6016
self-reported is not present here); 7/17/43, 121/865/6949, 4399/109121, 5757/922073 band checks with 0
failures; supports == acyclic partitions on all 4,231 labelled posets at n = 5; the sign census
1/3/11/44 balanced against 1/2/5/19 not, with `Δ_AT·ONE = 0` and AT-connectivity on **every** class to
n = 5; the boundary counts 0/2/11/55 provably-not with 1 vacuous and 1/2/4/7 undecided; and the
antichain's 1 usable move supplying 0 of 12/72/480 needed edges.

**§6's arithmetic is right, by hand and by machine.** Inversions `0,1,2,2,3,4`; signs `+ − + + − +`;
imbalance `+2`; `E·ONE = SGN` and `E·SGN = ONE`; `Δ_AT·ONE = 0`, `Δ_AT·SGN = (2,−6,4,4,−6,2)`,
`L^rel·SGN = 0`, `L^rel·ONE = (2,6,4,4,6,2)`; both kernels 1-dimensional; `⟨ONE,SGN⟩ = 2`; the projection
`(1/3)·SGN`. The R6 conclusion — the twist exchanges the plain and the sign-weighted sums, so Daniel's
element is the kernel on the **graph** side — is correct, and refuting pm-onethird's own flagged
derivation in the note rather than quietly is the right call. One nit: *"A chain has one linear extension,
so its imbalance is `1`"* is labelling-dependent (the same chain labelled downwards gives `−1`), four
lines before the note itself flags labelling-dependence.

**Instrument.** `note_check_output.txt` regenerates byte-identically; `note_check.py` has no import of
`face_geometry` or `hodge_leverage` and no `sys.path` manipulation, so the "shares no code" claim holds.

---

## Actions

1. **mg-6016 / pm-onethird, before sending:** fix F1 (`1,1,1,1,2`). One character class of error, but it
   is in the certification sentence and it does not add up.
2. **pm-onethird:** F2. Add the two proofs (they are five lines each, above) and rewrite §8's third
   bullet and §9 line 6. Then send Daniel the corresponding correction to the 09:33Z mail, which carries
   the same understated status. The note's contribution is larger than the note says.
3. **pm-onethird:** F4 is the audience-test finding and the one Daniel's own instruction bears on
   directly. Define `L^rel`, or fence §6 off as assuming the homological side, and drop §1's "no seventh"
   promise, which §6 falsified.
4. **Optional:** F3 (state the Tsetlin weights), F5 (one clause moving the counting identity's RHS from
   Brown's column to ours), F6 (runtime).
5. **Not for Daniel from me.** Raw verdict to pm-onethird; I have relayed nothing to Daniel and have not
   sent the note.
