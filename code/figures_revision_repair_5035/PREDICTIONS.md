# mg-5035 — predictions for the repair of `figures()`'s false revision exclusion

**COMMITTED BEFORE ANY SCRIPT IN THIS DIRECTORY EXISTS.** Nothing below is
revised after the fact. A refuted prediction is a result and stays as written.

Filed at HEAD `20614ef`.

---

## THE TICKET'S FRAMING IS STALE, AND I SAY SO BEFORE I SCORE ANYTHING

`mg-5035` says *"`figures()` claims in its own comment to exclude a git
revision"* — present tense. **It does not, at HEAD.** The comment died with
`lib70c7`'s old body when `mg-bf79` landed `675c2ba`, in the same commit that
reported the finding. This is disclosure **D2** below, not a prediction; I
grepped for it before writing this file. `pm-onethird` asked to be corrected and
this is the correction: at HEAD there is **no comment anywhere claiming the
exclusion**. The surviving mentions are `mg-bf79`'s and `mg-03d1`'s prose, and
both correctly state that the claim was **false**.

So the ticket's branch *"if the comment is the thing that is wrong, fix THAT"*
is already spent — somebody already did, without saying they had. What is left
live is the **behaviour**: an all-decimal short revision still reads as a
FIGURE. That is what this ticket repairs, and the decision between the two
branches is therefore forced by a measurement rather than taken by reflex.

---

## DISCLOSURES — measurements I had already taken when I wrote this file

Laundering a measurement into a prediction is the cheapest way to make a score
look good. These are **measurements**, taken before this file existed.

| # | what I had already measured or read |
|---|---|
| **D1** | I scanned every tracked `.md` / `.txt` / `.py` for tokens matching `lib7522._NUMBER` that are **all decimal, comma-free, 7–40 characters** — the shape of an abbreviated git revision. **270 occurrences, 50 distinct tokens.** Of the 50, **20 resolve** as a git object in this repository and **30 do not**. Population: tracked `.md`/`.txt`/`.py` at `20614ef`; grain of 270 = one occurrence on one line; grain of 50 = one distinct token. |
| **D2** | I grepped `a git revision` across the tree. The comment `mg-5035` describes is **absent from every `.py` at HEAD** except as text `p4_figures.py` *prints* to quote the deleted original. It survives only in `mg-bf79`'s and `mg-03d1`'s prose, where it is reported as false. |
| **D3** | I read `lib70c7.figures` — it is one statement, `return _L().figures(line)`. There is **one implementation body** (`lib7522.figures`) and one forwarder. `lib56dc.figures(line, small=)` is a deliberately independent third copy, kept as the instrument that can measure the other two. |
| **D4** | I read `mg-bf79`'s `p4_figures.py` P4e and its `README`: over 451 committed transcripts it found 1284 distinct figures, 31 of magnitude ≥ 1e6, of which 6 resolve as git objects. Those are **mg-bf79's numbers over mg-bf79's population**, not re-derived by me at the time of writing. |
| **D5** | I read both tripwires: `selftestbf79.py:191` asserts `B.L.figures("at 3738079 the census") == [3738079]`, and `selftest03d1.py:98` asserts `1234567 in B.L.figures("at \`1234567\` the census gives 9 sites")`. Both assert the false exclusion **as false**, on purpose, so a real fix turns them red. |
| **D6** | From the D1 scan I already know a **shape-only rule cannot work**: `431723379` (*"16999 classes, 431723379 labelled posets"*) and `2147483647` (INT_MAX in a fixture) are both revision-shaped and both genuine figures. So is `1103515245`, an LCG multiplier. This is why nothing below predicts a magnitude or length rule will do. |
| **D7** | I read that `3738079` — the revision whose flagging by `r6_self.py`'s E2 *is* the reported defect — **no longer appears in `mg-70c7`'s README**. `mg-bf79` wrote that it "names revisions in a form that is not all digits or does not name them at all". So the original corrupted output was **worked around in the prose**, not repaired in the rule. |

---

## THE RULE I INTEND TO SHIP, STATED BEFORE IT IS MEASURED

Neither of the two rules `mg-bf79` weighed and rejected:

* **not** a magnitude rule (`drop ≥ 1e6`) — D6 already shows it drops real figures;
* **not** a resolves-as-a-git-object rule — its answer changes as the object
  database grows, so the same document would be censused differently on
  different days. In an arc built on re-derivation that is disqualifying, and it
  is a stronger objection than `mg-bf79`'s "accident of the object database".

Instead: **a DECLARED-revision rule.** A token is excluded only when it is both
(**S**) revision-shaped *and* (**D**) **declared a revision by the line it sits
on** — a cue such as `at`, `commit`, `revision`, `rev`, `sha`, `carried by`,
`landed at`, `pinned`, `parent`, `merge-base`, or a `git` command on the line.
Deterministic, a property of the text and not of the repository, and the same
*kind* of rule as the three exclusions `figures()` already has — every one of
which is contextual (`:`-prefix, `#`-prefix, `lines N`) rather than numeric.

**The git object database is used in this tree only as an EVALUATION ORACLE for
scoring the rule, never inside the shipped rule.** If those two ever get
confused, the objection above applies to me.

---

## PREDICTIONS

| id | prediction |
|---|---|
| **P1a** | The shipped rule excludes **0 of the 30** non-resolving tokens of D1. *Precision, at the grain of one distinct token: 100%.* This is the direction that matters — `lib70c7`'s own sentence is that *a generous exclusion list turns an unbacked figure into a non-figure.* |
| **P1b** | The shipped rule excludes **between 8 and 18 of the 20** resolving tokens. *Recall is partial and I am predicting it partial*: several resolving tokens sit in fixed-width transcript **table columns** with no cue word anywhere on the line, and no text-only rule reaches them. |
| **P1c** | The single largest un-reached group is transcript table rows (`out_t2_census.txt`, `out_t4_rebase.txt`, `out_t5_control.txt` of `mg-1abe`). I predict **≥ 6** of the 20 resolving tokens are missed for exactly that reason. |
| **P2a** | Both tripwires (D5) go **RED** when the rule lands. I will update both to assert the new truth and record in each that it fired. If either stays green, the fix did not reach the implementation and that is a failure, not a pass. |
| **P2b** | `lib56dc.figures` is **left unrepaired on purpose** and therefore still reads a declared revision as a figure. That is this ticket's **positive control**: an instrument that could have shown the defect and does. |
| **P3a** | **CONTAMINATION.** At least **1** figure count published in a committed transcript of this arc changes once revisions are excluded. I predict **between 1 and 12** committed transcripts contain at least one count whose value moves. |
| **P3b** | I predict at least one of them is in `mg-bf79`'s or `mg-70c7`'s own tree — the trees whose probes report *figures no transcript backs* — because that is the census the defect bites. |
| **P3c** | I predict **0** changed counts in `docs/` — the human-facing prose — because no `docs/` figure is produced by `figures()`. If this is refuted it is the most serious result in the ticket, because a `docs/` figure is one somebody could build a claim on. |
| **P4a** | **ALREADY-CORRUPTED PUBLISHED OUTPUT.** I predict I find **≥ 1** committed transcript in which a git revision is printed under a label that calls it a FIGURE. I predict the clearest instance is `mg-bf79`'s own `out_p2_population.txt` line `UNBACKED README.md 3738079`. |
| **P4b** | I predict the count of *unbacked figures* published by `mg-70c7`'s `r6_self.py` E2 at the run committed in its transcript was **inflated by exactly 1** by this defect, and that the inflation was later removed **by editing the prose** (D7) rather than by fixing the rule — so no published count is wrong at HEAD **for that reason**, and the arithmetic fix retracts nothing there. |
| **P4c** | I predict there is **at least one** published count elsewhere in the arc that is still inflated at HEAD and that no prose edit removed. This is the prediction I most expect to be refuted, and it is the one worth filing: if it is refuted, the honest headline is *the defect was real, reported, and its published damage had already been papered over*, which is a smaller claim than the ticket assumes. |
| **P5a** | The exit code of this tree's `run_all.sh` is **non-zero**, because probes here report findings by exit code. Pre-registered per-probe codes: `selftest5035` **0**, `f1_rule` **0**, `f2_contamination` **non-zero** (it counts contaminated counts), `f3_published` **non-zero**, `f4_self` **0**. |
| **P6a** | **The instrument's own defect count.** I predict I record **≥ 3** defects of *this* instrument found by its own selftest or by running it. Every tree in this arc that reported zero was wrong. |

---

## WHAT I WILL NOT DO, SAID IN ADVANCE

* I will **not** regenerate another tree's committed transcripts to make them
  agree with the new rule. `mg-03d1`'s A4d shows the cost of that and the brief
  of this arc forbids leaving another ticket's evidence rewritten. Where a
  committed transcript's figure moves, I **report the move** and leave the bytes
  alone — except for the two tripwires (P2a), which exist to be updated by
  exactly this ticket and say so in their own comments.
* I will **not** touch `lib56dc.figures` (P2b).
* I will **not** claim a revision is excluded on the strength of a hex-containing
  example. Every exclusion row this tree prints is an **all-decimal** token, and
  the hex ones are printed beside them only to show the rule is not keyed on hex.
