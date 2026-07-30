# Independent audit of mg-ebd8 / 714aceb — the locating exercise

**Auditor work item:** mg-d673. **Target:** `714aceb`,
`docs/OneThird-Landscape-Where-This-Lives.md` + `code/landscape_ebd8/`.
**Date:** 2026-07-30. **Instruments:** `code/landscape_audit_d673/`, `run_all.sh`, ~1.5 min.
**Not relayed to Daniel. STATE.md not edited.**

---

## VERDICT: **OVERSTATED, with 2 BROKEN.**

**The identifications hold.** pm-onethird redirected this audit mid-flight to the
expensive direction of error — *a too-generous "this is already known" makes us abandon
work that was actually new, and nothing downstream detects it*. I made that the primary
target and tested each identification as an **equality**, built from the published
definitions, with no shortcut through the repo's own description of its own objects.
All three survive, and two of them survive a stronger test than the target ran:

| identification | my test | result |
|---|---|---|
| `F(P)` = Brown §4.3's LRB of chains in `J(P)` | chains built in `J(P)`, product formed by **lattice joins and meets only** — never blockwise set intersection | bijection **0 bad**, products **0 bad of 936 261 pairs** to `n ≤ 5`, maximal chains ↔ linear extensions **0 bad**; and `J(P)` distributive **63/63**, so by Birkhoff §4.3's class and ours are the *same* class |
| `F(P)` = Brown §4.1's sign-condition subsemigroup `G` | braid arrangement **realised numerically**, sign vectors read off coordinates, `G = {F : σ_i(F) ≥ 0}` compared setwise with `F(P)` and the **Tits product** with the repo's product | **0 bad** on all 86 posets to `n ≤ 5`, all three columns. *This is the target's own pre-filed item 2, which it left unmeasured.* |
| `AC(P)` = the order-congruence lattice `O(P)` | `O(P)` built **literally from Czédli–Lenkehegyi**: `π = Ker f` for an order-preserving `f : P → Q`, searching **all labelled posets `Q`** — no acyclicity test, no topological sort, no reference to moves | **0 disagreements** on all 87 posets to `n ≤ 5` |

**And the mathematical core is confirmed by a route the target did not use.** The target
checked its Brown-Theorem-2 closed form against *the repo's own triangular solve* — both
sides being solutions of the same counting identity, so a shared misreading could not be
caught from inside. I checked it against the **actual transition matrix**: `dim ker(M − λI)`
in exact rational arithmetic. **0 bad** on all 16 classes at `n = 4` and 61 of 63 at
`n = 5`; the dimensions sum to `|L(P)|` every time, which also proves `M` diagonalisable.

**Every population reproduces from a disjoint rebuild**, certified against two external
sequences (A000112 posets, A000608 connected posets), with a canonical form that is a
minimum over the **full `S_n` orbit** — not `min()` over a frozenset, the shape that
silently returned labelled counts for isomorphism classes earlier in this arc:
`2, 5, 16, 63, 318` classes; `1, 5, 37, 397, 5757` moves; `4, 24, 206, 2353, 37029`
levels. And **the numbers the existing pipeline already carries** re-derive exactly:
**6197** faces (Hodge-Leverage Theorem L), **922 073** pairs, **7/16** and **49/63** join
failures (unified-gate row Q7), the note's §5a table **all fourteen rows**, and the note's
§5b eigenvalues under **all three published weightings** including the `w2` collision at
`11/32` with `dim ker = 2`.

**So the two BROKEN items are not in the locating.** They are both in material the ticket
explicitly forbade — *"Do not develop new mathematics — this is a locating exercise"* —
and they are the target's own pre-filed items 1 and 3. **Zero BROKEN in anything the
document locates, quotes or measures.** For the seventh time in eight generations, the
worst findings are outside the brief.

---

## TARGET ZERO — WHAT DID IT ADD BEYOND ITS BRIEF?

Enumerated first and treated as primary, per standing rule.

The ticket's prohibitions were explicit: **no publishability verdict, no novelty claim,
do not develop new mathematics, do not re-derive the two proved facts.** The document
honours the first two scrupulously (see "the risk that did not materialise", below). It
breaks the third in exactly three places, and **two of the three are the BROKEN items.**

| # | added beyond the brief | status |
|---|---|---|
| **Z1** | **The closed-form specialisation of Brown's Theorem 2 to the order cone** — translating `M_0` into a condition on blocks, and evaluating `\|μ(X,V)\|` as `∏(\|B\|−1)!`. Derived, not quoted; the document's own §6 item 3 says so. Promoted to the commit subject (*"Brown's Theorem 2 is STRICTLY SHARPER"*) and to §0's *"one place where the literature is ahead of the repo"*. | **BROKEN 1** |
| **Z2** | **The E8 Björner-submonoid claim** — that the greedoid band on the poset shelling antimatroid is *"a proper submonoid of ours"*. A derivation about a **different** monoid; not a location, and not measured. §6 item 1 says so. | **BROKEN 2** |
| **Z3** | **The P2 sign exponent** `μ(0̂,1̂) = (−1)^{n−1}·s`, derived from Jenča–Sarkoci's homotopy theorem via the reduced Euler characteristic rather than quoted. §6 item 5 says so. | **correct** — I re-derived it independently and it passes on all 402 posets where it is defined |
| Z4 | Importing KRS's *"graded and relatively complemented"* as available-and-not-in-the-repo; the §7 recommendation about amending the note. | in brief — the ticket asked for the delta and for what is left |

That Z1 and Z2 are the only two BROKEN items, and Z3 is the only other derivation, is
not a coincidence to be noted in passing. **The document derived three things and got two
of them wrong, while getting everything it located, quoted and measured right.** The
prohibition the ticket wrote was the correct prohibition.

---

## BROKEN 1 — the document's statement of the closed form is FALSE, and it is the sentence the commit nominates as its own sharpening

**The claim.** §0 item 2: *"Specialised to the order cone that reads `m_X = ∏_{B∈X}(|B|−1)!`
if every block of `X` is an **antichain of `P`**, and `0` otherwise."* Repeated in §0's
*"Brown's Theorem 2 names the spectrum-carrying levels outright — every block an antichain
of `P`"*, in §3.2's *"exactly the levels all of whose blocks are antichains of `P`, **which
is what `M_0` means**"*, and in the commit message.

**The defect.** `M_0` does not mean that. Brown's `M_0` is the set of flats meeting the open
region `U`, and a flat of the braid arrangement is *any* set partition. A partition all of
whose blocks are antichains of `P` need **not** meet the order cone: the quotient must also
be acyclic. The document drops that condition from every statement of the result.

**It is not a harmless abbreviation, because the "and 0 otherwise" ranges over all flats.**
Run as the document states it, the rule violates **Brown's own total-multiplicity
identity**:

```
  n=4:  1 of 16 posets fail       n=5:  10 of 63 posets fail
  first witness  P = {a<d, b<c},  |L(P)| = 6
      document's rule gives  sum m = 7      Brown's (10) requires 6
      spurious level:  ac|bd  with m = 1
          (both blocks are antichains of P; the quotient is NOT acyclic)
```

455 such spurious partitions exist at `n = 6`.

**The instrument is right and the prose is wrong.** `brown_theorem2.py`'s own docstring
carries the correct condition — *"every block is an ANTICHAIN of P, **and the quotient
P/pi is acyclic**"* — and its code ranges `X` over `AC(P)`, where acyclicity holds by
construction. So its measurement (0 bad of 318 classes / 37 029 levels) is sound and I
confirm it. **The measurement could not see the defect, because the code restricted to the
set on which the wrong statement happens to be right.** That is, precisely and in the
target's own words, *"a wrong derivation that happens to produce the right set"* — the
failure it pre-filed as item 3 and the one it named as this arc's signature.

**Why it matters operationally.** pm-onethird is holding a ticket on "Brown's Theorem 2 is
sharper". If that ticket is worked from the closed form **as the document states it**, it
returns wrong multiplicities on 1 in 16 posets at `n = 4` and 1 in 6 at `n = 5`. The fix is
one clause.

---

## BROKEN 2 — E8's *"a proper submonoid of ours"* is false, and contradicts the sentence beside it

**The claim.** L1 row H and the L2 table: Björner's greedoid band on the poset shelling
antimatroid is *"the sub-monoid of moves of the form (singletons…, rest) … For the antichain
this is the **free LRB**, support lattice Boolean … **A proper submonoid of ours**."*

The document flags the type mismatch itself — *"the elements are **words**, not ordered
partitions"* — and then calls the result a submonoid anyway. I built both and compared,
which is what §6 item 1 asks an auditor to do.

**Three findings, all measured:**

1. **The word → move map is never injective.** 0 of 63 posets at `n = 5`, 0 of 16 at
   `n = 4`, 0 of 5 at `n = 3`. A word of length `n−1` and its unique extension to length
   `n` give the *same* move. So the band is not a subset of `F(P)`; it **surjects onto**
   one.
2. **At the antichain the band is strictly LARGER than the whole of `F(P)`**, so it cannot
   be a submonoid of it — and this is the case the document names:

   | `n` | free LRB (A000522) | `\|F(antichain)\|` (A000670) |
   |---|---|---|
   | 2 | **5** | 3 |
   | 3 | **16** | 13 |

   The same table cell asserts *"this is the free LRB"* (true — my count matches
   `Σ n!/(n−k)!` exactly) and *"a proper submonoid of ours"* (impossible at `n = 2, 3`).
   The cell contradicts itself.
3. **"Proper" fails outright at `n = 2`:** the image is *all* of `F(P)`, 2 of 2 classes.
   It is proper for every poset at `n ≥ 3` (5/5, 16/16, 63/63).

**What is true**, and what the row should say: the map *is* a monoid homomorphism (63/63)
and its image *is* closed under the repo's product (63/63), so **a homomorphic image of
the greedoid band is a submonoid of `F(P)`, proper for `n ≥ 3`**. The abstract band's
support lattice *is* Boolean, `2^n` exactly (4, 8, 16, 32) — that half of the row is right.
The **"ADJACENT" verdict survives**, as the document predicted it would (*"Nothing else in
the document depends on it"*). This is a wrong reason for a right verdict.

**Scope of my instrument, stated because it bounds the finding.** I could not obtain
Björner's Theorem 4.15 or his product (4.8) in the original — arXiv's HTML rendering
truncates before §4.5. My construction uses the document's *own* identification (feasible
words of the shelling antimatroid; greedy product) and the standard fact that at the
antichain this is the free LRB, which my counts confirm. Finding 2 is
source-independent: it is arithmetic between two OEIS sequences.

---

## MAJOR — no false mathematics, but the claim outruns the evidence

**M1. Row Q licenses a "no" without enumerating the candidate space.** The table of empty
neighbourhoods says: *"the named programmes with that shape are **FI-modules /
representation stability** and **Deligne's `Rep(S_t)`**. Both are about stabilising or
interpolating the categories of `S_n`-representations themselves. **Neither has any contact
with this construction**."* Two things:

* This is the document's **one unhedged positive assertion about the literature**, and it
  is **not covered by E10 or E11** — both of which are booked as *"REPORT ON A SEARCH"*.
  Row Q asserts what the named programmes *are*, then answers no over that set of two. An
  impossibility claim built from a small enumerated candidate space was refuted by
  construction earlier in this arc.
* The enumeration is incomplete. Daniel's phrase is *"generalise the whole **Young lattice**
  paradigm to various combinatorial categories"*, and the named programme with exactly that
  shape is **towers of algebras / branching graphs** (Bergeron–Li; Bergeron–Lam–Li,
  *Combinatorial Hopf algebras and towers of algebras*) — where a tower of algebras yields
  a branching graph generalising Young's lattice, and the construction links directly to
  **dual graded graphs**, which is the document's own row L. It is not named anywhere.

  **I am not claiming it has contact.** I did not establish that either way, and saying so
  would be the same error in the other direction. The finding is about the candidate space,
  not the answer: row Q's "no" is licensed over a set of two that omits the closest match
  to the phrase it is answering.

**M2. L3's date rests on the weakest of its three supports.** L3 answers *"is the pairing
treated as a single paradigm?"* with **"The answer is yes, and it has been yes since
2000."** The 2000 date is Brown, and the Brown half is ledger row **E9**, whose own status
line reads *"READING OF A QUOTED SOURCE … **he does not spell it out in those words**"*.
Brown's §4.1 is stated at a generality that **covers** both ends — I verified this
directly, and it is a real and correct observation. But *covering* both ends is not
*treating the pair as a paradigm*, and the document's other two supports (MSS's memoir,
Bandelt–Chepoi–Knauer's COMs) date from **2015 and later**, not 2000. The bold headline is
stronger than the ledger row beneath it, and the ticket named this exact question as
potentially *"the finding"*. Same slip: *"the poset half is one of the three examples Brown
chose to write out"* — Brown presents the `x₁>x₂, x₃>x₄` lune as a lune in the braid
arrangement, not as the order cone of a poset. **The location is right; the claim about
treatment is a reading presented as a fact.**

**M3. "Strictly sharper" is the wrong word, and it is the word in the commit subject.**
pm-onethird asked directly. Sharper is a comparison, so I ran both sides: the repo's
triangular counting identity solved numerically, and Brown's closed form, at every level.

```
  n=5:  2 353 levels,  0 disagreements     n<=6 (target's own run): 37 029 levels, 0
```

**They agree everywhere, so there is no case where Brown's answer is better — it is the
same answer.** What Theorem 2 supplies that the identity does not is the answer *in closed
form*: the spectrum-carrying levels are named a priori (1 674 of the 2 353 levels to `n=5`
carry zero, and Brown names which without solving) rather than discovered by a solve. The
**document's own §0 says "strictly more informative"**, which is exactly right. The
**commit subject says "STRICTLY SHARPER"**, which is a bound word and is not. The
consequence pm-onethird is holding a ticket on is real but it is *"we can stop solving a
triangular system"*, not *"we have been getting weaker answers"*.

---

## MINOR

* **M4. The population arithmetic about its own instrument is wrong twice.** Ledger **E3**:
  *"two definitions agree setwise on all **405** classes at `n ≤ 6`"* — the target's own
  committed output runs `n = 2..6`, which is **404**. §6 item 5: P2 *"passes on **405**
  posets"* — P2 is `n/a` for `n < 3` and its own output says so, so it passes on **402**.
  405 is the count of *all* classes with `1 ≤ n ≤ 6`, which is neither test's population.
  Zero mathematics affected; this is the arc's standing location for BROKEN arithmetic —
  the landing's claims about itself.
* **M5. §6 item 6 mis-describes its own code, and points a future auditor at the wrong
  risk.** It says P2 implements Jenča–Sarkoci Definition 4.1 *"as **single** cyclic
  rotation of the word"* and worries that this would compute a coarser relation.
  `identify_lattice.py:316–320` loops `k = 1..n−1` — **all** rotations. The distinction is
  real and consequential, not pedantic: my first pass implemented the single-rotation
  version *as the document describes it* and it **disagreed with the Möbius function on 5
  posets to `n = 5`**. The document flagged a risk its code does not have and, in doing so,
  described away the reading that does fail. Safe direction; the code is better than its
  description.
* **M6. Under-reported populations.** *"Measured exhaustively at `n ≤ 5`: bijection 0 bad of
  **63** classes … **922 073** pairs"* — 63 and 922 073 are the `n = 5` **rows**. The `n ≤ 5`
  totals are **87** classes and **936 261** pairs. Conservative direction, but it is the
  same "which population is the claim about" slip as M4.
* **M7. §0 and E5 attribute the eigenvalue table and the `6×6` matrix to Brown §4.1.** The
  six chambers and the lune are §4.1; the table and the matrix are **§4.2**. The
  identification of the example with `P = {a<b, c<d}` is correct — I checked the six
  permutations `1234, 1324, 1342, 3124, 3142, 3412` are exactly the linear extensions.
* **M8. A prose/ledger status gap on the second "ours" item.** §0 states flatly *"It is
  Czédli–Lenkehegyi's theorem, from 1983"*, while the ledger books E6 as a **READING** and
  §6 item 4 admits *"I did not read … Czédli–Lenkehegyi … in the original"*. My I2
  instrument settles that the repo's `AC(P)` **is** the order-congruence lattice as that
  object is defined in the modern literature — that part is now measured, not read. It does
  **not** settle that Sturm 1971 or Czédli–Lenkehegyi 1983 state it; neither the target nor
  I went behind Jenča–Sarkoci's citation. Given that this sentence is the one asking
  pm-onethird to downgrade a repo contribution, the distinction between *the object is the
  same* (established) and *the 1983 paper says so* (a citation chain) should be visible in
  the document.
* **M9. "One place where the literature is ahead of the repo"** — the document then names a
  second (KRS's graded-and-relatively-complemented). Under-listing, harmless.

---

## THE RISK THE BRIEF NAMED, AND WHY IT DID NOT MATERIALISE

My original brief aimed at **a smuggled novelty claim**. I looked for one specifically:
every superlative in the document, every ledger row, every "not located". **There is no
smuggled novelty claim.** §5's `NOT CLAIMED` row is honest and complete; §2.1 says
*"stated as not located, which is **not** a synonym for new"* and repeats it in §7; the one
place novelty could leak — L3's *"one thing that is genuinely different about the second
instance"* — is hedged in its own sentence (*"That observation is the repo's; I did not
locate it in the literature, and per §2.1 that is a statement about my search"*).

**The over-claiming in this document runs the other way — toward "known", not toward
"new".** pm-onethird's mid-flight redirect was correct, and it is the more expensive
direction here for the reason given: a false novelty claim gets caught, a false
already-known does not. M1 and M2 are both in that direction; so, in a narrow sense, is
M8. **None of them is a false identification.** The three that matter — Brown §4.1,
Brown §4.3, and `O(P)` — I tested as equalities from the published definitions and they
hold. The document earned them.

---

## SCOPE AND OBLIGATIONS

Clean. The document does not edit `docs/OneThird-Semigroup-Walk-Family-Note.md`, does not
touch `λ₂`, `Δ_AT`, roadmap pricing or the mg-8fd1 gate's conclusions, states no
publishability verdict, and was not relayed to Daniel. Its §7 correctly leaves the
note-amendment call to pm-onethird. `run_all.sh` reproduces; the committed outputs match a
re-run.

**The one thing pm-onethird should act on before anything else:** the closed form as
written in §0 and §3.2 is missing *"and the quotient is acyclic"*. Everything downstream of
it — including the ticket being held on "Theorem 2 is sharper" — should use the condition
in `brown_theorem2.py`'s docstring, not the one in the prose.

---

## MY INSTRUMENTS

`code/landscape_audit_d673/`, pure Python 3, no third-party imports, sharing no code with
`code/landscape_ebd8/` (the target), `code/semigroup_note/`, `code/face_geometry/`,
`code/unified_gate_8fd1/` or `code/hodge_leverage/`.

| file | what it establishes |
|---|---|
| `audit_populations.py` | posets up to iso with a **full-orbit** canonical form, certified against A000112 and A000608; `\|F(P)\|`, `\|AC(P)\|` **two independent ways**, join/meet closure, Möbius vs Jenča–Sarkoci |
| `audit_spectrum.py` | the closed form against `dim ker(M − λI)` on the **actual matrix** in exact rationals; the note's §5a and §5b tables re-derived |
| `audit_e6_e8_m0.py` | E6 from a **numeric realisation** of the braid arrangement; `M_0` against Brown's total-multiplicity identity; Björner's band built and compared |
| `audit_identifications.py` | Brown §4.3 with **lattice-only** products; Czédli–Lenkehegyi's `O(P)` from the published definition; "sharper" run as a two-sided comparison |
| `audit_addenda.py` | JS Example 3.7; the populations the document's own claims are about; 922 073; free LRB vs ordered Bell |
| `diag_p2.py`, `diag_p2_cross.py` | forensics for the P2 disagreement. **No verdict rests on these** — `diag_p2_cross.py` imports the target's module and is not run by `run_all.sh` |

Sources I read myself rather than taking from the target: Brown `math/0006145` §4.1–4.3
(the §4.3 passage, the *"`G` is a subsemigroup of `F`"* sentence, Theorem 2's statement,
the `ℝ⁴` lune example, and the Diaconis attribution — **all five quotations in the document
check out verbatim**, with the §4.1/§4.2 location slip noted at M7); Jenča–Sarkoci
`1112.5782` abstract and main theorem. I did **not** obtain Björner's Theorem 4.15 or
Aguiar–Mahajan; the target did not either and says so.
