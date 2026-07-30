# mg-6cb9 — outcomes, scored against `PREDICTIONS.md`

`PREDICTIONS.md` was written after reading `e8fbd4f`'s source and before executing a probe. It
is not edited. This file scores it and records what went wrong **in this instrument**.

## Score

**36 exit-code predictions, 2 predictions about output text, 5 in prose. 3 wrong. All kept.**

| id | predicted | measured | kept as |
|---|---|---|---|
| **Q2** | `check_doc.py` exits **1** when C4's `2 of 45` anchor is deleted | **0** | **a finding, not a retune.** `2 of 45` is written **three times** into the file `check_doc.py` reads, and C4 is `flat(s) in flat(rep)` — a presence test. Deleting the copy a reader reads leaves the run green. A3b measures all five anchors: 19, 3 and 2 copies for three of them. This is mg-8a5c's *"the gate is a presence test"*, which mg-a318 repaired in the Hodge tree and mg-835f confirmed; the species tree still has it |
| **R29** | `e2` stays **silent** when the restatement is followed by a paragraph saying it was corrected | **fires, exit 1** | **the rule is narrower than I read it.** `e2` exonerates on the paragraph **carrying** the occurrence and on nothing else; I wrote the negation as the *next* paragraph. Kept as predicted, and **R29b added — not substituted** — putting the negation inside the same paragraph, where it is silent as it should be |
| **P-SEAM** | *"the largest non-firing shared run sits well below `RUN_FRAC = 0.50`"* | the largest non-firing run **clears the fraction outright** — 6 tokens at 100 % — and is stopped by `RUN_MIN` | **wrong about which half binds.** The seam is `RUN_MIN = 8` with **2 tokens of margin**, not `RUN_FRAC`. The prediction looked at the threshold the repair discusses and missed the one that actually bites. A3d reports both and probes the `RUN_MIN` one |

Everything else landed: the four widenings and the one narrowing each behave as their own
sentences say (A1g), both subdirectory probes came back silent as predicted (Q10, Q17), and
`e1_extents.py` confirmed the extent as true over the subdirectory it cannot see (Q17e).

## Three defects in this instrument. One inverted a result.

1. **A restored `.py` left LIVE BYTECODE behind, and it inverted A3d's seam probe.**
   A3a's `D5` disarms `kernd633.RUN_FRAC` from `0.50` to `2.00`, runs `e2`, and restores the
   source. Python validates `__pycache__/*.pyc` on **(source mtime in whole seconds, source
   size)**. `0.50` and `2.00` are the same number of bytes, and the restore landed in the same
   second as the write, so the stale bytecode **validated**. Every later `e2` run in the tree
   imported `RUN_FRAC = 2.00` from a file that says `0.50`, with `git status` clean throughout.
   A3d's seam probe therefore reported the 7-token strike as **firing** — the opposite of the
   truth — and `e2`'s control (a) reported *"0 findings, expected 1"*, i.e. **the detector
   reporting itself broken because of my harness**. Confirmed by unmarshalling the `.pyc` and
   reading `2.0` out of its constants. Fixed two ways (`-B` plus `PYTHONDONTWRITEBYTECODE`, and
   a purge of `__pycache__` on every restore of a `.py`) and asserted four ways in
   `selftest6cb9.py` §4. **`git status --porcelain` was clean the entire time this was
   happening**, which is why the restore contract alone is not enough and the self-test asserts
   the cache separately.

2. **Q22's needle matched a header that is always printed.**
   The first version looked for `compared by neither`; the run prints that phrase in capitals,
   so Q22 read `*** NOT NAMED ***` against a run that names the passage twice. Correcting the
   case would have made it pass **while still testing nothing**, because the header prints
   whether or not any passage is under the floor. The needle now points at the **passage text**.
   A needle that is always present is the presence-test defect in item Q2 above, committed by
   the file reporting it.

3. **A first attempt to reproduce `e2`'s control (a) outside `e2` silently mismatched on a
   combining character.** `K̄` pasted through a shell heredoc did not equal the `K̄` in the
   document, so my scratch reproduction reported 0 findings where the real run reports 1, and
   for a few minutes I read that as a defect in `e2`. It is a defect in reproducing by retyping.
   The instrument now runs `e2` as a subprocess and reads its output rather than re-implementing
   its controls.

## The one thing no list named, and why I chose it

The brief says: audit one thing no list names, and say what you chose. **I chose the
subdirectory.**

mg-7dd3 found two extents wider than the code. mg-d633 closed both by widening the code, and in
doing so replaced *"the document and 4 code trees"* with the much stronger **"EVERY REGULAR FILE
in each tree is read — there is no extension rule"**. That sentence is true today for one
reason: no tree under `code/species_*` contains a directory. Both scans reach it through
`os.listdir` and `continue` past anything that is not `os.path.isfile`, which drops a directory
**by a rule no sentence carries** — the exact phrase mg-d633 used for the defect it removed. The
undecodable list is printed *"one by one, as it is found, so it cannot grow unseen"*; this
exclusion grows unseen. And `e1_extents.py`, the file whose entire job is deciding whether a
printed extent is true, enumerates the tree with the same non-recursive `os.listdir` — so it
confirms the sentence over a file it also cannot see.

Nobody's list names it because a repair is checked against the defect it was written for. This
one was created in the act of the repair, by a sentence that got stronger while the code got no
deeper.
