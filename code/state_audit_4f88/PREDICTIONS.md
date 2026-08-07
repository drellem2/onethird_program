# mg-4f88 — PREDICTIONS, committed BEFORE any content of STATE.md or of f85a4e8's diff is read

INDEPENDENT AUDIT of mg-2860 (the STATE.md leading-form correction).

Written and committed before I have read **one byte of STATE.md's body** at any
commit, and before `git show f85a4e8 -- STATE.md` has been run. What I have read
is listed exhaustively under EXPOSURES below; nothing there is laundered into a
prediction without being named as already-known.

## THE SHAs I AM AUDITING — named, per the dispatch instruction

| what | sha |
|---|---|
| worktree HEAD | `dafe75910f731927affdf366457d681e262acf62` |
| **STATE.md's last-modifying commit** | **`491d42c79f7628c18cb7a5d197faa9f4600cd6c1`** (mg-b488) |
| STATE.md blob at HEAD | `7f73bfc87b4bc4caab6c836f8c3922a2416863cf` |
| the parent under audit (mg-2860) | `f85a4e83e55fc0f0d36d8f060fddb9591d13ddd6` |
| the pre-edit file (mg-2860's base) | `f758468651b0d968c31e13147ea3e5234e8c5ace` (mg-ea0e's landing `cc4c663`… — resolved as f85a4e8^) |

The dispatch note said STATE.md was at `491d42c` and told me to audit the CURRENT
file and name THAT sha if it had moved. **It has not moved**: `git log -1 -- STATE.md`
is still `491d42c`, even though HEAD has advanced to `dafe759`. Both are recorded
above so a later reader can tell the difference.

## MY BRIEF IS WRITTEN AS IF THIS AUDIT RAN THE DAY THE PARENT LANDED. IT DID NOT.

This is my first framing correction and it is pre-registered rather than
discovered. My ticket says *"Read the **new first screen** as a stranger"*. There
is no such thing as "the new first screen" any more:

- **12 commits have modified STATE.md between `f85a4e8` and HEAD.**
- The file has gone **34,573 → 84,637 bytes** (175 → 209 lines) since the parent.
  It is 2.4x the size of the thing the brief describes.
- At least two of those 12 commits (`905526f` mg-325c, `05a0061` mg-c4f5) name
  mg-2860 in their subject and one of them repairs a defect it introduced.

So "the new first screen" is **two objects**, and a verdict that does not separate
them is uninterpretable:

- **(A) the parent's own edit** — what `f85a4e8` did to `f758468`. This is what
  checks 1/3/5 are literally about, and it is a frozen historical object.
- **(B) the file a reader meets today** — the blob at `491d42c`. This is what
  Daniel would actually open, and it is what the *purpose* of the brief is about.

**I will report every check separately for (A) and (B), and I will say which one
each finding lives in.** A PASS on (A) with a FAIL on (B) is a real and likely
outcome, and reporting only (A) would be the same "verdict describing a file that
no longer exists" failure the mayor's HOLD note was written to prevent.

## DECLARED DEFINITIONS — bound NOW, before I can tune them to a result

- **"first screen" = the first 40 physical lines of STATE.md.** I also record the
  first 4,000 characters as a second, wrap-independent cut, and will report both.
  I am not permitted to move this boundary after seeing where the condition sits.
- **"the condition"** = the statement that the constant form `1 - λ_std ≤ ε_spec`
  is confirmed **only conditionally**, because L4-as-stated may need an
  n-dependent modulus, and **if it does, the answer flips**. Both halves —
  *conditional* AND *what the condition is* — must be present for me to score it
  as carried. A bare "conditional" with no L4 is a HALF, and I will score it as
  a half, not as a pass.
- **"the mathematics moved"** = any change, in `f85a4e8`'s diff, to a theorem
  statement, a numeric figure, an inequality, a quantifier, or a ledger row's
  *status verdict* — as opposed to which form is stated first, or prose framing.
- **substring survival** is checked byte-for-byte with `grep -F`, and every
  "N occurrences" count is `grep -c` on lines with a stated `grep -o` occurrence
  count beside it where they can differ (mg-5ce3 was bitten by exactly this).

## EXPOSURES — what I already know before predicting (H1–H11)

These are **not** predictions. Naming them is the point; a "hit" on something in
this list is a reproduction and I will label it as such in the verdict.

- **H1.** I have read mg-2860's **entire ticket body** via `mg show`, including all
  four instructions verbatim, its condition paragraph ("IF L4 NEEDS AN
  n-DEPENDENT MODULUS, THE ANSWER FLIPS"), its two finite-n figures
  (`eps_spec <~ 2e-2`, crossover `n ~ 900`), its two named defect sites (the wall
  statement and the Axis 1 summary), and Daniel's two 2026-08-06 additions.
  **My checks 1 and 4 therefore test the parent against a brief I have memorised,
  which is a weaker test than a cold read and I say so.**
- **H2.** I have read the parent's **commit subject**: *"docs: STATE.md LEADS WITH
  WHAT THE ARCHITECTURE CONSUMES — a CONSTANT UNIFORM IN n, not the limit; and
  (LIB-weak) is on the board for the first time (mg-2860)"*. This **already
  answers** my check 2's "(LIB-weak) MUST BE STATED" in the affirmative. P4 below
  is a reproduction attempt, not a discovery, and scoring it as a hit would be
  laundering.
- **H3. A PRIOR AUDIT HAS ALREADY SCORED MY TARGET, AGAINST IT.** `05a0061`
  (mg-c4f5) states in its subject that STATE.md's *"row 8 CONTRADICTS ITSELF EIGHT
  WORDS APART (`closes this row as phrased` beside `does not supply the constant
  form this row leads with`), **introduced by mg-2860 when it rewrote the row's
  lead** and carried mg-c3ca's `as written` forward"*. So my check 3 ("the
  mathematics must not move… a mathematical change smuggled into it would be
  invisible") is **not** a first look: a defect introduced by this exact edit is
  already on the record, already repaired, and I knew it before I opened the diff.
- **H4.** The same subject states *"`never attacked by any arc` HOLDS, 0 of the 4
  pre-c3ca items among 2,360 having it as a deliverable"*. **My check 2b — "CHECK
  THAT FACT" against the corpus's history — has already been performed by another
  agent and I know its answer.** I will still run my own census, because my
  brief's whole premise is that the answer changes what mg-c3ca should do; but a
  confirming result is a REPRODUCTION of mg-c4f5, not independent evidence, and
  the only genuinely new information I can produce is (i) a different population
  or predicate, or (ii) an attack landing **after** mg-c4f5's census closed.
- **H5. A PRIOR AUDIT HAS ALSO SCORED MY TARGET, IN ITS FAVOUR.** `905526f`
  (mg-325c) subject: *"THE INVERSION WAS NEVER IN THE FILE — **mg-2860 refused
  it**, so error 1 of this ticket is STALE"*.
- **H6.** `a682e1d` (mg-d1a2) subject hands me check 4's arithmetic outright:
  *"it reconciles mg-33f5's 900C against this file's own 900 (**18C/eps_spec at
  eps_spec = 2e-2**, C >= 1, so >= 885 is a FLOOR)"*. 18/0.02 = 900. I have not
  yet checked where `18C` comes from and that is the part I can still test.
- **H7.** `4ef64d7` (mg-5ce3) subject names `ε_spec = 2×10⁻²` as **"the repaired
  ε_spec"** and `2×10⁻⁴` as **"the superseded one"**, and gives 6/ε_spec = 300.
- **H8.** My dispatch note tells me mg-131e **REFUTED** `eps_spec = 2/(n+1)` at
  n=6, that mg-b488 landed that refutation into STATE.md (`491d42c`), and that
  mg-372e is still correcting six source documents — so a live `2/(n+1)` in a
  *source* document is a known in-flight correction, not a finding. I am told to
  say where I saw it anyway.
- **H9.** I have measured, before predicting: STATE.md is 32,772 bytes / 175 lines
  at `f758468`, 34,573 / 175 at `f85a4e8` (**+1,801 bytes, +0 lines**), and
  84,637 / 209 at HEAD.
- **H10.** I have the full `git log --oneline` of STATE.md and the subjects of all
  12 intervening commits, several of which are very long and describe their own
  edits in detail. I have **not** read the file.
- **H11.** mg-b0ae was created **2026-08-06 00:32:43Z**; mg-2860 at **17:13:23Z**;
  my own item mg-4f88 at **17:15:28Z**. So mg-b0ae **predates** the parent by ~17h
  and check 5 is answerable rather than anachronistic. (I had feared the reverse.)

## PREDICTIONS

Probabilities are my honest credence now. I will score each HELD / REFUTED /
UNRESOLVED and keep the wording untouched.

### On the condition (check 1) — THE WHOLE RISK

- **P1 (0.90).** The condition is present **somewhere** in `f85a4e8`'s added text.
  *(Low information: instruction 2 of the ticket is emphatic and the parent's
  author read it. This is nearly a formality and I say so.)*
- **P2 (0.65).** The condition is present **on the first screen as I defined it
  above (first 40 lines)** at `f85a4e8`. This is the check that can actually fail:
  a diligent author satisfies instruction 2 by adding a paragraph *somewhere*,
  and "present" is much cheaper than "where the reader meets the claim".
- **P3 (0.45).** The condition is on the first 40 lines of the **CURRENT** file
  (`491d42c`). I am betting close to even. 12 rewrites of a file that grew 2.4x
  is a lot of opportunity for a qualifier to be pushed below the fold, and none
  of the 12 intervening commits' subjects mentions preserving it.
- **P3b (0.35).** The condition survives in the current file but **detached from
  the constant form** — i.e. both appear, but not within the same sentence or
  bullet, so a reader can meet the constant form without meeting L4. This is the
  failure mode my brief actually cares about and it would not show up in any
  presence test.

### On (LIB-weak) (check 2)

- **P4 (0.95, REPRODUCTION — see H2).** `(LIB-weak)` appears in STATE.md at
  `f85a4e8` and it was not there at `f758468`.
- **P5 (0.55).** The strength chain reads **exactly** `(B) ⟹ LIB ⟹ (LIB-weak) ⟹
  λ_std → 1` with all four terms present and in that order, at `f85a4e8`. I am
  genuinely unsure — briefs routinely name a chain in a tidier form than the file
  adopts, and this one has four named objects to get right.
- **P6 (0.80).** The phrase "never attacked" (or a byte-for-byte near variant)
  appears in STATE.md at `f85a4e8`.
- **P7 (0.75).** The "never attacked by any arc" fact **survives to the current
  file** at `491d42c`.
- **P8 (0.30).** My own corpus census finds an arc that **did** attack
  `(LIB-weak)`, contradicting mg-c4f5's `0 of 4`. Low, because H4 tells me the
  answer; I keep the bet because my population will differ (mg-c4f5's census was
  *pre-c3ca* items only, and 2,360 is not the corpus today).
- **P9 (0.60) — MY PREDICTED HEADLINE.** The real defect here is **not** that
  `(LIB-weak)` was attacked, but that **"never attacked" is true of the
  HYPOTHESIS and false of the IMPLICATION a reader will attach it to**. The
  corpus has attacked `(LIB-weak) ⟹ (LIB-const)` hard and twice — mg-325c found
  it rendered as a plain implication at four sites when it needs `n ≥ N₀`, and
  mg-c4f5/mg-5ce3 established **no N₀ works for the class**. If the file says
  "never attacked by any arc" near a chain that includes that implication, the
  page carries an unattacked-ness that is not true of everything in scope.
  *I am betting the sentence is locally true and globally misleading.*

### On the mathematics not moving (check 3)

- **P10 (0.80).** At least one change in `f85a4e8`'s diff is **not** purely a
  change of leading form. *(H3 all but guarantees this; the row-8 contradiction
  is one. I score a hit here as a reproduction unless I find a second, different
  one.)*
- **P11 (0.75).** **No theorem STATEMENT changed** — no inequality, quantifier or
  named constant moved. The parent's instruction 4 is explicit and the +1,801
  bytes / +0 lines shape (H9) is consistent with in-place cell edits, not with a
  restatement.
- **P12 (0.55).** At least one **ledger row's verdict/status cell** changed text
  in `f85a4e8`, beyond the row-8 lead. Row edits are how this file states things,
  so "leading form only" is hard to keep inside prose.

### On the finite-n numbers (check 4)

- **P13 (0.85, ARITHMETIC HANDED TO ME — see H6).** `n ~ 900` reconciles as
  `18C/ε_spec` at `ε_spec = 2×10⁻²`, `C ≥ 1`. What I can still test, and will:
  **where `18C` comes from**, and whether the file at either commit *states* the
  `C` dependence or prints a bare `900`.
- **P14 (0.55).** The file prints `n ~ 900` **without** its `C` and without the
  `18C/ε_spec` derivation at `f85a4e8` — i.e. the reconciliation mg-d1a2 later
  had to perform was necessary because the parent shipped a bare number. *(If the
  parent had shown the derivation, mg-d1a2's "two unlinked correct numbers for
  one threshold" would not have arisen.)*
- **P15 (0.50).** `2×10⁻²` is presented at `f85a4e8` **without** being marked a
  calibration — no "calibrated", "fitted", "not derived", or pointer to mg-6bc2
  at the site. My brief says this specific over-presentation is the risk. Even.
- **P16 (0.35).** `2×10⁻²` and `n ~ 900` were **not both added by `f85a4e8` at
  all** — instruction 3 ("while you are there") is the softest of the four and is
  the one an author under time pressure drops. If so my check 4 is vacuous for
  (A) and lives only in (B).

### On mg-b0ae (check 5)

- **P17 (0.35).** The parent's commit message **names mg-b0ae** and says it
  changed the first screen that audit was sent to cold-read.
- **P18 (0.30).** The parent's commit message names mg-b0ae **and dates it**.
  Dating is the half that gets dropped.
- **P19 (0.55).** mg-b0ae had **already completed** before `f85a4e8` landed
  (created 00:32Z, parent landed some time after 17:13Z — H11), in which case the
  hazard my brief describes did not materialise and the finding is that my own
  ticket's check 5 was worrying about a race that had already resolved. **This is
  a correction to MY brief, not to the parent's work**, and I pre-register it as
  such.

### Standing targets

- **P20 (0.30).** The parent reproduces its own defect class in mirror — the
  edit that stopped overstating now **understates**, e.g. by presenting the
  constant form as *merely* conjectural when it is confirmed-conditionally, or by
  demoting the limit and rate to the point where a reader cannot tell they are
  available and proven.
- **P21 (0.60).** At least one **bound word** ("at most"/"at least"/"≤"/"<",
  "uniform in n" vs "independent of n", "constant" vs "absolute constant") is used
  loosely at one of the two rewritten sites.

### MY TWO MOST LIKELY ERRORS, filed in advance

- **P22 — I attribute to mg-2860 a defect that a LATER commit introduced.** Twelve
  commits and a 2.4x size increase sit between the parent and the file I can read,
  and the temptation to read the current file, find a flaw, and score it against
  the parent is the single easiest mistake available here. **GUARD, bound now:
  every finding I state against mg-2860 must be exhibited in the output of
  `git show f85a4e8 -- STATE.md` (or `git diff f758468 f85a4e8 -- STATE.md`), and
  I must print the attributing commit for every finding about the CURRENT file.**
  No finding about (A) may rest on the current file's text.
- **P23 — I score a presentational contradiction as "the mathematics moved".** The
  row-8 defect of H3 is exactly this shape: a self-contradicting cell where
  neither half is a false theorem. My brief's check 3 asks specifically whether
  *mathematics* was smuggled in, and inflating a framing defect into a
  mathematical one would be this audit committing the over-claim it was sent to
  look for. **GUARD: a finding is scored "mathematics moved" only if I can name
  the object that changed (inequality / quantifier / figure / status verdict) and
  print both sides.** Otherwise it is filed as framing, explicitly.

### What I already expect NOT to do

- I will not re-derive L4, the master bound, or `(LIB-weak) ⟹ λ_std → 1`. This is
  a **presentational** audit by construction and I will say so rather than imply
  coverage I do not have.
- I will not re-run mg-c4f5's 101,658-poset check or mg-131e's dual certificates.
- Any statement I make about `2×10⁻²` being a calibration rather than a derivation
  is a statement about **how the corpus presents it**, not a re-derivation of it.
