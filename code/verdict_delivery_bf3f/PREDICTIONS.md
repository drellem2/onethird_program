# mg-bf3f — predictions for the VERDICT-DELIVERY DETECTOR

**Committed before any script of this instrument exists.** The only code that has
run is throwaway probing outside the repository; everything it measured is
disclosed below as a MEASUREMENT (M-rows), not laundered into a prediction. The
P-rows are the falsifiable ones: each is a thing I have not yet measured at the
time this file is committed.

Written 2026-08-06/07 by polecat `dbf3f` on branch `polecat-dbf3f`.

---

## 0. WHAT THE TICKET ASKS AND WHAT I AM ANSWERING

pm-onethird asks for one predicate:

> AN ITEM REACHING `done` (OR `archived`) WITH NO VERDICT MAIL RECEIVED BY ITS
> FILER IS A DROPPED VERDICT.

and for the cause to be **determined**, not assumed, between two live
hypotheses:

- **pm-onethird's**: instruction drift — the worker's instructions degraded over
  a long run and the verdict is never sent.
- **mayor's**: polecat reap — the worker is stopped between producing the
  verdict and mailing it.

The mayor's dispatch note adds a third demand, which governs the shape of this
suite: **MAKE THE DETECTOR FIRE.** A detector for a silent failure that has
never been seen to fire is this arc's signature defect. Section D3 exists only
to make it fire on a failure I construct on purpose.

---

## 1. MEASUREMENTS DISCLOSED (not predictions — these are already known to me)

**M1.** `pm-onethird` has filed 184 work items. 149 of them have a `work.done`
event in `~/.macguffin/events.jsonl`.

**M2.** A crude detector — "no message anywhere in pm-onethird's mailbox
(cur+new+archive, 979 messages) mentions the item id" — reports 26 of those 149.
I already know this detector is wrong in both directions; see M3 and P2.

**M3.** Resolving the worker from the item's own result sidecar
(`{"branch": "polecat-<name>"}`) and requiring the message's `From` to equal that
worker, pm-onethird's mailbox holds **28 verdict mails covering 21 distinct
items**.

**M4.** Verdict-mail arrival relative to the item's `work.done`: **21 of 28
arrive BEFORE done**, by 4 to 167 minutes. The remaining 7 arrive at 0 or −1
minutes. **Not one arrives more than one minute after done.**

**M5.** `agent_stopped` (reason=`requested`) follows `work.done` by **0 or 1
second** for the overwhelming majority of pm-onethird's items — and the
distribution is the same in the delivered group as in the dropped group
(delivered: 0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,13,55,608,689,2525,2685 s;
dropped: 0 or 1 s for all but none).

**M6.** Four polecats on dropped items sent mail to `mayor` well inside their own
lifetime and never mailed the filer: `x77e6` (5 mails, last 52 min before its
stop), `z9a59` (73 min), `y0120` (10 min), `c1d6c` (21 min).

**M7.** The instruction *"mail the verdict to `pm-onethird` BEFORE submitting to
the refinery"* appears in **16 of pm-onethird's 184 filed items**. First:
mg-fcb2, 2026-07-31T04:13:24Z. **Last: mg-5854, 2026-07-31T10:02:11Z.** It has
appeared in **no ticket filed since 2026-07-31 10:02Z** — not on 08-04, not on
08-05, not on 08-06.

**M8.** Contingency over pm-onethird items reaching done on/after
2026-07-31T04:13Z: instruction present → **14 of 16 delivered**; instruction
absent → **7 of 45 delivered**.

**M9.** 19 of 19 sampled dropped items carry a result sidecar written by the
refinery — `{"branch":…,"completed_by":"refinery","mr":…,"target":"main"}` — and
**not one carries a verdict**. The `mg done --result` half of pm-onethird's
instruction is empty in every case I have looked at.

**M10.** The polecat dispatch protocol's own step 7 hands the worker
`mg done --result="{\"branch\": \"$BRANCH\"}"` — a result template with no
verdict field — and tells it that pogod will usually have closed the item first.

**M11.** mg-69be (the `for Daniel` CORE LEMMA, commit 6ed98c4 in
`one_third_width_three`) was filed by `daniel`, not pm-onethird. Its polecat sent
**zero mail of any kind**. pm-onethird relayed the lemma to the `human` mailbox
**by hand** at 2026-07-15T17:24:22Z, 37 minutes after mayor's merge notice. So
the deliverable did reach Daniel; the *mechanism* did not deliver it.

**M12.** 4 of the 149 have no `polecat-*` branch in their sidecar, so no worker
is resolvable from mg's own store.

---

## 2. PREDICTIONS

Scored in `OUTCOMES.md` after the suite runs. Misses are kept as written.

### The population

**P1.** The instrument's own count of dropped verdicts for `pm-onethird`, under
the rule it declares, will be **more than eleven**, and I predict it lands in
**35–45**. The ticket's "eleven" is pm-onethird's count of what it *noticed*.

**P2.** **Zero** of the 21 items with a known worker→filer verdict mail (M3) will
be reported as dropped. This is the false-positive control and it is the
prediction I least want to lose.

**P3.** Run across every filer rather than only pm-onethird, the detector will
report drops for **at least one filer other than pm-onethird**, and I predict
`daniel` will be the largest such population with **≥ 20** dropped items.

**P4.** The detector will report a non-empty **UNDECIDABLE** bucket — items whose
worker cannot be resolved from mg's own store — and I predict its size for
pm-onethird is exactly **4** (M12), i.e. that resolving from the sidecar is the
only resolution the instrument needs.

### Making it fire

**P5.** The hermetic construction (D3) builds a throwaway `MG_ROOT`, drives the
**real `mg` binary** through new/claim/done, and asserts the detector reports
exactly **1** dropped verdict on the arm where no verdict mail was sent and
exactly **0** on the matched arm where one was. Both will pass.

**P6.** The **first form** of the detector will FAIL at least one of the
constructed edge cases. Named in advance, the three I think most likely to break
it: (a) an item that reached `archived` rather than `done`; (b) a verdict mail
that was archived out of the filer's active mailbox; (c) a filer with no mailbox
directory at all. I predict **(c)** is the one that breaks first.

**P7.** Run on the live store while `mg-bf3f` is still `claimed`, the detector
will **not** report `mg-bf3f`. Run after `mg-bf3f` lands, with no verdict mail
sent, it **will**. I intend to exercise the second half deliberately and record
the transcript, then send the verdict and record the detector going quiet.

### The cause

**P8.** The reap hypothesis will be **REFUTED for the mail channel**: I predict I
will not be able to construct a single dropped item in which the polecat's
`agent_stopped` precedes a mail it could otherwise have sent, and that in **0 of
the dropped items** does the stop fall inside the interval where compliant
polecats actually mail (M4: 4–167 minutes *before* done).

**P9.** The reap hypothesis will be **CONFIRMED for the `mg done --result`
channel**, which is a different fault with a different owner: I predict **≥ 95%**
of pm-onethird's done items carry a refinery-written sidecar, so a polecat that
followed "write `mg done --result` with your verdict" would have been beaten to
the item by pogod. That half routes to **mayor**.

**P10.** The instruction-presence association (M8) will hold under the
instrument's own independent re-derivation, and I predict a Fisher exact
two-tailed p below **1e-5**.

**P11.** At least **3 of the 7** instruction-absent-but-delivered items were
worked by an agent that never worked an instruction-carrying ticket — so ticket
text is a strong predictor but not the whole mechanism, and I will say so rather
than claim a single cause.

**P12.** pm-onethird's own framing — "*compliance appears to have drifted*" —
will be **CORRECTED, not confirmed**: the drift I predict the instrument finds is
in the **filer's ticket template**, not the worker's compliance. Stated sharply:
I predict the instrument shows the instruction stopped being *written* on
2026-07-31, and that no worker after that date was ever asked.

### Recovery

**P13.** mg-ec63's verdict is in neither pm-onethird's mailbox nor its result
sidecar. I predict it **is** recoverable in full from its branch's commit
messages, in **fewer than 6 commits**.

### This instrument's own defects

**P14.** The population will move under my own hand: by the time the transcripts
are committed, **at least one more item** will have joined the dropped list that
was not in it when the first section ran. Three tickets in a row in this arc were
refuted by exactly this, so it is filed as a prediction rather than discovered
afterwards.

**P15.** I will find and record **≥ 2 defects of this instrument itself**.

**P16.** This instrument will itself be a dropped verdict unless I act: mg-bf3f
carries **no** verdict-mail instruction (it is one of the 51 filed after
2026-07-31), so by the mechanism I am about to prove, my own verdict is
scheduled to be lost.

### Exit codes, declared in advance

| section | file | expected exit |
|---|---|---|
| D1 population/census | `d1_population.py` | 0 |
| D2 cause discrimination | `d2_cause.py` | 0 |
| D3 make it fire (hermetic) | `d3_fire.py` | 0 |
| D4 live fire + recovery list | `d4_live.py` | 0 |
| self-test | `selftest_bf3f.py` | 0 |
| `verdictwatch.py --filer pm-onethird` | deliverable | **1** (non-zero: drops exist) |

`verdictwatch.py` exiting **1** is the point. A detector for this failure that
exits 0 today would be reporting that eleven-plus verdicts arrived.

---

## 3. WHAT I AM NOT DOING, DECLARED IN ADVANCE

- I am **not** repairing the cause. The repair is a one-line edit to
  pm-onethird's ticket template plus, on mayor's side, the `--result` channel;
  neither is mine to make from a polecat worktree, and doing one without the
  other is exactly the failure the ticket warns about.
- I am **not** reading any mailbox other than the ones named in this file.
- I am **not** claiming the detector sees verdicts delivered by channels it
  cannot read — a verdict spoken in a commit subject, in a `docs/` file, or in a
  Slack-side relay is invisible to it, and the README will say so as a bound
  rather than a footnote.
