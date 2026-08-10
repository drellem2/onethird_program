# OneThird — **THE ANTI-CORRELATION IS ONE INEQUALITY, NOT A γ-REGIME COINCIDENCE.** `mg-51f4`'s whole `n = 7` census re-derives **exactly** on an independent instrument; `n = 8` is now **ENUMERATED** — 2800472 posets, 2600369 primitive — and **both routes still fail at 0 of them**, with `c_or(8) = 0.943649`; and the disjunction at both `n` follows from a **single** sufficient condition `ρ·Δ_P ≤ 1` holding on the `(F)`-failing set, **certified on integers at 168 of 168 and 3589 of 3589** and out to `n = 18` on `(F)`'s own family. **The proof the ticket asked for does not exist in the route invariants** — the relaxation is FEASIBLE, and it stays feasible even after adding `C₃^(III) = 1` itself

**Work item:** `mg-c50b` — successor to `mg-51f4`, filed on its own recommendation.
**Scope taken:** the ticket's instruction — *file against the anti-correlation, not against
either route and not against the loss.* Neither route is attacked here. The loss `Λ_M`
appears once, as a reproduction.

---

## §0. THE STATE AFTER THIS TICKET

| | status |
|---|---|
| **`mg-51f4`'s `n = 7` enumeration** | **RE-DERIVED AND CONFIRMED**, exactly, on an instrument sharing no source line with it. `96428 / 86278`, `(F)` false at **168**, `(M♯)` at **4**, both at **0**, and every published constant to every printed digit. The ticket's *"a merge is not a check"* caveat is discharged. |
| **The disjunction at `n = 8`** | **ALIVE, and now EXHAUSTIVE.** 2800472 naturally labelled posets on `[8]`, **2600369 primitive**, **0 with both routes failing**. `c_or(8) = 0.943649`. Never computed before. |
| **The mechanism** | **RESTATED AS ONE INEQUALITY, `(L*)`,** which is uniform in `n` by construction where the γ-bin story could never be. **Certified exactly** wherever the disjunction is at risk: 168/168 at `n = 7`, 3589/3589 at `n = 8`, and every member of `(F)`'s own family to `n = 18`. |
| **A UNIFORM-IN-`n` PROOF of the disjunction** | **STILL OPEN — and now known not to be reachable from the route invariants.** §5 exhibits a point satisfying *every* unconditional inequality this corpus holds at which **both routes fail**. Any proof must use the poset, not the five scalars. |
| **`mg-51f4` §7's stated mechanism** | **ITS STATED FORM IS FALSE.** *"a poset with a very thin bottleneck has a Fiedler vector that **is** monotone — L2's first disjunct holds there"* is false at **144 of the 168**. Only its **quantitative** form survives: `ρ ≤ 1.0238` there. `mg-51f4` labelled it a conjecture; this is a refinement, not a withdrawal. |
| **The `n` the architecture consumes** | `n ≥ 99`. **Nothing here reaches it.** Exhaustive to `n = 8`; two families to `n = 16`–`18`, every row labelled FAMILY. |

**The one-sentence version.** The two routes' failure sets are disjoint not because they
occupy disjoint γ bands — a γ band is not a statement that can be uniform in `n` — but
because at every poset where `(F)` fails the monotone cone price `ρ = μ_pref/(1−λ_std)` is
within `2.4 %` of 1 and `ρ·Δ_P` is under `0.93`, which is *by itself* enough to give `(M♯)`;
and that single inequality, not the 86278 separate checks, is what the successor should
try to prove.

**What may not be quoted without its scope.** `c_or(8) = 0.943649` and the population
`2800472 / 2600369` are **exhaustive at `n = 8`**. `c_or(7) = 0.894472`, `c♯ = 1.018707`,
`f* = 1.297074`, `c_true(7) = 0.340719` are exhaustive at `n = 7`. **Every family number
carries the word FAMILY and is not a maximum over its `n`.** `c_or` is **not** extrapolated
here and must not be; §3 says why the last increment does not license it.

---

## §1. THE RE-DERIVATION — THE TICKET'S OWN CAVEAT, DISCHARGED

The ticket: *"onethird_program HAS NO QUALITY GATES … The `n = 7` enumeration underneath
this entire ticket is UNVERIFIED BY ANY GATE … RE-DERIVE THEM INDEPENDENTLY."*

`code/anticorrelation_c50b/libc50b.py` was written from the corpus's definitions
(`mg-76b2` §2–§3, `mg-28ff` §2–§3) with **`lib51f4.py` unopened**, and stayed unopened
until the census below was committed (`PREDICTIONS.md` H3). It computes the transport by a
down-set dynamic program and decides every verdict on **integer** matrices: with
`(S_P)_{ij} = PI_{ij}/L`, `Q = QI/(2L)`, `N = NI/n`, the test `Q − tN ⪰ 0` at `t = a/b` is
`b·n·QI − 2·L·a·NI ⪰ 0`. No float touches a verdict.

| | `mg-51f4` | **this instrument** |
|---|---|---|
| posets on `[n]`, `n = 2..7` | `2/7/40/357/4824/96428` | **identical** |
| primitive | `1/4/27/275/4070/86278` | **identical** |
| `c_true(n)`, `n = 3..7` | `0.222222 / 0.271353 / 0.308339 / 0.327508 / 0.340719` | **identical** |
| `c♯(n)` | `0.500000 / 0.636846 / 0.803289 / 0.943151 / 1.018707` | **identical** |
| `f*(n)` | `0.250000 / 0.306250 / 0.550747 / 0.811649 / 1.297074` | **identical** |
| `c_or(n)` | `0.250000 / 0.306250 / 0.550747 / 0.753639 / 0.894472` | **identical** |
| `max ρ`, `n = 3..7` | `1.0000 / 1.0854 / 1.1412 / 1.2176 / 1.2762` | **identical** |
| `max Λ_M(7)`, `max Λ_F(7)` | `110.967`, `13.083` | **identical** |
| **`(F)` false at** | **168** of 86278 | **168** |
| **`(M♯)` false at** | **4** of 86278 | **4** |
| **both false at** | **0** of 86278 | **0** |
| both `n = 7` witnesses | §5's two posets | **reproduced to every printed digit** (`s0` A9a/A9b) |

**One difference, recorded rather than smoothed.** `mg-51f4` §7's γ-bin table reads
`21532` in `[0.30, 0.50)` and `1600` in `[0.50, 1]`; I read `21531` and `1601`. Both
columns total 86278. It is one poset at the bin edge and a half-open-versus-closed
convention on the last bin; **no other cell differs and no figure moves.** Not mine to
adjudicate.

**`f*(6)`.** I get `0.811649`, `mg-51f4`'s value, not `mg-28ff`'s `0.811654`. That
resolves the sixth-figure disagreement `mg-51f4` §4 recorded, in `mg-51f4`'s favour, on a
third instrument. `mg-29fe` already found the cause; I only add a vote.

> **THE CENSUS STANDS.** Nothing in `mg-51f4`'s `n = 7` result required a gate. It is
> right.

---

## §2. THE REDUCTION — BOTH ROUTE FAILURES AGAINST ONE THRESHOLD EACH

> **PROPOSITION (exact, unconditional, uniform in `n`).** *With `γ = 1 − λ_std`:*
> $$(F)\ \text{fails at }P\iff M>\sqrt{2\gamma};\qquad
> (M^\sharp)\ \text{fails at }P\iff \Delta_P^2>2\gamma\ \text{ and }\ \mu_{\mathrm{pref}}>t^{*}(P),$$
> $$t^{*}(P)\;=\;\Delta_P-\sqrt{\Delta_P^2-2\gamma}\;=\;\frac{2\gamma}{\Delta_P+\sqrt{\Delta_P^2-2\gamma}}\ \in\ \Bigl[\tfrac{\gamma}{\Delta_P},\ \tfrac{2\gamma}{\Delta_P}\Bigr].$$

**Proof.** `c♯ = sweep(μ,Δ_P)/(2γ)` with `sweep = μ(2Δ−μ)` for `μ ≤ Δ` and `Δ²` beyond. On
the first branch `μ(2Δ−μ) > 2γ ⟺ (μ−Δ)² < Δ²−2γ ⟺ μ > Δ − √(Δ²−2γ)`, which needs
`Δ² > 2γ`. On the second branch `sweep = Δ² > 2γ` is the same condition, and there
`t* < Δ < μ` automatically, so the single form covers both branches. `(F)` is immediate
from `f* = M²/(2γ)`. The bracket on `t*` follows from `Δ ≤ Δ+√(Δ²−2γ) ≤ 2Δ`. ∎

**Machine check.** The reduction's verdict versus the direct verdict at **every one of the
90655 primitive posets `n ≤ 7`: 0 disagreements** (`s2` S2.1). *(This control earned its
keep: its first run reported 4, 20, 105 and 740 disagreements, and the defect was **mine
and in the check**, not in the reduction — I had coded the case `Δ² ≤ 2γ`, where `(M♯)`
**cannot** fail, as `u_M = +∞` instead of `0`. Kept, in `libc50b`'s history and in `s2`'s
comment.)*

> **COROLLARY (two-sided, uniform in `n`, free).**
> $$\rho\,\Delta_P\le 1\ \Longrightarrow\ (M^\sharp)\text{ HOLDS};\qquad
> \rho\,\Delta_P> 2\ \Longrightarrow\ (M^\sharp)\text{ FAILS}.$$

The first half is the floor of `mg-51f4` §2 sharpened from `ρ = 1` to `ρ ≤ 1/Δ_P`; the
necessity half `ρ > 1/Δ_P` is `mg-29fe`'s, and the **sufficiency** half `ρ > 2/Δ_P` is the
other side of it, which the corpus did not carry. Between `1/Δ_P` and `2/Δ_P` the verdict
genuinely needs `t*`.

**Why this matters more than the algebra suggests.** `mg-51f4` §7 states the mechanism as
*"`(F)` exceeds 1 only at `γ < 0.1`; `(M♯)` only at `γ ∈ [0.1, 0.3)`"*. **A γ band names a
constant, and a statement about a named constant cannot be proved uniformly in `n` unless
something forbids the band from moving.** Nothing in the corpus does.

*Measured, because I first wrote that the bands **do** move at `n = 8` and that was an
assertion I had not run.* **They do not, at `n = 8`:** the `(F)`-failing posets there have
`γ ∈ [0.026507, 0.071016]`, **0 of 3589** at `γ ≥ 0.10`. So the band is stable at the one
new `n` I can test — which is evidence *for* the mechanism and still not a route to a
proof, because two points do not pin a constant. What *did* move is the height profile: the
`(F)`-failing set reaches **height 5** at `n = 8` where at `n = 7` it stopped at 3.

The reduction replaces the band with a **scale-free** comparison, and that is the only form
in which the anti-correlation could ever be proved once and for all `n`.

---

## §3. `n = 8` IS ENUMERATED — AND THE DISJUNCTION SURVIVES IT

**Population.** `2800472` naturally labelled posets on `[8]`, of which **`2600369`
primitive**. *(I wrote `2903405` from memory before the run; the run's own count is
`2800472` and the file was corrected.)*

**Method, and exactly what is exhaustive about it.** A full exact treatment of 2.6 M
posets is out of reach; a **rigorous two-stage screen** is not. Since `μ_pref ≤ 2Φ*_pref`
(the centred prefix indicator is monotone, and `n/max(k,n−k) ≤ 2`) and `t ↦ t(2Δ−t)`
increases on `[0,Δ]`,
$$c^{\sharp}\;\le\;c^{\sharp}_{\mathrm{UB}}\;:=\;\mathrm{sweep}\bigl(\min(2\Phi^{*}_{\mathrm{pref}},\Delta_P),\Delta_P\bigr)/(2\gamma),$$
so any poset with `min(c♯_UB, f*) ≤ 0.85` **provably** has `min(c♯,f*) ≤ 0.85`. 7203
survived. Every survivor then got the full exact treatment.

| | at `n = 8` | status |
|---|---|---|
| **BOTH ROUTES FAIL** | **0 of 2600369** | **EXHAUSTIVE and EXACT.** Both failing forces `min > 1 > 0.85` and `c♯_UB ≥ c♯`, so every both-failing poset survives the screen. None did. |
| **`c_or(8)`** | **`0.943649`** | **EXHAUSTIVE.** Every excluded poset provably has `min ≤ 0.85 < 0.943649`. |
| `(F)` failures | **≥ 3589** | **NOT a census** — see below. |
| `(M♯)` failures | unknown | **NOT computed at `n = 8`.** |

> **A DEFECT OF MINE, CAUGHT AND KEPT.** `s3_n8.py` first printed *"`(F)` FAILS at 3589 of
> 2600369"* and *"`(M♯)` FAILS at 0 of 2600369"*. **Both lines state the wrong
> population.** The screen keeps a poset only when `f* > 0.85` **and** `c♯_UB > 0.85`, so a
> poset where `(M♯)` fails while `(F)` is comfortable is screened out and never reaches
> stage 2. The correct readings are: `(F)` fails at **at least** 3589 (those that also have
> `c♯_UB > 0.85`), and **no `n = 8` poset has `(M♯)` failing together with `f* > 0.85`** —
> which says nothing about `(M♯)`'s failure count at `n = 8`. This is `PREDICTIONS.md` E9,
> *a screened population read as an enumerated one*, committed by me at the one place where
> the population changes underfoot. `s5_n8_scope.py` exists only to restate it, and the
> labels in `s3_n8.py` are repaired.

**The argmax.** `c_or(8) = 0.943649` is attained at
`dn = (0,0,2,0,8,24,62,63)`, with `Δ_P = 62/65`, `Φ*_pref = 1/26`, `M = 723/2080`,
`γ = 0.047583`, **height 4**, `c♯ = 0.943649` and **`f* = 1.269610`** — so `(F)` has already
failed there and `(M♯)` is what is holding the disjunction up.

**AND THE MARGIN CLOSED.** I am not going to dress this up:

| `n` | 3 | 4 | 5 | 6 | 7 | **8** |
|---|---|---|---|---|---|---|
| `c_or(n)` | `0.250000` | `0.306250` | `0.550747` | `0.753639` | `0.894472` | **`0.943649`** |
| increment | — | `+0.056` | `+0.245` | `+0.203` | `+0.141` | **`+0.049`** |

The increments continue to decelerate — `+0.049` after `+0.141` — and `c_or` is still
**rising**, now at `0.944` with `5.6 %` of headroom. **Six points after a turnover is not a
trend and I do not extrapolate it**; the architecture consumes `n ≥ 99` and nothing here
comes near it. What the sixth point does establish is that `c_or(7) = 0.894` was not a
ceiling.

---

## §4. THE LEMMA — `(L*)`, AND WHY THE DISJUNCTION IS ONE INEQUALITY

> **`(L*)` (conjectural, uniform in `n` as stated).** *At every primitive poset,*
> $$M^{2}>2\gamma\quad\Longrightarrow\quad \mu_{\mathrm{pref}}\cdot\Delta_P\;\le\;\gamma
> \qquad\text{i.e.}\qquad \rho\le 1/\Delta_P .$$

> **`(L*)` IMPLIES THE DISJUNCTION, UNIFORMLY IN `n`, IN ONE LINE.** By §2,
> `ρ ≤ 1/Δ_P` gives `μ_pref ≤ γ/Δ_P ≤ t*`, hence `(M♯)` HOLDS at every poset where `(F)`
> fails, hence the two failure sets are disjoint at every `n`. ∎

**`(L*)` IS CERTIFIED EXACTLY WHEREVER THE DISJUNCTION IS AT RISK.** The certificate is one
integer PSD test per poset: an exhibited monotone vector gives an *exact* `μ_ub ≥ μ_pref`,
and `PSD(Q − μ_ub Δ_P N)` gives `γ ≥ μ_ub Δ_P ≥ μ_pref Δ_P`. **This is the cheap direction**
— refuting `(M♯)` needs a copositivity *lower* bound, which is what stops `mg-51f4` past
`n = 15`, whereas `(L*)` needs only an upper bound and costs `O(n²)`.

| population | `(L*)` certified | `max ρΔ_P` there *(float measurement)* |
|---|---|---|
| the **168** `(F)`-failing primitive posets on `[7]`, EXHAUSTIVE | **168 of 168** | `0.923894` |
| the **3589** `(F)`-failing survivors at `n = 8` | **3589 of 3589** | `0.968818` |
| **FAMILY** near-ordinal antichains, `n = 6..18` (`(F)` fails from `n = 9`) | **every member** | `0.894` at `n = 18` |

> **THE CONSEQUENCE, AND IT IS THE POINT OF THIS TICKET.** The disjunction at `n = 7` is
> **not** 86278 independent checks and at `n = 8` is **not** 2600369. It is **one
> sufficient condition, `ρΔ_P ≤ 1`, holding on the 168 (resp. 3589) posets where it is the
> only thing standing between the two routes** — with a margin, certified on integers at
> every one of them.

**`(L*)` IS NEITHER VACUOUS NOR TRIVIALLY TRUE, AND THAT IS A CONTROL, NOT A REMARK.**
`ρΔ_P > 1` **does** happen — on `mg-51f4`'s own `(M♯)` family, chain(`n−1`) + one isolated
point, `ρΔ_P` crosses 1 at `n = 10` and reaches `1.078` at `n = 16` **(FAMILY)**. It simply
never happens where `(F)` fails: on that family `u_F = M/√(2γ)` runs `0.477 → 0.396`,
falling. So `(L*)`'s hypothesis is doing real work, and both of its arms are live.

**WHAT `(L*)` IS NOT.** It is **not proved**. It is a conjecture with an exact certificate
on two enumerated populations and one family, and it is offered as the successor's target
because it is the first form of the anti-correlation that *could* be uniform in `n`.

### 4.1 `mg-51f4` §7's stated mechanism is false; its quantitative form survives

`mg-51f4` §7, explicitly as a conjecture: *"a poset with a very thin bottleneck has a
Fiedler vector that **is** monotone — L2's first disjunct holds there — which pins `c♯` to
its floor."*

**Measured, exhaustively, over the 168:** `ρ = 1` at **24 of 168**. L2's first disjunct
**fails at 144 of them, 85.7 %.** The stated mechanism is false. What is true is the
quantitative statement it was reaching for: over those same 168, `max ρ = 1.023794` — the
cone price is within **2.4 %** of 1, not equal to it. Since `c♯ = ρΔ_P − ρ²γ/2`, a `2.4 %`
excess is all `(M♯)` gets, and it is not enough.

Dually, over the 4 posets where `(M♯)` fails, `max ρ = 1.231604` and
`min u_F = M/√(2γ) = 0.540079` — **`(F)` sits `46.0 %` below its own failure threshold
there.**

### 4.2 The margin, on the scale the thresholds live on

`c_or` is a maximum over *all* posets. The quantity that prices the disjunction is the
distance of the *second* route from failing **at the posets where the first has already
failed**:

| | `n = 7` | `n = 8` |
|---|---|---|
| `min u_M = μ_pref/t*` over the `(F)`-failing set | `0.739915` (**26.0 %** margin) | `0.790802` (**20.9 %**) |
| `min u_F = M/√(2γ)` over the `(M♯)`-failing set | `0.540079` (**46.0 %**) | not computed |

Both readings — `c_or` and `u`— cross 1 together; they are two parametrisations of the same
event and **neither is more correct than the other**. They are reported side by side
because they close at different *rates*: `c_or` went `0.894 → 0.944` (headroom `10.6 %` →
`5.6 %`) while the `u_M` margin went `26.0 % → 20.9 %`. **Both are closing.** Anyone
quoting one should quote the other.

---

## §5. THE OBSTRUCTION — WHY THE PROOF THE TICKET ASKED FOR IS NOT WHERE IT WAS LOOKED FOR

The ticket asks for a proof, uniform in `n`, that both routes cannot fail together. §4 says
what would deliver one. This section says what will **not**, and it is a theorem.

**THE CONSTRAINT LIST.** Every entry is machine-verified at **90655 of 90655** primitive
posets `n ≤ 7` (`s1` S1.2). An entry that had failed there would have come *out* of the
list; that is what makes the conclusion a theorem rather than a wish.

| | | source |
|---|---|---|
| **(I1)** | `0 < γ ≤ μ_pref` | the cone sits inside `1^⊥` (`mg-51f4` §2) |
| **(I2)** | `μ_pref ≤ 2Φ*_pref` | centred prefix indicators are monotone; `n/max(k,n−k) ≤ 2` (`mg-76b2` Lemma 2.1) |
| **(I3)** | `Φ*_pref ≤ M ≤ Δ_P ≤ 1` | mediant; and `leak(A_k) ≤ m_k Δ_P` |
| **(I4)** | `φ_k ≤ Δ_P` for every `k` | same |
| **(I5)** | `γ ≤ 2Φ*_pref` | (I1)+(I2) |

Both routes fail `⟺ M² > 2γ` **and** `μ_pref(2Δ_P − μ_pref) > 2γ`.

> **THEOREM (obstruction, uniform in `n`).** *The point*
> $$\Delta_P=1,\quad \Phi^{*}_{\mathrm{pref}}=0.30,\quad \mu_{\mathrm{pref}}=0.60,\quad M=0.70,\quad \gamma=0.20$$
> *satisfies **every** one of (I1)–(I5) and has `c♯ = 2.100` and `f* = 1.225` — **both over
> 1**. Hence the disjunction `max_P min(c♯,f*) < 1` is **not** a consequence of (I1)–(I5).
> Any proof of it must use information about `P` beyond the five scalars
> `(γ, Δ_P, Φ*_pref, M, μ_pref)` and the profile.*

**And it is realisable as a profile at every `n`,** so this is not an artefact of one `n`:
the list constrains `(φ_k)` only through its minimum, its `m`-weighted mean and its
ceiling, and a profile with minimum `0.30`, mean `0.70` and maximum `≤ 1` exists for every
`n ≥ 4`.

**Three strengthenings, none of which closes it** (`s2` S2.3):

| add | result |
|---|---|
| `c_true ≤ 1`, i.e. `γ ≥ Φ*²/2` — **`C₃^(III) = 1` ITSELF** | **still feasible** |
| the (false, hypothetical) sharpening `μ_pref ≤ Φ*_pref` | **still feasible** |
| a bounded-spread hypothesis `Λ_F = M/Φ*_pref ≤ 3` | **still feasible** |

> **The target does not imply the disjunction.** `C₃^(III) = 1` plus every scalar
> inequality in the corpus is consistent with both routes failing at the same poset. The
> disjunction is a strictly finer statement than the thing it is being used to certify, and
> **that is why it has survived: it is not the same fact wearing a different hat.**

The reason is structural and worth naming. Every inequality in the list pushes the same
way: they all *upper*-bound `μ_pref` and `M` and *lower*-bound nothing but `γ ≤ μ_pref`.
The disjunction needs an inequality that couples `μ_pref` **downward** to `M` **upward** —
an anti-correlation — and the corpus contains none. `(L*)` is exactly such an inequality,
and it is why §4 is the successor's target and this section is not.

---

## §6. A NEW CORPUS FIGURE, PICKED UP IN PASSING — THE L2 CENSUS AT `n = 7`

`ρ = 1` is exactly L2's first disjunct (a dominant standard eigenvector is monotone along
`e`). Counting it exhaustively:

| `n` | primitive | `ρ = 1` (L2's first disjunct holds) | **L2's first disjunct FAILS** |
|---|---|---|---|
| 3 | 4 | 4 (100 %) | **0** |
| 4 | 27 | 17 (63.0 %) | **10** |
| 5 | 275 | 109 (39.6 %) | **166** |
| 6 | 4070 | 906 (22.3 %) | **3164** |
| **7** | **86278** | **10806 (12.5 %)** | **75472 — NEW** |

The failure column `0, 10, 166, 3164` reproduces `mg-28ff` §2's V00 counts **exactly**, and
sums to its own census figure **3340**. **The `n = 7` row has not been computed before.**
*(`ρ = 1` is decided here numerically at `10⁻⁹` and is a **MEASUREMENT**, not an exact
certificate; `ρ > 1` is exactly certifiable and `ρ = 1` is not, because it asks whether an
algebraic minimiser lies in a cone.)*

---

## §7. PREDICTIONS SCORED

`PREDICTIONS.md` was committed at `8587726`, before one line of `libc50b.py` existed.

| | bet | outcome |
|---|---|---|
| **P1** (0.93) | `[DERIVED PRE-RUN]` the reduction of §2 | **HELD.** 0 disagreements at 90655 primitive posets, and it is §2. |
| **P2** (0.80) | **PRINCIPAL LIVE BET** — the scalar relaxation is FEASIBLE, so no proof lives in the route invariants | **HELD**, §5 — and more strongly than I bet: it survives adding `C₃^(III) = 1` itself. The guard (exhibit the point, list the inequalities one by one) is met. |
| **P3** (0.85) | `[FORMALITY]` `96428 / 86278 / 168 / 4 / 0` re-derive exactly | **HELD**, §1, every one. |
| **P4** (0.60) | if any disagreed it would be `(M♯)`'s 4 | **VOID** — nothing disagreed. Scored as not run, not as held. |
| **P5** (0.45) | height separates the two failure sets: `(F)` at height ≤ 3, `(M♯)` at ≥ 4 | **LOST.** `(F)` fails at heights `{2:44, 3:124}` and `(M♯)` at `{3:2, 4:2}` — **they overlap at height 3**, and at `n = 8` the `(F)` set reaches height 5. Height is not the hidden variable. |
| **P6** (0.35) | `μ_pref = γ` at every height-2 poset | **LOST**, and it was refutable from `mg-28ff`'s own census before I ran anything: `ρ = 1` at 906 of 4070 at `n = 6` while there are 1324 height-2 posets. Measured: `100 / 63.6 / 34.0 / 16.8 / 8.5 %` at `n = 3..7`. |
| **P7** (0.75) | outcome (b) does not land — no both-failing poset | **HELD.** 0 at `n ≤ 8` exhaustively, 0 on every family tested. |
| **P8** (0.55) | `c_or(8) > c_or(7)`, on a defensible population | **HELD**, and the population is exhaustive: `0.943649 > 0.894472`. |
| **P9** (0.30) | the entrywise certificate `min_{k,ℓ} Q_{kℓ}/N_{kℓ}` closes the `μ_pref` sandwich at ≥ 50 % of primitive posets `n ≤ 6` | **LOST, badly, and the direction is the finding**: it closes at `14.8 % / 2.5 % / 0.2 %` at `n = 4/5/6` — **worsening with `n`**, mean relative gap rising to `0.90`. That shortcut to cheap exact `μ_pref` at large `n` is dead, and I would have wasted a ticket on it. |
| **P10** (0.55) | the `c_or` argmax is a third population, neither route near its own extreme | **LOST.** The `c_or(8)` argmax has `f* = 1.269610` — `(F)` has *failed* there, close to its own `n = 7` maximum of `1.297`. |
| **P11** (0.90) | `[FORMALITY]` `5230 / 4377`, `1/4/27/275/4070`, `c_true(6)`, `c♯(6)` | **HELD**, all. |
| **P12** (0.70) | the `f*(6)` sixth figure resolves in `mg-51f4`'s favour | **HELD**: `0.811649`. |

**My principal live bet held; four of the twelve lost, and the one I would most have liked
to lose — P7 — held.** P9's loss is worth more than several of the holds.

---

## §8. TWO DEFECTS OF MY OWN, BOTH CAUGHT BY ARMS FILED IN ADVANCE, BOTH KEPT

1. **`u_M = +∞` where it should have been `0`.** `s2`'s first run reported the reduction
   disagreeing with the direct verdict at `4, 20, 105, 740` posets. The reduction was
   right; **my check was wrong** — I coded the case `Δ_P² ≤ 2γ`, in which `(M♯)` *cannot*
   fail, as `u_M = +∞`, i.e. as *always failing*. The control caught my own instrument, not
   the object under test, which is what a control is for. After the fix: 0 at 90655.
2. **A screened population printed as an enumerated one** — `PREDICTIONS.md` E9, committed
   by me. §3's box. `s5_n8_scope.py` exists only because of it.

**And one arm that could not have fired, rebuilt.** `s0`'s C1 asserts that the *mutated*
floor `c♯ ≥ Δ_P + γ/2` is violated; it fires at 4070 of 4070, so it discriminates. C3
asserts the one-case `(M♯)` differs from the theorem's two-case form somewhere, and fires
at **exactly 5 posets `n ≤ 6`** — independently landing on `mg-29fe`'s finding that those
5 are the **antichains**, one per `n`.

---

## §9. NOT DONE

* **`(L*)` is not proved.** It is certified exactly on two enumerated populations and one
  family. A proof of it would be this lineage's first uniform-in-`n` statement about the
  disjunction, and it is the successor this ticket should file.
* **`(M♯)`'s failure count at `n = 8` is not computed** and is not claimed (§3's box). Nor
  is `max c♯(8)`, `max f*(8)` or `c_true(8)` — the screen does not deliver them.
* **Nothing reaches `n ≥ 99`.** Exhaustive to `n = 8`; two families to `n = 16` and `n = 18`.
  **No family number is a maximum over its `n`.**
* **`c_or` is not extrapolated**, at `n = 8` or anywhere. Its sixth point is measured.
* **L2 is untouched** — not proved, not refuted, not attacked. §6 counts its first
  disjunct; it does not adjudicate it.
* **Neither route is attacked.** No better monotone test vector was sought except as an
  *upper* bound certifying `(M♯)` HOLDS, which is `PREDICTIONS.md` E5's guard.
* **The sweep's loss is out of scope** and appears once, as a reproduction of
  `Λ_M(7) = 110.967`.
* **`ε₀`, `17/78`, `STATE.md`, `roadmap.md` are untouched**, and no other document is
  edited. §1's γ-bin difference and §4.1's refinement of `mg-51f4` §7 are **reported, not
  landed**; they are `mg-51f4`'s to adjudicate.

---

*`mg-c50b`. Instrument: `code/anticorrelation_c50b/` — `libc50b.py` written from the
corpus's definitions with `lib51f4.py` unopened until the census was committed, every
verdict decided on **integer** matrices, and floats confined to the search for candidate
monotone vectors. `s0_selftest.py` **17/17 forced arms**, including two independent PSD
devices, `mg-51f4`'s both `n = 7` witnesses to every printed digit, and five negative
controls.*
