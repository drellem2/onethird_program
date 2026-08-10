# THE EITHER-DISJUNCT CLAIM, REPAIRED OUTSIDE `STATE.md` AT THREE SITE-GROUPS — and the CHECKED-AND-LEFT lists in this lineage are now wrong at THREE of them

**Work item.** `mg-be0b`, filed by `pm-onethird` off `q3329`'s verdict on `mg-3329` (`641ef42`),
which repaired `STATE.md` at three rows and **flagged rather than edited** the sites that are
other instruments' property. This lands those. Mid-run correction to Group A's inventory
received from `pm-onethird` (off `q07fd`'s audit of `mg-3329`) and **incorporated, not deferred**.

**THE DEFECT, ONCE.** `L2` is a **DISJUNCTION** — *"a dominant standard eigenvector is monotone
in the distinguished order, **or at least yields a low-conductance prefix**"* (`STATE.md:116`,
quoting `spectral_near_ordinal_sum_program.tex:560–566` through `mg-76b2` §2). **That `.tex` is
not in this repository and was not re-read here**; the quote is carried on `STATE.md`'s record,
which carries it on `mg-fa70`'s, which read it at the source. So an unqualified *"under L2"* is
*"under **either** disjunct"* with the words removed. `C₃^(III) = 1` is proved on the **FIRST**
disjunct; on the second the constant is **RELOCATED** into L2's own unnamed *"low-conductance"*,
not eliminated.

**WHAT IS NOT DONE, AT THE TOP, BECAUSE BOTH ERRORS WERE AVAILABLE HERE AND THE OTHER ONE IS
MORE EXPENSIVE.** The second disjunct is **UNQUANTIFIED** — weaker than, and different from,
**REFUTED**. It is **not struck, not called false, and not treated as refuted anywhere** in this
repair. **`REDUCES C₃ TO L2`** and **`L3 IS NOT AN INDEPENDENT LEMMA`** both survive on **BOTH**
disjuncts (`mg-76b2` §9 row 8) and **neither is withdrawn** — withdrawing either was `mg-fa70`'s
own recorded over-correction, and it would re-open a lemma count the programme has banked.
**NO NUMBER MOVES ANYWHERE IN THIS REPAIR.** No figure, count, threshold, census or table entry
changes in any of the three groups; every claim repaired was **true as measured** and
**under-scoped as written**, except where marked otherwise below.

---

## 1. Group A — `code/c3_prefix_capture_76b2/`: `mg-fa70`'s recorded clean check is FALSE, re-verified here

`mg-fa70` §2.1 lists *"`code/c3_prefix_capture_76b2/` (greps clean)"* on its CHECKED-AND-LEFT
list. Re-run rather than taken from `mg-3329`'s report:

```
grep -rn  "either disjunct"    code/c3_prefix_capture_76b2/   ->  0
grep -rnE "under L2|given L2"  code/c3_prefix_capture_76b2/   ->  6
```

**TRUE OF THE PHRASE, FALSE OF THE CLAIM** — and recorded in the same amendment whose headline
finding was *sweep for the CLAIM, not the PHRASE*.

### 1.1 What was repaired (5 sites, 3 files)

| site | read | reads |
|---|---|---|
| `s2_sweep.py:2` (module header) | ``C_3 = 1 given L2`` | ``C_3 = 1 given L2's FIRST DISJUNCT`` |
| `s2_sweep.py:57` → `out_s2_sweep.txt:2` (banner) | `given L2` | `given L2's FIRST DISJUNCT` |
| `s2_sweep.py:31` (the (S4) red drill) | *"Without L2 the conclusion genuinely fails"* | **Without L2's FIRST DISJUNCT** — the drill sweeps NON-MONOTONE dominant eigenvectors, so it removes the first disjunct only |
| `s4_budget.py:85` → `out_s4_budget.txt:23` | *"s2 shows that under L2 it does not degrade anything"* | **under L2's FIRST DISJUNCT** |
| `lib76b2.py:382–383` (`monotone_in_span` docstring) | *"L2 as the source states it is EXISTENTIAL … so `'YES'` is a hit for L2"* | **`'YES'` IS A HIT FOR L2's FIRST DISJUNCT, NOT FOR L2** |

`s2_sweep.py:31` and `lib76b2.py:382` **carry the claim with no matching phrase at all** and are
`q07fd`'s find, relayed by `pm-onethird` mid-run. They are the same defect as the other three,
inside the very instrument whose flag states it.

### 1.2 `lib76b2.py:382` is the load-bearing one, and it is a RENAMING — verified, not asserted

The old docstring **misquoted the source's own L2** by dropping the second disjunct and then
defined the instrument's `'YES'` as *a hit for L2*. `'YES'` is a hit for the **first disjunct**.
That verdict is consumed at `s2_sweep.py` and `s3_c3.py`, i.e. **upstream of the census**, which
is why the name had to be fixed rather than annotated.

**No logic changed and the census is byte-identical.** `1890 YES / 3340 NO / 0 UNDECIDED`
(`out_s2_sweep.txt:36–40`) and `163 of 5230` degenerate top eigenspaces are unchanged, and those
lines are **not among the changed lines of any transcript**. Measured: after the `lib76b2.py`
edit, `out_s1_dictionary.txt`, `out_s3_c3.txt` and `out_selftest76b2.txt` all regenerate
**BYTE-IDENTICALLY** — a library edit that touched behaviour could not have left three
transcripts that read from it unchanged.

### 1.3 `PREDICTIONS.md:68` — an unrepairable occurrence, left deliberately

`code/c3_prefix_capture_76b2/PREDICTIONS.md:68` (`P12`, *"The theorem **C₃ = 1 given L2**
survives every red drill…"*) carries the claim and is **NOT EDITED**. It is a pre-registration
artefact whose value is that it was never touched. Recorded here as an occurrence that stays.
**A second one, which no ticket named:** `code/c3_audit_a94c3/PREDICTIONS.md:61` (`P10`) carries
*"(`C₃^gap > 1` under L2)"* under the same policy and is likewise left.

### 1.4 The numbers-neutrality method, run in the prescribed order

`q3329`'s method, which is the standard here:

1. **Reproduce byte-identically before touching anything.** `out_s2_sweep.txt` and
   `out_s4_budget.txt` both reproduced **BYTE-IDENTICALLY** (sha256 recorded pre-edit).
2. Make the label edits.
3. **Regenerate and confirm the diff is EXACTLY the label lines.** It is:

```
out_s2_sweep.txt   2 changed lines (the banner)          line count 69  -> 69
out_s4_budget.txt  4 changed lines (one reflowed pair)   line count 142 -> 142
```

Every free-standing number in both transcripts is identical before and after (multiset of all
numeric tokens not attached to an identifier: **IDENTICAL**). No `.txt` was hand-edited.

---

## 2. Group B — `docs/OneThird-ChainSelection-mg-9461.md`: the ticket named 2 sites, the claim-sweep found 7

Straight document repair, no instrument involved. `mg-fd7c` (`c20ad80`) repaired `:140`; these
survived it. Seven sites, tabulated in the document's own new `mg-be0b` amendment block: §2.1,
§0 item 5's provenance box, §2.3's table, §3's opening and closing sentences, §7's proposed
`STATE.md` text, and §11.

**Two of the seven are worth naming here.**

- **§7 is the text this document OFFERS for `STATE.md:164`.** It read *"`C₃^(III) = 1` is PROVEN
  CONDITIONAL ON L2"*. `STATE.md:169` now reads *"CONDITIONAL ON L2's FIRST DISJUNCT — A STRICTLY
  STRONGER CONDITION THAN `L2`, WHICH IS A DISJUNCTION"* (landed `mg-3329`). So the proposal had
  come to **disagree with what actually landed**, in the direction of the weaker claim. Repaired
  to agree.
- **§11 read *"everything else is either **proven** (`C₃^(III)`)"***, which drops the conditional
  **altogether** and not merely the disjunct — the most compressed form of the defect in the
  document, in the section a successor ticket reads for its scope.

## 2.1 `mg-fd7c`'s own CHECKED-AND-ALREADY-CORRECT record is FALSE at one of its four entries

`mg-fd7c`'s amendment block records: *"§5.3, §2.3, §6 and §7's «chain (IV)'s own `40/49`
threshold» were checked and are **already correct** — untouched."* Re-run rather than inherited:

| entry | for the L2-scope defect |
|---|---|
| §5.3 | **clean** — record is right |
| §6 | **clean** — record is right |
| §2.3 | **CARRIED IT** — the `C₃^(III)` row of its own four-row table read *"PROVEN flat, under L2"* |
| §7 | never claimed as checked; carried it |

The entry is **false for the L2-scope defect and may well have been true for the `40/49` defect**
— and that is the trap, because the record does not say **which defect** it was checked against,
so a reader takes a clean bill for both. This is the **third** CHECKED-AND-LEFT list in this
lineage found wrong in as many days (`mg-fa70`'s *"greps clean"*, its own §2.1; `mg-fd7c`'s §2.3;
and the two-site inventories both `mg-fa70` and this ticket published). **Do not inherit one.
Re-run it.**

---

## 3. Group C — `code/c3_audit_a94c3/`: UNDER-SCOPED, NOT FALSE — and 8 label sites, not 3

`a3_currency.py` builds its population with `p["mono"] == "YES"`, i.e. **the 1032 primitive
posets exhibiting L2's first disjunct**. Every figure it prints is **TRUE AS MEASURED**; what was
missing is that the site said so. **Nothing is marked false here and no measurement is
restated.** The `C4` finding — `C₃^gap > 1` at `1023 of 1032`, worst `2.386`, even on the branch
where `mg-76b2`'s theorem holds — stands exactly as it was.

The ticket named `a3_currency.py:210/:217/:241` and `out_a3_currency.txt:89/:95/:107`. Re-running
the sweep found **eight** label occurrences in that file, in six places: the module docstring
(`:23`), the `C4` banner, two lines of `C4`'s opening prose, `C4`'s two closing lines, the `C5`
banner, and `C5`'s `P8` verdict. All eight now carry the scope. One more outside the script:
`code/c3_audit_a94c3/README.md:52`'s `P4` row read *"1023 of 1032 posets **that exhibit L2**"*.

**Regeneration, same rule as Group A:** `out_a3_currency.txt` reproduced **BYTE-IDENTICALLY**
before any edit; after, **20 changed lines, all label prose, line count `127 → 127`**, every
free-standing number identical, and `:89`/`:95`/`:107` still land on the three sites the ticket
named. `out_selftesta94c3.txt`, `out_a1_algebra.txt` and `out_a2_dictionary.txt` all regenerate
**BYTE-IDENTICALLY**.

### 3.1 STOPPED AND REPORTED: `a4_census.py` does not reproduce, so its site is NOT repaired

`code/c3_audit_a94c3/a4_census.py:77` and `out_a4_census.txt:42` carry the same claim in a
dependency list — `C_3 = 1  <- L2, Cheeger's hard half, …`. **Repairing it requires
regenerating `out_a4_census.txt`, and step 1 of the method FAILS there**, so per the ticket's own
rule this is reported as a finding and **left untouched**:

```
out_a4_census.txt   census universe: 15 files, 2770 lines   (on disk)
                    census universe: 15 files, 3124 lines   (regenerated today)
                    32 changed lines; line count 183 -> 183
```

**The cause is understood and is not a defect in the script.** `a4_census.py` scans
`docs/OneThird-C3-PrefixCapture-mg-76b2.md` and reports **line numbers inside it**. That document
has been amended twice since the transcript was committed (`ade980b` `mg-01ea`, `bb6a0ff`
`mg-fa70`), growing `2770 → 3124` lines, so every line number the transcript prints has moved and
one quoted excerpt has been rewritten. **The committed transcript is a measurement at its own
commit, not a live property** — the same shape as `mg-3bb9`'s finding about a committed `0 stale`.
Its **verdicts are unaffected**: the L4 census classification and the `mg-200d` census are about
*which* lines mention L4, and the regenerated run finds the same set of statements at new
addresses.

**Why this blocks the repair rather than merely annotating it.** Hand-editing
`out_a4_census.txt` is forbidden (it is an output, not a source). Editing `a4_census.py`'s label
and leaving the transcript stale would put the two in disagreement, and the transcript is what
gets read. Regenerating would silently land 32 lines of unrelated churn as though it were this
repair. So the site stays, recorded. **Fixing it is a separate landing** whose first task is to
decide whether that transcript should be refreshed at all — and it needs `pm-onethird`, because
refreshing it re-dates an audit's evidence.

**Not the same as `1.3`.** `PREDICTIONS.md` is unrepairable **by policy** and should stay wrong
forever. This one is repairable and is merely **not repairable by me under this ticket's method**.

---

## 4. Both directions checked at every site, per the ticket

`q3329` found `STATE.md` row 9 naming **L2** and marking it `FALSE` when what is refuted is L2's
**first disjunct** — an **over**-statement of what is refuted, the mirror of the
over-statement of what is proven. Every site above was read for both. **No over-statement of
refutation was found outside `STATE.md`**, and the sites that could have carried one and do not
are recorded rather than left silent:

- `code/c3_audit_a94c3/out_a4_census.txt:19` and `mg-76b2`'s *"L3 is a consequence of L2"* —
  **CORRECT AS WRITTEN, deliberately left.** That reduction survives on **both** disjuncts
  (`mg-76b2` §9 row 8), so adding *"first disjunct"* here would be the over-correction the ticket
  forbids. Checked, not missed.
- `docs/OneThird-ChainSelection-mg-9461.md` §3's *"If L2 fails in **both** disjuncts there is no
  `C₃^(III) = 2` to fall back on"* — **CORRECT AS WRITTEN**, and the only edit in that paragraph
  is to the label sentence after it.
- `s2_sweep.py`'s own THEOREM statement (`:6–14`) already read *"(this is L2's first disjunct,
  and Step 3 of the architecture)"* **before** this repair, and `s4_budget.py:12`'s chain (I)
  header already read *"L2's first disjunct"*. **The proofs and the code always assumed the first
  disjunct; only the labels over-reached.** That is why nothing computed needed to change.

## 5. This repair, checked for the defect it repairs

A remedy is an artefact of the same kind as the defect, so it is subject to it. Enumerated and
checked:

1. **Does this document, or any note added by it, itself say *"under L2"* unqualified?** Swept:
   every remaining occurrence in the three groups is either disjunct-aware, a **quotation of the
   old text inside a repair note**, or one of the two `PREDICTIONS.md` sites left by policy.
2. **Does it publish a CHECKED-AND-LEFT list of its own — the exact artefact that was wrong
   three times above?** Yes: §1.3, §3.1 and §4. They are stated **with what was checked and by
   which method**, because the failure mode in `mg-fd7c` §2.3 was not a missing check but a check
   whose **scope was unrecorded**.
3. **Does it over-correct anywhere?** The second disjunct is called `UNQUANTIFIED` and never
   `FALSE`; no lemma-count result is withdrawn; no number is restated.
4. **Does it assert anything it did not measure?** The source `.tex` is **not in this repository**
   and was **not** re-read; every quotation of L2 is carried on `STATE.md:116`'s record and is
   labelled as such at each use. `1032`, `1890/3340/0`, `1023 of 1032` and `2.386` are **quoted
   from transcripts verified byte-identical**, not re-derived.
