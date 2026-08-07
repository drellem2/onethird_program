# mg-4d3b — predictions for the INDEPENDENT AUDIT of mg-f3ff

**COMMITTED BEFORE ANY SCRIPT OF THIS AUDIT EXISTS.** Nothing below was written
after seeing a number produced by code of mine. Everything I had already
measured by hand at the moment I wrote this file is listed in §0 as a
DISCLOSURE and is *not* counted as a prediction — a prediction I already knew
the answer to is a laundered measurement, and this arc has been caught doing it.

The subject is `code/census_repair_f3ff/` as it stands merged on `origin/main`
(commits `9c54a99` predictions, `10cda77` census+repair, `aea066d` README+s4).
The parent merged **unaudited**; this item was filed late.

---

## 0. DISCLOSURES — what I had already measured BY HAND before writing this file

These are measurements, not predictions. They are here so the scorecard cannot
claim credit for them.

- **D1.** I read all of `README.md`, `lib_f3ff.py`, `s0_freshness.py`,
  `run_all.sh`, `out_s1_rows.txt` (rows 1–3), `out_selftest_f3ff.txt`, the tail
  of `out_s4_crosscheck.txt`, and the NC3 block of `s2_controls.py`. So the
  parent's *claimed* row figures (row 1 = 7, row 2 = 5 as 4+1, rows 3 and 4 = 0)
  are known to me. Predicting them is not blind and P1–P4 below say so.
- **D2.** `find ~/.macguffin/work -name 'mg-*.md'` → **2386** files, and **0**
  of them have an id outside `[0-9a-f]{4}`. So `lib_f3ff.TICKET_RE`'s hex-only
  alphabet covers the whole live population. **This is not a defect** and I will
  not report it as one.
- **D3.** `out_selftest_f3ff.txt` contains exactly **40** `[PASS]` and **0**
  `[FAIL]`, so the README's "40 checks, 0 FAIL" is arithmetically right. But the
  instrument's own last line prints only `== selftest: 0 FAIL ==` — **40 is a
  README figure, not a printed one.**
- **D4.** The four ticket TITLES, read from `mg show`:
  - mg-e35b: `DROPPED VERDICT mg-fcf1 (2026-07-30, **no landing commit, no successor**)`
  - mg-fccb: `DROPPED VERDICT mg-d112 (2026-07-29, **no landing commit, no successor**)`
  - mg-a74f: `DROPPED VERDICT mg-16eb (2026-07-30, **no successor**)`
  - mg-dffa: `DROPPED VERDICT mg-5800 (2026-07-30, **no successor**)`
  Two of the four assert TWO premises. The deliverable measures ONE.
- **D5.** By hand, `git log origin/main --no-merges --format='%H %aI %s' | grep -E '\((mg-16eb|mg-5800)\)'`
  returns three commits: `253924065` (2026-07-30T19:14:18+01:00, mg-16eb),
  `e34a3c549` (2026-07-30T19:09:50+01:00, mg-16eb), `8ce78fb54`
  (2026-07-30T18:29:56+01:00, mg-5800). All three predate their rows' filing
  instants. **I already know rows 3 and 4's parents own commits.** P6 is
  therefore NOT BLIND on its existence half and is blind only on rows 1 and 2
  and on the aggregate.
- **D6.** `grep -n allow_fetch *.py` shows `allow_fetch` is a parameter of
  `Fetched.__init__` and `fetch_all` and is **wired to no caller and no CLI
  flag**. It is dead as merged. I know this before predicting P9.
- **D7.** `lib_f3ff.git_log` passes `--no-merges`. Merge commits are outside the
  population and `POPULATION` does not say so.
- **D8.** `Fetched.__init__`'s existence guard is
  `if not isdir(path/".git") and not isdir(path)` — an `and` where the natural
  reading is `or`.
- **D9.** NC3's forced failure sets `fetch_rc = 128` and **returns before the
  `git fetch` subprocess is ever spawned**. It does not exercise the real
  `r.returncode != 0` branch. Both branches converge on `self.sha is None`.
- **D10.** The committed `out_s1_rows.txt` records `onethird_program` at
  behind-0 and `one_third_width_three` at behind-46.

---

## 1. The four rows, re-derived independently

- **P1 (NOT BLIND, D1).** Row 1 — successors of `mg-fcf1` at or before
  2026-07-31T04:13:24Z — reproduces at **7** in `onethird_program` and **0** in
  `one_third_width_three`, verdict **REFUTED**, under an implementation sharing
  no code with `lib_f3ff.py`.
- **P2 (NOT BLIND, D1).** Row 2 — `mg-d112` at ≤ 04:12:41Z — reproduces at
  **5**, split **4 + 1** across the two repos, verdict **REFUTED**.
- **P3 (NOT BLIND, D1).** Row 3 — `mg-16eb` at ≤ 04:22:15Z — reproduces at
  **0**, verdict **UPHELD**.
- **P4 (NOT BLIND, D1).** Row 4 — `mg-5800` at ≤ 04:22:50Z — reproduces at
  **0**, verdict **UPHELD**.
- **P5 (BLIND).** At least one of the four *counts* will **not** reproduce
  exactly under my implementation, because of `--no-merges` (D7) or the
  `owner == parent` exclusion. I put this at **40%** — I expect the verdicts to
  survive and think the counts probably will too. **If P5 fails I keep it as a
  miss; it is the honest bet, not the flattering one.**

## 2. THE HEADLINE I EXPECT — the premise that was renamed

- **P6 (half NOT BLIND, D5).** The deliverable measures exactly one of the two
  premises its own population asserts. `successors()` excludes commits whose
  owner **is** the parent — so the "**no landing commit**" half of rows 1 and 2's
  titles is **never measured for any row**, and the "briefs were sound" verdict
  on rows 3 and 4 rests on a measurement that structurally cannot see the
  parent's own landing commit.
  I predict: **all four parents own ≥1 commit dated at or before their row's
  filing instant** (known for 3 and 4 by D5; blind for 1 and 2), so the
  "no landing commit" clause is **FALSE on 4 of 4** while the README reports the
  census as wrong on **2 of 4**. The figure is right about the premise it names
  and is offered as the accuracy of the census.
- **P6′ (BLIND).** The README's sentence *"Rows 3 and 4 were not [dispatched on
  a premise the tree contradicted]: 0 successor commits existed, **and their
  briefs were sound**"* is the load-bearing overreach — the soundness verdict
  ranges wider than the measurement under it. I predict this sentence survives
  in the merged README verbatim and that no committed transcript qualifies it.

## 3. The fetch-failure requirement — the ticket's addendum item 3

- **P7 (BLIND).** A **real** fetch failure (a clone whose `origin` URL does not
  resolve — not `force_fail=True`, which returns before `git fetch` runs, D9)
  nevertheless propagates correctly: `Fetched.unknown` is True, `census_row`
  returns `UNKNOWN`, `successors` returns `None`, `generations` returns `None`,
  and **no row prints "no successor"**. I predict the parent's claim **SURVIVES**
  my stronger test, 4 of 4 rows UNKNOWN. Confidence **high (~85%)**.
- **P8 (BLIND).** My forced-failure test needs a mutation control or it is
  vacuous: a `Fetched` that returned UNKNOWN unconditionally would pass P7. I
  predict the paired good-clone arm returns a non-UNKNOWN verdict, so the
  detector is shown non-constant. If it does not, my own P7 is worthless and I
  say so.
- **P9 (NOT BLIND on the wiring, D6; BLIND on the behaviour).** The
  `allow_fetch=False` branch is the **live counterexample to the addendum's
  rule inside the repaired library**: it sets `reason = "fetch skipped by flag"`,
  leaves `sha` resolved from whatever the last fetch left, and `unknown` stays
  **False** — so `print_freshness` prints `ok` and a full staleness figure for a
  repo that was **never fetched in this run**. "I could not look" rendered as
  "I looked". I predict this reproduces exactly. It is **dead as merged** (D6)
  and I will report it as LATENT, not live — calling a dead branch a live defect
  would be this audit committing the parent's own class of error.

## 4. Every printed count must be able to move

- **P10 (BLIND).** I can move row 3's count from 0 to ≥1 by adding, in a scratch
  clone outside both source repos, one commit whose message names `mg-16eb` with
  an author date before 04:22:15Z and an owner that is not `mg-16eb` — and the
  verdict flips **UPHELD → REFUTED**. So the row counts are **NOT FORCED**.
- **P11 (BLIND).** At least one printed figure in the deliverable **is** forced
  and is not labelled so. My candidate, named in advance: the `0` in
  *"0 of 4 verdicts flip at any pinned depth"* (NC4) — pinning `origin/main~k`
  can only **remove** commits from a date-bounded window that was already fully
  populated before the pin, so for rows 3 and 4 (count 0) the answer cannot
  move in the refuting direction at any k. **60%.**

## 5. The instrument's own defect class

- **P12 (BLIND).** `s3_graph.py` prints `work store: <path>, N ticket file(s)
  readable` and, with the store absent or unreadable, reports **N = 0 and
  `(none)`** rather than UNKNOWN — a third channel whose silence is read as
  absence, in the new code of the deliverable sent to remove exactly that. The
  source *names* B8 as a blind spot, which is a caveat present; the test is
  whether the caveat is **checked against its hypothesis**. I predict: named,
  not enforced. **70%.**
- **P13 (BLIND).** The suite re-run today reproduces exit **0**, selftest
  **40/0**, and all four row counts **unchanged** (the rows are date-bounded at
  2026-07-31, so later commits cannot enter them), while the freshness **shas**
  differ from the committed transcripts. A row count that *did* move would mean
  history was rewritten (B4) and would be the finding.

## 6. Correcting pm-onethird's framing

- **P14 (BLIND).** The parent brief's diagnosis — *"a census built on a channel
  took that channel's silence as evidence of absence"* — I predict is
  **substantially right but already conceded to be incomplete by the parent
  itself**: `README` §4 records that the mail store *did* contain the successor
  information and that the census's defect was the **shape of the query**, not
  the emptiness of the channel. I predict my own re-reading agrees with §4 and
  that the correction pm-onethird asked for is therefore **already in the
  deliverable**, so the thing I have to correct is the brief, not the child.

## 7. My own most likely error, filed in advance

- **P15.** The error I am most likely to make is **over-reading P6**: rows 3 and
  4's titles say only "no successor", so a landing commit does not contradict
  *their* titles at all, and I may be building a defect out of a clause that
  only two of four rows carry. If the honest reading is that the deliverable
  measured the operative premise correctly and merely aggregated two title
  forms into one sentence, then P6 is a **presentation** finding and not a
  **measurement** finding, and I will say so rather than inflate it. I record
  this now because the arc's repeated failure is an auditor whose headline is
  the defect he came looking for.
