# Independent audit of mg-2da3 / `bf17716` — the working-tree control for `b68db5d`'s delta

**mg-2216**, 2026-07-30. Pre-filed at the same time as the ticket it audits, and deliberately
so: mg-2da3's whole deliverable is an **instrument**, and an instrument whose only evidence
of sensitivity is the negative control its own author wrote is the defect being repaired,
one level up.

Reproduce: `sh code/state_control_audit_2216/run_all.sh` (~11 s; `out_mutations.txt` and
`out_claims.txt` committed, both reproduce byte-identically at this commit).

---

## VERDICT — OVERSTATED with 2 BROKEN

**The repair's central move is right and is confirmed here independently.** The pinned
battery was not touched, its historical reproduction still works byte-identically, the new
instrument really does read the working tree, it really can fail, and **all three record
corrections are TRUE** — I re-derived each of them from the sources rather than reading the
commit's arithmetic. **Both of its caveats are true too**, which matters because a caveat
reads as rigour and is almost never audited: I checked them as claims and they hold. And for
the **second time in this arc**, there is **zero material beyond the brief** — every one of
the six changed files maps onto one of the ticket's four numbered items.

**What is BROKEN is the coverage of the new control, in both halves, and it is broken in
exactly the shape the ticket predicted**: `negative_control.py` mutates precisely the things
`delta_control.py` tests, so it establishes sensitivity to its author's four mutations and
nothing wider. I built **fourteen mutations of my own**, none of them mg-2da3's, chosen to be
*small* where mg-2da3's are large. **Eight of them pass silently**, including the destruction
of 1,556 characters of a certified correction block and the replacement of 38% of the
certified ledger cell with the letter `x`.

**"Nothing was lost" is not re-opened here and stands.** The repair states it correctly,
does not re-verify it, and says in the right words that a blind certification of a one-line
edit is a **control** defect and not a content defect. That framing is correct and I have
nothing to add to it.

| | |
|---|---|
| **B1** | The README half of the certified delta is **five substrings**, and the author's NC3 deletes exactly the line one of them tests. Hollow the F1 correction block — keep its header, delete its 1,556-character body — and the control exits **0**. |
| **B2** | The `STATE.md` half is a **length-and-substring** control. Every length-preserving mutation of the certified cell passes: one character, a five-character inversion of the row's verdict on its own proof, a whitespace-only substitution, a token-multiset-preserving reorder, and 3,000 junk characters. |
| **MINOR 1** | The correction is not findable **from the point of use**. Nothing in `code/state_audit_6a2f/` warns a future re-runner, and the per-row history of the row `b68db5d` edited names neither the correction nor the new control. |
| **MINOR 2** | `~25 s` for its own battery, stated twice. Measured **3.31 / 3.32 / 3.41 s**. The two statements of *what* those seconds are contradict each other at 25 s and agree at 3.3 s. |
| **MINOR 3** | *"THE CONVENTION, so this cannot recur silently"* — Appendix A's four clauses are documentation. Nothing greps. |
| **MINOR 4** | The **one-grep test** the convention promotes is asked of a *directory*. **Seven directories under `code/` are mixed**, including `state_landing_audit_bd41/` — the very audit this repair is landing. |

---

## What I did NOT do

**I did not re-run `negative_control.py` and call the instrument verified.** That is this
arc's recurring failure and it is why mg-56be's refutation counted. I read it, so that I
could deliberately avoid its four mutations, and then built my own battery from the file
format and from git — its table parser included, so that a parsing defect could not be
shared between the instrument and its audit. `code/state_control_audit_2216/` imports
nothing from `code/state_landing_control_2da3/`, `code/state_audit_6a2f/`,
`code/state_restructure_34bf/` or `code/state_landing_audit_bd41/`.

---

## CONFIRMED — the things the repair got right, re-derived here

### The pinned battery's original purpose is intact — the ticket's second target

This is the axis on which a repair of this shape most easily trades one defect for another,
and it did not.

- `git diff --name-only bf17716^..bf17716 -- code/state_audit_6a2f` is **empty**. Not one
  byte.
- The battery still reproduces `out_audit.txt` **byte-identically at this commit**:
  **96,291 bytes produced, 96,291 committed, exit 0**. The historical reproduction of
  mg-6a2f's audit of `57f962f` works exactly as before.
- The commit's load-bearing claim about it — *"not one of them opens the working tree or
  resolves `HEAD`"* — **holds**: a grep for `open(` or `HEAD` over all seven scripts in the
  directory returns nothing. (`run_all.sh` calls `git rev-parse --show-toplevel`, which
  neither opens the tree nor resolves `HEAD`; the claim survives its own test.)
- The repair touched **six files** and none of them is an existing instrument.

### The new instrument really reads the tree, and really can fail

Six of my fourteen mutations came out the way the design says they should, and I count that
as confirmation rather than as a null result:

| | mutation | exit | |
|---|---|---|---|
| M14 | the certified row duplicated, so its key no longer identifies one row | **1** | CAUGHT — `[FAIL] exactly one ledger row keys to mg-276d` |
| M07 | the row's pointer to its own per-row history deleted (−158 chars) | **2** | CAUGHT — the MOVED path |
| M12 | 60 lines inserted above the certified row | 0 | tolerated, and the design says so |
| M13 | the certified row moved to the end of the file, byte-identical | 0 | tolerated |
| M04 | 40 trailing spaces inside the raw field, outside the stripped cell | 0 | tolerated |
| M08 | a different >2,000-character ledger row deleted outright | 0 | tolerated — out of the delta |

**The key-based design claim is confirmed independently.** M12 and M13 are the strongest form
of the author's stated goal — *"it survives legitimate later commits inserting lines above the
row"* — and it survives not just insertion but relocation of the row to the end of the file.
A line-anchored check would have failed both.

### All three record corrections are TRUE

Each re-derived from the source, not read off the commit:

- **A3 — the ancestry.** `git log --format=%p` gives `57f962f <- 97cb533 <- 60f4dac`.
  `60f4dac` **is** mg-34bf's parent's parent, and *"two commits before mg-34bf's parent"*
  was off by one. The correction is right, and it is right to say the attribution it sits
  inside is undisturbed.
- **A2 — the over-claim.** mg-6a2f's document at **`:212`** reads
  *"| pm-onethird's ticket (a stale revision, line bytes) | 5.4 / 9.2 / 13.5 / 10.8 / 11.7 |"*.
  It **did** name the source. And the genuinely new part is genuinely new: `db08b4c:STATE.md`
  is **327 lines** with **0** occurrences of `mg-a3d4`.
- **A1 — the blind certification.** Confirmed a second time, and **under a mutation that is
  not mg-bd41's**: with the last 3,000 characters of row `:135`'s cell replaced by `x`
  (M06), the pinned battery still emits its **96,291 bytes**. mg-bd41 gutted the file;
  I damaged one cell surgically; same verdict. The finding does not depend on the size of
  the mutation. The plain statement the ticket asks for is present and correctly worded:
  *"that re-run is evidence about `57f962f`. It is not, and cannot be, evidence about
  `b68db5d`."*

### Both caveats hold — audited as claims, not accepted as fairness

A caveat reads as rigour and is almost never audited. These two are load-bearing, so:

- *"`b68db5d`'s SECOND cited re-run IS genuine."* **True.**
  `code/state_restructure_34bf/verify_relocation.py:95` is
  `new = open("STATE.md", encoding="utf-8").read()` — it does open the working tree — and its
  four cited figures reproduce here exactly: **10 cells / 11,625 words / 125 maximal runs /
  0 unaccounted**.
- *"The `verify_relocation.py` failure is pre-existing, not mine."* **True**, and the
  author's method for settling it was the right one. I settled it a second way that does not
  touch the tree at all: `Appendix A` had already diverged from `57f962f` at **`bdcb006`**,
  two commits before `b68db5d`. The repair's +2 lines cannot have caused a failure that
  already existed.

### The SCOPE arithmetic is true, and the exclusion zone was respected

- `b68db5d`: **380 lines, 62 table rows, 210 cells.** `bf17716`: **382 lines, 62 rows,
  210 cells.** Both as stated.
- Row `:135` in the tree is **byte-for-byte** what `b68db5d` left it.
- **No per-row history file and no ledger row was touched.** The `STATE.md` change is +2
  lines in Appendix A and nothing else.
- `out_control.txt` reproduces **byte-identically** (7,410 bytes).

### Beyond the brief: ZERO — for the second time in the arc

The ticket has four numbered items. Item 1 → `code/state_landing_control_2da3/`. Item 2 →
the A1 block in `docs/state-history/README.md`. Item 3 → the Appendix A paragraph. Item 4 →
the A2 and A3 blocks. Nothing else changed. **The standing target for this arc — seven
consecutive generations with the worst finding in material added beyond the brief — is not
hit here, and both BROKEN items below are squarely inside the brief's item 1.** mg-6a2f was
the first generation to score zero here; this is the second.

---

## BROKEN 1 — the README half of the certified delta is five substrings, and the negative control is shaped around them

**The published claim**, in three places (commit message, `delta_control.py`'s docstring, and
the README's own A1 block):

> certifies `b68db5d`'s actual delta — row `:135`'s F1 repair and **this file's F1 / F2 / B1
> blocks**

**What is actually checked** is section 6 of `delta_control.py`: five `marker in readme_tree`
substring tests. Nothing else. The blocks themselves — several thousand characters of
correction text, which *are* the delta on this side — are uncertified beyond the single line
each marker happens to sit on.

Three of my mutations damage material inside that named scope and the control exits **0**:

| | mutation | Δ characters | exit |
|---|---|---|---|
| **M09** | the **F1 correction block hollowed out**: its first line kept, its entire body deleted | **−1,556** | **0** |
| **M10** | the F2 block's measured figure *"13,188 → 7,703 characters at the landing"* falsified to **9,703** | 0 | **0** |
| **M11** | the figure the repair's **own A1 block** rests on, *"175,552 to **37,958** bytes"*, falsified to **137,958** | +1 | **0** |

**M09 is the finding.** The author's NC3 cuts the F1 block out *including its header line* —
and the header line is the only thing tested. Keep the header, delete the body, and the
control is silent. **That is a control tuned to the mutation its author used, which is the
closed loop this ticket exists to repair, one level up.** It is not a hypothetical: it is
`out_mutations.txt`, M09, exit 0.

**M11 has a second edge.** The falsified figure is the one the repair's own correction uses
as its evidence — *"gutted `STATE.md` from 175,552 to 37,958 bytes"*. The instrument shipped
to defend that correction cannot detect the correction's evidence being changed.

**The fix is small.** Section 6 tests membership; it needs to test the blocks. Bounding each
block (header line to the end of its blockquote, which `negative_control.py` already does in
order to cut one) and hashing the bounded region under the existing `MOVED` discipline would
catch all three, and would age out loudly the first time someone legitimately edits a block.

---

## BROKEN 2 — the `STATE.md` half is a length-and-substring control, and every length-preserving mutation passes

**What section 2–5 of `delta_control.py` actually certifies about the 7,876-character
certified cell:** five substrings present-or-absent, one ordering relation, three exact
character counts (7,703 / 7,876 / +173), one whole-file `**`-parity tally, and one
largest-cell identity. **Character count is the only thing standing between the cell's
content and a green exit.**

| | mutation class | mutation | Δ chars | exit |
|---|---|---|---|---|
| **M01** | single-character | *"every ridge in 1 or **2** facets"* → *"1 or **3**"* — a false statement about the pseudomanifold the row's mathematics rests on | **0** | **0** |
| **M02** | length-preserving | *"the proof is **sound**"* → *"the proof is **bogus**"* — the row's verdict on its own proof, inverted in five characters | **0** | **0** |
| **M03** | whitespace-only | the spaces in `**The mathematics.**` → U+00A0. **No visible character changes at all**; the heading stops rendering | **0** | **0** |
| **M05** | reordering | two adjacent sentences swapped. **Length and whitespace-separated token multiset both preserved exactly** | **0** | **0** |
| **M06** | bulk-but-quiet | the **last 3,000 characters** of the cell replaced by `x`, `**` markers preserved so parity holds. **38% of the certified cell** | **0** | **0** |

**Sizing this honestly, in both directions.** Under the *narrowest* reading of the published
scope — *"row `:135`'s F1 repair (one line, **+173 characters**)"* — M01, M02, M05 and M06
are outside the letter, because none of them touches the F1 sentences. I say that plainly
because the opposite would be the over-reading this arc keeps producing. But two wider
statements are published alongside it and **both are falsified by M06**:

- the ticket's own requirement, item 1: *"A control for that change must read the working
  tree / `HEAD` and **must fail when the file is mutated**."*
- the README's A1 block, in the repair's own words: *"it exits non-zero both when the repair
  is damaged (`1`) and when a measured constant of the landing has moved (`2`) — **never
  green about a delta that is no longer the delta it was written for**."*

**And the repair is already inside the design.** The commit is emphatic that there is
*"no line number and **no frozen-blob comparison** anywhere"*, on the ground that frozen
blobs age out. But the instrument **already freezes three exact constants of that same
cell** — 7,703, 7,876, +173 — and handles their ageing with exit code 2. Freezing the cell's
*content* under the same `MOVED` discipline catches all five misses above and ages out
exactly as loudly. **The design froze the cell's length, which is the weaker of the two
quantities, and rejected freezing its content on a ground its own length constants already
concede.** A `sha256` of the stripped cell, reported as `MOVED`, is roughly four lines.

*(M03 is worth its own sentence: it is the only mutation here with **no visible character
change whatsoever** — an ASCII space becomes U+00A0, the character count is identical, the
byte count is not, and `delta_control.py` **prints** the cell's byte count on every run
without ever checking it.)*

---

## MINOR findings

**MINOR 1 — the correction is not findable from the point of use, and the good pattern was
applied to the least important of the three.**
The ticket asks whether the correction is findable *from the claim it corrects*. The claim is
in a frozen commit message, so the honest test is: where will a future agent meet it?

- `code/state_audit_6a2f/` — the place someone about to re-cite the battery actually stands —
  carries **no note at all**. A grep over all seven scripts for the new control, or for any
  statement of which revision the battery is evidence about, returns nothing.
- `docs/state-history/attempt-mg-276d.md`, the per-row history of the row `b68db5d` edited,
  mentions **neither** mg-2da3 nor the new control — although the repo's own rule 2 is
  *"every correction relocates here, and the row keeps a pointer naming it."*
- By contrast the **A3** correction sits **573 characters** after the bullet it corrects, as
  an adjacent blockquote. That is the right pattern, and it was applied to the *least*
  consequential of the three corrections while A1 — the ticket's headline — got a new section
  at the end of the file with nothing pointing down at it.

The convention itself is followed correctly: the README is where mg-7735 put its own F1/F2
corrections (`git log -S` confirms), and Appendix A already corrects a commit log on the
stated precedent (*"RECORDED HERE BECAUSE NOTHING ELSE CORRECTS A COMMIT LOG"*). **The
placement is conventional; the reachability is not.** The cheap repair is a comment header in
`code/state_audit_6a2f/run_all.sh` naming the revision it is evidence about — the ticket
forbade *repointing* that battery at the working tree, which is right, but it did not forbid
annotating it, and a comment changes no output byte.

**MINOR 2 — the runtime figure.** *"~25 s"*, in the commit message and again at
`run_all.sh:25`. Measured on this box: **3.31 s, 3.32 s, 3.41 s** over three runs; the pinned
battery it runs twice is **1.47 s**. The number is out by ~7.5×, and it makes the commit's
two descriptions of the composition contradict each other: *"two of those seconds are the
pinned battery"* (8% of 25 s) versus `run_all.sh`'s *"most of it"* (>50%). At the true total,
2.9 s of 3.3 s, **both descriptions are right**. One wrong number is doing all the damage.

**MINOR 3 — status language.** *"THE CONVENTION, so this cannot recur silently."* Appendix
A's four clauses are documentation and nothing enforces them; no check greps for a pinned
citation. The convention makes recurrence **detectable by someone who reads Appendix A**,
which is a real improvement and is worth what it is worth — it does not make it impossible.
This is the only place the commit's status language runs hot; everywhere else — *"repair the
certification, not the battery"*, *"a control defect, not a content defect"*, the explicit
naming of what is left open — it is accurate, and the "left open" paragraph naming mg-bd41's
five MINOR findings as deliberately untouched is exactly right.

**MINOR 4 — the one-grep test's granularity.** Appendix A promotes a mechanical test:
*"does any script in **it** open the working tree or resolve `HEAD`?"* The subject is a
directory, and *any* is a disjunction — so one tree-reading script licenses citing the whole
directory's output as evidence about a commit. **Seven directories under `code/` are mixed**,
so this is instantiated rather than theoretical:

```
state_landing_audit_bd41   tree-reading 3, pinned 1 (cellmeasure.py)
state_restructure_34bf     tree-reading 5, pinned 2
unified_gate_audit_446b    tree-reading 3, pinned 4
landscape_audit_d673       tree-reading 1, pinned 6
counterexample_probe_24a3  tree-reading 2, pinned 3
face_geometry_audit_f1b2   tree-reading 1, pinned 4
face_geometry_audit_fcf1   tree-reading 1, pinned 3
```

`state_landing_audit_bd41/` is the audit **this very repair is landing**, and it answers YES
while `cellmeasure.py` remains pinned. The commit itself relies on the finer distinction when
it writes *"`verify_relocation.py`'s **completeness half** opens the working tree"* — the
right unit is the **check**, not the directory. One clause: *grep the check you are citing,
not the folder it lives in.*

---

## The instruments

```
code/state_control_audit_2216/
    mutation_battery.py   14 mutations, none of them mg-2da3's, applied to the working tree
                          and restored under a finally + sha256 check; refuses to run dirty
    claims_audit.py       read-only: the pinned battery's purpose, findability, the commit's
                          own arithmetic, and both caveats audited as claims
    run_all.sh            both, ~11 s measured
    out_mutations.txt     committed output, reproduces byte-identically
    out_claims.txt        committed output, reproduces byte-identically
```

**Instrument discipline.** Nothing shells out to `wc` — characters are `len(str)`, bytes are
`len(bytes)`, and every figure names its unit. No mutation is stacked on another: the tree is
restored from its byte snapshot before each one. Every tally names the population it was
taken over (210 cells, 62 rows, 14 mutations). The one figure that cannot reproduce
byte-identically — wall-clock — is reported as a bracket in the committed output and as raw
seconds only here, stamped with the box it was measured on.

**What my own battery does not establish.** It measures *sensitivity*, not correctness: a
mutation passing means the control cannot see that change, not that the change is present.
The tolerance rows (M04, M08, M12, M13) are in the battery precisely so this cannot be read
as a demand for a stricter instrument in every direction — some of what `delta_control.py`
ignores, it ignores correctly and on the record.
