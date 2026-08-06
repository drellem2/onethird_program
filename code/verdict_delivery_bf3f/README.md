# mg-bf3f — the verdict-delivery detector

    verdictwatch.py --filer pm-onethird     # exit 1 while drops exist

pm-onethird asked for one predicate, a report rather than an alarm, and the
cause **determined** rather than assumed. mayor added one demand that governs the
whole suite: **make the detector fire**, on a verdict dropped on purpose, before
shipping it.

---

## THE HEADLINE

**The count is not eleven. It is 122.** Eleven is what pm-onethird noticed.

**The cause splits in two, and they are different faults with different owners.**

- **Mail channel — mayor's reap hypothesis is REFUTED.** Not because the reap
  isn't real (it is, and pogod's own event log confirms mayor's account of it:
  `requested`, within 0–1 s of the landing, in 122 of 122 dropped cases) but
  because **that same distribution holds in the delivered group**. A quantity
  identical in both groups cannot separate them.
- **pm-onethird's hypothesis is CONFIRMED and its statement of it is wrong.**
  Compliance did not drift. **The instruction did.** The line *"mail the verdict
  to pm-onethird BEFORE submitting to the refinery"* appears in 16 of 191 items
  pm-onethird has filed, last on **2026-07-31T10:02:11Z**, and in **0 of the 55
  filed since**. Every worker that was asked delivered. No worker after that date
  was ever asked, so none of them failed to comply.
- **Result channel — mayor's reap hypothesis is CONFIRMED, and it is mayor's.**
  The instruction's other half, `mg done --result` with the verdict, is
  structurally unreachable and has been routed to mayor rather than fixed here.

---

## THE DISCRIMINATION, WHICH IS A TIME INTERVAL

H-REAP requires the verdict to be written inside the window between the worker's
last chance to mail and its stop. So the question is not *does the reap happen*
(it does) but *is the verdict written inside its window*.

    Every delivered verdict, without exception, was sent BEFORE the reap window
    opened. 18 of 25 more than a minute before, up to 167 minutes before. The
    latest any verdict has ever arrived is 0.7 minutes AFTER its landing, from a
    polecat that ran `mg done` itself.

    The reap fires at landing + 0.5 s. It cannot suppress a mail sent 167
    minutes earlier.

And nine dropped items carry **positive proof of liveness**: their polecats went
on mailing *mayor* and then lived 10, 14, 21, 30, 52 and 73 minutes longer.
`x77e6` sent five mails to mayor and its stop came 52 minutes after the last one.
Those processes were alive and mailing. They were never asked to mail the filer.

    instruction present ->  14 delivered,  0 dropped   (100%)
    instruction absent  ->   7 delivered, 38 dropped   ( 16%)
    Fisher exact two-tailed p = 8.7e-09

Honest qualifier, kept because it weakens the headline: **7 of the 7**
instruction-absent items that were delivered anyway came from an agent that had
never seen the instruction on any ticket. Ticket text is a very strong predictor
of delivery. It is not the whole mechanism.

---

## THE DETECTOR HAS BEEN SEEN TO FIRE — THREE WAYS

mayor: *"Do not ship a detector you have only ever seen stay quiet."*

1. **Hermetic, on purpose** (`d3_fire.py`). A throwaway `MG_ROOT` driven through
   the **real `mg` binary** — new / claim / done / mail send / mail archive — with
   a matched pair: arm A's verdict dropped deliberately, arm B's sent. Reports
   exactly 1 and exactly 0. Plus six edge cases: archived item, verdict archived
   out of the active mailbox, filer with no mailbox at all, verdict mailed to the
   wrong addressee, item still in flight, near-miss sender name.
2. **Mutation-tested** (`selftest_bf3f.py` S4). The matched pair is evidence only
   if a constant detector fails it. Two mutants — always-DELIVERED and
   always-DROPPED — are built and both are caught (8 and 5 constructions).
3. **Live, on this ticket's own verdict** (`d4_live.py`). mg-bf3f carries no
   verdict instruction; it is one of the 55. That this ticket's verdict was
   itself scheduled to be lost was filed as **P16 before any of this code
   existed**. With the landing simulated and pm-onethird's mailbox read live, the
   detector reported `mg-bf3f` **DROPPED** — committed as
   `out_d4_live_BEFOREMAIL_DROPPED.txt`. The verdict mail was then sent and
   `out_d4_live.txt` shows the same live row reading **DELIVERED**. Both states
   of one row, neither inferred from the other.

---

## WHAT THIS DETECTOR CANNOT REACH — sized, not footnoted

- **A verdict delivered by any channel but macguffin mail** — a commit subject, a
  `docs/` file, an out-of-band relay — is invisible and is counted DROPPED. The
  polarity is deliberate; the ticket's complaint is that a commit subject is not
  delivery. So **122 is an upper bound on "verdicts nobody received" and a lower
  bound on "verdicts that did not arrive as mail"**.
- **A polecat whose work never merges and never mails leaves no trace at all.**
  The worker's identity enters macguffin only when the refinery writes
  `branch: polecat-<name>` into the result sidecar, at merge. Items with no
  resolvable worker go to their own **UNDECIDABLE** bucket — currently 2 for
  pm-onethird, listed by id — and are never silently absorbed into either answer.
- **The `shape` fallback resolver is asymmetric by construction and says so.** It
  is consulted only when the sidecar is silent, and accepted only when the name
  it proposes actually appears as a `From:` in that filer's mailbox. So it can
  move a row UNDECIDABLE → DELIVERED and **never** to DROPPED: it can shrink the
  reported count, never inflate it.
- **`creator: daniel` on an item filed before 2026-07-30 05:00Z means UNKNOWN.**
  `mg new --help` records that the creator field became per-agent only at
  mg-ddf4; before that it was the unix user, identical for every agent on this
  box. The all-filers table shows 999 drops against `daniel`; that number is
  creator-unknown, not Daniel's lost verdicts, and the instrument says so in its
  own output rather than publishing the scarier figure.

---

## SIX DEFECTS OF THIS INSTRUMENT

Found while building it, recorded rather than tidied. P15 predicted ≥ 2.

1. **The worker was displayed under a name it never used.** `sorted(names)[0]`
   prefers `mg-y0120` over `y0120` alphabetically. Alternate spellings are for
   *matching*; only the branch's own spelling is for *reading*.
2. **Sidecar-only worker resolution filed known deliveries as "cannot tell".**
   mg-9a19 and mg-65eb — both hand-verified DELIVERED before this code existed —
   landed in UNDECIDABLE. Fixed with a second, deliberately narrow resolver.
3. **A scary number that was true of a population nobody meant.** The all-filers
   table's `daniel: 999` is creator-unknown. Corrected in the instrument's own
   output, at the point of publication.
4. **THE WORST ONE: a control that passed vacuously.** `mail()` read the MSG-ID
   by scanning for a dotted token; `mg mail send` prints a *path*, so the scan
   returned `None`, the P6b construction silently skipped its own setup, and then
   asserted DELIVERED against a verdict that had never been archived. A vacuous
   pass of exactly this arc's shape, **inside the file whose only job is to prove
   the detector is not vacuous.** The setup now raises, and its effect is
   asserted rather than printed.
5. **The instrument could not see a single item in flight.** A claimed item is
   not `mg-bf3f.md` on disk — macguffin stamps the owning pid into the filename
   (`mg-bf3f.md.90246`) — and the glob was `*.md`. Harmless for the predicate,
   since a landed item is back to a plain `.md`; not harmless for anything asking
   about work in flight, so it is fixed rather than scoped around. It is why the
   live fire in D4 could not run at first.
6. **A simulated landing had no worker, so the live fire reported UNDECIDABLE.**
   Not a bug but a genuine bound (see above), and the honest fix was to let the
   caller supply the worker — taken from `git rev-parse --abbrev-ref HEAD`, the
   exact string the refinery will write at merge — and to mark the row
   `worker_supplied` so no reader mistakes it for something the store said.

---

## THE FILES

| file | what it is |
|---|---|
| `PREDICTIONS.md` | 16 predictions + 12 disclosed hand measurements, committed at 7cb7a18 before any script existed |
| `OUTCOMES.md` | those predictions scored; 5 refuted and kept as written |
| `lib_bf3f.py` | the predicate, the two resolvers, the declared bounds |
| `verdictwatch.py` | **the deliverable.** exit 1 while drops exist, `--json`, `--since`, `--all` |
| `d1_population.py` | the census; the 21-item false-positive control; every filer |
| `d2_cause.py` | the discrimination; Fisher exact; the routing of the result channel |
| `d3_fire.py` | the verdict dropped on purpose, through the real `mg` binary |
| `d4_live.py` | the live fire on this ticket's own verdict; the backlog; mg-ec63 recovered |
| `selftest_bf3f.py` | regressions for defects 1 and 5; the mutation test |
| `run_all.sh` | 6 declared exit codes; writes transcripts outside the tree and moves them in after the last probe exits |

`run_all.sh` refuses to start if `BF3F_RUNNING` is inherited, and names the
caller — mg-ec63 recorded that this arc's own probes execute any `run_all.sh`
they find, and that two runners in one directory share their `out_*.txt` paths,
which produced a zero-byte transcript beside a non-zero exit.

---

## WHAT I DID NOT DO

- **I did not repair the cause.** It is one line in pm-onethird's ticket template
  plus mayor's `--result` channel. Shipping one from a polecat worktree and
  leaving the other is precisely the failure this ticket warns about.
- **I did not check mg-790f or the partial-spawn cleanups.** mayor offered them.
  No dropped verdict in this population traces to either, and I did not conflate
  a different question with this one. Named so it can be asked properly.
- **I read no mailbox but** `pm-onethird`, `mayor`, `human`, `daniel` and
  `daniel-creator`, and the last three only for the `for Daniel` question.
- **mg-ec63 is recovered but not re-audited.** Its verdict is in one commit,
  7fccb4e; I report where it is and what it says, not whether it is right.

## ONE CORRECTION TO THE TICKET'S FACTS

The `for Daniel` deliverable (6ed98c4 / mg-69be) **did** reach Daniel.
pm-onethird relayed it to the `human` mailbox by hand at 2026-07-15T17:24:22Z,
37 minutes after mayor's merge notice. Its polecat sent zero mail of any kind,
and the item was filed by `daniel`, not pm-onethird. The deliverable arrived; the
mechanism did not deliver it. That is a smaller failure than the ticket assumes
and it is worth saying, because the by-hand relay is the thing that worked.
