# A source line inside a loop is N executions

*The six findings of `mg-dee4` against `1ee1f1b` (`mg-7522`), landed. `mg-7522`
repaired the three open sites of `682db2c` (`mg-05eb`), which audited the
arc-wide `| tee` sweep `52aeaf4` (`mg-c2b3`).*

Instrument: `code/runner_exit_repair_70c7/`. `sh run_all.sh`, about four
minutes, pure Python 3, no dependencies, no network. Every figure below is
printed by a probe in that directory next to the predicate that produced it.
`PREDICTIONS.md` was committed **before any probe in that directory existed**.

> **AMENDED BY `mg-bf79`, after `mg-56dc` audited this repair.** Four things in
> this document's own instrument were wrong and are now repaired; three of them
> touch figures stated below and the fourth is the reason one of them was
> unreadable.
>
> * **The `9` in the F5 section was right and the transcript backing it was
>   wrong.** The probe printed the **(site, target) ROW** count under the label
>   `executing sites`. `9` is the distinct-SITE count. Both grains are now
>   printed under their own grain words **at a named revision**, because the
>   census ranges over the whole repository and therefore moves.
> * **The strictest self-rule ranged over one directory's transcripts** and now
>   ranges over the **11 artifacts this deliverable authored**, derived by
>   provenance from the whole repository — including this document.
> * **The "one marker rule" had dropped `proven`.** Restored: **9 → 10**, which
>   is `mg-dee4`'s D4 union.
> * **Two copies of `figures()` disagreed on the integer 3.** There is one now.
>
> The record is `code/runner_exit_repair_bf79/` — `README.md`, `OUTCOMES.md` and
> six transcripts. **And the finding that outranks all four: the classifier
> `mg-56dc` built to catch label/grain mismatches cannot see this one.** `rows`
> and `sites` are the same grain word to it, because its axis is
> SITE-vs-EXECUTION and this was ROW-vs-SITE. A label-reading check is necessary
> and is not sufficient.

---

## The short version

`mg-dee4` found six things, and five of them are the same thing: **a count is
not a measurement until you say what it ranges over.**

1. **`11 of 11 read directly` was eleven LINES.** Three of them sit inside `for`
   loops and execute eight times between them; a hand-list of three argv covered
   four of the eight, and one of the three did not match the line it was
   labelled with. **The verdict survived; the arithmetic did not.**
2. **`154 changed files` is reproduced by no anchor** — in a document that
   states, one commit later, that a number that moves belongs in a transcript.
3. **It judged its subject by a nine-alternative rule and itself by a
   three-alternative one**, over a population that excluded every `.md`.
4. **The claim rule was line-local**, and the strongest claim in the file it was
   pointed at had wrapped.
5. **The caller scan was still a name rule**, with two names instead of one.
6. **The consumption clause was narrower than the reason written for it**, and
   the two came apart on a file all three rules missed for three different
   reasons.

---

## 1 — sites are not runs

> **A source line inside a loop is N executions, not one. An enumeration that
> counts SITES cannot support a claim about RUNS, and the two are
> indistinguishable in a report that does not say which it is at.**

The retroactive clearance covered eleven pipelines the sweep's filename never
reached. Eight are `| tee` lines in two `run_audit.sh`, derived from the
runners' own bytes, and those eight are sound: derived rows cannot drift from
the source, and each carries a real exit code and a real wall time.

The other three are `git diff "$base..HEAD" -- "$dir" | wc -c | tr -d ' '`
lines in two `run_all.sh` — and they are inside

```sh
for pair in "a4aeeb9 code/state_layer_audit_218d" \
            "3a80d99 code/state_delegation_audit_5644" \
            "2a29f30 code/state_delegation_repair_bee1"; do
    base=${pair%% *}; dir=${pair#* }
```

Three lines, **eight runs**. They were covered by three hand-written argv
containing **two distinct commands**, so **four of the eight runs were never
executed** — and the row labelled `state_delegation_audit_16eb/run_all.sh:39`
carried an argv **without the `':!*.md'` pathspec that line 39 has**, so that
line's discarded stage was never read in any shape.

**The rows are derived now.** The loop header expands to its literal items, the
body's own `base=${pair%% *}` assignments are followed, and `argv_of` returns
`None` rather than leaving an unresolved `$` in a command it is about to run —
because a command that was never run, labelled with a source line, is exactly
the row this repairs. The refusal is pinned in both senses: a loop over `$DIRS`
reports *not statically expandable* and is never counted as one iteration.

**16 of 16 exit 0** — 8 `| tee` invocations plus 8 `git diff` invocations. And
the corrected population is not a single number: it is **34 sites inherited from
a transcript nobody in this chain has re-run, plus 16 executions run here.**
Adding them would be adding sites to runs.

The byte counts the repair called *verified* are **computed** now, on both
mechanisms — the stream length `| wc -c` reported and the file size
`wc -c < FILE` reports — for all eight executions, including the two of
`state_delegation_repair_0049` that the published parenthesis did not list. A
figure covering six of eight under the words *the byte counts* is the same shape
as `11 of 11` covering four of eight. `mg-dee4` ran both arms and the claim
**held**, which is what makes it reportable rather than damning: **`verified`
was checkable, was not checked by its author, and turned out true.**

---

## 2 — a rule stated in prose is applied where the author was looking

`c252f96` wrote *"a number that moves belongs in a transcript"* and applied it,
correctly, to the four totals of a 2×2 table. **Three paragraphs below it** the
same document said *"anchored to the pin the byte-comparison sees **154 changed
files**"*, and nothing reproduces 154:

| anchor | files |
|---|---|
| `s4_unpin.py`'s own committed transcript, at the time | 166 |
| `1ee1f1b`, the repair | 257 |
| `1ee1f1b^`, the commit before | 240 |
| the worktree / `main`, today | see `out_r2_anchor.txt` — it moves |

So the sentence points at `out_s4_unpin.txt` now. But moving one figure repairs
one figure, and the finding is about a **rule applied by hand**. So the rule is
a check: a **figure census** reads every number in a reader-facing artifact and
asks whether any transcript of its own tree prints it. Unbacked figures are
either repointed or dispositioned by hand with the transcript that does carry
them — a quotation of `mg-c2b3`'s own scoping sentence is backed by `mg-c2b3`'s
transcript, and that is written down rather than fixed by widening the corpus
until everything passes.

**A defect in that census, recorded rather than smoothed away.** Its first draft
built the corpus by matching every number in the transcript text. Under that
rule `154` came back **BACKED** — by the string `s3_figure.py:154` in
`out_s5_self.txt`. **A line number was backing a measurement**, and the census
would have blessed the exact figure it exists to catch. The corpus is now built
with the same figure rule the claim side uses, and `on line 89` is not a figure
either.

---

## 3 — apply to yourself the rule you apply to your subject

> **A nine-alternative test for them and a three-alternative one for you is not
> a stricter standard applied leniently. It is a different instrument, and it
> will not find what theirs finds.**

`s3_figure.MARK` — pointed at the sweep — had nine alternatives.
`lib7522._STRENGTH` — pointed at this tree — had three. **`verified` was named
as one of the three markers in the D4 docstring, in the README and in the
published document, and was in the nine and not in the three.** And the
self-facing population was `*.py` + `*.sh`, so the README, `OUTCOMES.md`,
`PREDICTIONS.md` and the published document were all outside it — **three of the
four artifacts `mg-05eb`'s OPEN 2 found wrong were exactly that kind.**

Two rules cannot be kept in step by intention. There is **one rule object** now,
`lib7522.MARK`; `s3_figure` and `s5_self` both use it, so a marker added for one
is added for both by construction. The population includes the `*.md` and the
document.

And the verdict changed shape, because `0 USES` under the widened rule is not
attainable and should not be. **A bare marker beside a figure the tree computed
is not the defect; a bare marker beside a figure nothing here produces is.** So
a use is **BACKED** when every figure in its window is printed by a transcript
this tree commits, and **UNBACKED** otherwise. Only UNBACKED is counted. A use
with no figure at all is listed under a **stated limit**: D4 asks whether a
number stood on a word, and a qualitative marker is outside its reach.

The first thing the repaired check found in its own tree was
`OUTCOMES.md:88` — *"…counts the same bytes the pipeline did, **verified**
against the"* — whose figure `2111` no transcript printed. That is `mg-dee4`'s
F4 arriving through F3's door, and it is fixed by **computing the byte counts**,
not by deleting the word.

### The claim rule was line-local

A claim was a **line** carrying both a marker and a number. In hard-wrapped
prose the marker and its figure land on different lines routinely — and
`OUTCOMES.md:88` carries the marker with its figure on line 89, so **neither
line scored.** The rule that produced *"20 strength-marked numeric claims, every
one dispositioned"* could not see the strongest claim in the file it was pointed
at.

With a window of **one line in either direction**, the same population is **24**.
The four it adds are dispositioned one at a time like the twenty; three of them
are markers written inside comments **about** the marker, which is the
mention-for-occurrence distinction this arc keeps re-deriving, arriving through
the window rather than through the line. They are dispositioned rather than
excluded by a rule tuned to drop them — **a rule that drops what it does not
want is how a population becomes a hand-list.**

---

## 4 — widening a name list is not making it a property

The caller scan matched `run_all\.sh`. The first repair made it
`(?:run_all|run_audit)\.sh`. **That is one filename replaced by two.**

At `973ca61`, the commit that published `out_r4_property.txt`: **9 distinct
executing SITES name a `*.sh` whose basename is neither**, across 6 distinct
target scripts, **4 of them reading the exit status** — and **0 sites name the
`run_audit.sh` the widening added**, so the widening is not exercised by
anything in the arc.

**The same census gives 10 (site, target) ROWS** at that revision, because
`code/runner_exit_c2b3/selftestc2b3.py:155` names two scripts on one line. This
paragraph used to read `At HEAD` and the transcript it cited printed the **10**
under the word *sites* — mg-56dc/T1c, repaired in mg-bf79, which prints both
grains each under its own grain word. **The count was wrong and the label was
right.** And the census ranges over the whole repository, so it moves. A figure
from a moving census belongs to a revision, which is why one is named here and
`HEAD` no longer is; the value at any later revision is printed by
`code/runner_exit_repair_bf79/out_p1_grain.txt`, which re-derives it at both
grains, rather than written into this paragraph where it could not be
re-measured.

The property *was* stated — in `mg-7522`'s library, whose comment says the name
rule *"is widened here to the property"*, **here** being the library and not the
file that was repaired. **A property stated where the check does not live is a
property nothing enforces.** It is `libc2b3.targets` now — the sweep's own
library, used by the sweep's own scan, pinned by five both-senses rows in the
sweep's own self-test:

> **A caller is a line that executes something and names a shell script.**

The widening loses nothing, which is checked in that direction too. The two
limits that remain are named at the rule: the tree is read from a directory
component on the same line, and a path assembled at run time is invisible to any
line-local rule whatever the anchor.

**And the self-test's own fixtures joined the population it counts** — five
lines naming a `*.sh` inside an executing construct. They are printed in the
census, not folded away.

---

## 5 — fix the population; the instance is secondary

P2 tested consumption with **errexit alone**, at file grain. The reason written
for pulling the three `git diff` lines in was about the **value**:

> *"a `git diff` that failed produced an empty stream, `wc -c` reported `0`, and
> the proof read `-> 0 bytes`"*

Both readings are true of those three lines, because both of those files happen
to set `-e`. **The difference was invisible in the population that produced it.**

`code/branching_audit_a218/c0_repro.sh:47` is where they come apart:

```sh
COUNT=$(grep -o '[0-9][0-9 ]*' "$WORK/out_selftest.txt" | tr -d ' ' | tail -1)
```

`set -u` and no `-e`. The discarded `grep` and `tr` can fail; the value reaches
`COUNT`; `COUNT` drives `BAD`; `BAD` drives `exit 1`; and nine sites in four
files read that exit code. **All three rules miss it and each for a different
reason** — the name rule because it is `c0_repro.sh`, the shape rule because
there is no `tee`, the property rule because there is no `set -e`.

`consumed` is a named disjunction now — **ERREXIT** or **VALUE** — and the arm is
printed with every row, so a reader can disagree with one arm without discarding
the other. At `bee07a1` the population goes from **19 files / 26 pipelines** to
**20 / 27**; at `HEAD`, from 0 to **1**.

**The instance is not repaired, and the reason is measured rather than argued.**
The real script is run twice on a scratch copy of its own bytes, once as
committed and once with the discarded `grep` given an option it rejects:

| arm | exit | prints `DISAGREES` |
|---|---|---|
| as committed | 0 | no |
| `grep` forced to fail | **1** | **yes** |

**Its failure direction is loud** — the opposite of the silent green the sweep
existed to find. That is what makes it a hole in a population rather than a live
swallow, and it is why the repair is to the predicate.

---

## The deliverable, checked for the defects it repairs

`r6_self.py` turns the same four questions on this tree: is every count's grain
stated; is every figure of mine printed by a transcript of mine; is every rule I
point at `lib7522` pointed at `lib70c7`; and is any population of mine defined
by a filename. Its own runner is run through the **widened** predicate, not the
one it replaced.

**Two predictions missed and are kept.** I predicted the widened P2 at `bee07a1`
would land between 21/29 and 28/40; it is 20/27 — I reasoned from the size of
the gap between two rules without checking how much of it the value arm could
reach, which is the same mistake `mg-dee4` recorded in its own P4. And I
predicted at least two files in the widened P2 at `HEAD`; there is one.

**Five defects in this instrument are recorded rather than smoothed away.** The
figure-census corpus that let a line number back a measurement, above. A first
draft of the grain check that **forbade the string `11 of 11` outright**, so that
every artifact which had correctly described what it repaired went red for
saying so — a check that would have been satisfied by deleting the record of the
defect; quoting and asserting are counted separately now. A first draft of
the marker rule that scored `` `verified against the` `` as a **use**, because
it tested the single character on each side of the marker rather than
containment in the quoted span — and the first thing it flagged was this
repair's own comment about the finding. **A correction test that was itself
line-local**, so a correction which wrapped scored as an assertion of the very
figures it was correcting — F4's defect inside the repair of F4. And a
transcript corpus built from the **git index**, which is empty on the run that
produces the transcripts, so 108 figures came back unbacked and every one of
them was one fact about the index.

**What is not established, named rather than folded into a total.** That the
value arm is the *right* widening — that is a disagreement with a definition,
and the definition is written out in full so that disagreeing with it is
possible. `mg-c2b3`'s own 34, still cited and still not re-measured. That a
backed figure is backed by the *right* measurement — the backing test asks
whether a figure appears in a transcript, not whether it answers the same
question, and every row prints the figure so the sense is checkable by eye. And
every intermediate commit: this is read at `HEAD`, on one machine.

**And what was deliberately not regenerated.** `out_k1_census.txt` is the
transcript recording `ticket 1 / re-derived 0 / DIFFERS`, and `mg-05eb` cites it
as that record. The regex is repaired, so a re-run would print `AGREES` and
destroy the citation. A transcript is the record of a run at a time.
