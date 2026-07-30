# mg-7dd3 — OUTCOMES: every prediction scored, and this instrument's own defects

`PREDICTIONS.md` was written before any script in this directory ran and has not been edited
since — except for two additions made **in the same pre-run sitting** and labelled as such:
section G (the eleventh strike, spotted by a `grep` for `~~`) and section H (added after
pm-onethird strengthened the ticket at 21:15). Neither was written after a run.

## **72 predictions. 66 held. 6 missed. Every miss is kept as written.**

The count is 72 because that is how many rows the file has; scoring them one by one is the
whole point of writing them down, so none is folded into a summary.

| § | held | missed |
|---|---|---|
| A — reproduction (6) | A1 A2 A3 A4 A6 | **A5** |
| B — the corrections at source (10) | all 10 | — |
| C — extent (11) | C1 C2 C3 C4 C5 C6 C7 C8 C10 C11 | **C9** |
| D — the seam (7) | D1 D3 D4 D5 D6 D7 | **D2** |
| E — over-correction (5) | all 5 | — |
| F — mutations (17) | M0 M1 M2 M3 M4 M5 M6 M7 M8 M9 M10 M12 M13 M14 M16 | **M11**, **M15** |
| G — the eleventh strike (4) | G1 G2 G3 | **G4** |
| H — extent width (12) | all 12 | — |

---

## THE SIX MISSES

**A5** — *"`c4_scope.py` and `c5_doc.py` re-run unmodified reproduce their committed outputs;
exits 0 / 1."* The byte-identity held. **The exit codes are 0 and 0.** `c5_doc.py` prints
`C5 TOTAL BAD: 1` and exits 0. I assumed a checker reporting a finding exits nonzero.

**C9** — *"the fraction of `code/species_7d75` that is exonerated ground is between 10 % and
50 %."* **Not measured in that form.** Between writing it and running it I replaced the metric
with a better one — the number of *independent* clauses per hit, which gives **59 % of hits
held by two or more**. The better number does not make the bet correct: I changed the
instrument between predicting and measuring, so the prediction is unscored, and unscored
counts as missed.

**D2** — *"my sweep over all 17 block quotes finds no pair above 45 %."* **One pair, at
52.8 %** — lines 472–473 against 480–481. I read it rather than moving the threshold: it is
two different Aguiar–Mahajan quotations sharing *"the algebra of symmetric functions"*, not a
duplicate. It is also invisible to `s2_seam.py`, both passages being under its 300-character
floor. **The miss is what sent me to the verbatim-run criterion, which is what found B1.**

**M11** — *"delete the marker AND every other clause in the window → exit 1."* **Exit 0.**
Mine, not the checker's: the source reads *"IS CLOSURE, AND ONLY CLOSURE."* and I rewrote only
the first `CLOSURE`, so the per-statement negation still matched. **M11b**, added after the
miss and labelled in the source, exits 1. The prediction stays as written.

**M15** — *"my own detector, unmutated tree → `d2_extent.py` exit 0."* **Exit 1.** Written
before I knew `d2_extent.py` would find anything; it finds four things, so its exit is 1 by
its own design. A prediction that assumed its own result.

**G4** — *"X8 asserted at source → `s1_extent.py` 0, `c4_scope.py` 1."* The first half held.
**`c4_scope.py` exits 0** while printing `C4 STILL ASSERTED AT SOURCE: 1` and
`C4 TOTAL BAD: 1`. **This miss became finding C2** — 25 of the arc's 31 scripts exit 0
unconditionally, including the two mg-a4ef re-ran to corroborate itself.

**The one I said I was most likely to be wrong about was M10** — that the
`CORRECTED AT SOURCE (mg-a4ef …)` marker is not load-bearing. **It held: exit 0.** Deleting
the marker the repair points at does not move the number, because three other clauses hold the
same hit.

---

## THE SEVEN DEFECTS THIS INSTRUMENT COMMITTED, IN THE ORDER THEY HAPPENED

Each is a regression assertion in `selftest7dd3.py` section 7.

1. **`d1_source.py` matched a wrapped sentence against RAW BYTES and failed on a sentence that
   is there.** *"two readers of one audit produced two different lists"* wraps across a
   `> `-prefixed line in §14.2. **This is the identical defect I had already predicted (D4) in
   `s2_seam.py`'s dead `quoted` variable** — committed, in the same session, by the instrument
   that predicted it. Fixed by flattening §14.2 first.

2. **`d2_extent.py`'s lead-in test reported the CORRECTED line as the leak.** Its first
   version extracted words with `[0-9a-z]+`, which collapses `K̄(Π)` and `K(Π*)` both to the
   single token `k` — throwing away the Greek letter and the star, **which are the entire
   correction**. The instrument written to find a claim hiding behind a lead-in reported the
   repair as the defect. Fixed by using the full tokeniser.

3. **`d2_extent.py` counted `shutil.copytree`'s BINARY reads as "the checker read this
   file".** `s1_extent.py`'s control (c) copies a whole tree, so every file in it — including
   `run_all.sh` — showed as opened. **That would have hidden finding A1.** Fixed by recording
   the mode and counting text reads only.

4. **`d4_survivals.py` tested "nothing was lost" against a LIST OF PHRASES** and reported five
   re-wrapped lines as unaccounted-for deletions. A list of phrases is the failure mode this
   whole audit is about. Replaced by a measurement — the longest run of each removed line still
   present at HEAD — which then had two bugs of its own: a flat 6-token bar a 4-token line can
   never clear, and a leading `>` anchoring every run to the blockquote marker.

5. **`d3_seam.py` ranked by similarity ratio, which cannot tell "said twice" from "about the
   same subject".** Two different AM quotations score 52.8 %; §14's two boxes scored 55.7 %.
   The longest shared **verbatim run** separates them cleanly — 6 words against 17 — and the
   control against the document at `ebecd89` confirms the sweep finds the pair mg-73df found.

6. **`d3_seam.py` applied one of `s2_seam.py`'s two reference filters** and reported
   *"mg-af28 §2.6"* as a dangling internal reference. `s2_seam.py` excludes it correctly. A
   checker firing on a convention rather than a defect — which is the exact false positive
   `s2_seam.py`'s own comment says its first version had.

7. **Three `print("… %s …")` calls with no format operator**, one of which is the same defect I
   report against `out_s2_seam.txt` (`56%%` printed literally). Mine crashed; theirs is
   committed.

**Seven defects, five of them the same shape as something this audit reports against the work
it audits.** That is not modesty. It is the strongest evidence available that the shape is a
property of the task and not of the worker — and two of them (2 and 3) would have inverted a
finding if they had survived.
