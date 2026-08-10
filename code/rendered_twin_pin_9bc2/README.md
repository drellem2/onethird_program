# mg-9bc2 — the rendered twin's pin, and the finding that it was never generated

`docs/state-of-the-wall.html` carried the words **`Generated 2026-07-19`** for three weeks.
This directory replaces that with something a reader or a control can check, and reports two
findings that are worth more than the staleness the ticket was filed about.

Run it:

```sh
sh code/rendered_twin_pin_9bc2/run_all.sh
```

## FINDING 1 — there is no generator, so `Generated` was false, not merely stale

The ticket said: *"Find the generator; if there is no generator and it was hand-built, SAY
SO — that is a more important finding than the staleness."* **There is no generator.**

- `git log --follow docs/state-of-the-wall.html` is **five commits**. The oldest, `29ffbf7`
  *"Initial: canonical State of the Wall"*, adds the twin and `STATE.md` **in the same
  commit**. The four after it are hand edits.
- mg-957a's commit message says so in as many words: *"the .html carried the identical false
  sentence verbatim, and fixing only the .md would have been this ticket's own failure mode
  in a second file."* That is a description of editing two files by hand.
- **Nothing in the repository writes the file.** The only three scripts that name it —
  `code/eps_spec_sweep_372e/s1_census.py`, `s2_classify.py`,
  `code/rate_sweep_910c/r2_classify.py` — all **read** it as a corpus member.

So the file **cannot be regenerated**, and this instrument does not pretend to. What it can
do is make the twin **name the `STATE.md` it is a rendering of** — mg-1abe's phrase, *a
publisher is not a pin* — and check that name per ledger row.

## FINDING 2 — the ticket's own premise about `STATE.md`'s size is stale

The ticket asks: *"STATE.md is now 4,658 words and readable, which was the entire problem the
HTML may have been solving. IF IT HAS NO REMAINING PURPOSE, DELETING IT IS A BETTER
OUTCOME."*

**`STATE.md` is not 4,658 words.** mg-ea0e's 32,772-byte executive summary landed at
`cc4c663` on **2026-08-06** and began growing back the same day:

| commit | date | bytes |
|---|---|---|
| `b80dea0` | 2026-07-30 | 186,710 |
| `cc4c663` | 2026-08-06 | **32,772** ← mg-ea0e |
| `f85a4e8` | 2026-08-06 | 34,573 |
| `d41d18c` | 2026-08-07 | 46,344 |
| `276aead` | 2026-08-07 | 66,038 |
| `641ef42` | 2026-08-10 | **110,640** |

**3.4× in four days, to 59% of the pre-restructure size, and 16,861 words against the
restructure's own `< 6,000` target.** The readability problem the twin exists to solve is
therefore *back*, which is the single most important input to the keep-or-delete question
and it points the opposite way from the ticket's framing. It is also a finding in its own
right, outside this ticket's scope: **the restructure had no ratchet**, so nothing held it.

## The recommendation: KEEP, pinned — do not delete

The ticket authorises deletion and this lineage has repeatedly found that removing a failure
mode beats adding a detector. **Here it does not, for three reasons:**

1. **The purpose the ticket assumed was gone is not gone.** See finding 2 — `STATE.md` is
   110,640 bytes and growing. Deleting the readable rendering on the stated ground that
   `STATE.md` is now readable would be acting on a premise that expired four days ago.
2. **Deleting is not the cheap side of the trade.** The twin's real cost is that every
   `STATE.md` ledger repair must be duplicated by hand, and that cost is now *measured and
   located* rather than discovered by audit: **2 of 12 rows**, named. That is a smaller
   standing cost than losing the only readable presentation of the program.
3. **The failure mode being removed is the unfalsifiable claim, not the file.** `Generated
   <date>` is gone, guarded against re-introduction, and replaced by a pin that fails.
   Deleting the file would remove the same failure mode, but so does this, at lower cost.

**What would change the recommendation:** if the reconciliation debt is not paid down — if a
later run reports more drifted rows than this one's two — the twin is being carried rather
than maintained, and deleting it becomes the better call. The control makes that a number
somebody can read instead of an impression.

## What was NOT done

- **The drifted rows were not repaired.** Rows **8** and **9** are reported, not fixed. Row 9
  is **mg-2f44**'s (`Depends: mg-9bc2`), and that ticket exists specifically to land it;
  fixing it here would silently close somebody else's item. Row 8 is a **second drifted row
  that no ticket names** — the twin's lede narrates it in prose, but nothing tracked it.
- **The twin was not regenerated**, because there is nothing to regenerate it with. Only its
  *provenance* claims were repaired (the header, the meta block, the footer).
- **No prose outside the ledger table is covered.** mg-957a's nine aggregating sentences live
  mostly there. See `COVERAGE.md` §2.
- **Nothing runs this automatically.** There is no CI, no git hook, and no gate in this
  repository — checked, not assumed (`.github` absent, `$(git rev-parse --git-common-dir)/hooks`
  has no non-sample entries). See `COVERAGE.md` §5; this is the highest-value follow-up.

## Files

| file | what it is |
|---|---|
| `lib9bc2.py` | ledger parsing (markdown + HTML), normalisation, digests, the pin format |
| `twin_pin.py` | the control (6 sections) and `--reconcile` |
| `seed_pin.py` | one-shot: seed the pin at `276aead`, the last commit that edited **both** files |
| `negative_control.py` | 11 mutations, each naming the section that must catch it |
| `COVERAGE.md` | what the control does not cover, including its own two shipped defects |
