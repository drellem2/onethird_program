# mg-40e4 — INDEPENDENT AUDIT of mg-5f7c: the suppression instrument's fail polarity

**Verdict in one line: the DECISION mg-5f7c made is right and is confirmed here; the
INSTRUMENT still does not hold it, on 7 of 28 constructions; and one of the three premises
mg-5f7c argued it from is false.**

`PREDICTIONS.md` was committed before any script of this audit existed
(`93ab336`, `predictions:`). Every figure below is scored against it, misses included.

---

## A convention, because this arc keeps losing track of whose number a number is

Every figure in this document is one of three things and says which:

* **re-derived** — computed by this audit's own code from rendered bytes or from the tree,
  with the population and grain named. Agreement with mg-5f7c is then a *replication*.
* **read** — mg-5f7c's or mg-65eb's figure, quoted, attributed, and **not** re-derived.
* **new** — a figure with no counterpart in the parent.

An orphaned number cannot be chased, so there are none below.

---

## 1. THE POLARITY DECISION — CONFIRMED, AND ITS ARGUMENT PARTLY REFUTED

The ticket that produced mg-5f7c required it to **decide** whether the instrument should fail
open or closed *in terms of what it protects against*, not to make the code and the documents
agree. **It did.** `README.md:17-50`, `polarity_5f7c.py:10-38` and `visible_a74f.py:47-60` all
carry the same three-premise argument, written as an argument and not as a note.

**Premise-by-premise, re-derived:**

| | mg-5f7c's premise | this audit |
|---|---|---|
| 1 | `DECLARED` S4 says the `hidden` **attribute** and `NOT_COVERED` line 1 puts a class outside the set, so a third document already said fail-open and only the code disagreed | **HOLDS.** Both strings are in `visible_a74f.py` at the anchor `6fb424f` and both are printed on every run. Q1 evaluates the printed set independently of both READMEs and reaches the same reading. |
| 2 | the costs are asymmetric: over-detection manufactures a fabricated defect in somebody else's document, under-detection merely fails to find one, **and the whole of what it can miss is enumerated under `NOT_COVERED`** | **THE ASYMMETRY HOLDS. THE CLAUSE IN BOLD IS FALSE** — Q1/Q27 and Q1/Q28 are documents a reader is shown **nothing** of, missed by an **in-set** mechanism (S4), which no line of `NOT_COVERED` enumerates. `Under-detection here is bounded and declared` is not true. |
| 3 | there was no single posture to document anyway: the one bug failed closed on one input and open on another | **HOLDS, and is stronger than stated.** Re-derived at the anchor over this audit's own 28 constructions: **11 of 28 fail closed and 4 of 28 miss an in-set mechanism** — both directions, one bug. |

**Premise 2's false clause does not overturn the decision**, and this audit says so rather than
inflating a finding: premises 1 and 3 settle it on their own, and the asymmetry itself — a
false SUPPRESSED is this instrument manufacturing evidence against another artifact, a false
NOT SUPPRESSED only fails to find one — survives intact and is the right reason. **The polarity
mg-5f7c chose is the correct one. What is wrong is the claim that under-detection is bounded,
and — see §2 — the claim that the instrument now holds the posture at all.**

**A repair that inverted the guard and rewrote the documents to match would look identical to a
correct one.** It is worth saying how that was excluded here rather than assumed: Q1's `correct`
column is computed from the **printed** `DECLARED`/`NOT_COVERED` text, and Q1's `vs POSTURE`
column is computed from **what a reader is shown**, which no document in the repository can
change. An inverted guard would show as `REPORTS OUT-OF-SET` on Q09–Q13 — an embedded
stylesheet, an external stylesheet, `aria-hidden`, `opacity:0`, off-screen positioning. All
five report `(none)`. **The guard is not inverted.**

---

## 2. THE FINDING: THE REPAIRED INSTRUMENT STILL FAILS CLOSED

`visible_a74f.py` prints, on every run:

> WHAT THE DECLARED SET DOES NOT COVER. … **THIS INSTRUMENT FAILS OPEN** … THAT SENTENCE WAS
> FALSE UNTIL mg-5f7c AND IS NOW EXECUTED RATHER THAN CLAIMED.

**POPULATION: 28 HTML documents written by this audit, none imported from `polarity_5f7c.py`.
GRAIN: one document, one marker position, the set of DECLARED mechanisms reported at it.**
All figures **re-derived**.

| | at `6fb424f` | on this tree |
|---|---|---|
| reports SUPPRESSED for content a reader IS SHOWN (**fails closed**) | **11 of 28** | **7 of 28** |
| disagrees with the printed declared set | 12 of 28 | 6 of 28 |
| misses an **in-set** mechanism | 4 of 28 | 2 of 28 |

The repair roughly halved it. **It did not close it.** The seven are two different defects:

### F1 — S5 matches `display:none` as a SUBSTRING OF THE STYLE ATTRIBUTE'S VALUE (Q19–Q22)

Four documents with **no stylesheet anywhere in them**, which a browser paints in full, and
which the repaired instrument reports **SUPPRESSED by S5**:

| | document | why a browser paints it |
|---|---|---|
| Q19 | `<div style="xdisplay:none">` | CSS Syntax 3 §5.4.4 — an unrecognised property name makes the declaration invalid at parse time; it is dropped whole |
| Q20 | `<div style="--display:none">` | CSS Variables 1 §2 — a custom property sets no CSS property |
| Q21 | `<div style="/* display:none */ color:red">` | CSS Syntax 3 §4.3.2 — comments are consumed by the tokenizer and produce no tokens |
| Q22 | `<div style="font-family:'display:none'">` | CSS Syntax 3 §4.3.5 — a string token's contents are not declarations |

**This is mg-5f7c's own P06 one level down, on the line mg-5f7c rewrote.** P06 —
`<div data-style="display:none">` — is *a property name matched inside a longer attribute
name*. F1 is *a property name matched inside a longer property name*, in the value. The repair
replaced the attribute-**name** extraction (`re.search(r'style\s*=\s*"([^"]*)"', attrs)` →
`attr.get("style", "")`) and left the **value** test byte for byte as it was:

```
    6fb424f:  re.search(r"display\s*:\s*none|visibility\s*:\s*hidden", style.group(1), re.I)
    HEAD:     re.search(r"display\s*:\s*none|visibility\s*:\s*hidden", attr.get("style",""), re.I)
```

Q19–Q22 therefore report `S5` **identically at both revisions** — this is not a regression, it
is the half of the defect the repair did not reach. Q23 (`<div alt="display:none">`) is the
control and reports `(none)`, so this is a statement about style **values** and not about the
name parse, which is sound.

### F2 — THE DECLARED SET ITSELF OVER-DETECTS (Q24, Q25, Q26)

Three documents where the code implements `DECLARED` **exactly** and the answer is still
SUPPRESSED for content a reader is shown in full:

* **Q24 `<details><summary>MARKER</summary>…</details>`.** HTML §4.11.1: the first `summary`
  child **is the closed widget's own label and is always rendered**. S1 says *inside a
  `<details>` carrying no `open` attribute*, and a summary is inside one.
* **Q25 `<textarea>MARKER</textarea>`.** HTML §4.10.11: the child text is the control's
  **default value and is painted**. S3 lists `textarea` beside `script`, `style` and
  `template`; the other three are not painted and `textarea` is.
  **`polarity_5f7c.py`'s P16 is this exact document and its `browser` column says `BLANK`.**
  A row name that is not its measurement, in the suite written to prove the polarity — and
  `six65eb.Shown`, the second instrument (§3), decides this row the **other** way.
* **Q26 `<style>[hidden]{display:block !important}</style><div hidden>…`.** CSS Cascade 5
  §6.2: an important author declaration beats the UA rule `[hidden]{display:none}`.
  **This is the row the ticket asks for by name — the polarity on a document WITH a
  stylesheet.** `NOT_COVERED` is written throughout as though a stylesheet can only *add*
  suppression the instrument misses. A stylesheet can equally *remove* one the instrument
  reports, and then the instrument is manufacturing precisely the evidence mg-5f7c's own
  premise 2 says must never be manufactured.

F2 is a defect of the **declared set**, not of the repair, and mg-5f7c explicitly and
defensibly declined to enlarge the set (its "did NOT do" #3). **What is not defensible is that
the sentence `THIS INSTRUMENT FAILS OPEN` is printed without the qualification**: it is true of
mechanisms *outside* the set and false of three constructions *inside* it.

### F3 — `NOT_COVERED` DOES NOT BOUND WHAT THE INSTRUMENT CAN MISS (Q27, Q28)

* **Q27 `<div title="a>b" hidden>`** — `_TAG`'s `[^>]*` stops at the first `>`, which HTML
  §13.2.5.34 says does not end the tag inside a quoted value. The tag is never seen and
  `hidden` is never parsed: reported `(none)` for a blank page.
* **Q28 `<div hidden />`** — HTML §13.2.5.6: a solidus on a non-void HTML element is ignored
  and the `div` stays open. `suppressors` treats any tag whose attribute text ends in `/` as
  self-closing and never stacks it: `(none)` for a blank page.

Both are misses produced by an **in-set** mechanism and a parser. Neither is in `NOT_COVERED`'s
seven lines. This is what refutes premise 2's bounding clause.

---

## 3. THE FRAMING SENTENCE IS FALSE: A SECOND SUPPRESSION INSTRUMENT IS COMMITTED

> `visible_a74f.py` is **the only instrument in this repository that measures suppression**. No
> second instrument contradicts it, so each of mg-65eb's findings against it was unopposed.
> — `code/state_suppression_repair_5f7c/README.md:3-4`, and again at `polarity_5f7c.py:4`

**POPULATION: 645 committed `.py` files. GRAIN: one file. RULE, stated before the sweep:** a
file qualifies iff it tests for the `hidden` attribute **and** tests a `<details>` for `open`
**and** tests an inline style for `display:none`. Five qualify; two decide on their own rather
than importing `visible_a74f`:

* **`code/state_visibility_audit_65eb/six65eb.py`, `class Shown`** — "THIS AUDIT'S OWN
  VISIBILITY INSTRUMENT. It is not `visible_a74f.py` and it does not import it… This one hands
  the bytes to the STANDARD LIBRARY'S HTML parser and reads ATTRIBUTES BY NAME." **That is
  mg-5f7c's repair, already written, in the directory of the audit that raised the ticket.**
* **`code/state_claims_repair_0120/verdicts0120.py:133`** — the same parser again, with a
  comment naming the reason: *"defect mg-65eb found in `visible_a74f.py` (`class="hidden"`
  scored suppressed there)"*.

So mg-65eb's findings were **not** unopposed — mg-65eb built the opposing instrument in the
same audit — and mg-5f7c had a second opinion on disk to cross-check its repair against and did
not run it. Q1 runs it: **the two instruments give opposite answers on 2 of 28 constructions on
this tree and 8 of 28 at the anchor.**

**`Shown` is not an oracle either**, which is why Q1 prints it as a column and not as a
verdict: it misses Q28 exactly as `visible_a74f.py` does, and it reports S5-equivalent
suppression on Q19–Q22 by the **same** value-substring rule (`"display:none" in style`). **F1
is arc-wide, not a defect of one file.** Where it differs is Q25 (`textarea`) — it does not
treat a textarea as suppressing, which is the correct reading — and Q27, which its parser gets
right.

---

## 4. THE BYTE OFFSET SPENT AS AN INDEX — RE-DERIVED, AND THE POPULATION ENLARGED

The "true" offset here is **defined**, not borrowed: *the smallest `j` such that
`html.unescape(out[j:])` begins with the marker*. It is neither `unescape_with_map` (the
repaired function — auditing a repair with the repaired function is not an audit) nor
`out.find` (which both mg-5f7c and mg-65eb substituted for it).

### A. mg-5f7c's population, re-derived

**POPULATION: mg-a74f's published run — 5 documents × 2 renderers × 5 cited sections = 50
section observations, taken from `6fb424f`'s own `ROWS`. GRAIN: one marker lookup.**

* **32 of 50** walked from a position that is not the marker's — **re-derived**, and it
  reproduces mg-5f7c's **read** figure of 32.
* the 18 that were not are **V1's ten** (inside a comment a renderer escapes nothing) plus the
  **eight `H1`s** — **re-derived**, split confirmed per row.
* **0 of 10** published row figures move at the true offset — **re-derived**.
* **50 of 50** — the *repaired* `unescape_with_map` lands exactly on the independently defined
  true offset. **A check on the repair, using a definition the repair does not supply.**
* This re-derivation of the **shipped** walk reproduces the committed transcript
  `code/state_delegation_repair_a74f/out_run_all.txt` figure for figure. **AGREES.**

### B. THE POPULATION mg-5f7c DID NOT AUDIT — and this is where the answer changes

`rows65eb.py:240` recomputes the identical defective expression —
`V.suppressors(out, u.index(V.marker(h)))` — and **mg-65eb publishes the result** in
`out_rows65eb.txt` and its `out_run_all.txt`.

**POPULATION: 4 constructions × 2 renderers × 5 cited sections = 40 further published section
observations and 8 further published row figures. GRAIN: one marker lookup.** All **new**.

* **34 of 40** walked off the marker.
* **2 of 8 published row figures MOVE**: `R2c` on both renderers, published
  `not-suppressed 5/5`, answer at the true offset `0/5`.
* the re-derivation reproduces `out_rows65eb.txt` figure for figure. **AGREES.**

**What that is and is not.** It is **not** a false claim left standing: mg-65eb publishes that
`5/5` *knowingly*, as the exhibit of the defect, and says so in its prose. What it is: mg-5f7c
wrote that *"the next document put to this instrument would not have been protected by the
shape of the last five"* — and **the next document had already been put to it, by the audit
that raised the ticket, and it had already moved, and it was already published.** mg-5f7c
re-created that very document as its own section-A construction and did not count it as a
published figure. Over the population *every committed figure produced by that expression*, the
answer is **2 of 18 move**, both named, rather than **0 of 10**.

**So: had the offset already corrupted a published figure? NO — over both populations, no
published figure asserts something false.** `0 of 10` and `no published figure of mg-a74f is
wrong` are both correct as written. They are correct over a population smaller than the one
that existed.

### C. `out.find(marker)` is not "the marker's position", and two audits used it as though it were

**POPULATION: all 90 observations of A and B. GRAIN: one marker lookup, three candidate
definitions.** `out.find` returns **-1 on 5 of 90** — mg-65eb's `R1` under `marked`, where the
renderer writes the marker with a character reference and the literal bytes are not in the
page. On those, `offsets_5f7c.py` counts the observation WRONG and then **omits it from the
comparison set** while still printing a total; `rows65eb.py` counts it FREE via a literal
string. Neither says its comparison population is smaller than its wrong-offset population.
**Inside mg-5f7c's own 50 this never fires** (0 of 50 undefined), so its printed `0 of 10` is
not affected — the substitution was harmless *there* and is not harmless in general.

---

## 5. THE OTHER THINGS THE TICKET ASKED

* **The unimplemented S1 (D2).** Repaired. Q18 —
  `<details data-open="open" title="open me">`, `open` in two decoy values and not as an
  attribute — reports **S1**. **Re-derived**, and the double decoy is this audit's, not the
  ticket's.
* **No replacement prediction of the next gap without a falsifier.** **HOLDS.** Q3/C2 prints
  every forward-looking line in the five files mg-5f7c added: all seven are *about* mg-a74f's
  failed prediction or are the refusal to issue another. What stands in its place (`A5`/`P13`/
  `V8`) is a standing row that can go red, not a forecast. **This audit issues none either.**
* **Predictions not rewritten after the result.** **HOLDS, and this is the check that matters:**
  `PREDICTIONS.md` in the tree is **byte for byte identical** (8339 bytes) to `PREDICTIONS.md`
  in mg-5f7c's own `predictions:` commit. Every pre-registered id is scored in the README.
* **The scoring header does not match its own table.** `README.md:160` says *"Predictions — 11
  of 13 held"*. The table beneath it has **12 rows, 10 ✅ and 2 ❌** — **re-derived by
  counting**. The likeliest reading is that the 8th section (disclosed in mg-5f7c's own defect
  #1 as added after `PREDICTIONS.md`) was counted as a thirteenth scored row; it is not a row
  of the table. A count whose population is not the thing printed under it, in the scoring
  header of the repair that catalogues that defect. The *"both misses are kept as written"*
  half of the same sentence is **correct**.
* **Patch-id, then adjudicate.** mg-5f7c's five commits exist twice in this object store. All
  five pre-rebase twins are **not** ancestors of `main`; all five carry the **same**
  `git patch-id --stable` as the commit that is. `README.md:283` pins `e3fb80e` at patch-id
  `9af08bc5d909054ae89a4ad8565e7531d60e2602`; **measured, it matches**, and the commit carrying
  it on `main` is `bdeab76`. `merge-base --is-ancestor` returns a false negative on all five,
  which mg-5f7c wrote down **in advance**.
* **Does the repair still reproduce at HEAD?** **Yes.** mg-5f7c's own `run_all.sh`, re-run here
  with the renderers installed: **8 of 8 sections on their pre-registered exit codes**, and
  `git status --porcelain` empty afterwards.

---

## 6. PREDICTIONS — 11 of 14 held, and all three misses are kept as written

| # | | |
|---|---|---|
| P1 the repaired instrument still fails closed on a stylesheet-free document, via an S5 value substring | ✅ | Q19–Q22, all four named shapes |
| P2 the `hidden`/`open` name parse is sound at the value level | ✅ | no witness exists; Q23 is the control |
| P3 `<textarea>` is shown, S3 fires, and `polarity_5f7c.py`'s P16 browser column is wrong | ✅ | Q25 |
| P4 a marker in `<summary>` of a closed `<details>` reports S1 for content a reader sees | ✅ | Q24 |
| P5 `NOT_COVERED` does not bound under-detection: `<div title="a>b" hidden>` reports `(none)` | ✅ | Q27, **and Q28 as a second shape I did not predict** |
| P6 the decision survives the argument — CONFIRMED, argument partly refuted | ✅ | §1 |
| P7 32 of 50, split 10 + 8 | ✅ | re-derived per row |
| P8 0 of 10 published row figures move under *my* definition of the true offset | ✅ | |
| P9 `out.find` and the index-map agree on all 50 | ✅ | 0 of 50 undefined **inside that population** — 5 of 90 outside it |
| **P10 ≥1 further published population exists, AND none of its figures moves** | ❌ **MISS** | the first half holds; **2 of 8 move**, and this is the most useful thing in the audit |
| P11 no forecast of the next gap | ✅ | 7 lines printed, all classified |
| **P12 re-scoring reproduces 11 held / 2 missed with nothing rewritten** | ❌ **MISS** | nothing was rewritten and the misses are A6/B3 as predicted — but the table is **10 of 12**, not 11 of 13 |
| P13 mg-5f7c's own suite reproduces 8 of 8 with a clean tree afterwards | ✅ | |
| **P14 this audit will contain a defect of its own class, found by itself** | ✅ | §7 — and I would rather it had been a miss |

**P10's miss is the one that mattered.** I predicted the enlarged population would change
nothing and it changed the headline: the counterexample to *"luck of row design"* was not
hypothetical and was not in the future — it was published, in this repository, by the audit
that raised the ticket, before mg-5f7c was written.

**P12's miss** is half a miss and is recorded as a full one: the substantive prediction (no
post-hoc editing) held byte for byte, and the arithmetic I predicted would reproduce does not,
because the header does not match its own table.

---

## 7. FOUR DEFECTS OF THIS AUDIT'S OWN INSTRUMENTS

1. **THIS RUNNER MADE ITS SUBJECT FAIL BY EXISTING.** The first full pass printed
   `AT LEAST ONE SECTION MISSED ITS PRE-REGISTERED EXIT CODE` **for mg-5f7c**, a repair that
   reproduces perfectly. The cause was `run_all.sh` itself: still untracked, so the tree was
   dirty, so `prose_5f7c.py` — which refuses to start on a dirty tree — exited 2, and the
   failure arrived wearing mg-5f7c's name. Repaired structurally, by refusing to start and
   **naming the files**, not by a retry. Committed as its own commit so the sequence is legible.
2. **Q3's instrument rule selects on strings and over-selects.** `polarity_5f7c.py` and
   `rows65eb.py` qualify as "suppression instruments" because their *constructions* contain the
   strings the rule looks for. That is why the sweep prints a second column (does the file
   decide on its own, or import `visible_a74f`?) and why the two exhibits in §3 were confirmed
   **by reading them**, not by the count. The count alone would not support the claim it is
   printed under.
3. **No browser was run.** Every `reader` column is a reading of the HTML and CSS
   specifications. mg-5f7c disclosed the same limit; what is added here is that **each row
   carries the specific rule it rests on**, so a reader can disagree with a citation rather than
   with an assertion. The rows this matters most for are Q24, Q25 and Q26, and they are the
   three whose spec rules are the least ambiguous in the file.
4. **Q1's `Shown` column is a cross-check and is printed as one.** It is a second instrument,
   not a ground truth; it shares F1 and misses Q28. No verdict of this audit rests on it.

---

## 8. WHAT WOULD HAVE SHOWN A PROBLEM HAD ONE EXISTED — the negatives, with their instruments

Three of this audit's findings are negatives. Each is stated with the instrument that could
have shown the positive, because an absence produced by not looking is not a result.

* **"The guard is not inverted."** Q09–Q13 are five documents a browser blanks or hides by a
  mechanism outside the declared set — an embedded stylesheet, an external stylesheet,
  `aria-hidden`, `opacity:0`, off-screen positioning. An inverted guard reports a mechanism on
  at least one. All five report `(none)`, at both revisions. Q12 and Q13 put the out-of-set
  mechanism **inside the `style` attribute S5 reads**, which is where an inversion would be
  cheapest to hide.
* **"No published figure was corrupted."** The instrument is the same walk run at two offsets
  over the same rendered bytes — not a reading of transcripts, which is why Q2 renders. It
  **did** fire: 2 of 8 in mg-65eb's population. It fired at 0 of 10 in mg-a74f's because the
  documents there are shaped so that a displaced position stays inside the same suppression,
  and Q2 prints the per-row displacement (`H2-112`, `H3-120`, …) that shows the displacement
  was real and the verdict survived it anyway.
* **"The predictions were not rewritten."** The instrument is a byte comparison against the
  `predictions:` commit, which fails on a single changed character. The scoring-header finding
  in §5 is what the same section looks like when it *does* find something.
* **This audit's own counts can move.** `selftest_40e4.py` T3 runs the identical 28 documents
  against the instrument at `6fb424f`: 11 fail closed and 12 disagree with the set, against 7
  and 6 on the tree. A population that scored the repaired and unrepaired instruments alike
  could not see the repair at all, and no row of Q1 would be evidence.

---

## 9. WHAT THIS AUDIT DID NOT DO

1. **It did not repair anything.** F1, F2 and F3 are left standing and Q1 exits 1 while they
   do. Fixing S5 is a one-line CSS-declaration parse and is a different decision from auditing;
   fixing F2 means changing the declared set, which mg-5f7c argued should not be mixed with a
   polarity repair and which this audit agrees should not be mixed with an audit of one.
2. **It did not audit `prose_5f7c.py`'s C1/C2/C3 findings** beyond confirming their exit codes
   reproduce. The untracked-file, one-extra-key and nearest-basename repairs are taken as
   **read**, not re-derived. That is the largest hole in this audit's coverage and it is here
   rather than left to be noticed.
3. **It did not re-derive mg-5f7c's B3 measurement** (`{'ON THE LINE': 2, 'BY PROXIMITY': 1}`
   over 3 phrases in 18 files). **Read**, not re-derived.
4. **It did not check mg-a74f's `r16 SHOWN` column or mg-65eb's R1**, both of which mg-5f7c
   explicitly left alone and both of which remain open.
5. **It did not run a browser** (§7.3), and it did not run the arc's other trees.
6. **It did not touch any pre-registration file**, its own or anybody's, after committing it.

---

## Running it

```sh
D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
NODE_PATH="$D/node_modules" sh code/suppression_polarity_audit_40e4/run_all.sh
```

Run it on a **committed** tree — section 6 re-runs mg-5f7c's runner, whose section 4 refuses to
start on a dirty one, and this runner refuses first and says why (§7.1). Sections 1–3 and 5
need only `python3` and `git`; section 4 needs the renderers and exits 3 with the install line
without them, because none of its figures can be produced from the transcripts alone.

**Sections 2, 3 and 5 exit 1 by design.** The findings stand; a runner that went green while
they stand would be reporting the absence of its own results. These exit codes are **not**
pre-registered and the runner says so — this audit pre-registered findings, not exits.

| file | what it is |
|---|---|
| `PREDICTIONS.md` | committed before any script here existed (`93ab336`) |
| `q1_polarity_40e4.py` | the polarity on two axes over 28 constructions, with `six65eb.Shown` in the third column |
| `q2_offsets_40e4.py` | the offset re-derived from a defined true position, over 90 observations in two populations |
| `q3_claims_40e4.py` | the four claims mg-5f7c makes about the repository and about itself |
| `selftest_40e4.py` | 14 controls on this audit's own instruments, including that its population can move |
| `lib40e4.py` | `git show` + `exec`, and nothing that decides anything |
| `out_q1_polarity.txt`, `out_q1_polarity_6fb424f.txt` | the suite on this tree (7 fail closed) and at the anchor (11), so it is shown reporting something else |
| `out_q2_offsets.txt`, `out_q3_claims.txt`, `out_selftest_40e4.txt` | one full run of each |
| `out_run_all.txt` | one full pass, including mg-5f7c's own eight sections nested inside section 6 |

**This audit's `predictions:` commit is `93ab336` on `polecat-c40e4`.** The refinery rebases, so
that sha will differ on `main`; the patch-id will not, and it is the identity to check.
