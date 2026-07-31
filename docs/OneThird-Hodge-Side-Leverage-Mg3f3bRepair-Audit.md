# Independent audit of the mg-3f3b `n/a`-and-vocabulary repair

**Object.** mg-3f3b's repair of mg-7e39's four findings — landed at `4785086`, completed through
`75333b2`. Instrument: `code/hodge_leverage_audit_97fb/`, `sh run_all.sh`, ~5 min, **no shared
code with the artifact**. Transcript: `code/hodge_leverage_audit_97fb/out_audit_97fb.txt`.
Predictions, committed before any script of this instrument existed: `PREDICTIONS.md` at `5309132`.

The mathematics is not re-opened. What is measured is the documentary layer: four repairs, each of
which is a claim a deliverable makes about itself.

---

## The four repairs stand

| mg-7e39's finding | mg-3f3b's repair | this audit |
|---|---|---|
| **F1** `K11 @ the STATE.md row` is `n/a` for a fact about the derivation | `k_layout` shifts alignment in **either table format**; every `n/a` reason restated to carry a count | **HOLDS.** The cell now reads `FIRES (rec)`, and it fires under an independent mutation of mine as well |
| **F3** 1 of 6 touched | the construct repaired at every occurrence, `DISPOSITIONS` **empty** | **HOLDS at the numerator.** 0 live at `4785086` and 0 at HEAD, counted by my rule over my vocabulary. The denominator is a finding — G4 |
| **F5** the sweep's vocabulary is a hand list of five | the gate **declares** `ROW_KINDS`; `ROW_NAMES` reads it **by AST** | **HOLDS.** Derived, not copied, and the fail-closed rule can be made to fail |
| **F2** the sweep's published `.py` population was wrong at the commit that published it | the count re-derived from `git ls-tree` at a named commit | **HOLDS as a mechanism, FAILS as a state at HEAD** — G5 |

And the primary target of the brief:

> **Every `n/a` the repair produces, read as a claim, with the case it says is impossible
> constructed: 7 of 7 SURVIVE.**

Each of the seven is a fact about its site, not about the derivation, and each carries a count a
reader can check at the site without reading the gate. The matrix went from **8 `n/a` to 7 by
covering a cell, not by dropping one**: exactly one cell moved out of `n/a`, none moved in, and none
became `SILENT`. The cell that moved was re-fired here by a mutation written from the kind title —
and it fires at `803bd50` too, which locates mg-7e39's F1 precisely: **a defect of the instrument
that reports coverage, not of the gate that provides it.**

---

## G5 — the F2 repair is F2 at HEAD, and its own transcript says otherwise

The repair's rule is that a **transcript** is recomputed by the publication step while **prose**
must point at one, because prose has no publication step. `S4a` checks each transcript against the
tree **at its own publishing commit** and records `0 disagree of 2`.

Re-checked here at HEAD:

| transcript | publishes | tree at its publishing commit |
|---|---|---|
| `code/hodge_leverage_repair_6df0/out_repair_6df0.txt` | 473 | `3958b5a` — **481** |
| `code/hodge_leverage_repair_3f3b/out_repair_3f3b.txt` | 473 | `75333b2` — **481** |

**Both were right when written.** The commits they were written against — `c1a57fd` and `3d7b32f` —
hold exactly the count each transcript states, and the `C2d` rows of `out_audit_97fb.txt` carry both
numbers. The **merge rebased** the commits onto a tree that had grown, and `publishing_commit()` is
`git log -1`, so the commit that publishes each figure is no longer the commit it was measured at.

(This paragraph deliberately **points at the transcript** rather than restating the population, which
is the repair's own rule for prose. Restating it here would have made this report the tenth file in
the population my own `C2b` counts, and my own transcript stale about it — which is the shape of
everything above.)

This is not the failure F2 named. F2 was *wrong when written*. This is the complementary one, and
the repair's own vocabulary has no word for it: the "publication step" it means is **the run**, and
the step that broke this is **the merge**. Nothing re-runs the check after one.

The fix is a choice about what "publishes" means — regenerate the two transcripts at the commit that
now publishes them, or stop keying the check on `git log -1` — and it belongs to whoever lands it.

---

## G4 — the reconciliation: neither six is the population

mg-7e39 reports **6 existed, 1 touched, 5 live**. mg-3f3b's landing commit reports **0 of 6**. The
brief's instruction was to count rather than adopt the later figure. Counted here, over every `.py`
file under `code/` in the tree at each commit, by an AST rule that accepts `in` **and `not in`** and
excludes comparators bound to a heading function's output:

| commit | | live occurrences | population swept |
|---|---|---|---|
| `803bd50` | mg-6df0's parent | **7** | 448 `.py` |
| `77306a7` | mg-6df0 landed | **6** | 448 `.py` |
| `979df72` | mg-3f3b's probe commit | **6** | 481 `.py` |
| `4785086` | mg-3f3b's repair landed | **0** | 481 `.py` |
| HEAD | | **0** | 487 `.py` |

So: **7 existed, mg-6df0 touched 1, 6 were live; mg-3f3b touched 6 of 6, 0 remain.**

The two sixes are **not the same six**.

- mg-7e39's six is `1 touched + 5 live` at `803bd50`. It contains
  `verify_landing.py:1815` — already repaired — and is missing
  `audit_a318_repair.py:327`, a `WRITTEN ONCE` occurrence that its vocabulary, regexed out of the
  gate's `print` calls, could not see. It is **short by one**.
- mg-3f3b's six is exactly the set that was **live when it started**, which is correct for that
  question and is a *different set* of the same size.

Both numerators hold. **The population that EXISTED is 7, and neither party's six names it.**

The `not in` half matters: `reseal`'s refusal read `"SITE RECORD" not in d`, and that is the one
occurrence mg-6df0 repaired. A rule that only saw `in` would have reported that repair as touching
nothing — which is what this audit's first run did.

### The four that select 6 gate rows where 3 were meant

Of the six occurrences live at `77306a7`, **four** select 6 of the gate's 34 rows by substring where
the heading test selects 3. The three extras are the same three every time, and they are named
individually in the transcript rather than counted:

    RECORD PARTITION @ the STATE.md row
    RECORD PARTITION @ §14
    RECORD PARTITION @ H8

— the rows whose own explanation *names* the row being searched for. The other two occurrences
(`READ AT THE SITE` at 12 of 34, `WRITTEN ONCE` at 10 of 34) select the same rows under both tests
and are the construct anyway.

### Derived against hand, as a count of occurrences rather than a set diff

"The vocabulary is two names short" is a fact about a list. This is the fact about the tree:

| commit | by the gate's **declaration** (7 names) | by mg-6df0's **hand list** (5 names) |
|---|---|---|
| `803bd50` | **7** | **5** |
| `77306a7` | **6** | **4** |

Both occurrences the hand list cannot see are in the same file —
`audit_a318_repair.py:326` (`READ AT THE SITE`) and `:327` (`WRITTEN ONCE`), adjacent lines. mg-7e39
measured this gap as **5 against 4** with a vocabulary regexed out of the gate's `print` calls; the
declaration sees more than either, and the two extra names buy exactly two occurrences at both
commits.

---

## G2 — the F2 repair's own population is a hand list

`COMPUTED` names **2** transcripts and `PROSE` names **4** prose files. Sweeping the tree with the
repair's **own** `POP_FIGURE` rule finds **9** files that publish a `.py` population; **5** are in
neither list.

That is F5's defect — a scope nobody chose — landed on F2's axis by the deliverable that landed F5
on the vocabulary axis one section earlier.

**And extending the list would not simply widen the check.** `POP_FIGURE` takes the *first* match in
a file and applies no quotation exemption, so `code/hodge_leverage_audit_7e39/out_audit_7e39.txt` —
whose first match is the `429` it is **reporting as the defect** — reads as stale and is not. A
hand-picked list hides two things at once: that the scope is short, and that the rule was never
asked to work outside it.

The `S4b` quotation exemption has the same shape: it is keyed on `"…"` and `“…”`, and this arc
states its corrected figures in **bold**.

---

## G1 — the fail-closed rule that makes an `n/a` carry a count is `\d`

The repair's answer to F1 is that a decline reason with no measurement in it is RED:

```python
countless = [(t, n, w) for t, n, w in reasons if not re.search(r"\d", w)]
```

Any digit, anywhere in the sentence. A ticket id is digits.

Run over the **eight** reasons the pre-repair matrix printed at `979df72` — every one of them a
sentence with no measurement in it, which is why they were repaired — the rule blocks 6 and
**passes 2**, and both pass on the digits inside `mg-ec07`:

> *"fewer than two table rows carrying figures INSIDE this site (the ledger's other rows are outside
> it — mg-ec07's X2, declared open)"*

Demonstrated at HEAD, where the rule is live: one measurement-free decline reason, written twice and
differing by the twelve characters `(mg-9207 E3)`. **Without** the id the gate flags it and exits 1.
**With** it, the gate does not flag it and exits 0. Same sentence, same absence of any measurement,
opposite verdicts.

The repair's own comment says there is no mechanical test for *"is this sentence about the site"* and
that there is one for *"does this sentence contain a number measured at the site"*. There is not. The
test it has is *"does this sentence contain a digit"*, and that is a weaker thing.

---

## G3 — the matrix's own census is a substring test over a whole row

`repair_ec07.py`'s `R3a` censuses the matrix with

```python
fires  = sum(l.count("FIRES")  for l in cells)
na     = sum(l.count("n/a")    for l in cells)
silent = sum(l.count("SILENT") for l in cells)
```

over a printed line whose **first 62 columns are the kind title**. It is a substring test over a
whole row — the construct this entire arc repairs — in the census of the very matrix whose `n/a`
cells are mg-7e39's F1. It is outside the sweep's reach by construction: the sweep's vocabulary is
**gate row names**, and these are **cell values**.

At HEAD the two censuses agree at `29 / 0 / 7`, because no kind title happens to contain any of the
three words. Agreement is why nobody has met it, not evidence that it is sound. One kind title edited
to contain the literal `n/a`, **with no cell of the matrix changing**, moves the substring census
from 7 to 8 while the census by column stays at 7.

A census that counted its own *legend* is the first version of that row, recorded in
`repair_ec07.py` as a defect and fixed. A census that counts its own row *titles* is the version
that replaced it.

---

## What must not be disturbed

| | |
|---|---|
| the product | **29 of 29** applicable cells of the 36-cell matrix FIRE, **0 SILENT**, scored by running the artifact as a **subprocess** and reading gate rows out of its stdout |
| the site sentences | cutters written from the **disclosure sentences** in `EXTENT_OF`, not from `framed_row`/`section`, reproduce the gate's three sites at **3 of 3** on line count and character count. That is the test of whether a scope sentence is a specification or a label |
| the refusal | `partition` bent lossy **at one site at a time**, then `--reseal`: **3 of 3 REFUSE with the record sha unchanged** at HEAD, and **3 of 3 BLESS with the record rewritten** at `803bd50`, where the defect is still present |
| the vocabulary | declared **7**, printed **6**, hand-listed **5**; `CENSUS ROSTER` declared and never printed; **0** printed kinds undeclared. One name removed from `ROW_KINDS` makes the gate exit 1 with the declared-vocabulary row refuted |
| the historical fact | the transcript committed at `77306a7` publishes **429**; the tree there holds **448**, and so did its parent. Re-derived from `git ls-tree` here, not quoted |

---

## Two defects of this instrument, kept as written

**A sweep rule that cannot tell a set of headings from a whole row manufactures findings.** The first
version reported `"FIGURE ORDER" in bad` in `audit_ec07.py` as the construct — but `bad` is a set of
*headings*, so that membership test is the remedy spelled as a set lookup. The fix was itself short,
reporting `"CENSUS ROSTER" not in moved` where `moved` is a *vocabulary*. A rule that widens a
population by one and a vocabulary that narrows one by one are the same mistake, and this audit made
the first while measuring the second.

**The site's own length is one of the live figures.** `cell` is `len(state_row(...))`, so any
mutation that changes the STATE.md row's byte count moves a figure at all three sites. The first
`K11` construction here inserted one space and got exit 1 with six FIGURE rows refuted — a K01
wearing K11's name. It now *moves* a space instead: one cell gains the padding another loses, length
identical, figure-token multiset identical.

Both are in `PREDICTIONS.md` and in the transcript.

---

## Standing

- **17 of 17** on-disk probes restored their file **byte-identically**; a single False makes the run
  red. A probe that rewrites the artifact while auditing it is the failure mg-3f3b named for itself,
  and asserting the restore is not the same as checking it.
- Every exit code was predicted before the run. The misses — the two above, and `6 of 6` predicted
  where `6 of 6` was right for a reason I had wrong — are kept as written.
- Every number here names its population. There are no bare totals.
