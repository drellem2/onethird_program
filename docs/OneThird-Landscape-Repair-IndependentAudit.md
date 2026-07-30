# Independent audit of the mg-1953 repair (`6b1eacf`)

**Work item:** mg-3b51. **Target:** mg-1953 / `6b1eacf`, the repair of mg-ebd8's derivations in
`docs/OneThird-Landscape-Where-This-Lives.md`. **Date:** 2026-07-30.
**Instrument:** `code/landscape_repair_audit_3b51/`, `run_all.sh`, ~5 min, pure Python 3,
**sharing no code with the target, with mg-ebd8's instruments, or with mg-d673's**, reading
**none** of mg-1953's committed outputs and executing **none** of its scripts.

---

## VERDICT

**THE REPAIR HOLDS. All four substantive fixes are correct, and every number mg-1953 writes
into the document reproduces exactly from an instrument that takes a different route at every
step. 0 BROKEN. 4 MINOR, of which 2 are coverage observations rather than errors.**

The specific thing this audit was filed to check — *is the acyclicity fix exercised where it
can fail, or has the repair reproduced the original defect one level up?* — comes back
**yes, it is exercised there**, and the repair's own instrument ranges `X` over all flats
exactly as it says. I reproduced the defect, the witness, and all three counts from a disjoint
route, and then took the statement one order further than mg-1953 did.

**The headline finding is small and is about the repair's control, not its mathematics.**
mg-1953's `R1d`, billed as *"the control that must fire"* and as **demonstrating** that
restriction to `AC(P)` is what hid the defect, **cannot fail**: on `AC(P)` the original rule
and the repaired rule are the *same set of flats* by definition. The fact it asserts is true
and important; its evidential billing is one notch too strong. That is finding **A1** below.

**Read this next to what it upholds.** mg-1953 was handed four fixes and a standing warning
that the arc's failure mode is material beyond the brief. It executed all four, changed no
locating status word it was not told to change, left the document's headline and `NOT CLAIMED`
row untouched, and added **exactly one** correction outside both its ticket and mg-d673's
findings — an arithmetic fix to the document's own citation (*"thirty years old"* for a 2000
paper → *"twenty-six"*), which is **right**. After seven consecutive generations of
beyond-brief findings, that is the cleanest scope discipline this arc has produced.

---

## WHAT I REPRODUCED, AND HOW THE ROUTE DIFFERS

Every number below is from `code/landscape_repair_audit_3b51/`. Where mg-1953 makes a
representation or algorithm choice, I make the other one, so agreement is evidence rather than
a shared bug.

| step | mg-1953 | this audit |
|---|---|---|
| poset carrier | frozenset of strict pairs | packed reachability bitmasks |
| poset enumeration | filter the `2^C(n,2)` transitively closed upper-triangle subsets | extension by a new **maximal element** over an order ideal |
| **"does the flat `X` meet the open cone `U`?"** | exhaustive search over the `\|X\|!` block orderings | **numeric construction with a certificate on both sides** — longest-path potentials, and the constructed point **verified** against every defining equation of the flat and every defining inequality of `U`; on the negative side an **exhibited directed block cycle**, whose strict inequalities sum to `t < t` |
| linear extensions | filter all `n!` permutations | DP over order ideals |
| multiplicities | — | the repo's triangular identity `Σ_{Y refines X} m_Y = ∏_B \|L(P\|_B)\|`, rebuilt from the identity |

The two decision procedures for *"`X` meets `U`"* are both implemented here and
**cross-validated flat by flat** — `0` disagreements over every flat of every poset to `n ≤ 5`
(`selftest.py`). `AC(P)` is likewise computed twice, as the acyclic-quotient flats and as the
supports of the `P`-compatible ordered set partitions: `0` posets disagree.

Enumeration certified against **A000112** (`1, 2, 5, 16, 63, 318`), **A000110**, **A000670**,
**A000522**. `selftest.py` carries **139 assertions** and exits non-zero on any failure — it
caught one arithmetic slip of my own while I was writing it (§ *What I could not establish*).

---

## R1 — THE ACYCLICITY REPAIR. CONFIRMED, AND CHECKED WHERE IT CAN FAIL.

### The counts, from my own instrument

| `n` | classes | flats | original rule ≠ `M_0` | repaired rule ≠ `M_0` | posets where the original breaks `Σ m_X = \|L(P)\|` | **spurious flats** |
|---|---|---|---|---|---|---|
| 2 | 2 | 4 | 0 | 0 | 0 | 0 |
| 3 | 5 | 25 | 0 | 0 | 0 | 0 |
| 4 | 16 | 240 | **1** | 0 | **1 of 16** | **1** |
| 5 | 63 | 3 276 | **10** | 0 | **10 of 63** | **18** |
| 6 | 318 | **64 554** | **101** | 0 | **101 of 318** | **455** |

**1 of 16, 10 of 63, 101 of 318, and 455 spurious flats at `n = 6` — all four exactly as the
document states**, and `64 554 = 318 × 203` flats is right. The `n = 5` spurious count (18)
appears in mg-1953's self-test but not in the document; it also matches.

### The witness, reproduced on the auditor's own labels

The brief asked me to reproduce **mg-d673's** witness, not mg-1953's relabelling of it:

```
P = {a<d, b<c}   |L(P)| = 6
  ORIGINAL rule  sum_X m_X = 7    (Brown's identity requires 6)   MISMATCH
  REPAIRED rule  sum_X m_X = 6                                     ok
  spurious flat  ac|bd   m = 1   blocks antichains: True   in AC(P): False   meets U: False
     NO-certificate from the constructive test: block cycle 1 -> 0 -> 1
```

**The old rule sums to 7 where Brown's identity requires 6, on the level `ac|bd`** — the
auditor's witness, on the auditor's labels, found independently. mg-1953's own instrument
reports the same class under a different labelling (`P = {a<c, b<d}`, flat `ad|bc`); I ran that
labelling too and it also sums to **7**. Both are the two-disjoint-2-chains class, and it is the
**unique** `n = 4` failure (1 of 16) with no failure at `n ≤ 3`, so *"smallest witness"* is right.

### Is the fix exercised OUTSIDE `AC(P)`? Yes — and necessarily so.

Every flat on which the two rules disagree, split by region:

| `n` | disagreeing flats | inside `AC(P)` | **outside `AC(P)`** |
|---|---|---|---|
| 4 | 1 | 0 | **1** |
| 5 | 18 | 0 | **18** |
| 6 | 455 | 0 | **455** |

`100%` outside, at every `n`, and this is a theorem rather than luck: `{antichain blocks}`
intersected with `{acyclic quotient}` **is** `{antichain blocks and acyclic quotient}`, so a
check confined to `AC(P)` cannot distinguish the two rules at all. mg-1953's
`closed_form_outside_AC.py` ranges `X` over `set_partitions(n)` — every flat — at every one of
its four tests. **The repair's check does run in the region where the original error was
invisible to its own measurement.**

### Would it have caught the original defect? Yes — and three further wrong statements too.

I ran a mutation panel through the same two tests (`n ≤ 6`, 404 classes):

| rule | `≠ M_0` as sets | `Σ m_X ≠ \|L(P)\|` |
|---|---|---|
| **DOC** (mg-ebd8's statement) | 112 bad of 404 | 112 bad of 404 |
| **REPAIRED** (mg-1953) | **0 bad of 404** | **0 bad of 404** |
| mut: acyclic only (drop the antichain clause) | 399 bad of 404 | 399 bad of 404 |
| mut: convex blocks + acyclic | 399 bad of 404 | 399 bad of 404 |
| mut: acyclicity tested only when `\|X\| ≥ 3` | 15 bad of 404 | 15 bad of 404 |

The last mutation is the interesting one: it is a rule that is right on most flats and wrong
only on the coarse ones, i.e. the shape a *partially* repaired statement would have. The test
kills it. **The repaired rule is the only one of the five that survives, and the test has power
against near misses, not just against the original.**

### One order past the repair's range

mg-1953 verifies to `n = 6`. I extended to **`n = 7`**: 5 439 labelled representatives,
877 flats each, 4 770 003 flat evaluations. Every isomorphism class at `n = 7` (2 045, A000112)
has a representative in the sweep, because every 7-poset is a 6-poset plus a maximal element
over an order ideal and all 318 six-element classes are extended in every way.

* repaired rule `= M_0` as sets: **0 bad of 5 439**; `Σ m_X = |L(P)|`: **0 bad of 5 439**
* original rule: **2 837 bad of 5 439**, **39 828 spurious flats**
* first failure: `P = {a<d, b<e, c<f}`, `|L(P)| = 630`, original sums to **917**

**The repaired statement survives one order past the range in which it was repaired, and the
original fails harder there.** It is still a specialisation verified by exhaustion, not proved;
see *What I could not establish*.

---

## R2 — E8. CONFIRMED, EVERY COLUMN.

Built from scratch: feasible words of the poset shelling antimatroid, Björner's greedy product,
and `φ(w) = ({w₁},…,{w_k}, rest)`.

| `n` | classes | band axioms | `φ → F(P)` | **homomorphism** | image closed | **proper** | **injective** | band ⊆ `F(P)` |
|---|---|---|---|---|---|---|---|---|
| 2 | 2 | 2/2 | 2/2 | 2/2 | 2/2 | **0/2** | 0/2 | 0/2 |
| 3 | 5 | 5/5 | 5/5 | 5/5 | 5/5 | **5/5** | 0/5 | 0/5 |
| 4 | 16 | 16/16 | 16/16 | 16/16 | 16/16 | **16/16** | 0/16 | 0/16 |
| 5 | 63 | 63/63 | 63/63 | **63/63** | 63/63 | **63/63** | **0/63** | 0/63 |

Antichain cardinalities: band `2, 5, 16, 65, 326` (A000522) against `|F(P)|` `1, 3, 13, 75, 541`
(A000670) — **5 vs 3 and 16 vs 13 at `n = 2, 3`**, exactly as quoted, and the document is right
to bound that comparison to `n = 2, 3` (the inequality reverses at `n = 4`).

Every clause of the replacement is confirmed: monoid homomorphism, image inside `F(P)` and
closed under the repo's product, **proper exactly for `n ≥ 3`** (0/2 at `n = 2`, where the image
is all of `F(P)`), **never injective**, and the band is not even a subset of `F(P)`. The
"ADJACENT" verdict for row H survives on the corrected reason, as E8 says.

E8's scope clause — that the band tested is *the one the document identifies*, not one read off
Björner's Thm 4.15 — is correct and I inherit the same limit; see *What I could not establish*.

---

## R3 — "STRICTLY SHARPER" → "STRICTLY MORE INFORMATIVE". CONFIRMED, AND STRENGTHENED.

Two-sided, level by level: the repo's triangular solve (rebuilt from the identity, never
consulting the closed form) against Brown's repaired closed form (never consulting the solve).

| `n` | classes | levels | disagreeing levels | bad posets | levels carrying **zero** | carrying nonzero |
|---|---|---|---|---|---|---|
| 2 | 2 | 4 | 0 | 0 | 1 | 3 |
| 3 | 5 | 24 | 0 | 0 | 11 | 13 |
| 4 | 16 | 206 | 0 | 0 | 125 | 81 |
| 5 | 63 | **2 353** | **0** | 0 | **1 674** | 679 |
| 6 | 318 | **37 029** | **0** | 0 | **28 988** | 8 041 |
| **total** | **404** | **39 616** | **0** | **0** | | |

**0 disagreements at all 39 616 levels to `n ≤ 6`, 0 posets bad of 404** — and at `n = 5`
specifically, **0 disagreements at every one of the 2 353 levels**, which is the figure the brief
told me to verify myself. The support claim also holds: `supp(m) = M_0` at every one of the
39 616 levels, `0` exceptions. The true gain survives too: **28 988 of 37 029** at `n = 6` and
**1 674 of 2 353** at `n = 5` carry zero.

I added the direction check a bound word requires. **Neither side is ever larger than the other
at any of the 39 616 levels** — `0` where the closed form exceeds the solve, `0` where it falls
short, `39 616` equal. *"Sharper"* has no direction to point in; *"more informative"* is a
statement about *when* the answer is available, and the zero-level count is the honest size of it.

**The word replacement is complete, and the adoption argument is not re-introduced.** Every
occurrence of *"sharper"* in the repaired document (3) sits inside a quotation being refuted;
every occurrence of *"weaker tool"*, *"weaker form"* and *"adopt … Theorem 2"* across `docs/` and
`STATE.md` (7 in total) is negated or withdrawn in its own sentence. `STATE.md` carries no row
for this work item, so there is no missed site there. The commit message of `714aceb` is frozen
and §0 correctly declares itself the place the correction lives.

Concretely, on the worked example `P = {a<b, c<d}`: **14 levels, of which exactly 6 carry
multiplicity** — `ac|bd, ac|b|d, ad|b|c, a|bc|d, a|bd|c, a|b|c|d`, each with `m = 1`, summing to
`|L(P)| = 6`. That is the document's list, entry for entry, and its *"six of the fourteen levels"*.

---

## R4 — THE POPULATIONS. ALL EXACT.

| figure | document | mine |
|---|---|---|
| classes `2 ≤ n ≤ 6` (E3) | 404 | **404** |
| classes `3 ≤ n ≤ 6` (§6 item 5) | 402 | **402** |
| classes `n ≤ 5` (E1) | 87 | **87** |
| moves `n ≤ 5` total | 6 197 | **6 197** |
| product pairs `n ≤ 5` total | 936 261 | **936 261** |
| product pairs, `n = 5` row | 922 073 | **922 073** |
| levels `2 ≤ n ≤ 6` | 39 616 | **39 616** |
| classes by `n` | 1, 2, 5, 16, 63, 318 | **identical** |
| moves by `n` | 1, 5, 37, 397, 5 757 | **identical** |
| levels by `n` | 1, 4, 24, 206, 2 353, 37 029 | **identical** |
| product pairs by `n` | 1, 13, 321, 13 853, 922 073 | **identical** |
| connected classes (§3.1) | 1, 3, 10, 44, 238 | **identical** |
| *"twenty-six years old"* for a 2000 paper | 26 | **26** |

---

## SCOPE — CHECKED IN BOTH DIRECTIONS

**Did it re-open the locating? No.** The eleven ledger status words, original (`714aceb`) against
repaired: **one changed, and it is E8** (`READING, not measured` → `MEASURED`), which the brief
ordered and which I independently re-measured above. E1, E3, E4, E5, E6, E7, E9, E10, E11 are
byte-identical. E2 retains `MEASURED + QUOTED` with an annotation that correctly separates the
false *statement* from the sound *measurement*. No identification is re-derived, re-tested or
hedged; where §8 needs the audit's re-tests it **cites** them.

**Did it over-correct? No.** The §0 headline (*"The construction is a known special case of
something standard"*) is intact, §0 items 1 and 3 are intact, and the `NOT CLAIMED` row is
byte-identical. Nothing treats *"2 BROKEN"* as impeaching the document; §8 opens by saying the
original got everything it located, quoted and measured right, which is what mg-d673 found.

**Material beyond the brief — one item, and it is correct.** 40 marked repair sites. All but one
map to mg-1953's ticket or to a numbered mg-d673 finding (*"one place"* → *"two places"* is the
audit's M9; the L3 lune sentence is the audit's M2). The single exception is
*"thirty years old"* → *"twenty-six"* for a paper published in 2000, which is arithmetic about
the document's own citation and is right. **No new mathematics is developed.** The one place
where the repair could have drifted into it — R2's replacement statement — was dictated by the
ticket, and R1a's construction-based decision of `M_0` is a measurement, not a derivation.

---

## FINDINGS

### A1 — MINOR. `R1d`, "the control that must fire", cannot fail.

mg-1953 reports (§8 R1, and `closed_form_outside_AC.py`'s docstring): *"restricted to `AC(P)`,
the original rule is **0 bad of 318** — so the restriction is **demonstrated** to be what hid the
defect, not merely alleged to be."*

Restricted to `AC(P)`, the original rule **is** the repaired rule, as a set of flats:
`{antichain blocks} ∩ {acyclic quotient} = {antichain blocks and acyclic quotient}`. I checked it
as an identity anyway — **404 of 404 posets to `n ≤ 6`**. So `R1d`'s number is `R1b`'s
repaired-rule column under another name; it cannot come out differently, and it cannot fail while
the repaired rule passes.

The *content* is right and worth stating — the restriction really is what hid the defect. What is
one notch too strong is the billing: this is a **one-line set identity**, provable, not a control
with power to fail. This repo has a standing statement of the criterion
(`code/hodge_leverage_audit_86a3/audit_controls.py:4` — *"a control must be able to FAIL on the
construction it guards"*), and by that criterion `R1d` is a restatement, not a control.

**Why it matters and why it is only MINOR.** It is the original defect's shape recurring one level
up — a check that can only be run where it must pass — which is precisely what my brief asked me
to watch for. But nothing downstream rests on `R1d` having independent power: the discriminating
work is done by `R1a` and `R1b`, which range over all flats and do have power (the mutation panel
above). **Suggested wording:** *"restricted to `AC(P)` the two rules are the same set, so the
target's measurement could not have seen the difference — verified as an identity on all 404
classes"*.

### A2 — MINOR. The same slip R4 repairs, in the figure R3's headline rests on. Not in the repaired document.

R4 fixes two *"`n = 5` row quoted as an `n ≤ 5` total"* slips and adds a total row to §3.3 *"so
the slip cannot recur"*. It recurs on the same day, in `docs/roadmap.md:41`:

> *"The audit refuted it: **0 disagreements at every one of 2,353 levels** to n≤5"*

Levels by `n` are `1, 4, 24, 206, 2 353`. The `n ≤ 5` total is **2 588** (2 587 for `2 ≤ n ≤ 5`);
**2 353 is the `n = 5` row.** Conservative direction — the comparison actually covers more levels
than the sentence claims.

**The repaired document itself is clean here** — it writes *"(4, 24, 206, 2 353, 37 029 by `n`)"*
and *"1 674 of 2 353 at `n = 5`"*, both correct — and `roadmap.md` is not among the files mg-1953
edited. **This is for pm-onethird, not a defect in `6b1eacf`.** It is recorded because R4's own
claim is that the slip *cannot recur*, and the one live instance of it in the repo sits in the
sentence carrying R3's headline.

### A3 — MINOR. The self-test guards one direction only.

§4 and the commit message describe `code/landscape_repair_1953/selftest.py` as failing loudly
*"if the document and the instruments ever drift apart"*. It does not read the document: the
expected values are hard-coded constants transcribed from it (the document's filename appears
once in the file, in a docstring). It fails if the **instruments** drift from those constants; an
edit to the document's numbers passes silently. The 101 assertions are real and the constants are
right — I reproduced all of them — but the guarantee is one-directional, and this is the same
class mg-2216 raised against `bf17716`'s control. Cheap fix if wanted: grep the stated figures out
of the markdown and assert against those.

### A4 — MINOR / residual. Row Q enumerates, withdraws cleanly, and states no contact criterion.

The repair does what the brief asked and does it in the honest form. Seven named programmes,
correctly counted; the unhedged *"neither has any contact"* is **withdrawn to a hedge** and booked
under **E10** as a report on a search, where it belonged; no-contact is claimed only for
(1) FI-modules, (2) Deligne, (4) differential posets and (5) dual graded graphs, each as a report
on a search; and **(3) towers of algebras / branching graphs, (6) Okounkov–Vershik and
(7) diagram algebras are claimed neither way, with the document saying in terms that it did not
test them.** That is the right shape: the added candidates are **named and declared untested**
rather than named and silently counted as searched, which is the failure the brief warned about.

What the row does **not** say is **what would have counted as contact**. There is no criterion, so
the four negatives remain unfalsifiable in the same way the original *"no"* was — correctly
scoped now, but still not checkable by a reader. Adding one sentence (*"contact would mean a
published treatment of `O(P)`, of walks on a convex set of chambers, or of the `P`-compatible
ordered partitions as an object in that programme"*) would close it. **Not a defect in what is
asserted** — the row asserts less than its evidence, which is the right direction.

---

## WHAT I COULD NOT ESTABLISH

Stated explicitly, because a clean audit that hides its limits is worth less than its numbers.

1. **Nothing about what the sources say.** I read no PDF. Brown 2000, Björner, MSS,
   Jenča–Sarkoci, Czédli–Lenkehegyi, Bergeron–Li and Bergeron–Lam–Li are all untested by me.
   Everything above is mathematics and arithmetic; **no attribution in the document is
   corroborated by this audit.** In particular I did not check that Brown's Theorem 2 says what
   the document says it says, only that the specialisation the document states is the correct
   description of `M_0` and reproduces the repo's own solve.
2. **That the greedoid band is Björner's.** I built the object the document identifies, as
   mg-1953 and mg-d673 did. E8's scope clause is correct and I inherit it: R2's columns are
   about *the document's object*, not about Thm 4.15.
3. **That the repaired closed form is a theorem.** It is verified by exhaustion to `n = 6` by
   mg-1953 and to `n = 7` here. Neither of us proves it. (The `M_0` characterisation itself —
   antichain blocks and acyclic quotient — does have a one-paragraph proof, which the
   certificates in my decision procedure amount to; the *value* `∏(|B|−1)!` is verified, not
   derived, in both instruments.)
4. **Whether towers of algebras, Okounkov–Vershik or diagram algebras have contact.** Row Q
   claims nothing either way and neither do I.
5. **The locating.** Out of scope by instruction, and correctly so — mg-d673 established it as
   equalities (0 bad of 936 261 pairs, 0 bad on 86 posets, 0 disagreements on 87) and mg-1953
   does not re-open it. I did not re-run those tests and this audit is not evidence about them.
6. **My own arithmetic, before the self-test caught it.** I first asserted the `n ≤ 5` level
   total as 2 587; it is **2 588** (2 587 excludes `n = 1`). `selftest.py` failed on it and it is
   fixed. Recorded because an audit that reports its instrument caught nothing is reporting less
   than it knows.

**One thing checked and found fine, since the brief asked for it specifically:** I looked for the
stronger reading quietly retained in prose after the correction. §0's *"Two places where the
literature is ahead of the repo, not behind it"* survives the refutation — *ahead* is carried by
informativeness (the zero levels named `a priori`), not by sharpness, and the sentence's own
follow-on says *"strictly more informative"*. The L2 multiplicity row explicitly withdraws
*"a weaker form of the published one"* as *"the 'strictly sharper' claim in another costume"*.
I found no site where the bound reading survives.

**And one gap in the repaired statement that I closed rather than left open.** E2 says the
multiplicities are `|μ(X,V)|`; both the original and the repaired form evaluate that as
`∏_B(|B|−1)!` and neither instrument checks the step. Möbius function of `Π_n` computed here from
its defining recursion: `|μ(0̂,X)| = ∏_B(|B|−1)!` on **all 203 flats at `n = 6`** and every flat
below, 0 exceptions. The chain is complete; it simply was not complete inside the repair.

---

## REPRODUCE

```
cd code/landscape_repair_audit_3b51 && ./run_all.sh    # ~5 min, pure Python 3
```

Committed outputs: `out_r1_offAC.txt`, `out_r1_n7.txt`, `out_r3_r4.txt`, `out_r2_e8.txt`,
`out_scope_text.txt`, `out_selftest.txt` (139 assertions, exits non-zero on any failure).

**"Sharing no code" checked, not asserted.** Across mg-ebd8's three instruments, mg-d673's five
and mg-1953's four, the only identical function body is a four-line `factorial` loop, and the
longest common contiguous run of code is seven lines — the definition of the ordered-partition
product, which admits no materially different spelling. mg-1953's claim is sound; mine is checked
by the same method.

---

## PRE-FILED AUDIT — WHERE TO ATTACK *THIS* DOCUMENT

Per arc convention, ordered by expected yield.

1. **A1 is the finding most likely to be wrong in its sizing, not its content.** I call `R1d` a
   restatement rather than a control. An auditor who thinks the distinction is empty should say
   so — the identity is one line and either it settles the question or the billing was fine.
2. **My `n = 7` sweep uses labelled representatives with duplicates left in.** The coverage
   argument (every 7-poset is a 6-poset plus a maximal element over an ideal) is a proof, not a
   measurement, and I did not verify that the 5 439 representatives hit all 2 045 classes by
   canonicalising them. If the argument is wrong, A7's `0 bad of 5 439` is about an unknown
   subset.
3. **The mutation panel is four hand-picked wrong rules.** A panel is worth its enumeration, and
   mine is not exhaustive over plausible mis-statements — the same criticism this document makes
   of row Q's original candidate space, applied to me.
4. **Everything in `What I could not establish`, especially item 1.** Six unread primary sources
   remain the largest hole in the underlying document and this audit does nothing about them.
5. **A2 is about a file mg-1953 did not edit.** If that makes it out of scope for this audit
   rather than a note for pm-onethird, say so.

---

## SCOPE OF THIS AUDIT

No edit to `docs/OneThird-Landscape-Where-This-Lives.md`, to `STATE.md`, to `docs/roadmap.md`, to
`docs/OneThird-Semigroup-Walk-Family-Note.md`, or to any instrument other than my own. Nothing
about `λ₂`, `Δ_AT` or the pricing. No publishability verdict, no novelty claim. The locating is
not re-opened. §7's note-amendment recommendation and A2's roadmap sentence are both
pm-onethird's call, not mine.
