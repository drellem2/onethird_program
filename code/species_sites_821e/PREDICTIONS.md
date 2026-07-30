# mg-821e — predictions, written before the probes ran

Every exit code below was written down before the corresponding probe was executed. Three of
them were wrong and all three are **kept as written**, with what actually happened recorded in
`OUTCOMES.md`. A battery whose expectations are written after the run cannot be wrong, and this
arc has said so since mg-6f61.

---

## P1 — depth

The repair makes three walks recursive. A probe is **IN** if the printed extent claims the site,
**OUT** if it does not, **DEL** if it is an IN probe re-run with the recursion removed, and
**GUARD** if it runs `e1_extents.py`, whose exit 1 means *an extent line is false* — the
opposite polarity to a checker's.

| id | dir | mutation | predicted |
|---|---|---|---|
| P0a/b/c | — | unmutated, each of the three | **0** |
| P1 | IN | X4 in `species_7d75/sub/leak.md`, run past `w3_scope.py` | **1** |
| P2 | IN | X3 in the same place, past `s1_extent.py` | **1** |
| P3 | IN | X1 **two** levels down in another tree | **1** |
| P4 | IN | X1 in an **extensionless** file in a subdirectory | **1** |
| P5 | IN | X1 in `sub/PREDICTIONS.md` — `EXCLUDE` is a path, not a basename | **1** |
| P6 | OUT | X1 under `__pycache__` — the one stated directory rule | **0** |
| P7 | OUT | X1 in a subdirectory of a tree `s1_extent.py` disclaims | **0** |
| P8 | OUT | X4 in a subdirectory of a tree `w3_scope.py` does not name | **0** |
| P9 | OUT | X1 appended to a **named exclusion at the root** | **0** |
| P10 | DEL | P1's plant, `w3_scope.py`'s descent line removed | **0** |
| P11 | DEL | P2's plant, `s1_extent.py`'s descent line removed | **0** |
| P12 | GUARD | subdirectory planted, `s1_extent.py` not recursing | **1** |
| P13 | GUARD | subdirectory planted, `w3_scope.py` not recursing | **1** |
| P14 | GUARD | subdirectory planted, everything recursing | **0** |
| P15 | GUARD | `e1_extents.py`'s **own** descent line removed | **1** |

**Why P5.** `EXCLUDE` names five files and the run prints them root-relative. Matching on the
basename would make a printed list mean more than it says, so it matches the path. P5 is the
probe that decides which reading is in the code.

**Why P14 is predicted 0 and matters anyway.** mg-6cb9's Q17e is the same mutation and that
audit scores a `WIDE` row as good only at exit 1. Post-repair nothing is false, so 0 is the
correct answer and Q17e's row will read red against a repaired tree. P12/P13/P15 are what
distinguish *the guard works* from *the guard is absent*.

---

## P2 — sites

`check_doc.py`'s C4. Each row deletes **one** anchor from **one** heading region and leaves every
other copy alone. `HEAD` is `check_doc.py` as committed before this ticket, run against the same
mutated document.

| id | anchor / site | predicted at HEAD | predicted now |
|---|---|---|---|
| S1 | target, front matter (1 copy) | 1 | **1** |
| S2 | `mg-a61f`, front matter (19 copies) | **0** | **1** |
| S3 | instrument, front matter (2 copies) | **0** | **1** |
| S4 | instrument, §11 REPRODUCE | **0** | **1** |
| S5 | `2 of 45`, §2.1 (3 copies) | **0** | **1** |
| S6 | `2 of 45`, §11 REPRODUCE | **0** | **1** |
| S7 | §10's heading (1 copy) | 1 | **1** |
| S8 | an `mg-a61f` copy in §5 — **not** a declared site | — | **0** |
| S9 | a `2 of 45` copy in §8 — **not** a declared site | — | **0** |
| S10 | unrelated prose rewritten | — | **0** |
| every-copy | each anchor deleted everywhere | 1 | **1** |

**The prediction that is the finding.** S2, S3, S4, S5, S6 at HEAD: 0. That is mg-6cb9's F3
restated as an expectation, and if any of them came back 1 the finding would be wrong.

---

## P3 — wiring

| id | what | predicted |
|---|---|---|
| (1) | e2 on the tree as found, and its control (a) firing | exit **0**, control fires |
| (2) | every strike marker deleted from the target document and B1 restored | exit **0**, **0 standing** |
| (3) | at least one strike **exonerated** — restatement is legitimate | > 0 |
| P3b | each of the three runners, unmutated: check's output present | exit **0**, present |
| P3b | the same three, wiring block removed: output absent | exit **0**, absent |
| P3c | B1 restored on disk, runners **wired** | exit **1**, `STANDING UN-STRUCK` |
| P3c | B1 restored on disk, runners **unwired** | exit **0**, green |

**P3c's second row is the historical state**, and predicting 0 is predicting that mg-6cb9's F2
is real: three runners green while B1 stands.

---

## The three that were wrong

Recorded here so they are visible beside the predictions rather than only in `OUTCOMES.md`:

1. **P3a (2) exit 0 — actual 1.** Not the sweep: e2's own control (a). See `OUTCOMES.md` 1.
2. **`unwire` leaving a runnable script.** Predicted implicitly by the first version of P3b's
   `unwired` column, predicted 0, actual 1 — the cut left a dangling `}`. `OUTCOMES.md` 2.
3. **The self-test's `git sees it`.** Predicted to fail when a probe mutates a file; it could
   not, twice over, for two different reasons. `OUTCOMES.md` 3.
