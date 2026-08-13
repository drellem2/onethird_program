# mg-96df — nine broken line anchors: the verdict is LEAVE AND RECORD, and it was already ruled

**Ticket:** mg-96df, filed by p688c out of mg-688c's descent sweep. Nine line
anchors in three documents resolve to text that is not what the citing sentence
says is there. *"VERDICT REQUIRED: renumber / convert to section anchors / leave
and record."*

**Answer: LEAVE AND RECORD — and it is not a new decision.** mg-cdd5 settled this
class in writing, naming two of the three files, and it landed (`4ce7da3`,
21:26:20Z) fifty-nine minutes before this ticket was filed:

> **Anchors in frozen audit records are LEFT.** `code/row3b_audit_eba7/OUTCOMES.md`
> and `docs/state-history/audit-mg-eba7-of-mg-55f2.md` both anchor into
> `ComparisonRoute.md:104`; that line was **edited in place**, so those anchors
> still stand — but the standing rule here is that a record of what was read at
> the time is not improved by being re-pointed at what is true now.
>
> — `code/mirror_staleness_cdd5/README.md`, §5

So the three documents keep their numbers and each gains a **DRIFT NOTE** at the
bottom, which is the ticket's own *"if 'leave', say so at the sites."*

---

## 1. Four findings, and three of them contradict the ticket

**F1 — NONE OF THE NINE LACKS A TARGET. The ticket says four do.** Its table is
produced by exact line comparison and marks *"(text no longer present verbatim)"*
on **five of its nine sites**, which are **four** distinct cited lines — the
ticket's prose counts the targets, its table counts the sites, and both readings
land on the same conclusion: *"they need a human to decide whether the citing
sentence still says something true, which is why this is not a mechanical patch."*
Every one of them relocates, on a prefix of 43 characters or more:

| the ticket's *"no verbatim target"* | actually |
|---|---|
| `ComparisonRoute.md:104` (two sites) | **it did not move** — `:104` is the same table row, rewritten in place |
| `KillShot-Probe.md:20` | `:68` — 125-char prefix, strike and warning appended |
| `KillShot-Probe.md:103` | `:151` — 43-char prefix, strike and warning appended |
| `KillShot-Probe.md:286` | `:350` — 73-char prefix, warning appended |

The predicate is correct and the conclusion does not follow. **This corpus's
repair idiom is to append a strike and a warning to a line rather than replace
it**, so a withdrawn row is byte-different and is the same row. An exact matcher
meets that idiom and reports UNREPAIRABLE. `a0_selftest.py` §1 plants the case
and shows both answers side by side.

**F2 — one of those four was already repaired, in this repository.**
`:286 → :350` is mg-cdd5's number, derived from a *"unique 74-character prefix"*
and applied to `STATE.md` at `4ce7da3`. The *unrepairable* row and its completed
repair have been sitting here together.

**F3 — three of the nine are not drifted anchors at all, and what is stale in
them is a claim.** `ComparisonRoute.md:104` still resolves. The three citing
sentences say, in the present tense, that it is *"a live status table"* quoting
`0/132` *"bare"*, that *"nobody owns it"*, that it is *"the part of the finding
that still has no carrier."* `a8688f2` (mg-e2a0, 2026-08-07T22:20:29Z) struck
that exact cell — its subject is *"land mg-55f2's 0/132 ruling AT ITS
DESTINATION"* — so the audit's open item was closed within the hour and the
audit does not know it. **No renumbering could have reached this**, because the
line never moved. It is the sharpest thing in the ticket and the ticket does not
name it.

**F4 — the argument against renumbering is measured, not preferred.** The cited
document contains the only hand-written renumbering in this hazard, in its own
banner at `949c439:22–24`: *"`STATE.md` row 3b cites this document at `:286`,
which … is `:345` after it. Line refs into this file made before 2026-08-07 are
off by `+59` from here down."* **Both figures are wrong by five.** The row is at
`:350`; the offset for it is `+64`; and there is no single offset to quote — the
five anchors into that file move by `+48`, `+48`, `+53`, `+53`, `+64`. Exactly
one commit touched the file in the whole window, so this is not later drift:
**the hand-written renumbering was wrong the day it was written.** Two lines
above it, the same banner gets it right — *"Sites are named by section, not by
line."* (A defect in `one_third_width_three`; reported, not fixed. This
repository does not own that file.)

## 2. Two corrections to the ticket's own framing

**The seven were not "correct when written" against `origin/main` — they were
correct against a checkout that had not moved in nineteen days.** mg-cdd5
established that authors here were reading the mirror checkout, pinned at
`912f1b1` (2026-07-19). `BK-Transport-Transfer-Probe.md:112` had already shifted
on 2026-07-29, nine days before the audit was written. *"Nobody made a mistake,
the target moved"* is the right conclusion for the wrong reason.

**The forty minutes are push times and the commit clocks disagree in direction.**
The ticket dates the authoring at `22:36:18Z` and the shift at `23:16:33Z`.
`e9ae5e0` carries author date `21:33:04Z` and commit date `22:36:18Z`; `a8688f2`
carries `22:20:29Z` in the cited repo. On those clocks the strike lands 47
minutes *after* the audit was written and 16 minutes *before* it was committed.
Nothing turns on it — the stale checkout decides it either way — which is why
both are printed rather than the flattering one.

## 3. The population was re-derived, not taken on trust

The ticket's table is pinned to `949c439` and says so. Nothing here quotes it.
`a1_anchors.py` re-extracts every anchor from the three documents and resolves it
against the cited repo's **`ls-remote` answer**, printing the measured revision
and whether it still equals the pin.

| | |
|---|---|
| anchors in the three documents | 31 raw, 29 unique |
| into the cited repo | **11** |
| the cited number still lands on the cited row | 3 |
| moved, with a determinate new number | 8 |
| **without a determinate target** | **0** |
| the cited *text* changed, so a quotation of it is stale | 5 |

Against the ticket's nine: the extra two are `Reverse-Cheeger:310–313`, a **bare
backticked range** whose end (`:452`) is the number a repairer actually needs and
which the ticket's `(file, doc, line)` key collapses into its `:310` row — the
same blind spot mg-cdd5 had to close by hand for `STATE.md` — and
`ExpectedRank-Certificate.md:84–90`, which is not broken.

**And the ticket's population is confirmed rather than assumed.** The repo-wide
arm resolves every explicit anchor into the cited repo, 365 unique, and finds
**0 drifted outside the three named documents**. That check has its own trap and
it is disarmed: an earlier version resolved every anchor forward from `912f1b1`
and so scored `STATE.md`'s two **already-repaired** anchors as broken, because
`:449` does not exist at the old revision. A sweep that scores a completed repair
as a defect goes red precisely because its own finding was acted on.

## 4. The repair could have committed the defect it reports — and nearly did

*A remedy is an artifact of the same kind as the defect, so it is subject to it.*
The enumeration was written before the notes were, and one arm of it changed the
repair:

**All three documents are themselves cited by line.**
`docs/OneThird-SupersededDescent-mg-688c.md` — mg-688c's own deliverable, the
ticket that filed this one — anchors at `audit-mg-eba7-of-mg-55f2.md:112` and
`OUTCOMES.md:72`; `code/mirror_staleness_cdd5/README.md` anchors at all three.
**A banner at the top of any of these files breaks live anchors in the course of
repairing a report about broken anchors.** So the notes are **appended**, and
`a2` arm **X1** re-reads each file at `HEAD` and fails if a single existing line
changed. 20 incoming anchors, 0 disturbed.

The rest of the enumeration:

* **X2 — not one number in the notes was typed.** Every relocation the notes
  state is re-derived from the two revisions *and* required to appear in the
  note. A typo fails on one side, a bad derivation on the other. 11 claims.
* **X3 — the durable form is durable.** Each section a note names must exist at
  the cited revision *and be unique there*; a heading occurring twice is no
  better than a line number.
* **X4 — the pin.** The notes' numbers are true at one revision, so each note
  must **name** it. Currency is **reported, never scored** — a control that goes
  red because the world moved on is the same defect mg-cdd5 caught in its own
  arm E1.
* **X5 — D1, the sweep must not sweep itself,** and the exclusion is measured
  rather than asserted: 483 anchor-shaped strings repo-wide, 410 after excluding
  the three instrument directories, 22 of the difference this instrument's own
  transcripts.
* **X6 / X7** re-derive the two findings the notes rest on (F4, and which halves
  of §1.4's closing observation survive) from the repository, rather than
  trusting the note that states them.

## 5. What was adjudicated, since the ticket asked for a human

**§1.4's closing observation is now half true, and the surviving half is the
sharp one.** It observes that the probe carries `standard dominance | **holds**`
at `:198` and **GREEN** at `:20`/`:103` *"with no scope qualifier."* At
`949c439`, `:20` (`:68`) and `:103` (`:151`) **both gained the qualifier**;
`:198` (`:251`) is **byte-identical and still unqualified**, and what it gained
is a parenthesis five lines below saying the row is a per-poset readout *"flagged
and deliberately left, mg-e2a0."* So *"a reader who stops at `:198` gets an
unqualified 'holds'"* **still stands**, deliberately and on the record, and is
now the only part of that observation that does.

**`bb60`'s anchor is a stale read and the note says so.** `7058fbd` wrote
`KillShot-Probe.md:127–142` on 2026-08-12, five days after those lines moved. It
resolved only because the checkout it was read from stood at 2026-07-19. The
quoted sixteen lines are byte-identical at `:180–195`, so §3's reasoning is
untouched; what the anchor now carries is evidence of the stale read, which is a
second reason not to renumber it away.

## 6. Not done, and why

* **Nothing in `one_third_width_three` is touched.** F4 is a defect in that
  repository's own banner. This branch targets `onethird_program`.
* **No detector is shipped, and this suite is deliberately NOT on `build.sh`.**
  The ticket says a watcher for moved anchors *"is a bigger ticket than this one
  and should be filed separately if wanted"*, and it is right — `a1` is scoped to
  this repair, not to standing surveillance. Gating merges on it would also make
  every merge depend on a **second repository being checked out on the host**:
  `a1`/`a2` exit 2 when `one_third_width_three` is absent, so on a machine
  without it the gate would go red for a reason that has nothing to do with the
  branch. A standing detector has to answer without reading any checkout — which
  is exactly the shape mg-cdd5 gave its own — and that is the separate ticket.
* **`STATE.md` is not touched.** mg-cdd5 repaired it; the repo-wide arm confirms
  both of its anchors are current.

## 7. Files

| | |
|---|---|
| `lib96df.py` | the match ladder, section anchors, read-only blob access |
| `a0_selftest.py` | 45 checks on planted text — the ladder before it meets the corpus |
| `a1_anchors.py` | re-derive the population and relocate every member |
| `a2_controls.py` | 39 arms, mostly aimed at this repair |
| `run_all.sh` | all three in order, ~13 s measured, exit 0 |

Re-run rather than quoting the transcripts: they carry line numbers into a moving
file, which is the defect this ticket is about.

## `a1` and `a2` read THIS repository at an as-of commit too (`mg-20ee`)

`lib96df`'s **E1** says an instrument about stale reads must not itself read a stale checkout —
and then applies that only to the *mirror*. The repo-wide sweeps in `a1` and `a2` walked **this**
repository's working tree, so every `doc:NNN` they printed was an offset into a file this
instrument does not own, over a corpus that grows under it: the exact defect `mg-96df` exists to
measure, in the measuring instrument. It had already fired — a re-run on 2026-08-13 moved the
repo-wide population from **365 to 413** and the anchor-shaped count from **483 to 531**.

**E1b** turns E1 around on this repository. The citing repo is read at `SELF_AS_OF = f59fe1f` via
`git ls-tree`/`git show`, the same mechanism E1 already required of the mirror. No predicate and
no verdict changes; what changes is which bytes the predicates are evaluated over.
`ANCHOR_DRIFT_AT=HEAD` (or `=WORKTREE`, or any commit) re-measures against a different corpus.

**Two other things had to be named before the transcripts could reproduce at all**, and both were
pre-existing:

- **E1c — `a1` printed the absolute worktree path** (`/Users/daniel/.pogo/polecats/p96df`). That
  made the transcript reproduce for exactly one operator. What identifies the citing repo is the
  **commit**, not the checkout, so the line now prints `SELF_AT`. `program_root()` is still used
  to locate the git directory; it is no longer printed and no longer walked.
- **X1 spelled "before and after the repair" as "HEAD vs the working tree"**, which is only the
  same thing while the repair is still uncommitted in the author's own checkout. For every later
  operator it silently re-answered a different question. The two states are now named:
  `SELF_AT^` is before, `SELF_AT` is after. Measured, not asserted — this reproduces the committed
  `363/115`, `77/33` and `253/32` exactly.

**X5's number moves once, and the reason is worth keeping.** It went `483 → 489`, and the
instrument's own contribution `22 → 28`. The cause is not the pin: `a2` counted **its own
not-yet-written transcript**. `out_a1_anchors.txt` carries 22 anchor-shaped strings and
`out_a2_controls.txt` carries 6, but `a2` runs before `a2`'s own output exists, so the old run
saw only a1's 22. `22 + 6 = 28` is the self-consistent value and the pinned run is the first one
that can reach it. **The verdict does not move** — `without > with_ex` still holds and X5's point
(the exclusion matters) is untouched. So the number was *self-referentially unstable*, and
pinning is what gave this instrument a fixed point at all.

**Both directions measured, which is the acceptance.** Unchanged corpus: two consecutive
`run_all.sh` runs are byte-identical — the transcripts are a fixed point. Changed corpus
(`ANCHOR_DRIFT_AT=HEAD`): `a1` differs in 6 lines and **every one is an address, a
population count, or the as-of block**; no adjudication changes.
