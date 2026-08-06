# mg-5035 — `figures()` now excludes a git revision, which it claimed to and never did

**Object.** `lib7522.figures()` — the arc's rule for *is this number a FIGURE, a
measurement that must be backed by a transcript?* `mg-70c7` shipped it under a
comment listing **"a git revision"** among the things it excluded. It never did.
`mg-bf79` hit that against its own output, diagnosed it, and deliberately left
it unfixed. `mg-5035` fixes it.

Predictions committed before any script of this repair existed:
`PREDICTIONS.md`, at the commit before `lib5035.py` appears in the tree.

---

## FIRST, THE TICKET'S FRAMING IS STALE, AND CORRECTING IT CHANGES THE JOB

`mg-5035` says *"`figures()` claims **in its own comment** to exclude a git
revision"* — present tense — and offers two branches: fix the exclusion, or fix
the comment.

**There is no such comment at HEAD.** It died with `lib70c7`'s old body when
`mg-bf79` landed `675c2ba` — *the same commit that reported the finding*. So one
branch was already taken, silently. What the arc was actually carrying was
**the defect with the false claim removed**, which is worse than either: a reader
had nothing left to disagree with, and the only surviving mentions were two
`OUTCOMES.md` files correctly calling the claim false.

So the decision between the ticket's two branches is **forced by a measurement,
not taken by reflex**: the comment cannot be the thing to fix because it does not
exist. **The code is what is wrong, and the code is what this ticket repairs.**

---

## THE RULE, AND WHY IT IS NEITHER OF THE TWO mg-bf79 REJECTED

`mg-bf79` weighed a **magnitude** rule (`drop ≥ 1e6`) and a
**resolves-as-a-git-object** rule, measured both, and rejected both. Both
rejections hold, and one of them gets stronger here:

* **Magnitude.** This corpus contains `431723379 labelled posets`, `2147483647`
  (an INT_MAX in a fixture), `1103515245` (an LCG multiplier) and
  `33554432 relations`. A magnitude rule drops every one. *A generous exclusion
  list turns an unbacked figure into a non-figure* — `lib70c7`'s own sentence.
* **Resolves-as-an-object.** `mg-bf79` called this *an accident of the object
  database*. The sharper objection is that **its answer changes as the database
  grows**: the same document would be censused differently on different days. In
  an arc built on re-derivation that is disqualifying.

**Shipped instead: a DECLARED-revision rule.** A token is excluded only when it
is *both*

| half | what it is | why it is not enough alone |
|---|---|---|
| **shape** | 7–40 decimal digits, no separator | the four genuine figures above all carry it |
| **declaration** | the line **names** it a revision — `at`, `commit`, `carried by`, `git rev-parse`, `landed at`, … | a cue with no shape is just a word |

Walking left from the token, fillers (`by`, `to`, `is`, …) and **sibling
revisions** are skipped, so `git rev-parse on 973ca61, 645b5a4, 3942319` declares
all three. The first other word decides.

This is **the same kind of rule `figures()` already had.** Every pre-existing
exclusion — `:`-prefix, `#`-prefix, `lines N` — is contextual, not numeric. The
repair adds a fourth contextual exclusion rather than a new kind of one.

**The git object database appears in this tree only as an EVALUATION ORACLE for
scoring. `lib7522.figures` never calls git.** Keeping those two apart is the
whole reason the objection above does not land on me.

---

## WHAT WAS MEASURED

| probe | question | answer |
|---|---|---|
| **F1a** | is a **constructed all-decimal** short revision excluded? | **10 of 10.** Three of them name no object in this repository, which is the point: the rule reads text, so a revision that does not exist yet is excluded exactly like one that does. |
| **F1b** | are genuine revision-shaped **figures** still figures? | **8 of 8 kept**, `431723379` and `2147483647` among them. |
| **F1c** | precision / recall over every tracked `.md`/`.txt`/`.py` | **14 of 50** distinct shaped tokens excluded; **10** resolve, **4** do not — and all four of those are lines naming a revision this repository does not contain, so the oracle is wrong on all four, not the rule. Every one of the 4 is printed by file and line. |
| **F1d** | what does the rule **not** reach? | **10** resolving tokens, **5** of them bare fixed-width table columns with no word to their left. Named, not hidden. |
| **F1e** | can this instrument show the defect? | mg-56dc's untouched copy still reads **10 of 10** as figures. F1a is a difference, not a tautology. |
| **F2a** | the contamination, with its denominator | **48 of 86,750** numbers stop being figures — **0.055%** — across **18 of 1,535** tracked files. This tree is EXCLUDED from that population: its own transcripts print declared revisions as evidence and contaminate the census (a further **55**, counted separately). |
| **F2b** | the dangerous direction: was a figure **backed only by a revision**? | the backing corpus loses **1 of 1,494** integers (`478508621408`), and **0** claim lines in the arc were acquitted by it. |
| **F3** | already-corrupted published output | **the one recorded instance was never committed as a count**, and its inflation was removed by **editing the prose, not the rule**. |
| **F4a** | did the arc's tripwires fire? | **2 of 2**, proved by re-running the old assertions, not asserted. |

### Populations and grains

Every count above is over a stated population at a stated grain, and every count
row in the transcripts carries its grain on the line beneath it. *One unit* is,
respectively: one file, one number on one line, one distinct token, one distinct
integer, one selftest case. Where a number is repeated from another agent it
says so — `mg-bf79`'s `1284 / 31 / 6` is **mg-bf79's, over mg-bf79's population,
at mg-bf79's commit**, and F2d re-derives the same three at HEAD both ways rather
than comparing across populations.

---

## THE HONEST HEADLINE ON DAMAGE, WHICH IS SMALLER THAN THE TICKET ASSUMES

The ticket asks whether a published figure was inflated by a counted revision,
and notes correctly that an arithmetic fix does not retract a published number.
**Searched, and here is what is there:**

1. **The one recorded corruption was never published.** `r6_self.py` exited 1 for
   exactly one run, on `UNBACKED README.md 3738079`. That run's transcript was
   never committed. `r6_self.py` exits 0 at HEAD.
2. **It was papered over, not fixed.** `mg-bf79`: *it exits 0 again now, because
   the prose no longer names an unstable revision.* Confirmed — **0**
   revision-shaped tokens remain in `mg-70c7`'s README. The workaround is what a
   reader would have had to notice to know the rule was still wrong, and nothing
   said so.
3. **4 committed transcripts would read differently** if re-run — in `mg-97fb`,
   `mg-f922`, `mg-3f3b` and `mg-1abe`. **None of them publishes a figure count
   computed by `figures()` over its own text.** They are lines that *name* a
   revision.
4. **2 `docs/` files** carry a revision a census would have counted — **and this
   refutes my own P3c.** `figures()` never ran over `docs/`, so no published
   human-facing number is wrong; the claim the evidence supports is the smaller
   one, that it *would* have been.

So: the defect was real, was reported, was left live for a whole ticket, and its
**published** damage is one uncommitted non-zero exit. Saying that plainly is the
point — overstating it would be the same failure as the comment that started it.

---

## WHAT WAS NOT DONE, AND WHY

* **No other tree's committed transcripts were regenerated.** Those transcripts
  are the evidence F2 and F3 measure; rewriting them to agree with a rule I
  changed would destroy it. The four that would move are listed by name.
* **`lib56dc.figures` was not repaired.** It is the positive control, and
  `f4_self.py`/F4c checks every run that it still is.
* **The bare-table-column gap was not closed.** Every candidate rule for it
  (column position, hex neighbours) keys on layout rather than on meaning, and
  the one place it matters most — `UNBACKED README.md 3738079` in mg-bf79's
  transcript — is a *record of the defect*, where firing would erase evidence.
* **`figures()` still has 3 definitions in the arc**, and that is the intended
  number: one implementation (`lib7522`), one forwarder (`lib70c7`), one
  independent control (`lib56dc`). This tree defines **none**.

## Files

| file | what it is |
|---|---|
| `PREDICTIONS.md` | committed before any script here existed |
| `lib5035.py` | shared instrument; imports both rules, implements neither |
| `selftest5035.py` | 27 cases, half of them asserting the repair does **not** fire |
| `f1_rule.py` | the rule scored in both directions |
| `f2_contamination.py` | claim side and backing side, with denominators |
| `f3_published.py` | the hunt for already-corrupted output |
| `f4_self.py` | this tree held to its own standard |
| `OUTCOMES.md` | predictions scored, including the misses, and this instrument's own defects |
