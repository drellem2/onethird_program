# `code/corpus_universe_1d6c/` — the instrument for mg-1d6c

**What this measures.** A published corpus figure is exactly half its population and a glob is
the reason. Three things the brief names, and two it does not.

1. **What the glob actually matches**, against what it is described as matching — enumerated and
   diffed in both directions, never reasoned about from the pattern.
2. **The full population**, derived by a mechanism that does not share the glob's blind spot, at
   three states and through two parsers.
3. **The consumers** — every published figure that inherits the undercount, found four ways.
4. **The self-check repaired** to the standard it enforces: three fixes, each proved able to fire.
5. **A gate that declares what it cannot reach**, with a size on every excluded class.

```
sh code/corpus_universe_1d6c/run_all.sh      # ~30 s, no network, no deps
```

**`run_all.sh` EXITS 1 AND IS SUPPOSED TO.** Four of its six steps are predicted **1** in
`PREDICTIONS.md` — they exit 1 because what they check is true. **7 of 7 exit values landed on
prediction.**

**The published account is `docs/repair-mg-1d6c-the-universe-and-the-glob.md`.** This file is
about the instrument: what it chose, what it got wrong, and where to attack it.

---

## 1. THE FILES

| file | what it is |
|---|---|
| `PREDICTIONS.md` | 16 predictions, 8 sub-rows and 7 exit values, committed at `c192801` **before any `.py` here existed**, with **nine** hand measurements disclosed as measurements rather than laundered into predictions |
| `lib1d6c.py` | the universe library. Six file-list universes, a prefilter with its soundness argument, and commit materialisation that never touches the working tree |
| `p1_glob.py` | **what the glob matches vs what it is described as matching** — five universes by five mechanisms, diffed both ways, control first |
| `p2_population.py` | **the full population** — three states, two parsers, two grains, and the bill for this ticket's own prose |
| `p3_consumers.py` | **who inherits the undercount** — call sites, transcript figures, prose figures with a control column and a hand adjudication, and the consumer nobody had named |
| `p4_selfcheck.py` | **the self-check repaired** — three fixes, three classifiers side by side, and six controls |
| `p5_declaration.py` | **the gate that declares what it cannot reach** — a total partition of the population and five constructed trees it must fail on |
| `selftest1d6c.py` | 40 cases. U1/U2 are the important ones: they prove the instrument that reported **0** could have reported a positive |
| `out_*.txt` | the committed transcripts of the run in this commit |
| `out_p4_selfcheck_FIRSTFORM_exit1.txt` | `p4`'s **first form**, kept because respecifying its classifier moved a number **towards** my own finding |
| `out_donotdisturb_d075.txt` | mg-d075's suite re-run from this branch, hand-run and restored — green, and two transcripts that do not regenerate |

---

## 2. THE ONE CHOICE THAT MADE A DIFFERENT ANSWER POSSIBLE

mg-aaf4 said it plainly: *"THE UNIVERSE IS THE CHOICE THAT MADE A DIFFERENT ANSWER POSSIBLE.
Adopt that method, not just its number."* So this instrument changes the universe and **nothing
else** — and it goes one step further than mg-aaf4 did:

| | mg-19ec | mg-d075 | mg-aaf4 | mg-1d6c |
|---|---|---|---|---|
| unit | para / cell | para / cell | para / cell | **the parent's, imported and executed** |
| parser | own | re-implemented | re-implemented | **`lib_d075`, imported — there is no parser of mine** |
| universe | one file | one file + `docs/*.md` | a file list | **six file lists, each named, sized and diffed** |

**There is no parser of mine, so a count of mine that differs from the parent's cannot be my
parser.** The cost is that a defect in `lib_d075`'s reader is invisible to me; the compensation
is `p2`'s cross-parser control, which counts the same universe through `lib_aaf4` — a reader
sharing no line with it — and reports **0 rows either sees alone**.

---

## 3. WHAT THIS INSTRUMENT GOT WRONG

**Three defects. Two in `p4`'s scope classifier, found by putting three classifiers side by side
rather than by the self-test; one in the self-test itself, found by the self-test.**

- **It read a PATH as a numeric scope.** `code/branching_audit_19ec` contains digits, because a
  ticket id is four hex characters. H3's rule — *the substring carrying the bound contains a
  digit* — is sound where H3 applies it, to a rank bound, and unsound the moment it is pointed
  at a path.
- **It read an ordinal LABEL as a count.** `10 sentence`, out of *"the row-10 sentence of §3"*.
  **mg-aaf4 respecified for exactly this and wrote the reason at its own point of check; I did
  not read that closely enough before writing mine, and hit the same rock.**

The first form scored **9 of 10**; the second scores **7 of 10** and agrees with mg-aaf4's
independent classifier on **10 of 10 rows**. Both transcripts are committed. **The
respecification moves my count towards my own finding, and saying so is the only thing that
makes the second form worth more than the first.**

**THE THIRD IS A VACUOUS CHECK, AND IT IS THIS ARC'S OWN DEFECT ARRIVING IN MY SELF-TEST.**
`M3` claims to test that materialising a blob out of a commit leaves the working tree alone. Its
first form asserted that `git status --porcelain` mentioned nothing outside this instrument's own
directory — **a global property standing in for a local one.** It passed twice, and it failed the
instant this ticket added a file to `docs/`, which has nothing whatever to do with materialising.
**A check that passes because the rest of the world happens to be quiet is not a check**; the
form that shipped takes the status before and after and compares them, and `M4` additionally
asserts the blob landed outside the repository at all. The first form's transcript is committed
as `out_selftest1d6c_FIRSTFORM_exit1.txt`.

**`PREDICTIONS.md` P13 therefore HOLDS, and it held later than I expected.** It predicted the
self-test would find ≥ 1 defect of this instrument. For two runs it found **0** — and it found 0
*for the same reason M3 was broken*: nothing had yet disturbed the part of the world M3 was
accidentally reading. The two classifier defects were found somewhere else entirely, by the
three-column comparison in `p4`.

---

## 4. THE NEGATIVE THAT NEEDED AN INSTRUMENT

`p1` reports that the glob's **non-recursion costs zero sites**: the 12 tracked files under
`docs/state-history/` state the figure nowhere. **A zero from a probe nobody has seen fire is
not a finding.** `selftest1d6c.py` U1 and U2 build a tree in which a subdirectory file *does*
hold a site, run the same two functions over it, and assert that the glob returns 1 file and 1
site while the walk returns 2 and 2. **U4 does the same for the tracked/worktree hole**, which
is also empty at this commit.

Every other check here is held to the same rule: `p4`'s six controls, `p5`'s five constructed
trees, `p1`'s empty-diff control, `p3`'s 141-occurrence breadth control and its 18-row control
column.

---

## 5. FOR WHOEVER AUDITS ME

- **`MY_NUMERIC` is a choice and it was respecified once**, in the direction of my own finding.
  Both transcripts are committed. **If it looks like a classifier tuned to a result, say so** —
  and note that its agreement with mg-aaf4's is evidence of convergence, not of independence,
  since I read mg-aaf4's source before writing the second form.
- **`p3`'s five adjudication rows are mine.** I could have published the machine's 12. The
  reasons are at the point of the check and printed per row; **argue with them there.**
- **`p5`'s four classes are a taxonomy I invented.** A file whose path matches no rule fails the
  gate, which is the safety property — but the *rules themselves* encode a judgement about which
  invariants outrank bounding. If PRE-REGISTRATION should not be exempt, that is an argument
  against this gate's design, not a bug in it, and it would move **10** sites.
- **The prefilter is a superset argument, not a measurement.** `p1`'s 1.8 checks it on one
  universe only. A file whose site survives the parser but whose raw text carries neither `33`
  nor a naming string would be invisible to every count here, and I have not proved none exists.
- **STATE C is not stable.** It includes my own prose, so it moves with my next commit. Any
  reader re-running this suite after this commit should expect STATE A and B to be fixed and
  STATE C to have drifted — and if it has not, that is worth a question.
