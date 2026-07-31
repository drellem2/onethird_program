# mg-8d5e — the derived anchor, and the term that counted a smaller population than it named

**Repairs:** mg-2c77's two open sites on the mg-69d1 repair (`d01ff32`).
**Instrument:** `code/repair_8d5e/` — 5 scripts, 35 self-test assertions, worst exit 0.
`PREDICTIONS.md` committed in `f7a30d1` **before any script of this instrument existed**.

| | audit | site | one sentence |
|---|---|---|---|
| **A-1** | mg-2c77 | **OPEN 1** | a **derived anchor re-pointed when a sentence was edited**, and both sides of the pre-repair comparison became the already-repaired predicate |
| **A-2** | mg-2c77 | **OPEN 2** | a **term in a count denoted 39 operands** where the count covered **17** |

They look unrelated. They are the same failure in two materials: **a name that goes on meaning
what it used to mean while the thing it points at has moved.** §4 is about that.

---

## 1. A-1 — the anchor

### What was wrong

`libe34a` derived the subject of `k1`'s comparison instead of writing it down, and said why:

> `PRE_REV` is DERIVED, not written down. […] A literal is a claim that stops being checked the
> moment the file moves.

That reasoning is right and it is not withdrawn. But the derivation was **the last commit that
touched `g1_provenance.py`**, and mg-69d1 touched `g1_provenance.py` — to correct a **sentence**
about which case the `both together` row catches. The anchor followed the edit:

```
REPAIR_REV   4755d02  (mg-76cc's repair)      →  d01ff32  (mg-69d1's own)
PRE_REV      3bc2cf76 (its parent)            →  e5787e11
```

Both sides of the comparison became mg-76cc's **already-repaired** predicate, differing only in the
prose mg-69d1 edited. `k1` went on printing **0 backwards at the exit grain, 0 at the finding
grain, 0 files named by an old finding over 7 inputs** — every number mg-e34a had booked, and every
number now about a different pair of revisions.

> **A derived anchor follows every edit to the file it derives from, including edits with nothing
> to do with the property.** A literal cannot notice that the file moved. A derivation cannot
> notice that it has started measuring something else. The second failure is the quieter one,
> because the number is identical.

### What the repair is

Each anchor is now **three things, and no two of them fail the same way**:

| | how | what it catches |
|---|---|---|
| **derived from the property** | `first_introducing(g1_provenance.py, "kernel_source=")` | the file moving, renaming, being rewritten |
| **pinned** | `REPAIR_REV_PIN`, with the reason beside it | the derivation re-pointing |
| **compared** | `ANCHOR_DRIFT`, gated in `k1 (i)` and in `selftest_e34a` | either of the above, **loudly** |

`kernel_source=` **is** mg-76cc's repair, not a description of it: the two-source signature that
makes *this script with that kernel* expressible at all, and whose absence was mg-957f's F-1. The
marker is asserted **monotone** over the file's history — once present, present in every later
commit — because a marker that came and went would make *first introducing* answer about the first
of two introductions.

**The derivation that re-pointed is kept and printed** as `LAST_TOUCHING_G1`, used by no anchor.
Deleting the quantity that moved would be the third version of the same mistake.

### Three things the audit did not have

**The defect is reproduced, not recalled.** `r1 (ii)` builds a commit that appends a comment to
`g1_provenance.py`. The file-history derivation moves to that commit; the property anchor does not.
Both outcomes are gated: a property anchor that also moved would be no repair, and a file-history
derivation that did **not** move would mean the input never exercised the defect.

**The check is made to fail, three ways.** A wrong pin, an unfindable marker, and a marker made
non-monotone — each a commit in its own clone, each scored by **mg-e34a's own selftest** rather
than by the script that built it. All three red, each naming what it found.

**Both history anchors had moved, and mg-2c77 named one.** `PRE_7E58_REV` was
`nth_touching(g1, 1)^` — an *index* into the file's history. mg-69d1's commit pushed every index
along by one, so the column `k1` labels **before mg-7e58** came to hold **mg-76cc's** parent. An
index into a history is an anchor derived from that history and re-points for exactly the same
reason.

### And a second script, which is where the count actually moved

`REPAIR_REV` is not only `k1`'s. `k4_cancel.py` uses it to select **which commit message** is
scanned for the inverted sentence under test. Under the drifted anchor:

| which message `k4` scans | revision | carries the sentence? |
|---|---|---|
| what `k4`'s **committed transcript** recorded | `4755d029` | **yes** |
| under the file-history anchor (pre-repair `HEAD`) | `d01ff32d` | **no** |
| under the property anchor (this repair) | `4755d029` | **yes** |

So the drift did not merely re-label `k1`'s columns. It **moved a population**: a copy of the
sentence under test left `k4`'s count, and nothing in `k4`'s output moved that a reader could
notice. That is the whole finding said in one row — *the figure is identical and it is about
something else*.

### The confirmation, re-derived

mg-2c77's instruction was **re-run `k1` and re-derive the kernel-half confirmation, which is
currently unsupported**. It was unsupported for a structural reason, not a bookkeeping one.

The confirmation is not a `0` in a verdict block. mg-957f's F-1 was that the kernel half of the
predicate had been **deleted**: bend `kern_a218.py` and the predicate stays silent. mg-76cc
restored it. The evidence is a **difference between two columns** on that one input:

| predicate revision | exit | self | findings | |
|---|---|---|---|---|
| before mg-7e58 — `52aeaf43` | 1 | 0 | 2 | |
| **BEFORE THIS REPAIR** — `3bc2cf76` | **0** | 0 | **0** | **silent** |
| this repair | **1** | 1 | **3** | **fires** |

With the drifted anchor both columns were the same predicate and the row read `both fire` — which
is what a comparison of a thing with itself prints whatever the truth is. `r2` gates both halves
separately, and `k1`'s own bucket for that input now reads `new fires, old silent` at both grains.

`k1` re-runs at exit **1** with **one** finding — the cancelling-pair finding that is in its
committed transcript and that mg-69d1 named as not closed. The **two** findings it booked at the
pre-repair `HEAD` — its own report of the drift — are gone, because `g1_provenance.py` and
`lib58da.py` at `3bc2cf76` are now byte-identical to `lib76cc`'s pin `e006581c`, which `k1 (i)`
checks.

---

## 2. A-2 — the term

### What was wrong

`explicit boolean operand` denotes **39** operands in `face_complex.py` and `posets.py`.
mg-69d1's table classifies the **17** that lie inside a deciding condition. **22 are in no
column** — 20 and 2, named individually.
`boolean_operands` walks only inside `deciding_conditions`, so an `and` in a `while`, in an
assignment, or in an `if` whose body assigns and breaks is outside every column.

### Fix the walk or fix the term — and why the term

mg-2c77 offers both. This ticket fixes the **term**, and the reason is stated before the
measurement:

* the **bound** sentence mg-69d1 narrowed already names *the deciding conditions*, and mg-2c77
  says so explicitly: *the narrowed BOUND sentence itself is NOT affected […] and is correct*;
* widening `boolean_operands` to walk whole modules would **not widen the sweep by one operand** —
  the sweep deletes top-level operands of deciding conditions and nothing else. It would relabel
  22 operands into a column while leaving the bound saying what it says now.

The term is the thing out of step with the bound, and the bound is the thing that was measured.

| file | operands of every `and`/`or`, anywhere | of those, inside a deciding condition | in no column |
|---|---|---|---|
| `face_complex.py` | 35 | 15 | 20 |
| `posets.py` | 4 | 2 | 2 |
| **ALL** | **39** | **17** | **22** |

Both walks are written in `lib8d5e.py` and the narrow one is asserted against the **shipped**
`kern5f9a.boolean_operands` **span for span** before any subtraction rests on it. A subtraction
whose narrow side comes from the thing under test is whatever that thing says.

`p1_bound.py` (ii) now prints **both** populations and the difference, so the subtraction is on the
page rather than in a reader's head.

### The ruler was not moved

The scoring rule is mg-2c77's, character for character: **QUALIFIED** if the words
`deciding condition` stand within 3 lines in the same file; a **quotation** if `NO FURTHER` or
`is read as` stands in the same window; otherwise the census, unqualified.

It looks for the **unhyphenated** words. `q3_operands.py`'s own lines carrying `deciding-condition`
were scored UNQUALIFIED by it. So every site repaired here carries the unhyphenated words in the
window as well as the hyphenated term in its sentence — and the self-test asserts that a site
carrying **only** the hyphen still scores UNQUALIFIED. Widening the rule to accept the hyphen
would have closed the finding by moving the ruler.

The rule is then run at `adcfb1f` — the revision where mg-2c77's table was committed — and required
to return **that table's own 15 in-`d01ff32` sites, path and line**. It does: 15 matched, 0 only
mine, 0 only its. Two rules that agree on constructed inputs can still disagree on a tree.

### What each site got — and the kind is derived, not listed

| kind (derived from the path) | treatment | why |
|---|---|---|
| a **live claim** about what the instrument covers | **edited** to carry the qualifier | it is what a reader has |
| a **transcript** (`out_*.txt`) | the source line that **prints** it is edited, and the script re-run **by its own runner** | a transcript is a measurement; hand-editing one falsifies it |
| a **record committed before its own run** (`PREDICTIONS.md`) | an **addendum in place**, the original row standing | a later ticket does not rewrite what an earlier one predicted |

**15 → 0** in files `d01ff32` touched. The shipped classifier's edit is a **comment**, measured
rather than asserted: the module is parsed before and after and the two syntax trees compared.

**20 sites remain unqualified in the tree, and every one is a record** — mg-2c77's own finding text
and transcripts, mg-eaef's instrument and write-up. Each states what that audit found at the moment
it ran. They are named individually in `r3 (iv)` and left standing: rewriting another ticket's
record to make this ticket's count come out is the failure this arc exists to avoid.

---

## 3. What this deliverable checked about itself

mg-2c77 closes by addressing whoever writes this: *check that every anchor you derive still points
where you think, and that every term you use in a count means the same thing at every site you use
it. Enumerate what you checked.* `r4` answers with measurements.

* **11 anchors enumerated** — 3 on a property, 6 pinned-and-derived, **2 on a file's history and
  declared used by nothing**. The two history ones are `libe34a`'s kept evidence.
* **All of them perturbed.** A commit appends a comment to every file they derive from —
  `libe34a.py`, `kern5f9a.py`, `lib8d5e.py` — and every anchor is re-derived in the clone.
  **0 moved.** *It does not move* is a measurement here, not a property of the week this was
  written in.
* **2 counted terms scored at every site** in this deliverable's own files: the census phrase (by
  mg-2c77's rule, so my count and its count are one measurement) and `15 site`, which must name the
  population `d01ff32` wherever it appears. **0 bare.**
* **36 changed paths, every one in a named kind**, over a population derived from git rather than
  listed.

### The one thing this repair did that it refuses to let anyone else do

`code/repair_8d5e/PREDICTIONS.md` was committed before any script existed. One row of it — the
sentence describing A-2 — was **afterwards reworded** so that it carries the unhyphenated words the
rule looks for. No predicted value was touched, and the file says so.

It is booked in `r4 (ii)` because both alternatives were worse: leaving it would have left this
deliverable asserting the census unqualified in the one file that says what it set out to do, and
editing it silently would be exactly the treatment this ticket refuses to give mg-69d1's prediction
file. **The asymmetry is real and it is disclosed rather than smoothed** — that is the
finding-shaped part of this deliverable, and it is here rather than left for the next audit to
find.

---

## 4. The mechanism, which is the thing to carry

Both sites are the same failure in different materials.

**A-1** is a name (`PRE_REV`) that went on meaning *the predicate before the repair* while the
thing it pointed at became *the predicate after the repair*. **A-2** is a name
(`explicit boolean operand`) that went on meaning *every `and`/`or` operand* while the thing it
counted was *the operands inside a deciding condition*. In both cases every number stayed where it
was, and in both cases that is precisely why nothing complained.

> **A figure that cannot move when its subject moves is not measuring its subject.** mg-c4c8 said
> it about a declared unit; mg-6cb9 said it about a census anchor; this ticket says it about a
> revision and about a word.

The defence is the same in both materials and it is not a technique, it is a habit: **state the
population beside the figure, and check the two against each other.** An anchor states its
population by being pinned as well as derived, and gating the disagreement. A term states its
population by carrying its qualifier at every site, and by printing the wider figure beside the
narrower one so the subtraction is on the page.

And the tell is the same in both: **the number did not move.** mg-2c77 found A-1 because 0/0/0 was
suspiciously stable across a commit that changed the subject, and found A-2 because 4-of-15 and
all-of-17 were two answers to a question whose population was 39. A figure that survives a change
to what it is about has stopped being about it.

---

## 5. The auditor's own instrument, re-run unmodified — and one more of the same

`r2 (v)` runs mg-2c77's `q3_operands.py` and `q4_prerepair.py` against the repaired tree, with not
one character changed.

**`q3`'s census finding is gone.** A-2 is closed, measured by the instrument that raised it. `q3`
still books its other two findings — the `not swept: nested` deletion sentence, and `not
determined` being unreachable by any input. Those are mg-2c77's and they are **not** among the two
open sites this ticket was given; they are named individually in `r2 (v)` so that *2 remain* cannot
be read as *2 unrepaired*.

**`q4` still fires, and it is wrong now.** Its gate is

```
R.gate(pre_rev == pinned, "…PRE-REPAIR COMPARISON NO LONGER COMPARES MG-76CC's REPAIR…")
```

— a comparison of **revision identity**, where `pinned` is `lib76cc.REV_957F` = `e006581c`. The
property is **file identity**. `e006581c` and `3bc2cf76`, the true first parent of mg-76cc's repair,
are **different commits at which `g1_provenance.py` and `lib58da.py` are byte-identical** — which is
exactly what mg-e34a's own design says and what `k1 (i)` checks and passes. `r2 (v)` prints both
comparisons side by side.

The tell is in `q4`'s own message. It now reads:

> REPAIR_REV moved from **`4755d029`** (mg-76cc's repair) to **`4755d029`** (mg-69d1's own)

**A gate whose message says a value moved from a revision to itself is not measuring movement.** It
is comparing two identifiers, and the identifiers were never the property. That is a third instance
of this document's §4 — a name standing in for the thing it names — and it is in the auditing
instrument, one rung further out again.

It is mg-2c77's record and this ticket **does not edit it**: the same rule applied to every other
record here. It is measured and pointed at, so that a reader who runs `q4` and sees red knows what
they are looking at.

## 6. What is not repaired here, and is pointed at

`code/repair_69d1/p3_reason.py` (i-b) runs its discriminator **against `HEAD`**, described as *the
committed tree, where the defect is still present*, and books a self-error on finding 0 live
assertions there. `HEAD` moves on every commit, and **mg-69d1's own repair landing is what removed
the last live assertion** — so that control has been vacuous since the moment the repair it belongs
to was committed, and `code/repair_69d1/run_all.sh` has had worst exit 1 since then.

**The same shape as A-1, in a script mg-2c77 did not name.** `r1 (vi)` runs it at the revision
before this repair began and shows it **already red there** — observed, not caused. It is not
repaired, because this ticket's population is mg-2c77's two open sites and widening it would be a
decision nobody asked for. It is written down here so that it is a pointer and not a silence.
