# mg-e331 — PREDICTIONS, committed before one line of the instrument exists

The ticket is: `mg-ea0e` restructured `STATE.md` from 186,710 B / 29,094 w to 32,772 B / 4,658 w
on 2026-08-06 against a stated target of **under 6,000 words**, nothing held it, and four days
later it is back. My job is to characterise the growth, decide whether the target is right, build
a ratchet, and demonstrate that the ratchet fails on a commit that breaks it.

## H — WHAT I ALREADY MEASURED BEFORE PREDICTING (disclosed, not laundered into bets)

A prediction about a number I have already read is not a prediction. These are **measurements**
and they are stated so that nothing below can be scored as a bet that was never at risk.

- **H1.** `STATE.md` at HEAD (`f9771023`) is **123,612 bytes / 18,969 words**, not the
  110,640 / 16,861 the ticket quotes. The ticket's figures were mg-9bc2's reading at
  `641ef428` and **two more landings have arrived since** (`4fcbc713` mg-2f44 +627 B,
  `f9771023` mg-8d63 +11,689 B). The regression is **66% of pre-restructure by bytes**, not
  59%, and it grew **while this ticket sat in the queue**.
- **H2.** I ran the per-commit size walk over `git log --first-parent main -- STATE.md`
  before predicting. **mg-ea0e IS NOT THE FIRST RESTRUCTURE.** `57f962f1` (mg-34bf,
  2026-07-30) cut 192,898 → 164,577 B and the file was back at 186,710 B **eight hours and
  eight landings later**. So the arc has paid for this **three** times, not twice, and the
  ticket's own count is one short.
- **H3.** I ran the per-section decomposition. Of the +90,840 B added since mg-ea0e landed,
  **+47,536 (52%) is the `## Attempt index` section**, +13,859 the `### Full ledger`,
  +11,189 the section titled `## The one-paragraph state`.
- **H4.** `docs/state-history/` exists, was created by mg-ea0e, holds 9 `attempt-*.md` files
  plus 4 others, and **has been written to since** (three commits, all on 2026-08-07).

## P — THE BETS

Scored in `out_p1_growth.txt` and `out_x1_positive.txt` by machine, not by hand.

- **P1 — 0.80 — THE GROWTH IS NEW ROWS, NOT ACCRETION IN OLD ONES.** In the attempt index,
  the bytes added by rows that did not exist at `cc4c663e` exceed the bytes added by growth of
  rows that did, by at least 5×. If this loses, a ratchet is the wrong instrument: a file whose
  every existing row is swelling is one where the content genuinely has no other home, and
  capping the total would simply start failing every landing.
- **P2 — 0.75 — AND THE LEDGER IS THE OPPOSITE.** In `### Full ledger`, **zero** rows were
  added and the growth is entirely in-place. The two halves of the file are growing by two
  different mechanisms and a single explanation of "STATE.md is big" covers neither.
- **P3 — 0.85 — THE 6,000-WORD TARGET IS UNREACHABLE AT HEAD AND RATCHETING TO IT WOULD BE
  RED ON ARRIVAL.** Even if every byte of the new attempt-index rows were relocated to
  `docs/state-history/`, the residue exceeds 6,000 words. I therefore expect to **decide
  against mg-ea0e's number as a gate threshold** and set the ceiling where the file stands.
  This is the prediction I am least comfortable with and the one most likely to read as
  laundering, so it is stated in advance with its own falsifier: if the residue comes in
  under 6,000 words, the target is right, I am wrong, and the ratchet goes to 6,000.
- **P4 — 0.70 — THE CONTENT HAS A HOME AND DID NOT GO THERE.** At least 3 of the new
  attempt-index rows were added by commits that wrote **nothing** to `docs/state-history/`.
  This is what separates "a ratchet will relocate the problem" from "a ratchet will send
  content to a destination that already exists and is already conventional here".
- **P5 — 0.90 — THE RATCHET GOES RED ON REAL COMMITTED BYTES, NOT ONLY ON A SYNTHETIC
  MUTATION.** `git show b80dea0e:STATE.md` (29,094 w, the pre-restructure file) drives the
  ratchet RED, and `git show cc4c663e:STATE.md` (4,658 w, the post-restructure file) also
  drives it RED — in the *other* direction, as slack that must be ratcheted down. A ceiling
  that only ever answers one way is half a control.
- **P6 — 0.60 — THE GATE'S OWN NEGATIVE-CONTROL DISCIPLINE WILL CATCH ME AT LEAST ONCE.**
  At least one of my probes will come back UNFALSIFIABLE or SETUP FAILED on its first run —
  i.e. a predicate already satisfied by the good input. Every author in this arc who wrote
  this prediction down has won it.
- **P7 — 0.55 — THE MERGE GATE WILL NOT NOTICE STATE.md TODAY.** Running the existing
  `./build.sh` against a tree whose `STATE.md` is the 186,710-byte pre-restructure file exits
  **0**. The gate that exists is blind to the property this ticket is about, which is why the
  remedy is a new gated field and not a new schedule.

## E — MY OWN ERRORS, FILED IN ADVANCE

- **E1. A RATCHET WHOSE CEILING CAN BE RAISED IS A SPEED BUMP.** Mine can be raised — one
  line in `CEILING.json`, in the same commit, with a written reason. I do not have an argument
  that this stops growth; I have an argument that it stops **silent** growth, which is the
  defect actually named. If the ceiling is raised at every landing, this instrument will have
  produced a changelog of the regression and nothing else. That is a real outcome and I am
  recording it as a possible one rather than claiming it away.
- **E2. I AM MEASURING A FILE I AM NOT EDITING.** This branch does not change `STATE.md`.
  So my ratchet is green on my own branch by construction, and a check that has only ever been
  green on the branch that introduced it is exactly what P5 exists to answer for.
- **E3. THE CEILING I SET IS A NUMBER I READ TODAY.** If another branch lands a legitimate
  STATE.md change between my measurement and my merge, my ceiling is stale at its own landing
  and the gate goes red for a reason its author cannot act on — mg-724a's own recorded/gated
  split is about precisely this hazard, and I am walking into the same one from the other side.
  The remedy available to that author is the one-line raise, which is E1's problem again.
- **E4. WORDS, NOT BYTES.** mg-ea0e's target is in words, so the gated field is words; but
  `len(text.split())` is a definition, not a fact, and a future editor who reformats tables
  can move it without changing what a reader must read. I am gating a proxy and saying so.
- **E5. I MAY BE BUILDING THE THING mg-ea0e BUILT.** mg-ea0e also landed a `run_all.sh` and a
  verification transcript. Its defect was not that it lacked a script; it was that nothing
  **asked** the script at a landing. If my suite lands without being wired into the merge gate,
  I have committed this ticket's own defect inside the instrument that repairs it.
- **E6. THE POSITIVE CONTROL RUNS A CHECKER, NOT A MERGE.** Driving `ratchet.py` red against
  a planted tree is weaker evidence than a refinery merge request that comes back `failed`.
  mg-724a raised exactly this bar and cleared it with a live MR. If I do not clear it, the gap
  is named here in advance and not discovered later.
- **E7. `docs/state-history/` COULD BE THE NEXT STATE.md.** Relocation with no ratchet on the
  destination moves the growth rather than stopping it. Nothing here measures the destination,
  and that is a scope decision, not an oversight.
- **E8. I HAVE READ THE ANSWER TO P1–P4 IN OUTLINE ALREADY** (H2, H3), so P1 and P2 are bets
  about how a *rule* scores a population whose shape I have seen, not discoveries. They are
  kept because the rule can still disagree with the eyeball, and if it does the rule wins.
