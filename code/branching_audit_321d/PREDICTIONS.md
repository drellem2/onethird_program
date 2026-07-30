# `mg-321d` — exit codes and answers predicted BEFORE running

Written before `h1`–`h4` were run for the first time. The misses are **kept as
written** and marked; nothing here is edited to agree with the run.

The target of the audit is `673b4c0` (`mg-58da`), the repair of the two
questions `mg-d330` left open about `code/branching_audit_a218/c1_branching.py`.

## What I expect to find, in words, before measuring it

* **A and B ARE kept separate.** From reading the document once: `§1` is B and
  `§2` is A, the bottom-line table gives them separate rows, and I expect to
  find no single sentence that is offered as the verdict on both. I predict
  `h1` books **0** findings on the separation.
* **B's re-run really happened.** `g1 (iii)` re-runs `c1@286d5030` against the
  target `@286d5030` and diffs against the committed record. I predict my own
  independent redo agrees: **198 cells, 0 disagreements, exit 0, byte-identical**
  to `git show 286d5030:…/out_c1_branching.txt`, and the revision is named in
  full in the prose.
* **All 24 are classified.** I predict `g3`'s table carries **24 rows**, each
  with one of the three labels, and that the census `0 / 24 / 0` is what the
  rows say — not just what the summary says.
* **The set-level property: all five were re-run, and it is 4 of 5.** I predict
  `g4 (iii)` runs all five in place, that `c3_withdrawal.py` is the one red, and
  that the two members that state vertex figures agree with each other 24 of 24.
* **THE GRAIN ERROR IS IN THE FIX.** This is the prediction I most expect to be
  right, and it is why `h2` exists: `g1` compares `c1_branching.py` **by file
  sha** and books a difference as *"the measuring half of the reproduction is
  not the same code"*. This ticket's own edit changed that file. So I predict
  `g1` **exits 1 on the tree as committed**, with a finding its own `§1` refutes
  — the file moved, the measurement did not.
* **`g4`'s attribution is computed against a moving HEAD.** `touched_13b2` is
  `sha@286d5030 != sha@HEAD` and `touched_58da` is `sha@HEAD != sha@worktree`.
  Once this ticket's commit *is* HEAD the second is empty and the first absorbs
  `c1`. I predict `g4` at HEAD says **`ed9cde4` touched 2 of the five** — which
  is false of `git log` — and **this ticket touched 0**.

## Exit codes, predicted

| | script | predicted |
|---|---|---|
| **Q1** | `python3 selftest_321d.py` | **0** |
| **Q2** | `python3 h1_questions.py` | **0** — the separation holds and B and A are each answered |
| **Q3** | `python3 h2_grain.py` | **1** — 2 findings: `g1`'s file-grain provenance check, and `g4`'s attribution |
| **Q4** | `python3 h3_setlevel.py` | **1** — 1 finding: 4 of 5 green, `c3` open. Everything else agrees |
| **Q5** | `python3 h4_mine.py` | **1** — 2 findings, both mine, both below |
| | `./run_all.sh` | **1** |

## The two things I chose myself, and what I predict of each

Neither is named by the ticket. Both are picked because they are the same
*shape* as the arc, one level in.

**M1 — `g1`'s byte-for-byte confirmation of the committed record never reads
the file in the tree.** `g1` compares `git show 286d5030:out_c1_branching.txt`
against a re-run of the code at `286d5030`. Both sides are historical objects.
The document's `§3` says the record is *"checkable rather than merely
preserved"*. I predict: **corrupt `out_c1_branching.txt` in the working tree and
`g1`'s byte-check stays green** — it is a check on git, not on the tree a reader
reads. Predicted: the byte-check does not fire (**a miss for the check**, a hit
for the prediction).

**M2 — the narrowing covers ABSENCE but not MISREAD.** The repair routes *"I
cannot find the cell"* to `SELF-ERROR`. It does not route *"I found something
that is not the cell"* anywhere: the count regex still matches **any** line of
seven integers whose first is one digit, anywhere in `T1b2`, first match wins.
`lib58da.py`'s own docstring says so and neither the repair nor the document
books it. I predict: a target carrying a stray seven-integer row and no vertex
table makes the **repaired** `c1` report **6 FINDINGS against the target**,
`SELF-ERRORS 0` — the original defect's exact shape, one parser branch over.

## Where I expect to be wrong

I expect at least one of these to miss. Most likely candidates: the exact
finding count of `h3` (`g4` may already book something I think it does not), and
M2's count of 6 — the stray row lands under one `beta`, so 6 is the arithmetic,
but `c1` may fall into the SET branch first and give 0.

## Q6 — added after Q1–Q5 had run, and predicted before it was written

`h5_doccheck.py`. This arc has punished, repeatedly, a document whose figures no
instrument reads — and punished hardest the gate that asks whether *a* correct
value occurs somewhere in a file rather than reading the value **at the site a
reader reads** (`mg-8a5c`/`mg-a318`). So the figures in this audit's own
document are gated: each is located by its anchoring sentence or table row, the
number is read out of **that** line, and it is compared against the number
derived from the committed `out_h*.txt`.

Predicted, before writing it: **exit 0**, every gated figure agreeing, and
**every** corruption probe firing — one per gated figure, each mutating that
figure alone in a scratch copy of the document, plus a null probe that changes
an unrelated word and must stay green. If any probe fails to fire, the gate is
reading the file rather than the site and is worth nothing.

---

# ACTUAL — filled in after the run. The misses are kept as written above.

| | script | predicted | actual | |
|---|---|---|---|---|
| **Q1** | `selftest_321d.py` | 0 | **0** (60 assertions) | HIT |
| **Q2** | `h1_questions.py` | 0 | **0** | HIT |
| **Q3** | `h2_grain.py` | 1, **2** findings | **1**, **3** findings | **exit HIT, count MISS** |
| **Q4** | `h3_setlevel.py` | 1, 1 finding | **1**, 1 finding | HIT |
| **Q5** | `h4_mine.py` | 1, 2 findings | **1**, 2 findings | HIT |
| **Q6** | `h5_doccheck.py` | 0, every probe fires | **0**, **16 of 16** fire, null probe green | HIT |
| | `./run_all.sh` | 1 | **1** | HIT |

**Q3 is the miss and it is kept as written.** I predicted two findings from
`h2` and got three. The third is *"`g1`'s live `FINDINGS` (1) differ from its
committed record (0)"* — I had folded the record-vs-live disagreement into the
grain finding when writing the prediction, and the script books it separately
because they are different claims: one is *why* `g1` goes red, the other is that
the documented `REPRODUCE` command does not reproduce the committed output at
all. A miscount of findings is a bookkeeping error; a finding that does not fire
is a dead channel. Both fired.

Everything substantive was predicted correctly:

* **A and B are kept separate** — `h1` books 0. Different answers, different
  scripts, no cross-reads, and both re-derived here.
* **B's re-run at `286d5030902d09a7eb336a4a5dec18bf7b9de64c` reproduces** —
  198 cells, 0 disagreements, exit 0, byte-identical to the committed record.
* **24 of 24 classified**, and my classification agrees with `g3`'s rows,
  `g3`'s rows agree with `g3`'s summary, and the document's three buckets sum
  to 24.
* **`g1` exits 1 on the tree as committed**, with the file-grain finding, and
  its own `PREDICTIONS.md` records `ACTUAL 0 HIT`.
* **`g4` says `ed9cde4` touched 2 of the five and this ticket touched 0**,
  which `git log` refutes.
* **M1: 0 of 3 probes fire.** Corrupting and then deleting the committed record
  in the working tree both leave `g1` printing `BYTE-IDENTICAL`.
* **M2: 4 of 4 directions predicted correctly**, including the count of **6**,
  and including the null probe that had to stay green.

## THE MISS INSIDE THE INSTRUMENT, KEPT

On its first run `h3`'s reader for `mg-2060`'s `out_b1_branching.txt` matched
only the header form `--- beta = b ---`. `mg-2060` writes `beta=3:`. The reader
recovered **0 of 24** cells and the cross-comparison booked **four findings**
against an instrument that agrees with the target at 24 of 24 — *absence
rendered as disagreement, inside the instrument auditing that exact defect, on
its first run.* It is recorded in `h3_setlevel.py`'s own source and in the
README. The fix is in two places, not one: the pattern accepts both forms, and
a source the script cannot read now goes to the **SELF-ERROR** channel and is
excluded from the compared population — so the same mistake cannot be silent
next time. `selftest_321d.py` grew the anchoring assertions because of it.

And a third, in `h5`'s first draft: `derive()` anchored `PARSER ARTIFACT` on a
substring that matches **three** lines of `h1`'s output. It did not guess — it
refused, booked a `SELF-ERROR` and reported *"figures gated: 1 of 17"*. That is
the behaviour the second half of the `h3` fix installed, working on its first
opportunity: an ambiguous anchor shrinks the population visibly instead of
certifying a figure read off the wrong line. Two document figures were also
un-gateable as first written (`c0_repro`'s figure shared a line with the pair
count, and the assertion count appeared only in the README); **the document was
changed to make them gateable**, which is the right direction — the gate was not
loosened to fit the prose.

A smaller one, same run: the first anchoring assertion placed its poison row
*before* `(ii)`, which is *inside* subsection (i), so it asserted the opposite
of what it meant. Caught by the assertion failing, fixed, and the complementary
assertion (the same row inside (i) **is** read) added beside it so the check
cannot pass by the reader being inert.
