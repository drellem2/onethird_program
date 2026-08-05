# mg-c067 — independent audit of the mg-132a publication-anchor repair

    sh run_all.sh                  # ~90 s, exit 0
    sh run_all.sh --at <rev>       # the same audit as of any commit — RUN THIS AFTER A MERGE

Committed transcripts: `out_c1_rebase.txt` … `out_selftest_c067.txt`. The predictions, **written
and committed before any script in this directory existed**: `PREDICTIONS.md` (`0df8ec7`, an
ancestor of `806533b` which adds the first script — `T4` reads that ordering out of git rather than
asserting it).

> ### ⚠️ Provenance of this file and of the six transcripts beside it (mg-c3a2)
>
> The polecat that ran this audit **died on 2026-07-31 with `README.md`, `c2_anchors.py` and all six
> `out_*.txt` uncommitted.** mg-c3a2 recovered that work. What landed and what did not:
>
> - **`c2_anchors.py` and this `README.md` are the dead polecat's, kept** — they carry the `C2a`
>   de-rating below, they run, and their figures re-derive. What its author *meant* is not
>   recoverable and was not guessed at; they are kept because they are **right**, not because they
>   were found.
> - **The six rescued transcripts were dropped, and re-run rather than trusted.** They were measured
>   at `6e15a1a`, the pre-rebase branch tip, which is **not an ancestor of `main`** — and they were
>   written *before* the `c2_anchors.py` edit rescued alongside them, so they were already a record
>   of a run of a different script. **Every `out_*.txt` here was produced by mg-c3a2's own
>   `sh run_all.sh` at `a053d74`**, aggregate exit `0`.
> - **Re-running moved real numbers**, which is why the rescued ones could not simply be committed
>   either: the population is **528** `.py` files at `a053d74` against 510 at `6e15a1a`, and `C2b'`
>   reads **8 of 8 anchors unreachable** against 2 of 8, because the merge displaced this audit's own
>   six anchors along with the parent's.
>
> **And the transcripts this replaces did not reproduce from the code they were committed with.**
> The six `out_*.txt` merged to `main` are measured at `378cf01` and read `C2b` **`REFUTED`** on all
> six of this instrument's own transcripts, with the population parsed as `4611510` — that is defect
> #3 below. But `4ad011a`, the commit that carries those transcripts, is the commit that **fixed**
> `FIGURE_RE`: running the merged `c2_anchors.py` with `--at 378cf01` today reads `C2b`
> **`CONFIRMED`, 8 of 8**. They are the pre-fix run, committed beside the fix. The rescued
> transcripts were the dead polecat's re-run correcting exactly that, and it died before committing
> them. **Defect #3 is therefore recorded here in prose and is no longer visible in any transcript in
> this directory** — the row it refuted on now confirms, which is what a repaired grammar is supposed
> to do.
>
> The re-run also surfaced defect **#5**, which had been invisible at every commit the original run
> measured.

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
otherwise careful to price itself. `C3c` measures the room: **191 distinct populations over the 460
commits in this object store at `a053d74`**, and a figure only has to have been true **once,
anywhere** for a declared anchor to certify it forever.

**And the obvious repair does not work** (`C3d`) — requiring the anchor to be an ancestor of the
publishing commit **accepts the shopped anchor and rejects the parent's genuine one**, because the
rebase is precisely what took the genuine one off that line of descent. The two are not
distinguishable from inside the repository. That is the honest form of the finding: substitution is
not a bug in the lattice, it is the residue of moving the examiner into the file.

## Every anchor asserted, not believed (`C2b`)

*"If it records a measuring commit, assert that commit's tree actually yields the figure."* — **8 of
8** declared anchors resolve and their trees yield the published figure (the parent's 2 and this
audit's own 6), **re-derived by this module's own `git ls-tree` walk**, its own blob filter and its
own sha256 digest. The declared `count=` field
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

`C5d` sweeps the old word: **233 occurrences of `stale` across 657 committed `.py`/`.md` files at
`a053d74`**, 20 qualified by a nearby word naming which defect is meant, 213 bare. The new word was
**not** retrofitted, and that is correct — a deliverable that rewrote 213 sites would have made its
own transcript unreviewable.

## The one finding that had to be de-rated

`C2a` reports that the parent's `COMPUTED` is a **hand list of 3 against a tree of 4** — the omitted
file is `out_audit_97fb.txt`, and the source comment scopes the list honestly (*"every place in this
arc … for the sweep"*) while the row it feeds drops both qualifiers.

**Its first version said 3 against 10, and that would have been a false finding.** By the time this
audit runs, six of the ten matches are **this audit's own transcripts** — a population inflated by
the instrument's output landing in the set it sweeps, charged against a deliverable written before
any of them existed. The row now cuts at the parent's own last commit (`1e30484`) and charges only
what existed then. **The real gap is one file**, and `C2a''` is why even that is the symptom rather
than the defect: `out_audit_97fb.txt` publishes **7 population figures at 5 distinct commits**, one
anchor per *row* — all 7 re-derive correctly — and `read_anchor()` returns one anchor per *file*.
Adding it to `COMPUTED` would not check it; it would check one seventh of it.

## Five defects of this instrument, kept rather than smoothed away

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
3. **My own figure grammar read the tail of a commit sha as part of the population.** `FIGURE_RE`'s
   inner class was `[\d,\s]`, which crosses a newline — and this audit's own banner puts the anchor
   sha on the line directly above the figure, so `…378cf011b463` + newline + `510 .py files` parsed
   as one figure, `4611510`. **`C2b` refuted on all six of this instrument's own transcripts** and
   that is how it was found: the row asserting *every declared anchor's tree yields its published
   figure* is the row that catches an auditor who cannot read his own figures. The parent's
   `POP_FIGURE` uses literal spaces there and never had the defect. An audit of figure provenance
   whose own grammar mis-parsed a figure is worth recording rather than quietly fixing. ⚠️ **Do not
   go looking for that refutation in `out_c2_anchors.txt`** — the transcripts here are a post-fix run
   and the row confirms; see the provenance box at the top for where the refuting run went.
4. **`C2a`'s first version charged the parent for this instrument's own output.** It read *3 against
   10* where 6 of the 10 were transcripts this audit had just written, against a deliverable
   finished before any of them existed — a finding manufactured by the sweep including the sweeper.
   The section above is the de-rating; it is listed here too because a finding that had to be
   withdrawn is a defect of the instrument and not only a smaller number.
5. **`C2b'` capped its own list at three and did not say so.** The row reads *"each survives only on
   a side ref"* and then printed `unreachable[:3]`. That was written when 2 anchors were unreachable
   and 3 was therefore the whole list; on `main` all 8 are unreachable and the row showed three
   entries, **the same commit repeated**, with nothing marking the cut. **A silent cap under the
   word `each` is the exact defect this arc keeps finding**, and it was invisible until the
   instrument was re-run somewhere its own numbers had moved — which is the audit's own thesis
   turned on itself. Repaired by mg-c3a2: the row now names every distinct commit and states how
   many there are. Found by re-running, not by reading.

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
