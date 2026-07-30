# Independent audit — the mg-8916 repair (`b055ae5` + `f5360bf` + `d1dd84d`)

**Work item mg-8aae. Pre-filed in the same action as its parent mg-8916.**
**Instrument: `code/hodge_leverage_audit_8aae/`, `run_all.sh`, ~4 min. Committed transcript:
`out_audit_8916.txt`. Predicted exit code, written before the first run: 1. Observed: 1.
30 checks, 1 refuted, 2 findings.**

---

## Verdict

**PARTIAL. The repair is real and it is the harder of the two repairs on offer.**

mg-835f's primary target — *12 of 12 reader-facing figures corrupted on disk make the run red,
12 of 12 restorations make it green* — is **intact, and intact at a granularity nobody has
measured it at before**: for each of the 12, it is the `READ AT THE SITE` row **for that figure**
that fails, not merely some other row of the widened gate. The widening did not absorb the check
it was added beside. G-1 is closed against an instrument that is not the repair's own: wording
this audit chose, slots this audit chose, each slot **controlled green before use**, fires 6 of 6
and restores 6 of 6. And the repair **says which of the three dispositions it took**, in the
document and again at the code.

Two things are open, and both are the same shape as the findings they descend from — a printed
extent slightly wider than the code that backs it.

| | |
|---|---|
| **H-1** | **THE CENSUS IS A MULTISET, SO A PERMUTATION IS INVISIBLE.** Two *declared* figures of equal length exchanged in ordinary prose leave the multiset identical, every designated statement correct and the length unchanged. The runner stays at **exit 0 at 2 of 2** sites probed, while the section now asserts two figures the wrong way round. This is not one of the three exclusions the repair prints. **MODERATE** |
| **H-2** | **`SUMMARY vs ROWS` COMPARES A VALUE WITH ITSELF.** It scores `printed == derived` where `printed = FORCE_SUMMARY or derived`, so with the forcing hook unset it is `x == x` and **cannot fail for any tree**. It does not read the sentence that is printed: with the REFUTED branch's own headline edited to say CONFIRMED, the transcript reproduces **G-2's exact artifact** — "THE PRIMARY TARGET IS CONFIRMED" printed above its own refuted PRIMARY rows — and the check stays `[CONFIRMED]`. **MODERATE** |

**0 mathematical statements are touched here and no finding of mg-835f, mg-8a5c or mg-8916 is
re-marked.**

---

## 1. Which repair was done — and it is said

The ticket named three dispositions and warned that a **silent narrowing reads as a fix while
being a reduction in coverage**. mg-8916 took none of the two it named: it **widened the code**,
and it says so in the document (*"CLOSED BY WIDENING THE CODE. The stated extent is not
narrowed"*) and again in `verify_landing.py` at the widening itself.

Checked here, not taken on the document's word:

- `census_gate` **does not exist** at `b055ae5^` and is called by `figure_gate` at HEAD — a
  widening, not a re-wording.
- Checks **(a) at the site** and **(b) written once** are still printed as part of the extent
  after the widening.
- The measurement the choice rests on — *"there is nothing to remove"* — is **re-derived here**
  over all 12 (site, figure) pairs, with this instrument's own tokenizer: **0 live figures are
  written more times than their site licenses**. So the preferred repair genuinely had nothing to
  remove, and the choice really was between widening the code and narrowing the claim.
- The printed extent — **17 / 16 / 36 licensed figure tokens, 69 in total** — is **re-counted by
  a tokenizer that shares no regex with the one that produced it**, and the two agree at 3 of 3
  sites. The extent is not a number written beside the gate.

**On the ticket's "change the structured value and confirm the prose changes with it":** that
test does not apply, and the reason is worth stating rather than skipping. There is **no
derivation to test**, because there is no prose duplicate — the mg-a318 repair already removed
the second copy, and `WRITTEN ONCE` keeps it removed. What mg-8916 added is not a derivation but
a **census against a hand-declared roster**, which is a different object with a different
failure mode: it is **fail-closed**, so a roster that falls out of step with the documents makes
the run red rather than silently agreeing with it. That is the right direction, and it is the
direction the ticket's warning is about.

---

## 2. mg-835f's 12 of 12 is not weakened — checked at row granularity

This is the result the ticket asked to be protected, and an exit-code check cannot protect it: a
widening that made the run red for a *new* reason while the old check went quiet would keep the
headline and lose the result.

So each of the 12 designated figures is corrupted **on disk** to a different figure **of the same
length** (so nothing measured moves underneath the gate), and the requirement is stricter than
mg-835f's:

| requirement | result |
|---|---|
| the real runner goes red | **12 of 12** |
| **and the `READ AT THE SITE` row FOR THAT FIGURE is the row that failed** | **12 of 12** |
| the restoration returns the runner to exit 0, sha256-verified | **12 of 12** |

**The old check is doing the old work. The census did not absorb it.**

The in-memory battery rides inside the runner, so it was re-taken on every one of the ~50 runner
invocations this audit made: it grew from **9 mutations to 14** and **14 of 14 move the gate as
predicted**, N1–N3 (the presence-test's own blind spot) still firing alongside N10–N14. Nothing
was traded for the widening.

---

## 3. G-1 is closed against wording this audit chose

Not mg-835f's sentence and not mg-8916's named ballast. The prose slot at each site is selected
here **by a procedure**, and each slot is **controlled before use**: blanked length-preservingly,
the runner must stay green — so a fire is attributable to the *figure*, not to the edit. A
candidate that lands inside a marked quotation is rejected, because a probe there would measure
the declared exemption rather than the gate.

| probe | control | result | restored |
|---|---|---|---|
| this audit's own sentence carrying `+9 999`, at 3 sites | green 3 of 3 | **GATE FIRES 3 of 3** | silent 3 of 3 |
| the same carrying `+1 630` — a value **already on the roster** at all three sites | green 3 of 3 | **GATE FIRES 3 of 3** | silent 3 of 3 |

**6 of 6 fire; 6 of 6 restorations return the runner to exit 0.** The roster-reuse shape is the
one a set-membership census passes, and the multiset catches it: the transcript shows it firing
as *"`+1 630` appears 2x, licensed 1x"*.

And **mg-835f's own instrument, unmodified**, re-run here rather than quoted from mg-8916's
transcript: **3 of 3 U1 rows read `GATE FIRES`, 0 findings, exit 0**, with its committed
transcript sha256-identical afterwards. It is byte-identical between `b055ae5^` and HEAD, so the
instrument that raised the findings was not edited by the repair that answers them.

---

## 4. H-1 — the census is a multiset, so a permutation is invisible

**Audited because no line of the brief names it**, and because it is G-1's own shape one
generation on.

The census asks whether every figure a reader meets is *licensed*. It cannot ask whether each is
attached to the statement it belongs to — a multiset comparison has no notion of position. So:
**exchange two declared figures of equal length in ordinary prose.**

| probe | predicted | observed |
|---|---|---|
| **H8**: `before mg-a2bd : 13 551` ↔ `after mg-a2bd : 16 692` | gate SILENT | **gate passes, exit 0** |
| **the STATE.md row**: the chain `2 928 → 6 069 → −875 → +755` run backwards in its last two terms | gate SILENT | **gate passes, exit 0** |

Both mutations are checked to be **permutations and nothing else** before they are written: the
multiset of figure tokens is verified identical before and after, and every designated statement
verified to read the same value.

Nothing about either is outside the gate's declared reach. Each is **inside the section**, **not
inside a marked quotation**, **of the figure-shaped class**, **length-preserving**, and leaves
**every designated statement correct**. All three of the gate's checks are satisfied, and:

- H8's own table now says the `STATE.md` row **shrank** across mg-a2bd, against the `(+3 141)`
  printed on the same line;
- the STATE.md row's chain — **the chain F-1 was born in** — now asserts the gap reached `+755`
  *before* it went negative.

A reader meets a wrong figure at the site, in ordinary prose, and the widened gate is silent.

**What this is and is not.** The code does what its own sentence says: every token present is
licensed. What is wrong is the **extent list** — the repair prints three exclusions (marked
quotations / outside the section / not figure-shaped) and **position is a fourth**. That is the
same defect as G-1: a printed claim slightly wider than the code under it. The cheapest honest
repair is one line on that list; the fuller one is to bind roster entries to the statements they
belong to, which is what `(a)` already does for the live figures.

---

## 5. H-2 — `SUMMARY vs ROWS` compares a value with itself

The ticket: *"the summary-versus-rows check must exist and must be SHOWN to fire. Make them
disagree and confirm it goes red."*

**Direction 1 — the repair's own hook, re-run here.** Forced with `MG8916_FORCE_SUMMARY`, the
check goes `[REFUTED]` and the refuted count moves **3 → 4**, exactly one. That reproduces, on
this tree, what mg-8916 reported.

**Direction 2 — the same artifact, made the way G-2 was actually made.** G-2 was not an
environment variable; it was a **hand-written sentence**. So the disagreement is created in the
sentence instead of in the verdict variable: the REFUTED branch's own headline is edited from
`f"THE PRIMARY TARGET IS {verdict} IN THIS TREE"` to a literal `CONFIRMED`.

| | |
|---|---|
| the transcript now prints | `THE PRIMARY TARGET IS CONFIRMED IN THIS TREE: 2 of 2 rows tagged…` |
| its PRIMARY rows say | **REFUTED** |
| `SUMMARY vs ROWS` | **`[CONFIRMED]`** |
| refuted count | **3 → 3, unmoved** |

**G-2's exact artifact is reproduced with no environment variable set, and the check is green.**

The mechanism is two lines:

```python
printed = FORCE_SUMMARY or derived
record(printed == derived, ...)
```

With the hook unset, `printed` **is** `derived`. The check cannot fail for any tree, any figure,
any row. It is not a comparison of the printed verdict against the rows — it is a comparison of
the rows' verdict with itself, and the document calls it the former.

**In the repair's favour, and it matters:** the **derivation is the real repair and it is sound.**
The verdict can no longer be *chosen*; the branch is selected by the rows, and the parenthetical
count is taken from the rows. G-2 as it stood cannot recur by accident. What is overstated is the
**check**, and what is left standing is the **branch text**, which is still hand-written prose
asserting things the rows do not carry (*"the repair's three figures are the POST-commit ones and
reproduce exactly from the tree"*).

**And this is the vacuous-check shape wearing the fix's name.** It was demonstrated firing — the
ticket's requirement is met literally — but only through a hook built for the demonstration. The
demonstration establishes that the plumbing counts and exits; it does not establish that the check
discriminates, because it cannot. Three vacuous checks in one night were caught by asking *has it
been shown to fire?*; this one passes that question and fails the next one, which is *can it fire
on anything but the thing that was built to make it fire?*

---

## 6. The rule applied to this repair's own summary

*"If this deliverable's own summary disagrees with its own rows, believe the rows and report the
summary as the defect."*

Checked, and it does not:

| the document's header | `out_repair_8916.txt` |
|---|---|
| 18 checks | **18 checks recorded** |
| 0 refuted | **0 refuted** |
| predicted exit 0, observed 0 | consistent |

and 5 of 5 of its headline rows are located verbatim in the transcript it cites. **The summary
agrees with its rows, so there is nothing to disbelieve.** The one prediction mg-8916 records as
missed — that the preferred repair would apply — is kept as written in its own document.

---

## 7. The seam check, and its threshold

**THRESHOLD: 0.80 similarity, minimum passage length 60 characters after normalisation, marker
window ±12 lines** — the same threshold, minimum and window mg-a218 and mg-d330 used, so the
sweeps are comparable. Swept population: the 7 files a reader of this arc actually reads, at
HEAD, against every passage the three repair commits deleted.

A line a commit **rewrites in place** appears in the diff as a deletion and its replacement is of
course still live in the same file — that is editing, not a seam, and those are dropped and
counted separately. A passage that survives **and is marked as corrected within the window** is
not a seam defect and is not counted; the mg-835f audit's broken reproduction contract is
annotated in a ⚠️ block three lines below the contract, which a line-local test cannot see.

**Result: 0 unmarked survivals**, over 6 swept deleted passages (26 of the 32 deletions were
in-place rewrites) × 2 285 live lines.

---

## 8. What this audit got wrong, kept as written

Across three runs this instrument refuted **five rows that were its own defects and not the
repair's**. They are in `PREDICTIONS.md`, they are annotated at the code that was wrong, and they
are not tidied away — an audit that edits its own misses out of its predictions file is an audit
reporting on itself. The final run refutes **one** row, and that one is the target's.

| predicted | what happened | whose defect |
|---|---|---|
| the printed extent agrees | **MISSED TWICE** — H8: runner 36, this instrument 27, then 27 again | **mine.** My second tokenizer took a whole run of space-separated groups as one token. Flattened, H8's three-column table reads `9 748 11 378 13 367` — three figures — and a parser that asks whether the *whole run* is well formed drops all three. **The runner was right about the tree both times and I reported the disagreement against it.** Corrected to consume groups greedily left to right; the two tokenizers now agree exactly, **17 / 16 / 36 = 69** |
| 6 of 6 prose probes fire | **PARTIAL TWICE** — 4 of 6, then 2 of 6 with the sites swapped | **mine.** First my ballast picker rejected any candidate containing a newline and these documents are hard-wrapped, so §14 offered none; then my line-based rewrite skipped lines starting with `\|`, and the `STATE.md` row **is** a markdown table cell, so every one of its lines starts with `\|` |
| 0 seam findings | **MISSED** — 14 reported | **mine.** 14 of 14 were lines the commit rewrote **in place** — an edit, not a seam — or correction markers sitting outside a line-local window |

**Every row that was about the target was predicted correctly on the first run and has not
moved**: 12/12 at row granularity, 12/12 restored, the forced summary firing and moving the
refuted count by exactly one, mg-835f's instrument at 0 findings and exit 0, the document's header
agreeing with its transcript — and the two findings, **both predicted before they were run**.

The pattern is worth naming, since this arc collects them: **every one of my five misses was an
instrument that disagreed with the target and was itself wrong.** A disagreement between an
instrument and its target is not evidence about the target until the instrument has been checked
in the direction that would embarrass it.

---

## Reproduction

    sh code/hodge_leverage_audit_8aae/run_all.sh     # ~4 min, exit 1

The transcript regenerates byte-identically at any tree in which `STATE.md`,
`docs/OneThird-Hodge-Side-Leverage.md`, `docs/state-history/attempt-mg-a3d4.md`,
`docs/OneThird-Hodge-Side-Leverage-Mg835fRepair.md`,
`docs/OneThird-Hodge-Side-Leverage-Mg8a5cRepair-IndependentAudit.md`,
`code/hodge_leverage_landing_e1d0/`, `code/hodge_leverage_audit_8a5c/`,
`code/hodge_leverage_audit_835f/` and `code/hodge_leverage_repair_8916/` are unchanged; it embeds
no sha of its own, and it was **checked byte-identical across two consecutive runs**. It
**mutates the tree and restores it** — `STATE.md`, the deliverable, the
row-history file and the mg-8a5c instrument's source — refuses to run against a tree in which any
of those is dirty, and verifies every restoration by sha256. `git status` is clean after a run
except for `code/hodge_leverage_audit_8aae/out_audit_8916.txt`.
