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
| `run_all.sh` | what `build.sh` invokes. g2 first, then g1; worst exit wins |
