# `code/runner_exit_audit_dee4` — the independent audit of mg-7522

`sh run_all.sh` — about 6 minutes, pure Python 3, no dependencies, no network.

**Target:** `1ee1f1b` (mg-7522), the repair of the three open sites of
`682db2c` (mg-05eb), which was itself the independent audit of the arc-wide
`| tee` sweep `52aeaf4` (mg-c2b3).

**Written from scratch.** `libdee4.py` does not import `lib7522`, `libc2b3` or
`lib05eb` for anything it measures. Two of the three things mg-7522 repaired
were defects **of a predicate**, so an audit that borrowed the repaired
predicate could not disagree with it about the thing that might still be wrong.
Where a probe deliberately runs *mg-7522's own rule* — to turn a rule it aimed
at its subject back on itself, or to run the pre-repair form against the same
inputs — it says so in its printed output.

## What is here

| file | what it answers |
|---|---|
| `PREDICTIONS.md` | every count, with **when it was written**: PREDICTED, INHERITED, or MEASURED FIRST — and the predicted exit code of every probe |
| `selftestdee4.py` | every rule in **both senses**, and this tree checked for the four defects it audits, over `*.py`, `*.sh` **and `*.md`** |
| `a1_outside.py` | **the population, checked by looking for something OUTSIDE it** |
| `a2_direct.py` | **were the statuses read DIRECTLY, and at what grain** |
| `a3_anchor.py` | **the pin** — unpinned for the census, still pinned for the comparison? |
| `a4_superlatives.py` | **the repair's own strongest wording, checked first** |
| `a5_floor.py` | the floor: **the instrument mg-7522 edited under mg-05eb's citations, run** |
| `OUTCOMES.md` | six findings, seven confirmations, the prediction miss and one defect in this instrument |

## Verdict in one line

**The population really is a predicate and it covers everything in this
repository; the census really is unpinned while the comparison keeps its pin.
But the retroactive clearance was read at the grain of LINES over source that
executes in LOOPS — 3 hand-listed argv, 2 distinct commands, for 8 runtime
statuses — and the repair's own `0 USES` comes from a three-alternative rule,
missing the `verified` it names itself, over a population that excludes every
`.md`, which is where three of its subject's four wrong artifacts were.**

## The four targets, and what each returned

### 1 — the population: **nothing outside it in this repository, and one thing outside the predicate**

`A1a` re-derives all five of mg-7522's figures under an independent parser and
gets **72 / 23 / 53 / 19 / 26 / 19 / 42 / 17 / 34** — identical, to the last row.
So the check is not the definition; it is what the definition cannot reach.

* `A1b` — **is `.sh` itself a name rule?** Every tracked file, whatever its
  extension, read for a shell shebang. **0** shell scripts outside `*.sh`.
  Established from `git ls-files` with no suffix filter and the file's own
  first line, not from a list of extensions I thought of.
* `A1c` — **can the defect live in Python?** All **428** tracked `*.py` walked
  as ASTs. **1** shell-executing call site, resolved one level through its
  wrapper: **3** literal strings reach that shell and **0** are pipelines.
* `A1d`/`A1e` — **which clause of P2 drops what.** P2 tests consumption with
  `has_set_e(file) and not guarded(line)` — **errexit, at file grain**. But
  mg-7522's own written reason for pulling the three `git diff` lines in is
  about the **value**: *"a `git diff` that failed produced an empty stream,
  `wc -c` reported 0, and the proof read `-> 0 bytes`."* The two agree on those
  three lines only because those files set `-e`. **`code/branching_audit_a218/
  c0_repro.sh:47` is where they come apart** — a three-stage pipeline whose
  discarded `grep` and `tr` can fail, whose value drives `BAD`, whose `BAD`
  drives `exit 1`, and whose exit code is read at **9 sites in 3 files**. All
  three rules in the arc miss it, each for a different reason. Its failure
  direction is **loud**, and that is printed too.

### 2 — the clearance: **the verdict survives, the enumeration does not**

The 8 `| tee` rows are **derived** from `tee_pipelines(pre)` and `invocation()`
over the runners' own pre-repair bytes; the transcript carries a real exit code
and a real wall time for each. That half is sound.

The 3 `git diff` rows are a **hand-list**, and all three source lines sit inside
`for` loops:

| | lines | argv mg-7522 ran | distinct commands | runtime executions |
|---|---|---|---|---|
| `state_delegation_audit_16eb` | 2 | 2 | 2 | **6** |
| `state_delegation_repair_0049` | 1 | 1 | 1 | **2** |

and the row labelled `…16eb/run_all.sh:39` runs a command **that is not on line
39**: line 39 is the `nmd=` line with a `':!*.md'` pathspec and the argv has
none. **The `':!*.md'` form was never executed in any shape.** `A2c` executes
all 8 and reads **8 of 8 exit 0** — so the clearance's substance is fine and
the word *directly* is doing more work than the evidence under it.

What remains **unexamined and is named as such**: mg-c2b3's own 34 are cited,
not re-measured, so `45 of 45` is 16 statuses re-derived here plus 34 inherited.

### 3 — the pin: **not reintroduced**

Read out of the source rather than out of the prose: `CALLER_REF = None` is the
census, `REF = L.TICKET_REF = bee07a1` is the classification, and
`changed_since(L.PINNED)` is the comparison. **The comparison still compares
against a fixed pre-repair ref.**

`A3b` runs the pre-repair predicate against the same inputs, one change at a
time, and re-derives mg-7522's own 2×2 left column: **1 site pinned, 1 at HEAD**.
The anchor alone moves nothing — which is exactly what *"unpinning is necessary
and not sufficient"* means, now measured by two independent instruments.

Two things the section does not carry: the repaired target regex is **still a
name rule with two names** (9 executing sites at HEAD outside it, 4 reading the
status, and **0** sites naming the `run_audit.sh` it added); and the published
figure **`154 changed files`** matches **no anchor** — the instrument's own
transcript says **166**, and the worktree-against-the-pin figure moves as
the arc grows, so it is left in `out_a3_anchor.txt` rather than written here.

### 4 — the strongest wording, checked first as the ticket asks

| | the rule mg-7522 judges its SUBJECT by | the rule it judges ITSELF by |
|---|---|---|
| where | `s3_figure.MARK` | `lib7522._STRENGTH` |
| alternatives | **9** | **3** |
| includes `verified` | **yes** | **no** |
| population | every artifact of `52aeaf4`, `.md` included | `MINE_PY + MINE_SH` |

`verified` is named as one of the three markers in `s5_self.py`'s D4 docstring,
in the README and in the published document — and is absent from the rule that
produces the **0**. `out_s5_self.txt` states the extent honestly; the README and
the document print the 0 without it. That is mg-7522's own **F3** with the roles
unchanged: the instrument was right and the summary dropped its scope.

And the CLAIM rule is **line-local**. `OUTCOMES.md:88` carries *"verified against
the"* with its figure on line 89, so neither line scores. Widening the window by
one line takes **mg-c2b3's own artifacts from 20 claims to 24** — the four the
hard wrap stepped over were never dispositioned. `A2d` then does what the word
`verified` stood in for: runs both arms on the same 8 inputs. **The claim holds.**

## The floor — one thing no list in the ticket names

**mg-7522 edited the instrument mg-05eb cites and deliberately did not re-run
it.** That decision is right and stated three times. Its side effect is that
`libc2b3.py`, `k1_census.py`, `k2_consume.py`, `selftestc2b3.py` and 63 lines of
rewritten shell now have **no current record**, so a break in them would be
silent. `A5` runs them: all four probes exit 0, both rewritten runners exit 0
with **5 of 5** and **3 of 3** steps reached, a forced failure gives **exit 1
with 0 of 4 later steps run**, and the worktree is byte-identical afterwards —
so all 8 of those transcripts regenerate exactly. And the `pipefail` row now
reads **ticket 1 / re-derived 1 / AGREES** in a live run of the subject's own
instrument, where the committed transcript reads **DIFFERS**. That is the
strongest available confirmation of OPEN 2 and it is positive.

## This tree, checked for the defects it audits

`selftestdee4.py` runs every rule in both senses and then turns the four defects
on this tree's own bytes.

1. **A population defined by a name.** `ls_tracked()` **does** take a suffix
   argument — deliberately, and the opposite of mg-7522's structural answer,
   because `A1b`'s question is *"is `.sh` itself a name rule?"* and a primitive
   that hard-codes `.sh` cannot ask it. The obligation here is therefore
   enumeration, not absence: every call site that names a file kind is listed
   and dispositioned.
2. **A stale anchor.** Every anchor is listed with the question it serves, and
   `ls_tracked`, `read` and `exists` all default to `ref=None`.
3. **A discarded status.** This tree's `run_all.sh` scores **0 pipelines of any
   kind** under `A1`'s own P2 predicate with every step redirecting and
   guarding. Every subprocess takes a list argv; there is **one** deliberate
   `/bin/sh -c`, in `A2d`, because reproducing the pre-repair *pipeline* is the
   measurement, and it is declared rather than hidden behind a rule that would
   not see it.
4. **A strength marker.** Over **every** file including the `.md`, under the
   nine-alternative rule and not the three. The first draft fired **26** times
   on its own regexes and on the sentences quoting mg-7522 while dispositioning
   it — the arc's recurring defect, reproduced here — so occurrences are
   **dispositioned with coverage checked both ways** rather than scored.

**What cannot be checked here, stated rather than omitted:** whether P2 is the
*right* predicate. `A1e` argues its consumption clause is narrower than the
reason mg-7522 gives for it, and points at one file where that bites. That is a
disagreement with a definition, which is the only useful thing to have about
one.
