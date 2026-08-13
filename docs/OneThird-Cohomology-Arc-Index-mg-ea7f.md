# The cohomological (F-series) arc — index, status, and where it lives (mg-ea7f)

*Five index entries and their pointers. **Not** a précis of the mathematics: the mathematics is in
the linked documents, in another repository, and this file exists so that the next person who asks
about it is **routed** rather than answered from memory.*

**Nothing in this file is load-bearing for `STATE.md`'s ledger.** The F-series is a **sibling**
programme — the compatibility-geometry / cohomological attack, pursued in
`one_third_width_three` — not a link in this repository's spectral / near-ordinal-sum chain. It is
indexed here because it was **not indexed anywhere**, and an unindexed result is worse than an
absent one (§ *Why this file exists*).

⚠️ **All paths below are in `../one_third_width_three/` unless stated otherwise**, written relative
to this repository's root and following the convention `STATE.md` rows 3b and 6 already use. **All
12 resolve from the canonical checkout** (`/Users/daniel/research/onethird_program`) and from no
other, which is a property of every cross-repo link in this record, not a new one.

**Search terms this file exists to be found by**, since being found is its entire function:
*cohomology, cohomological, homology, sphere, spherical, Čech (ASCII: Cech), `Pos_n`, `PPF_n`,
`Δ_n`, F17, F18, F28, F31, UCC, sheaf, obstruction class, `ω_bal`, discrete Morse.*

---

## The five entries

### 1. F17 + F18 — **GREEN, unconditional.** The sphere theorem for `Pos_n`.

`Hyp(n)`: for the poset `PPF_n` of proper partial orders on `[n]` (order complex `Δ_n = Δ(PPF_n)`),

> `H̃^k(Δ_n, Q) = 0` for `0 < k < n − 2`, and `H̃^{n−2}(Δ_n, Q) = sgn_{S_n}` — for **every** `n ≥ 3`.

Proven by an induction whose two inputs are both closed:

- **F17** (`mg-4d3a`, verdict **GREEN-equivariant-uniform**) — an `n`-uniform `S_n`-equivariant
  cofiber discrete-Morse reduction gives `H̃_d(Δ_{n+1}/Δ_n) ≅ 2·H̃_{d−1}(Δ_n)` as `S_n`-reps,
  **unconditionally**, all `n ≥ 3`; hence **(UCC.1) ⟺ Hyp(n)** — the inductive hypothesis
  re-expressed, not an independent input.
  [`compatibility-geometry-F17-equivariant-cofiber-morse.md`](../../one_third_width_three/docs/compatibility-geometry-F17-equivariant-cofiber-morse.md),
  ledger [`state-F17.md`](../../one_third_width_three/docs/state-F17.md). Harness 21/21.
- **F18** (`mg-d039`, verdict **GREEN-ucc2-proven**) — the inclusion `ι_n : Δ_n ↪ Δ_{n+1}` is
  null-homotopic, by the explicit `S_n`-equivariant poset zig-zag `ι_n ≤ κ_n ≥ const_{ω_n}` with
  `κ_n(x) = x ∪ ω_n`. **Uses no hypothesis whatsoever**, hence non-circular by construction.
  Therefore `ι_n^* = 0` and **`δ_n` is injective for every `n ≥ 3`** — **(UCC.2)**, unconditional.
  [`compatibility-geometry-F18-ucc2-delta-injective.md`](../../one_third_width_three/docs/compatibility-geometry-F18-ucc2-delta-injective.md),
  ledger [`state-F18.md`](../../one_third_width_three/docs/state-F18.md). Harness 43 677/43 677.

With both, **(UCC) is complete and the F10 cohomological core is UNCONDITIONAL** (F18 Thm 5.3):
`Hyp(n)` for all `n`, and the balanced-pair obstruction class
**`ω_bal^{(n)} ∈ H̃^{n−2}(Δ_n, Q)^{sgn}`** exists and is unique up to scale, with `±1` pairing.

**This is the entry that was answered wrongly.** It is GREEN, it is unconditional, and it is
**not** in the Frankl / union-closed arc.

### 2. F28 — **AMBER**, the functoriality wall.

`mg-d0fa`, verdict **AMBER-framework-unclear**. The sheaf-cohomology-on-`POSET` framework is
well-defined and operational at the constant-coefficient level — that is exactly where F17+F18
lands — but **no candidate BK-derived sheaf `F_BK` on `PPF_n` is both functorial under refinement
and admits a canonical morphism `φ : F_BK → F_ℓ ≅ Q_`** that F17+F18 could then constrain. Without
that morphism, the sphere theorem cannot be pointed at low-conductance configurations.
[`compatibility-geometry-F28-sheaf-cohomology-on-POSET.md`](../../one_third_width_three/docs/compatibility-geometry-F28-sheaf-cohomology-on-POSET.md),
ledger [`state-F28.md`](../../one_third_width_three/docs/state-F28.md) §5.1, §7.6.

### 3. F31 — **RED**, terminal for the Čech-bias closure route.

`mg-01ce`, verdict **RED-injectivity-fails-chain-locality-obstruction**. `Φ_*` is **not** injective
on the bad-cut Čech class: `Φ` is built only from a chain's own cover relations and per-step
probabilities, so the whole chain-locally-buildable sgn-isotype `K_chain-loc` sits inside
`ker(Φ_*)` — and the bad cut's *defining* feature is precisely the kind of data that puts it there.
F30's `c_BC(P) = 0` is therefore **structurally generic, not a contradiction**. All three candidate
refinements (richer cover, stabiliser-orbit, twisted coefficients) wall on either F17+F18-anchor
breakage or chain-locality persistence, so AMBER is not the honest verdict.
[`compatibility-geometry-F31-phi-star-injectivity.md`](../../one_third_width_three/docs/compatibility-geometry-F31-phi-star-injectivity.md),
cumulative ledger [`state-F29.md`](../../one_third_width_three/docs/state-F29.md) (session 3).
Predecessors: F29 `mg-70b0`
([`compatibility-geometry-F29-cech-bias-cohomology.md`](../../one_third_width_three/docs/compatibility-geometry-F29-cech-bias-cohomology.md)),
F30 `mg-c3fe`.

**Routes walled for milestone-1 part (iii): five, and the count in that document disagrees with
itself.** F31 §6.3's table has **five rows** — Route A (F25 `mg-c6f2`, RED), Route B (F25/F27, RED),
hybrid spectral→cohomology (F27 `mg-a3e3`, RED), sheaf-cohomology-on-`POSET` (F28 `mg-d0fa`, AMBER),
Čech-bias (F29→F30→F31, RED) — and the prose under it calls Čech-bias *"the fifth route"*. The
headline phrase in the same section is nonetheless **"four routes walled"**, inherited verbatim from
the F31 ticket body, which was written **before** the fifth row existed. Read the table, not the
phrase. *(Reported, not repaired: the document is another repository's.)*

### 4. F31 retracts nothing upstream. **The closure route is dead and the sphere theorem is alive.**

This is the single most misreadable point in the arc, and a record carrying only *"walled"* would
produce the **mirror image** of the wrong answer already on file. F31 §6.5 lists what its RED does
**not** touch, and F17+F18 head that list:

- **F17 + F18** (`mg-4d3a`, `mg-d039`) — GREEN, unchanged.
- **F-series cohomological core parts (i)–(ii)** — unconditional post F17+F18; unaffected.
- **F19–F23 chamber-Morse arc**, **`mg-b345` Quillen-fiber route (iii)** — parked, untouched.
- **The Lean `width3_one_third_two_thirds` 4-axiom artifact** — trust surface unchanged.
- **`main.tex` + Steps 1–8** — Route B mathematically correct conditional on Hyp A; unchanged.
- **F30's unconditional dissolve of U1** in the chain-level dialect — unchanged; F31's wall is
  *chain-locality*, a **different** obstruction from F28's *functoriality* wall (F31 §4.4).

F31 walls a **specific closure route**. It refutes nothing.

### 5. The cross-repo pointer itself.

**The F-series lives in `one_third_width_three`, not here.** F8–F31, their state ledgers
(`state-F17.md`, `state-F18.md`, `state-F28.md`, `state-F29.md`) and their harnesses
(`scripts/compat_geom_F*.py`) are all in that repository's `docs/` and `scripts/`. Nothing in
`onethird_program` reproduces them and nothing here should: this file is an **index**, and the
`../one_third_width_three/` links above are the whole of its content.

**The scoping documents behind the arc**, for anyone reconstructing how it was set up:
[`compatibility-geometry-posn-sphere-scoping.md`](../../one_third_width_three/docs/compatibility-geometry-posn-sphere-scoping.md)
(`mg-5ee2`) and
[`compatibility-geometry-poset-cohomology-scoping.md`](../../one_third_width_three/docs/compatibility-geometry-poset-cohomology-scoping.md)
(`mg-d60d`).

---

## The *other* cohomological arc, and why the two get confused

There is a **second**, genuinely separate cohomological line: the **Frankl / union-closed** arc, in
`union_closed` — [`docs/Frankl-Cohomology-Synthesis.md`](../../union_closed/docs/Frankl-Cohomology-Synthesis.md),
closed by `mg-5cc6` with **"No"** across 15 probed constructions.

**Both statements are true and they are about different objects.** The Frankl arc is closed. The
1/3–2/3-side sphere theorem is F17+F18 and is **GREEN and unconditional**. Answering a question
about the second with the status of the first is the exact error this file exists to prevent, and it
is the error that was made (below).

---

## Why this file exists

**Measured at `mg-ea7f` (2026-08-13):** `STATE.md`, `EXECUTIVE-SUMMARY.md` and `README.md` contained
`cohomolog`, `homolog`, `sphere`, `Čech` — **0, 0, 0, 0 times each.** The entire arc was invisible
from every top-level record document in this repository.

It fired twice.

- **2026-08-06 (`mg-e768`).** Daniel: *"i remember that we proved the whole category pos_n is
  spherical, but i can't remember if we proved anything for individual posets."* The provenance
  answer on record placed the spherical work in the Frankl / union-closed arc and reported that
  route closed. **Half right.** The Frankl half is correct and separately closed; the 1/3–2/3-side
  sphere theorem is F17+F18, GREEN and unconditional, and that half of the answer was **wrong**.
- **2026-08-13.** Daniel asks again from a different angle — *"cohomology of Pos_n is S^(n−2), pair
  bias yields cohomology constraints, and relative cohomology of the poset in the category creates a
  contradiction"* — and asks where it got blocked. Answering it took a full-corpus search across
  2,852 items and four repositories.

**A record that omits a result does not merely fail to answer it — it lets a confident wrong answer
be assembled from what remains, because the true source is not there to contradict it. An absence is
not neutral.**

## What this file is subject to, said before someone finds it

**A remedy is an artifact of the same kind as the defect, so it is subject to that defect.** Two
ways this index can be exactly the thing it repairs, both real:

1. **It is an index of five entries, not a census of the F-series.** F8–F16, F19–F24 and F26 are
   named here only in passing (F19–F23 as *parked*, F10 as the cohomological core) and are **not**
   indexed with status. A reader who takes silence here as absence there would be making, one level
   down, the mistake this file was written to stop. The sibling repository's `docs/` is the census;
   this is a route to it.
2. **Every status above is a snapshot at 2026-08-14 and nothing checks it.** No instrument in this
   repository reads `one_third_width_three`; no pin covers these twelve paths; no gate fails if a
   verdict there moves or a file there is renamed. A GREEN that turns AMBER next door turns nothing
   here. That is the same class of defect one repository over, and it is stated rather than fixed.

**And the class is not fixed by this file.** A corpus can only be audited for what it *says*; it is
never audited for what it *omits*. Every instrument in this programme reads documents that exist and
checks claims that are written; nothing scans for a load-bearing result that no document mentions,
which is why this survived from 2026-05-16 until a human asked twice. `mg-5998` records the same
**shape** of defect on a different subject (the shape of a minimal counterexample, written nowhere)
— read for the pattern, not as a duplicate. **No ticket currently closes the class.**
