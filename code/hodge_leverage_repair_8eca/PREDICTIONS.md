# mg-8eca — predictions, written BEFORE the first run

Repair of the two items mg-8aae left open on the mg-8916 repair (H-1, H-2).
Every exit code and every probe verdict below is written before the instrument is run.
Misses are kept as written.

| # | probe | predicted |
|---|---|---|
| P0 | `verify_landing.py` on the clean, repaired tree | exit 0 |
| P1 | **the four EXCHANGES on disk** — two declared figures of equal length swapped in ordinary prose, at 2 sites × 2 disjoint pairs | **GATE FIRES 4 of 4** — this is the mutation mg-8aae observed at exit 0 |
| P1b | ...and the row that failed is the **`FIGURE ORDER` row FOR THAT SITE**, and the ONLY row that failed | 4 of 4 |
| P1c | the four restorations, sha256-verified | exit 0, 4 of 4 |
| P1d | each mutation is a permutation and nothing else (same multiset, same designated reads, same length) | asserted before writing, 4 of 4 |
| P2 (D0) | `SUMMARY vs ROWS` on the artifact as it stands | `[CONFIRMED]`, refuted 3 |
| P3 (D1) | `MG8916_FORCE_SUMMARY=CONFIRMED` — mg-8916's hook, kept | `[REFUTED]`, refuted 3 → 4 |
| P4 (D2) | **the REFUTED branch's headline edited by hand ON DISK, no env var** — mg-8aae's own direction-2 mutation | **`[REFUTED]`, refuted 3 → 4** — where the old check stayed `[CONFIRMED]` with the count unmoved |
| P5 (D3) | the **count** edited and the verdict word left correct | `[REFUTED]`, refuted 3 → 4 — the second read carries weight on its own |
| P6 (D4) | **the defect reinstated** (`printed = FORCE_SUMMARY or derived`) with D2's edit still applied | **`[CONFIRMED]`, refuted back to 3** — the deletion test |
| P7 | mg-8aae's own `audit_8916_repair.py`, unmodified, on this tree | its two A4 permutation rows read `GATE FIRES`; **0 findings** |
| P8 | its committed transcript `out_audit_8916.txt` | sha256-identical afterwards |
| P9 | mg-8916's own `repair_835f.py`, unmodified, on this tree | 18 checks, 0 refuted, exit 0 — nothing it demonstrated is dropped |
| P10 | the negative control battery inside the runner | grows 14 → 18, **18 of 18** move the gate as predicted |
| PX | this instrument's own exit code | **0** |

## Misses, kept as written

The first run refuted two rows. **Both were defects in THIS INSTRUMENT and in this repair's own
edits, not in the repair's substance** — and one of them is the more interesting kind: a repair
that broke the instrument that raised the finding. They are recorded rather than tidied away.

| # | predicted | first run | whose defect | disposition |
|---|---|---|---|---|
| P7 | mg-8aae's A4 rows read `GATE FIRES` | **MISSED** — its instrument **crashed** in A1 before reaching A4 | **mine** | my edit to the runner's printed-extent line (adding `in N declared slots`) broke mg-8aae's A1, which **re-counts the printed extent by parsing that line**. An instrument that raised a finding must be able to re-run **unmodified** against the repair that answers it. Corrected: the extent line keeps its exact shape and the slot count goes on a line of its own, with a comment at the site saying why |
| — | the mechanism row (`printed = FORCE_SUMMARY or derived` is gone) | **MISSED** — it read the string in the repaired file | **mine** | the repaired file **quotes the removed line** in its docstring and in the ⚠️ block recording the removal. A check that cannot tell the defect from the note recording its removal goes red on an honest repair. Corrected: the match is anchored to the code line, indentation and all |
| P1/P1b/P1c/P1d | 4 of 4 red, 4 of 4 at the `FIGURE ORDER` row, 4 of 4 restored, 4 of 4 permutations | **HIT, 4/4/4/4** | — | H-1's mutation now moves the gate |
| P2–P6 | D0 green, D1/D2/D3 red +1, D4 green | **HIT, 5 of 5** | — | including D4, which is what makes D2 attributable |
| P9 | mg-8916's instrument: 18 checks, 0 refuted, exit 0 | **HIT** | — | measured after the repair, not quoted from its transcript |
| P10 | 18 of 18 | **HIT** | — | N1–N14 unchanged, N15–N18 added |
| PX | exit 0 | **HIT** on the corrected instrument | — | it exited 1 on the first run, on the two rows above |

### A note on the second miss, because it is the shape this repair is about

Both misses are the same error in miniature: **a check whose measured property does not line up
with the failure it is supposed to see.** The extent-line regex measured a *string*, when what it
needed was the *count*; the mechanism check measured *presence anywhere in the file*, when what it
needed was *presence as code*. Neither is a coverage problem and neither would have been fixed by
checking more things — which is exactly mg-8aae's closing note, arriving on this instrument's own
first run.
