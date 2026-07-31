# Independent audit of the mg-9207 repair (mg-ff3e)

**Audit id:** mg-ec07 · **pre-filed in the same action as its parent** · **instrument:**
`code/hodge_leverage_audit_ec07/`, `sh run_all.sh`, ~1 min, exit 1 ·
**transcript:** `code/hodge_leverage_audit_ec07/out_audit_ec07.txt` ·
**predictions, written before the first run, every miss kept:**
`code/hodge_leverage_audit_ec07/PREDICTIONS.md`

**Target:** `code/hodge_leverage_landing_e1d0/verify_landing.py` at HEAD — the census made
*"position-aware over the WHOLE record"* by `c7f9079` and `11ef9a9`, reported by `3bf0cd2`.

**56 checks recorded, 40 confirmed, 14 measurements, 2 refuted, 6 findings. Verdict: PARTIAL.**

---

## The answer to the question the assignment asks first

> *Did it fix the SET, or the next field?*

**It fixed the set — over the site. The projection did not go away; it moved up a level, from the
FIELD to the SITE.**

The lossless half of the claim is true, and this audit measures it at the finest unit there is.
`A1` substitutes **every character of every site, alone** — a population of **37 866**, derived
from the tree and not from any list — and asks the live `census_gate` whether any row refutes:

| site | characters | fire at HEAD | fire at `eb600f7` (the repair's parent) |
|---|---|---|---|
| the `STATE.md` row | 13 367 | **13 367** | 110 |
| `§14` | 16 647 | **16 647** | 112 |
| `H8` | 7 852 | **7 852** | 240 |
| **total** | **37 866** | **37 866 (100.0%)** | **462 (1.2%)** |

The right-hand column is the control the standing instructions require: the same instrument, run
against the gate at the commit where the defect is still present, catches **1.2%**. An instrument
that fires on everything is not measuring the repair. This one is.

**But the field it does not reach is the site boundary, and the same kind of exchange is still
silent in it.** `A5` runs three probes on disk, against the real runner, no environment variable
set, every one length-preserving and moving no figure:

| probe | what is exchanged | where | exit | refuted |
|---|---|---|---|---|
| `X3` | H8's two historical **column headers** — mg-9207's `E3` verbatim | **inside** a site | **1** | 3, incl. `SITE RECORD @ H8` |
| `X1` | `STATE.md`'s ledger table **column headers** (`\| verdict \| attempt \| note \|`) | outside every site | **0** | **0** |
| `X2` | the **verdict labels** of the two ledger rows immediately above the A5 row | outside every site | **0** | **0** |

`X1` is *the same mutation as `X3`*. mg-9207 raised it, mg-ff3e enumerated it, checked it, and
caught it — at `H8`. At the `STATE.md` site the identical mutation is exit 0 with nothing refuted,
and the reader is left with a ledger whose verdict column is labelled `attempt`. `X3` is the
discrimination control: without it, `X1`'s silence would be my probe failing rather than the gate.

### Finding E-1 — the residual projection is the SITE, and it is now the whole of the residue

This is **not** a claim that mg-ff3e hid it. mg-ff3e states it, plainly, beside the gate. The
finding is that the residue *is* the whole of what is left, that it is very large, and that it is
of the same kind the arc has now met six times.

### Finding E-2 — the sentence that sizes that residue is not true of the code at 1 of 3 sites

The disclosure a reader meets, in `verify_landing.py` and again in R5:

> *"text OUTSIDE the site is not read, **because a site is a section**."*

Measured against the code: **2 of 3 sites are sections.** The `STATE.md` site is **one line**,
returned by `find_line`, not by `section`. So what is excluded there is not *"the rest of the file
outside this section"* — it is *"the whole ledger table this row is a row of, including its column
headers"*, which is exactly what `X1` exchanges.

| | inside a record | outside every record |
|---|---|---|
| `STATE.md` (183 508 chars) | 13 367 | 170 141 |
| the deliverable (115 974) | 16 647 | 99 327 |
| the history file (21 027) | 7 852 | 13 175 |
| **total (320 509)** | **37 866 — 11.8%** | **282 643 — 88.2%** |

This is the shape mg-ff3e's own R5 opens by naming: *"Both of the last two findings were a printed
extent slightly wider than the code beneath it."* It is a third instance, in the deliverable that
says so.

The assignment's third branch — *add a field outside the stated set and confirm the claim visibly
stops matching rather than silently going stale* — is `X1` and `X2`. **It goes stale silently.**

---

## The second question, which is not the same question

> *The parent is required to enumerate what else is of the same kind BEFORE fixing. Check the
> enumeration exists, is the parent's own, and that each item was checked rather than named.*

Checked from **git** and from the runner's own stdout on this run, not from mg-ff3e's summary of
itself.

| | result |
|---|---|
| **does an enumeration exist?** | **Yes** — `N19`–`N25`, seven probes, four kinds named as kinds (labels beside a figure, a column heading over a figure, a figure inside a marked quotation, layout) |
| **was each item CHECKED rather than named?** | **Yes, 7 of 7.** Each carries a verdict *written before the run* and an *observed* verdict, both printed by the runner on this run — not only in a committed transcript |
| **is it the parent's own?** | **Substantially. 4 of 7** (`N22`–`N25`) are mg-ff3e's own additions; 3 carry finding ids mg-9207's own artifact names (`E2`/`E2b`/`E3`) |
| **did it happen BEFORE the fix?** | **Not demonstrably. 0 of 7** exist at any commit before `c7f9079` — the commit that lands the fix. There is no artifact in this repository, at any earlier commit, that enumerates the set |

The discipline **worked**, and that should be said first: seven kinds, all seven exercised, four of
them found by asking the question rather than by being told. That is the difference between this
repair and the two before it, and it is why the figure case and the label case are both closed
inside the site.

### Finding E-4 — the enumeration is over KINDS, not over SITES × KINDS

Each kind was checked at **one** site. `N21` — a column heading over a figure — was checked at
`H8`. The same kind at the `STATE.md` site is `X1`, and `X1` is silent. The question *"what else is
of the same kind as the thing I just fixed?"* was asked of the **mutation** and not of the
**site**, so the set that got fixed is *the set of exchange kinds at the sites that were already
being probed*.

This is the same generator mg-ff3e diagnosed one level down. Its own words: *"each repair widened
the projection BY ONE NAMED FIELD, so the next exchange moved into what was still dropped."* The
enumeration widened the set of **kinds** and the complement became the set of **sites**.

---

## The third question — nothing confirmed was disturbed

> *12 of 12 exchanges red at 3 of 3 sites for figures. Re-run it and report.*

**Replication is not corroboration when the copies share a source**, so mg-9207's instrument is not
re-run here and its bottom line is not quoted. `A3` builds the population from `partition`: **every
unordered pair of asserted figure slots whose values differ.**

| site | pairs | fire | `FIGURE ORDER` refuted | `SITE RECORD` green | `RECORD PARTITION` green | `FIGURE CENSUS` green |
|---|---|---|---|---|---|---|
| the `STATE.md` row | 127 | 127 | 127 | 127 | 127 | 127 |
| `§14` | 116 | 116 | 116 | 116 | 116 | 116 |
| `H8` | 604 | 604 | 604 | 604 | 604 | 604 |
| **total** | **847** | **847** | **847** | **847** | **847** | **847** |

`FIGURE ORDER` is the **only** census row that fails on a figure exchange, at **847 of 847** —
mg-9207's result re-derived at 70× its population by an instrument that shares no code with it,
*after* two rows were added to the gate. `A5b` bridges the fixture to disk: one equal-length
differing-value exchange per site, real runner, **3 of 3 exit 1 with `FIGURE ORDER` refuted and
`SITE RECORD` green**.

`A4` turns mg-ff3e's second uncovered bullet from a sentence into a measurement: **39 of 39**
equal-value figure exchanges are byte-identical to the original. It is an empty set, and that is
now checked rather than asserted.

`A2b`: the asserted-figure population is **identical** at 3 of 3 sites before and after the repair,
so the comparison above is like with like.

### A2c — neither half of the record is redundant, with both numbers

On **point mutations** `SITE RECORD` catches 37 866 of 37 866 and `FIGURE ORDER` 462: `SITE RECORD`
alone would do. On **exchanges** `FIGURE ORDER` catches 847 of 847 and `SITE RECORD` 0: `FIGURE
ORDER` alone does. Each row is the whole of the answer on the population the other is blind to,
which is why mg-ff3e's `D1b`/`D2` split at that seam was the right unit.

### A2 — the row that licenses the claim cannot be moved by any document

`RECORD PARTITION` fires on **0 of 37 866** single-character mutations. `rejoin(partition(raw)) ==
raw` is an identity that holds for every string, so no edit to any document can falsify it. That is
not a defect — it is what mg-ff3e said the row is, and why `D3` had to bend the *code*. It is
recorded here with a number because "measured rather than claimed" is doing a lot of work in the
repair's prose, and what is measured is a property of `partition`, not of the documents.

---

## The floor item: the blessing path

*One thing no list in the assignment names.* I chose **`--reseal`** — by mg-ff3e's own description,
*"the only step in this instrument that can make a wrong document green"*. `B0`: **0 invocations
anywhere under `code/`.** It is named in four places and executed in none. A control that has never
been run is a sentence.

| probe | | exit | predicted |
|---|---|---|---|
| `B1` | a live figure corrupted, then `--reseal` | **1 — REFUSED**, record sha256 unchanged | 1 ✓ |
| `B4` | the refusal deleted (one statement), same corruption | **0 — blesses a wrong document** | 0 ✓ |
| `B2` | `partition` bent lossy (D3's shape), then `--reseal` | **0 — BLESSED** | 1 ✗ |
| `B6a` | a label exchange outside the seven probe literals | **1**, `SITE RECORD @ H8` refuted | 1 ✓ |
| `B6b/c` | `--reseal`, then the runner again | **0 / 0, 0 refuted** | 0 / 0 ✓ |

`B1` and `B4` together are the good news: the refusal exists, it works on a wrong figure, and it is
load-bearing at its finest unit — delete the one statement and a wrong document gets blessed.

### Finding E-5 — the refusal is holed at the three rows that license the whole claim

`reseal()` refuses while any gate row *other than* `SITE RECORD` is refuted, and it identifies those
rows like this:

```python
blocking = [d for ok, d in figure_gate(texts, measured)
            if not ok and "SITE RECORD" not in d]
```

A **substring test over the whole row**. The `RECORD PARTITION` row's own explanation says
*"…everything else by `SITE RECORD`, and nothing is in neither"* — so it matches, and it is
excluded. Measured: **of 34 gate rows, 6 are excluded; 3 are the `SITE RECORD` rows, which is
intended, and 3 are the `RECORD PARTITION` rows, which is not.** With `partition` bent lossy,
`--reseal` exits **0** and writes a declared record built from a partition that is not the section.

This is **R5 item 3, verbatim**. mg-ff3e found exactly this defect in its own scoring code —
*"`\"FIGURE CENSUS\" in row` matched the `SITE RECORD` row's own explanation, which names the other
rows"* — fixed it there with `heading()`, and kept it in its `PREDICTIONS.md` as a defect of its
own. What it did not do is ask the question its parent ticket exists to enforce: *where else does
this shape live?* It lived forty lines away, in the file being repaired, guarding the blessing
path. **The fix is the same one line: key on the row's heading.**

### Findings E-3 and E-6 — after a reseal, what is protected is what was named

`--reseal` refuses on a wrong **figure** and, by construction, **cannot** refuse on a wrong
**label**: `SITE RECORD` is excluded from the refusal, and `SITE RECORD` is the only row a label
exchange moves. That is the design, and this audit does not dispute the design — the alternative
to a blessing path is a freeze. What it disputes is that the narrowing was never measured.

Measured now, in two steps:

- `B3` blesses `X3`'s label exchange. All 34 gate rows go green. The runner still exits 1 — but
  **not** because a gate row caught it. `N21` locates its text by content, its literal has moved,
  and it reports `PROBE NOT APPLIED`, so the negative control's aggregate reads *6 of 7*. The
  runner noticed **its own probe**, not the document. *(I predicted exit 0 here; the miss is kept,
  and it is what produced `B6`.)*
- `B6` uses a label exchange **outside** those seven frozen literals and read by no designated
  reader: H8's first code block is made to assert that the deliverable's §14 copy is both
  `10 623 chars (unchanged)` and `2 928 → 6 069 chars (more than doubled)`. The runner catches it
  (exit 1, `SITE RECORD @ H8` refuted — **the repair works**). One `--reseal`. Then **exit 0, 0
  refuted rows**, with the contradiction on the page.

So the residual protection after a blessing is exactly the **seven strings the enumeration named**,
and only as a side effect of how those probes locate their text. Same shape as E-1 and E-4, one
level up.

---

## Findings, ranked

| id | finding | evidence |
|---|---|---|
| **E-5** | `reseal`'s refusal excludes the 3 `RECORD PARTITION` rows by a substring test over the whole row. A lossy partition is blessed at exit 0. **This is R5 item 3 live in the artifact it was repairing** | `A7-B2`, `A7-B2b` |
| **E-1** | the field it does not reach is the **site boundary**: mg-9207's `E3` kind, at the `STATE.md` site, is exit 0 with 0 refuted, while the same kind inside a site is exit 1 | `A5-X1`, `A5-X2`, `A5-X3` |
| **E-6** | one `--reseal` turns a real label exchange **fully green** — exit 0, 0 refuted — outside the seven enumerated literals | `A7-B6` |
| **E-4** | the same-kind enumeration is over **kinds, not sites × kinds**, and did not demonstrably precede the fix (0 of 7 before `c7f9079`) | `A8` |
| **E-2** | *"a site is a SECTION"* is false at 1 of 3 sites; 88.2% of the three files is outside every record | `A6` |
| **E-3** | the blessing path is the whole of (e)'s strength and had **no control anywhere in the arc** before this audit | `A7-B0`–`B4` |

## What this audit does not do

- **It does not repair E-5.** It is one line. An audit that fixes its own findings has no
  independent check left; the repair belongs to a follow-up ticket, with a control that shows the
  refusal blocking a lossy partition.
- **It does not re-open the figure case.** A3 and A5b confirm it at a larger population than the
  result they are checking.
- **It does not touch `J-1`/`J-2`/`J-3`.** `B3`'s post-reseal exit 1 is adjacent to `J-3` and is
  reported, not repaired.
- **`A1`, `A2`, `A3` and `A4` are fixtures in memory, declared as such.** `A5`, `A5b` and `A7` run
  on disk against the real runner with no environment variable set, and they are the evidence.
- **0 mathematical statements are touched.**
