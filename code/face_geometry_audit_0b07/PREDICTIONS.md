# mg-0b07 — predictions, registered before the runs

Every prediction below was written down before the run it names. Misses are kept
where they were made; nothing here is edited after the fact. Where a measurement
was made **before** its prediction was registered, that is said in the row rather
than dressed up as foresight.

Subject: `0fb0e00` (mg-64b6), the repair of mg-c4c8's OPEN 1 and OPEN 2.

---

## p1 — is the declaration DERIVED?

| # | run | prediction |
|---|---|---|
| p1.1 | the instrument copied to a temp tree, **unperturbed**, `d2_deletion.py` re-run | exit **0**; `AFTER-5`'s declaration line identical to the one the in-place run prints. This is the harness's own control: if a copied tree changes the answer, nothing below means anything. |
| p1.2 | **W** — `AFTER-5`'s patch WIDENED (a second `return`, gate `diagonal`, taken out too), nothing else edited | the printed declaration goes `1 \`return\`` → **2 \`return\``**, and its label list gains `'diagonal'`. `d2` exit **1** — the widened patch trips the "no mutation removes more than one return" claim, which is the right thing for it to do. |
| p1.3 | **M** — `AFTER-4`'s patch REPOINTED at a clause of `gate_violations`, nothing else edited | the declaration goes `0/1/0 from \`absorb_trace\`` → **`0/0/1` from `gate_violations`**, i.e. it changes UNIT KIND and FUNCTION together. `d2` exit **1** (AFTER-4 is registered as CHANGES and a clause of `gate_violations` is inert). |
| p1.4 | **N** — `AFTER-6`'s patch NARROWED to remove nothing at all (`old` == `new` modulo whitespace-free no-op is impossible; instead the anchor is replaced by itself plus a `pass`) | *not run* — see the transcript; superseded by p1.2/p1.3, which change the declaration in two different directions. |
| p1.5 | no second, independent statement of the size survives anywhere | `returns_removed` (mg-9220's line heuristic) is **absent** from `d2_deletion.py` and `kern5f9a.py`; the `MUTATIONS` table contains **no integer literal**. HOLDS. |
| p1.6 | the four committed transcripts regenerate byte-identically from the committed tree | `out_d1_trace.txt`, `out_d3_reintroduction.txt`, `out_d4_auditor_rerun.txt` **reproduce**. |

**Registered after its run, and said so:** `out_d2_deletion.txt` was regenerated
before these predictions were written, in reconnaissance. It **differs** from the
committed transcript. The row is reported with that provenance and is not counted
as a prediction.

## p2 — the 8 of 11, re-measured

| # | run | prediction |
|---|---|---|
| p2.1 | mg-9220's eleven sentences read by **this auditor**, independently of mg-c4c8's H4 | my reading agrees with mg-c4c8's quoted triples on **11 of 11**. |
| p2.2 | the eleven measured against mg-9220's own patches with this audit's own AST census | **8 UNDERSTATE, 3 AGREE, 0 OVERSTATE**. Per tag: exact — `BEFORE-1`, `AFTER-3`, `AFTER-4`; understating — `BEFORE-2`, `AFTER-1`, `AFTER-2`, `AFTER-5`, `AFTER-6`, `R1`, `R2`, `R3`. |
| p2.3 | the specimen's fidelity: `UNITS_AS_SHIPPED` sentences vs `b6bc2ef`'s `UNITS` | **11 of 11 byte-identical**. |
| p2.4 | the specimen's fidelity: the patches the comparison applies vs `b6bc2ef`'s | **10 of 11 identical as text**; `R3` differs in FORM (two edits here, one concatenated anchor there) and is predicted **identical in effect** — same measured triple under both forms. |
| p2.5 | the subject's verdict printer fed a declaration that **overstates** its patch | it prints `*** UNDERSTATES ***`. The printer is a binary `got == reading`, so the direction it names is not measured. Predicted to fire. |

## p3 — the grain regress: the next rung, found here

| # | run | prediction |
|---|---|---|
| p3.1 | `absorb_trace` on the live tree: **every** `BoolOp` node, not only the ones the subject's enumerator reaches | **0**. The subject's "0 deciding clauses" is exact under the wider reading too. |
| p3.2 | `face_complex.py`: BoolOps the subject's `deciding_clauses` does **not** reach | **at least one** (conditions whose body does not return). The subject's population is the one its sentence names; the file has more. |
| p3.3 | any enumerated clause containing a `BoolOp` anywhere below it (not only as a direct child) | **none**. The `nested` check is narrower than its sentence, latently. |
| p3.4 | **S1** — the `shape` condition reduced to its ORDER half alone (`len(A) != len(B)`) | artifact **CHANGES**, exit **1**. |
| p3.5 | **S2** — the `shape` condition reduced to its WIDTH half alone (widths over the common prefix) | artifact **BYTE-IDENTICAL**, exit **0** — mg-c4c8's inert clause, alive under the rewrite. |
| p3.6 | **S3** — the `shape` condition replaced by `False` | artifact **CHANGES**, exit **1** (the whole gate, as `AFTER-5`). |
| p3.7 | the finest unit whose perturbation the battery can see, at this site | the `return` **for deletion**; a **semantic sub-condition** for perturbation, and one of the two is inert. So `clause` is not the floor and neither is `return`. |

## p4 — do not disturb what is confirmed

| # | run | prediction |
|---|---|---|
| p4.1 | `absorb_trace`'s returns on the live tree, enumerated here and each replaced by `pass` ALONE | **6 returns, 6 of 6 CHANGE.** Exit codes, in source order: `shape` **1**, `diagonal` **0**, `magnitude` **1**, `find`'s root **1**, `parity` contradiction **1**, the accepting return **1**. |
| p4.2 | the inert `shape` return | **1** `shape` return in `absorb_trace`, **removed** and not annotated; `controls.py`'s constructed-pair entries **18**, unchanged from `b6bc2ef` — nothing was added to watch it. |
| p4.3 | the negative control, run as a process on the committed broken artifact | exit **1**. |
| p4.4 | mg-c4c8's F3 pair (`gate_violations`, `diagonal_moves` shape guards) deleted alone | **2 of 2 BYTE-IDENTICAL**, exit 0 — disclosed as not closed, and predicted unchanged. |

## p5 — did the ENUMERATION happen, and is it its own?

| # | run | prediction |
|---|---|---|
| p5.1 | `SELF_DEFECT_BRANCHES` | **8** branches, **6** marked CHECKED, **2** carrying a stated reason. |
| p5.2 | each CHECKED branch's named claim located in the file | **6 of 6 located**. |
| p5.3 | branch 1's check (`nodes`, the grain-free channel) fed a patch that removes syntax none of the three named units names | the "not coarser" claim goes **red**. The check works. |
| p5.4 | branch 1's check fed a **size-preserving** substitution — syntax removed on one side, the same count added on the other | the claim stays **green** while syntax was removed. `nodes` is a NET difference, so the grain-free channel has a grain of its own: the size. |
| p5.5 | branch 7's stated reason ("no smaller DELETION at this site") | **TRUE as stated**. Its conclusion — that the regress cannot continue below a clause — is predicted **FALSE**, by p3.5. |
| p5.6 | a branch covering the enumeration's own completeness | **absent**. |

## floor item — chosen here because no list in the brief names it

**What this commit wrote OUTSIDE the thing it repairs.** Four derived artifacts
were regenerated and two prior landing documents edited, one of the four inside
another audit's directory.

| # | run | prediction |
|---|---|---|
| f.1 | each regenerated control equals what its own generator produces on the committed tree | **4 of 4**. |
| f.2 | files this commit touched under any `*_audit_*` directory | exactly **one** (`face_geometry_audit_e7bc/pc_all_pass.txt`), and it is a generated control, not a transcript or a finding. |
| f.3 | the two prior landing documents' diffs | **additive only** — no prior figure, verdict or finding text altered. |
