# mg-2ff6 — PREDICTIONS

**ADOPT cfd9c's FROZEN / GROWING / OBSERVED DATED-POPULATION CONVENTION ACROSS
THE ARC'S 27 ARC-WIDE FIGURES AND THE 10 REF-LESS PROSE SITES.**

Committed **before one line of `lib2ff6.py` exists** and before any probe in
`code/grain_axis_audit_03d1/` or `code/grain_arity_9160/` is edited. The base
ref is `5c0849a`; every figure this ticket moves is a figure that reads
`5c0849a`'s value today.

This ticket **MOVES PUBLISHED OUTPUT IN TWO TREES**. cfd9c's `run_all.sh`
checked with `git status` that it moved nothing; mine cannot make that check
and must not pretend to. What replaces it is an **accounting**: every figure
that moves is named, with its published value, its new value, and its class.

---

## H — WHAT I HAVE ALREADY MEASURED BY HAND, DISCLOSED AS MEASUREMENT

An exposure disclosed is not a prediction. These are things I read or ran
**before** writing this file, and no bet below may be scored on them.

| | |
|---|---|
| **H1** | **My ticket body prints the answer to the size question.** `517 -> 832`, `1191 -> 2093`, `400 -> 614`, `370 -> 577`, `79800 -> 188191`, `68596 -> 166682`, `86.0% -> 88.6%`, `246 -> 504`, `626 -> 1283`. Any "does it move" reproduction below is a **FORMALITY** and is scored as one. |
| **H2** | **I ran `s4_convention.py` at `5c0849a` before writing this file.** It prints `0 of 27`, and the per-tree split: `grain_axis_audit_03d1` 18, `grain_arity_9160` 4, `runner_exit_audit_56dc` 1, `runner_exit_repair_70c7` 2, `runner_exit_repair_bf79` 1, `state_relocation_audit_b0ae` 1. So I know the 27 and I know which trees they are in. |
| **H3** | **I listed all 27 flagged rows with their line numbers and values** using S4c's own rule, re-typed into a throw-away script outside the repository. That listing is not committed and is not evidence for anything; it is disclosed because it is how I know where to edit. |
| **H4** | **I read `lib9160.corpus()` and `parent_corpus()` before predicting.** So I know that `mg-9160`'s `400` / `79800` / `11` are computed against a **ref-pinned reconstruction** and not against the disk. P1 below is therefore **NOT** a bet about those three. |
| **H5** | **cfd9c's S2c already enumerates the 10 prose sites**, file and line, in `out_s2_drift.txt`. I did not find them; I read them. |

---

## P — THE BETS

| id | claim | p |
|---|---|---|
| **P1** | **THE TICKET'S OWN HEADLINE FIGURE OF 27 IS AN OVER-COUNT, AND S4c SAYS SO IN ITS OWN TEXT.** At least **4 of the 5** flagged rows outside the two probe trees have a population that is **NOT** the arc-wide corpus — a per-tree census, or a control — so they are collected by a rule about the LABEL and not by a fact about the population. The honest arc-wide count is **≤ 23**. | 0.80 |
| **P2** | **AND THE SCORE AFTER THIS TICKET IS NOT 27 OF 27.** S4c, re-run unmodified, scores **22 of 27** — the 22 in the two trees this ticket is scoped to, and not the 5 it is not. I will not touch the other four trees to make a checker print a rounder number. | 0.70 |
| **P3** | **A MINORITY OF THE 22 ACTUALLY MOVE.** At most **15** of the 22 flagged rows change value between `5c0849a` and the re-run. The rest are FROZEN — their population is a ref or a hand list, and dating them changes their *presentation* and not their *value*. | 0.60 |
| **P4** | **AND THE FROZEN ONES ARE CONCENTRATED IN `mg-9160`.** At least **3 of `mg-9160`'s 4** flagged rows do not move, because their population is `9f1ecaa + eacc5e1` and not the disk. (Licensed by H4 as to *why*; the bet is the count.) | 0.75 |
| **P5** | **`classifying BOTH` STAYS 0** — the ticket's own "arguably not an exception" survives contact with the re-run, and it stays 0 for a structural reason and not a lucky one: `BOTH` needs one string matching `EXEC_WORDS` **and** `SITE_WORDS`, and `grain_nouns` returns single de-pluralised nouns. | 0.85 |
| **P6** | **THE `files` INTERVAL IS EMPTY AT EVERY OBSERVED FIGURE I RENDER**, and at least one other field's interval is **NOT** empty — so the convention is carrying information rather than decoration, checked rather than asserted. | 0.85 |
| **P7** | **RE-RUNNING CONVERGES AT ROUND 2.** Rounds 2 and 3 of the probes I re-run are **byte-identical to each other**, though round 1 is not — because my own tree's transcripts join the corpus between round 1 and round 2, and their SHAPE does not depend on their VALUES (cfd9c's S1). | 0.60 |
| **P8** | **THE PROSE SITES NEED NO RECOMPUTATION AND I WILL NOT DO ONE.** All 10 keep their published value to the digit; what changes is that each gains a ref. Checked by a diff that shows **0** of the 10 published figures altered. | 0.90 |
| **P9** | **THERE IS A CHECK IN THIS ARC THAT CANNOT SEE MY PROSE WORK AND WOULD REPORT `0 dated` AFTER IT.** I name it in advance: cfd9c's **S2c**, whose `noref` is computed over the PATH and whose `0` is a printed literal. I predict it is a literal and not a computation, and that re-running cfd9c unchanged after this ticket still prints `0`. | 0.70 |

---

## E — MY OWN ERRORS, FILED IN ADVANCE

| id | the error |
|---|---|
| **E1** | **I MAKE THE OLDER TREES DEPEND ON THE NEWER ONE.** `a1_axes.py` will `import libfd9c`, which is backwards in time. The alternative is restating `pop`/`render_figure`/`state_of` in two more trees, which is cfd9c's own "a second definition that agrees today is worse than the first". I take the import and record the cost: `code/grain_axis_audit_03d1/` no longer re-runs in a checkout that lacks `code/corpus_fixedpoint_fd9c/`. |
| **E2** | **I RE-RUN ONLY THE PROBES I EDIT, NOT THE SUITES.** `run_all.sh` in `mg-03d1` also runs `a2`–`a5`, and `a4` runs another tree's suite twice. Re-running them would move figures this ticket did not decide to move. So the two trees will be left in a state where some transcripts are from one commit and some from another — which is exactly the condition this convention exists to make readable, committed by the ticket that adopts it. |
| **E3** | **MY OWN TREE JOINS THE CORPUS IT MEASURES.** Every figure I publish here is OBSERVED in cfd9c's sense, and the ref on it is the commit BEFORE the one that publishes it (cfd9c's `at()` says so about itself). I inherit that offset and do not fix it. |
| **E4** | **A REF IS NOT A DISK STATE.** All my re-runs are dated `@5c0849a` because that is HEAD throughout, but they read three different working trees (before my edits, after the probes moved, after my own transcripts landed). The ref is honest about the COMMIT and silent about the DISK. P7's convergence check is the only thing standing between that and a lie. |
| **E5** | **I MIGHT CREATE COUNT ROWS IN PROSE.** `a6_self.py` counts count-row-shaped lines in `mg-03d1`'s three `.md` files and today gets 0, and its exit code includes that number. A prose edit ending in whitespace-then-digits would change another tree's exit code as a side effect of a citation. |
| **E6** | **`27` IS A NUMBER I INHERITED AND P1 SAYS IT IS WRONG — AND I PUT IT IN MY OWN TITLE ANYWAY.** If P1 hits, my ticket title over-counts by the same rule S4c warns about in its own paragraph. I keep the title and score the bet. |
| **E7** | **I CANNOT RUN S4c WITHOUT RUNNING cfd9c's WHOLE PROBE.** The checker is inline in `s4_convention.py` and importing it executes it. I will run it as a **subprocess** and quote its output rather than re-typing the rule — which means my transcript contains another tree's output, and if that tree changes, my transcript is a quotation of something that no longer exists. The alternative was a second copy of the rule, which the ticket forbids by name. |
| **E8** | **I DO NOT RESPECIFY S4c AND I MAY THEREFORE PUBLISH A FAILURE.** If the convention as cfd9c wrote it does not fit `mg-03d1`'s or `mg-9160`'s transcript shapes, the ticket's trap says fix the probe or record the failure. Recording a failure is the outcome I am least likely to reach for and the one I have pre-committed to. |
| **E9** | **THE ACCOUNTING IS A DIFF AND A DIFF HAS TWO SIDES.** I read the "published" side out of `git show 5c0849a:<path>` and the "new" side off the disk. If I edit a transcript by hand at any point, the two sides stop being comparable and nothing in my instrument would notice. |
