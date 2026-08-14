# Predictions — `mg-3c92`, written before any arm of this directory existed

**The subject is the carry-forward `mg-9b6b` filed and `mg-3c92` inherited:** *any arm that can
return "no answer" and "the answer is zero" must print them differently, because conflating them
made a closed route read as open.* That is a proposal about the whole estate. This directory asks
whether the estate exhibits the defect, and — the half that decides whether the proposal can be a
rule rather than a slogan — **whether the collapse is detectable at all.**

**A prediction made after the measurement is worse than none**, so §0 discloses every figure that
was already in front of me when these were written.

---

## §0 — what was already measured when these were written

Three `git grep` probes over `code/**.py` at `3ef7b6a` (my worktree's HEAD during scoping; the arms
re-take everything at the pin `179da0a`), and **nothing else**. No AST was parsed, no arm existed,
and the census figures below were not known:

1. **`max(…, default=…)` / `min(…, default=…)` — 0 occurrences.** `default=` occurs 60 times and
   every one of them is an `argparse` keyword. So the single spelling a linter would reach for
   first is **absent from this corpus**, and P1 is a confirmation rather than a discovery.
2. **`… else 0` occurs in 284 files**, and the frequency table is dominated by two shapes that are
   *not* the defect: `sys.exit(1 if BAD else 0)` (≈150 of them) and matrix indicators
   `(deg[i] if i == j else 0)`. I read that table. I did **not** count what is left after them.
3. **`or 0` — 0 occurrences.** The `xs and max(xs) or 0` idiom is absent.

The population was also taken: **1 249 tracked `.py` files under `code/` at the pin**, 1 121
tracked `out_*.txt` transcripts.

**So P1 is disclosed-not-blind, and P2, P3, P4, P5, P6 and P7 were made blind.**

---

## The predictions

| | prediction | exposure — what a wrong answer would cost |
|---|---|---|
| **P1** | The AST census confirms §0.1: **zero** aggregate calls (`max`, `min`, `next`, `sorted`) carrying a numeric `default=`/fallback argument | Disclosed, not blind. If the AST finds one the grep missed, §0 is wrong about its own probe and every other figure taken by grep in this directory is suspect. |
| **P2** | The **guarded-collapse** class — `f(X) if X else <number>`, where the guard is a bare truthiness test and `X` is named inside the true branch — is **non-empty and small: between 1 and 40 sites** over the 1 249 files | Both ends matter. **Empty** and this directory has no subject and must report *"the corpus does not exhibit the spelling"* rather than a repair. **Hundreds** and no hand adjudication is possible, so §5 becomes a sample and every verdict below it weakens. |
| **P3** | **Most candidate sites are not defects** — the collapsed `0` is either the correct answer or never reaches a transcript. I predict **strictly fewer than half** of the P2 sites survive hand adjudication | This is the false-positive direction and it decides the FORM of the remedy. If most sites are real, the rule can be a lint. If most are false, a lint would train its readers to ignore it, and the rule has to be a *reporting* discipline instead. |
| **P4** | The detector **fires** on the collapsing spelling of `mg-9b6b`'s `G` reconstructed from its own library, and **does not fire** on the spelling that shipped (`mx if mx is not None else "EMPTY"`) | The one demonstrated instance in the estate is the only ground truth there is. A detector that cannot flag it is measuring something else; one that also flags the repair would condemn the fix and make the rule unfollowable. |
| **P5** | The rule is **not enforceable by spelling**, and the corpus proves it rather than the argument: there are **at least 10** sites where an aggregate (`sum`, `len`, a `Fraction` ratio) is taken over a *filtered* comprehension with **no guard at all**, so an empty selection prints `0` with nothing in the source to match on | If the unguarded family is empty, "not enforceable" is theory, the guarded class is the whole story, and a lint would in fact be sufficient. This is the prediction that decides whether the carry-forward can be a mechanical rule. |
| **P6** | This directory's own arms return **0** candidate sites when the detector is run over them | An arm about `EMPTY`-vs-`0` that commits the defect refutes its own rule harder than any census could confirm it. Reflexivity is cheap here and is the first thing a hostile reader would try. |
| **P7** | **Wrong-direction control.** Dropping the *guard-is-named-in-the-true-branch* requirement multiplies the candidate count by **at least 10×** | If the count barely moves, that requirement is decoration, the census is a plain `else 0` grep wearing an AST, and P2's small number is small for a reason I did not measure. |

---

## Outcome, filled in after the run — refuted ones are kept, not edited

*Left empty in the commit that writes the predictions, and in no other.*

| | outcome |
|---|---|
| **P1** | |
| **P2** | |
| **P3** | |
| **P4** | |
| **P5** | |
| **P6** | |
| **P7** | |
