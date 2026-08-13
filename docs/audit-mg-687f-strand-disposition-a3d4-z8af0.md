# DISPOSITION of two unmerged polecat branches — `polecat-a3d4` and `polecat-z8af0`

**Work item:** mg-687f (filed by mayor 2026-08-10 on pm-onethird's behalf)
**Established by:** mg-687f, 2026-08-13
**Instruments:** `git cherry`, blob-identity against `origin/main`, `git log -S`, and
`~/.pogo/events.log`
**Scope, unchanged from the ticket:** establish the disposition. **No work-loss claim, no
merge, neither branch submitted to the refinery.** Acting on this is pm-onethird's call.

---

## VERDICT

| branch | disposition | why |
|---|---|---|
| `polecat-a3d4` | **(a) landed — and the branch ITSELF merged** | MR `mr-d9lbnmitjv1tur4p9b9g`, merged 2026-07-30T02:54:15Z as `2919d28` |
| `polecat-z8af0` | **(a) content landed — via a SIBLING polecat — with one named residual** | `polecat-x8af0` merged the same work item as `2657490` at 2026-08-05T21:35:42Z |

**Neither branch is work loss. Neither was abandoned on purpose. Both are the residue of a
mechanism, and the two mechanisms are different** — which is why the ticket's instruction to
judge them separately was the right one.

The residual on `z8af0` is **one mathematical result and two instrument rows that exist
nowhere on main** (§3.3). That is a decision for pm-onethird, not a finding of loss.

---

## 1. `polecat-a3d4` — the branch was submitted and merged

pm-onethird established this as LANDED by blob identity (9 of 15 files byte-identical on
main). That is correct and it is independently reproduced here — but there is a simpler and
stronger fact underneath it, and it was in `~/.pogo/events.log` the whole time.

    2026-07-30T02:06:06Z  agent_spawned            cat-a3d4, worktree ~/.pogo/polecats/a3d4
    2026-07-30T02:54:12Z  refinery_merge_attempted branch polecat-a3d4, mr-d9lbnmitjv1tur4p9b9g
    2026-07-30T02:54:15Z  refinery_merged          merge_commit 2919d28, 2.59 s
    2026-07-30T02:54:17Z  agent_stopped            exit 0, reason "requested"

`2919d28` on main and `c2f1854` on the branch have the **same author date**
(`2026-07-30 03:49:30 +0100`) and the **same subject**. `2919d28` *is* `c2f1854`, rebased by
the refinery — its committer date `03:54:13 +0100` is the merge event to the second.

So the branch went through the refinery on the normal happy path and the polecat was stopped
two seconds after its own merge. **`git cherry` reports `c2f1854` "not upstream" because the
rebase resolved conflicts against main's parallel same-day work, which altered the patch of 6
of the 15 files and therefore its patch-id.**

Blob identity against main, reproduced (`__pycache__` excluded, 15 files):

| | files |
|---|---|
| **IDENTICAL** (9) | `.gitignore`, `controls.py`, `linalg.py`, `links.py`, `local_to_global.py`, `lrb.py`, `run_theorems.py`, `controls_output.txt`, `theorems_output.txt` |
| **DIFFERS** (6) | `lrb_output.txt`, `run_all.sh`, `run_lrb.py`, `run_sweep.py`, `sweep_output.txt`, `docs/OneThird-Hodge-Side-Leverage.md` |
| **ABSENT ON MAIN** | none |

**Disposition: (a). Redundant, safe to reap. Nothing to do.**

### 1.1 What this corrects in the ticket body

The 02:14Z append reads *"THE COMMIT IS 44 MINUTES LATER THAN THE ARCHIVE. The polecat kept
working, and pushed, after its item had already been archived out of every normal listing."*

Whatever the archive mtime records, the branch **merged five minutes after its tip commit**,
and the agent stopped two seconds after that. There is no window in which a polecat was
working an item that had been closed out from under it. The mtime ordering is not evidence of
one.

---

## 2. `polecat-z8af0` — a DOUBLE DISPATCH, and the first branch won

The five patches are real and are not upstream by patch-id. They are also a **complete
second, independent execution of the same work item**, done while the first execution's
branch was still sitting recoverable in the refinery.

    2026-08-05T19:17:30Z  agent_spawned            cat-x8af0 on mg-8af0
    2026-08-05T20:06:27Z  refinery_merge_attempted branch polecat-x8af0, mr-d9pp7aatjv1h244d84g0
    2026-08-05T20:06:27Z  refinery_merge_FAILED    stage "fetch", terminal:true
                                                   "Could not resolve host: github.com"
    2026-08-05T20:52:32Z  agent_stopped            cat-x8af0, exit 0, reason "requested"
    2026-08-05T20:52:32Z  work_item_claim_released mg-8af0
    2026-08-05T20:52:36Z  work_item_claimed_at_spawn  cat-z8af0 on mg-8af0     <-- 4 SECONDS LATER
    2026-08-05T21:35:40Z  refinery_merge_attempted branch polecat-x8af0, mr-d9pq4c2tjv1h244d84ig
    2026-08-05T21:35:42Z  refinery_merged          merge_commit 2657490, 2.38 s
    2026-08-05T21:35:44Z  agent_stopped            cat-z8af0, exit 0, reason "requested"

Read in order: **a transient DNS outage failed `x8af0`'s merge terminally; `x8af0` was then
stopped and its claim released; the item read as available and `z8af0` was dispatched onto it
four seconds later; `z8af0` re-derived the entire ticket for 43 minutes; `x8af0`'s branch was
resubmitted and merged; pogod's merge-completion stop then fired — on `z8af0`, two seconds
after a merge it had no part in.**

`z8af0` never had a chance to submit. It was not abandoned, and nobody decided anything about
it.

### 2.1 This is a THIRD signature, and not the one mg-687f was filed about

mg-687f's signature is *pushed, stopped before submit, item silently returns to PENDING*.
`z8af0` is *pushed, stopped before submit, item closed DONE by a sibling's merge*. The
first branch's terminal merge failure is the initiating event and it is a network fault, not
a lifecycle one. **Four data points, three distinct mechanisms** — pm-onethird's refusal at
02:14Z to name a cause from them was correct and remains correct.

---

## 3. Did `z8af0`'s content land? Per finding, by content, not by patch-id

The landed work is `polecat-x8af0`'s: `c420303` (predictions), `0c3a2ba` (F2), `534c06b`
(F1), `66130f8` (F3), `2657490` (docs). All five are authored 2026-08-05 20:23–20:47Z and
committed 21:35:40Z — one rebase, at the merge.

### 3.1 All three findings landed, with the same headline conclusions

| finding | `z8af0` (unmerged) | `x8af0` (on main) | same conclusion? |
|---|---|---|---|
| **F2** — V6 scored a literal beside it | `0c39f34` | `0c3a2ba` | **yes** — V6 replaced by rows scored outside the file, all shown to fire |
| **F1** — coverage numerator was `N/N` | `fb158c5` | `534c06b` | **yes** — and *both* repair it by asking `mutation_applied_at_site` of every poset in the sweep |
| **F3** — I4's ≥3-facet zero "is a result" | `a82acb3` | `66130f8` | **yes** — ALL FOUR zeros are FORCED; forced by a property of the prefix family, not of the mutation |

`controls.py` on main carries the withdrawal in prose, and goes **further** than the branch:
*"ALL FOUR ARE FORCED — and so is `facet_swap01`'s, and so is the uncorrupted build's."*
Main also handles the `n = 2` degenerate case the branch's argument does not reach, forecast
by its own `PREDICTIONS.md` E4.

**On the mathematics, main is ahead of the branch, not behind it.**

### 3.2 What was checked, and how

    git cherry origin/main origin/polecat-z8af0            -> 5 patches, exit 0
    git diff --name-only $(git merge-base ...) BR          -> 15 files
    blob identity vs origin/main                           -> 0 identical, 7 differ, 8 absent
    git log -S'forcing_8af0'          origin/main          -> 0 commits
    git log -S'THE FULL PROFILE'      origin/main          -> 0 commits
    git log -S'consecutive but partial' origin/main        -> 0 commits
    git log -S'ALL FOUR ARE FORCED'   origin/main          -> 2 commits   <-- the finding landed

Zero file-identity, as pm-onethird measured — because the two executions wrote **different
instruments to different filenames** for the same three repairs, not because the work is
missing. `forcing_8af0.py` has no counterpart name on main; main's F3 instrument is
`probe_f3_ridge_multiplicity.py`.

### 3.3 THE RESIDUAL — three rows on the branch that are on no commit on main

This is the only part of `z8af0` that is not on main in some form, and one of the three is a
mathematical result rather than an instrument nicety.

1. **The bound is TIGHT, and "consecutive" is not the dividing line.** `forcing_8af0.py` S4
   sweeps every level-size profile of length 2–4 on a 5-element ground set — 11 profiles —
   and finds max ridge multiplicity ≤ 2 on **exactly one**, the full profile `[1,2,3,4]`.
   `[1,2]` is consecutive and gives **4**; `[2,3]` is consecutive and gives **3**.
   So I4's zero rests on the *whole* of the premise, not part of it.
   **Nothing on main states this.** Main's `V4c` and `probe_f3` measure the premise and the
   bound; neither asks whether the premise is tight. This row also refuted its own author's
   first form, and the failing transcript is kept at `out_forcing_8af0_FIRSTFORM_exit1.txt`.
2. **A negative control on the multiplicity routine.** S3 constructs a facet family with
   profile `[1,3]` over 3 elements — violating the premise — and runs the *same*
   `ridge_multiplicity` routine on it, which reports **3**. Without it, "0 families with a
   ridge in ≥ 3 facets" is the answer of a procedure never seen to say anything else. Main's
   `V4c` and `probe_f3` have no such row.
3. **The verifier firing on a real defect.** `out_verify_e35b_F2COMMIT_exit1.txt` — the
   repaired verifier exiting 1 on the *real* tree at the F2 commit with F1 deliberately still
   present. Main's evidence that its replacement rows can fire is constructed inputs only.

**These are not lost findings** — the ticket's three defects are repaired on main — **but
(1) is a result main does not have.** Reaping the branch discards it. That is pm-onethird's
call and is deliberately not made here.

---

## 4. Exit routes, as mg-687f asked

| branch | exit | route |
|---|---|---|
| `cat-a3d4` | `exit_code 0`, `reason "requested"` | stopped 2 s after **its own** merge — happy path |
| `cat-z8af0` | `exit_code 0`, `reason "requested"` | stopped 2 s after a **sibling's** merge closed its item |

**Neither was a hard exit.** So these two say nothing about the ticket's open question of
whether `reportStrandedWorkOnRelease` survives `kill -9`.

And their absence from `events.log` has a simpler explanation than a gate bypass: **the first
`work_item_stranded_push` event in the entire log is `2026-08-09T21:01:59Z`** (12 events
total as of 2026-08-13). That is four days after `z8af0`'s release and ten days after
`a3d4`'s. The gate was not emitting on either date. Their absence is fully explained without
invoking a hard exit, and is **not** evidence they were clean.

---

## 5. Two things worth handing to mg-be37's sweep

Recorded, not filed. mg-be37 is claimed and in flight.

1. **`git cherry` over-reports even on branches that went through the refinery and merged.**
   `polecat-a3d4` is the proof: MR merged, agent stopped on the happy path, and `git cherry`
   still says "1 patch not upstream" — because the refinery rebase resolved conflicts and
   changed the patch-id. This is stronger than the rescued-into-another-branch case pm-pogo
   raised, because here there is no other branch to look at. A sweep keyed on `git cherry`
   must publish its output as **candidates requiring a content check**, in those words.
2. **A shape the existing gate may be blind to in principle.** `z8af0` was released holding
   pushed unmerged work at the moment its work item had *just been closed* by a sibling's
   merge. If the gate keys on an open work item, that state is invisible to it. **This is a
   question, not a finding** — the gate was not live on 2026-08-05, so it cannot be tested
   against this instance, and reading `strandedgate.go` is out of this ticket's scope.

---

## What this does NOT establish

- Not whether `z8af0`'s residual (§3.3) is worth landing. It is described, not valued.
- Not that `a3d4`'s 6 differing files are *better* on main — only that its own commit merged.
- Not whether the gate fires on a hard exit. Neither branch took one (§4).
- Nothing about `polecat-x8af0`'s worktree or `~/research/one_third_width_three`, the repo
  path its spawn event names. Not looked at; out of scope.
