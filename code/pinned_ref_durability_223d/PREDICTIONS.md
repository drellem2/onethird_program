# mg-223d — predictions for THE DURABILITY OF THE ARC'S PINNED REFS

Committed **before any script of this tree exists**, in its own commit, so that
what follows can be scored against a file whose bytes predate the instrument.

The subject is D10 as cfd9c filed it: **`9f1ecaa` is not an ancestor of HEAD**,
and the arc's one stable instrument — mg-9160's reconstruction — takes it as an
input. cfd9c found this incidentally, correctly declined to repair it, and said
in so many words that it had **not** swept for others.

---

## H — DISCLOSURES. What I had already measured before writing this file.

This section exists because a prediction made after the measurement is not a
prediction, and the arc's own repeated finding is that the laundering is what
does the damage. Everything here is a **measurement**, and nothing in it is
scored.

| | disclosed |
|---|---|
| **H1** | `9f1ecaa` resolves, is a commit, and `git merge-base --is-ancestor 9f1ecaa HEAD` exits 1. Confirmed by hand before this file. |
| **H2** | It is reachable from exactly one ref: `refs/remotes/origin/polecat-z03d1`. `git branch -a --contains` names that and nothing else. It is on **no tag** — this repository has **zero** tags. |
| **H3** | `origin` is `https://github.com/drellem2/onethird_program.git`, a real GitHub remote, and there are **246** `refs/remotes/origin/polecat-*` refs. |
| **H4** | The cause is the **refinery rebase**. `9f1ecaa`'s patch-id twin `6fda370` **is** on main. I measured this for `9f1ecaa` by hand, and then for a wider set (H6). |
| **H5** | The arc already knows this mechanism and I did not discover it: `code/idiom_sweep_audit_18dc/PREDICTIONS.md:23` names the pairs `9f1ecaa`↔`6fda370`, `d33970b`↔`eacc5e1`, and `out_v1_population.txt:56` prints `9f1ecaa -> 6fda370 patch-id SAME tree DIFF runners 108 -> 111`. My contribution is not the mechanism; it is the **population**. |
| **H6** | A hand sweep of quoted hex literals (7–40 chars) in the **1096** tracked `*.py`/`*.sh` files gives **190** distinct literals, **176** of which resolve to a commit, of which **27 tokens / 26 distinct commits** are **not** ancestors of HEAD. All 26 are held by `origin/polecat-*` refs (14 distinct branches), 3 of them additionally by a local `refs/heads/polecat-*`. All **26 of 26** have a patch-id twin on `main` within its last 400 commits. So `9f1ecaa` is **1 of 26**, not a one-off. |
| **H7** | A widest-possible sweep — any hex token 7–40 anywhere in any of the **2423** tracked files — gives **1846** tokens, **1091** resolving to a commit, **381** of those not ancestors of HEAD. I have **not** established how many of those 381 are real references as opposed to accidental prefix collisions, and P5 is about exactly that. |
| **H8** | `code/corpus_fixedpoint_fd9c/out_s3_reconstruction.txt` prints, in section S3c(a), a table reading `9f1ecaa exists: True an ancestor of HEAD: False` and then, four lines below it, the sentence *"Both of mg-9160's are ancestors here."* I read both before writing this file. I did not write the transcript and I am not the ticket owner for that tree. |
| **H9** | `lib9160.parent_corpus()` is `[(p, "9f1ecaa") for p in corpus("9f1ecaa")] + [(p, "eacc5e1") for p in corpus("eacc5e1") if p.startswith("code/grain_axis_audit_03d1/")]`. I read it. `eacc5e1` **is** an ancestor of HEAD. |

---

## P — PREDICTIONS. Live bets on things I have **not** measured.

### P1 — the population of RECONSTRUCTIONS is tiny, and mg-9160's is the only exposed one. **0.75**

A *reconstruction*, for this tree, is a figure whose population is a **union of
two or more refs** — not a checkout, not a glob of the disk. I predict that over
all 179 `code/*` directories there are **at most 3** such figures, and that
**mg-9160's is the only one whose published numbers depend on a ref that is not
an ancestor of HEAD**.

Scored on: the census in `r3_reconstruct.py`, which must name every candidate it
rejected and why, not just the survivors.

### P2 — the twin is NOT a substitute, and I will show the figure move. **0.92**

Re-pointing `PARENT_REV` from `9f1ecaa` to its on-main twin `6fda370` **changes
the reconstruction**: at least one of `517 / 1191 / 246 / 626 / 400` moves. The
rebase carried the commit onto a later main, so its tree carries files that did
not exist when mg-03d1 ran. 18dc measured this for its own runner rule
(108 → 111); nobody has measured it for the 517.

This is the bet that decides the repair. If P2 loses, re-pointing is free and
tagging is unnecessary ceremony.

### P3 — a tag survives the failure mode and a branch-held commit does not. **0.85**

Built as an **exhibit**, not an assertion: a throwaway clone, both commits
present, branches deleted, `git gc --prune=now --aggressive` run, and then the
tagged commit still resolves while the untagged one is gone. I predict the
untagged commit is **collected** and the tagged one **survives**.

I predict specifically that I will have to defeat the **reflog** to see this —
that a naive `gc` leaves the object alive for the wrong reason (E5).

### P4 — nothing in the arc is dead yet. **0.80**

Of the 26, **zero** fail to resolve today. The whole finding is about a deadline,
not a casualty. If any of the 26 is already unresolvable this prediction loses
and the ticket's rank was, if anything, too low.

### P5 — the wide population is mostly FALSE POSITIVES, and reporting 381 would be an over-report. **0.70**

Of H7's 381 non-ancestor wide hits, I predict **more than half** are not
references to anything — 7-hex tokens that collide with some object's prefix by
accident (a digest, a colour, a hash column in a table). I predict the count of
*genuine* off-history references outside code is **under 60**.

I am making this bet because the tempting headline here is "381 broken pins" and
the arc's most-repeated defect is exactly that shape.

### P6 — the tag repair is NOT durable until pushed, and that is its real cost. **0.88**

`git tag` writes into the shared `.git` of this machine. The refinery merges
**branches**; it does not merge tags. So I predict that after my branch merges,
the tags exist on this machine and **not** on `origin`, and that the honest
statement of the repair has to say so rather than claiming durability it has not
got. I predict I will push the tags explicitly and report the push.

### P7 — the arc has a *convention* gap here, not just an object gap. **0.65**

I predict that **zero** of the 179 directories declare, anywhere in a tracked
file, that a figure of theirs depends on a ref remaining reachable. The
observation exists in one place (mg-fd9c's S3c(a)); the *convention* — a
checkable declaration — exists nowhere. If this is right, the repair that
matters is not the 26 tags but the control that fires when pin 27 is written.

---

## E — ERRORS OF MY OWN, filed in advance.

| | error, and why it is available to me |
|---|---|
| **E1** | **My population rule is quoted literals in `*.py`/`*.sh`.** A pin written unquoted, built by concatenation, read out of a `.md` at run time, or living in a `.json` fixture is **outside** it. I will report the rule's shape, not just its output, and I will say what it cannot see. |
| **E2** | **I double-count.** `3738079` and `37380799` are two tokens and one commit. Any count I print must say whether its unit is the token or the commit; "27" and "26" are both true of different things and interchanging them is the arc's grain defect in miniature. |
| **E3** | **My tags become provenance nobody authorised.** A tag named after a ticket reads like a claim that the ticket blesses that commit. They are keep-alive anchors and nothing else, and if the name suggests otherwise the name is wrong. |
| **E4** | **I "repair" a pin by re-pointing it at its twin** and silently move a published figure. The ticket forbids this in its own words and it is the single most available mistake in this task, because the twin is right there and the diff looks clean. |
| **E5** | **My gc exhibit passes for the wrong reason.** The reflog, `gc.reflogExpire`, the `origin/HEAD` symref, or a stale index all keep objects alive. A survival I cannot attribute to the tag is not evidence for the tag. |
| **E6** | **I declare durability I have not got** — tags on this machine only, and a report that says "durable" without saying "on this machine". P6 is the prediction; this is the error it is watching for. |
| **E7** | **My reachability check counts my own branch.** `for-each-ref --contains` will happily report `refs/heads/polecat-c223d`, and a commit whose only holder is the branch I am about to have deleted is *not* safe. I must exclude my own ref, and I must check that I did. |
| **E8** | **I treat "has a patch-id twin on main" as "is safe to lose".** For at least four directories in this arc — `idiom_sweep_audit_18dc`, `transcript_census_1abe/t4_rebase.py`, `publication_anchor_132a`, `audit_c067/c1_rebase.py` — the **pre-rebase commit is the subject**. Losing it does not degrade the figure; it destroys the finding. |
| **E9** | **I promote the reconstruction to an instrument while repairing it.** cfd9c's S3b names four things it cannot do. A repair that makes it easier to reach makes it easier to misuse, and the constraint is in the ticket for that reason. |
| **E10** | **I count `refs/heads/*` in this worktree as durable.** They are local branches of a shared `.git` that the refinery prunes. A local head is not a weaker tag; it is a branch. |

---

*Committed before `lib223d.py`, before `r0_selftest.py`, and before any output
of this tree exists. If the git history shows otherwise, this file is worthless
and should be read as a summary rather than a prediction.*
