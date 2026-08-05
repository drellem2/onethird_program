# `code/branching_bound_audit_aaf4/` — the instrument for mg-aaf4

**This audit was PRE-FILED IN THE SAME ACTION AS ITS PARENT.** `mg-aaf4` and `mg-d075` were
created by pm-onethird in one action on 2026-07-31, before mg-d075 had written a line — which
is the standard for this lineage and the reason mg-d075's own account could say, in advance,
*"mg-aaf4 is told not to inherit 9. It should not."* I did not choose my scope and mg-d075
could not choose it for me.

**What this measures.** Two things the brief names, and one it does not.

1. **The sites, counted by me** — not 4, not 8, not 9, not 10 — at two grains and over a
   universe that is not the glob `docs/*.md`.
2. **Every sentence in which mg-d075 faults someone else's scope, checked for its own** —
   against the standard mg-d075 applied to the *document*, not the one it applied to itself.
3. **The floor**: the liveness rule of this whole arc cannot tell a struck claim from a
   quotation of the strike marker, and no transcript in the arc prints what that removes.

```
sh code/branching_bound_audit_aaf4/run_all.sh     # ~40 s, no network, no deps
```

**`run_all.sh` EXITS 1 AND IS SUPPOSED TO.** `a5` was predicted **0** and returns **1**. That
miss is a result — see §6 — and the prediction is left exactly as it was committed. A runner
made green by rewriting the prediction it missed would be worth nothing.

---

## 1. THE FILES

| file | what it is |
|---|---|
| `PREDICTIONS.md` | 16 predictions and 8 exit values, committed at `f714b4c` **before any `.py` in this directory existed**, with all 15 hand commands run beforehand disclosed, and with **P-0 marked NOT A PREDICTION** because it was already measured |
| `lib_aaf4.py` | my reader. A re-implementation — it imports neither `lib_d075` nor mg-19ec's `e5_population.py`. Two grains, a file-list universe, and the NUMERIC-SCOPE/KEYWORD separation the parent has and does not turn on itself |
| `a1_population.py` | **I count the sites myself.** Seven populations, two grains, and the finding that the parent's own deliverable is half outside every population it counts |
| `a2_reproduce.py` | **reproduce before disagreeing** — mg-19ec's 8/4/4, mg-d075's 9/4/5 and its 10/10/0, all three matched row-by-row and text-by-text against the committed transcripts |
| `a3_criticism.py` | **the repair read as a claimant** — the parent's ten criticism sentences re-scored by the standard the parent set for the document, the prose file its self-check never looked at, and the same predicate turned on me |
| `a4_selfapply.py` | **the self-application ledger** — 9 charges mg-d075 lays, each measured on mg-d075 |
| `a5_donotdisturb.py` | **do not disturb**, and the provenance of what landed, by `patch-id` rather than by ancestry |
| `selftest_aaf4.py` | 17 cases, every document mutation asserted a real change before its verdict is read |
| `out_*.txt` | committed transcripts of the run in this commit |
| `out_a3_criticism_FIRSTFORM_exit1.txt` | the criticism check's **first form** — kept because respecifying it moved a number **towards** my own finding |
| `out_selftest_aaf4_FIRSTFORM_exit1.txt` | the self-test's **first form, 2 cases failing** — kept because one of the failures was mg-d075's own floor finding reproducing itself on me |

---

## 2. THE HEADLINE — the count, and the instrument that made it possible to disagree

**The instrument is the answer to "could you have found a different number?".** Mine differs
from the parent's in exactly three declared ways, and one of them produced the finding:

| | mg-19ec | mg-d075 | mg-aaf4 |
|---|---|---|---|
| unit | para / cell | para / cell | **para / cell — kept, on purpose** |
| grain | sentence | sentence | **sentence AND occurrence** |
| universe | one file | one file + `docs/*.md` | **a FILE LIST; `docs/` is not the boundary** |

**Population: live sentences of `docs/OneThird-Branching-Graphs-Where-This-Lives.md`. Grain:
one sentence.** Pre-repair STRICT **8 / 4 / 4**; pre-repair RELAXED **9 / 4 / 5**; as it
stands **10 / 10 / 0** under both. **All three are mg-d075's published values and all three
reproduce**, row for row and text for text, before this audit disagrees with anything (`a2`,
0 reproduction failures over 27 rows).

**Where the number changes is the universe.**

**Population: every markdown file tracked by git. Grain: one sentence.**

| | files | sites | unbounded |
|---|---|---|---|
| mg-d075's published corpus D (`docs/*.md`) | 7 | 36 | **12** |
| this audit, tracked `*.md` | **13** | **51** | **24** |

**TWELVE OF THE TWENTY-FOUR UNBOUNDED SITES ARE OUTSIDE `docs/`.** The published corpus figure
is exactly half of the population, and the glob is the whole of the reason.

**Population: the files mg-d075 itself authors or edits that state the figure. Grain: one
sentence.**

| file | sites | unbounded | inside the parent's gate |
|---|---|---|---|
| `docs/OneThird-Branching-Graphs-Where-This-Lives.md` | 10 | 0 | yes |
| `docs/repair-mg-d075-the-figure-and-its-scope.md` | 6 | 0 | yes |
| `code/branching_bound_d075/README.md` | 3 | 0 | **NO** |
| `code/branching_bound_d075/PREDICTIONS.md` | 4 | **4** | **NO** |

**FOUR FILES, TWO GATED, AND ALL FOUR UNBOUNDED SITES IN THE UNGATED HALF.** mg-d075's §5
says *"the corpus of this figure is now 7 files of `docs/` … my gate covers 2 of the 7"*. Over
its own deliverable the ratio is 2 of 4, and the two it cannot see are the two it wrote about
itself.

**AND THE PART THAT IS NOT A CRITICISM.** Those four sites are in a **pre-registration
commit**, and this lineage does not amend, reword, squash or rebase one away. Adding a bound
to a sentence of `PREDICTIONS.md` is a rewording. **So the bounding standard and the
pre-registration standard are in conflict on exactly this population, and mg-d075 could not
have repaired those sites without breaking a different invariant.** What it could have done,
and did not, is *name* the population as excluded by that invariant instead of drawing the
glob so that it never appeared. **My own `PREDICTIONS.md` carries 4 unbounded sites of the
same figure for the same reason, and I do not repair them either** (`a1` U5).

**Grain O.** The same file, counted by occurrence rather than by sentence: **11, not 10** —
one sentence states the figure twice. Neither number is wrong; they answer different
questions, and mg-d075 publishes one of them.

---

## 3. THE HARDER HALF — the repair read as a claimant

`s5_own_criticism.py`'s docstring says of its own standard:

> *A neighbouring sentence does not rescue it — that is precisely the standard this repair
> applied to the document, and applying a weaker one to myself would be the defect a second
> time.*

**It is a weaker one.** The standard applied to the document is `s4_hedge.py`'s H3: every
site's bound is classified NUMERIC SCOPE or SOFTENING WORD and only a numeric scope passes.
The standard `s5` applies to the repair's own sentences also accepts the bare words
`population`, `grain`, `live sentences`, the tokens `STRICT` / `RELAXED` / `POP-<n>`, and a
bare path `code/…`.

**Population: mg-d075's 10 criticism sentences. Grain: one sentence.**

| | count |
|---|---|
| pass `s5`'s own OWNSCOPE | **10 of 10** — mg-d075's published result, reproduced exactly |
| pass H3's standard (a numeric scope in the sentence) | **7 of 10** |
| **the gap** | **3** |
| **after hand adjudication** (`a3` C2b, both numbers published) | **1** |

The hand adjudication overturns two of the three as false negatives of *my* classifier and
leaves one standing. **The one that stands is the repair's own headline sentence:**

> ***FOUR was not the population, and EIGHT is not either.** The brief for this repair told me
> not to inherit 8; mg-aaf4 is told not to inherit 9.*

It asserts of two published figures that they are not the population, and names in its own
sentence neither the population, nor the file, nor the grain. The table that carries all three
is nineteen lines above it. **A sentence faulting two predecessors for stating a figure away
from its scope, stating a figure away from its scope.** That is the same shape as the §2.1
defect mg-d075 found in mg-dffa, one level up.

**And the population was short by a file.** `s5`'s `MINE` lists two documents; mg-d075
authored three. `code/branching_bound_d075/PREDICTIONS.md` contains **8 criticism sentences
under mg-d075's own FAULT ∧ TARGET predicate**, 6 of them with no numeric scope, and none of
them was ever looked at (`a3` C3).

**AND THE DETECTOR MISSES THE SENTENCE IT WAS WRITTEN FOR, BY ONE TENSE.** `s5`'s `FAULT`
regex lists `cannot see`. The sentence in mg-d075's own account that describes the defect this
whole repair exists for reads *"mg-19ec's POP-3 predicate **could** not see it"* — and is
therefore not a criticism sentence as far as `s5` is concerned. Under my wider predicate the
parent's prose yields **25** criticism sentences against its own **18**, and **8** are visible
only to mine, 6 of them with no numeric scope (`a3` C5). The gap is not a scandal; it is the
ordinary fate of a regex over prose, and it is the reason `s5`'s own transcript ends by saying
*"a defect outside the predicate is invisible to it. mg-aaf4 is asked to pick a different
one."* This is that different one.

**MYSELF.** `PREDICTIONS.md` P10 said in advance this check would fire on me. It does, hard.
**The count is printed in `out_a3_criticism.txt` and is deliberately not asserted here: this
README is inside the population C4 measures, so a figure quoted in this sentence changes the
figure the next run prints.** That is mg-d075's own lesson — its P6 was refuted for exactly
this reason — and the honest form is to point at the instrument. My predicate is deliberately
wider than the parent's, so my count is not comparable to its 0; what is comparable is the
direction, and it is the same one.

---

## 4. THE SELF-APPLICATION LEDGER

`a4` takes **9 properties mg-d075 faults somebody else for**, locates each charge in the file
at run time, and measures the same property on mg-d075. **4 SELF-APPLIES, 5 FAILS.**

| | the charge | measured on mg-d075 | |
|---|---|---|---|
| F1 | *"**26** is a hand-written literal no instrument computes"* | its README says **253** live sentences of its own prose, **twice**; its own committed transcript says **254**, twice | **FAILS** |
| F2 | *"that audit's transcript never prints a token count at all"* | its own transcript prints its own token count **2** times | SELF-APPLIES |
| F3 | *"One audit, two instruments, and only the smaller number reached the verdict"* | `s4`'s H3 banner names a population of **9**; the same block prints **10** rows and its own SUMMARY says **10 of 10**. The banner is a hardcoded literal | **FAILS** |
| F4 | *"mg-19ec's POP-3 predicate could not see it"* | the glob `docs/*.md` cannot see **12** unbounded sites, against the **12** it reports | **FAILS** |
| F5 | *"silently loosening a check that fires is exactly what these audits exist to catch"* | **2** first-form transcripts committed (this audit commits **2**) | SELF-APPLIES |
| F6 | *"FOUR was not the population, and EIGHT is not either"* | that sentence's own scope: **KEYWORD ONLY**, hand-adjudicated **NO SCOPE** | **FAILS** |
| F7 | *"Every number in this document is stated with the population it is over and the grain of the value"* | a counterexample from the same document — F6's sentence | **FAILS** |
| F8 | *"9 of 9 exit values matched"* | `run_all.sh` scores **7**; the arithmetic is disclosed in `PREDICTIONS.md`, so this is a grain gap and is recorded, not charged | SELF-APPLIES |
| F9 | *"This repair does not install one"* | **4** explicit statements that the class is not fixed, **0** claiming it is | SELF-APPLIES |

**The five failures share one shape, and it is not carelessness.** mg-d075 drew each of its
populations at a boundary that put its own instrument outside, and then measured honestly
inside the boundary. The arc's defect is a figure without its scope; this is **a scope without
its figure**.

---

## 5. INSTANCE, CLASS, OR NEITHER

mg-d075 computes **INSTANCE + REUSABLE ARTEFACT, not the class**, and says plainly that a
repo-wide check is what would address the class and that it does not install one. **I agree
with that verdict and I sharpen it in one direction:** the reusable artefact is not merely
un-installed, it is **mis-scoped**. It is parameterised by path and globbed over `docs/*.md`,
and 12 of the 24 unbounded sites — including all 4 in the parent's own hand — live outside
that glob. The instance is not fully addressed either, because the instance's population was
drawn at the wrong boundary.

**This is the third population defect of the arc** (a term denoting 39 vs a table classifying
17; a hand-list of 5 where the gate prints 6; a figure at 8 sites bounded at 4, then 9, then
10). It is now the fourth, and the fourth is of a new sub-kind: not *a count taken at the
wrong grain* but **a boundary drawn so that the counter is outside it**.

---

## 6. DO NOT DISTURB — and the one thing that moved

**mg-d075's suite re-runs green from this branch: 7 of 7 scripts on their committed
predictions, `run_all.sh` exit 0.**

**But one committed transcript does not regenerate.** `out_s6_class.txt` moves, on the line
that counts commits naming mg-19ec — it was **11** when mg-d075 shipped it.

`s6_class.py` counts with `git log --oneline --all` filtered on a ticket id — a population
spanning **every ref in the repository**, so it counts pre-rebase twins and unmerged branches
alongside what landed, and `--all` runs several times the count on `main`. **The commits that
moved it include this audit's own**, which moved it by naming mg-19ec in a commit subject.

**The current value is printed by `a5` rather than quoted here, and the reason is the finding
itself: any number I write in this sentence is stale by the commit that ships it.** `a5`'s D2
prints the diff, the three populations (`main`, `HEAD`, `--all`) side by side, and the list of
this audit's own commits inside the population.

That is the refutation of P14, and it is the finding `a5`'s D2 exists to catch: **a suite can
re-run green while its published transcript moves, and neither `run_all.sh` nor `git status`
says so.** The parent's directory is restored by `a5` afterwards; this branch carries none of
the regenerated output.

**The upstream do-not-disturb.** mg-19ec's `rerun_upstream.sh` — six suites, all predicted 0 —
re-run from this branch: see `out_upstream_rerun_aaf4.txt`. Those directories are restored by
that script and this branch carries none of their regenerated output either.

**PROVENANCE, by patch-id and not by ancestry.** Every commit-shaped token in mg-d075's prose:

| token | resolves | ancestor of `main` | patch-id |
|---|---|---|---|
| `ec98300` | yes | **no** | matches `424f606` on main — **REBASED, CONTENT INTACT** |
| `645b5a4` | yes | yes | on main directly |

**A recorded SHA that is not an ancestor of `main` is the EXPECTED state, not a discrepancy.**
The refinery rebases before merging; ancestry is a false negative by construction. **0 tokens
unaccounted for by both tests.**

---

## 7. THE FLOOR — one thing no brief in this lineage names

**THE LIVENESS RULE CANNOT TELL USE FROM MENTION, AND WHAT IT REMOVES IS NEVER PRINTED.**

The rule every ticket of this arc inherits is a text match for `**STRUCK` / `**CORRECTED` /
`**RE-SCOPED` and three phrases. A unit that *quotes* those markers in order to define them is
scored dead by them. **Population: units of tracked `*.md` that state the figure and are
removed by the liveness rule. Grain: one unit.** There are **9**, and **1 of them is killed by
a marker it only quotes** — `code/branching_bound_d075/PREDICTIONS.md` line 44, the paragraph
in which mg-d075 *defines the liveness rule*, carrying four quoted markers and one statement of
the figure.

I do **not** re-score anybody's numbers on this basis. The parent's counts are correct for the
rule as written, and mg-19ec's, mg-d075's and my own all use it. What is wrong is that the
exclusion is **silent**: no transcript in this arc prints it. `a1`'s U6 prints it.

**A consequence worth stating.** The site I named in advance in `PREDICTIONS.md` P1a —
`code/branching_bound_d075/PREDICTIONS.md` line 49 — is inside that very unit. **P1a is
refuted**: the sentence I named is not in the population, because the paragraph containing it
is scored dead by the rule it is quoting.

---

## 8. PREDICTIONS SCORED

`PREDICTIONS.md` was committed at `f714b4c` before any script here existed. **Nothing below was
revised after a run.**

| # | prediction | outcome |
|---|---|---|
| P-0 | *not a prediction* — `ec98300` non-ancestor, content intact by patch-id | disclosed in advance as already measured; re-taken by `a5` and confirmed |
| P1 | ≥ 1 unbounded site in the parent's own deliverable, ≥ 1 in its `PREDICTIONS.md` | **HELD** — 4, all of them there |
| P1a | the site is `PREDICTIONS.md` line 49 | **REFUTED.** That sentence is not in the population: its paragraph is scored dead by the liveness rule it quotes (§7). The four sites found are at lines 15, 15, 15 and 55 |
| P1b | the parent's gate cannot see it | **HELD** — 4 of 4 outside the gate |
| P2 | the parent's figure-stating deliverable is 4 files, gate covers 2 | **HELD**, exactly |
| P3 | 8/4/4, 9/4/5 and 10/10/0 all reproduce | **HELD** — 27 rows, 0 failures |
| P4 | grain O gives more than 10 | **HELD** — 11 |
| P5 | `thirty-three` occurs 0 times | **REFUTED** — 3 occurrences in tracked markdown, and **two of them are in my own sentence predicting there are none.** The third is mg-d075's README proposing that relaxation. The prediction manufactured its own counterexamples |
| P6 | ≥ 3 of the parent's 10 criticism sentences pass on a non-numeric token alone | **HELD** — 3 by machine; **1 survives hand adjudication**, and both numbers are published |
| P6a | the two named in advance are among them | **HELD** — both are; one of the two is the one that survives adjudication |
| P7 | 3 authored prose files, 2 scanned, 1 omitted, ≥ 1 criticism sentence in the omitted file | **HELD** — 8 criticism sentences in it |
| P8 | ≥ 2 prose/instrument figure pairs disagree | **HELD** — F1 (253 vs 254) and F3 (9 vs 10) |
| P9 | `s4`'s H3 banner is a hardcoded literal disagreeing with what it prints | **HELD** |
| P10 | my own criticism check fires on me | **HELD** — a majority of my criticism sentences carry no numeric scope; the count is printed by `a3` C4 rather than asserted here, because this README is in the population it counts |
| P11 | 10 of 10 site bounds are numeric scopes | **HELD** — 0 softening words, independently re-derived |
| P12 | applying H3's classifier to `s5`'s accepted scopes returns < 10 | **HELD** — 7 of 10 |
| P13 | instance not class, and the artefact mis-scoped | **HELD** — `a4` F4 measures the mis-scoping at 12 sites |
| P14 | the parent's suite re-runs green **and** its transcripts are byte-identical | **SPLIT — the second clause is REFUTED.** Green, 7 of 7 on prediction. `out_s6_class.txt` moves, and this audit's own commit is one of the things that moved it (§6) |
| P15 | 4 of 4 commits patch-id-matched, 0 of 4 ancestors | **REFUTED IN ITS POPULATION.** mg-d075 has **3** commits on main, not 4, and its prose records **2** commit tokens, of which 1 is an ancestor and 1 is rebased with the patch-id intact. **0 unaccounted.** The verdict I predicted is right and the population I predicted it over was wrong |
| P16 | ≥ 2 referents of the numeral `33` in the parent's deliverable, the family name saving the hedge-token site | **HELD** — 6 occurrences in the README's live sentences, 4 denoting the interval figure, 2 denoting something else, and the name is the whole of what separates them |

**16 predictions and 8 exit values: 12 held, 3 refuted, 1 split. 7 of 8 exit values landed;
`a5` was predicted 0 and returned 1, and that miss is §6.**

The three refutations have one thing in common and it is worth naming: **all three are
predictions about a POPULATION, made by an audit whose subject is populations.** P1a named a
site inside a unit I had not checked was live. P5 forecast an emptiness my own prose then
filled. P15 counted the parent's commits before counting them. mg-d075's two refutations were
of exactly this shape as well — *I predicted a count without allowing for the population
changing under my own hand.* **Three tickets in a row have now done it.**

---

## 9. WHAT THIS AUDIT DID NOT DO

- **It repaired nothing.** mg-d075's deliverable is merged and dated; editing it would destroy
  the evidence trail, and editing its `PREDICTIONS.md` would violate the pre-registration
  invariant. Every finding here is a report.
- **It did not repair its own four unbounded sites** either, for the second of those reasons,
  and the count is printed rather than omitted (`a1` U5).
- **It did not install a repo-wide check**, and `a1`'s U4 now says why one on its own would
  not help. **Population: the 24 unbounded sites of the tracked-markdown universe. Grain: one
  site.**

  | | sites | why |
  |---|---|---|
  | in `docs/` | **12** | dated audit records; editing destroys the evidence trail |
  | outside `docs/`, in a `PREDICTIONS.md` | **10** | pre-registration; never reworded |
  | outside `docs/`, in an ordinary instrument README | **2** | **genuinely repairable** — `code/branching_audit_5800/README.md`, `code/branching_repair_41aa/README.md` |

  A repo-wide gate over this figure would be permanently red on **22 of 24** sites for reasons
  that are correct, and would close **2**. **What is missing is not a gate; it is a declared
  exemption** — and until there is one, every ticket that widens the population inherits a
  number it cannot act on. Those 2 are noted and **not** repaired here: they belong to other
  tickets' instruments and this audit repairs nothing.

## 10. FOR WHOEVER AUDITS ME

- **`lib_aaf4.NUMERIC_SCOPE` is mine and it is a choice**, and it was respecified twice — once
  in the direction of my own finding (`row-10 sentence` is a label, not a count) and once
  against it (markdown bold must not hide a count). Both transcripts are committed and the
  reasoning is at the point of the check, not only here. **If either respecification looks
  like a classifier tuned to a result, say so.**
- **`a3`'s hand adjudication turned 3 into 1.** I could have published the 3. The reasons are
  written out per row in `out_a3_criticism.txt`; **argue with them there.**
- **My criticism predicate is wider than the parent's on purpose**, which makes C4's 15 not
  comparable to the parent's 0. Pick a third predicate.
- **`a4`'s 9 charges are a selection.** I chose them by reading the parent's prose. A charge I
  did not notice is invisible to the ledger, and the ledger says nothing about how many I
  missed.
