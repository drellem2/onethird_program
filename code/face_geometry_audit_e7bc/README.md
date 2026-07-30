# mg-e7bc — independent audit of mg-04a8 (`c7f9673`)

Run everything:

    ./run_all.sh            # ~90 s, 25 claims, 0 BROKEN, exit 0, 8 FINDINGS

Run the primary measurement on its own — mg-04a8's repaired label check, as a
process, against any artifact file:

    python3 checkrun.py ../face_geometry_instr_5f9a/positive_control_all_fail.txt
    echo $?                 # 1  -- THE CHECK GOES RED

    python3 checkrun.py ../face_geometry/controls_output.txt
    echo $?                 # 0  -- the check says yes

| file | what it measures |
|---|---|
| `kerne7bc.py` | mutation runner, row/summary parsers, corruption library, the eleven source edits |
| `checkrun.py` | the repaired check wrapped as a process with an exit code |
| `g1_positive_control.py` | THE PRIMARY MEASUREMENT: exit codes on the committed broken artifact and on five of this audit's own |
| `g2_deletion.py` | the deletion test, both directions, the 9 mg-d0e2 ran plus 2 no list names |
| `g3_differs_under.py` | five WOULD DIFFER UNDER statements, tested by making the change |
| `g4_seams.py` | the artifact's threshold, the control that carries it, 17 anchored figure-statements, the re-run |
| `pc_all_pass.txt` | this audit's own committed broken artifact — every row promoted to `[PASS]` |
| `out_g*.txt` | committed transcripts |

**CLAIMS vs FINDINGS.** A `[BROKEN]` claim means this instrument is wrong and sets
the exit status. A `[FINDING]` means mg-04a8 is, and is counted and printed but does
not. Conflating the two makes an audit unrunnable in CI by anyone.

**Independence.** The mutations, both parsers and the corruption generators are
re-derived from the source text, not imported from `kern5f9a.py` (the subject's own
runner) or `kernd0e2.py` (the previous audit's). The one import from the subject is
`check_labels` itself — auditing a paraphrase of it would be worthless.

Nothing under `../face_geometry` is written: every mutation goes to a copy in a
temporary directory, and no run uses `| tee` (mg-f922).

Findings and what would close them: `docs/audit-mg-e7bc-repaired-check.md`.
