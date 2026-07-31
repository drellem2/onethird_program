# The population is a predicate — and the clearance is a line count

*Independent audit of `1ee1f1b` (mg-7522), the repair of the three open sites of
`682db2c` (mg-05eb), which audited the arc-wide `| tee` sweep `52aeaf4`
(mg-c2b3).*

Instrument: `code/runner_exit_audit_dee4/`. `sh run_all.sh`, about six minutes,
pure Python 3, no dependencies, no network. Written from scratch — it imports
none of `lib7522`, `libc2b3` or `lib05eb` for anything it measures, because two
of the three things mg-7522 repaired were defects **of a predicate** and an
audit that borrowed the repaired predicate could not disagree with it.

---

## The short version

mg-7522 replaced a population defined by a **filename** with one defined by a
**property**, re-derived the figure its subject had called *confirmed exactly*,
and unpinned a census while leaving a comparison pinned. **All three hold, and
the third holds exactly as the danger was posed:** the comparison still compares
against a fixed pre-repair ref.

Three things did not survive contact with an instrument built separately.

1. **The clearance is a LINE count over source that executes in LOOPS.**
2. **The strongest new claim is produced by a rule missing one of the three
   markers it names, over a population that excludes every `.md`.**
3. **One prose figure in the published document matches no anchor at all.**

And one thing is outside the new definition, found by looking rather than by
arguing.

---

## 1 — the population, checked by looking for something outside it

The ticket for this audit says: do not check the definition, find something
outside it. So the first thing is to establish that the definition's own
arithmetic is not in dispute. A parser written from scratch re-derives all five
of mg-7522's figures at `bee07a1`:

| predicate | mg-7522 | re-derived |
|---|---|---|
| P0 tracked `*.sh` | 72 | **72** |
| P1 …a real pipeline | 23 files / 53 pipelines | **23 / 53** |
| P2 …status consumed and discarded stage can fail | 19 / 26 | **19 / 26** |
| the SHAPE rule — a real `\| tee` | 19 / 42 | **19 / 42** |
| the NAME rule — a real `\| tee` in a `run_all.sh` | 17 / 34 | **17 / 34** |

Identical to the last row. And at `1ee1f1b^` — the tree immediately before the
repair — the property population is **exactly the four files mg-7522 repaired**,
five pipeline lines between them; at HEAD it is **0**. Nothing in the property
population was left behind.

**So where is the outside?** Three places were checked and two are empty.

* **Is `.sh` a name rule?** `lib7522.ls_sh()` takes no name argument, which
  mg-7522 correctly calls structural — but it still selects on the string
  `.sh`, and an extension is a naming convention exactly as `run_all` is. Every
  tracked file in the repository, whatever its extension, was read for a shell
  shebang. **0 shell scripts outside `*.sh`.** Established from `git ls-files`
  with no suffix filter and each file's own first line, not from a list of
  extensions someone thought of. `.sh` loses nothing *here*; it remains a name
  rule, and the next shell script committed without the extension is invisible.
* **Can the defect live in Python?** All **428** tracked `*.py` walked as ASTs
  — grepping for `shell=True` scores the sentence saying `shell=True` is never
  used, which mg-05eb recorded and mg-7522 hit again. **One** shell-executing
  call site in the repository, resolved one level through its wrapper: three
  literal strings reach that shell and **none is a pipeline**.
* **Inside `*.sh`, which clause of P2 drops what?** This is where it is.

### `set -e` is not the only consumer

P2 tests consumption with `has_set_e(file) and not guarded(line)` — **errexit,
at file grain**. But mg-7522's own written reason for pulling the three
`git diff … | wc -c | tr -d ' '` lines into the population is not about errexit:

> a `git diff` that failed produced an empty stream, `wc -c` reported `0`, and
> the proof read `-> 0 bytes`

That is a claim about the **value**. The two reasons agree on those three lines
because those two files happen to set `-e`. Here is where they come apart:

```sh
# code/branching_audit_a218/c0_repro.sh:47   —  the file sets `-u`, not `-e`
COUNT=$(grep -o '[0-9][0-9 ]*' "$WORK/out_selftest.txt" | tr -d ' ' | tail -1)
```

Both discarded stages can fail. `COUNT` is compared against `699520` twelve
lines later, the comparison drives `BAD`, `BAD` drives `[ "$BAD" -eq 0 ] || exit
1` — and that exit code is read at **9 sites across 3 files**, 4 of them into a
finding. The status is consumed in the strongest sense the arc uses.

**All three rules in the arc miss it, each for a different reason:** the NAME
rule because the file is `c0_repro.sh`; the SHAPE rule because there is no
`tee`; the PROPERTY rule because there is no `set -e`.

**The direction it fails in, stated rather than left to be assumed.** A failing
`grep` empties the stream, `COUNT` becomes empty, the script prints `DISAGREES`
and exits 1. That is fail-**loud**, not the silent green mg-c2b3 was sweeping
for. This is a hole in the population and, on today's bytes, not a live swallow.
Both halves are the finding.

*And a prediction that went the other way, kept as written:* I predicted at
least one P2 pipeline at the pin lying outside mg-7522's "corrected population
of 45". Measured **0** — every one of the 26 is either a `| tee` or one of the
three `git diff` lines. The 45 covers the property population entirely.

---

## 2 — the clearance: the verdict survives, the enumeration does not

> "the 11 discarded statuses read directly, 11 of 11 exit 0, so the corrected
> population of 45 has now been read in full"

Two different things are claimed there and they have different evidence.

**The 8 `| tee` rows are sound.** They are *derived* — from `tee_pipelines()`
over each runner's own pre-repair bytes and `invocation()` over each line — so
the row set cannot drift from the source, and the transcript carries a real exit
code and a real wall time for each. This is mg-c2b3's K3b method, unchanged, and
it is what *read directly* means.

**The 3 `git diff` rows are a hand-list, and the source lines sit in loops.**

| file | pipeline lines | argv listed | distinct commands | executions at run time |
|---|---|---|---|---|
| `state_delegation_audit_16eb/run_all.sh` | 2 | 2 | 2 | **6** |
| `state_delegation_repair_0049/run_all.sh` | 1 | 1 | 1 | **2** |

Three argv containing **two distinct commands** cover **four of eight**
executions by argv-identity. And one row is mislabelled: the entry written as

```
("code/state_delegation_audit_16eb/run_all.sh", 39,
 ["git", "diff", "3a80d99..HEAD", "--", "code/state_delegation_audit_5644"]),
```

names line 39, but line 39 is

```sh
nmd=$(git diff "$base..HEAD" -- "$dir" ':!*.md' | wc -c | tr -d ' ')
```

— the `nmd=` line, with a `':!*.md'` pathspec the argv does not have. That row
ran **line 38's second loop iteration under line 39's label**, and the
pathspec-excluding form of the pipeline **was never executed in any shape**.

**So the hole was filled rather than reported.** All eight runtime executions
were run here as list argv and their exit codes read: **8 of 8 exit 0**.
Nothing was being swallowed. The finding is about the word *directly* and about
the population — which is the whole subject of this ticket — and not about the
verdict.

**What remains unexamined, named rather than folded into a total.** mg-c2b3's
own 34 are cited, not re-measured. After this audit `45 of 45` is *sixteen
statuses re-derived here plus thirty-four inherited from a transcript nobody
re-ran.* And everything here is read at HEAD, on one machine — mg-7522 states
that limit for itself and it is inherited unchanged.

---

## 3 — the anchor: not reintroduced, and one figure that moved

The danger the ticket poses is precise: *a repair that unpins BOTH has
reintroduced the moving-baseline defect the pin was added to fix.* Read out of
the source rather than out of the prose:

| file | anchor | present | question it serves |
|---|---|---|---|
| `k2_consume.py` | `CALLER_REF = None` | yes | **census** |
| `k2_consume.py` | `REF = L.TICKET_REF` | yes | **comparison** |
| `libc2b3.py` | `TICKET_REF = "bee07a1"` | yes | the pin itself |
| `s4_unpin.py` | `changed_since(L.PINNED)` | yes | **comparison** |
| `s4_unpin.py` | `changed_since(None)` | yes | its HEAD side, 0 by construction |

**The comparison still compares against a fixed pre-repair ref.** The document
names which anchor serves which purpose, in `k2_consume.py`'s own comment block
and in S4e's anchor inventory.

### the pre-repair predicate, against the same inputs

mg-7522 changed four things in one scan — the anchor, the file filter, the
`EXEC` regex and the target regex. Run one at a time over the same HEAD bytes:

| rule | sites | reading the status |
|---|---|---|
| pre-repair, as mg-c2b3 ran it (pinned) | 1 | 1 |
| pre-repair rule, HEAD bytes — the ANCHOR alone | 1 | 1 |
| …and the `run_all.sh` exclusion dropped | 1 | 1 |
| …and the `EXEC` regex widened | 1 | 1 |
| repaired, as it stands | 1 | 1 |

**The anchor alone moves nothing.** That is not a negative result — it is
mg-7522's own F4, re-derived by a separate instrument. Its README states the
literal-path column as `1 site` at the pin and `1 site` at HEAD, and *unpinning
is necessary and not sufficient* is precisely what a 1 → 1 says.

### two things the section does not carry

**The repaired target rule is still a name rule, with two names.** It went from
`run_all\.sh` to `(?:run_all|run_audit)\.sh`. mg-7522's own library states the
property — *"an executable source that runs a shell script"*, `(\w+\.sh)` — and
its comment says both name rules are *"widened here to the property"*: **here**
being the library, not the file it was repairing. At HEAD, **9 executing sites
name a `*.sh` whose basename is neither**, across 6 distinct target scripts,
**4 of them reading the exit status** — three of those four being the
`c0_repro.sh` of section 1. And **0 sites name `run_audit.sh`**, so the widening
mg-7522 made is not exercised by anything in the arc. The stated-limit comment
it added names the *literal-path* limit, correctly and usefully, and does not
name this one.

**And the published figure matches no anchor.** The document says:

> anchored to the pin the byte-comparison sees **154 changed files**

`s4_unpin.py` computes that with `git diff --name-only <ref> --`. Re-derived:

| anchor | files changed |
|---|---|
| `1ee1f1b^` against the pin | 240 |
| `1ee1f1b` against the pin | 257 |
| `main` today against the pin | *moves; `out_a3_anchor.txt` carries the live one* |
| **mg-7522's own committed transcript** | **166** |
| **the published document** | **154** |

This is section 2's defect inside section 3's document: a reader-facing artifact
carrying a number its own instrument's transcript disagrees with. And the rule
was already written down — one commit later, `c252f96` converted the moving
counts in this document to transcript pointers with the note *"a number that
moves belongs in a transcript"*, and applied it to the 2×2 totals **three
paragraphs above this figure**.

**What is not wrong, so the finding is not read wider than it is:** the claim
the figure supports — that the pinned side is more informative than the HEAD
side — holds at every anchor above, and `s4_unpin.py` asserts the *inequality*
rather than the number.

---

## 4 — the strongest wording, checked first

mg-7522 states the general form three times and it is right:

> "Confirmed exactly", "verified", "byte-identical" and their relatives mark the
> place where the author stopped looking. They are a reason to check FIRST.

It then applies that form to its subject with one rule and to itself with
another.

| | the rule for the SUBJECT | the rule for ITSELF |
|---|---|---|
| where | `s3_figure.MARK` | `lib7522._STRENGTH` |
| alternatives | **9** | **3** |
| `confirmed exactly` | yes | yes |
| `byte-identical` | yes | yes |
| **`verified`** | **yes** | **no** |
| population | every artifact of `52aeaf4`, `.md` included | `MINE_PY + MINE_SH` |

**`verified` is named as one of the three markers in `s5_self.py`'s own D4
docstring, in the README and in the published document — and is not in the rule
that produces the `0 USES` those documents print.** The population excludes the
tree's `README.md`, `OUTCOMES.md`, `PREDICTIONS.md` and the published document:
mg-05eb's OPEN 2 was a figure wrong in four artifacts, and **three of the four
are that excluded kind.**

`out_s5_self.txt` states the extent honestly — *"over this tree's 8 `*.py` and 1
`*.sh` files only … it does not range over the rest of the repository"*. The
README and the published document print the **0** without it. That is mg-7522's
own **F3**, roles unchanged: the instrument was right and the summary dropped
its scope.

### the claim rule is line-local, and the strongest claim wrapped

`s3_figure.py` scores a CLAIM as a **line** carrying both a marker and a number.
In a hard-wrapped paragraph the marker and its figure land on different lines:

```
OUTCOMES.md:88   `wc -c < FILE` counts the same bytes the pipeline did, verified against the
OUTCOMES.md:89   pre-repair output (`0 / 0 / 0 / 0 / 2111 / 0`, unchanged).
```

Neither line is a claim. Widening the window by **one line** takes **mg-c2b3's
own artifacts from 20 claims to 24** — so *"20 strength-marked numeric claims,
every one dispositioned"* is exact about the twenty the rule saw and silent
about the four a hard wrap stepped over.

### and then the thing the word was standing in for

No probe in mg-7522's tree computes a byte count, and the figure `2111` appears
in none of its six committed transcripts. So both arms were run here on the same
eight inputs — the pre-repair pipeline `git diff … | wc -c | tr -d ' '`, and the
post-repair `git diff … > FILE; wc -c < FILE`:

```
state_delegation_audit_16eb   0 / 0 / 0 / 0 / 2111 / 0     pre == post, 6 of 6
state_delegation_repair_0049  0 / 0                        pre == post, 2 of 2
```

**The claim holds.** `verified` was checkable, was not checked by its author,
and turned out true. That outcome is what makes this reportable rather than
damning — and the parenthesis lists six of the eight, which is the same shape as
`11 of 11` covering four.

---

## The floor — one thing no list in the ticket names

**mg-7522 edited the instrument mg-05eb cites and deliberately did not re-run
it.** The decision is right and is stated three times: a transcript is the
record of a run at a time, and rewriting `out_k1_census.txt` would destroy
mg-05eb's citations of it.

The side effect nobody asks about is that `libc2b3.py`, `k1_census.py`,
`k2_consume.py`, `selftestc2b3.py` and 63 rewritten lines of shell now have **no
current record**, so a break in them is silent. They were run:

* all four probes exit **0** at HEAD against the repaired library;
* both rewritten runners exit **0**, with **5 of 5** and **3 of 3** steps
  reached — reach read from the mtime of each step's redirect target, because
  the repaired shape sends every step's output to a file;
* forcing the first step of `run_audit.sh` to fail gives **exit 1 with 0 of 4
  later steps run** — non-zero **and** stopped, one site of the eight, and the
  narrowing is printed;
* `git status --porcelain` is identical afterwards, so all eight of those
  `out_*.txt` **regenerate byte for byte on this machine**;
* and the row at the heart of OPEN 2 now reads, in a live run of the subject's
  own instrument:

```
committed transcript : setting pipefail   ticket 1   re-derived 0   DIFFERS
live run at HEAD     : setting pipefail   ticket 1   re-derived 1   AGREES
```

That is the strongest confirmation available for OPEN 2, and it is positive.

---

## This audit, checked for the defects it audits

`selftestdee4.py` drives every rule in both senses and then turns the four
defects on this tree's own bytes. Two are worth naming because they are the
opposite of mg-7522's answers, deliberately:

* **`ls_tracked()` DOES take a name filter.** mg-7522's structural answer — a
  primitive with no name argument — is a good one, and it makes section 1's own
  question unaskable: a primitive that hard-codes `.sh` cannot be pointed at
  everything to find out whether `.sh` is a name rule. So the obligation here is
  **enumeration, not absence**: every call site that names a file kind is listed
  with a disposition, coverage checked both ways.
* **There is one deliberate `/bin/sh -c`,** in the byte-count probe, because
  reproducing the pre-repair *pipeline* is the measurement. It is declared in
  the self-test rather than hidden behind a rule that would not see it.

And one defect in this instrument, recorded rather than smoothed away: the
first draft of the floor probe measured *reach* by looking for a step's script
name in the runner's **stdout**. The repaired runners redirect every step to a
file, so the name never reaches stdout — the first run scored **0 of 5** and
**0 of 3** steps reached on two runners that had completed perfectly, and the
forced-failure check would have read *"0 later steps ran"* as a PASS for exactly
the wrong reason. It is mg-7522's own lesson one level down: a check that reads
a **form of output** rather than a **fact about the run** will agree with you
for the wrong reason.

**And a second one, caught by this audit's own F2.** The first draft of this
document wrote *"`main` today against the pin | 263"* into the table above.
Between that draft and the clean-tree run that produced the committed
transcripts, this audit's own twelve files landed and the figure became **275**.
That is section 3's finding reproduced inside the section that reports it. The
three anchors pinned to commits — `240`, `257`, `166` — stay in prose because
they cannot move; the one that moves is now a pointer to `out_a3_anchor.txt`.
mg-7522's `154` was wrong for the same reason, which is worth saying plainly:
not carelessness, but a figure read once from a tree that then grew.

**What cannot be checked here, stated rather than omitted:** whether P2 is the
*right* predicate. Section 1 argues its consumption clause is narrower than the
reason mg-7522 itself gives for it, and names one file where that bites. That is
a disagreement with a definition — which is the only useful thing to have about
one, and mg-7522 wrote its predicate out in full precisely so that disagreeing
would be possible.
