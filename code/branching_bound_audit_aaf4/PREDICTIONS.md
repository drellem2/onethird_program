# mg-aaf4 — PREDICTIONS, committed BEFORE any script of this audit exists

**This audit was PRE-FILED IN THE SAME ACTION AS ITS PARENT.** `mg-aaf4` was created by
pm-onethird at 2026-07-31 07:12:16Z in the same action that filed `mg-d075`, before mg-d075
had written a line — which is the standard for this lineage and the reason its brief could
tell mg-d075 in advance *"mg-aaf4 is told not to inherit 9"*. I did not choose my own scope
and mg-d075 could not choose it for me.

**Written and committed before a single line of `code/branching_bound_audit_aaf4/*.py`
exists.** Nothing below is revised after a run. A refuted prediction stays as written and is
reported as refuted. A refuted prediction is a RESULT.

---

## 0. FULL DISCLOSURE — every command I ran before writing this file

I did not come to these predictions cold. I read the parent's committed deliverable and ran
hand greps. All of them, in order:

1. `mg show mg-aaf4` — my brief.
2. `ls code/`, `ls code/branching_bound_d075/`, `ls docs/`, `wc -l` on the living document
   and on `docs/repair-mg-d075-the-figure-and-its-scope.md`.
3. `cat code/branching_bound_d075/README.md` — the parent's account of its own instrument.
4. `cat code/branching_bound_d075/PREDICTIONS.md` — the parent's 12 predictions.
5. `cat docs/repair-mg-d075-the-figure-and-its-scope.md` — the parent's prose repair.
6. `grep -n "33" docs/OneThird-Branching-Graphs-Where-This-Lives.md` — **10 hit lines** post
   repair: 33, 184, 195, 207, 230, 241, 246, 328, 434, 435.
7. `for f in docs/*.md; do grep -c '\b33\b' …` — 24 files of `docs/` carry a `33` line.
8. `cat code/branching_bound_d075/out_s4_hedge.txt`, `out_s1_census.txt`,
   `out_s5_own_criticism.txt` — three of the parent's six transcripts.
9. `sed -n '1,130p' code/branching_bound_d075/s5_own_criticism.py` — **the parent's
   self-criticism detector, including its `FAULT` / `TARGET` / `OWNSCOPE` regexes.**
10. `cat code/branching_bound_d075/run_all.sh`.
11. `grep -n '\b33\b'` over `code/branching_bound_d075/README.md` and `PREDICTIONS.md`.
12. `grep -n "253\|254"` over the parent's README, account and s5 transcript.
13. `grep -n "the 9 sites\|33 hedge tokens" code/branching_bound_d075/s4_hedge.py`.
14. `grep -n "thirty-three" docs/*.md`; `grep -no "30 [A-Za-z]*"` on the living document.
15. `git rev-parse` on `ec98300`, `645b5a4`, `3942319`, `4203bc8`;
    `git merge-base --is-ancestor` and `git show … | git patch-id --stable` on `ec98300`
    and `424f606`.

**So P-0 below is not a prediction at all.** It is a measurement I have already taken by
hand, and I am recording it here rather than letting it look like a forecast that landed.
Everything numbered P1 onward is a forecast whose value I have not seen a machine produce.

### P-0 — NOT A PREDICTION. Already measured, by hand, before this file.

The parent records `ec98300` as the commit of its `PREDICTIONS.md`. **`ec98300` resolves and
is NOT an ancestor of `main`** — the refinery rebased it. Its content survives at `424f606`:
both have patch-id `9f8adc69e222366cdec7b57a28f6b69fd263a1ab`. **This is the expected
false-negative of ancestry after a rebase and it is not evidence of tampering.** I will
re-take it in the instrument over all four of the parent's commits; the value above is
already known for one of them and is disclosed rather than scored.

---

## 1. THE COUNT — I do not take 8, and I do not take 9 or 10 either

The brief tells me to count the sites myself and to **say what instrument I used, because the
instrument is what decides whether I could have found a different answer.**

**My instrument is not the parent's.** The parent measures at **sentence grain** with a
liveness rule inherited from mg-19ec and a predicate keyed on the literal `33`. I measure at
**two grains, and over a wider universe**:

- **Grain O — one OCCURRENCE of the figure.** The unit is a single occurrence of the numeral
  denoting the Young–Fibonacci interval count, not the sentence containing it. Two
  occurrences in one sentence are two units. The parent's own §1 insists a number be stated
  with its grain; a count of sentences and a count of occurrences are different numbers about
  the same text, and the parent publishes only the first.
- **Grain S — one sentence**, split by **my own splitter**, not the parent's, and with my own
  liveness rule.
- **Universe U — every file this repair AUTHORS that states the figure**, not `docs/*.md`.
  The parent's corpus population D is *"`docs/*.md`"*. Its own `README.md` and its own
  `PREDICTIONS.md` state the figure and are not in `docs/`.

**P1 — THE PARENT'S OWN DELIVERABLE CONTAINS AT LEAST ONE UNBOUNDED SITE OF THE FIGURE, AND
IT IS OUTSIDE EVERY POPULATION THE PARENT MEASURES.** Population: live sentences of the four
files mg-d075 authors or edits that state the 33-interval figure — the living document,
`docs/repair-mg-d075-the-figure-and-its-scope.md`, `code/branching_bound_d075/README.md`,
`code/branching_bound_d075/PREDICTIONS.md`. Grain: one sentence. Predicate: the parent's own
STRICT one (figure and the name `Young–Fibonacci` in the sentence; bounded iff a rank scope
is in the same sentence).

- **Predicted: ≥ 1 unbounded, and ≥ 1 of them in `code/branching_bound_d075/PREDICTIONS.md`.**
- **P1a — I name a site in advance.** `PREDICTIONS.md` line 49: *"**Predicate:** the sentence
  states the 33-interval figure **about Young–Fibonacci intervals**, where the attribution may
  come from the sentence *or from the table cell / paragraph the sentence sits in*."* It
  states the figure, it names Young–Fibonacci, and it carries no rank bound.
- **P1b — the parent's gate cannot see it**, because `s1`'s population D globs `docs/*.md`
  and `s5`'s `MINE` lists two files, neither of them `PREDICTIONS.md`.

**P2 — the figure-stating file count of the parent's own deliverable is 4, not 2.** The
parent's §5 says *"the corpus of this figure is now 7 files of `docs/`, 36 sites … my gate
covers 2 of the 7"*. Population: files authored or edited by mg-d075 that state the figure.
**Predicted 4** (living doc, account doc, README, PREDICTIONS), of which the gate covers 2.

**P3 — the parent's pre-repair 9 / 4 / 5 and post-repair 10 / 10 / 0 REPRODUCE at sentence
grain.** Re-implemented independently against the same file, my STRICT and RELAXED counts
return the parent's published values row-for-row. *If this fails the disagreement is mine to
explain, not the parent's — a disagreement with a published figure is worth nothing until the
published figure has been reproduced.* This is the parent's own standard and I adopt it.

**P4 — AT OCCURRENCE GRAIN THE LIVING DOCUMENT'S NUMBER IS NOT 10.** Predicted: **greater
than 10** post-repair, because at least one sentence states the figure twice. I have not
counted this. If it comes back exactly 10 the prediction is refuted and grain made no
difference here.

**P5 — the figure is never written in words.** `thirty-three` does not occur anywhere in
`docs/`. Predicted **0 occurrences**, corpus-wide. (Measured at step 14 above as a `grep`
returning nothing; I record it as a prediction anyway because my instrument will re-take it
over a wider universe than `docs/*.md`.)

---

## 2. THE HARDER HALF — the repair read as a claimant

The brief: *"read every sentence in which the repair faults someone else's scope, and check
whether the repair does elsewhere what it criticises."*

**P6 — THE PARENT APPLIES A WEAKER STANDARD TO ITSELF THAN TO THE DOCUMENT, AND SAYS IN THE
SAME BREATH THAT IT DOES NOT.** `s5_own_criticism.py`'s docstring states: *"A neighbouring
sentence does not rescue it — that is precisely the standard this repair applied to the
document, and applying a weaker one to myself would be the defect a second time."* Its
`OWNSCOPE` regex accepts the bare words `population`, `grain`, `live sentences`, the tokens
`STRICT`, `RELAXED`, `POP-\d`, and a bare path `code/…`. **None of those is a numeric scope**,
and `s4_hedge.py`'s H3 exists precisely to separate a NUMERIC SCOPE from a SOFTENING WORD at
every one of the document's sites.

- **Predicted: ≥ 3 of the parent's 10 criticism sentences pass `OWNSCOPE` on a non-numeric
  token alone** and would fail the standard H3 imposes on the document.
- **P6a — I name two in advance.** `s5`'s `[07]` (*"FOUR was not the population, and EIGHT is
  not either…"*, scope printed as `population`) and `[10]` (scope printed as `population`).

**P7 — THE PARENT'S SELF-CRITICISM POPULATION OMITS ONE OF ITS OWN THREE PROSE DOCUMENTS.**
`MINE` is README + account doc; `PREDICTIONS.md` is not in it. Population: prose files
authored by mg-d075. Predicted: **3 authored prose files, 2 scanned, 1 omitted**, and
**≥ 1 criticism sentence in the omitted file** under the parent's own `FAULT ∧ TARGET`
predicate. Whether any of them is unbounded I do not predict — I predict only that the
population is short by a file and that the file is not empty of the thing being counted.

**P8 — A PROSE FIGURE OF THE PARENT'S DISAGREES WITH THE PARENT'S OWN TRANSCRIPT, IN THE SAME
COMMIT, AND IT IS THE FIGURE OF THE VERY CHECK THAT FAULTS A PREDECESSOR FOR EXACTLY THAT.**
The parent's §6 and `s4`'s H4 fault
`docs/OneThird-Warrant-Repair-mg-dffa-IndependentAudit.md` because it *"says twice"* it
scanned against **26** hedge tokens while the code carries **25** — *"a hand-written literal
no instrument computes."* Predicted: the parent's `README.md` says **253** live sentences of
its own prose **twice**, and its own committed `out_s5_own_criticism.txt` says **254**.
**Same shape, same arc, same commit, and said twice in both cases.** Predicted count of
disagreeing prose/instrument figure pairs found in the parent's deliverable: **≥ 2**.

**P9 — AN INSTRUMENT-SIDE POPULATION LITERAL OF THE PARENT'S DISAGREES WITH WHAT THE SAME
BLOCK PRINTS.** `s4_hedge.py`'s H3 banner is the literal string *"Population: the 9 sites"*;
the block prints **10** rows and its own SUMMARY says **10 of 10**. Predicted: the banner is a
hardcoded literal, changing the site count does not change it, and **the parent's population
defect survives inside the parent's own repair of population defects.**

**P10 — I WILL DO IT TOO.** The brief that commissioned the parent said whoever repairs this
should expect to commit the same defect in the repair; the parent predicted that of itself
and was right. **I predict my own criticism check (`a3`) exits 1 on its first run over my own
prose**, finding at least one sentence in which I fault mg-d075's scope while stating no
numeric scope of my own. I will commit that first transcript rather than only the fixed one.
If it exits 0 first time, P10 is refuted and I will say so.

---

## 3. BOUNDED, NOT MERELY HEDGED

**P11 — every bound the parent added to the living document is a numeric scope, and this
reproduces.** Population: the 10 post-repair sites of the living document. Grain: the exact
substring carrying the bound. Predicted **10 of 10 NUMERIC SCOPE, 0 SOFTENING**, independently
re-derived. I expect to confirm the parent here.

**P12 — but the standard is not applied uniformly across the parent's own deliverable.**
Predicted: applying H3's own NUMERIC-SCOPE-or-SOFTENING classifier to the scopes `s5` accepted
for the parent's 10 criticism sentences returns **< 10 numeric**. This is P6 measured with the
parent's own classifier rather than with mine.

---

## 4. INSTANCE OR CLASS

**P13 — the parent addressed the instance, and I will confirm its own verdict rather than
overturn it.** The parent computes `INSTANCE + REUSABLE ARTEFACT` and states plainly that it
does not install a repo-wide check. Predicted: **I agree**, and I predict the sharper version
— that the artefact is not merely un-installed but **mis-scoped**: it globs `docs/*.md`, and
the parent's own defects (P1, P7) live outside that glob. Predicted: **the class is not
addressed and the instance is not fully addressed either**, because the instance's population
was drawn at the wrong boundary.

---

## 5. DO NOT DISTURB

**P14 — the parent's suite re-runs green and its committed transcripts regenerate byte-identical.**
`sh code/branching_bound_d075/run_all.sh` exits **0**, all 7 scripts on prediction, and
`git diff --stat` over `code/branching_bound_d075/out_*.txt` after the run is **empty**.
I predict the byte-identity because the parent derives its anchor from the log rather than
pinning a SHA. **If any transcript moves, that is a finding and I will name which.**

**P15 — all four of mg-d075's commits survive the rebase with content intact.** Predicted:
**4 of 4** recorded-or-rebased pairs match by `git patch-id --stable`, **0 of 4** of the SHAs
the parent's own prose records are ancestors of `main`. Population: the four commits of
mg-d075. Grain: one commit. (One of the four is already measured — see P-0.)

---

## 6. THE FLOOR — one thing no brief in this lineage names

The standing asks for at least one thing no list names. Mine:

**P16 — THE NUMERAL `33` DENOTES TWO DIFFERENT POPULATIONS INSIDE THE PARENT'S OWN
DELIVERABLE, AND ITS DETECTOR CANNOT TELL THEM APART.** `code/branching_bound_d075/README.md`
line 33 says *"33 hedge tokens"*; the same file's line 50 says *"the figure `33`, the interval
count"*. A `\b33\b` predicate reads both. Predicted: **≥ 2 distinct referents of the numeral
`33`** in the parent's deliverable, and predicted that a naive re-use of the parent's own
STRICT predicate on the parent's own README **would score a hedge-token count as an interval
figure** unless the name `Young–Fibonacci` happens to save it. I predict the name **does**
save it at that site — i.e. the parent is lucky rather than careful here — and I will say
which it is.

---

## 7. EXIT CODES — every script, predicted before it exists

| script | what it exits on | predicted |
|---|---|---|
| `a1_population.py` | 1 if the parent's own deliverable holds an unbounded site of the figure | **1** |
| `a2_reproduce.py` | 0 if the parent's 9/4/5 and 10/10/0 both reproduce exactly | **0** |
| `a3_criticism.py` | 1 if any criticism sentence — the parent's or MINE — carries no numeric scope | **1 first run, 1 final** |
| `a4_selfapply.py` | 1 if any prose figure of the parent disagrees with its own instrument | **1** |
| `a5_donotdisturb.py` | 0 if the parent's suite re-runs green with transcripts unmoved | **0** |
| `selftest_aaf4.py` | 0 if every mutation of the corpus is caught by my detector | **0** |
| `run_all.sh` | 0 iff every script matches the row above | **0** |

**Note on `a3`'s final value: I predict it stays 1.** The parent's `s5` was predicted 1-then-0
because the parent could edit its own prose until the check passed. **I cannot edit
mg-d075's prose — it is merged and it is a dated record — so a check that gates on the
parent's sentences must stay red.** A check I could turn green by editing the thing under
audit would not be an audit. If `a3` ends at 0 this prediction is refuted.

**Eight predicted exit values across 6 scripts + the runner** (`a3` contributes two).

---

*Committed before `a1`…`a5`, `selftest_aaf4.py`, `lib_aaf4.py` and `run_all.sh` existed.
Sixteen predictions and eight exit values. Whatever these turn out to be, they stay as
written.*
