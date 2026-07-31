# mg-7522 — outcomes

## Predictions

| | prediction | result |
|---|---|---|
| **Q1** | `*.sh` at `bee07a1`: 72 | **HIT** (inherited from mg-05eb, re-derived here) |
| **Q2** | named `run_all.sh`: 64 | **HIT** (inherited) |
| **Q3** | real `\| tee`: 19 files / 42 pipelines | **HIT** (inherited) |
| **Q4** | of those, in `run_all.sh`: 17 / 34 | **HIT** (inherited) |
| **Q5** | outside the name rule: 2 files / 8 pipelines | **HIT** (inherited) |
| **Q6** | P2 at `bee07a1`: 19 files / 26 lines | **MEASURED FIRST — not scored.** mg-70c7 widened the consumption clause and the same predicate now reads **20 / 27**; the errexit arm alone still reads 19 / 26 and both rows are printed |
| **Q7** | name-missed and shape-missed sets are disjoint and neither empty | **HIT** — 2 files/8 lines and 2 files/3 lines |
| **Q8** | P2 at HEAD after this repair: 0 / 0 | **HIT for the errexit arm.** Under the widened clause it is **1 / 1** — `code/branching_audit_a218/c0_repro.sh:47`, dispositioned in `out_s1_population.txt` with its failure direction measured in `code/runner_exit_repair_70c7/out_r5_population.txt` |
| **Q9** | `*.sh` at HEAD > 72 | **HIT** — see `out_s1_population.txt`; the number moves as the arc grows, which is the point of the row |
| **Q10** | all 11 discarded statuses exit 0 | **HIT AT THE WRONG GRAIN, corrected by mg-70c7.** The 11 are SOURCE LINES; three of them sit in `for` loops and are 8 executions, so the population is **16 executions** — 8 `\| tee` + 8 `git diff`. All 16 exit 0. `out_s2_status.txt` |
| **Q11** | PRE-repair control: 8 of 8 SWALLOW | **HIT** |
| **Q12** | repaired control: 8 of 8 CAUGHT | **HIT** |
| **Q13** | 0 committed transcripts move | **HIT** |
| **Q14** | 0 of 8 pre-repair sites exit non-zero for an unrelated later reason | **HIT** — see below |
| **Q15** | `pipefail` under mg-c2b3's regex: 0 | **MEASURED FIRST — not scored** |
| **Q16** | under the repaired regex: 1 | **MEASURED FIRST — not scored** |
| **Q17** | `#!/bin/sh` on 59 of 64 | **MEASURED FIRST — not scored** |
| **Q18** | 10–20 strength-marked numeric claims | **HIT under a LINE-LOCAL rule** — 20. With the one-line window mg-70c7 gave it (mg-dee4/F4) the same population is **24**, and the prediction's range would have missed |
| **Q19** | 4 of them wrong | **MISS — 5** |
| **Q20** | 4700 appears in exactly one 2×2 cell | **HIT** — (HEAD, runtime-path) |
| **Q21** | unpinning alone is not sufficient | **HIT** |
| **Q22** | the pinned comparison sees strictly more | **HIT** — the two counts are in `out_s4_unpin.txt`, `S4c`. The figure `154` stood here and no anchor reproduces it (mg-dee4/F2); the pinned side moves as the arc grows and belongs in a transcript |
| **Q23** | `out_q2_wiring.txt` has 2 `SWALLOWED` rows | **MISS — 3** |
| **Q24** | this tree's runner: 0 pipelines, every step guarded | **HIT** — 0, 6 of 6 |
| **Q25** | 0 real `shell=True` / `os.system(` | **HIT** |
| **Q26** | 0 USES of a strength marker, MENTIONs > 0 | **HIT UNDER A DIFFERENT INSTRUMENT than the one this tree pointed at its subject** (mg-dee4/F3): 3 alternatives here against 9 there, over a population that excluded every `.md`. Re-run with the one shared rule and the `.md` included, `out_s5_self.txt` carries MENTIONs, BACKED uses, uses with no figure, and UNBACKED |

**Q19, kept as written.** I predicted **4** wrong figures and the probe
dispositions **5**. The one I did not predict is `OUTCOMES.md`'s own `pipefail`
row, which reads `AGREES` for a number the same tree's committed transcript
marks `DIFFERS`. mg-05eb named *"four reader-facing artifacts"* saying
*"confirmed exactly"*; `OUTCOMES.md` said `AGREES` instead, so it fell outside
the phrase and I inherited the boundary along with the count. **The miss is an
instance of the finding it was predicting** — I keyed on a form of words.

**Q23, kept as written.** I predicted *"2 `SWALLOWED` rows"* and the probe
measures **3 lines containing the word**. Two are the claim rows —
`species_repair_a4ef` and `species_remainder_f8fa`, both affected runners — and
the third is the section header `Q2e A RED SELF-TEST, SWALLOWED`. The
substance is right and the count is not, and the reason is exactly this arc's
recurring one: **I predicted a number of CLAIMS and the instrument counted a
number of MENTIONS.** It is left as a miss because the disagreement is more
instructive than a corrected prediction would be.

**Q14, and why it is worth a row.** At all 8 pre-repair sites the runner exits
**0**, so the exit-code column alone would have been sufficient *here*. It was
not sufficient for mg-c2b3: at 8 of its 34 sites the pre-repair runner exits 1
for an unrelated downstream `grep`, and an exit-code-only control would have
called those eight healthy. The conjunction is kept because it is the rule that
is right in both populations, not because it changed a verdict in this one.
**A control that only fires where it is needed cannot be checked where it is
not.**

---

## Findings

| | finding | class |
|---|---|---|
| **F1** | the population was a filename; 2 runners with 8 `\| tee` pipelines were still swallowing at HEAD after the sweep | population definition — MAJOR |
| **F2** | the population was *also* a shape; 3 more pipelines throw a status away without using `\| tee`, in files that **are** named `run_all.sh` | population definition — MAJOR, and **not named by mg-05eb** |
| **F3** | the one figure called "confirmed exactly" was wrong, and so is *"the shebang is `#!/bin/sh` on all 64 runners (measured)"* | summary-vs-rows |
| **F4** | unpinning the caller scan is **necessary and not sufficient** — the pin and a line-local literal-path rule are two independent reasons the same site was outside the enumeration | enumeration — the ticket's remedy is half of the fix |

### F2 — the shape rule missed what the name rule did not

`code/state_delegation_audit_16eb/run_all.sh:38,39` and
`code/state_delegation_repair_0049/run_all.sh:39` are

```sh
n=$(git diff "$base..HEAD" -- "$dir" | wc -c | tr -d ' ')
```

under `set -e`, printed beneath *"THE PREDECESSOR DIRECTORIES ARE UNMODIFIED —
proof, not assertion"*. The pipeline's status is `tr`'s. A `git diff` that
failed produced an empty stream, `wc -c` reported `0`, and the proof read
`-> 0 bytes`. **Both of mg-c2b3's rules missed this**: the file is named
`run_all.sh` so the name rule contained it, and the line has no `| tee` so the
shape rule dropped it. Only the property finds it.

The repair reads `git diff`'s own status and keeps the byte counts identical —
`wc -c < FILE` counts the same bytes the pipeline did, verified against the
pre-repair output (`0 / 0 / 0 / 0 / 2111 / 0`, unchanged): **that word now
stands next to a computation.** `S2a2` runs both mechanisms — the stream length
`| wc -c` reported and the file size `wc -c < FILE` reports — over all **8**
derived executions and prints every value, including the two of
`state_delegation_repair_0049` that this parenthesis does not list. Until
mg-70c7 no probe in this tree computed a byte count and the figure stood on the
word `verified`; `mg-dee4`'s A2d ran both arms and the claim **held**, which is
what makes it reportable rather than damning.

### F4 — the 2×2

`code/species_depth_audit_4700/` is found in exactly one of four cells:

| | literal path only | + runtime path |
|---|---|---|
| **pinned `bee07a1`** | not found | not found |
| **HEAD, unpinned** | not found | **FOUND — 8 sites, 5 reading the status** |

mg-05eb's diagnosis — *"it could not have been [in the enumeration]: the caller
scan runs at the pinned `bee07a1`, and that tree landed after the pin"* — is
**true and incomplete**. Unpin the scan and it is still invisible, because
`run_runner(t)` and `subprocess.run(["sh", "run_all.sh"], cwd=d)` carry no
literal `<tree>/run_all.sh` on the executing line. The anchor fix belongs in
mg-c2b3's scan and is made there; the rule fix is measured here and named as a
**stated limit inside `k2_consume.py`**, because a limit that is written down is
checkable and an absence is not.

---

## Three defects in this instrument, recorded rather than smoothed away

All three are the **same** defect, and it is the one this arc keeps finding: **a
mention counted as an occurrence.** All three were in the instrument built to
find it, and all three were caught by this tree's own self-test rather than by a
reader.

1. **The `shell=True` check was a grep, and matched the sentence saying
   `shell=True` is never used.** It reported 4 of this tree's 8 Python files as
   violations — `lib7522.py`, `s2_status.py`, `s5_self.py`, `selftest7522.py` —
   every one of them on a line *asserting the absence of the thing*. mg-05eb
   recorded this exact defect in its own self-test and I reproduced it.
   **Replaced by an AST walk** (`lib7522.shell_true_sites`), which cannot
   mistake a docstring for a call. Strictly harder than the rule it replaces.

2. **The "`ls_sh` contains no runner-filename literal" check read the
   docstring.** `ls_sh`'s docstring names `run_all.sh` on purpose — it explains
   why there is no name rule — and the check would have forced the explanation
   to be deleted to pass. **Replaced by `lib7522.function_code`**, which returns
   the function body with the docstring removed.

3. **The strength-marker check counted its own detecting regex.** It reported 15
   violations, of which every one was a regex literal, a quotation of mg-c2b3's
   wording, or the sentence saying the marker must not be used.
   **Replaced by a MENTION/USE rule**: a marker written inside quotes,
   backticks or emphasis is being *named*; written bare and applied to a figure
   it is being *used*. That is the same distinction as *"a comment quoting
   `| tee` is not a pipeline"*, one level up, and this tree needed it for the
   same reason its subjects did.

   One consequence is listed in the open rather than special-cased: the rule's
   own worked example in `lib7522.py` is a bare use by construction, so the
   labels `<- USE` / `<- MENTION` are in `_MENTION_SIGNALS`. A line that
   declares itself an illustration is not an assertion.

**All three were greps for a form of words.** The repaired versions are
structural in two cases (an AST walk, a docstring-stripped body) and an explicit
stated rule in the third. That is the pattern worth keeping: **when a check for
a form of words fails on its own documentation, the fix is usually not a better
pattern but a different kind of question.**

---

## What was checked, and what honestly cannot exhibit the defect

`s5_self.py` prints this list live; it is repeated here because a reader of the
prose should not have to run the tree to see it.

| defect | branch | verdict and reason |
|---|---|---|
| D1 name-defined population | `lib7522.ls_sh()` | **cannot** — the signature is `(ref=None)`; no name parameter exists to filter with |
| D1 | the 9 filter sites in `s1`/`s3` | **checked** — every one is the sweep's own rule being measured next to the property rule |
| D2 stale anchor | `s5_self.py` | **cannot** — it reads only the current world; a pinned answer would be about a tree that no longer exists |
| D2 | every other probe | **checked** — every anchor listed with which question it serves; population primitives default to `ref=None` |
| D3 discarded status | this tree's Python | **cannot** — list argv, no shell, no pipeline; `returncode` read on every path including the timeout, which prints `-` not `0` |
| D3 | `selftest7522.py`'s fixtures | **cannot** — they are strings parsed by the rules, never executed, so no status exists |
| D3 | this tree's `run_all.sh` | **checked** — 0 pipelines under S1's own P2 predicate, 6 of 6 steps redirect and guard |
| D4 strength marker | every figure | **checked** — one rule (`lib7522.MARK`, 9 alternatives) in both directions, over this tree's `*.py`, `*.sh`, `*.md` and the published document; a USE is BACKED when every figure on its line is printed by a transcript of this tree, and only UNBACKED is counted. `out_s5_self.txt` |

**Not checked, stated rather than omitted.** That the property predicate is the
*right* one. It is written out in full in `lib7522.pipelines`,
`discarded_stages`, `guarded` and `stage_can_fail` so that disagreeing with it
is possible. A predicate nobody can disagree with is not a definition.

Also not checked: `code/runner_exit_c2b3/`'s committed transcripts are **not**
regenerated, so `out_k1_census.txt` still shows the pre-repair regex's `DIFFERS`
row. That is deliberate — it is the record of the run that produced the sweep's
commit and mg-05eb cites it — and it is stated in `k1_census.py`'s docstring,
in the sweep's `README.md`, and in `s3_figure.py`'s S3e rather than left for a
reader to trip over.
