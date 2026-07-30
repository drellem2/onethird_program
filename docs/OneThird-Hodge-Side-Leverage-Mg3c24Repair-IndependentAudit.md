# Independent audit — the mg-3c24 repair

**Work item:** mg-f922 (pre-filed in the same action as its parent, mg-e1d0).
**Object audited:** `bbe83b5` — *"CLOSE mg-3c24, dropped and recovered by the successor detector"* —
together with its evidence sibling `3756553`. Those two commits land mg-3c24's findings **F1–F4**;
mg-3c24 was the audit of `1e61031` (mg-a2bd's strike of ledger row `G″`).
**Audit instrument:** `code/hodge_leverage_audit_f922/` — `run_all.sh` → `out_audit.txt`, ~2.4 s,
49 checks, **0 refuted, 10 findings**, exit 1. Predicted exit code **1**, written before the run.
**STATE.md NOT edited. mg-3c24's mathematics NOT re-opened.**

---

## §1 — Verdict

**THE REPAIR IS REAL AND NOTHING RETREATED — and then it committed the defect it was repairing.**

Everything the landing says it did, it did. The false sentence is struck (quoted, not deleted, so a
reader can check what was struck). The enlargement **is** recorded at the three sites the landing
names, including the `STATE.md` cell where the row A5 is about is read. The four figures reproduce
exactly, from a route that locates both rows by different anchors. Nothing is hedged, nothing is
re-counted, `G″` is still struck and `G′` is still not narrowed. F3's restored wording is the right
one and agrees with §6.1 and ledger row `G′`. F4's second site is closed and the brief really does
have six items.

**The finding is what the disclosure hands the reader.** Its own framing sentence is *"a reader of
A5 must meet the **current** gap rather than the one it was opened with"*. The gap it then prints as
current is **−875**. In the tree the landing leaves behind it is **+755** — because the same commit
added 1 630 characters to the cell it was measuring. The figure was made stale **by the commit that
prints it**, at all three disclosure sites, and the accompanying claim that the sign has *flipped*
is now inverted. That is `1e61031`'s defect — *a number asserted in the commit that made it false* —
recurring inside the repair of that defect, one generation on.

It is not a matter of interpretation whether this was measured: **the landing's own instrument says
so.** Re-run at the commit it ships in, `verify_landing.py` exits **1** with **1 REFUTED**, against a
committed transcript recording **0**.

| | severity | finding |
|---|---|---|
| **A** | MODERATE | the one document that states A5 verbatim — mg-d39d's own audit — carries **no marker at all**, though this arc annotates audit documents in place and `1e61031` did exactly that |
| **B** | **MODERATE** | the gap printed as **current** (`−875`) is the gap at the landing's **parent**; the commit that prints it made it `+755`. Three sites, present tense |
| **C** | MINOR–MODERATE | and the sign claim inverts with it — *"flipped sign"* describes a gap that is positive; `+9 608` is `+17 023` |
| **D** | MODERATE | F3's condition is restored at four sites and **missing at two more**, one of them inside ledger row **J** itself, which credits **J alone** with exactly the conclusion F3 says J alone does not carry |
| **E** | MODERATE | the landing's committed evidence transcript does **not** reproduce at the commit it was committed in — 0 refuted committed, 1 refuted on re-run |
| **F** | MINOR–MODERATE | and it **cannot**: it embeds the sha it was run at, which is neither the landing nor the landing's parent — so *"regenerates byte-identically AT THIS COMMIT"* is false by construction. Its runner pipes into `tee`, so it exits 0 either way |
| **G** | MODERATE | H8's `+9 608` is not a re-measurement: neither it nor its `10 483` appears anywhere in the transcript H8 cites as the source of every figure in it |
| **H** | MODERATE | the commit subject is *"CLOSE mg-3c24"*; **F5 and F6 are not landed, not ticketed, and not named** in the landing's own list of what it deliberately did not do |

**0 BROKEN mathematics. 0 over-correction. Every finding is a claim a document makes about itself —
which is what mg-3c24 said of its own seven, and is now true of its repair.**

> ⚠️ **ANNOTATION ADDED 2026-07-30 BY mg-8e30, landing findings B, C, E and F of this audit.**
> Added in place, in the form `1e61031` used on mg-86a3's audit document, so that a reader who
> arrives at a finding meets its disposition — which is this audit's own finding **A**, applied to
> itself. **Nothing in this document is rewritten and no verdict is softened; the findings below
> stand exactly as filed.**
>
> | | disposition |
> |---|---|
> | **B** | **LANDED.** All three sites restate the cell-only gap from the **post-commit** state and say so at the figure. |
> | **C** | **LANDED.** The *"flipped sign"* / *"SIGN FLIPPED"* claim is **withdrawn** and is **not** replaced by the opposite claim — the correction restores no character-based claim in either direction. |
> | **E** | **LANDED.** `verify_landing.py` exits **0** with **0 refuted** and `out_verify.txt` is regenerated against the tree it ships in. |
> | **F** | **LANDED.** The transcript no longer embeds a sha: T1's live row reads the **working tree** and prints the word `tree`. `run_all.sh` redirects instead of piping into `tee`, captures the verifier's status and exits with it. |
> | **G** | **LANDED incidentally to B/C.** T1's chain table now carries a **row-history column** at every commit, so every figure H8 states is printed by the transcript H8 cites. |
> | **A, D, H** | **NOT landed. Open.** mg-8e30's brief is B/C plus the instrument and the general rule; A, D and H are named here so they are not read as closed. |
>
> **Two things measured rather than asserted, because this annotation would otherwise be the
> compliance claim this audit distrusts.** (1) The general rule is in `STATE.md` Appendix A as
> ***"A COMMIT THAT MEASURES SOMETHING IT ALSO MODIFIES MUST PUBLISH THE POST-COMMIT MEASUREMENT"***,
> and the figure GATE now **formats what it has just measured** and looks for that, rather than
> string-matching a frozen `−875`; a four-mutation negative control in the same file shows the new
> gate fires on exactly the edit that defeated the old one. (2) **This audit's own instrument still
> reports `F-B` and `F-C` when re-run, and that is expected rather than a repair that did not
> take** — `F-B` fires on `gap ≠ −875`, which is true of every tree from here on, and its
> site list is built by string-matching the struck wording, which now survives only inside the
> correction's **marked quotation** at §14 and as the historical figure in H8. That is near miss
> **(2)** of this audit's own §9, one generation on. `code/hodge_leverage_audit_f922/` is left
> **untouched** — it is the frozen record of what it audited, and its `out_audit.txt` is not
> regenerated.

---

## §2 — What could not be broken

- **The four figures**, re-derived from git with a row locator sharing **no anchor** with the
  landing's: `13 551 → 16 692` for the `STATE.md` cell across `1e61031`, against a **static
  `10 623`** for §14's copy, so the mismatch A5 reports went **`2 928 → 6 069`** — more than doubled,
  ×2.07. Both files are in that one commit.
- **The strike is not hedged.** `G″` is still struck through and still labelled FALSE AS A UNIVERSAL;
  `G′` is still explicitly *"true as stated"* and *"not rolled back"* at both the deliverable and the
  summary; no hedging verb was introduced anywhere near the strike (five forms searched, zero found).
- **Nothing was re-counted.** Every counterexample / strike / Theorem-G figure —
  `55 (poset, level)`, `3901 of 7989`, `48 846`, `405 posets`, `2748`, the four `n = 5` ordinal sums,
  `THEOREM G STANDS`, `PROVEN-by-computation` — occurs the **same number of times** before and after
  the repair, in both files.
- **F3's restored wording is the right one**, and it is the wording §6.1 and ledger row `G′` already
  carried: the base case `λ₂(F(A_m)) ≤ 1/2`, *"J alone does not give it"*, *"Theorem G gives only
  `≥ 1/2` in both directions"*, and — at the row — *"stays **computational** and is verified for
  `m ≤ 9`"*.
- **F4 is genuinely closed.** mg-a806's ticket has **six** numbered items, counted from the ticket
  itself; both live sites now say six and name all six correctly against it; neither still **asserts**
  four, and both keep the old wording as an explicitly marked *CORRECTED FROM* quotation.
- **F2 is genuinely closed.** §14 no longer carries an independent site count; it defers to §6's
  table, which still has three rows and still says *"Three"*.
- **The mg-2da3 landing control PASSES and its committed transcript regenerates byte-identically**,
  on 11 content digests and 11 presentation records. The `3756553` re-baseline is honest.

---

## §3 — Target 1(b): was the enlargement recorded where a reader of A5 meets it?

The brief's primary target, because the parent had to do two things and the second is the skippable
one. **It was done — at three sites.** Sweeping the tracked `.md` files for statements of A5 rather
than working from a list:

| file | states A5 | carries `2 928 → 6 069` |
|---|---|---|
| `STATE.md` (the cell A5 is about) | yes | **yes** |
| `docs/OneThird-Hodge-Side-Leverage.md` §14 | yes | **yes** |
| `docs/state-history/attempt-mg-a3d4.md` H8 | yes | **yes** |
| `docs/…-GppStrike-IndependentAudit.md` (mg-3c24) | yes | yes (it is the finding) |
| **`docs/…-StateLanding-IndependentAudit.md` (mg-d39d)** | **yes — this is where A5 is *stated*** | **no** |

### Finding A (MODERATE) — the document that states A5 carries nothing

mg-d39d's audit is where A5 exists as a finding: its summary table (*"**A5** | MODERATE | §14 asserts
the `STATE.md` row 'carries the same clauses'; it carries at least five it does not"*) and its §6. A
reader who follows A5 to A5 gets the finding as it was opened and **no indication that it was
enlarged, that it was audited, or that anything has been landed against it.** The file contains
`mg-3c24` zero times, `mg-e1d0` zero times, and no enlargement figure.

**This is an omission, not a convention, and that was measured rather than argued.** `1e61031` — the
commit under repair — annotated mg-86a3's audit document **in place**:

> **⚠️ ANNOTATION ADDED 2026-07-30 BY mg-a2bd — the cell's own text is left verbatim as the record of
> what this audit proposed; the proposed strengthening is FALSE.**

and §6's disposition table **counts that file as one of the three sites the strike touches**. The
practice exists, the landing's own F2 repair leans on the table that records it, and the one document
whose subject is A5 was not given the same treatment.

---

## §4 — Findings B and C: the figure a reader meets is not the current one

The disclosure's framing sentence, in `STATE.md`:

> **stated here because this is where A5 is recorded, and a reader of A5 must meet the current gap
> rather than the one it was opened with**

and then, three clauses later:

> **The current gap is not that number:** mg-34bf's restructure flipped the cell-only figure to
> **−875** …

| | at `6c0f0da` (the landing's parent) | in the tree the landing leaves |
|---|---|---|
| `STATE.md` cell | 9 748 | **11 378** |
| relocated row history | 10 483 | **16 268** |
| §14 copy | 10 623 | 10 623 |
| **gap, cell only** | **−875** | **+755** |
| **gap, cell + relocated history** | **+9 608** | **+17 023** |

### Finding B (MODERATE)

`−875` and `+9 608` are the figures at the landing's **parent**. The landing's own commit added
**+1 630** characters to the cell — it says so, prominently, in its own message (*"THE CELL GREW AND
THE GROWTH IS DISCLOSED"*, 8 440 → 10 070 stripped) — and that growth is exactly what moves the gap
off `−875`. So the number offered to the reader as *the current gap* was made stale **by the commit
that offered it**, and it is asserted in the present tense at **all three** disclosure sites:
`STATE.md`'s cell, §14, and H8.

### Finding C (MINOR–MODERATE) — and the sign inverts

The content of the disclosure is not merely a number but a claim about **direction**: *"the cell-only
gap has **flipped sign**"*, *"SIGN FLIPPED"*, *"the character metric no longer measures the
mismatch"*. In the tree the cell-only gap is **positive**, `+755` — the same sign it had when A5 was
opened. The **conclusion** drawn from it survives: A5 does now stand on clauses, **6 of 6** probed
clauses asserted by the row and by nothing in §14, and that reproduces. The premise offered for it
does not.

§14 additionally states: *"**Every figure in this paragraph is re-measured** from git and the tree by
`code/hodge_leverage_landing_e1d0/verify_landing.py` **T1**"*. T1, re-run, prints `+755` and
`+17 023` and marks the sign claim **REFUTED**.

**Why this is the same defect and not a near relative.** F1 is: *a commit asserted a figure about a
document while making that figure false, and nobody re-measured*. Here: a commit asserted a figure
about a document while making that figure false, and the instrument that would have caught it was
run against the pre-commit tree.

---

## §5 — Target 2: did the repair over-correct? No.

mg-3c24 found **0 BROKEN mathematics**, reproduced from a fully disjoint route, and concluded the
strike is right **for the right reason**. The risk on the other side is a repair that hedges.

Diffing `bbe83b5^` against the tree across `STATE.md` and the deliverable: **every** headline figure
occurs the same number of times; `G″` is still struck and still FALSE AS A UNIVERSAL; `G′` still
carries *"Do not weaken G′: it is true as stated"* and *"is **not** rolled back"*; five hedging forms
searched near the strike, zero found. The counterexample counts are not reopened and Theorem G is not
put in doubt at any site. **Nothing to report in this direction.**

---

## §6 — Target 3: F3's condition, at every site

The restored wording is correct and is the wording the body sites already carried. §6.1: *"**Given
`λ₂(F(A_b)) ≤ 1/2` for `3 ≤ b ≤ n`** — the computational half, verified for `b ≤ 9`"*. Row `G′`:
*"What stays computational is only the base case `λ₂(F(A_m)) ≤ 1/2`, `m ≤ 9`"*. Both `STATE.md`
summaries now agree with them, name Theorem J as insufficient alone, and state that **Theorem G gives
only `≥ 1/2` in both directions**. That is the right condition, restored as a **computational base
case**, exactly as the brief specifies.

The landing's instrument checks a **hard-coded list of four sites**, so it cannot see a fifth. This
audit sweeps the two live documents for the **conclusion** and asks, of each occurrence, how far away
the base case is:

| site | base case |
|---|---|
| `STATE.md` cell | **37 chars away** |
| `STATE.md` Appendix A tally bullet | **35 chars away** |
| deliverable §6.1 body bullet | **195 chars away** |
| deliverable §6.1 **heading** | **none within 900 chars either side** |
| deliverable **ledger row J** | **none within 900 chars either side** |

### Finding D (MODERATE) — and the sharpest instance is inside row J

Ledger row **J**, verbatim:

> **Two consumers:** it is why `G″` is false, and it is **the missing step in row `G′` (the max over a
> level is attained at the one-big-block face)**.

This is F3's defect in its purest form: the parenthesis credits **Theorem J** with the conclusion, and
F3's whole content is that J does not carry it — J gives that the one-big-block face is the only face
that *can* attain the factor's own `λ₂`, **not that it wins**, and Theorem G bounds only from below.
A reader who arrives at the ledger — the place a ledger is for — meets the unconditioned form.

The **§6.1 heading** (*"The second consequence: `γ_i` for `A_n` is attained at the one-big-block face"*)
is the weaker sibling: its body carries the condition 20 lines below. It is reported because this arc
has already had to repair a heading for exactly this reason — mg-a806's `0160cbf`, *"§9.4's heading
carried the falsified universal too"*.

**Both were introduced by `1e61031`** — the commit mg-3c24 audited — so these are misses of the same
sweep rather than new damage. But they refute the landing's own census, stated in H7 verbatim:

> Both the deliverable's §6.1 and its ledger row `G′` carry it; **only the two `STATE.md` summaries
> dropped it**, and both now carry it.

A repair that fixes the sites it was handed and states that those were the only sites is the shape
this arc keeps landing — F4, immediately below it in the same commit, is a repair being reported as
half-landed for precisely that reason.

---

## §7 — Target 4: counting the brief

mg-a806's items, read from the ticket rather than from anyone's description of it: **B1, B2, B3, B4,
B5, B6 — six.** B1 ledger row B6's falsification, B2 the stronger replacement scope sentence, B3 N1's
label, B4 the §10 table, B5 recording Theorem G's confirmation as prominently as the corrections,
B6 the Appendix A addition moved over from mg-8a12.

Both live sites now say **six** and name all six, each matching the ticket's own item. Neither
**asserts** four; both keep the old wording as a marked *CORRECTED FROM* quotation, which is the
strike-don't-delete convention the F1 repair also follows. The conclusion survives the recount at
both sites: `G″` is none of the six. B5 and B6 are verifiably landed (row **G**'s ✅ CONFIRMED block;
the Appendix A rule *"proving a property and testing for it are different operations"*), so the
landing's *"an under-count in the write-up and never an unlanded item"* holds.

**Nothing to report on F4.**

---

## §8 — Beyond the brief, declared: the landing's own evidence artifact

*The brief's list is a floor. The thing chosen, named nowhere in it: the artifact the whole landing
rests on. Chosen because the landing's central methodological claim is* **"EVERY NUMBER ABOVE IS
RE-MEASURED, NONE QUOTED … 30 checks, 0 refuted"** *— and that claim is one committed file.*

### Finding E (MODERATE) — the transcript does not reproduce at the commit it ships in

`code/hodge_leverage_landing_e1d0/verify_landing.py`, re-run at HEAD: **exit 1, 1 REFUTED**. The
committed `out_verify.txt`: **0 refuted**. The refuted line is T1's sign check — the same one behind
findings B and C, which is the point: **the landing's own instrument catches this, and the committed
run does not contain the catch.**

This is the defect class the *sibling commit in the same landing* exists to prevent. `3756553`, in
its own words: *"leaving it at the old figures would publish a control output that no longer
reproduces — the defect class this cluster exists to catch."* It regenerated the mg-2da3 control's
transcript and did not regenerate its own.

### Finding F (MINOR–MODERATE) — and it cannot reproduce, by construction

`run_all.sh` states: *"this transcript regenerates byte-identically **AT THIS COMMIT** (verified, two
runs)"*. The transcript's own T1 table prints the short sha of whatever commit it was run at, and the
committed copy prints **`a13b4a9`** — which is neither `bbe83b5` nor `bbe83b5^` (`6c0f0da`). A file
that embeds the sha it was run at cannot regenerate byte-identically at any later commit; the
statement is false the moment the transcript is committed, at every commit, forever.

`run_all.sh` also runs `python3 verify_landing.py | tee out_verify.txt` under `set -e`. A pipeline's
status is the **last** command's, so the runner exits **0** while the verifier exits **1**. Measured:
verifier 1, runner 0. The one line of the landing that would have surfaced findings B, C and E is the
line that cannot.

### Finding G (MODERATE) — `+9 608` was not re-measured

H8 prints `10 483` for the relocated history and `+9 608` for the combined gap, and closes: *"Every
figure above is re-measured from git and the tree by `verify_landing.py` **T1**; none is quoted from
mg-3c24, which matters here more than usual because the finding *is* that nobody re-measured a
number."* **Neither `9,608` nor `10,483` appears anywhere in `out_verify.txt`.** The transcript prints
`26,016` and `+15,393` — because it read the cell from git HEAD (pre-edit) and the history file from
the working tree (post-edit). H8's pair is the parent's history against the parent's cell. Three
figures, three different provenances, one commit, and the prose claims a single source it does not
have.

### Finding H (MODERATE) — four of seven, and the remainder is not named

The commit subject is **"CLOSE mg-3c24"**. mg-3c24's summary table carries **seven** findings, F1–F7.
The landing lands F1–F4 and closes with a section headed *"TWO THINGS THIS LANDING DELIBERATELY DID
NOT DO, named so they are not mistaken for oversights"* — which names (1) adding no new Appendix A
rule and (2) not landing mg-d39d's A5–A8. **It does not name F5, F6 or F7.**

F7 mg-3c24 itself declares *"needs no repair in the tree"*, so the live remainder is **F5** (the
*"exactly the posets where…"* quantifier gloss) and **F6** (the *"the repository was swept … three
sites"* census). Both are verifiably still in the tree unrepaired. **No ticket appears to exist for either** — every
item title across `available`, `claimed`, `pending` and `done` was searched, and the only three
naming mg-3c24 are mg-3c24 itself, mg-e1d0, and this audit. *(Titles only; a successor filed under a
title that names neither mg-3c24 nor its findings would not be found by that search, and this audit
did not read every body.)*

A landing that names two deliberate omissions and silently leaves two more is the *not-filed* shape
this landing was created to repair — mg-3c24 merged with findings and no successor. One generation
on, two findings narrower, and this time inside the paragraph written to prevent it.

---

## §9 — My own near misses

*A claim of compliance is cheap; a claim of non-compliance against yourself costs something. All
three are `REFUTED`/duplicate verdicts produced by the first version of the instrument, all against a
tree that was right. They are printed by `run_all.sh` as well as recorded here.*

1. **T5 windowed for the base case within a LINE.** §6.1's body occurrence sits in a bullet whose
   condition is ~90 characters earlier **in the same sentence**, split across a line break. The check
   scored it UNCONDITIONED — a false positive of exactly the kind this audit files against others, and
   it would have turned a 2-site finding into a 3-site one. Fixed by windowing the **flattened**
   document and printing the distance so a reader can judge *within reach* rather than take the
   instrument's word for it.
2. **T6 asserted that the string *"four things"* must be ABSENT**, and REFUTED on both files. Wrong:
   every survival is inside the correction's own marked *CORRECTED FROM* quotation — the same
   strike-don't-delete convention the F1 repair follows and which §2 above credits it for. An
   instrument that cannot tell an assertion from a quotation of a struck assertion files false
   findings. Fixed to test the assertion.
3. **T5 double-counted §6.1's heading**, once from the prose sweep and once from a separate heading
   pass, and would have reported four unconditioned sites where there are two distinct ones.

**And a fourth, structural, fixed rather than merely noted:** the first draft of this instrument
printed `git rev-parse --short HEAD` in its own T1 table — the exact construction of finding F. It
now prints the word `HEAD`, and `run_all.sh` states its reproduction contract in terms of the files
read rather than in terms of a commit. `run_all.sh` also does **not** pipe into `tee`; it redirects,
captures the status and exits with it. Both are one-line fixes to the artifact this audit criticises,
made here so the criticism is demonstrated rather than asserted.

---

## §10 — Actions, in order

1. **B and C** — re-measure and restate the current gap at all three sites, or drop the character
   figure entirely and let A5 stand on the clause probe, which is what the landing already concludes
   and which does reproduce. If the figure stays, it needs a gate that compares it against the
   measurement rather than string-matching `−875`.
2. **E and F** — regenerate `out_verify.txt` at the landing (it will show 1 refuted until B is
   fixed — that is the instrument working), stop printing HEAD's sha into it, and give `run_all.sh`
   the verifier's exit code instead of `tee`'s.
3. **D** — put the base case into ledger row **J**'s *"Two consumers"* parenthesis; the §6.1 heading
   is optional but has precedent. Then correct H7's census: it was four sites and two summaries, not
   two.
4. **H** — file the successor for mg-3c24's **F5** and **F6**, or record in the tree that they are
   open. The commit subject says CLOSE.
5. **A** — annotate mg-d39d's audit document at A5, in place, in the form `1e61031` used on
   mg-86a3's.
6. **G** — either re-measure H8's `+9 608` against the tree it ships in, or drop the sentence
   claiming every figure in it came from T1.

**NOT CLAIMED.** That any of mg-3c24's mathematics has been re-derived here — it was not, and
mg-3c24's own conclusion (0 BROKEN, reproduced from a disjoint route, the strike right for the right
reason, THEOREM G STANDS) is treated as established and was checked only for **disturbance**. That
mg-d39d's A2–A8 have been examined; they remain open. That row `G′`, row `G‴`, `A(P)`, the
counterexample counts or the `48 846` join links have been re-computed. Nothing here disturbs any of
them.
