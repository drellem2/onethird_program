# `code/primitivity_f5be/` — mg-f5be's instrument

**Work item.** `mg-f5be`. Filed by `pm-onethird` on Daniel's observation that `mg-409a`'s
ceiling witness `Z_n` is an ordinal sum, hence **decomposable**, while counterexamples to
(1/3)–(2/3) are **primitive**.

**Deliverable.** [`docs/OneThird-Primitivity-Objection-mg-f5be.md`](../../docs/OneThird-Primitivity-Objection-mg-f5be.md)

**Run.** `./run_all.sh` (arms `p0`–`p3`, ≈100 s). `p4` is the `n = 8` extension and takes
substantially longer; it is run separately and its transcript is committed.

## Arms

| arm | what it settles | cost |
|---|---|---|
| `p0_selftest.py` | enumeration counts against OEIS A000112/A001035, primitivity against named posets, the exact `alpha == 1` test against `lib409a`'s Jacobi, `delta`/`mu` controls | 5 s |
| `p1_chain.py` | **`pm-onethird`'s chain**, link by link, exactly, at every incomparable pair of every poset to `n = 6` | 4 s |
| `p2_primitive.py` | **alpha restricted to the primitive class**; whether `alpha = 1` is attained by any primitive poset; what the attaining set actually is | 46 s |
| `p3_frozen.py` | the **frozen** class — empty, and reported as empty; the near-frozen measurement | 4 s |
| `p4_n8.py` | the primitive census extended to `n = 8` (2 585 classes, max `alpha` = 0.3122, none attaining 1), with a colour-refined canonical form validated against brute force first | ~35 min |

## Populations, and what "exhaustive" means in each row

- `n ≤ 6`: **every isomorphism class** (1, 2, 5, 16, 63, 318 — checked against OEIS
  A000112 in `p0.1`, and the labeled counts 1, 3, 19, 219, 4231 checked against
  `lib409a`'s independent generator).
- `n = 7`: **every isomorphism class** (2 045, checked) for the enumeration itself, and
  **every primitive class** (234) for the alpha measurement. The *full* `n = 7` population
  is **not** measured for alpha.
- `n = 8`: **every primitive class** (2 585, `p4`). The full population is not enumerated,
  but the `n = 8` primitive enumeration is seeded from the **full** `n = 7` population and
  not the primitive one — deleting a maximal element from a primitive poset can *create* a
  module, so seeding from primitives would silently miss classes.

Posets with `|L(P)| = 1` — the chains — are excluded throughout: `mg-409a`'s theorem is
stated for `|L(P)| ≥ 2`, and a chain has no incomparable pair, so `delta` and `mu` are
extrema over the empty set. `p0.6` checks that asking for them **raises** rather than
returning a number.

## Independence, stated because a reader must price it

`lib409a` is **imported**, not re-implemented: posets, linear extensions, the two
compressions, the fibers, `Pi_o`/`Pi_e`, `M = 2I − Pi_o − Pi_e`, and the BK Dirichlet form
all come from `mg-409a`'s library. That is deliberate — this ticket audits a claim *about*
that object, so a second construction would make any disagreement uninterpretable. The
consequence is stated as **D5** in the deliverable: a defect in `lib409a`'s fiber
construction would propagate here undetected. What *is* built from scratch: enumeration up
to isomorphism, modular/ordinal decomposition, the pair statistics, the chain, and the
exact `alpha == 1` test.

## Exactness

Every `PASS` in this directory is an exact rational comparison, an exhibited rational
witness, or a combinatorial count. Two floats exist — `alpha_power` here and
`lib409a.jacobi_eigenvalues` — and both are **measurement**. In particular the headline
"the primitive maximum is 0.3876…" is a **measurement**; the statements carrying verdicts
are the exact ones: *no primitive poset attains `alpha = 1`* (exact rational orthogonality
test) and *every primitive poset in range carries an exhibited rational witness with
`R_M ≤ 525/832 < 1`*.
