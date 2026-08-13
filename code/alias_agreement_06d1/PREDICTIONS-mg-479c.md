# mg-479c — PREDICTIONS, committed before one line of the instrument exists

**THE TICKET.** mg-06d1's agreement check compares VALUES across the names of one quantity and
goes RED when two names disagree beyond the group's tolerance. It has no representation for two
names denoting one quantity **in different normalisations**. Both directions fail: a FALSE RED
(two conventions agreeing modulo a factor, reported as a disagreement, on a gate that blocks
merges) and a FALSE PASS (a genuine 2× error dismissable as "just a normalisation difference",
because the check gives an operator no way to tell them apart).

---

## H — WHAT I ALREADY KNOW, DISCLOSED RATHER THAN LAUNDERED

A prediction made after reading the answer is a report. These are reports and are marked as
such; everything under P is a bet.

* **H1 — I have read the whole of `code/alias_agreement_06d1/` and `BASELINE.json` before
  writing this.** I know the twelve pinned groups, that seven are pinned at tolerance
  `0.000e+00`, and that the gate has run with zero disagreements. So **P1 is not a bet about
  whether a normalisation pair exists among the twelve** — the ticket already states it does
  not, and I have confirmed it. P1 is a bet about whether the change is *measurably inert* on
  the real input, which is a different and checkable claim.
* **H2 — I have found a live corpus normalisation with an `n`-DEPENDENT factor before writing
  the representation.** `code/c3_audit_a94c3/a1_algebra.py:18` states
  `eps_spec / eps_c3ca = 6 n^2 / (n^2 - 1) -> 6`, and `code/unitmap_audit_9f91/out_m1_map.txt`
  tabulates both quantities as exact rationals at eleven values of `n` under the heading
  *"DIRECTION OF APPROACH (what a flat factor of 6 gets wrong at small n)"*. So **P4 is a
  report, not a bet**: I already know a constant-factor field cannot represent one of the three
  examples the ticket itself names, and I am recording that I knew it before choosing the
  representation rather than discovering it afterwards.
* **H3 — I have read STATE.md:172 and located the `μ_pref²` clause verbatim.** I am not going to
  decide it (ticket item 4, and mg-5e82 owns it). Knowing exactly where it is makes P8 — that I
  can build an arm proving I did *not* decide it — cheap, and it is filed as a bet only about
  whether such an arm is constructible without asserting either reading.

---

## P — THE BETS

| # | prob | claim |
|---|---|---|
| **P1** | **0.95** | **The twelve pinned groups' verdicts are UNCHANGED, bit-for-bit, by this ticket.** Every one of the 71 pinned names will be declared in the identity normalisation, so the canonical columns will be the raw columns and all twelve spreads will reproduce `observed_at_baseline` exactly. If this loses, my canonicalisation is not identity-preserving on identity factors and the seven exact-equality rows are the first casualty. |
| **P2** | **0.80** | **Both false directions can be planted on the REAL captured columns, without inventing a fixture.** A second name doubled inside one declared convention (the FALSE PASS) and a second name doubled *with* a declared factor of 2 (the FALSE RED) are both derivable from a column a tree actually produced. |
| **P3** | **0.75** | **The `convention` label and the factor will turn out to be two statements of the same fact, and requiring them to AGREE is the check that makes the RED message trustworthy.** Two names declaring the same convention must declare equal factors; two declaring different conventions must declare different factors. I expect to be able to make both hard refusals with no legitimate entry violating either. |
| **P4** | *report* | **A constant per-name factor is not enough.** `eps_spec / eps_c3ca = 6n²/(n²−1)` — see H2. The representation will be a rational function of `n` with integer coefficients, evaluated in exact `Fraction` arithmetic, of which the constant is the degree-0 case. |
| **P5** | **0.60** | **The carried tolerances become meaningless the moment a group gains a non-identity member, and I will have to REFUSE rather than rescale.** mg-0d1b measured max raw spread; members with *different* factors do not admit a single tolerance rescale. I predict I end up requiring the registrant to supply a canonical-frame tolerance with its own source, and refusing (exit 2, not exit 1) when they have not. Held at 0.60 because I may find a derivable rescale I have not seen. |
| **P6** | **0.70** | **My own remedy carries the defect it repairs, in a form I can name now: a declared factor is an unfalsifiable escape hatch.** An operator faced with a real 2× disagreement can silence it by declaring a factor of 2. Nothing in the machinery can distinguish that edit from a correct one. I predict the only honest mitigations are (a) the factor is printed on EVERY run, green as well as red, and (b) the RED message states whether the two names share a convention — and that I will not be able to close it. |
| **P7** | **0.65** | **The runtime cost is under 1 s.** The declaration arms need no recompute; the arms that need real columns reuse g1's single 30 s capture. If this loses, the gate goes past ~46 s and I have to argue the cost the way §1 of the README argues the first 31 s. |
| **P8** | **0.55** | **I can build an arm that PROVES this ticket did not decide mg-5e82's question** — i.e. that no pinned member carries a non-identity factor and no declaration mentions the `(L*)`/`(M♯)` gap — without the arm itself asserting either reading of it. Held near even because "proves an absence" is the shape of claim this arc keeps getting wrong. |
| **P9** | **0.50** | **`mkbaseline.py` and the gate will BOTH need the refusal, and I will be tempted to put it in only one.** The gate reads pinned members from `BASELINE.json`; `mkbaseline` is where a new name is registered. A refusal in `mkbaseline` alone is bypassed by a hand-edit to `BASELINE.json`; a refusal in the gate alone lets a bad baseline be written and only fails later. Even odds that I catch the second one only on re-reading my own diff. |

---

## E — ERRORS I MIGHT COMMIT, FILED BEFORE THEY HAPPEN

* **E1 — declaring the 71 identity factors as a JUDGEMENT rather than as a DERIVATION.** The
  only evidence I have that these names share a normalisation is that mg-0d1b measured them
  agreeing to ≤ tolerance. Writing `"factor": 1` by hand for 71 names would be 71 assertions I
  cannot back. They must be *seeded from the record*, with the measured spread quoted as the
  derivation, and the file must say in so many words that the declaration is **redundant** for
  these names and exists so the 72nd cannot be added silently.
* **E2 — the seeding script becoming a `--refresh`.** A script that fills in identity
  declarations for whatever is in the record will silently absorb the next name added to the
  record, which is precisely the defect. It must refuse to run once the file exists.
* **E3 — multiplying by `1.0`.** Even though `v * 1.0 == v` for every finite float, routing the
  identity case through a multiply makes the seven exact rows depend on that being true of
  `None`, of `inf`, and of whatever a tree returns next. The identity case must be a
  pass-through, and the bit-identity must be MEASURED and not argued.
* **E4 — a normalised comparison against a raw-frame tolerance.** See P5. Silently rescaling
  the frame the comparison happens in, while keeping the number that governs it, is this
  ticket's own defect one level up.
* **E5 — deciding STATE.md's row by accident.** Any declaration I register for the (L\*)/(M♯)
  gap, in either direction, decides mg-5e82's question under this ticket's cover. Ticket item 4
  forbids it and I have filed P8 to make the absence checkable.
* **E6 — a worked example that no tree computes, filed as a live declaration.** The eps pair is
  not pinned and not produced by any adapter. Putting it in the live declaration namespace
  would be a declaration about a name nothing computes — a statement the gate can never check.
  It goes in a separately-named section or not at all.
* **E7 — a `demo_wrong_way` against a strawman.** Showing that "the comparison with
  normalisation switched off" goes RED on a legitimate pair proves nothing unless that path IS
  the shipped pre-479c comparison. Either pin the old code by blob, or measure that the two
  paths agree on the real input — arguing it is not enough.
* **E8 — widening the check while claiming only to represent.** mg-a397 owns the widening. If I
  register a new alias group to have something to demonstrate on, I have done mg-a397's work
  badly instead of mine.
* **E9 — a red for a non-reason.** The ticket's own thesis is that a gate that reddens for a
  non-reason gets disabled. If my digest check goes red because somebody added a declaration for
  an *unpinned* name, I have shipped the failure mode the ticket is about. The digest must be
  over the declarations restricted to the pinned members.

---

## CONDITIONS FOR NOT MAKING THE CHANGE, filed in advance

So that a refusal cannot be assembled after the fact:

1. If the identity canonicalisation cannot be made bit-identical on the seven exact-equality
   rows, the change does not land — a normalisation field is not worth loosening the tightest
   rows in the gate.
2. If the runtime cost of the added arms exceeds ~5 s, the added arms do not go on the gate;
   they go in an off-gate exhibit and the README says so with the measurement.
3. If declaring the 71 identity factors turns out to require any assertion beyond mg-0d1b's
   measured agreement, the file is not seeded and the ticket lands as a refusal plus a
   representation that the next registrant must fill in.
