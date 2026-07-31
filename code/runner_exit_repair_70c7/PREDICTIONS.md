# mg-70c7 — predictions, written BEFORE any probe in this directory was run

The six findings of `mg-dee4` against `1ee1f1b` (mg-7522), repaired. Every number
below was written from reading the sources and mg-dee4's transcripts, before
`run_all.sh` existed in this tree. Misses are kept, not corrected into hits.

The commit that carries this file carries **no probe and no transcript**, so the
order is checkable from `git log` rather than asserted here.

---

## R1 — F1, the grain of the retroactive clearance

| id | prediction |
|---|---|
| **R1a** | The 3 `git diff` pipeline lines mg-7522 hand-listed can be **derived** from the two runners' own bytes at `1ee1f1b^` — the `for pair in …` header expands to a literal `(base, dir)` list on every one of them, so no argv needs to be written by hand. |
| **R1b** | The derived execution count is **8** discarded `git diff` invocations: `state_delegation_audit_16eb` 3 pairs × 2 pipeline lines = 6, `state_delegation_repair_0049` 2 pairs × 1 line = 2. |
| **R1c** | Of those 8, **4** are argv mg-7522 never ran, and the `':!*.md'` form of `16eb:39` is never run in any shape by its hand-list. |
| **R1d** | All 8 exit **0**, so the substance of `11 of 11` survives and only its arithmetic does not. |
| **R1e** | The corrected total at the execution grain is **16** discarded statuses read directly here — 8 `\| tee` + 8 `git diff` — and the sentence that replaces `11 of 11` states which grain it is at. |
| **R1f** | mg-7522's four reader-facing artifacts (`README.md`, `OUTCOMES.md`, `s2_status.py`, the published document) all carry the line-grain figure; **4 of 4** need the sentence changed. |

## R2 — F2, the figure with no anchor

| id | prediction |
|---|---|
| **R2a** | No anchor reproduces **154**. Predicted readings: `s4_unpin`'s own transcript **166**; the same measurement live at my run **larger than 275**, because mg-dee4 measured 275 on a clean tree and twelve more files have landed since. |
| **R2b** | After the repair the string `154` does not appear as a figure anywhere in the published document, and the sentence points at `out_s4_unpin.txt`. |
| **R2c** | A census of every number in the published document against mg-7522's own committed transcripts will find **more than one** figure that no transcript reproduces — `154` is unlikely to be alone, because nothing in that tree was checking for it. I predict **between 2 and 8** such figures, each of which is then either pointed at a transcript or dispositioned by hand with its reason. |

## R3 — F3, the rule it applied to itself

| id | prediction |
|---|---|
| **R3a** | `lib7522._STRENGTH` has **3** alternatives and `s3_figure.MARK` has **9**; `verified` is in the 9 and not in the 3, and it is named in the D4 docstring, in `README.md` and in the published document. |
| **R3b** | Under the 9-alternative rule, over the **unchanged** `MINE_PY + MINE_SH` population, D4 stops reading `0 USES`. I predict **at least 5** USEs appear, all of them in probe prose that prints a figure it computed in the same run. |
| **R3c** | So the repaired D4 must distinguish a marker that stands in for a check from one that stands beside it: a USE is **BACKED** when every number on its line is reproduced by a transcript this tree commits, and **UNBACKED** otherwise. I predict the repaired rule finds **0 UNBACKED** in `MINE_PY + MINE_SH`. |
| **R3d** | Widening the D4 population to this tree's `*.md` and the published document adds **3** artifacts (`README.md`, `OUTCOMES.md`, `PREDICTIONS.md`) plus the document, and I predict it finds **at least 1 UNBACKED** use among them — because that is exactly the kind mg-05eb's OPEN 2 was, three of its four wrong artifacts being of it. |

## R4 — F4, the line-local claim rule

| id | prediction |
|---|---|
| **R4a** | `S3a`'s CLAIM rule requires a marker and a number **on the same line**. Widening the window to the line and the one after it takes mg-c2b3's artifacts from **20 to 24** claims. |
| **R4b** | The 4 new claims include `code/runner_exit_c2b3/OUTCOMES.md:88`, whose marker is `verified against the` and whose figure `0 / 0 / 0 / 0 / 2111 / 0` is on line 89. |
| **R4c** | Every one of the 4 is dispositioned, and I predict **0** of them is WRONG — mg-dee4's A2d re-derived the `16eb` byte counts on both arms and they hold. |

## R5 — F5, the caller scan that is still a name rule

| id | prediction |
|---|---|
| **R5a** | At HEAD, `k2_consume.py`'s two-name rule misses **9** executing sites naming a `*.sh` whose basename is neither `run_all.sh` nor `run_audit.sh`, **4** of them reading the status. |
| **R5b** | **0** sites at HEAD name `run_audit.sh`, so the widening mg-7522 made is not exercised by anything in the arc. |
| **R5c** | Replacing the name list with the property — an executing site naming **any** `*.sh` under a tree directory — leaves `k2_consume.py`'s existing rows unchanged and adds those 9, so `out_k2_consume.txt` must be regenerated. I predict the previously-printed rows are a **subset** of the new ones, i.e. the widening removes nothing. |

## R6 — F6, the population hole

| id | prediction |
|---|---|
| **R6a** | P2's consumption test is errexit at file grain; mg-7522's written reason is about the **value**. Making consumption a named disjunction — errexit **or** the pipeline's output captured into a variable that is read elsewhere in the file — pulls `code/branching_audit_a218/c0_repro.sh:47` in. |
| **R6b** | Both arms are true of all three `git diff` lines, so the widening **changes nothing** about mg-7522's own three, which is why the two reasons looked the same. |
| **R6c** | At `bee07a1` the widened P2 grows from **19 files / 26 pipelines**. I predict the new figure is between **21/29** and **28/40**. |
| **R6d** | At HEAD the widened P2 is **not 0** — mg-7522's repair drove errexit-P2 to 0, and the value arm was never repaired against. I predict **at least 2** files. |
| **R6e** | Every discarded status of the new members, read directly, exits **0** — the direction of `c0_repro.sh` is fail-loud, and a hole in a population is not the same thing as a live swallow. |

## What this deliverable owes itself

mg-dee4 closes on *"this deliverable is of the same kind as the defect it
repairs."* So does this one. **R7**, predicted here and checked in `r6_self.py`:

| id | prediction |
|---|---|
| **R7a** | This tree's own `run_all.sh` is outside the **widened** P2 as well as the errexit one: 0 pipelines of any kind. |
| **R7b** | Every count this tree prints that ranges over source lines states whether it is a **site** count or an **execution** count, and `r6_self.py` checks that mechanically over its own transcripts. I predict the first draft fails this on at least one line of my own — the grain defect is the easiest one in this arc to reproduce. |
| **R7c** | Every number in this tree's own `README.md`, `OUTCOMES.md` and published document is reproduced by one of this tree's transcripts or dispositioned — the same census R2c runs on mg-7522's document, run on mine. I predict **0 undispositioned**. |
