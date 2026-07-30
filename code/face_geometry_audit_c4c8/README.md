# mg-c4c8 — independent audit of mg-9220 (`b6bc2ef`)

Run everything:

    ./run_all.sh            # ~230 s, 23 claims, 0 BROKEN, exit 0, 6 FINDINGS

Run the primary measurement on its own — every `return` in `face_complex.py`
deleted one at a time, with the artifact reported for each:

    python3 h1_per_return.py
    echo $?                 # 0

Run the negative control the brief asks about, as a process:

    python3 ../face_geometry_audit_e7bc/checkrun.py \
            ../face_geometry_instr_5f9a/positive_control_all_fail.txt
    echo $?                 # 1  -- THE CHECK STILL GOES RED

| file | what it measures |
|---|---|
| `kernc4c8.py` | the AST deletion harness: returns, clauses, splicing, battery runner, row parser |
| `h1_per_return.py` | **THE PRIMARY MEASUREMENT**: all 56 `return`s in `face_complex.py`, each deleted alone |
| `h2_the_nine_and_the_clause.py` | mg-d0e2's nine re-derived at their own unit on the live tree; then every CLAUSE of every deciding condition; then what the inert clause does |
| `h3_control.py` | the negative control re-run as a process, plus three corruptions no list names, one that must fire, and the repair's four scripts re-run against the claim counts its landing declares |
| `h4_declared_unit.py` | every DECLARED unit against its own patch; the landing table against the code; the provenance of the two pinned commits |
| `out_h*.txt` | committed transcripts |

**CLAIMS vs FINDINGS.** A `[BROKEN]` claim means this instrument is wrong and
sets the exit status. A `[FINDING]` means mg-9220 is, and is counted and printed
but does not. Conflating the two makes an audit unrunnable in CI by anyone.

**Independence.** The unit enumeration is the point of this audit, so it is read
out of `ast` rather than taken from anyone's list: the subject's `kern5f9a` and
mg-e7bc's `kerne7bc` both patch by `text.replace(old, new)` with `old` a literal
copied out of the source, which runs the mutations their author chose and cannot
enumerate the ones that exist. The row parser, the summary parser and the
retagger are re-derived here too. The one import from the subject is
`d2_deletion.UNITS` and `returns_removed` in `h4` — the declaration table *is*
the thing under audit there, and auditing a paraphrase of it would be worthless.

**Populations, not totals.** Every count in these transcripts is printed beside
the rows that produce it: 56 returns in one named file, 11 of them in the four
functions mg-d0e2's nine mutations touch; 11 clauses in 5 conditions; 28,900
predicate pairs over 85 shape profiles; 43 scored rows in a 23,684-byte artifact.
Each summary line in these files is computed from the rows above it, so a
disagreement between a summary and its rows is itself a defect — and the rows are
what to believe.

**Predictions.** Every exit code is predicted before its run and the misses are
kept as written: h1 43 of 56, h2 10 of 10 on the nine (after one repair,
disclosed below) and 11 of 11 on the clauses, h3 6 of 6, h4 11 of 11.

**One slip of this audit's own, kept rather than edited away.** `h2`'s first run
declared "invert `diagonal_moves`'s routing return" and inverted its shape guard
instead: `ast.walk` is breadth-first, so `[-1]` of the walk is not the last
return in source order. The registered prediction caught it (CHANGES/1 predicted,
IDENTICAL/0 observed). The selector now sorts by source position, and the
accidental mutation is kept as row `N9x` with its own prediction. It is the same
defect this audit exists to look for — a mutation whose declaration and whose
patch name different things — committed by the auditor.

Nothing under `../face_geometry` is written: every mutation goes to a copy in a
temporary directory, and no run uses `| tee` (mg-f922).

Findings and what would close them: `docs/audit-mg-c4c8-per-return.md`.
