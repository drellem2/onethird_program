# `eps0_threshold_3969` — is L4's THRESHOLD `ε₀` `n`-free, and what is its value?

Instruments for `mg-3969` (clause (a) of `mg-845e`'s gate). Findings, provenance and the
source quotation live in [`docs/OneThird-L4-Threshold-eps0-mg-3969.md`](../../docs/OneThird-L4-Threshold-eps0-mg-3969.md);
this file is the operating manual.

**This directory says NOTHING about L4's MODULUS `F`.** `F` is not computed anywhere in it. The
threshold and the modulus have already been conflated twice on this lineage; the instruments are
built so that the conflation is not available — no script here ever measures a drift magnitude, and
every predicate is a membership test in `[1/3,2/3]`.

## Exactness

Every quantity is an exact `Fraction`. **No float appears on any decision path** — floats occur
only inside `%.6f` in report lines, never in a comparison that decides an outcome. `Date`/`random`
are not used; the enumerations are deterministic and complete.

## What each script establishes

| script | question | headline |
|---|---|---|
| `lib3969.py` | — | source definitions (`Δ₁ :270–278`, `Φ :229–237`, `p_xy :59–62`, `δ :63–66`), each quoted at its site |
| `a1_vacuity.py [nmax]` | can the **consumable** threshold be measured? | **No.** 604 230 prefix cuts over every **non-chain** poset with `n ≤ 7`; disjunct (i) fires at every one, so the consumable statement holds at `ε = 1` throughout and the measurement is structurally vacuous |
| `a2_uniform.py [nmax]` | what about the **uniform** transfer threshold, **on cuts at which BOTH sides are non-chain**? | **`ε₀(U_either) ≤ 17/78`** (witness `n = 6`, **unchanged** when the sweep is extended to `n = 7`) and **`ε₀(U_smaller) ≤ 13/111`** (witness `n = 7`; the `n ≤ 6` run gives the weaker `1/7`), both uniform in `n` — **and both only within that restriction**, see the scope note below |
| `a3_witness.py` | is the witness real, or a bug in the extension builder? | both witnesses re-derived by brute force over all `n!` permutations — **no shared code with the sweep** — with a pair-by-pair certificate |
| `a4_mechanism.py [nmax]` | *why* does the transfer fail? | **not only** the `δ = 1/3` endpoint gap: a pair at `p_side = 1/2`, maximal interior slack `1/6`, is evicted at `Δ₁ = 5/19`. My own prediction lost |

```bash
python3 a1_vacuity.py 7     # ~2 min at n=7, ~2 s at n=6
python3 a2_uniform.py 6     # ~9 s        (n=7 takes ~40 min — run it detached)
python3 a3_witness.py       # instant
python3 a4_mechanism.py 6   # ~3 s
```

Committed outputs: `out_a1_vacuity.txt` (`n ≤ 6`), `out_a1_vacuity_n7.txt`, `out_a2_uniform.txt`
(`n ≤ 6`), `out_a2_uniform_n7.txt`, `out_a3_witness.txt`, `out_a4_mechanism.txt`.

`a3_witness.py` certifies the **`n = 6`** witnesses, which are the ones the `n ≤ 6` run reports. The
`n = 7` `U_smaller` witness that lowers that ceiling to `13/111` is reported by `a2` only and has
**not** been through the second code path.

## Poset encoding, and why it is complete

A poset on `[n]` for which `0 < 1 < … < n−1` is a linear extension is exactly a transitively closed
set of pairs `(i,j)` with `i < j`. Every finite poset has a linear extension, so it can be
relabelled into this normal form: enumerating those relations enumerates **every isomorphism
class**, with multiplicity.

That argument is checked rather than trusted — **NC5** double-counts (labelled poset, linear
extension) pairs:

```
n! · |poset_iter(n)|  ==  Σ over ALL labelled posets of e(P)
```

with the right-hand side built from an independent enumeration (all `3^C(n,2)` pair orientations,
transitivity-filtered), so a systematically missing class cannot cancel. It agrees exactly at
`n = 3,4,5`: `42`, `960`, `42 840`. A size check ("the count looks about right") would not catch a
missing class; this does.

## Controls, all firing

| id | control | why it is there |
|---|---|---|
| **PC1** | `{a<b} ⊔ {c}` has `|L| = 3` and `δ = 1/3` **exactly** | positive control on the `δ` code, and it is `Op-Form` Claim 3.3's own poset |
| **NC1** | a chain has `Δ₁ = 0` at every prefix and no `δ` | catches an off-by-one in the `σ(A_k)` convention |
| **NC2** | the antichain gives `Δ₁ = Φ = (n−k)/n` at `n = 4,5,6` | reproduces `Op-Form` §4.2's hand computation **and** Lemma 2.1's `Φ = Δ₁` identity, independently |
| **NC3** | `Δ₁ ≤ 1`, approached: `2/3, 3/4, 4/5, 5/6, 6/7` | the hand bound `\|A∖σ(A)\| = \|σ(A)∖A\| ≤ min(\|A\|,\|B\|)` |
| **NC4** | a deliberately **wrong** predicate — exact preservation `p^P = p^side` — fails at 9 986 cuts | if it did not fail, the instrument could not tell predicates apart and every green would be meaningless |
| **NC5** | completeness double-count (above) | the enumeration is the load-bearing assumption of every count reported |

## Reading the results without over-reading them

* **SCOPE (added `mg-5214` after `mg-d3c7`'s audit — read this one first).** `a2_uniform.py`
  sweeps **only cuts at which BOTH sides are non-chain**. That is a *restriction* of the
  population the architecture needs, which is **at least one** side non-chain. On the required
  population the `n ≤ 7` `U_either` ceiling is `1/7`, and an explicit family (a chain plus one
  isolated element, `n = 2k+1`, `Δ₁ = (k+1)/((2k+1)k) → 0`) makes the uniform threshold
  **`0` — refuted, not capped** — on both readings. `17/78` and `13/111` are correct and
  exactly reproduced *within the restriction* (three independent code paths) and must be quoted
  with it. See `code/eps0_audit_d3c7/b4_fullsweep.py`, `b6_family.py`, and
  `docs/repair-mg-5214-the-ceiling-and-its-population.md`. **This does not touch L4**: every
  family member satisfies disjunct (i) (`δ(P) = ⌊n/2⌋/n ≥ 1/3`).
* **TIE CONVENTION (added `mg-5214`).** `U_smaller` at an `|A| = |B|` cut uses a **designated
  side**; that is what reproduces the `58 755` failure count (`mg-d3c7` `b7` D2 — `58 538`
  tie-excluded, `58 560` tie-neither). Under a tie-neutral reading the `n ≤ 6` `U_smaller`
  ceiling is `13/74`, not `1/7`. The headline `13/111` is tie-independent.
* **POPULATION LABELS (added `mg-5214`).** `a1`'s `604 230` counts cuts of the **non-chain**
  posets; `a2`'s `604 250` counts cuts of **all** posets. The difference is exactly the chain
  poset at each `n`, `2+3+4+5+6 = 20`. Both are right for their own instrument.
* The ceilings bound a threshold **uniform in `n`**. They do **not** say `ε₀(n) ≤ 17/78` for a fixed
  `n`; at `n ≤ 5` there is no `U_either` violator at **any** `ε`.
* The ceilings are on the **`F`-free repaired** transfer statement (`mg-e35c` F5's form). They are
  **not** a refutation of L4-as-stated, whose branch (ii) remains available on every witness here.
* `a1`'s zero column is the point, not a null result: it is what "structurally unmeasurable" looks
  like when you go and look.
* Cuts are prefixes of the identity linear extension. The architecture's cut is a prefix of the
  **distinguished order** (`:82–86`), which exists only for counterexamples — the natural analogue,
  not the same object.
