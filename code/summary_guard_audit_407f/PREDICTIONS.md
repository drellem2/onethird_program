# mg-407f — PREDICTIONS for the INDEPENDENT AUDIT of mg-cf83

**Committed before any script of this audit exists and before I have read one line of
mg-cf83's diff or of the post-repair `s1_rows.py` / `c1_summary_guard.py`.**

The parent ticket (mg-407f) says: *pre-register predictions before reading the diff;
commit them first.* This file is that commit. What I already knew at the moment of
writing is disclosed below as **hand measurements (H)** rather than laundered into
predictions — a prediction I could already look up is not a prediction.

---

## What I have already looked at (HAND MEASUREMENTS — NOT BLIND, NOT SCORED)

**H1.** `git show --stat 247d4fe`: mg-cf83 touched exactly 6 files —
`code/census_repair_f3ff/README.md` (+41), `code/census_repair_f3ff/s1_rows.py`
(233 changed lines), `code/summary_guard_cf83/README.md` (+173),
`code/summary_guard_cf83/c1_summary_guard.py` (+385),
`code/summary_guard_cf83/out_c1_summary_guard.txt` (+176),
`code/summary_guard_cf83/run_all.sh` (+30). 988 insertions, 50 deletions.
I have read the **stat**, not the **patch**.

**H2.** The commit SUBJECT of 247d4fe (visible in my dispatch prompt, unavoidably)
reads: *"THE SUMMARY BLOCK CAN NO LONGER DISAGREE WITH THE ROWS — mg-4d3b's F1-F5 are
gone, proved by the auditor's own detector and by a positive control against a REAL
broken remote"*. So mg-cf83 **claims to have already run check 1 of my ticket**. My
check 1 is therefore an attempted **REPRODUCTION of a claimed result by a disjoint
harness**, not a blind first test. I will say so in the finding rather than bill it as
a discovery.

**H3.** From mg-4d3b's audit (9cbb9a3, already in the log): the pre-repair summary
printed `n = 4, and all 4 are now checked against the tree` when 0 were; `The census
was WRONG on 0 of its 4 rows and RIGHT on 0`; `4 of 4 checked, 0 refuted`; four rows
of `0 / 0` from `0 if not gens else len(gens)` where `not None` is True; and then
**died on `len(None)`**. These are the F1–F5 mg-cf83 says it removed.

**H4.** mg-4d3b censused **8 sites** in the deliverable's own scripts that break the
"None is not an empty list" rule, **6 of them spelled `or []`**. mg-cf83 touched only
`s1_rows.py` among those scripts.

**H5.** `ls code/census_repair_f3ff/` shows `lib_f3ff.py`, `s0_freshness.py`,
`s2_controls.py`, `s3_graph.py`, `s4_crosscheck.py`, `selftest_f3ff.py` all present
and **all absent from mg-cf83's file list** (H1). So whatever `or []` / `0 if not
gens` sites live in those six files are, as a matter of arithmetic on the file list,
**untouched by the repair**. This is not a prediction; it is subtraction.

**H6.** `ls code/` shows a directory `idiom_sweep_audit_18dc` exists. I have not
opened it. Its name suggests the `or []` idiom has been swept before by someone else;
if so, my check 3 may be duplicating landed work, and I should check rather than
assume novelty.

---

## PREDICTIONS (BLIND — scored honestly at the end, including the misses)

### On check 1 — the broken-remote arm

**P1 (80%).** Running the repaired `s1_rows.py` against a clone whose `origin` URL has
been broken *after* cloning (so `origin/main` still resolves from the stale ref, the
mg-4d3b shape) will produce a **summary block that reports UNKNOWN / `?` rather than
`0` and rather than "all 4 are now checked"**. I put this high because H2 says
mg-cf83 already ran this arm; I am testing whether its claim reproduces, and the base
rate for "the parent's own positive control reproduces" is high.

**P2 (65%).** The repaired script will **not crash** on the broken arm — i.e. the
`len(None)` death mg-4d3b hit at F5 is gone and the process exits 0 (or at least
prints a complete summary block before exiting). I am less sure than P1 because
"prints UNKNOWN" and "does not die 30 lines later" are separate fixes and only the
first is named in the commit subject.

### On check 2 — the healthy arm (can the check fail?)

**P3 (85%).** On a healthy clone the summary reports **real integers, not UNKNOWN** —
so the guard is not hard-wired. High confidence because a hard-wired UNKNOWN would
have made mg-cf83's own `out_c1_summary_guard.txt` (176 lines of committed output)
visibly useless to its own author.

**P4 (55%).** The healthy-arm summary will reproduce mg-f3ff's **`2 of 4`** headline
figure, which mg-4d3b explicitly declined to dispute. Only 55% because my clone is a
fresh one at a different HEAD than mg-f3ff's run, and the census rows are computed
against a moving tree — the number may legitimately move.

### On check 3 — None vs zero, swept rather than spot-fixed

**P5 (72%).** **At least one** `or []` or `0 if not <x>` site survives in
`code/census_repair_f3ff/` **outside** `s1_rows.py`. Grounded in H4+H5: 8 sites
censused, only one file touched. The uncertainty is whether the other 7 sites are all
inside `s1_rows.py` (possible — it was the fattest script).

**P6 (40%).** At least one surviving site is **LIVE** (reachable on a real code path
under a fetch failure) rather than LATENT. Lower, because mg-4d3b already classified
its 8 sites LIVE/LATENT and the LIVE ones are the ones a repair would naturally hit
first.

**P7 (60%).** The distinction will be carried by a **sentinel or a separate
`is None` test**, not by a type — i.e. no `Optional`-carrying wrapper class, just
`if x is None:` branches. Cheap prediction about style, but it matters: a sentinel
convention has to be applied at every site by hand, which is exactly the failure mode
check 3 is looking for.

### On check 4 — one path or two?

**P8 (45%).** mg-cf83 **derived the summary figures from the per-row values** as it
was told, for the *counts* — but **at least one summary sentence retains an
independently computed quantity** (e.g. an `n`, a total, or a "checked against the
tree" clause) that is not read off the rows. This is the hybrid outcome and I think it
is the single most likely one; the alternatives are "fully derived" (~35%) and "guards
bolted onto a second path" (~20%).

**P9 (50%).** There will be a **structural invariant** in the code — a shared record /
dict / dataclass that both the rows and the summary read — rather than merely a
convention that they agree. If present, check 4 answers itself; if absent, check 5
becomes the load-bearing test.

### On check 5 — can I make them disagree?

**P10 (35%).** I will **fail** to construct an all-or-nothing input (whole fetch
fails) where rows say UNKNOWN and the summary says a number. I.e. I expect check 5 to
come back "could not break it" on the *homogeneous* input. Stated as 35% for the
*disagreement*, so 65% that mg-cf83 holds on this axis.

**P11 (45%).** A **MIXED** input — some rows resolvable, some not (e.g. one of several
repos/refs broken, or a ref that resolves but a commit that does not) — is the arm
most likely to produce a misleading summary, either a genuine disagreement or an
over-broad UNKNOWN that discards real information. Higher than P10 because a repair
driven by an all-fail positive control is exactly the repair that does not consider
partial failure.

**P12 (30%).** The over-broad direction is the one I will actually find: the summary
goes UNKNOWN when *any* row is UNKNOWN, so 3 real rows + 1 unknown reports nothing.
That is **not** the audited defect (it is conservative, not false) and I will
label it as such rather than inflating it into F-class.

### On the instrument itself

**P13 (55%).** `c1_summary_guard.py` — the "auditor's own detector" of H2 — **shares
code with the thing it validates**, by importing from `census_repair_f3ff` or by
being run against the same in-process objects rather than against the script's stdout.
If so, a defect in the shared layer is invisible to it, which is the same
self-validation shape my ticket exists to break. My own detector will therefore work
on **stdout text**, sharing nothing.

**P14 (50%).** `out_c1_summary_guard.txt` (176 lines, committed) will contain at least
one arm whose failure is **simulated rather than real** (a flag, a monkeypatch, a
fake) alongside the real broken-remote arm the subject advertises. mg-4d3b's whole
F-series began with `force_fail=True` returning before `git fetch` was ever spawned.

---

## MY TWO MOST LIKELY ERRORS, FILED IN ADVANCE

**P15 (my most likely error, 45%).** **I mistake a crash for a clean UNKNOWN.** If I
break the remote and the script dies with a traceback before the summary block is
reached, the absence of a false `0` on my terminal is *not* the guard working — it is
F5 surviving in a new costume. **Guard I bind myself to now:** on the broken arm I
must assert (a) the process's exit status, (b) that the literal summary-block header
appears in stdout, and (c) that stdout after that header is non-empty. A pass claimed
without all three is void.

**P16 (my second most likely error, 40%).** **My "broken" arm is not broken.** If the
script reads only local refs, or has a cache, or never spawns `git fetch` at all on
the path I exercise, then breaking `origin`'s URL changes nothing and the two arms are
the same run — I would report a false pass with real-looking evidence. **Guard I bind
myself to now:** the broken and healthy arms must produce **textually different**
stdout, and I must additionally confirm by direct observation (a wrapper `git` on
PATH, or a `GIT_TRACE`) that **`git fetch` was actually spawned and actually failed**.
If I cannot demonstrate the fetch was attempted, check 1 is UNMEASURED and I must say
so rather than pass it.

---

## SCORING RULES I BIND MYSELF TO

- P1–P16 are scored as written, **including the misses**, and a miss is reported as a
  miss rather than reinterpreted into a hit.
- H1–H6 are **not** scored. If a finding merely restates one of them, it is reported
  as a **reproduction**, not a hit.
- If check 1 or check 2 comes back UNMEASURED under the P15/P16 guards, the verdict
  says UNMEASURED. "Both directions or neither" is the ticket's rule and I do not get
  to keep the half that worked.
