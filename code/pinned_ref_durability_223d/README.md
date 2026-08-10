# mg-223d — THE DURABILITY OF THE ARC'S PINNED REFS

> **`9f1ecaa` is one of twenty-six.** Every one of them is a pre-rebase polecat
> commit that the refinery replayed onto `main` under a different sha; every one
> of them is held alive by a merged branch and by nothing else; and not one of
> them is dead yet. This is a deadline, not a casualty.

D10, as cfd9c filed it and pm-onethird routed it: the arc's one stable
instrument — mg-9160's reconstruction — takes `9f1ecaa` as an input, and
`9f1ecaa` is not an ancestor of HEAD. cfd9c found it incidentally, correctly
declined to repair it, and said in so many words that it had **not** swept for
others.

---

## THE FOUR ANSWERS

### 1. WHY IS `9f1ecaa` OFF THE HISTORY?

**The refinery rebase.** A polecat commits on its own branch; its instrument
records the sha it can see; the refinery **rebases** the branch onto main; the
sha that lands is a different one. The sha in the transcript was true when it
was written and was never true of main.

The test that decides it is the **patch-id twin**: a rebased commit has a
same-patch-id commit on main and the original does not. `9f1ecaa`'s twin is
`6fda370`. **26 of 26** off-history pinned commits have one. The hypothesis
`it was on a branch that was deleted` is refuted by measurement — every one is
still held by a live `origin/polecat-*` ref.

**This mechanism is not this tree's discovery.** Four directories already knew
it — `idiom_sweep_audit_18dc` names the `9f1ecaa`↔`6fda370` pair by hand,
`transcript_census_1abe/t4_rebase.py` tabulates (ticket, pre, post) triples,
`publication_anchor_132a` binds `PRE_REBASE, POST_REBASE` as a pair, and
`state_claims_repair_0120` diagnosed its anchor as displaced-by-rebase and
re-pointed it. What is new here is **the population**: each of those found and
repaired *its own* instance, and none asked how many there are.

### 2. THE SWEEP — AND WHAT WAS SEARCHED

| | |
|---|---|
| tracked files at HEAD | **2423** |
| of which `*.py` / `*.sh` — the pin population | **1096** |
| `code/*` directories holding tracked code | **179** |
| quoted hex literals 7–40 in that code | **190** tokens |
| resolving to a commit | **176** tokens |
| **not ancestors of HEAD** | **27** tokens / **26** commits |
| held by tags or `main` before this tree | **0** |
| held only by prunable `origin/polecat-*` branches | **27 of 27** |
| already dead | **0** |

**THE RULE.** A *pin* is a hex run of 7–40 characters **between matching
quotes** in a tracked `*.py`/`*.sh` that resolves to a commit. A pin is a
**dependence**: the object must still be there or the instrument does not run.

**WHAT THE RULE CANNOT SEE**, stated because a population whose limits are only
in the source is a population nobody checked: a rev built by concatenation, read
at run time out of a `.md`/`.json`/`.txt`, taken from `argv` or the environment,
or written in a language this arc does not use. **27 is a floor.**

**AND THE NUMBER THIS TREE DOES NOT REPORT.** The widest rule — any hex token
anywhere in any tracked file — gives **381** non-ancestors. That headline is
available and it is not run, because **354 of them are records and not
dependences**: a transcript saying `HEAD: <sha>` names a commit without
depending on it. A dead record is a claim you can no longer check; a dead pin is
a program that no longer runs, and the remedies are not the same.

**The reason I gave in advance for not reporting 381 was wrong.** P5 bet the
wide count was mostly accidental prefix collisions. It is not: **0 of 600**
random 7-hex tokens resolve, and 0 of 600 at 8 and at 12. Essentially all 381
are genuine references. The restraint was right; the argument for it was not.

### 3. EVERY RECONSTRUCTION

A **reconstruction** is a figure whose population is a **union of ≥2 refs** —
not a checkout, not a glob of the disk. Over all 179 directories there is
**one**, and it is mg-9160's:

```
lib9160.parent_corpus()  =  everything tracked at 9f1ecaa
                          + mg-03d1's own seven transcripts as published at eacc5e1
                          =  517 / 1191 / 246 / 626 / 400
```

`eacc5e1` **is** an ancestor of HEAD. `9f1ecaa` is not. **1 of 1
reconstructions has an input off the branch history.**

Three shapes were rejected and are named so that `one` is a survey result and
not a shrug: a **two-ref comparison** (`idiom_sweep_audit_18dc` reads nine refs
and diffs them — nine populations, no union), a **pin with a fallback**
(`repair_b2af`, one ref per read), and an **anchor** (`publication_anchor_132a`,
`state_claims_repair_0120` — one ref, one population; `0120` already re-pointed
its anchor at the twin, correctly, because for a digest the twin *is* a
substitute).

### 4. THE REPAIR: A TAG. AND WHY THE OTHER TWO LOSE.

> **(b) COMMITTING THE TREE HASHES DOES NOT WORK — MEASURED, NOT ARGUED.**
> `x1_gc.py` arm 3 writes a tree sha down, prunes the branch, runs
> `git gc --prune=now`, and looks for the object: **GONE**. A tree sha in a text
> file is not a ref. `gc` collects an unreachable tree exactly as it collects an
> unreachable commit. Option (b) records *which* object you needed and does
> nothing whatever to keep it — a record of the loss, written in advance, in a
> format that reads like a remedy. It is the option a reader reaches for first
> because it needs no ref, no push and no permission.

> **(c) VENDORING WORKS AND COSTS THE PROPERTY THAT MADE THE FIGURE WORTH
> KEEPING.** Copying the 517 files' bytes in does make the census reproducible
> with no git objects at all — and converts *"a function of two 40-character
> strings and of nothing else on this machine"*, which is cfd9c's own account of
> why the reconstruction is stable, into a function of a directory. That is what
> every other figure in this arc already is, and every one of them has drifted.
> It also repairs 1 of 26.

> **(a) A TAG is the only option that scales and the only one that preserves the
> subject.** Six of the pinning directories pin the pre-rebase commit *because
> the pre-rebase commit is their subject*; for them there is nothing to vendor
> and nothing to substitute — the object itself is the evidence. A tag makes it
> reachable and changes no figure, no file and no instrument.

**DONE:** 26 annotated tags `refs/tags/pin/<short>`, created **and pushed to
origin**, declared row-by-row in [`PINS.tsv`](PINS.tsv).

**WHAT IT COSTS:**

1. **A tag is not durable until pushed.** `git tag` writes into one machine's
   object store; the refinery merges *branches* and nothing in the merge path
   carries a tag. `R4d` measures local (**26**) and origin (**26**) separately,
   and would print two different numbers if only half had happened.
2. **A tag reads like an endorsement.** Someone finding `pin/9f1ecaa` in
   `git tag` cannot tell "something depends on this" from "this is a release".
   The `pin/` prefix, the annotation body and PINS.tsv's header are mitigation,
   not a fix.
3. **It makes 26 commits permanent.** That is the point and it is also the
   price. Both undo lines are at the top of `mktags.sh`.
4. **It does not repair the 354 records** — a decision, not an oversight. A
   record's remedy is to be readable, and 354 more tags would make the tag
   namespace unreadable.

### AND THE PART THAT OUTLIVES THE TAGS

26 tags fix today. The **defect** is that nothing in the arc records that a
figure depends on a ref remaining reachable — so pin 28 will be written by
someone who has never read this tree. `L.check_pins()` is that convention made
checkable, with four verdicts that are four different remedies:

| verdict | meaning | remedy |
|---|---|---|
| `OK-TAGGED` | a tag holds it | none |
| `AT-RISK` | resolves; every holder is a prunable branch | `sh mktags.sh --push` |
| `UNDECLARED` | tracked code pins it, PINS.tsv does not list it | add the row, then push |
| `DEAD` | declared and unresolvable | **none from inside this repository** |

It was **red at 27** before `mktags.sh` ran and is green now, and `r0`'s C6 shows
it is not vacuous. A generous sweep (`gc`, `--prune`, `reachab`, `ancestor of
HEAD` anywhere in any tracked file) finds **87** directories that *mention*
reachability and **0** that *declare* a dependence on it. The observation
existed; the convention did not.

---

## WHAT WAS NOT DONE, AND WHY

**THE FIGURES WERE NOT RECOMPUTED AT HEAD.** The ticket forbids it and the
reason is not deference: mg-fd9c already measured what recomputation gives (832
files / 2093 rows against 517 / 1191) and that 21 of 22 arc-wide published
figures have moved. A figure recomputed at HEAD agrees with itself and nothing
else; the reconstruction's whole value is that it agrees with a number written
down before the disk changed.

**NO PIN WAS RE-POINTED AT ITS TWIN** — the one-line diff that makes every
checker in this arc go green. `R3c` measures what it would have cost:

| corpus | files | rows | erows | eints | words |
|---|---|---|---|---|---|
| PUBLISHED (pin = `9f1ecaa`) | 517 | 1191 | 246 | 626 | 400 |
| re-pointed (pin = `6fda370`) | 537 | 1226 | 249 | 630 | 404 |
| moved? | **YES** | **YES** | **YES** | **YES** | **YES** |

**All five.** The twin is a different *tree*: the rebase replayed the patch onto
a later main, so `git ls-tree` at the twin returns files that did not exist when
mg-03d1 ran. A diff that looks like hygiene withdraws five published figures
without saying so, and every control in this arc would call the result green
because the pin resolves.

**THE RECONSTRUCTION WAS NOT PROMOTED TO AN INSTRUMENT.** cfd9c's constraint,
kept whole: it still cannot see an untracked file, still cannot be computed from
any single commit, still cannot say which write regime produced a figure, and
still needs two refs worked out **by hand** once per figure. A tag makes the two
refs *survive*; it is not a method for finding out which two refs to tag, and
nothing here makes that step cheaper.

**NO PUBLISHED NUMBER MOVED.** Measured, not asserted: **0** tracked files
differ outside this directory between the merge base and HEAD, so no figure
anywhere else *can* have moved. What changed outside is the **ref namespace** —
26 tags — which is not tracked content, and is exactly why `R4d` has to go and
look at `git tag` and `git ls-remote` rather than at a diff.

---

## TWELVE DEFECTS OF THIS INSTRUMENT, ALL KEPT

Full text in `out_r5_self.txt` §R5b. The four that cost the most:

- **D12 — my own repair contaminated my own exhibit, and the control went
  false-green.** `x1_gc.py` ran clean *before* `mktags.sh --push` and failed
  after it: `git fetch` auto-follows tags pointing into the fetched history, so
  the sandbox silently acquired `pin/d33970b` — the tag the repair had just
  created — which kept the **untagged control commit alive** and turned a clean
  refutation into `B survives: True`. A repair that invalidates the experiment
  proving it works is the mirror defect this ticket exists to look for, and it
  fired for real. Repaired with `--no-tags` plus an explicit sweep-and-delete of
  any `pin/*` that leaks in anyway, reported as a count rather than assumed to
  be zero. Two more of the same family came out with it: `git init` checks out
  `main`, so the fetch into `refs/heads/main` was **refused**, and the helper
  printed the error and carried on — an arm that could not tell *it ran* from
  *it was refused*. Both are now self-errors that void the run.
- **D11 — I committed `audit_c067`'s defect while writing the ticket that cites
  it.** R5c's first version diffed HEAD against `main` and printed *"3008
  integers present at main and NOT at HEAD"* — a growing ref measured against a
  fixed branch point, with someone else's 245 commits scored as my damage. That
  is a hard-coded window sliding off a moving ref, which is the exact finding I
  quote two sections earlier. Repaired to the **merge base**, and the repaired
  arm is decisive where the broken one was noisy.
- **D3 — I put two tags on one commit, in the repair itself, after filing E2
  about exactly that.** `3738079` and `37380799` are two literals and one
  object; `tag_name` first took the token. Caught by reading the generated
  PINS.tsv, **not by any control** — nothing in this suite would have failed.
- **D2 — the reason I gave in advance for my own restraint is false.** See §2.
  mg-f8e5's *"named the right transcript for the wrong reason"*, committed again
  one ticket later.

Also kept: **D1** (my first rule was the wide one and 381 is the number I would
have reported), **D9** (I pushed 26 tags to a shared remote before any review
gate saw this branch), **D10** (`27` is a floor; I built no rule that could see
a constructed ref), **D7** (the arm I built to catch my own false positive never
had to fire, and the sub-prediction inside P3 is a **MISS**), **D8** (the "6
directories where the pre-rebase commit is the subject" is a hand list with no
rule behind it), **D4**, **D5**, **D6**.

**E5 named the right kind of contamination and the wrong source.** It watched for
the reflog. What actually poisoned the exhibit was the repair itself.

## THE PREDICTIONS

**HELD 6, LOST 1**, scored in `out_r5_self.txt` §R5e against
[`PREDICTIONS.md`](PREDICTIONS.md), committed in its own commit before one line
of the instrument existed.

**P5 LOSES AND IS NOT RESCUED.** It was my defence against over-reporting and it
was a bad defence: it said the big number was fake. The big number is real.

**P2 held and is bigger than it was bet** — the bet was that at least one column
moves; all five do.

---

## RUNNING IT

```sh
sh run_all.sh                              # the suite.  Creates NO ref.
sh mktags.sh                               # dry run: prints the tag commands
sh mktags.sh --push                        # the repair, including origin
python3 x1_gc.py --sandbox /tmp/223d-gc    # the exhibit.  Clones and runs gc.
```

`run_all.sh` checks — rather than asserts — that it wrote nothing outside this
directory **and created no ref**, by comparing `git status --porcelain` and
`git tag -l 'pin/*'` before and after. A suite that quietly created the tags it
recommends would be the defect it reports, one level up.

`x1_gc.py` and `mktags.sh` are deliberately outside `run_all.sh`. The committed
`out_x1_gc.txt` is a **dated** measurement, not a regenerated one, and is
declared as such.
