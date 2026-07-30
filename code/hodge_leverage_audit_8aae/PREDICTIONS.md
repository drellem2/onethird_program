# mg-8aae — predictions, written BEFORE the first run

Independent audit of the mg-8916 repair of mg-835f (`b055ae5`, `f5360bf`, `d1dd84d`).
Every exit code and every probe verdict below is written before the instrument is run.
Misses are kept as written.

| # | probe | predicted |
|---|---|---|
| P0 | `verify_landing.py` on the clean tree | exit 0 |
| P1 | the 12 designated reader-facing figures, corrupted ON DISK one at a time | runner red 12 of 12 |
| P1b | ...and the `READ AT THE SITE` row FOR THAT FIGURE is itself [FAIL] | 12 of 12 — not weakened |
| P2 | the 12 restorations, sha256-verified | exit 0, 12 of 12 |
| P3 | my own wrong-prose probe (my wording, my anchor, my ballast), 3 sites x 2 shapes | GATE FIRES 6 of 6 |
| P3b | the 6 restorations | silent 6 of 6 |
| P4 | **PERMUTATION**: two roster figures of equal length swapped in ordinary prose at a site — multiset unchanged | **gate SILENT, exit 0** — a wrong figure a reader meets that the census cannot see |
| P5 | `MG8916_FORCE_SUMMARY=CONFIRMED` on the mg-8a5c instrument | `SUMMARY vs ROWS` [REFUTED], refuted 3 -> 4, exit 1 |
| P6 | the summary SENTENCE TEXT mutated in source to assert CONFIRMED while the PRIMARY rows stay refuted | **`SUMMARY vs ROWS` stays [CONFIRMED]** — the check compares a variable with itself, not the printed sentence |
| P7 | mg-835f's own `audit_a318_repair.py`, unmodified, on this tree | 0 findings, exit 0, its 3 U1 rows GATE FIRES |
| P8 | the repair document's own header (18 checks, 0 refuted, exit 0) vs `out_repair_8916.txt` | agrees |
| P9 | the document's printed extent (17 / 16 / 36 licensed tokens; 6 / 9 / 16 historical) vs the live code | agrees |
| P10 | seam sweep of the repair's touched passages, threshold 0.80 / minlen 60 | 0 findings |
| PX | this instrument's own exit code | **1** — because P4 and P6 are predicted to be defects, and this instrument exits 1 on any finding |

## Misses, kept as written

The first run refuted 9 rows. **Three of the nine were defects in THIS INSTRUMENT, not in the
repair**, and they are recorded here rather than tidied away — an audit whose own misses are
edited out of its predictions file is an audit reporting on itself.

| # | predicted | first run | whose defect | disposition |
|---|---|---|---|---|
| P9 | the printed extent agrees | **MISSED** — H8: runner 36, this instrument 27 | **mine** | my tokenizer's `[+−]?\d[\d ]*` ran through H8's multi-space table columns and swallowed three figures into one unparseable run. Corrected to consume a space only when a digit follows. The runner was right |
| P3 | 6 of 6 prose probes fire | **PARTIAL** — 4 of 6; 2 never ran | **mine** | my ballast picker cut candidates at sentence boundaries and rejected any containing a newline; these documents are hard-wrapped, so §14 offered no candidate. Corrected to whole lines |
| P10 | 0 seam findings | **MISSED** — 14 reported | **mine** | my sweep counted a line the commit REWROTE IN PLACE as a deleted passage still living, and looked for the correction marker on the line itself rather than in a context window. 14 of 14 were artefacts. Corrected: in-place rewrites dropped, marker window ±12 lines (mg-d330's convention) |
| P4 | permutation invisible, gate SILENT | **HIT** — 2 of 2 at exit 0 | the target's | booked as finding H-1 |
| P6 | `SUMMARY vs ROWS` stays green on a sentence-level disagreement | **HIT** | the target's | booked as finding H-2 |
| P1/P1b/P2 | 12 of 12 red, 12 of 12 at row granularity, 12 of 12 restored | **HIT, 12/12/12** | — | mg-835f's primary target is intact |
| P5 | forced summary fires, refuted 3 -> 4 | **HIT** | — | |
| P7 | mg-835f's own instrument: 0 findings, exit 0 | **HIT** | — | |
| P8 | the document's header agrees with its transcript | **HIT** | — | |
| PX | this instrument exits 1 | **HIT** | — | two findings stand |

### Second round of my own defects, also kept

The corrected instrument's second run refuted two more rows, and **both were again mine**:

| predicted | second run | whose defect | disposition |
|---|---|---|---|
| P9 | **MISSED AGAIN** — H8: runner 36, this instrument 27 | **mine** | my first correction was not enough. Flattened, H8's three-column table reads `9 748 11 378 13 367` — that is THREE figures in one run of space-separated groups, and a parser that takes the whole run and then asks whether it is well formed drops all three. Groups are now consumed greedily left to right. **The two tokenizers now agree exactly at 3 of 3 sites, 17 / 16 / 36 = 69** |
| P3 | **PARTIAL AGAIN** — 2 of 6; the two sites swapped | **mine** | my line-based rewrite excluded lines starting with `\|`, and the `STATE.md` row IS a markdown table cell, so every one of its lines starts with `\|`. Candidates are now digit-free stretches WITHIN lines as well as whole lines, rejected on content rather than on how the line begins |

**Five refuted rows across two runs, five of five mine.** Every row that was about the target —
P1, P1b, P2, P4, P5, P6, P7, P8 — was predicted correctly on the first run and has not moved.
