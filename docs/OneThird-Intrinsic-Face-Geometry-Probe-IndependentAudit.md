# Independent audit — `OneThird-Intrinsic-Face-Geometry-Probe.md` (mg-276d)

**Auditor:** mg-e0ce (pre-filed per STATE.md Appendix A; did not author the target).
**Target, derived from the parent's merge commits** `83d253f · 7a67875 · 70f373c · f4c5462`
(the only document those commits add is `docs/OneThird-Intrinsic-Face-Geometry-Probe.md`;
they also add `code/face_geometry/`, which is audited as the instrument).
**Source read independently:** `~/files/intrinsic_face_geometry_program.tex`, 3894 bytes, read in
full before the deliverable's characterisation of it.
**Audit instrument:** `code/face_geometry_audit_e0ce/` — a from-scratch rebuild sharing no code with
theirs; outputs committed (`out_n5.txt`, `out_n6.txt`, `out_extra.txt`).
**Computation:** permitted (Daniel, 2026-07-29) and used by both sides. Its presence is not a finding.

---

## §0 — Verdict

**CONFIRMED. The GREEN stands, and it stands for the reason the deliverable gives.**

Theorems A, B and C are correct for **every finite poset**. I rebuilt both Laplacians from the
definitions by a route that shares nothing with theirs, swept the same complete population, and
re-derived the proof line by line. Every headline number reproduces (table in §2). The generalisation
from Daniel's one four-element example to all finite posets is carried by a **proof**, and the proof
is sound — which makes this the first deliverable in the arc whose most general statement is not
established by generalising from its instance.

**But the arc's standing failure mode did fire, at a sixth new location** — and it is the mildest
instance yet:

- **F1 (over-labelled universal, §0 correction (ii)).** §0 states the left/value reading of claim (2)
  *"fails on the antichain at **every `n ≥ 3`**"* and attributes it to **Theorem B (PROVEN)**. Ledger
  row **D2** labels the same refutation **PROVEN-by-computation on `n ≤ 5`**, and §11's own step-4c
  self-audit explicitly asserts it *"**is not** upgraded to 'proven' in §0 or §12"*. It was upgraded,
  in §0, in the clause the self-audit was checking. **The statement is true** — I verified it to
  `n = 8` and give the two-line proof in §4 below — so this is a mislabel, not a break. Repair: adopt
  the proof and upgrade row D2, or narrow §0 to `n ≤ 5`. **Do not paste §0's clause with row D2's
  label.**
- **F2 (control-coverage gap, §5).** §5 says the ticket requires *"the Laplacian code be demonstrated
  to produce the wrong answer"* and offers **two** demonstrations, the first being **N1 — the
  homology code is not sign-blind**. N1 runs a locally-defined `bad_boundary` through the *homology*
  path; it never touches `top_laplacians`. Worse, the corruption it uses **cannot** fire on the
  Laplacian: I rebuilt `L^rel` with all-`+1` simplicial signs and claims (1)–(3) **still hold**, on
  41/41 posets tested. Of the five `M`-mutations, **only M2 perturbs the construction** of the
  Laplacian from the complex; M1 and M3 perturb the twist, M4 and M5 perturb the target. So the
  deliverable has **no negative control on the boundary-matrix construction**. I supply one
  (facet-parity signs, `audit_extra.py` X3): it **fires on 38/38** posets with `|L(P)| ≥ 2`, and the
  true-sign build passes. **The pipeline survives the control it was missing** — the gap is in the
  argument for trusting it, not in the instrument.
- **F3–F6** — four summary-scope items (§2's independence paragraph, §10's "the foundation", §8.2's
  "hence the mixing time", §0's "not a similar one"). Detailed in §5. None touches a theorem.

**Audited in both directions, as the brief demands.** A RED here is cheap and I looked hard for one:
I pressed vacuity, the twist, the population, the instrument, and the scope, and found the
deliverable had **already closed each of them, correctly, and named the two degenerate subclasses as
non-evidence rather than counting them as successes** (§6.4, §6.5). A GREEN founds a program and is
the comfortable answer in the other direction; the check against that is that the GREEN rests on a
proof I re-derived independently, not on 405 agreeing computations. Both incentives were available
here and neither is what produced the verdict.

**What the GREEN does not buy, and the deliverable says so first:** this is an exact dictionary
between two descriptions of one matrix. §8.3 is accurate and unusually disciplined. Keep it attached.

---

## §1 — Reading the source myself

Read in full, independently of the deliverable. Three things the deliverable says about it that I
confirm, and one it gets right that is easy to get wrong:

1. *"the four-element example"* is **singular and unnamed**. There is no Hasse diagram, no relation
   list, no second four-element reference. The deliverable's decision — **test all 16** rather than
   guess — is the correct response and I verify it was carried out (all 16 rows present in
   `probe_output_n6.txt`, all four columns `True`; independently reproduced).
2. *"up to the orientation/sign twist"* is attached by the source to **claim (1) only**. The
   deliverable's correction (i) — that claim (2) needs it too — is right, and my sweep reproduces the
   6/405 figure with the same 6 posets (the chains).
3. The source writes `Σ_i (1 − s_i)` in `C[S_n]` **without saying which side `s_i` acts on**. True;
   the ambiguity is real and the deliverable is right to raise it.
4. **BK.** The source's BK section is explicitly conditional (*"**If** block moves can be realized
   as…"*) and is not a deliverable of the sketch's claims (1)–(3). Daniel's separate loosening
   (*"doesn't necessarily have to be bk graph"*) is honoured — see §7.

---

## §2 — Rebuild, not check (brief step 4)

`code/face_geometry_audit_e0ce/audit_rebuild.py`. Deliberate divergences from their route:

| object | theirs | mine |
|---|---|---|
| poset enumeration | `posets.py`, their own canonical form | transitively-closed subrelations of the natural order on `[n]`, canonicalised by min-over-`S_n` |
| facets of `F(P)` | `le_to_facet(w)` — **the chain-of-ideals description** | brute-force `Sur_iso(P,[n])` (set partitions × block orderings), **no ideal lattice anywhere** |
| ridges | all `(n−2)`-subsets of facets | brute-force `Sur_iso(P,[n−1])`, independently |
| face relation | delete the `i`-th ideal from a chain | **merge blocks `t, t+1`** of a surjective isotone map |
| `Δ_AT`, ambient Coxeter | from words / `n!×n!` matrix | same in kind, written independently; both right **and** left actions |
| Lemma 1 (chains ↔ `Sur_iso`) | used to build the complex | **never used to build anything** — tested at the end as a claim |

Result — every number in the deliverable, reproduced:

| quantity | deliverable | this audit | |
|---|---|---|---|
| posets up to iso, `n ≤ 6` | 405 (1,2,5,16,63,318) | 405 (same split), A000112 | ✔ |
| claim (1) / (2) / (3)weak / (3)strong | 405 / 405 / 405 / 405 | 405 / 405 / 405 / 405 | ✔ |
| `L^abs = (n−1)I + A`, `L^rel = D + A` | (★), §4 | 405/405 | ✔ |
| every ridge in 1 or 2 facets | all | 405/405 | ✔ |
| facets ↔ `L(P)` | all | 405/405 | ✔ |
| `dim ker L^rel = 1` | 405 | 405 (exact rank to `|L| ≤ 120`; components above) | ✔ |
| non-degenerate | 394 | 394 (claim (1) on all 394) | ✔ |
| untwisted (1) / (2) hold on | 6 / 6, all `\|L\| = 1` | 6 / 6, exactly the six chains | ✔ |
| `\|Aut(P)\| > 1` / disconnected | 275 / 108 | 275 / 108 | ✔ |
| left/value action holds on | 3/5, 5/16, 8/63 | 3/5, 5/16, 8/63 | ✔ |
| claim (2) vs a genuine `n!×n!` compression | asserted | verified `n ≤ 5`, 87/87 | ✔ |
| their Lemma 1, tested not used | PC3 at `n ≤ 4` | 87/87 at `n ≤ 5`, **all `k`** | ✔ |
| **purity** of `F(P)` (row L3) | PC3 at `n ≤ 4` | **404/404 at `2 ≤ n ≤ 6`** — new coverage | ✔ |
| `H̃(F(P)) = S^{n−2}` iff antichain, else acyclic | PC4, `n ≤ 5` | independently, all `n ≤ 4` + antichains `n = 4,5` | ✔ |

**Re-derivability of the instrument.** `bash code/face_geometry/run_all.sh` reproduces
`controls_output.txt` and `probe_output_n6.txt` **byte-for-byte** (17 s here). Every figure in the
document is re-derivable from the committed repo. ✔

---

## §3 — The proof, re-derived

I reconstructed §3–§4 without reading their proof first, then diffed. It is correct.

- **Lemma 3(a).** `[I_{t−1}, I_{t+1}]` is a rank-2 interval of the distributive lattice `J(P)` (graded
  by cardinality). A rank-2 interval of a distributive lattice has at most two atoms: two distinct
  atoms `a,b` join to the top, and a third atom `c` gives
  `c = c ∧ (a∨b) = (c∧a) ∨ (c∧b) = x`, contradiction. Maximal chains = atoms. **Correct.**
- **Lemma 3(b).** With `a = w_t`, `b = w_{t+1}`: the only candidate second atom is
  `I_{t−1} ∪ {b}`, an ideal iff every `P`-predecessor of `b` lies in `I_{t−1}`, i.e. iff `a ≮_P b`;
  and `b ≮_P a` automatically since `a` precedes `b`. So *diamond ⟺ `a,b` incomparable ⟺ `τ_t`
  legal*. **Correct.**
- **Lemma 4.** `|σ| = |τ| = n−1`, `σ ≠ τ`, `ρ ⊆ σ∩τ` with `|ρ| = n−2` forces `|σ∩τ| = n−2`, so the
  shared ridge is unique. **Correct.**
- **The off-diagonal sign.** `σ` and `τ = σ·s_t` differ only in the `t`-th ideal, so the shared ridge
  sits at index `t` in both and the incidence numbers are equal — product `+1`. **Correct**, and I
  reproduce it from the merge picture: merging blocks `t,t+1` of either facet yields the same
  surjection, at the same `t`.
- **(★) `L^abs = (n−1)I + A`, `L^rel = D + A`; `E A E = −A`.** `ε(w·s_t) = −ε(w)`, so `E` anticommutes
  with `A` and commutes with diagonals. **Correct**, and verified on all 405.
- **Theorem B's second equality.** `Σ_i(1−s_i) = (n−1)I − Σ_i R_{s_i}`; restricting rows and columns
  to `L(P)` leaves `(n−1)I` on the diagonal and the **induced-subgraph** adjacency off it. **Correct**,
  and I checked it against a literal `n!×n!` build rather than the identity.
- **Uniqueness of the twist.** Any diagonal `±1` conjugator must satisfy `η(σ)η(τ) = −1` on every
  edge; the AT graph is connected, so `η` is unique up to global sign. **Correct.** One point the
  deliverable does not make but which its own argument covers: `sgn(w)` depends on the *labelling* of
  `P`, and relabelling multiplies every `sgn` by a global sign — so conjugation by `E` is
  labelling-independent and the twist **is** intrinsic. Worth stating, because "the twist depends on
  a choice" is the obvious objection and it has an answer.

**Is it the same twist at every `n`?** Yes — `E = diag(sgn w)`, one formula, no `n`-dependence, no
fitted parameter. Checked at every `n ≤ 6` in my own build. **This is not a twist that varies with
`n`.**

---

## §4 — The two-line proof §0 asserted and row D2 lacked (repairs F1)

**Claim.** For the antichain on `n ≥ 3` elements, the left/value reading of claim (2) is false.

*Proof.* On the antichain `L(P) = S_n`, so the compression is the whole matrix and the left reading
asserts `A_left = A_right` on `C[S_n]`. Take `w = s_1`. Its right-neighbours include `s_1 s_2`; its
left-neighbours are `{s_j s_1}`. Now `s_1 s_2 ≠ s_2 s_1` (the braid relation, `n ≥ 3`), and for
`j ≥ 3`, `s_j s_1 = s_1 s_j ≠ s_1 s_2`. So `s_1 s_2` is a right-neighbour and not a left-neighbour;
the two matrices differ. ∎

Verified computationally at `n = 3,…,8` (`out_extra.txt`, X2); at `n = 2` the two coincide, matching
the deliverable's `n ≥ 3`. **With this, row D2 can be upgraded to PROVEN and §0 needs no narrowing.**

---

## §5 — Exhaustive ledger (including reductions asserted in prose)

`C` = confirmed, `B` = broken, `OL` = over-labelled / mis-scoped. Their row labels in brackets.

| # | claim (site) | their label | verdict |
|---|---|---|---|
| 1 | `Sur_iso(P,[k])` ≅ chains of `k−1` proper ideals [L2] | PROVEN | **C** — re-proved; and tested `n ≤ 5`, all `k`, 87/87, by a build that never uses it |
| 2 | `F(P)` pure of dim `n−2`, facets ↔ `L(P)` [L3] | PROVEN | **C** — re-proved; purity independently verified `n ≤ 6` (their PC3 reached `n ≤ 4`) |
| 3 | every ridge in 1 or 2 facets [L4] | PROVEN | **C** — re-proved (distributivity ⇒ ≤2 atoms); 405/405 |
| 4 | free ridges ↔ forbidden generators [L5] | PROVEN | **C** — re-proved; 405/405 as a set equality |
| 5 | two facets share ≤ 1 ridge [L6] | PROVEN | **C** — re-proved |
| 6 | `L^abs = (n−1)I + A`, `L^rel = D + A` [L7] | PROVEN | **C** — re-proved; 405/405 |
| 7 | **Theorem A**, claim (1), all finite posets [A] | PROVEN | **C** — independently re-derived and re-swept |
| 8 | **Theorem B**, claim (2) = compression [B] | PROVEN | **C** — checked against a literal `n!×n!` compression, not against `(n−1)I − A` |
| 9 | **Theorem C strong**, bijection [C1] | PROVEN | **C** |
| 10 | **Theorem C weak**, `L^abs − L^rel` diagonal count [C2] | PROVEN | **C** |
| 11 | the Laplacian difference does **not** identify *which* generators [C3] | FALSE as stated | **C** — correctly self-refuted; the source's *"precisely"* is right only in reading C1 |
| 12 | the twist is needed for (2) too [D] | PROVEN + by-comp | **C** — 6/405 untwisted, exactly the chains |
| 13 | left/value reading false, **at every `n ≥ 3`** (§0) | attributed to Thm B | **OL — F1.** Row D2 labels it by-computation on `n ≤ 5`; §11 asserts no upgrade was made; §0 makes one. True; proof now supplied (§4) |
| 14 | left/value holds on 3/5, 5/16, 8/63 [D2] | by-comp `n ≤ 5` | **C** — exact reproduction |
| 15 | `E = diag(sgn)` unique up to global sign [E] | PROVEN | **C** — re-derived; add the labelling-independence remark (§3) |
| 16 | `dim H_{n−2}(F,∂F) = 1`, generator `Σ sgn(w)σ_w` [F] | by-comp | **C** — 405/405 |
| 17 | `ker L^abs = 1` iff antichain [G] | by-comp | **C** — reproduced by my own homology path too |
| 18 | AT graph connected [H1] | cited | **C** — correctly cited, not claimed |
| 19 | "relative" = relative to the free-ridge subcomplex [L1] | CONDITIONAL | **C** — correctly labelled. §7's three reasons are honest; reason 1 is admittedly selection-by-consequence and is presented as such |
| 20 | leverage / higher faces / weighted / BK [H2–H5] | untested | **C** — all four correctly declared untested |
| 21 | *(prose, §2)* "**None of the three is built via the chain description**" | — | **OL — F3.** True of the three named objects; the complex whose Laplacians are computed **is** built that way (`le_to_facet` inside `top_laplacians`). Their cross-check reaches `n ≤ 4`; this audit closes it to `n ≤ 6` |
| 22 | *(prose, §5)* N1 is one of two demonstrations that **the Laplacian code** produces the wrong answer | — | **OL — F2.** N1 exercises the homology path only, and the corruption it uses **cannot** fire on the Laplacian (all-`+1` signs: claims (1)–(3) still hold, 41/41) |
| 23 | *(prose, §11)* input (iii) "the standard simplicial signs …"; "**Removing any of (i)–(iv) breaks the result**" | — | **OL — F2b.** False for the sign half as a computed fact. Defensible only if "the result" means "`L^rel` is a Hodge Laplacian at all"; as written it names a load-bearing input that is not one. The inner-product half **is** load-bearing |
| 24 | *(prose, §10)* "**The foundation the sketch rests on** is sound and is a theorem" | — | **OL — F4.** The sketch's foundation also includes the LRB product (§8.3(6), unused), the higher faces (§8.3(3), untested), the Young-module picture (never touched) and the BK realisation (§8.3(2), untested). Narrow to *"the foundation claims (1)–(3) supply"*; §12 inherits this |
| 25 | *(prose, §8.2)* "λ₂(Δ_AT), **hence the mixing time**" | — | **OL — F5.** λ₂ alone does not determine mixing time, and the chain's generator is `(1/(n−1))(D−A)`. §8.3(4) handles the constant; the *"hence"* is not covered |
| 26 | *(prose, §0)* "the **same matrix**, not a similar one" | — | **OL — F6.** `E L^rel E` **is** obtained by a similarity (`E` is an involution). §8.1 says it correctly; §0 read alone denies the operation §8.1 performs |
| 27 | *(prose, §0)* "**All three claims are PROVEN**" vs row C3 "FALSE as stated" | — | **tension, disclosed.** Correction (iii) is in the same section, so this is not a defect — but claim (3) **in the source's own wording** is proven only in a reading the probe supplied |
| 28 | *(repo)* three `__pycache__/*.pyc` committed | — | **hygiene.** Step 7: binary build artifacts in the tree |

**Nothing in this ledger is BROKEN.** Rows 13 and 21–26 are label/scope; rows 1–20 are confirmed.

---

## §6 — The population claim, pressed hardest (brief item 1; step 4d)

**Did it test posets, or *a* poset?** Posets. The population is the **complete isomorphism-class
enumeration** at each `n ≤ 6` — not a sample, not a family with a locked parameter. I re-enumerated
it by a different canonicalisation and got the identical 1, 2, 5, 16, 63, 318.

**Is the tested class the class it claims?** No — and this is the point. The claimed class is *all
finite posets*, which is strictly larger than the tested class, and the gap is bridged by a **proof**
that I re-derived (§3). The proof's inputs are `J(P)` distributive and graded by cardinality, the
standard simplicial structure, and reading L1. **No step uses `n ≤ 6`, connectivity, or `Aut(P)`.**
This is the first target in the arc where the most general statement is proof-carried rather than
instance-carried, and it is why the verdict is CONFIRMED rather than OVERSTATED.

**The four-element ambiguity.** Undecidable from the source — I agree, having read it. All **16**
were tested, not one picked. Verified.

**4d, run against the deliverable's own 4d.** §11 nominates Theorems A/B/C as the most general
statements and clears them. That is right about A/B/C — and **it is not the most general statement in
the document**. Theorems A–C are quantified over posets and proved. §0's *"fails on the antichain at
every `n ≥ 3`"* is quantified over **`n`**, is supported by witnesses at `n ≤ 5`, and its own ledger
row says so. That is the generalisation step, it sits in a *correction to the source* rather than in
a theorem, and the deliverable's self-audit walked past it while checking exactly that clause. **Six
for six, at a sixth new location — and for the first time the over-wide statement is true, with a
two-line proof (§4) rather than a repair.**

**Other scope axes.** *Regime*: complete enumeration, no off-class inference. ✔ *Normalisation*:
`§8.3(4)` closes it explicitly — degree-normalised Laplacians are **not** covered, and I confirm
`D^{−1/2}(D−A)D^{−1/2}` is not the top relative Hodge Laplacian in the orthonormal inner product when
`D` is non-constant. ✔ *Object*: BK and the sub-top faces closed at §8.3(2,3). ✔ *Inference*: proof,
not induction from 405 instances. ✔

---

## §7 — Degeneracy and BK scope (brief items 3 and 6)

**Degeneracy — the vacuity shape this programme has hit before.** Not vacuous here, and the
deliverable got there before me:

- **Antichain** (`L(P) = S_n`): no free ridge, `∂F(P) = ∅`, so `L^rel = L^abs` and claims (1),(2)
  collapse to the ambient statement; claim (3) is vacuously true. The deliverable **names this as the
  one subclass where the bridge says nothing new** (§6.5) and excludes it from the non-degenerate
  count. Correct, and correctly volunteered.
- **Chain** (`|L(P)| = 1`): both sides the zero `1×1` matrix. Excluded, and named as not evidence.
- **394 of 405 are non-degenerate** — `|L(P)| ≥ 2` **and** at least one free ridge — independently
  reproduced, with claim (1) holding on all 394. Largest non-degenerate instance at `n = 6` has
  `|L(P)| = 360`. **The identity is not an identity between two trivial objects.**

**BK, both directions (Daniel: *"doesn't necessarily have to be bk graph"*).** Clean both ways.
The deliverable does **not** treat failure-to-reach-BK as a failure — the verdict is GREEN with
§8.3(2) declaring BK untouched, and BK never appears as a success criterion. And it does **not**
quietly re-impose BK as the target — §10 recommends a *non-BK* next probe (price the Hodge-leverage
bet) in preference to the operator algebra. No finding in either direction.

---

## §8 — Step 4c: every summary diffed against the body

Four summary artifacts (§0, the §8.1 box, the ledger, the §12 row) diffed clause by clause.

- **§0 correction (ii)** — over-labelled, F1 above. **This is the one clause to repair before §12 is
  pasted.**
- **§0 "the same matrix, not a similar one"** — F6.
- **§0 "All three claims are PROVEN"** — in tension with row C3; disclosed in-section (row 27).
- **§8.1 box** — carries "unweighted" and "all finite posets, no restriction" inline. **Clean.**
- **Ledger** — accurate to the body throughout; row C3 self-labels FALSE rather than dropping the
  inconvenient reading. **Clean, and better than the arc's norm.**
- **§12 proposed `STATE.md` row** — audited as a primary artifact. It carries its own conditions
  (unweighted, L1 conditional, `A(P)` not built, the honest net) rather than pointing at them, which
  is what 4c has been asking for since mg-d112. **Three repairs before pasting:**
  1. *"the **antichain** as the smallest witness against it at each `n`"* — scoped in §12 to
     `n = 3,4,5`, so §12 is **already correct**; keep it that way and do **not** import §0's
     "every `n ≥ 3`" unless row D2 is upgraded with the §4 proof. Upgrading is the better repair.
  2. *"the operator-algebra ticket need not re-establish the foundation"* inherits F4 — say **which**
     foundation (claims (1)–(3)), since the LRB product, the higher faces, the Young-module picture
     and BK are all untouched.
  3. *"five named mutations of the identity test, each rejected on 100% of the posets where it
     bites"* — true, and it should not be read as covering the construction of the Laplacian. Add:
     *four of the five perturb the twist or the target; the construction-side control is
     `audit_extra.py` X3, added by the audit, and it fires.*

  With those three, the row is safe to paste. **It is the strongest proposed row this arc has
  produced** — it volunteers the degenerate subclasses, the untested axes and the "no bound, no new
  tool" net without being asked.

---

## §9 — The instrument (brief item 5)

- **Positive controls fire and are real.** P1 (five standard complexes), P2 (A000112), P3 (two
  enumerations of `F(P)` agree, `∂∘∂ = 0`, facets ↔ `L(P)`, ridge multiplicities), P4 (`F(P)` against
  the known homotopy type), P5 (`ker L^abs` vs `H_{n−2}` by disjoint code paths). P5 is genuinely
  sharp. All reproduced independently where I could.
- **Negative controls: five fire, and their vacuity is computed rather than asserted** — I read
  `negative_control_identity` and confirm the applicability test is a real matrix comparison, and
  that M3's 14 vacuous cases are exactly `|L(P)| ≤ 2` (where both sign patterns give product `−1`
  across the single edge). **This is the discipline the programme fixed twice this week, applied
  correctly.**
- **The gap (F2).** No mutation perturbs the boundary-matrix construction; N1, which looks like it
  does, is on the homology path and **could not fire there anyway**. Supplied and committed:
  `audit_extra.py` X3 — facet-parity signs, rejected on 38/38 where `|L| ≥ 2`.
- **Re-derivability.** `run_all.sh` reproduces both committed outputs byte-for-byte. ✔
- **Hygiene.** `__pycache__/*.pyc` committed (row 28).

---

## §10 — Honest net, and what routes on

**Real progress, not relocation.** The source asserted three things about one four-element example;
they are now theorems about every finite poset, with the twist pinned, the side of the `s_i` action
pinned, and one of the three corrected. That is more than the ticket asked for.

**And it buys no bound.** The deliverable says this first and says it repeatedly; I have nothing to
add except that it is right. `Δ_AT` and `E L^rel E` are the same matrix, so every statement transfers
*because they are equal*. Whether the Hodge side carries technique the graph side lacks is untested,
and §10's recommendation — price that bet before building `A(P)` — is the right next question.

**Routes to pm-onethird (first-line), pm-onethird second-line. I have not edited `STATE.md`.**
Actions: (a) repair F1 by upgrading row D2 with the §4 proof; (b) narrow §10/§12's "the foundation";
(c) record F2 so the next deliverable's control battery covers construction as well as comparison;
(d) F3, F5, F6 are one-line wording fixes; (e) drop the `.pyc` files.

**One process note, offered not asserted.** Appendix A says a deliverable's own 4d is not a
substitute for the external pass. This target is the second to run 4d on itself and the first to run
4c on itself as well — and both were careful, and the defect still landed **inside the clause 4c was
checking** (§11 states that correction (ii) was not upgraded in §0; §0 upgrades it). That is the
sharpest evidence yet for the rule: **a self-audit cannot see the sentence it is auditing.**
