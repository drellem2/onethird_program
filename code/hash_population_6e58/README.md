# mg-6e58 — the arc's denominator, and what a capital letter was hiding

`code/hash_population_6e58/` — 5 scripts, 55 self-test assertions, worst
exit 1.

`PREDICTIONS.md` was committed **before any script of this instrument
existed** (`90e0cee`, displaced by the refinery rebase — see the last section).
23 rows scored, **19 hit, 4 missed, every miss kept as written** with what was
wrong recorded beside it.

Run it with `./run_all.sh`. Three scripts exit 1 **by design and by
prediction** — `p2` because the denominator is wrong at this tree, `p3`
because the sentence it scores is in another ticket's document, `p4` because
the gate it examines cannot fire and this branch does not edit it.

---

## THE HEADLINE: THE OMISSION WAS NEVER ONLY ABOUT CASE

The ticket, from mg-0ba7's audit of mg-b2af: `lib330a._HASH_FORMATS` is
`("--format=%H", "--pretty=%H", "--format=format:%H")`, and `--format=%h` —
**lower-case** — is not in it, so the population this arc's every count is
taken over is defined by a capital letter.

That is true, and it is not the whole of it. At this tree, over every `*.py`
under `code/`, one `ast` walk classified under four nested denominators:

| figure | POP-A `_HASH_FORMATS` | POP-B `+ "--format=%h"` | POP-C git's documented spellings |
|---|---|---|---|
| ALL call sites | 45 | 60 | **86** |
| history-derived | 23 | 31 | **55** |
| `NEWEST` | 9 | 10 | 11 |
| `INDEXED` | 12 | 15 | 25 |
| `UNRESTRICTED` | 2 | 6 | **19** |
| `OLDEST` | 12 | 12 | 12 |
| `PICKAXE` | 6 | 11 | 12 |
| `RANGE` | 4 | 6 | 7 |

Grain: one `ast.Call` node = one site. Population: every `*.py` under `code/`
at **this branch's tree** — not mg-330a's tree, not mg-0ba7's. mg-0ba7
reported 44 → 59 and 1 → 4 at its own tree; I have run none of its code and
those figures are not re-derived here, because a before/after across two
trees measures the trees.

**Adding `--format=%h` to the tuple recovers 15 sites and leaves 26.**
Sixteen of the 26 emit a **full `%H` hash**:

```
--format=%H %s          --format=%H\t%s          --format=%H%x1f%s
--format=%H%x1e%B%x1f   --format=%H%x1f%s%x1f%B%x1e
```

Every one of those contains the exact placeholder `_HASH_FORMATS` is built
out of, and the tuple cannot see any of them — because `f in strs` is
**equality** and the format string is longer than the literal. There is no
lower-case letter anywhere in `--format=%H %s`.

So the class is not *"`%h` is missing"*. The class is *"the format test is a
literal-set membership over a string with internal structure."* A repair that
adds a fourth literal fixes one instance of a class with at least two
members. **That is the ninth generation of the shape the ticket says not to
add, and it is why this ticket does not edit the tuple.**

The full spelling table, measured rather than recalled:

| spelling | sites | grain | in `_HASH_FORMATS`? |
|---|---|---|---|
| `--format=%H` | 45 | FULL | **yes** |
| `--format=%H\t%s` | 8 | FULL | no |
| `--format=%H %s` | 4 | FULL | no |
| `--format=%H%x1f%s` | 2 | FULL | no |
| `--format=%H%x1e%B%x1f` | 1 | FULL | no |
| `--format=%H%x1f%s%x1f%B%x1e` | 1 | FULL | no |
| `--format=%h` | 15 | ABBREV | no |
| `--format=%h %s` | 2 | ABBREV | no |
| `--format=%h %ad %s` | 2 | ABBREV | no |
| `--oneline` | 7 | ABBREV | no |

`--format=format:%H` **is** in the tuple and is at no site here, so the
tuple's effective width at this tree is **two** spellings out of ten.

---

## HOW THE WAYS WERE ENUMERATED, SINCE THAT IS THE ACTUAL ASK

> ENUMERATE THE WAYS, not the flags you happen to recall, and say how you
> enumerated them.

`p1_ways.py` reads `man git-log` on this machine (git 2.50.1) and parses it.
It prints what it read, so the claim being checked is a **reading**:

- **Placeholders.** 58 parsed from the placeholder list; 6 whose description
  contains "hash"; **2** whose description is a *commit* hash — `%H`
  (`commit hash`) and `%h` (`abbreviated commit hash`). `%T`/`%t`/`%P`/`%p`
  are excluded by reading their descriptions, not by my knowing what they
  are. **The two differ by case alone, and that is the ticket in one line.**
- **Built-in formats.** 7 found whose documented sample shows a commit
  identifier (`oneline`, `short`, `medium`, `full`, `fuller`, `reference`,
  `email`). `raw` and `mboxrd` are handled but **not** found — declared in
  `lib6e58.EXTRACTOR_BLIND` with the documentation sentence that exempts
  each, because a blind spot that is written down is a different object from
  one that is not.
- **Options.** `--oneline` (documented as `--pretty=oneline
  --abbrev-commit`), `--abbrev-commit`, `--no-abbrev-commit`. The last two
  never make a hash appear; they change its **grain**, so `--abbrev-commit`
  demotes FULL to ABBREV within the same call and is never an emitter alone.
- **The default.** With no `--format`, git's documented default is `medium`,
  which prints `commit <hash>`. So a bare `git log` **is** revision-producing
  and mg-330a's classifier returns `None` for it. Measured separately as
  POP-D rather than folded in — see below, where all of POP-D's increment
  turns out to be false positives.
- **Named and not counted**: `rev-parse --short`, `rev-parse`, `show
  -s --format=%H`, `describe`, `rev-list`, `for-each-ref
  --format=%(objectname)`. Each addresses a commit; none is `git log`, and
  changing the subcommand set would make the before/after incomparable.

---

## THE SELFTEST IS THE DELIVERABLE

The brief is explicit that what ships must fail if someone later adds a fifth
spelling. `selftest_6e58.py` is 55 assertions, every one on a line of Python
**constructed in the file** and parsed with `ast` — nothing asks the
repository anything.

- **The positive control contains both cases**, side by side, and is built
  before anything is counted:
  `git("log","-1","--format=%H","--",path)` and the same line with `%h`. The
  detector separates them by **grain** (FULL vs ABBREV); mg-330a's tuple
  **sees the first and not the second**, which reproduces the defect on a
  constructed line rather than recalling it from a tree. A case-blind search
  is run against the same control and shown to match both while being unable
  to say which is which — the brief's warning, executed instead of quoted.
- **The equivalence that makes this a defect and not a count**:
  `git log -1 --format=%h -- <path>` classifies as **`NEWEST`** — A-1's
  defect, spelled with a lower-case letter — and identically to the `%H`
  line, so the difference between them is the denominator and nothing else.
- **git's own escape rules**: `%%h` is a literal percent and **not** a hash;
  `%x68` is a hex byte and not a placeholder; `format:`/`tformat:` prefixes;
  `--pretty=oneline` is FULL and `--pretty=oneline --abbrev-commit` is
  ABBREV.
- **Closure, two-sided.** Everything git documents must be handled, and
  everything handled must be documented **or declared**. A **drill** injects
  a fifth spelling (`%Q`, and a `futureline` format) into a *constructed* man
  page and requires the closure comparison to go red — because a gate that
  has never been seen red is a gate whose red is unmeasured.
- **And from the other direction**: every placeholder used in any `git log`
  format anywhere under `code/` must be one git documents. A spelling that
  appears in the tree without appearing in the documentation turns this file
  red.

---

## THE CONSUMERS — WHICH PUBLISHED FIGURES INHERIT THE OMISSION

The ticket asks for the consumers, not just the constant. Eleven, all
computing over `_HASH_FORMATS` directly or through `lib_b2af.census`, which
imports it:

`lib330a.py:218` (the constant) · `s1_anchors.py` · `out_s1_anchors.txt` ·
`audit_330a/README.md` · **`docs/audit-mg-330a-the-anchor-and-the-term.md`** ·
`lib_b2af.py:295` · `t1_population.py` · `ANCHORS.tsv` ·
`repair_b2af/README.md` · `selftest_b2af.py:272` · `repair_b2af/PREDICTIONS.md`

**One of them is a merged document.** `docs/audit-mg-330a-the-anchor-and-the-term.md`
states *36 revision-producing `git log` call sites* and *16 history-derived
call sites across 13 directories* in commit `fba5f63`. So yes — a figure
computed over the narrow denominator is asserted in a merged commit. It is
**named here and not rewritten**: it is another ticket's document, and
mg-b2af declined to rewrite it for the same reason.

**`_HASH_FORMATS` is also left as it is.** mg-330a's transcripts are evidence
of a run. Widening the constant behind them makes every committed figure in
that directory unreproducible *while still looking reproducible* — which is
the exact failure mode mg-b2af named as DISPLACEMENT. The corrected
classifier lives here, is written from git's documentation rather than
imported, and is checked against mg-330a's over the same `ast.Call` nodes:
**87,934 nodes compared, 0 kind disagreements under POP-A.** Every delta in
this document is therefore attributable to the denominator and not to a
re-taxonomy.

---

## THE STILL-OPEN LIST NAMES A FILE THAT IS IN NO CENSUS IT CITES

mg-b2af's `WHAT IS STILL OPEN` says `code/repair_69d1/p3_reason.py` is
*"the one site in the 19"* that is `UNRESTRICTED`. The ticket says the count
is wrong. It is — and the **referent** is worse.

| commit | `UNRESTRICTED` POP-A | POP-C | `git log` sites in `repair_69d1/` |
|---|---|---|---|
| `fba5f63` mg-330a on `main` | 1 | 9 | **0** |
| `b94cb1e` its pre-rebase twin | 1 | 8 | **0** |
| `b1c3467` the claim's own tree | 1 | 14 | **0** |
| this branch | 2 | 19 | **0** |

`code/repair_69d1/` contains **no `git log` call of any spelling**, at any
commit measured. It anchors on `HEAD` through `git grep`, `git show` and
`rev-parse` — none of which this census can see. The one `UNRESTRICTED` site
under mg-330a's own classifier is `code/repair_8d5e/lib8d5e.py:167`.

**How a non-member got into the sentence.** mg-330a's taxonomy *docstring*
names a kind `HEAD`, and that prose row is where `p3_reason.py` is named.
`classify_call` never returns `HEAD` — it returns `UNRESTRICTED`, which the
prose never mentions:

| | |
|---|---|
| documented but never returned | `HEAD`, `TWO-SIDED` |
| returned but never documented | `UNRESTRICTED`, `NEWEST-norestrict` |

So the sentence took a **name** from one taxonomy and a **count** from
another. That is mg-b2af's own F-2 — one number over two populations —
committed inside mg-b2af's list of what it left open.

**And the corrected count is not itself a finding.** All 19 are hand-read in
`p3`: every one splits the output into a list and searches it. By mg-330a's
own `RANGE` reasoning those are *a set, not an anchor*. **The count went
1 → 19 and the number of unrestricted single anchors went 0 → 0.** Reporting
"19 sites of the defect" would be a term denoting more than it covers, which
is mg-2c77's A-2, which this arc has already made once.

The correction is written into `code/repair_b2af/README.md` beneath the
original bullet, which is left as written.

---

## F-A — A GATE WHOSE INPUT CANNOT CONTAIN THE THING IT GATES ON

`t1_population.py:430` checks `not [r for r in pinned if r["kind"] ==
"OLDEST"]`. `pinned` is `ANCHORS.tsv`; `t1` writes it from `spendable` ⊂
`refined` ⊂ `_hist`, and `lib_b2af` filters `_hist` to `HISTORY_KINDS =
("NEWEST", "NEWEST-norestrict", "INDEXED", "UNRESTRICTED")`. **`OLDEST` is
not in that tuple.** The tested set is empty for every input the script can
produce.

Proved from the code path *and* constructed in a clone: delete `--reverse`
from one `OLDEST` site, and `OLDEST` goes **12 → 11**, the site re-enters as
`INDEXED` — a treated kind — and the gate still evaluates `True`. That
reproduces mg-0ba7's construction, which I had not run and had only read
about.

`p4` ships a gate that **can** see it: a set difference over the tree's own
classification at two points, fired on the construction (1 row) and silent on
the unmutated control (0 rows). `t1_population.py` is **not** edited — its
committed transcripts are evidence of a run of that script, and editing one
without regenerating the other makes the pair inconsistent. The note in
mg-b2af's README points here.

---

## WHAT FIRED ON ME

- **My selftest went red on its first complete run**, exactly as `P5-a`
  predicted and not on what I expected: it reported `%a` and `%c` as
  undocumented placeholders. `placeholders_in` tokenises one character after
  `%` (right for a hash, which is never longer) while git documents `%ad`,
  `%an`, `%cr`. **A single-character tokeniser and a single-character
  documented set agreed with each other and disagreed with git.** Kept at
  `out_selftest_6e58_FIRSTFORM_exit1.txt`; the comparison is now made at the
  finer grain and the reason is in the code.
- **My documentation extractor missed two of the formats `P1-c` named**,
  including `oneline`, because its first rule required the literal
  `commit <hash>` and `oneline`'s documented sample is `<hash> <title-line>`.
  Kept at `out_p1_builtins_FIRSTFORM.txt`. `raw` is still missed and is a
  declared exemption, so `P1-c` is a **partial miss** and scored as one.
- **My claim-locator in `p3` was an exact-string test defeated by a line
  break.** It looked for `one site` in the raw file text, where the sentence
  wraps as `the one\nsite`. An exact match beaten by whitespace, one commit
  after naming exact matches beaten by case. Kept at
  `out_p3_unrestricted_FIRSTFORM_selferr.txt`.
- **My hand-adjudication of the POP-D rows was keyed on `file:line`, and a
  line moved.** Editing `lib6e58.py` shifted its own site from 353 to 363, so
  a verdict I had already written came back `NOT ADJUDICATED` — **A-1, the
  defect at the root of this whole arc, committed inside its repair by me.**
  It is keyed on the source text now.
- **`P2-b` missed by one because I summed the wrong grain.** I predicted 87
  by adding up spelling *occurrences*; there are 87 occurrences in **86**
  calls, because one call carries two spellings. A grain error, in the ticket
  about naming the grain.
- **`P2-d` missed and the measured number then moved while I worked** — two
  of the POP-D rows are my own scripts, which entered the population as I
  wrote them. The figure is printed from the run and quoted in no sentence
  here, because any sentence carrying it would be stale by the commit that
  shipped it.
- **`P2-e` was wrong in both directions.** I predicted every kind except
  `RANGE` would grow; `RANGE` grew and `OLDEST` did not.
- **`P3-c` was wrong and the truth was worse.** I predicted the extra
  `UNRESTRICTED` sites were a *staleness* — a directory that did not exist
  when the sentence was written. They are not: the named file has never been
  in the population, at any of the four commits measured.

---

## WHAT I DID NOT DO — STATED, NOT IMPLIED

- **I ran none of mg-0ba7's code and have not seen it.** Every claim I
  attribute to mg-0ba7 comes from the ticket body written by pm-onethird. Its
  44 / 22 / 1 → 59 / 28 / 4 figures are **not** re-derived here; they were
  measured at a different tree, and I re-derived the *finding* at mine
  instead. The one thing I can say about its numbers is that my tree
  disagrees with all six of them, which is what two different trees do.
- **I did not edit `lib330a._HASH_FORMATS`**, `s1_anchors.py`,
  `t1_population.py`, `ANCHORS.tsv`, or any committed transcript of mg-330a
  or mg-b2af. I did not re-run their suites.
- **I did not rewrite `docs/audit-mg-330a-the-anchor-and-the-term.md`.** Its
  `36` and its `16 across 13 directories` are named as consumers and left in
  place.
- **I did not repair mg-330a's `log` half**, though `p2` (v) shows it matches
  a filename, a banner and the word inside its own source. Every count here
  holds it fixed so the delta is attributable to the denominator. Recorded so
  it is not found for a tenth time.
- **I did not adjudicate whether the 26 newly-visible sites are *defects*.**
  They are members of a population that was mis-drawn; whether each one's
  anchor should move is the next ticket's question, and answering it here
  would be a term denoting more than it covers.
- **I did not gate the arc's *other* documents** against the corrected
  denominator. `p2` names the eleven consumers; treating them is not what
  this ticket does.

---

## A FORECAST THIS TICKET MAKES ABOUT ITSELF

`PREDICTIONS.md` was committed at `90e0cee` on this branch. **The refinery
rebases before merging, so that sha will not exist on `main`** — and
`git merge-base --is-ancestor 90e0cee main` will return a **false negative**
that says nothing about whether the content landed. The check that works is
`git patch-id --stable`, comparing the pre-registration commit's patch id
against the commits on `main`.

This was written before the merge, not discovered after it (`P5-d`), and it
is the same displacement mg-b2af forecast for its own transcripts and mg-aaf4
forecast for its own predictions file. Three generations have now recorded it
in advance; none has been surprised by it.

---

## THE FILES

| file | what it is |
|---|---|
| `PREDICTIONS.md` | 23 scored rows plus 3 disclosures, committed before any script existed |
| `lib6e58.py` | the apparatus: the man-page enumeration, the format-string parse, the four populations, the classifier written from mg-330a's docstring |
| `selftest_6e58.py` | 55 assertions on constructed lines — the positive control, the escape rules, the closure, the fifth-spelling drill |
| `p1_ways.py` | the ways, read out of `man git-log` and printed with what they were read from |
| `p2_population.py` | the four denominators, the deltas, the eleven consumers, the before/after |
| `p3_unrestricted.py` | the STILL-OPEN sentence, its count, its referent, and how the two taxonomies got joined |
| `p4_gate.py` | F-A: the proof from the code path, the absorption constructed in a clone, and a gate that fires on it |
| `out_*.txt` | the committed transcripts of the run that ships |
| `out_*_FIRSTFORM_*.txt` | the runs where three of my own checks fired on me, kept rather than deleted |
