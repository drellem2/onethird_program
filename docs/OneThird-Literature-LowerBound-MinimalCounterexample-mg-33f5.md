# The literature lower bound on a minimal counterexample's size

*mg-33f5. Filed by ab6fa as the successor to mg-b6fa's verdict, as its cheapest high-payoff item.
This is a **literature** document: no theorem is proved here and no census is run here.*

---

## Answer, in one line

**A bound exists, it is a verification range and not a structural bound, and it clears nothing that
matters.** A minimal counterexample has **n ≥ 12** by a refereed result (Peczarski 2006) and
**n ≥ 15** by an unrefereed preprint ten days old (Gupta 2026). The programme's two explicit
thresholds are **n ≥ 100** (master-bound route, primitive posets) and **n ≈ 900C** (the (LIB) /
(LIB-const) crossover). **Neither bound reaches either threshold**, and neither can ever reach the
third — the `N₀` in `(LIB-weak) ⟹ (LIB-const)` — because that one is *unspecified*, which is not a
size a number can exceed.

So: the ticket's hoped-for payoff — *"an afternoon of reading that could make every `for n ≥ N₀`
statement applicable"* — **does not land**. What the afternoon does buy is real but small, and it is
sized in §3.

---

## 1. The bounds, with their exact quantifiers and hypotheses

### (L1) Peczarski 2006 — REFEREED. Minimal counterexample has **n ≥ 12**.

> M. Peczarski, *The Gold Partition Conjecture*, **Order 23** (2006), 89–95.
> doi:[10.1007/s11083-006-9033-1](https://doi.org/10.1007/s11083-006-9033-1)

The paper introduces the **Gold Partition Conjecture (GPC)**, proves **GPC ⟹ 1/3–2/3** (his
Proposition 1), and establishes GPC for three classes: **posets of width two, semiorders, and
posets containing at most 11 elements.**

**The consumed consequence.** Every non-chain poset on `n ≤ 11` has a 1/3-balanced pair.
Contrapositive: **a counterexample to 1/3–2/3 has at least 12 elements.**

**Hypotheses, stated so they can be checked against our posets.** *None beyond finiteness.* The
class is **all unlabeled posets on at most 11 elements** — no width bound, no height bound, no
thinness, no structural restriction of any kind. Our objects are finite posets. **The bound applies
to us with nothing to verify.** This is the rare case where a citation carries no side condition.

### (L2) Gupta 2026 — PREPRINT, NOT REFEREED. Minimal counterexample has **n ≥ 15**.

> Anish Gupta, *Balance Constants, Majority Cycles, and the Gold Partition Conjecture through
> Fourteen Elements*, arXiv:[2607.23926](https://arxiv.org/abs/2607.23926).
> v1 2026-07-27, v2 2026-07-30. **Ten days old at the time of writing (2026-08-07).**

Verbatim, from the abstract:

> "A second exhaustive pass over the same classes verifies Peczarski's Gold Partition Conjecture
> through fourteen elements, extending his order-11 frontier and implying in particular that the
> $1/3$-$2/3$ Conjecture holds through order 14."

Verbatim, the corollary that carries it:

> **Corollary 6.** "Every non-chain poset on at most 14 elements has balance constant at least 1/3."

**The consumed consequence: a counterexample to 1/3–2/3 has at least 15 elements.**

**Hypotheses.** Again *none* — "every non-chain poset on at most 14 elements", no class
restriction. The population is all **1,338,193,159,771** unlabeled posets on fourteen elements.
*Checked independently here:* OEIS [A000112](https://oeis.org/A000112)`(14) = 1,338,193,159,771` ✓
— exact agreement, so the paper is censusing the object we mean by "poset" (unlabeled, i.e.
isomorphism classes) and is not off by a labelling convention.

**Cumulative, not point.** The claim is *through* order 14, not *at* order 14. Orders 12 and 13
reproduce De Loof, De Baets and De Meyer, and the author reports those "as a regression, not as a
contribution"; orders ≤ 11 are Peczarski's.

**THE AUTHOR'S OWN CAVEAT, WHICH MUST TRAVEL WITH THIS CITATION:**

> "No independent per-poset check is made above order 9."

Orders 10–14 rest on internal consistency and *aggregate* external agreement (class totals against
published OEIS data), **not** on per-class independent verification. Combined with being
unrefereed and ten days old, that is the whole risk in the number 15.

**How to cite these two.** Lead with **n ≥ 12** — refereed, twenty years settled, and it is what any
argument should be built to survive. Quote **n ≥ 15** as the current computational frontier with the
preprint status attached. If Gupta is wrong the fallback is 12, and §3 shows the strategic
conclusion is identical either way.

---

## 2. Verification range ≠ structural bound. Kept apart, as the ticket demands.

Everything in §1 is a **verification range**: a claim of the form *"for all posets with n ≤ N, the
conjecture holds"*, established by exhausting isomorphism classes. It is a statement about a
finite list. It gives no reason, no mechanism, and no property of a counterexample beyond its size.

**A structural lower bound on a minimal counterexample's size does not exist in the literature.**
I looked for one and found none. §4 says what the looking was.

What *does* exist is a body of **class exclusions**. These are a different claim and **must not be
added to the census figure**. They constrain a counterexample's *shape*, and only two of them
induce a size floor at all — as a derived consequence, not as a stated bound.

| class for which 1/3–2/3 (or GPC) is proved | source | size floor it induces on a counterexample |
|---|---|---|
| width two | Linial 1984 | **none** (small posets of width ≥ 3 exist) |
| semiorders | Brightwell | none |
| height two / bipartite | — | none |
| *N*-free ordered sets | Zaguia, Electron. J. Combin. 19(2) #P29 (2012) | none |
| cover graph is a forest | Zaguia, arXiv:1610.00809 | none |
| 5-thin | SIAM J. Discrete Math., doi:10.1137/0405037 | some element incomparable to ≥ 6 others ⟹ **n ≥ 7** |
| **6-thin** | **Peczarski, Order 25 (2008), 91–103** | some element incomparable to ≥ 7 others ⟹ **n ≥ 8** |
| nontrivial automorphism | Peczarski (2017) | none — but a counterexample must be **rigid** |

*"k-thin"* means **every element is incomparable with at most k others** (Peczarski 2008, verbatim
from the publisher's abstract: "every element of the poset is incomparable with at most six
others").

**The strongest size floor the structural side yields is n ≥ 8** — and the arc's own exhaustive
census already reaches n ≤ 8. So the entire structural literature contributes **zero** to the size
question beyond what this repository already had.

**But note the direction of the residue, because it is worth more than the size floor.** These
results say a minimal counterexample must be **rigid**, of **width ≥ 3**, **not** *N*-free, **not**
a semiorder, **not** of height 2, **not** 6-thin (so *some element is incomparable to ≥ 7 others*),
and its cover graph is **not** a forest. That is structural information about the object L1b and L4
are reasoning about. **It is not a size bound and this document does not report it as one** — but
it is the part of this literature most likely to be useful, and nothing in this corpus records it
either.

---

## 3. Does it clear the thresholds? **No.** Sized, not asserted.

The two explicit thresholds, re-derived by mg-b6fa and traced here to their live sites:

| # | threshold | live value | site |
|---|---|---|---|
| T1 | master-bound route, **non-chain** (`m ≥ 1`) | needs `n ≥ 11` | audit F5, `OneThird-lambda-std-Operative-Form-IndependentAudit.md:506` |
| T2 | master-bound route, **primitive** (`m ≥ n−1`, so `d ≥ 2/n`) | needs `n ≥ 2/ε_spec = 100` | audit A1 §7.2 + F5, same file `:414`, `:506` |
| T3 | (LIB) vs (LIB-const) numerical crossover | `n ≈ 900C` | `STATE.md:13`; audit `:476` |
| T4 | `(LIB-weak) ⟹ (LIB-const)` | `N₀` **UNSPECIFIED** | `STATE.md:13`, ledger row 8 |

All at the repaired calibration `ε_spec ≲ 2×10⁻²` (audit F5). Arithmetic re-checked here and
agreeing with the audit's: `n(n−1) ≥ 1/ε_spec · 2 = 100` gives `n ≥ 11` (at `n = 10`, `90 < 100`);
`2/ε_spec = 100` gives T2.

| threshold | `n ≥ 12` (refereed) | `n ≥ 15` (preprint) |
|---|---|---|
| T1 non-chain, `n ≥ 11` | **CLEARS** | **CLEARS** |
| T2 primitive, `n ≥ 100` | **NO** — short by 88 | **NO** — short by 85 |
| T3 crossover, `n ≈ 900C` | **NO** — short by ≥ 888 | **NO** — short by ≥ 885 |
| T4 unspecified `N₀` | **UNREACHABLE IN PRINCIPLE** | **UNREACHABLE IN PRINCIPLE** |

**The one it clears is the one that does not matter.** T1 is the `m ≥ 1` form. Minimal
counterexamples are **primitive** (`STATE.md` glossary; ledger row 2), so T2 is the operative
threshold and T1 is never the live constraint. A reader who sees "CLEARS" in that row and stops
reading will draw the wrong conclusion; that is the miscitation this document most expects.

**Sizing the actual gain.** The master bound is dead for every primitive poset on `n ≤ 99`. Before
this ticket, the arc could exclude `n ≤ 8` from its own census, leaving orders **9…99 = 91**
unresolved inside the dead zone. With `n ≥ 15` the residue is **15…99 = 85**.

> **6 of 91 orders removed. 6.6%.**

Against T3 at the most favourable reading `C = 1`: `9…899 = 891` becomes `15…899 = 885` —
**6 of 891, 0.67%**. And `C` is unspecified with `C ≥ 1`, so **0.67% is an upper bound on that
gain**, not an estimate.

**T4 is the important row and it is not a matter of size.** `N₀` in `(LIB-weak) ⟹ (LIB-const)` is
*unspecified*. No finite lower bound, however large, clears an unspecified threshold — the
comparison is not unfavourable, it is **undefined**. `STATE.md`'s own sentence — *"the gap is a
QUANTIFIER, not a constant"* — is exactly right, and it means this ticket's route was never
available against T4 even in principle. **A literature lower bound can only ever help against
thresholds that are EXPLICIT.** T2 and T3 are explicit; the bound falls three orders short of them.

---

## 4. What the search was

A negative is a fact about the search until the search is stated. The negative here is §2's — *no
structural lower bound on a minimal counterexample's size exists* — and the instrument that would
have produced a positive is the same one that found L1 and L2, which it did find.

**Searched** (web search + publisher/arXiv fetch, 2026-08-07):

- `1/3-2/3 conjecture posets verified computationally all posets at most 11 elements Peczarski`
- `Peczarski "gold partition conjecture" Order 2006 verified posets "at most 11 elements" 1/3-2/3`
- `1/3-2/3 conjecture known cases width two Linial semiorders N-free height two which classes proved minimal counterexample must be`
- `"1/3-2/3 conjecture" OR "balanced pair" smallest counterexample must have at least elements lower bound structural`
- `"minimal counterexample" "1/3-2/3 conjecture" size elements at least must contain`
- `De Loof De Baets De Meyer mutual rank probabilities all posets up to 13 elements 1/3-2/3 conjecture verified`
- `Peczarski "6-thin" poset definition "incomparable to at most" gold partition conjecture Order 2008`
- OEIS A000112 cross-check of the order-14 population figure

**Sources actually opened:** arXiv abstract and full HTML of 2607.23926; arXiv abstract of
1706.04985 (Olson–Sagan); publisher abstracts via search for Order 23 (2006) 89–95, Order 25 (2008)
91–103, SIAM JDM 10.1137/0405037; OEIS A000112 values.

**Boundary — what I did NOT read.** Stated because the ticket asks, and because a bound quoted
through a secondary source is a weaker object than one read:

- **I did not read Peczarski 2006 in full.** Springer redirects to an auth IdP (HTTP 303). The
  "at most 11 elements" figure is taken from **three independent secondary reports** — the
  publisher's own abstract, the Olson–Sagan literature summary, and Gupta's introduction — which
  agree. **I did not see Peczarski's own sentence verbatim**, so the *exact quantifier wording* of
  L1 is reported at second hand. Its *content* is corroborated three ways.
- **I did not read Peczarski 2008 (6-thin) in full** — same paywall. The k-thin definition is the
  publisher's abstract.
- **I did not read De Loof–De Baets–De Meyer** (the orders 12–13 census Gupta reproduces), so the
  independence of that regression check is taken on Gupta's word.
- **I did not read the Olson–Sagan survey body** — the arXiv PDF would not parse. Only its abstract.
  The class list in §2 therefore rests on search-level summaries of that survey plus Gupta's
  introduction, and **the attributions in §2's table other than Peczarski 2008 are not
  independently verified by me.**
- **I did not verify Gupta's computation**: not the C code, not the archived data, not any
  re-enumeration. I ran no census (the ticket forbids it and mg-b6fa refuted it as impossible past
  `n ≈ 10`).
- **I did not search** MathSciNet or zbMATH (no access), nor any non-English literature, nor
  pre-1984 sources, nor sorting-theory literature beyond what GPC dragged in.
- **I did not check** whether the Gupta preprint has since been refereed, withdrawn, or superseded
  beyond its v2 listing of 2026-07-30.

---

## 5. The corpus gap the ticket asserts — independently confirmed

ab6fa's premise was that this repository has never looked. Re-checked here rather than inherited:

- `grep -rlni "verified for all posets\|no counterexample below\|exhaustively verified\|verification range"` over `STATE.md`, `docs/`, `code/` → **0 files.**
- `grep -rn "Peczarski"` over `STATE.md`, `docs/` → **0 hits.**

The corpus does cite literature, and cites it carefully: Sah, Kahn–Saks, Kahn–Linial, Brightwell,
Linial, Ma–Shenfeld, Aires–Kahn, Chan–Pak–Panova, Olson–Sagan. **The computational-verification
line is simply absent** — the corpus records its own census reach (`n ≤ 8`, 19,440 non-chain posets,
16,998 at `n = 8`; `OneThird-Counterexample-Under-The-Action.md:148`) and nothing about anyone
else's. The premise holds.

*A consistency check worth one line:* the arc's 16,998 non-chain posets at `n = 8` against
OEIS A000112(8) = 16,999 — exactly one chain removed ✓. The arc's census and the literature's are
counting the same objects.

---

## 6. Recommendation

**Land the citation, and land the fact that it does not help.** The dangerous outcome of this
ticket is a corpus that now cites "n ≥ 15" without the sentence that says it falls short of 100 and
of 900C — a bound that gets cited *as though* it discharged the `n ≥ N₀` problem is worse than the
gap it fills, because the gap was at least visible.

Suggested `STATE.md` wording (for pm-onethird, whose file it is):

> **Literature lower bound on a minimal counterexample (mg-33f5).** `n ≥ 12` — refereed:
> Peczarski, *Order* **23** (2006) 89–95, GPC (⟹ 1/3–2/3) for all posets on ≤ 11 elements, no class
> restriction. `n ≥ 15` — unrefereed preprint, Gupta arXiv:2607.23926 (2026-07-27), GPC through
> order 14 over all 1,338,193,159,771 unlabeled posets, with the author's caveat that no
> independent per-poset check is made above order 9. **These are verification ranges, not
> structural bounds, and they clear neither `n ≥ 100` (master-bound, primitive) nor `n ≈ 900C`
> (the (LIB) crossover); against the unspecified `N₀` of `(LIB-weak) ⟹ (LIB-const)` no finite
> bound can help at all.** They remove 6 of the 91 orders in the master-bound dead zone (6.6%).

**Cost of the negative half: nothing further.** There is no structural lower bound to find, the
class exclusions top out at `n ≥ 8`, and the route by which a literature bound could have
discharged the quantifier gap is closed — not for want of a large enough `N`, but because `N₀` is
unspecified. **This item does not have a successor.** The one thing in §2 that might: nobody in
this corpus has written down that a minimal counterexample must be rigid, of width ≥ 3, and carry
an element incomparable to ≥ 7 others. That is a *shape* item, not a *size* item, and it is not
this ticket.
