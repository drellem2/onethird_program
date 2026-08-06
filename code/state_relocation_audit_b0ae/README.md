# mg-b0ae — INDEPENDENT AUDIT of the mg-ea0e STATE.md relocation

**Object under audit:** `cc4c663` (mg-ea0e), parent `78ae4d9`. Merged. `STATE.md` is unchanged
between `cc4c663` and HEAD — checked, not assumed (`out_b8_findability.txt` B8.2).

**Verdict: the relocation lost nothing.** 0 of 441 atoms of the old file are missing, 0 of 68
mg-ids are unreachable, 0 of 79 marker occurrences lost, 0 of 251 mathematical atoms altered,
and lines 1-129 carry the same SHA-256 on both sides. mg-ea0e's byte accounting reproduces.

**And one published figure of mg-ea0e's is wrong, in both places it appears.** It is a
bookkeeping total, it changes no acceptance decision, and it can be chased to exactly what
produced it. That is F1.

Run it: `bash code/state_relocation_audit_b0ae/run_all.sh` — eight sections, eight transcripts,
committed. The audited revisions are pinned in `libb0ae.py`, not read from HEAD, because HEAD
moves and the object under audit does not.

---

## The convention this suite is built on

**No count without its population and its grain.** `libb0ae.row()` raises if either is
omitted; a bare integer cannot reach these transcripts. That is not decoration — it is the
defect this lineage keeps finding, and F2 below is that defect appearing again, in the
audited work, in exactly the place the ticket predicted it would.

**Patch-id is not used anywhere in this audit.** 1 of 234 pairs in this arc has identical
content under different patch-ids, because a diff is a fact about a base as well as a tree.
The question here — did this text survive — is answered directly by byte-level presence, so
there is no reason to route it through an oracle that answers a different question.

**A negative needs an instrument that could have shown the positive.** Every "0" below is
printed beside a control that goes red. Withhold the largest destination file and 142 atoms
go missing and 14 mg-ids become unreachable; corrupt every atom by one character and all 441
go missing, all 79 marker contexts fail, all 251 mathematical atoms fail; ask for three
invented mg-ids and 0 are found. The instrument can see an absence. It did not see one.

---

## F1 — THE ORPHANED CORPUS FIGURE (the headline defect, and it is small)

mg-ea0e publishes an A1 acceptance row twice — in its commit message and in
`code/state_restructure_ea0e/README.md:48` — ending:

> Corpus total `245,161 → 261,318`

Its own committed transcript, `code/state_restructure_ea0e/out_verify_relocation_ea0e.txt:32`,
which its README says re-derives everything, prints:

> `corpus total, old: 276,707   new: 295,751   (+19,044)`

Neither addend matches. The other six figures in that same row (186,710 / 32,772 / 2,796 /
29,976 / 157,996 / +1,262) match the transcript character for character.

**It is chaseable, and it lands somewhere specific.** The two gaps are 31,546 old and 34,433
new — different numbers, which rules out a typo and a units error and points at a *population*
difference. Exactly one file in the transcript's own destination block has 31,546 as its
before-size and 34,433 as its after-size: `docs/state-history/README.md`. Remove it from both
sides of the transcript's pair and you get the published pair exactly
(`out_b7_orphan.txt` B7.1).

mg-ea0e's verifier totals the files whose size **changed**. `docs/state-history/README.md`
changed only because mg-ea0e itself edited it. **The published figure is a real measurement of
an earlier state of the same tree**, taken before that edit, carried into the final commit
message and README beside six figures that were re-derived at the end.

**What it costs: nothing, and I want to be exact about that.** The corpus row feeds one check,
"the corpus as a whole did not shrink". It passes under both pairs. No content claim, no
acceptance decision, and no other figure depends on it. What it costs is the property that
makes this arc's transcripts worth keeping: a number that can be chased to a producing
procedure. This one could be chased — and the chase ends at a run that is not the one shipped.

---

## F2 — THE MARKER COUNTS ROSE OVER A POPULATION THE CLAIM DOES NOT NAME

The ticket named this in advance: *the counts all went up, which is consistent with markers
being preserved AND with the corpus now including files that already had markers.*

It is the second. mg-ea0e's ten pairs (STRUCK 8→13, RETRACTED 0→2, … BROKEN 43→71) **all ten
reproduce**, and reproduce **only** over the TRANSITIVE CLOSURE of markdown links out of the
new STATE.md — 13 files. Over the one-hop corpus, 7 of 10 reproduce. Over a like-for-like
population — new STATE.md plus only the text this commit added — 2 of 10
(`out_b3_markers.txt` B3.1).

The clearest case is `RETRACTED 0 → 2`. Old STATE.md contains the word zero times. The new
STATE.md contains it zero times. Every file one link away contains it zero times. Both
occurrences are in `docs/state-history/README.md`, which is at **hop 2** and which this commit
did not touch. The row is arithmetically true and reports nothing about this relocation.

**mg-ea0e's A3 row calls its corpus "one link away".** Its verifier walks a closure. For the
ids that distinction happens to be empty — all 34 relocated ids really are at hop 1
(`out_b5_ids.txt` B5.1) — but for the markers it is not: three of the ten rows need a hop-2
file, and one of those rows is *entirely* hop-2.

**The safety claim survives anyway, and at a stricter grain than mg-ea0e used.** Counting
cannot distinguish "43 BROKEN preserved" from "43 deleted and 71 new ones arrived", so every
marker occurrence in the old file was matched individually by its own ±60 characters of
surrounding text: **79 of 79 survive** in new STATE.md or in text this commit added — the
like-for-like population, not the closure. Control: all 79 fail under a one-character
corruption (`out_b3_markers.txt` B3.2).

Read the **P2 column** of that table, not P4 or P5, for what a reader of the summary now sees:
STRUCK 2, REFUTED 3, BROKEN 11, RETIRED 0, CORRECTED 0. The corrections are reachable; most of
them are no longer *visible*. That is what a summary is, and it is the trade pm-onethird's
spec chose. It is worth stating plainly rather than leaving inside a rising count.

---

## F3 — THE SURPLUS: the explanation is right, and slightly too large

mg-ea0e explains its +1,262-byte surplus as each relocated row's retained sentence sitting in
both places. **Re-derived independently: those seven sentences total 1,346 bytes, all seven
confirmed present in both the row and its destination file** (`out_b1_bytes.txt` B1.4). The
stated cause is real and is *larger* than the surplus it explains, by 84 bytes — the residual
is a grain artefact of the two different decompositions, not a missing 84 bytes of text, and
the coverage census settles that independently at 0 missing.

I filed the opposite prediction (P1: the explanation under-explains) and it is a miss.

**The attack the ticket asked for, and its result.** A surplus can hide a loss offset by a
duplication, and the specific mechanism available here was real: the seven destination files
**pre-existed this commit** (mg-34bf built them from these same rows), so a search run at HEAD
can be satisfied by text that never moved. Measured: **0 bytes and 0 atoms** of the old file
are matched only by pre-existing text (`out_b1_bytes.txt` B1.3, `out_b2_coverage.txt` B2.1).
Every one of the 59 columns of the seven relocated rows is present in **its own** destination
file's added lines (B2.4). The disguise was available and was not used.

---

## F4 — THE MANDATE HELD, AND THE ONE PLACE JUDGEMENT LIVED

The brief gave three moves and no editorial latitude. Every line that left STATE.md was
charged to a move by its old line number: 126 to MOVE 1 (:180-381), 21 to MOVE 2 (:142-177), 7
to MOVE 3 (:130-136), and **0 from outside all three** (`out_b6_process.txt` B6.1). 27 lines in
the new file have no old antecedent: the 7 rewritten rows, the 14-line current-position
paragraph MOVE 2 explicitly permits, and 6 lines of link and provenance boilerplate. Both
self-reported departures check out: old :382-386 ("Why 1/3") is still in place, and row :133
does keep its second sentence and does carry the DISCHARGED it was kept for.

The one place a claim could have been invented is that composed paragraph. Its nine quoted
clauses: 5 match their source exactly, 7 after whitespace normalisation (STATE.md hard-wraps),
**9 after emphasis markup is also stripped** (`out_b6_process.txt` B6.2b). The two stragglers
are `*cancellation*` → `cancellation` and `**consume the frozen hypothesis directly**` →
plain. **The words are the source's words; the typography is not.** mg-ea0e's claim is that no
mathematical claim was reworded, and at the grain that claim is about — words — it holds. At
the grain of "verbatim quotation", two of nine are lightly re-typeset inside quotation marks.
I record it because it is the only distance between the source and the summary I could find,
not because it is worth fixing.

**And 0 mathematical claims were reworded anywhere**: all 251 mathematical atoms of the old
file survive character for character, control 251 of 251 (`out_b4_prefix_math.txt` B4.2).
**Lines 1-129 are byte-identical, not retyped** — same SHA-256 over the exact byte range, and
the longest identical prefix is exactly 129, located by the script rather than taken from the
claim (B4.1).

---

## F5 — THE RELOCATION DID NOT MOVE THE ANSWER. IT DELETED THE DISTANCE.

This is the ticket's §5, and it is the finding I did not expect.

**The reading, and its honest provenance.** I read the new STATE.md top-down and answered in
about 70 seconds of reading. I was **not** a cold reader: by then I had read :125-175 closely
while building B1-B7. I had **not** read :1-129 as prose — only hashed it. So the reading below
is of material I had not read, in a file whose shape I already knew. Discount it accordingly.

**The answer, from the file alone:** *Yes — it is the whole program.* A minimal counterexample
is primitive and frozen (`δ < 1/3`); Theorem E takes that to a low-conductance BK cut
(**proven, any width**); the easy/Buser direction bounds the gap by any cut (**proven**, ledger
row 5) and L3 says the best cut is a prefix (**empirical, 125/126**); a thin interface should
force a balanced pair (**L4, open, secondary**); a balanced pair contradicts minimality
(**proven**). The single open primary link is **L1b**: bad mixing ⟹ `λ_std → 1`, with
`(B) ⟹ LIB ⟹ λ_std→1` one-way. So: the Cheeger/spectral route exists, its easy direction is
proven, and the hard direction *is* the wall. Where I looked: the one-paragraph state (:11-13),
the mermaid proof chain (:49-70), the eight-row ledger (:74-90).

**Now the measurement.** Every one of those spans sits at **the same line number in the old
file** (`out_b8_findability.txt` B8). Of course it does — lines 1-129 are byte-identical. The
answer completes at :95 in both files. **The relocation did not move the answer one
character.**

So the retrieval failure of 2026-08-05 cannot have been caused by the answer being in the
wrong place, and cannot have been fixed by moving it. What changed is the denominator:

| | old | new |
|---|---|---|
| answer complete by line | :95 | :95 (identical bytes) |
| as a share of the file, by lines | 25% | 54% |
| as a share of the file, by bytes | **4%** | **24%** |
| bytes a reader passes *after* the answer | 178,729 | 24,791 |

A reader of the old file who found the answer had no way to know they had found it, because
96% of the document was still ahead of them. That is what 4% → 24% buys, and it is a real
buy — but it is a claim about *confidence that you are done reading*, not about *findability*.
**pm-onethird's framing, which I was asked to correct, is off here.** The spec's premise is
that the answer was buried and needed relocating. The answer was never buried; the 178,729
bytes *behind* it were. The three moves were the right moves for the wrong stated reason, and
the result is better anyway.

---

## Riders

**R1 — the blast radius nobody sized.** mg-ea0e discloses "line references outside STATE.md
were not rewritten" — honest, and not a measurement. Measured: **196 `STATE.md:<n>` citations
across 38 files; 67 of them now point past the end of the file**, against **0** for the same
citation set scored at `78ae4d9` (`out_b6_process.txt` B6.3). Split by whether the citing
artifact is still consulted: 45 citations in 12 **live documents**, 5 in 4 **live scripts**
(`face_geometry_audit_e720/verify_landing_claims.py`,
`hodge_leverage_audit_8a5c/audit_repair_8e30.py`, `state_layer_audit_218d/render218d.py`, and
mg-ea0e's own README), and 17 in 3 **frozen transcripts**, which are archaeology and are
supposed to be frozen. The live scripts are the ones that will now read the wrong line.
Out of scope for this ticket; noted, not fixed.

**R2 — the untouched prefix is why this is not worse.** 33 of the 196 citations point into
:1-129 and are safe by construction. Among them are mg-2de0's citations of `STATE.md:27` and
`:28`, filed one commit *after* the relocation and still resolving correctly.

**R3 — new STATE.md has 18 markdown links, 15 local, 0 dead** (`out_b6_process.txt` B6.4).

**R4 — the summary is already stale, and not because of mg-ea0e.** Of the five most recent
work-item ids on main, four are unnamed in STATE.md: mg-2de0 (which refutes mg-00b9's Lemma B
outer bound and lands *after* this commit), mg-00b9, mg-c3ca (which landed *before* `78ae4d9`
and was already unrecorded), mg-1abe. A file whose job is to be current is 4 landings behind.
Attribution matters: one of those four predates the object under audit, one postdates it, and
none of them is mg-ea0e's to have carried.

---

## Corrections to my own brief

The dispatch for this ticket states the shape change as **"29,125 words -> 4,658"**. Those two
numbers come from different instruments. `wc -w` gives 29,125 old and 4,660 new; Python
`.split()` gives 29,094 old and 4,658 new. mg-ea0e's own published pair (29,094 → 4,658) is
internally consistent and reproduces exactly; the brief's pair is `wc -w` on the left and
`.split()` on the right (`out_b1_bytes.txt` B1.1, which prints all four). The same brief's
"longest line 13,601 -> 1,772" mixes grains the same way: the old longest line is **13,367
characters** (13,601 bytes) and the new is **1,772 characters** (1,816 bytes) — characters on
one side, bytes on the other. Neither correction changes anything; both are the arc's own
recurring defect, arriving this time in the audit brief.

I disclosed 29,125 as a measurement in `PREDICTIONS.md` §0 and deduced correctly that mg-ea0e's
instrument was not `wc -w`. I did not then turn the same question on the brief. That is D5 in
`OUTCOMES.md`.

---

## WHAT I DID NOT DO

- **I did not re-verify mg-34bf's original construction** of the seven `attempt-*.md` files.
  My population starts at `78ae4d9`; whether those files were faithful when built is a
  different ticket's question.
- **I did not read `docs/audit-stage-process.md` or `threads-chronology.md` as prose.** They
  were checked as byte containers — every atom of the old file's :142-177 and :180-381 is
  present in them character for character — not read for sense. A destination file that is
  byte-perfect and incoherent would pass every check in this suite.
- **I did not verify the mathematics.** "No claim was reworded" is a statement about strings.
  Whether ledger row 8 or L1b is *true* is mg-2de0's territory, not mine.
- **I did not check the rendered `docs/state-of-the-wall.html`**, which STATE.md:5 still dates
  "Generated 2026-07-19". mg-ea0e flagged it stale and did not regenerate it; I confirmed the
  line is still there and went no further.
- **I did not fix anything.** No STATE.md byte, no dead citation, no orphaned figure. F1 and R1
  are reports.
- **I did not use `git patch-id`**, deliberately (see above).
- **My §5 reading was not cold.** See F5.
