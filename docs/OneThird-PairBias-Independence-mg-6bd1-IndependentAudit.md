# INDEPENDENT AUDIT of `mg-345e` — is the pair-bias derivation of `ε_spec` independent of L4's modulus question?

**Work item.** `mg-6bd1`. Pre-filed in the SAME ACTION as `mg-345e`, per this program's
standing pre-filed-audit discipline.
**Target.** `mg-345e` at `550a7f105c30273b06d376a60d720cd61b652499`, which answered
**(A) INDEPENDENT**.
**Instrument.** `code/pairbias_indep_audit_6bd1/`.
**Predictions.** `code/pairbias_indep_audit_6bd1/PREDICTIONS.md`, committed at `3cbc554`
**before any script of this audit existed and before one line of mg-345e's derivation was
read** — with eight hand measurements disclosed rather than laundered into predictions.

---

## 0. THE SHA I READ, AND IT IS TWO SHAS BECAUSE ONE OF THEM IS THE HONEST ONE

The dispatch note named `491d42c79f7628c18cb7a5d197faa9f4600cd6c1` and warned STATE.md
may have moved. Measured **before** any prediction was written:

```
git rev-parse 491d42c:STATE.md  ->  7f73bfc87b4bc4caab6c836f8c3922a2416863cf
git rev-parse 65866c2:STATE.md  ->  7f73bfc87b4bc4caab6c836f8c3922a2416863cf   (HEAD)
```

**The file I read is blob `7f73bfc87b4bc4caab6c836f8c3922a2416863cf`.** `491d42c` is still
the most recent commit touching STATE.md; six commits landed after it without touching the
file, so the commit SHA the dispatch gave me and the object I read are the same thing.
`mg-a83c` had not landed as of HEAD `65866c2037ccebba0f6d880ec6be55b4927b3261`.

I name the **blob** and not only the commit because the commit is the identifier that rots
when some *other* file is edited. The blob is the identifier of what was actually read.

---

## 1. Verdict

> ## **CONFIRMED WITH CORRECTIONS. (A) INDEPENDENT SURVIVES A RE-DERIVATION ONE LEVEL DOWN — AND IT IS NOT THE CONFLATION.**
>
> **The dependency list was re-derived, not accepted.** All five of `mg-345e`'s named
> inputs were walked to their own recorded statements and adjudicated by the step that
> would fail if L4 were withdrawn. **0 of 5 is L4-dependent at depth 2** (§3). The chain
> from `δ(P) < 1/3` to `ε_sup < 1` is exhibited in full in §3.3 with nothing elided, and
> `Δ₁`, a cut, a prefix, Cheeger, `C₃`, Step 6, L4's `F` and L4's threshold appear at no
> node of it. **`mg-6bc2` is correctly unblocked.**
>
> **THE SCOPE CONFLATION DID NOT HAPPEN, AND I CHECKED IT AT THE STRONGEST POINT.** Every
> sentence in which `mg-3af9` appears was extracted verbatim rather than classified
> (§4). Both are consumption-scoped, both carry `mg-3af9`'s own *"strictly positive"*
> quantifier — which is the exactness note `mg-c8c6` insisted on — and `mg-345e` wrote a
> `SCOPE DISCIPLINE` paragraph at `:216` saying in its own words that none of it touches
> provability. **`mg-345e` is NOT BROKEN on the trap this audit was filed to catch.**
>
> **FOUR CORRECTIONS, one of which is material and is a reproduction I say is a
> reproduction:**
>
> 1. **§6's `1/6` census is wrong on both of its counts, and the missed occurrence is
>    `mg-345e`'S OWN HEADLINE NUMBER IN OTHER UNITS.** *"`1/6` occurs twice in this corpus
>    and neither occurrence is a supply-side derivation"* — `mg-c4f5:415` says
>    *"Freezing unconditionally gives only `ε < 1/6`"*, which is supply-side, and I
>    re-derived in exact rationals that it is the **same theorem** as `ε_sup < 1`: one
>    statement `E[inv_e] < n(n−1)/6` divided two ways, `÷ n²` giving `(n−1)/(6n) → 1/6` and
>    `÷ (n²−1)/6` giving `n/(n+1) → 1`, ratio `6n²/(n²−1) → 6` (§5). So `mg-345e`'s
>    *"no claim is made here about whether `1/6` is the right answer"* is **too modest about
>    its own §2**. **THIS IS A REPRODUCTION**, not my discovery: `mg-6bc2` filed it as its
>    H5 at 18:21 and `mg-9adf` landed the unit map at `21ee93f` 19:30 — both **after**
>    `mg-345e`. I re-derived it rather than citing it, and the arithmetic is mine.
> 2. **§3's arm-B point 1 holds on ONE of L4-as-stated's THREE branches** (§6).
>    *"L4 fired from a thin prefix reached without L1b contradicts `δ(P) < 1/3` outright"*
>    is blocked on (ii) by `mg-3af9` and on (iii)-as-stated by `Op-Form`'s own **PROVEN**
>    ledger claim 8 — **both cited by `mg-345e` elsewhere in the same document.** This does
>    not move §3's conclusion, which stands on its point 2 (`2/3` vs `ε_leak ≈ 0.20`) alone.
> 3. **§5.1's "NARROWER" is right about `F` and incomplete about the branch structure**
>    (§7). What Step 6 needs — *"if `Δ₁ ≤ ε₀` then (i) or (iii-exact)"* — is **strictly
>    stronger** than L4-as-stated: a disjunct removed and a branch tightened. `mg-345e`
>    writes that strengthened statement on the page and then labels the move *narrower*.
> 4. **The scope qualifier is in the body, in both STATE.md rows and in the commit body —
>    and absent from the commit SUBJECT** (§4.2), which is what the next agent greps. Under
>    this audit's own pre-registered guard (P13) that is a **LABELLING** finding and may not
>    be called BROKEN, and it is not.
>
> **ONE SUPPORT SUPPLIED IN `mg-345e`'S FAVOUR THAT IT DID NOT EXHIBIT** (§7.2). Its
> threshold-vs-modulus refinement would be circular if the *only* argument for the
> threshold's `n`-freeness were `Op-Form` §3.2's support 1, which reasons **from** `F`.
> It is not: §3.2's support 2 is `F`-free — *"nothing downstream of L4 contains an `n` …
> the window `[1/3,2/3]` has width `1/3` at every `n`"*. The refinement is available.
>
> **AND ONE PIECE OF LUCK THAT IS NOT LUCK** (§8): `mg-345e` prints `2/(n+1)` **zero
> times**, so tonight's `mg-131e` refutation does not touch it — and `mg-9adf`/`mg-6bc2`
> subsequently proved `n/(n+1)` is **attained**, which upgrades its §6 from a bound to an
> equality. **Its headline is stronger tonight than when it landed.**

---

## 2. What was re-derived rather than checked

Nothing in `code/pairbias_indep_audit_6bd1/` imports `lib345e` or reads
`code/pairbias_independence_345e/out_*.txt`. The ledger reader is a two-pass
split-on-pipes/token-walk reader rather than a regex over the label cell, chosen
specifically so that `mg-345e`'s own Defect-1 failure mode — an under-reading quantifier —
could not be inherited along with its result. Exact rationals throughout; no float on any
path that decides anything.

**Every printed figure of `mg-345e` reproduces.** `out_b1_ledger.txt`, `out_b2_algebra.txt`:

| figure | `mg-345e` | `mg-6bd1`, independent code | |
|---|---|---|---|
| ledger rows | 36 | **36** | ✓ |
| recorded dependency edges | 11 | **11**, and all six source rows exhibited | ✓ |
| transitive dependents of claim 4 | `[12, 17, 18, 23]` | **`[12, 17, 18, 23]`** | ✓ |
| supply claims `21,22,25,26,27` reaching 4 | 0 of 5 | **0 of 5**, ancestor sets all empty | ✓ |
| claim 28 reaches claim 4 | no | **no**; label mentions both `L4` and `C₃` with no edge | ✓ |
| `E_unif[footrule] = (n²−1)/3` | to `n=7` brute, `n=59` by sum | **brute force `n≤7`, double sum `n≤59`, 0 mismatches** | ✓ |
| `ε = 2m/(n²−1) = d·n/(n+1)` | 0 mismatches | **0 mismatches over 10,699 `(n,m)` grid points, `n ≤ 40`** | ✓ |
| `ε_sup < 1` | `< 1` uniformly | **sup over the grid `= 40/41 < 1`; ceiling `n/(n+1)`, never attained** | ✓ |
| `0.20²/2` | `1/50` | **`1/50` exactly** | ✓ |
| gap factor | `50` | **`50` exactly**; at finite `n` it is `50n/(n+1)` | ✓ |

Four negative controls on the ledger graph fire (`out_b1_ledger.txt`): severing `17←4`
empties `{18, 23}` from the closure; a fake `26←18` puts a supply claim on `4`; truncating
claim 17's clause moves the **edge count** and not the verdict, which is `mg-345e`'s own
Defect 1 reproduced deliberately and confirmed non-verdict-bearing; and dropping `given`
as a keyword identifies the eleventh edge as `32←28`.

**One currency check `mg-345e` did not run and which this lineage has failed twice.**
Ledger claim 26 records the constant as **`2/3`**; `mg-345e`'s §0 cites claim 26 for the
value **`1`**. Both are right and the conversion is **exact, not asymptotic**:
`E[inv_e]/E_unif[inv] = 2/3` at every `n`, while `ε_spec = n/(n+1)`, and
`(n/(n+1)) / (2/3) = 3n/(2(n+1))`. **`mg-345e`'s citation is correct and is not a
conflation** (`out_b2_algebra.txt` C3).

---

## 3. THE ONE-LEVEL-DOWN WALK — the check this ticket exists to run

`mg-345e`'s Claim 2.1 list is five items. The ticket for this audit says a list is not
enough: *"an argument can be independent of L4 by NAME while consuming a lemma that is
itself conditional on L4."* So each input was taken to **its own recorded statement** and
adjudicated by the rule I bound myself to in advance (P14): **to call an input
L4-dependent I must exhibit the inequality or step that fails when L4 is withdrawn.
Naming a document is not enough.** `out_b5_depth2_walk.txt`.

### 3.1 The five inputs

| # | input | recorded at | L4 at depth 2? |
|---|---|---|---|
| 1 | `inv_e(σ)` | `STATE.md:43` glossary | **NO** — a definition. Names the distinguished order `e`, supplied by input 3, and nothing else. |
| 2 | frozen `δ(P) < 1/3` | the minimal-counterexample condition | **NO** — it is the *hypothesis*, upstream of the whole architecture including L4. |
| 3 | coherence (`mg-61bb`) | `STATE.md:155` | **NO, and proved twice independently** — see §3.2. |
| 4 | linearity of expectation | — | **NO.** ZFC. |
| 5 | `mg-210d`'s master bound | `docs/state-history/attempt-mg-210d.md:54` | **NO** — see §3.2. |

### 3.2 The two that needed real work

**Input 3, coherence.** `STATE.md:155` records it as *"a logical **consequence** of
`δ<1/3` (same poset class — shrinks it by zero)"*, whose only residual is subadditivity of
balances `β(u,w) ≤ β(u,v) + β(v,w)`. **And it is derived a second time from the other
side**: `mg-210d`'s own record calls it a *"free by-product … frozen ⟹ the majority
relation is automatically a linear extension, and `1/3` is exactly the threshold"*.
Neither derivation mentions a cut, a prefix, or a modulus. **Withdraw L4 and no symbol in
either argument changes.**

**Input 5, the master bound.** `1 − λ_std ≤ 3E[footrule]/(n²−1) ≤ 6E[inv]/(n²−1)`. Two
steps: a spectral estimate of `λ_std` against expected displacement, and Diaconis–Graham's
`D ≤ 2I`, a finite combinatorial identity. `Op-Form` §6.1 hand-checks the second inequality
and the antichain equality separately; `mg-c4f5` re-derived the whole bound by hand at 0
violations over 101,658 posets `n ≤ 7`. **No step takes a cut, a prefix, a modulus or a
threshold as input.** And `mg-345e` marks this input *"(only for the `λ_std` rendering)"* —
correctly: the ticket's own `(LIB-const)` form `E[inv_e] ≤ (ε/6)(n²−1)` does not need it.

**A machine screen over the recorded statements returns `NONE` for every L4-indicator
token** (`L4`, `Δ₁`, `near-ordinal-sum`, `modulus`, `F(ε)`, `prefix`, `Cheeger`, `C₃`,
`Step 6`, `interface element`, `leak`). **That screen is a screen and is labelled one** —
it cannot see a dependence the record does not write down, which is why the adjudications
above are hand-written and quote the step.

### 3.3 The chain I walked, end to end, with nothing elided

```
δ(P) < 1/3                                              [HYPOTHESIS]
    |
    +--(mg-61bb; independently mg-210d's by-product)--> e exists and is canonical
    |       inputs: subadditivity of balances. No cut. No modulus.       [L4-FREE]
    |
    +--> for each incomparable pair {i<j}: Pr[j ≺_σ i] < 1/3            [HYPOTHESIS]
            |
            +--(linearity of expectation)--> E[inv_e] = Σ Pr[…] < m/3   [L4-FREE]
                    |
                    +--(m ≤ C(n,2), arithmetic)--> E[inv_e] < n(n−1)/6  [L4-FREE]
                            |
                            +--( ÷ (n²−1)/6 )--> ε_spec  < n/(n+1) → 1  [L4-FREE]
                            +--( ÷ n²        )--> ε_c3ca < (n−1)/(6n) → 1/6
```

**Not on this chain, at any node:** `Δ₁`, a cut, a prefix, Cheeger, `C₃`, Step 6, L4's
`F`, L4's threshold `ε₀`, `mg-3ce3`'s calibration, `mg-3af9`'s branch-(ii) result.

### 3.4 The one place L4 *is* one level down — and it is on the other side

`Op-Form`'s ledger records **`23 ← 18 ← 17 ← 4`**, and claim 4 is literally *"L4's `F` is
`n`-free"*. Claim 23 **is** `(LIB-const)` — but as the **architecture's requirement**, i.e.
the claim that a constant *uniform in `n`* is the right thing to want. So the honest
depth-2 finding is a split, and it is exactly `mg-345e`'s split:

* the **inequality** `E[inv_e] ≤ (c/6)(n²−1)` with `c` uniform in `n` — **L4-FREE**;
* the claim that a uniform-in-`n` `c` is what the architecture **needs** — **L4-conditional**,
  through `23 ← 18 ← 17 ← 4`.

`mg-345e`'s §1 supply/demand table puts the cut in exactly this place, and its own P1
predicted *"claim 23 in dependents-of-4; 25, 26 outside"* before running. **The split
survives the walk.**

---

## 4. THE SCOPE CONFLATION — checked at its strongest point, and it did not happen

`pm-onethird` conflated `mg-3af9`'s **consumption** result with a **provability** claim on
2026-08-07 and reversed the same sweep. `mg-345e` was warned in its own ticket body. A
document that has been warned is both more likely to guard correctly and worse if it does
not, so this was checked by **extracting every sentence containing `mg-3af9` verbatim**
rather than by a keyword classifier — a classifier tuned until it returns the answer I
want is unfalsifiable. `out_b3_census_scope.txt`.

### 4.1 Both sentences, and they are consumption-scoped

```
:34   > (ii) is unconsumable for **every strictly positive** `F` (`mg-3af9`,
        UNCONDITIONAL, audited `mg-c8c6`)
:209  | (ii) remove/modify `≤ F(ε)n` interface elements | **moot** — unconsumable by
        Step 6's stated transfer for **every strictly positive** `F`, `o(ε)` included |
```

Both are about **what Step 6 can consume**. Neither says anything about whether L4-as-stated
is provable. **And both carry the `strictly positive` quantifier**, which is not decoration:
`mg-c8c6`'s audit of `mg-3af9` records that `mg-3af9`'s own flat §0 sentence
*"No modulus rescues Step 6's transfer on branch (ii)"* is **literally false for `F ≡ 0`**,
and that the correct statement is the quantified one. `mg-345e` cites the quantified form,
not the flat one. That is the difference between using an audited result and using its
headline.

`mg-345e` then wrote, at `:216–223`, unprompted:

> **SCOPE DISCIPLINE — read this before citing the row above.** Every entry is a statement
> about what Step 6 **consumes**. **None of it says L4-as-stated is or is not provable at
> an `n`-free modulus.** … The `n`-freeness of `F` remains exactly as open as it was.

**`mg-345e` IS NOT BROKEN. The trap this audit was filed to catch was not sprung.**

### 4.2 Where the qualifier is, and the one column it is missing from

Under P13's binding guard, a defect present only in a compression is a **labelling**
finding and may not be called BROKEN. Measured across all four columns:

| column | carries the scope guard |
|---|---|
| document body (`:216`) | **yes** |
| `STATE.md` rows (`:164`, and `:15`'s parenthetical) | **yes** |
| commit body | **yes** — *"SCOPE DISCIPLINE, HELD: … Row 11 unchanged."* |
| **commit SUBJECT** | **no** |

The subject reads *"…AND THE GATE IT NAMES IS WRONG TWICE"* with no scope clause. The
subject is what the next agent greps. This is the same shape `mg-94c3` found in `mg-76b2`
(currency named in §6, absent from the title) and in itself (conditional at the claim,
absent from the commit subject). **It is a labelling finding and it is reported as one.**

---

## 5. CORRECTION 1 — the `1/6` census, and why it is bigger than a miscount

`mg-345e` §6: *"`1/6` occurs twice in this corpus and neither occurrence is a supply-side
derivation."* Re-run against the tree **at `mg-345e`'s own commit**, so it is scored
against what it could actually have seen (`out_b3_census_scope.txt`).

The raw regex count is 34 across 14 files, and **that is not the number to quote** — five
hits are the substring `1/6` inside `61/61` and `6197/6197`, and thirteen more are other
subject matter (Hodge `γ`-weights, `mg0a11`'s `1/C(6,1)`, branch-(ii) cut arithmetic,
roadmap prose). In the `ε_spec`/pair-bias subject matter the **distinct** occurrences are:

1. `Op-Form` §6.4, *"slack `≤ 1/6` for a centred pair"* — **demand**-side, BROKEN as
   labelled by `mg-e35c` F5. `mg-345e` names this one.
2. `mg-e2de`'s `1/6`, the collapse of a local `δ` **lower** bound at co-degree 2
   (`STATE.md:158`) — neither supply nor demand. `mg-345e` names this one.
3. **`docs/OneThird-LIBweak-mg-c4f5-IndependentAudit.md:415`** —
   *"**Freezing unconditionally gives only `ε < 1/6 ≈ 0.167`.**"* — **SUPPLY-SIDE.**
   `mg-345e` does not name it.

**So the sentence is wrong on both counts under any scoping: there are at least three, and
the third is the kind it says does not exist.**

### 5.1 And the third one is `mg-345e`'s own theorem

`mg-c3ca` Prop. 4.1 normalises by `n²`: `E[inv_e] ≤ ε·n²`. Re-derived here in exact
rationals over `n = 2..40`, 0 mismatches (`out_b2_algebra.txt` C4):

```
ONE theorem:   frozen  ⟹  E[inv_e] < m/3 ≤ n(n−1)/6
     ÷ n²       ⟶   ε_c3ca < (n−1)/(6n)  ↗  1/6      (never attained; NC7 fires)
     ÷ (n²−1)/6 ⟶   ε_spec  < n/(n+1)    ↗  1        (never attained)
     ratio      :   ε_spec/ε_c3ca = 6n²/(n²−1)  →  6   (27/4, 216/35, 3200/533, …)
```

**`ε_sup < 1` and `ε < 1/6` are the same statement under two divisions, ~6× apart because
of the units.** `mg-345e`'s §6 closes with *"Whether either is Daniel's `1/6` is `mg-6bc2`'s
question and I have not attempted it"* — and its own §2 already contains the answer to the
unit half of that question.

**THIS IS A REPRODUCTION AND I SAY SO PLAINLY.** `mg-6bc2` filed it as its H5 at 18:21;
`mg-9adf` landed the full unit map at `21ee93f` (19:30) and `mg-9f91` audited it — both
**after** `mg-345e` at 14:12. My contribution is that the arithmetic above was re-derived
from `mg-c3ca`'s and `Op-Form`'s definitions rather than read off `STATE.md:15`, and that
it is scored against `mg-345e`'s own tree.

### 5.2 What this does NOT do

It does not touch **(A) INDEPENDENT**. Both divisions of `E[inv_e] < n(n−1)/6` are the last
two lines of the §3.3 chain, and that chain is L4-free at every node. **A unit error on the
supply side cannot import an L4 dependence** — there is no L4 in either denominator.

---

## 6. CORRECTION 2 — §3's arm-B point 1 holds on one branch of three

§3 argues the independence is *forced*, and names one escape (the direct-prefix route,
`mg-00b9` repaired by `mg-2de0`). Its point 1 about that escape reads:

> *"L4 fired from a thin prefix reached without L1b contradicts `δ(P) < 1/3` **outright** —
> the frozen class is empty, and every statement about minimal counterexamples is vacuously
> true, `ε_spec` included."*

L4-as-stated is a **three-way disjunction**. `out_b4_branches_and_arch.txt`:

| branch | Step-6 contradiction? | authority | cited by `mg-345e`? |
|---|---|---|---|
| (i) `P` contains a `1/3`-balanced pair | **YES** | definition of `δ(P)` | yes, §5.1 row (i) |
| (ii) remove/modify `≤ F(ε)n` interface elements | **NO** | `mg-3af9`, unconsumable for every strictly positive `F` | **yes, §5.1 row (ii)** |
| (iii) as stated | **NO** | `Op-Form` Claim 3.2 = **ledger claim 8, PROVEN**, for any `F > 0` under either reading | **yes** — it reads that ledger in §2 and §4 |
| (iii\*) repaired to exact `[1/3,2/3]` | **YES** | `Op-Form` §3.4's repair, `mg-e35c` F5 | yes, §5.1 row (iii) |

**From L4-as-stated the contradiction follows on 1 of 3 branches.** So *"outright"* is
available only on (i), and it is blocked on the other two by results `mg-345e` itself cites
in the same document — one of which is `Op-Form`'s own **PROVEN** claim.

**What this does and does not move.**

* It does **not** touch the verdict. §2 establishes independence by **exhibiting** an
  L4-free derivation; §3 only argues that independence is *forced*.
* It does **not** reopen §3's conclusion. §3's point 2 — the repaired direct route reaches
  only `Δ₁ ≤ 2/3` against `ε_leak ≈ 0.20`, and `2/3 > 0.20` — closes the escape on its own
  and is independent of point 1. I confirmed `2/3` at `mg-2de0`'s §0.
* It **does** mean point 1 is not available **as written**: if the escape ever became live,
  L4-as-stated firing into (ii) would empty nothing, so the question would not
  automatically "dissolve".

### 6.1 And a smaller one: §3 arm A's machine part decided nothing

`lib345e.ARCH_EDGES` is a **path**: every node has out-degree ≤ 1. On a path,
*"0 paths avoiding X"* is true of **every** interior node. Exhibited
(`out_b4_branches_and_arch.txt`): the traversal returns `1 / 0` identically for
`pair bias`, for `L1b conclusion`, and for `thin prefix`. **The traversal has zero
discriminating power.** All of arm A's content is in the transcription — `mg-345e` declares
that transcription as its Defect 3 and labels the conclusion *"[PROVEN, on the
hand-transcribed step graph]"*, which is honest; what it does not say is that the machine
added nothing to it. **The part of §3 that carries information is the hand search for the
missing edge, which `mg-345e` ran without being asked to.**

---

## 7. CORRECTION 3 — "NARROWER" is right about `F` and incomplete about the branches

### 7.1 The incompleteness

§5.1 concludes:

> *"So what Step 6 consumes is an `F`-free statement: **"if `Δ₁ ≤ ε₀` then (i) or
> (iii-exact)"**. The demand's dependency on L4 is a dependency on that statement's
> THRESHOLD `ε₀`, not on its MODULUS `F`."*

The `F` half is **correct** and I confirm it: `Op-Form` §3.3 records that the source never
uses (ii), and §3.4's recommended repair removes `F` from (iii), leaving `F` only in the
branch nobody consumes.

But *"if `Δ₁ ≤ ε₀` then (i) or (iii-exact)"* is **strictly stronger** than L4-as-stated —
one disjunct removed and one tightened. It is not implied by L4; it implies L4. So the
demand's burden is not simply a *narrower slice* of the modulus question:

* **narrower** in the `F` dimension — `F`'s value is not consumed. ✓
* **stronger** in the branch dimension — the statement Step 6 needs is a **new open
  problem**, not a sub-question of an existing one.

`mg-345e` writes the strengthened statement on the page, in the very sentence, and then
labels the move *narrower*. A reader who takes "NARROWER" as "less work to do" is misled
about the branch dimension. **This is a framing correction. It does not affect the verdict,
and it does not affect §5.2's `C₃` point, which is independent and which I confirm.**

### 7.2 A support `mg-345e` needed and did not exhibit — supplied here, in its favour

§5.1 says the demand needs the threshold's `n`-freeness rather than the modulus's. But
`Op-Form` §3.2 **derives** the threshold's `n`-freeness *from* the modulus reading
(support 1: *"`n` appears exactly once in L4, and it appears multiplied by `F`, not inside
it"*). If that were the only support, `mg-345e`'s refinement would be circular — it would
be discarding `F` while standing on an argument made of `F`.

**It is not the only support.** `Op-Form` §3.2's support 2 is `F`-free:

> *"Nothing downstream of L4 contains an `n`. … The predicate being contradicted is
> `δ(P) < 1/3` — a max over pairs of a probability, compared against the absolute constant
> `1/3`. The window `[1/3,2/3]` has width `1/3` at every `n`. **The entire downstream of
> Step 5 is dimensionless.**"*

That argument never mentions `F`. **So the threshold's `n`-freeness has an `F`-free support
and `mg-345e`'s narrower reading is available.** It does not exhibit this; it is exhibited
here, and it is the reason correction 3 is a framing correction rather than a defect.

**Scope, stated in the same breath:** none of §7 says anything about whether L4-as-stated,
or the strengthened `(ii)`-free form, is **provable** at any modulus or threshold. That
question is untouched by this audit and stays exactly as open as `mg-345e` left it.

---

## 8. TWO THINGS IN `mg-345e`'S FAVOUR THAT ITS AUTHOR COULD NOT HAVE KNOWN

1. **It prints `2/(n+1)` zero times** — in the document and across the whole instrument.
   `mg-131e` refuted `ε_spec = 2/(n+1)` at `n = 6` at 19:50 and `mg-b488` landed it at
   20:06, **5h38m after** `mg-345e`. `mg-345e`'s number is `n/(n+1)`, the frozen ceiling at
   `d = 1`, which is a **different quantity** from `mg-200d`'s per-slot value. **Its landing
   needs no correction from `mg-372e`'s in-flight sweep.**
2. **Its §6 got stronger.** `mg-345e` §6 says the route *stops* at `1` and calls it a bound.
   `STATE.md:15` now records `max{ 6E_μ[inv_e]/(n²−1) : μ ∈ M_n } = n/(n+1)`, **attained**,
   with `≤` and `≥` both proven for all `n` (`mg-6bc2` Claim 3.1, via `mg-9adf`). So the
   stopping point is an **equality for the information pair bias consumes**, not a bound
   awaiting a better argument — which is `mg-345e`'s §6 claim, upgraded in kind.

**Where I saw `2/(n+1)` presented as live**, per the dispatch note's request: **nowhere in
`mg-345e`'s deliverable or instrument**, and `STATE.md` blob `7f73bfc8` already carries
`mg-b488`'s refutation. The six SOURCE documents `mg-372e` is correcting were not read by
this audit and I make no claim about them.

---

## 9. Predictions, scored — including the ones I got wrong, kept as written

`PREDICTIONS.md`, committed at `3cbc554`.

| # | prediction | outcome |
|---|---|---|
| P1 | `mg-92e6`'s diagonal-capacity bound is on the dependency list | **MISSED.** It is not an input to Claim 2.1 at all — the derivation is three lines and needs none of the sharpening machinery. `mg-345e` places `mg-92e6` on the same *L4-free* list as a **tool**, which is a different claim and a correct one. My prediction assumed a longer derivation than exists. |
| P2 | `b_x` and Diaconis–Graham are on the list | **MISSED, with a rider.** Same reason. Diaconis–Graham's `D ≤ 2I` **is** consumed, but *inside* input 5, not as a separate item. |
| P3 | the INDEPENDENT verdict survives my re-derivation (filed at 0.60) | **HELD.** 0 of 5 inputs L4-dependent at depth 2, §3. |
| P4 | at least one input is conditional on something that is not L4 | **HELD, weakly.** Input 5 is ledger claim 21, labelled `CONDITIONAL — cited from mg-210d (audited)`. That is a citation-conditionality on an audited result, not an open one, and `mg-345e`'s list does not flag it. Reported at its true weight. |
| P5 | the independence instrument sees dependence by NAME only | **HELD, both halves.** The ledger graph scores labels (`mg-345e` says so itself), and §6.1 shows the architecture traversal has zero discriminating power. |
| P6 | **the main hazard** — `mg-3af9` used to discharge the gate's first disjunct / touch provability | **REFUTED, and this is the important miss.** §4. Both `mg-3af9` sentences are consumption-scoped, carry the `strictly positive` quantifier, and are fenced by a `SCOPE DISCIPLINE` paragraph. |
| P7 | it names the consumption/provability distinction explicitly | **HELD** — `:216–223`, verbatim in §4. |
| P8 | the qualifier survives in the body and dies in the compression | **HELD IN ONE COLUMN OF THREE.** It survives in the body, in both `STATE.md` rows and in the commit body; it is absent only from the commit **subject**. Reported as a labelling finding per P13, not as BROKEN. |
| P9 | the `1/6` census is wrong and a missed occurrence is supply-side | **HELD — AND IT IS A REPRODUCTION**, of `mg-6bc2`'s H5 and `mg-9adf`'s landing, both of which post-date `mg-345e`. §5. Scored as a reproduction, not a discovery. |
| P10 | `2/(n+1)` appears in the deliverable | **MISSED. 0 occurrences**, and the miss is in `mg-345e`'s favour — §8. |
| P11 | every printed figure reproduces on my own code | **HELD** — 10 of 10, §2. |
| P12 | the `STATE.md` edit survives byte-for-byte through three rewrites | **HELD** — three probe substrings, 1 occurrence each, in blob `7f73bfc8`. |
| P13 | *my* likely error: scoring BROKEN on a compression | **AVOIDED.** The guard was applied: §4.2 is reported in four columns and is called a labelling finding. |
| P14 | *my* likely error: manufacturing a dependency out of a citation | **AVOIDED, and it was live.** §7.2 is exactly where I could have committed it — `Op-Form` derives the threshold from the modulus, which looked like a depth-2 L4 dependence. The guard forced me to find the failing step, and support 2 is `F`-free, so the finding **went in `mg-345e`'s favour** instead. |

---

## 10. Defects of THIS instrument, kept in the source

Two of these are the same shape, and **both flatter the party under audit**, which is why
they are on the page.

**D1 — my ledger reader dropped a row, and `mg-345e`'s did not.** The first form demanded
exactly four `|`-separated cells. `Op-Form`'s claim 1 contains `$|A|\le n/2$` — **literal
pipes inside math** — so the row was dropped: **35 rows and 10 edges against `mg-345e`'s 36
and 11**, and because claim 1 is a dependency of claim 17, the eleventh edge went with it.
**`mg-345e`'s greedy regex does not have this defect and ITS numbers are right.** Found by
disagreeing with the parent, **not** by any control of mine. Guarded now by selftest S2.

**D2 — a negative control that scores itself FAILED against correct code.** NC6 asserts
`ε_spec ≠ 2/3` and reports `n = 2`, because `n/(n+1) = 2/3` there **exactly**. A genuine
small-`n` coincidence of the kind `mg-131e` refuted `2/(n+1)` over tonight. Disclosed and
kept rather than tuned away.

**D3 — the census read nothing and returned `mg-345e`'s own number.** `git ls-tree -r`
without `--full-tree`, run from a subdirectory, lists only that subtree. `docs/` matched
nothing and the `1/6` census returned **exactly 2** — which is the number under audit. A
broken instrument agreeing with the audited party is the failure this whole discipline
exists to prevent. Caught only because the verbatim-quote block printed nothing. Guarded
by S6.

**D4 — the depth-2 screen confirmed the verdict by failing to open the evidence.** Bare
relative paths passed to `grep` from this subdirectory found no files, and the screen
printed *"L4-indicator tokens: NONE"* for **every** input. Guarded by S3, which now requires
a missing evidence path to **raise** rather than return clean; the screen also prints the
naive-`mg-id`-grep confound it avoids (an `mg-61bb` grep also hits `STATE.md`'s L1b
blockquote, which is saturated with L4 tokens).

**19 of 19 selftests pass** (`out_selftest6bd1.txt`).

---

## 11. WHAT I DID NOT DO

- **No L4 attempt.** Whether L4-as-stated is provable at an `n`-free modulus is exactly as
  open as it was, and this audit adds nothing to it in either direction.
- **No attempt at the `ε_spec` derivation**, and **no claim about which `1/6` Daniel meant.**
  §5 establishes a **unit identity** between two printed constants. It does not say the
  conjecture is confirmed or refuted, and that question is Daniel's.
- **No poset enumeration, and no independent verification of `mg-210d`'s master bound,
  `mg-61bb`'s coherence result, `mg-92e6`'s diagonal-capacity bound, `mg-3af9`'s branch-(ii)
  theorem, or `mg-2de0`'s `2/3`.** Each was taken at its recorded, audited statement. §3's
  walk asks whether these consume L4 — **not** whether they are true.
- **`C₃` not attempted**, and §5.2 of `mg-345e` is confirmed by reading, not by measurement.
- **The source `.tex` was not opened.** Every `tex:` reference here is at second hand
  through `Op-Form`, which is audited (`mg-e35c`), exactly as `mg-345e` declares of itself.
- **No edit to `STATE.md`, to `Op-Form`, or to `mg-345e`'s deliverable.** This is a
  proposal. `STATE.md` was rewritten three times tonight and `mg-a83c` is queued to rewrite
  it again; editing it from an audit branch would race a landing. Nothing here is urgent
  enough to justify that — corrections 2, 3 and 4 are to `mg-345e`'s document, and
  correction 1 is **already on `STATE.md:15`** via `mg-9adf`'s unit map, which post-dates
  `mg-345e` and says the same thing.
- **I did not read `mg-345e`'s `out_*.txt` files or import `lib345e`** at any point.
- **`n ≤ 40` throughout the grid work**, and `n ≤ 7` for anything brute-forced. Every
  `n → ∞` statement here is a limit of an exact closed form, not an extrapolation from
  data — but it is also not a poset computation, and no poset was enumerated by this audit.
