# `code/species_extent_d633` — the extent, measured; and the check a strike needs

**Work item:** mg-d633. **Repairs:** mg-7dd3 (`798afb7`), findings **A1**, **A2**, **B1** and
**C1**, against `106e121` (mg-a4ef).

```
sh code/species_extent_d633/run_all.sh          # ~2 min, no network
```

## What this is for

mg-a4ef made every checker **print its own extent**. That is the right structural remedy: a
total that names its population cannot turn *"not examined"* into *"examined and clean"*.
**It also moves all of the trust to one line per checker**, and mg-7dd3 measured those lines
and found two of four **wider than what the code reads** — which is worse than printing no
extent at all, because a bare `TOTAL BAD: 0` invites the question *of what?* and an extent line
answers it.

So this tree does two things.

1. **It measures every extent line, and probes every one from both sides.**
2. **It adds the one check no per-section checker can do**: a claim struck in a document must
   not stand un-struck elsewhere **in that same document**.

## The repairs, and which kind each was

| finding | checker | what was false | repair |
|---|---|---|---|
| **A1** | `s1_extent.py` | *"the exclusion cannot grow unseen — 5 file(s)"*; the real exclusion was 9, four `run_all.sh` dropped by an extension filter named nowhere | **CODE WIDENED** — every regular file is read; undecodable files are printed by name |
| **A1** | `w3_scope.py` | *"over ONE tree"*, with the same extension filter | **CODE WIDENED** — the same way |
| **A2** | `s2_seam.py` | two limits named, `MIN_CHARS = 300` omitted; it removed 6 of 17 block quotes and 65 of 124 paragraphs from the comparison **altogether** | **CODE WIDENED** — a second pass compares every passage over 60 normalised chars at 90 %; what neither pass compares is printed one per line |
| **C1** | `check_doc.py` | *"over ONE FILE … it reads no code"*; it reads two, and the second carries five of its own assertions | **CLAIM NARROWED** — nothing needed widening |
| **B1** | — | the AM §17.5 quotation struck in §4 and asserted live in §0, 310 lines apart, since `83ac472` | fixed **at §0**, and `e2_crosssection.py` added |

## The scripts

| file | what it does |
|---|---|
| `kernd633.py` | tokens, paragraphs, longest **verbatim run**, the strike rule, the sandbox |
| `trace_open.py` | runs a checker with `open` instrumented and records every path it **reads** |
| `e1_extents.py` | **is the printed extent true?** Each checker's read set against what it prints |
| `e2_crosssection.py` | **a struck claim must not stand un-struck elsewhere in the same document** |
| `e3_bothways.py` | **27 probes, 5 checkers**: inside the claimed extent → must fire; outside → must stay silent |
| `selftestd633.py` | 50 assertions, about half of them that the detector does **not** fire |

Each script prints its own extent under its own total, and E1 is the file that checks that
those sentences are true.

## What mg-1d26 changed here, and why

`e2_crosssection.py` and `kernd633.py` were the **other 551 lines of the verdict path**. The
three species runners' exit status is `e2`'s, so a deletion in either of these two files
changes what those runners tell a reader — and mg-4adb's deletion population covered the 255
runner lines and neither of these files. mg-d53d deleted all 806 and found **six deletions
that turned a red gate green, four of them silently**, including one that made this checker
**read no document, print nothing and return 0**. `code/verdict_path_repair_1d26/` closes
them and demonstrates each one going red; four mechanisms landed in these two files:

* `arm_verdict()` / `deliver()` in `kernd633.py` — **the only way this checker can exit 0.** A
  run that never reaches its verdict exits **9**; an **empty population** exits **2** with its
  own sentence, because `returned 0` and `examined nothing` must not be the same state. The
  population size is printed on **every** run, passes included.
* The population is **enumerated twice**, by `os.walk` with a stated residue and by `glob`,
  and a disagreement is a finding with both deltas named.
* The verdict is **computed twice** — the counter, and a recount off the rows actually
  printed — and the two must agree.
* **E2b controls `(f)` and `(g)`**: a claim restated *after* its own strike, and *before* it.
  All five earlier controls restated before, so one deleted line in `kernd633.strike_findings`
  could blind the detector to half the cases with all five staying green.

`arm_verdict()` is a call and not an import side effect: `e1_extents.py`, `e3_bothways.py` and
`selftestd633.py` import this kernel and do not deliver a verdict through it.

`out_e2_crosssection.txt` was regenerated with those changes. **Its `E2 TOTAL BAD: 1` is a
live cross-section finding in `code/face_geometry_repair_e35b/README.md`** — struck in one
paragraph, asserted in another — and not a regression of anything here.

## What it does not cover, named

* **E2 compares a strike only against its own document.** A claim struck here and asserted in
  *another* file is invisible to every checker in this repository. That is the next hole, and
  it is named rather than closed.
* **E2 matches verbatim runs.** A claim restated in different words is invisible to it.
* **E3 probes each extent at a few points.** An extent probed at two points is not an extent
  verified at every point, and the choice of points is the author's. The probes are listed by
  name in the output so a successor can see which regions were never touched.
* **E1 compares what was read with what was printed.** It does not test whether a checker's
  rules are right or whether it fires on what it reads — a checker that opens every file and
  looks at none of them passes E1 and fails E3, which is why both exist.

## Predictions

`PREDICTIONS.md` was written before any probe ran and is not edited afterwards. **1 of 21
predictions was wrong** and is kept as written; `OUTCOMES.md` scores it and records the three
defects found in this instrument itself, two of which would have inverted a result.
