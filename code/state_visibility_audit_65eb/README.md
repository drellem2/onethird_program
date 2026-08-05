# mg-65eb — INDEPENDENT AUDIT of the mg-a74f visibility-instrument repair

**Pre-filed in the same action as its parent.** `PREDICTIONS.md` was committed at `880fc15`,
**before any `.py` or `.sh` in this directory existed** — verifiable without trusting this
sentence: `git ls-tree 880fc15 code/state_visibility_audit_65eb/` holds `PREDICTIONS.md` and
nothing else. Every figure below is scored against it and **every miss is kept as written**.

> The anchor in the line above is checked by nothing. That is this audit's section 5 finding
> turned on itself, and it is stated here rather than left for the next auditor to find.

---

## THE VERDICT

**The repair holds. Its three answers are sound, nothing regressed, and the classification is
honest.** Against that:

| | |
|---|---|
| **5 of the 9 rows** mg-a74f publishes as `MATCHES` **are separable by construction** | §1 |
| **3 of the 5 separations are in `visible_a74f.py`** — the instrument built to answer OPEN 1 | §1 |
| the instrument whose safety argument is that it **fails open** **fails CLOSED** on `class="hidden"` | §2 |
| `739f7bd`, the anchor carrying this repair's **own integrity claim**, is **STALE** | §5 |
| **`claims16eb.py` carries 4 of its 17 verdicts as the literal `False`** — and nothing runs it | §3 |
| **0 regressions**, 0 disagreements on the six, 0 downgrades | §3, §4 |

The last row of the table is the one this audit did not go looking for, and it is the one a
reader should carry away. It is below as **FINDING B**.

---

## 1. THE PRIMARY TARGET — the property CLAIMED beside the quantity COMPUTED

`rows65eb.py`, transcript `out_rows65eb.txt`. Population: **the 9 rows `claims_a74f.py`
publishes** under *"EVERY INSTRUMENT THIS REPAIR ADDS, AND WHETHER ITS ROW NAME IS ITS
MEASUREMENT"* — 8 `MATCHES` and 1 `DOES NOT MATCH, deliberately`.

**9 of 9 reached a verdict. 5 SEPARATED, 4 NOT SEPARATED.** Every separation is a document or
a tree on which the two sets differ, built and run, not argued:

| row | separated by |
|---|---|
| **R2** `visible_a74f` `not-suppressed` | three ways — see below |
| **R4** `prose_a74f` P1 | a path named and absent scores 0 findings if its extension is not one of six; an **untracked** file satisfies a claim about *the revision* |
| **R5** `prose_a74f` P2 | a false `section N` claim is invisible unless the literal `run_all.sh` is **on the same line** |
| **R6** `prose_a74f` P3 | one extra key named `"note"` removes a pinned table from the population entirely |
| **R7** `prose_a74f` P4 | the verdict is decided by the **nearest `.py` basename in the preceding 400 characters**, not by the claim's subject |

**The three separations inside `visible_a74f.py`, which is the finding:**

- **R2a — it fails CLOSED.** `<div class="hidden">` scores `not-suppressed 0/5` on both
  renderers. `NOT_COVERED` names class-based hiding as *outside* the declared set, the
  document has no stylesheet, and **a reader is shown every section of it**. The docstring
  and the README both say the instrument *fails open*. This is §2 below.
- **R2b — it does not implement its own declared S1.** `<details title="open me">` carries no
  `open` attribute, so declared S1 holds of it; the instrument scores it `5/5 not-suppressed`
  because `open` is matched as a **word anywhere in the attribute text**.
- **R2c — an offset taken in one string is spent in another.** `visible_a74f.main()` takes
  `html.unescape(out).index(marker)` and spends it as an index into `out`. Put 3000 `&`
  before mg-a74f's **own V3 blank page** and it scores `5/5 NOT SUPPRESSED` against `0/5`
  without them. **A byte offset standing in for a position is the defect class this whole arc
  is about, and it is in the instrument built to repair it.**

**The four not separated, with the reason stated rather than left as absence:** R3 (mg-a74f
already publishes it as a mismatch and builds V1/V3/V4 to show it), R8 (the exit code is read
from `subprocess.returncode` and never inferred from stdout — the one thing that could
separate them is what §2 of `battery_a74f.py` refuses in writing to do), R9 (claimed and
computed are the same predicate over the same two revisions), and **R1, which this audit
predicted would separate and which did not** — see MISSES.

> **A separation is not a bug report.** Each instrument above is correct about the quantity it
> computes. What is reported is that the quantity is not the property the row names.

---

## 2. THE DIRECTION OF THE ERROR — the parent's own safety argument, refuted

`visible_a74f.py`'s docstring and mg-a74f's README both say the instrument **FAILS OPEN**:
*"a suppression mechanism outside the set is scored NOT SUPPRESSED"*. That one-directional
claim is the whole of why the column may be trusted.

**It is refuted, and in the direction that matters.** `class="hidden"` is named by
`NOT_COVERED` as outside the declared set, and it is scored **SUPPRESSED**. A document with no
stylesheet in it shows a reader every section, and the instrument reports a mechanism
suppressed them. **Predicted in `PREDICTIONS.md` §2 before the probe existed, and observed.**

---

## 3. THE SIX CLAIMS — re-classified from scratch

`six65eb.py`, transcript `out_six65eb.txt`, **exit 0**.

**The enumeration is COMPLETE.** `claims16eb.py` run unmodified at `bd24efc` reports 6 BROKEN
of 17 rows; mg-a74f's `SIX` (read out of `claims_a74f.py` with `ast`, not transcribed) joins
to all six. **Nothing in mg-16eb's six is missing from mg-a74f's enumeration and nothing is
added.**

**The classification agrees on all six, and there is no downgrade.**

| | this audit | mg-a74f | probe |
|---|---|---|---|
| claim 1 | FALSE | FALSE | resolved the path at `bd24efc`: it does not exist |
| claim 2 | FALSE | FALSE | counted `mutations_0049.ROWS` at `bd24efc`: 9, not 6 |
| claim 3 | FALSE | FALSE | **construction** — 2 of 2 forbidden drifts exit **0** at `bd24efc` |
| claim 4 | FALSE | FALSE | **construction** — **both** directions refuted |
| claim 5 | FALSE | FALSE | resolved the section by its **command**: both batteries are in section 8 |
| claim 6 | TRUE OF A DIFFERENT PROPERTY | TRUE OF A DIFFERENT PROPERTY | **construction** — 5/5 bytes on the page, **0/5 shown to a reader** |

The rule that assigns those buckets is written in code and applied identically to all six:
*refuted as named **and** true of the measured quantity → TRUE OF A DIFFERENT PROPERTY;
refuted as named alone → FALSE; not probeable → UNSUPPORTED; otherwise → TRUE-BUT-UNEVIDENCED.*

**The hazard the brief names is absent, and the reason is worth saying rather than leaving as
an absence: both soft buckets are empty.** There is nowhere to downgrade *to*. Every one of
the six was refutable by resolving a reference or by building a tree, and this audit did one
or the other for all six rather than reading mg-a74f's label.

The one row where the classification could have gone wrong is **claim 6**, and it is the row
carrying the different label. Its two conjuncts come apart under construction exactly as
mg-a74f says. **Claim 4 — refuted in *both* directions, so no reading of it survives — is
correctly *not* in that bucket.** That distinction is the whole of what this section was asked
to check.

### The constructions, because a classification is only as good as its evidence

**Claim 3, at `bd24efc` and at HEAD** — the same three mutations of `DELEGATED_PRESENTATION`,
each run through `delta_control.py` *as it stands at that revision*:

| | `bd24efc` | HEAD |
|---|---|---|
| D1 a presentation record for a section nothing delegates | **exit 0 — quiet** | exit 2 |
| D2 a whole target file certified here and delegated by nobody | **exit 0 — quiet** | exit 2 |
| D3 a delegated section's record deleted *(the direction the sentence gets right)* | exit 2 | exit 2 |

Two of the two drifts the sentence forbids are silent at `bd24efc`, and both are caught at
HEAD. **That is claim 3 refuted where the defect is present and the repair demonstrated where
it is not, from an instrument that is not mg-a74f's.**

**Claim 4, at `bd24efc`** — presentation decided by *this audit's own* HTML walk, never by the
control's opinion of itself:

| | exit | cited sections shown to a reader |
|---|---|---|
| E1 an ordinary fenced code example inside cited section H3 | **1** | **5/5 on both renderers** |
| E2 `<details><summary>` over the whole document | **2** | **0/5 on both renderers** |

**Both directions fall.** Exit 1 does not mean "not presented" (E1), and "not presented" does
not mean exit 1 (E2).

### FINDING B — the enumerator's own verdicts are pinned

**This is the finding this audit did not go looking for, and it is the largest.**

`claims16eb.py` — mg-16eb's program, *the one that produced the six* — makes 16 `claim()`
calls. Read with `ast`, **7 carry a constant verdict, and 4 of those are the literal `False`
on the main path**:

```
claims16eb.py:94    delta_control.py:757 (DELEGATED_PRESENTATION)        LITERAL False
claims16eb.py:142   delta_control.py:346 (the EXIT CODES table)          LITERAL False
claims16eb.py:194   .../README.md:105-106                                LITERAL False
claims16eb.py:217   .../render0049.py:11 and out_render.txt              LITERAL False
```

Those are claims 3, 4, 5 and 6 — **four of the six**. Run `claims16eb.py` unmodified **on the
repaired tree** and it reports **4 BROKEN of 17**, and **4 of 4 of them are the pinned rows**.
Claims 1 and 2, whose verdicts are computed (`exists`, `count == ...`), flipped to `holds`
when mg-a74f repaired them. The other four cannot flip. **They would report BROKEN whatever
the repair did.**

Two consequences, and they point in opposite directions:

1. **In mg-a74f's favour** — a reader who runs the auditor's own claim-checker on the repaired
   tree gets a transcript saying four of the six are still broken. **That transcript is not
   evidence against the repair.** It is what a constant returns.
2. **Against the record** — `claims16eb.py` is named *"THE CLAIMS mg-0049 ADDED, **CHECKED**"*.
   For 4 of its 17 rows the quantity computed is a constant. **That is this audit's primary
   question one level up: a row name that is not its measurement, in the auditor rather than
   in the auditee.** mg-16eb filed OPEN 1 against exactly this shape in mg-0049.

**And nothing runs it.** No file in `code/state_delegation_repair_a74f/` names
`claims16eb.py`. mg-a74f re-runs `battery16eb.py` and reports 6 of 8; it does not re-run the
program that produced the six it is repairing. Section 11 of this audit's `run_all.sh` runs
it, so the contradiction is at least on the record.

---

## 4. DO NOT DISTURB WHAT IS CONFIRMED — **0 regressions**

`rerun65eb.py`, transcript `out_rerun65eb.txt`, **exit 0**. Both of mg-16eb's confirmed
figures **moved**, and a moved figure is not a regression. So each was measured **at both
revisions** and the answer is the set difference, not the totals either side of it:

| | `bd24efc` | HEAD |
|---|---|---|
| mg-0049's committed transcripts reproducing | **5 of 7** | **5 of 7** |
| the two that do not | `out_coverage218d.txt`, `out_selftest_negative.txt` | *the same two* |

**Reproduced at `bd24efc` and not at HEAD: NONE.** Nothing this repair did moved them.

**The separator, measured rather than argued.** `out_selftest_negative.txt` records
`STATE.md at rest: 177464 bytes` — read *out of the committed transcript*, not typed into the
script. `STATE.md` is **177464** bytes at `8ce78fb` (mg-0049's own baseline), and **186710**
at `bd24efc` **and** at HEAD. The recorded figure was **already wrong before mg-a74f
existed**. "This repair broke two transcripts" and "two were already stale" are separated by
a measurement.

**mg-16eb's `8 of 8` is now `6 of 8`, and that movement IS the repair.** The rows that moved
are **A1 and A2 at exit 2 rather than 0** — the two drift constructions. mg-16eb predicted
PASS for them *because the hole was open*. `six65eb.py` §C builds the same two drifts
independently and reads the same two codes. `B3 exit 2` and `C1 exit 1` are unchanged.
`battery_a74f.py` at HEAD: **exit 0, 8 of 8 against its own predictions.**

---

## 5. THE FLOOR — one thing no list in the brief names: **the anchors this repair spends**

`anchor65eb.py`, transcripts `out_anchor65eb.txt` (**exit 1**) and
`out_anchor65eb_bd24efc.txt` (**exit 0**, the negative control).

The brief names rows, claims, a surface and a re-run. It does not name **the revisions the
repair pins its own integrity claim to**. Population computed, not listed: every `.py`, `.md`
and `.sh` under the four directories — 26 files, **24 distinct hex tokens over 139
occurrences**.

**23 ANCHOR-LIVE. 1 ANCHOR-STALE. 0 DEAD. 0 NOT-A-REVISION.**

The stale one is **`739f7bd`**, named at `code/state_delegation_repair_a74f/README.md:20`,
carrying mg-a74f's central integrity claim — *"`PREDICTIONS.md` was committed before any
script in this directory existed"*. It resolves, it is **not an ancestor of HEAD**, and it is
reachable only from `polecat-a74f` — **an unmerged branch, which is exactly the kind of object
that gets deleted after a merge.**

**The property is not thereby refuted.** Re-derived independently: `cfd2af5` is an ancestor of
HEAD carrying the same subject, and `git ls-tree cfd2af5 code/state_delegation_repair_a74f/`
holds `PREDICTIONS.md` **and nothing else**. The predictions really were committed first.
**What has rotted is the pointer** — a citation a reader of `main` cannot follow.

**EXISTENCE IS NOT ANCESTRY, demonstrated on the live defect rather than argued.** The defect
is present at HEAD right now, so the demonstration needs no reconstruction:

```
git cat-file -e 739f7bd^{commit}                    exit 0   PASSES
git cat-file -e 739f7bd:.../PREDICTIONS.md          exit 0   PASSES
git merge-base --is-ancestor 739f7bd HEAD           exit 1   FAILS
```

**Two of the three pass — and they are the two idioms this repair's own code is written in**
(`claims_a74f.py:57`, `prose_a74f.py:114`). A checker built the way this repair reads
revisions would certify this anchor as fine.

**Nothing checks any of them.** `prose_a74f.py` — the checker mg-a74f added for exactly this
class of rot — checks four shapes: paths, `section N` references, pinned tables, `all N rows`
phrases. **A revision is not one of them.** The proxy is computed and printed with its
quantifier so the reader need not take it on trust: the only hex character class in any source
in the population is `\bmg-[0-9a-f]{4}\b`, which accepts **4** hex digits and is a work-item
id. **SHA-shaped patterns: 0.**

And the rot is invisible for a reason: `739f7bd` is **spent by no program and checked by no
program**. The eight shas that *are* spent (`bd24efc`, `b68db5d`, …) are all LIVE, so no
program fails today. **The one anchor carried by prose alone is the one that rotted.**

**The negative control.** The same program, same rule, at `bd24efc` — where this repair's
directory does not yet exist — is **22 LIVE, 0 STALE, exit 0**.

---

## 6. THE NEW SURFACE, AND THE SINGLE POINT OF FAILURE

**The surface this repair lays is `visible_a74f.py`'s declared suppression set**, and **one
claim is now verifiable only through it.** `render0049.py`'s R5 was narrowed off the
suppression question and now *points at* `visible_a74f.py`; `render16eb.py`'s `SHOWN` column is
demonstrated wrong by that same file. Population rule computed and printed with the matching
token: **5 files** under `code/` carry a suppression-verdict token, and after this repair
**nothing else in the repository measures suppression at all.**

**That is a single point of failure the repair introduced. It is not a defect, and it is
reported as the brief asks. What is a defect is where the gap turned out to be.**

mg-a74f names this surface itself and predicts its next gap as *"a mechanism outside the
set"*. **THE GAP IS NOT WHERE THE PREDICTION PUT IT.** Two of the three separations in §1 are
**inside** the declared set — S1 and S4 are not implemented as declared — and the third is an
offset bug, not a mechanism at all. A reader who trusts the prediction watches for stylesheets
and JavaScript while `class="hidden"` scores SUPPRESSED and `<div hidden>` behind an ampersand
scores NOT SUPPRESSED, **and no second instrument in the repository would contradict either.**

---

## 7. EVERY PREDICTION, SCORED — and the misses kept

`PREDICTIONS.md` was committed at `880fc15` before any script here existed. It discloses four
things probed by hand *before* it was written (rows R2a/R2b/R2c, row A1, row S5b, and an
`ls-tree`), each marked `← probed` there and not counted as a prediction here.

| § | prediction | observed | |
|---|---|---|---|
| 1 | 6 separations over the 9 rows | **5** | **MISS — R1** |
| 1 | R2, R4, R5, R6, R7 separable | all five separated | ✔ |
| 1 | R3, R8, R9 not separable | not separated | ✔ |
| 2 | R2a refutes *fails open*, in the CLOSED direction | refuted | ✔ |
| 3 | agreement on all six | 6 of 6 | ✔ |
| 3 | 5 FALSE + 1 TRUE-OF-A-DIFFERENT-PROPERTY | exactly | ✔ |
| 3 | 0 UNSUPPORTED, 0 TRUE-BUT-UNEVIDENCED, no downgrade | 0, 0, 0 | ✔ |
| 3 | S5a — claim 5's repair is sound | section 8 runs mg-5644's suite; its §5 is mg-218d's sixteen | ✔ |
| 3 | S5b — this audit's own seventh candidate is REFUTED | refuted, and reported as refuted | ✔ |
| 4 | `reproduce16eb.py` on the tree: 5 of 7 | 5 of 7 | ✔ |
| 4 | the same at `bd24efc`: 5 of 7, the same two | 5 of 7, the same two | ✔ |
| 4 | the two are `out_coverage218d.txt`, `out_selftest_negative.txt` | exactly those | ✔ |
| 4 | `battery16eb.py`: 6 of 8, A1 and A2 | 6 of 8, A1 and A2 | ✔ |
| 4 | A1, A2 exit **2**; B3, C1 exit **2, 1** | 2, 2, 2, 1 | ✔ |
| 4 | `battery_a74f.py` §2: 8 of 8 | 8 of 8, exit 0 | ✔ |
| 4 | the recorded `STATE.md` figure is **177464** and `bd24efc` is larger | 177464; `bd24efc` 186710 | ✔ |
| 4 | regressions attributable to mg-a74f: **NONE** | 0 | ✔ |
| 5 | A1 — `739f7bd` resolves, not an ancestor, property TRUE, anchor STALE | exactly | ✔ *(probed)* |
| 5 | A2 — `bd24efc`, `8ce78fb` resolve and are ancestors | both LIVE | ✔ |
| 5 | A3 — programs resolving a sha from this prose: **0** | 0 | ✔ |
| 5 | A4 — `cat-file -e` passes `739f7bd` today; ancestry is the property | exit 0 vs exit 1 | ✔ |
| 6 | the surface is `visible_a74f.py`'s declared set; one claim only through it | confirmed | ✔ |
| 6 | the gap is **not** where mg-a74f's prediction put it | 2 of 3 inside the declared set | ✔ |
| 8 | `git diff` over the four audited directories: 0 bytes | 0 bytes, before and after | ✔ |

### THE MISS, kept as written

**§1 predicted R1 SEPARABLE and it is scored NOT SEPARATED.** The construction — every marker
written `&mdash;`, so a reader is shown `H1 — ` and the bytes `H1 — ` are nowhere in the HTML —
**works on `marked` and not on `markdown-it`**, which decodes the entity itself. This audit's
committed rule for that row was *"separates on every engine"*, and it is kept. The row is
scored NOT SEPARATED and the prediction is scored a miss.

**The rule itself is a row-name/measurement mismatch of the kind this file exists to report:**
it NAMES *"is this row separable"* and COMPUTES *"does it separate on both engines"*. It is
reported rather than rewritten. On `marked` alone, the two sets differ on all five cited
sections, which is the direction the brief calls *"content shown but not a byte in that
file"*.

### PREDICTIONS.md's own miscount, kept

§7 row 0 says *"the three audited directories"*. **There are four.** `run_all.sh` §0 prints
all four and says so on the line above.

---

## 8. THE DEFECTS OF THIS AUDIT'S OWN INSTRUMENTS

Seven, all found by this audit, all fixed, each with the reason stated in the code that
carries it. They are listed because an audit that reports only the defects of others is not
reporting its population.

1. **`rows65eb.py` R1's rule** names *"is this row separable"* and computes *"on both
   engines"*. Kept, not rewritten — §7 above.
2. **`anchor65eb.py`'s CHECKED proxy** first matched `mg-[0-9a-f]{4}` and reported one
   sha-checker where there are none. Fixed by **printing the quantifier** and reading the
   verdict off it, so the reader is not asked to trust this audit's reading of a pattern.
3. **`anchor65eb.py`'s SPENT filter** first excluded a whole **file** when a token also
   appeared in its docstring, which silently dropped `claims_a74f.py:38` — the single most
   load-bearing spent anchor in the population. Fixed to exclude per **site**. *A population
   rule that drops the row it exists to find is the defect this whole arc is about.*
4. **`six65eb.py`'s claim-5 probe** first asked whether section 7's **title** mentioned
   `218d`. It does — section 7 is `coverage218d.py`, a *different program of the same audit* —
   so the probe returned TRUE-BUT-UNEVIDENCED and this audit **disagreed with mg-a74f for a
   reason that was entirely its own instrument's**. Fixed to read the **commands**. The
   prediction was not touched; the measuring code was.
5. **`six65eb.py`'s enumeration join** was on the **site**. mg-16eb cites
   `delta_control.py:757` and mg-a74f cites `:798` for the same sentence — the file grew
   between the two revisions. **A line number is a fact about a revision**, and joining on it
   reported six mismatches where there were none. Fixed to join on the claim's own words.
6. **`six65eb.py`'s pinned-verdict count** first lumped guard branches in with main-path
   constants (7 against 4). Fixed to mark branches reachable only when an anchor has rotted —
   a constant there is a deliberate alarm, not a pinned result.
7. **`rerun65eb.py`'s exit-code regex** was anchored to the start of a line, and
   `battery16eb.py` prints four rows on one line. It read `A1` and dropped `A2` — **half of
   this audit's own predicted headline.**

---

## 9. WHAT THIS AUDIT LEAVES OPEN

- **OPEN 1 — `visible_a74f.py`'s three defects are unrepaired.** This audit locates and
  constructs them; it does not fix them, and it is the only instrument in the repository that
  measures suppression. §1 and §6.
- **OPEN 2 — `claims16eb.py`'s four pinned verdicts are unrepaired**, and the file is a
  merged auditor's transcript-producing program. Repairing it means deciding whether a
  *finding* may be re-measured by the party it was filed against. §3, FINDING B.
- **OPEN 3 — `739f7bd` is still stale**, and the branch it lives on can be deleted at any
  time. A one-line `ANCHOR-LIVENESS` gate — `git merge-base --is-ancestor` over every sha in
  a directory's prose — does not exist anywhere in this repository. `anchor65eb.py` is that
  gate; it is not wired into any control. §5.
- **This audit's own integrity anchor** (`880fc15`, first paragraph) is subject to exactly the
  rot it reports, and will be, the moment this branch is rebased and deleted.

---

## FILES

| file | what it is |
|---|---|
| `PREDICTIONS.md` | committed at `880fc15`, **before any script here existed** |
| `rows65eb.py` / `out_rows65eb.txt` | §1 — the row ledger and its constructions (exit 1) |
| `anchor65eb.py` / `out_anchor65eb.txt` | §5 — the anchors, resolved (exit 1) |
| `out_anchor65eb_bd24efc.txt` | §5 — the same program as a negative control (exit 0) |
| `six65eb.py` / `out_six65eb.txt` | §3 — the six re-classified, and FINDING B (exit 0) |
| `rerun65eb.py` / `out_rerun65eb.txt` | §4 — both confirmed figures at both revisions (exit 0) |
| `run_all.sh` / `out_run_all.txt` | all of it in order, section-numbered to `PREDICTIONS.md` §7 |

**Nothing in `code/state_delegation_repair_a74f/`, `code/state_delegation_repair_0049/`,
`code/state_landing_control_2da3/` or `code/state_delegation_audit_16eb/` is modified.**
`run_all.sh` §0 and §13 print `git diff` over all four, before and after everything runs.
