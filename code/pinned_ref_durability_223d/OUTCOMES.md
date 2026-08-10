# mg-223d — OUTCOMES

`PREDICTIONS.md` was committed at **`5712984`**, in its own commit, before one
line of `lib223d.py` existed. Nine disclosures (`H1`–`H9`) are kept in it as
**measurements** rather than laundered into predictions — including `H6`, which
is the whole population sweep. This ticket's honest exposure is large and it is
on the page.

## THE PREDICTIONS

| | bet | p | verdict |
|---|---|---|---|
| **P1** | ≤3 reconstructions in the arc; only mg-9160's is exposed | 0.75 | **HELD, with its limit stated** — 1 found, and it is mg-9160's. The final rule is a **reading** rule; what is automated is only the necessary condition (a file pinning ≥2 commits). That is D8's shape and is why this is not a clean hit. |
| **P2** | the on-main twin is NOT a substitute; ≥1 of 517/1191/246/626/400 moves | 0.92 | **HELD, and bigger than the bet** — **all five** move: 517→537, 1191→1226, 246→249, 626→630, 400→404. |
| **P3** | a tag survives `gc --prune=now`, an untagged branch-held commit does not | 0.85 | **HELD on the claim, MISS on the sub-prediction.** Exhibited in a throwaway clone. The sub-prediction that I would have to *defeat the reflog* is a **MISS** — the untagged commit died in arm 1 as well (D7). What I had to defeat instead was **my own repair** (D12). |
| **P4** | nothing in the arc is dead yet | 0.80 | **HELD** — 26 of 26 still resolve. |
| **P5** | the wide population is mostly false positives; genuine count <60 | 0.70 | **LOST, AND NOT RESCUED.** 0 of 600 random 7-hex tokens resolve; 0 of 600 at 8; 0 of 600 at 12. Essentially all 381 are genuine references. |
| **P6** | the tags are not durable until pushed, and saying so is the real cost | 0.88 | **HELD** — the refinery merges branches and not tags; `R4d` had to make both `26`. |
| **P7** | zero directories declare a reachability dependence | 0.65 | **HELD as stated** — 87 *mention* reachability under a deliberately generous rule; **0** declare one, and none is checkable. |

**HELD 6, LOST 1.**

### THE ONE THAT LOST IS THE ONE THAT SHAPED THE REPORT

P5 was my defence against over-reporting, and it was a **bad defence**: it said
the big number was fake. The big number is real — 381 non-ancestor commit
references exist in tracked files and nearly all of them are genuine. What keeps
381 out of the headline is a **different claim**, which I had to make after the
fact: 354 of them are **records** and not **dependences**. A dead record is a
claim you can no longer check; a dead pin is a program that no longer runs.

That is mg-f8e5's *"named the right transcript for the wrong reason"*, committed
again one ticket later, by an author who had read it. It is D2.

## THE ERRORS FILED IN ADVANCE, AND WHICH ONES I COMMITTED

| | filed as | what happened |
|---|---|---|
| **E1** | my population rule is quoted literals in `*.py`/`*.sh` and cannot see a constructed ref | **STANDS, and is reported as D10.** `27` is a floor with no upper bound. |
| **E2** | I double-count tokens as commits | **COMMITTED — in the repair itself.** `tag_name` first took the token, so one commit got two tags. D3. |
| **E3** | my tags become provenance nobody authorised | **AVOIDED** — `pin/` prefix, an annotation body that says "anchor, not endorsement", and PINS.tsv's header. Mitigation, not a fix, and R4b says so. |
| **E4** | I "repair" a pin by re-pointing it at its twin and silently move a figure | **AVOIDED, and the cost measured instead.** R3c prints both rows. All five columns would have moved. |
| **E5** | my gc exhibit passes for the wrong reason (reflog) | **RIGHT KIND, WRONG SOURCE — and it happened.** The reflog guard was unnecessary (D7). What actually poisoned the exhibit was **my own repair**: tag auto-follow carried `pin/d33970b` into the sandbox and the untagged control went false-green (**D12**). |
| **E6** | I declare durability I have not got | **AVOIDED** — R4d measures local and origin separately. |
| **E7** | my reachability check counts my own branch | **AVOIDED** — `holders()` excludes it by default, and `r0`'s C4c shows the answer changing (1→0) when it does not. |
| **E8** | I treat "has a twin on main" as "safe to lose" | **AVOIDED** — R2c names six directories where the pre-rebase commit **is** the subject. |
| **E9** | I promote the reconstruction to an instrument while repairing it | **AVOIDED** — R4e and R3d. All four of cfd9c's limits are still true. |
| **E10** | I count `refs/heads/*` in this worktree as durable | **AVOIDED** — `durable_holders()` counts only tags and `main`. |

**Two errors I filed were committed** (E2, and the P5 reasoning that was not on
the E-list at all). **Two I did not file and committed anyway:**

- **D11** — running my own damage check against a *growing* `main` instead of
  the merge base, which is `audit_c067`'s exact defect committed inside the
  report that cites it.
- **D12** — the repair contaminating the exhibit that proves the repair works.
  E5 was pointed at the right *kind* of contamination and the wrong *source*: it
  watched the reflog, and the poison was my own 26 tags.

## THE HAND MEASUREMENTS, RE-STATED AS SCORED OR NOT

`H1`–`H9` are not scored and were never eligible to be. They are listed here so
that a reader can see how much of this tree's output was already in my hands
when I wrote the predictions: **the entire code population sweep** (H6, giving
26 and the branch-holder table) and **the twin mechanism** (H4, H5, which was
already in `idiom_sweep_audit_18dc`). What the predictions actually bet on was
the *consequence* of those measurements — whether the twin substitutes (P2),
whether a tag saves it (P3), whether the wide number was noise (P5), and whether
tagging alone is durable (P6).

## WHAT THIS TREE DID NOT SETTLE

- **`27` is a floor.** No rule here can see a rev built by concatenation, read
  out of a `.md` at run time, or taken from `argv`. D10.
- **The 6 "subject" directories are a hand list.** No rule stands behind the 6,
  so no rule could have returned 7. D8.
- **Whether all 26 pins are worth keeping** is a reading of 13 directories by
  their owners. The tag makes the decision reversible in the direction that
  matters: a tag can be deleted; a collected object cannot be restored.
- **The 354 records are untouched**, deliberately. Their remedy is to be
  readable, not to be tagged.
