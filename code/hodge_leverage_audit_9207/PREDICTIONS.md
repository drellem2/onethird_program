# mg-9207 — predictions, written BEFORE the first run

Independent audit of the mg-8eca repair (`d59ecd9` + `bee07a1`) of the two items mg-8aae left
open on the mg-8916 repair: **H-1** (the figure census is a multiset, so exchanging two declared
figures is invisible) and **H-2** (`SUMMARY vs ROWS` is `x == x`, firing only off a purpose-built
hook).

Every exit code and every probe verdict below is written before the instrument is run.
**Misses are kept as written.**

## The standard this audit holds the demonstrations to

The defect mg-8aae raised was *a check that fired only through a purpose-built hook while being
`x == x` against the artifact*. So a demonstration counts here **only if it runs the same path a
real defect would**: the real file on disk, the real runner as a subprocess, no environment
variable, no in-memory call of the gate function, no fixture. mg-8eca's own negative control
`N15`–`N18` calls `figure_gate` on in-memory copies — that is a **fixture** and is not accepted
here as evidence; it is re-taken on disk below.

---

## C — the census, on disk, against the real runner

`python3 code/hodge_leverage_landing_e1d0/verify_landing.py`, run as a subprocess against the
real files, with the mutation written to disk first. Pairs are **selected by a procedure**, not
by hand: within a site's asserted figure sequence, every pair of **adjacent, distinct,
equal-length** tokens **neither of which is a value measured live this run**, taken greedily
disjoint, first four per site.

| # | probe | predicted |
|---|---|---|
| C0 | the runner on the clean tree | **exit 0** |
| C1 | my scanner's asserted sequence lengths agree with the roster's declared slot counts (17 / 16 / 36) | 3 of 3 |
| C2 | **each exchange on disk → the runner goes red** | **GATE FIRES, 12 of 12** |
| C3 | ...and the row that failed is the **`FIGURE ORDER` row for that site**, and the **only** row that failed | 12 of 12 |
| C4 | ...and the site's `CENSUS` (licensing, multiset) row stays `[CONFIRMED]` — the artifact's own evidence that the mutation was a permutation and nothing else | 12 of 12 |
| C5 | each exchange applied **twice** returns the file byte-identical (a transposition is an involution) and the runner exits 0 | 12 of 12 |
| C6 | **3-cycles, both cyclic senses** — three distinct equal-length non-live tokens rotated forward and backward | GATE FIRES, 4 of 4 (2 sites × 2 senses; the `STATE.md` row has no such triple and is reported as absent, not as a pass) |
| C7 | every restoration sha256-verified against the pristine file | all pass |
| C8 | **§14** — the site mg-8eca never exchanged on disk (`N15`–`N18` are `H8` and the `STATE.md` row) | included in C2–C5, GATE FIRES |

**C2–C4 are the primary target.** If any exchange is silent, or if the only firing path is
`figure_gate` called in memory, H-1 is reported **unfixed**.

## E — did the fix move the invariance?

| # | probe | predicted |
|---|---|---|
| E1 | two occurrences of the **same** token exchanged | the exchange is the **identity on the bytes** — 0 characters change, so there is nothing to detect and mg-8eca's declaration is true by construction |
| E2 | **the two LABELS exchanged instead of the two figures** — `H8`'s `mg-a2bd` table, `before mg-a2bd` ↔ `after  mg-a2bd`, figures left where they are | **SILENT, exit 0** — the same reader-visible defect as mg-8aae's own `N15` (the table says the row *shrank* across `mg-a2bd`), reached from the other side |
| E3 | the two historical **column headers** of `H8`'s three-column table exchanged | **SILENT, exit 0** — every historical column now attributed to the wrong commit |
| E4 | two **row labels** exchanged inside the same table (`gap, cell only` ↔ `gap, cell + relocated history`) | **GATE FIRES**, and the rows that fail are the two `READ AT THE SITE` rows, **not** `FIGURE ORDER` |
| E5 | a figure **moved to a different site with the same value** (`48 846` dropped at `H8`, doubled at the `STATE.md` row) | **GATE FIRES** at both sites |

E2/E3 are this audit's own item — **nothing in the assignment names them**. The prediction is
that they are silent, i.e. that the repair closed the *figure* half of a transposition and left
the *label* half open, so the invariance moved rather than went away.

## D — `SUMMARY vs ROWS`, on the real artifact

`python3 code/hodge_leverage_audit_8a5c/audit_repair_8e30.py`, run as a subprocess, **no
environment variable set** except where the row says otherwise. There are exactly **2** rows
tagged `PRIMARY`, and on the tree as it stands **both are refuted**.

### D-row — the direction the assignment names: move a ROW, not the sentence

| # | probe | predicted |
|---|---|---|
| D0 | the audit on the clean tree | `SUMMARY vs ROWS` **`[CONFIRMED]`**; exit 1; 3 refuted rows |
| D1 | **`2` of 2 `PRIMARY` rows refuted** (the tree as it stands) | `SUMMARY vs ROWS` **`[CONFIRMED]`** |
| D2 | **`1` of 2 refuted** — the **first `PRIMARY` row's own expectation** brought up to the live measurement **on disk**, the second left stale | `SUMMARY vs ROWS` **`[CONFIRMED]`** — it does **not** fire |
| D3 | **`0` of 2 refuted** — **both** `PRIMARY` rows' expectations brought up to the live measurement on disk | `SUMMARY vs ROWS` **`[CONFIRMED]`** — it does **not** fire |

*Method note, written before the first run.* The `PRIMARY` rows compare live lengths against
constants frozen in the instrument's **own source** (`a == 12692 and h == 18593 and b == 10623`),
and the source itself says a later commit that legitimately moves them makes these rows refuted
on a re-run. So the row is moved **by editing the row**, on disk, with no environment variable —
rather than by editing `STATE.md`, the deliverable and the row-history file, which the audited
instrument's own dirty-tree guard refuses to run over (it `git checkout --`s those three and
`SystemExit(2)`s if they are already dirty, which would abort before the bottom line is reached).
`audit_repair_8e30.py` is **not** in that guard's scope, which is what makes this direction
runnable at all.
| D4 | therefore: **no achievable state of the rows makes the check fire** | 3 of 3 states green — the check discriminates edits to `primary_summary`'s **own source text**, not disagreement between the summary and the rows |

D2/D3 are the assignment's *"edit a row in the real document so it disagrees with the summary"*.
The prediction is that **it cannot be done**, and that this is the finding rather than a failure
of the probe: on the `REFUTED` path the printed verdict is `{verdict}` and the printed count is
`{len(bad)}`, which are the same two expressions the other side recomputes.

### D-text — the direction mg-8eca demonstrates, re-taken here

| # | probe | predicted |
|---|---|---|
| D5 | mg-8aae's direction-2, verbatim, on disk, **no env var**: the `REFUTED` branch's headline edited to a literal `CONFIRMED` | **`[REFUTED  ]`** |
| D6 | the **count** edited and the verdict word left correct | **`[REFUTED  ]`** |
| D7 | **a coherent false summary** — headline *and* count both moved to the `CONFIRMED` reading, which is what a hand-writer producing G-2 would actually write | **`[REFUTED  ]`** |
| D8 | mg-8916's hook, kept: `MG8916_FORCE_SUMMARY=CONFIRMED` | **`[REFUTED  ]`** |

### D-del — the deletion test, at the finest unit that has a return

The repaired condition is `agree = printed == derived and said == owed`. Each conjunct is
deleted **on its own** and every direction above is re-scored against it.

| # | deletion | predicted |
|---|---|---|
| D9 | `printed == derived` removed, `said == owed` kept | D5 **still red**, D6 **still red**, D7 **goes green**, D8 (hook) **goes green** |
| D10 | `said == owed` removed, `printed == derived` kept | D5 still red, D6 **goes green**, D7 still red, D8 still red |
| D11 | the defect reinstated (`printed = FORCE_SUMMARY or derived`) | D5, D6, D7 **all green**; D8 red — the control that makes D5–D7 attributable |
| D12 | **so: of the four directions mg-8eca declares, how many isolate `printed == derived`?** | **1 — and it is D8, the hook.** D5 and D6 leave that conjunct inert; D7 is this audit's own construction and is not in mg-8eca's battery |

If D12 lands as predicted it is a finding of exactly the shape mg-8aae raised, one level down:
half of the repaired condition is still demonstrated **only** through the environment variable.

## S — do not disturb what is confirmed

| # | probe | predicted |
|---|---|---|
| S1 | mg-8aae's own `audit_8916_repair.py`, **unmodified**, on this tree | **0 findings**, exit 0; its `A2` (12 of 12 at row granularity) and `A3` (G-1 against its own wording) still hold |
| S2 | mg-8916's own `repair_835f.py`, **unmodified** | 18 checks, 0 refuted, exit 0 |
| S3 | every committed transcript this run reads is sha256-identical afterwards | all pass |
| S4 | `git status --porcelain` outside this directory after the run | empty |

## PX — this instrument's own exit code

**1.** Not because the repair fails — C2–C4 and D5–D8 are predicted to hold — but because E2/E3
and D4/D12 are predicted to land as findings, and an instrument that raises findings and exits 0
is the defect this arc keeps meeting.

---

## Misses, kept as written

Nothing above this line has been edited. Four rows missed. **Three were defects in THIS
instrument** — and the fourth is the most interesting result in the audit.

| # | predicted | first run | whose defect | disposition |
|---|---|---|---|---|
| C3 | the `FIGURE ORDER` row is the only row that failed, 12 of 12 | **MISSED — 4 of 12** | **mine** | the criterion counted **every** refuted line. The landing runner's own negative-control battery re-evaluates its 18 mutations against the **mutated** site texts, so 8 of 12 exchanges legitimately turn its self-test row red as well. That row is a true report of a tree nobody should ship; it is not a gate row. Corrected: scored over **GATE rows**, and the self-test row counted separately as `C7b`. Re-run: **12 of 12** |
| C4 | the site's licensing row stays `[CONFIRMED]`, 12 of 12 | **MISSED — 0 of 12** | **mine** | my parser looked for `GATE @ <site>: CENSUS --`; the row prints `GATE @ <site>: FIGURE CENSUS --`. A check that cannot find the row it scores reports `None` and calls it a failure. Corrected. Re-run: **12 of 12** |
| E2 | the label exchange is **SILENT, exit 0** | **HALF MISSED — silent at the gate, exit 1** | **the audited tree's** | the gate refuted **0 rows** — the substance was right. But the runner still exited 1, by **AssertionError out of its own negative control**: mg-8eca's `transpose` freezes `H8_TABLE` as a literal and asserts it occurs once, and the label exchange rewrites those two lines. So a silent gate and a crashed runner produce the same integer. This became finding **J-3**, and it is the reason every E row is now scored at **gate granularity** and not at the exit code |
| S1 | mg-8aae's instrument: 0 findings, **exit 0** | **MISSED on the exit code, and on the row counts** | **mine, twice** | (a) I counted `[REFUTED  ]` at any indent, so mg-8aae's six **echoed** sub-run GATE lines — which are its probes *working* — read as its own failures. Corrected: only rows at exactly two spaces of indent are the instrument's own. (b) exit 0 was wrong on the substance: mg-8aae's A4 permutation row is now **refuted**, because the gate fires where it observed exit 0, and its predictions are left as written reading `PREDICTION MISSED`. **That is what a landed finding looks like from the raising instrument's side**, so exit 1 is correct and my prediction was not |

### Added after the first run, and predicted before the second

Declared as additions rather than folded into the table above.

| # | probe | predicted before run 2 | run 2 |
|---|---|---|---|
| C7 | how many of the 12 exchanges make the runner **crash** rather than report | some — the four that collide with the control's frozen literals | **HIT, 4 of 12**, and they are exactly mg-8eca's own `N15`–`N18` sites |
| C7b | how many turn the runner's negative-control self-test row red | 8 of 12 | **HIT, 8 of 12** |
| E2b | the same label exchange at a table the control does **not** hard-code | **SILENT, exit 0** — so the finding is not one accident | **HIT** |

### Hits

`C0`, `C1` (17 / 16 / 36, 3 of 3), `C2` (**12 of 12**), `C5`, `C6` (4 of 4, with the `STATE.md`
row's absence of a usable triple reported as an absence), `C8` (§14 fires like the rest), `E1`,
`E3`, `E4`, `E5`, `D0` (`[CONFIRMED]`, exit 1, **3** refuted rows), `D1`–`D4` (**3 of 3 states
green**), `D5`–`D8` (**4 of 4 red**), `D9`–`D12` (the grid came out exactly as predicted, cell for
cell), `S2`/`S3`/`S4`, and `PX` (**exit 1**).
