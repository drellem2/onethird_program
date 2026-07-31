# mg-70c7 — the six findings of mg-dee4, repaired

`mg-dee4` is the independent audit of `1ee1f1b` (mg-7522), which repaired the
three open sites of `682db2c` (mg-05eb), which audited the arc-wide `| tee`
sweep `52aeaf4` (mg-c2b3). This tree lands its six findings.

Instrument: `sh run_all.sh`, about 4 minutes, pure Python 3, no dependencies,
no network. Every figure below is printed by a probe here next to the predicate
that produced it, and the transcripts are committed.

**`PREDICTIONS.md` was committed before any probe in this directory existed**
(`93bd689`), so the order is checkable from `git log` rather than asserted in
the file. Two of its predictions missed and are kept as written.

---

## The six, and where each is repaired

| | finding | repaired at | checked by |
|---|---|---|---|
| **F1** | *"11 of 11 read directly"* is **eleven LINES**, and four of the eight runs those lines execute were never run | `s2_status.py` — the hand-list is now a derivation from the runners' own bytes, at the execution grain | `r1_grain.py` |
| **F2** | the published `154 changed files` is reproduced by **no anchor** | the document points at `out_s4_unpin.txt`; a **figure census** makes the rule a check | `r2_anchor.py` |
| **F3** | it judged its subject by a **9-alternative** rule and itself by a **3-alternative** one, over a population that excluded every `.md` | one rule object, `lib7522.MARK`; the `.md` and the document join the population; BACKED / UNBACKED replaces a count of uses | `r3_strength.py` |
| **F4** | the CLAIM rule is **line-local** and the strongest claim wrapped | `s3_figure.WINDOW = 1`, applied in both directions; 20 → **24** | `r3_strength.py` |
| **F5** | the caller scan is still a **name** rule, now with two names | `libc2b3.targets` — the property, in the sweep's own library, with the sweep's own both-senses fixtures | `r4_property.py` |
| **F6** | a status-consuming pipeline outside the population, missed by all three rules for three different reasons | `lib7522.consumed` is a named **disjunction**: errexit **or** value | `r5_population.py` |

And **R6**, the section about the instrument: the same four questions turned on
this tree.

---

## F1 — a source line inside a loop is N executions

The three `git diff … | wc -c` lines sit inside `for pair in …` loops and
execute **eight** discarded `git diff`s between them. mg-7522 covered them with
a **hand-list of three argv containing two distinct commands**, so four of the
eight runs were never executed — and one row was labelled
`state_delegation_audit_16eb/run_all.sh:39` while carrying an argv without the
`':!*.md'` pathspec that line 39 has, so **that form was never run in any
shape.**

The rows are now **derived**: the loop header expands to its literal items, the
body's own `base=${pair%% *}` assignments are followed, and `lib7522.argv_of`
returns `None` rather than leaving an unresolved `$` in a command it is about to
run. `r1_grain.py` re-derives them under a parser written here — `lib7522` has
the derivation because that is where the check lives, and `lib70c7` has its own
because a repair that re-derived its subject's number with its subject's parser
would agree with itself by construction.

**The verdict survives and the enumeration does not.** All eight exit 0.

## F2 — a rule stated in prose is applied where the author was looking

`c252f96` wrote *"a number that moves belongs in a transcript"* and applied it
to the 2×2 totals **three paragraphs above** a bare `154 changed files` that no
anchor reproduces. So the repair is not only to move that figure: `r2_anchor.py`
runs a **figure census** — every number in a reader-facing artifact against
every figure its own tree's transcripts print — and `s5_self.py` runs the same
census on this tree's own artifacts.

**A defect in that census, recorded rather than smoothed away.** Its first draft
built the corpus by matching every number in the transcript text. Under that
rule `154` came back **BACKED** — by the string `s3_figure.py:154` in
`out_s5_self.txt`. A **line number** was backing a measurement, and the census
would have blessed the exact figure it was written to catch.

## F3 / F4 — apply to yourself the rule you apply to your subject

`verified` was named as one of the three markers in `s5_self.py`'s own D4
docstring, in mg-7522's README and in the published document — and was **in the
nine and not in the three**. There is one rule object now; `s3_figure` and
`s5_self` share it, so a marker added for one is added for both by construction.

The population was `*.py` + `*.sh`, which is a name rule with one letter
changed. It now includes this tree's `*.md` **and the published document** —
the kind three of `mg-05eb`'s four wrong artifacts were.

And the verdict changed shape. `0 USES` under the widened rule is not
attainable and should not be: a bare marker beside a figure the tree **computed**
is not the defect. A USE is **BACKED** when every figure in its window appears in
a transcript this tree commits, and **UNBACKED** otherwise. Only UNBACKED is
counted, and a USE with no figure is listed under a **stated limit** — D4 asks
whether a NUMBER stood on a word, and a qualitative marker is outside its reach.

The claim rule was line-local. With a one-line window in either direction,
mg-c2b3's artifacts go from **20 to 24** — and the claim `mg-dee4` most wanted to
check, `OUTCOMES.md:88`'s *verified* with its figure on line 89, scored as
neither line.

## F5 — the property, stated where the check lives

`run_all\.sh` → `(?:run_all|run_audit)\.sh` is **one filename replaced by two**.
At HEAD, **9 executing sites name a `*.sh` whose basename is neither**, 4 of them
reading the status, and **0 name the `run_audit.sh` the widening added**. The
property was stated in `lib7522` — one directory over from the check. It is
`libc2b3.targets` now, in the sweep's own library, used by the sweep's own scan,
pinned by five both-senses rows in the sweep's own self-test.

> A caller is a line that executes something and names a shell script.

The widening **loses nothing** — `r4_property.py` checks that direction too —
and the two limits that remain are named at the rule.

## F6 — fix the population; the instance is secondary

P2's consumption test was errexit at file grain; the reason written for it was
about the **value**. `lib7522.consumed` is now a disjunction with both arms
named and printed on every row. At `bee07a1` it takes P2 from **19 / 26** to
**20 / 27**; at HEAD from 0 to **1**, and the one is
`code/branching_audit_a218/c0_repro.sh:47`.

That site is **not repaired**, and the reason is measured rather than argued:
`r5_population.py` runs the real script twice on a scratch copy of its own
bytes, once as committed and once with the discarded `grep` given an option it
rejects. As committed: **exit 0**. Forced: **exit 1, printing `DISAGREES`.** The
direction is **loud**, which is the opposite of the silent green mg-c2b3 swept
for — a hole in a population, now filled, and not a live swallow.

---

## What was regenerated, and what deliberately was not

`out_k1_census.txt` is **not** regenerated. It is the transcript recording
`ticket 1 / re-derived 0 / DIFFERS`, and `mg-05eb` cites it as that record; the
regex is repaired, so a re-run would print `AGREES` and destroy the citation.
`out_selftest.txt` and `out_k2_consume.txt` in that tree **are** regenerated,
because the rules they exercise changed and a transcript of a rule that no
longer exists is not a record of anything.

mg-7522's six transcripts are all regenerated: its probes changed.

## What this repair does NOT establish, named rather than folded into a total

* **That the value arm is the RIGHT widening.** F6 is a disagreement with a
  definition. `lib7522.consumed` is written out in full so that disagreeing with
  it is possible.
* **mg-c2b3's own 34.** Still cited, still not re-measured. The covered set is
  *16 executions run here + 8 `| tee` sites mg-7522 derived + 34 inherited from a
  transcript nobody in this chain has re-run.*
* **That a BACKED figure is backed by the RIGHT measurement.** The backing test
  asks whether a figure appears in a transcript, not whether it appears as the
  answer to the same question. Weak in one direction, and every row prints the
  figure so the sense is checkable by eye.
* **Every intermediate commit.** Read at `HEAD`, on one machine — inherited from
  mg-7522's own statement of the same limit.
