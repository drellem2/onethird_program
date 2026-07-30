# `state_delegation_repair_0049` — mg-0049's repair of mg-5644's B1

The object repaired is `code/state_landing_control_2da3/`, the **seventh** control in this
lineage. The audit being answered is **mg-5644** (merged `3a80d99`), which audited
**mg-bee1** (`a2d5a81` + `2a29f30`).

```sh
D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
NODE_PATH="$D/node_modules" sh code/state_delegation_repair_0049/run_all.sh    # ~7 min
```

## What was broken, in one line

**mg-bee1's repair created the surface it was then blind on.** Closing mg-218d's B2 meant
delegating: the certified ledger cell cites five sections of
`docs/state-history/attempt-mg-276d.md` **by name**, and mg-bee1 gave each of them a content
digest. It gave them nothing else. The two files the instrument **reads** carry three things
— a content digest, a presentation record, and section 8's default-deny guards over the whole
file. The file it **points at** carried the first of the three.

So mg-5644 put mg-babf's own `B05`/`B06` to it, one file out: **one `<!--` line at the top of
the target, never closed.** Every cited section byte-identical. Every delegated digest
matching. `marked` and `markdown-it` agreeing over 60 comparisons that **zero of the five
cited sections are visible at all** — a reader following the certified cell's six links **is
shown a blank page** — and **the control exits 0**.

## What this repair does

**No new mechanism.** `presentation.py` is applied to the delegated surface the way it is
already applied to the certified one:

- **section 2c** takes a **presentation record** per cited section, over the *whole* section
  with its heading line included, so `state` is `rendered` only if every line of it is. Not
  presented → **FAIL**; record moved → **MOVED**.
- **section 8**'s two default-deny guards now read **every declared target file** in full,
  exactly as they read `STATE.md` and the state-history README.

Both halves were needed, and this is the part a one-line summary of the repair gets wrong.

## The guards ALONE would have closed R1 and not R2 — measured, not argued

mg-5644's recommendation, and the work item filed from it, both name section 8's guards.
Taken literally and alone that closes **one** of the two rows: a fenced code block is
*inside* `presentation.py`'s declared subset, so `anomalies()` is silent about it by design
and `html_tokens()` skips fenced lines by construction. `R2` is caught by the **presentation
record** alone, on `state = fenced-code` — which is exactly how the same mutation is caught in
the two files the instrument reads. It is still one mechanism; both halves of it had to cross
the file boundary. `split_0049.py` measures this over all nine rows:

| regime | rows still exit 0 | count |
|---|---|---|
| mg-bee1 (content digest only) | `R1` `R2` `R3` `R4` `R5` `R6` `R8` `R9` | **8 of 9** |
| a guards-only extension | `R2` `R3` `R4` `R6` | **4 of 9** |
| mg-0049 | `R3` `R4` | **2 of 9** |

The two that remain are the **stated bound**, not a miss — see below.

## The nine rows, every exit code predicted before the run

Run on **mg-5644's harness, imported unmodified**. mg-bee1 argued the right way round for a
party under test — an auditor builds its own harness, a repair runs on the auditor's — and
that is kept. **9 of 9 behaved as predicted.**

| | mutation | vs mg-bee1 | vs mg-0049 | caught by |
|---|---|---|---|---|
| `R1` | the cited file HTML-commented whole (reader sees nothing) | 0 | **1** | guard **and** record |
| `R2` | the cited file fenced whole (renders as a code sample) | 0 | **1** | **record alone** |
| `R3` | a retraction at the **top** of the target | 0 | 0 | *the bound* |
| `R4` | a new **uncited** section appended to the target | 0 | 0 | *the bound* |
| `R5` | a `<details>` wrapper: suppresses nothing, is raw HTML | 0 | **2** | **guard alone** |
| `R6` | the cited sections moved under an "Appendix Z" heading | 0 | **2** | **`heading` field alone** |
| `R7` | a cited section **deleted** (positive control) | 1 | 1 | inherited mechanism, unweakened |
| `R8` | the whole file inside a **closed** HTML comment | 0 | **1** | guard **and** record |
| `R9` | one **tab** in the target's uncited opening paragraph | 0 | **2** | guard — **this is a cost** |

## The bound, stated in terms of what a READER IS SHOWN

This lineage's recurring defect is **a true sentence quantified over the wrong thing**.
mg-bee1 published the bound as *"closed for **cited sections**"* — quantified over *which
sections are followed*, which says nothing about whether a reader sees them. What is now
certified:

> A reader who follows a certified region's citation **is shown** the section it names, as
> prose, under the heading path that was certified — for every section any certified region
> cites by name.
>
> **What a reader is shown on that page outside those sections is not certified.** The
> target's title, its opening paragraph and its uncited sections are text a reader **is**
> shown, and no field of any record answers for them: `R3` and `R4` still exit 0. The claim
> is about the sections a citation **lands on**, not about the page they sit in.

## The cost, printed rather than conceded

`R9` — one tab in an uncited paragraph of the target, which changes **nothing** a reader sees
on either renderer (measured: `render0049.py`, 5/5 sections still shown as prose on both) —
**exits 2**. That is the price of extending default-deny to a third file, and the two
certified files have always paid it. A re-baseline nobody expected is how a control stops
being run, so it is a battery row and a sentence in `COVERAGE.md` rather than a discovery for
the next auditor.

## What is NOT undone — re-measured, not read off committed outputs

| claim | measured here |
|---|---|
| mg-218d's 16-mutation battery, **unmodified** | `git diff a4aeeb9..HEAD -- code/state_layer_audit_218d/` is **0 bytes**; re-run in section 7 of `run_all.sh` |
| mg-5644's own battery, **unmodified** | `git diff 3a80d99..HEAD -- code/state_delegation_audit_5644/` is **0 bytes**; re-run in section 7 |
| mg-5644's `Q1` `Q2` | now report **"did not behave as this audit predicted"** — they predicted exit 0 and got exit 1. That is the repair, reported by the auditor's own instrument, unedited |
| mg-5644's `Q3`–`Q6` | unchanged: 0, 0, 1, 2 |
| the statement repair, the 141/141 renderer agreement, the 10→6 improvement, the surviving document-global-ordinal negative | **untouched.** Nothing in `globalpos_bee1.py`, `render218d.py` or `l2pop5644.py` is edited or contradicted here |
| `coverage218d.py` | **40 of 40** claims in `COVERAGE.md` still hold against the code, the tree and a mutation |
| the eleven certified regions | **no content digest and no presentation digest moved.** `STATE.md` and the state-history README are not edited by this repair at all |

## Which layer is uncontrolled after this fix

**Seven for seven it has moved rather than closed, and this generation was the sharpest form:
it moved onto ground the previous repair itself laid. Assume the same of this one.**

The layer to read as newly open is **what a reader is shown on the delegated target OUTSIDE
its cited sections** — `R3` and `R4`. It is **structurally identical** to the cross-section
gap mg-218d found in the two certified files: a bound at the *section*, and a reader who does
not read in sections. The mechanism was carried across the file boundary and its bound came
with it.

**Where I would look next, in order.**

1. **A reader-scoped rather than section-scoped bound.** The honest sentence is about a
   *page*; every mechanism here is about a *section*. That mismatch is the whole lineage in
   one line, and it is now present on two surfaces.
2. **The delegation surface's own derivation.** `delegation_map()` follows links whose *text*
   matches `H<n>`. A certified region that cites a section in prose — "see H4 of the attempt
   file" — or links it with different text delegates **nothing**, and nothing says so. The
   surface is default-deny about targets it *finds*; it is silent about citations it cannot
   see. That is a list-shaped hole in a rule that was adopted precisely to stop being a list.
3. **L2, still open, and now open on two surfaces.** A near-copy of a cited section, added to
   the target under a new name, is a region that is not on the set.

## Files

| file | what it is |
|---|---|
| `mutations_0049.py` | the nine mutations, defined once so the battery and the decomposition are over the same population. Every one edits **only** the delegated target |
| `battery_0049.py` | the nine run against the real control as a subprocess, on mg-5644's harness unmodified. Exit codes predicted before the run |
| `split_0049.py` | which **mechanism** catches which row — content / guards / presented / record — and the three regimes derived from them. In memory; touches nothing |
| `render0049.py` | this repair's five **new** claims against `marked` and `markdown-it`: 100 comparisons, both agreeing on every one |
| `run_all.sh` | all of the above, plus the two `git diff` proofs and mg-5644's whole audit re-run |

`out_*.txt` are the committed outputs of a single run of `run_all.sh`.

## Safety

`battery_0049.py` and section 7's re-runs mutate tracked files in the working tree and
restore them under a `finally` plus a sha256 check; each refuses to run on a dirty tree.
`split_0049.py` and `render0049.py` mutate nothing on disk — every mutation there is applied
to a string in memory. Nothing in `code/state_landing_control_2da3/` imports anything from
this directory.
