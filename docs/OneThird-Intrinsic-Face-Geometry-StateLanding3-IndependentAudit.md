# Independent audit of `ba3ec79` (mg-f2e1) — the A5 widening

**Auditor:** mg-6653, pre-filed before mg-f2e1 committed. **Target:** `ba3ec79`, *"STATE: widen the
A5 trigger to cover STATE.md itself"*, landing the mg-f7bc audit of `db08b4c` (mg-1319).
**Instruments:** `code/face_geometry_audit_6653/` — `verify_claims.py` (mg-f2e1's claims about the
tree, the diff and the history, all re-measured from git), `attack_banner.py` (five mutations of the
control battery, run to completion, against E5). Both regenerate byte-identically; 11.6 s total.

## VERDICT: **OVERSTATED, 1 BROKEN**

The widening is **right**, and it lands where the ticket asked. Every one of the six repairs E1–E6 is
present, in place, and correct on the facts it is fixing; the no-restructure instruction was obeyed
exactly; nine of mg-f2e1's own re-measurements reproduce, including the 318-character figure to the
character. **What is BROKEN is the sentence mg-f2e1 nominates as *"the strongest available evidence"*
for the widening.** It is false in four checkable ways, it contradicts the audit it cites, and the
commit that actually carried the arc's only BROKEN item is a commit the **pre-existing** A5 clause
already covered — so the widening's headline argument does not survive, even though the widening
does.

Three further items are over-wide, and the shape this arc predicted holds for the **fifth**
consecutive generation: **two of the three worst findings are inside material mg-f2e1 added BEYOND
its brief**, and both are sentences about its own method.

| | finding | class |
|---|---|---|
| **A1** | *"row `G″` … added to `STATE.md` by the mg-a806 landing … introduced by a STATE landing, into the file that no trigger watched"* — the row was added to `docs/OneThird-Hodge-Side-Leverage.md` by `f6756c0`, a commit that touches no `STATE.md` and **does** touch a harness and an instrument's printed output, so the old clause already fired on it. mg-d39d, the cited audit, says *"STATE.md is clean."* | **BROKEN** |
| **A2** | E5's new CONTROL ON THE ARTIFACT: the F5 false positive is **constructible** with the control in place (ATTACKS B and C), while its docstring claims it *"makes the artifact's occurrences of the banner exactly the bottom line's"* | **MAJOR** |
| **A3** | E2's replacement enumeration — the fix for a false coverage claim — omits **2 of 6 files, 13 of 31 occurrences and 5 unflagged sites**, one of them mg-f7bc's own audit document | **MAJOR** |
| **A4** | E3's replacement changelog line asserts *"the per-site enumeration in §5"*; §5 contains no enumeration and **is not touched by this diff** — the exact defect E3 exists to name, in the line E3 rewrote | **MAJOR** |
| **A5** | *"row 135 grew a further 949 bytes (+7.6%)"* — measured on mg-f7bc's own metric it is **+2,127 bytes (+17.1%)**, understated 2.24× | **MODERATE** |
| **A6** | *"the whole defect population sat in ledger rows, Appendix A paragraphs, control-output text, changelogs and commit messages"* — mg-5630's A4 defect was in the **scoring logic**, and mg-f2e1's own message says its repair *"changes behaviour"* | **MINOR** |
| **A7** | *"Deliverable documents are already inside the stage"* — not true of **repair** commits to a deliverable, which the narrowing test exempts; `f6756c0` is the counterexample and it is the A1 commit | **MINOR** |

---

## A1 (BROKEN) — the widening's load-bearing evidence is false, and the audit it cites says so

`STATE.md` Appendix A, in the block this commit inserts, and again in the commit message:

> **And then the arc's FIRST BROKEN item arrived and it was a LEDGER ROW: mg-d39d's A1 — row `G″`,
> labelled `PROVEN`, FALSE on 55 (poset, level) pairs at `n ≤ 6` … — added to `STATE.md` by the
> mg-a806 landing, beyond its brief, and struck by mg-a2bd.** So **the strongest available evidence
> for this widening** … is that the one piece of broken mathematics the arc has produced **was
> introduced by a STATE landing, in a row nobody had asked for, into the file that no trigger
> watched.** … A trigger aimed at the artifact that PRODUCES the numbers and not at the artifact that
> DESCRIBES them **was pointed at the component with the clean record.**

Four independent refutations, each one line of git:

1. **The row was never in `STATE.md`.** `git log -S'G″' -- STATE.md` returns exactly two commits:
   `1e61031` (mg-a2bd's *strike record*) and `ba3ec79` (this commit, quoting it). No commit ever
   added the row to `STATE.md`. It was added by **`f6756c0`** to
   **`docs/OneThird-Hodge-Side-Leverage.md`**, as that document's own ledger row — `PROVEN`, *"free
   from **G** + Theorem **L**"*.
2. **`f6756c0` does not touch `STATE.md` at all.** Its four files are
   `code/hodge_leverage/run_all.sh`, `code/hodge_leverage/run_sweep.py`,
   `code/hodge_leverage/sweep_output.txt`, `docs/OneThird-Hodge-Side-Leverage.md`. mg-a806's two
   `STATE.md` commits (`16bee79`, `5b63037`) do not contain the row.
3. **It was not *"the file that no trigger watched"* — three of those four files are instruments.** A
   harness (`run_all.sh`), a sweep script, and *the text an instrument prints* (`sweep_output.txt`)
   are the trigger's own enumerated list. **The pre-existing A5 clause already fired on the commit
   that carried the arc's only BROKEN item.** Which also disposes of *"pointed at the component with
   the clean record"* on its own terms: with respect to that item, the instrument clause's record is
   not the clean one either.
4. **mg-d39d, cited as the evidence, states the opposite.** Its commit message, on the A1 finding:
   *"The false sentence is mg-86a3's step-4b aside, promoted to a PROVEN ledger row without being
   rebuilt. Blast radius is two lines and **`STATE.md` is clean**."*

**Why this is BROKEN and not MAJOR.** It is a factual statement, false, checkable in seconds, landed
permanently into `STATE.md` Appendix A as the standing rationale of a rule, and explicitly nominated
by its author as the strongest evidence for that rule. It is also the specific claim a future reader
will re-inherit — the paragraph exists *"because a rule nobody believes gets argued away"*, so the
next person to argue about A5 will argue about this sentence.

**What survives, and it matters that it does.** The **widening itself is correct and I could not
break it.** Its other two evidentiary legs both reproduce exactly:

- `c50ce32` (mg-60d3) is **1 file changed, `STATE.md`, nothing else** — the existence proof of the
  shape the trigger missed. Verified.
- `c0cf104`'s `STATE.md` hunk is **exactly eight added lines**, and both of the defects mg-1319 was
  repairing are inside them (*"closed the Lemma-1 cross-check to `n ≤ 6`, by a build that never uses
  Lemma 1"* and the *"SIX for six"* 4d contradiction). `c0cf104` also touches `controls.py`, which is
  why they were audited at all. Verified.

So the rule stands on evidence; the sentence offered as its **strongest** evidence must be struck. The
honest replacement is available and is stronger than what was written, because it does not need the
BROKEN row: **the arc's defect population is concentrated in summary artifacts, and the trigger
covered none of them.**

**And the corrected fact has a consequence the widening does not address.** The arc's only BROKEN item
landed in a **deliverable document's own ledger row** — an artifact that satisfies the widening's own
test (*"does a reader consult this artifact INSTEAD OF the source it summarises?"*) and that the
widened clause does **not** name, because the clause names one file. mg-d39d caught it, but it caught
it as a landing audit under the narrowing test's *new mathematical content* branch, not because of any
artifact clause. **The hole did not move; it was mis-located.** That is for pm-onethird, not for this
audit, and it is the reason A7 below is not cosmetic.

## Did the widened wording fire where it had to? Tested the way mg-f7bc tested the last one

The instruction was to run the **new** wording against four commits and to check the opposite failure.

| commit | item | files | `STATE.md`? | instrument? | new clause |
|---|---|---|---|---|---|
| `c0cf104` | mg-78c0 | 11 | yes | yes | **FIRES** |
| `c50ce32` | mg-60d3 | 1 | yes | no | **FIRES** — the shape that fired nothing before |
| `db08b4c` | mg-1319 | 4 | yes | yes | **FIRES** |
| `16bee79` | mg-a806 | 1 | yes | no | **FIRES** |
| `5b63037` | mg-a806 | 3 | yes | yes | **FIRES** |
| `f6756c0` | mg-a806 | 4 | **no** | yes | instrument clause only — **and this is the A1 commit** |
| `0160cbf` | mg-a806 | 1 | no | no | nothing fires — **correctly**: a narrowing of a heading to match an already-struck universal |

**The hole did not move on the shape the widening targets.** Every `STATE.md`-only landing in the arc
is now caught, `c50ce32` included, and that is what the ticket asked for.

**And it did not over-fire.** 29 of 53 commits in history touch `STATE.md` (55%); 7 of the last 25
(28%). *"Widen it"* was the instruction most likely to be over-applied and it was not: the *"WHAT THIS
DOES NOT WIDEN INTO"* paragraph gives a usable test (*does a reader consult this instead of the
source*) plus a concrete exclusion list, and 45% of the arc's commits fall outside the trigger. **This
is not a trigger that fires on everything.** One wording note, not a finding because no commit in the
arc exhibits it: the exclusion list mixes artifact classes (`README`, `.gitignore`, frozen audit
documents) with *change* classes (*a typo fix*, *a path correction*), and applied to a typo fix
**inside** a ledger row the two paragraphs give opposite answers. Cheap to fix while the block is
being edited for A1.

## A2 (MAJOR) — E5's new control: the false positive is constructible

E5 is the item whose test was *"try to construct the false positive rather than reasoning that it is
gone."* So `attack_banner.py` mutates a private copy of `controls.py`, runs the whole battery, and
reads the artifact the way a grep does. Five attacks.

**What holds, verified not assumed:**

- The artifact contains `ALL CONTROLS PASS` **zero** times. `c0cf104` had it once (line 34, the true
  bottom line); `db08b4c` had it twice (lines 4 **and** 5, both `[PASS]`-prefixed); now none. A
  case-insensitive grep returns exactly one line and it is the negation.
- **ATTACK A — the positive control on the new control holds.** Fed mg-1319's two row names verbatim,
  the control **fails**, exits **1**, reports both offenders with the banner masked as
  `<all-pass-banner>`, and does not reintroduce the string on the objecting run. It is a control, not
  a tautology, exactly as claimed.
- **ATTACK E — the A4 repair underneath it is sound.** Unguarding the `cannot_fail_rows` branch so the
  banner becomes reachable with a non-empty tally makes the **self-test's own assertion** fail and the
  run exit 1. The right instrument catches it.
- **ATTACK D fixes the scope boundary honestly:** a row name carrying the banner with a doubled space
  is not detected, and should not be — what the control buys is exactly *"no row name contains these
  17 characters."*

**What does not hold — ATTACKS B and C both succeed:**

```
ATTACK B -- the banner moved into a `detail=` string (same line, same [PASS] prefix)
  exit code                        : 0
  grep 'ALL CONTROLS PASS'         : 1 hit at line 6
       [PASS] a real failure still exits nonzero and is reported first  -- clean-run bottom line is 'ALL CONTROLS PASS'
  CONTROL ON THE ARTIFACT          : [PASS] ... rows scanned: 40; offending rows: none
  bottom line                      : ... this battery's bottom line is NOT 'all controls pass'.
  ==> ATTACK SUCCEEDS
```

That is **the F5 defect, in full, with the control in place**: the banner literal on a
`[PASS]`-prefixed line six lines from the top of `controls_output.txt`, above a bottom line explicitly
denying it, and the new control reporting `offending rows: none` and exiting 0. `detail` prints on the
**same line** as the row name behind the **same** `[PASS]` prefix, so a grep cannot distinguish them —
B is a cheaper route to the defect than the one mg-1319 took. ATTACK C reaches it via a section
heading.

**The sentence to strike** is in `artifact_banner_check`'s own docstring, and it contradicts its
predecessor two lines above:

> **Scoped exactly:** this checks the row NAMES this run printed … It does not police `detail`
> strings, the section headings, or this file's own prose — **so it makes the artifact's occurrences
> of the banner exactly the bottom line's, and claims nothing further.**

The disclaimer is right and the conclusion drawn from it is wider than it: if details and headings are
not policed, the control cannot make the artifact's occurrences *exactly* the bottom line's. This is
**output text claiming more than the code that prints it verifies** — Appendix A's fourth checkable
question — inside the control mg-f2e1 built to remove an instance of it, in a paragraph headed *"Scoped
exactly"*. Two generations of the same defect at the same site.

**One further limit, and it is the honest reading of what E5 bought.** Line 5 of the committed
artifact still reads:

```
  [PASS] with no cannot-fail row the bottom line IS the all-pass banner
```

A `[PASS]` row five lines from the top still *says* the bottom line is the all-pass banner, above a
bottom line saying it is not. The row is conditional — exactly as mg-1319's was; **the only thing that
changed is that the literal is gone.** The defect is now invisible to grep rather than absent from the
artifact. That is precisely what E5 claimed to do (*"any grep on the string became a false-positive
generator"*) and it is not more than that, so this is a scoping note and not a finding — but the
commit message's *"a string that cannot be confused with the bottom line"* is one notch wider than
what landed.

## A3 (MAJOR) — the enumeration that replaces a false universal is itself incomplete

The instruction was explicit: *enumerate every occurrence of `38/38` yourself; do not accept a count.*
There are **31** occurrences in **6** files (excluding this audit's own scanner, 5 more, named here so
its absence is not mistaken for coverage either). Grouped into **sites** — the enclosing paragraph,
which is what a reader arriving by search or quotation reads — there are **20**.

`STATE.md` Appendix A now says:

> … this is now an **ENUMERATION and not a universal**, re-derived site by site by mg-f2e1 rather than
> inherited: **five live sites, all flagged** … **One instrument comment** … **Two sites deliberately
> NOT flagged and named here so the absence is not mistaken for coverage:**
> `Probe-IndependentAudit.md:45` and `:311` …

**The live half is correct and I could not break it.** Row 135, the Appendix A paragraph, the Probe's
§-head changelog, §5 and §12 each name the `[:20]` truncation inside the paragraph that quotes the
number — §12 in two paragraphs (the reversal preamble mg-f2e1 added, and the `⟪…⟫` marker inside the
block), both flagged. `audit_x3_equivalence.py:84` reads as described, correct as written. Both named
`Probe-IndependentAudit.md` sites are indeed unflagged, as stated.

**The frozen half is not.** Two whole files are outside the enumeration:

| file | occ | sites | unflagged sites |
|---|---|---|---|
| `…-StateLanding-IndependentAudit.md` (mg-5630's audit) | 5 | 5 | **3** — `:22`, `:88`, `:259` |
| `…-StateLanding2-IndependentAudit.md` (**mg-f7bc's own audit**) | 8 | 6 | **2** — `:429`, `:559` |

The enumeration names **4 of 6 files** and accounts for **18 of 31 occurrences**. It says *"**Two**
sites deliberately NOT flagged"*; there are **seven** unflagged sites. The largest omission is
`OneThird-Intrinsic-Face-Geometry-StateLanding2-IndependentAudit.md` — **mg-f7bc's own audit document,
the document this commit is landing** — which is never named anywhere. mg-5630's audit is gestured at
(*"flags the truncation in its own §3.3 for a reader arriving from there"*, which is true: `:64` reads
*"population is 41 = 5+16+20, a `[:20]` truncation — see §3.3"*) but not enumerated, and its `:88`
(*"The audit's `out_extra.txt` X3 38/38 is a real recorded run"*) is unflagged in place.

**Every omitted site is inside a frozen audit document and every one of them discusses the truncation,
so no reader is misled about the number.** The defect is entirely in the **coverage claim** — and that
is the point. A8's universal was replaced *on the stated ground* that a coverage claim wrong once is
not evidence the second time; the replacement is a list whose stated completeness is wrong in the same
direction, at the same site, one generation on. The repair is one clause: name the class (*every
frozen independent-audit document*) instead of counting two members of it, or complete the list.

## A4 (MAJOR) — the replacement changelog asserts a fix that is not in the diff

E3's own lesson, stated twice in this commit and once in `Probe.md` itself: **a changelog is an
assertion about a diff and nothing checks it against the diff.** So I checked it against the diff.

The Probe's §-head changelog, rewritten by this commit, now ends:

> … that claim was false when written, so **the per-site enumeration in §5 and in `STATE.md` Appendix
> A** replaces it rather than being restated more confidently.

`STATE.md` Appendix A does carry an enumeration. **§5 does not.** §5 carries the truncation *flag*
mg-1319 landed — *"Flagged because `38/38` is quoted as a headline … the audit's population is a
`[:20]` TRUNCATION"* — and nothing resembling a per-site list. And **§5 is not touched by this commit
at all**: the Probe diff has exactly three hunks, `@@ -37,2 +37,9 @@`, `@@ -138,3 +145,11 @@`,
`@@ -798 +813,10 @@` — the §-head changelog, §2, and §12. This is a changelog entry asserting content
that is not in the diff, in the line E3 rewrote, in the sentence that names that exact failure mode.

**Everything else in E3 is right, and its numbers reproduce from source.** `out_n6.txt:44` is verbatim
`their Lemma 1 verified on : 87/87 (n<=5, all k)`; `out_extra.txt:2` is `404/404 posets (2<=n<=6)
PURE`. §2's corrected sentence **is** the one the document labels `(F3, repaired …)` at line 140.
mg-1319 **did** correct the same overstatement at §11 (verified in `db08b4c`'s own diff), so *"at §11
by mg-1319, and at §2 … only now by mg-f2e1"* is right about both halves. One imprecision, recorded
and not filed: the entry mg-f2e1 calls one that *"claimed the correction outright"* did carry a
location tag, `(§11)` — it misidentified the site rather than omitting one.

## A5 (MODERATE) — the one number mg-f2e1 reports about its own restraint is wrong

> OUT OF SCOPE, deliberately: audit F7 … Reported for the ticket that owns it: **row 135 grew a
> further 949 bytes (+7.6%) here** … Every claim above was re-verified against source rather than
> inherited.

Measured on the metric mg-f7bc's F7 used — line bytes, whose `7,832 → 11,727` reproduces **exactly**
at `c0cf104 → db08b4c`:

| | L131 | L132 | L133 | L134 | **L135** |
|---|---|---|---|---|---|
| `db08b4c` (mg-1319) | 5351 | 9228 | 13487 | 10824 | 11 727 |
| `de54c3a` (parent) | 5351 | 9228 | 13487 | 10824 | **12 455** |
| `ba3ec79` (mg-f2e1) | 5351 | 9228 | 13487 | 10824 | **14 582** |

**+2,127 bytes (+17.1%)**, or +2,088 characters (+17.0%) — not +949 (+7.6%). A character-level diff of
the line gives four insertions totalling 2,134 characters against 46 deleted: the E4 connective (191 +
1,111) and the E4b correction (723 + 98). The reported figure understates by **2.24×**, in the one
sentence reporting the growth of the row an audit had just flagged **for growth**, and it appears in
the list of claims *"re-verified against source rather than inherited."* Row 135 is now **86% larger
than mg-f7bc's F7 baseline** across two landings.

## A6, A7 (MINOR) — two over-wide clauses in the WHY paragraph

**A6.** *"the whole defect population sat in ledger rows, Appendix A paragraphs, control-output text,
changelogs and commit messages."* mg-5630's A4 finding was in the **scoring logic**: `db08b4c`
introduced `score()`, `summarise()` and the `CANNOT_FAIL` tally, and this commit's own message says
*"A4's scoring repair is real, **changes behaviour**, and survived nine adversarial attacks."* A defect
whose repair changes behaviour did not sit in text. The correct form is *concentrated in*, not *the
whole of*.

**A7.** *"Deliverable documents are already inside the stage."* Not true of **repair** commits to a
deliverable, which the narrowing test two paragraphs earlier explicitly exempts unless they widen or
add new mathematical content. `f6756c0` is the counterexample — and it is the commit that carried the
arc's only BROKEN item. It was audited because it added new mathematical content, not because
deliverable documents are already inside the stage. Small as a sentence; load-bearing here, because it
is the clause that makes the A1 relocation look already-handled.

## Target 6 — did it restructure anything? **No. It obeyed.**

- **Rows 131–134 byte-identical** across `de54c3a → ba3ec79`: 5351 / 9228 / 13487 / 10824. No row
  split, none re-flowed.
- **Ledger table-row count unchanged: 58 → 58.**
- `STATE.md` 350 → 362 lines. Exactly three lines edited **in place** (135, 276, 282) plus a 12-line
  insertion after line 335 (the A5 block). No content moved between files: the Probe's three hunks are
  additions, and nothing deleted from `STATE.md` reappears in the Probe.
- Row 135's growth is entirely accounted for by E4 and E4b (see A5) — a **large** change, but the
  size is the E4/E4b text, not a restructure. The instruction was followed; only the *report* of the
  size is wrong.

## Target 4 — E4 landed, and E4b with it

Read in reading order, as a quoted fragment would be:

> … the sixth deliverable did the *generalisation* correctly **— and, in the same document, still
> asserted one universal in §0 off `n ≤ 5` antichain witnesses with no proof present, which is why it
> appears in the second 4d tally rather than in neither. BOTH FACTS ARE TRUE OF THE SAME DOCUMENT AND
> NEITHER CANCELS THE OTHER …**

The connective begins **61 characters** after the clause. A reader who quotes the clause alone gets the
reconciliation with it. **The fix has landed.**

**The 318 figure reproduces exactly.** In `db08b4c:STATE.md` line 135, start of *"did the
`*generalisation*` correctly"* to start of *"Step 4d DID fire here"* is **318 characters** (325 bytes),
with no connective in the gap. mg-f7bc's F7 table calls it *"318 bytes"*; the figure is exact in
**characters**, which is how mg-f2e1 states it, and mg-f2e1 is the more careful of the two.

**E4b holds.** The stale counts (*"the other **six** firings"*, *"FIRED AT **SEVEN** LOCATIONS"*)
survive only inside their own correction note, quoted as what the row used to say; the row now points
at Appendix A's two tallies instead of hard-coding a number Appendix A recounts. That is Appendix A's
own resolution applied to itself, and it cannot rot on the next recount.

## Target 7 — what mg-f2e1 added beyond its brief, which is the primary target

The rule this arc just learned, from mg-d39d's `G″`: **the defect is in the material the landing added
beyond what it was asked for.** Five additions, and it holds again.

| addition | asked for? | outcome |
|---|---|---|
| the `G″` / *"arc's FIRST BROKEN item"* evidence paragraph | **no** — the ticket asked only to *"state WHY in the rule: every defect this arc has produced landed in a summary artifact"* | **carries A1 (BROKEN)** |
| `artifact_banner_check()`, a new control | **no** — the ticket asked only to *"make the self-test emit a string that cannot be confused with the bottom line"* | **carries A2 (MAJOR)** |
| E4b, row 135's stale counts | no (self-declared, found while fixing E4) | **correct**, and correctly done in place |
| the §12 preamble **reversal** + a second `⟪…⟫` marker beside *"the pipeline survived the control it was missing"* | beyond the literal brief, which named only the `38/38` site | **correct**, and it improves the artifact: the *"corrected in §5, not here"* call was the inconsistency |
| the *"reach defect"* parenthetical on repository scope in A5 | **no** | accurate as far as this repository can show, and correctly hedged (*"not demonstrable from the artifact the audit stage watches"*) |

**Two of five carry the two most serious findings, and both are sentences about mg-f2e1's own method.**
Fifth consecutive generation, same shape, and predicted in the audit brief before the commit existed.

## What stands, and it is most of the commit

Recorded because a RED verdict on the summary must not read as a RED on the work.

- **The widening is right, fires on every `STATE.md`-only landing in the arc, and does not fire on
  everything.** `c50ce32` verified as the existence proof; `c0cf104`'s eight-line hunk verified as
  carrying both mg-1319 defects; 45% of the arc's commits fall outside the trigger.
- **All six of E1–E6 are present and correct on the facts they fix.** E6's 78-vs-82 line-F split is
  exactly right: `out_nc3.txt` shows `line3 : 78 of 78 biting FIRES` for the ridge-drop and `line3 :
  82 of 82 biting SILENT` for the mis-indexed enumeration, so only one of `db08b4c`'s two corruptions
  leaves NC3's negative lines silent — and it is correctly scoped as *recorded, not fixed*, because a
  commit message is immutable.
- **The six cited 0-BROKEN verdicts all check out** (`013e073`, `fcc8a11`, `321509f`, `2cc8d57`,
  `34c151f`, `de54c3a`).
- **mg-f2e1 corrected its own ticket rather than inheriting it.** The ticket asserts `c50ce32`
  *"carried TWO OF THE THREE DEFECTS THIS COMMIT IS REPAIRING."* It did not — both rode in via
  `c0cf104`'s hunk. The landing states `c0cf104`, correctly, and keeps `c50ce32` only as the
  `STATE.md`-only existence proof. **The one place it was handed a wrong number, it did not adopt it**,
  which is the discipline mg-f1b2 found missing a generation earlier.
- **The instrument repair was not revisited and not over-corrected**, as instructed; nothing reads as
  *"the battery was broken."*
- **`controls_output.txt` regenerates byte-identically** (two runs, 2.1 s each, identical to the
  committed file). The A4 machinery underneath E5 is sound (ATTACK E).
- **The no-restructure instruction was obeyed exactly**, and the commit names what it deliberately did
  not do.

## The repair, in order of cost

1. **Strike and replace the `G″` sentence in `STATE.md` Appendix A and stop citing it as the strongest
   evidence** (A1). The row landed in `docs/OneThird-Hodge-Side-Leverage.md` (line 877 as `f6756c0` left it) via `f6756c0`, a
   commit the instrument clause already covered, and mg-d39d says `STATE.md` was clean. The widening
   does not need it.
2. **Decide what the corrected fact implies for the clause's scope** (A1 tail, A7): the arc's only
   BROKEN item was a ledger row in a **deliverable document**, which passes the widening's own
   *reader-consults-this-instead-of-the-source* test and which the clause does not name.
3. **Strike the last clause of `artifact_banner_check`'s "Scoped exactly" paragraph** (A2) — *"so it
   makes the artifact's occurrences of the banner exactly the bottom line's"* — and, if the guarantee
   is wanted, scan `detail` strings and headings too; ATTACK B is four lines.
4. **Complete or re-class the `38/38` enumeration** (A3): name the class *every frozen
   independent-audit document*, or list all seven unflagged sites.
5. **Fix the changelog's `§5` claim** (A4) and **the +949 figure** (A5).
6. **Narrow *"the whole defect population"* to *"concentrated in"*** (A6).

---

*This document scores CLAIMS. It does not re-open the probe's mathematics, which mg-e0ce, mg-5630 and
mg-f7bc rebuilt and which nothing here touches. `STATE.md` was NOT edited by this audit.*
