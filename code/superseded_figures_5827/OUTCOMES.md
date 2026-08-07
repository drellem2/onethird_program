# OUTCOMES — `mg-5827`, scored against `PREDICTIONS.md`

Predictions were committed at `8c398a5`, before any script of this instrument existed. **Misses are
kept as written.** Four of twelve are misses.

| # | prediction | outcome | measured |
|---|---|---|---|
| **P1** | ≥ 8 flat-text sites outside `STATE.md` at `f758468`; point estimate **14**, range **8–22** | **MISS** | **23** — outside my own declared range. I anchored on the population I had already repaired by hand (M1+M3 = 14 sites) and predicted my own hand sweep back at myself. The detector counts *occurrences*, not the *edits* I made, and several lines carry two registry entries at once. The prediction was right about the mechanism and wrong about the number, by the same anchoring error the ticket's `:389` line number makes. |
| **P2** | 0 flat-text sites *inside* `STATE.md` at that commit — the whole miss is the file boundary | **HIT** | **0** |
| **P3** | the positive control fires | **HIT** | C1: 2 defects, exit 1 |
| **P4** | the mutation test kills both constant detectors | **HIT** | always-DEFECT fails C2; always-CLEAN fails C1 |
| **P5** | 0 flat-text sites at HEAD in `docs/` and `STATE.md` | **HIT** | 0, over 1,754 tracked text files |
| **P6** | a non-empty NOT-a-defect set, point estimate **> 15** | **HIT** | 60 occurrences total: 26 `REPAIRED`, 23 `AUTHORITY`, 11 `FROZEN`, 0 `DEFECT` |
| **P7** | ≥ 1 occurrence in a committed transcript under `code/`; named `code/state_audit_6a2f/out_audit.txt` | **HIT** | 11 occurrences across **7** transcripts, the named one among them |
| **P8** | the proximity rule misfires, and the failure is a **false NEGATIVE** | **HIT on direction, and it was worse than predicted** | it misfired **twice**, in both directions. The false negative is the one that matters and is exactly as predicted: `repair_markers` held `STRUCK`, matched case-insensitively, so the ordinary word *"struck"* nearby laundered a live figure. Found by control C4, which I wrote to test something else. |
| **P9** | `docs/state-of-the-wall.html` carries 0 occurrences of the superseded constants | **HIT** | 0 — it carries the stale *SPREAD sentence* but no stale *figure* |
| **P10** | the registry mechanism cannot express defect 2's class (a superseded *claim*, not a *value*) | **HIT** | recorded as a declared limit, not fixed. The (A) SPREAD contradiction this same ticket repaired is invisible to this instrument. |
| **P11** | the instrument finds ≥ 1 occurrence my hand sweep missed — *"the prediction I most expect to lose, and losing it is the good outcome"* | **HIT, and it is the instrument's headline** | `docs/OneThird-lambda-std-Operative-Form.md` §7.1. See below. |
| **P12** | this instrument flags itself, and I get the exclusion wrong on the first form | **MISS** | it did not. `registry.json` listed its own directory as a declared authority from the first version, so the self-flag never happened. I filed this because that shape has bitten the arc repeatedly; it did not bite here. |

Two further predictions were implicit in P8 and are recorded as misses of detail rather than of
substance: I predicted **one** proximity misfire and there were **two**, and I predicted the false
negative would come from a site sitting near an *unrelated* repair marker, whereas it came from a
*marker word appearing as ordinary English*.

---

## P11 — the site the hand sweep missed, and it fails the OTHER way

`docs/OneThird-lambda-std-Operative-Form.md` §7.1 read:

> mg-3ce3 searched for exactly the failure event … at absolute thresholds up to `ε = 0.20`, **i.e. an
> order of magnitude above the `ε_leak ≈ 0.02` the constant budget needs**, and found 0 RED events in
> 6681 posets.

At the repaired calibration `ε_leak ≈ 0.20`, the probe ran at **exactly** the budget, not an order of
magnitude above it. Worse: **that measurement is what `mg-e35c` F5 uses to calibrate the repaired
value in the first place**, so it cannot simultaneously be evidence of headroom above that value.

**Direction.** This site made the *empirical* position look **safer** than it is. The headline site
at §6.3 made the *mathematical* position look **worse** than it is. One superseded input, two
opposite-signed errors, in the same document. The ticket asked for direction to be weighted rather
than size alone; the measurement is that direction is a **property of the site**, not of the input,
and cannot be inferred from the correction.

---

## The three defects of this instrument, left in the code

1. **C4 failed on the first form, in the false-negative direction.** `STRUCK` matched
   case-insensitively laundered live figures near the ordinary word *"struck"*. A detector that
   reports clean and a corpus that is clean then look identical — this instrument's own subject
   matter, inside this instrument. Repaired: shouted markers match case-sensitively.
2. **The ±6-line window cut a supersession box in half** and called its own tail a live claim.
   Repaired structurally (blockquote = one annotation unit), not by widening, and the new exemption
   is bounded by controls C10/C11 so one blockquote cannot silence another.
3. **The retrospective's 23 is not a blind measurement.** The registry was written by someone who
   already knew where the sites were. Stated in `s2`'s own output section 6, not only here.

## What was not checked

* No mathematics re-derived. Repaired values are `mg-e35c`'s, checked arithmetically against their
  stated inputs (`0.2²/2 = 2e-2`; `2e-2/6·n² = 3.3e-3 n²`; `2e-2·C(n,2) ≥ 1 ⟺ n ≥ 11`;
  `3C/3.3e-3 ≈ 900`; `0.5/0.2 = 2.5`) and no further.
* `mg-3ce3`'s `0 RED / 6681` was **not** re-run at source.
* `docs/state-of-the-wall.html` was **not** repaired. It is a rendered snapshot generated 2026-07-19
  and stale in more ways than this class; it carries 0 occurrences of the superseded constants, so
  it is flagged rather than fixed.
* The registry covers **one** correction event (`mg-e35c` F5) in six entries. Other superseded
  inputs in this corpus were not surveyed and are not claimed to be absent.
* Whether `mg-2860` *could* have found the fifth site with the tools it had was not established;
  only that a search would have.
