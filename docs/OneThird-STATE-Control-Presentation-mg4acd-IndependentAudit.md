# Independent audit of mg-4acd / `e4426c9` — the presentation record

**mg-218d**, 2026-07-30. Pre-filed at the same time as the ticket it audits. **Fifth control
in this lineage**: the first (`b68db5d`'s headline re-run) was blind at the INPUT because it
pinned fixed revisions; the second (`bf17716`) at the MUTATION SET because it tested
substrings its own author chose; the third (`e924590`) closed both with a content digest and
was blind at the LOCATOR; the fourth (`e4426c9`) closed the locator with a presentation
record. This audit assumes the blind spot **MOVED** rather than closed, and its primary
question is which layer is uncontrolled now.

Reproduce: `sh code/state_layer_audit_218d/run_all.sh` (~2 min). Five outputs committed
beside it. Sections 1, 2 and 4 mutate `STATE.md`, `docs/state-history/README.md`,
`docs/state-history/attempt-mg-276d.md` and (in two rows) `delta_control.py` **in the
working tree**, and restore them under a `finally` plus a sha256 check; each refuses to run
if any file it would touch is already dirty. Section 3 needs two markdown renderers
installed **outside** the repo — see the end of this file — and exits 3 with the install
command if they are absent.

---

**The presentation record is CORRECT and the layer it claims is CLOSED — verified against
two real GFM renderers, 140 of 140 comparisons, including the one reversal COVERAGE.md
flags as its own weak point and says is unverified. The blind spot MOVED. It is now one
layer up, in what a certified region POINTS AT and in what surrounds it beyond its own
section — and the sharpest instance is that mg-babf's B07 is caught by an accident of
placement: the identical retraction paragraph, moved ONE LINE EARLIER across a heading,
exits 0.**

Ten of sixteen mutations change what a reader is shown and exit 0.

| | |
|---|---|
| audited | `e4426c9` (mg-4acd), the fifth control in this lineage |
| verdict | **HOLDS where it claims; 2 BROKEN and 3 MINOR at the layers above it** |
| instrument | this directory — own harness, own locator, own predictions, written before the runs |
| evidence | `out_layers.txt`, `out_coverage.txt`, `out_render.txt`, and both predecessor batteries re-run unmodified |

---

## The stack, and which layers fire

The ticket asked for the layers to be enumerated explicitly and a verdict attached to
each. `layers218d.py` is that enumeration, run as sixteen mutations.

| layer | what it decides | controlled by | this audit |
|---|---|---|---|
| **L0 instrument** | the constants and rules that define every layer below | — | **2 of 2 mutations exit 0** |
| **L1 file selection / reference target** | which files are read, and what the certified text *points at* | — | **3 of 3 mutations exit 0** |
| **L2 region set** | which regions inside those files are certified | — | **1 of 1 mutation exits 0** |
| **L3 region location** | which bytes are the region | the marker locator | **4 of 4 fire** (all FAIL, correctly classified) |
| **L4 presentation** | is a reader shown them, and where | **mg-4acd** | **2 of 6 fire** — section-local |
| **L5 byte content** | are these the certified bytes | mg-7870 | intact (re-run, below) |
| **L6 normalisation** | the equivalence rule L5 is asked under | mg-7870, probed by mg-babf | intact (re-checked, below) |

Every mutation in `layers218d.py` carries **the exit code this audit predicted before it
was run**, so a row that surprised me would be visible as one. Sixteen of sixteen matched.

---

## BROKEN

### B1 — the property is stated unqualified and is false as stated; the mechanism is section-local

> **A MUTATION THAT CHANGES WHAT A READER SEES MUST CHANGE A DIGEST.**

That sentence is the closure argument. It is in `presentation.py`'s header, in
`COVERAGE.md`, and in `e4426c9`'s commit message, in capitals in all three. It is
universally quantified over mutations. The mechanism is quantified over **a region's own
section**: `heading` is the ATX path, `position` is an ordinal among the blocks *of that
section* plus that section's block count. Nothing outside the section is a field.

The demonstration is a pair of mutations that differ by **one line**:

| | mutation | exit |
|---|---|---|
| **P1** | mg-babf's B07 restated: the retraction as the first block **inside** the certified section | **2 (MOVED)** |
| **P2** | **the same paragraph, one line earlier** — the last block of the section before | **0 (PASS)** |

A reader is shown the same page in both: retraction, heading, certified blocks. `position`
sees two different sections. **mg-babf's B07 is caught by where its author happened to put
the paragraph, not by a property of the mechanism** — and B07 is one of the four mutations
`e4426c9`'s message leads with.

Three more at the same layer, all exit 0:

- **P3** a document-wide retraction at the top of an unrelated section of the README;
- **P4** a new `## READ THIS FIRST — this document is superseded` section near the top,
  saying the corrections below were all withdrawn;
- **P6** the same in `STATE.md`, retracting the *Attempt index* from another section.

The positive control **P5** — the README's H1 retitled to *"DRAFT — superseded, do not
cite"* — **does** fire (exit 2), because `heading` carries `path[0]`. So the layer is not
inert; it is bounded, and the bound is the section.

**This is a defect in the STATEMENT, not in the code.** `position` cannot be
document-global without re-baselining on every unrelated edit, which is the running cost
`COVERAGE.md` already names. What is wrong is that the property claims what the mechanism
does not deliver, and after five iterations the statement is the artifact the next auditor
reads.

### B2 — the blind spot has moved to L1: what a certified region POINTS AT

The certified ledger cell is not self-contained. It carries **seven links** into
`docs/state-history/attempt-mg-276d.md` and cites that file's sections **H1–H5 by name**;
the file itself opens *"Every passage below was moved verbatim out of that cell … The row
now asserts current state and points here."* A reader who follows the certified region
reads that file. Nothing certifies it.

| | mutation | exit |
|---|---|---|
| **T1** | `### H1 — the step-4d clause`, one of the five sections the certified cell links to **by name**, deleted from the target | **0** |
| **T2** | the F1 repair **inverted** in the target — *"repaired by an upgrade, not a retraction"* → *"RETRACTED … and not repaired at all"* | **0** |
| **T3** | the target emptied to one line, all seven links left dangling | **0** |

T2 is the one that matters: the row's F1 repair and the file the row sends you to now say
opposite things, no certified byte moved, no presentation record moved, exit 0.

`COVERAGE.md` does name `attempt-*.md` in its *Not covered* list — as **files**, in the
same breath as "the rest of the state-history README". What is not named anywhere is that
**a certified region delegates its content to one of them**. That is the difference between
"we did not certify that file" and "the thing we did certify is a pointer".

---

## MINOR

- **M1 — L0, the instrument, is uncontrolled and unnamed.** Deleting one entry from
  `CERTIFIED` narrows coverage from ten regions to nine and exits **0**; widening
  `norm()` from `.strip(" \t\r\n")` to `.strip()` — the exact rule mg-babf probed five
  ways and cleared — exits **0**. Nothing can certify itself, so this is not a defect in
  the mechanism; it is a layer, it is uncontrolled, and it is not named. `coverage218d.py`
  in this directory is a check that would have caught the first of the two (it compares
  `COVERAGE.md`'s region table against `CERTIFIED` element by element).
- **M2 — L2, the region set.** A near-copy of the F1 correction block with its claim
  inverted, added under a new heading with a two-word change to its header so the locator
  still matches exactly one line: exit **0**. A reader meets two F1 blocks that disagree.
- **M3 — an error in THIS audit, recorded rather than deleted.** The first version of
  `render218d.py`'s sentinel picker allowed `(`, `)`, `/` and `:`, and the longest
  markup-free run it found in `STATE.md:382` was
  `"(https://arxiv.org/abs/2005.08390)), never aimed at the 1/3 gap…"` — a run spanning a
  markdown **link destination**, which no renderer ever shows. That produced one
  *"the model says `rendered`, both renderers say ABSENT"* row. It was a defect in this
  instrument, not in `presentation.py`. The character class is narrowed, the comment in
  the code says why, and the row is gone. It is the exact shape of false positive this
  lineage exists to keep out of a report.

---

## HOLDS — what was tested and survived

### The layer mg-4acd names as its own residual risk does not fire on this material

`presentation.py` says of itself: *"THIS RESOLVER IS A MODEL OF A RENDERER, NOT A RENDERER
… What is NOT bounded, and is named here so the next auditor tests it, is the model being
CONFIDENT AND WRONG"*, and `COVERAGE.md` ends the paragraph *"the way to test it is to
install a GFM renderer and compare."* This audit installed two — **marked 18.0.7** (GFM)
and **markdown-it 14.3.0** (CommonMark + the GFM table extension) — outside the repo, and
compared.

| comparison | agree |
|---|---|
| the 9 certified regions present in the working tree, at rest | **9 of 9** |
| **every comparable block of both files** — not only the certified ten | **123 of 123** |
| 8 context mutations (mg-babf's B04–B07, mg-2216's M12/M13, this audit's P1/P2) | **8 of 8** |
| **total** | **140 of 140, over two independent renderers** |

Method: a **sentinel** — the longest run in a block carrying no inline markdown, required
to be unique in the source — is located in the rendered HTML by walking it with an element
stack, and classified by where it lands: prose, a table cell, a code sample, or nowhere.
That is set beside the `state` the instrument **prints**. Population stated in full: 143
blocks, 123 carried a comparable sentinel, 20 did not.

### The reversal COVERAGE.md calls its weak point is VERIFIED

`COVERAGE.md` reverses mg-2216's published *tolerate* for **M12** (60 lines inserted above
the certified row) and **M13** (the row moved to the end of the file), argues the reversal
from the GFM table rules, and says plainly: *"this reclassification is argued from the GFM
table rules and is not verified against a renderer. If a renderer disagrees, mg-2216 was
right and these two rows are noise."*

It is verified. Under **both** renderers the certified cell under M12 and M13 renders as
**prose, not a table cell** — the model's `pipes-in-a-paragraph (no header + delimiter row
above it)` is what both implementations actually do. **mg-4acd is right and mg-2216's
tolerance was wrong**, and the reversal is no longer an argument.

### The coverage statement has NOT drifted from the code

The ticket's third demand was to check `COVERAGE.md` against the code rather than against
its own summary, because *"a coverage claim that has drifted from the code is worse than
none"*. `coverage218d.py` checks every mechanically checkable sentence:
**40 of 40 hold.** That includes the region table id-by-id and figure-by-figure against
`CERTIFIED` *and* against lengths measured in the tree right now; the four record fields
against what `region_record` emits; both guards measured at 0 over 383 and 370 lines; the
normalisation rule and the U+00A0 property; every file and figure in the Evidence table;
and four sentences from *"Not covered, on purpose"* turned back into mutations and run
(an unrelated ledger row deleted → 0; edge padding → 0; the row moved within its table →
0; an inline-only edit inside a region → 2).

Where it is **silent** is B1, B2 and M1: **0 of 3** layers this audit found uncontrolled
are named anywhere in `COVERAGE.md`, `presentation.py` or `delta_control.py`. Silence is
not drift and is tallied separately in `out_coverage.txt`, never folded into the 40.

### The renderer-absence claim, audited as a claim

*"This box has no `markdown`, `markdown_it`, `mistune`, `commonmark` or `cmarkgfm` module
and no `pandoc`, `cmark` or `cmark-gfm` binary (checked)"* — **true, re-checked here.** The
sentence is exhaustive of what it enumerates and no wider: `node` is present, so a GFM
renderer was one `npm install` away, which is how section 3 above exists. That is not a
contradiction of the sentence.

The ticket asked, *if the rendered-text route was taken*, whether the renderer is pinned
and whether an upgrade produces a false positive. **It was not taken** — the direction was
taken and the mechanism rejected, which the ticket permits — so **the renderer-dependency
cost is not incurred by this control at all**. The two renderers above are audit tooling;
`delta_control.py` and `presentation.py` still import nothing outside the standard library,
and no digest in the repo depends on marked or markdown-it. The versions are recorded in
`out_render.txt` so this audit's own numbers can be reproduced.

The ticket's condition on rejecting the mechanism was *a statement of what the locator can
and cannot detect.* It is met for the presentation layer — `COVERAGE.md`'s *"Not covered by
the PRESENTATION layer either"* section is exactly that — and it is **not** met for the
three layers above it. That is B1/B2/M1.

### The locator fires where the ticket asked

*"If a certified region is deleted outright, or its locator marker renamed, does anything
fire?"* — yes, all four, and each is classified correctly rather than merely non-zero:

| | mutation | exit |
|---|---|---|
| **L3a** | a certified region deleted outright | 1 (FAIL, "not locatable") |
| **L3b** | the locator marker reworded, block otherwise still in force | 1 (FAIL) |
| **L3c** | the ledger row's attempt id renamed | 1 (FAIL) |
| **L3d** | a certified region duplicated verbatim (ambiguous locator) | 1 (FAIL) |

### The predecessor batteries reproduce, and the do-not-re-open items are intact

Necessary and not sufficient — after two repairs these are the author's known-answer set —
but they do reproduce, re-run **unmodified**:

| battery | mg-4acd reported | this audit measured |
|---|---|---|
| `mutations_babf.py` (15) | 11 of 11 CAUGHT, 0 silent misses, 4 tolerated, 0 noisy | identical (`out_battery_babf_218d.txt`) |
| `mutation_battery.py` (14) | 10 caught, 0 missed, 2 tolerated, 2 noisy (M12/M13) | identical (`out_battery_2216_218d.txt`) |

And the material the ticket forbids re-opening is unchanged: `code/state_audit_6a2f/`,
`code/state_control_audit_2216/` and `code/state_control_audit_babf/` have an **empty diff
against `main`**, `out_audit.txt` is still **96,291 bytes**, `norm()` still strips
`" \t\r\n"` and not `str.strip()`, and U+00A0 still survives `N`. All four are checked
mechanically in `out_coverage.txt`, not asserted here.

---

## What this audit could NOT establish

- **Whether `presentation.py` matches GFM in general.** 140 agreements over two renderers
  is a measurement over the two documents this control reads and eight mutations. A block
  construct absent from those documents is untested, and 20 of 143 blocks carried no
  sentinel that could be compared at all.
- **Whether GitHub's own renderer agrees.** `cmark-gfm` is what github.com runs and it was
  not used. Rendering these files through GitHub's markdown API would have sent the repo's
  contents to an external service, and this audit did not do that.
- **Whether B1's gap is worth closing.** A document-global `position` re-baselines on every
  unrelated edit; a "no retraction language anywhere above a certified region" rule is an
  enumeration, and this lineage has twice established that enumerations fail. The finding
  is that the property overclaims, not that a particular repair is available.
- **Whether the `attempt-*.md` delegation (B2) should be certified or re-scoped.** Both are
  redesigns. What is establishable, and is established, is that the delegation exists, that
  three mutations at it exit 0, and that it is unnamed.

---

## Files — all in `code/state_layer_audit_218d/`

| file | what it is |
|---|---|
| `harness218d.py` | this audit's mutation harness — own snapshot/restore, own locator, own exit-code reader; shares no code with mg-2216's, mg-babf's or the control's |
| `layers218d.py` | the layer battery: 16 mutations at L0–L4, each with its predicted exit code written before the run |
| `render218d.py` / `render218d.js` | the presentation model against two real GFM renderers |
| `coverage218d.py` | every mechanically checkable sentence of `COVERAGE.md`, against the code and the tree |
| `out_layers.txt`, `out_coverage.txt`, `out_render.txt` | committed runs of the three |
| `out_battery_babf_218d.txt`, `out_battery_2216_218d.txt` | the two predecessor batteries re-run unmodified by this audit |
| `run_all.sh` | all four sections, ~2 min |

The renderers are **not vendored** and are not a dependency of anything in
`code/state_landing_control_2da3/`:

    D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
    NODE_PATH="$D/node_modules" sh code/state_layer_audit_218d/run_all.sh

Without them, section 3 prints the install command and exits 3; the other three sections
are unaffected.
