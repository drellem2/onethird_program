# mg-6ef4 — PREDICTIONS

Written and committed **before** `t1`–`t4` were run, and not edited afterwards. Every prediction
below names an exit code or a specific row. Misses are kept as written and developed in
`OUTCOMES.md`.

Two counters, separate on purpose (mg-4700's convention, kept): `Tn TOTAL BAD` counts outcomes that
contradict **mg-5040's own claims**; `Tn PREDICTIONS MISSED` counts predictions in this file that
were wrong. A wrong prediction about code this ticket did not write is information, not a defect.

The subject is `3c8f535` + `f93e41f` + `3bc2cf7` (mg-5040), which repaired mg-4700's three OPEN
items. The pinned pre-repair revision is `4372fae` — mg-5040's own pin, reused deliberately so that
"before" means the same thing in both instruments.

---

## T1 — OPEN 1. Did it SUBTRACT, or widen a third time?

mg-5040 took **option 1**: state the walk's bound, and state it *in the enumeration* — the walk
returns every entry it declined, and an entry that is not the one stated `__pycache__` rule is
counted into that checker's `TOTAL BAD`. So the question is not whether the sentence is right today.
It is whether the **next** world-change arrives as a printed line or as silence.

| id | question | prediction | basis |
|---|---|---|---|
| P1a | `w3_scope.py` at HEAD, with a **mode-000 regular file** holding a live forbidden statement planted in `code/species_7d75` | **exit 0**, silent — the statement is never named | the walk reaches it (`os.path.isfile` is true), so it is not residue; the `open()` then raises `PermissionError`, which the read layer catches as `OSError` and files under **UNDECODABLE**, which is printed but **not** counted into `bad` |
| P1b | the same statement in a **readable** file, same tree — the attribution control | **exit 1**, `*** STILL ASSERTED ***`, naming the file | if this is not red, P1a's silence means nothing |
| P1c | a **readable** file whose bytes are not valid UTF-8, same tree | **exit 0**, and it lands in the **same** printed bucket, under the **same** wording, as P1a | `UnicodeDecodeError` and `OSError` are caught by one `except` and printed as "skipped as not decodable UTF-8 text" |
| P1d | are P1a's and P1c's printed lines distinguishable to a reader? | **no** — same list, same sentence, and the sentence is **false for P1a** (the file is perfectly decodable; this process cannot open it) | one bucket, two worlds |
| P1e | is the mode-000 file anywhere in any checker's **residue** (`declined, NOT STATED`)? | **no**, 0 of 4 checkers | the residue is computed at the walk; this decline happens after it |
| P1f | `s1_extent.py` at HEAD with the mode-000 file | **exit 1**, but **NAMES IT: no** — loud for the wrong reason, its `shutil.copytree` control raising on a file it cannot read | mg-4700 D2b and mg-5040 P1e are the same shape; this is the third and fourth instance of it |
| P1g | `e1_extents.py` row *"reads every non-excluded regular file of all four trees"* with the mode-000 file present | **ok** — E1 **certifies the extent as true** over a file that was never read | `trace_open.py` records the path **before** calling the real `open`, so an attempt that raises is recorded as a read; `want <= got` therefore holds |
| P1h | `e1_extents.py` overall | **exit 1**, through rows about `s1_extent.py`'s output, not through the extent | collateral of P1f |
| P1i | `w3_scope.py` at the **pin** `4372fae`, same plant | **exit 0** — silent there too | this class is untouched by the repair in either direction; it is not a regression, it is a generation the subtraction did not reach |
| P1j | does the **stated bound** match the code exactly? | **no — at least 2 mismatches.** (i) the printed bound says the walk "reads no entry that is not a regular file", but `os.path.isfile` **follows symlinks**, so a symlink to a regular file *is* read; (ii) the printed bound says the walk "RETURNS EVERYTHING IT DECLINED", and `walk_residue`'s own first statement is `if not os.path.isdir(root): return files, stated, unstated` — an entire root declined with **empty** residue | read from the shipped source |
| P1k | `walk_residue(<a path that is not a directory>)` | returns `([], [], [])` — three empty lists, **no residue entry at all** | the early return above |

**The shape of the finding, stated in advance so the run can falsify it.** mg-5040 removed the
silence **at the walk**. The file set these checkers quantify over is built in **two** layers — walk,
then read — and the second layer still declines in silence, under a bucket whose stated reason is
wrong for the case that matters. If P1a is red instead of silent, this whole section is wrong and I
will say so.

---

## T2 — OPEN 2. Is it a rung?

mg-5040's answer: *"THE STRUCTURE IS REMOVED … there is exactly one unit here that has a return;
`set -e` carries the verdict."* That sentence names, in the runner, the thing I expect to be the
fifth rung.

| id | question | prediction |
|---|---|---|
| P2a | non-comment lines in the rewired block, per runner | **2, 2, 2** — an `echo` heading and a `python3` call |
| P2b | delete the `echo` heading alone, e2 forced red | **3 of 3 still exit 1**, full output present — the heading is **inert**. 1 of 2 parts has no return, where mg-4700 found 2 of 3 |
| P2c | **the fifth rung.** Delete `set -e` alone — one line, **outside** the block and outside every deletion population applied to it — with e2 forced red | **3 of 3 exit 0**, with e2's finding printed **in full**. The check runs, prints, and the runner is green: mg-6cb9's F2 exactly, reached by deleting a line no deletion test has ever included |
| P2d | the attribution control: `set -e` present, e2 forced red | **3 of 3 exit 1** |
| P2e | is `set -e` in the deletion population of mg-821e's `p3_wiring.py`, mg-4700's `q2_wiring.py`, or mg-5040's `r2_wiring.py`? | **no — 0 of 3.** Every one of them enumerates the block |
| P2f | does anything — self-test, checker, or runner — assert the `echo` heading exists? | **no** |

**So: it did not add a fourth level of granularity — it made the code small enough that the third
level fits.** The rung I expect is not one level finer. It is one **scope wider**: the statement that
carries the verdict is not in the block, and a test whose population is the block cannot reach it at
any grain.

---

## T3 — the census, the copies, and the source

| id | question | prediction |
|---|---|---|
| P3a | `*.md` under `docs/` and `code/` at `af432ee`, from `git ls-tree` alone | **131**, against **123** claimed — short by **8**, mg-4700's number reproduced independently |
| P3b | the same at `e8fbd4f` | **105** against **100** — short by **5** |
| P3c | the count at HEAD | **≥ 155**, and **≠** the number in any committed `e2` transcript |
| P3d | committed `e2_crosssection.py` transcripts at HEAD that state a census figure **without** naming a revision | **≥ 1** — for those the sentence is WRONG, not STALE, and mg-5040's anchor only protects transcripts written after it |
| P3e | commit-message **objects** over all refs stating a figure for `A2 TOTAL BAD` | **≥ 4**, against mg-5040's "two commit messages" — this history carries rebase **twins** (`3c8f535`/`42f48ca`, `f93e41f`/`cada54f`, `3bc2cf7`/`fc98142` are visibly paired), so a message counted once exists twice |
| P3f | distinct message **texts** stating a figure | **3** |
| P3g | the **source** the copies share | `code/species_sites_821e/out_a2_6cb9_after.txt` — mg-5040's answer, which I expect to confirm rather than displace |
| P3h | copies in committed **files** at HEAD stating the old figure with no correction beside them | **≥ 1** outside the two mg-5040 disposed of |

**Replication is not corroboration.** Whatever the count, I score the number of **independent
derivations** of the figure, not the number of agreeing copies — and I expect that number to be
**1**.

---

## T4 — the floor. One thing no list in the ticket names

**Chosen: `kern5040.Probe`'s restore proof, and whether it can see the perturbation this audit
itself has to make.** I picked it because T1 requires `chmod 000` on a tracked file, and the first
thing to ask of a borrowed harness is whether it would have noticed.

| id | question | prediction |
|---|---|---|
| P4a | inside a `kern5040.Probe`, `chmod 000` a **tracked** file and leave it that way. What does `probe.restored` say? | **True** — restored. `git status --porcelain` and `git diff` see only the executable bit; a `644 -> 000` change is invisible to both, and `Probe` snapshots **bytes only** |
| P4b | the same perturbation under a mode-aware proof (this instrument's `Probe6ef4`) | **not restored**, and it names the file and both modes |
| P4c | `Probe.__enter__` on a worktree where a tracked file is already unreadable | the file is **absent from the snapshot**, silently — `except OSError: pass` — so it is also un-restorable, and nothing says so |
| P4d | does mg-5040's `selftest5040.py` assert the restore contract in the direction that must fail? | **yes** — but only for a **left-behind file**, never for a **left-behind mode** |

The restore is a list of remembered undos (`self.made`), and the proof cannot see the class nobody
remembered. That is mg-5040's own sentence about `os.walk`, turned on the harness it wrote to
measure `os.walk`.

---

## Exit codes predicted for this instrument's own probes

| probe | predicted exit |
|---|---|
| `selftest6ef4.py` | **0** |
| `t1_bound.py` | **1** |
| `t2_wiring.py` | **1** |
| `t3_census.py` | **1** |
| `t4_restore.py` | **1** |

A probe exits 1 when it has a finding. `run_all.sh` redirects and reads each status with an explicit
`||` guard — nothing is piped (mg-c2b3), and `set -e` is **not** relied on to carry any verdict in
this file, for the reason T2 is about.
