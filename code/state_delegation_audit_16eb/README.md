# `state_delegation_audit_16eb` — the independent audit of mg-0049 / `9ca11c4` + `5594c69`

The object audited is mg-0049's repair of mg-5644's `B1`: the **eighth** control in this
lineage. mg-0049 audited-and-repaired mg-bee1 (`a2d5a81` + `2a29f30`), which repaired
mg-218d, which audited mg-4acd, which repaired mg-babf.

```sh
D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
NODE_PATH="$D/node_modules" sh code/state_delegation_audit_16eb/run_all.sh    # ~12 min
```

## Verdict

**THE REPAIR IS REAL AND NOTHING WAS RETREATED FROM.** mg-5644's `Q1` and `Q2` — the two
rows that showed a reader a blank page at exit 0 — are exit 1, measured on mg-5644's own
battery re-run unmodified. Every committed output of mg-0049's run reproduces
**byte-identically** from this audit's independent run. `141/141`, the `10→6`, the surviving
document-global-ordinal negative, `40/40`, `27` model cases `0` wrong and `negative_control`
`10/10` all stand. The section-8 guard was **extended**, not duplicated: one list, one loop,
the same two guards. **8 of 8** new mutations behaved as this audit predicted before the run.

**AND THE BLIND SPOT MOVED AGAIN — three times, and all three onto ground the repair itself
laid.** That is the eighth generation running, and the second running in which the new gap is
on the repair's own new material rather than on anything it inherited.

| | finding | where it is |
|---|---|---|
| **BROKEN 1** | the repair's own visibility instrument measures **bytes in the HTML** and reports it as **what a reader is shown**, on the one row where the mutation is a *container* — and the blank page it produces is classified **drift**, not damage | `render0049.py`, `out_render.txt`, the exit-code table |
| **BROKEN 2** | the repair added a **second pinned table** and published that the two tables "cannot drift apart quietly in **either** direction". One direction is real; the other exits **0** | `delta_control.py:757`, `DELEGATED_PRESENTATION` |
| **BROKEN 3** | a cited section a reader is shown **in full** is reported as one **"THE READER IS SHOWN NOTHING OF"**, at **exit 1**, and the instrument's own documented recovery **does not clear it** | `is_presented()` over the new whole-section span |
| **MINOR 1** | `delta_control.py` points at a file that does not exist, with the wrong row count — in the one document no checker in this repository can check | `delta_control.py:233` |
| **MINOR 2** | the "What is NOT undone" table's two cross-references both name the wrong `run_all.sh` section | `README.md:105-106` |
| **MINOR 3** | `position` is inert on the delegated surface, which is disclosed; that this makes the surface strictly weaker than the certified one *in a field the certified one carries* is not | `region_record`, measured by `B1` |
| **MINOR 4** | the stated baseline commit is two commits before the repair's actual parent | `delta_control.py:753` |

**None of the three BROKEN is on mg-0049's own list of where it might have failed.** That
list names `R3`/`R4`, `delegation_map()`'s derivation, and `L2`. mg-a61f established the rule
this audit applied: a self-filed list of one's weak points **directs attention**, and the
broken row is the one it omits. Eight for eight, that rule has now held.

---

## BROKEN 1 — the visibility instrument measures the artefact, not the reader

`render0049.py` is the file mg-0049 built to answer *"what is a reader shown?"* for its five
new rows. On `R5` it records, and `out_render.txt` prints:

> `R5` `<details>` at the top **SUPPRESSES NOTHING**: every cited section is still on the
> page as the document's own prose … `marked  ANY 5/5  HEADING 5/5` …
> `markdown-it  ANY 5/5  HEADING 5/5`

Both numbers are correct. Neither is the question. `render16eb.py` runs the same mutation
through the same two renderers and, instead of stripping the tags, **walks the tag stack**:

```
B3  <details><summary> at the top of the target
    marked       text-in-html 5/5   SHOWN TO A READER 0/5
                 every cited section sits inside [1] closed <details> element(s); </details> in page: 0
    markdown-it  text-in-html 5/5   SHOWN TO A READER 0/5
                 every cited section sits inside [1] closed <details> element(s); </details> in page: 0
```

`<details>` is a normal element. Unclosed, it runs to the end of the document, so **every
cited section is its descendant on both renderers**. It carries no `open` attribute, and per
the HTML Standard a browser renders such an element's summary and nothing else until the
reader clicks. **A reader following the certified cell's six links is shown a disclosure
triangle.** That is `R1`'s and `R8`'s outcome — the blank page this whole repair exists to
catch — reached by a construct that is neither malformed nor exotic.

What the control does about it, and why this is a finding rather than a miss:

* the control is **not blind**: the raw-HTML guard fires, so `R5` and `B3` exit non-zero;
* but they exit **2**, which `delta_control.py`'s own table defines as drift — *"Re-baseline
  this instrument, record the new figure, and say which commit moved it"*. The documented
  response to a blank page is to **accept it**;
* `split_0049.py`'s `R5` row records `presented: 0`. The presentation record — the mechanism
  this repair was built to extend — **does not see it**. Only the guard does, and the guard's
  verdict is drift;
* `B3` shows the same page built with a `<summary>`, so it reads as an ordinary collapsible
  rather than as damage.

**Why this is the lineage's signature defect and not a detail.** mg-4acd was landed to stop
certifying *"are these the certified bytes?"* and start certifying *"is a reader shown
them?"*. `render0049.py`'s `ANY`/`HEADING` columns are the first question wearing the second
question's name. The regression is in the repair's own instrument for the distinction, on the
one row of its five where the mutation is a **container** rather than a **suppressor** — and
the verdict paragraph generalises from it: *"`R5`, `R6` and `R9` are the honest half. In all
three, every cited section is still on the page, as the document's own prose, on both
renderers."* For `R6` and `R9` that is true. For `R5` it is false.

---

## BROKEN 2 — a second pinned table, without the cross-check the first one has

`delta_control.py:757`, over the table the repair added:

> A cited section present in `DELEGATED` and absent here has no certified record, so its
> comparison fails and exits non-zero: **the two tables cannot drift apart quietly in either
> direction.**

Measured, on this audit's harness, with every exit code predicted before the run:

| row | mutation | predicted | observed |
|---|---|---|---|
| `A3` | a delegated section's **presentation record deleted** | 2 | **exit 2** |
| `A1` | a presentation record for a section **nothing delegates or cites** | 0 | **exit 0** |
| `A2` | a **whole target file** certified here and delegated by nobody | 0 | **exit 0** |
| `A5` | *(control)* the same shape on **mg-bee1's** table: a content digest deleted | 2 | **exit 2** |

One of the two directions is real. Nothing iterates `DELEGATED_PRESENTATION`: section 2c
iterates `DELEGATED` and looks rows up with `.get(target, {}).get(name, "")`, so a row that is
in the new table and in nothing else is never visited, and neither is a whole file.

`A5` is what makes `A1` mean something. mg-bee1's table does **not** have this hole — its keys
are cross-checked against the sections the certified text actually cites, which is the check
`delegation_map()` exists to provide. The repair added a second table beside it and did not
give it the same treatment.

**This is `L2` one level up.** `L2` — *"a digest over a chosen set of regions cannot see a
region that is not on the set"* — is named as still open in `COVERAGE.md`, in
`delta_control.py`'s header and in mg-0049's README, three times, as the next auditor's
target. The repair then created a new chosen set with the same property, in the instrument
itself, and published a sentence saying it had not.

---

## BROKEN 3 — a section shown in full, reported as shown to nobody, at exit 1, unrecoverable

`region_record`'s `state` is the **set** of states over the span; `is_presented()` accepts
only the singleton `"rendered"`. That is right for a certified region, which is a paragraph or
a quote block and cannot contain a fence. A **delegated section** is a heading and everything
under it, in a history document about a computation.

`C1` adds one ordinary, closed, fully visible code example to cited section `H3`:

```markdown
An example of that rescaling, so a reader can check it:

```python
d_true = np.diag(row_signs) @ d_allplus
```
```

Both renderers, measured: **5 of 5 cited sections shown**, the example rendered as a
`<pre><code>` block, its text on the page. The control:

```
[FAIL] docs/state-history/attempt-mg-276d.md H3: PRESENTED to a reader
       state      fenced-code+rendered
       >>> THE CERTIFIED CELL SENDS A READER TO THIS SECTION AND THE READER IS SHOWN NOTHING OF IT.
```

**exit 1.** The sentence is false: a reader is shown every line of the section.

Then the part that makes it more than a wording defect. `delta_control.py` publishes exit 2 as
recoverable — *"Re-baseline this instrument, record the new figure"* — and exit 1 as damage.
`battery16eb.py`'s section 2 follows that recovery path to the letter: it runs the
instrument's own `--emit-baseline` against the mutated tree and splices **both** regenerated
tables back verbatim, with no hand edits.

```
  before re-baselining        exit 1
  after  re-baselining        exit 1   (PREDICTED BEFORE THE RUN: exit 1)
```

`is_presented()` is checked before, and independently of, the baseline. **There is no
recovery.** The target file cannot gain a code example inside a cited section without the
control reporting damage, permanently, and the only way out is to edit the instrument.

mg-0049 printed one cost — `R9`, a tab in uncited prose, exit 2, re-baselineable — and was
right to. This cost is strictly worse and is not among the nine. The proximate cause is a
sentence in `region_record`'s new docstring that is true about the code and false about the
semantics:

> `state` is the set of states over the WHOLE span … **That is what makes this one function
> serve a certified region (a few lines) and a DELEGATED SECTION (a heading and everything
> under it) without a second mechanism for the second.**

One function does serve both. It does not answer the same question about both, because
*"every line of this span is prose"* is the right predicate for a paragraph and the wrong one
for a section.

---

## MINOR 1 — the one document nothing in this repository can check

`delta_control.py:233`, added by this repair:

> `code/state_delegation_repair_0049/guards_only_0049.py` runs the guards-only control against
> all **six** rows and prints the split.

There is no such file. The script is `split_0049.py`, and it runs **nine** rows — six is
mg-5644's population, not this repair's. `COVERAGE.md`, `code/state_delegation_repair_0049/README.md`
and `code/state_landing_control_2da3/run_all.sh` all name it correctly.

**The one that does not is the one nothing checks.** mg-218d built `coverage218d.py` to check
`COVERAGE.md`'s sentences against the code, and it does that by reading `delta_control.py`
**as the ground-truth box** — so by construction it cannot check a claim made inside it. This
repair added **fifty-seven lines** of new load-bearing prose to that file's header, including
the restated bound, the exit-code semantics and the `DELEGATED_PRESENTATION` provenance.
`claims16eb.py` is the check that did not exist:

```
11 of 16 checkable claims mg-0049 ADDED hold against the tree.
WHERE THE BROKEN ONES ARE.  3 of the 5 are in delta_control.py, the file coverage218d.py
reads as the ground truth box and therefore cannot check.  0 are in COVERAGE.md, the one
added document that has an external checker.
```

That distribution is the finding. **The checked document is right; the unchecked one is
wrong, in the same paragraph, about the same script.** It is the asymmetry between *files we
read* and *files we point at* — the exact defect mg-0049 was filed to repair — recreated one
level up, in documentation rather than in mechanism.

## MINOR 2 — the over-correction table's own pointers

mg-0049's README, "What is NOT undone" — the table that answers the over-correction question:

> mg-218d's 16-mutation battery, **unmodified** … re-run in **section 7** of `run_all.sh`
> mg-5644's own battery, **unmodified** … re-run in **section 7**

Section 7 is `coverage218d.py`. mg-5644's battery is section **8**, and mg-218d's sixteen are
re-run inside it, via mg-5644's own `run_all.sh` section 5. The re-runs themselves happen —
this audit reproduced both byte-identically — so only the pointer is wrong. It is recorded
because a claim in the table that answers "did you retreat from anything?" is load-bearing.

## MINOR 3 — the delegated surface is weaker than the certified one, in a certified field

`B1` exchanges cited sections `H3` and `H4` in the target. Not one byte of either changes;
both keep their certified heading path; both are prose; both renderers show them **in the new
order**. **exit 0.**

On the two files the instrument *reads*, a certified region's ordinal among the blocks of its
section **is** certified — `position` is one of the four fields of every presentation record,
with its own group of cases in `presentation.py`'s self-test (`_POSITION_CASES`). On the file
it *points at*, `position` is inert. `B2` is
the control: move one cited section verbatim under a different parent and the record moves,
exit 2 — so the record is read, and it is `position` specifically that carries nothing here.

mg-0049 discloses that `position` is inert, in `delta_control.py` and in `COVERAGE.md`, and
says why (a section is not a block, so it has no ordinal among blocks). That is correct and it
is the reason this is MINOR rather than BROKEN. What is not said is the consequence: the
delegated surface is **not** read "exactly as" the certified one, in a field the certified one
certifies, and the repair's own PASS banner says *"the same two questions are answered for 5
DELEGATED sections"*.

## MINOR 4 — provenance

`delta_control.py:753` says *"Baselined by mg-0049 against the working tree at `8ce78fb`"*.
`8ce78fb` is mg-5800's commit, two before mg-0049's actual parent `db2b77d`. Harmless: the
target file is byte-identical at `8ce78fb`, `db2b77d` and `HEAD`, and `claims16eb.py`
recomputes all five records from `8ce78fb` and gets the pinned values. Recorded because this
lineage's own rule is *"say which commit moved it"*.

---

## What was checked and found intact

| the brief's question | answer, and how it was measured here |
|---|---|
| were mg-5644's and mg-218d's batteries re-run **unmodified**? | **yes**, by `git diff` and not by reading the committed outputs. `git diff a4aeeb9..HEAD -- code/state_layer_audit_218d/` and `git diff 3a80d99..HEAD -- code/state_delegation_audit_5644/` are both **0 bytes**. mg-bee1's directory has a 2,111-byte `.md` diff (the correction of record, appended under the row, leaving the row verbatim) and **0 bytes** of non-`.md` diff |
| do the committed outputs reproduce? | **yes, byte-identically**, all six, from this audit's own runs: `out_battery_0049.txt`, `out_split.txt`, `out_render.txt`, `out_coverage218d.txt`, `out_5644_rerun.txt`, and `state_landing_control_2da3/out_control.txt`. **0 figures in this repair are unreproduced** |
| was the section-8 guard **extended** or **duplicated**? | **extended.** One `guarded` list, one loop, the same two guards, `STATE.md` and the README and every declared target in the same iteration. No second mechanism |
| over-correction — did `141/141`, the `10→6`, the statement repair or the document-global-ordinal negative retreat? | **none of them.** `render218d.py`: `141 of 141`. mg-218d's sixteen re-run inside mg-5644's: `6 of 16` silent, down from 10, with `P2 P3 P4 P6 S1 I1` still the silent list. `globalpos_bee1.py` re-run unmodified and byte-identical: the negative stands. `presentation.py`: `27 cases, 0 wrong`. `negative_control.py`: `10/10`. `coverage218d.py`: `40 of 40` |
| was the bound restated in terms of **what a reader is shown**? | **yes, and the restatement is sound** — but see BROKEN 1: the *instrument* that measures "what a reader is shown" was not restated with it |
| is the stated bound (`R3`, `R4`) honest? | **yes**, re-measured here rather than inherited. Both still exit 0, deliberately, and both are named in three documents |
| did the repair weaken what it inherited? | **no.** `A5` fires, `R7` fires, mg-bee1's `T1`/`T2`/`T3` shapes all still fire |

## The eight new rows

Every exit code was written into `mutations16eb.py` and committed **before** `battery16eb.py`
was executed once. **8 of 8** behaved as predicted.

| | surface | mutation | predicted | observed |
|---|---|---|---|---|
| `A1` | the table mg-0049 **added** | a presentation record for a section nothing delegates or cites | 0 | **0** |
| `A2` | the table mg-0049 **added** | a whole **target file** certified here and delegated by nobody | 0 | **0** |
| `A3` | the table mg-0049 **added** | a delegated section's presentation record **deleted** | 2 | **2** |
| `A5` | mg-bee1's table *(control)* | a delegated section's **content** digest deleted | 2 | **2** |
| `B1` | reader order, cited | two cited sections **exchanged**; no byte of either changes | 0 | **0** |
| `B2` | heading path *(control)* | one cited section moved verbatim under a different parent | 2 | **2** |
| `B3` | blank page, classified | `<details><summary>` at the top: a **closed widget** over the whole page | 2 | **2** |
| `C1` | the whole-section span | an ordinary **code example** inside a cited section, fully shown | 1 | **1** |

Plus one construction that is not a row: `C1` followed by the instrument's own documented
recovery path, `--emit-baseline` and both tables spliced back verbatim — **still exit 1**.

Six of the eight are aimed at what mg-0049's self-filed list does **not** name. Four of the
eight are controls whose only job is to make the other four mean something.

## Where I would look next, in order

1. **`is_presented()`'s predicate on a span that is a section.** The honest question about a
   section is not *"is every line prose?"* but *"is every line **shown**?"* — a fence is
   shown, and `FENCED_CODE`'s own comment in `presentation.py` says so in those words
   (*"shown, but as a code sample"*). The two are conflated only because the certified surface
   could never tell them apart.
2. **A visibility measure that walks the tag stack rather than stripping tags.**
   `render16eb.py` does it in thirty lines. The visibility measures in this cluster's
   renderer evidence — `render218d.py`'s plain-run scan and `render0049.py`'s `ANY`/`HEADING`
   columns — both answer "is the text in the rendered output?", which is the question this
   lineage exists to stop asking. `<details>` is the first construct that
   separates the two, and it will not be the last: `hidden`, `aria-hidden`, and any element
   with a `style` attribute do the same.
3. **A checker for `delta_control.py`'s header.** `coverage218d.py` cannot be it — it reads
   that file as ground truth. `claims16eb.py` is a start and is scoped to one diff; the
   general form is that **every document in this cluster needs a checker that is not itself**,
   and `delta_control.py` is currently the only one that has none.
4. **`L2`, and now on three surfaces.** Still open on the certified region set, open on the
   target's own sections, and now open on `DELEGATED_PRESENTATION` itself.

## Files

| file | what it is |
|---|---|
| `harness16eb.py` | this audit's own snapshot / restore / exit-code harness — the sixth, sharing no code with the five before it. Unlike them it can mutate the **instrument**, which is what `A1`–`A5` require |
| `mutations16eb.py` | the eight mutations, with the exit code predicted before the run written into the file |
| `battery16eb.py` | the eight against the real control as a subprocess, plus the **recovery demonstration** |
| `claims16eb.py` | every checkable claim mg-0049 **added**, checked. Scope is the diff, not the repository |
| `render16eb.py` | what a reader is **actually** shown, on `marked` and `markdown-it`, with the tag stack walked rather than the tags stripped |
| `run_all.sh` | all of the above, plus the three `git diff` proofs and mg-5644's whole audit re-run unmodified |

`out_*.txt` are the committed outputs of a single run of `run_all.sh`.

## Safety

`battery16eb.py` mutates tracked files in the working tree — `STATE.md` is never among them,
but `delta_control.py` is — and restores every one under a `finally` plus a sha256 check. It
refuses to run if any file it is about to touch is already dirty in git. Run it on a committed
tree.
