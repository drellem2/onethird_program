# mg-ff3e — predictions, written before the first run

Every row below was written before `repair_9207.py` was run for the first time. **Misses are kept
as written**, with what they turned out to be, because a prediction quietly edited after the fact
is not a prediction.

## The exit code

**0.** Not because the repair cannot fail — R1 and R2 are the whole question — but because the
seven label-side exchanges are the mutation the new comparison exists to catch, and because the
one thing here that is *expected* to come back red (mg-9207's own E rows, R4) is scored as a
refuted **prediction of silence**, not as a refuted check of this instrument's.

## R1 — the label half, on disk

| probe | prediction |
|---|---|
| `R1a` clean tree | exit 0, 0 refuted rows |
| `E2` H8's mg-a2bd table labels (mg-9207's own, verbatim) | **runner red; `SITE RECORD` for H8 refuted; `FIGURE CENSUS` and `FIGURE ORDER` for H8 both green** |
| `E2b` the bbe83b5 table's two row labels | same |
| `E3` the two historical column headers | same |
| `E6` §14's two correction attributions | same, at `§14` |
| `E7` the `STATE.md` row's two history anchors | same, at `the STATE.md row` |
| `E8` a figure inside a marked quotation | same, at `§14` |
| `E9` the three-column table's alignment | same, at `H8` |
| `R1e` restorations | 7 of 7 return exit 0, sha256-verified |
| `R1f` crashes | **1 of 7 — `E2` only.** mg-9207's `J-3`: mg-8eca's `transpose` freezes `H8_TABLE` as a literal and asserts it occurs once, and `E2` rewrites those two lines. The gate rows print before the negative control runs, so the verdict is still readable; the **exit code** is not the gate's. J-3 is mg-9207's own open item and is **not** in this assignment's scope — it is reported here, not repaired |

The `FIGURE CENSUS`/`FIGURE ORDER` half of each row matters as much as the fire: it is the
artifact's own evidence that the mutation moved no figure, so a fire is attributable to the half
of the record that was not being compared and not to a designated reader breaking.

## R2 — the defect reinstated

| deletion | prediction |
|---|---|
| `D1` (e) deleted whole | **silent — 0 of 7 caught at the gate.** Without this, "the check fires" and "the instrument fires" are the same sentence |
| `D1b` only the `SITE RECORD` comparison | **silent — 0 of 7.** The finest unit: this row alone is what catches them |
| `D2` only the `RECORD PARTITION` row | **still red — 7 of 7.** A different check; it is not what catches a label swap |
| `D3` `partition` made lossy (segments shorter than 2 chars dropped) | **`RECORD PARTITION` red at 3 of 3 sites.** A claim of exhaustiveness that cannot fail is the `x == x` this arc has now met twice |

## R3 — the exhaustiveness map (a fixture, declared)

Every segment and every figure of every site, mutated alone. **All fire.** The population is
derived from `partition`, so the prediction is about a population nobody wrote down: roughly 70
segments and 69 figures over the three sites. Empty/whitespace-only segments are reported as an
**absence with the reason** (there is no character in them to mutate) rather than counted as
passes.

## R4 — the instruments that raised it, re-run unmodified

| | prediction |
|---|---|
| mg-9207 exit | **1, and that is correct.** Its `E2`/`E2b`/`E3` rows predict SILENCE and silence is what this removes |
| mg-9207 E-findings | **0**, down from 3 |
| mg-9207 `C3` | **still CONFIRMED, 12 of 12** — the `FIGURE ORDER` row is still the only gate row that failed on a *figure* exchange, after two rows were added to the gate. This is the row most at risk from this repair and it is the reason the record is masked with a value-independent marker rather than frozen with the figures in it |
| mg-9207 `J-3`/`J-2`/`J-1` | **still raised.** Not this assignment's items; nothing here should close them and nothing here should disturb them |
| frozen transcripts | 5 of 5 sha256-identical after every re-run |

## What would refute this repair

- Any of the seven exchanges leaving the gate silent on disk.
- Any of them caught by something other than `SITE RECORD` — that would mean the fire is a
  designated reader breaking, i.e. re-measuring a check that already existed.
- `D1b` still red — the row would not be load-bearing.
- mg-9207's `C3` moving off 12 of 12 — the repair would have broken the previous generation's
  result to close its own.

## Misses from the first run, kept as written

*(filled in after the first run; a prediction edited to match the result is not a prediction)*

- **`R1f` — predicted 1 crash at `E2`, observed 1 crash at `E2`.** Held. Recorded here because it
  is the one row where the *expected* observation is a defect that belongs to somebody else's
  ticket.
- **A MISS OF OMISSION, and the biggest thing the first full run found: nothing above predicted
  anything about mg-8aae's `A3`, and `A3` can no longer run.** It picks its probe slot by a
  procedure and controls it by **blanking the slot and requiring the runner to stay green**. After
  this repair, blanking any prose makes the runner red, so the search returns nothing:
  `no unread prose slot found` at **6 of 6** slots, which with its three aggregate rows is 9 of
  mg-8aae's 10 refuted rows. The prediction table above should have had a row for it and did not.
  It is reported as a **disturbance** (R4d), with G-1's closure re-derived by mg-8916's own
  instrument and by `N10`–`N13` (R4e) — and it is also the strongest available statement of what
  the repair does: **mg-8aae's own search for text the gate does not read now finds none.**
- **A defect of this instrument's own, found before the first full run and kept here rather than
  quietly fixed:** the attribution check first read `"FIGURE CENSUS" in row`, and the `SITE
  RECORD` row's own explanation *names* `FIGURE CENSUS` and `FIGURE ORDER` — so every probe was
  scored as having broken a figure row, 7 of 7, and the check went red for a reason that was
  entirely its own. It is the same shape as the defect being repaired (a comparison keyed on
  something wider than the field it means), and the fix is `heading()`, used everywhere a row is
  identified. It is item 3 of R5's self-application list.
