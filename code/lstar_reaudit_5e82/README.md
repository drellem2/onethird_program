# mg-5e82 — INDEPENDENT RE-AUDIT OF THE n = 12 VERDICT

> ## VERDICT: **CONFIRMED.**
>
> Both routes fail at `dn = (0,0,3,7,15,7,63,2,135,391,7,1159)`, n = 12, LE = 10584,
> re-certified on an instrument that imports none of `lib5cba`, `lib789d`, `libc50b`.
> Every published figure reproduces to every printed digit. **The disjunction
> `(F) ∨ (M♯)` is FALSE. It is not a theorem uniform in `n`, and the `(F)`-or-`(M♯)`
> route to `C₃ = 1` does not close.**
>
> **AND THE ONSET ROW IS CONFIRMED TOO, WHICH THE TICKET DID NOT ASK FOR.** cb417
> landed at `5e31a13` while this audit was running, carrying 26 witnesses at
> `n = 10..14`. The `n = 10` row — the tightest margin in the corpus, `min(c♯,f*) =
> 1.000546`, **42× tighter than the n = 12 one it displaced** — re-certifies here on
> this instrument, from this instrument's own rationals. So the negative does not
> depend on `n = 12` and does not depend on `lib5cba`.

---

## 0. THE THREE EXPOSURES, RANKED BY pm-onethird, ANSWERED IN THAT ORDER

| | what it is | verdict | how |
|---|---|---|---|
| **(i)** | `μ_pref ≥ m_lo` by exact copositivity — the hard direction, no exhibited vector can produce it | **ESTABLISHED** | `R(m_lo)` is **COPOSITIVE**, 2047 of 2047 faces visited, `a3` |
| **(ii)** | `γ < g_ub` by the PSD device refusing | **ESTABLISHED** | one exhibited integer vector, 11 entries, all `≤ 10⁵`, `a2` |
| **(iii)** | `sweep(m_lo,Δ) > 2·g_ub` in `Fraction`s | **ESTABLISHED** | margin `+0.002790801218`, `a4` |

All three. On the ticket's own routing that is **CONFIRMED**, not PARTIAL.

---

## 1. THE NUMBERS, AND THEY ARE cb417's NUMBERS

```
Delta   = 195/196                          re-derived   MATCHES
M       = 7717/21168                       re-derived   MATCHES
LE      = 10584                            re-derived   MATCHES
n       = 12, primitive, naturally labelled, transitively closed        ALL FOUR HOLD

gamma   < g_ub = 529992611/8589934592      = 0.061699260375462   [R(g_ub) NOT PSD]
mu_pref >= m_lo = 550121491741/8388608000000 = 0.065579592197061 [R(m_lo) COPOSITIVE]

(F)  FAILS :  g_ub < M^2/2 = 0.066451892088930
(M#) FAILS :  sweep(m_lo,Delta) = 0.126189321969173  >  2*g_ub = 0.123398520750925

  exact margin  =  9622873671904623050657031 / 3448068464705536000000000000
                =  +0.002790801218          cb417 reports +0.002790801218

  f*         >  1.077028990       cb417: 1.077028990
  c#         >  1.022616164       cb417: 1.022616164
  min(c#,f*) >  1.022616164       cb417: 1.022616164
  u_M        >= 1.023413503       cb417: 1.023413503
```

**AND, SEPARATELY, HOW MUCH ROOM THERE ACTUALLY IS.** The published bounds are tight
against the true values, so this audit brackets both exactly rather than only checking
the inequalities:

```
gamma    in [0.061699260334344, 0.061699260334344]     g_ub - gamma  = 4.11e-11
mu_pref  in [0.065579592197861, 0.065579592197861]     mu_pref - m_lo = 8.00e-13
```

`m_lo` sits **8·10⁻¹³** below the true `μ_pref`. That is not a hazard — it is exact
rational arithmetic and the certificate is a certificate — but it is worth stating
where a reader might assume slack. **Both bounds are loose in the SAFE direction:**
`(F)` needs `γ < M²/2` and `(M♯)` needs `sweep > 2γ`, and raising `g_ub` or lowering
`m_lo` makes *both* harder. A loose bound here can only weaken the claim, never
inflate it. The margin that matters is `+0.00279`, and it stands against slacks seven
and ten orders of magnitude smaller.

---

## 2. WHY THIS IS NOT THE SAME INSTRUMENT

`lib5e82.py` re-derives every object from the definition. Arm `S0` checks the
independence **on the parse tree**, not on the source text, and there is a reason:

> My first version of that arm grepped for lines containing both `import` and a
> forbidden name. **It went RED on its own docstring** — the sentence *"This audit
> imports none of lib5cba / lib789d / libc50b"* contains both. That is mg-a0d6's D6
> committed a second time, inside an audit of instruments that agree with themselves.
> A text scan cannot tell a claim from a binding; `ast` can, and it also catches an
> `importlib` call that a grep for `import` would miss.

**TWO PLACES WHERE THE METHOD DIFFERS, NOT ONLY THE AUTHORSHIP.** cb417's own D5
records that `lib5cba`, `lib789d` and `libc50b` agree on `Δ`, `M` and `LE` but all
three descend from **one reading of one derivation** — three agreeing is not three
independent. So:

1. **NO TRANSPORT DP AT ALL.** This instrument **enumerates every one of the 10584
   linear extensions** and counts `PI[i][j]` by tallying. The definition of `PI` is
   *"how many linear extensions place `i` at `j`"*; this counts exactly that. There is
   no recursion over order ideals to get wrong. The generator's **completeness** is
   checked by brute force against filtering all `n!` permutations at every naturally
   labelled poset of `n ≤ 6` (5231 posets) and 259 of the 96428 at `n = 7` — because
   a generator that silently DROPS extensions would lower `LE` and move every scalar
   below it, and checking only that each sequence produced is valid would not see it.
2. **THE PSD TEST IS A CONGRUENCE, NOT A CHARACTERISTIC POLYNOMIAL.** The corpus reads
   PSD off the coefficient signs of `det(xI+A)`. This uses exact symmetric congruence
   with a tracked basis, which yields the inertia *and an exhibited rational vector*
   when the answer is no.

`Q` and `N` are built **from the definition** (`Q_kl = ψ_k'(I−A)ψ_l`) and the corpus's
closed forms are then **checked against them** rather than used to build them. Both
agree. The scaling `R(a,b) = b·n·QI − 2·LE·a·NI = 2·LE·n·b·(Q − tN)` is re-derived and
verified entrywise in `Fraction`s.

---

## 3. (ii) THE PSD REFUSAL — ONE VECTOR, AND YOU CAN CHECK IT BY HAND

`R(g_ub)` has inertia `(+10, −1, 0)`. The refusal needs none of that. It needs one
vector:

```
c = [1129, 100000, 23020, 6888, 274, 2905, -14157, 13206, 1770, -1380, 1933]

c' R(g_ub) c  =  -1000754663691312     <  0
```

Eleven integers, none above `10⁵`, and one dot product. **No algorithm of mine has to
be trusted for `γ < g_ub`.** Read as a Rayleigh quotient the same vector gives
`c'Qc/c'Nc = 0.061699260359122 < g_ub`.

---

## 4. (i) THE COPOSITIVITY — THE ONE THAT MATTERS

There is **no certificate of this shape** for `μ_pref ≥ m_lo`, and that is the whole
point: an exhibited monotone vector bounds `μ_pref` from **ABOVE** and can never
certify that it is large. mg-51f4 named the trap; mg-c50b records it as its E3. A
"yes" here is the output of a routine, so the routine has to be complete and has to be
shown capable of saying no.

**THE CRITERION IS DERIVED IN THIS FILE, NOT QUOTED.** `R` is not copositive **⟺**
for some nonempty `S ⊆ [m]` the system `R_S y = 1_S, y < 0` is feasible — proved from
the KKT conditions of `min{c'Rc : c ≥ 0, Σc = 1}` in `lib5e82.py`'s docstring, with no
nonsingularity assumption. Arriving at the same criterion mg-5cba uses is a
*re-derivation*, not an inheritance; the implementation is independent and the
Fourier–Motzkin engine is exercised directly by arm `S2` on hand-made systems whose
answer is obvious by inspection, **including the strictness case** `y = (t, −t)`,
which is infeasible strictly and feasible non-strictly.

```
R(m_lo) IS COPOSITIVE                        ==>  mu_pref >= m_lo
faces visited            : 2047   (of 2^11 - 1 = 2047)
singular faces met       : 0
singular faces DECIDED   : 0
```

**MEASURED: 0 SINGULAR FACES AROSE**, which agrees with mg-5cba's own measurement.
Reported as a measurement, so that the completeness upgrade is recorded as
**UNEXERCISED here** rather than as load-bearing. `S2` exercises it where it is needed.

`R(m_lo)` is **not** entrywise nonnegative (48 negative entries of 121) and **not**
PSD, so neither trivial sufficient condition applies. Nor is the routine one that says
yes to everything: `a0` runs it on **Horn's matrix**, which is copositive and is *not*
expressible as PSD + nonnegative, and on Horn with one diagonal entry lowered to
`9/10`, which is not copositive.

### 4.1 THE CONTROL THAT MATTERS IS RUN ON THIS MATRIX, NOT ONLY ON TEXTBOOK ONES

Bisecting the copositivity device gives `μ_pref ∈ [0.065579592197861, …]`. At `t` just
**above** that, the routine must refuse — and it does, handing back a monotone
`c ≥ 0`, support `{0,1,2,3,7,8,10}`, with Rayleigh quotient `0.065579592197861 < t`.
**That exhibited `c` is the upper bound, and it is exactly the direction mg-51f4 warns
about**: it proves `μ_pref ≤ 0.0655795922` and could never prove `μ_pref` is large.
Its quotient is still `≥ m_lo`, so it refutes the bisection point and not the claim.

---

## 5. A STEP THE WORK ITEM'S SUMMARY STATES IN A FORM THAT DOES NOT CARRY IT

The chain

> `μ_pref ≥ m_lo` and `sweep(m_lo,Δ) > 2·g_ub > 2γ` ⟹ (M♯) fails

needs `sweep` to be nondecreasing between `m_lo` and `μ_pref`. `sweep(μ) = 2Δμ − μ²`
**rises on `[0,Δ]` and falls after it**, so the condition the work item lists —
`m_lo ≤ Δ` — is **not by itself** what the argument uses. What it uses is
**`μ_pref ≤ Δ`**.

**THIS IS A SEAM, NOT AN ERROR.** Under the corpus's own clamped reading — mg-5cba §2's
survival proof evaluates `sweep = Δ²` when `μ_pref > Δ` — `sweep` is nondecreasing
everywhere and `m_lo ≤ Δ` *is* sufficient. So both readings are defensible and the
corpus contains both.

**This audit removes the question instead of adjudicating it.** `a3.2` and `a4`
certify `μ_pref ≤ Δ` by an exhibited vector (`c = e₁`, giving `μ_pref ≤ 0.0714286 ≪
Δ = 0.9948980`), and `a4` evaluates **both** readings of `sweep` and shows they agree
here. **The verdict holds under either.**

`a4` also derives, rather than quotes, why the two published forms of the failure
agree: `sweep(μ) − 2γ = −(μ − t*)(μ − t**)` with `t** = Δ + √(Δ²−2γ)`, and
`μ_pref ≤ Δ < t**`, so `c♯ > 1 ⟺ μ_pref > t* ⟺ u_M > 1`.

---

## 6. THE PROVENANCE FINDING — CONFIRMED, AND REFINED IN FORM

Read from `main`, not from this branch.

```
code/audit_5cba/out_a5_scope.txt:52
  LE=10584  Delta=195/196  M=7717/21168  gamma in [0.061699260,0.061699262]  mu_pref >= 0.065579592
```

and, the same two numbers again:

```
docs/OneThird-LStar-mg-5cba-IndependentAudit.md:63
  | **C5 `n=12`** | `195/196` | `0.061699262` | `0.065579592` | `1.057468` | `1.077029` | — |
```

**CONFIRMED IN SUBSTANCE, REFINED IN FORM.** They are not two halves in two places.
They are on **one line** of `out_a5_scope.txt` and again on **one line** of the audit
table — same poset, same `Δ`, both bounds, printed twice on main. Multiplying them is
four lines of arithmetic. `a4.4` does it **using only those published decimals** and
gets `+0.0027907976`, agreeing with pm-onethird's own hand check to eight decimal
places. **This counterexample has been on main since mg-5cba landed.**

### 6.1 THE MECHANISM: A BLANK CELL BECAME A PUBLISHED BOUND

```
:59   C1 `n=9`         u_M = `0.943486`
:60   C2 `n=9`         u_M = **`0.947534`**
:61   C3 `n=10`        u_M = `0.981830`
:62   C4 `n=11`        u_M = `0.958326`
:63   **C5 `n=12`**    u_M = —
```

Five rows, four values, one dash — **confirmed on main**. `STATE.md` then publishes
`(M♯) HOLDS at **4 of 4**` with four figures — **confirmed on main**.

**AND NO STEP IN THAT CHAIN STATED A FALSEHOOD.** The dash is *honest*: mg-5cba did not
compute `u_M` at C5 and did not say it had. `4 of 4` is *true of the four it names*.
mg-b417's inherited sentence — *"`u_M = 0.981830` is the closest any (M♯) witness has
come to failing"* — is true **of the four that were COMPUTED**. What no sentence
carries is that a fifth certified counterexample sits beside them with the cell blank,
and the reader of *"4 of 4"* beside *"FIVE counterexamples certified"* has to notice
the arithmetic unaided. That is the finding, and it is a finding about **blank cells,
not about wrong numbers**.

---

## 7. THE FOURTH SITE — SETTLED, AND NOT TOUCHED

`STATE.md:172` says *"the gap between `(L*)` and `(M♯)` is exactly `μ_pref²`"*.

```
doubled     (L*) conclusion :  2*Delta*mu          <= 2*gamma
            (M#)            :  2*Delta*mu - mu^2   <= 2*gamma      gap = mu^2
undoubled   (L*) conclusion :    Delta*mu          <=   gamma
            (M#)            :    Delta*mu - mu^2/2 <=   gamma      gap = mu^2/2
```

**WHICH NORMALISATION IS THE ROW IN? The undoubled one.** The same row writes `(L*)` as
`M² > 2γ ⟹ μ_pref·Δ_P ≤ γ` — checked mechanically, `a6` P3. mg-5cba §2 displays the
pair in the **doubled** form, where the clause is exactly right. So the clause has
travelled from a display block into a sentence in a *different* normalisation without
its factor of 2; **in the row's own normalisation the gap is `μ_pref²/2`.**

**NOT FIXED HERE, and pm-onethird was right to say so.** It changes no verdict — `a4`
evaluates `(M♯)` from its definition and never uses the gap clause. It is recorded
because it is the mg-0d1b hazard **in the form the alias-agreement check cannot see**:
a factor of 2 between two conventions is indistinguishable, to a value comparison,
from two implementations disagreeing.

---

## 8. SCOPE — EACH CLAUSE SEPARATELY, INCLUDING THE ONES NOT RE-RUN

**`n ≤ 8` IS UNTOUCHED.** Re-derived here **exhaustively at `n ≤ 6`**: `(F)` holds at
every primitive poset, so the `(F)`-failing set is empty and *both routes fail at 0*
for a reason stronger than a census — the conjunction has no candidates at all.
Primitive counts come out `4 / 27 / 275 / 4070` at `n = 3..6`, matching the corpus.
This doubles as a control on this instrument: devices that manufactured route failures
would manufacture them here, where an exhaustive census exists to disagree.

**DECLARED UNVERIFIED, and named rather than passed over:** `n = 7` (96428 / 86278,
recomputed independently by mg-a0d6 in 1443 s, not repeated here) and **`n = 8`
(2800472 / 2600369, `c_or(8) = 0.943649`) — NOT recomputed by anybody in this ticket.**
I assert nothing about it.

**`n = 9, 10, 11` ARE NOT SETTLED BY THIS — AND THE PICTURE MOVED WHILE I WAS WORKING.**
As the ticket was written, this was a lone `n = 12` witness. cb417's landing at
`5e31a13` certifies **`n = 10`**. `a7` re-certifies that row here (§9). The four
original counterexamples at `n = 9, 9, 10, 11` have `u_M < 1` and are **unaffected**;
a refutation of this verdict would not have disturbed them either.

**"THE ONSET IS `n = 10`" IS STILL NOT A CLAIM THIS AUDIT SUPPORTS.** What is supported
is *both routes fail at THIS poset, which has `n = 10`*. `n = 9` was searched with 30
restarts and did not cross; **that is a statement about 30 restarts.** This is mg-5cba's
own R1 hazard — the smallest `n` an instrument looked at, published as the smallest `n`
where the thing happens — and cb417 states the bar itself.

**NOTHING HERE BEARS ON `C₃ = 1`.** `(F)` and `(M♯)` are two **sufficient** routes; their
disjunction is what the dependency diagram consumes. A poset where both fail removes
the **route**, not the **result**. What dies is *"the disjunction is a theorem uniform
in n"* — the same thing `(L*)`'s refutation cost, one level up. Theorem A and the
`n ≤ 8` enumerations stand.

---

## 9. BEYOND THE TICKET: THE ONSET ROW, RE-CERTIFIED

cb417 landed while this audit ran, and its marker covers **the whole tree**. A verdict
that re-certified only C5 would license removing a marker over work it never examined.
The `n = 10` row is also **the most exposed thing in the corpus** —

| | `min(c♯,f*)` | margin over 1 |
|---|---|---|
| `n = 10` (the onset) | `1.000546` | **`5.5e-4`** |
| `n = 12` (this ticket's) | `1.022616` | `2.3e-2` |

— **42× tighter**, and carrying the more consequential claim. So `a7` re-certifies it
here. **No rational is read from cb417; only the posets are.** `γ`'s upper bound is
this instrument's own smallest bisection point where the PSD device refuses, `μ_pref`'s
lower bound its own largest point where copositivity holds.

```
n | this audit                                  | cb417   | agrees
 9 | c# > 0.969346517   (F) holds, does NOT refute | 0.969347 | yes  <- NEGATIVE CONTROL
10 | c# > 1.000546470   sweep - 2g = +0.000058319  | 1.000546 | REFUTES
11 | c# > 1.027641546   sweep - 2g = +0.003161659  | 1.027642 | REFUTES
12 | c# > 1.022616164   sweep - 2g = +0.002790801  | 1.022616 | REFUTES
```

**The `n = 9` row is the control in the other direction**: cb417's own table says its
best `n = 9` champion does *not* refute, and this instrument agrees. A device answering
YES by habit fails there.

So **the disjunction being false does not depend on `n = 12` and does not depend on
`lib5cba`.**

**STILL NOT RE-RUN HERE:** the other 23 certified posets, `W(13)` and `W(14)`, the
`0 of 36` refusal count, the `93.8% / 6.2%` decomposition, and the `u_M = v_L·D`
identity. None was examined.

---

## 10. DISPOSING OF THE MARKER — WHICH IS THIS TICKET'S TO DRIVE

cb417's `README.md:3–14` carries:

> **⚠️ PENDING INDEPENDENT RE-CERTIFICATION — mg-5e82.** *Every verdict in this tree is
> CERTIFIED-PENDING-AUDIT.*

**DISPOSITION: CONFIRMED — and the marker is READY FOR REMOVAL AS TO THE CERTIFIED
COUNTEREXAMPLES AT `n = 10`, `n = 11` AND `n = 12`, NOT AS TO THE WHOLE TREE.**

That is not a hedge, and it is not the ticket's PARTIAL branch either. PARTIAL is
defined over (i)/(ii)/(iii) and **all three are established**. The narrowing is that
the marker's scope is *"every verdict in this tree"*, written for a tree that did not
exist when mg-5e82 was filed, and mg-5e82 was scoped to one poset. Whoever removes it
should:

* **DELETE** the blanket sentence *"Every verdict in this tree is
  CERTIFIED-PENDING-AUDIT"*, and
* **REPLACE** it with a marker naming the surviving exposure — the 23 other certified
  posets, `W(13)`/`W(14)`, the `0 of 36` count, the decomposition and the identity —
  which this audit did not look at.

**The removal is a separate act by whoever lands the `STATE.md` edit, not by me.** I
have edited no document outside this directory.

### 10.1 WHAT MOVES IN `STATE.md`, AND WHAT DOES NOT

Confirmed present on main by `a6` P4, all three at `:172`:

* **(a)** *"AND THE DISJUNCTION SURVIVES IT"* — **FALSE as a general statement.** It
  survives at the four witnesses that carry `u_M < 1`; it does not survive at C5.
* **(b)** *"`(M♯)` HOLDS at 4 of 4, `u_M = 0.943486 / 0.947534 / 0.981830 /
  0.958326`"* — **four figures for five certified counterexamples**, and now for far
  more than five.
* **(c)** *"What is lost is exactly one thing: the uniform-in-`n` proof."* — **the
  uniform-in-`n` proof of the DISJUNCTION is now lost as well**, not only `(L*)`'s.

**NOT MOVED, and checked present on main so that a later edit cannot quietly take them
with it:** the `n = 7` enumeration (`96428/86278`), the `n = 8` enumeration
(`2800472/2600369`), `c_or(8) = 0.943649`, Theorem A, the onset correction, the depth
table.

`STATE.md` stands at **exactly 19,077 words against mg-e331's ceiling of 19,077**, so
the correcting edit requires raising the ceiling in the same commit under mg-e331's
documented procedure. **Both halves of that measured here rather than relayed:**
`git show main:STATE.md | wc -w` = `19077`, and
`code/state_ratchet_e331/CEILING.json` reads `"words_ceiling": 19077`. There is no
slack at all — the edit in §10.1 cannot land without the raise.
**This branch does not touch `STATE.md`.**

---

## 11. DEFECTS OF MY OWN — ALL KEPT

**D1 — THE INDEPENDENCE ARM WENT RED ON ITS OWN DOCSTRING.** My first `S0` grepped for
lines containing `import` and a forbidden name; the sentence *"This audit imports none
of lib5cba / lib789d / libc50b"* matched. **mg-a0d6's D6, committed again by an author
who had read mg-a0d6's D6.** Fixed with `ast`, which also closes an `importlib` hole a
text grep never covered.

**D2 — A RUNTIME I HAD NOT MEASURED, IN THE COMMENT CLAIMING IT WAS MEASURED.**
`run_all.sh` first read `66.3 s`. The measured figure is `52.2 s` (three runs:
52.2 / 54.4 / 52.2). **mg-17aa's D4 in the same place mg-17aa found it.** The sentence
and the measurement were written in the wrong order; both are kept in the file.

**D3 — A CLAUSE THAT COULD NOT FAIL, INSIDE AN AUDIT ABOUT A BOUND NOBODY COMPUTED.**
`a1` contained a comprehension ending `and False` — vacuously true. `a4` contained
`check("mu_pref <= Delta", True, True)` — a scored arm with a constant in it, and it
was scoring **the one side condition §5 shows the argument actually needs**. `a5`
carried three more. All four replaced by real measurements or demoted out of the
scoreboard; the `a4` one now exhibits `c = e₁`.

**D4 — MY SINGULAR-FACE COUNTER WOULD HAVE UNDER-REPORTED.** It incremented only for
rank-deficient faces that were also *consistent*, so *"0 singular faces arose"* could
have meant *"no singular face happened to be consistent"*. Fixed to count every
rank-deficient face; the answer is still 0, but it is now the measurement it claims.

**D5 — THE SCOPE I WAS GIVEN WAS ALREADY STALE WHEN I STARTED.** mg-5e82 describes a
lone `n = 12` witness. cb417's landing had 26 at `n = 10..14`, and I found that only by
re-fetching `main` late in the run. Had I not, I would have returned a verdict
disposing of a marker over a tree four times larger than the one I audited. `a7` exists
because of that, and §10's narrowing is its consequence.

**D6 — WHAT I DID NOT DO.** I did not re-run `n = 7` or `n = 8`. I did not recompute
`c_or(8)`. I did not examine 23 of cb417's 26 witnesses, `W(13)`, `W(14)`, the
decomposition or the identity. I did not search for counterexamples at `n = 9`. Each
is named in §8 and §9 as unverified rather than left to be inferred from silence.

---

## 12. FILES

```
lib5e82.py         the instrument: enumeration, exact PSD by congruence with witness,
                   exact copositivity by support enumeration with Fourier-Motzkin
common5e82.py      the poset and the two published rationals, in one place
a0_selftest.py     independence (ast), both devices on known matrices, Horn, the FM
                   engine directly, LE-generator completeness by brute force at n<=7
a1_witness.py      STEP A -- the poset, by explicit enumeration of all 10584 extensions
a2_gamma.py        STEP B -- gamma < g_ub, one exhibited vector
a3_mu.py           STEP C -- mu_pref >= m_lo, exact copositivity, + the refusal control
a4_routes.py       STEP D -- both failures, the margin, u_M, both readings of sweep
a5_scope.py        STEP E -- n <= 6 exhaustive; what is NOT re-run, named
a6_provenance.py   the two published halves, the dash, STATE.md's four sites (from main)
a7_frontier.py     cb417's onset rows, re-certified; n = 9 as a negative control
run_all.sh         all eight, worst exit wins.  52.2 s measured.
```

`sh run_all.sh` — **8 arms, 0 failures.**
