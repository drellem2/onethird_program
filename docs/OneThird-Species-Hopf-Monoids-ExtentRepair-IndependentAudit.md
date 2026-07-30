# Independent audit — the mg-d633 extent repair, all four extents, and whether the cross-section check fires

**Work item:** mg-6cb9. **Audits:** `e8fbd4f` (mg-d633), which repairs mg-7dd3 / `798afb7`
findings **A1**, **A2**, **B1** and **C1** against mg-a4ef / `106e121`.
**Instrument:** `code/species_extent_audit_6cb9`, `sh run_all.sh`, ~3 min, no network.
**Pre-filed in the same action as its parent**, so nothing here was chosen after seeing the
repair's own conclusions.

---

## 0. BOTTOM LINE

**The repair is real and it goes further than it was asked to.** Both wide extents were closed
by **widening the code**, not by narrowing a sentence; the one narrowing is labelled as a
narrowing in the run a reader reads and in the source; the cross-section check exists, and
**I made it fire, three ways, in two documents, on disk** — it is not the vacuous check this
arc has produced twice. Every deletion test I could construct moves the artifact.

**Three things it did not close, and one of them it created.**

| # | severity | finding |
|---|---|---|
| **F1** | **MAJOR** | *"EVERY REGULAR FILE in each tree is read — there is no extension rule"* is true **only because no species tree contains a directory.** Both repaired scans use a non-recursive `os.listdir` and drop directories **by a rule no sentence carries** — word for word the defect mg-d633 removed one layer up. The sentence got stronger; the code got no deeper. `e1_extents.py`, whose whole job is deciding whether a printed extent is true, **has the same blind spot**, so it certifies the sentence over a file it also cannot see. Measured: **Q10, Q17, Q17e all silent** |
| **F2** | **MAJOR** | The cross-section check is **reachable by reading and not by running.** It is named in every artifact a reader meets and is called by **0 of the 3** species-tree `run_all.sh`. The three trees whose checkers were all green while B1 stood cannot run the check that closes B1 |
| **F3** | **MAJOR** | `check_doc.py`'s C4 is a **presence test** over a document that writes **3 of its 5 anchors more than once** (19, 3 and 2 copies). **Deleting the copy a reader reads leaves the run green.** mg-8a5c found this exact shape, mg-a318 repaired it in the Hodge tree, mg-835f confirmed the repair; the species tree still has it |
| **F4** | MINOR | The committed `out_e2_crosssection.txt` says **100 markdown files**; the tree it ships in holds **105**. The run was produced at `c7f9673`, **three commits before the commit that ships it**. The census is right and the verdict survives — the **extent line** is false, in an audit about extent lines |
| **F5** | MINOR | `check_doc.py`'s repair was a **claim narrowing**, and nothing guards it at its own site: making the file read two more documents changes nothing it prints and nothing it exits |
| **F6** | NOTE | **The seam is `e2`'s `RUN_MIN`, and it is two tokens wide.** The document B1 lived in carries a **7-token strike**; restated **verbatim** in another section it is silent. `e2`'s extent names two holes and not this one |
| **F7** | NOTE | Every one of mg-d633's 28 E3 probes ran in a sandbox with **no `.git`**, so `s1_extent.py`'s controls (a) and (b) were skipped in all of them and, through `bad += ctl`, contributed nothing to any exit code E3 recorded |

**Nothing retreated. 0 mathematics disturbed.**

---

## 1. ALL FOUR EXTENTS, BOTH DIRECTIONS, AT MY OWN SITES

The brief is explicit that checking only the two repaired extents is not enough. **29 probes,
5 checkers, exit codes predicted before the run.** Each is one mutation applied to the **real
worktree** and undone, with `git status --porcelain` compared before and after.

| checker | its extent line claims | INSIDE → fires | OUTSIDE → silent | verdict |
|---|---|---|---|---|
| `check_doc.py` | 10 stricken sentences × **1 file**, plus a **second** file for C4's five assertions *"and for nothing else"*; reads no code | **1 of 2** | **3 of 3** | the miss is **F3**, not a false extent: C4 fires only when **every** copy of an anchor is gone |
| `w3_scope.py` | X4, X5 and the character-ring rule over **1 tree**, *"every regular file in it, with no extension rule"* | **2 of 2** | **2 of 2** | exact at every site I could name — **except a subdirectory (F1)** |
| `s1_extent.py` | 11 corrections × the document + **4 trees**, *"EVERY REGULAR FILE of each"*, less 5 named and the undecodable named | **4 of 4** | **3 of 3** | the same |
| `s2_seam.py` | one document; passages over 60 chars at 90 %, over 300 at 45 %; tables and headings in neither; ≤ 60 chars in neither **and listed** | **2 of 2** | **4 of 4** | **exact**, including the two boundaries the repair wrote |
| `e2_crosssection.py` | every `*.md` under `docs/` and `code/`, a strike against **its own document**, verbatim runs | **3 of 3** | **4 of 4** | **fires** — §2 |

**The sites I chose, and why they are not mg-d633's.** A `run_all.sh` in a tree E3 planted
nothing in (Q11); an **extensionless** file, because the repaired sentence is now *"every regular
file"* and an extension filter is precisely what was removed (Q7, Q12); a committed `out_*.txt`,
which s1's extent explicitly says is **not** skipped (Q6, Q13); a **non-UTF-8 file**, to check
that the undecodable list really does name what it drops — it does, `blob.bin` by name (Q18); and
a long passage tuned to **47.5 %** similarity over 423 characters (Q20).

**Q20 matters on its own.** All three of mg-d633's `s2_seam.py` IN-probes are **exact**
duplicates, so all three fire on the 90 % said-twice pass that mg-d633 added. **The 45 % sweep —
the original threshold, the one that predates the repair — is exercised alone by no probe in
that instrument.** Q20 fires it. The branch is live; nobody had shown it.

### 1.1 F1 — the sentence got stronger and the code did not get deeper

mg-d633 replaced an extension filter with *"EVERY REGULAR FILE in each tree is read — there is
no extension rule"*, and it is right that this is the better repair: it widens the code instead
of narrowing the claim. But both scans reach the tree like this:

```python
for f in sorted(os.listdir(root)):
    p = os.path.join(root, f)
    if not os.path.isfile(p) or f in EXCLUDE:
        continue
```

`os.listdir` is not recursive and `os.path.isfile` is False for a directory, so **a directory is
dropped by a rule no sentence carries** — which is, word for word, mg-d633's own description of
the defect it removed. Measured:

| probe | mutation | exit |
|---|---|---|
| **Q10** | X4 asserted in `code/species_7d75/sub/leak.md` | **0 — `w3_scope.py` silent** |
| **Q17** | X3 asserted in the same place | **0 — `s1_extent.py` silent** |
| **Q17e** | the same subdirectory, run past `e1_extents.py` | **0 — the extent-checker says the extent is TRUE** |

Q17e is the part that makes this MAJOR rather than a note. `e1_extents.py` exists to compare
what a checker **reads** with what it **prints**, and its own `regular(tree)` helper is another
non-recursive `os.listdir` — so the file that measures printed extents shares the blind spot it
is measuring, and confirms a sentence over a file neither of them can see.

Today no tree under `code/species_*` has a subdirectory, so the printed sentence **is true** —
by accident of the tree, with nothing that makes it fail on the day it stops being. The
undecodable list is printed *"one by one, as it is found, so it cannot grow unseen."* This
exclusion grows unseen, and it is the one the repair's own sentence rules out.

### 1.2 Narrowed the claim, or widened the code — and does it say?

| repair | kind | says so in the committed run? | says so in source? |
|---|---|---|---|
| `s1_extent.py` | **CODE WIDENED** | yes | yes |
| `w3_scope.py` | **CODE WIDENED** | yes | yes |
| `s2_seam.py` | **CODE WIDENED** | yes | yes |
| `check_doc.py` | **CLAIM NARROWED** | yes | yes |

**A silent narrowing reads as a fix and is a reduction in coverage. There is no silent narrowing
here.** Three widened, one narrowed, all four labelled in the run a reader reads. That is the
part of this repair that is unambiguously right, and F5 is what the one narrowing costs.

---

## 2. THE CROSS-SECTION CHECK FIRES

A check never shown to fire is worth nothing, and a control the author wrote against their own
detector is the thing being audited. So I re-introduced struck claims **on disk**, in live
documents, and read what the run said.

| id | direction | what | exit | run says |
|---|---|---|---|---|
| **R25** | IN | §4's struck AM §17.5 quotation, live and unmarked in **§0** — B1 itself | **1** | `strike line 486  run 42 of 42 (100%) restated at line 1257  *** STANDING UN-STRUCK ***` |
| **R26** | IN | §8's struck extremal claim, restated live in another section | **1** | STANDING |
| **R27** | IN | a struck claim in the **Bratteli** document, restated in another of its sections | **1** | `strike line 624  run 32 of 33 (97%)  *** STANDING UN-STRUCK ***` |
| R28 | OUT | the same restatement, in a **different** document | 0 | silent |
| R29 | OUT | with the retraction in the **next** paragraph | **1** | **my prediction missed — see below** |
| R29b | OUT | with the retraction **inside** the paragraph | 0 | silent |
| R30 | OUT | inside a second `~~strike~~` | 0 | silent |

**R27 is the one that shows the rule is not tuned to the document it was written for.** It fires
in a document nobody in this arc has planted in, on a claim nobody wrote a row for, because the
rule is *"the longest verbatim run a strike shares with its own document outside every strike"*
and the input is the `~~` a worker already types.

**R29 missed and is kept.** I wrote the retraction as the *next* paragraph; `e2` exonerates on
the paragraph **carrying** the occurrence and on nothing else. R29b was **added, not
substituted**, and is silent where the rule actually applies.

### 2.1 F2 — reachable by reading, not by running

| site | names `e2_crosssection.py`? |
|---|---|
| `s1_extent.py` and `s2_seam.py`'s own printed output | **2 of 2** |
| the document that carried B1 | yes |
| the repair document | yes |
| **`run_all.sh` of the three species trees** | **0 of 3** |

`e2` runs from `code/species_extent_d633/run_all.sh` and from nowhere else. A worker repairing
`code/species_repair_a4ef` runs that tree's `run_all.sh`, gets every checker in it, and does not
get the cross-section check. **B1 lived in a document those three trees check.** The correction
is true, it is written where a reader meets it, and the runner who would catch the next B1 does
not execute it. That is the fifth-instance class this audit was told to watch for, and a repair
for that class which is itself unreachably placed is the finding.

### 2.2 F4 — the shipped evidence predates its own commit

```
the committed out_e2_crosssection.txt says      100 markdown file(s)
`git ls-tree HEAD` -- the tree it shipped in -- 105
```

Counting `*.md` under `docs/` and `code/` at each recent commit puts **100 at `c7f9673`** —
**three commits before `e8fbd4f`**. A second, independent witness: the committed rows for the
Bratteli document cite strike line **112**, and the shipped tree has that strike at **120**.
The five files the shipped evidence never read include **the repair's own document** and its
`README.md`.

The census — 12 strike-carrying files, 30 strikes — is **correct for the shipped tree**, so
nothing standing was missed and the verdict survives. What is false is the **extent line**, which
is the one sentence this whole arc has decided a total must carry. The rule already exists in
Appendix A, from mg-8e30 / `e16e41c`:

> *"A COMMIT THAT MEASURES SOMETHING IT ALSO MODIFIES MUST PUBLISH THE POST-COMMIT
> MEASUREMENT."*

*(This audit's own instrument adds a markdown file containing a literal `~~strike~~`, which moves
a live run to 13 files and 31 strikes. That is stated in the run rather than netted out, and it
is why the comparison above is against `git ls-tree HEAD` and not against my worktree.)*

---

## 3. "UNDER WHAT CHANGE WOULD THE ANSWER DIFFER?" — THE CHANGE, MADE

For every check the repair touched, the code's own sentence about what would flip it, **made**,
and the artifact compared.

| id | check | the change | answer |
|---|---|---|---|
| **D1** | `s1_extent.py` | put the extension filter back | **differs** 1 → 0 |
| **D1e** | is that widening guarded? | the same, run past `e1_extents.py` | **differs** 0 → 1 |
| **D2** | `w3_scope.py` | put the extension filter back | **differs** 1 → 0 |
| **D2e** | is that widening guarded? | the same, past `e1` | **differs** 0 → 1 |
| **D3** | `s2_seam.py` | disable the 90 % said-twice pass | **differs** 1 → 0 |
| **D4** | `check_doc.py` | make it read **two more documents** | **THE SAME** — 0 → 0 |
| **D4e** | is that narrowing guarded? | the same, past `e1` | **differs** 0 → 1 |
| **D5** | `e2_crosssection.py` | disarm `RUN_FRAC` so the rule can never fire | **differs** 0 → **1**, through `e2`'s **own** controls |

**D5 is the shape to keep.** Disarming `e2` makes `e2` red, because it carries controls that
assert its detector still fires. None of the other four has that property.

**D4 is F5.** `check_doc.py`'s repair was a sentence, and a sentence has no deletion test at its
own site. It **is** guarded — by `e1_extents.py`, one layer out, in the audit instrument that
`check_doc.py`'s own `run_all.sh` does not call. Same shape as F2: the guard exists and the
runner who would trip it is somewhere else.

### 3.1 F3 — the anchor a reader reads can be deleted with the run green

My prediction **Q2** said deleting C4's `2 of 45` anchor makes `check_doc.py` exit 1. It exited
**0**, and here is why:

| anchor | copies in the file | delete **one** | delete **all** |
|---|---|---|---|
| names its target | 1 | **exit 1** | exit 1 |
| names the audit (`mg-a61f`) | **19** | **exit 0** | exit 1 |
| names the instrument | **2** | **exit 0** | exit 1 |
| records the missed predictions (`2 of 45`) | **3** | **exit 0** | exit 1 |
| records what it did NOT repair | 1 | **exit 1** | exit 1 |

C4 is `flat(s) in flat(rep)` — a presence test over the whole document. For three of five
anchors it is a check on **no site**. mg-8a5c wrote this finding in the Hodge tree
(*"the gate is a presence test"*), mg-a318 repaired it there by writing each figure **once per
site**, mg-835f measured the repair at 12 of 12. The species tree has not had that pass.

---

## 4. THE SEAM, AND THE THRESHOLD

| threshold | value | margin in the live tree |
|---|---|---|
| `s2` said-twice `REPEAT_RATIO` | 0.90 | worst live pair over the floor **53 %** → **37 points** (reproduces mg-d633's figure independently) |
| `s2` sweep `THRESHOLD` | 0.45 | worst live pair over 300 chars **24 %** → 21 points |
| `s2` `REPEAT_FLOOR` | 60 chars | what it excludes is **printed**, one passage per line — verified, Q22 |
| **`e2` `RUN_MIN`** | **8 tokens** | **closest non-firing run: 6. TWO TOKENS** |
| `e2` `RUN_FRAC` | 0.50 | closest non-firing fraction at ≥ 8 tokens: 34 % → 16 points |
| `e2` exoneration | — | **3 strikes are held silent by it alone** |

**F6, measured rather than argued.** `docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md` —
the document B1 lived in — carries a **seven-token strike**, *"as three independent agreements
about the term"*. Restated **verbatim**, in another section of that same document:

```
strike line 311   run   7 of   7 (100%)  restated at line 1256   below the rule
```

**e2 exits 0.** Its extent paragraph names two holes — another document, and *"a claim restated
in different words, at any length"* — and does not name this one: a claim restated in the **same
words**, in the **same document**, in another section, invisible because the claim is short. The
live tree already holds a strike one token below the floor.

I am not arguing `RUN_MIN` is wrong. Three of its non-firing rows are one-token strikes on the
word *"strike"* itself, and a floor is how those stay quiet. The finding is that **the margin is
two tokens and no sentence says so**, while the margin that is stated (37 points) is on the
threshold that is not binding.

---

## 5. WHAT REPRODUCES

* `sh code/species_extent_d633/run_all.sh` re-run unmodified at `e8fbd4f`, **before this
  instrument existed**: **exit 0**, E1/E2/E3 all `TOTAL BAD: 0`. The only differences from the
  committed outputs are F4's counts and the line numbers that go with them — **7 lines in two
  files**, every one of them a file count or a strike line number, and not one of them a verdict.
  Re-run again **with** this instrument in the tree: still exit 0, with E1's and E2's counts up
  by the markdown files I added.
* All six checkers exit 0 on the tree as found (self-test §5).
* `s1_extent.py`'s controls **(a)** at `ebecd89` and **(b)** at `83ac472` are **armed** in every
  probe here — 0 *"git unavailable"* lines — and are **skipped in all 28** of mg-d633's, whose
  sandbox does not copy `.git` (**F7**). E3's exit codes are real; two of the four controls
  behind them simply were not run, and its table does not say so.

---

## 6. THIS INSTRUMENT'S OWN DEFECTS, KEPT

Three, and **one inverted a result** — recorded in full in `OUTCOMES.md`:

1. **A restored `.py` left live bytecode behind.** `D5` disarms `kernd633.RUN_FRAC` and restores
   it; `0.50` and `2.00` are the same byte length and the restore landed in the same second, so
   Python's `(mtime, size)` validation **accepted the stale `.pyc`** and every later `e2` run
   imported `RUN_FRAC = 2.00` from a file that says `0.50`. The seam probe in §4 first reported
   the **opposite** of the truth, and `e2`'s control (a) reported *"0 findings, expected 1"* —
   my harness making a detector report itself broken. **`git status --porcelain` was clean the
   whole time.** Fixed two ways and asserted four ways in the self-test.
2. **Q22's needle matched a header that always prints.** Correcting the case would have made it
   pass while still testing nothing; it now points at the passage text. That is F3's defect,
   committed by the file reporting F3.
3. **A scratch reproduction of `e2`'s control (a) mismatched on a combining character** (`K̄`
   retyped through a heredoc) and for a few minutes read as a defect in `e2`. The instrument
   runs `e2` as a subprocess and reads its output instead.

**3 of 41 predictions were wrong** and are kept as written. One of them — Q2 — is F3.

---

## 7. WHAT THIS AUDIT DOES NOT COVER

* **29 probes is not an extent verified at every point**, and the choice of points is mine. They
  are listed by name in the output so a successor can see which regions were never touched.
* **No probe plants two mutations at once**; none tests a checker against a mutation of its own
  source.
* **Every `e2` probe restates verbatim**, because that is all `e2` matches. Paraphrase is
  untested here and is named as untested there.
* **§3 can only test flip conditions the code STATES.** An unstated one cannot be tested this
  way; its absence is reported instead.
* **Reachable is not read.** §2.1 measures whether the correction sits in the artifact carrying
  the false belief and whether a runner reaches it. Whether anyone reads it is not measurable
  here, and F2 is about the runner, which is.
* **F1 is latent.** No species tree has a subdirectory today, so no run is currently wrong. What
  is wrong is that nothing would notice.

---

## 8. THE ONE SENTENCE

mg-d633's own lesson is *"a structural remedy is not done when it ships; it is done when its
single point has been measured in both directions."* This audit measured that point in both
directions and found the repair sound. The three things it did not close have one shape between
them: **the correction is right, and the thing that would keep it right is somewhere the person
who needs it does not go** — `e2` in a runner the species trees do not call, `e1` guarding a
sentence `check_doc.py`'s own runner never reaches, and an anchor checked over a whole document
instead of at the site a reader reads. **The extent line was the remedy for a total that named
no population. The next one is a remedy for a check that names no site.**
