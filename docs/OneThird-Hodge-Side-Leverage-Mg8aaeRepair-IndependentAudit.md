# Independent audit — the mg-8eca repair (`d59ecd9` + `bee07a1`)

**Work item mg-9207. Pre-filed in the same action as its parent mg-8eca.**
**Instrument: `code/hodge_leverage_audit_9207/`, `run_all.sh`, ~7 min. Committed transcript:
`out_audit_9207.txt`. Predicted exit code, written before the first run: 1. Observed: 1.
32 checks, 2 refuted, 6 findings.**

---

## Verdict

**PARTIAL. Both of mg-8aae's items are genuinely closed, and neither closure runs through a hook,
a flag or a fixture.**

The question this audit exists to answer is not *does the repair contain more code* — mg-8aae's
defect was a check that fired **only through a purpose-built hook** while being `x == x` against
the artifact, so the only thing that counts is whether the new check fires on **the same path a
real defect would**. Every demonstration below writes the mutation **to disk**, into the real
document, scores it by running the real runner **as a subprocess**, sets **no environment
variable**, and never calls the gate function in memory.

> ⚠️ **mg-8eca's own negative control `N15`–`N18` calls `figure_gate` on in-memory copies of the
> site texts. That is a fixture, and it is not accepted here as evidence.** It is a good fixture
> and it is not worthless. But *"the gate function returns `False` when called with a mutated
> string"* and *"the runner goes red when the document is wrong"* are different sentences, and
> the whole of H-1 and H-2 is that difference. All four exchanges are re-taken on disk, plus
> eight more, plus §14 — a site mg-8eca's battery never touched.

**H-1 is closed.** Twelve exchanges, pairs chosen **by a procedure** rather than by hand, written
to disk at **3 of 3 sites**, make the real runner red at **12 of 12**. At **12 of 12** the
`FIGURE ORDER` row **for that site** is the **only gate row that failed**, and at **12 of 12**
that site's licensing row is still `[CONFIRMED]` — which is the *artifact's own* evidence that
each mutation was a permutation and nothing else. 3-cycles fire in **both cyclic senses**, 4 of
4. A transposition is its own inverse, so "both orderings" of one pair is one text; the
involution is checked (12 of 12 return byte-identical) and the question is then asked properly
with a 3-cycle, which is the smallest permutation that has two distinct orderings.

**H-2 is closed.** The headline edit, the count edit and a coherent false summary all make
`SUMMARY vs ROWS` fire **on disk with no environment variable**, and reinstating the two removed
lines turns all three green again — without that control, *the check fires* and *the instrument
fires* are the same sentence.

**Nothing confirmed is disturbed.** mg-8aae's own instrument, unmodified, re-run here rather than
quoted: **0 findings**, its **12 of 12 at row granularity** intact in 3 of its own rows, its G-1
prose probes at 3 of 3. mg-8916's own instrument, unmodified: **18 checks, 0 refuted, exit 0**.

Three things are open.

| | |
|---|---|
| **J-1** | **`SUMMARY vs ROWS` IS TWO INDEPENDENT DERIVATIONS WITH RESPECT TO THE PRINTED TEXT, AND ONE WITH RESPECT TO THE ROWS — AND THE ROW'S OWN WORDING CLAIMS THE WIDER ONE.** It prints *"READ BACK OUT OF THE LINES THIS RUN WILL PRINT"* and *"its 2 PRIMARY rows, counted again here"*, which reads as two derivations of one quantity meeting. On the `REFUTED` path they are one: the printed verdict is `{verdict}` and the printed count is `{len(bad)}` — the two expressions the other side recomputes — so the round trip is a regex through an f-string. **Measured, not argued: 0, 1 and 2 of 2 `PRIMARY` rows refuted, all three states produced on disk, all three green.** No achievable state of the rows makes it fire. **LOW–MODERATE** — the check is real and catches exactly the edit that made G-2; the printed extent is wider than the code |
| **J-2** | **HALF THE REPAIRED CONDITION IS STILL ISOLATED ONLY BY THE HOOK, AMONG THE DIRECTIONS mg-8eca DECLARES.** `agree = printed == derived and said == owed`. Deleted **one at a time**: removing `printed == derived` alone leaves mg-8eca's own on-disk D2 (headline) and D3 (count) **still red**, because `said == owed` fires on both. The only declared probe that isolates it is `MG8916_FORCE_SUMMARY`. A **coherent** false summary — headline *and* count moved together, which is what a hand-writer producing G-2 would actually write — does isolate it on disk with no env var, and is this audit's construction, not mg-8eca's. **LOW** — the clause is load-bearing; what is missing is the probe |
| **J-3** | **THE RUNNER'S OWN NEGATIVE CONTROL CRASHES ON EDITS AT ITS OWN PROBE SITES, AND THE CRASH IS INDISTINGUISHABLE FROM A FIRE.** `transpose` freezes three literals lifted out of the live documents — `CHAIN`, `H8_TABLE`, `H8_HIST_ROW` — and `assert`s each occurs exactly once. An edit at those lines, **including the very exchange the control exists to model**, raises `AssertionError`: **4 of 12** exchanges here, and E2 below, **where the gate refuted 0 rows and the run still exited 1**. A reader who reads the exit code concludes the gate caught a mislabelled table it never saw. **MODERATE** |

And this audit's own item, which nothing in the assignment names:

| | |
|---|---|
| **E2/E2b/E3** | **THE INVARIANCE MOVED; IT DID NOT GO AWAY.** An exchange has two halves — the **figures**, and the **statements they are attached to** — and mg-8eca closed the first. Exchange the two **labels** instead of the two figures and mg-8aae's own reader-visible defect comes back: H8's table says the `STATE.md` row **shrank** across mg-a2bd, every figure token sits in its declared slot, and the gate refutes **nothing**. **3 of 3** label-side exchanges are silent, two of them at exit 0. **MODERATE** |

**0 mathematical statements are touched here and no finding of mg-835f, mg-8a5c, mg-8916 or
mg-8aae is re-marked.**

---

## 1. H-1 — the census, on disk, at three sites, against the real runner

### 1.1 The probes are chosen by a procedure, not by hand

Within each site's own asserted figure sequence: every pair of **adjacent, distinct,
equal-length** tokens **neither of which is a value measured live this run**, taken greedily
disjoint from the front, first four per site. Live values are excluded because exchanging one
moves a *designated* statement as well, and a probe that fires two rows cannot show which row saw
it.

The reader that finds those tokens is this instrument's own. It shares **no regex** with the
gate: it scans character by character, and it **masks marked quotations in place** — blanking
them to spaces rather than deleting them — so every token keeps its offset in the real file and
the mutation can be written back at that offset. Checked before use, because a probe built on a
reader that disagrees with the roster is exchanging tokens the gate never looks at:

| site | my reader finds | the roster declares |
|---|---|---|
| the `STATE.md` row | 17 asserted figure tokens | 17 slots |
| §14 | 16 | 16 |
| H8 | 36 | 36 |

### 1.2 Twelve exchanges, on disk, 12 of 12

| | |
|---|---|
| the runner goes **red** | **12 of 12** |
| the `FIGURE ORDER` row **for that site** is the **only gate row** that failed | **12 of 12** |
| that site's **licensing** (multiset) row is still `[CONFIRMED]` | **12 of 12** |
| the exchange applied twice returns the site **byte-identical** | **12 of 12** |

The third row is the one that matters most, and it is deliberately scored by the **audited
artifact** rather than by the prober: the census's licensing half is a multiset question, so a
mutation that left it green *is* a permutation, asserted by the thing being audited.

**§14 fires like the other two.** mg-8eca's `N15`–`N18` are H8 and the `STATE.md` row; §14 was
never exchanged, on disk or in memory. It goes red at 4 of 4 here.

### 1.3 "Both orderings" — asked properly

A transposition **is its own inverse**, so a pair has exactly one exchanged text and *"both
orderings"* of one pair is not a question that can be asked. The involution is checked instead
(12 of 12), and the question is put to the smallest permutation that genuinely has two distinct
orderings: a **3-cycle**, run **forward and backward**.

| site | forward | backward |
|---|---|---|
| §14 (`13 551`, `16 692`, `+1 630`) | `FIGURE ORDER` refuted | `FIGURE ORDER` refuted |
| H8 (`13 551`, `16 692`, `+3 141`) | `FIGURE ORDER` refuted | `FIGURE ORDER` refuted |
| the `STATE.md` row | **no triple of distinct, equal-length, non-live tokens exists at this site** | reported as an **absence**, not passed over as a fourth pass |

---

## 2. Did the fix move the invariance? — this audit's own item

mg-8eca prints what it does not cover, which is the right instinct, and its list is honest as far
as it goes: two occurrences of the **same** token exchanged is *"the identity map on values"*.
That is true **by construction** and is checked here rather than repeated — `−875` occurs 4× in
the row history, and exchanging any two of them changes **0 characters**. There is no artifact.

**But an exchange has two halves.** mg-8aae's H-1 mutation moved the *figures* under fixed
*labels*. Move the *labels* under fixed *figures* and the reader meets the identical defect:

| probe | gate rows refuted | runner exit |
|---|---|---|
| **E2** H8's mg-a2bd table: `before mg-a2bd` ↔ `after  mg-a2bd`, figures untouched | **0** | 1 — **by `AssertionError`**, see J-3 |
| **E2b** the `bbe83b5` table: `STATE.md row cell` ↔ `this file (the relocated history)` | **0** | **0** |
| **E3** the three-column table's two historical **column headers** exchanged | **0** | **0** |
| **E4** two **row labels** exchanged *inside the designated table* | **2** — both `READ AT THE SITE` | 1 |

E2 produces, character for character, the reader-visible state mg-8aae raised H-1 on: *the table
says the `STATE.md` row went 16 692 → 13 551 across mg-a2bd*, i.e. that it shrank, and the chain
the whole finding was born in running backwards. Every figure token is in its declared slot. The
census is position-aware **over figures**, not over the **claims they are attached to**.

E4 marks the boundary precisely, and it is a real boundary rather than a hole everywhere: a label
*is* checked — exactly where a designated reader keys on it, and nowhere else.

**E5, the other half of the assignment's question — a figure moved to a different site at the
same value.** H8's declared `48 846` and §14's declared `44 055` exchanged **across** the two
sites, length-preserving, no live figure touched: the runner goes red with **both** sites'
`FIGURE CENSUS` **and** `FIGURE ORDER` rows refuted. A cross-site move changes both sequences and
both multisets, so this one the roster sees twice over.

**What the new census can and cannot distinguish, stated flatly:**

- it **can** distinguish two declared figures exchanged at a site — the whole of H-1;
- it **can** distinguish a figure moved between sites, and a new or dropped figure;
- it **cannot** distinguish two occurrences of the same token exchanged, **and says so**;
- it **cannot** distinguish a figure that stays in its slot while the **statement around it**
  changes — the labels, the column headers, the row order of a table the designated reader does
  not key on. **This is not printed, and it is the same defect one step to the left.**

---

## 3. J-3 — an exit code is not a verdict

`transpose` in the landing runner's negative control lifts three literal strings out of the live
documents and asserts each occurs exactly once in its site:

```
assert t[site].count(before) == 1, (site, before)
```

`CHAIN`, `H8_TABLE` and `H8_HIST_ROW` are those literals. They are the *very lines* the control's
own probes exchange — so any edit there, including an edit of exactly the kind the control
exists to model, raises `AssertionError` instead of reporting.

- **4 of 12** exchanges in §1.2 crashed the runner. They exit 1 and their `FIGURE ORDER` row *had*
  already printed, so the substance survived — but the exit code is no longer the gate's.
- **E2** is the dangerous case: **the gate refuted 0 rows** and the run still exited 1. Read the
  exit code and you conclude the gate caught a mislabelled table. It did not see it.

This is why every row in §2 is scored at **gate granularity**. The fix is the one the census
itself already uses: locate the probe text **by content** and fail with a message, not by a
frozen literal and an `assert`.

A second, milder effect, separated from the first because it is a true report rather than a
crash: **8 of 12** exchanges also turn the runner's negative-control **self-test** row red,
because the battery evaluates its own 18 mutations against the **mutated** site texts. That row
is a correct statement about a tree nobody should ship. It is not a gate row, and counting it as
one is what made this audit's first run report `4 of 12` where the answer is `12 of 12` — a miss
kept as written in `PREDICTIONS.md`.

---

## 4. H-2 — `SUMMARY vs ROWS` on the real artifact

### 4.1 The direction the assignment names: move a ROW, not the sentence

There are exactly **two** rows tagged `PRIMARY`. Their expectations are constants frozen in the
audited instrument's own source, and the source itself says a later commit that legitimately
moves them makes these rows refuted on a re-run — which is the state this tree is in. So the row
is moved **by editing the row**, on disk, in the real file, with no environment variable.

*(Not by editing `STATE.md`, the deliverable and the row history: the audited instrument's own
dirty-tree guard `SystemExit(2)`s over those three before the bottom line is ever reached.
`audit_repair_8e30.py` is not in that guard's scope, which is what makes this direction runnable
at all.)*

| state of the rows | the bottom line a reader gets | `SUMMARY vs ROWS` |
|---|---|---|
| **2 of 2** refuted (the tree as it stands) | `THE PRIMARY TARGET IS REFUTED IN THIS TREE: 2 of 2 rows tagged` | `[CONFIRMED]` |
| **1 of 2** refuted | `THE PRIMARY TARGET IS REFUTED IN THIS TREE: 1 of 2 rows tagged` | `[CONFIRMED]` |
| **0 of 2** refuted | `THE PRIMARY TARGET IS CONFIRMED: …(2 of 2 rows tagged PRIMARY are [CONFIRMED].)` | `[CONFIRMED]` |

**No achievable state of the rows makes the check fire.** The assignment's direction — *edit a
row in the real document so it disagrees with the summary* — **cannot be done**, and that is the
measurement, not a failure of the probe. On the `REFUTED` path the printed verdict is `{verdict}`
and the printed count is `{len(bad)}`; `derived` and `owed` recompute those two expressions. The
round trip through the regex is real work and it is not *nothing* — but it is not a second
derivation of the same quantity. **`x == x` with more steps is still `x == x`; this is `x == x`
with a printer and a parser in between, which is strictly more than the old check and strictly
less than the sentence beside it says.**

What the check **does** discriminate is an edit to `primary_summary`'s **own source text** —
which is real, is not a hook, and is exactly how G-2 was made. **So H-2 is closed.** The extent
is narrower than the printed wording, which is the same shape as both of mg-8aae's findings and
is finding **J-1**.

### 4.2 The direction mg-8eca demonstrates, re-taken here

All on disk, all with `MG8916_FORCE_SUMMARY` **unset** except the last:

| direction | `SUMMARY vs ROWS` |
|---|---|
| **D5** the `REFUTED` branch's headline edited to a literal `CONFIRMED` (mg-8aae's direction 2) | `[REFUTED  ]` |
| **D6** the **count** edited, the verdict word left correct | `[REFUTED  ]` |
| **D7** a **coherent** false summary — headline *and* count moved together | `[REFUTED  ]` |
| **D8** mg-8916's hook, kept: `MG8916_FORCE_SUMMARY=CONFIRMED` | `[REFUTED  ]` |

### 4.3 The deletion test, at the finest unit that has a return

`agree = printed == derived and said == owed` is **two clauses of one condition**. Deleting them
together tests neither, so each is deleted **on its own** and every direction is re-scored:

| deletion | D5 | D6 | D7 | D8 (hook) |
|---|---|---|---|---|
| `printed == derived` removed | RED | RED | **green** | **green** |
| `said == owed` removed | RED | **green** | RED | RED |
| **the defect reinstated** (`printed = FORCE_SUMMARY or derived`) | **green** | **green** | **green** | RED |

Read the first row. Of the directions **mg-8eca declares**, the only one that isolates
`printed == derived` is **D8 — the environment variable**. D5 and D6 leave it inert: with 2
`PRIMARY` rows and 2 refuted, editing the headline moves the count's *expectation* from `(2,2)` to
`(0,2)` as a side effect, so `said == owed` fires on both and the clause could be deleted without
moving a byte of either demonstration.

**It is not inert code** — D7 isolates it on disk with no environment variable, and D7 is this
audit's construction. What is missing is the probe, not the clause. That is finding **J-2**, and
it is mg-8aae's own finding one level down: a term demonstrated only through the hook.

The last row is the control that makes the other two readable. Without it, *the check fires* and
*the instrument fires* are the same sentence.

---

## 5. Nothing confirmed is disturbed

Scored by re-running the instruments that raised the findings, **unmodified**, rather than by
quoting them or mg-8eca:

- **mg-8aae's `audit_8916_repair.py`** — **0 findings**, 30 of its own rows, exit 1. Its single
  refuted row is **A4's own permutation row**, now false *because the gate fires*, with its
  predictions left as written reading `PREDICTION MISSED` at 2 of 2 sites. That is what a landed
  finding looks like from the raising instrument's side, and it is why exit 1 here is not a
  regression. **My prediction of exit 0 was wrong and is kept as written.**
- **the 12 of 12 at row granularity survives the widening** — 3 of mg-8aae's own A2 rows report
  it: the runner goes red, the row that failed is the `READ AT THE SITE` row **for that figure**,
  and 12 of 12 restorations return exit 0.
- **G-1 stays closed against the auditor's own wording** — mg-8aae's own prose probes, in slots it
  chose by procedure and controlled green before use, at 3 of 3.
- **mg-8916's `repair_835f.py`** — **18 checks, 0 refuted, exit 0**. mg-8eca's claim of "18
  checks" holds, and the population is named: **18 is 16 confirmed + 2 measured + 0 refuted**, not
  18 confirmations.

Restoration is **checked by sha256**, not asserted: 4 mutated files byte-identical, 5 committed
transcripts byte-identical — including `out_verify.txt`, which is why this instrument runs
`verify_landing.py` directly and never the landing `run_all.sh`. `git status` over the mutated
files is empty.

---

## 6. What is left, sized

| | | |
|---|---|---|
| **E2/E2b/E3** | the census is position-aware over **figures**, not over the **claims** they are attached to; the label-side exchange reproduces mg-8aae's own defect and is silent at 3 of 3 | **MODERATE.** The narrow fix is to print it as uncovered, beside the same-token exclusion. The real fix is that a table row's **label and its figures are one unit**, and the roster declares only half of it |
| **J-3** | the negative control's frozen literals turn an edit at its own probe sites into a crash the exit code cannot be told from a fire | **MODERATE.** Locate by content, fail with a message |
| **J-1** | `SUMMARY vs ROWS` discriminates edits to its own source text, not disagreement between summary and rows; the printed wording claims the wider property | **LOW–MODERATE.** Narrow the wording, or make the count side genuinely independent |
| **J-2** | of the directions mg-8eca declares, only the hook isolates `printed == derived` | **LOW.** Add D7 — a coherent false summary — to the battery |

**Not re-opened, and not weakened:** mg-835f's 12 of 12, G-1, G-2, mg-8916's 18 checks, and both
of mg-8aae's items, which are closed.
