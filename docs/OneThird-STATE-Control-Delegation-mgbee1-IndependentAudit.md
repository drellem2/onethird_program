# Independent audit of mg-bee1 / `a2d5a81` + `2a29f30` — the statement repair and the delegation

**mg-5644**, 2026-07-30. Pre-filed at DISPATCH, per mg-0e24, because the rule living in the
filer's path was bypassed three times on 2026-07-30. **Sixth control in this lineage.**

The first (`b68db5d`'s headline re-run) was blind at the **INPUT** — it pinned fixed
revisions. The second (`bf17716`) at the **MUTATION SET** — it tested substrings its own
author chose. The third (`e924590`) closed both with a content digest and was blind at the
**LOCATOR**. The fourth (`e4426c9`) closed the locator with a presentation record and was
blind at the **PROPOSITION** — it published a universally quantified sentence over a
section-local mechanism. The fifth was mg-218d's audit, which found that. **Five for five,
the blind spot MOVED rather than closed**, so the primary question here is not whether
mg-bee1's fix is correct. It is *which layer is uncontrolled now*, answered per layer and
**verified rather than inherited** — an inherited layer verdict is exactly the pinned-input
defect this lineage already suffered once.

Reproduce: `sh code/state_delegation_audit_5644/run_all.sh` (~6 min). Five outputs committed
beside it. Sections 1, 2 and 5 mutate `docs/state-history/attempt-mg-276d.md` and
`delta_control.py` **in the working tree** and restore them under a `finally` plus a sha256
check; each refuses to run on a dirty tree. Section 3 needs two markdown renderers installed
**outside** the repo and exits 3 with the install command if they are absent.

---

**THE STATEMENT REPAIR IS REAL AND THE DELEGATION CLOSES B2 ON ITS OWN TERMS. NOTHING THAT
SURVIVED WAS WEAKENED — the two-renderer agreement is 141 of 141 in this worktree, one MORE
than mg-218d measured, because mg-bee1's own new block joined the population. AND THE BLIND
SPOT MOVED AGAIN, TWICE. The repair created a NEW REGION SET — five delegated sections of a
file outside the two the instrument reads — gave it a content digest and NO presentation
record, and published it as "closed for cited sections". mg-babf's B05/B06 work verbatim on
it: one `<!--` line at the top of the target and a reader who follows the certified cell's
six links is shown a BLANK PAGE by both `marked` and `markdown-it`, every delegated digest
matches, and the control exits 0.**

**And in beyond-brief material: the new L0 probes are four fixtures somebody chose,
published as a rule. `str.strip()` removes 29 characters, the published rule admits four,
the probes name two of the 25 that matter, and 23 of 25 single-character widenings of `EDGE`
exit 0 — one edit each, probes left in place and passing. mg-bee1's own battery row `I3`
widens `EDGE` with `U+00A0`, which is the character probe 2 is built around.**

| | |
|---|---|
| audited | `a2d5a81` + `2a29f30` (mg-bee1), the sixth control in this lineage |
| verdict | **HOLDS where it claims; 2 BROKEN and 1 MINOR at the layers it created** |
| instrument | `code/state_delegation_audit_5644/` — own harness, own predictions, written before the runs |
| evidence | `out_delegated.txt`, `out_norm.txt`, `out_render.txt`, `out_l2pop.txt`, `out_layers_5644.txt` |

---

## What is NOT undone — re-measured, not read off the committed outputs

Every figure in this table was produced by an independent run in this worktree.

| claim | mg-bee1 reports | this audit measured |
|---|---|---|
| mg-218d's 16-mutation battery re-run **UNMODIFIED** | 10 silent → 6 | `git diff a4aeeb9..HEAD -- code/state_layer_audit_218d/` is **empty**. An independent re-run is **byte-identical** to `out_layers_bee1.txt`. 10 → 6 confirmed; `T1` `T2` `T3` `I2` now fire; still silent: `I1` `S1` `P2` `P3` `P4` `P6` |
| the presentation model against two real GFM renderers | "140 of 140 stands" | **141 of 141**, both renderers agreeing on every comparison. The population grew by mg-bee1's own new certified block. **Nothing retreated** |
| mg-babf's 15, re-run unmodified | 11 of 11 caught, 0 silent misses | identical |
| mg-2216's 14, re-run unmodified | 10 caught, 0 missed, 2 tolerated, 2 noisy | identical |
| `coverage218d.py`, re-run unmodified | 40 of 40 claims hold; **3 of 3** uncontrolled layers NAMED | identical — but there is now a **fourth**, and it is named nowhere |
| B2: a cited section deleted / the F1 repair inverted there / the file emptied | `T1` `T2` `T3` all fire (1 / 2 / 1) | confirmed, and independently reproduced on this audit's own harness as `Q5` `Q6` |
| `battery_bee1.py` 7 of 7 predicted; `globalpos_bee1.py` | as committed | both reproduce **byte-identically** |

**The statement repair.** *"A MUTATION THAT CHANGES WHAT A READER SEES MUST CHANGE A
DIGEST"* is gone from all three editable locations and replaced by the bounded form, with
cross-section context named as uncovered in each. The correction of record for `e4426c9`'s
uneditable commit message is a new **certified** block in `docs/state-history/README.md`. A
repo-wide grep finds a fourth occurrence of the unqualified sentence, in mg-218d's own audit
document, where it is the thing being criticised — which is correct. **This is the acceptance
item the ticket put first, and it was done first and done fully.**

**The re-baselining cost was stated, and the trade was not taken.** mg-bee1 did not make
`position` document-global. It implemented that alternative, measured what it would close (4
of 5 silent rows), measured what it would cost over the **complete** git history of both
certified files (36 commits of `STATE.md`, 35 transitions, 29 re-baselines, 83%), and found
that `P7` — a retraction that *replaces* a paragraph elsewhere — is silent under it too, so
the unqualified sentence stays false. **That is the right call and the negative survives:
nothing was built here that refutes it.** `P7` moves no ordinal and no block count under any
scoping, so no re-scoping of `position` reaches it.

**No over-correction.** L3, L5, L6 and the renderer agreement stand and are stronger, not
weaker. Not one line of `presentation.py`'s model changed and not one line of
`code/state_layer_audit_218d/` did.

---

## BROKEN

### B1 — the delegated surface has a content digest and no presentation record

mg-4acd exists because mg-babf established that *"are these the certified bytes?"* and *"is
anybody shown them?"* are different questions, and that a control answering only the first
passes while a certified block sits inside an HTML comment. mg-218d verified the answer
against two renderers.

mg-bee1 then created a **new region set** — the five sections of
`docs/state-history/attempt-mg-276d.md` that the certified ledger cell cites by name — and
gave it a content digest under the same `N` as every other region and **no presentation
record**. Its own docstring records that, as a fact, in a coverage list:

> DELEGATED (mg-bee1), digested under the same N but **NOT carrying a presentation record**

and nowhere says what it costs. What is published instead, in `COVERAGE.md`'s layer table
and again in `code/state_delegation_repair_bee1/README.md`, is:

> | **L1 what a region points at** | … | **closed for cited sections** (`T1` `T2` `T3`) |

**The bound is stated in terms of WHICH SECTIONS are followed — cited versus uncited. It is
stated nowhere in terms of whether a reader is shown them.** So mg-babf's mutations were put
to the new surface:

| | mutation | exit | what a reader is shown |
|---|---|---|---|
| **Q1** | one `<!--` line at the top of the target, never closed | **0** | **nothing — a blank page** |
| **Q2** | one ``` line at the top of the target, never closed | **0** | every cited section as unrendered source inside a code sample |
| **Q3** | a retraction paragraph at the top of the target | **0** | mg-bee1's stated bound, confirmed |
| **Q4** | a new uncited section appended | **0** | mg-bee1's stated bound, confirmed |
| **Q5** | a cited section's heading retitled | **1 (FAIL)** | positive control — the mechanism is not inert |
| **Q6** | a contradiction inserted inside cited `H3` | **2 (MOVED)** | positive control |

Six of six carried the exit code predicted before the run.

**Q1 is measured, not argued.** `render5644.py` hands the mutated file to `marked` and to
`markdown-it` and asserts absence: **60 comparisons, both renderers agreeing on every one.**
Unmutated, all five cited sections render as headings on both. Under Q1, **zero of five are
visible at all on either.** Under Q2, zero of five render as headings and all five survive as
literal source — which is precisely the state mg-babf's B05 put the F1 block into and which
mg-4acd's `state` field classifies as a miss.

In every one of Q1 and Q2, **no byte of any cited section changes**: each section begins at
its own `###` heading and the mutation is one line above the first of them. Every delegated
digest matches. The control prints `PASS`.

**Why this is the lineage's pattern and not a nitpick.** `delta_control.py` section 8 already
carries two default-deny presentation guards — *"0 block constructs outside the modelled
subset"* and *"0 raw-HTML tokens in text presented as prose"* — run over the whole of both
certified files. Neither Q1 nor Q2 has an analogue there, because those guards exist. **The
guards are not applied to a delegated target, and the repair that created delegated targets
did not extend them.** The hole did not exist before `a2d5a81`; the repair created the
surface it is on.

**Severity.** A reader following the certified cell is the entire reason B2 was a finding —
mg-218d's own words were *"a certified region pointing at something a reader cannot read is
damage"*, and mg-bee1 adopted them, classifying a missing cited section as **FAIL** rather
than MOVED for exactly that reason. Q1 produces the same experience for that reader and exits
0.

### B2 — the L0 probes are four fixtures somebody chose, published as a rule (BEYOND BRIEF)

mg-bee1's ticket has five acceptance items. Section 0 of `delta_control.py` — `NORM_RULE`
and `norm_rule_probes()` — is none of them. It is mg-bee1's own addition, closing mg-218d's
`I2`. **Roughly seven consecutive generations of this arc have put their worst finding in
beyond-brief work**, because unbriefed work has no acceptance criteria and so nothing tests
it, and this generation continues the record.

The published rule is the standard:

> `N(region)` = the region's characters with ASCII SPACE, TAB, CR and LF removed from the
> TWO ENDS of the whole region — **nothing else** — encoded UTF-8.

The claims made for the probes are:

> These probes are the rule as an assertion: each one is a sentence of the docstring above,
> and **each fails if the code stops meaning it**. They are BEHAVIOURAL, not textual, so
> **they fire on a widened EDGE constant** exactly as on a widened `strip()` call.
> … It raises one specific silent divergence … **from free to two edits**, and that is the
> whole claim.
> — and in `COVERAGE.md`: "a widened `strip()` call *or* a widened `EDGE` constant **is a
> non-zero exit**."

**The arithmetic.** `str.strip()` removes the 29 characters for which `str.isspace()` is
true. The published rule admits 4. So **25 characters**, placed in `EDGE`, make the code stop
meaning its own published rule. The four probes name **two** of them — `U+00A0` and `U+2028`.

**The sweep — the population, not a sample.** Each of the 25 added to `EDGE` on its own, one
full run of the control each:

```
population 25; 2 fire; 23 exit 0
FIRE   (2): U+00A0 U+2028
SILENT (23): U+000B U+000C U+001C U+001D U+001E U+001F U+0085 U+1680 U+2000 U+2001 U+2002
             U+2003 U+2004 U+2005 U+2006 U+2007 U+2008 U+2009 U+200A U+2029 U+202F U+205F
             U+3000
```

**The two that fire are the two the probe list was built around.** And the probe labelled
*"nothing INTERIOR is touched"* has a single fixture, `"a \t  \n b"`, so any interior rewrite
of a character absent from it passes: `norm()` gaining `.replace("​", "")` is one edit
and exits 0.

| | mutation | predicted | observed |
|---|---|---|---|
| **E1** | `EDGE` widened by the 23 characters no probe names | 0 | **0** |
| **E2** | `EDGE` widened by `U+00A0` — **mg-bee1's own `I3`** | 1 | 1 (FAIL) |
| **E3** | `EDGE` widened by `U+2028` — probe 3's own character | 1 | 1 (FAIL) |
| **E4** | `EDGE` widened by `U+000C` alone | 0 | **0** |
| **E5** | `EDGE` widened by `U+2003` alone | 0 | **0** |
| **E6** | `norm()` gains an interior `.replace(U+200B, "")` | 0 | **0** |
| **E7** | `norm()` gains an interior `.replace(U+00A0, " ")` | 1 | 1 (FAIL) |
| **E8** | `norm()` widened to a bare `.strip()` — mg-218d's `I2` | 1 | 1 (FAIL) |

Eight of eight as predicted.

**mg-bee1's own row `I3` is "the EDGE constant widened, norm() untouched", and the character
it widens `EDGE` with is `U+00A0`** — the character probe 2 is built around. It is a positive
control presented as the general claim, and it is the only widening in the battery.

**What this audit does NOT claim.** `E8` fires: the specific divergence mg-218d found *is*
closed, because a bare `strip()` eats both `U+00A0` and `U+2028` and probes 2 and 3 are built
from exactly those. That is a real gain and it is not retracted here.

**And this is not the "nothing certifies the instrument" complaint.** That caveat is correct
and is not at issue: it covers an edit that changes `norm()` **and deletes the probes**.
Every row above **leaves the probes in place and passing**, which is the case the caveat says
is covered — so *"from free to two edits"* is false: E1, E4, E5, E6 and all 23 silent
characters are **one** edit.

**Self-awareness is not a control.** mg-bee1 named its own likely failure mode (probe
deletion) and handled the case it named. The case it did not name is the one that fires.

**This is the lineage's own record repeating inside the cure.** Generation 2's defect was
*author-chosen substrings at the MUTATION SET*. Generation 5's was *a universally quantified
sentence over a mechanism quantified on a chosen subset*. Section 0 is **both, in the same
file, in the commit that repaired generation 5.**

---

## MINOR

### M1 — a precise number that its own instrument contradicts

`code/state_delegation_repair_bee1/README.md` and the message of `2a29f30` both report that
a document-global ordinal would re-baseline on

> **83%** of the commits that have touched `STATE.md` and **4 of 4** that have touched the
> state-history README

`out_globalpos.txt`, committed in the same commit, prints:

```
docs/state-history/README.md
    6 commits touched it; 5 commit-to-commit transitions
    block count changed at 5 of them  (100%)
```

**5 of 5, not 4 of 4.** The rate is the same and the conclusion does not turn on it. The 83%
figure checks out and its population is complete — 36 commits is the entire history of
`STATE.md`, not a window, so the qualifier is genuinely on the number. **The most citable
thing in a document is its most precise number, and this one disagrees with the instrument
printed beside it.**

---

## Which layer is uncontrolled after mg-bee1

mg-218d found L0, L1 and L2 firing on none of their six. **That verdict was re-measured here
rather than carried forward.**

| layer | mg-bee1 publishes | this audit |
|---|---|---|
| **L0** instrument | "partly closed — `norm()` checked behaviourally against its published rule" | **the specific divergence is closed; the RULE is not asserted.** `E8` fires. 23 of 25 widenings and any unlisted interior rewrite exit 0, one edit each. `I1` still 0 |
| **L1** what a region points at | "**closed for cited sections**" | **closed for their BYTES; OPEN for their PRESENTATION** (`Q1` `Q2`), and stated nowhere |
| **L2** region set | **OPEN**, fix declined as mutation-shaped | **OPEN**, agreed. The *reason given* is overstated — below |
| **L3** region location | closed, 4 of 4 fire | confirmed |
| **L4** presentation | section-local, and now SAID to be | confirmed and correctly stated (`P2` `P3` `P4` `P6` `P7` exit 0). **L4 on the delegated surface is new and is stated nowhere** |
| **L5** byte content | closed | confirmed |
| **L6** normalisation | closed, "now asserted by section 0" | closed by the digest; **"asserted by section 0" over-claims** — see B2 |

**The answer to the ticket's primary question: the uncontrolled layer after this fix is L4
ON THE SURFACE L1's REPAIR CREATED.** It is the same layer mg-4acd closed, one file out, on a
region set that did not exist before `a2d5a81`. The fix is available and cheap: section 8's
two default-deny guards already do this job for the two files the instrument reads.

**Sixth for sixth, the blind spot moved rather than closed** — and for the first time it
moved onto ground the repair itself laid.

---

## The negatives, tested by construction

Three negatives fell in this arc on 2026-07-30, all refuted by construction and none by
argument. mg-bee1 publishes two more, and both were built against before being assessed.

**"A document-global ordinal still leaves the sentence false" — STANDS.** `P7` replaces a
paragraph in place: no ordinal moves, no block count moves, under any scoping. Nothing was
built that refutes it, and `globalpos_bee1.py` reproduces byte-identically.

**"Closing L2 by counting blockquotes would catch mg-218d's mutation and not the layer …
and there is not one here" — OVERSTATED, not false.** `l2pop5644.py` builds a **population
rule**: every blockquote block in the README must be either certified or explicitly declared
not-certified, with the same two-way default-deny mg-bee1 itself wrote for the delegation
surface, plus a uniqueness clause. **6 of 6** L2-shaped mutations fire — mg-218d's `S1` as
built, a verbatim duplicate, a near-copy in the middle of the file, one with no new heading,
one directly above a certified block, and a deletion in the rot direction. Three of those
mg-218d never wrote. It is not shaped around `S1`, and its discipline is already in
`delta_control.py`: section 8 is default-deny over an enumerated population.

**Its bound, which is why this is an observation and not a third BROKEN:** it closes L2 for
blockquotes in one file. A contradicting near-copy written as a plain paragraph, or as a
table, or placed in `STATE.md`, is outside its population and still exits 0. **mg-bee1's
substantive point — that no rule here decides which blocks *ought* to be certified in
general — survives. The specific reason given for declining does not: the available fix is
not mutation-shaped, it is cheap, and it costs one declared entry on this tree.**

---

## This audit's own instrument, and its own two defects

`l2pop5644.py` was wrong twice before it was right, and both are recorded in its docstring
rather than quietly fixed:

1. it compared certified region spans to blockquote spans **by line number**, and reported
   five false hits the moment a mutation shifted a line;
2. once fixed to match by content marker, it was **silent on a verbatim duplicate**, because
   one marker matched two blocks.

Both are failures this cluster's own locator discipline already forbids — the second is
exactly what `_unique_marker_line` exists to prevent. Finding them in this audit's own
instrument is the reason the instrument is committed and not only its conclusion.

`harness5644.py` is this audit's own — not mg-218d's, not mg-bee1's — with its own snapshot,
restore discipline and exit-code reader. mg-218d's sixteen are **also** re-run on mg-218d's
own harness, unmodified, so the "unmodified" claim rests on `git diff` and an independent
re-run rather than on this audit's reimplementation of anything.

Reproduce everything: `sh code/state_delegation_audit_5644/run_all.sh`. For section 3:

```sh
D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
NODE_PATH="$D/node_modules" sh code/state_delegation_audit_5644/run_all.sh
```

The renderers are installed **outside** the repo and are a dependency of this audit only,
never of the control.
