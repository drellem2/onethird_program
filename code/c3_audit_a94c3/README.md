# `c3_audit_a94c3` — mg-94c3's independent audit of mg-76b2

**Work item.** `mg-94c3`. **Audits.**
[`docs/OneThird-C3-PrefixCapture-mg-76b2.md`](../../docs/OneThird-C3-PrefixCapture-mg-76b2.md)
and `code/c3_prefix_capture_76b2/`, as merged at `7b7d093`.
**Deliverable.**
[`docs/OneThird-C3-PrefixCapture-mg-94c3-IndependentAudit.md`](../../docs/OneThird-C3-PrefixCapture-mg-94c3-IndependentAudit.md).
**Predictions.** [`PREDICTIONS.md`](PREDICTIONS.md), committed at `e200f18` **before any script
of this instrument existed**.

```
sh run_all.sh          # ~30 s, all sections expected to exit 0
```

## 1. Independence, concretely

`libA94.py` shares **no line** with `lib76b2.py`. It is written from
`spectral_near_ordinal_sum_program.tex` directly:

| object | source line | why it matters here |
|---|---|---|
| `R(σ)e_a = e_{σ(a)}`, `(T_P)_{xa} = Pr[x` at position `a]` | `tex:130–146` | fixes `σ : position → element`, the exact point at which `mg-76b2 §8` reports a live bug in a sibling instrument |
| `S_P = ((T_P+T_Pᵀ)/2)|_H` | `tex:160–163` | |
| `⟨1_A,(I−S_P)1_A⟩ = E|A∖σ(A)|` | `tex:220–227` | checked BOTH ways (matrix, and counting over `L(P)`) — a single path can be wrong the same way twice |
| `Φ_P(A) = E|A∖σ(A)|/|A|`, `Δ₁` | `tex:229–237`, `:270–278` | |

There is **no numpy on this machine**, so the eigen path is a hand-written cyclic Jacobi
solver. That is an accident of the environment and it is the right accident: the two
instruments share no linear-algebra dependency either.

Exact `Fraction` arithmetic for every conductance, Rayleigh quotient and ratio built from
them. Floating point **only** for eigenvalues, and every figure that depends on one is
labelled FLOAT where it is printed.

## 2. Sections

| script | what it does |
|---|---|
| `selftesta94c3.py` | **NC1–NC6, the negative controls.** Every detector shown failing on purpose. |
| `a1_algebra.py` | **The one thing the ticket asks first.** Re-derives `n ≥ 4C₃/ε_leak² − 1` from Op-Form, exact rationals, brute-force search vs closed form at 30 grid points; checks WHICH normalisation each side is in; exhibits invariance under consistent conversion and the ~6× error under a mixed one; re-derives all four chains. |
| `a2_dictionary.py` | Re-derives Lemmas 2.1, 3.1, 3.2, 3.3 from the source and measures each. Scores P1, P2, P3. |
| `a3_currency.py` | The adversarial section: three currencies for `C₃`, measured **restricted to posets that exhibit L2's first disjunct**. Scores P4, P5, P8. |
| `a4_census.py` | The L4 census (verified at `mg-3ce3`'s source, in another repo) and the `mg-200d` census. Scores P6, P7. Re-checks mg-76b2's claim 14 against Op-Form. |

## 3. Scoring

| # | outcome | note |
|---|---|---|
| P1 | **HELD** | 0/25684; factor 2 attained 4812× |
| P2 | **HELD** | 0/4377; worst `Φ²/(2(1−λ_std)) = 0.2813` |
| P3 | **HELD** | 0/6132; red drill 3340/3340 |
| P4 | **HELD** (bet 70%) | `C₃^gap > 1` at 1023 of 1032 posets **that exhibit L2's FIRST DISJUNCT**, worst `2.386`. This is correction `C1`. *(scope added at the claim, `mg-be0b`; this read "that exhibit L2". `L2` is a **disjunction**, so the unqualified form claims a population this instrument never built — its filter is `mono == "YES"`. **No figure moves and nothing is marked false**: `1023 of 1032` was true as measured. The `a3_currency.py` row above already carried the scope and always did.)* |
| P5 | **MISSED** (bet 45%) | 16/16 of §7's figures reproduce — once a defect of *mine* is removed (§4 below) |
| P6 | **HELD** (bet 80%) | and verified at `mg-3ce3`'s predicate, not against mg-76b2's scope statement |
| P7 | **HELD** (bet 75%) | 1 of 24 claims falls; 6 machine-bare sites all read as labelled by hand |
| P8 | **HELD** (bet 65%) | chain-(III) constant is `1` at 1032/1032 |
| P9 | **AVOIDED, and it was live** | the error I filed against myself — reading `Φ*_pref/Φ*` as what the theorem is about. P4's result is exactly the material that would have produced it. |
| P10 | **AVOIDED** | `C1` is reported as FRAMING, in the ticket's own words |

Hand measurements `H1`–`H10` were **disclosed in `PREDICTIONS.md` before any script existed**
and are NOT scored as predictions. `H4` (invariance under consistent conversion) and `H5` (the
mixing error is worth ~6×, optimistically) are the two that carry the audit's headline, and
both were derived by hand first and machine-confirmed second.

## 4. Defects of this instrument, kept in the source

Three of the four were caught by my own negative controls firing **against correct code**.

1. **`c = ρ_max/λ_std` divided by zero at the antichain** (`λ_std = 0`, so `c` is `0/0`) and
   printed `min c = 0.000` at every `n`. `mg-76b2`'s population is smaller than mine by
   exactly 1 at every `n` and **its exclusion is the correct one**. `P5` scored HELD on this
   artefact before the fix and MISSED after — the fix cost me a prediction and it is reported
   that way round.
2. **`NC2` dropped its own hypothesis**: it asserted Lemma 3.3's conclusion about whatever
   vector Jacobi returned for the antichain — `[0.707,−0.707,0,0]`, not monotone — and failed
   against correct code. Fixed by using the source's own tied vector `(a,a,a,−3a)`.
3. **`NC3` ran `n = 3,4,5`** and reported `8177/11312` against `mg-76b2`'s `8178/11316`. Its
   `n ≤ 5` **includes `n = 2`** and the single missing disagreement is the 2-chain witness the
   document itself names.
4. **The conditional-marker classifier counted the word `window`** — the noun a conditional
   qualifies, not the qualifier. `NC5` caught it. The 6 remaining machine-bare sites are
   reported and then read **by hand**, not tuned away; tuning the regex until it returned `0`
   would have made the census unfalsifiable.

## 5. Declared limits

- `n ≤ 6`. Every `n`-growth statement is a **direction**; a finite population can refute a
  uniform-in-`n` bound and can never establish one.
- `0` of `4376` primitive posets here are inside the budget `ε_spec ≤ 2×10⁻²` (smallest gap
  `0.0562`), so **every `C₃` figure is measured outside the regime it would be used in**.
- Degenerate top eigenspaces (163 posets) return `UNDECIDED` rather than being searched, so the
  monotonicity test is *sufficient* only and `mg-76b2`'s existential search is the stronger
  instrument. `1727 + 163 = 1890` reconciles the two counts exactly.
- `ε_leak = 0.20` is **HEURISTIC** — `mg-3ce3`'s envelope — and is not pinned here.
- Every `1−λ_std` is FLOAT (Jacobi). Comparisons that could turn on float noise are stated with
  their tolerance (`1e-9` for eigen-multiplicity and inequality slack, `1e-12` for zero-gap).

## 6. `a4_census` is pinned to an as-of commit (`mg-c824`)

`a4_census.py` prints **line numbers into documents it does not own** — `mg-76b2`'s
deliverable, `mg-76b2`'s instrument, `Op-Form`, and `mg-3ce3`'s probe *in another
repository*. Those addresses are not a property of anything this audit established. Between
this transcript's commit and 2026-08-13 the deliverable was amended twice (`ade980b`,
`bb6a0ff`) and the instrument once (`48cbbd8`), so a re-run moved **32 lines and changed no
verdict** — the same statements, found at new addresses.

That made `out_a4_census.txt` **non-reproducible by construction**, and the cost was not
cosmetic: this lineage repairs labels under a numbers-neutrality method whose step 1 is
*"reproduce the committed output byte-identically before touching anything"*, so the method
**could not be applied to this file at all**. `mg-be0b` stopped its sweep here for exactly
that reason.

**The fix pins the bytes rather than reformatting the numbers.** A line number into someone
else's file is a volatile address by nature and no printing convention makes one stable;
what *can* be made stable is the thing addressed. `a4_census` now reads its corpus at a
declared commit via `git show` — `AS_OF = 7b7d093`, the commit §0 above already names as
what this audit audits, and the same bytes the transcript's own commit `c80a4f1` saw (blobs
`1b8184c5`, `c406c73f`, tree `f69cdef3`, identical at both).

| | |
|---|---|
| pinned re-run | **byte-identical**, for as long as `AS_OF` is reachable |
| `A4_CENSUS_AT=HEAD` (or `=WORKTREE`, or any commit) | re-measures and **re-addresses**; measured against `HEAD` at `4c68992`, **every differing line is an address, the corpus-size line, or the as-of block**, and **all seven verdicts are identical** |
| `mg-3ce3`'s probe | in another repository and unpinnable from here, so its `sha256` is stamped instead and `D1b`'s addresses are declared valid at that digest |

The transcript now opens with an **as-of stamp** naming what is an address and what is a
finding, and each address list is marked where it is printed. The label repair at the `C₃ = 1`
row of `a4_census.py`'s dependency list — `:77` as `mg-be0b` addressed it — (`← L2` →
**L2's FIRST DISJUNCT**, the site `mg-be0b` stopped at) landed
under the numbers-neutrality method after the pin, and it passes: **23 of 23 addresses
unchanged, no numeric token of the previous transcript lost, and the only four lines that do
not survive verbatim are the three headers whose colon moved and the repaired label itself.**

### This remedy exhibited the defect it repairs, and the enumeration caught it

The scope note added at `:77` first cited **`STATE.md:116`** — a line number into a document
`a4_census` does not own, i.e. the exact defect, reintroduced inside its own repair. It was
**already wrong when written**: that text sits at `STATE.md:126` today. It now cites the
**ledger row** (`row 9`) and quotes the disjunction verbatim. A row number is an identity; a
line number is an address.

Two residual costs, stated rather than left to be discovered:

1. **`AS_OF` must stay reachable.** If it is ever pruned, `a4_census` exits non-zero with an
   actionable message — deliberately, rather than falling back to a live read and emitting a
   transcript that silently disagrees with the committed one.
2. **`a4_census` now needs `git` and a work-tree.** Copied outside a repository it fails;
   `A4_CENSUS_AT=WORKTREE` is the escape hatch and reproduces the pre-pin behaviour.

Pinning also makes this suite eligible for `build.sh`'s looped set for the first time. It is
**not** added here — out of scope for `mg-c824`.

### The general finding: `a4_census` is not the only one — 64 instruments, 98 transcripts

A count, not an impression. Over every tracked `code/**/out_*.txt`, an address `path:NNN` was
taken as **computed into a foreign file** when (a) the path resolves to a tracked file outside
the transcript's own instrument directory, (b) the literal token `path:NNN` does **not** occur
in that instrument's own `.py`/`.sh` (which would make it a hardcoded citation, a
stale-citation hazard but not a reproducibility one), and (c) the instrument actually reads
that file — it names it, or walks the tree.

| measure | count |
|---|---|
| transcripts carrying a computed foreign address | **105** |
| distinct instruments | **64** |
| instruments where the addressed file has **already moved** since the transcript was committed | **40** |
| transcripts whose addresses are therefore presumed **already stale** | **54** |

So the defect is not rare and it has already fired in a majority of the instruments that
carry it. **None of them is fixed here** — `mg-c824` says name them and it will be scoped.
The full list is in this ticket's verdict mail to `pm-onethird`. The classifier's known bias
is toward over-counting (an instrument that merely *echoes* a foreign file's own prose
citation is counted), and toward under-counting addresses into files outside this repository,
which `git ls-files` cannot see at all — `a4_census`'s own `mg-3ce3` probe is one such.

**One mislabel found in passing and deliberately not fixed.** `code/gate_fixed_point_f771/`
attributes `mg-c824` to `code/libweak_audit_c4f5/out_a4_census.txt` — in `lib_f771.py`'s
*WHAT IS WATCHED* paragraph, in `g1_controls.py`'s membership row `E5`, and inside both
committed gate transcripts. (Cited by paragraph and by row, not by line, for the reason
this section is about.) The two
files share a basename; `mg-c824`'s is **this** one. The gate's *logic* is unaffected (it
watches everything, regenerates nothing, and `E5`'s point holds of either file), so this is a
label, not a defect — and repairing it would regenerate a `build.sh`-looped gate's transcripts
inside a repair whose whole warrant is that nothing moves.
