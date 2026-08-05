# mg-8af0 — predictions for the repair of mg-fcb2's F1, F2 and F3

**Committed before a single line of this repair's code exists.** Nothing below is edited after a
result comes in. A refuted prediction is a result and stays on the page with the result beside it.

Target: mg-fcb2's independent audit of the merged mg-e35b repair (`5f542f0`). Three findings are in
the ticket's *WHAT TO DO*:

* **F1** — `controls.py:1927` supplies `(N, N)` for *"the named load-bearing site is corrupted on
  %d/%d posets"*. Same expression twice; the count cannot move, and the sentence is false one poset
  outside the population it has been run on.
* **F2** — `verify_e35b.py:402` scores `forced == 3 and len(table) == 11`, where `table` is the
  literal defined twenty lines above it. **This is the one that matters.** A row that scores against
  a literal reports the same verdict whatever the input; it has never been shown capable of
  reporting anything else, and it is why F1 survived a table headed *"EVERY COUNT THIS REPAIR
  PRINTS"*.
* **F3** — *"no ridge in >= 3 facets, I4 zero"* is labelled `COULD MOVE` and cannot move at any n.

**Order.** F2 is repaired first, in its own commit, and F1 second. Repairing F1 while the verifier
still scores against a literal leaves the mechanism that hid F1 fully intact.

---

## What is NOT a prediction — measurements already taken

Recorded here so that nothing below is read as forecast when it is not. Before writing this file I
ran four probes against the tree under repair. Their answers are **facts on the page already** and
are excluded from the scoring table:

* **M-1.** The named site is corrupted, at the grain `mutation_applied_at_site` uses (the ORDERED
  facet list built by `le_to_facet` differs), on **86 of the 86** posets of the shipped population
  (`n` in 2..5). So the shipped figure `86/86` is *true* — the defect is that it is not computed.
* **M-2.** At the stronger grain (the facet **SET** differs, not merely its order) the answer is
  **82 of 86**, not 86. The two grains differ by 4 posets. Any figure I print names which one it is.
* **M-3.** `all_posets(1)` returns one poset; both facet maps return the empty chain on it, so the
  site is not corrupted there. On the widened population the truth is **86 of 87**, against the
  `87/87` the shipped expression would print.
* **M-4.** There are **32** `%`-format sites carrying at least one `%d` lexically inside
  `negative_control_incidence`, carrying 173 `%d` conversions between them. This is the population
  the completeness row will be scored over; I measured it before choosing it, and say so.

Everything below this line was written without running anything else.

---

## The decision mg-fcb2 left open (its OPEN 4)

> *Whether admitting n = 1 is the right fix for F1, or whether the count should simply be measured
> over the population it has, is a decision about the battery's scope and not one this audit should
> make.*

**Decided here: measure it over the population the section declares (`n` in 2..5); do not widen.**
Widening moves every other count in the section and every figure in the committed artifact, to fix a
defect that is not about the range — the defect is that the numerator is not computed. The widened
population is not discarded: it becomes the **constructed input that flips the repaired figure**,
which is the only way to show the figure is now capable of moving.

---

## Predictions

### On F2 — the scoring mechanism

**P-1.** The repaired completeness row derives its population from the **source of
`negative_control_incidence`**, not from a list in the verifier. Free names read by its scored
condition will include a name bound from that parse, and `len(table) == 11` will not appear
anywhere in the file.

**P-2.** At the F2 commit — F1 **not yet repaired** — `verify_e35b.py` exits **1**, with exactly
**one** REFUTED row, and that row is the structural-tautology row naming `controls.py`'s coverage
site. This is the point of the ordering: the control fires on the real tree, on a real defect, in a
committed transcript, before the defect is fixed. *If it exits 0 at that commit, the mechanism has
not been shown capable of failing and the repair is worth nothing.*

**P-3.** At the F1 commit the same row goes green and `verify_e35b.py` exits **0**.

**P-4.** Against a copy of `controls.py` with one extra count-bearing print injected and the
verifier untouched, the completeness check reports exactly **1** unclaimed site and REFUTES. This is
mg-fcb2's F2 demonstration run in the other direction, against the repair.

**P-5.** Against a copy with one anchor's sentence deleted, the completeness check REFUTES in the
**other** direction (an anchor claiming no site) rather than passing silently. I expect the first
form of my check to get exactly one of these two directions and not both.

**P-6 (risky).** Classifying all 32 sites will turn up **at least one** count in the section whose
verdict is FORCED and which mg-e35b's 11-row table does not list at all.

### On F1 — the count

**P-7.** After the repair the coverage sentence prints **`86/86`** on the shipped population — the
same characters as before — and `controls_output.txt` is **BYTE-IDENTICAL** to the committed one.
A repair that changes no printed figure is the expected outcome here and is why F1 needed an
instrument rather than an eye.

**P-8.** The same repaired expression, evaluated on the widened population, prints **`86/87`** where
the shipped one prints `87/87`. (The two figures are M-3; what is predicted is that the repaired
expression is what produces them.)

**P-9.** The no-op construction — `le_to_facet_offbyone := le_to_facet` — makes the repaired figure
print **`0/86`** where the shipped one prints `86/86`.

### On F3 — the label

**P-10.** Over every poset with `n <= 6` under **both** facet maps — **810** families, being
`405 = 1+2+5+16+63+318` posets up to isomorphism times 2 maps — the largest number of facets sharing
a ridge is **2**, and the number of families with a ridge in `>= 3` facets is **0**.

**P-11.** The forcing generalises past the two maps: **any** facet family whose members are chains
of masks of sizes `1, 2, ..., n-1` has ridge multiplicity at most 2, because a ridge omits the
level-`k` mask and the two masks bracketing it differ in exactly two elements, leaving exactly two
candidates to re-insert. So I4's zero is FORCED at every n, and *"its zero is the only one of the
four that is a result"* is false in `controls.py` and in `verify_e35b.py`'s V4b alike. Both are
corrected.

### On this repair's own instruments

**P-12.** My completeness check fires on **me** the first time it runs — an anchor matching two
sites, or a site I failed to claim. The failing transcript is committed beside the passing one
rather than replaced.

**P-13.** `face_geometry/run_all.sh` exits **0** after all three repairs and `probe_output_n6.txt`
is byte-identical.

### Exit codes, all predicted before anything is written

| script | predicted |
|---|---|
| `verify_e35b.py` at the F2 commit | **1** |
| `verify_e35b.py` at the F1 commit and after | **0** |
| `flips_8af0.py` (the constructed inputs) | **0** |
| `forcing_8af0.py` (F3's counting argument) | **0** |
| `run_all.sh` (this directory) | **0** |
| `face_geometry/run_all.sh` | **0** |

---

## What this repair will NOT do, stated in advance

* **F5 is not repaired here.** mg-fcb2's gauge standard disqualifies `NEGATIVE CONTROL 2`'s M1 and
  M3. That is a change to a different section's rows (mg-fcb2's OPEN 2) and is not touched.
* **F6 is not repaired here.** `code/face_geometry_audit_fcf1/audit_nc4.py:41` is another tree's
  instrument (mg-fcb2's OPEN 3).
* **The population is not widened to n = 1** — see the decision above.
* **F4 is not in the ticket's WHAT TO DO.** Its subject — the `why` string beside *"detector says
  NOT-GAUGE on 288 of 297"* — sits inside the very table F2 makes me rewrite, and mg-fcb2 showed the
  sentence is false with the substitution **reached**. I will correct that one string and say so
  here rather than leave a sentence I have read and know to be false inside a table I am rewriting.
  No other part of F4 is addressed.
* **No scoring change to row I4.** Its surviving forced clause is deferred to its own item by
  mg-e35b and stays deferred.
