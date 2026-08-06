# mg-ea0e — the three-move `STATE.md` relocation, and its check

Daniel, 2026-08-06: *"onethird_program STATE.md needs a big overhaul because it is not
readable … links to supplementary reference material can be provided, it should be an
executive summary."* pm-onethird turned that into a **relocation spec with exactly three
moves** and dispatched it with **no editorial latitude**. This directory is the mechanical
execution of that spec and the instrument that checks it.

**This polecat judged nothing about what is load-bearing.** Those calls are pm-onethird's
and it made them. What is here is cut and paste, plus arithmetic.

## The measured cost this repairs

Hours before the ticket was filed Daniel asked *"is there a Cheeger constant / spectral gap
from which the 1/3–2/3 conjecture would follow? NOT SURE WHAT WE'VE PROVEN SO FAR."* The
answer is the first section of `STATE.md`. He could not retrieve it; pm-onethird could not
either, and answered about the wrong operator with the file open. **The document failed both
its most expert readers on the same question the same night.**

## What moved

| move | what | from | to |
|---|---|---|---|
| 1 | Appendix A, *Audit-stage process* — 52% of the file, more words than all its mathematics | `STATE.md:180–381` | [`docs/audit-stage-process.md`](../../docs/audit-stage-process.md) |
| 2 | *Where the threads converge* — a chronological log, one dense paragraph per attempt | `STATE.md:142–177` | [`docs/state-history/threads-chronology.md`](../../docs/state-history/threads-chronology.md) |
| 3 | the seven attempt-index cells over the spec's own 2,000-character threshold — `:130`–`:136`, the largest 13,367 characters | `STATE.md:130–136` | appended to the **existing** `docs/state-history/attempt-<id>.md` files mg-34bf built |

Every one of those blocks is in its destination **whole and unedited, character for
character**. Each site it left carries a link back.

## What stayed, and it is byte-identical

`STATE.md` lines **1–129 are identical to the base commit `78ae4d9`** — checked, not
asserted: the one-paragraph state, the two axes, the glossary, the proof chain, **the full
ledger with all its rows verbatim**, the single lemma L1b, and the first attempt rows. So is
§ *Why 1/3 — the elementary anchor (proven)* at the end. **No mathematical claim is reworded
anywhere in this change**, in `STATE.md` or in any destination file.

## Acceptance, measured

Run `bash code/state_restructure_ea0e/run_all.sh`; the transcript is committed as
`out_verify_relocation_ea0e.txt`. The checker reads `STATE.md` at the base commit out of git
and the corpus off disk, and re-derives everything; it does not read the builder's spec and
does not trust any list of what moved.

| | result |
|---|---|
| **A1 byte accounting** | old `STATE.md` **186,710**; new `STATE.md` **32,772**, of which **2,796** is composed link boilerplate and **29,976** is old text still in place; old text found **verbatim** in linked files **157,996**. `29,976 + 157,996 = 187,972 ≥ 186,710`, **surplus +1,262** — the surplus is text deliberately carried in *both* places (each row's retained sentence also sits in its history file). Corpus total `245,161 → 261,318`. |
| **A2 shape** | **4,658 words** (target < 6,000) and **longest line 1,772 chars** at `:124` (target < 2,000). Was 29,094 words with a 13,367-character line. The longest line left is a row this change did not touch. |
| **A3 mg-ids** | **68** distinct mg-ids in the old file, **0 unreachable**. 34 still in `STATE.md`; 34 now reachable one link away. |
| **A4 population** | enumerated per file, printed in the transcript — not taken from the three moves. |
| **A5 markers** | every `STRUCK` / `RETRACTED` / `RETIRED` / `CORRECTED` / `SUPERSEDED` / `REFUTED` / `DISCHARGED` / `BROKEN` / `withdrawn` / `void` occurrence survives in the reachable corpus; **0 lost**. |
| **C0 coverage** | every line of the old file — and every **column** of every rewritten ledger row — is present character for character in `STATE.md` or in a file it links to. **0 missing.** |

## The two places this departs from the spec, and why

Both are reported rather than decided quietly; both are one-line reversions.

1. **Appendix A is moved as `:180–381`, not `:180–382`.** Line `:382` is the header
   `### Why 1/3 — the elementary anchor (proven)` and its body is `:383–386`. Taking the
   range literally would separate a header from its body and orphan four lines of **proven
   mathematics** under a heading that had moved. `### Why 1/3` is named by none of the three
   moves, so it stays in `STATE.md`, untouched. Revert by setting `APPENDIX_LAST = 382`.
   *(Note that lines `:378–380`, a mixing/balance reference paragraph and the forbidden-band
   paragraph, are inside the spec's range and were moved with it. They are reference
   material rather than audit process; the spec's range is the spec's call and this polecat
   did not narrow it.)*
2. **Row `:133` keeps two sentences, not one.** Its opening sentence states a condition —
   *"cannot consume branch (ii) for any modulus `F(ε) = Ω(ε)`"* — that the cell's very next
   sentence records as **DISCHARGED** by mg-3af9. Keeping only the first would leave a
   superseded claim standing unmarked in the index, which is the defect this whole
   convention exists to prevent (`docs/state-history/README.md`: *a row must not be able to
   contain a claim and its own retraction*). Every other row keeps exactly its opening
   sentence, verbatim.

## What this did NOT do

- **No mathematics was rewritten, re-scoped or summarised.** The only prose composed
  anywhere is the link boilerplate, the file headers, and the one short current-position
  paragraph the spec asks for at the *Where the threads converge* site — and that paragraph
  is built from the chronology's own quoted clauses.
- **Rows `:114` and `:124` were left alone.** They are under the spec's own 2,000-character
  acceptance threshold, so they are not "the oversize cells".
- **No `attempt-<id>.md` file was created.** All seven destinations already existed; the
  spec says APPEND to the existing files and not to invent a scheme.
- **`docs/state-of-the-wall.html`** (`STATE.md:5`, *"Generated 2026-07-19"*) was **not**
  regenerated. It was already stale against `STATE.md` before this change and regenerating
  it is not one of the three moves. Flagged, not fixed.
- **Stale line references outside `STATE.md` were not rewritten.** `STATE.md` is 176 lines,
  not 387; references into Appendix A now resolve into `docs/audit-stage-process.md`. A note
  in `docs/state-history/README.md` records this. The references inside the relocated cells
  are historical statements and were moved verbatim with them.
- **No judgement about whether a spec call is right.** Where executing one would have
  required that, it is in *the two departures* above instead.

## Files

- `build.py` — the relocation. Idempotent only against the pre-relocation tree; **do not
  re-run it on an already-relocated `STATE.md`**, it would append a second copy of each cell.
- `verify_relocation_ea0e.py` — the check. Independent of the builder; safe to re-run.
- `run_all.sh` — runs the check and writes the transcript.
- `out_verify_relocation_ea0e.txt` — the committed transcript.
