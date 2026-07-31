# The mg-ec07 repair — the refusal, the product, and the extent

**Target:** mg-ec07's three open items on `code/hodge_leverage_landing_e1d0/verify_landing.py` —
`E-5` (the blessing path's refusal), `E-4`/`E-1` (the enumeration's grain), `E-2` (the printed
extent).

**Instrument:** `code/hodge_leverage_repair_6df0/`, `sh run_all.sh`, ~2 min, exit 0.
**33 checks, 26 confirmed, 7 measured, 0 refuted.** Predictions written before the first run with
**six misses kept**: `code/hodge_leverage_repair_6df0/PREDICTIONS.md`.
**0 mathematical statements are touched.**

---

## What was wrong, in one sentence

**Two fixes with a scope nobody chose, at two levels:** a one-line remedy applied where the defect
was *found* and not where it *occurs*, and an enumeration over **kinds** where the population is
**sites × kinds**.

---

## 1. `E-5` — the refusal excluded the three rows that license the whole claim

`--reseal` is, in mg-ff3e's own words, *"the only step in this instrument that can make a wrong
document green"*. It refuses while any gate row other than `SITE RECORD` is refuted — and it
identified those rows with:

```python
blocking = [d for ok, d in figure_gate(texts, measured)
            if not ok and "SITE RECORD" not in d]        # a SUBSTRING TEST over the whole row
```

Every row in this gate explains itself **by naming the other rows**. `RECORD PARTITION`'s says
*"…the figures are checked by FIGURE CENSUS and FIGURE ORDER, everything else by SITE RECORD, and
nothing is in neither"*. So:

| | rows selected, of 34 |
|---|---|
| `"SITE RECORD" in row` | **6** |
| `heading(row).endswith("SITE RECORD")` | **3** |

The three that differ are the `RECORD PARTITION` rows — **one per site, and they are the rows that
license "the record is lossless"**. Measured behaviourally, on disk:

| probe | before | after |
|---|---|---|
| `partition` bent lossy, then `--reseal` | **exit 0, BLESSED**, `site_records.txt` changed — the record it wrote was built from a partition that is not the section | **exit 1, REFUSED**, record unchanged |
| the same, with the fix **reverted one statement** | — | **exit 0, BLESSED again** |
| a wrong **live figure**, then `--reseal` | exit 1, REFUSED | exit 1, REFUSED |

The third row is what stops the second from being decoration: the repair widens the refusal without
weakening the half that already worked.

**This is R5 item 3 of mg-ff3e's own instrument, verbatim.** It found `"FIGURE CENSUS" in row` in
its own scoring code, fixed it there with `heading()`, and wrote the remedy down. The same
construct was live **forty lines away** in the file it was repairing.

> **A fix applied at the site of discovery, in a file that contains the same construct elsewhere,
> is a fix with a scope nobody chose.** The remedy was known, written and adjacent. Forty lines of
> distance was enough.

`heading()` is now module-level and is the only way any caller in that file says which row it means.

## 2. The sweep — because the reported line is never the population

The fix is not scored by the line it repaired. `R2` sweeps **429 `.py` files** for the construct,
under a stated rule (a row heading in double quotes as the operand of `in`/`not in`, not keyed on
`heading(...)`, not a quotation of the construct), and every hit is either repaired or carries a
disposition **keyed on its exact line** — so a new occurrence anywhere makes the section red.

**It found two live occurrences nobody had reported:**

| | |
|---|---|
| `repair_835f.py:309` | `hit = [l for l in refuted if "FIGURE CENSUS" in l]` |
| `audit_8916_repair.py:518` | `hit = [l for l in refuted_lines(lines) if "FIGURE CENSUS" in l]` |

Each selects **6 of 34 rows where 3 were meant**. Each feeds a `print` of one example row beside a
probe whose verdict is the real runner's exit code, so **no recorded verdict depends on either** —
that is measured and stated, not assumed, and neither file is edited here: they are other
deliverables' shipped instruments under committed transcripts. They are a ticket, not a
repair-in-passing.

The same sweep over the **sentence** *"a site is a section"* finds it in **6 instrument files, 13
occurrences**. Nobody had checked it at 3 of 3 sites.

## 3. `E-4` / `E-1` — the population is the product

mg-ff3e's enumeration **happened and was well-evidenced**: seven probes, 7 of 7 with a verdict
written before the run and an observed verdict after it. What it was not, was the product. Each
kind was checked at **one site**, and a table with one cell per row reads as complete.

`X1` is what that cost: exchanging the `verdict` and `attempt` **column headers** of `STATE.md`'s
ledger table is mg-9207's `E3` verbatim — the kind mg-ff3e enumerated and **caught at H8** — and at
the `STATE.md` site it was **exit 0 with 0 refuted rows**.

Two changes:

**(a) The site is the row and the header it is read under.** A cell whose column header can be
exchanged in silence is a figure attached to the wrong statement, which is what this gate exists
for. The record grew by **43 characters** and the reseal diff is exactly two lines — the header and
its delimiter. It is *not* the table: see §5.

**(b) The negative control mutates the FILE and re-cuts the sites from it.** The battery this
replaces applied every mutation to the **site text**, which cannot exhibit a site-boundary defect
by construction — it is testing the projection it was handed. That, not the missing cells, is why
the gap could survive an enumeration.

The runner now prints, every run, **12 kinds × 3 sites**:

```
    kind                                              the STATE.md row    §14           H8
    K01 the LIVE figure a reader meets, corrupted     FIRES               FIRES         FIRES
    …
    K09 two COLUMN HEADERS exchanged (E3 -- X1)       FIRES (rec)         n/a           FIRES (rec)
```

**28 of 28 applicable cells fire; 0 silent; 8 `n/a`, each with the reason its derivation failed**
(no marked quotation carrying a figure at that site; no column header line inside §14; a one-line
row has no paragraph to relocate). *"It does not apply here"* and *"it fired"* are different
answers and a reader is entitled to tell them apart.

On disk, against the real runner:

| probe | before | after |
|---|---|---|
| `X1` — STATE.md's ledger column headers | exit 0, 0 refuted | **exit 1**, `SITE RECORD @ the STATE.md row` refuted, every FIGURE row green |
| `X3` — the same kind at H8 (the control) | exit 1 | exit 1 |
| `X2` — two ledger rows that are **not** this site's | exit 0 | exit 0 — **still silent, declared, §5** |

## 4. `E-2` — the extent is measured, not written

The sentence a reader met beside the gate was *"text outside the site is not read, **because a site
is a section**"*. It was true at 2 of 3 sites. It is replaced by a table the code computes:

```
  THE THREE SITES, and WHAT A SITE IS -- derived from the code that computes it:
    the STATE.md row      13,410 chars /   3 line(s)  `framed_row()`  -- 170,098 of 183,508 outside
    §14                   16,647 chars /  72 line(s)  `section()`     --  99,327 of 115,974 outside
    H8                     7,852 chars /  52 line(s)  `section()`     --  13,175 of  21,027 outside
      framed_row = the table ROW and the HEADER LINES it is read under -- not the table's other rows
      section    = the markdown SECTION, heading to the next heading of the same or shallower level
    TOTAL   37,909 of 320,509 (11.8%) inside a record; 282,600 (88.2%) outside every record
```

Each site's anchor is the **function object** that cuts it out, and `EXTENT_OF` is keyed on that
function's name: **a site whose anchor has no declared extent makes the run red.** A new site
cannot inherit a sentence written for a different shape.

**The residue is not closed and the ratio does not move**: 88.2% before, 88.2% after. What closes
is a *kind* — the frame a site's own figures are read under. Saying otherwise would be this same
defect one level up.

## 5. What is NOT covered, with the cost measured

- **The ledger's other rows.** `X2` exchanges the verdict labels of two rows that are not this
  site's, and it is **still silent**. Covering it means making the site the whole table: **22 more
  rows, ~44 000 characters** of unrelated verdicts frozen behind a reseal, so that every edit to
  any attempt-index row is red until someone regenerates the record. That is a trade pm-onethird
  sizes; what this repair owes is the measurement.
- **Two occurrences of the same figure token exchanged** — still the identity map on the bytes.
- **The construct in two other instruments**, §2 — measured, dispositioned, not edited.

## 6. The disturbance this repair causes, stated first among its consequences

**A site is no longer a contiguous substring of its file**, at 1 of 3 sites. Two shipped
instruments encode that assumption and both now stop early:

| instrument | what happens |
|---|---|
| `audit_ec07.py` | `A5b` raises `AssertionError: the edit did nothing`; `A5b`, `A7`, `A8` never run |
| `repair_9207.py` | `R1` still fires **6 of 7** label probes and its seventh **reports** itself (*"the site text does not occur exactly once in STATE.md"*) — its own convention working; `R2` then raises `TypeError: write() argument must be str, not None` — the same convention **missing**, one section later |

Both need the same one line: `with_site(files, name, new_site)`, which the artifact now exports, in
place of `text.replace(site, new, 1)`. Neither is edited here.

**A repair that removes a control owes the measurement it removed**: `A5b`'s claim — one figure
exchange per site on disk, caught by `FIGURE ORDER` with `SITE RECORD` green — is re-derived in
`R3g` at **3 of 3 sites**, through the artifact's own anchor table.

And it changes what the re-run audit's silence means: **`E-5` is absent from its findings because
`A7` never ran**, not because it was answered. The row says so. A finding missing from a section
that did not execute is not an answer, and that distinction is invisible in a findings list.

## 7. The order, because that was the note this ticket carried

mg-ec07's closing note was not about a defect: *"0 of 7 probes exist at any commit before `c7f9079`,
the commit that lands the fix"*. The enumeration was real and checked; what was absent was any way
to see afterwards that it came first.

So the probes and `PREDICTIONS.md` were committed **against the unrepaired artifact**, in their own
commit, with the transcript of that run beside them — `R1b` at that commit reads **exit 0, BLESSED**
— and `R6a` re-derives the ordering from `git log` rather than asserting it here.

## 8. This deliverable is of the same kind as the defect it repairs

It applies a scoped fix and writes sentences about coverage. Both shapes are checked:

| | |
|---|---|
| **is the fix applied everywhere the construct occurs?** | `R2` sweeps the tree, not the file; 4 remaining occurrences, 0 undispositioned, 2 of them previously unreported. `R6b` turns the same sweep on this instrument: one deliberate use, in the row that **measures** the substring test, declared in three places |
| **is every scope sentence true at every site?** | `R5` re-measures the printed extent independently and `R5c` makes an undeclared anchor red. The sentence is keyed to the code's own function name |
| **six misses kept in `PREDICTIONS.md`**, four of them this instrument's own defects | three of the four are the **same shape as the finding**: a state check keyed on a substring of prose, a census that counted its own legend, and a derivation whose silent failure was indistinguishable from a fact about the site — that one made 7 cells read `n/a` and would have shipped a matrix that looked complete |

**The third of those is worth its own line.** The matrix reported **19 applicable cells** in its
first run, with a printed reason beside each `n/a`. The reasons were true sentences about the
write-back and read as facts about the sites. *An enumeration at the right grain still needs its
cells to be real* — the grain was fixed and the cells were empty, which is the finding's next
generation and it was two hours old.
