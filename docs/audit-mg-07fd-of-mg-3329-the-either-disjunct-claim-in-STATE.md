# INDEPENDENT AUDIT — mg-07fd of mg-3329 (`641ef42`)

**VERDICT: CONFIRMED-WITH-REPAIRS.**

Every one of mg-3329's six checkable arms holds against the file. Its `STATE.md` count of
**three rows** is right, its repair is correctly weighted (nothing struck, nothing withdrawn,
no number moved), and its instrument edit is numbers-neutral — I re-ran the instrument at
both revisions rather than reading its claim.

Two things it got wrong, and both are the same defect it was sent to repair, in the two
places it did not look:

* **`STATE.md` HAS A TRACKED RENDERED TWIN, `docs/state-of-the-wall.html`, AND IT CARRIES
  LEDGER ROW 9 IN ITS PRE-REPAIR FORM VERBATIM** (`:380`). It is neither repaired, nor
  flagged, nor on the "deliberately left" list — it is not in mg-3329's candidate space at
  all. So the honest count is **FOUR SITES OVER TWO FILES**, not three over one. The
  precedent naming this exact failure is in this lineage and is explicit: mg-957a repaired
  nine aggregating sentences **"across BOTH files"** and wrote that *"the .html carried the
  identical false sentence verbatim, and fixing only the .md would have been this ticket's
  own failure mode in a second file."*
* **mg-3329's OWN FLAGGED ITEM 1 UNDERCOUNTS.** It reports the `CLAIM` sweep of
  `code/c3_prefix_capture_76b2/` as returning **5**. Mine returns **7** in-policy. The two it
  misses — `lib76b2.py:382–383` and `s2_sweep.py:31` — carry **no matching phrase from its own
  four spellings**, which is the finding its own headline is about, committed inside the flag
  that states it.

That makes this the **SEVENTH** instance of the lineage's standing defect and the **THIRD**
time the thing that was wrong was a **CLEAN CHECK** — mg-3329 falsified mg-fa70's recorded
`greps clean`, and this audit falsifies mg-3329's recorded count of that same directory.

---

## 1. THE `CLAIM` SWEEP, RE-RUN INDEPENDENTLY — AND WHAT I RANGED OVER TO EARN THE COUNT

**COUNT IN `STATE.md`: THREE ROWS — `:116`, `:164`, `:169`. Identical to mg-3329's three.**

A matching count off a narrower sweep is not agreement, so here is the candidate space. The
`CLAIM` is taken to be *any sentence that attributes to `L2`-as-a-disjunction something
established (or refuted) only on one of its disjuncts* — not the phrase.

| # | Sieve run over the whole file | Lines returned | Disposition |
|---|---|---|---|
| 1 | `L2`, `L₂`, `L_2`, `Lemma 2` | `116`, `164`, `169` | all three are CLAIM sites |
| 2 | `disjunct*` (any case) | `72`, `116`, `118`, `164`, `167`, `169` | `72` = "proven **or** empirical", a different disjunction; `118` = L4 branch (iii); `167` = the **disjunctive** per-slot LP value (mg-200d/mg-131e). Three other objects. |
| 3 | `C₃` · `C_3` · `C3` | `15`, `116`, `164`, `169` | `15` is the blanket *"`C₃` unquantified"*, which mg-3329 declares left — see §5 |
| 4 | Content-words with **zero** phrase overlap: `standard.eigenvector`, `dominant standard`, `monotone in the distinguished`, `monotonicity`, `low-conductance prefix`, `prefix capture`, `Cheeger`, `Step 3` | `+ 5`, `60`, `65`, `76`, `110`, `117`, `158` | `60`/`65` mermaid node labels; `5`/`117` = row 10 (**L3**, `125/126`); `76`/`110` = row 3b standard **dominance**, a different row; `158` = probe D. **No new CLAIM site.** |
| 5 | Pointer sites — `row 9`, `rows 9 and 10` | `72`, `164`, `169` | `72` is a **live pointer**, so it inherits the repair; this is the ticket's own positive pattern working |
| 6 | Provenance — `mg-76b2` | `116`, `164`, `169` | nothing new |
| 7 | **The file's tracked rendered twin, `docs/state-of-the-wall.html`** | **`350`, `380`** | **NOT in mg-3329's candidate space — see §2** |

Sieve 4 is the one that has to be run for the count to mean anything, because three of
mg-fa70's thirteen origin sites had no matching phrase at all. It returns seven extra lines
and **none** of them is a CLAIM site. So the three is real *for `STATE.md`*, and mg-3329's
own method warning does not catch it out inside that file.

**SITES, not rows:** within the three rows the claim occurs at **five** repaired sites —
`:116` (row 9's title + evidence cell), `:164` (the contested `either disjunct` sentence, and
the fourth spelling *"(ii) IS CONDITIONAL ON L2"* in the very next sentence), `:169` (the
headline, and the inherited-endorsement clause) — plus **one blanket-scope site deliberately
left** at `:169` (§5, repair **R2**) and one at `:15` (correctly left).

---

## 2. THE FINDING — `docs/state-of-the-wall.html:380`

`STATE.md:13` names it in the file's own header: *"Rich rendered version:
`docs/state-of-the-wall.html`"*. It is **tracked** (`git ls-files` returns it), and this
lineage has repaired it in the same landing as `STATE.md` twice — mg-957a (`d41d18c`) and
mg-55f2 (`276aead`, whose subject ends *"in BOTH files"*).

`641ef42` does not touch it. It is on neither the **FLAGGED, NOT EDITED** list nor the
**CHECKED AND DELIBERATELY LEFT** list, so "not repaired" and "not looked at" are **not**
distinguishable here — which is the exact distinction mg-3329 built those two lists to
preserve.

What the twin carries, unrepaired:

* **`:380` — ledger row 9, verbatim pre-repair**: `L2 standard-eigenvector monotonicity` ·
  `FP✗` · `false as stated` · `2/126`. This is precisely the sentence mg-3329 repaired at
  `STATE.md:116` on the ground that **the `FP✗` is the first disjunct's and `L2` itself is
  `OPEN`, not refuted**.
* **`:350`** — the twin of `STATE.md:72`, *"one is refuted as stated (row 9)"*. This one needs
  **no** edit: it is a **live pointer**, and it will inherit `:380`'s repair automatically —
  the same inheritance that worked for ledger rows 9/10 at the origin. It is listed only so
  that repairing `:380` is known to be sufficient.

The twin contains **no** `C₃` and **no** `mg-76b2` content (`grep -c` returns `0` for both),
so `:164`/`:169` have no HTML counterpart. **The gap is exactly one row.**

**PROPOSED REPAIR R1 — `docs/state-of-the-wall.html:380`. NOT LANDED HERE, and §6 says why.**

CURRENT (exact, one line):

```html
          <tr><td class="rowlabel">9</td><td class="what">L2 standard-eigenvector monotonicity</td><td class="ctr"><span class="kind fpx">FP&#10007;</span></td><td class="ctr"><span class="pill false">false as stated</span><span class="fx">2/126, at the two highest-λ</span></td><td class="ctr"><span class="tag">n=6 data</span></td></tr>
```

REPLACEMENT (mirrors the landed `STATE.md:116`; **`FP✗` kept, `2/126` kept, cell count kept**):

```html
          <tr><td class="rowlabel">9</td><td class="what">L2&rsquo;s <b>FIRST DISJUNCT</b> &mdash; standard-eigenvector monotonicity<span class="fx">&#9888;&#65039; SCOPE REPAIRED: <code>L2</code> is a DISJUNCTION (&ldquo;a dominant standard eigenvector is monotone in the distinguished order, <b>or at least yields a low-conductance prefix</b>&rdquo;), so this <span class="kind fpx">FP&#10007;</span> refutes the FIRST clause and says NOTHING about the second. <b>L2 itself is OPEN, not refuted.</b> STATE.md row 9 / :169 (mg-3329, on mg-fa70)</span></td><td class="ctr"><span class="kind fpx">FP&#10007;</span></td><td class="ctr"><span class="pill false">first disjunct false as stated</span><span class="fx">2/126, at the two highest-λ; L2 as a disjunction: OPEN</span></td><td class="ctr"><span class="tag">n=6 data</span></td></tr>
```

**A SECOND STALENESS IN THE SAME FILE, FLAGGED AND NOT MINE:** the twin says at two sites
that mg-65f5's R1 is *"carried by `mg-a1db`, **NOT applied here**"*. R1 **landed** at
`25cc5b2`. So the twin is behind on two landings, not one, and the correct repair is one
ticket that syncs both — which is a landing, not an audit, and is why R1 is proposed rather
than applied.

---

## 3. THE OVER-CORRECTION ARM — **NOT** COMMITTED. CONFIRMED, AND MEASURED

qfa70's caught draft withdrew *"L3 is not an independent lemma"*, which survives on **both**
branches. mg-3329 did not commit that error, and the check is a count rather than a reading:

| Test | Result |
|---|---|
| Strikethrough (`~~`) occurrences, whole file, before → after | **20 → 20.** Nothing was struck anywhere in `STATE.md` |
| Is the second disjunct anywhere called `false` / `refuted` / struck? | **No.** The words carried are `UNQUANTIFIED` (`:164`, `:169`), `NOT ESTABLISHED` (`:169`, row 7 split (b)), `RELOCATED, not eliminated` (`:169`). All three are the weaker word, which is the correct one |
| `:169` *"L3 IS NOT AN INDEPENDENT LEMMA"* | **Present, unedited.** So is *"the programme carries **three** independent open lemmas here, not four"* |
| `:169` title *"REDUCES `C₃` TO L2"* | **Present.** Correctly so — the LEMMA-count reduction survives on both disjuncts; only the CONSTANT is first-disjunct-only, and the title now says exactly that |
| `:116` row 9's mark | **`FP✗` unchanged.** No ledger floor moves — contrast mg-a1db, where a floor rose `OPEN → U` |
| Aggregating sentence `:72` (*"one is refuted as stated (row 9)"*) | **Still true** of the re-scoped row, and unedited — it points rather than restates |

**The rescue is presented as costly, never as failed** — see §4.

---

## 4. THE INHERITED-ENDORSEMENT CLAUSE — CONFIRMED, AND ON THE RIGHT SIDE OF THE LINE

`:169` now reads: *"**THE `either disjunct` FRAMING IS NOT FREE** … The framing was offered as
the reason the `FP✗` is not fatal … After mg-39bf §2.2 it does **LESS** work than that,
because leaning on the second disjunct means leaning on the branch whose constant is
**UNNAMED IN THE SOURCE**. The rescue is **REAL but NOT FREE**: what the second disjunct buys
is the **LEMMA-COUNT** reduction, not a quantified `C₃`."* — and it **cites** mg-76b2 §9 row
7's `(a)`/`(b)` split rather than asserting the framing, `(a)` `PROVEN` / `(b)`
`NOT ESTABLISHED`.

*"Costs something"* and *"does not work"* were the two errors available. The landed text says
**REAL but NOT FREE** and `NOT ESTABLISHED`. It says the true one.

---

## 5. NO NUMBER MOVED — VERIFIED BY MULTISET, NOT BY READING

| Check | Result |
|---|---|
| Numeral multiset of `STATE.md`, before vs after | **`0` numerals removed.** Nothing in the file changed value |
| Numerals **added** | All are ticket ids (`3329`, `76`, `70`, `39`), section refs (`3.2`, `2.2`, `12`), `STATE.md` line refs (`164`, `169`), row `9`, and `.tex` line refs (`560`, `566`, `40`, `325`, `500`, `525`, `552`, `553`, `562`) — plus **two genuine figures**: the `603`-line source and the `5×` count of *"low-conductance"* |
| Are those two figures labelled? | **Yes, at the claim:** *"the source is not in this repository, so this row carries the figure on mg-fa70's record and mg-3329 did **NOT** re-verify it at the `.tex`"*. I cannot check them either — the `.tex` is not in this repository — and they are recorded here as **inherited, unverified by this audit** |
| File length / table integrity | **210 lines**, and the **pipe count is identical at every one of the 210 lines**. No `STATE.md` line reference anywhere in the corpus moves |
| `:169` clause (1) — *"under L2's second disjunct there is no `C₃` either, because the prefix is the output"* | **BYTE-IDENTICAL.** The new material is **appended beside it** as a parenthetical, not folded into it, exactly as the ticket required |

**ONE UNANNOUNCED FOURTH EDIT AT `:169`, AND IT IS A CORRECTION mg-3329 DID NOT CLAIM CREDIT
FOR.** The commit itemises a three-way split; there is a fourth textual change. Before:
*"…because the prefix is the output. mg-94c3 confirms **it** at **1032 of 1032** primitive
posets exhibiting L2's **first** disjunct…"*. After: *"…confirms **the `C₃^(III) = 1`
statement** at 1032 of 1032…"*. The insertion forced the pronoun out — but the old `it` bound
to a sentence about the **SECOND** disjunct while the population is the **FIRST** disjunct's,
so the substitution repairs a real dangling referent. **No figure moves; `1032 of 1032` and
`0.2603` are untouched.** Recorded because an unlisted edit in a landing that says "three
rows and only three" is the kind of thing that should not be found by the next reader.

**RESIDUAL — REPAIR R2, `STATE.md:169`.** One blanket *"under L2"* survives that makes a
**measured** assertion, and mg-3329 declares it left: *"a NEGATIVE claim erring CONSERVATIVE,
converting an unknown into a refusal rather than a licence."* The disposition is **stated**,
which is what §6 asks of it, and the direction of error is safe. But it is the odd one out of
three parallel texts, and the other two were scoped **in this same landing**:

| Site | How the same sentence is scoped after `641ef42` |
|---|---|
| `STATE.md:164` | *"and **mg-94c3's measurement** makes that substitution **FALSE** rather than merely unlicensed"* — scoped by attribution |
| `s1_chains.py` E3 guard | *"…is **measured** at 1.500, 1.473, 1.990, 2.386 … and exceeds 1 at **1023 of 1032** posets (mg-94c3 s3). Substituting 1 here is FALSE"* — scoped by population |
| **`STATE.md:169`** | *"because `C₃^gap` is *not* `1` **under L2**, so the substitution is **FALSE**, not merely unlicensed"* — **blanket** |

The `1023/1032` is measured on the **first-disjunct** population. On a poset satisfying only
the second disjunct, `C₃^gap` is **unmeasured**, so there the substitution is **unlicensed**
but not demonstrably **FALSE** — a claim of the same shape as the five that were repaired,
pointing the safe way.

CURRENT:

> and the measurement above is what **closes** the door, because `C₃^gap` is *not* `1` under L2, so the substitution is **FALSE**, not merely unlicensed.

REPLACEMENT (**the door stays shut on both branches; only the KIND changes**):

> and the measurement above is what **closes** the door — on **both** branches, with the KIND at each: on L2's **FIRST** disjunct `C₃^gap` is *not* `1`, and that is where the `1023 of 1032` was measured, so there the substitution is **FALSE**; on the **SECOND** disjunct `C₃^gap` is **UNMEASURED**, so there it is **UNLICENSED**. Either way it is refused, and only the first half is a measurement.

---

## 6. mg-3329's OWN SCOPE PARAGRAPH, TESTED AGAINST THE FILE — 7 OF 8 EXACTLY TRUE, 1 FALSE

The ticket says to take nothing in it on report. Every checkable assertion, re-run:

| # | mg-3329's claim | Verdict |
|---|---|---|
| 1 | mg-a1db's five edits are `:13/:74/:76/:79/:81` | **TRUE**, exactly those five hunks |
| 2 | `:164` and `:169` are byte-identical across `25cc5b2` | **TRUE** — both `sha1`s match pre- vs post-a1db |
| 3 | File stays at 210 lines, every table row keeps its pipe count | **TRUE** at all 210 lines |
| 4 | `s1_chains.py` reproduced its committed output **byte-identically before** the edit | **TRUE** — re-run at `641ef42^` in isolation, `diff` empty |
| 5 | After the edit the regenerated output differs at **exactly three lines, all label text** | **TRUE** — and re-running the landed script now still reproduces `out_s1_chains.txt` byte-identically. Every `eps_dem`, ratio, count and guard verdict unchanged |
| 6 | `s2`/`s3` do not import `s1_chains`; chain (I)'s `needs` is never printed | **TRUE** — no import; `needs` is stored at `:52` and read nowhere |
| 7 | Flagged items 2 and 3 exist as stated (`mg-9461.md:102`, `:328`; `a3_currency.py:210/:217/:241` + `out_a3_currency.txt:89/:95/:107`) | **TRUE** at all nine line references |
| 8 | Flagged item 1: *"grep for the CLAIM returns **5**"* in `code/c3_prefix_capture_76b2/` | **FALSE — it returns 7** |

**ITEM 8, THE FALSE ONE.** mg-3329's five are right and I reproduce them
(`s2_sweep.py:2`,`:57`; `out_s2_sweep.txt:2`; `s4_budget.py:85`; `out_s4_budget.txt:23`), and
`PREDICTIONS.md:68` is an eighth raw hit correctly excluded by its declared *"every
`PREDICTIONS.md`"* policy. **Two more carry the CLAIM with no matching phrase:**

* **`lib76b2.py:382–383` — the load-bearing one.** *"`L2` as the source states it is
  EXISTENTIAL (**"a dominant standard eigenvector is monotone"**), so `'YES'` is a hit for
  `L2`."* It **misquotes the source's own statement of `L2`** by dropping the second disjunct
  — `STATE.md:116` now quotes that source in full, *"…**or at least yields a low-conductance
  prefix**"* — and then defines the instrument's `YES` as *a hit for `L2`*. `YES` is a hit for
  the **FIRST DISJUNCT ONLY**. This verdict is consumed at `s2_sweep.py:154` and
  `s3_c3.py:236`/`:250`, i.e. it is upstream of the `1890 / 3340 / 0` census, so this is the
  one site of the seven where the mis-scoping is attached to a number rather than to prose.
  **No number is wrong** — the population genuinely is the monotone-vector one — but its
  *name* in the code is `L2`.
* **`s2_sweep.py:31`** — *"Without `L2` the conclusion genuinely fails; the theorem is not
  vacuous."* The `(S4)` red drill removes the **first** disjunct only (it sweeps
  **non-monotone** dominant eigenvectors); its refuting posets may satisfy the second, on
  which nothing there is measured.

Both are **flag-scope**, not repair-scope, so R3/R4 below are proposed at the same standing as
mg-3329's own flagged items 2 and 3 — recorded with line numbers so *"not repaired"* and
*"not looked at"* stay distinguishable.

**PROPOSED R3 — `code/c3_prefix_capture_76b2/lib76b2.py:382–383`** (docstring only; the
function's behaviour, its `YES/NO/UNDECIDED` verdicts and every count downstream are
untouched):

CURRENT:

```
    L2 as the source states it is EXISTENTIAL ("a dominant standard eigenvector is
    monotone"), so 'YES' is a hit for L2 and 'UNDECIDED' is silence, not a miss.
```

REPLACEMENT:

```
    L2's FIRST DISJUNCT as the source states it is EXISTENTIAL ("a dominant standard
    eigenvector is monotone in the distinguished order"), so 'YES' is a hit for THE
    FIRST DISJUNCT and NOT for L2 — L2 is a DISJUNCTION and also holds where that
    eigenvector merely "yields a low-conductance prefix", which this function does not
    test (mg-fa70; scope mg-07fd).  'UNDECIDED' is silence, not a miss.
```

**PROPOSED R4 — `code/c3_prefix_capture_76b2/s2_sweep.py:31`** (module docstring only):

CURRENT:

```
          Without L2 the conclusion genuinely fails; the theorem is not vacuous.
```

REPLACEMENT:

```
          Without L2's FIRST DISJUNCT the conclusion genuinely fails; the theorem is not
          vacuous.  The drill removes the FIRST disjunct only — its refuting posets may
          still satisfy L2's second, on which nothing here is measured (mg-fa70; scope
          mg-07fd).
```

---

## 7. SITE 3 DISPOSITION — REPAIRED, STATED, AND ITS NEUTRALITY RE-VERIFIED HERE

`code/chain_selection_9461/s1_chains.py:86` was **REPAIRED**, not left, and the choice is
stated at length rather than silently — including the argument for why it does not re-open
mg-9461. Nothing is orphaned and no ticket is owed.

Sweeping for the CLAIM found **three** strings in that file, not the one flagged: chain (I)'s
`needs` (`"L2 (either disjunct) — Step 3 as written"`, on the **`C₃`-free** chain, which is
where the label asserted precisely the unestablished half), chain (III)'s report-row label,
and the E3 guard message. All three now read `L2's FIRST DISJUNCT`.

**Numbers-neutrality re-verified independently rather than inherited:** I ran `s1_chains.py`
at `641ef42^` in an isolated copy (empty `diff` against its committed output) and at `HEAD`
(empty `diff` against its committed output). The committed output moves at **exactly three
lines**, all of them label text; the `eps_dem` column (`1/50`, `1/100`, `2/15`, `100/1193`),
the ratio column, and the guard verdicts are unchanged. `out_s0_selftest.txt` untouched;
`s2`/`s3` do not import `s1_chains`.

---

## 8. WHAT THIS AUDIT DID NOT DO

`L2` not attempted, `C₃` not re-derived, no mathematics re-checked, no population
re-enumerated, no figure re-measured. **The two `.tex` figures (`603`-line source, `5×`
"low-conductance") are inherited and are NOT verified here** — that source is not in this
repository, so this audit is in exactly the position mg-3329 declared for itself and says so.
mg-9461's ruling not re-opened, mg-94c3/mg-01ea not re-audited, `docs/` not swept beyond
mg-3329's own flagged references and the twin.

**RANGED OVER AND EXCLUDED, so the candidate space is stated rather than implied:** there is
no `roadmap.md` in this repository (`README.md` and `STATE.md` are the only top-level
markdown, and `README.md` contains **zero** `L2`); `docs/state-of-the-wall.html` is the
**only** `.html` under version control, so there is exactly one rendered twin; no
`docs/state-history/` row file exists for row 9 (only row 11); and
`code/state_audit_6a2f/out_audit.txt:1551` quotes row 9's old cell
(*"…false as stated (2/126)…"*) but is a **committed output snapshot of a run at a past
commit** — staled by every `STATE.md` landing alike, in the same class as `PREDICTIONS.md`,
and not mg-3329's to regenerate.

**Nothing landed in `STATE.md`,
`docs/state-of-the-wall.html`, or `code/c3_prefix_capture_76b2/` — R1–R4 are proposals**,
mailed to pm-onethird and carried by **`mg-2f44`**, so that no half is deferred without a
ticket. R1 in particular is withheld deliberately rather than out of caution: the twin is
behind on **two** landings, and deciding whether to sync both is pm-onethird's call, not an
auditor's.
