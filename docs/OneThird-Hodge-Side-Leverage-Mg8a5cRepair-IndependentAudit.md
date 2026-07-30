# Independent audit — the mg-a318 repair (`b80dea0` + `7f66005`)

**Work item mg-835f. Pre-filed in the same action as its parent mg-8a5c.**
**Instrument: `code/hodge_leverage_audit_835f/`, `run_all.sh`, ~2 min. Committed transcript:
`out_audit_a318.txt`. Predicted exit code, written before the first run: 1. Observed: 1.**

---

## Verdict

**THE PRIMARY TARGET IS CONFIRMED, AND IT IS CONFIRMED BY MEASUREMENT RATHER THAN BY READING
THE GATE.** The brief was explicit that a gate can be renamed rather than fixed, so nothing
below concludes from `verify_landing.py`'s source that it checks the site. Instead: every one
of the **12 reader-facing (site, figure) pairs** — 5 at the `STATE.md` row, 2 at deliverable
§14, 5 at H8 — was corrupted **on disk**, one at a time, with every other occurrence of that
figure left correct, and the real runner was executed against the mutated tree.

| | result | population |
|---|---|---|
| **mutated and fired** | **12 of 12** exit 1 | the 12 (site, figure) pairs the documents publish |
| **untouched and silent** | **12 of 12** return to exit 0 | the same 12, restored and verified byte-identical by sha256 |
| **the check that fired** | **12 of 12** is the SITE READ | `GATE @ <site>: '<figure>' READ AT THE SITE = …, MEASURED THIS RUN = …` — not the written-once counter alone |
| **wrong at the site, right elsewhere in the file** | **12 of 12** fire | the exact configuration `e16e41c`'s gate passed at all three sites |
| **right at the site, wrong elsewhere in the file** | **12 of 12** silent | the gate's *declared* scope: a site is a section, not the file |

**Every mutation is length-preserving, and that is not a detail.** Four of the five figures are
lengths of the very text being mutated, so an *insertion* moves the measurement and the gate
fires for a reason that has nothing to do with where it looks. A mutation that changes a file's
length proves nothing about a self-referential gate. Every mutation in this audit preserves the
byte length of the file it touches, by construction and by assertion — so each of the 12 fires
is attributable to the gate reading the site.

**The clean null is undisturbed.** The five published figures reproduce by **three disjoint
routes** — Python `len` on the decoded working tree, coreutils `wc -m` on `git show HEAD:…`,
perl `length()` under `-CSD` on `git cat-file blob HEAD:…` — 5 of 5 agreeing, two of the three
routes never touching the working tree. No commit between `b80dea0` and HEAD touches any of the
three files. The repair **did** move the cell it was measuring (`+675` characters to the
`STATE.md` row), so the fixed point was real and was solved rather than avoided.
`out_verify.txt` regenerates byte-identically at HEAD, and so does the mg-2da3 control whose
committed output `7f66005` regenerated to follow this repair's `STATE.md` edit — which is the
discriminator between an evidence file regenerated to **follow** a corrected document and one
bent to **agree** with a wrong one.

**0 mathematical statements are touched by this audit and none is re-opened.** Nothing
retreated: all four of mg-8a5c's findings carry a disposition annotated in place, F-1 and F-2
LANDED and F-3 and F-4 NOT LANDED, and none is re-marked here.

**What is open is one level out from the gate, and one sentence short of the summary repair.**

| | severity | finding | disposition |
|---|---|---|---|
| **G-1** | **MODERATE** | the gate reads **one designated statement per site**; a reader reads the **section**. A wrong figure written into the site in **ordinary prose** — not in the labelled form the gate's regex locates — is not seen, at **3 of the 3 sites**, at exit 0. This is not F-1 reopened: F-1's own shape now fires 12 of 12. It is F-1's **mechanism** one level out, and the arc has precedent that the next correction *adds* a mention rather than corrupting the existing one — that is exactly how F-1 was born, out of mg-8e30's own corrected wording | ⚠️ **LANDED 2026-07-30 by mg-8916, BY WIDENING THE CODE — the stated extent is NOT narrowed.** `figure_gate` now also takes a **CENSUS** of every figure-shaped token the *section* asserts, prose included, against the live measurements plus a declared roster of each site's historical figures. The three U1 probes that were silent here **fire 3 of 3 on disk against the real runner**, and so does the probe a set-membership test would pass (a wrong prose figure reusing a roster value); all 6 restorations return the run to exit 0, sha256-checked — `code/hodge_leverage_repair_8916/` R1 |
| **G-2** | **MINOR–MODERATE** | `7f66005` exists to make `audit_repair_8e30.py` "tell the truth on a RE-RUN". Its BOTTOM LINE has **two** sentences and **one** was amended. Re-run at HEAD the instrument prints two `[REFUTED]` lines in **T1, its own declared PRIMARY TARGET** — *"the three published parts reproduce from the tree"* and *"THE REPAIR'S FIGURES DID NOT GO STALE"* — and then prints, unconditionally, *"THE PRIMARY TARGET IS CONFIRMED: the repair's three figures are the POST-commit ones and reproduce exactly from the tree."* Both are in the same transcript. This is the shape `7f66005`'s own commit message calls "the defect this whole arc keeps paying for", surviving inside the fix for it | ⚠️ **LANDED 2026-07-30 by mg-8916.** The bottom line is no longer written: it is **DERIVED** from the rows tagged `PRIMARY`, and a `SUMMARY vs ROWS` check compares the two and is recorded like any other check. **T1 is not relaxed to keep the summary true** — it audits `e16e41c`, so its expectations are the figures `e16e41c` published. The check is **shown firing**: forced to the sentence it used to print unconditionally, it goes `[REFUTED]` and moves the refuted count — `code/hodge_leverage_repair_8916/` R2 |

**Neither is a retraction of the repair.** The repair did the harder half first and did it
right; both findings are about the edge of what it now covers.

⚠️ **NEITHER G-1 NOR G-2 IS LANDED HERE, and saying so is not a formality.** This audit changes
no document it audits: it adds `code/hodge_leverage_audit_835f/` and this file and nothing else,
because an auditor that repairs what it is auditing destroys the measurement. Both are open and
are pm-onethird's to size. **mg-3c24 merged with findings and no successor was ever filed** —
the audit-successor detector recovered that drop, and it is the reason this paragraph exists
rather than being left implied.

⚠️ **BOTH ARE NOW LANDED, by mg-8916 (2026-07-30), and the successor was filed rather than
dropped.** The dispositions above are annotated in place; the repair and its evidence are
[`OneThird-Hodge-Side-Leverage-Mg835fRepair.md`](OneThird-Hodge-Side-Leverage-Mg835fRepair.md)
and `code/hodge_leverage_repair_8916/`, `run_all.sh`, ~30 s. **Nothing in the body of this audit
below this line has been edited** — the measurements it reports are the measurements it took,
against the tree it took them against, and a later repair must not rewrite them. In particular
**§6's U1 rows still read `gate passes`, and they were correct when taken**: that is what the
gate did before mg-8916, and `code/hodge_leverage_repair_8916/` R1 is the record of the same
probes firing after it.

---

## 1. The primary target: the gate, mutated at each site, on disk

The brief calls this the deletion test's sibling — *do not read the gate's code and conclude it
checks the site; make a reader-visible figure wrong and see whether the run goes red.* So the
instrument writes to `STATE.md`, `docs/OneThird-Hodge-Side-Leverage.md` and
`docs/state-history/attempt-mg-a3d4.md`, runs `verify_landing.py` against the mutated tree,
`git checkout --`s the file back inside a `finally`, verifies the restoration by sha256, and
runs the gate **again** — because a gate that fires on everything is worth no more than one
that fires on nothing.

    #   site               figure   wrote     predicted   observed    restored
    1   the STATE.md row   gap      +9 999    FIRES       FIRES       silent
    2   the STATE.md row   both     +99 999   FIRES       FIRES       silent
    3   the STATE.md row   cell     99 999    FIRES       FIRES       silent
    4   the STATE.md row   hist     99 999    FIRES       FIRES       silent
    5   the STATE.md row   copy     99 999    FIRES       FIRES       silent
    6   §14                gap      +9 999    FIRES       FIRES       silent
    7   §14                both     +99 999   FIRES       FIRES       silent
    8   H8                 gap      +9 999    FIRES       FIRES       silent
    9   H8                 both     +99 999   FIRES       FIRES       silent
    10  H8                 cell     99 999    FIRES       FIRES       silent
    11  H8                 hist     99 999    FIRES       FIRES       silent
    12  H8                 copy     99 999    FIRES       FIRES       silent

**Both directions, at every site.** 12 of 12 mutated-and-fired; 12 of 12 untouched-and-silent.
The written-once counter fires additionally on 10 of the 12 — the 2 it does not are the frozen
§14-copy figure at the `STATE.md` row and at H8, which the gate declares non-live and which may
legitimately recur in the quoted history.

**And the discriminating case, which A1 alone does not settle.** A1's mutation removes the
correct copy along with the wrong one, so a presence test would also have fired. §2 puts the
correct copy back.

---

## 2. Site read or presence test? The configuration that fooled `e16e41c`

F-1 was never "a wrong number". It was a wrong number **at the site** with a right one
**elsewhere in the same file**, and a gate that could not tell them apart. So each of the same
12 pairs was corrupted at the site **and** a correct copy of the very figure was planted
elsewhere in the same file, outside the site, length-preservingly, over a named word of exactly
its length (`'answer'`, `'bridge'`, `'record'`, …, all printed in the transcript).

**12 of 12 fire.** A presence test passes every one of them.

The converse — site left correct, a wrong copy planted outside it — is **silent 12 of 12**.
That is reported as the gate's *declared scope* rather than as a pass or a fail: the repair
says at all three sites that a site is a **section**, not the file that contains it, and it is.
§6 asks what that leaves **inside**.

---

## 3. Derivation, or declared duplication?

The ticket prefers one figure **deriving** from the other over a cleverer gate, and the
repair's own new Appendix A rule adds the fallback: an unavoidable duplicate must be
**declared** beside the figure. Both halves measured.

**(1) The within-site duplicate is gone, structurally.** Over the population of 4 live figures
× 3 sites = 12 cells, the maximum within-site count of any live figure is **1**. The chain's
tail points at the live figure instead of restating it. mg-8a5c's own multiplicity table,
re-run at HEAD, independently reports **0 of 15 cells** carrying a needle more than once (it
was 3, all of them the live gap).

**(2) The duplication is not gone; it moved up a level — and the gate now requires that shape.**

    gap, cell only                 +2 744   written at 3 of 3 sites
    gap, cell + relocated history +23 771   written at 3 of 3 sites
    STATE.md row cell              13 367   written at 2 of 3 sites
    relocated history              21 027   written at 2 of 3 sites

**10 written literals of the 4 live figures survive across the 3 sites.** Two copies in one
section became one copy in each of three files. This is the irreducible residue — three
documents must each state the figure to a reader who is reading only one of them — but it is a
residue, and calling the duplicate "gone" without qualification would be the overstatement this
arc keeps auditing.

**(3) It is declared, at 3 of 3 sites.** The phrase *"written once **per site**"* appears in
the prose beside the figure at the `STATE.md` row, at §14 and at H8; "per site" is precisely
the declaration that other sites carry the same figure. All three additionally mention both
other sites by name (a token-presence test, reported as one). **The brief's second question
resolves in the repair's favour:** derivation was chosen where derivation was possible, and
what could not be derived is declared rather than left silent for the next editor to find.

---

## 4. The clean null: this repair edits the cells it reports on

mg-8a5c's primary target was that mg-8e30's figures had not gone stale, and it held by three
disjoint routes. This repair runs the same mechanism again on its own numbers, so the same
question is asked with tooling chosen to share no implementation.

    quantity                             py/tree  wc -m/blob  perl/blob  agree
    STATE.md A5 cell                      13,367      13,367     13,367    yes
    relocated row history (file)          21,027      21,027     21,027    yes
    deliverable §14 copy                  10,623      10,623     10,623    yes
    gap, cell only                        +2,744      +2,744     +2,744    yes
    gap, cell + history                  +23,771     +23,771    +23,771    yes

Python `len` on the decoded working tree; coreutils `wc -m` under a UTF-8 locale on
`git show HEAD:…` (the newline `grep` emits is subtracted explicitly rather than absorbed);
perl `length()` under `-CSD` on `git cat-file blob HEAD:…`. **5 of 5 agree**, and two of the
three routes never read the working tree at all.

All 12 figures a reader meets equal the measurement. `git log b80dea0..HEAD --` over the three
files is empty. `out_verify.txt` regenerates byte-identically (15,863 chars). The mg-2da3
control regenerates byte-identically at exit 0 (37,233 chars) — the check that matters most
here, because `7f66005` *regenerated* that committed output to follow this repair's `STATE.md`
edit, and a document left wrong with its evidence bent to agree presents identically in a diff
to a document corrected with its evidence regenerated to follow.

**The repair's own figures did not go stale.**

---

## 5. The seam sweep — three corrections, one artifact

`bbe83b5` (mg-e1d0), `e16e41c` (mg-8e30) and `b80dea0` (mg-a318) have each corrected the same
three passages. Three sweeps, every population and threshold printed.

**Sweep 1 — figure-bearing sentences.** Population: sentences ≥ 120 chars carrying a figure, in
the 4 documents the three corrections touched (`STATE.md` 266, the deliverable 152, the
mg-8a5c audit doc 45, `attempt-mg-a3d4.md` 27 — **490 sentences, 119 805 pairs**). Similarity:
`difflib.SequenceMatcher.ratio()` on flattened text, **threshold 0.80**. **1 pair** crosses it
and **0** are seam hits: the deliverable and the row history state the same `γ_i ≤ 1/2` result
at ratio 0.955 **with identical figures**, which is a summary and its history file agreeing.

**Sweep 2 — marked quotations.** Population: marked quotations ≥ 60 chars in the same 4
documents (`STATE.md` 39, the deliverable 12, the audit doc 6, the row history 5 — **62
quotations, 1 891 pairs**). **Threshold 0.75**, deliberately lower than sweep 1 because a
quotation is short and a one-figure difference costs more of the ratio. **9 pairs** cross it,
**0** are seam hits; all 9 are printed with why, and the discriminator is stated: a pair counts
only if **both** members carry figures and the figure sets disagree. One member eliding its
figures behind `…` is an abbreviation of a passage, not a second copy of a number.

**WHAT WOULD HAVE COUNTED**, so both nulls are checkable rather than asserted: for sweep 1, two
figure-bearing sentences (mean length 377 chars) sharing ≥ 80% of their characters while
stating different numbers — a stale copy differing only in a 5–7 character figure scores ~0.98
and would be reported. For sweep 2, the same withdrawn passage quoted in two places with two
different numbers in it, which is precisely the shape `−875` had before mg-8e30.

**Sweep 3 — the normative sentence, because the arc's own rule is that a duplicated literal is
a seam whether or not a figure is in it.** Population: written copies of the Appendix A rule
across every `.md` file in the repository. **4 copies, at 2 lengths:**

    short  STATE.md                                                    (inside the A5 cell)
    LONG   STATE.md                                                    (Appendix A itself)
    short  docs/OneThird-Hodge-Side-Leverage-Mg3c24Repair-IndependentAudit.md
    LONG   docs/OneThird-Hodge-Side-Leverage-Mg8e30Repair-IndependentAudit.md

Two carry the clause *"AND MUST SAY WHICH SIDE OF THE EDIT IT IS ON"* and two stop before it —
including the copy inside the `STATE.md` A5 cell, which quotes the rule under a title that is a
**prefix** of the title Appendix A gives it. **PRE-EXISTING AND NOT THIS REPAIR'S:** `git log -S`
puts both lengths in `e16e41c` (mg-8e30), one generation earlier; mg-a318 neither widened nor
narrowed them. Named rather than counted, and not raised as a finding against mg-a318.

---

## 6. The floor — one thing no list in the brief names

**Chosen because of how F-1 was born.** F-1 did not arrive as a corruption of an existing
figure. It arrived because mg-8e30's own **correction added** a second mention of the live gap
— the chain's tail — and the gate could not tell the two apart. mg-a318 removes that copy and
gates against a second one. But the gate reads **one designated statement per site**, located
by its exact wording, and a reader reads the whole section. So: if the next correction writes
the figure into the section in **ordinary prose** rather than in the labelled form, does
anything see it?

    probe                                                                    predicted    observed
    U1 the STATE.md row: a WRONG figure restated in ordinary prose at the site  gate passes  gate passes
    U1 §14: a WRONG figure restated in ordinary prose at the site               gate passes  gate passes
    U1 H8: a WRONG figure restated in ordinary prose at the site                gate passes  gate passes
    U2 H8: a FIFTH column added to the three-column table                       GATE FIRES   GATE FIRES
    U3 STATE.md row: the live figure re-marked as a QUOTATION                   GATE FIRES   GATE FIRES
    U4 STATE.md: the whole row duplicated (the locator's uniqueness)            GATE FIRES   GATE FIRES
    U5 §14: the statement REWORDED, the figure still correct                    gate passes  GATE FIRES

**G-1.** The sentence *"the gap is now +9 999 characters."* was written inside the `STATE.md`
row, inside §14 and inside H8, **length-preservingly** so that no measurement moved, leaving
the labelled statement the gate reads correct and untouched. **The run stayed at exit 0 every
time.** A reader of any of the three sites now meets two figures for the same quantity, one of
them wrong, with the checker green.

This is **not** F-1 reopened, and it should not be reported as if it were: F-1's own shape —
corrupting the designated statement, or restating the figure a second time in the **same**
labelled form — now fires 12 of 12 (§1) and fires on the reinstated duplicate (the repair's own
N5). G-1 is F-1's *mechanism* one level out: the copy the gate cannot see is no longer a second
**labelled** figure but an **unlabelled** one. The reason it is worth landing rather than
noting is the precedent — the last two corrections in this chain each *added* prose next to the
figure, and one of them created F-1 by doing so.

**The gate is fail-CLOSED where the locator can break**, which is the right direction and is
confirmed on 3 of 3 structural probes: a fifth table column, a figure re-marked as a quotation,
and a duplicated `STATE.md` row all make the run **red**, not green.

**U5 is the same property, reported as a cost rather than a defect.** Rewording `cell-only gap
**+2 744**` to `cell-only gap **of** +2 744` — a copy-edit changing no figure — turns the run
red. Fail-closed is correct; what the transcript does not currently say is that an innocent
edit to the *wording* is a red run, and someone will meet that without warning.

---

## 7. Predictions, including the ones that missed

Written before the runs and kept as written.

| prediction | observed |
|---|---|
| instrument exit code | **1**, as predicted |
| A1, all 12 pairs FIRE | **12 of 12**, as predicted |
| A1, all 12 restorations silent | **12 of 12**, as predicted |
| A2 part A, all 12 FIRE | **12 of 12**, as predicted |
| A2 part B, all 12 silent | **12 of 12**, as predicted |
| A6 U1 ×3, `gate passes` | **passes ×3**, as predicted — this is G-1 |
| A6 U2/U3/U4, `GATE FIRES` | **fires ×3**, as predicted |
| **A6 U5, `gate passes`** | **MISSED — it FIRES.** A wording change is not a figure change, so a pass was predicted. The gate is fail-closed on rewording, which is *better* than the prediction, and is reported as a cost rather than folded in quietly |
| **method, not outcome** | **MISSED.** The three U1 probes were first run as **insertions** and observed to fire at two of three sites. That meant nothing: an insertion moves the very lengths the figures are, so the gate fired on its own measurement rather than on the site. Re-run length-preservingly, all three pass. The insertion runs are not reported as fires anywhere, and G-1 rests only on the length-preserving runs |

`verify_landing.py`'s own nine-mutation battery was **not** taken as evidence for anything in
§1 or §2: it runs `figure_gate` in memory on strings, which is the right design for that
instrument but is the author's own control. Everything in §1 and §2 is on disk, against the
real runner, by code that shares nothing with it except the module it is auditing.

---

## Reproduction

    python3 code/hodge_leverage_audit_835f/run_all.sh     # ~2 min, exit 1

The transcript regenerates byte-identically at any tree in which `STATE.md`,
`docs/OneThird-Hodge-Side-Leverage.md`, `docs/state-history/attempt-mg-a3d4.md`,
`docs/OneThird-Hodge-Side-Leverage-Mg8e30Repair-IndependentAudit.md`,
`code/hodge_leverage_landing_e1d0/`, `code/hodge_leverage_audit_8a5c/` and
`code/state_landing_control_2da3/` are unchanged; it embeds no sha of its own, and it was
checked byte-identical across two consecutive runs.

⚠️ **THAT CONTRACT IS BROKEN BY mg-8916, DELIBERATELY, AND `out_audit_a318.txt` IS FROZEN AT
THIS RUN.** mg-8916 edits `code/hodge_leverage_landing_e1d0/verify_landing.py` (the G-1
widening) and `code/hodge_leverage_audit_8a5c/audit_repair_8e30.py` (the G-2 derivation), which
are two of the seven paths named above. A re-run therefore does **not** reproduce this
transcript — §6's three U1 rows would read `GATE FIRES`, which is the repair. **The committed
transcript is the run as TAKEN and is not regenerated**; the post-repair measurement of the same
probes is `code/hodge_leverage_repair_8916/out_repair_8916.txt`. Which artifact is frozen and
which is regenerated is stated in both, because a document left wrong with its evidence bent to
agree presents identically in a diff to a document corrected with its evidence regenerated to
follow.

It **mutates the tree and restores it**,
refuses to run against a dirty one (scoped to the three files it will `git checkout --`), and
verifies every restoration by sha256. `git status` is clean after a run except for
`code/hodge_leverage_audit_835f/`.
