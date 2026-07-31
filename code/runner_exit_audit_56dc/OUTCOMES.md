# mg-56dc — outcomes

The independent audit of `mg-70c7`'s grain-and-population repair, which landed
the six findings of `mg-dee4` against `1ee1f1b`. Every figure below is printed
by a probe in this directory next to the predicate that produced it; the
transcripts are committed.

**The one-line verdict.** *The six repairs hold where they were pointed and both
population repairs hold against cases built outside their old definitions — but
the self-check has the shape of the finding it repairs: the strictest rule it
applies to anything ranges over the `out_*.txt` of one directory, its
self-facing marker population is the `*.py` + `*.sh` it faults `mg-7522` for,
its "one rule object" is the subject's nine alternatives verbatim and drops the
one `mg-dee4` named as being in the self rule and not the subject's, and four
artifacts publish `9` for a quantity their own instrument prints as `10`.*

---

## Predictions, scored

`PREDICTIONS.md` was committed at `6aa043a`, before any probe in this directory
existed. **Five missed and are kept as written.**

| id | prediction | outcome |
|---|---|---|
| **T1a** | 60–130 printed count rows in the 7 transcripts; ≥2 labels whose grain disagrees with the prose | **MISS — 50.** I predicted the row count from the transcripts' page length rather than from their table density; most lines in them are prose, not rows. The second half **HIT**: three quantities disagree (T1c, T1d, T1e) |
| **T1b** | `16eb` 2 sites / 6 executions, `0049` 1 / 2, total 3 / 8; the 8 `\| tee` in no loop so 8 / 8 | **HIT** — exactly, under a parser written here. **11 sites / 16 executions** |
| **T1c** | `out_r4_property.txt`'s 43 and 10 are ROWS; distinct sites 42 and 9 | **PART HIT, PART MISS.** The **outside** column is exactly as predicted — **10 rows / 9 sites**, reproduced at the publishing commit, at HEAD, and by `mg-70c7`'s own probe re-run live. The **all** column does not reproduce at all: the transcript prints **43** and the same rule gives **49** at the commit that ships it, because a whole-repository census moves while an arc is landing. I predicted a number for a column that has no stable value |
| **T1d** | 4 artifacts state 9 where the transcript prints 10 | **HIT** — `README.md:97`, the published document `:176`, `r4_property.py:7`, `OUTCOMES.md:42` |
| **T1e** | three readings of the `c0_repro.sh` caller count reproduce | **HIT** — four, in fact: `10 in 5`, `nine in four`, `nine in three`, and `mg-dee4`'s `9` |
| **T2a** | E1's population is one directory's `out_*.txt`; ≥3 count lines in the four artifacts flagged | **MISS — 0 flagged.** The population half **HIT** and is the finding; the body-count half missed, and the reason is worth keeping: I reasoned that prose unchecked by a rule would fail it. It does not. **A rule that is not run has not passed** — which is `mg-dee4`'s own argument about `0 USES` — but that is a statement about reach, and I predicted a number as if it were a statement about defects |
| **T2b** | `proven` is in `MARK_OLD` and not in the merged `MARK`; the union would be 10 | **HIT** — 9 / 3 / 10, and `mg-dee4`'s transcript carries the row `in SELF and not in SUBJECT  1  proven` |
| **T2c** | ≥1 marker USE outside the self-facing population | **HIT** — **6** USEs over the 3 `*.md` and the document, 0 of them UNBACKED under `R6b`'s own quoting exclusion |
| **T2d** | the two `figures()` copies differ on exactly `3` and agree on every other integer in 0..500 | **HIT** — 1 disagreement, 500 agreements |
| **T3a** | an invented basename is caught by the property and missed by the two-name rule at `1ee1f1b` | **HIT** — 3 of 3 against 2 of 3, with the pre-repair rule read out of the commit where it still runs |
| **T3b** | a no-`set -e` capture-and-read fixture is VALUE under the repaired clause and outside the errexit-only one | **HIT** — 2 of 2 against 0 of 2 |
| **T3c** | the quiet fixture is in the population on the same terms, and its forced arm exits 0 where the loud one exits 1 | **HIT** — both run; loud **1**, quiet **0** with its printed answer changed from `rows seen: 7` to `rows seen: 0` |
| **T3d** | 0 direction tests in either membership predicate | **HIT** — 0 in all four functions, asked of the code with the docstring removed |
| **T4a** | `mg-dee4`'s tree byte-unchanged, both disclosures present | **HIT** — 0 files changed since `ba85387`; 4 of 4, 2 of 2 and 1 of 1 phrases present |
| **T4b** | 4 kept misses and 5 recorded instrument defects | **HIT** |
| **T4c** | P0 72, P1 23/53, P2 errexit 19/26, either 20/27, shape 19/42, name 17/34 | **HIT** — 7 of 7 rows re-derive |
| **T4d** | exactly the four repaired files at `1ee1f1b^`, 0 at HEAD, anchor fixed | **HIT** — under the ERREXIT clause, which is the clause the claim was made under; the widened clause gives **five**, the fifth being the member the VALUE arm adds. Both are printed rather than one substituted for the other |
| **T4e** | 8 of 8 executions exit 0 | **HIT** — over 3 source lines |
| **T5a** | the transcript's blob is unchanged and still reads DIFFERS | **HIT** — its body is byte-identical to the blob at `52aeaf4` below the 37-line label this ticket prepends |
| **T5b** | the row re-derives as AGREES at HEAD | **HIT** — 1 file under the repaired regex, 0 under the pre-repair one, over 64 runners |
| **T5c** | 1 of 3 sites carry the note at `main`, 3 of 3 after | **HIT** |
| **T5d** | 2–8 members in the class, ≤3 noted | **MISS — 38 members, 1 noted at `main`.** I predicted from the one instance in front of me. The funnel is 406 committed transcripts → 298 cited from outside their directory → 79 recording a defect → **38** whose producing code has changed since. Predicting a population size from an instance is the error this whole arc is about, committed by its auditor in its own predictions file |
| **exit codes** | 0 / 3 / 4 / 0 / 0 / 0 | **5 of 6 HIT, `t5_fixture.py` MISS — 1.** I predicted T5 would go green once the notes were added and forgot that T5d's class finding is a finding, which is the same mistake as T2a's: reasoning about a probe's verdict from the part of it I was about to fix |

---

## Two defects in this instrument, recorded rather than smoothed away

**1. The row-grain census was written against HEAD and compared with a
transcript produced on another tree.** T1c's first run reported that my
derivation and `out_r4_property.txt` disagreed on the ROW count itself — 49
against 43 — and scored it as a defect of mine. It is neither: the caller census
ranges over the whole repository, and `973ca61` is a merge of a branch whose
probes ran before `mg-19ec` and `mg-3f3b` landed. The probe now derives at the
transcript's own **publishing commit**, read from `git log -1 -- <transcript>`
rather than named by hand, **and** re-runs `mg-70c7`'s own probe live so the
comparison is against a number produced now. The finding rests on the column
that reproduces and prints the one that does not, rather than dropping it.

**2. The class census's first predicate was `the producing code changed`, and it
returned 128.** That is every tree whose runner was touched after its
transcripts were committed — which is most trees, and says nothing about
evidence. The predicate now has a stage in front of it: **the transcript must
record a defect**, by a rule listed in the transcript rather than described
(`DIFFERS`, `SWALLOWED`, `WRONG`, `FINDING:`, `TOTAL BAD: [1-9]`, `MISSED`,
`*** `). 406 → 298 → 79 → 38. The 128 is not deleted from the record; it is what
the looser predicate said, and the looser predicate was mine.

*(A third thing worth recording as method rather than as a defect: the first
draft of the marker census split `lib7522.MARK` on every `|` and reported `of`
as a marker this arc names — it is the second branch of `\ball (?:\d+|of)\b`.
Splitting at depth 0, which is the rule `alternatives()` already uses to say
"nine against three", removes it. A different splitting rule in the audit of a
rule-splitting finding would have been this audit's own F3.)*

---

## What was added, and what was deliberately not touched

| artifact | changed? | why |
|---|---|---|
| `runner_exit_c2b3/out_k1_census.txt` | **a 37-line label PREPENDED; the record below it unaltered** | the PM's ruling: a transcript that no longer reproduces is a hazard unless it says so. The body below the marker line is byte-identical to the blob at `52aeaf4`, and `t5_fixture.py` checks that on every run. `mg-dee4`'s `a5_floor.py` scans this file for the first line carrying `pipefail` and a verdict; no line of the label carries both, so that scan returns the row it always returned |
| `runner_exit_audit_05eb/README.md` | **a note at the F2 citation** | the citation is what a reader meets first. Without the note, a reader who re-runs the transcript concludes the record was wrong, which is the opposite of the truth |
| the regeneration decision itself | **NOT revisited** | `mg-70c7` was right not to regenerate and the PM ratified it. That decision is not this ticket's, and nothing here re-runs `k1_census.py` into that file |
| `runner_exit_audit_dee4/*` | **NOT touched** | an audit's transcript is the record of what it found. T4a checks it is byte-unchanged |
| `runner_exit_repair_70c7/*` | **NOT touched** | this tree answers it; it does not edit it. The four artifacts stating `9` are named here rather than corrected, because correcting a subject's prose is how an audit stops being one |
| the other **36** members of T5d's class | **NOT touched** | they are named in `out_t5_fixture.txt`. Relabelling 36 transcripts across six arcs is not one audit ticket's call, and doing it silently would be worse than leaving it counted |

---

## What this audit did NOT check, named rather than folded into a total

* **Whether the VALUE arm is the right widening.** Inherited limit, stated by
  `mg-70c7` and by `mg-dee4` before it. T3 checks the population against cases
  outside the old definition; it does not argue the definition.
* **`mg-c2b3`'s own 34.** Cited, not re-measured, for the fourth ticket running.
  The covered set is still *16 executions run here + 8 `| tee` sites derived + 34
  inherited from a transcript nobody in this chain has re-run* — and note that
  the first of those three is at the **execution** grain and the other two are at
  the **site** grain, which is why they are not added.
* **Whether a stale-looking transcript really fails to reproduce.** T5d's
  criterion is necessary and not sufficient, so **38** is an **upper bound** and
  the direction is stated. Only one member is measured as actually not
  reproducing, in T5b.
* **Whether a grain WORD is the right one.** T1a reads the word. T1c is what
  catches a wrong one, and only for the one count it re-derives at both grains.
* **Every intermediate commit.** Read at `HEAD` and at named refs, on one
  machine — the same limit every tree in this arc states.
