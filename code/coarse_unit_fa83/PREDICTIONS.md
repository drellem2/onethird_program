# PREDICTIONS — `code/coarse_unit_fa83/`, committed before any arm exists

mg-fa83, the successor carrier for mg-cda7. The claim being tested is mg-cda7's own
carry-forward, stated in its general form:

> **a control defined over a coarser unit than the thing it is guarding is necessary and
> cannot be sufficient** — and the way to find out is to build rules that pass it and are
> wrong, rather than to argue.

mg-cda7 did this once, for one control (the history-walk detector's in/out split, a proxy
over **paths** guarding a decision about **lines**). This directory asks whether the shape is
that control's or the estate's, on the population where a false pass costs something: **the
arms `./build.sh` runs**, i.e. the ones that block a merge.

## §0 What was already known when this file was written

Stated first, because a prediction of something already measured is a record of nothing.

1. mg-cda7's own numbers, quoted and not re-derived: 13 rules, 7 gain, 5 move the OUT column,
   2 pass and are wrong; 816 out-of-family lines over 179 paths; 38 `walk_lines`.
2. `code/state_ratchet_e331/lib_e331.py`'s docstring already says `a word count is a proxy
   for what a reader must read, not the thing itself` (its own E4). The proxy is **declared**.
3. `f0_registry_discipline.py` and `c0_concept_discipline.py` each carry a paragraph headed
   `WHAT THIS ARM DOES NOT DO, said here so its green is not over-read` — presence of a
   field, not truth of it; presence of a pointer, not correctness of it.
4. `code/control_gate_724a/BASELINE.json`'s `twin.mutations_total` says, in its own `why`,
   `a mutation quietly deleted is coverage quietly removed, and it would otherwise be
   invisible: 16 of 16 caught reads exactly like 17 of 17`.

So the estate has **named** this shape at four sites. What no site has is a **witness** — a
tree that passes the control and is wrong. That gap is this directory's whole subject, and
(2)–(4) are why the predictions below are about *which* trees pass, not about whether the
limits exist.

## §1 The predictions

Each is a claim about what a **real arm, run as a subprocess against a mutated tree**, prints.
`WITNESS` = the arm's decision is unmoved and the tree is wrong by a named fine-unit
measurement. `CAUGHT` = the arm's decision moved.

| id | prediction | confidence |
|---|---|---|
| **P1** | STATE.md rewritten so the token *count* is identical and every token is 2 000 characters — bytes ×~250 — leaves `ratchet.py` GREEN. `WITNESS`. | high |
| **P2** | STATE.md with **every non-ledger line's words replaced by filler**, the ledger table and a small hand-named preserved set left byte-identical, leaves **all four** document arms unmoved. `WITNESS`. | **low — this is the one I expect to be refuted first** |
| **P3** | `docs/FACTS.md` entry F1 with its `**SCOPE.**` body replaced by `n/a` leaves `f0` GREEN. `WITNESS`. | high |
| **P4** | `docs/FACTS.md` with one entry deleted and one fabricated entry added — count unmoved — leaves `f0` GREEN. `WITNESS`. | high |
| **P5** | A `docs/CONCEPTS.md` §2 row whose pointer is `mg-0000`, an id no work item has ever had, leaves `c0` GREEN. `WITNESS`. | high |
| **P6** | The P1 recipe applied to `docs/CONCEPTS.md` leaves `c0` GREEN — *the same recipe transfers to an independently written control*. `WITNESS`. | high |
| **P7** | `docs/FACTS.md` F1's `**KIND.**` mark changed `U` → `OPEN` — a proved fact re-graded as open — leaves `f0` GREEN, because §2 checks the mark is **recognised**, not that it is **right**. `WITNESS`. | high |
| **P8** | Every recipe's paired **must-fire** mutation fires on its own target arm. A pair that does not fire means the sandbox is not exercising that arm at all and its witness is worth nothing. | high |
| **P9** | The preserved set P2 needs is **small** — under 20 lines of a 5 199-word document. Its size is the merge gate's real coverage of STATE.md, measured rather than asserted. | low |
| **P10** | **At least one recipe I expect to pass will be CAUGHT.** A witness search that finds a witness everywhere is measuring its own permissiveness, exactly as mg-cda7's `6 of the 13 gain nothing at all` is the base rate its 2 passes are read against. | medium |

## §2 What this directory will NOT do, predicted here so a later reader can check it did not

- **It will not edit another directory's arm.** The witnesses are exhibited and priced; making
  any of them red is a rewrite of somebody else's control, its transcript and, for the two
  suites `control_gate_724a` gates, of `BASELINE.json`. mg-585e's rule: a demonstration that
  is binding by the back door is not a demonstration.
- **It will not touch the real working tree.** Every arm runs against a sandbox. That is
  asserted here so that the arm which checks it (`w0`) is checking a published claim.
- **It will not join `build.sh`.** Its subject is a claim about controls, not a control.

## §2b OUTCOMES — added after the run, with §1 left exactly as it was written

Three of the ten came back other than predicted, and all three are recorded as refuted rather
than reworded. `out_w1_witnesses.txt` and `out_w0_selftest.txt` are the evidence.

| id | outcome |
|---|---|
| **P1** | **HALF REFUTED.** `ratchet.py` is unmoved — `WITNESS` of `e331` — but `03cf` and `602d` both **moved**, because each reads STATE.md for a pointer of its own. So it is a witness of the ratchet and **not** of the gate, which is a distinction P1 did not make and §2 of the arm now prints per recipe. `9bc2` CRASHED, which is reported and **not** counted as a catch. |
| **P2** | **CONFIRMED — the one I expected to fall.** R2b passes all four. R2a, which keeps the ledger *alone*, is **CAUGHT by `03cf`**, so the preserved set is doing real work and §4 reports its size. |
| **P3** | CONFIRMED. |
| **P4** | CONFIRMED. |
| **P5** | CONFIRMED. `POINTER_RE` is `mg-[0-9a-f]{4}`, and `mg-0000` matches it. |
| **P6** | **REFUTED, and it is the most useful line in the run.** `c0` **REFUSES at exit 2** — its section anchors are gone, and its own rule is that *a rename must be LOUD*. The same recipe passes the ratchet and is blocked by the concepts gate, and the difference is one default-deny predicate that already exists one directory over. §3b of the arm and §3 of the README carry it. |
| **P7** | CONFIRMED. |
| **P8** | CONFIRMED — 6 of 6 pairs fired. |
| **P9** | **REFUTED ON ITS NUMBER.** The preserved set is **28** lines, not under 20 — the ledger table alone is 26. The claim it was standing in for survives and is larger than predicted: 3 151 of 5 199 words are outside every fine-unit check. |
| **P10** | CONFIRMED, by P6. One of the seven was caught by its target, and it is the base rate the other six are read against. |

**One prediction was not written down and should have been.** Nothing in §1 predicted that an
arm could reach **no decision at all**. Two worlds do — one by a designed refusal and one by an
uncaught `ValueError` — and the two had to be separated after the fact, because folding a crash
into `caught` credits a control with coverage it does not have. That distinction is in the
shipped classifier (`lib_fa83.run_arm`) and is checked by `w0` D3b.

## §3 The two ways this instrument can be worthless, and the arms that must exist for them

1. **A sandbox that does not exercise the arm.** Every witness ships a paired mutation the arm
   **must** catch (P8), and the base sandbox must reproduce the arm's real verdict.
2. **A "wrongness" nobody can check.** Every recipe carries a *fine-unit measurement* —
   computed by this directory, printed, and independent of the control — so that `wrong` is a
   number and not an adjective.
