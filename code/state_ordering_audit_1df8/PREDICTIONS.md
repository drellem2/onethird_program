# mg-1df8 — PREDICTIONS for the INDEPENDENT AUDIT of the STATE.md strength-ordering correction

Committed **before** one byte of `STATE.md`'s content is read, before any diff of
`905526f` / `f85a4e8` / `05a0061` is opened, and before any script in this
directory exists.

**Target named:** `STATE.md` as of commit `491d42c79f7628c18cb7a5d197faa9f4600cd6c1`
(last commit touching `STATE.md` on `origin/main` at the time of writing; `origin/main`
HEAD is `dafe75910f731927affdf366457d681e262acf62`; blob
`7f73bfc87b4bc4caab6c836f8c3922a2416863cf`). This matches the SHA the mayor named in
the dispatch note. If it has moved when I run, I audit the CURRENT file and name THAT
SHA, per the dispatch note.

---

## Part 0 — EXPOSURES, DISCLOSED RATHER THAN LAUNDERED INTO PREDICTIONS

The house style in this arc is that a prediction is worthless if it is a restatement
of something the dispatch prompt already told me. These are what I already hold. Every
prediction below that is downstream of one is marked with the exposure it inherits.

- **H1 — MY BRIEF ALREADY ASSERTS THE ANSWER TO CHECK 1.** The ticket body states the
  three definitions *and* the conclusion `(LIB) < (LIB-weak) < (LIB-const)`. So check 1
  is not a blind re-derivation; it is a check of an asserted ordering. I mitigate by
  (a) deriving from the definitions only, (b) testing each adjacent pair for implication
  in **both** directions, which the brief does not ask for, and (c) refusing to use the
  brief's `<` symbol until I have fixed its meaning myself.
- **H2 — I HAVE ALREADY DONE THE DERIVATION BY HAND.** It is three lines and I did it
  while reading the brief. So **P1 is a formality and I say so.** The content of this
  audit's mathematics is P2/P3, which the brief's linear-chain framing *excludes by
  construction*.
- **H3 — I HAVE READ 40 `STATE.md` COMMIT SUBJECTS.** Not one byte of the file, no diff.
  In this repo commit subjects are load-bearing prose, so this is a real exposure. In
  particular I already hold:
  - `f85a4e8` (mg-2860, 08-06 18:52) — *"STATE.md LEADS WITH WHAT THE ARCHITECTURE
    CONSUMES — a CONSTANT UNIFORM IN n, not the limit; and (LIB-weak) is on the board
    for the first time"*
  - `905526f` (08-07 00:38) — *"THE INVERSION WAS NEVER IN THE FILE — mg-2860 refused
    it, so error 1 of this ticket is STALE; the live defect was error 2, and STATE.md
    rendered `(LIB-weak) …`"*
  - `4ef64d7` (08-07 17:15) — *"N₀ IS NOT UNSPECIFIED — NO N₀ WORKS FOR THE CLASS"*
  - `05a0061` (08-07 01:49) — mg-c4f5's audit landed, *"THE PREMISE HOLDS AND THAT IS
    NOT THE HEADLINE"*
- **H4 — CHECK 5's SECOND HALF IS ANSWERED BEFORE I START.** `mg show mg-c4f5` returns
  `Status: done` and `05a0061` is on `main`. So "check whether mg-c4f5 has run" is
  already YES and P11 is a reproduction, not a discovery. What is *not* answered is
  whether its verdict actually bears on the ordering row, and that is the part I will
  work.
- **H5 — THE "PREMISE IS THE THING THAT WAS WRONG" SHAPE WAS SHOWN TO ME.** My dispatch
  prompt's recent-activity block contains `cf476ba`, *"mg-2eed's INDEPENDENT AUDIT of
  mg-b488's STATE.md landing — CONFIRMED at 491d42c, AND THE BRIEF'S OWN PREMISE IS THE
  THING THAT WAS WRONG"*. P8 below is that same shape. **It is therefore a pattern I was
  handed, not one I found**, and should be discounted accordingly if it hits.
- **H6 — THE `2/(n+1)` SIGHTING IS PRE-DISCLOSED.** The dispatch note tells me mg-131e
  refuted `eps_spec = 2/(n+1)` and that seeing it live in a *source document* is a known
  in-flight correction (mg-372e). So that cannot be a finding of mine; at most a location
  report.
- **H7 — I KNOW THE BRIEF'S AUTHOR IS SELF-DECLARED UNRELIABLE ON THIS ROW.** "I have
  been wrong on this row twice today in opposite directions." This is an instruction to
  weight the brief *down*, and I read it as licensing P8/P9.

I have **not** read: `STATE.md` (any version), any diff, mg-c3ca's or mg-c4f5's
deliverable bodies beyond the first 40 lines of each *ticket* (not deliverable), or any
file under `docs/`.

---

## Part 1 — THE MATHEMATICS (checks 1, 2)

Definitions as the brief gives them, with `E := E[inv_e]` a function of `n`:

- **(LIB)** `E = O(n/γ)`
- **(LIB-weak)** `E = o(n²)`
- **(LIB-const)** `E ≤ (ε/6)(n² − 1)`

**P1 — FORMALITY (see H2).** `(LIB) ⟹ (LIB-weak)` and `(LIB-weak) ⟹ (LIB-const)
eventually`. So under the reading "the admitted bound grows faster as you move right",
the brief's chain `(LIB) < (LIB-weak) < (LIB-const)` is **CORRECT** and the
"opposite" that merged this morning was **WRONG**. Confidence 0.93. I claim no credit
for this; H1 handed it to me.

**P2 — THE ORDERING IS NOT A CHAIN, AND THIS IS THE REAL CONTENT.** As *sets of
functions of n*, `(LIB-weak)` and `(LIB-const)` are **INCOMPARABLE**: neither implies
the other.
  - `(LIB-const) ⇏ (LIB-weak)`: `E(n) = (ε/6)(n²−1)` satisfies (LIB-const) with
    equality at every `n` and is `Θ(n²)`, not `o(n²)`.
  - `(LIB-weak) ⇏ (LIB-const)`: an `o(n²)` function may exceed `(ε/6)(n²−1)` at any
    finite prefix of `n`.
  So the brief's own `<` is only defensible under an **eventually** reading, and a
  reader who takes it as implication in the stated direction is misled in the *second*
  direction. **Confidence 0.90 that this is mathematically right; confidence 0.35 that
  STATE.md says it.** If STATE.md renders the ordering as a flat chain without the
  eventually-qualifier, that is a FINDING and it is the *same defect class* the ticket
  was raised about — a third inversion in a new costume.

**P3 — `(LIB) ⟹ (LIB-weak)` IS CONDITIONAL ON γ, AND THE BRIEF STATES IT FLAT.**
`O(n/γ)` is `o(n²)` **only if γ is bounded below by a positive constant** (more
precisely `γ = ω(1/n)`). If `γ` may decay like `1/n`, `O(n/γ) = O(n²)` and the first
link of the chain **fails**. Confidence 0.85 that this is right; confidence 0.25 that
STATE.md pins γ's n-dependence at the point it states (LIB). **If neither the brief nor
STATE.md fixes γ's dependence on n, the chain's first link is unproven as written** and
I will say so as a correction to my framing-giver.

**P4 — "DIFFER IN KIND" IS THE RIGHT PHRASE AND THE KIND IS: LIMIT vs UNIFORM.**
(LIB-weak) is a statement about a limit (`E/n² → 0`); (LIB-const) is a uniform-in-`n`
inequality with an explicit constant. They do **not** differ by a constant factor, and
no constant converts one into the other. Confidence 0.95.

**P5 — NO `N₀` WORKS UNIFORMLY OVER THE CLASS `o(n²)`, AND I CAN PROVE IT.** For any
candidate `N₀` and any `ε > 0` there is `E ∈ o(n²)` with `E(N₀) > (ε/6)(N₀²−1)` — take
`E(n) = M·n^{3/2}` with `M` large. So the quantifier gap is not "find the `N₀`"; it is
"there is no `N₀` for the class, only one per member". Confidence 0.90. **Downstream of
H3** (`4ef64d7`'s subject already says "NO N₀ WORKS FOR THE CLASS"), so this is a
reproduction of a landed result, not a discovery — I predict it *because* I was told it,
and my contribution is the exact witness, not the claim.

**P6 — THE `N₀` FOR A GIVEN MEMBER MOVES WITH `ε`.** For `E(n) = M n^{3/2}`,
`N₀ ~ (6M/ε)²`, so it blows up as `ε ↓ 0`. Confidence 0.92. This is the "surviving
threshold MOVES WITH n / with ε" the brief's check 4 gestures at, made explicit.

---

## Part 2 — THE DOCUMENT (checks 2, 3, 4, 5, 6)

**P7 — THE QUANTIFIER GAP WILL *NOT* BE STATED AT THE POINT (LIB-weak) IS INTRODUCED.**
This is the brief's check 3 and its stated failure mode ("both in STATE.md, one row
apart"). Prediction: **50/50**. I deliberately do not favour either side. The reason I
refuse a lean: a document that has been rewritten by mg-2860, mg-c4f5's landing,
`4ef64d7` and `491d42c` in 30 hours has had four chances to fix this and four chances to
re-break it. Confidence 0.50, and I commit *in advance* to the acceptance criterion:
the sentence at the (LIB-weak) site must (a) say (LIB-weak) does **not** supply the
operative form, and (b) name the gap as a **quantifier** (or say "for all n" vs "for
large n" in words). A bare pointer to another row **fails**, by the brief's own
argument, and I will score it FAIL even if it looks helpful.

**P8 — THE BRIEF'S OWN PREMISE IS PARTLY STALE.** The brief says "I asserted the
opposite this morning and it merged." `905526f`'s subject says the inversion was **never
in the file** because mg-2860 refused it. So the thing that merged may have been a
*ticket*, not a *file state* — and the correction I am sent to audit may already be a
correction of a defect that was only ever in pm-onethird's head. Confidence 0.60.
**Contaminated by H5 — discount heavily.**

**P9 — I WILL FIND AT LEAST ONE PLACE WHERE THE ORDERING IS STATED WITHOUT ITS
QUANTIFIER.** Not necessarily the (LIB-weak) row — anywhere in `STATE.md`. Confidence
0.70. STATE.md is an executive summary (`cc4c663`: 186,710 → 32,772 bytes) and
compression is exactly the operation that drops quantifiers.

**P10 — "NEITHER PROVED NOR BLOCKED" SURVIVES BUT LOSES ITS TEETH.** Prediction: the
text keeps "not blocked" and does **not** carry, at that site, both (a) that mg-c3ca's
forward vector's marginal form is FALSE and (b) that the surviving threshold moves with
`n`. Confidence 0.55 that at least one of (a)/(b) is missing at the site.

**P11 — mg-c4f5 HAS RUN (reproduction, see H4).** Confidence 0.99, worth nothing. The
live question is whether its verdict *touches the ordering row at all*; I predict it
does **not** directly — it audited the L1b premise `(LIB-weak) ⟹ λ_std → 1`, which is a
different statement from the ordering among the three LIB forms. Confidence 0.65. If so,
the brief's "its verdict outranks everything above" is **inapplicable**, not obeyed.

**P12 — mg-c3ca IS SAID TO BE UNAUDITED: I PREDICT THIS IS EITHER ABSENT OR NOW FALSE.**
mg-c3ca is `archived`, and mg-c4f5 was pre-filed as its audit and is `done`. So a
STATE.md sentence saying "mg-c3ca is UNAUDITED" would now be **stale in the other
direction**. Confidence 0.55 that the "unaudited" marker is either missing or
contradicted by mg-c4f5's existence. This is the brief's check 5 turning into a finding
against the brief.

**P13 — NO THEOREM STATEMENT MOVES (check 6).** Confidence 0.80 that a diff of the
correction touches only characterisation/hedging language. If a theorem moves I report
it as a finding.

**P14 — I WILL FIND `2/(n+1)` SOMEWHERE.** Confidence 0.45, and per H6 it is **not a
finding**, only a location report.

---

## Part 3 — MY OWN MOST LIKELY ERRORS, FILED IN ADVANCE

**P15 — I SCORE A CROSS-REFERENCE AS A STATEMENT.** The single most likely way I return
a wrong PASS is by reading a nearby sentence, in the same paragraph or the next line,
as "at the point (LIB-weak) is introduced". The brief is explicit that one-row-apart is
the failure. **Guard, bound now, before I open the file:** I will fix the (LIB-weak)
introduction site by line number first, quote the **contiguous byte range** of that row
/ cell / bullet verbatim into the report, and score checks 2–4 **against that quoted
range alone**. Anything found outside it is reported as "present elsewhere, does not
discharge", never as a pass.

**P16 — I MISTAKE THE ORDERING'S DIRECTION BECAUSE `<` IS UNDEFINED.** "Stronger" for a
*hypothesis* is the reverse of "larger" for a *bound*, and this arc has already inverted
on exactly that. **Guard:** I will never write `<`. I will write `⟹` in the direction I
mean, and every claim in my verdict will be phrased as an implication with a named
direction, never as a comparison.

**P17 — I MANUFACTURE A FINDING OUT OF P2's INCOMPARABILITY.** If STATE.md's text is
scoped so that it is only ever talking about the *eventually* reading, P2 is correct
mathematics and an irrelevant complaint. **Guard:** P2 is only scored as a FINDING if I
can quote a STATE.md sentence that a competent reader would take as an unqualified
implication in the stated direction.

**P18 — I TREAT `git log` SUBJECTS AS THE FILE.** They are 200-char summaries written by
the agent being audited. **Guard:** every claim about what STATE.md says is backed by a
quoted line number from the blob at the named SHA, never by a commit subject.

---

## Part 4 — WHAT I EXPECT TO BE UNABLE TO DO

Filed now so it cannot be quietly dropped later:

- I will **not** re-prove `(LIB-weak) ⟹ λ_std → 1`. That is mg-c4f5's job and it is done.
- I will **not** attack (LIB-weak) itself.
- I will **not** re-derive mg-c3ca's forward vector from scratch; I will check only
  whether STATE.md's *characterisation* of it is consistent with what mg-c3ca's own
  deliverable says.
- I make **no** edit to any theorem statement. If I find one wrong, I report it.
