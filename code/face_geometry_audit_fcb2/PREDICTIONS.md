# mg-fcb2 — predictions, committed BEFORE any script of this audit exists

**Target:** the MERGED mg-e35b repair (`5f542f0`), which landed the remaining OPENs of mg-fcf1's
audit of NEGATIVE CONTROL 4. This is an independent audit; it does not re-do the repair.

Everything below was written after reading `controls.py`, `verify_e35b.py`, `out_verify_e35b.txt`,
`controls_output.txt` and the commit message, and **before a single line of this audit's own code was
written**. Nothing here is edited afterwards. Misses are kept as written and listed in the README.

## What I chose to audit that the ticket's list does not name

**The gauge standard applied OUTSIDE `negative_control_incidence`.** The ticket says to apply the
repair's rejection standard to the rows *it* keeps. The repair keeps a whole battery. `NEGATIVE
CONTROL 2`'s M1–M5 and `NEGATIVE CONTROL 3`'s parity row are scored rejections in the same file,
under the same acceptance bar mg-2789 was held to ("show your corruption is NOT absorbable into a
parameter the battery already varies"), and no one has ever asked them the gauge question. I ask it,
with my own detector, and report the count it disqualifies.

## The claims this audit will test, and the answer predicted for each

### P1 — the coverage line prints a count that CANNOT come out otherwise

`controls.py:1944` supplies `(N, N)` for *"The named load-bearing site is corrupted on %d/%d
posets"*. Numerator and denominator are the **same expression**.

- **P1a** — the printed figure is `86/86` at HEAD. **Predicted: confirmed.**
- **P1b** — it is a tautology of the code path in exactly the F3 sense this repair was landing: no
  input moves it. **Predicted: confirmed.**
- **P1c** — and unlike the `344/344` target case, the underlying property is **not** a theorem at
  every n. On a population that includes n = 1, `le_to_facet` and `le_to_facet_offbyone` agree (both
  return the empty chain), so the mutation does not apply there. **Predicted:** with n = 1 admitted
  the truth is **86 of 87** while the print still reads **87/87**. This is a count that cannot move
  *and* whose sentence can be false.
- **P1d** — it is **absent from `verify_e35b.py`'s V6 table**, whose header is *"EVERY COUNT THIS
  REPAIR PRINTS"*. **Predicted: confirmed** — the table's 11 rows contain the `61/86` coverage figure
  and not the `86/86` one.

### P2 — V6's completeness row scores a literal, not completeness

`verify_e35b.py:400` scores `forced == 3 and len(table) == 11` over a **hardcoded list**. The README
says *"V6 prints this table and scores that it is complete."*

- **P2a** — the condition reads only the literal it is written beside and never touches the artifact.
  **Predicted: confirmed.**
- **P2b** — therefore it cannot fail on an omission, which is why P1d survived it. **Predicted:
  confirmed** — I will demonstrate by adding a twelfth printed count to the *artifact* and showing
  the row stays green.

### P3 — the dichotomy, re-derived by an instrument that shares no line with either existing one

`verify_e35b.py` already re-derives it once; **replication is not corroboration when the copies share
a source**, so this audit's witness search is written from the definition again, and the spectral
half is done with **exact integer characteristic polynomials** rather than `not_isospectral`'s five
modular shifts.

- **P3a** — `297 = 288 + 9 + 0`, per row I1 `66/6`, I2 `82/0`, I3 `82/0`, I4 `58/3`, swap01 `0/72`.
  **Predicted: reproduced exactly.**
- **P3b** — **no pair is BOTH spectrally separated and gauge.** The shipped code bins with
  `if not_isospectral: … elif witness: … else: unclassified`, so a pair that is both would be
  silently filed as NON-SIMILAR and one of the two instruments would be wrong with no row to catch
  it. This check does not exist anywhere in the repair. **Predicted: 0 contradictions.**
- **P3c** — every one of the 9 GAUGE witnesses reconstructs to the corrupted matrix entry by entry
  under my own reconstruction. **Predicted: 9/9.**
- **P3d** — exhaustive search over all `m!` permutations × all `2^m` sign vectors agrees with the
  shipped classification on every biting pair with `|L(P)| <= 6`. **Predicted: full agreement.**
- **P3e** — exact integer char-polys agree with `not_isospectral`'s modular verdict on all 297.
  **Predicted: full agreement** (`not_isospectral` is one-sided, so a disagreement can only be
  "exact says non-isospectral, modular said no" — I predict that set is empty here).

### P4 — the gauge standard asked of the rows kept OUTSIDE NEGATIVE CONTROL 4

Question asked of each scored corruption row in the battery: *on the posets where it bites, is the
corrupted matrix a signed-permutation conjugate of the true one?*

- **P4a** — `M1 no sign twist`: **predicted 100% GAUGE** (the twist *is* a diagonal sign
  conjugation, so `L_M1 = D·L_true·D` with π = id).
- **P4b** — `M3 wrong twist`: **predicted 100% GAUGE** (same, with `D' D`).
- **P4c** — `M2 absolute Laplacian`: **predicted 0% GAUGE.**
- **P4d** — `M4 target scaled by 2`: **predicted 0% GAUGE** (trace doubles).
- **P4e** — `M5 one edge deleted`: **predicted 0% GAUGE.**
- **P4f** — NC3 `facet-parity signs`: **predicted 100% GAUGE** — and **already disclosed** in that
  row's own text (*"the corruption is the diagonal conjugation L → D·L·D … it covers ONE SIGN GAUGE"*),
  so it is a confirmation and not a finding.
- **P4g** — so the standard disqualifies **two rows nobody has asked** (M1, M3), and their text says
  nothing about it. **Predicted: confirmed.**

### P5 — the hedges, enumerated

- **P5a** — *"a NOT-GAUGE answer is bounded by the candidate list"*, and the row claims *"here every
  not-gauge pair is settled by the spectral proof instead, so no answer in this row rests on the
  bound."* **Predicted: true — 0 of the 288 not-gauge answers rest on the bound.**
- **P5b** — the two clauses of `signed_permutation_witness`'s shape guard are disclosed as **NOT
  COVERED**. I run the deletion test myself. **Predicted: both deletions leave `controls_output.txt`
  byte-identical**, i.e. the disclosure is accurate and complete.
- **P5c** — the I4 vacuity remainder: 25 blind, 24 with a different facet SET ⇒ **exactly 1 poset on
  which the mutation applied, preserved the facet multiset, and left `L^rel` fixed** — a
  relabelling-shaped blindness that no line names. **Predicted: exactly 1, and `|L(P)| <= 2` on it.**
- **P5d** — `"no claim is made either way"` no longer appears as an assertion. **Predicted:
  confirmed.**

### P6 — do not disturb what stands (a regression here outranks every finding above)

Re-derived from scratch, not read from the transcript:

- **P6a** — `L_parity = D·L_true·D` on **86/86**. **Predicted: confirmed.**
- **P6b** — the absorbability predicate vs. my own brute force over all `2^m` sign vectors on
  **306/306** (poset, mutation) pairs with `|L(P)| <= 8`. **Predicted: confirmed.**
- **P6c** — `facet_swap01` bites on **72/86**, absorbable on **0/72**, spectrum provably moves on
  **0/72**, GAUGE on **72/72**. **Predicted: confirmed.**
- **P6d** — NC3 could not have caught any of the four: with each of I1–I4 in place, NC3 line 2 is
  SILENT on 86/86 and NC3 line 3's scored condition `n_rej == n_app` still holds (bite counts
  82/82/72/79 vs 82 uncorrupted). **Predicted: confirmed — all four NC3 rows stay green.**
- **P6e** — `face_geometry/run_all.sh` still exits **0** on this worktree. **Predicted: confirmed.**

### P7 — the new control, demonstrated where the defect is still present

The new control is a **structural-tautology scanner**: parse `controls.py`, find every `%d/%d` in a
printed/scored format string inside `negative_control_incidence`, pair it with its two argument
expressions, and flag the ones where the two are the same expression.

- **P7a** — at HEAD (`5f542f0`, the merged repair) it **fires**, on exactly one site: the coverage
  line's `(N, N)`. **Predicted: 1 finding.**
- **P7b** — at `5f542f0^` (the commit before the repair) the coverage line does not exist, so it is
  **silent**. **Predicted: 0 findings** — which shows the defect is *introduced* by this repair and
  the control is not a pre-existing complaint.
- **P7c** — against a patched copy where `(N, N)` is replaced by a measured count, it is **silent**.
  **Predicted: 0 findings.**

## Exit codes, predicted before anything is run

| script | predicted exit | why |
|---|---|---|
| `selftest_fcb2.py` | **0** | this audit's own instruments against answers known in advance |
| `a1_counts.py` | **1** | P1 and P2 are refutations of claims the repair makes |
| `a2_dichotomy.py` | **0** | P3 predicts the repair's dichotomy is right |
| `a3_standard_elsewhere.py` | **1** | P4g refutes "the standard has been asked of the rows kept" battery-wide |
| `a4_hedges.py` | **0** | P5 predicts every hedge's disclosure is accurate |
| `a5_standing.py` | **0** | P6 predicts no regression |
| `a6_control_at_commit.py` | **0** | P7 predicts the control behaves as specified at all three trees |
| `run_all.sh` | **1** | it propagates the worst of the above |
| `face_geometry/run_all.sh` | **0** | unmodified by this audit |

## The verdict this audit expects to reach, stated in advance so a miss is visible

**The repair's mathematics is sound and its dichotomy holds** (P3, P6). **Its own count-completeness
claim does not** (P1, P2): the repair landed "a count that could not have come out otherwise is not
evidence", printed a new tautological count in the very line that lands F5, and wrote the row that
was supposed to catch it as a self-check on a hardcoded list. If P1–P2 come out as predicted this is
**the F3 defect reproduced at the surviving line** — the exact shape the ticket says to look for.
