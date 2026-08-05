# mg-0ba7 — the INDEPENDENT AUDIT of mg-b2af's anchor-population repair

`code/anchor_population_audit_0ba7/` — 7 scripts, 52 self-test assertions,
worst exit 1.

**PRE-FILED IN THE SAME ACTION AS ITS PARENT.** `mg-0ba7` and `mg-b2af` were
created together by `pm-onethird` on 2026-07-31: the audit of the repair was
a ticket before the repair had a line of code. That is the standard for this
lineage, it is why `PREDICTIONS.md` can be scored at all, and it is why the
brief could name *include the sites with no `--format=%H`* before anybody
knew what including them would cost.

`PREDICTIONS.md` was committed at `e5d37a4`, **before any script of this
instrument existed**. **25 rows scored, 19 hit, 6 missed, every miss kept as
written.**

Run it with `./run_all.sh` (about five minutes; `a3` runs `k2_five.py` twice
inside a clone). Four scripts exit 1 and three of the four were predicted to.

---

## THE HEADLINE: THE POPULATION IS DEFINED BY A CAPITAL LETTER

mg-b2af's own headline is **A SEARCH BY FLAG HAS A POPULATION DEFINED BY A
FLAG.** It found that for `--format=%H` against the two named helpers — and
then imported the flag list unchanged (*"mg-330a's classifier, imported on
purpose"*, *"population by mg-330a's classifier, **unchanged**"*) and refined
the 19 *"without touching the denominator"*.

`lib330a._HASH_FORMATS` is

```
("--format=%H", "--pretty=%H", "--format=format:%H")
```

**`--format=%h` is not in it.** A classifier written fresh here from mg-330a's
own docstring, run over the same `ast.Call` nodes at the same tree:

| | mg-330a's classifier | mine |
|---|---|---|
| revision-producing call sites | 44 | **59** |
| history-derived | 22 | **28** |
| directories holding one | 14 | **19** |
| `UNRESTRICTED` | 1 | **4** |

**15 call sites, and every one of them is `--format=%h`.** Six are in the
defect classes. `git log -1 --format=%h -- <path>` **is** `NEWEST` — A-1's
defect spelled with a lowercase letter — and it is in no population this arc
has published: not the brief's 16, not mg-330a's 37, not mg-b2af's 40.

`selftest_0ba7.py` (2) asserts this on **one constructed line of Python**, so
that *"mine sees 15 more"* is a property of the two rules and not of this
tree, and re-reads `lib330a._HASH_FORMATS` at run time so the claim cannot go
stale silently.

The consequence for the deliverable's own headline number: mg-b2af's
STILL-OPEN list says of `code/repair_69d1/p3_reason.py` that it is
*"`UNRESTRICTED`, the loudest form of the defect … **the one site** in the 19
that no pin can help"*. There are **four** `UNRESTRICTED` sites at this tree,
and three are invisible to the classifier that list was drawn from.

---

## `OLDEST` WAS **NOT** ABSORBED — AND THE GATE THAT SAYS SO CANNOT SAY IT

The brief: *confirm `OLDEST` was not absorbed into the defect population —
check the repair did not make A-2's mistake while fixing it.* **It did not,
and this is the part of the ticket that confirms.**

Absorption is a *site* that is `OLDEST` at one tree and history-derived at
another, so it is asked of **membership sets, not counts**, at five trees, in
all ten ordered pairs:

| tree | `OLDEST` (set / rows) | history-derived (set / rows) |
|---|---|---|
| `ea97d0a` mg-330a pre-repair | 8 / **11** | 24 / 25 |
| `fba5f63` mg-330a repair | 8 / **11** | 24 / 25 |
| `14c6c3b` mg-b2af repair | 9 / **12** | 26 / 28 |
| `b1c3467` mg-b2af evidence | 9 / **12** | 26 / 28 |
| worktree | 9 / **12** | 26 / 28 |

**0 sites cross the boundary in either direction, in all ten pairs, and the
sets are nested along the commit order.** The count moved because the tree
moved. mg-b2af's published *"the sweep says 11 at every tree"* **reproduces
here at the row grain, under a different classifier** — which is what an
independent recount can add and a re-run cannot.

Two grains are printed side by side because they disagree — 9 as a set of
`(file, argument tuple)`, 12 as a count of call sites — and **neither is
reported under the other's name**.

**Now the gate.** `t1_population.py:430`:

```python
R.check(not [r for r in pinned if r["kind"] == "OLDEST"], ...)
```

`pinned` is `ANCHORS.tsv` — a four-row file **this ticket wrote**, drawn from
a population `HISTORY_KINDS` excludes `OLDEST` from by construction. So it is
constructed: in a clone, `--reverse` is deleted from one `OLDEST` call site.

| | before | after |
|---|---|---|
| `OLDEST` sites | 12 | **11** |
| history-derived sites | 28 | **29** |
| **the parent's `OLDEST` gate** | GREEN | **GREEN** |

**A site was absorbed and the check that watches for absorption did not
move.** The gate is not *wrong* — checking the treated population is a fine
thing to check. It is offered under a sentence about the **measured**
population (*"Absorbing it would inflate this repair's population"*), and the
check that sentence describes is not made anywhere. One predicate, two
populations, the narrower printed under the wider one's name.

**And the same question asked of my own widening**: of the 15 sites only my
classifier sees, **0 are `OLDEST`** and 6 are in the defect classes. The
widening costs me and does not flatter me, which is why it is reported rather
than argued.

---

## THE SITES WITH NO `--format=%H`: A NAME-LIST IS A POPULATION TOO

The brief: *include the call sites carrying no `--format=%H`; the parent
found 16 such, invisible to a flag-grep.* True — and `sweep_helper_uses`
carries the literal tuple `("last_touching", "nth_touching")` in its body.
**A search by NAME has a population defined by a NAME-LIST**, and this one
has two entries.

Derived instead: SEED = every function whose body contains a history-derived
call **and whose return value is tainted by it**; CALL SITES = every call
reaching such a definition **through the calling file's own bindings**.

| | sites | directories |
|---|---|---|
| mg-330a's two-name bare-name match, `CALL` rows only | 12 | 3 |
| **import-resolved closure** | **48** | **8** |

**9 distinct helper names; mg-330a's list has 2 of them** —
`base_before_dir`, `commits_touching`, `last_lacking`, `log_paths`,
`my_last_touching`, `my_nth_touching`, `publishing_commit` are the seven it
does not.

The name-match is wrong in **both** directions:

- **17 call sites** whose bare name is a seed name resolve, through the
  importing file's own bindings, to a **different definition** — four separate
  `commits_touching`s that take a `"%s..%s"` **RANGE**, which is a *set* with
  no single revision to re-point. Same name, different kind.
- **1 call site is honestly UNRESOLVED** and named as such:
  `code/hodge_leverage_repair_3f3b/repair_7e39.py:987` reaches its helper
  through `importlib.util.spec_from_file_location`. **No static closure can
  resolve it**, and that is stated as a limit of this instrument rather than
  dropped.
- **1 file uses `import *`** and is named for the same reason.

mg-b2af's own finding — *the document's "16 call sites" is the ROW count over
two populations, 4 `DEF` + 12 `CALL`* — **reproduces exactly at my tree**, so
it survives a tree it was not measured at.

---

## THE GATE AT THE POINT OF SPEND: A RULE WHOSE POPULATION IS A DIRECTORY

**F-1's repair holds, under a drift it did not choose.** In a clone, two pins
are re-pointed at two real revisions **chosen here** (mg-330a's own two
commits), derivations untouched:

| script | anchor spent | clean clone | under constructed drift |
|---|---|---|---|
| `k2_five.py` | `PRE_7E58_REV` | exit 0, `TOTAL BAD: 0` | exit 1, **`TOTAL BAD: 1`** |
| `k4_cancel.py` | `REPAIR_REV` | exit 1, `TOTAL BAD: 2` | exit 1, **`TOTAL BAD: 3`** |

Both print a spend-gate row naming the anchor they spend. **mg-b2af's table
reproduces exactly**, at a different tree, under a different drift. That
confirms.

**Two findings sit beside it.**

**(1) `t2`'s structural rule walks `code/branching_audit_e34a/`.** Resolved by
AST repo-wide — an `Attribute` on a name bound to `libe34a`, not a grep, so
that a file naming `REPAIR_REV` only in prose is not counted — **8 files spend
a `libe34a` anchor** and **3 of them are ungated and outside that directory**:

```
code/audit_2c77/q4_prerepair.py      spends PRE_REV, REPAIR_REV
code/repair_8d5e/r2_kernel_half.py   spends PRE_REV, REPAIR_REV
code/repair_8d5e/r4_self.py          spends all six
```

Each would run to a clean exit on a re-pointed anchor — the sentence F-1 was
written to retire — and `t2` is silent about all three because its population
is a directory.

**(2) `gate_spent` cannot gate two of the anchors `libe34a` derives.** Read
out of the module's own source: it derives **six** module-level anchors;
`ANCHOR_OF` has **four** keys. Asking `gate_spent` about `LAST_TOUCHING_G1`
or `NTH_TOUCHING_1` produces a **SELF-ERROR** — the unknown-name path
mg-b2af built as a safety feature, right about the name-list and wrong about
the anchor.

**And the asymmetry is the point.** `LAST_TOUCHING_G1` is the anchor that
**already re-pointed once** — `libe34a`'s own docstring records mg-69d1's
sentence edit moving it `4755d02 → d01ff32`. *The one anchor in the module
with a demonstrated history of drifting is the one the drift gate will not
accept the name of.*

---

## THE TWO LABELS, RECOUNTED

mg-b2af, READ: *20 sites; by SCOPE every one another ticket's; by KIND 5
records (3 transcripts, 2 prediction files) and 15 live claims.*

Re-implemented here from mg-2c77's rule character for character, at my tree,
excluding my own directory: **29 sites; by KIND 8 records and 21 live claims;
by SCOPE 29 another ticket's.** Both labels print, separately, with separate
counts and separate populations. **The two-function shape survives a
re-implementation at a different tree by a different hand.**

A recount using the subject's own rule can only find that the tree moved, so
the same sites are labelled a second time by a path rule written here: **any
`.txt` is a record**, because what makes a transcript uneditable is that it
records a run, not that somebody spelled its name `out_`.

**At this tree the two rules agree on all 29** — every `.txt` in the residue
is also an `out_*.txt`. That is a fact about this tree and not a confirmation,
so the difference is **constructed**: a hypothetical
`.../transcript.txt` is `live claim` under mg-b2af's `kind_of` and
`transcript` under mine. **KIND is the rule that decides whether a site gets
EDITED**, so a record whose filename does not begin `out_` would be offered
for editing. A latent difference, not a miscount, and it is booked as one.

---

## DISTINCTNESS BY RESOLUTION

**Constructed, not recalled.** One commit that edits `lib58da.py` and does
not touch `g1_provenance.py`. Two real, distinct commits; the blob for the
untouched path is the same object.

| | |
|---|---|
| distinctness by **sha** | **PASS** — they differ |
| distinctness by **resolution** | **FAIL** — the same object |

The content predicate **fires on a pair chosen by somebody else**, which is
what an independent audit adds to *it passed on its own pair*. mg-b2af's own
pair (`d01ff32d`, HEAD) still shows `ca90929f` on both sides **94 commits
later**.

**And the direction nobody in this arc has asked.** Every statement of the
lesson is about anchors that must **differ**. The mirror — anchors that must
be the **same** — is not symmetric, because a commit is a whole tree. Two of
`ANCHORS.tsv`'s four rows share the resolved revision `d01ff32d`; they name
the **same path**, so they agree. **The file is built right — it carries a
`path` column beside the `resolved` column. The point is that the sha column
alone could not have been.**

---

## THE FLOOR — ONE THING NO LIST IN THE BRIEF NAMES, NAMED IN ADVANCE

`classify_call` returns `None` unless the call carries **both** a `log`
argument **and** a hash format. So every population in this arc — 36, 37, 40,
16, 19, and mine — is a population of *revision-producing calls **that use
`git log` with an explicit hash format***.

**`git rev-parse`, `git rev-list`, `git merge-base` and `git describe`
produce revisions and carry neither.**

- **120 call sites** in `code/` use one of the four and are **in no published
  population of this arc**.
- **24 of them derive from `HEAD`**, across **15 directories** — the
  `UNRESTRICTED` shape, in four fewer characters, beside a STILL-OPEN list
  that calls the one site it can see *"the one site"*.

`git rev-parse` of a literal sha **normalises** a revision somebody already
chose and cannot re-point; that split is printed, and the rule for it is
stated as approximate because it is.

**And the limit of my own floor is stated as a limit.** `REV_COMMANDS` is a
four-entry tuple in `lib_0ba7.py` — **it is a name-list, which is what this
audit is about.** `git show --format=%H`, `for-each-ref`, `reflog`,
`name-rev`, `blame` are not in it (165 further call sites name one of those
five), and a call that builds its argv from a variable is invisible to every
AST rule here. **125 is a LOWER BOUND and it is labelled one.** I am not
closing this audit by claiming the enumeration I fault others for lacking is
complete in my hands.

---

## FOUR DEFECTS OF THIS INSTRUMENT, FOUND BY IT AND KEPT

1. **The taint test was a population defined by the syntax I thought of
   first.** `_tainted_return` propagated through `ast.Assign` alone.
   `lib8d5e.last_lacking` and `lib8d5e.base_before_dir` both receive the
   anchor through a **`for` target** and return it, so both scored
   `returns=False` and **two real anchor helpers were dropped from the
   closure**: 11 returning seeds and 40 call sites instead of 13 and 48.
   Found by reading the seed table's own named rows — which is why the rows
   are named. The comment sits at the fix; the assertion is
   `selftest_0ba7.py` (4), which fails on the first form.

2. **The scorer could not express the predictions it was scoring.** `score`
   compared `predicted == actual`, and every RANGE row in `PREDICTIONS.md`
   (`25..45`, `21..30`, `1..6`) is a string beside an int. `a4`'s first
   transcript **scored three HITs as MISSes**, one of them right by a margin
   of one. A scorer that reports a suite as worse than it was is the same
   class of error as one that reports it as better. The failing transcript is
   kept as `out_a4_labels_FIRSTFORM_miss3.txt` — **it is a REGENERATION at
   the shipping commit with only the `hit=` arguments removed, not the
   original bytes**, because the original run went to a terminal and was
   never redirected; saying so is cheaper than letting a regenerated
   transcript pass for a captured one. The defect is asserted live in
   `selftest_0ba7.py` (10).

3. **`a2`'s two grains disagreed and the first draft printed one of them.**
   `OLDEST` is 12 call sites and 9 distinct `(file, argument tuple)` pairs.
   The boundary question needs the set; the census question needs the rows.
   The first form of `a2`'s table printed only the set and would have read as
   a third answer to mg-b2af's `11` — a label/grain mismatch inside a section
   about label/grain mismatches. Both columns now print with the reconciliation
   written beside them.

4. **The instrument measured itself.** It walks `code/` and it *lives* in
   `code/`. `selftest_0ba7.py`'s constructed fixtures are real `ast.Call`
   nodes carrying real `git log` argv lists, so **one of them entered my own
   census**: the total read 60 where the subject supports 59, and the
   history-derived read 29 where it supports 28. **Caught because the totals
   moved between the draft transcript and the shipping one while the subject
   did not change** — which is only visible because the drafts were kept. It
   is one site, and one site is exactly the size of error that gets rounded
   into a headline. Every figure in `a1`, `a2` and `a6` now excludes
   `code/anchor_population_audit_0ba7/`, the self-count prints beside them,
   and it is never added in. **The `SCOPE` label this audit spends a section
   on is the label I needed and did not apply to myself.**

---

## THE SIX MISSES, KEPT AS WRITTEN

| row | predicted | measured | what was wrong |
|---|---|---|---|
| **P-1** | at most **4** classifier disagreements, most likely in `RANGE`'s dead branch | **15**, none in `RANGE` | I named two candidate mechanisms and got the second half only. Worse: I had *already measured* both classifiers' totals (M-1: 44 against my own later 59) and still wrote a bound of 4 over a gap I could have subtracted. A prediction contradicted by a measurement in the same file. |
| **P-2** | closure of **25–45** sites | **48** | The range was drawn from the parent's 12 and a guess at the multiplier. It is out by three and the direction is the one that matters — I under-guessed how much a name-list misses. |
| **P-4c** | mg-b2af's tree has **11** `OLDEST`, mine **12**, one new site | **12 and 12, 0 new** | The step 11→12 happened between mg-330a's commits and mg-b2af's, **not** between mg-b2af's and mine. I put a real step in the wrong interval. The nesting claim the row was made to support holds. |
| **P-8b** | the records share grows *faster* than live claims, because each new ticket ships transcripts and a `PREDICTIONS.md` | 8 of 29 against 5 of 20 — grew by **2.6 points** | Scored a HIT and it should not carry weight. A 2.6-point move on n=29 is not evidence for the mechanism I gave, and the row is kept mainly to say so. |
| **P-10** | **5–40** sites in no published population | **120** | An order of magnitude low. I predicted the CLASS existed — which was the point of the row — and then guessed its size from nothing, which the row did not need and should not have carried. |
| **exit codes** | at least **4 of 8** predicted exit codes wrong | **1 of 8** (`a4` predicted 0, exits 1) | mg-b2af predicted its twelve would not all land and all twelve landed; I over-corrected into predicting mass failure and called 4 "a real number and not a hedge" in advance. It was a hedge in the other direction. |

---

## WHAT THIS AUDIT CONFIRMS

Not everything here is a finding, and an audit that reports only findings has
a population defined by what it was looking for.

- **`OLDEST` was not absorbed.** 0 crossings, 10 ordered tree pairs, sets
  nested. mg-b2af declined A-2's mistake and the decline holds at every tree.
- **F-1's gate fires at the point of spend**, under a drift mg-b2af did not
  choose, at a tree it was not measured at — `k2` 0→1 and `k4` 2→3, exactly
  as published.
- **F-2's two labels are two functions, two columns, two counts**, and the
  shape survives an independent re-implementation.
- **The content-identity lesson is a running check**, and it fires on a
  constructed pair it has never seen.
- **mg-b2af's `16 = 4 DEF + 12 CALL` finding reproduces at my tree**, so it
  was a fact about the document and not about the commit it was measured at.
- **`ANCHORS.tsv` carries a `path` column beside its `resolved` column**, so
  the one place where equal shas would be ambiguous is not ambiguous.

---

## WHAT IS STILL OPEN

- **The 15 `%h` sites are not treated**, and 6 of them are in the defect
  classes. They are in eleven other tickets' directories. This audit counts
  and names them; treating them is not this audit's to do, and rewriting
  another ticket's instrument to make this ticket's number come out is the
  failure the arc exists to avoid. **Converted to property-derived by this
  audit: 0 of 28**, written as `0`.
- **The 3 ungated external spenders are not gated.** Two are mg-8d5e's and
  one is mg-2c77's.
- **`LAST_TOUCHING_G1` and `NTH_TOUCHING_1` remain ungateable by name.** The
  fix is two keys in `ANCHOR_OF`, in another ticket's file.
- **The floor's 120 is a lower bound**, and the five further commands named
  above are unenumerated.

---

## A FORECAST THIS TICKET MAKES ABOUT ITSELF

mg-b2af forecast that the refinery would rewrite its shas and that its
transcripts would name commits that no longer exist on `main`. **It was
right, and this deliverable pins `06c9271`, `14c6c3b`, `b1c3467`, `fba5f63`
and `ea97d0a` — all five of which are about to be rewritten again if any of
them is still on this branch.**

So every content claim here is made with **`git patch-id --stable`**, not with
`merge-base --is-ancestor`: **ancestry gives a FALSE NEGATIVE after a
rebase.** `selftest_0ba7.py` (8) constructs the case — a cherry-pick, a
different sha, the same patch-id — so the tool this forecast depends on is
demonstrated rather than asserted.

**If a re-run after the merge prints different shas in `a2`'s tree table and
the same 0-crossings beneath it, that is this forecast being confirmed, not a
defect.**

---

## THE FILES

| file | what it is |
|---|---|
| `PREDICTIONS.md` | 25 scored rows plus 6 disclosed measurements, committed at `e5d37a4` before any script existed |
| `lib_0ba7.py` | the apparatus: a second classifier written from mg-330a's docstring, the import-resolved closure, the floor, both label rules, `Report` |
| `selftest_0ba7.py` | **52 assertions on constructed inputs**, including both of this instrument's own defects |
| `a1_population.py` | the census re-derived by AST; two classifiers row by row; the closure against the name-list |
| `a2_oldest.py` | the `OLDEST` boundary at five trees; the absorption constructed |
| `a3_gate.py` | who spends, repo-wide; the two ungateable anchors; the drift constructed |
| `a4_labels.py` | KIND and SCOPE recounted, and the rule tested against a constructed path |
| `a5_resolution.py` | distinctness by resolution, constructed |
| `a6_floor.py` | the floor: revisions produced without the word `log` |
| `out_*.txt` | the committed transcripts of the run that ships |
| `out_a4_labels_FIRSTFORM_miss3.txt` | the scorer defect, regenerated and labelled as regenerated |
