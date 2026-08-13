# mg-9bc2 — what `twin_pin.py` covers, and what it deliberately does not

Read this before citing the control. Its verdict is narrower than *"the twin is correct"*,
and the gap is where the next instance of this defect will live.

## What it covers

| # | Section | What a `PASS` means |
|---|---|---|
| 1 | pin present | The twin names a `STATE.md` revision, and the row label sets in `STATE.md`, the twin, and the pin are the same set. |
| 2 | per-row digests | No `STATE.md` **ledger row** has changed since the twin was last reconciled. This is the load-bearing check. |
| 3 | whole-file digest | `STATE.md` is byte-identical to the pinned revision. Informational only — see below. |
| 4 | kind marks | Every ledger row carries the same `Kind` mark in both documents. Live; does not consult the pin. |
| 5 | default-deny guard | The twin does not call itself `Generated <date>`, and does not claim canonicity on a line that fails to name `STATE.md`. |
| 6 | visible ↔ machine pin | The header's human-readable provenance line quotes the same commit as the machine-readable pin. |
| 7 | the pin resolves | The pinned commit **exists**, is an **ancestor of an integration ref**, and **carries the `STATE.md` the pin digests**. |
| 8 | in-flight relocations | Any row section 2 subtracted was **declared**, has **actually moved**, and its deferral **has not expired** — i.e. no integration-reachable commit carries these `STATE.md` bytes yet. |

Section 3 **differs on nearly every run and that is not a defect.** `STATE.md` changes
constantly outside the ledger; if section 3 carried the verdict, the control would be red
permanently and would be ignored inside a week — which is precisely how `Generated
2026-07-19` survived three weeks. Section 2 carries the verdict.

## What it does NOT cover

**1. Whether an unmoved row is faithfully summarised. This is the big one.** The twin is a
*summary* rendering. Its cells are deliberately shorter than `STATE.md`'s — row 3b is **3,391**
characters in `STATE.md` against **829** in the twin, row 9 is **898** against **95** — so no
byte relation between the two exists or should. The control answers
*"which rows have moved underneath the summary?"*. It
cannot answer *"is the summary of this unmoved row true?"*. **A row that has never moved, and
was summarised wrongly on the day it was written, passes every section here.** Nothing short
of a reader comparing the cells will catch that, and this instrument does not pretend
otherwise.

**2. Anything outside the ledger table.** The twin has seven sections; only the `Full ledger`
table is digested. Its proof-chain prose, obstruction cards, and attempt index are
uncovered — and mg-957a's repair was of *nine aggregating sentences*, most of which live in
that uncovered prose. **The historically most common form of this defect is out of scope.**
Extending section 2 to named prose blocks is the obvious next move and was not done here.

**3. The `<i>`/`<s>` bypass in section 5, which is declared rather than closed.** A banned
string inside `<i>…</i>` or `<s>…</s>` is treated as a quotation of superseded text and
skipped. This exists because the repaired lede has to *say* what the false claim was, and
the first version of the guard failed that very repair. Wrapping a live claim in `<i>` hides
it from section 5. The cost to anyone doing that is that the claim renders in visible
italics as a quotation, which a reader can see; the same discipline `STATE.md` already uses
with `~~…~~`. It is a hole, it is on purpose, and it is written down here rather than
discovered later.

**4. Whether `--reconcile` told the truth.** `--reconcile` records that the twin's cells for
the named rows *were actually updated*. Nothing verifies that. It refuses to re-pin a row
that has not moved, and it refuses a blanket re-pin that does not name its rows — both of
which make a false reconciliation deliberate rather than accidental — but a caller who edits
nothing and re-pins anyway gets a green control over a stale page. **This is the single
easiest way to defeat the whole mechanism.** The defence is that the re-pin is a visible diff
in the commit that contains no corresponding change to the twin's ledger cells, which a
reviewer can see; that is a social defence, not a mechanical one.

**4b. Whether a DECLARED in-flight relocation actually reconciled the twin's cell.** Item 4
above, one level up, and it is the same hole for the same reason. Section 8 checks that a
declared row really moved in `STATE.md` and that its deferral has not expired. It cannot
check that the twin's *cell* for that row was rewritten — nothing can, for the reason in item
1: the twin is a summary and no byte relation to `STATE.md` exists. **A landing A that
relocates the row's essay, declares it, and leaves the twin's cell untouched is green here.**
The defence is the same social one item 4 names: the declaration is a new committed file
naming the rows, in a diff that either does or does not also touch those cells.

**5. ~~That the control is run at all.~~ CLOSED — `mg-724a`, recorded here `mg-188d`.** The
superseded text is kept struck rather than deleted, because it was the highest-value follow-up
this file named and the record of it being paid should survive: ~~*Nothing in this repository
invokes `code/rendered_twin_pin_9bc2/run_all.sh` on commit, on merge, or on any schedule. There
is no hook, no CI, and no gate — this was checked, not assumed. An instrument nobody runs is the
same artifact as a date nobody re-reads, which is the defect this ticket was filed about, one
layer up. Wiring it into whatever gate the repository grows is not done and is the highest-value
follow-up here.*~~ `./build.sh` at the repository root now runs this suite on every merge request,
through `code/control_gate_724a`, and the refinery is configured to fail the merge on a non-zero
exit — demonstrated by `mg-724a` blocking a real merge request in 19 seconds, not argued. What it
gates on is `BASELINE.json`'s declared fields, so read that file for what a green gate is actually
asserting; it is narrower than *"the twin is correct"* for every reason on this page.

**6. The COST of the two-landing protocol, which is real and is a choice rather than an
oversight.** Between landing A and landing B, `main` is RED for **every** branch, not only
the one that opened the protocol — section 8 grades `DISCHARGEABLE` the instant landing A's
bytes reach an integration ref. That is the construction `code/control_gate_724a/gate.py`'s
own §3 refuses for its `recorded` fields, *"a gate that fails for reasons its author cannot
act on is a gate that gets removed six weeks later"*, and it is taken here anyway on one
difference: **the author CAN act on it.** The remedy is one command, section 8 prints it in
the failure, it needs no knowledge of what landing A was about, and anyone may run it. The
three priced alternatives are worse:

- **Move `twin.worklist` in `BASELINE.json` instead.** One line, no red at all, and it never
  comes back — the field that makes the twin's exit code mean something would carry a
  permanent expectation that a published ledger row is drifted. That is laundering, and
  `mg-724a`'s `x1` exhibit exists to show what that field is load-bearing for.
- **Grade `DISCHARGEABLE` as a report rather than a red.** Then nothing whatever forces
  landing B, and the declaration is a permanent subtraction with better paperwork.
- **Leave the deadlock.** The row never moves. That is the state this mechanism was built to
  leave, and `docs/STATE-SPLIT-PROPOSAL-mg-14ad.md` §8.3 is the measurement of it.

**7. `--root` is a real bypass and is declared.** `twin_pin.py --root <somewhere with no git>`
makes sections 7 and 8 both answer `unknown`, which grades nothing. It exists because
reachability cannot be planted by editing a file and the three worlds that demonstrate
section 8 need a real repository; it moves the WHOLE question rather than narrowing it, and
`run_all.sh` never passes it. Section 8's `unknown` also **declines to honour** a declaration
rather than honouring it — so the one thing `--root` cannot buy is a quiet subtraction.

## The instrument's own defects, all three caught by running it

Filed because a repair is an artifact of the same kind as the defect it repairs, so it is
subject to that defect, and all three of these are that. **Every one was found by running
the thing, not by reading it** — which is the argument for the instrument existing at all.

- **`run_all.sh` laundered a `DRIFT` verdict into `CLEAN`.** The first version piped both
  commands through `tee`, so `$?` was *tee's* status and never the instrument's. It printed
  `control exit : 0 … CLEAN — the twin's pinned ledger rows all still match STATE.md` over a
  control that had exited 1 naming two drifted rows. **A runner that cannot report its own
  instrument's failure is the same artifact as a date nobody re-reads**, one layer in. Now
  redirect-then-`cat`; POSIX `sh` has no `PIPESTATUS`.

- **Section 5 was blind to the exact string it was written for.** The first version matched
  the raw line against `/\bGenerated\b\s+20\d\d-\d\d-\d\d/`, and the twin's own markup is
  `<span><b>Generated</b> 2026-07-19</span>` — the tags sit between the word and the date, so
  the guard never fired on the one claim this whole ticket is about. The scan now runs over
  tag-stripped text. **A guard against a false claim, blind to that claim, in the file the
  ticket names.** Only a live run found it.
- **The pin's own `state-sha256` field never parsed.** The field-name pattern was
  `[a-z-]+`, and `state-sha256` contains digits, so section 3 compared the actual digest
  against the empty string and printed `DIFFERS` — the right answer for the wrong reason,
  which would have kept printing the right answer after `STATE.md` stopped moving.

## Two more of the instrument's own defects, found at the first reconciliation (mg-2f44)

The three above were found by *running* the instrument. These two were found by **using it
for its purpose** — reconciling a row and re-pinning it — which is a different event and had
never happened before. Both are the same defect in two places: **a fixture that hardcoded
the one thing the instrument exists to let change.**

- **`negative_control.py`'s section-6 mutation had a one-use lifetime.** It read
  `text.replace("@ 276aead1a8c5 (2026-08-07)", …)`. The moment `--reconcile` moved the pin to
  a new commit, the search string matched nothing, the mutation became a no-op, and the
  harness scored it `SETUP FAILED` — **which is the harness working**, and is why this one was
  visible. It now reads the commit out of the file with a regex, so it survives every re-pin.

- **The positive control could not fail, and did not fail when it should have.** This is the
  serious one, and nothing reported it. The baseline assertion was

      ok = (code == 1 and "rows 8 and 9" not in out and "8 9" in out
            and "STRUCTURAL" not in out)

  where `"8 9" in out` was meant to say *the drift worklist is exactly rows 8 and 9*. It is a
  substring test against the **whole report**, and section 1 prints
  `PASS  all three row sets agree: 1 2 3a 3b 4 5 6 7 8 9 10 11` on every healthy run — so
  `"8 9"` matched **there**, unconditionally, forever, whatever had actually drifted. When
  mg-2f44 reconciled row 9 and the true worklist became `8`, the baseline still scored
  `CAUGHT`. **The positive control is what licenses reading every other row of the table**, so
  a baseline that cannot fail is worth more than any single mutation it guards — and it is
  `run_all.sh` laundering a `DRIFT` into `CLEAN` a third time, in the file written to catch
  that class. It now parses section 2's worklist **line** and compares the row list
  **exactly**, against an expectation **derived from the pin** rather than typed in — so it
  neither rots at the next reconciliation nor passes on a coincidence. Demonstrated to
  discriminate: the correct set scores `CAUGHT`; `['8','9']` (the stale literal), `[]`, and
  `['3b']` all score `HOLE`.

## Six more, found by mg-9876's audit of how this directory's controls get VALIDATED

The three above were found by *running* the instrument; the two before this by *using* it. All
six below were found by a third event again: **running every arm against an input in which the
thing it names has stopped happening, and requiring its report to move.** Each was
demonstrated red before it was repaired, and the transcript of that run is committed at
`code/control_audit_9876/out_a2_discriminate_PREREPAIR.txt`.

- **`run_all.sh` printed `CLEAN` over a control that never ran.** Exit 127 matched none of its
  branches and fell through to the green. **This is the fourth instance of instance 1, in the
  file rewritten to remove it.** Removing the `tee` fixed *whose* exit code was read; it left
  standing the deeper error, that a python process exits 1 both when the control finds drift
  and when it dies in a traceback. Renaming `STATE.md`'s ledger header was demonstrated making
  this script report a traceback as `DRIFT, and the instrument demonstrably fails when it
  should`, at **exit 0**. The runner now requires the control to have printed a `VERDICT` line
  before any branch is taken, refuses an exit code outside `{0,1,2}`, and refuses a DRIFT whose
  worklist is empty.

- **Section 5 exempted every line containing `<!--`.** The skip was
  `if L.PIN_START.split()[0] in line` — that token is `<!--`, so an ordinary HTML comment
  anywhere on a line hid the whole line from the guard, and a live
  `<!----><span><b>Generated</b> 2026-08-10</span>` was demonstrated walking past. It was also
  *too narrow* for its stated job: only the pin block's first line carries `<!--`. An
  undeclared bypass, wider and narrower than the thing it named at once. Now a line range.

- **Section 6 was a substring test.** `pinned_commit in shown` against the whole visible line —
  smell #1, inside the arm added to check a *duplicated* provenance string. A pin commit
  truncated to four characters **passed**. Now the commits are parsed out of the line and the
  list compared exactly, which also catches a visible line naming a second revision.

- **Section 3 could not tell a moved `STATE.md` from a pin carrying no digest.** Deleting
  `state-sha256` made it compare against the empty string and print `DIFFERS`, the same word
  it prints on ordinary runs, under a heading that says `DIFFERS` is not a defect. The
  ancestor of this is two entries above: the field-name **pattern** was repaired and the
  **absence** never was. Absence is now its own check at structural grade.

- **The ledger could gain a column and every arm stayed green.** `row_digests` joins four cells
  *by name* and `parse_state_ledger` refuses only *fewer* than five, so a sixth column added to
  the header and all twelve rows left section 2 byte-identical. The pin now records the column
  list its digests were taken over. Digesting the whole raw row would have moved every pinned
  digest and forced a re-pin nobody reconciled — the one move this instrument forbids.

- **`run_all.sh` named rows 8 and 9 as literals in its own prose**, one file away from the rule
  below, and the sentence was already half wrong. The worklist is now read out of section 2.

**And the practice fix, which is worth more than the six.** `negative_control.py` now takes the
**unmutated** report first and requires every mutation's `expect` string to be **absent from
it**; a string already present scores `UNFALSIFIABLE` and takes the harness non-zero. That is
mg-2f44's repair generalised from the one arm it fixed to all sixteen. The earlier repair
parsed section 2's worklist line for the positive control and did not ask whether the other ten
rows had the same defect. They did not — measured, not assumed — but nothing would have said
so, and nothing would have said so about the eleventh.

**The rule these two produce, stated so it is a rule and not a lesson:** nothing in
`negative_control.py` may name a pinned commit or a drifted row as a literal. The drift set
and the pin commit are precisely what every reconciliation moves; a fixture that spells them
out is a check with an expiry date, and the second one above shows it can expire **silently**.

**Still uncovered, and mg-2f44 did not change it:** everything under *What this does not
cover* above stands unedited. In particular **(2)** — only the ledger table is digested — is
why row 9's repair could be checked but the three **prose** paragraphs mg-2f44 also synced
(the summary, the machinery set, the fork) could **not** be. Those were reconciled against
`STATE.md:13`/`:76`/`:81` by hand and by reading, and **no control saw them**. And **(4)**
stands at full strength here: this reconciliation's claim that row 9's cell was actually
updated rests on the diff being visible in the same commit, which is a social defence.

## Five more, found by the FIRST CLEAN RUN — a fourth event again (mg-188d)

The first three above were found by *running* the instrument, the two after them by *using* it to
reconcile one row, and the six after those by mg-9876's audit of how the arms get validated.
These five were found by a fourth event, which had never happened: **the control going GREEN.**
Rows 8 and 9 had been drifted since the pin was seeded, so `section 2 clean` was a state this
directory had never been in, and five separate things turned out to depend on it never happening.
mg-188d reconciled row 8 — establishing what `STATE.md` says, rewriting the twin's row-8 cell,
and re-pinning in the same commit — and all five fired at once.

- **The runner printed its worklist line ONLY in the DRIFT branch.** `run_all.sh` emitted `The
  worklist, READ OUT OF SECTION 2 rather than typed here: …` inside `if [ "$CONTROL" -eq 1 ]` and
  nowhere else, so the field existed exactly while the twin was broken and vanished the moment it
  was fixed. mg-724a's merge gate reads that field by exactly-once anchored match — 0 matches is
  `REFUSED` — so **the first clean twin took `./build.sh` to `GATE VERDICT: REFUSED`, exit 2, and
  would have blocked the merge with a message saying the GATE was broken rather than that the twin
  was clean.** Measured on mg-188d's branch before it was fixed. **It was not fail-open, which is
  exactly why it would have survived**: the merge still failed. A gate whose load-bearing field is
  observable only in the failing state cannot report its own success. The line is now printed on
  every run, `(none)` for the empty set, and `lib724a` reads that token.

- **Section 3 graded an exit code its own four following lines say is not a defect.** It ran
  `worst = max(worst, 1)` on `DIFFERS` while printing *"This alone is NOT a defect and must not be
  read as one … section 2 is the check that carries the verdict"*, which this file says twice more.
  The contradiction was **unreachable** while section 2 was never clean. Once it was, it became
  what the *next* `STATE.md` landing produces: one appended comment line took the control to exit
  1 with an EMPTY worklist, the runner's DRIFT branch printed a verdict naming *"section 2's
  worklist"* over a section 2 that had named nothing, and exited **2 BROKEN**. So the first clean
  twin would have made this repository's merge gate red-broken for the next author to touch
  `STATE.md` at all, prose or ledger, for a reason they could not act on. Section 3 now reports and
  does not grade; a missing or malformed digest is still structural.

- **mg-9876's arms `R1`-`R4` borrowed a drifted row from the live tree.** `_moved_row` returned
  whatever happened to be drifted and `None` when nothing was; row 8 made `None` unreachable, so
  four arms came back `SETUP FAILED  TypeError: … not NoneType` the instant the subject was fixed
  — **four arms of the auditor destroyed by the audit succeeding**, which is the shape recorded two
  sections above about that instrument's own selftest, arriving a third time in the arms nobody
  re-read when the first two were repaired. The drifted row is now CONSTRUCTED when absent, from
  one pinned digest overwritten with another pinned digest — derived from the captured bytes, so it
  cannot rot at the next reconciliation the way the thing it replaces did.

- **mg-9876's arm `C3` was repaired, and re-baselining it at 0 would have been the wrong fix.**
  C3 scored `UNFALSIFIABLE` because section 3 says `DIFFERS` on nearly every run, so its predicate
  was already true on the good input — a standing finding, gated by mg-724a at
  `audit.arms_not_shown = 1` precisely so its repair would be deliberate. mg-188d's reconciliation
  made C3 discriminate **by accident**, because `STATE.md` happened to be byte-identical to the new
  pin, and 0 would then have been a dated reading about whether the corpus was still — red at the
  next unrelated edit. C3's good side now re-points the sandbox pin's `state-sha256` at the
  sandbox's own `STATE.md`, which is C2's own documented rule applied to the arm it had not been
  applied to, and 0 was **demonstrated stable**: 50 of 50 arms discriminate with `STATE.md`
  byte-identical to the pin and with a line appended to it.

- **mg-724a's own mutator was a substring replace, and its `E2` typed the value it expected.**
  `_set_str` ended `m.group(0).replace(m.group("v"), new, 1)`, so flipping the `0` of `0 not;` in
  `VERDICT: 50 arms probed, 50 shown to discriminate, 0 not;` landed on the `0` inside `50` and
  mutated a *different field* than the one the probe scores — probe `T6` went `HOLE`. It had agreed
  with the correct rule for as long as the numbers happened to line up. `E2` planted exit `0`
  against a description reading *"where the baseline says 1"*, and came back `SETUP FAILED` the
  moment the audit suite stopped being red. Both are the rule stated at the top of that file —
  nothing may name as a literal the thing every landing moves — not applied inside it. Now
  span-replacement and a planted status derived from the observed one.

**What this does NOT change.** Everything under *What this does not cover* stands. In particular
**(1)** — a row that never moved and was summarised wrongly passes every section — is why mg-188d
also rewrote the twin's L1b card and its lede **by reading**, and **(2)** is why the `(A) SPREAD`
strike it landed in the machinery paragraph is invisible to this control: **the pin digests the
ledger table only, and three of mg-188d's four twin edits are prose that no section here sees.**
**(4)** stands at full strength: that row 8's cell was actually rewritten rests on the diff being
in the same commit as the re-pin. **(5) IS NOW CLOSED and was the highest-value follow-up named
here:** `./build.sh` runs this suite on every merge request, via `mg-724a`'s gate.

## Section 7 arrives, and it closes a hole this file could not see (mg-7cc3)

`twin_pin.py` gained **section 7** — the only section that asks git anything. mg-3902 found the
hole, wrote the check as a separate suite because the fold was blocked, and filed the fold as
its successor; this is that successor.

- **The hole, stated as the shape rather than the instance.** Section 3 checks the pinned
  digest against the LIVE WORKING TREE and section 6 checks the pinned commit against a VISIBLE
  COPY OF ITSELF. **Neither of the two provenance fields was ever compared against the thing
  they claim to describe.** Setting both copies to `deadbee` was measured leaving this control
  at `VERDICT: CLEAN`, exit 0 — an unfalsifiable provenance claim shipped inside the instrument
  built to remove unfalsifiable provenance claims, which is `Generated 2026-07-19` one layer
  down.

- **EXISTENCE, ANCESTRY AND BYTE-IDENTITY ARE THREE DIFFERENT QUESTIONS.** The live bad pin,
  `c308368`, **resolved**: a section 7 asking only "does this commit exist?" would have gone
  green on the exact input that motivated it. Ancestry is asked first and reported first; the
  digest is a consequence and reporting it first sends the reader off to regenerate a digest
  when the pin itself is what is wrong.

- **The root cause was in `reconcile()` and is now refused rather than detected.** It stamped
  `rev-parse --short HEAD` while digesting the working tree. The refusal costs **two commits
  instead of one**, and it is the only guarantee available that the revision a pin names and
  the bytes it digests are one revision.

- **What section 7 still does not cover.** It cannot tell you the pinned revision is the RIGHT
  one to have pinned — only that it exists, integrates, and carries what the pin says it does.
  A reconciliation that re-pins at a commit whose `STATE.md` is byte-identical but which is not
  the revision the twin's cells were read from is invisible here, exactly as **(4)** above is
  invisible: the pin records that the cells WERE updated and cannot verify it.

- **`unknown` is a fourth world and not a fifth kind of red.** A tree with no repository — an
  export, a tarball, a probe's sandbox — is REPORTED and not graded. That branch exists because
  the same defect has now been written twice in this arc: mg-9876's `S1`/`S2`/`S3` (*"`ROOT` was
  not a git repo and three arms were condemned by one line"*) and then mg-3902's first draft of
  this very check. Reading that it exists did not stop it being written again, so it is built
  in — `lib9876.make_sandbox(history=False)` keeps the world reachable.

### One thing mg-7cc3 added that NO arm scores, named rather than left to be found

`reconcile()`'s **choice of which commit to name** is not an arm and cannot be, by this
lineage's own definition: an arm is a place that can say NO, and choosing a commit says
nothing. Arm `R5` covers the refusal beside it; the *selection* — prefer the newest
integration-reachable commit carrying these exact bytes, fall back to `HEAD` with a warning —
is covered only by a hand-run measurement, recorded in `README.md`'s table of runs.

**Why the sandbox cannot probe it**, stated so the gap is a fact and not an oversight: in
mg-9876's sandbox `HEAD` *is* `main`, so both branches of the choice return the same commit
and the two cannot be told apart there. The measurement that does tell them apart builds a
branch commit on top of `main` by hand. **If that selection silently regressed to
`rev-parse --short HEAD`, nothing in the gate would say so** — what would eventually say so is
section 7, on the next reconciling branch, reporting `IN FLIGHT` where it now reports `PASS`.
That is a real detector and it is one merge too late.

## Section 8 arrives, and it is a DEADLOCK being broken rather than a hole being closed (mg-1344)

Every previous section on this page was added because something could go wrong and nothing
would say so. **Section 8 is the opposite case: nothing was wrong, and something correct
could not happen.** `docs/STATE-SPLIT-PROPOSAL-mg-14ad.md` §4 budgets the `Full ledger`
section **2,887 → 600 words** by relocating four row essays. mg-927a landed every other line
of §4 and measured that this one **cannot land at all** — not "was not got to".

**The three facts, and each is individually correct.**

1. Moving a pinned ledger row grows section 2's worklist, and `twin.worklist` is a **gated**
   field in `code/control_gate_724a/BASELINE.json`. The row edit alone is RED.
2. `reconcile()` **refuses** while `STATE.md` on disk differs from `STATE.md` at `HEAD`, so
   the re-pin cannot share the row edit's commit. That refusal is `mg-7cc3`'s repair of
   `mg-3902`'s root cause and its own comment says *"THE COST IS TWO COMMITS INSTEAD OF ONE."*
3. A re-pin one commit later on the same branch names a hash **the refinery's rebase destroys**
   — `pin_target()` finds no integration-reachable commit, falls back to `HEAD`, and prints
   its own warning. Section 7 grades the resulting orphan RED. `7e7bfb7 twin: point the pin
   at the commit that survives the rebase — 2fbd5ce did not exist after it (mg-cdd5)` is this
   repository's receipt that it has happened.

**WHICH OF THE THREE THIS CHANGES, AND WHY IT IS NOT LAUNDERING.** It changes **(1)**, and it
does not change it by making the gate quieter. A ledger-row relocation becomes two landings —
**A**: move the essay, reconcile the twin's cell, do not re-pin, and **declare** the row in
`IN-FLIGHT.json`; **B**: once those bytes are on an integration ref, `--reconcile --rows N`,
which now finds a main-reachable commit and passes section 7. A declared row is subtracted
from section 2's worklist, and **the subtraction is the entire risk**, so it is bought with a
predicate that expires without anyone deciding to let it:

> the declaration is HONOURED only while **no integration-reachable commit carries these
> `STATE.md` bytes** — i.e. only while landing B is *impossible*.

That predicate is `reachable_state_commit()`, **the same function `pin_target()` calls** to
choose which commit a re-pin may name. It is called, not paraphrased, so *"the gate honours
this"* and *"a correct pin can be made"* cannot become two answers. The consequence is the
point and it is the whole argument: **the moment landing A merges, its own declaration goes
RED, and it stays red until landing B lands.** A laundered field is green forever. This one
cannot stay green past the moment its excuse expires — measured in both directions against a
real git history, not argued (`negative_control.py`'s three planted worlds, and `a2`'s
`C8d`).

**What the gate sees.** `twin.worklist` is now the **undeclared** half and its baseline value
is **unchanged at `[]`** — deliberately, because moving *that* value is the laundering-shaped
edit. The declared half is a second gated field, `twin.inflight`, also `[]` today. A branch
that moves a row without declaring it is RED exactly as before; a branch that declares one
moves `twin.inflight` and `twin.verdict_grade` (`CLEAN` → `IN FLIGHT`) and says why in
`BASELINE.json`. The sum of the two fields is what `twin.worklist` alone used to be.

**`IN FLIGHT` is a fourth verdict word at exit 0, and the polarity is borrowed, not invented.**
Section 7 has always treated an in-flight **commit** as *reported, not graded* — grading it
would make the gate red on every correct in-flight reconciliation. Section 8 gives an
in-flight **worklist** the same treatment for the same reason. The exit code was never this
directory's classifier; the verdict word is, and `run_all.sh` now takes its closing sentence
from that word rather than from `$CONTROL`, because a runner that printed *"CLEAN — the twin's
pinned ledger rows all still match STATE.md"* over a tree where some demonstrably do not is
this directory's founding defect for the fifth time.

### Two fail-open paths this section shipped with, and how they were found

Neither was found by anything failing. They were found by **enumerating the ways the remedy
could exhibit the defect it remedies** — which is the rule this estate states and which is
skipped exactly when a fix demonstrably works, as this one did at the time.

- **Three different "git could not answer" routes returned the same value as "git answered,
  and the bytes are on no integration ref".** No work tree, no integration ref, and an
  unobtainable blob id all reached `reachable_state_commit() -> None`, i.e. `HONOURED`. The
  search not being *able* to run was reported as the search having run and come back clean —
  an unfalsifiable claim inside the arm added to keep a subtraction honest. The three routes
  are now enumerated and answer `unknown`.
- **`unknown` was going to be honoured, by copying section 7's polarity one line too far.**
  Section 7 reports and does not grade an unverifiable pin, because grading it would condemn
  a pin the *checkout* cannot check. Here the sign is inverted: the declaration's effect is to
  **remove** a row from the field the merge gate exists for, so honouring one whose expiry
  cannot be evaluated is a subtraction taken on trust — an export, a tarball or a shallow
  clone would silently honour any declaration at all. `unknown` now reports, grades nothing,
  and **does not honour**: the rows stay in the worklist. Arm `C8e` and world N29 are that
  half, planted rather than promised.

### And one the estate's own instruments found, in mg-1344's first run of them

Three, in fact, and none of them by reading:

- **The arm census REFUSED**, naming fifteen unregistered arm-shaped sites this branch had
  added. That is `a1_census`'s stated purpose — *"when somebody adds a seventh section to
  `twin_pin.py` and does not register it, the census refuses instead of quietly reporting a
  stale 38"* — met by a branch adding an eighth. Fifteen arms are now registered.
- **`a2`'s runner probes went LAUNDERED for H3, H4, H6 and H7.** The stub `twin_pin.py` those
  probes substitute prints only a VERDICT line, so the runner's new `declared in-flight rows`
  refusal (arm H8) fired in *every* world and both sides exited 2. The stub is the control's
  **contract** with its runner and the contract grew a line; it now carries it.
- **`a3`'s planted world P5 rotted.** Its injection point was two consecutive lines of
  `twin_pin.py` quoted verbatim, and the fourth verdict word landed between them. The harness
  scored `SETUP FAILED` rather than a pass — P4's own subject, working — and the fixture now
  derives its anchor by position. That is the *fifth* recorded instance in this arc of a
  fixture spelling out the thing that changes, this time in the file whose job is proving the
  auditor can fail.

## Section 8 is USED for the first time, and the first use found five things (mg-bdb0)

`mg-1344` shipped the protocol and deliberately did not exercise it; **`mg-bdb0` is landing A
of the first real relocation** — ledger rows `3b`, `6`, `8` and `11`, the last unlanded line of
`docs/STATE-SPLIT-PROPOSAL-mg-14ad.md` §4. Every one of the five below was found **by running
it**, and none of them is a defect in section 8 itself: they are the estate around section 8
assuming a world in which `IN-FLIGHT.json` does not exist — the assumption that was true on
every run until this one, and that nothing could have falsified until a declaration was real.

**This is the enumeration this file's own header asks for**: *a repair is an artifact of the
same kind as the defect, so it is subject to that defect.* Section 8's remedy exhibits it
squarely — a mechanism whose worlds are all planted cannot tell you what it does to a tree it
is actually in.

- **The negative control's sandbox did not carry the tree's own declaration, while its
  expectation did.** `inflight_text = fn("") if target == "inflight" else ""` built every
  sandbox WITHOUT `IN-FLIGHT.json`, and `expected_drift` subtracted the declared rows read from
  the LIVE one. Two different worlds scored against each other. With no declaration in the
  repository they agreed trivially and nothing said so; the moment one existed the **positive
  control** reported `worklist is ['3b', '6', '8', '11'], expected exactly (none)`, the runner
  exited 2 before printing its worklist line, and `mg-724a`'s gate answered **REFUSED**. Every
  arm's sandbox now mirrors the tree.
- **Fixing that alone would have made the positive control satisfiable by an instrument that
  had stopped reporting the moved rows at all.** In the in-flight world section 2 subtracts the
  declared rows, so the worklist line is absent and `want_rows` is empty — and a scorer that
  checked only that is `mg-2f44`'s `"8 9" in out` arriving by the one route section 8 opened.
  `score_baseline` now checks **both** of section 2's lines, against a declared set derived
  from the pin and the declaration rather than typed, and refuses any exit code but 0 for a
  wholly declared relocation.
- **The planted landing-A world inherited the subject's pin, so it was a clean world only
  while the subject was clean.** `build_protocol_repo` re-derived the whole-file `state-sha256`
  from `base_state` and did **not** re-derive the twelve per-row digests. Once four of the
  subject's rows differed from the committed pin, the "throwaway repository" contained five
  drifted rows with one declared, `This is the WORKLIST` appeared, and **the one world in that
  file that must pass** scored `HOLE`. The fixture now builds its own row digests and asserts
  the count.
- **The three planted worlds' expect strings stopped discriminating the moment this
  repository went in flight.** `HONOURED — REPORTED, NOT GRADED` is in the real tree's own
  report during landing A, so `mg-9876`'s guard correctly scored world A `UNFALSIFIABLE` — the
  guard working, on an arm with nothing wrong with it. Each world now requires its own
  `declared in-flight rows: 1` as well, the guard fires only if the **whole conjunction** is
  already true of the unmutated report, and `a2`'s `N27`-`N29` hand the bad side the whole
  conjunction. Three arms had gone `LAUNDERED` in between; that is the fix being checked by the
  thing it changed.
- **`make_sandbox()` copied `IN-FLIGHT.json` into a sandbox it then commits to `main`.**
  `run_control` already refuses to let section 8 fall back to the REAL declaration —
  mg-1344's own *"a sandbox that reads one file out of the tree it is isolating"* — but the
  copytree brought the same file INTO the sandbox where the default path found it anyway, and
  `_template()` commits the whole tree onto `main`. So the sandbox's `main` carried exactly the
  `STATE.md` the declaration defers a re-pin for, and section 8 graded it **`THE DEFERRAL HAS
  EXPIRED` by construction**. `N11`, `N13` and `N19` all went `UNFALSIFIABLE` on their own good
  side: three arms of the auditor destroyed by the subject being **mid-protocol** — the fourth
  time in this lineage a fixture has borrowed the subject's own state, and the second time it
  was the subject being *fine* rather than broken. The sandbox drops any inherited declaration;
  probes that need one plant their own.

**What is still NOT covered, and item 4b is now a live cost rather than a hypothetical.**
Landing A reconciled the twin's four cells and **nothing checked it** — the diff is the whole
of the evidence, exactly as item 4b says. What was offered in its place: `IN-FLIGHT.json` names
the rows, so a reviewer knows which four cells to read, and `docs/STATE-SPLIT-PROPOSAL-mg-14ad.md`
§8.3b tabulates what left each row and under which clause. That is a better pointer than item 4b
had, and it is still a social defence.
