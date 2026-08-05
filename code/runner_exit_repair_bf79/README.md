# mg-bf79 — mg-56dc's four openings, repaired, plus the floor item nothing named

`mg-56dc` audited `mg-70c7`'s grain-and-population repair and closed with *the
six repairs hold where they were pointed* — and four openings, every one of them
a defect **of the instrument that found the defects**. This ticket closes them.

**An independent audit of this repair was already filed and waiting on it when
the predictions were written** — `mg-03d1`, `Depends: mg-bf79`. `PREDICTIONS.md`
was committed **before any script in this directory existed**, which is checkable
from `git log`: the commit carrying it is the one whose subject begins
`predictions: mg-bf79`, and no other commit of this tree precedes it. **Seven of the
26 scored rows carry a miss, and none has been revised.**

## The one-line verdict

*The count was wrong and the label was right — `9` is the distinct-SITE count and
the transcript printed the ROW count under the site word. And the instrument the
brief sent me to run over the whole artifact **cannot see that defect at all**:
`rows`, `basenames` and `sites` are the same grain word to it, because its axis is
SITE-vs-EXECUTION and this is ROW-vs-SITE. mg-56dc found T1c by re-deriving the
quantity at two grains and could not have found it with its own classifier.*

## What was repaired

| | the opening | what was done | which was wrong |
|---|---|---|---|
| **O1** | a count labelled `executing sites` printed **(site, target) ROWS (10)** where four artifacts publish the **SITE count (9)** | `r4_property.py` prints **both grains, each under its own grain word, at a named revision**; the four artifacts now state the grain **and** a revision | **the COUNT.** `9` is the site count, and it is what the artifacts always said |
| **O2** | the strictest self-rule, E1, ranged over **one directory's `out_*.txt`** (7) | `lib70c7.published_by` — a **property** over the whole repository. **11 artifacts**, 4 of them prose, 1 four directories away, **0 lost** | the population |
| **O3** | the "one rule object" **dropped `proven`** | restored to `lib7522.MARK`: **9 → 10 = mg-dee4's D4 union**, diffed by name **and behaviourally** in both directions | the merge — it was *the subject's rule pointed at me too*, and only a **union** cannot lose a member |
| **O4** | two copies of `figures()` **disagreed on 3** | `lib70c7.figures` **calls** `lib7522.figures`. 1 disagreement → 0 | **mg-70c7's copy.** Both docstrings said `0, 1 and 2`; only mg-7522's did it |
| **F** | *the floor item, in neither brief*: `figures()` was **not the only rule kept in two copies** | `alternatives()` too — a **rule**, producing the published figure *"nine alternatives against three"*, in **two byte-identical copies**. Unified. **15** names are defined in both libraries; every one is dispositioned | — |

## Read this first: the finding that outranks the four

**The sixth instrument's classifier cannot see O1.** `out_p1_grain.txt`/P1f puts
the words to `lib56dc._classify` and prints the answers:

```
      `sites         `  classifies as  SITE
      `rows          `  classifies as  SITE
      `basenames     `  classifies as  SITE
      `executions    `  classifies as  EXECUTION
```

`rows` and `sites` are **the same grain word** to it — correctly, on its own
terms: both range over source rather than over runs, which is the F1 distinction
it was built for. So **a count labelled `sites` holding a ROW value passes it.**

The brief told this ticket to *check the classifier, since it works from labels*.
That is the answer: a label-reading check is **necessary and not sufficient**, and
the gap between the two is exactly one defect wide — the one it was pointed at.
**And P1f's own test inherits the blind spot it measures**, which is recorded in
the transcript rather than tuned away.

## The probes

| probe | what it establishes | exit |
|---|---|---|
| `selftestbf79.py` | every predicate on inputs with **known answers, in both directions** — mg-56dc/T3d found *0 direction tests in either membership predicate* | **0** |
| `p1_grain.py` | O1: the publishing commit **derived** not named; the quantity at two grains at that commit and at HEAD; the ledger of every count row of the repaired output; the blind spot | **0** |
| `p2_population.py` | O2: the old population, the new one, 0 lost, the member no path could reach, and what the widening **found** | **0** |
| `p3_ruleset.py` | O3: the alternatives named and diffed by name **and behaviourally**; rule objects diffed; what restoring `proven` costs, under a **controlled counterfactual** | **0** |
| `p4_figures.py` | O4 and F: one implementation each, 0 disagreements over 0..500, the by-name duplicate census with a disposition per name | **0** |
| `p5_self.py` | this tree checked for the four defects it repairs | **0** |

`PREDICTIONS.md`/P5c predicted **6 of 6 exit 0** and that is what happens — the
one prediction of this file that was *supposed* to be easy.

## Which transcripts were regenerated, and which were not

A repair whose transcript still shows the defect is not a repair; a transcript
regenerated for no reason is churn that hides what moved. So the rule is: **the
transcripts regenerated are those whose producing probe or its rules this ticket
changed**, and the rest are left alone. Both lists are here because a list of one
without the other is an assertion.

**RE-RUN, and their bytes MOVED** (7) — `mg-70c7`: `out_r2_anchor.txt`,
`out_r3_strength.txt`, `out_r4_property.txt`, `out_r6_self.txt`. `mg-7522`:
`out_selftest_7522.txt`, `out_s3_figure.txt`, `out_s5_self.txt`.

**RE-RUN, and came back BYTE-IDENTICAL** (2) — `mg-70c7`'s
`out_selftest_70c7.txt` and `out_r1_grain.txt`. They are named here rather than
folded into either list, because *re-run* and *changed* are two facts and a
single list would let a reader infer the wrong one. Both probes reference the
changed rules, so re-running them was right; neither number moved, so nothing in
them is a fact about this ticket.

**NOT RE-RUN** (4) — `mg-70c7`'s `out_r5_population.txt`; `mg-7522`'s
`out_s1_population.txt`, `out_s2_status.txt`, `out_s4_unpin.txt`.

**And the claim that this is safe is measured, not asserted.** A `grep` for
`MARK|strength_lines|figures|transcript_figures|alternatives` over each probe
returns **0** for all four of those, and non-zero for every probe that was
re-run. `mg-7522`'s `s1`/`s2`/`s4` also take about twenty minutes and `s2`
executes runners in the working tree; re-running a probe whose rules did not
change, to churn a whole-repository census, would make the diff unreadable for no
gain.

**`mg-56dc`'s and `mg-dee4`'s trees are BYTE-UNCHANGED.** This ticket **imports**
`lib56dc` — its `count_rows`, `grain_of`, `exec_site_rows`, `exec_sites` and its
parameterised third `figures()` — because the brief tells this repair to run the
sixth instrument over the whole artifact. Importing an auditor's instrument is not
editing its findings, and `p5_self.py`/S4 asserts the difference with `git diff`.

## The pin that went red, and why it was moved

`selftest7522.py` hard-pins *the marker rule has 9 alternatives*. Restoring
`proven` turned it **red — which is the pin working.** It is now 10, and **the
authority for 10 is not that the code says 10**: it is mg-dee4's D4 union, which
`out_a4_superlatives.txt` publishes as `9 subject + 1 self-only`, and which
`out_p3_ruleset.txt` re-derives from mg-dee4's own source and checks
**behaviourally** against the restored rule on 20 probe words — 0 reached by one
and not the other. Updating a pin to match the code is how a pin becomes
decoration; updating it to match the finding the code was changed to satisfy is
what a pin is for, and the two are told apart by whether an independent artifact
publishes the new number.

## Six defects of this instrument, recorded rather than smoothed away

Five consecutive deliverables in this lineage have found their own defect class
in their own tooling. This is the sixth, and it found six.

1. **The provenance query's `\(` was a BRE group.** `--grep='\(mg-70c7\)'` — in
   git's basic regex `\(` opens a **group**, so the pattern reduced to the bare
   string `mg-70c7`, matched every commit whose *body* mentions this tree, and
   returned **15** artifacts including **my own auditor's README, OUTCOMES,
   PREDICTIONS and published document**. A population meant to be *the artifacts
   I authored* had silently become *the artifacts of everyone who has written
   about me* — and E1 would then have been grading mg-56dc. An escape that means
   the opposite in the dialect it lands in is the same failure as a label that
   names the wrong grain. The subject is now matched in Python.
2. **The revision-and-grain check was LINE-LOCAL — twice.** First draft required
   figure, grain word and revision on **one line** and reported 1 of 4 against
   prose that states all four. Second windowed the revision and left
   `9`-near-`sites` line-local: 3 of 4, failing the published document, whose
   sentence wraps between the figure and the grain word. That is **mg-dee4's F4**,
   the defect `mg-70c7`'s own R3d repaired by making `s3_figure.WINDOW` symmetric
   — reproduced while checking that it had been, and then reproduced again one
   conjunct in. **The rule was fixed, not the prose.**
3. **The alternative diff compared regex SOURCE against mg-dee4's PROSE
   RENDERING.** `all (?:\d+|of)` against `all <n> / all of` — and it reported
   **3 phantom gained alternatives** that mg-dee4's rule has had all along. It now
   reconstructs mg-dee4's union from its own source and compares **behaviourally**
   on 20 probe words.
4. **The moved-numbers claim attributed ARC DRIFT to this ticket.** A live run
   diffed against a committed transcript said **5** count rows moved. A controlled
   counterfactual — write the pre-repair `MARK` back, run, restore the exact bytes
   — says **3**; the other 2 move with the repository whether or not this ticket
   exists. That is **mg-56dc's own recorded defect #1**, committed by the ticket
   repairing its findings, and it is the number `3` that this deliverable is to be
   held to.
5. **P1f's blind-spot test inherits the blind spot it measures.** It reports 1 in
   the published version and 1 in the repaired one, because the row it picks after
   the repair is labelled `ROWS` and the classifier calls that SITE too. A
   label-reading test cannot audit a label. Recorded, not tuned.
6. **The T2 fixture was invisible to its own population.** `exec_site_rows` builds
   from `git ls-files`, so a `mkdtemp` fixture written only to disk returned 0
   rows and 0 sites — reading as a broken parser and actually an untracked file.
   That is `lib70c7.outs()`'s own recorded defect from the other side. The fixture
   is `git add -N`'d and removed in a `finally`.

## And one finding reported and NOT fixed

**`lib70c7.figures()`'s comment claimed to exclude "a git revision" and never
did.** A short revision that happens to be all decimal digits is matched and
passes every exclusion. Not hypothetical: repairing O1 required naming a revision
in `mg-70c7`'s README, and `r6_self.py`'s E2 immediately reported it as **a figure
no transcript backs**. The check was right by its own rule and the rule's stated
exclusion list was false.

**It is not fixed here, and the reason is measured rather than pleaded.** Over all
451 committed transcripts there are 1284 distinct figures, **31** of magnitude
≥ 1e6, of which **6** resolve as git objects. A magnitude rule drops **25 genuine
figures** including `2147483647`, an INT_MAX in a fixture. A resolves-as-an-object
rule drops 6 for an accident of this repository's object database rather than a
property of the number. *A generous exclusion list turns an unbacked figure into a
non-figure* — `lib70c7`'s own sentence, which is why the wrong fix is worse than
the finding. `selftestbf79.py` **asserts the false exclusion as false**, so if a
later ticket fixes it that row goes red and names itself.

## Also named and not acted on

**`captured_var` is a rule kept in two identical copies** — and not a small one:
it is mg-dee4's **F6**, *the variable a pipeline's output is captured into*, the
VALUE arm of the consumption clause F6 is entirely about. It agrees today. So did
`alternatives()`. It is out of scope because `mg-56dc`'s O4 names `figures()`, and
because `captured_var` is reached by `s2_status.py` and `k2_consume.py`, whose
transcripts this ticket does not regenerate. Changing a rule I cannot re-measure
would be the defect this whole arc is about. **Naming it is the only honest thing
to do with a finding you are not going to act on.**

## Running it

```sh
sh code/runner_exit_repair_bf79/run_all.sh
```

About one minute. Pure Python 3, no dependencies, no network. Run it on a
committed tree: P1 and P4 report figures derived at HEAD, and a dirty worktree
makes those rows facts about your edits rather than about the arc. Two probes
write and restore — `p3_ruleset.py` the pre-repair `MARK` line, `selftestbf79.py`
a `mkdtemp` fixture and one intent-to-add index entry — and each asserts its own
restore rather than relying on the other.

**The committed transcripts are from a second consecutive run.** `p5_self.py`
reads this tree's own transcripts, which do not exist on a first pass, so a first
run reports 0 count rows of its own and that zero would read as a pass.
