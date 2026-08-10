# (L*) IS FALSE — refuted at n = 9, exactly, on integers

**mg-789d.** Successor to mg-c50b, filed on its own recommendation.

---

## 0. The result, in one line

The ticket asked for a proof of

> **(L\*)**  `M^2 > 2*gamma`  ⟹  `mu_pref * Delta_P <= gamma`

— the single inequality that would have delivered the two-route disjunction **uniformly
in n**, certified at 168/168 (n = 7), at 3589/3589 of an n = 8 screen, and on every
member of (F)'s own family out to n = 18.

**(L\*) is false.** It fails first at **n = 9**, at

```
dn = (0, 1, 0, 4, 0, 0, 32, 96, 239)        n = 9,  LE = 1890,  height 4
```

where, in exact rationals,

```
Delta = 62/63,   M = 41/84
(F) FAILS      : gamma  <  M^2/2 = 1681/14112              [integer PSD test FAILS]
gamma          <  23459/200000  = 0.117295                 [certified upper bound]
mu_pref        >= 6011/50000    = 0.120220                 [certified: Q - sN COPOSITIVE]
mu_pref*Delta  >= 186341/1575000 = 0.1183117  >  gamma
```

so the hypothesis of (L\*) holds and its conclusion fails. **Four** counterexamples are
certified this way in total — two at n = 9, one at n = 10, one at n = 11 — and a hill
climb at n = 9 reached **6 distinct local optima above 1** from 40 restarts, so this is a
region and not a fluke. This is the ticket's **outcome (b)**.

**What it does not cost.** (L\*) was *sufficient* for the disjunction, not equivalent to
it. At all three counterexamples **(M#) still HOLDS** — `u_M = mu_pref/t*` is
0.943, 0.982, 0.958 — so the disjunction survives. What died is the *route*: the
disjunction again has no uniform-in-n proof, only the n ≤ 8 enumerations.

---

## 1. Why the hunt was aimed where it was

(L\*) rearranges, with no loss, to

> **(L\*)** ⟺ `Delta_P * (rho_P - 1)  <=  1 - Delta_P  =  min_i (S_P)_ii`,  where `rho = mu_pref/gamma`

(divide `rho*Delta <= 1` by nothing; subtract `Delta` from both sides). Read this way the
lemma says: *the monotone cone's deficiency `rho - 1` must be no larger than the pinning
of the least-pinned element.* The room it leaves **shrinks to nothing as any element
becomes free**, and the (F)-failing posets — a thin cut between two internally mixing
blocks — are exactly the ones that drive `Delta -> 1`.

That is the whole geometry of the problem, and it is what mg-c50b's own numbers were
already saying: the measured margin `max rho*Delta` over the (F)-failing set went
**0.923894 (n = 7) → 0.968818 (n = 8)**. This ticket does not extrapolate that (mg-c50b
declined to and so does this document); it went and looked at n = 9.

**Two mechanisms that had never been run at once.** `rho > 1` needs a *free element whose
natural label disagrees with where the Fiedler vector wants it* — mg-c50b's chain+point
family. `(F)` failing needs a *thin cut between mixing blocks* — mg-c50b's near-ordinal
antichain family. Each of mg-c50b's two families runs exactly one of the two. The
counterexample runs both: `Delta = 62/63` because element 5 sits at position 5 with
probability 1/63 (nearly free), while the rest of the poset carries the thin cut. **That
is why neither family found it**, and it is why the search here varies the *labelling* as
well as the relations — the population is *naturally labelled* posets, and `gamma`,
`Delta`, `M`, `mu_pref` all move when the labelling moves.

---

## 2. The certificate, and why the easy direction is the wrong one

Refuting (L\*) at `P` requires **both**

* `M^2 > 2 gamma` — an *upper* bound on gamma; and
* `mu_pref * Delta > gamma` — a **lower** bound on `mu_pref`.

The lower bound is the hard direction and it is precisely the trap mg-51f4 names and
mg-c50b records as its E3: an *exhibited* monotone vector bounds `mu_pref` from **above**
and can never certify that `mu_pref` is large. The hunt scores posets with such an upper
bound — correct for *screening*, because a screen that can only over-state the hunted
quantity cannot hide a counterexample — and worthless as proof.

So `mu_pref >= s` is certified by **exact copositivity**. In the psi basis
`mu_pref = min over c >= 0 of c'Qc/c'Nc`, so

```
mu_pref >= s = a/b   <==>   Q - sN copositive   <==>   b*n*QI - 2*LE*a*NI  copositive
```

an *integer* matrix. Copositivity is decided exactly: the minimum of `c'Rc` over the
standard simplex is attained at a point all of whose support coordinates are positive,
where the first-order condition is `R_S c_S = t*1` with value exactly `t`; enumerating
every support `S` and solving in `Fraction`s decides the sign with no floating point
anywhere. A singular face is **refused**, not guessed at.

`gamma < g` is certified by the corpus's own integer PSD device, run in the failing
direction.

**Controls, run before the candidates** (`s5` §5.1–5.2):

| control | expected | got |
|---|---|---|
| mg-c50b S4.1 argmax `(0,0,0,4,4,31,29)`, ρΔ = 0.923894 | **not** a counterexample | not a counterexample |
| mg-c50b S2.2 witness `(0,0,0,0,15,11,15)`, ρ = 1 | **not** a counterexample | not a counterexample |
| chain(9)+point, mg-c50b publishes ρΔ = 1.00636 | `mu_pref*Delta > gamma` **certified** | certified; (F) holds, so (L\*) untouched |

The third is the one that matters: it shows the copositivity machinery can certify the
hard direction *on a poset whose answer the corpus already publishes*, so a "refuted"
verdict on the candidates is not an artefact of a certifier that says yes to everything.

---

## 3. The three routes that were tried first, and are now closed

Before the hunt, three structural routes to (L\*) were proposed and measured on the whole
exhaustive n = 7 (F)-failing set. All three are **sufficient** for (L\*) and all three are
strictly stronger, so refuting them costs (L\*) nothing — but it closes the natural
attempts, which is what mg-c50b's obstruction did for the scalars.

| route | statement | max over the 168 | verdict |
|---|---|---|---|
| **(R1) prefix-tightness** | `R*Delta <= 1`, `R = min_k n*leak(A_k)/(gamma*k(n-k)) >= 1` | **1.020090** | **REFUTED** (holds at 166/168) |
| **(R2) rearrangement** | `W*Delta <= 1`, `W = E(g-down)/E(g)` for the Fiedler vector `g` | **12.871823** | **REFUTED** (holds at 35/168) |
| **(R3) cone invariance** | rows of `A` stochastically ordered ⟹ `rho = 1` | — | **TRUE, and proved** — but covers only **4 of 168** |

**(R1) is the important negative.** `R` is built from a *single prefix indicator* — the
object routes (F) and `c_true` are already phrased in. Its refutation says the corpus's
existing prefix machinery cannot reach (L\*) on its own. The **depth table** (`s3`) makes
this exact: writing `v_j` for `mu_j*Delta/gamma` with `mu_j` the best nonincreasing test
function taking at most `j+1` values,

```
 j (cuts) |  max v_j  | v_j <= 1 at
    1     |  1.020090 | 166 of 168      <- single prefix indicators: REFUTED
    2     |  0.942841 | 168 of 168
    3     |  0.930123 | 168 of 168
    4..6  |  0.923894 | 168 of 168      <- = the full cone
```

So at n = 7, (L\*) needs **at least two cuts** and no more than four. That is a fact about
the posets, not a choice of proof.

### Theorem A (new, proved, uniform in n)

Let `A = (S_P + S_P^T)/2`. Say `P` is **stochastically ordered** if
`sum_{j<=k} a_{i,j} >= sum_{j<=k} a_{i+1,j}` for every `i < n` and every `k`. Then
`mu_pref(P) = gamma(P)`, hence `rho = 1` and (L\*)'s conclusion holds at `P` outright —
with or without the (F) hypothesis.

*Proof.* (1) The hypothesis is exactly the statement that `A` maps the monotone cone
`C = {f_1 >= ... >= f_n}` into itself: for `f` in `C`,
`(Af)_i - (Af)_{i+1} = sum_j u_j f_j` with `u_j = a_ij - a_{i+1,j}` and `sum_j u_j = 0`,
so Abel summation gives `sum_{k<n} U_k (f_k - f_{k+1})` with `U_k = sum_{j<=k} u_j >= 0`,
a sum of products of nonnegatives. (Taking `f = 1_{A_k}` gives the converse.)
(2) `A' = (I+A)/2` is symmetric doubly stochastic with spectrum in `[0,1]`, the constants
at 1, and `A'C ⊆ C`. (3) In `V = R^n/<1>` the image of `C` is a **proper** cone — `C`'s
lineality space is exactly the constants, so it is closed and pointed, and strictly
decreasing vectors are interior. (4) The spectrum of the induced map is
`{(1+lambda_i)/2 : i >= 2}`, all nonnegative, so its spectral radius is `(1+lambda_2)/2`.
(5) Perron–Frobenius for cone-preserving maps (Krein–Rutman; Berman–Plemmons Ch. 1
Thm 3.2) gives an eigenvector for the spectral radius **inside** the cone. (6) Lift to the
centred representative: `A'f = ((1+lambda_2)/2) f + c*1`, and pairing with `1` forces
`c = 0`, so `Af = lambda_2 f`. (7) `f` is nonincreasing, centred, nonzero, with Rayleigh
quotient `1 - lambda_2 = gamma`; since `mu_pref >= gamma` always, `mu_pref = gamma`. ∎

Machine-checked at **every one of the 90655 primitive posets of n ≤ 7** (`s4`): 338 of
them satisfy (SO) and `rho = 1` at all 338, with no exception at any n. The converse is
false at every n ≥ 3 (e.g. 906 posets have `rho = 1` at n = 6 but only 281 satisfy (SO)),
so (SO) is a criterion and not a restatement. The negative control runs too:
chain(n-1)+point violates (SO) by 0.375…0.4375 at n = 8…16, exactly where `rho > 1`.

Its honest coverage of the (F)-failing set is **4 of 168 (2.4%)**, and it is reported at
that value. It *cannot* be pushed past 24 of 168 (14.3%) by any argument of this shape,
because only 24 have `rho = 1` at all; at the other 144, (L\*) is a genuine inequality
between two different numbers rather than an identity.

---

## 4. `LSTAR(n)`: the one number

`(L*)` is exactly the statement that no poset has both of

```
v_F = M^2/(2 gamma) > 1     ((F) fails)          v_L = mu_pref*Delta/gamma > 1   ((L*)'s conclusion fails)
```

so define `LSTAR(n) = max over primitive P on [n] of min(v_F, v_L)`; (L\*) holds at `n`
iff `LSTAR(n) <= 1`. This is to (L\*) what `c_or(n)` is to the disjunction, and it had
never been computed.

```
 n | primitive |  LSTAR(n)   | status
 3 |         4 |   0.250000  | exhaustive
 4 |        27 |   0.306250  | exhaustive
 5 |       275 |   0.550747  | exhaustive
 6 |      4070 |   0.794253  | exhaustive
 7 |     86278 |   0.923894  | exhaustive
 8 |   2600369 |  >= 0.968818 | SEARCH ONLY -- see the scope note below
 9 |         - |  >= 1.013539 | SEARCH ONLY -- (L*) FALSE
10 |         - |  >= 1.020310 | SEARCH ONLY -- (L*) FALSE
11 |         - |  >= 1.025044 | SEARCH ONLY -- (L*) FALSE
12 |         - |  >= 1.057643 | SEARCH ONLY -- (L*) FALSE
```

`LSTAR(7) = 0.923894` at `(0,0,3,3,15,2,3)`, and it equals mg-c50b's `max rho*Delta` over
its (F)-failing set — as it must, since at n = 7 the maximiser has `v_F > 1`. The rows
from n = 8 down are **lower bounds from search, never maxima over their n**.

**Non-vacuity, sharper than the corpus had it.** mg-c50b established that `rho*Delta > 1`
does occur, citing chain+point from n = 10. It occurs **from n = 6**: over all 4070
primitive posets at n = 6, `max rho*Delta = 1.15672` (`s2` §2.4). So the (F) hypothesis in
(L\*) is load-bearing four values of n earlier than the corpus knew.

### Scope note on n = 8 — the one place this document declines to close

n = 8 was pushed with **60 hill-climb restarts** and topped out at `min(v_F,v_L) =
0.968818` at `(0,0,2,0,8,24,63,62)`. That number is *exactly* mg-c50b's published n = 8
maximum of `max rho*Delta` over its (F)-failing set, at a relabelling of their argmax —
an independent re-derivation of their figure by a different method.

It is **not** a census. n = 8 has 2600369 primitive posets and this examined a vanishing
fraction. mg-c50b's own n = 8 statement about (L\*) is over the survivors of a 0.85 screen
(their `s5` scoping note), and that screen was designed for the *disjunction*, not for
(L\*) — `v_L > 1` does not imply `c# > 0.85`. **Whether (L\*) already fails at n = 8 is
open.** "First failure at n = 9" is a statement about what has been *exhibited*.

---

## 5. The instrument

`code/lstar_789d/lib789d.py` works in **f-space** — functions on positions — where
mg-c50b's instrument works in the `psi_k` coefficient basis. The dictionary
(`c'Qc = f'(I-A)f`, `c'Nc = ||f - fbar||^2`, `{c >= 0}` = nonincreasing `f`) is **verified
exactly at every poset of n ≤ 6**, as a machine identity and not an assumption (`s0` A3).

f-space buys the thing the obstruction demands: the faces of the monotone cone become
**consecutive-block partitions of the positions**, so `mu_pref` is computable **exactly in
both directions** by face enumeration, where the parent has an exhibited-vector upper
bound and a copositivity bracket.

**Reproduction of mg-c50b, to every printed digit** (`s0` A6–A7): population counts
1/4/27/275/4070; `max rho` 1.085410 / 1.141242 / 1.217605 at n = 4,5,6; the S2.2 witness
`(0,0,0,0,15,11,15)` at `gamma = 0.043382`, `rho = 1.000000`, `rho*Delta = 0.769231`,
`f* = 1.223785`; the S4.1 argmax at `rho*Delta = 0.923894`; the n = 8 argmax at
`Delta = 62/65`, `Phi* = 1/26`, `M = 723/2080`, `gamma = 0.047583`; the chain+point family
at n = 10, 12, 16. The n = 7 (F)-failing count re-derives at **168**.

### Two defects of my own, both kept

**D1 — a control that was one-sided, read as if it were two-sided.** `mu_ub_float`
originally returned `lambda_min` of a face's *subspace* without checking the minimiser is
nonincreasing. On the face with every cut present that subspace is all of `R^n`, so the
method returned `gamma` at every poset — a *lower* bound where an upper one was needed —
and the first hunt read `rho = 1` everywhere. My validation scored it as
`max(mu_ub - mu_exact)`, which is **blind to `mu_ub < mu_exact`**, exactly the direction
the defect went. Caught by cross-checking against the independent `mu_faces` path, which
disagreed with my own self-test. `s0` arm A5b now asserts **both** signs separately.

**D2 — a self-test arm that was simply wrong.** I asserted `chain gamma > 0`, reasoning
from the path graph's `1 - cos(pi/n)`. A chain has `LE = 1`, so `S_P = I`, `A = I` and
`gamma = 0` exactly; the arm failed and the *arm* was the error, not the code. Kept as a
live arm asserting `gamma == 0` **and** that the chain is not primitive.

D1 is the one that matters: had it not been caught, this document would have reported
`rho = 1` universally and concluded (L\*) trivially true.

---

## 6. Status ledger

| claim | status |
|---|---|
| (L\*) is false, first exhibited at n = 9 | **CERTIFIED** — 4 posets (2 at n=9, 1 each at n=10,11), exact rationals, integer PSD + exact copositivity |
| the n = 9 failure is a region, not a point | **MEASURED** — 6 distinct local optima above 1 from 40 restarts |
| the disjunction survives at all three counterexamples ((M#) holds) | **MEASURED**, `u_M` = 0.943 / 0.982 / 0.958 |
| (R1) single-prefix route to (L\*) | **REFUTED** at n = 7, 2 of 168 |
| (R2) rearrangement route to (L\*) | **REFUTED** at n = 7, 133 of 168 |
| Theorem A: stochastically ordered ⟹ `rho = 1` | **PROVED**; machine-checked at every primitive poset n ≤ 7; covers 4/168 |
| (L\*) needs ≥ 2 cuts and ≤ 4 cuts at n = 7 | **MEASURED**, exhaustive over the 168 |
| `max rho*Delta` over all primitive n = 6 posets = 1.15672 | **MEASURED** — the (F) hypothesis bites from n = 6 |
| `LSTAR(n)` at n ≤ 7 | **EXHAUSTIVE** |
| `LSTAR(n)` at n ≥ 8 | **SEARCH ONLY** — lower bounds, never maxima |
| whether (L\*) already fails at n = 8 | **OPEN** — 60 restarts reached 0.968818, not a census |

## 7. What the successor should do

1. **Settle n = 8.** An exhaustive n = 8 pass on `min(v_F, v_L)` with a screen built for
   `v_L` (not for `c#`) would turn "first failure at n = 9" into a theorem or move it to
   n = 8. mg-c50b's screen does not cover this question and its own scoping note says so.
2. **Do not repair (L\*) by weakening it.** The depth table says any surviving prefix-side
   statement needs ≥ 2 cuts at n = 7 already; the n = 9 counterexample uses the full cone.
3. **The disjunction is again unproved uniformly in n.** The two mechanisms that combine
   to kill (L\*) — a nearly-free element and a thin cut, in the same poset — are the place
   to look for whether they can also make *both routes* fail. They do not at n ≤ 11 (`s6`
   §6.1), and `u_M` there reaches **0.982**, which is closer than any published figure.
