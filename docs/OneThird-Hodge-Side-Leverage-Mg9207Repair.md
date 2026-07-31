# The mg-9207 repair — the census compares the WHOLE record, not one more field

**Work item mg-ff3e. Landing mg-9207's E2 / E2b / E3: *the invariance MOVED rather than went
away*.**
**Instrument: `code/hodge_leverage_repair_ff3e/`, `run_all.sh`, ~20 min. Committed transcript:
`out_repair_ff3e.txt`. Predicted exit code, written before the first run: 0.**

---

## What was wrong, in one sentence

mg-8eca made the figure census **position-aware for the FIGURES and not for the LABELS**, so
exchanging the two labels instead of the two figures put mg-8aae's own reader-visible defect back
on the page — H8's table saying the `STATE.md` row **shrank** across mg-a2bd — with every figure
token in its declared slot, the length unchanged, and the gate refuting **nothing**, at **3 of 3**
label sites.

**The assignment's instruction is the whole design and it is right:** *do not make it
position-aware for labels — that relocates the defect a third time.*

---

## 1. The generator, because after the third instance that is the only question worth asking

| repair | what the census compared | what the next audit exchanged |
|---|---|---|
| mg-8916 | the **multiset** of figure tokens | mg-8aae exchanged two **figures** — a multiset is invariant under a transposition |
| mg-8eca | the **sequence** of figure tokens | mg-9207 exchanged the two **labels** — a sequence of figures is invariant under permuting what they hang on |
| **mg-ff3e** | **the whole record** | — |

The gate compares a **projection** of the section against a declared expectation. **Whatever the
projection drops is invisible**, and each repair enlarged the projection **by exactly one named
field**: values, then order-of-values. The complement was always *everything else*, so the next
exchange moved into it. Widening field by field buys one generation each, and the fix's author
never sees the next one **because they are looking at the reported one**.

**The only projection with an empty kernel is the identity.** So the projection is made
**lossless** rather than wider.

---

## 2. The repair: cut the record in two along a seam the record defines

`partition(raw)` walks the figure-shaped tokens of the section and returns
`(segments, figures)`, and both halves are compared, both positionally:

| half | compared against | by |
|---|---|---|
| **figures** — every figure-shaped token the section asserts | `ORDER`, by value and by declared slot | `FIGURE CENSUS` + `FIGURE ORDER` (unchanged) |
| **segments** — every byte that is not one of those tokens | the declared record in `site_records.txt`, byte for byte, in order | `SITE RECORD` (new) |

**No field is named, so no field can be left behind because nobody named it.** Labels, table row
headings, column alignment, the text inside a marked quotation, and any field a later editor
invents are in `segments` the moment they are written, without `verify_landing.py` being edited.

Two smaller things fall out of the same cut and are worth naming:

- `figure_sequence` and `assertions` are now **both derived from one `quoted_spans`**. Two
  implementations of the marked-quotation convention is exactly how the two halves would come to
  disagree about which bytes are in neither.
- **exempt from the census is not the same as unchecked.** A figure inside a marked quotation is
  still exempt from the *count* — that convention is kept, with its reason — but it now sits in a
  segment and is frozen there byte for byte. `E8` is that probe.

### And "the two halves are the whole record" is MEASURED

`rejoin(segments, figures) == raw` is a **gate row**, per site, every run. Without it, *lossless*
would be a sentence written beside the code — which is the precise shape both of the last two
findings had.

**D3** puts a kernel back: the segments compared **case-insensitively**, which is a projection and
is the shape of every repair before this one. The `RECORD PARTITION` row goes **red at 3 of 3
sites**. A claim of exhaustiveness that cannot fail certifies nothing.

---

## 3. Measured on disk, against the real runner, with no hook

Every probe is written **to disk** into the real document and scored by running
`verify_landing.py` as a **subprocess**, with **no environment variable set** and the gate never
called in memory — mg-9207's standard, adopted here.

**Scored at GATE-ROW granularity**, because the runner can exit 1 without the gate having seen
anything (mg-9207's `J-3`).

| probe | runner | `SITE RECORD` | `FIGURE CENSUS` | `FIGURE ORDER` |
|---|---|---|---|---|
| **E2** H8's mg-a2bd table labels exchanged *(mg-9207's own, verbatim)* | red | **REFUTED** | CONFIRMED | CONFIRMED |
| **E2b** the `bbe83b5` table's two row labels *(mg-9207's own)* | red | **REFUTED** | CONFIRMED | CONFIRMED |
| **E3** the two historical column headers *(mg-9207's own)* | red | **REFUTED** | CONFIRMED | CONFIRMED |
| **E6** §14's two correction attributions — a site mg-9207 never probed on the label side | red | **REFUTED** | CONFIRMED | CONFIRMED |
| **E7** the `STATE.md` row's two row-history anchor labels — likewise | red | **REFUTED** | CONFIRMED | CONFIRMED |
| **E8** a figure inside a **marked quotation** | red | **REFUTED** | CONFIRMED | CONFIRMED |
| **E9** the three-column table's **alignment**, no figure moved | red | **REFUTED** | CONFIRMED | CONFIRMED |

**7 of 7 red; 7 of 7 caught by the `SITE RECORD` row for that site; 7 of 7 with that site's figure
rows still green; 7 of 7 restorations return the runner to exit 0, sha256-verified.**

The second and third columns matter as much as the first. A widening that made the run red for a
*new* reason while the label check stayed quiet would keep the headline and lose the result — and
the green figure rows are **the artifact's own evidence** that the mutation moved no figure,
asserted by the thing under test rather than by the prober. That is mg-9207's `C4` convention
pointed the other way.

---

## 4. The defect reinstated, at the finest unit

*Demonstrating that a check fires proves the instrument fires unless removing the check makes the
same artifact go uncaught* (mg-8eca's `D4`). And **which unit** is removed is mg-9207's `J-2`: a
deletion test that can only remove a whole function cannot tell two clauses apart. So `(e)` is
**two rows in two calls**, and each is deleted alone.

| deletion | predicted | observed |
|---|---|---|
| **D1** `(e)` deleted whole | silent | **0 of 7 caught** |
| **D1b** only the `SITE RECORD` comparison | silent | **0 of 7 caught** |
| **D2** only the `RECORD PARTITION` row | still red | **7 of 7 caught** |
| **D3** `partition` made lossy (case-insensitive segments) | `RECORD PARTITION` red | **red at 3 of 3 sites** |

D1b is the one that matters: it isolates the new comparison as **the** thing that catches a label
exchange, and D2 shows that `RECORD PARTITION` — which is what licenses the exhaustiveness claim —
is not doing that work and is not a second copy of it.

---

## 5. Every field of every record, not just the one that was reported

*"No field can be left behind"* is a claim about a **population**, so it is measured over the
population. `partition` enumerates it — nobody writes the list — and every segment and every
figure of every site is mutated **alone**:

| site | segments | empty | fired | figures | fired |
|---|---|---|---|---|---|
| the `STATE.md` row | 18 | 0 | **18** | 17 | **17** |
| §14 | 17 | 0 | **17** | 16 | **16** |
| H8 | 27 | 10 | **27** | 36 | **36** |

**62 of 62 non-blank segments and 69 of 69 figures.** The 10 whitespace-only segments are reported
as an **absence with the reason** — there is no character in them to mutate — rather than counted
as passes; their bytes are still compared, so one that acquires content changes the record like
any other.

⚠️ **This is in memory and it is declared a fixture.** *"The gate function returns `False` when
called with a mutated string"* and *"the runner goes red when the document is wrong"* are different
sentences. §3 is the evidence; this is the **map** — and it is the enumeration the assignment asks
for: *what else is of the same kind as the thing I just fixed?*, asked **before** fixing rather
than one generation at a time.

---

## 6. Not scored by its own author

mg-9207's instrument, **unmodified**, re-run against the repaired tree:

- its **E2/E2b/E3 findings go to 0**, from 3;
- its `E` rows now **refute their own prediction of silence** — `0 of 3 label-side exchanges leave
  the gate silent`, where it wrote `3 of 3`. **Its exit is 1 and that is correct**: that is what a
  landed finding looks like from the raising instrument's side, and its predictions are left as
  written;
- **`C3` still holds at 12 of 12** — the `FIGURE ORDER` row is still the *only* gate row that fails
  on a **figure** exchange, after two rows were added to the gate. This is the result most at risk
  from this repair, and it is why the declared record masks figures with a **value-independent**
  marker instead of freezing them in place: a figure exchange must move the *figure* half and
  nothing else.
- **5 of 5** committed transcripts are sha256-identical after every re-run.

**Every one of its rows that moved is accounted for.** Its committed transcript reads *32 checks:
30 confirmed, 2 refuted*; against the repaired tree it reads **32 checks: 25 confirmed, 7
refuted**, and the five that moved are:

| row | why |
|---|---|
| `E2`, `E2b`, `E3` and the `THE INVARIANCE MOVED` aggregate — **4** | each **predicted SILENT and observed FIRES**. This is the finding landing, from the raising instrument's side |
| `S1b` — **1** | it asserts mg-8aae has exactly **one** refuted row; mg-8aae now has ten, for the single reason in the next section |

`C7` and `C7b` were already refuted before this repair and still are: they are `J-3`, untouched.
**No row that was confirmed for a reason other than the defect being present has moved.**

mg-8eca's instrument, unmodified: **exit 0, 0 refuted, 0 findings.** Nothing it demonstrated is
dropped.

### The one place this repair disturbs a prior instrument, reported rather than counted away

**mg-8aae's `A3` can no longer run, and the reason is the repair.** `A3` picks its probe slot by a
**procedure** and controls it first: the slot is blanked length-preservingly and **the runner must
stay green**, so that a fire is attributable to the figure written into it and not to the edit.
After this repair, **blanking any prose makes the runner red** — so the search returns nothing and
reports `no unread prose slot found` at **6 of 6** probe slots. That, plus the three aggregate rows
that depend on it, is 9 of its 10 refuted rows; the tenth is its own `A4` permutation row, already
refuted by mg-8eca.

**This is not G-1 reopening, and the distinction is measurable rather than rhetorical.** mg-8aae's
`A3` is a search for *text at the site that the gate does not read*, and it now finds **none at 3
of 3 sites**. That is the extent of this repair, measured by an instrument that is not its own —
the strongest statement of it available, and it arrives as a refuted row because the instrument
was written when such text existed.

G-1's closure is re-derived by two routes that do not need an unread slot: **mg-8916's own
instrument, unmodified, exits 0** with its U1 wrong-prose probes firing at 3 of 3, and `N10`–`N13`
of the runner's own negative control fire on the same shapes.

**It is a real cost and it is stated as one:** a future auditor wanting `A3`'s method on these
three sections must either reseal around a blanked slot or measure the extent some other way. The
alternative — leaving prose the gate does not read, so that the method keeps working — is the
defect.

---

## 7. The cost, stated

Any edit to these three sections that is not a live measurement makes the run **red** until the
declared record is regenerated: `python3 verify_landing.py --reseal`. That is the fail-closed cost
and it is the same cost the roster already carries — an editor meets a red run for an honest edit.

Three things narrow the reseal, which is the one step that can make a wrong document green:

1. it **refuses** while any gate row other than `SITE RECORD` is refuted, so a section whose
   figures are wrong cannot be blessed by resealing it;
2. what it writes is **text**, so the blessing is a **reviewable diff**. A `sha256` would be
   smaller and exactly as strong — and a hash bump is a rubber stamp with nothing to read;
3. it is not invoked by `run_all.sh`, so it cannot happen as a side effect of a run.

**It is a declaration, not a duplicate.** A duplicate is a second place a *reader* meets the claim
with nothing comparing the two, so one goes stale in silence (mg-a318 `F-1`). The declared record
is read by the gate alone and compared to the document on every run: a divergence **is** the red
run.

---

## 8. What is NOT covered, printed rather than left to be found

- **Text outside the site.** A site is a **section** — the one projection that remains. Unchanged
  since mg-8a5c, stated where a reader meets the gate, and itself gated: `section()` anchors by
  content and `N6` relocates a whole disclosure out of §14 to show the gate notices. Widening it
  to the file is a different trade and is pm-onethird's to size.
- **Two occurrences of the same figure token exchanged.** Still the identity map on the bytes: an
  **empty set**, not a blind spot, and the difference is checkable.
- **What a roster entry MEANS.** `ORDER` says where `10 483` goes and `HISTORICAL` says it is
  *"this file at bbe83b5^"*; nothing checks that sentence against git. Unchanged from mg-8eca, and
  now the widest thing left.
- **The reseal**, as above.

## 9. Two of mg-9207's open items are deliberately NOT touched

- **`J-3`** — the runner's own negative control raises `AssertionError` on edits at its own probe
  sites, and a crash and a fire are the same integer. It **reproduces here at E2** (mg-8eca's
  `transpose` freezes `H8_TABLE` and asserts it occurs once; E2 rewrites those two lines). It is
  **reported with a number and left alone** — it is mg-9207's item, not this assignment's. Every
  verdict in §3 is read from the **gate rows**, which print before the control runs, which is why
  it does not touch the result. The seven probes **added** here report rather than assert, so no
  new instance of it is created.
- **`J-1` / `J-2`** — the extent printed beside `SUMMARY vs ROWS`. Untouched, and confirmed still
  raised.

---

## 10. This deliverable is of the same kind as the defect it repairs

It is a comparison, repairing a comparison, and it compares things. The defect is: **comparing a
record by identity on some fields and position on others, so that whatever is in neither is
silent.** Every comparison this deliverable performs, enumerated — and where a branch cannot
exhibit the defect, **the reason**, because a reason is checkable and an omission is not:

| # | comparison | can it exhibit the defect? |
|---|---|---|
| 1 | `SITE RECORD` — skeleton against the declared record | **Can, and does not.** `==` on whole strings, so its kernel is empty by construction. What makes the string really *be* the whole non-figure half is `RECORD PARTITION`, and D3 shows that row failing when it is not |
| 2 | `RECORD PARTITION` — `rejoin(segments, figures) == raw` | **Cannot.** Equality on two whole strings; there is no field structure to be partial about. Its risk is the opposite one — being unfalsifiable — and **D3 is the answer to that**, not to this |
| 3 | R1's scoring of probe verdicts | **DID — twice, and both are kept.** `"FIGURE CENSUS" in row` matched the `SITE RECORD` row's own explanation, which *names* the other rows, so 7 of 7 probes were scored as having broken a figure row. And mg-9207's finding **IDs** were matched by prose, so `J-3`'s text — *"and E2 below where the gate saw NOTHING"* — counted as an E2 finding still standing. Both fixed by keying on the **heading** and on the **ID** rather than on the line |
| 4 | R3's population — segments and figures from `partition` | **Cannot** in the field-by-field sense: nothing is named, the population is derived. Its real limit is that it is **in memory**, declared in its own heading rather than left to be found |
| 5 | R4's re-run scoring | **Can.** Narrowed: rows are counted from their `[MARKER]`s rather than parsed out of a bottom-line sentence whose wording differs between the four instruments, and findings are identified by ID. This one is real and is stated rather than dressed up |
| 6 | the frozen-transcript check — `sha256` before and after | **Cannot.** A hash over a whole file has no field structure |

**Two of the six could exhibit it and are shown not to or narrowed; one DID, twice, and its own
attribution rows caught it; three cannot, each with the reason.** The one that caught its own
defect is the point: the check that says *which row caught the probe* is what made a comparison
keyed too widely visible, in the same run.
