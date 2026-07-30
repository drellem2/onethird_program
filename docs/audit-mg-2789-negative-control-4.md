# INDEPENDENT AUDIT of mg-2789 (commit 104fb11) — NEGATIVE CONTROL 4

**Auditor:** mg-fcf1 (pre-filed audit; no coordination with mg-2789)
**Target:** `104fb11` — "probe: NEGATIVE CONTROL 4 — a construction-side control on the
INCIDENCE STRUCTURE that fires, is not absorbable into the twist, and says only what it
verifies (mg-2789)"
**Files audited:** `code/face_geometry/controls.py`, `code/face_geometry/face_complex.py`,
`code/face_geometry/controls_output.txt`, `code/face_geometry/run_all.sh`
**Audit code:** `code/face_geometry_audit_fcf1/` (`rebuild.py`, `audit_nc4.py`,
`audit_extra.py`, `audit_gauge.py`; outputs `out_nc4.txt`, `out_extra.txt`, `out_gauge.txt`)

---

## VERDICT: **OVERSTATED**

**0 BROKEN mathematics.** Every committed number reproduces exactly from an independent
rebuild, and both committed output files regenerate byte-identically. mg-5630's premise —
the one thing that could have made this deliverable worthless — is **CONFIRMED**, not
refuted: this is not built on sand.

The single question the ticket asked — *can this control fail on something the battery does
not already catch?* — has a **split answer**, and it is a different split for each row:

| row | bites | non-similar (real content) | **fires on the gauge it rejected** | can the row fail? |
|-----|-------|---------------------------|------------------------------------|-------------------|
| I1 ridge's facet list | 72/72 | 66 | **6 of 72** | **no — theorem** |
| I2 free/interior split | 82/82 | 82 | 0 | **no — theorem** |
| I3 ridge enumeration | 82/82 | 82 | 0 | **no — theorem** |
| I4 `le_to_facet` off-by-one | 61/61 | 58 | **3 of 61** | yes |

Three of the four rows **cannot fail**, by proof, contradicting the deliverable's explicit
claim that they can. The one row that genuinely can fail (I4, the named load-bearing site)
fires on a pure facet relabelling — the exact gauge for which this section *rejected*
`facet_swap01` — on 3 of its 61 posets, and is **silent on 24 posets where a mis-indexed
`le_to_facet` really does build a different complex**.

So the gap mg-5630 relocated is **narrowed substantially and honestly, not closed**.

---

## WHAT IS CONFIRMED (independently, by a disjoint route)

`code/face_geometry_audit_fcf1/rebuild.py` imports nothing from `code/face_geometry/`. It
builds the facets as the **maximal chains of the proper part of the ideal lattice J(P)** —
the definition of `F(P)` as an order complex — deliberately *not* via `le_to_facet`, which
is one of the sites under audit. The word attached to a facet is recovered from the chain
afterwards and used only for index ordering and the orientation twist. Claim (1),
`E·L^rel·E = D − A`, holds on **86/86** posets on that route.

Reproduced exactly, with my own counts over the population I state (all posets on 2..5
elements up to isomorphism, N = 86):

* **rows I1–I4:** bites 72/72, 82/82, 82/82, 61/61 — identical.
* **vacuity:** 14, 4, 4, 25 vacuous, on `|L(P)|` in `[1,2]`, `[2,6,24,120]`, `[1]`,
  `[1,2,3,4,5,6,8,12,24]` — every multiset identical.
* **absorbability:** 0/72, 0/82, 0/82, 0/61 — identical.
* **spectrum provably moved:** 66/72, 82/82, 82/82, 58/61 — identical.
* **instrument checks:** genuine diagonal conjugation reported absorbable 86/86; one
  diagonal entry moved reported not absorbable 86/86; my own (independent BFS + explicit
  reconstruction) decision agrees with brute force over all `2^m` sign vectors on
  **306/306** `(poset, mutation)` pairs with `|L(P)| ≤ 8` — the same count, and 51 posets ×
  6 modes = 306 checks out.
* **the NC3 witness:** the same predicate scores NC3's facet-parity corruption absorbable
  **82/82** and its spectrum moved **0/82**. So the four rows really are falsifiable *by
  that predicate*, and the witness is real.
* **the rejected candidate:** `facet_swap01` bites 72/86, absorbable 0/72, spectrum moved
  0/72 — identical. And I verify the ground of the rejection: it **is** a
  signed-permutation conjugate of the true matrix on **72/72**. The rejection was correct,
  and reporting it rather than dropping it is exactly the discipline mg-5630 asked for.
* **mg-5630's line-F experiment**, rebuilt independently: NC3's all-+1 line is SILENT
  **86/86** under all four mutations; its parity line bites **82 / 82 / 72 / 79** against
  82 uncorrupted — so it reads verbatim under I1 and I2 and moves only by bite-count
  accident under I3 and I4. **NEGATIVE CONTROL 3 could not have caught any of the four
  incidence errors.** That part of mg-2789's case stands entirely.
* **byte-identical regeneration:** `controls_output.txt` and `probe_output_n6.txt` both
  regenerate with no diff. The probe is untouched.

### mg-5630 IS NOT WRONG — the load-bearing premise re-derived

The ticket named the highest-value possible finding: that mg-5630's gauge-absorption
argument is itself flawed. It is not. Rebuilding the parity corruption from the definitions
and comparing against `diag((-1)^j) · L_true · diag((-1)^j)`:

```
L_parity == D.L_true.D verified on 86/86 posets; the corruption bites on 82.
```

`L_parity = D·L_true·D` holds **exactly, on every poset in the population**. mg-2789 is
built on a sound foundation.

### The runtime rule IS respected (target 6)

`negative_control_incidence` is called unconditionally from `controls.py`'s `main()`, which
`code/face_geometry/run_all.sh` runs. **No scoping, no on-demand split, no reintroduction of
the mg-7db4 defect.** Measured on this host: NC4 alone **1.40 s** (claimed 1.4 s — exact),
`controls.py` 2.2 s user / 3.2 s real (claimed 1.9 s), `run_probe.py` at n ≤ 6 20.1 s user
(claimed 17.4 s). Host variance, not a defect; the conclusion (order-seconds, no scoping
needed) holds.

One wording item: `run_all.sh` now calls this "the CI-adjacent battery". **There is no CI
in this repository** — no `.github`, no workflow or pipeline file of any kind; the only
runners are the two hand-invoked `run_all.sh` scripts. "CI-adjacent" is aspirational.

---

## FINDINGS

### F1 (headline). Two of the four rows fire on the gauge this section rejected

`facet_swap01` was rejected, correctly, because *a relabelling of the facet set is a
signed-permutation conjugation, hence isospectral, hence a gauge*. Applied consistently,
that same standard disqualifies part of two of the four rows that were kept.

**I4, in closed form.** The off-by-one is the true map composed with a cyclic rotation of
the word:

> `prefixes(w[1:]) = prefixes_true(rot(w))`, where `rot(w) = (w_1,…,w_{n-1},w_0)`.

Whenever `rot` maps `L(P)` onto itself, the mutated facet **set** *is* the true facet set
and the mutation is nothing but the permutation `σ` induced by `rot`. For an **antichain**,
`L(P) = S_n` and `rot` is a bijection of `S_n`, so this happens. Further,
`sgn(rot(w)) = (-1)^{n-1} sgn(w)` is a *global* sign, so it cancels in the twist and the
conjugation is a **bare permutation**. Verified:

```
antichain n=3, |L(P)|=6     sigma is exactly the rot map: True
      L_mut[i][j] == L_true[sigma i][sigma j] for all i,j: True
antichain n=4, |L(P)|=24    (same)
antichain n=5, |L(P)|=120   (same)
```

`L_mut = Π^T · L_true · Π` **exactly**. These three posets are **precisely** row I4's
"spectrum provably moved on 58 of those 61" remainder. The output hedges — *"where a row
reports the spectrum moving on fewer than all of its biting posets, NO claim is made either
way on the remainder"* — and that hedge is pointed at the very three posets where the answer
**is** known and is adverse. They are not unseparated; they are **provably isospectral**.

Consequently the committed output's own sentence is false as written:

> *"row I4 replaces it with an off-by-one in `le_to_facet`, **whose spectrum does move**."*

It does not move on 3 of the 61 posets the row counts. (The clause appears in the commit
message too.)

**I1.** Row I1's six unproved posets are not an accident of a short invariant list either.
All six have `|L(P)| = 3`, and on all six the corruption is a **signed-permutation
conjugate** of the true matrix — exhibited, `σ = (0,2,1)`, with characteristic polynomials
agreeing mod `2^61−1` at 5 shifts (degree 3, so this determines the polynomial; the
coefficients are bounded far below the prime, so it is a proof):

```
L_true = [ 1 -1  0]        L_mut  = [ 1  0  1]
         [-1  2 -1]                 [ 0  1 -1]
         [ 0 -1  1]                 [ 1 -1  2]
```

**The classification is complete — no unclassified remainder.** Every biting poset of every
row is either provably non-similar (a spectral invariant moved, so it is not a similarity
transform of any kind) or provably a relabelling gauge:

```
row     bites  non-similar    gauge   unclassified
I1         72           66        6              0
I2         82           82        0              0
I3         82           82        0              0
I4         61           58        3              0
swap01     72            0       72              0
```

**Positive control on this finding's own instrument**, because a gauge detector that always
says "gauge" on small matrices would be worthless: over the 21 biting 3×3 `(poset, mutation)`
pairs it says GAUGE on 6 and NOT A GAUGE on 15, and it never contradicts the spectral proof
(0 cases where it claims a gauge and an invariant proves the spectrum moved).

**Sizing.** This does not break a row. Each row's *stated* claim — "not absorbable into a
diagonal ±1 twist" — is true as written, on 0/72 and 0/61. What fails is the section's own
consistency: the wider gauge family it invoked to reject `facet_swap01` contains its own
corruption on 9 `(poset, row)` pairs. I4 remains a **much better** replacement than
`facet_swap01` (gauge on 3/61 versus 72/72) — the replacement is a real improvement, just
not a clean one.

### F2. Three of the four rows CANNOT FAIL, and the deliverable explicitly says they can

The output's last measurement block states:

> *"mg-2789 added no [CANNOT FAIL] row: each of the four rows above fails if its corruption
> stops biting or turns out absorbable."*

For I1, I2 and I3 **both** failure modes are provably unreachable.
`absorbable_by_diagonal_twist` returns `False` the instant a **diagonal** entry moves
(`s_i² = 1` pins the diagonal). And all three mutations provably move the diagonal:

```
I2: L_mut == L_true + e_j.e_j^T exactly (j = the free ridge's one facet) on 82/82.
    A rank-one bump on ONE diagonal entry.
I3: L_mut == L_true minus that ridge's rank-one outer product on 82/82.
    Both diagonal entries drop by 1.
I1: the abandoned facet's diagonal entry drops by exactly 1 on 72/72.
diagonal of L^rel moves on 72/72, 82/82, 82/82 biting posets respectively.
```

So for those three rows, "absorbable on 0 of N" is **arithmetic, not evidence** — the
predicate cannot return `True` on any of them, at any n, for any finite poset. And they
cannot stop biting either: whenever the mutation applies, the diagonal moves, so `L_mut ≠
L_true`; and `rej == app` follows from claim (1) holding, which the section itself says. The
scored condition `app > 0 and rej == app and absorb == 0` is therefore a **theorem** for
I1, I2 and I3.

Not an artefact of mutating the first eligible ridge, either — swept over **every** eligible
choice:

```
I1   over ALL 1449 eligible (poset, ridge) choices: absorbable on 0, failed to bite on 0
I2   over ALL  981 eligible (poset, ridge) choices: absorbable on 0, failed to bite on 0
I3   over ALL 1459 eligible (poset, ridge) choices: absorbable on 0, failed to bite on 0
```

By the file's own mg-1319 taxonomy these are `[CANNOT FAIL]` rows. This is **mg-78c0's
defect shape at a new location** — a provable statement recorded as an 82/82 observation —
and here it is compounded by an explicit denial that any such row was added. Only **I4** is
a genuine measurement, and I4 is the row with the gauge sub-population and the blind spot in
F4.

The residual real content of I1/I2/I3 is *not* zero: their corruptions genuinely are not
gauges (the trace moves, so they are not similarity transforms of any kind), and that is a
real advance over NC3. The defect is the **evidential status** claimed for it, not the
mathematics.

### F3. Two printed "measurements" are tautologies of the code path

1. > *"the target D-A is byte-identical to the uncorrupted target on 344/344 (poset,
   > mutation) pairs — all four mutations are construction-side only, unlike M4 and M5"*

   `claim1_pair` computes the target as `_, target = at_laplacian(P)`. `incidence_mode` is
   not an argument of `at_laplacian` and is never forwarded to it. The target **cannot**
   differ, for any poset, any mutation, any n. `344 = 4 × 86` is forced by the call
   signature. It is offered as evidence for a property it cannot test.

2. > *"no ridge lies in >= 3 facets under any of the four mutations"*

   Forced for three of the four: I1 sets the re-targeted ridge's facet list to `{j1,j3}`,
   size 2 by construction; I2 does not touch the boundary matrix at all; I3 deletes a row.
   Only the **I4** entry is a measurement.

### F4. I4's vacuity is a different kind of vacuity, under the same label

Vacuity recomputed independently and the reason checked against the real one:

| row | vacuous | kinds | real reason | posets vacuous for another reason |
|-----|---------|-------|-------------|-----------------------------------|
| I1 | 14, `\|L\|∈[1,2]` | 4 chain, 1 antichain, 9 other | fewer than 3 facets, so no third facet to aim at | **0** |
| I2 | 4, `\|L\|∈[2,6,24,120]` | **4 antichains** | no *free* ridge exists — `F(P)` is a sphere | **0** |
| I3 | 4, `\|L\|∈[1]` | **4 chains** | no interior ridge exists | **0** |
| I4 | 25 | 4 chain, 1 antichain, 20 other | the off-by-one *happens* to leave `L^rel` unchanged | — |

For I1/I2/I3 vacuity means **"the mutation did not apply"**. For I4 it means something
categorically different — **"the mutation applied and the pipeline did not notice"**:

```
posets where the off-by-one produces a DIFFERENT facet set and the
claim-(1) test is nevertheless silent: 24 of 86
by |L(P)|: [(1,4), (2,6), (3,3), (4,2), (5,1), (6,4), (8,2), (12,1), (24,1)]
of those, with |L(P)| >= 3 (so not a 1x1 or 2x2 degeneracy): 14
```

On 24 posets (14 non-degenerately) a mis-indexed `le_to_facet` really does build a different
complex and **claim (1) still holds**. That is a genuine, newly-visible limit on the site
F3 of `c0cf104` calls load-bearing, and it is stated nowhere. The row's own wording
("*where the corruption changes `L^rel`*", 25 vacuous) is **correctly scoped** — this is a
missing statement, not a false one — but two different facts are wearing one label, and one
of them is the more interesting.

### F5. "Closes the gap" is sized one notch too wide (target 3, over-claiming direction)

> *"Closes the gap mg-5630 relocated"* — commit message, first line of the body.

Right in kind, too wide in degree. The honest statement the evidence supports:

* the four incidence sites are now perturbed, and NC3 provably could not have caught any of
  them (verified above);
* the named site `le_to_facet` is covered on **61 of 86** posets, of which **58** are
  non-similar corruptions and 3 are the rejected gauge; on **24** the corruption is
  invisible;
* of the four rows, **one** carries measured evidence about the battery's discriminating
  power; the other three carry a theorem about a rank-one perturbation of a diagonal.

Note the direction this cuts *for* mg-2789 as well: I2 uniquely bites on the 4 chains where
M1/M4/M5 are vacuous, which I confirm — that is real, non-overlapping coverage.

### F6 (minor, both directions on the same line)

`run_all.sh`'s new comment replaces a stale "~11 seconds" with measured numbers, which is a
strict improvement. Two small items: the numbers are 15–30% host-optimistic (see above), and
"the CI-adjacent battery" describes a CI that does not exist in this repository.

---

## WHAT I TRIED TO BREAK AND COULD NOT

* **mg-5630's premise.** `L_parity = D·L_true·D` on 86/86. Sound.
* **The absorbability instrument.** My own independent decision procedure (BFS over the
  off-diagonal support graph plus **explicit reconstruction of S and a direct matrix
  comparison**, so a `True` is self-certifying) agrees with brute force over all `2^m` sign
  vectors on 306/306 pairs, and agrees with the committed instrument's answers everywhere.
  It is a correct decision procedure for the right family: the construction's genuine gauge
  freedom is one orientation sign per facet, which is exactly `diag(±1)`, and the battery's
  `M1`/`M3`/`sign_fn` knobs all live in that family.
* **Instance-dependence.** Mutating the first eligible ridge is not a lucky choice: over
  3889 `(poset, ridge)` choices across I1/I2/I3, nothing became absorbable and nothing
  stopped biting.
* **The rejection of `facet_swap01`.** Signed-permutation conjugate on 72/72. Correct, and
  reported rather than buried.
* **Reproducibility.** Both committed output files regenerate byte-identically.
* **The runtime rule.** Unconditional, in-band, 1.40 s.
* **STATE.md.** Untouched, as the commit says. The docs passage it declined to fix is
  flagged explicitly and left to pm-onethird rather than half-fixed. This is the first
  deliverable in the arc to name what it deliberately did not do.

---

## NET

Real progress, and the best-disciplined instrument deliverable in this arc so far: the
predecessor's gauge defect is correctly diagnosed, the fix genuinely perturbs the incidence
structure, a candidate was rejected on principle and the rejection *reported*, the
absorbability question is decided rather than argued, and the printed output hedges honestly
in several places where it did not have to.

The overstatement is at the same location the arc keeps finding it — the deliverable's own
description of its control coverage — and it takes two forms this time. The evidential one:
three of four rows are theorems presented as counts, in a paragraph that explicitly denies
adding a row that cannot fail. The consistency one: the gauge standard used to reject
`facet_swap01` is not applied to the rows that were kept, and it disqualifies 9
`(poset, row)` pairs of them, including all three of the posets the output's own hedge points
at. Plus one genuinely new fact nobody has recorded: on 24 of 86 posets a mis-indexed
`le_to_facet` builds a different complex and claim (1) does not notice.

**RED verdict — OVERSTATED. 0 BROKEN mathematics, 0 unreproduced numbers.**
