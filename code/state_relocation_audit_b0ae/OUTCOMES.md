# mg-b0ae — OUTCOMES: the pre-registered predictions, scored

Scored against `PREDICTIONS.md` as committed at `9daa0f2`, before any script of this audit
existed. Nothing below has been reworded. **8 hit, 5 missed.**

Every figure cited here names the transcript that produced it. A figure with no transcript
is not in this table.

| # | prediction (abbreviated — the file has it in full) | verdict | what was measured |
|---|---|---|---|
| P1 | retained-sentence bytes are **< 1,262**, so mg-ea0e's stated cause UNDER-explains its surplus | **MISS** | 1,346 B (`out_b1_bytes.txt` B1.4). It **over**-explains, by 84 B. Direction wrong. |
| P2 | 0 non-rewritten lines absent from the reachable corpus | **HIT** | 0 of 441 atoms MISSING (`out_b2_coverage.txt` B2.1) |
| P3 | a NON-ZERO number of bytes is credited to text that pre-existed in the destinations | **MISS** | 0 B and 0 atoms (`out_b1_bytes.txt` B1.3, `out_b2_coverage.txt` B2.1). Every old atom is satisfied by new STATE.md or by text **this commit added**. The mechanism I predicted would disguise a loss is simply not present. |
| P4 | coverage of the 7 moved rows survives when only ADDED text may satisfy it | **HIT** | 0 of 59 columns missing (`out_b2_coverage.txt` B2.4) |
| P5 | the 10 marker increases are a POPULATION artefact | **HIT** | all 10 pairs reproduce **only** at the transitive closure; 7 at one hop; 2 like-for-like (`out_b3_markers.txt` B3.1) |
| P6 | 0 marker occurrences lost at OCCURRENCE grain | **HIT** | 79 of 79 survive; control 79 of 79 die under a 1-char edit (`out_b3_markers.txt` B3.2) |
| P7 | lines 1-129 byte-identical, not retyped | **HIT** | same SHA-256; the longest identical prefix is **exactly** 129 (`out_b4_prefix_math.txt` B4.1) |
| P8 | 0 mathematical claims reworded | **HIT** | 0 of 251 math atoms absent; control 251 of 251 (`out_b4_prefix_math.txt` B4.2) |
| P9 | my own regex will NOT return exactly 68 distinct ids | **MISS** | exactly 68, and the loose pattern adds 0 (`out_b5_ids.txt` B5) |
| P10 | 0 mg-ids unreachable | **HIT** | 0 unreachable, 0 at hop ≥ 2, 34/34 split confirmed (`out_b5_ids.txt` B5.1) |
| P11 | mg-ea0e exercised unreported judgement beyond its three moves | **MISS** | 0 lines removed from outside the three ranges (`out_b6_process.txt` B6.1). The nearest thing found is smaller and is recorded as F3 below. |
| P12 | the new file answers the Cheeger question within the first 60 lines | **MISS** | the answer completes at :95 (`out_b8_findability.txt` B8). It is answered — the boundary I pre-registered was simply wrong, and see F5, which is the more interesting result. |
| P13 | STATE.md @HEAD is stale w.r.t. mg-2de0 | **HIT** | 4 of 5 recent ids unnamed, including mg-2de0's refutation (`out_b8_findability.txt` B8.2). **Not mg-ea0e's defect** — that commit landed after. |

## Why the misses matter more than the hits

P1 and P3 were my two attacks on the surplus, filed in the belief that a balancing byte total
is the classic disguise for a loss. **Both failed, and they failed in the direction that
strengthens mg-ea0e**: there is no pre-existing-text credit at all, and the double-counting is
larger than the surplus rather than smaller. The instrument that would have caught the
opposite is in `out_b2_coverage.txt` B2.3 — withhold the largest destination and 142 atoms go
missing; corrupt every atom by one character and all 441 go missing. It can see an absence. It
did not see one here.

P9 and P11 were bets that the parent's population and mandate would not survive re-derivation.
They did.

## Defects of THIS instrument

| # | defect | how it surfaced | state |
|---|---|---|---|
| D1 | my link closure resolved a bare `README.md` inside `docs/state-history/` to the **repo-root** README, not the sibling — swapping a 40-line index for a project README and changing the corpus | 3 of 10 marker rows looked unreproducible; the parent's own closure had 13 files and mine had 15, with the sibling absent | FIXED in `libb0ae.py:link_closure`, comment kept at the site |
| D2 | my quoted-clause matcher tested exact substrings against hard-wrapped prose, so a clause spanning a newline read as MISSING | 4 of 9 quotes in the composed paragraph reported not-found; two were still not found after the whitespace fix and turned out to differ only in **emphasis markup** | FIXED — three grains now printed (`out_b6_process.txt` B6.2b) |
| D3 | my first `git ls-tree` call passed an empty pathspec and aborted the run | crash on the first execution of B1 | FIXED; it is why `run_all.sh` carries an empty-transcript guard, since the same class of fault is what makes a runner report exit 0 having executed nothing (mg-2de0's first recorded defect) |
| D4 | P1 was filed as a comparison against **1,262** without pinning whose decomposition that number is over. mg-ea0e's two addends are defined differently from mine, so my ±84 residual is partly an artefact of my own grain, not a fact about the file | scoring P1 | recorded, not fixable after the fact — the prediction was scoreable but not clean |
| D5 | **the ticket brief I was given states "29,125 words -> 4,658", which mixes two instruments.** 29,125 is `wc -w`; 4,658 is Python `.split()`. The same old file is 29,094 under `.split()`. I disclosed 29,125 as a measurement in PREDICTIONS.md §0/M1 and correctly deduced that mg-ea0e's instrument was not `wc -w` — and then did not check whether my own brief had mixed them | `out_b1_bytes.txt` B1.1, which prints every count under both instruments | the brief's word figure is corrected in README.md §Corrections; mg-ea0e's own pair (29,094 → 4,658) is internally consistent and reproduces |
| D6 | this audit is **not** a cold read of the ticket's §5. By the time I ran it I had read :125-175 in detail while building B1-B7 | disclosed rather than discovered | see README.md §5, which states what I had and had not read at the moment of the reading |
