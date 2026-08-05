# mg-fcb2 — independent audit of the mg-e35b control-battery repair

**Target:** the merged mg-e35b repair (`5f542f0`), which landed the remaining OPENs of mg-fcf1's
audit of `NEGATIVE CONTROL 4` in `code/face_geometry/controls.py`, together with its verifier
`code/face_geometry_repair_e35b/verify_e35b.py`.

**Verdict, in one sentence.** *The repair's mathematics is sound and its dichotomy holds under an
instrument that shares no line with it; its own count-completeness claim does not — the line that
lands F3 prints a new tautology whose sentence is false on the nearest population it has never been
run on, and the row that was supposed to catch that scores a hardcoded literal.*

Run it with `sh run_all.sh` (about 6 minutes, pure Python 3, exit 1).

---

## The pre-registration, and why it is the first commit on this branch

`PREDICTIONS.md` was committed at `064c79c` **before a single line of this audit's code existed**.
Every prediction below was scored against that file as written. Nothing in it has been edited, and
two predictions that a defective probe scored OFF are recorded as instrument defects rather than
rewritten (see *Defects of this audit's own instruments*).

The polecat that wrote it was killed by the 2026-08-04 network outage before writing any script.
This run resumed from that commit rather than from `main`, because writing the predictions after
seeing the results would have destroyed the only property the pre-registration exists to establish —
and would have produced an audit indistinguishable from a valid one.

**30 predictions scored. 0 off prediction.** All seven exit codes were predicted before anything ran
and all seven came out as predicted.

| script | predicted | actual |
|---|---|---|
| `selftest_fcb2.py` | 0 | **0** |
| `a1_counts.py` | 1 | **1** |
| `a2_dichotomy.py` | 0 | **0** |
| `a3_standard_elsewhere.py` | 1 | **1** |
| `a4_hedges.py` | 0 | **0** |
| `a5_standing.py` | 0 | **0** |
| `a6_control_at_commit.py` | 0 | **0** |
| `run_all.sh` | 1 | **1** |
| `face_geometry/run_all.sh` | 0 | **0** |

---

## The instruments, and why they are not the repair's

The standing order: *replication is not corroboration when the copies share a source.*
`verify_e35b.py` re-derives the dichotomy by calling `face_complex.not_isospectral` and rebuilding
the witness search over `controls.gauge_candidate_perms`' candidate list — the two things the
section under audit uses. A bug in either is invisible to it by construction.

* **`charpoly_exact`** — the whole characteristic polynomial over **Z**, recovered by CRT under a
  Hadamard coefficient bound. The shipped route evaluates `det(A − k·I) mod (2^31−1)` at five fixed
  shifts; five samples of a polynomial can miss, every coefficient cannot.
* **`signed_perm_witness`** — a backtracking search over **all of S_m**, pruned by a
  Weisfeiler-Leman colouring and closed by a parity union-find over the signs. It takes no candidate
  list, so its NOT-GAUGE answers are not bounded the way the shipped detector's are. An exhausted
  search returns the sentinel `"BUDGET"` and never `None`, so "searched and found nothing" can never
  be read as "no witness exists".

Both are checked in `selftest_fcb2.py` against exhaustive brute force — a Leibniz cofactor expansion
for the polynomial, all `m!` permutations × `2^m` sign vectors for the witness — plus positive and
negative controls on each, before either is pointed at the tree under audit. 8 rows, exit 0.

---

## Findings

### F1 — the line that lands F3 prints a new tautology, and its sentence is FALSE (A1.1)

`controls.py:1927` supplies `(N, N)` for *"The named load-bearing site is corrupted on %d/%d
posets"* — **numerator and denominator are the same expression**, established from the AST and not
from the output. It prints `86/86`. Two constructed inputs:

* **`le_to_facet_offbyone := le_to_facet`**, so the named site is corrupted on **no poset at all**.
  True count 0/86. The line still prints **86/86**.
* **the population widened to admit n = 1** — the section builds `range(2, nmax + 1)`, so the
  one-element poset is the nearest legal input it has never been run on. Both facet maps return the
  empty chain there, so the site is not corrupted. The line prints **87/87**; the truth is **86 of
  87**; and row I4 stays **`[PASS]`**.

This is the F3 defect reproduced in the very sentence that lands F3, with the aggravating feature the
`344/344` case did not have: that count is a theorem at every n, this one is a **false statement**
one poset outside the population.

### F2 — V6's completeness row scores a literal, not completeness (A1.2)

`verify_e35b.py:402` scores `forced == 3 and len(table) == 11` where `table` is a list of string
literals defined twenty lines above it. Its only free names are `forced` and `table`; nothing in it
opens `controls_output.txt`. Demonstrated rather than argued: a **twelfth printed count added to the
artifact**, with the verifier untouched, leaves the row **green**. It cannot fail on an omission,
which is why F1 survived a table headed *"EVERY COUNT THIS REPAIR PRINTS"* — the 86/86 is absent from
it, and the `61/86` from the same sentence is present.

### F3 — a count labelled `COULD MOVE` that cannot move at any n (A1.3, A1.4)

V6 labels *"no ridge in >= 3 facets, I4 zero"* `COULD MOVE`, and the artifact says *"I4 rebuilds the
facet enumeration outright, so a ridge there CAN lie in >= 3 facets; its zero is the only one of the
four that is a result"*. **It is not a result.** Both facet maps return a chain of masks of sizes
`1, 2, …, n−1`, so deleting the level-`i` mask leaves exactly two candidates to re-insert — at most
two facets share any ridge, at every n, for either map. Checked over every poset with n ≤ 6 under
both maps (810 families): the largest number of facets sharing a ridge is **2**. It is forced by the
same counting as the other three, not a fourth measurement.

### F4 — V6's stated reason for one row does not move that row (A1.3b)

V6's `why` for *"detector says NOT-GAUGE on 288 of 297"* is *"a detector that accepted everything
would print 297 here"*. Substituted — and the substitution is shown to have been **reached**, 297
calls — it still prints **288**. The binning is `if not_isospectral: … elif witness: …`, so the 288
spectrally separated pairs never reach the detector at all. The count does move (the population
moves it), but the reason printed for it is false.

### F5 — the rejection standard, asked of the rows the repair keeps OUTSIDE its own section (A3)

This is what the ticket asks for and what the repair did not do. mg-e35b turned its one sentence — *a
relabelling of the facet set is a signed-permutation conjugation, hence isospectral* — on the four
rows of `NEGATIVE CONTROL 4`. **It did not turn it anywhere else.** Asked of the battery's other
scored corruption rows, with this audit's own detector:

| row | bites on | GAUGE | verdict |
|---|---|---|---|
| M1 no sign twist | 82 | **82 (100%)** | disqualified |
| M2 absolute Laplacian | 82 | 0 | clears |
| M3 wrong twist | 72 | **72 (100%)** | disqualified |
| M4 target scaled by 2 | 82 | 0 | clears |
| M5 one edge deleted | 82 | 0 | clears |
| NC3 facet-parity signs | 82 | **82 (100%)** | disqualified, **and its row says so** |

**The standard disqualifies two rows nobody has asked — M1 and M3 — and their printed text says
nothing about it.** Both are pure diagonal sign conjugations, i.e. exactly the gauge `facet_swap01`
was rejected for being; `NEGATIVE CONTROL 3`'s parity row is the third and is the only one of the
three that discloses it in its own text.

The standard is **not** a rubber stamp: it rejects M2, M4 and M5 on a spectral proof each time, so
the three it disqualifies are a decision about those rows and not a property of the detector.

### F6 — a second tautology site, unpredicted, outside the target (A6.5)

The new control swept repo-wide (522 Python files, 275 `X/Y` sites) flags **two**. The second is
`code/face_geometry_audit_fcf1/audit_nc4.py:41` — **mg-fcf1's own instrument**, the audit whose F3
finding was *"two printed measurements were tautologies"*, printing `holds on %d/%d` with `N` twice.
It cannot come out otherwise for a stronger reason than the one it found: the loop above it
`assert`s the equality on every poset, so a failure crashes the script rather than lowering the
count. **Not scored as a defect of mg-e35b** — different file, different item — and reported because
a control that hides its own second finding is worth nothing.

---

## What was confirmed, and is not a finding

* **The dichotomy is right.** `297 = 288 + 9 + 0`, per row I1 66/6, I2 82/0, I3 82/0, I4 58/3,
  swap01 0/72 — **reproduced exactly** by exact charpolys and a search over all of S_m (A2.1).
* **No pair is both spectrally separated and a gauge** (A2.2). The shipped `elif` cannot see such a
  pair and has no row for it; both questions were asked of all 369 pairs and there are none. This
  check does not exist anywhere in the repair.
* **All nine gauge witnesses reconstruct entry by entry** under this audit's own reconstruction, and
  the three of row I4 are the antichains at |L(P)| = 6, 24 and 120 (A2.3).
* **The candidate-list bound is discharged at every size** (A2.4). Brute force over `m!` × `2^m`
  agrees with the shipped classification on all 155 pairs with |L(P)| ≤ 6, and an unbounded search
  agrees on all 214 above it. No NOT-GAUGE answer in that row rests on the bound.
* **Exact integer charpolys agree with the five-shift modular verdict on all 369 pairs** (A2.5).
* **Every hedge the repair writes is accurate** (A4). The 288 not-gauge answers are all settled by a
  spectral proof, 0 by the bound. The two shape-guard clauses disclosed as `NOT COVERED` really are:
  deleting either, or both, leaves `controls_output.txt` **byte-identical**. The 25-poset vacuity
  remainder decomposes exactly as `24 + 1`. The withdrawn hedge is gone as an assertion and survives
  only inside the sentence that withdraws it.
* **Nothing that stands was disturbed** (A5). `L_parity = D·L_true·D` on 86/86; absorbability against
  brute force on 306/306; `facet_swap01` bites 72/86, absorbable 0/72, spectrum moves 0/72, GAUGE
  72/72; NC3 stays green under all four corruptions (bite counts 82/82/72/79 against 82 uncorrupted),
  so it could not have caught any of them; `face_geometry/run_all.sh` exits 0 and regenerates its
  artifacts byte-identically.
* **Row I4's surviving scored clause is forced — and the repair says so** (A3.3). On the three posets
  where its diagonal survives, 12/48/240 off-diagonal magnitudes differ and **nothing differs in sign
  alone**, so `|s_i s_j| = 1` rejects before a sign is read. That is the ticket's *"a repair that
  relabels three and leaves a fourth unexamined has reproduced the defect at the surviving row"* —
  and it is **not** reproduced: the artifact states it, and records that removing the clause is a
  scoring change deferred to its own item.

---

## What this audit chose that the ticket's list does not name

**The gauge standard applied outside `negative_control_incidence`** (A3, and finding F5). The ticket
says to apply the repair's rejection standard to the rows *it* keeps. The repair keeps a whole
battery, and `NEGATIVE CONTROL 2`'s M1–M5 and `NEGATIVE CONTROL 3`'s parity row are scored rejections
in the same file under the same acceptance bar, which nobody has ever asked the gauge question. This
was named in `PREDICTIONS.md` before any of it was run.

Three further things nobody asked for: the **both-buckets check** (A2.2), the **multi-ridge counting
argument** (F3), and the **repo-wide sweep** that produced F6.

## The new control

`a6_control_at_commit.py` carries a **structural-tautology scanner**: parse a source, pair every
`%d/%d` in a format string with the two argument expressions that fill it, and flag the sites where
the two are the same expression. It is a **source** check, not an output check — plenty of honest
ratios are `k/k` on a given population (`facet_swap01` is GAUGE on 72/72 and that row can go red);
what separates a measurement from a tautology is whether the two halves *can* differ, which is a
property of the code path.

Demonstrated at three trees, the first of which is a commit where the defect is still present:

| tree | sites examined | flagged | |
|---|---|---|---|
| HEAD (the merged repair) | 34 | **1** | the coverage line's `(N, N)` |
| `5f542f0^` (before the repair) | 28 | 0 | the line does not exist there |
| HEAD with the count measured | 34 | 0 | silent once repaired |

The patch is **run**, not just scanned: the repaired figure prints `86/86` on the shipped population
and `86/87` on the widened one, where HEAD's prints `86/86` and `87/87`. So the remedy produces a
count that is evidence.

---

## Defects of this audit's own instruments

Recorded rather than quietly corrected, because an instrument defect that changes a verdict is a
result. **Both were found and fixed before the run that ships, and both had scored a prediction OFF
that is in fact ON.**

1. **The AST probe matched the wrong site.** It took the *first* `%`-BinOp it walked past inside
   `negative_control_incidence`, which is the instrument check's `(yes, N)` and not the coverage
   line, and reported the two arguments as different expressions — scoring **P1b** off prediction
   when P1b is correct. The probe now identifies the site by the sentence it prints and asserts if
   that sentence is not found. This is the same shape as mg-c067's figure-grammar defect: a probe
   that locates its target by position rather than by content.
2. **The free-name probe counted a builtin.** It scored `len` as a name V6's condition reads,
   so the condition's operands did not look like "the literal beside it" — scoring **P2a** off
   prediction when P2a is correct. Builtins are now excluded.

A third thing worth recording, though it is a limitation rather than a defect: `signed_perm_witness`
tries the identity permutation as a shortcut before the general search. Nothing rests on it — every
witness it returns is reconstructed and compared entry by entry — but it means the search order is
not uniform across pairs.

## OPEN

1. **The 86/86 is not repaired here.** This is an audit; it constructs the input that moves the
   count and demonstrates a patch that fixes it, but does not land the patch. The one-line repair is
   in `a6_control_at_commit.py:patched_source`.
2. **M1 and M3 have no gauge disclosure.** F5 establishes that the standard disqualifies them; adding
   the sentence to their rows is a change to `NEGATIVE CONTROL 2` and belongs to its own item.
3. **`audit_nc4.py:41`** (F6) is in mg-fcf1's tree and is left alone deliberately.
4. **The population still starts at n = 2.** Whether admitting n = 1 is the right fix for F1, or
   whether the count should simply be measured over the population it has, is a decision about the
   battery's scope and not one this audit should make.
5. **The scanner is not wired into any runner.** It flags one site in the tree it audits and one
   outside it; making it a scored row somewhere is a change to a battery, not to an audit.
