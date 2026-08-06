# `mg-1d6c` — predictions, committed before any script of this instrument exists

**This file is a pre-registration.** It is committed in a `predictions:` commit that contains
**no `.py` file of this directory**, and this lineage never rewords, amends, squashes or
rebases one away. Everything below is written before the first line of `p1_glob.py` is typed.

**What this ticket is.** `mg-aaf4` reported that `mg-d075`'s published corpus figure — 12
unbounded sites — is **exactly half** of the 24 it counts over every markdown file tracked by
git, and that the glob `docs/*.md` is the whole of the reason. My brief asks three things:
enumerate what the glob **actually matches** against what it is **described as** matching;
re-derive the full population by a method that does not share the glob's blind spot; and
enumerate the **consumers** — every published figure that inherits the undercount. It also asks
for three repairs to `mg-d075`'s self-check, and for the excluded population to be **declared at
the gate with its size** instead of being made invisible by where the glob was drawn.

**The brief's own caution, restated so I am held to it:** *exactly half* is a hint and must not
become the conclusion. If the true count is not 24 I say so, and a tidy ratio does not survive
into my report because it is memorable.

---

## 0. DISCLOSURES — measurements I already took by hand, NOT predictions

Every command I ran before writing this file is listed here with what it returned. A figure
below is a **measurement**; laundering one into a prediction would make this pre-registration
worthless. Nine disclosures.

| # | what I ran | what it returned |
|---|---|---|
| **D1** | `git ls-files '*.md' \| wc -l`; `find . -name '*.md' -not -path './.git/*' \| wc -l`; `git status --porcelain -uall \| grep '\.md$'` | **292** tracked, **292** on disk, **0** untracked |
| **D2** | `ls docs/*.md \| wc -l`; `git ls-files 'docs/**' \| grep '\.md$' \| wc -l`; `find docs -mindepth 1 -maxdepth 1 -type d` | **105** at the top level of `docs/`, **117** tracked under `docs/` at any depth, exactly **one** subdirectory — `docs/state-history`, holding **12** `.md` |
| **D3** | for every tracked file, `grep -l 'Young.Fibonacci'` ∧ `grep -q '33'` | **52** files: **14** `.md`, **22** `.txt`, **16** `.py` |
| **D4** | the same list filtered to `docs/state-history/` | **0** files |
| **D5** | `grep '^SUMMARY' code/branching_bound_audit_aaf4/out_a1_population.txt` | mg-aaf4's published values, quoted and **not yet re-derived by me**: U4 **13** files, **51** sites at sentence grain, **24** unbounded, **60** occurrences; U1 pre-repair STRICT 8/4 unbounded and RELAXED 9/5 unbounded, as-it-stands 10/0 under both; U2 **11** occurrences; U3 4 files, gate covers 2, 4 unbounded and all 4 outside the gate |
| **D6** | `grep` over `code/branching_bound_d075/README.md` and `docs/repair-mg-d075-the-figure-and-its-scope.md` | mg-d075's published corpus: pre-repair **29** sites in 6 files, 17 unbounded; post-repair **36** sites in 7 files, **12** unbounded; the universe named as *"the 101 `docs/*.md` that are not this repair's own"* |
| **D7** | read `code/branching_bound_d075/s4_hedge.py` H3 | its NUMERIC-SCOPE classifier is exactly `re.search(r"\d", bound_substring)` on the substring carrying the bound |
| **D8** | read `code/branching_bound_d075/s5_own_criticism.py` | `MINE` lists **2** paths; `FAULT` contains the literal `cannot see`; `OWNSCOPE` admits bare `population`, `grain`, `live sentences`, `STRICT`, `RELAXED`, `POP-\d` and a bare `code/…` or `docs/…` path |
| **D9** | `git log --diff-filter=AM -- code/branching_bound_audit_aaf4/out_a1_population.txt` | the transcript carrying mg-aaf4's census was written at **`8132d75`** (2026-08-05) |

**D3 is a grep, not a census.** It reports which files contain both strings anywhere; a *site*
requires the parent's unit, liveness and same-sentence rules, and I have run none of those by
hand. Every count of sites below is therefore a genuine forecast.

**One thing I have deliberately NOT run:** the parent's predicate over any universe at all. No
site count, no bounded/unbounded split, no per-file row. That is the whole content of P3–P6 and
it stays unmeasured until the scripts exist.

---

## 1. THE PREDICTIONS

**Population and grain are named on every row, because a count whose population is not named is
the defect this arc is about.**

### The glob, against its description

| # | prediction | how it is falsified |
|---|---|---|
| **P1** | The universe `mg-d075` calls `docs/*.md` is implemented as `os.listdir(DOCS)` filtered on `.endswith(".md")`, which differs from its description in **two** mechanical ways: it is **not recursive**, and it reads **the working tree, not the index**. The enumeration prints both difference sets. | either property absent, or the printed sets empty where I say they are non-empty |
| **P1a** | The recursion blind spot is **non-empty as a file set**: **12** tracked `.md` under `docs/state-history/` are invisible to it. (Population: tracked `.md` under `docs/`. Grain: one file. The 12 is D2, so this row is a prediction only about *invisibility*, not about the number.) | fewer than 12 invisible, or any of them visible to the glob |
| **P1b** | The tracked-vs-worktree blind spot is **REAL BUT EMPTY at `HEAD`** — 0 untracked `.md` (D1), so it costs nothing today and would cost silently tomorrow. I predict my instrument prints it as an empty set rather than omitting it. | a non-empty set, or the check not printed at all |
| **P2** | **The recursion blind spot costs ZERO SITES.** No file under `docs/state-history/` states the figure at all, so the entire 12-of-24 gap is the `docs/` **boundary** and none of it is the missing `**`. | ≥ 1 site found under `docs/state-history/` |

### The population, re-derived

| # | prediction | how it is falsified |
|---|---|---|
| **P3** | **mg-aaf4's 24 reproduces under a different parser.** Population: live sentences of every `.md` tracked at `8132d75`. Grain: one sentence. Predicate: the parent's RELAXED. Using `lib_d075`'s reader — mg-aaf4 used its own re-implementation, so this is a like-for-like count through the *other* parser — I predict **13 files, 51 sites, 24 unbounded**, all three exact. | any of the three differing |
| **P3a** | If P3 misses, the disagreement is a **parser** disagreement and not a universe disagreement, and I will say which rows differ rather than publishing a new total. | — (a discipline, scored by whether I did it) |
| **P4** | At `HEAD` **before this ticket's own commits**, the same measurement is **unchanged: 13 / 51 / 24**. Nothing landed between `8132d75` and `20614ef` that touches this figure. | any of the three moved |
| **P5** | **The tidy half is REAL and not a classifier artefact:** at `HEAD` the split is **12 inside `docs/` and 12 outside**, re-derived through the parent's parser. I predict the exactness is a **coincidence of this corpus**, not a law, and I predict my own report will say so in those words. | a split other than 12/12 |
| **P6** | **THE POPULATION CHANGES UNDER MY OWN HAND, and I say in advance what I will do about it.** This file states the 33-interval figure for Young-Fibonacci intervals of rank 6 and below, so it enters the population it measures. I predict my own deliverable contributes **≥ 1 site** and **0 unbounded sites**, because every figure-stating sentence I write carries `rank 6` in that same sentence. Three tickets in a row have been refuted by predicting a count without allowing for the population moving under their own hand; this row is the allowance. | ≥ 1 unbounded site of mine, or 0 sites of mine (which would mean I dodged the population rather than entered it bounded) |
| **P7** | **The excluded file types are declared with their size, not globbed away.** Population: tracked `.txt` and `.py` (22 and 16 by D3). I predict their site count under the same predicate exceeds **100**, that it is **reported and not repaired**, and that the reason printed is *transcripts and instruments quote sites rather than assert them*. | site count ≤ 100, or the population omitted from the transcript |

### The consumers

| # | prediction | how it is falsified |
|---|---|---|
| **P8** | **At least 5 distinct published figures inherit the glob**, across **at least 3 distinct files**. Population: figures in tracked prose whose value is computed over, or quoted from, the `docs/*.md` universe. Grain: one published figure. | fewer than 5, or fewer than 3 files |
| **P8a** | `s6_class.py`'s *"gate covers 2 of 7 corpus files"* is one of them — its denominator **7** is the glob's file count and inherits the undercount even though the numerator is about something else. | the denominator not derived from the glob |
| **P8b** | **At least one consumer is a figure nobody has named yet** — not `36`, `12`, `29`, `17` or `7`. | every consumer I find is one of those five |

### The self-check repairs

| # | prediction | how it is falsified |
|---|---|---|
| **P9** | Tightening `OWNSCOPE` to H3's standard (D7: the matched scope must carry a digit that is a **count or a bound**, not a label such as `POP-3`) scores mg-d075's criticism sentences at **7 of 10** — mg-aaf4's figure, re-derived by me from the source rather than copied from its transcript. | any value other than 7, which I publish as a disagreement with mg-aaf4 rather than adjusting my classifier |
| **P9a** | The one that survives hand adjudication is the headline sentence *"FOUR was not the population, and EIGHT is not either."* | a different sentence surviving, or none |
| **P10** | Adding `code/branching_bound_d075/PREDICTIONS.md` to `MINE` raises the criticism population from **10** to **18** (+8, mg-aaf4's C3), of which **≥ 6** carry no numeric scope. | a different added count, or fewer than 6 |
| **P11** | Replacing the tense-sensitive `FAULT` token `cannot see` with a **property match** (any of *can/could/cannot/could not/does not/did not* against *see/detect/reach/cover*, plus the existing markers) admits the sentence *"mg-19ec's POP-3 predicate could not see it"*, and that sentence **fails** the numeric standard, because `POP-3` is a label and not a count. | the sentence still missed, or admitted and scored as bounded |
| **P12** | The repaired check, run over mg-d075's three authored documents, **exits 1** — it bites. | exit 0 |
| **P13** | **Every check I build is proved able to fire before its pass is trusted.** For each of the four repairs (universe, `OWNSCOPE`, `MINE`, `FAULT`) the self-test constructs an input on which it fires and asserts it does. I predict **≥ 1 defect of this instrument** is found by its own self-test and recorded rather than quietly fixed. | no positive control for some check, or 0 instrument defects recorded (which I would report as a suspiciously clean run, not as success) |
| **P14** | **The declaration partitions the population with nothing left over:** every site of the full tracked-`.md` universe falls in exactly one declared class — repairable, dated audit record, or pre-registration — and the class sizes sum to the total. | ≥ 1 site unclassified, or the sizes not summing |

### What I will not do

| # | prediction | how it is falsified |
|---|---|---|
| **P15** | **I do not edit `mg-d075`'s or `mg-aaf4`'s instruments, transcripts or pre-registrations.** The three repairs are shipped as a **successor gate in this directory**, and mg-d075's suite still re-runs green from my branch — 7 of 7 on its committed predictions. Editing `s5_own_criticism.py` in place would make its committed transcript non-regenerable, which is the exact defect mg-aaf4's D2 caught one level up. | any file under `code/branching_bound_d075/` or `code/branching_bound_audit_aaf4/` modified by my commits, or its suite not green |
| **P16** | **I do not repair the 24.** 22 of them are unrepairable for reasons that are correct (dated records, pre-registrations) and 2 belong to other tickets' instruments. My deliverable is the declaration, not the edit. | any of the 24 sites reworded by me |

---

## 2. EXIT VALUES, PREDICTED

| script | predicted exit | why |
|---|---|---|
| `p1_glob.py` | **1** | exits 1 when the glob's actual match set differs from the set it is described as matching. It does. |
| `p2_population.py` | **1** | exits 1 when the published corpus unbounded count is an undercount of the full population. It is. |
| `p3_consumers.py` | **1** | exits 1 when ≥ 1 published figure inherits the undercount. |
| `p4_selfcheck.py` | **1** | exits 1 when any criticism sentence fails the numeric standard — P12. |
| `p5_declaration.py` | **0** | exits 1 only if a site of the full population falls in no declared class — P14. |
| `selftest1d6c.py` | **0** | exits 1 on any failing case, after P13's defects are fixed; the first form's transcript is committed either way. |
| `run_all.sh` | **1** | four of the six are predicted 1 **and are supposed to be**. A runner made green by weakening a check that fires is the thing this arc exists to catch. |

**7 predicted exit values. 16 predictions and 8 sub-rows.** Nothing below the line in this file
will be revised after a run. If a prediction misses, it stays as written and the miss is
reported next to it.

---

## 3. THE ONE THING I AM MOST LIKELY TO GET WRONG

**P3 and P4 — that 24 reproduces.** I am forecasting an exact match on three numbers, through a
parser that is not the one that produced them, over a universe I have not yet enumerated. The
honest reason I expect it: mg-aaf4 kept the parent's unit deliberately so that a disagreement
about a count could not hide inside a disagreement about a parser, and mg-d075's 8/4/4, 9/4/5
and 10/10/0 already reproduce across both parsers. If P3 misses, the finding is that the two
parsers disagree — which would be a bigger result than the one I was sent to get, and I would
publish it as such rather than as a correction to the 24.

**And the second most likely: P5.** *Exactly half* is the kind of figure that survives into a
report because it is memorable. I have predicted 12/12 because that is what mg-aaf4 measured
and I have no reason yet to doubt it — but I have written P5's falsifier to name the alternative
in advance, and if the re-derivation gives anything else, the half goes and the number stays.
