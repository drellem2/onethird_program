# The mg-8aae repair — the census is position-aware, and `SUMMARY vs ROWS` reads the sentence it prints

**Work item mg-8eca. Landing mg-8aae's two open findings, H-1 and H-2.**
**Instrument: `code/hodge_leverage_repair_8eca/`, `run_all.sh`, ~5 min. Committed transcript:
`out_repair_8eca.txt`. Predicted exit code, written before the first run: 0. Observed: 0.
23 checks, 0 refuted.**

---

## What was wrong, in one sentence each

mg-8aae's own closing note is the right frame and this repair is built on it:

> **Both open items are the same two questions in different clothes** — is the measured property
> invariant under the guarded failure (a multiset is invariant under exchange; `x == x` is
> invariant under everything), and is the demonstration at the right target (the hook versus the
> check). **Neither is a coverage problem, and neither is fixed by checking more things.**

| | |
|---|---|
| **H-1** | The figure census compared a **MULTISET**. A transposition preserves a multiset exactly, so exchanging two *declared* figures of equal length in ordinary prose left every check satisfied and the runner at **exit 0 at 2 of 2** sites — while H8's own table said the `STATE.md` row **shrank** across mg-a2bd and the chain F-1 was born in ran backwards. |
| **H-2** | `SUMMARY vs ROWS` scored `printed == derived` where `printed = FORCE_SUMMARY or derived`. With the hook unset it was **`x == x`** and could not fail for any tree. It had been *demonstrated firing* — through the hook built to make it fire. |

**0 mathematical statements are touched here, and no finding of mg-835f, mg-8a5c, mg-8916 or
mg-8aae is re-marked.** What mg-8aae confirmed is not re-opened: the 12 of 12 at row granularity
and G-1 closed against wording that audit chose both stand, and R3 re-measures them by re-running
its instrument rather than quoting it.

---

## 1. H-1 — the roster is now an ordered list of slots

The census asked *is every figure a reader meets licensed?* That is a multiset question and the
multiset answered it. It could not ask *is each licensed figure attached to the statement it
belongs to?*, and that is the question a transposition asks.

**The repair changes what is measured.** `LIVE_CENSUS` and the counted `HISTORICAL` roster are
replaced by a single declaration, `ORDER`: the figure tokens each site is licensed to carry, **in
the order a reader meets them**, with `@gap`/`@cell`/`@copy`/`@hist`/`@both` standing for the live
figures at the values measured this run.

- the **multiset** the licensing check compares is **derived from `ORDER`**, and so is
  `LIVE_CENSUS`, so the two cannot drift apart. There is one declaration of multiplicity, not two;
- `HISTORICAL` keeps only **what each token is** — the count is `ORDER`'s, counted. A roster that
  says "twice" and a document that writes it three times can no longer both be satisfied by
  editing one of them;
- `census_gate` records a **`FIGURE ORDER`** row per site beside its licensing row, reporting the
  first occurrence at which the section and the roster diverge;
- the roster is fail-closed in a second way now: an existing figure fires until its slot is moved
  to where a reader meets it.

### It is measured on disk, in both positional senses

Four exchanges, each **asserted to be a permutation and nothing else before it is written** —
identical multiset, identical designated reads, identical length. A probe that also moved the bag
would be re-measuring the census that already existed.

| probe | predicted | observed | restored |
|---|---|---|---|
| **H8**, mg-8aae's own: `before mg-a2bd : 13 551` ↔ `after mg-a2bd : 16 692` | GATE FIRES | **GATE FIRES** | green |
| **H8**, the other sense: the row-history line's `10 483` ↔ `16 268` | GATE FIRES | **GATE FIRES** | green |
| **the STATE.md row**, mg-8aae's own: the chain's last two terms, `−875` ↔ `+755` | GATE FIRES | **GATE FIRES** | green |
| **the STATE.md row**, the other sense: the chain's first two terms, `2 928` ↔ `6 069` | GATE FIRES | **GATE FIRES** | green |

**4 of 4 fire; 4 of 4 restorations return the runner to exit 0, sha256-verified.**

And the requirement is stricter than "the run goes red", because a widening that made the run red
for a *new* reason while the positional check stayed quiet would keep the headline and lose the
result: **at 4 of 4, the row that failed is the `FIGURE ORDER` row FOR THAT SITE, and it is the
only row that failed.**

A transposition is its own inverse, so "both orderings" of one pair is one text. What is done
instead is two **disjoint** pairs per site, exchanged in opposite positional senses — an earlier
pair of the chain as well as its last two; a later-column value moved earlier as well as an
earlier one moved later — so the demonstration is not one accident per site.

The in-memory battery inside the runner grows from **14 mutations to 18**, N15–N18 being the four
exchanges, and **18 of 18 move the gate as predicted**. N1–N14 are unchanged and still fire.

---

## 2. H-2 — the check reads the sentence it prints

The two lines mg-8aae quoted:

```python
printed = FORCE_SUMMARY or derived
record(printed == derived, ...)
```

With the hook unset, `printed` **is** `derived`. It was not a comparison of the printed verdict
against the rows; it was a comparison of the rows' verdict with itself.

**The repair makes the two sides independently obtained.** One is **read out of the lines the run
will print**, by parsing the sentence a reader reads — exactly as the figure gate in
`verify_landing.py` reads each figure out of the statement that asserts it. The other is
**recomputed from the rows**. Two things are read back, not one: the **verdict word** and the
**`N of M` count**, each compared against a value recomputed from the rows.

A headline saying anything other than one of the three verdicts reads back as `UNREADABLE` and
therefore disagrees — fail-closed, because a bottom line a checker cannot parse is a bottom line
nothing is checking.

### And it is demonstrated on the REAL artifact, not on the hook

| | direction | `SUMMARY vs ROWS` | refuted |
|---|---|---|---|
| **D0** | the artifact as it stands | `[CONFIRMED]` | 3 |
| **D1** | `MG8916_FORCE_SUMMARY=CONFIRMED` — mg-8916's hook, **kept** | `[REFUTED]` | 3 → **4** |
| **D2** | **the REFUTED branch's headline edited by hand ON DISK, no environment variable** | **`[REFUTED]`** | 3 → **4** |
| **D3** | the **count** edited, the verdict word left correct | `[REFUTED]` | 3 → **4** |
| **D4** | **the defect reinstated**, with D2's edit still applied | `[CONFIRMED]` | back to **3** |

**D2 is mg-8aae's own direction-2 mutation, verbatim** — the one the old check passed at
`[CONFIRMED]` with the count unmoved. It reproduces G-2's exact artifact (*"THE PRIMARY TARGET IS
CONFIRMED"* printed above its own refuted `PRIMARY` rows) with no environment variable set, and
now the check catches it and moves the count by exactly one.

**D1 is kept deliberately.** Nothing mg-8916 demonstrated is silently dropped; `FORCE_SUMMARY`
still exists and still reaches the *sentence*, which is why it still fires. What changed is that
it no longer reaches the *check's own left-hand side*, so it is no longer what the claim rests on.

**D4 is the control that makes D2 mean anything.** Reinstating the two removed lines under D2's
edit makes the same artifact go uncaught again. Without it, *"the check fires"* and *"the
instrument fires"* are the same sentence — which is the distinction mg-8aae's whole finding turns
on, applied here to this repair rather than asserted about the last one.

**D3 is the deletion test for the second read.** With the verdict word left correct and only the
parenthetical count moved, the check still fires: the count is load-bearing on its own, not
decoration on the verdict.

---

## 3. Scored by the instrument that raised the findings, not by this one

A repair scored only by its author's instrument is scored by its author. So **mg-8aae's
`audit_8916_repair.py` is re-run here, unmodified**, and its committed transcript is
sha256-checked afterwards.

| | |
|---|---|
| its A4 permutation rows | **2 of 2 read `GATE FIRES`** where it observed exit 0 at 2 of 2 |
| its findings | **0** — neither H-1 nor H-2 is raised by the instrument that raised them |
| `out_audit_8916.txt` | **sha256-identical afterwards** — the run as *taken* is not overwritten to agree with this repair |

Its **predictions are left as written** and now read `PREDICTION MISSED`. That is the correct
record of a finding that has been landed: from the raising instrument's side, a landed finding is
a missed prediction.

And **mg-8916's own `repair_835f.py`, likewise unmodified**, still reports **18 checks, 0 refuted,
exit 0** against the repaired tree — measured here by re-running it, not quoted from its
transcript.

### One seam, declared rather than left to be found

`out_repair_8916.txt` is **left as taken** and is not regenerated, and the reason is a real seam
rather than an aesthetic preference. mg-8aae's **A7** checks mg-8916's document against mg-8916's
transcript by looking for an **echo of the mg-8a5c check's message text** — and that message text
is one of the two things this repair changed. Regenerating that transcript would therefore make
A7 fail on a needle that no longer exists, silently, in an instrument nobody edited.

So the transcript stays what it is: the run mg-8916 made, at the tree it made it on. This is
checked (sha256-identical after this run, and the needle still present) and **stated**, and
anyone who does regenerate it must move A7's needle in the same commit.

---

## 4. This repair's own first run refuted two rows, and both were its own

Kept in `PREDICTIONS.md` rather than tidied away, because they are the same shape as the findings
being landed:

- the edit to the runner's **printed-extent line** broke **mg-8aae's A1**, which re-counts that
  extent by *parsing* the line. An instrument that raised a finding must be able to re-run
  **unmodified** against the repair that answers it. The line keeps its exact shape and the slot
  count went to a line of its own, with a comment at the site saying why;
- the **mechanism check** — *"`printed = FORCE_SUMMARY or derived` is gone"* — read the string in
  the repaired file's own ⚠️ block *recording its removal*. A check that cannot tell the defect
  from the note about removing it goes red on an honest repair. It is now anchored to the code
  line, indentation and all.

Both are one error in miniature: **a check whose measured property does not line up with the
failure it is supposed to see.** Neither would have been fixed by checking more things.

---

## 5. What is NOT covered, printed rather than left for the next audit

An extent that is not printed becomes the next claim wider than its code — which is what both of
mg-8aae's findings were, one generation apart. So R4 prints it, and the runner prints the
positional exclusion at the gate itself.

**The census**, after this repair, covers every figure-shaped token the section asserts, at the
value it should have **and in the slot a reader meets it in**. It does **not** cover:

- **two occurrences of the SAME token exchanged with each other.** This is not an omission that
  can be closed: the sequence is over *values*, and exchanging equal values is the identity map on
  the artifact as well as on the measurement. There is nothing there to see. **Position is
  covered; identity of equal figures is not, and cannot be.**
- a token outside the section, inside a marked quotation, or not of the figure-shaped class —
  unchanged from mg-8916, and unchanged deliberately.
- **what a figure MEANS.** The roster says `10 483` is *"this file at bbe83b5^"*; nothing checks
  that sentence against git. A roster entry whose prose is wrong is invisible here.

**`SUMMARY vs ROWS`**, after this repair, compares the printed verdict **and its count** against
the rows, both sides obtained independently. It does **not** cover:

- the **rest of the branch text**, which is still hand-written prose asserting things the rows do
  not carry (*"the repair's three figures are the POST-commit ones and reproduce exactly from the
  tree"*). The verdict sentence is checked; the paragraph around it is not. mg-8aae named this
  and it is named again here rather than quietly counted as closed.
- any row not tagged `PRIMARY`.

---

## 6. The rule applied to this deliverable's own summary

*"If this deliverable's own summary disagrees with its own rows, believe the rows and report the
summary as the defect."*

This instrument lands H-2, whose content is that a summary-versus-rows check comparing a value
with itself is not a check. So **its own bottom line is derived from its rows** — tagged `H-1` and
`H-2` — and the agreement is scored by **reading the verdict and the count back out of the lines
about to be printed**: the same repair, applied here, rather than asserted about somebody else's
file. The closing prose for each finding is reachable **only down the CLOSED branch**; an OPEN
verdict prints the rows that did not hold instead of the sentence they were supposed to license.

| the document's header | `out_repair_8eca.txt` |
|---|---|
| 23 checks | **23 checks recorded** |
| 0 refuted | **0 refuted** |
| predicted exit 0, observed 0 | consistent |

---

## Files

| | |
|---|---|
| `code/hodge_leverage_repair_8eca/` | this repair's instrument, R1–R4, `run_all.sh`, ~4 min |
| `code/hodge_leverage_landing_e1d0/verify_landing.py` | **the census**, now positional: `ORDER`, `expected_sequence`, the `FIGURE ORDER` row, and N15–N18 |
| `code/hodge_leverage_audit_8a5c/audit_repair_8e30.py` | **`SUMMARY vs ROWS`**, now reading the printed sentence: `printed_summary_verdict`, `printed_summary_count` |
| `code/hodge_leverage_audit_8aae/` | mg-8aae's instrument and transcript — **untouched**, and re-run here |
| `code/hodge_leverage_repair_8916/` | mg-8916's instrument — **untouched**, and re-run here |
