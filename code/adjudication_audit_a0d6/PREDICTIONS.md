# `mg-a0d6` — PREDICTIONS for THE INDEPENDENT AUDIT OF THE `mg-d19f` ADJUDICATION

**Committed before one line of the instrument exists.** The subject is `095260c`, which
adjudicated a contradiction between two landed canonical documents: it declared
`docs/OneThird-L2-Conditionality-mg-28ff.md:21` **TRUE** and struck three sentences in
`docs/OneThird-SweepLoss-mg-51f4.md` as **FALSE**. An adjudication adds no measurement; it
declares a published statement false. If it went the wrong way the arc has corrected a true
document and left a false one standing.

---

## §0. EXPOSURE — WHAT I ALREADY KNEW BEFORE PREDICTING

Stated so that no arm below can be sold as a discovery when it is a reproduction.

* **H1 — I have read `code/sweep_loss_51f4/out_s3_n7.txt`.** I know it prints
  `86278 primitive of 96428` and `route (F) FAILS (f* > 1): 168 of 86278`. **So P1 is a bet
  about whether an INDEPENDENT instrument reproduces a number I already know, not a bet
  about what the number is.** That is still the bet worth making — the landing's own
  adjudication arm (`r1_adjudicate.py`) reads that figure **out of that transcript** and
  therefore inherits it; nothing in the exchange has ever recomputed it. But the discovery
  half is gone and I am not selling it.
* **H2 — I have read `out_r1_adjudicate.txt`, the landing's verdict, in full, before
  writing a probe.** I know which way it went and I know its three joints. My arms are
  therefore *chosen from its claims*: an absence of findings from me is weak evidence,
  because I looked where it pointed. E3 below is the same fact as an error.
* **H3 — I have already `grep`ped the three sample figures at `HEAD` and at `2f76a01`.** I
  know the raw occurrence counts on both sides and I know they are not `5`. So P3 is a bet
  about whether that gap is a **defect** or an **accounting convention**, not a bet about
  the count.
* **H4 — I have read `mg-28ff` at `cb496e9` lines 200/217/245/247/417.** So the three
  joints' textual half is confirmed for me before I predict; what is NOT confirmed is the
  half that matters — whether the underlying measurement makes joint 1 *false of the truth*.

---

## §1. THE PRINCIPAL BETS

| # | p | claim |
|---|---|---|
| **P1** | **0.85** | **The exhaustive `n = 7` re-derivation reproduces `168 of 86278` EXACTLY**, on an instrument that imports neither `lib51f4` nor `lib28ff` and shares no source line with either, and every `f* > 1` verdict it returns is certified in exact rational arithmetic (an exhibited test vector, never a float eigenvalue). **This is the bet the whole audit rests on:** if it misses, the adjudication's ground truth is not what both documents believe. |
| **P2** | 0.90 | **Route (F) fails at ZERO primitive posets for every `n ≤ 6`.** This is the half nobody has stated: it makes `mg-28ff`'s *"100 % at every enumerated `n`"* **true of `n ≤ 6`** and false **only** at `n = 7`, which is exactly what `mg-28ff:21` claims and no more. If (F) also failed at `n = 6`, `mg-28ff:21` would be true for a *bigger* reason than it gives and the repair landed on that document would be an under-correction. |
| **P3** | 0.70 | **The repaired §12 bullet's *"five appearances"* is not recoverable by any uniform machine rule over the document at `HEAD`** — the raw literal count is strictly larger — so the repair carries, in weaker form, the class of defect it repairs: **a count asserted over a population whose membership rule is not stated.** Filed as a finding of DEGREE, not a reversal: the five it names are individually correct and it is the *blanket* that is unstated, which is the same shape as the three sentences it struck. |
| **P4** | 0.60 | **THREE IS THE RIGHT NUMBER.** A mechanical sweep of `mg-51f4` at `2f76a01` for every sentence quantifying over how `mg-28ff`'s `n = 7` figures are labelled or quoted finds **exactly the three sites the landing handled** and no fourth. I hold this at only 0.60 because the landing found two of three by *reading*, and a reader who found two extra may still have stopped one short. |
| **P5** | 0.65 | **NOTHING TRUE WAS STRUCK.** At each of the three sites, every clause inside the strikethrough is false and every clause left standing is true. In particular the replacement *"I do not USE any of them"* is TRUE: none of `0.176145`, `0.850074`, `0.832530` enters §0's, §4's or §6's own tables — each appearance is a QUOTATION of `mg-28ff`'s text. |
| **P6** | 0.80 | **`mg-28ff:21` is TRUE as a whole**, not just in its headline: its embedded numerals `168` and `86278` are the exhaustive figures, its `§4.3 summary` pointer resolves to `cb496e9:247`, and the row it calls a sample is `cb496e9:245`. The landing left it standing and nobody re-checked it. |
| **P7** | 0.75 | **No figure moved.** The multiset of numeric literals in `mg-51f4` at `2f76a01` is a **subset** of the multiset at `HEAD` — nothing was dropped, i.e. the repair withdrew no measurement — and every literal ADDED is either a `mg-28ff`/`mg-3bb9` population figure (`98`, `208`, `40`, `106`, `35`, `101`) or a commit id. |
| **P8** | 0.55 | **The two documents never disagreed about a NUMBER.** Every numeric literal that appears in both, at the states at which they contradicted each other, agrees. The contradiction is entirely in the summaries. (The landing asserts this in prose; it is checkable and was not checked.) |
| **P9** | 0.50 | **The `40–200` clause is wrong in a second way the landing named but did not measure:** `40` is a *primitive count* and `200` is a *draw size*, so the range mixes units — and I predict the machine check confirms **no draw of size 40 and no primitive count of 200 exists anywhere in `mg-28ff`'s instrument at `cb496e9`.** |

---

## §2. WHAT WOULD MAKE ME REVERSE THE LANDING

Named in advance so that a reversal cannot be assembled after the fact:

1. **(F) fails at 0 of 86278 at `n = 7`.** Then `mg-28ff:21` is false, the landing corrected
   the true document, and every strike must be reverted.
2. **(F) also fails at some `n ≤ 6`.** Then `mg-28ff`'s §4.3 sentence is false for a reason
   its own repair does not give, and `mg-28ff:21` is true but **under-stated**.
3. **`cb496e9:247` does not say `enumerated`,** or `cb496e9:245` is not a sample. Then joint
   1 has no textual basis and the adjudication rests on a misquotation.
4. **A struck clause is true.** Then the repair over-reached and the over-reach is a
   withdrawal of a true statement, which is the failure mode this arc exists for.

---

## §3. NINE ERRORS OF MY OWN, FILED BEFORE THEY HAPPEN

* **E1 — I read the definitions of `γ`, `M`, `leak` out of `lib51f4`'s and `lib28ff`'s
  docstrings.** An instrument that shares no *source line* can still share a *mistake* read
  out of prose. The only defence is a cross-check against a genuinely different route, and I
  commit to two: `leak(A)` from linear-extension enumeration versus `⟨1_A,(I−S)1_A⟩` from the
  matrix, and the transport `T` from a down-set DP versus from filtering `n!` permutations at
  `n ≤ 6`.
* **E2 — a float eigenvalue can straddle the boundary.** `f* > 1 ⟺ γ < M²/2`. Any verdict
  decided by a float `γ` is a verdict decided by rounding. Every reported failure must be
  certified by an **exhibited rational vector** `v ⊥ 1` with `⟨v,(I−S)v⟩/⟨v,v⟩ < M²/2`, which
  is an exact upper bound on `γ` and needs no eigensolver at all; every reported
  *non*-failure in the boundary band must be certified by an exact PSD test in the other
  direction. If I report `168` off a float screen alone, the number is mine and not the
  arc's.
* **E3 — I looked where the landing pointed.** My three-sites arm sweeps for the *class* the
  landing named. A defect of a class it did not name is invisible to me for exactly the
  reason `mg-51f4`'s blanket was invisible to `mg-51f4`.
* **E4 — "appearance" is not a machine word.** If I score `five appearances` with a string
  count I will be measuring my own rule, not the document's claim. If P3 fires I must print
  **my rule** beside the disagreement and say that the rule is mine.
* **E5 — agreement with `lib51f4` on the population may be cheap.** Both instruments will
  build naturally-labelled posets by extending down-sets, because the mathematics forces it.
  An agreement between two forced constructions is not two witnesses. The `n ≤ 6` brute-force
  permutation cross-check is what makes it one.
* **E6 — I can "verify" a strike by re-reading the document that made the claim.** The
  struck sentences are claims about `mg-28ff`; every one must be checked against `mg-28ff` at
  the state `mg-51f4` read (`cb496e9`), never against `mg-51f4`'s own description of it.
* **E7 — my no-figure-moved arm will go RED on the repair's own quotations**, exactly as the
  landing's `D4` did, because a document that quotes the sentence it repairs contains the
  defect's text twice. I will not "fix" that by exempting §0.0; I will report the raw count
  and the classified count side by side.
* **E8 — the exhaustive run is long and I will be tempted to sample it.** A sampled
  re-derivation of a number whose whole point is that a *sample* was read as an
  *enumeration* would be this ticket's own defect wearing a stopwatch. If I cannot afford the
  full population I will say `NOT RE-DERIVED` rather than print a sampled `168`.
* **E9 — I am the fourth reader of these two documents and the first three each found
  something the previous missed** (`mg-64cb` found one site, `mg-d19f` found three,
  `mg-3bb9` re-measured the populations). The base rate says I will find a fourth thing. That
  makes me *want* to find one, which is the exact pressure that manufactures findings.

---

## §4. WHAT THIS TICKET WILL NOT DO

* It will **not** edit `mg-28ff`, `mg-51f4`, or `code/contradiction_repair_d19f/`. An audit
  that repairs its subject cannot report what the subject looked like.
* It will **not** re-open either document's mathematics beyond the one number the
  adjudication turns on.
* It will **not** adjudicate `mg-51f4` §11's other five proposed sites; the landing left them
  explicitly unadjudicated and that decision is not this ticket's to reverse.

*`mg-a0d6`, before the instrument.*
