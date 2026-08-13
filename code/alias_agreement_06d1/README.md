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
* **(mg-479c)** It does not establish that any declared normalisation is the **right** one —
  see §7's D9. The field records what somebody claimed a name's frame is; nothing here
  checks the claim against the tree that produces the name.

---

## §7 THE NORMALISATION FIELD (mg-479c)

**The gap.** Everything above compares **values** across the names of one quantity. It had
no representation for two names denoting one quantity **in different normalisations**, so a
factor of 2 between two live conventions and a genuine 2× error were **the same signal**.
Both directions fail:

* **FALSE RED** — two conventions that agree modulo a factor report as a disagreement. On a
  gate that blocks merges, a red for a non-reason is how gates get disabled.
* **FALSE PASS** — a genuine 2× error becomes dismissable as *"just a normalisation
  difference"*, because the check gives an operator **no way to tell them apart**.

**Nothing is firing today, and that is why it was built today.** The twelve pinned groups
contain no normalisation pair; the gate has run with zero disagreements. The exposure is
**prospective** — it arrives the moment the check is widened (mg-a397's candidates) or a new
alias is registered — and a representation added after the first false red is a
representation added under pressure to make a red go away.

### The field is per NAME, not per quantity

Two names for one quantity may legitimately differ by a **stated** factor, so the factor is
a property of the name. The semantics are one line:

```
raw(name, at a poset of size n)  ==  factor(name, n) * canonical(quantity, n)
```

`NORMALISATION.json` declares, for each of the 71 pinned names, a **convention** (a name for
a frame) and a **factor** (the frame's content). `{"num":[1],"den":[1]}` is the identity and
is a **pass-through**, not a multiply by `1.0` — routing the identity through a multiply
would make the seven exact-equality rows depend on `v * 1.0 == v` also holding of `None`, of
`inf`, and of whatever a tree returns next.

**The factor is a rational function of `n`, and this corpus already needed one.**
`code/c3_audit_a94c3/a1_algebra.py:14` records `eps_spec = 6E[inv_e]/(n²−1)` against
`eps_c3ca = E[inv_e]/n²`, i.e. `eps_spec/eps_c3ca = 6n²/(n²−1)`. Arm **N3** reads the exact
rationals `code/unitmap_audit_9f91/out_m1_map.txt` tabulates at five values of `n` — under
that file's own heading *"what a flat factor of 6 gets wrong at small n"* — and checks the
declared factor against their ratio in `Fraction` arithmetic: **declared 5 of 5, a flat
constant 6 zero of 5.** A constant-factor field could not have represented one of the three
examples the ticket itself names, and that was known **before** the representation was
chosen (H2 of `PREDICTIONS-mg-479c.md`, filed in advance and scored as a report at zero
credit).

### One input, two verdicts — the whole demonstration

`W9c` and `W10` in `g1_values.py` plant **identical columns**: a real `leak(A_1)` column that
`anticorrelation_c50b` actually produced, **doubled**. They differ only in the declarations,
and they come out opposite ways:

| arm | declarations | verdict |
|---|---|---|
| **W9a** | the pre-479c comparison (`norm=None`) | **RED** — the false red, with no field in which to say otherwise |
| **W9b** | factor `2` declared, group tolerance still mg-0d1b's **raw-frame** max spread | **REFUSED** — not rescaled |
| **W9c** | factor `2` **and** a canonical-frame tolerance | **GREEN**, canonical spread bit-identical to the baseline's `0.000e+00` |
| **W9d** | W9c's declarations, plus one extra ULP on top | **RED** — a declared factor buys a frame, not slack |
| **W10** | the live declarations — one shared convention | **RED**, *and the message says why* |

W10's RED now reads, in full:

```
BOTH NAMES DECLARE THE SAME CONVENTION ('mg-0d1b-raw'), so this residue is NOT a
  normalisation difference.
  It is a disagreement between two implementations of one quantity in one frame.
  File a ticket.
  NOTE: the two columns are in a CONSTANT RATIO of 2 across every comparable poset.
  That is the shape of an undeclared normalisation — but the declarations above say
  there is none, so either a factor is missing from this file or one of the two trees
  is wrong by that factor.  The instrument cannot tell which and does not guess.
```

The ratio note is **exact-only**: it fires when the two raw columns stand in an exactly
constant `Fraction` ratio at every comparable poset, which is a strong condition and is
usually **silent**. It is a diagnostic and never a verdict — it moves nothing from red to
green or back, and it never proposes a factor to declare.

### An undeclared normalisation is REFUSED, not defaulted to "same"

Exit **2**, not exit 1, and the difference is the ticket's item 3. On a merge gate, exit 1
says *"two of your numbers disagree, file a ticket"* and exit 2 says *"this instrument could
not answer"* — conflating them tells an author the wrong thing. This is c9876's and cb417's
lesson (a missing value must be loud, never blank) applied to a **field** rather than to a
cell. **W12** runs it against the **good** columns on purpose: the values agree perfectly,
the declaration is removed, and the instrument still refuses, because agreement measured in
a frame nobody has stated is not a measurement anybody can quote.

### The 71 identity factors are SEEDED, not asserted

The only evidence anybody has that these names share a normalisation is that **mg-0d1b
measured them agreeing** in the raw frame. Writing `"factor": 1` seventy-one times by hand
would have been seventy-one assertions this ticket cannot back (filed in advance as **E1**).
So `mknorm.py` seeds each declaration from `BASELINE.json` and carries the measured spread
it was seeded from as a machine-checkable number, which `libnorm.validate` re-checks against
the record on **every** gate run — arm **D6** edits one and the gate refuses. The
declarations are **redundant** for these 71 names and exist so the 72nd cannot be added
silently. `mknorm.py` **refuses to run once the file exists**, because a script that fills in
identity declarations for whatever is in the record would silently absorb the next name into
the identity normalisation, which is this ticket's own defect arriving through its remedy.

### The tolerance is a number in a frame, and the frame moved

mg-0d1b's tolerances are the **observed max raw spread** over POP-PRIM. The moment a group
gains a non-identity member the comparison happens in a different frame and that number no
longer governs it. Members with *different* factors do not admit a single rescale, so the
instrument **refuses** and requires a canonical-frame tolerance with its own source (`W9b`,
`D8`). The converse is refused too: a canonical tolerance declared for a group whose members
are all identity is a number nobody checked, waiting to take effect on the next declaration
edit (`D9`). Silently rescaling the frame while keeping the number that governs it would be
this ticket's own defect one level up — filed in advance as **E4**.

### THE CHANGE DECIDES NOTHING, AND THAT IS MEASURED

Item 4 of the ticket: settling whether STATE.md's row is in the halved or the doubled form
is a mathematical question and was mg-5e82's business. mg-5e82 has since settled it — that
row now reads `μ_pref²/2 **in this row's own normalisation**` and names mg-479c as carrying
the general hazard — so there is nothing left here to decide even by accident. Arm **N5**
measures it anyway: **0 of 71** pinned names carry a non-identity factor, **0 of 12** groups
carry more than one convention, **0** live declarations use the `(L*)`/`(M♯)` gap's language,
**0** canonical tolerances are declared. What that establishes is that the **declarations**
are silent; that STATE.md is untouched is a property of the diff, and N5 says so rather than
claiming it.

### THE COST

**0.02 s.** `g3_normalisation.py` recomputes no tree — it is a property of two committed JSON
files and one committed transcript. `g1`'s falsification block went from 0.1 s to **0.63 s**
(the exact-ratio diagnostic walks the pinned pairs in `Fraction` arithmetic); its 29 s
recompute is untouched and is reused by the seven new worlds rather than repeated. Condition
2 of `PREDICTIONS-mg-479c.md` set ~5 s as the line above which the arms would have gone
off-gate. They did not reach it.

### FIVE DEFECTS OF MY OWN, AND THE FIRST ONE IS NOT CLOSED

**A remedy is an artifact of the same kind as the defect, so it is subject to that defect.**

* **D6 — A DECLARED FACTOR IS AN UNFALSIFIABLE ESCAPE HATCH, AND I CANNOT CLOSE IT.** An
  operator facing a real 2× disagreement can make it go away by declaring a factor of 2.
  Nothing in this machinery can tell that edit from a correct one — the two are the same
  bytes. **This was filed at 0.70 before the instrument existed (P6) and it survived
  intact.** What is bought is that the edit cannot be made *quietly*: a factor is the content
  of a convention, so declaring one without also declaring a **new convention** is
  self-contradictory and refuses (`W11`), every factor is printed on **every** run green as
  well as red (`N0`), and that printing lands in a committed transcript that
  `code/gate_fixed_point_f771` compares against the tree on every merge. That makes the
  hatch **loud**. It does not make it narrow.
* **D7 — the digest is a speed bump and I nearly shipped it as a control.** `pinned_digest`
  makes an edit to a pinned declaration a two-place edit; anybody willing to update both gets
  past it. It is kept because two places is worse than one for an accidental edit, and it is
  labelled in `N2` rather than counted as a control.
* **D8 — the seeded derivations quote the group label, and my first "decides nothing" arm
  reported nine hits on the word `mu_pref`.** Six of the twelve groups *are* about `μ_pref`;
  matching the bare name reported nine findings that meant nothing — a red for a non-reason,
  in the arm whose subject is reds for non-reasons. The scan is now on the **clause**
  (`(L*)`, `(M♯)`, `μ_pref²`, the halved/doubled wording), and the near miss is recorded here
  rather than quietly fixed.
* **D9 — this arm checks that a frame is DECLARED, never that it is RIGHT.** A name in a
  doubled convention, declared as identity by somebody who believed it, passes everything
  here. That is mg-06d1's own **D4** (agreement is not correctness) one level up, and it is
  the same trade: what is bought is that the claim is now *written down* and comparable.
* **D10 — the worked example is not gated by anything that computes it.** `eps_spec` /
  `eps_c3ca` is the corpus's live `n`-dependent normalisation and **no adapter produces
  either name**, so it sits in an `illustrative` section that `N3` validates against
  committed exact rationals and `g1` never compares. If either quantity's definition moves,
  `N3` catches it only via `out_m1_map.txt`; if that transcript moves too, nothing here
  notices. It is a demonstration that the representation is strong enough, not a control on
  the pair.

---

## Files

| file | what it is |
|---|---|
| `BASELINE.json` | the pinned expectation: 12 groups, 71 names, tolerances carried from mg-0d1b, plus the predicate vector digest and return types |
| `mkbaseline.py` | derives that file from `alias_groups.json`. **Run by hand. Never by the gate.** |
| `NORMALISATION.json` | mg-479c's normalisation field: per **name**, the convention it reports in and the factor to divide by. 71 live declarations + 2 illustrative |
| `mknorm.py` | seeds that file from `BASELINE.json`'s measured spreads. **Run by hand, once. Refuses to run again.** |
| `libnorm.py` | the representation: the rational-function factor, the refusals, and the canonicalisation |
| `libagree.py` | the comparison, the mutation harness, and the CAUGHT/MISSED/UNFALSIFIABLE scoreboard |
| `predicates.py` | the ten primitivity predicates, carried verbatim from x3's V4 |
| `g1_values.py` | the float arm — 12 groups over POP-PRIM in the canonical frame, + 15 planted worlds. **30 s** |
| `g2_predicate.py` | the predicate arm — 10 names over POP-ALL, + 7 planted worlds. **0.2 s** |
| `g3_normalisation.py` | the declaration arm — 71 declarations, + 10 planted worlds. **0.02 s** |
| `x0_exhibit.py` | the end-to-end control: a real edit to a real tree, `./build.sh`, verified restore. **Not run by the gate** |
| `PREDICTIONS-mg-479c.md` | mg-479c's pre-registration, committed 2026-08-10 before one line of `libnorm.py` existed |
| `SCORING-mg-479c.md` | that pre-registration scored against what the instrument did |
| `run_all.sh` | what `build.sh` invokes. g2, then g3, then g1; worst exit wins |
