# mg-b417 — PREDICTIONS for THE u_M FRONTIER

Written and committed **before one line of the search instrument exists**. Everything
below is dated by this commit and by nothing else.

---

## 0. THE EXPOSURE, DISCLOSED AND NOT LAUNDERED

A prediction market with an insider is not a prediction market. What I already knew
when I wrote this file is stated first, in full, because the single largest fact in
this ticket was **found before any instrument of mine existed** and betting on it here
would be fraud.

**H1 (the big one). I HAVE ALREADY FOUND AND CERTIFIED A WITNESS WITH `u_M > 1`, AND IT
WAS ALREADY IN THE CORPUS.** Before writing any search code I read
`code/audit_5cba/out_a5_scope.txt` and
`docs/OneThird-LStar-mg-5cba-IndependentAudit.md`. mg-5cba certified **five** `(L*)`
counterexamples, not four. Its audit table prints a `u_M` column with **four values and
one dash**; the dash is `C5`, `n = 12`,
`dn = (0,0,3,7,15,7,63,2,135,391,7,1159)`. Multiplying the two figures mg-5cba itself
published for that poset gives `u_M >= 1.0234`, and I have certified it in exact
rationals with `lib5cba.py`:

```
gamma < 529992611/8589934592      (R NOT PSD)
mu_pref >= 550121491741/8388608000000   (R COPOSITIVE)
sweep(mu_lo, Delta) - 2 gamma_ub = +0.002790801218  > 0   =>  (M#) FAILS
(F) also fails there  =>  min(c#, f*) >= 1.022616164 > 1
```

So **the DISJUNCTION is false**, it was false in committed evidence before this ticket
was filed, and my ticket's premise — "u_M = 0.981830 at n=10 is the closest any (M#)
witness has come to failing" — is **wrong**, inherited from a table cell that was
blank. Item 3 of my own ticket fired before item 1 began. Mailed to pm-onethird at
the moment of certification.

**Nothing below bets on that.** It is a fact of the corpus at this commit, not a
prediction, and any file of mine that presents it as a search result is lying about
where it came from.

**H2. I have also already derived the identity the trend section is organised around**
(four lines of algebra, no instrument):

```
u_M = v_L * D,     D = (1 + sqrt(1 - 2 gamma / Delta^2)) / 2 < 1
(M#) fails  <=>  v_L > 1 + rho * mu_pref / 2         [rho = mu_pref/gamma]
```

and have checked it reproduces all four published `u_M` figures to six places. So "the
(M#) frontier is the (L*) frontier discounted by `D`" is not a bet either.

**H3.** I know `w(7) = 0.890780` exhaustively and `c_or(8) = 0.943649` exhaustively
from `code/anticorrelation_c50b/`, and that at `n = 7` there are already **4 primitive
posets with `u_M > 1`** where `(F)` holds. So "an unrestricted `u_M` hill climb finds
`u_M > 1`" is a known non-event, not a discovery.

---

## 1. WHAT IS ACTUALLY UNCERTAIN, AND WHAT I BET ON IT

The live question is no longer *whether* the disjunction fails. It is **where it starts
failing, how hard, and whether the corpus's `n <= 8` floor is the real boundary**.

| # | Prediction | p |
|---|---|---|
| **P1** | **A hill climb finds a CERTIFIED `min(u_F,u_M) > 1` at some `n < 12`** — i.e. 12 is not the onset. | **0.65** |
| **P2** | **`n = 9` in particular yields a certified counterexample to the disjunction.** The `(L*)` counterexample region at `n = 9` is known to be broad (6 distinct local optima above 1 from 40 restarts, mg-789d), and `u_M > 1` needs only `v_L > 1 + mu/2`. But `mu ~ 0.12` at both `n = 9` witnesses, so the required excess is ~6% against an observed 1.3%. I think `n = 9` is genuinely hard. | **0.30** |
| **P3** | **The search maximum of `min(u_F,u_M)` is MONOTONE INCREASING in `n` over `9..14`** — no dip. | **0.55** |
| **P4** | **The winning direction is SMALL `mu_pref`, not large `v_L`.** Formally: the champion at each `n >= 12` has smaller `mu_pref` than the median `(L*)` counterexample at that `n`. This is the whole content of `v_L > 1 + rho*mu/2` and it is the one structural claim I am willing to be wrong about in public. | **0.75** |
| **P5** | **`u_M` does NOT saturate**: the certified search maximum at `n = 14` exceeds the `n = 12` value `1.023414` by at least 0.02. | **0.50** |
| **P6** | **At least one champion the fast screen hands up FAILS to certify** — i.e. `mu_ub` over-states it across 1 at least once, and the exact stage refuses it. This is the arm that makes the screen's direction load-bearing rather than decorative. | **0.60** |
| **P7** | **The `(F)`-failing constraint binds.** At every `n`, the argmax of `u_M` over ALL primitive posets found by search has `u_F < 1` — i.e. the free `u_M` maximiser is never a disjunction counterexample, and the two searches must be run separately. | **0.70** |
| **P8** | **The champion posets at `n = 12..14` have height 4**, as all five certified `(L*)` counterexamples do. | **0.60** |

**Falsifiers, stated in advance.** P1 is falsified by 12 remaining the smallest certified
`n` after the declared restart budget — *and that is a SEARCH result, not a proof that
9/10/11 are clean*, and I will write it that way or the prediction is worthless. P4 is
falsified by champions whose `mu_pref` is at or above the counterexample median. P6 is
falsified by every screened champion certifying, which would mean the screen is tight
here and the two-stage design bought nothing.

---

## 2. ERRORS I EXPECT TO MAKE, FILED BEFORE THEY HAPPEN

**E1. I WILL BE TEMPTED TO REPORT A SEARCH MAXIMUM AS A MAXIMUM.** My own ticket bars
`0.968818` at `n = 8` from being quoted as a maximum and says the same bar applies to
anything I find. Every number this tree produces at `n >= 9` is a **SEARCH** figure over
a population it did not enumerate, and it must carry that word in the same sentence as
the digits. `min(u_F,u_M) >= x`, never `= x`.

**E2. THE SCREEN OVER-STATES THE THING I AM REPORTING.** mg-789d's `mu_ub_float` is an
UPPER bound on `mu_pref`, which is exactly right for *hunting* (nothing is missed) and
exactly wrong for *reporting a maximum* (everything is inflated). This tree uses it to
hunt and must never print a figure derived from it as a result. mg-5cba's R6 is this
error, already committed once in this thread, at four rows of one table.

**E3. I WILL CONFLATE `max u_M` WITH THE FRONTIER.** `u_M > 1` alone is not a
disjunction event — it happens at 4 primitive posets by `n = 7`. The frontier is
`max_P min(u_F, u_M)`. A hill climb pointed at bare `u_M` reports a spectacular and
meaningless result on day one.

**E4. `u_M` AND `c#` ARE TWO NUMBERS SHARING ONE PREDICATE** (mg-0d1b, and its
interchangeability is population-bound). I will print both at every witness rather than
quoting one and naming the other.

**E5. THE CERTIFICATE DIRECTIONS ARE OPPOSITE FOR "HOLDS" AND "FAILS".** mg-5cba
certified `(M#) HOLDS` at C1–C4 with `mu` from ABOVE and `gamma` from BELOW. To certify
`(M#) FAILS` I need `mu` from BELOW and `gamma` from ABOVE — the *hard* direction for
`mu`, requiring exact copositivity, which is the trap mg-51f4 named. Getting this
backwards produces a confident counterexample out of nothing. **I made a version of
this error already**, in my first interactive check, by pasting `2*gamma_ub` into a
slot expecting `gamma_ub` and reading `u_M >= 0.49`; it was caught because the answer
moved the wrong way, not because anything checked it.

**E6. `mu_bracket`'s LOW END IS SEEDED FROM A FLOAT AND IS NOT TESTED BY THE LOOP.**
`lib5cba.mu_bracket(lo=...)` only ever raises `lo` when `mu_ge(mid)` returns True; if no
mid ever passes, the returned `lo` is the *unverified seed*. Every certificate this tree
prints must re-assert `mu_ge(m_lo)` as a standalone call, not inherit it from a bracket.
Same for `gamma_ge(g_ub)` being False.

**E7. A LIFTED SEED IS NOT AN INDEPENDENT RESTART.** If I seed `n+1` from the champion
at `n`, the resulting family is one trajectory wearing six hats, and reporting "6
restarts agreed" would be reporting my own seed six times. Random restarts and lifted
seeds are counted and reported **separately**.

**E8. I HAVE ALREADY BEEN HANDED THE ANSWER AND MAY BUILD A SEARCH THAT CONFIRMS IT.**
The n=12 witness is in my hands before the search exists. A search whose population,
seeds and move set are chosen after seeing the target can rediscover it and prove
nothing. The random-restart arm is therefore run with seeds fixed in this file
(`20260810`) and **without** C5 in its seed list, so that "the climb reaches n=12-class
posets on its own" is a claim that can fail.

**E9. THE `(L*)`-GAP POPULATION IS FIVE POSETS.** "Hill-climb from the (L*)-gap
population" sounds like a population and is a handful. Any distributional statement I
make about it ("the champions have smaller `mu`") is over `n <= 5` observations per
class and I will say the count next to the claim.

---

## 3. WHAT THIS TREE WILL NOT DO

- **No `n = 8` census.** Barred by the ticket, and nothing here needs it.
- **No attempt to weaken `(L*)` into survival.** The depth table measured that door shut.
- **No claim about `C_3`.** A dead route is a dead route, not a dead conjecture.
- **No new onset figure without its population and its ref.** Three successive
  statements of the `rho*Delta` onset were wrong in this thread. If I say "the
  disjunction first fails at `n = k`" I will be saying "first **exhibited** at `n = k`,
  over the population I searched, at this commit" — or I will not say it.
