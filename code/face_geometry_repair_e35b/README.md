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

> **CORRECTED by mg-8af0 (mg-fcb2's F3), 2026-08-05.** ~~*and by I4's zero being the one
> measurement of the four*~~ — **that sentence is false and so is the "three of the four" above
> it.** All four zeros are forced, and so are `facet_swap01`'s and the uncorrupted build's. The
> forcing is a property of the **facet family**, not of the mutation: both maps are prefix
> families, so every facet is a chain of masks of sizes 1..n−1, a ridge is that chain with one
> level deleted, and re-inserting a mask of the missing size admits **exactly two** candidates.
> Checked over five modes and every poset 2 ≤ n ≤ 6 — 2424 builds, 76554 facets, maximum ridge
> multiplicity **2** — in `code/face_geometry_repair_8af0/probe_f3_ridge_multiplicity.py`. The
> n = 2 case needs a separate argument (|L(P)| ≤ 2) and is counted separately there. **What this
> ticket got right and mg-8af0 keeps: the target's byte-identity on 344/344 is forced, and the
> AST check of it stands.** See `code/face_geometry_repair_8af0/README.md`.

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

> **The last row is the state at mg-e35b and stays as written.** It has moved twice since: to 28
> checks at mg-8af0, and to **29 checks, 0 refuted, exit 0** at mg-843d — which is also the first
> commit at which anything other than a hand invocation runs it. In between, from `de86fee` to
> mg-843d, it was **28 checks, 1 REFUTED, exit 1**. See "The census question, answered" below.

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

---

# The census question, answered — and the suite is now gated (mg-843d, 2026-08-13)

**V6b fired on a real input on 2026-08-10 and nothing in the estate ran it.** `verify_e35b.py`
exited 1 on `main` from `de86fee` until today: **28 checks, 1 REFUTED — V6b CENSUS, measured 210
specifiers against a declared 184.** `de86fee~1` measures 184; `de86fee` (mg-17aa) rewrote
`negative_control_incidence` and did not re-declare the census. mg-8af0's README recorded the
finding on 2026-08-13 and deliberately did not repair it, because *re-declaring 184 → 210 is the
one edit that silences a live disagreement without answering it*. This is the answer, and then
the re-declaration.

## The question, stated so it can come out either way

**Do the 26 values `de86fee` added belong in the census at all?** If they do, the declaration was
stale and moves. If they do not, the values are the defect and the declaration was right. Those
are opposite outcomes with the same symptom, and the number matching is not evidence for either.

`census()` states its own population and the population is **lexical**: the `%`-format
expressions with a string-literal left operand inside `negative_control_incidence`, at a grain of
one conversion specifier. So the question has a decidable form — are `de86fee`'s new expressions
that? — and it is answered at the **site** level rather than by comparing two totals:

| | sites | specifiers |
|---|---|---|
| declared, at `de86fee~1` | 34 | **184** |
| sites **removed** by mg-17aa | −5 | −28 (1 + 9 + 1 + 9 + 8) |
| sites **added** by mg-17aa | +11 | +54 (4+16+2+1+11+5+2+8+1+2+2) |
| measured, at `de86fee` and at HEAD | **40** | **210** |

**Every one of the sixteen is mg-17aa's row rewrite**, and it is legible as such. What left: the
mg-8a12 routing row (*"the MOVED-DIAGONAL split SEPARATES on this population"*), its
`DIAGONAL_MOVES` clause, and the two absorbability sentences that row carried. What arrived: the
`[CANNOT FAIL]` row over all four I-rows, the falsifiability check that replaced the routing row,
and the per-row planted-worlds lines it prints. That is the content `de86fee`'s commit message
describes, appearing where it says it appears.

**Verdict: they belong. The declaration was stale and it moves to 210** —
`d` 150 → 162, `s` 48 from 34, the four channel bounds unchanged at 0/0/0/1. The values are not
the defect; *not re-declaring* was. The derivation above is in the source at the declaration, not
only here, because the next person to see this row fire will be reading the source.

## What moving the number did not settle, and the row that now settles it

The 26 are **not** 26 new printed values. Measured by running the section rather than reading it:

| fate | at `de86fee~1` | at HEAD | what it is |
|---|---|---|---|
| **printed** — the site's string is in `controls_output.txt` | 183 | **194** | the census's own headline claim |
| **unreached** — the site never evaluates | 0 | **14** | one conditional-expression branch mg-17aa keeps on purpose: *"THIS BRANCH IS REACHED ONLY BY A MUTATION SET WITH A PAIR THAT CLEARS BOTH FORCED GATES"* |
| **discarded** — evaluated, thrown away | 1 | **2** | a `dict.get` default, which Python evaluates before it knows it is not needed |

So of the 26, **11 are new printed values and 15 are not.** Nothing about that is wrong — a
branch kept so the routing can put a clause back with no edit is a branch that should not fire
today, and the census counts it rather than exempting it for the same reason it counts the one
`i % 3`. But the census's docstring headline — *"every formatted value NEGATIVE CONTROL 4
prints"* — was over by 1 the day it was written and is over by 16 now, and **that gap is what
made this question expensive**: answering it took a bespoke probe, which is why the estate sat
red for three days rather than five minutes.

`verify_e35b.py` therefore gains **V6d REACH**: V6b's population, V6b's grain, split by fate,
with the three summing to V6b's own declared total (scored, not assumed) and the probed run
required byte-identical to the committed artifact (also scored — an instrument that perturbs
what it measures would be reporting on a document that does not exist).

**V6d is watched firing**, in `demo_v6d_row_can_go_red.py`, over four structural mutations of a
throwaway copy of `code/face_geometry/`:

| construction | V6b | V6c | V6d |
|---|---|---|---|
| D0 the copy, unmutated | GREEN | GREEN | GREEN |
| **D1 a printed value moved into an unreachable branch, artifact regenerated** | GREEN | GREEN | **RED** |
| D2 a new `%d` in a branch nobody runs | RED | GREEN | RED |
| D3 a new `%d` in what the run prints, artifact regenerated | RED | GREEN | RED |
| D4 the artifact hand-edited | GREEN | RED | RED |

**D1 is the answer to "is this row redundant?"** — a value stops being printed and the record is
regenerated to agree. V6b is lexical and cannot see it; V6c compares a fresh run to the committed
file and both moved together; V6a covers only the twelve counts in `TABLE`. **D2 and D3 are why
the split is printed**: both move V6b by exactly one specifier and they are opposite events, and
V6b reports the same number for both.

**The demonstration found a defect in the row it demonstrates, and it is kept.** `census_reach`
first keyed its probe records on **line numbers**, and `ast.unparse` puts two `%`-sites on one
line — so D0, the unmutated copy, came out **RED**. A row that mis-scores a copy of the tree it
was written against would have shipped if the demonstration had been an argument. It is keyed on
a site index now.

## The remedy is an artifact of the same kind as the defect, and here is where it is exposed

The defect was **a declared number that a real measurement contradicted, whose cheapest repair
was to move the number.** V6d is three more declared numbers of exactly that kind, and a future
legitimate edit to `controls.py` will contradict them too. **That exposure is real and it is not
closed here** — it is the shape mg-479c names as an unfalsifiable escape hatch, and nothing in
the machinery distinguishes an operator who moves `printed: 194` because they looked from one who
moves it because it was red.

Three things narrow it, and none of them eliminates it:

1. **The split is scored to sum to V6b's own total.** A specifier cannot be moved out of both
   rows at once, so the two declarations cannot drift into disagreeing about one population.
2. **The probed run is scored byte-identical to the committed artifact.** An instrument that
   perturbs what it measures would report a split of a document that does not exist.
3. **The answer is now cheap.** The reason this sat red for three days is not only that nothing
   ran it — it is that answering it needed a bespoke probe. V6d *is* that probe, run every time.
   The next firing arrives with `unreached +N` or `printed +N` already printed beside it, which
   is the sentence a re-declaration has to justify.

**What is NOT claimed:** that V6d catches every way a value can stop being printed. It is one
number per fate, so two changes that cancel are invisible to it — the same limit V6b carries and
states in its own row name. The demonstration prints that limit as a NOT-SHOWN line rather than
leaving it to be discovered.

## Should this suite be in `build.sh`? Yes, and here is the test that says so

`build.sh` gated six suites when this ticket opened and this was not among them, which is why a
control could fire
correctly for three days into an empty room — **every merge in that window gated green with a red
tripwire in the same tree**, including `7025d03` at 45 s. It is the **seventh suite in the loop**
now — mg-f771 landed an eighth mid-rebase which runs after the loop and outside it. Not every
script under `code/**` should be: most are one-off audits that measured a tree, published a
transcript and finished, and re-running those on every merge gates on history.

**The test is what a suite's rows read, not what its directory is called.** All four of V6a, V6b,
V6c and V6d are scored against `code/face_geometry/controls.py` and `controls_output.txt` —
files *other tickets keep editing*, and `de86fee` is the proof that they do. A row whose input is
a live file is a standing control; a row whose input is its own literal is mg-fcb2's F2, and this
suite had exactly that row and had it removed.

**Ordering, because it mattered.** A red suite added to the gate blocks every merge in the
repository. The census is answered and the suite green *before* the `build.sh` edit, in this one
commit.

**Cost, measured on this host and not added up:** the whole gate is **88.4 / 87.1 / 85.2 s** over
three runs with the suite in, against **44.8 s** measured minutes earlier without it. It nearly
doubles the gate — the 3 s spread across the three is load, not the gate. 42.3 s of
that is this suite's runner — 7.2 s verifier, 35.0 s demonstration — and `build.sh` names the
demonstration as the removable half so that dropping it later is a decision with a number
attached, which is more than this suite's absence from the gate ever had.

**And it lands under `mg-f771`'s invariant from its first gate run, which is the right way
round.** That suite — merged onto main while this branch was in the queue — makes a committed
`out_*.txt` that disagrees with what the gate just produced a RED. This suite writes two of them,
`out_verify_e35b.txt` and `out_demo_v6d.txt`, and neither embeds a wall-clock or a worktree path,
so neither leans on `mg-f771`'s two normalisation rules: they converge by being deterministic
rather than by being exempted, checked by running the whole gate after the rebase. That matters
more than usual here — this ticket exists because of a transcript that sat on main disagreeing
with its tree, and a suite added to stop that arriving *outside* the control that stops it would
have been the joke version.

## What mg-843d deliberately did NOT do

- **Re-declare 184 → 210 on its own.** That was the forbidden repair and it is the one this
  ticket exists to avoid: it makes the symptom go away without deciding which of two opposite
  things happened.
- **Edit `de86fee`'s values, or `controls.py` at all.** The 26 are legitimate content. The census
  was the stale side and the census is the side that moved.
- **Re-audit mg-17aa.** Whether the `[CANNOT FAIL]` extension is sound is **mg-79ba**, a
  different question about the same parent. Nothing here touches it.
- **Regenerate `out_demo_f2.txt`.** It did not need it: with V6b green again the demonstration
  reproduces its committed transcript **byte for byte**, 20/20 cells. It was never stale in
  content — it was a correct record that the tree had drifted away from and drifted back to.
- **Widen the census's population.** The channel bounds (`fstrings`, `format_calls`,
  `str_calls`, `nonliteral_mod`) are untouched at 0/0/0/1.
- **Gate anything else, or repair anything else that is red.** Two are noted and left, because
  they are neither this ticket's subject nor caused by it:
  - `code/face_geometry_rows_17aa/run_all.sh` **exits 1 on main and cannot do otherwise.** Its
    containment arm diffs the worktree against `744cfd5`, mg-17aa's own branch base, and
    everything that has landed since is off its allowlist — 356 paths today, from tickets that
    have nothing to do with it. It is green only on the branch that wrote it. Its transcript was
    regenerated in the course of checking that and **reverted uncommitted**; a branch-relative
    containment check is not a standing control and must not join the gate as one.
  - The `d2` BROKEN claim in `face_geometry_instr_5f9a`, pre-existing since `bfd7948` and
    documented in its own runner. Untouched, as at mg-e35b and mg-8af0.

## Files

- `verify_e35b.py` — **29 checks** over the 86-poset `n ≤ 5` population (24 at mg-e35b, 28 after
  mg-8af0, 29 after mg-843d); re-derives every new number by a route that shares no line with the
  repair, cross-checks the witness search against exhaustive search over permutations × sign
  vectors, checks the forcedness claims in the AST, and prints the could-it-have-moved table.
  Exit 0 iff every check passes.
- `out_verify_e35b.txt` — its committed transcript.
- `demo_v6d_row_can_go_red.py` — V6d watched going red on four mutations (mg-843d).
- `out_demo_v6d.txt` — its committed transcript.
- `run_all.sh` — regenerates both transcripts; the worst exit wins. **It is `build.sh`'s seventh
  looped suite, so it is no longer hand-invoked** — and both transcripts are therefore under
  mg-f771's fixed-point control, which is checked below.
