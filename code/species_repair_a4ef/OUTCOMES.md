# mg-a4ef — OUTCOMES: 22 predictions, 5 missed, and the misses are kept as written

`PREDICTIONS.md` beside this file was written **before any edit and before any run**.
Nothing in it has been touched since. This file scores it.

mg-73df's note to whoever took this ticket: *"predicted all 60 battery cells before running
them, missed 4, and KEPT THE WRONG PREDICTIONS AS WRITTEN. That is the standard for this
repair too: predict, then record what you got wrong rather than adjusting the prediction. A
claim of compliance is cheap; a recorded near-miss is not."*

**Score: 17 of 22 held, 5 missed.** The most interesting miss is **P3**, which was my single
declared beyond-brief bet, and it was **wrong**.

---

## The scoreboard

| # | prediction | outcome |
|---|---|---|
| **P1** | X3 asserted at exactly 2 places in `species_7d75` — `t6:149` and `out_t6:66` | **HELD**, exactly those two |
| **P2** | X6/X7 asserted at exactly 2 places, `t6:15` and `t6:16` | **MISSED** — see below |
| **P3** | `y(i) ≤ y(j)` still asserted at source in `species_7d75`, ≥1 hit | **MISSED — 0 hits.** See below |
| **P4** | none of the other seven stricken statements asserted in `species_7d75` | **HELD**, 0 each |
| **P5** | `species_repair_6f61` and `species_remainder_f8fa` come back 0 | **HELD** |
| **P6** | my own tree trips my own detector via `stricken_a4ef.py` | **HELD**, and worse than predicted — see below |
| **P7** | Y2 is at source too, exactly 1 occurrence in the code trees | **HELD** — `t4_one_operation.py:22`, which no list named |
| **P8** | after the fix, 0 plain-isomorphism readings across document and code | **HELD** |
| **P9** | re-running `species_7d75`: exactly one committed output changes | **HELD** — only `out_t6_fock_and_record.txt`; the other six byte-identical |
| **P10** | every `TOTAL BAD` in that tree stays 0 | **HELD**, T1–T6 all 0, 759-assertion self-test unchanged |
| **P11** | the two Y5 docstring fixes change no committed output | **HELD** — `out_r2_columns.txt` byte-identical after the 40→45 fix |
| **P12** | `CHECK_DOC: PASS (0 problems)` after the §14 deletion | **HELD** |
| **P13** | in `species_repair_6f61` only `out_check_doc.txt` changes | **HELD** |
| **P14** | mg-a61f's battery re-run **unmodified** is still byte-identical | **HELD** — 456 328 assertions, `A4 TOTAL BAD: 1`, 0 elsewhere, `git status` clean |
| **P15** | `w3_scope.py` still reports 12 against `83ac472`, PASS now | **HELD**, both |
| **P16** | after the deletion, no block-quote pair above 40 % | **HELD** — worst pair now **5 %**, down from 56 % |
| **P17** | the miscount of the banner has no other occurrence | **HELD** |
| **P18** | §14.3 needs no edit; the sentence it quotes is in the surviving §14.2 | **HELD** — §14.3 is untouched by this repair |
| **P19** | no passage says *"an eighth defect, if there is one"* or calls the filing *"shelved"* | **MISSED on the first half** — see below |
| **P20** | I will find at least one defect in my own checker | **HELD**, and there were **four** |
| **P21** | mg-73df's committed outputs stop regenerating byte-identically, and I will not regenerate them | **HELD** — see the note at the end |
| **P22** | Y2 stays wording; no new mathematics | **HELD** |

---

## The five misses, as written and not adjusted

### P3 — my one declared beyond-brief bet, and it was wrong

I predicted the stricken inequality direction `y(i) ≤ y(j)` was **still asserted in ASCII in
`code/species_7d75`**, on the reasoning that a braid-cone docstring is exactly where an
uncorrected quotation survives. **It is not there at all.** The only occurrence in any code
tree is `species_repair_6f61/r3_quotes.py:122`, which is the file that *compares* the
extracted quotation against the document's and is therefore quoting it in order to correct
it.

I record this as the most useful miss of the five, because the reasoning that produced it is
the same reasoning that produced **P7**, which was right and found `t4_one_operation.py:22` —
a Y2 occurrence at source that no brief and no previous list named. **The method was sound
and this particular bet lost.** Predicting a specific location is cheap; the value was in
scanning the whole list against the whole tree, which is what actually found both.

### P2 — off by one, and it is a property of my own instrument

I predicted the AM §17.5 quotation would be asserted at **2** places, `t6:15` and `t6:16`,
because that is how mg-73df's line-by-line detector reported it. Mine reports **1**, at
`t6:15`. The sentence is one sentence wrapped over two lines, and this instrument matches
across line breaks, so a wrapped sentence is **one hit at the line it starts on** rather than
two hits at two. The prediction was written against the previous instrument's counting rule
and I changed the rule. Recorded rather than reconciled.

### P19 — the first half is wrong, and the reason matters

I predicted that after the fix **no** passage would say *"an eighth defect, if there is
one"*. One still does: **§14.2**, which says *"An eighth defect, if one exists, ..."*.

**And it should.** §14.2 is the surviving copy, it is the prediction mg-6f61 made before
mg-f8fa ran, and §14.3 answers it **by name** — *"§14.2 predicted that a further defect, if
one existed, would be outside every beam"*. Editing §14.2 now would be **tidying a prediction
after its outcome is known**, which is exactly what this arc's standard forbids and exactly
what this file exists to not do.

**This makes mg-73df's own check over-broad.** `c5_doc.py`'s rule is *"no passage still says
'an eighth defect, IF there is one' after 14.3 reports it found"*, with no exception for the
passage §14.3 resolves — so it reported `*** NO ***` on **2** passages before this repair and
still reports it on **1** after, and the only way to clear it would be to rewrite a
prediction. `s2_seam.py` replaces the rule with the precise one: **every occurrence must lie
inside §14.2**, the passage a later section resolves by name. That passes, and it would still
have caught the deleted copy, which sat outside the exchange.

### P6 — right, and the reality was worse

I predicted my own list module would trip my own detector. It did. I did **not** predict that
the first version of the detector would report **19 hits of which 14 were false positives** —
`check_doc.py`'s own `STRICKEN` table, `w3_scope.py`'s `FORBIDDEN` docstring, and
`r1_smallest.py`, the file whose entire purpose is to **refute** X1, all read as asserting the
statements they carry in order to correct them.

### P20 — right, and there were four, not one

Kept on the record in the kernel's own comments:

1. **No per-statement negation.** One global marker regex, so a file quoting a claim to refute
   it read as asserting it. 14 false positives. Fixed by adopting mg-73df's three-way rule —
   name a repair, negate **this** statement, or sit in a declared table — rather than
   re-deriving a rule two workers had already narrowed twice after recorded false negatives.
2. **Flattening without masking `print()` scaffolding.** Between *"axiom with"* and *"0
   failures"* sit the characters `")` and `print("`, which no whitespace-tolerant pattern
   crosses. The instrument written to catch `t6_fock_and_record.py:149` **missed
   `t6_fock_and_record.py:149`**.
3. **The mask blanked newlines too**, so every masked scaffold cost one line of the count and
   the first hit was reported **30 lines above where it is** — line 119 for a sentence on line
   149. A detector with a wrong line number is a detector a reader cannot check.
4. **Two own-negation regexes exonerated their own sentences.** X2a's was a bare `PROVED`,
   which matches case-insensitively inside *"not **proved**"*; X2c's was a bare `located`,
   which matches inside *"**not located**"*. Both self-exonerating, both caught by
   `selftesta4ef.py` section 6 — which is why that section tests each pattern against **both**
   the stricken form and the corrected form.

A fifth, smaller: `flat()` and `_offsets()` disagreed on leading whitespace. Two flatteners
that disagree is one flattener you cannot reason about.

---

## mg-73df's instrument, re-run against the repaired tree

`code/species_audit_73df/run_all.sh` re-run **unmodified** now reports, from an instrument
this repair did not write:

| | before | after |
|---|---|---|
| `c4_scope` still asserted in `code/species_7d75` | **4** | **0** |
| `c4_scope` at `83ac472` (its control) | 8 | **8**, unchanged — the detector still detects |
| `c5_doc` near-duplicate block quotes | **1 pair at 56 %** | **none** |
| `c5_doc` banner back-reference | *"five" vs "Eight"* | **no back-reference left** |
| `c5_doc` the filing described as shelved | **both present** | **consistent** |
| `c5_doc` `r2_columns.py` docstring | *says 40, prints 45* | **says 45, prints 45** |
| `c5_doc` `C5 TOTAL BAD` | 4 | **1**, and that one is P19 above |
| `c4_scope` `C4 TOTAL BAD` | — | **0** |

**Those two regenerated outputs are committed here** as `out_c4_scope_73df_after.txt` and
`out_c5_doc_73df_after.txt`, beside this file — the same convention `w3_scope.py` uses with
`out_w3_scope_before.txt`.

**`code/species_audit_73df`'s own committed outputs are left exactly as mg-73df filed them
(P21).** They are the record of what that audit found when it looked, and overwriting them
with `no near-duplicate block quotes` would delete the evidence for the ticket this repair
closes. So `code/species_audit_73df` will **not** regenerate byte-identically after this
commit, and that is deliberate and is stated here rather than left for a successor to trip
over.
