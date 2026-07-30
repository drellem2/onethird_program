# mg-a4ef — PREDICTIONS, WRITTEN BEFORE ANY EDIT AND BEFORE ANY RUN

mg-73df predicted all 60 of its battery cells before running them, missed 4, and kept the
wrong predictions as written. This file is written to the same rule: **nothing below is
edited after a run.** Outcomes are recorded in `OUTCOMES.md` beside it, and every miss is
recorded there rather than fixed here.

Written 2026-07-30, before touching `code/species_7d75/t6_fock_and_record.py`, before
touching the document, and before writing a line of `s1_extent.py`.

---

## A. What the unified detector finds on the CURRENT tree (before my fix)

The list is the union of `check_doc.py`'s ten `STRICKEN` rows and `w3_scope.py`'s two
`FORBIDDEN` rows. The targets are `code/species_7d75`, `code/species_repair_6f61`,
`code/species_remainder_f8fa` and the document.

| # | prediction |
|---|---|
| **P1** | In `code/species_7d75`, X3 (*"0 failures on 4399 basis elements"*) is asserted at **exactly 2** places: `t6_fock_and_record.py:149` and `out_t6_fock_and_record.txt:66`. |
| **P2** | In `code/species_7d75`, the AM §17.5 quotation (X6/X7) is asserted at **exactly 2** places, both in `t6_fock_and_record.py` (lines 15–16), **and not** in `out_t6_fock_and_record.txt` — it is a module docstring and docstrings are not printed. |
| **P3** | **§9 row 6's stricken inequality direction — `y(i) ≤ y(j)` — is still asserted at source in `code/species_7d75`, in ASCII, in at least one file.** This is not on mg-73df's list of four and is my main beyond-brief bet: the Aguiar–Ardila definition was corrected in the document from `≤` to `≥`, and a braid-cone docstring is exactly where the uncorrected form would survive. I predict **≥ 1 hit**. |
| **P4** | None of the other seven stricken statements (§8 C3's extremal claim, the Aguiar–Ardila *"braid cone"* sentence, §2.2's control count, §5 control (ii)'s *"fires hard"* numbers, §6 item 6's *"measured, not proved"*, §10 item 2's errand, S12's non-location) is asserted anywhere in `code/species_7d75`. **0 hits each.** |
| **P5** | `code/species_repair_6f61` and `code/species_remainder_f8fa` come back **0 still-asserted**, as mg-73df reported. |
| **P6** | Scanning **my own tree** `code/species_repair_a4ef` will trip my own detector, because `stricken_a4ef.py` contains every forbidden string by construction. I predict I hit this and have to exclude the list module by name — a self-inflicted false positive of the same family as `w3_scope.py`'s recorded false negative. |

## B. Y2 at source — the beyond-brief half of the wording finding

| # | prediction |
|---|---|
| **P7** | §0's *"the left side **is** Solomon's descent algebra"* is **not** the only occurrence. `code/species_7d75/t4_one_operation.py` carries the same plain reading at source, unmarked. I predict **exactly 1** occurrence in the code trees. |
| **P8** | After correcting both, a regex for *"left side is Solomon's"* not followed within 2 lines by *anti* returns **0** across document and code. |

## C. What changes, and what must not, when I fix the source

| # | prediction |
|---|---|
| **P9** | Re-running `code/species_7d75/run_all.sh` after editing `t6_fock_and_record.py`: **exactly one** committed output changes — `out_t6_fock_and_record.txt`. The other six (`out_selftest.txt`, `out_t1`–`out_t5`) regenerate **byte for byte**. |
| **P10** | `T6 TOTAL BAD: 0` is unchanged, and every other `TOTAL BAD` in that tree stays 0. The correction is to what the file *says*, not to what it *computes*. |
| **P11** | The docstring fixes for Y5 (`w3_scope.py` 6→12, `r2_columns.py` 40→45) change **no** committed output: neither module docstring is printed. |
| **P12** | Re-running `code/species_repair_6f61/run_all.sh` after my document edits: `CHECK_DOC: PASS (0 problems)`. The box I delete is the *first* copy, whose opening is *"THE SAME LIMITATION APPLIES TO THIS SECTION"*; `check_doc.py` requires *"THE SAME LIMITATION APPLIES TO §14 ITSELF"*, which is in the surviving §14.2. |
| **P13** | `out_r1_smallest.txt`, `out_r2_columns.txt`, `out_r3_quotes.txt` and `out_selftest.txt` in `species_repair_6f61` regenerate **byte for byte**; only `out_check_doc.txt` changes, and only because I add an extent line to it. |
| **P14** | **mg-a61f's battery, re-run unmodified after my document edits, is still byte-identical at 456 328 assertions**, `A4 TOTAL BAD: 1` and 0 elsewhere. Its anchors are quoted strings in §0–§13; I touch one word in §0's headline box and a box in §14, and I predict neither is an anchor. |
| **P15** | `w3_scope.py` re-run against the pre-repair tree at `83ac472` still reports **12 problems** after I add its extent declaration; against the repaired tree, **0**, i.e. `W3 SCOPE: PASS`. |

## D. The seam, after the fix

| # | prediction |
|---|---|
| **P16** | After deleting the first §14 limitation box, a general duplicate sweep over all block quotes in the document finds **no pair above 40 %**; the previous maximum was 56 %. |
| **P17** | Deleting that box removes the *only* occurrence of *"the five items in the banner at the top"*, so no count-of-the-banner claim survives anywhere; the banner's own *"Eight things changed"* is then unopposed. |
| **P18** | §14.3's opening — *"§14.2 predicted that a further defect, if one existed, would be outside every beam"* — still reads correctly against the surviving §14.2, **with no edit to §14.3 needed**, because the sentence it quotes is in §14.2 and not in the deleted copy. |
| **P19** | After the fix, no passage in the document says *"an eighth defect, if there is one"*, and no passage calls mg-f8fa's filing *"shelved"*. |

## E. A defect I expect to find in my own instrument

| # | prediction |
|---|---|
| **P20** | I will find at least one defect in my own checker before it is finished, of the same family as the two mg-73df kept on its record and the one `w3_scope.py` kept on its. If I find none, that is itself reportable and I will report it as such rather than claim a clean build. |

## F. What I predict I will NOT be able to do

| # | prediction |
|---|---|
| **P21** | `code/species_audit_73df`'s committed outputs will **stop** regenerating byte-identically, because the tree they measure changes. I will **not** regenerate them: an audit's committed output is the record of what it found when it looked, and rewriting it to say `0` would erase the finding this ticket exists to close. |
| **P22** | Y2 stays **wording**. I am changing one phrase in the document and one docstring at source; I am **not** establishing `Sol(S_n) ≇ Sol(S_n)^{op}`, and no new mathematics is added by this repair. |
