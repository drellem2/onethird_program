# `mg-0d1b` — predictions for THE ALIASED-SCALAR SWEEP

*Committed before one line of the instrument exists. Scored in `README.md` after it runs.*

The ticket's finding is that **one scalar was tracked under two names in two threads, and
neither thread could see the other's number** — `mg-28ff`'s cell `V10` is `ρ·Δ_P`, and
`code/l2_audit_29fe/out_s3_counterfactual.txt` printed the correct `n = 5` onset before
either published onset statement was written. My job is to find the **other** aliased
scalars, compare their **values**, and leave an **index**, not prose.

---

## H — what I already know, disclosed rather than laundered

A prediction made after the measurement is a formality. These are the things I read during
scouting, **before** writing this file, so that nothing below can be scored as a hit that
was really a lookup.

* **H1. THE KNOWN INSTANCE IS ALREADY WIDER THAN THE TICKET SAYS, AND I KNOW IT.** The
  ticket names two names in two threads. I have already seen **four**: `V10`
  (`l2_conditionality_28ff` doc `:279`, recomputed in `l2_audit_29fe/s3_counterfactual.py`
  and again in `l2_underclaim_audit_3bb9/a1_reversal.py`), `rho*Delta` (`lstar_789d`,
  `anticorrelation_c50b/s4_lstar.py`), `v_L` (`audit_5cba/a3,a5,a7`), and the `ρΔ` column of
  `lstar_landing_8d63/s1_onset.py`. I have also seen that
  `l2_underclaim_audit_3bb9/out_a1_reversal.txt` prints `first n at which each variant
  exceeds 1: {'V11': None, 'V10': 5, 'V01': 6, 'V00': 4}` — a **third** instrument printing
  the `n = 5` onset. So "the sweep finds more than two names for ρΔ" is **not a bet** and is
  not predicted below.

* **H2. I HAVE ALREADY SEEN A LIVE VALUE DISAGREEMENT.** `audit_5cba/out_a7_onset.txt` D-B:
  `LSTAR(6)` reads `0.794253` in `mg-789d`'s landing and `0.794235` in `mg-5cba`'s audit,
  and `mg-5cba` settles it on an exact bracket `[0.794234562, 0.794234567]` — the landing's
  figure is a **digit transposition** and is attained at no primitive `n = 6` poset. So
  "the sweep finds at least one disagreement" is **not a bet** either. What *is* a bet is
  whether there is a **second, unadjudicated** one (P3).

* **H3. I HAVE ALREADY RUN A `def`-NAME CENSUS** over all 967 `.py` files under `code/` and
  read the result, so P5's count is a bet about *adjudication*, not about discovery.

* **H4. I HAVE ALREADY SEEN `u_M` AND `c#` PRINTED AS SEPARATE COLUMNS OF ONE TABLE**
  (`anticorrelation_c50b/out_s4_lstar.txt` §S4.2) while `out_s2_theory.txt:31` says
  `(M#) fails <=> u_M > 1` and `sweep_loss_51f4` prices the same route with `c#`. P4 is a
  bet about what the sweep *concludes* about that pair, not about whether both exist.

---

## P — the bets

| # | prediction | p |
|---|---|---|
| **P1** | **The value probe — which is name-blind — finds at least one alias group of ≥ 3 distinct names in ≥ 3 different trees that is NOT ρΔ_P, Δ_P, or γ.** Δ_P and γ are free (I have read their `def`s); the bet is that a *fourth* concept is aliased at that width. | 0.75 |
| **P2** | **Among the core poset scalars, the aliases AGREE.** Every alias group the value probe forms over the common `n ≤ 5` population agrees to `1e-9`, with **zero** new numeric disagreements beyond H2's already-adjudicated `LSTAR(6)`. The hazard this ticket exists for is **silence, not error**. | 0.70 |
| **P3** | **There is no SECOND unadjudicated numeric disagreement.** Scored MISS if the sweep finds a published figure for an aliased scalar that another tree contradicts and that no audit has already settled. | 0.65 |
| **P4** | **`u_M` and `c#` are NOT the same scalar and ARE interchangeable in threshold statements** — i.e. their value vectors differ but `u_M > 1` and `c# > 1` agree pointwise on the probed population. That is a *worse* hazard than a plain alias: two numbers, one predicate, and a reader who quotes the number rather than the predicate carries the wrong one. | 0.60 |
| **P5** | **The value probe reaches fewer than 15 of the 184 trees under `code/`.** Most of the corpus is meta — about transcripts, pins, gates, provenance — and computes no poset scalar at all. A sweep that reported "184 trees searched" without saying how many could be *measured* would be over-claiming. | 0.70 |
| **P6** | **At least one alias group is NOT an independent control, because the two trees share code.** `lstar_landing_8d63` imports `lstar_789d/lib789d.py` by its own admission. So the index must carry a *shares-code* column or it will sell a re-run as a corroboration. | 0.90 |
| **P7** | **The name index finds at least one quantity computed under ≥ 5 distinct symbol names.** γ is my candidate (`gap_exact_bounds`, `gap_at_least`, `gamma_float`, `gamma_bracket`, `gamma_ge`, `bracket_gap`, `gap_float`, `gap_bracket`, `spectral_gap`). | 0.80 |
| **P8** | **The value probe finds at least one pair of names that LOOK like the same quantity and are NOT** — a name-level false positive that only a value comparison can kill. `λ₂` in `chain_iv_*` versus `λ₂` in `hodge_leverage_*` is my candidate. | 0.55 |
| **P9** | **My own index cannot see an alias whose name I did not think of, and the value probe can.** Scored HIT if at least one alias group is formed by the value probe over a name the hand table does not list. This is the arm that makes the instrument more than my own vocabulary. | 0.60 |

---

## E — the ways I expect to be wrong, filed in advance

* **E1. I CALL TWO THINGS ALIASES BECAUSE THEY COINCIDE ON A SMALL POPULATION.** Everything
  cheap enough to sweep exhaustively is `n ≤ 5`, and distinct scalars can agree there. The
  report must say **"agrees on the stated population"** and never **"is"**. Any group I
  promote to *identity* must be backed by a definition read out of the source, not by the
  vector alone.
* **E2. I IMPORT A MODULE THAT RUNS ITS SUITE AT IMPORT.** This already happened in
  scouting: `code/libweak_audit_c4f5/a6_calibration.py` printed 60 lines of another
  ticket's audit into my probe's output. The whitelist is explicit for this reason, and a
  probe that emits another directory's transcript is a defect, not noise.
* **E3. I COUNT A QUOTATION AS A COMPUTATION.** Half this corpus is audits *quoting* other
  trees' figures. An index that lists every document mentioning `ρΔ` as a *site computing*
  `ρΔ` is an inflated index and is worse than none.
* **E4. MY INDEX IS MY OWN VOCABULARY.** The name table is hand-written, so a quantity
  tracked under a name I never thought of is invisible to it — **the ticket's own defect
  wearing a lookup table**. P9 is the arm that is supposed to catch this, and if P9 misses I
  must say so rather than report a clean sweep.
* **E5. I RENAME SOMETHING.** The ticket forbids it in its own words. Guard: `git diff
  --stat` against the merge base must show **0 files outside `code/alias_index_0d1b/`**.
* **E6. FLOAT TOLERANCE MERGES TWO DISTINCT SCALARS.** A tolerance loose enough to absorb
  two libraries' different bracket widths is loose enough to merge two nearby quantities.
  Both the tolerance and the observed max intra-group spread must be printed.
* **E7. I SELL A RE-RUN AS A CORROBORATION.** Two trees agreeing because one imports the
  other's library is not an independent check, and calling it one is exactly the "free
  independent control" claim the ticket asks for, made falsely. See P6.
* **E8. I RE-OPEN THE ONSET QUESTION.** The ticket forbids it: settled at `n = 5`. If my
  probe prints a ρΔ column it is as a **fingerprint for alias detection**, not as a
  re-derivation, and no arm of this instrument may return a verdict on the onset.
* **E9. I REPORT A CLEAN SWEEP WITHOUT NAMING THE POPULATION.** The ticket makes this
  explicit — a null result is useful *only* if it says what was examined. `x1` exists
  solely to make the population a printed number rather than an impression.

---

*mg-0d1b. If a bet below is scored by an arm that could not have failed, it is scored
UNFALSIFIABLE, not HIT — mg-9876's rule, adopted rather than paraphrased.*
