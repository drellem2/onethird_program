# mg-6df0 — the refusal, the product, and the extent

Target: mg-ec07's **E-5**, **E-4** and **E-2** on `code/hodge_leverage_landing_e1d0/verify_landing.py`
(the census made lossless over the site by mg-ff3e / `c7f9079`, audited by `8cdda32`).

    sh run_all.sh          # ~2 min, exit 0

Report: `docs/OneThird-Hodge-Side-Leverage-Mg9207RepairAudit-Repair.md`.
Predictions, written before the first run, with **six misses kept as written**: `PREDICTIONS.md`.
Committed transcript: `out_repair_6df0.txt`. One hand-run transcript of another deliverable's
instrument, kept as evidence for a disturbance this repair causes: `out_ff3e_rerun.txt`.

## Two findings, one shape, at two levels

| | |
|---|---|
| **E-5** | the fix was applied **where the defect was found** and not where it **occurs**. mg-ff3e found `"FIGURE CENSUS" in row` in its own scoring code, fixed it with `heading()`, wrote it up as R5 item 3 — and the same construct was live **forty lines away** in `reseal()`, in the file it was repairing |
| **E-4** | the enumeration was over **KINDS** where the population is **SITES × KINDS**. Each kind was checked at one site, so the mutation caught at H8 was **exit 0** at the `STATE.md` site |

Both are *a scope nobody chose*. So this deliverable is scored by scope, not by the line:
`R2` sweeps the **tree** for the construct, and `R3` reports the **matrix**, not a total.

## What changed in the artifact

| | |
|---|---|
| `heading()` | promoted to module level and used by **every** caller that identifies a gate row — the local copy in the negative control is gone, and `reseal()`'s refusal is keyed on it. `"SITE RECORD"` as a substring selects **6 of 34** rows; as a heading, **3** |
| `framed_row()` | the `STATE.md` site is the ledger **row and the header lines it is read under**, not one line. The column headers that say what its cells *mean* are inside the record |
| `ANCHORS` | the three sites as **data** — name, file, cutting function, anchor text, write-back — so the printed extent and the negative control are both *derived* from the same table |
| `texts_from(files)` | mutations go through the **file** and the sites are re-cut from it. A battery that mutates site texts in place cannot exhibit a site-boundary defect: it is testing the projection it was handed |
| `EXTENT_OF` + `site_extents()` | what a site **is**, keyed on the anchor function and printed with measured counts. A site whose anchor has no declared extent makes the run **red** |
| `kind_matrix()` | **12 kinds × 3 sites**, every kind derived by a rule and attempted at every site, run on every invocation |

## The evidence

| | |
|---|---|
| `R1b` / `R1c` | `partition` bent lossy, then `--reseal`: **exit 1, REFUSED**, record unchanged. Revert **that one statement** to the substring test and the same probe is **exit 0, BLESSED**, record changed. The fix is load-bearing at its finest unit |
| `R1d` | a wrong live figure is still **REFUSED** — the half that already worked is not weakened |
| `R2a` | 429 `.py` files swept, **4 remaining occurrences, 0 undispositioned**. ⚠️ **Two of them nobody had reported** (`repair_835f.py:309`, `audit_8916_repair.py:518`) — the reported line is never the population |
| `R3a` | **28 of 28 applicable cells fire, 0 silent**, 8 `n/a` each with the reason its derivation failed. `K09 @ the STATE.md row` is mg-ec07's **X1** |
| `R3d` | **X1 on disk: exit 1**, `SITE RECORD @ the STATE.md row` refuted, every FIGURE row green — against **exit 0, 0 refuted** at the parent commit |
| `R3f` | **X2 is still silent, and declared**, with the cost of covering it measured: the ledger's other **22 rows / ~44 000 characters** |
| `R6a` | **the probes precede the fix in git** — re-derived from `git log`, not asserted |

## The disturbance, stated first because it is the largest consequence

**A site is no longer a contiguous substring of its file**, at 1 of 3 sites. Two shipped instruments
assume it is, and both now **stop early**:

- `audit_ec07.py` — `A5b` raises `AssertionError: the edit did nothing`, so `A5b`, `A7` and `A8`
  never run. **The measurement A5b makes is re-derived in `R3g`**: one figure exchange per site on
  disk, 3 of 3 exit 1 with `FIGURE ORDER` refuted and `SITE RECORD` green.
- `repair_9207.py` — `R1` still fires **6 of 7** label probes and its seventh **reports** itself
  (`E7: the site text does not occur exactly once in STATE.md`), which is its own convention
  working; `R2` then raises `TypeError: write() argument must be str, not None`, which is the same
  convention **missing** one section later. Transcript: `out_ff3e_rerun.txt`, run once by hand.

Both need the same one line — `with_site(files, name, new_site)`, which the artifact now exports,
in place of `text.replace(site, new, 1)`. **Neither is changed here**: they are other deliverables'
instruments under committed transcripts, and this repair's brief is not to edit them. The
assumption they encode was never written down anywhere, which is why it is worth a ticket.

## What is NOT covered

- **The ledger's other rows** (X2). The site is a row and its frame, not the table. Covering it
  freezes ~44 000 characters of unrelated verdicts behind a reseal — a trade pm-onethird sizes.
- **The residue is not closed and the ratio barely moves**: **282 600 of 320 509** characters
  (88.2%) of the three files are still outside every record. What closes is a **kind**.
- **`E-5`'s construct in two other instruments**, dispositioned in `R2a` with their exposure
  measured (each selects 6 rows where 3 were meant) and their consequence read: both feed a
  `print`, neither scores a verdict.
