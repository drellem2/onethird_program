# `label_vs_computation_68ef` — is a label-vs-computation check buildable?

`mg-68ef` carries `mg-9d9e`'s remainder. That branch corrected two of its own prose defects **by
re-reading rather than by a control**, and named the class:

> A mislabelled column that prints the right number is the defect this corpus keeps finding one
> estate over.

The carry-forward asks whether a **label-vs-computation** check is buildable — comparing what a
header claims against what the arm beneath it computes — **or whether this class is irreducibly a
reading problem, in which case saying so is itself the deliverable.**

`AS_OF = 5ffb22e`. Every figure is a function of that commit except `m1.6`, the reflexive scan,
which must read the worktree because this directory is younger than the pin — **an exemption by
arithmetic and not by rule**, declared at the section. The two exhibits are read out of the tree at
`3561300` (`p9d9e`'s own commit) and at `AS_OF`, and are never re-typed (`mg-d2c2`).

## The answer

**Both. A check is buildable, it works, and it cannot reach either of the two defects the ticket
was filed from.**

- The check is real: it segments a table, pairs each column to the expression that fills it, and
  compares the numeric literals the label names against the literals the computation spells. `m0`
  D1 and D2 plant a mislabelled column and it is caught, in a fixture and in the real exhibit file.
- Over **1 252** tracked `.py` it adjudicates **4** column labels and returns **0** real
  disagreements. Its only firing is a **false positive** — a heading whose padding before a
  parenthesis reads as a juxtaposed product — adjudicated by hand in `m1.3` and not matched away.
- **Neither exhibit is in its class.** Exhibit B's *column header was never wrong*: it reads
  `note's ceiling 0.9399(a+b)` at both revisions and agrees with `0.9399 * size * k` at both. The
  correction moved a **prose note** four lines above the table. Exhibit A is an `O(...)` claim in a
  docstring, and nothing syntactic reaches it.

So the ticket's own sentence names a shape that **is** checkable, and what it was written about is
two shapes that are not. That is the finding, and it is the carry-forward's second option arriving
with a reason rather than a shrug.

## The funnel — where the reach is actually lost

| stage | count |
|---|---|
| tables (a rule line with a header above it) | 65 in 25 files |
| … paired to a `%`-format row template of matching arity | 25 |
| column labels in paired tables | 128 |
| … formula-shaped | 20 |
| … … adjudicable (the label names a numeric literal) | 4 |
| … … … DISAGREE | 1, and it is a false positive |

Two losses dominate, and they are different in kind. **65 → 25** is *pairing*: most tables print
their rows some way other than one `%`-tuple whose arity matches the header. **20 → 4** is
*adjudicability*: `a+b`, `log2 n!`, `E/(n log₂ n)` are formulas in **symbols**, and the symbols are
not the arm's variable names — `a+b` labels a column filled by `size`. Deciding those needs a
reader who knows what the symbols mean, which is the same reader the ticket says found both
defects.

`NOT ADJUDICABLE` is a verdict here and not a pass. 16 of the 20 paired formula labels are in it.

## Why the obvious implementation is wrong, measured on the exhibit itself

The estate's own exhibit defeats the naive splitter. Its header is

```
     n | node size a+b | H(word | earlier) | note's ceiling 0.9399(a+b) | overpay
```

— a column label **containing the delimiter**. Splitting on `|` gives 6 fields against the row
template's 5 placeholders, so the table goes unpaired and the check is blind exactly where the
class was found (`m0` D5). The disambiguator is the `---+---` rule line, a convention this estate
already writes.

And the rule line is not byte-aligned with its header everywhere: **8 of 65** tables need a
one-character shift, in the source *and* in the committed transcript. A segmenter taking the `+`
columns literally mis-segments them **without complaining** (`m0` D4).

## The other half — `O(...)` claims

43 claims in 30 files; 33 are polynomial nesting claims that can be ranked at all. The only proxy a
matcher has is syntactic loop-nesting depth, and it equals the claimed rank in **11 of 33**.

On the one claim this estate is *known* to have got wrong it is worse than useless: `feasible_merges`
has loop depth **1** against a wrong claim of **2** and a right claim of **3** — so a lint reading
*the body has fewer loops than the docstring claims* would treat `O(a*b)` as conservative and
**license** it. The two dimensions of that DP live in the memo key, not in any `for`.

⚠️ Disagreement in that column is **not an accusation** and no arm here uses it as one. A `for` loop
over a constant-size list is not a dimension and a memoised recursion has dimensions in no loop at
all. What the column measures is that the proxy and the claim are measuring different things.

## The arms

| arm | what it is |
|---|---|
| `m0_selftest.py` | ten worlds: six plants CAUGHT, three REQUIRED-INERT, one that DOES NOT BIND HERE and says so |
| `m1_reach.py` | the funnel, the sweep, the hand verdict, the `O(...)` population, the reflexive scan |
| `m2_exhibits.py` | the two exhibits read at both revisions; P6's refutation |

`m0` runs **first**, because `m1`'s headline is a zero and a zero is what a narrowed class, a broken
segmenter or a matcher that never fires returns for free.

## Three defects found in this instrument, and what they cost

1. **The population depended on the working directory.** `git ls-tree -r --name-only <rev>` run from
   a subdirectory lists only that subtree, so the corpus fell from 1 252 files to this directory's
   own three the moment `run_all.sh` did its `cd`. Caught by `m1.3`'s refusal — the hand table named
   a site the matcher no longer found — and fixed by anchoring every git call to `ROOT` and walking
   `--full-tree`. **This is the exact failure `m1.0` exists to catch, arriving inside the instrument
   that prints `m1.0`.**
2. **D3 asserted a guard was load-bearing and it is not.** Two drafts. `NUMLIT`'s identifier guard
   does what it claims at the unit level — without it `log2 n!` contributes a literal `2` — and
   moves the corpus figure **not at all**, because such labels carry no operator and are excluded a
   stage earlier. Recorded as `does not bind here` rather than claimed as a pass.
3. **The matcher's only corpus hit is its own false positive**, and the tighter spelling that
   removes it was written *after* seeing it. Both spellings ship and both counts are printed, so the
   reader sees what the repair costs instead of being handed the number the tighter rule gives.

## What this directory does not do

- **It repairs nothing.** The one flagged site is a false positive and belongs to
  `code/pairbias_audit_a832f` regardless.
- **It is not in `build.sh`**, and the reason is not cost (~47 s). Nothing here is a property the
  estate must hold: the subject is a question put to `pm-onethird`, and a measurement that gates is
  one its subjects learn to spell around.
- **It proposes no lint.** On the evidence above a lint would adjudicate 4 labels in 1 252 files and
  be silent on both exhibits. What is worth having is the *reporting discipline* the ticket already
  practises: a formula in a header is a claim, and the only instrument that checks it is a reader.
- `STATE.md` untouched, so the ratchet is untouched and no twin re-pin is owed. `docs/FACTS.md` gets
  no entry (`mg-3da1`'s homelessness test — every measurement here is consumed by this landing) and
  `docs/CONCEPTS.md` no row.

## Reproducing

```sh
sh code/label_vs_computation_68ef/run_all.sh      # ~47 s, exit 0
```

No clock and no randomness anywhere in the suite, so two consecutive runs are byte-identical on all
three transcripts.
