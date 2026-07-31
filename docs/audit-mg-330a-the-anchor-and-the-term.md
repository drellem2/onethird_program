# Independent audit of the mg-8d5e anchor-and-term repair (`dfa263c`)

**mg-330a.** Pre-filed in the same action as its parent. Instrument:
`code/audit_330a/` — 6 scripts, 36 self-test assertions, worst exit 1.
`PREDICTIONS.md` committed in `71a1f55` **before any script of this instrument
existed**, 20 rows, 16 HIT, **4 misses kept as written** with what was wrong
beside each.

The brief's first instruction was the load-bearing one: **do not check the
derivation's logic — resolve it and look.** Nothing in this audit reads a
derivation and reasons about it.

---

## THE TWO OPEN SITES ARE CLOSED, AND THEY HOLD UNDER CONSTRUCTION

### A-1 — the anchor no longer follows a sentence

A cosmetic comment appended to `g1_provenance.py`, committed in a clone:

| probe | `REPAIR_REV` follows? |
|---|---|
| at `e2577e5` — the commit **before** the repair | **YES, silently.** All three history anchors move; `selftest_e34a.py` still exits **0** |
| at HEAD — the repair | **NO.** All four anchors unmoved, `ANCHOR_DRIFT` empty |

The control is the half that matters. At `e2577e5` the cosmetic commit
*becomes* `mg-76cc's repair` and its parent *becomes* `the pre-repair
predicate` — and nothing goes red, because there is nothing for the derivation
to disagree with. That is what "silently" means, and it is measured rather than
recalled.

All four anchors resolve to the pairs their prose names — `4755d029 /
3bc2cf76` and `4372fae9 / 52aeaf43` — and the **subject** of each commit is
printed beside the sha, because `4755d029 agrees with 4755d029` is true of any
derivation that has drifted onto its own pin. The two-sided property test holds
both ways: `kernel_source=` **present** at the anchor and **absent** at its
first parent, for each.

**Refuses or reports?** Both, correctly divided. A cosmetic edit **reports** —
the kept history derivation moves, is printed, and the `apart` distance grows.
A property-moving edit **refuses**. An instrument that refused to run on every
comment could not be run on a live tree.

**The three pieces fail in three different ways**, built here rather than read
out of `r1 (iii)`: a wrong pin (3 assertions, 1 drift row), an unfindable
marker (1 assertion, 1 drift row), a non-monotone marker (1 assertion, **0**
drift rows — caught by a different mechanism entirely). No single commit
silences more than one.

### A-2 — the term carries its qualifier

**39** operands denoted, **17** inside a deciding condition, **22** in no
column — counted by an independent AST walk written from `kern5f9a`'s own
sentence, and all 22 named individually. `35/15/20` and `4/2/2` by file.

The 15 sites, re-derived at `adcfb1f1` by mg-2c77's own rule and re-scored at
HEAD: **15 QUALIFIED, 0 unqualified.** The ruler was not moved — a constructed
site carrying only the hyphenated `deciding-condition` still scores
**UNQUALIFIED**.

### The confirmation is a DIFFERENCE

Re-derived from scratch, each pinned `g1` travelling with its own `lib58da`:
`3bc2cf76` → **0/0/0**, HEAD → **1/1/3** on the kernel bend. `k1_prerepair.py`
re-run unmodified prints the same two triples. Two independent derivations, one
answer.

**And the vacuity is sharper than the parent states it.** The drifted `this
repair` column resolves to `d01ff32d`, where `g1_provenance.py` is
**byte-identical to `g1_provenance.py` at HEAD** — under the drifted anchor the
column labelled *"the repair"* was not merely the same predicate as the current
one, it was the same **file**. Both drifted columns print **1/1/3** on the same
bend: one predicate asked twice. And the two drifted *sources* differ by sha,
which is why nothing complained — it was never a comparison of a file with
itself, and only that kind is visible to a sha.

---

## TWO FINDINGS

### F-1 — THE DRIFT GATE IS NOT WHERE THE ANCHOR IS USED

`ANCHOR_DRIFT` is built once at import of `libe34a` and gated in **2 of the 4**
scripts that read an anchor.

| script | anchors it reads | drift gate |
|---|---|---|
| `k1_prerepair.py` | `REPAIR_REV`, `PRE_REV`, `PRE_7E58_REV` | yes |
| `selftest_e34a.py` | `REPAIR_REV`, `PRE_REV`, `PRE_7E58_REV` | yes |
| `k2_five.py` | `PRE_7E58_REV` | **NO** |
| `k4_cancel.py` | `REPAIR_REV` | **NO** |

`k4_cancel.py` is **the script the repair itself identifies as the one "where
the count actually moved"** — where `REPAIR_REV` selects which commit message
is scanned, and where the drifted anchor made k4 print `d01ff32d : no` against
its own transcript's `4755d029 : yes`. It does not carry the gate. Run alone,
either script would print a number derived from a drifted anchor with nothing
to say so. The repair made drift loud in the two places that check the anchor
and silent in the two places that spend it.

### F-2 — `every one a record` IS TWO POPULATIONS UNDER ONE WORD

`dfa263c`'s summary: *"20 sites remain unqualified in the tree, every one a
record, named individually in r3 (iv)."*

Re-derived at HEAD by the same rule, excluding this audit's own files: **exactly
20.** This audit found **no site the repair did not name**, and the decision to
decline them is right — rewriting another ticket's record to make this ticket's
count come out is the failure this arc exists to avoid.

But `r3 (iii)` derives a site's **kind** from its **path** — `out_*.txt` is a
transcript, `PREDICTIONS.md` is a record, **anything else is a live claim** —
and that is the rule that decides whether a site gets edited. `r3 (iv)` then
labels the same residue by **scope** (whose ticket owns the file), and the
summary sentence reports the scope label as the kind label. Under the repair's
own path rule, of those 20:

- transcripts and prediction files: **5**
- **LIVE CLAIMS** — source and prose: **15**

A reader who applies `r3 (iii)`'s rule to `r3 (iv)`'s list gets 15 live claims
where the sentence says 0.

**That is A-2's own shape — one word over two populations — in the sentence
summarising the repair of a word over two populations.**

---

## THE POPULATION OF HISTORY-DERIVED ANCHORS, FINALLY ENUMERATED

The brief: *the population of history-derived anchors has still never been
enumerated.* It is now, repo-wide, by `ast` over every `.py` under `code/` —
**36** revision-producing `git log` call sites, classified by **how** the
revision is obtained:

| kind | sites | |
|---|---|---|
| `NEWEST` (`log -1 … -- <path>`) | **7** | HISTORY-DERIVED — the A-1 defect class |
| `INDEXED` (`log … -- <path>` then `[n]`) | **8** | HISTORY-DERIVED — A-1's second half |
| `UNRESTRICTED` (no pathspec) | **1** | HISTORY-DERIVED, on the branch |
| `OLDEST` (`log --reverse` then `[0]`) | 10 | **stable** against later edits |
| `PICKAXE` (`log -S` / `log -G`) | 6 | PROPERTY-DERIVED |
| `RANGE` (`log <a>..<b>`) | 4 | a set, not an anchor |

Plus **16 call sites of the two named helpers** (`last_touching`,
`nth_touching`), which contain no `--format=%H` at all — a flag-grep would miss
exactly the construct the repair is about.

**16 history-derived call sites across 13 directories.** The two the repair
named are two of them. `OLDEST` is named separately on purpose: a file's
*creation* does not move when the file is edited, and lumping it in would count
a safe construct as the defect — which is A-2's mistake, inside an audit of
A-2.

The repair's own enumeration ("11 anchors, 3 on a property, 6 pinned-and-
derived, 2 on a file's history") is scoped to `code/repair_8d5e/`, which its
transcript states plainly. It is not this population, and the difference is
printed rather than inferred.

`code/repair_69d1/p3_reason.py (i-b)` — the one the repair points at and
declines to fix, an anchor on `HEAD`, vacuous since mg-69d1's own repair landed
— confirmed still red: its committed transcript ends `TOTAL BAD: 1`.

---

## `LAST_TOUCHING_G1` — A DETECTOR, DEMONSTRATED

Checked by **deleting both names in a clone and re-running**, not by reading:
**2** scripts read them, **no anchor derives from either**, deletion makes the
consumers raise (exit 1), and **2** selftest assertions are stated in terms of
them — that the property anchor and the history anchor still return different
commits, and that the second history anchor had moved too. `used by no anchor`
is true; `used by nothing` is false. What removal would lose is a detector, and
it would lose it loudly.

---

## PRESERVED — ALL FOUR, AT THEIR PUBLISHED VALUES

`q1_reason.py` and `q2_bound_edge.py` re-run unmodified, both **exit 0**:

- **The fourth input that is neither case** — `one-sided`, a kern-alone bend:
  `IDENTICAL / MOVED / MOVED`, caught at **2 of 3** rows. Present.
- **The second conspiring pair of a different shape** — `conspiring-B`
  (`EXTRA_VERTEX_2C77 = True`, a **boolean** default adding an absent vertex)
  against `conspiring-A` (`DIM_SHIFT_69D1 = 1`, an **integer** default shifting
  a value). Both bodies read by `ast`; genuinely different constructions.
- **The edge probe** — unperturbed **11**; inside all three clauses **12**
  (`swept`); and **11, 11, 11** outside, filing in `not swept: nested`, **NO
  COLUMN**, and `not swept: file` respectively.
- **`AND NOTHING ELSE`** — **11 of 11** sweep rows applied, **0** removed an
  operand from outside.
- **`kern5f9a.py`** — the one file the repair touched that all four rest on.
  Text sha differs; **parsed module IDENTICAL** before `dfa263c`, after it, and
  at HEAD. 3847 AST nodes unchanged. The edit is a comment, checked at the
  grain of the program rather than the grain of the text.

**mg-8d5e's own `PREDICTIONS.md`** was introduced at `e2577e5`, at which
**0 of 6** scripts of its instrument existed, and it records **4 misses** with
what was wrong beside each. Both claims hold.

---

## FIVE DEFECTS OF THIS INSTRUMENT, RECORDED RATHER THAN SMOOTHED AWAY

1. The selftest expected **6** operands on a constructed module and the walk
   returned **8** — I listed four BoolOp *pairs* and wrote the count of pairs.
   Red on my own arithmetic before any number rested on it.
2. The anchor classifier tested for `-S` and **not `-G`**, filing a real
   `git log -G` site under the defect class and **inflating the defect
   population by one** — A-2's mistake inside an audit of A-2. Found by reading
   the sweep's own named rows, which is why the rows are named.
3. `s3`'s "each pinned source must differ from HEAD" guard was applied to every
   column and booked a SELF-ERROR against the drifted `the repair` column,
   whose whole point is that it *is* the current predicate. The instrument
   scored a fact as a fault — and the fact was worth more than the guard: it is
   the byte-identity result above, now printed as evidence.
4. `s5`'s conspiring-shape check printed `not found by this reader` where a
   gate wanted yes/no. A reader that answers "I don't know" is not a reader
   that answers "no", and printing the first where a gate wants the second is
   how a check becomes decoration.
5. `s5`'s edge probe asked only whether the substrings `11` and `12` occurred
   **anywhere** in q2's output. q2 prints dozens of numbers and two of them are
   two digits — **a gate whose red is unreachable**, which is the same defect
   as a comparison of a predicate with itself, committed in the audit whose
   subject is that defect.

---

## THE MISSES, KEPT AS WRITTEN

| row | predicted | actual | what was wrong |
|---|---|---|---|
| **P-1d** | 2–4 history-derived sites outside `libe34a` | **15**, across 13 directories | I reasoned from the two the repair named. The class is not rare; it is this repo's default way of asking "when did this file change". The prediction was itself an anchor on a sample of two. |
| **P-4c** | 0 unqualified live claims at HEAD | **15** | I predicted from the repair's summary *sentence* rather than from its *rule*. That is exactly the reading error F-2 names — made before I found it. |
| **q3** | exit 0 | **exit 1**, 2 findings | The repair only claimed q3's **census** finding, and that one is gone. I assumed the other two went with it. A miss on my side, not a defect in the repair. |
| **s4** | exit 0 | **exit 1** | Follows from P-4c. |

**One disclosure, made before any measurement.** `k1_prerepair.py` was launched
**before** `PREDICTIONS.md` was written, because it takes ~10 minutes and I did
not want it on the critical path. Its transcript was not read at the time of
writing, so P-K1 (exit 1 — HIT) is honest, but the *ordering* is not clean.
Booked rather than smoothed: pretending otherwise would be the exact failure
this arc exists to catch.

---

## THE MECHANISM

The parent's sentence was *"a figure that survives a change to what it is about
has stopped being about it."* The two findings here are the same sentence in
two other materials.

**F-1** is a gate that is loud where the anchor is *checked* and silent where
it is *spent*. **F-2** is one word carrying a rule in one section and a
different rule in another, so that a true summary and a true table say opposite
things about the same 20 sites.

Both are the shape the repair fixed, one level out from where it fixed it — not
because the repair was careless, but because a name that keeps its meaning only
inside the section that defines it is a name that has already started to drift.

Full record: `code/audit_330a/README.md` and the five transcripts beside it.
