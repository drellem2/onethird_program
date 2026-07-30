# mg-6cb9 — predictions, written before any probe ran

Written after reading `e8fbd4f`'s source and **before** executing a single probe. Not edited
afterwards. `OUTCOMES.md` scores it and keeps the misses.

The audit target is `e8fbd4f` (mg-d633), which repairs mg-7dd3's A1, A2, B1 and C1 against
mg-a4ef / `106e121`. mg-7dd3 measured four printed extents and found **two wider than what the
code reads**. This instrument re-measures **all four**, from both sides, at sites of my own
choosing, and demonstrates the cross-section check firing.

## How these probes differ from mg-d633's own E3

mg-d633's 28 probes run against a `shutil.copytree` **sandbox that contains no `.git`**. I
predict (P-S1) that `s1_extent.py`'s controls **(a)** at `ebecd89` and **(b)** at `83ac472`
therefore print *"git unavailable — SKIPPED"* in every one of those probes, and since
`bad += ctl` those two controls contribute nothing to any exit code E3 recorded. My probes
mutate the **real worktree in place** and restore it, so every checker runs against a live git
repository with all four of its controls armed. `git status --porcelain` is asserted empty
before and after each probe.

## Predicted exit codes

`IN` = the mutation is inside what the printed extent claims → the checker **must fire** (exit
1). `OUT` = outside it → the checker **must stay silent** (exit 0). `WIDE` = a site the printed
extent claims and I predict the code does not read.

### `check_doc.py` — *"over ONE FILE … a SECOND file for section C4's five assertions and for nothing else … It reads no code"*

| id | dir | mutation | predicted exit |
|---|---|---|---|
| Q0a | — | unmutated | 0 |
| Q1 | IN | un-strike X6b (`y(i) ≤ y(j)`) in the document | 1 |
| Q2 | IN | delete C4's `2 of 45` anchor from `…-Repair.md` | 1 |
| Q3 | OUT | X6a asserted live in a third `docs/*.md` | 0 |
| Q4 | OUT | X6a asserted live in `code/species_7d75/README.md` | 0 |
| Q5 | OUT | an un-struck X1 planted in `…-Repair.md` away from C4 — tests *"and for nothing else"* | 0 |

### `w3_scope.py` — *"X4 and X5 plus the character-ring rule, over ONE tree: N file(s), every regular file in it, with no extension rule"*

| id | dir | mutation | predicted exit |
|---|---|---|---|
| Q0b | — | unmutated | 0 |
| Q6 | IN | X5 asserted in a committed `out_*.txt` in `species_7d75` | 1 |
| Q7 | IN | X4 in a NEW **extensionless** file `species_7d75/NOTES` | 1 |
| Q8 | OUT | X5 in `species_remainder_f8fa/README.md` — another tree | 0 |
| Q9 | OUT | X7, not on w3's two-item list, in `species_7d75/README.md` | 0 |
| **Q10** | **WIDE** | X4 in `species_7d75/sub/leak.md` — a **subdirectory** of the one tree | **0 — silent** |

### `s1_extent.py` — *"11 corrections over the document and 4 code trees, EVERY REGULAR FILE of each, less the 5 named above and the N named as undecodable"*

| id | dir | mutation | predicted exit |
|---|---|---|---|
| Q0c | — | unmutated | 0 |
| Q11 | IN | X6a in `species_repair_6f61/run_all.sh` — a `run_all.sh` in a tree mg-d633 did not probe | 1 |
| Q12 | IN | X1 in a NEW **extensionless** `species_repair_a4ef/NOTES` | 1 |
| Q13 | IN | X4 in a committed `out_*.txt` — the extent says these are **not** skipped | 1 |
| Q14 | OUT | X1 in `species_repair_a4ef/PREDICTIONS.md` — a NAMED exclusion | 0 |
| Q15 | OUT | X1 in `code/species_extent_d633/README.md` — a tree the extent disclaims | 0 |
| Q16 | OUT | X1 in `docs/OneThird-Audit-mg-7dd3-Extent-Repair.md` | 0 |
| **Q17** | **WIDE** | X3 in `species_7d75/sub/leak.md` — a **subdirectory** of a named tree | **0 — silent** |
| Q18 | IN | a non-UTF-8 file added to `species_7d75` | 0, **and named** in the undecodable list |
| Q17e | — | with Q17's subdirectory in place, run `e1_extents.py` | **0 — the extent-checker does not catch it** |

**Why I predict Q10, Q17 and Q17e.** Both repaired scans read `os.listdir(root)` and `continue`
on anything that is not `os.path.isfile`. A directory is dropped **by a rule no sentence
carries** — which is the exact wording mg-d633 used for the extension filter it removed. The
undecodable list is printed *"one by one, as it is found, so it cannot grow unseen"*; a
subdirectory grows unseen. And `e1_extents.py`'s own `regular(tree)` helper is a non-recursive
`os.listdir` too, so the file that measures whether the printed extent is true **shares the
blind spot it is measuring**. If these three come back 0/0/0 the repair *narrowed the code's
reach in no direction but widened the printed claim from "4 trees" to "EVERY REGULAR FILE"* —
a new false extent created in the act of repairing an extent.

### `s2_seam.py` — *"every passage over 60 normalised characters compared at 90 %; those over 300 compared again at 45 %; tables and headings in no passage; at or below 60 characters compared to nothing at all"*

| id | dir | mutation | predicted exit |
|---|---|---|---|
| Q0d | — | unmutated | 0 |
| Q19 | IN | a 60–300 char **prose** paragraph duplicated verbatim | 1 |
| Q20 | IN | a >300 char paragraph altered to land strictly **between 45 % and 90 %** | 1 |
| Q21 | OUT | a heading duplicated | 0 |
| Q22 | OUT | a ≤60 char passage duplicated | 0, **and listed** |
| Q23 | OUT | a 60–300 char passage repeated at 45–90 %, not 90 %+ | 0 |
| Q24 | OUT | a table row duplicated | 0 |

**Q20 is the probe I expect to matter.** Every one of mg-d633's three `s2_seam.py` IN-probes
(P14, P14b, P15) is an **exact** duplicate, so all three fire on the 90 % said-twice pass that
mg-d633 added. **The 45 % sweep — the original threshold, the one that was there before the
repair — is exercised alone by no probe in that instrument.** I predict Q20 fires; if it does
not, the 45 % half of the printed extent is a branch nothing reaches.

### `e2_crosssection.py` — the cross-section check

| id | dir | mutation | predicted exit |
|---|---|---|---|
| Q0e | — | unmutated | 0 |
| Q25 | IN | §0's AM §17.5 misquotation restored verbatim — B1 itself | 1 |
| Q26 | IN | §4's X7 strike restated verbatim in **§9 of the same document** | 1 |
| Q27 | IN | a Bratteli strike restated in another section of the Bratteli document | 1 |
| Q28 | OUT | the same restatement placed in a **different** document | 0 |
| Q29 | OUT | the restatement in a paragraph that says it was `corrected` | 0 |
| Q30 | OUT | the restatement inside another `~~strike~~` | 0 |

## Predictions that are not exit codes

* **P-STALE.** `e8fbd4f`'s committed `out_e2_crosssection.txt` prints an extent of **100
  markdown files**. I predict that number is **false at the tree it was committed into** — the
  repair commit itself adds four `.md` files, and its own parent chain adds a fifth. I predict a
  clean re-run at `e8fbd4f` prints **105**, and that the shifted line numbers in that output
  place the run at `c7f9673` — **two commits before the commit that ships it**. The arc's
  Appendix A already carries *"A COMMIT THAT MEASURES SOMETHING IT ALSO MODIFIES MUST PUBLISH
  THE POST-COMMIT MEASUREMENT"* (`e16e41c`, mg-8e30). Predicted: the repair document's own
  document is **not in the sweep whose output ships as evidence for it**.
* **P-S1.** `s1_extent.py` in a `.git`-less sandbox prints *"git unavailable — SKIPPED"* for
  controls (a) and (b). Predicted: yes, in mg-d633's E3 sandbox.
* **P-NARROW.** The repair says which of the four repairs narrowed the claim and which widened
  the code: three widened, one (`check_doc.py`) narrowed. Predicted: this is accurate and
  stated in `README.md`, in the repair document, and **in each checker's own printed output**.
* **P-PLACE.** Each of the four corrections is reachable from where its false belief lived,
  because in all four cases the false belief lived in the checker's own printed extent line and
  the correction is printed there. B1's false belief lived in §0 of the document and is
  corrected at §0. Predicted: all five reachable.
* **P-SEAM.** `s2_seam.py`'s 90 % said-twice threshold has, per mg-d633, 37 points of headroom
  (worst live pair 52.8 %). Predicted: I reproduce 52.8 % independently. For `e2`, I predict the
  largest **non-firing** shared run in the repository sits well below `RUN_FRAC = 0.50`.
