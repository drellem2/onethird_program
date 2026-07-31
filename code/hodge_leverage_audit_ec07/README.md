# mg-ec07 — independent audit of mg-ff3e's repair of mg-9207

Target: `code/hodge_leverage_landing_e1d0/verify_landing.py` at HEAD — the census made
**"position-aware over the WHOLE record"** by `c7f9079` / `11ef9a9`, reported by `3bf0cd2`.

    sh run_all.sh          # ~1 min, exit 1 (this audit raises findings)

Report: `docs/OneThird-Hodge-Side-Leverage-Mg9207Repair-IndependentAudit.md`.
Predictions, written before the first run with every miss kept: `PREDICTIONS.md`.
Committed transcript: `out_audit_ec07.txt`.

## The verdict in one line

**It fixed the SET, over the site — and the projection moved up a level to the SITE.** The record
really is lossless: 37 866 of 37 866 characters of the three sites cannot be substituted in
silence. But the same *kind* of exchange mg-9207 raised is still silent at the site the
enumeration did not visit, and one `--reseal` turns any label exchange fully green.

## Not a replication

`repair_9207.py` and `audit_8eca_repair.py` are **not run** and their bottom lines are **not
quoted**. Every population here is derived from the tree by `audit_ec07.py`. The only thing
imported from the artifact is the **gate itself** — an audit that re-implements the gate audits
its own re-implementation.

And every new control is demonstrated against a commit where the defect is still present: `A1`
runs its byte census against the gate at `eb600f7`, the repair's parent, as well as at HEAD.

## Question 1 — did it fix the SET, or the next field?

| | |
|---|---|
| **A1** | every character of every site substituted **alone** — 37 866 of them, derived from the tree. **37 866 of 37 866 fire.** Against the pre-repair gate at `eb600f7` the same instrument catches **462** (1.2%). The claim "lossless over the site" is true and is now measured at the finest unit there is |
| **A2** | which row catches it. `SITE RECORD` 37 866, `FIGURE CENSUS`/`FIGURE ORDER` 462, **`RECORD PARTITION` 0** — `rejoin(partition(raw)) == raw` is an identity that holds for *every* string, so no document edit can move it. Not a defect; the number is the point |
| **A5** | **the field it does not reach, on disk.** `X1` exchanges the two **column headers of `STATE.md`'s ledger table** — the identical mutation mg-9207 raised as `E3` and mg-ff3e enumerated and caught. **Exit 0, 0 refuted.** `X2` (two ledger row verdict labels) likewise. `X3`, the same kind *inside* a site, is **exit 1** with `SITE RECORD @ H8` refuted — so the silence is the gate's, not the probe's |
| **A6** | the printed reason against the code. *"text outside the site is not read, **because a site is a section**"* — 2 of 3 sites are sections; the `STATE.md` site is **one line** from `find_line`. **88.2%** of the three files is outside every record |

**Finding E-1** — the residual projection is the **site**, and the same kind of exchange is still
silent in it. **Finding E-2** — the sentence that sizes that residue for a reader is not true of
the code at 1 of 3 sites, which is the shape mg-ff3e's own R5 opens by naming.

## Question 2 — did the same-kind enumeration HAPPEN?

Checked from **git** and from the runner's own stdout, not from mg-ff3e's account of itself.

- **It exists**: seven probes, `N19`–`N25`.
- **Each was CHECKED, not named**: 7 of 7 carry a verdict written *before* the run and 7 of 7 carry
  an *observed* verdict, in the runner's own stdout on this run.
- **It is substantially the parent's own**: 4 of 7 are mg-ff3e's additions; 3 carry finding ids
  mg-9207's own artifact names.
- **It did not demonstrably precede the fix**: **0 of 7** exist at any commit before `c7f9079`,
  which is the commit that lands the fix.

**Finding E-4** — the enumeration is over **kinds, not over sites × kinds**. `N21` (column headers)
was checked at `H8` and nowhere else; `X1` is that kind at the `STATE.md` site, and `X1` is silent.
The question *"what else is of the same kind?"* was asked of the **mutation** and not of the
**site**. That is where E-1 comes from.

## Question 3 — is what was confirmed still confirmed?

**Yes, and more of it.** `A3` enumerates every unordered pair of asserted figure slots with
differing values — **127 / 116 / 604 = 847** over the three sites, derived from `partition` and not
from anybody's list of twelve:

- **847 of 847 fire**, `FIGURE ORDER` refuted on every one;
- `SITE RECORD`, `RECORD PARTITION` and `FIGURE CENSUS` **green on every one**.

mg-9207's *12 of 12 at 3 of 3* is not merely re-run — it is re-derived at 70× the population by an
instrument that shares no code with it. `A5b` bridges the fixture to disk: 3 of 3 sites, exit 1,
`FIGURE ORDER` refuted, `SITE RECORD` green. `A4` turns mg-ff3e's *"an empty set rather than a
blind spot"* into a measurement: **39 of 39** equal-value exchanges are the identity map on the
bytes.

## The floor item — A7, the blessing path (no list in the assignment names it)

`--reseal` is, in mg-ff3e's own words, *"the only step in this instrument that can make a wrong
document green"*. **Nothing in the arc executes it** (`B0` = 0 invocations under `code/`).

| | |
|---|---|
| `B1` | a wrong live figure → **REFUSED**, record sha256 unchanged. The refusal works |
| `B4` | the refusal deleted, one statement → **blesses a wrong document**. It is load-bearing |
| `B2` | `partition` bent lossy → **BLESSED, exit 0**, and the record it wrote is built from a partition that is not the section |
| `B6` | a label exchange outside the seven frozen probe literals → the runner catches it (exit 1, `SITE RECORD` refuted), one `--reseal`, and then **exit 0 with 0 refuted rows** |

**Finding E-5** — the refusal identifies the rows it excludes with `"SITE RECORD" not in d`, a
substring test over the whole row, and the `RECORD PARTITION` row's own explanation *names* `SITE
RECORD`. **3 of 34 gate rows are excluded that were never meant to be**, and they are the three
that license the whole "lossless" claim. This is R5 item 3 verbatim — the defect mg-ff3e found in
its own scoring code, fixed there with `heading()`, kept in its `PREDICTIONS.md`, and did not ask
where else the same shape lived. It lived forty lines away in the file it was repairing. The fix is
the same one line: key on the row's **heading**.

**Finding E-3 / E-6** — after a reseal, the residual protection against a label exchange is exactly
the **seven strings** the enumeration named, and only because those probes locate their text by
content and report `PROBE NOT APPLIED` when it moves. Outside those seven, a blessed exchange is
exit 0 with nothing refuted. Same shape as E-1 and E-4, one level up: **what is protected is what
was named.**

## What this audit does NOT do

- **It does not fix anything.** E-5 is a one-line change and it is not made here; an audit that
  repairs its own findings has no independent check left.
- **It does not re-open the figure case.** A3/A5b confirm it at a larger population than before.
- **It does not touch J-1 / J-2 / J-3**, mg-9207's own open items. `B3`'s post-reseal exit 1 is
  adjacent to J-3 and is reported, not repaired.
- **A1, A3 and A4 are fixtures in memory, declared as such.** A5, A5b and A7 run on disk against
  the real runner with no environment variable set, and A5/A5b are the evidence.
