# OneThird — Pinning the operative `λ_std` form, by backward derivation from L4

**Work item.** `mg-88bd` (repo `onethird_program`).
**Method.** Paper-and-pencil. **Zero computation** — no scripts, no data, no enumeration.
Every numerical statement below is either a hand identity, a quoted line from a source, or an
explicitly-labelled read-off from an already-merged empirical table.
**Predecessor.** `mg-1fdb` (the lookup that established the question was malformed) and
`mg-a58f` / `mg-d112` (which flagged the scoping question and correctly declined to settle it).

---

> ## ⚠ SUPERSEDED INPUT — every numeric budget below is 100× too pessimistic (mg-e35c F5, landed mg-5827)
>
> **This document's calibration input is superseded.** The audit of this document
> ([`OneThird-lambda-std-Operative-Form-IndependentAudit.md`](OneThird-lambda-std-Operative-Form-IndependentAudit.md),
> §F5) found §6.4's "L4 usable" row **BROKEN as labelled**: it is calibrated under the branch-(iii)
> reading that §3.4 *of this same document* proves cannot close Step 6, and it reads `F(ε) < 1/6` —
> a **necessary** condition at the *maximum* possible slack — as if it were a calibration point.
> Under this document's own recommended (iii)-repair the correct calibration is the `ε` at which
> mg-3ce3's `survives` predicate first fails, and the probe reports **0 RED events across all 6681
> posets up to `ε = 0.20`**.
>
> | quantity | as written below | **repaired (mg-e35c F5)** | direction of the error |
> |---|---|---|---|
> | `ε_leak` | `≈ 0.02` | **`≈ 0.20`** | — |
> | `ε_spec` budget | `≲ 2×10⁻⁴` | **`≲ 2×10⁻²`** | 100× too small |
> | remaining gap factor (§6.3) | `≈ 5×10³` | **`≈ 50`** | **100× too pessimistic** |
> | master-bound RHS (§6.4) | `≈ 3.3×10⁻⁵ n²/C₃` | **`≈ 3.3×10⁻³ n²/C₃`** | 100× too small |
> | Claim 7.2 threshold (§7.3) | `n ≤ 100` | **`n ≤ 10`** (primitive: `n ≤ 100`) | — |
> | (LIB)/(LIB-const) crossover (§7.4) | `n ≈ 10⁵` | **`n ≈ 900`** | — |
> | antichain-exclusion margin (§7.2) | factor `25` | **factor `2.5`** | 25× too generous |
>
> **THE ERROR DIRECTION INFLATES PESSIMISM.** Every headline number in §§6.4–7.4 and §10 that
> reads as bad news reads *worse* than the repaired calibration supports. The one exception is
> the antichain-exclusion margin at §7.2, which moves the other way (`25` → `2.5`) and is the only
> repaired figure that makes this document's case *weaker*; §7.2's verdict survives it, since
> `1/2 > 0.20` still.
>
> **What does NOT move.** No mathematical statement changes. The *form* — `1 − λ_std ≤ ε_spec`, an
> absolute constant uniform in `n` — is untouched; so are Lemma 2.1, the Cheeger direction, Claim
> 6.1, the master-bound cross-check and every `[PROVEN]` label on a non-numeric claim. §7.3's
> *verdict* also survives, via the constant-free argument (the mg-210d route's unconditional output
> is `ε_spec < 1`, useless at any budget) — F5 breaks the *reasoning* of §7, not its conclusion.
>
> **The constant is still not pinned.** `2×10⁻²` is not a replacement certainty: the honest
> statement, and the one the audit directed be landed, is that **the constant is unpinned by ~2
> orders of magnitude and the pessimistic reading is the smaller one**. Sites below are annotated
> in place rather than rewritten, so the derivation as filed stays readable.
>
> *Superseded values are left in the text and marked; nothing is silently replaced.*

---

## 0. Verdict

> **The operative form is a fourth form, not one of the three in the corpus.**
>
> The architecture requires
> $$1-\lambda_{\mathrm{std}}(P)\;\le\;\varepsilon_{\mathrm{spec}}$$
> for an **absolute constant** $\varepsilon_{\mathrm{spec}}>0$, **uniformly in $n$** — i.e. an
> explicit constant threshold holding at *every* $n$, not an asymptotic statement.
>
> It is **not** the limit ($\lambda_{\mathrm{std}}\to1$), **not** the rate
> ($1-\lambda_{\mathrm{std}}\le C/(\gamma n)$), and it is **not quite** the source's own
> "sufficiently small $\varepsilon$" either — because the source leaves the quantifier over $n$
> unstated, and the uniformity is the whole content.
>
> As an asymptotic class it is **strictly weaker than both** debated forms:
> $$\text{rate}\;\Longrightarrow\;\text{limit}\;\Longrightarrow\;\text{constant-threshold (for }n\ge N_0)$$
> but neither asymptotic form supplies the uniformity, so neither *implies* it outright.
>
> **In inversion terms** (via the mg-210d master bound) the requirement is
> $$\mathbb E[\mathrm{inv}_e]\;\le\;\tfrac{\varepsilon_{\mathrm{spec}}}{6}\,(n^2-1),
> \qquad\text{equivalently}\qquad
> \mathbb E[\text{footrule}]\;\le\;\varepsilon_{\mathrm{spec}}\cdot\mathbb E_{\text{unif}}[\text{footrule}],$$
> i.e. **a constant-factor improvement on the uniform-random-permutation value** — weaker than
> (LIB-weak) $o(n^2)$, which is weaker than (LIB) $O(n)$.
>
> **But — and this is the load-bearing caveat, see §7 — the weakening is not good news.** The
> constant is small (budget: $\varepsilon_{\mathrm{spec}}\lesssim2\times10^{-4}$ **— SUPERSEDED,
> read $\lesssim2\times10^{-2}$; mg-e35c F5, see the banner above**), which makes the
> "weaker" requirement **numerically stronger than LIB at every $n$ below roughly $10^5$**
> **[SUPERSEDED — below roughly $900$]**; and the
> only conversion tool we hold (mg-210d's master bound) is sharp at the antichain, so it cannot
> deliver a small constant for *any* non-chain poset on $\lesssim100$ elements
> **[SUPERSEDED — $\lesssim10$ elements; $\lesssim100$ for the primitive class, which is the
> relevant one]**. The relaxation is
> real, it is correctly derived, and it buys the mg-210d route **nothing** — a conclusion that
> **survives the repair**, because the mg-210d route's unconditional output is
> $\varepsilon_{\mathrm{spec}}<1$ and is therefore constant-free (mg-e35c F9).

---

## 1. Sources, and the notation collision that has been hiding the answer

Canonical source (**not in either repo**):
`/Users/daniel/Library/Mobile Documents/com~apple~CloudDocs/spectral_near_ordinal_sum_program.tex`
(603 lines). Line references below are to that file unless marked otherwise.

**The symbol $\varepsilon$ carries two different meanings in the source, three lines apart in the
architecture, and the whole "limit vs rate" confusion lives in the gap.**

| symbol | where | meaning |
|---|---|---|
| $\varepsilon$ | Step 2, `:494–497` | **spectral**: $\lambda_{\mathrm{std}}(P)\ge1-\varepsilon$ |
| $\varepsilon$ | Step 4, `:502–507` | **spectral** (same one): $\Phi_P(A_k)\lesssim\sqrt\varepsilon$ |
| $\varepsilon$ | §12 `:459`, L4 `:466` | **leakage**: $\Delta_1(A_k,A_k^c)=\varepsilon$ |

Below I write $\varepsilon_{\mathrm{spec}}$ for the first and $\varepsilon_{\mathrm{leak}}$ for the
second. They are related by Cheeger and differ by a **square** (§4). Every prose statement of the
form "$\varepsilon$ sufficiently small" in the source is ambiguous between them until this is fixed.

**Cross-repo note.** The L1–L4 of this file (`:556–570`) are the spectral programme's open lemmas.
They are **not** the `(L1)–(L4)` band invariants of `one_third_width_three/step8.tex:2022 ff.`,
which are a different object; nothing below refers to those.

---

## 2. The first thing to fix: the $\Phi\to\Delta_1$ conversion is the identity, not a bound

The ticket located the possible $n$-dependence in the "$\varepsilon\to\Delta_1$ conversion".
There is no conversion. There is an identity.

**Lemma 2.1 (no conversion loss).** *For $A\subseteq[n]$ with $0<|A|\le n/2$ and $B=[n]\setminus A$,*
$$\Phi_P(A)\;=\;\Delta_1(A,B).$$

*Proof.* $\Phi_P(A)=\mathbb E_\sigma|A\setminus\sigma(A)|\,/\,|A|$ (Def., `:229–237`) and
$\Delta_1(A,B)=\mathbb E_\sigma|A\setminus\sigma(A)|\,/\,\min(|A|,|B|)$ (Def., `:270–278`).
For $|A|\le n/2$ we have $|B|=n-|A|\ge|A|$, so $\min(|A|,|B|)=|A|$. The two numerators are the same
expression and the two denominators agree. $\square$ **[PROVEN]**

**Corollary 2.2.** With $A=A_k=\{1,\dots,k\}$ and $K_k=|A_k\setminus\sigma(A_k)|$ (`:239–250`),
Step 5's displayed condition $\mathbb E K_k\ll\min(k,n-k)$ (`:509–512`) is *literally* the statement
$\Delta_1(A_k,A_k^c)\ll1$, which is *literally* $\Phi_P(A_k)\ll1$ for $k\le n/2$.
**Steps 4 and 5 state the same inequality about the same number.** **[PROVEN]**

This is worth stating plainly because it eliminates the most natural place an $n$ could have been
hiding. $\Delta_1$ is already a **per-element density** — that is exactly what the
$\min(|A|,|B|)$ normalisation is for. Step 5 is not a further reduction of Step 4; it is a
re-reading of it in poset language.

---

## 3. Backward step 1 — what $\Delta_1\le\varepsilon$ must mean for L4 to fire

### 3.1 L4, quoted in full (`:464–474`)

> **Conjecture (Near-ordinal-sum stability).**
> There exists $F(\varepsilon)\to0$ such that if $\Delta_1(A,B)\le\varepsilon$, then one of the
> following holds:
> (i) $P$ contains a $1/3$-balanced pair;
> (ii) after removing or modifying at most $F(\varepsilon)n$ interface elements, $P$ becomes
> $P[A]\oplus P[B]$;
> (iii) a balanced pair in $P[A]$ or $P[B]$ remains balanced up to error $F(\varepsilon)$ in $P$.

### 3.2 The quantifier is the answer

**Claim 3.1 (the modulus is $n$-free).** *L4's $F$ is a function of $\varepsilon$ alone. Therefore
$\varepsilon$ must be an absolute constant below a threshold; requiring $\varepsilon\to0$ with $n$
is permitted but buys nothing, and requiring $F$ to depend on $n$ makes the statement unstatable.*
**[PROVEN — as a reading of the stated form; the reading is argued, not assumed]**

Three independent supports, none of which requires interpreting prose charitably:

1. **$n$ appears exactly once in L4, and it appears multiplied by $F$, not inside it.** Branch (ii)
   reads $F(\varepsilon)\,n$. If $F$ were $F_n$, then "$F(\varepsilon)\to0$" would have no
   referent (as $\varepsilon\to0$ for each fixed $n$? uniformly in $n$? the two differ) and branch
   (ii) would be a schema, not a statement. The only reading under which L4 is a single
   universally-quantified sentence over all $(P,n,A,B)$ is: $F:(0,\varepsilon_0)\to\mathbb R_{\ge0}$
   with $\lim_{\varepsilon\to0}F(\varepsilon)=0$, applied uniformly.

2. **Nothing downstream of L4 contains an $n$.** L4's consumer is Step 6 (`:514–515`): transfer a
   balanced pair to $P$, contradicting minimality. The predicate being contradicted is
   $\delta(P)<1/3$ — a max over pairs of a probability, compared against the absolute constant
   $1/3$. The window $[1/3,2/3]$ has width $1/3$ at every $n$. **The entire downstream of Step 5 is
   dimensionless.** An error term is useful iff it is small compared to that window, and "small
   compared to $1/3$" is an $n$-free condition.

3. **The programme's own executable artifact already committed to this reading.** The mg-3ce3 probe
   (`one_third_width_three/docs/OneThird-L4-NearOrdinalSum-Stability-Probe.md`) computes a *single*
   envelope $F(\varepsilon)$ pooled across $n=5\ldots16$ at **absolute** thresholds
   $\varepsilon\in\{0.02,0.05,0.10,0.15,0.20\}$ (`:136–144`). An $n$-dependent modulus would make
   that table meaningless. This is usage evidence for the reading, not proof of it. **[HEURISTIC]**

**Consequence.** The answer to the ticket's question (1) is: **L4 needs $\varepsilon$ to be an
absolute constant below a threshold. It does not need $\varepsilon$ to shrink with $n$.**

### 3.3 The steelman for $n$-dependence, and why it fails

The only route by which L4 could demand $\varepsilon\to0$ with $n$ is if a proof went through
branch **(ii)** *and* needed the modified set to be $O(1)$ rather than a constant fraction — i.e.
$F(\varepsilon)n=O(1)$, hence $\varepsilon\le F^{-1}(c/n)$.

Two reasons this is not the architecture's requirement:

- **The source never uses (ii).** Step 6 (`:514–515`) says "use near-ordinal-sum stability to
  *transfer a balanced pair* from $P[A_k]$ or $P[A_k^c]$ to $P$". That is branch (iii) (with (i) as
  the trivial closure). Branch (ii) is a structural alternative that no stated step consumes.
- **It would demand far more than either debated form.** Taking the mg-3ce3 fitted modulus
  $F(\varepsilon)\approx0.32\,\varepsilon^{0.55}$ (`:149`) as an order-of-magnitude stand-in,
  $F(\varepsilon)n=O(1)$ gives $\varepsilon=\Theta(n^{-1.82})$, hence (by §4)
  $\varepsilon_{\mathrm{spec}}=\Theta(n^{-3.64})$ and (by §6)
  $\mathbb E[\mathrm{inv}_e]=O(n^{-1.64})=o(1)$ — a *vanishing* expected inversion count, stronger
  than LIB, LIB-weak and everything else on the table. If a future proof routes through (ii) in this
  form, it is not a refinement of the present question; it is a different programme.
  **[HEURISTIC — rests on the fitted modulus, which is empirical]**

### 3.4 A separate defect found on the way: branch (iii) does not close Step 6

This is not an $n$-dependence issue and it does not change the verdict, but it is load-bearing for
anyone who writes L4 down as a lemma, so it is recorded here rather than discovered again.

**Claim 3.2 (endpoint gap).** *Branch (iii) as literally stated cannot produce the Step 6
contradiction, for any $F(\varepsilon)>0$, under either natural reading of "remains balanced up to
error $F(\varepsilon)$".* **[PROVEN]**

*Proof.* Minimality gives $\delta(P[A])\ge1/3$, i.e. a pair $\{x,y\}\subseteq A$ with
$p^{P[A]}_{xy}\in[1/3,2/3]$. Branch (iii) yields either
$p^P_{xy}\in[\tfrac13-F,\tfrac23+F]$ (reading: "balanced, up to error $F$") or
$|p^P_{xy}-p^{P[A]}_{xy}|\le F$ (reading: "drifts by at most $F$"), and the second implies the
first. But $\delta(P)<1/3$ says only $p^P_{xy}\notin[1/3,2/3]$, which is *consistent* with
$p^P_{xy}\in[\tfrac13-F,\tfrac13)\cup(\tfrac23,\tfrac23+F]$. No contradiction. $\square$

**Claim 3.3 (the gap cannot be repaired by demanding interior slack from minimality).** *There is a
poset attaining $\delta=1/3$ exactly, so minimality cannot be strengthened to
"$\exists$ pair with $p\in[\tfrac13+c,\tfrac23-c]$".* **[PROVEN, by hand]**

*Proof.* Take $P_0=\{a<b\}\sqcup\{c\}$ on three elements. $\mathcal L(P_0)=\{abc,\,acb,\,cab\}$,
so $|\mathcal L(P_0)|=3$. Then $p_{ac}=\Pr[a\prec c]=2/3$ (realised by $abc,acb$) and
$p_{bc}=\Pr[b\prec c]=1/3$ (realised by $abc$). Both incomparable pairs sit exactly on the boundary,
so $\delta(P_0)=1/3$ with zero slack. $\square$

**Note that $n$-dependence does not repair this either**: for any $\varepsilon>0$, however it scales
with $n$, $F(\varepsilon)>0$ at each finite $n$, and the slack can be $0$ at that $n$. **The endpoint
gap is orthogonal to the limit-vs-rate question, and settling the latter neither creates nor cures
it.**

**Recommended repair (proposal, not an edit).** Restate (iii) as *exact* preservation — "a balanced
pair in $P[A]$ or $P[B]$ remains in $[1/3,2/3]$ in $P$" — leaving $F(\varepsilon)$ to appear only in
(ii). This is not a strengthening invented here: it is **precisely the predicate mg-3ce3 tested**
(`:86–88`: "*that pair survives in the full poset: $p^P_{xy}\in[\tfrac13,\tfrac23]$*"; the
`survives` field is "*does at least one balanced-in-side pair stay in $[\tfrac13,\tfrac23]$ in
$P$*"), and it is the form that returned **0 RED events over 6681 posets**. The probe has been
supplying evidence for the repaired form, not the stated one. **[PROVEN that the probe tests the
repaired form; the probe's green is HEURISTIC evidence for it]**

---

## 4. Backward step 2 — what "$\ll$" in Step 5 must mean, and what Step 4 then fixes

### 4.1 Step 5

By Corollary 2.2, Step 5's $\mathbb E K_k\ll\min(k,n-k)$ *is* $\Delta_1\le\varepsilon_{\mathrm{leak}}$.
By Claim 3.1, $\varepsilon_{\mathrm{leak}}$ must be an absolute constant. Hence:

> **"$\ll$" is to be read as "$\le\varepsilon_0\cdot\min(k,n-k)$ for an absolute constant
> $\varepsilon_0>0$" — a small constant fraction. It is *not* $o(\min(k,n-k))$.**

The $o(\cdot)$ reading is consistent with the source and strictly stronger; it simply is not
required by the consumer. **[CONDITIONAL on Claim 3.1]**

### 4.2 Step 4 — the square is a constant loss, not an $n$ loss

Step 4 (`:502–507`) reads $\Phi_P(A_k)\lesssim\sqrt\varepsilon$. Its warrant is the lower half of the
Cheeger sandwich (`:318–324`):
$$\frac{(\Phi_P^\ast)^2}{2}\;\le\;1-\lambda_{\mathrm{std}}(P)\;\le\;2\Phi_P^\ast.$$
From $1-\lambda_{\mathrm{std}}\le\varepsilon_{\mathrm{spec}}$ we get
$\Phi_P^\ast\le\sqrt{2\varepsilon_{\mathrm{spec}}}$, so requiring
$\Phi_P(A_k)\le\varepsilon_{\mathrm{leak}}$ is met as soon as
$$\boxed{\;\varepsilon_{\mathrm{spec}}\;\le\;\tfrac12\,\varepsilon_{\mathrm{leak}}^{\,2}\;}$$
— **a squaring of a constant, which is a constant.** No $n$ enters. **[PROVEN, given the sandwich]**

(Consistency check, by hand: the antichain has $T_P=\tfrac1nJ$, hence $S_P|_H=0$ and
$1-\lambda_{\mathrm{std}}=1$; and for $|A|=k\le n/2$,
$\mathbb E|A\setminus\sigma(A)|=\sum_{x\in A}\Pr[\mathrm{pos}(x)>k]=k(n-k)/n$, so
$\Phi_P(A)=\Delta_1=(n-k)/n\ge1/2$, minimised at $k=n/2$. The right-hand sandwich
$1\le2\cdot\tfrac12$ is an **equality** at the antichain. **[PROVEN]** This same computation is
reused as the non-vacuity check in §7.2.)

### 4.3 The one place an $n$ could still enter — and the source closes it

Cheeger sweeping produces a low-conductance *threshold set*; Step 3 / L2 / L3 must convert that to a
low-conductance **prefix**. L3 (`:564–566`) says only "with quantitatively controlled loss" —
unquantified. **If that loss were a factor of $n$, everything above changes**: we would need
$\varepsilon_{\mathrm{spec}}\le\varepsilon_{\mathrm{leak}}^2/(2n)$, and the whole question would
reopen with an $n$-dependent answer.

The source pins it. The **Prefix-capture** conjecture (`:360–364`) states the threshold cut's
Rayleigh quotient "captures a **constant fraction**, or possibly $1-o(1)$, of the dominant standard
eigenvalue." So the intended loss is a constant factor. **[quoted; the conjecture itself is OPEN]**

Two honest riders on that quotation:

- **As literally worded, prefix capture is too weak to use.** "Captures a constant fraction $c<1$ of
  $\lambda_{\mathrm{std}}$" gives a prefix Rayleigh quotient $\rho\ge c\lambda_{\mathrm{std}}\approx c$,
  hence $1-\rho\approx1-c$ — a *constant floor*, not a small gap. The chain needs constant-factor
  capture of the **gap**: $1-\rho_{\text{prefix}}\le C_3\,(1-\lambda_{\mathrm{std}})$. The
  alternative wording in the same sentence ($1-o(1)$) is the gap-form in disguise.
  **[PROVEN — arithmetic on the stated form]**
- Under **either** repair the loss is a constant $C_3$, giving
  $\varepsilon_{\mathrm{spec}}\le\varepsilon_{\mathrm{leak}}^2/(2C_3)$. Under the **literal** reading
  the chain does not merely acquire an $n$ — it breaks outright, at a constant floor.
  **So there is no reading of the source under which $n$ enters at L3.** **[CONDITIONAL on the
  quoted sentence being the intended one]**

**This is the last candidate site.** Walking the chain L4 → Step 5 → Step 4 → Step 3 → Step 2, every
conversion is either an identity (Lemma 2.1), a squaring of a constant (§4.2), or an unquantified
constant factor that the source explicitly calls a constant fraction (§4.3). **Nowhere does an $n$
enter.**

---

## 5. Backward step 3 — the operative form of the $\lambda_{\mathrm{std}}$ requirement

### 5.1 The form

Step 2 (`:492–497`) states exactly:
$$\lambda_{\mathrm{std}}(P)\ge1-\varepsilon\quad\text{"with sufficiently small }\varepsilon\text{"}.$$
Sections 3–4 show this reading is not merely permitted — it is **forced by L4**. The corpus's third
form is the operative one.

**But it is not one of the three as any of them is currently written**, because all three leave the
quantifier over $n$ unstated, and that quantifier is the content:

| corpus form | where | status against the derivation |
|---|---|---|
| **limit** $\lambda_{\mathrm{std}}\to1$ | `STATE.md:13`, `:86` row 8 | **stronger than needed**, and asymptotic: gives the threshold only for $n\ge N_0$, with ~~$N_0$ *unspecified*~~ **no $N_0$ that works for the class at all — rider below** |
| **rate** $1-\lambda_{\mathrm{std}}\le C/(\gamma n)$ | mg-7ae7 | **much stronger than needed**; also asymptotic, but with an *explicit* threshold $n\ge C/(\gamma\varepsilon_{\mathrm{spec}})$ |
| **fixed constant** $\lambda_{\mathrm{std}}\ge1-\varepsilon$ | tex Step 2 `:494–497`, L1 `:557–558` | **right shape, quantifier missing** |
| **operative (this document)** | — | $1-\lambda_{\mathrm{std}}\le\varepsilon_{\mathrm{spec}}$, $\varepsilon_{\mathrm{spec}}$ an **explicit absolute constant**, at **every** $n$ (equivalently: with an explicit finite exceptional set) |

The ordering as *asymptotic statements* is rate $\Rightarrow$ limit $\Rightarrow$ constant-threshold
(for large $n$). The ordering as *usable hypotheses* is not a chain: neither asymptotic form delivers
uniformity, and the constant form demands it. The rate form's one genuine practical advantage over
the limit form is that its exceptional set is **explicit**. **[PROVEN]**

**[THRESHOLD READING SUPERSEDED — mg-4417, on mg-c4f5 §5.3 (landed `STATE.md` by mg-5ce3).**
*Unspecified* understates the limit row above, and it understates it in the direction that invites
work. The threshold is not merely unknown-but-there: **no $N_0$ works for the class at all**, so
*go and find $N_0$* is a **closed** question rather than an open one. The argument is
[`OneThird-LIBweak-mg-c4f5-IndependentAudit.md`](OneThird-LIBweak-mg-c4f5-IndependentAudit.md) §5.3
and it is **pointed at here, not restated**.

**THE TRANSFER IS THE PART TO READ, because §5.3 is not about this row's hypothesis.** §5.3 proves
its statement for **(LIB-weak) $\Rightarrow$ (LIB-const)** — the *inversion*-side hypothesis
$\mathbb E[\mathrm{inv}_e]=o(n^2)$. This row's hypothesis is the **limit** $\lambda_{\mathrm{std}}\to1$.
Those are different implications and §5.3 must not be quoted as though it ruled on this one
directly. It reaches this row **a fortiori**, in one step, and the step is this document's own
Claim 21: the master bound $1-\lambda_{\mathrm{std}}\le6\mathbb E[\mathrm{inv}_e]/(n^2-1)$ makes
every $o(n^2)$ family a $\lambda_{\mathrm{std}}\to1$ family, so the class §5.3 exhibits its
counterexample in is a **subclass** of this row's, and a counterexample in a subclass is a
counterexample in the class. **Kind, marked at the step:** that route runs through Claim 21, which
this ledger labels **CONDITIONAL** (cited from mg-210d), so the a-fortiori transfer inherits that
label and nothing stronger. **The conclusion does not depend on it.** For the limit form alone it
needs no construction and no master bound at all — $\lambda_{\mathrm{std}}\to1$ is *by definition*
a per-family $\exists N$, carrying no uniformity over the class, so the per-class threshold fails
outright. §5.3 is cited because it is the corpus's **landed** statement, not because this row
requires its machinery.

**THE PRECISION THAT MUST TRAVEL:** what is false is the **PER-CLASS** claim — *that there is an
$N_0$ beyond which every family in the class satisfies the constant form*. The **PER-FAMILY**
statement is **TRUE and is left standing**: a single family with $\lambda_{\mathrm{std}}\to1$ does
have a threshold of its own, it is simply not a function of the hypothesis and so cannot be
extracted from it. Anyone needing $N_0$ must first prove something strictly stronger than the
limit — a **rate**, which is the row below, and whose explicit exceptional set is exactly the
advantage §5.1 already credits it with.

**WHAT THIS DOES NOT STRIKE.** Claim 19 and the paragraph above it are **untouched and correct**:
rate $\Rightarrow$ limit $\Rightarrow$ constant-for-large-$n$ holds per family, and *"neither
asymptotic form delivers uniformity"* is precisely what §5.3 sharpens rather than contradicts.
The defect is the single word *unspecified*, and it is the same word struck at
[`OneThird-LIBweak-mg-c3ca.md`](OneThird-LIBweak-mg-c3ca.md) `:100` — **which cites this table for
that sentence** (*"this is not new mathematics — it is mg-88bd's result"*), making this row the
**upstream** of that strike. **]**

### 5.2 Where mg-7ae7's rate came from — it is an artifact of the input, not a demand of the consumer

This matters because the rate has been treated as a target for months.

mg-7ae7's target $1-\lambda_{\mathrm{std}}\le C/(\gamma n)$ was chosen to match the *shape of its
input*: Theorem E (`one_third_width_three/step8.tex:57–73`) delivers
$\Phi(S)\le\eta(\gamma,n):=2/(\gamma n)$. The $1/n$ is what the BK-side averaging argument happens to
produce.

Theorem E's own statement says what its consumer actually needs (`step8.tex:68–72`, verbatim):

> Here $\eta(\gamma,n)\downarrow0$ as $n\to\infty$ for any fixed $\gamma\in(0,1/3]$; **for every
> fixed $\gamma,T$ the bound lies below any prescribed positive threshold once $n\ge n_0(\gamma,T)$**
> (Remark…), which is what the main-theorem cascade of Proposition… requires.

and Remark `rem:n-dependence-g1` (`step8.tex:290–305`) is titled "**$n$-dependence absorbed by the
small-$n$ base case**", substituting $\eta(\gamma,n)(n-1)\le2/\gamma$ to reduce the cascade to "the
$n$-independent arithmetic condition $\gamma^2c_5(T)c_6(\delta-K(T)\varepsilon)\ge2$".

**So on the BK side too, the $1/n$ is produced by the tool and then explicitly discarded by the
consumer.** The rate form is a *property of the proof we happen to have*, not a requirement anything
downstream imposes. Carrying it forward as a target for $\lambda_{\mathrm{std}}$ imported a factor of
$n$ that no consumer asked for. **[PROVEN — direct quotation of both source statements]**

---

## 6. Backward step 4 — converting to the inversion requirement

### 6.1 The master bound, and its calibration

mg-210d's master bound (`STATE.md:130`; re-derived there from scratch, recorded sharp):
$$1-\lambda_{\mathrm{std}}\;\le\;\frac{3\,\mathbb E[\text{footrule}]}{n^2-1}\;\le\;\frac{6\,\mathbb E[\mathrm{inv}]}{n^2-1},
\qquad\text{equality at the antichain.}$$

Two hand checks, both independent of mg-210d's derivation:

- **The second inequality** is Diaconis–Graham's upper half $D\le2I$. **[PROVEN]**
- **The equality claim is confirmed.** For uniform $\sigma\in S_n$,
  $\sum_{i,j}|j-i| = 2\sum_{d=1}^{n-1}d(n-d) = n(n^2-1)/3$, so
  $\mathbb E_{\text{unif}}[\text{footrule}] = (n^2-1)/3$; substituting gives $3\cdot\tfrac{n^2-1}{3}/(n^2-1)=1$,
  which matches $1-\lambda_{\mathrm{std}}=1$ at the antichain (§4.2). **[PROVEN, by hand]**

### 6.2 The requirement

$1-\lambda_{\mathrm{std}}\le\varepsilon_{\mathrm{spec}}$ is *implied by*
$$\boxed{\;\mathbb E[\mathrm{inv}_e]\;\le\;\frac{\varepsilon_{\mathrm{spec}}}{6}\,(n^2-1)\;}
\qquad\text{equivalently}\qquad
\mathbb E[\text{footrule}]\;\le\;\frac{\varepsilon_{\mathrm{spec}}}{3}(n^2-1)
\;=\;\varepsilon_{\mathrm{spec}}\cdot\mathbb E_{\text{unif}}[\text{footrule}].$$

**The cleanest statement of the answer to the ticket's question (4):** the architecture needs a
random linear extension of a minimal counterexample to have expected footrule displacement
**a small constant fraction of the uniform-random-permutation value**. Not $o(\cdot)$ of it, and not
$O(n)$ against its $\Theta(n^2)$.

Call this **(LIB-const)**. As asymptotic classes:
$$\text{(LIB) } O(n)\;\subsetneq\;\text{(LIB-weak) } o(n^2)\;\subsetneq\;\text{(LIB-const) } \le cn^2 .$$
**Neither of the two forms named in the ticket is the answer; the answer is weaker than both.**
**[CONDITIONAL on §§3–5 and on the mg-210d master bound]**

### 6.3 What freezing already gives, for free

**Claim 6.1.** *Under the frozen hypothesis with distinguished order $e$,
$\mathbb E[\mathrm{inv}_e]<m/3$, where $m$ is the number of incomparable pairs.* **[PROVEN]**

*Proof.* $\mathrm{inv}_e(\sigma)$ counts incomparable pairs $i<j$ with $j\prec_\sigma i$
(`STATE.md:41`; `tex:87–90`). By the counterexample orientation, $\Pr[j\prec i]<1/3$ for each such
pair, so $\mathbb E[\mathrm{inv}_e]=\sum_{i<j,\,i\parallel j}\Pr[j\prec_\sigma i]<m/3$. $\square$

Since $\mathbb E_{\text{unif}}[\mathrm{inv}]=\binom n2/2$ and $m\le\binom n2$, Claim 6.1 says
freezing alone delivers $\mathbb E[\mathrm{inv}_e]<\tfrac23\,\mathbb E_{\text{unif}}[\mathrm{inv}]$
— a constant-factor improvement on random, unconditionally, i.e. **(LIB-const) already holds, with
constant $2/3$**. Fed through the master bound (whose inversion form is itself a factor $3/2$ lossy
at the antichain, since $D\le2I$ is not tight there) this yields
$1-\lambda_{\mathrm{std}}<6(m/3)/(n^2-1)=d\cdot n/(n+1)$ with $d=m/\binom n2$ — reproducing
mg-210d's recorded degenerate bound exactly, and confirming the arithmetic against an
already-audited result. **[PROVEN]**

**So the entire remaining gap on this route is a constant factor:** we hold
$\varepsilon_{\mathrm{spec}}<n/(n+1)\to1$ and need
$\varepsilon_{\mathrm{spec}}\approx2\times10^{-2}$ — **a factor of roughly $50$**, with no $n$ in it
anywhere. Nothing asymptotic is at stake.

> **[FIGURE REPAIRED — mg-e35c F5, landed mg-5827.]** This sentence read
> *"need $\varepsilon_{\mathrm{spec}}\approx2\times10^{-4}$ — a factor of roughly $5\times10^{3}$"*
> until 2026-08-07. Both numbers came from §6.4's superseded budget; the repaired calibration puts
> the gap at **$\approx50$, not $\approx5{,}000$**. **The stale figure overstated the remaining gap
> by 100× — it made the wall look a hundred times further away than this route's own arithmetic
> supports.** The qualitative claim ("the entire remaining gap is a constant factor, with no $n$ in
> it") is what §6.3 proves and is **unaffected**; only the size of the constant moves. It is still a
> factor of ~50 and the constant is still unpinned by ~2 orders of magnitude in both directions.

### 6.4 The constant budget, made explicit

| step | relation | source | label |
|---|---|---|---|
| L4 usable | $F(\varepsilon_{\mathrm{leak}})<$ pair's slack; slack $\le1/6$ for a centred pair | §3 | ~~PROVEN (given the repaired (iii))~~ **BROKEN as labelled — mg-e35c F5** |
| read off modulus | ~~$F(0.02)\le0.073<1/6$; $F(0.05)\le0.198>1/6$ $\Rightarrow$ $\varepsilon_{\mathrm{leak}}\approx0.02$~~ **SUPERSEDED $\Rightarrow$ $\varepsilon_{\mathrm{leak}}\approx0.20$** (0 RED / 6681 posets up to $\varepsilon=0.20$) | mg-3ce3 envelope `:136–144` | **HEURISTIC** (empirical envelope) |
| Cheeger | $\varepsilon_{\mathrm{spec}}\le\varepsilon_{\mathrm{leak}}^2/2\approx$ ~~$2\times10^{-4}$~~ **$2\times10^{-2}$** | §4.2 | PROVEN (the *relation*; the *number* moves with the row above) |
| L3 loss | divide by $C_3$ | §4.3 | **UNQUANTIFIED** |
| master bound | $\mathbb E[\mathrm{inv}_e]\le\tfrac{\varepsilon_{\mathrm{spec}}}{6}(n^2-1)\approx$ ~~$3.3\times10^{-5}n^2/C_3$~~ **$3.3\times10^{-3}n^2/C_3$** | §6.2 | CONDITIONAL |

> **[ROW SUPERSEDED — mg-e35c F5, landed mg-5827.]** The "L4 usable" row is **BROKEN as labelled**,
> for three compounding reasons, and it is the numeric spine of §7:
>
> 1. **The label is backwards.** Under the *repaired* (iii) that §3.4 above recommends — "a balanced
>    pair remains in $[1/3,2/3]$" — **$F$ does not appear in the statement at all**, so there is no
>    $F(\varepsilon_{\mathrm{leak}})<\text{slack}$ condition to calibrate.
> 2. **Under the *stated* (iii) the row contradicts §3.4's own Claim.** §3.4 proves the available
>    slack can be **$0$** (the $P_0$ witness), so no $F>0$ satisfies $F<\text{slack}$. The $1/6$ is
>    the slack of a *centred* pair — the **maximum possible** — used as if it were a guarantee.
>    $F(\varepsilon)<1/6$ is a **necessary** condition read as a **calibration point**.
> 3. **The consequence is quantitative and one-directional.** The correct calibration under the
>    recommended repair is the $\varepsilon$ at which mg-3ce3's `survives` predicate first fails, and
>    the probe reports **0 RED across all 6681 posets up to $\varepsilon=0.20$** — supporting
>    $\varepsilon_{\mathrm{leak}}\approx0.20$, hence
>    $\varepsilon_{\mathrm{spec}}\le0.2^2/2=2\times10^{-2}$, **100× larger than the
>    $2\times10^{-4}$ this row was filed with.**
>
> The struck values are kept above so the derivation as filed stays readable.

**So the form is pinned; the constant is not.** Pinning the constant requires quantifying exactly two
things the source leaves open: **L4's modulus $F$** and **L3's prefix-restriction loss $C_3$**.
That is the honest residual under-determination, and it is a *different* under-determination from
the one this ticket opened with. **[AMENDED — mg-e35c F5:** this sentence is right and §7 below then
uses the unpinned constant *as though it were pinned*. The honest statement is that
$\varepsilon_{\mathrm{spec}}$ is **unpinned by ~2 orders of magnitude, and the pessimistic reading is
the smaller one.**]

---

## 7. The strength check — is the weaker requirement still strong enough?

The ticket flags this explicitly, and it must be answered before the weakening is reported as a win.
It has three parts. **Two pass; the third is where the news turns bad.**

### 7.1 Does breadth of the hypothesis class break the contradiction? — **No, and the objection is misdirected**

The worry: if $\Delta_1\le\varepsilon_0$ holds for many non-counterexamples, can it contradict
minimality?

It can, and the reason is structural. The architecture's shape is
$$\text{counterexample}\;\Rightarrow\;\text{thin prefix}\;\Rightarrow_{\text{L4}}\;\text{$P$ has a balanced pair}\;\Rightarrow\;\text{not a counterexample}.$$
The conclusion L4 draws from thinness is "*$P$ has a balanced pair*" — which is **true and
unremarkable for a non-counterexample**. Non-counterexamples in the hypothesis class are therefore
harmless; they do not weaken the contradiction. This is the architecture's specific good fortune and
it does not generalise: an architecture whose thinness-conclusion were false for general posets
would indeed be destroyed by a broad hypothesis class. **[PROVEN — logic]**

**What the breadth does do is relocate the burden onto L4.** Under the constant reading, L4 must hold
for *every* poset with a $\Delta_1\le\varepsilon_0$ prefix, not merely for counterexamples. So:

> **The constant-fraction reading is weaker upstream (easier for Step 2 / L1 to deliver) and
> strictly stronger downstream (L4 must cover a larger class). It is not free.**

And that heavier burden has already been stress-tested: mg-3ce3 searched for exactly the failure
event — thin interface, both sides non-chain, no within-side balanced pair — at absolute thresholds
up to $\varepsilon=0.20$, i.e. ~~an order of magnitude above the
$\varepsilon_{\mathrm{leak}}\approx0.02$ the constant budget needs~~ **[SUPERSEDED — mg-e35c F5,
landed mg-5827: at the repaired calibration $\varepsilon_{\mathrm{leak}}\approx0.20$, so
$\varepsilon=0.20$ is *exactly* the budget and not an order of magnitude above it]**, and found
**0 RED events in 6681 posets** up to $n=16$
(`probe :110–116, :247`). **[HEURISTIC — empirical, and the probe is silent on $n$-stratification
at fixed $\varepsilon$, which is the one cheap check that would directly corroborate $n$-uniformity;
flagged, not run, per the no-computation directive.]**

> **[DIRECTION NOTE — this site fails the OTHER way, and it is the site the whole repair turns on.]**
> As written, this sentence offered the reader a **safety margin that does not exist**: it said the
> stress test ran an order of magnitude beyond what the budget needs. It did not. **This very
> measurement — 0 RED across 6681 posets up to $\varepsilon=0.20$ — *is* what F5 uses to calibrate
> $\varepsilon_{\mathrm{leak}}\approx0.20$ in the first place**, so it cannot simultaneously be
> evidence of headroom above that value. The stale figure here made the empirical position look
> **safer** than it is, while the same stale figure at §6.3 made the *mathematical* position look
> **worse** than it is. One superseded input, two opposite-signed errors — which is why direction
> has to be read per site and cannot be inferred from the input.
>
> **This site was missed by the hand sweep of `c413c9e` and found by the detector in
> `code/superseded_figures_5827/`.** It is the instrument's first live catch and it is recorded as
> such rather than folded silently into the repair.

### 7.2 Is the condition vacuous — does every poset have a thin prefix? — **No**

If $\Delta_1\le\varepsilon_0$ held trivially, Step 4's output would carry no information and Step 6
would be asking L4 to prove the conjecture unaided.

**Claim 7.1.** *Every prefix of the $n$-antichain has $\Delta_1\ge1/2$.* **[PROVEN]** — the
computation is in §4.2. Since $1/2\gg\varepsilon_0\approx0.02$, the condition excludes the
maximum-entropy object by a factor of 25. It is genuinely restrictive.

> **[FIGURE SUPERSEDED — mg-e35c F5, landed mg-5827.]** At the repaired calibration
> $\varepsilon_0\approx0.20$, so the margin is $1/2\,/\,0.20=$ **a factor of $2.5$, not $25$**.
> **This is the one repaired figure that moves against this document** — every other one below is
> 100× too pessimistic; this one was 10× too generous. **The verdict of §7.2 survives**: $1/2>0.20$,
> so the antichain is still excluded and the condition is still not vacuous. What no longer survives
> is the word *"$\gg$"* and the comfort of an order-of-magnitude margin.

### 7.3 Does the weakening actually help the route we hold? — **No. This is the bad news.**

The master bound is our only stated $\lambda_{\mathrm{std}}\leftarrow\mathbb E[\mathrm{inv}]$
conversion, and it is **sharp at the antichain** — the object at the opposite extreme from a frozen
poset. Pushing the constant-form target through it:

$\varepsilon_{\mathrm{spec}}\approx2\times10^{-4}$ **[SUPERSEDED — read $2\times10^{-2}$; the
arithmetic of this subsection is exact, only its input moves. See the box below.]** combined with
Claim 6.1 requires
$d\cdot n/(n+1)\le\varepsilon_{\mathrm{spec}}$, i.e. incomparability density
$d\lesssim2\times10^{-4}$, i.e. $m\lesssim2\times10^{-4}\binom n2$.

**Claim 7.2.** *For $n\le100$ this forces $m=0$ — the poset must be a chain, hence not a
counterexample.* **[PROVEN]** — $2\times10^{-4}\cdot\binom n2\ge1$ requires $n(n-1)\ge10^4$, i.e.
$n\ge101$.

> **[THRESHOLD SUPERSEDED — mg-e35c F5, landed mg-5827.]** At the repaired
> $\varepsilon_{\mathrm{spec}}\approx2\times10^{-2}$ the same arithmetic gives
> $d\lesssim2\times10^{-2}$ and $2\times10^{-2}\cdot\binom n2\ge1$ requires $n(n-1)\ge100$, i.e.
> $n\ge11$ — so **Claim 7.2's threshold is $n\le10$, not $n\le100$.** The arithmetic as printed is
> exact; only its input moves. A **free sharpening the audit adds** (mg-e35c A1) recovers most of
> the ground: minimal counterexamples are **primitive**, primitivity forces $m\ge n-1$ hence
> $d\ge2/n$, so the master bound cannot deliver the target below $n\le2/\varepsilon_{\mathrm{spec}}$
> — **$n\le100$ at the repaired budget** (and $n\le10^4$ at the superseded one). The claim as
> printed was **both 100× too pessimistic in its input and weaker than the available argument**;
> the two errors point in opposite directions and the primitive form lands back near the printed
> number for a different reason.

So the mg-210d master bound **cannot deliver the architecture's target for any non-chain poset on at
most ~100 elements**, and above that demands a near-chain density. mg-210d's recorded verdict
("best constant this route proves $=0$") therefore **survives the relaxation intact**: dropping from
the limit/rate to a constant does not rescue that route, because the master bound's loss is a
constant factor and the target is now a constant.

**Per the ticket's second warning, this is a statement about the tool, not a lower bound on the
problem.** The master bound uses a *single test vector* — the centred linear position function
$\widetilde u$ (`tex:400–424`) — and consumes freezing exactly once, at the per-pair $<1/3$ level.
Its antichain-sharpness is a property of $\widetilde u$, not of $\lambda_{\mathrm{std}}$. The
variational problem over all $f\in H$, and any genuine Buser/reverse-Cheeger transfer, are
unconstrained by it. **The correct redirect is: the constant-gap target is the right target; the
master bound is the wrong tool for it; look for a bound that is not antichain-sharp.**
**[CONDITIONAL]**

### 7.4 And the sting: "asymptotically weaker" is **numerically stronger** in every plausible range

(LIB) $\mathbb E[\mathrm{inv}_e]\le Cn/\gamma$ versus (LIB-const)
$\mathbb E[\mathrm{inv}_e]\le3.3\times10^{-5}n^2$. These cross at
$n\approx(C/\gamma)/(3.3\times10^{-5})\approx10^5$ for $C=\Theta(1)$, $\gamma=1/3$. Below that,
**(LIB-const) is the harder statement.** At $n=100$: (LIB) permits $\approx300C$ inversions;
(LIB-const) permits $0.33$.

> **[CROSSOVER SUPERSEDED — mg-e35c F5, landed mg-5827.]** At the repaired budget (LIB-const) reads
> $\mathbb E[\mathrm{inv}_e]\le3.3\times10^{-3}n^2$ and the crossover is
> $n\approx3C/(3.3\times10^{-3})\approx\mathbf{900}$, **not $10^5$**; at $n=100$ (LIB-const) permits
> $33$ inversions, not $0.33$. **This matters for the section's own claim**: "every plausible range"
> is **OVERSTATED**. The programme's empirical base lives at $n\le16$, which is still far below
> $900$, so *the direction of the sting is intact* — but the crossover now sits at a size a minimal
> counterexample could plausibly have, rather than two orders of magnitude beyond one. §7.4's
> closing label ("the *direction* of the effect is robust; the number $10^5$ is not") anticipated
> exactly this and is the reason the section survives its own repair.

Since a minimal counterexample — if one exists — is a *specific finite poset of unknown size*, and
the programme's entire empirical base lives at $n\le16$, an asymptotic weakening that carries a
$10^{-5}$ constant is **not obviously a gain at the $n$ that matters**. This is the precise sense in
which the weaker-looking requirement is not good news, and it is a different failure mode from the
one the ticket's warning anticipated: the trap here is not that the condition is too weak to
contradict minimality (§7.1 shows it is not), but that its *constant* makes it operationally
stronger than the requirement it replaces.

**[HEURISTIC — the crossover depends on $F$, $C_3$, $C$ and $\gamma$, none of which is pinned. The
*direction* of the effect is robust; the number $10^5$ is not.]**

---

## 8. What remains under-determined

Reported as a real outcome, per the ticket.

1. **L3's prefix-restriction loss $C_3$** is unquantified in the source, and the Prefix-capture
   conjecture that would quantify it is (a) open and (b) **as literally worded, too weak to use**
   (§4.3). Both the value of $\varepsilon_{\mathrm{spec}}$ and the correct statement of L3 wait on
   this.
2. **L4's modulus $F$** exists only as an empirical envelope (mg-3ce3). Every numeric in §6.4
   inherits that status.
3. **L4 branch (iii) needs the repair of §3.4** before it can close Step 6 at all. Independent of
   this ticket's question, but it is upstream of any attempt to quantify $F$.
4. **The source does not *forbid* the $o(\cdot)$ reading of "$\ll$"** — it merely does not require
   it. The determination in this document comes from the *consumer* (L4), not from Step 5's own
   wording. Anyone who rejects the reading of Claim 3.1 is entitled to the stronger reading; they
   should then say which downstream step consumes it, because none currently does.

---

## 9. Claim ledger

Every claim in the document, including reductions asserted in prose.

| # | Claim | § | Label |
|---|---|---|---|
| 1 | $\Phi_P(A)=\Delta_1(A,A^c)$ for $|A|\le n/2$; the $\varepsilon\to\Delta_1$ conversion is an identity | 2.1 | **PROVEN** |
| 2 | Steps 4 and 5 state the same inequality about the same quantity | 2.2 | **PROVEN** |
| 3 | The source uses $\varepsilon$ for two distinct quantities (spectral / leakage) | 1 | **PROVEN** (reading of `:494`, `:506`, `:459`, `:466`) |
| 4 | L4's $F$ is $n$-free; $\varepsilon$ must be an absolute constant below a threshold | 3.2 | **PROVEN** as a reading; the reading is argued from the quantifier, from the $n$-free downstream, and from usage |
| 5 | Nothing downstream of Step 5 contains an $n$ (the $[1/3,2/3]$ window is absolute) | 3.2 | **PROVEN** |
| 6 | mg-3ce3's pooled envelope is usage evidence for the $n$-free reading | 3.2 | **HEURISTIC** |
| 7 | The branch-(ii)-with-$O(1)$ steelman would demand $\mathbb E[\mathrm{inv}_e]=o(1)$, stronger than everything on the table | 3.3 | **HEURISTIC** (uses the fitted modulus) |
| 8 | Branch (iii) as stated cannot produce the Step 6 contradiction, for any $F>0$, under either reading | 3.4 | **PROVEN** |
| 9 | $\delta(\{a<b\}\sqcup\{c\})=1/3$ exactly, so minimality cannot be strengthened to give interior slack | 3.4 | **PROVEN** (3 linear extensions, by hand) |
| 10 | The endpoint gap is not repaired by any $n$-dependence in $\varepsilon$ | 3.4 | **PROVEN** |
| 11 | mg-3ce3 tested the *repaired* form of (iii), not the stated one | 3.4 | **PROVEN** (quotation, probe `:86–88`) |
| 12 | "$\ll$" in Step 5 = constant fraction, not $o(\min(k,n-k))$ | 4.1 | **CONDITIONAL** on claim 4 |
| 13 | $\varepsilon_{\mathrm{spec}}\le\varepsilon_{\mathrm{leak}}^2/2$; the Cheeger square is a constant loss | 4.2 | **PROVEN** given the sandwich `:318–324` |
| 14 | Antichain: $\lambda_{\mathrm{std}}=0$, $\Delta_1\ge1/2$ on every prefix, right-hand Cheeger is equality | 4.2 | **PROVEN**, by hand |
| 15 | Prefix capture as literally worded gives a constant floor, not a small gap — too weak to use | 4.3 | **PROVEN** (arithmetic on `:360–364`) |
| 16 | Under either repair of prefix capture, L3's loss is a constant $C_3$; no reading injects an $n$ | 4.3 | **CONDITIONAL** on `:360–364` being the intended statement |
| 17 | L3 is the last candidate site for $n$-dependence; the chain is $n$-free end to end | 4.3 | **CONDITIONAL** on 1, 4, 13, 16 |
| 18 | Operative form: $1-\lambda_{\mathrm{std}}\le\varepsilon_{\mathrm{spec}}$, absolute constant, uniform in $n$ | 5.1 | **CONDITIONAL** on 17 |
| 19 | rate $\Rightarrow$ limit $\Rightarrow$ constant-for-large-$n$; neither asymptotic form supplies uniformity | 5.1 | **PROVEN** |
| 20 | mg-7ae7's $1/(\gamma n)$ is inherited from Theorem E's output shape, and Theorem E's own consumer discards it | 5.2 | **PROVEN** (verbatim `step8.tex:68–72`, `:290–305`) |
| 21 | Master bound $1-\lambda_{\mathrm{std}}\le3\mathbb E[D]/(n^2-1)\le6\mathbb E[I]/(n^2-1)$ | 6.1 | **CONDITIONAL** — cited from mg-210d (audited); second inequality and antichain equality re-verified here |
| 22 | $\mathbb E_{\text{unif}}[\text{footrule}]=(n^2-1)/3$ | 6.1 | **PROVEN**, by hand |
| 23 | Requirement (LIB-const): $\mathbb E[\mathrm{inv}_e]\le\tfrac{\varepsilon_{\mathrm{spec}}}{6}(n^2-1)$, i.e. $\mathbb E[D]\le\varepsilon_{\mathrm{spec}}\mathbb E_{\text{unif}}[D]$ | 6.2 | **CONDITIONAL** on 18, 21 |
| 24 | (LIB) $\subsetneq$ (LIB-weak) $\subsetneq$ (LIB-const): the architecture needs less than either debated form | 6.2 | **PROVEN** as a class inclusion; **CONDITIONAL** as the architecture's requirement |
| 25 | Frozen $\Rightarrow\mathbb E[\mathrm{inv}_e]<m/3$ | 6.3 | **PROVEN** |
| 26 | Freezing alone already gives (LIB-const) with constant $2/3$; the whole gap is a constant factor | 6.3 | **PROVEN** |
| 27 | Claim 6.1 through the master bound reproduces mg-210d's $1-\lambda_{\mathrm{std}}<d\,n/(n+1)$ | 6.3 | **PROVEN** (cross-check against an audited result) |
| 28 | Constant budget ~~$\varepsilon_{\mathrm{leak}}\approx0.02$, $\varepsilon_{\mathrm{spec}}\approx2\times10^{-4}/C_3$~~ **$\varepsilon_{\mathrm{leak}}\approx0.20$, $\varepsilon_{\mathrm{spec}}\approx2\times10^{-2}/C_3$** | 6.4 | ~~**HEURISTIC** (empirical $F$) + **UNQUANTIFIED** ($C_3$)~~ **BROKEN as derived (mg-e35c F5)** — the "L4 usable" row it rests on is self-inconsistent; superseded figures 100× too pessimistic |
| 29 | Breadth of the hypothesis class does not break the contradiction; it relocates burden onto L4 | 7.1 | **PROVEN** (logic) |
| 30 | mg-3ce3 stress-tested that heavier burden at $\varepsilon$ an order of magnitude above budget: 0 RED / 6681 | 7.1 | **HEURISTIC** (empirical; no $n$-stratification available) |
| 31 | The condition is not vacuous: every antichain prefix has $\Delta_1\ge1/2$ | 7.2 | **PROVEN** |
| 32 | Master bound cannot deliver the target for any non-chain poset on ~~$n\le100$~~ **$n\le10$** | 7.3 | **PROVEN** given 28 — but 28 is BROKEN; **and weaker than available**: primitivity gives $n\le2/\varepsilon_{\mathrm{spec}}=100$ at the repaired budget (mg-e35c A1) |
| 33 | mg-210d's "best constant $=0$" verdict survives the relaxation; the relaxation buys that route nothing | 7.3 | **CONDITIONAL** on 28, 32 |
| 34 | 33 is a limit of the tool ($\widetilde u$ is antichain-sharp), **not** a lower bound on the problem | 7.3 | **PROVEN** (the bound is a single-test-vector bound, `tex:400–424`) |
| 35 | (LIB-const) is numerically *stronger* than (LIB) below ~~$n\approx10^5$~~ **$n\approx900$** | 7.4 | **HEURISTIC** — direction robust, number not; the number moved 100× with 28 (mg-e35c F5), and *"every plausible range"* is **OVERSTATED** |
| 36 | $C_3$, $F$, the (iii) repair, and the licence for the $o(\cdot)$ reading remain open | 8 | **UNQUANTIFIED / OPEN** |

---

## 10. Proposal for pm-onethird — what STATE.md should say once this lands

**Stated as a proposal, not an edit.** `mg-1fdb` is concurrently reconciling row 8 and the *single
lemma to prove* section; nothing in this document has been written into `STATE.md`, and it should not
be merged into those lines by anyone but the arc that owns them.

> **[PROPOSAL PARTLY SUPERSEDED — mg-e35c, landed mg-5827.]** This proposal was landed into
> `STATE.md` by **mg-23f5** (`e139da3`) and **mg-2860** (`f85a4e8`), *with the audit's amendments*.
> Two riders below are **not** to be re-landed as written:
>
> * **Rider (a) — the `2×10⁻⁴` budget and the `10⁵` crossover.** Do **not** land as flat text
>   (mg-e35c amendment 7). `STATE.md` correctly carries `ε_spec ≲ 2×10⁻²` and the crossover at
>   `n ≈ 900`. The honest form is *"the constant is unpinned by ~2 orders of magnitude and the
>   pessimistic reading is the smaller one."*
> * **Rider (b) — "buys the mg-210d route nothing".** The conclusion survives, but the *reason* is
>   not the numeric budget: the mg-210d route's unconditional output is `ε_spec < 1`, a constant-free
>   fact (mg-e35c F8/F9). What the weakening **does** change is that a constant `λ_std` is now the
>   right currency, so Residual **(R)** is shape-correct and its insufficiency is *quantitative*, not
>   *categorical* — the caveat that used to sit at `STATE.md:130`/`:147` was withdrawn on that basis.
>
> Rider (c) and the branch-(iii) note landed unamended.

> **Proposal.** Row 8 and the *single lemma to prove* section currently state the L1b conclusion as
> the limit `λ_std → 1`, and mg-7ae7 states it as the rate `1 − λ_std ≤ C/(γn)`. Both are
> **stronger than the architecture requires and neither is the operative form.** Backward derivation
> from L4 — whose modulus `F(ε)` carries no `n`, and whose entire downstream (the absolute `[1/3,2/3]`
> window) is dimensionless — fixes the requirement as `1 − λ_std ≤ ε_spec` for an **explicit absolute
> constant `ε_spec`, uniformly in `n`**; the conversions in between are an identity
> (`Φ_P(A) = Δ₁(A,Aᶜ)` for `|A| ≤ n/2`), a squaring of a constant (Cheeger), and one unquantified
> constant factor that the source itself calls a constant fraction (L3 / prefix capture). In inversion
> terms this is **(LIB-const)** `E[inv_e] ≤ (ε_spec/6)(n²−1)` — equivalently
> `E[footrule] ≤ ε_spec · E_unif[footrule]` — which is **strictly weaker than (LIB-weak) `o(n²)`,
> itself strictly weaker than (LIB) `O(n)`**, so the third clause of row 8's implication chain should
> read `(B) ⟹ LIB ⟹ LIB-weak ⟹ (LIB-const) = what L4 consumes`, with each arrow one-way. Three
> riders belong with it, or the row will read as better news than it is: **(a)** the constant is
> small (budget ~~`ε_spec ≲ 2×10⁻⁴`~~ **`≲ 2×10⁻²`**, resting on mg-3ce3's empirical modulus and on
> L3's unquantified
> loss), so (LIB-const) is *numerically stronger* than (LIB) at every `n` below roughly ~~`10⁵`~~
> **`900`** — an
> asymptotic weakening, not a practical one; **(b)** mg-210d's master bound, being antichain-sharp,
> **cannot** deliver it for any non-chain poset on ~~`n ≤ 100`~~ **`n ≤ 10`** (**`n ≤ 100`** for the
> primitive class, which is the relevant one), so the "best constant = 0" verdict
> survives the relaxation unchanged and the correct redirect is to a bound that is not
> antichain-sharp, not to a re-run of that route; and **(c)** mg-7ae7's `1/(γn)` should be recorded
> as inherited from Theorem E's output shape rather than demanded by any consumer — `step8.tex:68–72`
> and Remark `rem:n-dependence-g1` say in terms that the BK cascade needs only "below any prescribed
> positive threshold" and absorb the `n`-dependence into the small-`n` base case. Separately and
> independently of the form question, **L4 branch (iii) as written in the source cannot produce the
> Step 6 contradiction for any `F(ε) > 0`** (it yields `p^P ∈ [1/3 − F, 2/3 + F]`, which is
> consistent with `δ(P) < 1/3`), and the witness `{a<b} ⊔ {c}` with `δ = 1/3` exactly shows minimality
> cannot be strengthened to supply the missing slack; the repair is to restate (iii) as exact
> preservation in `[1/3,2/3]`, which is already the predicate mg-3ce3 tested and found green — row 11
> should carry that note.

---

## 11. Scope statement

One deliverable, as budgeted. Nothing was split off. Not done, and deliberately:

- No edit to `STATE.md` (owned by `mg-1fdb` this cycle; §10 is a proposal only).
- No edit to any file in `one_third_width_three` (different repo; the L4 repair of §3.4 and the
  prefix-capture repair of §4.3 are recommendations to pm-onethird, not landed changes).
- No computation of any kind. The one cheap check that would directly corroborate `n`-uniformity —
  re-stratifying mg-3ce3's survival data by `n` at fixed `ε` — is **flagged and not run**, per the
  standing directive.
