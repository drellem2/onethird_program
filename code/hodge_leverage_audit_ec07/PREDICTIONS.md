# mg-ec07 — predictions, written before the first run

Every row below was written before `audit_ec07.py` was run for the first time, and before any
mutation was applied to the tree. **Misses are kept as written**, with what they turned out to be.

This is an INDEPENDENT audit of mg-ff3e's repair of mg-9207. Nothing here re-runs mg-ff3e's
`repair_9207.py` or mg-9207's `audit_8eca_repair.py` and reports their totals: **replication is
not corroboration when the copies share a source.** Every population below is derived from the
tree by this instrument's own code.

## The exit codes, every one, predicted before running

| command | predicted exit |
|---|---|
| `python3 code/hodge_leverage_landing_e1d0/verify_landing.py`, clean tree | **0** |
| `python3 audit_ec07.py --full` | **1** — the arc's convention is exit 1 when an audit raises a finding, and A5/A6 are expected to raise one |
| `X1` STATE.md ledger **column headers** exchanged, real runner on disk | **0 — SILENT** |
| `X2` two ledger **row verdict labels** exchanged next to the A5 row, real runner | **0 — SILENT** |
| `X3` H8's two historical **column headers** exchanged (mg-9207's `E3`, in-site control) | **1** |
| `X4`/`X5`/`X6` one **figure** exchange per site, real runner on disk | **1** each |
| `B1` `--reseal` with a live figure corrupted on disk | **1 — REFUSED** |
| `B2` `--reseal` with `partition` bent lossy (D3's shape) | **1 — REFUSED** |
| `B3` `--reseal` after mg-9207's `E2` label exchange at H8 | **0 — BLESSED** |
| `B3b` the real runner after `B3` has resealed | **0 — GREEN with the defect on the page** |
| `B4` `--reseal` with the refusal itself deleted, live figure corrupted | **0 — BLESSES A WRONG DOCUMENT** |

## A1 — the record is the site, byte for byte (my own instrument, in memory, a fixture)

Population, derived from the tree and not from a list: **37 866 characters** over the three sites
(`the STATE.md row` 13 367, `§14` 16 647, `H8` 7 852). Each character substituted **alone** with a
character it is not, and `census_gate` — the live gate, called directly — asked whether any row
refutes.

| | prediction |
|---|---|
| A1 at `HEAD` | **37 866 of 37 866 fire.** If the record really is lossless there is no byte of the site that can move in silence |
| A1 against the **pre-repair** gate (`eb600f7`, where the defect is still present) | **between 373 and 800 of 37 866**, i.e. under 3%. 373 of those characters are inside asserted figure tokens; the rest are the guard characters immediately around a token. This is the control: an instrument that catches nearly everything at `HEAD` and almost nothing one commit earlier is measuring the repair and not itself |

## A2 — which row catches it

| | prediction |
|---|---|
| every non-figure character that fires at `HEAD` | caught by **`SITE RECORD`** |
| every figure character | caught by **`FIGURE CENSUS`** and/or **`FIGURE ORDER`** |
| **`RECORD PARTITION`** | **fires 0 of 37 866.** `rejoin(partition(raw)) == raw` is an identity that holds for *every* string, so no mutation of the document can move it. That is not a defect — it is what mg-ff3e said it was, and why `D3` had to bend the code to falsify it — but it means the row that licenses "the whole record is compared" is **unfalsifiable by any document edit**, and this audit says so with a number |

## A3 — the figure half is not disturbed (my own `C3`, at a derived population)

Population: **847** unordered pairs of asserted figure slots with **differing values**, per site
(127 / 116 / 604), enumerated from `partition`, not from anybody's list of twelve.

| | prediction |
|---|---|
| exchanges that fire | **847 of 847** |
| `FIGURE ORDER` refuted on each | **847 of 847** |
| `SITE RECORD` green on each | **847 of 847** — the record masks figures with a value-independent marker, so moving figures must not move the record |
| `RECORD PARTITION` green on each | **847 of 847** |
| `FIGURE CENSUS` green on each | **847 of 847** — a transposition preserves a multiset exactly, which is mg-8aae's `H-1` |

If this holds, mg-9207's *12 of 12 at 3 of 3* is not merely re-run, it is **re-derived at 70× the
population by an instrument that shares no code with it**, and mg-ff3e has not weakened it.

## A4 — "two occurrences of the same token exchanged is an empty set" — measured, not read

Population: **39** equal-value figure pairs (9 / 4 / 26). For each, exchange and compare the
resulting text to the original **byte for byte**.

**Prediction: 39 of 39 are byte-identical**, so mg-ff3e's second uncovered bullet is an empty set
rather than a blind spot, and this audit turns that sentence into a measurement.

## A5 — the field it does not reach, ON DISK

The claim under audit is *"position-aware over the WHOLE record"* — mg-ff3e's own words, and the
assignment's first branch: **find a field it still does not reach.**

| probe | prediction |
|---|---|
| `X1` `STATE.md`'s ledger table **column headers** (`\| verdict \| attempt \| note \|`) exchanged | **SILENT — runner exit 0, 0 refuted.** This is *the identical kind* as mg-9207's `E3`, which mg-ff3e enumerated and caught. It is silent here because the `STATE.md` site is **one line**, so the header of the table that line sits in is outside it |
| `X2` the verdict labels of the two ledger rows **immediately above** the A5 row exchanged | **SILENT — exit 0.** mg-9207's `E2b` kind, outside the site |
| `X3` H8's two historical column headers exchanged — **the discrimination control** | **exit 1, `SITE RECORD @ H8` refuted, H8's `FIGURE CENSUS` and `FIGURE ORDER` green.** Same kind, inside a site. If `X3` were silent too, `X1`/`X2` would be my probes failing rather than the gate |
| restorations | 3 of 3 sha256-identical to the pre-probe file |

## A6 — the stated set against the code

mg-ff3e states the residue rather than hiding it, so the assignment's third branch applies too:
**verify the stated set matches the code.**

The sentence, printed beside the gate and in `R5`: *"text OUTSIDE the site is not read, **because a
site is a section**."*

| | prediction |
|---|---|
| sites obtained by `section()` | **2 of 3** (`§14`, `H8`) |
| sites obtained by `find_line()` — **one line, not a section** | **1 of 3** (`the STATE.md row`) |
| the sentence as written | **false at 1 of 3 sites**, and it is the site whose file is largest |
| bytes of the three files inside a record | **37 866 of 320 509 — 11.8%** |
| bytes outside every record | **282 643 — 88.2%** |

`X1`/`X2` are the assignment's *"add a field outside it and confirm the claim visibly stops
matching rather than silently going stale"*. **Prediction: it goes stale silently** — the runner
stays green.

## A7 — the blessing path (the floor item; no list in the assignment names it)

`--reseal` is, in mg-ff3e's own words, *"the one step in this instrument that can make a wrong
document green"*. mg-ff3e names three things that narrow it. **Nothing in the arc executes it.**

| | prediction |
|---|---|
| `B0` invocations of `--reseal` in `code/` and `docs/`, excluding prose | **0 executed anywhere** — named in four places, run in none |
| `B1` a live figure corrupted, then `--reseal` | **REFUSED, exit 1, `site_records.txt` sha256 unchanged** |
| `B2` `partition` bent lossy, then `--reseal` | **REFUSED, exit 1** — `RECORD PARTITION` is *not* in the `"SITE RECORD" not in d` exclusion, so it blocks |
| `B3` mg-9207's `E2` label exchange, then `--reseal` | **exit 0, record CHANGED, runner then green.** By design; the whole narrowing is that a human reads the diff. I will report **how many lines that diff is** |
| `B4` the refusal deleted (`blocking` filter removed), live figure corrupted, `--reseal` | **exit 0 — a wrong document blessed.** The deletion test for the control, at its finest unit |
| `B5` `reseal()`'s `measured` against `t1`'s | **identical**, both from the working tree |

## A8 — the same-kind enumeration: did it HAPPEN?

This is a different question from whether the fix works, and it is checked from **git**, not from
the report's own summary of itself.

| | prediction |
|---|---|
| an enumeration exists | **yes** — `PREDICTIONS.md` R1, 7 rows; `N19`–`N25` of the runner's own control |
| each item CHECKED rather than named | **7 of 7 checked** — every one is a probe with a written verdict and a transcript line |
| the enumeration is the parent's own | **4 of 7 are its own** (`E6`–`E9`); 3 are mg-9207's verbatim (`E2`/`E2b`/`E3`) |
| it happened **BEFORE** the fix | **NO, not demonstrably.** The earliest commit in which any of the seven appears is `c7f9079` — **the commit that lands the fix**. There is no artifact in this repository, at any earlier commit, that enumerates the same-kind set. The enumeration is *contemporaneous with* the fix, not prior to it |
| the enumeration's **grain** | **kinds, not sites × kinds.** `E3` (column headers) was checked at `H8` and nowhere else, and `X1` is that exact kind at the site where it is unreachable. This is the cost of the grain and it is measurable |

## What would refute this audit

- Any of A1's 37 866 characters moving in silence at `HEAD` — that would refute mg-ff3e's claim,
  not this audit, and I predict none do.
- `X3` silent — my probes would be broken and `X1`/`X2` would prove nothing.
- A3 dropping below 847 of 847, or `SITE RECORD` firing on a figure exchange — mg-9207's `C3`
  would have been disturbed and I would have to report it.
- `B1` blessing a wrong figure — the refusal would not be load-bearing.
- The pre-repair control catching more than ~800 of 37 866 — my A1 instrument would not be
  measuring the repair.

## Added during construction, before the first run, and marked as such

Two things were added while the instrument was being written and **before it had ever been run**.
They are listed here separately rather than folded into the tables above, because a prediction
that appears after the fact is not a prediction and a *measurement* that appears after the fact
should say so.

- **A2b — did the asserted-figure population itself move?** mg-ff3e re-derived `figure_sequence`
  from `partition` and unified the marked-quotation convention. If *which* tokens count as
  asserted had changed, A3 would not be comparing like with like. Recorded as a **measurement**,
  not scored. (Expectation, stated for the record: identical at 3 of 3.)
- **A5b — one figure exchange per site, on disk.** A3 is a fixture in memory; this bridges it to
  the artifact. The pair is chosen **equal-length and differing-value**, because three of the five
  measurements are lengths of these files and a probe that changed one would fire the designated
  readers for a reason that has nothing to do with the record. **Prediction: exit 1 at 3 of 3,
  `FIGURE ORDER` refuted, `SITE RECORD` green.**

## Round 2 — one probe added AFTER round 1, predicted before it was run

Round 1's `B3` missed: I predicted the runner would exit **0** after a reseal blessed a label
exchange, and it exited **1**. The reason is not a gate row — all 34 gate rows are green — it is
that `N21`, one of the seven pre-registered same-kind probes, locates its text **by content**, and
after the exchange its literal is no longer there, so it reports `PROBE NOT APPLIED` and the
negative control's aggregate reads **6 of 7**. That is the runner noticing **its own probe's
literal moved**, not the gate noticing the document is wrong.

So the decisive probe is a label exchange that is **not one of the seven frozen literals** and is
**not read by any designated reader**: in H8's first code block, exchange the two 29-character
row labels `deliverable §14 copy` and `the mismatch A5 reports`, which makes the block assert that
the §14 copy is `10 623 chars (unchanged)` **and** that it is `2 928 -> 6 069 chars (more than
doubled)` — a reader-visible contradiction, no figure moved.

| | prediction |
|---|---|
| `B6a` the exchange alone, real runner | **exit 1, `SITE RECORD @ H8` refuted** — the repair works, which is what makes the rest of this probe meaningful |
| `B6b` `--reseal` after it | **exit 0 — BLESSED** |
| `B6c` the real runner after the reseal | **exit 0, 0 refuted, fully green** — no gate row, no probe, and no aggregate notices |

## Misses, kept as written

Four predictions missed. Two were this instrument's own defects, one was an understatement, and
**one is the largest finding in the audit.**

- **`A7-B2` — predicted `--reseal` REFUSED (exit 1) with `partition` bent lossy. Observed exit 0:
  it BLESSED, and the record it wrote was built from a partition that is not the section.** The
  prediction's stated reason — *"`RECORD PARTITION` is not in the `"SITE RECORD" not in d`
  exclusion"* — is wrong, and it is wrong for the reason that makes it interesting: the
  `RECORD PARTITION` row's own explanation *names* `SITE RECORD` (*"…everything else by SITE
  RECORD, and nothing is in neither"*), so the substring test excludes it. 3 of 34 gate rows are
  excluded that were never meant to be. **This became finding E-5**, and it is R5 item 3 — the
  defect mg-ff3e found in its own scoring code and fixed there — still live in the artifact it was
  repairing.
- **`A2` — predicted the attribution would PARTITION: non-figure characters caught by `SITE
  RECORD`, figure characters by the `FIGURE` rows. Observed `SITE RECORD` catches all 37 866**,
  figure characters included, because destroying a figure token moves its bytes into a segment.
  The figure rows catch 462 and add nothing on this population; they earn their keep on
  **exchanges**, where `SITE RECORD` is green on all 847. Recorded as `A2c`: neither row is
  redundant, and each is the whole of the answer on the population the other is blind to.
- **`A7-B3` — predicted the runner would exit 0 after a reseal blessed a label exchange. Observed
  exit 1**, with all 34 gate rows green. The cause is `N21` reporting `PROBE NOT APPLIED` because
  its own frozen literal had moved — the runner noticing *its own probe*, not the document.
  Round 2's `B6` is the probe that miss demanded, and `B6` came out **exit 0, 0 refuted**.
- **`A7-B0` — predicted 0 invocations of `--reseal` under `code/`. Observed 1: this file.** An
  instrument that counts itself in its own population. Fixed by excluding this directory; the
  original reading is kept here because it is the same shape as the two defects mg-ff3e kept in
  its own `PREDICTIONS.md`.

Everything else held exactly: `A1` 37 866 of 37 866 and the pre-repair control 462 (predicted
373–800); `A3` 127 / 116 / 604 = **847 of 847**; `A4` **39 of 39**; `A6` 2 of 3 sites are sections
and 88.2% of the three files are outside every record; `X1`/`X2` **silent at exit 0** with `X3`
**caught at exit 1**; `A5b` 3 of 3; `B1` refused; `B4` blessed; `A8` 0 of 7 before the fix and
7 of 7 checked.
