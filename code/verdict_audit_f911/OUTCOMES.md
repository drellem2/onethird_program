# mg-f911 — OUTCOMES

Predictions from `PREDICTIONS.md` (committed at 7c1b16d, before any of the
parent's 18 files was opened), scored against what happened. Refuted predictions
are kept as written.

Every count below is from **2026-08-09**. The parent's are from **2026-08-07**.
Where they differ, both are given.

---

## VERDICT ON THE PARENT: CONFIRMED, with one live defect and one rot

`verdictwatch.py` is a correct detector of the predicate it claims. It fires on a
drop constructed on purpose, stays quiet on its matched control, covers the
archived case, sizes what it cannot see, and its causal claim survives an
out-of-sample test the parent could not have run. The two findings against it are
(a) **its evidence went stale within a day of landing** and (b) **nothing runs
it**.

---

## SCORING

| # | p | claim | outcome |
|---|---|---|---|
| P1 | 0.85 | `verdictwatch.py` runs live and exits non-zero | **HIT** — 196 scanned, 124 dropped, exit 1 |
| P2 | 0.45 | population reads `work/done/` only, misses `work/archive/` | **REFUTED** — `glob(work/**/mg-*.md*, recursive=True)`, lib_bf3f.py:69 |
| P2a | 0.40 | `mg-c3ca` appears nowhere in the parent's output | **REFUTED** — out_verdictwatch.txt:119 |
| P3 | 0.70 | nothing schedules it; it still depends on pm-onethird | **HIT** — see DEFECT-B |
| P4 | 0.60 | a *second* silently-excluded class exists | **HIT, small** — 1 landing (`mg-0426`) has no item file and is in no bucket |
| P5 | 0.75 | my own count within ±10 of 122 but not equal | **HIT** — 124 |
| P6 | 0.55 | landed population larger than 149 | **HIT** — 196 |
| P8 | 0.80 | I can force it to fire | **HIT** — A1.1 arm A, FORCED |
| P9 | 0.80 | matched negative not reported | **HIT** — A1.1 arm B, FORCED |
| P10 | 0.35 | a realistic over-report exists | **SPLIT** — constructible (A1.2 C) but **0 live instances in 1336 messages** |
| P11 | 0.30 | any mail counts, so DELIVERED is an upper bound | **HIT** — A1.3 F; 1 of 70 credits is not verdict-shaped, 8 are credited by an earlier message |
| P12 | 0.65 | fewer than 11 verdicts recovered with content | **HIT** — exactly **1** (mg-ec63) |
| P13 | 0.55 | mg-ec63 specifically not recovered | **REFUTED** — it is the one the parent *did* recover |
| P14 | 0.50 | the eleven are not enumerated as eleven | **HIT** — the ticket names **7** |
| P15 | 0.95/0.85 | parent's sidecar never gets its verdict; the mail exists | **HIT both** |
| P16 | 0.60 | my own `--verdict-file` sidecar will land | see "this report's own defect class" |

**Six of sixteen missed.** P2 was my principal live bet and it lost cleanly: I bet
against the enumeration on three named grounds and all three were wrong. P13 lost
because I assumed the parent had recovered nothing; it had recovered exactly the
one item the ticket asked for first.

---

## THE FINDINGS

### DEFECT-A — the fire suite rotted 22 hours after it landed, and nothing noticed

`d3_fire.py` (the matched pair) and `selftest_bf3f.py` (the mutation test) both
**crashed on this machine today**:

    RuntimeError: mg mail send failed: Error: no mailbox named "filer-a",
    and no work item is called that either: mg has never seen this recipient

mg-d639 (filed 2026-08-07T13:15Z) made an unknown mail recipient a refusal rather
than a silent create. The `mg` binary carrying it is dated **Aug 7 23:06**.
mg-bf3f landed **2026-08-06T23:48:50Z**. So the suite was broken roughly **22
hours after it landed**, by an unrelated change, and stayed broken for two days
until this audit ran it.

**What rotted is exactly the part that mattered.** The read-only halves
(`d1_population.py`, `d2_cause.py`) still run and still exit 0. The two that died
are the two that constitute the evidence that the detector is not vacuous — the
whole of mayor's demand, *"do not ship a detector you have only ever seen stay
quiet."* As of yesterday the claim "it has been seen to fire" was true and no
longer reproducible by running the committed code.

**Repaired here**, one flag (`--create`) at `d3_fire.py:80`, the single call site
both probes share. After the repair: **13/13 constructions pass, exit 0**, and the
mutation test again catches both constant mutants (8 and 5 constructions).

It failed *loudly* — a crash, not a vacuous pass — which is the difference
between this and the class the arc usually finds. It is still a detector whose
proof-of-life is a script nobody runs.

### DEFECT-B — the detector depends on the filer remembering it, which was brief item 6

    "CHECK IT DOES NOT DEPEND ON ME. If the design requires the filer to notice
     anything, it has reproduced the mechanism it replaces."

`verdictwatch.py` is a command. Searched: **0** `pogo schedule` entries across all
22 registered schedules, **0** cron entries, **0** references to `verdictwatch`
anywhere outside its own directory except a stale search index. The only thing
that makes it report is pm-onethird deciding to run it.

pm-onethird's original complaint was *"that is me being lucky on a cadence."*
The deliverable replaces *noticing a ticket went done* with *remembering to run a
script*. That is a better instrument on a mechanism of the same kind. The parent
did not claim otherwise, and its "WHAT I DID NOT DO" says it did not repair the
cause — but the ticket asked item 6 and the shipped artifact does not answer it.

**Not repaired here.** Registering a schedule is a change to the fleet's
scheduling surface from a polecat worktree, and the parent's own reasoning
against shipping half a cause-fix applies. Named so it can be asked properly.

### DEFECT-C — "any mail counts" is a bound the README does not size

The predicate is *a message in the filer's mailbox whose `From:` is the worker*.
Nothing tests that the message is a verdict. **Forced:** a worker that mails
"I am stuck, can you clarify scope?" and never files a verdict reads DELIVERED
(A1.3 F).

The README sizes four bounds explicitly and this is not among them. Live
incidence: **1 of 70** delivered rows is credited by a subject that is not
verdict-shaped, and **8** are credited by the *earliest* of several messages,
which dates the row by whichever message came first. So the DROPPED count is a
**lower** bound and DELIVERED an **upper** bound — the opposite direction from
the bound the README does state.

### NOT-A-DEFECT — the over-report trap has zero live instances

A verdict signed with the branch spelling `polecat-<name>` instead of the agent
name `<name>` is in the filer's mailbox and is still reported DROPPED (A1.2 C,
forced). `worker_names()` derives `{name, mg-name}` and never the `polecat-`
form.

**Candidate space measured: 1336 messages in pm-onethird's mailbox. Zero have a
`polecat-*` sender. Zero DROPPED rows have any message from a sender carrying
their id under a spelling the resolver missed.** So the 124 is **not** inflated by
this. It is a latent trap, and reporting it as a live miscount would have been the
over-report the brief warns retires a detector. Recorded as latent.

---

## CORRECTIONS TO MY OWN BRIEF

**1. The `archived` premise is false.** The brief says *"mg-c3ca reached
`archived`, not `done`."* The live store shows `work.done` at
2026-08-06T00:48:36Z and `work.archive` 21 hours later. Further, **`mg archive`
refuses an item that has not gone done** (constructed: rc=4, *"not done — it is
claimed"*), so *no* item can reach archived without passing through done, and
`load_landings`' `work.archive` branch is unreachable as a first landing.

The real hazard in the archived case is not the status word — it is that the
item's **file moves out of `work/done/`** into `work/archive/<month>/`. I
constructed that move and confirmed the item is still found and still reported
(A1.4 G). The parent handles it. **My P2 bet against this lost on the merits.**

**2. "The eleven" is not a set.** mg-bf3f names **seven** — mg-ec63, mg-6e58,
mg-0120, mg-5f7c, mg-d53d, mg-ba2a, mg-1abe — then *"and others"*. The remaining
four are enumerated nowhere. The brief instructs "check each has an actual
recovered verdict"; four of the eleven cannot be checked because they were never
named. Any report printing eleven ids has silently chosen four.

**3. Item 4's worry does not apply: both halves were repaired.** The brief warns
that repairing one cause leaves the other alive. The parent routed the
`mg done --result` half to mayor rather than fixing it, and **that half is now
fixed and live**: mg-dfea's `--verdict-file` fix (7a865a8) is an ancestor of the
running pogod revision 738e322, and **256 of 2047 result sidecars now carry a
`verdict` key**. Neither cause survives.

## CORRECTIONS TO THE PARENT'S FRAMING

**1. "It was never lost from the repository, only from its reader" — true, and
now measured.** The parent asserted it about mg-ec63. Across the whole backlog it
holds for **123 of 124**; the exception is `mg-a053` (archived, tagged `broken`),
which has no verdict-bearing commit in either repository. So the consolation is
right, and there is exactly one item it is wrong about.

**2. The recovery was one item, not the backlog.** The parent's D4.4 prints 30 of
122 rows as id + **ticket title**. A ticket title is what the filer wrote when
filing; it is not what the worker found. On the brief's own standard — *"the
finding, not the fact of its absence"* — the backlog is a count. `RECOVERED_VERDICTS.md`
in this directory does the recovery: **7 of 7 named items, each from a commit
stamped with its own id**, with the worker's own words reproduced. For mg-ec63
that is `7fccb4e` — the same commit the parent identified independently.

---

## THREE DEFECTS OF THIS AUDIT, all caught before publication

Filed in advance as E3 (*"I build my own predicate with a different rule, get a
different number, and call the difference a defect when my rule is the wrong one"*).
It fired three times.

1. **I nearly published "64 verdicts have nothing to read."** My recovery rule was
   a hand-written whitelist of whole commit-type strings. This arc writes
   *compound* types — 98 `docs+repair` and 98 `docs+audit` commits scored as
   not-a-verdict because the exact string was not in my table. A hand list over an
   open population, which is the defect this arc keeps filing against others.
   Component-based now. **64 → 1.**
2. **I searched one repository.** 14 of those 64 are filed against
   `one_third_width_three`, which my search never entered. Both repos now.
3. **I recovered the wrong commit for the item that mattered most.** My docstring
   said "authored on the item's own branch"; the code only grepped for a mention,
   so mg-ec63 resolved to `e11b63e` — mg-18dc's *audit of* mg-ec63. An auditor's
   verdict about an item is not that item's verdict, and calling it recovered is
   the exact substitution this brief is about. Own-branch attribution is required
   now, and a mention-only fallback is labelled ⚠ in the output.

Defect 1 is the serious one: unrepaired, this audit's headline would have been a
false and much scarier number than the truth.

---

## THIS REPORT'S OWN DEFECT CLASS

The standing target: *a report about undelivered reports that itself goes
undelivered would not be new here.*

- **Mailed to pm-onethird before submitting**, per the retrofit in my own
  dispatch — the channel the parent proved is the only one that works.
- **`--verdict-file` passed at submit**, so the sidecar carries it too. mg-bf3f's
  own sidecar carries no `verdict` key; the fix that changes this landed after it.
- **The recovered content is committed as a file**, not as a commit subject. A
  commit subject is what this whole arc has been failing to read.

`a1_controls.py` is committed with its transcript and, unlike the artifact it
audits, **it runs on today's `mg`**.

---

## WHAT I DID NOT DO

- **I did not repair DEFECT-B.** No schedule registered, no crew duty filed. It is
  the one finding that needed a change outside this worktree.
- **I did not re-audit any recovered verdict.** `RECOVERED_VERDICTS.md` reports
  where each finding is and what it says, not whether it is right — the same
  scope limit the parent set for mg-ec63.
- **I did not reproduce the parent's 122, its 149, its 16-of-191, or its
  8.7e-09.** My population is 196/124 on a store that moved. A3.1 recomputes the
  contingency table with my own regex and gets the same *shape* (93% vs 11%,
  p=1.9e-29); that is evidence the parent computed what it said, not an
  independent confirmation.
- **A3.2's out-of-sample result is confounded and says so.** The retrofit was not
  the only change on 2026-08-07; the finding was circulated fleet-wide the same
  day. It rules out H-REAP-as-cause (the reap is unchanged, the rate is not); it
  does not isolate the ticket body from everything else that happened.
- **I did not read any mailbox but `pm-onethird`'s**, and only for this predicate.
- **I did not check the 14 `one_third_width_three` items' commits by hand** — they
  are included by rule, not inspected.
- **My verdict-shaped classifier in A2.2 reads subjects with a keyword regex.** It
  establishes the direction of the bound, not a corrected count.
