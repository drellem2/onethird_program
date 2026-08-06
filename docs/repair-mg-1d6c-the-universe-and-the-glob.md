# mg-1d6c — the universe, the glob, and what a gate should say about what it cannot reach

**Instrument:** `code/corpus_universe_1d6c/` — `sh code/corpus_universe_1d6c/run_all.sh`
(~30 s, no network, no dependencies). **It exits 1 and is supposed to**: four of its six
steps are predicted 1 in `PREDICTIONS.md` because the things they check are true.

**Predictions** were committed at `c192801`, before any `.py` of that directory existed, with
nine hand measurements disclosed as measurements. **That SHA will not be an ancestor of `main`
— the refinery rebases before merging.** Check it by `patch-id` against the `predictions:`
commit that landed, not by `git merge-base --is-ancestor`.

---

## 1. WHAT THE GLOB MATCHES, AGAINST WHAT IT IS DESCRIBED AS MATCHING

mg-d075's corpus universe is written in its own prose as *"the whole docs corpus … every
`docs/*.md`"* and implemented as `os.listdir(L.DOCS)` filtered on `.endswith(".md")`. Both sets
are enumerated by `p1` and diffed in both directions; nothing here is a reading of the pattern.

**Population: files. Grain: one file.**

| universe | mechanism | files |
|---|---|---|
| `G_IMPL` | `os.listdir(docs)` — the universe **as implemented** | **106** |
| `G_SHELL` | `sh -c 'ls -1 docs/*.md'` — the universe **as written** | **106** |
| `D_TRACK` | `git ls-files`, `.md` under `docs/` **at any depth** | **118** |
| `M_TRACK` | `git ls-files`, `.md` anywhere | **295** |
| `M_DISK` | `os.walk`, `.md` anywhere outside `.git/` | **295** |

**THE IMPLEMENTED UNIVERSE DIFFERS FROM THE DESCRIBED ONE IN TWO MECHANICAL WAYS**, and both
are printed whether or not they bite:

- **It is not recursive.** **12** tracked markdown files under `docs/state-history/` are
  invisible to it.
- **It reads the working tree, not the index.** At this commit that hole is **real and empty**
  — 0 untracked and 0 tracked-but-absent. It is printed as empty rather than omitted, because
  a hole that costs nothing today is the one that costs silently tomorrow.

**THE CONTROL COMES FIRST.** `G_IMPL` against `G_SHELL` is **empty**, so the diff machinery
reports no difference where there is none — which is why the differences above are differences.

**AND THE NON-RECURSION COSTS ZERO SITES.** Population: live sentences of those 12 files.
Grain: one sentence. **0 sites, 0 unbounded.** *The whole of the gap this ticket is about is
the `docs/` boundary and none of it is the missing `**`.* The zero is trustworthy because the
same code, pointed at a constructed tree whose subdirectory does hold a site, reports it —
`selftest1d6c.py` U1/U2, the most important cases in that file.

---

## 2. THE POPULATION, AND WHETHER IT IS 24

**Derived from `git ls-files` at a named commit, never from `os.listdir`** — a re-derivation
through the same mechanism cannot discover what that mechanism excludes.

**Population: every `.md` tracked at the named commit. Grain: one sentence (S) and one written
occurrence (O). Predicate: the arc's RELAXED, `lib_d075`'s own code, executed.**

| state | commit | files | sites S | unbounded | occurrences O |
|---|---|---|---|---|---|
| **A** mg-aaf4's census | `8132d75` | **13** | **51** | **24** | **60** |
| **B** main's tip when this ticket began | `20614ef` | 13 | 51 | **24** | — |
| **C** the working tree, including my own files | — | 14+ | 52+ | **24** | 61+ |

**24 IS THE COUNT.** mg-aaf4's `13 / 51 / 24 / 60` reproduce **exactly** — and they reproduce
through the *other* parser: this instrument imports `lib_d075` and changes only the file list,
so where mg-aaf4 re-implemented the reader, I execute the parent's. **The cross-parser control
is 0 rows either sees alone**, so a count that differs from mg-aaf4's is a universe difference
and cannot be a parser difference.

**THE SPLIT IS 12 INSIDE `docs/` AND 12 OUTSIDE, AND IT IS A COINCIDENCE OF THIS CORPUS, NOT A
LAW.** Nothing forces the two sides to be equal; the ratio moves the moment any ticket writes
one more figure-stating sentence on either side of the boundary. The tidy half is reported
because it re-derives, not because it is memorable.

**THE POPULATION MOVED UNDER MY OWN HAND AND THE BILL IS PRINTED.** `PREDICTIONS.md` P6 said in
advance that this ticket's own prose would enter the population it measures, and predicted the
contribution would be **sites > 0 and unbounded = 0** — because every figure-stating sentence I
write carries `rank 6` in that same sentence. `p2`'s STATE C prints my sites and my unbounded
count as a separate row. Three tickets in a row were refuted by predicting a count without
allowing for the population moving under their own hand; the allowance is the prediction.

**THE EXCLUDED FILE TYPES ARE DECLARED WITH THEIR SIZE.** Population: tracked `.txt` and `.py`.
Grain: one sentence. **122 sites in 32 files, 48 unbounded** — reported, **not** repaired, and
named rather than patterned away. A transcript *prints* a site and an instrument *matches* one;
neither asserts the figure in its own voice, and bounding a transcript means editing the record
of a run. **It is the same decision mg-d075 made. The difference is that its size is here.**

---

## 3. WHICH PUBLISHED FIGURES INHERIT THE UNDERCOUNT

The 12 is one symptom. `p3` enumerates the rest four ways.

**C1 — the call sites.** Population: tracked `.py`. Grain: one occurrence of a universe-building
idiom. **4 narrow occurrences, every one of them mg-d075's** — `s1_census.py:96`, `:143`, `:242`
and `s6_class.py:95`. **Control:** the same scan finds **141** recursive or git-derived
occurrences elsewhere in the same corpus, so it is not blind to breadth.

**C2 — the transcript figures.** **3** `SUMMARY` lines over the corpus, all correct over the
population their instrument could see:

```
SUMMARY s1_census: D corpus 36 sites in 7 files, 12 unbounded
SUMMARY s1_census: PRE-REPAIR D corpus 29 sites, 17 unbounded
SUMMARY s6_class: corpus 7 files, 36 sites, 12 unbounded remaining
```

**C3 — the prose figures.** Population: live sentences of tracked `.md` naming the corpus
universe and carrying a number. Grain: one sentence. **30 sentences, 12 carrying a glob-derived
value, 18 in the control column.** Machine, then hand-adjudicated per row with a reason:

| verdict | rows | |
|---|---|---|
| **INHERITS** | **4** | states a glob-derived value as the population — 3 in mg-d075's README, 1 in its account document |
| DIAGNOSES | 4 | mg-aaf4 states the glob's figure in order to fault it |
| MINE | 3 | this ticket's own prose, quoting with attribution |
| NOT A CONSUMER | 1 | mg-aaf4's *"24 files of `docs/` carry a `33` line"* — a different quantity colliding with the glob's bounded-site count |

**C3c — THE CONSUMER NOBODY HAD NAMED.** `docs/repair-mg-d075-the-figure-and-its-scope.md:51`
publishes the universe's *own size*: *"the **101 `docs/*.md`** that are not this repair's own"*.
It is not a site count, so no audit of the site counts ever looked at it, and it carries the
same boundary. Re-derived at this commit: **the glob 106, tracked `.md` under `docs/` 118, the
repository 295.**

**C4 — the second-order consumers.** **5 files carry an inheriting figure; 3 of them quote it
rather than compute it.** Each is a dated record and none is edited here.

**AND IT HAS ALREADY DRIFTED IN A COMMITTED TRANSCRIPT.** mg-d075's suite re-runs green from
this branch — 7 of 7 scripts on their committed predictions, `run_all.sh` exit 0 — and **two of
its transcripts do not regenerate**: `out_s6_class.txt` on its commit count (mg-aaf4's finding,
`git log --all`), and `out_s1_census.txt` on **`102 docs/*.md exist now` → `105`, twice**. That
is C3c's quantity moving in a published record with no exit code anywhere saying so — and it
moved again while this ticket was being written: **105 at that hand run, 106 once this account
document itself landed in `docs/`.** Evidence:
`code/corpus_universe_1d6c/out_donotdisturb_d075.txt`. The directory is restored; this branch
carries no regenerated output of it.

---

## 4. THE SELF-CHECK, REPAIRED TO THE STANDARD IT ENFORCES

`s5_own_criticism.py` says applying a weaker standard to itself *"would be the defect a second
time"*. It is a weaker one in three ways. **Nothing of mg-d075's is edited** — its regexes and
its file list are imported from its source and executed, and its published result is reproduced
before anything is disagreed with. Editing `s5` in place would make its committed transcript
non-regenerable, which is the defect mg-aaf4 caught one level up.

**Population: mg-d075's authored prose. Grain: one sentence.**

| | criticism sentences | carrying a numeric scope |
|---|---|---|
| `s5` as published | 10 | **10 of 10** — reproduced exactly |
| **FIX 1** — the standard is H3's: a count or a bound, not a keyword | 10 | **7 of 10** |
| **FIX 2** — `+ code/branching_bound_d075/PREDICTIONS.md`, never looked at | **18** | 6 of the 8 added carry none |
| **FIX 3** — a property match instead of the tense `cannot see` | **19** | the 19th is *"mg-19ec's POP-3 predicate **could** not see it"*, and it carries no numeric scope |

**FIX 1 is my classifier and it was wrong twice before it was right.** Its first form —
H3's digit rule transplanted onto `s5`'s accepted substrings — scored **9 of 10** and accepted
`code/branching_audit_19ec` (a path with a hex ticket id) and `10 sentence` (out of *"the row-10
sentence"*). The first form's transcript is committed as `out_p4_selfcheck_FIRSTFORM_exit1.txt`
and the reasoning sits at the point of the check. **DISCLOSURE: the respecification moves my
count towards the finding I was sent to check.** The compensation is that `p4` prints **three
classifiers side by side, row by row** — `s5`'s, mine, and mg-aaf4's, imported and executed —
and mine and mg-aaf4's **agree on 10 of 10 rows** having been written independently.

**Hand adjudication: 3 fall, 2 are false negatives of my regex, 1 stands** — the same 3 → 1 as
mg-aaf4, reached by my own reading, published per row with reasons. **The one that stands is the
repair's own headline sentence:** *"FOUR was not the population, and EIGHT is not either."* It
asserts of two published figures that they are not the population and names neither the
population, the file, nor the grain. The table carrying all three is nineteen lines above it —
and a neighbouring table is exactly what this repair told the *document* was not enough.

**FIX 3 is a property, not a synonym list**, because a tense-sensitive detector drifts again on
the next word: a negated or modal verb of perception, over eleven verbs, tense- and aspect-free.
Eight cases in `selftest1d6c.py` hold it to that, including the case that asserts the parent's
own regex **does** miss the tense.

---

## 5. THE DELIVERABLE: A GATE THAT DECLARES WHAT IT CANNOT REACH

> **WHAT mg-d075 COULD HAVE DONE IS NAME THE POPULATION AS EXCLUDED, INSTEAD OF DRAWING THE GLOB
> SO THAT IT NEVER APPEARED.**

`p5_declaration.py` is that gate. **It counts the whole population and then says, by name and
with a number, which parts of it it will not act on.** A gate reporting 12 because 12 is all it
can see is indistinguishable from a gate reporting 12 because 12 is all there is.

**Population: every `.md` tracked by git — 295 files. Grain: one live sentence.**

| class | unbounded sites | what the gate does |
|---|---|---|
| LIVING DOCUMENT | **0** | **enforced** — this file is reworded freely |
| INSTRUMENT README | **2** | **enforced** — ordinary prose about an instrument |
| PRE-REGISTRATION | **10** | **declared exclusion** — never reworded |
| DATED RECORD | **12** | **declared exclusion** — editing destroys the evidence trail |
| UNCLASSIFIED | **0** | the gate **fails** on any of these |
| *tracked `.txt` and `.py`* | *48 in 32 files* | *declared exclusion — outside the `.md` universe* |

**22 of 24 are excluded by a stated invariant rather than by the shape of a pattern**, the
partition is total, and **the 2 that are enforced are named** — `code/branching_audit_5800/README.md`
and `code/branching_repair_41aa/README.md`. They are **not repaired here**: they belong to other
tickets' instruments, and this ticket repairs a universe, not a sentence. A backlog that is a
list can be worked; a backlog that is a number cannot.

**The gate is proved able to fail.** Five constructed trees, and the one that matters is C5:
**a file cannot buy an exemption by living in `docs/`.** The exemption is for audit *records*;
a `docs/` file that is not one falls through to UNCLASSIFIED and fails.

---

## 6. PREDICTIONS SCORED

**16 predictions, 8 sub-rows, 7 exit values. Nothing was revised after a run.**

| # | outcome |
|---|---|
| P1, P1a, P1b | **HELD** — two mechanical differences; 12 files invisible; the tracked/worktree hole real, empty, and printed |
| P2 | **HELD** — the recursion blind spot costs **0** sites |
| P3 | **HELD** — 13 / 51 / 24 / 60, all four, through the other parser |
| P3a | did not arise — the parsers agree row for row |
| P4 | **HELD** — unchanged between `8132d75` and `20614ef` |
| P5 | **HELD** — 12 / 12, re-derived, and reported as a coincidence |
| P6 | **HELD** — this ticket entered the population it measures, and entered it bounded |
| P7 | **HELD** — 122 sites in the declared file-type exclusion, > 100 |
| P8, P8a, P8b | **HELD** — 4 call sites + 3 transcript figures + 4 inheriting sentences across 5 files; `s6`'s denominator among them; and C3c is the unnamed one |
| P9 | **HELD at 7 of 10** — by a classifier that needed one respecification, with the first form's transcript kept |
| P9a | **HELD** — the headline sentence is the one that stands |
| P10 | **HELD** — 10 → 18 criticism sentences, 6 of the 8 added carry no numeric scope |
| P11 | **HELD** — the tense-hidden sentence is admitted and fails the numeric standard |
| P12 | **HELD** — `p4` exits 1; the check bites |
| P13 | **HELD, and later than I expected.** Every check has a positive control — 40 self-test cases, 6 in `p4`, 5 in `p5`, all firing. **3 defects of this instrument** are recorded rather than quietly fixed: two in `p4`'s scope classifier, found by putting three classifiers side by side; and **`M3`, a vacuous self-test case that read a global property to test a local one, passed twice, and failed the instant this ticket wrote an unrelated file into `docs/`** |
| P14 | **HELD** — the partition is total, 0 unclassified |
| P15 | **HELD** — 0 files of mg-d075 or mg-aaf4 modified by my commits; mg-d075's suite green, 7 of 7 |
| P16 | **HELD** — the 24 are not repaired |

**Exit values: 7 of 7 on prediction.**

---

## 7. WHAT THIS TICKET DID NOT DO

- **It did not repair the 24, or any of them.** 22 are excluded for reasons that are correct and
  2 belong to other tickets. The deliverable is the declaration, not the edit.
- **It did not edit mg-d075's or mg-aaf4's instruments, transcripts or pre-registrations.** The
  three fixes to `s5` are shipped as a successor check in this ticket's own directory. mg-d075's
  `s5_own_criticism.py` is unchanged on disk and still exits 0 on its own population.
- **It did not run the wide `.txt`/`.py` population as a gate.** It is declared with its size and
  left alone.
- **It did not re-derive mg-d075's pre-repair corpus figures** (29 / 17). Only the post-repair
  36 / 12 was reproduced against the working tree; the pre-repair pair is quoted from mg-d075's
  own transcript and is labelled as quoted wherever it appears.
- **It changed no line of the living document.** The living document has **0** unbounded sites
  and needed none.
