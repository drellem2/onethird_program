# `code/branching_audit_957f` — the instrument for `mg-957f`

An **independent audit of `mg-7e58`** (`4372fae`), which repaired `mg-58da`'s
provenance apparatus on `mg-321d`'s findings `G-1` and `G-2`.

> The defect was **an apparatus built to establish provenance getting
> provenance wrong about itself** — `g4` attributing `c1` to a commit that never
> touched it, and `g1` exiting 1 on a finding its own section refutes.

```
./run_all.sh          # ~25-40 min, pure Python 3, no dependencies, NO NETWORK
```

Committed outputs: `out_selftest_957f.txt`, `out_j1_attribution.txt`,
`out_j2_silencing.txt`, `out_j3_setlevel.txt`, `out_j4_reproduce.txt`,
`out_j5_doccheck.txt`.

**Exit codes are the finding channel.** Every `j*.py` exits `0` iff
`SELF-ERRORS == 0` **and** `FINDINGS == 0`, and both numbers are printed
separately, so a non-zero exit never means the instrument is broken.
`PREDICTIONS.md` holds every exit code and answer predicted **before** the run,
**with the miss kept as written**. `j2` and `j4` are predicted to exit `1` and
do.

## What each file decides

| file | what it decides |
|---|---|
| `lib957f.py` | the readers, the clone helper, and a `run_c1()` that takes the **script and the kernel at independently chosen revisions**. `lib58da`'s own `run_c1` binds both to one `script_rev`, which is exactly `F-1` and cannot be seen with an instrument that inherits that signature |
| `selftest_957f.py` | **74 assertions** before anything is believed: the five readers on known, **absent** and **hostile** input; cell locality; `replace_once` refusing zero sites and two; the git helpers at five named revisions; `run_c1`'s independent kernel argument; `clone()` in both modes |
| `j1_attribution.py` | **every** attribution `g1` and `g4` print, re-derived here from `git log` by **two** routes that must agree first, each scored AGREES / WRONG COMMIT / UNVERIFIABLE — and then the derivation tested **by changing the history** in three clones |
| `j2_silencing.py` | how `g1` was reconciled: the disposition stated at three sites, four clones on `c1` with `g1` unmodified, and **what the old predicate covered that the new one does not** |
| `j3_setlevel.py` | the set-level property re-derived on readers written here — 10 pairs, 24 cells, **all five** members re-run, five locality probes |
| `j4_reproduce.py` | the thing no list named: does `G-3` **stay** shut once the next commit lands? |
| `j5_doccheck.py` | every figure in this audit's document, gated **at its own site** against a committed `out_j*.txt`, each gate deletion-tested with a null probe beside it |

## The two findings

* **`F-1` — coverage lost in the repair.** `g1`'s file-sha finding covered
  **two** files: `c1_branching.py` **and** `kern_a218.py`, the file `g1`'s own
  section (ii) labels *"the measuring half"*. Section (v) replaces it with a
  comparison of `c1`'s measurement — but takes both sides through
  `run_c1(..., script_rev=L.REV_A218)`, which pins `kern_a218.py` at `REV_A218`
  on **both** sides. A kernel that moved reaches neither side. Measured in one
  clone whose `kern_a218.py` is bent **as a commit**: the bend moves **24 of 24**
  of `c1`'s own vertex cells, the **pre**-repair `g1` exits 1 with a finding
  naming `kern_a218.py`, and the **post**-repair `g1` exits **0** and names it
  nowhere.
* **`F-2` — `G-3` is shut at one revision, not shut.** `g1` and `g4` interpolate
  the current `HEAD` into files that are committed, so
  `code/branching_audit_58da/`'s record stopped reproducing at the very next
  commit. `k2`'s `B1` is the branch aimed at exactly this and compares
  self-errors, findings, exit codes and finding **texts** — every one of which
  is invariant under a moving `HEAD`. Bytes are what `G-3` was about.

## What this audit CONFIRMS

* **The attribution is right and it is derived.** 17 of 17 attributions agree
  with a derivation made here; 0 wrong commit, 0 unverifiable. Changing which
  commit touches a file makes the attribution follow, in 3 of 3 clones.
* **`g1` was NOT silenced in the `c1` case.** The disposition is stated at 3 of
  3 sites, each check deletion-tested, and the replacement predicate goes red on
  a real measuring-half regression: 4 of 4 clone directions predicted, with the
  file sha moving in two of them and only one a defect.
* **The set-level property survives.** 10 of 10 pairs at 24 of 24 cells over
  240 comparisons, on readers written here; 5 of 5 members re-run in place;
  5 of 5 locality probes move their own cell and no other.

## What is NOT closed here, and is not this audit's to close

`c3_withdrawal.py` is red — `mg-d330`'s second finding, booked OPEN by
`mg-58da`, reported by name in `j3` and never counted as this audit's own.
`mg-321d`'s `M-1` and `M-2` are untouched by `mg-7e58` and untouched here.
