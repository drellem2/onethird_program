# `code/species_repair_a4ef` — one list, every target, and the extent printed

**Work item:** mg-a4ef, on the independent audit **mg-73df** (`ebecd89`,
`docs/OneThird-Audit-mg-73df-Species-Repair-Final-State.md`).
**Subject:** `docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md` and the three code
trees under it — `species_7d75`, `species_repair_6f61`, `species_remainder_f8fa`.

```
cd code/species_repair_a4ef && ./run_all.sh     # ~5 s, pure Python 3, no network
```

Outputs: `out_selftest.txt` (133 assertions), `out_s1_extent.txt`, `out_s2_seam.txt`.

---

## What was wrong

mg-73df's MAJOR: **X3 — the correction mg-f8fa's own repair centres on — was still in force at
source**, in `t6_fock_and_record.py:149` and in the committed `out_t6_fock_and_record.txt:66`,
**inside a run ending `T6 TOTAL BAD: 0`**, together with the AM §17.5 quotation. Both are
named **verbatim in `check_doc.py`'s own `STRICKEN` table**.

> **A checker has two scopes — what it reads and what it looks for — and fixing one reads as
> fixing both.** `check_doc.py` had the full list over one file. `w3_scope.py` had a two-item
> list over a directory. Between them every file was covered and every statement was covered,
> and **no statement was covered in every file.**

## What this instrument does

| file | what |
|---|---|
| `stricken_a4ef.py` | **THE ONE LIST** — the union of `check_doc.py`'s ten `STRICKEN` rows and `w3_scope.py`'s two `FORBIDDEN` rows, plus **Y2**, which is new. Each row carries both forms: the exact document sentence and the source-code patterns. |
| `kerna4ef.py` | flattened scanning with an offset→line map, `print()`-scaffold masking, and the three-way exoneration rule. |
| `s1_extent.py` | runs the one list over the document **and all four code trees**, prints the **extent matrix**, and four controls. |
| `s2_seam.py` | the check nobody's brief asked for: a duplicate-passage sweep, cross-reference resolution, and the three staleness patterns this seam produced. |
| `selftesta4ef.py` | 133 assertions, half of them that the detector does **not** fire on things that look like the defect. |

**The extent is printed by the run**, because mg-73df's MAJOR is what a `TOTAL BAD: 0` means
when nobody says what it ranged over:

| checker | statements | targets |
|---|---|---|
| `check_doc.py` (mg-6f61) | 10 of 11 | **1 file** — the document |
| `w3_scope.py` (mg-f8fa) | **2 of 11** | 1 tree — `code/species_7d75` |
| `s1_extent.py` (mg-a4ef) | **11 of 11** | the document **+ 4 code trees** |

Both older checkers now **declare their own extent in their own output** as well, so a passing
run of either cannot be read as coverage of the other's.

## Controls, because a detector only ever seen to pass is worth nothing

* **(a)** the same detector at `ebecd89`, the state mg-73df audited — **4 asserted**, against
  **0** now, and it names X3 at `out_t6_fock_and_record.txt:66` and `t6:149`.
* **(b)** at `83ac472`, before mg-f8fa — **9 asserted**, and it catches X4 and X5 there, the
  two `w3_scope` covers, so the control tests the detector and not the coverage claim.
* **(c)** a statement injected into a scratch copy raises the count 0 → 1.
* **(d)** the exoneration rule is **not** disarmed by three phrases that have actually
  disarmed a checker in this arc, and **is** still cleared by a marker naming the repair.

Independently: **mg-73df's own `c4_scope.py`, re-run unmodified, goes from 4 still-asserted to
0**, and its `c5_doc.py` from 4 findings to 1. Those two runs are committed here as
`out_c4_scope_73df_after.txt` and `out_c5_doc_73df_after.txt`.

## Five defects this instrument found in itself, kept on the record

They are in `OUTCOMES.md` and in the source comments beside the code that carries them. The
two that matter:

1. **The instrument written to catch `t6_fock_and_record.py:149` missed
   `t6_fock_and_record.py:149`.** Flattening whitespace does not cross the `")` / `print("`
   between *"axiom with"* and *"0 failures"*.
2. **Two own-negation regexes exonerated their own sentences** — a bare `PROVED` matches
   inside *"not proved"*, a bare `located` inside *"not located"*. Which is why
   `selftesta4ef.py` tests every pattern against **both** the stricken form and the corrected
   form.

## Predictions

`PREDICTIONS.md` was written **before any edit and before any run** and has not been touched
since. `OUTCOMES.md` scores it: **22 predictions, 5 missed, misses kept as written.** The one
declared beyond-brief bet — that the stricken inequality direction was still live at source —
**lost**.

## Extent of this instrument, stated

`s1_extent.py` covers 11 statements over one document and four code trees. It says nothing
about the other documents in `docs/`, about `code/species_audit_a61f` or
`code/species_audit_73df`, or about any statement not on the list. `s2_seam.py` sweeps one
document and cannot see a duplicate spread across two, or one paraphrased below 45 %.

**And the list is still a list.** It is the union of two lists, and mg-73df's finding is that a
union of lists is still a list. The only structural improvement here is that a correction now
has **one** place to be recorded instead of two, so the next one cannot be enforced over half
the tree by accident.
