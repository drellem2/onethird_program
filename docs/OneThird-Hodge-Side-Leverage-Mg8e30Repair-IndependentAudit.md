# Independent audit — the mg-8e30 repair (`e16e41c` + `61de121`)

**Work item mg-8a5c. Pre-filed in the same action as its parent mg-8e30.**
**Instrument: `code/hodge_leverage_audit_8a5c/`, `run_all.sh`, ~5 s, no code shared with
`verify_landing.py`. Committed transcript: `out_audit_8e30.txt`. Predicted exit code, written
before the first run: 1. Observed: 1.**

---

## Verdict

**THE PRIMARY TARGET IS CONFIRMED. The repair's own figures did NOT go stale.** Re-measured
from the post-commit tree by code that shares nothing with the instrument it audits, all five
published quantities reproduce exactly:

    STATE.md A5 cell                        12 692 codepoints  (12 914 bytes)
    relocated row history (whole file)      18 593 codepoints  (18 924 bytes)
    §14 frozen copy                         10 623 codepoints  (10 832 bytes)
    gap, cell only                          +2 069             (+2 082 bytes)
    gap, cell + relocated history          +20 662            (+21 006 bytes)

**Three mutually independent routes agree**: this instrument, the audited `verify_landing.py`,
and mg-f922's own `audit_repair.py` re-run at HEAD. mg-f922 findings **B and C are LANDED** at
all three sites, each stating which side of the edit it is on. The withdrawn *"flipped sign"*
claim stays withdrawn and the gap is positive. **0 mathematical statements are touched by this
audit and none is re-opened.**

**What is open is not the numbers — it is the gate that is supposed to keep them right, and one
stale self-referential locator of the same defect class.**

| | severity | finding |
|---|---|---|
| **F-1** | **MODERATE** | the new figure gate **passes when the figure a reader reads is wrong**, at all three sites. It is a substring-*presence* test, and the correction prints the live gap **twice** per site — once as the live figure, once as the tail of the chain `2 928 → 6 069 → −875 → +755 → +2 069`, which ends at the current gap **by construction**. Corrupting either copy alone leaves the gate green. Self-perpetuating: every future correction re-creates the pair |
| **F-2** | MINOR–MODERATE | and the repair's own four-mutation negative control **cannot see F-1**: its `M3` is `str.replace` with no count, so it deletes *every* copy and the gate necessarily fires. The realistic edit — one copy — is not in the battery |
| **F-3** | MINOR | `STATE.md:319` is `STATE.md:322` in the tree — off by 3, across 5 later commits to the file, one of which is mg-8e30 itself. Same defect class as the one the new rule names, one level up: a measurement of the file's own layout, correct when written and silently falsified afterwards |
| **F-4** | MINOR | `61de121` says **"13 lines"** in its subject and **"All thirteen changed lines"** in its body. The diff changes **11**, and `git show --stat` **in the same commit** says 11 insertions / 11 deletions. Every line is accounted for, so nothing rests on it — but a total contradicted by its own commit's `--stat` is the shape this arc keeps paying for |

**Nothing retreated.** Every declaration `e16e41c` makes under *"DECLARED, NOT HIDDEN"* is
checked here and holds, one of them more strongly than declared (below).

⚠️ **DISPOSITION, added 2026-07-30 by mg-a318 — annotated in place rather than answered
elsewhere, which is this arc's own convention for closing an audit.**

| | disposition |
|---|---|
| **F-1** | **LANDED, both halves, and the structural half first.** The chain's tail now **points at** the live figure instead of restating it, so each live figure is **written once per site** — mg-8a5c's own multiplicity table, re-run at the repair, reports **0 of 15 cells carrying a needle more than once** (was 3, all of them the live gap). And the gate no longer asks whether a value *occurs*: `verify_landing.py` **reads each figure out of the statement that asserts it** — by label from the `STATE.md` row and §14, by row label from H8's `AFTER mg-8e30` column — and compares it to what the run measured. Marked quotations are excluded before reading, so a quoted withdrawn figure cannot satisfy a check. **N7 is landed with it:** §14 and H8 are anchored on their **sections**, so relocating a disclosure out of its section fires the gate |
| **F-2** | **LANDED.** The battery is rebuilt to **nine** mutations, every one a **single-copy** change, run through `figure_gate` — **the same function the gate calls**, not a paraphrase, which is the other half of what let the old battery certify a gate slightly unlike the live one. N1–N3 are mg-8a5c's N1/N4/N5, the three single-copy corruptions the old gate observed at exit 0; N5 reinstates the duplicate itself, so the structural repair cannot be silently undone; N6 is the relocation |
| **F-3** | **NOT LANDED**, and named so it is not mistaken for done — the stale `STATE.md:319` locator and the *"this commit"* ambiguity are pm-onethird's to size |
| **F-4** | **NOT LANDED** (a commit message; nothing in the tree rests on it) |

⚠️ **AND ONE CONSEQUENCE OF THE STRUCTURAL FIX, DECLARED HERE BECAUSE IT LIVES IN THIS AUDIT'S
OWN INSTRUMENT.** `audit_repair_8e30.py`'s mutation **N2** — *"corrupt the CHAIN-TAIL copy only"* —
**has no target any more**, because there is no second copy to corrupt. Its `nth(..., 1)` now
finds nothing and the mutation is a no-op, which a naive re-run would report as a gate that
failed to fire. **The predicate is amended by mg-a318 to say so** (it reports `N/A — no second
copy exists` and counts it as the defect being structurally gone), and `out_audit_8e30.txt` is
**left as committed**: it is the record of what the audit found at `f58f7fd`, not a live gate, and
overwriting it would destroy the evidence the finding was made on.

---

## 1. The primary target: re-measured from the POST-commit state

The defect mg-8e30 repaired was a pre-edit number published as current. **The repair's own
figures are exposed to the identical mechanism** — writing a cell's length into that cell
changes it — so the only audit worth running is a re-measurement taken *after* the repair's own
commit. That is target T1, and it **CONFIRMS**.

The repair calls its four figures *"a fixed point solved as one"*, converged in two rounds.
**That claim is verified**: at `61de121` the number each document states is the number that
document has. The second commit `61de121` touches only `out_control.txt`, so it cannot move
them.

**Route independence is real, not asserted.** `verify_landing.py` locates the two rows by
scanning line prefixes and raising unless exactly one matches; this instrument uses
`re.findall` over the whole file and **prints the match count** (1 and 1) rather than asserting
it. Every length is reported in **both** Unicode codepoints and UTF-8 bytes.

**NOTE, not a finding — the unit is not named.** The three sites say *"12 692 characters"*.
That is codepoints; the byte reading is **12 914**, and the gap under it is **+2 082** rather
than **+2 069**. The arc's own `out_control.txt` names both (*"183253 bytes, 180093
characters"*); the three disclosure sites name neither. The convention is consistent and
nothing is wrong — it is simply a figure whose two readings differ by 222 published without the
word that picks one.

## 2. The committed instrument output agrees — and it agrees because the numbers are right

`code/hodge_leverage_landing_e1d0/run_all.sh` re-run at HEAD: **exit 0, 34 checks, 31 confirmed,
3 measurements, 0 refuted, and `out_verify.txt` regenerates BYTE-IDENTICALLY.** mg-f922's
findings **E and F are LANDED**: the runner redirects instead of piping into `tee` and exits
with the verifier's status; the transcript embeds no sha and prints the word `tree`.

**The discriminator is not that the two files agree.** Agreement between a document and an
output regenerated from it is guaranteed and proves nothing — that is the closed loop this
lineage keeps producing. The discriminator is whether the document's figure is right *now*,
independently measured. **It is** (§1). So the reconciliation was done by fixing the numbers.

### 2b. `61de121` is literally "regenerate the committed output" — so every line is taken alone

Two things present identically in that diff: **(1)** a document number corrected and the output
regenerated to follow — legitimate; **(2)** a number left wrong and the output regenerated to
stop disagreeing with it — the defect. **All 11 changed lines are resolved individually, and
all 11 are case (1).** Ten independently re-derivable figures, re-derived here from the
post-commit tree:

    STATE.md bytes 183253                 len(utf-8)                    183 253   ok
    STATE.md characters 180093            len(str)                      180 093   ok
    STATE.md 384 lines (header)           count('\n')                       384   ok
    STATE.md 385 lines (guard section)    len(split('\n'))                  385   ok
    62 table rows                         lines starting '|'                 62   ok
    largest stripped cell 11384           max over all '|' lines         11 384   ok
      — and over data rows only, i.e. the SAME under both cell rules      11 384   ok
    the largest cell is in the mg-a3d4 row                                        ok
    7876 < 11384                                                                  ok
    STATE.md at-rest sha 6129b1bc8b7bf774 sha256(STATE.md)[:16]                   ok
    NC1 gutted 385 -> 185 lines           385 − 200 deleted                 185   ok

**11 384 is the figure this commit actually changed** (`10 070 → 11 384`, the `BIGGEST_STRIPPED`
constant in `delta_control.py`), and it reproduces under **both** natural cell-enumeration
rules. The re-baseline is a document corrected and its evidence regenerated to follow.

**Named rather than counted as confirmed:** *"210 cells"* is **not** reproducible from the
description the transcript gives. Two natural rules give **258** (every `|` line) and **245**
(data rows only). The transcript calls 210 *"the population every whole-file tally below is
over"* but does not define the rule. **No conclusion here rests on it** — the figure the commit
changed reproduces under both. *"115 rendered blocks"* and NC1's *"42438 bytes"* come from the
control's own parser and its own mutation and are checked indirectly instead: `e16e41c` changes
exactly **2** content lines of `STATE.md` — the A5 cell and **one** new Appendix A paragraph —
so `114 → 115` being **+1** is consequential, as declared.

**NOTE, pre-existing and not introduced here:** one transcript reports the same file as **384
lines** in its header and **385 lines** in its guard section. Both are right — `count('\n')` and
`len(split('\n'))` — and neither says which.

## 3. The general guard was added, not just the three figures — CONFIRMED

`STATE.md` Appendix A carries **"A COMMIT THAT MEASURES SOMETHING IT ALSO MODIFIES MUST PUBLISH
THE POST-COMMIT MEASUREMENT, AND MUST SAY WHICH SIDE OF THE EDIT IT IS ON"**. It is a **general**
rule, not a note about three numbers: it states the mechanism (*"the observation was correct
when it was made and false when it was committed"*), gives **three numbered requirements**, and
supplies a **mechanical test** — *does the instrument resolve `HEAD` or open the working tree?*
It is mirrored verbatim into the mg-f922 audit document. **The brief's third item is satisfied.**

## 4. The SEAM check — two repairs, one artifact

`bbe83b5` and `e16e41c` both edited the `STATE.md` cell, §14 and H8. **Two sweeps, both
thresholds reported.**

**Sweep 1 — quoted units.** Population: markdown blockquote lines ≥ 120 chars plus `*"…"*` /
`*'…'*` marked quotations ≥ 60 chars, over the four documents both repairs touched. **98 units,
4 753 pairs**, similarity `difflib.SequenceMatcher.ratio()` on flattened text, **threshold
0.80**. Result: **8 exact duplicates, 0 of them figure-bearing** (they are rule names and the
struck `G″` statement, which are *supposed* to repeat verbatim); **1 near-duplicate at 0.984**,
differing only in the case of one letter, carrying no figure. **No seam defect.**

**Sweep 2 — figure-bearing sentences, no length floor, threshold lowered to 0.60.** Population:
**33 sentences, 528 pairs**. Result: **0 pairs at or above 0.60.**

**What would have counted, so the null result is checkable.** Sweep 1: any two quoted units
above the floors at ratio ≥ 0.80 carrying *different* figures — e.g. the same *"used to read …"*
quotation holding `−875` in one document and `+2 069` in another. Sweep 2: any two figure-bearing
sentences (mean length **449 chars**) sharing 60% of their characters; a stale copy differing
**only** in its figure — 5 to 7 characters — scores ≈ 0.97 and would be reported with FIGURES
DIFFER. Neither sweep fired.

**Related sweep, reported because a null result should say what it cannot see.** All **23**
occurrences of `−875` across the four documents were classified assertion-vs-history. **0 assert
it as a current figure**; 19 were auto-classified as historical and 4 were flagged by the
heuristic and cleared on manual reading — 4 false positives, **0 false negatives**. The stale
figures that survive do so as marked quotations of what was withdrawn, which is what the repair
declares.

**And a similarity sweep is structurally blind to two copies of a figure inside ONE line — which
is where the seam actually is.** See §5.

## 5. F-1 — the figure gate passes when the figure a reader reads is wrong

**The gate's shape is right and is a genuine improvement.** It formats what it has just measured
and requires the documents to carry *that*, instead of string-matching a frozen `−875` that went
on passing after the commit which made it false. Nothing below retracts that.

**But it is a substring-*presence* test, and the corrected wording puts the live gap into each
site twice.** Once as the live figure, and once as the tail of the chain
`2 928 → 6 069 → −875 → +755 → +2 069` — which **ends at the current gap by construction**.
Multiplicity, over the 5 needles the gate tests × the 3 texts it tests them in = **15 cells**:

| needle | STATE.md row | §14 (whole file) | H8 |
|---|---|---|---|
| gap `+2 069` | **2** | **2** | **2** |
| cell+hist `+20 662` | 1 | 1 | 1 |
| cell `12 692` | 1 | 0 | 1 |
| hist `18 593` | 1 | 0 | 1 |
| side-of-edit phrase | 1 | 1 | 1 |

**3 of 15 cells carry the same needle more than once, and all three are the live gap.** Seven
mutations run against the **real** runner — nothing re-implemented — with every verdict written
before the run, and restoration checked by sha256 rather than asserted:

    N1  STATE.md row: corrupt the LIVE gap figure only    predicted exit 1    observed exit 0
    N2  STATE.md row: corrupt the CHAIN-TAIL copy only    predicted exit 1    observed exit 0
    N3  STATE.md row: corrupt BOTH copies                 predicted exit 1    observed exit 1
    N4  §14: corrupt the LIVE gap figure only             predicted exit 1    observed exit 0
    N5  H8: corrupt the LIVE gap figure only              predicted exit 1    observed exit 0
    N6  H8: corrupt cell+history (1 copy per site)        predicted exit 1    observed exit 1
    N7  §14: move the whole disclosure OUT of §14         predicted exit 1    observed exit 0

**N3 and N6 fire, so the gate is alive — it simply cannot tell the copies apart.** And this is
**self-perpetuating**: the chain records the metric's history, so every future correction appends
the new gap and re-creates the pair. It is a seam defect of exactly the kind the brief names —
*the next edit builds on whichever copy it reaches* — living inside a single line, where a
similarity sweep cannot see it.

**F-2 — the repair's own negative control cannot detect this.** `verify_landing.py`'s `M3` is
`docs["H8"].replace(doc_num(a - b, signed=True), "")` — `str.replace` with **no count argument**,
so it removes *every* copy and the gate necessarily fires. The battery's four mutations are all
of that shape. A single-copy corruption, which is the realistic edit, is not in it.

**N7 is a second, independent hole in the same gate.** The instrument's own comment states the
right principle — *"Anchored on the ROW, not on STATE.md as a whole: a figure that satisfies the
gate from somewhere else in the file is not a figure a reader of A5 meets"* — and then applies it
to `STATE.md` **only**. §14 is anchored on the **whole deliverable file**, so the entire
disclosure paragraph can be relocated verbatim into a new appendix at the end of the document and
the gate still exits 0.

**The fix both point at is the same one:** anchor each needle to the sentence that asserts it,
and require **exactly one** match rather than at least one.

## 6. F-3 — my chosen unbriefed target: does *"this commit"* compose?

**Chosen because the repair's rule specifies a *convention* and no list asks whether the
convention survives contact with a second user.** The rule requires a document to say which side
of an edit its figure is on; mg-8e30's chosen phrase is *"this commit"* / *"this repair"*. That
is right for one anchor in one file.

`STATE.md` at HEAD carries **8 such anchors on 6 distinct lines** (population: all 385 lines),
written by **4 different commits** — `60f4dac`, `bdcb006`, `db08b4c`, `e16e41c` — with **nothing
in the prose distinguishing them**. A reader at L136 and a reader at L364 both meet *"this
commit"* and they denote different commits.

**The concrete cost is already paid.** `bdcb006` wrote *"the paragraph headed «Does a REPAIR need
a fresh audit? The narrowing test» — `STATE.md:319` **as this repair leaves the file**"*. At
`bdcb006` the heading **was** at line 319: measured post-commit and labelled with its side of the
edit, exactly as the new rule asks. **In the tree it is at line 322** — off by 3, across **5**
later commits to the file, one of them mg-8e30's own. The rule covers the moment of writing and
says nothing about the anchor rotting afterwards.

**The paragraph containing it already knows.** It says, of the very clause it is correcting,
*"Locate it by that heading and not by the number, which is the whole reason the struck clause
was wrong."* **The repair is to delete the number**, not to update it.

## 7. Declared-not-hidden: all three declarations checked

1. **`code/hodge_leverage_audit_f922/` is left untouched and still reports F-B and F-C.**
   **CONFIRMED, and the mechanism is confirmed by reading the instrument rather than the commit
   message**: F-B's site list is built by matching three literal strings. `STATE.md` **has**
   dropped off that list; §14 and H8 still match because the struck wording survives inside the
   correction's marked quotation. Exactly as declared. Re-run at HEAD it exits **1**, with F-E
   and F-F **gone** — and its table independently reproduces `12 692 / 18 593 / 10 623 / +2 069 /
   +20 662`, a third route to §1.
2. **The mg-f922 audit document is annotated in place with the disposition of every finding.**
   **CONFIRMED and counted against its population**: the findings table has **8** rows, ids A–H;
   **6** disposition rows cover **8** ids; **uncovered: none**.
3. **`code/state_restructure_34bf/verify_relocation.py` FAILs and it is pre-existing.**
   **CONFIRMED, and more strongly than declared**: it exits 1 with *"FAIL — 2 problem(s)"*, and
   the same run in a throwaway worktree at `f4eaea6` — before any edit of this cluster — produces
   **byte-identical** output.

## 8. Predictions, and the one that was wrong

Ten predictions were written before the first run and are kept as written in the work record.
**Nine held. One was wrong, and it is the one that found F-1.**

**M-A, predicted `exit 1`, observed `exit 0`:** I expected that corrupting the live gap figure in
the `STATE.md` row would fire the gate. It did not, because the row carries that figure twice.
**The wrong prediction is the finding** — had it been right, there would be nothing to report.
The five follow-up mutations that diagnosed it (N2–N5, N7 above) were all predicted correctly,
including N7, which was predicted from reading the gate's own anchoring comment.

**Near-miss recorded against this audit's own instrument.** The `−875` assertion-vs-history
classifier (§4) is a ±260-character keyword heuristic and produced **4 false positives out of
23**. They were cleared by reading each one. A reader should treat that sweep's *auto* verdicts
as a filter, not a result; the 0-assertions conclusion rests on the manual pass.

**And the seam sweep the brief asked for found nothing, while a different sweep on the same
question found F-1.** Sentence-similarity cannot see two copies of a figure inside one line. The
briefed sweep is reported in full above with its thresholds and its would-have-counted, because
a null result whose blind spot is unstated is worth less than the blind spot costs.

## 9. One note on the audited instrument's signalling rule

`code/hodge_leverage_audit_f922/run_all.sh` states its reproduction contract honestly and
conditions it on the files it reads — but it adds a triage rule: *"a finding that stops firing is
a repair, and a check that stops passing is a regression."* Re-run at HEAD, **5 checks stop
passing, and every one of them is a repair** — they are the checks that *confirmed* the defects
mg-8e30 fixed. The rule mis-triages in exactly the direction that would make a successful repair
look like a regression. Not a finding against mg-8e30; recorded so the next reader of that
transcript is not misled by it.

---

## What this audit did not do

Nothing here re-derives or re-opens mg-3c24's or mg-e1d0's mathematics — mg-3c24 found **0
BROKEN** and every number reproduced from a disjoint route, and **0 mathematical statements are
touched**. mg-f922's findings **A, D and H remain NOT landed** and are correctly named as open in
the tree; this audit does not land them and does not re-scope them. Ledger row A5 itself remains
open and is pm-onethird's to size.
