# `mg-e34a` — predictions, written before each script was run

Every exit code and every answer in the `predicted` column was written
**before** the script it names was executed. Where a prediction missed, **the
prediction stays as written** and the actual is recorded beside it, with why.
A predictions file that records only hits is a file written afterwards.

Nothing reads this file.

**Two of the runs below went red on defects in MY OWN instrument before they
went green.** Those are recorded here too, in `§Instrument misses`, because a
script that was quietly fixed until it agreed is a script whose agreement
means nothing.

---

## Exit codes

| script | predicted | actual |
|---|---|---|
| `selftest_e34a.py` | **0** | 0 |
| `k1_prerepair.py` | **1** | 1 |
| `k2_five.py` | **0** | 0 |
| `k3_undisturbed.py` | **0** | 0 |
| `k4_cancel.py` | **1** | 1 |
| `run_all.sh` (worst) | **1** | 1 |

`k1`–`k4` exit `0` iff `SELF-ERRORS == 0` **and** `FINDINGS == 0`. `k1` and
`k4` were predicted red because `k1` books the cancelling pair and `k4` books
the rationale that names it.

---

## `selftest_e34a.py`

**Predicted exit `0`.** — **actual exit `0`**, 54 assertions, 0 failed. HIT.

---

## `k1_prerepair.py` — the pre-repair predicate against the same inputs

**Predicted exit `1`** — because of the last row.

| row | predicted | actual |
|---|---|---|
| `PRE_REV`, derived as the parent of the last commit touching `g1_provenance.py` | `3bc2cf76` | `3bc2cf76` — HIT |
| `g1` and `lib58da` at `e006581c` (mg-76cc's written literal) vs at the derived parent | IDENTICAL, both files | IDENTICAL, both — HIT |
| NULL input | both silent | both silent — HIT |
| `kern_a218.py` dim +1 | **new fires, old silent** — this is `F-1`, and closing it is the repair's job | new fires (`1`, `1/3`), old silent (`0`, `0/0`) — HIT |
| `c1_branching.py` dims +1 | both fire | both fire — HIT |
| `c1_branching.py` comment appended | both silent | both silent — HIT |
| `c1_branching.py` line past (iii) | both silent | both silent — HIT |
| `kern_a218.py` comment appended (my input) | both silent | both silent — HIT |
| the cancelling pair (my input) | **both fire** — the old one through its `c1` comparison, the new one through two halves | both fire (old `1/3`, new `2/5`) — HIT |
| backwards at the exit grain | `0` | `0` — HIT |
| backwards at the finding grain | `0` | `0` — HIT |
| files named by an OLD finding and by no new one | `0` | `0` — HIT |
| non-moving inputs on which **this repair** books a finding | `1` — the cancelling pair | `1` — HIT |
| non-moving inputs on which the **pre-repair** predicate books a finding | `1` — the same one; the class is not new | `1` — HIT |

**Actual exit `1`**, `0` self-errors, `1` finding. HIT.

**MISS, kept as written.** I predicted the exit grain and the finding grain
would separate somewhere in this table — that was the whole reason for printing
both. They agree on all seven inputs. What actually differs is the SELF-ERROR
column: both bent inputs make each predicate raise a self-error (it cannot
build a probe out of an already-bent file), so `exit 1` on those rows is partly
a fact about the script rather than a catch. The two grains being printed
separately is still right; that they agreed here was luck, not design, and
saying so is the point of keeping this row.

---

## `k2_five.py` — OPEN 2, counted on five

**Predicted exit `0`.**

| row | predicted | actual |
|---|---|---|
| files `run_all.sh` writes, enumerated from its own source | `5` | `5` — HIT |
| the runner's redirections against `mg-76cc`'s written list of five | agree | `0` written-and-not-listed, `0` listed-and-not-written — HIT |
| reproduce **byte for byte** | `1 of 5`, `out_selftest_58da.txt` only | `1 of 5`, `out_selftest_58da.txt` — HIT |
| reproduce under the revision normalisation | `5 of 5` | `5 of 5` — HIT |
| lines unexplained after normalisation | `0` | `0` — HIT |
| the substitution acts at the same positions on both sides | yes | `0` files where they differ — HIT |
| the record's revision is an ancestor of HEAD | yes | yes — HIT |
| commits from the record's revision to HEAD | **not `0`** — mg-76cc measured `0` in a worktree whose HEAD *was* the record's revision; six commits have landed on `main` since | **`6`** — HIT on the direction; the figure itself was not predicted |
| `g4_fleet.py` exits 1 inside `run_all.sh` | yes — mg-d330's second finding, booked OPEN by mg-58da | `run_all.sh` exit `1` — HIT |
| a control perturbation of the committed side still caught after normalisation | yes, both | yes, both — HIT (**but see `§Instrument misses`**) |

**Actual exit `0`**, `0/0`. HIT.

---

## `k3_undisturbed.py` — what mg-957f confirmed, re-derived at HEAD

**Predicted exit `0`.**

| row | predicted | actual |
|---|---|---|
| attributions enumerated from `g4`'s and `g1`'s own output | `17` | **`18`** — MISS. `g4`'s `(none) uncommitted` entry is two printed lines and is scored twice here (an ATTRIBUTION-block row and a summary line) where `mg-957f` scored it once. The difference is named in the transcript rather than reconciled away. |
| attributions agreeing with a re-derivation at **HEAD** (mg-957f pinned `2d23d880`) | `17 of 17` | **`18 of 18`** — HIT on the substance, on a population one larger |
| the two independent derivation routes agree | on all members | `5 of 5` — HIT |
| `g1`'s three pre-mg-76cc direction probes still present and HIT | `3 of 3` | `3 of 3` — HIT |
| `g1`'s probe population at HEAD | `5 of 5` | `5 of 5` HIT — HIT |
| `g4` exit and totals unchanged from mg-957f's reading | exit `1`, `0/2` | exit `1`, `0/2` — HIT |
| `g1` exit and totals | exit `0`, `0/0` | exit `0`, `0/0` — HIT |

**Actual exit `0`**, `0/0`. HIT (**but see `§Instrument misses`**).

---

## `k4_cancel.py` — the floor: one thing no list in the ticket names

**Predicted exit `1`.**

I chose the sentence `mg-76cc` uses to justify the row it added, because a
rationale is a claim and this one is checkable by building the input it names.

| row | predicted | actual |
|---|---|---|
| the cancelling pair moves the `c1_branching.py` half alone | MOVED | MOVED — HIT |
| it moves the `kern_a218.py` half alone | MOVED | MOVED — HIT |
| it moves the `both together` half | **IDENTICAL** — the row named `cancellation` is the one row a cancelling pair passes | IDENTICAL — HIT |
| therefore the shipped rationale (*"a pair of changes that cancel would pass each half on its own"*) is | **FALSE, inverted** — booked as a finding | FALSE — HIT, booked |
| copies of that sentence in the tree, enumerated from `git grep` | `2` — `g1`'s docstring and `g1`'s printed text | **`4` in the tree plus the commit message = `5`** — MISS. It is also in `out_g1_provenance.txt` (the committed transcript of the printed text) and in `docs/repair-mg-76cc-…md`. Enumerating from `git grep` instead of from memory is exactly why the miss is visible rather than silent. |
| the `both together` row is dead weight (carries nothing the halves do not) | **yes** | **NO** — MISS. A *conspiring* pair — each half harmless alone, the two together moving the measurement — is caught by that row and by neither half. The row is load-bearing. The finding is therefore written against the **sentence**, not against the row, and `k4 (iii)` says so. |
| `mg-76cc`'s own `PREDICTIONS.md` rows whose predicted exit disagrees with its committed transcript | `0` | `0` over `5` `.py` rows, both columns — HIT |
| (not predicted; found on the way) `lib76cc.findings_of()` over-counting | — | `1 of 5` committed transcripts read: `out_g4_fleet.txt` reads `3` against its own trailer's `2`. Booked. |

**Actual exit `1`**, `0` self-errors, `2` findings. HIT on the exit code, on
one finding I predicted and one I did not.

---

## Instrument misses — my own scripts, red before they were green

Kept because a script quietly fixed until it agreed is a script whose
agreement means nothing.

* **`k2`, first run: exit `1`, one SELF-ERROR and one FINDING, both mine.**
  * The control *"a figure changed in `out_g3_findings.txt`"* was written as
    `replace("198", "197")` and `198` is not in that file. It changed nothing
    and correctly booked itself a SELF-ERROR rather than a pass. Replaced with
    a control that finds a digit in the file rather than naming one — the
    literal was the defect, not the file.
  * The control *"the record's revision swapped for another real one"* was
    booked as a FINDING against `mg-76cc`. It was **my control that was wrong**:
    it swapped the token but then normalised against the *original* revision,
    so of course the difference survived. `r2`'s actual claim is that the
    normalisation **re-derives** the token from the transcript. Rewritten to do
    that, swapping the subject too, and it is absorbed as `r2` says. No finding
    against `mg-76cc` remains from it, and none should have been raised.
* **`k3`, first run: exit `1`, one SELF-ERROR and one FINDING, one mine and
  one real.**
  * `FINDING: g4 summary -- mg-58da -> 1 (c1_branching.py) -- disagrees` was
    **mine**: `g4` writes that summary row two ways, by commit prefix and by
    ticket name, and I resolved only the first. Fixed to resolve the ticket
    through the commit subject. `18 of 18` agree.
  * `SELF-ERROR: g4_fleet.py printed a trailer that does not match its own
    listed lines: FINDINGS says 2, 3 lines listed` was **real, and about the
    reader rather than about `g4`**. It is the seed of `k4 (v)` / `E-3`: a
    `FINDING:` line quoted from a nested run at deeper indentation is not the
    outer script's own. My reader now discriminates on position and
    indentation; `lib76cc`'s and `lib58da`'s do not, and that is the finding.
