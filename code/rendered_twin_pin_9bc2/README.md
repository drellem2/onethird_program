# mg-9bc2 — the rendered twin's pin, and the finding that it was never generated

`docs/state-of-the-wall.html` carried the words **`Generated 2026-07-19`** for three weeks.
This directory replaces that with something a reader or a control can check, and reports two
findings that are worth more than the staleness the ticket was filed about.

Run it:

```sh
sh code/rendered_twin_pin_9bc2/run_all.sh
```

## FINDING 1 — there is no generator, so `Generated` was false, not merely stale

The ticket said: *"Find the generator; if there is no generator and it was hand-built, SAY
SO — that is a more important finding than the staleness."* **There is no generator.**

- `git log --follow docs/state-of-the-wall.html` is **five commits**. The oldest, `29ffbf7`
  *"Initial: canonical State of the Wall"*, adds the twin and `STATE.md` **in the same
  commit**. The four after it are hand edits.
- mg-957a's commit message says so in as many words: *"the .html carried the identical false
  sentence verbatim, and fixing only the .md would have been this ticket's own failure mode
  in a second file."* That is a description of editing two files by hand.
- **Nothing in the repository writes the file.** The only three scripts that name it —
  `code/eps_spec_sweep_372e/s1_census.py`, `s2_classify.py`,
  `code/rate_sweep_910c/r2_classify.py` — all **read** it as a corpus member.

So the file **cannot be regenerated**, and this instrument does not pretend to. What it can
do is make the twin **name the `STATE.md` it is a rendering of** — mg-1abe's phrase, *a
publisher is not a pin* — and check that name per ledger row.

## FINDING 2 — the ticket's own premise about `STATE.md`'s size is stale

The ticket asks: *"STATE.md is now 4,658 words and readable, which was the entire problem the
HTML may have been solving. IF IT HAS NO REMAINING PURPOSE, DELETING IT IS A BETTER
OUTCOME."*

**`STATE.md` is not 4,658 words.** mg-ea0e's 32,772-byte executive summary landed at
`cc4c663` on **2026-08-06** and began growing back the same day:

| commit | date | bytes |
|---|---|---|
| `b80dea0` | 2026-07-30 | 186,710 |
| `cc4c663` | 2026-08-06 | **32,772** ← mg-ea0e |
| `f85a4e8` | 2026-08-06 | 34,573 |
| `d41d18c` | 2026-08-07 | 46,344 |
| `276aead` | 2026-08-07 | 66,038 |
| `641ef42` | 2026-08-10 | **110,640** |

**3.4× in four days, to 59% of the pre-restructure size, and 16,861 words against the
restructure's own `< 6,000` target.** The readability problem the twin exists to solve is
therefore *back*, which is the single most important input to the keep-or-delete question
and it points the opposite way from the ticket's framing. It is also a finding in its own
right, outside this ticket's scope: **the restructure had no ratchet**, so nothing held it.

## The recommendation: KEEP, pinned — do not delete

The ticket authorises deletion and this lineage has repeatedly found that removing a failure
mode beats adding a detector. **Here it does not, for three reasons:**

1. **The purpose the ticket assumed was gone is not gone.** See finding 2 — `STATE.md` is
   110,640 bytes and growing. Deleting the readable rendering on the stated ground that
   `STATE.md` is now readable would be acting on a premise that expired four days ago.
2. **Deleting is not the cheap side of the trade.** The twin's real cost is that every
   `STATE.md` ledger repair must be duplicated by hand, and that cost is now *measured and
   located* rather than discovered by audit: **2 of 12 rows**, named. That is a smaller
   standing cost than losing the only readable presentation of the program.
3. **The failure mode being removed is the unfalsifiable claim, not the file.** `Generated
   <date>` is gone, guarded against re-introduction, and replaced by a pin that fails.
   Deleting the file would remove the same failure mode, but so does this, at lower cost.

**What would change the recommendation:** if the reconciliation debt is not paid down — if a
later run reports more drifted rows than this one's two — the twin is being carried rather
than maintained, and deleting it becomes the better call. The control makes that a number
somebody can read instead of an impression.

## What was NOT done

- **The drifted rows were not repaired.** Rows **8** and **9** are reported, not fixed. Row 9
  is **mg-2f44**'s (`Depends: mg-9bc2`), and that ticket exists specifically to land it;
  fixing it here would silently close somebody else's item. Row 8 is a **second drifted row
  that no ticket names** — the twin's lede narrates it in prose, but nothing tracked it.
- **The twin was not regenerated**, because there is nothing to regenerate it with. Only its
  *provenance* claims were repaired (the header, the meta block, the footer).
- **No prose outside the ledger table is covered.** mg-957a's nine aggregating sentences live
  mostly there. See `COVERAGE.md` §2.
- **Nothing runs this automatically.** There is no CI, no git hook, and no gate in this
  repository — checked, not assumed (`.github` absent, `$(git rev-parse --git-common-dir)/hooks`
  has no non-sample entries). See `COVERAGE.md` §5; this is the highest-value follow-up.

## Files

| file | what it is |
|---|---|
| `lib9bc2.py` | ledger parsing (markdown + HTML), normalisation, digests, the pin format |
| `twin_pin.py` | the control (8 sections) and `--reconcile` |
| `seed_pin.py` | one-shot: seed the pin at `276aead`, the last commit that edited **both** files |
| `negative_control.py` | 26 arms — 23 mutations, each naming the section that must catch it, and three worlds built in a real throwaway git repository |
| `IN-FLIGHT.json` | **absent, and that is the normal state.** Section 8's declaration: the ledger rows whose re-pin is deferred to a second landing. Written by hand at landing A, deleted at landing B |
| `COVERAGE.md` | what the control does not cover, including its own two shipped defects |

## SECTION 7 — the one that asks git, added by mg-7cc3

Sections 1-6 shipped without ever asking git anything, and the gap has a shape worth naming:
**section 3 compares the pinned digest against the LIVE WORKING TREE, and section 6 compares
the pinned commit against a VISIBLE COPY OF ITSELF.** So the field whose own header calls
itself *"the only thing in this file that says which `STATE.md` it is a rendering of"* was
checked only against its own duplicate, and two copies of a string agreeing with each other is
consistency, not provenance.

**Measured, not argued (mg-3902):** setting **both** copies to `deadbee` — a commit that does
not exist — left this control at `VERDICT: CLEAN`, **exit 0**. It is now
`negative_control.py`'s row 16 and section 7 catches it.

**It was not hypothetical.** At `origin/main` on 2026-08-13 the pin named `c308368`, reachable
only from `origin/polecat-p0e8c`, whose `STATE.md` hashes to `3d8d56d0…` against the pin's
recorded `118158cb…`. mg-daba corrected that data; this section is the half that could not see
it. Both were owed and they were separate tickets.

### Reachability is checked BEFORE byte-identity, and the order is the point

`c308368` **resolves.** It is a real object. A section 7 that asked *"does this commit exist?"*
would go green on the exact pin that motivated it. And choosing on byte-identity first is what
produced the bad pin: *"which commit does this file reproduce at?"* returns one obviously
correct answer, and when that answer is off `main` you are then arguing yourself out of the
only candidate you found. Asking *"which main-reachable commits are eligible?"* first cannot
produce the bad pin at all. So an unreachable pin reports **NOT AN ANCESTOR** as the primary
fault and the digest is printed after it as a consequence.

| world | test | graded? |
|---|---|---|
| **integration** | an ancestor of `origin/main` (or `main`) | **GREEN** — both halves hold |
| **in flight** | an ancestor of *this* `HEAD` but of no integration ref | **reported, not graded** — the one legitimate way to name an unmerged commit, and still not done: **the refinery rebases**, so this hash is rewritten out of existence when the branch lands. `2fbd5ce` died that way at mg-cdd5 |
| **orphan** | an ancestor of neither | **RED** — `c308368` exactly |
| *unknown* | no integration ref resolves, or there is no repository here | reported, not graded — *"git cannot answer" is not "the answer is no"* |

**Byte-identity does not rescue an orphan, and that is demonstrated rather than argued.**
`a2_discriminate.py`'s C7b probe builds one with `git commit-tree` on `HEAD`'s own tree inside
mg-9876's sandbox: its `STATE.md` is byte-identical to the digest the pin records, and the arm
is red anyway.

## The root cause, repaired — `reconcile()` refuses, and then picks a better commit

`reconcile()` stamped `git rev-parse --short HEAD` while digesting the **working tree**. Those
are the same revision only while `STATE.md` is clean — and a reconciliation is exactly the case
where it is not, since the natural way to do one is to edit the `STATE.md` row, rewrite the
twin's cell and re-pin, all in one commit. Do that and **the pin names the revision before the
edit and digests the one after it.** Every reconciliation that touched `STATE.md` produced a
false pin, and nothing could say so.

Two changes, in that order:

1. **It refuses** while `STATE.md` on disk differs from `STATE.md` at `HEAD`, and leaves the
   twin unwritten. The cost is **two commits instead of one**: land the `STATE.md` edit, then
   reconcile the twin against it.
2. **It then names the newest commit reachable from an integration ref whose `STATE.md` is
   these exact bytes** — eligibility first, reproduction second. A twin-only reconciliation
   therefore never lands an in-flight pin again, which matters because section 7 now *grades*
   the orphan that a rebase would turn it into. When no such commit exists (the `STATE.md`
   change is on this branch and nowhere else) it falls back to `HEAD` and **says so**, loudly.

## Every claim above is a run, with its exit code

Nine measurements on this branch on 2026-08-13. The two rows pm-onethird named as this
ticket's acceptance demonstrations are the third and fourth.

| world | section 7 says | exit |
|---|---|---|
| the pin as it stands on `main` (`b364767`) | `PASS` on ancestry, `PASS` on the digest | **0** |
| — the same tree through the six-section control | there was no section 7 | 0 |
| **both copies set to `deadbee`** (mg-3902's measurement) | `FAIL  the pinned commit DOES NOT RESOLVE` | **2** |
| **both copies set to `c308368`** — a REAL commit, reachable only from `origin/polecat-p0e8c` | `FAIL  … REACHABLE FROM NOTHING THIS REPOSITORY INTEGRATES`, then the digest fault after it | **2** |
| an orphan built with `git commit-tree` on `HEAD`'s own tree, digest byte-identical | `FAIL` on ancestry, `PASS` on the digest — the discriminating case | 2 |
| a later, main-reachable commit whose `STATE.md` is not the digested one | `PASS` on ancestry, `FAIL  THE PIN NAMES ONE REVISION AND DIGESTS ANOTHER` | 2 |
| an **in-flight** commit: an ancestor of `HEAD`, of no integration ref | `IN FLIGHT — REPORTED, NOT GRADED, AND NOT YET ACCEPTABLE` | **0** |
| a tree with **no `.git`** | `REPORTED, NOT GRADED — no git work tree` | **0** |
| `--reconcile --rows 1` with an uncommitted `STATE.md` edit | `REFUSED: STATE.md on disk differs from STATE.md at HEAD`, and the twin was **not** written (checked) | 1 |
| `--reconcile` on a branch whose `HEAD` (`3c0c275`) is ahead of `main` (`ed7e3a9`) without touching `STATE.md` | `pinning at ed7e3a9, the newest commit reachable from \`main\` whose STATE.md is these bytes` — and section 7 then says `PASS … ancestor of \`main\``, where the old `rev-parse HEAD` would have left it `IN FLIGHT` and an ORPHAN after the rebase | 0 |

**Rows 7 and 8 are the ones that could have been red for a non-reason and are not.**

### What is NOT a standing control, named rather than left to be discovered

Rows 3-6 and 9 are arms: `a2_discriminate.py` runs each of them two-sidedly on every merge, so
they cannot quietly stop firing. **Rows 7 and 8 are not.** They are ungraded reports, so there
is nothing for an arm to score, and what is on the record for them is the measurement above and
not a check. mg-3902 put the objection best about its own version of this: *an escape hatch
nobody has watched open is the same unfalsifiable thing as a check nobody has watched fire.*
It has now been watched open, once, by hand, on 2026-08-13 — which is better than the
alternative and is weaker than the other seven rows.

## SECTION 8 — the two-landing protocol, added by mg-1344

**The problem was not that something could go wrong.** It was that something correct could
not happen. `docs/STATE-SPLIT-PROPOSAL-mg-14ad.md` §8.3 measured it: the `Full ledger`
section's **2,887 → 600 word** relocation *cannot land in a merge request at all*, because
three individually correct facts close on each other — the row edit alone turns the gated
`twin.worklist` red, `reconcile()` refuses to re-pin in the same commit, and a re-pin one
commit later names a hash the refinery's rebase destroys. `7e7bfb7` is the receipt.

**The remedy is two landings, and section 8 is what makes landing A green.**

| | what happens | what section 8 says |
|---|---|---|
| **A** | relocate the row's essay, reconcile the twin's *cell*, **do not re-pin**, and write `IN-FLIGHT.json` naming the rows | `HONOURED` — the rows leave section 2's worklist, the verdict word becomes `IN FLIGHT`, exit **0** |
| *(A merges)* | those `STATE.md` bytes are now on an integration ref | `DISCHARGEABLE` — **RED**, and red for every branch until B lands |
| **B** | `--reconcile --rows N`, delete `IN-FLIGHT.json`, return `twin.inflight` to `[]` | `PASS` on section 7 — `pin_target()` finds a main-reachable commit |

**The one thing that makes this a remedy rather than laundering** is that `HONOURED` is
decided by `reachable_state_commit()` — *the same function `pin_target()` calls* — so the
declaration is honoured for precisely as long as a correct pin is impossible, and not one
merge longer. `twin.worklist`'s baseline value in `BASELINE.json` is deliberately
**unchanged at `[]`**: an undeclared moved row is red exactly as before. See `COVERAGE.md`'s
section-8 entry for the full argument, the priced alternatives, and the declared cost.

### The protocol, measured end to end

Six worlds on 2026-08-13, three of them in a throwaway git repository built by
`negative_control.py` on every run, and three by hand in the same shape.

| world | section 8 says | exit |
|---|---|---|
| no `IN-FLIGHT.json` (the normal state) | `PASS  no IN-FLIGHT.json` | **0** |
| **landing A on a branch**: row 1 relocated, declared, `main` does not carry it | `HONOURED — REPORTED, NOT GRADED`, and row 1 is **absent from the worklist** | **0** |
| **the same declaration once `main` carries the bytes** | `DISCHARGEABLE … THE DEFERRAL HAS EXPIRED` | **2** |
| **landing B**: `--reconcile --rows 1` on that repository | `pinning at a1baf62, the newest commit reachable from \`main\`…`, and section 7 then `PASS` on ancestry **and** the digest | 0 |
| landing B done but `IN-FLIGHT.json` left behind | `FAIL  declares row(s) that have NOT moved` **and** `THE DEFERRAL HAS EXPIRED` — both directions force the file out | 2 |
| a declaration with no history to check the expiry against | `REPORTED, NOT GRADED, AND NOT HONOURED` — the rows stay in the worklist | 1 |

**The last row is the fail-open direction and it was nearly shipped.** Section 7 answers
`unknown` by reporting and not grading, which is right there; copied here it would have meant
an export or a shallow clone silently honouring any declaration at all, because the effect of
a declaration is to *remove* a row from the field the merge gate exists for. Not grading and
not honouring are the same doctrine at opposite signs. Arm `C8e` and world N29 hold it.

### What it costs on the merge critical path

**mg-724a's gate went 54.3 s → 110.1 s on this host**, measured from the committed
`out_gate.txt` on either side of the change and not from arithmetic: twin 4.9 → 9.7 s, audit
49.5 → 100.4 s. Fifteen new arms, each run **twice** by `a2_discriminate.py` with each side in
its own sandbox, is a few seconds an arm by construction. `.pogo/refinery.toml`'s timeout is
20 minutes, so the headroom is ~11× against the ~75× that file recorded at 16 s — a quarter of
what it was, which is the half of this that is a cost and not a purchase.

**One formatting repair came out of the same measurement.** `gate.py` printed its per-suite
timing as `%6.1fs`, which right-aligns, so `97.6s` carried one more leading space than
`100.4s`. mg-f771's normaliser rewrites the *number* to `<t>s` and cannot touch the padding
around it, so this line disagreed with its committed copy **across the 100-second boundary**
and the merge gate went RED for a wall-clock difference it had already declared to be noise.
Two consecutive runs here did exactly that. The fix is on the producing side; widening the
normaliser is the unfalsifiable escape hatch `lib_f771.py`'s own header refuses.

### What is NOT covered, in one line each

Landing A can declare a row, relocate its essay and **leave the twin's cell untouched** —
`COVERAGE.md` item 4b, and it is item 4 one level up rather than a new hole. ~~And the whole
protocol is **not exercised by any standing landing**: this branch ships the mechanism and
does **not** move the ledger row. The first real landing A is the successor, and until it
lands the six rows above are the only evidence — three of them re-run on every merge, three
by hand.~~

### The successor happened — mg-bdb0, 2026-08-13, and it is landing A for real

**`STATE.md` ledger rows `3b`, `6`, `8` and `11` are relocated and declared**, `IN-FLIGHT.json`
exists on that branch, `twin.inflight` moved `[]` → those four in `BASELINE.json` and
`twin.verdict_grade` `CLEAN` → `IN FLIGHT`. `twin_pin.py` reports **`VERDICT: IN FLIGHT`** at
exit 0 with section 8 **`HONOURED`**, `twin.worklist` is still `[]` and still means what it
meant. The six planted worlds above are no longer the only evidence.

**THE FIRST REAL USE FOUND FIVE THINGS, AND NOT ONE OF THEM IS IN SECTION 8.** They are all in
the estate *around* it — the negative control, its fixtures, and `mg-9876`'s sandbox — each
assuming a world in which `IN-FLIGHT.json` does not exist, which is what every run before this
one was. Two of them turned the merge gate `REFUSED` rather than red. `COVERAGE.md`'s
section-8-was-used entry has all five; the shape they share is that **a mechanism whose worlds
are all planted cannot tell you what it does to a tree it is actually in.**
