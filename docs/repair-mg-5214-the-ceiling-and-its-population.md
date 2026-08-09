# mg-5214 — the ceiling and its population: `17/78` KEEPS ITS NUMBER AND GAINS ITS SCOPE

**Work item:** `mg-5214`. **Parent:** `mg-3969` (the L4-threshold `ε₀` result).
**Finding repaired:** `mg-d3c7` §4, the independent audit of that result.
**Date:** 2026-08-09. **Files edited:** `docs/OneThird-L4-Threshold-eps0-mg-3969.md`
(the live document), `code/eps0_threshold_3969/README.md` (the seventh site, §5), and one
pointer paragraph in `docs/OneThird-L4-Threshold-eps0-mg-d3c7-IndependentAudit.md` §4.5.
**`STATE.md` is NOT edited** — it carries none of the affected figures yet (§7).
**No code written.** The instrument this repair rests on is `code/eps0_audit_d3c7/`, landed by
`mg-d3c7` at `6e5d88b`; it was **re-run in full before any document was edited** (§3).

---

## 0. WHAT WAS WRONG, IN ONE SENTENCE

**`mg-3969` published a proven ceiling `ε₀ ≤ 17/78 = 0.2179` and a "under 9 % of headroom"
claim without saying, in the same sentence, that both are measured on a *restriction* of the
population the architecture needs — and on the population it actually needs, the same threshold
is `0`.**

The number is right. The number is *exactly* right: `mg-d3c7` re-derived it on a third code
path (`e(P) = 26`, `Δ₁ = 17/78`, all four landings `9/13, 19/26, 19/26, 4/13`, slack `0` on all
four) and then attacked it — exhaustively over all **96 428** naturally labelled posets on `[7]`
and all **578 568** prefix cuts there is **no `U_either` violator thinner than `17/78`** in its
own scope. **Nothing is withdrawn here.** What is added is the scope, and the result that lives
outside it.

## 1. THE TWO POPULATIONS, AND WHY ONE OF THEM IS THE REQUIRED ONE

| | population | `n ≤ 7` cuts | `U_either` violators | thinnest `Δ₁` | uniform `ε₀` |
|---|---|---|---|---|---|
| **BOTH** | cuts at which **both** sides are non-chain — `mg-3969`'s sweeps | 335 496 | 682 | `17/78 = 0.217949` | `≤ 17/78` |
| **ONE+** | cuts at which **at least one** side is non-chain — **architecturally required** | 604 012 | 2 042 | `1/7 = 0.142857` | **`0`** |

**ONE+ is the required one, and `mg-3969` says so itself.** On a minimal counterexample disjunct
(i) is false by hypothesis, so a pair must transfer from *a* side. A single chain side merely
means the pair comes from the other one; only the *both*-sides-chain case is genuinely out of
scope, and that case is settled by Remark 5.0 (two chain sides force width `≤ 2`; Linial's
theorem covers width 2).

**And `mg-3969` disclosed the gap correctly, in §9:** *"My sweeps skip every cut at which either
side is a chain — a coverage gap I did not close… a sweep that includes them may lower both."*
That prediction was right in direction and understated in size. `mg-d3c7` closed it.

## 2. IT IS NOT A LOWER CEILING — IT IS NO CEILING

`1/7` is the `n ≤ 7` figure, not the answer. The answer is a family.

Let `P(n,k)` be the chain `c₁<⋯<c_{n−1}` plus one isolated element `z`, with
`A = {z, c₁,…,c_{k−1}}` (a down-set, so a legitimate prefix cut) and `B = {c_k,…,c_{n−1}}` (a
chain, contributing no pair). Then `e(P) = n`; `p^P(z<c_j) = j/n` while `p^A(z<c_j) = j/k`;
`Δ₁ = (n−k)/(n·min(k,n−k))`; and a pair `(z,c_j)` balanced in the side (`k/3 ≤ j ≤ 2k/3`) is
evicted in `P` as soon as `n > 2k`. Taking `n = 2k+1`:

```
        Δ₁  =  (k+1) / ((2k+1)·k)   →  0     as k → ∞,
```

with **every** balanced-in-side pair evicted at every `k ≥ 3`.

> **`ε₀(U_either) = ε₀(U_smaller) = 0` on the architecturally required population.
> REFUTED AT EVERY POSITIVE `ε` — not capped at `17/78`, and not capped at `1/7` either.**

`U_smaller` falls to the same family because `|A| = k < n−k = |B|`, so the *smaller* side is the
non-chain one. Verified in exact rationals to `k = 200` (`Δ₁ = 201/80200 = 0.0025`, 67
balanced-in-side pairs, none surviving), with the hand formulae for `e(P)` and `Δ₁` agreeing at
every member and the brute-force `n!` path agreeing at `n ≤ 9`.

## 3. WHAT I RE-RAN BEFORE EDITING A WORD

A repair that publishes a scope is subject to the defect it repairs: it can quote a figure
whose population it has not itself checked. So every figure this repair writes into the live
document was reproduced first, from `mg-d3c7`'s committed instrument, in this worktree.

| script | what it establishes | result |
|---|---|---|
| `b0_selftest.py` | 8 controls, incl. **C2**: the two totals | `SELFTEST PASSED`; non-chain cuts `12+117+1424+24115+578562 = 604 230`, all-poset cuts `14+120+1428+24120+578568 = 604 250`, **difference exactly the 20 chain-poset cuts** |
| `b4_fullsweep.py 7` | BOTH vs ONE+ side by side | BOTH: 335 496 cuts, 682 / `17/78`, and `13/111` for `U_smaller` — **matching `mg-3969` exactly**. ONE+: 604 012 cuts, 2 042 / `1/7`, `U_smaller` `13/111` |
| `b6_family.py` | the family, exact rationals | every member a `U_either` **and** `U_smaller` violator; `Δ₁ → 0` |
| `b7_scope_and_arith.py` | D1, D2, D3, D4 | D1: `δ(P) = 3/7, 4/9, 5/11, 6/13, 15/31 ≥ 1/3` at every member. D2: `58 755` reproduced **exactly and only** under a designated-side tie rule (`58 538` tie-excluded, `58 560` tie-neither). D3: all eight published arithmetic figures `[ok]` |

This is **replication, not independent derivation** — I ran `mg-d3c7`'s code, I did not write my
own. The independent check already exists and is `mg-d3c7`'s: it shares no code with
`code/eps0_threshold_3969/`. What my re-run establishes is that the committed transcripts match
what the scripts print today, which is the thing a document quoting them needs.

## 4. THE TWO THINGS THIS REPAIR IS NOT

**It does NOT touch L4, and that was verified rather than assumed.** Every member of the
refuting family has `δ(P) = ⌊n/2⌋/n ≥ 1/3`, so **L4's disjunct (i) holds outright** and
L4-as-stated is satisfied at every one of them (`b7` D1). What falls is `mg-3969`'s deliberately
**(i)-free** surrogate — and (i) *had* to be dropped, for the reason `mg-3969` §5.1 gives: on a
minimal counterexample (i) is false by hypothesis. The surrogate was the right object to build,
and being refutable is what a right object looks like.

**It does NOT weaken `mg-3969` — it sharpens it.** `mg-3969`'s leading conclusion is that
`ε₀^cons` is structurally unmeasurable and that proving it positive **is** the conjecture
(Claims 5.1–5.2, which `mg-d3c7` did not re-derive and did not contest, and which this repair
leaves untouched). It offered `ε₀^unif` as the honest, refutable replacement target. The finding
is that the replacement target is *itself refuted*. So the parent's thesis — **there is no
measurable positive threshold here** — comes out stronger than it was stated, not weaker. Only
its published bound needed a scope.

If a later reader takes this repair to mean "`mg-3969` was wrong", the repair has been
mis-scoped in the opposite direction and has become a second version of the same defect.

## 5. THE SIX SITES, AND WHAT EACH NOW SAYS

All in `docs/OneThird-L4-Threshold-eps0-mg-3969.md`.

| # | site | was | now |
|---|---|---|---|
| **1** | §0 verdict table | statement column said *"asserted for **all** posets"*, bound column bounded the both-sides-non-chain restriction — **two different objects in one row** | a **population column**, both restricted rows labelled `335 496` cuts, and a **new row** for the required population carrying `ε₀ = 0`, PROVEN, with the family as its witness |
| **2** | §0 headroom | *"`ε₀` cannot be raised by more than 9 %, ever, at any `n`"* | the 9 % is stated **as a fact about the restriction**, beside the required-population reading where the calibration `0.20` is a factor `1.4` **above** the `n ≤ 7` value `1/7` and above the uniform value `0` by everything; closes with *"may not be quoted without it"* |
| **3** | §0 close + §7 recommendation | *"`mg-845e` should be released against `ε₀(U_either) ∈ (0, 17/78]`, the only one a proof can ever produce"* | **struck, kept visible, and replaced.** That interval is **empty** on the required population. The replacement records what *can* be recorded: the `n`-free form, `ε_dem = ε₀²/2` exactly, `17/78` **with its restriction**, and that no positive uniform threshold exists |
| **4** | §10 proposed `STATE.md` text | `17/78` and *"under 9 % of headroom and no more"* with **no scope qualifier** — **the text proposed for landing** | replaced with text that carries the scope in the same sentence, publishes `ε₀ = 0` beside it, and says explicitly that the qualifier may not be dropped. Superseded version kept struck beneath it |
| **5** | §5.2 `604 230` vs §6.0 `604 250` | both correct, **neither labelled**, 20 apart | each labelled with its population (non-chain posets' cuts vs all posets' cuts), and the difference named as the chain posets' `2+3+4+5+6 = 20` |
| **6** | Claim 6.2 / §6.0 tie cell | the `n = 6` fallback witness at `1/7` sits at an `|A| = |B| = 3` **tie** where side `A`'s pair `1/2 → 3/7` **survives**; the designated-side convention was real, consistent, and **undeclared** | convention **declared** in §6 with the counts that identify it (`58 755` vs `58 538` vs `58 560`), and a rider on Claim 6.2 giving the tie-neutral `n ≤ 6` ceiling `13/74 = 0.17568`. **Headline `13/111` unaffected** — its witness has sizes `4` and `3` |

§9's coverage-gap bullet is also updated to record that the gap is closed and how it came out,
and §11 gains the four reproduce lines for `code/eps0_audit_d3c7/`. Four further in-document
mentions that quoted `17/78` or the 9 % unqualified — §3's one-line answer for `ε₀^unif`, §6.0's
"where this lands against the corpus's number", §8's K11 row, and §9's `n = 7` bullet — were
found by sweeping **every** occurrence of `17/78`, `9 %` and each population figure after the
six sites were done, and are repaired too (§6 below).

**A seventh site, outside the document.** `code/eps0_threshold_3969/README.md` asked *"what about
the uniform **(all-posets)** transfer threshold?"* and answered `17/78`. That is the same defect
in the parent's own instrument README, and the parenthetical is the exact word the sweep does not
support. It now carries the restriction, a scope note, the tie convention, and the population
labels for `604 230` vs `604 250`.

## 6. THE SWEEP OVER MY OWN REPAIR

A repair that publishes a scope is an artifact of the same kind as the defect, so it can commit
the defect: quote the number, forget the qualifier, one paragraph further down. After the six
sites were edited I swept the whole document for every occurrence of `17/78`, `13/111`, `1/7`,
`9 %`, `604 230`, `604 250`, `335 496` and `604 012` and read each in place.

| what the sweep found | disposition |
|---|---|
| §3's `ε₀^unif` one-liner: *"bounded above by `17/78` uniformly in `n`"* — no scope | repaired: carries both the restriction and the `= 0` result |
| §6.0's *"correct to within 9 % of a bound that is now proven, and it can never be raised further"* — **the twin of site 2, and I had not been sent to it** | repaired: 9 % stated as a fact about the restriction, with a rider showing the comparison **inverts** without it (`0.20` is a factor `1.4` *above* `1/7`) |
| §8's K11 row: `604 230` unlabelled, `17/78` unscoped | repaired: population named, restriction named, refutation added |
| §9's `n = 7` bullet: *"`U_either` unchanged at `17/78`"* | repaired: scope added, plus the note that the refuting family is a construction and not bounded by `n = 7` |
| §6.0's new ONE+ `U_smaller` row would have introduced a **fresh** unlabelled convention (`58 730` is tie-excluded, unlike the document's `58 755`) | labelled at the point of first use, so the repair does not re-commit the defect it names in site 6 |
| the two struck blocks (§7's old recommendation, §10's old text) still contain unqualified `17/78` and "under 9 %" | **left as they are, deliberately.** They are struck, labelled as superseded, and their whole purpose is to show what the unqualified version said |

## 7. WHAT I DID NOT DO

* **I did not edit `STATE.md`.** It carries no `17/78`, no `0.2179`, no `604 230` and no 9 %
  headroom claim today — checked by `grep` before starting — so the defect had **not** yet
  propagated there. §10 is the text *proposed* for landing, and landing it remains
  `pm-onethird`'s call; what this repair guarantees is that whatever gets landed from §10 now
  carries its scope.
* **I did not re-derive anything independently.** §3 is replication of `mg-d3c7`'s instrument.
  The independent path is `mg-d3c7`'s own, and `mg-3969`'s four instruments were not run by me
  at all.
* **I did not re-open Claims 5.1/5.2, L4, `C₃`, or `mg-3ce3`'s numbers.** All taken as they
  stand; the repair is about scope on a published bound, not about any of them.
* **I did not extend any sweep.** Everything exhaustive here stops at `n = 7`, exactly as both
  parents' did. The `ε₀ = 0` result is not a sweep at all — it is a family with a hand proof,
  checked in exact rationals to `k = 200`.
* **I did not touch `mg-845e`.** §7's repaired recommendation is input to it, not a discharge of
  it. That it is now unblocked and that §7's old text would have pointed it at an empty interval
  is precisely why this repair was routed ahead of it.
* **I did not edit `docs/roadmap.md`, and it carries the defect at two lines.** Its
  2026-08-09 18:30Z sweep says *"`eps_0(U_either) <= 17/78` and `eps_0(U_smaller) <= 1/7`, both
  uniform in n. Our calibrated 0.20 is within **9%** of a ceiling that can never be raised"*
  (`:30–32`) and *"`eps_dem <= (17/78)^2/2 = 0.023751` [PROVEN ceiling] … **under 19% of
  headroom**"* (`:37–38`) — both unscoped, and the `U_smaller` figure there is the superseded
  `1/7` rather than `13/111`. **That file is `pm-onethird`'s**: it is generated, its header says
  it prepends rather than regenerates, and the section carrying these lines already self-labels
  **"Status: CONDITIONAL AND UNAUDITED. mg-d3c7 is the pre-filed independent audit and is now
  dispatchable."** The audit has now returned, so the next sweep is the right place to resolve
  it. **Flagged to `pm-onethird` by mail rather than edited**, because a polecat rewriting a
  dated generated record is how two versions of one history get created.
