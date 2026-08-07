# mg-345e — predictions for the PAIR-BIAS / L4 INDEPENDENCE question

**Committed before any script of this instrument exists.** Written after reading
`docs/OneThird-lambda-std-Operative-Form.md` (736 lines) end to end, `STATE.md`, `mg-6bc2`,
`mg-92e6`, and the head of `docs/OneThird-Direct-Prefix-Route-mg-2de0-Audit.md`. Everything I
already know from that reading is filed below as a **DISCLOSURE**, not laundered into a
prediction. Only the rows marked **P** are bets.

---

## Disclosures — hand measurements already in my possession, so they are not predictions

**D1.** `mg-88bd`'s claim ledger (`Op-Form:626–668`) records claim 23 — the (LIB-const)
statement `E[inv_e] ≤ (ε_spec/6)(n²−1)` — as **CONDITIONAL on 18 and 21**, and claim 18 as
**CONDITIONAL on 17**, and 17 as **CONDITIONAL on 1, 4, 13, 16**. Claim **4 is "L4's `F` is
`n`-free"**. So the *demand* chain's dependence on L4 is already recorded in the document's own
ledger and I do not have to discover it.

**D2.** The same ledger records claims **25** (`frozen ⟹ E[inv_e] < m/3`) and **26** (freezing
alone gives (LIB-const) with constant `2/3`) as **PROVEN**, unconditionally, with no
`CONDITIONAL on` clause of any kind.

**D3.** `Op-Form:§6.3` states the pair-bias output as `1 − λ_std < d·n/(n+1)` with
`d = m/binom(n,2)`, and says it reproduces mg-210d's recorded degenerate bound exactly.

**D4.** `Op-Form:§6.4` gives the demand budget as
`ε_spec ≤ ε_leak²/(2C₃)` with **`C₃` UNQUANTIFIED**, and `Op-Form:§8.1` records that the
Prefix-capture conjecture that would quantify `C₃` is both **open** and, as literally worded,
**too weak to use**.

**D5.** `STATE.md:15` carries `ε_spec ≲ 2×10⁻²` with **no `C₃`** — i.e. the live headline figure
silently sets `C₃ = 1`. `0.20²/2 = 2×10⁻²` is the `C₃`-free arithmetic.

**D6.** `mg-e35c` F5 (quoted in the `Op-Form` banner) establishes that under the *recommended*
(iii)-repair **`F` does not appear in branch (iii) at all**, so there is no
`F(ε_leak) < slack` condition left to calibrate.

**D7.** `STATE.md` row 11 records `mg-3af9` (audited `mg-c8c6`) as: branch (ii) is unconsumed by
Step 6's stated transfer for **every strictly positive modulus**. Branch (i) is trivial and
contains no `F`.

**D8.** `docs/OneThird-Direct-Prefix-Route-mg-2de0-Audit.md:0` answers "does the contradiction
follow with NO spectral statement?" with "**on the route repaired: yes**", headline constant
`2/3`, and `:218–221` traces the direct and spectral routes to the **same `ε_leak`**.

**D9.** `STATE.md:17` and the *why it is hard* paragraph record that both faces of the single
lemma are **false for abstract frozen distributions**, so any improvement must use real-poset
realizability. `mg-92e6`'s own ticket states the marginal/joint boundary in the same terms.

**D10.** The 1/3–2/3 conjecture is verified for **all** posets to `n = 14`
(`mg-33f5`, Gupta arXiv:2607.23926) — so the frozen class `δ(P) < 1/3` is **empty at every `n`
this corpus can enumerate**, chains aside.

---

## P — the bets

| # | prediction | why I might be wrong |
|---|---|---|
| **P1** | Mechanising the `Op-Form` ledger's own `CONDITIONAL on` clauses and taking the transitive closure will put **claim 23 in the dependents-of-4 set** and **claims 25, 26 outside it**. | The encoding is mine; a mis-parse of a prose "CONDITIONAL on" would produce this answer for the wrong reason. The mutation control exists for this. |
| **P2** | The dependents-of-4 set will have **between 4 and 8 members** (I have not counted; I have only walked 23→18→17→4 by eye). | I may be missing indirect dependents through 12 and 33. |
| **P3** | **No claim on the supply path** — 22, 25, 26, 27, and the master-bound claims 21 — will reach claim 4. **0 surprises.** | Claim 21 is `CONDITIONAL — cited from mg-210d`; if I encode "cited from" as a dependency edge to something that itself touches 4, the supply path would light up. I predict it does not, and if it does I will report it rather than re-encode. |
| **P4** | My exact-rational algebra check will reproduce **`ε_pairbias(n, d) = d·n/(n+1)`** from `E[inv_e] < m/3` and the (LIB-const) definition, and reproduce `E_unif[footrule] = (n²−1)/3`, at **0 mismatches**. | This is my own algebra and it is the thing most likely to be wrong. |
| **P5** | The supremum of `d·n/(n+1)` over `d ≤ 1` is **1**, and no value **strictly below 1** is obtainable from per-pair information alone without an upper bound on `d` for frozen posets. I predict **the corpus contains no such upper bound** — a grep for a frozen-conditional *upper* bound on incomparability density returns **0 hits**. | The corpus is large and I have read a small part of it. `mg-e2de`'s co-degree ≥ 2 result is a *lower* bound on local density and might have an upper-bound corollary I have not seen. |
| **P6** | The mutation control — inject a fabricated edge `26 ← 4` — will make the detector report claim 26 as L4-dependent, i.e. the detector is **not** constant-NO. | If my reachability is written to special-case the supply claims, the mutation passes vacuously. This is the failure shape this arc keeps producing. |
| **P7** | **This ticket's own headline will be a split verdict, and I will be tempted to report it as a clean (A).** I predict I write at least one sentence that states the independence without naming which of the two `ε_spec` questions it is about, and that I have to repair it before landing. | — |
| **P8** | **My own most likely error, filed in advance:** conflating "an `ε_spec` that is *constant, uniform in n*" (a property of the SUPPLY bound) with "an `ε_spec` that *suffices*" (a property of the DEMAND threshold). **This is exactly the conflation `pm-onethird` made on 2026-08-07 and had to reverse**, and the ticket warns me about its neighbour (consumption vs provability). I am predicting I make the *other* one. | — |
| **P9** | The `Op-Form` ledger has **36** claims and I will encode **36** nodes; the number of encoded dependency edges will be **between 12 and 20**. | Pure guess on the edge count. |
| **P10** | I predict the instrument **cannot express** the finding that matters most — that the demand side is gated on L4's *threshold* `ε₀` rather than its *modulus* `F`. That is a reading of what Step 6 consumes, and no dependency graph over a claim ledger can carry it. **The mechanised part of this ticket is the cheap part.** | — |

---

## What this instrument is NOT

It audits the **recorded dependency structure of `mg-88bd`'s claim ledger**, not the mathematics.
A claim whose ledger label understates its true dependencies will be scored as independent here.
That is a real limit and it is why the doc argues the independence from the *mechanism* as well,
and does not rest on the graph.

It performs **no poset enumeration**. Per D10 the frozen class is empty everywhere it could be
enumerated, so any empirical calibration of the pair-bias constant would be measuring a
hypothetical population. **The one cheap check that looks attractive — sweeping near-frozen
posets — is declared and NOT run**, for that reason.
