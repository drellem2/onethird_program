# mg-dd8b — INDEPENDENT AUDIT of mg-24fb

## VERDICT: **NOT RUNNABLE AS BRIEFED — mg-24fb HAS NOT LANDED.** What is delivered is a
## PRE-STRIKE BASELINE, and it already answers the two questions the brief cared most about.

**STATE.md read at commit `491d42c79f7628c18cb7a5d197faa9f4600cd6c1`, blob
`7f73bfc87b4bc4caab6c836f8c3922a2416863cf`, 209 lines.** That is the SHA my dispatch named,
confirmed independently by `git log -1 origin/main -- STATE.md` rather than accepted; my
worktree is byte-identical to `origin/main` on that file (`git diff --stat` empty). **It did
not move under me.** Re-checked at the end of the audit and still `491d42c`.

**Gate state, measured 2026-08-07 22:06 and again at the end:**

    mg show mg-24fb                        ->  Status: available
    git log --all --oneline --grep='24fb'  ->  0 commits, any branch

**Note for anyone re-running that grep:** from `5358a39` onward it returns **1** — my own
predictions commit, whose subject contains the string `mg-24fb`. mg-24fb still has zero
commits of its own. Filter on the trailing `(mg-XXXX)` marker, not a bare substring.

My brief says "DO NOT START until mg-24fb has landed." It has not. There is no diff.
**Checks 3, 4(partly), 5 and 6 of my brief have no object and are reported NOT DONE below,
not PASS.** A file nobody edited trivially satisfies "was not silently rewritten", and
converting that into a PASS is the precise defect this lineage keeps catching. P12 of
`PREDICTIONS.md` bound me to this before I knew what I would find.

---

## THE TWO FINDINGS

### FINDING 1 — THE "FIVE vs SIX" IS NOT AN ERROR. IT IS AN UNNAMED FRAME, AND BOTH NUMBERS ARE RECOVERABLE.

My brief and mg-24fb's ticket both treat mg-5ce3's "FIVE sites" over a list of six as a
miscount to be adjudicated. **I counted independently and neither number is wrong. They are
answers to two different questions, and the defect is that neither question was stated.**

Structural class of every on-topic occurrence in
`OneThird-Literature-LowerBound-MinimalCounterexample-mg-33f5.md` (measured, `s4_sites.py`):

| line | structural context | occurrences |
|---|---|---|
| 15  | running prose | 1 |
| 137 | **table row** (threshold table, row T4) | 1 |
| 148 | **table row** (clearance table, row T4) | 1 |
| 166 | running prose | **2** |
| 255 | **blockquote** — the document's *proposed STATE.md ledger entry* | 1 |
| 261 | running prose | 1 |

Now count, declaring the frame each time:

| frame | answer |
|---|---|
| on-topic LINES, running prose only | **3** |
| on-topic LINES, prose + tables, **excluding** the proposed-ledger blockquote | **5** |
| on-topic OCCURRENCES, prose + tables, excluding the blockquote | **6** |
| on-topic LINES, **including** the blockquote | **6** |
| on-topic OCCURRENCES, including the blockquote | **7** |
| raw `unspecified` LINES, no judgement | **7** |
| raw `unspecified` OCCURRENCES, no judgement | **8** |

**FIVE is exactly the on-topic line count excluding the proposed-ledger blockquote. SIX is
exactly that count including it — and is also the occurrence count excluding it.** mg-5ce3
enumerated six addresses (one of which is the blockquote) and reported five. Both of its
numbers sit on this table. It changed frame between its verdict and its list without saying
so, which is a real defect — but it is **not** the line-vs-occurrence error mg-24fb's ticket
diagnoses, and "which number is right" is the wrong question. Seven numbers are right.

**MY OWN COUNT, WITH ITS FRAME NAMED IN THE SAME BREATH, BECAUSE THAT IS THE WHOLE POINT:**

> **FRAME:** occurrences of the primary term `unspecified` that are (a) **ON-TOPIC** — about
> the `N₀` of `(LIB-weak) ⟹ (LIB-const)`, not some other unspecified quantity — and (b)
> **LIVE** — asserted in the document's own voice, not struck and not quoted from another
> document; counted across **all** structural contexts including tables and blockquotes.
>
> **ANSWER: 7 OCCURRENCES on 6 LINES** in `…-mg-33f5.md`
> **plus 1 OCCURRENCE on 1 LINE** in `OneThird-LIBweak-mg-c3ca.md`
> **= 8 OCCURRENCES on 7 LINES across the two documents.**

Raw, with no judgement applied, it is **9 occurrences on 8 lines**; the difference is the one
off-topic site below.

#### 1a. A SITE BOTH PRIOR COUNTS CORRECTLY EXCLUDED, AND WHICH A STRIKE MUST NOT TOUCH

`…-mg-33f5.md:162` — *"And `C` is unspecified with `C ≥ 1`"* — is about **`C`, the constant in
the `n ≈ 900C` crossover**, not about `N₀`. A grep for `unspecified` returns it; §5.3 has
nothing to do with it. Neither mg-5ce3 nor mg-24fb listed it, so **both got this right**, and
I record it because the next agent to re-run the grep will find 8 and not 7 and must not
"repair" the discrepancy by striking a correct sentence.

#### 1b. THREE OF THE SEVEN INHERITED ADDRESSES DO NOT CARRY THE WORD, AND THE REASON IS SYSTEMATIC

| inherited | today | what is actually on the inherited line |
|---|---|---|
| `mg-33f5:165` | **MISS** | the sentence *starts* here; `unspecified` is on **:166** |
| `mg-33f5:260` | **MISS** | the sentence *starts* here; `unspecified` is on **:261** |
| `mg-c3ca:100` | **MISS** | the sentence *starts* here; `unspecified` is on **:101** |

All three misses are the same thing: **the cited line is where the CLAIM begins and the word
wrapped to the next line.** That is a coherent citation convention — arguably a better one —
but it is undeclared, it is used inconsistently (`:15`, `:137`, `:148`, `:255` cite the word),
and **it is not usable as a grep address: 3 of 7 inherited addresses return zero hits.**

`…-mg-33f5.md` has **exactly one commit** on `origin/main` (`102792a`), so **no line can have
drifted since it was written.** These are mis-citations, not staleness — a different defect
with a different fix. My P4 (drift, P = 0.35) is therefore **MISSED**, and refuted by git
rather than by argument.

**Consequence for mg-24fb:** a polecat that strikes "at the six lines mg-5ce3 named" will
strike two lines that do not contain the claim and will **miss the double occurrence at
:166** — the one line in the corpus where the LINES/OCCURRENCES distinction actually bites.

---

### FINDING 2 — THE SYNONYM SWEEP FOUND ONE SITE, IT IS IN THE OTHER DOCUMENT, AND IT IS **CORRECT AS WRITTEN**

Nobody had run mg-5ce3's STATE.md synonym set against these two files. I ran it, after proving
the instrument finds planted occurrences of every term (`s1_census.py`, positive control 14/14
terms plus 4 targeted sub-checks; negative control 0 spurious matches on clean text).

Against `…-mg-33f5.md`: **all five brief-named synonyms return 0.** With the controls passing,
that absence is evidence. One extended-set hit, `:260` *"not for want of a large enough `N`"*,
is the same sentence as :261 and not a separate site.

Against `OneThird-LIBweak-mg-c3ca.md:113`, **one hit**, and it is the interesting one:

> `o(n²)` gives a constant threshold only **eventually**; `(LIB-const)` at the required
> constant gives it at every `n`. **The difference is the quantifier over `n`, not a constant.**

**This is the PER-FAMILY statement, and per-family is TRUE.** It is not the superseded reading.
It is what §5.3 leaves standing. **It must not be struck**, and it is the site most likely to be
struck by a sweep run on the synonym set without reading the hits — which is exactly the sweep
my own brief ordered. Reported as a hazard created by my brief, not by mg-24fb.

So: **P5 HIT** (the sweep found a site outside the known set) but **for the opposite reason to
the one it was betting on** — the new site is not a residue, it is a correct sentence.

---

## THE REMAINING CHECKS

### CHECK 4 (format) — THE BRIEF'S PREMISE IS ALREADY FALSE, MEASURED BEFORE mg-24fb EXISTS

My brief: *"mg-2df8 already struck neighbouring sentences… **Two strike formats in one file is
a defect in its own right.** Compare them directly."* That presumes one format to match.
`s2_format.py`, run on the **pre-mg-24fb** file so it cannot be back-fitted:

`OneThird-LIBweak-mg-c3ca.md` — 5 strikes, 4 markers, **3 distinct marker shapes**:

| site | shape | author |
|---|---|---|
| `:32`  | `**[NAME — mg-XXXX, on <src> §N.**  …` | mg-2df8 |
| `:52`  | `**[NAME — mg-XXXX, on <src> §N.**  …` | mg-2df8 |
| `:119` | `**[NAME — <who>: …]**` (**colon**, not `.**`) | mg-e35c / mg-5827 |
| `:325` | `> **NAME (mg-XXXX, …) — …**` (**blockquote, parentheses, no bracket**) | mg-55f2 |

**And the three bracketed markers close three different ways: `**]**` (:32), `**]` (:52),
`]**` (:119) — so mg-2df8's OWN TWO MARKERS DISAGREE WITH EACH OTHER on their closing
delimiter.** mg-2df8's commit body says it worked "in the house style mg-5827 used on §2.3 of
this same file"; it did not match mg-5827's punctuation either.

**So the defect my brief names as a thing to prevent is already present, three ways over, and
"match mg-2df8's format" is not a well-defined instruction — mg-2df8 has two.** I did not
repair this; it is not my ticket. **P7 scored: HIT on the general shape (strike + bold
replacement + bracketed marker), MISS on "a single extractable format".**

`…-mg-33f5.md` has **0 strikes and 0 markers** — mg-24fb will be introducing a strike
convention into a file with no precedent while being told to match a file with three.

**Verdict on check 4: the reference standard is RECORDED (above). The comparison itself is
NOT DONE — there is nothing to compare against.**

### CHECK 5 (the overclaim) — BASELINE RECORDED; THE REINTRODUCTION CHECK IS **NOT DONE**

`s3_overclaim.py`, controls first: planted bare overclaim **flagged**; the *compressed
strike-annotation form* `**[SUPERSEDED — mg-c4f5 §5.3: no N₀ exists.]**` — the exact shape my
brief predicts — **flagged**; correctly qualified form **not** flagged; per-family detector
fires on the true half. 4/4.

| file | unqualified strong-form | qualified | per-family acks |
|---|---|---|---|
| `STATE.md` | **0** | 12 | 5 |
| `…-mg-33f5.md` | 0 | 0 | **0** |
| `OneThird-LIBweak-mg-c3ca.md` | 0 | 0 | **0** |

The guard raised one flag at `STATE.md:167` and **I read it by hand: it is my own false
positive.** *"there is no threshold to quote"* is about **mg-200d's refuted `2/(n+1)` threshold
arithmetic**, not about `N₀`. Kept in the output rather than tuned away, because a guard tuned
until it returns 0 is unfalsifiable. That is P13 firing on me as predicted.

**STATE.md's baseline is clean:** all 12 strong-form assertions carry the per-class qualifier
(`for the class`), and `:115` carries the explicit per-family disclaimer — *"a single family
satisfying (LIB-weak) does have **some** threshold of its own — it is simply not a function of
the hypothesis"*. That is the standard mg-24fb must not degrade.

**And here is the quantified risk, which is the useful part:** both target documents contain
**zero** per-family acknowledgements. **If mg-24fb writes a compressed strike saying "no `N₀`
exists" into either file, there is nothing anywhere in that file to rescue a reader from the
false per-class reading.** In STATE.md the surrounding cell would catch it; in these two
documents it would not.

### CHECK 3 (struck vs rewrote) — **NOT DONE.** No diff exists.

### CHECK 6 (STATE.md unmoved) — **NOT DONE as briefed**, and what I can say instead:
STATE.md is at `491d42c` / blob `7f73bfc`, unchanged from the SHA my dispatch named, and
unchanged between the start and end of this audit. **This establishes that nothing moved it
while I read it. It establishes NOTHING about mg-24fb**, which has not run.

---

## PREDICTIONS SCORED

| # | bet | outcome |
|---|---|---|
| P1 | occurrences > lines; ≥1 line carries two (P=0.45) | **HIT** — `:166` carries two; 8 vs 7 raw |
| P2 | five/six is a prose/list mismatch, not line-vs-occurrence (P=0.60) | **HIT, and stronger than stated** — both numbers are defensible under named frames |
| P3 | ≥1 of the six named sites is not a live assertion (P=0.50) | **MISS** — all six are live; the off-topic one (`:162`) was in neither list |
| P4 | line drift — ≥1 number no longer lands (P=0.35) | **MISS** — 3 of 7 do not land, but the file has ONE commit, so it is mis-citation, not drift. Right observation, wrong mechanism. |
| P5 | synonym sweep finds a site outside the known set (P=0.70) | **HIT** — `mg-c3ca:113`, but it is CORRECT, not a residue |
| P5b | "sufficiently large" occurs at all (P=0.55) | **MISS** — 0 in both files |
| P6 | positive control passes (P=0.97) | **HIT** — 14/14 terms, 4/4 sub-checks |
| P7 | mg-2df8's format is strike + bold + bracketed marker (P=0.45) | **HIT on shape, MISS on singularity** — three shapes, three closers |
| P8 | STATE.md at `491d42c` | **CONFIRMED, not predicted** (declared as such in advance) |
| P9 | `2/(n+1)` live in one of my two docs (P=0.30) | **MISS** — 0 occurrences in both. mg-372e's two documents were mg-6bc2 and mg-200d. |
| P10, P11 | about mg-24fb's landed content | **UNRESOLVED** — no diff |
| P12–P16 | my own error modes | P13 **FIRED** (`STATE.md:167` false positive, kept). P16 held. |

**Nine resolved, five hits, three misses, one hit-with-wrong-mechanism.**

---

## DEFECTS OF MY OWN, KEPT IN THE SOURCE

1. **`s2_format.py`'s shape-B pattern was greedy across the `.**` that ends a shape-A marker**,
   so its first run reported **2** shape-B sites where there is **1** — `:52` matched on the
   strength of a colon sixty words later. Found by reading my own output against the file,
   fixed by excluding `*` from the run, and the reason is written into the source at the
   pattern. A shape census that silently double-counts is the same class of instrument error
   this audit is about, and it was in my instrument.
2. **`s3_overclaim.py` flags `STATE.md:167`, which is a false positive** (mg-200d's threshold
   arithmetic, not `N₀`). Kept and adjudicated by hand in the text above rather than tuned out.
3. **My sentence splitter is not used in the final adjudication** — the `sentences()` helper in
   `s3` is dead weight; the ±600-character window does the work. Declared rather than deleted
   so the next reader does not assume it was load-bearing.
4. **A phrase wrapped across a line break is invisible to my per-line scan.** This is asserted
   as a KNOWN LIMITATION and tested as such (an expected-False sub-check in the positive
   control). It matters here: it is the *same* wrap that makes three inherited addresses miss.
   I did not run a whitespace-normalised whole-file scan to close it.

---

## WHAT I DID NOT DO

- **I did not audit mg-24fb.** It does not exist. Every statement above about it is
  conditional and labelled.
- **I did not re-derive or re-word §5.3's mathematics.** My prompt hands me the per-class /
  per-family distinction verbatim (exposure H4), so re-deriving it would not have been
  independent, and it is not my brief.
- **I did not edit STATE.md, either target document, or any other document.** This audit is
  measurement only. Everything above is a report; no repair is filed.
- **I did not repair the three-format inconsistency in `OneThird-LIBweak-mg-c3ca.md`**, or
  mg-2df8's two disagreeing closing delimiters. Noted, not fixed — not my ticket.
- **I did not check out `491d42c`.** My dispatch forbids it and the current file is the object.
- **I did not verify mg-5ce3's verdict text myself** — I have "said FIVE and listed SIX" only
  from mg-24fb's ticket body and my own dispatch (exposures H2/H3). My frame table shows both
  numbers are recoverable; **which one mg-5ce3 actually meant, I did not read.**
- **I did not sweep any file other than these two and STATE.md.** `docs/state-of-the-wall.html`
  and the other ~90 documents in `docs/` are unswept for this reading.
- **I did not run any mathematics.** No LP, no poset enumeration, no arithmetic. This is a
  documentary audit and its instruments are three greps with controls.

---

## RUNNING IT

    python3 code/n0_strike_audit_dd8b/s1_census.py     # site census, both units, + controls
    python3 code/n0_strike_audit_dd8b/s2_format.py     # strike/marker format reference standard
    python3 code/n0_strike_audit_dd8b/s3_overclaim.py  # per-class qualifier guard + controls
    python3 code/n0_strike_audit_dd8b/s4_sites.py      # inherited line numbers resolved

`s4` exits 1 by design — three inherited addresses do not carry the term, and that is Finding 1b.
