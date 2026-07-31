# mg-eaef — every prediction, registered before its run

Registered 2026-07-31, before any script in this directory was executed. Two of
them missed. **The misses are kept as written**, with what actually happened
beside them, because a prediction table edited after the run is a table that
predicts nothing.

## Exit codes

| script | predicted | actual |
|---|---|---|
| `selftest_eaef.py` | 0 | 0 |
| `e1_operand.py` | 0 | 0 |
| `e2_bound.py` | 0 | **1 on the first run — MISS**, 0 after the claim was restated (see e2.4) |
| `e3_derived.py` | 0 | 0 |
| `e4_remeasure.py` | 0 | 0 |
| `e5_floor.py` | 0 | **1 on the first run — MISS**, 0 after the splice was fixed (see e5.4) |
| `run_all.sh` | 0 | 0 |

Both misses were defects in **this** instrument, not in the subject, and both
were caught by a `[BROKEN]` claim rather than by inspection — which is what the
claim/finding split is for.

## e1 — the operator move, and the two rungs below it

| # | prediction | outcome |
|---|---|---|
| e1.1 | delete the ORDER half alone → BYTE-IDENTICAL, exit 0 | HIT — 23,695 bytes, exit 0 |
| e1.2 | delete the WIDTH half alone → CHANGES, exit 1 | HIT — 24,909 bytes, exit 1 |
| e1.3 | every NESTED boolean operand deleted alone → BYTE-IDENTICAL, exit 0 | **MISS** — 4 of 4 CHANGE, exit 1. Registered on the assumption that anything the sweep skips is something the battery cannot see; the opposite is true here, and it makes the finding stronger rather than weaker |
| e1.4 | the rung-7 assignment patch → BYTE-IDENTICAL, exit 0, and the predicate's answer on the separator pair flips | HIT — byte-identical at exit 0; `False` at gate `shape` → `True` at gate `parity` |

The count in e1.3 was also registered wrong: "2 (mat_eq)" was written, and there
are **4** — two in `mat_eq` and two in `proper_ideals`.

## e2 — the bound

| # | prediction | outcome |
|---|---|---|
| e2.1 | census re-derives: `face_complex.py` 73/5/11/11/1002, `posets.py` 6/1/2/1/55 | HIT |
| e2.2 | the `operands` column reads 2 for `posets.py` and the sweep deletes 0 there | HIT |
| e2.3 | explicit boolean operands in neither census column: predicted 2 | **MISS** — 4 |
| e2.4 | *(not registered in advance)* the first writing of the "sweep does not visit posets.py" claim asserted that `_is_transitively_closed` occurs **once** in the subject's transcript. It occurs **three** times — twice in the NOT SWEPT sentence, which names both its clauses, and once in the compounds table. The claim was about the sweep's rows and was written as a count over the whole file: the same substitution of a convenient population for the intended one that this audit is looking for, committed by this audit. It is restated over the enumeration line it is actually about, and the original is kept in a comment at the site | MISS, kept |

## e3 — the derived declaration

| # | prediction | outcome |
|---|---|---|
| e3.1 | control: `AFTER-6` (1,0,0,7) and `AFTER-4` (0,1,0,4) on the unedited copy | HIT |
| e3.2 | direction W: `AFTER-6` gains one statement and more nodes, keeps `absorb_trace` | HIT — (1,0,0,7) → (1,1,0,18) |
| e3.3 | direction K: `AFTER-4` → 0 statements, ≥1 boolean clause, function becomes `gate_violations` | HIT — (0,1,0,4) in `absorb_trace` → (0,0,1,11) in `gate_violations` |
| e3.4 | no other tag's declaration moves in either direction | HIT — 1 of 11 each way, and it is the tag that was edited |

## e4 — the re-measure

| # | prediction | outcome |
|---|---|---|
| e4.1 | the population is still 11 | HIT |
| e4.2 | 8 UNDERSTATE / 3 AGREE / 0 OVERSTATE / 0 MIXED | HIT |
| e4.3 | the three that AGREE are `BEFORE-1`, `AFTER-3`, `AFTER-4` | HIT |

## e5 — the floor item

| # | prediction | outcome |
|---|---|---|
| e5.1 | `d2_deletion.py` re-run unmodified at HEAD exits 1 with exactly 1 BROKEN | HIT |
| e5.2 | 8 commits have touched `face_complex.py`, 2 have a two-clause `shape` guard, and the newer is not the pin | HIT |
| e5.3 | with the named pair added, deleting the ORDER clause CHANGES the artifact at HEAD and at `b6bc2ef` | HIT — after e5.4 |
| e5.4 | *(not registered in advance)* the first writing of the spliced control row produced an unterminated string literal, so both patched trees failed to run and produced a **0-byte artifact**. Both comparison claims read BROKEN — correctly, since `IDENTICAL` against an empty baseline is exactly the "the run failed the same way" reading a deletion test must never make. A guard now raises rather than comparing when a baseline is empty | MISS, kept, and the guard is the fix |
