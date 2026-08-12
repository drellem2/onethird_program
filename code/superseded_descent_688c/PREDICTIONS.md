# mg-688c PREDICTIONS — DID ANYTHING DESCEND FROM THE SUPERSEDED READINGS?

Filed 2026-08-12, **mid-investigation and not before it**, which is the only honest place to
file it. The exposure is disclosed below rather than laundered: several of the ticket's
questions were already answered at my keyboard before this file existed, and those are
**REPORTS at zero predictive credit**. Only the items marked **LIVE** were unmeasured when
this file was committed.

---

## EXPOSURE, STATED FIRST

Before writing this file I had already run, by hand:

- the reflog of `main-mirror` and of `origin/main` in `one_third_width_three`;
- `gh api .../events` for that repo's push history (85 `PushEvent`s);
- `git diff 912f1b1 949c439` over the four affected cited documents;
- a fingerprint grep over `onethird_program` commits inside the strike hazard window;
- `git log -S` for the two line anchors in `STATE.md`.

So R1–R5 below are **things I already know**. They are written down because the ticket asks
for them and because a prediction file that omits what the author already knows is worse than
no prediction file. They score **nothing**.

---

## R1–R5 — REPORTS (already measured, ZERO CREDIT)

- **R1.** The window is **boundable exactly**, on both ends, and the bound does not need a
  guess. The `main-mirror` branch was created `2026-07-20T23:36:35Z` and repaired
  `2026-08-12T21:07:16Z`, both from its own reflog (two entries, nothing between).
- **R2.** The mirror was **born current, not born stale**: `912f1b1` was pushed to
  `origin/main` at `2026-07-19T22:08:44Z` and the next push landed `2026-07-21T00:05:09Z`,
  which is *after* the branch was created. It was current for 28m34s of its 22-day life.
- **R3.** Four distinct cited documents changed between `912f1b1` and `949c439`; three carry
  strikes/withdrawals; one (`BK-Transport-Transfer-Probe`) carries a correction with no strike.
- **R4.** The per-claim hazard windows are **much shorter than the staleness window** — the
  Reverse-Cheeger and Kill-Shot withdrawals were pushed on `2026-08-07`, four days and 22 hours
  before the repair, not 22 days before it.
- **R5.** `STATE.md`'s `:310` / `:286` anchors — mg-cdd5's "caught in the act" evidence — were
  authored at `2026-08-07T17:09:24Z` (`276aead`), which is **before** the two pushes that
  shifted those line numbers. So they were correct against the live remote when written and
  are **not** evidence that their author read the stale checkout. This is a correction to an
  inference in mg-cdd5's commit message, not to any of its measurements.

## P1–P6 — LIVE (unmeasured when this file was committed)

- **P1 (mail).** A fingerprint sweep of every message under `~/.macguffin/mail` dated inside a
  hazard window returns **0 descendants**. Confidence 0.85. I expect hits — the phrases are
  common in this programme's mail — and I expect every one of them to carry the withdrawal.
- **P2 (`946`).** The `946`→`956` correction has the longest hazard window of the four
  (13d 3h, from `2026-07-29T18:02:52Z`). I predict **0 descendants** in `onethird_program`,
  and further that the *corrected* figure `956` appears **nowhere** in this repository — i.e.
  the correction never propagated here because nothing here consumes that count.
  Confidence 0.7 on the second clause; it is the one I am least sure of.
- **P3 (line anchors).** Outside the three sites mg-cdd5 repaired, **no** reference of the form
  `<affected-doc>:<N>` anywhere in `onethird_program` resolves at `912f1b1` and fails at
  `origin/main`. Confidence 0.8.
- **P4 (tier-2 citing files).** All three tier-2 citing files named by mg-cdd5's sweep were
  authored **before** the withdrawal that made their cited document superseded, so none can
  have descended from it. Confidence 0.75.
- **P5 (verdict).** The total is **NOTHING-DESCENDED**. Confidence 0.8. The alternative I take
  most seriously is a *silent* descendant — a document that consumed the withdrawn reading
  without reproducing any fingerprint of it — and P6 is the only defence against that.
- **P6 (the honest limit).** The sweep is **fingerprint-based and therefore cannot be
  exhaustive**. I predict I will end up reporting a measured zero *with that limit named*,
  not a zero that claims to have read every artifact for meaning. Confidence 0.95 — this is
  nearly a statement of intent, and it is here so that the limit is on the record before the
  result is, rather than appearing afterwards as an excuse.

## WHAT WOULD FALSIFY THE VERDICT

One artifact, authored inside a hazard window, that asserts any of the struck claims **without**
its withdrawal — or that quotes a line anchor which resolves only at `912f1b1`. One is enough;
the verdict is a zero and a zero dies on a single witness.
