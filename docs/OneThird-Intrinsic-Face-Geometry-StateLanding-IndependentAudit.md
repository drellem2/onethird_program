# Independent audit — mg-78c0 (`c0cf104`), the mg-276d/mg-e0ce STATE landing

**Auditor:** mg-5630. **Independent:** did not author mg-276d, mg-e0ce or mg-78c0.
**Object under audit:** the diff of `c0cf104` — `STATE.md` (row 135, Appendix A), `docs/OneThird-Intrinsic-Face-Geometry-Probe.md`
(§0, §2, §4, §5, §8.2, §9, §10, §11, §12), `code/face_geometry/{controls.py,face_complex.py,controls_output.txt}`, `.gitignore`,
and the five deleted `.pyc` blobs. Commit contents confirmed against the ticket's list: **no undeclared candidate**
(`face_complex.py` and `.gitignore` were named; the `code/face_geometry_audit_e0ce/__pycache__` deletions were not, and are
inert).

**Instruments.** (1) `code/face_geometry_audit_5630/audit_nc3.py` → `out_nc3.txt`: a **disjoint** rebuild — own poset
enumeration (transitive-closure filter over upper-triangular relations + orbit dedup), own ideal chains, own boundary
matrix, own `d^T d`. It imports neither `code/face_geometry/` nor `code/face_geometry_audit_e0ce/`. Population re-derived
independently: `{n=2: 2, 3: 5, 4: 16, 5: 63}` = **86**, of which **82** have `|L(P)| ≥ 2`.
(2) `code/face_geometry_audit_5630/audit_x3_equivalence.py` → `out_x3_equivalence.txt`: cross-calls **all three**
implementations (mg-e0ce X3, the adopted NC3, mine) poset by poset under a shared canonical-form index, to settle whether
the adopted control is the audit's control (§2.6).

**Method note (per the coordinator's course correction, and it is the right correction).** Every count below is one I
**produced**, not one I read. The facet-parity corruption was re-implemented from the definitions and run to get my own
number, which is then compared to the committed 82/82; Corollary B′ was **derived** independently before being compared
to the transcript. I also read both reconciliations the coordinator flagged as false-positive traps — the `82`-vs-`86`
vacuity at doc line 365 and the `38/38`-vs-`82/82` population reconciliation at lines 367–369 — and **I file neither as a
finding**: both are correct, and I verified the second rather than accepting it (§2.6, §3.3).

---

## VERDICT: **OVERSTATED**

**0 BROKEN mathematics. Every committed number reproduces, two of them byte-identically. The D2 upgrade is fully
justified and is *not* a disguised generalisation.** What is overstated is the commit's own claims *about method* —
the three places where it changes program state:

- **A1 (primary, BROKEN as claimed).** NEGATIVE CONTROL 3's negative-control content is a **diagonal ±1 gauge
  perturbation, provably absorbable into the twist**, and it **cannot fail on any construction corruption that is not a
  per-facet sign convention** — demonstrated. It closes mg-e0ce's *code-path* gap and does not close the *coverage* gap
  that STATE.md Appendix A says it closes.
- **A2 (OVERSTATED, in `STATE.md`).** "closed … the Lemma-1 cross-check … to `n ≤ 6`" — the audit closed Lemma 1 to
  `n ≤ 5` (87/87). Only purity reached `n ≤ 6` (404/404). The doc states the corrective numbers in the same sentence;
  Appendix A carries the overstatement with the numbers stripped.
- **A3 (internally contradictory, in `STATE.md`).** Row 135 says step 4d's hazard **"did not fire here"**; Appendix A
  says **"the invariant of step 4d held … the defect sat where the document was least expecting it (4d)"**; template
  step 4d still says **"Five for five now"** and does not list the sixth. Three counts, one commit, on the flashiest
  claim in it.

Per the brief's item 6, A1 is **also a finding against mg-e0ce**, whose CONFIRMED verdict I do not soften: the remedy
mg-e0ce supplied is narrower than the rule mg-e0ce asked to be recorded, and mg-78c0 transcribed it faithfully and
promoted it. **The transcription is clean; the transcribed remedy is over-sold.**

---

## 1 — Claim ledger

Every claim the commit added, upgraded, struck or narrowed. (The untouched foundation — L1–L7, Theorems A/B/C, rows
A/B/C1/C2/D/E/F/G — is mg-e0ce's object and was re-derived there; I re-derived Theorem A/B's consequences only where
`c0cf104` leans on them. I found nothing against them.)

| # | claim, as `c0cf104` states it | verdict |
|---|---|---|
| 1 | **Corollary B′ — PROVEN**, the antichain refutes the left/value reading at every `n ≥ 3` | **CONFIRMED** |
| 2 | **ledger row D2 → PROVEN** (+ PROVEN-by-computation), and §0 correction (ii) now agrees with it | **CONFIRMED** |
| 3 | NC3 line 1: true simplicial signs, claim (1) holds **86/86** | **CONFIRMED** (recomputed) |
| 4 | NC3 line 2: all-`+1` signs leave **both** top Laplacians unchanged, **86/86**; claims (1)–(3) survive | statement **CONFIRMED and provable** (stronger than reported); **cited evidence does not measure it** — see §3.2 |
| 5 | NC3 line 3: facet-parity **rejected 82/82** where it bites, bites on all 82 | **CONFIRMED** (recomputed) |
| 6 | the audit's own X3 **fires 38/38** | **CONFIRMED**; population is **41 = 5+16+20**, a `[:20]` truncation — see §3.3 |
| 6b | the adopted NC3 **is** the audit's X3 (*"both numbers are of the same control on different populations"*) | **CONFIRMED** — same rule, same indexing, per-poset agreement 86/86 in all three modes, and the port is **stronger** on population — §2.5 |
| 7 | **the construction-side control closes the gap; "a control battery must cover CONSTRUCTION as well as COMPARISON", and the battery now does** | **BROKEN as claimed** — §2 |
| 8 | "*the pipeline SURVIVED the control it was missing*", no over-correction into "the instrument was broken" | **CONFIRMED and honest** — §2.4 |
| 9 | F2b: *"removing any of (i)–(iv) breaks the result"* struck for the sign half; inner-product half load-bearing | **CONFIRMED**, correctly sized both directions — §4.1 |
| 10 | F3: `le_to_facet` **is** in the pipeline, Lemma 1 is load-bearing, cross-check closed to `n ≤ 6` | substance **CONFIRMED**; the `n ≤ 6` half **OVERSTATED** — §4.2 |
| 11 | F4: *"the foundation"* → *"the foundation claims (1)–(3) supply"* at §10, §12, STATE row | **CONFIRMED**; §12's row *subject line* not narrowed (disclosed) — §4.3 |
| 12 | F5: §8.2's *"hence the mixing time"* struck | **CONFIRMED**, correctly sized — §4.4 |
| 13 | F6: §0's *"not a similar one"* corrected; `E` is an involution so `L ↦ ELE` **is** a similarity | **CONFIRMED** — §4.5 |
| 14 | twist labelling-independence remark | **CONFIRMED** — §4.6 |
| 15 | *"the FIRST proof-carried generalisation in the arc"*, quoted from mg-e0ce | quotation **faithful** (`013e073:23–24`); claim **PLAUSIBLE** — §5.1 |
| 16 | *"SIX for six"* / *"step 4d's hazard did not fire here"* / *"Five for five now"* | **INTERNALLY CONTRADICTORY** — §5.2 |
| 17 | *"the sixth was a label not the mathematics"* | **PLAUSIBLE**, self-flattering as a slogan; long form accurate — §5.3 |
| 18 | artifact hygiene: `.pyc` dropped, `.gitignore`, outputs re-derivable, `~17 s` | **CONFIRMED CLEAN**; one stale number — §6 |

---

## 2 — NEGATIVE CONTROL 3 (the primary axis)

### 2.1 The counts reproduce; the record is real

`python3 controls.py 5` reproduces `controls_output.txt` **byte-identically** (`diff` empty), and after `bash run_all.sh`
`git status --porcelain` is **empty** — so `probe_output_n6.txt` reproduces byte-identically too. Independently, by my
own route: true signs 86/86, all-`+1` 86/86, facet-parity rejected **82/82** and biting on **all 82** posets with
`|L(P)| ≥ 2`. The audit's `out_extra.txt` X3 38/38 is a real recorded run. **Nothing here is fabricated or mis-copied.**
Measured runtime 18.1 s against the doc's `~17 s`.

### 2.2 Does it reach the construction? Yes on the code path — and that is the whole of what it reaches

`claim1_pair(..., sign_mode=…) → top_laplacians(sign_mode=…) → boundary_matrix(sign_mode=…)`. The corruption genuinely
re-enters `boundary_matrix`, which N1 never did. **The code-path half of mg-e0ce's F2 is honestly closed.**

Now the mathematics of the two sign modes, which nobody checked:

**(a) all-`+1` cannot fire, and it is a theorem, not an 86/86 observation.** A facet of `F(P)` is a maximal chain of
proper non-empty ideals, so its members have cardinalities `1, …, n−1`; a ridge omits exactly one cardinality, so the
deletion index `i` is determined by the **ridge alone**, not by the facet. Hence

```
    d_true  =  diag((−1)^{i(g)}) · d_allplus          (row rescaling by ±1)
```

and therefore `d^T d` is **identically equal** in the two modes — absolute and relative, free-row dropping commutes with
a row rescaling. Verified: `TRUE boundary = diag(row signs) * ALLPLUS boundary on 86/86 posets`. So "this corruption
cannot fire here" holds **for every finite poset**, not for 86 of them. The deliverable under-claims; no harm, but the
two-line proof would have made the row airtight instead of empirical, and it is the row the whole F2 narrative rests on.

**(b) facet-parity is a re-orientation, absorbable into the twist.** `sign_mode="parity"` sets
`s = (−1)^i · (−1)^j`, i.e.

```
    d_parity =  diag((−1)^{i(g)}) · d_allplus · diag((−1)^j)   ⇒   L_parity = D · L_true · D,   D = diag((−1)^j)
```

Verified exactly: `parity L_rel == diag((−1)^j) . true L_rel . diag((−1)^j) on 82/82`. Two consequences:

- It is **isospectral**. It cannot detect anything about the construction that the spectrum sees.
- It is **absorbable into `E`**: running claim (1) with `sign_mode="parity"` and twist `E·D` **passes on 86/86**
  (`out_nc3.txt`, line D). So the corruption is observationally identical to *corrupting the twist* — which is exactly
  what NEGATIVE CONTROL 2's **M1** (no twist) and **M3** (wrong twist) already do. It lives inside precisely the
  diagonal-`±1` gauge group that **F6's own repair, in this same commit**, says claim (1) is stated modulo ("the same
  matrix after a relabelling of the basis vectors by signs").
- Independent corroboration that the *specific* pattern `(−1)^j` is doing no work: the two codebases enumerate `L(P)` in
  **different orders on 23 of the 86 posets** (`out_x3_equivalence.txt`), so their `D` matrices differ there — and both
  reject on every one. What the control detects is "the diagonal is not the twist", for **any** non-`±I` diagonal. That
  is the M1/M3 content, reached through a different code path.

### 2.3 Positive control on the control — the check the ticket predicted would be skipped, and it was

I corrupted the pipeline in two genuinely construction-side ways that are **not** sign conventions, and asked what NC3's
three lines report (`out_nc3.txt`, line F):

| deliberate corruption of the construction | NC3 line 1 (true signs pass) | NC3 line 2 (all-`+1` unchanged) | NC3 line 3 (parity rejected) |
|---|---|---|---|
| **mis-indexed facet enumeration** (swap facets 0,1 — corrupts the `le_to_facet` step F3 admits is load-bearing) | fires (14/86) | **SILENT** (86/86) | **SILENT** — still rejects **82 of 82**, check passes verbatim |
| **drop one ridge from the complex** | fires (39/86) | **SILENT** (86/86) | fires only because the *bite-count* moved 82 → 78 — an accident of the `len(par_app)==len(bites)` clause, not a detection |

**NC3's negative-control lines cannot fail on a non-sign construction error.** Line 2 is a tautology under §2.2(a);
line 3 varies a gauge parameter the battery already varied. The only line with real detection power is **line 1** —
`"true simplicial signs: claim (1) holds on 86/86"` — which is **not a negative control at all**: it is a restatement
of the probe's own positive result, already printed two lines above by NC2's `"uncorrupted claim-(1) test passes on
86/86"`.

So the correct sizing:

- **True:** "the true-sign build passes it", "the pipeline survived the control it was missing", "the instrument was
  never wrong".
- **Not true:** Appendix A's *"the battery's coverage of the construction was **zero**, while reading as though it were
  covered"* → implicitly non-zero after the repair. Coverage went from zero to **one absorbable sign gauge**, and it
  still reads as though the construction is covered. **That is the same defect one notch down, in the paragraph written
  to name the defect.**
- **4d, textbook:** a property incidental to the instance (a `sign_mode` knob that happens to re-enter
  `boundary_matrix`) promoted to a law (*"a control battery must cover CONSTRUCTION as well as COMPARISON"*, and this
  battery now does). The hypothesis never made: **that the corruption is not absorbable into a parameter the battery
  already varies.** mg-e0ce's own wording of X3 is narrow and honest — *"perturb the SIMPLICIAL SIGNS of the boundary in
  a facet-dependent way"* — and the over-reading happens at mg-78c0's promotion of it into `STATE.md` (line 330 of the
  audit asked for the rule; the control supplied does not satisfy the rule).

**Recommended third checkable question for Appendix A's next-battery list** (it has two; this is the one that would have
caught this): *(3) is the corruption absorbable into a parameter the battery already varies? If it is, the control tests
the gauge, not the construction.* A control that would satisfy the rule: perturb the **incidence structure** (a ridge's
facet list, the free/interior split, the facet or ridge enumeration) — corruptions that are not diagonal conjugations.
My line-F harness is one.

### 2.4 The framing itself — is *"THE PIPELINE SURVIVED THE CONTROL IT WAS MISSING"* honest?

**Yes.** I pressed this as a self-flattering reading and it survives. The construction is provably correct; all-`+1`
provably cannot fire; facet-parity is correctly rejected; the instrument was not broken and saying so would be false.
The refusal to over-correct into "the instrument was broken" is right, and STATE.md's *"Do not read this row as 'a
control was broken' or 'the Laplacian code was wrong'; neither happened"* is accurate. **The dishonesty is not in the
framing of the survival — it is in the framing of the coverage.**

### 2.5 Is the adopted NC3 the same control as the audit's X3, or a weaker re-implementation wearing its name?

**It is the same control — CONFIRMED, and this one comes out in mg-78c0's favour.** Counts reconciling would not have
established it, so I compared the code and then the per-poset verdicts.

**The rule, in both:** `alternating simplicial sign × (−1)^{facet column index}`, with the column index equal to the
**linear-extension index** in both. mg-e0ce sorts the facets into `L(P)` order explicitly to arrange this
(`audit_rebuild.py:384`, `order = sorted(..., key=lambda i: idx[fw[i]])`, then `s = ((-1)**(t-1)) * (1 if c % 2 == 0 else
-1)`); the deliverable gets it structurally (`facets = [le_to_facet(w) for w in les]`, then
`s = (-1)**i * col_sign`, `col_sign = 1 if j % 2 == 0 else -1`). Same family, same indexing, same alternating factor
(`t−1 ≡ i`).

**Per-poset, not per-count** (`out_x3_equivalence.txt`): all three implementations matched through a canonical-form index
(86 posets recovered by each of the three independent enumerators), then compared boolean-by-boolean:

| sign mode | mg-e0ce X3 == adopted NC3 == mine, per poset |
|---|---|
| `true` | **86/86** |
| `allplus` | **86/86** |
| `parity` | **86/86** |

No disagreement on any poset in any mode. And the agreement is **not** an indexing artifact: the two codebases enumerate
`L(P)` differently on **23 of 86** posets, so their `(−1)^j` patterns genuinely differ there and both still reject.

**The reconciliation at doc lines 367–369 is verified, not merely read.** Running *my* implementation on the *audit's*
population (`posets_upto_iso(n)[:20]` for `n = 3,4,5` → 41 posets, 38 with `|L(P)| ≥ 2`) reproduces the audit's triple
exactly: **true 41, all-`+1` 41, parity rejected 38 of 38**. So "same control, two different populations" is true, and the
port is strictly **stronger** than the original on population (86 complete vs 41 truncated). **No transcription failure
here, and I do not file the raw 38-vs-82 discrepancy as a finding.**

This closes the last open question about the port's fidelity and leaves §2.2–§2.3 exactly as they stand: the control was
transcribed faithfully, and **what was faithfully transcribed is a gauge test.** The defect is in the description of what
such a control covers, not in the porting.

### 2.6 One presentation defect

`controls_output.txt` prints `[PASS]` on a control that provably **cannot** fail, and ends `ALL CONTROLS PASS`. The
mg-e0ce instrument scores the identical fact as `[C3 -] all-+1 signs: claim (1) HOLDS  **FAIL**`. mg-78c0 converted the
auditor's FAIL row into a PASS row. It is disclosed inline (*"reported, not a pass"*), so it is not deceptive — but a
battery whose bottom line is "ALL CONTROLS PASS" while containing a tautological row is the same "reads as though
covered" failure, and this is a committed artifact that will be quoted.

---

## 3 — The numbers, and what the cited evidence actually measures

### 3.1 Corollary B′ / row D2 — CONFIRMED, and it is a proof

I re-derived the argument rather than reading it. Left-neighbours of `s_1` are `{s_j s_1}`: `j = 1` gives `e`; `j = 2`
gives `s_2 s_1 ≠ s_1 s_2` by the braid relation (needs `n ≥ 3`); `j ≥ 3` gives `s_j s_1 = s_1 s_j ≠ s_1 s_2`. So
`s_1 s_2` is a right-neighbour and not a left-neighbour, for **every** `n ≥ 3`, and on the antichain `L(P) = S_n` so the
compression is the whole matrix and Theorem B (PROVEN, all finite posets) supplies `E L^abs E = (n−1)I − A_right`.
**Valid, general, and not a computation wearing a proof's label.** Independently confirmed at `n = 3,…,8`
(`s_1 s_2 ∈ R∖L` at every one) and, by a *different* test than either the deliverable's or the audit's — a full-matrix
comparison of `E L^abs E` against `(n−1)I − A_side` — the left reading **FAILS** at `n = 3,4,5,6` and **HOLDS** at
`n = 2`. Transcription from `013e073` §4 is faithful in substance and in the `n = 2` caveat.

**On the brief's item-4d question — is the D2 upgrade itself the kind of generalisation the commit claims the arc stopped
making?** **No.** The universal is carried by the proof; the `n = 8` computation is correctly demoted to a check on it,
and the doc says so explicitly. The label `PROVEN` is earned. Minor: row D2's lead clause *"and **FALSE** for the
left/value action"* is unqualified where the reading is per-poset (the left form *holds* on 3/5, 5/16, 8/63) — the row's
own body qualifies it correctly, and this phrasing predates the commit.

### 3.2 "both matrices unchanged" is true, and neither cited run measures it

Three places assert it: §5's table (*"**both matrices unchanged**, 86/86"*), §5's F2 prose (*"neither matrix changes …
(audit: 41/41 posets; reproduced here on 86/86)"*), and STATE row 135 (*"both top Laplacians are unchanged by it, so
claims (1)–(3) survive it"*). What the cited runs measure:

- `negative_control_construction` compares `claim1_pair(P, sign_mode="allplus")[0]` against `claim1_pair(P)[0]` — that is
  `E·L^rel·E` **only**. `L_abs` is never compared, and claims (2) and (3) are never re-run under `sign_mode`
  (`claim2_test`/`claim3_test` take no `sign_mode`). The `check()` string nonetheless says *"both top Laplacians
  UNCHANGED"* — **the printed control message asserts more than the code that prints it verifies**, and that string is
  in `controls_output.txt`.
- the audit's X3 41/41 and `audit_rebuild` C4b 23/23 measure **claim-(1) survival**, not matrix equality.

So the statement's cited support is **0 of 2 runs**. I verified it directly and it is **true** — `L_rel` unchanged 86/86
**and** `L_abs` unchanged 86/86 — and §2.2(a) proves it for all finite posets. Given both Laplacians are identical,
claims (2) and (3) survive trivially. **Correct conclusion, mis-cited evidence, in a self-reported control.** Exactly
the class this audit stage exists for.

### 3.3 The audit's population, mis-described

**To be explicit: the `38/38`-vs-`82/82` discrepancy is *not* my finding.** Lines 367–369 reconcile it correctly, and I
verified the reconciliation by reproducing the audit's triple on the audit's population with my own code (§2.5). The
narrower finding is about how that population is *described*.

`construction_side_control()` iterates `posets_upto_iso(n)[:20]` for `n = 3,4,5` → `5 + 16 + 20 = 41`. §5 describes this
as *"(20 posets per `n` at `n = 3,4,5`)"*, which would be 60 and contradicts the 41 the same section quotes twice. It is
a `[:20]` **truncation** — at `n = 5` the control saw 20 of 63 posets, in enumeration order. Substantively harmless (the
probe's own port covers the complete population at `n ≤ 5`, 82/82, which is the number that matters), but neither doc nor
STATE flags the truncation while quoting 38/38 as a headline. **Likewise not a finding:** the `82`-vs-`86` gap is fully
accounted for at doc line 365 — 4 posets have `|L(P)| = 1`, one facet, no second column to flip against — and my own
independent bite count agrees exactly (82 of 86, and the parity mutation bites on **all** 82).

---

## 4 — The strikes and narrowings, each sized in both directions

### 4.1 F2b — correctly sized

Sign half of (iii) **is not** load-bearing: proved in §2.2(a), for all finite posets, not just computed. Strike correct
and in fact under-claimed. Inner-product half **is** load-bearing: `d^T d` is the adjoint w.r.t. the orthonormal chain
inner product; a weighted inner product gives a different matrix and breaks equality with the unweighted `D − A`
(§8.3(4) already scoped this). **No over-correction:** the note keeps the defensible reading of the struck clause and
labels it as a steelman rather than asserting it. Amusing and worth recording: the sign half's non-load-bearingness is a
*consequence of* input (ii) (grading by cardinality), so (ii) is doing work the struck clause credited to (iii).

### 4.2 F3 — substance right, coverage claim overstated

`top_laplacians` does call `le_to_facet`, so Lemma 1 **is** load-bearing for the numbers: confirmed by reading the
pipeline. The narrowing is correct and was needed. **But:** *"it closed the purity and Lemma-1 cross-checks from `n ≤ 4`
to `n ≤ 6`"*. The audit's own `out_n6.txt` reports `their Lemma 1 verified on : 87/87 (**n<=5**, all k)` and
`purity 404/404 (2<=n<=6)`. Purity reached `n ≤ 6`; **Lemma 1 reached `n ≤ 5`.** The doc supplies the corrective numbers
in the same sentence (so it self-contradicts); **`STATE.md` Appendix A repeats the `n ≤ 6` claim for both checks with the
numbers stripped** — *"it closed coverage the deliverable had left at `n ≤ 4` (purity and the Lemma-1 cross-check, to
`n ≤ 6`, by a build that never uses Lemma 1)"*. That is a scope over-statement newly introduced into program state, in
the paragraph about self-audits missing things, while transcribing someone else's audit. (`404` vs `405` is *not* an
error: the audit's range is `2 ≤ n ≤ 6`, the probe's `405` includes `n = 1`.)

### 4.3 F4 — applied, with one unpatched site

Narrowed at §10, at §12's recommendation clause, and in the live STATE row (*"the **foundation claims (1)–(3) supply**
for the intrinsic face-geometry program"*). The list of what is *not* covered (left-regular-band product,
higher-codimension faces, Young modules, BK realisation) matches §8.3. **Not narrowed:** §12's proposed-row *subject
line* still reads *"the **intrinsic face-geometry program's foundation**"*. Disclosed by the new "Status: landed … the
row as it stands in `STATE.md` is the authority" note, so this is a stale-proposal artifact rather than a live
over-claim.

### 4.4 F5 — correctly sized

The chain one would want is generated by `(1/(n−1))(D−A)`, so the *"hence"* did not follow from `λ_2(D−A)` as the row
stated. Strike correct. The stated reason *"`λ_2` alone does not determine a mixing time"* is loose in isolation — a gap
fixes the relaxation time exactly and `t_mix` to within `log|L(P)|` — but the note's operative clause is *"the 'hence'
was never covered by anything in **this document**"*, which is a claim about the document and is true. **No
over-correction:** the surviving row (`λ_2 ↔ first nonzero eigenvalue`) is exactly what the identical-spectrum row
already licenses.

### 4.5 F6 — correct

`E = diag(sgn w)`, `E² = I`, so `E L E = E L E^{−1}` **is** a similarity; the original *"the same matrix, not a similar
one"* was self-contradictory. The replacement (*"the same matrix after a relabelling of the basis vectors by signs, …
not an isospectral coincidence"* + the known-conjugator gloss) is right, and §8.1 is correctly named as the form to
quote. Note the coupling to §2.2(b): F6 concedes the identity is stated modulo the diagonal-`±1` gauge, and NC3's live
corruption lies inside that gauge.

### 4.6 The twist labelling-independence remark — correct

Relabelling `P` by `π` sends each linear extension `w ↦ π∘w`, so `sgn ↦ sgn(π)·sgn`, so `E ↦ sgn(π)E` and
`E L E ↦ sgn(π)² E L E = E L E`. Correct, and correctly described as covered by the existing uniqueness argument rather
than as a new fact.

---

## 5 — The meta-claim (brief item 4d: audit the most general statement, wherever it sits)

### 5.1 *"the FIRST proof-carried generalisation in the arc"* — quotation faithful, claim PLAUSIBLE

The quoted sentence is verbatim in `013e073` lines 23–24. Attribution to the auditor is correct and explicit. As a
claim it is **mg-e0ce's**, quantified over "the arc", and I cannot refute it: the arc's prior deliverables are largely
refutation-by-witness, where the general statement *is* generalised from a witness family — which is the locked-parameter
failure mode itself. **Two caveats.** (i) The generalisation it credits (one four-element example → all finite posets,
by Theorems A/B/C) is **mg-276d's, landed at `70f373c`**; `c0cf104` re-describes it, and the row title change is
accurate as re-description, not as new result. (ii) The denominator is unstated: "the arc" here means *the deliverables
Appendix A tracks a 4d finding for* — a perfect 6/6 rate whose sample is the audited subset. Appendix A does name the
five, so this is disclosed by construction rather than hidden.

### 5.2 *"SIX for six"* vs *"4d did not fire here"* vs *"Five for five now"* — INTERNALLY CONTRADICTORY

`c0cf104` leaves three mutually inconsistent statements in `STATE.md`:

| site | says |
|---|---|
| row 135 | *"Step 4d's own hazard — instance read as law — **did not fire here**; what fired was a label"* |
| Appendix A, new para (line 250) | *"**The invariant of step 4d held**: the over-wide statement was at a **sixth new location**"*; *"the defect sat where the document was least expecting it (**4d**)"* |
| Appendix A, template step 4d (line 199) | *"**Five for five now**, at a new location each time"* — mg-e0ce/mg-276d **not listed** |

The row and the new paragraph directly contradict each other on whether 4d fired on mg-276d, and the template step the
paragraph is amending was not re-counted. My own reading sides with **Appendix A**: §0 asserted a universal in `n` from
`n ≤ 5` antichain witnesses with no proof in the document — that *is* instance-read-as-law, and it was defused only
because an external auditor supplied a proof afterwards. So the row's *"did not fire here"* is the wrong one of the
three, and it is the one in the summary that gets quoted. This is the commit's own §4c hazard firing on the commit, in
the artifact the commit exists to write.

### 5.3 *"the sixth was a label not the mathematics"* — PLAUSIBLE, self-flattering as a slogan

The long form in Appendix A is accurate and well-hedged (*"a universal in `n` attributed to a theorem while the ledger
row carried `PROVEN-by-computation on n ≤ 5`"*, *"the only one where the over-wide statement is TRUE"*, *"repaired by an
upgrade … not a retraction"*). All of that I confirm. The **slogan** compresses it into something milder than the fact:
a *label* error is `PROVEN` written where `PROVEN-by-computation` was meant **for a statement already proved**. Here no
proof existed in the deliverable; the mathematics of the universal was **absent**, and the auditor supplied it. The real
distinction from the prior five — the over-wide statement was *true and provable* rather than *false* — is genuine and
is the finding worth keeping; *"a label not the mathematics"* is not that distinction, and it is the phrase that
travels.

---

## 6 — Constraint compliance / artifact hygiene — CLEAN

Computation was permitted, so I flag none per se. Proportionality: `controls.py` +59 lines, `face_complex.py` +30, one
4-line output append. `.gitignore` is two lines (`__pycache__/`, `*.pyc`); five previously-tracked `.pyc` blobs removed;
`git ls-files` now shows **no** `.pyc` or `__pycache__`; no tracked file over 60 KB except the pre-existing `STATE.md`.
No stray dataset, no large enumeration. Re-derivability is the strongest part of this commit: `bash run_all.sh` leaves
`git status --porcelain` **empty**.

One stale number: the doc's re-derivability line was updated `~11 s → ~17 s`, but `run_all.sh`'s own header still says
`# Total runtime on a 2024 laptop: ~11 seconds`. Measured here: **18.1 s**. Also cosmetic: the new §0 block says *"Six
repairs"* while seven sites are marked (F1, F2, **F2b**, F3, F4, F5, F6).

---

## 7 — State changes and effect on prior work

- **mg-276d (`70f373c`, `f4c5462`) — upheld.** Theorems A/B/C untouched by anything here; row D2's upgrade is earned.
- **mg-e0ce (`013e073`) — CONFIRMED verdict **not** softened, and one finding **against** it.** Its F1 (over-labelled
  universal) and its diagnosis of F2 (N1 is on the homology path and provably cannot fire on the Laplacian) are both
  correct and I reproduced both. Its **remedy** for F2 is weaker than the rule it asked to be recorded: X3 perturbs the
  boundary matrix only by a diagonal `±1` gauge that is absorbable into the twist, so it does not demonstrate the
  construction coverage the rule demands. mg-e0ce's own wording of X3 is appropriately narrow; the over-claim is created
  at mg-78c0's promotion.
- **`STATE.md` — two items need PM action** (I did not edit it): the Lemma-1 `n ≤ 6` overstatement in Appendix A (§4.2),
  and the 4d contradiction across row 135 / the new paragraph / template step 4d (§5.2).
- **No prior claim is refuted.** Nothing here reopens a GREEN or flips a ledger row.

---

## 8 — THE HONEST NET

**Real progress.** The D2 upgrade is genuine: a universal that was asserted-and-unproven is now proved, generally and
correctly, and the label matches. The six repairs are all in the right direction and four of them (F2b, F4, F5, F6) are
correctly sized in both directions. The control was ported **faithfully** — same rule, same indexing, per-poset agreement
with the original on 86/86, on a strictly larger population (§2.5). Re-derivability is exemplary — two committed outputs
reproduce byte-identically. Artifact hygiene is clean. The refusal to over-correct the control finding into "the
instrument was broken" is right and I tried to break it and could not.

**Relocation, not progress.** NEGATIVE CONTROL 3. It moved the control-coverage gap from *"no control reaches the
construction's code path"* to *"a control reaches the code path and varies only a gauge the battery already varied,
and cannot fail on a non-sign construction error."* The gap that mattered — can this battery distinguish a correct
construction from an incorrect one? — is **still open**, and it is now recorded in `STATE.md` as closed, with a forward
rule the adopted control does not satisfy. `le_to_facet` is the concrete uncovered site, and F3 in the same commit
identifies it as load-bearing.

**Vacuous.** NC3 line 2 as a control (it is a theorem, not a test) and NC3 line 1 as a *negative* control (it duplicates
NC2's last line).

**The pattern holds, at a seventh location.** Arithmetic: not wrong once. Mathematics: not wrong once. The over-wide
statement is in **the commit's own claim about its control coverage**, and the contradiction is in **the commit's own
claim about the arc's track record** — i.e. in the two most self-congratulatory sentences it wrote, both of them about
method rather than about posets. The deliverable predicted this genre of failure in the same commit ("*a self-audit
cannot see the sentence it is auditing*") and then instantiated it, one level up: **an audit-driven repair cannot see the
sentence that describes the repair.**

---

*mg-5630, 2026-07-30. Instruments: `code/face_geometry_audit_5630/audit_nc3.py` → `out_nc3.txt` (disjoint rebuild) and
`audit_x3_equivalence.py` → `out_x3_equivalence.txt` (three-way per-poset cross-check). Verdict mailed to pm-onethird,
who owns `STATE.md` and the Daniel report. This auditor did not edit `STATE.md`, and did not ask what pm-onethird's
independent D2 verdict was before deriving its own.*
