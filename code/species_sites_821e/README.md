# `code/species_sites_821e` — the repair of mg-6cb9's three OPEN items

**Work item:** mg-821e. **Repairs:** mg-6cb9 (`26c8d5c`), which audited mg-d633 / `e8fbd4f`.
**Run:** `sh code/species_sites_821e/run_all.sh`, about 4 minutes, **no network**.

mg-6cb9's standing note is the brief: *three findings, three different grains — a contingent
extent, a check that never executes, and a presence test. They are not variations of one bug and
should not be closed with one fix.* They are closed by three separate changes to three separate
files, each with its own probe file and its own deletion test.

| open | the defect | the change | the file that measures it |
|---|---|---|---|
| **1** | *"EVERY REGULAR FILE"* was true **only because no tree had a subdirectory** | `s1_extent.py`, `w3_scope.py` and `e1_extents.py` all **recurse**; one directory rule (`__pycache__`) is left and is **printed** | `p1_depth.py` |
| **2** | the check closing B1 was called by **0 of 3** species runners | the **removal question first** (outcome 2, measured), then wired into all three, verified **by running them** | `p3_wiring.py` |
| **3** | C4 was a **presence test** over a document with 3 of 5 anchors written more than once | seven **(site, anchor)** pairs, each checked in the heading region a reader meets it in | `p2_sites.py` |

## What is in here

```
kern821e.py        in-place mutation with a verified restore, plus run_runner()
selftest821e.py    86 assertions on the harness contract, over half of them
                   that something does NOT happen
p1_depth.py        OPEN 1.  18 probes: IN / OUT / DELETION TEST / GUARD
p2_sites.py        OPEN 3.  7 site deletions x 2 checkers, 3 non-site
                   mutations, 4 delete-every-copy mutations
p3_wiring.py       OPEN 2.  the removal question, then 12 run_all.sh runs
PREDICTIONS.md     every exit code, written before the run.  3 were wrong
OUTCOMES.md        what happened, including 4 defects in this instrument
```

## Three things worth knowing before you run it

**It mutates the worktree it runs in.** One edit at a time, restored, with `git status
--porcelain` *and the full `git diff`* compared before and after every probe; a difference stops
the run with exit 2. mg-6cb9 established why a sandbox is not good enough here: a `copytree` has
no `.git`, so `s1_extent.py`'s controls (a) and (b) fall into their `git archive` failure branch
and contribute nothing to the exit code being measured.

**Do not kill it mid-probe.** The restore lives in the process. A `SIGTERM` inside a `Probe`
leaves the last mutation on disk — which happened during development and is in `OUTCOMES.md`.
If it dies, read `git diff` before believing the tree.

**`p3_wiring.py` runs whole `run_all.sh` scripts, twelve times.** That is the point of it: a call
written into a script is not evidence that the script executes it, because a guarded branch, an
early exit or a swallowed error all leave the line in place. The only evidence is the runner's
own stdout, so that is what is read.

## The one thing that will look red and is not

mg-6cb9's `a1_bothways.py` row **Q17e** plants a subdirectory and runs `e1_extents.py`, and that
instrument scores a `WIDE` row as good only at **exit 1**. `e1_extents.py` exits 1 when **an
extent line is false** — the opposite polarity to a checker. With the walks repaired, no extent
line is false, so Q17e now exits 0 and mg-6cb9's table prints `*** EXTENT WIDER ***` against a
tree where the extent is true.

That label is that instrument's scoring, not a surviving defect, and `p1_depth.py` P1c says so in
its own output rather than leaving it to be discovered. The measurement that separates *the guard
works* from *the guard is absent* is **P12, P13 and P15**: put any one of the three walks back to
non-recursive with a subdirectory planted, and `e1_extents.py` exits 1. Before this ticket it
could not, which is exactly what Q17e found.

## Related

* `docs/OneThird-Species-Hopf-Monoids-Repair-Sites.md` — the repair document.
* `docs/OneThird-Species-Hopf-Monoids-ExtentRepair-IndependentAudit.md` — mg-6cb9, the audit this
  answers.
* `code/species_extent_audit_6cb9/` — mg-6cb9's instrument, re-run unmodified against the
  repaired tree; its transcript is committed here as `out_a1_6cb9_after.txt`.
