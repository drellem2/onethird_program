# mg-29fe — predictions for the INDEPENDENT AUDIT of mg-28ff

Committed **before** `docs/OneThird-L2-Conditionality-mg-28ff.md` is opened and before one
line of `code/l2_conditionality_28ff/` is read. Written from the dispatch body and from the
parent's commit subjects only.

---

## H — exposure, disclosed rather than laundered

**H1 (VERY LARGE).** My spawn prompt printed mg-28ff's **entire essay-length commit subject**,
including:

- the theorem statement `Phi*_pref^2 <= R(g)(2 Delta_P - R(g))`, `Delta_P = max_i(1-(S_P)_ii)`;
- the two added steps (`d_i <= Delta_P` kept where the parent wrote 1; evaluating the
  Cauchy–Schwarz factor `sum a_ij(h_i+h_j)^2 = 2 sum d_i h_i^2 - E(h)` rather than discarding
  `-E(h)`), **and** the counterfactual "with the un-sharpened `2 Delta_P R(g)` form the constant
  already EXCEEDS 1 at n=5 (6 of 275 primitive)";
- both route constant sequences verbatim — cone `0.125, 0.500, 0.637, 0.803, 0.943`, footrule
  `0.125, 0.250, 0.306, 0.551, 0.812`;
- `c_true` verbatim — `0.125, 0.222, 0.271, 0.308, 0.328`, deltas `.097, .049, .037, .019`;
- the identity `sum_k leak(A_k) = (1/2) E[Spearman footrule]` and the bound
  `Phi*_pref <= E[D_F]/(2 floor(n^2/4))`;
- the `4377/4377`, `3340`, `10464 pairs / 0 exceptions`, `5230 posets`, `6%`/`19%` headroom
  figures; and the diagnosis sentence "THE SWEEP IS WHAT DEGRADES".

So **every number I "reproduce" is a REPRODUCTION, not a discovery**, and I tag them
`[FORMALITY]` when scoring. The dispatch additionally pre-answers item 1 by printing the
increment sequence, so I do not get credit for "finding" that .097 > .049 > .037 > .019 is
decreasing — the only live question there is whether the numbers are RIGHT.

**H2 (LARGE).** The dispatch states the ticket's own verdict on the affirmative half
("expect it to hold") and names all five attack surfaces. I did not choose the attack surfaces.

**H3 (MEDIUM).** I have read `git log` on main, so mg-81ff's, mg-39bf's, mg-d3c7's and mg-9461's
subjects are known to me, including the standing `17/78` scope guard.

**H4.** I have NOT opened: the parent's document, the parent's code, `lib76b2.py`,
`libA94.py`, or the source `.tex`. Everything below is a bet, not a report.

---

## P — predictions (probability = my credence BEFORE looking)

**P1 — 0.30 — the increment sequence has an arithmetic slip.**
The dispatch flags it and dispatches usually flag real things, but `.097/.049/.037/.019` from
`.125/.222/.271/.308/.328` is checkable by hand and I get `.097, .049, .037, .020`. So my live
bet is not "the deltas are wrong" but **P1b at 0.55: the last delta is `.020` and not `.019`**,
i.e. a rounding-direction slip (0.328 - 0.308 = 0.020 exactly at 3dp) that is cosmetic and does
NOT invert the diagnosis. Guard bound in advance: I must recompute `c_true` from my own bracket
in exact rationals, at 3+ significant figures, before scoring either.

**P2 — 0.45 — "four points is not a trend" is a fair hit and the ticket's own framing
over-reads it, but the over-read is NOT the one the dispatch expects.**
I predict the deltas ARE decreasing, so the dispatch's inversion scenario ("the routes are fine
and the truth moves") does not fire. The real weakness I expect is different: **`c_true` at n=3
is the SAME 0.125 as both routes at n=2/3**, i.e. the three columns are not independent at the
left end, so "the routes diverge from the truth" is a statement about 3 usable points, not 4.

**P3 — 0.60 — "IT IS THE CHEEGER SWEEP THAT DEGRADES" is under-separated.**
This is my **principal live bet**. I predict the evidence separates the sweep from
`Delta_P` only if `Delta_P` is measured and shown FLAT across n, and I predict it is NOT flat —
`Delta_P = max_i(1 - (S_P)_ii)` should rise toward 1 with n. If `Delta_P` rises, then the
theorem's own RHS `R(g)(2 Delta_P - R(g))` grows with n for free, and the divergence is at
least partly `Delta_P` and not the sweep. Guard bound in advance: I must **measure `Delta_P`'s
maximum and its distribution at each n = 3..6 on my own code** before scoring this, and I score
P3 LOST if max `Delta_P` is flat (within 0.02) across n.

**P4 — 0.35 — an n=7 figure is used somewhere as if exhaustive.**
The dispatch says route (F) "certifies at 100% of primitive posets at EVERY n = 2..7". If n=7
is a 40–200 sample, then "100% at n=7" is a sample statement, and "100%" reads as exhaustive.
I predict at least one sentence carries the n=7 number without the sample qualifier. Guard: I
must quote the sentence and the sample size from the same document before scoring.

**P5 — 0.25 — the counterfactual (item 4) is overstated.**
"the constant EXCEEDS 1 at n=5, 6 of 275" is a precise, cheap, falsifiable claim and the parent
gives an exact count, which is the signature of a real measurement rather than a rhetorical one.
So I bet it holds. What I predict at **0.50** is the weaker defect: that only ONE of the two
steps is actually load-bearing at n=5, and the commit sells both jointly ("BOTH ARE LOAD-BEARING")
off a single joint counterfactual. Guard: I must run the 2x2 (drop each step alone, drop both).

**P6 — 0.35 — the quantifier move has a second use site the parent did not check.**
The parent asserts "L2 enters at exactly ONE place — Lemma 3.3". A byte-wise check at source
either confirms or refutes that. I predict the ONE-place claim is TRUE as stated but that the
parent verified it by reading rather than byte-wise, so the claim rests on a weaker argument
than it appears to (the mg-39bf pattern: the zero is right, the argument for it is weaker than
advertised).

**P7 — 0.70 — the affirmative half holds.**
Exact PSD certificates plus exhibited rational vectors plus 20/20 selftest is a hard target.
I record NOW what would falsify it so I cannot retro-fit: (a) a primitive poset n<=6 where my
own independently-written cone feasibility fails; (b) a certificate whose PSD check passes only
in float; (c) a "primitive" population whose count disagrees with the known 4377.

**P8 — 0.20 — I find a defect that actually invalidates mg-51f4's scoping.**
Low, because mg-51f4 is scoped against "the sweep's loss" and even a partial re-attribution to
`Delta_P` leaves the sweep as a real loss channel. A finding here is more likely to REFINE
q51f4's scope than to void it. I will mail it either way, immediately, per the dispatch.

---

## E — errors of my own, filed in advance

**E1.** I re-derive `c_true` with a DIFFERENT definition than the parent's and score a
disagreement as the parent's arithmetic slip. Guard: before scoring P1, I must state my
definition of `c_true` explicitly and check it reproduces the parent's n=2 and n=3 values, which
are the ones least likely to hide a definitional gap.

**E2.** I attribute the divergence to `Delta_P` off a float measurement with no exact check —
publishing a re-attribution produced by a broken instrument, which is the defect mg-39bf named.
Guard: the `Delta_P` numbers go through exact rationals.

**E3.** I count "primitive posets" with a different predicate and get a number other than 4377,
then read my own population bug as a parent defect. Guard: my count must hit 1, 1, 2(?), ...,
4377 at n<=6 before ANY population-level claim is scored.

**E4.** I score "four points is not a trend" as a defect when the parent never claimed a proof
from four points — attacking a strawman the dispatch handed me. Guard: I must quote the
parent's ACTUAL sentence about convergence before calling it an over-read.

**E5.** I treat agreement with the parent as confirmation when my code is a paraphrase of
theirs. Guard: I do not open `lib28ff.py` until my own `lib29fe.py` produces its numbers.
**This is the guard I am most likely to break** because the parent's lib is right there and
reading it is faster than writing mine.

**E6.** I publish an n=7 count as exhaustive myself while auditing exactly that defect —
the remedy exhibiting the defect it remedies. Guard: every n=7 number I print carries its
population size and the word SAMPLE or EXHAUSTIVE explicitly.

**E7.** I sell "0 counterexamples over an enumerated population" as a bound — the parent's own
E7. Guard: every maximum I report is labelled a maximum over an enumerated finite population.

**E8.** I delete or withdraw a contested figure rather than qualifying it, against the standing
scope guard (fourth occurrence today). Guard: I add scope, never subtract numbers.
