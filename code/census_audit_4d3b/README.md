# mg-4d3b — INDEPENDENT AUDIT of mg-f3ff (the census-method repair)

mg-f3ff was filed to repair a census built on **mail routing**, and merged
**unaudited**. This item was filed late to audit it. Two things were asked for:
re-derive the four rows myself from a **fetched** `origin/main`, and check that
a **failed fetch prints UNKNOWN rather than "no successor"**.

    sh run_all.sh          # ~4 min, pure Python 3 + git, no third-party packages

Suite exit **0**. Selftest **40 checks, 0 FAIL**.
Predictions committed at **`c372c54`**, before any script here existed.

---

## THE VERDICT IN ONE PARAGRAPH

**The census figures are CONFIRMED and the fetch-failure rule holds where
mg-f3ff tested it. The defect is one layer up, in the part mg-f3ff did not
test: its own summary output.** All four rows re-derive to the same numbers
under a reader sharing no code with `lib_f3ff` — 7 / 5 / 0 / 0, REFUTED /
REFUTED / UPHELD / UPHELD, `2 of 4`, identical on both clocks. A **real**
fetch failure (not `force_fail=True`, which returns before `git fetch` is ever
spawned) propagates to UNKNOWN through mg-f3ff's own library in all six failing
arms. But run mg-f3ff's own `s1_rows.py` under that failure and its summary
block prints *"all 4 are now checked against the tree"*, *"The census was WRONG
on 0 of its 4 rows and RIGHT on 0"*, *"4 of 4 checked, 0 refuted"*, and four
rows of `0 / 0` — then dies on `len(None)`. **The check that cannot distinguish
"I looked and there was nothing" from "I could not look" is the sentence this
whole ticket exists to eliminate, and it is in the deliverable's own summary.**

---

## 1. The four rows, re-derived (`a1`)

The reader here is deliberately **not** mg-f3ff's. mg-f3ff asks git to match
(`git log --grep <parent> -i`); this reads **every commit reachable from the
ref** and matches in Python. A shared defect in git's regex, `-i` semantics or
encoding handling is therefore impossible. Both repos are small (387 and 429
commits at the run's `origin/main`), so reading all of them costs nothing.

| row | ticket | parent | verdict | onethird_program | one_third_width_three | mg-f3ff said |
|---|---|---|---|---|---|---|
| 1 | mg-e35b | mg-fcf1 | **REFUTED** | 7 | 0 | REFUTED, 7 |
| 2 | mg-fccb | mg-d112 | **REFUTED** | 4 | 1 | REFUTED, 4+1 |
| 3 | mg-a74f | mg-16eb | **UPHELD** | 0 | 0 | UPHELD, 0 |
| 4 | mg-dffa | mg-5800 | **UPHELD** | 0 | 0 | UPHELD, 0 |

**4 of 4 reproduce exactly**, under both clocks, with merges included *and*
excluded. `2 of 4` stands. Freshness stated: `origin/main` fetched in both
repos and resolved by sha, with the cross-path check that this worktree and
`/Users/daniel/research/onethird_program` resolve the same commit.

Two worries checked and **dismissed rather than inflated**:

- **`--no-merges`.** `lib_f3ff.git_log` passes it and its `POPULATION` text
  does not say so. `a0` counts **0 merge commits** reachable from `origin/main`
  in either repo. The flag excludes nothing on this population. Undocumented,
  not a defect.
- **The ticket-id alphabet.** `TICKET_RE` is hex-only. **0 of 2386** ticket
  files in the work store have an id outside `[0-9a-f]{4}`. Not a defect.

## 2. The premise that was renamed (`a2`)

Two of the four titles assert **two** premises:

    mg-e35b:  DROPPED VERDICT mg-fcf1 (no landing commit, no successor)
    mg-fccb:  DROPPED VERDICT mg-d112 (no landing commit, no successor)
    mg-a74f:  DROPPED VERDICT mg-16eb (no successor)
    mg-dffa:  DROPPED VERDICT mg-5800 (no successor)

`lib_f3ff.successors()` excludes commits whose owner **is** the parent —
*"the parent's own work is not its successor"*. As a definition of SUCCESSOR
that is correct and this audit does not dispute it. But it is exactly the
object the `no landing commit` clause is about, so that clause is **unmeasured
for every row**. Measuring it:

| row | parent | landing commits owned by the parent, ≤ filing instant |
|---|---|---|
| 1 | mg-fcf1 | **1** — `34c151f` (2026-07-30) |
| 2 | mg-d112 | **1** — `cd261b9` (2026-07-29, `one_third_width_three`) |
| 3 | mg-16eb | **2** — `e34a3c5`, `2539240` (2026-07-30) |
| 4 | mg-5800 | **1** — `8ce78fb` (2026-07-30) |

So the census carries two premises and mg-f3ff measured one:

    `no successor`      -- wrong on 2 of 4   (mg-f3ff's figure; a1 reproduces it)
    `no landing commit` -- wrong on 2 of the 2 rows that assert it,
                           and false-in-fact for 4 of 4 parents

**`2 of 4` is not wrong**, and the README's table header names the premise it
scores (`premise \`no successor\` is`). What does not survive is the paragraph
under it, which offers `2 of 4` as **the accuracy of the census**, and §1's
*"Rows 3 and 4 were not [dispatched on a contradicted premise]: 0 successor
commits existed, **and their briefs were sound**."* Soundness is a verdict on
the brief; the measurement under it covers one clause of the title, and every
one of those four verdicts **had in fact been committed and was findable in the
tree by its own ticket id** at the moment it was recorded as dropped.

I filed this as my most likely error (**P15**) before measuring, on the reading
that rows 3 and 4's titles say only *no successor* so nothing in them is
contradicted. That half stands. It does not rescue rows 1 and 2, whose stated
premise is unmeasured by the instrument built to check it.

## 3. The fetch-failure rule (`a3`) — where the audit lands

mg-f3ff's NC3 sets `force_fail=True`, which **returns from `Fetched.__init__`
before the `git fetch` subprocess is spawned**. It proves the UNKNOWN
*propagation*; it does not prove a real failure *reaches* it. Seven arms on
throwaway clones close that:

| arm | construction | result |
|---|---|---|
| **A** | both clones healthy — **the mutation control** | REFUTED/REFUTED/UPHELD/UPHELD — **not constant-UNKNOWN**, so B–G mean something |
| **B/C/D** | `origin` URL unresolvable in repo 1 / repo 2 / both | 4 of 4 rows UNKNOWN, `generations()` → None |
| **E** | `origin` remote removed | UNKNOWN |
| **F** | repo directory absent | UNKNOWN |
| **G** | ⚠️ **clone first so `origin/main` RESOLVES, then break the URL** | UNKNOWN — and the ref is asserted to resolve, so the pass is not an artefact of an absent ref |

Arm G is the incident's own shape: no network at boot, every checkout holding
yesterday's refs. **mg-f3ff's library gets it right, and NC3's conclusion is
confirmed by a test it did not run rather than repeated.** So does this audit's
library, tested in the same arms.

### Then the script level, which NC3 never reaches

`s1_rows.py`, copied verbatim beside a `lib_f3ff.py` whose **only** edit is the
`REPOS` constant, run against arm G's broken clone. What it gets **right**,
stated first: every row's verdict column prints `UNKNOWN`; the count prints
`?`, never `0`; the failed repo prints `onethird_program=UNKNOWN`; the chain
prose says `CHAIN: UNKNOWN`, not `none`; the reason is named. Five checks, five
passes. Then, further down the same transcript:

| | the summary block under a real fetch failure |
|---|---|
| **F1** | the accuracy table renders UNKNOWN's depth columns as **`0 / 0`** — `s1_rows.py:76-79`, `0 if not gens else len(gens)`, and `not None` is True |
| **F2** | **`n = 4, and all 4 are now checked against the tree`** prints verbatim when **0** were checked — a fixed string with no guard |
| **F3** | **`The census was WRONG on 0 of its 4 rows and RIGHT on 0`** — a substantive claim about the subject, asserted from zero measurement |
| **F4** | **`4 of 4 checked, 0 refuted`** in the superseded-figure paragraph, whose own next sentence is *"this does not round toward either"* |
| **F5** | `s1_rows.py` then **dies**: `len(L.successors(...))` on `None` at `:131` — 30 lines from the docstring reading *"callers must NOT treat None as an empty list. That confusion is the whole subject of this ticket."* |

**SCOPE, STATED RATHER THAN IMPLIED.** The per-row sections are correct.
`s0_freshness.py` exits 1 on an unreadable repo and `run_all.sh` propagates it,
so a **full-suite** run under this failure is loudly non-zero. F5's crash is
loud — but it lands *after* F1–F4 are already on stdout, and it is a traceback,
not a diagnosis. What is defective is the block a reader scanning for the
answer reads first.

## 4. The rule broken in the deliverable's own scripts (`a5`)

`lib_f3ff.successors()` returns `None` for an unreadable repo and says callers
must not treat it as `[]`. A source census of who does:

| file:line | idiom | reachable under a fetch failure? |
|---|---|---|
| `s1_rows.py:123,124` | `... or []` | **LIVE** |
| `s1_rows.py:131` | `len(successors(...))` | **LIVE** — this is F5's crash |
| `s2_controls.py:130,131` | `... or []` | LATENT (NC1 runs with a healthy fetch) |
| `s2_controls.py:283` | `len(successors(...))` | LATENT |
| `s3_graph.py:85,86` | `... or []` | **LIVE** |

**8 sites**, 6 spelling the merger as `or []`. This is not a claim that any row
verdict is wrong — `a1` re-derived all four from a disjoint reader and they
reproduce exactly. It is the claim that the rule the library states is broken
by the scripts around it, and `a3` shows what that prints.

Two more, each **executed** rather than read:

- **F6/F7 — the work store, a third channel.** Run `s3_graph.py` against an
  empty store: it prints `0 ticket file(s) readable` and `(none)` for all four
  rows, **exits 0, and no UNKNOWN appears anywhere**. Its very next printed
  line names blind spot B8. The hazard is **declared and not enforced** — and
  P9's outcome flips from HIT to MISS purely from channel silence, still
  reported as a prediction outcome. mg-f3ff enforces the same rule twice for
  repos (library + NC3) and zero times for the channel `s3` actually reads.
  *A caveat is checked against its hypothesis by running it.*
- **F8 — `allow_fetch=False`.** The repo reports `ok`, prints a resolved sha
  and a full staleness figure; the string `fetch skipped by flag` is stored in
  `.reason`, which `line()` prints **only on the UNKNOWN branch**. The one fact
  that would tell the reader no fetch happened is computed and then not shown,
  and the row prints `UPHELD`. **Its size, stated: `allow_fetch` is wired to no
  caller and no CLI flag in the merged tree** (verified by grep before
  predicting). It is **LATENT**. Calling a dead branch a live defect would be
  this audit committing the class of error it came to look for.

## 5. Every printed count, moved (`a4`)

- **Each of the four row counts MOVES.** A constructed commit naming the
  parent, owned by another ticket, back-dated to 2026-07-01, raises every row
  by exactly 1 — and rows 3 and 4 flip `UPHELD → REFUTED`. **The 0s are
  measurements, not defaults.** The negative twin is run too: the *same* commit
  dated 2026-08-01 moves nothing, so the date bound is live and not decorative.
- **NC4's `0 of 4 verdicts flip` is half FORCED, and mg-f3ff does not say so.**
  Pinning `origin/main~k` can only *remove* commits from a window closed on
  2026-07-31, so `REFUTED → UPHELD` is reachable and `UPHELD → REFUTED` is
  **not**. Rows 3 and 4 print 0 and **cannot flip at any depth, by construction
  rather than by evidence**.
- **And the quantifier is false as written.** mg-f3ff sampled depths 10, 25 and
  60. Sweeping **every** depth 0–387: **row 1 flips at depth 344, row 2 at
  371.** Its `s2` transcript is careful — *"0 of 4 flipped at depth 10"*, *"at
  depth 25"*, *"at depth 60"*. It is the **README** that writes three samples up
  as *"0 of 4 verdicts flip at **any** pinned depth."* Same place as F1–F4: the
  summary, not the instrument.

## 6. CORRECTING THE FRAMING (pm-onethird asked me to)

**The brief's diagnosis is right, and the brief is behind its own child on it.**
mg-f3ff's README §4 already records that pm-onethird's inbox **did** contain the
successor information — 2 messages on row 1, 1 on row 2, naming the successor
tickets by id before the filing instant — and concludes the census's defect was
the *shape of the query* (it looked for a verdict message **addressed to it**),
not the emptiness of the channel. That is the correction, it is already landed,
and this audit agrees with it. What the brief generalises from one instance is
*"a census built on a channel took that channel's silence as evidence of
absence."* The sharper statement, which mg-f3ff earned and the brief has not
absorbed: **a census built on a channel asked that channel one shape of
question and read a miss as an absence.** Switching channels does not fix that;
`a5`'s F6 is the same error committed on the tree-era work store.

**And the brief's remedy is one layer too low.** It says *"a check that cannot
distinguish 'I looked and there was nothing' from 'I could not look' is the
whole subject."* mg-f3ff put that check in the **library**, enforced it twice,
and proved it with NC3 — and then the **summary text** merged the two anyway, at
F1–F4, because a fixed string is not a check at all. The rule needs to reach the
sentence, not just the function.

## 7. Scorecard against `c372c54`

Fifteen predictions, committed before any script here existed. **P1–P4 are
disclosed NOT BLIND and are reported as reproductions, not as hits.** Of the
blind ones: **6 hit, 1 missed, 1 half.**

| | prediction | result |
|---|---|---|
| P1–P4 | the four row verdicts and counts | reproduce exactly — **NOT BLIND, not counted** |
| P5 | at least one count fails to reproduce (40%) | **MISS** — all four reproduce under both clocks and both merge settings. Kept as written. |
| P6 | all 4 parents own ≥1 commit at their filing instant | **HIT** (rows 3–4 disclosed not blind; 1–2 blind) |
| P6′ | *"their briefs were sound"* survives unqualified in the merged README | **HIT** |
| P7 | a **real** fetch failure propagates to UNKNOWN in mg-f3ff's library | **HIT** — 6 of 6 failing arms |
| P8 | the mutation control is non-vacuous | **HIT** — arm A returns real verdicts |
| P9 | `allow_fetch=False` prints `ok` for an unfetched repo | **HIT**, and reported LATENT |
| P10 | row 3's count can be moved 0 → ≥1 | **HIT**, and the late-dated twin moves nothing |
| P11 | a printed figure is forced and unlabelled; named candidate NC4 (60%) | **HIT** on the forcing, **and more** — the `any depth` quantifier is also false |
| P12 | `s3` reports an empty work store as 0, not UNKNOWN (70%) | **HIT** |
| P13 | the suite re-runs green, counts unchanged, shas differ | **HIT** — re-run in place: exit 0, selftest 0 FAIL, 7/5/0/0 unchanged; only freshness shas and the post-instant figures move |
| P14 | the brief's diagnosis is right but already superseded by §4 | **HIT** — see §6 |
| P15 | my own most likely error: over-reading P6 | **fires in its weak form only** — rows 3–4 are presentation, rows 1–2 are measurement |

**No prediction was edited after seeing a result.** P5 is recorded as missed.

## 8. DEFECTS OF THIS INSTRUMENT, KEPT

1. **An assertion that named the wrong object.** `a3`'s first
   *"unreadable repos return None"* check asserted that **every** repo returned
   None. In arms B/C/E/F only one repo is broken and the healthy one correctly
   returns a list — so it **FAILED 16 times against code behaving exactly as
   required**. This arc's signature shape, committed by the auditor sent to find
   it. Corrected in place; the old form and why it was wrong are in the source.
2. **My source census read my own prose as code.** `a5`'s first `or []` /
   `len()` census flagged a line of `a3_fetchfail.py` that is a **sentence
   describing the defect**. A rule that reads text as code, inside the section
   whose subject is a rule that reads one thing as another. Fixed by
   **classifying** (`CODE` / `PROSE`) rather than dropping, so the hit is still
   shown.
3. **My own selftest fixtures used ids outside the alphabet I had verified.**
   `mg-pppp` is not `[0-9a-f]{4}`, so two checks failed against correct code —
   an assertion refuted by its own fixture, two hours after I recorded as D2
   that the alphabet is hex-only. Found only because the selftest failed.
4. **`a4`'s depth sweep slices a cached commit list** instead of re-running git
   3000 times. That is licensed by history being linear (0 merges, measured in
   `a0`) — and the licence is **asserted**, at four sample depths per repo,
   rather than assumed.
5. **The first suite run died** because `MG4D3B_SCRATCH` named a directory that
   did not exist. An env var pointing at a missing path is a configuration, not
   an error; it is created now.
6. **`a3`'s script-level arm patches `REPOS` by regex.** If the patch failed to
   apply the arm would test nothing — so a failed substitution is reported as
   **VACUOUS**, not passed. Same guard on `a5`'s `WORK_STORE` redirect.

## 9. WHAT I DID NOT DO

- **I did not re-audit mg-f3ff's `s3` or `s4` findings.** The ticket-reference
  graph, the duplicate-work overlap, and the chain-reader cross-check against
  mg-e35b's independent list are unexamined here except where `a5` runs `s3`
  against an empty store. §7's `3 generations / 7 generations / 13 ground truth`
  bracket is **not** re-derived.
- **I did not re-run or re-implement NC2, the mail reader.** §6 takes mg-f3ff's
  own account of what its inbox contained at face value. I did not open
  pm-onethird's maildir at all, so the claim *"the information was present"* is
  mg-f3ff's, repeated, not confirmed.
- **I did not find or run pm-onethird's actual census code.** Neither did
  mg-f3ff; that blind spot is inherited whole.
- **I did not fix anything.** No line of `code/census_repair_f3ff/` is edited,
  no ticket body is corrected, no STATE.md row is touched. F1–F8 are reported
  where a repair would land, and the repair is not mine to file.
- **I did not reopen mg-e35b, mg-fccb, mg-a74f or mg-dffa**, and did not correct
  the `no landing commit` clause in the two titles that carry it falsely.
- **I did not search beyond the two repos mg-f3ff named.** B2 is inherited.
  `one_third`, `union_closed`, `investments` and `lineara` are unread.
- **I did not touch either source repo's working tree.** `git fetch` and
  `git log` only; every clone, broken remote and injected commit is under the
  scratchpad.
- **I did not decide whether rows 1's and 2's polecat work was duplicate.**
  mg-f3ff declined that too, for the same reason.
- **I did not check whether the `0 / 0` of F1 has ever appeared in a real
  transcript.** The committed `out_s1_rows.txt` was taken with both fetches
  healthy, so F1 is a demonstrated behaviour of the code, not an observed
  historical error.

## 10. Files

| file | what |
|---|---|
| `PREDICTIONS.md` | committed at `c372c54`, **before any script here existed**, with ten hand measurements disclosed |
| `lib4d3b.py` | the audit's reader — no import of and no code shared with `lib_f3ff`; population and blind spots in the source |
| `a0_which_tree.py` | fetch, resolve, sha, staleness, and the worktree/source cross-path check |
| `a1_rows.py` | the four rows re-derived, both clocks × merges in/out |
| `a2_landing.py` | the `no landing commit` premise mg-f3ff's instrument cannot express |
| `a3_fetchfail.py` | seven arms of **real** fetch failure, library and script level |
| `a4_move.py` | moving every printed count; NC4's forcing and its quantifier |
| `a5_selfdefect.py` | the `or []` census, the empty work store, `allow_fetch=False` |
| `selftest4d3b.py` | 40 checks, including the transcribed instants and premise strings re-derived from the work store |
| `run_all.sh` | the runner; reports the instrument's status, not `tee`'s |
| `out_*.txt` | committed transcripts of a full run |
