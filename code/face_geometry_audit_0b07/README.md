# mg-0b07 — independent audit of mg-64b6 (`0fb0e00`)

> **`p3_grain.py` NOW EXITS 1 AGAINST THE LIVE TREE, AND THAT IS THIS AUDIT WORKING**
> (added by mg-f7e1, 2026-07-31 — no transcript or finding below is edited).
> This audit's finding **B1** was acted on: `absorb_trace`'s `shape` condition is spelled
> with an `or` again, so exactly one of `p3`'s six claims — *"`absorb_trace` contains 0
> boolean operators of ANY kind"* — is **BROKEN**, because that is the thing the repair
> put back. Its three perturbation rows (S1/S2/S3) still match 3 of 3 and its cross-run
> against `b6bc2ef` still holds: the spelling moved, the units did not. The subject's own
> `d4_auditor_rerun.py` runs this script unmodified and **scores exactly which claim broke
> and why**, so the red is a measurement rather than a landmine. The commands below still
> describe this audit's run against the tree it audited; against a tree at or after
> `mg-f7e1`, `p3` exits 1 and `run_all.sh` with it.

Run everything:

    ./run_all.sh            # ~10 min, 39 claims, 0 BROKEN, exit 0, 7 findings

Run the primary measurement on its own — **change the subject's patch and see
whether its "derived" declaration follows**:

    python3 p1_derived.py
    echo $?                 # 0

Run the one that answers *is `clause` the floor?* — each half of the `shape`
condition perturbed alone, on the live tree and at the pinned two-clause commit:

    python3 p3_grain.py
    echo $?                 # 0

| file | what it measures |
|---|---|
| `kern0b07.py` | the harness: an AST census, return/clause enumeration, a splicer, the battery runner, and a runnable **copy of the subject's own instrument** in a temp tree |
| `p1_derived.py` | **THE PRIMARY MEASUREMENT**: the subject's `d2_deletion.py` run four times — unperturbed as a control, then with its patch WIDENED and with it REPOINTED at another unit in another function — with nothing else edited |
| `p2_units.py` | mg-9220's eleven written declarations reconstructed from `b6bc2ef`, read again here, and measured by this audit's own census |
| `p3_grain.py` | the finest unit whose PERTURBATION the battery can see, measured on the live tree and cross-run at `b6bc2ef` where the same units are clauses |
| `p4_confirmed.py` | the six returns under individual deletion, here and at the pin; the inert return; the negative control as a process; mg-c4c8's F3 pair |
| `p5_enumeration.py` | did the enumeration happen — each of the subject's eight branches located, two of its checks exercised, both stated reasons checked |
| `p6_floor.py` | **the floor item**, chosen here: what this commit wrote *outside* the thing it repairs |
| `selftest_0b07.py` | this audit's own primitives on inputs counted by hand |
| `out_*.txt` | committed transcripts |
| `PREDICTIONS.md` | every prediction, registered before its run |

**CLAIMS vs FINDINGS.** A `[BROKEN]` claim means **this instrument** is wrong and
sets the exit status. A `[FINDING]` means **mg-64b6** is; it is counted and
printed and does not. Conflating the two makes an audit unrunnable in CI by
anyone who does not already know the answer.

**Independence.** `kern5f9a.py` — the subject's kernel, and the thing that
computes the declaration under audit — is **not imported anywhere**. The census,
the enumerators, the splicer, the row parser and the battery runner are
re-derived here from `ast`. `d2_deletion` **is** imported, in `p2` and `p5` only,
and only for its data tables (`UNITS_AS_SHIPPED`, `SHIPPED_PATCHES`,
`MUTATIONS`, `SELF_DEFECT_BRANCHES`): those tables *are* the object under audit,
and auditing a paraphrase of them would be worthless. Every number printed about
them is computed here.

**Reading source code is not the test.** The subject's declaration could be
computed by correct code that nothing reaches, or printed from a transcript
somebody regenerated. So `p1` **changes the patch** — one token of the mutation
table, in a copy — and reads what the subject's own `d2` prints, twice, in two
different directions. The unperturbed copy is run first as the harness's own
control.

**Populations, not totals.** Every count is printed beside the rows that produce
it: 6 returns in one function measured on two trees, 11 declarations against 11
patches, 16 boolean operators of which 4 decide a return, 3 perturbations of one
condition, 43 scored rows in a 23,695-byte artifact, 4 regenerated controls.

**Predictions.** `PREDICTIONS.md`, registered before the runs. Misses are kept
where they were made and are named in the transcripts: `f.3` ("the prior landing
documents' diffs are additive only") was wrong, and `p5.2` scored 5 of 6 on its
first run because this audit's locator looked for a printed sentence inside
source code. Both are in the transcripts, neither is edited away.

Nothing under `../face_geometry` is written: every mutation goes to a copy in a
temporary directory, and no run uses `| tee` (mg-f922).

Findings and what would close them: `docs/audit-mg-0b07-derived-and-the-floor.md`.
