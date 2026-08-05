# mg-6e58 — PREDICTIONS

**Committed before any script of this instrument exists.** Nothing below is
edited after a run. Where a run disagrees, the row keeps its original wording
and the disagreement is recorded beside it in `README.md`.

The ticket: `lib330a._HASH_FORMATS` is
`("--format=%H", "--pretty=%H", "--format=format:%H")`, and `--format=%h`
— **lowercase** — is not in it. mg-0ba7 measured 44→59 call sites and 1→4
`UNRESTRICTED` **at its own tree**. Every figure in this file is at **my**
tree (`polecat-z6e58`, parent `9643a5e`), which is a different tree, so my
numbers are not comparable to mg-0ba7's and I do not predict its numbers.

---

## DISCLOSURE FIRST — WHAT I HAD ALREADY MEASURED WHEN I WROTE THIS

Pre-registration is worthless if it launders a measurement as a forecast.
Before writing this file I ran two throwaway commands in the shell, and their
answers are in rows **D-1**–**D-3**. Those rows are **not predictions**; they
are measurements already taken, restated so that the scripts can be checked
against them.

| id | already measured, not predicted |
|---|---|
| **D-1** | mg-330a's own classifier at my tree: `ALL 45` — `OLDEST 12`, `INDEXED 12`, `NEWEST 9`, `PICKAXE 6`, `RANGE 4`, `UNRESTRICTED 2`, 0 unparsed. Population: every `ast.Call` in every `*.py` under `code/`. Grain: call sites. |
| **D-2** | The literal string `--format=%h` occurs in **15** `git log` calls at my tree. |
| **D-3** | Format strings that **contain** `%H` or `%h` without **being** one of the four literals exist at my tree: `--format=%H\t%s`, `--format=%H %s`, `--format=%H%x1f%s`, `--format=%H%x1e%B%x1f`, `--format=%H%x1f%s%x1f%B%x1e`, `--format=%h %s`, `--format=%h %ad %s`, plus `--oneline`. |

D-3 is the reason this ticket is not a one-line tuple edit, and I knew it
before I predicted anything. **Everything below is genuinely open at the time
of writing.**

---

## THE ENUMERATION (P1) — WHAT GIT'S OWN DOCUMENTATION SAYS

The brief forbids enumerating the flags I happen to recall. The population I
will read is `man git-log` on this machine (git 2.50.1, Apple Git-155),
parsed, not remembered.

| id | prediction |
|---|---|
| **P1-a** | The placeholders whose documented description is a **commit** hash are exactly two: `%H` (`commit hash`) and `%h` (`abbreviated commit hash`). No third. |
| **P1-b** | `%T`/`%t` (tree) and `%P`/`%p` (parent) will also match a naive "hash" grep, and my extractor must **exclude** them. If it does not, it over-collects and I will say so. |
| **P1-c** | The built-in `--pretty=<name>` formats documented as printing a commit identifier number **at least 7**: `oneline`, `short`, `medium`, `full`, `fuller`, `reference`, `raw`. |
| **P1-d** | My extractor will **MISS `mboxrd`**, because its documentation says only "like email" and contains no literal hash line of its own. I predict this against myself and will keep it. |
| **P1-e** | `--oneline`, `--abbrev-commit` and `--no-abbrev-commit` are all three documented on `git-log(1)` and all three change whether/how a commit identifier is printed. |
| **P1-f** | The documented default when no `--format`/`--pretty` is given is `medium`, which prints `commit <hash>` — so a bare `git log` **is** revision-producing, and mg-330a's classifier calls it `None`. |

## THE POPULATIONS (P2) — FOUR NESTED DENOMINATORS AT ONE TREE

- **POP-A** = mg-330a's `_HASH_FORMATS`, verbatim (3 literals, exact match).
- **POP-B** = POP-A + the literal `--format=%h`. *This is the one-line repair
  the brief forbids;* I measure it so the cost of stopping there is a number.
- **POP-C** = doc-derived: any `--format=`/`--pretty=` **value containing** a
  `%H`/`%h` placeholder (`%%` honoured as an escape), plus the built-in format
  names of P1-c, plus `--oneline`.
- **POP-D** = POP-C + `git log` calls with **no** format argument at all
  (P1-f's default `medium`).

| id | prediction | grain |
|---|---|---|
| **P2-a** | POP-B `ALL` = **60** (D-1's 45 + D-2's 15), i.e. no call carries both `--format=%H` and `--format=%h`. | call sites |
| **P2-b** | POP-C `ALL` = **87**. | call sites |
| **P2-c** | POP-C − POP-B ≥ **20**, and **at least 15 of that increment are `%H` — FULL-hash — sites**. If so, the omission was **never only about case**, and adding `%h` to the tuple would leave more sites hidden than it recovers. | call sites |
| **P2-d** | POP-D − POP-C = **4**. | call sites |
| **P2-e** | Every kind count except `RANGE` grows from POP-A to POP-C. | per-kind |
| **P2-f** | `PICKAXE` grows too, i.e. there is at least one `git log -S/-G` with a lowercase or composite format. **Low confidence.** | per-kind |

## THE STILL-OPEN LIST (P3)

`code/repair_b2af/README.md` says `p3_reason.py` is "**the one site** in the
19" that is `UNRESTRICTED`.

| id | prediction |
|---|---|
| **P3-a** | At my tree, under mg-330a's **own** classifier, `UNRESTRICTED` is already **2**, not 1 (D-1). So the sentence is false even without this ticket's finding. |
| **P3-b** | Under POP-C, `UNRESTRICTED` ≥ **4**. |
| **P3-c** | At least one of the additional `UNRESTRICTED` sites is in a directory that did not exist when mg-b2af wrote the sentence, so the sentence was **true when written and is false now** — a staleness, on top of the blindness. **Genuinely open; I have not looked.** |

## F-A — THE GATE THAT CANNOT SEE AN ABSORPTION (P4)

`t1_population.py:430` gates on `not [r for r in pinned if r["kind"] ==
"OLDEST"]`, where `pinned` is `ANCHORS.tsv`.

| id | prediction |
|---|---|
| **P4-a** | `ANCHORS.tsv` carries **0** `OLDEST` rows and its four rows' kinds are drawn from `HISTORY_KINDS`, which excludes `OLDEST` by construction. The gate's input **cannot** contain the value it tests for. |
| **P4-b** | In a clone with `--reverse` deleted from one `OLDEST` site, the `OLDEST` count drops by exactly 1 and the absorbed site reappears in a **history-derived** kind — the population grows by absorbing a class that does not have the defect. |
| **P4-c** | Evaluated on that clone, the gate predicate at `t1_population.py:430` is still **True** (silent). |
| **P4-d** | A gate that compares the tree's `OLDEST` count against a recorded expectation **does** fire on the same clone. |

## AGAINST MYSELF (P5)

| id | prediction |
|---|---|
| **P5-a** | My selftest exits 1 on its first complete run, on something I did not foresee. |
| **P5-b** | A **case-blind** search (`grep -i '%h'`) at my tree returns a count that is neither POP-A's nor POP-C's, and would report "found them all" — the exact blindness under repair. I will construct a positive control with **both** `%H` and `%h` on separate constructed lines and show my detector separates them and a case-blind one does not. |
| **P5-c** | The closure test — "the documented hash-emitting spellings are exactly the ones this instrument handles" — will go **red** if a fifth spelling is added. I will show it red by adding one to a **constructed** doc string, not by editing git. |
| **P5-d** | This file's commit SHA will be **displaced** by the refinery rebase. `git patch-id --stable` will match on `main`; `merge-base --is-ancestor` will give a false negative. Recorded in advance, not discovered afterwards. |
| **P5-e** | I will **not** re-run mg-330a's or mg-b2af's suites and will not regenerate their transcripts. Their committed figures stay as they are; my correction is published beside them, not over them. |

## WHAT I AM NOT DOING, STATED IN ADVANCE

- I am **not** editing `lib330a._HASH_FORMATS`. mg-330a's transcripts are
  evidence of a run; silently widening the constant behind them would make
  every committed figure in that directory unreproducible while still looking
  reproducible. The corrected classifier lives here, is written from git's
  documentation rather than imported, and is compared against mg-330a's.
- I am **not** re-running or rewriting `docs/audit-mg-330a-the-anchor-and-the-term.md`.
  Its `36` and its `16 across 13 directories` are stated in a **merged**
  commit; this instrument names them as consumers and publishes the corrected
  figures. It does not rewrite another ticket's merged document.
- I have run **none** of mg-0ba7's code and have not seen it. Every claim I
  attribute to mg-0ba7 comes from the ticket body written by pm-onethird.
