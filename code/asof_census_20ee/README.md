# `code/asof_census_20ee/` — mg-20ee's census, and what the first tranche learned

`pc824` measured this population and mailed it. `mg-20ee` exists because *"the census has an
owner rather than living in one verdict mail"* — so the first thing in this directory is the
census **as an instrument**, pinned like any other, and the second is the ground truth that
corrects it.

| file | what it is |
|---|---|
| `census.py` / `out_census.txt` | the classifier. A **net**, pinned at `5a62e8c`, re-runnable |
| `ground_truth.sh` / `out_ground_truth.txt` | re-runs each candidate suite and asks whether its transcript still reproduces. **The number to quote** |
| this file | the tranche landed, the remainder, and the rules found by measurement |

## The numbers, and why three of them disagree

    pc824, mailed          105 transcripts   64 instruments   40 already moved
    census.py at 5a62e8c   125 transcripts   73 instruments   (2070 addresses)
    ground truth, re-run     —                —               32 actually stale

The classifier here is **looser** than `pc824`'s and says so: it resolves bare paths by suffix and
its *"the instrument actually reads that file"* test is weaker. It also **cannot see that an
instrument already reads at a declared commit** — `code/state_audit_6a2f` pins two literal revs
and is counted anyway. Both biases inflate it.

**32 is the honest already-stale count on this evidence**, and it comes from running the
instruments rather than from reasoning about `git log`. Of 44 candidates, 9 reproduce (the
classifier was wrong about them) and 3 have no runner.

Report the smaller number and declare the difference. Quoting 44, or 105, would be quoting a net
as if it were a catch.

## What landed in this branch

Five instruments, each verified in both directions, one commit each.

| instrument | `AS_OF` | transcript effect | direction 2 |
|---|---|---|---|
| `absent_step_7ae5` | `1024bc2` | 3 counts move, **no classification** | 46 lines: counts, addresses, tallies, stamp |
| `anchor_drift_96df` | `f59fe1f` | `+7/-1`, `+1/-1` | 6 lines, all addresses/counts |
| `n0_strike_audit_dd8b` | `dafe759` | `+28/-0` × 4 | counts move **by design**; every control identical |
| `face_geometry_audit_e720` | `8fab006` | `+18/-0`, `+25/-0` | every attack outcome identical; **2 verdicts move — reported** |
| `pairbias_indep_audit_6bd1` | `52d290a` | `+20/-0` × 2 | 8 lines, all addresses; every adjudication identical |

All five satisfy `git merge-base --is-ancestor <AS_OF> origin/main`.

## The criterion, as corrected by `pm-onethird` mid-branch

The ticket's stated acceptance — *"reproduces byte-identically against the declared commit"* —
is **not sufficient on its own**, and following it literally produced a bad pin in this branch's
own first commit. `absent_step_7ae5` reproduces byte-identically at exactly one commit,
`3fce8b9`, which is **not an ancestor of `origin/main`**: the refinery rebased the branch, and
that commit survives only because `origin/polecat-p7ae5` still points at it. That is `mg-daba`'s
defect, committed deliberately.

**Both conditions, in this order:**

1. `git merge-base --is-ancestor <declared-commit> origin/main` **must** be yes;
2. the transcript reproduces byte-identically at that commit.

**When they conflict, regenerate at the main-reachable commit.** Checking (2) first is what
produces a bad pin, because it makes the unreachable commit look like the only right answer.

Then apply the discrimination: if only addresses, corpus-size lines and the as-of block move, it
is a **pinning** — land it. **If a verdict moves, that is a finding** — report it; do not absorb
it into a pinning commit.

## Three `AS_OF` rules, all found by measurement, none by assumption

A successor should **search** for the pin, not guess it. All three of these appeared in five
instruments:

1. **The newest ancestor that reproduces** (`n0_strike_audit_dd8b`). Notably **not** the commit
   carrying the transcript: `STATE.md` gained a line before that commit landed, putting one
   address at `:210` against the committed `:209`.
2. **The parent of the carrying commit** (`face_geometry_audit_e720`). Its evidence is `git log`
   walks, and pinning at the carrying commit lets a `-60` walk reach *that commit itself*. **An
   instrument is run before it is committed**, so the history it measured excludes its own commit.
3. **`main`'s twin of a rebased commit** (`absent_step_7ae5`), when byte-identity and
   main-ancestry are incompatible — with the price measured and published.

The general form: **anything reasoning about identity by sha or ancestry breaks across a rebase,
and this repo rebases every merge.** Key on content, or on a main-reachable commit.

## The address defect is usually not alone

Every instrument in this tranche needed something else named before *any* transcript could
reproduce. None of these is an address, and none was folded in silently:

- **An absolute worktree path** printed into the transcript (`anchor_drift_96df`), so it
  reproduced for exactly one operator — `p96df` — and for nobody else, ever.
- **"HEAD vs the working tree"** standing in for *"before and after the repair"*, which is only
  the same thing while the repair sits uncommitted on the author's own desk.
- **A self-referential count**: `a2` was counting its own **not-yet-written** transcript, so its
  `483/22` could never have been reproduced by anyone. Pinning is what gave that suite a fixed
  point at all. `22 + 6 = 28` is the self-consistent value; the verdict does not move.
- **A synthetic fixture routed through the pin** (`pairbias_indep_audit_6bd1`), which looked for
  a selftest's temp file in a commit that never contained it and took the transcript from 226
  lines to 2. Explicit paths are read off disk; only the corpus default is pinned.
- **Unbounded history walks** scored as verdicts (`face_geometry_audit_e720`).

## What remains

27 of the 32 measured-stale instruments are unrepaired, plus the ~24 not-yet-stale ones the
ticket defers and the 3 with no runner. `out_ground_truth.txt` lists every candidate with the
size of its drift, which is the best available ordering for the next tranche — the small ones
(`species_remainder_f8fa` at `2+/2-`, `species_repair_a4ef` at `2+/4-`) are cheap; the large ones
(`runner_exit_audit_dee4` at `774+/91-`, `landing_audit_sweep_64cb` at `363+/111-`) are likely
carrying more than an address defect.

**Cost, measured rather than estimated: about 30 minutes per instrument** done to the acceptance,
across five. The ticket's *"do not do all 64 in one branch"* is right for a second reason it does
not give — not only reviewability, but that a rushed pin is indistinguishable from a correct one
in the diff and is caught only by the two-direction test.

**Two entries in `out_ground_truth.txt` are not independent**, and are marked there:
`n0_strike_audit_dd8b` reports `REPRODUCES` only because this branch had already pinned it when
the sweep reached it, and `census_remainder_f8e5` reports `rc=143` because its worker was killed
after 37 minutes to unblock the sweep — that line is unreliable and must be re-measured.
