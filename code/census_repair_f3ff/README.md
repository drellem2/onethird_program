# mg-f3ff — the dropped-verdict census, re-derived from the tree, and the method repaired

pm-onethird filed four **DROPPED VERDICT** tickets inside ten minutes on
2026-07-31. Every one asserts, in its title, some form of *no landing commit* /
*no successor*. The census that produced them was built from **mail routing**,
not from the commit tree, and mg-e35b's polecat had already proved one row
false.

This deliverable re-derives all four rows from the commit log of **both** repos,
scores each against predictions committed **before any script here existed**
(`72e36cb`), and replaces the method.

    sh run_all.sh          # ~50 s, pure Python 3 + git, no third-party packages

Suite exit **0**. Selftest **40 checks, 0 FAIL**.

---

## 1. The four rows

| row | ticket | filed (UTC) | parent | premise `no successor` is | successor commits at filing | predicted (72e36cb) |
|---|---|---|---|---|---|---|
| 1 | mg-e35b | 04:13:24 | mg-fcf1 | **REFUTED** | 7 | REFUTED — **HIT** |
| 2 | mg-fccb | 04:12:41 | mg-d112 | **REFUTED** | 5 (4 + 1, both repos) | REFUTED — **HIT** |
| 3 | mg-a74f | 04:22:15 | mg-16eb | **UPHELD** | 0 | UPHELD — **HIT** |
| 4 | mg-dffa | 04:22:50 | mg-5800 | **UPHELD** | 0 | UPHELD — **HIT** |

Both clocks agree on all four rows: no row's verdict depends on whether you read
author date or committer date.

### The accuracy, with the denominator named

**2 of 4.** The population is the four DROPPED VERDICT tickets filed between
04:12:41Z and 04:22:50Z — the **whole census**, not a sample of it, and n = 4.
All four are now checked against the tree.

The brief's own figure was *1-of-1 refuted so far on a population of 4*, with
three rows unchecked. That figure is **superseded, not contradicted**: 4 of 4
checked, 2 refuted. `2 of 4 wrong` and `4 of 4 wrong` are different claims and
nothing here rounds toward either.

### Were the polecats sent to re-land existing work?

Rows 1 and 2 were dispatched on a premise the tree already contradicted — 7 and
5 successor commits respectively already existed at the filing instant. Rows 3
and 4 were not: 0 successor commits existed, and their briefs were sound.

**Two of the four polecats caught it themselves, before mg-f3ff existed.**
mg-e35b's `5f542f0` corrects the premise and lists the chain by sha. mg-fccb's
`1b00147` carries a section headed *PREMISE CORRECTION* — and diagnoses the
cause: *"the detector likely missed it because b169561's subject names mg-dbd1
and mg-1fdb but not the verdict id mg-d112."* That polecat had already found
NC1's failure mode by hand.

Whether their own commits **duplicate** the pre-existing work is not decidable
from commit metadata, and s3 reports the overlap rather than judging it. See §6.

---

## 2. The repaired method

`lib_f3ff.py` states its population and its blind spots **in the source**, and
`s0` prints both. In short:

**Population.** Every commit reachable from `origin/main` in each repo of a
**named repo list**, after a fetch whose exit status was checked. A commit is a
successor of parent *P* when its **full message** contains *P*, its owning
ticket is not *P*, and its date is ≤ the filing instant.

**Three rules the old method broke:**

1. **Fetch first, resolve `origin/main` explicitly, print the sha.** Never a
   bare local `main`, never `HEAD`. Every section prints its own freshness — a
   freshness measured once and imported is a claim, not an observation.
2. **State the staleness.** The committed transcripts were taken with
   `one_third_width_three` **46 commits behind** origin/main — it was 45 an hour
   earlier in this same session, which is the point: the number is a property of
   the run, not of the repo, so it is printed by every section rather than
   asserted once in prose.
3. **UNKNOWN is not zero.** `successors()` returns `None`, never `[]`, for an
   unreadable repo, and UNKNOWN is sticky across a readable one. Enforced twice
   — at the library level in the selftest, at the script level in NC3.

**The repo list is not taken from the ticket's `repo:` field.** Row 2's parent
carries `repo: one_third_width_three` and has four of its five successors in the
*other* repo. Scoping a search to the ticket's own metadata is the mail defect
with a different bounded channel — see NC4b.

### What it cannot see — eight blind spots, and three of them bite here

B1 unmerged branches · B2 repos not on the list · B3 successors naming neither
the parent nor a descendant · B4 rewritten history · B5 rebase-moved committer
dates · B6 non-commit landings · B7 mention-is-not-descent · B8 tickets deleted
from the work store.

Three are **demonstrated on this population** rather than merely listed:

- **B2** — NC4b, below.
- **B7** — the chain reader run strict and loose: 3 generations / 10 commits vs
  7 / 81 on row 1. The loose reader compounds citations into "generations".
- **B3** — s4: three mg-a806 commits that mg-e35b's own verdict counts as chain
  are invisible to **both** readers.

---

## 3. Negative controls (`s2`)

| control | what it does | result |
|---|---|---|
| **NC1** subject-only reader | reads `%s` instead of `%B` | **degrades on rows 1 and 2** — 0 successors where the full reader finds 7 and 5. A tree reader that reads only subject lines fails identically to the mail census. |
| **NC2** the mail reader | re-implemented against pm-onethird's own 938-message maildir | **agrees with the tree on 4 of 4.** See §4 — this refutes P7 and it is the most load-bearing result in the run. |
| **NC3** forced fetch failure | takes the same branch the real `ssh: connect to host github.com port 22` took, in both directions | **GREEN.** 4 of 4 rows print UNKNOWN; `generations()` returns None. Never "no successor". |
| **NC4** stale checkout, constructed | re-runs the identical derivation at `origin/main~10/~25/~60` and at the 46-behind local HEAD | 0 of 4 verdicts flip at any pinned depth; row 2's `one_third_width_three` count moves 1 → 0 at the real local HEAD. |

### NC4b — the census's wrong answer, reproduced from the commit log

Take the census's **own repo scoping** (row 2 searched only in its parent's
`repo:` field) and the **46-behind checkout** this run actually found on disk:

```
both repos, origin/main   -> 5 successors -> REFUTED   (what s1 reports)
scoped repo, origin/main  -> 1 successor  -> REFUTED
scoped repo, local HEAD   -> 0 successors -> UPHELD    <-- THE CENSUS'S WRONG ANSWER
```

Two defects, **neither of which is "reading mail"**, either alone leaving the
verdict standing, together reproducing the census's error *with the authority of
having read the tree*. This is the ticket's addendum, constructed rather than
warned about.

---

## 4. The finding that changes the account of what went wrong

**The reconstructed mail reader does not reproduce the census's error.** It
agrees with the tree on 4 of 4 rows, including both rows the census got wrong.
The successor information *was* in pm-onethird's own inbox, before the filing
instant, naming the successor tickets by id — 2 such messages on row 1, 1 on
row 2. **P7 predicted 0 and is a MISS.**

So:

- **Stands** — the census was built on mail rather than the tree and is wrong on
  2 of 4 rows. s1 measures that directly and it does not depend on this control.
- **Stands** — a channel-based census cannot distinguish silence from absence,
  whatever this particular inbox happened to hold.
- **Falls** — *"the mail store contained no successor, so the census could not
  have known."* It did contain one. The census looked for a **verdict message
  addressed to it** and read the absence of that shape as absence of the work;
  mentions of the successor sitting in the same inbox did not count because they
  were not the shape it queried.
- **Open** — this reconstruction is mine, not pm-onethird's code. I did not find
  the census's implementation and do not claim to have run it. What is measured
  is that the **information was present**, not that the original query would have
  found it.

---

## 5. Scorecard against `72e36cb`

Eleven predictions, committed before any script here existed. **8 hit, 2 missed,
1 sub-clause missed.**

| | prediction | result | where |
|---|---|---|---|
| P1 | row 1 REFUTED, ≥3 generations | **HIT** (3 strict / 7 loose — see §7) | `out_s1_rows.txt` |
| P2 | row 2 REFUTED in both repos | **HIT** | `out_s1_rows.txt` |
| P2′ | …successors *all* authored 2026-07-29 | **MISS** — 954c29e is 07-30 | `out_s1_rows.txt` |
| P3 | row 3 UPHELD | **HIT** | `out_s1_rows.txt` |
| P4 | row 4 UPHELD | **HIT** | `out_s1_rows.txt` |
| P5 | 2 of 4 refuted, n=4, brief's figure superseded | **HIT** | `out_s1_rows.txt` |
| P6 | subject-only control degrades rows 1 and 2 | **HIT** exactly | `out_s2_controls.txt` |
| P7 | 0 mail messages name a successor on row 1 | **MISS** — 2 do | `out_s2_controls.txt` |
| P8 | ticket graph buys ≥1 commit on row 1 the direct grep misses | **MISS** — 0 on row 1 (**4 on row 2**) | `out_s3_graph.txt` |
| P9 | rows 3 and 4: successor tickets exist, all commits postdate filing | **HIT** — 2 and 4 tickets, 6 and 10 commits, all after | `out_s3_graph.txt` |
| P10 | a *second* row self-refuted by its own polecat | **HIT** — rows 1 and 2 | `out_s3_graph.txt` |
| P11 | ≥1 declared blind spot bites on this population | **HIT** — B2, B7, B3 | NC4b, s1, s4 |

**No prediction was edited after seeing a result.** P2′, P7 and P8 are recorded
as missed. P8 is instructive: the graph bought nothing on the row I named and
**4 commits on the row I did not**, which is a different claim from the one
committed and is not counted as a hit.

---

## 6. Defects of this instrument, kept

1. **s3's weak rule.** The first P10 rule was a keyword flag; it fires on row 4,
   where "premise" is about the mathematics and there are 0 successor commits for
   it to be about — a false positive on 1 of the 3 rows it flags. The weak rule
   is **kept in the source beside** the strong one rather than deleted.
2. **The chain reader is wrong in both directions** (§7).
3. **P10's strong rule proves a citation, not an intent.** The quoted lines are
   printed so the reader scores the meaning.
4. **`generations()` loose mode is O(frontier × repos × log)** — its frontier
   grows with every citation, which is why `s1` at ~19 s is the slowest section
   of a ~50 s suite. Not a correctness defect, but it is the same
   mention-is-not-descent problem showing up as runtime.

---

## 7. s4 — the chain reader measured against a list it did not produce

mg-e35b's polecat listed row 1's chain **by sha** in `5f542f0`, before mg-f3ff
existed. s4 extracts those shas from the commit message (rather than
transcribing them — a hand-typed ground truth is one I could have typed to agree
with my own output), cross-checks the extraction against the hand transcription
from the ticket body (**they agree exactly, 9 of 9**), and scores both chain
modes against it.

Ground truth: 13 commits. **Strict finds 5. Loose finds 10. Neither contains
it.** The three missed by both are mg-a806 commits naming neither mg-fcf1 nor
any descendant — blind spot B3.

So `3 generations` and `7 generations` are **both wrong** as a count of the
chain, and row 1's depth figure should be read as a bracket, not as either
endpoint.

**This does not move any row verdict.** REFUTED/UPHELD is decided by the
generation-1 successor count, which is a direct grep of the parent id and does
not use the chain descent at all. That is the scope of the damage, stated — not
a defence of the depth figure.

---

## 8. WHAT I DID NOT DO

- **I did not reopen mg-e35b, mg-fccb, mg-a74f or mg-dffa.** All four are done.
  A census is repaired by replacing the instrument, not by editing the rows it
  produced.
- **I did not rewrite the four ticket bodies**, and did not correct the
  "no successor" claims in their titles.
- **I did not re-audit the mathematics of any parent**, or check whether any
  parent's findings were right.
- **I did not decide how much of rows 1's and 2's polecat work was duplicate.**
  s3 reports the overlap in commits; whether `5f542f0` re-lands `8fc5111` is a
  reading of two deliverables, not a metadata comparison, and I did not do it.
- **I did not find or run pm-onethird's actual census code.** NC2 is my
  reconstruction of the method from its description. §4's "Open" says what that
  does and does not license.
- **I did not query the mail store's routing records** — only message contents
  and `Date:` headers. Whether a verdict mail was *sent and dropped* versus
  *never sent* is not distinguished here.
- **I did not search any repo beyond the two named.** B2 is a blind spot of the
  replacement, disclosed, and NC4b shows it biting.
- **I did not check the other two repos in `~/research`** (`one_third`,
  `union_closed`) for successors. If the arc's work reaches them, this census
  cannot see it.
- **I did not touch either source repo's working tree.** `git fetch` only; no
  checkout, pull, stash, or rebase in `/Users/daniel/research/*`.
- **I did not verify that the `~/.macguffin/work` store is complete.** B8 stands:
  a deleted ticket is invisible to s3.

---

## 9. Files

| file | what |
|---|---|
| `PREDICTIONS.md` | committed at `72e36cb`, **before any script here existed** |
| `lib_f3ff.py` | the method: population, blind spots, fetch/UNKNOWN, successor and chain readers |
| `s0_freshness.py` | which tree — fetch, resolve, print sha and staleness |
| `s1_rows.py` | the four rows re-derived, both clocks, scored against P1–P5 |
| `s2_controls.py` | NC1–NC4b, scored against P6–P7 |
| `s3_graph.py` | ticket-reference graph, duplicate-work overlap, scored against P8–P10 |
| `s4_crosscheck.py` | the chain reader vs mg-e35b's independent list |
| `selftest_f3ff.py` | 40 checks on the harness itself |
| `run_all.sh` | the runner; reports the instrument's status, not `tee`'s |
| `out_*.txt` | committed transcripts of a full run |

⚠️ `out_s1_rows.txt` is the transcript of the run **as merged, before mg-cf83**.
It is deliberately not regenerated: it is the record of a run at its own commit,
and re-running it here would re-derive census figures that mg-4d3b has since
confirmed and this ticket was told not to re-open. The post-repair transcript —
healthy path and failure path, side by side — is
`code/summary_guard_cf83/out_c1_summary_guard.txt`.

⚠️ The same applies to `out_s2_controls.txt`, `out_s3_graph.txt` and
`out_s4_crosscheck.txt`: they are the transcripts of the run **as merged, before
mg-7085**, and are deliberately not regenerated for the same reason. The
post-repair transcripts — six scripts, three arms, before *and* after, side by
side — are in `code/sibling_sweep_7085/out_r1_sweep.txt` (§11).

---

## 10. mg-cf83 — `s1_rows.py`'s summary block, repaired

> **Scope.** This section is about **`s1_rows.py` only** — that is the file
> mg-cf83 repaired, and its transcript is the evidence below. The same defect
> was alive in three of its siblings until mg-7085; that sweep is **§11**, and
> until it landed, a reader who stopped here would have concluded the
> deliverable's summary blocks were repaired when `s3_graph.py`'s was not.

mg-4d3b ran this directory's own `s1_rows.py` against a repo whose `git fetch`
really failed. **The per-row sections were right and the summary block was
not**, in one transcript: `n = 4, and all 4 are now checked against the tree`
printed when 0 were; `The census was WRONG on 0 of its 4 rows and RIGHT on 0`;
`4 of 4 checked, 0 refuted`; four rows of `0 / 0` from `0 if not gens else
len(gens)`, where `not None` is True; and then a `TypeError` on `len(None)`,
thirty lines from the docstring saying callers must not treat None as an empty
list. A total fetch failure read as a clean, fully-measured result — in the
part a human reads first.

`s1_rows.py` now holds three rules, each exercised against a **real** broken
remote by `code/summary_guard_cf83/c1_summary_guard.py`:

1. **`?` and `0` are different answers.** `cell()` renders an unmeasured figure
   as `?`; `generations()` returns `None` for unreadable and `[]` for a genuinely
   empty chain, and the table no longer prints them the same.
2. **No fixed string asserts a count that was not measured.** Every sentence
   carrying a figure has a branch for the figure not existing, and that branch
   prints UNKNOWN.
3. **The summary cannot disagree with the rows.** Every figure after the row
   loop is a fold over `lines`, which is the row sections' own output. Nothing
   in the summary re-reads a repo or calls anything that can return `None` —
   which is also why F5's crash is now unreachable rather than merely caught.

The prediction scoring gained a third state, `UNMEASURED`: a row that could not
be read is neither a hit nor a miss, and calling it a MISS asserts an outcome
the run did not observe. `s1` now exits **1** when a repo could not be read —
findings about the census still exit 0, as `run_all.sh` documents; *this run did
not happen* is a different thing and exits like `s0_freshness.py` does.

---

## 11. mg-7085 — the rest of the sweep: `s2`, `s3`, `s4`

§10 was true of `s1_rows.py` and of nothing else. mg-407f confirmed that repair
sound in all three arms with a harness sharing no code with it, and found the
same defect **alive in two siblings** — by running them, not by reading them.
This section is the rest of the sweep. Evidence:
`code/sibling_sweep_7085/out_r1_sweep.txt`, which runs all six scripts and
`run_all.sh` in three arms, **in both the before and the after state**, so every
"repaired" claim below is a *difference between two runs* rather than an absence
observed once. An absence observed once is also what a script that never ran
looks like.

### The spelling lesson, which is the part worth reusing

mg-cf83's ticket told it to grep `0 if not gens`. **That spelling finds the site
already repaired and nothing else.** The live defect was spelled

```python
g1 = p8_gain.get(1, 0)          # s3_graph.py
```

— a **dict default on an accumulator the row loop's `continue` never wrote**,
which is the same None-becomes-zero merger wearing different syntax.
`p9_rows.get(3)` returning `None` and rendering as `no` is the same one again,
in boolean clothing. So a sweep must **enumerate the ways a `None` can become a
`0`** — `or []`, `.get(k, 0)`, `if not x`, `len(x or [])`, a truthiness test on
a possibly-`None`, a bare `for` over a possibly-`None` — and then **check each
site by running the failing arm**, because reading a guard is exactly what makes
an insufficient one look sufficient.

### What was live, what was latent, and how each was told apart

Classified from the **printed output of a real failing run** — a broken remote
set *after* cloning, so `origin/main` still resolves and the UNKNOWN is a failed
fetch rather than an absent ref — never by reading the source.

| site | spelling | verdict | evidence |
|---|---|---|---|
| `s3_graph.py` scoring block | `p8_gain.get(1, 0)`, `p9_rows.get(n)` | **LIVE** | rows print `UNKNOWN — a repo could not be read.`; `OBSERVED: 0` prints **twelve lines below**; P8/P9/P10 scored MISS; **exit 0** |
| `s2_controls.py:80` | `sum(len(x) for x in _p.values())` | **LIVE** | dies with mg-4d3b's F5 verbatim: `TypeError: object of type 'NoneType' has no len()` |
| `s4_crosscheck.py:110` | `for gen in gens` | **LIVE, and only on the *partial* arm** | `TypeError: 'NoneType' object is not iterable` |
| `s3_graph.py:85-86` | `or []` | **LATENT** | sits after the `continue`; never reached in any arm run |
| `s2_controls.py:130-131` | `or []` | **LATENT — with an expiry date** | sits after the crash; see below |
| `s2_controls.py:247-288` | `len(successors(...))` | **LATENT** | sits after the crash |
| `s0_freshness.py`, `selftest_f3ff.py` | — | **MEASURED CLEAN** | run in both failing arms; no crash, no false zero, exits correct |

**The `or []` sites are not billed as the live defect.** mg-407f classified them
LATENT from printed evidence and that was right. Billing them live was the easy
wrong answer, and disagreeing with it would need printed evidence of its own.

**But one of them had an expiry date, and that is the load-bearing detail.**
`s2_controls.py:130` is latent *only because the crash at line 80 returns
first*. Repair the crash alone and control flow reaches it: `None` becomes `[]`,
`tree` becomes `UPHELD`, and NC2 prints `MAIL says UPHELD; TREE says UPHELD;
agree` — **an agreement between a reader and a reader that said nothing**, in
the control whose result §4 of this README rests on. So it is repaired in the
same commit as the crash. A latent site downstream of a live one is not a
separate ticket; it is part of repairing the live one.

### What the three rules cost `s3_graph.py`

The row loop used to `continue` past an unreadable row **without recording
anything**, which is precisely what let a dict default speak for it. It now
appends an `UNMEASURED` entry, and every scoreboard figure is a fold over that
list — rule 3, the same shape as `s1_rows.py:154-160`. `?` and `UNMEASURED`
render where `0`, `no` and `MISS` used to. The exit agrees with `s1`: **1** when
a repo could not be read.

**The sharpest form of the finding is the flip.** On the healthy arm `P9` and
`P10` print `HIT`; on the broken arm the *unrepaired* file printed `MISS` for
both. Two published prediction verdicts inverted **with nothing changed but
whether a repo could be read**. After the repair the healthy arm still prints
`HIT` and the broken arm prints `UNMEASURED`, and the flip is gone.

### `s2_controls.py`: a control that did not run is not a control that passed

Beyond the crash, two controls asserted results from nothing:

- **NC1 would have gone RED.** With `moved` collapsed to `False`, every row
  compares `UNKNOWN` to `UNKNOWN`, `deg` is empty, and the RED branch fires:
  *"the harness does not distinguish the readers"* — a **false accusation
  against this instrument**, raised by a run that read no repo, exiting 1 for
  the wrong reason. It is now `UNMEASURED`, which is neither GREEN nor RED.
- **NC4 is gated whole, and not merely None-guarded.** Its question is *does
  staleness alone move the answer*, which it answers by differencing a live read
  against a pinned one. `Pinned` hard-codes `unknown = False`, so on a failing
  arm the live side is UNKNOWN while the pinned side reads a ref that still
  resolves locally — the control would print a difference, attribute it to
  staleness, and be measuring the fetch failure. Putting a `?` at each `len()`
  would have kept it running and kept it wrong.
- **NC3 is degenerate under total failure**, and now says so. It forces *one*
  repo to fail; if the other is unreadable anyway, GREEN means *"UNKNOWN was
  printed"* and not *"the forcing caused it"*. Stated, not counted as evidence.

### `s4_crosscheck.py` — a guard one repo narrower than the thing it guarded

Its guard checked `fm[REPOS[0]].unknown`. `generations()` returns `None` if
**any** repo is unknown. So under a **partial** fetch failure — repo 1 readable,
repo 2 not; the commonest arm there is, and the one a half-broken network
produces — it walked past its own guard, printed a ground truth, and died at the
scoring loop. This is `len(None)` in a new costume, caught by `for gen in gens`
instead of by `len`.

**No prior arm would have found it.** Under *total* failure the first guard
fires and the file is clean; mg-cf83's and mg-407f's failing arms were total, and
s4 was one of the three scripts neither ran at all. It was not known-good — it
was unmeasured, and this is what was under it.

### The coverage gap, closed rather than re-recorded

mg-407f recorded that `s0_freshness`, `s4_crosscheck` and `selftest_f3ff` had
never been run in any arm, and asked that this silence not become a clean bill
of health. All three are now run in both failing arms:

- **`s0_freshness.py`** — clean. UNKNOWN propagates, exits 1. Not repaired.
- **`selftest_f3ff.py`** — clean, 0 FAIL, exits 0 under both failing arms.
  ⚠️ One observation, **not repaired and noted rather than swept**: it resolves
  `git rev-parse --show-toplevel` from its own CWD, so run from a directory that
  is not inside a git checkout it dies on `not a git repository`. This harness
  produced exactly that on its first run and it looks identical to a finding
  about the subject. It is a fragility of the selftest's fixtures, not the
  None-becomes-zero defect, and it is left alone.
- **`s4_crosscheck.py`** — **not clean**; see above.

**`run_all.sh`'s aggregate exit** was also unmeasured and is now measured: **0**
on the healthy arm, **1** on both failing arms — before *and* after. It exited 1
before the repair too, because `s0`/`s1`/`s2`/`s4` already failed and **masked
`s3`'s false 0**. An aggregate that is 1 because *something* failed cannot tell
you which script lied. The per-script exits can, which is why they were made to
agree.
