# `code/coarse_unit_fa83/` — rules that pass a gated control and are wrong

**mg-fa83, the successor carrier for mg-cda7.** mg-cda7 measured one control's blind spot by
constructing widenings that pass it, and its carry-forward is the general claim:

> **A control defined over a coarser unit than the thing it is guarding is necessary and
> cannot be sufficient** — and the way to find out is to build rules that pass it and are
> wrong, rather than to argue.

This directory tests that claim by construction, on the population where a false pass costs a
merge: **the arms `./build.sh` runs**. A control that nothing invokes has never told anybody
anything — mg-937c measured exactly that, 0 of 150 stale transcripts in a directory the gate
runs — so the gate's own suites are the only population where `passes and is wrong` is a cost
rather than a curiosity.

## 1 What it does

`w1_witnesses.py` builds fourteen trees, each the corpus with one document mutated, and runs
**four real gated arms** against every one of them as subprocesses. Nothing is imported,
re-spelled, or read out of a committed transcript (mg-d2c2): a re-spelling makes every finding
a statement about the re-spelling, and a committed transcript is an answer about another tree.

| | |
|---|---|
| `e331` | `code/state_ratchet_e331/ratchet.py` — STATE.md's **word count** against a declared ceiling |
| `03cf` | `code/facts_registry_03cf/f0_registry_discipline.py` — `docs/FACTS.md`'s **field presence** and **entry count** |
| `602d` | `code/concepts_gate_602d/c0_concept_discipline.py` — `docs/CONCEPTS.md`'s **pointer presence** and word cap |
| `9bc2` | `code/rendered_twin_pin_9bc2/twin_pin.py` — STATE.md's **per-row ledger digests** |

The sandbox is a tree of symlinks into the corpus with real directories only along the mutated
path, so a world costs milliseconds instead of 41 MB. Each arm derives its own `ROOT` from
`os.path.abspath(__file__)` — which does not resolve symlinks, where `realpath` would — so an
arm invoked inside the sandbox reads the sandbox's documents. That is the whole trick.

## 2 The result

**7 candidate witnesses. 6 pass their target arm. 5 pass every arm in the population.**

| | recipe | target | verdict |
|---|---|---|---|
| R1 | STATE.md at the same token **count**, every token 2 000 characters — 35 KB → 10.4 MB | `e331` | passes `e331`, **caught by** `03cf`,`602d` |
| R2b | every non-ledger line's words replaced by `lorem`, ledger + 2 pointer lines held | `9bc2` | **passes every arm** |
| R3 | `F1`'s `**SCOPE.**` body replaced by `n/a` — 702 characters → 14 | `03cf` | **passes every arm** |
| R4 | one entry deleted, one fabricated entry added — the count is unmoved at 26 | `03cf` | **passes every arm** |
| R5 | the `alpha(P)` row points at `mg-0000`, an id no work item has ever had | `602d` | **passes every arm** |
| R6 | the R1 recipe on `docs/CONCEPTS.md` | `602d` | **CAUGHT** — refuses at exit 2 |
| R7 | `F1` re-graded `` `U` `` (proved) → `` `OPEN` `` — a recognised mark, and the wrong one | `03cf` | **passes every arm** |

Each ships a **paired must-fire** mutation of the same document that the arm must catch —
`6 of 6 fired`. Without it, *unmoved* cannot be told from *not running*, which is the failure
mg-585e's F1 exists to prevent one directory over.

### The base rate, which is the context the six are read in

**1 of 7 was caught by its own target.** mg-cda7 printed `6 of the 13 gain nothing at all` for
the same reason: a search that finds a witness everywhere is measuring its own permissiveness.
The number here is small, and the honest reading of a small number is that these controls are
coarse rather than that this search is loose — which is why the must-fire column exists and
why `w0` D4 asserts that a change no arm reads moves **0 of 4**.

### And a crash is not a catch

`R1` takes `twin_pin.py` to an uncaught `ValueError`. It blocks the merge and it detects
nothing, so it is reported as `CRASH` and **subtracted** from the catches. `R6` takes `c0` to
an exit-2 **refusal it printed on purpose**, which is counted. A traceback and a finding leave
the same exit code (mg-9876) and this directory refuses to fold them together — crediting a
control with a mutation that merely broke it is how coverage gets claimed that nobody has.

## 3 The one that was caught is the remedy, and it costs one predicate

R1 and R6 are **the same recipe on two documents** and they come back opposite ways. The
difference is one design decision, already written down in the arm that has it:

> *"If a heading is reworded the anchor is not found and this arm REFUSES (exit 2) rather than
> passing — a rename must be LOUD. It cannot be silent-green, because a gate that quietly
> stops checking is worse than no gate: it is a gate people believe in."*
> — `c0_concept_discipline.py`

That is a **default-deny on the document's shape**, and it is what stops a count-valued control
being passed by a document that is no longer the document. `ratchet.py` has none. Sharper:
`lib_e331.measure()` computes `bytes`, `lines`, `max_line_chars` **and** `lines_over_2000`, and
`verdict()` reads **only** `words` — the four finer numbers are printed and gate nothing. The
coarse unit is chosen at the *decision*, not at the *measurement*, which is mg-cda7's own shape
(the in/out split is computed and printed; the decision uses the proxy).

**This branch does not make that change.** It rewrites another directory's arm, its transcript
and its PREDICTIONS, and a demonstration that is binding by the back door is not a
demonstration (mg-585e). It is exhibited, priced, and handed to that arm's owner.

## 4 What the merge gate actually holds in STATE.md, as a number

R2b's preserved set is the answer, because it is the set of lines that had to be held
byte-identical for every arm to stay green:

```
STATE.md            211 lines, 5 199 words
the ledger table     26 lines
naming docs/FACTS.md      2 lines      (f0 §3 reads STATE.md for the entry-count pointer)
naming docs/CONCEPTS.md   2 lines      (c0's FINDABLE reads STATE.md for the link)
PRESERVED SET        28 lines of 211  (13.3%) — 2 048 of 5 199 words (39.4%)
```

**3 151 of STATE.md's 5 199 words are outside every fine-unit check the merge gate performs**,
and R2b is a tree in which all of them are the word `lorem` and all four arms are green. The
ratchet sees the **count**; the twin sees the **ledger rows**; the complement is guarded by
neither and it is the majority of the document.

That number is also the strongest thing this directory found *for* the estate: R2a, which keeps
only the ledger, is **caught** — by `f0`, because `f0` reads STATE.md for its own pointer. The
coverage is real, it is an accident of another arm's dependency, and nothing wrote it down
before this.

## 5 The remedy is an artifact of the same kind as the defect, and it was

`w0_selftest.py` D6 is the plant worth reading. `w1`'s first draft compared each arm's decision
as the pair `(exit code, grade word)`. That pair is **coarser than the arm's own decision
sentence**: `f0` prints `VERDICT: GREEN — 26 entries`, so a tree that gains a valid entry
leaves `(0, GREEN)` exactly where it was while the sentence moves `26 → 27`. A `WITNESS`
declared in that unit would have been this directory's subject arriving inside this directory.

D6 builds that tree, shows the coarse unit blind and the shipped unit not, and **the unit was
made finer rather than the finding softened** — `lib_fa83.decision` returns the whole scrubbed
decision line. It is still coarser than the arm's whole output, and that is said in the
docstring rather than left to be found.

`w0` is 18 plants, 18 CAUGHT, and it runs **first**: everything `w1` prints is a statement
about the estate only if the sandbox is faithful, and `w0` is what says it is.

## 6 What this cannot see — its own coarser unit

1. **The population is four arms**, chosen because their subject is a document. A gated arm
   that reads one of these files incidentally is invisible here. That is a proxy over a
   coarser unit, in the directory about proxies over coarser units.
2. **No `.git`.** Every git-valued decision is out of reach: `twin_pin` §7 grades itself
   `REPORTED, NOT GRADED` here and `gate.py` refuses outright (measured: exit 2, `field
   twin.worklist matched its pattern 0 time(s)`). A witness a git-valued section would catch
   still reads as a witness.
3. **`WRONG` IS THIS BRANCH'S READING.** The damage columns are numbers; that an emptied
   `SCOPE` or an `mg-0000` pointer is a *defect* is a judgement — the same one `OWNERS.json`
   makes about `cause`, and it declares that nothing checks it.
4. **A witness is loud in `git diff`.** What it is not is *blocked*. mg-be37's finding is the
   reply: a detector with no addressee and one that never fired are indistinguishable, and so
   are a reviewer who reads and one who does not.
5. **This directory's own headline is a count**, which is §7's defect in §2. `6 of 7 pass` is
   unmoved by a recipe *deleted* and a weaker one *added*, exactly as `twin.mutations_total`
   is. What stops it here is that the arm prints the **set** — every recipe by id, headline
   and verdict — so the count summarises something a reader can re-read rather than standing
   in for it. That is the only remedy found for a count in this whole exercise, and it is a
   disclosure, not a check.
6. **A must-fire pair proves the arm runs, not that it is sensitive to the witness's kind of
   change.** Each pair moves a check of the same arm; none is evidence that the arm could in
   principle have seen its partner. It closes *the sandbox is not exercising this arm* and
   nothing wider.

## 7 The sharpest instance in the estate is the one this could not build

`code/control_gate_724a/BASELINE.json` gates two **integers** over the twin's negative control,
`twin.mutations_caught` and `twin.mutations_total`, and the second exists because of this exact
shape. Its own `why`:

> *"Gated because a mutation quietly deleted is coverage quietly removed, and it would
> otherwise be invisible: 16 of 16 caught reads exactly like 17 of 17."*

**The remedy there is the same kind of artifact as the defect**: a count was guarded by adding
a second count, so a mutation *deleted* and a different one *added* moves neither field. That
is mg-cda7's `gains lines, OUT unmoved` letter for letter, on the file that gates the gate.

**It is read and not witnessed**, and the difference is this directory's whole point, so it is
labelled rather than dressed up: exercising it needs `gate.py`, `gate.py` needs the twin
suite's git-valued sections, and this sandbox has no git by construction. Filed forward.

## 8 Not in `build.sh`, and the reason is not the runtime

The suite is **~4 s**, so cost is not the argument. Two things are:

- **Its subject is other people's controls.** Every finding is a property of an arm this
  directory does not own, and an arm that went red on them would make every branch red for a
  defect it reports rather than introduces — mg-e35b's red-on-improvement in the
  measurement's clothes. `w1` therefore exits 0 whatever it finds; only `w0` may go red.
- **A gate that runs four other gates' arms in sandboxes doubles the surface** on which a
  change to any of those four fails a merge here for a reason its author cannot act on
  (mg-724a's recorded/gated split).

`w0` alone is gateable by that argument, and it is not proposed here either: it guards this
directory's instrument, which nothing else consumes.

## 9 What this leaves

- **The `BASELINE.json` pair, §7 — filed as `mg-f10d` rather than left as a sentence**, which
  is what this directory's `declares-remainder` tag requires. Read and not witnessed. It needs
  a sandbox with a real throwaway git repository, which `negative_control.py` already builds
  three of — so the machinery exists one directory over and was not lifted here.
- **The remedy at `e331`, §3.** One predicate, exhibited and declined on scope.
- **The other nine gated suites.** Their inputs are posets, so a mutated markdown file is not
  a fact about them — but *whether* their controls are coarse over the objects they compute is
  an entirely open question and this directory says nothing about it.
- **The population is documents.** The same method applied to a *computation* — mutate the
  input poset, not the input file — is the obvious next axis and no line of this directory
  touches it.
