# `code/branching_repair_76cc/` — the two sites `mg-957f` left open

```
./run_all.sh          # pure Python 3, no dependencies, NO NETWORK
```

Several minutes: `r2` and `r3` each run `mg-58da`'s `g4_fleet.py` more than
once and it takes about a minute and a half a time.

| script | what it settles |
|---|---|
| `selftest_76cc.py` | the instrument, before any finding rests on it — **93** assertions |
| `r1_kernel.py` | **`OPEN 1`** — the kernel half of `g1`'s predicate, restored and shown firing |
| `r2_reproduce.py` | **`OPEN 2`** — `G-3`, closed on five outputs instead of one |
| `r3_prerepair.py` | the standing instruction applied to **this** repair: the pre-repair predicates run against the same inputs |
| `r4_doccheck.py` | this deliverable, checked for the defect it repairs |

Every script exits `0` iff `SELF-ERRORS == 0` **and** `FINDINGS == 0`. A
non-zero exit means *this script has something to report*, never *this script
is broken*; the two numbers are printed separately and every count names its
population. `PREDICTIONS.md` holds the exit code and answer predicted for each
**before** it was run, with the misses kept as written.

## What is being repaired

`mg-957f` audited `mg-7e58` and left two open sites.

**`OPEN 1` — the kernel half of the predicate is gone.** `g1_provenance.py`'s
file-sha finding covered `c1_branching.py` **and** `kern_a218.py`, the file
`g1`'s own section (ii) labels *"its kernel — the measuring half"*. Its
replacement took both sides of its comparison through
`run_c1(script_rev=REV_A218)`, which loads the kernel from that revision, so
the kernel was pinned on both sides and a kernel that moved reached neither.
**This is the first site in this arc where a repair removed detection rather
than relocating a defect**, and it is visible only by running the pre-repair
predicate.

**`OPEN 2` — `G-3` is shut at one revision**, with `1 of 5` committed outputs
reproducing byte for byte.

## Why the instrument is built the way it is

* **`run_c1` takes the script and the kernel as two independent sources.**
  `lib58da`'s own `run_c1` bound both to one `script_rev`, which is the whole
  of `OPEN 1`. A signature that cannot say *this script with that kernel*
  cannot ask the question, and an instrument that inherits the defect cannot
  measure it.
* **The readers import no `re`.** `lib58da` reads `c1`'s vertex sets with one
  regex per row and `lib957f` with `ast.literal_eval`; this uses
  `str.partition`. Two readers that share an implementation share a blind spot.
* **Every mutation is a `COMMIT`, in a temp clone.** `g1` reads `c1` and the
  kernel with `git_show`, so a working-tree bend reaches nothing and comes back
  silent for the wrong reason. `mg-957f` made exactly that mistake and kept it
  in its predictions.
* **Nothing here writes into** `code/branching_audit_58da/`,
  `code/branching_audit_a218/`, `code/branching_audit_321d/`,
  `code/branching_audit_957f/`, `code/branching_repair_7e58/` or
  `code/branching_locate_db09/`. `r2` runs `mg-58da`'s own `run_all.sh`, and
  it runs it **in a clone**, because that script redirects into the very files
  under test.
* **No pipe in `run_all.sh`** (`mg-c2b3`): each script's stdout is redirected,
  `$?` read on the next line, the worst propagated — and `r4` (iv) runs this
  very file with a red stub in it to check that the red survives.

The write-up is `docs/repair-mg-76cc-kernel-half-and-five-outputs.md`.
