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
| **P1** | **REFUTED — 16 sites, not 0**, and refuted by this directory's own subject. §0.1 read a probe's `0` as *"there are none"* when it meant *"this probe could not look"*. Two independent failures: `\b` is **not a word boundary in `git grep`'s POSIX ERE** — it matches nothing and does not complain, which is what produced the literal `0` — and `[^)]*` cannot cross the `)` in `max((len(l) for l in lines), default=0)`, which is how 12 of the 16 are written, so repairing the first alone would have given `3 of 16`. (`z1` §9.) |
| **P2** | **REFUTED on the upper side — 93 sites**, against a predicted ceiling of 40. The class is non-empty, so the directory has a subject; it is 2.3× wider than I allowed. The stated cost did **not** fall due: full adjudication survived, because §5's verdict turned out to be **computable from the operation** for 70 of the 93 and only 23 needed a hand. (`z1` §2, §5, §6.) |
| **P3** | **REFUTED — 61 of 93 (66%)**, against a predicted *strictly fewer than half*. **AND THE CRITERION MOVED, WHICH IS DISCLOSED RATHER THAN LEFT TO BE NOTICED**: the arm judges *invertibility* — is the fallback the operation's own value on the empty input, or a choice? — which is **narrower** than P3's *"is a defect"*. It never asks whether anyone reads the number. Judged against the criterion the arm actually applies. (`z1` §5–6.) |
| **P4** | **HELD, and by more than it asked.** The reconstructed collapse fires (`MAXMIN`, `COLLAPSE`); the shipped spelling is in **no class at all** — out on two independent grounds, guard and fallback — and **which ground does the work is measured**, by substituting on the line read from the tree rather than by argument. (`z0` D1, D2.) |
| **P5** | **HELD, at 1 004 sites — 11× the class a matcher can see.** `sum([]) == 0` is the language's collapse: no fallback in the source, no guard to find, nothing to match on. **This is the prediction that decides the shape of the remedy** and it says the rule cannot be a lint. (`z1` §9.) |
| **P6** | **HELD — 0.** This directory's arms contain no collapsing site. They contain 13 `UNGUARDED_SUM` sites, which §9 says of the other 1 004 are not defects and says of these too. |
| **P7** | **REFUTED — 5.6×, not the ≥10× predicted** (520 loose against 93 strict). The requirement is still load-bearing — it removes 82% of the class, and `z0` D3 shows it is what excludes the exit-code shape rather than some accident — but **the number I named was wrong and the paragraph is not rewritten to fit it.** (`z1` §8.) |

**Four of the seven are refuted, and the one I would keep is P1** — because it is refuted by the exact confusion the ticket exists to describe, inside the pre-registration of the directory measuring it. A tool returned *nothing at all*, *nothing at all* was read as *zero*, and it was published as a measured fact.

**THE LANDING'S HEADLINE FIGURE WAS NOT PREDICTED AT ALL, AND THAT IS SAID HERE RATHER THAN IN THE README.** `z1` §3 — the estate already keeps EMPTY out of the number system in **88.8%** of guarded ternaries and **86.3%** of `default=` aggregates, two disjoint spellings agreeing to one part in forty — rests on a class (`GUARDED_PRESERVING`, `AGGREGATE_DEFAULT_NONE`) that **did not exist when these predictions were written**. It was added after the first census run, when the `default=None` sites turned up beside the `default=0` ones in P1's post-mortem. It is the strongest thing here and it is **not** evidence that anything was predicted well; a figure invented after the measurement is a figure whose exposure was never stated.

**One thing came out differently and is not a prediction:** the verdict was to be entirely by hand, and it is not. Writing the 93 rows made it clear the question — *is the fallback a definition or a choice?* — is decidable from the operation alone for `sum`, `len`, `max`, `min` and division, so those 70 are **computed** and only the 23 remaining are judged. A rule and a judgement in one column would have been indistinguishable, so they are in two.
