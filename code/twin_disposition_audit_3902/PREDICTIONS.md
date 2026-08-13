# mg-3902 — PRE-REGISTERED PREDICTIONS

Filed before any file under audit is opened. Written after reading, and ONLY after
reading: (a) the mg-3902 ticket body including its 2026-08-13 recurrence addendum,
(b) `mg show mg-ea0e`, (c) `git log --oneline` subject lines for
`docs/state-of-the-wall.html`, (d) `ls code/rendered_twin_pin_9bc2/`.

## EXPOSURE — disclosed, not laundered

The commit subjects in (c) are unusually long in this repo and they carry conclusions,
not just labels. Reading them told me the disposition before I filed a single bet.
Specifically, `9efb3df` says in its own subject line:

    THE TWIN WAS NEVER GENERATED — `Generated 2026-07-19` WAS FALSE IN BOTH HALVES,
    and the ticket's own premise for deleting it EXPIRED FOUR DAYS AGO: STATE.md is
    110,640 bytes and 16,861 words, NOT the 32,772 / 4,658 the ticket quotes ...
    Pinned per ledger row instead

So **R1–R3 below are REPORTS at zero credit.** I am not betting on them; I am recording
that I knew them before starting, so that a later reader cannot mistake them for
findings. Anyone scoring this file should score P1–P8 only.

### R1 (REPORT, zero credit)
The parent is **mg-9bc2**, not mg-ea0e. mg-ea0e is the STATE.md executive-summary
overhaul; mg-9bc2 is the ticket that was actually asked to dispose of
`docs/state-of-the-wall.html`, and it quotes the same `4,658` word count my own ticket
quotes.

### R2 (REPORT, zero credit)
The parent chose **NEITHER** of my ticket's two branches. It did not regenerate and it
did not delete. It kept the file and added a **per-ledger-row pin** with a checker at
`code/rendered_twin_pin_9bc2/`.

### R3 (REPORT, zero credit)
The parent found that the file's `Generated 2026-07-19` line was **false** — there was
no generator; the page was hand-built. My ticket's deliverable-3 anticipated exactly
this and it is therefore not a discovery of mine.

## LIVE BETS

**P1 (0.90) — MY TICKET'S FRAMING IS THE PRIMARY DEFECT, AND SO IS MY PARENT-TICKET'S.**
The ticket presents a binary (regenerated / deleted) and instructs the auditor to pick a
branch. The actual disposition is a third thing, and the third thing is *better* than
either branch. An audit that files under IF-REGENERATED and grades the pin as a
half-hearted regeneration would be scoring the parent against a menu the parent was
right to refuse.

**P2 (0.85) — THE `4,658 words` PREMISE IN MY OWN TICKET IS STALE BY MORE THAN THE
PARENT SAID.** The parent measured 16,861 words in July. Commits on `main` this month
mention a word ratchet at 21,328. If STATE.md is now >20k words, my ticket's deliverable
6 ("decide whether the file should exist at all, given STATE.md is now 4,658 words")
rests on a number that is wrong by a factor of about 4.5 — and the *direction* of the
error reverses the deliverable's implicit recommendation. I predict I will measure
STATE.md at >20,000 words.

**P3 (0.75) — THE STALENESS CHECK IS REAL AND WILL GO RED WHEN I MUTATE STATE.md.**
Deliverable 2 demands I make it fail. I predict it fails correctly on a one-line edit to
a *pinned* row. I split out the harder half as P4.

**P4 (0.55) — THE CHECK HAS A BLIND REGION AND MY MUTATION WILL FIND IT IF I AIM AT AN
UNPINNED ROW.** `COVERAGE.md` exists, which means the instrument's authors wrote down
what it does not cover. A checker with a declared uncovered region will pass a mutation
aimed into that region. I predict: mutating a pinned row → RED; mutating prose the pin
does not digest → GREEN, silently. Both are correct behaviour for what it is, and both
must be reported, because "the staleness check passes" means nothing without its scope.

**P5 (0.70) — THE DISPLACEMENT QUESTION HAS A DIFFERENT SHAPE HERE THAN MY TICKET
ASSUMES.** Deliverable 1 says "verify the HTML matches STATE.md AT THE COMMIT THE HTML
NAMES." I predict the page names **more than one commit** — one per pinned row, not one
for the page — so there is no single "the commit the HTML names", and the displacement
question has to be asked per row. I further predict at least one pin points at a commit
that is **not an ancestor of main's tip** or is otherwise unreachable/rewritten, because
`7e7bfb7`'s subject says a rebase already destroyed one pin target once.

**P6 (0.65) — THE WORD "Generated" STILL APPEARS IN THE FILE.** Deliverable 3 asks me to
confirm it is gone unless true. `cdec2e8`'s subject quotes a live string
`<!----><span><b>Generated</b> 2026-08-10</span>` from this file, dated a month after the
parent landed. I predict the word is present, and that it is now *true* in a narrow sense
(a date stamp maintained by hand or by the pin tooling) while still being the word most
likely to be misread as "this page was produced from STATE.md by a program". Being
present is not by itself a defect; being present without a generator is.

**P7 (0.60) — THE RECOMMENDATION WAS ARGUED, AND THE ARGUMENT IS BETTER THAN THE ONE MY
TICKET ASKED FOR.** Deliverable 6 wants a stated reason. I predict the parent stated one
and that it is empirical rather than aesthetic: the readability problem the page exists
to solve came *back* when STATE.md regrew. I also predict the argument has since gone
stale in its own way — the reason was pinned to a word count that has moved again.

**P8 (0.50) — THE DELIVERABLE REPRODUCES ITS OWN DEFECT CLASS, AND I WILL TOO.**
Standing target. A staleness fix that goes stale. `a1d43b0` (mg-c824) landed days ago
finding "64 instruments, 98 transcripts, 40 of them ALREADY STALE". I predict the pin
instrument's own committed `out_*.txt` transcripts are stale against the tree they
describe — i.e. the check's *record of having passed* is older than the file it checked.
And I predict my own audit document will contain at least one number that is stale at the
moment it lands, because I am writing it against a moving `main`; I will name which.

## THREE CONDITIONS FOR REVERSING MY OWN VERDICT — filed in advance

1. If the pin check cannot be made to fail at all, the disposition is **worse** than
   deletion would have been, because a page that advertises a check nobody has seen fail
   is a stronger false assurance than a page with no check.
2. If any pinned commit is unreachable from `main`, the pin is a **claim about a commit
   that does not exist**, and that is the same defect class as the `Generated` lie the
   parent repaired.
3. If a live link to the file exists in a doc that would 404 on deletion, that is
   evidence FOR the parent's keep decision independent of any readability argument, and
   I must say so even though my ticket only asked me to check links under IF DELETED.

## WHAT I DO NOT EXPECT TO ESTABLISH

- Whether the page is *useful to a reader*. I can measure whether it is accurate. I have
  no instrument for whether anyone reads it, and I will not dress a preference as a
  measurement.
- Whether the hand-built page's prose is a faithful *summary* of STATE.md's prose. The
  pin digests named rows. Everything outside those rows is unchecked by the instrument
  and unchecked by me except where I read it by eye, which I will label as such.
