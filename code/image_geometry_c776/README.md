# `code/image_geometry_c776/` — mg-c776's instrument for *where the image of `P -> pi(Unif(L(P)))` sits inside `M_n`*

Deliverable: [`docs/OneThird-ImageGeometry-mg-c776.md`](../../docs/OneThird-ImageGeometry-mg-c776.md).

Subject: `mg-8b32`'s `C4`. Its `T4` closed the inside of a fiber (`max H` over a realizable fiber
is exactly `log2 e(P)`, attained at `Unif(L(P))`, so the `M_n` relaxation is already tight fiber by
fiber) and its `C3` therefore put **the entire slack of the `M_n` ceiling on marginal vectors that
are not of the form `pi(Unif(L(Q)))`**. What is left is one question:

> **Characterise the image `R_n = { pi(Unif(L(P))) : P a poset on n elements }` inside `M_n`.**

## 1. The answer, in the ticket's own order of value

| the ticket asked for | what is here |
|---|---|
| a separating condition satisfied by image points and violated off-image | **exists, and is exact** (`c1`): `pi` is an image point iff `pi = r(pi)` where `r(pi) := pi(Unif(L(P(pi))))`. Equivalently `R_n` is the set of **vertex-barycentres of the box-faces of `M_n`**. It is NOT `b4.4`-circular — it names neither `e(P)` nor an entropy |
| the image's convex position | **the worst possible** (`c2`): `R_n` contains every vertex of `M_n`, so `conv(R_n) = M_n` and **no inequality valid on the image cuts anything off the body**. 97.2% of the image at `n = 5` is non-extreme in its own hull |
| how far a non-image point of `M_n` can sit from the image | **`1/6` in sup norm at the point that matters** (`c4`): the two-atom law's marginal vector `pi*` carries the whole ceiling, and the nearest image point to it is the antichain, at exactly `1/6`, at every `n` |
| whether hypothesis (1) alone confines you near it | **no** (`c4.3`): `pi*` satisfies hypothesis (1) at every pair with the bound attained, and the image point nearest to it is the **worst violator of hypothesis (1) there is** (`delta = 1/2`). `r` moves the objective the wrong way, `C(n,2)/3 -> C(n,2)/2` |

**And where the image meets hypothesis (1) it lands on ground already surveyed** (`c3`): the
boundary class is **rigid** — every poset with `delta(P) <= 1/3` has **every** incomparable pair at
flip **exactly `1/3`**, so `eps_spec(P) = d(P) * n/(n+1) = eps_sup(P)` EXACTLY and the pair-marginal
supply is **attained** rather than merely valid. **THAT IS `docs/FACTS.md` F23** (`mg-6ff4`),
already registered and exhaustive to `n = 9` where this arm reaches `n = 7`. `c3` is corroboration
by a third route and says so in its own header; what this ticket adds is the consequence read from
the image side — **no fact about the image can move `eps` except through `d`**, which is F23's own
`NOT` field and `mg-6ff4` §9's declared non-bridge.

## 2. What is here

| arm | question | headline |
|---|---|---|
| `c0` | do the objects work? | poset enumerator against OEIS A001035 to `n = 6`; `L(P)` against filtering `S_n`; the down-set DP against counting `L(P)`; a planted defect caught on 200 of 219; **`lib8b32` imported here and nowhere else**, 0 disagreements on 238 posets |
| `c1` | the characterisation | `R_n = Fix(r) = ` the box-face barycentres; `r . r = r` on 600 exact body points; two planted near-misses fail it |
| `c2` | can it be an inequality? | **no** — `conv(R_n) = M_n`, 300 seeded directions, 0 separations |
| `c3` | inside hypothesis (1) — **CORROBORATION of F23, not discovery** | the strictly frozen population is **empty** at `n <= 6`; on the boundary every pair is at exactly `1/3`; `d_max = 2/3, 1/3, 1/5, 4/15, 4/21` and `\|B_n\| = 1,2,3,5,8` at `n = 3..7`, each agreeing with `mg-6ff4`'s closed forms term by term |
| `c4` | how far, and which way | `1/6` at `pi*`, attained uniquely at the antichain; `r` increases `E[inv_e]` |

Run: `sh run_all.sh` — 38 s of CPU measured on this host, five arms green, transcripts committed.
Deterministic: re-running produces byte-identical transcripts (checked), and no arm prints a path,
so no transcript here is operator-valued (`mg-4020`'s defect, avoided by construction).

## 3. The population warning, which governs every number in `c3`

`delta(P) < 1/3` is the counterexample condition and the conjecture is verified to `n = 14`
(`mg-33f5`), so **the strictly frozen population is empty at every `n` an instrument can reach** —
`c3.1` re-establishes that exhaustively over all 134 492 labelled posets at `n <= 6` rather than
quoting it. Every number after `c3.1` is measured on the **closed boundary `delta <= 1/3`**, which
is a different set from the hypothesis. This is `docs/FACTS.md` F1's own warning, and it is why the
deliverable states the boundary results as `FP` about the boundary and **not** as evidence about
frozen posets.

`mg-8b32`'s `b4.3` calls the same closed set "the hypothesis population" — its `72 of 219` at
`n = 4` is reproduced here as 48 non-total posets plus 24 total orders, which is how the two
instruments are known to be talking about the same set.

## 4. Independence, and the one import

Nothing here imports `lib0fc6`. `lib8b32` is imported by **`c0` alone**, deliberately: this
directory's poset enumerator is extension-by-a-new-element (not filtering `3^C(n,2)` sign
patterns) and its marginal map is a forward/backward down-set DP (not a walk over the support), so
agreement on 238 posets is agreement between two routes. Importing it in an *arm* would convert
that evidence into a tautology, which is `mg-8b32` §3's discipline applied to `mg-8b32`.

The `n = 7` sweep is exhaustive rather than sampled for an exact reason, and the reason is
**verified on the full population before it is used**: `c3.1` checks over all 134 492 labelled
posets at `n <= 6` that every boundary poset has a coherent `L*` and is a subrelation of it, so
relabelling `L*` to the identity loses nothing and the whole population sits among the transitive
subrelations of the `n`-chain (96 428 of them at `n = 7`). A restriction validated only inside its
own image validates nothing.

## 5. What this directory does NOT do, and where it could be wrong

- **It does not re-run `a2.3`, `mg-8b32`'s `b3` witness search, or `mg-0fc6`'s `M_n` separation
  sweep.** `pi*`'s optimality over `M_n` (`= C(n,2)/3`) is **cited** to `mg-6bc2` Claim 3.1 and
  `mg-0fc6` `a3.3` for general `n`; the witness itself is rebuilt here so the table's numbers are
  this file's own, but the *maximality* is not re-derived.
- **`c3`'s rigidity is `FP` at `n <= 7`, and it is F23's result, not this branch's.** F23 is `FP`
  at `n <= 9`; the closed forms `4*floor(n/3)/(n(n-1))` and `sum_k C(n-2k, k)` are `mg-6ff4`'s and
  are cited, not re-derived. This arm measures five terms of each and agrees.
- **`c4.5` is a SAMPLE and is labelled one.** The maximum of `dist(pi, R_n)` over the whole body is
  not computed; 120 seeded exact points give a lower bound on it and nothing else.
- **`c1.4`'s two-vertex near-miss is idempotent**, measured on all 219 posets at `n = 4`. That is
  printed rather than swapped out, because it is the useful half: idempotence is not the content of
  `T1`, *which set is fixed* is.

## 6. Provenance

`pc776`, 2026-08-13, from `mg-c776`, the successor `p8b32` recommended and `pm-onethird` adopted.
Of the two facts `mg-8b32` left homeless, **one is filed** as `docs/FACTS.md` F25 — re-derived here
independently in `c3.4` rather than copied, and given a *reason* a re-measurement alone would not
have produced — and **the other is deliberately not filed**, because F23 already carries it as the
`n = 6` value of a registered closed form. The deliverable's §8 says why.
