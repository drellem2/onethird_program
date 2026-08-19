# mg-06d1 — CASHING THE TWELVE CONTROLS

`code/alias_index_0d1b/INDEX.md` records **11 quantities aliased across up to 13 names in
up to 11 trees, with ZERO disagreements in 12 measured groups.** mg-0d1b built that index
and named the consequence itself:

> the hazard is SILENCE, not error. Twelve independent instruments compute the same twelve
> quantities and nothing has ever compared them. EVERY ROW IS A CONTROL THE ARC HAS ALREADY
> PAID FOR AND HAS NEVER CASHED.

This directory cashes them. It adds **no mathematics** — every scalar is still computed by
the tree that owns it, through that tree's own entry point, via `lib0d1b`'s adapters, which
this suite *imports* rather than reimplements. What is new is the comparison, and the fact
that it now runs on **every merge**, on `./build.sh`.

Nothing is renamed. Every name below is spelled the way its own tree spells it.

---

## §1 THE RUNTIME, MEASURED BEFORE IT WAS CHOSEN

The ticket's step 3: *"MEASURE THE RUNTIME FIRST and report it… Do not assume it is cheap
because the index was."* It is not cheap. Recomputing twelve trees over mg-0d1b's 306
primitive posets, on this host:

| tree | n=3 | n=4 | n=5 | total |
|---|---|---|---|---|
| `l2_conditionality_28ff` | 0.03 | 0.66 | 16.36 | **17.05 s** |
| `l2_audit_29fe` | 0.01 | 0.31 | 10.32 | **10.64 s** |
| `chain_iv_c_81ff` | 0.00 | 0.02 | 0.48 | 0.51 s |
| `lstar_789d` | 0.00 | 0.01 | 0.35 | 0.37 s |
| `l2_underclaim_audit_3bb9` | 0.00 | 0.01 | 0.34 | 0.36 s |
| `eleak_repair_8311` | 0.00 | 0.01 | 0.33 | 0.34 s |
| `anticorrelation_c50b` | 0.00 | 0.01 | 0.24 | 0.25 s |
| `audit_5cba` | 0.00 | 0.01 | 0.23 | 0.24 s |
| `sweep_loss_51f4` | 0.00 | 0.01 | 0.18 | 0.19 s |
| `direct_prefix_audit_2de0` | 0.00 | 0.00 | 0.11 | 0.12 s |
| `c3_prefix_capture_76b2` | 0.00 | 0.00 | 0.09 | 0.10 s |
| `c3_audit_a94c3` | 0.00 | 0.00 | 0.07 | 0.07 s |
| **all twelve** | 0.05 | 1.07 | 29.1 | **30.2 s** |

Two trees are **92 % of the cost** and n=5 is **96 %** of it. The predicate arm (g2) is
**0.18 s** — free, and it has been free the entire time nobody ran it.

**The measured effect on the gate**, both numbers taken with `time sh build.sh` on this
host:

| | before | after |
|---|---|---|
| `./build.sh` | **12.96 s** | **44.8 s** |

**mg-479c re-measured this on the same host** and added to it: g3 is **0.03 s** (it does no
recompute at all) and g1's six added arms **0.1 s**, because they reuse the same captured
matrix the W arms do. This suite ran **31.0 s** before mg-479c and **30.2 s** after, in one
session — the addition is below this host's run-to-run variance. `./build.sh` measured
**42.8 s** and **44.5 s** on two runs against the **44.8 s** recorded above; both samples are
quoted rather than the better one. See §7.

### What was gated, and the subsets that were costed and rejected

**GATED: all 12 groups, all 71 names, all 12 trees, the full 306-poset POP-PRIM.** The two
alternatives the ticket invites were both measured first:

* **Drop the two slow trees** (`l2_conditionality_28ff`, `l2_audit_29fe`) → **2.5 s**, a
  12× saving, and every one of the twelve groups survives with ≥3 names. **Rejected:** a
  tree dropped from the gate is a *permanent blind spot* — an edit to `lib28ff.py`, one of
  the most-cited libraries in the corpus, becomes structurally invisible to this check.
  A poset dropped is a smaller sample; a tree dropped is a hole with a name.
* **Keep all twelve trees on a reduced population** (n≤4 plus a strided n=5) → ~6 s at
  stride 6. **Rejected on the ticket's own instruction:** mg-0d1b's tolerances are the
  *observed max spread over POP-PRIM at 306 posets*. Over any subset the observed spread is
  ≤ that, so carrying the recorded tolerance onto a subset makes it **looser than the
  observed agreement — decorative, by the ticket's definition.** Running the subset honestly
  would mean re-measuring twelve tolerances, i.e. inventing new ones, which step 2 forbids.
  The tolerances and the population are one object and were kept together.

So **nothing is scheduled and nothing is deferred**; the whole check is on the gate.
44.8 s sits against `.pogo/refinery.toml`'s **20-minute** timeout (27× headroom) and against
the fleet's observed median 2m30s of duplicate gate work (mg-da30). mg-724a accepted 16 s
after the same argument; this is the same argument with a bigger number and it is stated
here rather than left for whoever next wonders why merges got slower.

---

## §2 THE ONE DESIGN DECISION — PINNED MEMBERSHIP

`x3_values.py` forms alias groups **from the values** and reads the names afterwards. That
is the right instrument for *discovery* and the wrong one for a *gate*, because its failure
mode is silence in exactly the case the gate exists for:

> if `chain_iv_c_81ff:lambda2_bracket` stopped agreeing with the other eight `gamma` names,
> x3's clustering would put it in its own cluster, print "8 names in 8 trees" instead of
> nine, and **exit 0**.

A group that quietly loses a member *is* the defect, not the report of it. So the gate pins
membership from `BASELINE.json` — mg-0d1b's own machine output, frozen — and asks only
whether the pinned members still agree.

**This is demonstrated, not asserted.** Arm **W4** plants a column drifted a whole unit out
of the `gamma` group and reports what mg-0d1b's own value-blind rule does with the *same*
input:

```
CAUGHT  W4 column DRIFTS OUT of `gamma` entirely (+1.0 at every poset)
        value-blind clustering on the SAME input: gamma cluster 9 -> 8 names,
        drifted column alone in its own cluster: True, NO error raised — that rule exits 0 here
```

Four things go RED, and only the first is a "disagreement" in the everyday sense — the
other three are the shapes silence actually takes: `DISAGREE`, `MEMBERSHIP-LOST`,
`TREE-BROKEN`, `COMPARABILITY` (a name still produced but comparable at a different number
of posets than when the tolerance was measured — `spread()` *skips* None/NaN/inf, so a
column decaying toward all-None would otherwise agree with everything over an ever-smaller
set).

---

## §3 THE TOLERANCES ARE CARRIED, NOT INVENTED

Every tolerance is **read out of `code/alias_index_0d1b/alias_groups.json`** — x3's own
machine output, the same file `x2_index.py` builds INDEX.md from — by `mkbaseline.py`, and
never retyped. The labels are likewise *parsed* out of `x2_index.py`'s `LABELS` table.

This is not a hypothetical risk. **The ticket body itself quotes the tolerances rounded** —
"4.7e-10 / 9.1e-13 / 7.3e-12 / 1.1e-07" — where the record says 4.665708e-10 / 9.097167e-13
/ 7.310375e-12 / 1.107879e-07. A gate built from the ticket's own quote would be looser than
the observed agreement. Arm **W8** measures exactly that: W2's mutation re-checked at a
plausible typed `1e-6` **passes**.

Seven of the twelve rows are pinned at **0.000e+00 — exact equality.**

| row | names | trees | tolerance |
|---|---|---|---|
| `leak(A_1)` | 13 | 11 | 0.000e+00 |
| `gamma` | 9 | 9 | 4.665708e-10 |
| `Delta_P` | 7 | 7 | 0.000e+00 |
| `Phi*_pref` | 7 | 7 | 0.000e+00 |
| `mu_pref` | 7 | 7 | 9.097167e-13 |
| `rho*Delta_P` | 6 | 6 | 7.310375e-12 |
| `Phi*_all` | 6 | 5 | 0.000e+00 |
| `E_footrule` | 4 | 4 | 0.000e+00 |
| `M` | 4 | 4 | 0.000e+00 |
| `rho` | 3 | 3 | 4.440892e-15 |
| `1 - rho(A_1)` | 3 | 3 | 0.000e+00 |
| `mu_pref (upper bound)` | 2 | 2 | 1.107879e-07 |

Seven exact rows only work if the recompute is bit-reproducible, so that is **measured on
every run** rather than assumed: `12 of 12 groups reproduce the baseline's observed spread
exactly`. A group drifting *below* its tolerance is **not** RED — a tolerance is a ceiling,
and reddening on any change at all is the useless instrument arm **W3** exists to rule out.

**There is no `--refresh`.** A disagreement is a finding and gets a ticket; it is not
resolved by preferring the more recently edited tree, and not by widening a tolerance. A
tolerance edited to admit an observation is the observation deleted. `mkbaseline.py` is
never run by the gate, and it *refuses* to write a baseline that would paper over a live
disagreement.

---

## §4 THE PREDICATE ROW HAS ITS OWN ARM (g2)

Ten trees carry ten names for the primitivity **predicate**, agreeing at all 404 posets. It
is the largest alias group in the corpus and it matters more than any float row, because it
defines the population every published `6 of 275` is stated over.

*"A boolean that agrees is quieter than a float that agrees, and an equality check on it can
pass for reasons a float check would not."* Four such reasons, each with its own arm:

* **P3 — the population hides it.** A predicate replaced by `return True` agrees with all
  nine others on POP-PRIM. Arm P3 shows the same mutation **RED on POP-ALL and silent on
  POP-PRIM**. This is why g2 runs on POP-ALL and g1 does not.
* **P4 — agreement is invariant under the population moving.** If the poset generator
  changed, all ten predicates would follow it and go on agreeing perfectly. The planted
  world reports **0 pairwise disagreements**; only the pinned vector digest catches it.
* **P5 — `bool()` coercion.** A predicate returning `[1]`/`[]` gives an identical vector and
  an identical digest. Caught only by the pinned return type.
* **P6 — a predicate that does not discriminate cannot corroborate.** The live split
  (306 True / 98 False) is asserted, not assumed.

**§G2c, which fell out of a mistake of mine (D1) and is the sharpest thing in this
directory:** restricted to POP-PRIM, **11 of the 11 vectors are constant** — necessarily,
because POP-PRIM *is* the set where this predicate is true. On the corpus's published
population these ten trees agree perfectly and carry **zero bits** of information about each
other. g1's tolerances are stated over POP-PRIM because that is where the floats are
published; g2 runs on POP-ALL because that is the only place the boolean says anything. The
two arms genuinely want different populations, and that — not symmetry — is why the
predicate row needed an arm of its own.

---

## §5 THE POSITIVE CONTROL, AND FIVE DEFECTS OF MY OWN

**`x0_exhibit.py` — one real edit, one real command.** `E_footrule` gains `+ 1/10^9` in
`code/sweep_loss_51f4/lib51f4.py`, one of the four trees that compute the footrule. Then
`./build.sh` — the command `.pogo/refinery.toml` names — is run:

```
./build.sh  exit 1
  RED    E_footrule                4/ 4 names   spread 1.000e-09   tol 0.000e+00
           DISAGREE — direct_prefix_audit_2de0:E_footrule  vs  sweep_loss_51f4:E_footrule
             spread 1.000000e-09 > tolerance 0.000000e+00 at poset #0:
             direct_prefix_audit_2de0:E_footrule = 2.6666666666666665
             vs   sweep_loss_51f4:E_footrule = 2.6666666676666666
```

The unmodified gate is scored **first** (exit 0), the tree is restored byte-identically
under a checked sha256, and `git diff --quiet` confirms it. `15 of 15` falsification arms
across g1 (6 CAUGHT, 2 REFUSED-CORRECTLY) and g2 (5 CAUGHT, 2 REFUSED-CORRECTLY) are
satisfactory; the mutations are **derived** from values the trees actually produced — one
ULP, a multiple of the pinned tolerance — never typed as known-bad literals.

> **As of mg-479c the suite carries `31 of 31` arms** — 21 CAUGHT, 10 REFUSED-CORRECTLY, 0
> unsatisfactory: g1's 8 W-arms plus 6 N-arms, g2's 7, and g3's 10. §7.

**A remedy is an artifact of the same kind as the defect, so it is subject to it.** Five
defects of my own, all kept:

* **D1 — my "naive check" was not naive, and my own scoreboard caught it.** P3b claimed to
  run the boolean-agreement check somebody would plausibly have written, but left this
  gate's *own* discrimination test switched on. It reported 10 problems and the scoreboard
  scored the arm **FALSE-POSITIVE**. The 10 were real, and became §G2c above — the best
  reading in this directory came out of a broken arm, not a working one.
* **D2 — my first `run_all.sh` was a FAIL-OPEN MERGE GATE.** It wrote
  `python3 … || true; RC=$?`, which captures the exit status of `true` and is therefore 0
  forever. A gate that cannot report red, in the suite whose entire subject is a control
  that cannot fire. Caught by reading my own diff, not by any arm.
* **D3 — the exhibit misreported its own evidence.** `x0_exhibit.py`'s first line filter had
  an operator-precedence bug (`a or b or c and d`) and printed *other suites'* output as if
  it were this one's finding. An exhibit whose job is to show what the gate said, showing
  something else.
* **D4 — this gate checks AGREEMENT, NOT CORRECTNESS, and cannot tell the difference.** If
  all eleven trees changed together — a shared convention edited, or `lib0d1b`'s canonical
  poset form altered — every row stays green. It is a cross-check between independent
  implementations and it is worth exactly as much as their independence, which mg-0d1b's
  V3 arm established and this suite *inherits without re-establishing*.
* **D5 — the tolerance is the observed spread, so this suite is pinned to this host's
  arithmetic.** Seven exact-equality rows leave no float slack at all. Two independent runs
  here reproduce all twelve spreads bit-for-bit, and the seven exact rows are rational
  (`Fraction`) arithmetic converted by correctly-rounded `float()`, which is the reason to
  expect it to hold elsewhere — but **I have not run this on a second machine**, and if it
  does not hold, this gate fails for a reason no author can act on. That is mg-724a's own
  named hazard arriving by a different road, and the `bit-reproducibility` line printed on
  every run is the early warning, not a fix.

---

## §6 WHAT THIS DOES NOT ESTABLISH

* It does not establish that any of these twelve quantities is **right** — see D4.
* It does not establish agreement at **n > 5**. Everything here is mg-0d1b's population,
  n = 3,4,5. Two scalars that agree there can differ at n = 8.
* It does not cover the **DECLARED** rows of INDEX.md — `LSTAR(n)`, `c_or(n)`, `c#`, `u_M`,
  `f*`, `eps_spec`, `delta(P)`, `lambda_2`. Those were leads and not findings when mg-0d1b
  filed them and they are leads still. `delta(P)` — nine name-forms in eight trees — remains
  **the largest unswept candidate in the corpus**.
* It does not cover the **172 trees** no adapter reaches, of which mg-0d1b's `x1` classifies
  59 as doing the arc's mathematics with no adapter.

## §7 mg-479c — THE NORMALISATION FIELD

> **THE ALIAS AGREEMENT CHECK CANNOT TELL A NORMALISATION FROM A DISAGREEMENT: a factor of 2
> between two live conventions and a genuine 2× error are the same signal, and this corpus
> demonstrably carries both.**

§2–§5 above describe a check that compares **values** across the names of one quantity. It
had no representation for two names denoting the same quantity **in different
normalisations**, and both directions of that hole are live:

* **FALSE RED** — two conventions that agree modulo a factor report as a disagreement. On a
  gate that blocks merges, a red for a non-reason is how gates get disabled.
* **FALSE PASS** — a genuine 2× error becomes dismissable as *"just a normalisation
  difference"*, because the check gave an operator no way to tell them apart.

They are the **same missing bit** read from opposite ends: the index could not state whether
two names share a convention.

### §7.1 The representation, and why it is not a constant

`NORMALISATION.json` declares, **per name and not per quantity**:

```json
"chain_iv_c_81ff:lambda2_bracket": {
  "convention": "gamma",
  "to_canonical": {"num": [1], "den": [1]},
  "source": "DERIVED, not asserted: mg-0d1b measured this group's 9 names agreeing to …"
}
```

`to_canonical` is `num(n)/den(n)` — integer coefficients, low order first, evaluated in
exact `Fraction` arithmetic. **A per-name constant would have been unable to say what this
corpus already knows.** `code/c3_audit_a94c3/a1_algebra.py:18` states

> `eps_spec / eps_c3ca = 6 n^2 / (n^2 - 1) -> 6`

and `code/unitmap_audit_9f91/out_m1_map.txt` tabulates both quantities as exact rationals
under the heading *"DIRECTION OF APPROACH (what a flat factor of 6 gets wrong at small n)"*.
Arm **N14** re-derives the declared factor at **all 11 rows** of that table and **N15**
measures what a flat 6 gets wrong (`+0.0833` at n=3). The eps pair is one of the ticket's
own three examples and it is **n-dependent**; a constant field would have shipped unable to
represent it.

The eps pair lives in `worked_examples`, **not** in `declarations`: no adapter produces
either name, so an entry in the live namespace would be a statement the gate can never
check.

### §7.2 The three refusals, and why they are exit 2 and not exit 1

| refusal | when |
|---|---|
| `UNDECLARED-NORMALISATION` | a pinned name has no entry. **Never defaulted to "same"** — ticket item 3, and c9876's/cb417's lesson (a missing value must be loud, never blank) applied to a field rather than a cell. |
| `TOLERANCE-FRAME` | a group carries a non-identity factor while its tolerance is mg-0d1b's max spread of **raw** values. Not rescalable — members with different factors admit no single multiplier — so the registrant must record a canonical-frame tolerance with its own source. |
| digest moved | the declarations for the 71 pinned names no longer hash to what `BASELINE.json` was cut against. **Restricted to the pinned members**, so declaring a normalisation for a name this gate does not pin does *not* redden it (that would be this ticket's own thesis, shipped inside its remedy). |

An undeclared field means the comparison **could not be made**, which is a different fact
from two numbers disagreeing, and this suite's exit convention already separates them
(`1` a control fired, `2` refused/broken). `Scoreboard.arm_outcome` exists because a
two-valued arm cannot express it.

**The refusal is in `mkbaseline.py` AND in the gate, and that is not belt-and-braces.**
`mkbaseline` is where a new name is registered; the gate reads pinned members out of
`BASELINE.json`. A refusal in the first alone is bypassed by a hand-edit to that file; a
refusal in the second alone lets a bad baseline be written and only fails at the next merge.

### §7.3 The convention label is load-bearing, not a comment

Two names declaring the **same** convention must declare **equal** factors; two declaring
**different** conventions must declare **different** factors. Both are hard refusals
(**N8**, **N9**), scoped **per quantity**. That rule is what makes the RED message's sentence
worth anything:

```
DISAGREE — c3_audit_a94c3:spectral_gap  vs  chain_iv_c_81ff:lambda2_bracket
  spread 1.000000e+00 > tolerance 4.665708e-10 at poset #31 (IDENTITY frame)
  c3_audit_a94c3:spectral_gap = 0.99999999999999956   vs   … = 1.9999999990686774
  normalisation: … in convention 'gamma' (x 1/1);  … in convention 'gamma' (x 1/1)
  raw ratio … = 0.500000000233  = 1/2
  THESE TWO NAMES ARE DECLARED TO BE IN THE SAME CONVENTION ('gamma'), so this is a
  DEFECT and not a normalisation difference.
```

That is ticket item 2 as output rather than as intent: *"an operator seeing `these differ by
exactly 2, and the index says these two names share a convention` knows it is a real defect;
seeing a bare inequality, they do not."*

### §7.4 IT IS INERT TODAY, AND THAT IS MEASURED

The twelve pinned groups contain **no normalisation pair** — the ticket's own `WHY NOT HIGH`.
All 71 names are declared in the identity normalisation, which is **derived from mg-0d1b's
measurement and not asserted**: names agreeing to ≤ `max_spread` over 306 posets are in one
normalisation, and each entry's `source` quotes the spread it is derived from. The
declaration is **redundant for these 71 names**; it exists so the 72nd cannot be added
silently.

* **N1** — the identity is a **pass-through**, not a multiply by `1.0`: **71 of 71 columns
  returned as the same list object, 71 of 71 bit-identical.** `v * 1.0 == v` for every finite
  float, and routing the identity through a multiply would make seven exact-equality rows
  depend on that staying true of whatever a tree returns next.
* **N2** — the pre-479c raw comparison and the canonical one give **identical verdicts on the
  real input**: 12/12 spreads identical, both 0 red, 0 refusals.
* `bit-reproducibility: 12 of 12` is unchanged, and `BASELINE.json`'s diff is **333
  insertions, 0 deletions**.

### §7.5 THE WRONG WAY, RUN RATHER THAN ARGUED

`x1_wrongway.py` (off the gate) loads `libagree.py` **as it is on `main`, by blob sha**, and
runs *its* `check_groups` on the same input. Not a flag of mine — the code that has been on
`build.sh` since mg-06d1 landed:

| input | pre-479c | mg-479c |
|---|---|---|
| a legitimate normalisation pair (doubled **and declared** doubled) | **1 red** | 0 red, 0 refused |
| a genuine 2× error (doubled, **not** declared) | **1 red** | **1 red**, naming the ratio and the shared convention |

**The pre-479c gate gives the same answer to both.** That is the ticket in one line.

### §7.6 WHAT THIS DOES NOT CLOSE — and it is the important paragraph

**A DECLARED FACTOR IS AN ESCAPE HATCH AND THIS MACHINERY CANNOT CLOSE IT.** An operator
facing a real 2× disagreement can silence it by declaring a factor of 2, and nothing here
tells that edit from a correct one. It was filed in advance as **P6 at 0.70** and it did not
improve on contact. The two mitigations are both *reporting*, not enforcement:

1. every non-identity factor is printed on **every** run, green as well as red — g3's
   inventory and g1's `norm …` column. A factor that only becomes visible when something
   breaks is invisible;
2. the RED message states whether the two names **share a convention**, so a clean ratio
   inside one convention reads as a defect and not as units.

The declaration file is committed, so the edit is a diff with an author. **That is the whole
of the protection**, and stating it here is not a disclaimer — it is the reason `mknorm.py`
refuses to run twice and the reason the digest is pinned into `BASELINE.json`.

### §7.7 ITEM 4 — NOTHING IS RESOLVED, AND THE ABSENCE IS CHECKABLE

Ticket item 4: *"DO NOT RESOLVE ANY EXISTING AMBIGUITY AS PART OF THIS."* `STATE.md:172`
says *"the gap between `(L*)` and `(M♯)` is exactly `μ_pref²`"*; in the normalisation that row
itself uses (`μ·Δ ≤ γ`) it is `μ_pref²/2`, and it is `μ_pref²` in the doubled form
`2μ·Δ ≤ 2γ`. **Both readings are in the corpus.** That is mg-5e82's business and a
mathematical question.

An absence is a weak thing to claim, so **N7** makes it checkable: no declaration may mention
the gap and **no pinned name may carry a non-identity factor**. It reads `0` and `0` today
and goes RED the day either stops being true. `STATE.md` is not edited, `alias_groups.json`
is not rewritten, no tolerance is invented, and no alias group is added — **mg-a397 owns the
widening** and registering a group to have something to demonstrate on would have been doing
its work badly instead of mine.

### §7.8 FIVE DEFECTS OF MY OWN, ALL KEPT

* **D1 — I wrote the consistency rule GLOBALLY and it rejected the very file this ticket
  exists to write.** "Different convention labels must declare different factors" is correct
  *within one quantity* and nonsense across the corpus: twelve groups whose members are all
  in the identity normalisation are twelve different conventions sharing one factor. My first
  version refused all 71 seeded declarations. The rule is now scoped per group, and the
  scoping is stated in `libnorm.check_consistency`'s docstring rather than being a silent
  parameter.
* **D2 — MY OWN REFUSAL INTERCEPTED THE TICKET'S HEADLINE CASE, and my own scoreboard scored
  it FALSE-POSITIVE.** Arm N3 — a legitimate normalisation pair going GREEN, the whole point
  of the ticket — came back `expected GREEN, got REFUSAL`, because declaring a non-identity
  factor puts the group in a canonical frame and the `TOLERANCE-FRAME` refusal fires first.
  Both behaviours are right; what was wrong was my model of registration, which is a **two-part
  act** (a factor *and* a canonical-frame tolerance) and which I had written as one. N3 now
  plants both halves and N6 plants the first alone. Caught by an arm and not by reading.
* **D3 — my N4 assertion was stricter than my own message and would have failed for the right
  reason.** The arm looked for the ratio reported as `EXACTLY 2/1`; `lambda2_bracket` is a
  bracket midpoint, so the real ratio is `0.500000000233` and the message correctly prints
  `= 1/2` without `EXACTLY`. The *message* was right and the *arm* was wrong — the opposite
  of the usual direction, and worth writing down for that reason.
* **D4 — this field is checked for CONSISTENCY, never for TRUTH.** §7.6. It is D4 of §5
  arriving one level up: that gate checks agreement and not correctness, and this one checks
  that the declarations do not contradict each other and not that any of them is right.
* **D5 — running `./build.sh` rewrote three transcripts in three directories that are not
  mine**, which is mg-724a's D5 arriving by the same road it always does. They are restored
  and `0 files outside this directory differ`. Two of the three were **already stale on
  `main`** — `control_audit_9876`'s sweep reads `188 directories` where the tree now has 192,
  and `724a`'s gate records `208` membership candidates where it now observes `209`, both from
  suites that landed after those transcripts were cut. That is **not this ticket's finding to
  act on** and it is written down rather than fixed.

### §7.9 THE PREDICTIONS

`PREDICTIONS-mg-479c.md` was committed **before one line of the instrument existed**, with
two exposures disclosed (H2: I had already found the n-dependent eps factor, so **P4 is a
report and not a bet**).

| | claim | outcome |
|---|---|---|
| **P1** 0.95 | the twelve verdicts are unchanged bit-for-bit | **HIT** — 12/12 spreads, 71/71 columns |
| **P2** 0.80 | both false directions plantable on real columns | **HIT** — N3/N4, a doubled real column |
| **P3** 0.75 | convention ↔ factor must be made to agree | **HIT, and it cost me D1** |
| **P5** 0.60 | the carried tolerance does not survive, and I refuse rather than rescale | **HIT** — `TOLERANCE-FRAME` |
| **P6** 0.70 | the declared factor is an unfalsifiable escape hatch I cannot close | **HIT, unhappily** — §7.6 |
| **P7** 0.65 | added runtime under 1 s | **HIT by a wide margin** — g3 is **0.03 s**, g1's six arms **0.1 s** |
| **P8** 0.55 | I can prove I did not decide mg-5e82's question | **HIT** — N7 |
| **P9** 0.50 | I put the refusal in only one of the two places at first | **HIT** — I wrote the gate's copy first |

---

## Files

| file | what it is |
|---|---|
| `BASELINE.json` | the pinned expectation: 12 groups, 71 names, tolerances carried from mg-0d1b, plus the predicate vector digest and return types |
| `mkbaseline.py` | derives that file from `alias_groups.json`. **Run by hand. Never by the gate.** |
| `libagree.py` | the comparison, the mutation harness, and the CAUGHT/MISSED/UNFALSIFIABLE scoreboard |
| `predicates.py` | the ten primitivity predicates, carried verbatim from x3's V4 |
| `g1_values.py` | the float arm — 12 groups over POP-PRIM, + 8 planted worlds. **30 s** |
| `g2_predicate.py` | the predicate arm — 10 names over POP-ALL, + 7 planted worlds. **0.2 s** |
| `x0_exhibit.py` | the end-to-end control: a real edit to a real tree, `./build.sh`, verified restore. **Not run by the gate** |
| `run_all.sh` | what `build.sh` invokes. g2, then g3, then g1; worst exit wins |
| `NORMALISATION.json` | **mg-479c** — the normalisation declared **per name**: convention, `to_canonical` factor as `num(n)/den(n)`, and a source. Plus the eps worked example, and what is deliberately **not** declared |
| `mknorm.py` | seeded that file **once** from mg-0d1b's measured agreement. **Refuses to run again.** Never run by the gate |
| `libnorm.py` | the factor (exact `Fraction`, rational function of `n`), the declaration loader and its refusals, canonicalisation, and the RED message's normalisation sentence |
| `g3_normalisation.py` | the declaration arm — inventory, representation unit checks, the eps worked example re-derived from mg-9f91's table, + 10 planted worlds. **0.03 s** |
| `x1_wrongway.py` | the wrong-way exhibit: the **blob-pinned pre-479c `libagree.py`** run on a legitimate normalisation pair. **Not run by the gate** |
| `PREDICTIONS-mg-479c.md` | mg-479c's predictions, committed before one line of it existed |
