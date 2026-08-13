# `code/absent_step_7ae5/` — mg-7ae5's instrument

Deliverable: [`docs/OneThird-AbsentStep-mg-7ae5.md`](../../docs/OneThird-AbsentStep-mg-7ae5.md).
Runtime **11.7 s** on this host, measured by `time sh run_all.sh` and not by addition.

## 1. What this is for

`mg-ac0c` enumerated L1b's downstream, pinned it, and returned **UNDETERMINED because a step
is ABSENT** — row 13, Step 6's threshold `ε₀`. This ticket asks three things about that step
and nothing else: **state it**, **price it**, and **check it against `mg-0e8c`'s density
restatement**, since the ticket suspects it *"may be absent only in the sparse reading"*.

**This directory does NOT re-pin what `mg-ac0c` pinned.** Its 25 rows, its four chains, its
closure sweep and its controls are cited, not redone. What is measured here is one thing
nobody has measured: **the strength of the hypothesis `(T)` carries**, i.e. how much the
*"P has a thin prefix"* clause buys over the bare 1/3–2/3 conjecture. `Op-Form` §7.2 settles
that the class is non-empty and excludes the antichain, from **one** object; it does not
measure the class.

## 2. Files

| file | what it does |
|---|---|
| `PREDICTIONS.md` | committed at `5968f17`, before one line of `lib7ae5.py` existed — with the exposure disclosed: the ticket ordered me to read `mg-ac0c`'s table first, so `R1`–`R4` are REPORTS at zero credit |
| `lib7ae5.py` | `Δ₁`, `Φ`, `p_xy`, `δ`, the density `d`, the ordinal-sum test, `U_either` on both populations, and the closure arithmetic in `mg-0e8c`'s density currency. Written independently of `lib3969.py` **on purpose** — agreement with mg-3969's published numbers is only evidence if the code paths are different |
| `a0_selftest.py` | **§A** definitions against hand-computable objects · **§B** the decomposability identity and the `δ(P⊕Q) = max` lemma, by exhaustion · **§C** **fifteen plug-backs** to values published by mg-3969, mg-d3c7, Op-Form, mg-0e8c, mg-ac0c and **mg-832f** — the last four of which establish that `a2` §D' REPRODUCES mg-832f's finding rather than making one · **§D** four wrong-direction worlds · **§E** the monotone-ceiling detector tested on a population where the answer is known and is NOT monotone |
| `a1_statement.py` | the absent step stated, and the **currency crossings** of the 25-row chain. No poset is enumerated: this is a reading of mg-ac0c §1, with each row's currency-in and currency-out declared so a reader can disagree row by row |
| `a2_price_hypothesis.py` | the price: exhaustive over every poset on `n ≤ 6`, the size of the thin-prefix class on two populations, stratified by `δ(P)`, and then **after minimality** |
| `a3_density.py` | the sparse reading: mg-d3c7's family against the closure requirement at its own density, then the exhaustive `n ≤ 6` failure sweep stratified by a density floor |
| `a4_novelty.py` | seven decisive patterns with every raw hit printed, three non-decisive ones reported as establishing nothing. **The seventh was added mid-run after the first six produced a false NEW**, and the reason is in the source rather than in a commit message: the corpus says *primitive* where I wrote *indecomposable*, and a vocabulary mismatch is how a corpus search manufactures novelty |
| `out_*.txt` | committed output of each, at the commit that added it |

## 3. The controls, and what each is for

`a0` is **GREEN at every control**. Three of them are the ones that matter:

- **§B4 — `δ(P[A] ⊕ P[B]) = max(δ(P[A]), δ(P[B]))`**, exhaustive over all 1 053 ordinal-sum
  splits at `n ≤ 6`. Everything §D' of `a2` concludes rests on it, so it is checked rather
  than asserted: a decomposable frozen poset has a frozen **side**, so **minimality forbids
  it**.
- **§C4 — mg-3969's Claim 6.1 witness reproduced in full**: `|L(P)| = 26`, `Δ₁ = 17/78`, and
  **all four** balanced-in-side pairs landing on `9/13, 19/26, 19/26, 4/13` — the published
  values, verbatim, on independent code.
- **§C11 — mg-832f's audit reproduced on four values**, including the `δ ≤ 1/3` counts
  `3, 6, 9, 21` and the primitive minimum of `δ` at `2/5, 4/11, 5/14`. These are the control
  that keeps `a2` §D' honest: its headline is **mg-832f's**, published before this ticket
  existed, and this instrument reproduces rather than discovers it.
- **§E — the detector for `a3`'s monotone-ceiling claim, run on a synthetic population where
  the ceiling does NOT rise.** It reports the non-monotonicity. Without this, `a3`'s
  monotone result would be a claim about my loop rather than about posets.

**§D1 is a control that came back EXPECTED-EQUAL and is kept as such.** Normalising `Δ₁` by
`max(|A|,|B|)` instead of `min` does not move the `17/78` witness — because that witness has
`|A| = |B|`. The control is blind at its own headline witness, and `D1b` establishes the
blindness is the witness's property and not the control's. A control that cannot fail at the
place it is pointed is worth exactly what it says and no more.

## 4. What this instrument deliberately does NOT do

1. **It re-measures nothing of `mg-ac0c`'s.** The 25 rows, the pins, the four chains and the
   `ε₀` sweep are inputs.
2. **It does not attempt `(T)`.** Naming and pricing is this ticket; proving is not.
3. **It touches no canonical file.** `STATE.md`, `FACTS.md` and `CONCEPTS.md` are
   `pm-onethird`'s; row 8's restatement is `mg-28b6`'s live work and this directory
   coordinates with it rather than duplicating it (mail sent at start of run).
4. **It reads no `.tex`.** The source is not in this repository; L4, Steps 1–6 and the
   definitions are carried on the record of the documents that read it.

## 5. `a4_novelty` is pinned to an as-of commit (`mg-20ee`)

`a4_novelty.py` prints **line numbers into files this instrument does not own** — its corpus is
*every* `.md`/`.tex`/`.html` in the repository. Those addresses are not a property of anything
`mg-7ae5` established; they are offsets into files every other ticket amends. That made
`out_a4_novelty.txt` **non-reproducible by construction**, and it had already gone stale: a
worktree re-run on 2026-08-13 moved 29 lines.

The remedy is `mg-c824`'s, proven on `code/c3_audit_a94c3/a4_census.py`: **pin the bytes, do not
reformat the numbers.** The corpus is read at a declared commit via `git ls-tree`/`git show`
instead of from the working tree, and the transcript opens with an as-of stamp naming that commit
and saying which of its lines are addresses and which are findings.

**`AS_OF = 3fce8b9`, chosen on a measurement.** At that commit the previously-committed
transcript reproduces **byte-identically** — checked before one line of it was edited, which is
step 1 of the numbers-neutrality method passing. The regenerated transcript is `40 +/ 0 -` against
the old one: the stamp is added and **not one existing line moves**.

**The residual cost, stated rather than left to be found.** `3fce8b9` is reachable from
`origin/polecat-p7ae5` — the branch that produced this instrument — but it is **not an ancestor of
`main`**: the refinery rebased the branch and `main` carries the twin `1024bc2`. The two are *not*
interchangeable, and the difference was measured: `1024bc2`'s corpus is 512 files against
`3fce8b9`'s 508, and three raw-hit counts move with it (`15→18`, `16→17`, `49→51`). So `1024bc2`
is recorded as a fallback with its price, not as an equivalent. If `3fce8b9` is ever pruned,
`a4_novelty.py` **exits non-zero with that message** rather than falling back to a live read.

**Both directions were measured, which is the acceptance.**

- *Unchanged corpus*: two consecutive pinned runs are byte-identical, and the committed
  transcript is a fixed point of `run_all.sh`.
- *Changed corpus* (`A4_NOVELTY_AT=HEAD`): 46 lines differ. 16 of them are `raw hits:` counts and
  the remaining 30 are addresses, per-file tallies, or the as-of block. **No classification
  moves** — every `DECISIVE`/`NON-DECISIVE` verdict is identical.

**The raw-hit counts are corpus-valued, and the stamp says so.** This is worth stating because
getting it wrong would be the same error one level up. A count of how much of *the whole
repository* mentions a phrase measures the repository, not `mg-7ae5` — as `a4`'s own closing
paragraph already said ("Every count above is DOCUMENTARY, at this commit, over this file set").
What `a4` concludes — the classifications and the ruling that a grep can show a *phrase* absent
but never a *statement* — is unchanged.

`A4_NOVELTY_AT=WORKTREE` restores the pre-pin behaviour exactly.
