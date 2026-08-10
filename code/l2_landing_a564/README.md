# `l2_landing_a564` — `mg-a564`'s landing check

`mg-a564` landed `mg-3bb9`'s six repairs (A–F) on
`docs/OneThird-L2-Conditionality-mg-28ff.md`. **Four of the six are labelling or citation
repairs**, and this lineage has now produced **three labelling repairs in a row that carried a
labelling defect** — `mg-b58d`'s repair 3 wrote *"40 primitive of 90 drawn"* where the scripts
evaluate `named_posets(7) + sample_posets(7, 90)`, and that is repair E.

So this landing's own labels are not asserted. `a1_landing_check.py` checks them, against the
only two things that can contradict them, plus one sweep by class:

| arm | what it decides | what would make it fail |
|---|---|---|
| **1** | **repair E** — every `n = 7` population figure the document prints, re-measured on **`lib28ff`'s own generators** (not copied from `mg-3bb9`) | any figure differing from `named_posets(7)` 8/5, `sample_posets(7,90)` 90/35, `sample_posets(7,200)` 200/101, unions **98/40** (97 distinct) and **208/106** (207 distinct); or repair 3's defective label surviving anywhere |
| **2** | **repairs A, B, D, F** — every `file:line` the six repairs cite is opened and read | a cited line not containing what it is cited for; in particular `s3_counterfactual.py:60` and `:66,:72` not being the same predicate on the same number, which **is** repair A |
| **3** | **repair C** — a sweep for **blanket universal quantifiers about rows**, the class the defect belongs to | any of the five blanket forms asserted in the document's own voice rather than quoted as replaced wording |
| **4** | **repair B** — P11 scored `LOST` against the bet as filed, the scope restored in every cell whose bet carries it, and §9's summary count agreeing with its table again | the flip's wording surviving; P4's `n ≤ 6` still dropped; the scoring convention living only inside one row |

**Arm 3 is the one that matters methodologically.** `mg-b58d`'s check ran over **figures** and
passed; the defect was a surviving **quantifier over rows**, which no per-figure check can
reach. This arm sweeps the *class*, not a list of known instances — and doing so **found three
further sites nobody had flagged** (§8.1's *"every constant carries `n ≤ 6`"*, §8.1/§10's
*"`17/78` appears nowhere"*, §5's *"every table above is keyed on 4377 and 3340"*), all
re-scoped, none withdrawn.

Every arm carries a **negative control**, because repair A is about a check that could not
fail. Arm 3 carries two, in both directions: the sweep must **fire** on an unscoped blanket and
must **stay silent** on the same words inside a quotation of replaced wording; and the
quoted-span rule is asserted non-vacuous (italic quotations cover **2.9 %** of the document).

## Two defects of my own, both caught by the arms and both kept

* **The first version of arm 3 was the broken thing, not the text.** It accepted a hit if a
  reassuring phrase appeared *nearby* — and it failed on two correctly-quoted hits in this
  landing's own repair notes. A nearby-marker heuristic passes on almost anything and fails
  unpredictably; it was replaced by the precise rule (**the hit must sit inside an
  italic-quoted span `*"…"*`**, the form this document reserves for wording it has replaced).
  **The control was made precise rather than relaxed until it passed**, which is the failure
  mode repair A lands and which would have been very easy to commit here.
* **Arm 3 then failed on a real inconsistency in my own edit.** §5's re-scoping note quoted the
  replaced wording in plain double quotes instead of the document's `*"…"*` convention, so the
  sweep read it as an assertion. **The document was fixed, not the rule.**

## Not done

`a1` does **not** re-derive the exhaustive `n = 7` figures, and says so in its own output.
`0.340719`, `1.018707`, `1.297074`, `168 of 86278` and `96428` rest on **one instrument**
(`mg-51f4`) over a population 21× larger than anything `lib28ff` enumerated; `mg-3bb9` verified
them as **faithful copies** of `code/sweep_loss_51f4/out_s3_n7.txt` — copies, not truths.
**`mg-a91f` carries the independent re-derivation as its first target**; it is not re-filed
here. One expensive computation, two consumers.

Run: `python3 code/l2_landing_a564/a1_landing_check.py` — exit `0` = every arm passed.
Output: `out_a1_landing_check.txt`.
