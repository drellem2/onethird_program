# mg-5035 — outcomes

Scored against `PREDICTIONS.md`, committed before any script in this directory
existed. **Refuted predictions are kept as written.** Six of thirteen missed,
including the three that mattered most, and the misses are the useful part.

Every figure below is **re-derived by me at HEAD** unless it names another
agent. Where a number is another agent's it says whose and whether I
re-derived it.

---

## THE HEADLINE

`lib7522.figures()` now excludes a git revision, which its comment claimed and
its code never did. The repair is a **DECLARED-revision rule**: a token is
dropped only when it is both revision-**shaped** (7–40 decimal digits) and
**declared** a revision by the line it sits on. It reads text only and never
consults the object database.

* **10 of 10** constructed all-decimal short revisions are now excluded —
  including three that name **no object in this repository**, which is the
  point: a text-only rule excludes a revision that does not exist yet exactly
  like one that does.
* **0 of 8** genuine revision-shaped figures are dropped — `431723379 labelled
  posets` and `2147483647` among them.
* **48 of 86,750** numbers across **18 of 1,535** tracked files stop being
  figures: **0.055%**.
* The dangerous direction is **empty**: the backing corpus loses **1 of 1,494**
  integers and **0** claims in the arc were acquitted by it.
* **Both arc tripwires fired**, proved by re-running their old assertions.

---

## THE TICKET'S FRAMING, CORRECTED

`pm-onethird` asked to be corrected and wrote *"I have not run any of this."*
One correction, and it changes what the job was:

> **The comment does not exist at HEAD.** It died with `lib70c7`'s old body when
> `mg-bf79` landed `675c2ba` — the same commit that reported the finding.

So the ticket's second branch (*"if the comment is the thing that is wrong, fix
THAT"*) had already been taken, by the ticket's own source, without saying so.
What the arc carried was **the defect with the false claim deleted**, which is
worse than either: nothing was left for a reader to disagree with. The choice
between the branches was therefore **forced by a measurement**, which is what the
ticket asked for.

Everything else `pm-onethird` relayed from `mg-bf79` **checks out**: two copies
disagreeing on `3` (now one implementation and one forwarder), `alternatives()`
unified, and the disposition of the 15 shared names read before touching either.

---

## PREDICTIONS, SCORED

| id | prediction | outcome |
|---|---|---|
| **P1a** | excludes **0 of 30** non-resolving tokens; precision 100% | **REFUTED — 4 excluded.** And the adjudication matters: all four are lines that *name* a revision which simply does not exist in this repository — a `REVS = [...]` fixture, `mg-03d1`'s prediction table, and two sentences in `lib7522.py`'s own new comment. Read as revisions by a human the rule is right and **the oracle is wrong on all four**. I adjusted neither; F1c prints every one by file and line. |
| **P1b** | excludes **8–18 of the 20** resolving tokens | **HELD — 10.** |
| **P1c** | **≥ 6** of the misses are bare table columns | **REFUTED — 5.** All 10 misses *are* in `mg-1abe`/`mg-f3ff` census tables, so the shape of the claim held; the discriminator I filed (*no word to the token's left*) counts 5, because in the other 5 the neighbouring column is a hex sha my test reads as a word. Scored as filed. |
| **P2a** | both tripwires go **RED** | **HELD — 2 of 2**, and proved rather than asserted: `f4_self.py`/F4a re-runs the *old* assertions against the repaired rule. Both are re-pointed, not deleted. |
| **P2b** | `lib56dc` left unrepaired as positive control | **HELD**, and checked every run by F4c. |
| **P3a** | **1–12** committed transcripts change | **HELD — 4** (`mg-97fb`, `mg-f922`, `mg-3f3b`, `mg-1abe`). |
| **P3b** | at least one of them in `mg-bf79`'s or `mg-70c7`'s tree | **REFUTED — none.** Their transcripts print `3738079` as a *bare* token beside a filename, which the rule does not reach. F3d says why that is correct there. |
| **P3c** | **0** changed counts in `docs/` | **REFUTED — 2 files, 4 occurrences.** I filed this as *"the most serious result in the ticket if refuted"* and it is refuted, so the qualifier is honoured rather than quietly dropped — with the limit stated: `figures()` never ran over `docs/`, so no published human-facing number is wrong. The supported claim is that one **would** have been. |
| **P4a** | **≥ 1** transcript prints a revision under a figure label; clearest is `out_p2_population.txt` | **HELD — 5 sightings**, and the named one is among them. |
| **P4b** | `mg-70c7`'s E2 count inflated by exactly 1, removed later by a **prose edit** not a fix | **HELD.** `mg-bf79`'s own transcript: *it exits 0 again now, because the prose no longer names an unstable revision.* Re-derived by me: **0** revision-shaped tokens in `mg-70c7`'s README at HEAD. The *"exactly 1"* half is **mg-bf79's**, from its account of a single non-zero run; I did not re-derive it and say so. |
| **P4c** | **≥ 1** published count still inflated at HEAD | **REFUTED — 0**, and I filed it as the one I most expected to be refuted. **None of the 4 moving transcripts publishes a figure COUNT**; each merely *names* a revision. The honest headline is the smaller one: the defect was real, was reported, was left live for a whole ticket, and its published damage is **one uncommitted non-zero exit**. |
| **P5a** | `f2` and `f3` exit **non-zero** | **REFUTED — both exit 0.** I predicted they would count findings; they count only the *dangerous* direction (a false acquittal, a witness the fix misses) and both are empty. The pre-registered codes for `selftest5035`, `f1_rule` and `f4_self` (**0**) held. |
| **P6a** | **≥ 3** defects of this instrument | **HELD — 5**, listed below. |

**7 held, 6 refuted.**

---

## DEFECTS OF THIS INSTRUMENT

Every tree in this arc that reported zero was wrong.

1. **A copula broke the declaration.** `HEAD is 3738079` did not read as a
   revision. Found by `f1_rule.py`/F1a going red on its own tenth row, not by
   review. Fixed by adding `is/was/are/were` as fillers — **which creates a
   residual risk** (`at HEAD is 431723379` would lose a genuine figure), so F1f
   now prints that construction and counts its realised occurrences in the
   corpus: **0**.
2. **This tree contaminated its own census.** Once committed, its transcripts
   are tracked `.txt` files full of declared revisions printed *as evidence*.
   The claim-side delta read **109** instead of **48**, and — worse — the
   backing-corpus loss read **0 of 1,506** instead of **1 of 1,494**, because
   `f2_contamination.py` **prints `478508621408` as the integer it reports
   leaving the corpus, which puts it straight back in.** A census that reports a
   number and thereby changes it. The subject population now excludes this tree
   and the self-count (**55**) is printed beside it.
3. **`f4_self.py` crashed on its own population rule.** It gathered every
   tracked file under this tree rather than every `.py`, and `ast.parse` on
   `run_all.sh` took the probe down *after* F4b had printed — a probe whose
   population rule is looser than what it does with the members, found inside
   the probe that checks for exactly that.
4. **F4d counted selftest case names as count rows.** `^      \.\.\.` matches
   both. It reported **59 of 67** and all 8 "failures" were its own. A count row
   is `B.plain`'s format and **ends in an integer**; that is the discriminator.
   Now **35 of 35**.
5. **The runner's summary grepped its own transcript.** `grep out_*.txt` matches
   `out_run_all.txt`, which already contains every line being grepped because
   each probe is `cat`ed. The summary printed everything **twice**. Caught by
   reading the output, not by a check.

---

## WHAT I DID NOT DO

* **I did not regenerate another tree's committed transcripts.** They are the
  evidence F2 and F3 measure. The 4 that would move are listed by name in F3c.
* **So two transcripts are now knowingly STALE, and a reader will hit them.**
  I edited `selftestbf79.py` and `selftest03d1.py` (the tripwires) and
  `a3_ledger.py`'s A3f prose, and I **re-ran all three to verify they are
  green** — `selftest03d1 TOTAL BAD: 0`, `selftestbf79 TOTAL BAD: 0` — but I
  did **not** commit the regenerated `out_selftest_bf79.txt`,
  `out_selftest_03d1.txt` or `out_a3_ledger.txt`. Their committed bytes still
  show the pre-repair reading, which is a **true measurement at their own
  commit** and the record of when the claim was false. `a3_ledger.py`/A3f now
  says so in the probe itself, so the disagreement is documented at the source
  rather than left for a census to find. This is the `mg-1abe` stale-vs-wrong
  distinction, on purpose: these are **stale, not wrong**.
* **I did not repair `lib56dc.figures`.** It is the positive control.
* **I did not close the bare-table-column gap.** Every candidate rule for it
  keys on layout rather than meaning, and at the one place it matters most —
  `UNBACKED README.md 3738079` in `mg-bf79`'s transcript — firing would rewrite
  the *record of the defect* while repairing the defect.
* **I did not re-derive `mg-bf79`'s `1284 / 31 / 6`.** Those are its numbers over
  its population at its commit. F2d re-derives the same three quantities at HEAD
  in both directions instead of comparing across populations.
* **I did not verify the `docs/` prose against its own sources.** F2c reports
  which `docs/` lines a census *would* have miscounted; whether the surrounding
  claims are right is a different question and is not answered here.
