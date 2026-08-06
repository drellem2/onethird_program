# mg-b0ae — PREDICTIONS for the INDEPENDENT AUDIT of the mg-ea0e STATE.md relocation

**COMMITTED BEFORE ANY SCRIPT OF THIS AUDIT EXISTS.** Nothing under
`code/state_relocation_audit_b0ae/` other than this file exists at the commit that carries it.

The audited object is `cc4c663` ("docs: STATE.md IS AN EXECUTIVE SUMMARY …", mg-ea0e), whose
parent is `78ae4d9`. Both are on `main`; mg-ea0e HAS MERGED. All "old" figures below are against
`78ae4d9:STATE.md`; all "new" figures are against `STATE.md` at this branch's HEAD, which contains
`cc4c663` and no later change to `STATE.md`.

---

## 0. MEASUREMENTS ALREADY MADE — disclosed, NOT laundered into predictions

These were taken while reading the ticket and the audited commit, before this file was written. A
prediction filed on any of them would be a lie about when I knew it.

- **M1 — sizes.** `wc -l -w -c`: old `78ae4d9:STATE.md` = 386 lines / 29,125 words / 186,710
  bytes. New `STATE.md` @HEAD = 175 lines / 4,660 words / 32,772 bytes. **The BYTE figures match
  mg-ea0e's exactly (186,710 → 32,772). The WORD figures DO NOT** — its commit subject says
  29,094 → 4,658. So mg-ea0e's word instrument is not `wc -w`, and the gap is +31 old / +2 new.
  Whether that is a defect or two legitimate grains is a question for this audit, not a prediction.
- **M2 — line-count off-by-one is consistent.** mg-ea0e's prose says STATE.md is "176 lines rather
  than 387"; `wc -l` says 175 and 386. A consistent +1 on both sides is the signature of
  `len(text.split("\n"))` on a newline-terminated file. Disclosed so I do not later "discover" it.
- **M3 — the destination attempt files PRE-EXISTED this commit.** `git ls-tree 78ae4d9
  docs/state-history/` lists all seven `attempt-mg-{210d,276d,3af9,63e3,88bd,a3d4,a58f}.md`
  (plus `attempt-mg-48ab.md`, `attempt-mg-c47a-drop.md`, `ledger-row-11-L4.md`, `README.md`), and
  `--stat` shows each of the seven gaining **26 lines**. mg-34bf built them from the same ledger
  rows mg-ea0e has now appended. **Therefore any coverage or marker search run over those files
  AT HEAD can be satisfied by text that was already there and did not move.** This is the single
  most load-bearing fact I have before starting, and it is a measurement, not a finding.
- **M4 — mg-ea0e's own claims, quoted from its commit message**, which I will re-derive rather than
  check: old 186,710 B; new 32,772 B of which 2,796 composed boilerplate and 29,976 old-text-in-
  place; 157,996 B of old text found verbatim in linked files; 29,976 + 157,996 = 187,972, surplus
  **+1,262**, explained as "text deliberately carried in BOTH places, each row's retained sentence
  also sitting in its history file"; corpus 245,161 → 261,318; 4,658 words; longest line 1,772 @:124;
  **68** distinct mg-ids, **0** unreachable (34 in place, 34 one link away); markers STRUCK 8→13,
  RETRACTED 0→2, RETIRED 2→3, CORRECTED 5→7, SUPERSEDED 1→1, REFUTED 6→10, DISCHARGED 5→7,
  BROKEN 43→71, withdrawn 4→4, void 5→9, **0 lost**; lines 1-129 byte-identical to 78ae4d9.
- **M5 — two departures and one non-fix are SELF-REPORTED** by mg-ea0e (Appendix A moved as
  :180-381 not :180-382; and a second, argued in its README), plus `docs/state-of-the-wall.html`
  left stale. Self-reported departures cannot be my headline; only unreported ones can.
- **M6 — a later commit exists.** `0c9125e` (mg-2de0) landed AFTER `cc4c663` and refutes mg-00b9's
  Lemma B outer bound. It did not touch STATE.md. This is context for the cold read (§5), and the
  fact of its existence is a measurement.

I have NOT yet: run any diff, opened `build.py` or `verify_relocation_ea0e.py`, opened
`docs/audit-stage-process.md`, `threads-chronology.md`, any `attempt-*.md`, or read new `STATE.md`
past the sizes above.

---

## 1. PREDICTIONS — scored later in OUTCOMES.md, hit or miss, no rewording

Every prediction names the POPULATION it is over and the GRAIN of its value.

### The surplus (brief's attack #1)

- **P1 (0.60) — the retained-sentence explanation UNDER-explains the +1,262.**
  Population: the 7 relocated ledger rows. Grain: bytes. I predict the total bytes of the
  deliberately-duplicated "retained opening sentence" across those 7 rows is **strictly less than
  1,262** — i.e. the parent's stated cause is real but not sufficient, and other duplication
  (status labels, row ids, link boilerplate counted on both sides) makes up the rest. *Miss if the
  retained sentences alone sum to ≥ 1,262, or if the surplus decomposes exactly.*
- **P2 (0.75) — the surplus is not hiding a loss.** Population: every line of old STATE.md that is
  not one of the 7 rewritten ledger rows. Grain: whole stripped line, exact-string. I predict
  **0 lines** absent from the reachable corpus. *An instrument that could show the positive: the
  same line-presence check, run with one destination file withheld, must report a non-zero miss
  count — I will run that negative control and print it.*
- **P3 (0.85) — a NON-ZERO number of bytes credited to "found verbatim in linked files" was
  ALREADY IN THOSE FILES at 78ae4d9.** Population: the 157,996 B mg-ea0e credits. Grain: bytes
  attributable to pre-existing vs added lines. *This is the mechanism by which a byte total can
  balance while content is lost.*
- **P4 (0.65) — but excluding pre-existing text does not open a hole.** Population: the 7 moved
  rows, all three columns. Grain: column text, exact-string. I predict coverage of every moved row
  is still complete when ONLY lines ADDED by `cc4c663` are allowed to satisfy it.

### The markers (brief's attack #2)

- **P5 (0.80) — the 10 marker increases are a POPULATION artefact, not evidence of safety.**
  I predict that over a like-for-like population — old STATE.md vs (new STATE.md **plus only the
  text `cc4c663` added**) — at least one marker's count is **equal, not increased**, and that the
  parent's larger corpus figure is explained by pre-existing attempt-file text and the new files'
  provenance headers.
- **P6 (0.70) — 0 marker occurrences lost at OCCURRENCE grain.** Population: every occurrence of
  STRUCK / RETRACTED / RETIRED / CORRECTED / SUPERSEDED / REFUTED / DISCHARGED / BROKEN /
  withdrawn / void in old STATE.md, matched by its *containing line or cell*, not counted.
  Counting is not matching: 43 BROKEN → 71 BROKEN is consistent with all 43 being deleted and 71
  new ones appearing. *Instrument that could show the positive: the same occurrence match with a
  deliberately corrupted context string must fail to match.*

### The untouched prefix and the mathematics

- **P7 (0.90) — lines 1-129 are byte-identical to `78ae4d9`, not retyped.** Grain: SHA-256 over the
  exact byte range. *Retyping is exactly what a hash detects and a word-diff hides.*
- **P8 (0.75) — 0 mathematical claims reworded.** Population: every line/cell of old STATE.md
  carrying a mathematical token (a fraction, an inequality operator, `^`, `sqrt`, `Theta`, `O(`,
  `beta`, `eps`, `log`, or a bare number adjacent to one of these). Grain: exact string. I will
  print the population size before the verdict, because a verdict over an unstated population is
  the defect this arc keeps finding.

### The ids

- **P9 (0.50) — my own id regex will NOT find exactly 68 distinct mg-ids in the old file.**
  A count is a fact about a regex as well as a file. *Miss if I get exactly 68.*
- **P10 (0.85) — 0 mg-ids unreachable**, where "reachable" is defined by ME as: present in new
  STATE.md, or present in a file that new STATE.md links to *by a link I parsed out of the file*,
  not by a hand-list of the three moves.

### Process and the cold read

- **P11 (0.50) — mg-ea0e exercised judgement beyond its three moves in at least one place it did
  NOT self-report.** Population: the full `cc4c663` diff of STATE.md. *Self-reported departures
  (M5) do not count.*
- **P12 (0.60) — the new STATE.md answers the Cheeger/spectral-gap question within its first
  screen** (defined in advance as the first 60 lines), timed.
- **P13 (0.70) — whatever answer it gives is STALE**: STATE.md @HEAD does not reflect mg-2de0's
  refutation of the Lemma B outer bound (`0c9125e`, merged after `cc4c663`). This is a finding
  about the corpus, not about mg-ea0e, and I will label it as such.

---

## 2. WHAT I WILL NOT DO

- **I will not use `git patch-id` as an oracle.** This arc has 1 of 234 pairs with identical
  content under different patch-ids. Byte-level presence checks answer this ticket directly and
  patch-id answers a question about diffs against bases, which is not the question.
- I will not re-verify mg-34bf's original attempt-file construction; my population starts at
  `78ae4d9`.
- I will not fix anything I find in STATE.md. This is an audit; a repair is a different ticket.

## 3. DEFECTS OF THIS INSTRUMENT

Recorded in OUTCOMES.md as they occur, including my own. The parent arc's convention is that an
auditor committing the defect it audits is the most valuable row in the table, not the most
embarrassing.
