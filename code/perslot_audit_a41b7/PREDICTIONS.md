# `mg-41b7` — predictions for the INDEPENDENT AUDIT of `mg-200d`

Committed **before** any script of this audit exists, and **before one byte** of
`code/perslot_symmetry_200d/`, `docs/OneThird-PerSlot-AdjacencySymmetry-mg-200d.md`,
`STATE.md`, or `code/dual_certificate_131e/` has been read.

Target under audit: `mg-200d`, landed on `main` at

* `762921d` — `finding+instrument+docs: PER-SLOT ADJACENCY SYMMETRY BUYS Θ(n²) → Θ(n), NOT A CONSTANT — AND THE TICKET'S OWN SIZING PARAGRAPH IS WRONG BECAUSE OF IT (mg-200d)`
* `ffc5501` — evidence transcripts
* `731a9ab` — the post-landing re-check

`main` at the time of writing is `dafe75910f731927affdf366457d681e262acf62`.

---

## 0. Prior exposure — disclosed, not laundered into predictions

This audit is **heavily contaminated before it starts**, and most of the contamination arrived
in the dispatch prompt itself. Every one of the following was in my hands before a single
prediction below was written. Anything I score as a "hit" that lives in this list is a
**reproduction**, and I say so at the prediction.

* **H1.** My dispatch prompt quotes commit `b7b6941` verbatim in its recent-activity block:
  *"THE <= DIRECTION IS CERTIFIED AT n=3,4,5 AND IS FALSE AT n=6 — mg-200d's eps_spec = 2/(n+1)
  IS A SMALL-n COINCIDENCE, AND THE ROUTE HAS NO TARGET TO PROVE"*. So I already know
  `mg-200d`'s headline rational **and** that a sibling claims to have broken it at `n = 6`.
  My dispatch explicitly forbids reconciling against `mg-131e`; I will not, but I cannot
  un-read it.
* **H2.** The same block quotes `c80a4f1` (`mg-94c3`), which hands me `mg-200d`'s numbers in
  full: *"E[inv] = 2/3, 1, 4/3 at n = 3,4,5 gives 6E/(n^2-1) = 1/2, 2/5, 1/3 = 2/(n+1)"*.
  There is nothing left to predict about **what number `mg-200d` reports**.
* **H3.** Before writing this file I ran `git log --grep=mg-200d` and read commit **subjects**
  (not bodies, not files). That gave me `mg-200d`'s headline —
  *"PER-SLOT ADJACENCY SYMMETRY BUYS Θ(n²) → Θ(n), NOT A CONSTANT — AND THE TICKET'S OWN
  SIZING PARAGRAPH IS WRONG BECAUSE OF IT"*. This **pre-answers brief item 3** (it reports an
  improvement) and **most of brief item 6** (a sizing sentence exists, and it is a correction
  of the ticket's own).
* **H4.** The same listing gave me `mg-200d`'s own predictions subject `a21bf88`, which
  discloses three of its hand measurements: its **H2** (all-pairs adjacency symmetry holds for
  uniform `L(P)` iff `P` is an antichain), its **H4** (*"it is outright INFEASIBLE at n=3"*),
  and its **H7** (`mg-6bc2`'s adjacency diagnostics were computed on a sub-probability measure
  of mass `2/3`). H4 is *directly* the subject of brief item 4.
* **H5.** I listed `code/perslot_symmetry_200d/` **file names only**:
  `lp200d.py`, `v1_forms.py`, `v1b_n6_surrogates.py`, `v2_disjunctive.py`, `v3_families.py`,
  `selftest200d.py`, plus transcripts including `out_v1_n6.txt`. From names alone I infer
  `mg-200d` tested **several forms** and a **disjunctive** variant, and that it attempted `n=6`.
  That materially reshapes brief item 2, which presumes a single imposed symmetry.
* **H6.** The dispatch tells me `mg-00a1` is in flight downstream, and `git log --all` shows a
  commit `bb0d7e9` **not on `main`** claiming *"THE DISJUNCTIVE PER-SLOT VALUE IS Theta(n^2) —
  SUPERLINEAR ... mg-200d's Theta(n^2) -> Theta(n) HEADLINE IS REFUTED"*. I will not read it and
  will not reconcile against it; it is disclosed so that agreement with it later is not read as
  independent corroboration.
* **H7.** My brief carries a **self-correction** stating that its own item 5 is false, and hands
  me the corrected version (`mg-6bc2` Claim 3.1 inversion attainment is all-`n` by a two-atom
  construction; Claim 4.1 footrule attainment is the finite-population `{3,4,5,6,8}` one).
* **H8.** I read `code/pairbias_sharpening_6bc2/README.md` — the **parent**, not the party under
  audit — to fix the baseline LP. It states: maximise `E[inv_e]` over all probability measures
  on `S_n` subject to `P(pair flipped against e) ≤ 1/3` for every pair; `max = C(n,2)/3`. It
  also carries `mg-ba78`'s in-place repair banner, which **strikes** the pre-repair adjacency
  diagnostics: the completed optimum violates *aggregate* adjacency symmetry at **2 of 3** pairs
  at `n=3`, where the superseded figure said **0**.

### Hand measurements made before any prediction below, and before reading `mg-200d`

* **H9 (mine, by hand, `n = 3`).** With `J_k(x,y) = μ{σ : σ⁻¹(k)=x, σ⁻¹(k+1)=y}`, the **literal**
  per-slot system `J_k(x,y) = J_k(y,x)` for **all** slots `k` and **all** pairs forces, at `n=3`,
  `μ₁₂₃=μ₂₁₃`, `μ₁₃₂=μ₃₁₂`, `μ₂₃₁=μ₃₂₁` (slot 1) and `μ₃₁₂=μ₃₂₁`, `μ₂₁₃=μ₂₃₁`, `μ₁₂₃=μ₁₃₂`
  (slot 2), whose only solution with `Σμ = 1` is the **uniform** measure. Uniform has every pair
  flipped with probability `1/2 > 1/3`. So the literal system **intersected with the pair-bias
  relaxation is INFEASIBLE at `n=3`** — not "optimum 0", *empty*. This agrees with `mg-200d`'s
  own disclosed H4 (see H4 above), which I had already read; the derivation is mine.
* **H10 (mine, by hand, `n = 3`).** The **aggregate** form `J(x,y) = J(y,x)`, `J = Σ_k J_k`,
  combined with `E[inv] = 1` (which forces all three flip probabilities to exactly `1/3`) is
  **also infeasible** at `n=3`: the three symmetry equations sum to `μ₁₂₃ = μ₃₂₁`, and then
  `μ₁₃₂ = μ₂₃₁`, `μ₂₁₃ = μ₃₁₂`, forcing `p₂+p₃+p₄+p₅ = 2/3` against the normalisation's `1-2t`,
  i.e. `2/3 = 1`. **So the aggregate form does NOT "exclude nothing" at `n=3`.**
* **H11 (mine, arithmetic on H2).** `2/3, 1, 4/3 = (n-1)/3` at `n = 3,4,5`, and
  `6·((n-1)/3)/(n²-1) = 2/(n+1)` identically. So `mg-200d`'s number, in the `E[inv]` currency the
  parent LP is written in, is `(n-1)/3` against the parent's `C(n,2)/3 = n(n-1)/6` — a ratio of
  exactly `2/n`, which is what turns `Θ(n²)` into `Θ(n)`.

---

## 1. Predictions

Confidence in brackets. Predictions marked **[REPRO]** are reproductions of figures already in
my hands via §0, kept only so the arithmetic is checked, and they may not be scored as hits.

**P1 [0.90].** `mg-200d` uses `fractions.Fraction` throughout and there is no floating-point
number anywhere on the path from the constraint matrix to the reported optimum.

**P2 [0.90].** The value `mg-200d` reports does **NOT** come from the literal all-pairs /
all-slots per-slot system, because (H9) that system is infeasible at `n=3` against the pair-bias
constraint. It comes from a **weakened** form.

**P3 [0.80].** `mg-200d` says so itself — it reports the literal per-slot form as infeasible
(or as forcing uniform) somewhere in its deliverable, rather than silently substituting.

**P4 [0.60].** The weakening is **disjunctive**: a maximum over branches, each branch imposing
per-slot symmetry only on a selected set of pairs/slots, rather than a single relaxed LP.
(Inferred from the file name `v2_disjunctive.py` — H5 — so this is half-exposed.)

**P5 [REPRO, 0.75].** My own exact-rational LP, sharing no code with
`code/pairbias_sharpening_6bc2/` or `code/perslot_symmetry_200d/`, reproduces `E[inv] = 2/3, 1,
4/3` at `n = 3,4,5` for whatever form `mg-200d` actually solved.

**P6 [0.95].** No poset is enumerated anywhere on `mg-200d`'s path. The object is measures on
`S_n` throughout.

**P7 [0.85, half-exposed via H3].** A sizing sentence exists, it is stated against
`ε_spec = 3·d·q̄·n/(n+1)` and the `d·q̄ ≤ 1/150` target, and it says this is a **milestone, not a
wall-breaker** — indeed the headline says the ticket's own sizing paragraph is *wrong*, so I
predict the correction runs in the **pessimistic** direction (the per-slot value is *smaller*,
so it supplies *less*, so the wall gets *further away*, not closer).

**P8 [0.55].** The `Θ(n²) → Θ(n)` growth statement rests on an exact sweep at `n ≤ 5` plus an
unfinished `n = 6`, and is marked at the claim as a **conjecture/pattern**, not a theorem for
all `n`. If it is stated as an all-`n` theorem off a finite sweep, that is BROKEN and it is the
error this lineage makes most often (my brief's item 5, in its *corrected* form per H7).

**P9 [0.85, hand-derived at H10].** Brief item 2's premise — *"mg-6bc2 measured that the
aggregate form excludes NOTHING at n=3"* — is **FALSE**, and it is traceable to `mg-6bc2`'s
**superseded** pre-`mg-ba78` figure of `0` aggregate violations, which was measured on a
sub-probability measure missing a third of its mass and has since been struck to `2 of 3`.
If so, **my own brief is wrong on the same point twice** (item 5 already conceded), and I should
say so rather than score `mg-200d` against it.

**P10 [0.70].** I will **not** find a feasible measure beating `mg-200d`'s reported optimum
*in the form it actually solved*. (Brief item 3 asks me to try; I will, and I expect to fail.)

**P11 [0.60].** The optimum is **exhibited** by an explicit measure whose per-slot constraints I
can verify by substitution, not merely returned as a solver value.

**P12 [0.50].** The load-bearing defect, if there is one, is **not a rational number** — it is a
scope/kind statement: the growth claim, the branch the value belongs to, or the currency
(`E[inv]` vs `ε_spec` vs `ε_c3ca`).

---

## 2. My two most likely errors, filed in advance

**P13 — I score a difference of CONSTRAINT FORM as a mathematical error.** "Per-slot adjacency
symmetry" has several defensible formalisations (`σ⁻¹(k)` vs `σ(k)`; ordered vs unordered pairs;
slots `1..n-1` vs `1..n` cyclic; equalities vs the disjunctive relaxation). If I pick a different
one and get a different number, the honest finding is *"the ticket is ambiguous"*, not
*"mg-200d is wrong"*.
**Guard, bound before I open `lp200d.py`:** I will extract `mg-200d`'s constraint **rows** from
its code and assert, as an *assertion and not a dependency*, that my independently generated rows
are a permutation of its rows. A numeric disagreement is a finding **only** if the rows agree and
the optima do not. If the rows differ, the finding is about the *reading*, and I will report both
numbers with both readings named.

**P14 — I conflate INFEASIBLE with OPTIMUM ZERO in my own solver** and report a false
infeasibility (or, worse, a false optimum on an empty polytope). This is precisely the confusion
brief item 4 warns about, and it would be committed by the auditor sent to check for it.
**Guard, bound before any LP is solved:** my solver is **two-phase**; it prints the phase-1
residual explicitly; and my selftest feeds it (a) a knowingly infeasible system, (b) a knowingly
feasible system whose optimum is `0`, and (c) a knowingly feasible system with a known nonzero
optimum, and **requires all three to be distinguished**. If that negative control does not fire,
no LP result in this audit may be reported.

---

## 3. What I have already decided NOT to do

* Not reconcile against `mg-131e` (`b7b6941`) or `mg-eaa1` (`35edad7`), and not read
  `code/dual_certificate_131e/` or `code/dual_certificate_audit_eaa1/`. `mg-131e`'s landing is
  **not** evidence about `mg-200d`; treating it as such is the circularity this stage exists to
  break.
* Not read `bb0d7e9` / `mg-00a1`, which is not on `main`.
* Not import, execute, or copy `lp6bc2.py` or `lp200d.py` into my solving path. The **only**
  permitted contact with `mg-200d`'s code is reading it to extract its constraint rows for the
  P13 assertion.
