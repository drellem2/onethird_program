# mg-5f7c — the repo's only suppression instrument, made to fail the way both its documents said

`visible_a74f.py` is **the only instrument in this repository that measures suppression**. No
second instrument contradicts it, so each of mg-65eb's findings against it was unopposed.

**`PREDICTIONS.md` was committed before any script of this repair existed**, and every figure
below is scored against it, misses included. The pre-repair anchor is **`6fb424f`** — this
branch's base, and an ancestor of `main` when the branch was cut. **That anchor is a sha and a
sha is immune to renumbering, not to displacement:** the refinery rebases before merging, so
this repair's own `predictions:` commit will land on `main` under a different sha than it has
on `polecat-z5f7c`. The check for that is `git patch-id --stable`, never
`git merge-base --is-ancestor`, which returns a false negative after a rebase. That is
mg-a74f's `739f7bd` lesson, recorded here **in advance** rather than rediscovered.

---

## Which way, and why — the question the ticket asks before it asks for a fix

The docstring said fail open. The README said fail open. The code failed **closed**. Making
those agree is two different repairs with opposite safety postures, and picking by reflex —
"the code is the truth, edit the prose" — decides a safety question by typography.

**The code was wrong. Both documents were right. The instrument now fails open.** Three
reasons, in the order that settles them:

1. **The declared set already said so, and it is printed on every run.** `DECLARED` S4 reads
   *inside an element carrying the `hidden` **attribute***. The first line of `NOT_COVERED`
   reads *any rule from an external or embedded stylesheet, **including `display:none` on a
   class***. So the docstring, the README **and the instrument's own printed declared set**
   all agreed with each other, and only the implementation disagreed with all three. There was
   never a third document to reconcile — there was one function that did not implement the set
   it prints.

2. **The costs are not symmetric.** Every use this instrument is put to in this arc is
   refuting another artifact's claim that a reader is shown something — V1 exists to show
   `render16eb.py` scoring a blank page 5 of 5 SHOWN. A SUPPRESSED verdict it cannot justify
   is therefore **the instrument manufacturing the evidence it is cited for**: a fabricated
   defect in somebody else's document. A NOT SUPPRESSED verdict it cannot justify merely fails
   to find one, **and the whole of what it can miss is enumerated under `NOT_COVERED` and
   printed on every run.** Under-detection here is bounded and declared; over-detection is
   unbounded and invisible. That asymmetry is the entire reason the column is named
   `not-suppressed` and not `shown`.

3. **There was no single posture to document anyway.** D1 failed **closed** and D2 failed
   **open** and they are **one bug**: an attribute *name* matched by regex over the attribute
   *text*, values included. Documenting the behaviour as it stood would have required the
   sentence *"fails closed on some inputs and open on others, depending on what words appear
   inside unrelated attribute values"*, which is not a safety posture. **This is the fact that
   makes the decision unavoidable rather than a judgement call**, and it is why the ticket's
   "do not just make them agree" is right: there was nothing to agree *with*.

## The proof — both directions, on constructions, against the pre-repair code

`polarity_5f7c.py` runs **sixteen hand-written HTML documents** through `suppressors()` twice:
once as it is in the tree, and once as it is at `6fb424f`, **read with `git show` and executed
unmodified**. No renderer is involved, so the polarity claim does not rest on two npm packages
being installed. A repair whose only evidence is its own new code agreeing with its own new
expectations is not evidence; the pre-repair column is.

**POPULATION: 16 hand-written documents. GRAIN: one document, one marker position, the set of
DECLARED mechanisms reported at that position.**

| | at `6fb424f` | on this tree |
|---|---|---|
| wrong | **6 of 16** | **0 of 16** |
| fails **CLOSED** | P02 P03 P04 P05 P06 | — |
| misses its own **declared set** | P11 | — |

* **P02–P05 — fails CLOSED.** `class="hidden"`, `id="hidden"`, `title="the hidden cost of
  this"` and an unquoted `class=hidden`. Every one is a document with **no stylesheet in it**
  that a browser paints in full, and every one scored SUPPRESSED.
* **P11 — misses its own declared set.** `<details title="open me">` carries no `open`
  attribute, so S1 holds and a reader is shown a closed widget. It scored NOT SUPPRESSED.
* **P13 and P14 — the fail-open posture, executed.** An embedded `<style>` that really does
  blank the page, and `aria-hidden`. Both are in `NOT_COVERED`; both are reported **NOT
  SUPPRESSED**, correctly, at both revisions. **A suppression instrument nobody has seen
  decline to suppress is not evidence of a fail-open posture**, so these two rows are standing
  and go red the moment an out-of-set mechanism starts scoring as suppression.
* `visible_a74f.py` itself carries the same proof through the real renderers as **V5** (the
  repaired `class="hidden"`, 5/5), **V6** (`<details title="open me">`, 0/5 by S1), **V7**
  (V3's blank page behind 3000 `&`, 0/5 by S4) and **V8** (the embedded stylesheet, 5/5 —
  suppression the instrument must decline to report).

### P06 is this repair's own finding, and it is a third face of the same bug

`<div data-style="display:none">` — a `data-` attribute whose **name ends in `style`**. The
pre-repair S5 test was `re.search(r'style\s*=\s*"([^"]*)"', attrs)`, which matches inside
`data-style="…"`. So a document a browser paints in full scored SUPPRESSED by **S5**, and
nothing in mg-65eb's verdict pointed at it. It was found by writing the attribute parser
rather than by reading the report, and it was live at the anchor.

## The offset — and whether it had already been spent

`offsets_5f7c.py`. `main()` took `html.unescape(out).index(marker)` and spent it as an index
into `out`. `&amp;` is five characters of one string and one of the other, so the tag-stack
walk started four characters short per entity ahead of the marker.

**A. The construction.** `visible_a74f.main()` — the real one, with the renderer replaced by a
function handing back one constructed document — over `<div hidden>` behind 3000 `&amp;`. The
row's committed prediction is the correct answer, so a wrong offset is reported by the file
under test **in its own words and in its own exit code**: `not-suppressed 5/5` and exit 1 at
`6fb424f`, `0/5 by S4` and exit 0 on this tree. The marker sits at 15018 in the document and
3018 in the unescaped string; `<div hidden>` is at 15001. The walk started 12000 characters
early, inside the ampersands, and found nothing open.

**B. Had it already corrupted a published figure? Measured, not assumed.**

**POPULATION: mg-a74f's published run — 5 documents × 2 renderers × 5 cited sections = 50
section observations, taken from `6fb424f`'s own `ROWS` rather than retyped. GRAIN: one marker
lookup.**

* **32 of 50** were walked from a position that is not the marker's. (The other 18 are V1's
  ten — inside an HTML comment a renderer escapes nothing — and the eight `H1`s, which sit
  ahead of the first entity.)
* **0 of 10 published row figures change** when the walk is redone at the true offset.

**No published figure of mg-a74f is wrong, and that is luck of row design rather than
instrument correctness.** All five of those documents apply their mechanism to the *whole*
document — a comment around all of it, a `<div hidden>` never closed — so a displaced position
is still inside the same suppression and returns the same verdict. Section A is the same
defect on a document where the displacement crosses the tag, and there it returns the opposite
answer. **A correct number computed by a wrong method is not a correct method**, and the next
document put to this instrument would not have been protected by the shape of the last five.

## `prose_a74f.py` — the three lower-priority findings

`prose_5f7c.py` puts two of them to constructions under restore discipline (snapshot, mutate,
`finally`, and a refusal to start on a dirty tree) and **measures** the third.

| | before, at `6fb424f` | after, on this tree |
|---|---|---|
| **C1** an untracked file satisfying a claim about a *revision* | reference **passes** | reference **FAILS**, and says *present but UNTRACKED* |
| **C2** one extra key `"note"` removes a pinned table | `DELEGATED_PRESENTATION` **leaves** the population | **stays**, and its key mix is printed |
| **C3** a verdict decided by the nearest `.py` basename in 400 characters | attribution not stated | every row says `ON THE LINE` or `BY PROXIMITY` |

* **C1.** P1 says *exists at the revision being read* and resolved against `os.walk`, which
  sees untracked files. An untracked file is at **no** revision: it exists on one disk until
  somebody runs `git clean`, and every reader of every commit gets the dangling reference P1
  passed. `exists` is now `git ls-files`, and *named but only untracked* is reported as its own
  thing rather than collapsed into *absent*. A side effect worth naming: at the anchor the
  probe file was also **in the population of files whose prose gets read** — 19 files against
  18 — so an untracked file could contribute claims as well as satisfy them.
* **C2.** P3's population was *dicts **every** key of which is a repo path*. One `"note"` key
  emptied it, the printed count dropped by one and the check passed because nothing was left
  to fail — in a check whose entire subject is *a pinned table nothing looks at*. The rule is
  now ***any** key is a repo path*, which fails toward checking more; the cost of that
  direction (a dict that merely happens to carry a path key is now required to be iterated) is
  written into the code rather than left to be discovered.
* **C3.** Attribution is now two-tier and **every row says which tier it used**, because a
  co-occurrence on the same line is a measurement and proximity is a guess. A row attributed
  by proximity whose count disagrees with the chosen script and **agrees with another
  candidate in the same window** is now a finding rather than a pass or a fail, since nothing
  in the checker decides which the sentence means.
  **No construction is offered for C3, and that is a decision rather than an omission**: a
  construction here would be a sentence I wrote to be ambiguous, proving only that the rule can
  be fooled by prose designed to fool it. What replaces it is a measurement over the real
  population, printed on every run — **`{'ON THE LINE': 2, 'BY PROXIMITY': 1}` over 3 phrases
  in 18 files**.

## Predictions — 11 of 13 held, and both misses are kept as written

| | held? | |
|---|---|---|
| A1 `class="hidden"` → 5/5 both engines | ✅ | by `(nothing)` |
| A2 `<details title="open me">` → 0/5 by S1 | ✅ | |
| A3 `<div hidden>` behind 3000 `&` → 0/5 by S4 | ✅ | the same answer as the same document with no `&` |
| A4 V0–V4 report the already-committed figures | ✅ | 5/5, 0/5, 0/5, 0/5, 0/5 on both engines |
| A5 the embedded stylesheet → 5/5, fail-open shown | ✅ | the row that would have falsified the decision |
| **A6 the two revisions disagree on the D1 and D2 documents and no others** | ❌ **MISS** | **they disagree on SIX** |
| A7 `unescape_with_map` reproduces `html.unescape` | ✅ | 18 of 18 documents |
| B1 untracked passes before, fails after | ✅ | |
| B2 one `"note"` key drops the table before, not after | ✅ | |
| **B3 ≥1 phrase has >1 candidate in its 400-character window** | ❌ **MISS** | **0 do** |
| B4 same finding count before and after (0 / 4) | ✅ | 0 on the tree, 4 at `bd24efc` |
| exit codes, 7 pre-registered sections | ✅ | 7 of 7 |

**A6's miss is the more useful of the two.** I predicted the old and new code would separate
on exactly the two documents mg-65eb named. They separate on **six**: D1's shape recurs on
four different attributes (`class`, `id`, `title`, and an unquoted value), and **P06 is a
shape neither D1 nor D2 names** — the same bug on S5's `style` test, which nobody had
reported. Writing the prediction from the ticket's two examples imported the ticket's
implicit claim that there were two shapes. There were three, on five attributes.

**B3's miss** is a prediction about this repository's prose that turned out false: every `all
N rows` phrase in the population has at most one script in its window, so the old rule was
never actually choosing *between* candidates here. **The defect was real and its blast radius
was zero**, and that is worth knowing precisely because the repair went in anyway — a rule
that would return an unearned verdict on the next paragraph somebody writes is worth fixing
before that paragraph exists, but the count is 0 and is reported as 0.

## What this repair did NOT do — stated, not left to be noticed

1. **No replacement prediction of where the next gap will be.** mg-a74f predicted its next gap
   would be "a mechanism outside the declared set"; two of the three defects were **inside**
   it and the third was not a mechanism at all, and mg-5f7c's judgement — that the failed
   prediction did more damage than the three defects, because it aimed the next reader away —
   is accepted here. A prediction of that kind is admissible only if it says what would
   falsify it, and I cannot write a falsifiable one about a gap whose shape is unknown by
   definition. **The honest form of "the next gap will be somewhere I am not looking" is
   silence, not a shorter list.** What stands in its place is **V8 / P13**, which is not a
   forecast: it is a row that fires on every run and goes red the moment the instrument scores
   an out-of-set mechanism as suppression.
2. **mg-65eb's R1 is not repaired.** `bytes-in-html` names *the marker present in the
   serialised HTML* and computes *present in `html.unescape(...)`*; on `marked`, `&mdash;`
   markers separate the two sets on all five sections. mg-65eb scored that row NOT SEPARATED
   under its own `all engines` rule. It is **not in mg-5f7c's scope** and is untouched. Note
   that this repair's offset map makes it *cheaper* to repair, not repaired: `index` now
   carries every unescaped position back to its raw one.
3. **The declared set is not enlarged.** No mechanism was added to S1–S5. Widening the set is
   a different decision from correcting an implementation of it, and mixing the two would have
   made the polarity argument unfalsifiable.
4. **mg-16eb's `r16 SHOWN` column is left wrong on purpose**, exactly as mg-a74f left it, and
   `prose_a74f.py`'s exemption list, `_quoted`, P2 and the `REPORTS` mechanism are untouched.
5. **mg-a74f's `PREDICTIONS.md` is not edited**, and neither is any other pre-registration file
   in this repository.

## Four defects of this repair's own instruments, recorded rather than smoothed away

1. **`run_all.sh` section 8 was added after `PREDICTIONS.md`.** The exit table pre-registers
   seven sections; the eighth — `polarity_5f7c.py --rev 6fb424f`, the can-this-suite-go-red
   check — was written afterwards, when it became obvious that a suite reporting `0 of 16
   wrong` proves nothing unless it is shown reporting something else. It is scored as an
   addition, not folded into the seven.
2. **`prose_5f7c.py` mutates the real tree.** Two tracked files and one untracked file, under
   a `finally` and a refusal to start dirty. It is the same discipline mg-a74f's sections 1, 5
   and 6 use, and it carries the same risk: a hard kill between the write and the `finally`
   leaves the tree modified. The run prints `git status --porcelain` at the end and calls a
   non-empty result a finding.
3. **`offsets_5f7c.py` section A replaces `subprocess` inside the module under test** so that
   the construction runs on a machine with no npm packages. Nothing that shim returns reaches
   a measurement — the renderer itself is replaced — but a module whose imports have been
   swapped is not quite the module that ships, and saying so is cheaper than a reader working
   it out.
4. **The polarity suite's "what a browser does" column is my reading of the HTML spec, not a
   browser.** No browser was run. For P02–P06 and P13 that reading is uncontroversial (no
   stylesheet exists in P02–P06; P13's does exactly one thing), but it is a human judgement in
   a table of computed values and it is not marked as computed anywhere but here.

## Two transcripts, and which commit each is a measurement at

`out_run_all_a74f_PRE5f7c.txt` is `code/state_delegation_repair_a74f/out_run_all.txt` **as it
stood before this repair** — kept because a repair that regenerates the transcript it
contradicts leaves no trace of the contradiction. mg-a74f's own `out_run_all.txt` **is**
regenerated here, by its own `run_all.sh`, at the commit that ships this README: section 4 of
it is `visible_a74f.py`, which this repair changed, and a directory that ships a transcript its
own scripts no longer produce is worse than one whose transcript moved.

**Comparing the two shows a staleness that predates this repair**: `README.md:80` in the old
transcript is `README.md:100` in the new one, because mg-0120 added twenty lines to that
README after mg-a74f's run and nothing regenerated the transcript. The same warning mg-a74f
wrote about its own files applies to every file in this directory, **including after the merge
that lands them**.

## Running it

```sh
D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
NODE_PATH="$D/node_modules" sh code/state_suppression_repair_5f7c/run_all.sh
```

Run it on a **committed** tree. Sections 1–4 and 8 need only `python3` and `git`; section 5
needs the renderers and prints the install line and exits 3 without them — **the polarity
claim does not depend on them**, which is why section 1 is renderer-free and comes first.

| file | what it is |
|---|---|
| `PREDICTIONS.md` | committed before any script here existed |
| `polarity_5f7c.py` | the polarity, on 16 renderer-free constructions, beside the code at `6fb424f` |
| `offsets_5f7c.py` | the offset defect, and an audit of the 50 observations already published with it |
| `prose_5f7c.py` | C1 and C2 under restore discipline; C3 measured and the reason it is not constructed |
| `run_all.sh` | all of it, with every exit code checked against `PREDICTIONS.md` |
| `out_*.txt` | the committed transcripts of one full run |
| `out_run_all_a74f_PRE5f7c.txt` | mg-a74f's transcript as it stood before this repair |
