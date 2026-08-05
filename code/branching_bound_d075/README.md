# `code/branching_bound_d075/` — the instrument for mg-d075

**What this measures.** How many sentences of
`docs/OneThird-Branching-Graphs-Where-This-Lives.md` state the 33-interval Young–Fibonacci
figure, how many of them carry the scope that figure has (`rank(w) ≤ 6`), and whether the
prose this repair itself writes meets the standard it imposes on that document.

**The prose account is `docs/repair-mg-d075-the-figure-and-its-scope.md`.** This file is the
instrument's own record: what each script does, what it found, what it found *in this
repair*, and the prediction scorecard.

```
sh code/branching_bound_d075/run_all.sh          # ~5 s, no network, no deps
```

`run_all.sh` is green **only if every script's exit code equals the value `PREDICTIONS.md`
committed for it before that script existed**, and only if each script also wrote at least
one `SUMMARY` line. The second condition exists because of a defect of this runner, found by
this runner: `s1_census` is predicted to exit **1**, a Python traceback also exits 1, and for
one run a crash was scored `ok`. An exit code alone is not evidence that a script ran.

---

## 1. THE FILES

| file | what it is |
|---|---|
| `PREDICTIONS.md` | 12 predictions and 9 exit values, committed at `ec98300` **before any `.py` in this directory existed**, with every hand command run beforehand disclosed |
| `lib_d075.py` | the reader: units, liveness, sentence grain, and the two predicates. A **re-implementation**, not an import — a check that runs the parent's code cannot refute the parent's code |
| `s1_census.py` | **I count the sites myself.** Four named populations, pre-repair and post-repair side by side |
| `s2_reproduce.py` | **the parent's 8/4/4 reproduced** row-by-row against its own committed transcript, then the one clause whose removal turns 8 into 9 |
| `s3_bound.py` | **the gate**: 0 unbounded, no site lost, no figure lost, and this repair's own prose held to the same standard |
| `s4_hedge.py` | **bounded, not merely hedged** — 33 hedge tokens, and the predecessor's own hedge figure counted rather than quoted |
| `s5_own_criticism.py` | **the sentences in which I fault someone else's scope, checked for my own** |
| `s6_class.py` | **instance or class?** — measured, verdict computed from a rule stated above the answer |
| `selftest_d075.py` | 17 deliberate breakages, each asserted to be a real change before its verdict is checked |
| `out_*.txt` | committed transcripts of the run in this commit |
| `out_s3_bound_FIRSTFORM_exit1.txt` | the gate's **first form, exiting 1** — kept because it fired on me |
| `out_s5_own_criticism_FIRSTRUN_exit1.txt` | the self-criticism check's **first run, exiting 1** — kept for the same reason |

---

## 2. THE HEADLINE

**Population: live sentences of `docs/OneThird-Branching-Graphs-Where-This-Lives.md`, at the
pre-repair anchor `645b5a4`. Grain: one sentence.**

| predicate | sites | bounded | unbounded |
|---|---|---|---|
| **STRICT** — the sentence contains the figure `33`, the interval count at `rank(w) ≤ 6`, **and** the sentence names Young–Fibonacci (mg-19ec's POP-3) | **8** | 4 | 4 |
| **RELAXED** — one clause dropped: the naming may come from the cell or paragraph | **9** | 4 | **5** |

**EIGHT IS NOT THE POPULATION EITHER.** The ninth is the row-10 sentence of §3, which said
*"on 28 of 33 intervals"* of the 33 intervals `[0̂, w]` with `rank(w) ≤ 6` and never spelled
*"Young–Fibonacci"* — and which **mg-19ec's own POP-1 block already printed and scored
unbounded.** One audit, two instruments, and only the
smaller number reached the verdict.

Post-repair, over the same file: **10 sites, 10 bounded, 0 unbounded, under both
predicates.** 10 rather than 9 because this repair's own note states the figure and so joins
the population it describes — it carries the bound too.

---

## 3. WHAT EACH SCRIPT ESTABLISHED

- **s1** — pre-repair A 8 / B 9 / ceiling 10 / corpus **29 sites in 6 files, 17 unbounded**.
  Post-repair A 10 / B 10 / ceiling 11 / corpus 36 sites in 7 files, 12 unbounded.
- **s2** — the parent's transcript parsed to 8 rows; my independent STRICT re-implementation
  returns the same 8 line numbers and the same 8 verdicts; **0 reproduction checks failed**.
  Dropping the same-sentence clause admits **1** site and retracts none.
- **s3** — 0 unbounded under both predicates; all 9 pre-repair sites matched by shared
  vocabulary; 1 integer occurrence fell and it is adjudicated at the site that caused it.
- **s4** — 10 of 10 site bounds are numeric scopes, not softening words; 3 of 14 new
  sentences carry a hedge token and **all 3 enumerate what falls inside it**.
- **s5** — over **253** live sentences of my own prose, **10** are criticism sentences;
  **1 of 5 was unbounded on the first run** (before the README existed), 0 of 10 now.
- **s6** — 3 of 3 prior instances located; gate covers 2 of 7 corpus files; **VERDICT
  INSTANCE + REUSABLE ARTEFACT**.
- **selftest** — 17 mutations, 0 failures, every mutation asserted non-trivial first.

---

## 4. THE FLOOR — two things no brief in this lineage named

1. **The liveness rule is applied per CELL, so one ledger row yields both struck and live
   cells.** `s2`'s R3: **3 rows** of the document split that way — B2′, B4′, B7′. Row B4′ has
   **2 struck cells and 1 live**, and the live one is a site this repair had to bound.
   Adjudicated over those 3 rows as a property of the instrument, not scored as a defect:
   a row recording a withdrawn reading *should* contribute the replacement as a live claim.
2. **The predecessor's own hedge figure is a hand-written literal.**
   `docs/OneThird-Warrant-Repair-mg-dffa-IndependentAudit.md` says twice that the phrasings
   were scanned *"against 26 hedge tokens"*; the `HEDGES` list in
   `code/branching_audit_19ec/e2_f2_clauses.py` has **25** entries and that audit's transcript
   never prints a token count. Its phrasing population is **15** in the transcript and **13**
   in the verdict that reached this repair's brief. Both are this arc's own defect class.
   **Neither is repaired here** — that document is a dated record — and neither is scored
   against this repair. Handed to mg-aaf4.

---

## 5. WHAT THIS REPAIR DID TO ITSELF

Six, all found by this repair's own instruments, all recorded rather than tidied away. The
full account is §4 of `docs/repair-mg-d075-the-figure-and-its-scope.md`; in brief:

1. A bound written into the **next** sentence rather than its own — the §2.1 defect,
   reproduced by me while repairing it.
2. `|λ| ≤ 6` written inside a markdown table cell, splitting ledger row B4 on the pipe.
3. This repair's own note, **unbounded**, and asserting a population figure its own existence
   had already falsified.
4. A grain mismatch in `s4`'s own output: a `set` count printed against a `list` count.
5. **Two checks respecified after they fired on me** — G3's first form forbade any integer
   occurring fewer times (it fired on the deliberate factoring of two unbounded *"of the 33"*
   restatements into one bounded statement); G2's first form demanded the population be the
   same size (it fired the moment this repair recorded itself in the document). The
   first-form transcript is committed. **The reasoning lives in the code at the point of each
   check, not only in prose.**
6. A line-number identity that was not one: G3's per-site adjudication first keyed on line
   numbers and reported 4 sites as having lost a figure — every one an artefact of this
   repair shifting the lines below its own edits.

And one of this **runner**: a crashed script scored `ok` because its traceback exit matched
the predicted 1. Fixed by requiring a `SUMMARY` line.

---

## 6. WHAT THIS REPAIR DID NOT DO

- **It did not repair the corpus.** 12 sites remain unbounded in 5 `docs/*.md` this repair
  does not touch. They are audit and repair records dated by their commits; editing them
  would destroy the evidence trail. The decision was taken in `PREDICTIONS.md` P5 **before**
  the corpus was counted, and the number is printed rather than omitted.
- **It did not address the class.** A path-parameterised predicate can be pointed at a fourth
  document; it cannot be pointed at the habit of writing a figure and its scope in different
  places. What would address the class is a check running over every document on every
  commit. This repair does not install one.

---

## 7. PREDICTIONS SCORED

`PREDICTIONS.md` was committed at `ec98300` before any script here existed. **Nothing below
was revised after a run.**

| # | prediction | outcome |
|---|---|---|
| P1 | 9 sites, 4 bounded, 5 unbounded — not 8 | **HELD**, exactly |
| P1a | the ninth is the row-10 sentence at line 307, named in advance | **HELD** |
| P1b | mg-19ec's own POP-1 already printed it | **HELD** (s2 checks the transcript, not memory) |
| P2 | the parent's 8/4/4 reproduces exactly, same 8 line numbers | **HELD**, 0 checks failed |
| P3 | my 5 unbounded of the 9 = the parent's 4 of the 8 plus line 307, none moving the other way | **HELD** |
| P4 | corpus > 20 sites and more than half unbounded — a blind forecast | **HELD**: 29 sites, 17 unbounded (59%) |
| P5 | the corpus is reported and not repaired, named as a scope decision | **HELD** |
| P6 | after the repair: 0 unbounded under both predicates, **population 9 unchanged** | **SPLIT — the second clause is REFUTED.** 0 unbounded holds under both. The population is **10**, not 9: this repair's own note states the figure and joins the population. Kept as written |
| P7 | every bound an enumeration or numeric scope, and **0 new phrasings carrying a hedge token** | **SPLIT — the second clause is REFUTED.** 10 of 10 bounds are numeric scopes. **3 of 14** new sentences carry a hedge token — `kind` and `some`, two tokens I added to the list myself — and all 3 enumerate what falls inside them, which is mg-19ec's own standard. The literal prediction of 0 is wrong |
| P8 | the sharpest site is line 186 and both halves must be bounded | **HELD** |
| P9 | **s5 exits 1 on its first run — I will do it too** | **HELD.** 1 of 5 of my criticism sentences was unbounded, and it was the one faulting mg-dffa's clause for having no bound. It fired twice more as the deliverable grew: 2 of 10 once the README joined the population, and `s3`'s G4 found 2 unbounded sites in the README itself. Transcript committed as `out_s5_own_criticism_FIRSTRUN_exit1.txt` |
| P10 | instance + one class-level artefact, not the class, said plainly | **HELD**: `s6` computes INSTANCE + REUSABLE ARTEFACT |
| P11 | row B4′ splits struck/live, ≥ 2 struck and ≥ 1 live | **HELD**: 2 struck, 1 live |
| P12 | ≥ 1 other row splits the same way | **HELD**: 2 others, B2′ and B7′ |

**12 predictions: 10 held, 2 refuted in one clause each. 9 of 9 exit values matched.**

The two refutations are both of the same shape, and it is the shape this whole arc is about:
**I predicted a count without allowing for the population changing under my own hand.** P6
assumed a repair does not join the population it repairs; P7 assumed a token list I extended
myself would not fire on my own prose. Neither was argued away and neither prediction was
edited.

---

## 8. FOR mg-aaf4

The pre-filed audit is told not to take **8** from mg-19ec. **Do not take 9 or 10 from me
either.** Specifically:

- **The RELAXED predicate is mine and it is a choice.** It relaxes exactly one conjunct. A
  different relaxation — attribution from the *section*, or a figure written `thirty-three` —
  gives a different population. Neither is tried here.
- **`s1`'s populations A–D are four choices out of many.** The one that matters is B; C and D
  exist so the liveness rule and the one-file scope cannot be mistaken for the reason a
  number is small.
- **`s5`'s FAULT/TARGET/OWNSCOPE regexes are mine, and they collected 10 sentences out of
  253.** A defect outside those regexes is invisible to them. That is stated in the
  transcript itself, and picking a different predicate is the obvious floor to audit.
- **`out_s3_bound_FIRSTFORM_exit1.txt` and `out_s5_own_criticism_FIRSTRUN_exit1.txt` are
  committed on purpose.** If either respecification looks like a check being loosened to go
  green, say so — the reasoning is at the point of each check in `s3_bound.py`, and it is
  meant to be arguable.
