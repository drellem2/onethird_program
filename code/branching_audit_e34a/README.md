# `code/branching_audit_e34a/` — the independent audit of `mg-76cc` (`4755d02`)

```
./run_all.sh          # pure Python 3, no dependencies, NO NETWORK
```

Several minutes: `k2` runs `mg-58da`'s own `run_all.sh` in a clone, and `k1`
makes 21 pinned `g1` runs across 7 clones.

| script | what it settles |
|---|---|
| `selftest_e34a.py` | the instrument, before any finding rests on it — **54** assertions |
| `k1_prerepair.py` | **the primary target** — the pre-repair predicate, run against the same inputs |
| `k2_five.py` | **OPEN 2** — `G-3`, counted on five here rather than read off a table |
| `k3_undisturbed.py` | what `mg-957f` confirmed, re-derived at HEAD rather than at its own pinned HEAD |
| `k4_cancel.py` | **the floor** — one thing no list in the ticket names, chosen and said |

Every script exits `0` iff `SELF-ERRORS == 0` **and** `FINDINGS == 0`. A
non-zero exit means *this script has something to report*, never *this script
is broken*; the two numbers are printed separately and every count names its
population. `PREDICTIONS.md` holds the exit code and answer predicted for each
**before** it was run, with the misses kept as written.

## What is being audited

`mg-76cc` (`4755d02`) closed the two sites `mg-957f` left open on `mg-7e58`:

* **`OPEN 1`** — the kernel half of `g1_provenance.py`'s measurement-invariance
  predicate had been *removed* by `mg-7e58`, not relocated. `mg-76cc` gave
  `lib58da.run_c1` a separate `kernel_source` and grew section `(v)` from one
  implicit half to three named ones and from three direction probes to five.
* **`OPEN 2`** — `G-3` was shut at one revision, with `1 of 5` committed
  outputs reproducing. `mg-76cc` narrowed the claim and closed it on five
  under a named normalisation.

## Findings

**The repair holds on its primary target.** Across 7 inputs × 3 revisions of
the predicate = 21 runs, there is **no input where the pre-repair predicate
fires and this one is silent** — not at the exit grain, not at the finding
grain, and no file named by an old finding that no new one names. `OPEN 1` is
closed: the kernel bend is caught, naming `kern_a218.py`, where the predicate
it replaced was silent. `OPEN 2` is closed on five, counted here.

**Three findings, none of which reopens either site:**

1. **The rationale for the row `mg-76cc` added is inverted** — in five places,
   including `g1`'s docstring, `g1`'s own printed output and the commit
   message. It says a pair of changes that cancel *"would pass each half on
   its own"*. Built and measured: a cancelling pair **MOVES both halves** and
   leaves **`both together` IDENTICAL**. The row named `cancellation` is the
   only one of the three that a cancelling pair passes. `k4 (iii)`.
2. **On that input the repaired predicate books two findings saying the 198
   cells "have to be re-taken"** while its own `both together` row — the only
   one that asks what the tree as it stands measures — prints `IDENTICAL` on
   the same run. `k1 (v)`. The pre-repair predicate books it too, so the class
   is not new; what is new is that the repair's own rationale names this input
   and states the opposite outcome.
3. **`lib76cc.findings_of()` over-counts**, demonstrated on a file committed at
   HEAD: it matches the substring `   FINDING: `, so a finding *quoted* from a
   nested run at deeper indentation is counted as the outer script's own.
   `out_g4_fleet.txt` reads 3 where its own trailer says 2. `r3` uses that
   reader for the `names kern_a218.py` column the whole `OPEN 1` verdict turns
   on — it happens not to bite there, so this is a live defect with no live
   consequence. `k4 (v)`.

Nothing `mg-957f` confirmed is weaker: attributions **18 of 18** agree against
a ground truth derived twice over `286d5030..HEAD`, `g1`'s three pre-`mg-76cc`
direction probes are present by name and HIT, and `g4` and `g1` read exactly
as `mg-957f` read them.

## Why the instrument is built the way it is

* **The pre-repair revision is DERIVED, not written down.** `lib76cc.py`
  carries `REV_957F = "e006581c…"` as a literal beside the comment *"g1 BEFORE
  mg-76cc"*. Here it is the parent of the last commit that touched
  `g1_provenance.py`, computed — and `k1 (i)` then checks that the literal and
  the derivation name byte-identical files, because if they did not, `mg-76cc`
  ran something other than the predicate its patch replaced. (They do.)
* **The pinned predicate travels with its own `lib58da`.** `mg-76cc` changed
  `run_c1`'s signature in the same commit as `g1`; a pre-repair predicate run
  against the repaired library is a third thing that never existed.
* **The buckets are not filtered by a declaration.** `r3` restricts its
  backwards set to inputs *it has declared real defects*, which makes the
  answer depend on the declaration. Here every input is bucketed and the
  declaration is printed beside the bucket.
* **Two grains, not one.** `r3` compares exit codes. A script can exit 1 on a
  SELF-ERROR alone — it could not build a probe — and at the exit grain that
  is indistinguishable from a catch. The finding grain and the file-naming
  grain are printed separately.
* **`k2`'s population comes from `run_all.sh`'s own redirections**, not from a
  written list of five that could not notice a sixth.
* **`k3`'s range ends at HEAD**, not at `mg-957f`'s own HEAD. `mg-05eb` has
  already booked a finding in this arc whose whole content was that a scan had
  been pinned.
* **Every mutation is a COMMIT, in a temp clone.** `g1` reads `c1` and the
  kernel with `git show`, so a working-tree bend reaches nothing and comes
  back silent for the wrong reason.
* **No pipe in `run_all.sh`** (`mg-c2b3`).

The write-up is `docs/audit-mg-e34a-mg76cc-kernel-half-and-five.md`.
