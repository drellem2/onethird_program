# mg-9876 — auditing how `code/rendered_twin_pin_9bc2`'s instruments get VALIDATED

Three separate controls in one directory each certified their own **execution** rather than
the property they were **named for**. That is not three mistakes; it is what a validation
practice produces by default when the only question asked of a check is *did the expected
string appear?*. This directory asks the other question, of every arm, and answers it by
running the thing rather than reading it.

```sh
sh code/control_audit_9876/run_all.sh
```

## The question

> What would this check report if the thing it names **stopped happening**?
> If the answer is *the same as now*, it is laundered.

Answered two-sidedly. Every arm is run against an input where its subject **holds** and one
where its subject has **stopped**, and its own report is read through one predicate both
times. A predicate satisfied by the **good** input is not a weaker check — it is the mg-2f44
defect (`"8 9" in out`, matched by a line section 1 prints unconditionally, forever) and it is
scored red **against this instrument**, never quietly accepted.

## The files

| file | what it is |
|---|---|
| `lib9876.py` | the arm registry (50 arms), the mechanical site-discovery that makes it falsifiable, and the sandbox every probe runs in |
| `a1_census.py` | the list and its **size**, plus the machine check that no arm-shaped site in the sources is unregistered. Refuses (exit 2) if one is |
| `a2_discriminate.py` | every arm run against a known-bad input (Part A), and the demonstrated holes in arms that pass Part A (Part B) |
| `a3_auditor_selftest.py` | six planted worlds with known verdicts — **how it was established that this instrument can fail** |
| `a4_sweep.py` | the same smells counted across all 178 directories under `code/`, as candidates |
| `FINDINGS.md` | the counts both ways, the seven repairs, and six defects of my own |
| `out_*_PREREPAIR.txt` | the frozen transcripts from before the repairs — the other half of every `CLOSED` |

## Three things this directory does that the audited one did not

1. **The enumeration's completeness is checked, not claimed.** A hand list says 50 and nobody
   can tell whether the real number is 53. `a1_census.py` rediscovers every arm-shaped site
   mechanically and refuses if any is unclaimed. Demonstrated: `a3`'s P5 injects an
   unregistered check into a copy and the census exits 2. It fired for real when this
   ticket's own repairs added 13 sites.

2. **Every green has a matching red on disk.** Part B's register would be a list of
   accusations if it could only print `CONFIRMED`, and a list of assertions if it could only
   print `CLOSED`. Both runs are committed.

3. **The runner does not classify by exit code.** Each producer must leave its own decision
   line in its transcript. A run that exits 0 without one **did not run**, and is reported
   `BROKEN`, never green. That is the repair for instance 1, taken one layer further than
   removing the pipe took it.

## What it does not do

It does not decide whether the twin is correct, whether an unmoved ledger row is faithfully
summarised, or whether the 177 other directories' checks can fail — those are indexed, not
audited, and `a4_sweep.py` says so on its own face. And it does not make either suite **run**:
nothing in this repository invokes them on commit, on merge, or on any schedule.
`COVERAGE.md` §5 was the highest-value follow-up before this ticket and still is.
