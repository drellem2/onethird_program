# `mg-76cc` — predictions, written before the run, misses kept as written

Every exit code and every answer in the left-hand column was written **before**
the script producing it was run. Where a prediction missed, **the prediction
stays as written** and the actual is recorded beside it, with why. A
predictions file that records only hits is a file written afterwards.

---

## Exit codes

| script | predicted | actual |
|---|---|---|
| `selftest_76cc.py` | **0** | 0 |
| `r1_kernel.py` | **0** | 0 |
| `r2_reproduce.py` | **0** | 0 |
| `r3_prerepair.py` | **0** | 0 |
| `r4_doccheck.py` | **0** | 0 |
| `run_all.sh` (worst) | **0** | 0 |

`r1`–`r4` exit 0 iff `SELF-ERRORS == 0` **and** `FINDINGS == 0`. A finding here
would mean the repair does not hold, not that the script is broken.

---

## `P1` — the kernel bend reaches `c1`

**Predicted: 24 of 24** of `c1`'s own vertex cells move when `kern_a218.py`'s
`vertices()` is bent. **Actual: 24 of 24.** `r1` books this as a **SELF-ERROR**
if it is anything else — a corruption probe that corrupts nothing makes every
row below it say whatever it likes.

## `P2` — three revisions of `g1`, one bent-kernel clone

| `g1` revision | predicted | actual |
|---|---|---|
| `ef388417` — before `mg-7e58` | exit **1**, names `kern_a218.py` | exit 1, `0/2`, names it |
| `e006581c` — before `mg-76cc` | exit **0**, `0/0`, names it **nowhere** | exit 0, `0/0`, no |
| this repair | exit **1**, names `kern_a218.py` | exit 1, `1/3`, names it |

The middle row is `mg-957f`'s `F-1` reproduced. If it did not reproduce, this
ticket would be about nothing, and `r1` says so as a **SELF-ERROR** rather than
proceeding.

**Predicted for the repaired `g1` in that clone: `1` self-error and `5`
findings. Actual: `1` and `3`. MISS — see below.**

## `P3` — the null clone

**Predicted: exit 0, `0/0`, and `5 of 5` direction probes.** A predicate
restored by making it fire on everything is not restored. **Actual: exit 0,
`0/0`, 5 of 5.**

## `P4` — `mg-7e58`'s four `c1` directions, against the repaired `g1`

**Predicted 4 of 4**, unchanged: exits `0`, `1`, `0`, `0`. Restoring one half
of a predicate is a way to break the other. **Actual: 4 of 4.**

## `P5` — the per-unit deletions

| unit deleted | predicted | actual |
|---|---|---|
| the `kern_a218.py` row of `HALVES` | no finding names `kern_a218.py` | exit 1, `1/2`, **names it nowhere** |
| the both-together row of `HALVES` | fewer findings than the repaired `g1` books in the same clone | `2 < 3` |
| the kernel row of `PROBES` | the probe population shrinks | `4 of 4`, down from `5 of 5` |
| the one-line repair inside `measurement()` | **exit 1**, `g1`'s own kernel probe MISSes | exit 1, `0/1`, `4 of 5`, it MISSes |

The last is `F-1` put back on an otherwise unmodified tree. A gate that does
not catch the defect being repaired is a claim.

## `P6` — `G-3`, raw

**Predicted: 1 of 5** committed outputs reproduce byte for byte, over **9**
differing lines — 5 in `out_g1_provenance.txt`, 1 in `out_g2_redo.txt`, 1 in
`out_g3_findings.txt`, 2 in `out_g4_fleet.txt`. **Actual: 1 of 5, 9 lines, and
that exact split. Right number, wrong derivation — see below.**

`mg-957f` predicted `2 of 5` here and got `4 of 5`; it had found the
`HEAD[:8]` interpolation in `g1` and `g4` and not the prose in `g2` and `g3`.
That population is enumerated here by running rather than by grep.

## `P7` — `G-3`, normalised

**Predicted: 5 of 5** reproduce with the one recorded revision normalised away,
and **0** differing lines unexplained. **Actual: 5 of 5, 0 unexplained, over
10 substitutions on the committed side.**

## `P8` — the impossibility

**Predicted:** the same tree at two different revisions differs from the
committed record at **the same** `(file, line)` positions both times, and both
normalise to 0. **Actual: the same 9 positions, both 0.**

## `P9` — the normalisation is not a blanket

**Predicted: both controls caught.** A figure changed in
`out_g3_findings.txt` and a whole line changed in `out_g4_fleet.txt` must both
survive normalisation as differences. **Actual: both caught.**

## `P10` — the pre-repair predicates, same inputs

**Predicted:** `0` inputs where an older predicate catches a **real** defect
and this one is silent, and `0` non-defect inputs on which this repair fires.
**Actual: 0 and 0.**

**And predicted, as the interesting row rather than a failure:** `g1` at
`ef388417` exits **1** on inputs that are **not** defects — the unmodified tree
included — because its file-sha predicate fires whenever `c1_branching.py`'s
sha moved. That is `mg-321d`'s `G-1`, and it is why *"the new predicate must
catch everything the old one caught"* is the wrong rule and *"…everything the
old one caught **that was real**"* is the right one. **Actual: `ef388417`
exits 1 on four of the five inputs, three of which are not defects.**

## `P11` — the four scripts this repair never opened

**Predicted: 0 differing lines** for each of `selftest_58da.py`, `g2_redo.py`,
`g3_findings.py`, `g4_fleet.py`, run end to end with `lib58da` before and
after, compared under the same normalisation. **Actual: 0, 0, 0, 0 — and
identical exits and totals, `0`, `0`, `0`, `1` with `g4`'s two.**

**Predicted `12` `run_c1` call sites in those four scripts. Actual `11`.
MISS — see below.**

## `P12` — the runner

**Predicted:** the real `run_all.sh` with five green stubs exits **0**; with
one stub made red it exits **1**. **Actual: 0 and 1.**

## `P13` — the document, checked against the runs

**Predicted: 0** figures of the form *"N of M"* in
`docs/repair-mg-76cc-kernel-half-and-five-outputs.md` that appear in no
`out_r*.txt`, and all **3** claim rows true. **Actual, on the first run: 1
unanchored figure and 1 claim row false. MISS — see below.** After the two
were dealt with: **7 distinct figures, 0 unanchored, 3 of 3 claim rows true.**

---

## The misses, kept as written

**`P2` — 5 findings predicted, 3 booked.** The prediction was derived from the
*check* population: two target forms × three halves is six
measurement-invariance checks, of which four go red in a bent-kernel clone, plus
the kernel null probe missing, makes five. Section (v) books **one finding per
half**, naming the target forms it moved on inside the finding text, so the
four checks are two findings and the total is three. The direction was right
and the grain of the count was wrong — which is the same error, one level up,
as answering a question about a measurement at the grain of a file.

**`P11` — 12 call sites predicted, 11 counted.** The first enumeration matched
any line containing `run_c1(`, and `selftest_58da.py`'s module docstring
contains the sentence *"`run_c1()` really runs the script at the revision it
names"*. A **prose mention counted as a call site** is a population inflated by
prose, which is precisely the failure the *no bare totals* rule exists to
catch, committed by the section applying it. The filter now requires
`L.run_c1(`, and the excluded mention is **printed as excluded** rather than
silently dropped — a population that shrinks quietly is the thing this whole
ticket is about.

**`P13` — the doccheck went red on its own document, twice, and both were
real.** One was the document's fault: §0 quoted `mg-957f`'s *"17 of 17"*, a
figure no run of this repair produces, so a reader could not check it here.
It is now stated without a figure. The other was the *check's* fault: the
"what remains" sentence was present and capitalised, and the comparison was
case-sensitive, so a document that said exactly what it was asked to say was
booked as not saying it. The check now flattens emphasis and case. Both are
kept because they are opposite failures of the same gate, and only running it
told them apart.

**`P6` — right for the wrong reason, kept because that is not a hit.** The
differing-line count was predicted at 9 by counting `HEAD` interpolations in
the four transcripts *as they stood before this repair*. This repair removes
one from `g1`'s section (v) header, which used to print `HEAD[:8]` and no
longer does, and adds a second probe label that does. The two cancel exactly.
The answer is 9 for a different reason than the one predicted, and a figure
that comes out right by cancellation was not derived.

---

## One caught before any conclusion rested on it

`selftest_76cc.py` asserts that each source surgery on `g1_provenance.py`
removes **exactly** the number of lines it declares and leaves the file
compiling, and that `repin_kernel` is exactly **invertible** — applying it and
substituting back gives the original file byte for byte. The first
`drop_kernel_probe` was written to find the probe row by scanning for a line
prefix and deleting to the next `]:`, which removed the wrong span. The
self-test caught it as a line-count mismatch before `r1` (v) had drawn any
conclusion from it. It is an exact source span now, and the assertion that it
is stays.
