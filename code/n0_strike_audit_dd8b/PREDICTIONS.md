# mg-dd8b — PREDICTIONS for the INDEPENDENT AUDIT of mg-24fb

Committed **before one byte of either target document is read**, and — unusually for this
lineage — before the audited work exists at all.

## 0. THE FRAME, STATED FIRST BECAUSE IT CHANGES WHAT THESE PREDICTIONS ARE

`mg show mg-24fb` reports **`Status: available`**. `git log --all --oneline --grep='24fb'`
returns **zero commits on any branch**. My brief says in its own words:

> Pre-filed in the SAME ACTION as mg-24fb. DO NOT START until mg-24fb has landed.

**mg-24fb has not landed.** There is no diff. So these predictions are pre-registered
against an artefact that does not exist yet, which is a strictly stronger pre-registration
than the usual one: there is no diff to have peeked at, and no wording to have absorbed.

That also means checks 3, 4, 5 and 6 of my brief (struck-vs-rewrote, format match, overclaim
reintroduction, STATE.md untouched) are **currently unrunnable**. P12 pre-commits me to
reporting them as NOT DONE rather than converting an absence of edits into a PASS. This is
the exact failure this corpus keeps catching, and it is available to me right now in its
purest form: a file nobody edited trivially satisfies "was not silently rewritten".

## 1. EXPOSURES — what I already hold by reading, disclosed rather than laundered

**H1.** I read **the entire body of mg-24fb** via `mg show mg-24fb`. It is a detailed ticket.
So I am not blind to the parent's *instructions*, only to its *execution*.

**H2 — the load-bearing one.** mg-24fb's body hands me the candidate site set verbatim:
"mg-5ce3 reports the 'unspecified N_0' reading at **:15, :137, :148, :165, :255, :260**"
in `OneThird-Literature-LowerBound-MinimalCounterexample-mg-33f5.md`, plus
`OneThird-LIBweak-mg-c3ca.md:100`. **My count is therefore NOT blind.** I hold six specific
line numbers before counting. P1/P2 are scored knowing this: a count that merely reproduces
those six is a REPRODUCTION, not an independent measurement, and I will say so in those
words. The independent content of my count is (a) the unit, (b) sites *outside* that set,
and (c) whether each named site is actually LIVE.

**H3.** My dispatch prompt already tells me "its predecessor said FIVE and listed SIX". So
the existence of a five/six discrepancy is **given to me**, not discovered. P2 bets on its
*mechanism*, which is the only part still open.

**H4.** My prompt states the PER-CLASS / PER-FAMILY distinction verbatim, including which
one is FALSE and that it is section 5.3. Check 5 is therefore a **matching exercise against
a standard I was handed**, not a derivation. I did not re-derive 5.3 and P13 says I will not.

**H5.** My prompt names STATE.md at `491d42c79f7628c18cb7a5d197faa9f4600cd6c1`. I confirmed
this independently with `git log -1 origin/main -- STATE.md` before writing this file, so P8
is a confirmed measurement, not a prediction.

**H6.** I ran `git show --stat dafe759` (mg-372e) **before** writing this file. Its "TWO
documents" are `OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md` and
`OneThird-PerSlot-AdjacencySymmetry-mg-200d.md` — **neither of my two targets**. So the
in-flight 2/(n+1) correction my prompt warns me about does not touch my files by that commit.
P9 is what remains open: whether 2/(n+1) appears LIVE in my two documents anyway, unswept.

**H7.** I have NOT opened either target document, mg-2df8's diff, mg-5ce3's verdict, or
STATE.md's body. Every prediction below about their contents is genuinely blind.

## 2. PREDICTIONS

**P1 (count, mg-33f5 doc).** Counting case-insensitive occurrences of `unspecified` in
`OneThird-Literature-LowerBound-MinimalCounterexample-mg-33f5.md`, I predict
**OCCURRENCES >= LINES**, and I predict **at least one line carries two occurrences**, making
the two numbers differ. P(differ) = 0.45. If they are equal I say so.

**P2 (mechanism of FIVE-vs-SIX).** The discrepancy is *not* a line-vs-occurrence artefact.
It is a prose/list mismatch — a verdict sentence saying "five" above an enumeration of six
distinct line numbers. P = 0.60. The competing hypothesis (two of the six lines are the same
logical site, so "five sites, six lines" is *defensible*) I put at P = 0.25, and I will look
for it specifically rather than assuming sloppiness.

**P3 (the six are not all LIVE).** At least one of :15, :137, :148, :165, :255, :260 is
**not a live assertion** — it is a quotation, a heading, a bibliography line, or already
marked. P = 0.50. This is the one that would make BOTH prior counts wrong in the same
direction, and it is the shape mg-372e just found ("wrong in BOTH directions").

**P4 (line drift).** The six line numbers were recorded by mg-5ce3 against an *older*
revision of the file. At least one no longer lands on an "unspecified" line today. P = 0.35.
I will resolve every number against today's file and report drift as drift.

**P5 (synonym sweep finds something).** The mg-5ce3 synonym set — "not specified", "unknown
threshold", "sufficiently large", "for large enough", "eventually" — hits **at least one site
in these two documents that is outside the six-plus-one set**. P = 0.70. Highest-probability
individual term: **"sufficiently large"** (P = 0.55 it occurs at all), then "eventually"
(P = 0.45, but with high false-positive rate — see P14).

**P6 (positive control).** My sweep instrument, run against a file with a deliberately
planted occurrence of each synonym, finds all of them. P = 0.97. This is a formality and I
report it as one — but I run it, because an absence reported by an untested grep is worth
nothing, and my brief demands exactly this.

**P7 (mg-2df8's format).** The strike format already in `OneThird-LIBweak-mg-c3ca.md` uses
markdown strikethrough `~~...~~` on the superseded text with an adjacent bracketed or bolded
supersession note naming the superseding item. P = 0.45 for that specific shape;
P = 0.85 that *some* consistent in-place format exists and is mechanically extractable.

**P8 (STATE.md SHA) — CONFIRMED, NOT PREDICTED.** `491d42c79f7628c18cb7a5d197faa9f4600cd6c1`.
Measured before this file was written (H5). I will re-measure at the end and report whether
it moved under me.

**P9 (2/(n+1) in my two documents).** `eps_spec = 2/(n+1)` appears LIVE in at least one of my
two target documents, i.e. mg-372e's sweep did not reach them. P = 0.30. If found I report
where and do **not** treat it as my finding — my prompt pre-discloses it as in-flight.

**P10 (STATE.md untouched by mg-24fb).** If mg-24fb lands before I finish, it does not edit
STATE.md. P = 0.80 — its own ticket body says "DO NOT restate section 5.3's mathematics here
... Point at it", and this lineage's polecats have been reading their briefs.

**P11 (the overclaim).** If mg-24fb lands, no site it writes asserts the strong "no N_0
exists" form without the per-class qualifier. P = 0.70. The residual 0.30 is exactly the
compression risk my brief names: a strike annotation is short, and the short form of 5.3 is
the false one.

## 3. MY OWN MOST LIKELY ERRORS, FILED IN ADVANCE

**P12 — the one this frame makes almost inevitable.** I report checks 3–6 as PASS because an
unlanded ticket cannot have broken them. **Guard, bound now:** any check whose object does
not exist is reported as **NOT DONE / NOT APPLICABLE**, never PASS, and my verdict headline
must not contain the word PASS for any of them.

**P13 — scoring a synonym hit that is not about the N_0 threshold at all.** "sufficiently
large" and especially "eventually" are ordinary mathematical English and will occur in
sentences with nothing to do with the LIB-const threshold. **Guard:** every hit is read in
context by hand and classified ON-TOPIC / OFF-TOPIC *before* it enters any count, and the
off-topic ones are reported with their count rather than silently dropped — a sweep that
reports only its survivors is unfalsifiable.

**P14 — counting an already-struck or quoted occurrence as LIVE.** mg-2df8 struck neighbours
in one of these files; a struck sentence still contains the word. **Guard:** every occurrence
classified LIVE / ALREADY-STRUCK / QUOTED-AS-HISTORY before it is counted, with the three
subtotals published separately so the reader can recombine them under a different definition
than mine.

**P15 — conflating "the audited work did not land" with "the audit failed".** The baseline
measurement is a real deliverable and it is *more* useful taken before the strike than after.
**Guard:** ship it, name it a baseline, and state plainly what it is not.

**P16 — asserting a count without naming the unit,** which is the precise defect I was sent
to find in someone else. **Guard:** every number in my verdict carries its unit inline —
LINES or OCCURRENCES — or it does not go in the verdict.

## 4. WHAT I WILL NOT DO, DECLARED NOW

- I will **not** re-derive or re-word section 5.3's mathematics. Neither would be independent
  (H4) and it is not my brief.
- I will **not** edit STATE.md, either target document, or any other document. This audit is
  measurement only; if I find live defects I report them, and filing repairs is someone's
  ticket, not mine.
- I will **not** check out the 491d42c version of STATE.md. My prompt forbids it and the
  current file is the correct object.
