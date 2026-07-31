# mg-19ec — predictions, committed BEFORE any probe of this audit is run

**Work item:** mg-19ec. **Target:** the mg-dffa warrant narrowing (`645b5a4`) of
`docs/OneThird-Branching-Graphs-Where-This-Lives.md` and
`code/branching_repair_41aa/check_doc.py`, landing mg-5800's F1–F4.

This file is committed **before** `code/branching_audit_19ec/` runs for the first time. The
standing rule is *"predict every exit code before running and keep the misses as written."*
Nothing below is edited after the fact; misses are recorded in the deliverable next to the
prediction that missed.

---

## 1. EXIT CODES

Every probe in this directory exits **1** if it finds a defect and **0** if it does not.
`run_all.sh` is green **iff every probe's actual exit code equals the prediction recorded
here** — so a probe that was predicted to fire and does not is a miss the runner reports,
not a silence.

| # | command | predicted exit | why |
|---|---|---|---|
| P1 | `python3 selftest19ec.py` | **0** | my kernel is correct or I have no instrument |
| P2 | `python3 e1_f1_cells.py` | **0** | I expect the two WIDENED cells (B1, B5) to be true and carried by the evidence they name |
| P3 | `python3 e2_f2_clauses.py` | **1** | I expect the two NARROWED clauses to have kept an unbounded population — see §2 |
| P4 | `python3 e3_f4_brown.py` | **0** | I expect Brown `§4.3` to read as reported, and no second example in `§4.3` |
| P5 | `python3 e4_f3_control.py` | **0** | I expect the new `check_doc.py` check to fire in every configuration I can put it in |
| P6 | `python3 e5_population.py` | **1** | I expect the population of the warrant defect in this document to be **larger than four** |
| P7 | `python3 e6_standing.py` | **0** | I expect 0 BROKEN, every figure to reproduce, and the Birkhoff-free converse to survive |
| P8 | `python3 e7_instrument.py` | **1** | I expect mg-dffa's own `w3_brown.py` to exit **0** when it verifies nothing |
| P9 | `./run_all.sh` | **0** | green iff P1–P8 all match |

## 1b. EXIT CODES OF THINGS I DID NOT WRITE (the "do not disturb" re-run)

| # | command | predicted exit |
|---|---|---|
| U1 | `code/branching_warrant_dffa/run_all.sh` | **0** |
| U2 | `python3 code/branching_repair_41aa/check_doc.py` | **0** (31 checks, 0 failed) |
| U3 | `code/branching_audit_5800/run_all.sh` | **0** |
| U4 | `code/branching_repair_41aa/run_all.sh` | **0** |
| U5 | `code/branching_audit_6ad0/run_all.sh` | **0** |
| U6 | `code/branching_af28/run_all.sh` | **0** |
| U7 | `git status --porcelain` restricted to those four directories, after U1–U6 | **empty** — every committed output regenerates byte-identical |

---

## 2. THE SUBSTANTIVE PREDICTIONS, STATED SO THEY CAN MISS

### On the four replacement sentences

* **F1a (B1, widened).** I predict the widened cell is **true**: on the 44 partitions with
  `1 ≤ n ≤ 7` the map `ideal ↦ shape` is a lattice isomorphism, meet and join, **0 bad**,
  and the ordered-pair count **5 464** is `Σ_λ |[∅,λ]|²` over those 44.
* **F1a's sub-claim about `af28`.** The cell says *"T1 in `code/branching_af28/` itself
  tests the **order** isomorphism only."* mg-dffa's evidence for this is a **word count** —
  0 occurrences of `meet` or `join` in T1's body. I predict the stronger reading survives a
  **reading** of T1: no meet or join is computed under any other name either. **If it does
  not, the cell is supported by a proxy and not by what it asserts.**
* **F1b (B5, widened).** I predict `67 / 20 / 87` and `all 87` are what the two cited
  outputs actually print, that mg-6ad0's `Φ` is asserted to be an **algebra** map (without
  which "surjective with nilpotent kernel" does not give the step), and that the cell's
  `LOCATED, not MEASURED` self-description is accurate — mg-dffa re-ran neither.
* **F2a and F2b (narrowed).** I predict **every number reproduces** — 33 / 5 / 28, witness
  `221`, 17 distinct `P`, 5 of them not skew cell posets (2 at `|P| = 5`, 3 at `|P| = 6`),
  30 of 30 on the Young side. **And I predict the narrowing left two populations
  unbounded:**
  1. *"**28 of the 33** finite Young–Fibonacci intervals"* — there are **infinitely many**
     finite intervals `[0̂, w]` in Young–Fibonacci. The population measured is
     `rank(w) ≤ 6`. The bound is in §2 item 2 and in row 10's mg-41aa clause; it is
     **not** in the replacement sentence, whose entire content is now a count.
  2. *"the intervals of Young's lattice are `J(P)` for `P` **exactly** the skew cell
     posets"* — stated with no bound, in the very clause that faults the Young–Fibonacci
     side for naming no class. The document's own ledger row **B2** records that
     *"exactly"* as **measured** to `n ≤ 6`, and mg-5800's own NOT-CLAIMED list includes
     *"that the converse of X1 holds beyond `n = 6`."*
  I predict **both** are real and that the second is the more serious, because it is a
  **new** sentence and it widens in the direction the repair was narrowing.
* **F4 (premise read).** I predict the located text is exactly as reported. I predict the
  document's *"it introduces exactly one example"* rests on a **word count** (one occurrence
  of `example` in `§4.3`), and I predict that when I look for example-introducing
  constructions that do **not** use the word — `consider`, `for instance`, `e.g.`, a second
  `Figure` reference to a different object — I find **none**, so the sentence stands.
* **F3 (control closed).** I predict the new check fires in every configuration I can build,
  including two mg-dffa did not run: a **duplicate** `SKEW8` line, and a mutation of
  `out_young.txt`'s published row rather than of the computed count.

### On whether four is the population

* I predict the population of *"a claim stated with more warrant than its evidence carries"*
  in `docs/OneThird-Branching-Graphs-Where-This-Lives.md` is **strictly greater than four**,
  and that at least one instance is in text mg-dffa **wrote**.
* I will name the population my predicate ranges over rather than printing a bare total.

### On what must not be disturbed

* **0 BROKEN**, every figure reproduces from a disjoint instrument, and the converse of X1
  at `n = 6` **without Birkhoff**. I predict I reproduce the Birkhoff-free converse on my own
  instrument at **107 of 405** — 405 posets on 1..6 elements, 107 skew cell poset classes on
  1..6 cells — with the two sides built from partitions and from order ideals and compared by
  canonical form, and **0 counterexamples in either direction**.

### The thing no list here names, chosen by me

* **mg-dffa's own runner is green in an environment with no network.** `w3_brown.py`
  returns **0** on download failure, `run_all.sh` uses `set -e` with `||` guards keyed on
  exit status, and the final `grep ... || true` cannot fail. So the probe that carries F4 —
  the premise the headline stands on — verifies nothing and reports nothing, and every
  status line downstream stays green. I predict this reproduces, and I predict it is
  **declared** (the docstring and the account's §7 both say the probe exits 0) and therefore
  a **warrant** defect of the same kind as F3 rather than a hidden one.
* Second choice, same probe: **the download is unpinned.** No checksum, no arXiv version.
  I predict I can pin it, and I will publish the digest so the next reader can tell whether
  they read the same bytes.
