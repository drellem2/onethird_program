# A count that says `sites` and prints rows

*The independent audit of `mg-70c7` (`d456f58`, `973ca61`), which landed the six
findings of `mg-dee4` against `1ee1f1b` (`mg-7522`). `mg-7522` repaired the
three open sites of `682db2c` (`mg-05eb`), which audited the arc-wide `| tee`
sweep `52aeaf4` (`mg-c2b3`).*

Instrument: `code/runner_exit_audit_56dc/`. `sh run_all.sh`, about four minutes,
pure Python 3, no dependencies, no network. Every figure below is printed by a
probe in that directory next to the predicate that produced it.
`PREDICTIONS.md` was committed **before any probe in that directory existed**;
**five of its predictions missed and are kept as written.**

---

## The short version

`mg-70c7` repaired six things and repaired them where it pointed. The audit's
subject is what it pointed at.

1. **The `16 of 16` is sound, and this is the first place it is shown both
   ways.** 3 `git diff` source lines run 8 times; 8 `| tee` lines run 8 times
   *because no loop encloses one of them*. **11 sites, 16 executions**, derived
   here under a parser that shares no code with either of the arc's two.
2. **And one directory over, the same distinction is lost.**
   `out_r4_property.txt` prints **10** under the label `executing sites`. It is
   a count of **(site, target) match rows**. The distinct-**site** count is
   **9** — and **9** is what the README, the published document, the probe's own
   docstring and the prediction `OUTCOMES.md` scores as a **HIT** all say.
3. **The strictest rule the repair applies to anything stops at a path.**
   `r6_self.py`'s E1 — *every count over source carries a grain word* — ranges
   over `M.outs(M.TREE)`: the `out_*.txt` of one directory. The four artifacts
   the same tree calls *"my reader-facing artifacts"* are outside it.
4. **The "one rule object" is one of the two rules, not their union.** `proven`
   was an alternative of the old self-facing rule, and `mg-dee4`'s transcript
   names it in a row of its own — *`in SELF and not in SUBJECT  1  proven`*. It
   is not in the merged rule.
5. **Two copies of the figure rule disagree on the number 3.** That is the floor
   item; nothing in the brief named it.
6. **The class of preserved-but-unlabelled transcripts has 38 members.** One was
   found by a worker's conscience. The population had not been counted.

---

## 1 — sites are not runs, counted both ways

> **A source line inside a loop is N executions. Where the two numbers coincide,
> say why they coincide — a ratio of 1 that is a fact about the source reads
> exactly like a ratio of 1 that is a mistake.**

| runner | loop items | SITES | EXECUTIONS | why |
|---|---|---|---|---|
| `state_delegation_audit_16eb` | 3 | **2** | **6** | 2 lines × 3 items |
| `state_delegation_repair_0049` | 2 | **1** | **2** | 1 line × 2 items |
| `face_geometry_audit_f1b2` | 0 loops | **5** | **5** | no loop encloses a `\| tee` |
| `face_geometry_audit_fcf1` | 0 loops | **3** | **3** | no loop encloses a `\| tee` |
| | | **11** | **16** | |

The published `16 of 16` is at the execution grain and holds.
`out_s2_status.txt` already prints this breakdown; this is an independent
derivation of it, and the reason the `| tee` column has a ratio of 1 is printed
rather than assumed.

Of the **50** printed count rows in `mg-70c7`'s seven transcripts, **3** claim
the execution grain outright, **46** claim a site grain, **1** carries no grain
word within eight lines, and **4** get their grain only from a **column header
further up than any two-line window can see** — F4's own defect, arriving at the
grain check rather than at the marker check.

## 2 — the count that says `sites` and prints rows

`libc2b3.targets` returns *every shell script a line names*. One line can name
two:

```py
ck("`sh ./x.sh` is seen", L.invocations("sh ./b0.sh | tee o.txt"),
```

`selftestc2b3.py:155` — a both-senses fixture the repair itself added — names
`x.sh` and `b0.sh`. The scan emits two rows for it, and the transcript adds them
under the label **`executing sites`**:

| grain | outside the two names |
|---|---|
| (site, target) **rows** | **10** |
| distinct **sites** | **9** |

Both numbers reproduce at the transcript's own publishing commit, at HEAD, and
in `mg-70c7`'s own probe re-run live. **Four artifacts state 9** — the README,
the published document, `r4_property.py`'s docstring, which adds that this is
*"a measurement and not a citation of mg-dee4"*, and the **R5a** row that
`OUTCOMES.md` scores as a **HIT**. It is a citation of `mg-dee4`, which measured
9 before those fixtures existed. The prose is right about the grain; the
instrument prints the other one; the two were never compared.

**The same shape once more.** The sites reading `c0_repro.sh`'s exit status are
published as **10 in 5 files**, **nine in four files**, **nine in three files**,
and **9**. The differences are whether the instrument counts its own line and
sites against files. Re-derived under the probe's own rule: **10 in 5** with the
instrument trees, **9 in 4** without. No artifact says which reading it is at.

## 3 — a self-check whose population is a path

> **A self-check that stops at its own directory has a population defined by a
> path. It has not passed; it has not been run.**

`r6_self.py` asks four questions of this tree. The **figure** census reaches the
README, `OUTCOMES.md`, `PREDICTIONS.md` and the published document. The **grain**
check — the rule that repairs F1, the largest finding — does not: its population
is `M.outs(M.TREE)`. Run unchanged over those four here, it examines **48** count
lines it never saw.

It flags **0**, and that is kept rather than softened: I predicted at least three
and there are none. The finding is the reach and not a body count, which is
`mg-dee4`'s own argument about `0 USES` over `*.py` + `*.sh` — and the **marker**
check has that population too. `MINE_PY + MINE_SH`, **9** files, with its own
three `*.md` and its document outside it, in the section that repairs F3, three
paragraphs from `R3b` faulting `mg-7522` in exactly those words.

## 4 — the union that was not a union

`mg-dee4`'s F3 was nine alternatives for the subject and three for itself. The
repair made one object — the **subject's nine, verbatim**:

| | in the merged rule |
|---|---|
| `confirmed exactly`, `byte-identical`, `byte for byte`, `verified`, `(measured)`, `identical`, `confirmed`, `all <n>`, `exactly <n>` | yes |
| **`proven`** | **no** |

`proven` was one of the old self-facing rule's three, and `mg-dee4` printed a row
about it: *`in SELF and not in SUBJECT  1  proven`*. Its own D4 used the
**ten**-alternative union. `R3a` puts **the three markers the D4 docstring
names** to the merged rule and finds all three; three is not the population of
markers this arc names.

## 5 — the floor item: two copies of one rule

The repair's answer to F3 is that *two rules cannot be kept in step by intention;
they can be kept in step by being one object.* `MARK` is one object. `figures()`
is two:

```py
lib70c7.py   _SMALL = 3        ...   if v <= _SMALL:   continue
lib7522.py                     ...   if v > 2:         out.append(v)
```

Over the integers 0..500 they disagree on **exactly one value — `3`** — while
both docstrings say they exclude *0, 1 and 2*. `r3_strength.py`'s R3c computes an
UNBACKED count with one copy and raises BAD when it differs from the number
`out_s5_self.txt` printed with the other.

## 6 — the population, tested outside its own definition

Both population repairs were put to cases that did not exist when either rule was
written, with the **pre-repair rule read out of the commit where it still runs**:

| case | pre-repair rule | repaired rule |
|---|---|---|
| a site executing `zz_probe_56dc.sh` | **MISS** | **HIT** |
| a fixture with no `set -e`, captured and read | **outside** | **in, arm VALUE** |

**And F6's failure direction.** `mg-70c7` measured the direction of its one
member and found it loud. A rule that caught only loud failures would be a
different rule, so a **quiet** fixture of the same shape was built and **run**:

| fixture | as written | discarded stage forced to fail | in the population? |
|---|---|---|---|
| loud | exit 0 | **exit 1**, prints `DISAGREES` | in |
| quiet | exit 0, `rows seen: 7` | **exit 0**, `rows seen: 0` | in |

The quiet one is the silent green the sweep exists to find, and it is in the
population on exactly the same terms. **0** direction tests appear in either
membership predicate, asked of the code with the docstrings removed. The clause
is the population rule it claims to be.

## 7 — the fixture, and the class

`out_k1_census.txt` was **not** regenerated; its body is byte-identical to the
blob at `52aeaf4` and still reads *ticket 1 / re-derived 0 / DIFFERS*. **The
hazard is measured:** over the 64 runners at the ticket's own revision, the
pre-repair regex matches **0** and the repaired one matches **1**. The
transcript will not reproduce, and a reader who re-runs it concludes the record
was wrong.

At `main` the note was at **1 of 3** sites. This ticket adds it to the
transcript — as a label above a marker line, with the record below unaltered —
and to `mg-05eb`'s citation of it. **The regeneration decision is not
revisited.**

**And the class, counted.** 406 committed transcripts → **298** cited from
outside their own directory → **79** that record a defect by a rule listed rather
than described → **38** whose producing code has changed since they were written.
**1** carried a note; **2** do now. The remaining **36** are named in
`out_t5_fixture.txt` and are not this ticket's to relabel. The criterion is
*necessary and not sufficient*, so 38 is an **upper bound** and the direction is
stated.

---

## What holds, and what was not disturbed

`mg-dee4`'s tree is **byte-unchanged** since `ba85387`, and both of its
disclosures are present verbatim — including the one that matters most, that
A5's first draft measured reach from **stdout**, scored **0 of 5** on a run that
had completed perfectly, and *"would have read A5d's forced-failure check as a
PASS for the same wrong reason"*. All **4** of `mg-70c7`'s kept misses are still
scored MISS and all **5** of its recorded instrument defects are still recorded.

**7 of 7** rows of the published population table at `bee07a1` re-derive. The
property population at `1ee1f1b^` is **exactly the four repaired files** under
the errexit clause and **five** under the widened one, the fifth being the member
the VALUE arm adds. The errexit arm at HEAD is **0**. The comparison is still
against a fixed pre-repair ref, and the HEAD-anchored call beside it is the 2×2's
own exhibit of why it must not be. **8 of 8** executions exit **0**.

## Two defects in this instrument, recorded rather than smoothed away

**The row census was written against HEAD and compared with a transcript
produced on another tree**, and reported the difference as my error before it
reported it as anyone's. It derives at the transcript's own publishing commit
now — read from `git log`, not named by hand — and re-runs the subject's probe
live, and it rests its finding on the column that reproduces while printing the
one that does not.

**The class census's first predicate returned 128**, which is every tree whose
runner was touched after its transcripts landed. A stage was added in front of
it: the transcript must **record a defect**, by a rule written down rather than
described. The 128 is kept in the record, because it is what the looser
predicate said and the looser predicate was mine.

## Five predictions missed, and they are kept

I predicted the transcripts held **60–130** count rows; they hold **50**. I
predicted the grain rule would flag **at least 3** lines of prose it had never
been run over; it flags **0**. I predicted a stable number for a column that has
no stable value. I predicted the class had **2 to 8** members; it has **38** —
predicting a population size from the one instance in front of me, which is the
error this entire arc is about, committed by its auditor in its own predictions
file. And I predicted `t5_fixture.py` would exit **0** once I had added the notes,
forgetting that its class finding is a finding.

## What is not established, named rather than folded into a total

That the VALUE arm is the *right* widening — a disagreement with a definition,
and the definition is written out in full. `mg-c2b3`'s own **34**, cited and
still not re-measured for the fourth ticket running — and at the **site** grain,
which is why it is still not added to the 16. That a stale-looking transcript
really fails to reproduce: **38** is an upper bound and only one member is
measured. Whether a grain **word** is the right one: T1a reads the word, and T1c
is what catches a wrong one, for the one count it re-derives at both grains. And
every intermediate commit: this is read at `HEAD` and at named refs, on one
machine.
