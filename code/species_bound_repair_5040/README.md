# mg-5040 — the bound repair

Repairs mg-4700's three OPEN items. The prose that matters is in
`docs/OneThird-Species-Hopf-Monoids-Bound-Repair.md`; this file says what the instrument is and how
to run it.

```
sh run_all.sh      # ~25 minutes, pure Python 3, NO NETWORK
```

`git archive` and `git log` are used against this repository, which is local.

## What is in here

| file | what it measures |
|---|---|
| `selftest5040.py` | the instrument's own contracts, including the **restore proof in the direction that must fail** and the pin's "does not already carry the repair" assertions |
| `r1_bound.py` | OPEN 1 — four structures planted in a real tree, four checkers each, at HEAD and at the pinned pre-repair revision |
| `r2_wiring.py` | OPEN 2 — the wiring block split by line and deleted one part at a time, three runners, at HEAD and at the pin |
| `r3_summaries.py` | OPEN 3 — every copy of `A2 TOTAL BAD` in a commit message or a committed file, its disposition, and which copies share a source |
| `r4_self.py` | this deliverable checked for the defect it remedies, in four kinds, with two branches named as unable to exhibit it and a reason for each |
| `kern5040.py` | the header, the checker runner, and the `Probe` that mutates the real worktree and proves it put it back |

## The three things this instrument does differently, and why

**It mutates the real worktree.** Two of mg-4700's three OPEN items are about a distinction that is
invisible by reading — a checker silent because nothing is wrong and a checker silent because it
cannot see are the same bytes on stdout. So structures are planted and runners are executed.
Restoration is proved with `git status --porcelain --untracked-files=all` **and** the full `git
diff`, both compared with the state at entry. `--untracked-files=all` is not decoration: plain
`--porcelain` collapses an untracked directory to one line, and this instrument's own directory is
such a directory until it is committed. The self-test caught that by asserting the restore proof in
the direction that must fail.

**Every comparison is anchored on `4372fae`, never on `HEAD`.** mg-821e anchored two comparisons on
`HEAD` and they stopped comparing anything the moment its own repair landed. `r4_self.py` R4d greps
this instrument's own sources and fails if it finds a comparison anchored on `HEAD`.

**It repairs nothing it measures.** mg-6cb9's `a1_bothways.py` and `a2_crosssection.py` and mg-4700's
`q1`–`q4` are run unmodified and whatever they say is reported, including where it is inconvenient.

## What it perturbs, declared

This tree's own markdown files sit under `code/`, and `e2_crosssection.py` reads every `*.md` under
`code/`. So the live markdown census is higher than the shipped tree's by the number of files here.
None of them contains a literal strike, so the strike census is not perturbed. `r3_summaries.py`
counts from `git` at a named revision as well as from the worktree, and prints the difference between
the two columns by name.

## Exit-code convention

A checker exits **1** when it has a finding and **0** when it does not. `Rn TOTAL BAD` counts
outcomes that contradict **this repair's own claims**; `R1 PREDICTIONS MISSED` counts predictions in
`PREDICTIONS.md` that were wrong. **The two are separate on purpose** — a wrong prediction about code
this ticket did not write is information, not a defect, and one number could not tell a reader which
had happened.
