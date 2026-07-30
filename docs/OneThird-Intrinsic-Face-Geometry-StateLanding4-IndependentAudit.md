# Independent audit — mg-7d5a / `d5a3043` (the strike of the A5 widening's own argument)

**Auditor:** mg-e720, independent. **Date:** 2026-07-30.
**Object under audit:** the diff of `d5a3043` — `STATE.md` (Appendix A, two paragraphs edited and
three added), `code/face_geometry/controls.py` (+83/−11), `controls_output.txt`,
`code/face_geometry_audit_6653/run_all.sh` (+21), `code/face_geometry_landing_7d5a/` (new, 4 files),
`docs/OneThird-Intrinsic-Face-Geometry-Probe.md` (+20/−7) — and the commit message, which this arc
treats as part of the deliverable.
**Instruments:** `code/face_geometry_audit_e720/` — `verify_landing_claims.py` → `out_verify.txt`
(26 scored statements), `attack_artifact_check.py` → `out_attack.txt` (8 attack routes).
Both regenerate byte-identically at any commit, not only at this one; see `run_all.sh`.
**`STATE.md` was NOT edited by this audit.**

---

## VERDICT: **OVERSTATED — 3 BROKEN sentences, all in material added beyond the brief**

**The repair itself is right, and it is the strongest landing in this arc so far.** The false
sentence is gone. Every number in the commit reproduced from a disjoint rebuild — twenty of twenty-six
scored statements REPRODUCED, including all four refutations, the whole `38/38` population with its
class tallies, every byte count of row 135, and every changelog clause against the diff it describes.
The code repair to `artifact_banner_check` holds against attacks I rebuilt independently at new
injection sites. **The `38/38` claim carries a stated, executable method for the first time in three
generations, and its numbers are exact.**

**And the defects are exactly where the ticket predicted: outside the seven items, in sentences about
the landing's own method.** Six findings. Three are BROKEN — false as written, load-bearing, and
checkable in one command each — and all three are in text nobody asked for:

| | finding | where | class |
|---|---|---|---|
| **F1** | `STATE.md` now carries two mutually contradictory accounts of why `f6756c0` was audited, ten lines apart, and the false one is repeated twice | `STATE.md:343`, `:351` vs `:341` | **BROKEN** |
| **F2** | the A7 re-sizing narrows the audit stage **below** the standing rule set — the word *"only"* removes the instrument route the same section says is never exempt | `STATE.md:351` | **BROKEN** |
| **F3** | the STATUS block written into mg-6653's `run_all.sh` says that audit's *"FINDINGS are unaffected"*; running it at this commit flips two scored rows to REFUTED, **because of this landing's own edit** | `code/face_geometry_audit_6653/run_all.sh:22-23` | **BROKEN** |
| **F4** | the repaired control's printed heading and docstring claim a property the code does not enforce; **four constructible routes** put the banner into the artifact with the control reporting `offending lines: none` and the battery exiting 0 | `controls.py:67`, `:1117`, `:1122`, `controls_output.txt:61` | **MAJOR** |
| **F5** | the new LIVE class contains a **code comment**, which the A5 exclusion list in the same file explicitly excludes; the membership is inherited from mg-f2e1's list, in the paragraph whose point is that the class replaces the list | `STATE.md:276` | **MODERATE** |
| **F6** | *"the commit that repaired it says the repair «changes behaviour»"* — the repairing commit is `db08b4c`; the commit that said it is `ba3ec79`, one generation later | `STATE.md:339` | **MINOR** |

**A RED verdict here is not a failure of the landing. It is the fifth-generation rule working on the
sixth generation.** `mg-f2e1` landed *"the defects land in what a landing added beyond its brief, in
sentences about its own method"*; that rule has now predicted its own violation three times running,
and this is the third.

---

## TARGET 0 — what did it add that nobody asked for?

The brief is H0–H7. Diffing the commit's output against those seven items, six things sit outside them:

| # | beyond-brief addition | size | finding? |
|---|---|---|---|
| **B1** | a **new OPEN finding filed into `STATE.md`** — *"AND THE CORRECTED FACT RELOCATES A HOLE RATHER THAN CLOSING ONE"* (`:343`) | 1 paragraph | **F1** |
| **B2** | a **+21-line STATUS block written into mg-6653's own `run_all.sh`** | 21 lines | **F3** |
| **B3** | the A7 sizing's *justification* clause — *"exempt by the narrowing test two paragraphs up, audited only because it added new mathematical content"* (H7 asked for the sizing, not this) | 1 clause | **F1, F2** |
| **B4** | rewording the control's **printed section heading** (H2 asked for the docstring or the code, not the artifact text) | 1 line | **F4** |
| **B5** | the A3 **re-framing from an enumeration to a class** (H3 asked for a re-enumeration with its method) | 1 paragraph | **F5** |
| **B6** | a new 484-line instrument, `code/face_geometry_landing_7d5a/verify_landing.py`, + harness + 2 transcripts | 4 files | clean |
| **B7** | the second changelog correction, the `(§11)` precision — mg-6653 *"recorded this and did not file it"* | 1 clause | clean, and correct |

**Five of the six findings are in B1–B5. B6 and B7 are clean.** The one finding not in beyond-brief
material, F6, is in a sentence about the landing's own sourcing. **The primary target was the right
target.**

One thing deserves credit under this heading, because it is the opposite of the arc's habit: the
commit has a **`NOT DONE, DELIBERATELY`** section naming a cheap fix it declined (mg-6653's
observation that the exclusion list mixes artifact classes with change classes), with the reason —
*"this arc's own rule is that the defects land in what a landing added beyond its brief."* It named
the rule and then broke it three paragraphs earlier. That is not hypocrisy; it is the measurement.

---

## 1 — did it strike the argument without weakening the rule? **Struck: YES. Weakened: YES, but not where the ticket looked.**

### The strike is complete and every refutation reproduces

Verified from git myself, not taken from the ticket or from mg-6653
(`out_verify.txt`, TARGET 1 — 7 of 7 REPRODUCED):

- **`c50ce32`** — `1 file changed, STATE.md, 13 insertions(+), 5 deletions(-)`. **Exactly as claimed.**
  The A5 widening's replacement evidence is TRUE, and the widening survives on it.
- **`f6756c0`** — 4 files: `code/hodge_leverage/run_all.sh`, `run_sweep.py`, `sweep_output.txt`,
  `docs/OneThird-Hodge-Side-Leverage.md`. **No `STATE.md`. Three instruments.** So the pre-existing
  instrument clause fired on it, and the struck sentence's *"the file that no trigger watched"* is
  false. **Confirmed independently, as instructed.**
- **The row is at `docs/OneThird-Hodge-Side-Leverage.md:877`** as `f6756c0` left it — that document's
  own ledger row, `PROVEN`, *"free from **G** + Theorem **L**"*.
- **`git log -S 'G″' -- STATE.md`** returns exactly `ba3ec79` and `1e61031`. **And I ran the stronger
  test mg-7d5a did not:** `git log -G` on the row's *own wording*
  (`one of whose blocks induces an antichain`) over `STATE.md` returns **only `1e61031`** — mg-a2bd's
  strike record. The row's text has never entered `STATE.md` except inside the record of its striking.
  The claim survives the sharper form of its own test.
- **`mg-d39d` (`522048f`)** says, verbatim: *"Blast radius is two lines and `STATE.md` is clean."*
- **The `NOT INHERITED` call is right.** `c0cf104`'s `STATE.md` hunk is 8 added lines and carries
  **both** defects (the Lemma-1 `n ≤ 6` overstatement and the `SIX for six` 4d contradiction);
  `c50ce32`'s hunk carries **neither**. mg-f2e1's ticket said otherwise; declining to inherit it was
  correct, and the landing does not reintroduce it.

### The rule still covers `STATE.md`-only commits

Textually verified identical across `d5a3043^ → d5a3043`: the instrument trigger, the `STATE.md`
clause, **THE HOLE** and the narrowing test. **A commit that touches only `STATE.md` still earns the
stage.** H0 holds on the load-bearing text and the ticket's first worry does not materialise.

### But the exclusion list *was* narrowed, and below what is true — **F2**

`STATE.md:351`, as landed:

> **Deliverable documents are inside the stage when they are WRITTEN, and a repair to one re-enters it
> **only** if the repair widens or adds new mathematical content.**

`STATE.md:355`, unchanged, in the same section:

> **The narrowing test above is about mathematical CLAIMS and does not exempt instruments: adopting a
> control, rescoring a row, or rewording what a control prints is not a narrowing.**

A repair commit to a deliverable that touches an instrument therefore re-enters the stage **by the
instrument clause**, whether or not it adds mathematics. `f6756c0` — the commit the new sentence
offers as its counterexample — is precisely that case, and **this commit proved it four paragraphs
above.** The word *"only"* deletes a route the rule set keeps.

**This is the ticket's item 6 in its second direction and it is worse than cosmetic**, because the
narrowed clause is what a future reader will apply. mg-6653 wrote the weaker and defensible form
(*"It was audited because it added new mathematical content, **not because** deliverable documents are
already inside the stage"* — a contrast with one clause, not a universal). mg-7d5a **strengthened an
inherited claim into a universal** while sizing down an over-wide one. A landing that removes an
over-wide claim and installs a differently-over-wide one in the same sentence has not sized it.

**Also inherited with it:** *"exempt by the narrowing test two paragraphs up."* The narrowing test is
at `STATE.md:309`; two paragraphs above `:351` is **THE HOLE**, which only refers to it. mg-6653 said
*"two paragraphs earlier"* and it was wrong there too.

### And the same false premise is repeated in the OPEN finding it filed — **F1**

Three sentences from one commit, ten lines apart in one file:

| line | text | status |
|---|---|---|
| **341** | *"`f6756c0` … **does** touch `run_all.sh`, `run_sweep.py` and `sweep_output.txt` … so **the PRE-EXISTING clause already fired** on the commit that carried the arc's only BROKEN item"* | **TRUE** — the commit's own headline refutation, measured by its own T1, and by me |
| **343** | *"mg-d39d caught it, but as a landing audit under the narrowing test's *new mathematical content* branch, **not because of any artifact clause**."* | **FALSE** |
| **351** | *"`f6756c0` … **audited only because** it added new mathematical content"* | **FALSE** |

The instrument clause **is** an artifact clause — the same section closes with *"**Two artifact
classes trigger** — instruments, and the state-of-the-program summary."* Lines 343 and 351 are
refuted by line 341.

`:343` is the paragraph this landing **filed as a new OPEN finding for pm-onethird**, beyond its
brief. Its abstract claim is true and worth filing: *the widened clause names one file, and a
deliverable document's own ledger row passes the widening's own reader-consults-this-instead-of-the-
source test.* **The evidence it offers for that claim is not.** It nominates `f6756c0` — and
`f6756c0` is a commit the rule already fires on, which is **the exact ground on which this commit
struck mg-f2e1's sentence.** Generation five argued for a widening using the one commit the widening
was not needed for; generation six argues for a relocated hole using the one commit whose coverage it
had just proved.

Both false clauses are **lifted verbatim or strengthened from mg-6653** (`StateLanding3`, lines 93-94
and 296-297), in a commit whose second paragraph reads *"nothing is inherited from mg-6653, from
mg-f2e1, or from the ticket."* mg-6653 itself contradicts itself on this — its recommendation 1 calls
`f6756c0` *"a commit the instrument clause already covered."* **mg-7d5a re-measured the true half into
T1 and adopted the false half into prose.** That is mg-f1b2's finding at mg-8a12 — *the routing was
adopted from the auditor instead of measured* — at a new location, sixth generation.

**Blast radius.** Three sentences in `STATE.md`. Nothing mathematical. The A5 rule's **conclusion**
survives on `c50ce32` and `c0cf104` and needs none of it; the newly-filed OPEN finding survives on its
abstract form. What must not be relayed is *"no artifact clause covered the commit that carried the
arc's only BROKEN item"* — the same file proves the opposite.

---

## 2 — the new control: **can you still construct the false positive? NO by mg-6653's routes; YES by four others.**

Rebuilt independently in `attack_artifact_check.py`, from the repaired docstring's claim rather than
from mg-6653's script. **Every injection site below is a different function from the one mg-6653 used.**

### The code repair holds where it was broken — this is real and it is verified

| route | result |
|---|---|
| **A** — the banner in a row NAME (the pre-repair route) | control `[FAIL]`, exit 1 → **not a tautology; correctly stays a scored row, not `[CANNOT FAIL]`** |
| **B** — the banner in a `detail=` string, injected in the **incidence battery** (mg-6653 used `scoring_self_test`) | control `[FAIL]`, exit 1 → **repelled** |
| **C** — the banner as a bare `print()` heading, injected in **`positive_control_homology`**, so it lands at the top of the artifact (mg-6653 used a mid-file heading) | control `[FAIL]`, exit 1 → **repelled** |
| **D** — one artifact line assembled from **two `write()` calls**, so the literal never appears in a single write | control `[FAIL]`, exit 1 → **repelled**; the tee's reassembly is correct |

**mg-6653's ATTACKS B and C really are dead, and not by accident of where they were injected.** The
`ArtifactTee` is the right mechanism, and the repair chose the strong option (scan the stream) over
the one mg-6653 offered (*"scan `detail` strings and headings too; ATTACK B is four lines"*). Credit
also for a detail nobody had to do: the check's name retains the substring *"no control row's own text
contains"*, which is what mg-6653's unmodified detector greps for — so **the repair kept the
auditor's instrument able to score it.** As a cross-check I re-ran that script: byte-identical to the
committed `out_attack_banner_after_repair.txt`.

### But four routes reach the artifact unopposed — **F4**

| route | banner in artifact? | control row | exit |
|---|---|---|---|
| **P1** — a bare `print()` **after** the check, above the bottom line | **yes**, line 62 | `[PASS] … offending lines: none` | **0** |
| **P2** — a **new control row appended after the check** (mg-1319's F5 row name verbatim) | **yes**, line 63 | `[PASS] … offending lines: none` | **0** |
| **P3** — `os.write(1, …)`, into the artifact around the tee | **yes**, line 1 | `[PASS] … offending lines: none` | **0** |
| **P6** — a **module-level `print()`**, before `main()` installs the tee | **yes**, line 1 | `[PASS] … offending lines: none` | **0** |

**Three of the four are a bare `print()`.** The commit message says the check now reads *"what a grep
of `controls_output.txt` reads, whatever route printed it — **including a bare `print()` added
tomorrow**."* P1 is a bare `print()` added tomorrow, four lines below the check.

The property actually enforced is: **no line printed *before this row*, through `sys.stdout`, after
`main()` installed the tee, carries the 17-char literal.** Three claims are written around it, in
ascending over-statement:

- `ArtifactTee.__doc__`: *"what this object records **IS** the artifact"* — refuted by **P3** and
  **P6**; stated as an identity, and it is not one.
- the docstring: *"It now scans every line `ArtifactTee` has recorded, **which is every line of the
  artifact**"* — refuted by **P1/P2**, and **contradicted by the very next paragraph of the same
  docstring**, which says *"(a) It reads the lines written BEFORE it runs."*
- the docstring again, and this is the load-bearing one: *"so «the artifact's occurrences of the
  banner are exactly the bottom line's» is now the property **enforced** rather than the property
  **claimed**."* That composite property holds **only while this row stays last in `main()`**, and
  nothing pins it there. **mg-6653's finding was "the docstring claims more than the code enforces."
  The repair strengthened the code and then wrote a new docstring sentence that claims more than the
  code enforces.**
- the **printed heading**, which is the text an instrument prints and therefore an A5 object in its
  own right: *"CONTROL ON THE ARTIFACT -- **nothing above the bottom line may carry the banner**."*
  P1 and P2 are above the bottom line and carry the banner.

**The one place it is said correctly is the check's own detail string** — *"lines scanned: 61 (**the
whole artifact above this row**; 40 row names among them)"*. That is exact. The heading above it, the
docstring above that, and the commit message above that each widen it by one notch. **The instrument
is honest and its labels are not.**

**Not scored as a defect, correctly disclosed:** *"(b) it scans the exact 17-character literal,
case-sensitive"* (mg-6653's ATTACK D boundary) and *"(c) it says nothing about … text a caller appends
to `controls_output.txt` outside the `tee`."* Both true, both named. The repair also correctly keeps
the row **scored** rather than `[CANNOT FAIL]`, per the standing rule — A, B, C and D all make it
fail, so it covers something. **That judgement is right and I could not overturn it.**

---

## 3 — the enumeration: **CONFIRMED, exactly, and the method is real**

I counted from the tree myself. **My population, and my method, stated first:**

> Every path in `git ls-tree -r d5a3043`; each blob decoded as UTF-8, with anything that fails to
> decode **reported rather than silently skipped**; occurrences of the literal `38/38` counted, not
> lines; occurrences grouped into sites by enclosing blank-line-delimited paragraph. **No exclusions**
> — this instrument's files are not in the commit under audit, so it has nothing to exclude.

**Result at `d5a3043`: 54 occurrences, 13 files, 38 sites.**

mg-7d5a reports **50 / 12 / 35** and declares exactly one exclusion by name and in its own output —
its own transcript `code/face_geometry_landing_7d5a/out_verify.txt`, at 4 occurrences and 3 sites,
*"because a scanner that counts its own output cannot regenerate byte-identically."*

**54 − 4 = 50. 13 − 1 = 12. 38 − 3 = 35. All three numbers are exact on independently-written code.**

The three class tallies reproduce too, each one exactly:

| class | mine | mg-7d5a's paragraph |
|---|---|---|
| LIVE | 3 files, 16 occ, 7 sites | 3 / 16 / 7 |
| FROZEN AUDIT | 4 files, 20 occ, 18 sites | 4 / 20 / 18 |
| INSTRUMENT | 5 files, 14 occ, 10 sites | 5 / 14 / 10 |

And the class statement itself — *"every remaining occurrence is inside a frozen independent-audit
document or inside an audit/landing instrument's own source or transcript"* — is **TRUE**: no file
falls outside the three classes. **Every site in the three LIVE files names the truncation**, checked
paragraph by paragraph.

**Tried to break the population and could not:** no tracked blob fails to decode as UTF-8, so the
skip step drops nothing; and of the three `.gitignore`'d files in the worktree (two `.pyc`, one
settings file) **none** carries the literal, so excluding ignored files loses nothing at this commit.

**This is the first stated method in three generations of this claim, and it is the reason I could
check it in one run instead of arguing about it.** Two generations replaced a false coverage claim
with another false one; this one replaced it with a class boundary, a population, and an instrument
that reprints both on demand. **H3 is discharged.**

### One defect in the class, and it is about the method — **F5**

The stated boundary is the A5 test: *"the artifacts a reader consults INSTEAD OF the source, **which is
this rule's own test**."* The A5 exclusion list, in the same file and the same section, says:

> *"A README, **a code comment**, a path correction, a typo fix, a commit-message reword, a
> `.gitignore` line and the frozen independent-audit documents do **not**: nobody retires a question on
> their authority."*

`code/face_geometry_audit_5630/audit_x3_equivalence.py:84` **is a code comment**, and it is in the
LIVE class. It is there because **mg-f2e1's member list had it** (*"One instrument comment …
audit_x3_equivalence.py:84 … correct as written"*) — i.e. **inherited**, in the paragraph whose entire
argument is that a class replaces an inherited list, in a commit that says nothing is inherited.

Direction: **conservative.** Including it makes *"every LIVE site is flagged"* a stronger claim, and
the site does disclose the truncation (weakly — its comment says *"the audit's OWN population"*; the
`[:20]` that makes it a truncation is in the code three lines below). So no number is wrong and no
reader is misled. What is wrong is that the boundary is not being applied as stated: on the stated
test, LIVE is **2 files / 15 occurrences / 6 sites**. A class that is derived from the previous
member list rather than from its own boundary has not replaced the list.

---

## 4 — the changelog lines: **every clause checks out. H4 is discharged.**

`d5a3043` has **one** hunk in the Probe, in the §-head changelog. Every clause it adds or edits,
against the diff it describes:

| clause | verdict |
|---|---|
| the old wording was *"the per-site enumeration in §5 and in `STATE.md` Appendix A"* | **REPRODUCED** — verbatim at `ba3ec79:41-44` |
| **§5 is not touched by `ba3ec79` at all**; its three hunks in this file are the §-head changelog, §2 and §12 | **REPRODUCED** — post-image hunks `(34-48)`, `(142-158)`, `(810-822)`; §2 = 109-158, §5 = **348-474 (untouched)**, §11 = 707-788 (untouched), §12 = 789-823 |
| §5 carries the truncation **FLAG**, not an enumeration, and mg-1319 landed it | **REPRODUCED** — §5 has *"Flagged because `38/38` is quoted as a headline … a `[:20]` TRUNCATION"* and no site list; `git log -S` on that flag returns `db08b4c` |
| the §2 clause stands | **REPRODUCED** — §2 is in a hunk, and it is the sentence the document labels `(F3, …)` |
| the §12 clause stands | **REPRODUCED** — §12 is in a hunk, both the reversal preamble and the second marker |
| *"claimed the correction outright"* was imprecise: **the replaced entry did carry `(§11)`** | **REPRODUCED** — `ba3ec79^` reads *"corrected to `n ≤ 5` for Lemma 1 (§11)"* |
| *"Both are fixed above"*, and *"the `STATE.md` claim is now a class statement"* | **REPRODUCED** — the first is in this hunk, the second in this commit's `STATE.md` hunk |

**Nothing the block asserts is absent from the diff.** This is the mechanical check that has caught
something in every previous generation, and this generation is the first to pass it. Worth stating
plainly, because the ticket expected otherwise.

The second correction — the `(§11)` precision, which mg-6653 recorded and declined to file — is
**correct**, and taking it while the line was open is the right call.

---

## 5 — the measurement: **CONFIRMED. Metric named. Reproduces to the byte.**

**My metric, stated because the ticket is right that two different byte counts of this row have now
appeared in this arc:** the number of **UTF-8 bytes in the single `STATE.md` line containing
`THE PIPELINE SURVIVED THE CONTROL IT WAS MISSING`, newline excluded.** The row is located by that
marker, **not by line number**, so the measurement does not depend on line numbers holding still.
(They do hold: the row is line 135 at all five revisions below.)

| revision | bytes | chars | |
|---|---:|---:|---|
| `c0cf104` (mg-78c0) | **7,832** | 7,702 | mg-f7bc's F7 baseline |
| `db08b4c` (mg-1319) | **11,727** | 11,544 | F7 measured the growth to here — **+49.7 %** |
| `de54c3a` | 12,455 | 12,252 | parent of `ba3ec79` |
| `ba3ec79` (mg-f2e1) | **14,582** | 14,340 | the commit under repair |
| `d5a3043` (mg-7d5a) | **14,582** | 14,340 | **row untouched by this landing** |

- **F7's `7,832 → 11,727` reproduces exactly**, so the metric mg-7d5a says it used is the metric
  mg-f7bc used.
- `de54c3a → ba3ec79` = **+2,127 bytes (+17.08 %), +2,088 characters.** mg-7d5a reports
  *"+2,127 bytes (+17.1 %), or +2,088 characters."* **Exact, on all three figures.**
- `949 / 12,455 = 7.62 %`, which is the `+7.6 %` mg-f2e1 reported — so **the denominator was right and
  only the numerator was wrong**, exactly as mg-7d5a diagnoses. **Understated 2.24×.**
- `14,582` is **+86.2 %** on the F7 baseline, against the **49.7 %** the restructure decision cites.
  I checked the decision: `docs/roadmap.md:50-54`, *"Evidence: row 135 grew **49.7 %**
  (7,832 → 11,727 bytes)."* **The correction strengthens that decision**, and mg-7d5a's insistence
  that it not be relayed as if it might weaken it is correct.
- Rows 131-134 byte-identical `de54c3a → HEAD`: `5351 / 9228 / 13487 / 10824`. **No restructure, no
  row split.**

**H5 is fully discharged and this is the cleanest item in the commit.**

---

## 6 — over-correction, both directions

**A6 (*"the whole defect population sat in"* → *"concentrated in"*): correctly sized. No
over-correction.** The narrowing is justified — mg-5630's A4 defect was in the scoring logic — and
*"concentrated in"* is not weaker than the evidence supports: six audits returned `0 BROKEN
mathematics`, and the exception is named in the same parenthesis. **A true general claim was not
stripped here.**

**A7: over-corrected. See F2 above** — the *"only"* narrows the stage below the standing rule set.
That is this section's second direction, and it is where the correction reflex landed.

### F6 — the A6 justification misattributes its own quotation

`STATE.md:339` reads *"the commit that **repaired** it says the repair «changes behaviour»."*

- The commit that repaired mg-5630's A4 is **`db08b4c`** (mg-1319) — its message: *"the scoring defect
  fixed in `controls.py`."* Its message does **not** contain the phrase.
- The commits whose messages do are **`ba3ec79`** (mg-f2e1, reporting the repair a generation later),
  **`a85fb28`** (mg-6653's audit, which correctly wrote *"this commit's own message"*), and `d5a3043`
  itself.

**`d5a3043`'s commit message gets it right** — *"ba3ec79's own message says that repair «changes
behaviour»."* Only the sentence it wrote into `STATE.md` moves the quotation onto the repairing
commit. MINOR: the point of A6 stands entirely, and the narrowing it justifies is correct. It is
listed because attribution derivations are a tracked class in this arc and because the durable
artifact is the one that is wrong.

---

## What I tried and could NOT break

Per the ticket: a GREEN needs to be argued harder than a RED, so the GREEN parts are argued here.

1. **Eight attack routes on `artifact_banner_check`.** B/C rebuilt at different injection sites: both
   repelled. A split-write line: repelled. The positive control: still fires. **The code repair is
   sound and it is not a tautology.**
2. **The `38/38` population, three ways.** Counted from the commit rather than the tree (different
   population source from mg-7d5a's); checked every tracked blob for UTF-8 decodability (none fails);
   checked all three `.gitignore`'d worktree files (none carries the literal). **The count is exact
   and the exclusion loses nothing.**
3. **The row-135 metric.** Located the row by content rather than by line number, in case the arc's
   two conflicting byte counts came from line drift. They did not — the row is line 135 throughout,
   and both counts reproduce on the same metric. Checked characters as well as bytes: `+2,088`, also
   exact.
4. **The four refutations, in a sharper form than the commit used.** `git log -G` on the row's own
   wording, not `-S` on the row label: still only mg-a2bd's strike record. **The strike gets stronger
   under a stronger test.**
5. **Whether the rule was quietly narrowed at the load-bearing clauses.** Compared the trigger, the
   `STATE.md` clause, THE HOLE and the narrowing test across the diff: **all four textually
   identical.** The narrowing I did find is in the exclusion list (F2), not in the trigger.
6. **Regeneration, all four committed transcripts.** `controls_output.txt` regenerates
   byte-identically twice and matches the committed file; both `face_geometry_landing_7d5a` outputs
   regenerate byte-identically; and mg-6653's two outputs do **not** regenerate — which is what the
   new header says. **Working tree clean after every run.** The claim *"both landing outputs
   regenerate at this commit and will not at later ones, stated in `run_all.sh` rather than claimed
   away"* is honest and it is the right way to handle a live-tree instrument.
7. **Whether the A4 changelog block asserts anything outside its own diff** — the check that has fired
   every generation. It does not.

---

## What STANDS

- **The A5 widening. Untouched, and its evidence is now true.** `c50ce32` is a real existence proof
  and I verified it. The false sentence is gone and the rule is not.
- **`artifact_banner_check`'s code.** A byte-stream check is the right mechanism and it defeats both
  constructed false positives, from injection sites the constructor never used.
- **The `38/38` population, with a method.** 50/12/35 and 16/7/3 · 20/18/4 · 14/10/5, all exact.
- **Every changelog clause against its diff.** First generation to pass this.
- **Row 135's measurement.** `+2,127 / +17.1 % / +2,088 chars / 14,582 / +86.2 %`, all exact, and the
  direction call is right.
- **The A6 narrowing.** Correctly sized in both directions.
- **The `(§11)` correction** mg-6653 declined to file.
- **Scope discipline on the relocation**: recorded as OPEN for pm-onethird rather than acted on —
  correct, notwithstanding F1's defect in its evidence.
- **The `NOT DONE, DELIBERATELY` section.** Naming a declined fix so its absence is not mistaken for
  coverage. The discipline mg-fcf1 credited as a first, applied again.

## What must be repaired

1. **`STATE.md:343`** — strike *"not because of any artifact clause."* The OPEN finding stands on its
   abstract form (the clause names one file; a deliverable's ledger row passes the rule's own test);
   it must not stand on `f6756c0`, which line 341 proves the instrument clause caught.
2. **`STATE.md:351`** — remove *"only"*, or add the instrument route: *"…re-enters it if the repair
   widens or adds new mathematical content, and independently whenever it touches an instrument."*
   And drop *"audited only because it added new mathematical content"* — line 341 refutes it.
   Fix *"two paragraphs up"* → the line reference.
3. **`code/face_geometry_audit_6653/run_all.sh`** — *"Its FINDINGS are unaffected; only the transcript
   is"* is false as written: two scored rows flip to REFUTED at this commit because this landing moved
   the Probe's line numbers. Say which two and why, or say that the instrument's row-matching is by
   line number and has aged out.
4. **`controls.py` / `controls_output.txt`** — either pin `artifact_banner_check` last (assert nothing
   prints after it, which is three lines) or size the three claims to what the detail string already
   says correctly: *"the whole artifact above this row."* The printed heading is the urgent one; it is
   the text an instrument prints, which is an A5 object.
5. **`STATE.md:276`** — either apply the stated boundary (LIVE = 2 files / 15 / 6, moving the code
   comment to INSTRUMENT) or state the exception and why the A5 exclusion list's *"a code comment"*
   does not govern here.
6. **`STATE.md:339`** — *"the commit that repaired it"* → *"the commit that reported the repair
   (`ba3ec79`)"*.

---

*Raw verdict to pm-onethird. Not relayed to Daniel. `STATE.md` not edited.*
*Reproduce: `sh code/face_geometry_audit_e720/run_all.sh`.*
