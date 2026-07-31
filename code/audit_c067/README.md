# mg-c067 — independent audit of the mg-132a publication-anchor repair

    sh run_all.sh                  # ~90 s, exit 0
    sh run_all.sh --at <rev>       # the same audit as of any commit — RUN THIS AFTER A MERGE

Committed transcripts: `out_c1_rebase.txt` … `out_selftest_c067.txt`. The predictions, **written
and committed before any script in this directory existed**: `PREDICTIONS.md` (`0df8ec7`, an
ancestor of `806533b` which adds the first script — `T4` reads that ordering out of git rather than
asserting it).

## Verdict: **the repair holds.** Its own transcript is stale in its predecessor's exact shape, 2 of 2 — and that is the decision working, not the defect recurring.

The ticket's second demand was to run the repaired check against the repair's own published figures
at the commit that publishes them after merge. Done, at three revs. The result:

| | committed transcript claims | re-run at HEAD |
|---|---|---|
| its own verdict (`A3a`) | `AGREES` | **`DISPLACED`** |
| figures displaced (`A1c`) | 1 | **3** |
| anchors not reachable (`A1d`) | 1 | **3** |

**Every published row of the parent's committed transcript has moved.** `out_anchor_132a.txt` and
`out_repair_3f3b.txt` — the 2 it records as `AGREES` — both read `DISPLACED` when the same
instrument is re-run. That is the predecessor's failure shape exactly: a transcript asserting a
green word about a property that has since changed underneath it.

**And it is not the predecessor's failure.** The predecessor's `0 STALE` was stale **and wrong** —
the figures it blessed were red under its own rule once the tree moved. This transcript's rows are
stale **and still correct**: every claim is true of the commit it names, the live re-run exits `0`
with `0 refuted`, and no gate flips. `STALE-AND-RED` and `STALE-AND-GREEN` are different failures,
and producing the second instead of the first **is** answer (2). Reporting them as one would be the
same conflation the parent was filed to fix.

## The primary target: the case the other answer handles

The parent chose **answer (2)**, the measuring commit. Two cases separate the answers, and they fall
opposite ways.

**DISPLACEMENT** — a figure true at its anchor in a tree that has moved on. Answer (1) calls it red;
(2) calls it green. Constructed at `C3a` on both real transcripts: (1) says RED, (2) says
`DISPLACED`. **The deliverable says plainly that it does not catch this** — the README section *"The
price, stated rather than hidden"* opens with the case, and `A1c` says `NOT RED, AND THAT IS THE
DECISION`. Bar met.

**SUBSTITUTION — "anchor shopping"** — a figure that was never true of the tree it was measured at,
carrying a declared anchor pointing at some other commit whose tree does hold it. Constructed at
`C3b` and fed to the parent's own `verdict_from_text()`: it reads **`DISPLACED`, green**. Every
defence passes *by being satisfied* — the sha resolves, the count re-derives from `git ls-tree`, the
digest matches, and the declared count agrees with the published figure so `INCONSISTENT` does not
fire. `A2c` catches a declared anchor whose tree does **not** hold the figure; this is the case where
it **does**.

> Under (1) the examiner is fixed by `git log -1` and the file cannot argue with it.
> Under (2) **the publication step names its own examiner.**

**That transfer of authority is the real price of the decision, and it is unnamed** in a deliverable
otherwise careful to price itself. `C3c` measures the room: 177 distinct populations over 418
commits, and a figure only has to have been true **once, anywhere** for a declared anchor to certify
it forever.

**And the obvious repair does not work** (`C3d`) — requiring the anchor to be an ancestor of the
publishing commit **accepts the shopped anchor and rejects the parent's genuine one**, because the
rebase is precisely what took the genuine one off that line of descent. The two are not
distinguishable from inside the repository. That is the honest form of the finding: substitution is
not a bug in the lattice, it is the residue of moving the examiner into the file.

## Every anchor asserted, not believed (`C2b`)

*"If it records a measuring commit, assert that commit's tree actually yields the figure."* — 2 of 2
declared anchors resolve and their trees yield the published figure, **re-derived by this module's
own `git ls-tree` walk**, its own blob filter and its own sha256 digest. The declared `count=` field
was used as the thing to be refuted, never as the answer. `C4d` compares the two derivations across
45 commits: 0 disagreements. That row licenses every count in this audit — and the arc has already
recorded two copies of `figures()` disagreeing on 3 (`8c55168`).

## What I chose to audit that no list named (`C2c`)

`A2d` sells the digest as the answer to the strongest objection against (2). It demonstrates it on a
**synthetic** transcript, and `A1d` says the two legacy figures cannot use it because they predate
the anchor line. **That leaves exactly one real figure carrying a digest: the parent's own** — the
first case where the remedy can be tested rather than demonstrated, and the rebase has put it in
precisely the state the remedy was built for.

**4 commits in the object store hold the 495-file population the parent was measured against. 0 are
reachable from HEAD.** All 4 sit behind one ref.

> So the digest and the declared sha **are not two independent routes to the tree — they are two
> names for commits that one branch deletion removes together.** `A2i` measures this exposure *for
> the legacy figures* and offers the digest as the answer to it; the parent's own figure now has the
> digest **and** the same exposure.

**And it narrowed while this audit was running** (`C1a''`). The first execution resolved those
commits through the local branch `polecat-132a`; the second **crashed** because that branch had been
deleted between the two runs. The objects survive, on one remaining ref. `A1d`'s forecast — "survives
on whatever side ref still points at it and dies at the next `git gc`" — observed rather than
reasoned about, inside this audit's own runtime.

## Redundancy by independence of failure mode (`C4`)

Three routes — `DECLARED`, `INFERRED`, `RECOVERED` — each broken in turn on a real transcript:

| construction | verdict | route that carried it |
|---|---|---|
| intact | `DISPLACED` | DECLARED |
| sha mangled, digest intact | `DISPLACED` | **RECOVERED** |
| digest mangled, sha intact | `DISPLACED` | **DECLARED** |
| anchor line deleted | `DISPLACED` | **INFERRED** |
| anchor line deleted **and** body hex stripped | **`UNANCHORED`** | none — **fails closed** |

The sha and the digest each survive the other's corruption, so `A2d`'s claimed redundancy is real.
**But they are one line, written by one `print`.** Delete it — a truncated transcript, a crashed
redirect, an edited header — and both die together (`C4b`). The survivor is `INFERRED`, which the
parent itself says "selects for agreement and therefore cannot witness `WRONG WHEN WRITTEN`". Under
that common-mode failure the remaining redundancy **cannot witness the defect the arc exists to
catch**, and the lattice gives `had a declared anchor and lost it` the same label as `never had one`
— evidence of damage and ordinary history, one word.

`C4c` corrupts the transcript **on disk** and confirms the verdict does not move: the working tree is
genuinely ignored, which is load-bearing for the whole `--at` remedy. Bytes restored and verified
byte-identical.

## The vocabulary gap (`C5`)

**There is a word for the merge and it is a verdict, not a sentence** — `DISPLACED`, one of six
rungs, green, defined as *"right when written, moved by a rebase"*. The test was deliberately not
*does the prose say merge*: a word that only lives in a README cannot be returned by a check.

The two defects are separated **by the gate** (`C5b`): one transcript, two anchors differing in
nothing but which tree is named — `DISPLACED` (green) against `WRONG WHEN WRITTEN` (red). The
repaired file carries the vocabulary 5 of 5 (`C5c`), including the rule **imported** from
`anchor_132a` rather than copied.

`C5d` sweeps the old word: **189 occurrences of `stale` across 623 committed `.py`/`.md` files**, 14
qualified by a nearby word naming which defect is meant, 175 bare. The new word was **not**
retrofitted, and that is correct — a deliverable that rewrote 175 sites would have made its own
transcript unreviewable.

## Two defects of this instrument, kept rather than smoothed away

1. **I twice built a checker that could not tell a claim from a mention.** `C2a`'s first draft
   counted `out_audit_7e39.txt`'s `429` as a published figure; it is a **quotation**, inside a
   finding that says that figure is stale. Then `C5c` tested `clause not in src`, **refuted**, and I
   read the refutation as a finding against the parent before checking the site — the clause appears
   exactly once, inside the sentence that retracts it. **Both times the rule I needed was already on
   the page**: this arc's own `S4b`, *"a figure inside a QUOTATION is exempt … it is how a correction
   note states the figure it corrects"*, written in the very file I was testing.
2. **`T1` read all six of its own transcripts from disk and refuted on its own** — which is
   truncated to 0 bytes by the redirect that is writing it. `PREDICTIONS.md` `P9` predicted this
   would happen before it passed. The fix is the parent's: read the self-transcript from git at its
   publishing commit. `anchor_132a.py`'s `verdict_for()` documents this exact hazard and I walked
   into it anyway.

Three predicted exit codes also missed (`C1b`): `--at HEAD`, `--at 1e30484` and `--at cb9f282` were
each predicted **1** and are **0**. The reasoning was that `A3a` asserts its own verdict is `AGREES`;
it does not — it reports whichever verdict fires and stays green while that verdict is green. **The
row was built to survive exactly this and it did.** Kept as written.

## The gap this audit does not close either

`A3c` names it: nothing re-runs the check after a merge, because the rebase is performed by the
refinery *outside* the repository. **This audit inherits it** (`T3`) — these figures are a
measurement at the commit named in each banner, the merge will displace them, and no hook re-runs.
What `C1d` adds is the measurement of how long the gap stayed open in practice: **the parent's `--at`
is the whole remedy it offers for the merge, and it had not been run once between the merge that made
it necessary and this audit.** A remedy whose trigger is a human remembering is the same class of
control as the one that failed.

## Reproduction

Read-only apart from its own six transcripts and one probe. `C4c` writes to `out_anchor_132a.txt` in
the working tree to prove the parent ignores the working tree; it restores in a `finally:` and then
**verifies the restore byte-for-byte**, and the row is red if the restore failed. Exit is `0` when no
control of *this* instrument was refuted — **findings about the parent do not set it**, because an
audit that exited 1 for finding what it was sent to find could not distinguish *the subject has a
defect* from *the auditor is broken*.
