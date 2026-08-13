# mg-479c — the pre-registration, SCORED

`PREDICTIONS-mg-479c.md` was committed on **2026-08-10** (author date preserved through the
refinery's rebase; landed as `1a0240a`) before one line of `libnorm.py` existed. This file
scores it against what the instrument did. It is written after the instrument ran and is
therefore worth exactly as much as the pre-registration's ordering makes it worth — which is
the whole reason that commit was worth rescuing rather than rewriting.

**Headline: 6 live bets, 6 confirmed, and the confirmations are the LEAST interesting part.**
Every live bet came in, which is a warning and not a result: five of the six were bets about
what I would *choose to build*, and an author who both writes the predictions and holds the
pen is not being tested by those. The two things worth reading are **P6**, which I predicted
I would fail to close and did fail to close, and the three errors I committed anyway.

---

## The reports (zero credit, and they were declared as such in advance)

| # | claim | outcome |
|---|---|---|
| **H1** | I had read the whole directory and `BASELINE.json` first: 12 groups, 7 at tolerance `0.000e+00`, zero disagreements ever. | Stands. This is why **P1** was filed as a bet about *measurable inertness* rather than about whether a normalisation pair exists among the twelve. |
| **H2 / P4** | A constant per-name factor is not enough: `eps_spec/eps_c3ca = 6n²/(n²−1)`, tabulated as exact rationals at eleven `n` in `code/unitmap_audit_9f91/out_m1_map.txt`. | **Report, and it drove the design.** The factor is a rational function in exact `Fraction` arithmetic. Arm **N3** parses that transcript's eleven-row table — carried, not retyped — and checks three things: the table's own `ratio` column equals `eps_spec/eps_c3ca` at **11 of 11**, the declared factor reproduces it at **11 of 11**, and a flat constant `6` reproduces it at **0 of 11**, still `6.001e-04` out at `n = 100`. |
| **H3** | I had located STATE.md's `μ_pref²` clause and would not decide it. | Stands, and it got easier: **mg-5e82 has since settled that row**, which the pre-registration did not know. See P8. |

---

## The live bets

| # | prob | outcome | what actually happened |
|---|---|---|---|
| **P1** | 0.95 | **CONFIRMED** | *"The twelve pinned groups' verdicts are UNCHANGED, bit-for-bit."* All 71 names are declared in the identity normalisation and the identity case is a **pass-through** — the same column object, not a multiply. `g1` re-runs the shipped pre-479c comparison (`norm=None`) on the same captured columns every run and reports `12 of 12 groups bit-identical`; a difference is exit 2, which is condition 1 of the pre-registration wired in as a runtime refusal rather than left as a promise. |
| **P2** | 0.80 | **CONFIRMED** | *"Both false directions can be planted on the REAL captured columns."* `W9`/`W10` plant **identical** columns — a real `anticorrelation_c50b:leak(1)` column, doubled — and differ **only** in the declarations, coming out GREEN and RED respectively. No fixture was invented. The group was switched from `gamma` to `leak(A_1)` mid-build for a reason the prediction did not anticipate: `gamma` agrees only to `4.666e-10`, so a doubled `gamma` column stands in a ratio of *approximately* 2, and the exact-ratio diagnostic would have needed a fuzzy match. On the exact-equality group the ratio is exactly `2` in `Fraction` arithmetic and nothing rests on a tolerance. |
| **P3** | 0.75 | **CONFIRMED** | *"The convention label and the factor are two statements of the same fact, and requiring them to AGREE is what makes the RED message trustworthy."* Both rules ship as hard refusals — `CONVENTION-SPLIT` (one convention, two factors) and `CONVENTION-PHANTOM` (two conventions, one factor) — and no legitimate entry violates either. `W11` is the payoff: it is what stops the 2× being silenced quietly. |
| **P5** | 0.60 | **CONFIRMED, and it was the right side of an even bet** | *"The carried tolerances become meaningless the moment a group gains a non-identity member, and I will have to REFUSE rather than rescale."* No derivable rescale was found — members with different factors do not admit one — so `TOLERANCE-FRAME` refuses and the registrant must supply a canonical-frame tolerance with its own source. `W9b` and `D8` measure the refusal; **`D9` is the half the prediction did not see**: a canonical tolerance declared for an all-identity group is *also* refused, because a number waiting to take effect on the next declaration edit is a number nobody checked. |
| **P6** | 0.70 | **CONFIRMED — AND IT IS THE ONLY ONE THAT MATTERS** | *"A declared factor is an unfalsifiable escape hatch and I will not be able to close it."* **I did not close it.** An operator facing a real 2× can declare a factor of 2 and nothing distinguishes that edit from a correct one. Both mitigations the prediction named are shipped — the factor is printed on **every** run (`N0`) and the RED message states whether the two names share a convention — and one it did not name fell out of P3: the edit cannot be made *quietly*, because a lone factor without a new convention is self-contradictory (`W11`). The hatch is **loud**, not **narrow**, and README §7 D6 says so in those words. |
| **P7** | 0.65 | **CONFIRMED** | *"Runtime under 1 s."* `g3` is **0.02 s** (it recomputes no tree). `g1`'s falsification block went 0.1 s → **0.63 s**, the cost being the exact-ratio diagnostic walking pinned pairs in `Fraction` arithmetic; the 29 s recompute is untouched and is **reused** by all seven new worlds. Condition 2 (~5 s ⇒ off-gate) was not reached. |
| **P8** | 0.55 | **CONFIRMED, and the ground moved under it** | *"I can build an arm that PROVES this ticket did not decide mg-5e82's question."* Arm **N5** reports 0 of 71 non-identity factors, 0 of 12 multi-convention groups, 0 declarations using the gap's language, 0 canonical tolerances. **What the prediction did not know: mg-5e82 had already settled STATE.md's row**, which now reads `μ_pref²/2 in this row's own normalisation` and names mg-479c as carrying the general hazard. So the arm proves an absence that was no longer at risk. Its honest scope is stated in its own output: it measures that the *declarations* are silent, not that the branch is — that STATE.md is untouched is a property of the diff. |
| **P9** | 0.50 | **CONFIRMED, and by the mechanism it predicted** | *"`mkbaseline` and the gate will BOTH need the refusal, and I will be tempted to put it in only one."* `mknorm.py` refuses to run once the file exists (the registration side) **and** `libnorm.validate` refuses an undeclared or unseeded pinned name on every gate run (the read side), so a hand-edit to `NORMALISATION.json` is caught even though `mknorm` never sees it. The even odds were on catching the second only on re-reading my own diff; in fact the read-side refusal was written first, because `g1`'s exit-2 path had to exist before there was anything to seed. |

---

## The errors, and three of them happened

`E1`–`E9` were filed before the instrument existed. Six were avoided **because they were
filed**; three were committed and are kept.

| # | filed as | what happened |
|---|---|---|
| **E1** | declaring 71 identity factors as a JUDGEMENT rather than a DERIVATION | **AVOIDED.** `mknorm.py` seeds every declaration from `BASELINE.json` and carries the measured spread as a machine-checkable field; `D6` edits one and the gate refuses. The file says in so many words that the declaration is *redundant* for these names. |
| **E2** | the seeding script becoming a `--refresh` | **AVOIDED.** `mknorm.py` refuses to run once the file exists, and says why. |
| **E3** | multiplying by `1.0` | **AVOIDED.** The identity case returns the same column object. The bit-identity is **measured** against the pre-479c path on every run, not argued. |
| **E4** | a normalised comparison against a raw-frame tolerance | **AVOIDED.** `TOLERANCE-FRAME`, and `D9` for the converse. |
| **E5** | deciding STATE.md's row by accident | **AVOIDED** — and see P8: mg-5e82 got there first. |
| **E6** | a worked example that no tree computes, filed as a live declaration | **AVOIDED.** The `eps` pair sits in an `illustrative` section that `N3` validates and `g1` never compares. README §7 D10 records what that costs: nothing gates the pair itself. |
| **E7** | a `demo_wrong_way` against a strawman | **AVOIDED, by the second of the two routes the prediction offered.** `W9a` runs the *actual* pre-479c comparison — `check_groups(..., norm=None)`, still reachable and still the code path `W1`–`W8` falsify — and `G1b` measures the two paths agreeing on the real input rather than arguing it. |
| **E8** | widening the check while claiming only to represent | **AVOIDED.** No alias group was registered; the twelve pinned groups and 71 names are unchanged. mg-a397 still owns the widening. |
| **E9** | **a red for a non-reason, shipped inside the remedy** | **COMMITTED, TWICE, AND CAUGHT BOTH TIMES.** (1) The digest is restricted to pinned members precisely so a declaration for an unpinned name cannot move it — `D4` measures that, and that half was designed in. (2) The half that was *not*: my first `N5` scanned live declarations for the bare string `mu_pref` and reported **nine hits**, because six of the twelve groups *are* about `μ_pref` and the seeded derivations quote the group label. Nine findings that meant nothing, in the arm whose subject is findings that mean nothing. Fixed to scan the **clause**; recorded as README §7 D8 rather than quietly repaired. |

**Two further defects the pre-registration did not anticipate, both kept:**

* **`x0_exhibit.py` was reading a fixed four-line window** of the gate's RED block. My own
  change made that block longer, so the exhibit would have printed the finding cut off
  mid-sentence — README §5's **D3** (an exhibit whose job is to show what the gate said,
  showing something else) arriving a second time through a different door. The window is now
  the RED line plus its continuations.
* **The digest is a speed bump and I nearly counted it as a control.** README §7 D7.

---

## What this leaves for whoever is next

* **mg-a397's widening is where this earns anything.** Today: 12 groups, 71 names, one
  convention, zero non-identity factors, nothing firing. The field's whole value is that the
  72nd name cannot be registered silently.
* **P6 is open and is not closable by this machinery.** The escape hatch is a property of
  letting anybody declare a factor. Narrowing it means checking a declared frame against the
  tree that produces the name, which is a different and much larger instrument.
* **The `eps` pair is the corpus's live `n`-dependent normalisation and no adapter reaches
  it.** If mg-a397's widening brings either name under an adapter, its declaration moves from
  `illustrative` to `declarations` and becomes the first real test of the representation.
