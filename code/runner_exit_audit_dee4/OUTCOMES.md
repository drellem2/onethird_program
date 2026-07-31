# mg-dee4 — outcomes

Independent audit of `1ee1f1b` (mg-7522), the repair of the three open sites of
`682db2c` (mg-05eb). Every figure below is printed by a probe in this directory
next to the predicate that produced it; the transcripts are committed.

**The one-line verdict.** *The population really is a predicate now and the
census really is unpinned while the comparison keeps its pin — but the
retroactive clearance was read at the grain of LINES over source that executes
in LOOPS, and the repair's own `0 USES` is produced by a three-alternative rule
over a population that excludes every `.md`, which is where three of its
subject's four wrong artifacts were.*

---

## Findings

| id | probe | finding |
|---|---|---|
| **F1** | A2b | **`11 of 11 … read directly` is 11 LINES, not 11 statuses.** The 8 `\| tee` rows are derived from the runner's own bytes and are direct. The 3 `git diff` rows are a **hand-list of 3 argv containing 2 distinct commands**, over source lines that sit in `for` loops and execute **8** discarded `git diff`s at run time. The row labelled `state_delegation_audit_16eb/run_all.sh:39` runs a command **that is not on line 39** — line 39 carries a `':!*.md'` pathspec and the argv has none — so the `':!*.md'` form was never executed in any shape. A2c reads all 8 and they are **8 of 8 exit 0**: the verdict survives, the enumeration does not. |
| **F2** | A3d | **The published document's `154 changed files` matches no anchor.** `s4_unpin.py`'s own committed transcript prints **166** for the same measurement; `1ee1f1b` against the pin is **257**, `1ee1f1b^` is **240**, and the worktree-against-the-pin figure moves as the arc grows — `out_a3_anchor.txt` carries the live one. It is a bare prose figure in the section whose thesis is that anchors matter, in a document that states one commit later that *"a number that moves belongs in a transcript"* — a rule `c252f96` applied to the 2×2 totals **three paragraphs above this figure** and not to this one. |
| **F3** | A4a, A4b | **`0 USES` is a weaker claim than it reads.** `lib7522._STRENGTH` has **3** alternatives; `s3_figure.MARK`, the rule mg-7522 pointed at its subject, has **9**. **`verified` is named as one of the three markers in the D4 docstring, in the README and in the published document, and is not in the rule that produces the 0.** And the population is `MINE_PY + MINE_SH`: the README, `OUTCOMES.md`, `PREDICTIONS.md` and the published document are all outside it. mg-05eb's OPEN 2 was a figure wrong in four artifacts, **three of which are that excluded kind.** `out_s5_self.txt` states the extent; the README and the document print the 0 without it. |
| **F4** | A4d | **`S3a`'s CLAIM rule is LINE-LOCAL and the strongest claim wrapped.** A claim is a line carrying both a marker and a number. `OUTCOMES.md:88` carries *"verified against the"*, and its figure `0 / 0 / 0 / 0 / 2111 / 0` is on line 89 — neither line is a claim. Widening the window by ONE line takes **mg-c2b3's own artifacts from 20 to 24**, so *"20 strength-marked numeric claims, every one dispositioned"* is exact about the 20 the rule saw and silent about the four a hard wrap stepped over. |
| **F5** | A3c | **The repaired caller scan is still a NAME rule — with two names.** `k2_consume.py`'s target regex went from `run_all\.sh` to `(?:run_all\|run_audit)\.sh`. mg-7522's own library states the property (`\w+\.sh`) and its comment says the name rule *"is widened here to the property"* — **here** being the library, not the file it repaired. **9** executing sites at HEAD name a `*.sh` whose basename is neither, across 6 distinct target scripts, **4 of them reading the exit status**. The stated-limit comment mg-7522 added names the *literal-path* limit correctly and does not name this one. And **0 sites** at HEAD name `run_audit.sh`, so the widening it made is not exercised by anything in the arc. |
| **F6** | A1e | **A status-consuming pipeline outside the new population.** `code/branching_audit_a218/c0_repro.sh:47` — `COUNT=$(grep -o … \| tr -d ' ' \| tail -1)`. Both discarded stages can fail; the value reaches `BAD`, `BAD` reaches `exit 1`, and **9 sites in 3 files read that exit code**, 4 of them into a finding. It is outside P2 for exactly one reason: the file sets `-u` and not `-e`, and P2 tests consumption with **errexit only** — while mg-7522's written reason for pulling the three `git diff` lines in is about the **value** (*"`wc -c` reported 0, and the proof read `-> 0 bytes`"*), not about errexit. The two reasons agree on those three lines because those files happen to set `-e`. This is where they come apart. **The direction matters and is stated: a failing `grep` here makes the script report DISAGREES and exit 1 — fail-loud, not the silent green mg-c2b3 swept for.** A hole in the population; not a live swallow. |

**All three of mg-c2b3's rules miss F6 and each for a different reason** —
the NAME rule because the file is `c0_repro.sh`, the SHAPE rule because there
is no `tee`, and the PROPERTY rule because there is no `set -e`.

---

## Confirmations — what this audit re-derived and found sound

| id | probe | confirmation |
|---|---|---|
| **C1** | A1a | **All five of mg-7522's population figures re-derive identically** under a parser written from scratch: P0 **72**, P1 **23**/**53**, P2 **19**/**26**, shape **19**/**42**, name **17**/**34** at `bee07a1`. |
| **C2** | A1b, A1c | **Nothing outside `*.sh` in this repository.** 1 200-odd tracked files across 8 extensions, **0** with a shell shebang and no `.sh`; **428** tracked `*.py` walked as ASTs, **1** shell-executing call site, **3** literal strings reaching that shell, **0** of them a pipeline. The one whole-file over-read hit is a markdown cell terminator in a mutation payload and is dispositioned rather than tuned away. |
| **C3** | A1a | **At `1ee1f1b^` the property population is exactly the four files mg-7522 repaired** — `run_audit.sh` ×2 and the two `state_delegation` runners, 5 pipeline lines. At HEAD, **P2 is 0**. Nothing in the property population was left behind. |
| **C4** | A2c, A2d | **8 of 8** discarded `git diff` statuses exit 0 at the runtime grain, so the retroactive clearance's substance holds. And the `verified` byte-count claim **holds**: both arms run on the same 8 inputs, `0 / 0 / 0 / 0 / 2111 / 0` for `16eb` exactly as written, plus `0 / 0` for `0049` that the parenthesis does not list. |
| **C5** | A3a | **The moving-baseline defect is not reintroduced.** `CALLER_REF = None` for the census, `REF = L.TICKET_REF = bee07a1` for the classification, `changed_since(L.PINNED)` for the comparison. Read out of the source, not taken from the prose. |
| **C6** | A3b | **mg-7522's own F4, re-derived independently.** The literal-path column is **1 site pinned and 1 at HEAD** — the anchor alone moves nothing, which is what *"unpinning is necessary and not sufficient"* means. The `run_all.sh` exclusion, the EXEC widening and the target widening each move it by 0 as well. |
| **C7** | A5 | **The instrument mg-7522 edited under mg-05eb's citations still runs.** `k1_census.py`, `k2_consume.py`, `libc2b3.py` and `selftestc2b3.py` all exit 0 at HEAD; the `pipefail` row reads **ticket 1 / re-derived 1 / AGREES** live where the committed transcript reads **DIFFERS**; both rewritten runners exit 0 with **5 of 5** and **3 of 3** steps reached; forcing the first step of `f1b2` to fail gives **exit 1 with 0 of 4 later steps run**; and `git status --porcelain` is identical afterwards, so all 8 of those `out_*.txt` **regenerate byte for byte on this machine**. |

---

## Prediction misses, kept as written

**P4 — I predicted a hole in the corrected population and there is none.**
I predicted at least one P2 pipeline at the pin lying outside mg-7522's
"corrected population of 45". Measured: **0**. Every one of the 26 P2 pipelines
at `bee07a1` is either a `| tee` or one of the three `git diff` lines, so the
45 covers the property population entirely. The prediction was reasoning from a
gap between two numbers (53 pipelines, 42 tees) without checking whether the
difference was in P2. It was not.

**A defect in this instrument, recorded rather than smoothed away.** A5's first
draft measured *reach* — "did the later steps still run" — by looking for the
target script's **name in the runner's stdout**. The repaired runners send every
step's output to a file and `cat` it, so the name never reaches stdout: the
first run scored **0 of 5** and **0 of 3** steps reached on two runners that had
completed perfectly, and A5d's forced-failure check would have read *"0 later
steps ran"* as a PASS for the same wrong reason. Reach is now read from the
**mtime of each step's redirect target**. The lesson is mg-7522's own, one level
down: a check that reads a *form of output* rather than a *fact about the run*
will agree with you for the wrong reason.

**And a second one, caught by this audit's own finding.** The first draft of
`OUTCOMES.md`, the README and the published document each wrote *"`main` today
is 263"* into prose — the live worktree-against-the-pin figure. Between drafting
and the clean-tree run that produced the committed transcripts, this audit's own
twelve files landed and it became **275**. That is **F2 reproduced inside the
audit of F2**, and it is fixed the way `c252f96` fixed its neighbours: the three
anchors that are pinned to commits (`240`, `257`, `166`) stay in prose because
they cannot move, and the one that moves is now a pointer to
`out_a3_anchor.txt`. The number was wrong for the same reason mg-7522's was —
not carelessness, but a figure read once from a tree that then grew.

---

## What this audit did NOT check, named rather than folded into a total

* **mg-c2b3's own 34.** They are cited, not re-measured. `45 of 45` is, after
  this audit, *8 re-derived by me + 8 re-derived by me at the finer grain + 34
  inherited from a transcript I did not re-run.*
* **The 8-site positive control.** A5d is **1 site of the 8**, on one runner,
  and says so in its own output.
* **Whether the property predicate is the RIGHT one.** F6 argues its
  consumption clause is narrower than the reason given for it. That is a
  disagreement with a definition, not a measurement of one.
* **Every intermediate commit.** Everything here is read at HEAD, on one
  machine, inherited from mg-7522's own statement of the same limit.
