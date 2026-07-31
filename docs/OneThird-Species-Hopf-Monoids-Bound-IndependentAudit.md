# Independent audit of the mg-5040 bound repair — the second layer, the fifth rung, and the source

**Target:** mg-5040 / `3c8f535` + `f93e41f` + `3bc2cf7`, which repaired the three OPEN items
mg-4700 / `5c16f5c` left against mg-821e / `af432ee` + `b534db7` + `41ac5d4`.
**Audit landed:** mg-6ef4, pre-filed in the same action as its parent.
**Instrument:** `code/species_bound_audit_6ef4`, `sh run_all.sh`, about 12 minutes, no network,
30-assertion self-test.
**Predictions:** `code/species_bound_audit_6ef4/PREDICTIONS.md`, committed in `b2a849b` before a
single probe ran and not edited since. Three missed; all three are in
`code/species_bound_audit_6ef4/OUTCOMES.md` and two of them are better than the predictions were.
**Pin:** `4372fae` — mg-5040's own, reused deliberately so that "before" means the same thing in
both instruments.

---

## 0. VERDICT

**It subtracted. It did not widen a third time.** `followlinks=True` appears nowhere, the word
"total" is not used, and each walk returns every entry it declined with an unstated entry counted
into that checker's own `TOTAL BAD`. The twenty-line wiring block is two lines with one return. The
census figure mg-4700 raised is closed for the tree this work ships in. Every one of the three OPEN
items moved in the right direction, and this audit disputes none of that.

Four MAJOR findings, and each is about **where the subtraction stops**:

1. **The residue was installed at the WALK, and the file set is built in TWO layers.** A regular file
   this process cannot open passes the walk, fails `open()`, and is filed under a printed sentence
   that says the reason was the file's *encoding*. It is not residue, it is not a finding, and its
   contents are never scanned. `w3_scope.py` — whose entire extent is `code/species_7d75` — exits 0
   with a live X4 statement in that tree, and so does the runner that executes it.
2. **Two mismatches between the printed bound and the code**, both inside the enumerator: a root that
   is not a directory is declined with an **empty** residue by the function's own first statement, in
   3 of 3 copies; and the printed sentence "reads no entry that is not a regular file" is false in the
   other direction, because `os.path.isfile` follows symlinks.
3. **The fifth rung is not a finer grain. It is `set -e`.** Deleting that one line — 53, 60 and 43
   lines above the call, and in **no** deletion population this arc has ever used — turns 3 of 3
   runners green **while they print e2's finding in full**.
4. **The figure rests on two derivations that disagree.** 10 commit objects, 5 distinct texts, 44
   file occurrences — and exactly **2** transcripts of a run of the checker that produces it, saying
   **2** and **1**. The one that says 2 was committed first. Nothing in the arc compared them.

One MINOR, and it is the floor item: **`kern5040.Probe`'s restore proof cannot see a permission
mode.** A tracked file left at `400` is reported RESTORED.

**Nothing confirmed was weakened.** mg-4700's census numbers are re-derived independently and hold
exactly. mg-4700's F5 is closed. mg-5040's refusal to take the ticket's own "three commit messages"
figure was the right move, and the measured population is larger and differently shaped than either
number. No mathematics was touched.

---

## 1. OPEN 1 — the walk names what it declined, and the READ does not

mg-5040 was offered two options and took the first, and it took it in the strongest available form:
not a bound written in prose beside the code, but a bound **stated in the enumeration**. Each walk
returns `(files, stated, unstated)`; anything in `unstated` is counted into that checker's
`TOTAL BAD`. The sentence in `s1_extent.py` is worth quoting because this audit agrees with it:

> EACH WIDENING BUYS EXACTLY ONE GENERATION. Depth, then symlinks, then mount boundaries, then a
> directory this process cannot read, then whatever is next. So this is not widened a third time.

That is right, and it is why the world-change constructed here is not another kind of *directory*.

**The set is built twice.** `os.walk` decides what is REACHED. `open(...).read()` decides what is
READ. `walk_residue` names everything declined at the first. The second declines too — its
`except (UnicodeDecodeError, OSError)` puts the entry on an `UNDECODABLE` list that is printed, is
**not** counted into `bad`, and is printed under a sentence saying the reason was the file's encoding.

So: **a regular file this process cannot open.** It is a regular file, so `os.path.isfile` is true
and the residue stays empty. It raises `PermissionError`, which is an `OSError`. Planted in
`code/species_7d75` at mode `000`, carrying a live X4 statement, against a no-plant baseline:

| checker | exit | names the file | reports the statement | printed its own verdict | residue |
|---|---|---|---|---|---|
| `w3_scope.py` | **0** | yes | **no** | — | **0** |
| `s1_extent.py` | 1 | yes | no | **NO** | 0 |
| `e1_extents.py` | 1 | no | no | yes | 0 |
| `e2_crosssection.py` | 0 | no | no | yes | 0 |

* The **attribution control** — the identical statement in a readable file — is exit 1 and names it.
  The silence is the mode, not the statement.
* `s1_extent.py` never reaches `S1 TOTAL BAD`. `shutil.copytree` in its own injection control raises
  `Permission denied`, so the diagnosis a reader is handed is that the **control** broke. mg-4700
  found this shape once; mg-5040 found it three times in four; this is a fourth structure and neither
  of them planted it.
* `e1_extents.py` — the file whose whole job is deciding whether a printed extent is true — reads
  *reads every non-excluded regular file of all four trees (53)* **ok**. `trace_open.py` records the
  path **before** calling the real `open`, so an attempt that raises is recorded as a read. mg-5040
  made E1 walk independently so that it could disagree with the subject; it agrees anyway, through the
  tracer instead of through the walk.
* The two layer-2 worlds are **byte-identical on stdout**. An unreadable-but-valid file and a
  genuinely undecodable one both produce
  `(skipped as not UTF-8 text: leak6ef4.py; skipped as __pycache__: the whole directory rule)`.

**What a reader actually meets is a runner.** With the plant on disk,
`code/species_remainder_f8fa/run_all.sh` — the runner that executes `w3_scope.py` — **exits 0**. So
does `species_repair_6f61`. One of three goes red and **0 of 1** red runners say anything about the
statement.

**This is not a regression.** The same plant at `4372fae` gives the same silence. It is a generation
the subtraction did not reach, and the probe that measures it is printed and deliberately **not**
scored for that reason.

**And two places where the sentence and the code have already parted.** Both were measured on the
functions lifted out of the shipped files by parsing them:

* `walk_residue`'s first statement is `if not os.path.isdir(root): return files, stated, unstated`.
  A whole root is declined with an **empty** residue, in 3 of 3 copies, by the function whose stated
  contract is that nothing is dropped without landing in one of the last two lists.
* The printed bound says the walk "reads no entry that is not a regular file". `os.path.isfile`
  follows symlinks, so a symlink to a regular file is returned in `files` and is in no residue.

Neither is reachable by planting anything. They are properties of the enumerator, and they are the
two places it stops being a measurement and becomes a rule somebody wrote down.

---

## 2. OPEN 2 — the structure was removed, and the return is somewhere else

The ticket asked whether mg-5040 removed the structure or added a fourth level of testing. **It
removed structure.** The block is two non-comment lines in 3 of 3 runners; deleting the call alone
leaves 3 of 3 green with no trace the check ran; deleting the heading alone leaves 3 of 3 red with
e2's full output present. One unit, one return, measured — mg-5040's claim holds as stated.

The heading is still inert, and **0 of 4** `.py` files that mention it require it: every one is a
deletion-test instrument that names the line in order to remove it, this audit's included. That is
mg-4700's F2 second bullet, one line shorter. It is not the finding.

**The finding is that the statement carrying the return is not in the block.** The runners say so
themselves:

> `set -e` carries the verdict, which is what it was already doing.

`set -e` sits 53, 60 and 43 lines above the call. mg-821e's `p3_wiring.py`, mg-4700's `q2_wiring.py`
and mg-5040's `r2_wiring.py` each enumerate **the block**; none of the three deletes that line.
Measured, with e2 forced red by one planted markdown file and the three runners executed unmodified:

| state | `species_repair_a4ef` | `species_remainder_f8fa` | `species_repair_6f61` |
|---|---|---|---|
| unmodified — the attribution control | 1 | 1 | 1, all printing `STANDING UN-STRUCK` |
| heading deleted alone | 1 | 1 | 1 |
| call deleted alone | 0 | 0 | 0 |
| **`set -e` deleted alone** | **0** | **0** | **0**, all printing e2's finding IN FULL |

The check runs. Its output is printed. The runner is green. That is mg-6cb9's F2 exactly.

**Why this is the cheapest available demonstration that the level-chasing does not terminate.** The
levels went gate (mg-9220) → clause (mg-64b6) → twenty-line block (mg-4700) → line (mg-5040), each
answer smaller than the last. The line that carries the return was outside all four, and **no
refinement of the grain reaches it**, because what is wrong is not the grain but the **scope**. A
deletion test whose population is "the wiring" cannot find a verdict carried at the top of the file,
and a fifth level of subdivision would not have found this one either.

---

## 3. THE CENSUS AND THE COPIES — replication is not corroboration, and here is the arithmetic

**Re-derived independently, from tree objects, by a different instrument:** `e8fbd4f` claims 100 and
holds 105; `af432ee` claims 123 and holds **131**. mg-4700's "8 short" is exactly right, and it was
not taken from mg-4700.

**The copies.** Over every commit object reachable from every ref — not from the pin —
`A2 TOTAL BAD` is stated by **10 commit objects** in **5 distinct texts**, and every one of the five
has a rebase twin. mg-5040 reported "two commit messages". Neither an object count nor a text count
is wrong; the sentence does not say which one it is, and in a history a merge queue rebases they are
not the same number. There are **43** occurrences in committed files besides, of which **3** state
the old figure with nothing beside them — including the source itself, at
`code/species_sites_821e/out_a2_6cb9_after.txt:119`.

**Those figures are measured at `3bf0cd2`, the revision this section grades.** The post-commit
re-run, published in this ticket's second commit per this arc's Appendix A, reads **11 objects, 6
texts, 44 file occurrences** — because this audit's own commit message states a figure and joins the
population it is counting. That is F3 one level out, inside the section about F3, and it is
mg-5040's own kept defect 7 happening to its auditor. **Post-commit is still not post-merge:** the
refinery rebases this branch, so the object count is a property of a tree that will be replaced, and
the only figures here that a merge cannot move are the ones anchored on `e8fbd4f`, `af432ee` and
`4372fae`, which git cannot move.

**The source, which is what the ticket actually asked for.** An artifact *derives* the figure if it
is a transcript of a run of `a2_crosssection.py`, identified by markers lifted from that script's own
source rather than written out by hand. Exactly two artifacts qualify — at 67 and 59 markers, against
5, 4, 3, 3 and 3 for everything that merely quotes:

| artifact | says | committed |
|---|---|---|
| `code/species_extent_audit_6cb9/out_a2_crosssection.txt` | **2** | first |
| `code/species_sites_821e/out_a2_6cb9_after.txt` | **1** | the one every message copied |

**53 copies rest on 2 derivations, and the derivations disagree.** A contradicting measurement of the
same figure by the same checker was already committed in this repository, and nothing in the arc ever
compared the two. Counting the copies measures how often the number was typed.

**And a probe that fired at nothing, kept.** It was built to catch mg-5040's own evidence commit
`3bc2cf7` stating the figure bare — a copy its own enumeration could not have contained, because that
enumeration is pinned at `4372fae` and a population fixed before the work runs cannot hold the copies
the work is about to make. The bound is real. Measured, the copy it could not see names `cada54f`
twice in the paragraph carrying it, and `cada54f` is the tree the figure is about. The probe is kept
because a section that only ever fires is a section nobody can check.

**One thing mg-5040's repair does not cover, and does not say it does not cover.** `MEASURED AT
<rev>` makes a committed census figure STALE rather than WRONG. It is forward-only: **3** committed
census figures at HEAD name no revision at all, and for those the sentence is wrong rather than
stale.

---

## 4. THE FLOOR — the restore proof, which no list in the ticket names

Chosen because this audit has to `chmod` a tracked file to ask its central question, and the first
thing to ask of a borrowed harness is whether it would have noticed.

`kern5040.Probe` snapshots **bytes** and proves the restore with `git status --porcelain
--untracked-files=all` plus the full `git diff`. git carries one bit of a file's mode.

* `chmod 400` on a tracked file, left unrestored: **`restored=True`**. The file is not restored.
* `chmod 000`: `restored=False` — correctly, and for the wrong reason. git cannot **read** the file,
  so it is reported as *modified* though not one byte changed. Right verdict, wrong diagnosis: the
  shape section 1 found in the subjects, in the harness that measured them.
* A tracked file that is **unreadable at entry** is absent from the snapshot (`except OSError: pass`),
  therefore un-restorable, and no field says so.
* `selftest5040.py` has 14 assertions mentioning `restored` and **0** mentioning a mode. It tests the
  contract in the direction that must fail — for the one class it had already thought of.
* `__enter__` is byte-identical at `cada54f`, the commit that published the harness, so none of this
  is an artifact of running it in a worktree it was not written for.

**No probe in mg-5040 is shown to have left the tree broken, and this is not a claim that one did.**
What is measured is that if one had, in this class, the proof would have said RESTORED. The restore
is a list of remembered undos and the proof cannot see the class nobody remembered — which is
mg-5040's own sentence about `os.walk`, turned on the harness it wrote to measure `os.walk`.

This audit's own probe states its bound the same way, in its own run: porcelain, full diff, bytes and
**mode**, for every tracked regular non-symlink file under the repository — and then names ownership,
xattrs, ACLs, times, directory modes, symlink targets and anything outside the repository as **not
covered**. That list is a measurement of what four proofs look at, not a promise that nothing else
can go wrong.

---

## 5. WHAT IS OPEN

1. **The read layer has no residue.** Every reached entry that `open()` declines lands in one bucket
   whose printed reason is the file's encoding, is not a finding, and is not distinguishable from the
   other member of that bucket. Section 1.
2. **`set -e` is in no deletion population.** Section 2. The block has one return and the runner's
   verdict is carried elsewhere.
3. **`e1_extents.py` cannot disagree with a subject about a file the subject failed to open**,
   because the tracer records the attempt. Section 1.
4. **Committed census figures written before `MEASURED AT` are wrong rather than stale**, and that
   population is named nowhere. Section 3.
5. **The restore proof is blind to a permission mode.** Section 4.

None of these reopens an OPEN item mg-5040 closed.
