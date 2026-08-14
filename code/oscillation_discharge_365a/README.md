# mg-365a — was the oscillation discharged, and by what?

The ticket asked for **a command, not an argument**. This is the command.

Its two questions are answered below, and **both answers differ from what the ticket expected**.
The ticket is not careless: it was filed at 03:30Z from a commit taken *before* `bd07d70` landed
at 00:41Z, and it describes a constant that no longer exists.

```
sh run_all.sh          # ~20 s, two transcripts, no clock and no randomness
```

---

## §1 The premise is stale, and that is the first finding

The ticket says, in the present tense:

> `out_g0_fixed_point.txt` **is** mg-f771's single self-exemption

`lib_f771.SELF_EXCLUDED` was **deleted** by `bd07d705` (mg-c15e), *nineteen minutes after the
commit the ticket was written from*. d1 §1 checks this **in both directions** — present at
`DELETION~1`, absent at the pin — because an arm that only checked for absence today would pass
identically against a repository that never had the constant, and would be reporting on its own
inability to find a string.

The mayor's own caution of 00:22Z is written on this ticket:

> a successor carrier filed while its cause was live can outlive the cause, and derived work can
> be discharged by the fix rather than needing its own slot.

**That caution was correct, and this directory is its measurement.** The remainder mg-585e
declared was discharged by mg-c15e before this item was ever staffed.

## §2 Question 2 — discharged, but not by what the ticket asks about

Carry-forward item 2 asks whether this is *"already discharged by mg-05c6"*.

**Yes discharged — no, not by mg-05c6.** `65c647bf`, mg-05c6's own refresh, is **solo commit #8
in the population it was asked to have removed**. It *paid* the toll; it did not remove it. The
discharge is `bd07d705`, mg-c15e's.

That distinction is not pedantry. An instrument answering "yes, discharged" without saying *by
what* would have confirmed the ticket's question while getting its subject wrong, and sent the
next reader looking for the mechanism in the wrong file.

### What carries it: **6 owed, 0 paid**

`0 of 8 landings touched the transcript` is **not enough on its own**, and d1 §4 says so out loud:
at mg-585e's measured pre-deletion rate (30 touches / 129 code/ commits) eight quiet landings has
probability **0.12**. A directory resting on that zero would be reporting a quiet window as a repair.

What makes it a repair is the counterfactual:

> `./build.sh` regenerates transcripts into the worktree and **then** g0 compares worktree against
> HEAD — so the old §2's disagreement set `D(T)` **contains** every watched transcript the landing
> went on to commit. A landing that committed one *provably* had `D(T) ≠ {}` and would have owed a
> refresh.

| since `bd07d705` | |
| --- | --- |
| main landings | 8 |
| that would have **OWED** a refresh | **6** |
| that touched the transcript at all | 0 |
| that **PAID** a solo refresh commit | **0** |

Transcripts graded NOISE or CORPUS are *restored* rather than committed, so they never enter this
count — it is a **lower bound**, which is the safe direction for a claim that a toll was owed and
not paid. The watched class is `lib_f771.is_watched` **imported**, and the corpus-scoped registry
`lib_f771.CORPUS_SCOPED` likewise, because a re-typed glob is a re-statement and a re-statement drifts.

## §3 Question 1 — self-inclusion was a property of the exemption, not of counting

Question 1 asks whether a self-inclusive count is a defect or the only truthful arrangement. It is
**neither, and it is already gone.**

The counting directory joined the population it counted because **counting required a `./build.sh`
run, and a `./build.sh` run moved that transcript**. Nothing about *counting* made the count
self-inclusive — the oscillation did, and it captured every branch equally. mg-585e was not
special; it was the 9th.

With the exemption deleted, the transcript is a function of `lib_f771.py`'s source, so a landing
that does not touch that file does not move it. **A directory can now count the population without
entering it** — and this one does: `out_g0_fixed_point.txt` is untouched by this branch. That
reading is a property of *this branch* rather than of the pin, so it is on **stderr** and not in
the transcript (README D4). A branch-dependent figure inside a pinned transcript is the defect this
whole arc is about, arriving one file over.

## §4 The number the ticket publishes is off by one, and the mechanism generalises

Both `15af11d3`'s own commit message and this ticket call it **"the 8th"**. Re-walking puts it at
**#9**.

`8` is `7 + 1`: mg-585e's figure **at its pin** `0cb0fa4`, incremented rather than re-walked.
`65c647bf` — mg-05c6's, sixteen minutes earlier — landed between the pin and the claim. The
arithmetic was right; the pinned figure had stopped being current.

> **A count derived by incrementing a pinned figure is wrong exactly when something landed in
> between, and it is wrong silently, because the arithmetic is right.**

d1 §2 re-derives mg-585e's `7` **at mg-585e's own pin** and agrees, which is what makes the
disagreement a finding about the *method* rather than about the walker. The population also grew
**7 → 10** after publication.

## §5 The trap in the figure a reader will reach for — **and my own prediction about it was refuted**

mg-585e's headline was `16 of 31 RED`. Its predicate tests for `DISAGREEMENTS, SHOWN` on a `§2`
line. **`bd07d70` deleted that heading.**

**P2 predicted re-running that predicate at this pin would report 0 RED. It reports 3.** Six of the
seven new versions *pre-date* the format change, still carry the old §2, and the predicate reads
them exactly as mg-585e intended. The prediction confused *since mg-585e's pin* with *since the
deletion*, and they are six versions apart. The section was rewritten to what ran.

**The trap is real and is latent rather than exhibited** — a weaker claim than P2 made, and the one
the record supports. Exactly **one** version exists under the new §2 (`bd07d70` itself) and n = 1 is
not evidence about a predicate. What *is* certain is structural: no version written after the
deletion can carry that string whatever the gate did. So the zero is owed to the **next** reader:
the moment a version lands after `bd07d70`, re-taking mg-585e's headline figure returns a zero that
measures a deleted marker and reads as *"it stopped"*.

It is printed rather than omitted precisely because anyone can re-derive it in one command, and an
omitted trap is a trap the next reader walks into alone.

## §6 The controls, and why they are the point

d1's entire finding is a **zero**, and a zero is what a broken instrument returns for free — an
empty walk, an unresolvable pin, a watched-class predicate narrowed until it matches nothing. d0
runs **first** for that reason.

| world | | |
| --- | --- | --- |
| D1 | CAUGHT | an empty history REFUSES rather than reporting 0 |
| D2 | CAUGHT | a pin that does not resolve REFUSES |
| D3 | CAUGHT | a pin that *resolves* but is not an ancestor of `origin/main` REFUSES |
| D4 | CAUGHT | `is_watched` narrowed to nothing collapses OWED 6 → 0 |
| D5 | **INERT** | widening `is_watched` cannot *remove* a commit from OWED |
| D6 | CAUGHT | the solo predicate loosened to `≥ 1 file` inflates 10 → 38 |
| D7 | CAUGHT | the corpus-scoped filter is exercised, **or its silence is named** |
| D8 | **INERT** | two consecutive d1 runs are byte-identical |

Both directions are run. A plant that makes everything red proves nothing, so two worlds are
**required-inert**, and the clean library is asserted green before *and after* every plant — no
plant mutates a module (each passes a predicate as an argument), and that re-measurement is what
says so rather than the design saying so.

**D7 is one-directional and says so.** Dropping the corpus-scoped filter changes nothing *today*,
because no landing in this window committed the one corpus-scoped transcript. That is a fact about
the window, not about the filter, so the world records `does not bind here` rather than claiming a
pass — and it starts binding the day a second path is registered.

**D3 can be unreachable rather than passing.** It plants a *real* commit that resolves but is not
on `origin/main` — this branch's own HEAD. If this branch had no commit off `origin/main`, the world
is marked unreachable instead of quietly passing.

## §7 Scope — what this directory does not do

* **It edits neither `code/verdict_invariance_585e/` nor `code/gate_fixed_point_f771/`.** Both are
  imported read-only. That is not tidiness: mg-585e's transcripts are pinned, and touching either
  would cost a refresh commit — which, in the directory whose subject *is* refresh commits, would
  be the eleventh instance filed by the arm that counted ten.
* **It is not in `build.sh`.** Nothing consumes these transcripts and the subject is a question put
  to pm-onethird, not a property the gate must hold. A measurement that is binding by the back door
  is not a measurement.
* `STATE.md` untouched, so the ratchet is untouched and no twin re-pin is owed. `docs/FACTS.md` gets
  no entry (mg-3da1's homelessness test — every measurement here is consumed by this landing) and
  `docs/CONCEPTS.md` no row.

## §8 What is left

Successor **mg-9c46**, filed before this branch merged. The remainder is *not* this file's subject
— it is §4's mechanism, which is general and has no detector:

> a published count derived by **incrementing a pinned figure** is wrong exactly when something
> landed between the pin and the increment, and nothing in this estate detects it.

This directory found one instance by hand, in the one place it happened to look. Whether there are
others is unmeasured, and the population — every prose or commit-message figure quoting a pinned
count — is not enumerated anywhere.
