# mg-688c — DID ANYTHING DESCEND FROM THE SUPERSEDED READINGS?

The instrument behind `docs/OneThird-SupersededDescent-mg-688c.md`.

mg-cdd5 found the `main-mirror` checkout 76 commits behind, repaired it, and reported that
4 of 6 `STATE.md` citations had been resolving into superseded text — 3 of them **struck**.
Its remedy makes those citations resolve correctly **from now on**. It says nothing about
what was read while they did not. That is this ticket.

**Verdict: NOTHING DESCENDED — with two stale reads caught, and neither of them read
withdrawn text.** The numbers, the populations and the limits are below and in the four
transcripts.

---

## THE PIN — read this before quoting any figure here

Every revision-dependent number in this directory is measured against

    one_third_width_three  origin/main = 949c43926b6eab9dfbd606b063992e2d7d2ea0ae
    one_third_width_three  main-mirror at the time of the defect = 912f1b1

**If `origin/main` moves, these transcripts go stale — which is the defect they are about.**
Re-run rather than quote. `run_all.sh` takes about four minutes.

This is not a formality. mg-cdd5 wrote the same pin for the same reason, and the reason is
that an instrument about superseded readings is exactly the kind of artifact that becomes a
superseded reading.

---

## WHAT IT MEASURES

| step | question | transcript |
|---|---|---|
| `s0_window.py` | when did the mirror last match `origin/main`, and for how long was each withdrawn claim dangerous? | `out_s0_window.txt` |
| `s1_delta.py` | for each affected citation, what did the STALE text say and what does the CURRENT text say? | `out_s1_delta.txt` |
| `s2_descent.py` | did anything cite, quote or reason from the stale reading? | `out_s2_descent.txt` |
| `s3_controls.py` | can the detector fire at all, and what are its blind spots? | `out_s3_controls.txt` |

## THREE DESIGN RULES, AND WHY EACH IS FORCED

**1. Nothing is read off a working copy.** Every revision-dependent fact comes from
`git show <rev>:<path>`. The mirror checkout is now REPAIRED: reading it would answer with
the current text on both sides of the comparison and the whole delta would come back empty.
A sweep about a stale checkout that reads a checkout is the defect it is about.

**2. The window is per-claim, not global.** A document written on 2026-08-01 quoting `0/132`
bare did not read withdrawn text — the withdrawal landed 2026-08-07. Each struck claim
carries its own hazard window, opening at the **push** that made its withdrawal fetchable.
`s3` X5 prices this rule: it excludes **177 of 242** occurrences in the commit population.
Without it the sweep reports 242 candidates, of which 177 have to be argued away one at a
time by hand — a zero drowned in noise it created itself.

**3. The population is named before any count**, and a zero is reported only next to the
population that produced it.

## THE FOUR POPULATIONS

| | population | in scope | swept |
|---|---|---|---|
| POP-A | `onethird_program` commits, **added lines only** | 544 of 573 | fingerprints |
| POP-B | macguffin work items, `[created, last-written]` overlapping a window | 1,469 of 5,100 | fingerprints |
| POP-C | macguffin mail | 11,573 of 30,364 | fingerprints |
| POP-D | line anchors into the four affected documents, at HEAD | 2,756 files | resolution at both revisions |

POP-A/B/C detect a claim being **repeated**. POP-D detects **the act of reading** — a line
number that resolves at `912f1b1` and not at `origin/main` can only have been copied out of
the stale copy, whatever words surround it. It is the only test here that does not depend on
an author reusing the claim's wording, and it is the one that actually found something.

## A FINGERPRINT HIT IS NOT A DESCENDANT

Most traffic about these claims in this programme **is the withdrawal propagating**. 124
fingerprint occurrences; 109 carry a withdrawal marker within 400 characters. The 15 that do
not are printed in full in `out_s2_descent.txt` and adjudicated by hand in the report — none
is a descendant, and the reasons are one line each.

The marker list is deliberately generous, which biases toward `CARRIES-WITHDRAWAL` — the
wrong direction, because it shrinks the pile that gets read by hand. `s3` X2 controls for
exactly that by planting withdrawal-marked sentences and requiring them to classify as
withdrawn, and X1 plants bare ones and requires them to survive as `BARE`.

---

## THIS INSTRUMENT IS SUBJECT TO THE DEFECT IT REPORTS

A remedy is an artifact of the same kind as the defect. Enumerated, and checked:

1. **It pins a moving ref.** Same defect, same shape. Mitigated only by saying so at the top
   and by `run_all.sh` being cheap. Not solved.
2. **It caches a remote's push history** (`data/push_events.json`). GitHub retains the events
   feed for about 90 days; the cache is what makes the window boundable to the second after
   that lapses, and it is also a snapshot that cannot be re-derived once it does. Captured
   2026-08-12; provenance recorded in `lib688c.push_events`.
3. **It quotes line numbers into the affected documents.** Every one is stated as measured at
   `949c439`, and the repair table in `s2` gives content-matched targets rather than
   arithmetic offsets — so a reader can re-find the text rather than trust the integer.
4. **It contains synthetic occurrences of every struck claim** — twice each in the claim
   table, five more planted in X1. Swept as corpus it is the largest cluster of bare
   assertions of withdrawn text in this repository (57 occurrences, X6). Excluded by name,
   and the exclusion is measured rather than asserted. mg-cdd5 hit this and excluded its own
   24 files; its directory is excluded here for the same reason, because its transcripts
   quote mirror-era anchors **as data**.
5. **It reads the citing repository's working copy** for POP-D, not `git show HEAD:`. That
   worktree is this branch and is clean apart from this directory, which is excluded; the
   inconsistency is real but bounded, and it is recorded here rather than hidden.
6. **One of its own fingerprints is blind.** `946` survives verbatim in the CURRENT text
   (the correction was landed as a banner above the sentence, not as an edit to it), so a
   bare `946` is not evidence of a stale read. X4 exists to say so out loud, because without
   it the two 2026-07-30 mails that quote `946` would sit in the report looking like the
   closest thing to a finding.

## WHAT THIS CANNOT ANSWER

The sweep is **fingerprint-based**. It finds a descendant that reuses a claim's wording or a
line number. It cannot find one that consumed a withdrawn reading and wrote it in words that
share nothing with the original — nor one that lives in a conversation that left no artifact
on this machine. POP-D narrows that gap because a line anchor is wording-independent, but it
does not close it. **The zero is a measured zero over four named populations, not a proof
that no reader was ever misled.**
