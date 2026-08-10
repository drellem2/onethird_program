# mg-9bc2 — what `twin_pin.py` covers, and what it deliberately does not

Read this before citing the control. Its verdict is narrower than *"the twin is correct"*,
and the gap is where the next instance of this defect will live.

## What it covers

| # | Section | What a `PASS` means |
|---|---|---|
| 1 | pin present | The twin names a `STATE.md` revision, and the row label sets in `STATE.md`, the twin, and the pin are the same set. |
| 2 | per-row digests | No `STATE.md` **ledger row** has changed since the twin was last reconciled. This is the load-bearing check. |
| 3 | whole-file digest | `STATE.md` is byte-identical to the pinned revision. Informational only — see below. |
| 4 | kind marks | Every ledger row carries the same `Kind` mark in both documents. Live; does not consult the pin. |
| 5 | default-deny guard | The twin does not call itself `Generated <date>`, and does not claim canonicity on a line that fails to name `STATE.md`. |
| 6 | visible ↔ machine pin | The header's human-readable provenance line quotes the same commit as the machine-readable pin. |

Section 3 **differs on nearly every run and that is not a defect.** `STATE.md` changes
constantly outside the ledger; if section 3 carried the verdict, the control would be red
permanently and would be ignored inside a week — which is precisely how `Generated
2026-07-19` survived three weeks. Section 2 carries the verdict.

## What it does NOT cover

**1. Whether an unmoved row is faithfully summarised. This is the big one.** The twin is a
*summary* rendering. Its cells are deliberately shorter than `STATE.md`'s — row 3b is **3,391**
characters in `STATE.md` against **829** in the twin, row 9 is **898** against **95** — so no
byte relation between the two exists or should. The control answers
*"which rows have moved underneath the summary?"*. It
cannot answer *"is the summary of this unmoved row true?"*. **A row that has never moved, and
was summarised wrongly on the day it was written, passes every section here.** Nothing short
of a reader comparing the cells will catch that, and this instrument does not pretend
otherwise.

**2. Anything outside the ledger table.** The twin has seven sections; only the `Full ledger`
table is digested. Its proof-chain prose, obstruction cards, and attempt index are
uncovered — and mg-957a's repair was of *nine aggregating sentences*, most of which live in
that uncovered prose. **The historically most common form of this defect is out of scope.**
Extending section 2 to named prose blocks is the obvious next move and was not done here.

**3. The `<i>`/`<s>` bypass in section 5, which is declared rather than closed.** A banned
string inside `<i>…</i>` or `<s>…</s>` is treated as a quotation of superseded text and
skipped. This exists because the repaired lede has to *say* what the false claim was, and
the first version of the guard failed that very repair. Wrapping a live claim in `<i>` hides
it from section 5. The cost to anyone doing that is that the claim renders in visible
italics as a quotation, which a reader can see; the same discipline `STATE.md` already uses
with `~~…~~`. It is a hole, it is on purpose, and it is written down here rather than
discovered later.

**4. Whether `--reconcile` told the truth.** `--reconcile` records that the twin's cells for
the named rows *were actually updated*. Nothing verifies that. It refuses to re-pin a row
that has not moved, and it refuses a blanket re-pin that does not name its rows — both of
which make a false reconciliation deliberate rather than accidental — but a caller who edits
nothing and re-pins anyway gets a green control over a stale page. **This is the single
easiest way to defeat the whole mechanism.** The defence is that the re-pin is a visible diff
in the commit that contains no corresponding change to the twin's ledger cells, which a
reviewer can see; that is a social defence, not a mechanical one.

**5. That the control is run at all.** Nothing in this repository invokes
`code/rendered_twin_pin_9bc2/run_all.sh` on commit, on merge, or on any schedule. There is no
hook, no CI, and no gate — this was checked, not assumed. **An instrument nobody runs is the
same artifact as a date nobody re-reads**, which is the defect this ticket was filed about,
one layer up. Wiring it into whatever gate the repository grows is not done and is the
highest-value follow-up here.

## The instrument's own defects, all three caught by running it

Filed because a repair is an artifact of the same kind as the defect it repairs, so it is
subject to that defect, and all three of these are that. **Every one was found by running
the thing, not by reading it** — which is the argument for the instrument existing at all.

- **`run_all.sh` laundered a `DRIFT` verdict into `CLEAN`.** The first version piped both
  commands through `tee`, so `$?` was *tee's* status and never the instrument's. It printed
  `control exit : 0 … CLEAN — the twin's pinned ledger rows all still match STATE.md` over a
  control that had exited 1 naming two drifted rows. **A runner that cannot report its own
  instrument's failure is the same artifact as a date nobody re-reads**, one layer in. Now
  redirect-then-`cat`; POSIX `sh` has no `PIPESTATUS`.

- **Section 5 was blind to the exact string it was written for.** The first version matched
  the raw line against `/\bGenerated\b\s+20\d\d-\d\d-\d\d/`, and the twin's own markup is
  `<span><b>Generated</b> 2026-07-19</span>` — the tags sit between the word and the date, so
  the guard never fired on the one claim this whole ticket is about. The scan now runs over
  tag-stripped text. **A guard against a false claim, blind to that claim, in the file the
  ticket names.** Only a live run found it.
- **The pin's own `state-sha256` field never parsed.** The field-name pattern was
  `[a-z-]+`, and `state-sha256` contains digits, so section 3 compared the actual digest
  against the empty string and printed `DIFFERS` — the right answer for the wrong reason,
  which would have kept printing the right answer after `STATE.md` stopped moving.

## Two more of the instrument's own defects, found at the first reconciliation (mg-2f44)

The three above were found by *running* the instrument. These two were found by **using it
for its purpose** — reconciling a row and re-pinning it — which is a different event and had
never happened before. Both are the same defect in two places: **a fixture that hardcoded
the one thing the instrument exists to let change.**

- **`negative_control.py`'s section-6 mutation had a one-use lifetime.** It read
  `text.replace("@ 276aead1a8c5 (2026-08-07)", …)`. The moment `--reconcile` moved the pin to
  a new commit, the search string matched nothing, the mutation became a no-op, and the
  harness scored it `SETUP FAILED` — **which is the harness working**, and is why this one was
  visible. It now reads the commit out of the file with a regex, so it survives every re-pin.

- **The positive control could not fail, and did not fail when it should have.** This is the
  serious one, and nothing reported it. The baseline assertion was

      ok = (code == 1 and "rows 8 and 9" not in out and "8 9" in out
            and "STRUCTURAL" not in out)

  where `"8 9" in out` was meant to say *the drift worklist is exactly rows 8 and 9*. It is a
  substring test against the **whole report**, and section 1 prints
  `PASS  all three row sets agree: 1 2 3a 3b 4 5 6 7 8 9 10 11` on every healthy run — so
  `"8 9"` matched **there**, unconditionally, forever, whatever had actually drifted. When
  mg-2f44 reconciled row 9 and the true worklist became `8`, the baseline still scored
  `CAUGHT`. **The positive control is what licenses reading every other row of the table**, so
  a baseline that cannot fail is worth more than any single mutation it guards — and it is
  `run_all.sh` laundering a `DRIFT` into `CLEAN` a third time, in the file written to catch
  that class. It now parses section 2's worklist **line** and compares the row list
  **exactly**, against an expectation **derived from the pin** rather than typed in — so it
  neither rots at the next reconciliation nor passes on a coincidence. Demonstrated to
  discriminate: the correct set scores `CAUGHT`; `['8','9']` (the stale literal), `[]`, and
  `['3b']` all score `HOLE`.

**The rule these two produce, stated so it is a rule and not a lesson:** nothing in
`negative_control.py` may name a pinned commit or a drifted row as a literal. The drift set
and the pin commit are precisely what every reconciliation moves; a fixture that spells them
out is a check with an expiry date, and the second one above shows it can expire **silently**.

**Still uncovered, and mg-2f44 did not change it:** everything under *What this does not
cover* above stands unedited. In particular **(2)** — only the ledger table is digested — is
why row 9's repair could be checked but the three **prose** paragraphs mg-2f44 also synced
(the summary, the machinery set, the fork) could **not** be. Those were reconciled against
`STATE.md:13`/`:76`/`:81` by hand and by reading, and **no control saw them**. And **(4)**
stands at full strength here: this reconciliation's claim that row 9's cell was actually
updated rests on the diff being visible in the same commit, which is a social defence.
