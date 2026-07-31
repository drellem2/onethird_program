# mg-e35b — landing the rest of mg-fcf1 on NEGATIVE CONTROL 4

mg-fcf1 audited mg-2789 (NEGATIVE CONTROL 4, the incidence-structure control) on 2026-07-30 and
returned **OVERSTATED, 0 BROKEN mathematics**. Its verdict was filed as *dropped — no landing commit
and no successor*. **That premise is half wrong and the correction is the first thing this ticket
found:** `8fc5111` (mg-8a12) landed mg-fcf1's F2 and `f024985` (mg-da45) landed the row-I4 reason,
and both were themselves audited (`de54c3a`, `1d922a1`) and repaired again (`5cae82c`, `c7f9673`,
`b6bc2ef`, `0fb0e00`, `bfd7948`). What was still unlanded at HEAD is what is landed here.

## What was already landed before this ticket, and is not touched

| mg-fcf1 | landed by | state at HEAD |
|---|---|---|
| F2 — three rows cannot fail | mg-8a12 `8fc5111` | a single `[CANNOT FAIL]` row; the contradicted self-report corrected in place |
| F1 — *"whose spectrum does move"* is false | mg-8a12 / mg-da45 | the sentence is narrowed and cites mg-fcf1 |
| F5 — *"closes the gap"* | mg-a806 into `STATE.md` | recorded as *relocation, not closure* |

## What this ticket lands

**F1/F2 tail — the gauge standard is now asked of the rows KEPT.** `facet_swap01` was rejected
because *a relabelling of the facet set is a signed-permutation conjugation, hence isospectral*, and
that sentence was never turned on the four rows kept. Turned on them it disqualifies **9 (poset,
row) pairs**. `signed_permutation_witness` (in `controls.py`, beside `absorbable_bruteforce`)
classifies every biting pair **GAUGE** — an exhibited permutation and sign vector, reconstructed in
full and compared entry by entry — or **NON-SIMILAR** — a spectral proof. The dichotomy is complete:
**297 = 288 + 9 + 0**, per row I1 66/6, I2 82/0, I3 82/0, I4 58/3, and swap01 0/72. Two scored rows
are added: the completeness of the dichotomy, and a positive control on the detector.

The sentence this replaces was *"THIS FILE makes no claim either way on the remainder"*. **It covered
exactly the nine pairs where the answer is known and adverse.** A hedge is not automatically honest.

**F3 — two printed measurements were tautologies.** Both are now printed as properties, with the
forcing named: the target's byte-identity on 344/344 is forced because `at_laplacian` takes no
`incidence_mode` (checked here in the AST, not argued), and three of the four `no ridge in ≥ 3
facets` zeros are forced because I1/I2/I3 never *raise* a ridge's facet count. That the comparisons
can move at all is shown separately — by M4/M5 for the target, and by I4's zero being the one
measurement of the four.

**F4 — `vacuous` was one word for two facts.** For I1/I2/I3 it means the mutation did not apply (14,
4, 4 — and **0** for any other reason). For I4 it means the opposite: the mutation applied on **all
25**, built a genuinely different facet set on **24** of them (**14** with `|L(P)| ≥ 3`), and claim
(1) still held — **the pipeline is blind to the named load-bearing site there**. Stated in row I4 and
in the measured block; **deliberately not scored**, because a row scoring *"the split separates"*
would go red the day somebody fixed the blindness.

**F5 — coverage sized.** `61/86` at `le_to_facet`, of which `58` are non-similar. Printed in the
section. `STATE.md` is not edited from here: it already carries the qualitative correction and is
pm-onethird's ledger, so the numbers are routed to them — the same choice mg-2789 made about the
`Probe.md` passage it flagged rather than half-fixed.

**Minor — `run_all.sh` called this "the CI-adjacent battery".** There is no CI in this repository
(no `.github/`, no `.gitlab-ci.yml`, no `.circleci/`, no `Makefile`); the claim is removed and the
runtimes are re-measured on the tree that ships the comment (19.4 s total, `controls.py` 2.2 s, NC4
1.7 s) rather than carried forward.

## Every count this repair prints, and whether it could have come out differently

`verify_e35b.py` section V6 prints this table and scores that it is complete. Three of the eleven are
FORCED and are printed as properties, not offered as evidence:

- **FORCED BY THE CODE PATH** — target byte-identical on 344/344.
- **FORCED BY CONSTRUCTION** — the `≥ 3 facets` zeros for I1/I2/I3.
- **FORCED BY MATHEMATICS** — `facet_swap01` classified GAUGE on 72/72. Scored anyway, as an
  *instrument check* like the three absorbability ones above it, and the row says the answer is known
  in advance and that it fails only if the detector is wrong.

The other eight could each come out otherwise, and the row that scores each says what would move it.

## The disagreements this work produced, recorded rather than smoothed away

1. **The two witness searches disagreed on first run.** `verify_e35b.py` solves the sign system by
   Gaussian elimination over GF(2); `controls.py` solves it by BFS. The first GF(2) version
   back-substituted pivots in **decreasing** order and reported `facet_swap01` as *10 gauge, 62
   unclassified* against the shipped *72*, and disagreed with exhaustive brute force on 3 of 86 small
   pairs. The bug was in this file, not in the shipped one. It is recorded in the source at the line
   that was wrong: a cross-check that has never once disagreed is not evidence that it could.
2. **Putting the new functions in `face_complex.py` cost two instruments.** mg-0b07's p3, re-run at
   HEAD by `d4_auditor_rerun.py`, runs *this* tree's `controls.py` against a **pinned**
   `face_complex.py` from `b6bc2ef`. A new function there that `controls.py` imports makes that mix an
   `ImportError` — 0 bytes, exit 1, both pinned rows MISS, `d4` from 0 BROKEN to 5. They live in
   `controls.py` now, beside `absorbable_bruteforce`, which is where a derived expected value belongs
   anyway. **What that costs is stated in the source:** `d2`'s clause sweep reads its population from
   `face_complex.py` and `posets.py`, so the two clauses of the witness's shape guard are not swept —
   exactly as `posets.py`'s two are not. When they *were* swept, both came back **NOT COVERED**.
3. **`d1_trace.py` caught a name.** It asserts `controls.py` defines no function with `gate` in its
   name. `permute_conju**gate**` broke it. Renamed to `permute_matrix`.

## What this repair changed outside `code/face_geometry/`

Adding two scored rows and three measured lines moves the artifact's extents, and several frozen
audit instruments hold literals about them. **No frozen audit document is edited.** What changed:

- `face_geometry_audit_e7bc/pc_all_pass.txt` and `face_geometry_instr_5f9a/positive_control_all_fail.txt`
  — **derived controls**, regenerated. Each one's own claim says a control describing a previous
  artifact tests nothing about this one.
- `face_geometry_instr_5f9a/d4_auditor_rerun.py` — its expectations for the frozen literals are
  updated and say so: `e3_seams.py` 2 → 4 broken, `g1_positive_control.py` 0 → nonzero (its frozen
  row count 43 against an artifact now carrying 45), and the two live extents 64 → 68 and 42 → 44.
  The frozen audits themselves are untouched: a stale count in a document written to record a tree is
  corrected by saying which tree it recorded.

## State of the runners after this commit

| runner | before | after |
|---|---|---|
| `face_geometry/run_all.sh` | exit 0 | exit 0 |
| `face_geometry_instr_5f9a` d1 / d2 / d3 / d4 | 0 / 1 / 0 / 0 BROKEN | 0 / 1 / 0 / 0 BROKEN |
| `face_geometry_landing_da45`, `_7d5a` verify_landing | exit 0 | exit 0 |
| `face_geometry_audit_6653/run_all.sh` | exit 0 | exit 0 |
| `face_geometry_repair_e35b/verify_e35b.py` | — | 24 checks, 0 refuted, exit 0 |

`d2`'s one BROKEN claim is the pre-existing git-pin staleness documented in its own `run_all.sh`
(*"d2 EXITS 1 AT HEAD AND HAS SINCE bfd7948"*) and is present on the unmodified tree; this commit
neither causes nor fixes it, and adds a tenth commit to the history that claim counts.

## What this ticket deliberately did NOT do

- **Rescope row I4's scored condition.** `absorb == 0` stays in it. The rejections are real on all 297
  pairs and a gauge pair is still one where the corrupted matrix differs from the target; what the
  gauge finding narrows is what a rejection is *evidence for*, and that is carried by the coverage
  line rather than by re-scoring. Extending the `[CANNOT FAIL]` row to all four remains its own item,
  for the reason the file already records.
- **Edit `STATE.md`.** See F5 above.
- **Edit `docs/OneThird-Intrinsic-Face-Geometry-Probe.md`**, whose *"N1 is a control on the homology
  path"* passage mg-2789 flagged and left for pm-onethird. Still flagged, still left.
- **Fix the frozen literals in mg-e7bc's and mg-d0e2's audit instruments.**

## Files

- `verify_e35b.py` — 24 checks over the 86-poset `n ≤ 5` population; re-derives every new number by a
  route that shares no line with the repair, cross-checks the witness search against exhaustive
  search over permutations × sign vectors, checks the forcedness claims in the AST, and prints the
  could-it-have-moved table. Exit 0 iff every check passes.
- `out_verify_e35b.txt` — its committed transcript.
- `run_all.sh` — regenerates the transcript.
