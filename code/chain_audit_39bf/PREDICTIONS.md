# `mg-39bf` — predictions, committed BEFORE `docs/OneThird-ChainSelection-mg-9461.md` is opened

**Item.** `mg-39bf` — *independent audit of `mg-9461`, filed late because its brief went
stale mid-run. Check the REPLACEMENT of its mid-flight self-correction, re-derive the central
claim, and check three riders.*

**Rule I am binding myself to.** Everything below is written before I open the parent's
deliverable document `docs/OneThird-ChainSelection-mg-9461.md`, before I open any script in
`code/chain_selection_9461/`, and before I run any count against the source `.tex`. Anything
already handed to me is tagged `[FORMALITY]` and is **not** a scored bet.

---

## H — EXPOSURE, DISCLOSED RATHER THAN LAUNDERED

My exposure on this item is **very large**, larger than `mg-d3c7`'s or `mg-f911`'s was, and
listing it is the only thing that stops a `[FORMALITY]` being read as a finding.

* **H1.** My dispatch's *"Recent activity"* block printed **all three** of `mg-9461`'s
  essay-length commit subjects in full. That gave me, verbatim and before any work: the
  headline ruling (*"STEP 6 CONSUMES NONE OF THE FOUR CHAINS"*), the constant
  (`ε_spec ≤ 2×10⁻²`), the byte-wise evidence (*"C_3 occurs 0 times in the whole 603-line
  file; Rayleigh/Cheeger/sqrt/std occur 0 times in Steps 5 and 6"*), the `s0` self-caught
  `count_extensions` defect, the two live guards (chain (II) refusing `C₃=1`; a `Spec` where a
  `Leak` belongs raising), the negative control on the chain arithmetic, and the
  720-poset / 7905-cut cross-check with 0 mismatches.
* **H2.** My ticket body states the self-correction **on both sides**: the struck version
  (*"chain (III) adds no open statement, (II)/(IV) each add a fifth"*) and the replacement
  (*"chain (III) needs a lemma; chains (II) and (IV) need a lemma AND a constant"*), plus the
  `40/49` threshold I am asked to test.
* **H3.** My ticket body states the optimism headline (`0.20` sits 40 % above the `n≤7`
  required-scope ceiling `1/7`) and the universal negative (*"there is no experiment that
  improves 0.20"*) verbatim.
* **H4.** Before writing this file I read: `mg-9461`'s pre-registration
  `PREDICTIONS.md` at `3cd39f1` (its **predictions**, not its conclusions); the mid-flight
  correction mail in `~/.macguffin/mail/q9461/cur/`; and the commit graph. I have **not**
  opened `docs/OneThird-ChainSelection-mg-9461.md`, `code/chain_selection_9461/README.md`, or
  any `out_*.txt`.

**What is therefore genuinely mine to get wrong:** whether the *replacement* asymmetry is
sound; whether the counts reproduce **on an instrument I proved can find something**; whether
the correction really cost nothing; whether the 40 % and its table have consistent direction;
and whether the universal negative survives an enumeration of candidate experiments.

---

## P — PREDICTIONS

### P1 `[BET 0.80]` — the md5 and the line count verify exactly

`md5 db095fbe…`, 603 lines. Deliberately near-`[FORMALITY]`: `mg-d3c7` (`6e5d88b`) already
published the same md5 prefix and the same 603 from an independent read, so two parties agree
before I start. I score this only as an instrument check on **my own** reading, not as a
finding about the parent.

> **GUARD.** A file that reads as 0 bytes, or that `md5` refuses, must be reported as
> *instrument failure*, never as *count = 0*. The eviction case (`mg-3969`) is live on this
> exact path.

### P2 `[BET 0.75]` — the zero-counts reproduce

`C₃` 0 times file-wide; `Rayleigh`/`prefix capture`/`Cheeger`/`sqrt`/`std` 0 times inside
Steps 5–6.

> **GUARD, bound now.** *No zero I publish may stand without a positive control on the same
> instrument, the same path, the same invocation* — a token I have independently established
> IS present, counted correctly, in the same run that produces the zero. A prior audit on this
> lineage shipped a broken instrument that agreed with the party under audit; the only defence
> is that the instrument demonstrates sensitivity in the same breath.

### P3 `[BET 0.45]` — **PRINCIPAL LIVE BET** — the replacement asymmetry is NOT clean

I predict the corrected sentence — *"(III) needs a lemma; (II) and (IV) need a lemma **and** a
constant"* — is **over-stated in at least one direction**, most likely because chain (III)'s
own open statement (L2) is *also* quantitative, i.e. it does not merely have to be *true*, it
has to be true *with a good enough constant*, in which case (III) needs "a lemma and a
constant" too and the asymmetry collapses back toward the tie it corrected **from**.

The specific failure mode I expect: `C₃ = 1` for chain (III) is **conditional on L2**, and L2
proved in a weaker form would give `C₃ = 1+δ` rather than `C₃ = 1`. If so the parent has
smuggled the constant into (III) as "already known" because a *sweep* pinned it at 1, which is
numerical evidence, not a proved number — the same category of thing it charges (II)/(IV) with
lacking.

> **GUARD.** I may only score P3 as held if I quote, from `Op-Form` §4.2–4.3 or the parent's
> own text, the **exact open statement** each chain rests on, and show that (III)'s is
> quantitative in the same sense (II)/(IV)'s is. If (III)'s open statement really is purely
> qualitative — a true/false disjunct with no free constant — P3 is **LOST** and I say so.

### P4 `[BET 0.30]` — the optimism table has a direction defect in at least one row

The headline arithmetic itself I expect to be **right**: `0.20 / (1/7) = 1.4`, i.e. 40 % above.
That much is a `[FORMALITY]`-grade check. The bet is that some *other* row of the table has an
inverted sign or an inverted comparand — most plausibly a row where a *smaller* `ε_leak` is
the *safer* direction and the table scores it as optimistic, or a row comparing against
`ε_spec` (a square of `ε_leak` through Cheeger) as if it were commensurable with `ε_leak`.
The square is the live trap on this lineage; `mg-d3c7` named it.

### P5 `[BET 0.55]` — the universal negative is over-claimed

*"There is no experiment that improves 0.20; only a proof moves it."* I predict I can name at
least one candidate class of experiment that would move the operative figure and that the
parent does not dispose of. My advance candidates, named now so I cannot invent them after
reading:

1. a **larger-`n` exhaustive or randomised sweep** producing a *smaller* required-scope
   ceiling, which moves the *gap between* 0.20 and what is required (the optimism, not the
   number, but the optimism is what the sentence is about);
2. a **search for a better constant in the step that consumes `ε_leak`** — if the consuming
   inequality has slack, a numerical optimisation over its free parameters lowers the demanded
   `ε_leak` without any new lemma;
3. an **adversarial search for the worst poset family**, which could *raise* the demand and
   thereby show 0.20 is not merely optimistic but refuted — an experiment that "improves" the
   figure's *status* by killing it;
4. a **witness search for the prefix-capture fraction** at moderate `n`, which is precisely
   the number `40/49` is compared against, and is measurable.

If the parent has already enumerated and disposed of all four, P5 is **LOST**.

### P6 `[BET 0.40]` — something WAS invalidated by the correction

The parent reports *"nothing had to be discarded"*. I predict at least one artefact
pre-dating the correction is materially touched by it. Concretely: `3cd39f1` carries `17/78`
at line 98 and the `10×` at lines 68/82/84, and the correction's items 1 and 3 are exactly
those two objects. Whether that is *load-bearing* is what I have to determine — line 98 may be
a mere arithmetic example.

> **GUARD.** *"Appears in the text"* is not *"was discarded"*. I must show a **prediction, a
> derivation, or a deliverable sentence whose truth value changes** under the correction
> before scoring P6 held. A worked example that happens to use the numeral is not that.

### P7 `[BET 0.30]` — rider (a) is already in the corpus

The claim that Op-Form 4.3's `n`-freeness is conditional on `C₃` being a constant, so
`n`-freeness holds for exactly one of the four chains. I predict this is already stated
somewhere — most likely `mg-94c3` (the audit of `C₃ = 1`) or `mg-345e`.

### P8 `[BET 0.35]` — the timeline in my own ticket is wrong

My ticket says the correction landed *"~40 minutes in"*; the mayor's dispatch note says
*"~5 minutes into its run"*; the mail itself says *"You were dispatched ~5 minutes ago"*. Two
of these cannot both be right. I predict the ticket body's *40 minutes* is the wrong one, and
that the correction was **sent** before `3cd39f1` was authored (contradicting the ticket's
*"the correction landed after it"*) even if it was **read** afterwards.

---

## E — ERRORS I EXPECT TO MAKE, FILED IN ADVANCE

* **E1.** I score the asymmetry LOST because I read *"a constant"* as *"a decimal number"*
  where the parent means *"a quantitative strengthening"*. **Guard:** quote the parent's exact
  words for each chain's open statement before scoring P3 either way.
* **E2.** I publish a zero produced by a broken instrument — the precise failure the ticket
  warns of, and the one I am most likely to commit because I will feel the check is trivial.
  **Guard:** P2's guard above, enforced by an assertion in the script, not by my intention.
* **E3.** I build the timeline on the ticket's own *"40 minutes"* rather than on mtimes and
  author dates. **Guard:** every time in my report must cite a file mtime, a mail `Date:`, or
  a git author date.
* **E4.** I re-attack `ε₀` or re-derive `C₃ = 1`, both explicitly forbidden. **Guard:** if a
  line of my analysis needs either, I cite `mg-845e` / `mg-76b2`+`mg-94c3` and stop.
* **E5.** I quote `17/78` without its scope, the exact defect struck at `7cd8ae7` today.
  **Guard:** grep my own deliverable for `17/78` before committing and require the scope
  clause within the same sentence.
* **E6.** I accept the parent's `s1` chain solver as independent confirmation of the parent's
  chain arithmetic. It is the parent's own route and the ticket forbids exactly this.
  **Guard:** any chain arithmetic I confirm must be re-solved from the `Φ` bounds by my own
  code, or scored as *unverified*.
* **E7.** I conflate `ε_leak` and `ε_spec` across the Cheeger square while checking the
  optimism table, producing a factor-of-`ε` error and calling it the parent's.
  **Guard:** every figure in my table carries its unit, spelled, in the same cell.
